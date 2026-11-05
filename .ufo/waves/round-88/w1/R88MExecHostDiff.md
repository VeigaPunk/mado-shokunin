# R88MExecHostDiff — host-config coverage receipt (base resolver vs round-88 c2 candidate)

Seat: R88MExecHostDiff (leaf, wave w1, round 88). Date 2026-11-06. Base revision
`24ba2a9ddac21c1211579231e6ee1d98963f9988`. This is a measurement receipt: what the base tool and the
candidate tool each resolve on the host's real mako configuration. It is **not** a score, a mutation
run, or a verdict on C1/C2; no case file was used and no counter was run against a candidate.

## Pins and inputs

| item | value |
|---|---|
| base tool | `git show 24ba2a9ddac21c1211579231e6ee1d98963f9988:tools/mado-mako.py` |
| base sha256 | `67a955a5fa06135c2748855b7e452bd3f0792c540002009ec90842ee5c986698` |
| candidate tool | `.ufo/waves/round-88/build/mado-mako.c2.py` |
| candidate sha256 | `8d86f131b0964c2c0ee8e92df543611f0f850ef1960219b0d71a8f3042dbabfb` |
| working-tree `tools/mado-mako.py` | same sha256 as the candidate (byte-equal at measurement time) |
| host config argument | `/home/vgpnk/.config/mako/config` |
| host config, realpath | `/home/vgpnk/.config/omarchy/current/theme/mako.ini` (`config` is a symlink; caller-named, so outside the C2 stance) |
| include chain | `mako.ini:1` -> `~/.local/share/omarchy/default/mako/core.ini` (realpath `/home/vgpnk/.local/share/omarchy/default/mako/core.ini`, inside `/home/vgpnk`) |
| `--home` actual value | `/home/vgpnk` (expanded). Neither tool calls `expanduser` on `--home` (`tools/mado-mako.py` at base rev line 527 `home = args.home`; `mado-mako.c2.py:665`), so a literal `~` would make the include target relative and refused. |

Host config read scope: only `~/.config/mako/config` (a symlink), the file it points at
(`/home/vgpnk/.config/omarchy/current/theme/mako.ini`, 5 lines) and its one include
(`/home/vgpnk/.local/share/omarchy/default/mako/core.ini`, 38 lines). Nothing else was read on the host.

## Grid

36 inputs: app-name {notify-send, Spotify, firefox} x urgency {low, normal, critical} x modes
{[], [do-not-disturb]} x summary {"Setup Wi-Fi", "hello"}. Base invocation:
`--config ~/.config/mako/config --home ~ --app-name APP --urgency URG [--mode MODE]`.
Candidate: same plus `--summary <grid value> --body grid-body --category grid-category
--desktop-entry grid-desktop-entry --app-icon grid-app-icon --actionable false --expiring false`.
`cand-bare` = the candidate invoked exactly like the base (the extra inputs belong to the candidate's
model and cannot be passed to the base, whose CLI has no such flags).

All 108 tool invocations (36 x 3 tools) exited rc=0; the driver's own stderr was empty (each tool's
one-line `MADO_MAKO: resolved=... refusals=...` stderr summary is captured and not recorded).
Columns `inv` / `to` / `lay` / `obl` are `effective.invisible` / `default-timeout` / `layer` /
`on-button-left`; `ref` is the number of refusals. Every base row has 7 refusals, every candidate
row 5.

| app | urgency | modes | summary | base rc | base invisible | base timeout | base layer | base on-button-left | base refusals | cand rc | cand invisible | cand timeout | cand layer | cand on-button-left | cand refusals |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| notify-send | low | - | Setup Wi-Fi | 0 | 0 | 5000 | top | invoke-default-action | 7 | 0 | 0 | 5000 | top | invoke-default-action | 5 |
| notify-send | low | - | hello | 0 | 0 | 5000 | top | invoke-default-action | 7 | 0 | 0 | 5000 | top | invoke-default-action | 5 |
| notify-send | low | do-not-disturb | Setup Wi-Fi | 0 | 0 | 5000 | top | invoke-default-action | 7 | 0 | 0 | 5000 | top | invoke-default-action | 5 |
| notify-send | low | do-not-disturb | hello | 0 | 0 | 5000 | top | invoke-default-action | 7 | 0 | 0 | 5000 | top | invoke-default-action | 5 |
| notify-send | normal | - | Setup Wi-Fi | 0 | 0 | 5000 | top | invoke-default-action | 7 | 0 | 0 | 5000 | top | invoke-default-action | 5 |
| notify-send | normal | - | hello | 0 | 0 | 5000 | top | invoke-default-action | 7 | 0 | 0 | 5000 | top | invoke-default-action | 5 |
| notify-send | normal | do-not-disturb | Setup Wi-Fi | 0 | 0 | 5000 | top | invoke-default-action | 7 | 0 | 0 | 5000 | top | invoke-default-action | 5 |
| notify-send | normal | do-not-disturb | hello | 0 | 0 | 5000 | top | invoke-default-action | 7 | 0 | 0 | 5000 | top | invoke-default-action | 5 |
| notify-send | critical | - | Setup Wi-Fi | 0 | 0 | 0 | overlay | invoke-default-action | 7 | 0 | 0 | 0 | overlay | invoke-default-action | 5 |
| notify-send | critical | - | hello | 0 | 0 | 0 | overlay | invoke-default-action | 7 | 0 | 0 | 0 | overlay | invoke-default-action | 5 |
| notify-send | critical | do-not-disturb | Setup Wi-Fi | 0 | 0 | 0 | overlay | invoke-default-action | 7 | 0 | 0 | 0 | overlay | invoke-default-action | 5 |
| notify-send | critical | do-not-disturb | hello | 0 | 0 | 0 | overlay | invoke-default-action | 7 | 0 | 0 | 0 | overlay | invoke-default-action | 5 |
| Spotify | low | - | Setup Wi-Fi | 0 | 1 | 5000 | top | invoke-default-action | 7 | 0 | 1 | 5000 | top | invoke-default-action | 5 |
| Spotify | low | - | hello | 0 | 1 | 5000 | top | invoke-default-action | 7 | 0 | 1 | 5000 | top | invoke-default-action | 5 |
| Spotify | low | do-not-disturb | Setup Wi-Fi | 0 | 1 | 5000 | top | invoke-default-action | 7 | 0 | 1 | 5000 | top | invoke-default-action | 5 |
| Spotify | low | do-not-disturb | hello | 0 | 1 | 5000 | top | invoke-default-action | 7 | 0 | 1 | 5000 | top | invoke-default-action | 5 |
| Spotify | normal | - | Setup Wi-Fi | 0 | 1 | 5000 | top | invoke-default-action | 7 | 0 | 1 | 5000 | top | invoke-default-action | 5 |
| Spotify | normal | - | hello | 0 | 1 | 5000 | top | invoke-default-action | 7 | 0 | 1 | 5000 | top | invoke-default-action | 5 |
| Spotify | normal | do-not-disturb | Setup Wi-Fi | 0 | 1 | 5000 | top | invoke-default-action | 7 | 0 | 1 | 5000 | top | invoke-default-action | 5 |
| Spotify | normal | do-not-disturb | hello | 0 | 1 | 5000 | top | invoke-default-action | 7 | 0 | 1 | 5000 | top | invoke-default-action | 5 |
| Spotify | critical | - | Setup Wi-Fi | 0 | 1 | 0 | overlay | invoke-default-action | 7 | 0 | 1 | 0 | overlay | invoke-default-action | 5 |
| Spotify | critical | - | hello | 0 | 1 | 0 | overlay | invoke-default-action | 7 | 0 | 1 | 0 | overlay | invoke-default-action | 5 |
| Spotify | critical | do-not-disturb | Setup Wi-Fi | 0 | 1 | 0 | overlay | invoke-default-action | 7 | 0 | 1 | 0 | overlay | invoke-default-action | 5 |
| Spotify | critical | do-not-disturb | hello | 0 | 1 | 0 | overlay | invoke-default-action | 7 | 0 | 1 | 0 | overlay | invoke-default-action | 5 |
| firefox | low | - | Setup Wi-Fi | 0 | 0 | 5000 | top | invoke-default-action | 7 | 0 | 0 | 5000 | top | invoke-default-action | 5 |
| firefox | low | - | hello | 0 | 0 | 5000 | top | invoke-default-action | 7 | 0 | 0 | 5000 | top | invoke-default-action | 5 |
| firefox | low | do-not-disturb | Setup Wi-Fi | 0 | 0 | 5000 | top | invoke-default-action | 7 | 0 | 1 | 5000 | top | invoke-default-action | 5 |
| firefox | low | do-not-disturb | hello | 0 | 0 | 5000 | top | invoke-default-action | 7 | 0 | 1 | 5000 | top | invoke-default-action | 5 |
| firefox | normal | - | Setup Wi-Fi | 0 | 0 | 5000 | top | invoke-default-action | 7 | 0 | 0 | 5000 | top | invoke-default-action | 5 |
| firefox | normal | - | hello | 0 | 0 | 5000 | top | invoke-default-action | 7 | 0 | 0 | 5000 | top | invoke-default-action | 5 |
| firefox | normal | do-not-disturb | Setup Wi-Fi | 0 | 0 | 5000 | top | invoke-default-action | 7 | 0 | 1 | 5000 | top | invoke-default-action | 5 |
| firefox | normal | do-not-disturb | hello | 0 | 0 | 5000 | top | invoke-default-action | 7 | 0 | 1 | 5000 | top | invoke-default-action | 5 |
| firefox | critical | - | Setup Wi-Fi | 0 | 0 | 0 | overlay | invoke-default-action | 7 | 0 | 0 | 0 | overlay | invoke-default-action | 5 |
| firefox | critical | - | hello | 0 | 0 | 0 | overlay | invoke-default-action | 7 | 0 | 0 | 0 | overlay | invoke-default-action | 5 |
| firefox | critical | do-not-disturb | Setup Wi-Fi | 0 | 0 | 0 | overlay | invoke-default-action | 7 | 0 | 1 | 0 | overlay | invoke-default-action | 5 |
| firefox | critical | do-not-disturb | hello | 0 | 0 | 0 | overlay | invoke-default-action | 7 | 0 | 1 | 0 | overlay | invoke-default-action | 5 |

Stable facts across the whole grid: `on-button-left` = `invoke-default-action` in every run of every
tool; `default-timeout` 5000 and `layer` top except under `urgency=critical` (0 and overlay, both
tools); `include:` applied by both tools in all runs.

## Refusals (deduplicated over the 36 inputs)

Base tool (7 distinct; 7 per input):

- `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:15: invisible='true': expects 0 or 1`
- `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:18: invisible='false': expects 0 or 1`
- `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:24: criteria field 'summary~' is outside the model (refused)`
- `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:27: criteria field 'summary~' is outside the model (refused)`
- `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:30: criteria field 'summary~' is outside the model (refused)`
- `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:33: criteria field 'summary~' is outside the model (refused)`
- `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:36: criteria field 'summary~' is outside the model (refused)`

Candidate tool (5 distinct; 5 per input):

- `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:24: criteria field 'summary~' is outside the model (refused)`
- `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:27: criteria field 'summary~' is outside the model (refused)`
- `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:30: criteria field 'summary~' is outside the model (refused)`
- `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:33: criteria field 'summary~' is outside the model (refused)`
- `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:36: criteria field 'summary~' is outside the model (refused)`

`cand-bare` has the identical 5-refusal set, and the candidate and cand-bare effective values agree
on all 36 rows, so no refusal on this host is attributable to an input the candidate models but the
grid did not supply.

The candidate's set is a strict subset of the base's: `core.ini:15` and `core.ini:18` disappear.
Everything else — the five `summary~` criteria sections — is refused identically by both.

Because every base row has exactly 7 refusals and the union over the grid is exactly those 7, each
base row carries the full 7-set; likewise every candidate row carries the full 5-set. The dedup
lists are therefore also the per-input lists, not an over-approximation.

## Probes without notification inputs

Same host config, no `--app-name`, no `--urgency`, no `--mode` (the candidate probe supplies only the
fixed extra inputs: `--summary hello` plus body/category/desktop-entry/app-icon and the two false
booleans):

**base_no_inputs**: rc=0, refusals=9
  - `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:11: criteria needs --app-name to decide the match; section not applied`
  - `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:15: invisible='true': expects 0 or 1`
  - `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:18: invisible='false': expects 0 or 1`
  - `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:20: criteria needs --urgency to decide the match; section not applied`
  - `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:24: criteria field 'summary~' is outside the model (refused)`
  - `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:27: criteria field 'summary~' is outside the model (refused)`
  - `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:30: criteria field 'summary~' is outside the model (refused)`
  - `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:33: criteria field 'summary~' is outside the model (refused)`
  - `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:36: criteria field 'summary~' is outside the model (refused)`
**candidate_no_inputs**: rc=0, refusals=7
  - `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:11: criteria needs --app-name to decide the match; section not applied`
  - `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:20: criteria needs --urgency to decide the match; section not applied`
  - `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:24: criteria field 'summary~' is outside the model (refused)`
  - `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:27: criteria field 'summary~' is outside the model (refused)`
  - `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:30: criteria field 'summary~' is outside the model (refused)`
  - `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:33: criteria field 'summary~' is outside the model (refused)`
  - `/home/vgpnk/.local/share/omarchy/default/mako/core.ini:36: criteria field 'summary~' is outside the model (refused)`

Both add `core.ini:11` and `core.ini:20` ("criteria needs ... to decide the match; section not
applied"), i.e. those two sections are decidable only when their input is supplied. With
`--home` omitted entirely, both tools return exactly one refusal,
`/home/vgpnk/.config/omarchy/current/theme/mako.ini:1: include ~/ needs --home (no implicit HOME
fallback)` — the include chain, and with it the whole of `core.ini`, is then never read.

## Section-by-section coverage

| host section | option(s) | base | candidate | observable |
|---|---|---|---|---|
| `mako.ini:1` | `include=~/.local/share/omarchy/default/mako/core.ini` | read | read (containment: realpath inside `--home`) | `applied` contains `include:` in all runs |
| `mako.ini:3-5` | text/border/background colour | applied | applied | effective colours `#bebebe` / `#e68e0d` / `#121212` |
| `core.ini:1-9` | globals (anchor, group-by, default-timeout, width, margins, padding, border-size, max-icon-size, font) | applied | applied | `anchor=top-right`, `default-timeout=5000`, `max-icon-size=32`, `width`/margins in effective |
| `core.ini:11-12` | `[app-name=Spotify] invisible=1` | decided when `--app-name` given; refused ("needs --app-name") when not | same | Spotify rows `invisible=1`; probe refuses `:11` |
| `core.ini:14-15` | `[mode=do-not-disturb] invisible=true` | **not applied**: value refused at `:15` ("expects 0 or 1") | applied | firefox+DND: base 0, candidate 1 |
| `core.ini:17-18` | `[mode=do-not-disturb app-name=notify-send] invisible=false` | **not applied**: value refused at `:18` | applied | notify-send+DND: both 0, but base reaches 0 by refusing both lines |
| `core.ini:20-22` | `[urgency=critical] default-timeout=0 layer=overlay` | decided when `--urgency` given; refused ("needs --urgency") when not | same | critical rows 0 / overlay; probe refuses `:20` |
| `core.ini:24-25, 27-28, 30-31, 33-34, 36-38` | `[summary~="..."] on-button-left=...` (and `:37 max-icon-size=80`, `:38 format`) | **refused** (criteria field outside the model) | **refused** (same) | `on-button-left` stays `invoke-default-action` in all runs; `max-icon-size` stays 32 |

Nine criteria sections in `core.ini`. The candidate applies options in four (lines 11, 14, 17, 20 —
with inputs supplied); the base applies options in two (11, 20) and refuses the value lines of the
other two (14/15, 17/18). Both refuse the five `summary~` sections, which are the host's quick-action
buttons.

## do-not-disturb resolution (modes=[do-not-disturb])

| app-name | base `invisible` | candidate `invisible` | why |
|---|---|---|---|
| notify-send | 0 | 0 | `core.ini:14` sets true, `core.ini:17` sets false for this app; candidate applies both. Base refuses both lines and lands on the default 0 — same value, different path. |
| Spotify | 1 | 1 | `core.ini:11` sets 1; `core.ini:14` also sets true. `core.ini:17` does not match (app-name differs). Base gets 1 from `:11` alone. |
| firefox | **0** | **1** | only `core.ini:14` applies; base refuses its value. This is the only effective-value divergence in the grid (6 of 36 rows: firefox x DND x 3 urgencies x 2 summaries). |

Urgency does not change `invisible` (the `urgency=critical` section touches timeout/layer only), and
the summary axis changes nothing in either tool because `summary~` is refused before a value is used.

## Findings

1. **Base cannot resolve the host DND state.** `core.ini:15` writes `invisible=true` and
   `core.ini:18` writes `invisible=false`; the base resolver refuses both as "expects 0 or 1"
   (observed on every one of its 36 runs). A firefox notification under DND therefore resolves
   `invisible=0` under the base and `invisible=1` under the candidate. This is the coverage move the
   declaration describes, observed on the real config rather than on authored cases.
2. **Both tools miss the host's five quick-action sections.** `core.ini:24, 27, 30, 33, 36` use
   `summary~` (POSIX ERE), outside both models. Consequence visible in the grid: `on-button-left` is
   `invoke-default-action` for every input, and `core.ini:37 max-icon-size=80` is never applied
   (effective stays 32 from `core.ini:8`). `core.ini:38 format` coincides with the tool default, so
   that section's refusal is not observable in `format`.
3. **The host config exercises the boolean-grammar half of C1 only.** It contains no `app-icon`,
   exact `summary`, `body`, `category`, `desktop-entry`, `actionable` or `expiring` criteria, so the
   candidate with all five string inputs plus both booleans produces byte-identical stdout to
   cand-bare on all 36 rows (raw stdout compared byte-for-byte, 36/36 equal). The extended-field half
   of C1 is not evidenced by this host.
4. **`--home` is load-bearing for both tools.** `mako.ini:1` uses `~/`; without `--home` the include
   is refused ("no implicit HOME fallback") and nothing below `mako.ini` is read (1 refusal each).
5. **Containment accepts the host include.** The candidate's include target realpath lies inside
   `/home/vgpnk`, so the include is read; `include_applied` is true in all candidate runs. This config
   contains no escaping include, so it does not exercise the refusal branch — that is C2's case-file
   business, not this receipt's.

## Reproduce

Script (copied into this wave directory): `.ufo/waves/round-88/w1/R88MExecHostDiff-grid.py`,
sha256 `65c82f35e2ce338b56e5a69b4b31457566588c18082a888fbe0f1cdaafdea575`.

```
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/mado-r88/R88MExecHostDiff
mkdir -p "$S"
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show \
  24ba2a9ddac21c1211579231e6ee1d98963f9988:tools/mado-mako.py > "$S/base.py"
python3 -I .ufo/waves/round-88/w1/R88MExecHostDiff-grid.py \
  --base "$S/base.py" \
  --candidate /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-88/build/mado-mako.c2.py \
  --out "$S/grid.json"
```

Commands actually run and their exit codes: `git show ... > base.py` rc 0; `sha256sum` pins rc 0;
the grid driver rc 0 (36 rows, 3 tool invocations each, stderr empty); the raw candidate-vs-cand-bare
stdout comparison rc 0 (36/36 equal); the analysis one-liners rc 0. No counter was run.

## Limits / non-claims

- Measurement only. No c1/c2 counter was executed against a case file, and no candidate score is
  implied. Counter `--selftest` runs are outside this seat's item and were not performed.
- Semantic correctness of `true`/`false` as mako option booleans is declaration C1's sourced claim
  (S494); this receipt records what each tool resolves, not which resolution mako itself performs.
  The man page was not re-opened for this seat.
- One host, one config chain, one moment in time (2026-11-06). `~/.config/omarchy/current` is a real
  directory here; if it becomes a theme symlink the realpath pins above change.
- The base's 0 for notify-send+DND coincides with the candidate's; coincidence is not coverage.

## Scratch

`S=$HYAKU_SCRATCH/mado-r88/R88MExecHostDiff` (default `/fast/scratch/hyaku/mado-r88/R88MExecHostDiff`)
was used with `TMPDIR="$S"` and removed at exit; nothing from it survives except the two files copied
to this directory.

## Installs

None.
