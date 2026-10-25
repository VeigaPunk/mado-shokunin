# mado round 40 — registration v2 (re-registration, frozen before any round-40 data)

Supersedes the predicates of `registration.md` (freeze `5e7e88525cc539563de7746361b2650802e81809`, base
`9fc511ddce708327377161202f358ce37dc266ba`); the claims, their axes and the base are unchanged. The wave `w1`
(64 seats, results `w1-results.json`) falsified the v1 predicates **before any data commit** — no
`tools/mado-options.py` change, no entry, no registry row, no Gate line had landed. The v1 counters stay in
the tree as the superseded predicates; the claims bind to the v2 predicates below, which were committed (with
their controls and the receipts of those controls) in this freeze, before the data commits. Honest ordering:
two w1 seats scored a delivered candidate against v1 (`ExecToolLive`, `ExecToolIndep`: `13/13`), so v2 was
written after seats had seen v1 scores; v2 is strictly stronger than v1 on every point (nothing loosened), and
the operator rules which predicate binds — the report gives both scores at the data tip.

## What the wave found, and where each finding is closed

| Finding (seat, report) | v1 consequence | v2 change |
|---|---|---|
| `CritC1Cheat` `cheat-c-leak-min.py`: a tool with **no conversion** execs the counter's own model, found through `/proc/<ppid>` or the lane path | TARGET_MET at 13/13 | every tool and selftest runs in a bubblewrap sandbox (no lane, no counter, no /home, fresh /proc, read-only tree); no bwrap → SETUP exit 2 |
| `CritC1Cheat` `cheat-d-forge.py`: forged the stub's `calls.log`, never ran the compositor | 13/13 | the fake compositor is a unix-socket server held by the counter process; the table lives only there; the request log is the server's |
| `RevC1Counter` S1: fixtures replayable from public `(REV, i)` seeds | 13/13 | per-run nonce mixed into every seed, printed and replayable (`--nonce`); coverage comes from a deterministic lattice, not the draw |
| `RevC1Counter` S2/`CritC1Cheat` B: echo selftest satisfies clause b | b:1 | clause b2: 6 nonce-chosen comparison flips in the tool's NEW functions must fail the selftest (>= 4 of 6; >= 12 sites) |
| `RevC1Counter` S3, S5, S7, S8: live payload presence-only, failure legs unchecked, naming by substring, duplicate rows | 13/13 | `live` compared token-wise with the value the server sent; tree digest re-checked after every run; stderr must name only the victim; rows must equal the expected sorted key list |
| `RevC1Counter` S4: hostile probe enforced by argparse accident | 13/13 | `--probe=…` spellings, `a/--batch`, `a b`, `a;dispatch`, `--live` with `--getoption` |
| `RevC1Counter` S6: `exec("import socket")` passes clause g | g:1 | clause g denies `exec`/`eval`/`compile`/`__import__` names and `/proc`, `c1-r40`, `quality/counters` strings (a heuristic; the sandbox is the boundary) |
| `MutC1Controls`: 14 of 22 further mutants survived | — | generator covers alpha ties, weight case, fractional angles, floats within 1e-6, padded replies, the sentinel phrase as a str value, probe duplicates/failures, a probe sorting before the declared keys, a two-component vec2 difference in either component, default program lookup, row order, `live` type; 57 controls |
| `CritGeneratorCoverage`, `CritClaimWording` F1, `ExecAllOptionsForms`, `ScoutOptionTypes`: a fifth native form **`vec2`** (6 of 353 options; none declared on this host) | "four native forms" false as a universal | the tool and the counter handle `int|float|str|custom|vec2`; the capture `c1/native-capture-all.jsonl` (353 lines) is committed and read by clause k2 |
| `CritGeneratorCoverage`, `RevModelVsSource`: gradient colour tokens are parsed by Hyprland's `ParserUtils::parseColor` (`floor(a*255.F)`, uint8 channels, `#rgb` forms), not by hyprlang's `configStringToInt` (`std::round`) | model wrong on three classes | separate `grad_color` and `hl_int` models; generator draws gradient spellings a config FILE can carry (`#` starts a comment); stoi-prefix angles |
| `ExecStubFidelity`: the real reply is `{"option": "k", "int": 1, "set": true }` + `\n`, floats `%f`, failure message on **stdout** with rc 1 | stub unrealistic | stub bytes follow `HyprCtl.cpp` dispatchGetOption (`:1701-1728` at the host commit), with padding variants; failure fixtures speak on stdout |
| `SentLiveVerbs` (critical): a config-declared key `x/--batch` turns one `getoption -j` into a `[[BATCH]]` request that runs `dispatch exec` | tool passed it through | every key (declared or probed) must fully match `[A-Za-z0-9_.][A-Za-z0-9_.:-]{0,127}` before any request (exit 2, named); program resolved to an absolute regular executable not group/other-writable (exit 5); stdin `/dev/null`; environment limited to PATH, HYPRLAND_INSTANCE_SIGNATURE, XDG_RUNTIME_DIR (+LC_CTYPE); reply read to 64 KiB; strict reply typing; `--live` with `--getoption` refused |
| `RevToolSafety` F2/F3: `null` reply raised TypeError; unbounded capture | exit 1 / OOM | named exit 5; 64 KiB cap |
| `CritC2Cheat`: 5 files / 1.4 kB / one receipt shared by four ids / `forms int=1` scored `1/1` | admitted | receipts >= 512 bytes, distinct path+sha+quote per id, exactly one GATE line per id in column 0; the forms line must equal the counts of the committed capture (70 lines), the allforms line those of the 353-line capture; quotes may not sit on a census line |
| `RevC2Counter` F1–F4, X01–X13; `MutC2Controls` M4, M7 | six mutants admitted; two control gaps | token-exact `used-by`; fence-aware README and entry; census lines standalone in the entry and the receipt; sha on its own line; stale/indented GATE lines refused; new controls for the opened date and for a receipt committed outside `fetch/` |
| `RevSeparability` F1/F4, `CritClaimWording` F4 | "C1 shares no file with C2" false | corrected below |

## Claims (unchanged in substance)

- **C1 — operability (capability acquisition).** `tools/mado-options.py` gains `--live` (+ `--hyprctl PATH`,
  `--probe KEY`): one `hyprctl getoption -j KEY` per declared key, native replies converted the way the host
  converts them and compared; rows carry the vocabulary `agreement | agreement* | mismatch | config-only |
  live-default` (`agreement*` = equal, `set`, and more than one declarer) and a `live` field.
  - **Predicate `PRED-C1-r40-v2`:** the docstring of `quality/counters/c1-r40-live-v2.py` (the code is the
    same sentence).
  - **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r40-live-v2.py --repo . --rev <rev>`
    (a fresh nonce per run; the nonce is on the final line and replayable with `--nonce`).
  - **Before** (base): `fixtures=0/19 tool=present verdict=TARGET_MISSED`, exit 1 (`receipts/c1-v2-before-base.txt`).
  - **Target:** `fixtures=19/19 tool=present verdict=TARGET_MET`, exit 0, at the data commit and at the tip
    (the tip = the last lane commit before the report; the report names it). Clauses a, b (selftest n >= 79),
    b2, g, k, k2 all hold.
  - **Kill rule:** anything else at the data tip is a miss, reported as an honest stop; no narrowing.
- **C2 — coverage (sourced).** `corpus/knowledge/hyprctl-getoption-native-forms-r40.md`: what the compositor
  answers to `getoption -j` (five forms and `no such option`), the per-form conversion, the gradient colour
  parser's floor-versus-round difference, the angle-inheritance rule with the host's two rows, `vec2`, the host
  census. Cites held S162, S173, S180, S181, S158, S215 (re-opened; `used-by` only) and new rows opened this
  round (the 0.54.0 Using-hyprctl page, and one own-work census receipt).
  - **Predicate `PRED-C2-r40-v2`:** the docstring of `quality/counters/c2-r40-forms-entry-v2.py` (clauses a–h).
  - **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r40-forms-entry-v2.py --repo . --rev <rev>`
  - **Before:** `admitted=0/1 verdict=TARGET_MISSED`, exit 1 (`receipts/c2-v2-before-base.txt`).
  - **Target:** `admitted=1/1 verdict=TARGET_MET`, exit 0. **Kill rule:** as C1.

## Controls (committed receipts, run at the pre-freeze commit `c96cf6d8cdc15377bc7482d306090aae2217e471`)

- **C1:** `receipts/ctl-c1-v2.txt` — `CTL_C1V2: controls=57 correct=57/57`: the reference (`c1/ctl-ref-tool-v2.py.txt`,
  which is byte-identical to the candidate later committed as `tools/mado-options.py`) reaches TARGET_MET; the base tool scores `0/19`; the seven w1 cheats (judge leak ×3, forged log, echo
  selftest, REV-seed replay, echo-with-base-parser; `c1/cheats/`) are not TARGET_MET; 48 single-defect mutants
  and single-edit cheats of the reference (fabricated `live`, exec-imported socket, hardcoded hostile list,
  duplicated rows, key allowlist dropped, child environment inherited, stdin inherited, reply cap dropped,
  `set`/value typing dropped, writable program accepted, `--live`+`--getoption` allowed, gradient alpha
  rounded, gradient tokens through the int parser, program not resolved …) each fail a fixture or a clause.
  One mutant (float64 instead of float32 alpha) is **equivalent** on every alpha with <= 3 decimals
  (`receipts/f32-equivalence.txt`: 0 of 999 differ) and is not a control.
  Three further reference runs at random nonces: `receipts/ref-random-nonces.txt`.
- **C2:** `receipts/ctl-c2-v2.txt` — `CTL_C2V2: controls=33 correct=33/33`: control P (a fabricated
  self-consistent set) is admitted (`1/1`: the declared residual); the 20 v1 mutants, the wave's RevC2Counter
  mutants X01–X14, the CritC2Cheat cheats (shared receipt, sub-512-byte receipts, N=1 census, quote on a
  census line, wrong allforms line) and the two MutC2Controls gaps are each `0/1`.

## Residuals (declared)

- C1: a tool that **contains** the reference conversion tables passes — it is then an implementation; the
  heuristic clause g and the sandbox do not prove conversion fidelity beyond the generator's value space. The
  live host census (62 agreement, 8 agreement*, 0 mismatch under the delivered tool) is reported, not scored,
  and is made by the same model the counter encodes: it cannot separate a copy of the tables from an
  independent implementation. The independent evidence is the seat oracle runs (`w1/ExecOracleHlInt`: 1401/1401
  of the generator's int spellings agree with the real hyprlang library; 164/188 on a wider corpus, the
  divergences being out of the generator's space — int64 width, `inf`/`nan`, inline comments) — cited, not scored.
- C2: a fabricated self-consistent set (invented receipts >= 512 bytes, distinct per id, invented quotes, count
  lines copied from the committed captures) passes; committed bytes cannot prove a receipt is what its
  location served or what the compositor answered. `admitted=1/1` measures admission wiring, not coverage of
  real surfaces beyond what the receipts hold (`RevSeparability` F2).
- Separability, corrected: the claims share **no evidence artifact**; both read the delivered tool — C1 by
  behaviour, C2 by its sha256 (clause h), so the delivered tool bytes must land before or with the census
  receipt and any later tool edit needs a regenerated receipt (`N17` control).
- A cited held row keeps cells 1–10 byte-equal to base (stricter than CORPUS.md's in-place rule): a
  `recheck`/`status` change on S162/S173/S180/S181/S158/S215 is not made this round.

## Frontier step, assimilation, considerthese (unchanged from `registration.md`, with the wave's verdicts)

- Assimilation theme "the host's bar producers": `ScrAssimK2` recommends REFUSING the staged
  `host-producer-outputs-r29.md` and admitting a re-grounded census successor; `ScoutK1K2Held` finds most of
  `host-bar-producers-r28.md` held. The decisions are the lesson's Gate, recorded after the data commits.
- considerthese `2026-10-25.md` proposal 2 (dead attempts and dirty closures from the watchdog digests): mined
  as a lesson table (`w1/ExecWatchdogTable/table.md`).

## Harm watch (unchanged)

`bash tools/mado-verify.sh --selftest` `460/460`; `python3 -I tools/mado-options.py --selftest` all-pass with
n >= 79 (base 71); `quality/check-index.py` complete; census exit 0; `check-axis-scores.py` `mismatched=0`;
the round-39 predicates re-measured at their own named revisions (a re-score at a later tip sees the changed
tool sha by design, `c4-r39` clause e). No config tree, service or compositor state is written; the only
compositor verb run is the read-only `hyprctl getoption -j` (plus `version` and `descriptions -j` by seats).
