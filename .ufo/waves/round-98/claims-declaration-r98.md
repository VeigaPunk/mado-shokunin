# mado round 98 — claims declaration (DRAFT; the L1 freezes it after w1 findings)

Round 98, hyaku run 15, attempt 1 (`MadoR98`). Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`; base revision
`35f3ce808788b11c063309b1b5ad0192754795ea` (branch `master`).

Two claims, two axes, causally separable. Stagnation nudge not claimed: every owned axis sits at
10 and a capability entered the table at rounds 88–97; the lowest-axis duty is a tie, and this
round is a frontier/capability move (AXES.md §The stagnation nudge).

## C1 — coverage: the launch argv GIO builds from a desktop entry's Exec key (capability)

**Surface.** Rounds 91/92/94/95/96/97 answered *which* MIME type and *which* application; the
frontier bullet every one of them leaves open is **launch** ("whether the application starts or a
portal answers"). This round moves the first half of launch into core: **the argv GIO 2.90.1 builds
from a desktop entry's `Exec` key and the file/URI arguments handed to `gio launch`** —
`expand_application_parameters` (gdesktopappinfo.c:2700-2750), `expand_macro`
(:2580-2700), `expand_macro_single` (:2507-2555), `expand_macro_uri` (:2557-2578), then
`g_shell_parse_argv` (gshell.c). Whether the resulting process starts, and whether a portal answers
instead, stays frontier.

**Candidate.** `tools/mado-execargv.py` (read-only, stdlib only, no subprocess in the candidate):

```
mado-execargv.py DESKTOP [FILE...] [--json]
mado-execargv.py --selftest
```

It models, from the desktop file's bytes and the argument list, **the sequence of argv vectors the
launch spawns** (`g_desktop_app_info_launch_uris_with_spawn`'s `do { … } while (dup_uris != NULL)`
loop: a one-URI field code consumes one argument per iteration, so N arguments mean N spawned
processes, each with its own argv):

1. The `[Desktop Entry]` group read: `Type`, `Name`, `Icon`, `Exec`, `Path`, `Terminal`, `Hidden`
   (read, **not** refused: `gio launch` builds the app info from the filename, and the only launch-path
   hidden check sits in the desktop-id lookup path, gdesktopappinfo.c:2209). A file without an `Exec`
   key refuses (`MADO_EXECARGV: ERROR no-exec desktop=...`, exit 2); a file that is not a key file
   refuses (`... ERROR desktop-file ...`, exit 2) - including a value carrying a GKeyFile escape
   outside `{s,n,t,r,\\}` (measured: `a\ b`, `a\z`, `a\:b`, `"a\"b"` all make `gio launch` print
   `Unable to load application information`, rc 1) and a file with no `Type` key (measured: refused,
   `desktop-file`). An Exec the load-time `g_shell_parse_argv` rejects refuses with cause `exec-parse`
   (measured: an unterminated quote).
   The argument step before expansion: `g_file_new_for_commandline_arg` turns each FILE argument into
   a GFile; for a local path or a `file://` URI the GFile's URI is derived from the path, so a
   fragment or query on a local file URI is **dropped** (measured: `%u` + `file://…/a.txt#frag` -> the
   path). A non-local URI keeps its bytes.
2. The Exec line walk is **byte-wise on the raw Exec value** (not on decoded code points): `%X` is a
   field code and the byte after `%` is **consumed** as the selector
   (measured: `100% done` -> `100done`, `a%1b` -> `ab`); a `%` that is the last byte is a literal `%`;
   every other byte is copied. The expansion appends to one string; the string is then parsed by
   `g_shell_parse_argv`'s grammar (whitespace splits, `'...'` literal, `"..."` with backslash
   escapes, `\` escapes the next byte outside quotes, an unterminated quote is an error).
3. Field codes, in the order the walk meets them:
   - `%f`/`%u`/`%d`/`%n`: consume **one** argument (nothing when none is left); append
     `g_shell_quote(value)`. On a non-local URI `%f`/`%d`/`%n` append **nothing** (the value is
     NULL).
   - `%F`/`%U`/`%D`/`%N`: consume **every** remaining argument, each `g_shell_quote`d and
     space-joined; nothing when none is left. On a non-local URI `%F`/`%D`/`%N` consume and **drop**
     it; the separator is emitted only after a non-NULL expansion (measured: `x%F` -> `x/abs/a.txt`).
   - `%u`/`%U`: the argument is first passed as a file path when the GFile has a local path (the
     `force_file_uri` rule), else as the URI itself. The `#`-bypass branch of `expand_macro_uri` is
     **not observable** through `gio launch` (a local file URI's fragment never reaches it, and for a
     non-local URI both branches answer the URI); the tool models the observable rule and the
     declaration records the branch as a named limit.
   - `%i`: `--icon ` + `g_shell_quote(<the themed icon name>)` when Icon is set (measured:
     `Icon=ic.png` -> `--icon ic`); the `.png`/`.xpm`/`.svg` strip applies only when the Icon value is
     **not an absolute path** (measured: `Icon=/tmp/ic.png` -> `--icon /tmp/ic.png`); an empty Icon
     still emits `--icon ` + `''`.
   - `%c`: `g_shell_quote(<the locale-selected Name>)` (measured: `Name[en_US]` wins under
     `LC_ALL=en_US.UTF-8`); `%k`: `g_shell_quote(<canonicalized absolute desktop path>)`.
   - `%m`: nothing (deprecated). `%%`: a literal `%`. Any other `%X`: nothing (no error).
4. The no-substitution rule: the test is **head-pointer equality** on the URI list, not a consumption
   count - so a non-consuming macro (`%c`/`%i`/`%k`/`%m`/an unknown code) still triggers the fallback
   (measured: `Exec=probe %c` + one file -> `[probe, 'Probe App', <file>]`); one space and a `%f`
   expansion are appended (so only the **first remaining** argument is used).
5. `g_shell_quote` is always single-quote with `'` -> `'\''`.
6. The iteration rule: repeat the whole expansion while arguments remain, each iteration consuming
   what its codes consume (measured: `%f %f` + 3 args -> 2 launches; `%f %F` + 3 -> 1; a `%F`-only
   Exec spawns once; a `%f` Exec spawns once per argument; an Exec with no consuming code spawns once
   per argument through rule 4; with no arguments, exactly one launch). `%u`/`%U` flip to the URI form
   when the desktop file carries `X-GIO-NoFuse=true`.
7. Scoring rule: the launch **count** and the **multiset** of argv vectors are the surface; the order
   of launches is not (the children race, and the probe's lock-assigned sequence number is not fork
   order - measured: the same `%f` three-file launch produced a,b,c and a,c,b across runs). The tool
   prints its launches in model order; the counter compares sorted vectors.

Output on stdout:

```
MADO_EXECARGV: launches=3
LAUNCH 1: argc=2
ARGV[1][0]=/abs/probe
ARGV[1][1]=/abs/a.txt
LAUNCH 2: argc=2
...
```

exit 0 on success; 2 on a refusal with one line `MADO_EXECARGV: ERROR <cause> detail=<...>` (causes:
`no-exec`, `desktop-file`, `exec-parse`). `--json` prints
`{"launches":N,"argv":[[...],...]}` (or `{"error":"<cause>","detail":"..."}`). `--selftest` runs its
own checks over fixtures it builds under a temp dir and prints `MADO_EXECARGV_SELFTEST: checks=N failed=M`
(exit 0 green / 1 failed).

**Oracle.** The installed `/usr/bin/gio` (`gio launch DESKTOP FILE...`) with a fixture probe child
whose `Exec` first token is a shell script that records its own argv to `<script>.out`. The probe
never reads a host file, never touches the network, and is created inside the case root.

**Frozen case file** (`.ufo/waves/round-98/controls/execargv-cases-r98.json`):
`{"version":1,"oracle":"gio launch + probe child argv records","gio_sha256":<pin>,"glib2":"2.90.1-1","classes":[...],"cases":[...]}`.
Case: `{"id","class","desktop":{"Name","Icon"|null,"Type","Exec","Path"|null,"Terminal"|null,"Hidden"|null,"X-GIO-NoFuse"|null},"desktop_raw":"<exact file bytes>"|absent,"args":[{"kind":"file","path":"<rel>"}|{"kind":"uri","uri":"<abs uri>"}],"files":{"<rel>":"<b64>"},"expect":{"launches":N,"argv":[[...],...]}}`.
The oracle waits for a **2 s quiet window** (cap 20 s), not 200 ms: `gio launch` returns before its
children write (measured: gio exits at 0.003 s, a child's record appears at 1.0 s, and a 200 ms window
truncated a 1.5 s-delayed write in 4/4 trials). The probe child takes a lock-assigned sequence number (`flock` on `<probe>.lock`, counter in
`<probe>.seq`) and writes one record file `<probe>.out.<n>` per spawn (`@@@ <argc>`, `P0=<argv0>`, then
`A<i>=<value>` lines); the oracle waits for the record set to be quiet for 2 s (cap 20 s) and parses
`<probe>.out.<1..N>` in sequence order. The recorded argv includes argv[0] (`P0`).
`X-GIO-NoFuse` is a desktop key the case may set (`true`/`false`); `desktop_raw`, when present, is the
exact file bytes and overrides the rendered block. The desktop file is written as
`<case root>/case.desktop` from the case's `desktop` values **literally**
(no escaping; a value that must carry a backslash or a newline is supplied through `desktop_raw`, the
exact file bytes), and the counter materialises the case with the SAME renderer and the SAME filename -
the oracle's `render_desktop` is normative and its sha256 is pinned in the case file header. The
`expect` is normalised by the case root only; the desktop filename is fixed, never rewritten. A case whose `gio launch` exits nonzero or writes no record is a REFUSAL
case: `expect` is `{"error":"<cause>"}` and the tool must exit 2.
`{probe}` in `Exec` is substituted with the absolute probe path at case build time; `{root}` in a
path is the case root. Every `expect` was recorded by `/usr/bin/gio` at the freeze, never by the
author.

**Classes (20, each >=3 cases; >=70 cases total):** `plain` (no field code, 0/1/2 args),
`f` (`%f` 0/1/2 args), `F` (`%F` 0/1/3 args), `u-file` (`%u` with a file argument),
`u-uri` (`%u` with an http URI), `u-anchor` (`%u`/`%U` with a `file://` URI carrying `#frag`: the
fragment is dropped by the GFile conversion, the path is used), `U-mixed` (`%U` file+URI), `d`
(`%d`), `n` (`%n`), `i` (`%i` with, without and with an absolute Icon),
`c` (`%c`, including a `Name[en_US]` locale case), `k` (`%k`), `pct` (`%%`, trailing `%`, `% `),
`bad` (`%z`, `%q`, `%1`), `nonlocal` (`%f`/`%F` with a non-local URI), `nofuse`
(`X-GIO-NoFuse=true`), `multilaunch` (`%f %f`, `%f %F`), `comment` (a `#` comment line in the
desktop file), `quote`
(single/double quotes and a `\\`-escaped backslash in Exec; an invalid escape is a refusal case),
`path` (a file name with a space and one with `'`).

**Counter** `quality/counters/c1-r98-execargv.py`, predicate **PRED-C1-r98-v1** (the same sentence
is the receipt label):

> TARGET_MET iff, at `--rev`, `tools/mado-execargv.py` is the frozen candidate
> (`tool_sha256 == --expect-tool-sha256`, printed `tool_pin=ok`) and, run under an empty PATH through
> the audit launcher with the structural allowlist (no process, socket, network or non-libc dynamic
> import; no sibling lane module), it answers (i) every frozen case exactly (`correct == cases`) over
> the declared 20 classes (`classes == 20/20`, each class >=3 cases, >=70 cases total); (ii) every
> frozen mutant killed (`killed == mutants`) and every class kills at least one mutant
> (`class_kills == 20/20`); (iii) every fresh seeded case exactly (`fresh == fresh_total`, >=40,
> fixtures generated at measurement time by a frozen generator, labels from the same oracle);
> (iv) the oracle is the installed `gio` (`--expect-gio-sha256`) and the case file's pinned renderer
> (`renderer_sha256`), and every frozen label was produced by this binary through that renderer at the
> freeze, a label being frozen only when two consecutive measurements agree; (v) the controls stay
> behind: three DISTINCT models - a naive `Exec.split()` with no field-code expansion, a
> field-code model that expands `%f`/`%F` but ignores quoting and iteration, and a memoriser - each
> score strictly fewer than the total on the frozen cases, and the memoriser scores 0 on the fresh
> leg;
> and (vi) the candidate's `--selftest` is green (`checks=N failed=0`, N >= 12).
> rc 0 TARGET_MET, 1 TARGET_MISSED, 2 SETUP_ERROR.

**Before.** At base `35f3ce80`: no lane tool answers a launch argv
(`git cat-file -e 35f3ce80:tools/mado-execargv.py` → absent; `git grep -il 'expand_macro\|g_shell_parse_argv' 35f3ce80 -- tools/` → nothing), so 0 of 0 cases are answered; the frontier bullet
names launch as open.

**Do-nothing control (measured before the freeze, receipt committed).** Measured 2026-11-07 on a
23-case probe family over 16 classes (`receipts/control-naive-r98.json`): a model that answers one
launch of `Exec.split()` (no quoting, no field codes, no iteration) scores **2/23**, and a model that
leaves the field-code tokens literal scores **2/23** — both strictly fewer than the total, so the
frozen counter's control clause holds. The two matches are the cases whose Exec has no field code and
no quoting (`plain-01`, `pct-02`).

## C2 — operability: the SOURCES registry's citation read-back (a new gate, and the 21 defects it finds)

**Surface.** Round-97's outside spot-check routed defect 5: `a1408d47` moved
`corpus/knowledge/mime-textdb-magic-r96.md` from S523's `recheck` cell into its `used-by` cell with no
old→new log, and it asked for "a registry read-back that catches a path landing in the recheck cell
(the census's `NF` test is blind to it)". The fleet census (`scripts/sources-census.sh`) checks row
shape, id/URL duplicates, enums, `E09` recheck validity and `E11` used-by existence — it never reads
**back** from an entry's `source:` frontmatter to the row's `used-by` cell. This round adds that
read-back as a committed gate.

**Candidate.** `quality/check-sources-readback.py` (read-only, stdlib only):

```
check-sources-readback.py --repo DIR [--json]
check-sources-readback.py --selftest
```

Rules (each finding is one line `SOURCES_READBACK: FINDING <rule> <id> <detail>`):

- `R1 recheck-path`: a row whose `recheck` cell contains `/` or ends `.md` (a repo path in the
  cadence cell).
- `R3 usedby-missing`: a `used-by` path that does not exist on disk (compared after
  `posixpath.normpath`; `-` and `—` are empty). A `used-by` path outside `corpus/` is legitimate
  (the registry cites `.ufo/waves/...` artifacts and `SKILL.md`: 21 such cells at base, all
  legitimate), so there is no R2.
- `R4 entry-cites-unacknowledged`: an id in a `corpus/knowledge/*.md` entry's `source:` frontmatter
  whose row has `status: mined` and whose `used-by` cell does not name that entry. The frontmatter
  scope is pinned: the `source:` entries of the frontmatter block, including indented `  - Sxxx`
  continuation items and wrapped continuation lines, and no `source:` line after the block. An id
  counts only when it is a standalone token (not preceded by `/`, not followed by `.`/`-`/`_`), so a
  receipt path such as `.ufo/waves/round-37/fetch/S213.receipt.txt` is not a citation. One finding
  per (row, entry) pair, never per occurrence.
- `R5 entry-cites-missing-row`: an id in that frontmatter with no registry row.
- `R6 duplicate-id`: a row id that appears twice.

Result line `SOURCES_READBACK: rows=N entries=M findings=K`; exit 0 clean / 1 findings / 2 setup.
`rows` counts 11-column registry rows; `entries` counts `corpus/knowledge/*.md` files.

**Counter** `quality/counters/c2-r98-sources-readback.py`, predicate **PRED-C2-r98-v1**:

> TARGET_MET iff, at `--rev`, `quality/check-sources-readback.py` is the frozen candidate
> (`gate_pin=ok`), its `--selftest` is green (`checks=N failed=0`, N >= 10) with stable finding ids,
> and (i) at `--base-rev` the gate is absent (`git cat-file -e <base>:quality/check-sources-readback.py`
> → absent, printed `base_gate=absent`) while the counter's own independent status-aware R4 pass over
> the base registry counts `base_mismatches`, which must equal `--expect-base-mismatches` (21) and
> `--base-rev` must differ from `--rev`; (ii) at `--rev` the gate runs on an extracted `--rev` tree
> whose `corpus/SOURCES.md` sha256 equals `git show <rev>:corpus/SOURCES.md`, reports `findings=0`,
> and its `rows`/`entries` equal the counter's own parse; (iii) the repair is complete **row → entry**:
> the counter's independent status-aware R4 pass over `--rev` counts 0, every base mismatch's row now
> names that entry, the set of entry paths at `--rev` equals the set at `--base-rev`, each entry's
> citation set at `--rev` is a superset of its base set, and the number of `used-by` paths added at
> `--rev` equals `repaired` (each added path is exactly a mismatch entry); (iv) the gate fails closed
> on planted defects cut from the `--rev` registry: one stripped `used-by` cell -> exactly one `R4`
> finding naming the planted entry, one path in a `recheck` cell -> exactly one `R1`, one dangling
> `used-by` -> exactly one `R3`, one duplicated id -> exactly one `R6`, one missing row -> exactly one
> `R5`, each with the planted id and exit 1, and a committed always-clean stub gate is rejected
> (`stub_flagged=1`); (v) the fleet census still validates the committed registry
> (`sources-census.sh validate --root ... mado` exit 0, W-codes allowed).
> rc 0 TARGET_MET, 1 TARGET_MISSED, 2 SETUP_ERROR.

**Before.** At base: no read-back gate exists (`git cat-file -e 35f3ce80:quality/check-sources-readback.py`
→ absent), and the counter's independent status-aware R4 rule counts **21** entry→row citations the
registry does not acknowledge (measured this round; the list is the counter's `base_mismatches` output
and is committed as a receipt). Two further base pairs (S030, S132) are citations the entries' own
bytes disown (S030's erratum maps every S030 citation to S017; S132 "stays queued and supports
nothing"), so a status-aware R4 does not require them and no used-by is written for them.

**Do-nothing control (measured before the freeze).** R98MCriticC2 measured four no-work shapes on the
base extraction: deleting the citations (findings 0, repaired 0), deleting the entries (entries
118 → 109), rewording a citation to an already-acknowledged row (one pair disappears), and a shotgun
that acknowledges every mismatch entry on every row (4095 added paths against 21). The predicate's
(iii) closes all four: `repaired` is row → entry, the entry-path set is pinned, each entry's citation
set is a superset of base, and `added_paths == repaired`. A stub gate is caught by (iv).

## Separability

C1 lands `tools/mado-execargv.py` + its counter + cases/mutants; C2 lands
`quality/check-sources-readback.py` + its counter + the 23-cell repair. Each counter is run at the
other claim's revision: C1 at the C2 tip (the tool and its inputs are unchanged there) and C2 at the
C1 revision (the gate is absent there → `SETUP_ERROR`/`TARGET_MISSED` as declared).

## Sources (opened this round; the L1's fetch receipt is `receipts/sources-open-r98.txt`)

- `gdesktopappinfo.c` — https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/gio/gdesktopappinfo.c
  (HTTP 200, 163369 B, sha256 `8e9ce1a8…`); scope: the launch argv expansion.
- `gshell.c` — https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gshell.c (HTTP 200, 21464 B,
  sha256 `640a0d0f…`); scope: `g_shell_quote` and the `g_shell_parse_argv` grammar.
- Desktop Entry Specification, "The Exec key" — 
  https://specifications.freedesktop.org/desktop-entry/latest/exec-variables.html (HTTP 200 after the
  documented 301 from `.../desktop-entry-spec/latest/exec-variables.html`, 17153 B, sha256
  `2c50a9e4…`); scope: the documented field codes and quoting.
- `gio(1)` installed page (`file:///usr/share/man/man1/gio.1.gz`, glib2 2.90.1-1) — a new scope on
  S527: the `launch` command's argument form.
- `corpus/SOURCES.md` itself and `scripts/sources-census.sh` (own-work, held S004) for C2's rule
  ground.

## Wave shape (declared before dispatch)

One v1 wave `w1`, 10 seats: 1 scout, 3 executors, 1 scribe, 1 connector, 1 reviewer, 1 critic,
2 mutation-testers. Attack share 4/10 = 40 %. The L1 holds the §3 planner seat (the validator
rejects `planner`); no residual call is planned.

## Freeze block (2026-11-07; the L1's pins, measured on the frozen bytes)

The declaration above is frozen at these pins. Every value is the sha256 of the bytes committed at the
artifacts commit; a counter refuses SETUP on any mismatch.

| artifact | path | sha256 |
|---|---|---|
| C1 candidate | `tools/mado-execargv.py` | `49f7fecdc3bef99a077fe73ac12f5fe211d7ae8c41df5ddc949daf685405f713` |
| C1 counter | `quality/counters/c1-r98-execargv.py` | `7ed2f8f62ca9bb0fe2706f1e6c09ad20d6276404f7f5112507842b0eee0a64c5` |
| C2 gate | `quality/check-sources-readback.py` | `f1000bf11e88149695aa96229fcf2155929ebbb72a2cfa215d8c24e2f37bd8f5` |
| C2 counter | `quality/counters/c2-r98-sources-readback.py` | `e944fdacd1285a44e3026b0c8ccccf9dce5f6ec687ec047c2327e8cec61e6e0a` |
| C1 cases | `.ufo/waves/round-98/controls/execargv-cases-r98.json` | `21cccc3ad94e99dff9cdb281a38b32579e9d3e6be14799a83b09499e466e370e` |
| C1 mutants | `.ufo/waves/round-98/controls/execargv-mutants-r98.json` | `32c207b32d8aa6126ee949383e7ab992f53c76369310a3e7d88c2b6240ce53bb` |
| C1 fresh generator | `.ufo/waves/round-98/controls/execargv-fresh-r98.py` | `b7bc137a643c771f1cd88a3909d1650205b37a155869ade84adc419e3515357c` |
| C1 renderer/oracle builder | `.ufo/waves/round-98/controls/execargv-probe-r98.py` | `182cf06cecf1a9d19436d18ca26792568839b6d4e2be7e6dce880d19ea88e3d4` |
| C2 mutants | `.ufo/waves/round-98/controls/readback-mutants-r98.json` | `78b7840b3b63a1c256f3093f0876f8e80a5ef0a51b9a74f3eba96c088826885d` |
| C2 planted manifest | `.ufo/waves/round-98/controls/readback-planted/manifest.json` | `52238a4cf8196b7cbbe392376b5a36967034a86a4ccf79cf21800632ea7cd339` |
| C2 stub gate | `.ufo/waves/round-98/controls/readback-planted/stub-always-clean-gate.py` | `cb2c9a9edc3239ad42636eecebb57910fb0345be34b79fa373f0179015acbff8` |
| oracle binary | `/usr/bin/gio` (glib2 2.90.1-1) | `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462` |

Case file: 88 cases, 20 classes (each >=3), every label frozen on two consecutive agreeing
measurements; `renderer_sha256` in the header equals the renderer pin above. The declaration's
predicate sentences, the counter's code and the receipt labels are the same sentences.

Pre-freeze corrections folded in (all measured this round, each with its witness in
`corpus/lessons/round-98.md`): the launch-sequence surface (M98-1), the unobservable `#` branch
(M98-2), the GKeyFile escape refusal (M98-3), `Hidden` read-not-refused (M98-4), the selector byte
consumption, the non-local-URI rules, the head-pointer fallback, the icon extension strip (only when
not absolute), the byte-wise walk, `X-GIO-NoFuse`, `exec-parse`, the 2 s quiet window, and the
multiset scoring rule.
