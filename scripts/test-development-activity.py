"""Small graph check: dedupe, merge inclusion, UTC cutoff and closed remote ancestry."""
import copy, importlib.util, sys
sys.dont_write_bytecode = True
from pathlib import Path
spec = importlib.util.spec_from_file_location('collector', Path(__file__).with_name('collect-development-activity.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
a, b, c, future, absent = [str(i) * 40 for i in range(1, 6)]
epoch = 1795305600  # 22 November 2026 00:00 UTC
base = {'cutoff': '2026-11-23T07:12:17+00:00', 'graph': {a: {'epoch': epoch, 'parents': []}},
        'selectedCommits': {a: {'epoch': epoch, 'parents': []}},
        'remoteBranches': [{'sha': c}, {'sha': c}, {'sha': future}]}
rows = {a: {'committer': '2026-11-22T00:00:00Z', 'parents': []},
        b: {'committer': '2026-11-23T00:00:00Z', 'parents': [a]},
        c: {'committer': '2026-11-23T01:00:00Z', 'parents': [a, b]},
        future: {'committer': '2026-11-24T00:00:00Z', 'parents': [c]}}
result = m.reconcile(copy.deepcopy(base), rows)
assert set(result['unionCommits']) == {a, b, c}
assert sum(len(x['parents']) > 1 for x in result['unionCommits'].values()) == 1
assert result['remoteParentFrontierClosed']
bad = copy.deepcopy(base); bad['remoteBranches'].append({'sha': absent})
try:
    m.reconcile(bad, rows)
except AssertionError:
    pass
else:
    raise AssertionError('Unresolved ancestry must block publication')
assert m.excluded_ref('refs/heads/tmp/check') and m.excluded_ref('codex/stock-preview-pending-import-backup')
assert not m.excluded_ref('refs/heads/feature/issues')
print('Passed: full-SHA dedupe, merges, cutoff, missing ancestry refusal and excluded refs')
