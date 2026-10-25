author: hyaku closure (non-author integrator, @m_strong)

# Round 14 — independent verification and discernment spot-check

Date: 2026-10-20. Status **ok**; **admitted**. This closure did not author the round, execute a lane gate, or alter lane-authored records or SHONEN marks.

Baseline: `873ff081b2ac363df771261b0ed950cba50d8988`.
Delivered lane revision: `97c35835da3702df2f397d5c70ac6b1d871f012d`.
Measured content: `32118fc1014837b3a385c7a66abbdc59b1560835`.
Fleet report: `.ufo/reports/round-14/mado.md`, committed by mado in `b24129da2f9808bbc53c1388b917477a1ac25f58`.

## Step-1 conformance

Commands actually run:

```sh
git -C /home/vgpnk/Projects/shokunin log --format='%an %H' -1 -- .ufo/reports/round-14/mado.md
git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain
git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-list --count '@{u}..HEAD'
git -C /home/vgpnk/Projects/shokunin/mado-shokunin merge-base --is-ancestor 873ff081b2ac363df771261b0ed950cba50d8988 HEAD
git -C /home/vgpnk/Projects/shokunin/mado-shokunin merge-base --is-ancestor 32118fc1014837b3a385c7a66abbdc59b1560835 HEAD
git -C /home/vgpnk/Projects/shokunin/mado-shokunin merge-base --is-ancestor 97c35835da3702df2f397d5c70ac6b1d871f012d HEAD
git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff 873ff081b2ac363df771261b0ed950cba50d8988 97c35835da3702df2f397d5c70ac6b1d871f012d -- SCORECARD.md
```

Observed: report author `mado-shokunin`; worktree output empty; ahead count **0**; all ancestry exits **0**. Both lane commits carry `mado-shokunin <mado@shokunin.local>` and precede the report (content 06:03:28Z, outcome 06:10:29Z, report 06:13:12Z). SCORECARD adds 141 lines without removing prior records. The report has all six required sections, substantial checkable work, and four `[~]` lines under `## SHONEN`, matching the four checklist boxes. It is not a marker.

The canonical `kimi-shokunin/templates/round-prompt.md` was rendered in memory with mado/14/fleet-root/axes/cwd substitutions and compared, whitespace-normalized, to the dispatched prompt prefix before campaign §6: **canonical_template_normalized_equal True**. The prompt is committed (`c49b20048d8c9219a61a5ebf05e13bb5728152c7`). Required mission, claim, frontier, L2, report, commit/push, write-scope and L0 contracts remain present; campaign mechanics expressly map the planner to L1 and leave role models operator-owned.

Plain JSON inspection of committed `w1/dispatch.json` gives **spawn=32, resume=0, total=32**; role counts executor=3, scout=8, connector=4, reviewer=6, critic=4, sentinel=2, scribe=2, revenger=2, mutation-tester=1; no task model parameters, and tooling RULES.md is in the context. This verifies recorded dispatch evidence, not a reconstruction of runtime scheduling.

Durable dispatch/completion digest, copied verbatim from the closure assignment:

```text
2026-10-20T02:37:48-03:00 launch mado round=14 pgid=1521146 driver=hyaku-inline attempt=1
2026-10-20T03:13:33-03:00 complete mado round=14; hyaku-inline attempt=1
```

The elapsed time exceeds two ticks but mado-authored commits establish progressing work, not silence. This closure opens no new lane mission.

History pin was checked as plain committed JSON, without running the closure gate: `sha256(json.dumps(rounds[:48],sort_keys=True,separators=(',',':')).encode())` is `ce97497ed699a8f0939be062d042cf4d6e3e7531116fbe4681593991d67f0a8e` at both fleet HEAD and anchor `ae19fca`, matching the committed pin; anchor ancestry exit **0**. No history pin was changed.

## Claims — re-measured versus evidence-verified

No lane gate, mutation harness, selftest, frozen verifier or `measure.py` was executed. Two fresh read-only reviewer seats audited coverage/source semantics and committed gate evidence. Their recommendations were independently adjudicated here; neither seat authored the round. All short `evidence/`, `frozen/` and `w1/` paths below resolve under `.ufo/waves/round-14/`.

### C1 coverage — improved; independently re-measured

The independent counting recipe actually run through Python Eval uses git only as a committed-byte reader:

```python
import subprocess, re, collections
R = '/home/vgpnk/Projects/shokunin/mado-shokunin'
B = '873ff081b2ac363df771261b0ed950cba50d8988'
A = '97c35835da3702df2f397d5c70ac6b1d871f012d'
def blob(rev, path):
    return subprocess.check_output(['git','-C',R,'show',rev+':'+path]).decode()
for rev in (B, A):
    rows = {}
    for line in blob(rev, 'corpus/SOURCES.md').splitlines():
        c = [v.strip() for v in line.split('|')[1:-1]]
        if c and re.fullmatch(r'S\d{3,}', c[0]): rows[c[0]] = c
    covered = []
    paths = subprocess.check_output(['git','-C',R,'ls-tree','-r',
             '--name-only',rev,'corpus/knowledge/']).decode().splitlines()
    for path in paths:
        text = blob(rev, path)
        cov = re.findall(r'^covers:\s*(U[1-7])\s*$', text, re.M)
        src = re.search(r'^source:\s*(.*)$', text, re.M)
        ids = re.findall(r'\bS\d{3,}\b', src.group(1)) if src else []
        joined = [s for s in ids if s in rows and rows[s][7]=='mined'
                  and path in rows[s][10]]
        if len(cov)==1 and joined: covered += cov
    print(rev, sorted(set(covered)), len(set(covered)),
          round(10*len(set(covered))/7,4), len(rows))
    print(collections.Counter(r[3] for r in rows.values()))
    print(collections.Counter(r[7] for r in rows.values()))
```

Observed, reduced without changing values:

```text
873ff081 U1 U2 U3 U4     4/7  5.7143 rows=46 A/B/C=42/1/3 mined/queued/rejected=34/8/4
97c35835 U1 U2 U3 U4 U5  5/7  7.1429 rows=50 A/B/C=46/1/3 mined/queued/rejected=38/8/4
U5 reciprocal mined joins: S047 S048 S041 S050
```

Separate git-byte equality checks show measured-content and delivered copies of `tools/mado-verify.sh`, U5, SOURCES and corpus README are identical. The new note begins with source/verified-at/recheck, has exactly `covers: U5`, and contains the output-management, colour-management and unexercised-feature sections with explicit unknowns. Reopened sources below support the actual bounded note, not just its structural counter. Coverage improves **+1.4286**; one new documented route is admitted, not four entries or complete U5 feature support.

Independent navigation measurement extracted README knowledge rows and compared them with `git ls-tree -r --name-only REV corpus/knowledge/`: **27/27 → 28/28**, missing=[], extra=[], duplicates=[]. Existing-row comparison of the registry found only **S041 column 10 (used-by)** changed; its new U5 backlink is logged old→new in the lesson.

### C2 operability — improved; execution evidence-verified, tally independently re-measured

The committed `evidence/{before,after}.txt` records are bound to baseline and measured content, respectively. I parsed their stdout JSON with `json.JSONDecoder().raw_decode(raw.split('stdout:\n',1)[1])[0]`. For each recorded case, I independently required: owning row contains FAIL; its detail after the PASS/FAIL column equals exactly `non-regular: ` plus affected_path; overall_exit=1; fail_row_ids contains only `hypr.root.sources_resolve`; replica_detail equals the owning row; toggle row matches the declared PASS/NOTE. This re-tally reads actual recorded rows, not the receipt's `detected` boolean, and executes no lane code.

| Case | Baseline row / exit / credit | Delivered row / exit / credit |
|---|---|---|
| direct-directory, default/hypr/windows.conf | PASS / 0 / 0 | FAIL exact `~/.local/share/omarchy/default/hypr/windows.conf` / 1 / 1 |
| all-directory-glob | PASS / 0 / 0 | FAIL exact `~/.local/state/omarchy/toggles/hypr/window-no-gaps.conf` / 1 / 1; toggle NOTE preserved |
| mixed-glob-directory | PASS / 0 / 0 | FAIL exact `~/.local/state/omarchy/toggles/hypr/dir.conf` / 1 / 1; regular sibling not accused |

Observed independent re-tally: **0/3 → 3/3**; selected overall failing runs **0/3 → 3/3**, scores **0.0000 → 10.0000** on this finite source-policy subset only. The isolated direct fixture was chosen before baseline observation; existing ai-usage inventory failure is correctly unscored. Fixture execution itself is evidence-verified, not freshly reproduced by this closure.

Plain `hashlib.sha256(git show REV:tools/mado-verify.sh)` gives `fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207` at both measured and delivered revisions, agreeing with the new selftest, file-plane and frozen receipts. The evidence reviewer independently matched committed-bindings.json, frozen gate/harness/verifier/expected bytes, the derived target `cd1d73d75fcc8e5b96d5b83c0d16660897e58cf32edf77416d389fa16b9f3f96`, and historical spec `c7ee75b97c38ac8f88410165a574ad1cba7f4653bd09d35e6814267a12df1dd8` to committed bytes. Full gate and derived target are intentionally different.

Evidence-verified, not re-executed:

- `gate-selftest.txt`: measured commit and raw gate digest in its own header; **372/372**, exit 0.
- `gate-file-plane.txt`: **29 PASS / 0 FAIL / 0 UNKNOWN / 8 SKIP / 4 NOTE**, exit 0. Its boundary equality is within that run, not across revisions and not live-health proof.
- `frozen-regression.txt`: gate and harness input SHA-256 verified before replay; historical table **10/10**, `MADO_REGRESSION: PASS`, `frozen_match`, exit 0. `frozen-selftest.txt`: **12/12**, exit 0. Frozen expected input hashes and the SKILL gate registry are present.
- `regression-recut.txt`, `regular-target-mutants.txt`, `retained-census-mutants.txt`: **10/10**, **4/4**, **8/8 KILLED**, GREEN controls and restore OK. These bind the documented derived executable; provisional whole-gate header debt is routed below, not silently treated as a measured full-gate run.
- `contract-red.txt` / `contract-green.txt`: the same contract audit records **FAIL detected=0/3, exit 1 → PASS detected=3/3, exit 0**.
- `provenance-red.txt` / `provenance-green.txt`: unchanged old selftest receipt fails for missing measured_commit/gate_sha256, exit 1; new selftest receipt passes, exit 0. No generic execution wrapper shipped.

The resolver review found metadata-only type checks and NUL-delimited expansion, with no dangerous regression demonstrated. Clean/file-symlink/newline-regular, order, missing and zero-match controls retain their declared behavior. Broader filesystem classes and whitespace diagnostic parsing are outside this denominator. This is explicitly the lane's strict supported-source policy, not a claim about Hyprland accepting or rejecting all such sources.

## Per-axis verdicts and no-harm judgment

| Axis | Verdict | Evidence and boundary |
|---|---|---|
| coverage | improved | Independently re-measured sourced U1–U4 → U1–U5, semantic source checks agree. |
| operability | improved | Independently re-tallied committed three-case behavior, revision/digest-bound execution evidence; not whole-domain saturation. |
| freshness | unchanged | New file-plane receipt clean with live SKIPs; no freshness score move claimed. |
| calibration | unchanged | No scored move; explicit limitations and learned outside corrections support discernment instead. |
| depth | unchanged | No separate axis claim; static protocol safety facts remain bounded. |
| adjacency | unchanged | PROVINCE unchanged; no kernel/DRM/hardware diagnosis or cross-domain absorption. |

SCORECARD is append-only in this diff and both lowest-axis coverage and separate operability were addressed. PROVINCE/SHONEN diff is empty. No retained owned-axis harm was found. No exploratory claim or newly entered repertoire capability is asserted.

## Outside discernment spot-check and source quotes

Source files were reopened on 2026-10-20. Installed XML hashes independently computed with `sha256sum` match the pinned S047/S048 source bytes: respectively `65b0f82a6cf129bf1a1c31a2428795abd33886c15ddd5f3ad97e5922d7bdc3a7` and `18a2678e3352c3be3fbeed20005d48852b7235d0d78f08b9c987a0b8e91449f9`. Thus these local opens check the exact XML, not an assumed package/version equivalence. The reviewer additionally fetched the pinned URLs independently.

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| U5 bounded documented output/colour route | admit | `/usr/share/wlr-protocols/unstable/wlr-output-management-unstable-v1.xml:466-498`; `/usr/share/wayland-protocols/staging/color-management/color-management-v1.xml:1692-1710`; pinned [S050](https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/protocols/OutputManagement.cpp) | agree | Contract, static implementation and untested behavior are distinguished; test stub and pre-apply disable scheduling justify mutation-class caution. |
| Successful test guarantees successful apply | reject | S047 XML test, lines 481–487; [pinned source](https://gitlab.freedesktop.org/wlroots/wlr-protocols/-/raw/a741f0ac5d655338a5100fc34bc8cec87d237346/unstable/wlr-output-management-unstable-v1.xml) | agree | Exact contract expressly allows later apply to fail. |
| Apply success guarantees every requested property | reject | Same XML apply, lines 466–473 | agree | Successful apply need not completely match the request; fractional-scale rounding is named. |
| Advertised manager / target luminance proves physical HDR accuracy | reject | S048 target_luminance lines 1692–1702 and committed S041 capture | agree | Theoretical target metadata and historical registry records are not physical measurement or exercised feature behavior. |
| S049 retained-data correction | admit as correction | `.ufo/waves/round-13/w1/globals.json:1-33`, global record bodies, and appended U4 erratum | agree | Globals contain interface/version while top-level probe/tool/compositor/session metadata also exists. Corrects scope without retracting observer-binding evidence. |

New-row quote checks against reopened sources: **S047 13 words**, “Even if the compositor succeeds to test a configuration, applying it may fail.”; **S048 20 words**, “This luminance range is only theoretical and may not correspond to the luminance of light emitted on an actual display.”; **S049 2 whitespace-delimited tokens**, `"display_socket": "wayland-1"`; **S050 9 words**, `TODO: STUB: applyTestConfiguration for test not implemented, returning true.` All are within 25 words, correctly located and grounded in the named scope. Source/body semantics were checked independently of coverage counters.

Required maintained census actually run:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
```

Observed exit **0**:

```text
mado W04 S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado W04 S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado W04 S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado ok /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
```

Output tabs are rendered as spaces above. Rejected/superseding historical warnings remain visible; no warning-free claim is made. Round frontier corpus verdict: **conformant**, with standalone ancillary receipt precision debt below.

## Learning-trend verdicts

- **Expansion: improved.** One actual new U5 knowledge entry on previously uncovered current-art ground, reciprocal mined citations and complete index; 4/7 → 5/7. S049 is correction, not expansion.
- **Quality: improved, bounded.** Stronger exact-source type policy, preserved controls, hash-pinned frozen evidence and explicitly safer static protocol-use boundary. Prior retained-data/equality wording is marked by appended corrections rather than left silently false. Ancillary receipt debt does not contradict the measured claim or derived-target evidence.
- **Discernment: improved.** This non-author spot-check agrees on admitted bounded knowledge/correction and rejected test/apply/HDR inferences. Prior R13-V1..V3 became lesson-backed QUALITY 19 and corrections/red-green provenance controls; QUALITY 18 is grounded in M4. No current outside agreement is inferred from authoring-wave seats.

## Routed defects and retained limits

**R14-V1 → mado next round, standalone ancillary receipt precision:** `evidence/{regression-recut,regular-target-mutants,retained-census-mutants}.txt:3-4` retain `input_binding: provisional worktree snapshot`, old whole-gate hashes (`ef50e262…` or `d6d5eb27…`) and no measured_commit header. Their `MUTATE_TARGET` and GREEN/restore lines bind the exact derived target `cd1d73d7…`, independently derivable from committed content, and the filed report explicitly excludes excised machinery. Therefore kill counts and C2 are verifiable, but these must not be read as standalone final-full-gate receipts. Append an explanatory correction mapping each provisional header to its committed derived target; keep historical bytes, and bind future standalone mutation receipts directly. Route is status-neutral; admission does not require rewriting these records.

Reviewer suggestions adjudicated, not silently adopted as extra acceptance criteria: direct symlink-to-directory/FIFO/socket behavior, glob dangling-link classification and missing mutation cases are broader type-policy disclosures/coverage limits, not a demonstrated counterexample to the explicitly finite three-case claim. The report already requires every direct/glob target to be regular and distinguishes lane policy from Hyprland behavior. Likewise S050 deferred apply success/cancelled-path analysis is outside the specifically opened callback/stub facts and unclaimed feature execution; no new implementation-coverage claim is invented. Retain these bounds if expanding that scope later.

R13-V1..V3 are resolved by the appended U4/S049 retained-data clarification, standing-use/LOG within-run equality correction, and self-contained new selftest receipt with red/green header evidence. The legacy mado round-1 L0 question remains operator-owned; no new question is created here.

SHONEN remains four author assertions. This closure does not establish all promotion boxes as independently checkable: historical end-to-end and no-oral-context evidence is not freshly executed promotion review. No promotion/mint, SHONEN edit or new capability-table entry is made.

Tool installs/updates by this closure and its reviewer seats: **none**. The lane's recorded install is **wlr-protocols r112.a741f0a-1**, official pacman extra, to inspect owning XML; download-only cache work is not another install. No upgrade or compositor/configuration mutation was performed by this closure.
