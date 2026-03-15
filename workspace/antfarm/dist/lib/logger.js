import fs from "node:fs";
import { readFile } from "node:fs/promises";
import path from "node:path";
import os from "node:os";
const LOG_DIR = path.join(os.homedir(), ".openclaw", "antfarm", "logs");
const LOG_FILE = path.join(LOG_DIR, "workflow.log");
const MAX_LOG_SIZE = 5 * 1024 * 1024; // 5MB
let logDirReady = false;
function ensureLogDirSync() {
    if (logDirReady)
        return;
    fs.mkdirSync(LOG_DIR, { recursive: true });
    logDirReady = true;
}
function rotateIfNeededSync() {
    try {
        const stats = fs.statSync(LOG_FILE);
        if (stats.size > MAX_LOG_SIZE) {
            const rotatedPath = `${LOG_FILE}.1`;
            fs.renameSync(LOG_FILE, rotatedPath);
        }
    }
    catch {
        // File doesn't exist yet, no rotation needed
    }
}
export function formatEntry(entry) {
    const parts = [entry.timestamp, `[${entry.level.toUpperCase()}]`];
    if (entry.workflowId) {
        parts.push(`[${entry.workflowId}]`);
    }
    if (entry.runId) {
        parts.push(`[${entry.runId.slice(0, 8)}]`);
    }
    if (entry.stepId) {
        parts.push(`[${entry.stepId}]`);
    }
    parts.push(entry.message);
    return parts.join(" ");
}
export function log(level, message, context) {
    try {
        ensureLogDirSync();
        rotateIfNeededSync();
        const entry = {
            timestamp: new Date().toISOString(),
            level,
            message,
            ...context,
        };
        const line = formatEntry(entry) + "\n";
        fs.appendFileSync(LOG_FILE, line, "utf-8");
    }
    catch {
        // Logging must never throw into the caller
    }
}
export const logger = {
    info: (msg, ctx) => log("info", msg, ctx),
    warn: (msg, ctx) => log("warn", msg, ctx),
    error: (msg, ctx) => log("error", msg, ctx),
    debug: (msg, ctx) => log("debug", msg, ctx),
};
export async function readRecentLogs(lines = 50) {
    try {
        const content = await readFile(LOG_FILE, "utf-8");
        const allLines = content.trim().split("\n");
        return allLines.slice(-lines);
    }
    catch {
        return [];
    }
}
