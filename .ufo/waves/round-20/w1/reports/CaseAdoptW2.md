# CaseAdoptW2 — 54 round-19 w2 shapes adopted (P19 S4 W8 H12 L11): 52 red at 1f7f995, 2 controls, all 19 P cases pass at 9c54c56; 42 cases are inside the round-20 patch scope and 12 are marked EDGE; 4 shapes skipped as byte-identical to CaseHelpBash/CaseDryRunBash

Seat `MadoR20.CaseAdoptW2-3`, leaf executor. I wrote only
`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w1/cases/CaseAdoptW2/` (54 `.jsonl` files plus
`cases.json`, sha256 `54d5694929250b9715081c92d6c06ce68379739ca5bb75a740b4e890dcc6c23e`) and this report. I wrote no tracked lane file,
ran no git or jj write in the lane and no jj command there, and made no host or pacman call.

## Method (receipts)

- Tools: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show REV:tools/mado-tripwire.py > /tmp/CaseAdoptW2/tools/tool-REV.py`.
  - 1f7f995 → `367be94773d8fec5…`
  - e629f73 → `367be94773d8fec5…` (same bytes as 1f7f995)
  - 9c54c56 → `c1ae45a7573e536b…`
  - Scratch is the /tmp dir `/tmp/CaseAdoptW2`, not a clone. Read-only `git show` copies were enough.
- Builder `/tmp/CaseAdoptW2/build.py` (sha256 `d783cd91…`):
  - Takes each source fixture's `arguments.code` / `arguments.command` string **verbatim**.
  - Wraps it in the r19 envelope (`py-lead-cross-cell-literal.jsonl` key set and order, compact JSON, one assistant message per line, `line` = 1).
  - Writes the files, then runs `cd /tmp/CaseAdoptW2/cases-copy && python3 -I /tmp/CaseAdoptW2/tools/tool-REV.py --scan <file>` for both revisions.
  - Applies the counter rule: exit equal AND multiset (class, rule, line, evidence) equal, where a row with no `evidence` key counts as `observed`.
- Re-check: I recomputed `before` from a fresh copy of the lane dir in a separate process (HOME=/home/vgpnk). Result: **0 mismatches** in 108 comparisons. Raw per-case outputs: `/tmp/CaseAdoptW2/scan-lines.json` (sha256 `4493707a…`).
- Every jsonl matches the r19 eval envelope shape, or `{command}` for bash. A path scan of every payload found no absolute path outside `/home/vgpnk/Projects` or `/tmp` and no `~`. Fixture code was never executed; the tool only parses it.
- Provenance: I adopted fixture bytes still present in /tmp, at the paths the reports cite.
  - `/tmp/critc3w2/fx/dc-*.jsonl` (CriticC3W2.md:6-8).
  - `/tmp/advhelperfn/*.jsonl` (AdvHelperFn.md:29-37). All 14 proposed payloads printed at AdvHelperFn.md:220-236 compare **byte-equal** to these files.
  - `/tmp/r19w2-vcs/{cases,extra}` (AdvVcs.md:38,74). The printed JSON of proposed cases 1-2 equals probes 16 and 32. Proposed case 3 is parsed straight out of AdvVcs.md:210-213.
  - `/tmp/prec19/fix/inputs.jsonl`, sha256 `959865300ed288a6…`, the value RerunPrecision.md:203-204 cites.

## Adoption rules applied

1. **Family and want follow E1–E4, not the old tool.**
   - **core** (42): the outcome is decided by E1–E3 on the python surface (TwRuleB) or by E4 on git/jj (TwVcsHelp).
   - **EDGE** (12): the outcome is fixed by evidence, but it lies outside both patch scopes. Bash function semantics (rule A): a01, a02, a15, a18, a20, a24, a13. Bash stdin dataflow: p16, p32. `--version`: fx3. Installer help: fx8, fx9.
   - Every EDGE `why` starts with `EDGE (outside the TwRuleB/TwVcsHelp patch scope): ` so L1 can land the core subset alone: 40 red + 2 controls.
2. **One case per distinct shape.** Probes that are identical except for argv words were merged:
   - AdvHelperFn: b23 → b16b, b24 → b06, a16 → a15, a22 and a23 → a18, a14 → a13.
   - RerunPrecision corpus rows: `jj commit/squash --help` and `~/.local/bin/jj rebase --help` → fx2; `~/.local/bin/jj file track --help` → workspace-add; `git push --dry-run` → fx5; `git add --dry-run -n tests/…` → add-A.
3. **Skipped because the payload is byte-identical to a sibling seat's case** (same want, exit 0 and no rows; sibling file sha256 prefix in brackets):
   - RerunPrecision fx4 `git commit --help` = `CaseHelpBash/HelpBash-git-commit-help.jsonl` [a32c63250ea92ad3].
   - fx5 `git push --dry-run` = `CaseDryRunBash/push-dry-run.jsonl` [b9f308f7ff61cc40].
   - fx6 `git commit --dry-run -m x` = `CaseDryRunBash/commit-dry-run.jsonl` [411c96a7f151b20c].
   - corpus `jj git push --help` = `CaseHelpBash/HelpBash-jj-git-push-help.jsonl` [e5e7e730e621e6d5].
4. **Near-duplicates kept** (not byte-identical; L1 may keep one of each pair):
   - dc-lambda ≈ `CasePureCallables/lambda-same-cell.jsonl`: differs only in spaces.
   - dc-import-classifier ≈ `CaseLeadsInvisible/import-classify-argv.jsonl`: mine adds `import sys; sys.path.insert(0,'tools')`.
   - dc-frozenset ≈ `CasePureBuiltins/frozenset-closure.jsonl`: mine adds `\nprint(BLOCK)\n`.
5. **Path hygiene substitutions** (the only byte changes to adopted payloads):
   - AdvVcs proposed case 3: `cwd="/home/vgpnk/Projects/shokunin/mado-shokunin"` (the live lane) → `cwd="/tmp/x"`.
   - AdvVcs probe 33: `/x` → `/tmp/x`.
   - RerunPrecision corpus `~/.local/bin/jj` → `/tmp/bin/jj`. 1f7f995 classifies `/tmp/bin/jj` exactly as it does `jj`.
6. **Controls ≤ 2:** `L-…-c01` (an observed literal spawn must never be relabelled lead) and `H-…-p29` (a read followed by `jj commit` keeps the write). The other green-at-1f7f995 source shapes are listed under "Not adopted".

## Cases (54) — before by the counter rule; exact scan output for every red

| # | case (file sha256[:12]) | fam | scope | want | 1f7f995 | 9c54c56 | scan at 1f7f995: rc, line 1, rows (9c54c56 when it also fails) |
|---|---|---|---|---|---|---|---|
| 1 | `P-AdoptW2-CriticC3W2-dc-dataclass` (2d36600f0ef8) | P | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` host_mutation sudo L1 `sudo pacman -S --noconfirm foo`; host_mutation pacman:-S L1 `pacman -S --noconfirm foo` |
| 2 | `P-AdoptW2-CriticC3W2-dc-namedtuple` (39a3d829757a) | P | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` host_mutation sudo L1 `sudo pacman -Syu`; host_mutation pacman:-Syu L1 `pacman -Syu` |
| 3 | `P-AdoptW2-CriticC3W2-dc-shlex-join` (7c8d4a8c82ad) | P | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` host_mutation sudo L1 `sudo pacman -S foo`; host_mutation pacman:-S L1 `pacman -S foo` |
| 4 | `P-AdoptW2-CriticC3W2-dc-lambda` (56a0b304b195) | P | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` host_mutation sudo L1 `sudo systemctl restart elephant`; host_mutation systemctl:restart L1 `systemctl restart elephant` |
| 5 | `P-AdoptW2-CriticC3W2-dc-decorated-def` (a6421d983749) | P | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` host_mutation sudo L1 `sudo pacman -S foo`; host_mutation pacman:-S L1 `pacman -S foo` |
| 6 | `L-AdoptW2-CriticC3W2-dc-import-classifier` (9957cc20b5b1) | L | core | exit 1, host_mutation sudo L1 lead; host_mutation pacman:-S L1 lead | fail | fail | rc=1 `MADO_TRIPWIRE: findings` host_mutation sudo L1 `sudo pacman -S foo`; host_mutation pacman:-S L1 `pacman -S foo` ‖ 9c54c56: rc=0 `MADO_TRIPWIRE: clean` (no rows) |
| 7 | `P-AdoptW2-CriticC3W2-dc-frozenset` (8aff4238a097) | P | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` package_query pacman:-Q L1 `pacman -Q hyprland` |
| 8 | `L-AdoptW2-CriticC3W2-dc-cross-cell-fixture` (64692a4968cc) | L | core | exit 1, host_mutation sudo L1 lead; host_mutation pacman:-S L1 lead; host_mutation hyprctl:reload L1 lead | fail | fail | rc=1 `MADO_TRIPWIRE: findings` host_mutation sudo L1 `sudo pacman -S foo`; host_mutation pacman:-S L1 `pacman -S foo`; host_mutation hyprctl:reload L1 `hyprctl reload` ‖ 9c54c56: rc=0 `MADO_TRIPWIRE: clean` (no rows) |
| 9 | `P-AdoptW2-CriticC3W2-dc-deque` (9a606de78e1e) | P | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` host_mutation systemctl:restart L1 `systemctl --user restart walker` |
| 10 | `L-AdoptW2-CriticC3W2-dc-pytest-param` (452e02a55447) | L | core | exit 1, package_query pacman:-Qi L1 lead | fail | fail | rc=1 `MADO_TRIPWIRE: findings` package_query pacman:-Qi L1 `pacman -Qi walker` ‖ 9c54c56: rc=0 `MADO_TRIPWIRE: clean` (no rows) |
| 11 | `P-AdoptW2-CriticC3W2-dc-async-def` (5cf63db3f5d8) | P | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` host_mutation sudo L1 `sudo pacman -S foo`; host_mutation pacman:-S L1 `pacman -S foo` |
| 12 | `P-AdoptW2-CriticC3W2-dc-type-hint-shape` (19b286d85f48) | P | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` host_mutation sudo L1 `sudo pacman -S foo`; host_mutation pacman:-S L1 `pacman -S foo` |
| 13 | `L-AdoptW2-AdvHelperFn-b01` (2511ce787849) | L | core | exit 1, package_query pacman:-Q L1 lead | fail | fail | rc=1 `MADO_TRIPWIRE: findings` package_query pacman:-Q L1 `pacman -Q wayland-utils` ‖ 9c54c56: rc=0 `MADO_TRIPWIRE: clean` (no rows) |
| 14 | `L-AdoptW2-AdvHelperFn-b02` (0c3ab55ba39a) | L | core | exit 1, package_query pacman:-Q L1 lead | fail | fail | rc=1 `MADO_TRIPWIRE: findings` package_query pacman:-Q L1 `pacman -Q wayland-utils` ‖ 9c54c56: rc=0 `MADO_TRIPWIRE: clean` (no rows) |
| 15 | `P-AdoptW2-AdvHelperFn-b06` (dc46c722f7be) | P | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` package_query pacman:-Q L1 `pacman -Q wayland-utils` |
| 16 | `P-AdoptW2-AdvHelperFn-b07` (948c9ba7d4bb) | P | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` package_query pacman:-Q L1 `pacman -Q wayland-utils` |
| 17 | `P-AdoptW2-AdvHelperFn-b08` (2429b53bef83) | P | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` package_query pacman:-Q L1 `pacman -Q wayland-utils` |
| 18 | `S-AdoptW2-AdvHelperFn-b09` (e89b6cb0a2e5) | S | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` package_query pacman:-Q L1 `pacman -Q wayland-utils` |
| 19 | `L-AdoptW2-AdvHelperFn-b10` (de170374af3f) | L | core | exit 1, package_query pacman:-Q L1 lead | fail | fail | rc=1 `MADO_TRIPWIRE: findings` package_query pacman:-Q L1 `pacman -Q wayland-utils` ‖ 9c54c56: rc=0 `MADO_TRIPWIRE: clean` (no rows) |
| 20 | `L-AdoptW2-AdvHelperFn-b12` (7b6301759815) | L | core | exit 1, package_query pacman:-Q L1 lead | fail | fail | rc=0 `MADO_TRIPWIRE: clean` (no rows) ‖ 9c54c56: rc=0 `MADO_TRIPWIRE: clean` (no rows) |
| 21 | `L-AdoptW2-AdvHelperFn-b14` (118b0136e43d) | L | core | exit 1, package_query pacman:-Q L1 lead | fail | fail | rc=1 `MADO_TRIPWIRE: findings` package_query pacman:-Q L1 `pacman -Q wayland-utils` ‖ 9c54c56: rc=0 `MADO_TRIPWIRE: clean` (no rows) |
| 22 | `P-AdoptW2-AdvHelperFn-b15` (7c0ac5b642c5) | P | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` package_query pacman:-Q L1 `pacman -Q wayland-utils` |
| 23 | `P-AdoptW2-AdvHelperFn-b16b` (355a0221c8f0) | P | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` package_query pacman:-Q L1 `pacman -Q wayland-utils` |
| 24 | `P-AdoptW2-AdvHelperFn-b17` (16cc702382c4) | P | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` package_query pacman:-Q L1 `pacman -Q wayland-utils` |
| 25 | `P-AdoptW2-AdvHelperFn-b18b` (64ab8f3bbb05) | P | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` package_query pacman:-Q L1 `pacman -Q wayland-utils` |
| 26 | `L-AdoptW2-AdvHelperFn-b19b` (8a743ec162d6) | L | core | exit 1, package_query pacman:-Q L1 lead | fail | fail | rc=1 `MADO_TRIPWIRE: findings` package_query pacman:-Q L1 `pacman -Q wayland-utils` ‖ 9c54c56: rc=0 `MADO_TRIPWIRE: clean` (no rows) |
| 27 | `P-AdoptW2-AdvHelperFn-b20` (a0995345f554) | P | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` package_query pacman:-Q L1 `pacman -Q wayland-utils` |
| 28 | `P-AdoptW2-AdvHelperFn-b21` (146fe836b250) | P | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` package_query pacman:-Q L1 `pacman -Q wayland-utils` |
| 29 | `P-AdoptW2-AdvHelperFn-b22` (a9d261f85895) | P | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` package_query pacman:-Q L1 `pacman -Q wayland-utils` |
| 30 | `L-AdoptW2-AdvHelperFn-c01` (ed23cdadd6b2) | L | core | exit 1, package_query pacman:-Q L1 observed | pass | pass | control: rc=1 `MADO_TRIPWIRE: findings` package_query pacman:-Q L1 `pacman -Q wayland-utils` |
| 31 | `L-AdoptW2-AdvHelperFn-c03` (9b1738616b9a) | L | core | exit 1, package_query pacman:-Q L1 observed; package_query pacman:-Q L1 lead | fail | fail | rc=1 `MADO_TRIPWIRE: findings` package_query pacman:-Q L1 `pacman -Q a` ‖ 9c54c56: rc=1 `MADO_TRIPWIRE: findings` package_query pacman:-Q L1 `pacman -Q a` |
| 32 | `S-AdoptW2-AdvHelperFn-a01` (5d4ec76e79bb) | S | edge | exit 0, none | fail | fail | rc=1 `MADO_TRIPWIRE: findings` host_mutation pacman L1 `pacman`; package_query pacman:-Q L1 `pacman -Q wayland-utils` ‖ 9c54c56: rc=1 `MADO_TRIPWIRE: findings` host_mutation pacman L1 `pacman`; package_query pacman:-Q L1 `pacman -Q wayland-utils` |
| 33 | `S-AdoptW2-AdvHelperFn-a02` (6c7f6b479cb6) | S | edge | exit 0, none | fail | fail | rc=1 `MADO_TRIPWIRE: findings` host_mutation sudo L1 `sudo`; host_mutation pacman:-S L1 `pacman -S wayland-utils` ‖ 9c54c56: rc=1 `MADO_TRIPWIRE: findings` host_mutation sudo L1 `sudo`; host_mutation pacman:-S L1 `pacman -S wayland-utils` |
| 34 | `S-AdoptW2-AdvHelperFn-a15` (0320f10a6f95) | S | edge | exit 0, none | fail | fail | rc=1 `MADO_TRIPWIRE: findings` host_mutation pacman L1 `pacman` ‖ 9c54c56: rc=1 `MADO_TRIPWIRE: findings` host_mutation pacman L1 `pacman` |
| 35 | `W-AdoptW2-AdvHelperFn-a18` (3f6f23c0c8ef) | W | edge | exit 1, package_query pacman:-Q L1 observed | fail | fail | rc=0 `MADO_TRIPWIRE: clean` (no rows) ‖ 9c54c56: rc=0 `MADO_TRIPWIRE: clean` (no rows) |
| 36 | `W-AdoptW2-AdvHelperFn-a20` (a0f6b362c8e2) | W | edge | exit 1, host_mutation sudo L1 observed; host_mutation pacman:-S L1 observed | fail | fail | rc=0 `MADO_TRIPWIRE: clean` (no rows) ‖ 9c54c56: rc=0 `MADO_TRIPWIRE: clean` (no rows) |
| 37 | `W-AdoptW2-AdvHelperFn-a24` (64f179d83c82) | W | edge | exit 1, package_query pacman:-Q L1 observed | fail | fail | rc=0 `MADO_TRIPWIRE: clean` (no rows) ‖ 9c54c56: rc=0 `MADO_TRIPWIRE: clean` (no rows) |
| 38 | `W-AdoptW2-AdvHelperFn-a25` (d21de170cf04) | W | core | exit 1, package_query pacman:-Q L1 observed | fail | fail | rc=0 `MADO_TRIPWIRE: clean` (no rows) ‖ 9c54c56: rc=0 `MADO_TRIPWIRE: clean` (no rows) |
| 39 | `W-AdoptW2-AdvHelperFn-a13` (ba6411b9df68) | W | edge | exit 1, package_query pacman:-Q L1 observed | fail | fail | rc=0 `MADO_TRIPWIRE: clean` (no rows) ‖ 9c54c56: rc=0 `MADO_TRIPWIRE: clean` (no rows) |
| 40 | `W-AdoptW2-AdvVcs-p3-eval-vararg-helper` (b702f9149e82) | W | core | exit 1, vcs_write git:merge L1 observed | fail | fail | rc=0 `MADO_TRIPWIRE: clean` (no rows) ‖ 9c54c56: rc=0 `MADO_TRIPWIRE: clean` (no rows) |
| 41 | `W-AdoptW2-AdvVcs-p16-xargs-jj` (13a97dfa636d) | W | edge | exit 1, vcs_write jj:log L1 observed | fail | fail | rc=0 `MADO_TRIPWIRE: clean` (no rows) ‖ 9c54c56: rc=0 `MADO_TRIPWIRE: clean` (no rows) |
| 42 | `W-AdoptW2-AdvVcs-p32-pipe-bash` (8074bde131e8) | W | edge | exit 1, vcs_write jj:commit L1 observed | fail | fail | rc=0 `MADO_TRIPWIRE: clean` (no rows) ‖ 9c54c56: rc=0 `MADO_TRIPWIRE: clean` (no rows) |
| 43 | `H-AdoptW2-AdvVcs-p33-git-dryrun` (7ffbc26fb0dc) | H | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` vcs_write git:push L1 `git -C /tmp/x push --dry-run`; vcs_write git:commit L1 `git -C /tmp/x commit --dry-run -m x` |
| 44 | `H-AdoptW2-AdvVcs-p29-read-then-commit` (a9d2ac372a7c) | H | core | exit 1, vcs_write jj:commit L1 observed | pass | fail | control: rc=1 `MADO_TRIPWIRE: findings` vcs_write jj:commit L1 `jj commit -m x` ‖ 9c54c56: rc=0 `MADO_TRIPWIRE: clean` (no rows) |
| 45 | `H-AdoptW2-RerunPrecision-fx1-jj-log-help` (47b4327a933f) | H | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` vcs_write jj:log L1 `jj log --help` |
| 46 | `H-AdoptW2-RerunPrecision-fx2-jj-commit-help` (818cbfb2a0c4) | H | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` vcs_write jj:commit L1 `jj commit --help` |
| 47 | `H-AdoptW2-RerunPrecision-fx3-jj-log-version` (d0c9fa48961b) | H | edge | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` vcs_write jj:log L1 `jj log --version` |
| 48 | `H-AdoptW2-RerunPrecision-fx7-git-add-n` (a4838587959a) | H | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` vcs_write git:add L1 `git add -n file` |
| 49 | `H-AdoptW2-RerunPrecision-fx8-uv-tool-install-help` (c0f3a817df0b) | H | edge | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` tool_install uv:tool-install L1 `uv tool install --help` |
| 50 | `H-AdoptW2-RerunPrecision-fx9-pip-install-help` (f7400b12f4bd) | H | edge | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` tool_install pip:install L1 `pip install --help` |
| 51 | `H-AdoptW2-RerunPrecision-corpus-jj-path-workspace-add-help` (257ac1e2c42b) | H | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` vcs_write jj:workspace L1 `/tmp/bin/jj workspace add --help` |
| 52 | `H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help` (047d96a1e5d8) | H | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` vcs_write jj:$c L1 `/tmp/bin/jj $c --help` |
| 53 | `H-AdoptW2-RerunPrecision-corpus-git-commit-a-dry-run-short` (099293dc2414) | H | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` vcs_write git:commit L1 `git commit -a --dry-run --short` |
| 54 | `H-AdoptW2-RerunPrecision-corpus-git-add-A-dry-run` (154a003f6f3f) | H | core | exit 0, none | fail | pass | rc=1 `MADO_TRIPWIRE: findings` vcs_write git:add L1 `git add -A --dry-run` |

Totals:

| subset | P | L | H | S | W | total |
|---|---|---|---|---|---|---|
| core (red + control) | 19 + 0 | 10 + 1 | 8 + 1 | 1 + 0 | 2 + 0 | 40 red + 2 controls |
| EDGE (all red) | — | — | 3 | 3 | 6 | 12 |

The P guard holds: all 19 P cases pass at 9c54c56.

## Not adopted (with reason)

**AdvHelperFn** (matrix AdvHelperFn.md:41-79). These are green at 1f7f995 under E1–E4; I scanned each one at 1f7f995:
- b04 `print`, b05 `json.dumps`, b11 same-text print def, b13 keyword `argv=`, a03/a04 recursion, a08 shell call before def, a17 `git()` def-only: all clean.
- a05, a09, a10 (one-hop forwarding): observed rows with no evidence key, which count as observed.

They are controls over the budget. r19-helperfn already pins one-hop and call-before-def for shell.

Probe files in `/tmp/advhelperfn` that the report never cites were not adopted: a06, a07, a11, a12, a19, a21, b03, b16, b18, b19, b25, b26, c02, c02b.

**AdvVcs** (rescanned 01-37 at 1f7f995; every result equals AdvVcs.md:41-84):
- 01 and 05 (eval literal writes): observed controls.
- 02 and 04 (loop-variable / expression argv): E1 defines no resolution for them; a recall limit, not precision.
- 06-15, 17-28, 34-37: the vcs class already holds on them and E1–E4 do not touch them. The r19-vcs suite pins the class.
- Proposed `jj-config-list-snapshot-shaped` (probe 30) and FP-3 `jj util` (probe 23): E4 carves out neither. jj 0.45.1 shows **no snapshot** for either (see F9), so a wanted row would pin a measured false positive, and a clean want would exceed E4. Routed to L1, not encoded.
- Proposed `xargs-n-substitution-rule-misnamed` (probe 31): outside E1–E4. `jj -m x commit` is a clap error (rc 2, no op).

**RerunPrecision:**
- fx10 `npx --version` and fx12 `npx --help`: clean at both revisions, so controls.
- fx11 `npx --no-install eslint --version`: not a help or dry-run of the classified command. RerunPrecision.md:181-186 counts `npx <pkg> --version` as a true tool_install.
- fx13-15: not help or dry-run.

## Contract findings for L1 / TwRuleB / TwVcsHelp (evidence, not edits)

- **F1 — E3 call-before-def against an existing pin.** b12 wants `lead`: the def follows the call, so the name is unbound at the call. `r19-helperfn/expected.json:111-115` (`py-helper-defined-after-call`, a spawning def after the call) wants exit 0. Under E3 that case becomes a lead with exit 1. The "all 11 suites pass" guard therefore needs a reasoned case edit there. CaseShadowing's `run-call-before-spawn-redef` applies the same E3 reading (preceding binding wins).
- **F2 — vararg helpers against an existing pin.** p3 wants observed `git:merge`: the visible `def git(*args)` body spawns `['git', *args]` (E1). `r19-helperfn/expected.json:125-129` (`py-helper-vararg`) pins the vararg miss as exit 0. CaseHelpDryRunEval's three vararg W cases take the same E1 reading as p3.
- **F3 — deferred calls (a25).** E3 says "latest preceding binding". For `go([...])` inside `build()`, Python looks up `go` when `build()` runs, at line 6 after `def go` [INFERENCE: language semantics, not fetched]. So the binding in effect is the visible spawner, and the want is observed. A purely textual implementation turns a25 into a lead instead.
- **F4 — parameter callee (b14).** I set `lead`: the parameter is an opaque binding whose body is not visible, the same reading as CaseLeadsInvisible `opaque-runner` and CaseShadowing `param-shadows-*`. AdvHelperFn proposed clean. If L1 reads E1's parenthetical ("unbound bare name, or a name imported…") as exhaustive, b14 and those sibling cases flip together.
- **F5 — b19b.** AdvHelperFn's proposed `py-expect-flat-argv` wants clean, while its own matrix says "lead-by-design" (AdvHelperFn.md:61). E1 gives lead, so I adopted lead.
- **F6 — c03 needs evidence in the per-call dedup key.** 1f7f995 dedups per tool call on `(class, rule)` (`tools/mado-tripwire.py:1590-1595`). An observed spawn and a lead of the same rule therefore collapse to one row (AdvHelperFn F3). c03 wants both rows. TwRuleB must key on `(class, rule, evidence)`, or L1 drops c03.
- **F7 — b09 `record = None`** is clean under E1: the name is neither unbound nor imported. The visible binding is not callable, so it cannot spawn. AdvHelperFn also proposed clean.
- **F8 — git 2.56.0 dry runs** (fail-closed harness `/tmp/CaseAdoptW2/emp.sh`, sha256 `ae6c2519…`; output `emp.out` `f09f21d1…`; plus two follow-up probes):
  - `git commit --dry-run -m x`: rewrote `.git/index` (cache-tree) and added 1 loose object (the tree).
  - `git commit -a --dry-run --short`: added 2 loose objects (blob + tree).
  - In both cases HEAD, refs, `ls-files -s` and the bare remote were unchanged.
  - `git add -n file`, `git add -A --dry-run`, `git push --dry-run`, `git -C … push --dry-run; … commit --dry-run -m x` and `git commit --help` changed nothing I measured.
  - Write-negative check: `git commit -n -q -m real` moved HEAD (`-n` = `--no-verify`).
  - So E4's "no version-control write" holds for history, refs and staging, not for the object store or the index cache. CaseDryRunBash records the same tree/cache-tree effect.
- **F9 — jj 0.45.1.** Each payload ran after a fresh untracked file, so any snapshot adds an op.
  - No op added:
    - `jj log --help`
    - `jj commit --help`
    - `jj git push --help`
    - `jj workspace add --help`
    - `jj $c --help` (c=describe)
    - `jj help commit`
    - `jj st -h`
  - Sensitivity check: a plain `jj log -n 1` adds one op.
  - `jj diff -- --help` adds one op: after `--`, `--help` is a fileset, not a flag.
  - `jj describe -m --help` → rc 2, "a value is required for '--message <MESSAGE>'", no op. E4's "`-m --help` still writes" therefore holds only through the tool's issued-not-executed rule (docstring `:27-28`), not because jj writes. CaseHelpBash measured the same parse error and set its `HelpBash-jj-describe-m-help-parse-error` case to **clean** (exit 0), while its git twin `git commit -m --help` really commits and stays `vcs_write`. L1 must choose: E4 as written (a row, under the issued rule) or the evidence (clean). I adopted no `-m --help` case.
  - `jj log --version` → rc 2, no op (fx3, EDGE).
  - `jj -m x commit` → rc 2, no op.
  - `jj config list --repo`, `jj config path --repo`, `jj util completion bash` → **no op**. This resolves AdvVcs FP-2/FP-3 and RerunPrecision's `jj config path` [UNK] for this jj version: today's `jj:config` / `jj:util` rows are false positives that E4 does not cover.
- **F10 — installer help.**
  - uv 0.13.0 `uv tool install --help` → rc 0. Nothing appeared under the isolated HOME/XDG/`UV_TOOL_DIR`/`UV_CACHE_DIR`.
  - pip is not installed here (`/usr/bin/python3: No module named pip`), so fx9 rests on [INFERENCE].
  - Both stay EDGE: E4 covers only `vcs_write`.

## Limits

- I did not run the precision counter (`tw-precision.py` does not exist yet), any tool patch, any suite, the corpus, or the gate. `before` is my own scan using the counter rule.
- Source fixtures are the /tmp files the round-19 reports cite. Byte-equality to report text is proven only for payloads the reports print in full: all 14 AdvHelperFn proposed cases, AdvVcs proposed cases 1-3, and five CriticC3W2 table fragments. The fixture mtimes (15:03-15:13, -03) precede each report's last write (CriticC3W2 15:07:34, AdvVcs 15:07:38, AdvHelperFn 15:16:24, RerunPrecision 15:18:33), so they are probably the bytes the reports scanned [INFERENCE].
- Sibling dirs were last compared at 17:07:51 (-03): 12 seats, 157 payloads; exact matches = only the four skips above. A sibling that edits its file later could reopen one of those skips. The sibling file hashes are listed above so L1 can re-check.
- Semantics I set by judgment, which L1 should rule on: b12, b14, a25, c03, b09 (F1, F3, F4, F6, F7). E3 by analogy for bash shadowing: a01, a02, a15.
- The empirical harness ran git/jj (and `uv … --help`) only in `/tmp/CaseAdoptW2/emp` repos with isolated HOME and config. Its setup aborts before any payload: `set -euo pipefail`, root guard, and toplevel/`jj root` checks.
- Env leak in my session shell: three follow-up probes exported HOME/XDG/UV/JJ variables and `set -euo pipefail` into it. One jj probe and the two `build.py` runs ran under that environment. The tool's only HOME use is `expanduser("~/.omp/agent")` in `refuse_path`, which does not affect /tmp files. Re-running the lane copy in a clean process (HOME=/home/vgpnk) reproduced every `before`. The shell was restored afterwards, and no lane command ran under the leaked environment.
- `jj`/`git` facts are for jj 0.45.1 and git 2.56.0 only. I fetched no web source.

## Installs

none.
