import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { ROOT, verify } from "./verify.mjs";
import { PUBLIC_FILES } from "./public-files.mjs";
const root = path.join(ROOT, "dist");
verify(root);
const port = Number(process.env.PORT ?? 4173);
const types = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".svg": "image/svg+xml",
  ".md": "text/plain; charset=utf-8",
};
http
  .createServer((req, res) => {
    const url = new URL(req.url, "http://preview.invalid");
    let request = url.pathname;
    for (const mount of ["/TinoDash2/decision-lab", "/decision-lab"])
      if (request === mount || request.startsWith(mount + "/")) {
        request = request.slice(mount.length) || "/";
        break;
      }
    const name = request === "/" ? "index.html" : request.slice(1);
    if (!["GET", "HEAD"].includes(req.method) || !PUBLIC_FILES.includes(name)) {
      res.writeHead(404, { "Content-Type": "text/plain" });
      res.end("Not a public asset.");
      return;
    }
    res.writeHead(200, {
      "Content-Type": types[path.extname(name)] ?? "application/octet-stream",
      "Cache-Control": "no-store",
      "X-Content-Type-Options": "nosniff",
      "Referrer-Policy": "no-referrer",
    });
    res.end(
      req.method === "HEAD"
        ? undefined
        : fs.readFileSync(path.join(root, name)),
    );
  })
  .listen(port, "0.0.0.0", () =>
    console.log(
      `Public-safe Decision Lab preview listening on 0.0.0.0:${port}. Only ${PUBLIC_FILES.length} allowlisted built files are served.`,
    ),
  );
