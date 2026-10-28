#!/usr/bin/env bash
# Reproduces the transcript. Scratch only; removes its scratch dir on exit.
set -u
D=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w1/R55ExecC1Harness
R=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55
S=/fast/scratch/hyaku/mado-r55/R55ExecC1Harness/run
rm -rf "$S"; mkdir -p "$S/work"; trap 'rm -rf "$S"' EXIT; cd "$S"
SYN=$S/synth; REV=$(python3 -I $D/tests/gen_synth.py $R $SYN); echo "synthetic good tree rev=$REV"
H="python3 -I $D/r55_ctl_c1.py"
t(){ local n=$1; shift; echo; echo "=== $n"; $H --repo "$SYN" --rev "$REV" --work "$S/work" "$@"; echo "rc=$?"; }
t "(a+b) synthetic good tree + minimal correct counter" --counter $D/tests/counter_ref.py
t "(c) always-green stub (must FAIL)" --counter $D/tests/stub_green.py
t "(d) always-red stub (must FAIL on good)" --counter $D/tests/stub_red.py
t "(e) noisy stub: correct counter plus one extra stdout line (must FAIL)" --counter $D/tests/stub_noisy.py
t "(f) silent stub (must FAIL)" --counter $D/tests/stub_silent.py
sed 's/missed.append("anchor:" + i); ok = False/pass/' $D/tests/counter_ref.py > $S/blind.py
t "(g) anchor-blind counter (must score 6/7 FAIL)" --counter $S/blind.py
mkdir -p $SYN/quality/counters && cp $D/tests/counter_ref.py $SYN/quality/counters/c1-r55-kbd-entry.py
git -C $SYN add -A && git -C $SYN -c user.name=ctl -c user.email=ctl@ctl commit -q -m counter
echo; echo "=== (h) default counter export at --rev (no --counter)"; $H --repo $SYN --rev HEAD --work $S/work; echo "rc=$?"
echo; echo "=== (i) setup errors"; $H --repo $SYN --rev nosuchrev --work $S/work 2>&1 | tail -1; echo "rc=${PIPESTATUS[0]}"
$H --repo $SYN --rev HEAD --work $S/work --counter /nonexistent 2>&1 | tail -1; echo "rc=${PIPESTATUS[0]}"
echo; echo "work leftovers: $(ls -A $S/work | wc -l)"
