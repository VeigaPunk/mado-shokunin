# ReviewJjDispositionFinal — corrected fix-or-why-not table for JjAuditMado / JjTrialMado

Seat: `MadoR18.ReviewJjDispositionFinal` (reviewer, leaf). Observed 2026-10-20
16:00–16:06Z (13:00–13:06 -0300). Target: `.ufo/waves/round-18/drafts/JjDisposition.md`
against `w1/reports/{CriticJjDisposition,RevJjTrialFindings,ConnJjFleetFixes}.md` and the
landed state at **`4c103b55b1ea5c3c555884afe3eb69b5189701b7`** (integration) with lane
`refs/heads/master` = `refs/remotes/origin/master` = **`abfbf35b1ed4d4a1eb294d525ef286be30f3886f`**
(receipts, child of `4c103b5`), HEAD detached at `abfbf35b` (`git symbolic-ref -q HEAD` rc=1).
Read-only git only; no jj command; no write outside this report; no installs.

Status key: **HOLDS** (true, evidence cited) · **FIXED-LANDED** (in `4c103b5`, verified by bytes) ·
**PARTIAL** · **OPEN** (not fixed, why-not stated) · **NOT-RE-RUN** (host pause) ·
**FLEET-OWNED** · **REJECTED** (a recommendation, with counterexample).

---

## 0. Verdict

The draft is correct on F1/F3/F7/F11–F13 and on the audit's incident residue. It is **stale or
wrong on twelve rows**, and its central inference — "the live lane has no repo jj config" — is a
**false premise**: jj 0.45 stores per-repo config at `~/.config/jj/repos/<config-id>/config.toml`,
not in `.jj/repo/`. Four draft rows are derived from that premise (R5, T4, H1, H7) and all four
invert. Two drafted recommendations (R2, R3) are **regressions** on this host. F10/F14/PIN are
**landed**; `.gitignore` is **committed**, not worktree-only; F16's why-not is the wrong reason.

| Draft row | Draft said | Final |
|---|---|---|
| F10 (`:3406` pipe-rc) | PENDING — GateRcFix | **FIXED-LANDED** at `:3477-3485` + OM9 |
| F14 (stub cannot fail) | PENDING — GateRcFix | **FIXED-LANDED** — per-verb rc knobs + OM9/OM10 |
| F15 (PIN drift) | OPEN, still `cd1d73d7…` | **PARTIAL** — PIN re-cut to `20714096…`; `/tmp` hardcode remains |
| H4 / T2 (`.ufo/state/`) | FIXED, worktree only | **FIXED-LANDED in HEAD** (blob `e8a7bb62…`) |
| R5 (init repairs `.jj`) | HOLDS in code, "NOT HOLDING live" | **HOLDS live** — config present and correct |
| T4 (config beyond init) | "CONTRADICTED for live lane" | **HOLDS** — all four keys in the host config file |
| H1 (`auto-track`) | PARTIAL, "UNVERIFIED" | **HARDENED** — `none()` verified by bytes; ignore in HEAD |
| H7 (`@` author) | OPEN, "would be authored as operator" | **HOLDS** — repo identity is `mado-shokunin` |
| F17 prior jj runs | CONFLICT | **FLEET-OWNED, resolved** — current store is helper-only |
| F6 / R2 | recommend `refs/heads/master` | **OPEN + R2 REJECTED** — false PASS after branch switch |
| F9 / R3 | recommend `rev-parse --git-dir` | **OPEN + R3 REJECTED** — upward discovery to `~/.git` |
| F16 / R4 | "needs a PIN re-cut" | **FLEET-OWNED** — wrong plane and duplicate authority |

Two further corrections to the sources: ConnJjFleetFixes' "SKILL count stale (`268/268` vs
`372/372`)" is not substantiated (every `268/268` in SKILL.md is append-scoped to `93e43f8f…`),
and the fleet jj helper was **replaced after the w1 reports** — installed `scripts/hyaku/jj-lane.sh`
is now sha256 `3369dc27…` (33,599 B, mtime 13:03:03 -0300 = 16:03Z), not the `24790416…` the
w1 reports audited. See §7.

---

## 1. Landed state, measured

All commands run from the lane root; outputs verbatim (truncated only where noted).

```
$ git rev-parse refs/heads/master refs/remotes/origin/master
abfbf35b1ed4d4a1eb294d525ef286be30f3886f
abfbf35b1ed4d4a1eb294d525ef286be30f3886f
$ git merge-base --is-ancestor 4c103b55 refs/heads/master ; echo $?      → 0
$ git rev-list --left-right --count refs/heads/master...refs/remotes/origin/master → 0  0
$ git show 4c103b5:tools/mado-verify.sh | sha256sum
c9fb0cef3e081dc878d69f8e20c148429bdfbdce949f8afaed705db957ea42b5  -
$ sha256sum tools/mado-verify.sh                                         (same, worktree)
$ bash tools/mado-verify.sh --selftest ; echo rc=$?
MADO_SELFTEST: 389/389 assertions passed
rc=0
```

* `.gitignore` **in HEAD**: `git show 4c103b5:.gitignore` (blob `e8a7bb62…`, 52 B) =
  `.ufo/interactive-sessions/`, `.ufo/state/`, `__pycache__/`.
  `git check-ignore -v .ufo/state/x` → `.gitignore:2:.ufo/state/` rc 0;
  `git ls-tree -r 4c103b5 | grep -c 'ufo/state'` → 0.
* Gate rc fix (diff `d9a5a18..4c103b5`, +81/−7): stub per-verb knobs at `:666-682`
  (`STUB_GIT_DESCRIBE_RC` / `STUB_GIT_REVPARSE_RC` / `STUB_GIT_SHOW_RC`); OM9 `:811-829`
  (`STUB_GIT_SHOW_RC=128` → `vs_head UNKNOWN`, detail names the path and `rc=128`, no
  "local edit"); OM10 `:832-851` (describe/rev-parse rc=128 → UNKNOWN, no "MOVED");
  row fix `:3468-3488`:

  ```
  blob=$(set -o pipefail; tmo git -C "$tree" show "HEAD:$OMARCHY_SKILL_REL" 2>/dev/null \
    | sha256sum | cut -d' ' -f1); grc=$?
  ...
  if [ "$grc" != 0 ]; then
    row omarchy omarchy.skill.vs_head UNKNOWN "cannot read HEAD:$OMARCHY_SKILL_REL (rc=$grc) …"
  ```

  `PIPESTATUS` is not used (`grep -c PIPESTATUS tools/mado-verify.sh` → 0) — the measured
  trap in ConnJjFleetFixes §4.1 is avoided (substitution-scoped pipefail, sound form).
* `PIN_MADO='20714096e1481e92c8f75414968b596b5b7c31cc684c1dd94b9c3edb0f772744'` (`:1704`).
  The selftest's R10 assertion (`:583`) compares the derived target (the file with the two
  MADO-R7 blocks excised) to `PIN_MADO`; my 389/389 run therefore proves the pin equals the
  landed bytes. Regression receipt `.ufo/waves/round-18/evidence/regression-recut.txt`:
  `MADO_REGRESSION: PASS … target=20714096…`, `CONTROL: GREEN`, D1–D9 + R1 all `KILLED`
  (10/10, 0 survived, flips 0), `MUTATE_RESTORE OK`. The first verdict line in that receipt is
  the expected `SETUP` refusal of the *old* pin (`cd1d73d7…`); the file's final verdict is PASS.
* Red-before receipt `.ufo/waves/round-18/evidence/gate-rc-redbefore.txt` §1: old gate at
  `d9a5a18`, stub `show` rc=128 → `FAIL … HEAD blob e3b0c44298fc… (local edit)`; the new gate's
  OM9 asserts the opposite.

---

## 2. JjAuditMado findings F1–F17 — final dispositions

| ID | Finding (short) | Final | Why-not / residual | Evidence at `4c103b5` |
|---|---|---|---|---|
| F1 | `mado-action-plan.py` has no git content | **HOLDS** | none needed | `git show 4c103b5:tools/mado-action-plan.py \| grep -n git` → no match; only `_self_invoke` (`:522`, called `:741,:845`) |
| F2 | Three executed git calls + precondition + stub | **HOLDS (inventory)** | numbers shifted: `:3382/:3391/:3406/:3347` → `:3447/:3456/:3477/:3412`; `grep -c 'git -C'` = 3 | gate `:3412` `[ -d "$tree/.git" ]`; `:3447` describe; `:3456` rev-parse; `:3477` show; stub `:666-682` |
| F3 | omarchy checkout is plain git, not colocated | **HOLDS** | bytes only; no git/omarchy command run there | `.git` is a directory; `.jj` absent; `.git/HEAD` = `ref: refs/heads/master`; `packed-refs` = `8fcc9d60… refs/heads/master` and `8fcc9d60… refs/tags/v3.8.4`; gate pins `:3334-3335` match |
| F4 | Live gate's three git rows PASS | **NOT-RE-RUN** | live layer needs `omarchy`/`hyprctl`; contract permits only `--selftest`/`--regression`. The stubbed live-layer suite (OM1–OM10) passes inside the 389/389 run; the audit's live observation is neither confirmed nor contradicted | `--selftest` rc 0; no live run |
| F5 | Colocated sandbox behaviour (`fixA`) | **NOT-RE-RUN** | jj forbidden; no sandbox rebuilt; consequences covered by F6 | — |
| F6 | HEAD-as-tip rows (`:3447`,`:3456`) misreport after `jj new` | **OPEN (by design, fail-closed)** | The rows still resolve HEAD. They fail closed: `describe` rc≠0 → UNKNOWN, `rev-parse` mismatch → FAIL/UNKNOWN, never a false PASS. The target is plain git (F3) and is not a colocation target (colocation covers lane repos). **R2 rejected** — see §3. The future form is **HEAD tree identity** (`HEAD^{tree}` vs `v3.8.4^{tree}`), which needs a new pin; round 19 | gate `:3447` (`git describe --tags --exact-match`, no ref), `:3456` (`git rev-parse HEAD`); host switches branches via `bin/omarchy-branch-set:18` and `bin/omarchy-update-branch:26` |
| F7 | No class-A markers | **HOLDS** | `symbolic-ref`, `@{u}`, `--abbrev-ref`, `branch --show-current` → no hits; `git status`/`--porcelain` only in a comment (`:3327`) and a selftest label (`:788`) | grep of the whole gate |
| F8 | Class-C index recipes unsafe across jj mutations | **OPEN (doc, L1)** | Doc-only and outside claims C1–C3. Latent: after a jj mutation the git index may not equal HEAD. Recommended form: commit-to-commit ranges, `git diff --numstat <base> <tip>`; delete the `git status` recipe | SKILL.md `:1084`, `:1264`, `:1408` (`git diff --numstat`), `:1673` (`git status --porcelain`) |
| F9 | `[ -d "$tree/.git" ]` misses worktree checkouts | **OPEN (latent)** | No live target is a worktree; the row's verdict is UNKNOWN but its detail ("no git checkout at $tree") is false. **R3 rejected as written** — `rev-parse --git-dir` walks upward to `~/.git` (§3). Safe minimal form if ever wanted: `[ -e "$tree/.git" ]` + a gitfile OM scenario; gate bytes move, so round 19 | gate `:3411-3412`; `.git` in both targets is a directory |
| F10 | `vs_head` turns an unreadable HEAD blob into a false "local edit" | **FIXED-LANDED** | rc captured before hashing; `grc≠0` → UNKNOWN naming path+rc; red-before recorded; the dead `-z` belt is retained but documented unreachable and harmless | gate `:3468-3488`; OM9 `:811-829`; `gate-rc-redbefore.txt` §1; `--selftest` 389/389 (my run) |
| F11 | No hooks in use | **HOLDS** | lane `.git/hooks`: no non-sample entry; `git config --get core.hooksPath` rc=1; omarchy `.git/hooks`: no non-sample entry | byte listing |
| F12 | No attributes or eol; LFS filters inert | **HOLDS, correction stands** | No `.gitattributes` or `.git/info/attributes` in either tree. `filter.lfs.*` originates in `file:/home/vgpnk/.config/git/config` (`git config --show-origin`), not the omarchy repo config | `git config --show-origin --get-regexp '^filter\.lfs\.'` (4 lines); attribute-file absence |
| F13 | jj bypasses hooks and eol | **HOLDS (latent)** | Nothing to bypass: no hooks, no attributes (F11, F12) | F11/F12 |
| F14 | Selftest git stub cannot fail | **FIXED-LANDED** | Per-verb rc knobs; OM9/OM10 assert the three UNKNOWN arms; +17 assertions vs round 17 | stub `:666-682`; OM9/OM10 `:810-851`; `gate-selftest.txt` = 389/389; my rerun 389/389 rc 0 |
| F15 | Selftest hardcodes `/tmp`; `PIN_MADO` drift | **PARTIAL** | PIN re-cut **landed** (`20714096…`, derived-target equality proven by R10 + selftest). `/tmp` mktemp templates remain at `:395` and `:1925` (ignore `TMPDIR`; cleanup is prefix-guarded). The source-claim "SKILL count stale 268/268 vs 372/372" is **withdrawn**: all four `268/268` occurrences (`:1393`, `:1506`, `:1683`, `:1706`; `:704` is an early `28/28` receipt) are append-scoped to `93e43f8f…`/2026-10-14, i.e. historical receipts, not a current claim | `:1704`; `:395`; `:1925`; SKILL contexts |
| F16 | No landedness check; lane was 8 ahead | **VERIFIED / FLEET-OWNED** | Lane is landed: `master = origin/master = abfbf35b`, ahead/behind 0/0, `4c103b5` ancestor. A gate row is **wrong**: `mado-verify.sh` gates the host config plane, not lane push state; the row would go red by design mid-round and duplicate the fleet's authority (`closure-prompt.md:22-26` step 1; helper now prints `landed <hash>` after `ls-remote`). What the lane owes is **one landedness receipt** at round end — none exists in `evidence/` today | `git rev-list --left-right --count` 0/0; `merge-base --is-ancestor` rc 0; `evidence/` listing |
| F17 | jj has been run in the live lane | **FLEET-OWNED — resolved; premise corrected** | The current op store (31 ops, 1 head, 12:18:08–12:56:40) contains **only helper-shaped** verbs: `git init --colocate`, `--ignore-working-copy bookmark`, `commit`, `diff --summary`, `file track`, `git push`; **0** hits for `jj log/status/show/describe/new`. All current writes are the helper's designed integration path. The audit's transscribed `jj log` ops belong to the **pre-12:18 store**, which no longer exists (`.jj` birth 12:18:08; the helper inits only when `.jj` is absent) — deleter `[UNK]`. "CONFLICT" removed: the fleet rule makes the helper the sole jj caller; the round's "no jj at all" binds seats. Known miss carried: the tripwire has no jj class (`SKILL.md:537`) | `.jj/repo/config-id`; op-store verbs (below); `lane-addendum.md:133-140`; `closure-prompt.md:24-28` |

---

## 3. §9 recommendations — corrected

| Rec | Recommendation | Final | Why |
|---|---|---|---|
| R1 | Fix `:3406` rc handling; add a failing-git OM scenario | **DONE (landed)** | F10/F14 above; OM9 is the scenario |
| R2 | Resolve the tip (`refs/heads/master`) instead of HEAD | **REJECTED** | **False PASS.** Reproduced in `/tmp/revjj-f6.*` (git 2.56.0): tag `v3.8.4` on `master`, then `git switch -c dev` + one commit → `describe HEAD` = `fatal: no tag exactly matches 'faa29e1…'` (today's row: UNKNOWN), but `describe master` = `v3.8.4` and `rev-parse --verify refs/heads/master` = the pin (`e33d41a9…`) while the worktree is `dev` — two identity rows would falsely PASS. The pin's meaning in the gate is "what is checked out" (`:3463` "every pin held at the old HEAD …", `:3370` "== HEAD:version blob at the pinned HEAD"). Host tools switch branches (`omarchy-branch-set:18`, `omarchy-update-branch:26`). Future form: HEAD **tree** identity |
| R3 | `rev-parse --git-dir` in place of `[ -d .git ]` | **REJECTED as written** | **Misattribution.** Reproduced: with a git repo at `$HOME` and a tree lacking `.git`, `git -C "$tree" rev-parse --git-dir` → `$HOME/.git` rc 0 and `rev-parse HEAD` → the dotfiles HEAD; the head row would report `MOVED: rev-parse HEAD → <wrong repo>`. Safe minimal form: `[ -e "$tree/.git" ]` (a gitfile makes the row work; a broken gitfile gives rc 128 → UNKNOWN). Optional, round 19, with a gitfile OM scenario |
| R4 | Landedness row in the gate | **NOT A GATE ROW** | Wrong plane (host config vs lane push state), would be red by design before every push, and duplicates `closure-prompt.md` step 1 + helper `landed`. Lane records one receipt instead (F16) |
| R5 | `init` must handle a pre-existing `.jj` | **HOLDS live** | The config **is** present: `~/.config/jj/repos/0c6bba43…/config.toml` (200 B, mtime 12:29:32) holds `trunk()=master@origin`, `snapshot.auto-track="none()"`, `user.name=mado-shokunin`, `user.email=mado@shokunin.local`. The installed helper re-applies `config set --repo` unconditionally after the `.jj` guard; on an existing `.jj` it imports HEAD with a `jj status` before any other call, and on a first colocation it refuses a staged index ("jj init would silently unstage them"). It still cannot untrack pre-existing `@` additions — it warns (and the new commit path warns on refused paths) |
| R6 | Keep jj out of live lanes entirely | **RESOLVED by fleet rule; not a conflict** | `lane-addendum.md:133-140`: never run a mutating jj command; "the helper is the only writer". `closure-prompt.md:28`: "Never run a jj command in the lane except through the helper". The round's stricter "no jj at all" binds seats; L1's helper commits are the designed path (op store §2/F17). Operator directive `67a3123` (fleet-root commit, not in the lane log; subject: "jj as git manager from now on on shokunin runs") is about shokunin commits *through the helper* |

---

## 4. JjTrialMado hazards H1–H7 — corrected

| ID | Hazard | Final | Evidence / why-not |
|---|---|---|---|
| H1 | Unignored `.ufo/` growth | **HARDENED; residual helper vector** | `.ufo/state/` is in the **HEAD** blob (line 2) and `__pycache__/` line 3; `check-ignore` rc 0; 0 tracked paths under `.ufo/state`; `snapshot.auto-track="none()"` verified in the host config. Residual: `.ufo/watchdog.log` is **not** ignored (`check-ignore` rc=1), and the ignore is not the invariant — the helper's `file track --include-ignored` can still admit ignored paths. The **new** helper adds a post-commit `git status --porcelain --ignored` check (`jj-lane.sh:665`); not measured by me |
| H2 | `git add` staging destroyed by jj mutations | **HOLDS for fleet doc; OPEN for SKILL.md** | `lane-addendum.md:133-137` now says "**Never** `git add`, `git commit`, …"; SKILL.md still has no `git add` or colocation guidance (only `:537` names jj as a non-class). T3 remains for L1 |
| H3 | Detached HEAD after every mutation | **HOLDS (observed)** | `git symbolic-ref -q HEAD` rc=1; HEAD = `abfbf35b` detached at the tip. No tool consumes HEAD (F7); receipts must use resolved refs |
| H4 | `.ufo/state/` not ignored | **FIXED-LANDED (HEAD, not worktree)** | blob `e8a7bb62…` in `4c103b5`; `check-ignore` rc 0; `git ls-tree` 0 under `.ufo/state` |
| H5 | Unignored >1 MiB scratch refused by jj | **PARTIAL / population stale** | No file >1 MiB under `.ufo/waves/round-18`; the only >1 MiB path in the worktree is `.ufo/interactive-sessions/…jsonl`, which is ignored (line 1). The helper's cap is now **10 MiB for named files** (`:540`) and a warn-and-skip for refused paths (`:665-666`); the "1 MiB" wording comes from jj's `snapshot.max-new-file-size`. The draft's 259-path population is stale (w1 reports are tracked at `4c103b5`) |
| H6 | No symlinks, nested `.git`, generated dirs | **CORRECTED** | **Two** tracked symlinks at `4c103b5`: `.ufo/waves/round-17/tripwire/hardening/symlink-target.jsonl` → `/etc/hostname`, and `.ufo/waves/round-18/tripwire/frozen/symlink-input/inputs/link.jsonl` → `payload.txt`. No nested `.git`. Both are fixtures |
| H7 | `@` author identity | **HOLDS (identity configured)** | Repo config sets `user.name=mado-shokunin` / `mado@shokunin.local`; a jj commit outside the helper would still be authored `mado-shokunin` (repo config overrides the user config). The draft's "would be authored as the operator" is false. `d9a5a18` is `protocol-shokunin` because the helper ran `--as protocol` (intentional) |

---

## 5. JjTrialMado recommendations T1–T5 — corrected

| Rec | Recommendation | Final | Evidence / why |
|---|---|---|---|
| T1 | Adopt `jj-lane.sh` | **DONE** | Op store proves helper init/commit/push; identity and ancestry hold; lane `landed`; helper now prints `landed <hash>` verified by `ls-remote` (`jj-lane.sh:234-249`) |
| T2 | Add `.ufo/state/` to `.gitignore` | **DONE (committed)** | `4c103b5:.gitignore` line 2 |
| T3 | Fleet doc note: seats must not `git add` | **DONE in fleet doc; OPEN in SKILL.md** | `lane-addendum.md:133-137`; SKILL.md silent (owner L1) |
| T4 | No per-lane jj config beyond `init` | **HOLDS** | The four keys live in `~/.config/jj/repos/0c6bba43…/config.toml`, which is exactly the per-repo config `init` writes; the draft's "CONTRADICTED" rests on the wrong path |
| T5 | No tooling installs | **HOLDS** | This seat installed nothing; no pacman/sudo/jj run. jj present at `~/.local/bin/jj` (0.45.1 per `RevJjTrialFindings`, version not re-read here) |

---

## 6. False premises corrected (each was load-bearing in the draft)

1. **"`.jj/repo/config.toml` is absent, so the live lane has no repo config."** The path is
   wrong. jj 0.45's own binary says "Per-repo config is stored in the same directory as your
   user config for security reasons." (`strings ~/.local/bin/jj`). Resolution chain, bytes only:
   `.jj/repo/config-id` = `0c6bba4313e6b57d66ba` (20 B) →
   `~/.config/jj/repos/0c6bba43…/metadata.binpb` names
   `/home/vgpnk/Projects/shokunin/mado-shokunin/.jj/repo` → `config.toml` beside it (200 B,
   mtime 12:29:32) holds all four keys. `.jj/repo/config.toml` is indeed absent, but that is
   not where jj looks. Consequent corrections: R5 HOLDS, T4 HOLDS, H1's live rule verified,
   H7 identity correct.
2. **F10/F14 are "PENDING".** True at the draft's `d3a0000` read time; false at `4c103b5`
   (gate sha `fba82a66…` → `c9fb0cef…`; PIN `cd1d73d7…` → `20714096…`).
3. **F15 "PIN_MADO still `cd1d73d7…`".** It is `20714096…` at `:1704`, and R10 proves it equals
   the derived target.
4. **H4 "worktree only".** It is in the HEAD blob, so the branch carries it.
5. **F16 why-not "a gate row needs a PIN re-cut".** The re-cut happened anyway; the real reasons
   are subject (host config plane vs lane push state) and duplicate authority.
6. **F16 "the gate's own rule (`:3262`) forbids `git status` on checkouts".** The rule is scoped
   to the **omarchy checkout** (`:3327`: "Never `git status`/`fetch` on the checkout"),
   and `lane-addendum.md:136` explicitly allows read-only `status` in a lane. The helper's
   `state` still runs `git status` and is not side-effect-free, but that is ConnJjFleetFixes H10, not a gate rule.
7. **F6 "read-only to this lane".** The fix is lane code; the why-not is the **false PASS** that
   R2 introduces, not read access.
8. **F6 "the fix changes gate bytes, so PIN_MADO must be re-cut".** True but irrelevant — every
   gate edit triggers a re-cut, and round 18 re-cut once already.
9. **H6 "one tracked symlink".** There are two at `4c103b5`.
10. **Conn's "SKILL count stale 268/268 vs 372/372".** The `268/268` lines are append-scoped to
    `93e43f8f…` and a dated append; they are historical receipts, not a current count claim.
    Nothing in SKILL.md asserts the current selftest count, so there is nothing stale to re-cut.
11. **F17 "CONFLICT".** The fleet rule (helper sole writer; seats no jj) resolves it. The current
    op log cannot see before 12:18:08 — the store was recreated — so no conclusion about the
    audit-era `jj log` runs may be drawn from it; the audit transcription is the only evidence,
    and the deleter is `[UNK]`.
12. **Draft status line "master = origin/master = `d3a0000`, not re-fetched".** Now
    `master = origin/master = abfbf35b` (receipts), with `4c103b5` an ancestor (0/0).

---

## 7. Fleet changes during the round (affects every helper citation)

* Installed helper `scripts/hyaku/jj-lane.sh` at my read: **sha256 `3369dc27…`, 33,599 B,
  mtime 2026-10-20 13:03:03 -0300 (16:03Z)**. The w1 reports cite `24790416…`; the helper was
  replaced after those reports (the `.new` drafts are gone), and `jj-lane-selftest.sh` is now
  32,120 B at the same mtime. The installed bytes now contain the rewrite's
  guards: fast-forward preflight (`:211`), `report_landed` with `ls-remote` verification
  (`:234-249`), divergence refusal (`:289`), canonical lane path/lock, and "`--ignore-immutable`
  is never used" (`:322`). `cmd_state` still runs `git status --porcelain` (`:176`, header
  `:153` "pure git, read-only"), so H10 survives in the installed file.
* Consequence: the w1 helper-owned catalogs (Conn H1–H20; JjSentinel F1–F9) describe the
  **previous** bytes and must be re-derived against `3369dc27…` before any closure cites them as
  live. Lane-owned findings F1–F17 are unaffected except T1/R5/F16, corrected above.
* The lane's last two commits were authored through the helper **before** that replacement
  (12:55/12:56); this is visible in the op store, so no lane hash is retroactively attributed to
  the new bytes.

---

## 8. Residual risk

* **F6 remains latent.** If anyone colocated the omarchy checkout (nobody plans to) the tag row
  would go UNKNOWN/FAIL, honestly. The safe future expression is a HEAD tree-identity pin.
* **F9 remains latent** for worktree checkouts, with a false detail string (verdict safe). The
  `-e` form is available but moves the gate and would need a fresh PIN.
* **The `.ufo/state/` ignore is not the invariant.** `jj file track --include-ignored` and a
  named-directory commit can still admit ignored content; the new helper's post-commit
  `--ignored` check is fleet code and was not measured here.
* **`.ufo/watchdog.log` is unignored** (`check-ignore` rc=1) — a growth path the round-17 lesson
  did not name.
* **No landedness receipt exists** in `.ufo/waves/round-18/evidence/`; the lane should append
  `rev-list --left-right --count` + `merge-base --is-ancestor` + the tip hash at round end.
* **SKILL.md doc debt** remains: class-C recipes (F8) and no `git add`/jj-colocation note (T3);
  the tripwire still has no jj class (`:537`), so a seat running `jj log` in the lane is
  invisible to `mado-tripwire` — a known miss, round 19 candidate.
* **Live gate rows were not re-observed** (host pause); F4 relies on the audit plus the stubbed
  OM1–OM10 suite.

## 9. Verification gaps and commands run

Performed (read-only): `git rev-parse|show|log|diff --stat|diff --numstat|ls-tree|cat-file|check-ignore|merge-base --is-ancestor|rev-list --left-right --count|config --show-origin`;
`sha256sum`, `stat`, `readlink`, `find` (sizes), `strings` on `.jj` op-store bytes and
`~/.local/bin/jj`, `ls`/`grep`/`sed -n` on the helper and addendum. One hermetic run:
`bash tools/mado-verify.sh --selftest` → `389/389`, rc 0 (the contract's allowed mode).
Two `/tmp` experiments (`git 2.56.0`, `HOME` redirected, dirs removed after): the F6 branch-switch
false-PASS and the F9 upward-discovery misattribution.

Not performed: no jj command; no live or `--no-live` gate; no `--regression` re-run (cited the
committed receipt); no helper selftest (drives jj); no `git status` in the lane; no
`git ls-files -o` (outside the contract's read-only list), so the draft's untracked population
was not re-derived; no network fetch (refs read locally); no omarchy/config command, no pacman,
no sudo, no host probe. Installs: none.
