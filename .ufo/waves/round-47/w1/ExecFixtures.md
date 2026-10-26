# ExecFixtures — w1 BUILD, round 47 (mado lane)

Deliverables (all under `.ufo/waves/round-47/w1/ExecFixtures/`):

| file | what | size | sha256 |
|---|---|---|---|
| `gen-fixtures.py` | generator + sandbox runner + `--nonce` + `--verify` + `--tripwire` | 86726 B | — |
| `fixtures.json` | 147 curated cases, 28 classes, `expect` produced by the real script | 135726 B | `4cad69ac260b937aebcd0ee43acb6ec86ef89810eb7f9ccb105b4645aa3018bb` |
| `fixtures-nonce.json` | `--nonce 47` → 150 random cases from the same grammar | 121617 B | `790bfb220f86b3ec2e1afcb528fdeb3fc50928b4a4f29550f6676ce662f37cef` |
| `receipts/` | 11 evidence files listed at the end | — | — |

Judge script: `/usr/bin/xdg-terminal-exec`, sha256
`89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac` — recomputed by the
generator on every run and compared to the pin before anything executes.

No `expect` value was typed by hand: every one is the stdout/exit status of the pinned script on
the materialized case, with the case root replaced by `$ROOT`.

## Counts (receipts/summary-curated.json, summary-nonce.json)

Curated: **147 cases / 28 classes / min 3 per class / 0 below 3 / 0 unstable / 0 intent mismatch**.
rc histogram `{0: 134, 1: 13}` → **134 select a terminal, 13 select nothing**.
Nonce(47): **150 cases**, stable, rc `{0: 81, 1: 69}` → 81 select / 69 no-terminal.

| class | n | what it forces |
|---|---|---|
| list-precedence-config-home | 5 | `xdg-terminals.list` in `$XDG_CONFIG_HOME` beats `$XDG_CONFIG_DIRS` |
| list-precedence-data-dir | 4 | `<data>/xdg-terminal-exec/*.list`, plain and desktop-prefixed |
| desktop-prefix-multicomponent | 5 | `Hyprland:GNOME` order, wrong order, mixed case, absent desktop list |
| list-syntax-noise | 6 | comments, blanks, whitespace-only, indented, trailing spaces, malformed id, `/directive` line |
| actions | 6 | valid action, action not in `Actions`, no `Actions` key, invalid action id, unlisted action group, no-retry |
| exclusion-syntax | 7 | `-id`, `+id`, both orders, exclusion vs explicit list, nonexistent id, marker + `:action` |
| duplicate-ids | 3 | same id in data-home vs one/two `$XDG_DATA_DIRS` components |
| subdirectory-ids | 3 | `sub/foo.desktop` → `sub-foo.desktop`, two levels, fallback scan |
| hidden | 3 | `true`, `false`, `TRUE` |
| nodisplay | 3 | `true` alone, `true` with list, `false` |
| type-key | 3 | `Link`, `Application`, absent |
| categories | 5 | missing `TerminalEmulator`, among many, no `Categories`, lowercase, no trailing `;` |
| tryexec | 5 | absent, present, present-not-executable, absolute exists, absolute missing |
| exec-missing | 3 | key absent, `Exec=`, spaces only |
| showin-keys | 5 | `OnlyShowIn` miss/hit, `NotShowIn` hit/miss, show-in ignored for explicit list |
| xdg-unset-vs-empty | 8 | each of the five XDG vars unset and empty |
| no-valid-entry | 4 | empty root, list naming a ghost, all entries invalid, `--print-cmd` on empty root |
| fallback-order | 4 | data-home wins, first data dir wins, first listed id invalid, ghost then fallback |
| terminal-args | 11 | `X-TerminalArgExec`, `-e`/`--`, `X-ExecArg` compat, `/execarg_strict`, `/execarg_default:`, Hold/Dir/Title/AppId, `\s` escape |
| exec-fields | 14 | `%f %U %i %% %z` ×2, quoted binary with space, quoted arg, `$`, tab, trailing spaces, escaped quote, unclosed quote, `;` |
| option-prepend | 6 | `--dir` (2-arg and `=`-concat), `--title`, `--app-id`, `--hold`, all five together |
| command-args | 7 | `--`, args with space/quote/newline, 10 args, positional `-e`, unknown option |
| print-modes | 8 | `--print-cmd` only, `--print-cmd=,`, `--print-delimiter=`, order normalisation, `--print-content`, content+cmd, duplicate id |
| localized-keys | 4 | `Name[de]` before/after `Name`, only localized, brackets in value |
| crlf | 5 | whole file, some lines, list file, `TryExec`, `Hidden` |
| bom | 3 | before group header, in list, before a key |
| long-lines | 3 | 4000-char Exec arg, 10000-char list comment, 2000-char Name |
| odd-paths | 4 | directory named `*.desktop`, dotted id, uppercase extension, dotfile |

All 27 required bullets plus `odd-paths`; the mapping is 1:1 with the table above.

## Method (how isolation was achieved, and why it is needed)

`bwrap 0.13.1` with `--unshare-all --die-with-parent --new-session --proc /proc --dev /dev`,
`/usr` read-only, `/etc`, `/usr/share`, `/usr/local`, `/tmp` masked with empty tmpfs, only the
case root (`--bind`, rw, for the cache) and a **toolbin** bound in. `env -i` then makes the
fixture's `env` the entire environment; `XDG_CACHE_HOME` is forced to `<root>/.cache` and wiped
before every run (cold cache, as the C1 contract requires).

Two host facts made this mandatory rather than cosmetic:

* this host ships **`/usr/bin/alacritty`**, so a `PATH` containing `/usr/bin` would let a host
  terminal satisfy `command -v` for a fixture that means to fail. The toolbin therefore contains
  exactly `bash find awk tr md5sum ls mkdir rm` — nothing else, verified by the tripwire diff below.
* `XDG_DATA_DIRS`/`XDG_CONFIG_DIRS` fall back to `/usr/local/share:/usr/share` and `/etc/xdg`
  when unset, so an unmasked host would decide the `xdg-unset-vs-empty` cases. Those three cases
  additionally name their entry in a config list (config home is consulted first), so they are
  robust even under a leaky sandbox; every other case pins both variables to nonexistent paths.

Reproducibility contract for the counter is in the script docstring: materialize `files` 0644 /
`exec` 0755, substitute `$ROOT` in `env`, `HOME=$ROOT/home`, `PATH=$ROOT/bin:<toolbin>`, fresh
empty cache dir, mask `/etc` `/usr/share` `/usr/local`, `/bin/sh` = bash, compare rc + stdout
after replacing the case root with `$ROOT`. `--verify FILE` implements exactly that path from the
JSON alone (147/147 and 150/150 clean at `--repeat 3`, in a **different** work dir than
generation — which is also the proof that every occurrence of the case root is substituted).

Stub content is not in the frozen schema, and it does not matter: only `command -v` ever looks at
those files. The tripwire shows **no execve of any `$ROOT/bin/*`** in any of the 297 cases.

## Behaviours measured — what the C1 tool must reproduce

These are the parts a re-implementation gets wrong by writing the *spec* instead of the *script*.
Each is backed by at least one fixture; locators are `grep -n` on the pinned script.

1. **`NoDisplay` is not implemented at all.** `grep -c NoDisplay /usr/bin/xdg-terminal-exec` → `0`.
   `j1`, `j2` select a `NoDisplay=true` entry.
2. **`Type` is not implemented.** `grep -c "'Type'"` → `0`. `k1` (`Type=Link`) is selected.
3. **A failed attempt is terminal for that ID.** `read_entry_path` failure is followed by
   `unalias "$xte__entry_id"` (`:1085`), so the fallback scan cannot revisit an entry that was
   already tried. `e2`, `e3`, `e5`, `e6` therefore exit **1 with empty stdout** even though the
   same ID exists as a plain, valid entry. A tool that "falls back to the plain entry" is wrong.
4. **Tokenizer and field-stripper errors do not reject the entry.** `de_strip_fields` returns 1
   *before* writing back (`:729` unknown field, `:708` second `%[fFuU]`) and `de_tokenize_exec`
   returns 1 *after* having appended what it parsed (`:623` unquoted special, `:683` unclosed
   quote); `check_entry_key … && continue` suppresses `set -e`. The half-built argv is used and
   the entry is accepted whenever the first word is on `PATH`. Consequences, all fixtures:
   `%z` survives verbatim (`t5`), `%f %F` keeps **both** (`t13`), `alacritty $HOME` yields
   `alacritty` (`t8`), `alacritty "unclosed` yields `alacritty`+`unclosed` (`t12`),
   `alacritty x;y` yields `alacritty`+`x` (`t14`), `a\"b` collapses to `ab` (`t11`).
5. **CR is `[[:space:]]` for the Exec tokenizer (`:573`) but not for `command -v`.**
   `y1`/`y2` accept a CRLF entry with clean argv; `y4` rejects it when `TryExec` carries the CR;
   `y5` accepts `Hidden=true\r` because only the exact word `true` is rejected (`:938`);
   `y3` shows a CRLF **list** line being dropped by `validate_entry_id` (`:1020`).
6. **`validate_entry_id` requires a lowercase `.desktop` suffix.** `bb3`: a `Foot.Desktop` ID in
   a list is discarded, so the preferred fallback entry wins.
7. **BOM before `[Desktop Entry]` kills the entry** (`z1`, rc 1): the header never matches, so
   `xte__read_exec` stays false and `Exec` is skipped as "wrong section" (`:950`). A BOM only
   before a key costs that one line (`z3`).
8. **Print order is fixed by the script, not by argv**: id → path → content → cmd
   (`:1329`, `:1338`, `:1340`, `:1470`). `u4` (`--print-cmd --print-id`) prints id first;
   `u7` collapses a duplicated `--print-id`.
9. **Delimiters**: `--print-cmd=,` joins args with `,` and emits **no trailing newline** (`u2`
   is `alacritty,--x`); `--print-delimiter=|` likewise (`u3`); the default `\n` adds one.
   `--print-content` ends with the file's own newline, and with `--print-cmd` also present an
   extra delimiter newline appears (`u6`).
10. **Prepend order** is `Exec…, app-id, title, dir, hold, exec-arg, user args` (`v3`, `v6`);
    `X-TerminalArgExec`/`ExecArg` is prepended only when user args exist (`u1` vs `w2`), and a
    `/`-less value (`--dir`) yields two argv words while a `=`-suffixed value concatenates (`s7`,
    `v1`). `-e` in argv always ends option parsing — the branch is `-e | "$XTE__EXECARG"`
    (`:1231`) — so it is *not* a user arg and the exec-arg is not doubled (`w4`), whereas after
    `--` the same `-e` **is** a user arg and does double (`w1`: `alacritty -e -e sh`).
11. **`/execarg_strict` discards any entry without an explicit `TerminalArgExec`** (`s4`, rc 1;
    `s11` moves to the next entry); `/execarg_default:id:--` supplies one in compat mode (`s5`).
12. **`Hidden` accepts anything except the exact string `true`** (`i3`).
13. **Exclusion markers act on the bare ID, action suffix ignored** (`f6`, `f7`), and `+` only
    prevents exclusion, it does not re-include an already excluded ID (`f2`, `f3`).
14. **Empty argv element = non-termination.** The option loop at `:1224` has no `case` branch for
    `""`, so `$#` never decreases: `--print-id ""` was killed by `timeout 3` (rc 124) while the
    control returned 0 — `receipts/empty-arg-spin.txt`. This case cannot be a fixture (`expect`
    cannot express "never returns") and is excluded deliberately; a counter that feeds it will hang.

## Safety evidence (receipts/tripwire.json, tripwire-nonce.json)

All 297 cases were re-run under `strace -f -e trace=execve,socket`:

* successful `execve` targets across the whole set: `/bin/sh`, `/usr/bin/bwrap`, `/usr/bin/env`,
  and the four external commands the script really uses (`awk`, `find`, `mkdir`, `tr`).
  No `$ROOT/bin/*` stub, no terminal binary, no shell beyond the script's own `/bin/sh`.
* `socket(` calls: **2 in every case**, and the bare-wrapper baseline is also 2 with
  `runs: [2,2,2]` stable → **0 socket calls attributable to the script**.
* no rc disagreement while tracing → the trace did not perturb behaviour.
* every case is screened before execution: a mode that exits before `exec "$@"` must be present
  (`Sandbox.args_are_safe` — `--print-*` or `--test`), otherwise the run is refused. That is what
  keeps the terminal launch at the end of the script unreachable.

Cache is out of contract and always cold: `save_cache` is backgrounded (`:1457`) and did not even
complete in print mode (`receipts/host-observation.txt` shows the cache dir still empty), but the
runner wipes `<root>/.cache` before every run regardless.

## Determinism

* curated rebuilt twice into independent work dirs: identical `sha256`
  `4cad69ac…3018bb` (three copies, `receipts/determinism.txt`);
* `--nonce 47` twice: identical `790bfb22…f37cef`; `--nonce 48` differs
  (`49d0763f…9f42c2`), so the nonce stream is seeded per N as specified;
* replay from JSON alone at `--repeat 3`: 147/147 and 150/150, 0 mismatches.

## Cross-check against the counter's pinned set (read-only, outside my scope)

`quality/counters/c1-r47-fixtures.json` (183 cases, sha256
`4b5a252f09975ed5e9e5a5a24e4fe749ac777770447c22f7c21bbb2c21da2168`) already exists and is the
file `quality/counters/c1-r47-terminal.py` pins (`FIXTURES_SHA256`, `MIN_FIXTURES = 100`, same
sha256 as on disk). It contains **all 147 of my cases byte-identical in every field** plus 36
`l1-`-named cases. I did not write that file; I verified it:

* `gen-fixtures.py --verify quality/counters/c1-r47-fixtures.json --repeat 2` → **183 verified,
  0 mismatches, 0 refused, 0 failures** (`receipts/verify-counter-set.json`), i.e. every record in
  the merged file still describes this host's resolver.
* one `l1-` case (`l1-test-mode`) drives the script with `--test`, which prints the argv and exits
  0 at `:1460`, also before `exec`. My pre-execution guard originally refused it as "no print
  mode"; it now accepts exactly two non-execing modes, `--print-*` and `--test`, and a refusal is
  reported per case instead of aborting the run. My own fixtures use only `--print-*`.

## Risks / limits (read before freezing predicates)

1. **`readdir` order.** Fallback order comes from `find -L` output. I avoided depending on it by
   construction: never two *valid* candidates inside one applications directory — the second
   candidate always sits in a lower-priority `$XDG_DATA_DIRS` component, or the selection is
   decided by an explicit list. `f1`–`f7`, `g1`–`g3`, `r1`, `r2`, `bb3`, `p8` and every nonce case
   are built that way. Repeats agreeing is weak evidence; the construction argument is the real one.
2. **`duplicate-ids` semantics are "last found wins"**, which in practice means *first in
   preference order* wins (`g1` data-home, `g2` first `XDG_DATA_DIRS` component, `g3` data-home).
   The script's own comment (`:780`) says "use last found if duplicate"; the observable outcome
   is preference order. Freeze whichever phrasing the counter can actually implement.
3. **Sandbox masking is part of the contract.** Without masking `/etc` and `/usr/share`, the three
   `xdg-unset-vs-empty` default cases could change on another host — they name their entry in a
   config list to stay robust, but a replay that also unmounts the cache isolation will drift.
4. **`/bin/sh` must be bash.** This host has no dash; `read`, `alias`, `${x%%pattern}` and `set -eu`
   behaviour are all bash-observable. Documented in the docstring, not encoded in the JSON.
5. **`expect` cannot carry stderr.** 13 cases exit 1 with empty stdout and diagnostic text on
   stderr; a tool that prints to stderr is still byte-identical under this contract. If the C1
   counter wants stderr fidelity, the schema needs a third field — freeze decision for the L1.
6. **Nonce is a grammar, not a fuzzer.** It recombines the curated dimensions (desktop string,
   list kind, per-entry validity, print set, command args); it will not invent an Exec line with
   a construct the curated set never uses. That is deliberate — 69/150 nonce cases end in
   no-terminal, which is a real distribution, but it is *my* distribution.

## Host observation (corroborates C2, does not claim it)

`receipts/host-observation.txt`: with `XDG_CACHE_HOME` pointed at scratch, print modes only,
`--print-id --print-path --print-cmd` printed `Alacritty.desktop`, the user-override path under
`~/.local/share/applications/`, and `alacritty`, rc 0; cache dir left empty. This reproduces the
L1 host fact from the wave spec, and is why the user-override directory is the preferred slot in
the `duplicate-ids` class.

## Blockers

None. Nothing outside the seat directory was written; no tracked file was edited; no pacman, no
compositor verb, no GUI/terminal launch, no socket. Scratch `/fast/scratch/hyaku/mado-r47/ExecFixtures`
was removed after the receipts were copied here.

## Receipts

`receipts/summary-curated.json` · `summary-nonce.json` · `tripwire.json` · `tripwire-nonce.json` ·
`verify-curated.json` · `verify-nonce.json` · `verify-counter-set.json` · `schema-check.txt` ·
`determinism.txt` · `empty-arg-spin.txt` · `host-observation.txt`
