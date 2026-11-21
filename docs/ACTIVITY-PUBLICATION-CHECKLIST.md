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
