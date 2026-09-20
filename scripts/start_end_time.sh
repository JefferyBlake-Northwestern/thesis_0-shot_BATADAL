python3 << 'EOF'
import json
from datetime import datetime

first_ts = last_ts = None
count = 0
for line in open('runs/stage1.jsonl'):
    r = json.loads(line)
    ts = r.get('ts')
    if ts:
        if first_ts is None:
            first_ts = ts
        last_ts = ts
        count += 1

if first_ts and last_ts:
    t0 = datetime.fromtimestamp(first_ts)
    t1 = datetime.fromtimestamp(last_ts)
    elapsed_h = (last_ts - first_ts) / 3600
    print(f"First row: {t0.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Last row:  {t1.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Elapsed:   {elapsed_h:.2f} hours")
    print(f"Total rows: {count}")
    print(f"Rate: {count / elapsed_h:.1f} rows/hour")
EOF
