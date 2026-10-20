# RustMine website

This repository contains only the public RustMine engineering journal website. The RustMine application source is maintained separately.

`index.html` is a dated 18 October 2026 engineering snapshot. Its screenshots, portrait, and styles are embedded. The favicon files and `analytics.js` are local static assets; the site needs no build pipeline.

The favicon set uses the current site's orange square mark on deep forest green. `favicon.svg` is the vector master; the ICO, PNG, Apple touch icon, and `site.webmanifest` provide browser and home screen sizes. The three exploratory brand directions remain unchosen.

`social-card.png` is the 1200×630 public link-preview image. It uses the current site mark and palette; Open Graph and Twitter metadata in `index.html` point to its absolute HTTPS URL.

## Analytics

The public footer discloses Cloudflare Web Analytics and Google Analytics 4. `analytics.js` loads the supplied GA4 Measurement ID automatically, lets the standard `config` call send its initial page view, fixes the page URL to `https://rustmine.org/`, keeps only a referrer's origin, and disables advertising signals and personalization in the tag. It makes no separate manual `page_view` call. Google account-side Enhanced Measurement settings have not been verified and may add events independently of this script. No visitor opt-in is presented.

## Cloudflare Pages

- Production branch: `main`
- Framework preset: None
- Build command: `exit 0`
- Build output directory: `.` (repository root)

The site is a development showcase. It does not represent a production-ready RustMine application or a verified performance gain.

## Search metadata

The canonical URL is `https://rustmine.org/`. `sitemap.xml` lists that one page; fragment links within it are sections, not separate pages. The repository's `robots.txt` retains the content-signal explanation that Cloudflare previously served and adds a sitemap pointer, with no crawler restrictions. Keep it aligned with the hosting policy if that policy changes.

The homepage includes WebSite, WebPage, and author identity data. Keep it aligned with visible claims and avoid software release, rating, pricing, compatibility, or speed assertions until they are verified. Existing gallery images under `assets/site/` are byte-for-byte extractions of the previously embedded images; retain their captions, dimensions, and privacy provenance when editing them.

## Upstream watch

The `#upstream-watch` section presents a dated Redmine research snapshot in three states: observed upstream, selected for RustMine review, and verified in an integrated RustMine release. The existing daily upstream research workflow supplies evidence to the site coordinator; this repository adds no timer or live feed. See the [refresh contract](docs/UPSTREAM_WATCH_REFRESH.md) before changing its date or entries.
