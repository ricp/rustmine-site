#!/usr/bin/env python3
"""Capture local Git activity without changing app refs; reconcile supplied live-remote metadata."""
from pathlib import Path
import argparse, collections, datetime as dt, hashlib, json, os, subprocess

def git(repo, *args, **kwargs):
    return subprocess.check_output(['git', '-C', str(repo), *args], text=True,
                                   env={**os.environ, 'GIT_OPTIONAL_LOCKS': '0'}, **kwargs)

def excluded_ref(value):
    return any(x in value.lower() for x in ['/tmp/', '/temp/', '/backup/', 'pending-import-backup', 'historical-review-only'])

def capture(repos, cutoff, remote):
    start = dt.datetime(2026, 11, 1, tzinfo=dt.timezone.utc).timestamp()
    snapshots, graph = [], {}
    for repo in repos:
        refs, excluded = [], []
        for line in git(repo, 'for-each-ref', '--format=%(refname) %(objectname)').splitlines():
            ref, sha = line.split()
            permitted = ref.startswith(('refs/heads/', 'refs/remotes/')) and not ref.endswith('/HEAD')
            permitted &= not excluded_ref(ref)
            (refs if permitted else excluded).append({'ref': ref, 'sha': sha})
        worktrees = []
        for block in git(repo, 'worktree', 'list', '--porcelain').strip().split('\n\n'):
            lines = block.splitlines()
            path = lines[0][9:]
            head = next((x[5:] for x in lines if x.startswith('HEAD ')), None)
            branch = next((x[7:] for x in lines if x.startswith('branch ')), '')
            live = Path(path).exists() and not any(x.startswith('prunable') for x in lines)
            live &= not excluded_ref(branch)
            worktrees.append({'path': path, 'head': head, 'exists': live})
        tips = sorted({x['sha'] for x in refs} | {x['head'] for x in worktrees if x['exists'] and x['head']})
        assert tips, 'No permitted local application heads'
        for line in git(repo, 'rev-list', '--timestamp', '--parents', '--stdin', input='\n'.join(tips)+'\n').splitlines():
            epoch, sha, *parents = line.split()
            row = {'epoch': int(epoch), 'parents': parents}
            assert sha not in graph or graph[sha] == row
            graph[sha] = row
        snapshots.append({'repo': str(repo), 'refs': refs, 'excludedRefs': excluded, 'worktrees': worktrees, 'tips': tips})
    eligible_remote = [x for x in remote['branches'] if not excluded_ref('/' + x['name'])]
    remote_tips = sorted({x['sha'] for x in eligible_remote})
    missing_tips = [sha for sha in remote_tips if sha not in graph]
    selected = {sha: row for sha, row in graph.items() if start <= row['epoch'] <= cutoff.timestamp()}
    return {'cutoff': cutoff.isoformat(), 'snapshots': snapshots, 'graph': graph, 'selectedCommits': selected,
            'remoteHeadsObservedAtUtc': remote['observedAt'], 'remoteBranches': eligible_remote,
            'remoteBranchesEnumerated': len(remote['branches']),
            'excludedRemoteBranches': [x for x in remote['branches'] if x not in eligible_remote],
            'remoteTipsNotInLocalGraph': missing_tips}

def reconcile(census, remote_rows):
    graph = dict(census['graph'])
    for sha, row in remote_rows.items():
        assert len(sha) == 40 and all(c in '0123456789abcdef' for c in sha)
        value = {'epoch': int(dt.datetime.fromisoformat(row['committer'].replace('Z', '+00:00')).timestamp()), 'parents': row['parents']}
        assert sha not in graph or graph[sha] == value, 'Conflicting full-SHA metadata'
        graph[sha] = value
    pending = [x['sha'] for x in census['remoteBranches']]
    visited, missing = set(), set()
    while pending:
        sha = pending.pop()
        if sha in visited:
            continue
        visited.add(sha)
        if sha not in graph:
            missing.add(sha)
        elif sha not in census['graph']:
            pending.extend(graph[sha]['parents'])
    assert not missing, 'Remote ancestry is incomplete: supply exact-tip commit metadata before publishing'
    cutoff = dt.datetime.fromisoformat(census['cutoff']).timestamp()
    start = dt.datetime(2026, 11, 1, tzinfo=dt.timezone.utc).timestamp()
    selected = dict(census['selectedCommits'])
    selected.update({sha: graph[sha] for sha in visited if start <= graph[sha]['epoch'] <= cutoff})
    census['unionCommits'] = selected
    census['remoteParentFrontierClosed'] = True
    census['unionSHA256'] = hashlib.sha256(('\n'.join(sorted(selected))+'\n').encode()).hexdigest()
    return census

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, action='append', required=True)
    parser.add_argument('--cutoff', required=True, help='Explicit ISO UTC committer cutoff')
    parser.add_argument('--remote-heads', type=Path, required=True, help='Fresh branches metadata from the authorized connector')
    parser.add_argument('--remote-history', type=Path, help='Exact full-SHA committer/parent metadata for heads absent locally')
    parser.add_argument('--output', type=Path, required=True, help='Private artifact OUTSIDE the public site checkout')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    assert not args.output.resolve().is_relative_to(root), 'Never write private census into the public checkout'
    cutoff = dt.datetime.fromisoformat(args.cutoff.replace('Z', '+00:00'))
    assert cutoff.tzinfo is not None and cutoff.utcoffset() == dt.timedelta(0), 'Use UTC'
    census = capture(args.repo, cutoff, json.loads(args.remote_heads.read_text()))
    if args.remote_history:
        census = reconcile(census, json.loads(args.remote_history.read_text())['rows'])
    with os.fdopen(os.open(args.output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), 'w') as f:
        json.dump(census, f, indent=2)
        f.write('\n')
    args.output.chmod(0o600)
    rows = census.get('unionCommits', census['selectedCommits'])
    counts = collections.Counter(dt.datetime.fromtimestamp(r['epoch'], dt.timezone.utc).date().isoformat() for r in rows.values())
    print(json.dumps({'cutoff': census['cutoff'], 'localRepositories': len(census['snapshots']), 'liveRemoteHeads': len(census['remoteBranches']),
                      'missingLocalTips': census['remoteTipsNotInLocalGraph'], 'remoteFrontierClosed': census.get('remoteParentFrontierClosed', False),
                      'uniqueCommits': len(rows), 'daily': dict(sorted(counts.items()))}))

if __name__ == '__main__':
    main()
