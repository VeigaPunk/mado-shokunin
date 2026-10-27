# CritRouted — round-48 w2 (FALSIFY): closure of D1–D4, R3, R4b

Seat `CritRouted`, leaf, wave `w2`, lane `mado-shokunin`, base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`,
freeze (scored revision) `3e6c848a0e1bbc9c7058226b86d0faefc5351c9d`. Attack surface: the routed round-47 items only.
Three throwaway `git clone --shared` trees under `/fast/scratch/hyaku/mado-r48/CritRouted` (toplevel asserted before
every commit, `seat <seat@scratch.invalid>`); the lane was not written, no predicate, counter, fixture, claim or
target was edited, no package installed. Every command and its output is in `w2/CritRouted/measurements.md` and the
receipts beside it. Scratch deleted before yielding.

**Result: six of six routed items close on measured evidence; three freezes are weaker than their seat reports imply
in ways that do not breach any registered clause. No blocker.**

| item | question | verdict |
|---|---|---|
| D1 | conditional HOME measured **and frozen**? | **yes** — 10 frozen HOME-UNSET fixtures + E-01; both branches bite (mutants score 199/204 and 193/204) |
| D2 | findings=128/115 receipted at named revisions? | **yes** — 115/128/128, repeated bytes identical |
| D3 | two-valid-candidate readdir fixtures? | **yes** — 10 READDIR cases, nine with normative `files_order`; a `sorted()` walk misses |
| D4 | range fix lands append-only? | **yes** — 96 → 123 lines, prefix byte-identical, working tree equals the simulated append |
| R3 | marker fails both ways and keeps real findings? | **yes** — marked waived / unmarked counted / forged path rejected / forged value rejected; 101 real findings stand |
| R4b | append preserves the frozen r45 verdict? | **yes** — both PRED-C2-r45 counters MET before and after; `(S303)` control → `g:0` MISSED |

## 0. What was scored, and why these bytes

* Freeze revision `3e6c848a` carries both counters, the 190+204 fixtures, the pin, the w1 seats and `l1-draft/`.
* C1 was scored on `freeze + .ufo/waves/round-48/l1-draft/mado-terminal.py`
  (`1dfde36c…`, byte-identical to the working-tree `tools/mado-terminal.py`). Instrument pins verified:
  `SHA256_WARM` = `4d946bd7…` = the committed `c1-r48-fixtures.json`; `SHA256_COLD` = `4836cc1d…`;
  `PIN_SHA256` = `89f2be9a…` = `/usr/bin/xdg-terminal-exec`.
* Baseline: `cold=190/190 warm=204/204 explained=394/394 generated=230/230 selftest=ok readonly=ok
  verdict=TARGET_MET` (rc 0, nonce 4848, `c1-baseline.txt`). A counter that cannot reach MET on the data
  candidate would have been a miss before any routed item; it does.

## 1. D1 — conditional HOME: measured, frozen, and it bites

**1.1 Measured.** `w1/ExecHomeUnset.md` ran 19 fixtures pin-vs-tool in the round-47 counter's own sandbox, 3
identical runs, and found 8 divergences, of which the conditional HOME cases are the point: HOME unset with
`XDG_CONFIG_HOME`/`XDG_DATA_HOME`/`XDG_CACHE_HOME` set → pin `rc 0` + id, base tool `rc 2` (C2/C2b); HOME unset
with exactly one of the three unset → pin `rc 1`, empty stdout at `:148`/`:166`/`:172`. `w1/ScrD1Line/lines.md`
independently reaches the same matrix and lands the lesson lines.

**1.2 Frozen.** The 204-case warm set carries class `HOME-UNSET` ×10 (`v2-hu-01…10`) plus `EDGE-HOMEUNSET`
(`E-01`), with `meta.note` naming the death site. All eleven pass in the baseline (`c1-baseline.txt`). The freeze is real,
not cosmetic: clause w compares tool vs the **live pin** and separately raises a setup error when the pin drifts
from the recorded `expect` (`score()`: `drift` is filled from the warm loop too), so hu-01's recorded `rc 0` is
enforced twice. The landed contract text matches (`l1-draft/mado-terminal.py:102-104`: "when any HOME-based default
is needed … exits 1 with empty stdout, and with all three set it runs normally"), and the lesson's M47-11 `fix`
line demands exactly that conditional reading.

**1.3 The predicate bites both ways** (mutants are one-hunk patches of the candidate tool, scored with the frozen
counter at nonce 4848):

| mutant | commit | result |
|---|---|---|
| `need_home` refuses with the tool's `exit 2` instead of the pin's `set -u` `rc 1` (branch: a default *is* needed) | 91a4d88d | `warm=199/204`, `explained=389/394`; FAIL `E-01`, `v2-hu-02`–`05` (`oracle=(1,'') tool=(2,'')`) — the exit-status half is frozen |
| HOME unset refused at `make_paths` entry, i.e. the round-47 base behaviour (branch: all XDG set) | 83bdea7a | `warm=193/204`, `explained=383/394`; FAIL **all eleven** HOME fixtures (`E-01`, `hu-01`…`hu-10`), e.g. `hu-01 oracle=(0,'foot\n--a\n') tool=(2,'')` |

**1.4 Both branches are therefore frozen, and neither mutant gets close.** The "refuse always" mutant is the exact
behaviour ExecHomeUnset measured at base, and the frozen set rejects it on eleven cases; the "refuse with the wrong
status" mutant is rejected on the four defaults-needed cases. Direct, sandbox-free measurement agrees: the candidate
returns `foot`, `rc 0` under `env -i … (HOME absent, three XDG set)`; the freeze-revision tool returns
`MADO_TERM_OUT_OF_CONTRACT: HOME unset`, `rc 2` (`d1-home-direct.txt`).

**1.5 Freeze limits (recorded, none a clause breach).**
* `HOME=""` (set but empty) cannot be expressed: `case_env()` forces `HOME=<root>/home` unless `HOME` is in
  `unset`, and `unset` can only remove it. ExecHomeUnset C4/C4b measured agreement at base; no fixture freezes it.
* The three death sites are not ordered by the predicate: all single-empty variants expect `rc 1` + empty stdout,
  so a tool that expands the cache default first passes clause w. The seat's report and M47-11 record the real
  order (`:148`, `:166`, `:172`), but only stderr — which the contract does not compare — carries it.
* The neighbouring D1 items are documented but unfrozen: the FIFO refusal is narrowed to the read
  (`l1-draft/mado-terminal.py:753-754`) and the symlink-loop refusal withdrawn in the docstring, yet the 204 has no
  FIFO case and no loop case (class `H1` is directories; `v2-h1-01…12`). A FIFO tree the pin answers around is
  therefore not judged. M47-12/M47-13 carry the lesson lines; the contract text names the read-time rule.

## 2. D3 — two valid candidates, readdir order

* **Fixtures exist and are normative.** `READDIR` ×10 (`v2-rd-01…10`); nine multi-entry cases ship
  `meta.files_order`, and the counter materializes in it (`write_files(…, order=meta.files_order)`,
  `c1-r48-terminal-cache.py:404`). The recorded winners are readdir-dependent and *not* sorted:
  `foot,kitty` → `kitty.desktop`; `konsole,ghostty` → `ghostty.desktop`; `foot,kitty,aaaa` → `aaaa.desktop`
  (`d3-readdir-fixtures.txt`). `meta.fs=xfs`; the replay work dir was asserted xfs (`stat -f`), matching the seat's
  filesystem claim.
* **Frozen and enforced.** All ten pass in the baseline (`warm=204/204`); the pin-drift check covers them.
* **The blind spot is closed, not merely described.** One-line mutant `names = sorted(de.name for de in
  os.scandir(cur))` in `_walk` (commit 7d9ed9cc) scores `warm=202/204`:

  ```
  v2-rd-05-three          FAIL oracle=(0,'aaaa.desktop\n')   tool=(0,'kitty.desktop\n')
  v2-rd-06-reverse-create FAIL oracle=(0,'ghostty.desktop\n') tool=(0,'konsole.desktop\n')
  ```

  with `explained=392/394`, `generated=228/230`, `verdict=TARGET_MISSED`. Two of the ten cases decide the verdict,
  which is what the routed D3 asked for (an expectation that fails a `sorted()` walk).
* Limit: the fixture seat's own risk 3 stands — the expects rest on creation order, declared as a host/filesystem
  dependency in `registration.md` (residuals). The replay reproduced it on xfs; a different `--work` filesystem
  would become a setup error, not a pass.

## 3. R3 — synthetic-material marker installed at the freeze, failing both ways

Installed with the delivered `install.sh` into a scratch clone at the freeze: **48 registry rows, 48 sidecars, gate
`82c9053a…`**, selftest `69/69` (`measurements.md` §3). The install commit is `576ba060`.

* **Not laundered.** Same revision, `--no-waivers` vs default: `findings=153` → `findings=101`, exit 1. The set
  difference (52 `(file, rule)` pairs in 48 files) equals the printed `WAIVER` set **exactly** (`True` in the
  comparison; R1 34 / R2 34 / R3 10 / R4 2 / R5 21 left). Nothing outside a valid marker pair disappears.
* **Both ways, one commit apart, same bytes:**

  | demo | rev | observed |
  |---|---|---|
  | unmarked synthetic fixture | 64498219 | `findings=154`, `FINDING … synthetic-clients.json rule=R1_CLIENT_DUMP count=1` |
  | + sidecar + registry row | 8276ce4a | `WAIVER … kind=fixture`, `findings=101`, no FINDING line |
  | same bytes at `.ufo/reports/session-clients.json` with a well-formed pair | c16060bd | `WAIVER_REJECTED … reason=path-outside-waves`, FINDING stands, `findings=102` |
  | real title inside a fixture path with a well-formed pair | 32f39a97 | `WAIVER_REJECTED … reason=value-not-synthetic:title-not-synthetic`, FINDING stands, `findings=103` |

* **Real findings preserved and still red:** `findings=101`, rc 1, including 11 findings in the three stale gate
  copies (round-45 `ExecPrivacyGate`, round-46 `ExecSessionTriage`, round-47 `ExecSessionMarker`). The delivered
  set waives 47 round-45 fixtures + 2 round-46 fixtures + its own byte-identical gate copy; it claims no green.
* Cosmetic defect (report-side, not data): `install.sh`'s header comment still says "the registry, 47 rows" /
  "47 sidecars" while the two counts it prints and the file contain 48 (47 `fixture` + 1 `gate-copy`).

## 4. R4b — round-45 errata that keeps the frozen round-45 verdict

* Append at the freeze: 107 → 158 lines, **prefix byte-identical** (`cmp -n`), block contains
  **0** source ids (`\b[Ss][0-9]{3,}\b`), no `source:`/`verified-at:`/`recheck:` line, no fence, no `BAD_LOC`.
  sha256 of the appended entry `73a6c4ac…1ffa0e` = the working-tree `corpus/knowledge/hyprland-monitor-rule-r45.md`,
  i.e. the integration is exactly this append and nothing else.
* Frozen instruments, before and after (same clone, revision-addressed reads):

  | rev | `c2-r45-monitor-entry.py` | `-v2.py` |
  |---|---|---|
  | 579f694b (base) | `admitted=1/1 TARGET_MET` rc 0 | `admitted=1/1 TARGET_MET` rc 0 |
  | 3e6c848a (freeze, no block) | `admitted=1/1 TARGET_MET` rc 0 | `admitted=1/1 TARGET_MET` rc 0 |
  | 344845ba (freeze + block) | `admitted=1/1 TARGET_MET` rc 0 | `admitted=1/1 TARGET_MET` rc 0 |

  Every row `clauses=a:1 … j:1`.
* **Instrument still bites:** the same block with `(S303)` restored in E6 → `admitted=0/1 TARGET_MISSED` rc 1,
  `g:0` on both counters. Clause `g` is the only thing the source id touches, so the delivered wording avoids it
  structurally rather than by luck.
* Cited numbers re-checked independently: entry `:18` (recheck/release), `:84` (S311 monitor-added emit), `:96`
  (host dump), `:98` (99.997 Hz), `:106` (description), `:107` (hyprlang form) are the lines the bullets name;
  `tools/mado-monitors.py` = `2f007417…` at both `4d22eeb` and `579f694b`; the round-47 pin dirs exist at the
  freeze. The seat's risk 2 (no frozen clause binds an errata bullet's `file:line`) is real but the bytes are right.

## 5. D4 — the round-47 entry locator erratum, append-only

* Reproduced on the base bytes: entry line 95 cites `terminal-route-r17.md:150-151`; the source sentence opens at
  `:149` (`- [UNK] Whether the `--dir=` value from … is valid at`) and closes at `:150` (`launch time. The helper
  is not run.`); `:151` is 1 byte (a blank line's newline). One wrong locator in the swept pair, as routed.
* Append: 96 → 123 lines, **prefix byte-identical** (`cmp -n`, `diff` clean), sha256
  `051e36b9…16efa` = the working-tree `corpus/knowledge/xdg-terminal-selection-r47.md`. Nothing above EOF moves, so
  every external locator into `:76`/`:88`/`:95` stays valid.
* The block states its own limit: the stale `:150-151` remains in the body, so a future predicate that greps the
  entry for the wrong range will still hit it — no such predicate exists in `registration.md`, and the appended
  lines carry exactly one full-file locator (`terminal-route-r17.md:149-150`, line 105) plus one bare `:150-151`
  mention (`d4-append.txt`: full-file locators at 76, 88, 95, 105).
* Consequence for closure: D4 is a receipt-only item. Its correctness now rests on the seat's sweep plus this
  independent recomputation, not on an instrument.

## 6. D2 (same routed set) — the session-material counts

`quality/check-session-material.py` at the freeze, revision-addressed, no worktree writes:

```
60edb66e files=18371 findings=115 rc=1
d40189c9 files=19969 findings=128 rc=1
579f694b files=19969 findings=128 rc=1
```
Second run of `579f694b` byte-identical to the first (`cmp` clean). The claim "128 at the tip (115 at base)"
reproduces on the instrument bytes named by the seat.

## 7. Risks / residuals for the L1 (none blocks closure)

1. **D4 and R4b are judged by no counter.** Both are append-only prose; the errata numbers are verified by seat
   scripts and my recomputation only. If the round wants them bound, the predicates must be registered *before* the
   data commit; they are not in `registration.md` now.
2. **HOME="" and the HOME death-site order** cannot be frozen by the fixture schema as registered (§1.5); the
   conditional branch that D1 actually asked for is frozen.
3. **FIFO read-time narrowing and loop withdrawal** are implemented and documented but have no frozen fixture; they
   are M47-12/M47-13 lesson lines, not round-48 predicates.
4. **D3's expectations are filesystem/creation-order dependent.** The freeze's residual declares it; the replay
   matched on xfs. A `--work` on another filesystem turns the ten cases into a setup error, not a miss.
5. **R3's install header comment undercounts (47 vs 48).** Cosmetic; the printed counts, registry and sidecars are
   48/48 and the gate enforces the rows.
6. **Counter scratch needs >1 MiB files.** The C1 instrument copies host binaries (`gawk` etc.) into its sandbox;
   under the seat's 1 MiB `ulimit -f` it dies with `OSError [Errno 27]`. The four counter runs used
   `ulimit -f 65536` (32 MiB) and nothing else; my own outputs peak at 30 220 B, scratch totalled 159 MB, no `/tmp`.
