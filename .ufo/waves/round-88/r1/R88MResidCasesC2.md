# R88MResidCasesC2 — residual r1 attack on frozen C2 bytes

Seat: R88MResidCasesC2 · 2026-11-06 · lane `/home/vgpnk/Projects/shokunin/mado-shokunin`
Bytes: base `24ba2a9ddac21c1211579231e6ee1d98963f9988` · freeze `9e36e3a3103349b939982e532feca443f02e660d` · C1 rev A `650e18bdf0ae404ec9a80874c4503ecf3237e8e6` · C2 rev B `7d3074865a9f5acfa0f1c9c66b460e73d4031331` · record tip `498855cb327cd4e3debfa9446ea38398c216dda1`.

**VERDICT: C2 VERIFIES.** All four attack items found no defect. One non-blocking observation on declaration wording; two minor citation notes.

Lane tree state during the run: `HEAD=498855cb`, 6 dirty entries (`quality/tool-ledger.md` modified; r1 dispatch files and `receipts/harm-final-r88.txt` untracked). Irrelevant to results: every counter reads bytes from git at `--rev` and self-verifies sha pins (proven by the identical outputs below).

## 1. Counter re-runs at the measured revisions — REPRODUCED, byte-identical to receipts

Counter bytes were taken from git, not the tree: `git show 7d307486…:quality/counters/c2-r88-include-containment.py` → sha256 `f8e18b7c915fe831e6eaafcd09fad0af9ac23d89514317f131fb1ed409e96767` (= freeze pin, declaration Freeze table); its r87 dependency `git show 7d307486…:quality/counters/c1-r87-mako-criteria.py` → sha256 `4d801c30b302ed5972142415012d8f461109459d9c44e85e0badef57a2ed3645` (= counter's `R87_COUNTER_SHA256`). Tool at B extracted separately: sha256 `c374d71514f1559a12593b1097cd5e6ccc8ba2c225f2fa2b2d7764ef29192237` (= receipt `tool_sha256`).

Run 1 (main measured command, lane root, `TMPDIR`/`--scratch-root` under `$HYAKU_SCRATCH/mado-r88/R88MResidCasesC2/run1b`):

```
python3 -I $S/counters/c2-r88-include-containment.py --repo . \
  --rev 7d3074865a9f5acfa0f1c9c66b460e73d4031331 \
  --base-rev 24ba2a9ddac21c1211579231e6ee1d98963f9988 \
  --cases .ufo/waves/round-88/controls/containment-cases-r88.json \
  --expect-cases-sha256 8b16c0cb0d73eb2e245b4b543db0a0396c824314cb8dbd26e5ad26214f20d039 \
  --expect-mutants-sha256 ff76cd698875cfc1eff6f36d5997e3df79e3ef694c22c4feb720885179403616 \
  --scratch-root $S/run1b
```

Exit 0. `diff receipts/c2-measured-B-r88.txt run1b.txt` → **empty** (whole receipt reproduced: 26/26 cases ok, controls `base_tool_correct=11 refuse_all_includes_correct=14`, mutants K1–K7 all killed, verdict `MADO_MAKO_CONTAINMENT: TARGET_MET … cases=26 correct=26 mutants=7 killed=7 … score=10.0000`, final line `rc=0`).

Run 2 (supplementary, same but `--base-rev 650e18bd…`): exit 0. `diff receipts/c2-supp-base-is-A-r88.txt run2b.txt` → **empty** (`TARGET_MET … base_rev=650e18bd… base_tool_sha256=07930521f8e4cfb8…` — the base tool at A is the C1 candidate build, as declared).

Context receipts re-read, consistent: `c2-before-A-r88.txt` = `MADO_MAKO_CONTAINMENT: SETUP_ERROR forgery anchor 'if not self.within_roots(real):' occurs 0 times`, rc 2 (see Observation O1); `c2-controls-prefreeze-r88.txt` = `BELOW_K cases=26 base_tool_correct=11 refuse_all_includes_correct=14` rc 0; `c1-harm-at-B-r88.txt` = C1 `TARGET_MET` at B (tool `c374d715…`, 62/62, 22/22); `harm-final-r88.txt` = selftests 460/460, 40/40, 28/28, index/ledger clean at `498855cb`.

## 2. Audit of k18–k26 against the stance and path_resolution(7) — ALL NINE EXPECTATIONS FOLLOW

Source bytes: case file read from the freeze commit (`git show 9e36e3a3…:.ufo/waves/round-88/controls/containment-cases-r88.json`, sha256 `8b16c0cb…` re-verified by the counter's `--expect-cases-sha256`); stance = C2 Stance/Defect paragraphs of `claims-declaration-r88.md` at the same commit; man page read as `zcat /usr/share/man/man7/path_resolution.7.gz | nl -ba` (man-pages 6.19, 2026-02-08; line numbers below are that numbering). Counter run 1 shows every k-case `ok ok` at B; the question here is whether each expectation follows from the stance + man page independent of the tool passing.

| case | expectation (runner semantics) | follows? | grounding |
|---|---|---|---|
| k18-dotdot-after-symlinked-dir | refuse, width 118 kept; decoy `home/secret.ini` (418) NOT read | YES | `~/linkdir/../secret.ini`: man L77–87 — a symlinked non-final component is resolved first and the walk continues in the target (`outside/sub`), so the following `..` is `outside/..`'s child resolution lands at `<root>/outside/secret.ini`, outside every root. Lexical normalization (mutant K6) would read the decoy; the case cleanly separates real from lexical resolution. Pin's man cite L77–80 exact. |
| k19-final-symlink-in-symlinked-dir | refuse, width 119 kept | YES | Prefix `~/linkdir` resolves inside home (man L77–87), but the final component `final.ini` is a symlink to `outside/esc.ini`. Man L169–178: `open`/`stat` follow the final link, so the file actually read is the resolved target; stance demands the fully resolved path be inside a root → refuse. Correct to refuse; refusing only the prefix would be the K7 mutant. |
| k20-absolute-with-dotdot | refuse, width 120 kept | YES | `@ROOT@/home/../outside/esc.ini`: man L136–145 — `..` refers to the parent directory and is honored "regardless of whether … actually present"; resolved path is `<root>/outside/esc.ini` → refuse. Note N2 on the pin's line numbers. |
| k21-proc-self-root-prefix | refuse, width 121 kept | YES (note N1) | `/proc/self/root<root>/outside/esc.ini` resolves to `<root>/outside/esc.ini` — `/proc/self/root` is a symlink to the process root (man L13–15: a leading `/` starts at "the root directory of the calling process"). The stance's "fully resolved path (realpath: every symlink … resolved)" carries the case; the named man page itself does not document procfs magic links (that is symlink(7) material) — see N1. |
| k22-symlink-chain-leaves-home | refuse, width 122 kept | YES | Two-link chain `l1→l2→outside/esc.ini`; every link resolved (man L77–87), well under the 40-link budget (man L105–107); terminal target outside → refuse. |
| k23-symlink-self-loop | refuse, width 123 kept | YES (note N1) | Self-loop → ELOOP at the 40-link limit (man L96–99, L105–107). The stance sentence enumerates "missing or non-regular targets are refused"; a loop is a third failure mode, but the refusal follows a fortiori: there is no resolved path to prove containment for, and the kernel could not open the literal path either (ELOOP). Expectation follows. |
| k24-symlinked-read-root | apply, width 624, no refusals | YES | `--read-root rootlink` where `rootlink→outside`: the frozen stance sentence says "each root itself resolved with realpath, so a symlinked root covers its target" (draft revision F10, present in the freeze). Resolved root `<root>/outside` contains resolved include `<root>/outside/inc.ini` → read. Encodes exactly the F10 revision; would NOT follow from the pre-revision stance, which the freeze supersedes. |
| k25-config-is-a-symlink | apply, width 625, no refusals | YES | Config `home/.config/mako/config → home/.config/theme/mako.ini`: stance — "The `--config` file itself is named by the caller and is not subject to the roots." Its include `~/core.ini` resolves inside `--home` → read. Host shape (symlinked mako config) is honored without weakening containment. |
| k26-secret-named-file-inside-home-is-read | apply, width 626, no refusals | YES | The stance explicitly declines to classify content inside a root ("it does not classify content inside a root (a secret-named file inside `--home` is read as declared — case k26)"). The case pins the named boundary of the stance rather than a violation. |

Set-level checks: K = 26 within the declared 12–32; each of k18–k26 carries a pin naming its w1 finding (R88MReviewC2 F2/F3/F4a–d/F10, R88MCritic C2(c)2–3), matching declaration Draft revision 5; escape cases keep the pre-include `width` so a partially-applied escape cannot masquerade as a refusal; k18's decoy (`home/secret.ini`=418) makes the expectation falsifiable against normpath-first resolution.

Notes:
- **N1 (grounding provenance, minor).** k21 and k23 rest on the stance's realpath requirement plus general kernel behavior; the man page named in the declaration grounds the symlink-walk and ELOOP mechanics but (for k21) not procfs magic links specifically. No defect — the expectations follow from the frozen stance text.
- **N2 (citation imprecision, minor).** k20's pin says "path_resolution(7) lines 141-142: dot-dot refers to the parent directory"; the parent-directory definition is L136–139 and L141–143 is the "conventional meanings" sentence (as k03's pin correctly cites). Substance unaffected.

## 3. Two escape inputs not in the case set — BOTH REFUSED

Tool at B (`git show 7d307486…:tools/mado-mako.py`, sha256 `c374d715…`), run `python3 -I $S/t.py --config … --home …` in scratch fixtures (absolute paths, no symlinks in the prefix).

**E1 — trailing-slash absolute include to an outside file** (case set has no trailing-slash input):
config `…/esc1/home/config.ini`:
```
width=701
include=<S>/esc1/outside/esc.ini/
```
`<S>/esc1/outside/esc.ini` = `width=901`. Invoked with only `--home <S>/esc1/home`. Result **rc 0, REFUSED**: `effective.width=701` (include not applied), `refusals=["…/esc1/home/config.ini:2: include target is not a regular file: …/esc1/outside/esc.ini/ (trailing /)"]`. Consistent with man L162–168 (a trailing `/` forces the preceding component to resolve as a directory — `esc.ini/` is not resolvable as a regular file) and with draft revision F8's named rule. The refusal names the offending path.

**E2 — `..` traversal out of a declared read root** (k20's dotdot is on `--home`; none of k13/k20/k24 puts a `..` on a `--read-root`):
config `…/esc2/home/config.ini`:
```
width=702
include=<S>/esc2/roots/../outside/esc.ini
```
`<S>/esc2/outside/esc.ini` = `width=902`; invoked with `--home <S>/esc2/home --read-root <S>/esc2/roots`. Result **rc 0, REFUSED**: `effective.width=702`, `refusals=["…/esc2/home/config.ini:2: include resolves outside the declared read roots: …/esc2/roots/../outside/esc.ini -> …/esc2/outside/esc.ini (declare it with --read-root to read it)"]`. The tool resolved the path (realpath through the declared root) and matched it against the root set, not the literal prefix — a lexical root-prefix checker would have accepted this input; the refusal text shows the resolved form and the remedy.

Neither escape read outside content. Both refusals are recorded per-include with the resolved path named, matching the stance's diagnostics sentence.

## 4. A→B file scope — ONLY tools/mado-mako.py CHANGED

`git diff --name-status 650e18bd…..7d307486…` → exactly `M	tools/mado-mako.py`; `--stat` → `tools/mado-mako.py | 95 +++++++++++++++++++++++++++++++++++++++++++++++++-----  (87 insertions, 8 deletions)`. No counter, case, mutant, receipt, or doc bytes changed between A and B. Corroboration already in receipts: C1 re-run at B (`c1-harm-at-b-r88.txt`) still `TARGET_MET` 62/62 with controls 14/15/33/43 — B's tool change did not move C1.

## Observations (non-blocking; frozen bytes — errata only, never predicates)

- **O1 (wording, LOW).** Declaration C2 Predicate line says "Before: the counter at the C1 content revision (no containment) → TARGET_MISSED", but the committed before-receipt `c2-before-A-r88.txt` is `SETUP_ERROR … anchor … occurs 0 times`, rc 2 — per the declaration's own draft revision 1 ("an anchor absent from the measured tool is a setup error (exit 2), never a scored miss") the counter cannot even build its refuse-all forgery from a tool without the containment test. The measured state exists and is honest; only the declaration's one-word expectation (`TARGET_MISSED` vs `SETUP_ERROR`) is loose. No scoring impact.
- **N1/N2** as in §2 (grounding provenance for k21/k23; k20 pin line numbers).

## Verification log (commands → exit codes)

| step | command (abridged) | exit |
|---|---|---|
| extract counters/tool from git at 7d307486 | `git show …` ×3 + `sha256sum` | 0; shas `4d801c30…`, `f8e18b7c…`, `c374d715…` all match pins |
| counter run 1 | see §1 | 0; `diff` vs receipt → empty |
| counter run 2 | see §1 | 0; `diff` vs receipt → empty |
| probe E1 | `python3 -I $S/t.py --config …/esc1/home/config.ini --home …/esc1/home` | 0; refused (JSON above) |
| probe E2 | `python3 -I $S/t.py --config …/esc2/home/config.ini --home …/esc2/home --read-root …/esc2/roots` | 0; refused (JSON above) |
| A→B scope | `git diff --name-status 650e18bd…..7d307486…` | 0; only `tools/mado-mako.py` |
| man page | `zcat /usr/share/man/man7/path_resolution.7.gz \| nl -ba` | 0; 266 lines |
| dead step | first counter attempt ran `$S/c2-counter.py` without its sibling r87 file → `FileNotFoundError: …/c1-r87-mako-criteria.py`, rc 1 | resolved by extracting the counter pair into one directory |

Installs: none. Mutating git/jj commands: none (fixture writes only under `$HYAKU_SCRATCH/mado-r88/R88MResidCasesC2/`, deleted after this report was written). Credential material: not read (host reads limited to the declaration-named man page and the lane's git bytes).
