# ScrRows — SOURCES rows S326..S338 for C2 (round 47, w1, 2026-10-26)

Seat: `ScrRows` (scribe). Target: draft the SOURCES rows the C2 entry
`corpus/knowledge/xdg-terminal-selection-r47.md` will cite. Lane repo
`/home/vgpnk/Projects/shokunin/mado-shokunin` at base 60edb66. Nothing frozen; no
product file written, no git/jj mutation, no lane index touched.

## Behavior

Rows drafted: **13** (S326-S338), 11-column registry format, status `mined`, opened
`2026-10-26`, `used-by corpus/knowledge/xdg-terminal-selection-r47.md`, no cell
contains `|`.

| row | source | kind |
|---|---|---|
| S326 | xdg-terminal-exec v0.14.3 script, **selection code** (list composition, validation, selection loop, print modes, cache) — scope distinct from S057's option/`--dir` code | code |
| S327 | same README, the **sections S056 does not hold** (:257-337: arguments, performance, compat mode, cache, Exec double-expansion, other implementations) | docs |
| S328 | `xdg-terminal-exec.1.scd` man page at the tag (config order, FILES, ENVIRONMENT) | docs |
| S329 | `test/tests.bats` upstream suite at the tag (hidden / TryExec / ShowIn / collation / actions / print) | code |
| S330 | XDG Default Terminal Execution Specification proposal, `proposals/xdg-terminal-exec.md` at MR 3 head `64c429df` | spec |
| S331 | Desktop Entry Specification source, `xdg/xdg-specs` @ `a0eaad5c` (file ID, value types, Type, Hidden, OnlyShowIn/NotShowIn, TryExec, Exec, Actions, extra actions) | spec |
| S332 | XDG Base Directory Specification source @ `a0eaad5c` | spec |
| S333 | omarchy v3.8.3 `applications/Alacritty.desktop` @ commit `6aa2aec1` (the deployed user entry) | code |
| S334 | omarchy v3.8.3 `config/xdg-terminals.list` (single-ID list, byte-identical to the host's) | code |
| S335 | omarchy v3.8.3 `bin/omarchy-default-terminal` (the only writer of `~/.config/xdg-terminals.list`) | code |
| S336 | omarchy v3.8.3 `bin/omarchy-cmd-terminal-cwd` (source of the hotkey's `--dir=` value) | code |
| S337 | host bytes: `~/.local/share/applications/Alacritty.desktop` (452 B, 713703ba…) and `/usr/share/applications/Alacritty.desktop` (374 B, d420b0f4…) | code |
| S338 | host installed omarchy tree: `version` = 3.8.3, installed entry and list digests equal the v3.8.3 tag bytes | dataset |

Distinct-from-held-ground statement is in the rows.md preamble: S056/S057 family
option code is S057's; S326 is the selection half of the same script. S059 already
digests `~/.config/xdg-terminals.list` and `bindings.conf:2-3`; S060 already digests
the system list. None of those bytes is re-claimed here.

## Gates (run, with output)

1. **Census validate, mirror with rows + stand-in** —
   `scripts/sources-census.sh validate --file <scratch-mirror>/corpus/SOURCES.md --today 2026-10-26`
   → **exit 0**, 0 E-codes, 17 warnings
   (`gate/validate-with-placeholder.txt`). The 17: `W04` S326 (same URL as S057),
   `W04` S327 (same URL as S056) — the two expected repeated URLs — plus 15
   pre-existing lane warnings (S030, S042, S045, S097, S119, S120, S121, S303,
   S307, S317, S318, S320, S321, S324 as W04; `W01` S277).
2. **Baseline, unmodified mirror** → **exit 0**, the same 15 pre-existing warnings,
   i.e. the mirror itself introduces nothing.
3. **Control without the stand-in** → **exit 1** with exactly **13 E11** findings,
   one per new row, all naming `corpus/knowledge/xdg-terminal-selection-r47.md`
   (`gate/validate-no-placeholder.txt`). This is the honest residual: the rows'
   `used-by` points at the C2 entry, which **does not exist in the lane yet**
   (checked 2026-10-26, before and after my work: absent). The exit-0 gate above
   therefore rests on a **mirror-only stand-in** at that path
   (`corpus/knowledge/xdg-terminal-selection-r47.md`, 4 lines, text "MIRROR-ONLY
   STAND-IN"), and I label it as such rather than as evidence. When the C2 seat
   lands the real entry the same validate run needs no stand-in; nothing else in
   the 13 rows fails.
4. **Quote verification** — `bash .ufo/waves/round-47/w1/ScrRows/verify-quotes.sh`
   → `QUOTES: 13 passed, 0 failed` (`gate/quotes.txt`). Each Gate line's quote is
   grepped in its receipt at the stated line; every quote is <= 25 words.
5. **Mirror fidelity** — `diff -u lane/corpus/SOURCES.md mirror/corpus/SOURCES.md`
   contains exactly the 13 added rows and nothing else (`gate/mirror-vs-lane.diff`,
   13 `+| S3` hunks); the mirror's first 274 lines are byte-identical to the lane's.

## Findings worth the L1's attention

- **F1 (provenance chain, new).** The host's selected entry is not a hand edit:
  `~/.local/share/applications/Alacritty.desktop` (713703ba…) is byte-identical to
  `omacom/omarchy` v3.8.3 `applications/Alacritty.desktop`, and
  `~/.local/share/omarchy/version` reads `3.8.3`; the installed tree's copy carries
  the same digest (S333/S338). The list `~/.config/xdg-terminals.list`
  (d035da57…, already S059) is byte-identical to omarchy v3.8.3
  `config/xdg-terminals.list` (S334). So the whole omarchy layer of the chain is
  pinned to tag `6aa2aec1`.
- **F2 (selection mechanism, code-grounded).** `find_entry` walks the explicit list
  first with `*ShowIn` checks off, then a `//fallback_start//` marker switches them
  on for the data-dir fallback (`xdg-terminal-exec:1057`, `:1060`, `:1071-1072`).
  Eligibility is cumulative: `TerminalEmulator` in Categories (`:816-828`),
  `Hidden=true` rejects (`:938-946`), `TryExec` must resolve (`:933-937`), `Exec[0]`
  must resolve (`:947-968`), the action must appear in `Actions` (`:829-845`,
  `:1004-1010`). This is what makes the 452-byte user entry eligible and the
  374-byte system entry not: only the user file carries `X-TerminalArg*`
  (`:1087-1089`, `:1091-1107` for compat mode).
- **F3 (spec status).** The "specification" the resolver implements is still an
  **open** merge request (`state: opened`, head `64c429dfaf44…`), so the C2 entry
  must not describe it as a released standard; S330 records the head SHA, not a tag.
- **F4 (host delta found while pinning).** The upstream v0.14.3 tag
  `xdg-terminals.list` is sha256 `a2b5bf69…`, i.e. the digest S060 already carries
  for the host system list; today's fetch reproduces it, so S060 needs no reopen.
- **F5 (available but not rowed).** The upstream repo ships a `Makefile` and a full
  `test/config` + `test/data` fixture tree; the fixture lists duplicate S329's
  teaching, so they were excluded, not missed (searchlog.md).

## Out of scope / not done

- The knowledge entry `corpus/knowledge/xdg-terminal-selection-r47.md` itself — C2's
  seat. I did not draft or stub it in the lane; the stand-in exists only in scratch.
- The live `xdg-terminal-exec --print-*` observation and the C1 tool — other seats.
- No merge into `corpus/SOURCES.md`, no edit to any tracked file.

## Touched surfaces

- Written (only): `.ufo/waves/round-47/w1/ScrRows/` — `rows.md`, `gate-lines.md`,
  `searchlog.md`, `verify-quotes.sh`, `fetch/` (16 receipts), `gate/` (4 receipts),
  and this report.
- Scratch: `/fast/scratch/hyaku/mado-r47/ScrRows/` (lane mirror + fetches), deleted
  before finishing. No `/tmp` use, no pacman/uv/npm install (nothing needed).

## Artifacts

```
.ufo/waves/round-47/w1/ScrRows.md                                        (this report)
.ufo/waves/round-47/w1/ScrRows/rows.md                                   13 rows, 43 lines
.ufo/waves/round-47/w1/ScrRows/gate-lines.md                             13 Gate lines + 16 pins with sha256
.ufo/waves/round-47/w1/ScrRows/searchlog.md                              search-log draft for L1
.ufo/waves/round-47/w1/ScrRows/verify-quotes.sh                          grep-based quote checker
.ufo/waves/round-47/w1/ScrRows/gate/quotes.txt                           QUOTES: 13 passed, 0 failed
.ufo/waves/round-47/w1/ScrRows/gate/validate-with-placeholder.txt        exit 0, 17 W, 0 E
.ufo/waves/round-47/w1/ScrRows/gate/validate-no-placeholder.txt          exit 1, 13 x E11 (the C2 dependency)
.ufo/waves/round-47/w1/ScrRows/gate/mirror-vs-lane.diff                  exactly 13 added rows
.ufo/waves/round-47/w1/ScrRows/fetch/                                    script, README, man, tests, proposal, 2 specs
.ufo/waves/round-47/w1/ScrRows/fetch/om/                                 omarchy v3.8.3: entry, list, writer, cwd helper
.ufo/waves/round-47/w1/ScrRows/fetch/host/                               host bytes: 2 entries, installed pair, version
```

## Limits of this report

Validator and quote results are quoted from the runs above; nothing else was re-run.
The stand-in file is not evidence and is marked as such in both `rows.md` § Gate and
its own text. The two W04 rows are expected and listed; no W-code was suppressed.
