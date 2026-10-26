# C1 contract: dead weight before data (SimpContract, round 43 w1)

Scope: `PRED-C1-r42`, unchanged from round 42. The scored contract is the docstring of
`quality/counters/c1-r42-geometry.py` (frozen `809dc2ca…`, present at base `a35cfdf…`), which restates the
docstring of the reference `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt` (sha256 `e3c2e4715059…`). The
reference is the executable oracle for every claim below: every "live" verdict has a pair of inputs the
reference answers differently, every "dead/redundant" verdict has a *violating variant* of the reference
that is byte-identical to it over a 647-case corpus, and every such corpus claim is accompanied by a
positive control that the corpus *does* catch.

Nothing in the lane was written; the frozen counter, controls, registration, reference and fetch receipts
were read only. All work ran under `/fast/scratch/hyaku/mado-r43/SimpContract/` (deleted at the end).

## 0. Method (two independent instruments)

- **A — input pairs.** `lab.py` loads the frozen reference as a module (`importlib` on the `.txt`, the
  same code path `python3 mado-geometry.py` takes: `run(argv, stdin)`, `Setup` → `SETUP` line + rc 2).
  `probes.py` runs 65 rows: 58 pairs where the two inputs produce different bytes/rc, 7 where they produce
  the same (the constraint sentences: flag order A05, directory vs chardev A08, zero-width `=` B06, tab
  tokens B08, TILED ignores the size column C17, leading-zero normalisation D02, the verdict first link
  D06). The two `rc+verdict` rows compare verdicts only, with the reason in the row note. **65/65 rows match expectation** (`evidence/probes.json`).
- **B — violating variants.** `equivalence.py` builds 11 edited copies of the reference. Four violate
  exactly one dead/redundant sentence; seven are positive controls that violate a live sentence. The corpus
  is every run the 37 fixtures make (107 replays, reconstructed in-process by patching only the counter's
  `execute`), plus boundary/path-kind cases (`/proc/kcore`, mode-000 files, `> 1048576` invalid JSON, a FIFO,
  `/dev/null`, a directory, 0/1048576/1048577-byte files), the regex0 alphabet battery, and a seeded
  500-case grammar lattice. Reference outcome histogram over the corpus:
  `rc0=108, rc1=15, rc3=189, rc4=277, SETUP usage=11, unreadable=20, too_large=12, bad_json=15` — every
  branch is reached. **4 equivalent variants: 0/647 diffs. 7 positive controls: 2–277 diffs each** (`evidence/equivalence.txt`).
- **C — fixture reconstruction.** `fixtures_scan.py` patches `counter.execute` and replays all 37 fixtures
  in-process against the frozen reference: **37/37 pass**, so the harness is the same oracle the counter is.
  It records every argv, stdin, file byte and the reference source lines executed (`evidence/fixture-scan.txt`).
  `deadproof.py` then answers "does any fixture input contain X?" (`evidence/deadproof.txt`).

## 1. Inventory

The counter docstring splits into 41 sentences. 22 of them are tool-contract sentences
(`C10`–`C14`, `C16`–`C24`, `C26`–`C33`); they expand into 62 distinct claims (65 pair rows, probe ids below). The
remaining 19 are one-line headings (`C09`, `C15`, `C25`, `C38`) or counter mechanics and declared
residuals (`C01`–`C08`, `C34`–`C37`, `C39`–`C41`), which no tool input can address.

| claim | contract text (abridged, ≤ 25 words) | verdict | evidence |
|---|---|---|---|
| A01 A02 A03 A04 | `--selftest` alone; `--clients` once; `--rules` one or more; two-token form only | live | A01–A04 |
| A05 | "(two-token form only, any order)" | live, **unexercised** | A05, F1 |
| A06 A07 | SETUP = one line + exit 2; reasons `usage/unreadable/too_large/bad_json` | live | A06, A07 |
| A08 A09 A10 A11 | missing/dir/FIFO/non-regular is unreadable; must not block; `> 1048576` is too_large | live | A08–A11 |
| A12 A13 A14 A15 | `--clients -` is stdin; not-UTF-8 JSON / non-list / non-object is bad_json (empty too) | live | A12–A15 |
| A16 | clients input judged before the rules files | live | A16 |
| A17 | rules files judged **in argument order** | live, **unexercised** | A17, F3 |
| B01 | "decoded as UTF-8 with errors replaced" | live, **unexercised** | B01, F2 |
| B02 | "a line is stripped of spaces and tabs at both ends" | live | B02 (P3 kills `strip()`) |
| B03 B04 B05 | RULE LINE fullmatch; `windowrulev2`/`WindowRule` ignored and counted nowhere | live | B03–B05 |
| B06 | "`windowrule[ \t]*=(.*)`" (zero-width `=` spacing) | live, constraint | B06 |
| B07 B08 B09 | effect = first token; runs of spaces/tabs; empty effect → `other` | live | B07–B09 |
| B10 B11 B12 B13 B14 | exactly two fields; `[0-9]{1,5}` ASCII; `on|off`; `match:class[ \t]+(.+)` | live | B10–B14 |
| B15 | "REGEX … 1-200 characters" | 200 live, **`1` dead** | B15, DEL-1, V2 |
| B16 B17 B18 B19 B20 | alphabet; escapes; no `(?`/`*+`/`++`/`?+`; compiles under `re` | live | B16–B20 |
| B21 B22 | unsupported counting; `n=`/`file=` numbering across files | live | B21, B22 |
| B23 B24 | class with no char < U+0020; `re.fullmatch` | live | B23, B24 (P1 kills search) |
| C01–C04 | `mapped` JSON false only; 0/null/"false" are not false | live | C01–C04 |
| C05 C06 C07 C08 C09 C10 C11 | class string/else ""; floating only `true`; size 2 ints, not bools, **"not floats"**, ≥ 0; address string/else "-" | live; **"not floats" redundant** | C05–C11, DEL-4 |
| C12 C13 C15 C16 C17 | last matching size rule; last matching float rule; BADSIZE ≻ TILED; AGREE/DIFFER | live | C12, C13, C15–C17 |
| C18 C19 | duplicate JSON key keeps the last value (class/size/floating/mapped; address) | live, address **unexercised** | C18, C19, F5 |
| D01–D03 | `json.dumps` ensure_ascii; WxH without leading zeros; input order | live | D01–D03 |
| D04 D05 D06 | verdicts and exit codes; NO_SIZE_RULES first; "tested in that order" | live only for the first link; **links 2–3 dead** | D04–D06, DEL-3, V3, V4, P5 |

## 2. Dead or redundant sentences (with the exact deletion text)

### DEL-1 — the lower bound of "1-200 characters" (redundant, twice over)

- **Claim.** `REGEX fully matches 1-200 characters` (`quality/counters/c1-r42-geometry.py:34`). The `1` can
  never decide anything: `match:class[ \t]+(.+)` (`:34`, model `MATCH_RE`) already requires ≥ 1 character,
  and the field is `strip(" \t")`-ed first (`:26-29`), so `match:class` + separators is stripped to a field
  with no separator, which fails `[ \t]+` before `.+` is ever consulted.
- **Proof.** V2 replaces `{1,200}` with `{0,200}` in the model's `SAFE_RE` and the reference's `SAFE`:
  **0/647 diffs** (`equivalence.txt: V2-regex-min-0`). Positive control P2 relaxes the lower bound **and**
  the field grammar (`[ \t]*`, `(.*)`) and then differs in 63/647 cases — so the bound is redundant only
  jointly with the field grammar, which must stay as it is.
- **Precedent in the frozen controls.** `.ufo/waves/round-42/ctl/run-c1-controls.py:72,73` already excludes
  `M38-regex-empty` as an equivalent mutant for exactly this reason; the contract sentence was never
  narrowed to match. This is the same class of dead weight as the round's `M20` `#` clause, which was deleted.
- **Deletion.**
  - contract (`quality/counters/c1-r42-geometry.py:34`):
    `the capture being REGEX; REGEX fully matches 1-200 characters of` → `the capture being REGEX; REGEX is at most 200 characters of`
  - reference docstring (`.ufo/waves/round-42/c1/ctl-ref-tool.py.txt:34`):
    `REGEX is 1-200 characters of` → `REGEX is at most 200 characters of`
  - model (`quality/counters/c1-r42-geometry.py:129`): `){1,200}")` → `){0,200}")`
  - reference code (`ctl-ref-tool.py.txt:69`): `){1,200}")` → `){0,200}")`
  - keep `MATCH_FIELD`/`MATCH_RE` and the strip exactly as they are (P2 shows why).

### DEL-2 — the stdin cap number "1048577" (dead as a number; the bound is live)

- **Claim.** "`--clients -` reads standard input, at most 1048577 bytes" (`c1-r42-geometry.py:20-21`;
  reference `:21-22`).
- **Proof.** V1 reads `MAX_BYTES + 2` instead: **0/647 diffs**, including stdin of 1048573…2097152 bytes.
  Any cap ≥ `MAX_BYTES + 1` is observationally identical, because every input over 1048576 is `too_large`.
  The **bound** itself is live and already caught by the frozen control `M05-stdin-short` (cap = `MAX_BYTES`),
  which the round-43 receipt lists as a kill.
- **Deletion.**
  - contract (`:20-21`): ``` `--clients -` reads standard input, at most 1048577 bytes; ``` → ``` `--clients -` reads standard input; ```
  - reference (`:21-22`): `an input larger than 1048576 bytes is too_large (stdin, ``` `--clients -` ```, is read at most 1048577 bytes);`
    → `an input larger than 1048576 bytes is too_large (stdin included);`
  - model: no edit (the model never reads stdin). Reference code `data = stdin.read(MAX_BYTES + 1)` may stay.

### DEL-3 — the last two links of the verdict order (dead)

- **Claim.** "DIFFER (differ>0; exit 1) | NO_MATCHING_CLIENT (matched=0; exit 3) | OK (exit 0), tested in
  that order" (`c1-r42-geometry.py:55-56`; reference `:55-57`).
- **Proof.** `differ > 0` implies `matched > 0` (only matched clients get a verdict), and `matched == 0`
  excludes `OK` by construction, so the three conditions are mutually exclusive and their order cannot be
  observed. V3 moves `DIFFER` after `NO_MATCHING_CLIENT`: 0/647. V4 tests `OK` first: 0/647. Positive
  control P5 puts `NO_MATCHING_CLIENT` before `NO_SIZE_RULES` and differs in 277/647 — the **first** link
  (`rules=0` before `matched=0`) is live and is the one the fixtures read (`empty0#0`).
- **Deletion.**
  - contract (`:55-56`): `V = NO_SIZE_RULES (rules=0; exit 4) | DIFFER (differ>0; exit 1) | NO_MATCHING_CLIENT (matched=0; exit 3) | OK (exit 0), tested in that order.`
    → `V = NO_SIZE_RULES (rules=0; exit 4), tested first; otherwise DIFFER (differ>0; exit 1) | NO_MATCHING_CLIENT (matched=0; exit 3) | OK (exit 0), three mutually exclusive conditions.`
  - reference (`:55-57`): the same replacement, keeping its own line wrapping.
  - model (`:318-325`): no edit required; the two `elif` branches may be permuted (V3 proves it).

### DEL-4 — "not floats" (redundant with "JSON integers")

- **Claim.** "a list of exactly two JSON integers (not booleans, not floats) that are >= 0"
  (`c1-r42-geometry.py:44`; reference `:45`).
- **Proof.** No JSON token is both an integer and a float; `1.0`, `1e0`, `1E0`, `0.0`, `-0.0`, `1.5` all
  fail the integer test alone (`evidence/deadproof.txt`, token table). The model's predicate
  `type(v) is int and v >= 0` (`:298`) and the reference's `isinstance(int) and not bool` are unchanged by
  the deletion; the frozen control `M15-size-float` stays killable because "integers" still excludes `1.0`
  (`sizevals0`). "not booleans" is **not** redundant (Python `True` is an `int`) — it stays.
- **Deletion.** `(not booleans, not floats)` → `(JSON booleans are not integers)` — in both docstrings
  (`c1-r42-geometry.py:44`, `ctl-ref-tool.py.txt:45`). Model: no edit; do **not** add
  `and not isinstance(v, float)` (dead code).

### DEL-5 — two reference-docstring sentences no input can answer (already dropped from the counter)

- `ctl-ref-tool.py.txt:14` — `It reads files and standard input only; it starts no process and opens no socket.`
  No argv/stdin makes the output depend on it. Its only scored residue is clause g's static name ban
  (`socket`/`urllib`/`subprocess` …) and, for "starts no process", the sandbox's
  `RLIMIT_NPROC = 1` — both environment-level, not input-level. **Delete the sentence** (keep the property in
  the tool's own README, or leave it to clause g).
- `ctl-ref-tool.py.txt:57-58` — `DIFFER is a report, not a fault: a user may have resized the window, or the
  compositor may have clamped the rule's size.` Motivation, unscored; the counter's contract omits it
  already. **Delete.**
- The counter's sentence `C08` claims its restatement is "the same sentence"; after DEL-5 that is true.

### DEL-6 (cosmetic) — duplicated word in the frozen contract

`c1-r42-geometry.py:29-30` reads `The effect is the first` / `first token of field 0`. Delete the repeated
`first` (no behaviour; the fixture B07 result is unchanged).

## 3. Deletion candidates I checked and **rejected** (they look dead, they are live)

| candidate | why it is *not* dead | witness |
|---|---|---|
| "the clients input (unreadable, too_large, bad_json)" order (`:23`) | the pairs overlap: a mode-000 regular file of 1048577 bytes and `/proc/kcore` (size 140 737 471 594 496, `EACCES`) are **both** unreadable and > 1048576; a 1048577-byte invalid-JSON file is **both** too_large and bad_json | P6 differs 2/647 (`SETUP unreadable` vs `SETUP too_large`); P7 differs 2/647 (`too_large` vs `bad_json`); only the *unreadable vs bad_json* link is vacuous (bad_json needs a successful read) |
| "at most 1048577 bytes" as a **bound** (as opposed to the number) | a tool reading only `MAX_BYTES` accepts a 1048577-byte valid document | frozen control `M05-stdin-short` is a kill; DEL-2 only removes the number |
| "tested in that order" — **first** link | `rules=0` and `matched=0` co-occur (empty rules file with clients) | P5 differs 277/647 (`empty0#0`) |
| "REGEX … 200 characters" upper bound | 200 accepted, 201 unsupported | B15; `regex0` carries both |
| "not booleans" | Python `True` is an `int` | C08 (`[True,2]` → BADSIZE); `sizevals0` |
| "BADSIZE (size none) | TILED (not floating)" priority | a bad size on a non-floating client is BADSIZE, not TILED — and `client0` **does** cover it: its `{}` client has class `""`, which the rule regex `a|` matches, size none, floating absent | C15; fixture scan (`client_badsize_and_not_floating` in `client0`) |
| (hypothesis — **not in the text**) "takes precedence over the size rule" | **no such sentence exists** in either docstring (`grep -n precedence` finds nothing); I had hypothesised it from the summary and it is not in the frozen text | `evidence/grep-precedence.txt` (both greps, exit 1) |
| "The effect is … (the empty string when there is none)" | an empty effect lands in `other`, not in `unsupported` | B07 |

## 4. Live, but unexercised by the 37 fixtures (free passes for a cheat)

Derived mechanically: every argv/stdin/file byte of all 107 fixture runs was replayed and scanned
(`deadproof.txt`, last block). For each line below, a tool that gets it wrong still scores 37/37.

| # | contract text | witness that it is live | what no fixture contains |
|---|---|---|---|
| F1 | "(two-token form only, any order)" (`:17`) | reversed flags give a report (A05) while `usage0#9` only tests a *trailing junk* token | no run with `--rules R --clients C` that is expected to succeed |
| F2 | "decoded as UTF-8 with errors replaced" (`:26`) | invalid byte → `unsupported=1`, rc 4 vs `AGREE`, rc 0 (B01) | no non-UTF-8 rule file (all texts are ASCII/valid UTF-8) |
| F3 | "the rules files in argument order" (`:23-24`) | missing-first → `unreadable`, big-first → `too_large` (A17) | no setup failure with ≥ 2 rules files |
| F4 | "The body is split on \",\"" (`:29`) | a `;`-separated line is `unsupported`; a tool that also splits on `;` accepts it | no rule line containing `;` (P4 differs 33/647) |
| F5 | "A duplicate JSON key keeps its last value" (`:48`) — **address** key | duplicate `address` prints the last one (C19) | `dupkeys0` duplicates class/size/floating/mapped only |
| F6 | "A PATH that is … unreadable" (`:19-20`) — permission denial | mode-000 file → `SETUP unreadable` (order matrix) | no mode-000 path; the unreadable fixtures use missing / directory / chardev / FIFO only |
| F7 | "(unreadable, too_large, …)" first link (`:23`) | mode-000 1048577-byte file, `/proc/kcore` → `unreadable` (P6) | no path that is both unreadable and oversized |
| F8 | "(… too_large, bad_json)" link (`:23`) | 1048577-byte invalid JSON → `too_large` (P7) | no oversized invalid-JSON input |
| F9 | "field 0 has exactly two argument tokens" (`:31`) — zero arguments | `windowrule = size, match:class a` → `unsupported=1` (B07) | no bare `windowrule = size` line |

Also unexercised, counter-side (not tool contract): `C05` "No bwrap → SETUP" (bwrap is present here, so the
branch cannot be reached), `C36` cost bound (no fixture tool hangs; a conforming tool never times out).

## 5. Findings for the L1 (not deletions)

- **DEF-1** `c1-r42-geometry.py:29-30` duplicated word (DEL-6).
- **DEF-2** The counter says the reference docstring *is* the contract "restated here, the code below being
  the same sentence" (`:8-10`). Two reference sentences are absent from the restatement (DEL-5), and the
  counter adds "fully" before "matches" twice where the reference has none. After DEL-5 the claim holds; the
  `fully` should be added to the reference so both texts agree (`matched` semantics unchanged — the code
  already uses `fullmatch`).
- **DEF-3** The freeze carries a clause the controls already call equivalent (`M38`/DEL-1) and a cap number
  that cannot be observed (DEL-2). Neither changes any score; both make the contract longer than the
  behaviour. If w1 reports before any data commit, a v2 re-freeze can drop them; no counter behaviour changes.
- **Coverage note (not a free pass):** the 11 accepted escapes are asserted only in aggregate by `regex0`
  (one line holding all of them). A tool that wrongly rejects one specific escape *is* caught, but the
  failure is not localised to the escape.

## 6. Numbers and replay

- Contract sentences read: 41; tool-contract sentences: 22; atomic claims probed: 62.
- Input pairs: 65 rows over 62 distinct claims, 65/65 expected (58 differ, 7 same). Variants: 11, 11/11 expected (4 equivalent at
  0/647; 7 positive controls at 2–277 diffs). Fixture replay: 37/37 against the frozen reference.
- Deletions proposed: 6 items (DEL-1…DEL-6): two sentences, three clauses, one bound and one duplicated
  word. Behaviour changed: none — each textual deletion is either proven unobservable by a variant that
  stays byte-identical over 647 cases, already excluded as equivalent by the frozen controls (`M38`), or
  unobservable outright (`MAX_BYTES + 2`, the `elif` order).
- Replay (scratch, ~2 min, no host mutation, no bwrap needed):
  `python3 probes.py; python3 equivalence.py; python3 deadproof.py; python3 fixtures_scan.py; python3 analyze.py`
  from the `scripts/` copy of this seat directory; receipts in `evidence/`.
- Tool installs: none (stdlib only; python 3.14.8 `/usr/bin/python3`).

### Tradeoff

The contract loses two sentences, three clauses and one bound. What it loses in prose it keeps in
strictness: the two
live-but-unexercised setup links (F7, F8) and the flag-order freedom (F1) are *not* deleted and *not*
claimed dead — they are the compensations this seat refused to spend. The cheapest real strengthening would
be nine new fixture inputs (one per F row); that is a counter change, not a contract deletion, and it is
outside this seat's scope.
