#!/usr/bin/env bash
# mado round 32 — wave-1 seat dispatcher.
# One batched dispatch of the validated wave: every seat in the validator's taskCall
# is launched concurrently, one `omp -p` process per seat, each carrying the seat's
# composed task text unchanged. Route table: the operator's `task.agentModelOverrides`
# in ~/.omp/agent/config.yml decides the alias per taxonomy role; no provider/model
# literal is hardcoded here and none is written into the lane repo.
# Seats write only their own report and their named scratch dir; they never touch the
# fleet repo, a sibling lane, the lane jj state or the lane Git index.
# Exit codes: 0 = all seats finished (per-seat codes in the manifest), 1 = launcher error.

set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
W="$LANE/.ufo/waves/round-32"
TASKCALL="$W/w1-taskcall.json"
LOGS="$W/w1/logs"
PROMPTS="$W/w1/prompts"
MANIFEST="$W/w1/manifest.json"
mkdir -p "$LOGS" "$PROMPTS"

python3 - "$TASKCALL" "$PROMPTS" > "$W/w1/seat-plan.tsv" <<'PY'
import json, sys, os, re
taskcall, prompts_dir = sys.argv[1], sys.argv[2]
d = json.load(open(taskcall))
tasks = d["taskCall"]["tasks"]
# Route table: the operator's own binding (read-only). Role decides the route.
cfg = open(os.path.expanduser("~/.omp/agent/config.yml")).read()
m = re.search(r"^  agentModelOverrides:\n((?:    .*\n)+)", cfg, re.M)
overrides = {}
for line in m.group(1).splitlines():
    k, _, v = line.strip().partition(":")
    overrides[k.strip()] = v.strip().strip('"')
for t in tasks:
    role = t["agent"]
    alias = overrides.get(role, "@m_kfc")
    p = os.path.join(prompts_dir, t["name"] + ".txt")
    open(p, "w").write(t["task"])
    print(f"{t['name']}\t{role}\t{alias}\t{p}")
PY
if [[ ! -s "$W/w1/seat-plan.tsv" ]]; then echo "dispatcher: empty seat plan" >&2; exit 1; fi

echo "dispatcher: launching $(wc -l < "$W/w1/seat-plan.tsv") seats concurrently"
: > "$W/w1/exit-codes.tsv"
while IFS=$'\t' read -r name role alias prompt; do
  (
    cd "$LANE" || exit 9
    timeout 1500 omp -p --no-session --approval-mode yolo --model "$alias" --cwd "$LANE" \
      --max-time 22m "$(cat "$prompt")" > "$LOGS/$name.log" 2>&1
    echo "$? $name $role $alias" >> "$W/w1/exit-codes.tsv"
  ) &
done < "$W/w1/seat-plan.tsv"
wait

python3 - "$W/w1/exit-codes.tsv" "$MANIFEST" "$W/w1/seat-plan.tsv" <<'PY'
import json, sys
codes, manifest, plan = sys.argv[1], sys.argv[2], sys.argv[3]
rows = []
for line in open(codes):
    parts = line.split(None, 3)
    if len(parts) == 4:
        rows.append({"seat": parts[1], "role": parts[2], "alias": parts[3], "exit": int(parts[0])})
plan_rows = [l.split("\t") for l in open(plan).read().splitlines() if l.strip()]
by_name = {r[0]: r[2] for r in plan_rows}
for r in rows:
    r["alias"] = by_name.get(r["seat"], r["alias"])
out = {"wave": "mado-r32-w1", "seats": len(plan_rows), "finished": len(rows),
       "dead": [r["seat"] for r in rows if r["exit"] != 0], "rows": sorted(rows, key=lambda r: r["seat"])}
json.dump(out, open(manifest, "w"), indent=1)
print(f"dispatcher: {len(rows)}/{len(plan_rows)} seats finished; dead={out['dead']}")
PY
exit 0
