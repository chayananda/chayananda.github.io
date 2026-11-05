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

Push to `main`. Vercel runs `python3 scripts/build.py` and publishes the result to chayananda.vercel.app. Other branches get preview URLs.
