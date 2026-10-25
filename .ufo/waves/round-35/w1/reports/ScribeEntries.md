# ScribeEntries — round 35 wave 1 report

Seat: ScribeEntries (scribe). Scope: draft the three adopted knowledge
entries' bodies in the lane's house style, to scratch only — no lane files
touched, no subagents dispatched (leaf member).

## Deliverable

`.ufo/waves/round-35/scratch/ScribeEntries/draft.md` (12,030 B) — three entry
bodies, in lane-registry id order:

| body | target path | cites |
|---|---|---|
| 1 | `corpus/knowledge/idle-lock-never-asked-r12.md` | S203, S204 |
| 2 | `corpus/knowledge/idle-lock-chain-armed-r14.md` | S205 |
| 3 | `corpus/knowledge/idle-lock-offered-in-the-bar-r15.md` | S206, S207, S208, S209, S210 |

## House style followed

Patterned on the lane's own `corpus/knowledge/waybar-module-text-route-r25.md`
(round-34 convention): a Lane/Round/substrates-read-only preamble, then
`source:` / `verified-at:` / `recheck:` frontmatter, then one
`gate-quote: Sxxx <quote>` line per cited row, then `**OBS**`/`**INF**`/`**UNK**`
paragraphs under `###` sections, ending with a "What this does not license"
section. OBS/INF/UNK are never mixed in one paragraph.

## Gate quotes — verified mechanically

Each quote is the receipt's own `located:` summary line, a verbatim contiguous
substring of the receipt bytes (same construction the golden control passes
with). Re-run:

```sh
python3 - <<'EOF'
import re
draft = open('.ufo/waves/round-35/scratch/ScribeEntries/draft.md').read()
for sid, q in re.findall(r'^gate-quote: (S\d+) (.+)$', draft, re.M):
    blob = open(f'.ufo/waves/round-35/fetch/{sid}.receipt.txt','rb').read()
    print(sid, len(q.split()), q.encode() in blob)
EOF
```

Actual output at write time: all 8 ids print `contiguous=True`, word counts
13–17 (bound is 1–25). Eight quotes for eight rows — matches the C1 target's
closed_rows=8 shape.

## What each entry does not license (stated in the bodies)

- **never-asked**: licenses the setup path only — expressly does NOT claim the
  desktop never offers the choice anywhere (the r15 entry corrects that
  over-read); the operator's preference stays UNK.
- **chain-armed**: armed ≠ observed firing — the 150/152 s figures are
  config-declared, no transition was waited out; armed state is a point
  sample, not a standing guarantee (stateless toggle, must be re-probed);
  preference UNK. The unit/probe disagreement is explained by the `uwsm-app`
  launch path recorded in this lane's own plane note — grounded in the lane's
  corpus, not in the receipt alone.
- **offered-in-the-bar**: the rendered module's current display is unverified
  (no RTMIN+9, no screenshot); "never taken" is NOT licensed — a bar click
  leaves no flag and the toggle is stateless, so past use cannot be excluded;
  preference UNK.

## Provenance note

Each body names the merge package's ids for the same documents (S309, S310,
S321, S329, S330, S331, S334, S336) in its preamble so the campaign can
reconcile the id remap (L0 ae2c52b8); the cited rows are the lane's own
S203–S210 per the registration's re-point-by-document rule.

## Divergence recorded in-body

The package's r15 document dates the oldest waybar backup 2026-10-06; the
S209 receipt's own sweep measures the oldest at 2026-10-03 17:44:32
(`.1791314470`). The body records the lane's measured figure and names the
disagreement, matching the golden control's treatment.

## Bounds kept

Scratch write only under `.ufo/waves/round-35/scratch/`; no `corpus/` touch,
no jj/git action, no sibling-seat files, `/home/vgpnk/Projects/shokuknow`
read-only throughout.
