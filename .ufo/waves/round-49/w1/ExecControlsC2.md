# ExecControlsC2 — do-nothing and forgery controls for the C2 counter draft (round 49, w1)

Base `03e4ae76aff7a4be59cb69970dd553baa319695a`. Instrument scored: the w1 draft
`.ufo/waves/round-49/w1/ExecCounterC2/c2-r49-bind-entry.py`, **sha256
`a2e91724ffca3b151f732047dfcb4d4aa76c3c554edd78ecfca2344f44b4ce04`** (bytes copied to
`w1/ExecControlsC2/receipts/draft-scored.py`, same digest). The draft moved four times while this
seat worked (`8e0c186b…` → `f772bba1…` → `12200189…` → `e6df8a19…` → `a2e91724…`); every verdict
below is from `a2e91724…`, re-run after each edit, and the digest is printed in the receipt header. No lane file was
edited.

**History in one line.** At `12200189…` this seat found four admitted forgeries (04, 09, 13, 14 — see
§3.1). The counter seat revised the draft twice: `e6df8a19…` closed 04, 13 and 14, and `a2e91724…`
closed the used-by boundary that control 17 recorded (a row whose only consumer is an already-held
document). The fourth (09) is kept as the declared trust-root residual. `receipts/controls.txt` is the
`a2e91724…` run: **18 of 18 controls return the verdict a correct counter must return, except 09.**

## 1. Method

Eighteen control bundles under `.ufo/waves/round-49/w1/ExecControlsC2/controls/`. Each one is a
candidate *state of the lane*: `drive.py` clones the lane `--shared` into
`/fast/scratch/hyaku/mado-r49/ExecControlsC2/work/<control>/repo`, checks out BASE, applies the bundle
(entry text, registry rows inserted inside `## Registry`, pins under `.ufo/waves/round-49/fetch/`, the
receipt under both `receipts/` and `fetch/`, `corpus/lessons/round-49.md`, the `corpus/README.md` index
row), commits once, and prints the REV. `score.py` runs the draft once per REV with `TMPDIR` inside that
control's scratch dir (never `/tmp`, so clause r's `tmp_root` guard is satisfied honestly) and the
inherited read-only socket variables; full per-control output is in `receipts/<control>.txt`.

`expect.json` separates two things: `expect` = the verdict a **correct** counter must return (the
design), `predicted` = what this draft was predicted to do. `controls.txt` compares the observed
verdict with the design and tags a divergence `DEFECT`.

## 2. Control set and observed verdicts (draft `e6df8a19…`)

| # | control | what it injects | design | observed | stopper under `e6df8a19…` |
|---|---|---|---|---|---|
| 00 | base-golden | complete entry: head S352-S354, pinned rows, 6 quotes at computed lines, 6 steps each carrying a verified quote, live receipt the entry repeats, Limits, held S303/S317/S319 cited | MET | **MET** | — (anchor; `overlap=0.000`) |
| 01 | do-nothing | empty commit, no entry | MISS | **MISS** | a |
| 02 | stub-head-one-sentence | full head, one body sentence | MISS | **MISS** | e, f (also g,h,i) |
| 03 | paste-r46-verbatim | round-46 chain pasted under a round-49 head, old citations left in place | MISS | **MISS** | d (`pin_not_cited_by_row`, 30 lines) |
| 04 | paste-r46-paraphrased | the same round-46 ground, citations stripped, every content word swapped | MISS | **MISS** | i (6-word shingle `overlap=0.232` ≥ 0.15) |
| 05 | quote-forged-one-word | one identifier inside a cited quote changed | MISS | **MISS** | d |
| 06 | locator-off-by-one | a true quote cited one line below its line | MISS | **MISS** | d |
| 07 | steps-without-locators | six steps with the verified quote/locator removed | MISS | **MISS** | e |
| 08 | branch-url-pin | one row URL ref replaced by `master` | MISS | **MISS** | c |
| 09 | digest-edited-row-file | pin byte changed (trailing space on an uncited comment line) **and** the row digest recomputed | MISS | **MET** | none — **DEFECT**, the declared trust-root residual |
| 10 | receipt-typed-by-hand | internally consistent false capture: binds=191 = 141 named + 42 code + 6 mouse + 2 switch, true digest, `int 0`; entry repeats it | MISS | **MISS** | r only (`f:1 r:0`) |
| 11 | receipt-accurate-handtyped | the truth, provenance "typed by hand from another terminal" | MET | **MET** | — (false-positive guard for r) |
| 12 | held-s319-reregistered | S319's URL/bytes re-registered as S355, cited instead of S319 | MISS | **MISS** | g (`re_registered_held_url`), i |
| 13 | registry-row-unused | new row S356, pinned, mined, Gate admit line, used-by a path that is not in the tree | MISS | **MISS** | i (`row_used_by_absent=S356:[…draft-notes.md]`) |
| 14 | step-locator-off-by-one | step 1's verified-quote locator shifted to 368 (the quote is at 367) | MISS | **MISS** | d, e (`verified_steps=5`) |
| 15 | held-prose-verbatim | eight byte-identical long lines from the held round-46 entry, no citations | MISS | **MISS** | i (`base_duplicates=8`) |
| 16 | row-duplicates-base-url | a new, correctly pinned row for `src/config/legacy/ConfigManager.cpp`, already held by S303/S317 | MET | **MET** | — (g is narrowed to S319 by design) |
| 17 | row-used-by-existing-path | new row S357, same shape as 13 but used-by an existing held document | MISS | **MISS** | i (`row_used_by_not_new`: the consumer must exist at REV *and* be absent at BASE) |

Eighteen of eighteen return the verdict a correct counter must return except 09, which is the declared
residual. The must-admit anchors (00 golden, 11 accurate hand-typed receipt, 16 base-URL reuse) are
admitted, so the draft is not a blanket rejector; 17, which was the boundary of the previous used-by
rule, now misses.

## 3. Findings

### 3.1 Closed between `12200189…` and `e6df8a19…` (measured both before and after)

- **Novelty (was F1).** At `12200189…` the test was a whole-line grep over `body[:40]`
  (`:840`, `:843`); control 04 (round-46 ground, citations stripped, one content word swapped per
  sentence) was admitted with `dup=0`. At `e6df8a19…` clause i also hashes 6-word shingles of the
  body against the base tree's `corpus/knowledge` + `corpus/lessons`; control 04 measures
  `overlap=0.232` against a 0.15 threshold and misses, while the golden measures `0.000` and control
  15 still misses on the whole-line half (`base_duplicates=8`). Clause text:
  `clause=i … grams=1187 base_grams=268678 overlap=0.232`.
- **Unused row (was F2).** At `12200189…` the only read of `cells[10]` was inside clause b's head-row
  loop (`:1007`); control 13 minted a row used by the round-46 entry and was admitted. At
  `e6df8a19…` i requires every new row's used-by to name the entry or a path that exists at REV;
  control 13 (used-by a non-existent path) misses at `row_used_by_absent`. Control 17 pins the
  boundary: an *existing but unrelated* path still satisfies the rule (`MET`), so the freeze buys
  "used by something in the tree", not "used by this round's claim".
- **Step locator (was F3).** At `12200189…` clause e only required `1 <= a <= b <= nlines` (`:575`),
  so control 14 (step locator 367 → 368) was admitted. At `e6df8a19…` each numbered step must carry a
  quote that clause d verifies; control 14 now misses (`clause=d` and `clause=e … verified_steps=5`).

- **Used-by boundary (was 17).** At `e6df8a19…` clause i accepted any used-by path that exists at REV,
  so control 17 (a new row used by the held round-46 entry) was admitted. At `a2e91724…` the named
  consumer must exist at REV **and** be absent at BASE; 17 misses at `row_used_by_not_new`, and 13
  (used-by a path that does not exist) still misses at `row_unused`. ENTRY itself qualifies (it is new
  by clause a), as does a new C1 path; the golden's rows are unaffected.

### 3.2 Still open (declared residual)

- **09 — clause c binds the row to the committed file, never to upstream.** `digest =
  hashlib.sha256(blob).hexdigest(); if digest not in digests:` compares the fetch copy with the digest
  the row records (`c2-r49-bind-entry.py:464-465` region); nothing re-fetches. Control 09 changes a
  pin byte on an uncited comment line and recomputes the row digest, so row == file while both differ
  from upstream, and it is admitted with every clause 1. The draft declares this ("the fetch copies at
  REV are the trust root"), and the round-48 v2 counter carried the same residual — but C2's claim
  says the ground is "pinned by sha256", and this is exactly where that sentence is weaker than it
  reads. Freeze action: state the residual in `registration.md` or add the round-47 precedent (a
  digest list owned outside the committed bytes).

### 3.3 Behaviour confirmed both ways (no action, recorded)

- A complete entry is admitted (00, all clauses 1); do-nothing at a (01); a head without a body at e/f
  (02).
- Forged quote (05) and shifted quote locator (06) refused at d; a true quote whose pin no row cites
  refused at d (03). Note 03's stopper is the *pasted text's own* round-46 citations, not the novelty
  test — the pair 03/04 is what shows the two nets are separate.
- No verified step quote at e (07); branch-ref URL at c (08); held S319 re-registration at g (12);
  byte-identical held prose at i (15).
- A hand-typed capture that contradicts the host is refused at r (10: f passes, r's
  `replay_mismatch … total=192/191` refuses it); a hand-typed capture that matches the host is
  admitted (11). r measures reproducibility, not authorship — so f is a receipt↔entry consistency
  check and r is load-bearing. A scoring run without a reachable compositor is a Setup (exit 2), not
  a pass; the freeze must say so.
- The two admitted-by-design rows are correct: g refuses only held S319's URL (`:769`, `:785`; the
  docstring at `:84-87` allows reopening other held sources), and i accepts any used-by path that
  exists at REV.

## 4. Operational notes for whoever writes the real entry

- **The receipt's form census must use the dump's taxonomy, not the config-line spelling.** A bind is
  `code` when `key` starts `code:` **or** when `key` is empty and `keycode` is non-zero, `mouse`/
  `switch` by prefix, everything else `named`; live on this host that is **named=142, code=42,
  mouse=6, switch=2, total=192** (measured). An entry or receipt saying `code=0` or listing the
  config-line `code:` spelling misses f and r.
- The head must sit inside the first 20 raw lines, `verified-at` on the opener date, and every `S###`
  token anywhere in the entry must exist in the registry at REV — citing held S303/S317/S319 is fine,
  citing a row you forgot to add is a ghost-id failure.
- `input:resolve_binds_by_sym` on this host is **int 0, set false**; f requires 0.
- The bind parser lives in `src/config/legacy/ConfigManager.cpp`, which the registry already holds at
  S303 and S317 at the same commit. g permits a fourth row for it (control 16, admitted), but the
  honest provenance is to cite S303/S317 — otherwise the round's row delta counts ground the registry
  already has.
- The replay compares the **raw JSON digest** of `hyprctl binds -j`; my capture's digest
  `9a47199e2297…` reproduced byte-identically across runs.

## 5. Reproduction

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-49/w1/ExecControlsC2
ulimit -f 65536
python3 build-controls.py        # deterministic bundle generation
python3 drive.py                 # one scratch clone + one commit per control; writes revs.json
python3 score.py                 # runs the draft per REV; writes receipts/controls.txt + receipts/<control>.txt
```
The clones are scratch and are deleted; the bundles and the driver are the reproducible artifact. If
the draft changes, re-run `score.py` (it records the scored digest in the receipt header); a changed
draft with the same eighteen verdicts means no regression.

## 6. Limits of these controls

- The golden bundle, its rows and its receipt are **control-harness bytes** written to satisfy the
  draft's grammar; they are not a proposal for the lane's entry, and the L1's real entry will differ in
  wording and row ids. The receipt's numbers and digest are from a real read-only capture, but the file
  is a shape summary written by this seat, not the L1's capture.
- Every forgery is injected in the clone; nothing was fetched at scoring time except the compositor's
  own read-only `binds -j` inside clause r.
- 09 is a defect **against the claim**, not against the draft's declared residuals (it is declared);
  the novelty, used-by and step-locator gaps found at `12200189…` are now closed at `e6df8a19…`, and
  their residuals (a whole-body rewrite above roughly one word in seven) remain by construction, as
  does 16 (g refuses only S319's URL).
- A control can only exercise the grammar it was built to; a draft edit that renames labels makes a
  bundle miss for a formatting reason, which `receipts/<control>.txt` shows as an unexpected clause
  rather than a silent pass. The `12200189…` → `e6df8a19…` re-run is the worked example: the golden
  first missed at e (`step_without_verified_quote`), and the golden was rewritten to carry a verified
  quote per step.

## 7. Host guard and pins

Pins fetched by this seat (manifest `pins/PINS.json`, each with URL and sha256):
`Hyprland-KeybindManager.cpp` `8d8f35fc…` (Hyprland `efb50993…`, `src/managers/KeybindManager.cpp`),
`libxkbcommon-src-keysym.c` `123e3390…` (libxkbcommon `xkbcommon-1.13.2`, `src/keysym.c`),
`Hyprland-IKeyboard.cpp` `8a800efe…` (copied from `.ufo/waves/round-46/fetch/`, equal to S319's
recorded digest), and `Hyprland-legacy-ConfigManager.cpp` `9db68cf4…` (controls 16 only).
No `pacman`, no package transaction, no compositor mutation, no input injection: the only compositor
reads were `hyprctl version`, `hyprctl binds -j` and `hyprctl getoption input:resolve_binds_by_sym -j`,
with `HOME`/`XDG_*` inside the seat scratch. No capture content is committed (the receipt is a shape
summary: no JSON, no device names, no home paths). No tool was installed. Scratch
`/fast/scratch/hyaku/mado-r49/ExecControlsC2/` is removed after the receipts were copied into this
seat dir.
