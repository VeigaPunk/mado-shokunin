# C2 forgeries — PRED-C2-r41-v1 (`quality/counters/c2-r41-focus-entry.py`, frozen)

Seat `CritC2Cheat`, wave w1, round 41. Nine fixture repos, each a throwaway
`D=$(mktemp -d)` with `git -C D init -q`, the throwaway identity passed by `-c`,
`git -C D rev-parse --show-toplevel` checked equal to `D` before the first
commit, and every later git call naming `-C D`. Builders are imported from
`.ufo/waves/round-41/ctl/run-c2-controls.py` (`main` never run); the frozen
counter runs as `python3 -I quality/counters/c2-r41-focus-entry.py --repo D --rev
A --base B`. The tightenings below are evaluated on the same committed bytes by
`tighten.py`, which imports the frozen counter's own parsers (`section`,
`unfenced`, `registry`, `norm`, `journal_counts`, `GATE_RE`, …) and adds only
the named rule.

Seat files (all under `.ufo/waves/round-41/w1/CritC2Cheat/`): `build-forgeries.py`,
`tighten.py`, `verify-quotes.py`, `harness.log`, `pins.log`, `quotes.log`,
`forgeries.json`.

## Result

All nine fixtures are admitted by the frozen counter (`admitted=1/1`, exit 0).
Eight are forgeries. The ninth is a **GENUINE-PROXY**: the real fetch bytes
(`.ufo/waves/round-41/fetch/`, sha256-identical) plus the real journal counts,
and it is the control that every proposed tightening must keep admitting.

```
GENUINE-PROXY                rc=0 admitted=1/1 verdict=TARGET_MET    new_bytes=63734  tighten_fail=none
F1-invented-receipts-512     rc=0 admitted=1/1 verdict=TARGET_MET    new_bytes=23106  tighten_fail=T1,T4,T6
F2-invented-journal          rc=0 admitted=1/1 verdict=TARGET_MET    new_bytes=49179  tighten_fail=T1,T2
F3-absent-package-paths      rc=0 admitted=1/1 verdict=TARGET_MET    new_bytes=63706  tighten_fail=T3
F3b-space-only-refuse-reason rc=0 admitted=1/1 verdict=TARGET_MET    new_bytes=63706  tighten_fail=T3
F4-localized-redirect        rc=0 admitted=1/1 verdict=TARGET_MET    new_bytes=69619  tighten_fail=T1,T4,T6
F5-shared-boilerplate-quote  rc=0 admitted=1/1 verdict=TARGET_MET    new_bytes=64040  tighten_fail=T1,T2,T5
F6-one-char-location         rc=0 admitted=1/1 verdict=TARGET_MET    new_bytes=64819  tighten_fail=T1,T4,T6
F7-two-new-ids               rc=0 admitted=1/1 verdict=TARGET_MET    new_bytes=23938  tighten_fail=T1,T2,T4,T6,T7

single-tightening matrix (X = refused by that tightening alone):
fixture                      T1  T2  T3  T4  T5  T6  T7
GENUINE-PROXY                .   .   .   .   .   .   .
F1-invented-receipts-512     X   .   .   X   .   X   .
F2-invented-journal          X   X   .   .   .   .   .
F3-absent-package-paths      .   .   X   .   .   .   .
F3b-space-only-refuse-reason .   .   X   .   .   .   .
F4-localized-redirect        X   .   .   X   .   X   .
F5-shared-boilerplate-quote  X   X   .   .   X   .   .
F6-one-char-location         X   .   .   X   .   X   .
F7-two-new-ids               X   X   .   X   .   X   X
FORGE_SUMMARY fixtures=9 admitted=9/9 genuine_proxy_clean=1
```

The genuine proxy's receipts are the frozen bytes (`pins.log`: nine
`pinned=1` lines, e.g. `focus-grab-v1.xml bytes=5447
sha256=0bc60c14d27f9079e0d1d9d706f91e67ad7da585f3b7f34ff7186a376c0285b4
pinned=1`), its journal line is the counter's own parse of
`fetch/xdph-journal.txt` — `journal sessions=2 adverts=78 interfaces=63
focus_grab=1` — and its six quotes each occur in exactly one fetch file
(`quotes.log`: `QUOTE_CHECK quotes=6 unique_ok=6/6`).

## Forgeries

### F1 — invented receipts at the 512-byte floor (1 536 forged bytes)

Three receipts of **exactly 512 bytes** each (`S301.html` 512 B, `S303.html`
512 B, `S304.html` 512 B), no relation to any upstream artifact, body = a
4-word sentence repeated; the journal row keeps the real journal so clause h is
satisfied. Entry 364 B, registry 1 034 B, lesson 952 B.

* Clauses that should have caught it: **d** (the receipt is the evidence) and
  **b/d** together (nothing ties the quote to the claim).
* Why they don't: d tests only `len(blob) >= 512`, the declared sha256, quote
  length 3–25 words, path/sha/quote distinctness, and `quote ⊆ norm(blob)`.
  `MIN_RECEIPT` is a size floor, not a content check; the docstring declares
  exactly this residual.
* Tightening: **T1** (frozen receipt pins). `T6` also refuses it, as a
  heuristic only.

### F2 — an invented journal that parses to the entry's line (4 691 B)

Two fabricated sessions (`-- Boot abc000…`, `-- Boot abc001…`), 40 adverts
naming `invented_iface_00…18` plus one `hyprland_focus_grab_manager_v1`, host
`h`, timestamps `2026-10-25T09:10:00+00:00` — no such bytes were ever in a
journal. Entry 701 B. The counter's own parser returns
`(2, 40, 20, 1)` and clause h compares the entry's line to that.

* Clause that should have caught it: **h** (the own-work receipt is a saved
  journal of *this host*).
* Why it doesn't: h parses whatever bytes the Gate line points at. Nothing
  checks that the journal is the host's, that the interface names are real
  globals, or that the timestamps are in a boot that happened; the declared
  residual covers "an invented journal that parses to counts the entry
  repeats".
* Tightening: **T2** (own-work receipt must be the pinned journal file, and the
  counts are recomputed from the pinned bytes) — also **T1**.

### F3 — ADMIT/REFUSE naming files that do not exist (0 forged receipt bytes)

The lesson's assimilation pair is rewritten to
`ADMIT merge/mado/knowledge/corpus/knowledge/no-such-entry-r99.md as
corpus/knowledge/hyprland-focus-grab-r41.md` (111 B) and
`REFUSE merge/mado/knowledge/corpus/knowledge/absent-r98.md reason=generic
wayland security analysis, not a measurement` (118 B). Neither path exists in
the staged package. All six receipts are the genuine bytes: the forgery is the
paperwork alone.

* Clause that should have caught it: **i** (the assimilation set is recorded
  "for the non-author closure to spot-check").
* Why it doesn't: `ADMIT_RE`/`REFUSE_RE` match the line and nothing resolves
  the path. The counter never reads the staged package
  (`/home/vgpnk/Projects/shokuknow/merge/mado`, read-only) or any manifest of
  it, so any string of the right shape passes. This is **not** covered by the
  declared residual, which is about receipt bytes vs their location.
* Tightening: **T3** (both paths must be members of the frozen two-entry
  staged-package allowlist; the staged files are 3 828 B and 1 765 B —
  `pins.log`).

### F3b — a REFUSE reason of 24 spaces (109-byte line, 0 words)

`REFUSE …privileged-client-surface-r29.md reason=` followed by 24 spaces. The
line is 109 B; `reason=` content is zero words.

* Clause that should have caught it: **i** (`reason=<text of >= 20
  characters>`).
* Why it doesn't: `REFUSE_RE = ^REFUSE (\S+\.md) reason=(.{20,})$` (`c2-r41-focus-entry.py:90`) — `.`
  matches spaces, and the line is matched after `splitlines()`, so the trailing
  run is preserved.
* Tightening: **T3** (`len(reason.split()) >= 4`).

### F4 — the localized channel behind a redirect (6 120 B)

`S287`'s location becomes `https://t.co/9xQ2fG` (20 B) and its receipt becomes
6 120 B of Japanese blog text whose quote is
`フォーカス グラブ マネージャ の 広告` (5 whitespace-separated tokens, so d's
3–25 word test passes). Entry 692 B.

* Clause that should have caught it: **i**'s last conjunct (no cited location
  contains `amgsk.dev`, `zhihu`, `/zh`, `/ja`: the localized-documentation
  channel is outside the province (`PROVINCE.md:75`)).
* Why it doesn't: the guard is four literal substrings
  (`c2-r41-focus-entry.py:91`) tested against cell 1 only (`:312`). A redirector
  URL carries none of them; the localized bytes live in the receipt, which the
  guard never reads. The literal list also misses `/jp/`, `qiita.com`,
  `zenn.dev`, and percent-encoded forms.
* Tightening: **T4** (percent-decode the location; reject redirector hosts;
  reject a localization-segment list including `/jp/`; require the receipt to be
  ≥ 90 % ASCII; require receipt content type to match the location extension) —
  and **T1**, which is decisive once receipts are pinned.

### F5 — one shared boilerplate sentence carries every quote (708 B shared)

The 118-byte footer `Fetched by the round 41 lane fetch harness on 2026-10-25
and frozen for the wave; do not edit these bytes by hand.` is appended to all
six receipts; the six Gate quotes are six different substrings of that footer
(`Fetched by the round 41 lane fetch harness`, `frozen for the wave; do not
edit these bytes`, `do not edit these bytes by hand`, `the round 41 lane fetch
harness on 2026-10-25`, `round 41 lane fetch harness on 2026-10-25 and
frozen`). Entry 558 B. Every "observation" in the entry is therefore the same
provenance sentence; none of them says anything about focus-grab.

* Clause that should have caught it: **d** (distinct quotes) and **g** (one
  entry line per id carrying its quote).
* Why it doesn't: d requires paths, sha256s and quotes to be distinct, but only
  tests `quote ⊆ this receipt`. A quote that is a substring of a footer shared
  by all receipts is distinct from its siblings and present in its own receipt;
  g then finds it on the entry line. Nothing asks the quote to be *exclusive* to
  its receipt.
* Tightening: **T5** (each quote occurs in its own receipt and in **no other
  cited receipt**). Feasible on the genuine set: the six genuine quotes are each
  unique across all nine fetch files (`quotes.log`).

### F6 — a cited row one character from the held row (840 B)

A new row `S289` with location `https://example.org/confiq.cpp`, one character
from the held row's `https://example.org/config.cpp`, cited by the entry with an
840-byte receipt `S289.txt` whose content is `near duplicate source body.` ×30.
Entry 741 B.

* Clause that should have caught it: **e** (a new id's location occurs in no
  other registry row).
* Why it doesn't: e compares the last whitespace token for exact equality (`:271`), so a
  one-character variant is a "distinct source". Nothing binds the location to
  the receipt's bytes, so the variant need not resolve to anything.
* Tightening: **T6** (the location's last path segment, percent-decoded and
  query-stripped, must be a substring of the Gate receipt's basename; own-work
  must name the receipt path itself) — and **T1**.

### F7 — two new ids: code tests `>= 2`, docstring says `>= 3` (2 365 B)

Base holds two rows (`S050`, `S051`); the entry cites both plus `S301` and
`S302`, so `new_ids = [S301, S302]`. The counter's clause c computes
`cl["c"] = int(rows_ok and len(new_ids) >= 2)` (`c2-r41-focus-entry.py:225`) and admits; the docstring says
"ids absent from the BASE registry (**at least 3**)". Registry 929 B, entry
419 B, invented receipts 792 + 791 + 782 B.

* Clause that should have caught it: **c** as written in the docstring, which
  the registration declares to be the predicate ("the docstring … IS the tool's
  contract").
* Why it doesn't: the code and the docstring disagree; the code is the one that
  runs.
* Tightening: **T7** (`len(new_ids) >= 3`). The genuine proxy has six new ids,
  so it is unaffected.

## Proposed tightenings (minimal additions to the frozen counter)

Each is a small rule over data the counter already reads; `tighten.py` is the
executable form, and the matrix above is the evidence. `PIN_RECEIPTS` is the
nine-entry sha256 table of the frozen fetch dir, verified against disk by
`python3 -I tighten.py --verify-pins` (`pins.log`, nine `pinned=1`).

| # | rule | closes | genuine-set evidence |
|---|---|---|---|
| T1 | every cited Gate receipt is `fetch/<basename>` with `basename` in `PIN_RECEIPTS` and `sha256(blob)` equal to its pin | F1, F2, F4, F5, F6 | GENUINE-PROXY passes (its receipts are those bytes) |
| T2 | the own-work id's receipt path is `fetch/xdph-journal.txt`, its sha256 is the pin, and the counts are recomputed from those bytes | F2 | GENUINE-PROXY: `(2, 78, 63, 1)` from the pinned bytes |
| T3 | ADMIT and REFUSE paths ∈ frozen staged-package allowlist; `len(reason.split()) >= 4` | F3, F3b | `focus-control-surfaces-r28.md` (3 828 B) and `privileged-client-surface-r29.md` (1 765 B) exist |
| T4 | percent-decode the location; reject redirector hosts; reject `amgsk.dev`/`zhihu`/`qiita.com`/`zenn.dev`/`/ja/`/`/jp/`/`/zh*/`/`/ko/`/`/tw/`; receipt ≥ 90 % ASCII; receipt content type matches the location extension (`.xml`→`<?xml`, `.cpp`/`.hpp`→`#include`/`#pragma`, `.html`→`<html`, `.md`→`# `, extensionless→HTML) | F4 | all six genuine receipts are 100 % ASCII and match their types |
| T5 | each quote occurs in its own receipt and in no other cited receipt | F5 | six genuine quotes, each in exactly one of the nine files (`quotes.log`) |
| T6 | location's last path segment (percent-decoded, query-stripped) is a substring of the Gate receipt's basename; own-work must name the receipt path | F1, F4, F6 (heuristic) | fetch names are repo-prefixed, so substring (not equality) is required |
| T7 | `len(new_ids) >= 3`, per the docstring | F7 | GENUINE-PROXY has six |

T1 is the load-bearing correction: with the nine receipt sha256s pinned in the
counter (frozen before any data commit, like `receipts/freeze-counter-check.txt`
pins paths), a data-phase seat can no longer mint receipt bytes, and F1, F4, F5,
F6 and F7's synthetic receipts all die at once. T2–T7 are independent and each
keeps the genuine proxy admitted on its own (matrix row `GENUINE-PROXY`).

## Tightenings considered and rejected as unsafe

* **Near-duplicate locations by edit distance 1** (the obvious answer to F6)
  rejects the genuine set: `fetch/Hyprland-FocusGrab.cpp` and
  `fetch/Hyprland-FocusGrab.hpp` differ in exactly one character (`c`→`h`), and
  their real locations `…/src/protocols/FocusGrab.cpp` / `…/FocusGrab.hpp` also
  differ by one. Both are legitimately cited sources.
* **Location basename == receipt basename** rejects the genuine set: the fetch
  dir prefixes the repo (`Hyprland-FocusGrab.cpp`, `quickshell-grab.cpp`,
  `xdph-PortalManager.cpp`) while the upstream path is `src/protocols/
  FocusGrab.cpp`, `…/focus_grab/grab.cpp`, `src/core/PortalManager.cpp`;
  equality is false, substring is true. T6 therefore uses substring.
* **Requiring the receipt to mention `focus_grab`** rejects the genuine portal
  receipt: `grep -c -i 'focus[_-]grab' fetch/xdph-PortalManager.cpp` = 0 (the
  portal binds the manager generically, via `Got interface`). A subject-token
  rule is not available.
* **Raising `MIN_RECEIPT`** does not close F1: the floor is a size, and F1 shows
  a 512-byte body passes; a forger pads. (Genuine minimum is 1 903 B —
  `protocols-README.md`.)

## Counter defects found beyond the declared residual

1. **c: code ≠ docstring.** `len(new_ids) >= 2` (`:225`) vs "at least 3" in
   the docstring. The registration declares the docstring the predicate, so the
   running code admits a narrower assimilation than registered (F7).
2. **i: the assimilation pair is unresolvable.** ADMIT/REFUSE are regex-matched
   and never resolved against the staged package (F3); the closure is the only
   defence and it is not told what the set must contain.
3. **i: `REFUSE_RE` accepts whitespace.** `reason=(.{20,})$` admits 24 spaces
   (F3b).
4. **i: the province guard is a four-literal substring test on cell 1.** A
   redirector URL, a `/jp/` path, or localized receipt bytes evade it (F4).
5. **e: exact-token equality only**, with no binding of location to receipt
   (F6).
6. **d: the quote test is one-directional.** `quote ⊆ receipt` with
   distinctness, but no exclusivity, so shared boilerplate carries every quote
   (F5).

## Residual after T1–T7

T1–T7 close fabrication of *bytes* and *paperwork*. They do not close the
semantic gap: a cited frozen receipt can be real, unique-quoted and type-correct
and still not support the sentence it is quoted for (the entry decides what its
`**OBS**` line claims). No token rule can close that without rejecting the
genuine portal receipt (0 `focus_grab` hits, above), so the semantic binding
remains the non-author closure's job. The trust root stays the freeze: a forged
fetch committed before the freeze would be pinned as genuine.

## Reproduction

```
cd .ufo/waves/round-41/w1/CritC2Cheat
python3 -I tighten.py --verify-pins     # nine pins match the frozen fetch dir
python3 -I verify-quotes.py             # six genuine quotes unique across the fetch dir
python3 -I build-forgeries.py           # nine fixtures, frozen counter + tightenings
```
