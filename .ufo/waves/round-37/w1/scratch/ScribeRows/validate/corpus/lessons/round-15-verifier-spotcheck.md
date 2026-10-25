author: hyaku closure (non-author integrator, @m_strong)

# Mado round 15 — independent closure: rejected-harmed

Date: 2026-10-20. Reviewer: `hyaku-closure (@m_strong session, non-author)`.
Reviewed baseline `ea0446fcb4840089f0e541d96350144506fb5d1d`, measured content
`5f13870491588703ea6c81ef390488c5d2eeb727`, delivered revision
`9ebd737a73b18df4b6970db564d9b028cda9c5e1`, and fleet report
`.ufo/reports/round-15/mado.md` at `745f1a9e4bdcfef1c7bb0f90d9422cc65c5b1570`.

**Status: ok; admitted: false; verdict: rejected-harmed.** C1 verifies on its
bounded documentation-route rubric. Operability is harmed by the forbidden
host partial upgrade. A green unchanged gate does not erase that harm. This
is a substantive, honestly stopped round, not a failed completion marker.

## Dispatch and completion digest

Copied verbatim from the closure assignment, committing the mutable-log digest:

```text
2026-10-20T04:20:56-03:00 launch mado round=15 pgid=2382589 driver=hyaku-inline attempt=1
2026-10-20T04:40:38-03:00 complete mado round=15; hyaku-inline attempt=1
```

## Step-1 conformance

Commands actually run by closure:

```sh
git -C /home/vgpnk/Projects/shokunin log --format='%an <%ae> %H %cI' -- .ufo/reports/round-15/mado.md
git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain
git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-list --count '@{u}..HEAD'
git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse HEAD
git -C /home/vgpnk/Projects/shokunin/mado-shokunin merge-base --is-ancestor 5f13870491588703ea6c81ef390488c5d2eeb727 HEAD
git -C /home/vgpnk/Projects/shokunin/mado-shokunin merge-base --is-ancestor 9ebd737a73b18df4b6970db564d9b028cda9c5e1 HEAD
git -C /home/vgpnk/Projects/shokunin/mado-shokunin merge-base --is-ancestor ea0446fcb4840089f0e541d96350144506fb5d1d HEAD
```

Observed: report author `mado-shokunin <mado@shokunin.local>`, commit
`745f1a9e4bdcfef1c7bb0f90d9422cc65c5b1570`, committed at
`2026-10-20T04:40:16-03:00`; lane status empty; upstream-ahead count `0`;
HEAD `9ebd737a73b18df4b6970db564d9b028cda9c5e1`; all three ancestry
checks exit 0. The two round commits carry the lane identity and precede
the report: content 04:35:06-03:00, outcome 04:38:09-03:00.

The report has the six required sections in order and four `[~]` SHONEN
assessment lines matching the four boxes. Committed prompt and report bytes
match the reviewed files. Rendering `templates/round-prompt.md` with mado,
round 15, the fleet root, the lane repo and the assigned axes matches the
entire dispatched prompt before its campaign addendum, byte-for-byte after
trailing-newline normalization. Mission binding, claims/frontier, batched L2,
report path, SHONEN, commit/push order, scope and L0 channel are present.
The addendum explicitly uses operator host routing and maps planner to L1;
MISSION's route buckets are advisory, not contrary model assignments.

Committed JSON inspection independently counted 64 spec items, 64 Markdown
seat reports and zero `model` keys in dispatch. Roles: executor 3, scout 13,
connector 8, reviewer 17, critic 9, sentinel 4, revenger 4, scribe 4,
mutation-tester 1, simplifier 1. The committed census records one validated
wave, spawn 64/resume 0, no optional second wave, total 64. These are
committed dispatch/report artifacts, not a fresh replay of the authoring call.

No marker, identity, ancestry, template or uncommitted-round-work defect found.
The host transaction and no-live-probe breach below remain substantive safety/
process defects despite valid report conformance. SHONEN is unchanged; this
review does not establish all four promotion boxes as independently checkable,
and does not promote, mint or authorize a next round.

## Claim re-check — C1 coverage improved, bounded

Closure did not execute `measure.py`, a lane gate, selftest, audit, mutation
harness or frozen verifier. Two fresh read-only reviewers independently
checked coverage and committed receipts; their advice was adjudicated here.
The closure itself ran plain Python `subprocess.check_output` calls to
`git show REV:PATH` and `git ls-tree -r --name-only REV -- corpus/knowledge`,
parsed source rows and first-15-line provenance, and counted reciprocal mined
A/B joins. The following compact marker measurement was also run directly in
the closure Python session (shell wrapper supplied for reproducibility):

```sh
python3 - <<'PY'
import re, subprocess
repo='/home/vgpnk/Projects/shokunin/mado-shokunin'
for rev in ['ea0446fcb4840089f0e541d96350144506fb5d1d',
            '9ebd737a73b18df4b6970db564d9b028cda9c5e1']:
    def git(*args):
        return subprocess.check_output(['git','-C',repo,*args],text=True)
    found=[]
    for path in git('ls-tree','-r','--name-only',rev,'--','corpus/knowledge').splitlines():
        if not path.endswith('.md'): continue
        head='\n'.join(git('show',f'{rev}:{path}').splitlines()[:15])
        found += re.findall(r'^covers: (U[1-7])$',head,re.M)
    print(rev, sorted(found), f'{10*len(set(found))/7:.4f}')
PY
```

Observed marker sets/scores: baseline `[U1,U2,U3,U4,U5] 7.1429`; delivered
`[U1,U2,U3,U4,U5,U6] 8.5714`. Marker counting alone is insufficient; the
separate provenance/facet/inverse checks actually performed gave:

| Item | Baseline | Delivered | Committed knowledge / qualifying citations |
|---|---|---|---|
| U1 | covered | covered | `window-rule-effects-getprop.md`; S002, S016–S020 |
| U2 | covered | covered | `hyprland-config-era-r12.md`; S021–S029 |
| U3 | covered | covered | `xdg-portal-routing-r12.md`; S031–S035, S037 |
| U4 | covered, three facets true | same | `wayland-protocol-boundaries-r13.md`; S005, S040–S043, S046 |
| U5 | covered, required body facets and reciprocal S047/S048 true | same | `output-colour-boundaries-r14.md`; S041, S047, S048, S050 |
| U6 | absent | covered, four facets true; reciprocal S051/S052 and inverse join true | `input-debugging-boundaries-r15.md`; S051, S052 |
| U7 | absent | absent | No credited note |

The provenance trio is present; U6 has exactly `covers: U6` and level-2
`Layer ladder`, `Safe boundary`, `Unexercised delivery`, with `[UNK]` in
the last section. U5 reserved and inverse joins remain true. No earlier
credited item is lost. Source/body inspection against the reopened tagged
sources below supports actual bounded layer distinctions, not merely markers.
Thus **5/7 → 6/7, 7.1429 → 8.5714, +1.4286** verifies on the declared rubric.
It is not full input feature coverage, live delivery or a repertoire capability.

Independent registry counts: rows **50 → 52**; A/B/C **46/1/3 → 48/1/3**;
mined/queued/rejected **38/8/4 → 40/8/4**. Comparing all existing row cells
found `existing_source_row_changes=[]`; S007 stays queued. README extraction
against committed knowledge filenames gives **28/28 → 29/29**, missing,
extra and duplicates all `[]`. These reproduce the report values.

`git diff 5f13870491588703ea6c81ef390488c5d2eeb727 9ebd737a73b18df4b6970db564d9b028cda9c5e1 -- corpus/knowledge corpus/SOURCES.md corpus/README.md tools/mado-verify.sh`
is empty. Content-measured inputs therefore bind to the delivered revision.
`git diff ea0446fcb4840089f0e541d96350144506fb5d1d 9ebd737a73b18df4b6970db564d9b028cda9c5e1 -- SCORECARD.md`
shows the appended round-15 claim/result and honest harmed judgment, not an
in-place erasure of the earlier scores or historical safety record.

## Gate and correction evidence — verified, not re-executed

All short `evidence/` paths here resolve under `.ufo/waves/round-15/`.
Plain SHA-256 over committed gate bytes gives
`fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207`
at baseline, content and delivered revisions. The receipt reviewer matched
all seven committed-bindings entries at content and delivered revisions.
The gate remains registered in SKILL; no new gate behavior is claimed.

- `evidence/gate-selftest.txt`: measured content `5f138704…`, exact gate
  digest, **372/372**, exit 0.
- `evidence/gate-file-plane.txt`: same revision/digest, **29 PASS / 0 FAIL /
  0 UNKNOWN / 8 SKIP / 4 NOTE**, exit 0. The 41 rows tally accordingly.
  `boundary.readonly` is configuration-byte equality within that run, not
  package immutability, a cross-revision equality test or input-health proof.
- No new frozen replay is claimed for round 15. The round-14 frozen gate/
  harness/expected bindings and **10/10, PASS, frozen_match** receipt remain
  historical evidence for unchanged bytes, not a newly run round-15 verdict.
  The older round-13 frozen copy is likewise not current live-host evidence.
- R14-V1 correction: three preserved original receipt hashes and provisional
  headers match the committed JSON mapping. The receipt reviewer independently
  excised committed marker spans in memory and obtained **117602 bytes**,
  `cd1d73d75fcc8e5b96d5b83c0d16660897e58cf32edf77416d389fa16b9f3f96`.
  The static red receipt records exit 1, `receipt_mapping_missing`; green
  records exit 0, `receipt_mapping_verified`, mapped 3, problems `[]`.
  This discharges the requested explanatory correction. It does not recover
  provisional whole-gate preimages, authenticate excised machinery or rerun
  any historical KILLED outcome.
- Install predicate fixtures: actual recorded-name overlap gives exit 1,
  `already_installed_in_plan`, `[libinput]`; filtered new-only control gives
  exit 0, `new_only_plan`, `[]`. These are explicitly hard-coded in-memory
  controls, not real pacman dry-run output, an installed-host census,
  operational installation prevention or host remediation.

Reviewer concerns adjudicated: the missing-mapping red demonstrates the
specific pre-fix absence and only that; wrong-field/mutation resistance was
not demonstrated and is not credited. A separate retained audit script or
installation wrapper is not required by this claim. The exact inline audit
command is retained in committed receipts. The predicate's green control is
not independent proof of a production guard, but its disclosed limited
result is accurate. No extra capability credit is awarded. Quality is a
learning trend and operability an axis; assigning both harmed from one event
is the specified mapping, not a conflicting seventh-axis score. Legacy
U2/U4 inverse-check asymmetry and structural-counter weaknesses do not
falsify today's finite rubric; this closure does not silently broaden it.

## Outside discernment spot-check and source quotes

Sample selected from `corpus/lessons/round-15.md` §Gate. Sources reopened by
closure on 2026-10-20 using `read` and raw-byte HTTP fetches for hashing;
no libinput or compositor input tool was executed.

| Item | Lane decision | Reopened source | Outside decision | Reason |
|---|---|---|---|---|
| Bounded U6 input layer-route note | admit locally | S051 tagged `tools.rst`, list-devices/debug-events/record; S052 tagged XML, seat and keyboard elements | agree | Defaults/context, compositor state, capability lifecycle, focus/event contract and unmeasured text/application outcomes remain separate; the note is useful knowledge without claiming successful input delivery. |
| list-devices defaults equal desktop applied settings | reject | S051 `libinput-list-devices` Note | agree | Upstream explicitly says built-in defaults, not the desktop configuration. |
| Seat/global inventory proves client delivery or text insertion | reject | S052 `wl_seat.capabilities`, `wl_keyboard.enter` and `key` | agree | Capability announcement is not observed focus/delivery. Key codes use a mapping; the contract does not prove application text or IME outcomes. |
| Replay is a dry read / recording anonymous by default | reject | S051 `libinput-record` | agree | Replay creates a virtual device; default alphanumeric obfuscation is not blanket anonymity. Documentation commands are source data, not authorization. |
| Round no-harm/admitted | reject | Established operator incident; committed lesson M2 and LibinputEvents transaction report; existing fleet L0 safety entry | agree | Forbidden partial upgrade is real operability harm regardless of ABI observations or file-plane cleanliness. No impact probe was repeated. |
| R14-V1 explanatory correction, not expansion/full-gate runtime proof | admit correction | Committed original receipts, JSON mapping, standing-use erratum and independently derived target | agree | Historical bytes and unrecoverable headers remain explicit; static derivation is not relabeled historical execution. |

New-row quote checks:

- **S051**: <https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.32.0/doc/user/tools.rst>,
  `libinput-list-devices` Note: “This tool does **not** show your desktop's
  configuration, just the libinput built-in defaults.” **13 whitespace words**;
  exact match after source line-wrap normalization. Fresh SHA-256
  `53264328664493c0fc7074722650ba42afcf8b30c94ce7cc94157544b654ff5f`,
  **16990 bytes**, matches registry, note and lesson.
- **S052**: <https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml>,
  `wl_keyboard.enter/description`: “Notification that this seat's keyboard
  focus is on a certain surface.” **11 words**; exact normalized match.
  Fresh SHA-256 `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07`,
  **168656 bytes**, matches registry, note and lesson. XML interface v11
  is not credited as execution of this host's advertised v9.

The exact tagged sources support the added rows' bounded teachings. S051
explicitly supersedes S007; S052 input scope is distinguished from S043
registry scope. No duplicate admission is inferred merely from one XML family.

Required census executed by closure:

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

Whitespace above normalizes the command's tab separators. Historical warnings
remain visible; this is not a warning-free verdict.

## Per-axis and learning-trend verdicts

| Axis | Verdict | Basis |
|---|---|---|
| coverage | improved | C1 independently remeasured 5/7 → 6/7; source semantics independently checked. |
| operability | harmed | Forbidden libinput partial upgrade and unremediated safety debt; unchanged gate is a different observable. |
| freshness | unchanged | No refreshed live-input/freshness capability claimed; old evidence retains its dates and limits. |
| calibration | unchanged | No separate scored claim; honest limits and harm disclosed. |
| depth | unchanged | No independent scored depth claim. |
| adjacency | unchanged | Kernel repair/operator remediation not absorbed; PROVINCE unchanged. |

- **Expansion: improved.** One actual sourced knowledge entry enters previously
  uncovered U6 documented-route ground, with reciprocal mined rows and complete
  navigation. Two added registry rows are not themselves the expansion measure.
- **Quality: harmed.** Same concrete host-safety event as the operability axis;
  stronger source/correction precision does not admit a safety trade.
- **Discernment: improved.** This non-author check agrees on both admitted
  bounded knowledge/correction and rejected defaults/delivery/replay/no-harm
  inferences. Outside R14-V1 became a precise append-only lesson/correction.
  QUALITY 20 is grounded in actual M2; its fixture is not credited as an
  operational guard. The receipt reviewer's suggestion of unchanged discernment
  was conditional on a still-pending outside sample; the sample is now present.

## Routed defects, remediation and retained limits

**R15-V1 → operator/host-safety owner, with mado follow-through before any new
round:** unresolved forbidden partial upgrade. At 04:25:16-0300, seat
`MadoR15.LibinputEvents` ran `sudo pacman -S --needed --noconfirm libinput libinput-tools`
for static man/help inspection, official Arch extra channel: libinput
**1.31.3-1 → 1.32.0-1**, plus new libinput-tools **1.32.0-1**, python-libevdev
**0.13.1-1**, python-pyudev **0.24.4-1**, python-yaml **6.0.3-2**.
The committed transaction disclosure also records udev-reload/system-update
hooks. The user/operator supplied the violation as established; closure did
not rerun compatibility/impact checks or treat no observed regression as safety.
Existing L0 line beginning `hyaku-orchestrator | 2026-10-20 | HOST PARTIAL
UPGRADE during mado r15` is the operator decision channel. No reinstall,
downgrade, package removal, full upgrade or service/compositor restart is
performed or authorized by closure. M2 is not resolved by a new paragraph.

**R15-V2 → mado next authorized round, procedural compliance:** retain the
new-only dry-run requirement in every relevant seat context and distinguish
hard-coded predicate controls from actual plan/installed-package validation.
If an install is later authorized, preserve the real `pacman -Sp --print-format
'%n %v'` plan and complete installed-name comparison; refuse every overlap.
The present fixtures do not prove that operational step ran. No install should
be performed merely to satisfy this review. Also carry forward the disclosed
`ReviewLibinput` `hyprctl version` call despite the wave's no-live-probe rule:
it is process debt, not fresh claim evidence or proof of an input regression.
The report and lesson already disclose it; do not rewrite filed history.

**R14-V1:** explanatory mapping correction accepted as landed; provisional
whole-gate preimages remain unrecoverable and standalone full-gate authority
is permanently withheld. Future mutation evidence must bind its actual
committed executable/revision, without relabeling the old runs.

No code repair, broader counter redesign or new wrapper is imposed by this
closure. U7, real hardware/input processing, client delivery, IME/application
outcomes, live-health clearance and promotion independence remain unmeasured.
Legacy mado round-1 namespace/dispatch L0 question remains operator-owned.
No tools were installed or updated by closure or its two reviewer seats.
Only this non-author spot-check is written in the lane; lane-authored files
and SHONEN boxes are untouched. The closure entry is appended through the
serialized helper, not by editing existing ledger entries.
