import { getDb } from "../db.js";
import { teardownWorkflowCronsIfIdle } from "./agent-cron.js";
import { emitEvent } from "./events.js";
export function getWorkflowStatus(query) {
    const db = getDb();
    // Try run number first (pure digits)
    let run;
    if (/^\d+$/.test(query)) {
        run = db.prepare("SELECT * FROM runs WHERE run_number = ? LIMIT 1").get(parseInt(query, 10));
    }
    // Try exact task match, then substring match
    if (!run) {
        run = db.prepare("SELECT * FROM runs WHERE LOWER(task) = LOWER(?) ORDER BY created_at DESC LIMIT 1").get(query);
    }
    if (!run) {
        run = db.prepare("SELECT * FROM runs WHERE LOWER(task) LIKE '%' || LOWER(?) || '%' ORDER BY created_at DESC LIMIT 1").get(query);
    }
    // Also try matching by run ID (prefix or full)
    if (!run) {
        run = db.prepare("SELECT * FROM runs WHERE id LIKE ? || '%' ORDER BY created_at DESC LIMIT 1").get(query);
    }
    if (!run) {
        const allRuns = db.prepare("SELECT id, run_number, task, status, created_at FROM runs ORDER BY created_at DESC LIMIT 20").all();
        const available = allRuns.map((r) => {
            const num = r.run_number != null ? `#${r.run_number}` : r.id.slice(0, 8);
            return `  [${r.status}] ${num.padEnd(6)} ${r.task.slice(0, 60)}`;
        });
        return {
            status: "not_found",
            message: available.length
                ? `No run matching "${query}". Recent runs:\n${available.join("\n")}`
                : "No workflow runs found.",
        };
    }
    const steps = db.prepare("SELECT * FROM steps WHERE run_id = ? ORDER BY step_index ASC").all(run.id);
    return { status: "ok", run, steps };
}
export function listRuns() {
    const db = getDb();
    return db.prepare("SELECT * FROM runs ORDER BY created_at DESC").all();
}
export async function stopWorkflow(query) {
    const db = getDb();
    // Try exact match first, then prefix match (same pattern as resume command)
    let run = db.prepare("SELECT * FROM runs WHERE id = ?").get(query);
    if (!run) {
        run = db.prepare("SELECT * FROM runs WHERE id LIKE ? || '%' ORDER BY created_at DESC LIMIT 1").get(query);
    }
    if (!run) {
        const allRuns = db.prepare("SELECT id, task, status, created_at FROM runs ORDER BY created_at DESC LIMIT 20").all();
        const available = allRuns.map((r) => `  [${r.status}] ${r.id.slice(0, 8)} ${r.task.slice(0, 60)}`);
        return {
            status: "not_found",
            message: available.length
                ? `No run matching "${query}". Recent runs:\n${available.join("\n")}`
                : "No workflow runs found.",
        };
    }
    if (run.status === "completed" || run.status === "cancelled") {
        return {
            status: "already_done",
            message: `Run ${run.id.slice(0, 8)} is already "${run.status}".`,
        };
    }
    // Set run status to cancelled
    db.prepare("UPDATE runs SET status = 'cancelled', updated_at = datetime('now') WHERE id = ?").run(run.id);
    // Update all non-done steps to failed
    const result = db.prepare("UPDATE steps SET status = 'failed', output = 'Cancelled by user', updated_at = datetime('now') WHERE run_id = ? AND status IN ('waiting', 'pending', 'running')").run(run.id);
    const cancelledSteps = Number(result.changes);
    // Clean up cron jobs if no other active runs
    await teardownWorkflowCronsIfIdle(run.workflow_id);
    // Emit event
    emitEvent({
        ts: new Date().toISOString(),
        event: "run.failed",
        runId: run.id,
        workflowId: run.workflow_id,
        detail: "Cancelled by user",
    });
    return {
        status: "ok",
        runId: run.id,
        workflowId: run.workflow_id,
        cancelledSteps,
    };
}
