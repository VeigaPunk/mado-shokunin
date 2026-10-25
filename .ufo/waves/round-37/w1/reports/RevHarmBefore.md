# RevHarmBefore — harm-watch baseline (before side), mado round 37 wave 1

Seat: reviewer, read-only. Date 2026-10-25.

## Verdict

**PASS. The baseline was captured, with one finding.** Every item the assignment names was run and exited cleanly. One exception: `check-index.py` and `check-index-rows.py`, run exactly as the prompt words them, exit 2 because they require `--rev` or `--root`. I reran both with `--rev master`, the same revision `check-axis-scores.py` uses, and both pass. The after-side seat MUST use the same flags, or its comparison will show a spurious change.

## Tree state at capture

- `git rev-parse HEAD master` → both `80b83c856b8cad60b88e63d8d3ab06b1d8dfea5b`.
- `git status --porcelain | wc -l` → `0`. The working tree is clean, so `--rev master` reads the same bytes as the checkout.
- The freeze commit `893a8aadc80ab19bc163e366d674a8ac32feacd0` is an ancestor of HEAD (`git merge-base --is-ancestor` → `ANCESTOR_EXIT=0`). One commit follows it: `80b83c8 round-37: the inherited round-36 DistillerFindings seat report (spot-check R1), and the wave-1 spec, prompts, dispatch and registry (38 seats)`. It changes 43 files (+1366 lines).
- Production paths are untouched since the freeze. `git diff --name-only 893a8aa HEAD | grep -vc '^\.ufo/'` → `NONUFO_COUNT=0`. `git diff --quiet 893a8aa HEAD -- tools quality corpus` → exit `0`.

## Items

| # | Command (cwd = lane root) | Summary line(s) | Exit | Verdict |
|---|---|---|---|---|
| 1 | `bash tools/mado-verify.sh --selftest` | `MADO_SELFTEST: 460/460 assertions passed` | 0 | PASS |
| 2 | `sha256sum tools/mado-verify.sh` | `050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1  tools/mado-verify.sh` | 0 | baseline |
| 3a | `python3 -I quality/check-index.py --repo .` (exactly as written) | `SETUP_ERROR: --rev or --root is required` | 2 | FINDING: impossible as written |
| 3b | `python3 -I quality/check-index.py --repo . --rev master` | `MADO_INDEX: rev=master indexed=50/50 missing=0 dangling=0 duplicates=0 coverage=10.0000/10` | 0 | PASS |
| 4a | `python3 -I quality/check-index-rows.py --repo .` (exactly as written) | `SETUP_ERROR: --rev or --root is required` | 2 | FINDING: impossible as written |
| 4b | `python3 -I quality/check-index-rows.py --repo . --rev master` | `MADO_INDEX_ROWS: rev=master rows=50 errors=0 warns=3` | 0 | PASS (3 warnings, listed below) |
| 5 | `python3 -I quality/check-axis-scores.py --repo . --rev master` | `MADO_AXIS: checked=3 mismatched=0 rev=80b83c856b8cad60b88e63d8d3ab06b1d8dfea5b` | 0 | PASS |
| 6 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | `mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` (8 lines: 1 `ok`, 7 `W04`) | 0 | PASS (7 warnings, listed below) |
| 7 | `sha256sum ~/.config/hypr/*.conf ~/.config/waybar/config.jsonc ~/.config/waybar/style.css` | 15 files (13 hypr + 2 waybar); combined digest of the listing `89e214b8c942c705c550b6868569b9943d37cf9d159c2757fc5bdce1f8ac3195` | 0 | baseline |
| 8 | `coredumpctl list --no-pager 2>/dev/null \| grep -ci hyprland` | `0` | grep 1 (no match); `coredumpctl` itself exit 0 | PASS: 0 Hyprland coredumps |

### Item 1 detail

The whole selftest output is a single line: `MADO_SELFTEST: 460/460 assertions passed`. Wall time was 13.27 s.

### Items 3 and 4: why they fail as written

The usage text explains it. `check-index.py --help` prints `usage: check-index.py [-h] [--rev REV] [--repo REPO] [--root ROOT] [--selftest]`, with `--repo REPO  git repo for --rev mode`. `check-index-rows.py` has the same usage. Passing `--repo .` alone selects no tree, so the gates fail at setup and never evaluate anything. The prompt omits `--rev master`, which item 5 already uses. Because the tree is clean, `--root .` should give the same result `[INFERENCE: not run]`.

The 3 warnings from the index-rows gate (4b), verbatim:

```
WARN cited-glob-nomatch: `.ufo/evidence/round-12/getprop-*.txt` in row knowledge/window-rule-effects-getprop.md
WARN cited-glob-nomatch: `.ufo/evidence/round-12/drift-*.txt` in row knowledge/config-drift-r12.md
WARN cited-glob-nomatch: `.ufo/waves/round-24/fetch/S###.bin` in row knowledge/rule-attribution-r24.md
```

### Item 5 detail

```
MADO_AXIS_ROW: axis=navigation published=50/50 derived=50/50 verdict=MATCH
MADO_AXIS_ROW: axis=calibration published=48/48 derived=48/48 verdict=MATCH
MADO_AXIS_ROW: axis=operability published=12/12 derived=12/12 verdict=MATCH
MADO_AXIS: checked=3 mismatched=0 rev=80b83c856b8cad60b88e63d8d3ab06b1d8dfea5b
```

### Item 6 detail

The full output is 8 lines; its sha256 is `abac25cbfda99920bba3d5275b4586743694347aa95c6ad77c2d91932dd585e1`. A tally of the second column (`cut -f2 | sort | uniq -c`) gives `1 ok`, `7 W04`. The W04 warnings:

```
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
mado	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
mado	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
```

### Item 7 detail (per-file sha256)

```
21e76af98ce791fa829b99d41a51014ec910a9db602e5a9806da233350ad423e  /home/vgpnk/.config/hypr/ai-usage.conf
5ace17016fe2998aa6e7ad2221c1889b430aa4b94faf5ef1f907d6301dd5fc46  /home/vgpnk/.config/hypr/autostart.conf
e574a1ed08535e31deeafe2a26432c6862bb101e8c45d5a6b3f997d7dc810581  /home/vgpnk/.config/hypr/bindings.conf
04af5cdf028bf48897a5cebe77c720d4352925e159f7c2f8c7484396f1be9c49  /home/vgpnk/.config/hypr/envs.conf
3726e488c0bf93028f1bba11017cf02d26da6dc3604362815bc4f3738b8e9949  /home/vgpnk/.config/hypr/gkeep.conf
e7d3b8dd983523e4defbfbacfd7ed73fc55407e175766bf44542e5708307de41  /home/vgpnk/.config/hypr/hypridle.conf
ce7483f35ab52bc28e3020a6fb0ac14b2e02de5817abe827ef8452a0190f8365  /home/vgpnk/.config/hypr/hyprland.conf
b8d173dcff5582873a448652e9f77273d447a4709dd40e4cf9268f0827968fc1  /home/vgpnk/.config/hypr/hyprlock.conf
3042e4a923030239f4edf7b1943f41f4ed57107550177130c96f3b215b226e22  /home/vgpnk/.config/hypr/hyprsunset.conf
3769c92ab7660f1795cb6d0af1bcc5a5614a299b29ae8358d1b85936bdd47bf4  /home/vgpnk/.config/hypr/input.conf
777a4fdc8b61db4419c3392d43fbb549ceb868bf8eaa84d9bf278d6e40a8c1ea  /home/vgpnk/.config/hypr/looknfeel.conf
69c9d8996dfdcd6747775e984a479c53a520bd2ef193d337e171927fdf6795ee  /home/vgpnk/.config/hypr/monitors.conf
2fded88a27b89f33cbc2b64a1258117df74b591f39a84c78ec3504a7d3b09136  /home/vgpnk/.config/hypr/xdph.conf
a408a33df48a39dc16214124dd0b86d6ab03e13802bac173146ae8a858aae829  /home/vgpnk/.config/waybar/config.jsonc
8f335ca01da53d32eb968c2f7752f3149f073e8e56411980913f4dd25d385fdf  /home/vgpnk/.config/waybar/style.css
```

Combined digest: `sha256sum <the 15 files> | sha256sum` → `89e214b8c942c705c550b6868569b9943d37cf9d159c2757fc5bdce1f8ac3195  -`. The glob matches 13 hypr `.conf` files (`ls ~/.config/hypr/*.conf | wc -l` → `13`).

### Item 8 detail

`coredumpctl list --no-pager >/dev/null` → `COREDUMPCTL_EXIT=0` with empty stderr, so the zero count comes from a working tool, not a hidden error. The list has 96 lines; none match `hyprland` (case-insensitive). I printed no coredump rows, per the privacy rule.

## Residual risk and verification gaps

- **Command-wording risk (items 3 and 4).** If the after-side runs the prompt's literal commands, both gates exit 2 and the no-harm comparison breaks. It needs `--rev master` (or `--root .` on a clean tree).
- **Pre-existing warnings.** The 3 index-rows warnings and 7 census W04 warnings exist before any round-37 work. A no-harm check should compare counts (warns=3, W04=7) rather than require zero.
- **Glob scope.** Item 7 hashes only the listed paths. Files Hyprland or Waybar `source` from elsewhere (theme includes outside `~/.config/hypr/*.conf`) are not covered `[INFERENCE: includes not enumerated]`.
- **Live host read once.** Hyprland was not queried (no `hyprctl`, no socket), so the item list does not cover compositor runtime state.

## Writes and tooling

- Writes: this report, plus scratch captures `/dev/shm/mado37-RevHarmBefore-selftest.txt`, `/dev/shm/mado37-RevHarmBefore-census.txt` and `/dev/shm/mado37-RevHarmBefore-cd.err`. No lane production file, git or jj state, config, service or socket was touched.
- Tool installs or updates: none.
