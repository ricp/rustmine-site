# RustMine website

This repository contains only the public RustMine engineering journal website. The RustMine application source is maintained separately.

The static site has seven routes: Home (`index.html`), Progress, Screens, Method, Journal, Design directions, and Privacy (each with its own `index.html`). Home gives a short dated snapshot; the deeper pages retain the source captions and evidence limits. Shared styling and behavior are in `site.css` and `site.js`. Assets, favicons, and `analytics.js` are local; the site needs no build pipeline. `legacy-fragments.js` on Home forwards previously shared root fragments and daily-note links to their new destinations.

The favicon set uses the current site's orange square mark on deep forest green. `favicon.svg` is the vector master; the ICO, PNG, Apple touch icon, and `site.webmanifest` provide browser and home screen sizes. The three exploratory brand directions remain unchosen.

`social-card-2026-10-20.png` is the 1200×630 public link-preview image. It follows the site's current hero tagline, mark, palette, and font stacks; Open Graph and Twitter metadata on every page point to its versioned absolute HTTPS URL. Its SHA-256 is `40c9d54ddcb237a38786af6a245d591b1a76c92727a40f8eb9fb418f4bd42b2b`. The older `social-card.png` remains available for existing cached links.

## Analytics

The public footer discloses Cloudflare Web Analytics and Google Analytics 4. `analytics.js` loads the supplied GA4 Measurement ID automatically, lets the standard `config` call send its initial page view, records the current RustMine.org page path without query or fragment, keeps only a referrer's origin, and disables advertising signals and personalization in the tag. It makes no separate manual `page_view` call. Google account-side Enhanced Measurement settings have not been verified and may add events independently of this script. No visitor opt-in is presented.

## Cloudflare Pages

- Production branch: `main`
- Framework preset: None
- Build command: `exit 0`
- Build output directory: `.` (repository root)

The site is a development showcase. It does not represent a production-ready RustMine application or a verified performance gain.

## Search metadata

Each page has its own canonical URL, Open Graph and Twitter title/description, and WebPage identity data. `sitemap.xml` lists all seven routes. The repository's `robots.txt` retains the content-signal explanation that Cloudflare previously served and adds a sitemap pointer, with no crawler restrictions. Keep it aligned with the hosting policy if that policy changes.

The pages include WebSite, WebPage, and author identity data. Keep it aligned with visible claims and avoid software release, rating, pricing, compatibility, or speed assertions until they are verified. Existing gallery images under `assets/site/` are byte-for-byte extractions of the previously embedded images; retain their captions, dimensions, and privacy provenance when editing them. The exact pre-reorganization public site and rollback route are recorded in [IA_ROLLBACK.md](docs/IA_ROLLBACK.md).

## Upstream watch

`/method/#upstream-watch` presents a dated Redmine research snapshot in three states: observed upstream, selected for RustMine review, and verified in an integrated RustMine release. The existing daily upstream research workflow supplies evidence to the site coordinator; this repository adds no timer or live feed. See the [refresh contract](docs/UPSTREAM_WATCH_REFRESH.md) before changing its date or entries.
