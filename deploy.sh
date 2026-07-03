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
FILE_LIST="$(find "$ROOT/site/media-site" -type f -not -name '.DS_Store' | sed "s|^$ROOT/site/media-site/||" | sort)"
FILE_COUNT="$(printf '%s\n' "$FILE_LIST" | grep -c .)"
echo "→ deploying $FILE_COUNT files from site/media-site to media-roadsoftimes:"
printf '%s\n' "$FILE_LIST" | sed 's/^/    /'

wrangler pages deploy "$ROOT/site/media-site" \
  --project-name media-roadsoftimes \
  --commit-dirty=true
