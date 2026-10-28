#!/bin/bash
# transcript driver: all scratch under /fast/scratch/hyaku/mado-r55/R55ExecC3Harness, removed at exit
D=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w1/R55ExecC3Harness
SC=/fast/scratch/hyaku/mado-r55/R55ExecC3Harness
trap 'rm -rf "$SC/S" "$SC/W"' EXIT
rm -rf "$SC/S" "$SC/W"; mkdir -p "$SC"
GOOD=$(python3 -I $D/mk_good_repo.py $SC/S) || exit 9
echo "synthetic good commit: $GOOD"
h() { python3 -I -c "import sys;sys.path.insert(0,'$D');import r55_ctl_c3 as m;sys.exit(m.run(sys.argv[1:]))" "$@"; }
for c in min_counter_c3.py stub_green.py stub_red.py stub_silent.py lazy_noprefix.py lazy_noreadme.py lazy_p23.py; do
  echo; echo "=== counter=$c"; h --repo $SC/S --rev $GOOD --work $SC/W --counter $D/$c 2>&1 | sed 's/rev=[0-9a-f]\{40\}/rev=<sha>/g'; echo "rc=${PIPESTATUS[0]}"
done
echo; echo "=== no --counter, counter absent at rev"; h --repo $SC/S --rev $GOOD --work $SC/W 2>&1 | tail -2; echo "rc=${PIPESTATUS[0]}"
echo; echo "=== committed-counter path: counter committed at rev"
python3 -I - <<PY
import subprocess,os
S="$SC/S"
def g(*a,inp=None): return subprocess.run(["git","-C",S]+list(a),input=inp,capture_output=True,check=True).stdout
g("read-tree","$GOOD"); h=g("hash-object","-w","--stdin",inp=open("$D/min_counter_c3.py","rb").read()).decode().strip()
g("update-index","--add","--cacheinfo","100644,%s,quality/counters/c3-r55-p19.py"%h); t=g("write-tree").decode().strip()
c=g("-c","user.name=ctl","-c","user.email=ctl@ctl","commit-tree",t,"-p","$GOOD","-m","with counter",inp=b"").decode().strip()
open("$SC/withcounter","w").write(c)
PY
h --repo $SC/S --rev $(cat $SC/withcounter) --work $SC/W 2>&1 | sed 's/rev=[0-9a-f]\{40\}/rev=<sha>/g'; echo "rc=${PIPESTATUS[0]}"
echo; echo "=== setup errors"
h --repo $SC/S --rev deadbeef --work $SC/W; echo "rc=$?"
h --repo $SC/S --work $SC/W; echo "rc=$?"
h --repo $SC/S --rev $GOOD --work $SC/W --bogus x; echo "rc=$?"
echo; echo "=== dispatcher via quality/check-r55-controls.py (lane copy has no r55_ctl_c3.py beside it; PYTHONPATH not used with -I)"
echo "leftover scratch dirs under W after runs:"; ls $SC/W
