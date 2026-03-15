import fs from "node:fs/promises";
import JSON5 from "json5";
import { resolveOpenClawConfigPath } from "./paths.js";
export async function readOpenClawConfig() {
    const path = resolveOpenClawConfigPath();
    try {
        const raw = await fs.readFile(path, "utf-8");
        const config = JSON5.parse(raw);
        return { path, config };
    }
    catch (err) {
        const message = err instanceof Error ? err.message : String(err);
        throw new Error(`Failed to read OpenClaw config at ${path}: ${message}`);
    }
}
export async function writeOpenClawConfig(path, config) {
    const content = `${JSON.stringify(config, null, 2)}\n`;
    await fs.writeFile(path, content, "utf-8");
}
