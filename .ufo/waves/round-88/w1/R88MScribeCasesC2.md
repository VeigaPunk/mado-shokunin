# R88MScribeCasesC2 — C2 containment case authoring (mado round 88, w1)

Seat: R88MScribeCasesC2 (scribe, leaf). Lane: /home/vgpnk/Projects/shokunin/mado-shokunin.
Base revision: 24ba2a9ddac21c1211579231e6ee1d98963f9988. No scoring was run; the L1 freezes and scores.

## Artifact

- Path: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-88/controls/containment-cases-r88.json`
- `sha256 3ee0dc9be8b313b788e17bceccd9366b84b74c76adaccf33bf5446e253d766f2` (8528 bytes)
- Schema: `mako-containment-r88-v1`; `notes` records the authoring stance and independence.

## Gates (item acceptance)

| Gate | Result | Evidence |
|---|---|---|
| JSON parses | PASS | `python3` `json.loads` in the validation cell, exit 0 |
| 14 ≤ K ≤ 20 | PASS | K = 17 |
| ≥ 6 escapes | PASS | 9 (`refusals: "present"`) |
| ≥ 6 positives | PASS | 8 (`refusals: "none"`) |
| every case has a pin | PASS | 17/17 non-empty |
| files/config/home/read_roots/symlink targets carry no `..` or leading `/` | PASS | structural check, `violations= none` |
| expected width reachable from authored text | PASS | each expected width literal appears as a `width=` line in that case's files |
| `sha256sum` | PASS | `3ee0dc9be8b313b788e17bceccd9366b84b74c76adaccf33bf5446e253d766f2` |

Commands run (all from the lane root unless noted), with exit codes:

1. `python3 - <<'PY' … json/structural validation … PY` — exit 0; printed `K= 17 escapes= 9 positives= 8`, `violations= none`, sha256.
2. `sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-88/controls/containment-cases-r88.json` — exit 0; digests equal (validation-cell and sha256sum agree).
3. `zcat /usr/share/man/man7/path_resolution.7.gz | nl -ba | sed -n '1,140p'`, `… sed -n '136,180p'` — exit 0 (source read for pins only).
4. `zcat /usr/share/man/man5/mako.5.gz | nl -ba | sed -n '40,55p'` — exit 0 (manual L45-48 include rule for the k10 pin).

No tool run against the candidate, no counter run (not even `--selftest`), no fixture repo, no git/jj command. Nothing written outside the two seat paths.

## Independence disclosure

- Read: the declaration draft (C2 section and fresh-start context), the C2 counter's module docstring only, `path_resolution(7)` lines 1-180, `mako.5` lines 40-55, and the C2 mutant list `controls/containment-mutants-r88.json` (allowed; it is a controls file, not the tool/build/counter body).
- The ranged read of the counter rendered lines 1-28 rather than 1-25; the extra lines are the docstring tail (`Inputs:` / `Exit map:`), and line 28 begins `import argparse`. No implementation body (no containment code, no parsing, no expected-value logic) was read.
- Not opened: `tools/mado-mako.py`, `.ufo/waves/round-88/build/`, the counter body, any committed tool revision. Case classes were derived from the stance text; the mutant list was consulted only to confirm the case classes the five mutants target (skip check, lexical resolution, prefix-without-separator, read roots ignored, home not a root) are represented.

## Case set (one line per case)

All cases declare `home: "home"`; only `width=` is used; every case sets width before its include line, so an escape's surviving value is the pre-include one.

1. `k01-symlink-file-escape` → escape → stance: "its fully resolved path (realpath: every symlink and `..` resolved) lies inside a declared read root"
2. `k02-symlink-dir-escape` → escape → path_resolution(7) L77-80: "If the component is found and is a symbolic link, we first resolve this symbolic link"
3. `k03-tilde-dotdot-escape` → escape → path_resolution(7) L141-143: "The path resolution process will assume that these entries have their conventional meanings"
4. `k04-absolute-outside-no-root` → escape → stance: "otherwise it is refused before it is stat'ed or opened, and the resolved path is what is opened"
5. `k05-prefix-sibling-escape` → escape → stance: "inside a declared read root — `--home` and each `--read-root DIR`"
6. `k06-chained-second-hop-escape` → escape → stance: "the include is refused (refusals present) and nothing from the target is applied"
7. `k07-symlink-root-then-escape` → escape → stance: "its fully resolved path (realpath: every symlink and `..` resolved) lies inside a declared read root"
8. `k08-missing-target-refused` → escape → stance: "missing or non-regular targets are refused"
9. `k09-directory-target-refused` → escape → stance: "missing or non-regular targets are refused"
10. `k10-tilde-include` → positive → mako.5 L45-48: "The path must be absolute or otherwise start with ~/"
11. `k11-absolute-inside-home` → positive → stance: "inside a declared read root — `--home` and each `--read-root DIR`"
12. `k12-symlink-inside-home` → positive → stance: "its fully resolved path (realpath: every symlink and `..` resolved) lies inside a declared read root"
13. `k13-outside-under-read-root` → positive → stance: "lies inside a declared read root — `--home` and each `--read-root DIR`"
14. `k14-symlink-into-read-root` → positive → stance: "its fully resolved path (realpath: every symlink and `..` resolved) lies inside a declared read root"
15. `k15-config-outside-home` → positive → stance: "The `--config` file itself is named by the caller and is not subject to the roots."
16. `k16-inhome-symlinked-dir` → positive → stance: "realpath: every symlink and `..` resolved" — `~/linkdir` resolves inside home
17. `k17-symlink-chain-inside-home` → positive → path_resolution(7) L107: "the maximum number of symbolic links that will be followed while resolving a pathname is 40"

Discriminating intent (why each escape is not redundant):

- k01 vs k02: final-component symlink vs a symlink in a *prefix directory* component; a lexical resolver passes k01 but still fails k02.
- k03: `..` text inside the include path (never in a `files` key), so only resolution of the include string itself can escape.
- k04: absolute outside path with no `--read-root` declared.
- k05: `<root>/home-evil/x.ini` against `home: "home"` — a `startswith(root)` check without the separator passes it (kills the prefix mutant class).
- k06: first hop inside home applies (`width=206` from `mid.ini`), second hop refused — distinguishes a whole-config rejection from a per-include refusal.
- k07: symlink into a declared root (`roots/`) whose own include escapes to `outside/`; the first hop must read (`width=207`), the second must refuse — separates containment of the resolved hop from containment of transitive includes.
- k08/k09: missing target and directory target (non-regular), both refused with the pre-include width surviving.
- Positives: k10 `~/`, k11 absolute-in-home, k12 symlink-in-home, k13 absolute outside under `--read-root`, k14 symlink into a declared root, k15 `--config` outside home (roots not applied to the config itself), k16 in-home symlinked directory component, k17 two-hop symlink chain inside home.

## Findings

- No contradiction found between the declaration's C2 stance and the authored cases; all 17 pins are verbatim fragments of the stance text, `path_resolution(7)`, or `mako.5` L45-48.
- Ambiguity noted for the L1 (not resolved here): k06/k07 assert that the *inner* file's own `width=` survives its refused second-hop include. This follows the stance's positional rule ("include content applied at the include line's position") plus target-scoped refusal ("nothing from the target is applied"), but if the tool instead rejects the whole file containing a refused include, k06 and k07 will be scored wrong. The alternative readings are unambiguous only from the stance text; a wave-2 note is warranted if the L1 wants that clarified in the declaration.
- k15 covers the `--config`-not-subject-to-roots clause; there is no declarative case for a *cycle* (item's stance lists cycles refused, but a cycle escape would duplicate k08/k09's "other include rules" class and the item's escape list does not require it). Not included to stay inside 14–20 without padding.

## Touched surfaces

- Written: `.ufo/waves/round-88/controls/containment-cases-r88.json` (new), `.ufo/waves/round-88/w1/R88MScribeCasesC2.md` (this report).
- Not touched: `tools/`, `quality/`, `corpus/`, `PROVINCE.md`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, the declaration, other lane files, fleet root, sibling repos, `scripts/`, `templates/`, `MANIFEST.json`, `.ufo/state/`, `.scratch/`.

## Out of scope / not done

- No candidate scoring, no counter execution, no mutant execution, no base-tool run (prohibited before the freeze and not in the item).
- No host mako config read (`~/.config/mako/…` not needed; the credential-material rule was not exercised beyond the man pages).
- No installs, no upgrades, so nothing to record under tooling authorization.
- No scratch directory was created (no clone, fixture, or counter `--scratch-root` use); nothing to clean, and no scratch remains on disk.

## Known limits

- Validation is structural only: the file has not been executed through the C2 counter. Whether the counter's `files` loader creates nested parent directories (k09's `home/adir/keep.ini`) and accepts directory-valued `symlink_to` (k02's `home/dir` → `outside`, k16's `home/linkdir` → `home/realdir`) is asserted from the documented schema, not observed.
- The expected `width` reachability check proves the literal is written somewhere in that case's files; it cannot prove the tool's include-order semantics until the L1 scores.
