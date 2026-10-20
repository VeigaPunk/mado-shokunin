# PipeRcCensus — criterion-26 runnable check

Seat: `MadoR18.PipeRcCensus` (leaf executor). Item: C1 / R17-V5 / JjAuditMado F10 —
a static census of piped command substitutions in `tools/*.sh` that assign their
result and never capture the producer's status.

Deliverable: `.ufo/waves/round-18/pipe-rc-census.py`
(sha256 `cb150cb2f9df6ddb4d80df37256b463ec5f4822790ede91543ff977b908a4564`,
17536 bytes). Nothing else in the lane was written; `/tmp/pipe-rc-lab/**` are
throwaway fixtures, not deliverables.

## What the tool does

```
python3 -I .ufo/waves/round-18/pipe-rc-census.py [--repo DIR] REV
```

* Enumerates `tools/*.sh` at `REV` with `git ls-tree -r --name-only`, reads each
  blob with `git show REV:path`, and **checks that read's return code** — the
  census tool itself cannot turn a failed read into the empty-input digest.
  Read-only git only; no index, refs, or temp writes.
* Shell-aware scan: single quotes, double quotes, comments, heredocs (including a
  heredoc inside a substitution body), `case` patterns, nested `$(...)`, escaped
  `\$(`. Backtick substitutions are not scanned (none carry a piped
  sha256sum/wc/cut at this revision).
* A **site** is a command substitution whose value is assigned
  (`NAME=` / `NAME="` / `NAME+=` / `NAME[IDX]=`) whose body has at least two
  top-level `|` stages and at least one non-first stage whose command word is
  `sha256sum`, `wc`, or `cut` (after `!`, `VAR=value` prefixes, and
  `xargs`/`timeout N`/`tmo`/`env`/`command`/`sudo`/`nice` wrappers).
* Verdicts and reasons:
  - `checked  # pipestatus` — PIPESTATUS read in/after the substitution.
  - `checked  # pipefail-*` — `set -o pipefail` in effect textually before the
    site and the body does not end in `|| true`/`|| :`; the suffix names what
    else consumes it (`errexit`, `condition`, `short-circuit`,
    `pipeline-fallback`, `status-var`, or `scope` when nothing does).
  - `checked  # precondition-guard` — producer is a bare `sha256sum`/`wc`/`cat`/
    `head` whose operand is proven a regular/readable file by a
    `[ -f OPERAND ]`/`[ -r OPERAND ]` test in the same command or the enclosing
    if/elif chain, and that branch also proves the tool present (`have TOOL`).
  - `unchecked  # producer-status-dropped; sinks=...`.
* Exit: `0` no unchecked site (GREEN), `1` at least one unchecked site (RED),
  `2` usage / bad revision / read failure. Output is one
  `SITE <path>:<line> unchecked|checked` line per site plus `SUMMARY` and
  `VERDICT` lines; two runs at the same revision are byte-identical.

## Baseline receipt (RED)

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin
$ python3 -I .ufo/waves/round-18/pipe-rc-census.py d9a5a18
SITE tools/mado-verify.sh:640 unchecked  # producer-status-dropped; sinks=cut
SITE tools/mado-verify.sh:942 unchecked  # producer-status-dropped; sinks=sha256sum,sha256sum
SITE tools/mado-verify.sh:944 unchecked  # producer-status-dropped; sinks=sha256sum,sha256sum
SITE tools/mado-verify.sh:962 unchecked  # producer-status-dropped; sinks=cut
SITE tools/mado-verify.sh:1377 unchecked  # producer-status-dropped; sinks=sha256sum,sha256sum
SITE tools/mado-verify.sh:2780 checked  # precondition-guard
SITE tools/mado-verify.sh:2788 unchecked  # producer-status-dropped; sinks=wc
SITE tools/mado-verify.sh:3336 checked  # precondition-guard
SITE tools/mado-verify.sh:3406 unchecked  # producer-status-dropped; sinks=sha256sum,cut
SITE tools/mado-verify.sh:3407 checked  # precondition-guard
SITE tools/mado-verify.sh:3444 unchecked  # producer-status-dropped; sinks=wc
SITE tools/mado-verify.sh:3474 unchecked  # producer-status-dropped; sinks=wc
SUMMARY rev=d9a5a18 commit=d9a5a18e17cd3a68b52148fcc01c4a30e340ba98 files=1 sites=12 checked=3 unchecked=9
VERDICT RED
exit=1
```

`:3406` is flagged, as the item requires. Scanning `refs/heads/master`
(`d3a0000`) yields the identical 12 sites and counts — no drift between the
baseline and the pre-registration commit.

## Every site at d9a5a18, with hazard judgement

| line | site (abridged) | verdict | judgement |
|---|---|---|---|
| 640 | `om_leafsha=$(sha256sum "$OMR/.../SKILL.md" \| cut -c1-12)` | unchecked | **Benign / weak assertion.** Round-8 selftest fixture; the file was written by the fixture two lines above. If the producer failed, the expected detail becomes `""` and the selftest comparator uses `awk index($0,"")` = 1, so the assertion cannot bite in either direction (`st_row_detail` at :700/:770). Selftest-only, never a production row. |
| 942 | `before=$(find "$A" -type f \| sort \| xargs sha256sum \| sha256sum)` | unchecked | **Latent proof-weakening, not a false FAIL.** Scenario A read-only proof; compared for equality with :944. A failed/empty `find` makes `xargs` run `sha256sum` on `/dev/null` (prints the 64-char empty digest, rc 0), and the final `sha256sum` hashes that line to the constant `abcfa6a9d4df344d1781bc2560b5e4cdcae08b39ed303063535e7e1e926a304a`; both sides then match and the proof passes vacuously. |
| 944 | `after=$(find "$A" -type f \| sort \| xargs sha256sum \| sha256sum)` | unchecked | Same as :942 (the other side of the equality). |
| 962 | `shaf=$(sha256sum "$A/.config/hypr/hyprland.conf" \| cut -c1-12)` | unchecked | **Benign.** Feeds a scenario-A NOTE assertion whose expected string is `"sha256 ${shaf}…"`; an empty producer value makes that expectation `"sha256 …"`, which does not occur in the actual row, so the selftest fails loudly rather than passing silently. |
| 1377 | `sfix=$(find "$A" -type f \| sort \| xargs sha256sum \| sha256sum)` | unchecked | **Latent proof-weakening.** S1 read-only proof compared at :1383 against a second identical substitution; both collapse to the same constant on producer failure, so the equality passes vacuously. |
| 2780 | `sha=$(sha256sum "$f" \| cut -c1-12)` | **checked** (precondition-guard) | **Benign.** Enclosed by `if [ -f "$f" ] && have sha256sum`; producer is `sha256sum` of a proven regular file, and the value only feeds a NOTE row. |
| 2788 | `nbak=$(find "$H" -maxdepth 1 -name '*.bak*' 2>/dev/null \| wc -l)` | unchecked | **Benign/low.** `2>/dev/null`; an erroring `find` reads as `0`, understating backup litter in a NOTE row that is never a verdict input. |
| 3336 | `ss=$(sha256sum "$leaf" 2>/dev/null \| cut -d' ' -f1)` | **checked** (precondition-guard) | **Benign.** The `then`/`elif`/`else` chain proves `sha256sum` present and `$leaf` a regular file before the `else` body runs. |
| 3406 | `blob=$(tmo git -C "$tree" show "HEAD:$OMARCHY_SKILL_REL" 2>/dev/null \| sha256sum \| cut -d' ' -f1)` | unchecked | **REAL HAZARD — JjAuditMado F10.** The producer is `git show`, and the enclosing guard (`! have git \|\| [ "$omtree" = 0 ] \|\| ! have sha256sum \|\| [ ! -f "$leaf" ]`) proves only that git exists, `$tree/.git` exists, sha256sum exists, and the **worktree** `$leaf` is regular. It proves nothing about `HEAD:default/omarchy-skill/SKILL.md` in the omarchy checkout: a missing/moved path in HEAD, an unreadable object, or the 5 s `tmo` timeout (rc 124, empty stdout) all make `git show` fail while `sha256sum` succeeds on empty stdin and emits the 64-character `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. `blob` is therefore non-empty, the `[ -z "$blob" ]` UNKNOWN branch at :3408 is unreachable, and the row renders FAIL “MOVED: … (local edit; editing the skill edits the checkout)” for a checkout with no local edit. Measured consequence (standalone reproduction): `blob=$(false \| sha256sum \| cut -d' ' -f1)` → `e3b0c442…`, rc 0, 64 chars, then the shipped logic prints `FAIL: MOVED: … (local edit)`. |
| 3407 | `sw=$(sha256sum "$leaf" 2>/dev/null \| cut -d' ' -f1)` | **checked** (precondition-guard) | **Benign.** Same branch as :3406 but the producer is `sha256sum` of the proven regular `$leaf`, not a repository object read. A residual read error would still surface as a wrong-direction FAIL, but the branch removes the practical failure modes. |
| 3444 | `nwant=$(printf '%s' "$OMARCHY_SKILL_GROUPS" \| wc -w \| tr -d ' ')` | unchecked | **Benign.** `printf` is a builtin that cannot fail here and `wc -w` always emits a number; the value is interpolated into a PASS/FAIL message, not a decision. |
| 3474 | `nd=$(find "$hooks" ... \| wc -l \| tr -d ' ')` | unchecked | **Benign/low.** Guarded by `[ -d "$hooks" ]` with `2>/dev/null`; feeds a NOTE row only. |

Classification totals: 12 sites; 3 checked (2780, 3336, 3407 — all
precondition-guard); 9 unchecked, of which **one is a real hazard (:3406)**,
**three weaken a proof in the vacuous-pass direction (942, 944, 1377)**, and
five are display/test-fixture values (640, 962, 2788, 3444, 3474).

### Piped substitutions deliberately not counted (scope: assignments only)

* `:1133`, `:1383`, `:2990` — substitutions used as command arguments, not
  assigned. Their producer status is also dropped; `:1383` has the same
  vacuous-equality shape as `:1377` (both sides of an `st_eq`).
* `:2215` — `gate_sha=$(sha256sum -- "$MADO_R8_SELF" 2>/dev/null || true)`: no
  pipe, and emptiness is handled by `[ -n "$gate_sha" ] || gate_sha=unavailable`.
* `:1065` — `h=\$("$REAL_SHA" | cut -d' ' -f1)` is escaped literal text inside a
  heredoc-emitted stub (the `sha256sum` stub for scenario I); it is data, not an
  assignment in `mado-verify.sh`.

## Lab receipts (throwaway fixtures under /tmp, not lane artifacts)

1. Per-case fixture repo (one file per case, 7 files):

```
SITE tools/c1.sh:4 unchecked  # producer-status-dropped; sinks=sha256sum,cut
SITE tools/c2.sh:3 checked  # pipefail-condition
SITE tools/c3.sh:2 checked  # pipestatus
SITE tools/c4.sh:4 checked  # precondition-guard
SITE tools/c7.sh:2 unchecked  # producer-status-dropped; sinks=wc
SITE tools/c8.sh:3 unchecked  # producer-status-dropped; sinks=sha256sum,cut
SITE tools/c9.sh:3 unchecked  # producer-status-dropped; sinks=cut
SUMMARY rev=HEAD commit=fd8849559bed9dd16b8ca4471387535bd7e51c74 files=7 sites=7 checked=3 unchecked=4
VERDICT RED
```

   `c8` is `set -o pipefail` plus `... | sha256sum | cut ... || true` — the
   explicit discard keeps it unchecked. `c9` proves a `case` pattern inside the
   substitution does not close it early (sink `cut` still found). A heredoc body
   containing `h=$(fake | cut ...)` in a fifth case is correctly ignored.

2. Edge fixture: `set -euo pipefail` + plain assignment → `checked # pipefail-errexit`;
   `set +o pipefail` before the site → `unchecked`; assignment inside double
   quotes (`x="$(... | cut -c1-5)"`) → found; nested `$(awk …)` producer with a
   `| wc -l` sink → found (`sinks=wc`); heredoc-inside-substitution → no site;
   `case` inside substitution → found. Output: 5 sites, 1 checked, 4 unchecked.

3. Green path: a fixture whose every site is checked prints
   `SUMMARY ... sites=3 checked=3 unchecked=0`, `VERDICT GREEN`, exit 0 —
   the checker can pass, so a criterion asserting exit 0 at a fixed revision is
   satisfiable.

4. Usage and failure modes: no argument → exit 2; unknown revision → exit 2
   (`pipe-rc-census: not a revision in …`); non-repository `--repo` → exit 2.
   Two identical runs at `d9a5a18` were byte-identical (`cmp` clean).

## Notes for wiring criterion 26 (L1 / QualityDraft)

* Red receipt to cite verbatim: `python3 -I .ufo/waves/round-18/pipe-rc-census.py d9a5a18`
  exits 1 and prints `SITE tools/mado-verify.sh:3406 unchecked` plus
  `unchecked=9`. This is the “shown able to fail” half.
* The contract's `pipefail` clause is implemented literally: `set -o pipefail`
  in effect plus no `|| true`/`|| :` discard makes a site `checked`; the reason
  token (`pipefail-scope` vs `pipefail-condition`) exposes whether anything
  actually consumes the status. A single `set -o pipefail` near the top of
  `tools/mado-verify.sh` therefore flips all nine unchecked sites, and the
  census goes GREEN — but that alone does **not** stop the :3406 masking:
  measured, `set -o pipefail; blob=$(false | sha256sum | cut …)` still yields the
  same 64-char `e3b0c442…`, rc 1, unused. The routed fix must consume the rc at
  the site (e.g. `if ! blob=$(…); then` with an UNKNOWN row), which the tool then
  reports as `pipefail-condition`, or restructure to check `git show`'s rc before
  hashing. The census is a static gate; the dynamic failing-`git`-stub scenario
  remains the behavioural bite for F10.
* If no global `pipefail` is added, nine sites need individual capture; six of
  them are display/test-fixture values where the cheaper route is to leave the
  census red and scope the criterion to “the pipeline that feeds a verdict row
  is checked”. The tool reports per-site reasons precisely so such a scoped
  assertion can name `:3406` rather than rely on counts.

## Limitations (documented static approximations)

* `set -o pipefail` scope is textual per file: a `set` inside one function
  credits later sites in the same file. At `d9a5a18` there is no `pipefail`
  anywhere, so the baseline numbers are unaffected; a fixed revision should put
  the `set` before the sites it is meant to cover.
* Guard polarity is not modelled: a negated `[ ! -f X ]` in an `elif` is
  accepted as proof for a site in the following `else` (correct for the three
  credited sites here) and would also credit a site placed in that `then` branch.
* The operand heuristic assumes the first non-option token of the producer is
  its file operand.
* `shopt -s lastpipe` is not modelled; only `$(...)` substitutions are scanned.
* Working-tree-only edits are invisible by design (reads go through `git show`).

## Installs / environment

No packages installed or upgraded (host pacman transactions are paused; none
were needed — Python 3 stdlib and git suffice). No pacman/omarchy/system probe
was invoked. Pre-existing sibling edits (`M tools/mado-verify.sh`,
`M tools/mado-tripwire.py`, `?? tools/__pycache__/`) were not touched.
