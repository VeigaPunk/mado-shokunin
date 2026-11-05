# R88MConnector — sibling overlap and cross-claim separability (read-only)

Round 88, wave w1, seat R88MConnector. Base `24ba2a9ddac21c1211579231e6ee1d98963f9988`.
Scope: sibling-lane scan, merge-package check, C1/C2 causal separability, earlier-round pattern reuse.
No candidate score was run: C1/C2 were executed only in `--selftest` and against the BASE tool.
No lane file outside this report was written.

## 0. Commands run (each with its exit code)

| # | command (fleet/lane paths absolute in the transcript) | rc | observed |
|---|---|---|---|
| 1 | `python3 -I quality/counters/c2-r88-include-containment.py --selftest --scratch-root $S` | **0** | `SELFTEST: passed=12/12` |
| 2 | `python3 -I quality/counters/c1-r88-mako-fields.py --selftest --scratch-root $S` | **0** | `SELFTEST: passed=15/15` |
| 3 | c2 counter, `--rev`/`--base-rev` = base `24ba2a9`, cases/mutants sha-pinned | **2** | `MADO_MAKO_CONTAINMENT: SETUP_ERROR git show 24ba2a9…:.ufo/waves/round-88/controls/containment-mutants-r88.json failed in .: fatal: path … exists on disk, but not in '24ba2a9…'` — dead step, see §6 |
| 4 | base tool + `--read-root /tmp` | **2** | `mado-mako.py: error: unrecognized arguments: --read-root /tmp` |
| 5 | hardlink probe under `$S/hl` (below) | 0 | realpath stays in-root, `nlink=2`, same inode as the outside file, content read |
| 6 | strace of `os.path.realpath` on an out-of-root symlink under `$S/esc` | 0 | `newfstatat(link, NOFOLLOW)` · `readlink(link)` · `newfstatat(outside target, NOFOLLOW)` |
| 7 | `readlink -f ~/.config/mako/config`; `readlink -f ~/.local/share/omarchy/default/mako/core.ini` | 0 | both resolve **inside `$HOME`** (True/True) |

Pins re-hashed, all match the declaration: `containment-cases-r88.json` `3ee0dc9b…766f2`,
`containment-mutants-r88.json` `49373eee…084a85`, `mako-mutants-r88.json` `40645a28…761d49b`.
`mako-cases-r88.json` was **ABSENT** (`test -s` false) at scan time; the C1 separability verdict below rests on the
case *schema and materializer*, not on the unwritten file.

## 1. Sibling-lane overlap

Sibling lanes are `/home/vgpnk/Projects/shokunin/*-shokunin` (20 lanes, mado excluded), plus the three shokunin
trees outside the fleet root (`/home/vgpnk/Projects/kimi-shokunin`, `shokuknow/tabi-shokunin`,
`shokunoin/kama-shokunin`). Query set: `\bmako\b`, `makoctl`, notification-daemon/notify-send/dunst/swaync,
`parse_boolean`, `path_resolution|include containment|symlink escape`, plus per-lane `realpath|readlink -f`.

| lane | path:line | what it is | overlap with C1/C2 | disposition |
|---|---|---|---|---|
| kengaku | `corpus/evidence/round95/graders/fix-code-vulnerability/upstream-bottle/bottle.py:4037-4040,4399` | Python **Mako template** adapter inside vendored Bottle | **none** — homonym (Python templating, not the Wayland notification daemon); no criteria grammar, no include= | ignore |
| game-dev-3d | `corpus/knowledge/unreal-mcp/adaptation-kimi.md:399` + 6 report copies (`reports/round-101..103/…`) | `notify-send -a 'Kimi Code'` call site in a hook | **none** — a notification *producer*, not the daemon's config resolver; no mako config, no criteria, no include | ignore |
| chousa | `corpus/knowledge/sweep-symlink-r19.md:1-47` (defect :10-23, fix :25-30, limits :32-37) | canonicalize **every** glob match, check both declared roots, refuse the whole sweep; named limits: post-expansion traversal, TOCTOU, `--root /` vacuity | **same stance family, different surface** (their `root_r`+`lane_r` ≈ C2's `--home`+`--read-root`); no shared bytes | **cite** — the closest prior art; reuse its `refused unopened` limit wording (§5) |
| chousa | `corpus/knowledge/hardlink-alias-r13.md:9-16,22-30,40-50` | symlink/hardlink canonicalization asymmetry; `nlink != 1` → refuse unread; named FP class | **C2 limit** the realpath rule cannot see; mado's draft already names it (`draft-knowledge…:105-107`) | **cite** — corroborates the draft; no case needed |
| chousa | `corpus/knowledge/pointer-boundary-r21.md:1-40` | relative pointer canonicalized, then checked against **both** roots; denylist applied to the canonical target | same pattern (canonicalize before the boundary test, both roots) | cite (design precedent) |
| chousa | `LOG.md:689-697`, `SCORECARD.md:961-986` | measured defect: "canonicalizes the glob's BASE but not each match" → outside symlink read | exactly C2's **K2-lexical-resolution** mutant shape | cite — K2's class is a proven recurring bug, not hypothetical |
| kasegi | `LOG.md:845,1123-1129`; `corpus/instruments/mirror-containment-check.py:1-24` | mirror containment: "rejects realpath escapes", 0/6 → 6/6 escape cases, 13-case matrix, base-vs-landed replay, fixture names confined, symlink targets must stay inside the case root | same **counter archetype** as C2 (escape cases + self-auditing controls + fail-before/pass-after), different surface | cite — counter-design precedent |
| kama | `LOG.md:146`; `corpus/lessons/round-2.md:46` | `symlinked-history containment` — a state dir refuses a symlinked root | same class (symlink as trust-boundary probe), different surface | cite in one line |
| mori | `LOG.md:85` | `/sys/fs/cgroup/../..` escape refused **shape-only** | same class (`..` inside a boundary test) | ignore (no shared surface) |
| kaidoku | `LOG.md:1102,1148` | "containment" = process/systemd/cgroup scoping | not path containment | ignore |
| souji | `LOG.md:1855` | child-env whitelist for a git subprocess | not path containment | ignore |
| fleet root (not a lane) | `MANIFEST.json` notes: kumitate "work-root containment", tsukuroi seat `Containment`, `mirror-containment-matrix` | dispatch bookkeeping for other lanes' seats | none | ignore |
| research/reports | `research/round-18-kimi-model-routing/battery-opencode/predictions/PREDICTIONS.md:94` "hit/miss by containment" | unrelated statistic | none | ignore |
| kimi-shokunin | `scripts/sources-census.sh:88,99,500-522` | `realpath` for repo-root/dir computation | no containment stance; no mako | ignore |

`parse_boolean` and `makoctl` occur in **no** sibling lane. `path_resolution(7)` occurs only in mado.

## 2. Merge package (`/home/vgpnk/Projects/shokuknow/merge/mado/`, read-only)

- Only mako-adjacent bytes: `SOURCES.append.md:42` (S238, the omarchy notification-silencing indicator) and
  `knowledge/corpus/knowledge/host-producer-outputs-r29.md:25,32` (quotes `if makoctl mode | grep -q 'do-not-disturb'`
  and "`makoctl mode` reports `default`"). No containment/realpath/symlink theme anywhere in the package.
- The package states "Nothing was written into the lane repo"; the lane holds **0** `S238` rows (`grep -c 'S238'
  corpus/SOURCES.md` → 0).
- **Verdict: assimilation does not apply this round.** S238 measures the DND *state* surface via `makoctl mode`; it
  is not a source for the criteria grammar (C1) or for containment (C2).
- One prose correction: the declaration's "Assimilation: none (no mako or containment theme in merge/mado/)" is
  imprecise — there *is* a mako-adjacent row (S238). The accurate sentence is "no mako **config-grammar** or
  containment theme; one mako-adjacent bar-producer row (S238), consistent with C1's host framing".

## 3. Cross-claim separability

**Verdict: SEPARABLE.** C1 can be measured at rev A without any C2 byte, and C2 at rev B without any C1 case byte.
Evidence, strongest first:

1. **C1 fixtures cannot leave `--home` — structurally.** `mako-cases-r88-v1` has one file map, `home_files`
   (`quality/counters/c1-r88-mako-fields.py:96-107`); `safe_relpath` rejects absolute paths and `..`/`.`/empty
   components (`c1-r87-mako-criteria.py:93-98`); `materialize` writes them *under* the case home
   (aliased from R87 at `c1-r88-mako-fields.py:67`, :211). C2 admits everything under `realpath(--home)`
   (`build/mado-mako.c2.py:446`). Therefore no C1 case can name an include that C2 would refuse — including the
   unwritten new cases, which the same loader must accept.
2. **C1's runner cannot escape either.** `c1-r88`'s `run_tool` passes only `--config <home>/…`, `--home <home>`,
   and the criteria args — never `--read-root` (`c1-r88-mako-fields.py:167-183`) — and runs with `cwd=home`
   (:182), so even the relative-include shape (reachable only through mutant M03) resolves inside `home`.
3. **C1's only carried include case is in-home.** Of the 22 frozen r87 cases, exactly one uses `include=`
   (`c13-include-globals-under-home`, `include=~/.config/mako/core.ini` with the file in `home_files`).
4. **C1's motivating host chain survives C2.** `~/.config/mako/config` is itself a symlink to
   `/home/vgpnk/.config/omarchy/current/theme/mako.ini`, and its only include is
   `~/.local/share/omarchy/default/mako/core.ini`; both realpath **inside `$HOME`** (measured, §0 row 7). The host
   case therefore resolves at B exactly as at A; the `--config` exemption (`c2.py:16-21`) is exercised by the host,
   not just by case k15.
5. **C2 needs no C1 byte.** All 17 containment cases use only `width=` (a base-tool global key) plus `read_roots`;
   a grep for criteria tokens returns only `"cases": [` and the three `read_roots` keys. No criteria section, no
   `--app-name/--urgency/--actionable/--expiring`.

**Shared bytes / shared surfaces (all checked, none breaks separability):**

| surface | evidence | effect |
|---|---|---|
| same tool file, different revisions | `TOOL_PATH = "tools/mado-mako.py"` in both counters; A then B | by design; the stacked-commit model is what makes C2's "before" = A meaningful |
| same function carries both claims' anchors | C1 M03 anchor `elif value.startswith("/"):` = `c2.py:415`; M04 `os.path.join(self.home, value[2:])` = `c2.py:414`; C2 K1 `c2.py:421`, K2 `c2.py:420`, K3 `c2.py:262`, K4 `c2.py:447`, K5 `c2.py:446` | every anchor occurs **exactly once** in the C2 candidate (counted); the C2 insert sits *after* M03/M04, so no anchor drift between A and B |
| same frozen r87 module, imported by sha | `R87_COUNTER_SHA256 = 4d801c30…` in both counters | one failure point, but pinned → loud, not silent |
| duplicated runner | r87 `run_tool` (`c1-r87:208-223`) vs C2's copy (`c2-counter:129-137`) | maintenance coupling only; current divergence is exactly the added `--read-root` |
| verdict rule rejects any rc≠0 | `c1-r87:229-231` | makes the base-tool control's figure a **mix** (see the risk note below) |

**Risk note for the L1 (not a proposal):** the C2 base-tool control appends `--read-root` unconditionally
(`c2-counter:131-133`), but the base tool has no such option — measured rc 2, `unrecognized arguments: --read-root`
(§0 row 4). So `base_tool_correct` (`c2-counter:173,192`) will mix six real "read the escape" failures with three
argparse failures (k07, k13, k14). The control is still strictly below K, so the predicate is unaffected; but the
single number invites the r86-class misreading ("the control figure is the containment signal"). After the freeze
(the run needs the mutants file at the measured rev, §6), print the per-case base reasons alongside the number.

## 4. Earlier mado rounds — reuse and contradictions

| pattern | evidence | stance's relation |
|---|---|---|
| "containment of symlinked includes" is the r87 named limit routed to r88 | `LOG.md:4297` | **lineage**: C2 is the answer to that limit; quote it in the claim |
| a frozen counter printed `TARGET_MET` on a symlink crib | `corpus/lessons/round-33-verifier-spotcheck.md:59-67`; `round-34.md:112-118` | **reuse**: C2 carries symlink cribs (k01 leaf, k02 dir, k12/k14/k16/k17) and a pre-data base control; K2 pins the lexical-resolution class |
| the mako config cell was the symlink's own size | `LOG.md:204` ("mako 50 B provenance resolved — the cell was the symlink's own size") | **reuse**: realpath before read; the host `--config` is a symlink, so the exemption must be realpath-based (`c2.py:655`) |
| `realpath` cannot canonicalize a missing path (an absent prefix was accepted) | `LOG.md:2699` | **reuse**: C2 realpaths declared roots (`c2.py:446-447`); the residual is that a *missing* `--read-root` becomes a lexical root (fail-closed, over-refusal only) — a limit, not an escape |
| instruments refuse a scratch path with a symlinked component | `LOG.md:3703` | **reuse**: the C2 counter materializes under `real_root = realpath(root)` and substitutes `@ROOT@` with the real root (`c2-counter:110-115`); convention held |
| path guards compare canonical forms of `{repo, lane root, dirname}` | `round-46.md:288` | **reuse**: C2 compares canonical roots, not raw strings |
| `link/.` bypassed a symlinked-dir check | `round-18-verifier-spotcheck.md:121` | **reuse**: deciding on `realpath` neutralizes trailing `/.`; no separate case needed |

**Contradiction (one, and it is textual):** the stance says an out-of-root include is "refused **before it is
stat'ed** or opened" (`claims-declaration-r88.md:79-80`; repeated at `build/mado-mako.c2.py:19-22`,
`quality/counters/c2-r88-include-containment.py:10-12`, `w1/draft-knowledge-mako-fields-containment-r88.md:85-87`).
It cannot be true: the containment decision is made on `os.path.realpath(target)` (`c2.py:420`) before the test at
`:421`, and resolution lstats/readlinks on the way. Measured for an out-of-root symlink: `newfstatat(link,
AT_SYMLINK_NOFOLLOW)`, `readlink(link)`, then `newfstatat(<outside target>, AT_SYMLINK_NOFOLLOW)`. So the outside
target's **metadata is touched before the refusal**; only the open is genuinely prevented (`self.load(real)` at
`:439` is after the check, and the tool's own `os.stat(real)` at `:426` is after it too).
The lane's own draft basis already says the opposite of the sentence — "`lstat` sees the link, `stat` sees the
target" (path_resolution(7) 169-178, quoted in the draft): resolution *is* the stat.

## 5. Proposed move (one, bounded, prose-only)

**M-1 — make the containment refusal sentence state what the code does, and name the resolution traversal as a
limit.** No predicate byte, case, mutant, control or score changes; C1's commit A is untouched because the sentence
exists only in the C2 header (the c1 candidate has no containment paragraph).

Replace "…otherwise it is refused before it is stat'ed or opened, and the resolved path is what is opened." with:

> …otherwise it is refused before it is opened — and before the tool's own `os.stat` — but not before it is
> resolved: the decision is made on the resolved path, so `os.path.realpath` lstats each component and readlinks
> each symlink first, and an out-of-root target's metadata is necessarily touched before the refusal. A refused
> include is never opened.

and add to the named-limits paragraph: "**Resolution touches metadata.** The refusal covers the open, not the
resolution traversal (measured: newfstatat on the link, readlink, newfstatat on the out-of-root target). chousa's
r19 sweep guard names the same limit — 'a refused unopened contract covers the match list, not the expansion
traversal' (`corpus/knowledge/sweep-symlink-r19.md:32-37`)."

Affected axes: **operability (C2)** — the claim's truth-conditions move from "falsifiable by a two-line strace" to
"named limit", which is how this lane already treats the hardlink/mount/TOCTOU class (`draft-knowledge:100-107`).
**Coverage (C1) — untouched**: no file read by C1's counter changes at A.

Synthesis behind it: C1 and C2 are one rule read in two directions — *refuse what the caller did not give you the
means to decide* (a criteria field with no supplied input; an include outside every declared root). The refusal is
of the **decision's use**, not of the path's existence; the current sentence mistakes the second for the first.

Risks: (a) four carriers quote the sentence — declaration, tool header, counter docstring, draft knowledge — and
must move in one commit or the claim and its knowledge entry disagree; (b) record it under `## Draft revisions`
(freeze pending), not as an erratum; (c) it changes the C2 tool sha and the c2 counter sha (both printed, neither
pinned), so the freeze's sha pins must be taken *after* the edit; (d) do not touch the c1 candidate — the sentence
is not in it.

Verification (each cheap, all read-only): (1) `rg -n "stat'ed or opened"` over the four carriers + `tools/` → 0
hits; (2) both counter selftests `--selftest` → `passed=12/12` / `passed=15/15`, rc 0; (3) `sha256sum` of
`containment-cases-r88.json`/`containment-mutants-r88.json` unchanged (`3ee0dc9b…`, `49373eee…`); (4) the candidate
tool's own `--selftest` at B → rc 0 (header text is not executed); (5) re-run the strace probe (§0 row 6) and read
the new sentence against the three syscalls.

## 6. Dead steps, installs, scratch

- **Dead step (rc 2, quoted):** the C2 counter against the base tool
  `MADO_MAKO_CONTAINMENT: SETUP_ERROR git show 24ba2a9ddac21c1211579231e6ee1d98963f9988:.ufo/waves/round-88/controls/containment-mutants-r88.json failed in .: fatal: path '.ufo/waves/round-88/controls/containment-mutants-r88.json' exists on disk, but not in '24ba2a9ddac21c1211579231e6ee1d98963f9988'`.
  Cause is freeze order, not a defect: the counter reads the mutant list from `--rev`, so the mutants file must be
  committed at or before the measured revision. After F it will be. The base control was therefore **not**
  measured by me; §3's risk note cites only the measured argparse fact, not a number.
- **Installs:** none (no pacman, no uv/npx/cargo). Nothing in `~/.local/bin` was created or modified.
- **Scratch:** `/fast/scratch/hyaku/mado-r88/R88MConnector/` (fixtures, traces, base-tool copy) is removed on exit;
  two early strays outside it (`/tmp/lanes.txt`, `/fast/scratch/hyaku/x.py`) were deleted during the run.
- **Not written:** `tools/`, `quality/`, `corpus/`, `PROVINCE.md`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, the
  declaration, `.ufo/state/`; the pre-existing working-tree state (`M quality/tool-ledger.md`, `M tools/mado-mako.py`,
  untracked round-88 files) is as I found it.
