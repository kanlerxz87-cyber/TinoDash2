import fs from "node:fs";
import path from "node:path";
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { ROOT, verify } from "./verify.mjs";
import { PUBLIC_FILES } from "./public-files.mjs";
const tests = fs
  .readdirSync(path.join(ROOT, "tests"))
  .filter((n) => n.endsWith(".test.js"))
  .sort()
  .map((n) => path.join(ROOT, "tests", n));
execFileSync(process.execPath, ["--test", ...tests], { stdio: "inherit" });
verify();
const dest = path.join(ROOT, "dist");
assert.equal(path.dirname(dest), ROOT);
assert.equal(path.basename(dest), "dist");
fs.rmSync(dest, { recursive: true, force: true });
fs.mkdirSync(dest);
for (const name of PUBLIC_FILES) {
  const target = path.join(dest, name);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.copyFileSync(path.join(ROOT, name), target);
}
verify(dest);
console.log(
  `Built ${PUBLIC_FILES.length} allowlisted public files in decision-lab/dist. No private inventory, repository files, tests or generated PDFs copied.`,
);
