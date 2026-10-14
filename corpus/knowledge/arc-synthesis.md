# Arc synthesis — mado's ten rounds, re-derivable (M10-1, round 10)

source: this repo's committed artifacts — the arc commits `74d3b7b`…`de22dfd`,
`tools/mado-verify.sh`, `corpus/knowledge/*.md` (19 notes), the round record
drafts under `plans/`, `reports/*.md`, `LOG.md`, `SCORECARD.md`, `SKILL.md` —
every number below names the command or record line that carries it
verified-at: 2026-10-14, round-10 write window (local 17:50–17:57 −03:00); the
gate ladder and all gate runs against commit `de22dfd` (HEAD at write)
recheck: `git show <commit>:tools/mado-verify.sh | sha256sum` + `wc -lc` for
the ladder; `bash tools/mado-verify.sh --selftest` (268/268 at `93e43f8f…`);
the per-claim commands inline; the census commands in §0
self-label: **M10-1** — the arc synthesis (round-10 plan §(a)); this file is
the lane's only write

Lane M10-1, round 10 (fleet training r9), wave width 32. Scratch
`/tmp/w10-m10-1/` (`hist/*.sh` + `*.selftest.log`, `selftest.log`,
`nolive.log`, `live.log`, `regression.log`, `spec.txt`, `spec.raw`, `mut-r5*`,
`gate-sha-*.txt`). Tags: **[OBS]** measured by this lane at the time named;
**[OBS-record]** cited from a round record (source named, never re-measured
here); **[INF]** inference; **[UNK]** unknown. The tenth round's own landing is
resolved at the commit, never self-declared here. The substrate was
read-only throughout (file reads, `wc`/`sha256sum`/`grep`, hyprctl read verbs,
`pgrep`/`stat`/`busctl`, the gate's own modes, the tameshi harness consumed
read-only); no compositor/session mutation; no socket connected; no secret
content read; no `git status`/`fetch` on the omarchy checkout.

## 0. Re-derivation protocol (one screen — every claim below re-derives from these)

```bash
cd mado-shokunin
git log --reverse --format='%h %ad %s' --date=format:'%H:%M:%S'   # §1 commits
for c in eead56b c8f6667 0c20a76 12c8f08 de22dfd; do             # §2 ladder
  git show $c:tools/mado-verify.sh >/tmp/hist-$c.sh; sha256sum /tmp/hist-$c.sh
  wc -lc </tmp/hist-$c.sh; bash /tmp/hist-$c.sh --selftest | tail -1; done
bash tools/mado-verify.sh --selftest; bash tools/mado-verify.sh --no-live
bash tools/mado-verify.sh; bash tools/mado-verify.sh --regression   # §2
grep -cE '^[[:space:]]*row [a-z-]+ ' tools/mado-verify.sh          # §3 census
grep -oE '^[[:space:]]*(row|row_from_rc) [a-z-]+ [a-z0-9._-]+' \
  tools/mado-verify.sh | awk '{print $NF}' | sort -u | wc -l        # 55 ids
grep -oE 'st_row_(has|detail) "\$[a-z_0-9]+" [a-z0-9._-]+' \
  tools/mado-verify.sh | awk '{print $NF}' | sort -u | wc -l        # 32 of 55
```

Ladder re-run [OBS, this lane, `/tmp/w10-m10-1/`]: every revision below still
runs its own `--selftest` faithfully at dispatch — no toolchain/fixture drift
was found, so no ladder row needs the [OBS-record] tag.

## 1. The arc ledger — mint + rounds 1–10

One row per round; sizes are the records' landing values (`wc -l`; notes
without a trailing newline show editor view +1 — the round-1 convention); the
commits are `git log --reverse` [OBS].

| # | commit | axis move | landed (measured, records) | gate sha256 | selftest | seats as the records name them |
|---|---|---|---|---|---|---|
| 0 | `74d3b7b` | mint | `MINT.md` (demand evidence + roster scan); probation ≥3 rounds | — | — | — |
| 1 | `65a2254` | coverage | 3 survey notes — `hyprland-config-plane.md` 217 L, `waybar-walker-plane.md` 364 L, `terminals-and-omarchy.md` 179 L; SKILL 22→186 L; admitted 3× ADMIT | — | — | audits re-verified anchors/counts |
| 2 | `e1e1bb7` | depth | `hyprctl-verification-layer.md` 280 L (56 `getoption` + 9 non-getoption pairs, 0 mismatch); `keybind-rule-semantics.md` 315 L (192/192 binds, 24 dispatchers); R2-E errata; SKILL →240 L | — | — | MADO-SCR (scribe re-verification) |
| 3 | `f9f58c0` | depth + coverage | `waybar-walker-semantics.md` 455 L; `config-health-report-r3.md` 550 L (F1–F10); `executor-test-sufficiency.md` 196 L; SKILL 240→396 L, sha `ef4c29e3…` frozen | — | — | MADO-R3-4 executor; MADO-B4 re-verification |
| 4 | `3d9ba45` | depth + calibration | `idle-lock-plane.md` 355 L; ERR-M errata append (R3-2 §0 6×→7× S3, F8 `wlSocket`→`wl_socket`, E2/E3); reproduction package | — | — | VER-M3, VER-M4 (record also names AUD-M1, ERR-M) |
| 5 | `eead56b` + `c03c249` | operability + calibration | first gate `tools/mado-verify.sh` v1 (1,098 L, 28/28, live CLEAN 35 pass/4 notes); `walker-deep.md` 617 L; box 4 closed by VER-M4B → PROBATION 4/4 | `d7edaab4…` | 28/28 | VER-M4B |
| 6 | `c8f6667` | operability | gate **proven to fail, then hardened** (28→53; 10/10 kills); `gate-mutation-proof.md` 167 L; `omarchy-drift-watch.md` 287 L; `remaining-planes-census.md` 333 L | `c4c1afb7…` | 53/53 | VER-M6 | AUD-M6 |
| 7 | `0c20a76` | operability + coverage | `--regression` mode (53→89); `theme-wallpaper-plane.md` 394 L; `walker-live-surface.md` 300 L; `reports/r7-aud-m7.md` (AUD-M7) | `90d50cdd…` | 89/89 | VER-M7 | AUD-M7 |
| 8 | `12c8f08` | operability + freshness | plane 7 `omarchy` (11 rows, OM1–OM8); `--snapshot` / `--snapshot-diff` (S1–S10); post-hardening sweep 10/10; selftest 89→217 | `7da4ec50…` | 217/217 | VER-M8 | AUD-M8 |
| 9 | `de22dfd` | coverage + operability | `theme` plane **file rows** (10; T1–T9); helper regex 7→8; 217→268; `walker-deep-r9.md` 398 L; `snapshot-diff-receipt-r9.md` 196 L; **not landed**: the two live theme rows (exempted by name), the walker live-surface rows, `walker-deep.md` §10/§11 | `93e43f8f…` | 268/268 | VER-M9 | AUD-M9 |
| 10 | (this round) | calibration + operability | this synthesis + the standing-use note (M10-2) + the record family closure (plan §(b)/(c)); no gate edit is this round's claim | — | — | in flight |

Seat artifacts in-repo [OBS, `ls reports/`]: `r7-aud-m7.md`, `r8-aud-m8.md`,
`r8-ver-m8.md`, `r9-aud-m9.md`, `r9-ver-m9.md`; the VER-M3/VER-M4/VER-M4B/
VER-M6/VER-M7 verdicts live in the records (SHONEN evidence lines, LOG) and
their scratch files are ephemeral — the records carry the load-bearing
hashes. `LOG.md:294-300`
carries the one-line round entries; `SHONEN.md` is 4/4 `[x]` byte-identical
since `c03c249` (`edace65e13c8ad20…`). AUD-M1's verdict is recorded in
`idle-lock-plane.md:379`; ERR-M is the round-4 errata lane (its blocks are the
`Errata (round 4)` sections across the notes).

### 1.1 The corpus as it stands (19 notes, `wc -l` + sha256 prefix, HEAD [OBS])

| note | L | sha16 | README row |
|---|---|---|---|
| `hyprland-config-plane.md` | 267 | `a46e2a5042490c51` | r1 |
| `waybar-walker-plane.md` | 474 | `c5d7a3ebff9e68ac` | r1 |
| `terminals-and-omarchy.md` | 204 | `ac8c94ad6fd623e8` | r1 |
| `hyprctl-verification-layer.md` | 302 | `bf5707a6dd42ffad` | r2 |
| `keybind-rule-semantics.md` | 315 | `eb3cbe3b96c608cf` | r2 |
| `waybar-walker-semantics.md` | 462 | `b92bee2cc69c95b9` | r3 |
| `config-health-report-r3.md` | 1005 | `acf59f9b06c63cec` | r3 |
| `executor-test-sufficiency.md` | 196 | `4c34f8848b7f95c9` | r3 |
| `idle-lock-plane.md` | 381 | `a0597be96c107799` | — (r4) |
| `province-accuracy-selfaudit.md` | 345 | `7c0a58208dea60e8` | — (r4/r5) |
| `walker-deep.md` | 617 | `0982ba066c72575a` | — (r5) |
| `gate-mutation-proof.md` | 167 | `716836ca1bf3484a` | — (r6) |
| `omarchy-drift-watch.md` | 287 | `49f5a9a14776d83d` | — (r6) |
| `remaining-planes-census.md` | 333 | `710e3e289643f2ff` | — (r6) |
| `theme-wallpaper-plane.md` | 394 | `8c578cc70e36506d` | — (r7) |
| `walker-live-surface.md` | 300 | `2bbb9609283f2d81` | — (r7) |
| `gate-mutation-sweep-r8.md` | 178 | `9d6435f5cdd52561` | — (r8) |
| `walker-deep-r9.md` | 398 | `a5acfe0162c9e5cd` | — (r9) |
| `snapshot-diff-receipt-r9.md` | 196 | `73b1466b6f876924` | — (r9) |

Notes that grew after landing did so by append-only errata (e.g.
`config-health-report-r3.md` 550 L at landing → 1005 L now, `Errata (round 4)`
block at `:553`; `hyprland-config-plane.md` 217 → 267 L; `idle-lock-plane.md`
355 → 381 L). Counts name their command: `wc -l corpus/knowledge/*.md`,
`sha256sum`; the landing values live in the records (`LOG.md:294-300`,
`SCORECARD.md`).

### 1.2 Record-debt movement across the arc [OBS]

| ledger | state at write | evidence |
|---|---|---|
| `corpus/README.md` | 19 L / `2dd274f5e270e65b…`, **8 rows / 11 notes unrowed** (r4 ×2, r5 ×1, r6 ×3, r7 ×2, r8 ×1, r9 ×2) | `grep -cE '^\| .knowledge'`; the file is byte-identical since round 3 | 
| `SCORECARD.md` | 21 L / `17fe5a4270698b08…`; rows 1–3 full, **rows 4–9 one-line stubs** | `sed -n '16,21p'` |
| `LOG.md` | 300 L / `b6b5a4b226722421…`; rounds 4–9 one-line entries (round 7 carries the fuller M7-1 paragraph at `:297`) | `wc -l`; `sed -n '294,300p'` |
| record drafts | ⟨PENDING⟩ never filled: r7 **13**, r8 **19**, r9 **19** (`grep -c PENDING`); committed as-is | `plans/round-{7,8,9}-record-draft.md` |
| `corpus/lessons/` | **0 entries — ten rounds** of the round-1 promise | `ls corpus/lessons/ | wc -l` |
| `walker-deep.md` | §10/§11 errata owed since r7; sha unchanged `0982ba066c72575a…`; the candidate text sits in `walker-deep-r9.md` §8 | `sha256sum`; r7/r9 records |

## 2. The gate's evolution — 28 → 53 → 89 → 217 → 268, mutation-hardened, regression mode

### 2.1 The ladder (re-derived from git blobs [OBS]; selftest re-run per revision [OBS])

| arc commit | round | gate sha256 (prefix) | lines | bytes | `--selftest` re-run | `PIN_MADO` |
|---|---|---|---|---|---|---|
| — | r1–r4 | (no gate; the round-1 "committed verdict gate" ceiling stood through round 4) | — | — | — | — |
| `eead56b` | r5 | `d7edaab4bf108625` | 1,098 | 45,334 | **28/28** | (absent) |
| `c8f6667` | r6 | `c4c1afb75dd1c8aa` | 1,186 | 50,126 | **53/53** | (absent) |
| `0c20a76` | r7 | `90d50cdd4d18410b` | 1,755 | 75,771 | **89/89** | `c4c1afb7…a5171` |
| `12c8f08` | r8 | `7da4ec5013583c91` | 2,887 | 131,612 | **217/217** | `d2bcdb31…db62` |
| `de22dfd` | r9 | `93e43f8fe8b9bdd4` | 3,231 | 150,103 | **268/268** | `dc7c4141…f8fd` |

`c03c249` (the SHONEN commit between r5 and r6) carries the identical r5 gate
blob. Every revision still runs its own suite faithfully — the historical
`--selftest` counts above are this lane's re-runs, not recitations.
`VERSION_STR` reads `mado-verify.sh v1 (mado-shokunin round 5 / M5-2)` at
**every** revision including the landed one (`grep -oE 'VERSION_STR="…"'`) —
the named residual below.

### 2.2 The landed revision's whole row re-run [OBS, `/tmp/w10-m10-1/`, sha before = after]

```
MADO_SELFTEST: 268/268 assertions passed                       rc 0
--no-live: CLEAN (29 pass, 4 notes)  counts: pass=29 fail=0 unknown=0 skip=8 note=4
live:      CLEAN (52 pass, 8 notes)  counts: pass=52 fail=0 unknown=0 skip=0 note=8
           boundary.readonly PASS, combined sha bb2639d9a980…
MADO_REGRESSION: PASS (case=mado-verify-hardened; target=dc7c4141…f8fd)  rc 0
REGRESSION_TABLE … match=10/10 recorded-killed=10 measured-killed=10
  survived=0 inconclusive=0 flips=0 · REGRESSION_CASE PASS (control=green restore=ok)
REGRESSION_SPEC sha256=c7ee75b9…1dd8 (recorded pin matches)
REGRESSION_HARNESS cf41efaa…242c75 (recorded b56c6e57… — provenance, not gated)
```

### 2.3 The kill ladder and the pin lineage

- The recorded defect spec is **re-derived here** from the gate's own heredoc
  (`mado_r7_spec_write`, `:1322-1372`): 10 `@defect` entries, 2,141 B, sha256
  `c7ee75b97c38ac8f…1dd8` — byte-equal to the pin [OBS].
- Rate path for the same spec: round-5 revision `d7edaab4` **4/10 (40 %)**
  [OBS-record: `gate-mutation-proof.md` §1; **re-derived by this lane**:
  killed=4 survived=6 inconclusive=0, control GREEN, `MUTATE_RESTORE: OK`,
  `/tmp/w10-m10-1/mut-r5.log`] → hardened `c4c1afb7` **10/10** [OBS-record,
  same note] → live `90d50cdd` **10/10** [OBS-record:
  `gate-mutation-sweep-r8.md` §1] → landed `93e43f8f` replayed by the gate's
  own `--regression` against the derived target **10/10 flips=0** [OBS,
  §2.2].
- Pin lineage: `c4c1afb7…a5171` (r7, one-family excision) →
  `d2bcdb31…db62` (r8, three-family excision) → `dc7c4141…f8fd` (r9). The
  three excised marker families: `MADO-R7-SELFTEST-BLOCK`,
  `MADO-R7-REGRESSION-BLOCK`, `MADO-R8-BLOCK`; the derived target = the file
  minus the families, and a widening outside every pair re-cuts the pin
  (`REGRESSION_RECUT`) instead of passing stale.
- Mutation discipline carried by the records: (r6 rule 1) an exit-only kill
  criterion is blind to the exit-flatten family; (r6 rule 2) a surviving
  mutant says "no test notices this clause", and nothing ships wider without
  a covering mutant; (r6 rule 3) mutation-test the copy
  (`--suite 'bash "$MUTANT" --selftest'`); (r7 rule 1) from r7 **every
  gate-widening claim carries `MADO_REGRESSION: PASS`** at the widened
  revision; (r7) the pin is never edited to match reality, a MOVED anchor is
  reported first; (r7, carried in r8's audit) the `killed-delta<=1` slack is
  deliberately not applied.
- The r9 owe, named: the recorded spec did **not** move with round 9 (10
  defects, same sha) — the ten landed theme clauses have **no recorded
  mutant of their own**; their kill vehicles so far are the T1–T9 selftest
  scenarios. The gate's own re-cut record says it plainly and AUD-M9 filed
  it (C4) — recorded, not smoothed [OBS-record + `grep`].

### 2.4 Modes and vocabulary at the landed revision

| mode | contract | established |
|---|---|---|
| (default) | live read-only run vs `$HOME` (or `MADO_VERIFY_ROOT`); verdict `MADO_VERIFY: CLEAN|DIVERGED`, exit 0/1 (usage 2) | r5 |
| `--no-live` | file plane only; verdict names the skipped live layer | r5 |
| `--root DIR` | verify DIR as the config root (the selftest's seam) | r5 |
| `--selftest` | hermetic fixture assertions under `/tmp/w5-mado-m52-*`; a failure exits 2 | r5 |
| `--regression [--keep]` | replays the recorded T6-1 case at the derived target; `MADO_REGRESSION: PASS|FAIL|SETUP`; refusals for `--target/--defects/--suite/--label/--workdir/--timeout/--tail` and the verify flags; env `MADO_VERIFY_HARNESS` | r7 |
| `--snapshot FILE` | runs the gate and writes a v1 receipt (`# mado-verify snapshot v1`, `created=`, `tool=`, `gate-sha256=`, `root=`, `scope=`); never overwrites (`MADO_SNAPSHOT: REFUSED`, rc 2) | r8 |
| `--snapshot-diff OLD NEW` | class-by-class receipt diff; `MADO_DIFF: SAME|DETAIL-CHANGED|CHANGED|SETUP` (exit 0/0/1/2); never prints `MADO_VERIFY:` | r8 |
| `--help` | base help lists the five original flags; each mode's paragraph is appended by that mode's `--help` (measured: `--regression/--snapshot/--snapshot-diff --help` each rc 0 and append) — base-help discoverability stays a named residual | r7/r8 |

Row classes PASS/FAIL/UNKNOWN/SKIP/NOTE; UNKNOWN blocks CLEAN, NOTE never flips
the verdict; a stubbed scenario proves row logic, never live values; a missing
tree fails closed.

### 2.5 Census at the landed revision [OBS, counting commands in §0]

`row` sites **189** + `row_from_rc` **6** = 195 (the helper definition at
`:116` excluded);
per-plane sites theme 27 / omarchy 56 / hypr-live 51 (+6 rc) / hypr 23 /
waybar 17 / terms 10 / gate 3 / walker 2; **distinct ids 55**; helper plane
regexes **8 ids** at seven sites (`:387`, `:391`, `:406-410`); **asserted row
ids 32 of 55**. Emitted at run time: no-live **41 rows** (29+4+8), live **60
rows** (52+8) — the theme plane emits 10 ids (4 literal sites + 6
helper-driven). Round-8 base for the same commands: 162 sites, 51 ids, 7
plane ids, 22 asserted.

## 3. The config plane as measured (what exists, verified how)

Domain measured, no verdict token of its own here — the gate's vocabulary
belongs to `tools/mado-verify.sh`. Values re-run read-only by this lane in the
round-10 window are [OBS]; the rest are [OBS-record], cited with the round
that measured them.

| surface | what exists (measured) | verified how | license boundary |
|---|---|---|---|
| hypr core | `~/.config/hypr/`: 12 active `*.conf` (13 entries incl. the dead backup); `hyprland.conf` 29 L pure orchestrator, **17** `source` statements, include order = precedence; 192 binds across 5 files; sha256 `4f52854a3c143dcf…` (= MADO-1 §2 pin, unchanged since round 1) | file bytes + `hyprctl` read verbs; `grep -cE '^source'` → 17; `hyprctl -j binds | jq length` → 192 | declarations vs effective value stay separate; file bytes never prove live state alone |
| hypr-live | `configerrors` empty rc 0; `general:gaps_out` `{"custom":"0 0 0 0","set":true}` (toggle-owned); `input:kb_layout` br; 57/57 `getoption` re-measure 0 mismatch (r3); DP-1 3440x1440@~100 | `hyprctl` live reads (r2 layer: 56 `getoption` + 9 non-getoption pairs; classes agreement/agreement*/live-default/mismatch/config-only) | dispatcher *behaviour* and per-window rule effects have no read verb → `[INF-docs]`/[UNK] |
| waybar | `config.jsonc` JSONC-parses, `reload_style_on_change: true`; bar top height 26; 19 modules; style imports the theme css; layer surface `waybar` + live tray watcher | file bytes + `hyprctl -j layers` + `busctl` tray property (r3); no IPC/query verb in waybar 0.15.0 → **module text stays UNKNOWN** (anti-claim branch, labelled) | introspection-capability ledger: `waybar(5)` documents defaults, never the live module text |
| walker | `config.toml` parses; version `2.17.0`; `app-walker@autostart.service` + `elephant.service` active; theme package `omarchy-default`; sockets `srwxr-xr-x` 0 B under `$XDG_RUNTIME_DIR`; `dev.benz.walker` D-Bus owner == walker pid; binary identity sha256 `64826a85…`, BuildID `a22452d1…` (r9) | consumer probes: `walker --version`, `pgrep -ax`, `stat` (never connect), `busctl --user list`; live surface note §4/§5 | socket protocol / rendered UI UNKNOWN by constraint; no reload path — restart is the apply path (r9) |
| terms | alacritty only installed of alacritty/foot/kitty/ghostty (`command -v`); font 12.5 + padding 14 uniform across the four declared configs; alacritty.toml imports the theme | file bytes + install-state sweep (r1/r3) | uninstalled terminals' configs are declarations only |
| theme | `theme.name` = `matte-black` (12 B); include/import chain resolves: `hyprland.conf:13`, `hyprlock.conf:1`, `waybar/style.css:1`, `alacritty.toml:1`, mako config symlink, walker css, swayosd css; `current/background` → `…/backgrounds/0-ship-at-sea.jpg`; 24 generated files + 4 backgrounds (r6 census) | file bytes + symlink resolution + the landed gate rows (9 PASS + 1 NOTE live) | the theme *choice* is operator-owned (NOTE always); the two note live rows (`wallpaper.live`, `display_agree`) are not landed |
| omarchy | `omarchy version` 3.8.3; version file 3.8.3 (== `HEAD:version`); tag `v3.8.4` exactly at HEAD `8fcc9d60…`; skill leaf sha `becd149e…` (392 L) == `HEAD:default/omarchy-skill/SKILL.md`; 282 commands in `--json --all` [OBS-record r8] | read-only verbs + `git describe/rev-parse/show`; **never** `git status`/`fetch`; dual pin resolved as a baseline relation (r6) | tree-wide cleanliness stays unmeasured by constraint (no `git status`) |
| idle/lock | hypridle/hyprlock/hyprsunset **absent** in the current session; autostart route demonstrably launches hypridle in a fresh session (r4 turnover); 150 s/152 s declared chain has no consumer while absent | `pgrep -x` (this lane) + the r3/r4 records | idle transitions UNKNOWN by constraint; stop-cause `[UNK]` (F1/S1, operator) |
| mako/swayosd | mako owns `org.freedesktop.Notifications`; DND via `makoctl mode` → `default`; swayosd present; mako config is a symlink into the theme | consumer probes (busctl, makoctl) | notification payloads never read |

Evidence classes (the routing lives in `SKILL.md:111-139`; the notes cited are
the licensing anchors): **file bytes** — what a file declares, include order,
orphans, substrate identity; **hyprctl live read** — effective value + owner,
parsed bind surface, layers, load health; **docs-inference** (`[INF-docs]`)
— procedure/grammar, never host state; **consumer-side probe** — runtime facts
another consumer owns; **gate rows** — the landed verdict instrument over the
first four. Divergence vocabulary: `agreement`/`agreement*`/`live-default`/
`mismatch`/`config-only` (r2), severity S1–S3 (r3 register F1–F10: 1×S1,
2×S2, 7×S3 — the r3 summary's "6×" corrected by ERR-M E2 in r4).

## 4. The boundaries held (and the rounds that measured them)

- **Read-only substrate** — every round: byte-identity proofs over the config
  trees (r2 §7; r3 §10 boundary proofs; r4 VER-M4 22/22 pins); from r5 the
  gate's own `boundary.readonly` row prints the combined hash
  `bb2639d9a980…` in every run — identical in every verdict run of this
  synthesis [OBS] and in every record through r9.
- **No compositor/session mutation** — no launcher open, no socket connect,
  no `omarchy theme set`, no `restart *`: held every round and re-stated in
  every anti-claim; the r9 walker rows would have been the first socket read
  and they did not land (the sockets were `stat`'d, never connected).
- **Scratch-only, single-writer** — the gate is edited by one lane per round
  (r5 M5-2, r6 M6-1, r7 M7-1, r8 M8-1/M8-2/M8-3, r9 M9-1); every edit
  carries the lane identity + a LOG entry; scratch `/tmp/w5-mado-m52-*` (gate
  fixtures), `/tmp/mado-verify-regression.*` (re-cut), `/tmp/w<N>-<lane>-*`
  (lanes); fixtures are removed by exact path, foreign dirs left alone.
- **Secrets shape-only** — no secret content read; r4 VER-M4 measured 0
  key-shaped hits; session material (clients) length/tags only.
- **Sibling repos read-only** — `tameshi-shokunin/tools/mutate-and-run.sh`
  consumed read-only by the gate's own mode and by sweeps; the exit-flatten
  family stays a recommendation to tameshi, never a patch; the omarchy
  checkout is read via `git show/describe/rev-parse` only.
- **No `git status`/`fetch` on the omarchy checkout** — one disclosed
  deviation in the r8 draft (index mtime provably predates the probe), none
  in r9 (recorded), none in this round's window.
- **Snapshots and receipts stay in scratch** — never committed; the r9
  receipt pair is the mode's first real use and lives in `/tmp` (the record
  quotes its lines because scratch does not survive).
- **No new frontier in the final round** — surfaces never covered are named
  as gaps (§6), not promised; promotion is never self-declared.

## 5. The three trends over the arc (LEARNING.md:23-35)

| trend | verdict | evidence |
|---|---|---|
| **expansion** | **improved** | 0 → 19 admitted notes (`ls corpus/knowledge/ | wc -l`); new kinds of source entered with citation: live read verbs (r2), consumer probes + RUN producers (r3), the mutation harness (r6), hermetic stubs (r8), snapshot receipts (r8/r9); each round's admission carries its coverage-map row or the round record's deliverables line |
| **quality** | **improved** | stale numbers were corrected by **appended** errata, never rewrites: mako 50→119 B, orphan `envs.conf`, R3-2 §0 6×→7×, F8 `wlSocket`→`wl_socket`, the 313→315 count; r2–r9 re-measured prior notes (57/57 `getoption`, 192 binds, pins) with 0 mismatch; the r3 executor test froze the SKILL sha; no admitted entry is known false and left unmarked |
| **discernment** | **unprovable-but-better** (the arc's own recorded harm-side fact) | `corpus/lessons/` is **0 entries after ten rounds** — no round ever recorded a non-author spot-check of its gate decisions (LEARNING.md:38-43), so the outside check that would make discernment a verdict was never taken up; `QUALITY.md` is unchanged since mint (8 L, `1923c94f49788ade…`), so no criterion was added with a lesson behind it — but also none without one. The named remainder: round 10 charters `corpus/lessons/round-10.md` or records the refusal — that resolution is not this note's to self-declare |

Trades named as trades (not admitted as improvements): the arc's operability
growth rests on one host and one toolchain (bash 5.3.15, single measurement
window per round); the hypr-live live body is exercised from the substrate,
never from a stub (round-6 open item, still open).

## 6. The gap ledger — surfaces the arc never made verdict-bearing

Each with why it stays unknown [OBS-record unless noted]:

| surface | why it stays unknown |
|---|---|
| rendered UI / screenshots | no landing site in the gate; grim read to stdout was a one-off probe (r1/r2), never a verdict input |
| walker socket protocol | never connected (constraint); the r9 note measured shape only — protocol semantics UNKNOWN |
| idle/lock transitions | no read surface; hypridle absent; idle-lock plane note keeps them UNKNOWN by constraint (r4) |
| dispatcher behaviour | no keystroke injection allowed — `[INF-docs]` only (r2, 24 dispatchers) |
| window-rule effects / exec-once results | no rule-read verb in Hyprland 0.56 (r2/R3-2) |
| waybar module text | no IPC/query verb in waybar 0.15.0 (r3 anti-claim branch) |
| env vars (orphan NVIDIA trio) | no query surface for the compositor's env; `printenv` covers the session's own (r2/F3) |
| hypridle/hyprsunset stop-cause | journal proves boot start; stop time/cause `[UNK]` (r3 F1, r4 turnover) |
| tree-wide omarchy cleanliness | `git status` on the checkout is forbidden; only `git show`-style reads are licensed (r6) |
| battery / power-supply | no device on this host (r3) |
| exit-flatten mutant family | harness-side boundary: KILLED is judged by exit only (r6, recommendation to tameshi) |
| theme live rows / walker live rows | not landed: hermetic barrier is structural (`--root` roots `$HOME`; `$XDG_RUNTIME_DIR` and the session bus sit outside); exempted by name (r9) |

## 7. Classification — every open item named, counts per class

Classes: **closed** (evidence exists) · **operator-owned** (a decision is the
operator's or the owning lane's; named) · **unknown** (no read surface or by
constraint; named). No item is left as "carried".

**Closed (9):**
1. mint-shape SHONEN defect — regenerated `f9f58c0` (canonical seed, 4/4 boxes now `[x]`).
2. SKILL stale "313" count — fixed to 315 in r3.
3. mako 50→119 B cell — R2-E1 applied r2.
4. orphan `envs.conf` omission — applied r2.
5. R3-2 §0 6×→7× S3 off-by-one — ERR-M E2 applied r4.
6. F8 `wlSocket`→`wl_socket` — ERR-M E3 applied r4.
7. SKILL `arrouillard` typo candidate — does not reproduce; withdrawn in r7.
8. r5 gate's 6 surviving mutants — killed by the r6 hardening (10/10).
9. r8 spec-refusal (9 non-unique anchors) — re-cut spec `85d946d7…6b01` shipped r8; the pin alarms during the r8/r9 re-cuts resolved at the landed revisions.

**Operator-owned (8):**
1. promotion / roster — operator decision, never self-declared (`SHONEN.md` 4/4, `PROVINCE.md`).
2. F1 hypridle absence (S1) — operator decision with the record's remedies.
3. F2 Alacritty opacity anomaly (S2) — operator.
4. F3 orphan NVIDIA env trio (S2) — operator.
5. F4–F10 (S3) — record-only, no action required.
6. rc-6 dead arm — pin-or-remove owner decision (since r6, open).
7. exit-flatten family — recommendation to the tameshi lane, never a patch.
8. record debt — README 11 unrowed notes; SCORECARD stubs 4–9; LOG one-liners 4–9; drafts' ⟨PENDING⟩ 13/19/19; `walker-deep.md` §10/§11 errata; theme clauses' covering mutant; the exemption list (theme live ×2, walker live ×4 rows, J/K/L stubs, the two usage arms, `VERSION_STR` + base-help discoverability, boundary-prefix assertion) — each is named above with its owner and its route (round-10 plan §(b)(vi)/(c) or the operator); if this round does not land one, it is the arc's named remainder.

**Unknown (12 named):** rendered UI · walker socket protocol · idle
transitions · dispatcher behaviour · window-rule effects · exec-once results ·
waybar module text · compositor env vars live · hypridle/hyprsunset
stop-cause · tree-wide omarchy cleanliness · battery device (absent) ·
edit-without-restart for walker config (every exercise path opens the
launcher — fenced).

## 8. Spot-checks (three, this lane, all re-run 2026-10-14)

1. **Ladder re-derivation.** `git show <commit>:tools/mado-verify.sh` for the
   five gate revisions → shas/lines above; each blob's own `--selftest`
   re-run → 28/28, 53/53, 89/89, 217/217, 268/268; landed revision's four
   modes green (§2.2) with the gate sha identical before and after every run
   (`/tmp/w10-m10-1/gate-sha-{before,after}.txt`).
2. **Kill-ladder re-derivation.** The recorded spec extracted from the gate's
   heredoc hashes to the pinned `c7ee75b9…1dd8` (2,141 B, 10 defects); replay
   against the round-5 blob → `killed=4 survived=6 inconclusive=0` (40 %),
   control GREEN, `MUTATE_RESTORE: OK`.
3. **Substrate anchors.** `hyprctl -j binds | jq length` → 192;
   `hyprctl -j getoption general:gaps_out` → `{"custom":"0 0 0 0","set":true}`;
   `sha256sum ~/.config/hypr/hyprland.conf` → `4f52854a3c143dcf…`;
   `theme.name` → `matte-black`; swaybg argv names the background symlink
   `-m fill`; `omarchy version`/file → 3.8.3, tag `v3.8.4` at HEAD `8fcc9d60`,
   skill leaf `becd149e…`; sockets `socket 755 0` (stat'd, never connected);
   `dev.benz.walker` present; `command -v` → alacritty only; boundary
   `bb2639d9a980…` in every verdict run.

## 9. Unknowns

- The committed round-10 revision: this note is written before the round-10
  commit; every gate number binds to `93e43f8f…` (round-9 landed). A later
  gate edit re-opens the selftest count, the pin and every verdict line.
- Whether round 10 lands the record family (§1.2 debt, the standing-use note,
  the lessons charter) — in flight at write.
- The r9 live theme rows and the walker live-surface rows: whether a seam
  (accepted `XDG_RUNTIME_DIR` override, `busctl`/`hyprctl` stub) ever lands,
  or the exemptions stand as the arc's permanent shape.
- The theme clauses' covering mutant: owed, untracked by the recorded spec.
- Whether each historical revision's suite stays faithful on another
  toolchain (single host, bash 5.3.15).
- Point-sample limits: every live anchor here is one window; a session
  restart invalidates the PIDs (the sockets' mtime marks the session start).

## 10. Falsifiable next-iterations (the arc's standing handover)

- If the gate moves: re-derive §2.1 + §2.5 and re-quote §2.2 — never cite
  this note's numbers for a revision it does not name.
- If a mutant for the theme clauses lands: the spec sha changes; re-derive
  the pin and the rate path.
- If the exempted live rows land: §6's gap row for theme/walker moves to
  closed, with the seam named.
- Before any promotion decision: read §7's record-debt row first — the arc's
  largest named remainder is its own record, not its gate.