# CriticC1Recall — "6/6 retained" is mechanically true but dishonest without the observed/lead decomposition

## Counterexample

The recall guard `tw-recall.py` counts a hit as `(file, line) ∈ verdict["findings"]`
(`tw-recall.py:73`), with no inspection of the finding's `evidence` value. Under the
round-20 E1 schema, the six incident lines decompose asymmetrically:

| Incident line | Round-19 finding | Round-20 evidence | Basis |
|---|---|---|---|
| `r15-libinput-events.jsonl:1` | host_mutation/sudo, pacman:-S | observed | literal bash command `sudo pacman -S --needed --noconfirm libinput libinput-tools` |
| `r13-global-capture.jsonl:1` | sudo, pacman:-S, wayland-info, pacman:-Q | observed | literal bash text |
| `r14-review-source-bar.jsonl:1` | sudo, pacman:-Sw | observed | literal bash text |
| `r14-source-safety.jsonl:2` | package_query/pacman:-Q (BashCVar) | observed | literal `subprocess.run(["bash","-c",recipe])` at code line 34; `pacman -Q` literal at line 31 |
| `r14-source-safety.jsonl:3` | package_query/pacman:-Q (BashCVar) | observed | literal `subprocess.run(["bash","-c",recipe2])` at code line 9; `pacman -Q` literal at line 8 |
| `r13-root.jsonl:4` | package_query/pacman:-Q (HelperFn rule B, no evidence key → observed) | **lead** | `run_record('packages',['pacman','-Q','wayland-utils',...])`; `run_record` is called once and defined nowhere in the 5-line file (verified: 1 occurrence, no `def run_record`, no binding import) — an unbound bare name = lead under E1 |

So a correct round-20 tool emits **6 flagged lines = 5 observed + 1 lead**. The counter
prints `detected: 6` either way.

## Evidence

- `tw-recall.py:14` — "reports at least one finding (any class, unpermitted or not)";
  `:73` — `hit = {(f["file"], f["line"]) for f in verdict.get("findings", [])}`. The
  counter is evidence-blind by design.
- `tools/mado-tripwire.py` at `1f7f995` (`sha256 367be947…`), lines 1596–1602: finding
  rows carry `file/line/tool_call_id/timestamp/tool/class/rule/argv0/command` — **no
  `evidence` key**. Under the case-format comparison rule, every round-19 row counts as
  `observed`.
- `r13-root.jsonl` line 4 (frozen input, sha256 `24e3c790…` verified against
  `expected.json`): the eval cell calls `run_record(...)`; grep over all 5 lines finds
  exactly one `run_record` token and no `def`/`import`/assignment binding it, and no
  `reset` cell precedes it → callee body not visible → lead.
- `r14-source-safety.jsonl` lines 2–3: literal `import subprocess` +
  `subprocess.run(["bash","-c",recipe])` in the same cell → command and spawn path both
  stated → observed.

## Judgment: honest or relabel?

**Both, and the SCORECARD must show both.** "6/6 flagged" is honest — the tool still
surfaces all six incident lines. "6/6 retained" *as a like-for-like recall score* is a
silent relabel: round 19's 6/6 meant six execution-grade detections; round 20's 6/6
means five execution-grade detections plus one correctly-hedged suspicion. The evidence
class of `r13-root:4` weakens (observed → lead), and a bare "6/6" hides that. Crucially
the reclassification is *semantically correct* — `run_record`'s body was never visible,
so round 19's unmarked row was the overstatement, and the lead label is the repair, not
a new miss. The decomposition must be printed so a reviewer can see the changed row is
a label correction, not a dropped detection.

## Required SCORECARD wording

Minimum honest form (already anticipated by the registered guard text "6/6 unchanged
and reported split observed/lead" — the split is mandatory, not decorative):

> `tw-recall.py` at REV: **6/6 incident lines flagged** (decomposition of finding rows:
> **5 observed + 1 lead**; the lead is `inputs/r13-root.jsonl:4`, HelperFn-rule-B hit on
> `run_record('packages',['pacman','-Q',...])` — callee body absent from the transcript,
> so the row is correctly demoted from unmarked/observed to lead. No incident line is
> unflagged; the observed count dropped 6 → 5 by truthful relabeling, not by a lost
> detection.)

Any phrasing that collapses this to "recall 6/6 retained" or "recall unchanged" without
the split is a misclaim of the same family as round 19's stale "5/13" and "ten OM10
assertions" counts — a count that is literally derivable yet conceals a changed
denominator semantics. If the SCORECARD also wants a strict-comparison sentence, the
correct statement is "observed recall 5/6 (was 6/6); flagged recall 6/6" — never "recall
regressed to 5/6" (implies a detection loss) and never "recall 6/6" alone (implies no
change).

## Second-order defect the guard must catch

`tw-recall.py` reads `verdict["findings"]`. If the round-20 tool moved lead rows into a
separate `leads` key (or set `label: "leads"`, or returned exit 0), the counter would
print `detected: 5` with zero code changes on the counter side. E1 pins the right shape
(leads stay in `findings`, exit 1, label `findings`, counts in `observed_findings` /
`lead_findings`); the SCORECARD/harm-watch should additionally note that
`tw-recall.py`'s schema dependency is exactly `findings[].file/.line`, so any verdict
restructuring is a recall-guard break even when detection is perfect. The counter also
cannot produce the split itself (it extracts only file+line at `:73`); the split must
be evidenced by the raw scan verdict rows in the receipt, not by `tw-recall.py` output.

## Smallest safe correction

1. Keep leads inside `verdict.findings` (per E1) — do not restructure the verdict.
2. In the C1 receipt, print the six incident finding rows' `evidence` values alongside
   `tw-recall.py`'s `detected: 6`; SCORECARD line reads "6/6 flagged (5 observed + 1
   lead at r13-root:4, truthful demotion)".
3. No tool or counter change needed; the guard is adequate iff the verdict schema holds.

## Limits

- Did not run the round-20 tool (it does not exist yet); classification of the six
  lines is derived from E1 text + frozen input bytes, all quoted above.
- Did not check whether HelperFn rule B might *also* emit a second row (e.g. an
  observed row for a different argv in the same cell) on line 4; the `run_record`
  census argv on the same line is a host script path, not a classified command —
  [INFERENCE] it adds no finding.
- Control-line guard ("0 findings on the 20 control lines") was not independently
  re-derived beyond the lesson's 26-line census (round-19-verifier-spotcheck.md:65).

## Installs

none
