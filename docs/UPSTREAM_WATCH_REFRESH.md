# Upstream watch refresh contract

The `#upstream-watch` section is a dated, reviewed source snapshot. The existing daily Redmine upstream research workflow supplies new evidence to the existing RustMine.org site coordinator. This repository adds no timer, crawler, or unreviewed live feed. The coordinator publishes the section through the normal `feature/*` → `develop` → `main` flow.

## Source and scope

- Start from the latest completed Orbit Picker digest and commit register, then verify the cited official Redmine release and security pages, SVN branches, and relevant issue status. GitHub is a community mirror used for convenient commit links, not an authority for release state.
- RustMine remains pinned to the verified Redmine 7.0.2 release artifact until an explicit application compatibility decision changes that baseline. Preserve the baseline label until such a decision is evidenced.
- Use the report's actual UTC source-check time in both the visible text and `<time datetime>` inside `#upstream-watch`. Never advance the timestamp for a failed or skipped research check. After a completed daily check, advance it even if no noteworthy upstream changes were found.
- Treat an upstream issue or behavior as one item. A trunk commit and its stable cherry-pick are links or statuses for that item, not two features or two product integrations. Do not turn open issues or unmerged PRs into promised Redmine features.

## Three public states

1. **Seen upstream:** only code committed on a named branch, or an official released change, with a direct source link and its accurate branch or release status. “Committed” does not mean released.
2. **For RustMine review:** a selected change with an explicit comparison or decision still needed. The wording must not promise implementation.
3. **Verified in RustMine:** a named behavior only after the application commit is integrated into its `main` and local preview, the exact-head gate passes, and private-clone preflight and guarded preview switch evidence are recorded. Link the public explanation to the dated RustMine milestone; never infer adoption from upstream detection or a matching feature name.

## Update boundary and checks

Edit only the HTML between `<!-- upstream-watch:start -->` and `<!-- upstream-watch:end -->` for a routine daily data refresh. Keep the three stage headings and the explanatory distinction. Preserve the rest of the website, including its separate project-progress snapshot, personal story, design, analytics, and favicon. Use public sources only; never copy local paths, logs, customer data, or raw research files into the site.

Before a release, check that the UTC timestamp matches the completed research report, every visible commit link resolves to the intended change, branch and release labels still hold, repeated trunk/stable changes are grouped, and any “Verified in RustMine” entry has the release evidence above. Check HTML structure and mobile layout where browser access is available. Push the feature branch, merge through `develop` and `main`, wait for the Cloudflare build, then confirm the public `https://rustmine.org/#upstream-watch` content. If any source or release state is uncertain, keep the last verified public entry and record the uncertainty in the research report instead of changing the site.
