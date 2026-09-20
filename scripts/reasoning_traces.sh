python3 << 'EOF'
import json, pandas as pd, collections
df = pd.read_csv('data/BATADAL_test_dataset.csv')
saved = collections.defaultdict(list)
for line in open('runs/stage1.jsonl'):
    r = json.loads(line)
    if not r.get('parse_ok'):
        continue
    wid = int(r['window_id'].lstrip('w'))
    gt_attack = int(df.iloc[wid*24:(wid+1)*24]['ATT_FLAG'].sum())
    key = (r['model'], r['authenticity'], r['verdict'], gt_attack > 0)
    if len(saved[key]) < 3:
        saved[key].append(r)

with open('reasoning_samples.md', 'w') as f:
    f.write("# Reasoning traces (3 samples per model x authenticity x verdict x ground truth)\n\n")
    for k in sorted(saved):
        model, auth, verdict, has_attack = k
        gt_label = "attack window" if has_attack else "normal window"
        f.write(f"## {model} {auth}: verdict={'attack' if verdict else 'normal'} on {gt_label}\n\n")
        for r in saved[k]:
            f.write(f"**{r['window_id']} rep{r['replicate']}:** {r.get('response_text', '')[:500]}\n\n")
print("Saved to reasoning_samples.md")
EOF
