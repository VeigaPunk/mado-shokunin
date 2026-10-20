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
