# R77ScribeEntryC1 — scoped scribe report

## Behavior and axes

Drafted the C1 knowledge entry `corpus/knowledge/bar-footprint-r77.md` per the seat spec, in the seat
directory only. Axes: coverage (C1 chain rows OBS/INF/UNK, each with a source row id + file:line),
provenance (trio `source: S457–S462` / `verified-at: 2026-11-04` / `recheck:` trigger), and no-harm
(no production byte touched, no host state changed, read-only probes only). Every number in the draft
carries a pointer: a pinned-source line (S457–S462 at efb5099 / 90b209a), a receipt line, or a capture
sha256. Nothing was re-measured: this seat cites the committed receipts and verifies citations against
the pinned read-only source trees.

## Artifacts and touched surfaces

- `.ufo/waves/round-77/w1/R77ScribeEntryC1/corpus/knowledge/bar-footprint-r77.md`: the seat-spec draft —
  provenance trio, ground statement, 11-link chain table (OBS/INF/UNK), host join 2026-11-04 with
  receipts, full tool contract (inputs, auto branches, reserved expectation, output-key exclusion,
  exit map, named limits), frozen-measurement citation, Sources section.
- `.ufo/waves/round-77/w1/R77ScribeEntryC1/pre-wave-evidence-r77.txt` and
  `control-baseline-r77.txt`: copies of the two receipts the draft cites (rule: cited receipts copied
  into the seat dir).
- `.ufo/waves/round-77/w1/R77ScribeEntryC1.md`: this report, at the validator-rendered path.
- Created then removed empty `/fast/scratch/hyaku/mado-r77/R77ScribeEntryC1/`; nothing was generated there.

The L1 owns integration. No committed corpus file, instrument, control set, registry, ledger, judge,
state file, fleet-root tracked file, `~/.config` path, or sibling directory was modified.

## Exact shell commands and observed outcomes

Only these shell commands ran; all returned normally:

```sh
sha256sum /usr/share/man/man5/waybar.5.gz
# 3972caaf1f025ed83b706cfe91f35d1c9e7c3ae87e5d37d881120d13a1044a42 — matches the S461 row
cd /fast/scratch/hyaku/mado-r77/l1-src && grep -n …   # line pins in Hyprland/Waybar pinned trees
# arrangeLayerArray 2587; both_horiz 2609/2612; "// Margin" 2634; box.round 2660;
# applyExclusive add/sub 2577/2580; passes 2691/2694; store 2696;
# HyprCtl reserved template 253, args 281-282, pixel size 278, levelNames 706-708,
#   layers entry fields 679-680;
# ReservedArea parent/child 19, apply 53, applyip 62;
# XML enum 86-90, set_exclusive_zone 152, margin sentence 196;
# bar.cpp namespace 232, size request 240, mode-exclusive 358/360, anchors 402-429
zcat /usr/share/man/man5/waybar.5.gz | grep -n -E "^(       )?(position|layer|…)…"   # no matches (roff escapes)
cd …/mado-shokunin && git log --oneline -4 -- corpus/knowledge/bar-footprint-r77.md
# 0fa69f41 2026-11-04 wave-found hardening …; 3e35d0a9 2026-11-04 C1 bar-footprint entry+index+frontier …
git status --short -- corpus/knowledge/bar-footprint-r77.md .ufo/waves/round-77
# only untracked: receipts/harm-watch-r77.txt, receipts/measurement-interim-r77.txt,
#   w1.ready, w1.ready.dispatched, w1/ — in-flight wave artifacts, not touched
git rev-parse --short HEAD    # c083db4f
ls -la .ufo/waves/round-77/fetch/ && sha256sum …/live-layers-r77.json …/live-monitors-r77.json
# 46eb2481… and e732af34… — both match the shas printed in receipts/pre-wave-evidence-r77.txt
cat .ufo/waves/round-77/fetch/sha256-r77.txt   # S457.bin 9af8a74e… … S462.bin 120eb913…
mkdir -p /fast/scratch/hyaku/mado-r77/R77ScribeEntryC1 …/w1/R77ScribeEntryC1/corpus/knowledge
cp receipts/{pre-wave-evidence-r77.txt,control-baseline-r77.txt} …/w1/R77ScribeEntryC1/
rmdir /fast/scratch/hyaku/mado-r77/R77ScribeEntryC1
```

Everything else was dedicated-tool reads: the round-77 declaration; both receipts; the S454–S463 range
of `corpus/SOURCES.md`; the committed `corpus/knowledge/bar-footprint-r77.md`; `tools/mado-barfoot.py`
(565 lines, all); `quality/counters/c1-r77-barfoot.py`; `Renderer.cpp:2525-2703`, `HyprCtl.cpp:245-293`
and `:640-708`, `ReservedArea.cpp:1-73`, the protocol XML ranges, `bar.cpp:170-250` and its anchor
grep; `fetch/live-*.json`, `fetch/S461.txt:55-196`, `fetch/sha256-r77.txt`;
`~/.config/waybar/config.jsonc`; the round-76 scribe findings precedent; `skill://godspeed`. Skills
read: godspeed. No tool installed or upgraded (none needed; `zcat`, `grep`, `git` already present).

## Gates and execution evidence

No counter, fixture, selftest, gate, verifier, mutation test or other runtime was invoked by this
seat; no git/jj mutation, package transaction, service restart, compositor write verb, socket,
screenshot, or `~/.config` write occurred. Host contact was the read-only `~/.config/waybar/config.jsonc`
file read plus source reads inside the pinned trees. This is a scribe handoff, not an independent
re-certification: the C1 scores cited below are the committed receipt's, at rev a83e9bee.

| Recorded evidence | Observed receipt result | Revision in receipt |
|---|---|---|
| `receipts/control-baseline-r77.txt` (`MADO_R77_BARFOOT` line) | cases=15 correct=15 mutants=5 killed=5 base_correct=8/15 tool_selftest=18/18 verdict=TARGET_MET | a83e9bee04bb65ab15204addde472a38c97eff73 |
| `receipts/pre-wave-evidence-r77.txt` (`MADO_BARFOOT_*` block) | host join CLEAN: box=MATCH reserved=EQ band=26 expected=26; gate selftest 460/460; census rc=0 | not printed (live run 2026-11-04T04:58) |
| `fetch/sha256-r77.txt` + `sha256sum` re-measure | S457–S462 and both live captures match the committed hashes | — |

## Findings and verbatim conflicts for canonical judgment

No severity grade assigned; provenance observations only.

1. The entry this seat was asked to draft already exists committed:
   `git log -- corpus/knowledge/bar-footprint-r77.md` shows `3e35d0a9` ("round-77: C1 bar-footprint
   entry+index+frontier, …") and `0fa69f41` ("round-77: wave-found hardening — refuse
   scaled/transformed monitors and dynamic cross sizes … entry limits name any-margin, static
   reserve, mode presets, level gap"), both dated 2026-11-04, present at tip `c083db4f`. The seat
   draft at `w1/R77ScribeEntryC1/corpus/knowledge/bar-footprint-r77.md` is the seat-spec rendering
   (trio + tagged 11-row chain + contract); the L1 decides which bytes integrate. The committed entry
   and the draft agree on every measured number (box 0,0,3440,26; band [0,26,0,0]; level 2; height 26;
   15/15, 5/5, 8/15, 18/18).
2. Committed entry §4 cites "`gls:src/layer-surface.c:264-288`" (gtk-layer-shell's auto zone) — a
   source outside the declared trio S457–S462 and absent from `corpus/SOURCES.md`; it is not
   verifiable from the pinned read-only trees. The NOT_MODELLED margin claim itself is licensed by
   the tool docstring ("gtk-layer-shell's auto exclusive zone composes margins in a way this tool does
   not model"), the declaration's named limits, and the compositor-side sources (S460 margin sentence
   :196; S457 `applyExclusive` add :2577). The seat draft drops the `gls:` pointer, keeps the claim,
   and tags the client-side composition UNK.
3. Committed entry §1 cites the manual at "lines 70/91/97/128/189 of the installed page"; the
   committed rendering `fetch/S461.txt` pins the key heads at layer :64, position :85 (text :91),
   height :93 (dynamic note :97), margin :124 (CSS note :128), exclusive :183 (default-true :186).
   The ":70" layer reference is off by six lines; harmless, noted verbatim.
4. Committed entry §4 bullet "Centring rounding" is licensed: the tool centres with floor division
   (`(mon_w - w) // 2`) while Hyprland centres in double and rounds the box (`Renderer.cpp:2612-2613`,
   `:2660`); the 1-px odd-delta gap is a true inference. The seat draft states it with those pins.
5. Assignment header lists freeze revisions e4717a1c / a83e9bee / 94b5afb1; the lane tip is now
   `c083db4f` with two later entry-touching commits (see finding 1) and untracked in-flight wave
   artifacts (`receipts/harm-watch-r77.txt`, `receipts/measurement-interim-r77.txt`, `w1.ready*`,
   `w1/`). This seat did not open the interim measurement receipt and claims nothing from it.

## Out of scope and known limits

No integration, no edit of the committed entry, no new measurement, no C2 work (sibling seat), no
fixture, no git/jj write anywhere. The draft's frozen-measurement section is a citation of
`control-baseline-r77.txt`, not a re-run. The gtk-layer-shell client composition stays UNK until a
pinned source lands in the ledger. The `wallpaper` level-0 no-contribution remark is INF (band equals
the bar's height exactly today); the zone's value and setter remain UNK by construction of the
replies (S458 entry fields carry no zone).

## Self-evaluation (not an execution gate)

| Axis | Score / 5 | Evidence and improvement |
|---|---|---|
| Accuracy | 5 | Every number re-pinned to S457–S462 file:line or a receipt line; capture and manual shas re-measured and matched; conflicts kept verbatim, not repaired. |
| Completeness | 5 | Trio, ground statement, 11 tagged chain rows, host join, full contract (inputs, auto branches, reserved rule, output exclusion, exit map, named limits), sources. |
| Clarity | 4 | One table per section; the chain table carries tag + pointer per row; a reader needs the SOURCES rows open for full sha provenance. |
| Actionability | 5 | Draft is integration-ready; findings 1–5 give the L1 exact decision points (integrate vs. keep committed entry; drop or pin the gls: pointer). |
| Conciseness | 4 | Draft ≈ 120 lines; the report repeats conflicts deliberately for a self-contained handoff. |

Overall 4.8/5. Highest-value next move is canonical disposition of the already-committed entry and the
unpinned `gls:` citation — both are judgment calls for the L1, not for this seat to fix silently.
