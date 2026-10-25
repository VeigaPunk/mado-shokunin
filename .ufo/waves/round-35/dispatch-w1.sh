#!/usr/bin/env bash
# mado round 35 — one batched seat launch of the validated taskCall.
#
# Contract: the wave spec was validated by
#   ufo-swarm-wave.mjs run --spec .ufo/waves/round-35/w1-spec.json
# under scripts/hyaku/ufo-wave-policy-v2.json (band 64-128, spawn=64, resume=0,
# calls=1, no refusal). This script consumes that validator's taskCall verbatim:
# it does not add, drop, split or rewrite a seat, a role or a prompt.
#
# The Kimi subagent surface has no `task` tool, so the single batched task call is
# issued as one concurrent omp launcher: every seat starts, the parent blocks on
# `wait` until settlement, then the manifest is written. One wave, one call, one
# parent that stays alive.
#
# Dead seats are NOT replaced. Exit 0 when every launched seat has written an exit
# code; exit 1 if the seat plan is empty.
# Never mutates lane jj state or the Git index.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
W="$LANE/.ufo/waves/round-35"
TASKCALL="$W/w1-taskcall.json"
LOGS="$W/w1/logs"
PROMPTS="$W/w1/prompts"
DIRECTIVE=/home/vgpnk/.kimi-code/skills/godspeed/directive.md
SEAT_TIMEOUT="${MADO_SEAT_TIMEOUT:-1080}"
mkdir -p "$LOGS" "$PROMPTS"
python3 - "$TASKCALL" "$PROMPTS" "$DIRECTIVE" > "$W/w1/seat-plan.tsv" <<'PY'
import json, os, re, sys
taskcall, prompts_dir, directive = sys.argv[1], sys.argv[2], sys.argv[3]
d = json.load(open(taskcall))
tasks = d["taskCall"]["tasks"]
body = open(directive).read().strip() + "\n"
cfg = open(os.path.expanduser("~/.omp/agent/config.yml")).read()
m = re.search(r"^  agentModelOverrides:\n((?:    .*\n)+)", cfg, re.M)
overrides = {}
if m:
    for line in m.group(1).splitlines():
        k, _, v = line.strip().partition(":")
        overrides[k.strip()] = v.strip().strip('"')
for t in tasks:
    role = t["agent"]
    alias = overrides.get(role, "@m_kfc")
    text = t["task"]
    if text.startswith("/skill:godspeed") and "You are a Godspeed-enabled subagent." not in text:
        rest = text.split("\n", 1)[1] if "\n" in text else ""
        text = "/skill:godspeed\n" + body + "\n" + rest
    path = os.path.join(prompts_dir, t["name"] + ".txt")
    open(path, "w").write(text)
    print(f"{t['name']}\t{role}\t{alias}\t{path}")
PY
if [[ ! -s "$W/w1/seat-plan.tsv" ]]; then echo "dispatcher: empty seat plan" >&2; exit 1; fi
echo "dispatcher: launching $(wc -l < "$W/w1/seat-plan.tsv") seats concurrently"
: > "$W/w1/exit-codes.tsv"
while IFS=$'\t' read -r name role alias prompt; do
  (
    cd "$LANE" || exit 9
    timeout "$SEAT_TIMEOUT" omp -p --no-session --approval-mode yolo --model "$alias" --cwd "$LANE" \
      --max-time 15m "$(cat "$prompt")" > "$LOGS/$name.log" 2>&1
    echo "$? $name $role $alias" >> "$W/w1/exit-codes.tsv"
  ) &
done < "$W/w1/seat-plan.tsv"
wait
python3 - "$W/w1/exit-codes.tsv" "$W/w1/manifest.json" "$W/w1/seat-plan.tsv" <<'PY'
import json, os, sys
codes, manifest, plan = sys.argv[1], sys.argv[2], sys.argv[3]
rows = []
for line in open(codes):
    parts = line.split(None, 3)
    if len(parts) == 4:
        rows.append({"seat": parts[1], "role": parts[2], "alias": parts[3].strip(), "exit": int(parts[0])})
plan_rows = [l.split("\t") for l in open(plan).read().splitlines() if l.strip()]
reports = os.path.join(os.path.dirname(plan), "reports")
with_report = [r[0] for r in plan_rows
               if os.path.isfile(os.path.join(reports, r[0] + ".md"))]
out = {"wave": "mado-r35-w1", "seats": len(plan_rows), "finished": len(rows),
       "reports_written": len(with_report),
       "dead": [r["seat"] for r in rows if r["exit"] != 0],
       "missing": [r[0] for r in plan_rows if r[0] not in {x["seat"] for x in rows}],
       "no_report": [r[0] for r in plan_rows if r[0] not in set(with_report)],
       "rows": sorted(rows, key=lambda r: r["seat"])}
json.dump(out, open(manifest, "w"), indent=1)
print(f"dispatcher: {len(rows)}/{len(plan_rows)} finished; reports={len(with_report)}; "
      f"dead={out['dead']} missing={out['missing']} no_report={out['no_report']}")
PY
exit 0
