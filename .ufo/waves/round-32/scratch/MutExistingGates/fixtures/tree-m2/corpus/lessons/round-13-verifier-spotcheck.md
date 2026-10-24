author: hyaku closure (non-author integrator, @m_strong)

# Round 13 — independent verification and source spot-check

Date: 2026-10-20. Status **ok**; **admitted**. This review did not author the round and changes no lane-authored record or SHONEN box.

Before: `7dcb785b7b943d03703181b218d7860a7b43007b`.
Delivered revision: `59cfbdc3ab5e7b6aaf68f86e1b2ae8d51c938b1e`.
Measured content: `95cbc41fe5d5db121b89c2ddd1f953728663c5f4`.
Report: fleet `.ufo/reports/round-13/mado.md`, carrying commit `50f6f4558ffe09eb4ca245d7f2075536751d76f7`.

## Step-1 conformance

Commands actually run from the fleet root:

```sh
git log --format='%an %ae %H %aI' -- .ufo/reports/round-13/mado.md
git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain
git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-list --count @{u}..HEAD
git -C /home/vgpnk/Projects/shokunin/mado-shokunin merge-base --is-ancestor 7dcb785b7b943d03703181b218d7860a7b43007b HEAD
git -C /home/vgpnk/Projects/shokunin/mado-shokunin merge-base --is-ancestor 95cbc41fe5d5db121b89c2ddd1f953728663c5f4 HEAD
git -C /home/vgpnk/Projects/shokunin/mado-shokunin merge-base --is-ancestor 59cfbdc3ab5e7b6aaf68f86e1b2ae8d51c938b1e HEAD
git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff 7dcb785b7b943d03703181b218d7860a7b43007b 59cfbdc3ab5e7b6aaf68f86e1b2ae8d51c938b1e -- SCORECARD.md
```

Observed: report author `mado-shokunin mado@shokunin.local`, report commit above, authored `2026-10-20T01:51:31-03:00`; lane worktree empty; ahead count **0**; all three ancestry exits **0**. Lane-authored content and measurement commits precede the report. Report has all six required sections and **four** `[~]` lines under `## SHONEN`; substantial committed work, not a marker.

Rendered the canonical `kimi-shokunin/templates/round-prompt.md` in memory with lane=mado, round=13, the absolute fleet root, declared axes and lane working directory. Compared it to the full operative prefix of `.ufo/prompts/mado-round-13.md`: `PROMPT_TEMPLATE_PREFIX True`; `git ls-files --error-unmatch` for the prompt exited **0**. Campaign addendum retains L1 planner mapping and one validated 32-seat native wave; no contradictory hardcoded route table in the template contract.

Durable dispatch/completion digest, copied verbatim from the closure dispatch:

```text
2026-10-20T01:04:05-03:00 launch mado round=13 pgid=654654 driver=hyaku-inline attempt=1
2026-10-20T01:52:01-03:00 complete mado round=13; hyaku-inline attempt=1
```

Elapsed time exceeded two ticks, but two pushed mado-authored commits establish progressing work, not silence. No new mission is opened here.

History pin was checked using committed JSON, not a closure-gate execution: `sha256(json.dumps(rounds[:48], sort_keys=True, separators=(',', ':')).encode())` is `ce97497ed699a8f0939be062d042cf4d6e3e7531116fbe4681593991d67f0a8e` both at fleet HEAD and anchor `ae19fca`; equals `.ufo/history-pin.json`; anchor ancestry exit **0**. No pin was rewritten.

## Claims — independently re-measured versus evidence-verified

No lane gate, harness, selftest or lane `measure.py` was executed. Plain committed-byte counts below were run independently in Python through `git show` / `git ls-tree`; C2 behavioral execution is **evidence-verified**, not a fresh behavioral run. Three fresh read-only seats independently reviewed coverage, gate evidence and no-harm; the integrator makes the final judgment.

### C1 coverage — improved; independently re-measured

The following is the independent counting recipe actually used (the final source-line selector searches `^source:`, not the first physical line):

```python
import subprocess, re, collections
R = '/home/vgpnk/Projects/shokunin/mado-shokunin'
B = '7dcb785b7b943d03703181b218d7860a7b43007b'
A = '59cfbdc3ab5e7b6aaf68f86e1b2ae8d51c938b1e'
def git(*args):
    return subprocess.check_output(['git', '-C', R, *args], text=True)
def blob(rev, path):
    return git('show', f'{rev}:{path}')
for rev in (B, A):
    rows = {}
    for line in blob(rev, 'corpus/SOURCES.md').splitlines():
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if cells and re.fullmatch(r'S\d{3,}', cells[0]):
            rows[cells[0]] = cells
    joins = []
    for path in git('ls-tree', '-r', '--name-only', rev, '--',
                    'corpus/knowledge').splitlines():
        text = blob(rev, path)
        covers = re.search(r'^covers: (U[1-7])\s*$', text, re.M)
        source = re.search(r'^source: (.*)$', text, re.M)
        if not covers or not source:
            continue
        ids = [s for s in re.findall(r'\bS\d{3,}\b', source[1])
               if s in rows and rows[s][7] == 'mined'
               and path in rows[s][10]]
        if ids:
            joins.append((covers[1], path, ids))
    items = sorted({j[0] for j in joins})
    print(rev, len(rows), items, len(items), round(len(items)*10/7, 4))
    print('tiers', dict(collections.Counter(r[3] for r in rows.values())))
    print('statuses', dict(collections.Counter(r[7] for r in rows.values())))
    print('joins', joins)
```

Observed output, reduced without changing values:

```text
before rows=39 covers=[U1,U2,U3] count=3 score=4.2857
       tiers A/B/C=35/1/3 statuses mined/queued/rejected=27/9/3
after  rows=46 covers=[U1,U2,U3,U4] count=4 score=5.7143
       tiers A/B/C=42/1/3 statuses mined/queued/rejected=34/8/4
U4 joins: S005 S040 S041 S042 S043 S046, all mined and reciprocal
```

Own committed-byte equality check found `tools/mado-verify.sh`, `corpus/README.md`, `corpus/SOURCES.md` and the U4 entry identical between measured content `95cbc41` and delivered `59cfbdc`. Coverage reviewer independently counted **26/26 → 27/27** knowledge/index paths with no missing, extra or duplicate note; the committed measurement agrees. Navigation did not regress.

Substantive spot read: U4 has three real decision rows (phase, advertisement, unexercised behavior), a phase/version table, separate registry bind/global semantics, explicit diagnostic bindings/detail-query limitations and a safe projection recipe. It is not a header-only entry. The delta is one bounded U4 knowledge entry, **not seven source rows or complete protocol-feature coverage**. U5–U7 and per-interface phase classification remain open.

### C2 operability — improved; committed execution evidence verified

Independent recount of the committed behavioral transcripts, executed against delivered `A` without invoking their producing program:

```python
import json
for name in ('before', 'after'):
    text = blob(A, f'.ufo/waves/round-13/evidence/{name}.txt')
    data = json.JSONDecoder().raw_decode(text[text.index('{'):])[0]
    passed = []
    for case in data['exact_set']['cases']:
        ok = (case['exit'] == 1 and 'FAIL' in case['row']
              and all(token in case['row'] for token in case['required']))
        passed.append(ok)
        print(name, case['case'], ok, case['exit'], case['row'])
    print(name, sum(passed), len(passed),
          sum(c['exit'] == 1 for c in data['exact_set']['cases']),
          data['revision'])
```

Observed:

| Case | Before complete owning-row diagnostics | After complete owning-row diagnostics |
|---|---|---|
| extra-local | false; exit 0, local inventory PASS | true; exit 1, `FAIL extra: extra.conf` |
| replace-local | false; exit 1, only `missing: xdph.conf` | true; exit 1, `FAIL missing: xdph.conf extra: extra.conf` |
| replace-source | false; exit 1, source resolver PASS | true; exit 1, `FAIL missing: ~/.config/hypr/ai-usage.conf extra: ~/.config/hypr/replacement.conf` |
| missing-gkeep | false; exit 1, local inventory PASS | true; exit 1, `FAIL missing: gkeep.conf` |

Tally **0/4 → 4/4**, matching the explicitly row-specific rubric; overall failing runs **3/4 → 4/4**, not zero baseline detection. The old include-order and source-target rows already detected source substitution and missing gkeep. No claim of +10 whole-domain operability or automatic admission follows from this finite subset. The committed record does not independently establish the wall-clock order of rubric clarification versus measurement; both first land in `95cbc41`.

Own `git show <A>:<path>` SHA-256 comparisons verified all four `committed-bindings.json` entries and both frozen input pins:

```text
tools/mado-verify.sh / frozen/gate.sh
  037b05dcd3f86e12e1b89ee5631f76ce95301b7c411957fad17ff0d7438a6569
frozen/harness.sh
  75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5
w1/globals.json
  ced47240c2a1941bbbf1f125d9a1e41624cfeeb8218ab2a3a425eb335a08a949
frozen/verify.py
  094bf3a494734e784b9a242e076e5c4f51dd71b355476ed071194a8606ee7591
w1/reports/MistakeFix.py
  a3a1559bcd8d5577578c3ee5b35b14d32049ec809c53df4989d08431f561c89e
```

Paths above other than `tools/` resolve under `.ufo/waves/round-13/`. Gate registry exists at `SKILL.md:411-433`, with owner, modes, verdict mapping, self-invocations, pins and scope. Committed evidence reviewed, **not re-executed**:

| Evidence under round-13/evidence | Observed committed result |
|---|---|
| gate-selftest.txt | 310/310 assertions; exit 0 |
| gate-file-plane.txt | 29 PASS, 0 FAIL, 0 UNKNOWN, 8 SKIP, 4 NOTE; CLEAN; exit 0 |
| regression-recut.txt + historical-results.tsv | 10/10 KILLED, control GREEN, restore OK; exit 0 |
| covering-mutants.txt + covering-results.tsv | 8/8 KILLED, control GREEN, restore OK; exit 0 |
| frozen-regression.txt | both input digests verified before execution; historical table match 10/10, flips 0; `MADO_REGRESSION: PASS`, `frozen_match`; exit 0 |
| frozen-selftest-corrected.txt | 12/12; exit 0; original crashing invocation retained separately |
| collision-selftest.txt | 25/25; exit 0 |
| collision-red-corrected.txt / collision-green-corrected.txt | actual historical S017/S030 pair rejects with exit 1; corrected registry exits 0 |

Evidence reviewer independently recovered the derived mutation target `87910c39…` by excising documented blocks, recovered unchanged historical spec `c7ee75b9…`, counted 10 and 8 KILLED rows, and confirmed all mutation anchors exist. Mutation coverage applies to that **derived executable**, not the excised regression/selftest machinery. The frozen companion pins its two executable inputs before comparison; its expected file is protected by committed history, not a circular self-hash.

## Per-axis and trend rulings

| Axis | Verdict | Evidence and boundary |
|---|---|---|
| coverage | improved | Source-joined U-items 3/7 → 4/7; substantive bounded U4 entry; navigation complete |
| operability | improved | Owning-row named-set diagnostics 0/4 → 4/4; committed selftests/regression/covering evidence; ordering and target existence preserved by inspection |
| freshness | unchanged | Committed current file-plane 29/29 PASS; no new full-live claim or revision-to-revision output-equivalence claim admitted |
| calibration | unchanged | No third axis claim; criterion 17's grounded learning is assessed below; citation-count growth is not itself judgment quality |
| depth | unchanged | Unscored; no claimed move or observed regression |
| adjacency | unchanged | Kernel/input-device and DRM diagnosis remain tsukuroi-owned; secrets remain kagi-owned; no configuration or sibling implementation absorbed |

- **Expansion improved:** one new admitted U4 entry cites six reciprocal mined rows on previously uncovered coverage-map ground. The independent count, body inspection and source reopens agree.
- **Quality improved, bounded:** stronger named-set instrument; append-only source-authority corrections/current receipts; no admitted factual feature claim shown false or stale and left unmarked. Gate kill tallies support the instrument only within their documented derived-target scope. Known directory-target, general-parser, toggle-glob, theme-mutation and full-live gaps are not closed here.
- **Discernment improved, narrowly:** this outside spot-check agrees on both an admit and rejects below. Independently, prior-round outside S030 disagreement becomes M1 plus QUALITY criterion 17 and a real historical red/current-green screen. This completes that prior learning; it is not a second new discovery merely because the same S030 correction appears twice.

## Outside discernment spot-check and newly written source quotes

Sources reopened on 2026-10-20 by this integrator; no Wayland diagnostic or feature exercise was run.

| Item | Lane decision | Reopened source | Outside ruling | Reason |
|---|---|---|---|---|
| U4 wayland-protocol-boundaries-r13.md | admit | [Pinned phase README](https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/3dac056d83ad8947eed6eb621f346e91da736efd/README.md), [S040 governance](https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/35d9638cf0c3f0bbf0c42996580a284f3d8ce564/GOVERNANCE.md), [S042 tool purpose](https://wayland.freedesktop.org/extras.html), installed `/usr/share/wayland/wayland.xml:117-178`, committed S041 JSON | agree | Distinguishes upstream phase, client-specific registry advertisement/bind and untested end-to-end behavior. Metadata wording debt below does not assert working HDR/output behavior. |
| Staging is a frozen stable API | reject | Same pinned README, Protocol phases / staging disclaimer / backward-incompatible changes | agree | Compatible additions can bump interface versions; incompatible changes require a new protocol major version. Staging is not immutable API. |
| Advertised output/colour manager proves HDR or output control works | reject | Installed core registry specification; S041 JSON; [Wayland debugging extras](https://wayland.freedesktop.org/extras.html) | agree | Registry discovery and diagnostic detail queries are not the intended feature's behavioral result. |
| S045 correction of distinct S030 admission | reject | [Current Window Rules](https://wiki.hypr.land/Configuring/Basics/Window-Rules/), plus registry S017/S030/S045 | agree | Same current page and overlapping syntax scope, not independent current-wiki evidence. A distinct pinned scope needs human justification. |

New-row quote checks: S040 §2.1.1 exactly contains “Experimental protocols begin with the \"xx\" namespace and do not include any relation to namespaces specified in section 2.1.” (**19 whitespace-delimited words**). S042 §Compositor features exactly contains “Running wayland-info will list all global interfaces advertized by the compositor.” (**11 words**, tool name styled in source). S045 introductory Note contains “Since Hyprland 0.55, hyprlang is deprecated in favor of lua.” (**10 words**); modified date remains 2026-08-26. All are within 25 words and ground their respective teaches cells.

Own S041 JSON recount: **72 globals / 71 interfaces**; `wl_compositor` version **6**. Own installed-source check: `sha256sum /usr/share/wayland/wayland.xml` gives `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07`; `pacman -Q wayland wayland-utils` gives **1.26.0-1 / 1.3.0-1**, matching the entry.

The required maintained census was run by this integrator:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
```

Observed exit **0**, `mado ok`; W04 warnings for S030, S042 and S045 duplicate URLs. Rejected/superseding history is retained rather than hidden. A warning-free registry is not claimed.

S046 anchor audit caution: the text reader transformed upstream source bytes and shifted displayed offsets. The reviewer re-fetched raw bytes and withdrew its initial offset finding: raw SHA-256 `fcdc6c09d8111c8bcec407299be9ef582105c8ff954ebf9b57fa25b5e86c46a6`, 88,132 bytes, detail calls at 1775/2031/2626/2744/2750, matching the registry. No anchor defect is routed on the transformed reader output. Tool discrepancy reported through `xd://report_issue`.

## Routed defects and retained limits

Route to **mado next round**, append-only corrections to existing filed knowledge/report statements:

1. **R13-V1, retained-data wording:** U4's “retained S041 data is only registry interface/version headers” is too broad. `globals.json` also retains sanitized package/probe/compositor metadata and the socket name; U4's following paragraph already acknowledges session correlation. Clarify “global records contain interface/version only; sanitized probe/session metadata is also retained.” This is a narrow internal wording inconsistency, not evidence of retained raw device/output identity, a false behavioral capability or owned-axis harm.
2. **R13-V2, evidence precision:** distinguish config boundary unchanged within one file-plane run (`gate-file-plane.txt:47`) from byte-identical *outputs across before/after revisions*. Only the former has a committed boundary receipt here. Do not use the report's ambiguous “byte-identical before/after” to infer the latter. Preserve the legitimate 29 PASS / 0 FAIL / 0 UNKNOWN result.
3. **R13-V3, direct selftest provenance:** future standalone selftest receipts should carry the measured gate revision/digest. `gate-selftest.txt` lacks its own revision header; the current binding is recovered from the report, content commit and `committed-bindings.json`, so this is status-neutral provenance debt, not a fabricated fresh run or failed C2 measurement.

Not defects requiring new scope: the strict row-specific metric is explicitly bounded; no alternative metric is substituted. A supersedes link is not automatic archival status for S006, and future mining of the historical row still needs human review. Broad `# hyprlang` refusal is deliberate fail-closed behavior; arbitrary grammar is not claimed. gkeep remains an observed baseline member, not an operator permanence ruling; the inherited L0 intent question remains unresolved. No new L0 question was created.

The fixed raw-scratch disclosure is retained as a real in-round incident, not rewritten into a clean initial capture. No retained axis harm was found. SHONEN remains four author assertions: this closure is not a complete promotion review and does not declare all boxes independently clear. Promotion/mint decisions remain operator-owned.

Tool installations by this verifier/review seats: **none**. Lane installation verified from its record and installed package: **wayland-utils 1.3.0-1**, pacman extra, for the assigned `wayland-info` diagnostic; no system upgrade claimed. No lane-authored file, SHONEN mark, driver state, sibling repo or external configuration was edited by this closure.
