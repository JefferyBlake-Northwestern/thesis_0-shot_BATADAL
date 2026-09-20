python3 << 'EOF'
import json, collections
c = collections.defaultdict(lambda: [0, 0])
for line in open('runs/stage1.jsonl'):
    r = json.loads(line)
    c[(r['model'], r['authenticity'])][0 if r['parse_ok'] else 1] += 1
for k in sorted(c):
    ok, fail = c[k]
    total = ok + fail
    print(f"  {k[0]:15s} {k[1]:18s}  {ok}/{total} parse_ok ({100*ok/total:.1f}%)")
EOF
