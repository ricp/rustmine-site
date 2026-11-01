#!/usr/bin/env python3
"""Check the current chart, counters and accepted-head scope; optionally re-count Git."""
from pathlib import Path
import argparse, collections, datetime as dt, hashlib, json, re, subprocess

root = Path(__file__).resolve().parents[1]
data = json.loads((root/'data/commit-history.json').read_text())
days = data['daily']
start = dt.date.fromisoformat(data['range']['start'])
end = dt.date.fromisoformat(data['range']['end'])
assert [r['date'] for r in days] == [(start+dt.timedelta(days=i)).isoformat() for i in range((end-start).days+1)]
assert sum(r['shared'] for r in days) == data['heads']['shared']['uniqueNonMerge']
assert sum(r['portableOnly'] for r in days) == data['portableOnlyBeyondShared']
assert data['heads']['portable']['uniqueNonMerge'] == data['heads']['shared']['uniqueNonMerge']+data['portableOnlyBeyondShared']
assert data['heads']['shared']['uniqueNonMerge'] == data['heads']['mainline']['uniqueNonMerge']+data['sharedOnlyBeyondMainline']
assert 'Not first-parent' in data['ancestry']
journal = (root/'journal/index.html').read_text()
figure = re.search(r'<figure class="build-chart".*?</figure>',journal,re.S).group()
assert f'data-shared-head="{data["heads"]["shared"]["commit"]}"' in figure
assert f'data-portable-head="{data["heads"]["portable"]["commit"]}"' in figure
assert f'--days:{len(days)}' in figure
bars = re.findall(r'<a class="build-chart-day" data-date="([^"]+)" data-count="(\d+)" data-zero="(true|false)".*?<span class="build-value">(\d+)</span>.*?--height:([\d.]+)%',figure,re.S)
assert len(bars)==len(days),(len(bars),len(days))
maximum=max(r['shared'] for r in days)
for (date,count,zero,label,height),expected in zip(bars,days):
    assert date==expected['date'] and int(count)==int(label)==expected['shared']
    assert (zero=='true')==(expected['shared']==0)
    assert abs(float(height)-100*expected['shared']/maximum)<.051
    assert f'href="#build-day-{date}"' in figure
    header=re.search(rf'<details class="build-day" id="build-day-{date}"><summary>(.*?)</summary>',journal,re.S).group(1)
    assert f'{count} shared-ancestry commit' + ('' if int(count)==1 else 's') in header
if start.year == end.year and start.month == end.month:
    range_label=f'{start.day}–{end.day} {end:%B %Y}'
elif start.year == end.year:
    range_label=f'{start.day} {start:%B}–{end.day} {end:%B %Y}'
else:
    range_label=f'{start.day} {start:%B %Y}–{end.day} {end:%B %Y}'
assert range_label in figure
assert '68cd7f1' not in figure and '9cd23f9d' not in figure
assert 'all commits reachable' in re.search(r'id="commit-count-method".*?</details>',journal,re.S).group().lower()
example=data.get('excludedActivityExample')
if example:
    note=re.search(r'<p class="build-chart-note" id="excluded-commit-activity">(.*?)</p>',figure,re.S).group(1)
    for date in example['allCurrentlyReadableRefsUniqueNonMerge']:
        for scope in ['shared','portable']:
            assert data['heads'][scope]['daily'].get(date,0)==0, 'Zero-day explanation must be revised for the new accepted ancestry'
    assert example['allTheseDatedCommitsOutsideSharedAndPortable']
    a,b=example['allCurrentlyReadableRefsUniqueNonMerge'].values()
    assert f'<strong>{a} and {b}</strong>' in note
    assert example['sourceReviewedCheckpoint'][:8] in note
for name in ['index.html','progress/index.html']:
    text=(root/name).read_text()
    shared_region=text[text.index('<div class="build-latest"'):]
    shared_short=re.search(r'<code>([^<]+)</code>',shared_region).group(1)
    assert data['heads']['shared']['commit'].startswith(shared_short),(name,'shared head stale',shared_short)
    portable_match=re.search(r'<(aside|section) class="build-progress" data-commit-scope="portable"[^>]*>.*?</\1>',text,re.S)
    assert portable_match, (name,'explicit portable scope missing')
    portable_region=portable_match.group(0)
    portable_short=re.search(r'<code>([^<]+)</code>',portable_region).group(1)
    assert data['heads']['portable']['commit'].startswith(portable_short),(name,'portable head stale',portable_short)
    counter=re.search(r'<p data-commit-count-summary="true">(.*?)</p>',text,re.S).group(1)
    for count in [data['heads']['shared']['uniqueNonMerge'],data['heads']['mainline']['uniqueNonMerge'],data['portableOnlyBeyondShared']]:
        assert f'<strong>{count:,}</strong>' in counter
    # A later accepted/shared or portable milestone must extend the chart's date range.
    # Source-only cards do not extend accepted shared/portable ancestry.
    current_dates=[re.search(r'<time datetime="([^\"]+)"',region).group(1) for region in [shared_region,portable_region]]
    for value in current_dates:assert end>=dt.date.fromisoformat(value[:10]),(name,'chart ends before current milestone')

parser=argparse.ArgumentParser();parser.add_argument('--app-repo',type=Path);args=parser.parse_args()
if args.app_repo:
    sets={}
    for scope,head in data['heads'].items():
        rows={}
        for line in subprocess.check_output(['git','log','--no-merges','--format=%H %ct',head['commit']],cwd=args.app_repo,text=True).splitlines():
            sha,epoch=line.split();rows[sha]=int(epoch)
        dates=collections.Counter(dt.datetime.fromtimestamp(t,dt.timezone.utc).date().isoformat() for t in rows.values())
        assert len(rows)==head['uniqueNonMerge'] and dict(dates)==head['daily'],scope
        assert hashlib.sha256(('\n'.join(sorted(rows))+'\n').encode()).hexdigest()==head['shaSetSha256'],scope
        sets[scope]=set(rows)
    assert sets['mainline']<=sets['shared']<=sets['portable']
    assert len(sets['portable']-sets['shared'])==data['portableOnlyBeyondShared']
print(json.dumps({'pass':True,'utcDays':len(days),'sharedHead':data['heads']['shared']['commit'],'portableHead':data['heads']['portable']['commit'],'sharedUnique':data['heads']['shared']['uniqueNonMerge'],'portableOnly':data['portableOnlyBeyondShared'],'sourceGitRecount':bool(args.app_repo)}))
