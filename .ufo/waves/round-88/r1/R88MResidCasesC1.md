# R88MResidCasesC1 — residual attack on C1, frozen bytes

Seat: R88MResidCasesC1 · 2026-11-06 · lane root `/home/vgpnk/Projects/shokunin/mado-shokunin` (all bytes read from git at the named revisions; no mutation anywhere).

## Verdict: **C1 VERIFIES**

All four attack items come back clean. Evidence per item below; every command's exit code stated.

## (1) Re-run of the C1 counting command at the measured revisions — reproduces both receipts

Command run exactly as declared in the frozen declaration (`## C1 — counting command`), from the lane root, `<CASES_SHA>` = `a0e81b191fb0f80ca352699ede47962c1ac01c1ae8e9e15ccf50b1d7fab4a091`:

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
TMPDIR=$S/runA python3 -I quality/counters/c1-r88-mako-fields.py --repo . \
  --rev 650e18bdf0ae404ec9a80874c4503ecf3237e8e6 \
  --base-rev 24ba2a9ddac21c1211579231e6ee1d98963f9988 \
  --cases .ufo/waves/round-88/controls/mako-cases-r88.json \
  --expect-cases-sha256 a0e81b191fb0f80ca352699ede47962c1ac01c1ae8e9e15ccf50b1d7fab4a091 \
  --expect-mutants-sha256 2a569770aa255cfaf0afc15c63136e8c261396ca280d5646c51171e9009864a1 \
  --expect-r87-cases-sha256 0a9558743a721f70bb64b48d188b375f1468a140b00ca75ac93ab59c316d5fe3 \
  --scratch-root $S/runA
```

- rev `650e18bd…` (A): exit **0**; verdict line byte-identical to `receipts/c1-measured-A-r88.txt` (`cmp` exit 0): `MADO_MAKO_FIELDS: TARGET_MET … cases=62 correct=62 carried=22/22 mutants=22 killed=22 naive_correct=14 globals_include_correct=15 base_tool_correct=33 inputs_ignored_correct=43 score=10.0000 tool_sha256=07930521… cases_sha256=a0e81b19…`
- rev `7d307486…` (B, harm check): exit **0**; verdict line byte-identical to `receipts/c1-harm-at-B-r88.txt` (`cmp` exit 0): same shape with `rev=7d307486… tool_sha256=c374d715…`.
- Full-output diffs: 214/214 content lines identical in both runs; the only difference is the receipt's trailing `rc=0` capture line, which the capturing seat appends after the counter's stdout (the counter does not print it). diff exit 1 solely on `215d214 < rc=0`.
- Counter bytes: the executed `quality/counters/c1-r88-mako-fields.py` sha256 `3678425addb5f661d3f284ef423e3566446b54714cb2148c5696a8cdfe11cc1f` = frozen-declaration pin = receipt `counter_sha256`; sibling `c1-r87-mako-criteria.py` sha256 `4d801c30b302ed5972142415012d8f461109459d9c44e85e0badef57a2ed3645` = receipt `r87_counter_sha256` = `git show 9e36e3a3:quality/counters/c1-r87-mako-criteria.py`. Working tree and freeze byte-identical for both counters.
- Controls re-derived, all strictly below N=62 as the predicate requires: naive 14, globals-include 15, base-tool 33, inputs-ignored 43; mutants 22/22 killed; carried r87 cases 22/22.

Dead step (recorded): running a copy of the frozen counter extracted to scratch (`$S/c1-counter-frozen.py`) fails with `FileNotFoundError: [Errno 2] No such file or directory: '…/c1-r87-mako-criteria.py'` (exit 1, both A and B attempts) — the counter resolves its r87 sibling relative to its own file, so the declared in-place command is the only runnable form; the in-place file was then proven byte-identical to the freeze (above), so frozen bytes were in fact executed.

## (2) L1-authored cases c60–c62 vs upstream mako v1.11.0 — all three expectations follow

Upstream fetched today: `curl -fsSL https://raw.githubusercontent.com/emersion/mako/v1.11.0/{types,criteria,config}.c` (exit 0); shas `types.c c2f3398d…`, `criteria.c 22767742…`, `config.c 94c3a4e7…` — byte-equal to the pins recorded in the frozen case file's `notes`. Case bytes from `git show 9e36e3a3:.ufo/waves/round-88/controls/mako-cases-r88.json` (sha256 `a0e81b19…` = freeze pin).

- **c60-urgency-high-means-critical** — pin `types.c:119-120`. Verified: `} else if (strcasecmp(string, "high")) == 0) { *out = MAKO_NOTIFICATION_URGENCY_CRITICAL;`. Notification `urgency=critical` → CRITICAL via `types.c:116-117`; section `[urgency=high]` → CRITICAL; `criteria.c:95-98` (`criteria->urgency != notif->urgency`) therefore matches → `anchor=bottom-center`. **Follows.**
- **c61-urgency-value-case-insensitive** — pin `types.c:110`. Verified: `strcasecmp(string, "low")` — section `[urgency=LOW]` parses to LOW through `criteria.c` → `apply_criteria_field` → `parse_urgency`; input `low` → LOW; equal → `anchor=bottom-center`. **Follows.**
- **c62-repeated-field-last-value-wins** — pin `criteria.c:298-299`. Verified: `strcmp(key, "app-name") == 0 → criteria->app_name = strdup(value);` — and `parse_criteria` applies every token in turn (space-delimited at `criteria.c:209`, final token at `:243`), each assignment overwriting the last → `[app-name=gamma app-name=alpha]` leaves `alpha` → matches input `alpha` → `anchor=bottom-center`. **Follows.**

No defect found in c60–c62.

## (3) Spot-check of 8 scout cases (c23, c25, c26, c27, c33, c46, c51, c56) — all follow

Manual source: `zcat /usr/share/man/man5/mako.5.gz | nl -ba` (the numbering the pins use). All eight expectations verified against the pinned line, manual and upstream:

- **c23** `include=relative.ini` refused, base section applies — manual L47 "The path must be absolute or otherwise start with ~/" ✓.
- **c25** unconfigured font default `monospace 10` — manual L170 "Default: monospace 10" ✓.
- **c26** unconfigured layer default `top` — manual L407 "Default: top" ✓.
- **c27** unconfigured border-size default `2` — manual L234 "Default: 2" ✓.
- **c33** `summary=Hello` vs input `hello` no match, no refusal — manual L447 "exact match on the summary"; `criteria.c:110-113` `strcmp` (case-sensitive) ✓.
- **c46** bare word `[actionable]` matches `actionable=true` inputs — manual L514 `[actionable]` bare form; `criteria.c:288` `value = "true";` ✓.
- **c51** `[actionable=true]` vs input `actionable=false` no match, no refusal — `criteria.c:86` `criteria->actionable == wl_list_empty(&notif->actions)` → `true == true` → section rejected ✓.
- **c56** `icons=yes` refused while default `icons=1` still effective — `config.c:590-593` routes through `parse_boolean` (`types.c:19-29`, accepts only true/false case-insensitive or 1/0), `yes` fails → refusal ✓.

Notes, not defects: c53 (`summary~`) expects refusal although upstream supports it — that is the lane's declared named limit in the frozen declaration ("summary~ and body~ stay refused and are named limits"), a stance case, correctly labelled. c57/c58 additionally verified: manual L623-628 DND example matches the fixture; the winner between `[mode=do-not-disturb]` and the more specific section follows from last-matching-section-wins (carried r87 case c21).

## (4) Freeze-commit hygiene — clean

- `git show 9e36e3a3103349b939982e532feca443f02e660d:tools/mado-mako.py | sha256sum` → `67a955a5fa06135c2748855b7e452bd3f0792c540002009ec90842ee5c986698` (exit 0) — the base tool; the candidate (`07930521…` at A) is **not** in the freeze, as declared.
- `git diff --name-only 9e36e3a3… 650e18bd…` → exactly `tools/mado-mako.py` (exit 0); `git show --stat 650e18bd…` → 1 file changed, +132/−20. Commit A changes **only** the C1 tool — separability by commit scope confirmed.

## Residual risk / verification gaps

- I did not independently re-derive the mutants' semantics (kill verdicts taken from the counter's real path; the mutation-tester seat's lane).
- The base-tool/inputs-ignored "unexpected-refusal" FAIL labels for c54–c62 are the counter's per-case control reasons (CLI-surface/inputs-ignored), counted into `base_tool_correct=33` / `inputs_ignored_correct=43`; I verified the counts and their strict-below-N use in the verdict, not each label's prose.
- Upstream .c files were fetched at audit time and matched the frozen pins byte-for-byte; if upstream retargets the `v1.11.0` tag the pins would catch it (shas recorded here).
- Six dirty working-tree entries exist at the lane (unrelated, unexamined); all audited bytes came from `git show` at the named revisions and none of the verdict-relevant files differ (counter shas proven equal).

Installs: none. Scratch `/fast/scratch/hyaku/mado-r88/R88MResidCasesC1/` deleted on exit.
