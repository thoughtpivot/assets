#!/usr/bin/env node
// Regenerates assets.json: a manifest of every public asset in this repo.
// Usage: node scripts/build-index.mjs          (write assets.json)
//        node scripts/build-index.mjs --check  (exit 1 if assets.json is out of date)
// Node 18+, no dependencies.
import { readdir, readFile, writeFile, stat } from "node:fs/promises";
import { join, relative, extname, basename, dirname, sep } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const OUT = join(ROOT, "assets.json");
const BASE_URL = "https://thoughtpivot.github.io/assets/";

// Extension -> [category, label]
const TYPES = {
  ".png": ["image", "PNG"], ".jpg": ["image", "JPEG"], ".jpeg": ["image", "JPEG"],
  ".gif": ["image", "GIF"], ".webp": ["image", "WebP"], ".avif": ["image", "AVIF"],
  ".svg": ["image", "SVG"], ".ico": ["image", "ICO"],
  ".pdf": ["document", "PDF"], ".html": ["document", "HTML"], ".htm": ["document", "HTML"],
  ".txt": ["document", "Text"], ".md": ["document", "Markdown"],
  ".csv": ["data", "CSV"], ".json": ["data", "JSON"],
  ".woff": ["font", "WOFF"], ".woff2": ["font", "WOFF2"], ".ttf": ["font", "TTF"], ".otf": ["font", "OTF"],
  ".mp4": ["video", "MP4"], ".webm": ["video", "WebM"], ".mp3": ["audio", "MP3"],
  ".zip": ["archive", "ZIP"],
};

// Site/tooling files that are not assets.
const SKIP_DIRS = new Set([".git", ".github", "node_modules", "scripts"]);
const SKIP_FILES = new Set(["index.html", "assets.json", "README.md", "404.html", ".nojekyll", "CNAME"]);

// Optional friendly names for folders; anything else is title-cased from the path.
const GROUP_TITLES = {
  "": "Root",
  "email": "Email brand logos",
  "email/bytewells": "Bytewells email templates",
  "email/bytewells/assets": "Bytewells email source logos",
  "vran": "Vran",
};

const BRANDS = [
  [/bytewells/i, "Bytewells"],
  [/vran/i, "Vran"],
  [/(^|[-_/])tp[-_.]|thoughtpivot/i, "ThoughtPivot"],
];

async function walk(dir, out = []) {
  const entries = await readdir(dir, { withFileTypes: true });
  for (const e of entries) {
    const full = join(dir, e.name);
    if (e.isDirectory()) {
      if (!SKIP_DIRS.has(e.name) && !e.name.startsWith(".")) await walk(full, out);
    } else if (e.isFile()) {
      const rel = relative(ROOT, full).split(sep).join("/");
      if (rel === e.name && SKIP_FILES.has(e.name)) continue; // root-level site files only
      if (e.name.startsWith(".")) continue;
      if (TYPES[extname(e.name).toLowerCase()]) out.push(rel);
    }
  }
  return out;
}

function pngSize(buf) {
  if (buf.length > 24 && buf.toString("ascii", 1, 4) === "PNG") {
    return { width: buf.readUInt32BE(16), height: buf.readUInt32BE(20) };
  }
  return null;
}

function svgSize(text) {
  const tag = (text.match(/<svg\b[^>]*>/i) || [""])[0];
  const num = (a) => {
    const m = tag.match(new RegExp(`\\b${a}\\s*=\\s*["']\\s*([\\d.]+)(px)?\\s*["']`, "i"));
    return m ? Math.round(parseFloat(m[1])) : null;
  };
  let width = num("width"), height = num("height");
  const vb = tag.match(/viewBox\s*=\s*["']\s*[-\d.]+[\s,]+[-\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)/i);
  if ((!width || !height) && vb) { width = Math.round(+vb[1]); height = Math.round(+vb[2]); }
  return width && height ? { width, height } : null;
}

function titleCase(p) {
  return p.split("/").map((s) => s.replace(/[-_]+/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())).join(" / ");
}

// File name wins over folder (e.g. email/bytewells/assets/tp-logo.svg is ThoughtPivot).
function brandOf(path) {
  for (const target of [basename(path), path]) {
    for (const [re, name] of BRANDS) if (re.test(target)) return name;
  }
  return null;
}

async function build() {
  const files = (await walk(ROOT)).sort((a, b) => a.localeCompare(b));
  const assets = [];
  for (const path of files) {
    const ext = extname(path).toLowerCase();
    const [category, label] = TYPES[ext];
    const full = join(ROOT, path);
    const { size } = await stat(full);
    let dims = null;
    if (ext === ".png") dims = pngSize(await readFile(full));
    else if (ext === ".svg") dims = svgSize(await readFile(full, "utf8"));
    const dir = path.includes("/") ? path.slice(0, path.lastIndexOf("/")) : "";
    assets.push({
      path,
      name: basename(path),
      dir,
      ext: ext.slice(1),
      type: label,
      category,
      bytes: size,
      ...(dims ? dims : {}),
      ...(brandOf(path) ? { brand: brandOf(path) } : {}),
      url: BASE_URL + path.split("/").map(encodeURIComponent).join("/"),
    });
  }
  const dirs = [...new Set(assets.map((a) => a.dir))].sort((a, b) => a.localeCompare(b));
  const groups = dirs.map((dir) => ({
    dir,
    title: GROUP_TITLES[dir] ?? titleCase(dir),
    count: assets.filter((a) => a.dir === dir).length,
  }));
  // No timestamps, so the output is deterministic and diffable in CI.
  return JSON.stringify({ baseUrl: BASE_URL, count: assets.length, groups, assets }, null, 2) + "\n";
}

const json = await build();
if (process.argv.includes("--check")) {
  let current = "";
  try { current = await readFile(OUT, "utf8"); } catch {}
  if (current !== json) {
    console.error("assets.json is out of date. Run: node scripts/build-index.mjs");
    process.exit(1);
  }
  console.log("assets.json is up to date.");
} else {
  await writeFile(OUT, json);
  console.log(`Wrote assets.json (${JSON.parse(json).count} assets).`);
}
