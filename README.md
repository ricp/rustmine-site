# RustMine website

This repository contains only the public RustMine engineering journal website. The RustMine application source is maintained separately.

`index.html` is a dated 18 October 2026 engineering snapshot. Its screenshots, portrait, and styles are embedded. The favicon files and `analytics.js` are local static assets; the site needs no build pipeline.

The favicon set uses the current site's orange square mark on deep forest green. `favicon.svg` is the vector master; the ICO, PNG, Apple touch icon, and `site.webmanifest` provide browser and home screen sizes. The three exploratory brand directions remain unchosen.

## Analytics

The public footer discloses Cloudflare Web Analytics and Google Analytics 4. `analytics.js` loads the supplied GA4 Measurement ID automatically, lets the standard `config` call send its initial page view, fixes the page URL to `https://rustmine.org/`, keeps only a referrer's origin, and disables advertising signals and personalization in the tag. It makes no separate manual `page_view` call. Google account-side Enhanced Measurement settings have not been verified and may add events independently of this script. No visitor opt-in is presented.

## Cloudflare Pages

- Production branch: `main`
- Framework preset: None
- Build command: `exit 0`
- Build output directory: `.` (repository root)

The site is a development showcase. It does not represent a production-ready RustMine application or a verified performance gain.
