python3 << 'EOF'
import json
lines = list(open('runs/stage1.jsonl'))
for line in lines[-10:]:
    r = json.loads(line)
    lat = r.get('latency_s', 0)
    tokens = r.get('response_output_tokens', '?')
    print(f"  {r['model']:15s} {r['authenticity']:18s} rep{r['replicate']} {r['window_id']}  "
          f"parse={r['parse_ok']}, verdict={r['verdict']}, {lat:.1f}s, {tokens}tok")
EOF
