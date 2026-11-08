#!/usr/bin/env bash
# Mounts each Play project (its own GitHub repo) at /play/<slug>/ in the built site.
#
#   scripts/fetch_play.sh <site-dir>
#
# Reads play/repos.txt (written by scripts/build.py: "slug owner/repo dir" per line),
# shallow-clones each repo and copies its <dir> folder to <site-dir>/play/<slug>/.
# Private repos need PLAY_TOKEN: a fine-grained GitHub token with read-only
# "Contents" access to those repos (stored as the PLAY_TOKEN Actions secret).
# A project that can't be fetched gets a holding page instead of failing the deploy.
set -euo pipefail

site="${1:?usage: fetch_play.sh <site-dir>}"
# Strip spaces/newlines that sneak in when the secret is pasted
PLAY_TOKEN="$(printf '%s' "${PLAY_TOKEN:-}" | tr -d '[:space:]')"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

while read -r slug repo dir; do
  [ -z "${slug:-}" ] && continue
  dest="$site/play/$slug"
  mkdir -p "$dest"
  if [ -n "${PLAY_TOKEN:-}" ]; then
    url="https://x-access-token:${PLAY_TOKEN}@github.com/${repo}.git"
  else
    url="https://github.com/${repo}.git"
  fi
  if GIT_TERMINAL_PROMPT=0 git clone --quiet --depth 1 "$url" "$tmp/$slug" 2>"$tmp/$slug.err" \
     && [ -f "$tmp/$slug/$dir/index.html" ]; then
    cp -R "$tmp/$slug/$dir/." "$dest/"
    rm -f "$dest/vercel.json"
    echo "  play/$slug  <-  $repo/$dir"
  else
    if [ -z "$PLAY_TOKEN" ]; then why="PLAY_TOKEN secret is empty or missing";
    else why="$(sed "s/${PLAY_TOKEN}/***/g" "$tmp/$slug.err" | tr '\n' ' ')"; fi
    echo "::warning::Could not fetch $repo for /play/$slug/ (token length ${#PLAY_TOKEN}): $why"
    cat > "$dest/index.html" <<HTML
<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Back soon · Chayananda Nagesh</title>
<style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#08090b;color:#b4b6bf;font:16px/1.6 Inter,system-ui,sans-serif;text-align:center}a{color:#b6a6ff}</style>
<p>This project is being updated and will be back shortly.<br><a href="/play/">Back to Play</a></p>
HTML
  fi
done < play/repos.txt
