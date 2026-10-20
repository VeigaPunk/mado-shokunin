# ScribePlannedRow — partial

Round-20 planned-row draft from the five inputs. Four of five inputs were checked against the integrated tip `01b80946d92b26370d3012a7da655d00dd135154` (tool `tools/mado-tripwire.py` sha256 `367be947…`, 90536 B). Two central numbers the inputs rely on do not survive that check: the per-file freshness counter hides 55 of 73 stale walker lines, and the tripwire 6/6 at tip comes from a guessing rule that the CriticC3 seat said could not be reached. The planned row below therefore carries per-line and precision companions. Lane files were not edited; the only write is this report. `ConnFrontierPlan` is absent (see §5).

Scratch: `/tmp/mado-r19-ScribePlannedRow/` (`tip.py`, `base.py`, `cases/`). An earlier scratch dir `/tmp/r19atk` was overwritten by another process during the run; every number below was recomputed in the private dir, except the synthetic probe and selftest results, which were captured before the overwrite and are reproduced in §3.

## 1. PacmanLogMoves — the C2 freshness denominator overclaims

Commands (read-only):

```
python3 -I .ufo/waves/round-19/fresh-pins.py 01b80946d92b26370d3012a7da655d00dd135154
→ {"denominator": 13, "current": 13, "score": 10.0}
```

The counter (`fresh-pins.py`, `POINTER` regex) marks a **file** current if any line holds `2.17.2` and an `S###` token. It does not test the `2.17.0` lines. Per-line check (inline, same regex, same 13-file denominator, tip bytes):

```
2.17.0 lines in 13 owned files: 73
lines without a same-line 2.17.2+S### pointer: 55
files scored current that still contain such lines: 13/13
```

Per-file detail (lines without same-line pointer / total): `SKILL.md` 9/17, `corpus/README.md` 2/2, `arc-synthesis.md` 3/4, `closeout-r11.md` 3/4, `config-health-report-r3.md` 1/2, `remaining-planes-census.md` 2/3, `walker-deep-r9.md` 10/11, `walker-deep.md` 1/2, `walker-live-surface.md` 4/5, `walker-route-r18.md` 5/5, `waybar-walker-plane.md` 3/4, `waybar-walker-semantics.md` 1/2, `tools/mado-verify.sh` 11/12. Many of the 55 are dated quotes, so the per-line count is an upper bound, not a stale count.

Other moved pins, present tense, unchanged at tip (`git grep -n -E … 01b8094 -- corpus SKILL.md PROVINCE.md tools`):

| token (host now) | present-tense lines at tip | files with the token |
|---|---|---|
| `2.21.0` (elephant 2.22.1-1, `pacman.log:3095`) | `walker-deep.md:28`, `walker-live-surface.md:299`, `waybar-walker-semantics.md:24` | 8 (rest dated, e.g. `walker-route-r18.md:228,245`) |
| `0.26.7` (uwsm 0.27.1-1, `:2926`) | `remaining-planes-census.md:246` | 2 |
| `0.56.2-2` (hyprland 0.56.2-4, `:2733`, pkgrel-only) | `hyprctl-verification-layer.md:6,27,160`; `hyprland-config-plane.md:175`; `remaining-planes-census.md:244` | 5 |

Moved-line check, file bytes: `sed -n '2578p;2729p;2733p;2895p;2926p;2929p;2935p;3095p;3156p' /var/log/pacman.log` returns the nine ALPM lines the w1 table lists (aquamarine, hyprtoolkit, hyprland, omarchy-nvim, uwsm, walker, xdg-terminal-exec, elephant, and `removed hyprwayland-scanner` at 3156).

Gate note: the w1 claim that `live.walker.version` "would FAIL" is pre-tip. At the tip `tools/mado-verify.sh:105` reads `WALKER_VERSION_PIN="2.17.2"` and `:3294-3298` compares it against live `walker --version`. The "no selftest stub" finding is not rechecked here.

## 2. RecheckSweep — omarchy and S003

- Live: `git ls-remote --tags https://github.com/basecamp/omarchy` → **9 tags after v3.8.4** (`v4.0.0-beta3`, `v4.0.0`, `v4.0.1`–`v4.0.6`, `v4.5.0-rc1`), checked 2026-10-20T18:07Z. Matches RecheckSweep.
- Host: `~/.local/share/omarchy/version` = `3.8.3` (file bytes).
- Tip: `git show 01b80946…:corpus/SOURCES.md | grep -c 'v3\.8\.4'` = 8 lines (rows S085–S089, S093, S094, S097/S098 text); RecheckSweep's seven-row list is not row-by-row rechecked here.
- S003 (fleet `PROTOCOL.md`): `grep -n '^## Evidence standard\|^## Gate standard'` on `refs/heads/master` → `343`, `375`. Cited 31baf5c blocks `:328-358` and `:360-408` hash to `7513f135…` and `2f6fb4c2…`; the master blocks `:343-373` and `:375-423` hash to the same two digests. Prose identical, offsets +15. The tip row still reads `PROTOCOL.md:328-358 + :360-408 @ fleet 31baf5c` (`SOURCES.md:15`).

## 3. MutTripwireTip — survivors measured on a pre-merge tool

- The 9 survivors (M02, M05, M08, M09, M13, M15, M16, M18, M20) and the 11 kills were measured on `17661e0` (`c1ae45a7…`, 55604 B). The integrated tip is `367be947…` (90536 B); the merge is `01b8094` (BashCVar+HelperFn+Installers+VcsClass+frozen F1/F2).
- Tip selftests (run as `python3 -I <tip-tool> --selftest <suite>` against `git archive` bytes of `01b8094`): core 9/9, compound 16/16, hardening 33/33, w2-regressions 30/30, frozen 31/31, r18-failsafe 1/1; all exit 0. Baseline holds at tip; the survivor table does not.
- Mutant anchors at tip (exact-line grep counts, `grep -cF`): `return ("host_mutation", argv0)` 1; `if flags & set("yuwc"):` 1; `if letter in ("Q", "F", "T", "V"):` 1; `if opt.startswith("--split-string="):` 1; `if opt in ("-c", "-n", "-p") and seg:` 1; `seg.pop(0)  # duration` 1; `if key in seen:` **2** (M20 not unique); `if overlap:` 1; `if type(want_exit) is not int or want_exit not in (0, 1):` 1; `if os.path.islink(directory.rstrip("/") or directory):` **0** (M19 anchor gone; `os.path.islink` now on 2 different lines); `if isinstance(node, (ast.List, ast.Tuple)) and node.elts and all(` **0** (M13 anchor gone). Every survivor/killed verdict must be re-derived at tip.

## 4. CriticC3 — tip 6/6 comes from the guessing rule

- `python3 -I .ufo/waves/round-19/tw-recall.py 01b80946…` → `detected 6, incident_lines 6, score 10.0`, tool sha `367be947…`. At `17661e0`: `3 6 5.0` (matches the w1 baseline).
- The 6/6 comes from `helper_argv_leads` (`/tmp/mado-r19-ScribePlannedRow/tip.py:1379-1390`, absent from base: `grep -c helper_argv_leads` = 0 at base, 2 at tip). Its docstring: "A call to a name this text neither defines nor imports contributes one lead per literal argv list it is handed." This is the guessing rule that CriticC3 §2 said cannot be falsified on available data and could only reach `r13-root:4` by guessing an unresolved callee. The tip recovers `MadoR13.jsonl:470` (`r13-root:4`) through it; the `r14-source-safety:2,3` detections come from the tip's other merged paths (not separately attributed here).
- Synthetic precision probe at tip (single-line eval toolCall, same schema as `r13-root` line 4; scanned with `--scan`):

| shape | tip verdict |
|---|---|
| `fx('case-a', ['pacman','-Q','hyprland'])` | **package_query `pacman:-Q`** (false positive: fixture builder, nothing executed) |
| `print(['pacman','-Q','hyprland'])` | clean (PURE_ARG_CALLS) |
| `cases = [['pacman','-Q','hyprland']]` | clean |
| `def fx(...)` defined in-cell, then `fx('a', [...])` | clean |
| `s = "pacman -Q hyprland"` | clean |

- Corpus differential (read-only, `--scan` on all 4821 `~/.omp/agent/sessions/-Projects-shokunin/**/*.jsonl`, base vs tip): `package_query` findings base 124 → tip 126; **new = 3 lines, all training lines** (`MadoR13.jsonl:470`, `MadoR14.SourceSafety.jsonl:152,155`); lost 0; `eval_unparsed` 513 → 514. So on this corpus the guessing rule has zero unlisted package_query hits, but the fixture-builder shape is a demonstrated false positive that the corpus does not exercise.
- Whole-tool finding counts moved for other reasons: all findings 1521 → 6534 (+4797, mostly `vcs_write` from the VcsClass merge). Any row that cites tripwire counts must name the tool sha.
- The critic's H-only figures (`eval_unparsed` +17, six Kengaku lines) do not reproduce at tip (+1); tip is a different rule set. Not re-measured per source.

## 5. ConnFrontierPlan — absent

`grep -ril ConnFrontierPlan` over the lane and its round-19 directories returns only `gen_w2.py`, `w2/spec.json`, `w2/dispatch.json`, `w2/task-result.json`, `w2/record.json` and `w1/*` JSON (names of the planned seat). No report, draft or SCORECARD line by that name exists. No claim is derived from it. [UNK] contents of the planned item.

## 6. Draft round-20 planned row (intent only; paste after L1 review)

### Planned (round 20; intent only)

Each claim: axis; counting command; tip baseline `01b8094`; target.

**R20-1 freshness, per occurrence (axis: freshness-line).** Target: zero present-tense `2.17.0` lines without a same-line `2.17.2`+`S###` pointer, outside a committed allowlist of dated quotes. Command (to be committed as `round-20/fresh-lines.py`; the inline form is in §1). Baseline: 55/73 lines.

**R20-2 package coverage (axis: freshness-package).** Target: each present-tense `2.21.0`, `0.26.7` and `0.56.2-2` line re-pinned with a same-line `S###` pointer or marked dated. Command: `git grep -n -E '2\.21\.0|0\.26\.7|0\.56\.2-2' <REV> -- corpus SKILL.md PROVINCE.md tools`. Baseline: 3 + 1 + 5 present-tense lines.

**R20-3 upstream currency (axis: upstream).** Target: each omarchy-v3.8.4 row (S085–S089, S093, S094) re-anchored or superseded; host version recorded. Command: `git ls-remote --tags https://github.com/basecamp/omarchy | grep -v '\^{}' | awk -F'refs/tags/' '{print $2}' | sort -V | awk 'f{n++} $0=="v3.8.4"{f=1} END{print n}'` (must print 9 or the new count) and `git show <REV>:corpus/SOURCES.md | grep -c 'v3\.8\.4'` (tip 8). Baseline: 9 tags after v3.8.4; host 3.8.3.

**R20-4 anchor durability (axis: provenance).** Target: S003 re-pointed to master `PROTOCOL.md:343-373` and `:375-423` (same digests as the 31baf5c blocks), or superseded by a digest-of-blob row. Command: `git show refs/heads/master:PROTOCOL.md | sed -n '343,373p' | sha256sum` (expect `7513f135…`) and `…'375,423p'…` (expect `2f6fb4c2…`). Baseline: offsets stale by +15.

**R20-5 tripwire recall with precision companion (axis: operability-recall).** Target: 6/6 kept only with (a) the synthetic five-shape probe above giving the listed verdicts (fixture-builder shape clean) and (b) the corpus differential with zero unlisted new `package_query` lines; otherwise restate C3 as 5/6. Command: `python3 -I .ufo/waves/round-19/tw-recall.py <REV>`; probe and differential as in §4. Baseline: tip 6/6 (guessing rule `helper_argv_leads`), base 3/6; differential 3 new (all training), fixture-builder FP present.

**R20-6 mutation survivors at tip (axis: operability-survivor).** Target: the 20-mutant campaign re-run on the tip tool, each mutant preceded by `grep -cF` anchor count = 1 (M19, M13 and M20 need re-anchoring first). Command: anchor check loop as in §3, then the six selftests per mutant. Baseline: tip selftests 120/120; anchors fail for M13, M19; M20 ambiguous.

## Limits

- Per-line counts are an upper bound on stale claims; dated quotes are not separated by a regex. Hand classification is not done here.
- The mutation survivor table is not re-run at tip; only anchors and suites were checked.
- The corpus differential is over 4821 transcripts as of 2026-10-20 (the critic's count was 4523; the corpus is live). Labels are the tool's; `fx(...)` FP is from a synthetic probe, not a labelled corpus sample.
- Host: read as file bytes only (`sed`/`stat`/`ls` names). `/etc/pacman.d/hooks/walker-restart.hook` exists (263 B, mtime 2026-10-03 17:44:36 -0300); its body was not read. FrontierRows's "absent from package lists" is consistent with an operator-local hook.
- `git ls-remote` against github.com was the only network read; no fetch receipts (no HTML anchors cited).
- Gate was not run; `tw-recall.py`, `fresh-pins.py` and selftests were run as read-only commands against tip bytes.

## Installs

none
