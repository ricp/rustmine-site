# Activity publication checklist

Use this checklist before every publication of application activity. This is a maintainer process, not an automatic deployment.

- Capture an explicit UTC committer-date cutoff and record when refs were observed.
- Enumerate the available application integration/implementation branches, registered worktrees and **all live remote application branch heads**. Do not rely only on stale local remote-tracking refs.
- Keep an internal exact-tip/full-SHA census and prove ancestry closure into the captured local graph or fetched remote history. Union full identities across every source before counting; never add repository totals. Include merges and committed untested/unmerged work in the current activity series.
- Exclude website commits, uncommitted changes, reflog/archive/tag/stash-only objects, automated checkout-only snapshots and unrelated temporary refs. Keep the old accepted-preview/non-merge metric separate.
- Notice date gaps. Publish unavailable counts as unavailable, never fake zero or a bar. Show actual dated work notes in the same weekly panel, including uncovered dates next to a partly counted week. Preserve historical notes and deep links.
- Refresh the census before each publication and before the data becomes **48 hours old**. If access or publication is blocked, retain the last verified cutoff and state the bounded coverage gap. Do not silently advance a date or schedule automatic deployment.
- Update aggregate data, captions, summaries, scope and cutoff together. Publish no private commit IDs, messages, paths, branch names, credentials or customer details.
- Run both commit-chart checks, the activity checker with the captured census/remote union, and HTML/link/ID/diff validation. Verify that the exact intended public dataset is included in the static-asset allowlist while private/control files remain excluded.
- Test desktop/mobile weekly controls, latest-first selection, known and uncovered dates, note links and the all-week no-JavaScript fallback. Promote through feature → develop → main with exact-head checks; verify the production build and actual public page/data. A commit or preview alone is not publication.

## Repeatable local capture and check

`scripts/collect-development-activity.py` reads Git metadata only. It does not fetch, change application refs, run the application, publish or schedule deployments. Run it on the authorized Mac with the application repositories available. The current series begins on 1 November 2026; a new month needs a deliberate reporting-range review.

1. Through the authorized GitHub connector, enumerate every live application branch (all pages). Save a **private, outside-checkout** JSON file containing `observedAt` in UTC and `branches`, each with `name` and full `sha`. Never substitute stale remote-tracking refs or invent missing counts.
2. Run the collector with repeated `--repo` arguments, an explicit UTC `--cutoff`, that `--remote-heads` file and a fresh outside-checkout `--output` path. It reports any remote tips absent from the local graph. No credentials are read or created.
3. Obtain exact-tip commit metadata through the same authorized connector until every parent reaches the captured local graph. A private `--remote-history` JSON contains `rows`, keyed by full SHA, each with UTC `committer` and full `parents`. Run the collector again to a fresh output path with this argument. An unresolved parent frontier blocks reconciliation.
4. Check the resulting private census with `python3 scripts/check-development-activity.py --census /private/census.json --remote-history /private/remote-history.json`, after preparing the aggregate-only public data and chart. `python3 scripts/test-development-activity.py` checks deduplication, merges, cutoff and incomplete-history refusal.

Keep raw refs, paths and commit metadata private. The public site receives date totals and explicit coverage only. A recurring runner must have the authorized Mac/SSD and connector access; this script alone does not supply them or enable unattended publication. If a runner cannot reach either source, report a partial census and the exact gap instead of moving the freshness date.
