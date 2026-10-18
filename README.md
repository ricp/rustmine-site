# RustMine website

This repository contains only the public RustMine engineering journal website. The RustMine application source is maintained separately.

`index.html` is the approved timeline proposal (version 23), an October 17, 2026 snapshot. Its screenshots, portrait, styles, and scripts are embedded, so the site needs no asset pipeline or external runtime dependencies.

The favicon set uses the current site's orange square mark on deep forest green. `favicon.svg` is the vector master; the ICO, PNG, Apple touch icon, and `site.webmanifest` provide browser and home screen sizes. The three exploratory brand directions remain unchosen.

## Cloudflare Pages

- Production branch: `main`
- Framework preset: None
- Build command: `exit 0`
- Build output directory: `.` (repository root)

The site is a development showcase. It does not represent a production-ready RustMine application or a verified performance gain.
