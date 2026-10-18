# assets

Public brand assets for ThoughtPivot, Bytewells and Vran: logos, icons and email templates.

Browse, download or copy URLs at **https://thoughtpivot.github.io/assets/**.

Every file is served from GitHub Pages at `https://thoughtpivot.github.io/assets/<path>`, for example
`https://thoughtpivot.github.io/assets/email/tp-logo.png`. Don't move or rename files that are already
linked from emails or sites (see `email/bytewells/README.md`).

## Adding or changing assets

1. Add the file in the right folder (`email/`, `vran/`, or a new folder per product).
2. Regenerate the manifest:

   ```sh
   node scripts/build-index.mjs
   ```

3. Commit the file together with the updated `assets.json`.

The home page (`index.html`) is plain static HTML/CSS/JS with no build step. It reads `assets.json`
and groups files by folder. A CI check (`.github/workflows/index.yml`) runs
`node scripts/build-index.mjs --check` on pushes and pull requests and fails if `assets.json` is out
of date. It never commits anything.

## How the manifest works

`scripts/build-index.mjs` (Node 18+, no dependencies) scans the repo for images (`png`, `jpg`, `gif`,
`webp`, `avif`, `svg`, `ico`), documents (`pdf`, `html`, `txt`, `md`), data, fonts and media. It skips
`.git`, `.github`, `scripts/` and the site files (`index.html`, `assets.json`, root `README.md`). Each
entry records the path, type, size, pixel dimensions for PNG/SVG, a guessed brand, and the public URL.
Friendly folder titles live in `GROUP_TITLES` at the top of the script; folders not listed there get a
title-cased name.

Preview locally:

```sh
python3 -m http.server 8000   # then open http://localhost:8000/
```
