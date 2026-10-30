# R56W3CritC1Forge — forge attack on PRED-C1-r56-v2 against the CORRECTED entry at the lane tip

Seat: R56W3CritC1Forge (leaf; no subagents). Wave 3, attempt 2 of round 56.
Target: the counter/harness/tables at the lane tip `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`
(= content revision `8a7b734627b06583a9106fcc0940f0a180ff331d` + attempt-1 receipts/LOG/SCORECARD/lesson).
Lane read-only: no tracked file, no index, no ref, no object of the lane or the fleet repo was written.
Scratch: `/fast/scratch/hyaku/mado-r56/R56W3CritC1Forge/` (`git clone --shared` of the lane; one commit per
variant; removed before this yield). Deliverable: `.ufo/waves/round-56/w3/R56W3CritC1Forge/receipts/forge-a2.txt`.

## Bottom line

**The wave-2 finding stands at the tip, unchanged in severity, and the corrected prose does not narrow it.**
The corrected entry is a better entry — but the counter that certifies it is *byte-identical* to the one
wave 2 attacked (`quality/counters/c1-r56-autoreload-entry.py` sha256 `2b2ef41b3329edde1b30a88ab13f9430b3522d052186b4eb00ebb154a0301fea`
at both `28fc86ac…` and `0f3a5436…`; `quality/r56_ctl_c1.py` `2151c3ed…`; `frozen-tables-v2.json` `9511151a…`).
The counter never reads meaning. My own rewrites — not wave 2's — falsify **all 33** propositions and still
print `content=33/33 verdict=TARGET_MET missed=none` with the harness at `good=ok controls=12/12 verdict=OK`.

Three things are **new at the tip** and were not in wave 2's report:

1. **The 9 E rows (E01–E09) are outside the frozen predicate entirely.** They are rows of the entry, they
   carry propositions, pins and quotes, and `content=33/33` counts 30 K + 3 H only. The frozen tables have
   **no `e` key at all** (`c1 keys = ['commit','controls','echo_min_quote_len','entry','h','host_pin_sha256',
   'k','new_row_ids','new_rows_min','opened','pin_dir','pin_sha256','pin_suffix','prov_window','rev_rule','rows']`).
   I replaced all nine E-row quote cells with text that exists in **no pin file**, replaced all nine E-row
   propositions with a denial, pointed all nine at a non-existent registry id `S999`, and added a **new row
   E10** citing a non-existent registry id `S396` and a non-existent pin file. **Every one of those is
   accepted: `TARGET_MET` + `controls=12/12` + `good=ok`.** The entry's row set grew from 33 counted to
   42 real; the predicate still counts 33.
2. **The corrected prose makes the lexical gap larger, not smaller.** The wave-2 corrections made each
   proposition *more specific* (K05, K07, K08, K14, K21 now carry the extra clauses the earlier draft
   omitted), and each added clause is content the frozen quote does not contain. Measured: identifier tokens
   of the proposition that the frozen quote does not supply went from **259 of 361** (w2) to **335 of 434**
   (tip). All 33 rows still pass with one shared identifier.
3. **Five registry rows the entry depends on (S391–S395) are read by no C1 leg.** `source_cell` reads only
   the 30 K-row sids (S383–S390) and `new_rows` reads S383–S390; S391–S395 are read by neither. I set their
   tier to `C`, status to `rejected`, opened to `1999-01-01`, their anchor to a file that does not exist and
   their `teaches` cell to a denial: **C1 stays `TARGET_MET` and the harness stays 12/12.** (C3 catches the
   emptied `used-by` — `missing=5` — so C3 covers the *back-reference*, not the *claim*.)

**Cheapest undetected forgery:** **one character.** Changing K24's `the GLOB_TILDE flag` to
`the GLOB_TILDE flags` (the pinned line passes ONE flag) is accepted:
`content=33/33 verdict=TARGET_MET missed=none`, harness `good=ok controls=12/12 verdict=OK`.
A clean 3-character version (K26 `at its last slash` → `at its first slash`, contradicting `find_last_of`)
is likewise accepted. **The counter's content leg is not a falsification test at any granularity.**

## Setup (read-only w.r.t. the lane)

- Pin: `git -C <lane> archive 0f3a5436… | tar -x` (the counter, harness, tables and 13 pinned files).
- Scratch repo `W` = `git clone --shared --no-checkout <lane> $S/W2`; `git rev-parse --show-toplevel`
  asserted equal to `$S/W2` before the first commit; identity `-c user.name=ctl -c user.email=ctl@ctl`;
  each variant is one commit; `git reset --hard 0f3a5436…` + `git clean -fdb` between variants so no
  variant can contaminate the next (an earlier pass of my driver did contaminate the C3 readings after
  round 5; the receipt below is from the clean consolidated re-run).
- Per variant, three real programs, each `python3 -I`, run from `/fast/scratch/…`:
  - `python3 -I <lane>/quality/counters/c1-r56-autoreload-entry.py --repo <W> --rev <sha> --work <scratch>`
  - `python3 -I <lane>/quality/check-r56-controls.py --claim c1 --repo <W> --rev <sha> --work <scratch>`
  - `python3 -I <lane>/quality/counters/c3-r56-used-by.py --repo <W> --rev <sha> --work <scratch>` (cross-check)
- Baseline on the lane itself (read-only, `--work` in scratch):
  `MADO_AUTORELOAD_ENTRY: rev=0f3a5436… rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none`, rc=0.
- Tools: **none installed or upgraded** (python 3.14.8 and git 2.56.0 only; no pacman, no network, no
  `uv`/`cargo`/`npm`). Host reads: none (no `hyprctl`, no `/proc`, no `~/.config`). The host guard was not
  needed for this item.

## Results — every variant (full diffs and counter lines in `receipts/forge-a2.txt`)

"accepted" = counter `TARGET_MET missed=none` **and** harness `good=ok controls=12/12 verdict=OK`.

| variant (attack) | counter | harness | C3 | accepted? | what a reader would reject |
|---|---|---|---|---|---|
| `base-honest` (control) | TARGET_MET 33/33 | ok 12/12 | MET | n/a | (baseline) |
| `para33` — **my own** lexical paraphrase of all 33 propositions | TARGET_MET 33/33 | ok 12/12 | MET | **yes** | 33 sentences wholly reworded; nothing changed |
| `false33` — **my own** semantic falsification of all 33 propositions | TARGET_MET 33/33 | ok 12/12 | MET | **yes** | every one of the 33 rows asserts the reverse of its pinned line |
| `neg3` — semantic negation of K04, K15, H01 (my choice) | TARGET_MET 33/33 | ok 12/12 | MET | **yes** | 3 of 33 rows assert the reverse |
| `shuffle` — row order shuffled (K inside K table, H inside H table) | TARGET_MET 33/33 | ok 12/12 | MET | **yes** | the table no longer reads in pin order; the `Chain` prose still says "K01…K30, one row per frozen quote" in order |
| `cheap1-K26` — 3 chars: "at its last slash" → "at its first slash" | TARGET_MET 33/33 | ok 12/12 | MET | **yes** | K26 contradicts the pinned `find_last_of` |
| `cheap1-K24-1char` — **1 char**: "the GLOB_TILDE flag" → "flags" | TARGET_MET 33/33 | ok 12/12 | MET | **yes** | the pinned line passes ONE flag |
| `eforge-e-fake-quotes` — all 9 E-row quotes = text in no pin | TARGET_MET 33/33 | ok 12/12 | MET | **yes** | 9 quoted lines that exist nowhere |
| `eforge-e-false-props` — all 9 E-row propositions = a denial | TARGET_MET 33/33 | ok 12/12 | MET | **yes** | 9 rows that assert the opposite of their quote |
| `eforge-e-src-S999` — all 9 E-row src cells → `S999` | TARGET_MET 33/33 | ok 12/12 | **MISSED (extra=2)** | C1 yes / C3 no | E rows citing a registry id that does not exist |
| `eforge-new-E10` — new row: id `S396`, pin `Hyprland-NotARealFile.cpp`, fabricated quote | TARGET_MET 33/33 | ok 12/12 | MET | **yes** | an invented row citing an invented source |
| `dup-K01-into-E01` — E01's proposition = K01's, byte-identical | TARGET_MET 33/33 | ok 12/12 | MET | **yes** | duplicate authority across the 33/42 boundary |
| `dup-K01-into-K02` — **positive control**, K02's proposition = K01's | **TARGET_MISSED** `row:K01,row:K02,tok:K02` | **good=bad** | MET | **no** | the uniqueness check fires *inside* the counted 33 |
| `echo-off-K28` — K28's quote is 24 chars < `ECHO_MIN` 30, so the echo leg is OFF for that row: quote embedded verbatim + a denial | TARGET_MET 33/33 | ok 12/12 | MET | **yes** | the row says the opposite of the line it quotes |
| `prose-false` — **six load-bearing prose claims inverted**, both row tables untouched | TARGET_MET 33/33 | ok 12/12 | MET | **yes** | the entry's `Chain`/`Consequences`/`Path resolution` prose now asserts the reverse (see the six substitutions below) |
| `prose-false-plus-K18` — the six prose inversions **and** the one-word K18 change | TARGET_MET 33/33 | ok 12/12 | MET | **yes** | both |
| `reg-S391-395-dead` — S391–S395: tier→C, status→rejected, opened→1999-01-01, anchor→a file that does not exist, `teaches`→a denial | TARGET_MET 33/33 | ok 12/12 | MET | **yes** | five dead registry rows the entry depends on |
| `scope-S383-1-112` — S383 anchor `ConfigWatcher.cpp:1-112` (file has 111 lines) | TARGET_MET 33/33 | ok 12/12 | MET | **yes** | wave-2 D2 reproduces at the tip: the bound is `len(blob.split(b"\n"))` = 112, one past EOF |
| `scope-S383-1-111` — S383 anchor covers the whole file | TARGET_MET 33/33 | ok 12/12 | MET | **yes** | wave-2 D3 reproduces: the scope leg is vacuous for the 10 K rows that cite S383 |

The six prose substitutions of `prose-false` (all in the entry's prose, none in a row table):

```
"The watch list is therefore rebuilt after every `reload()` from the then-current `m_configPaths`"
  -> "The watch list is therefore NEVER rebuilt after any `reload()` and keeps the first list it ever saw"
"A missing `source` target never enters the list."
  -> "A missing `source` target always enters the list and is watched as a missing path."
"No deduplication."
  -> "Every path is deduplicated, so a file reached twice is watched once."
"- `~`: the first byte is replaced by the value of `HOME`"
  -> "- `~`: the first byte is replaced by the value of `USER`"
"The event `name` field is never read, so the reported path is the watch's stored path, not the name the kernel reports."
  -> "The event `name` field is the reported path, so the kernel's name replaces the watch's stored path."
"`resetHLConfig()` (`legacy:764-786`) clears the list (776; K20), adds the main path (777-779)"
  -> "`resetHLConfig()` (`legacy:764-786`) adds the main path first (777-779) and clears the list afterwards (776; K20)"
```

## Re-verification of the corrected entry itself (the honest part)

These are the checks that **passed**; they are what the corrected prose bought.

| check | result |
|---|---|
| every K, H and E row's frozen quote is present at its stated pin line | **42/42, 0 failures** (independent of the counter) |
| every row's src id is a registry row | 42/42 |
| every E row's quote is at its pin line | 9/9 (E01 S393, E02 S383, E03 S392, E04 S394, E05–E07 S395, E08–E09 S391) |
| counter at the tip, on the lane itself | `rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none` |
| C1 controls harness at the tip | `good=ok controls=12/12 verdict=OK` |
| C3 at the tip | `entries=71 rows=332 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET` |
| the counter, the C1 harness and the frozen tables are byte-identical between `28fc86ac…` and `0f3a5436…` | yes (sha256 above) — **the correction was made in the entry, not in the checker** |

## Measured answers to the assignment's questions

**1. Which legs catch which forgery.**
- The **row grammar** (`row:<id>`) catches only structural damage: a duplicated proposition inside the counted
  33 (`dup-K01-into-K02` → `row:K01,row:K02`), a dropped row, a malformed cell.
- The **quote leg** (`quote:<id>`) catches a quote cell edited to a string that is not on the pinned line
  (harness control 8). It is **never** exercised by a semantic forgery: my forgeries keep the frozen quote
  cell byte-identical.
- The **content leg** (`tok:` ∧ `num:` ∧ `echo:`, `content=<e>/33`) catches a proposition that shares **no**
  identifier with the quote, that introduces a digit the quote does not contain, or that echoes the quote
  verbatim. It catches **none** of my forgeries: `false33`, `neg3`, `shuffle`, `cheap1-K26`,
  `cheap1-K24-1char`, `eforge-*`, `dup-K01-into-E01`, `echo-off-K28`, `prose-false` and `reg-S391-395-dead`
  all reach `content=33/33`.
  - Measured on the **honest** tip entry: **0 of 33** propositions contain a digit run, so the `num:` leg
    **cannot fire at all** — it is vacuous, not merely weak. The `echo:` leg is also satisfied trivially by
    every row (0 of 33 honest propositions echo their quote), and is **switched off entirely for the 4 rows
    whose quote is shorter than `ECHO_MIN` 30** (K08, K16, K20, K28). And `tok:` asks for **one** shared
    identifier: 8 of 33 quotes supply ≤2 identifiers, and **K10's quote supplies exactly one**
    (`IS_SYMLINK`).
  - So on the honest tip entry the content leg reduces to: *the proposition contains the string
    `IS_SYMLINK`*. Everything else about the sentence is unchecked.
- The **scope leg** (`scope:<id>`) catches an anchor that no longer covers the quoted line, and the
  **registration-v2 E3 bound** catches an anchor that reaches past EOF — except for the off-by-one that
  wave-2 D2 found, which reproduces at the tip (`ConfigWatcher.cpp:1-112` accepted for a 111-line file).
- The **source_cell leg** catches a K row citing the wrong registry row, a row whose registry row has the
  wrong status/tier/date/URL/`used-by`. It reads **only S383–S390**.
- The **prov leg** catches a `source:` line that is missing, out of order, past line 15, or that lists a
  non-registry id; and it catches a cited id that is not on the `source:` line. It reads only the **first 15
  lines** and only K-row sids.
- The **index leg** catches a missing or duplicated README line.
- The **pin_hash leg** catches an edited pin blob.
- The **new_rows leg** catches a missing S383–S390 registry row.
- **No leg of any kind reads**: the entry's **prose body** (111 of 168 lines; ~90 of the entry's ~134
  sentences), the **9 E rows**, the registry rows **S391–S395**, or the `teaches` cell of any registry row.

**2. The cheapest undetected forgery.**
**One character.** K24's proposition, `the GLOB_TILDE flag` → `the GLOB_TILDE flags`
(the pinned line `glob(absolutePath(rawpath, m_configCurrentPath).c_str(), GLOB_TILDE, nullptr, glob_buf.get())`
passes exactly one flag). Counter: `content=33/33 verdict=TARGET_MET missed=none`; harness:
`good=ok controls=12/12 verdict=OK`. Three-character version: K26 `at its last slash` → `at its first slash`,
which contradicts the pinned `find_last_of`. The forgery needs one row cell; the counter's content leg
cannot see either.

**3. Does the corrected prose change the wave-2 finding's severity?**
**No — it is the same defect, and the correction moved it slightly further from the evidence.**
- The counter, the C1 harness and the frozen tables are byte-identical to the wave-2 revision, so the
  wave-2 measurement re-runs unchanged; my own independent rewrites reproduce it (33/33 falsified, accepted).
- The correction was applied to the **entry**, not to the **checker**: it made 9 K and 7 E propositions true
  that wave-2's sentence-to-pin audit had found false. It cannot make `content=33/33` mean "entailment",
  because `content=33/33` never tested entailment.
- Two tip-specific effects make the gap **wider**, not narrower: (a) the corrected propositions carry more
  content per row (335/434 identifier tokens outside the frozen quote, versus 259/361 at wave 2), so a
  reader who trusts `content=33/33` is trusting a sentence the quote supplies less of; and (b) the tip grew
  the entry from 33 counted rows to **42 real rows**, of which the **9 E rows** are outside the predicate
  entirely, and grew the registry dependency to **S395**, of which **S391–S395** no C1 leg reads.
- The lane's own record already concedes the limit (`claims-frozen-v2.md` §"What v2 does not repair": "a
  forged proposition that shares a quote identifier, keeps to the quote's numbers and does not echo the quote
  passes") and the SCORECARD cell says "Not entailment: a lexical rewrite of all 33 propositions keeps
  `content=33/33`". **That disclosure is accurate but understates the reach**: it describes a paraphrase
  attack on the 33 counted rows, and does not mention that a one-character edit, the 9 uncounted E rows, the
  entry's prose body and five registry rows are all outside the check. Severity of the *underlying* defect:
  **unchanged (blocking for "TARGET_MET ⇒ sourced content")**; severity of the *disclosure*: **weakens the
  claim as written** — the round's own disclosure names only the paraphrase class.

## Defects (input → what it shows → severity)

| id | input | shows | severity |
|---|---|---|---|
| **D1** | `false33` (33 propositions, each contradicting its pinned line), `neg3` (3 of 33), `cheap1-K24-1char` (1 character), `prose-false` (six prose claims inverted) | the content leg is not a falsification test at any granularity; `TARGET_MET` + `controls=12/12` on an entry whose propositions and prose assert the reverse of their pins | **blocking** for the claim wording "sourced entry / quote identity … lexical grounding" read as evidence of content; the frozen limit concedes the paraphrase class only |
| **D2** | `eforge-e-fake-quotes`, `eforge-e-false-props`, `eforge-e-src-S999`, `eforge-new-E10` | the 9 E rows and any further row are **outside the predicate**: `content=33/33` counts 30 K + 3 H while the entry carries 42 rows; the frozen tables have no `e` list, so E-row quotes are never checked against a pin, E-row propositions never checked for truth, and E-row src ids are never checked against the registry | **blocking** for "the entry is sourced": the entry's own row set is 21 % unmeasured, and a *new* row can be added without any leg noticing |
| **D3** | `reg-S391-395-dead` (tier→C, status→rejected, opened→1999-01-01, anchor→a file that does not exist, `teaches`→a denial) | `source_cell`/`scope`/`new_rows` read only S383–S390; **S391–S395**, which five registry rows of this round's own entry depend on, are read by no C1 leg (C3 catches only the `used-by` back-reference, `missing=5`) | **weakens**: the registry binding the claim asserts is checked for 8 of the 13 rows the entry cites |
| **D4** | `prose-false` | the counter reads the provenance head (lines 1–15) and the row tables — **111 of 168 lines and ~90 of ~134 sentences of the entry are never read by any counter**; the load-bearing `Chain`, `Consequences`, `Path resolution` and `Limits` prose can be inverted wholesale | **weakens**: `TARGET_MET` says nothing about the entry's analysis |
| **D5** | `scope-S383-1-112` | the E3 bound is `len(blob.split(b"\n"))`, one past the last newline-terminated line (111-line file → 112) | **weakens** (small code defect; wave-2 D2 reproduces) |
| **D6** | `scope-S383-1-111` | a whole-file anchor makes `scope:` vacuous for the S383 rows (11 of 30 K rows) | **weakens** (wave-2 D3 reproduces) |
| **D7** | `dup-K01-into-E01` (accepted) vs `dup-K01-into-K02` (caught) | the proposition-uniqueness check is computed over the counted 33 only; the same byte-identical duplication is legal across the 33/42 boundary | **weakens** |
| **D8** | `echo-off-K28` | `ECHO_MIN` 30 switches the echo leg off for the 4 rows whose quote is shorter (K08, K16, K20, K28); on those rows the frozen quote may be embedded verbatim in a proposition that then denies it | **weakens** |
| **D9** | measured on the honest tip entry | the `num:` leg is **vacuous** (0 of 33 propositions contain a digit run) and the `echo:` leg is satisfied trivially by every row; the effective content constraint is "the proposition contains one identifier the quote supplies", and K10's quote supplies exactly one (`IS_SYMLINK`) | **weakens** (the content leg is one token wide) |
| **D10** | the tip's `source:` line reads `S392-S395 (extra-row anchors for E01, E03-E07)` | the literal-token rule (`(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])`) yields only **S392 and S395** from that range: **S393 and S394 are not on the provenance line at all**, although E01 cites S393 and E04 cites S394. The `prov` leg does not catch it because it only compares K-row sids | **weakens** (provenance line under-declares the sources it names; the C3 `extra` leg is what finally sees S393/S394 through the E-row `src` cells) |
| **D11** | `shuffle` | the row order is unchecked; the entry's own prose says the K table is "one row per frozen quote" in a reading order the counter never verifies | **cosmetic** |
| **D12** | the tip's `source:` line / E-row src cells vs `used-by` | the source line and the E-row `src` cells name **S383, S391, S392, S395** but the E rows cite **S393** and **S394**, which appear in the registry and in `used-by` but nowhere in the `source:` line | **weakens** (provenance incompleteness; see D10) |

## Defects not found (null results, with the command that found nothing)

- **A quote cell edited to a string absent from the pin** is caught — but only for the **counted** rows: the
  harness control 8 (`edited-quote` → `row:K05`) fires for K05, while `eforge-e-fake-quotes` (the same edit on
  all nine E rows) is accepted. Command: `receipts/forge-a2.txt`, VARIANT `eforge-e-fake-quotes`.
- **A duplicated proposition inside the counted 33** is caught (`dup-K01-into-K02` → `row:K01,row:K02,tok:K02`).
  The same duplication across the boundary is not (`dup-K01-into-E01`).
- **The `num:` leg is not vacuous on a mutated tree** — the harness control 3 (`false-number`, `num:K04`)
  fires. It is vacuous only on the honest tip entry (D9).
- **The `echo:` leg does fire** when a long quote is echoed (harness control 11 → `echo:<id>`). It is off for
  K08/K16/K20/K28 (D8) and it never fires on a paraphrase or a negation.
- **A registry row that no K row cites is not read by C1** — but C3's `extra` leg sees it
  (`eforge-e-src-S999` → C3 `extra=2`). C3 is the cross-check that catches the *back-reference* break; it
  cannot catch a false *claim* (D3).
- **Nothing in the C1 harness or counter reads the `teaches` cell of any registry row** (D3).

## Could not verify / not run

- **The truth of the 33 honest K/H propositions and the 9 E propositions.** I verified each row's frozen
  quote against its pinned line (42/42) and read the pin context for the rows the wave-2 audit had corrected
  (ConfigValues.cpp:492, ConfigWatcher.cpp:30–75 and 95–111, legacy ConfigManager.cpp:625–635 / 1830–1845 /
  2128–2136, MiscFunctions.cpp:61–70, HyprCtl.cpp:1185–1195, PropRefresher.hpp:10–25), but I did **not**
  re-derive the source behaviour row by row; the counter does not check it either. The wave-2 sentence-to-pin
  audit (`w2/R56W2RevProsePath.md`, `w2/R56W2RevProseLimits.md`) is the lane's record for that.
- **Entailment by a non-author reader.** Not run — this seat measures what the counter cannot see.
- **The C2 predicate and the tool.** Not attacked (out of scope for this item).
- **The live host.** Not read (not needed: the H-row quotes are byte-checked against the pinned captures,
  3/3 present at their stated lines).
- **`configValues.hpp` is not pinned** — the entry's own K01 says so ("what that argument means (the default)
  is in ConfigValues.hpp, which is not pinned"), and I confirmed no `ConfigValues.hpp` is in the pin set
  (`ls .ufo/waves/round-56/fetch/` shows only `Hyprland-PropRefresher.hpp`). The `MS` macro is at
  `Hyprland-ConfigValues.cpp:160` (`#define MS makeConfigValue`), so the *macro* is pinned but the
  *default-value semantics* are not; K01's wording is accurate about this.
- **`S391`'s pin hash.** `receipts/pins-extra.sha256` records it (lesson M56-9). Verified at the tip:
  the frozen `pin_sha256` map holds 8 keys and `Hyprland-PropRefresher.hpp` is **not** one of them, so the
  counter's `pin_hash` leg does not cover that pin — consistent with the lesson's own disclosure, and
  therefore a disclosed limit rather than a new defect. (This is why E08/E09's quotes are not hash-pinned.)

## Commands that produced the numbers

Each row of the results table is one variant: one edit set → one commit in `W` → the three commands above →
`receipts/forge-a2.txt` (full diff + the three result lines). The base row is `base-honest`.
`receipts/forge-a2.txt` is the consolidated clean run (20 variants, 520 lines) produced by
`/fast/scratch/hyaku/mado-r56/R56W3CritC1Forge/make_receipt.py`; the scratch tree and the driver scripts are
removed before this yield.
