# R90MScribeEntry — round 90 w1 scribe (knowledge entry for C1, SKILL registry rows for D2)

Seat: R90MScribeEntry. Round mado 90, hyaku run 15 attempt 1, wave w1. Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`, base revision `5041acf99e27263872bf0441ad5f9d4316152605`
(`git -C <lane> rev-parse HEAD`, rc 0). Working tree at read time: untracked `.ufo/waves/round-90/`,
`quality/counters/c1-r90-portal-routing.py`, `quality/counters/c2-r90-receipt-presence.py` — observed, not
mine. Nothing in this report is a measurement of C1 or C2: every counter-shaped run below is labelled DRAFT
and none touched `.ufo/waves/round-90/receipts/`.

## 1. Files written (only these)

| path | lines | bytes | role |
|---|---|---|---|
| `.ufo/waves/round-90/w1/knowledge-draft-xdg-portal-routing-resolver-r90.md` | 358 | 29,822 | draft knowledge entry for C1, target `corpus/knowledge/xdg-portal-routing-resolver-r90.md` |
| `.ufo/waves/round-90/w1/skill-registry-rows-draft-r90.md` | 37 | 12,416 | ten draft `## Gate registry` rows for routed D2 |
| `.ufo/waves/round-90/w1/R90MScribeEntry.md` | this file | — | report |

No other file was created or modified. Both drafts pass a per-table column-consistency check (every row in
a table has the header's pipe count; checked with a script over both files — "inconsistent pipe counts:
none"). No table cell contains a literal pipe.

## 2. Behaviour — what the two drafts hold

### 2.1 Knowledge entry (C1)

Front matter is the round-89 header shape (`source:`, `covers:`, `verified-at:`, `recheck:`) with the source
ids the item named: S501 (xdp 1.22.1 tarball and the three files it cites), S502 (GLib 2.90.1
`glib/gkeyfile.c`), S503 (host `portals.conf.5.gz`). `verified-at` says DRAFT and why: no measured receipt
exists before the freeze. It is organised so every element the item demanded carries an upstream line cite:

| required element | where | upstream anchor |
|---|---|---|
| the 21 interfaces queried | §1 table | xdp-types.h:46-146 constants, xdp-context.c:354, :368, :385-417, plus each interface's own `xdp_portal_config_find` site |
| desktop parsing | §2 | xdp-portal-config.c:114-131, :133-158, :140-142, :147-153, :160-173, :623 |
| backend loading and sort | §3 | :329, :359-365, :367-384, :192-199, :201-236, :244-246, :335-339, :255-265, :267-296 |
| per-directory config selection and the directory order | §4.1 | :466-508, :476-488, :491-505, :411-413, :460, :527-536, :538-589 |
| none / star / interface-key / default | §4.2, §5 rows 1-9 | :645-675, :668-672, :742-773, :749-753, :755-762, :764-770, :869-870, :872-894 |
| Settings find-all | §4.3 | :779-821, :801, :804-808, :927-1004, :945-946, :954-962, :964-965, :969-996 |
| UseIn fallback | §4.2, §4.3 | :897-921, :969-993 |
| gtk last resort | §4.2 | :823-853 (DBusName match at :839-841, support test :843-844, absence :852-853) |
| the GKeyFile rules inherited | §4.4 | gkeyfile.c:843-848, :890, :1851-1895, :1625-1626, :1736-1741, :1755-1758, :1760, :1796, :4561-4564, :4647-4672, :4674-4690, :1638-1649, :4604-4641, :4692-4801, :4787-4791, :411-413 (the empty-group case is the caller's read, not GLib's) |
| decision table | §5 | 17 rows, each with an upstream cite and a DRAFT case id |
| error-signature table | §6 | 8 rows; three are the shapes the item named, two of them corrected by measurement (see F5) |
| host section, the 21 lines | §7 | verbatim run output, backends/configs line, six no-backend interfaces, comparison with round 12 |
| oracle method and limits | §8 | private activation-free bus, fixture HOME/XDG_RUNTIME_DIR, unreachable system bus, completion marker, the five parsed messages, six limits |

### 2.2 SKILL registry rows (D2)

Ten rows in the registry's own eight columns (`SKILL.md:791`): the six r87-r89 counters with their measured
commands, case/mutant sha256 pins and measured revisions taken from `SCORECARD.md` :5103, :5104, :5138,
:5139, :5177, :5178 and the round-87/88/89 declarations; plus `c1-r90-portal-routing.py`,
`c2-r90-receipt-presence.py`, `tools/mado-portals.py` (probe) and `quality/check-receipt-presence.py` (gate)
with `REV`/`BASE`/`DIR` placeholders and no invented digest. The r87 C1 row records its true measured verdict
(`TARGET_MISSED` at `00c96721`), not a pass.

## 3. Commands run and their exit codes

Every run below is either read-only or DRAFT. No pacman transaction, no service operation, no session-bus
call, no credential read.

| # | command (abridged) | rc | observation |
|---|---|---|---|
| 1 | `curl -fsSL codeload…/1.22.1` + `sha256sum` + `tar xzf` + `curl …/glib/2.90.1/glib/gkeyfile.c` + `sha256sum` | 0 | tarball `5afeda953c3743efaa1160e73d62c5bfcac2ceca60e0e134e9b48ed651783625` (equals the declaration's pin); `gkeyfile.c` `e1d1270f6c9881daf8a9f49b41395cbdd8e99fa290212e8530e0bd3df23ff656`; 1004 + 5111 lines |
| 2 | `sha256sum xdp-portal-config.c xdp-types.h xdp-context.c gkeyfile.c /usr/share/man/man5/portals.conf.5.gz /usr/lib/xdg-desktop-portal` | 0 | `2da4fd83…`, `6b38de15…`, `2c009356…`, `e1d1270f…`, `01eba9b4…`, `e1429fbe…` |
| 3 | `python3 .ufo/waves/round-90/build/mado-portals.c1.py` | 0 | one `MADO_PORTALS:` line (desktops=hyprland; backends=hyprland,gnome-keyring,gtk,kwallet; the same config path listed twice) and 21 `MADO_PORTAL:` lines; 15 resolved, 6 `none (no-backend)` |
| 4 | `python3 .ufo/waves/round-90/build/mado-portals.c1.py --selftest` (DRAFT) | 0 | `MADO_PORTALS_SELFTEST: checks=19 failed=0` |
| 5 | `python3 .ufo/waves/round-90/controls/portal-oracle-r90.py --cases two.json --label two-labelled.json --scratch-root … --jobs 2` (DRAFT) | 0 | `PORTAL_ORACLE cases=2 incomplete=0 host_tail_sha256=4a4cf319…` (s02, g03) |
| 6 | same oracle over the frozen 92-case file, then a field diff against the committed labels (DRAFT) | 0 | `PORTAL_ORACLE cases=92 incomplete=0`; diff: **0 mismatched interface rows in 0 cases**; same host tail digest `4a4cf31921e25dc6e60b283cc1aa1b79f743096bfdfc9dbb77df887c16f0fbf9` |
| 7 | ctypes `g_key_file_load_from_file` + `g_key_file_get_keys` + `g_key_file_get_string_list` on six scratch files (GLib 2.90.1) | 0 | A no final newline → `['gtk']`; B `hyprland;gtk␠␠` → `['hyprland','gtk  ']`; C `hyprland; gtk` → `['hyprland',' gtk']`; D empty `[preferred]` → `ok=1 keys=[]`; E concatenation without newline → one group, `['kde']`, two `default` entries; F tab after value → `['gtk\t']` |
| 8 | `pacman -Q xdg-desktop-portal glib2`, and `pacman -Q` filtered to the portal and glib packages (read-only queries) | 0 | `xdg-desktop-portal 1.22.1-2`, `glib2 2.90.1-1`, `lib32-glib2 2.90.1-1`, `xdg-desktop-portal-gtk 1.15.3-2`, `xdg-desktop-portal-hyprland 1.4.1-2` |
| 9 | `/usr/lib/xdg-desktop-portal --version` | 0 | `xdg-desktop-portal 1.22.1`. This is the binary outside the oracle, so it is reported explicitly: the fetched source's `src/xdp-main.c:174-179` returns from `main` at `--version` before `xdp_context_new` (:198) and before any bus connection, so no session bus was contacted; no other direct invocation was made |
| 10 | `zcat /usr/share/man/man5/portals.conf.5.gz` (reads) | 0 | SYNOPSIS (six search paths), DESCRIPTION (precedence list, desktop case-folding), FILE FORMAT (`default`, interface keys, `none`, `*`), ENVIRONMENT |
| 11 | `ls -d /etc/xdg-desktop-portal ~/.config/xdg-desktop-portal ~/.local/share/xdg-desktop-portal /usr/local/share/xdg-desktop-portal` | 2 (all absent) | the only portal root on this host is `/usr/share/xdg-desktop-portal` |
| 12 | `cat` of `hyprland-portals.conf`, `gtk-portals.conf`, `portals/{gtk,hyprland,gnome-keyring,kwallet}.portal` (reads) | 0 | `default=hyprland;gtk` **without a final newline**; gtk 11 interfaces, hyprland 4, gnome-keyring Secret, kwallet Secret |
| 13 | `git -C <lane> rev-parse HEAD`, `git status --porcelain` (read-only) | 0 | `5041acf9…`; untracked round-90 tree and the two r90 counters |
| 14 | table-column check over both drafts | 0 | no inconsistent row |

DRAFT labels used in the knowledge entry are the committed oracle labels (`oracle` and `oracle_reason` fields
of `controls/portal-cases-r90.json`), which run 6 reproduced without a single changed field. They are still
draft because the freeze has not happened; the entry says so in `verified-at`.

## 4. Findings

**F1 — the declaration's round-12 coverage sentence is wrong on two interfaces.**
`.ufo/waves/round-90/claims-declaration-r90.md:23-24` says the round-12 note "does not list Secret, Background,
Wallpaper, RemoteDesktop, Clipboard, Usb, Settings". It does list Settings (`corpus/knowledge/xdg-portal-routing-r12.md:61`)
and Secret (`:62`); its table has 16 rows (`:47-62`) and omits **five**: Background, Wallpaper, RemoteDesktop,
Clipboard, Usb. Reproducer: grep `corpus/knowledge/xdg-portal-routing-r12.md` for table rows (lines beginning with a pipe and a
backticked first cell) → 16 rows, none of the five. The draft entry states the corrected count and adds the five rows (all `none`).
Its Secret row's `[UNK]` is resolved to "no backend" with the mechanism (gnome-keyring's `UseIn=gnome` is not
in the desktop list, and gtk does not implement Secret): xdp-portal-config.c:897-921, :843-844.

**F2 — host answer set.** 21 interfaces: gtk 11, hyprland 4 (Screenshot, ScreenCast, GlobalShortcuts,
InputCapture), none 6 (Background, Wallpaper, Secret, RemoteDesktop, Clipboard, Usb). Reproducer: command 3;
full output in the draft entry §7.

**F3 — Settings `find_all`'s `UseIn` branch deduplicates upstream but not in the tool, and the oracle hides
it.** Upstream's fallback loop adds one entry per (desktop, backend) pair with no dedup
(`src/xdp-portal-config.c:969-993`; the config path above it does dedup at :804-808). The candidate dedups
(`.ufo/waves/round-90/build/mado-portals.c1.py:417-418`), and the oracle's Settings parser dedups
(`.ufo/waves/round-90/controls/portal-oracle-r90.py:175`), so the frozen label can never show the difference.
Reproducing shape: `XDG_CURRENT_DESKTOP=KDE:GNOME`, no config that names Settings, one `.portal` with
`Interfaces=org.freedesktop.impl.portal.Settings` and `UseIn=kde;gnome` — upstream adds it twice, tool and
oracle once. No case in the frozen set covers it. Recorded as an oracle limit (draft entry §8), not as a
counter defect; the L1 decides whether a case is worth adding (it would need an oracle that does not dedup).

**F4 — the Usb label cannot distinguish "not queried" from "no backend".** `init_usb` is compiled only under
`HAVE_GUDEV` (`src/xdp-context.c:414-416`), and a non-query leaves the same empty label as a `none` decision.
The host line `Usb -> none` therefore means "no backend, if Usb was queried at all". Reproducer: no fixture can
separate them; this is a limit of both the oracle and the tool's claim.

**F5 — the item's "missing final newline merges keys" example is not what upstream does to a single file.**
`g_key_file_load_from_fd` flushes the parse buffer at EOF (`glib/gkeyfile.c:890`), so a config without a final
newline is parsed completely. Measured three ways: ctypes file A → `['gtk']`; the frozen case `d01-host-replica`
carries `hyprland-portals.conf` = `"[preferred]\ndefault=hyprland;gtk"` with no newline and the oracle labels
FileChooser=gtk (`default config`) and Screenshot=hyprland; and this host's own
`/usr/share/xdg-desktop-portal/hyprland-portals.conf` has no final newline and resolves the same way. The merge
is real only when something concatenates two fragments without a newline (ctypes file E: one group, the second
`[group]` header swallowed, `get_string_list` → `['kde']`); xdp never concatenates (each path is its own
GKeyFile, `src/xdp-portal-config.c:404-409`). The entry keeps the row and labels it a fixture-construction
hazard.

**F6 — the host run lists the same config path twice.** `XDG_DATA_DIRS` ends with `/usr/share` and the build
`DATADIR` is `/usr/share`, so `load_portal_configurations` loads `/usr/share/xdg-desktop-portal` twice
(`src/xdp-portal-config.c:573-587`). Harmless: `find` answers on the first copy and `find_all` dedups
(:804-808). Stated in the entry so the `MADO_PORTALS:` line is not read as a tool defect.

**F7 — D2 confirmed.** `SKILL.md:860` is the last `mado-r86-*` registry row; there is no row for any r87, r88
or r89 counter, and none for the two r90 instruments. Reproducer: `grep -n 'mado-r8[7-9]\|mado-r90' SKILL.md`
→ only the round-89 *lesson* mentions, no registry rows. The draft rows are complete enough to paste; the L1
owns the edit.

**F8 — the seat item's row shape is a six-field paraphrase; the registry has eight columns.**
`SKILL.md:791` is `name | gate/probe | entry command | verdict map | self-test command / spelling |
pinned-value path | write scope | owner`. The draft rows use the registry's columns, not the paraphrase.

**F9 — the draft verdict tokens are `DRAFT_TARGET_MET` / `DRAFT_TARGET_MISSED`.**
`quality/counters/c1-r90-portal-routing.py:271-278` and `quality/counters/c2-r90-receipt-presence.py:161-168`
prefix `TARGET_MET`/`TARGET_MISSED` with `DRAFT_` and return 3; the registry rows say exactly that (an earlier
draft of the rows said `DRAFT_MET`/`DRAFT_MISSED` and was corrected before this report).

**F10 — the counter does not bind the labels to the installed oracle binary.** The label file records
`oracle_binary_sha256` (`controls/portal-cases-r90.json`, `e1429fbe1bf6c220…` = the installed
`/usr/lib/xdg-desktop-portal`), but the setup gate
(`quality/counters/c1-r90-portal-routing.py:226-230`) validates only the case and mutant sha256 pins, the
presence of labels, the host tail digest and the absence of `/etc/xdg-desktop-portal`. It never compares the
installed binary's digest with the recorded one. Reproducer: `grep -n "oracle_binary_sha256" quality/counters/c1-r90-portal-routing.py`
→ no match (the field exists only in the label file, written by the oracle's `main`). Consequence: labels from
one binary would be scored on a host running another binary with an unchanged `/usr/share` tail. The entry
records this in §8 as an oracle/label limit; whether to add the check is the L1's call (it is a one-line pin
in a draft counter).

## 5. Out of scope (not done, by instruction)

- No measurement: no counter was run in scoring mode, nothing was written under
  `.ufo/waves/round-90/receipts/`, and no draft run is called a measurement anywhere.
- No edits to `SKILL.md`, `quality/`, `tools/`, `corpus/`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md`, the
  declaration, the candidates, the controls, `.ufo/state/`, `.scratch/`, or any sibling lane.
- No mutating git or jj command; the only git verbs were `rev-parse`, `status --porcelain` and `show`-class
  reads. No subagent dispatch, no peer message.
- No installs: no pacman transaction (the guard is respected), no uv/npx/binary install. Nothing to record in
  the tool-install ledger.

## 6. Dead steps (with the observed text)

- `grep -n "if a.selftest" quality/counters/{r87..r89}*.py` → no match (the code says `if args.selftest:`).
  Recovered by reading each `main()`.
- `grep -n "org.freedesktop.impl.portal" src/xdp-context.c` → no match: the constants are in `xdp-types.h` and
  `xdp-context.c` only has the Lockdown and Access lookups. Recovered with `grep -rn "define .*_DBUS_IMPL_IFACE"`.
- `cat /usr/share/xdg-desktop-portal/*.portal` → `No such file or directory`; the descriptors are under
  `portals/`. Recovered with `ls`.
- `grep -rn SELFTEST` over the round-87/88/89 receipts → no per-counter selftest counts for these six; the
  registry rows therefore quote no count for them (the tool's own `MADO_MAKO_SELFTEST`-class line is printed at
  run time).

## 7. Limits of this report

- The upstream line numbers are read from the pinned tarball (`5afeda95…`) and the pinned `gkeyfile.c`
  (`e1d1270f…`); they are not re-verified against a packaged source tree, because the package ships only the
  binary. The tarball and `gkeyfile.c` were deleted with the scratch directory; they are re-obtainable from the
  URLs and sha256 values in the entry's `source:` line.
- The knowledge entry is a draft for the L1 to land after the freeze; its `verified-at` says so, and it carries
  no claim about the round-90 counter's verdict.
- The registry rows quote measured commands and revisions from `SCORECARD.md` and the declarations; I did not
  re-run those counters (not my item), so their verdicts are transcribed from the committed records, not
  re-measured here.

## 8. Scratch

`S=$HYAKU_SCRATCH/mado-r90/R90MScribeEntry` (`/fast/scratch/hyaku/mado-r90/R90MScribeEntry`), 6.6 MB at
deletion: the tarball and extracted tree, `gkeyfile.c`, six ctypes fixture files, and the oracle's label and
case directories. Deleted with `rm -rf -- "$S"` (rc 0); `ls -d "$S"` then exits 2 with
`No such file or directory`. The parent `/fast/scratch/hyaku/mado-r90` is left in place for the other seats.
No scratch remains on disk for this seat.
