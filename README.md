# Chayananda Nagesh — Portfolio

Live: https://chayananda.vercel.app

Hand-written static site. No framework, no dependencies.

| What | Where |
|---|---|
| All content (case studies, metrics, experience, education) | `scripts/build.py` |
| Design system (colors, type, layout) | `assets/css/site.css` |
| Interactions (nav, reveal, hologram cards, TOC) | `assets/js/site.js` |
| Play projects list (title, description, thumbnail, repo) | `PLAY` in `scripts/build.py` |

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

## Play: vibe-coded projects in their own repos

`/play/` lists small side projects. Each project keeps its **own GitHub repo** and is published at
`/play/<slug>/` (e.g. www.chayananda.com/play/horoscene). On every deploy, the workflow runs
`scripts/fetch_play.sh`, which clones each repo listed in `PLAY` and copies its folder into the site.

- **Add a project:** add an entry to `PLAY` in `scripts/build.py` and a 16:9 thumbnail in `assets/img/play/`.
- **Update a project:** push to its repo, then re-run "Deploy to GitHub Pages" under **Actions** here.
- **Private repos** need the `PLAY_TOKEN` Actions secret: a fine-grained GitHub token with read-only
  *Contents* access to those repos. Without it, the project's page shows a "back soon" holding page.

## Keeping local and GitHub in sync

1. `git pull` before you start (picks up changes made elsewhere).
2. Edit, preview locally, then `git add -A && git commit -m "..." && git push`.
3. GitHub Actions builds and publishes `master` automatically.

The previous site is kept in the `old-site` branch of the same repo.
