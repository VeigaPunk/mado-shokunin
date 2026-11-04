# R81ScoutModel — findings ledger

Seat: source recon on the six new frozen C1 cases (read-only, no code edit, no instrument edit).
Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`; scratch: `/fast/scratch/hyaku/mado-r81/R81ScoutModel`
(removed after the receipt copy). Report: `.ufo/waves/round-81/w1/R81ScoutModel.md`.
Tool installs: none needed; no pacman transaction was run (host guard: all pacman paused anyway).

## Files read (read tool, path:range)

```
read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-81/fetch/S478.bin:40-75
read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-81/fetch/S478.bin:49-66:raw
read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-81/controls/c1-cases-r81.json
read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-81/controls/c1-cases-r81.json?q=.cases[]|{name,expect}
read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-81/controls/c1-cases-r81.json?q=.cases[]|select(.name|test("overflow-tie-negative|^auto-"))
read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-79/fetch/S464.bin:255-300
read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-79/fetch/S464.bin:178-200:raw
read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-79/fetch/S464.bin:294-330:raw
read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-79/fetch/S464.bin:338-360:raw
read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-80/fetch/S470.bin:2540-2580
read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-80/fetch/S470.bin:2600-2710
read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-80/fetch/S470.bin:2529-2600:raw
read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-81/receipts/measurement-c1-r81.txt
read /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-barfoot.py:100-200
read /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-barfoot.py:240-470
read /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-barfoot.py:470-640
read /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-barfoot.py:640-870
read /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-barfoot.py:900-1012
read /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-barfoot.py:1430-1483
read /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r81-overflow-auto.py:1-90
read /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r81-overflow-auto.py:94-300
```

## Commands run (exact shell argv)

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin && mkdir -p .ufo/waves/round-81/w1/R81ScoutModel /fast/scratch/hyaku/mado-r81/R81ScoutModel && ls .ufo/waves/round-81/w1/ && echo "--- seat dir ---" && ls -la .ufo/waves/round-81/w1/R81ScoutModel/
cd /home/vgpnk/Projects/shokunin/mado-shokunin && wc -l tools/mado-barfoot.py quality/counters/c1-r81-overflow-auto.py && sha256sum tools/mado-barfoot.py quality/counters/c1-r81-overflow-auto.py .ufo/waves/round-81/controls/c1-cases-r81.json | cut -c1-16,65-200
cd /home/vgpnk/Projects/shokunin/mado-shokunin && grep -n "DECL\|RESULT\|argparse\|add_argument\|def main\|def cmd_\|SELFTEST\|selftest" tools/mado-barfoot.py | cut -c1-200
cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -c "import json; d=json.load(open('.ufo/waves/round-81/controls/c1-cases-r81.json')); [print(c['name'], i, json.dumps(s,sort_keys=True)) for c in d['cases'] for i,s in enumerate(c.get('surfaces') or [])]"
cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -c "import json; d=json.load(open('.ufo/waves/round-81/controls/c1-cases-r81.json')); [ (print('==',n), print(' config',json.dumps([x for x in d['cases'] if x['name']==n][0]['config'],sort_keys=True)), print(' surfaces',json.dumps([x for x in d['cases'] if x['name']==n][0].get('surfaces'))), print(' layers',json.dumps([x for x in d['cases'] if x['name']==n][0]['layers'])) ) for n in ['overlay-unexclusive-full','full-box-vs-usable','top-margin-asym','same-level-order']]"
cd /home/vgpnk/Projects/shokunin/mado-shokunin && grep -n "exclusive_zone\|auto_exclusive_zone" .ufo/waves/round-79/fetch/S464.bin | cut -c1-160; echo ---; grep -n "POSITION_ANCHORS\|EDGE_RULES\|^LEVEL\|^ANCHOR\|RESERVED_INDEX\|OPPOSITE_EDGE" tools/mado-barfoot.py | cut -c1-160
cd /home/vgpnk/Projects/shokunin/mado-shokunin && grep -n "if (exclusive <= 0)\|static void applyExclusive\|box.x = bounds.x + ((bounds.width / 2)\|box.width <= 0 || box.height <= 0\|box.round();\|applyExclusive(\*usableArea\|exclusive + edges\[i\].margin > 0\|positive_axis += exclusive" .ufo/waves/round-80/fetch/S470.bin | cut -c1-140; echo ---; grep -n "std::round\|newW\|box.round" .ufo/waves/round-81/fetch/S478.bin | cut -c1-120
cd /home/vgpnk/Projects/shokunin/mado-shokunin && sed -n '2604,2624p' .ufo/waves/round-80/fetch/S470.bin | cat -n; echo ---; sed -n '2655,2665p' .ufo/waves/round-80/fetch/S470.bin | cat -n
cd /home/vgpnk/Projects/shokunin/mado-shokunin && grep -n "arrangeLayersForMonitor(const\|stable_sort\|arrangeLayerArray(PMONITOR, la\|m_reservedArea.addType(Desktop::RESERVED_DYNAMIC" .ufo/waves/round-80/fetch/S470.bin | cut -c1-150
cd /home/vgpnk/Projects/shokunin/mado-shokunin && sed -n '1,55p' .ufo/waves/round-79/fetch/S459.bin | cat -n
cd /home/vgpnk/Projects/shokunin/mado-shokunin && grep -rln "CReservedArea::CReservedArea\|RESERVED_DYNAMIC_TYPE" .ufo/waves/*/fetch/ 2>/dev/null | head; echo ---; ls .ufo/waves/round-81/fetch/ | head -30
cd /home/vgpnk/Projects/shokunin/mado-shokunin && grep -rln "m_reservedArea" .ufo/waves/*/fetch/*.bin | head; echo ---; for f in $(grep -rln "m_reservedArea" .ufo/waves/*/fetch/*.bin | head -3); do echo "## $f"; grep -n "m_reservedArea" "$f" | cut -c1-190 | head -8; done
cd /fast/scratch/hyaku/mado-r81/R81ScoutModel && python3 run.py 2>&1 | tee out.txt | cat
cd /home/vgpnk/Projects/shokunin/mado-shokunin && cp /fast/scratch/hyaku/mado-r81/R81ScoutModel/out.txt .ufo/waves/round-81/w1/R81ScoutModel/run-output.txt && wc -l .ufo/waves/round-81/w1/R81ScoutModel/run-output.txt && sha256sum .ufo/waves/round-81/w1/R81ScoutModel/run-output.txt | cut -c1-16
```

Replay argv (the driver's template; identical for every case, only the case directory changes):

```
/usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-barfoot.py \
  --config /fast/scratch/hyaku/mado-r81/R81ScoutModel/case-<name>/config.json \
  --layers /fast/scratch/hyaku/mado-r81/R81ScoutModel/case-<name>/layers.json \
  --monitors /fast/scratch/hyaku/mado-r81/R81ScoutModel/case-<name>/monitors.json \
  [--surfaces /fast/scratch/hyaku/mado-r81/R81ScoutModel/case-<name>/surfaces.json]
```

## Lines that matter

Instrument hashes (frozen, unchanged by this seat):

```
a129a435572805c3  tools/mado-barfoot.py
224051330291fdf4  quality/counters/c1-r81-overflow-auto.py
ab8154a1d4bc5d2a  .ufo/waves/round-81/controls/c1-cases-r81.json
```

Frozen measurement receipt (unchanged):

```
MADO_R81_BARFOOT: cases=39 correct=39 mutants=28 killed=28 base_correct=33/39 carried=33/33 tool_selftest=121/121 verdict=TARGET_MET rev=0e2ccd2a8692825cac534f57246053b276be9f13 tool_sha256=a129a435572805c3ae7730714f0dafdea2b9a7e420f53f0d109dc2d5f57d1230
```

Six new cases, literal RESULT (full stdout kept in `R81ScoutModel/run-output.txt`):

```
overflow-tie-negative      MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=26 expected=26 attributed=26 gt=0,26,0,0 attr=0,26,0,0 ls=VALID verdict=CLEAN
auto-dynamic-band-refused  MADO_BARFOOT: ERROR (stage=model auto zone on a dynamic height (0) is the client's allocation, not a declared value)   rc=3
auto-corner-edge           MADO_BARFOOT_DECL: monitor=M1 level=3 ns=panel box=0,26,200,100 anchor=top+left zone=0
auto-all-four-edge         MADO_BARFOOT_DECL: monitor=M1 level=3 ns=panel box=400,363,200,100 anchor=top+bottom+left+right zone=0
auto-parallel-edge         MADO_BARFOOT_DECL: monitor=M1 level=3 ns=panel box=400,363,200,100 anchor=top+bottom zone=0
auto-left-dock             MADO_BARFOOT_ATTR: monitor=M1 level=1 ns=dock edge=left contribution=40 box=0,0,40,800
auto-left-dock             MADO_BARFOOT_RESULT: monitor=M1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=26 expected=26 attributed=26 gt=0,26,0,0 attr=40,26,0,0 ls=VALID verdict=CLEAN
```

Source quotes used for the arithmetic:

```
S478:52-54,59-60  double roundedX = std::round(x); ... double newW = x + w - roundedX; ... w = std::round(newW);
S470:2613         box.x = bounds.x + ((bounds.width / 2) - (box.width / 2));
S470:2655         if (box.width <= 0 || box.height <= 0) {
S470:2660         box.round(); // fix rounding errors
S470:2531         if (exclusive <= 0) {
S470:2575         if ((exclusiveEdge == edges[i].singular_anchor || anchor == edges[i].singular_anchor || anchor == edges[i].anchor_triplet) && exclusive + edges[i].margin > 0) {
S470:2577         *edges[i].positive_axis += exclusive + edges[i].margin;
S470:2691/2694    arrangeLayerArray(PMONITOR, la, true, &usableArea); / arrangeLayerArray(PMONITOR, la, false, &usableArea);
S470:2696         PMONITOR->m_reservedArea.addType(Desktop::RESERVED_DYNAMIC_TYPE_LS, Desktop::CReservedArea{ORIGINAL_USABLE_AREA, usableArea});
S459:33-34        m_initialTopLeft = child.pos() - parent.pos(); m_initialBottomRight = (parent.pos() + parent.size()) - (child.pos() + child.size());
S464:270-273      gboolean horiz = (anchors[LEFT] == anchors[RIGHT]); gboolean vert = (anchors[TOP] == anchors[BOTTOM]);
S464:276          new_exclusive_zone = self->current_allocation.height;
S464:282          new_exclusive_zone = self->current_allocation.width;
S464:289          if (new_exclusive_zone >= 0 && self->exclusive_zone != new_exclusive_zone) {
S464:195          zwlr_layer_surface_v1_set_exclusive_zone (self->layer_surface, self->exclusive_zone);
S464:348          self->exclusive_zone = 0;
```

The one contradiction (report §3): `auto-left-dock`'s monitor reply is `reserved [0,26,0,0]` while
`S470:2696` + `S459:33-34` make the monitor's reserved area `[40,26,0,0]` for its own layers reply
(bar at `x=40`); the counter only compares the bar's top band, so the inconsistency is not asserted.

Probes (four classes, exact lines):

```
P1 probe-auto-left-margins    zone=45 then left contribution=48, bar box=48,0,952,26            right
P2 probe-triplet-preempts-edge top triplet preempts exclusiveEdge=left, contribution=30          right
P3 probe-edge-fallthrough     top guard 12-12=0 -> fall through to left, contribution=17          right
P4 probe-width-axis-skip      SKIP box=600,363,-200,100 reason=empty, boxes=MATCH,SKIP            right
```

## Scratch hygiene

Receipt copied to `.ufo/waves/round-81/w1/R81ScoutModel/run-output.txt` (107 lines, sha256
`3d181aa69f765868…`) before the scratch dir was removed. No path outside the seat dir, the scratch
dir and the two named lane paths was written; no git/jj mutation was run.

STATUS: ok
