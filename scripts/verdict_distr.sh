python3 << 'EOF'
import json, collections
c = collections.defaultdict(lambda: collections.Counter())
for line in open('runs/stage1.jsonl'):
    r = json.loads(line)
    if r['parse_ok']:
        c[(r['model'], r['authenticity'])][r['verdict']] += 1
for k in sorted(c):
    attack = c[k][True]
    normal = c[k][False]
    total = attack + normal
    print(f"  {k[0]:15s} {k[1]:18s}  attack={attack} ({100*attack/total:.0f}%), normal={normal} ({100*normal/total:.0f}%)")
EOF
