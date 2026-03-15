import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
const __dirname = path.dirname(fileURLToPath(import.meta.url));
// Bundled workflows ship with antfarm (in the repo's workflows/ directory)
export function resolveBundledWorkflowsDir() {
    // From dist/installer/paths.js -> ../../workflows
    return path.resolve(__dirname, "..", "..", "workflows");
}
export function resolveBundledWorkflowDir(workflowId) {
    return path.join(resolveBundledWorkflowsDir(), workflowId);
}
export function resolveOpenClawStateDir() {
    const env = process.env.OPENCLAW_STATE_DIR?.trim();
    if (env) {
        return env;
    }
    return path.join(os.homedir(), ".openclaw");
}
export function resolveOpenClawConfigPath() {
    const env = process.env.OPENCLAW_CONFIG_PATH?.trim();
    if (env) {
        return env;
    }
    return path.join(resolveOpenClawStateDir(), "openclaw.json");
}
export function resolveAntfarmRoot() {
    return path.join(resolveOpenClawStateDir(), "antfarm");
}
export function resolveWorkflowRoot() {
    return path.join(resolveAntfarmRoot(), "workflows");
}
export function resolveWorkflowDir(workflowId) {
    return path.join(resolveWorkflowRoot(), workflowId);
}
export function resolveWorkflowWorkspaceRoot() {
    return path.join(resolveOpenClawStateDir(), "workspaces", "workflows");
}
export function resolveWorkflowWorkspaceDir(workflowId) {
    return path.join(resolveWorkflowWorkspaceRoot(), workflowId);
}
export function resolveRunRoot() {
    return path.join(resolveAntfarmRoot(), "runs");
}
export function resolveAntfarmCli() {
    // From dist/installer/paths.js -> ../../dist/cli/cli.js
    return path.resolve(__dirname, "..", "cli", "cli.js");
}
