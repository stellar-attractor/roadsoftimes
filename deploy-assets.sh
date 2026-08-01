#!/bin/zsh
set -euo pipefail

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

# assets.roadsoftimes.com (project "assets-roadsoftimes") is the shared photo
# CDN for the Places/Times/Roads catalogs — small tables (tens to low
# hundreds of rows each), kept separate from media.roadsoftimes.com (which
# serves the much larger exhibit media tree). Museums stays on
# media.roadsoftimes.com / exhibits/ for now; not migrated here.
#
# Like media-roadsoftimes, this project has no Git provider; it only ever
# receives files via this direct upload. Mirrors deploy.sh's media-site
# block exactly — same content-hashing behavior, only changed files upload.
#
# NOTE: the "assets-roadsoftimes" Pages project + assets.roadsoftimes.com
# custom domain do not exist yet — this script is not runnable until they
# are provisioned by hand in the Cloudflare dashboard. Once they are, this
# script works unchanged.
wrangler pages deploy "$ROOT/site/assets-site" \
  --project-name assets-roadsoftimes \
  --commit-dirty=true
