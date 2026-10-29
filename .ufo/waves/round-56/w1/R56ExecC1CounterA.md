# R56ExecC1CounterA — C1 counter `c1-r56-autoreload-entry.py` (wave w1)

Deliverables (all under `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w1/R56ExecC1CounterA/`):
- `c1-r56-autoreload-entry.py` (sha256 `b47963dadf812bfdb17ac6c87130fd45169714ca4d6575fb8522e588fbfc9baa`, executable, python3 stdlib only, runs under `python3 -I`)
- `selftest-run.txt`, `control-run.txt` (the ten registered controls, real counter output lines), `lane-freeze-run.txt`

Authored by this seat; I am not a non-author reviewer. No tool was installed, nothing under ~/.config or ~/.local was touched, hyprctl was not run, no hold-out path was looked for or seen.

## What I did
Built the counter strictly from registration §C1 + claims-frozen PRED-C1-r56. Reads only git objects at `--rev` (`rev-parse`, `ls-tree -z`, `cat-file blob`; env scrubbed, HOME/TMPDIR = `--work`, created when missing; counter writes nothing). Only modes 100644/100755 accepted; a symlink blob or a path below a symlinked directory is absent. Embedded constant `TABLES_SHA256 = d50d2b7b…f9af`, checked against the blob at `--rev` (leg `tables_sha`). Prints exactly the frozen line; rc 0 only on TARGET_MET, 1 on a miss, 2 on a setup error (stderr reason, empty stdout; argparse usage errors, bad rev incl. whitespace/leading dash, non-root `--repo`, unexpected internal exception, and a table whose sha matches but whose shape is invalid). List-all: every failing leg is printed, order = registration table order (entry_absent, tables_sha, prov, index, row, quote, pin_hash, host, source_cell, scope, tok, num, new_rows), ids in frozen order K01..K30, H01..H03.

`--selftest --repo <lane> --rev <rev> --work <scratch>` needs the frozen-tables blob (sha-checked) and the 12 pins from `--rev`, builds scratch git repos (one `mktemp -d -p <work>/selftest-<pid>`, `git -C "$D"` everywhere, toplevel asserted before the first commit, `-c user.name=ctl -c user.email=ctl@ctl`) from a witness entry + registry S383..S390 + README that I generate, runs the counter as a child process per case, and removes its scratch.

## Commands and decisive output
```
python3 -I c1-r56-autoreload-entry.py --selftest --repo <lane> --rev 3423ae28… --work <scratch>
MADO_R56_C1_SELFTEST: 154/154 assertions passed          (rc 0, ~30-45 s)
python3 -I c1-r56-autoreload-entry.py --repo <lane> --rev 3423ae28… --work <scratch>
MADO_AUTORELOAD_ENTRY: rev=3423ae28… rows=0/30 hosts=0/3 sources=0/30 scope=0/30 content=0/33 new_rows=0/8 verdict=TARGET_MISSED missed=entry_absent,index,new_rows   (rc 1; at the freeze commit tables_sha holds)
```
Selftest covers: the witness (exact frozen line, rev echoed as given, deterministic, mode 100755 entry), registration controls 1-10 as written, tables_sha (trailing newline / absent / bad shape / symlink), prov (11 cases incl. window edge line 30/31, order, duplicate verified-at), index (4), row grammar (~40: trailing space/tab/CR, spacing, cell count, pipe, escaped pipe, 39/40 and 19/20 char boundaries, leading/trailing space, duplicate proposition, `S38`/`S3840`/`host` in K, `S383` in H, pin cell file/line/zero-padded, quote backticks double/none/tilde/trailing space, duplicate id identical/different, backtick fence, 3-space tilde fence, 4-space marker is no fence, fenced copy ignored, HTML comment multi-line/one-line, unterminated fence), host forgery, source_cell (status, tier A/B/C, opened, used-by absent/longer name/prefix path/list, URL commit/suffix/trailing byte/last token, man7 host token, duplicate id, malformed 12- and 10-cell rows, 3 vs 4 leading spaces, symlinked/absent registry), scope (19 locator cases: edges, off-by-one, reversed, comma/space lists, list stop, second occurrence, other-file, `: 492`, man7, `legacy/ConfigManager.cpp` substring), tok (4), num (14), symlinked entry/dir above entry/README/pin/pin-dir, repo through symlink, dirty working tree ignored, subdirectory repo, 8 setup-error invocations, empty tree, `--work` created.

Does the selftest bite? I ran four mutated copies of the counter (scratch, deleted): scope forced true → 131/154; num forced true → 147/154; registry uniqueness relaxed to "first row" → 152/154; tok forced true → 148/154. Each mutant fails exactly the cases targeting that leg.

Registered controls, real output (`control-run.txt`; rows→TARGET_MISSED, rc 1):
```
CTL1  missed=entry_absent                                   rows=0/30 … new_rows=8/8
CTL2  missed=tok:K01..K22,tok:K24..K30,tok:H01..H03         content=1/33   (K23 survives: junk text contains the identifier "source", K23 quote has `source=`)
CTL3  missed=num:K04                                        content=32/33
CTL4  missed=source_cell:K10,scope:K10                      sources=29/30 scope=29/30
CTL5  missed=prov,source_cell:K10,scope:K10
CTL6  missed=prov
CTL7  missed=row:K17                                        rows=29/30 sources=29/30 scope=29/30 content=32/33
CTL8  missed=row:K05,quote:K05                              rows=29/30
CTL9  missed=pin_hash                                       (first byte of the pin changed, quoted lines intact)
CTL10 missed=prov,source_cell:K29,source_cell:K30,scope:K29,scope:K30,new_rows   new_rows=7/8
```

## Ambiguities / defects in the contract (most literal reading taken; both readings)
1. **quote:<id> vs control 8 (substantive).** Leg table: "the frozen quote is a substring of line <line> of the pin blob" — that is independent of the entry, so editing a char inside the K05 quote cell would give only `row:K05`, and control 8 ("→ `quote:K05`") could never pass. I made `quote:<id>` fire in addition when the row's quote cell ≠ backtick+frozen quote+backtick (rows that cannot be split into 5 cells get only the pin-text half). Literal reading: first half only → control 8 unsatisfiable. The same mismatch makes a forged H cell fire `row`, `quote` and `host`.
2. **Controls 4 and 5 list fewer legs than the literal legs produce.** Control 4 (K10 cites S385) also fires `scope:K10` (S385's anchor has no `ConfigWatcher.cpp:`); control 5 (K10 cites S399) also fires `prov` unless S399 is added to the entry's `source:` line (prov requires every K-cited id in `source:`). Fine if the harness tests "contains"; a harness requiring the single listed leg fails. Scope reads the registry row the K row CITES (control 5 requires this), not the frozen sid.
3. **Dropped/duplicate/unsplittable row.** Only `row:<id>` is printed; every cell-reading leg is "not evaluable", not listed, and the row counts in no a..e figure (matches control 7 listing only `row:K17`). Alternative: list every dependent leg too.
4. **Rows with parseable cells but a semantic grammar failure** (short proposition, bad src cell, wrong pin cell, duplicate proposition) still get all other legs evaluated.
5. **source_cell "exactly one registry row of 11 cells".** I require exactly one row with that id at all, and it must have 11 cells (a second malformed row with the same id fails it). Alternative: exactly one 11-cell row, ignoring malformed duplicates. Registry is read line by line with NO fence/comment exclusion (§C1 states that exclusion only for entry rows). Ids must match `^ {0,3}\|\s*S[0-9]{3,}\s*\|` (4 leading spaces = not a row, shown in selftest).
6. **used-by "names the entry path":** path must occur not embedded in a longer path/name (`…r56.md.bak`, `x/corpus/…` fail; trailing `.` ok). Alternative: plain substring. URL = last `https?://\S+` token (a trailing byte breaks `endswith`). `rev_rule` key `Hyprland-*` is matched with fnmatch; tokens by substring of the URL.
7. **scope locator list:** `N|N-M` items separated by `,` + optional spaces/tabs, list starts immediately after `<basename>:` (so `: 492` fails), every occurrence tried; basename matching is a plain substring (so `Hyprland-legacy-ConfigManager.cpp:` matches `ConfigManager.cpp:`); `500-400` includes nothing.
8. **num:** "a digit run of the quote" = any `[0-9]+` run of the row's quote cell (neighbours ignored; the proposition side uses the stated lookaround regex). Strict alternative: only runs that the same regex finds in the quote (then `H03` could not use `50993780079460`). Line numbers and 0..3 compare as canonical decimals (`0148` ≠ 148; alternative: integer value). `0.56.2` in a proposition fails (56 is neither in the quote nor a frozen line) — writers must avoid it.
9. **tok/num use the row's own quote cell** (backticks stripped), not the frozen quote; they only differ if the quote leg already fails.
10. **prov:** `verified-at: 2026-10-28` must be an exact whole line, exactly one in the first 30 raw lines (fences not excluded); order uses the first `source:` and first `recheck:` line; S-ids are read from every `source:` line in the window; "registry row" = at least one regex-matching row with that id. S-ids cited by K rows come from the K rows' own cell 3.
11. **index:** README lines are not fence/comment-filtered (not stated for the README); any line starting `| ` + backtick + `knowledge/hyprland-config-autoreload-r56.md` + backtick counts, exactly one required.
12. **proposition uniqueness:** compared against every other row that has a well-formed 5-cell line; every row of an identical pair fails `row:`.
13. **pin_hash** covers `pin_sha256` (8) AND `host_pin_sha256` (4, including `host-watched-lstat.txt`, which no row quotes): "every pin blob" — alternative reading: only the 8 + 3 referenced pins.
14. **entry absent:** `entry_absent` + `tables_sha`, `index`, `pin_hash`, `new_rows` still evaluated (§C1 only says rows/hosts/sources/scope/content print 0). **Tables with wrong sha** but valid shape are still used to evaluate (list-all), `tables_sha` fires; wrong sha + invalid shape evaluates nothing table-dependent; right sha + invalid shape = rc 2; absent tables = `tables_sha` only.
15. `new_rows` uses `c1.rows` (S383..S390 → pin) and the same registry conditions as `source_cell` minus the frozen-sid equality; the `/8` is a constant (also `new_rows_min` must equal 8).
16. Registration says "`<pin>:<line>` equals the frozen pin file name and line" inside the row grammar and also lists no separate anchor leg, so a wrong pin cell is `row:` only (unlike r55's `anchor:`).

Observation for the harness author: control 2's placeholder text contains `source`, so K23 keeps `tok` (content=1/33, still `e<33`); control 1 prints new_rows=8/8 since the registry is untouched.

## Not verified / limits
- Never ran against the real entry (does not exist at the freeze commit); the witness is my own synthetic entry, built from the frozen tables and the real pins.
- Never ran the harness `quality/check-r56-controls.py` (not mine); my controls 1-10 are my reading of the registration text.
- Entailment of propositions is not checked (declared limit). A tokens-sharing forgery with only quote numbers passes, as registered.
- The tool only checks `--repo` is the repository root via `rev-parse --show-toplevel` (copied from the r55 D1 fix); a bare repo is not exercised.
- Scratch under `/fast/scratch/hyaku/mado-r56/R56ExecC1CounterA/` removed after this report.
