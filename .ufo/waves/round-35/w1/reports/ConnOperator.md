# ConnOperator — operator teachings vs QUALITY.md / SKILL.md

Seat: w1 ConnOperator (connector). Date: 2026-10-24. Read-only sweep; nothing edited.

## 0. Literal premise: the glob matches zero files

`corpus/lessons/operator-*.md` does not exist. Verified three ways:

- `ls corpus/lessons/` → 43 files, all named `round-<n>.md` or `round-<n>-verifier-spotcheck.md`; `grep -iv round` on the listing prints nothing.
- `find . -name 'operator-*' -not -path './.git/*'` over the whole lane → 0 hits.
- `git log --all` and `git status` → no committed or untracked `operator-*` file, none ever deleted.

The real operator-authored teaching corpus is `considerthese/YYYY-MM-DD.md` — six
daily reflection files (2026-10-19 … 2026-10-24), each with "Top 3 lessons / gains"
plus "Self-improvement suggestions (proposals only; not acted on)". The round-32
lesson treats it as canonical ("`considerthese/2026-10-23.md` (operator-authored,
read-only — not edited)", `corpus/lessons/round-32.md:120`). Section 1 below scores
those teachings; section 2 scores the other channel operator rulings actually travel
through (embedded directives inside lesson files). **If the spec meant literal
`operator-*.md` files that have not landed yet, the reflection table is vacuously
empty and section 1 is the whole answer.**

## 1. `considerthese/*` teachings vs QUALITY.md / SKILL.md

"Reflected" = a rule in `corpus/QUALITY.md` or `SKILL.md` states the teaching with a logic the next seat can apply, not merely that the incident is named somewhere.

### Reflected

| Teaching (file → item) | Where reflected | Pointer |
|---|---|---|
| 10-20 T1: never a partial upgrade; helpful-tool authorization is not install permission | QUALITY 20 (pre-install plan-vs-installed comparison) and 21 (host-pause: no transaction, no probe, not even to read `--help`); SKILL standing rule | `corpus/QUALITY.md:72-105` (criteria 20–21); `SKILL.md:39-45` (host-wide package pause) |
| 10-20 T1: prompt fences leaked twice — the fence must be a tool, not a sentence | QUALITY 21's classifier requirement (`mado-action-plan` must refuse the literal libinput argv even path-prefixed/mislabeled) | `corpus/QUALITY.md:88-92`; `SKILL.md:611-612` (gate registry rows `mado-action-plan`, `mado-action-plan-frozen`) |
| 10-20 T3: non-author admit/reject checks are the calibration spine | QUALITY 12 (`[x]` needs a named non-author verifier; a lane-dispatched seat stays `[~]`) | `corpus/QUALITY.md:18` |
| 10-21 T1 + 10-22 T1: a finite green suite is not no-harm; guards and honest stops are the deliverable | QUALITY 33 (no-harm credit only against discovery attacks frozen before the patch) and 35 (post-patch fixture is never a pre-patch guard); 30 (precision beside recall, with the removal-side gap recorded) | `corpus/QUALITY.md:316-320` (33, 35); `corpus/QUALITY.md:249-259` (30); `SKILL.md:1975,1981` (finite oracle ≠ no-harm; harmed classifier stays labelled) |
| 10-21 T3: receipts bound to tool bytes and measured revision | QUALITY 23 (verdict token ↔ receipt), 24 (`tool_sha256` + `measured_commit`), 26 (producer exit status) | `corpus/QUALITY.md:111-154` |
| 10-23 T1: replace self-model counters with the real compositor oracle | QUALITY 36 (self-model counter → independent oracle or declared agreement-only) | `corpus/QUALITY.md:324` |
| 10-23 T3: host safety as a property of the counter — isolated oracle + `HOST_SAFETY … delta=` receipts | Reflected as tooling + the safety fence, not a QUALITY criterion | `harness/oracle.py` (registered, not a doc); SKILL safety rules `SKILL.md:235-260`; QUALITY 29 fail-closed isolation `corpus/QUALITY.md:232-248` |
| 10-24 T2: a frozen counter can be silently dead — smoke-run it at freeze and commit the output | QUALITY 38/49 verbatim ("smoke-run once at freeze … the smoke receipt is the only cheap catch") | `corpus/QUALITY.md:332` / `corpus/QUALITY.md:355` |
| 10-24 T3: the corpus checks its own navigation; missing index rows are a defect | SKILL gate registry holds `check-index.py`/`check-index-rows.py`/`check-axis-scores.py`; QUALITY 52 (sweep finds a defect → record + route, repair is its own claim) | `SKILL.md:678` (mado-axis-scores row); `corpus/QUALITY.md:358` |
| 10-22 T2: stale `~/.config/{foot,kitty,ghostty}` trees = "declared bytes, no consumer" | SKILL terminal-tree table states it verbatim | `SKILL.md:121-127` |
| 10-19 T3: pinned bytes/line cites are evidence; cosmetic edits break receipts | QUALITY 6/7/13 (revision-named re-derivation, commit-hashed artifacts, durable evidence) | `corpus/QUALITY.md:12,13,19` |

### Not yet reflected (and what each would require)

| Teaching | Gap | What reflecting it requires |
|---|---|---|
| 10-19 T2: front-door + LOG writes need one writer or a rebase-before-merge check (README #1 vs #2 collision) | No QUALITY criterion covers concurrent writers colliding on one file | A criterion naming the single-writer rule for shared append surfaces (`LOG.md`, `README.md`) plus a rebase-before-merge preflight check; scope is fleet-side too, so it may belong in PROTOCOL, not only QUALITY |
| 10-20 T2: each documentary rubric has a finite ceiling; the next coverage claim needs a new declared rubric + baseline before it counts | QUALITY has no "saturated-rubric rollover" rule; SKILL:524 states the ceiling descriptively ("documentary rubric can complete while these remain unknown") but no admission rule | A criterion: a coverage claim must declare its rubric's denominator and state when it saturates; a saturated rubric cannot silently extend to N+1 — the rollover is a named new baseline (echoes QUALITY 22's "report literal vs semantic counters separately" but is about saturation, not selection) |
| 10-22 T1 (verifier-routed): freeze wave-2 attack fixtures as a registered population before any further tripwire change | QUALITY 35 covers "fixture found after a patch" but the *freeze-the-attack-population-first* phrasing is a routed, still-open debt | C2-style predicate: the registered attack population must land in a commit earlier than the next candidate; a check like `check-registration-order.py` extended to fixture populations. Round-35 C2's clause ledger is adjacent but does not encode it |
| 10-24 T1 (implicit): flag N consecutive self-audit rounds with no `tools/`/`corpus/knowledge/`/`PROVINCE.md` change (domain-vs-meta ratio) | Operator-side watch item; no lane rule requires surfacing it | Optional: a SCORECARD/LOG reporting convention (one line per round: domain-touch yes/no). Cheap, no counter needed; needs an owner to adopt it |
| 10-24 residual (named by operator): relevance-free lesson citations still pass — rubric checks resolution, not relevance | Open residual; QUALITY 54 binds anchor-to-file, nothing binds anchor-to-topic | A semantic check is not automatable cheaply — at minimum a declared limit line next to criterion 54/51 noting "resolution ≠ relevance" so future counters don't read green as topicality |
| Embedded ruling (round-25 M25-5): "never change the judged object" — the leg rule covers *after*, this hit was *during* judgment | Only implicitly covered by append-only errata (QUALITY 4/44); no rule names the during-judgment window | A criterion: once a claim is frozen and a judgment pass is running, edits to the judged artifact go into an appended errata block after the verdict, never in place; counts come from `ls`/`grep -c` of receipts, not memory |
| Embedded ruling (round-26 M26-4): dispatched task text must be byte-identical to the validator's rendering — the operator RULES.md suffix broke §6.2 | Disclosed "next round sends the rendered text unchanged"; nothing in QUALITY/SKILL encodes it; round-26 spotcheck suggests a rendered-text digest | Fleet-side fix (validator emits a digest of sent bytes) or a lane-side waiver clause; the spotcheck ruled "wave validation stands" only because the delta was operator-mandated — a criterion would need to carve out that suffix explicitly |
| Embedded ruling (round-26 M26-1): nested-Hyprland oracles must never touch the operator's live session | Fixed in `harness/oracle.py` (bubblewrap, own tinywl, `HOST_SAFETY delta=`) but the *rule* lives only in code + lesson, not in QUALITY/SKILL | A QUALITY criterion or SKILL safety-rule line: a counter harness that launches a compositor must run it in a private headless backend with cleared env and print a per-receipt host-impact delta; a receipt with `delta>0` is red, not a footnote |

### Operator proposals explicitly out of lane rule scope (listed, no action implied)

Daily-pass / operator-side items (metrics trend lines, hold-unblock briefs, commit-list caps, reflection readers) live in the operator's own loop; several were already acted on (10-23 proposal 3 → mined in round 32, `corpus/lessons/round-32.md:118-126`). The standing open debts they track — R15-V1 host remediation, PR #1, SHONEN `[~]`, tripwire H2 (`fleet .ufo/l0-questions.md:103`), the r28/r29 L0 pair (`.ufo/l0-questions.md:133-135`) — are operator-owned and correctly not in QUALITY/SKILL.

## 2. Embedded operator directives in lesson files

Swept all 43 `corpus/lessons/*.md` for ruling-shaped operator mentions. Beyond the three rows above, the remaining mentions are bookkeeping ("operator-owned" dispositions, L0 routing, wrap-up prohibitions) already enforced by PROTOCOL/driver mechanics — the round-16 wrap-up prohibition is even quoted inside `SKILL.md:39-45`. None carries an unabsorbed rule.

## 3. Bottom line

- Literal `operator-*.md`: **0 files — nothing to score.** If upstream intends to land operator teachings under that glob, section 1's table shape is the scoring rubric to reuse.
- Of the ~20 substantive teachings in `considerthese/` plus embedded rulings: **12 reflected** in QUALITY/SKILL with live pointers; **7 unreflected**, all itemized with the criterion/rule shape each would need; the rest are operator-loop items correctly outside both documents.
- Highest-value unreflected items for a future claim: the during-judgment edit ban (M25-5), the freeze-the-attack-population rule (r23 routed defect 6), and the live-session isolation rule (M26-1) — each has a real incident behind it and a mechanical check is already sketched in the incident text.
