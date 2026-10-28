set -eu
S=/fast/scratch/hyaku/mado-r55/R55ExecC2Harness
D=$(cat $S/D.txt); W=.ufo/waves/round-55
G="git -C $D -c user.name=ctl -c user.email=ctl@ctl"
[ "$(git -C $D rev-parse --show-toplevel)" = "$D" ]
C=$(cat $S/commit.txt)
python3 - "$D" "$C" <<'PY'
import json,sys
p=sys.argv[1]+"/.ufo/waves/round-55/frozen-tables.json"
d=json.load(open(p)); d["c2"]["holdout_commit_sha256"]=sys.argv[2]; json.dump(d,open(p,"w"),indent=1)
PY
$G add -A; $G commit -qm c1; echo "A_nohold=$($G rev-parse HEAD)"
cp -r $S/holdout $D/$W/fixtures/c2-holdout; $G add -A; $G commit -qm c2; echo "C_hold=$($G rev-parse HEAD)"
sed -i 's/"holdout_commit_sha256": "./"holdout_commit_sha256": "0/' $D/$W/frozen-tables.json; $G add -A; $G commit -qm c3; echo "D_badcommit=$($G rev-parse HEAD)"
git -C $D checkout -q HEAD~1 -- $W/frozen-tables.json
sed -i 's/DEF = {"repeat_rate": 25, "repeat_delay": 600/DEF = {"repeat_rate": 25, "repeat_delay": 500/' $D/tools/mado-kbdopts.py; $G add -A; $G commit -qm c4; echo "E_wrongtool=$($G rev-parse HEAD)"
cat > $D/tools/mado-kbdopts.py <<'PY'
import json,sys
from pathlib import Path
root=Path(".ufo/waves/round-55/fixtures/c2")
for d in sorted(root.iterdir()):
    if json.loads((d/"args.json").read_text())==sys.argv[1:]:
        sys.stdout.write((d/"expected.out").read_text()); sys.exit(int((d/"expected.rc").read_text()))
sys.stdout.write("MADO_KBDOPT: SETUP usage\n"); sys.exit(2)
PY
$G add -A; $G commit -qm c5; echo "F_lookuptool=$($G rev-parse HEAD)"
cp $S/standin.py $D/tools/mado-kbdopts.py
echo 'print("x")' >> $D/$W/ctl/empty.py; $G add -A; $G commit -qm c6; echo "G_badctl=$($G rev-parse HEAD)"
git -C $D checkout -q HEAD~1 -- $W/ctl/empty.py; $G rm -q -f tools/mado-kbdopts.py; $G add -A; $G commit -qm c7; echo "H_notool=$($G rev-parse HEAD)"
