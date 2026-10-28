set -eu
S=/fast/scratch/hyaku/mado-r55/R55ExecC2Harness
L=/home/vgpnk/Projects/shokunin/mado-shokunin
D=$(mktemp -d -p $S repo.XXXX)
git -C "$D" init -q
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ]
git -C $L archive 54dacbd843d64ba744cd3f1bdc2ec622e5010039 .ufo/waves/round-55/fixtures .ufo/waves/round-55/ctl .ufo/waves/round-55/fetch .ufo/waves/round-55/frozen-tables.json | tar -x -C "$D"
mkdir -p "$D/tools"; cp $S/standin.py "$D/tools/mado-kbdopts.py"
echo "$D" > $S/D.txt
# hold-out: 8 own fixtures in $S/holdout
rm -rf $S/holdout; mkdir -p $S/holdout
W=.ufo/waves/round-55/fixtures/c2-holdout
i=0
while IFS= read -r body; do
  i=$((i+1)); id=$(printf 'H%02d' $i); mkdir -p $S/holdout/$id
  printf "$body" > $S/holdout/$id/c1.conf
  printf '["--config", "%s/%s/c1.conf", "--keyboard", "kb1"]' $W $id > $S/holdout/$id/args.json
  mkdir -p "$D/$W/$id"; cp $S/holdout/$id/c1.conf "$D/$W/$id/"
  (cd "$D" && python3 -I tools/mado-kbdopts.py --config $W/$id/c1.conf --keyboard kb1 > $S/holdout/$id/expected.out; echo $? > $S/holdout/$id/expected.rc)
done <<'EOT'
device {\n name = kb1\n repeat_rate = 70\n}\n
input {\n  repeat_rate = on\r\n\trepeat_delay\t=\t 123\r\n}\n
device {\n repeat_rate = 5\n name = kb1\n}\n
input {\n numlock_by_default = yes please\n touchpad {\n  repeat_rate = 9\n }\n}\n
input {\n repeat_delay = 0x10\n repeat_rate = +5\n}\n
device {\n name = kb1 # c\n repeat_delay = 1\n}\ndevice {\n name = kb1\n numlock_by_default = 1\n}\n
input {\n repeat_rate = a\\\\b\n}\n
$x = 1\ninput {\n repeat_rate = 201\n}\n
EOT
(cd $S/holdout && find . -type f | sed 's|^\./||' | LC_ALL=C sort | while read f; do printf '%s\0%s\n' "$f" "$(sha256sum "$f" | cut -d' ' -f1)"; done | sha256sum | cut -d' ' -f1) > $S/commit.txt
echo $D; cat $S/commit.txt
