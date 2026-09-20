python3 << 'EOF'
import json, collections
c = collections.defaultdict(lambda: {'end_turn': 0, 'max_tokens': 0, 'other': 0})
for line in open('runs/stage1.jsonl'):
    r = json.loads(line)
    reason = r.get('response_stop_reason', 'unknown')
    if reason == 'end_turn':
        c[(r['model'], r['authenticity'])]['end_turn'] += 1
    elif reason == 'max_tokens':
        c[(r['model'], r['authenticity'])]['max_tokens'] += 1
    else:
        c[(r['model'], r['authenticity'])]['other'] += 1

print(f"{'model':15s} {'authenticity':18s}  end_turn max_tokens other")
for k in sorted(c):
    s = c[k]
    total = s['end_turn'] + s['max_tokens'] + s['other']
    print(f"  {k[0]:15s} {k[1]:18s}  {s['end_turn']:8d} {s['max_tokens']:10d} {s['other']:5d}  ({total} total)")
EOF
