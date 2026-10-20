# CriticC2 — C2 is real but narrow (it closes the R18-V3 disclosure defect; it does not make any walker fact fresh). The nine note pointers are honest apart from two overclaims. The gate re-pin, and the SKILL "read walker 2.17.2" wording, change what a pin means unless the PASS meaning is narrowed in the same edit.

Axes used: **F** freshness, i.e. pin currency (the C2 counter); **P** provenance/honesty (no claim beyond its evidence); **G** gate signal (what a row status certifies); **H** harm watch (selftest N/N, other counters).

## 1. Is it freshness or bookkeeping? Both, and the closure must name which part is which

- The defect it closes is real. R18-V3 found 2.17.0 pins stated as present tense with no in-file pointer. The verifier routed it as a provenance defect, and a dated pointer is the correct fix. That is a gain on **P**.
- It adds no fresh facts. After C2, the number of walker facts re-measured on 2.17.2 is **0**: help text, flags, D-Bus, sockets, version print, `pacman -Qkk` and the running PID are all still 2026-10-14 / 2.17.0 measurements. 13/13 = 10.0 on a sub-axis called "freshness" saturates the axis early. The closure text must say "13/13 pointed, 0 re-measured". It must not say "the walker corpus is current".
- Three of the 13 credits are formatting or incidental, not new disclosure:
  - **README.md** is "current" through `corpus/README.md:44`. That is the walker-route-r18 index row, which cites S072/S091. The actual dated sentence is `:135` ("2.17.0-era pins … are dated, not current"), which has no `2.17.2`/S### token. The credit is incidental and already present in the 9c54c56 baseline: `fresh-pins.py 9c54c56` gives README `pointer_lines [44]`.
  - **SKILL.md** already has a substantive pointer at `SKILL.md:1822-1829` (round-18 erratum: "pacman.log:2929 upgraded walker 2.17.0-1 → 2.17.2-1"). It fails the counter only because no S### token sits on the same line. Adding the token is bookkeeping. The new information in a round-19 SKILL erratum is coverage of `:1075` and `:1475-1476`, which the round-18 erratum never named (confirmed in `drafts/SkillPins-erratum.md:18`).
  - **walker-route-r18.md** is credited through its `source:` header line 1.

## 2. Counter blind spot (demonstrated)

`POINTER` accepts any S### token on any line containing `2.17.2`. Test in a /tmp clone at 17661e0: append `# walker 2.17.2 S001` to `tools/mado-verify.sh` and `see 2.17.2 S001` to SKILL.md, then commit. Run `fresh-pins.py HEAD`:

```
4 [('SKILL.md', [1845]), ('tools/mado-verify.sh', [3786])]
3277:    if [ "$kv" = "2.17.0" ]; then
```

The gate counts as "current" while its code pin is still `2.17.0`, and S001 is an unrelated row. Impacted axes: **F** (counter inflation) and **G**.

The counter is frozen and cannot change. The closure must add two review checks:
- (a) Every crediting line cites S090, S091 or S096 only.
- (b) `git show REV:tools/mado-verify.sh | grep -c '"2.17.0"'` = 0 if the gate is re-pinned. If it is not re-pinned, the closure must say so explicitly and not let a comment line stand in for a pin move.

## 3. The landed pointer blocks (worktree, nine notes)

**Prefix integrity holds.** For all nine files, `head -c <17661e0 size>` has the same sha256 as `git show 17661e0:<f>` (prefix_eq=yes ×9). The 9 "deletions" in `git diff --stat` come from the old files having no final newline, not from rewritten bytes. The new endings still lack a final newline. In `config-health-report-r3.md` the heading follows the last list line with no blank line; this is cosmetic.

**With the worktree regex simulated**, all nine notes match. Tokens: S090 alone in five notes; S090+S096 in remaining-planes-census, walker-deep-r9, walker-deep and walker-live-surface.

**Overclaims to fix (P):**

1. **waybar-walker-plane.md pointer, bullet 2:** "Version-bound, dated, **not valid for 2.17.2**: … and the `walker --help` flag list (`:196-197`)."
   - This is a negative fact nobody measured. The 2.17.2 help may be identical.
   - Fix: "not re-verified for 2.17.2".
2. **waybar-walker-plane.md pointer, bullet 3:** "the walker restart hooks at `/var/log/pacman.log:3062` and `:3123` (S090) **make that PID stale**."
   - S090's own limits column says "a log line is not a running-binary fact" (`corpus/SOURCES.md:102`).
   - Fix: mark it `[INFERENCE]` or write "may no longer be current". config-health-report-r3's pointer already uses that hedge.
3. **Citations of S096 while the row is still unrecorded:**
   - `grep '^| S096' corpus/SOURCES.md` returns nothing.
   - walker-deep.md and walker-deep-r9.md cite "(S096)" for the version literal; remaining-planes-census and walker-live-surface say "reserved/pending".
   - If S096 lands with different content, or does not land, four notes cite a phantom row.
   - Required order: S096 must be in SOURCES.md in the same commit.
4. **walker-deep.md pointer** labels a value `sha256[:16]` but prints 20 hex chars (`3c5c6867d0216d0c8643`). It also states a new host read ("`~/.config/walker/config.toml` … was re-read this round, unchanged") without a row token.
   - Fix: cite S091 for that file, or drop the clause.
   - The seat's instruction was "no new facts beyond the note, S090 and route-r18".

### What every pointer must say

- When the note's 2.17.0 values were measured.
- `/var/log/pacman.log:2929` (S090): the host package moved to 2.17.2-1 at 2026-10-20T09:16:46-0300. This is consistent with `/var/lib/pacman/local/walker-2.17.2-1/desc` INSTALLDATE 1792498606 = 2026-10-20 12:16:46 UTC; I read the file bytes.
- `/usr/bin/walker` read as bytes (S096; same digest as S091):
  - 7,039,912 B, sha `25240650…`
  - exactly one `2.17.2` (context `…elementsversion2.17.2\ntoggle exact search…`, offset 856,302)
  - zero `2.17.0`
- Which of the note's claims are version-bound and therefore dated, and which are not.

### What every pointer must refuse to claim

- **That `walker --version` prints `2.17.2`.** Round 9 proved print == rodata literal only for the 2.17.0 binary, by executing it (`walker-deep-r9.md:58,305`). Its own falsifier says a rebuilt binary moves sha and BuildID, and both moved: `64826a85…`→`25240650…` and `a22452d1…`→`19200fe4…` (per `drafts/HostWalkerBytes-row.md`). The upstream path supports it only as `[INF-docs]`: `walker-v2.17.2-src-main.rs:86-89` prints `env!("CARGO_PKG_VERSION")` in `connect_handle_local_options` (client-local, exits before startup), and `Cargo.toml:3` has `version = "2.17.2"`. Whether this binary is a faithful build of the tag stays `[UNK]` (`walker-route-r18.md:290-291`).
- **That the running walker service is 2.17.2.** The hook lines are not process facts.
- **That help text, D-Bus, sockets or the action list are unchanged or changed in 2.17.2.**
- **The word "re-verified"** for anything except file bytes that were actually re-hashed.

## 4. Is the gate re-pin justified by file bytes alone?

### For identity: yes

Three independent byte sources agree that the installed version is 2.17.2:
- the rodata literal (count 1, no 2.17.0)
- `desc` `%VERSION% 2.17.2-1`, with BUILDDATE 1791468872 = 2026-10-08 14:14:32 UTC, which matches the binary mtime `2026-10-08 11:14:32 -0300`
- `pacman.log:2929`

Upstream code shows the printed string is that literal. So predicting that live `walker --version` now prints `2.17.2` is a strong `[INFERENCE]`, but it is not observed.

### For the meaning of a PASS: no, not as currently written

- The gate defines the pins plane at `tools/mado-verify.sh:60-62`: "pins — … walker 2.17.0 (SKILL.md "Version pins"): **a changed pin is a FAIL — the claims must be re-verified, not silently reused**."
- The row comment `:3271` and header `:56` anchor the pin to "MADO-R3-1 §1/§6". config-health-report-r3 §6 carries "298 L", which is false for 2.17.2: S091 has 305 L.
- Flipping `"2.17.0"`→`"2.17.2"` at `:3277-3278` and leaving the rest makes a future live run print `PASS "2.17.2 (pin matches)"`. That PASS vouches for claims never measured on 2.17.2. This is exactly the silent reuse the gate exists to block.
- Impacted axes: **G** and **P**. This is an identity change of the row: it moves from "claims verified for this version" to "host carries this version".

### Same defect in the SKILL draft

`drafts/SkillPins-erratum.md:39` says of `SKILL.md:23` ("Version pins for all claims below: … walker 2.17.0"): "read 'walker 2.17.2' today". That re-pins the measurement-provenance pin of every SKILL walker claim to a version none of them was measured on.

Fix: "claims below were measured on walker 2.17.0; the host now carries 2.17.2 (S090/S096); not re-verified for 2.17.2".

### Smallest safe correction (two options for L1)

- **(i) Smallest:** keep `:3277-3278` at `2.17.0`. Add a header line beside `:60`: `walker pin held at 2.17.0 (claims measured on 2.17.0); host package/binary now 2.17.2 (S090 pacman.log:2929, S096 rodata) — live run will FAIL until re-verified`.
  - This earns the counter credit honestly, with no semantics change and no selftest change.
  - It deviates from the pre-registration wording ("pin … move with it"). The closure must say so instead of claiming the move.
- **(ii) If the pin moves:** in the same edit, narrow the PASS meaning.
  - PASS detail along the lines of `2.17.2 (installed-version identity; S096 file bytes) — walker claims dated 2.17.0, see SKILL errata r18/r19`.
  - `:56`, `:60-62` and `:3271` re-anchored from "MADO-R3-1 §1/§6" to walker-route-r18 + S090/S096.
  - The pins-plane sentence must state that for walker a match certifies identity, not claim re-verification.
  - Without these, (ii) is a defect, not a tradeoff.

## 5. When does the move become a harm?

1. **"Gate now FAILs where it passed."**
   - Not on hermetic modes. `live.walker.version` is emitted only inside `live_plane()`, which returns early with `live.plane UNKNOWN` when `hyprctl`/`HYPRLAND_INSTANCE_SIGNATURE` is absent (`tools/mado-verify.sh:3033-3047`). No `--regression` case references the walker pin text: grepping `@old`/`@new` for 2.17 finds nothing.
   - On the live host the row goes from FAIL `[INFERENCE]` (2.17.2 on disk vs pin 2.17.0) to PASS `[INFERENCE]`. Neither is observed this round.
   - The last observed live result is `.ufo/evidence/round-12/gate-live-after.txt:30` `PASS 2.17.0 (pin matches)`; no later live receipt exists.
   - A host on 2.17.0 (rollback) would FAIL after the re-pin. That is correct behaviour, not a harm.
2. **The "selftest stub" in the pre-registration does not exist.**
   - `SCORECARD.md:1103` says "the gate's `live.walker.version` pin **and its selftest stub** move with it". The GateFreshJj item says "update any selftest stub/assertion that prints or expects 2.17.0".
   - At 17661e0 no selftest scenario stubs `walker` or asserts `live.walker.version`. The only gate hits are `:3271-3292` plus header `:56,:60`. Scenario C (`:1042`) runs live with no hyprctl, so it stops at `live.plane UNKNOWN`.
   - Harm if the closure reports "stub moved" (false provenance), or if a new test asserts absence (`st_not_has … 2.17.0`). That test passes vacuously because the row is never emitted.
   - If L1 wants PASS, pin-changed FAIL and absent-binary arms exercised, the selftest needs a sandbox with:
     - a `hyprctl` stub answering `version` with rc 0
     - `HYPRLAND_INSTANCE_SIGNATURE` set
     - a `walker` stub printing `2.17.2` (PASS) or `2.17.0` (FAIL "pin changed: '2.17.0'"), and no walker for FAIL "not on PATH"
     - `st_row_has live.walker.version <status>` asserting presence for each arm
   - The selftest count N changes, so harm-watch "gate selftest N/N" must be re-cut. The round-18 receipts that record gate sha `c9fb0cef…` (`evidence/final/harm-watch-pins.txt:2`, `harm-measure-u.txt:9`) record the sha but do not gate on it, so they need no change.
3. **Two pin authorities disagree.** If the gate moves to 2.17.2 while SKILL "Version pins" (`SKILL.md:22-23`, the source the gate header names) stays a 2.17.0 provenance pin, or is reworded to 2.17.2 as in the draft, then either the authorities disagree or SKILL's claims are silently re-pinned. Gate and SKILL must use the same pin meaning in the same commit.
4. **Cross-claim interference with C3: none.** `tw-recall.py` reads its inputs and expected.json at `PIN_REV` 9c54c56 and digest-checks them (`tw-recall.py:49-59`). The gate edit does not touch them.

## Summary of corrections (smallest first)

- waybar-walker-plane pointer: "not valid for 2.17.2" → "not re-verified for 2.17.2", and mark the PID-stale clause `[INFERENCE]`.
- Land S096 in SOURCES.md in the same commit as the four notes that cite it. Fix walker-deep's `[:16]` label and either cite S091 for its config re-read or drop it.
- SKILL erratum: keep `:23` as a 2.17.0 provenance pin plus a dated pointer. Do not write "read walker 2.17.2".
- Gate: option (i), or option (ii) with the PASS meaning narrowed and the anchors moved. Do not claim a "selftest stub moved". If arms are added, assert presence per arm with a hyprctl+walker stub sandbox.
- Closure: report "13/13 pointed, 0 re-measured". Apply the review checks (row ∈ {S090, S091, S096}; no `"2.17.0"` code pin if the gate was claimed re-pinned). Note that the README and route-r18 credits are incidental or pre-existing.

## Limits

- I did not run the gate in any mode (no `--selftest` or `--regression`). The gate re-pin was not yet in the worktree when I read it (`git diff --stat 17661e0 -- tools` was empty), so I judged the plan, not landed bytes.
- I did not read every pointer seat's report. Each pointer was judged against its own note only through the lines it cites. I did not diff walker v2.17.0 against v2.17.2 sources; that is other seats' work.
- BuildID `19200fe4…` is taken from `drafts/HostWalkerBytes-row.md`; I did not recompute it.
- No web fetch, no walker/pacman/systemctl. Host reads were file bytes only: `/usr/bin/walker` (python `open()`, `sha256sum`, `stat`), `/var/lib/pacman/local/walker-2.17.2-1/desc` and `/var/log/pacman.log` (grep).
- The counter test ran in a /tmp clone, which I then removed.

## Installs

none
