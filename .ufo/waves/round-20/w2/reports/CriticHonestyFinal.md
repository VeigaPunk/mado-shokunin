# CriticHonestyFinal — partly falsified: every headline counter reproduces, but two receipt/mode defects and three bounded wording overclaims stand

Scope: prose-honesty pass over `corpus/lessons/round-20.md`, SCORECARD round-20 sections
(:1204-1343), `LOG.md` round-20 entry, `corpus/knowledge/tripwire-precision-r20.md`,
SKILL.md :542-571. All checks run in `/tmp/mado-r20w2-CriticHonestyFinal` (clone, origin
removed). Lane tip `a4046a8`.

## Confirmed (with commands)

| Claim | Command | Observed | Verdict |
|---|---|---|---|
| C1 `1f7f995` 29/175 (P7 S2 W4 H15 L1) | `python3 -I .ufo/waves/round-20/tw-precision.py 1f7f995c…` | P 7/66, S 2/17, W 4/22, H 15/52, L 1/18 → 29/175 | exact |
| C1 `28c6837` 172/175, misses = W-class-method-instance, H-jj-var-verb-help, L-b14 | same @ `28c6837` | 3 fails, exactly those names; b14 got `{exit:0,findings:[]}` vs want lead — "not implemented" accurate | exact |
| pre-harm `9c54c56` 110/175, P 66/66 | same @ `9c54c56a…` | 110/175, P 66/66 | exact |
| recall 6/6 = 5 observed + 1 lead, controls 0 | `tw-recall.py 28c6837` → detected 6/6; `tw-recall-split.py` → `detected_observed:5, detected_lead:1, control_findings:0` | exact |
| 11 suites 247/247 | harm-watch enumeration `.ufo/waves/round-{17,18,19}/tripwire/*` → 16+9+33+30+31+1+45+34+13+18+17=247, `--selftest` rc 0 each | holds **for that enumeration** (see O4) |
| 8 `r20_edit` each adds a finding; 2 lead cases gain marker | git-diff of `r19-bashcvar`/`r19-helperfn` expected.json: 8 clean→findings edits + `evidence:"lead"` added on `py-lead-two-calls`, `py-lead-cross-cell-literal`; no case lost a finding | exact |
| frozen replay | `--frozen .ufo/waves/round-19/frozen` → `frozen_match`; `round-18/frozen` → `frozen_verdict_mismatch` | exact |
| held-out 0/12 → 0/12 | `precision-heldout-{1f7f995,final}.txt` receipts parsed | exact |
| C2 20/28 → 22/30 | `measure.py 1f7f995` c1 `{criteria:28,lesson_cited:20}` → `a4046a8` `{30,22}` score 7.3333 | exact |
| tally-check red 5/5 MISMATCH (exit 1); green 4/4 | `tally-check.py --set red` rc=1, 5 MISMATCH; `--set green --rev a4046a8` rc=0, 4 MATCH | exact |
| `isolate.sh` FAIL_CLOSED 6/6 + positive | `bash isolation-check.sh .ufo/…/isolate.sh` → 6 FAIL_CLOSED + POSITIVE_CONTROL_OK, rc=0 | exact |
| SOURCES 98→112 | `grep -c '^| S' corpus/SOURCES.md` = 112 | exact |
| w1 85 seats, 0 dead | assignments.json 85 members ↔ 85 report .md, join complete | exact |
| LOG "Installs: none" | all 85 reports' `## Installs` = none (RevengeRuleBIntent says "No installs." inline) | exact |
| verdict keys | `mado-tripwire.py --scan` on `CaseLeadsInvisible--run-record.jsonl` → `lead_findings:1`, row `evidence:"lead"` | exact |
| M2 cite | `.ufo/waves/round-19/w2/reports/SentinelGatePath.md:75-79` documents `[ -e ] && mount && echo` under `set -e`, real `hyprctl probe` ran | exact |

## Falsifications / defects

**F1 — committed receipt violates the stated receipt contract.** SCORECARD:1324: "Receipts
`.ufo/waves/round-20/evidence/`, each headed `RECEIPT … measured_commit=28c6837…`".
`.ufo/waves/round-20/evidence/isolation-check-run.txt:1` reads
`measured_commit=PENDING` (unchanged since `f3da504`; all other 13 receipts comply).
Fixable: recut that receipt's header line; content is fine.
→ Replace the SCORECARD sentence with "each receipt except `isolation-check-run.txt` (its
header reads `measured_commit=PENDING`) is headed `measured_commit=28c6837…`" — or recut
the receipt and leave the sentence.

**F2 — the criterion-29 red fixture is committed non-executable.** `git ls-tree` mode
`100644` for `evidence/inns-r19-shape.sh`; `isolation-check.sh` refuses non-executables
(`COULD_NOT_EVALUATE`, exit 2). `bash isolation-check.sh …/inns-r19-shape.sh` in a fresh
checkout therefore cannot reproduce "FAIL_OPEN 5/6, exit 1" — the only reproduction is
its own receipt (content sha256 `8bd507f0…` matches). The `crit29-inns-r19-shape.txt`
receipt implies the file was executable when cut; the exec bit was never committed.
→ `git update-index --chmod=+x` / `chmod +x` the fixture, or add a sentence "the fixture
was run with an exec bit that was not committed; `chmod +x` before re-running the check".

**F3 — the knowledge note's `surface:` line is rejected by the lane's own instrument.**
`corpus/knowledge/tripwire-precision-r20.md:4` is free text; `measure.py` requires
`surface: P<n>` and lists it under `rejected` (`MALFORMED`) at `a4046a8`. c1 still reads
22/30 so C2 stands, but the note is invisible to the routing scan. Precedent notes use
`surface: P<n>`. → replace with `surface: P6` (lane tooling plane).

**F4 — "every existing tripwire suite all-pass" is enumeration-dependent.** The 247/247
claim holds only for `.ufo/waves/round-{17,18,19}/tripwire/*`. Two committed suites
outside that enumeration stay red at `28c6837`: `round-17/w2/adversarial` 6/26 (was 4/26
at `9c54c56`, 6/26 at `1f7f995` — no regression) and `round-18/drafts/tripwire/r18-helperfn`
17/24 (22/24 at `1f7f995` — 5 newly expected-clean py-helper cases now detected; the
merged `r19-helperfn` suite was edited to match, the draft was not). Not a regression in
claimed behavior, but the guard sentence says "every … suite".
→ Replace with "every suite under `.ufo/waves/round-{17,18,19}/tripwire/` (247/247);
`round-17/w2/adversarial` and `round-18/drafts/tripwire/r18-helperfn` remain
known-incomplete draft suites and were excluded".

**F5 — lesson "(exit 1)" needs `--set red`.** `round-20.md:17` "`tally-check.py
tally-claims.json` prints MISMATCH for all five registered round-19 statements (exit 1)".
With no `--set`, the green entries error for lack of `--rev` and exit is **2**
(TALLY_SUMMARY set=all n=9 mismatch=5 error=4). The stated run prints the five MISMATCHes
but exits 2; exit 1 requires `--set red`. → append "`--set red`" inside the parenthetical:
"(`--set red`, exit 1)".

**F6 — wording "the pre-harm reading is restored, not approximated" (SCORECARD:1257).**
The `9c54c56` reading is real (P 66/66 re-measured by me), but the tool at `9c54c56` was
run against a suite written a full round later — nothing was *restored* to `9c54c56`;
the 9c54c56 reading is a back-projection. Bounded; suggest "(the pre-harm tool re-measured
on this suite, not approximated)".

## Not overclaims (explicitly checked)

- "L1 ran no package/service/compositor/input command and no hyprctl" — consistent with
  the host pause and seat reports; no contradiction found in w1 reports (unverifiable
  negative, marked [INFERENCE] in the spirit of the seat self-reports).
- "held out … outside the contract … 0/12 before and after" — confirmed on receipts.
- M7 "no lane ref moved except by `jj-lane.sh`" — `git for-each-ref` in lane: `master` at
  `a4046a8`, no `refs/remotes/origin/*`; `refs/jj/keep/*` are jj internals. Holds.
- Knowledge note "resolved to depth 4" and other limits — spot-consistent with tool
  behavior; not exhaustively probed.

## Limits

- The whole-corpus no-harm diff vs `9c54c56` is explicitly pending (owned by sibling
  seats); not evaluated here.
- I did not run `jj --version` (no jj in lane) or any host-affecting command; S099–S112
  fetch bodies were not re-fetched (other seats own source integrity).
- `adversarial`/`r18-helperfn` failures were treated as outside the claimed enumeration;
  if L1 intends "every committed expected.json suite," F4 upgrades to a C1 guard breach.
- inns-r19-shape.sh content equality (sha256 `8bd507f0…` = receipt header) confirms the
  receipt measured these bytes; only the exec bit differs.

## Installs

none
