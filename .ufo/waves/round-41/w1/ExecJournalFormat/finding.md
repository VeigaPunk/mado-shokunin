# ExecJournalFormat — journal output variants against the frozen ADVERT grammar (mado round 41, w1)

Seat `ExecJournalFormat`, lane `mado-shokunin`, base `ab2bfaab661c846d1de9d58c01651cd156a13949`,
freeze `60c3914154333180450d5da27ba222d5763cc56a`. Host 2026-10-25, `journalctl --version` →
`systemd 262 (262-1-arch)`; `hyprctl version` → `Hyprland 0.56.2 … commit efb50993780079460b0cbed1363e2166a2de1d9f`.
Unit `xdg-desktop-portal-hyprland`; user journal window = 2 boots
(`-1 0a3785aac7104585a914f6cda41795a7`, `0 7ab69ee4149c4811a3faf6c08c9d119b`), 153 lines, 78 advert lines.

Everything below is a **read-only** capture: only `journalctl --user -u xdg-desktop-portal-hyprland
--no-pager -o FORMAT [-b N | --since D | --until D | --no-hostname]`, plus `--list-boots`, `--version`.
No compositor/socket access, no service mutation, no package transaction.

Contract under test: `quality/counters/c1-r41-globals.py` docstring (PRED-C1-r41-v1). It names exactly
one input shape — `c1-r41-globals.py:14-15`:

> The journal the tool reads is the output of
> `journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso`.

and its parser ignores everything else — `c1-r41-globals.py:31-33`:

> every other line (another program, another level, trailing or
> leading text, CR endings, bad timestamps, bytes that are not UTF-8) is ignored.

Two independent implementations were run on every capture: the frozen **reference**
(`.ufo/waves/round-41/c1/ctl-ref-tool.py.txt`, `--selftest` → `MADO_GLOBALS_SELFTEST: 47/47 passed`,
ADVERT at `ctl-ref-tool.py.txt:30`, BOOT at `:34`) and the counter's own scoring **model**
(`c1-r41-globals.py:252 model_sessions`, `:274 model_out`). Both agree on every row.

## 1. Per-format capture (one advert line, verbatim; boundary lines verbatim)

| `-o` | advert line as emitted (first advert of the window) | `-- Boot` boundary | empty-window boundary | adverts in file | ref rc / verdict | model rc / verdict |
|---|---|---|---|---|---|---|
| `short` (default) | `Oct 25 13:16:45 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]  \| Got interface: ext_foreign_toplevel_image_capture_source_manager_v1 (ver 1)` | `-- Boot 7ab69ee4149c4811a3faf6c08c9d119b --` | `-- No entries --` | 78 | **3 / NO_SESSIONS** | **3 / NO_SESSIONS** |
| `short-iso` | `2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]  \| Got interface: ext_foreign_toplevel_image_capture_source_manager_v1 (ver 1)` | `-- Boot 7ab69ee4149c4811a3faf6c08c9d119b --` | `-- No entries --` | 78 | 0 / OK (2 sessions, 63 interfaces, `focus-grab:1`) | 0 / OK |
| `short-iso-precise` | `2026-10-25T13:16:45.875228-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]  \| Got interface: ext_foreign_toplevel_image_capture_source_manager_v1 (ver 1)` | `-- Boot 7ab69ee4149c4811a3faf6c08c9d119b --` | `-- No entries --` | 78 | **3 / NO_SESSIONS** | **3 / NO_SESSIONS** |
| `short-full` | `Sun 2026-10-25 13:16:45 -03 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]  \| Got interface: ext_foreign_toplevel_image_capture_source_manager_v1 (ver 1)` | `-- Boot 7ab69ee4149c4811a3faf6c08c9d119b --` | `-- No entries --` | 78 | **3 / NO_SESSIONS** | **3 / NO_SESSIONS** |
| `cat` | `[LOG]  \| Got interface: ext_foreign_toplevel_image_capture_source_manager_v1 (ver 1)` | none (0 boot lines) | none (empty file, rc 0) | 78 | **3 / NO_SESSIONS** | **3 / NO_SESSIONS** |
| `json` | `{"_HOSTNAME": "plazir27", "_PID": "1918", "__REALTIME_TIMESTAMP": "1792945005875228", "MESSAGE": "[LOG]  \| Got interface: ext_foreign_toplevel_image_capture_source_manager_v1 (ver 1)", …}` | none | none (empty file, rc 0) | 78 | **3 / NO_SESSIONS** | **3 / NO_SESSIONS** |
| `short-iso --no-hostname` | `2026-10-25T13:16:45-03:00 xdg-desktop-portal-hyprland[1918]: [LOG]  \| Got interface: ext_foreign_toplevel_image_capture_source_manager_v1 (ver 1)` | `-- Boot 7ab69ee4149c4811a3faf6c08c9d119b --` | `-- No entries --` | 78 | **3 / NO_SESSIONS** | **3 / NO_SESSIONS** |

Byte invariants measured on all seven captures: exactly **two** spaces between `[LOG]` and `|`
(`grep -c '\[LOG\]  | Got interface:'` = 78, one-space count = 0); no line ends with a trailing space
(`grep -c ' $'` = 0) and no CR byte occurs (`grep -c $'\r'` = 0); the last line of each capture is an
ordinary entry/advert in that format's own shape.

`-- Journal begins at … --`: not emitted by any of the six formats on this host under the allowed verbs
(`grep -n 'Journal begins\|No entries' cap-*.txt` → no match, rc 1; the empty-window captures carry
`-- No entries --` instead). Its shape is journalctl's own,
from the installed binary: `strings /usr/bin/journalctl` →
`-- Journal begins at %s. --` and `-- Journal begins at %s, ends at %s. --`; the boot separator is
`%s-- Boot %02x…%02x --%s` (lowercase hex, 32 digits), `-- No entries --` is a literal.
Both header variants, injected at the head of a `short-iso` copy, are **ignored and harmless**:
ref rc 0, identical report (`captures/inject-iso.txt`, `inject-iso2.txt`).

## 2. Scoping variants that stay inside the grammar

| capture | lines / boot lines | ref rc | ref report |
|---|---|---|---|
| `-o short-iso -b 0` | 75 / 0 | 0 | `sessions=1 … pid=1952 interfaces=63 … OK` — parses, but `boot=-` and no boot marker |
| `-o short-iso -b -1` | 77 / 0 | 0 | `sessions=1 … pid=1918 interfaces=8 … OK` |
| `-o short-iso --since 2020-01-01` | 153 / 1 | 0 | identical to the plain capture: sha256 `bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7` |
| `-o short-iso --until 2020-01-01` | 1 / 0 | 3 | `-- No entries --` → `NO_SESSIONS` (correct: the window holds no adverts) |

`--diff` on a boot-scoped capture degenerates to `MADO_GLOBALS_DIFF: sessions=1 none` (k < 2), rc 0 —
measured on both `-b 0` and `-b -1` — so drift between two boots is only visible when the capture spans boots.

## 3. Findings (each names what it attacks)

**F1 — silent NO_SESSIONS on a non-empty advert file (the named failure class), 5 of 6 formats.**
`journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short` (and `-o short-iso-precise`,
`-o short-full`, `-o cat`, `-o json`) all hold **78** advert lines, yet the grammar reports
`sessions=0 … verdict=NO_SESSIONS`, exit 3, **stderr empty**. A genuinely empty journal
(`captures/empty-short-iso.txt`, sha256 `19c4e28b…`) produces the same exit 3, the same single stdout line
and the same empty stderr — the two cases are indistinguishable from the tool's observable surface.
Attacks: the `--journal-file` leg of the C1 contract as specified (`c1-r41-globals.py:14-15` fixes
`short-iso` as the only accepted shape; nothing requires rejecting or flagging another shape).

**F1b — the default output is the failing shape.** `journalctl --user -u … --no-pager > f` (no `-o`) is
byte-identical to `-o short` (`cmp` identical, sha256 `beab26855f3d6ad8…`). So the most natural way a user
produces a journal file for `--journal-file` is the shape the grammar silently drops.

**F1c — `--no-hostname` is the same trap on the accepted format.** `-o short-iso --no-hostname` keeps the
timestamp but drops the `\S+` host token the ADVERT regex requires (`ctl-ref-tool.py.txt:30-33`), so the
file holds 78 adverts and still reports `NO_SESSIONS`, exit 3. Users who set `--no-hostname` in
`SYSTEMD_*`/`JOURNALCTL` options get a silent empty census.

**F2 — `--expect` cannot rescue the misparse.** `--journal-file cap-short.txt --expect hyprland_focus_grab_manager_v1`
→ `expected_missing=hyprland_focus_grab_manager_v1 … verdict=NO_SESSIONS`, exit 3: `NO_SESSIONS wins over
MISSING_EXPECTED` (`c1-r41-globals.py:47`), so the one flag that exists to catch an absent global stays silent
too. Same input in `short-iso` → `verdict=OK`, exit 0.

**F3 — `--diff` reports "no sessions" instead of a parse failure.** On the same `-o short` file:
`MADO_GLOBALS_DIFF: sessions=0 none`, exit 3 — a drift check that never ran looks like "nothing to compare".

**F4 — the live leg has the same hole through a wrapper.** `--live --journalctl <prog>` accepts any absolute,
non-group/other-writable program (`ctl-ref-tool.py.txt` live rules); a wrapper that ignores argv and emits
`-o short` text yields `verdict=NO_SESSIONS`, exit 3 — not `SETUP journalctl_failed` (exit 5), because the
program exited 0. A reformatting `--journalctl` wrapper is therefore a second silent path to the same class.

**F5 — mixed shapes are silently half-parsed (worse than NO_SESSIONS).** Concatenating the `-o short` capture
with the `-o short-iso` capture (156 advert lines) gives exit 0 and a *full-looking* report built from the
78 `short-iso` lines only; the 78 `short` adverts are dropped with no diagnostic. The report is not even a
faithful subset of the accepted portion: the `-- Boot 7ab69ee4… --` marker carried over from the `short`
portion lands *before* the `short-iso` adverts, so session 1 reports `boot=7ab69ee4149c4811a3faf6c08c9d119b`
instead of `boot=-` (only line 1 of the report differs from the `short-iso`-only run; `cmp` on the two
reports). A stale boot attribution from a foreign-format region is silent and plausible.

**F6 — `-o json` is not byte-stable.** Three consecutive `-o json` captures of the same unit have equal
object content but three different sha256 (`61057fb6…`, `4a5a3b61…`, `d969e1f9…`): journalctl's JSON key
order varies per invocation. Any hash-pinned receipt over a `json` capture is unreproducible (the text
formats are stable: `short`/`short-iso`/`short-iso-precise`/`short-full`/`cat` each hashed identically twice).
`cat`/`json` also drop the `-- Boot` marker, so the boot-split rule and the `boot=` field are unavailable.

**F7 — accepted-format captures reproduce the L1's own receipt.** The plain `-o short-iso` capture hashes to
`bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7`, exactly the sha256 the wave registers
for `fetch/xdph-journal.txt`, and parses to `sessions=2 … interfaces=63 … classes=…,focus-grab:1,… verdict=OK`
with `hyprland_focus_grab_manager_v1 ver=1 count=1 class=focus-grab`. Supports: the reference's happy path and
the C1/C2 journal census.

## 4. Disposition (advisory only — the L1 integrates)

The contract freezes stdout byte-exactly and names `short-iso` as the input, so F1 is a *documented* format
dependency, not a contradiction of the frozen predicate; the reference still scores 24/24 and 47/47. What is
not covered by the contract is the *observable*: `NO_SESSIONS`/exit 3 is overloaded to mean both "empty
journal" and "non-empty journal in a shape the grammar ignores". Options for a v2 registration, none applied
here: (i) a `SETUP bad_format` (exit 2) when the text contains `Got interface:` but no ADVERT matches;
(ii) a `--journal-format {short-iso|short|…}` flag; (iii) at minimum a `--help`/docstring warning plus a
`--live` note that a reformatting `--journalctl` wrapper is not detected. Any of these changes the frozen
stdout/CLI sentence and must be re-registered before data.

## 5. Evidence in this directory

- `captures/` — the seven format captures, six `--since 2030-01-01` empty captures, `b0.txt`, `bm1.txt`,
  `since2020.txt`, `until2020.txt`, the two header-injection copies, `mixed.txt`, `wrap-short.sh`,
  `ref.py` (= `ctl-ref-tool.py.txt`), `ref-src.txt`.
- `runs.txt` — recorded output of `repro.sh`: per-format advert counts, ref rc/verdict, model rc/verdict,
  boundary lines, scoping variants, the three probes, and sha256 of every capture.
- `repro.sh` — regenerates all of the above into a fresh `mktemp -d`; it writes nothing in the lane.

Capture hashes (sha256): `short` `beab26855f3d6ad8b6ccf8ecd9f896d5d46fc362909c6a6fc826e4e89486c5b8`;
`short-iso` `bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7`;
`short-iso-precise` `e2fd9944d5a4620ed403c1b7267453ecf95be8bb33b10283a43f558ba46c2a4c`;
`short-full` `d42265f3ff09818c7640e87cbf8be2ddee7942d1b332c2db365ab57796aeeb86`;
`cat` `fef58aeb06792fffdc44a16ab0a26d63ed05b2117aaa3b44f5cd27cbae33a420`;
`--no-hostname` `9c4a0a2877e3b714041989649274c46eafa5aa5aa963bc05859b0394c6ca45cf`;
empty window (all four text formats) `19c4e28b2f54ea8f217db4e622b0a5c758efa7b77ce2dc0394b6d159568c0b2e`;
`json` varies per run (F6) — the stored `captures/cap-json.txt` is one sample
(`7ff69dbf87be20c1ff9d89f278829cf909bbd03cd0f011698b32a86e5c7a2f0a`, equal object content to the later
runs, different key order and hash).
