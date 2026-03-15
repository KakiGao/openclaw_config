import fs from "node:fs/promises";
import path from "node:path";
async function ensureDir(dir) {
    await fs.mkdir(dir, { recursive: true });
}
async function readFileIfExists(filePath) {
    try {
        return await fs.readFile(filePath, "utf-8");
    }
    catch {
        return null;
    }
}
export async function writeWorkflowFile(params) {
    const destination = params.destination;
    const existing = await readFileIfExists(destination);
    if (existing !== null && !params.overwrite) {
        return { path: destination, status: "skipped" };
    }
    await ensureDir(path.dirname(destination));
    await fs.copyFile(params.source, destination);
    return { path: destination, status: existing === null ? "created" : "updated" };
}
