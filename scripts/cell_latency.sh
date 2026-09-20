python3 << 'EOF'
import json, collections
c = collections.defaultdict(list)
for line in open('runs/stage1.jsonl'):
    r = json.loads(line)
    lat = r.get('latency_s')
    if lat:
        c[(r['model'], r['authenticity'])].append(lat)
for k in sorted(c):
    lats = c[k]
    avg = sum(lats) / len(lats)
    total_h = sum(lats) / 3600
    remaining_rows = 264 - len(lats)
    eta_h = remaining_rows * avg / 3600 if avg else 0
    print(f"  {k[0]:15s} {k[1]:18s}  n={len(lats)}, avg={avg:.1f}s, elapsed={total_h:.1f}h, eta={eta_h:.1f}h")
EOF
