# R98MExecOracle — C1 oracle case builder, frozen class suite, fresh generator

Round 98, hyaku run 15, wave w1, seat report. Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`; base `35f3ce808788b11c063309b1b5ad0192754795ea`.
Every measured cell below is from this seat's runs on this host (gio sha256
`d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462`, glib2 2.90.1-1)
unless a peer measurement is named as such. The declaration was amended twice
mid-wave (20-class schema, then the R98MReviewC1 folds); the freeze below is
against the final text.

## Axes (godspeed)

- **coverage** — 20 declared classes, 88 frozen cases (>=70), every listed coverage edge present,
  each class >=3.
- **oracle fidelity** — zero hand-written expects: every `expect` is what `/usr/bin/gio` did at
  freeze time, and per declaration predicate (iv) every frozen label was produced by **two
  consecutive agreeing measurements** (3-attempt cap; none needed a third).
- **determinism** — canonicalized expects (`{root}`/`{probe}`), sorted argv vectors (rule 7),
  seeded fresh generator, renderer sha pinned.
- **instrument robustness** — probe protocol survived three measured defects (below), each fixed
  before any byte was frozen; the reader window was raised to the declared 2 s/20 s after the
  declaration measured a 200 ms window truncating a 1.5 s-delayed write 4/4 trials.

## Deliverables (all committed this wave)

| file | role |
|---|---|
| `controls/execargv-probe-r98.py` | oracle case builder — **instrument** (spawns `/usr/bin/gio`; QUALITY 162/165 exemption; stdlib only) |
| `controls/execargv-cases-r98.json` | the frozen 20-class suite (contract 2 header + 88 cases) |
| `controls/execargv-fresh-r98.py` | fresh seeded generator — **instrument** (imports the builder by pinned path; spawns gio per case) |

The **candidate** (`tools/mado-execargv.py`, seat R98MExecTool) has no subprocess/process
exemption; these three files are instruments, not candidates.

## Oracle protocol (final, per the amended declaration)

1. Materialise `<root>/case.desktop` (name constant `case.desktop`; values written **literally**,
   no escaping — the case's Exec string is already the exact post-unescape bytes GKeyFile must
   see; `desktop_raw` replaces the whole file when exact bytes are needed) and `<root>/probe.sh`
   (0755), plus base64 `files` (`/`-suffixed keys are directories) and an `h/` HOME.
   The renderer key order is normative and pinned: `Type, Name, Icon, Exec, Path, Terminal,
   Hidden, X-GIO-NoFuse` (None keys omitted; `X-GIO-NoFuse` is the schema's 8th desktop key,
   emitted last).
2. `env -i LC_ALL=C HOME=<root>/h PATH=/usr/bin:/bin /usr/bin/gio launch <root>/case.desktop
   <args...>`, cwd = case root, 10 s timeout.
3. Probe child (exact `PROBE_SH`, flock sequence numbers, one record per spawn):

```sh
#!/bin/sh
# mado r98 launch probe: write one argv record per spawn to $0.out.<seq>.
# Sequence numbers are taken under a lock, so file order is spawn order.
exec 9>"$0.lock"; flock 9; n=$(cat "$0.seq" 2>/dev/null || echo 0); n=$((n+1)); echo "$n" > "$0.seq"; flock -u 9
{ printf '@@@ %s\n' "$#"; printf 'P0=%s\n' "$0"; i=1; for a in "$@"; do printf 'A%d=%s\n' "$i" "$a"; i=$((i+1)); done; } > "$0.out.$n"
```

4. The builder waits for the `.out.<seq>` set to go quiet (**2 s quiet window, 20 s cap** — the
   declaration's normative sentence; its case-file paragraph still carries the stale "200 ms of
   no change, 8 s cap" phrasing, see Risks), requires exactly one sealed record (`@@@ <argc>` +
   `P0=$0` + `A1..A<argc>`) per file, and reads it in sequence order. An unsealed/incomplete
   record set at the cap is `{"error":"setup-error"}` — an instrument failure, never a refusal
   label and never freezable (predicate iv); `meta` carries `record_state`/`setup_error`.
5. Refusal = `gio launch` exits nonzero **or** no record appears at all (rc 0, `record_state
   "empty"`). The cause is derived structurally from the case and only printed after gio
   confirmed the refusal: missing Exec -> `no-exec`; no `[Desktop Entry]` group, no
   `Type=Application`, or a GKeyFile escape outside {`\s`,`\n`,`\t`,`\r`,`\\`} -> `desktop-file`;
   otherwise -> `exec-parse`.
6. argv values are canonicalized back onto placeholders: the probe path and the case root are
   replaced as substrings anywhere in the value -> `{probe}` / `{root}` (attached codes can
   embed the root mid-token; a prefix-only rewrite leaked a transient path — defect 4).
   **No freeze-time absolute path is in the frozen file** (grep `/fast/|/home/|vgpnk` = 0 hits);
   the counter substitutes `measure_root` in (replaces `{probe}` first, then `{root}`).
7. **Freeze rule (predicate iv):** the suite driver measures each case up to 3 times and freezes
   a label only when two **consecutive** clean measurements agree; a `setup-error` measurement
   yields no label and breaks the chain. All 88 labels froze on the first pair; zero cases
   needed a third attempt; zero setup-errors occurred.

Pins: `gio_sha256 d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462` (re-hashed at
every builder run; mismatch prints `MADO_EXECARGV_PROBE_GIO_MISMATCH` on stderr),
`renderer_sha256 182cf06cecf1a9d19436d18ca26792568839b6d4e2be7e6dce880d19ea88e3d4` = sha256 of
`controls/execargv-probe-r98.py` (embeds `render_desktop` incl. the `X-GIO-NoFuse` key,
`PROBE_SH`, and the `case.desktop` / `probe.sh` name constants), published in the case file
header; cases file sha256 `21cccc3ad94e99dff9cdb281a38b32579e9d3e6be14799a83b09499e466e370e`;
fresh generator sha256 `b7bc137a643c771f1cd88a3909d1650205b37a155869ade84adc419e3515357c`.

## Freeze census (final re-freeze, rule-7 plane, two-measurement rule)

88 cases, 20 classes, zero intent mismatches, zero unfreezable cases: ok=81, refused=7,
spawns=93.

| class | cases | class | cases |
|---|---|---|---|
| plain | 4 | pct | 7 |
| f | 4 | bad | 8 |
| F | 3 | nonlocal | 5 |
| u-file | 3 | nofuse | 4 |
| u-uri | 3 | multilaunch | 3 |
| u-anchor | 5 | comment | 3 |
| U-mixed | 4 | quote | 8 |
| d | 3 | path | 4 |
| n | 3 | i | 6 |
| c | 5 | k | 3 |

(per-class minimum 3 satisfied everywhere; total 88 >= 70.)

Multi-launch reference cells (the L1's requested sequences, sorted plane):
`plain-02` (`Exec={probe} plain`, files a,b) -> launches=2,
`[[{probe}, plain, {root}/a.txt], [{probe}, plain, {root}/b.txt]]`;
`f-03` (`%f`, a,b) -> launches=2, `[[{probe}, {root}/a.txt], [{probe}, {root}/b.txt]]`;
`multilaunch-01` (`%f %f`, a,b,c) -> launches=2, `[[{probe},{root}/a.txt,{root}/b.txt],
[{probe},{root}/c.txt]]`; `multilaunch-02` (`%f %F`, a,b,c) -> launches=1 with all three;
`multilaunch-03` (`%u %u`, file+http) -> launches=1, `[[{probe},{root}/a.txt,
http://example.com/a]]`.

### Probe-protocol defects found and fixed before the freeze

1. **Shared-append interleaving** (measured first by R98MMutC1 on their probe, then observed here
   as `d-03-two` answering rc=0 with zero records while `n-03-two` measured cleanly): two children
   appending one record each to the same file corrupt both; the shell record is not a single
   atomic write. Fixed by per-spawn record files.
2. **Sequence/flock order != fork order** (ruling backed by both seats' data): flock acquisition
   races the spawn loop. This seat's own freeze evidence: run 2 froze `f-04-three` as
   a,c,b; the identical re-freeze froze a,b,c. Ruled unobservable -> declaration rule 7 (launch
   count + multiset of argv vectors, counter compares sorted). Driver and generator now freeze
   sorted vectors.
   A 20x control on the order-invariant `d-03` shape read `('{root}','{root}')` 20/20.
3. **`desktop_raw` dropped from the frozen entry** (found by the L1): `bad-06-not-keyfile` froze
   without the raw bytes, so its refusal was not materialisable from the frozen file. Fixed: the
   frozen entry carries `desktop_raw: "Hello world\n"` (verified in the committed bytes).
4. **`canon()` prefix-only rewrite leaked mid-string roots** (found by R98MExecCounter's
   end-to-end run, fresh case `fresh-07f72045b91a494c-56`): an attached/glued field code can put
   the case root mid-token (`end<root>/f2.txt`), and the prefix-only canonicalization left the
   transient absolute path in fresh output. Fixed post-freeze in `canon()` (probe path and root
   now substitute anywhere in the value; the frozen suite has no mid-string roots, so its expects
   are unchanged — verified by a 64/64 replay of every frozen case through the fixed builder).
5. **Reader window too short for the measured write delay** (declaration, from R98MReviewC1's
   timing data): gio exits at 0.003 s, a child's record appears at 1.0 s, and a 200 ms window
   truncated a 1.5 s-delayed write in 4/4 trials. Fixed before this freeze: `QUIET_S = 2.0`,
   `OUT_CAP_S = 20.0` (the declaration's normative sentence; its case-file paragraph still says
   "200 ms of no change, 8 s cap" — internal contradiction flagged under Risks).

### Refusal cells (measured stderr, quoted)

| case | cause | rc | gio stderr (last line) |
|---|---|---|---|
| bad-04-no-exec | no-exec | 1 | `gio: Unable to launch application '<root>/case.desktop': Desktop file didn't specify Exec field` |
| bad-06-not-keyfile | desktop-file | 1 | `gio: Unable to load '<root>/case.desktop': Key file contains line "Hello world" which is not a key-value pair, group, or comment` |
| bad-07-no-type | desktop-file | 1 | `gio: Unable to load application information for '<root>/case.desktop'` |
| quote-04/05-unterminated | exec-parse | 1 | `gio: Unable to load application information for '<root>/case.desktop'` |
| quote-07-escape-space, quote-08-escape-bad | desktop-file | 1 | `gio: Unable to load application information for '<root>/case.desktop'` |

(The stderr strings embed build-time root paths; the frozen expects do not.)

## Contract-vs-oracle deltas the L1 folded (all measured here, all landed in the declaration)

1. **Hidden=true launches** (bad-05: launches=1, argv recorded; matches R98MMutC1's
   gdesktopappinfo.c:2209 reading — the only hidden check is the by-id lookup, not
   `g_desktop_app_info_new_from_filename`). The frozen case is the measured success; a tool that
   models the old "Hidden refusal" fails bad-05.
2. **`%i` strips a case-sensitive `.png`/`.xpm`/`.svg` suffix only off non-absolute Icons** —
   Icon `ic.png` reaches argv as `--icon ic` (i-01, i-04), Icon `my icon` passes verbatim (i-03),
   Icon `""` still emits `--icon ''` (i-05: argv `[probe, --icon, ""]`), and Icon `/tmp/ic.png`
   keeps its suffix (i-06: `--icon /tmp/ic.png`). No Icon at all emits no `--icon` token (i-02).
3. **Local file URI fragments/queries are dropped before the `#` branch can matter** — `%u` with
   `file://{root}/a.txt#frag` measures as the path `{root}/a.txt` (u-anchor-01); with
   `?q=1#s` both fragment and query vanish (u-anchor-03); `http://example.com/p#y` keeps its
   fragment (u-anchor-02); `%U` with the same file URI also yields the path form (u-anchor-05).
   The declared `#` rule is a named limit, not observable through `gio launch`.
4. **Unknown codes `%z`/`%q` expand to nothing and consume nothing**, so the no-substitution
   default `%f` fires per iteration: bad-01 (`%z`, 1 file) gets its arg via the default;
   bad-03 (`%z`, 2 files) launches twice via the default. bad-02 (`%q %f`) shows `%q` leaving the
   explicit `%f` to consume. The digit selector `%1` behaves the same (bad-08: `%1` + 1 file ->
   `[probe, {root}/a.txt]` via the default).
5. **Trailing `%` is a literal `%` token** (pct-03 `hi %` -> `[probe, hi, %]`; pct-04 ->
   `[probe, %]`); `%%` folds to one `%` (pct-01 `100%`,`sure`; pct-02 attached `a%b`).
6. **The byte after `%` is consumed as the selector** (declaration rule 2): `100% done` ->
   `100done` (pct-06), `a%1b` -> `ab` (pct-07), `% x` -> `x` with the `%`+space both eaten
   (pct-05). The frozen suite pins the ASCII cells; the byte-wise (non-codepoint) walk itself
   cannot be frozen under the ASCII-only artifact rule — named limit for the counter.
7. **GKeyFile escape refusals**: `a\ b` and `a\z` refuse (desktop-file cause); the valid `\\`
   escape `"a\\"b"` is a success case with argv `a"b` (quote-03).
8. **No-Type refuses** with the `desktop-file` cause (bad-07), supporting contract 1's clause.
9. **`%d`/`%n` consume one arg per launch iteration** — `%d` yields the dirname (d-02: `{root}`;
   d-03: two launches), `%n` the basename (n-02: `a.txt`; n-03: two launches). d-03's two vectors
   are legitimately identical — a "vectors must be distinct" check would false-positive.
10. **Non-local URIs** (new `nonlocal` class): `%f`/`%d`/`%n` on http/mailto append **nothing**
    but still consume the argument (nonlocal-01/03/04 -> `[probe]`); `%F`/`%D`/`%N` consume and
    **drop** the non-local URI, and the separator is emitted only after a non-NULL expansion
    (nonlocal-02 `"{probe} %F"` + [http, a.txt] -> `[probe, {root}/a.txt]`, http gone); `%f` with
    [http, a.txt] launches twice — `[probe]` then `[probe, {root}/a.txt]` (nonlocal-05).
11. **`X-GIO-NoFuse=true` flips `%u`/`%U` to the URI form** (new `nofuse` class, structured
    desktop key, no `desktop_raw`): `%u`+file -> `file://{root}/a.txt` (nofuse-01), `%U`+[file,
    http] -> both URI forms (nofuse-02), `%u`+http stays http (nofuse-03, control), and `%f` is
    unaffected — still the path (nofuse-04, control).
12. **`%c` under the frozen `LC_ALL=C` env**: the locale-selected Name falls back to the plain
    `Name` — c-04 (`Name=Base Probe` + `Name[en_US]=US Probe`, desktop_raw) measures
    `[probe, Base Probe]`; with **only** `Name[en_US]` and no plain Name, `%c` appends nothing
    (c-05 -> `[probe]`). The declaration's "Name[en_US] wins" cell is an `en_US.UTF-8`-locale
    measurement (scout's); the frozen oracle env is fixed C, so the suite pins the C-locale
    behavior and the en_US win stays a scout-cited rule, not a frozen cell.
13. **`#` comment lines are accepted anywhere in the desktop file** (new `comment` class):
    before the group (comment-01), between the group header and keys and between keys
    (comment-02), and indented (comment-03) — all launch normally.
14. **Iteration consumption shapes** (new `multilaunch` class): `%f %f`+3 -> 2 launches
    (multilaunch-01); `%f %F`+3 -> 1 launch with all three (multilaunch-02); `%u %u`+[file,http]
    -> 1 launch carrying both expansions (multilaunch-03).

## Fresh generator (contract (iii) draft)

`execargv-fresh-r98.py --seed HEX --dir D --out F --count N` (all four required, no defaults;
deterministic under a seed: no timestamps, numbered case ids `fresh-<seed>-<NN>`). Weighted code
pool (f/u/F/U/i common; d/n/D/N/m/v/%/z/q rarer), literal pool incl. `"a b"`, `'a b'`, `end%`,
`a\ b` (the escape-refusal shape) and `a%1b` (selector consumption); ~8% of cases carry the
structured `X-GIO-NoFuse=true` key; ~1/4 of the rest carry `desktop_raw` bytes (locale
`Name[en_US]` or `#` comment flavors) — the JSONL record gains an optional `desktop_raw` key
with the frozen-file semantics; 0-4 args mixing files (incl. `with space.txt`, `it's.txt`) and
URIs (http/https-query/mailto/`file://{root}/...#s`). Every line's `expect` and `label`
(`ok` / `refusal:<cause>` / `setup-error`) is measured at generation time (setup-error retried
twice, then emitted fail-closed as `setup-error`, never as a refusal); vectors sorted per rule
7. One sibling-module load, pinned by path (QUALITY 165); touches only `case_expect`,
`GIO_SHA256`, `GLIB2` of the builder.

Dry run (seed `98c0ffee`, count 12, scratch, post-amendment grammar):
`FRESH_GEN: cases=12 ok=9 refused=3 setup=0`,
`FRESH_GEN_PIN: gio_sha256=d2164260...cfc462 glib2=2.90.1-1`.

| id | Exec (trunc) | raw | nofuse | label | launches |
|---|---|---|---|---|---|
| fresh-98c0ffee-00 | `{probe} a%1b %D %n` | - | - | ok | 1 |
| fresh-98c0ffee-01 | `{probe}` | - | - | ok | 2 |
| fresh-98c0ffee-02 | `{probe} tok %n %c` | - | - | ok | 2 |
| fresh-98c0ffee-03 | `{probe} %q %c a\ b "a b"` | - | - | refusal:desktop-file | - |
| fresh-98c0ffee-04 | `{probe} end%` | - | - | ok | 2 |
| fresh-98c0ffee-05 | `{probe} a\ b %% tok %d` | - | - | refusal:desktop-file | - |
| fresh-98c0ffee-06 | `{probe} %u` | - | - | ok | 4 |
| fresh-98c0ffee-07 | `{probe} %F a%1b` | - | - | ok | 1 |
| fresh-98c0ffee-08 | `{probe} a%1b "a b" %U %u` | Y | - | ok | 1 |
| fresh-98c0ffee-09 | `{probe} %U a%1b end%` | - | - | ok | 1 |
| fresh-98c0ffee-10 | `{probe} %f %u a\ b "a b"` | - | - | refusal:desktop-file | - |
| fresh-98c0ffee-11 | `{probe} %f 'a b'` | - | - | ok | 4 |

## Cross-instrument evidence

- R98MMutC1's independent reference-model cross-check: 47/47 cases match on the corrected probe
  protocol (their message, this round), covering the same refusal corners the suite freezes.
- R98MExecCounter confirmed the materialiser honours `desktop_raw` verbatim on both the frozen
  and fresh legs, and that their `DESKTOP_KEYS` order already matches the renderer's
  `Type/Name/Icon/Exec/Path/Terminal/Hidden/X-GIO-NoFuse` exactly.
- The L1's own 23-case naive-control family measures 2/23 under the P0 record shape
  (receipt `.ufo/waves/round-98/receipts/control-naive-r98.json`).

## Tooling installs

None. Everything used is preinstalled: python3 (stdlib only in both committed files),
`/usr/bin/gio` 2.90.1 (the oracle), `/usr/bin/flock` (util-linux, in the contract PATH). No
pacman transactions, no PATH-directory writes, no host mutations.

## Hygiene

Write scope held to the three owned files, this report, and scratch
`/fast/scratch/hyaku/mado-r98/R98MExecOracle` (deleted after this report; the dry-run JSONL lives
on in the table above). The three controls files are ASCII-only (verified 0 non-ASCII bytes);
this report uses typographic dashes per seat-report style. No git/jj commands, no
`agent://all`, no sibling-lane writes. The only child processes started are the builder's
`gio launch` and the probe children it spawns inside seat-built case roots under scratch.

## Risks / notes for the L1 and the counter

- **Declaration internal contradiction (flagged, not widened):** the case-file paragraph
  (claims-declaration-r98.md, the oracle paragraph) still says the oracle waits for "200 ms of no
  change, 8 s cap" while the normative sentence above it and the L1's wave message say 2 s/20 s;
  the classes paragraph also lists `u-anchor` twice (once as `%u` with `#`, once expanded as
  `%u`/`%U` with `file://` `#frag` — 20 unique names either way, and the frozen `classes` array
  carries each once). The builder implements 2 s/20 s; the counter should score against the
  frozen expects, not the stale numbers.
- The counter must substitute `measure_root` into every expect string (`{probe}` ->
  `<root>/probe.sh` first, then `{root}` -> `<root>`), use the same renderer sha
  (`182cf06c...e3d4`) and the same `case.desktop` filename; no dirname sniffing is possible or
  needed. The renderer key order is normative: `Type, Name, Icon, Exec, Path, Terminal, Hidden,
  X-GIO-NoFuse`.
- Comparison plane is rule 7: launches count + sorted vector multiset. d-03's identical vectors
  are correct, not corruption. Every frozen label was produced by two consecutive agreeing
  measurements (predicate iv); a `{"error":"setup-error"}` expect from `case_expect` is an
  instrument failure — the counter should treat it as SETUP_ERROR (its own rc-2 vocabulary),
  never as a scorable label.
- `%i` suffix stripping is load-bearing (i-01/i-04 strip, i-06 absolute path keeps, i-05 empty
  Icon emits `--icon ''`); a tool echoing the raw Icon key will miss them.
- The `%` walk is byte-wise on the raw Exec value; the suite pins the ASCII selector cells
  (pct-06/07, bad-08) but no non-ASCII case can be frozen under the ASCII-only artifact rule —
  the counter's candidate must implement the byte-wise walk from the declaration text.
- The fresh leg's refusal labels (`refusal:desktop-file` for `a\ b` Execs) depend on the escape
  classifier staying in the candidate's model; the frozen `quote-07/08` cases pin the same rule.
  Fresh JSONL records may carry `desktop_raw` (locale/comment flavors) and every desktop block
  carries `X-GIO-NoFuse` (null or "true"); the counter confirmed both legs honour them.
- `%c` locale selection is pinned only under `LC_ALL=C` (c-04/c-05); the declaration's en_US win
  is a scout measurement outside the frozen env — if the counter wants it pinned, it needs an
  env-parameterised oracle run, which is outside this seat's contract.
