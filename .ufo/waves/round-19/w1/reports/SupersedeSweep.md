# SupersedeSweep — checker + ledger built; red 11 STALE / 2 POINTED at 9c54c56 and 17661e0, green 13/13 in a /tmp clone, zero divergence from fresh-pins at red

Scope: criterion check for R18-V3 (round-18 verifier spot-check `corpus/lessons/round-18-verifier-spotcheck.md:119`: eleven owned files state walker 2.17.0 pins with no in-file pointer). I own exactly two files plus this report; L1 integrates.

## 1. Delivered

| Path | Size | Lines | sha256 |
|---|---|---|---|
| `.ufo/waves/round-19/supersede-sweep.py` | 7,326 B | 191 | `fd7c31df15e43309e7c425f811bdfb3fcd16cadf9698277e2e6ac665bd7a7dc4` |
| `.ufo/waves/round-19/supersessions.json` | 311 B | 13 | `87644b585eb486c0056c3b9800966a0d5a3d6e582f77141a8716adde0cd38d58` |

Ledger holds the specified entry verbatim (`id walker-2.17.2`, `old 2.17.0`, `new 2.17.2`, `since 2026-10-20`, `rows ["S090","S096"]`, the five scope globs) under `{"schema":"mado-supersessions-r19-v1","entries":[…]}`; `python3 -m json.tool` parses it. Neither file is gitignored (`git check-ignore` rc 1, no output).

Contract as implemented: `supersede-sweep.py REV [--ledger PATH]` (default ledger next to the script). Committed bytes only (`git rev-parse --verify`, `git ls-tree -r -z`, `git show REV:path`); writes nothing. Per entry and per file at REV whose bytes contain `old`, stdout is exactly one line: `POINTED <path>` when some line carries `new` plus a permitted row token, else `STALE <path>`. One count line per entry goes to stderr (`supersede-sweep: <id> rev=<commit> files=N pointed=P stale=S`); `# entry <id>` headers appear only when the ledger holds more than one entry. Exit 0 no STALE, 1 any STALE, 2 usage or could-not-evaluate (bad rev, unreadable/malformed ledger, `git show` failure).

Scope globs match component-wise, so `*` never crosses `/` (`tools/*` is direct children only). Ledger entries are validated: non-empty `id` (unique), non-empty `old`/`new` and `old != new`, non-empty `scope`, `rows` of `S###` shape (default `[]`); violations exit 2.

**Span rule (decision, stated for review).** A citation range such as `S072–S091` (en dash, em dash, or ASCII hyphen; second `S` optional) counts as citing every row in the range. This is the lane's own citation convention (`corpus/README.md:44` cites `S072–S091`; `corpus/lessons/round-15-verifier-spotcheck.md:103-106`; round-17 notes cite `S056-S060`). It is also load-bearing for the declared red: at 17661e0 `corpus/README.md:44` contains `2.17.2` and the literal tokens `S072`/`S091` only, so S090 is matched solely through the span. Measured with literal tokens only, the same tree yields **12 STALE**; the declared 11 exists only with the span reading. If L1 wants literal-token semantics instead, the published criterion red must be restated 12 and `corpus/README.md:44` must gain `S090`/`S096`.

## 2. Red at the two revs (the criterion's red-before)

```
$ python3 -I .ufo/waves/round-19/supersede-sweep.py 17661e0fa83f978fb659f5bb8fef47f0969f6945
supersede-sweep: walker-2.17.2 rev=17661e0fa83f978fb659f5bb8fef47f0969f6945 files=13 pointed=2 stale=11   (stderr)
STALE SKILL.md
POINTED corpus/README.md
STALE corpus/knowledge/arc-synthesis.md
STALE corpus/knowledge/closeout-r11.md
STALE corpus/knowledge/config-health-report-r3.md
STALE corpus/knowledge/remaining-planes-census.md
STALE corpus/knowledge/walker-deep-r9.md
STALE corpus/knowledge/walker-deep.md
STALE corpus/knowledge/walker-live-surface.md
POINTED corpus/knowledge/walker-route-r18.md
STALE corpus/knowledge/waybar-walker-plane.md
STALE corpus/knowledge/waybar-walker-semantics.md
STALE tools/mado-verify.sh
rc=1
```

Same 13-file set, same 11 STALE / 2 POINTED, rc 1 at `9c54c56a6a7528675027b7f628f97a1b8d1b8e8d`. This matches the declared "red 11 STALE of 13" and the criterion-28 text "red 11 STALE at 9c54c56". The 13 owned files are byte-identical between `9c54c56` and `17661e0` (verified by `git show` length+content equality per path), so the two revs cannot differ here.

## 3. Divergence from fresh-pins (required comparison)

`python3 -I .ufo/waves/round-19/fresh-pins.py 17661e0…` → denominator 13, current 2 (`code`, `evidence/fresh-pins-before.txt:7-8`). Programmatic set comparison of the two outputs:

```
fresh-pins denominator: 13 current: 2
sweep files: 13 pointed: 2 stale: 11
set equal: True
path-set only in fresh-pins: []
path-set only in sweep: []
pointer-set equal (current vs POINTED): True
current-not-pointed: [] pointed-not-current: []
```

**No divergence at red** — same file set, same two passing paths (`corpus/README.md`, `corpus/knowledge/walker-route-r18.md`). Three semantic differences remain and should be known before green:

1. **Fixed vs re-derived denominator.** fresh-pins pins the numerator/denominator at `9c54c56` (`fresh-pins.py:16-19`); the sweep evaluates the tree at REV. A file that loses its `2.17.0` bytes drops out of the sweep; fresh-pins keeps it in the denominator as not-current. Verified in a clone: after replacing the old token in `corpus/knowledge/walker-deep.md` (commit `fb1c7052efe290215300d815dcd6b6b4cf198de2`), sweep prints `files=12 … stale=10` and no line for that file, while fresh-pins would still count it. Deleting the old text without a pointer is therefore a green path for the sweep but not for fresh-pins — the C2 claim must be satisfied by adding pointers, not by deleting mentions.
2. **Scope predicate.** fresh-pins' `in_scope` uses prefixes (`corpus/knowledge/` any depth, `tools/` any depth); the ledger globs are literal single-component patterns. Both select the same 13 paths at both revs (no subdirectory files in those trees today); they would diverge if `tools/` or `corpus/knowledge/` gained a nested file containing `2.17.0`.
3. **Row breadth.** fresh-pins accepts any `S###` on the pointer line; the sweep accepts only the ledger's `S090`/`S096`. A green fix that cites only, say, `S091` satisfies fresh-pins and stays STALE here. Every C2 pointer line should name S090 or S096.

## 4. Green arm (13/13, exit 0)

`/tmp` clone of the lane at 17661e0, copies of both files dropped at `<clone>/.ufo/waves/round-19/` (the script resolves the lane from its own path). Appended one line to each of the 11 STALE files — `# round-19 pointer: walker 2.17.2 (S096 host bytes; S090 /var/log/pacman.log:2929)` — committed as `37cb6b24824b2132e860adb6b6b72eda423ccc7a`:

```
supersede-sweep: walker-2.17.2 rev=37cb6b24824b2132e860adb6b6b72eda423ccc7a files=13 pointed=13 stale=0
POINTED SKILL.md
POINTED corpus/README.md
POINTED corpus/knowledge/arc-synthesis.md
POINTED corpus/knowledge/closeout-r11.md
POINTED corpus/knowledge/config-health-report-r3.md
POINTED corpus/knowledge/remaining-planes-census.md
POINTED corpus/knowledge/walker-deep-r9.md
POINTED corpus/knowledge/walker-deep.md
POINTED corpus/knowledge/walker-live-surface.md
POINTED corpus/knowledge/walker-route-r18.md
POINTED corpus/knowledge/waybar-walker-plane.md
POINTED corpus/knowledge/waybar-walker-semantics.md
POINTED tools/mado-verify.sh
rc=0
```

## 5. Negative and usage arms

Wrong row is rejected (the ledger's `rows` restriction does real work): clone commit `7eb6f0679f8756ed14ee0eb6df976702011e7f87` appends `# unrelated row: walker 2.17.2 per S999` to `tools/mado-verify.sh`; with `rows ["S090","S096"]` it prints `files=13 pointed=2 stale=11` and `STALE tools/mado-verify.sh` (rc 1). The same tree with a `rows: []` ledger prints `files=13 pointed=3 stale=10` and `POINTED tools/mado-verify.sh` — any-`S###` is the looser arm, as specified.

Usage / could-not-evaluate (stdout empty in every case):

| Command | rc | stderr |
|---|---|---|
| no args | 2 | `usage: supersede-sweep.py REV [--ledger PATH]` |
| `bogusrev123` | 2 | `could_not_evaluate: rev bogusrev123` |
| `9c54c56 --extra` | 2 | `supersede-sweep: unexpected argument --extra` + usage |
| `9c54c56 --ledger` | 2 | `supersede-sweep: --ledger needs PATH` + usage |
| `9c54c56 --ledger /tmp/no-such-ledger.json` | 2 | `could_not_evaluate: ledger …: No such file or directory` |
| ledger `old == new` | 2 | `could_not_evaluate: entry x: old equals new` |
| ledger `rows: ["S90"]` | 2 | `could_not_evaluate: entry x: rows must be S### strings` |
| ledger `{"entries":[]}` | 2 | `could_not_evaluate: ledger: no entries` |
| `-h` | 0 | docstring on stdout |

`--ledger=PATH` and `--ledger PATH` both accepted after the positional. Multi-entry ledger prints `# entry e1` / `# entry e2` headers and per-entry stderr counts. Determinism: two identical runs produce byte-identical stdout and stderr (`cmp` clean), stdout sha256 `6e074482c6b4b1fd2497bb9a9071e300f47fbba27681e41714ec9b7c74b33644` (13 lines).

Semantics exercised directly against the module (all as expected): glob `corpus/knowledge/x.md` vs `corpus/knowledge/*.md` true, `corpus/knowledge/sub/x.md` false, `tools/mado-verify.sh` vs `tools/*` true, `tools/sub/mado-verify.sh` false, exact `corpus/README.md`/`PROVINCE.md` true, `x/PROVINCE.md` false; pointer lines `S072–S091`+2.17.2 true (span), `S090`+2.17.2 true, `S072-S091`+2.17.2 true, `S999`+2.17.2 false, `S091`+2.17.0-only false, `S0960`+2.17.2 false; `rows=[]` accepts `S999`+2.17.2 and rejects 2.17.2 with no token.

## 6. CriticC1 falsification, measured (decision for L1)

CriticC1 reports appending `# S096 2.17.2` to the 11 stale files scores fresh-pins 13/13 while every old line stays untouched — true, and my green arm is exactly that shape, because the contracted rule is file-level (`new` + permitted row on one line, `old` not required there). Tightening the sweep to require `old` **and** `new` **and** a row on the same line measures **13 STALE at 17661e0** (zero files qualify: `walker-route-r18.md:1` carries no `2.17.0`, `corpus/README.md:44` none — its old token is `:135`; the other eleven have no pointer line). Literal-token strict is also 13. So the strict rule is not a drop-in: it restates the criterion's red 11 → 13, and green then requires each appended pointer line to narrate `2.17.0 → 2.17.2` with S090/S096 on one line. I did not change the contracted rule; I replied to CriticC1 with these numbers. L1 owns the choice; the tool change is a one-line predicate either way.

The sweep's aim is sweep-completeness (eleven files had no pointer at all — `round-18-verifier-spotcheck.md:119`); pointer prose quality is the anchor/durability criteria's ground, not this check's.

## 7. Old-token map at 17661e0 (where the sweep fix must land)

40 `2.17.0` occurrences across the 13 files: `SKILL.md` 23,114,1075,1475,1476,1822,1824,1825 · `corpus/README.md` 135 · `corpus/knowledge/arc-synthesis.md` 229 · `closeout-r11.md` 43 · `config-health-report-r3.md` 900 · `remaining-planes-census.md` 246 · `walker-deep-r9.md` 30,58,60,78,103,110,111,305,316,317 · `walker-deep.md` 27 · `walker-live-surface.md` 19,37,38 · `walker-route-r18.md` 13,60,223,224,245 · `waybar-walker-plane.md` 38,197,405 · `waybar-walker-semantics.md` 23 · `tools/mado-verify.sh` 56,60,3277,3278. (`SKILL.md:1822` is the round-18 erratum, which mentions 2.17.0 and 2.17.2 but no S-row token, so it does not point; the fix belongs there and in `mado-verify.sh:60` / `:3277` for the gate pin.)

## 8. Cleanliness

No git/jj write of any kind in the lane; only reads (`show`, `ls-tree`, `rev-parse`, `diff --name-only`). All git writes (`clone`, `add`, `commit`) happened in `/tmp/r19-sweep-clone*`. `git diff --name-only` at report time lists 11 tracked files modified in the working tree by sibling seats (the stale notes, `measure-mutants.py`, `tools/mado-verify.sh`) — not my edits; none of the readings above is affected because both counters read committed bytes at REV. Host pause respected: no pacman/yay/paru/expac, no sudo/systemctl/journalctl, no walker/elephant/omarchy/notification/screenshot/input command, no live gate. No web fetch.

## Limits

- Pointer lines need not be dated: `since` is documentation and is never parsed; no check that the pointer names the supersession date.
- Row ids are textual tokens, not registry lookups: `S096` passes even though no S096 row exists at `17661e0`; row existence/quality is the SOURCES census's ground.
- Span matching admits a broad prior-round range as a pointer for any row inside it (today only `S072–S091` ∋ S090 does this); a fixer could cite an old range rather than a dated round-19 pointer and pass.
- File-level granularity: one pointer line clears a file with many untouched old mentions (CriticC1's mutant) — inherent to the contracted rule, measured in §6.
- Files absent at REV are not classified (no fixed denominator); fresh-pins owns the fixed set, and the two can diverge on deletion as recorded in §3.
- Untested: paths containing `:` or newlines, non-UTF-8 bytes (line scan decodes with `replace` after byte containment of `old`), CRLF line endings (splitlines strips `\r`; `new` match unaffected), and a ledger with more than two entries beyond the header/count path.
- I did not run any lane suite, the live gate (`bash tools/mado-verify.sh`), `--selftest`/`--regression`, `measure.py`, or the census; those are L1's post-integration gate.

## Installs

none
