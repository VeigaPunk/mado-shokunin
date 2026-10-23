# Residual — C2 RE-MEASURE (res seat `MadoR26.ResC2Remeasure`, independent re-derivation)

Seat: read-only on lane; scratch `/fast/scratch/hyaku/mado-r26/res/c2remeasure/`. No installs (python3/tooling sufficient).

## Identity (re-derived, not trusted from the receipt)

- `git show a496b02a:tools/mado-binds.py | sha256sum` = `01751e133eddb927d60190e233d341c7bc1b774b5ca05a1ed5bab741e2b8179b` = **01751e13…179b ✓**
- `git show a496b02a:.ufo/waves/round-26/c2/count.py | sha256sum` = `b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8` = **b92c32da…16a8 ✓** (equals registration pin)
- `oracle.py` at a496b02a = `680798ed…62e441` = pin; `count-v3.py` working tree = `8532d3e9…8375` = pin. Working-tree copies of counter/oracle/v3/tool all equal the pinned/committed bytes (`sha256sum` on files).
- Measured rev resolves to `a496b02abe544b42b9a2e0c044ba8611e43c1b4e`, same rev the original receipt used.

## Two fresh-seed counter runs (this seat)

Command exactly as ruled: `cd lane && env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 python3 -I .ufo/waves/round-26/c2/count.py a496b02a --jobs 4`. `--seed` omitted → counter draws fresh `os.urandom(8)` seeds itself.

| run | seed | cases_pass | embed_hits | coredump delta | verdict |
|---|---|---|---|---|---|
| original `evidence/c2-after-a496b02a.txt` | `629fd25ee94fb42a` | 51/51 | 0 | 0 | TARGET_MET |
| residual run 1 | `7b3ef210e27220b1` | 51/51 | 0 | 0 (1338→1338) | TARGET_MET |
| residual run 2 | `bb46e953b20eb836` | 51/51 | 0 | 0 (1338→1338) | TARGET_MET |

Different seeds → different generated cases (case names/compositions differ across all three receipts); snapshot digest stable `fe1b2d8b…727`, BASE=192 binds, `ORACLE_CHECK base_twice equal` both runs. Full transcripts: `receipt-run1.txt`, `receipt-run2.txt` in scratch.

## Tool audit (a496b02a bytes, stricter than the counter's embed check)

The counter's embed check covers only `arg`/`description` strings ≥12 chars (EMBED_MIN=12). I re-derived the oracle's BASE table myself by running `harness/oracle.py` directly (snapshot of `$HOME`, nested headless Hyprland; coredumps 1338→1338, delta 0) and checked **every string field of all 192 rows at any length** for substring presence in the tool bytes.

- Under the counter's exact rule: 0 hits over 248 distinct `arg`/`description` strings ≥12 chars — reproduces `embed_hits=0`.
- All-fields/any-length scan: 70 substring hits, all generic grammar vocabulary, not snapshot data. Longest are **dispatcher names** (`movecurrentworkspacetomonitor`, `togglespecialworkspace`, `movetoworkspacesilent`, …) which live in the admitted round-25 `DISPATCHERS` frozenset (KeybindManager vocabulary; the table carries the comment "no run of its bytes may spell a live bind-table value"). Remaining hits are single-char keys/args (`X`, `W`, `prev`, `10`, `-1`, `mouse`) — substring collisions and flag tokens, not embedded rows.
- **No snapshot-specific `arg` or `description` text appears anywhere in the tool** — the only `description` hit is the one-character `X`. No embedded base table, at any granularity the check could miss.
- Case keying: none. Whole-file scans find no path-name sniffing, mtimes/stat, `/proc`/`/sys`/mountinfo reads, hostname/platform/pid/cwd reads, `random`, `seed`, `tempfile`, `subprocess`, `eval`/`exec`. The only file I/O is `open(path, "rb")` on config paths under `--home`; CLI is `--home` only.
- Environment reads: **none remain** — `os.environ` is fully removed from the tool (see diff finding below).

## Diff `96101be5` → `a496b02a`: behaviour outside `{{…}}`

Complete hunk inventory: docstring rewrite; ~440-line insert (binary32 `{{…}}` machinery: `frac_to_f32`, `fmt_f32`, `stof`/`_scan_float`, `arith`, `parse_expression`, `expand_expressions`); `expand_expressions` call inside the variable-expansion loop; plus these **non-`{{…}}` deltas**:

1. **Environment seeding removed** (`State.env = dict(os.environ)` deleted; `get_var` no longer falls back to the environment). Observable: a tree where a bind/`bindd`/`unbind` line references a `$NAME` defined only in the environment now keeps it literal, where round-25 expanded it as hyprlang does. Already captured as **M26-10** in `corpus/lessons/round-26.md` (trade-off: also closes the out-of-`--home` read channel from round-25 defect 6; counter-blind because the 20-case V3 sample contains no env-var tree — BASE passing proves only that the snapshot's 192 binds don't use one).
2. **Variable-expansion cap now drops the line**: `for _ in range(100)` gains `if iteration == 99: return` ("Expanding variables exceeded max iteration limit" path). Old code fell through and handled the partially-expanded line; new drops it, matching hyprlang `getNextLine`'s error branch. Observable only on lines still expanding after 100 passes (pathological variable chains); no case generates such depth, so counter-blind — but aligned with the pinned source.
3. **`unescape_braces` → `strip_escapes` rewrite** (mutation-based, "loop stops one char early", `i -= 1`/`i += 1` bookkeeping). I fuzz-equivalenced the two implementations: 400,000 random strings over `\\ { } a b space tab` plus 16 boundary cases — **zero divergence**; it is a no-op rewrite of the same hyprlang rule.

Also worth restating (registration's own caveat): the V3 20-case half is a sampled no-harm check, not exhaustive (w1 `CritC2Design`). The env-var and max-iteration deltas sit exactly in its blind spots.

## Verdict

**`C2 RE-MEASURE agree`** — the recorded TARGET_MET re-derives twice on fresh seeds (51/51, embed_hits=0, exit=0, coredump delta 0) at the byte-identical tool and pinned counter/oracle. Stricter-than-counter embed audit and keying/environment scans find no cheat channel. Disclosure: round-25 behaviour outside `{{…}}` did change (env-var fallback removed — already M26-10; >100-pass lines now dropped — aligned with hyprlang; escape pass rewritten but proven behaviour-identical by fuzz); none of it is visible to the C2 counter and none reverses the measured verdict.
