#!/bin/zsh
set -euo pipefail

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

# cdn.roadsoftimes.com (project "roadsoftimes") is GitHub-connected and
# auto-deploys site/ (minus media-site/, which is gitignored) on push — this
# script does not touch it.
#
# media.roadsoftimes.com (project "media-roadsoftimes") has no Git provider;
# it only ever receives files via this direct upload. `wrangler pages deploy`
# walks the whole media-site/ tree to build its manifest, but it
# content-hashes each file first and only transfers bytes for hashes not
# already stored on Cloudflare — so an unchanged file is skipped, and a
# single changed file results in a single real upload. Wrangler's own output
# below (lines prefixed "+") lists exactly what got uploaded, not the tree.
wrangler pages deploy "$ROOT/site/media-site" \
  --project-name media-roadsoftimes \
  --commit-dirty=true
