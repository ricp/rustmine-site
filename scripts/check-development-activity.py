#!/usr/bin/env python3
"""Validate the committed-activity series; optionally recount a private captured-ref census."""
from pathlib import Path
import argparse,collections,datetime as dt,json,re,subprocess
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'data/development-activity.json').read_text())
assert 'including merge commits' in data['method']
assert sum(r['commits'] or 0 for r in data['daily'])==data['totalUniqueCommits']
assert sum(r['mergeCommits'] or 0 for r in data['daily'])==data['mergeCommits']
assert all((r['commits'] is None)==(r['mergeCommits'] is None) for r in data['daily'])
text=(root/'journal/index.html').read_text()
figure=re.search(r'<figure class="build-chart activity-chart".*?</figure>',text,re.S).group()
bars=re.findall(r'<a class="build-chart-day" data-date="([^"]+)" data-count="([^"]+)".*?</a>',figure,re.S)
assert len(bars)==len(data['daily'])
maximum=max(r['commits'] or 0 for r in data['daily'])
for (date,count),row in zip(bars,data['daily']):
 assert date==row['date']
 assert count==('unknown' if row['commits'] is None else str(row['commits']))
 assert f'href="#activity-{date}"' in figure
 assert f'id="activity-{date}"' in text
 bar=re.search(rf'<a class="build-chart-day" data-date="{date}".*?</a>',figure,re.S).group()
 if row['commits'] is None:assert 'Count not established' in bar and '<span class="build-value">—</span>' in bar
 else:assert abs(float(re.search(r'--height:([\d.]+)%',bar).group(1))-100*row['commits']/maximum)<.051
pages=re.findall(r'<section class="build-chart-page".*?</section>',figure,re.S)
assert len(pages)==3 and all(p.count('class="build-chart-day"')==7 and ' hidden' not in p for p in pages)
assert 'data-latest-label="Latest counted week"' in figure
assert '4–14 November counts are not established' in figure
assert '2026-11-21T09:54:40.888023+00:00' in figure
assert 'id="activity"' in text and text.index('id="activity"')<text.index('data-chart-scope="historical"')
for path in ['index.html','progress/index.html']:assert 'href="/journal/#activity"' in (root/path).read_text()
public=(root/'data/development-activity.json').read_text()+re.search(r'<section class="build-recent".*?</section>\s*<p class="build-jump"',text,re.S).group()
assert not re.search(r'\b[0-9a-f]{40}\b',public),'Private commit identities must stay out of the new aggregate series'
assert '/Users/' not in public and '/Volumes/' not in public and 'refs/heads/' not in public
parser=argparse.ArgumentParser();parser.add_argument('--census',type=Path);args=parser.parse_args()
if args.census:
 census=json.loads(args.census.read_text());cutoff=dt.datetime.fromisoformat(census['cutoff']).timestamp();start=dt.datetime(2026,11,1,tzinfo=dt.timezone.utc).timestamp();commits={}
 for snap in census['snapshots']:
  out=subprocess.check_output(['git','-C',snap['repo'],'rev-list','--timestamp','--parents','--stdin'],input='\n'.join(snap['tips'])+'\n',text=True)
  for line in out.splitlines():
   fields=line.split();epoch=int(fields[0]);sha=fields[1];parents=fields[2:]
   if start<=epoch<=cutoff:
    value=(epoch,len(parents)>1)
    if sha in commits:assert commits[sha]==value
    commits[sha]=value
 assert set(commits)==set(census['selectedCommits'])
 counts=collections.Counter(dt.datetime.fromtimestamp(epoch,dt.timezone.utc).date().isoformat() for epoch,_ in commits.values())
 merges=collections.Counter(dt.datetime.fromtimestamp(epoch,dt.timezone.utc).date().isoformat() for epoch,merge in commits.values() if merge)
 for row in data['daily']:
  if row['commits'] is not None:assert row['commits']==counts[row['date']] and row['mergeCommits']==merges[row['date']]
 assert len(commits)==data['totalUniqueCommits'] and sum(merges.values())==data['mergeCommits']
print(json.dumps(dict(passed=True,total=data['totalUniqueCommits'],mergeCommits=data['mergeCommits'],days=len(data['daily']),knownDays=sum(r['commits'] is not None for r in data['daily']),cutoff=data['countedAtUtc'],independentCapturedGitRecount=bool(args.census))))
