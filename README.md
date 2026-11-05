# Chayananda Nagesh — Portfolio

Live: https://chayananda.vercel.app

Hand-written static site. No framework, no dependencies.

| What | Where |
|---|---|
| All content (case studies, metrics, experience, education) | `scripts/build.py` |
| Design system (colors, type, layout) | `assets/css/site.css` |
| Interactions (nav, reveal, hologram cards, TOC) | `assets/js/site.js` |

## Edit and preview locally

```bash
python3 scripts/build.py        # generate the HTML pages
python3 -m http.server 8000     # open http://localhost:8000
```

The generated pages are git-ignored. Edit `build.py`, not the HTML.

## Deploy

Live at **www.chayananda.com** (chayananda.com redirects there), served by GitHub Pages from the
`chayananda/chayananda.github.io` repo.

Push to `master` in that repo. The workflow in `.github/workflows/pages.yml` runs
`python3 scripts/build.py`, collects the pages and `assets/`, and publishes them. Watch it under the
repo's **Actions** tab; it takes about a minute.

## Keeping local and GitHub in sync

1. `git pull` before you start (picks up changes made elsewhere).
2. Edit, preview locally, then `git add -A && git commit -m "..." && git push`.
3. GitHub Actions builds and publishes `master` automatically.

The previous site is kept in the `old-site` branch of the same repo.
