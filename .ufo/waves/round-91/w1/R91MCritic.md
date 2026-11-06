# R91MCritic — attack on `claims-declaration-r91.md`

Seat: R91MCritic (critic). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Declaration attacked: `.ufo/waves/round-91/claims-declaration-r91.md`, sha256
`c8577ea34528dbf308c3b07c96bf131122f4ff19c1ba8e32853ae8d73ad149d2` (read at 21:10, re-hashed at 21:31; mtime
21:07, unchanged since). Base rev `cc0381db585cc44c3dfc13ced807409c32c45bb0`.
Every run below is **DRAFT** (`--draft-tool` / `--draft-check`, oracle `--check`, candidate `--selftest`): a draft run is
not a measurement, and nothing was written under `.ufo/waves/round-91/receipts/`.
Scratch `S=/fast/scratch/hyaku/mado-r91/R91MCritic` was removed on exit; artifacts cited here that lived there were
copied-by-content into this report (commands, shas, outputs), not left on disk.

This seat found **six freeze-blocking defects** (F1–F6) and three wording/record defects (F7–F9). The two cheap
forgeries that the declaration's predicates do not yet exclude are F1 (C1) and F3 (C2); both are demonstrated, not
argued.

---

## 0. Summary of the attack

| # | Claim/axis | Counterexample (DRAFT) | Result | Smallest safe correction |
|---|---|---|---|---|
| F1 | C1 coverage | a pure fixture-fingerprint label table (no MIME work) against the C1 counter **as read at 21:07** (sha `f2b23f…`): `correct=89/89` | `DRAFT_TARGET_MET` — the predicate as then frozen is satisfiable by memory; the fresh leg was in the declaration's prose but **not in the counter** | state PRED verbatim in the declaration (round-90 pattern), keep the fresh leg in the counter (it is there since 21:19), pin the fuzz generator, reject `--fresh 0` |
| F2 | C1 sandbox | the declared "only the fixture and the tool file are visible" is **false**: host `/usr/share/mime`, `/usr/share/applications`, `/etc/xdg`, `~/.config/mimeapps.list` (1758 B) and the whole `--scratch-root` are readable; only gio/libgio are masked | the gio/libgio masks do work (`exec` EACCES, `dlopen` EACCES, `Gio` typelib load fails); the visibility claim does not | mask the host XDG/MIME roots and bind only the per-run work dir (or the case root + a read-only tool dir); reject label-bearing inputs under `--scratch-root` |
| F3 | C2 operability | a frozen-expectation lookup table (never opens a dispatch or a report) against the **current** C2 counter (`92f8c8…`) and the live planned set (`55e981…`, 45 expectations) | `DRAFT_TARGET_MET expectations=45 met=45` (with `mutants=[]`; the rc-only selftest leg and the `m-*.py` name branch defeat a real M) — the frozen set is the contract and is memorisable; no held-out leg exists in PRED-C2-r91-v1 | add a set-echo control (it would meet 45/45 and force the issue) **and** a held-out population/fresh fixture leg derived at measurement (round-90's 38-commit population is the precedent); randomise fixture dir names; verify the selftest tally/ids, not just rc; pin the measured check's sha |
| F4 | C2 semantics | the declaration's predicate says "exact SR01/SR02/SR03 lines" (declaration `:71-76`), while the independent labels and the current candidate make **SR04 a finding (rc 1)** and **SR03 a symlink**; at candidate `2e0f08…` the independent set scored **37/41** (G-fx06, G-fx13, G-fx15, G-fx14) | the declaration is stale against its own candidate and its own labelled set | update the C2 text: SR04 = defect (rc 1), SR03 = absolute/\../symlink, summary gains `untrailed=`; update F06/F18 (the live builder now has rc1/SR04 and SR03) and re-freeze the set |
| F5 | records | with the four new instruments added to a fixture tree at base and no ledger rows, `quality/check-tool-ledger.py --repo $D --rev HEAD` → `uncovered=4` (`tools/mado-mime.py`, `quality/check-seat-reports.py`, both r91 counters), `LEDGER: population=173 ledger_rows=169 … verdict=TARGET_MISSED` rc 1; `check-index.py --rev cc0381db` → `indexed=111/111` so the C1 knowledge note needs an index row; no `SKILL.md` gate-registry row for either instrument | the C1 and C2 revisions would fail the lane's own ledger gate, and the C2 gate has no registry home row | add the four ledger rows + two `SKILL.md` registry rows (C1 probe + C2 gate), split by commit (C1 rows in the C1 commit, C2 rows in the C2 commit: a C2 row in the C1 commit is `dangling`); add the `corpus/README.md` index row and the S-rows/fetch receipts |
| F6 | contract | the declaration names no candidate sha, case-set sha, mutant sha, oracle sha, fuzz-gen sha, counter sha, N/E/M/F, or measurement argv; round 90's declaration had all of them and a "Measurement argv" block | the frozen predicate is not reproducible from the declaration alone; the case file is still moving (89 cases at 21:14, "83 at draft time" in the text) | copy the round-90 shape into the declaration at the freeze: candidate sha, `mime-cases-r91.json` sha, mutants sha, oracle/fuzz-gen/counter sha, N/M/F/E, `--fresh 120`, measurement argv |
| F7 | axes | C1 is "coverage" but PROVINCE owns no default-application surface (`grep -n -i 'mime\|xdg-open\|mimeapps' PROVINCE.md SKILL.md corpus/README.md` → no line at base); C2 is operability (a runnable gate) and is not quality work | C1 is a capability acquisition on an *undeclared* plane; without a PROVINCE refinement the coverage score cannot move | add a PROVINCE refinement (the default-application plane as read-only observed state: `$XDG_CONFIG_HOME/mimeapps.list`, `<desktop>-mimeapps.list`, `$XDG_DATA_{HOME,DIRS}/applications`, `/usr/share/mime`) and state the coverage rubric (`check-index` 111/111 → 112/112, fraction 1.0, harm watch); C2 needs the operability rubric (suite fraction unchanged) |
| F8 | wording | the declaration says the C1 controls are "draft on the 83 L1 cases: do-nothing 6, naive 6, cache-only 21" (`:52-53`); the 89-case file measured **7/6/24/0** (`base absent 0`) at 21:15 | stale draft numbers | state them as draft numbers with the file sha, and let the freeze re-run them |
| F9 | provenance | the C1 knowledge entry's sources are not in `corpus/SOURCES.md` (no GLib MIME / shared-mime-info rows; only S502 gkeyfile exists) and there are no `round-91/fetch/` receipts; the declaration gives only the gdesktopappinfo sha256 | the note's citations would be unregistered/undated | open S-rows for gdesktopappinfo.c, gcontenttype-fdo.c, xdgmime*.c, gio-tool-mime.c, gfileutils (or reuse S502), shared-mime-info 2.5.1-2, with the fetch receipts; cite them in the note |

The two **cheap controls that the declaration's list omits**: an oracle shell-out (`/usr/bin/gio mime`) and a
ctypes/libgio call. Both are stopped by the sandbox: 7/89 on the frozen cases (the 7 no-default cases), i.e. the
sandbox does its job for the *binary* route. The third cheap control — the **label table** — is the one that mattered
(F1), and it is now stopped only by the fresh leg.

---

## 1. C1 — counterexample and draft runs

### 1.1 The pure label lookup meets the predicate as frozen at 21:07 (F1)

Artifacts: cases copy `42a08f2cc19f137ac591df5f558e0fb2fba65c7471ce0760e2d755497c53e874` (89 cases, 99 asks; the
lane file had grown from the declaration's 83), oracle copy `c3a13e26…` (identical to the lane oracle), empty mutants
`8b20394a…`, C1 counter **as read at 21:10, sha `f2b23fb8c061a196f184d37e430b9c45083a43212bc2b4f62adc62f123afc67c`**
(the file that ran; it had no `--fresh`), gio `d21642…`, libgio `b38001…`.

The forged tool `cheat_fp.py` (sha `75b5e253…`) hashes the fixture tree under its cwd (path, mode-exec, bytes) and
prints the memorised `{type: label}` for that hash — no MIME parsing, no XDG logic, no `gio`. Its map was built from the
same 89 cases with the oracle module's `materialise`; 99 label keys over 85 distinct trees.

Command (draft; run at 21:15):

```
python3 -I quality/counters/c1-r91-mime-resolution.py --repo mado-shokunin --rev cc0381db… --base-rev cc0381db… \
  --cases S/pins/cases.json --mutants S/mutants-empty.json --oracle S/pins/oracle.py \
  --expect-cases-sha256 42a08f… --expect-mutants-sha256 8b2039… --expect-oracle-sha256 c3a13e… \
  --expect-gio-sha256 d21642… --expect-libgio-sha256 b38001… --scratch-root S/c1run --jobs 8 \
  --draft-tool S/cheat_fp.py
```

Output (DRAFT): `MADO_MIME_RESOLUTION: DRAFT_TARGET_MET pred=PRED-C1-r91-v1 … cases=89 correct=89 l1=89/89 mutants=0
killed=0 oracle_agree=89/89 do_nothing_correct=7 naive_mimeapps_correct=6 cache_only_correct=24 base_tool_correct=0
base_tool=absent tool_sha256=75b5e253…`, rc 3.

The real candidate at its 21:15 bytes (`79645659…`) scored the same frozen predicate `correct=89/89` (rc 3) — the
counter could not tell them apart on the frozen set.

Caveat stated up front: the run used `mutants=[]` (the declared L1 + R91MMutC1 set was not frozen at that point —
F6), so the mutant clause is vacuous *in that run*. It is not the defense: a tool can name-branch
(`if basename == "candidate.py"`) and answer nulls when copied as `m-<id>.py`, which kills every mutant without
containing the mutant logic. `cheat_role.py` does exactly this on the current counter: `cases=89 correct=89
mutants=1 killed=1` (DRAFT, rc 3) while the frozen table is the only answer source; the only leg that stops it is
fresh (`fresh=21/120`). The label-table hole is real for the 21:07 predicate; the role branch shows a non-empty M
does not close it.

**The fix is already in the live counter** (sha `dc97fd64…`, 21:19): `--fresh` (line 164, default 120) and the fresh
block (lines 280-296, `seed = int(sha_bytes(tool_bytes)[:8], 16)`), and `met` now requires `fresh_ok == len(fresh_cases)`
(line 302-303). Re-run against the same frozen cases:

- candidate `ddbcd6e3…` (current build) with fuzz-gen `0d147b83…`: `DRAFT_TARGET_MET … cases=89 correct=89 fresh=120/120
  fresh_seed=3720140515`, rc 3.
- forged role tool `cheat_role.py` (the label table + `if basename == "candidate.py"` else null, so every mutant is
  killed by self-sabotage; 1-mutant file): `DRAFT_TARGET_MISSED … cases=89 correct=89 fresh=21/120 mutants=1 killed=1`,
  rc 3. The frozen table still scores 89/89; the fresh leg stops it.
- earlier pair candidate `596b73…` + fuzz-gen `52ef80…`: **89/89 frozen but 114/120 fresh**, wrong
  `fz-1500214029-030, -038, -074, -086, -089, -099`, i.e. a model that passes every frozen case can still miss real GLib
  alias/parent/recommended-list rules. The current pair passes all 120, but the episode shows the fresh leg is not
  cosmetic; the fz group (`controls/mime-cases-r91-fz.json` was 49 B — empty at 21:14) should carry the minimised
  disagreements.

**Corrections for the declaration:**
1. Paste PRED-C1-r91-v1 **verbatim** into the declaration (round 90 did), including the fresh clause, and name
   `--fresh 120`; the declaration currently only points at the counter docstring (`:51`).
2. Pin the fuzz generator (it changed 21:16→21:28: `52ef8043…` → `0d147b83…`), the cases file, mutants, oracle,
   counter, candidate; give the measurement argv (F6).
3. The counter should reject `--fresh` < 1 (currently `--fresh 0` makes the fresh clause vacuous); the declaration
   should state F = 120.
4. Add the **label-lookup forgery** and the **gio shell-out** as declared controls/replays with their frozen and fresh
   scores (round-90 F10/Forgery precedent): label table frozen N/N, fresh 3/30 (my 30-case run at seed 2036618841) or
   21/120 under the role branch; gio shell-out 7/89 frozen, ctypes 7/89 frozen.

### 1.2 Sandbox: the declared visibility is false (F2)

The counter's `sandbox_argv` (line 63-68) is `--ro-bind / /` + `--bind scratch scratch` + `/dev/null` over
`/usr/bin/gio` and the libgio real path + `--tmpfs <lane>` + `--unshare-net`. There is no masking of the host's XDG or
MIME data, and the **whole scratch root** (all case roots, the mutant copies, and any pinned cases file) is bound
read-write. Probe run inside the exact sandbox:

```
/usr/bin/gio                     size 0, mode 0666      (masked; exec → PermissionError)
/usr/lib/libgio-2.0.so.0         size 0, mode 0666      (masked; dlopen → EACCES)
/usr/share/mime                  dir 0755               (visible)
/usr/share/applications          dir 0755 (5616 B)      (visible)
/etc/xdg                         dir 0755               (visible)
/home/vgpnk/.config/mimeapps.list 0644, 1758 B          (visible)
<lane>                           FileNotFoundError      (masked — correct)
import gi → OK; gi.repository.Gio → "Failed to load shared library 'libgio-2.0.so.0' … Permission denied"
```

So the *forgery defenses for the oracle binary* hold, but the sentence "only the fixture and the tool file are
visible" (declaration `:48-49`) is false, and the scratch binding is a label-leak path: if the L1 passes `--cases`
and friends from under `--scratch-root` (as I did for pinning), the tool can walk to them and read the `expect`
labels. At measurement, keep `--cases/--oracle/--fuzz-gen/--mutants` in the lane (masked) **and** bind only the
per-run `work` dir (or a per-case root + a read-only tool dir). Tmpfs `/usr/share/mime`, `/usr/share/applications`,
`/etc/xdg`, and the user's config/data homes; mask `/usr/lib32/libgio*` (exists) for completeness; `/usr/lib/libgio-2.0.a`
is static and not a route from the isolated `python3`, but the 32-bit `.so` is unmasked.

### 1.3 C1 axis verdict

C1 is a capability acquisition on a surface PROVINCE does not own. The declaration's own evidence ("the lane had no
instrument on this plane: `git cat-file -e cc0381db:tools/mado-mime.py` fails") is an absence of ownership, not a
coverage row. AXES coverage is "fraction of the domain's real surfaces the skill governs (PROVINCE.md lists every
surface; none unexplored without reason)", so the claim needs, before the freeze:
- a PROVINCE refinement naming the default-application plane as a read-only observed surface (the files above);
- the coverage measurement that actually exists: `python3 -I quality/check-index.py --repo . --rev <C1 rev>` —
  at base it is `indexed=111/111 coverage=10.0000/10`; the new note + one `corpus/README.md` row make it 112/112
  (fraction 1.0; harm watch, not a score rise) — and the capability row in SCORECARD.

Without the PROVINCE line the claim is adjacency (report, do not absorb) or an un-scored capability; "coverage 0 →
all" (declaration `:56`) is neither the coverage rubric nor a number the SCORECARD can carry: the "all" is 13 distinct
types / 99 asks in the frozen cases (the host evidence's 538 types is explicitly not scored), so say that instead.

---

## 2. C2 — counterexample and draft runs

### 2.1 A frozen-set lookup table meets the current predicate 45/45 (F3)

Artifacts: independent labels `controls/seat-reports-labels-r91.json` (sha `c1c660d5…`, 46 rounds + 18 G fixtures,
`generated_with` = git only, candidate never opened); live builder `gen-c2-set-r91.py` (sha `8b0fab70…` at the time of
the run; the file changed again to `4a1952fc…`), producing a 45-expectation draft set `55e981cc…` for rounds
90/89/42/71 (I trimmed the round list for cost; the full set is the same shape); current C2 counter `92f8c84b…`;
current check `189b1437…`.

The forged check `cheat_memorize_c2.py` contains no dispatch/report reading: it maps `--round N` to the round's stored
finding lines, `--repo …/fx-<id>` to the fixture's stored rc/ids/summary, and `--all` to the totals; `--selftest`
prints a passing stub. Command (draft):

```
python3 -I quality/counters/c2-r91-seat-reports.py --repo mado-shokunin --rev cc0381db… --base-rev cc0381db… \
  --set S/c2set-live2.json --mutants S/mutants-empty.json \
  --expect-set-sha256 55e981… --expect-mutants-sha256 8b2039… --scratch-root S/c2now --draft-check S/cheat_memorize_c2_live.py
```

Output: `MADO_SEAT_REPORTS: DRAFT_TARGET_MET … expectations=45 met=45 selftest_rc=0 mutants=0 killed=0 base_met=0
always_ok_met=4 always_missing_met=0 receipt_presence_met=6 …`, rc 3. The real check `189b1437…` scored the same
45/45 (rc 3), and its controls were 0/4/0/7 — each below 45, exactly as the predicate requires.

Caveat: `mutants=[]` here too (the L1 + R91MMutC2 mutant file was not frozen). Two more legs are forgeable:
- the counter checks the check's `--selftest` **by exit code only** (`st_rc = subprocess.run(... "--selftest").returncode`,
  counter lines 199 and 218); the memoriser's stub prints `SEAT_REPORTS_SELFTEST: checks=10 failed=0` and exits 0, so
  the gate-standard "assert a stable expected finding-id" leg is not verified by the counter;
- a check copied as `m-<id>.py` can return rc 2 for everything (see the C1 role branch), so a real mutant set is
  killed without exercising the check; the set-echo control is what forces a held-out leg.

Why it works: the predicate only evaluates the **frozen set**, and the set is a file in the lane (the check runs
unsandboxed: `run_check` at counter line 54 passes only `PATH/HOME/LC_ALL/GIT_CONFIG_NOSYSTEM`, no cwd, no bwrap).
The fixture directory names are the expectation ids (`expectations()` line 108: `"fx-" + fx["id"]`), so even without
reading the set a check can key on the basename; the revision expectations are keyed by `--round N`. The current
controls (always-OK, always-MISSING, receipt-presence) do not test this; a **set-echo** control would meet 45/45 and
make the predicate unmeetable, which is the point.

Smallest safe correction, in order of cost:
1. Add a `set_echo` control (reads `--set`, prints every expected finding/summary) and require it below E. It will
   meet E/E, so the predicate cannot pass without a held-out leg — exactly the forcing function.
2. Add a held-out leg computed at measurement, not stored: the round-90 precedent is a **population** — every
   non-merge commit in a frozen range tagged with the expected missing set by plain git (38 commits in round 90).
   For seat reports the labeler is the same `git ls-tree`/`git cat-file` procedure the labels seat used; the check
   can compute it too (that is the gate), but it cannot know the counter's *chosen* fixture set. Alternatively (or
   additionally) generate fresh dispatch trees at measurement from a frozen generator seeded by the check's sha, with
   the expected rc/ids derived by the counter's own reference labeler (not imported from the check).
3. Randomise the fixture directory names (`mkdtemp`-style) so the id is not in the path, and run the check with
   `cwd=root` (the labels' `fixture_harness` contract says "the gate runs with this directory as its root/cwd";
   the counter currently does not set cwd).
4. Pin the measured check's sha in the declaration and require the receipt's `check_sha256` to equal it; otherwise a
   set-echo table copied into `quality/check-seat-reports.py` reads as the candidate.

### 2.2 The declaration's C2 semantics are stale (F4)

At the independent labels file (`c1c660d5…`) and candidate `2e0f08…` (the 21:15 bytes) the counter's 41-expectation
set gave `met=37`, failures **G-fx06-untrailed** (labels rc 1 / SR04, candidate rc 0), **G-fx15-prose-report-no-trailer**
(same), **G-fx13-symlinked-report** (labels SR03, candidate SR01), **G-fx14-mixed-summary** (ids order SR01/SR02 vs the
candidate's dispatch order). The candidate then changed (cde29c…, 189b14…): `WorkTree.is_link`/`GitTree.links` and
`SR03 unsafe …` for symlinks, `SR04` counted in `bad`, `exit 1 any finding`, summary gains `untrailed=`, `judge_fx`
compares sorted ids and optional summaries. Re-run on the live set: **45/45** for the current check `189b1437…`.

The declaration did not follow: `:66-69` still lists "present, missing, empty, unsafe, untrailed, plain residual
trailer, last-trailer-wins" as examples (the set has 40 fixtures: F01-F18, H01-H04, G-fx01…G-fx15) and `:71-76` says
"exact SR01/SR02/SR03 lines" while the candidate and the counter now emit and judge **SR04** (and the gate's exit 1
applies to it). The earlier candidate docstring's "SR04 … not a defect" is gone; the declaration must say:
- SR01 missing (absent), SR02 empty (zero-byte), SR03 unsafe (absolute, `..` component, **or symlink**), SR04 untrailed
  (no trailer → the seat cannot be checked) — **all four rc 1**;
- summary `… unsafe=U untrailed=X verdict=…`;
- the fixture set's F06/F18 (builder fixed at 8b0fab: F06 rc1/SR04, F18 rc1/SR03), and the G fixtures' expected ids.

Repro (DRAFT): the independent labels file + builder + counter + `--draft-check` above; the earlier failures are
reproduced by `G-fx06`, `G-fx13`, `G-fx15`, `G-fx14` (fixture files in the labels' `files` map; e.g. fx06's task is
`/skill:godspeed\n\nOwn: the fixture. No trailer was rendered for this seat.\n`, fx13's trailer target is
`{"symlink": ".real.md"}`).

### 2.3 The builder/labels join was broken in flight (now fixed; freeze note)

At 21:16 `python3 -I controls/gen-c2-set-r91.py controls/seat-reports-labels-r91.json 90 89 42 71` (builder sha
`acbbd5e7…`, labels `c1c660d5…`) failed `KeyError: 'missing'` at `gen-c2-set-r91.py:87` (`tot["missing"]`; the labels'
totals nest the counts under `totals.counts`) and would then fail `g["rc"]`/`g["ids"]` (the labels use
`expected_rc`/`expected_finding_ids`/`argv`/`mode`/`dirs`). The live builder (`8b0fab70…`, later `4a1952fc…`) now
builds the set (rc 0) and maps summaries/dirs/argv. Freeze note: re-run the *final* builder + labels at the freeze,
pin the set sha, and state E; the declaration currently names only the output path `controls/seat-reports-set-r91.json`
(`:66`), not the builder/labels or the count.

### 2.4 C2 axis verdict

C2 is operability (a runnable gate with `--selftest`, PROTOCOL §Gate standard), not calibration/quality work: the
gate's verdict is retention of evidence, not the lane's self-assessment; round 90's C2 receipt-presence gate was the
same axis. State the operability rubric (the hermetic suite fraction is unchanged; the instrument count 0 → 1) and the
capability row question (round 90 entered no capability row for its gate; if this round does, say so).

---

## 3. Records and gates that the round would fail (F5)

1. **Tool ledger.** Fixture: a `git init` repo under `$S` (toplevel asserted), `git -C $L archive cc0381db -- tools
   quality | tar -x`, plus `tools/mado-mime.py` (build `ddbcd6…`), `quality/check-seat-reports.py` (build `189b14…`),
   `quality/counters/{c1,c2}-r91-*.py`, committed under a fixture identity; then
   `python3 -I quality/check-tool-ledger.py --repo $D --rev HEAD` →
   `LEDGER-ROW reason=uncovered path=quality/check-seat-reports.py …` / `…c1-r91-mime-resolution.py` /
   `…c2-r91-seat-reports.py` / `…tools/mado-mime.py`; `LEDGER: population=173 ledger_rows=169 uncovered=4 dangling=0
   bad_pointer=163 … verdict=TARGET_MISSED rev=56ba6ea…`, rc 1. (The 163 bad pointers are the archive's missing
   `.ufo`/`corpus` targets in the trimmed fixture; the four uncovered lines are the point.)
2. **SKILL.md gate registry.** `grep -n 'mado-mime|check-seat-reports|r91' SKILL.md` → no row; round 90 has
   `mado-r90-portal-routing` (gate) and `mado-portals` (probe) rows and the corresponding ledger rows
   (`quality/tool-ledger.md:204-207`). PROTOCOL §Gate standard: "closure grades no gate conformant until its registry
   row exists at the lane's registry home." Add `mado-r91-mime-resolution` (gate/counter), `mado-mime` (probe),
   `mado-r91-seat-reports` (gate/counter), `check-seat-reports` (gate), with the pinned set path and selftest spelling.
3. **Ledger row placement vs separability.** A `quality/*.py` row for the C2 file in the C1 commit is `dangling`
   (the file is absent at the C1 rev); a missing row at either rev is `uncovered`. Add the C1 rows (tool + C1 counter)
   in the C1 commit and the C2 rows (gate + C2 counter) in the C2 commit; likewise the SKILL.md rows.
4. **Corpus index.** `check-index.py --rev cc0381db` → `indexed=111/111 … coverage=10.0000/10`, rc 0. The new C1
   knowledge note needs one `| \`knowledge/<name>.md\`` row in `corpus/README.md`; otherwise `missing=1` at the C1 rev.
5. **Sources.** No S-row for the GLib MIME chain or shared-mime-info (`S502` is gkeyfile only); no
   `.ufo/waves/round-91/fetch/` receipts; the declaration gives only the gdesktopappinfo sha. Open the rows/receipts
   (the lane's provenance pattern: round-90 S501-S503 + fetch), or the knowledge entry's citations are ungrounded.
6. **PROVINCE.** Round 23's inventory table and later refinements account for the lane's instruments; the new tool is
   not named. Add the PROVINCE refinement for the surface + the tool row (F7).

---

## 4. Every wording/predicate defect, with the fix the L1 can apply before the freeze

| # | Location | Defect | Fix |
|---|---|---|---|
| 1 | declaration `:48-49` | "only the fixture and the tool file are visible" — false (F2) | tighten `sandbox_argv` (mask host XDG/MIME roots; bind only `work`; reject label inputs under scratch) or rewrite the sentence to what the sandbox does (gio/libgio masked; lane masked; host XDG/MIME and scratch visible) |
| 2 | declaration `:51` | predicate not stated; only "verbatim in the counter docstring"; the declaration and counter diverged for 12 minutes (fresh in prose at 21:07, not in code until 21:19) | paste PRED-C1-r91-v1 verbatim; add the measurement argv (F6) |
| 3 | declaration `:46-47` | "F cases" / "the frozen fuzz generator" unnamed; generator changed 3×; no F value | name `controls/fuzz-gen-r91.py` sha, F=120, `--fresh 120`; reject `--fresh 0` |
| 4 | declaration `:52-53` | control numbers on "the 83 L1 cases" (6/6/21) are stale; measured 7/6/24/0 on 89; no label-lookup/gio control | state as draft numbers with the file sha; add the label-lookup and gio-shell-out replays with frozen/fresh scores |
| 5 | declaration `:42` | `controls/mime-cases-r91.json` does not exist and no merge tool/procedure is named; `fz` empty, `hx` separate | name the merge tool/sha (round-90 `merge-c1-cases-r90.py` precedent), the merged sha, N, and the oracle label run |
| 6 | declaration `:50` | mutants file/sha/M unnamed | name `mime-mutants-r91.json` sha and M (L1 + R91MMutC1) |
| 7 | declaration `:56` | "MIME types a lane tool resolves 0 → all" — universal without enumeration | "the 13 distinct types / 99 asks of the frozen cases; base 0/N → N/N" |
| 8 | declaration `:64` | "stable finding ids SR01-SR04" without definitions | paste the four finding definitions (symlink/untrailed included) |
| 9 | declaration `:66-69` | fixture list is "e.g."; no E, no set sha, no builder/labels | name the labels file (`c1c660d5…`), builder (`4a1952fc…`), set sha, E; enumerate the F/H/G groups |
| 10 | declaration `:71-76` | predicate omits SR04, the symlink SR03 and `untrailed=`; the candidate is already there | update the predicate text; re-freeze the set; F06/F18 already fixed in the builder |
| 11 | declaration `:70` | C2 mutants file/sha/M unnamed | name `seat-reports-mutants-r91.json` sha and M (L1 + R91MMutC2) |
| 12 | declaration `:71` | no set-echo control; no held-out leg; fixture names are ids | add the set-echo control + population/fresh leg; randomise names; cwd=root |
| 13 | declaration `:80-84` (separability) | the plan is real (disjoint files/counters; C2 absent at C1; C1 re-run at C2) but omits the shared records split and the C1 tool byte-stability | add: ledger/SKILL rows split per commit; `tools/mado-mime.py` bytes unchanged between the C1 and C2 revs (or re-measure C1 at the C2 rev with the same sha) |
| 14 | declaration `:87-90` (routed) | no ledger/registry/index/source items | add D4 ledger rows, D5 SKILL.md registry rows, D6 corpus index row, D7 SOURCES/fetch receipts |
| 15 | declaration `:28-29` (stagnation) | all owned axes at 10; C1/C2 move saturated axes; no PROVINCE row means C1's coverage cannot move | add the PROVINCE refinement + the index rubric; C2's operability rubric unchanged (harm watch) |
| 16 | counter `c1-r91` `:164` | `--fresh` no lower bound | reject < 1 (or require the declared F) |
| 17 | counter `c1-r91` `:63-68`, `:232/:252` | whole scratch bound; tool/mutant copies named `candidate.py` vs `m-<id>.py` (a tool can branch on `__file__` and kill mutants by self-sabotage; `cheat_role` did exactly that: frozen 89/89, mutants 1/1 killed, fresh 21/120) | bind only the per-run dir; name every variant `tool.py` in its own dir; keep the fresh leg mandatory |
| 18 | counter `c2-r91` `:54`, `:108` | the check runs unsandboxed with the lane (and the set/labels) readable; fixture dir = id | sandbox or held-out leg; random names; cwd=root |
| 19 | counter `c2-r91` `:212-215` | controls omit set-echo; receipt-presence stand-in meets the rc2 fixtures | add set-echo; keep the rest |
| 20 | labels/counter contract | labels say the gate runs with the fixture root as cwd; the counter does not set cwd | set `cwd=root` for fixtures (and lane for revisions) or amend the labels' contract |
| 21 | counter `c2-r91` `:199`, `:218` | the `--selftest` leg is `returncode == 0` only; a stub selftest (`checks=10 failed=0`) passes; PROTOCOL §Gate standard requires the exit **and** a stable finding id asserted | require the frozen selftest tally/ids (e.g. parse `SEAT_REPORTS_SELFTEST: checks=N failed=0` against a pinned N, or run the candidate's own selftest expectations from a frozen file) |

Dead steps (transient, recorded so the L1 does not chase them): the C2 builder was schema-incompatible at 21:16
(`KeyError 'missing'`; labels keys `expected_rc`/`expected_finding_ids`), fixed by 21:20; the C1 build file was
mid-edit at 21:20 (`c2a516d8…` scored 2/89 — a mid-edit, not a claim failure) and at 21:24 (`596b73…` scored 89/89
frozen, 114/120 fresh); current `ddbcd6e3…` scores 89/89 + 120/120 with fuzz-gen `0d147b83…`. The freeze must pin one
stable candidate, one case file, one generator, one counter, one set, one mutants file, and re-run both counters on
those bytes. Installs: none (no pacman, no tool install). Host safety respected: only `gio mime TYPE` (one argument)
under `env -i` with fixture roots; no two-argument `gio`, no `xdg-mime default`, no service/shutdown; fixture git only
under `$S` with `rev-parse --show-toplevel` asserted before the first commit; scratch removed on exit.

---

## 5. Answer to the three assigned questions

1. **Cheap controls.** Do-nothing 7/89; naive mimeapps 6/89; mimeinfo.cache-only 24/89; base absent 0; oracle shell-out
   7/89; ctypes libgio 7/89 (all blocked by the gio/libgio masks); **label table 89/89 on the frozen cases as the
   predicate stood at 21:07** (DRAFT_TARGET_MET) and 3/30 or 21/120 on fresh; the current counter's fresh leg catches
   it. C2: always-OK 4/45, always-MISSING 0/45, receipt-presence 7/45, base 0/45, **frozen-set echo 45/45**
   (DRAFT_TARGET_MET) — the C2 predicate has no leg that this control cannot satisfy.
2. **Axis naming.** C1 is coverage only after a PROVINCE amendment (the default-application plane is not in the Owns
   list) and with the real coverage rubric (`check-index` 111/111 → 112/112; the coverage fraction stays 1.0; the
   capability row is the acquisition). C2 is operability (a runnable gate, PROTOCOL §Gate standard), not quality work;
   its rubric is the instrument count (0 → 1) with the suite fraction unchanged. Universal clauses without enumeration:
   C1 "all" types, "every frozen case/mutant"; C2 "every frozen expectation", "each control"; the fixture "e.g." list —
   each needs N/M/E/F and a file sha. The separability plan is real (disjoint files/counters; C2 absent at C1; C1
   re-run at C2) with the shared-records caveat and the stable-tool-bytes requirement.
3. **Wording/predicate defects.** Table §4, items 1–20; the freeze-blocking ones are 2, 3, 5, 6, 9, 10, 11, 12, 14
   (contract/pins), 17–19 (counter weaknesses) and F5's ledger/registry/index/source rows.

---

### Reproducing the two headline counterexamples (after scratch deletion)

C1 label table: build `cases.json` from `controls/mime-cases-r91-l1.json`, hash each fixture tree under its cwd with
`(relpath, exec-bit, bytes)`, store `{treehash|desktop|type: expect}` from the oracle-materialised cases; the tool emits
the stored label. Run the counter at the pinned shas with `--draft-tool`. Expected: frozen 89/89, `DRAFT_TARGET_MET`
with the predicate as read at 21:10 (sha `f2b23f…`); `DRAFT_TARGET_MISSED` with the 21:19+ counter (fresh 3/30 or
21/120). C2 set echo: rebuild the set with the builder+labels, read the set, print the findings/summaries for
`--round N`, `fx-<id>` basenames and `--all`; expected 45/45 with the current counter and an empty mutants file
(the real mutants would need the role branch to be killed — `cheat_role` shows the mechanism).
