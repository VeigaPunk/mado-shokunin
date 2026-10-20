# RegistryDraft — `mado-verify` registry row (mado round 13, W1)

Seat: `MadoR13.RegistryDraft` (leaf; no delegation, no background jobs). Target:
`/home/vgpnk/Projects/shokunin/mado-shokunin`. Status: **draft/audit; no verdict issued, no shared
file written by this seat.**

Scope: the complete registry row for the existing verdict instrument at its registry home
(`PROTOCOL.md:375-423` §Gate standard; row fields `PROTOCOL.md:401-403`): entry, exit maps including
the mode-sensitive `2`, self-test spelling, pinned paths, write scope, owner, and the mutable
fleet-artifact dependency. No invented frozen baseline.

**Late observation:** during this draft another seat landed a `## Gate registry` section at
`SKILL.md:411-428` (three rows: `mado-verify`, `mado-regression`, `mado-snapshot-diff`). This file
therefore now does two things: (a) audits that landed block against the instrument and PROTOCOL and
gives exact cell corrections, and (b) carries the canonical single-row form as the alternative if
the lane prefers one row for one instrument.

Measurement state: the gate file was **under active edit** during this draft. Observed sha256
sequence at reads: `ea798ad0…` (baseline, == round-12 final, 3,245 L) → `c2f0de32…` (3,384 L) →
`240f5091…` (3,392 L) → `b6fd9e5e…` (3,392 L). All anchors below are therefore token/symbol-based;
line numbers are one read's snapshot and will move at the C2 cutover. `git status --short` at the
last read: ` M SCORECARD.md`, ` M SKILL.md`, ` M corpus/README.md`, ` M corpus/SOURCES.md`,
` M corpus/knowledge/config-drift-r12.md`, ` M corpus/knowledge/hyprland-config-era-r12.md`,
` M tools/mado-verify.sh`, `?? .ufo/waves/round-13/`,
`?? corpus/knowledge/wayland-protocol-boundaries-r13.md`.

## 0. Axes (godspeed)

| Axis | Move drafted here | Effect |
|---|---|---|
| coverage — registry schema | landed row audited field by field against `PROTOCOL.md:401-403`; gaps named with replacement cells | the row stops being a pointer and becomes a complete entry |
| operability — exit interpretation | mode-sensitive `2` disambiguated by mode **and** token; snapshot's pass-through verdict stated | a reader cannot mistake SETUP/REFUSED for a failed plane, nor a failing self-test for could-not-evaluate |
| operability — entry command | landed row's `--no-live` entry replaced by the true default plus scope flags | following the row no longer silently skips the live plane |
| maintainability | row cites constant **names**, not values/line numbers; tally and gate sha explicitly unpinned | survives the in-flight C2 edit and later re-cuts |

Rejected moves (harm none): do not pin the self-test tally (moves with additive cases); do not pin
the gate file digest (the gate grades the tree it runs on); do not invent an `expected.json`/frozen
root for `--regression` (none exists); do not restate the C2 census algorithm in the row.

## 1. Sources read (local files; no web opens this seat)

No URLs were opened and no source row is proposed: every anchor is a file in this repository or the
fleet protocol, at baseline revision `7dcb785b7b943d03703181b218d7860a7b43007b` plus the in-flight
working tree. Access date for all: **2026-10-20**. Tier/admission/flip: not applicable (not a
`corpus/SOURCES.md` row; no registry edit made).

| Source | Role |
|---|---|
| `/home/vgpnk/Projects/shokunin/PROTOCOL.md:375-423` (§Gate standard), `:401-403` (row fields) | canonical schema: verdict classes, self-test clause, registry fields, two-evidences clause, frozen-baseline resolution rule |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-verify.sh` | the instrument: header exit map, `usage()`, mode CLIs, constants, write sites |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/SKILL.md:411-428` (landed registry block) | the thing audited in §2 |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/gate-standing-use.md` §1, §4, §5 | prior mode table, cadence, maintenance rules, harness boundary |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/SKILL.md:497-533` (round-5 usage), `:1416-1435` (quick map) | earlier prose the registry row must index, not duplicate |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/SCORECARD.md:322-324, :331-348` | round-13 C2 target and baseline revision |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/evidence/round-12/after.txt:75-87` | last committed measurement of the baseline bytes |
| `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh` | mutable fleet artifact consumed by `--regression` |
| sibling registry precedents: `tsukuroi-shokunin/SKILL.md:1705-1715`, `kumitate-shokunin/SKILL.md:587-607`, `lore-shokunin/SKILL.md:48-70`, `souji-shokunin/SKILL.md:102-107` | fleet row shape (8 columns; token-qualified `2` precedent at `lore-shokunin/SKILL.md:67-68`) |

## 2. Audit of the landed block (`SKILL.md:411-428`)

The landed section is directionally right (three rows, an owner, a prose paragraph that already
names the mutable harness). Its gaps are exact and small:

| # | Severity | Finding | Exact correction |
|---|---|---|---|
| A1 | conformance | `Registry home: PROTOCOL.md §Gate standard, Registry.` names the **schema** location as the home. PROTOCOL says a child lane's registry home is its own `SKILL.md` (`PROTOCOL.md:398`). | `Registry home: this SKILL.md (schema: PROTOCOL.md §Gate standard, Registry).` |
| A2 | operability | The `mado-verify` entry is `bash tools/mado-verify.sh --no-live`, presented as the instrument's entry command. The script's default is a **live** read-only run; `--no-live` is a scope choice that makes the live layer read SKIP. A reader following the row never exercises the live plane. | `bash tools/mado-verify.sh` (default: live read-only against `$HOME` or `MADO_VERIFY_ROOT`; `--no-live` file plane only; `--live` forces live with a non-home root; `--root DIR`; `--snapshot FILE`; `--help`). |
| A3 | operability | Verdict map collapses `2` to "usage or snapshot refusal" and never states that `--snapshot` **passes through the child's 0/1** and only a refusal is 2. The other refusal causes (destination inside `<root>/.config`, child outside 0/1, unparseable report, rows vs counts, write/read-back) are unlisted. `--help` exiting 0 without a verdict is unstated. | `0` clean; `1` failed (FAIL or a required UNKNOWN blocking CLEAN); `2` could-not-evaluate by mode — verify/snapshot usage, snapshot REFUSED, selftest fixture-mktemp, regression SETUP, diff SETUP; the exception is `--selftest` printing `MADO_SELFTEST: FAILED —` → failed; `--snapshot` exits the child's 0/1; `--help` exits 0 with no verdict; other codes → could-not-evaluate. |
| A4 | conformance | `mado-regression` lists `mado_r7_spec_write()` under **pinned-value path**. That is a writer function, not a pin; the pinned bytes are `SPEC_SHA`'s. | `tools/mado-verify.sh`: `PIN_MADO`, `SPEC_SHA` (the embedded spec `mado_r7_spec_write()` writes), `TABLE_MADO`; `HARNESS_SHA_RECORDED` is provenance only. |
| A5 | operability | Write scopes say "isolated temporary trees" without the prefixes or retention rules. | `--selftest`: `/tmp/w5-mado-m52-selftest.*` (removed on pass, kept on failure); `--regression`: `/tmp/mado-verify-regression.*` (removed on PASS unless `--keep`; exact-path, prefix-guarded cleanup); `--snapshot`: caller-named FILE only. |
| A6 | conformance | `mado-verify`'s pinned-value path omits the live version pins; the regression pins appear only in row 2 although both rows are one script. | Add "inline live pins: Hyprland 0.56.2 / `efb5099…`, waybar v0.15.0, walker 2.17.0" to row 1; or consolidate to one row (§3). |
| A7 | minor | Owner is `mado` while the repo identity everywhere else is `mado-shokunin`. Fleet practice allows short names (`tsukuroi`, `souji`), so this is not a defect; exactness is cheap. | Optional: `mado-shokunin`. |
| A8 | structural (L1 judgment) | Three rows describe one script. PROTOCOL speaks of "a gate's registry entry" (singular); modes are not gates. The split also pushes the mode-sensitive `2` across three cells. | Either add a lead-in "one instrument; rows are its mode-level verdict maps", or use the single row + mode table in §3. |

The landed prose paragraph (`SKILL.md:424-428`) is **correct** and should be kept: "Regression's
mutable sibling harness digest is printed as provenance, not an enforced harness pin." The draft
below confirms it with the measured digest and adds the one conformance limit it states.

## 3. Canonical single-row form (paste-ready alternative)

If L1 keeps the three-row shape, apply A1–A6 above to the landed cells. If L1 prefers one row per
instrument, this block replaces `SKILL.md:411-428` (keep the existing prose paragraph):

```markdown
## Gate registry

Registry home: this SKILL.md (schema: `PROTOCOL.md:375-423` §Gate standard, Registry).
One row; detailed mode table, cadence and residual ledger:
`corpus/knowledge/gate-standing-use.md` §1/§4/§6. Historical usage sections
(round 5, round 10) retain their original revisions, not current instrument pins.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| `mado-verify` | gate | `bash tools/mado-verify.sh` from this lane's root (default: live read-only against `$HOME` or `MADO_VERIFY_ROOT`). Scope flags: `--no-live`, `--live`, `--root DIR` / `--root=DIR`. Modes: `--selftest`, `--regression [--keep]`, `--snapshot FILE`, `--snapshot-diff OLD NEW`, `--help` / `<mode> --help`. An absolute script path also works — the script resolves its own location. | `0` → clean. `1` → failed (FAIL, or a required UNKNOWN that blocks CLEAN — never a fake clean). `2` → could-not-evaluate, mode-sensitive: verify usage error; `--selftest` fixture-mktemp failure; `--regression` SETUP; `--snapshot` REFUSED; `--snapshot-diff` SETUP. Sole `2` that maps to **failed**: `--selftest` printing `MADO_SELFTEST: FAILED —`. `--snapshot` exits the **child's** 0/1 and only a refusal is 2. `--help` exits 0 with no verdict. Undeclared codes → could-not-evaluate. | `bash tools/mado-verify.sh --selftest` — spelling is the single token `--selftest` (no internal hyphen); implementation `selftest()`. Hermetic fixtures under `/tmp/w5-mado-m52-selftest.*`, no substrate reads; asserts exit codes and stable row ids (`st_eq` / `st_has` / `st_row_has` / `st_row_detail`). Tally printed, never pinned. | `tools/mado-verify.sh` — in-script constants: `PIN_MADO`, `SPEC_SHA`, `TABLE_MADO` (regression case; `HARNESS_SHA_RECORDED` is provenance only), `EXPECT` (hypr include order, 18 entries), `LOCAL` (declared local `*.conf` set, 13 entries incl. `gkeep`), `OMARCHY_*_PIN`, and the inline live version pins (Hyprland 0.56.2 / `efb5099…`, waybar v0.15.0, walker 2.17.0). No external baseline file. | Verify modes: **none** — `<root>/.config` hashed before/after (`gate boundary.readonly`). `--selftest`: `/tmp/w5-mado-m52-selftest.*` (removed on pass, kept on fail). `--regression`: `/tmp/mado-verify-regression.*` (removed on PASS unless `--keep`; exact-path, prefix-guarded cleanup). `--snapshot`: the named FILE only (must not exist; must not resolve inside `<root>/.config`; partial file removed on failed write). `--snapshot-diff`: none. | mado-shokunin |

Mode map (`MADO_VERIFY:` never appears in `--regression` / `--snapshot-diff` output):

| Mode | Verdict token | Exit | Writes |
|---|---|---|---|
| default / `--live` / `--no-live` / `--root DIR` | `MADO_VERIFY: CLEAN` or `DIVERGED` | 0 / 1 (2 usage) | none |
| `--selftest` | `MADO_SELFTEST: n/n assertions passed`, or `MADO_SELFTEST: FAILED — …` | 0 / 2 | `/tmp/w5-mado-m52-selftest.*` |
| `--regression [--keep]` | `MADO_REGRESSION: PASS` / `FAIL` / `SETUP` | 0 / 1 / 2 | `/tmp/mado-verify-regression.*` |
| `--snapshot FILE` (+ `--no-live` / `--live` / `--root`) | child `MADO_VERIFY:` passed through; `MADO_SNAPSHOT: WRITTEN` or `REFUSED` | child 0/1; 2 refusal | FILE only |
| `--snapshot-diff OLD NEW` | `MADO_DIFF: SAME` / `DETAIL-CHANGED` / `CHANGED` / `SETUP` | 0 / 0 / 1 / 2 | none |
| `--help`, `<mode> --help` | none printed | 0 | none |

Row classes PASS / FAIL / UNKNOWN / SKIP / NOTE: UNKNOWN blocks CLEAN, NOTE never flips a verdict.

**Mutable fleet artifact.** `--regression` consumes
`/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh` (override
`MADO_VERIFY_HARNESS`), resolved as `<fleet>/tameshi-shokunin/tools/mutate-and-run.sh` from the
gate's own path. It is read-only, outside this repo, and **not pinned**: the run prints
`REGRESSION_HARNESS: … sha256=<actual> (recorded revision b56c6e57… — provenance, not gated)`;
the check is the kill table, not the harness identity. The committed input snapshot is the
embedded defect spec (`SPEC_SHA`) applied to the derived target (`PIN_MADO`); the committed
expected verdict is `TABLE_MADO` (ten rows, all `KILLED`). No `expected.json` and no
`.ufo/waves/*/frozen` baseline exists for this gate, and none is claimed.

**Maintenance.** Any gate edit outside the three marker pairs (`MADO-R7-SELFTEST-BLOCK`,
`MADO-R7-REGRESSION-BLOCK`, `MADO-R8-BLOCK`) moves the derived target, so `--regression` reads
SETUP (could-not-evaluate) until the printed `REGRESSION_RECUT` command is run and
`PIN_MADO` / `TABLE_MADO` are updated. SETUP is not a gate failure. The base `--help` lists only
the five original flags; the three later modes print their contract via `<mode> --help` (excision
invariant; discoverability residual named in `corpus/knowledge/gate-standing-use.md` §5.7/§6) —
do not read mode absence from the base help.
```

## 4. Mode-sensitive exit map, expanded

PROTOCOL fixes only the outer interface: `0` = clean, `1` = failed fleet-wide, every other code is
declared per gate and mapped (`PROTOCOL.md:380-382`). This gate reuses `2` across modes; the row
must therefore carry mode **and** a token test, not code alone.

| Mode | Code | Class | Disambiguating token / condition |
|---|---|---|---|
| default / `--no-live` / `--live` / `--root` | 0 | clean | `MADO_VERIFY: CLEAN (` |
| same | 1 | failed | `MADO_VERIFY: DIVERGED (` — includes a required UNKNOWN blocking CLEAN |
| same | 2 | could-not-evaluate | `usage error:` (unknown or malformed argument, missing `--root` value, invalid `MADO_VERIFY_LIVE`) |
| `--selftest` | 0 | clean | `MADO_SELFTEST: n/n assertions passed` |
| `--selftest` | 2 | **failed** | `MADO_SELFTEST: FAILED —` (assertions executed and failed) |
| `--selftest` | 2 | could-not-evaluate | `cannot mktemp` (fixture tree could not be created) |
| `--regression` | 0 | clean | `MADO_REGRESSION: PASS` |
| `--regression` | 1 | failed | `MADO_REGRESSION: FAIL` (measured table differs) |
| `--regression` | 2 | could-not-evaluate | `MADO_REGRESSION: SETUP` (missing tool/harness, spec or pin mismatch, sweep refusal) or `usage error:` |
| `--snapshot FILE` | 0 / 1 | clean / failed | the child run's own `MADO_VERIFY:` verdict; write adds `MADO_SNAPSHOT: WRITTEN` |
| `--snapshot FILE` | 2 | could-not-evaluate | `MADO_SNAPSHOT: REFUSED` (destination exists, destination inside `<root>/.config`, child exited outside 0/1, report unparseable, rows do not reconcile with counts, write/read-back failed) or `usage error:` |
| `--snapshot-diff OLD NEW` | 0 | clean | `MADO_DIFF: SAME` (nothing moved) or `DETAIL-CHANGED` (details moved, classes did not) |
| `--snapshot-diff OLD NEW` | 1 | failed | `MADO_DIFF: CHANGED` (a row class or a scope field moved) |
| `--snapshot-diff OLD NEW` | 2 | could-not-evaluate | `MADO_DIFF: SETUP` (missing/malformed/edited snapshot, counts do not reconcile) or `usage error:` |
| any | 0 | **no verdict** | `--help` / `<mode> --help` |

Consequences for the row:

- Mapping the selftest's assertion failure to **failed** (token-qualified) is deliberate: the
  self-test evaluated and failed. Mapping its fixture-mktemp failure to could-not-evaluate keeps
  the distinction. Precedent for a token-qualified `2 → failed`: `lore-shokunin/SKILL.md:67-68`
  (`2 → failed only with REGRESSION-DETECTED`).
- `--snapshot`'s receipt can exit 2 *after* a clean child run; that is a refused receipt, not a
  diverged plane. `--snapshot-diff`'s `DETAIL-CHANGED` is a 0: detail drift is not a class move.
- A bare `2` on the default path is an invocation defect, so a caller that reads "nonzero = red
  plane" will misread it; the registry row exists to prevent exactly that.

## 5. Pinned values and pinned paths

All expected values live inside the gate; there is no external baseline file. Anchors below are the
constant names (stable); the parenthesised line numbers are one in-flight read (`240f5091…`,
3,392 L) and are not part of the contract.

| Pinned value | Constant / site | What it pins |
|---|---|---|
| regression target | `PIN_MADO` (`:1392`) | sha of this file with the three marker pairs excised |
| regression spec | `SPEC_SHA` (`:1393`) | embedded ten-defect spec bytes written by `mado_r7_spec_write()` |
| regression expected table | `TABLE_MADO` (`:1395`) | `D1:KILLED…R1:KILLED` (10 rows) |
| harness revision | `HARNESS_SHA_RECORDED` (`:1394`) | **printed as provenance, never compared** |
| hypr include order + source targets | `EXPECT` (`:2310`, 18 entries) | 18 source entries, order exact; every `~` entry re-rooted to `$ROOT` and required to resolve (glob ≥1 match) |
| local `*.conf` set | `LOCAL` (`:2394`, append `:2400`) | 13 declared names incl. `gkeep`; observed vs declared compared **exactly**, both sides named on FAIL |
| omarchy pins | `OMARCHY_VERSION_PIN`, `OMARCHY_TAG_PIN`, `OMARCHY_HEAD_PIN`, `OMARCHY_SKILL_SHA_PIN`, `OMARCHY_THEME_PIN`, `OMARCHY_CMD_SURFACE_PIN`, `OMARCHY_SKILL_GROUPS` | version 3.8.3, tag v3.8.4, HEAD 8fcc9d60…, skill leaf becd149e…, theme name, command surface |
| live version pins | inline comparisons | Hyprland 0.56.2 / `efb5099…`, waybar v0.15.0, walker 2.17.0 |
| self-identity | `VERSION_STR` (`:81`) | self-label only; the script's own digest is **not** asserted |

Pinned **paths** (read-only surfaces; `~` is re-rooted to `$ROOT`, so `--root DIR` re-roots every
one of them):

- `$ROOT/.config/hypr/hyprland.conf` and the 18 entries of `EXPECT` under
  `~/.local/share/omarchy/default/hypr/`, `~/.config/omarchy/current/theme/hyprland.conf`,
  `~/.config/hypr/`, `~/.local/state/omarchy/toggles/hypr/*.conf`.
- `$ROOT/.config/hypr/{hyprland,bindings,input,monitors,looknfeel,hypridle,hyprlock,hyprsunset,ai-usage,autostart,envs,xdph,gkeep}.conf` (the `LOCAL` set).
- waybar `config.jsonc` / `style.css`; walker `config.toml`; terminal configs
  (`alacritty.toml`, `foot.ini`, `kitty.conf`, `ghostty/config`); theme chain under
  `~/.config/omarchy/current/theme/` plus consumer imports; omarchy version file, checkout,
  skill link; `~/.local/state/omarchy/toggles/hypr/window-no-gaps.conf`.
- live reads: `hyprctl` read verbs only (`version`, `instances`, `configerrors`, `getoption`,
  `binds`, `monitors`, `layers`, `clients`, `workspaces`); `systemctl --user` status;
  `omarchy version` / `git describe|rev-parse|show` (never `git status`/`fetch`).

No frozen baseline name is registered, so PROTOCOL's bare-name resolution rule
(`PROTOCOL.md:404-406`) is not engaged. That is deliberate: the gate has no
`.ufo/waves/*/frozen` root and no `expected.json`.

## 6. Write scope

| Mode | Writes | Boundary proof |
|---|---|---|
| default, `--no-live`, `--live`, `--root DIR` | none | `<root>/.config` sha before/after; `gate boundary.readonly` PASS/FAIL/SKIP row |
| `--selftest` | `/tmp/w5-mado-m52-selftest.*` (mktemp) | removed on pass; kept and named on failure |
| `--regression [--keep]` | `/tmp/mado-verify-regression.*` (mktemp); embedded spec under it | removed on PASS; `--keep` retains; cleanup is exact-path and prefix-guarded; foreign `/tmp` dirs untouched |
| `--snapshot FILE` | the named FILE only | destination must not exist and must not resolve inside `<root>/.config`; partial file removed on failed write |
| `--snapshot-diff` | none | reads only the two named files |

Never writes the config plane, never mutates the compositor, never touches network. Scratch roots
are created only by the modes that need them; the verify path makes none.

## 7. Mutable fleet artifact dependency

| Fact | Value |
|---|---|
| Artifact | `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh` (fleet sibling, outside this repo) |
| Resolution | `${MADO_VERIFY_HARNESS:-<fleet>/tameshi-shokunin/tools/mutate-and-run.sh}`, `<fleet>` = three `dirname`s above the gate |
| Consumed by | `--regression` only (the default/live/file planes and `--selftest` do not touch it) |
| Observed identity | sha256 `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`, 77,904 B, mtime 2026-10-14 18:00 (read 2026-10-20) |
| Gated? | **No.** The run prints `REGRESSION_HARNESS: … sha256=<actual> (recorded revision b56c6e57… — provenance, not gated)`; `HARNESS_SHA_RECORDED` is never compared. The kill table is the check. |
| Committed expected verdict | `TABLE_MADO` (10/10 KILLED), pinned target `PIN_MADO`, pinned spec `SPEC_SHA`; last committed receipt `.ufo/evidence/round-12/gate-regression-after.txt:1-13` |
| Frozen baseline | **None.** No `expected.json`, no `.ufo/waves/*/frozen` under this lane. Do not add one as conformance theatre; whether the in-script pins plus committed receipt satisfy the §Gate "Two evidences" clause is a reviewer/integrator judgment, not this seat's. |

A second moving part is the live surface itself (`hyprctl`, systemd, the omarchy checkout). That is
the graded substrate, not a fleet artifact: its absence reads UNKNOWN and blocks CLEAN
(`live.plane UNKNOWN`), and it is never faked.

## 8. Placement, ownership, and what happened to the shared file

- Target file: `/home/vgpnk/Projects/shokunin/mado-shokunin/SKILL.md`; the landed section is at
  `:411-428`, between the round-13 diagnostic-boundaries block and `## Evidence trail & sources`.
- `SKILL.md` is a shared source file: this seat wrote no part of it. The landed edit belongs to
  whichever seat applied it; corrections A1–A8 belong to the lane's L1/integrator.
- The gate implementation (`tools/mado-verify.sh`) belongs to the C2 seat; this draft only reads it.
- If the section is kept in place, it should link, not duplicate, the two older prose homes:
  `SKILL.md:497-533` and `SKILL.md:1416-1435` (both re-anchored by the late edits).

## 9. Evidence ledger (exact quotes, all ≤25 words)

| # | Location | Quote | Use |
|---|---|---|---|
| E1 | `PROTOCOL.md:401-403` | "Row fields: name, `gate\|probe`, entry command, verdict map (code → class), self-test command and spelling, pinned-value path, write scope, owner." | the eight fields the row must carry |
| E2 | `PROTOCOL.md:380` | "`0` = `clean` and `1` = `failed` fleet-wide" | outer interface; `2` needs declaration |
| E3 | `PROTOCOL.md:386` | "asserting both the exit code and a stable expected finding-id" | self-test clause; this gate asserts row ids |
| E4 | `PROTOCOL.md:378-379` | "A tool that cannot fail is a **probe**, and is registered as one." | kind = gate (it exits 1 on real defects) |
| E5 | `tools/mado-verify.sh:12-13` | "Exit map: 0 = CLEAN · 1 = DIVERGED (a check FAILed, or a required check was UNVERIFIABLE) · 2 = tool/usage error (bad args; a failing --selftest)." | baseline exit map |
| E6 | `tools/mado-verify.sh:1389-1390` | "Exit map: 0 PASS · 1 FAIL (measured table differs) · 2 SETUP (cannot verify: missing tool/harness, spec or pin mismatch, sweep refusal) · 2 usage error." | mode-sensitive `2` in regression |
| E7 | `tools/mado-verify.sh` snapshot note (`:1815-1816` at the 240f5091 read) | "Exit = the run's verdict; the write adds MADO_SNAPSHOT: WRITTEN\|REFUSED (a refusal exits 2)." | snapshot exit rule |
| E8 | `tools/mado-verify.sh` diff note (`:1817-1819`, same read) | "MADO_DIFF: SAME\|DETAIL-CHANGED\|CHANGED\|SETUP (exit 0/0/1/2). Reads only the two files; never prints MADO_VERIFY:." | diff exit rule |
| E9 | `tools/mado-verify.sh` header (`:24`, same read) | "scratch lives under /tmp/w5-mado-m52-* and only --selftest makes it." | verify-path write scope |
| E10 | `tools/mado-verify.sh` selftest tail (`:1299`, `:1302`, same read) | "MADO_SELFTEST: $n_pass/$n_pass assertions passed" / "MADO_SELFTEST: FAILED — $n_pass passed, $n_fail failed" | token test that splits `2` |
| E11 | `tools/mado-verify.sh:1480` (regression target builder comment) | "anything new outside every pair still does, as the pin and its re-cut note in the header say" | SETUP after a C2 edit |
| E12 | `corpus/knowledge/gate-standing-use.md:227-230` | "its revision is printed as provenance, not gated (the recorded b56c6e57… differs and that is fine — the kill table is the check)" | harness is a named, unpinned dependency |
| E13 | `SCORECARD.md:340-343` | "Baseline source/local checks cannot detect same-count replacement or extra local files." + "stable row ids and named missing/extra details" | why the row must not depend on census internals, only stable ids |
| E14 | `.ufo/evidence/round-12/after.txt:76,80,83,86` | "MADO_SELFTEST: 269/269 assertions passed" · "MADO_VERIFY: CLEAN (52 pass, 8 notes; …)" · "MADO_REGRESSION: PASS (case=mado-verify-hardened; target=538d178b…)" · "ea798ad0… tools/mado-verify.sh" | last committed measurement of the baseline bytes; **not** row pins |
| E15 | `PROTOCOL.md:398` | "a child lane's *registry home* is its own `SKILL.md`" | A1: the landed home sentence points at the schema, not the home |
| E16 | `SKILL.md:413` | "Registry home: `PROTOCOL.md` §Gate standard, Registry." | the sentence corrected by A1 |
| E17 | `SKILL.md:420` | "`bash tools/mado-verify.sh --no-live` (omit flag for live; `--root DIR` for isolated roots …" | A2: the entry makes file-plane the default |
| E18 | `SKILL.md:420` | "2 could-not-evaluate (usage or snapshot refusal)" | A3: the collapsed mode-sensitive `2` |
| E19 | `SKILL.md:421` | "`PIN_MADO`, `SPEC_SHA`, `TABLE_MADO`, `mado_r7_spec_write()`" | A4: a writer function listed as a pin |
| E20 | `SKILL.md:424-426` | "Regression's mutable sibling harness digest is printed as provenance, not an enforced harness pin." | the landed prose is correct and is kept |

## 10. Risks and open items (for L1; no verdicts issued here)

1. **`--regression` will read SETUP on the current tree.** The C2 edits changed `verify()` /
   `EXPECT` / `LOCAL` (outside all three excised marker pairs), so the derived target no longer
   equals `PIN_MADO` (`538d178b…`). That is the designed alarm, not a gate failure; the parent's
   re-cut must update `PIN_MADO` (and `TABLE_MADO` if the measured table moves). The registry row
   must not quote the old pin as current.
2. **The gate file is moving under this draft.** Four distinct sha256 values were observed in one
   session. The row is therefore token-anchored; any line numbers the integrator copies must be
   re-read after the C2 cutover. This seat's line numbers are snapshot data, not contract.
3. **Stale harness digest in the note.** `corpus/knowledge/gate-standing-use.md:227-230` says
   harness sha "cf41efaa…242c75 today, unchanged since the round-8 freeze"; the live file now
   hashes `75ed934d…`. No verdict moves (the digest is provenance only), but the registry row must
   not repeat that digest as a pin — another reason the row names the artifact, not its hash.
4. **Landed-row gaps are the operability payload.** A2 and A3 are not cosmetic: following the
   landed `--no-live` entry skips the live plane, and the collapsed `2` makes a refused snapshot
   indistinguishable from a diverged config in a log reader. A1 is a one-line conformance fix.
5. **Base-help discoverability.** `--help` omits `--regression`, `--snapshot`, `--snapshot-diff`
   (excision invariant). The registry row compensates by listing all modes; the residual stays
   named in the standing-use note (§5.7/§6), not fixed here.
6. **Self-test tally is not a pinned value.** Last committed tally is 269/269 at `ea798ad0…`; the
   C2 suite adds assertions. The row records the command, spelling and token shape, never a count.
   A reviewer who wants a tally must run the mode (parent gate), not read the row.
7. **Two-evidences judgment.** The gate ships in-script input pins plus a committed receipt, with a
   mutable, unpinned harness. Whether that satisfies PROTOCOL's "two evidences" clause is left to
   the reviewer/integrator; this draft records the dependency honestly rather than inventing a
   frozen baseline.
8. **Row count/shape is L1's call.** Three mode rows vs one instrument row is a judgment; the
   single-row form in §3 is the lower-ambiguity option, but applying A1–A6 in place is sufficient
   if the landed shape is kept.

## 11. What this seat did not do

- No edit to `SKILL.md`, `tools/mado-verify.sh`, `SCORECARD.md`, `corpus/**`, or any host config.
- No gate execution: no `--selftest`, `--regression`, `--snapshot`, `--snapshot-diff`, live run, or
  census. Reads were static (`read`/`grep`/`sha256sum`/`wc`/`git status`/`git rev-parse`).
- No web source opened; no `corpus/SOURCES.md` row proposed; no tool installed or upgraded.
- No verdict on C1 or C2, no commit, push, or external-state action.

## Appendix — frozen two-evidences runner (round 13, dependent continuation)

Added at L1's request after the audit above; no earlier text was changed. Goal is the §Gate
standard "Two evidences" clause for a gate that grades a mutable fleet artifact — not a new
claimed axis.

**File:** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-13/frozen/verify.py`
(this seat's only implementation file; main populates the other three inputs).

| Field | Value |
|---|---|
| Entry | `python3 .ufo/waves/round-13/frozen/verify.py` — the frozen root is always the script's directory; the only flag is `--selftest`; the frozen-run subprocess timeout is fixed at 900 s |
| Self-test | `python3 .ufo/waves/round-13/frozen/verify.py --selftest` — spelling is the single token `--selftest` (no internal hyphen) |
| Inputs main populates | `frozen/gate.sh` (full final gate), `frozen/harness.sh` (read-only sibling copy), `frozen/expected.json` |

**`expected.json` shape** (values committed by main, never derived by the runner):

```json
{
  "inputs": {
    "gate.sh": "<sha256>",
    "harness.sh": "<sha256>"
  },
  "expected_exit": 0,
  "expected_marker": "MADO_REGRESSION: PASS"
}
```

The schema is exact: only those three top-level keys and only `gate.sh` / `harness.sh` inside
`inputs`. Any extra, missing or renamed key is refused as `frozen_error`. Both paths must resolve
inside the frozen root — a symlink escaping it is `snapshot_tampered` before hashing. No flat
alternate shape, no configurable paths, no environment overrides.

**Behavior, in order:**

1. Parse and validate `expected.json`; malformed or missing → exit 2 `frozen_error`.
2. sha256 both fixed inputs **before any execution**; a missing, changed, unsafe or unreadable
   input is named (`FROZEN_DETAIL: missing <name>` / `mismatch <name> expected=… actual=…`) and
   the run exits 2 `snapshot_tampered`; the gate is never invoked.
3. Only on full digest agreement: `bash <frozen>/gate.sh --regression` with
   `MADO_VERIFY_HARNESS=<frozen>/harness.sh`, cwd = frozen root; the gate's output is printed
   verbatim.
4. Verdict comparison: exit code must equal `expected_exit` **and** `expected_marker` must appear
   in the combined output. Contradiction → 1 `frozen_verdict_mismatch`; both hold → 0
   `frozen_match`. Start failure or timeout → 2 `frozen_error`.

**Machine-readable lines:** `FROZEN_INPUT: <name> sha256=<digest> verified` (one per fixed
input), `FROZEN_RUN: bash <gate> --regression (cwd=<root>, harness=<path>)`,
`MADO_FROZEN: MATCH|MISMATCH|TAMPERED|ERROR`, `FROZEN_DETAIL: …`, `FROZEN_ID: <stable id>`.
Ids: `frozen_match`, `frozen_verdict_mismatch`, `snapshot_tampered`, `frozen_error`. Codes follow
the fleet outer interface: 0 clean, 1 failed, 2 could-not-evaluate.

**Self-test (fixtures only, no real harness):** builds isolated trees under
`/tmp/mado-r13-frozen-selftest.*` (removed on pass, kept on failure) and asserts, against literal
pinned digests committed in `verify.py` rather than values recomputed from the fixtures:

| Fixture | Expected |
|---|---|
| clean gate (`MADO_REGRESSION: PASS`, exit 0) | 0 + `frozen_match` + gate invoked + `MADO_VERIFY_HARNESS` equals the fixture harness |
| marker/exit contradiction (prints `FAIL`, exits 0) | 1 + `frozen_verdict_mismatch` + gate invoked |
| digest tampered (pinned digest belongs to other bytes) | 2 + `snapshot_tampered` + gate **not** invoked |
| pinned input missing | 2 + `snapshot_tampered` + gate **not** invoked |
| malformed `expected.json` | 2 + `frozen_error` + gate **not** invoked |

No network, no host-config reads, no writes outside the temp fixture root. The runner itself never
writes outside that root; it only reads the frozen inputs and executes the frozen gate.

**Not executed by this seat.** Main runs the single post-integration check. Reconciliation note:
§7 above ("no `expected.json`") described the lane repo before this continuation; the frozen
directory now carries one, scoped to this runner and to the committed frozen run — it is not a
frozen baseline name under PROTOCOL's `.ufo/waves/*/frozen` resolution rule, and the registry row
in §3 does not need to change. If L1 wants the run named in the row, add
`frozen/verify.py` + `frozen/expected.json` to the pinned-value cell.

