# w1 / ExecLiveHost — live read-only runs of the L1 reference (DONE)

Seat assignee: ExecLiveHost. Lane: `mado-shokunin`, round 45, w1. Date 2026-10-26 (runs 15:55 -03:00).
Reference: `.ufo/waves/round-45/l1-draft/mado-monitors.py`, sha256
`c6ac5fc2d35e40b34dcf031940222fbe5ec5f0ce4b07d6a41866b196843726be` (same hash as the L1 receipt's `# tool sha256`).
Host: Hyprland `v0.56.2` commit `efb50993780079460b0cbed1363e2166a2de1d9f`, dirty=false (`hyprctl version -j`); one output (DP-1).

Every command, its stdout and its exit code are in `runs.txt` (this seat dir, 145 lines). Every quote below is
checked by `verify-quotes.py` against `runs.txt` and the L1 host receipt; `verify.txt` shows `VERIFY: all checks
passed` (17 quote checks plus the receipt comparison, all OK — including
`OK R1 stdout == receipts/live-monitors-host-l1.txt stdout (3 lines)`).

## Answer to the seat question

**`hyprctl monitors -j` and `hyprctl monitors all -j` do not differ on this host.** Both exit 0, both print 1339
bytes, and `cmp` exits 0: byte-identical dumps, no key present in only one form, equal commit-safe projections
(`runs.txt:134`). The reason is structural: the host has one output and no disabled output, and `all` only adds
disabled outputs. Consequently every run below returns the same verdict for both list forms
(R1==R2, R4==R5, R4==R11; `runs.txt:128`, `runs.txt:130`), and **this host cannot distinguish a tool that reads
either form**. The DISABLED branch is not reachable live here, and with the plain form a disabled output would be
absent from the dump entirely — `all` is the form the contract describes.

## Runs (all exit codes recorded; stderr empty on every run)

| run | list form | config input | exit | final line |
|---|---|---|---|---|
| R1 | `monitors all -j` | `~/.config/hypr/monitors.conf` | 0 | `... outputs=1 matched=1 ... verdict=OK` (`runs.txt:48`) |
| R2 | `monitors -j` | same | 0 | identical stdout to R1 |
| R3 | `monitors all -j` | all 19 files reached from `hyprland.conf`, source order | 0 | identical stdout to R1 |
| R3b | `monitors all -j` | the 19 plus `~/.config/hypr/hyprland.conf` itself | 0 | identical stdout to R1 |
| R4 | `monitors all -j` | omarchy shipped `~/.local/share/omarchy/config/hypr/monitors.conf` | 0 | `sel=""` rule, `verdict=OK` (`runs.txt:74`) |
| R5 | `monitors -j` | same omarchy file | 0 | identical stdout to R4 |
| R6 | `monitors all -j` | seat fixture: omarchy file with its only active `monitor=` line commented | 4 | `... lines=0 ... verdict=NO_RULES` (`runs.txt:89`) |
| R7 | `monitors all -j` | seat fixture: user monitors.conf with its only active line commented | 4 | `NO_RULES` |
| R8 | `monitors all -j` | seat fixture: `monitorv2 { output = DP-1 }` only | 5 | `... v2=1 ... verdict=NOT_COMPARED` (`runs.txt:101`) |
| R9 | `monitors all -j` | omarchy default **then** user file | 0 | 2 rules; DP-1 gets rule 2 (`runs.txt:107-109`) |
| R10 | `monitors all -j` | user file **then** omarchy default | 0 | 2 rules; DP-1 gets rule 1 |
| R11 | `monitors -j` | omarchy default | 0 | identical stdout to R4 |

R1's three stdout lines are byte-for-byte the L1 host receipt's stdout
(`receipts/live-monitors-host-l1.txt`), so the C1 reference's live-run receipt is independently reproduced at
tool sha `c6ac5fc2…` — `verify.txt` last line. `--selftest` also prints `MADO_MONITORS_SELFTEST: 33/33 passed`,
exit 0 (`runs.txt:131`), matching the registration's "selftest 33/33".

## Config scopes

`~/.config/hypr/hyprland.conf` reaches **19** files through `source =` (glob
`~/.local/state/omarchy/toggles/hypr/*.conf` expanded to 2; all 19 exist; list in `runs.txt`). A `grep -nE
'^[ \t]*(monitor|monitorv2)([ \t]*[={]|[ \t]*$)'` over all 19 returns exactly one line:
`/home/vgpnk/.config/hypr/monitors.conf:10:monitor = DP-1, 3440x1440@100, 0x0, 1` (`runs.txt:39`), and zero
`monitorv2` lines. So the loaded plane carries one rule, and R3/R3b collapse to R1's output — the tool sees no
extra rule or `monitorv2` block from the omarchy default tree, the theme file, the toggles, or the root file.

Commented alternatives are inert as the contract says: the user file has seven commented `# monitor...` lines
(`runs.txt:144`) and R1 reports `unsupported=0 badrules=0`, because a stripped line starting `#` does not
fullmatch the monitor pattern (`l1-draft/mado-monitors.py:33`). The omarchy shipped file behaves the same: one
active `monitor=,preferred,auto,auto`, six commented alternatives (`runs.txt:145`), `lines=1`.

## What the tool says about commented / default / v2 inputs

- **Default (empty-selector) rule**: `monitor=,preferred,auto,auto` is modelled as rule 1 `sel=""`,
  `mode=preferred pos=auto scale=auto transform=0 mirror=- disabled=false` (`runs.txt:74`); DP-1 takes it as the
  empty-selector fallback and the verdict is AGREE/OK. Only transform and mirror are actually compared there
  (mode is not compared for preferred, position/scale not compared for auto — `l1-draft/mado-monitors.py:47`,
  `:67`); the AGREE therefore says little about that file beyond transform 0 and `mirrorOf` "none".
- **Commented-out only**: with the single active line commented (R6, R7) the verdict is NO_RULES, exit 4,
  `lines=0` (`runs.txt:89`) — the ladder's first rung (`l1-draft/mado-monitors.py:85-88`), and the output is
  UNRULED rather than a silent OK.
- **`monitorv2`**: R8 gives NOT_COMPARED, exit 5, `v2=1` (`runs.txt:101`), i.e. the "a monitorv2 block ... can
  change which rule applies" rung above DIFFER in that same ladder.
- **Both scopes at once**: R9/R10 show rule numbering follows argument order (`n=1 sel=""` then
  `n=2 sel="DP-1"`, or reversed) while DP-1's effective rule is the named one in both orders — the "last rule
  whose selector matches it, else the first rule with an empty selector" lookup (`l1-draft/mado-monitors.py:8`).

## Supports / attacks

Supports:
- C1's live-run precondition on this exact host: the reference reproduces `receipts/live-monitors-host-l1.txt`
  verbatim, and the live values it joins are real — explicit mode `3440x1440@100` against live
  `refreshRate` 99.997 (|Δ| = 0.003 < 1, so the closeness bound at `l1-draft/mado-monitors.py:67` is exercised
  with a non-equal value), `0x0` position, `scale` 1, `transform` 0, `mirrorOf` "none".
- The comment, empty-selector, `monitorv2` and multi-file paths of the contract all behave as documented on
  real host bytes (R4-R10).

Attacks / limits (what this host does **not** show):
- **AGREE is file-scope, not config-scope.** R4 passes the omarchy *shipped* file, which the live
  `hyprland.conf` does not source, and still reports AGREE/OK (`runs.txt:74`). Nothing in the tool ties the named
  file to the config Hyprland actually loaded, so an OK on an unused file is indistinguishable from an OK on the
  loaded one. A verdict is only as good as the caller's claim about which files are sourced.
- **The live branch exercised is the trivial one.** Not reachable on this host: a disabled output (so
  DISABLED/live-disabled DIFFER), a second output or `mirror`, `transform` ≠ 0, a fractional scale needing the
  1/120 correction, a `desc:` selector, an unsupported or bad-key line, and 60 Hz defaulting — the pins' and
  fixtures' territory, not this host's.
- **List forms are indistinguishable here** (byte-identical dumps), so this seat gives no live evidence for the
  `all` requirement; it only shows nothing contradicts it.
- Observation for the C1 counter reading, not a defect: `python3 -I` does not affect the tool, which starts no
  process and opens no socket (`l1-draft/mado-monitors.py:22`). The pipeline still needs a live compositor: the
  seat shell env lacked `HYPRLAND_INSTANCE_SIGNATURE`, so `hyprctl` was given `XDG_RUNTIME_DIR=/run/user/1000`
  and the single signature name found under `/run/user/1000/hypr` (read-only lookup). That is harness
  environment, not tool input.

## Host safety and scope

Read-only throughout: only `hyprctl version -j`, `hyprctl monitors -j`, `hyprctl monitors all -j` were run — no
`dispatch`, `keyword`, `reload`, `setprop`, `--batch`, `output`, `plugin`, `kill`; no Wayland client of my own; no
pacman transaction; no host config or binary written; no git/jj mutation anywhere; nothing written outside this
seat dir. Receipts carry only the projected fields (name, width, height, refreshRate, x, y, scale, transform,
disabled, mirrorOf): description/make/model/serial never appear (checked by `verify-quotes.py`; the words
"description / make / model / serial" occur once, in the header line that names them as dropped). No tool was
installed. Scratch `/fast/scratch/hyaku/mado-r45/ExecLiveHost/` was removed after copying receipts into this
seat dir.

## Files in this seat dir

- `runs.txt` — 11 runs (R1-R11): command, stdout, exit code, stderr, projected dump, 19 source paths, grep
  result, list-form comparison, fixture hashes.
- `verify.txt` — output of `python3 -I verify-quotes.py` (`VERIFY: all checks passed`, exit 0).
- `verify-quotes.py` — greps every quoted line above and R1's stdout against `runs.txt` and the L1 receipt.
- `fx/omarchy-commented.conf`, `fx/user-commented.conf`, `fx/v2-only.conf` — the three derived inputs for
  R6-R8, each with a recorded sha256 and the exact transformation that produced it.
