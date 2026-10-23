# ScoutReportShape — L1 report shape (round 28)

Axis: report conformance (not a C1/C2 claim). Read-only. No claim measured. Tip `4f610066efd90804b055c42ae20c41a7f44404f9` (`master`). Tool installs: none.

## 1. Sections in order (prompt §4 = `templates/round-prompt.md:99-129`, copied in `.ufo/prompts/mado-round-28.md:99-129`)

Report path: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-28/mado.md` (absent now). Headings, in order:

1. **Work performed** — opens with the 1–3 declared claims and their axes, then one bullet per item, each with a pointer (path:line, command output, or commit).
2. **Landed changes** — every change tied to a `LOG.md` entry and to the commit that carries it.
3. **Before → after measurements** — one per claim, each with the counting command and the commit measured.
4. **Sources & frontier** — rows before→after with the counting command, rows added by tier, rows touched old→new, frontier rows advanced. Conformance only, not a marker predicate.
5. **Trend verdicts** — `expansion`, `quality`, `discernment`, each `improved` | `harmed` | `unchanged` | `unprovable-but-better`, with evidence, no scalar. Not a marker predicate.
6. **SHONEN** — one line per `SHONEN.md` box.

Shape model: `.ufo/reports/round-27/mado.md` uses those six `##` headings in that order. r27 also put the sourced-claim sentence and the gate-quote location inside **Sources & frontier**. Prompt §2b (not a seventh heading) still requires them: lesson `corpus/lessons/round-28.md` `## Mistakes` (class · evidence · captured-by · fix, or the sweep that found none) and at least one claim citing an `S###` opened this round.

### SHONEN line-per-box form

Heading the driver accepts (`scripts/shokunin-watchdog.sh:162`): `^#+ SHONEN` or a bold list item `- **SHONEN**`. Contract text (`PROTOCOL.md:163-168`, prompt `:118-119`): one line per box, mark plus pointer.

```
## SHONEN
- [~] <box> — <resolvable pointer>
```

- `[x] <non-author verifier>` plus a pointer. A mado-dispatched seat is still the lane (`PROTOCOL.md:63-73`). A bare `[x]` counts as `[~]` for the gate.
- `[~]` is author-asserted, not skipped, and needs a resolvable pointer.
- `[ ]` if that box is untouched (prompt `:119`).
- Four boxes. Missing the heading fails the contract even if the facts sit elsewhere, and that assessment is disqualified for promotion (`PROTOCOL.md:163-168`).

`SHONEN.md:5-12` is four `[~]` lines. Do not write `[x]` this round.

## 2. Boxes → evidence this round

| box | needs | exists | pending / do not claim |
|---|---|---|---|
| 1. Decision tables, error patterns, checklists, cited sources | A real table, an error-pattern list, a checklist, each citing a resolvable source (`PROTOCOL.md:69-73`) | `SKILL.md:129` routing table, `:266` checklist, `:353` error patterns, `:593-635` gate registry, `:674` source trail. Historical: `corpus/knowledge/executor-test-sufficiency.md` (`SHONEN.md:5-6`) | Uncommitted D1: worktree `SKILL.md:633-635` no longer say `pending` (master still does). Uncommitted D8: `LOG.md` erratum names superseded `631-636` → `630-635`; not on `master`. `SKILL.md:721` historical `[x]` is not this report's mark (`SKILL.md:1849-1851`). |
| 2. End-to-end domain task logged in `LOG.md` | An executed task plus a `LOG.md` entry | Historical: `corpus/knowledge/config-health-report-r3.md`, LOG round 3 (`SHONEN.md:7-8`) | Registration bars a live desktop task (synthetic HOME only, `:108`). The uncommitted LOG block is a citation erratum, not an e2e log. Round LOG entry lands with the commit. Stay `[~]`. |
| 3. Executable without oral context | Self-contained instructions with resolvable pointers | `executor-test-sufficiency.md`; `registration.md:31-67` predicate commands; `c1/count.py`, `c2/count.py` | Seats dispatched this round are still the lane. Stay `[~]`. |
| 4. No cross-domain bleed; `PROVINCE.md` accurate | Province still the boundary | `corpus/knowledge/province-accuracy-selfaudit.md`. `PROVINCE.md` and `SHONEN.md` have empty `git status --porcelain` | No new outside approval. Registration `:124-129` bars sibling and config writes. Stay `[~]`. |

## 3. Frontier section — required content and the census

Exact spec command (prompt `:64-66`; paste output and exit at start and at end; end exit 0 required):

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
```

`validate` does not print a row count. Rows/tiers come from census mode, or from the frozen `CORPUS.md:135` grep. Both were run.

Start receipt `.ufo/waves/round-28/evidence/census-start.txt` (mtime 19:35, before `SOURCES.md` mtime 19:37): exit 0, seven `W04` lines (S030, S042, S045, S097, S119, S120, S121), then `mado ok …/corpus/SOURCES.md`. No row count in that file.

Counted on `master` (`git show master:corpus/SOURCES.md`, frozen grep/awk, exit 0): **182** rows; tiers **A=175 B=1 C=6**; status **mined=163 queued=10 rejected=9**. Last id S182.

Same validate command, this seat, exit 0: the same seven `W04` lines and `mado ok`. Census mode, exit 0: `mado rows 183`, `tier.A 176`, `tier.B 1`, `tier.C 6`, `status.mined 164`, `status.queued 10`, `status.rejected 9` (FLEET line matches; `missing 0`). Frozen grep: 183.

That 183 is the dirty tree, not the landed after. Diff vs `master` is append-only (`corpus/SOURCES.md` +11):

- Added by tier: **A +1**, S183, kind `paper`, status `mined`, opened 2026-10-23, `used-by` `corpus/knowledge/mutation-testing-r28.md` (`SOURCES.md:195`).
- Touched old→new: **none** (no in-place `status` / `recheck` / `used-by` edit).
- Frontier rows advanced: **none** (S183 is `mined` on admission; no prior `queued` row moved).
- Search log (not a row): `SOURCES.md:397` under `## Search log`.
- End validate after the landing commit is still unrun. Do not file 183 as the after.

§2b companions, untracked, not committed: `corpus/knowledge/mutation-testing-r28.md` (cites S183; its own `## Gate` at `:29-34`) and `corpus/lessons/round-28.md` (`## Mistakes` M27-3; `## Gate` quote at `:19`, 11 words, title field). Lesson class token is `premature-saturation`, which is not in the `CORPUS.md:174-177` class list. Sourced claim named by registration: **C1 / S183**.

## 4. Marker-fail checklist (what omission fails the round)

Prompt `:121-125` (stricter): failed if the file is placeholder text, has no evidence pointers, or lacks **Work performed**, **Landed changes**, **Before → after measurements**, or **SHONEN**. Missing **Sources & frontier** or **Trend verdicts** is `ok` plus one conformance defect.

`PROTOCOL.md` wins where that conflicts (`:91-92`, `:202-206`):

- Marker → integrator `failed`: no lane work, no evidence pointer, and no resolvable commit. Real uncommitted work does not rescue it.
- Not a marker: a short report that names a real committed round-work hash. Status `ok`, minimum-content defect.
- Observed `report_of` (`shokunin-watchdog.sh:144-163`) accepts a file only when the SHONEN heading/bold marker matches and `wc -c` ≥ `MIN_REPORT_BYTES` (default 400). It does **not** check one line per box. Protocol prose (`:192-196`) says it does; the script is the weaker check.
- No SHONEN heading: driver does not complete the round.
- SHONEN present but not one `[x]`/`[ ]`/`[~]` line per box: contract defect and promotion-disqualified; not by itself a marker if a real hash is cited.

Also required substance, or the file is the marker (`PROTOCOL.md:152-155,194-196`): work performed; ≥1 evidence pointer; each landed change tied to a `LOG.md` entry; a commit hash that exists and is an ancestor of lane `HEAD`.

## Commands

- `sources-census.sh validate … mado` — exit 0 (seven W04 + ok). Output matches `evidence/census-start.txt` except that file predates S183.
- `sources-census.sh census … mado` — exit 0; `rows 183` as above.
- Frozen grep on worktree — 183, exit 0. On `master` blob — 182, exit 0. Tier/status awk as in §3.
- `git rev-parse master` — `4f610066efd90804b055c42ae20c41a7f44404f9`. `git grep -F S183 master -- corpus/SOURCES.md` — no hit. `git status --porcelain` — `M LOG.md`, `M SKILL.md`, `M corpus/SOURCES.md`; `??` knowledge note and lesson. `PROVINCE.md` clean.

Dead end: a first status awk printed `n[s]` for every key (bogus `163` thrice). Re-ran with `n[k]`. `corpus/lessons/round-28.md` was absent on the first `ls` and present at 20:11 (27 lines); mapped as untracked, not as missing.

Wrote only this file. No commit.
