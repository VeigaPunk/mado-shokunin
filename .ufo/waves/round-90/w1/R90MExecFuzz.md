# R90MExecFuzz — differential fuzz of the C1 candidate against the oracle

**DRAFT — pre-freeze.** Every oracle label in this report is a draft label taken before the L1
freezes the round. Nothing here is a measurement, no `receipts/` file was written, and no
`--draft-tool`/`--draft-check` run is claimed as a verdict. The L1 owns integration.

- Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin` — base `5041acf99e27263872bf0441ad5f9d4316152605`.
- Seat: `R90MExecFuzz` (leaf; no spawns, no peer messages, no fleet-root writes).
- Claim under test: **C1 coverage** — the resolver candidate
  `build/mado-portals.c1.py` against the oracle `controls/portal-oracle-r90.py`.
- Date: 2026-11-06. Host: xdg-desktop-portal **1.22.1-2**, glib2 **2.90.1-1**.

## 1. Method

`w1/fuzz-r90.py` is one seeded script: generate fixtures → write the case file → label it with
the oracle (`--jobs 8`) → run the candidate through its CLI for each case → compare per interface
**picks and reason** → minimise disagreements.

### Generator vocabulary (seeded, `random.Random(seed)`)

- **Descriptors**: the four host descriptors under `/usr/share/xdg-desktop-portal/portals`
  (`gtk`, `hyprland`, `gnome-keyring`, `kwallet`) copied verbatim, plus synthetic `*.portal`
  files with random `DBusName` (valid portal names, `org.freedesktop.secrets`, example names,
  and invalid forms such as `org`, `org..a`, `org.1a.b`), random `Interfaces` (0–6 of the 21
  `org.freedesktop.impl.portal.*` names, plus short/foreign/escaped entries), and random
  `UseIn` (0–4 desktop tokens, case variants, trailing `;`, invalid tokens, escaped separators,
  `\q`, trailing `\`, empty, absent). Styles also produce missing `DBusName`/`Interfaces`,
  `[Portal]`, duplicate `DBusName`, comments, CRLF.
- **Configs**: `default` and interface keys drawn from backend sources, `none`, `*`, unknown
  names, empty, and case variants; random `=`/` = `/` =\t` spacing; leading/trailing spaces;
  `\s`/`\;`/`\\`/`\q`/trailing-`\` escapes; comments, blank lines, keys before a group, bare
  garbage lines, duplicate keys, duplicate `[preferred]` groups, `[other]`, CRLF, no final
  newline. Files are `<desktop>-portals.conf`, `portals.conf`, or absent.
- **Desktops**: `Hyprland`, `KDE`, `GNOME`, `sway`, `XFCE`, `''` and absent, joined with `:`
  and interleaved with invalid tokens (`bad/val`, `Hypr.land`, `My.Desk`, `x.y`, `a b`, spaces,
  empty tokens), plus uppercase/lowercase variants.
- **Modes**: `dir` (`XDG_DESKTOP_PORTAL_DIR`, all files in one fixture dir) and `xdg`
  (config_home / config_dirs/`n` / data_home / data_dirs/`n`, with the host `/usr/share` tail
  and `/etc` appended by the compiled defaults, exactly as the oracle does).

The candidate is invoked as `python3 -I build/mado-portals.c1.py --json` with
`--portal-dir` in dir mode, or
`--config-home --config-dirs --data-home --data-dirs --sysconfdir /etc --datadir /usr/share`
in xdg mode, and `--desktop <value>` / `--desktop-unset`; its environment is minimal and
contains no `XDG_*` variables. Every fixture root and oracle scratch root is under
`$HYAKU_SCRATCH/mado-r90/R90MExecFuzz` (default `/fast/scratch/hyaku`).

**Verdict rule.** An interface disagrees when the oracle picks and the candidate picks differ,
or when both are `[]` but the oracle has a decision reason and the candidate's reason differs.
The oracle prints no decision line when it selects no backend, so oracle `[]` + no reason
accepts candidate reasons `none-key` and `no-backend` (per the seat item).

## 2. Runs (draft labels; incomplete = 0 everywhere)

| seed | cases | labelled | incomplete | agreed | disagreed | clean? | wall |
|---|---|---|---|---|---|---|---|
| 900150031 | 480 | 480 | 0 | 471 | 9 | no | 23.6 s |
| 900150032 | 400 | 400 | 0 | 393 | 7 | no | — |
| 900150033 | 400 | 400 | 0 | 392 | 8 | no | — |
| 900150034 | 400 | 400 | 0 | 400 | 0 | yes | 22.4 s |
| **total** | **1680** | **1680** | **0** | **1656** | **24** | | |

(`—` = wall not separately captured; the two runs shared one background shell.)
`clean` = `--clean`, which removes the two descriptor styles whose `UseIn` does not unescape.
The primary seed was re-run after the first pass: identical counts (480/480, 471/9) and `rc=0`.

Oracle banner for every batch:
`PORTAL_ORACLE cases=<N> incomplete=0 host_tail_sha256=4a4cf31921e25dc6e60b283cc1aa1b79f743096bfdfc9dbb77df887c16f0fbf9`
(this is the digest pinned in the declaration). `xdg-desktop-portal` binary digest:
`e1429fbe1bf6c2203ba07f478b9e92e9221437b13a92eebafb0982748583a4f8`.

## 3. Finding — one defect class, 24/24 disagreements

**Candidate defect.** `build/mado-portals.c1.py:277-280` reads `UseIn` with
`string_list(g["UseIn"])` inside the all-or-nothing `try`. When the value fails GKeyFile
unescaping (`UseIn=kde\q`, `UseIn=kde\` at end of value), `KeyFileError` is caught and the
**whole descriptor is dropped**.

**Upstream behaviour.** `xdg-desktop-portal-1.22.1/src/xdp-portal-config.c:244-249` obtains
`UseIn` with `g_key_file_get_string_list (keyfile, "portal", "UseIn", NULL, error)` and
**does not inspect the error**: `impl_config->use_in` becomes NULL and
`g_hash_table_insert (portals, ...)` still registers the backend. GLib itself sets an
invalid-value error at `glib/gkeyfile.c:4761` (tag 2.90.1), so the list is unparsable — the
portal simply loses its `UseIn` list.

Two observable consequences, both exercised:

1. **Name/config/`*` selection** loses a backend the oracle still has.
   `f22` (`dir`, desktop `XFCE`):
   `beta.portal` = `Interfaces=…Access;`, `UseIn=kde\`; `xfce-portals.conf` =
   `default =\tnone;None;` then `default = lambda;beta` (last default wins → `lambda;beta`).
   Oracle: `Access -> ["beta"] (default config)`; candidate: `Access -> [] (no-backend)`.
   Same shape in `f03`, `f09`, `f10`, `f12`, `f14`, `f17`, `f18`, `f20`, `f21`, `f24`
   (11/24 entries; dir and xdg modes).
2. **Host-tail shadowing.** A descriptor with a host source and a broken `UseIn` still
   suppresses the later `/usr/share` copy of the same source
   (`src/xdp-portal-config.c:195-199` duplicate-source skip; load order
   `src/xdp-portal-config.c:358-384`, `DATADIR` last). The candidate skips the broken
   descriptor, so the host copy loads and its `UseIn`/gtk-last-resort decisions reappear.
   `f02` (`xdg`, desktop `GNOME:\t:xfce`): one file,
   `data_dirs/1/xdg-desktop-portal/portals/gnome-keyring.portal` =
   `Interfaces=DynamicLauncher;InputCapture;GlobalShortcuts;Background` (no `Secret`),
   `UseIn=kde\q`. Oracle shadows host `gnome-keyring.portal`:
   `Secret -> []` (no line); candidate loads host `gnome-keyring` (`UseIn=gnome`):
   `Secret -> ["gnome-keyring"] (usein)`.
   `f05` (`xdg`, desktop `KDE`) is the gtk-fallback variant: a one-file `gtk.portal` shadow
   with `DBusName=…desktop.gtk2`, `Interfaces=AppChooser;Inhibit;Background`,
   `UseIn=kde\q` removes the gtk fallback in the oracle (`FileChooser -> []`), while the
   candidate loads the host `gtk.portal` (`FileChooser -> ["gtk"] (gtk-last-resort)`).
   Same shape in `f01`, `f04`, `f06`, `f07`, `f08`, `f11`, `f13`, `f15`, `f16`, `f19`, `f23`
   (13/24 entries, for `gtk`/`hyprland`/`gnome-keyring`/`kwallet`).
3. **Settings / `find_all`** inherits consequence 1: `f21` (`xdg`, desktop `Hyprland`) —
   `theta.portal` has `UseIn=kde\` and `Settings`; the config is
   `config_home/xdg-desktop-portal/portals.conf = default=nosuch\s;theta;kwallet;`.
   Oracle: `Settings -> ["theta","gtk"] (config)`; candidate (theta dropped):
   `Settings -> ["gtk"] (config)`.

All 24 raw disagreements contain at least one `.portal` fixture whose `UseIn` ends in `\` or
contains `\q` (checked programmatically over the raw JSON: 24/24). Breakdown after
minimisation: 13 host-source shadowing, 11 named/config/`*` selection.

## 4. Minimised disagreements

`w1/fuzz-r90-disagreements.json` — 24 entries `f01`…`f24` in the oracle case format
(`id`, `mode`, `desktop`, `files`, `oracle`, `oracle_reason`) plus `candidate`, `diffs`,
`original_diffs`, `origin_case`, `origin_seed`, minimisation statistics, and the shared
`cause`/`upstream` fields.

Minimisation: two greedy rounds of single-step reductions (drop one file, or drop one line
from one file), each step accepted only if the oracle+candidate rerun kept the **exact**
interface/reason difference signature. Result: 24/24 entries kept their signature; the final
fixtures total 9,248 characters across 24 cases (e.g. `f02` and `f05` down to one file,
`f22` to 147 characters). Each entry was re-labelled and compared again from the final file:
`VERIFY cases=24 disagree=24`.

## 5. Clean replication (no unparseable `UseIn`)

`seed 900150034 --clean` (400 cases, all the other descriptor/config quirks intact):
**400/400 agree**, `incomplete=0`, `rc=0`. Together with the 1,656 agreeing cases of the
three normal seeds, the candidate matched the oracle on picks and reasons everywhere except
the 24 `UseIn` cases above. A second seed with `--clean` was not run; this is the declared
bound of the search.

## 6. Commands run (exact; exit status)

```sh
S=/fast/scratch/hyaku/mado-r90/R90MExecFuzz
W1=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-90/w1

# labelling + comparison (each prints PORTAL_ORACLE ... incomplete=0)
python3 "$W1/fuzz-r90.py" --scratch-root "$S/run1" --cases 480 --jobs 8                  # rc 0
python3 "$W1/fuzz-r90.py" --scratch-root "$S/run-900150032" --cases 400 --seed 900150032 --jobs 8  # rc 0
python3 "$W1/fuzz-r90.py" --scratch-root "$S/run-900150033" --cases 400 --seed 900150033 --jobs 8  # rc 0
python3 "$W1/fuzz-r90.py" --scratch-root "$S/run-clean-900150034" --cases 400 --seed 900150034 --clean --jobs 8  # rc 0
python3 "$W1/fuzz-r90.py" --scratch-root "$S/rerun-primary" --cases 480 --jobs 8         # rc 0, identical counts
python3 "$W1/fuzz-r90.py" --scratch-root "$S/rerun-clean" --cases 400 --seed 900150034 --clean --jobs 8  # rc 0, 400/400

# hand-built minimal probes (8 cases, all DISAGREE; 3 is this tool's "disagreements found")
python3 "$W1/fuzz-r90.py" --verify "$S/min/cases.json" --scratch-root "$S/min-verify" --jobs 8   # rc 3

# minimisation over the three raw disagreement files + the clean run (counts only)
python3 "$W1/fuzz-r90.py" --scratch-root "$S/minimise2" --jobs 8 --minimise \
  "$S/run1/fuzz-r90-disagreements.json" "$S/run-900150032/fuzz-r90-disagreements.json" \
  "$S/run-900150033/fuzz-r90-disagreements.json" "$S/run-clean-900150034/fuzz-r90-disagreements.json" \
  --out "$W1/fuzz-r90-disagreements.json"                                                # rc 0; 24/24 same signature

# independent re-check from the delivered file
python3 "$W1/fuzz-r90.py" --verify "$W1/fuzz-r90-disagreements.json" --scratch-root "$S/final-verify" --jobs 8  # rc 3, 24/24 DISAGREE
```

Environment/provenance commands (all read-only): `sha256sum /usr/lib/xdg-desktop-portal`
(`e1429fbe…`), upstream tarball 1.22.1 (`5afeda95…`, matches the declaration), fetched
`glib/gkeyfile.c` at tag 2.90.1 (`e1d1270f…`), `pacman -Q glib2 xdg-desktop-portal`
(`2.90.1-1`, `1.22.1-2`), `ls` of the portal configuration chain (`/etc/xdg-desktop-portal`,
`/etc/xdg/xdg-desktop-portal`, `~/.config/xdg-desktop-portal`, `~/.local/share/xdg-desktop-portal`
all absent; `ls` rc 2, expected). No installs, no pacman transaction, no git/jj mutation.

## 7. Limits / risks

- These are **draft** oracle labels; the freeze may change the case set, mutants and predicate.
  No counter was run and no receipt path was touched.
- Invalid UTF-8 cannot be carried through the oracle case format (the oracle writes fixtures as
  UTF-8), so it is not fuzzed; likewise directory/symlink fixtures are not representable.
- Locale-suffixed keys are generated but only their effect on selection is observable; outcome
  agreed in all generated cases.
- The oracle parser stops at `org.freedesktop.portal.Desktop acquired`; only the 21 start-up
  interfaces are labelled. Settings duplicate sources are deduplicated by the oracle parser and
  by the candidate alike.
- The xdg runs depend on the host tail; its digest is pinned above and in every oracle banner.
- The `[]` + no-reason rule cannot distinguish `none-key` from `no-backend`; both are accepted.
- Upstream line numbers are from the 1.22.1 tarball (sha above); the installed package is
  `1.22.1-2`, whose binary digest is recorded instead.
- The candidate report's `gtk-last-resort` identification uses `DBusName`; the fuzz exercises
  the shadowing interaction but not backend liveness (out of scope for C1).

## 8. Files written by this seat

- `.ufo/waves/round-90/w1/fuzz-r90.py` — seeded generator, oracle/candidate driver,
  comparator, minimiser, verifier.
- `.ufo/waves/round-90/w1/fuzz-r90-disagreements.json` — 24 minimised draft disagreements.
- `.ufo/waves/round-90/w1/R90MExecFuzz.md` — this report.

Scratch (`$HYAKU_SCRATCH/mado-r90/R90MExecFuzz`) was removed after the runs; nothing outside
the three files above was written in the lane.
