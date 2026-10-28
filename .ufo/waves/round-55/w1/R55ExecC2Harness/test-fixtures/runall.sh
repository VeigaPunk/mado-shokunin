S=/fast/scratch/hyaku/mado-r55/R55ExecC2Harness; D=$(cat $S/D.txt); H=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w1/R55ExecC2Harness/r55_ctl_c2.py
mkdir -p $S/work
t(){ name=$1; shift; echo "### $name"; (cd $S && python3 -I $H --repo $D --work $S/work "$@"; echo "rc=$?"); }
t "A standin, no hold-out at rev"  --rev 085784fe59be3087ef384aceb2b3b08306aad405
t "B standin, no hold-out at rev, --holdout external (own 8)" --rev 085784fe59be3087ef384aceb2b3b08306aad405 --holdout $S/holdout
t "C standin, hold-out at rev, commit matches" --rev dba80a22eda0d0304c0ef67585e15ecca7f24c93
t "D standin, hold-out at rev, frozen sha wrong" --rev 26aded2b05c6752fbf6f463fb01dc28ae3d67daa
t "E wrong tool (default delay 500)" --rev ca0fe34cddb754e2912aee3f9c5beb00252d1555
t "F lookup-table tool" --rev 5569c957c33e2a3aa72dd1c798e3b30eede99d72
t "G control empty.py prints x" --rev b107eed71146cbea8d932f523eb2ffc9b668cf47
t "H tool absent at rev" --rev 87394e51e9a0a7f0be45a9160ecfa271031e98ff
t "I symbolic rev (branch tip = H) via HEAD" --rev HEAD
t "J bad rev" --rev nonesuch
t "K tampered external holdout (one byte)" --rev 085784fe59be3087ef384aceb2b3b08306aad405 --holdout $S/holdout_tampered
echo "### L missing --work"; python3 -I $H --repo $D --rev HEAD; echo rc=$?
