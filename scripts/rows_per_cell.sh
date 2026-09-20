python3 << 'EOF'
import json, collections
c = collections.Counter()
for line in open('runs/stage1.jsonl'):
    r = json.loads(line)
    c[(r['model'], r['authenticity'])] += 1
for k in sorted(c):
    print(f"  {k[0]:15s} {k[1]:18s}  {c[k]:3d} rows")
EOF
