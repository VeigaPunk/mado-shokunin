# RevC2Counter — findings on `PRED-C2-r41-v1` (`quality/counters/c2-r41-focus-entry.py`)

Reviewed end-to-end against its docstring (clauses a–i) and the control runner
`.ufo/waves/round-41/ctl/run-c2-controls.py` (receipt `receipts/ctl-c2.txt`: 41/41).
Frozen counter == HEAD (`git diff 60c3914 HEAD -- c2-r41-focus-entry.py` empty). All
probes ran through the control runner's own `score()` (temp git repos in /tmp, cleaned up);
each finding names its reproduction. Severity: High / Medium / Low.

---

## High

### H1 — The whole validation surface is anchored to the entry's first 20 lines; citations past line 20 are completely invisible
- Counter: `c2-r41-focus-entry.py:188-193` — `ids` is built from `text.splitlines()[:20]` only.
  Every later clause (c, d, e, g, i) iterates over those `ids`; no other scan of the entry
  exists. `SRC_RE` (line 82) only feeds this list.
- Reproduction: entry cites `S304` at the file tail (after 30 filler lines, i.e. past line 20)
  → `admitted=1/1 TARGET_MET`; the same citation within the first 20 lines is fully validated.
  A **ghost citation** `source: S999 - ghost row` (no registry row, no GATE line, no receipt,
  no OBS line) at the file tail is also admitted (`admitted=1/1`); put in the head it is
  rejected (c:0 d:0 g:0). So a body-only citation carries zero accountability.
- Effect: any id cited only below line 20 is unverifiable — no row, gate, receipt, quote, or
  localization check applies. The docstring sentence "every cited id has exactly one `## Registry`
  row" (clause c) and the clause-i localization sentence are thereby enforceable only for the
  first 20 lines, as implemented. This is a contract hole: an entry can bury any number of cited
  sources (including localized-channel or fabricated ones) below the window and still be admitted.
- Line refs: `c2-r41-focus-entry.py:186-193` (head/ids), `:204-225` (c), `:227-260` (d),
  `:262-272` (e), `:287-302` (g), `:309-313` (i).

### H2 — Clause b's head scan is not the `unfenced` text; fenced `source:` lines count, contradicting the docstring
- Docstring (`c2-r41-focus-entry.py:6-7`): "Fenced code blocks (``` ... ```) of the entry and
  of the README are removed before any line is matched."
- Code: `head = text.splitlines()[:20]` operates on the **raw** text (line 188); `unfenced`
  (lines 133-141) is applied only later for `lines`/`entry_lines` (clauses g/h). The `verified-at`
  / `recheck` header scan (lines 195-202) is also on raw `head`.
- Reproduction: moving `source: S301 - protocol xml` inside a ``` fence within the first 20 lines
  → `admitted=1/1` (the fenced source line still counts toward clause b's ≥4 distinct sources).
- Effect: the docstring's "removed before any line is matched" is false; fenced material can
  satisfy clause b. Conversely, an adversary cannot hide head citations via fences (they still
  count), so the practical risk is the contract mismatch plus H1's window.

### H3 — Cheapest forgery: a fabricated self-consistent set passes at ~9.2 KB committed bytes
- Control P is the declared residual ("a fabricated self-consistent set passes"); the suite's P
  fixture is **13,860 committed bytes / 10 files**. A minimal fabricated set meeting every
  threshold — 2 sessions, 40 adverts, 20 distinct late-session interfaces, 1 focus_grab advert in
  an invented journal; three invented 512+B receipts; invented quotes — **passes at 9,220
  committed bytes / 9 files** (`admitted=1/1`). Reproduction: minimal-forgery builder in the probe
  harness (journal 4,251 B; receipts 3×~512 B; SRC/LES/ENTRY/README).
- The receipt bytes are invented; the journal parses to exactly the counts the entry repeats
  (clause h compares only counter-computed vs entry-repeated counts). Nothing ties a receipt to
  its served location or to the host journal. The residual is therefore unbounded below 13.9 KB —
  the freeze receipt does not establish a floor.
- Lines: journal grammar enforcement `c2-r41-focus-entry.py:155-178, 83-88`; clause h
  `:274-285`.

### H4 — Clause i's localized-channel test is a substring heuristic on the full cell; rename defeats and false positives confirmed
- Code: `BAD_LOC = ("amgsk.dev", "zhihu", "/zh", "/ja")` (line 91); clause i checks
  `any(b_ in rows[0][1] for b_ in BAD_LOC)` (lines 309-313) — a plain substring test on the whole
  source cell (title + location), for cited ids only.
- Rename defeat: the cited row's location `https://zenn.dev/articles/hyprland-focus-grab`
  (Japanese-channel platform, none of the four tokens) → `admitted=1/1`. Also unblocked:
  any mirror/proxy host (e.g. `web.archive.org`), translated domains, or one of the many
  non-token Japanese/Chinese platforms.
- False positives (substring hits in benign material):
  - location `https://example.org/zhang-project` → **rejected** (i:0) via `/zh`;
  - title "works - https://ja.wikipedia.org/wiki/Hyprland" with an innocuous English location →
    **rejected** (i:0) via `/ja` — the test scans the **title cell**, not just the location,
    contrary to the docstring's "source row's location".
- Effect: the clause is both under- and over-inclusive; a rename defeats it, and ordinary content
  trips it. A hostile host rename (any localized platform without those substrings) bypasses the
  PROVINCE.md exclusion entirely.

---

## Medium

### M1 — Docstring-vs-code: clause c requires "at least 3" new ids; code implements ≥2 (P1 passes with 2)
- Docstring (lines 16-17): "ids absent from the BASE registry (at least 3)". Code:
  `cl["c"] = int(rows_ok and len(new_ids) >= 2)` (line 225).
- Reproduction: base with two held rows (S050, S051); entry cites S050,S051,S301,S302
  (2 new ids) → `admitted=1/1`. The control suite cannot express this (its base has one held row,
  and clause b forces ≥4 distinct cited ids, so new_ids ≥ 3 in every fixture with one held row).
- Effect: the counter is weaker than its contract sentence; an entry with exactly two new sources
  is admitted against the docstring.

### M2 — The assimilation-binding sentences are unenforced: REFUSE/ADMIT accept any path
- Docstring (lines 45-48): ADMIT "the assimilation set's admit" / REFUSE "the assimilation set's
  reject". Code (lines 306-314): any `ADMIT <pkg> as <entry>` and any
  `REFUSE <pkg> reason=<≥20 chars>` satisfy clause i; no relation to the staged package set.
- Reproduction:
  - `REFUSE corpus/knowledge/unrelated.md reason=not a measurement of focus grab` → admitted;
  - `ADMIT merge/mado/knowledge/corpus/knowledge/other-surface-r99.md as <entry>` → admitted.
- Effect: the non-author closure spot-check depends on the human noticing the path mismatch; the
  count predicate does not bind either line to the staged packages.

### M3 — Clause h's "not a tool's report" is not syntactically verifiable
- Docstring (lines 32-34): the receipt "is a saved journal (… not a tool's report)". The parser
  (`journal_counts`, lines 155-178) accepts any text whose lines match the ADVERT/BOOT grammar;
  there is no structural marker that distinguishes a journal from a tool dump.
- Reproduction: receipt = `MADO_GLOBALS_TOOL_REPORT v1\nparsed=ok\n` + 40 advert-shaped lines +
  quote → `admitted=1/1`.
- Control J04 only exercises a report with **no** advert lines; a report that emits advert-shaped
  lines (i.e. exactly what C1's tool would print if it echoed the journal) passes.

### M4 — Sentence-level mutant coverage gaps (the "no mutant kills it" answer)
Every clause letter has ≥1 killing mutant (a:N01, b:N11, c:N02/N07/N08/N12/N13/N16/X05/X14,
d:N03/N04/N05/N12/N14/X11/X13/Y01/Y02, e:N09, f:N06/X07, g:N03/N04/N05/N10/N12/N14/X11/X13/Y01/Y02,
h:N15/J01-J11/X03/X11, i:A01-A05), so the "which clause is unkilled?" question has no clause-level
answer. But the following **sentences** inside clauses have no dedicated mutant, and in three cases
the enforcing code could be deleted without changing any of the 41 control outcomes (the controls
never vary along that axis):

| sentence | enforced by code? | controls exercising it | probe |
|---|---|---|---|
| b: `recheck:` ISO/`NNd`/`on-*` | yes (lines 200-202) | none (N11 only flips `verified-at`) | P7 (nonsense recheck rejected — check works, uncovered) |
| b: "first 20 lines" scope | yes (line 188) | none (no mutant moves citations across the window) | P3/P19 (boundary behavior; no control) |
| c: "(at least 3)" new ids | no — code is ≥2 (line 225) | none (N07 leaves 1, never 2) | P1 admits with 2 |
| d: quote lower bound "3-25 words" | yes (line 246) | none (N05 only tests the 26-word upper bound) | P12 (2-word quote rejected — check works, uncovered) |
| h: "not a tool's report" | no (grammar-only, lines 155-178) | J04 only (report without advert lines) | M3 probe admits with tool preamble |
| i: REFUSE/ADMIT bound to the assimilation set | no (lines 306-314) | A01/A02/A03 (absence/retarget of ADMIT; never REFUSE path) | M2 probes admit |

The counter's own sentence-level tests are therefore concentrated on clause letters, not on every
sub-requirement; three of the six sentences above are contract words the code does not implement.

### M5 — Counter vs C1 predicate grammar: identical regexes, but both stricter than their docstrings
- The C2 counter's `ADV_RE`/`BOOT_RE` (`c2-r41-focus-entry.py:84-88`) are **byte-identical** to
  C1's (`quality/counters/c1-r41-globals.py:170-174`) — verified by diff. The claim that clause h
  "agrees with the C1 predicate grammar" is true for the two counters.
- Both are stricter than their prose: C2's docstring ADVERT grammar (lines 40-42) says
  `TS HOST xdg-desktop-portal-hyprland[PID]: [LOG]  | Got interface: NAME (ver N)` with no
  format constraints; the code demands ISO-8601-with-timezone TS
  (`\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}`), exactly two spaces before `|`, name
  ≤128 chars, version ≤6 digits. The runner's own test double (`run-c2-controls.py:55-56`) uses
  the looser `\S+ \S+` for TS and `\d{1,6}` for version — a third, different grammar. A saved
  `-o short` journal (no timezone) would satisfy the docstring but score 0 sessions under the
  code; the runner would parse it fine.
- The real fetched journal `fetch/xdph-journal.txt` (19,130 B, sha256
  bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7) parses under the counter's
  grammar to (2 sessions, 78 adverts, 63 distinct, 1 focus_grab) — consistent with the
  registration's provisional census and with the 153-line receipt.

---

## Low

### L1 — A second, malformed GATE line for the same id is invisible to "EXACTLY ONE line"
- Code: `GATE_RE` (lines 79-80) only matches well-formed lines; a second line with a bad sha
  (e.g. `sha256=zz`), not indented, neither matches the regex nor the `<indented>` detector.
- Reproduction: adding `GATE S303 … sha256=zz …` beside the valid one → `admitted=1/1`.
- Effect: the "exactly one line" check counts only parseable lines; a duplicate line carrying a
  typo is silently ignored. Low, because a *well-formed* duplicate is caught (X13).

### L2 — Registry cell equality is not byte-equal as documented
- Docstring (lines 16-17): held ids "keep cells 1-10 byte-equal". Code (line 150):
  `[c.strip() for c in line.strip().split("|")[1:-1]]` — cells are whitespace-trimmed before the
  comparison, so `|S050|` vs `| S050 |` compare equal. Cosmetic divergence; does not weaken held
  rows in practice.

### L3 — Clause e's location-uniqueness scan ignores malformed rows
- Code (lines 262-272): duplicate check iterates only rows with exactly 11 cells; a second row
  with ≠11 cells never participates, so a duplicate location hidden in a malformed row escapes e.
  Low (registry rows are machine-generated by the lane's append-only schema).

---

## Residual risk / verification gaps
- The counter cannot distinguish invented bytes from served bytes (declared residual); the minimal
  forgery measured here (9,220 B) shows the residual is cheaper than the freeze's 13,860-B control
  P. No byte-level or journal-authenticity check exists (nor could it without host access).
- H1's 20-line window is the largest structural gap: any content below line 20 is unvalidated.
  The clause-b "first 20 lines" scope and clause-c "at least 3" are the two contract sentences with
  no enforcement path at all.
- Clause i's substring heuristic is defeated by host rename and trips on benign `/zh`/`/ja`
  substrings, including in title cells (M6? no — H4).
- Control suite provenance: all 41 controls pass against the frozen counter; the suite targets
  clause letters, not every sentence; the gaps in M4 are those sentence-level holes.

Reproduction files: probe harness at `/tmp/revc2c_probe.py` (scratch; deleted after handoff if
desired) — all probe outputs quoted in this file were produced by it or by the inline /tmp probes
recorded above (control runner `score()`/`commit_all()` reused verbatim; temp git repos cleaned).
