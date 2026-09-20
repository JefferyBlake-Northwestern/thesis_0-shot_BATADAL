python3 << 'EOF'
import json, collections
# What's the latest cell being worked on?
latest = None
for line in open('runs/stage1.jsonl'):
    r = json.loads(line)
    latest = (r['model'], r['authenticity'], r['replicate'])

if latest:
    print(f"Latest cell: {latest[0]} {latest[1]} rep{latest[2]}")
    v = collections.Counter()
    parse_ok = parse_fail = 0
    for line in open('runs/stage1.jsonl'):
        r = json.loads(line)
        if (r['model'], r['authenticity'], r['replicate']) == latest:
            v[r['verdict']] += 1
            if r.get('parse_ok'):
                parse_ok += 1
            else:
                parse_fail += 1
    total = parse_ok + parse_fail
    print(f"  Rows: {total}/88 ({100*total/88:.0f}%)")
    print(f"  Parse OK: {parse_ok}/{total} ({100*parse_ok/total:.0f}%)")
    print(f"  Verdicts (of parsed): attack={v.get(True, 0)}, normal={v.get(False, 0)}")
EOF

