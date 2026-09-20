python3 << 'EOF'
import json, collections, pandas as pd
df = pd.read_csv('data/BATADAL_test_dataset.csv')

def window_has_attack(wid_str):
    wid = int(wid_str.lstrip('w'))
    return df.iloc[wid*24:(wid+1)*24]['ATT_FLAG'].sum() > 0

stats = collections.defaultdict(lambda: {'attack_parse_ok': 0, 'attack_parse_fail': 0, 
                                          'normal_parse_ok': 0, 'normal_parse_fail': 0})
for line in open('runs/stage1.jsonl'):
    r = json.loads(line)
    if r['model'] != 'opus-5': continue
    key = r['authenticity']
    has_attack = window_has_attack(r['window_id'])
    if r.get('parse_ok'):
        if has_attack: stats[key]['attack_parse_ok'] += 1
        else: stats[key]['normal_parse_ok'] += 1
    else:
        if has_attack: stats[key]['attack_parse_fail'] += 1
        else: stats[key]['normal_parse_fail'] += 1

print(f"{'authenticity':18s}  attack_ok/attack_total  normal_ok/normal_total")
for k in sorted(stats):
    s = stats[k]
    at_ok, at_fail = s['attack_parse_ok'], s['attack_parse_fail']
    nl_ok, nl_fail = s['normal_parse_ok'], s['normal_parse_fail']
    at_total = at_ok + at_fail
    nl_total = nl_ok + nl_fail
    print(f"  {k:18s}  {at_ok}/{at_total} ({100*at_ok/max(at_total,1):.0f}%)  {nl_ok}/{nl_total} ({100*nl_ok/max(nl_total,1):.0f}%)")
EOF
