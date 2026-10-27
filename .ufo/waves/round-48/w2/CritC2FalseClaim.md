# W2 / CritC2FalseClaim — falsification of the round-48 C2 XKB empirical classifications

Wave w2 (FALSIFY), policy v1, base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`, lane `mado-shokunin`.
Scope: the **empirical** half of C2 — the host observations in
`l1-draft/xkb-keymap-compile-r48.md` (its "The five name classes" table, the multi-layout paragraph, steps 1-7
and 9) against the committed capture `receipts/xkbcli-compile-keymap-r48.txt` and the frozen replay clauses of
`quality/counters/c2-r48-xkb-entry.py` (f, r). Nothing was scored; no lane file was written outside this report
and `w2/CritC2FalseClaim/`.

Host under test (read from the package database, no pacman run): `libxkbcommon-1.13.2-1`,
`xkeyboard-config-2.48-1`, `xkbcli --version` → `1.13.2`; `/usr/share/X11/xkb -> /usr/share/xkeyboard-config-2`.
Method: read-only `xkbcli compile-keymap` (`compile`/`test`/`kccgst` verbs only), 66 scripted invocations across
four probe scripts plus 5 ad-hoc real-host replays, each in an isolated `HOME`/`XDG_CONFIG_HOME` under
`/fast/scratch/hyaku/mado-r48/CritC2FalseClaim` except the explicit real-host replays (R1-R3, V1, U5) which set
`HOME=/home/vgpnk`.

## Verdict

**The empirical classification set is not falsified.** Every compiled behaviour the entry states reproduced
exactly — same stdout, same stderr lines, same exit status — including the positive keymap byte-for-byte
(`efd487a399201523540f4e5bbf81818be3183f6d9957c2f2b12469a2cf6fce81`, 2090 lines / 73079 bytes, stderr empty) in
both the clause-r environment and the real host environment. The two clauses that bind the receipt (f windows,
r replay) admit the draft entry + committed receipt; a mechanical replay of clause f's own window logic over
those two files returns every required window in the affirmative (`w2/CritC2FalseClaim/clausef.txt`).

Four defects were found that a reader should treat as **pre-data prose/custody repairs, not predicate breaks**:

| id | kind | severity | what fails |
|---|---|---|---|
| F1 | prose refuted literally | P2 | `--model nope` "silent at every level" — false at `XKB_LOG_LEVEL=debug` |
| F2 | prose incomplete | P2 | "only a WARNING about the missing second variant" — a second WARNING line is emitted |
| F3 | count/alias imprecision | P3 | "installs four rulesets" — `xorg` is a symlink to `base`; three distinct rulesets |
| F4 | evidence custody | P2 | include-path precedence is labelled "observed" but the receipt holds only a recipe |

None of F1-F4 changes a compiled classification, and no clause (c/d/e/f/g/h/i/r) reads the affected cells, so the
frozen predicate is untouched by them. They are listed so L1 can repair the prose (or, for F4, choose between a
fuller receipt with a re-registered S350 pin and a downgraded state cell) **before** the data commit.

## F1 — `--model nope` is not "silent at every level"

Entry: `| --model nope | silent at every level; geometry pc(pc104) instead of pc(pc105) | rc 0 |`.
Step 7's narrower sentence ("prints nothing even at `XKB_LOG_LEVEL=warn`") is true; the table cell is not.

```
$ env -u XDG_CONFIG_HOME HOME=/home/vgpnk XKB_LOG_LEVEL=debug /usr/bin/xkbcli compile-keymap --test --layout br --model nope 2>&1 \
    | grep -E "RMLVO|model|WARNING|ERROR"
xkbcommon: DEBUG: Compiling from RMLVO: rules 'evdev', model 'nope', layout 'br', variant '(null)', options '(null)'
```

At DEBUG the RMLVO trace names `model 'nope'`, and the run also prints the include-path INFO/DEBUG lines. The
committed receipt itself contains this line class in its `--verbose` section for `model 'pc105'`, so "silent at
every level" cannot be literally true of the same binary. Substantively the classification holds: **no WARNING and
no ERROR is emitted about the model**, rc 0, geometry `pc(pc104)` instead of `pc(pc105)` (reproduced at default,
warn and debug levels). Suggested repair: "no diagnostic at any level; at DEBUG the RMLVO trace names the model;
geometry `pc(pc104)`".

## F2 — the `br,us`/`nodeadkeys` run emits two WARNING lines, not one

Entry: "`--layout br,us --variant nodeadkeys` gives symbols `pc+br(nodeadkeys)+us:2+inet(evdev)` and **only a
WARNING about the missing second variant** (visible at `XKB_LOG_LEVEL=warn`)".

```
$ env XKB_LOG_LEVEL=warn /usr/bin/xkbcli compile-keymap --test --layout br,us --variant nodeadkeys
xkbcommon: WARNING: More layouts than variants: "br,us" vs. "nodeadkeys".
xkbcommon: WARNING: Multiple definitions of group 0 name in map 'nodeadkeys'; Using 'Portuguese (Brazil, no dead keys)', ignoring 'Portuguese (Brazil)'
rc=0
```

The symbols value, rc and the missing-variant warning all match; the second WARNING (duplicate group-0 name from
merging `br` with `br(nodeadkeys)`) is unlisted, so "only" is wrong as an enumeration. No WARNING/ERROR appears at
the default ERROR level, and the same second warning appears for the `nodeadkeys,intl` case in addition to the
ERROR line. Suggested repair: name both lines, or say "only WARNING-level lines (a missing second variant and a
duplicate group-0 name)".

## F3 — `xorg` is a symlink to `base`, not a fourth ruleset

Entry step 3: "The package installs four rulesets - `base`, `evdev`, `xorg`, `xfree98` (receipt `ls`)"; the
receipt's plain `ls` (no `-l`) cannot show the alias, and the census line says `rules_files=4`.

```
$ stat -c '%F %n' /usr/share/xkeyboard-config-2/rules/xorg /usr/share/xkeyboard-config-2/rules/base
symbolic link /usr/share/xkeyboard-config-2/rules/xorg
regular file /usr/share/xkeyboard-config-2/rules/base
$ ls -l /usr/share/xkeyboard-config-2/rules/    # xorg -> base, xorg.lst -> base.lst, xorg.xml -> base.xml
$ ... --kccgst --rules base --layout br > base.k ; ... --rules xorg ... > xorg.k ; cmp base.k xorg.k
identical=yes
```

So the directory holds three distinct ruleset files (`base`, `evdev`, `xfree98`) plus the `xorg` alias and its
`.lst`/`.xml` aliases. Behaviour is unaffected (`xorg` compiles and equals `base` byte-for-byte), and every
other row of the name table is correct. Suggested repair: "three ruleset files plus an `xorg` symlink alias to
`base`"; leave the census wording as directory entries if preferred.

## F4 — the include-path precedence observation is not in the receipt

Entry answer table: "where a name is searched for, and which path wins | step 6 | **sourced, precedence
observed**". The receipt's section is titled `== include-path precedence (ephemeral probes; recreate with the
recipe below)` and carries only a `#`-comment recipe with expected rc values — no captured stdout/stderr/rc for
any of the three legs. The `$HOME/.config/xkb` fallback named in step 6 is not in the recipe at all. The
classifications themselves are true; I reproduced every leg (and the fallback) independently:

| leg | command shape | observed |
|---|---|---|
| `$XDG_CONFIG_HOME/xkb` | file at `$XDG/xkb/symbols/mado48`, `--layout mado48` | rc 0, resolves (`MADO48-XDG`) |
| `$HOME/.config/xkb` fallback (XDG unset) | file at `$HOME/.config/xkb/symbols/mado48` | rc 0, resolves (`MADO48-HOMECONFIG`) |
| fallback must not apply when XDG is set | XDG→nonexistent, `$HOME/.config/xkb` present | rc 1, XKB-338 `symbols/mado48` |
| `$HOME/.xkb` | file at `$HOME/.xkb/symbols/mado48` | rc 0, resolves |
| precedence XDG before `$HOME/.xkb` | both present | XDG wins |
| `$XKB_CONFIG_EXTRA_PATH` | `extra/symbols/mado48`, XDG `.xkb` empty | rc 0, resolves (`MADO48-EXTRA`) |
| `$HOME/.xkb` before extra path | both present | `.xkb` wins |
| versioned before unversioned extension dirs | `<extv>/subv`, `<extu>/subu` | versioned wins; order extv, extu, root |
| root override + legacy fallback | `XKB_CONFIG_ROOT=/nonexistent-root` | rc 0, `WARNING: Root include path failed; fallback to "/usr/share/X11/xkb"` (hidden at default level) |
| root empty disables fallback | `XKB_CONFIG_ROOT=` | rc 1, XKB-338 `rules/evdev`, no fallback |
| `HOME=/nonexistent-home`, XDG unset | recipe leg 3 | rc 1, XKB-338 |

Two pre-data options: (a) capture the three legs into the receipt — this changes the receipt's sha256 and the
S350 pin digest, so per `registration.md` it is only legal as a new registration version followed by the complete
control set; (b) downgrade the state cell to "sourced; precedence replayed independently
(`w2/CritC2FalseClaim`), recipe in receipt". Either keeps the claim's truth; only the evidence attribution moves.

## F5 — observation, zero predicate impact

Receipt header `taken: 2026-10-27T00:08:08Z` (UTC) against `verified-at: 2026-10-26` in the entry and the rows'
`opened 2026-10-26`. The file's mtime is 2026-10-26 21:08 local; no clause compares the two. Listed only so a
future reader does not read the UTC date as a round mismatch.

## Reproduced — the full classification set, not falsified

Every row below is a live probe from this seat; `probe*.txt` is the transcript (stdout+stderr+rc).

**Name classes** (`probe.txt`, `probe2.txt`)

| classification | observed | entry |
|---|---|---|
| `--rules base`, `--rules xorg` | rc 0, keycodes `xfree86+aliases(qwerty)`, symbols `pc+br+inet(pc105)`, geometry `pc(pc105)` | matches |
| `--rules xfree98` | rc 1, `[XKB-595] No components returned from XKB rules "xfree98"`, `[XKB-822]` | matches |
| `--rules nope` | rc 1, XKB-338 `rules/nope` + census, `[XKB-595] Cannot load XKB rules "nope"`, `[XKB-822]` | matches |
| `--model nope` | rc 0, geometry `pc(pc104)`, no diagnostic (see F1) | matches but for "every level" |
| `--layout br` | rc 0 | matches |
| `--layout zz` | rc 1, XKB-338 `symbols/zz`, XKB-661 `zz`, XKB-769 `Abandoning symbols file "(unnamed map)"`, XKB-822 | matches |
| `--variant nodeadkeys` | rc 0 | matches |
| `--variant nope` / `--variant caps` | rc 1, XKB-661 `br(nope)` / `br(caps)`, XKB-769, XKB-822 | matches |
| `--options compose:caps` | rc 0, symbols `pc+br+inet(evdev)+compose(caps)` | matches |
| `--options nope:nope` | rc 0, `[XKB-595] Unrecognized RMLVO option "nope:nope" was ignored` at the default level | matches |
| mixed `compose:caps,nope:nope` (both orders) | rc 0, known option kept, unknown dropped with XKB-595 | consistent (unlisted) |

**Defaults and empty names** — no names → `evdev`/`pc105`/`us`/`pc(pc105)`; `--layout '' --variant intl` → rc 0,
symbols `pc+us+inet(evdev)`, stderr empty at default, the `Layout not provided...` WARNING only at warn;
`--rules ''` → evdev; empty model/variant replaced; `--options ''` **respected as empty** even with
`XKB_DEFAULT_OPTIONS=nope:nope --enable-environment-names` (no XKB-595), while omitting `--options` uses the
default (XKB-595) — this empirically confirms step 1's `rmlvo->options == NULL` quote.

**Multi-layout pairing** — `br,us`+`nodeadkeys` → `pc+br(nodeadkeys)+us:2+inet(evdev)` (warning; see F2);
`br`+`nodeadkeys,intl` → `pc+br(nodeadkeys)` + ERROR `Less layouts than variants`, rc 0; `br,us`+`,dvorak` →
`pc+br+us(dvorak):2+inet(evdev)` (compile rc 0 under `--test`, so `us(dvorak)` is a real map); `br,us`+`,nope` →
`--test` rc 1 XKB-661 `us(nope)`; `br,us` no variant → `pc+br+us:2`; `br,us,de` → `us:2, de:3`;
`br,us,de`+`nodeadkeys,dvorak` → `br(nodeadkeys)+us(dvorak):2+de:3`, rc 0, silent at default; `br,us`+3 variants →
ERROR, truncated to 2, rc 0; `br,zz` (unknown layout second) → rc 1 XKB-338 `symbols/zz`.

**Include paths, rules shadowing, `.pre`/`.post`** — order reproduced as `$XDG/xkb` (or `$HOME/.config/xkb`),
`$HOME/.xkb`, extra path, versioned ext subdirs, unversioned ext subdirs, root, legacy fallback
(`probe3.txt` K1-K6, G2-G4; `probe4.txt` T7-T8). First hit wins for symbols and for rules: a user
`$XDG/xkb/rules/evdev` copy with an extra `! option` section yields `+mado48` in the KcCGST, proving the user
copy shadows the root's. `<name>.pre` and `<name>.post` are read, and from **every** include path in path order:
two posts (XDG + extra) both contributed (`+compose(caps)+compose(rwin)`), and a duplicate option name appended
both values in path order.

**Pins and host facts** — all 20 `**OBS**` locators were spot-read at their cited lines and every quoted span
is verbatim (rules.c:530/1259/1297/2063, xkbcomp.c:157/161, include.c:355/501, context.c:317/336/503,
context-priv.c:208, meson_options.txt:46, rules/evdev:175 & :570, symbols/br:47, compile-keymap.c:521/587,
messages-codes.h:116/150). `symbols/br` has exactly 11 `xkb_symbols` maps and neither `nope` nor `caps`;
`rules/evdev:55-59/:61-64/:109-175/:529-586` contain the wildcard/option sections as cited; the two host input
files still hash `3769c92a…` and `bee5aa68…`; `~/.config/xkb`, `~/.xkb`, `/etc/xkb` and both extension dirs are
absent on the host; the entry's positive compile claim reproduces in the real host environment.

## Predicate contact (frozen instrument)

- **clause f** (receipt as capture): replaying its window logic mechanically over the draft entry + the
  committed receipt — `layout`/`variant`/`option`/`positive` windows each resolve to exactly one labelled rc
  (1/1/0/0), `positive+br` windows = 7 with the single digest `efd487a3…`, and the entry states version,
  positive rc 0, digest prefix and all three negative rcs on unfenced lines (`clausef.txt`: every line `True`).
  No rc can drift to a neighbouring case in this receipt.
- **clause r** (replay): `--layout br --options compose:caps` → rc 0, sha256 `efd487a3…` (byte-equal, twice);
  `--test --layout zz` / `--test --layout br --variant nope` / `--test --layout br --options nope:nope` → rc
  `(1, 1, 0)`, stderr carries `Couldn't find file`, `process include statement`, `XKB-595`. The receipt's
  `^<64hex>\s+host.keymap$` line is present.
- The F1/F2 cells are read by no clause (they carry no quote locator and are not one of clause f's four probe
  values), so repairing them does not disturb a frozen clause.

## Coverage gaps found (not misses — unlisted behaviours worth a row)

- **G1 zero-byte file.** A 0-byte `rules/<name>` or `symbols/<name>` on an include path yields
  `Couldn't read XKB file …: Invalid argument` / `Couldn't read rules file …: Invalid argument` (EINVAL), then
  XKB-661/XKB-595, rc 1 — a distinct failure class from the "missing file" (XKB-338) and "no map" (XKB-661)
  classes the entry tabulates (`probe3.txt` K7/K8).
- **G2 fifth layout.** `--layout br,us,de,fr,gb` → rc 0, four groups compiled, the fifth dropped with
  `[XKB-595] Unrecognized RMLVO layout "gb" was ignored` (XKB_MAX_GROUPS=4 boundary). The entry's layout class
  covers a missing symbols file, not a known layout beyond the group limit.
- **G3 empty layout slot.** `--layout br,,us --variant nodeadkeys` → rc 0, silent, symbols
  `pc+br(nodeadkeys)+us:3` — the empty slot consumes group 2 and shifts the later layout's index.
- **G4 mixed option list.** One unknown option in a comma list is dropped with XKB-595 and the rest compiles.
- **G5 debug includes unrelated noise.** At DEBUG any compile prints include-path INFO/DEBUG lines regardless of
  the model/option question, so "silent" can never be a whole-run property (the source of F1).

## Not attacked here

Held ground S318/S319 and the compositor half (no Hyprland reload, no keymap dump); per-layout variant
enumeration beyond `br`/`us`; compat/types option families (`grp:*`, `caps:*`, `lv3:*`); the README index row,
registry cell counts and numbered-step citation binding (other w2 seats); all C1 material.

## Bounds and hygiene

- Scratch `/fast/scratch/hyaku/mado-r48/CritC2FalseClaim`: 549,651 bytes total, largest file 73,079 B (the
  positive keymap), `ulimit -f 2048` (512-byte units) in every writer shell, no `/tmp`, removed after the
  evidence was copied.
- Read-only host: `compile-keymap` `compile`/`test`/`kccgst` verbs, `--version`, `stat`/`readlink`/`ls -l`,
  `sha256sum` of the two named input files and package-db directory names. No pacman, no package install, no
  input injection, no compositor/service mutation, no GUI/terminal launch, no `xdg-terminal-exec`. No device
  names, window titles, serials or process tables printed. No git/jj command at all; no lane file written
  outside `w2/CritC2FalseClaim.md` and `w2/CritC2FalseClaim/`.

## Evidence

`w2/CritC2FalseClaim/`: `probe.txt` (classes, defaults, multi-layout, include paths A-H) + `probe.sh`;
`probe2.txt` (untested multi-layout, empty names, legacy root, `XKB_DEFAULT_*`) + `probe2.sh`;
`probe3.txt` (path order K1-K6, rules shadow/pre/post, real-host R1-R3) + `probe3.sh`;
`probe4.txt` (T1-T10) + `probe4.sh`; `clausef.txt` (clause-f window replay over draft entry + receipt) +
`clausef.py`; `commands.txt` (index).
