# Falsify23 fixture — rebuild instructions

The attack fixture is not committed to the lane. It is reproduced from the lane base plus the
receipt patch in this seat directory. All of it lives under scratch; nothing tracked is touched.

```sh
SCRATCH=/fast/scratch/hyaku/mado-r52/Falsify23
SEAT=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/w1/Falsify23
mkdir -p "$SCRATCH" && cd "$SCRATCH"
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/mado-shokunin fixture
cd fixture
git rev-parse --show-toplevel      # must print the fixture dir
git rev-parse HEAD                 # 85d57a818c3707397e21c840b6498b105ba798aa
mkdir -p .ufo/waves/round-52/fetch
cp .ufo/waves/round-51/fetch/Hyprland-KeybindManager.cpp \
   .ufo/waves/round-51/fetch/Hyprland-legacy-DispatcherTranslator.cpp \
   .ufo/waves/round-51/fetch/Hyprland-HyprCtl.cpp \
   .ufo/waves/round-51/fetch/Hyprland-ConfigActions.cpp \
   .ufo/waves/round-52/fetch/
git apply "$SEAT/receipts/fixture-corpus-delta.patch"
git add -A
git -c user.name=Falsify23 -c user.email=falsify23@local commit -q -m "fixture"
TMPDIR="$SCRATCH" python3 -I "$SEAT/probe-c2-r52.py" --repo fixture --rev HEAD --work work-green
TMPDIR="$SCRATCH" python3 -I "$SEAT/probe-c2-r52.py" --repo fixture \
   --rev 85d57a818c3707397e21c840b6498b105ba798aa --work work-base
TMPDIR="$SCRATCH" python3 -I "$SEAT/novelty-audit.py"
```

What the patch adds (all under `corpus/`, verified byte-identical on rebuild):

- `corpus/knowledge/hyprland-dispatcher-dispatch-r52.md` (also kept verbatim as
  `fixture-entry.md`): four propositions that restate the round-51 dispatcher entry's chain
  steps 3, 1, 8 and 5, with the same pins, the same line spans and the same quotes, plus a
  `## Propositions` map table and the pin manifest the grammar expects.
- `corpus/SOURCES.md`: four new rows S380-S383, `status=mined`, `opened 2026-10-27`, each bound
  to a `pins` path under `.ufo/waves/round-52/fetch/`.
- `corpus/README.md`: one index row for the new entry.

The four `round-52/fetch/` pins are byte copies of the round-51 pins (`receipts/fixture-pin-shas.txt`,
`receipts/fixture-pins-vs-r51-cmp.txt`).

`probe-c2-r52.py` is the committed `quality/counters/c2-r51-dispatch-entry.py` with the constants
retargeted (`ENTRY`, `ENTRY_NAME`, `FETCH_ROOT`, `BASE=85d57a81...`, `ROW_MIN/MAX=380..383`, print
prefix) and one added clause (e) that encodes the frozen proposition-count/mapping requirement the
round-51 counter did not have. Clauses (a)-(d) are otherwise the committed machinery unchanged.
