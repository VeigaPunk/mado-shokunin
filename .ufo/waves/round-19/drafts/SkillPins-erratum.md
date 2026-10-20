# SkillPins — round-19 SKILL.md walker erratum draft

Target: `/home/vgpnk/Projects/shokunin/mado-shokunin/SKILL.md`, 1,844 lines, byte-identical to
baseline `9c54c56` (`git diff --stat 9c54c56 -- SKILL.md` prints nothing). Append point: after
line 1844 (last line `> and the bound receipt are the defence).`, file ends with `0a`), two
blank lines (the separator convention before `## Errata (round 18, append-only)` at `:1818-1819`),
then the heading below. Draft only — L1 owns the edit.

## 1. Present-tense walker version/size pins in SKILL.md

`grep -nE '2\.17\.0|298 L|64826a85|--version' SKILL.md` returns:

| Line | Pin text (quote) | Covered by the round-18 erratum (`:1820-1828`)? |
|---|---|---|
| 23 | `walker 2.17.0 (MADO-1 §9; MADO-2 §1; re-verified \`hyprctl version\`)` — under the "Version pins for all claims below" sentence at `:21` | **Yes** — `:1822` names "the version pin … at the top of this file (lines 22-23)". No S token on those lines, so it does not satisfy the round-19 pointer. |
| 114 | launcher row, files cell: `~/.config/walker/config.toml` (49 L; packaged table `/etc/xdg/walker/config.toml`, 298 L — MADO-R3-1 §6) | **Yes for `298 L`** — `:1824` names the "packaged table '298 L'". `49 L` is unchanged, so no supersession exists to date. |
| 114 | launcher row, consumer cell: `walker 2.17.0` via `app-walker@autostart.service` + `elephant.service` | **Yes** — `:1824` names the launcher row's `walker 2.17.0`. No S token. |
| 1075 | `walker --version` = `2.17.0`; binary sha `64826a8531eac525…` | **No** — the round-18 erratum never names `:1075`, the `--version` reading or the `64826a85…` digest; `:1828` only says the *running* binary is `[UNK]`. |
| 1473 | binary sha256 `64826a85…` | **No** — no digest supersession anywhere in `:1820-1828`. |
| 1474 | BuildID `a22452d1…`, `.comment` rustc 1.97.1 (Arch) / LLD 22.1.8 | **No** — BuildID/toolchain not named. |
| 1475 | package `walker 2.17.0-1` with `pacman -Qkk` 29 files / 0 altered | **No** — package pin not named; the log line in `:1825` implies it but no file-count statement. |
| 1476 | printed `2.17.0\n` proven to be the compiled-in rodata literal (offset 847,791) | **No** — offset and rodata claim not re-anchored. |

Not in scope: `:169` (`mako --version` misuse, no walker version), `:114` `elephant.service`
name and the `walker-restart.hook` lines (no version pin), any `--version` mention outside a
walker pin.

## 2. Proposed append — exact text

Every non-empty line below was written to hold both `2.17.2` and an `S###` token on the same
line, so the whole appended block (heading included) satisfies the round-19 pointer predicate
`2\.17\.2.*\bS\d{3}\b|\bS\d{3}\b.*2\.17\.2`. Two blank lines precede the heading; one blank line
separates the heading from the blockquote.

```markdown
## Errata (round 19, append-only — walker 2.17.2 pins; S090/S091/S096)

> Erratum (round 19; SkillPins): walker is installed at 2.17.2-1 — S090 `/var/log/pacman.log:2929` records `[ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)` at 2026-10-20T09:16:46-0300, and the only walker version literal in `/usr/bin/walker` is `2.17.2` (S096). This supersedes the pins above: the round-18 erratum at `:1820-1828` already dates `:23` and `:114`, while `:1075` and `:1473-1476` are re-anchored here for the first time.
> - Former `SKILL.md:23` — "walker 2.17.0 (MADO-1 §9; MADO-2 §1; re-verified `hyprctl version`)": dated 2026-10-14 (round-18 erratum `:1822`); read "walker 2.17.2" today, package 2.17.2-1 per S090 and the binary's sole version literal per S096 — the `hyprctl version` clause re-verifies Hyprland, not walker.
> - Former `SKILL.md:114`, packaged-table cell — "298 L": dated 2026-10-14 (round-18 erratum `:1824`); re-verified 2026-10-20 (`wc -l`, `sha256sum`) as 305 L / 13,743 B / `3c5c6867…` (S091), byte-equal to the upstream v2.17.2 `resources/config.toml` recorded at S073.
> - Former `SKILL.md:114`, consumer cell — "walker 2.17.0 via `app-walker@autostart.service` + `elephant.service`": the version is dated and now 2.17.2 (S090 upgrade line; S096 binary literal); the two unit names and the restart route were not re-probed this round and remain as written.
> - Former `SKILL.md:114`, user-config cell — "49 L": re-verified 2026-10-20 unchanged at 49 L / 1,336 B / `fecf71fa…` (S091); the only moved value on that row is the walker version, now 2.17.2 (S090).
> - Former `SKILL.md:1075` — "`walker --version` = `2.17.0`; binary sha `64826a8531eac525…`": the 2.17.0 reading is a dated 2026-10-14 execution, not repeated (`--version` launches the binary; host pause); today's file bytes are 7,039,912 B / sha256 `25240650…` with the sole version literal `2.17.2` at file offset 856,302 in the `.rodata` run `version2.17.2\n` (S096) — the printed line is inferred from that literal, not observed.
> - Former `SKILL.md:1473` — "binary sha256 `64826a85…`, BuildID `a22452d1…`": dated round-9 identity of the 2.17.0-1 build; the installed 2.17.2 build's bytes hash `25240650…` with BuildID `19200fe47eb6c90fc4956f0d52d0c7c84bb89e99` (`sha256sum`, `readelf -n`; S096).
> - Former `SKILL.md:1474` — "`.comment` rustc 1.97.1 (Arch) / LLD 22.1.8": dated round-9 toolchain; the 2.17.2 build's `.comment` reads rustc 1.99.0 (b940084d7 2026-09-28), LLD 23.1.1, GCC 16.2.1 20260810 (S096, `readelf -p .comment`).
> - Former `SKILL.md:1475` — "`walker 2.17.0-1` with `pacman -Qkk` 29 files / 0 altered": the package pin is superseded by 2.17.2-1 (S090); the `-Qkk` count is a dated round-9 record, not re-run this round (host pacman pause), so it stays `[UNK]` for 2.17.2 and is not claimed.
> - Former `SKILL.md:1476` — "printed `2.17.0\n` … rodata literal (offset 847,791)": dated; the 2.17.2 binary's sole version literal sits at 856,302 (S096), and its embedded default config at offset 806,960 is 13,743 B / `3c5c6867…`, byte-equal to the `/etc/xdg` file (S091).
> - Residual — the running process stays `[UNK]` (no process probe, host pause); 2.17.2 is established for the installed package (S090) and for the `/usr/bin/walker` bytes (S096), and `corpus/knowledge/walker-route-r18.md` remains the documentary route for 2.17.2 with the host rows S090/S091 in support.
```

The heading deliberately carries the subject and the three row tokens so that no appended
non-empty line is unmatched; only blank separator lines are exempt.

## 3. Per-old-line disposition (dated vs re-verified)

| Old line | Dated (as recorded) | Re-verified today (2026-10-20, file bytes only) | Superseding value | Token |
|---|---|---|---|---|
| 23 | version pin dated 2026-10-14 (MADO-1 §9; MADO-2 §1) | not re-run as a process; installed package `walker-2.17.2-1` present at `/var/lib/pacman/local/walker-2.17.2-1/desc` (`%VERSION%` 2.17.2-1), last log line is the upgrade | `walker 2.17.2` | S090 (`/var/log/pacman.log:2929`), S096 (binary literal) |
| 114 `298 L` | length dated 2026-10-14 (MADO-R3-1 §6) | `wc -l` = 305; `sha256sum` = `3c5c6867…`; 13,743 B; equals the embedded default at binary offset 806,960 and S073's upstream v2.17.2 file | 305 L | S091, S073 |
| 114 `walker 2.17.0` | dated 2026-10-14 | unit files not read this item; only the version moves (the `app-walker@autostart.service` / `elephant.service` names and the `omarchy restart walker` route are unchanged text, not re-probed) | 2.17.2 | S090, S096 |
| 114 `49 L` | — (still current) | re-verified: `wc -l` 49, 1,336 B, `sha256sum` `fecf71fa…`; equal to S085's stock file | unchanged | S091 |
| 1075 `--version` + sha `64826a8531eac525…` | execution reading dated 2026-10-14, not repeated (launch permission absent) | binary bytes only: 7,039,912 B / `25240650…`; one walker version literal `2.17.2` at offset 856,302, preceded by `version`, followed by `\n`, inside `.rodata` (section off 0x0b6900, size 0x074654); zero `2.17.0` matches | sha `25240650…`; printed version inferred `2.17.2\n` | S096 |
| 1473 | round-9 build identity (sha, BuildID) | `sha256sum` `25240650…`; `readelf -n` Build ID `19200fe47eb6c90fc4956f0d52d0c7c84bb89e99` | as listed | S096 |
| 1474 | round-9 toolchain | `readelf -p .comment` → rustc 1.99.0 (b940084d7 2026-09-28), LLD 23.1.1, GCC 16.2.1 20260810 | as listed | S096 |
| 1475 package | round-9 package pin | `-Qkk` not run (pacman pause); package dir name and log line agree on 2.17.2-1 | `walker 2.17.2-1` | S090 |
| 1475 `-Qkk` 29 files | round-9 check | **not checked** — `[UNK]` for 2.17.2, stated as such | — | (S096 line says not claimed) |
| 1476 | round-9 rodata offset 847,791 | one `2.17.2` literal at 856,302; embedded default at 806,960 = 13,743 B `3c5c6867…` | 856,302 | S096, S091 |

## 4. Coverage check (runnable)

Extract the appended block and assert every non-empty line matches the pointer predicate:

```bash
cd /home/vgpnk/Projects/shokunin/mado-shokunin
awk '/^## Errata \(round 19/,0' SKILL.md | grep -vE '^[[:space:]]*$' \
 | grep -vE '2\.17\.2.*\bS[0-9]{3}\b|\bS[0-9]{3}\b.*2\.17\.2' \
 && echo NONCONFORMING || echo ALL-LINES-CARRY-2.17.2-AND-S###
```

and for the C2 counter itself:

```bash
python3 -I .ufo/waves/round-19/fresh-pins.py REV   # SKILL.md row must flip to current, pointer line = heading
```

Byte-exact apply helper (extracts this draft's fenced block, 3,418 B,
sha256 `f61b82ee79cea6d49353dd4cedcee15305da3642aae795c8da691b5679da6ad4`):

```bash
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 - <<'PY'
import hashlib, re
d = open('.ufo/waves/round-19/drafts/SkillPins-erratum.md').read()
blk = re.search(r'```markdown\n(.*?)\n```', d, re.S).group(1)
assert hashlib.sha256(blk.encode()).hexdigest() == 'f61b82ee79cea6d49353dd4cedcee15305da3642aae795c8da691b5679da6ad4'
s = open('SKILL.md').read()
assert '## Errata (round 19' not in s and s.endswith('\n')
open('SKILL.md', 'w').write(s + '\n\n' + blk + '\n')
PY
```

Baseline for comparison (run this seat): denominator 13, current 2 (SKILL.md false,
`walker-route-r18.md:1` true), score 1.5385 — SKILL.md gains the 3rd file once the block lands.

## 5. Planner notes / residuals

- **S096 is reserved, not yet a row.** This draft cites it as the reserved id. L1 must open
  S096 with: `/usr/bin/walker` 7,039,912 B sha256 `25240650686fe6adf0e945530f6e701f5b67535f3e8f9187b08f022317d93096`,
  sole walker version literal `2.17.2` at file offset 856,302 in `.rodata`, and
  `/var/log/pacman.log:2929`; `--version` was not executed.
- **C2 wording "and the upstream release".** The 305 L bullet cites S073 for the upstream
  v2.17.2 file, but S073 is a round-18 row. If L1 reads C2 as requiring a *new this-round*
  upstream-release row, add `S0xx-pending` on that same line; the erratum already contains
  `2.17.2`, so the predicate still passes.
- **`walker --version` is not observed.** The printed `2.17.2\n` is inference from the rodata
  literal (same shape as the round-9 proof for `2.17.0`), and the erratum says so.
- **`pacman -Qkk` 29 files / 0 altered is not re-run** and is explicitly left `[UNK]` for
  2.17.2 rather than restated.
- **Corroboration outside the S ids:** `/var/lib/pacman/local/walker-2.17.2-1/desc` line 5
  `2.17.2-1` (file bytes; directory name `walker-2.17.2-1`). Not cited in the erratum to keep
  each line on the assigned rows; available if L1 wants a second host anchor.
- **Elephant 2.22.1** (pacman.log:3095) is outside this item; `:114` names the unit only.
- **No SKILL rewrite:** the erratum is append-only; the old pin lines stay untouched.
