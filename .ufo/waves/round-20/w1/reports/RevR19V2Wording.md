# RevR19V2Wording — append an explicit S096 tally correction

## Axes

- **Fidelity:** distinguish the closure-defined any-line and first-qualifying-line counts from the older RerunC2 evidence-attribution count.
- **Completeness:** carry the correction across every live round-19 summary that repeats or implies the stale tally.
- **Scope:** state that S096 is host-byte provenance, not a walker behavior re-measurement.

## Findings

### High — the live round-19 summaries repeat a stale 5/13 figure

- `SCORECARD.md:1167-1171` says “5/13 name S096 on the crediting line.”
- `corpus/lessons/round-19.md:108-109` says “5 of 13 credited files name S096 on the crediting line” and says the rest credit S090 or the README span.
- `LOG.md:1323-1325` repeats “5/13 name S096 on the crediting line.”

Those are not the closure’s current fixed-set any-line or first-line counts. The closure defines the denominator and qualifying line in `corpus/lessons/round-19-verifier-spotcheck.md:59-61`: the 13 baseline files containing `2.17.0` at `9c54c56`, and a qualifying line has `2.17.2` plus an `S###` token on that same line. At the reviewed tip, **8/13** files have S096 on any qualifying line; considering only each file’s first qualifying line gives **6/13**. Five have no S096 on any qualifying line and cite only S090:

- `corpus/knowledge/arc-synthesis.md:392`
- `corpus/knowledge/closeout-r11.md:299`
- `corpus/knowledge/config-health-report-r3.md:1009`
- `corpus/knowledge/waybar-walker-plane.md:479`
- `corpus/knowledge/waybar-walker-semantics.md:467`

The composition clause in `round-19.md:108-109` should therefore also be corrected: the five named files are S090-only; README and `walker-route-r18.md` have later qualifying S096 lines, despite their first qualifying lines citing the README’s S072–S091 span.

**Independent re-derivation:** I reproduced the registered fixed-set construction and same-line regex from `.ufo/waves/round-19/fresh-pins.py:7-17, 31-54` with read-only `git show` of the 13 files. Command: `python3 /tmp/revr19v2/s096.py` (script SHA-256 `46fc2b0a95e5ba051ff1eca5d5db43a5577da1542d3eebc7ae5af99cbfc8f7a9`). Output excerpt:

```text
== b435568: any-line 8/13, first-line 6/13
== 1f7f995: any-line 8/13, first-line 6/13
== e629f73: any-line 8/13, first-line 6/13
13-file set changed b435568->e629f73: NONE (identical)
```

The any-line S096 set is SKILL, `corpus/README.md`, `remaining-planes-census`, `walker-deep-r9`, `walker-deep`, `walker-live-surface`, `walker-route-r18`, and `tools/mado-verify.sh`. The two that distinguish 8 any-line from 6 first-line are README (`:44` first qualifying line; S096 at `:137-138`) and `walker-route-r18.md` (`:1` first qualifying line; S096 at `:328`).

**Why 5/13 appeared:** `round-19/w2/reports/RerunC2.md:71-73` describes a narrower “S096 cited as evidence” bucket at `01b8094`, not the closure’s any-line/first-line definition. My same-line recount at `01b8094` is 7/13 any-line and 6/13 first-line; excluding the two explicit S096-denial rows yields the report’s 5/13 evidence-attribution category. This historical report should not be rewritten as though it measured the later tip.

### Medium — SCORECARD’s C2 summary needs an explicit coverage bound

`SCORECARD.md:1133` calls C2 “sourced on S096,” then describes the 13/13 pointer result and says the claim is dated provenance, not re-measurement. Its final caveat is correct, but the summary does not say that S096 appears on qualifying lines in only 8/13 files, and can be read as extending S096 coverage to all 13. Add the 8/13 and 6/13 distinction and the five-file list in the append-only correction; do not erase the existing provenance-not-remeasurement caveat.

### No correction needed — the round-20 registration already names the discrepancy

`SCORECARD.md:1270-1271` already records “5/13 name S096” versus “8/13 any-line / 6/13 first-line” as a red example for criterion 30. It is not a current round-19 result statement and should remain as registered. The closure at `corpus/lessons/round-19-verifier-spotcheck.md:59-61` is the source of truth and must not be edited.

## Exact append-only correction draft

Use this block in the new round-20 corrections-to-round-19 section of `SCORECARD.md` and as the R19-V2 correction text in `corpus/lessons/round-20.md` (minor heading/anchor adaptation only):

> **R19-V2 — S096 pointer tally (append-only correction).** The round-19 “5/13 name S096 on the crediting line” statements (`SCORECARD.md:1167-1169`, `corpus/lessons/round-19.md:108-109`, `LOG.md:1323-1325`) carry forward the narrower “S096 cited as evidence” count in `.ufo/waves/round-19/w2/reports/RerunC2.md:71-73`, measured at `01b8094`; they are not the current any-line or first-qualifying-line S096 counts. In the fixed 13-file set defined by `.ufo/waves/round-19/fresh-pins.py` (files containing `2.17.0` at `9c54c56`; qualifying lines contain `2.17.2` and an `S###` token on the same line), **8/13** files have S096 on any qualifying line and **6/13** have S096 on their first qualifying line. The five files with no S096 on any qualifying line and an S090-only dated pointer are `corpus/knowledge/arc-synthesis.md:392`, `closeout-r11.md:299`, `corpus/knowledge/config-health-report-r3.md:1009`, `corpus/knowledge/waybar-walker-plane.md:479`, and `corpus/knowledge/waybar-walker-semantics.md:467`. Thus the pre-registered promise that every file cite the new host-byte row S096 remains unmet. The `fresh-pins.py` 13/13 result is a permissive pointer count, not 13/13 S096 citations. S096 establishes `/usr/bin/walker` **byte provenance**, not behavior: zero walker behavior facts were re-measured on 2.17.2; `walker --version`, the running process, and 2.17.2 behavior remain `[UNK]`.

**LOG carrier text:** add a concise correction under the new round-20 LOG entry, with a link to the SCORECARD block and round-20 lesson: “R19-V2 correction: S096 occurs on any qualifying line in 8/13 files, and on the first qualifying line in 6/13; five named files remain S090-only. The 13/13 `fresh-pins.py` result counts a permitted pointer row, not S096 coverage. S096 is host-byte provenance, not a 2.17.2 behavior re-measurement. See [SCORECARD round-20 correction] and `corpus/lessons/round-20.md`.”

## Required carriers and locations

Append-only; do not patch the historical statements in place:

1. `SCORECARD.md` — a new round-20 “corrections to round 19” section, explicitly covering the incomplete C2 summary at `:1133` and the stale count at `:1167-1171`.
2. `corpus/lessons/round-20.md` — the R19-V2 correction block, with the five S090-only paths and the provenance-not-behavior limit.
3. `LOG.md` — a round-20 entry carrying the concise correction above; retain the historical round-19 entry at `:1323-1325` unchanged.

The correction must identify all four round-19 statement locations: `SCORECARD.md:1133`, `SCORECARD.md:1167-1171`, `corpus/lessons/round-19.md:108-109`, and `LOG.md:1323-1325`. `SCORECARD.md:1270-1271` already records the 8/13 and 6/13 discrepancy; it is not a replacement for the correction block.

Do not rewrite dated wave-2 reports (including `RerunC2.md:71-73`) or the verifier closure. Those preserve the earlier snapshot and its stated classification; the round-20 correction should explain the difference instead.

## Evidence anchors

- `SCORECARD.md` lines 1133, 1167-1171, 1270-1271; SHA-256 `0139a1a403d4a0e431106e9d7fe70009daa86b7016e7dbbc81292d4593e62914`.
- `corpus/lessons/round-19.md` lines 108-109; SHA-256 `da9d8a87a2fe79bc9bf3614e3d29412b39abb4a5affa33a89a77dd6a7afbcdf6`.
- `LOG.md` lines 1323-1325; SHA-256 `27f6bb64e3ba816b31fba1fc35968b08916829c206cbccb5eb86a449cce56769`.
- `corpus/lessons/round-19-verifier-spotcheck.md` lines 59-61; SHA-256 `dcb7a9134022e010ef357a095ded13d15d6f77a9090dc2976f0c9d8090fea0a0`.
- `.ufo/waves/round-19/fresh-pins.py` lines 7-17, 31-54; SHA-256 `a094be019968ef2cff4bf643be5f5f2b62d24b957310a4c0620a0ea2c5bcd789`.
- Revisions resolved read-only: `e629f73` = `e629f731172b8238caffe50f152217ce56535fb4` (HEAD/pre-registration), `b435568` = `b435568540f9a28f4f7bb902af8dbe6a5b084dfe`, `1f7f995` = `1f7f995caa25627db804e996cccd87fe38a3a1b6`; 13-file set byte-identical between `b435568` and `e629f73`.

## Residual risk and verification gaps

- This is a wording/tally review only; no lane files other than this report were edited, and no tests or behavioral checks were run.
- No LSP device/server was available in the mounted tool routes; caller/definition/diagnostics checks were not applicable to these prose locations.
- No walker executable, process, host state, or behavior was probed. These remain `[UNK]`, consistent with the closure.

## Installs

None.
