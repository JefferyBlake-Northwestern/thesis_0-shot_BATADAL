python3 << 'EOF'
import json, collections
from datetime import datetime

cells = collections.defaultdict(lambda: {'first': None, 'last': None, 'n': 0})
for line in open('runs/stage1.jsonl'):
    r = json.loads(line)
    ts = r.get('ts')
    key = (r['model'], r['authenticity'])
    if cells[key]['first'] is None:
        cells[key]['first'] = ts
    cells[key]['last'] = ts
    cells[key]['n'] += 1

print(f"{'model':15s} {'authenticity':18s}  {'start':19s}  {'end':19s}  {'hours':>6s}  n")
for k in sorted(cells):
    c = cells[k]
    t0 = datetime.fromtimestamp(c['first']).strftime('%m-%d %H:%M:%S')
    t1 = datetime.fromtimestamp(c['last']).strftime('%m-%d %H:%M:%S')
    hours = (c['last'] - c['first']) / 3600
    print(f"  {k[0]:15s} {k[1]:18s}  {t0}  {t1}  {hours:6.2f}  {c['n']}")
EOF
