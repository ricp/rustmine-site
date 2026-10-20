# Pre-reorganization site and rollback

The exact public RustMine.org site before the information reorganization is commit `66cd35547bd510fac0240f65aec96201dd16ca0e`. The non-overwriting annotated remote tag `pre-ia-reorganization-2026-10-20` points to that commit. It preserves the original single-page HTML, assets, analytics, metadata, and sitemap.

To inspect it without changing a checkout:

```sh
git fetch origin --tags
git show pre-ia-reorganization-2026-10-20:index.html
git ls-remote origin 'refs/tags/pre-ia-reorganization-2026-10-20^{}'
```

For a rollback, start a new branch from the then-current `origin/main`. Review any site changes made since the reorganization. Revert the reorganization release merge on that branch with `git revert -m 1 <reorganization-release-merge-sha>` if it is still the only change to remove. If later changes depend on the new routes, prepare a reviewed restoration diff against the tagged site instead. Test the result, then use explicit `HEAD:refs/heads/feature/<slug>`, `HEAD:refs/heads/develop`, and `HEAD:refs/heads/main` pushes in that order, verifying each remote ref and the public page. Do not force-push or move the preserved tag.

The new homepage redirects previously shared `/#...` fragments to their new pages in `legacy-fragments.js`. A rollback to the tagged site restores the original single-page anchors.
