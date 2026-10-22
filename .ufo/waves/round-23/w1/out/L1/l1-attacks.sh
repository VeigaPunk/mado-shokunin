#!/usr/bin/env bash
# L1 scratch check: run the lane's candidate tools/mado-tripwire.py against the repair set and every
# wave-1/wave-2 attack fixture set, in a fresh scratch clone. Usage: l1-attacks.sh NAME
set -euo pipefail
L=/home/vgpnk/Projects/shokunin/mado-shokunin
D=/fast/scratch/hyaku/mado-r23/L1-$1
rm -rf "$D"; git clone -q "$L" "$D"; cp "$L/tools/mado-tripwire.py" "$D/tools/"
cd "$D"; git -c user.name=v -c user.email=v@v commit -qam "$1"
sha256sum tools/mado-tripwire.py
T="$D/tools/mado-tripwire.py"; B="$D/.ufo/waves/round-23/evidence/tool-base-cd9da20c.py"
python3 -I "$L/.ufo/waves/round-23/repair/measure.py" --tool "$T" | python3 -c 'import json,sys;d=json.load(sys.stdin);print("repair",d.get("passed"),d.get("total"),d.get("error"),[r["id"] for r in d.get("results",[]) if not r["passed"]])'
python3 -I "$L/.ufo/waves/round-22/oracle/measure.py" --tool "$T" > /tmp/r22o.json; python3 -c 'import json;d=json.load(open("/tmp/r22o.json"));print("r22oracle",d.get("status"),d.get("summary",d.get("counts")))' || true
mkdir -p .ufo/waves/round-23/w2/out .ufo/waves/round-23/w1/out
cp -r "$L"/.ufo/waves/round-23/w2/out/* .ufo/waves/round-23/w2/out/ 2>/dev/null || true
cp -r "$L"/.ufo/waves/round-23/w1/out/Crit* .ufo/waves/round-23/w1/out/
# AttackFrameScopes
cd .ufo/waves/round-23/w2/out/AttackFrameScopes/discovery; cp "$B" base.py; cp "$T" tool.py
python3 -I mkprobes.py probes >/dev/null; python3 -I probe.py probes /fast/scratch/hyaku/mado-r23/afs-p1.json >/dev/null
python3 -I mkprobes2.py probes2 >/dev/null; python3 -I probe.py probes2 /fast/scratch/hyaku/mado-r23/afs-p2.json >/dev/null
python3 -I probe.py ../fixtures /fast/scratch/hyaku/mado-r23/afs-fx.json >/dev/null
cd "$D"
for f in afs-p1 afs-p2 afs-fx; do python3 - "$D/../$f.json" "$f" <<'EOF'
import json,sys,collections
d=json.load(open(sys.argv[1])); res=d if isinstance(d,list) else (d.get("results") or d.get("cases"))
print(sys.argv[2], dict(collections.Counter(r["verdict"] for r in res)), [r["id"] for r in res if r["verdict"]=="REGRESSED"])
EOF
done
# AttackEscapeGate
(cd .ufo/waves/round-23/w2/out/AttackEscapeGate && python3 -I run.py "$B" "$T" | python3 -c 'import json,sys,collections;d=json.load(sys.stdin);print("escape",dict(collections.Counter(r["verdict"] for r in d["results"])))')
# AttackRecallRegress
(cd .ufo/waves/round-23/w2/out/AttackRecallRegress && for c in cases1 cases2 cases-final; do python3 -I probe.py $c.json "$D/../rr-$c" "$D/../rr-$c.json" "$T" >/dev/null 2>&1; python3 -c 'import json,sys,collections;d=json.load(open(sys.argv[1]));r=d.get("results") or d.get("cases");print("recall",sys.argv[2],dict(collections.Counter(x["verdict"] for x in r)))' "$D/../rr-$c.json" $c; done)
