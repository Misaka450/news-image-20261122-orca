import { cp, mkdir } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = dirname(fileURLToPath(import.meta.url));
const outputDir = resolve(process.env.MAKEFUN_OUTPUT_DIR || "/output");

await mkdir(outputDir, { recursive: true });
await cp(join(repoRoot, "entry.png"), join(outputDir, "entry.png"));
