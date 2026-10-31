# Commit history and progress updates

Before publishing progress, timeline or counter changes, run:

    python3 scripts/check-commit-chart.py

When the authorized application repository is available, also re-count its exact accepted heads:

    python3 scripts/check-commit-chart.py --app-repo /path/to/Rustmine

Keep `data/commit-history.json`, the Journal chart, daily-note counters, Home and Progress consistent. A new accepted shared or portable head requires a source recount; do not merely advance the check date. Count all reachable non-merge commits once by full SHA and UTC committer date. Keep application main/develop, accepted shared ancestry, portable-only commits and other unintegrated branches distinct.

Verify the actual canonical Journal chart and captions on desktop and mobile, including its newest dates and zero-count days. Milestone-anchor checks alone are insufficient. Preserve dated historical notes, privacy, and the existing design, story, analytics and favicon.
