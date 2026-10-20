# Round 14 — output/colour boundaries and regular source targets

Date: 2026-10-20. Baseline `873ff081b2ac363df771261b0ed950cba50d8988`.
Declared claims: C1 coverage, sourced U1–U4 → U1–U5; C2 operability,
three directory-shaped source targets acquire owning-row named failures.
`SCORECARD.md` §Round 14 declares the rubric before measurements.
Each claim is independently verifiable; source knowledge does not depend
on the resolver fix. No exploratory claim or promotion clearance.

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M1 | scope / retained-data wording | Outside R13-V1, `round-13-verifier-spotcheck.md`; U4 §Advertisement says all retained S041 data is headers, although top-level metadata is retained | QUALITY 3; no field-specific retention criterion before this round | Append U4 erratum: global records are interface/version only, sanitized probe/session metadata also remains. S049 supersedes the same broad retention phrase in immutable S046, preserving its diagnostic-binding claim. QUALITY 19 grounds field-specific wording. |
| M2 | attribution / evidence precision | Outside R13-V2; fleet report round-13/mado.md “byte-identical before/after”; actual `gate-file-plane.txt` boundary row | QUALITY 9 | Append standing-use and LOG clarification: config bytes unchanged within that run; no byte-identical outputs across before/after revisions claimed. Preserve 29 PASS / 0 FAIL / 0 UNKNOWN historical result and filed report bytes. |
| M3 | reference-drift / standalone provenance | Outside R13-V3; round-13 `evidence/gate-selftest.txt` has no measured gate revision/digest header | QUALITY 7, 9 and 13 already apply; no duplicate criterion added | Future round-14 standalone receipts carry resolved measured commit, raw gate SHA-256, exact command and observed exit in the receipt itself. The same header audit is to be recorded red on the original receipt and green on the new one; the original is not rewritten. |
| M4 | vacuous existence predicate | `tools/mado-verify.sh` at baseline uses direct `-e` and any `compgen -G` match; ReviewResolver/GateRecon identify directory false-greens | QUALITY 14 covers sets, but not target file type | Require a regular file for direct sources and every matched glob member; follow symlinks to files, refuse directory/dangling targets with owning-row diagnostics. QUALITY 18; isolated direct/default-windows, all-directory and mixed-glob cases. Source-order swap remains an unscored existing-behavior control. |

The initial ai-usage direct-directory fixture choice would independently
fail local inventory. Before any baseline run, ReviewResolver's finding
moved it to default/hypr/windows.conf, read by no other baseline row.
The all-directory toggle fixture also makes no_gaps NOTE; that side effect
is explicitly retained, not described as all-row isolation.

## Gate

### Candidate decisions

- **Admit:** `knowledge/output-colour-boundaries-r14.md`, U5's bounded
  documented transaction/colour-description route. S047/S048 are primary
  exact XMLs; reopened S041 is an explicitly historical advertisement.
  The note distinguishes test/apply, manager features/image descriptions
  and unexercised feature behavior, with concrete decision rows.
- **Admit as correction, not expansion:** U4 retained-data erratum, S049
  and standing-use R13-V2 clarification. These do not add another U-item.
- **Reject:** successful output test guarantees apply success — S047 test
  explicitly denies it. Flip: stronger exact-scope guarantee; still not
  observed host success without an authorized action/result.
- **Reject:** apply success guarantees every property matches — S047
  allows fractional-scale rounding. Flip: property-by-property actual
  state agreement for the specified request.
- **Reject:** advertised colour manager or image-description luminance
  proves HDR/panel accuracy — S041 lacks that evidence and S048 says
  target luminance may be theoretical. Flip: authorized feature-specific
  end-to-end evidence and physical measurement for physical claims.
- **Reject as implementation candidate:** new arbitrary-command receipt
  wrapper. It introduced a second format and generic execution surface
  when the actual R13-V3 correction only requires direct committed-run
  headers. ReceiptBuild/ReviewReceipt/AttackMistake reports remain
  advisory rejected-design evidence; `receipt.py` was removed before
  landing. No wrapper capability, selftest or mutation result is claimed.
- **Not admitted:** actual output test/apply, HDR/ICC/rendering behavior,
  full per-interface phase crosswalk, kernel/DRM diagnosis, U6/U7,
  arbitrary source grammar, generic non-regular filesystem classes beyond
  the named fixture policy, historical theme mutation gaps or promotion.

### Opened rows and located quotes

Access date for every row below: **2026-10-20**. Quotes are ≤25 words;
XML anchors are exact element names rather than transformed-reader offsets.

| row | opened source / revision | located quote | disposition |
|---|---|---|---|
| S047 new | https://gitlab.freedesktop.org/wlroots/wlr-protocols/-/raw/a741f0ac5d655338a5100fc34bc8cec87d237346/unstable/wlr-output-management-unstable-v1.xml | `zwlr_output_configuration_v1.test`: “Even if the compositor succeeds to test a configuration, applying it may fail.” | mined by U5; raw SHA-256 65b0f82a6cf129bf1a1c31a2428795abd33886c15ddd5f3ad97e5922d7bdc3a7 |
| S048 new | https://gitlab.freedesktop.org/wayland/wayland-protocols/-/raw/1.49/staging/color-management/color-management-v1.xml | `wp_image_description_info_v1.target_luminance`: “This luminance range is only theoretical and may not correspond to the luminance of light emitted on an actual display.” | mined by U5; raw SHA-256 18a2678e3352c3be3fbeed20005d48852b7235d0d78f08b9c987a0b8e91449f9 matches installed wayland-protocols 1.49-1 XML |
| S049 new | `.ufo/waves/round-13/w1/globals.json`, captured_utc 2026-10-20T04:10:03Z, canonical own-work path | `.probe.display_socket`: `"display_socket": "wayland-1"` | mined retention correction; metadata demonstrably exists outside globals records; supersedes S046 wording, not its diagnostic-code finding |
| S041 reopened | Same committed capture, not a new client run | `.compositor.version`: `"version": "0.56.2"` | existing historical row remains mined; U5 used-by added |
| S050 new | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/protocols/OutputManagement.cpp | `COutputConfiguration::applyTestConfiguration`, test branch: `TODO: STUB: applyTestConfiguration for test not implemented, returning true.` | mined static safety caveat; parent also opened setDisableHead's saved disabled state plus scheduleReload before test/apply; no binary/source equivalence or live state change asserted |

Parent opened both selected raw XMLs and the installed colour source;
read-only package/digest commands are committed under round-14/evidence.
Advisory older README/governance revisions are not substituted for colour
tag 1.49. Alternate wlr repository revisions are not additional admissions.
A package-derived r112 version is not asserted to be an upstream git tag.

SourceSafety's adversarial source walk motivated one additional exact
implementation open, S050. Its test stub and early disable callback mean
the XML contract cannot license a safe dry-run assumption. Parent opened
the tagged callbacks directly and added only those static facts to U5;
broader advisory host/driver conclusions were not admitted. Creating or
building an output transaction is mutation-class even before apply.
This deepens the same U5 entry, not an additional claim or U-item.

### Registry mutations — old → new

| row | field | old | new | reason |
|---|---|---|---|---|
| S041 | used-by | corpus/knowledge/wayland-protocol-boundaries-r13.md | corpus/knowledge/wayland-protocol-boundaries-r13.md, corpus/knowledge/output-colour-boundaries-r14.md | historical advertisement reused with its exact retained-data boundary |

No existing status/recheck/other used-by field changes. S046's immutable
cell remains historical; S049 carries the correction. S049 is not another
diagnostic implementation discovery or knowledge expansion.

### Wave and outside verification

One validated native batch of 32 seats. L1 holds the canonical planner
seat; connector PlanningWalk is the bounded data-walk mapping, not a
validator-bypassing planner swarm role. Full unchanged taskCall, spec,
registry and seat reports are under `.ufo/waves/round-14/w1/`.
Source/reviewer/critic reports are authoring-lane advice, not independent
clearance. Preliminary claims (including must/should wording, alternate
source pins and ai-usage fixture isolation) are not final admitted facts.

**Fresh non-author admit/reject spot-check and round admission: pending
parent after-report closure.** The prior round's outside R13-V1..V3 are
learned here; no current outside verdict is fabricated. SHONEN remains
four author assertions.

### Tooling and safety

OutputSpec installed **wlr-protocols r112.a741f0a-1**, official pacman
`extra`, via `sudo pacman -S --needed --noconfirm wlr-protocols`, to open
the owning XML locally. ReviewSourceBar also used pacman `-Sw` to download
the same package into cache for source inspection; download-only is not
a second install. No full-system upgrade or partial `-Sy` was performed.
All other seat tool records report no installs/updates.

Host configuration and compositor state are read-only; no feature
requests were issued by this round. The package installation is the
explicit tooling exception, not compositor mutation. Sibling provinces
remain read-only; compositor display policy does not absorb DRM/KMS,
driver, input-kernel or hardware diagnosis. There was no inherited
uncommitted lane work at start; the non-author round-13 spotcheck is
preserved untouched.

Safety's low-severity incident is retained: AttackCoverage invoked a
read-only-looking `jj log` without `--ignore-working-copy`, creating
local jj snapshot/import state. No history was rewritten to hide it;
future read-only jj calls must use that flag. This did not change the
domain configuration/compositor or create a third axis claim.
Public-source scratch owners removed their exact round-14 `/tmp`
paths after Safety's scan, with successful removal commands; prior
round-13 selftest trees and foreign scratch were deliberately untouched.
Some preliminary reports predate the package install or final gate
digest; they are advisory chronology, not current-state authority.

Original source-hash pipelines recorded their shell-pipeline exit.
`evidence/source-bindings-pipefail.txt` additionally binds each fetch
with pipefail enabled, so curl failure cannot be hidden by sha256sum.
The colour release's annotated tag object and peeled commit are distinct;
the exact binding is in `evidence/colour-release-binding.txt`.
All abbreviated evidence paths in this lesson resolve under
`.ufo/waves/round-14/`.

### Exercised verification — L1 after all seats finished

Content measured at `32118fc1014837b3a385c7a66abbdc59b1560835`.
Full commands/stdout/stderr/exits are under
`.ufo/waves/round-14/evidence/`; these are observed results, replacing
the earlier explicitly unrun predictions without rewriting them.

- `python3 .ufo/waves/round-14/measure.py 873ff081b2ac363df771261b0ed950cba50d8988`:
  U1–U4 4/7, navigation 27/27, regular-target diagnostics 0/3 and
  all three selected overall exits 0; `before.txt`, exit 0.
- Same command at `32118fc1014837b3a385c7a66abbdc59b1560835`:
  U1–U5 5/7, navigation 28/28, exact diagnostics 3/3 and overall
  exits all 1; `after.txt`, exit 0. All U5 structural facets, reserved
  source joins and inverse reciprocity pass. These are structural
  counts, not semantic truth: parent opened sources/body and
  AttackCoverage agrees on the actual bounded note, as authoring advice.
- Both revisions retain clean, order, file-symlink, newline-regular,
  direct-missing and zero-match behavior; the overlap control shows
  local inventory already detects ai-usage-directory at baseline.
  The all-directory case retains toggle NOTE, while direct/mixed keep PASS.
- `bash tools/mado-verify.sh --selftest`: 372/372, exit 0;
  `gate-selftest.txt` carries resolved measured commit and raw digest.
- `bash tools/mado-verify.sh --no-live`: 29 PASS, 0 FAIL, 0 UNKNOWN,
  8 SKIP, 4 NOTE, exit 0; `gate-file-plane.txt`. Within-run config
  boundary equality only, not cross-revision output equality.
- `regression-recut.txt`: historical 10/10 KILLED; new
  `regular-target-mutants.txt`: 4/4 KILLED; retained
  `retained-census-mutants.txt`: 8/8 KILLED. All GREEN controls/restore OK,
  all exits 0; TSVs retain each measured mutant. The derived target is
  cd1d73d75fcc8e5b96d5b83c0d16660897e58cf32edf77416d389fa16b9f3f96;
  excised regression/snapshot machinery is outside those mutant claims.
- `python3 .ufo/waves/round-14/frozen/verify.py`: verifies input
  digests first, table match 10/10, `MADO_REGRESSION: PASS` and
  `frozen_match`, exit 0; `frozen-regression.txt`. Its `--selftest`
  is 12/12, exit 0; `frozen-selftest.txt`.
- M4's same inline auditor (full command in `contract-red.txt` /
  `contract-green.txt`) exits **1**, FAIL 0/3, on baseline measurements,
  then **0**, PASS 3/3, on delivered measurements. The source-policy
  repair is demonstrated able to fail, not just a green count.
- M3's same inline header auditor (full command in
  `provenance-red.txt` / `provenance-green.txt`) exits **1** on the
  unchanged round-13 selftest receipt, naming missing measured_commit
  and gate_sha256; it exits **0** on the new receipt. No wrapper shipped.
- Maintained source census: before and after both exit 0, retaining W04
  S030/S042/S045 warnings; full outputs `census-before.txt` /
  `census-after.txt`. Revision counter: rows 46 → 50; A/B/C
  42/1/3 → 46/1/3; mined/queued/rejected 34/8/4 → 38/8/4.
  Four new source rows support one new U5 entry plus the correction.
- Existing conservative merge screen: `python3
  .ufo/waves/round-13/w1/reports/MistakeFix.py --registry corpus/SOURCES.md`
  exits 0, rows=50, collisions=0; `source-merge.txt`. Historical rejected
  and explicit superseding history is retained, not silently erased.
- `committed-bindings.json` binds gate/measure/frozen/spec inputs to
  measured content. Raw gate fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207
  equals frozen gate input; retained harness is 75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5.
- `cleanup.json` records exact selftest directories emitted by this
  round's own mutation runs and removed after receipts/TSVs were copied.
  Foreign/round-13 fixtures were not swept.

Source-review-only gaps remain explicit: the probe's U4 facets are
structural, the maintained census checks registry validity separately,
and its three scored diagnostics do not test space-containing paths.
The final exactly-one `covers:` selector was tightened before measurement.
No source parser, full-config hash, theme mutation or feature-behavior
capability is inferred from these observations.

Local C1/C2 verdicts: improved. Learning trends: expansion improved,
quality improved, discernment improved narrowly via learned outside
R13-V1..V3. Current-round independent admit/reject spot-check remains
pending the parent's after-report non-author closure.
