python3 << 'EOF'
import json, collections, pandas as pd
df = pd.read_csv('data/BATADAL_test_dataset.csv')

results = collections.defaultdict(lambda: {'tp':0,'fp':0,'fn':0,'tn':0})
for line in open('runs/stage1.jsonl'):
    r = json.loads(line)
    if not r.get('parse_ok'): continue
    wid = int(r['window_id'].lstrip('w'))
    start = wid * 24
    end = min(start + 24, 2089)
    flagged = set(r.get('flagged_offsets') or [])
    key = (r['model'], r['authenticity'])
    for hour_idx, offset in enumerate(range(start, end)):
        gt = df.iloc[offset]['ATT_FLAG'] == 1.0
        pred = hour_idx in flagged
        if gt and pred: results[key]['tp'] += 1
        elif gt and not pred: results[key]['fn'] += 1
        elif not gt and pred: results[key]['fp'] += 1
        else: results[key]['tn'] += 1

print(f"{'model':15s} {'authenticity':18s}   P      R      F1     TP/FP/FN/TN")
for k in sorted(results):
    s = results[k]
    prec = s['tp']/(s['tp']+s['fp']) if (s['tp']+s['fp']) else 0
    rec = s['tp']/(s['tp']+s['fn']) if (s['tp']+s['fn']) else 0
    f1 = 2*prec*rec/(prec+rec) if (prec+rec) else 0
    print(f"  {k[0]:15s} {k[1]:18s}  {prec:.3f}  {rec:.3f}  {f1:.3f}   {s['tp']}/{s['fp']}/{s['fn']}/{s['tn']}")
EOF
