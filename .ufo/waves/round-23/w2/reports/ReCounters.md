# ReCounters — wave-2 falsification: C2/C3 re-measure + sources census (2026-10-22)

Reviewer seat MadoR23.ReCounters. Leaf: no subagents dispatched. No lane files edited; only this
report written. No tools installed or updated (nothing was needed; tooling directive registry:
none).

## Verdict summary

- **C2 coverage: PASS.** After at landed tip 2f1134f3 = **3/3, exit 0** (target 3/3). Before at
  base e33ea304 = **0/3, exit 1** — byte-identical to the registered v2 receipt. Counter v2
  audited line-by-line; credited S-row sets hand-recomputed from the committed note and they match.
- **C3 calibration: PASS.** After at landed tip 2f1134f3 = **0, exit 0** (target 0). Before at
  base = **5, exit 1** — matches the v2 receipt (registration's clarification 4; the older "4"
  was the v1 shell form). PROVINCE.md accounts for exactly the 5 tracked tools; the five rows'
  stated read/write scopes spot-check true against the tool code.
- **Census: exit 0.** 7 W04 duplicate-url warnings + final `mado ok` line. W04 is a warning that
  never changes exit status (script contract and its own selftest `W04-does-not-fail-validation`
  expects exit 0). All 7 W04 ids are pre-round-23 rows (S030–S121); the round-23 rows S123–S152
  added zero new W04 findings.

## What I ran (exact commands, cwd = /home/vgpnk/Projects/shokunin/mado-shokunin unless noted)

1. `python3 -I .ufo/waves/round-23/c2/count.py 2f1134f38930fc8b067d2d7f5bba126338faabdd` →
   `{"rev": "2f1134f3…", "counter_version": 2, "note_present": true, "terminals":
   {"foot": ["S140","S141","S144","S145","S146","S147","S148","S149"],
    "kitty": ["S123","S124","S125","S126","S127","S128","S129","S130","S133"],
    "ghostty": ["S134","S135","S136","S137","S138","S139","S150","S151"]},
   "count": "3/3"}` — **exit 0**.
2. `python3 -I .ufo/waves/round-23/c3/count.py 2f1134f38930fc8b067d2d7f5bba126338faabdd` →
   `self_assessment: "- [~] No cross-domain bleed (PROVINCE.md still accurate)"`,
   `tracked_tools` = the 5 tools, `accounted_rows` = the same 5, `mismatches: []`,
   `count: 0` — **exit 0**.
3. `python3 -I .ufo/waves/round-23/c2/count.py e33ea30461f6e9bbeee40beef19770a953f7a105` →
   `note_present: false`, all terminals `[]`, `count: "0/3"` — **exit 1**.
4. `python3 -I .ufo/waves/round-23/c3/count.py e33ea30461f6e9bbeee40beef19770a953f7a105` →
   same 5 tracked tools, `accounted_rows: []`, all 5 listed as mismatches, `count: 5` — **exit 1**.
5. `cwd=/home/vgpnk/Projects/shokunin`: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
   validate --root /home/vgpnk/Projects/shokunin mado` — full output, **exit 0**:
   ```
   mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
   mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
   mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
   mado	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
   mado	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
   mado	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
   mado	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
   mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
   ```

My four counter runs match the registered receipts byte-for-byte in every JSON field:
`evidence/c2-before-v2-e33ea304.json`, `evidence/c3-before-v2-e33ea304.json`,
`evidence/c2-after-2f1134f3.json`, `evidence/c3-after-2f1134f3.json`.

## Measurement identity checks

- `git rev-parse HEAD` = 2f1134f3… = the landed tip; working copy clean
  (`git status --porcelain` empty) for both counters, SOURCES.md, the note, PROVINCE.md, SHONEN.md.
  Working-tree script bytes are therefore the committed tip bytes.
- Both counters read committed bytes only (`git -C LANE show <rev>:<path>`); LANE resolves via
  `Path(__file__).resolve().parents[4]` = the lane root. Revs are data, so running the tip's
  counter bytes over the base rev is exactly the registered before/after protocol (clarification
  10: after-values on committed bytes, not working-tree drift).
- The counters are net-new between base and tip (`git diff --stat e33ea304 2f1134f3` shows 101+78
  insertions, 0 deletions), i.e. absent at base; the same tip bytes produced both of my
  measurements, so the before/after delta is not a counter change. v1 exists only in lane history
  (6b383c46), as the docstrings state.
- Tip classifier hash: `git show 2f1134f3:tools/mado-tripwire.py | sha256sum` =
  `41489991163627f56de79bc360d4f13454fa5d50787a5802927b9cac562ca009` — matches the registered
  landed C1 artifact.
- Note: the lane's `master` ref sits at 6b383c46 while the working-copy HEAD is the landed tip
  2f1134f3 (jj-colocated). All my reads used explicit revs, so this did not affect any number.

## Falsification attempts that failed (i.e. the claims held)

**C2 mechanism and saturation.** Counter v2 requires, per terminal: a note table row whose first
cell is exactly that terminal (backticks optional), a `~/.config/<T>/` cell, and a cited S-row
with exactly 11 cells, status `mined`, opened `2026-10-22`, a source cell naming T whole-word,
naming neither other terminal, containing T's upstream (foot: codeberg.org/dnkl/foot; kitty:
github.com/kovidgoyal/kitty or sw.kovidgoyal.net/kitty; ghostty: ghostty.org or
github.com/ghostty-org/ghostty), and a used-by cell naming the note. Hand-recomputing the union of
S-tokens cited by the note's five foot, five kitty and five ghostty route rows gives exactly the
sets the counter printed ({S140,S141,S144–S149}, {S123–S130,S133}, {S134–S139,S150,S151}). The
note's prose `source:` line additionally cites S131, S142, S143, S152, but no route row cites
them, so the counter correctly does not credit them; S132 is queued ("stays queued and supports
nothing") and cannot pass. Full-row reads of S123 and S140 confirm the tail cells
`| mined | 2026-10-22 | on-release | corpus/knowledge/terminal-trees-r23.md |`, 11 cells, source
cells naming exactly one terminal at its upstream (github.com/kovidgoyal/kitty;
codeberg.org/dnkl/foot), no cross-terminal words. Before-value 0/3 is honest: the note file simply
does not exist at base.

**C3 mechanism and saturation.** Counter v2 evaluates only while SHONEN box 4 is asserted (it is
`[~]` at both revs), counts tracked `tools/**.py|**.sh` recursively (`git ls-tree -r` — exactly
the 5 files at tip, no subdirectory stragglers), and accepts only a PROVINCE table row whose
first cell is the backticked tool path with ≥4 non-empty cells. At base no PROVINCE table row
names any tool (bare prose mentions don't count) → 5. At tip the Round-23 refinement table names
all 5 → 0. The 5 accounted rows are the 5 tracked files, so the target was reached by naming, not
by shrinking the population; no tool was removed.

**PROVINCE honesty spot-checks (calibration axis).** Each row's stated scope against the code:
- `mado-tripwire.py`: `lstat` + `S_ISLNK` refusal and realpath guard confining reads to
  `~/.omp/agent/sessions` (lines 3001–3043); `REFUSED_NAMES = ^agent\.db`; zero write-mode
  calls (`mkstemp|NamedTemporary|open(...,'w'|makedirs|mkdir|.write(` → no matches). Matches the
  "reads transcripts, writes nothing" row.
- `mado-action-plan.py`: `O_NOFOLLOW` + `S_ISREG` regular-file-only reads (lines 150–160);
  `--selftest` runs inside `TemporaryDirectory(prefix="mado-plan-selftest-")` on a snapshot copy
  of itself (lines 702–705). Matches its row.
- `mado-assessment.py`: `is_symlink()` refusals, 2 MiB `MAX_BYTES` bounded read,
  `resolve().is_relative_to(root)` escape check (lines 41–66, 222–223). Matches its row.
- `mado-verify.sh`: selftest scratch only under `/tmp/w5-mado-m52-selftest.*`, regression scratch
  under `/tmp/mado-verify-regression.*`, prefix-guarded cleanup. Matches its row.
- `mado-evidence-audit.py` row not code-checked (reads/writes claims are C1 scope; its
  accounted-for status is what C3 measures).

## Findings by severity

- **Blocking: none.**
- **Low (measurement note, no action required):** the census validates the fleet *working tree*,
  not a revision; its result reflects every lane's current checkout, so it is evidence about
  today's tree, not about 2f1134f3. The round's byte-exact-census receipt requirement is still
  met by pasting this run's output.
- **Info (counter laxity, harmless here):** C2's whole-word regex excludes only `[a-z0-9]`
  neighbours, so punctuation-adjacent forms (`foot.ini`, `kitty.conf`) count as "naming" the
  terminal. Every credited row also passes the exclusivity + upstream + used-by gates and names
  the terminal genuinely, so no credit in this measurement rests on the laxity. Worth knowing if
  the counter is reused elsewhere.

## Residual risk and verification gaps

- S-row tail cells (`mined | 2026-10-22 | on-release | note`) were verified in full for S123 and
  S140 only; the remaining 28 credited rows passed the same mechanical gate over committed bytes
  (code read, logic sound), but I did not eyeball each raw row.
- `mado-evidence-audit.py`'s PROVINCE row was not spot-checked against its code (see above).
- C1 repair/guards numbers were out of my scope (other seats own them); I only confirmed the tip
  classifier hash matches the registered landed artifact.
- LSP was not used: the artifacts here are data files and counter scripts with no language server
  attached; all checks were exact-run and committed-byte reads.
