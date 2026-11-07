# R92MExecFuzz — fuzz report (DRAFT; all runs below are non-measurement draft runs)

**Status (top, first line):** DRAFT — draft fuzz evidence for L1 integration; nothing here is a measurement.

Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Base `d992ef7494b054591ee9104df1da49264678df5d`.
Candidate: `.ufo/waves/round-92/build/mado-xdgmime.c1.py` (4121d583…)
Oracle: `.ufo/waves/round-92/controls/xdgmime-oracle-r92.py` (e5160399…, labels from installed `/usr/bin/xdg-mime` a587107f…)
Frozen generator: `.ufo/waves/round-92/controls/fuzz-gen-r92.py` (891704bf…)
Extended generator (this seat, optional): `.ufo/waves/round-92/controls/fuzz-gen-r92-ext.py`
Scratch: `$S=$HYAKU_SCRATCH/mado-r92/R92MExecFuzz` (HYAKU_SCRATCH default `/fast/scratch/hyaku`); removed on exit
except cited artifacts copied to `w1/`. Runtime per 120 cases is measured with the parallel harness (16 workers,
host has 126 CPUs); the counter's sandbox + frozen seed will differ — see §1.

Method (each case): oracle `label_case` (materialised fixture + `xdg-mime query default TYPE` per type,
`env -i` whole-environment, cwd = fixture root) vs candidate `mado-xdgmime.c1.py --json` invoked with an
empty start-environment plus the case's env via `--env` (candidate is a read-only file replay; it was not run
inside `bwrap` here — the counter does that; results are labelled DRAFT for that reason). A case counts as a
disagreement iff the candidate's `(default, rc)` map ≠ the oracle's `expect` map (crash/rc≠0 ⇒ disagreement).

## 1. Frozen generator — 12 seeds × 200 cases = 2400 cases (DRAFT)

| seed | disagreements | wall (16-worker) | per-120 |
|---|---|---|---|
| 1 | 0/200 | 4.7s | 2.8s |
| 2 | 0/200 | 4.6s | 2.7s |
| 3 | 0/200 | 4.3s | 2.6s |
| 4 | 0/200 | 4.6s | 2.8s |
| 5 | 0/200 | 5.7s | 3.4s |
| 6 | 0/200 | 4.4s | 2.7s |
| 7 | 0/200 | 4.8s | 2.9s |
| 8 | 0/200 | 4.7s | 2.8s |
| 9 | 0/200 | 6.5s | 3.9s |
| 10 | 0/200 | 7.6s | 4.6s |
| 11 | 0/200 | 7.3s | 4.4s |
| 12 | 0/200 | 6.4s | 3.9s |
| **total** | **0 / 2400** | | |

**Distinct disagreement classes: none.** Every frozen-generator case agreed exactly (including exit status).
Sequential (non-parallel) timing for reference: one early sequential run of seeds 1–4 timed out at 300s
(slow oracle startup; parallel is ~50× faster); the per-120 figures above are the parallel-harness figures.
Stored detail: `fuzz-results.json` (copied to `w1/`), `fuzz-disagreements.json` (empty lists).

## 2. Targeted gap probes (DRAFT; hand fixtures in oracle case schema)

| # | probe | result |
|---|---|---|
| symlink-mimeapps (symlink → real mimeapps.list) | OK (a.desktop) |
| symlink-desktop (symlink → real .desktop) | OK |
| symlink-dangling-desktop (dangling → skip to b.desktop) | OK |
| unreadable-desktop mode 000 (→ skips to b.desktop) | OK |
| Exec `env A=1 p0` (cut -d= -f2-) | OK |
| Exec `-n` (builtin/echo flag) | OK |
| Exec `"p0 x"` quoted-with-space, `bin/p0 x` exists | OK |
| Exec multi-line first-wins, Exec with spaces, tab-separated | OK |
| InitialPreference multiple lines / X- vs plain / `+5` / ` 7` | OK (both None where `test -gt` fails) |
| MimeType grep anywhere, defaults BRE `*`, [a-c], semicolon-spaces, indent, vendor/glob XCD | OK |
| LXQt dispatch rc=3, KDE v6 generic, KDE v5 no-trader generic, KDE no-version+ktradertest generic | OK |
| flatpak-info override, LXQt+flatpak override, XCD unset, DESKTOP_SESSION fallback, data/config HOME fallbacks, dir-as-file | OK |
| PATH trailing-colon/empty-entry/dot/double-slash **with /usr/bin reachable** | OK (all four) |
| MIME edge: `""`, `text`, `-foo/bar`, `text/`, `text/plain extra`, `--version` | OK |

Declared-refusal divergences (candidate rejects with rc=2 `unsupported`; xdg-mime answers — all in the
candidate docstring's refusal list, §3):

| probe | xdg-mime (oracle) | candidate |
|---|---|---|
| NUL byte in a read file (`b64` …\x00) | `(None, rc 0)` — grep/awk ignore the file | rc=2 `unsupported: NUL byte in …` |
| KDE v5 + `ktraderclient5` on PATH (stub) | `(None, rc 4)` — `defapp_kde` runs stub, gets no `DesktopEntryPath`, `exit_failure_operation_failed` (xdg-mime:1223-1248) | rc=2 `unsupported: KDE trader ktraderclient5 on PATH` |
| Asked type `--help` | usage text, rc 0 | rc=2 `unsupported: --help prints the usage text` |
| `XDG_UTILS_REALPATH_BACKEND=realpath` | resolves normally (`xdg_realpath` honours the set backend, xdg-mime:710-743) | rc=2 `unsupported: … set` |
| PATH *without* `/usr/bin` (`{R}/bin:` only) | `(None, rc 0)` — `grep: command not found` etc. (xdg-mime:612,1133,1156,1210); candidate scope assumes coreutils/grep/gawk on PATH | candidate resolves via `cwd`-empty-entry ⇒ `a.desktop`, rc 0 **(silent divergence; out of declared scope — generator docstring guarantees PATH reaches /usr/bin)** |

The last row is the only non-refusal divergence found, and it is outside the candidate's declared assumption
("PATH reaches GNU coreutils/grep/gawk under their own names"). The frozen and extended generators both keep
`/usr/bin` on PATH, so it cannot arise at measurement. No silent in-scope divergence was found.

## 3. Rule classes the frozen generator never produces (and the extended generator adds)

Diffing `fuzz-gen-r92.py` (sampled 2500 cases: only `text` specs; env keys `HOME/XDG_CONFIG_HOME/XDG_CONFIG_DIRS/
XDG_DATA_HOME/XDG_DATA_DIRS/PATH/XDG_CURRENT_DESKTOP[/XDG_MENU_PREFIX/KDE_SESSION_VERSION]`; TYPES ⊆ 10 sane
types; IDS ⊆ 10 paths; Exec first-tokens = the 25 listed; InitialPreference ∈ `{1,5,10,abc,-1,"", "7\r","3 "}`)
against the candidate docstring + installed `xdg-mime` source (`defapp_generic` 1174-1219, `check_mimeapps_list`
1121-1171, `desktop_file_to_binary` 338-376, `search_desktop_file` 1074-1085, `defapp_fallback` 1087-1119,
`detectDE` 561-657, `first_word` 302-306, `xdg_realpath` 710-743):

Frozen generator NEVER produces:
- `{"symlink": …}` / `{"dir": True}` specs, `{"b64": …}` specs, NUL bytes, non-UTF8 bytes, mode `000` (only `755/644` + dir `755` + one `p0`-with-space exec) — all ~15 `readable`/`NUL`/`isdir` branches in the candidate are unexercised.
- Env: `XDG_CURRENT_DESKTOP` unset/empty; `DESKTOP_SESSION`, `KDE_FULL_SESSION`, `GNOME_DESKTOP_SESSION_ID`, `MATE_DESKTOP_SESSION_ID`, `LXQT_SESSION_CONFIG`, `DESKTOP`, `XDG_RUNTIME_DIR` (+ `flatpak-info` file); `KDE_SESSION_VERSION` unset (the `ktradertest` branch); XCD values beyond the 10 (`GNOME-Flashback`, `X-Cinnamon`, `ENLIGHTENMENT`, `MATE`, `XFCE`, `LXDE` — these map to known `DE`s but still take the generic path; the `gnome3` rewrite at detectDE:652 is dead config for `query default`).
- Asked types outside RFC 6838 restricted-name (`text/[a-c]`, `text/*`, `a;b`, spaces, `""`, `text`, `text/`, `--help`, `--manual`) — candidate refuses these by design (TYPE_CHARS filter).
- PATH: empty entries, `.` entries, double slashes — candidate's cwd-fallback is unexercised (all frozen PATHs are 2–3 non-empty components).
- Exec: duplicate `Exec=` lines, `Exec` args containing `=` beyond `env A=1`, tab-separated, leading/trailing spaces, `%F %f %U %u %i %c %k` mixes, `NoDisplay`/`Hidden` (correctly irrelevant to `defapp`), keywords-as-Exec (`if`, `cd`, `p0='x'`).
- InitialPreference: `0`, `+5`, `007`, ≥2³¹, multiple IP lines, non-UTF8.
- mimeapps: tab-indented keys, ` [Default Applications]` with leading space, `=`-spacing variants beyond `=`/` =`, `; ` spacing, NUL lines, directory-as-mimeapps.list.
- Lists/headers: `[Added Associations]` as `defaults.list` header (frozen only uses it in mimeapps), symlinked `mimeinfo.cache`/`defaults.list`.
- Layouts: `a.deeper/nest/` (3-deep), `.hidden/` (hidden subdir — `subdirs` skips dot-names), top-level regular file `p0` in cwd (glob/cwd-relative `command_v` exercise — frozen puts progs only in `bin/`/`bin2/` + cwd-file `p0` rarely).

Extended generator (this seat) adds all of the above while preserving the frozen scope contract (PATH always
reaches `/usr/bin`; no `qtxdg-mat`/`ktraderclient*` on PATH; NUL only via `b64`). Same interface: `generate(seed, n)`.

### Extended generator run (DRAFT) — 6 seeds × 200 = 1200 cases

| seed | disagreements | wall | per-120 |
|---|---|---|---|
| 1–6 | 116, 114, 109, 107, 109, 104 /200 | 1.6–2.2s | 1.0–1.3s |
| **total** | **659 / 1200 (~55%)** | | |

All 659 are declared-refusal `rc=2 unsupported`, **zero value mismatches**:
- type outside RFC 6838 restricted-name: 511 cases (110× `text/[a-c]`, 106× `text/plain;x`, 98× `text/*`, 96× `text/plain extra`, 101× `--help` — counts overlap per-case)
- NUL byte in a read file: 148 cases
- No other `unsupported` message occurred (no `XDG_UTILS_*` set, no KDE-trader, no PATH-unset in the extended generator).

Filtered to in-scope cases only (drop cases with an outside-charset asked type, a `--help` ask, or a NUL file):
**0 / 229 mismatches** (seeds 1–3). In other words, every class the extended generator adds that lies inside the
candidate's declared scope (symlinks, dirs, modes, dispatch envs, duplicate Exec, IP extremes, PATH empty/dot
entries, …) agrees exactly; disagreement is 100% confined to the candidate's declared refusal surface.

## 4. Risks / blockers

- DRAFT, not measurement: the candidate was invoked directly (no `bwrap` sandbox); the counter's sandbox,
  pinning and seed = sha256(file) will produce the official fresh leg. No `--draft-tool` counter run was executed
  by this seat (the `fuzz-gen`/`w1` write scope and the 60 s `--fresh` leg are L1-owned at the freeze).
- The sequential-vs-parallel timing gap (≈50×) means the counter's 120-case fresh leg will be dominated by
  oracle startup, not by the candidate; per-120 is a property of the harness, not the tool.
- KDE-trader/realpath-backend/NUL/charset/`--help` divergences are declared refusals; if the frozen predicate
  ever asks a type outside RFC 6838 or sets `XDG_UTILS_*`, the tool must refuse (rc=2) and cannot score that
  case — the freeze must keep both generators inside the declared scope, as the frozen one does.
- Installed binaries (pins): xdg-mime a587107f…, bash c14c8f49…, grep 19280b0e…, gawk 3ac64468…,
  realpath 5f6c63c5…, basename a21add5f… (match the declaration's list). No tools were installed or changed.
- Report trailer: `Report: .ufo/waves/round-92/w1/R92MExecFuzz.md`

---

## Reproduction (how each DRAFT run was produced)

Frozen: `fg=load(fuzz-gen-r92.py); for seed in 1..12: cases=fg.generate(seed,200); expect=oracle.label_case(c,$S);
candidate: python3 -I cand --json --cwd <root> --env=… -- types; compare (default,rc) maps.` Extended: same with
`fuzz-gen-r92-ext.py` (seeds 1–6). Gap probes: hand-written oracle-schema cases listed in §2, same harness.
All oracle runs are `xdg-mime query default TYPE` only (host-safety contract honoured); all fixture roots are
under `$S` and were removed after copying `fuzz-results.json`, `fuzz-disagreements.json`,
`fuzz-ext-results.json`, `fuzz-ext-disagreements.json` to `w1/`. No files outside `w1/` + the owned
`controls/fuzz-gen-r92-ext.py` + scratch were written; no git mutations; no receipts written.
