# ExecJournalFormat — report (mado round 41, w1)

**Status: complete.** Scoped finding at `.ufo/waves/round-41/w1/ExecJournalFormat/finding.md`
(plus `captures/`, `runs.txt`, `repro.sh`, `verify_quotes.py`, `quotes.txt` in that seat directory).
No writes outside the seat directory and this report; nothing frozen was edited; no mutating git/jj; no
compositor/socket access; no package transaction; only read-only `journalctl --user -u <unit> --no-pager
-o FORMAT [-b N | --since D | --until D | --no-hostname]`, `--list-boots`, `--version`, plus `strings`
on `/usr/bin/journalctl` and `hyprctl version`.

## What was measured

- Host: `systemd 262 (262-1-arch)`; Hyprland 0.56.2 (`efb50993780079460b0cbed1363e2166a2de1d9f`).
- Unit `xdg-desktop-portal-hyprland`, user journal, 2 boots (`-1 0a3785aac7104585a914f6cda41795a7`,
  `0 7ab69ee4149c4811a3faf6c08c9d119b`), 153 lines, **78 advert lines** per capture.
- Two independent parsers run on every capture: the frozen reference
  (`.ufo/waves/round-41/c1/ctl-ref-tool.py.txt`, `--selftest` → `47/47 passed`) and the counter's scoring
  model (`quality/counters/c1-r41-globals.py:252/274`). They agree on every row.

## Result (the assigned question)

| `-o` | advert shape | ref rc / verdict |
|---|---|---|
| `short` (**journalctl's default**) | `Oct 25 13:16:45 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]  \| Got interface: … (ver 1)` | **3 / NO_SESSIONS** |
| `short-iso` | `2026-10-25T13:16:45-03:00 plazir27 xdg-desktop-portal-hyprland[1918]: [LOG]  \| Got interface: … (ver 1)` | 0 / OK (2 sessions, 63 interfaces) |
| `short-iso-precise` | `2026-10-25T13:16:45.875228-03:00 …` | **3 / NO_SESSIONS** |
| `short-full` | `Sun 2026-10-25 13:16:45 -03 plazir27 …` | **3 / NO_SESSIONS** |
| `cat` | `[LOG]  \| Got interface: … (ver 1)` | **3 / NO_SESSIONS** |
| `json` | one object per line, advert text inside `"MESSAGE"` | **3 / NO_SESSIONS** |
| `short-iso --no-hostname` | `2026-10-25T13:16:45-03:00 xdg-desktop-portal-hyprland[1918]: [LOG]  \| …` | **3 / NO_SESSIONS** |

Boundary lines: `-- Boot 7ab69ee4149c4811a3faf6c08c9d119b --` is emitted by `short`, `short-iso`,
`short-iso-precise`, `short-full` (line 78) and **absent** from `cat`/`json`; `-- No entries --` is the
whole body for the four text formats on an empty window, and `cat`/`json` emit nothing (rc 0). No capture
under the allowed verbs emits `-- Journal begins at … --`; its shapes are journalctl's own
(`strings /usr/bin/journalctl`: `-- Journal begins at %s. --`, `-- Journal begins at %s, ends at %s. --`)
and both injected variants are ignored with an unchanged report (rc 0).

## Findings the L1 should weigh

1. **The named failure class is real and broader than one format.** Five of six `-o` values, plus
   `--no-hostname` on the accepted format, leave a file with 78 adverts that the grammar reports as
   `sessions=0 … verdict=NO_SESSIONS`, exit 3, **stderr 0 bytes** — byte-for-byte the observable of a
   genuinely empty journal (`captures/empty-short-iso.txt`, rc 3, stderr 0). `journalctl --user -u … >
   f` (no `-o`) is byte-identical to `-o short`, so the most natural capture is the failing one.
2. `--expect` does not rescue it (`NO_SESSIONS wins over MISSING_EXPECTED`), and `--diff` prints
   `sessions=0 none`; a check that never ran is indistinguishable from a clean one.
3. The live leg has the same hole: `--live --journalctl <wrapper>` where the wrapper emits `-o short`
   yields `NO_SESSIONS`/exit 3, not `SETUP journalctl_failed`.
4. Mixed-shape files are half-parsed at exit 0 and can carry a **wrong** value: a `short` capture
   concatenated with a `short-iso` capture reports session 1 `boot=7ab69ee4…` instead of `boot=-`
   (only that field differs from the `short-iso`-only report).
5. `-o json` is not byte-stable (key order varies per invocation; three runs, three sha256, equal object
   content), so a hash-pinned json receipt is unreproducible. Text formats are stable.
6. The accepted path is intact: the plain `-o short-iso` capture hashes to
   `bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7` (the wave's own `fetch/xdph-journal.txt`
   sha256) and parses to `sessions=2 … interfaces=63 … focus-grab:1 … verdict=OK`.

## Disposition

The frozen predicate is not contradicted (reference 24/24, selftest 47/47, both parsers agree); the
contract fixes `short-iso` as *the* input. The gap is that `NO_SESSIONS`/exit 3 is overloaded to mean both
"empty journal" and "non-empty journal in an ignored shape". Any remedy (a `SETUP bad_format`, a
`--journal-format` flag, or a documented warning) changes the frozen stdout/CLI sentence and therefore
needs a v2 registration before data. Nothing was changed here.

## Exact retained evidence

- `finding.md` — the per-format table with verbatim advert/boundary lines and F1–F7.
- `captures/` — 7 format captures, 6 empty-window captures, `b0.txt`, `bm1.txt`, `since2020.txt`,
  `until2020.txt`, `inject-iso.txt`, `inject-iso2.txt`, `mixed.txt`, `wrap-short.sh`, `ref.py`,
  `ref-src.txt`.
- `runs.txt` — output of `repro.sh`: advert counts, byte invariants (two-space, trailing space, CR),
  ref rc/verdict, model rc/verdict, boundary lines, scoping variants, `--diff` on `-b 0`/`-b -1`,
  the three probes, mixed-vs-base diff, stderr sizes, sha256 of every capture.
- `repro.sh` — regenerates everything into a fresh `mktemp -d` (writes nothing in the lane);
  re-run: `sh .ufo/waves/round-41/w1/ExecJournalFormat/repro.sh "$(mktemp -d)"`.
- `quotes.txt` — `verify_quotes.py` over `finding.md` against `quality/counters/c1-r41-globals.py`:
  `QUOTES: n=2 all_ok=1 max_words=22`.
- Key hashes: `short-iso` `bf8fa91a…`, `short` `beab2685…`, `short-iso-precise` `e2fd9944…`,
  `short-full` `d42265f3…`, `cat` `fef58aeb…`, `--no-hostname` `9c4a0a28…`, empty window `19c4e28b…`,
  `-b 0` `1ff1497d…`, `-b -1` `d14279a2…`; `--since 2020-01-01` is byte-identical to the plain capture.

## Tools installed

None (no package transaction; `python3`, `journalctl`, `strings`, `cmp` were already present).

## Risks / blockers

- None blocking. Residual: the `-- Journal begins at … --` shape was not reproducible with the allowed
  read verbs; its two forms come from the installed binary's format strings and their effect was measured
  by injection, not by a live header. `-o export`, `verbose`, `json-pretty`, `with-unit` were not run
  (outside the assigned verb list) and are not claimed.
