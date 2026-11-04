# R67ScoutState — instrument-state recon (C2 surface + C1 assess + used-by fixture)

Read-only recon. Lane tip while working: `ac376ef3` (freeze `061dc329`); measured base
`0b28ffb4baac9586566d246c3f0986b2bb650a33`. No lane file was edited; every write went to
`/fast/scratch/hyaku/mado-r67/R67ScoutState/`, removed at yield with `rm -rf` (the per-command
`trap … EXIT` did not fire in this harness's temporary shells; absence verified afterwards).
No pacman transaction, no tool install, no host/compositor probe.

## Commands run (exact, from the lane root)

| command | rc | output |
|---|---|---|
| `python3 -I quality/counters/c3-r56-used-by.py --selftest --repo . --rev HEAD --work $S/ub-selftest` | 0 | `MADO_USED_BY_SELFTEST: 16/16 assertions passed` |
| `python3 -I quality/counters/c3-r56-used-by.py --repo . --rev 0b28ffb4… --work $S/ub-real` | 0 | `MADO_USED_BY: … entries=78 rows=372 … exempt=24 verdict=TARGET_MET missed=none` |
| `bash quality/landing-counters.sh --selftest --scratch-root $S/lc` | 0 | `MADO_LANDING_COUNTERS_SELFTEST: 58/58 assertions passed` |
| `python3 -I quality/counters/c1-r66-register.py --repo . --rev HEAD` | 0 | `MADO_R66_REGISTER: headings=1 rows=8 groups=8/8 receipts=4 resolved=4 gate=ok verdict=TARGET_MET` |
| `python3 -I quality/check-tool-ledger.py --repo . --rev HEAD` | 0 | `LEDGER: population=108 ledger_rows=108 uncovered=0 … verdict=TARGET_MET` |
| probe1 (r66 forgery shapes + used-by legs) | 0 | 8 C1 cases + 3 UB lines, quoted in §2–§3 |
| probe2 (R control end-to-end on the base child) | 0 | 5 UB lines, quoted in §1.5 |
| probe3 (4 extra r66 shapes) | 0 | 4 C1 lines, quoted in §3 |

Probe code is embedded in §2.3 (copyable) and §3 (one-liners); the scratch copies were removed.

---

## 1. C2 control surface map

### 1.1 `quality/landing-counters.sh`

Env hardening (already at base, unchanged by r67):

- `:6` `for git_var in "${!GIT_@}"; do unset "$git_var"; done`
- `:8` `export GIT_OPTIONAL_LOCKS=0 GIT_NO_REPLACE_OBJECTS=1`
- `:14-16` sibling paths: `counters/c3-r56-used-by.py`, `check-tool-ledger.py`, `../tools/mado-receipt-citecheck.py`
- `:41-43` leg dispatch: used-by gets `--work "$SCRATCH_ABS/ub"`; ledger and citecheck do **not** get a work dir.

`marker_valid` `:46-76` (one child-owned marker, exact revision, verdict consistent with rc):

- `:48` `[ "$rc" -le 1 ] || return 1` — rc 2 is never a valid marker (any crash → ERROR).
- `:49-53` prefix per leg, exactly one matching line required.
- `:64-69` `rev=$REV` must be a whole whitespace-delimited field; `verdict=$met` required and duplicate
  `verdict=` refused.
- `:70-75` citecheck branch — **the zero-citation guard**:
  - `:71` regex `\ citations=([0-9]+)\ resolved=([0-9]+)\ missing=([0-9]+)\ `
  - `:73` `[ "$citations" -gt 0 ] && [ "$citations" -eq "$((resolved+missing))" ] || return 1`
  - `:74` `if [ "$rc" -eq 0 ]; then [ "$missing" -eq 0 ]; else [ "$missing" -gt 0 ]; fi`

Run loop and the marker-invalid branch:

- `:239` `verdict=GREEN exitcode=0`
- `:240-245` legs run in order `nav usedby ledger citecheck`; `rc` captured, `LANDING_LEG <leg> rc=N` printed.
- `:246-251` `if ! marker_valid …; then … verdict=ERROR exitcode=2; elif [ "$rc" -eq 1 ] && [ "$exitcode" -eq 0 ]; then verdict=RED exitcode=1; fi`
  → ERROR outranks RED; a contract violation is exit 2, never a silent pass.
- `:253-254` `MADO_LANDING_COUNTERS: <GREEN|RED|ERROR> (nav=… usedby=… ledger=… citecheck=…)` and `exit`.

Consequence for M-Z: deleting `[ "$citations" -gt 0 ] && ` at `:73` makes a `citations=0 … verdict=TARGET_MET`
marker at rc 0 pass `:73` and `:74` (0 == 0 + 0) → GREEN/exit 0 instead of ERROR/exit 2.

`--selftest` shim and WITNESS:

- `:97-129` heredoc shim installed as `$SW/shim/python3`; `:99-105` maps argv[1] to
  `nav|-|*/c3-r56-used-by.py|*/check-tool-ledger.py|*/mado-receipt-citecheck.py`; `:106-109` missing child → 2.
- `:110` `printf '%s\n' "$leg" >>"$WITNESS"` — appended **before** the mode dispatch, so every leg
  is witnessed even when the shim exits early.
- `:111-113` `TEST_MODE=skip` → exit 0 (no marker); `crash` → exit 2.
- `:114-115` `red` → rc 1 + `verdict=TARGET_MISSED`.
- `:116-125` per-leg marker text; **`:122`** is the citecheck arm and hardcodes positivity:
  `printf 'MADO_CITECHECK: rev=%s files=1 citations=1 resolved=%s missing=%s skipped_large=0 verdict=%s\n' "$FIXTURE_REV" "$((1-rc))" "$rc" "$verdict"`.
- `:127` `duplicate` prints the marker twice.
- `:132` `export WITNESS=… FIXTURE_REV=… REAL_PYTHON=… TEST_LEG=none TEST_MODE=green`
- `:133-146` matrix legs `none nav usedby ledger citecheck` × modes `green red crash skip duplicate`
  (`none` only green = 21 runs); `:138` truncates the witness; `:140-141` expected rc map
  `red→1`, `crash|skip|duplicate→2`; `:143-144` asserts the witness equals
  `$'nav\nusedby\nledger\ncitecheck'` (all four legs executed exactly once).
- `:147-191` missing-sibling ERROR, `--round` required, dirty-path guards, inherited-Git isolation,
  `/tmp`/`/var/tmp`/`/dev/shm` refusal, symlinked scratch parent, empty-population RED.
- `:190` `MADO_LANDING_COUNTERS_SELFTEST: %d/%d`; `:191` nonzero if any assertion failed.

Constraint for the Z case (derived from `:73-74`): the zero-citation fixture **must** print
`citations=0 resolved=0 missing=0 verdict=TARGET_MET` at rc 0. If it printed `missing>0`,
`:74` would reject it too, so deleting the positivity clause at `:73` would leave the case red and
the mutant would **survive**. The sibling draft `R67ExecLanding.md` uses exactly `0/0/0` (its
62/62 run and M-Z probe rc 1 are that seat's evidence, not re-run here).

Scratch checks `:210-220`:

- `:210` `--scratch-root` required in both modes.
- `:212` relative → `$PWD/…`; `:213-217` walks each lexical prefix and refuses any symlink component;
  `:218` `realpath -m`; `:219` refuses `/`, `/tmp`, `/var/tmp`, `/dev/shm` and their children;
  `:220` `mkdir -p` only after the checks.
- No `mktemp`/`TMPDIR` fallback anywhere: scratch is caller-declared only.
- TOCTOU window between `:215`/`:219` and `:220` exists but is not exercised by any control.

### 1.2 `quality/counters/c3-r56-used-by.py` — git access

`git_env(work)` `:59-71` returns a **fresh dict** (nothing inherited):

```
:61 PATH (inherited value, default /usr/bin:/bin)
:62 HOME=work   :63 TMPDIR=work   :64 LC_ALL=C
:65 GIT_CONFIG_NOSYSTEM=1   :66 GIT_CONFIG_GLOBAL=/dev/null
:67 GIT_LITERAL_PATHSPECS=1 :68 GIT_OPTIONAL_LOCKS=0 :69 GIT_TERMINAL_PROMPT=0
```

**No `GIT_NO_REPLACE_OBJECTS`**, no `GIT_CONFIG_SYSTEM`, no `GIT_DIR`. Because the dict is fresh,
the instrument's `:8` export (`GIT_NO_REPLACE_OBJECTS=1`) is **dropped** for this child.

Every git call it makes (all `git -C <repo>` via `:93-96`, `env=self.env`, `timeout=300`):

| line | call | purpose |
|---|---|---|
| `:81` | `rev-parse --verify --quiet --end-of-options <rev>^{commit}` | resolve rev, then `:85` fullmatch hex |
| `:87` | `rev-parse --show-toplevel` | `:88-89` refuse a non-root repo |
| `:100` | `ls-tree -z <sha> -- <path>` | modes/types/oids |
| `:121` | `cat-file blob <oid>` | **the byte read replace-refs rewrite** |
| `:241` | `Repo(repo, t["base_rev"], work)` (same three calls) | base pairs, fail-closed |
| `:308`, `:327` | `git -C <fixture> … init/add/commit/rev-parse HEAD` | `--selftest` only |

Read surface: regular blobs only `:45`; `corpus/knowledge` direct children `:127-145`;
fences `:149-163`; `cite()` `:166-171`; `src()` first 15 lines `:173-179`; registry `:181-201`;
pairs `:208-237`; base hash `:239-251`; frozen tables `:254-267`; legs `:270-303`.

CLI `:444-449`: `--repo`, `--rev`, `--work` (**required**), `--selftest`, `--detail`.
`:458` `os.makedirs(a.work, exist_ok=True)` with no `/tmp` refusal and no realpath — a direct caller
can put `HOME`/`TMPDIR` under `/tmp`. There is **no `--tables`/override flag** (see §2.2).

### 1.3 `quality/check-tool-ledger.py` — git access

`git_env(home=None)` `:101-110`:

```
:102 PATH, SYSTEMROOT (from os.environ)   :104 HOME = home or $HOME or /nonexistent
:105-107 GIT_CONFIG_NOSYSTEM=1, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull
:108 GIT_OPTIONAL_LOCKS=0   :109 LC_ALL=C
```

**No `GIT_NO_REPLACE_OBJECTS`, no `TMPDIR`** (so any git child temp file falls back to `/tmp`).

`run_git` `:113-115` (`env=git_env()`), and the call sites: `:126` `rev-parse --git-dir`
(`check_repo`), `:135-136` `rev-parse --verify --end-of-options <rev>^{commit}` (`resolve_rev`),
`:145` `ls-tree -r -z <sha>` (`tree`, oids only), `:162` `show <sha>:<path>` (`blob`, bytes).
`invoke` `:539-543` runs the gate as a subprocess with `git_env(home)`.
Scratch: `resolve_work` `:424-460` takes `--work`, else `--scratch-root`, else `$TMPDIR` (`:429`);
refuses `/tmp`, `/var/tmp`, `/dev/shm` case-folded (`:433-449`); `tempfile.mkdtemp(dir=real)` `:460`.

### 1.4 `tools/mado-receipt-citecheck.py` — subprocess env

- `run_check` `:98-103`: `subprocess.run(["git","-C",repo,"ls-tree","-r","--name-only",rev], capture_output=True, text=True, check=True)`
  — **no `env=`**, so it inherits the whole environment. Launched from `landing-counters.sh`
  (`:8` export) it inherits `GIT_NO_REPLACE_OBJECTS=1`; launched directly it does not. This is the
  third r67 edit (dispatch: give it an explicit env with the key).
- Scratch refusal `:217-228`: `:220` requires `--scratch-root` for `--selftest`; `:224`
  `if sr.rstrip("/\\") in ("/tmp", "C:/tmp") or sr.startswith(os.path.abspath("/tmp")):`
  → refuses `/tmp` (and over-refuses `/tmpfoo`), but **accepts `/var/tmp` and `/dev/shm`**, and
  `abspath` does not resolve symlinks (a symlink to `/tmp` passes).

### 1.5 R-control mechanics (observed end-to-end on the base child)

Probe2 built the counter's own minimal fixture (2 entries, 4 rows), committed a defective
registry (S001 used-by names `corpus/knowledge/missing-r56.md`), then planted
`refs/replace/<ghost-SOURCES-blob> → <clean-SOURCES-blob>` and ran the **base** child
(`git show 0b28ffb4:quality/counters/c3-r56-used-by.py`):

```
R real-view   on-ghost-no-replace rc=1 … extra=1 … verdict=TARGET_MISSED missed=extra
R real-view   on-clean            rc=0 … verdict=TARGET_MET missed=none
R base-child  on-ghost-with-replace rc=0 … extra=0 … verdict=TARGET_MET missed=none
R guarded     on-ghost-with-replace rc=1 … extra=1 … verdict=TARGET_MISSED missed=extra
R guarded     on-clean              rc=0 … verdict=TARGET_MET missed=none
```

`guarded` = the same module with one key added to `git_env()` (`e["GIT_NO_REPLACE_OBJECTS"]="1"`).
So M-R's exact recipe is sound: the **base** child reads forged TARGET_MET; the key restores the
real TARGET_MISSED, and the clean green path is unchanged.

M-R target ambiguity (flag for L1/reviewers, not a re-scope): three files gain the key this round
(dispatch seat R67ExecChildren, `w1-dispatch.json:130`, items 1–3), and the frozen declaration says
"the child" (singular). The baseline receipt records `usedby_guard=0 ledger_guard=0`
(`control-baseline-r67.txt`), so the harness must name the one file whose mutant it builds. The
harness seat text (`w1-dispatch.json:135`) already says "copy the used-by child" — that choice is
consistent with the proof above; the ledger/citecheck keys then remain installed but are **not**
what M-R kills.

Cross-check against the seat drafts (they appeared during this recon; read-only):
`R67ExecChildren/draft/quality/counters/c3-r56-used-by.py:70`, `…/check-tool-ledger.py:109`,
`…/tools/mado-receipt-citecheck.py:103` carry the key; `R67ExecHarness/draft/quality/counters/c2-r67-landing-controls.py`
pins `USEDBY = "quality/counters/c3-r56-used-by.py"` (`:55`), asserts the key occurs exactly once
before deleting it (`:232-235`), and pre-checks that the guard hides the forged path (`:365`).
That is the mechanism proven in the probe above.

---

## 2. Minimal used-by TARGET_MET fixture

### 2.1 Required inputs (all from git objects at `--rev`; worktree never opened)

| input | rule | line |
|---|---|---|
| repo root | `rev-parse --show-toplevel` realpath == `--repo` | `:87-89` |
| rev | resolves to one commit, hex 40–64 | `:81-86` |
| `.ufo/waves/round-56/frozen-tables-v2.json` | regular blob, sha256 `9511151a…95e2`; `c3` keys required | `:41`, `:254-267` |
| `c3.allowlist_path` (`.ufo/waves/round-56/c3-name-only.tsv`) | regular blob, sha256 `70653e09…48ee`, **exactly 24 rows** | `:275-292` |
| `c3.base_rev` (`13f0acbe…`) | must resolve **in the same repo**; base missing-pair set hashes to `630007b0…` or setup error | `:239-251` |
| `corpus/SOURCES.md` | regular blob; each row line `| S\d{3,} | …` must have **exactly 11 cells**; used-by is **cell index 10** | `:49`, `:181-201` |
| `corpus/knowledge/*.md` | direct children, regular blobs (100644/100755), `.md`, basename length > 3 | `:43-45`, `:127-145` |
| citations | `S\d{3}` (exactly 3 digits) outside fences, whole-doc for entries; first 15 lines + line-start `source:` for source ids | `:46-51`, `:166-179` |
| pairs | `(S in row ids, entry cites S)`; used-by↔citation must be reciprocal unless allowlisted | `:208-237`, `:279-280` |
| allowlist rows | 4 tab cells `(S, path, linesha, note)`; linesha = sha256 of the citing lines joined by LF; an allowlisted pair may not appear in used-by; line drift → `stale` | `:225-237`, `:282-283` |
| fences | `^ {0,3}(```|~~~)`; a fence suppresses citations, **not** registry rows | `:48`, `:149-163` |

Not read by this counter: `corpus/README.md` / any index. The index row (`| \`knowledge/<name>.md\``
exactly once) is the **nav leg's** requirement (`landing-counters.sh:19-40`), not used-by's.

### 2.2 Two fixture recipes — the CLI has no tables override

`check()` always calls `load_tables` (`:272`) and `base_pairs` (`:284`); `main` exposes no
`--tables`/`--base` flag (`:444-449`). Therefore:

- **In-process recipe (minimal, what the counter's own selftest does, observed green):** build the
  two-commit fixture below and call `check(D, sha, work, override=t)`. `override` supplies
  `{allowlist_path, allowlist_sha256, exempt, base_rev, base_pairs_sha256}` and marks tables good
  (`:254-256`).
- **CLI recipe (the only way to get TARGET_MET through `main`):** the fixture repo must contain the
  real r56 base commit `13f0acbe…` **and** the byte-exact frozen tables + 24-row allowlist. The
  practical shape is `git clone` of the lane into scratch (contains `13f0acbe`) plus one fixture
  commit that adds a knowledge entry, a registry row, and the defect; the replace ref goes on top.
  A from-scratch repo cannot be TARGET_MET via the CLI (base objects absent → `:243` setup error 2).

### 2.3 Copyable minimal fixture (the selftest shape, `:348-376`)

```python
HEADER = b"| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n"
# each row: 11 cells; used-by is cell 11; paths match corpus/knowledge/[A-Za-z0-9_.-]+\.md
W = "corpus/knowledge/witness-r56.md"   # cites S001, S002, S004 outside fences; source: S001, S002
X = "corpus/knowledge/second-r56.md"    # source: S003; cites S003
base commit:  registry all used-by "-" + W + X
good commit:  registry {S001:W, S002:W, S003:X, S004:W} + allow.tsv row "S004\t<X>\t<linesha>\tnamed only to be refuted"
t = {allowlist_path:"allow.tsv", allowlist_sha256:<sha>, exempt:1,
     base_rev:<base commit>, base_pairs_sha256:<hash of base missing pairs>}
```

Observed (`probe1`): `entries=2 rows=4 missing=0 extra=0 … exempt=1 verdict=TARGET_MET`, rc 0.

### 2.4 Which defect hits which leg

| defect in the fixture | leg | evidence |
|---|---|---|
| **used-by cell names a missing knowledge file** | **`extra`** (`p not in entries`, `:280`) | observed: `extra=1 … TARGET_MISSED missed=extra`, rc 1 |
| used-by cell names an existing entry that does not cite S | `extra` (`(s,p) not in pairlines`) | observed: `missing=1 extra=1 … missed=missing,extra` |
| entry cites S but the row's used-by omits it (and no allowlist row) | `missing` | `:279`; `ctl3` at `:406` |
| `source:` names an S id that is not a row id | `dangling` | `:281`; `ctl4` `:409` |
| allowlisted pair also listed in used-by | `conflict` | `:282`; `:415` |
| allowlist linesha drift / pair gone | `stale` | `:283`; `ctl9` `:412` |
| allowlist blob sha differs / row count ≠ 24 (override: ≠ exempt) | `allow_sha` / `exempt` | `:289-292` |
| frozen tables blob absent or sha differs | `tables_sha` | `:293` |
| base commit absent, pair hash differs, `SOURCES.md` absent, bad cell count | setup error, exit 2 | `:242-250`, `:212`, `:198` |

Note: `ROW_ID` accepts `S\d{3,}` (`:49`) but `S_TOKEN` only matches exactly three digits (`:50`), so
a 4-digit row id can never be cited and any used-by it carries becomes `extra`. Duplicate row ids are
not detected by any leg (`rows` counts duplicates, `ids` de-duplicates).

### 2.5 Lane state at base

`entries=78 rows=372 missing=0 extra=0 dangling=0 conflict=0 stale=0 lost=0 exempt=24 verdict=TARGET_MET`
(rc 0). `corpus/SOURCES.md` header is at `:11-12`, first row `:13`, 372 row lines.

---

## 3. C1 `assess` semantics and the forgery shapes still accepted at `0b28ffb4`

Source: `quality/counters/c1-r66-register.py` (committed at base; identical at HEAD).

| element | rule | line |
|---|---|---|
| heading | exactly one line with `startswith("### Surface state register (2026-11-03")` | `:24`, `:79-82` |
| block | from that line to the first `## ` line or a line whose `strip()` == `<!-- r65 register end -->` | `:25`, `:84-91` |
| table rows | lines `startswith("|")`; `cells()` = `strip()` then `strip("|")` then split — no column-count check | `:67-68`, `:88-91` |
| row filter | drop separator rows, and drop any row immediately followed by a separator row | `:71-72`, `:89-91` |
| row count / groups | exactly 8 rows; each of the 8 `GROUPS` exactly once in cell 0 | `:28-32`, `:92-97` |
| block receipts | every token in the **whole block text** matching `RECEIPT_RE` must resolve | `:33`, `:58-65`, `:105-108` |
| receipt grammar | whitespace split; lstrip `` `'"([<*_| `` / rstrip `` `'")]>*,;:.| ``; fullmatch `.ufo/waves/round-65/receipts/<no space , | , ) > +>.(txt|json|md|sh)` | `:33`, `:58-65` |
| **row[3] rule** | cell index 3 (4th cell, position only, header names never read); at least **one** resolvable receipt required; extra cells ignored | `:109-112` |
| live gate | `LIVE_PATH` resolves and `LIVE_LINE in live.splitlines()` (line presence) | `:26-27`, `:113-116` |
| state truth | never checked | `:145` (`state-truth-not-measured` expects accept) |

Accepted at `0b28ffb4` — **observed** (probe1/probe3, all `accepted=True`):

1. **unreferenced live object** — live receipt committed and gate-ok, every row cites only
   `gate-fileplane-r65.txt` (baseline case 5, and `selftest:146` asserts accept).
2. **live path in a state cell only** — block scan resolves it, rows cite file-plane (baseline case 6).
3. **row hidden by a following separator** — `| waybar | … | … | \`<live>\` |` + `|---|---|---|---|`
   inside the block: dropped by `:94-97`, row count still 8.
4. **heading free suffix** — `### Surface state register (2026-11-03-FORGED, elsewhere)` matches `:79`.
5. **register inside a code fence** — ` ``` ` before the heading: still one heading, 8 rows, accepted.
6. **extra columns** — a 5-cell row passes; header names are never read.
7. **live line appended to a forged body** — `"FORGED live gate body\n" + LIVE_LINE + "\n"` at
   `LIVE_PATH` passes (`:114` is membership, not file identity).
8. **unrelated committed receipt** — any committed `.txt/.json/.md/.sh` under `round-65/receipts/`
   satisfies row[3]; no content/group binding.
9. **valid receipt + dangling non-matching pointer in the same cell** — `gate-fileplane-r65.txt` plus
   `` `…gate-fileplane-r65.txt:12` `` passes; tokens that fail `RECEIPT_RE` are never validated
   (also why `.ufo/waves/round-64/…` pointers in state cells pass).
10. **arbitrary state/prose cells** — by design (`:145`).

Rejected (observed): receipt only in the 5th cell; colon-suffixed receipt as the row's only pointer.

Real register shape (matters for the r67 accept path): block at `PROVINCE.md:258-274`, header `:264`,
rows `:265-272`, sentinel `:274`. Only **3 of 8** rows carry the live path in cell 3
(`hypr plane`, `waybar`, `idle/lock plane`); `terminal configs`, `theme/wallpaper`, `omarchy skill docs`,
`windows desktop plane` cite file-plane/probe receipts only. The r67 rule must therefore be
**block-level** ("live ∈ ∪ receipts_in(row[3])"), or the genuine register is rejected.

The r66 selftest encodes the two weak expectations the r67 control set reverses:
`:145` `state-truth-not-measured → accept`, `:146` `unreferenced-live-receipt → accept`.

---

## 4. `/tmp` / `TMPDIR` (round-67 scratch-policy defect class; observed by read, not executed)

| file:line | issue |
|---|---|
| `quality/check-counter-discrimination.py:132` | default mutant root `Path(f"/tmp/mado-r36-mutants-{args.profile}")`; `ensure_mutants` (`:137-153`) writes a generated mutant tree there. Real `/tmp` writer, ignores `TMPDIR`. |
| `quality/check-r38-discrimination.py:18`, `:155` | default sandbox root `/dev/shm`; `tempfile.mkdtemp(dir=a.sandbox_root or None)`. |
| `quality/counter-selftest.py:482-484` | `a.scratch or tempfile.gettempdir()` → `/tmp` when `TMPDIR` is unset. |
| `tools/mado-receipt-citecheck.py:224` | refuses only `/tmp` (+ literal `C:/tmp`); `/var/tmp`, `/dev/shm` accepted; no `realpath` (symlink to `/tmp` passes); `startswith("/tmp")` over-refuses `/tmpfoo`. |
| `quality/counters/c3-r56-used-by.py:447`, `:458` | `--work` required but never refused for `/tmp`; `abspath` not `realpath`. |
| `quality/check-tool-ledger.py:101-110` | env constructor **omits `TMPDIR`** (and `GIT_NO_REPLACE_OBJECTS`), so git children fall back to `/tmp` for temp files. |
| `.ufo/waves/round-67/controls/score-baseline-c2.py:49-54` | `abspath` + `startswith` refusal (no `realpath`/case-fold) and `shutil.rmtree(scratch, ignore_errors=True)` **before** setup — a caller-named existing dir is deleted. |
| `.ufo/waves/round-67/controls/score-baseline-c1.py:32-36` | same prefix refusal shape, no `realpath`; only `makedirs`. |

Clean: `quality/landing-counters.sh:210-220` (caller-declared only, symlink walk, `/tmp` family refused);
`quality/check-tool-ledger.py:424-460` (honours `TMPDIR`, refuses family + home);
`quality/counters/c3-r56-used-by.py:59-71` (sets `HOME`/`TMPDIR` to `--work`);
`tools/mado-receipt-citecheck.py:225` refuses `/tmp` (partially).
`tempfile.mkdtemp()` without `dir=` (`check-index.py:177`, `check-index-rows.py:318`,
`check-axis-scores.py:114`, `check-locators.py:277`, `check-round-outcome-first.py:209`,
`check-session-material.py:2078`) honours `TMPDIR`, so it is a fallback, not an override.

---

## 5. Round-level landing hazards (observed)

1. **Ledger population grows.** `quality/*.py` and `quality/counters/*.py` are the population
   (`check-tool-ledger.py:81-82`; `population=108` at HEAD). Adding `c1-r67-register.py` and
   `c2-r67-landing-controls.py` makes 110; each needs exactly one `quality/tool-ledger.md` row whose
   description is non-empty and whose pointer names a file containing the instrument's basename,
   or the landing ledger leg goes TARGET_MISSED.
2. **Used-by reciprocity for the new knowledge entry.** A new `corpus/knowledge/*.md` enters
   `entries`; the new `SOURCES.md` row must be 11 cells with the entry in cell 11, and the entry must
   cite that `S` id outside fences. `exempt` is pinned at 24 and the allowlist sha is pinned, so no
   allowlist row may be added; an uncited new entry also breaks the nav leg's index
   (`landing-counters.sh:19-40` needs exactly one `| \`knowledge/<name>.md\`` row in `corpus/README.md`).
3. **C1 accept path is narrow.** The r67 counter must accept `PROVINCE.md:258-274` as committed
   (3/8 rows carry live in cell 3) and must reject cases 1–2 of §3; the r66 selftest's accept
   expectations for those shapes cannot be carried over.
4. **C2 Z fixture must be `0/0/0` at rc 0** (§1.1); the M-Z mutant then makes the selftest red.
5. **No `--tables` override on the used-by CLI** (§2.2): the R fixture must contain the real r56
   base commit or call `check(..., override=)` in-process.

## 6. Unverified / unknowns

- `check-tool-ledger.py`'s `show <sha>:<path>` replace sensitivity is **inferred** from the baseline
  receipt (`child_env_read=forged guarded_read=real`, `control-baseline-r67.txt`) and the shared git
  layer; I did not plant a `refs/replace` against the ledger child.
- The r67 counters are **not** at the production paths (`quality/counters/c1-r67-register.py`,
  `quality/counters/c2-r67-landing-controls.py` absent). Seat drafts for the C2 harness and the three
  child edits appeared during the recon and were read only for the env/guard lines cross-checked in
  §1.5; no draft for `c1-r67-register.py` was observed.
- `tools/mado-verify.sh --selftest` (the 460/460 operability rubric) was not run: outside this seat.
- The citecheck `/var/tmp` acceptance was read from source only — executing it would have written
  under `/var/tmp`, which this seat forbids.
- Scratch `/fast/scratch/hyaku/mado-r67/R67ScoutState/` removed with `rm -rf` and verified absent
  (per-command `trap … EXIT` did not fire in this harness); no other path written.
