#!/usr/bin/env python3
"""Validate the committed-activity series; optionally recount a private captured-ref census."""
from pathlib import Path
import argparse,collections,datetime as dt,importlib.util,json,re,subprocess,sys
sys.dont_write_bytecode=True
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'data/development-activity.json').read_text())
start_day=dt.date.fromisoformat(data['range']['start']);end_day=dt.date.fromisoformat(data['range']['end'])
assert [r['date'] for r in data['daily']]==[(start_day+dt.timedelta(days=i)).isoformat() for i in range((end_day-start_day).days+1)]
assert dt.datetime.fromisoformat(data['countedAtUtc']).date()==end_day
assert 'including merge commits' in data['method']
assert sum(r['commits'] or 0 for r in data['daily'])==data['totalUniqueCommits']
assert sum(r['mergeCommits'] or 0 for r in data['daily'])==data['mergeCommits']
assert all((r['commits'] is None)==(r['mergeCommits'] is None) for r in data['daily'])
text=(root/'journal/index.html').read_text()
figure=re.search(r'<figure class="build-chart activity-chart".*?</figure>',text,re.S).group()
bars=re.findall(r'<a class="build-chart-day" data-date="([^"]+)" data-count="([^"]+)".*?</a>',figure,re.S)
known=[r for r in data['daily'] if r['commits'] is not None]
assert len(bars)==len(known)
maximum=max(r['commits'] or 0 for r in data['daily'])
for (date,count),row in zip(bars,known):
 assert date==row['date']
 assert count==('unknown' if row['commits'] is None else str(row['commits']))
 assert f'href="#activity-{date}"' in figure
 assert f'id="activity-{date}"' in text
 bar=re.search(rf'<a class="build-chart-day" data-date="{date}".*?</a>',figure,re.S).group()
 if row['commits'] is None:assert 'Count not established' in bar and '<span class="build-value">—</span>' in bar
 else:assert abs(float(re.search(r'--height:([\d.]+)%',bar).group(1))-100*row['commits']/maximum)<.051
pages=re.findall(r'<section class="build-chart-page".*?</section>',figure,re.S)
assert len(pages)==(len(data['daily'])+6)//7
for page,offset in zip(pages,range(0,len(data['daily']),7)):
 rows=data['daily'][offset:offset+7]
 assert page.count('class="build-chart-day"')==sum(r['commits'] is not None for r in rows)
 assert ' hidden' not in page
 for row in rows:
  if row['commits'] is None:
   assert f'data-activity-date="{row["date"]}"' in page
   assert 'Commit numbers unavailable for these days' in page
assert 'data-count="unknown"' not in figure
assert 'data-latest-label="Latest activity week"' in figure
assert 'commit numbers are unavailable' in figure
assert data['countedAtUtc'] in figure
assert 'id="activity"' in text and text.index('id="activity"')<text.index('data-chart-scope="historical"')
for path in ['index.html','progress/index.html']:
 banner=(root/path).read_text()
 assert 'href="/journal/#activity"' in banner
 assert f'data-activity-cutoff="{data["countedAtUtc"]}"' in banner
 assert f'{data["totalUniqueCommits"]:,} application commits' in banner
 assert f'latest day: {data["daily"][-1]["commits"]} commits' in banner
for path in ['index.html','progress/index.html','journal/index.html']:
 page=(root/path).read_text();date=end_day.isoformat()
 assert f'<time datetime="{date}">{end_day.day} NOV {end_day.year}</time>' in page
 assert f'Site content updated · <time datetime="{date}">{end_day.day} November {end_day.year} UTC</time>' in page
public=(root/'data/development-activity.json').read_text()+re.search(r'<section class="build-recent".*?</section>\s*<p class="build-jump"',text,re.S).group()
assert not re.search(r'\b[0-9a-f]{40}\b',public),'Private commit identities must stay out of the new aggregate series'
assert '/Users/' not in public and '/Volumes/' not in public and 'refs/heads/' not in public
parser=argparse.ArgumentParser();parser.add_argument('--census',type=Path);parser.add_argument('--remote-union',type=Path);parser.add_argument('--remote-history',type=Path);args=parser.parse_args()
if args.census:
 census=json.loads(args.census.read_text());cutoff=dt.datetime.fromisoformat(census['cutoff']).timestamp();start=dt.datetime(2026,11,1,tzinfo=dt.timezone.utc).timestamp();commits={};local_graph={}
 assert census['cutoff']==data['countedAtUtc']
 for snap in census['snapshots']:
  out=subprocess.check_output(['git','-C',snap['repo'],'rev-list','--timestamp','--parents','--stdin'],input='\n'.join(snap['tips'])+'\n',text=True)
  for line in out.splitlines():
   fields=line.split();epoch=int(fields[0]);sha=fields[1];parents=fields[2:]
   row={'epoch':epoch,'parents':parents};assert sha not in local_graph or local_graph[sha]==row;local_graph[sha]=row
   if start<=epoch<=cutoff:
    value=(epoch,len(parents)>1)
    if sha in commits:assert commits[sha]==value
    commits[sha]=value
 assert set(commits)==set(census['selectedCommits'])
 if args.remote_history:
  assert not args.remote_union
  assert local_graph==census['graph'],'Captured local graph changed'
  spec=importlib.util.spec_from_file_location('activity_collector',root/'scripts/collect-development-activity.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
  reconciled=module.reconcile(dict(census,graph=local_graph),json.loads(args.remote_history.read_text())['rows'])
  assert reconciled['unionCommits']==census['unionCommits'] and reconciled['remoteParentFrontierClosed']
  commits={sha:(row['epoch'],len(row['parents'])>1) for sha,row in reconciled['unionCommits'].items()}
 if args.remote_union:
  remote=json.loads(args.remote_union.read_text());assert remote['parentFrontierClosed'] and not remote['missingFrontier']
  assert not (set(commits)&set(remote['newNovember']))
  for sha,row in remote['newNovember'].items():commits[sha]=(int(dt.datetime.fromisoformat(row['committer'].replace('Z','+00:00')).timestamp()),len(row['parents'])>1)
 counts=collections.Counter(dt.datetime.fromtimestamp(epoch,dt.timezone.utc).date().isoformat() for epoch,_ in commits.values())
 merges=collections.Counter(dt.datetime.fromtimestamp(epoch,dt.timezone.utc).date().isoformat() for epoch,merge in commits.values() if merge)
 for row in data['daily']:
  if row['commits'] is not None:assert row['commits']==counts[row['date']] and row['mergeCommits']==merges[row['date']]
 assert len(commits)==data['totalUniqueCommits'] and sum(merges.values())==data['mergeCommits']
print(json.dumps(dict(passed=True,total=data['totalUniqueCommits'],mergeCommits=data['mergeCommits'],days=len(data['daily']),knownDays=sum(r['commits'] is not None for r in data['daily']),cutoff=data['countedAtUtc'],independentCapturedGitRecount=bool(args.census))))
