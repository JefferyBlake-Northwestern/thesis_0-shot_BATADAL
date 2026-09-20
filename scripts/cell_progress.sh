python3 << 'EOF'
import json, collections
c = collections.Counter()
for line in open('runs/stage1.jsonl'):
    r = json.loads(line)
    c[(r['model'], r['authenticity'], r['replicate'])] += 1

# Print in expected execution order
for model in ['opus-5', 'gpt-5.6-sol', 'grok-4']:
    for auth in ['native', 'schema_preserved', 'obfuscated']:
        for rep in [0, 1, 2]:
            n = c.get((model, auth, rep), 0)
            bar_len = int(n / 88 * 30)
            bar = '█' * bar_len + '░' * (30 - bar_len)
            status = '✓' if n == 88 else ('→' if n > 0 else ' ')
            print(f"  {status} {model:15s} {auth:18s} rep{rep}  [{bar}] {n:3d}/88")
EOF

