# ExecIndepA — C1 independent implementation (mado round 45, w1)

Seat: `ExecIndepA`. Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` (mado-shokunin, desktop/compositor craft).
Scope: C1's contract only (operability, capability acquisition: `tools/mado-monitors.py`). C2 untouched.

## Status

**Done.** An independent implementation of the PRED-C1-r45 contract scores **49/49 fixtures at seeds 45, 7
and 1234**, selftest **70/70**, read-only **ok**, at a scratch-clone commit — i.e. **TARGET_MET** three times.
Base is 0/49. No lane file was edited; the only lane artefacts are this report, the draft tool and the
receipts under my seat directory.

## Independence method

The contract source was **only** the reference docstring. The reference file is 532 lines; I extracted the
docstring with `ast.get_docstring` and never read below it:

```
python3 - <<'EOF'
import ast
t=ast.parse(open('.ufo/waves/round-45/l1-draft/mado-monitors.py').read())
print(ast.get_docstring(t, clean=False))
EOF
```

I did read the **frozen counter** (`quality/counters/c1-r45-monitors.py`, clauses a/s/f/r, FIXTURES list,
seed substitution, harness) — it is the objective test set and a different frozen file, not the reference
implementation. Everything semantic below comes from the docstring; the counter told me only *which cases*
are tested, never how the reference computes them.

The implementation is python3 stdlib only (`json, math, os, re, stat, struct, sys, fractions`) —
`mado-monitors.py:7-14` — starts no process, opens no socket, writes nothing.

## Evidence (all paths relative to this seat directory)

| Check | Command | Result | Receipt |
|---|---|---|---|
| selftest | `python3 -I mado-monitors.py --selftest` (env `PATH=/usr/bin:/bin`, fresh HOME) | `MADO_MONITORS_SELFTEST: 70/70 passed`, rc 0 | transcript; 70 assertions on parsed rules, rule storage, matcher, scale correction, verdicts and setup reasons |
| fixtures, seed 45 | `python3 -I <lane>/quality/counters/c1-r45-monitors.py --repo <clone> --rev HEAD --work <scratch>/w` | `fixtures=49/49 selftest=ok readonly=ok tool=present verdict=TARGET_MET` rev `d3920089e0e250dbf82ebdd9ed5f0909891142d2` seed 45 | `receipts/c1-final-seed45.txt` |
| fixtures, seed 7 | same, `--seed 7` | `49/49 … TARGET_MET` rev `d3920089…` seed 7 | `receipts/c1-final-seed7.txt` |
| fixtures, seed 1234 | same, `--seed 1234` | `49/49 … TARGET_MET` rev `d3920089…` seed 1234 | `receipts/c1-final-seed1234.txt` |
| base (negative) | `--repo <lane> --rev 0c89478af821a6424c9ac922eafe02e39630cf4f` | `fixtures=0/49 selftest=fail readonly=fail tool=absent verdict=TARGET_MISSED` | `receipts/c1-base-zero.txt` |
| tool hash | `sha256sum mado-monitors.py` | `1b8545c0b6a58b29b13e89db87c5ec79a3ffbe66b4bb84db991eec23f56c4982` (equals `git show HEAD:tools/mado-monitors.py \| sha256sum` in the clone) | `receipts/tool-sha256.txt` |
| live host, read-only | `hyprctl monitors all -j` + `--config ~/.config/hypr/monitors.conf`, projected shape-only | `MADO_MONITORS: lines=1 rules=1 … outputs=1 matched=1 agree=1 differ=0 disabled=0 verdict=OK` — reproduces the L1 receipt (AGREE, OK) at Hyprland 0.56.2 efb50993 | `receipts/live-host-projected.txt` (names/selectors redacted; no serials, descriptions or titles kept) |

Clone recipe (scratch only): `mktemp -d -p /fast/scratch/hyaku/mado-r45/ExecIndepA clone.XXXXXX`,
`git clone -q --shared --no-checkout <lane>`, `git rev-parse --show-toplevel` asserted equal to the clone,
`git checkout -q --detach 22a8dedd02f507689c567777e0f20b5e645c8ce0`, tool copied to `tools/mado-monitors.py`,
committed with `-c user.name=seat -c user.email=seat@scratch.invalid`. Scoring rev `d3920089…` is the
scratch commit; the lane index and the fleet repo were never touched.

## Every failing fixture observed, verbatim

All failures came from my own file; each is reproduced by a **deliberately broken variant** committed in its
own scratch clone, so the failure text is reproducible rather than recalled. Variants were produced by one
mechanical edit of the final file (receipts name the edit). In both variant runs `selftest=fail` as well,
because the fixed selftest inside each variant asserts the corrected semantics — that is expected, the
fixture lines are what the variant run is for.

### A. `rules=` read as "rule additions" (4 failures) — `receipts/variant-rules-adds-seed45.txt`, rev `8dd9866393b3c34c3e1f6d967b32078226e8c9dd`

```
PRED-C1-r45 clause=f fixture=transform-modifier FAIL rc=0 want_rc=0 stderr=0 got='MADO_MON_RULE: n=1 sel="eDP-7" mode=1920x1080@60.00 pos=0x0 scale=1.0000 transform=3 mirror=- disabled=false\nMADO_MON_OUTPUT: name="eDP-7" rule=1 differ=- verdict=AGREE\nMADO_MONITORS: lines=2 rules=2 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK\n'
PRED-C1-r45 clause=f fixture=same-selector-erases FAIL rc=0 want_rc=0 stderr=0 got='MADO_MON_RULE: n=1 sel="DP-5" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false\nMADO_MON_OUTPUT: name="DP-5" rule=1 differ=- verdict=AGREE\nMADO_MONITORS: lines=2 rules=2 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK\n'
PRED-C1-r45 clause=f fixture=readd-moves-last FAIL rc=0 want_rc=0 stderr=0 got='n=2 sel="desc:Dell Inc. 6AHUHV" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false\nMADO_MON_OUTPUT: name="DP-5" rule=2 differ=- verdict=AGREE\nMADO_MONITORS: lines=3 rules=3 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK\n'
PRED-C1-r45 clause=f fixture=two-files-later-overrides FAIL rc=0 want_rc=0 stderr=0 got='MADO_MON_RULE: n=1 sel="DP-5" mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0 mirror=- disabled=false\nMADO_MON_OUTPUT: name="DP-5" rule=1 differ=- verdict=AGREE\nMADO_MONITORS: lines=2 rules=2 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=1 differ=0 disabled=0 verdict=OK\n'
```

`got` is correct on every other field; only `rules=` differs (`2` vs `1`, `3` vs `2`).

**Deciding sentence:** "Rules are numbered n=1.. in the final list." plus the summary field
"`rules=<n>`" — read with the fixture, `rules` is the size of the **final** rule list, not the number of
additions. The contract never says this in words; the fixtures decide it. **My file was wrong.**

### B. missing the `K/120` branch of the scale correction (1 failure) — `receipts/variant-no-k-branch-seed45.txt`, rev `e12d2dd7cbc4c90e4392d40ccd9f81cda5637c87`

```
PRED-C1-r45 clause=f fixture=scale-1.6 FAIL rc=1 want_rc=0 stderr=0 got='N_RULE: n=1 sel="DP-5" mode=2880x1920@120.00 pos=0x0 scale=1.6000 transform=0 mirror=- disabled=false\nMADO_MON_OUTPUT: name="DP-5" rule=1 differ=scale verdict=DIFFER\nMADO_MONITORS: lines=1 rules=1 v2=0 unsupported=0 badrules=0 outputs=1 matched=1 unruled=0 agree=0 differ=1 disabled=0 verdict=DIFFER\n'
```

(the leading `MADO_MON_RU` is clipped by the counter's own 300-character `got` window; the rest of the line is
byte-for-byte what the counter printed, `awk 'length($0)'` = 377).

**Deciding sentence:** "else, with K = round-half-up(S*120), K/120 when it divides both; else the first of
(K+i)/120, (K-i)/120 for i = 1..89 that divides both". My first draft jumped straight to the `K±i` loop and
never tried `K/120`, so 1.6 was "corrected" to a farther divisor found at some `i ≥ 1`. **My file was wrong**;
the loop's `i` starts at 1 and K itself is a separate candidate.

(The first scoring round, before these two fixes, was `fixtures=44/49`. Reproduced exactly by a variant
holding **both** defects — rev `759aba4a0e448ae019b0b298895b206084e705b8`, `receipts/variant-combined-seed45.txt`
— whose five failures are `readd-moves-last`, `same-selector-erases`, `scale-1.6`, `transform-modifier`,
`two-files-later-overrides` (`receipts/variant-combined-failures.txt`, sorted): the A set plus B, and nothing
else. So these five are the complete set of fixtures that ever failed for me; the final file passes all 49 at
three seeds.)

## Sentences I had to read twice

Format: quote [id · locator] → reading 1 / reading 2 → decider. Every quote is <= 25 words and every
locator is `ref:NN` in `l1-draft/mado-monitors.py`, computed by `verify-quotes.py` from `ast.get_docstring`
(receipt `receipts/quote-check.txt`: `MADO_QUOTES: checked=16 bad=0`); the script also greps the docstring
for each fragment and asserts the fragment is present in this report, so no locator below is typed by hand.

1. "Adding a rule erases every earlier rule with the same selector and appends it." [Q1 · ref:55] +
   "The first rule in the current list whose selector equals SEL is copied with that transform and the copy
   is added" [Q2 · ref:38].
   R1: the `transform` modifier appends a copy and leaves the original in place. R2: "the copy is added" means
   the normal add, i.e. the original is erased first, so the transformed rule is the only one.
   **Decider:** `transform-modifier` (one rule at `n=1`, `rules=1` over two lines).

2. "`addreserved` … If a rule with selector SEL exists nothing changes (the reserved area is not compared)"
   [Q3 · ref:41].
   R1: "nothing changes" still counts as a rule for `rules=`. R2: no add at all.
   **Decider:** `addreserved-keeps-rule` (`rules=1` over two lines).

3. "Rules are numbered n=1.. in the final list." [Q4 · ref:55] against the summary field `rules=<n>`.
   R1: number of rules ever added. R2: final list size.
   **Decider:** `readd-moves-last` (`lines=3 rules=2`). See failure A.

4. "field 1 `transform`: field 2 must be one digit 0-7, else the line adds one to `badrules`." [Q5 · ref:38]
   vs "A MODE, POSITION, SCALE or transform VALUE outside these forms makes the line `unsupported` (not
   modelled)." [Q6 · ref:53].
   R1: a bad `transform` **value** in the KEY position is `badrules` (same word as the modifier).
   R2: only the field-1 modifier is `badrules`; the `transform, 9` KEY form is `unsupported`.
   **Decider:** `transform-modifier-bad` decides only the field-1 form (`badrules=1`). The KEY form has
   **none** — a hole (see below); I implemented R2, which is the sentence's literal reading ("transform
   VALUE … makes the line unsupported").

5. "`hyprctl monitors all -j` reports each output's live state" + "live_disabled is `disabled` == JSON true"
   [Q7 · ref:64].
   R1: the dump's `disabled` is a boolean flag to trust as-is (missing → disabled). R2: only the JSON literal
   `true` counts; a missing or non-boolean `disabled` is enabled.
   **Decider:** `disabled-but-live` / `live-disabled` cover `false`/`true` only; the missing-key case has
   **none**. I implemented R2 (`mon.get("disabled") is True`).

6. "A live value that is missing or of the wrong JSON type (… integers for width, height, x, y, transform,
   id … a string for mirrorOf; booleans are never numbers) fails its field." [Q8 · ref:78].
   R1: `id` is the only place where type matters for mirror, so a Python `int`-like float would be fine.
   R2: `id` must be an integer; `mirrorOf` must be a string; `True`/`False` are never integers.
   **Decider:** `wrong-types` decides `x="0"` and `transform=true` (`differ=position,transform`); the `id`
   and `mirrorOf` halves have **none**. I implemented R2.

7. "… the expected scale E is Hyprland's correction of S for the live `width` and `height` … else, with
   K = round-half-up(S*120), K/120 when it divides both; else the first of (K+i)/120, (K-i)/120 for i = 1..89"
   [Q9 · ref:71] and "none found means the scale is not compared" [Q10 · ref:73].
   R1: "not compared" = the field fails (nothing to agree with). R2: "not compared" = the field is skipped.
   **Decider:** **none**. I implemented R2. Note this branch is hard to reach: `K/120 = 1.0` divides every
   integer pixel size and 120 lies inside `[K-89, K+89]` for S ≲ 1.74, so a "none found" case needs a
   scale above ~1.74 and unlucky dimensions (e.g. S=2.0 with 3440x1441).

8. "S (a 32-bit float; S < 0.25 becomes 1.0, as Hyprland's parser does)" [Q11 · ref:52] and "RATE (the
   number after `@` rounded to a 32-bit float, else 60)".
   R1: "32-bit float" is a storage note that only affects printing. R2: the value must be rounded through
   IEEE-754 binary32 before it feeds the K computation / the 1.0 closeness test.
   **Decider:** **none** — no fixture distinguishes binary32 from binary64: `f32(1.3)*120 = 155.99999…`
   and `1.3*120 = 156.00000000000003` both give K=156, `f32(1.6)*120` and `1.6*120` both give 192, and both
   `f32(99.997)` and `99.997` are within 1.0 of the live rates used. I applied R2 (`struct` binary32), since
   it is the literal text and cannot hurt a value printed at 2/4 decimals.

9. "two-token form only; anything else is usage" [Q12 · ref:24], then "`--monitors V` exactly once and
   `--config V` one or more times, in any order".
   R1: a value that itself starts with `--` is a value. R2: a value that looks like an option is usage.
   **Decider:** **none** (`setup-usage` only covers a missing `--config`). I implemented R1 (any token is a
   value; only the flag position is checked).

10. "NO_RULES (exit 4, lines = 0 and v2 = 0)" [Q13 · ref:85] against "NOT_COMPARED (exit 5, v2 > 0 or
    unsupported > 0 …)".
    R1: `lines = 0` alone is NO_RULES (the v2 clause is redundant because a `monitorv2` line usually carries
    no `=`). R2: NO_RULES needs both; a file with `monitorv2 {` and no `monitor =` line is NOT_COMPARED.
    **Decider:** **none** — `monitorv2` fixture has `lines=1`. I implemented R2, the literal parenthesis.

11. "A line whose first token (up to a space, tab, `=` or `{`) is `monitorv2` adds one to `v2`." [Q14 · ref:32].
    R1: the token is the first *whitespace-free* word. R2: the token ends at the first of those four
    characters, so `monitorv2=1` and `monitorv2{` are also `monitorv2`.
    **Decider:** **none** — the fixture uses `monitorv2 {`. I implemented R2.

12. "KEY VALUE pairs from field 4 while the key field is not" [Q15 · ref:44] and "any other key adds one to
    `badrules` and the rule is not added", against 'field i is "" past the end' [Q16 · ref:36].
    R1: a trailing key with no value is an unknown/incomplete key → `badrules`. R2: its value is "" by the
    "field i is "" past the end" rule, so e.g. `mirror,` would set the mirror to the empty name.
    **Decider:** **none**. I implemented R2 for `mirror` (empty name) and `unsupported` for `transform,`
    (the "" value fails the digit test).

## Contract holes found (no fixture decides; candidates for a v2 re-registration note)

- `rules=` is defined only by fixtures, never by a docstring sentence (failure A would have been avoided by
  one clause; Q4 says only how rules are *numbered*).
- `transform, <bad>` in KEY position: `unsupported` vs `badrules` (sentence 4).
- scale "none found means the scale is not compared": pass vs fail (sentence 7) — and the branch is nearly
  unreachable because `1.0` divides any integer pixel size.
- binary32 rounding is unobservable in all 49 fixtures (sentence 8).
- `disabled` missing / non-boolean on a dump element (sentence 5).
- `id` / `mirrorOf` type failures (sentence 6): only the `x`/`transform` halves of "wrong-types" are tested.
- `lines = 0` with `v2 > 0` (sentence 10); `monitorv2=` / `monitorv2{` without a space (sentence 11).
- a trailing KEY with no VALUE (sentence 12); a line whose unknown key and invalid MODE co-occur (my code
  counts `unsupported` only — untested).

## Risks

- Residual (declared by the registration, and true here): a tool holding a model of the contract is an
  implementation of it. Passing 49/49 says my file agrees with the contract's cases, not that the contract
  matches Hyprland beyond the pins.
- My scratch-clone commit (`d3920089…`) is not the lane's data commit; the L1 integrates. If the L1 prefers
  the reference file, this file is still the independent second reading the wave asked for — the diff between
  them is a direct measure of contract ambiguity (the holes above are where I would expect the two to differ
  silently).
- Live check used only allowed reads (`hyprctl monitors all -j`, `hyprctl version`) against the host's own
  config; the receipt keeps the verdict and summary only (no names, selectors, serials, descriptions).

## Files in this seat

- `w1/ExecIndepA/mado-monitors.py` — the independent tool (625 lines, sha256 above). The L1 copies it to
  `tools/mado-monitors.py`; nothing else is needed.
- `w1/ExecIndepA/verify-quotes.py` + `receipts/quote-check.txt` — the quote/locator binder for this report.
- `w1/ExecIndepA/variant-*.py` — the deliberately broken variants behind the verbatim failure lines above
  (`rules-adds`, `no-k-branch`, `combined`); they are evidence, not deliverables.
- `w1/ExecIndepA/receipts/` — counter runs (three seeds + base), the two variant runs, the combined run,
  the tool hash, the score rev and the shape-only live projection.
- `w1/ExecIndepA.md` — this report.

## Tools installed

None. No pacman, no network fetch, no new package; python3 stdlib only.

## Scratch

`/fast/scratch/hyaku/mado-r45/ExecIndepA/` (clones, `w/`, selftest HOME) — deleted at the end of the seat;
all citable receipts were copied into `receipts/` first.
