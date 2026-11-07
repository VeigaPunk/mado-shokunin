# mado round 98 - lessons

Round 98, hyaku run 15, attempt 1 (`MadoR98`). Two frozen claims from
`.ufo/waves/round-98/claims-declaration-r98.md`: C1 coverage (new surface: `tools/mado-execargv.py`,
the launch argv sequence GIO 2.90.1 builds from a desktop entry's `Exec` key) and C2 operability
(`quality/check-sources-readback.py`, the registry citation read-back, and the 23 cells it repaired).
This file is the scribe's draft for the L1 to land after the freeze; the measured cells are the L1's.

## Mistakes

**M98-1 - the oracle read a shared output file, so a multi-spawn launch looked like "the last argument
wins" and the first model of the surface was wrong.**
Class: instrument race mistaken for a model rule. `gio launch` returns before the spawned child writes
its argv; the probe wrote to one `probe.sh.out`, so with `%f` and three arguments the three children
overwrote each other and the reader saw only the last writer.
Evidence: the first probe family (`.ufo/waves/round-98/receipts/control-naive-r98.json` run 1) read
`A1=c.txt` for `%f` with a,b,c; the appended-record probe (probe3, `@@@ <argc>` per spawn) showed three
spawns, one per argument, in order a,b,c. The cause is `g_desktop_app_info_launch_uris_with_spawn`'s
`do { expand_application_parameters(...) } while (dup_uris != NULL)` (gdesktopappinfo.c:3003-3025).
Captured-by: none of the round's instruments - the L1's own second probe found it; the declaration's
first draft would have frozen a single-argv surface.
Fix: the surface is the launch SEQUENCE; the probe appends one record per spawn atomically and the
oracle waits 200 ms of quiet (8 s cap) before parsing; the declaration's rule 6 states the iteration.
Shown able to fail: with the one-file probe, `%f` + a,b,c reads one argv (c); with the appended-record
probe the same command reads three (`a`, `b`, `c`).

**M98-2 - the declaration asserted a `#` branch that the CLI cannot reach.**
Class: a source rule stated without its caller's pre-processing (the `QUALITY.md` 166 family, applied to
an input transformation). `expand_macro_uri` bypasses `force_file_uri` when the URI contains `#`, but
`gio launch` builds each argument with `g_file_new_for_commandline_arg` (gio-tool-launch.c:116) and a
local file URI's fragment is dropped before `expand_macro_uri` sees it; for a non-local URI both
branches answer the URI.
Evidence: measured `%u` + `file://…/a.txt#frag` -> the path; `%u` + `http://…/x#y` -> the URI; `%f` +
`file://…/a.txt?q=1` -> the path. Found by R98MMutC1 and re-measured by the L1.
Captured-by: the mutation tester's cross-check; the declaration's rule 3 was written from the source
alone.
Fix: the model includes the `g_file_new_for_commandline_arg` step; the `#` branch is a named limit; the
`u-anchor` class expects the path.
Shown able to fail: the frozen class's oracle label is the path, so a candidate that applies the raw
`#` rule mismatches.

**M98-3 - the desktop-file parser was declared to keep an invalid escape literal; GKeyFile refuses it.**
Class: parser-error policy stated from the model instead of measured. GKeyFile rejects any Exec escape
outside `{s,n,t,r,\\}`; `gio launch` then prints `Unable to load application information` and exits 1.
Evidence: measured `a\ b`, `a\z`, `a\:b`, `"a\"b"` all refused (rc 1, no probe record); the first
control family's `quote-02` case was refused for this reason.
Captured-by: R98MMutC1's probes; the L1's control run (quote-02 expected `None`).
Fix: an invalid escape is a `desktop-file` refusal case; the `quote` class's backslash case is written
as `\\` in the file.
Shown able to fail: `env -i … gio launch <case with a\ b>` exits 1 and writes no record.

**M98-4 - the declaration declared a `Hidden` refusal that the launch path does not perform.**
Class: a check attributed to the wrong code path. `g_desktop_app_info_new_from_filename`
(gdesktopappinfo.c:2108-2112) loads the key file without a hidden gate; the only launch-path hidden
check is in the desktop-id lookup (:2209).
Evidence: `Hidden=true` + a valid Exec launches (rc 0, probe records the argv); R98MExecTool confirmed
the source lines.
Captured-by: R98MMutC1's probe and R98MExecTool's source read.
Fix: `Hidden` is read but not refused; the declaration says so.
Shown able to fail: the frozen `Hidden` case's oracle label is a launch, so a candidate that refuses it
mismatches.

**M98-5 - 23 entry-to-row citations were unacknowledged by the registry, and no instrument read them
back.**
Class: a registry cell that no checker reads (the round-97 spot-check's routed defect 5, generalised).
An entry's `source:` frontmatter names a row; the row's `used-by` cell does not name the entry. The
fleet census checks used-by existence (`E11`) and recheck validity (`E09`), never the reverse direction.
Evidence: base `35f3ce80`, 23 pairs over 8 entries and 14 rows
(`.ufo/waves/round-98/receipts/c2-base-mismatches-r98.txt`); S030 and S132 carried `—`.
Captured-by: nothing in the fleet census; the round-97 spot-check named the missing read-back.
Fix: `quality/check-sources-readback.py` (R4) and the 23-cell repair
(`.ufo/waves/round-98/controls/readback-repair-map-r98.json`).
Shown able to fail: the gate's planted copy (one used-by cell stripped) produces exactly one R4 finding;
the base registry produces 23.

**M98-6 - two junk files sat at the fleet root since mado rounds 90/94.**
Class: misroot leftovers that the round's own sweep did not attribute. `f.txt` (2 B, mtime 2026-11-07
04:40, inside round 94) and `trail-ids.txt` (1 B, mtime 2026-11-06 20:36, inside round 90) were
untracked at `/home/vgpnk/Projects/shokunin/`; the round-97 spot-check flagged them.
Evidence: `git -C /home/vgpnk/Projects/shokunin status --porcelain` listed both; their bytes are
`x\n` and `,`.
Captured-by: the round-97 spot-check (defect 6), not the sweep that ran in round 97.
Fix: copied byte-exact into `.ufo/waves/round-98/misroot/` (`cmp` clean), the fleet copies deleted, and
the sweep re-run.
Shown able to fail: `cmp` exited 0 before the deletion; the fleet status no longer lists them.

**M98-7 - the probe's "single printf" record was not atomic, and multi-spawn cases interleaved.**
Class: control-input concurrency defect (M98-1's family, in the oracle this time). Two children appending
to one file interleaved line by line, so the parser dropped the first record and mis-assigned the second.
Evidence: R98MMutC1 measured the raw bytes (`@@@ 2` twice, then `P0` twice, `A1` twice, `A2` twice) and
R98MExecScoutExec measured 1/20 torn records under load; the first control family's multi-launch rows
were affected.
Captured-by: R98MMutC1's cross-check of the oracle builder; the L1's own control had used one child per
case and did not see it.
Fix: per-spawn record files with a lock-assigned sequence number (`flock`), read in sequence order.
Shown able to fail: the shared-file form produced a visibly torn record in 1/20 runs; the per-file form
25/25 clean.

**M98-8 - the counter and the oracle materialised the same case from different bytes.**
Class: shared-contract drift between two instruments (the `QUALITY.md` 164 class, applied to a fixture).
The oracle wrote `case.desktop` with literal values; the counter wrote `t.desktop` with GKeyFile escaping,
so an Exec carrying one backslash was a refusal under the oracle's bytes and a success under the
counter's, and every `%k` expect named the wrong filename.
Evidence: R98MMutC1 read both drafts; the L1 ruled the oracle's renderer normative and pinned its sha256.
Captured-by: the mutation tester's cross-read, not either instrument's own checks.
Fix: one renderer (`render_desktop`, pinned `renderer_sha256`), one filename (`case.desktop`), literal
values plus a `desktop_raw` branch.
Shown able to fail: a case with `Exec=... a\ b` (one backslash) refuses under the oracle bytes and
launches under the escaped bytes.

**M98-9 - a frozen case carried a refusal expect for a desktop block that renders a valid file.**
Class: label/input inconsistency in a frozen control (M96-1's family). `bad-06-not-keyfile` had a valid
`[Desktop Entry]` block and no `desktop_raw`, so the materialised bytes launch, while the expect said
`desktop-file`.
Evidence: R98MMutC1's baseline (61/64) and R98MExecOracle's re-freeze; the raw bytes that produced the
refusal were never in the file.
Captured-by: the mutation tester's run of the candidate over the frozen cases.
Fix: the case carries `desktop_raw` with the exact bytes; the oracle freezes a label only when two
consecutive measurements agree.
Shown able to fail: the pre-fix file's `bad-06` expect is `desktop-file` while the rendered bytes launch.

**M98-10 - the frozen expect ordered a multi-spawn launch as if the order were observable.**
Class: a race frozen as a value (M98-1's family). The children run concurrently, so the shared-append
order was completion order; the same `%f` three-file launch produced a,b,c and a,c,b across runs, and the
lock-assigned sequence is not fork order either.
Evidence: R98MMutC1's f-04/n-03 order findings and R98MExecScoutExec's 3/3 inversion under a delayed
first child.
Captured-by: the mutation tester's reference model and the scout's load test.
Fix: rule 7 - the surface is the launch count and the MULTISET of argv vectors; the counter compares
sorted vectors.
Shown able to fail: the same launch read a,b,c and a,c,b on two runs.

**M98-11 - the declaration's `%i` rule omitted the extension strip and its absolute-path exception.**
Class: a source rule stated without its guard (M98-2's family). `%i` strips `.png`/`.xpm`/`.svg` only
when the Icon is not an absolute path (`gdesktopappinfo.c:2036-2055`).
Evidence: R98MExecOracle measured `Icon=ic.png` -> `--icon ic`; R98MReviewC1 measured
`Icon=/tmp/ic.png` -> `--icon /tmp/ic.png`.
Captured-by: the oracle's case run and the reviewer's model probe.
Fix: rule 3 states both.
Shown able to fail: the two measured rows above.

**M98-12 - the C2 counter is not idempotent on a reused scratch root.**
Class: tooling defect (scratch hygiene). A second run with the same `--scratch-root` dies
`FileExistsError … planted-r1/corpus`.
Evidence: the L1's second C2 measurement attempt (the first had succeeded).
Captured-by: the L1's re-run, not the counter's selftest.
Fix: the receipt uses a fresh scratch root; the counter should clear or version its planted dirs next
round (routed).
Shown able to fail: the second run exits 1 on `FileExistsError`.

## Gate

### Registry rows (opened 2026-11-07; the L1's fetch receipt is
`.ufo/waves/round-98/receipts/sources-open-r98.txt`)

| id | locator | access | located quote | line |
|---|---|---|---|---|
| S528 | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/gdesktopappinfo.c (HTTP 200, 163369 B, sha256 8e9ce1a8327a2daf6bc16e8dcfb653c482afde7bebc2ca2621747626b5495b0d); host package glib2 2.90.1-1 | 2026-11-07 | `/* If there is no macro default to %f. This is also what KDE does */` | gdesktopappinfo.c 2738 |
| S529 | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gshell.c (HTTP 200, 21464 B, sha256 640a0d0fbc9c50d0c70eb8f9ff2c4994392515c6174f76ade9292d7500e60442); host package glib2 2.90.1-1 | 2026-11-07 | `We always use single quotes, because the algorithm is cheesier.` | gshell.c 202 |
| S530 | Desktop Entry Specification, "The Exec key" - https://specifications.freedesktop.org/desktop-entry/latest/exec-variables.html (HTTP 200 after the 301 from `.../desktop-entry-spec/latest/exec-variables.html`, 17153 B, sha256 2c50a9e427b295928d2b05a19049ab74db18e5d11567c0bd14a8f0f70635277e) | 2026-11-07 | `Arguments may be quoted in whole. If an argument contains a reserved character the argument must be quoted.` | exec-variables.html |
| S531 | `gio(1)` manual, GLib 2.90.1 - file:///usr/share/man/man1/gio.1.gz (installed page: no HTTP status for a `file://` locator; container sha256 810077be12cf2df5006db1e1b9b967f6c505930033c68aa9cfc964281906a565, 4961 B; decompressed sha256 84b3cdad868feecd69f113b789d7009113e16531b67d750cd0e424ba2bcb8bc5, 18793 B, 781 lines); owner `pacman -Qo` = glib2 2.90.1-1 | 2026-11-07 | `Launch a desktop file from any location given.` | gio.1 221 |
| S532 | https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/gio-tool-launch.c (HTTP 200, 3991 B, sha256 16b4c8683b00407670f600eda0e65e9d929a59daac499cbe8f3d1fd532f6595a); host package glib2 2.90.1-1 | 2026-11-07 | `args = g_list_append (args, g_file_new_for_commandline_arg (argv[i]));` | gio-tool-launch.c 116 |

S528 duplicates S518/S521/S505/S526's URL under a new scope, S531 duplicates S527's page under a new
scope, and the census's W04 warnings are expected for both. Every quote is a whitespace-collapsed line
of the fetched bytes and is <= 25 words.

### Rows touched

The old -> new log is derived from base `35f3ce80` to the final registry (not from the working map,
which grouped three items and mismatched eight `new` values): `.ufo/waves/round-98/controls/readback-repair-log-r98.json`
has one entry per changed cell - 23 cells, 24 added `used-by` paths:

- **16 repaired `used-by` cells, 21 added paths** (the status-aware R4 pairs): S457, S459, S460, S464,
  S465, S466, S470, S481, S484, S485, S493, S501, S502, S511, S512, S517. Each cell gains exactly the
  entry that cites it (S460 gains `bar-footprint-allocation-r82.md` and `bar-footprint-rounding-auto-r81.md`;
  S464 gains three; S470 gains three; the rest one each).
- **3 held rows gain the C1 entry**: S504, S506, S527 gain `corpus/knowledge/gio-exec-argv-r98.md` in
  `used-by` only; no anchor, digest, scope or status cell moves.
- **4 new rows** S528-S531 (tier A), `used-by` correct from birth.
- The two disowned citations are **not** repaired and carry no used-by: S030 (`rejected`; the entry's
  round-13 erratum maps every S030 citation to S017) and S132 (`queued`; the entry says it "stays queued
  and supports nothing").
- The round-97 spot-check's S523 repair (a path moved from `recheck` to `used-by` by `a1408d47`) is
  logged here old -> new: `recheck` was `corpus/knowledge/mime-textdb-magic-r96.md` (a path in the
  cadence cell) and is now `180d`; `used-by` gained that path.

### Candidates considered (round 98)

| candidate | decision | reason | flip |
|---|---|---|---|
| `corpus/knowledge/gio-exec-argv-r98.md` | **admit** (if the entry's rules all cite a located line or an oracle-labelled probe row) | the C1 surface is new to the coverage map (no lane tool answered a launch argv at base) | a GLib tag that changes the expansion |
| S528-S532 | **admit** | each is HTTP 200 at the recorded URL (S531 an installed page with its owning package), digests re-measured, quotes located and <= 25 words | a newer GLib pin |
| the `#`-bypass branch as a model rule | **reject as a model fact** | unobservable through `gio launch` (M98-2): a local file URI's fragment is dropped before `expand_macro_uri`; for a non-local URI both branches answer the URI | a caller that passes a URI with a fragment |
| `Hidden=true` as a refusal | **reject as a model fact** | measured launch (M98-4); the check lives in the desktop-id lookup, not the filename constructor | a launch path that consults Hidden |
| `%d`/`%n`/`%N` as unimplemented (the spec says Deprecated) | **reject as a model fact** | GLib 2.90.1 implements them (expand_macro cases 'd'/'n'/'D'/'N'); measured `%d` -> dirname, `%n` -> basename | a GLib tag that drops them |
| the spec's `%i` "two arguments" wording | **reject as a model fact** (admit the observation) | GLib appends `--icon ` + the quoted icon as one string, which the shell parse splits into two argv entries; the spec's "two arguments" describes the result, not the append | a spec revision that matches the implementation's wording |

## Census

- Start: 462 rows at base `35f3ce80` (`.ufo/waves/round-98/receipts/census-start-r98.txt`, rc 0, 62 W04
  warnings, no E-codes).
- End: 466 rows (`.ufo/waves/round-98/receipts/census-end-r98.txt`, rc 0); the four new rows
  (S528-S531) are tier A.
- Rows added: S528-S531 (tier A: two code files, one spec, one installed manual scope).
  Rows touched: 23 `used-by` repairs + the C1 entry's cited rows + S523's recheck/used-by repair.
  Frontier rows advanced: the launch argv (the frontier half of "launch" named since round 91) moves
  into core; whether the process starts, the portal path and `Terminal=true` stay frontier.

## Cross-domain evidence

The desktop-entry launch plane is GIO's (`gdesktopappinfo.c`), the shell grammar is GLib's
(`gshell.c`), and the documented contract is the freedesktop Desktop Entry Specification. The
adjacent lane surfaces are the round-91 default-application plane (which application), round-92
`xdg-open`'s resolver (which file), and round-94's name-to-type step (which type); this round answers
the argv those resolutions would launch with. `file(1)`/libmagic is not this surface.

### Round-97 spot-check closure (append-only, this round)

- **D7 (r96 declaration misquotes r95 routed defect 3).** Closed by restatement: the round-98 C2
  section names the three r95 unguarded tools as the r95 spot-check lists them (`tools/mado-mako.py`,
  `tools/mado-verify.sh`, `quality/check-receipt-presence.py`) and does not substitute
  `tools/mado-mimesniff.py`; the r96 text stays as committed and is superseded by this sentence.
- **D9 (role census drift).** Closed by reporting the census from the registry: round 98's w1 registry
  holds 4 executor + 2 mutation-tester + 1 scout + 1 scribe + 1 connector + 1 reviewer + 1 critic
  (11 seats); re-derived for round 97, `w1/swarm-registry.json` holds 6 executor seats, not the 3 the
  round-97 report said.
- **D5 (S523 used-by/recheck log).** Logged old -> new in this lesson's `### Rows touched`.
- **D6 (fleet leftovers).** `f.txt` and `trail-ids.txt` swept byte-exact into
  `.ufo/waves/round-98/misroot/` and the fleet copies deleted (M98-6).
