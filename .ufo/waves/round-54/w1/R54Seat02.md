# R54Seat02 — C1 source-truth counter path: the frozen proposition-table leg (item 2)

Seat: `R54Seat02`, role `executor`, wave `w1`. Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`,
base `e25149fec8152a3aabd2b18a0ee8663b23cf65aa`, freeze commit `350d30e4ec5531f65ce99a57efeb8216f38e678a`.
Item 2 of the six C1-executor items: **the second bound object of the C1 counter path, the
committed entry's frozen proposition table (P19–P22) and its `verbatim`-quote judge**, audited
inside the whole clause-(a)(b)(c)(d) path and the six frozen controls.

Draft-only: every artefact below was built in `/fast/scratch/hyaku/mado-r54/R54Seat02`, no lane
file was created, modified or deleted, no git/jj mutation ran against the lane, no subagent was
dispatched, no producer or host probe ran, nothing was installed.

## 1. Ground measured (static committed pins only)

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin && git rev-parse HEAD
350d30e4ec5531f65ce99a57efeb8216f38e678a          # freeze commit, base e25149fe is its parent
$ git ls-tree -r --name-only e25149fe -- .ufo/waves/round-52/fetch/
Hyprland-ConfigActions.cpp
Hyprland-ConfigActions.hpp
Hyprland-KeybindManager.cpp
Hyprland-legacy-DispatcherTranslator.cpp
README.txt
SHA256SUMS
$ git cat-file -e e25149fe:corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md && echo YES
YES            # the entry under test is already committed at the base
$ ls quality/counters | grep -c r54
0              # PRED-C1-r54's before-state, matching receipts/before.txt
```

Pin sha256 recomputed from git blobs at `e25149fe` (`git show <rev>:<path> | sha256sum`), all four
equal to the frozen table of `registration.md:14-19` and to the values committed in
`.ufo/waves/round-52/fetch/SHA256SUMS`:

| pin | computed at base |
|---|---|
| `Hyprland-ConfigActions.cpp` | `a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637` |
| `Hyprland-ConfigActions.hpp` | `746c6f517620eb039afbfbb9a4a0e2d5ba1c5eb117bcc8f396173f63091b7073` |
| `Hyprland-KeybindManager.cpp` | `8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40` |
| `Hyprland-legacy-DispatcherTranslator.cpp` | `7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771` |

Entry `corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md` at base and at the freeze
commit hash identically (`764f48679447fd62858e9773607a3c0bee5395b6182bdf9f30f5d7c95f4d0b65`, 24 lines):
the P19–P22 rows are present, 7 cells each, `Pin:anchor` and `Quote` cells byte-equal to the frozen
table of `registration.md:25-30` for all four propositions.

## 2. Working prototype (scratch) — the path is buildable as frozen

`/fast/scratch/hyaku/mado-r54/R54Seat02/proto/c1-r54-errata-truth.py` implements the whole frozen
predicate: it reads every byte from git objects at `--rev` (never the working tree), extracts the
entry's P19–P22 rows, compares them to the frozen table, locates each quote in the pin named by the
row's `Pin:anchor` cell, checks the anchor side-claims, recomputes the pin hashes, and materialises
each of the six frozen controls as a mutated commit in `--work` to prove rejection. Measured against
the real lane:

```
$ python3 -I proto/c1-r54-errata-truth.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
    --rev e25149fec8152a3aabd2b18a0ee8663b23cf65aa --work <scratch>
MADO_ERRATA_TRUTH: rev=e25149fec8152a3aabd2b18a0ee8663b23cf65aa propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
exit=0
```

stdout is exactly one line (`... | wc -l` → `1`); detail lines go to stderr. `--selftest` prints
`selftest: 31/31 passed` plus `selftest: 6/6 control red runs passed` (one red run per frozen
control). The six controls each drop their designated leg:

```
detail: control C1-CTL-1 leg=quotes        quotes=3/4 rejected
detail: control C1-CTL-2 leg=anchors       anchors=3/4 rejected
detail: control C1-CTL-3 leg=pins          pins=3/4 rejected
detail: control C1-CTL-4 leg=anchors       anchors=3/4 rejected
detail: control C1-CTL-5 leg=propositions  propositions=3/4 rejected
detail: control C1-CTL-6 leg=quotes        quotes=3/4 rejected
```

So **the frozen target is reachable**; the contract is not self-defeating. The rest of this report
is what a builder must get right, and where the frozen text does not decide for them.

## 3. Finding 1 (predicate-relevant): the frozen quotes are NOT byte-contiguous in the pins

This is the decisive item-2 result. `claims-frozen.md:22-24` requires each Quote cell to occur
"verbatim and contiguous in the round-52 pin"; `registration.md:51-53` adds the judge rule
"exact byte contiguity after single-space normalization of interior newlines ONLY where the frozen
quote itself carries a newline (P19/P21/P22 are single logical lines)".

Measured byte-exact occurrence counts of each frozen quote inside the pin named by its own row,
read from git at `e25149fe`:

```
P19  byte-exact occurrences in Hyprland-ConfigActions.cpp            : 0
P20  byte-exact occurrences in Hyprland-ConfigActions.cpp            : 1
P21  byte-exact occurrences in Hyprland-legacy-DispatcherTranslator.cpp : 0
P22  byte-exact occurrences in Hyprland-legacy-DispatcherTranslator.cpp : 0
```

and across **all 285 `.cpp`/`.hpp` pin copies in the tree** (`.ufo/waves/*/fetch/*`, `*w1/*/pins/*`):
`P19=0, P20=5, P21=0, P22=0`. The `P19`/`P21`/`P22` hits that do exist in the tree are all in
`.md`/`.tsv` artefacts (entry drafts, earlier wave reports), never in a pin.

The cause is structural, not accidental. Each frozen quote is the *whitespace-collapsed rendering*
of a multi-line source region:

```
1554: '    g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);'
1555: ''
1556: '    if (S.m_passPressed == 1) {'
1557: '        if (!isMouse)'
1558: '            g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);'
```

frozen `P19` quote = `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); if (S.m_passPressed == 1) { if (!isMouse) g_pSeatManager->sendKeyboardKey(...);`
— the four content lines of that five-line span joined with single spaces, indentation dropped,
blank line 1555 collapsed away. Same shape for `P21` (content on 619, blank 620, 621, 622) and `P22`
(content on 573 and 574). None of the four frozen quotes contains a newline, so the registration's
parenthetical "(P19/P21/P22 are single logical lines)" is true of the *entry cell*, not of the *pin
region*.

**The two clauses cannot both be satisfied under the literal reading.** Clause (b) says the `P19`
quote must be found "spanning exactly lines 1554–1558"; a byte-exact contiguous match cannot span a
multi-line region unless the quote itself contains newlines, and none of the four does (measured:
`"\n" in quote` is False for all four). Verified:

| judge | P19 | P20 | P21 | P22 | quotes |
|---|---|---|---|---|---|
| (A) raw byte-exact, no normalization | 0 | 1 | 0 | 0 | **1/4 → TARGET_MISSED** |
| (B) pin whitespace collapsed, quote verbatim | 1 @1554-1558 | 1 @1576 | 1 @619-622 | 1 @573-574 | 4/4 → TARGET_MET |

Only reading (B) satisfies clauses (a) and (b) together, and (B) is the reading under which the
frozen side-claims are exactly true (spans `1554-1558`, `1576`, `619-622`, `573-574` — each match
is unique in its pin, so the anchor is unambiguous).

**Actionable for the builder:** implement the quote leg as *collapse the pin's whitespace runs to a
single space, then require the quote to occur contiguously in that collapsed text, mapping the match
back to a line span via a per-character line map*. Do **not** implement "the quote appears byte-exact
in the pin": that counter prints `quotes=1/4` and a false `TARGET_MISSED` on the honest base. Record
the reading explicitly in the counter header, because `registration.md:51-53` as written invites the
wrong one. This is a frozen-text ambiguity that decides the verdict; it is not mine to edit
(`claims-frozen.md:5-7`: a falsified predicate is an honest stop or a v2 re-registration).

## 4. Finding 2: the quote leg must be verbatim, and the frozen-table check is the load-bearing one

Four candidate judges, scored against the honest pins and against an entry whose `P21` quote is
re-spaced (`; if (` → `;  if `):

```
E1 honest pins:        A byte-exact 1/4 | B collapse-pin 4/4 | C collapse-both 4/4 | D ws-regex 4/4
E2 re-spaced entry:    A rejects      | B rejects         | C ACCEPTS (hole)| D ACCEPTS (hole)
```

(C collapses both sides; D builds `\s+`-joined regex from the quote.) Under C/D the over-permissive
judge admits a quote the entry does not carry verbatim; the counter still rejects that tree only
because the frozen-table drift check fires (`prop=3/4`). That is the second half of the finding:
**the "extract the committed entry's rows and check them against THIS table byte-for-byte modulo
trailing spaces" clause of `registration.md:21-23` is not redundant with the quote leg — it is what
makes a verbatim judge safe.** A counter that skips the frozen-table comparison and relies on a
whitespace-insensitive quote match is gameable by a one-character re-spacing.

Trailing spaces must be tolerated exactly as `registration.md:21-23` says (`.rstrip()` on both sides):
an entry `P21` quote carrying one trailing space scores `prop=4/4 quote=4/4 anch=4/4` under that
rule, and `prop=3/4` under a strict byte comparison — the latter would be a false miss.

## 5. Finding 3: the anchor leg needs exact-span equality, not containment or tolerance

The four side-claims are exact line identities (`registration.md:32-34`), and three looser judges
each admit a control:

- **containment** ("the quote lies inside the anchor's range"): `591-627`, `600-622`, `618-622`,
  `619-623` all accept `P21`'s span `619-622`. `C1-CTL-4` (`:573`) happens to fall outside 591–627,
  so that single control cannot discriminate containment from equality — a counter may pass all six
  controls while holding the wrong anchor rule.
- **±1 tolerance**: admits `C1-CTL-2` (`:1576` → `:1575`) because the true span 1576 is within one
  line of the claimed 1575.
- **range-only with the pin resolved from the frozen table instead of the entry cell**: admits
  **`C1-CTL-2`, `C1-CTL-4` and `C1-CTL-6`** outright — 3 of the 6 frozen controls:

```
C1-CTL-1 leg=quotes     variant: prop=3 quote=3 anch=3 pin=4   designated-leg-drops=True
C1-CTL-2 leg=anchors    variant: prop=4 quote=4 anch=4 pin=4   designated-leg-drops=False  <- ADMITTED
C1-CTL-3 leg=pins       variant: prop=4 quote=4 anch=4 pin=3   designated-leg-drops=True
C1-CTL-4 leg=anchors    variant: prop=4 quote=4 anch=4 pin=4   designated-leg-drops=False  <- ADMITTED
C1-CTL-5 leg=propositions variant: prop=3 quote=3 anch=3 pin=4 designated-leg-drops=True
C1-CTL-6 leg=quotes     variant: prop=4 quote=4 anch=4 pin=4   designated-leg-drops=False  <- ADMITTED
```

The three admitted controls are exactly the three that mutate the *entry's* `Pin:anchor` cell. So
the counter **must** resolve pin and anchor from the entry's own cell (`claims-frozen.md:23-24`: "in the
round-52 pin named by its Pin:anchor cell") and then require the located span to equal the claimed
span exactly. Pin name is the basename before the final `:` of the cell; note the pin names contain
no `:` while the anchor always does, so `rsplit(":", 1)` is the correct split.

The side-claims are exactly true at base — `sendkeystate` opens at line 591 and closes at 627
(`591: 'static SDispatchResult sendkeystate(...) {'`, `626: '    return result;'`, `627: '}'`), and
`P22`'s return at 573-574 follows the scan's closing brace at 571 (`571: '            }'`). The
`P22` clause must therefore be `start > 571`, not `start >= 571`.

## 6. Finding 4: the hash leg has three plausible readings; only one survives `C1-CTL-3`

`C1-CTL-3` (registration.md:44) flips one hex nibble of a recorded sha256 in the tree's `SHA256SUMS`
and requires `pins≤3/4`. Measured per implementation:

| hash leg | pins on the CTL-3 tree | outcome |
|---|---|---|
| computed pin bytes vs the frozen table | 4/4 | **control ADMITTED** — the tree's sums are never read |
| computed pin bytes vs the tree's own `SHA256SUMS` | 3/4 | control rejected |
| recorded-vs-frozen **and** computed-vs-frozen | 3/4 | control rejected, and the pin bytes stay bound to round 52 |

Only the third rejects `C1-CTL-3` *and* keeps clause (c)'s "the round-52 recorded sha256" meaning
what it says. The first is the trap: it passes `C1-CTL-3`'s spirit (pin bytes unchanged) but ignores
the tree's recorded sums entirely, so the same implementation reports `pins=4/4` on a tree whose
`SHA256SUMS` has been rewritten. The second is a different trap: it makes the tree self-certifying,
so a coherent pin+sums co-mutation passes. Demonstrated: append a comment to
`Hyprland-KeybindManager.cpp` and refresh `SHA256SUMS` faithfully → the frozen-table comparison
catches it (`pin leg 3/4`), the self-consistent comparison does not.

Two further hash-leg facts a builder must handle:

- the recorded `SHA256SUMS` lines carry **absolute** paths rooted at the original lane
  (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/fetch/...`). A counter must key on
  `os.path.basename`; resolving the recorded path directly breaks in any clone at another path.
- the file is named `SHA256SUMS` (no extension) in `round-52/fetch/`, but `registration.md:12` calls
  it "its committed `SHA256SUMS.txt`". `claims-frozen.md:81` says "`(+SHA256SUMS)`". The round-54
  fetch dir *does* contain `SHA256SUMS.txt`, so the mis-citation is easy to inherit. `C1-CTL-3` at
  `registration.md:44` says "the tree's SHA256SUMS", which is the correct name.

## 7. Finding 5 (coverage, distinct from every other seat's input): no frozen control mutates a pin

All six controls at `registration.md:42-47` mutate the **entry** (CTL-1, 2, 4, 5, 6) or the
**`SHA256SUMS`** file (CTL-3). None mutates a pin's bytes. Consequences measured:

**(a) A counter that never locates a quote in a pin still rejects 6/6 controls and prints
`TARGET_MET`.** A "self-consistent" counter — compare the entry's cells to an embedded frozen table,
plus check each pin's computed hash against the tree's *own* `SHA256SUMS` — rejects all six:

```
C1-CTL-1 -> REJECTED (prop=3 quote=3 anch=3 pin=4)
C1-CTL-2 -> REJECTED (prop=3 quote=3 anch=3 pin=4)
C1-CTL-3 -> REJECTED (prop=4 quote=4 anch=4 pin=3)
C1-CTL-4 -> REJECTED (prop=3 quote=3 anch=3 pin=4)
C1-CTL-5 -> REJECTED (prop=3 quote=3 anch=3 pin=4)
C1-CTL-6 -> REJECTED (prop=3 quote=3 anch=3 pin=4)
self-consistent counter rejects 6/6 frozen controls
honest base -> prop=4 quote=4 anch=4 pin=4 -> verdict=TARGET_MET
```

and then reports `TARGET_MET` on the honest base **having never verified a single quote against a
pin byte**. This is the §9 do-nothing shape the freeze was written to exclude
(`claims-frozen.md:41-43`), and the six controls do not actually exclude it: they force the counter
to read the entry and the sums, not to read the pins' quoted regions.

**(b) The two real pin-side attacks are invisible to the frozen control set.** With a faithful
`SHA256SUMS` refresh, (i) rewriting the `P22` error string (`key not found` → `key NOT found`) and
(ii) prepending a line to `Hyprland-ConfigActions.cpp` (shifting every `P19`/`P20` anchor by one)
both leave clauses (a)/(b) false while the six controls all still reject:

```
K1 pin quote rewritten + sums refreshed: full counter -> TARGET_MISSED (P22 quote absent; pin leg 3/4)
K2 pin shifted + sums refreshed:         full counter -> TARGET_MISSED (P19 1555-1559, P20 1577; pin leg 3/4)
```

My prototype catches both (quote leg / anchor leg, plus the frozen-hash leg). This is the input this
seat contributes that the frozen six do not test: **the pin-side mutation with a consistent sums
refresh**. It is not a predicate violation — the predicate's clauses (a)/(b)/(c) are exactly what
kill it — it is a gap in the frozen *control inventory* worth a v2 control if the L1 wants the
`controls=6/6` field to discriminate the quote/anchor legs rather than only the table leg.

**(c) A duplicate-row ordering hole in the entry itself.** `parse_entry` keyed by ID keeps the last
row for an ID. Measured:

```
good P19 row first, forged P19 row second -> prop=3 quote=4 anch=3 pin=4   (caught)
forged P19 row first, good P19 row second -> prop=4 quote=4 anch=4 pin=4   (ADMITTED)
```

because the later good row overwrites the earlier forged one. No frozen control covers a duplicate
row at all. The builder must require **exactly one row per P19–P22** (a cheap `ids.count == 4` plus a
duplicate check) — otherwise the verdict depends on row order and a stale/forged duplicate preceding
the true row is silently admitted. A stray `P23` row is harmless (measured `prop=4 quote=4 anch=4`).

Robustness edges worth pinning in the implementation (all measured):

- an unescaped `|` inside a Quote cell shifts every later cell (7 → 8 cells) and silently changes
  which cell is read as the quote; the counter must reject a row whose cell count is not 7, and must
  not "repair" it. An escaped `\|` is *not* unescaped by a naive `split("|")` either.
- reordered proposition rows are harmless (`P22,P19,P20,P21` → all legs 4/4): key on ID, never on
  row position.
- a non-breaking space inside the quote is collapsed by Python's Unicode `\s+` on the pin side but not
  in the verbatim quote, so it correctly misses; do not add NBSP folding, since that would make the
  judge whitespace-insensitive (Finding 2).
- an absent `SHA256SUMS` must yield `pins=0/4`, not a setup error (measured: `pins=0/4`).

## 8. Finding 6 (integration, harm-watch): landing the counter breaks PRED-C1-r51 unless a ledger row lands

`quality/counters/c1-r54-errata-truth.py` enters the round-51 ledger population
(`quality/tool-ledger.md`, PRED-C1-r51: every file under `quality/counters/*.py`). Measured in a
scratch clone at base:

```
before:  C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET
+ counter, no ledger row:
         detail: uncovered path=quality/counters/c1-r54-errata-truth.py
         C1_R51: population=83 ledger_rows=82 uncovered=1 ... checker=failed verdict=TARGET_MISSED   exit=1
+ counter + ledger row pointing at `.ufo/waves/round-54/registration.md`:
         detail: checker: LEDGER-ROW reason=bad_pointer ... detail=pointer-missing:.ufo/waves/round-54/registration.md
+ ledger row pointing at `.ufo/waves/round-54/claims-frozen.md` (at the freeze rev):
         C1_R51: population=83 ledger_rows=83 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET   exit=0
```

Two hard requirements follow. The pointer cell must name a file that **exists at the scored
revision** *and* whose bytes contain the instrument's **basename** as a name
(`check-tool-ledger.py:262-266,305-325`). `registration.md` does not contain the string
`c1-r54-errata-truth` (0 hits); `claims-frozen.md` does (2 hits) — so
`` `.ufo/waves/round-54/claims-frozen.md` `` is the working pointer, and `registration.md` is not.
At base `e25149fe` neither file exists (both land in the freeze commit), so the ledger row and the
counter must land in the same commit for the r51 counter to stay green at the final revision.

`bash tools/mado-verify.sh --selftest` was run once at base and prints
`MADO_SELFTEST: 460/460 assertions passed` — the frozen harm-watch value, unchanged by any of this
work (nothing was written to the lane).

## 9. Edge cases and open questions for the L1

1. **Quote judge ambiguity (blocking for an implementer, not for the claim).** `registration.md:51-53`
   as written ("exact byte contiguity … ONLY where the frozen quote itself carries a newline")
   excludes the normalization that clauses (a) and (b) jointly require. Reading (B) is the only
   self-consistent one; the counter must document it. If the L1 wants the literal reading instead,
   the frozen target is unreachable (`quotes=1/4` on the honest base) and the honest stop is a v2
   re-registration, not an edit (`claims-frozen.md:5-7`).
2. **`SHA256SUMS.txt` vs `SHA256SUMS`** (`registration.md:12` vs the actual `round-52/fetch/SHA256SUMS`).
   Naming the wrong file yields `pins=0/4` and a false miss.
3. **Absolute paths inside `SHA256SUMS`.** Match on basename only.
4. **No pin-side control.** The six frozen controls do not exercise clauses (a)/(b) against pin
   bytes; a self-consistent, quote-blind counter reaches `controls=6/6 verdict=TARGET_MET`. If the
   `controls=6/6` field is meant to certify the quote leg, a seventh control (pin rewrite with a
   refreshed sums file) is needed — that is a v2 question.
5. **Duplicate proposition rows** are unconstrained by the frozen table and the verdict depends on row
   order. Require exactly one row per ID.
6. **`--work` default.** The predicate's command (`claims-frozen.md:20`) passes no `--work`; the lane's
   own sterling precedent (`c1-r51-ledger.py:REFUSED_ROOTS`) treats a scratch root under `/tmp`,
   `/var/tmp` or `/dev/shm` as a hint, not a setup failure. My prototype follows that (default
   `mkdtemp` under `TMPDIR`, detail line if the resolved root is refused); a hard refusal there would
   make the default invocation exit 2.
7. **`rev=` in the printed line.** The frozen sentence writes `rev=<rev>`; print the fully resolved
   commit sha (as `c1-r51-ledger.py` prints `rev=<resolved>`), so a short-sha invocation is still
   deterministic and a grader comparing to the full hash matches.

## 10. Risk / status

- Predicate reachable: **yes**, demonstrated end to end at the honest base (`TARGET_MET`, exit 0,
  one stdout line, `controls=6/6` with each control's designated leg dropping).
- Frozen texts contradicted by the committed pins: the `verbatim` judge rule (§3) and the
  `SHA256SUMS.txt` file name (§6) — reported, not edited.
- Frozen control set under-covers clauses (a)/(b) (§7a) and duplicate rows (§7c) — reported as a v2
  candidate, not repaired here.
- Lane cleanliness: no lane file created, modified or deleted; `git status` unchanged by this seat
  (the two pre-existing modifications `corpus/README.md`, `corpus/SOURCES.md` and the untracked C2
  entry/lesson files belong to other seats). No tool was installed or updated, so there is no
  tool/version/channel record to report.

## 11. Artefacts (built in scratch, removed before yield as the seat spec requires)

The prototype that produced every measurement above is deleted with the scratch tree. Its exact
core is reproduced in Appendix A so the builder can lift it verbatim instead of re-deriving the four
traps in §3–§7. Harnesses `mutants.py` (eight general mutants) and `item2.py` (ten quote-leg
experiments) produced §3, §4, §6; the ordering/hash variants in §5, §7 were run as one-off probes
over the same `verify_core`.

## 12. Commands to re-run (for whoever lands the counter)

```
python3 -I quality/counters/c1-r54-errata-truth.py --repo . --rev e25149fec8152a3aabd2b18a0ee8663b23cf65aa
#   expect: MADO_ERRATA_TRUTH: rev=e25149fe... propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
#   expect: exit 0, exactly one stdout line
python3 -I quality/counters/c1-r54-errata-truth.py --selftest --repo . --rev <rev>
#   expect: selftest: >=30/>=30 passed ; selftest: 6/6 control red runs passed
python3 -I quality/counters/c1-r51-ledger.py --repo . --rev <rev> --work <scratch>
#   expect: population=<N+1> ledger_rows=<N+1> uncovered=0 verdict=TARGET_MET   (requires the ledger row)
bash tools/mado-verify.sh --selftest        # expect MADO_SELFTEST: 460/460 assertions passed
```

## Appendix A — the verified core (as run; lift as-is)

```python
import hashlib, os, re, subprocess        # stdlib only; the counter runs under `python3 -I`

def git_env():
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.setdefault("LC_ALL", "C.UTF-8")
    return env

def blob(repo, rev, rel):
    """Bytes of <rel> at <rev> from the object database, or None when absent.

    NEVER read the working tree: the frozen controls are mutated *trees*, so every input has to
    come from `--rev` (registration.md:36-38).
    """
    p = subprocess.run(("git", "-C", repo, "show", "%s:%s" % (rev, rel)),
                       capture_output=True, env=git_env())
    return p.stdout if p.returncode == 0 else None

def strip_code(cell):
    cell = cell.strip()
    return cell[1:-1] if len(cell) >= 2 and cell[0] == "`" and cell[-1] == "`" else cell

FROZEN = {  # registration.md:25-30, transcribed byte-for-byte
 "P19": dict(pin="Hyprland-ConfigActions.cpp", anchor="1554-1558",
   quote="g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); if (S.m_passPressed == 1) { "
         "if (!isMouse) g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, "
         "WL_KEYBOARD_KEY_STATE_PRESSED);",
   sha256="a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637"),
 "P20": dict(pin="Hyprland-ConfigActions.cpp", anchor="1576",
   quote="g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);",
   sha256="a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637"),
 "P21": dict(pin="Hyprland-legacy-DispatcherTranslator.cpp", anchor="619-622",
   quote="auto result = sendshortcut(modifiedArgs); if (keyState == 2 && result.success) "
         "result = sendshortcut(modifiedArgs);",
   sha256="7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771"),
 "P22": dict(pin="Hyprland-legacy-DispatcherTranslator.cpp", anchor="573-574",
   quote='if (!keycode) return {.success = false, .error = "sendshortcut: key not found"};',
   sha256="7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771"),
}
ORDER = ("P19", "P20", "P21", "P22")
SIDECLAIM = {"P19": (1554, 1558, None, None), "P20": (1576, 1576, None, None),
             "P21": (619, 622, 591, 627),    "P22": (573, 574, 571, None)}
PIN_HASHES = {  # registration.md:14-19, all four pins (P19..P22 name only two of them)
 "Hyprland-ConfigActions.cpp": "a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637",
 "Hyprland-ConfigActions.hpp": "746c6f517620eb039afbfbb9a4a0e2d5ba1c5eb117bcc8f396173f63091b7073",
 "Hyprland-KeybindManager.cpp": "8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40",
 "Hyprland-legacy-DispatcherTranslator.cpp":
     "7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771",
}
SUMS_REL, PINS_REL = ".ufo/waves/round-52/fetch/SHA256SUMS", ".ufo/waves/round-52/fetch"
ENTRY_REL = "corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md"


def collapse(text):
    """Reading (B): whitespace runs -> one space, with a per-character line map.

    The line of a collapsed space is the line the whitespace run STARTS on, which is what makes
    the recovered span (1554, 1558) rather than (1554, 1559).
    """
    out, linemap, line = [], [], 1
    for m in re.finditer(r"\s+|\S+", text):
        seg = m.group(0); start = line; line += seg.count("\n")
        if seg.strip() == "":
            if out and out[-1] != " ":
                out.append(" "); linemap.append(start)
        else:
            out.append(seg); linemap.extend([start] * len(seg))
    joined = "".join(out)
    a, b = 0, len(joined)
    while a < b and joined[a] == " ": a += 1
    while b > a and joined[b - 1] == " ": b -= 1
    return joined[a:b], linemap[a:b]


def locate(collapsed, linemap, quote):
    """Every verbatim contiguous occurrence, as a (start_line, end_line) span."""
    return [(linemap[m.start()], linemap[m.end() - 1])
            for m in re.finditer(re.escape(quote), collapsed)] if quote else []


def parse_entry(text):
    """{pid: (line_index, cells)} - 7 cells, keyed by ID, never by row position."""
    rows = {}
    for i, line in enumerate(text.split("\n")):
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) >= 7 and cells[0] in FROZEN:
            rows[cells[0]] = (i, cells)          # NOTE: last row wins - see §7c, forbid duplicates
    return rows


def anchor_of(cell):
    """'Hyprland-ConfigActions.cpp:1554-1558' -> (basename, '1554-1558'); pin names carry no ':'."""
    pin, anchor = os.path.basename(cell).rsplit(":", 1)
    return pin, anchor


def span_of(anchor):                              # '1576' or '1554-1558'
    a, _, b = anchor.partition("-")
    return int(a), int(b or a)


def parse_sums(text):                             # recorded paths are ABSOLUTE: key on basename
    out = {}
    for line in text.split("\n"):
        parts = line.split()
        if len(parts) >= 2:
            out[os.path.basename(parts[-1])] = parts[0]
    return out


def verify_core(repo, rev):
    """Measure the four legs at <rev> from git objects only."""
    r = dict(propositions=0, quotes=0, anchors=0, pins=0)
    entry_b = blob(repo, rev, ENTRY_REL)
    if entry_b is None:
        return r                                   # entry absent -> all legs 0
    rows = parse_entry(entry_b.decode("utf-8", "replace"))
    sums_b = blob(repo, rev, SUMS_REL)
    recorded = parse_sums(sums_b.decode("utf-8", "replace")) if sums_b else {}
    pins = {}

    for pid in ORDER:
        spec = FROZEN[pid]
        if pid not in rows:
            continue
        cells = rows[pid][1]
        pin_cell = strip_code(cells[4]); quote = strip_code(cells[5])
        entry_pin, entry_anchor = anchor_of(pin_cell)

        # -- the frozen table, byte-for-byte modulo trailing spaces (registration.md:21-23)
        if (entry_pin == spec["pin"] and entry_anchor == spec["anchor"]
                and quote.rstrip() == spec["quote"].rstrip()):
            r["propositions"] += 1

        # -- clause (a): resolve the pin from the ENTRY's cell, then locate the quote (reading B)
        if entry_pin not in pins:
            data = blob(repo, rev, "%s/%s" % (PINS_REL, entry_pin))
            pins[entry_pin] = data.decode("utf-8", "replace") if data else None
        if pins[entry_pin] is None:
            continue
        c, lm = collapse(pins[entry_pin])
        spans = locate(c, lm, quote)
        if not spans:
            continue
        r["quotes"] += 1

        # -- clause (b): exact span equality, then the side-claim
        want = span_of(entry_anchor)
        if want not in spans:
            continue
        lo, hi = SIDECLAIM[pid][2], SIDECLAIM[pid][3]
        if pid == "P22":
            if span_of(entry_anchor)[0] <= lo:      # must be strictly AFTER line 571
                continue
        elif lo is not None and not (lo <= want[0] and want[1] <= hi):
            continue
        r["anchors"] += 1

    # -- clause (c): recorded == frozen AND computed == frozen (both, per §6)
    for name, expected in PIN_HASHES.items():
        data = blob(repo, rev, "%s/%s" % (PINS_REL, name))
        if not data:
            continue
        if recorded.get(name) == expected and hashlib.sha256(data).hexdigest() == expected:
            r["pins"] += 1
    return r
```

Control mutations, exactly as `registration.md:42-47` words them (each applied to a clone of the
scored tree at a fresh commit, then re-measured with `verify_core`):

```python
CELL_PIN_ANCHOR, CELL_QUOTE = 4, 5

def mutate_entry_cell(text, pid, idx, fn):
    rows = parse_entry(text); lines = text.split("\n"); i = rows[pid][0]
    cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
    cells[idx] = fn(cells[idx])
    lines[i] = "| " + " | ".join(cells) + " |"
    return "\n".join(lines)

def control_mutation(control, repo, rev):
    entry = blob(repo, rev, ENTRY_REL).decode("utf-8", "replace")
    if control == "C1-CTL-1":       # splice P19's quote
        new = mutate_entry_cell(entry, "P19", CELL_QUOTE, lambda c: strip_code(c).replace(
            "if (S.m_passPressed == 1) { if (!isMouse)", ""))
    elif control == "C1-CTL-2":     # P20 anchor :1576 -> :1575
        new = mutate_entry_cell(entry, "P20", CELL_PIN_ANCHOR, lambda c: c.replace(":1576", ":1575"))
    elif control == "C1-CTL-4":     # P21 anchor :619-622 -> :573
        new = mutate_entry_cell(entry, "P21", CELL_PIN_ANCHOR, lambda c: c.replace(":619-622", ":573"))
    elif control == "C1-CTL-5":     # drop the P22 row
        lines = entry.split("\n"); del lines[parse_entry(entry)["P22"][0]]
        return ENTRY_REL, "\n".join(lines).encode()
    elif control == "C1-CTL-6":     # P19 pin -> KeybindManager.cpp
        new = mutate_entry_cell(entry, "P19", CELL_PIN_ANCHOR, lambda c: c.replace(
            "Hyprland-ConfigActions.cpp", "Hyprland-KeybindManager.cpp"))
    elif control == "C1-CTL-3":     # one hex nibble of a recorded sha256
        sums = blob(repo, rev, SUMS_REL).decode("utf-8", "replace").split("\n")
        for i, line in enumerate(sums):
            if line.strip().startswith(PIN_HASHES["Hyprland-ConfigActions.cpp"]):
                d = list(line.split()[0]); d[-1] = "0" if d[-1] != "0" else "1"
                sums[i] = "".join(d) + line[64:]; break
        return SUMS_REL, "\n".join(sums).encode()
    return ENTRY_REL, new.encode()
```

Report: `.ufo/waves/round-54/w1/R54Seat02.md`
