python3 << 'EOF'
import json, collections
cells = collections.defaultdict(lambda: {'first_ts': None, 'last_ts': None, 'last_lat': 0, 'n': 0, 'sum_lat': 0})
for line in open('runs/stage1.jsonl'):
    r = json.loads(line)
    key = (r['model'], r['authenticity'])
    ts = r.get('ts')
    lat = r.get('latency_s', 0)
    if cells[key]['first_ts'] is None:
        cells[key]['first_ts'] = ts
    cells[key]['last_ts'] = ts
    cells[key]['last_lat'] = lat
    cells[key]['sum_lat'] += lat
    cells[key]['n'] += 1

print(f"{'model':15s} {'authenticity':18s}  wall_clock_h  sum_lat_h  n")
for k in sorted(cells):
    c = cells[k]
    if c['n'] > 1:
        wall_h = (c['last_ts'] - c['first_ts'] + c['last_lat']) / 3600
        sum_h = c['sum_lat'] / 3600
        print(f"  {k[0]:15s} {k[1]:18s}  {wall_h:12.2f}  {sum_h:9.2f}  {c['n']}")
EOF
