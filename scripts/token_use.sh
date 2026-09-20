python3 << 'EOF'
import json, collections
c = collections.defaultdict(list)
for line in open('runs/stage1.jsonl'):
    r = json.loads(line)
    tokens = r.get('response_output_tokens')
    if tokens is not None:
        c[(r['model'], r['authenticity'])].append(tokens)

print(f"{'model':15s} {'authenticity':18s}  {'n':>4s} {'avg':>7s} {'max':>6s} {'≥16k':>5s}")
for k in sorted(c):
    tokens = c[k]
    avg = sum(tokens) / len(tokens)
    mx = max(tokens)
    n_ceiling = sum(1 for t in tokens if t >= 16000)
    print(f"  {k[0]:15s} {k[1]:18s}  {len(tokens):4d} {avg:7.0f} {mx:6d} {n_ceiling:5d}")
EOF
