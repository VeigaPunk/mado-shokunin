# R91MExecHost — host agreement: C1 candidate vs the live `gio mime`

Seat: leaf executor, host-agreement falsifier, round 91 / wave `w1`. Report path as dispatched:
`.ufo/waves/round-91/w1/R91MExecHost.md`.
**Status: DRAFT.** No freeze, no measurement, no receipt. Nothing under `receipts/` was written.

## 1. Environment, exactly as the tool saw it

```
XDG_CURRENT_DESKTOP=Hyprland
XDG_DATA_DIRS=/usr/local/share:/usr/share
XDG_CONFIG_DIRS=/etc/xdg
XDG_CONFIG_HOME=/home/vgpnk/.config
XDG_DATA_HOME=/home/vgpnk/.local/share
HOME=/home/vgpnk
PATH=/run/user/1000/fnm_multishells/1589455_1794007303555/bin:/home/vgpnk/.local/share/fnm:/home/vgpnk/.opencode/bin:/home/vgpnk/.local/bin:/home/vgpnk/.cargo/bin:/home/vgpnk/.local/share/mise/installs/node/latest/bin:/home/vgpnk/.local/share/mise/shims:/run/user/1000/fnm_multishells/1019894_1793962499190/bin:/home/vgpnk/.local/share/omarchy/bin:/run/user/1000/fnm_multishells/1556_1793632040352/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/opt/cuda/bin:/usr/lib/jvm/default/bin:/usr/bin/site_perl:/usr/bin/vendor_perl:/usr/bin/core_perl:/home/vgpnk/.minimax/bin:/home/vgpnk/.minimax-code/bin:/home/vgpnk/.grok/bin:/home/vgpnk/.kimi-code/bin
```

The tool's own view (its `MADO_MIME_DIRS` line, live run):

```
MADO_MIME_DIRS: desktops=hyprland config=/home/vgpnk/.config,/etc/xdg data=/home/vgpnk/.local/share/applications,/usr/local/share/applications,/usr/share/applications
```

Installed subjects (read-only `pacman -Q`): `glib2 2.90.1-1`, `shared-mime-info 2.5.1-2`, `desktop-file-utils 0.28-1`; `gio version` → `2.90.1`.

| object | path | sha256 |
|---|---|---|
| candidate | `.ufo/waves/round-91/build/mado-mime.c1.py` | `79645659c5a257e57c90ef4fb25d32bfb134b6f2ed03d3ead6788bdfbb1be160` |
| oracle | `/usr/bin/gio` | `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462` |
| oracle lib | `/usr/lib/libgio-2.0.so.0` → `libgio-2.0.so.0.9000.1` | `b38001cca69b2890a22fd3f6590bea7392bf489009de7ddfb6dbf296a133685e` |

gio and libgio hashes equal the declaration's pins.

## 2. Type census (step 1)

Keys (containing `/`) of `Default Applications` / `Added Associations` / `Removed Associations` / `MIME Cache`
in every file the seat item names, plus the left column of `/usr/share/mime/aliases` and `subclasses`:

| source | present | keys / left column |
|---|---|---|
| `~/.config/mimeapps.list` | yes | 56 |
| `~/.config/hyprland-mimeapps.list` (the `*-mimeapps.list` match) | yes | 1 |
| `/etc/xdg/*mimeapps.list` | **absent** | 0 |
| `~/.local/share/applications/{mimeapps.list,defaults.list}` | absent | 0 |
| `~/.local/share/applications/mimeinfo.cache` | yes | 149 |
| `/usr/local/share/applications/*` | directory absent | – |
| `/usr/share/applications/{mimeapps.list,defaults.list}` | absent | 0 |
| `/usr/share/applications/mimeinfo.cache` | yes | 522 |
| `/usr/share/mime/aliases` | yes | 357 lines, 357 distinct |
| `/usr/share/mime/subclasses` | yes | 629 lines, 589 distinct children |

**1211 unique types, 42 of them `x-scheme-handler/…`.**
The live config is thin: 57 config-file keys (56 nvim/imv/mpv/chromium/Evince/Nautilus plus the tool-chain schemes, and one
`x-scheme-handler/zcode` in the per-desktop file); everything else is cache-, alias- or subclass-derived.

## 3. Method

- Candidate, live environment, one process: `python3 -I <candidate> --json <all 1211 types>` (the resolver is built once
  from the same environment; per-type answers are identical to per-type invocations of the same code path).
- Oracle: 1211 separate invocations `gio mime TYPE` — **one argument only**, never the write form — inheriting the live
  environment.
- Compared field by field: `default`, `registered` (order-sensitive), `recommended` (order-sensitive).
- Two full runs for determinism; the second run produced **0 changed fields**.

## 4. Result (step 2)

```
types=1211   agree=1089   print-shape=122   semantic DIFF=0   types_with_default=1089
```

Full table (totals at its top, one row per type with both answers):
`.ufo/waves/round-91/w1/R91MExecHost-diff.txt`, sha256 `ce2cba283eeaf395db6abcbb1400e04d634d8f15b133da3a3cc253c326c3d64a`, 1211 data rows.

**The 122 `DIFF` rows are one benign print-level class**, not a disagreement: for a type with no handler at all, `gio`
prints only `No default applications for “…”` and elides the lists (`gio/gio-tool-mime.c` prints `Registered`/
`Recommended` only after a default), while the candidate answers `default=none` plus two empty lists. All 122 have
`default=null` on both sides **and empty candidate lists** — there is no type where the candidate invents a handler.
The counter's `correct()` ignores the lists when the label default is null, so this class cannot consume a case. The
table marks them `DIFF`/`list-elision` to keep the print-level honesty; `semantic_DIFF=0` counts the real ones.

Representative agreeing rows (both sides identical, order included):

```
text/plain        default=nvim.desktop          registered=libreoffice-writer.desktop,nvim.desktop  recommended=same
text/x-csrc       default=nvim.desktop          registered=nvim.desktop,libreoffice-writer.desktop  recommended=nvim.desktop
inode/directory   default=org.gnome.Nautilus.desktop  registered=recommended=that id
x-scheme-handler/mailto  default=HEY.desktop    registered=recommended=HEY.desktop
```

## 5. Evidence that the agreement is not just the default column

| probe | count | result |
|---|---|---|
| types whose `registered` list has ≥2 ids (order matters) | 696 | all equal, order included |
| types where `registered != recommended` | 611 | all equal |
| types where the default is **not** the first registered id | 347 | all equal |
| alias pairs (`/usr/share/mime/aliases`) whose canonical type has a default | 262 | alias and canonical default identical on both sides |
| types named **only** in `aliases`/`subclasses` (not in any mimeapps/cache) that resolve a default equal to a subclass parent's default | 360 | all equal (parent fallback reproduced) |
| rows with a default but empty lists (`x-scheme-handler/about`, `x-scheme-handler/unknown` → `chromium.desktop`) | 2 | equal |

Two live-environment sensitivity probes, each checked on both sides:

- `PATH=/usr/bin:/bin` instead of the live PATH changes **3** candidate answers
  (`x-scheme-handler/mailto`, `x-scheme-handler/zoommtg`, `x-scheme-handler/zoomus` → no default; the handlers
  `omarchy-webapp-handler-hey` / `-zoom` live in `~/.local/share/omarchy/bin`, which the reduced PATH omits).
  `env PATH=/usr/bin:/bin gio mime` on the same three types also prints `No default applications`. Same rule, same answer.
- `XDG_CURRENT_DESKTOP` unset changes **1** candidate answer (`x-scheme-handler/zcode`: the per-desktop
  `hyprland-mimeapps.list` default beats the `[Default Applications]` fallback of `zcode.desktop`); `env -u
  XDG_CURRENT_DESKTOP gio mime x-scheme-handler/zcode` prints `zcode.desktop`. Same precedence, same answer.

DRAFT side-check: `python3 -I <candidate> --selftest` → `MADO_MIME_SELFTEST: checks=17 failed=0`, rc 0.

## 6. Cases (step 3) — `controls/mime-cases-r91-hx.json`

File written (mine), sha256 `1739ecc394adbd93f122e091ead267d5cf6ed1f12c60fb4ddef2d2d0a9531394`, oracle-labelled
(`MIME_ORACLE: cases=1 types=1 … changed=0`, rc 0).

- `hx-01` — the reduction of all 122 print-level DIFFs: an empty fixture (no desktop files, empty `aliases`/
  `subclasses`) and the type `application/x-hx-nohandler`. Raw evidence:
  `gio` → `No default applications for “application/x-hx-nohandler”`; candidate on the same fixture →
  `{"default": null, "registered": [], "recommended": []}`.
- The case's label is `{default: null, registered: null, recommended: null}` because gio prints no lists; **it therefore
  cannot discriminate** — the do-nothing control passes it. The file's `note` says so and invites the L1 to drop it.
  No other case was contributed because there was nothing else to reproduce.

## 7. Limits and risks

1. **No semantic disagreement exists on this host**, so this seat cannot produce a falsifying case; the falsifiers that
   can are fixture-shaped (L1 case set, blind and fuzz seats), not live-host-shaped.
2. **The oracle's read form cannot verify `registered`/`recommended` for a no-default type.** The candidate's empty
   lists there are *consistent* with "no handler anywhere" (all 122) but unverified by gio. Any battery case whose label
   default is null is passed by an answer that reports junk lists — a discrimination limit of the case shape, not a
   candidate defect.
3. **Answers are PATH-bound**: 3 of 1211 answers move with PATH, and gio moves with them. The comparison is valid only
   for the PATH recorded in §1; a battery run under a different PATH (the counter passes the case's own PATH) is a
   different question and must stay fixture-local.
4. Census scope: types that exist only inside `/usr/share/mime/mime.cache` and appear neither in the named config files
   nor in the left column of `aliases`/`subclasses` are outside this seat's set (the item names the text files). The
   tool does read both caches (`~/.local/share/mime/mime.cache`, `/usr/share/mime/mime.cache`).
5. **Declaration gap**: the DRAFT's case-family list is `bl-`, `fz-`, `mc-`, `rv-`, `sh-`; `hx-` (this seat's item) is
   not named. The L1 must add it in the freeze text or fold `hx-` into the seat-finding families.
6. One table row names an oauth-callback desktop id; per the credential-material rule its hex suffix is redacted to
   `dev.omp.oauth-callback.<redacted>.desktop` in the table (the desktop file itself was never opened, and no config
   file content other than keys was inspected).

## 8. Commands run (exit codes)

| command | rc |
|---|---|
| `python3 -I collect.py` (census, live host) | 0 |
| `python3 -I compare.py` (candidate vs 1211 `gio mime TYPE`) — run twice | 0, 0 |
| `python3 -I table.py` → `w1/R91MExecHost-diff.txt` | 0 |
| `python3 -I mime-oracle-r91.py --cases hx-src.json --label hx-labelled.json` | 0 |
| `python3 -I mado-mime.c1.py --selftest` (DRAFT) | 0 |
| `env -i … gio mime application/x-hx-nohandler` / `env -i … candidate … --desktop-unset -- application/x-hx-nohandler` | 0, 0 |
| `env PATH=/usr/bin:/bin gio mime …` (3 types), `env -u XDG_CURRENT_DESKTOP gio mime x-scheme-handler/zcode` | 0 |
| `pacman -Q glib2 shared-mime-info desktop-file-utils`, `gio version` | 0 |

No counter run (no `--draft-tool` invocation) — scoring belongs to the L1. No install performed; `~/.omp/agent/RULES.md`
is not present at that path. No `gio mime` two-argument form, no `xdg-mime`/`xdg-settings`/`update-desktop-database`, no
application launched, no pacman transaction.

## 9. Files written

- `.ufo/waves/round-91/w1/R91MExecHost-diff.txt` — full diff table (new)
- `.ufo/waves/round-91/w1/R91MExecHost.md` — this report (new)
- `.ufo/waves/round-91/controls/mime-cases-r91-hx.json` — one oracle-labelled case (new, mine)

Scratch `$HYAKU_SCRATCH/mado-r91/R91MExecHost` is removed on exit.
