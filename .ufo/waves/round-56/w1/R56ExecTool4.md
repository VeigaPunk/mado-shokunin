# R56ExecTool4 — w1 report: `mado-watchplan.py` (C2)

## Done
Wrote `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w1/R56ExecTool4/mado-watchplan.py` (522 lines, stdlib only, sha256 `95805b9b42676428be31b913c6f392a5cba770e758ec69b73ad79d900bbab62b`), strictly from registration §C2. I read only registration.md, claims-frozen.md, the 18 fixtures, `tools/mado-devices.py` (conventions: parse_args, Setup exception, selftest, run/main) and the host config via the tool. No other seat's tool was read. No hold-out path or file was seen.

Deliverables (same directory): `mado-watchplan.py`, `live.txt`, `fixtures-result.txt`, `selftest.txt`, `fixture-runner.py` (the driver I used; its `cwd=` points at my scratch dir, now removed, so edit it to rerun).

## Checks run
- 18 fixtures: every `args.json` with `{FX}` replaced by the absolute fixture dir, `python3 -I <tool>`; stdout bytes and exit status compared with `expected.out`/`expected.rc`. All 18 PASS: F01..F18 (rc 0 except F12/F17/F18 rc 2), final line `18 /18`. Fixtures run from the working tree (git symlinks F05/F06/F10 are intact there); I did not run through `git archive`. No fixture edited; I believe none is wrong.
- `python3 -I mado-watchplan.py --selftest` → `MADO_WATCH_SELFTEST: 82/82 assertions passed`, exit 0 (private `tempfile.mkdtemp` tree, removed; `/tmp` holds no leftovers). The selftest line is `MADO_WATCH_SELFTEST: <n>/<n> assertions passed`; the spec gives only `<n>/<n> assertions passed`, so the prefix is my choice.
- Live, read-only: `hyprctl getoption misc:disable_autoreload -j` gave `{"option": "misc:disable_autoreload", "int": 0, "set": false }` (saved in scratch, now removed). Then `python3 -I <tool> --config $HOME/.config/hypr/hyprland.conf --home $HOME --getoption <that file>` → rc 0, saved as `live.txt`. Decisive lines: header `autoreload=on disable_autoreload=unset paths=40 unsupported=0 errors=0`; 40 primary watches, no canonical watch (no symlinks in the tree), `MADO_WATCH_LIVE: ... config=0 live=0 verdict=AGREE`, `DONE watches=40 unsupported=0 errors=0 live=AGREE`. The glob `~/.local/state/omarchy/toggles/hypr/*.conf` yields flags.conf and window-no-gaps.conf (n=37, 38). No file under `~/.config` or `~/.local` was written.
- Not run: no `git archive` export of the fixtures, no hold-out, no `check-r56-controls.py`, no ctl stubs (not assigned).
- Tools installed: none.

## Defensive behaviour (contract-implied answers)
| case | behaviour | basis |
|---|---|---|
| non-UTF-8 bytes in config or getoption | decoded with `errors="replace"` (U+FFFD), output encoded UTF-8; glob results use surrogateescape both ways | Model: "decode as UTF-8 with errors replaced" |
| last line without `\n` | parsed like any line (split on `\n`; a trailing `\n` gives an empty last element, skipped) | Model |
| `}` with an empty stack | no-op, nothing counted | "exactly `}` pops the stack" |
| glob error (bad pattern, OSError, ValueError, RecursionError) | treated as no match → `ERROR reason=nomatch`. `[x`, `a[`, `*[` are plain python-glob no-matches | Source handling step 4 |
| symlink loop as source target (`l1 -> l2 -> l1`) | glob matches it (`lexists`), `os.stat` fails ELOOP → `ERROR reason=inaccessible`, rest of line skipped | step 5 |
| symlink loop as list entry | `isdir` false, `lexists` true → `type=file`; `realpath(strict=True)` fails → no canonical watch | Watch list |
| file sourcing itself | depth cap 16: entries main + depth 1..17 = 18, `unsupported=1` (selftest asserts `paths=18 unsupported=1`) | step 5 |
| unreadable but regular sourced/config file | listed, not parsed | Arguments |
| huge decimal value | kept as normalised decimal string (no int conversion, avoids python's 4300-digit limit) | VALUE rule |
| strict JSON | `NaN`/`Infinity` constants are rejected as `bad_json` | "a JSON object" |

## Ambiguities (both readings; the tool follows the first)
1. **Setup precedence when several apply.** Not specified. Taken: usage > unreadable > too_large > bad_json (the order the text lists them); the getoption file is checked before the config tree. Alternative: first failure in processing order. Differs only when a fixture has e.g. a too_large sourced file and a bad_json getoption.
2. **`}` underflow.** No-op (taken) vs `unsupported` +1.
3. **Exponential self-sourcing** (a file with k source lines that sources itself yields k^16 entries). The contract says nothing. **Added deviation:** more than 262144 list entries → `MADO_WATCH: SETUP too_large`, exit 2 (constant `MAX_ENTRIES`). The alternative is to run unbounded. Not in registration's divergence list; the L1 may veto it. No fixture is near it.
4. **`$`/`{`/backslash test is on the whole stripped line**, trailing comment included (taken): `misc:disable_autoreload = 1 # {x}` is `unsupported`. Alternative: the part before the comment.
5. **`len(RAW) < 2` counts characters, not bytes** (Hyprland counts bytes): a single non-ASCII character is not `bogus` here.
6. **`--display-root` with both the given text and its realpath matching**: the given text wins; the order is "given, then realpath". Trailing `/` removal removes exactly one slash (`/` becomes the empty prefix, so everything absolute prints `$ROOT...`).
7. **`--getoption` JSON line-splitting**: lines split on `\n` only and stripped of the model's whitespace set; a pretty-printed multi-line object is `bad_json`.
8. **`~user` and `~` forms**: `~x` with `--home` expands to `home + "x"` (literal `RAW[1:]`), no slash inserted; `--home` with a trailing `/` gives `home//a.conf`, which is kept (selftest asserts it).
9. **`config=<0|1>` in the live line**: the tool treats a non-zero accepted value as 1 (non-zero test on the normalised decimal string, so `007` is non-zero).
10. **`--config` as FIFO/device**: `os.stat` is not regular, so it is listed (`type=file` via `lexists`) and never opened; no hang possible.
11. Header text for the `--selftest` line prefix (above).

## Defects found
None in fixtures or registration. One observation: registration says the harness exports with `git archive` + `tar -x`; F14 has no `tree/` directory in the working tree (an empty tree cannot be committed), and the tool's expected output there depends on the path simply not existing. This matches how the harness works and gives `type=missing`, so it is not a defect.

## Could not verify
- Behaviour of the sealed hold-out (not seen).
- Python version dependency: tested on 3.14.8 only. `os.path.realpath(strict=True)` needs 3.10+; `glob` leading-dot semantics are the stdlib's.
