# Omarchy drift watch — freshness arm 1 (M6-2, round 6)

Measured 2026-10-14 on this host, read-only. Every claim carries an anchor:
`path:line` or an inline command with its output. Raw probe transcript:
`/tmp/w6-mado-omarchy-drift/probes.log` (scratch, 44 lines); command-table
dumps `commands.json` (267 listed) and `commands_all.json` (282 with hidden)
sit beside it. Nothing was written outside this file; the omarchy skill and
the checkout were read only (`PROVINCE.md:10-11`; round-6 plan `:36-37`).

This note is watch arm 1 (freshness): the omarchy surface — the installed
skill, its upstream shape, and the release markers that identify the
installation — as a declared baseline vs live, in the gate's verdict
vocabulary (`HELD|MOVED` per pin; `MOVED` → `DIVERGED` naming the pin;
unavailable probe → `UNKNOWN`, never "clean").

## 0. Position in the round-6 move

- The round-6 plan (`:27-36`) defines this arm as (b), *gated on* (a) the
  mutation proof. At dispatch (a) is **not landed**: no
  `corpus/knowledge/gate-mutation-proof.md`, and the repo tree was clean then
  (`git -C mado-shokunin status --porcelain` → empty, my own repo; other
  lanes' and this note's files appeared after). So the
  gate landing is spec-only here (§6); the measurement itself is complete and
  the constants are paste-ready.
- Decision (recorded, §5): this watch ships as a **companion note + arm
  spec**, not as a gate edit from this lane.
- Gate reference state at dispatch: `tools/mado-verify.sh` sha256
  `d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13`,
  1098 lines, 6 plane ids (`gate`, `hypr`, `hypr-live`, `terms`, `walker`,
  `waybar` — census from `row <plane>` sites and the selftest awk regex
  `mado-verify.sh:352,356`). No `omarchy.*` row id exists yet (grep → 0).

## 1. What is actually installed

### 1.1 The skill is a symlink into the read-only checkout (structural)

`~/.agents/skills/omarchy` is **not a copy** — it is a symlink:

```
ls -la ~/.agents/skills/ →
  omarchy -> /home/vgpnk/.local/share/omarchy/default/omarchy-skill
```

created by the checkout's own installer, `install/config/omarchy-ai-skill.sh:2-6`:
`ln -sfn "$OMARCHY_PATH/default/omarchy-skill" ~/.agents/skills/omarchy` plus
three siblings — `~/.claude/skills/omarchy`, `~/.codex/skills/omarchy`,
`~/.pi/agent/skills/omarchy` — all four present, all pointing at the same
target (`readlink` each; link mtimes 2026-10-03 17:44:36.85x -0300).

Consequences for this arm:

- "Installed skill vs upstream content" drift is **structurally impossible
  while the link holds**: the two paths are one file. The sha equality
  `becd149e…` at both paths is definitional, not evidence of sync.
- The freshness surface is therefore (i) **link topology** (link intact /
  retargeted / replaced by a copy / dangling) and (ii) **checkout motion**
  (HEAD/tag/version content) — not a copy-vs-origin comparison.
- Prior phrasing was under-specified, not wrong: `terminals-and-omarchy.md:117-119`
  calls the skill "a single file `SKILL.md`"; true of the leaf, silent on the
  parent being a link into the checkout. Append-only precision item here; an
  erratum to MADO-3 is a *candidate*, not applied (write scope).
- Operator hazard worth naming: editing anything under
  `~/.agents/skills/omarchy/` edits the checkout, which the skill's own rule
  forbids (`SKILL.md:41`, `:49`); the watch row `omarchy.skill.vs_head` (§6)
  detects such an edit without ever running `git status`.

### 1.2 The dual pin, resolved by measurement

- `omarchy version` reads the repo file: `bin/omarchy-version:5` is
  `cat $OMARCHY_PATH/version` → `3.8.3`.
- The tag `v3.8.4` is **exactly at HEAD** (`describe --tags --exact-match` →
  `v3.8.4`; `tag --points-at HEAD` → `v3.8.4`), and `git show HEAD:version` is
  `3.8.3\n` — `diff` against the worktree file → `IDENTICAL`.
- So the disagreement is **upstream-internal** (release tag vs version-file
  content at that commit), not a dirty local state and not an install fault.
  Baseline relation to watch: *tag = version file + one minor release*
  (v3.8.4 ↔ 3.8.3). Cross-refs: `SKILL.md:20-24` (dual pin named),
  `SKILL.md:351` (decision row), MADO-R3-1 §8.4.

## 2. Baseline pins — re-anchored at dispatch (2026-10-14, read-only)

Draft-time pins (round-6 plan `:29-33`) re-measured **identically** — `omarchy
version` 3.8.3; `git describe` v3.8.4 (HEAD 8fcc9d60); SKILL.md 392 L /
14,908 B / `becd149e…`; mtime 2026-10-03 17:42; theme `Matte Black`. Extended
pin set for the arm:

| # | Pin | Value (anchor) |
|---|---|---|
| P1 | `omarchy version` | `3.8.3`, rc 0 (`bin/omarchy-version:5`) |
| P2 | `~/.local/share/omarchy/version` | `3.8.3\n`, 6 B, mtime 2026-10-03 17:42:36.9298; == `HEAD:version` blob |
| P3 | checkout git identity | tag `v3.8.4` at HEAD `8fcc9d6048af4cb0e3af8512c78049857a3b53dd` (short `8fcc9d60`), branch `master`, commit 2026-07-20T14:05:35-07:00 (`21:05:35Z`), 4,363 commits, 1,237 tracked files, 63 tags |
| P4 | skill leaf (via link) | 392 L / 14,908 B / sha256 `becd149e4d1c0767a80bcc1eb84e86e509149dc1e4b3d680cf24ab54bea5256d` / mtime 2026-10-03 17:42:32.303286116; == `HEAD:default/omarchy-skill/SKILL.md` blob; == checkout path (one file, §1.1) |
| P5 | link topology | `~/.agents/skills/omarchy` → `…/default/omarchy-skill`; 3 sibling links equal target; link mtime 17:44:36.85 |
| P6 | theme state | `omarchy theme current` → `Matte Black`, rc 0; `current/theme.name` = `matte-black` (12 B, mtime 17:49); `current/theme` is a real dir; `current/background` symlink → `theme/backgrounds/0-ship-at-sea.jpg` |
| P7 | checkout shape | top level 17 entries; counts bin 283, config 33, default 28, install 9, migrations 330, themes 19; newest migration `1784518937.sh` = 2026-07-20 03:42:17Z (≈17.4 h before HEAD); README 228 B ("…Linux distribution by DHH", omarchy.org) |
| P8 | command surface | `commands --json` 267 rows / 53 groups; `--json --all` 282 rows (15 `hidden=true`); `commands --check` → "Command metadata check passed (282 commands)" rc 0; all 11 groups the skill's table names (§4) present live |
| P9 | install-time cluster | checkout files written 17:42:32.2xx–17:42:36.93 on 2026-10-03; links 17:44:36.85; `~/.config/omarchy/hooks/`, `current/` 17:44–17:49 — one install sequence, no later upstream write observed |

Independent second sample of the "checkout, not dirty" property (index-free):
`bin/omarchy` worktree sha `2a5a2f06ce36…` == `git show HEAD:bin/omarchy` sha.

## 3. Drift classes for this watch

| Class | Watches | Probe | Verdict mapping |
|---|---|---|---|
| C1 release-marker relation | P1 vs P2 vs P3 components | `omarchy version`; version file bytes; `git describe/rev-parse` | any component ≠ baseline → MOVED → DIVERGED naming it |
| C2 checkout motion | HEAD, branch, tag, commit/tracked/tag counts, newest migration | git read verbs (no `status`, no `fetch`) | MOVED → DIVERGED; forces re-verification of all pins held at the old HEAD |
| C3 link topology | P5 intact / retarget / replaced-by-copy / dangling | `-L`, `readlink -f`, sha of resolved path | decoupled → MOVED → DIVERGED (copy with equal sha is still MOVED: freshness is no longer structural) |
| C4 skill content | P4 sha/mtime; worktree vs HEAD blob | `sha256sum`; `git show HEAD:… | sha256sum` | differs from baseline or from HEAD blob → MOVED (plain upstream edit vs local edit distinguished by the blob row) |
| C5 docs register | skill text vs live surface (§4) | route/table/path checks | NOTE-level (see D-1 in §6); new item → NOTE naming it |
| C6 surface shape | P7/P8 counters (counts, groups) | listings; `commands --json --all` | NOTE-level counters; *derived* skill-group check is PASS/FAIL |
| C7 probe availability | any verb missing/timeout/absent tool | rc capture with `timeout 5` | UNKNOWN (blocks CLEAN); never a silent pass |
| C8 install-time ordering | link/checkout/config mtimes | `stat` | NOTE only (evidence that links came from the installer) |

Design note: C1–C4 are the verdict-bearing pins (they are exactly the plan's
declared pin set plus the link/blob refinements); C5–C6,C8 are record-level
NOTEs, matching the gate's own "NOTEs never flip the verdict" discipline
(`mado-verify.sh:29-30`) and its existing treatment of `omarchy theme current`
reads as NOTEs (`mado-verify.sh:1015-1020`).

## 4. Skill-text vs live-surface register (docs drift)

Method: every `omarchy …` route form the skill's text/blocks name (40
candidates, `SKILL.md:91-99,105,114-124,149,159-161,172,203,212,240-241,254-258,270,274,312-315,320-325,334,337,340,345,348,359,382`) checked
against `commands_all.json` (route + aliases + `routes[]`). Result: 39/40
PRESENT.

- **R1 — stale route form (open).** `omarchy setup fingerprint` (`SKILL.md:123`)
  is not a live route: the live form is `omarchy setup security fingerprint`
  (registered; fallback route equal). No `bin/omarchy-setup-fingerprint`
  binary exists (`ls` → No such file), so direct-route resolution
  (`bin/omarchy:349-372`) cannot match, and prefix help only matches when the
  input *is a prefix of* a route (`bin/omarchy:1030-1034`) — it is not.
  `[INF]` from the command table + dispatcher code; the verb was **not
  executed** (§7). Candidate erratum for the skill lane (append-only; not
  applied — PROVINCE read-only).
- **R2 — hooks layout carried.** `SKILL.md:219-223` shows flat files
  `theme-set`/`font-set`/`post-update`; live `~/.config/omarchy/hooks/` holds
  five `*.d` dirs — `battery-low.d` (`play-warning-sound.sample`),
  `font-set.d` (`show-font-notification.sample`), `post-boot.d`
  (`weather.sample`), `post-update.d` (`install-voxtype.hook`,
  `show-update-notification.sample`), `theme-set.d`
  (`show-theme-notification.sample`). Re-measured; same finding as MADO-3 §7
  (`terminals-and-omarchy.md:138-146`).
- **R3 — method lesson (no drift).** `omarchy upload log` (`SKILL.md:337`) is
  **not** broken: the binary `bin/omarchy-upload-log` (4,103 B, `-rwxr-xr-x`)
  carries `omarchy:hidden=true` (`:3-5` of that file) so it is absent from the
  default listing but present in `--json --all` and resolvable by direct
  binary match. Lesson for the watch: **a bare `omarchy commands --json`
  under-reports; use `--all` or resolve by binary.** The first pass of this
  lane mis-read it as ABSENT before the `--all` check.
- Path claims re-checked live: four terminal configs (`SKILL.md:166-169`)
  exist with MADO-3 sizes (876/516/954/1325 B, mtimes 2026-10-03 19:02:29);
  checkout tree names (`SKILL.md:48-56`) all exist (§2 P7); stock theme
  `matte-black` present among 19 themes; `tokyo-night`/`catppuccin` also stock.

## 5. Arm vs note — the call, and why

**Companion note (this file) + paste-ready arm spec (§6); no gate edit from
this lane.** Reasons:

1. Write scope: this lane's assignment names exactly one output file
   (`omarchy-drift-watch.md`); the gate is another lane's single-writer
   artifact this round.
2. Ordering: round-6 plan `:46-47` gates (b) on (a). A gate edit now would
   collide with the in-flight mutation proof, whose evidence contract wants a
   frozen target sha (`MUTATE_RESTORE`); landing the arm *changes* that sha.
3. Plumbing: the arm's hermetic selftest needs the `$MUTANT` target fix the
   plan assigns to (a) — the landed selftest invokes the committed path
   `"$BASH_BIN" "$0"` (`mado-verify.sh:368,389,406,415`) and its helpers
   hard-code the six plane ids (`:352,356`). Landing rows before that fix
   would ship untestable code.
4. The note carries everything a landing needs (constants, rows, fixture
   sketch, open decision D-1), so landing is mechanical once (a) is green.

## 6. Paste-ready arm spec for `tools/mado-verify.sh` (plane `omarchy`)

Plane id `omarchy` (fits the `%-9s` plane column, `:1069`); row-id namespace
`omarchy.*` is free; gate census 6 → 7 plane ids. Constants payload (paste
verbatim; re-anchoring is an append-only erratum event here, never a silent
edit):

```
OMARCHY_VERSION_PIN="3.8.3"
OMARCHY_TAG_PIN="v3.8.4"
OMARCHY_HEAD_PIN="8fcc9d6048af4cb0e3af8512c78049857a3b53dd"
OMARCHY_SKILL_SHA_PIN="becd149e4d1c0767a80bcc1eb84e86e509149dc1e4b3d680cf24ab54bea5256d"
OMARCHY_SKILL_LINK_TARGET=".local/share/omarchy/default/omarchy-skill"
OMARCHY_THEME_PIN="Matte Black"
OMARCHY_SKILL_GROUPS="refresh restart toggle theme install launch capture reminder pkg setup update"
```

Rows (probe → status; `tmo` = the gate's 5 s timeout helper, `:99`):

| Row id | Probe (read-only) | HELD → PASS / MOVED → FAIL | Unavailable |
|---|---|---|---|
| `omarchy.version.cmd` | `tmo omarchy version` | `3.8.3` | omarchy off PATH → UNKNOWN (live) / SKIP under `--no-live` naming scope |
| `omarchy.version.file` | cat `$ROOT/.local/share/omarchy/version` | `3.8.3` | file missing → FAIL (install broken) |
| `omarchy.git.tag` | `git -C … describe --tags --exact-match` | `v3.8.4` | git/repo absent → UNKNOWN |
| `omarchy.git.head` | `git -C … rev-parse HEAD` | full sha pin | git/repo absent → UNKNOWN |
| `omarchy.skill.link` | `-L` + `readlink -f` == `$ROOT/.local/share/omarchy/default/omarchy-skill` | PASS; replaced-by-copy / dangling / retarget → FAIL (MOVED) | readlink absent → UNKNOWN |
| `omarchy.skill.sha` | `sha256sum` of resolved leaf | pin sha | unreadable (dangling) → FAIL; sha256sum absent → UNKNOWN |
| `omarchy.skill.vs_head` | `git show HEAD:<path> \| sha256sum` vs worktree | equal (index-free dirty check; verified 3/3 today: version, SKILL.md, bin/omarchy) | git absent → UNKNOWN |
| `omarchy.cmd.groups` | `omarchy commands --json --all` → the 11 skill groups ⊆ live groups | all present; missing → FAIL naming it | omarchy/python3 absent → UNKNOWN |
| `omarchy.cmd.surface` | `--all` row count vs 282 | NOTE (counter) | — |
| `omarchy.theme` | `tmo omarchy theme current` | NOTE printing `HELD|MOVED` vs `Matte Black` — see D-1 | UNKNOWN |
| `omarchy.doc.drifts` | R1/R2 checks (§4) | NOTE; new drift names itself | — |

Guards: all verbs are read-only (`version`, `theme current`, `commands --*`,
`git describe/rev-parse/show/log/ls-tree/rev-list/tag`, `stat`, `sha256sum`,
`readlink`). Never: `git status` on the checkout (audit §3.5,
`province-accuracy-selfaudit.md:110-128`: `git status --porcelain` refreshes
the index stat cache), `git fetch`, or any mutating verb (`theme set`, `bg
next`, `restart *`, `refresh *`, `install *`, `setup *`, `update`, `reinstall`,
`upload log`). Root-splitting: file/link/git rows use `$ROOT`; `omarchy
version` and `commands` are PATH/live probes and follow the gate's existing
live-skip semantics (`mado-verify.sh:587-591`) — under `--no-live` they read
SKIP with the scope named in the verdict, exactly like `live.plane`; when live
is requested and the verb is unavailable they read UNKNOWN and block CLEAN.

Selftest fixture sketch (hermetic; pattern = scenario C sandbox,
`mado-verify.sh:400-412`): build `$T/root/.local/share/omarchy/{version,
default/omarchy-skill/SKILL.md}` mattering only to the file rows; sandbox PATH
with stubs `omarchy` (prints `3.8.3`), `git` (answers `describe`, `rev-parse`,
`show` from a canned fixture map, so the git rows are exercised without a real
repository), `readlink`, `sha256sum`, and python3 when available. Scenarios:
(A) clean → file rows PASS and stubbed git/live rows PASS; zero FAIL, zero
UNKNOWN; (B) version file `3.8.4` → FAIL row naming MOVED + DIVERGED; (C)
stub `omarchy` removed with live requested → UNKNOWN row, verdict refuses
CLEAN; (D) link target replaced by a real dir with equal sha →
`omarchy.skill.link` FAIL (decoupled) while `omarchy.skill.sha` PASS —
explicitly refusing to let a copy masquerade as the live skill. Suite
invocation must target `$MUTANT` per round-6 plan `:17-18` — currently a gap
(`$0` runs, `:368`); M6-1 owns that fix and the helper-regex widening
(`:352,356`).

**D-1 (open decision, one-line switch).** Round-6 plan `:31-33` lists
`omarchy theme current` among the pins ("any MOVED reads DIVERGED"), but the
theme is operator-owned mutable state and the gate already treats `omarchy
theme current` as a NOTE (`:1015-1020`). This spec keeps it NOTE-level while
printing HELD/MOVED in the detail: otherwise a routine theme change turns the
freshness gate permanently red, which is a false alarm. If the integrator
prefers the plan's literal reading, the switch is `NOTE` → `FAIL` on that one
row; no other row changes.

## 7. Probes deliberately not run

`omarchy theme set/bg next`, `restart *`, `refresh *`, `install *`, `setup *`,
`update`, `reinstall`, `upload log` (network upload), `omarchy debug` (system
dump; only `debug --help` was read: usage `[--no-sudo] [--print]`), `git
status`/`fetch` on the checkout, and any write to any surface. No network was
used. (Note `omarchy update --help` was also not run; the skill's other named
routes were checked from the command table, not by execution.)

## 8. Observation / inference / unknown

**Observations** (all anchored above): the skill is a symlink into the
checkout (§1.1); the four pins re-measure identically to draft (§2); tag v3.8.4
sits exactly on HEAD whose version file reads 3.8.3 (§1.2); the skill's route
forms are 39/40 live (R1 the exception) and its hooks-layout claim is stale
(R2); `upload log` is hidden, not absent (R3); the checkout worktree matches
its HEAD blobs on three sampled files (index-free).

**Inferences** (not independently proven): the symlinks were made by the
installer (script + mtimes, C8 `[INF]`); the docs drifts are upstream
documentation lag rather than host faults (skill text ships from the same
checkout); the 2026-10-03 17:42–17:49 mtime cluster is one install+first-setup
sequence.

**Unknowns**: (1) tree-wide cleanliness of the checkout — not measured by
constraint (no `git status`); only sampled rows cover it; (2) whether upstream
*intends* the tag/version-file gap — the watch pins the observed relation, not
the policy; (3) status of (a) and whether the arm lands this round — integrator
decision, spec is complete; (4) `omarchy setup fingerprint`'s failure text not
observed live (code-path `[INF]` only, execution deliberately avoided); (5)
whether the hidden `upload log` default arg (`install`) matches the skill's
usage intent; (6) post-update hook activation intent (operator-owned, out of
this arm).

## Errata (append-only)

- (none yet)

Re-anchor protocol: a MOVED pin is reported first, never smoothed. Changing
the baseline (constants in §6, table in §2) requires an appended erratum
naming old→new values, the reason, and the re-measure command — the baseline
is never edited to match reality.
