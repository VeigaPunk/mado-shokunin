#!/bin/bash
# R56W3MutBwrapChannels -- probe with the HARNESS' EXACT argv and EXACT scrubbed env.
#   staged_run(bwrap): cmd = [bwrap, --unshare-all, --die-with-parent, --ro-bind /usr /usr,
#     --symlink usr/lib /lib, --symlink usr/lib64 /lib64, --symlink usr/bin /bin, --dev /dev,
#     --ro-bind <stage> <stage>, --ro-bind <program> <program>, --tmpfs /w, --chdir /w,
#     python, -I, program] + args, env=scrubbed_env(work)
#   run_program (no bwrap): cwd=<work>/cwd-N, env=scrubbed_env(work)
set -u
S=/fast/scratch/hyaku/mado-r56/R56W3MutBwrapChannels
R=$S/receipts
W=$S/jail-work
rm -rf "$W"; mkdir -p "$W/stage-1/F01/tree" "$W/cwd-1" "$W/c2-tool-XXX" "$W/c2-export-XXX/.ufo/waves/round-56/fixtures/c2/F01"
echo "x" > "$W/stage-1/F01/tree/hyprland.conf"
printf 'THE ANSWER KEY\n' > "$W/c2-export-XXX/.ufo/waves/round-56/fixtures/c2/F01/expected.out"
cp "$S/cheats/probe-jail.py" "$W/c2-tool-XXX/mado-watchplan.py"
SCRUB="PATH=/usr/local/bin:/usr/bin:/bin HOME=$W TMPDIR=$W LC_ALL=C.UTF-8 LANG=C.UTF-8"

echo "=== A) bwrap jail, harness argv + harness scrubbed env ==="
env -i $SCRUB bwrap --unshare-all --die-with-parent --ro-bind /usr /usr --symlink usr/lib /lib \
  --symlink usr/lib64 /lib64 --symlink usr/bin /bin --dev /dev \
  --ro-bind "$W/stage-1/F01" "$W/stage-1/F01" \
  --ro-bind "$W/c2-tool-XXX/mado-watchplan.py" "$W/c2-tool-XXX/mado-watchplan.py" \
  --tmpfs /w --chdir /w \
  /usr/bin/python3 -I "$W/c2-tool-XXX/mado-watchplan.py" \
    --config "$W/stage-1/F01/tree/hyprland.conf" --display-root "$W/stage-1/F01" \
  > "$R/jail-probe-bwrap.out" 2> "$R/jail-probe-bwrap.err"
echo "rc=$?"
sed -n '/=== ENV ===/,/=== CWD ===/p' "$R/jail-probe-bwrap.out"
sed -n '/=== ROOTS ===/,/=== WALK/p' "$R/jail-probe-bwrap.out"
echo "-- does the jail show the export or the answer key?"
grep -cE "c2-export|expected.out|THE ANSWER KEY" "$R/jail-probe-bwrap.out" || true
echo "-- cwd ancestors seen from inside the jail:"
sed -n '/=== CWD ANCESTORS ===/,/=== ARGV ===/p' "$R/jail-probe-bwrap.out" | head -12

echo
echo "=== B) no sandbox: cwd = <work>/cwd-1, harness scrubbed env ==="
( cd "$W/cwd-1" && env -i $SCRUB /usr/bin/python3 -I "$W/c2-tool-XXX/mado-watchplan.py" \
    --config "$W/stage-1/F01/tree/hyprland.conf" --display-root "$W/stage-1/F01" ) \
  > "$R/jail-probe-nosb.out" 2> "$R/jail-probe-nosb.err"
echo "rc=$?"
sed -n '/=== ENV ===/,/=== CWD ===/p' "$R/jail-probe-nosb.out"
echo "-- cwd ancestors seen with no sandbox:"
sed -n '/=== CWD ANCESTORS ===/,/=== ARGV ===/p' "$R/jail-probe-nosb.out" | head -12
echo "-- is the answer key reachable from the no-sandbox cwd?"
grep -oE "c2-export[^ ]*|expected.out|THE ANSWER KEY" "$R/jail-probe-nosb.out" | sort -u | head -10
