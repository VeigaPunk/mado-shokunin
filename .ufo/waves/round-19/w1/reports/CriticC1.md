# CriticC1 — 27 adds partial discernment but its checker is inverted, 28 restates PROTOCOL with a new but gameable check, 29 repeats 24 and inflates the count

Scope: the planned C1 criteria 27–29. The SCORECARD tail (`SCORECARD.md:1092-1098`) only says "append-only lesson-cited QUALITY criteria … target ≥ 21/29". The criterion bodies come from the QualityDraft item in `.ufo/waves/round-19/w1/spec.json`:
27 durable anchors, 28 supersession sweep, 29 self-application. All reads below are at
`9c54c56a6a7528675027b7f628f97a1b8d1b8e8d` unless a different revision is named. For tool runs I used a scratch clone
`/tmp/criticc1-r19`, checked out at 9c54c56. No lane git or jj write was made.

Axes used for this critique: (a) **discernment**: does the check give a red on a real 9c54c56 artifact that no existing check already gives? (b) **restatement / duplicate authority** against QUALITY 6/7/9/13/16/23/24/25 and the fleet `PROTOCOL.md`; (c) **red reality**; (d) **gameability / survivors**; (e) **C1–C2 independence**.

## 0. The counter cannot tell discernment from inflation

`measure.py` c1 (`.ufo/waves/round-17/measure.py:84-93`, instrument `de4c422b…`) counts any `^N\. .*lessons/` line. It never checks that the cited lesson exists or that the criterion has a red. Baseline: `{'criteria': 26, 'lesson_cited': 18, 'score': 6.9231}` (run at 9c54c56).

- Appending any lesson-cited line raises the fraction while it is below 1. So the move from 18/26 to 21/29 tells you nothing about discernment on its own.
- `corpus/lessons/round-19.md` does not exist at the pre-registration commit: `git cat-file -e 17661e0:corpus/lessons/round-19.md` gives `fatal: … does not exist`. The new citations dangle unless the lesson lands in the same commit, which is criterion 8's landedness rule. The c1 counter would still credit them.
- **Gate L1 should apply** (from criterion 25's logic): a new criterion counts as discernment only if its red on 9c54c56 is not already produced by an existing committed check on the same artifact.

## 1. Criterion 27 — durable anchors (R18-V1 S094, R18-V4 S084)

**Restatement of 7/9/13/23/24? No.** Those criteria bind *lane* artifacts and receipts to commits and producers. Criterion 27 is about whether *external* source bytes can be reproduced. The real overlaps are elsewhere:

- QUALITY 6 (`QUALITY.md:12`): "pinned value … named revision".
- QUALITY 16 (`:22`): upstream docs only as dated `[INF-docs]`.
- Most of all, the round-18 lesson M7 (`corpus/lessons/round-18.md:22`). It already names `fetch-verify.py`'s CONFLICT rule as the fix for S094.

**Red that already exists at 9c54c56 (duplicate authority for the per-fetch arm).** I ran `python3 -I .ufo/waves/round-18/fetch-verify.py --sources corpus/SOURCES.md --rows S063,S064,S084,S094,S076` in the clone (fetch-verify sha `07e7ac74…`):
- 4 `CONFLICT` URLs (`…/omarchy/tree/v3.8.4/themes/matte-black` has 5 distinct digests, including the S094 anchor `50c1ac25…`), `exit=1`.
- Yet `ROW S094 receipted`, `ROW S084 receipted`, `ROW S063 receipted`, `ROW S064 receipted`.

So S094's per-fetch red is **not new**. The only real gap in the existing tool is that it does not attribute a CONFLICT digest that a row's anchor cites back to that row. That is a small fix to fetch-verify, not a second tool. The S084 alias red **is new**: no existing check rejects it, and fetch-verify credits it.

**Reproducibility, measured today.** Receipts are in `.ufo/waves/round-19/fetch/CriticC1/receipts.jsonl` (4 lines):
- `docs.rs/xdg/latest/…BaseDirectories.html` fetched twice → 200, 105,537 B, `0291cfe6…` both times. That equals the S084 anchor and 4 committed round-18 receipts (`0291cfe6…` at 15:41, 16:00, 16:00, 16:01Z).
- `wiki.hypr.land/Hypr-Ecosystem/hypridle/` fetched twice → 200, 254,750 B, `b45c03dc…` both times. That equals the S063 anchor and its committed receipt.
- So docs.rs and wiki HTML are **byte-stable**. "Docs site / *.html ⇒ per-fetch" is a false class. S084's defect is the alias only (the `latest` page `0291cfe6…` ≠ the pinned `/3.0.0/` page `adaec7c3…` in committed receipts). The per-fetch class holds for GitHub tree pages.

**Strongest counterexample: the drafted checker is inverted.** I ran `anchor-durability.py` (worktree sha `6b100e87…`, uncommitted) as `python3 -I .ufo/waves/round-19/anchor-durability.py 9c54c56`:

| Rows | Output | Problem |
|---|---|---|
| S094 | `PER_FETCH_DIGEST` | correct, via the receipt join, because the S094 row text holds no tree URL |
| S084 | `UNPINNED_ALIAS` | correct |
| S063, S064 | `PER_FETCH_DIGEST` | wrong: their digest is reproduced by 3 fetches |
| S016, S017, S029, S031, S032 (`--rows`) | `durable — no digest credited to a page and no alias segment` | same unversioned "Latest git" wiki class as S063, but with **no** digest at all |

So a row with *less* evidence passes and a row with a reproducible digest fails. The cheapest way to green S063 or S064 would be to delete its digest. This is a vacuous/perverse arm. The URL-token alias regex (`latest|main|master|HEAD`) also lets every unversioned wiki URL through: the S063 row itself says "not version-pinned to v0.1.8". `S005 … blob/main` passes only by "pinned by date 2026-01-16".

**Verdict on 27:** a real discernment gain for the alias arm (S084 is a real red no existing check produced). The per-fetch arm repeats fetch-verify / round-18 M7. As drafted, the check gives wrong labels and rewards digest removal.

**Smallest safe correction:**
- Print `durable` only on a positive token: a tag- or commit-pinned URL plus sha256, a registry checksum, or a content id.
- Give digestless page rows their own non-durable label, or scope the criterion text explicitly to digest-credited rows and say that digestless docs rows fall under QUALITY 16.
- Print `PER_FETCH_DIGEST` only when receipts hold ≥2 distinct 200 digests for a URL whose digest the row cites. That is fetch-verify's CONFLICT rule joined by digest, ideally a `--rows` attribution fix inside fetch-verify itself.
- Label a stable page digest on an unversioned page `UNPINNED`.
- Declare the honest 9c54c56 red set before the green arm: {S084, S094} plus S063/S064 (unpinned), with the wiki rows scoped by a stated rule, never by id. Otherwise the green arm needs S063/S064 supersession, which was never declared.

I sent this to `MadoR19.AnchorDurability`.

## 2. Criterion 28 — supersession sweep (R18-V3)

**Restatement of 7/9/13/23/24? No.** It **restates the fleet rule** at `/home/vgpnk/Projects/shokunin/PROTOCOL.md:363` ("**Corrections sweep every mention.** … a corrected fact left standing in a sibling file is still a defect"). The spot-check itself cites this rule (`round-18-verifier-spotcheck.md:119`). It also overlaps QUALITY 6 ("corrections preserving old and new values").

What is new is only the runnable check. That is legitimate calibration: the rule existed in PROTOCOL with no check, and the round-18 fix stopped at the SKILL erratum.

**Red is real.** `supersede-sweep.py 9c54c56 --ledger supersessions.json` (sha `fd7c31df…`, ledger `87644b58…`) → `files=13 pointed=2 stale=11`, exit 1.

**Counterexample (gameability).** In the clone I made commit `48012dad`, which appends the line `# S096 2.17.2` to the 11 stale files and changes nothing else:
- `fresh-pins.py` gives **13/13**.
- `supersede-sweep.py` gives `pointed=13 stale=0`.
- Meanwhile `git grep -c 2.17.0` still shows SKILL.md 8, walker-deep-r9.md 10, tools/mado-verify.sh 4 unannotated present-tense mentions. The gate pin is unchanged, yet the gate file counts as current.
- The rule is file-granular; PROTOCOL says "every mention". Baseline credit is also partly incidental: `corpus/README.md:44` is a table row about walker-route-r18 that holds `2.17.2 S072 S091`; README's actual old-value line is `:135`.

SupersedeSweep measured the strict variant (old AND new AND row on one line): **13 STALE** at 17661e0 and 9c54c56. I also measured it: 0/13 pass at 9c54c56 and on the mutant. Its ledger rows already reject an unrelated row token (S999 stays STALE). So the gaming needs a real superseding row cited without naming the old value.

**C1/C2 independence (axis e).** The 28 check and the C2 counter (`fresh-pins.py`) are "the same set by construction" (SupersedeSweep item). One repair sets 28 green **and** moves C2 from 2/13 to 13/13. The SCORECARD "Separable" sentence (`:1113-1114`) holds only at counter level. Criterion 28's green arm is not independent evidence for C1.

**Verdict on 28:** promotes an existing PROTOCOL rule into a check and shows a real red. That is a modest discernment gain, not inflation. But its green can be met without sweeping a single mention.

**Smallest correction (L1's choice; no counter change, because C2 is pre-registered):**
- Either word the criterion as "file-level sweep completeness" and record the `48012dad` mutant as a known limit;
- or adopt the strict line rule for the new, unfrozen supersede-sweep and restate its red as 13/13.

In both cases the ledger is hand-written, so the check catches only supersessions somebody has already logged. A completeness arm tying ledger entries to SOURCES superseding rows (S097→S094, S098→S084) would close the round-18 failure mode itself.

## 3. Criterion 29 — self-application (R18-V2)

**This is a restatement of 24 (with 13 and 25).** Evidence:
- QUALITY's own round-18 preamble (`QUALITY.md:126-130`) says criteria 7/9/13/23 carry input and commit binding, and that 24 "adds only what those leave open: the identity of the *producer*".
- The round-14/15 rulings say "No duplicate provenance criterion" (`:57-61`, `:65-70`).
- Criterion 26's red-before *is* "a sentence that relies on a … selftest … receipt". That is exactly the subject of 24.

**Red already produced by 24's own unchanged checker.** I ran `python3 -I .ufo/waves/round-18/receipt-check.py /tmp/criticc1-claims.json` (checker `a2c05fe1…` at 9c54c56; it takes the claims path from `argv[1]`, `receipt-check.py:56`) with two claims at 9c54c56:

```
RECEIPT c26-redbefore MISSING_PROVENANCE
RECEIPT c26-regression-recut MISSING_PROVENANCE
EXPECT_SUMMARY: 2/2   exit=0
```

`git show 9c54c56:…/gate-rc-redbefore.txt | grep -c 'tool_sha256=\|measured_commit='` → 0.

The defect was also already recorded at 9c54c56 in the SCORECARD append correction (`SCORECARD.md:1037-1046`: "lack that header … they are provenance only"). It was a gap in the claims file, `.ufo/waves/round-18/receipt-claims.json`, which has no gate-rc entry. It was not a missing rule.

29's only new words are "before the criterion is counted as shown able to fail". These change nothing measurable: `measure.py` c1 reads no evidence, and the instrument stays `de4c422b…` by declaration.

**Verdict on 29:** count inflation (+1 numerator, zero new red). LessonDraft M4 says the same thing ("criterion 24 … fails on its sibling").

**Smallest correction:** do what rounds 14 and 15 did:
- an application paragraph ("R18-V2 applies existing criterion 24 …") with no new number;
- the round-19 `receipt-claims.json` red claims;
- the GateSwapReceipt header-bound re-cut.

## 4. Honest outcomes for C1

| Plan | c1 | Note |
|---|---|---|
| 27 + 28 + 29 as drafted | 21/29 = 7.2414 | 29 is inflation; 27's checker is inverted |
| 27 (corrected) + 28, 29 as an application note | 20/28 = 7.1429 | still above 6.9231; the declared target ≥21/29 is missed, which must be reported as missed |
| Splitting 27 into per-fetch and alias criteria | 21/29 | the two are genuinely distinct classes (measured: S084 is stable, S094 rotates), but the per-fetch red already exists in fetch-verify, so a separate number for it is a tradeoff for L1, not a free gain |

## Limits

- I did not run the gate, any selftest, `frozen-repin.py`, `landed-check.sh`, `gate-swap.sh` or the tripwire tool.
- The sibling checkers are uncommitted worktree bytes (shas above). Their verdicts may change after this report.
- I did not read QualityDraft.md (not present in `drafts/` when I checked). The criterion texts are taken from the spec.json item prompt.
- I did not test whether S016/S017/S029/S031 wiki pages are used as version-specific support: `[UNK]`; that is a semantic judgement the regex cannot make.
- "S005 date counts as pinning" is the checker's rule. I did not verify GitLab blob HTML stability.
- 2 + 2 live fetches today and 1–4 committed receipts per URL. Byte stability over a longer window is `[UNK]`.
- Scratch clone `/tmp/criticc1-r19` (mutant commit `48012dad` exists only there) and `/tmp/criticc1-claims.json` are left in place as provenance only.

## Installs

none

## Addendum — re-run at anchor-durability.py `431faab4…` (reason-only revision)

`python3 -I .ufo/waves/round-19/anchor-durability.py 9c54c56 --rows S016,S017,S029,S031,S032,S063,S064,S084,S094` (clone, exit 1):
`S016/S017/S029/S031 durable — no page digest; anchor pins date 2026-08-26`; `S032 durable — … pins date 2026-10-19`;
`S063/S064 PER_FETCH_DIGEST`; `S084 UNPINNED_ALIAS`; `S094 PER_FETCH_DIGEST … matched by path tail themes/matte-black`.

The inversion stands in substance. A page-modified date on an unversioned "Latest git" page, or an *access* date (S032), does not pin bytes or version: the next deploy changes the content under the same URL and date field. S063 is the same wiki page class, with the same "page modified 2026-08-26" in its row (scope cell) plus a digest reproduced 3×, and it is the one flagged. The criterion 27 text ("tag/commit-pinned bytes with digest, content id or registry checksum") admits none of S016–S032's anchors; the checker calls them durable. Correction unchanged: treat dates as dating, not pinning (`UNPINNED` for unversioned pages regardless of digest), or scope 27 to digest-credited rows by stated rule. The S094 hit uses a receipt path-tail match, not a digest join: it is right here, but a path-tail heuristic can bind an unrelated repo's `themes/matte-black` receipt [INFERENCE; not tested].

## Addendum 2 — anchor-durability.py `b098cf4a…`

Re-run at 9c54c56, `--rows S016,S032,S063,S064,S084,S094` (exit 1, flag set unchanged: S063 S064 S084 S094). Access dates no longer count as pins (`S032 durable — no assigned class fired; anchor dates the access, not a revision`).

- **Conceded:** the fleet contract `/home/vgpnk/Projects/shokunin/CORPUS.md:99-100` defines `anchor` revision as "version, commit, or publication date". So S016's "modified 2026-08-26" clearing is within the contract. My earlier "inversion" is a contract tradeoff, not a checker defect. The tradeoff is that a dated, unversioned page passes while a page with a digest fails. That is a decision for L1 or the contract, not something the tool should settle.
- **Residual (token precision, criterion 23 style):** the printed tokens overstate the evidence.
  - `durable` on S032 means "no class fired", not "reproducible".
  - `PER_FETCH_DIGEST` on S063/S064 asserts per-fetch bytes, but measured digests reproduce (3×, committed receipt + `fetch/CriticC1/receipts.jsonl`). The reason text was softened; the verdict token was not.
- **Smallest correction:** use neutral tokens, `unflagged` for no class and `PAGE_DIGEST` for an unversioned page digest. Reserve `PER_FETCH_DIGEST` for rows with ≥2 distinct 200 digests in receipts (S094 only at 9c54c56). If criterion 27 or the SCORECARD cites S063/S064 as "per-fetch", that sentence fails criterion 23.

## Addendum 3 — anchor-durability.py `825e0fe5…` (closes my 27 checker objection)

Re-run at 9c54c56, `--rows S032,S063,S064,S084,S094` (exit 1, FLAGGED S063 S064 S084 S094). Each page-digest reason now prints its committed receipt coverage:
- S063 and S064: `1 committed 200 record(s), 1 distinct digest(s)`.
- S084: `6 … 1 distinct`.
- S094: `5 … 5 distinct`.

S032 prints `no assigned class fired`. The per-fetch evidence is now visible on each row, so my reproducibility objection is answered at line level. The remaining item is the coarse tokens (`PER_FETCH_DIGEST` on S063/S064, `durable` as "unflagged"). Renaming them is L1's contract call. Any SCORECARD/criterion sentence should cite the coverage field, not the token, when it says "per-fetch" (criterion 23).
