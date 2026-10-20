# MadoR19.RerunSweep — partial

Attack on `.ufo/waves/round-19/supersede-sweep.py` (tool sha256 `fd7c31df15e43309e7c425f811bdfb3fcd16cadf9698277e2e6ac665bd7a7dc4`, ledger sha256 `87644b585eb486c0056c3b9800966a0d5a3d6e582f77141a8716adde0cd38d58`; both equal the blobs at `01b8094` — `git cat-file -p 01b8094:<path> | sha256sum`. The ledger worktree file was then extended by a sibling seat at 15:07:33-0300; §9 covers that, and it is not part of the measured baseline above).

**Verdict.** The tool's own documented contract holds and all three assigned probes behave exactly as claimed. Red and green arms reproduce independently. What breaks is the *meaning* attached to POINTED: it is satisfied by a round-18 span citation (`corpus/README.md:44`, sole satisfying line, introduced by `4c103b5`), so it does not test QUALITY 28's "in the same round"; the `new`/`old` literals are unanchored substrings; row validity is unchecked; a scope that matches zero files (or drops three of the thirteen) exits 0 with no denominator; and five file classes are invisible to the sweep.

All mutations were made in a throwaway clone (`git clone /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/sweep-attack`, checked out `01b8094`), and the clone's own copy of the script was run so `LANE` resolved to the clone. `git reset --hard 01b8094` after every probe.

## 1. Independent re-run of the claimed arms (in the lane, read-only)

```
$ python3 -I .ufo/waves/round-19/supersede-sweep.py 9c54c56
supersede-sweep: walker-2.17.2 rev=9c54c56a6a7528675027b7f628f97a1b8d1b8e8d files=13 pointed=2 stale=11
STALE SKILL.md ; POINTED corpus/README.md ; STALE … (9 more) ; POINTED corpus/knowledge/walker-route-r18.md ; STALE tools/mado-verify.sh
exit=1
$ python3 -I .ufo/waves/round-19/supersede-sweep.py df84807      → files=13 pointed=13 stale=0, exit=0
$ python3 -I .ufo/waves/round-19/supersede-sweep.py 01b8094…d154 → files=13 pointed=13 stale=0, exit=0
```

Reproduces lesson `corpus/lessons/round-19.md:18` and QUALITY `corpus/QUALITY.md:187-188` exactly (13/2/11 red, 13/13/0 green). Cross-check of the denominator: `python3 -I .ufo/waves/round-19/fresh-pins.py 9c54c56` → `"denominator": 13, "current": 2`, and its per-file `pointer_lines` for `corpus/README.md` is `[44]` — the two counters agree, and they agree on the same incidental line (finding 3).

## 2. The three assigned probes (clone, each a committed synthetic tree on top of `01b8094`)

| probe | file added | result |
|---|---|---|
| T1 no pointer | `corpus/knowledge/z-stale-plain.md` = "Walker is pinned at 2.17.0 on this host; nothing else follows." | `files=14 pointed=13 stale=1`, `STALE corpus/knowledge/z-stale-plain.md`, **exit 1** — as claimed |
| T2 pointer S999 | same old line + `Superseding note: walker 2.17.2 (S999).` | `stale=2` (`z-ptr999.md` and the T1 file still present in that tree), **exit 1** — S999 is not permitted |
| T3 pointer S096 | same old line + `Superseding note: walker 2.17.2 (S096).` | `files=14 pointed=14 stale=0`, `POINTED corpus/knowledge/z-ptr096.md`, **exit 0** |
| T3b span | `walker 2.17.2 (S090-S096)` | POINTED, exit 0 (span convention works) |

T1's tree also confirms a *new* in-scope file stating the old value is caught; the check is not merely a fixed file list.

## 3. Live overclaim: `corpus/README.md` is POINTED only on a round-18 line

Computed with the script's own `glob_path`/`covered_rows` over `01b8094` committed bytes — for each of the 13 files, the lines satisfying `pointed()`:

```
=== corpus/README.md  satisfying_lines=1
  :44: | `knowledge/walker-route-r18.md` (round 18; surface P3) | Documentary upstream contract for Walker v2.17.2 … | `source:` S072–S091 in [SOURCES](SOURCES.md); …
```

`corpus/README.md:44` is the coverage-map row for a *different* note. Its pointer channel is the span `S072–S091` (covers S090) plus the string `Walker v2.17.2`. It is not about the README's own `2.17.0` text at `:135` ("2.17.0-era pins … are dated, not current") or `:139` ("the 13 owned files that said `2.17.0` carry dated pointers to S090/S091/S096"). The round-19 paragraph does not satisfy the predicate line-wise: `2.17.2` is on `:138` and `S096` is on `:137` — different lines.

Provenance: `git log -S'Documentary upstream contract for Walker v2.17.2' -- corpus/README.md` → `4c103b5` (round 18), and `git show 9c54c56:corpus/README.md | sed -n 44p` still contains `S072–S091`. Consequence: at the **red** baseline the 2 "pointed" files are both round-18 text — `corpus/README.md:44` and `corpus/knowledge/walker-route-r18.md:1`, the latter the note's `source:` header, which lists S072…S091 explicitly (S090 among them: `sed -n 1p | grep -o 'S[0-9]\{3\}'` gives S072–S091 at `9c54c56`, S072–S091+S098 at tip) next to `v2.17.2` fetch URLs. `git log -S'S090' -- corpus/knowledge/walker-route-r18.md` → only `4c103b5`, the commit that also added the file. Zero round-19 pointers existed at `9c54c56`. So `POINTED` means "the file contains, anywhere, a line with the new string and a row token" — not QUALITY 28's "carries, **in the same round**, an in-file pointer" (`corpus/QUALITY.md:183`). The green delta 11→0 is still real; the naming is what overclaims.

Same class, second instance: `SKILL.md`'s first satisfying line is `:573`, the registry row that documents this very ledger ("… id `walker-2.17.2`: old `2.17.0`, new `2.17.2`, rows S090 and S096 …"). A file that quotes the ledger passes; SKILL.md also has genuine errata (`:1853-1864`), so the file is fine, the mechanism is not.

## 4. Soundness holes in the predicates (latent — no live instance today)

- **`new` is an unanchored substring.** T8: file with `2.17.0` + `Changelog token: walker 2.17.20 (S096).` → `POINTED corpus/knowledge/z-17120.md`, **exit 0**. A line that does not carry 2.17.2 discharges the file. `new` is also matched inside `12.17.2`.
- **`old` is an unanchored substring.** T9: in-scope file whose only version is `12.17.0` → `STALE`, **exit 1**. False red.
- Not live: `git grep -nE '[0-9]\.?2\.17\.0|2\.17\.0[0-9]' 01b8094 -- <13-file scope>` and the same for `2.17.2` return nothing.
- **Row validity is unchecked.** T15: ledger `rows:["S999"]` over a file citing `2.17.2 (S999)` → `POINTED`, exit 0, although `corpus/SOURCES.md` has no S999 (rows stop at S098). QUALITY 28 requires "the SOURCES row that superseded it"; the check never consults `corpus/SOURCES.md`.
- Negative control: span widening via dates does **not** work. T10: `2.17.2 (S200-2026)` → `STALE`, because `SPAN`'s trailing `\b` rejects `2026` (only `202` matches the digit group, then digit `6` kills the boundary). The span channel itself is real and is what carries finding 3.

## 5. Vacuous green: no denominator, and `**` is not recursive

```
scope "corpus/knowledge/*.markdown" → files=0 pointed=0 stale=0, exit=0
scope "corpus/knowledge/"           → files=0 pointed=0 stale=0, exit=0
scope "corpus/knowledge"            → files=0 pointed=0 stale=0, exit=0
scope "corpus/knowledge/gone.md"    → files=0 pointed=0 stale=0, exit=0
scope "corpus/knowledge/**"         → files=10 pointed=10 stale=0, exit=0   # dropped README/SKILL/tools, still green
scope "corpus/**/*.md"              → files=14 pointed=12 stale=2, exit=1   # matches corpus/lessons/*.md, NOT corpus/README.md
```

A typo, a directory instead of a file, or a scope that silently loses three of the thirteen files all exit 0. Nothing asserts `files=13`; the count appears only on stderr. `glob_path` splits on `/` and `fnmatch`es components, so `**` degrades to `*` in one component — it is never recursive, which the docstring does not say. `fresh-pins.py` has a fixed `PIN_REV` denominator; this counter has none.

## 6. Scope holes (measured: the sweep cannot see these at all)

Each injected a present-tense old-value claim into the clone and re-ran; every injection run stayed `files=13 pointed=13 stale=0`, exit 0 (the deletion probe is the one count-changing row and is marked as such):

| class | probe | result |
|---|---|---|
| `corpus/knowledge/` subdirectory | `corpus/knowledge/sub/z-sub.md` (2.17.0, no pointer) | invisible |
| non-`.md` under knowledge | `corpus/knowledge/z-txt.txt` | invisible |
| `LOG.md` | appended "Present-tense LOG note: walker is 2.17.0 on this host." | invisible |
| `AGENTS.md` | appended same sentence | invisible |
| `tools/` subdirectory | `tools/sub/z-t7.sh` | invisible |
| uncommitted worktree | present-tense 2.17.0 appended to `walker-deep.md`, not committed | invisible (exit 0); documented "committed bytes only" |
| deletion | `git rm corpus/knowledge/walker-deep.md` → files=12, exit 0 | visible reduction only on stderr |

What is actually outside scope today, checked on committed bytes at `01b8094`: `git grep -l '2\.17\.0' 01b8094 -- ':!.ufo'` → 13 in-scope files plus `LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/lessons/round-{17-verifier-spotcheck,18,18-verifier-spotcheck,19}.md`, `plans/round-{7-record-draft,8-record-draft,9.plan}.md`. Reading them: `LOG.md:245` is a dated round-3 log line; `SCORECARD.md:1008/1030/1083`, `corpus/QUALITY.md:185`, `corpus/SOURCES.md:102-103`, the lessons and the plans are historical descriptions or plan text. `AGENTS.md`, `MINT.md`, `SHONEN.md` and the root `README.md` contain no `2.17` at all. [INFERENCE] No out-of-scope file states 2.17.0 as a present-tense pin, so the current green is not false *today* — but that is a reading of prose, not something the tool can assert, and a widening probe shows it: scope `+"corpus/lessons/*.md"` (+`corpus/*.md`, `*.md`, `plans/*`) gives `files=24 pointed=16 stale=8` (`STALE LOG.md, SCORECARD.md, corpus/QUALITY.md, corpus/lessons/round-17-verifier-spotcheck.md, corpus/lessons/round-18-verifier-spotcheck.md, plans/*`). Note `corpus/QUALITY.md` is STALE under its own rule — criterion 28's text puts `2.17.2` and `S090/S096` on separate lines.

## 7. File-level blind spot, quantified (disclosed limit, but stronger than stated)

- T16: old claim at `:3`, pointer at `:7` — "The gate pins walker 2.17.2 (S096) for OTHER rows only." → POINTED, exit 0. Distance is irrelevant; the pointer need not refer to the mention.
- T30: append `Current state 2026-10-20: walker 2.17.0 is installed (new present-tense line, no pointer).` to the already-pointed `corpus/knowledge/walker-deep.md` → still `pointed=13 stale=0`, exit 0.
- T31 control: the identical line in a new file → `STALE corpus/knowledge/z-newpin.md`, exit 1.

QUALITY 28's limit sentence says "one pointer line clears a file with other untouched mentions; a reviewer reads each pointer, the check only proves none is missing" (`corpus/QUALITY.md:188-190`). Measured, the check also does not notice a *re-introduced* mention inside an already-cleared file (T30), so it is not a regression guard for the next round — it is a one-shot presence test.

## 8. Complete / documented behaviour that held

`--help` → 0; `REV --ledger PATH extra` → 2 + usage; `--ledger=` → `could_not_evaluate: ledger : No such file or directory`, 2; malformed JSON → 2; missing ledger → 2; bad rev → 2; `rows:["S090-S096"]` (span string in rows) → `rows must be S### strings`, 2; duplicate id, `old==new`, empty scope → 2 (read in `load_ledger`); `rows:[]` permits any `S###` (T32: `See S777 for the new 2.17.2.` → POINTED, exit 0, as documented); multi-entry `# entry <id>` headers and per-entry stderr counts (T17); one stdout line per file, count line on stderr, nothing written (contract as stated in the docstring and SKILL.md:573).

## 9. Concurrent sibling ledger extension (uncommitted, not my baseline)

At 15:07:33-0300 a sibling seat rewrote the worktree `.ufo/waves/round-19/supersessions.json` (now sha256 `a0e6cfbe2f096602ce8f85132cefe37b0fdb9ddbd2f1172e46a65236d9cfb636`, 3 entries; committed blob stays `87644b58…`). I did not touch it. Running the committed tool with that worktree ledger against committed tip bytes:

```
$ python3 -I .ufo/waves/round-19/supersede-sweep.py 01b8094
supersede-sweep: walker-2.17.2  … files=13 pointed=13 stale=0
supersede-sweep: S094-to-S097   … files=3 pointed=2 stale=1
supersede-sweep: S084-to-S098   … files=2 pointed=1 stale=1
…
# entry S094-to-S097
STALE SKILL.md
POINTED corpus/README.md
POINTED corpus/knowledge/theme-route-r18.md
# entry S084-to-S098
STALE SKILL.md
POINTED corpus/knowledge/walker-route-r18.md
exit=1
```

Both new entries are red on `SKILL.md`, and the reason is structural: at `01b8094`, SKILL.md contains `S084` and `S094` only on line 572 (the `mado-anchor-durability` registry row: `git show 01b8094:SKILL.md | sed -n 572p | grep -o 'S0[0-9][0-9]'` → `S084 S094`), and contains `S097`/`S098` nowhere (`grep -c` → 0, 0). No seat has modified `SKILL.md` in the worktree (`git status`). The entries that do pass, pass on the sentence that announces the supersession itself — `corpus/README.md:141` ("S097 supersedes S094's per-fetch GitHub") carries old, new and row on one line, so row-id supersessions are self-satisfying exactly where the announcement exists: the first satisfying line for the new entries is the description, not a pointer to an owned mention. `corpus/knowledge/walker-route-r18.md:327` is a real in-place replacement ("S084 … was replaced in place by S098").

If this ledger is meant to land in this wave, the check will be red (exit 1) until SKILL.md gains an S097/S098 line in one of those rows' scope. Flagged, not fixed — the file is another seat's.

## Limits

- Everything above is the clone at `01b8094` plus synthetic commits; no lane file was edited and no gate was run.
- "Present-tense vs historical" outside scope is a judgement on prose ([INFERENCE]); the tool has no such distinction, which is the point of §6.
- I did not audit the honesty of all 13 pointers' *wording* beyond the satisfying-line census in §3 (that is `MadoR19.CriticC2W2`/`CriticC1W2` territory). I did verify each file has ≥1 satisfying line and quoted the first.
- `2.17.20`/`12.17.0` are synthetic; `git grep` shows no live instance, so those two are reported as latent, not live.
- The `S072–S091` span-credit reading is [INFERENCE] of the lane's citation convention as the docstring defines it; the bytes (line 44 at red) are observed.

## Installs

none.
