# CritC2Gaming: does the landed C2 note reach 3/3 for honest reasons?

Verdict: **honest 3/3.** No terminal counts only through a hole. Every counted id sits in an unfenced Markdown table row. It is cited in that row's `sources` cell as a bounded token, and it resolves to a single 11-cell row in the `## Registry` section. Every counted row's pinned upstream bytes re-fetch with byte counts and sha256 identical to the registry. One counted id, S149 (the foot wiki), passes the upstream test only through the prefix hole (V2-H6). Its target is upstream's own wiki, so the pass is honest, and foot keeps 7 ids without it. One provenance defect in the note does not affect the count: the ghostty C5 row's "§4" reference is dangling.

Scope: the lane tip 2f1134f38930fc8b067d2d7f5bba126338faabdd. The note and the SOURCES rows S123-S152 landed at c8cb3930. The counter is `.ufo/waves/round-23/c2/count.py` v2, last changed at 4de44647, with sha256 at the tip `fc5b533c...`, identical to the working copy. The holes are those listed in `w1/reports/RevC2Counter.md` for v2.

## 1. Re-run of the registered after-value

- Command: `prlimit --as=402653184 timeout 15 python3 -I .ufo/waves/round-23/c2/count.py 2f1134f38930fc8b067d2d7f5bba126338faabdd`, run in the lane.
- Result: 3/3, exit 0. foot has 8 ids (S140, S141, S144-S149). kitty has 9 (S123-S130, S133). ghostty has 8 (S134-S139, S150, S151).
- `cmp` against `evidence/c2-after-2f1134f3.json` shows the output is byte-identical to the L1 receipt.
- The RevC2Counter v3 candidate (`RevC2Counter-work/count_v3.py`, sha256 `5d0206ef...`) was copied into my scratch clone so that its `parents[4]` lookup resolves to a lane clone. At the same revision it gives 3/3, exit 0, with the same id sets per terminal. It reports `duplicate_ids: []` and `malformed_registry_rows: []`. v3 closes the duplicate-id, Leads-scope, fence, table-scope, id-prefix and upstream-boundary holes, so this alone shows none of those holes is load-bearing.

## 2. Per-row hole check

The script is `/fast/scratch/hyaku/mado-r23/CritC2Gaming-work/holes.py` (sha256 `14e15665...`). It reads only through `git show` at the tip. Its output is `holes-at-tip.json` (sha256 `4340ecde...`). It checks every route row the v2 counter accepts and recomputes the count under each stricter rule separately.

| Hole (RevC2Counter id) | What the tip shows | foot / kitty / ghostty under the strict rule |
|---|---|---|
| Fenced rows (V2-H3) and pipe lines with no table (V2-H4) | The note has no fences. All 18 accepted route rows (lines 28-32, 38-42, 48-52 and 63-65) sit in tables with a header and a delimiter row. | 8 / 9 / 8 |
| Duplicate ids (V2-H1a-c) | No `S###` id starts more than one row anywhere in SOURCES.md. | unchanged |
| Registry scope, Leads (V2-H2) | S123-S152 each appear once, under `## Registry`, unfenced. No new id appears under `## Leads (unopened)`, `## Paths` or `## Search log`. The only other mention of a new id is S123 inside S132's own registry row. | unchanged |
| Id prefixes (V2-H5a/b) | The loose `S\d{3}` and the bounded token give the same ids on every accepted row. Nothing like `S1400` or `XS140` appears. | 8 / 9 / 8 |
| Ids cited outside the `sources` cell | Every counted id is in that row's `sources` cell. The ghostty rows also repeat ids in their prose cells, but no id counts only through prose. | 8 / 9 / 8 |
| Upstream prefix boundary (V2-H6) | S149's source cell contains only `codeberg.org/dnkl/foot.wiki.git`, which passes the substring test `codeberg.org/dnkl/foot`. Every other counted row has a bounded upstream match. | **7** / 9 / 8 |
| Annotation words in route rows (V2-H13/H14) | No accepted route row contains unused, rejected, retracted, withdrawn, superseded, queued, unopened, placeholder, todo, tbd, stub, fake, invalid, dead or obsolete. The one queued source, S132, is not cited by any route row and is not counted (status `queued`, used-by `—`). Foot row 31 says the wiki spelling is "stale for 1.28.0". That bounds the claim and does not mark the row as unused. | 8 / 9 / 8 |
| 12-cell or double-space rows dropped silently (V2-H10, V2-H15) | All 30 new rows parse to exactly 11 cells. | unchanged |
| Bookkeeping-only rows (V2-X1) | See section 3. Every counted row's bytes re-fetch and match. Rows that only do bookkeeping (S131 and S152, which are changelogs, plus S142 and S143) are cited only in the `source:` header line. That line is not a table row, so these ids are not counted. The host-declaration rows (63-65) cite no id and add nothing. | unchanged |
| All rules at once | | **7 / 9 / 8, still 3/3** |

S149 is the only id that rests on a hole. The prefix hole lets a fork or neighbouring repository pass. Here the neighbour is `dnkl/foot.wiki`, upstream's own Codeberg wiki for the same project, and the row marks it as "NOT pinned to a release tag". Even v3's boundary rule (next character not in `[A-Za-z0-9_-]`) would accept it, because the next character is `.`. Foot does not need it: rows 28-30 and 32 carry S140, S141 and S144-S148.

## 3. The bookkeeping-only attack: re-fetching the counted rows' bytes

`pins.py` (sha256 `eab1d6e7...`) extracts each counted row's raw-fetch URL, sha256 and byte count. Then:

- The 24 rows with a raw URL were fetched with `curl -sSL --max-time 40`, one at a time. All returned HTTP 200, and all 24 match on bytes and sha256. The receipt is `refetch.json` (sha256 `6b5fc2bb...`). For S134 and S135 the comparison used the pinned website-repo `.mdx` digest, not the moving rendered page.
- S149: `git clone --bare https://codeberg.org/dnkl/foot.wiki.git`, then `git show 2475351a:Home.md`. The output is 32739 bytes with sha256 `78bd64dc...`, which matches. Lines 1011-1015 are the FAQ "How do I reload the configuration? Restart foot ...".
- Tag pins, checked with `git ls-remote`:
  - foot `1.28.0` peels to `ab33c9a1...` (tag object `3d97bba5`).
  - kitty `v0.49.2` peels to `b2cb8712...` (tag object `e3005973`).
  - ghostty `v1.3.1` peels to `332b2aef...` (tag object `22efb0be`).
  - ghostty `v1.2.3` peels to `6d2dd585...` (tag object `ae9b7892`).
  
  All match the note and the rows.
- Content spot-check of each terminal's search-path row in the fetched bytes:
  - S140 `foot.ini.5.scd:14-20` gives `XDG_CONFIG_HOME/foot/foot.ini` (defaulting to `$HOME/.config/foot/foot.ini`), then `XDG_CONFIG_DIRS`.
  - S145 `config.c:421-473` has `"/.config/foot/foot.ini"`.
  - S124 `simple_cli_definitions.py:366-370` lists `$XDG_CONFIG_HOME`, then `~/.config`, then `$XDG_CONFIG_DIRS`, and the first that exists is used.
  - S125 `utils.h:202-244` has `KITTY_CONFIG_DIRECTORY`, `XDG_CONFIG_HOME`, `~/.config` and `XDG_CONFIG_DIRS`.
  - S134 `index.mdx:36-55` has `$XDG_CONFIG_HOME/ghostty/config.ghostty`, which defaults to `$HOME/.config`.
  - S136 has `ghostty/config.ghostty`, and S137 has `XDG_CONFIG_HOME` with `.config` as the default.

  The cited spans state the routes the rows claim.

So V2-X1, where self-written rows reach 3/3 with nothing opened, does not describe this landing. Every counted row is backed by public, pinned bytes that re-hash to the registered digest.

## 4. Defects found that do not affect the count

1. **The "§4" reference is dangling.** It is in the note, ghostty row C5, line 52: "Negative claim, sweep recorded in §4." The note has no §4; its sections are Upstream contract, Host declaration, Safe observation, Unexercised behavior and Supersedes. The text was copied from `w1/reports/SrcGhostty.md` line 169. That report's §4 holds the two site-versus-source conflicts, not the sweep. The sweep appears there only as a command (line 53), with no recorded result. That report directory is also untracked at the tip (`git status` shows `?? .ufo/waves/round-23/w1/reports/`), so the note's header citation "reports under .ufo/waves/round-23/w1/reports/" names files that are not committed. This affects provenance only: S139, the only id C5 cites, is also cited by row C4 (line 51), so the ghostty count does not change. The smallest correction is to cite the sweep where it is actually recorded, or record its command and result in the note. I did not re-run the v1.3.1 treewide sweep, so the negative claim itself is unverified by me.
2. **S149 passes on a prefix match** (section 2). It is honest today. The counter could still accept a real fork under the same prefix. That is a counter defect that the v3 boundary rule narrows; it is not a defect of this landing.

## 5. Commands and receipts

- Lane, read-only:
  - `git rev-parse HEAD master` returns 2f1134f3 for both.
  - `git log --oneline -6 <tip>`.
  - `git show <tip>:corpus/knowledge/terminal-trees-r23.md`.
  - `git show <tip>:corpus/SOURCES.md`.
  - `git show <tip>:.ufo/.../c2/count.py | sha256sum`.
  - `git log -- c2/count.py` shows the last change at 4de4464.
  - The v2 counter run (section 1), `git status --short --ignored` on `w1/reports/`, and `git ls-files`.
  - No jj command was run. The only lane write is this report.
- Scratch:
  - The clone is at `/fast/scratch/hyaku/mado-r23/CritC2Gaming`. It is used only to host the v3 counter copy; nothing was committed.
  - The work directory is `/fast/scratch/hyaku/mado-r23/CritC2Gaming-work/`. It holds `holes.py`, `pins.py`, `holes-at-tip.json`, `pins.json`, `refetch.json`, `v2-at-tip.json`, `v3-at-tip.json`, `fetched/S1xx` and `foot.wiki.git`.
- Every counter or analyzer child ran under `prlimit --as=402653184 timeout 15 python3 -I`, one at a time, over committed bytes.
- Installs or updates: none. I used python3, git, curl, prlimit and timeout, all already present. The host was not changed.
- Not done:
  - I did not re-run the ghostty v1.3.1 treewide sweep behind C5.
  - I checked claim correctness beyond the search-path spot-checks only for the counted spans named above; the other claims are left to the note-claims reviewers.
  - I did not re-hash the host-file sha256 values in the host-declaration table. Those rows cite no id and do not affect C2.

Verdict: C2 3/3 at 2f1134f3 is honest. foot (7 of 8 ids, or 8 counting the wiki), kitty (9) and ghostty (8) each count through unfenced table rows, sources-cell citations and unique registry rows whose pinned bytes re-hash. No terminal counts only through a hole. The correctable defect is provenance only: the dangling "§4" in ghostty row C5, and a header that cites uncommitted w1 reports.
