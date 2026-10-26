# ExecLiveDryRun — w2 FALSIFY: the live receipt the round will land

**Verdict: the live capture and `explain --observed` AGREE on this host (rc 0), the capture's bytes are
stable and independently match w1's, the receipt shape passes the privacy gate with 0 findings — but the
w1 entry draft as written would FAIL C2 clause f on a mechanical placeholder fill, and four receipt-shape
mistakes are cheap to make. One counter gap (a capture of a different option triple) passes clause f.**

- Lane: `mado-shokunin`, round 47, wave w2 (falsify, policy v1)
- Frozen: `d7527d608ad2b2e3cc398fdde34db7947b254a1a` (base `60edb66e2f1cb90acc6e9442fc93ded0ca42d750`)
- Frozen bytes used (verified equal to the working tree by sha256):
  - `quality/counters/c2-r47-terminal-entry.py` = `cdd4c8460c7289cedab3f8c7426cf80065516d7d51df3ea56272e614bc6e9be5`
  - `quality/counters/c1-r47-terminal.py` = `2b9c2d0e35992d51ef2e83378db240877f8967be7235909931f24da8e0abf3f8`
  - `.ufo/waves/round-47/l1-draft/mado-terminal.py` = `762d042c96e7e5f2c3187133b0ffe670c1d076b698b958199602cfa019aa6c08`
- Seat dir (artifacts, untracked): `.ufo/waves/round-47/w2/ExecLiveDryRun/`

## 1. The live capture (read-only, print modes only)

Every invocation carried `XDG_CACHE_HOME=<scratch>/cache-cold` (fresh dir) and `TMPDIR=<scratch>`; no
launch, no compositor verb, no host write. Command:

```
XDG_CACHE_HOME=$S/cache-cold /usr/bin/xdg-terminal-exec --print-id --print-path --print-cmd > $S/capture.txt
```

stdout (84 B, rc=0, stderr empty), sha256 `9eb0a761e78db8b69a386536e2332cb4cb86275ca83c2eeb43a8721edae45cbc`:

```
Alacritty.desktop
/home/vgpnk/.local/share/applications/Alacritty.desktop
alacritty
```

- `sha256(/usr/bin/xdg-terminal-exec)` = `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac`
  = the pin and the C1 `PIN_SHA` entry.
- **Cross-seat agreement**: w1 `ExecLive` recorded the same sha for its base triple
  (`.ufo/waves/round-47/w1/ExecLive/receipts/live-host.txt`, "three repeats ... all sha256 =
  9eb0a761..."). My independent cold run and a warm-cache repeat reproduce it byte for byte
  (`capture-r47.txt` = `capture-warm.txt` = `print.out`; `cmp` clean).
- The printed path is the **user** copy while `/usr/share/applications/Alacritty.desktop` also exists
  (374 B, `ls -l`): the round-17 `[UNK]` **selection half** is answered — the user override wins. The
  launch half stays `[UNK]` and the entry already says so.
- The selecting list line is `~/.config/xdg-terminals.list:3` = `Alacritty.desktop`
  (`sed -n 3p`, list sha `d035da571a6bfc7d626d4a88846ea86a8adb6f6662f1f8b4abe2330e53ceb71b`, 3 lines —
  the same sha w1 recorded). The data-side list `/usr/share/xdg-terminal-exec/xdg-terminals.list`
  (25 lines = 7 comments, 3 blank, 11 `/`-directives, 4 `-<id>` fallback exclusions, and **0** plain
  entry lines), so only the user list is an entry source — supports the entry's "This host" claim.

## 2. `explain --observed` on that capture: MADO_TERM line, exit code, trace classes

```
python3 -I .ufo/waves/round-47/l1-draft/mado-terminal.py explain --observed $S/capture.txt
```

stdout (509 B, `explain.out`, sha256 `b97c39e86b47e39327d11ed8358c0b52c94e6500329fd976be13ac88b8d3ae61`),
**rc = 0**, stderr empty:

```
MADO_TERM_DESKTOPS: hyprland
MADO_TERM_TRACE: list /home/vgpnk/.config/xdg-terminals.list
MADO_TERM_TRACE:   /home/vgpnk/.config/xdg-terminals.list:3 entry Alacritty.desktop
MADO_TERM_TRACE: list /usr/share/xdg-terminal-exec/xdg-terminals.list
MADO_TERM_TRACE:   candidate Alacritty.desktop (listed) /home/vgpnk/.local/share/applications/./Alacritty.desktop: SELECTED
MADO_TERM: selected=Alacritty.desktop path=/home/vgpnk/.local/share/applications/Alacritty.desktop cmd=alacritty cache=present verdict=AGREE
```

Contract checks exercised on live bytes (all in the seat dir):

| run | rc | MADO_TERM tail |
|---|---|---|
| `explain` (no `--observed`) | 0 | `cache=present verdict=OK` |
| `explain --observed capture-r47.txt` | 0 | `cache=present verdict=AGREE` |
| same, fresh empty `XDG_CACHE_HOME` | 0 | `cache=absent verdict=AGREE` |
| same, repeated in the same env | 0 | byte-identical to the first run (`cmp` clean) |
| `--observed` with the id perturbed (`AlacrittyX.desktop`) | 1 | `verdict=DIFFER` |
| `--observed` with a 4th line (`--working-directory=/tmp`) | 1 | `verdict=DIFFER` |
| `--observed` in a bare env (empty XDG trees) | 1 | `selected=- path=- cmd=- cache=absent verdict=DIFFER` |

**Trace line classes.** The draft emits 9 classes (`trace-classes.txt`, locators computed by `grep -n`
in `.ufo/waves/round-47/l1-draft/mado-terminal.py`):

1. `list <path>: unreadable -> the resolver exits 1 (errexit)` (:441)
2. `list <path>` (:444)
3. `  <list>:<line> entry <line>` (:471)
4. `  <list>:<line> discarded <repr>` (:480)
5. `  candidate <id> (<tag>) <path>: rejected: <why>` (:662)
6. `  candidate <id> (<tag>) <path>: skipped: no Exec word` (:665)
7. `  candidate <id> (<tag>) <path>: skipped: not a TerminalEmulator` (:668)
8. `  candidate <id> (<tag>) <path>: skipped: no TerminalArgExec in strict mode` (:678)
9. `  candidate <id> (<tag>) <path>: SELECTED` (:680)

This receipt exercises only 2, 3 and 9 (with `<tag>` = `listed`) plus the `MADO_TERM_DESKTOPS` line; the
rejection/skip/unreadable/discarded classes are unexercised by a healthy host and must not be expected in
the receipt. The `<path>` in class 9 is the raw `find` path with the `/./` marker (the `MADO_TERM` `path=`
folds it) — copy it as printed if the receipt quotes the trace.

## 3. Session material: `~/.local/share/applications` under the gate's rules

`quality/check-session-material.py` has four rules (R1 clients dump, R2 socket table, R3 monitor identity,
R4 home listing = **more than 10 distinct lines that consist solely of an absolute `/home/<user>/...`
path**). A path sitting inside a sentence, a key=value line, or a `MADO_TERM:` line is never counted
(`HOME_PATH_RE` + "no whitespace in the line").

- The capture contributes exactly **1** bare home-path line
  (`/home/vgpnk/.local/share/applications/Alacritty.desktop`), 1 of 10 allowed → **not a finding**.
- Ran the gate on a fixture holding the proposed receipt **plus the verbatim explain trace** plus the
  capture (`gate-proposed.txt`): `SESSION_MATERIAL: files=2 findings=0`, rc 0.
- Positive control in the same fixture (a file of 11 distinct bare home paths, `gate-hostile-control.txt`):
  `FINDING ... rule=R4_HOME_LISTING count=11`, rc 1 — the gate discriminates, so the 0 is meaningful.
- **Verdict**: naming `~/.local/share/applications/Alacritty.desktop` is a single quoted path, allowed by
  the lane's shape-only rule and by the gate. 5004 tracked `.ufo` files already carry `/home/vgpnk`.
- **Caution (not a gate finding, a spirit finding)**: do not copy w1's whole `XDG_*` block. It includes
  `XDG_SESSION_ID`, `XDG_SEAT_PATH`, `XDG_RUNTIME_DIR`, `XDG_VTNR` — session identifiers the four gate
  rules do not detect. The receipt needs only the six variables the resolver reads (see §4).

## 4. C2 clause f, run by hand on the proposed receipt shape

Method: the **frozen** counter is imported (`importlib`) and its own `clause_f()` is called on a
throwaway git fixture (`base` empty commit → data commit) — no re-implementation, no lane write:

```
python3 -I .ufo/waves/round-47/w2/ExecLiveDryRun/clause-f-dryrun.py <scratch> matrix   # cases 0-6
python3 -I .ufo/waves/round-47/w2/ExecLiveDryRun/clause-f-dryrun.py <scratch> extra     # cases 7-8
python3 -I .ufo/waves/round-47/w2/ExecLiveDryRun/clause-f-dryrun.py <scratch> gaps      # cases 9-13
python3 -I .ufo/waves/round-47/w2/ExecLiveDryRun/clause-f-dryrun.py <scratch> emit      # proposed receipt
```

Entry text = the real `w1/ScrEntry/entry.md` with the `<LIVE:*>` tokens substituted
(`print-id`, `print-path`, `print-cmd`, `verdict=AGREE`, `live-receipt-r47.txt`, …). Receipt =
`proposed-receipt-r47.txt` (895 B); capture = `capture-r47.txt`.

| # | entry | receipt / capture | clause f | why |
|---|---|---|---|---|
| 0 | **mechanical fill** (draft as written) | good / good | **FAIL** `entry_line_does_not_state=Alacritty.desktop ~/.local/...` | see H1 |
| 1 | + line states id **and** tilde path | good / good | **PASS** | the shape to land |
| 2 | as 1 | `observed: <path>` (colon) | FAIL `receipt_no_observed` | line must be `observed=<path>` |
| 3 | as 1 | receipt 181 B | FAIL `receipt_short=...:181` | `MIN_RECEIPT=256` |
| 4 | as 1 | 2 `XDG_*=` lines | FAIL `env_lines=2` | needs >= 3 |
| 5 | as 1 | `observed=receipts/...` (not repo-relative) | FAIL `observed_missing_or_held` | `git show REV:.ufo/...` only |
| 6 | as 1 | states `kitty.desktop` | FAIL `entry_line_does_not_state` | contradiction caught |
| 7 | as 1 | `resolver_sha256=<16 hex>` | FAIL `receipt_no_resolver_sha` | full 64-hex digest line |
| 8 | as 1 | capture first line `Alacritty.desktop:New` | FAIL `observed_not_a_print_capture` | action suffix breaks `.desktop` |
| 9 | as 1 | receipt claims `XDG_CURRENT_DESKTOP=GNOME` | **PASS** | **H4 gap** |
| 10 | as 1 | capture has a 4th line `--working-directory=/tmp` | **PASS** | **H3 gap** |
| 11 | as 1, absolute `path` instead of `~/` | good / good | PASS | either form accepted |
| 12 | receipt cited in `receipts/c2/…` | good / good | FAIL `receipt_missing=.ufo/waves/round-47/receipts/c2` | **H2 trap** |
| 13 | as 1 | good / good | PASS | control for 9-12 |

C2 remains separable from C1: the only `subprocess` in the frozen counter is `git`
(`grep -n "subprocess\|mado-terminal" quality/counters/c2-r47-terminal-entry.py` → lines 157/162, and
line 73 is the docstring).

### Holes

**H1 — ROUND-BLOCKING (cheap to fix, no counter change needed): the w1 entry draft fails clause f on a
mechanical placeholder fill.** Clause f takes `cand` only from entry lines that name
`terminal-route-r17.md:144` (regex `terminal-route-r17\.md:144(?!\d)`), then requires **one of those
lines** to state the selected id and the path/`~/` form. In `w1/ScrEntry/entry.md` the two such lines
are the `ground:` line (:7) and "Reading the way round" (:68); both carry `<LIVE:verdict>` /
`<LIVE:live-receipt>` but **neither states the id or the path**. The live values sit in the table rows
(:63-:66), which do **not** cite `:144` and therefore never enter `cand`/`cited_lines`. Substituting
tokens only (what a fill-in pass does) yields case 0: `entry_line_does_not_state`.
Repro:

```
python3 -I .ufo/waves/round-47/w2/ExecLiveDryRun/clause-f-dryrun.py <scratch> matrix   # CASE 0
```
Fix (case 1 passes): on the `:144-145` sentence state both values, e.g.
`... answered by the live receipt `.ufo/waves/round-47/receipts/live-receipt-r47.txt`; the resolver
picks `Alacritty.desktop` at `~/.local/share/applications/Alacritty.desktop` there) ...`
(`clause-f-dryrun.py` `V2-states-id-and-path` is exactly this edit).

**H2 — trap: the receipt must sit directly under `.ufo/waves/round-47/receipts/`.** The citation regex
stops at `/` (`receipts/[A-Za-z0-9._-]+`), so a receipt cited as `receipts/c2/live-receipt-r47.txt`
yields `cand=['.ufo/waves/round-47/receipts/c2']` and clause f reports `receipt_missing` (case 12). The
freeze tree already has a `receipts/ctl-c2/` subdirectory, so this is an easy mistake. Put the C2
receipt at `receipts/<flat-name>.txt`; the `observed=` capture may live anywhere (`\S+`).

**H3 — gap: clause f accepts a capture of a *different* option triple.** Only `first[0]`/`first[1]` are
checked, so a real capture of `--print-id --print-path --print-cmd --dir=/tmp` (4 lines) passes (case 10)
even though `explain --observed` calls that same file **DIFFER** (rc 1, `explain-dir4.out`). The
counter's `OBS` control covers a *contradicting* capture, not a *different invocation* whose first two
lines agree. Cheap hardening if the L1 wants it in v2: require `len(first) == 4` (3 lines + trailing
empty) or `first[2]` non-empty and a `command:` line matching the recorded triple. Not a claim failure —
the id/path claim is still true — so I rate it low.

**H4 — gap: the receipt's `XDG_*` values are counted, not bound.** `XDG_CURRENT_DESKTOP=GNOME` in the
receipt passes while the capture came from a `Hyprland` run (case 9). Same hardening class as H3.

**H5 — shape constraints demonstrated, not guessed** (cases 2-5, 7-8): `observed=` is a bare
`key=value` line; `observed` is repo-relative; `resolver_sha256=` is the full 64-hex line; receipt
>= 256 B and mode 100644; >= 3 lines starting `XDG_[A-Z_]+=`; capture line 1 ends `.desktop` (an action
selection `id:action` breaks it) and line 2 starts `/`.

**H6 — contract wart in `explain --observed` (not round-impacting): an empty capture with no terminal
reports AGREE.** With a sanitized env the resolver exits 1 and prints nothing; `explain --observed` then
sets `mine = ""` and compares it to an empty file → `MADO_TERM: selected=- path=- cmd=- cache=absent
verdict=AGREE`, **rc 0** (`explain-bare-empty.out`). Defensible ("the three printed items are equal") but
it is an agreement with nothing selected. C2 clause f cannot be satisfied this way (it requires a
`.desktop` first line and an absolute path), and C1's fixtures always select. Worth a docstring sentence,
not a counter change.

**H7 — reproducibility wrinkle: the `cache=` field is env-dependent.** `explain` reports whether
`$XDG_CACHE_HOME/xdg-terminal-exec` exists *at explain time*, and the capture's own background
`--print-cmd` write creates it. Same capture, same host: with the capture's cache dir →
`cache=present`, with a fresh empty dir → `cache=absent` (both `verdict=AGREE`, rc 0;
`explain-freshcache.out`). Everything else is byte-stable (repeat run identical). The receipt must
record the `XDG_CACHE_HOME` used, or the non-author closure sees a different `MADO_TERM:` line while the
verdict still agrees. Do not read `cache=present` as "the capture used the cache".

**H8 — host-bound receipt (declared residual, restated with a live demonstration).** With empty XDG
trees the resolver exits 1, stdout empty (`bare.err`: "No valid terminal entry was found in: …"), and
`explain --observed <host capture>` → `selected=- … verdict=DIFFER`, rc 1 (`explain-bare.out`). So the
capture **must** be taken in this host's env, and a closure run in a sanitized sandbox (the C1 bwrap
allowlist has no `/home`, `/usr/share`, `/etc`) will not reproduce AGREE. Record the env in the receipt.

## 5. Proposed receipt shape (passes clause f, gate clean, AGREE rc 0)

`proposed-receipt-r47.txt` (895 B) — the parts clause f and the gate bind, in order:

```
resolver_sha256=89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac
command: xdg-terminal-exec --print-id --print-path --print-cmd
observed=.ufo/waves/round-47/receipts/live-capture-r47.txt
capture_sha256=9eb0a761e78db8b69a386536e2332cb4cb86275ca83c2eeb43a8721edae45cbc (stdout incl. trailing newline)
XDG_CURRENT_DESKTOP=Hyprland
XDG_CONFIG_HOME=/home/vgpnk/.config
XDG_CONFIG_DIRS=/etc/xdg
XDG_DATA_HOME=/home/vgpnk/.local/share
XDG_DATA_DIRS=/usr/local/share:/usr/share
XDG_CACHE_HOME=<scratch>/cache-cold (fresh, so the capture is a cold-cache run)
explain: MADO_TERM: selected=Alacritty.desktop path=/home/vgpnk/.local/share/applications/Alacritty.desktop cmd=alacritty cache=present verdict=AGREE (rc=0)
```

plus the capture as its own file (`capture-r47.txt`, 84 B) and, optionally, the verbatim explain stdout
(`explain.out`) — the gate stays at 0 findings with the trace embedded (`gate-proposed.txt`).

## 6. Tooling / safety

- No tool installed or upgraded; no pacman, no host-service call, no compositor verb, no launch.
- The resolver ran **only** with `--print-*`, always with `XDG_CACHE_HOME` inside scratch; the only file
  written on the host side was `<scratch>/cache-cold/xdg-terminal-exec` (188 B, copied to the seat dir as
  `scratch-cache.txt`; never a citable path).
- Fixture repos: `git init` under scratch, `rev-parse --show-toplevel` asserted equal to the fixture dir
  before the first commit; every later call names `-C <dir>`.
- Lane untouched (read-only git only: `git show`, `git ls-tree`, `sha256sum`); scratch removed at the end.

## 7. Risks

1. **H1 is the one to fix before data** — a fill-in pass alone scores clause f 0 and the round misses C2.
2. H2/H5 are silent-shape traps; the `emit` mode of `clause-f-dryrun.py` gives the L1 a passing receipt
   to compare against.
3. H3/H4 are counter gaps that a hostile entry could use; they do not make today's claim false.
4. The receipt is a host-state observation (user list + user entry + PATH); a closure must run here and
   with the recorded `XDG_CACHE_HOME`.

## 8. Seat-dir index

`capture-r47.txt` (84 B, sha 9eb0a761…) · `capture-warm.txt` · `capture-dir4.txt` · `capture-bad.txt` ·
`print.out` (identical to capture) · `explain.out` (sha b97c39e8…) · `explain-plain.out` ·
`explain-differ.out` · `explain-dir4.out` · `explain-freshcache.out` · `explain-repeat.out` ·
`explain-bare.out` · `explain-bare-empty.out` · `bare.err` · `scratch-cache.txt` ·
`trace-classes.txt` · `proposed-receipt-r47.txt` · `proposed-receipt-with-trace.txt` ·
`gate-proposed.txt` · `gate-hostile-control.txt` · `clause-f-dryrun.py` · `clause-f-dryrun.out` ·
`clause-f-dryrun-extra.out` · `clause-f-gaps.out` · empty stderr captures (`capture.err`, `print.err`,
`explain.err`)
