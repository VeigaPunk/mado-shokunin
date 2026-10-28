# R55W2CritAdmission — admission audit, round 55 (C1, C2, C3) at 57584ed67716340b3d466fa04333ac0bab3fb79e

Seat: R55W2CritAdmission (leaf, no subagents). Scope: compare (a) the frozen v1 predicate sentence in
`.ufo/waves/round-55/claims-frozen.md` / `registration.md`, (b) the v2 errata in `registration-v2.md` +
`frozen-tables-v2.json`, (c) the instrument output at the scored rev, and the do-nothing controls, then say whether each
claim passes AXES.md admission ("every claim verifies and no axis is harmed"). Receipts: `receipts/`, attack inputs:
`attacks/`. Everything was run with `python3 -I` / `bash`, `TMPDIR` or `--work` under
`/fast/scratch/hyaku/mado-r55/R55W2CritAdmission/`. The lane was never written; attack copies are scratch clones
(`git clone` of the lane, `git checkout --detach 57584ed6` in the clone, one committed mutation per clone; toplevel asserted
before every commit). Tools installed: none.

## 1. Verdict table

Verdict key: SURVIVES = measured and matches the claim as written; BROKEN = a concrete input or a text check shows the
claim, the predicate or the entry is wrong or over-stated; NOT-REPRODUCED = an attack that did not reproduce;
UNVERIFIED = not checked by this seat.

| # | Target | (a) frozen v1 sentence | (b) v2 change | (c) measured at 57584ed6 | Measured line IS the frozen sentence? | Verdict | Evidence |
|---|---|---|---|---|---|---|---|
| A1 | C1 counter line | `MADO_KBD_ENTRY: rev=<rev> rows=18/18 hosts=6/6 sources=<n>/<n> new_rows=<m>/3 verdict=TARGET_MET missed=none`, exit 0 | E4 defines `sources=<c>/<d>` (c = K rows whose source leg holds; d = 18). v1 left it undefined | `rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET missed=none`, rc 0 | Yes: same grammar, same fixed values; `sources` now has a definition | SURVIVES (mechanical) | `receipts/claims-at-rev.txt` |
| A2 | C1 harness (controls) | `MADO_R55_CONTROLS: claim=c1 good=ok controls=7/7 verdict=OK`, exit 0 | E3 (host row evaluated independently of quote), E6 (C1-CTL-7 required leg `pin_hash`, embedded sha is v2's), E9 (scrubbed env, `python3 -I`) | 7/7 controls ok, `good: ok`, final line identical, rc 0 | Yes for the summary line; the harness also prints one `C1-CTL-n` line per control before it (format addition, not a change of verdict) | SURVIVES | `receipts/claims-at-rev.txt` |
| A3 | C1 claim content: "the entry settles these K/H propositions" | Not checked by any frozen leg: the counter proves quote identity, row, source and host binding only (declared in claims-frozen "Declared limit"; registration-v2 "Unchanged and still declared limits") | none | Attack k1: one K01 proposition replaced by placeholder prose (≥40 chars), K01 pin/line/quote untouched → `rows=18/18 hosts=6/6 sources=18/18 new_rows=3/3 verdict=TARGET_MET missed=none` | n/a | BROKEN as a content verifier (predicate admits a proposition that asserts nothing). Content is UNVERIFIED by the predicate and rests on the w2 sentence audit | `receipts/attacks.txt`, `attacks/mutations.py` |
| A4 | C1 entry row K16 (the row v2 changed) | v1 K16 quote `if ((!VAL \|\| !VAL->m_bSetByUser) && !fallback.empty())` (contains `\|`, unparseable under the cell rule) | E1: quote is now the pipe-free `!VAL->m_bSetByUser) && !fallback.empty())`; proposition unchanged | Pin line 1119 is `    if ((!VAL \|\| !VAL->m_bSetByUser) && !fallback.empty())`. K16 proposition still says "tests whether the device value pointer is **absent or not set by the user**". The quoted fragment carries only the "not set by the user" half; the `!VAL` absence test is no longer quoted | — | v2 narrowed the quote to pass the cell rule while the proposition still claims the absence half. Entry defect the counter cannot see | BROKEN (entry-level over-claim; claim-relevant) | `receipts/k16-quote-vs-proposition.txt` |
| A5 | C1 registry anchors for K14 and K17 | Not checked: `source_cell` checks URL suffix, commit/rev token and status only | none | S318 records `ConfigValues.cpp:271-279` but K14 is at `:280`. S052 records `wl_keyboard :2573-2699` but K17 is at `:2741` (and E04/E05 at `:2732`/`:2740`). The entry's Limits section says so itself | — | BROKEN-in-registry (sourced-claim duty §2b item 4 not met for K14, K17); the counter does not and cannot see it; declared in the entry | `SOURCES.md` rows S318, S052 at rev; entry "Registry anchor gaps" |
| A6 | C1 version word "Hyprland 0.56.2" (entry title) | Not a predicate leg; the pin is `efb50993…` | none | `hyprctl version` (read verb): "Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean" — matches the pin commit | — | SURVIVES (host read; not part of the predicate) | `receipts/host-tool-run.txt` and transcript below |
| A7 | C1 K-row provenance and new rows | `new_rows=<m>/3` with S378–S380 | E2 per-pin revision rule (Hyprland-* commit token; wayland pin needs `1.26.0/protocol/wayland.xml`) | `new_rows=3/3`; `source_cell` leg holds for 18/18 | — | SURVIVES (mechanical); the v2 rule admits S052 for K17 by a family-specific suffix rule — a widening limited to one pin family, K17 cites that spec, so the widening is correct for that row | `receipts/claims-at-rev.txt`, v2 `rev_rule` |
| B1 | C2 counter/harness line | `MADO_R55_C2: rev=<rev> fixtures=18/18 holdout=8/8 holdout_commit=ok controls=3/3 verdict=TARGET_MET`, exit 0 | E7: KEY definition for empty stack; numlock 0..1 declared a lane rule; harness private dir; commitment formula spelled out. Frozen constants unchanged | `fixtures=18/18 holdout=8/8 holdout_commit=ok controls=3/3 verdict=TARGET_MET`, rc 0. Controls: `const-host` 1 of 26, `empty` 0, `lookup-committed` 18 committed / 0 hold-out | Yes, identical grammar and values | SURVIVES | `receipts/claims-at-rev.txt` |
| B2 | C2 hold-out integrity | `holdout_commit_sha256` fixed at the freeze (`54dacbd8`) before dispatch | v2 keeps the same commitment | v1 and v2 tables both carry `1275d7f8…c549`; `frozen-tables.json` blob at `54dacbd8` = blob at rev (`d5a8aa79…`); v1 file sha `bf46c889…` unchanged | — | SURVIVES: the hold-out was not re-sealed. Residual: the hold-out is now public and the four candidates tied 8/8, so it no longer discriminates future tools (see §3) | `receipts/v1-v2-tables-and-freeze.txt` |
| B3 | C2 surface claim "runnable on this host, against the real input.conf" | Surface text only; the predicate runs committed copies (F02 reads `fetch/host-input.conf`) | none | Read-only spot check: `python3 -I tools/mado-kbdopts.py --config ~/.config/hypr/input.conf --getoption <scratch>/getoption.jsonl` → `keyboard=* repeat_rate=40 repeat_delay=250 numlock=1 from=G/G/G unsupported=0`, three `AGREE`, `DONE keyboards=1 unsupported=0 live=AGREE`, rc 0. `cmp` of `~/.config/hypr/input.conf` with the committed pin: equal | — | SURVIVES as a spot check (not a predicate leg). The per-keyboard branch was not observed (no `device` block; `getoption` takes no device) | `receipts/host-tool-run.txt` |
| B4 | C2 numlock range provenance | v1 §C2 listed the numlock range `0..1` under "Range (ConfigValues.cpp:277-280 pin)" | E7: ConfigValues.cpp:277 is a Bool without min/max; 0..1 is the lane's modelling rule | — | v1's source attribution was false; v2 corrects it. Behaviour unchanged (a numlock value 2 is `unsupported` by lane rule, not by source) | v2 corrects a false source claim (narrowing of provenance, not of behaviour) | `registration-v2.md` E7; C1 entry "numlock 0..1 range is the lane's modelling rule" |
| C1' | C3 counter line | `MADO_P19_FIX: rev=<rev> prefix=identical rows=13/13 pin=ok p23=ok readme=ok verdict=TARGET_MET missed=none`, exit 0 | E8: adds `rows:heading` and `stale` legs (stricter). Frozen Q table and P23 anchor unchanged (table diff shows no c3 change) | `prefix=identical rows=13/13 pin=ok p23=ok readme=ok verdict=TARGET_MET missed=none`, rc 0 | Yes. The printed legs are the frozen legs plus the two declared additions (`missed=` names them only when they fail) | SURVIVES (mechanical) | `receipts/claims-at-rev.txt` |
| C2' | C3 harness line | `MADO_R55_CONTROLS: claim=c3 good=ok controls=6/6 verdict=OK`, exit 0 | E8: C3-CTL-1 requires `rows:` + `p23`; C3-CTL-5 changed (see C3''), control count stays 6 | `good: ok`, six controls pass, final line identical, rc 0 | Yes for the summary line; the harness prints one line per control first | SURVIVES | `receipts/claims-at-rev.txt` |
| C3'' | C3-CTL-5 (control changed in v2) | v1: "old-wording (the P23 cell reduced to the P19 sentence) → `p23`" | E8: P23 cell := P19 sentence + ` == 0 RELEASED otherwise`, required leg `stale` | Harness: `C3-CTL-5 old-wording-stuffed: pass ... stale`. The v1-shaped control (P23 cell := P19 sentence verbatim) on the counter: `p23=bad`, `missed=p23,stale`, TARGET_MISSED | — | v2 changed the control's mutation and its required leg. The v1-shaped control still fails the counter (`p23`), so the v1 detection still holds; v2 adds a stricter stale check. No widening found | SURVIVES (stricter) | `receipts/attacks.txt` (c5), `receipts/claims-at-rev.txt` |
| C3''' | C3 P23 content vs pin | Lexical: `p23` = tokens present (`m_passPressed`, `== 1`, `== 0`, `PRESSED`, `RELEASED`) and one of `otherwise`/`any other`/`else` (declared "lexical, presence-only") | E8 adds `stale` (no `only when`, no verbatim P19 sentence) | Manual check of the committed P23 text against pin `Hyprland-ConfigActions.cpp:1554-1576`: `== 1` → non-mouse keyboard PRESSED, mouse pointer PRESSED (1556-1560); `== 0` → keyboard RELEASED, pointer RELEASED (1561-1565); else → keyboard PRESSED then RELEASED, pointer PRESSED then RELEASED (1566-1572); `sendKeyboardMods(0,0,0,0)` at 1576 clears. The committed P23 text matches | — | The P23 sentence itself is correct (SURVIVES, manual). The predicate does not verify it: flipping the `== 0` arm to PRESSED (contradicting Q06 `…STATE_RELEASED` at 1563 in the same block) → `p23=ok … verdict=TARGET_MET`; token salad `m_passPressed == 1 \`== 0\` PRESSED RELEASED otherwise` → `TARGET_MET`. BROKEN as a verifier | `receipts/attacks.txt`, `receipts/attack-tokensalad-p23.txt` |
| H1 | Harm: `bash tools/mado-verify.sh --selftest` | 460/460 (baseline `receipts/before.txt`) | none | `MADO_SELFTEST: 460/460 assertions passed`, rc 0 (export of rev; `TMPDIR` scratch) | — | SURVIVES | `receipts/harm-watch.txt` |
| H2 | Harm: navigation index | 69/69 → 70/70, never fewer | none | `MADO_INDEX: rev=57584ed6… indexed=70/70 missing=0 dangling=0 duplicates=0 coverage=10.0000/10`, rc 0 (base 3b55b6e9 gives 69/69) | — | SURVIVES | `receipts/harm-watch.txt` |
| H3 | Harm: census | `scripts/sources-census.sh validate --root … mado` exit 0 | none | rc 0; E-lines 0; 26 W04 warnings (duplicate-URL across scopes; includes S380 `IKeyboard.hpp`, a warning only) and one W01 (S277, pre-existing) | — | SURVIVES | `receipts/harm-watch.txt` |
| F1 | Freeze files (claims-frozen.md, registration.md, frozen-tables.json, fixtures/c2, ctl, fetch, freeze-verify.py) | byte-identical from freeze commit `54dacbd8` (18:46:52) | v2 is a new file (`5a43d67f`, 20:11:17), committed before the real entry (`ebd66fbf`, 20:16:27) and before any counter | Blob ids at rev equal blob ids at `54dacbd8` for all seven paths | — | SURVIVES | `receipts/v1-v2-tables-and-freeze.txt` |
| F2 | Frozen-table diff v1 → v2 | Only the frozen tables may differ, and only as v2 lists | E1 (K16 quote) and E2 (`rev_rule`) | `diff` of sorted JSON: exactly the K16 quote line (139), the added `rev_rule` block (174-177), `schema` and `supersedes` (392-404). No other c1, c2 or c3 value changes | — | SURVIVES (no unlisted table change) | `receipts/v1-v2-tables-and-freeze.txt` |

## 2. Admission verdict per claim (AXES.md: "every claim verifies and no axis is harmed")

| Claim | Verifies by its frozen predicate? | Harm | Admission reading |
|---|---|---|---|
| C1 (keyboard repeat/numlock entry) | Yes: counter line A1 and harness A2 match the frozen sentences at rev | None (H1–H3) | Admissible as a mechanical quote-binding claim. Not admissible as a content claim until the K16 row is corrected (A4) and the K14/K17 registry anchors are fixed or declared (A5); the proposition truth rests on the w2 sentence audit (A3) |
| C2 (`tools/mado-kbdopts.py`) | Yes: B1, hold-out commitment intact (B2) | None | Admissible. Host spot check agrees (B3). Hold-out now public (residual R5) |
| C3 (P23 correction) | Yes: C1' and C2' match the frozen sentences; C3-CTL-5 change is stricter (C3'') | None | Admissible on the frozen predicate. The P23 text is correct against the pin (C3'''), but the predicate would also pass a falsified P23 (A-level attack, §1) — the claim is verified as presence, not as truth |

Overall: all three frozen predicates produce the frozen lines at `57584ed6`, all controls pass, the harm watch is clean, and
the v1→v2 change set is exactly what registration-v2 lists, with no unlisted table change. Under the literal AXES rule the
round is admissible on the mechanical reading. The operator should rule on whether a predicate that admits a placeholder
proposition (A3) or a falsified branch (C3''') is "verified" for admission; this seat reports that it is not verified in content.

## 3. Residual risks (exact)

- R1 (C1, A3): the counter admits a K-row whose proposition asserts nothing. Reproduced: `attacks/mutations.py` k1 clone,
  commit `bb09bc2389f89e796c88eb6e7eed42ba992c29fe`, K01 proposition replaced; counter output in `receipts/attacks.txt`:
  `verdict=TARGET_MET missed=none`. Wave-1 `R55CritDoNothing` found the same with a full junk entry (independent confirmation).
- R2 (C3, C3'''): the `p23` leg is lexical. Reproduced twice: `== 0` arm flipped to PRESSED (clone `p23`, commit
  `173395911a27be2e087b19764dd9671f1b7ab212`) and token salad P23 (commit `28ff7cabb214b6259793ff816be2382890695ce5`), both
  `TARGET_MET`. Wave-1 `R55RevC3` (J2) found the same. The attacked P23 contradicts Q06 in the same block; no leg compares
  P23 to the Q rows.
- R3 (C1, A4): K16 proposition claims an absence test that the v2 quote does not contain. Not caught by any leg.
- R4 (C1, A5): K14 (S318 anchor ends `:279`, line `:280`) and K17 (S052 anchor ends `:2699`, line `:2741`) cite registry rows
  whose recorded anchors do not reach the cited line. The counter checks only URL suffix, commit/rev token and status. The
  entry declares this in its Limits.
- R5 (C2, B2): the hold-out (`fixtures/c2-holdout`) is revealed and committed in the lane. Future tools can be tuned against it;
  all four wave-1 candidates scored 8/8, so the hold-out did not discriminate among them. The lookup-table control is the
  only one it separates (0/8).
- R6 (C2, B3/B4): the predicate exercises committed copies; the live read on the real host was done once by this seat (AGREE,
  unsupported=0). The numlock 0..1 range is a lane rule, not a source fact (v2 says so; v1 did not).
- R7 (format): the C1 and C3 harnesses print one line per control before their summary line. The frozen sentence is the
  summary line; a reader who expects the harness to print only that line will see extra lines.
- R8 (C1 title): "Hyprland 0.56.2" is supported by `hyprctl version` (host read) and the pin commit, but no frozen leg checks
  the version string against the pin. Host version is a read fact, not a predicate fact.
- R9 (v2 provenance): v2 was written by the L1 after the wave-1 critics attacked the v1 predicates (commit order is clean:
  `5a43d67f` precedes `ebd66fbf`). The v2 K16 fix chose to drop the absence half of the quote rather than to narrow the K16
  proposition (A4); that choice is in the L1's hands and is reported here.
- R10 (census): 26 W04 warnings are present at rev; S380 is among them. Warnings do not change the exit code. This seat did
  not run a base-rev full census for a line-by-line comparison (the base export needs the full root; not done).

## 4. Commands (exact; all reproduced in `receipts/receipts.sh`)

```
python3 -I quality/counters/c1-r55-kbd-entry.py --repo <lane> --rev 57584ed6… --work <scratch>/c1
python3 -I quality/check-r55-controls.py --claim c1|c2|c3 --repo <lane> --rev 57584ed6… --work <scratch>/hcN
python3 -I quality/counters/c3-r55-p19.py --repo <lane> --rev 57584ed6… --work <scratch>/c3
TMPDIR=<scratch>/rc bash tools/mado-verify.sh --selftest            # in an export of the rev
python3 -I quality/check-index.py --rev 57584ed6… --repo <lane>
bash scripts/sources-census.sh validate --root <scratch>/root mado   # root = export as mado-shokunin/ + shokunin.conf
python3 -I tools/mado-kbdopts.py --config ~/.config/hypr/input.conf --getoption <scratch>/getoption.jsonl   # read-only
hyprctl version ; hyprctl getoption input:{repeat_rate,repeat_delay,numlock_by_default} -j ; hyprctl devices -j   # reads only
```

## 5. Not run / not verified

- Sentence-to-pin entailment of the K and H rows and of P23 beyond the manual P23 check: not this seat's scope (w2 sentence
  audit / closure review). The manual P23 check is one reading, not an audit.
- Base-rev census comparison (not run; see R10). Freeze-order checker `quality/check-freeze-order.py` not run by this seat.
- The C2 hold-out fixture contents were not read by this seat beyond what the frozen C2 harness does at the rev.
- No host mutation: no `hyprctl keyword/dispatch/reload`, no config write. No install.
