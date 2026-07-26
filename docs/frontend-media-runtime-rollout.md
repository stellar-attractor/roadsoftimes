# Frontend media runtime rollout

The frontend reads media filenames from `infographics.json`; it does not accept
stored URLs or directory paths for exhibit media.

`site/js/media-runtime.js` is the only public path builder. It combines:

1. the museum slug from `museums.json`;
2. a typed media role;
3. the ASCII filename stored in the exhibit record.

The primary origin is `https://media.roadsoftimes.com`. The single fallback is
`https://media-roadsoftimes.pages.dev`, with an identical relative path.

Load `media-runtime.js` before `infographic-player.js`. Missing runtime,
non-ASCII filenames, unknown museum slugs, stored paths, and incompatible file
extensions fail closed instead of entering a resolver cascade.

Before publishing, run all `site/tests/smoke_*.js` files. The final data-layer
gate validates the complete catalog and audits the production player for legacy
path inference. Deployment verification should sample at least one exhibit from
multiple museums and cover `800_glow`, `800`, `png`, and `previews` paths on
both origins.
