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
# it only ever receives files via this direct upload. Each `wrangler pages
# deploy` is a full snapshot, not additive, so the whole media-site/ tree
# must be uploaded in a single run.
FILES="$(find "$ROOT/site/media-site" -type f | wc -l | tr -d ' ')"
echo "→ deploying $FILES files from site/media-site to media-roadsoftimes"

wrangler pages deploy "$ROOT/site/media-site" \
  --project-name media-roadsoftimes \
  --commit-dirty=true
