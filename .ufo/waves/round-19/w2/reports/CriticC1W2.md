# CriticC1W2 — partial

Ruling. The C1 count of 18/26 → 20/28 reproduces. Both new criteria have a real red at `9c54c56` and a green at the tip when re-run. The missed pre-registered target (≥21/29) is stated honestly in the lesson. The rise is only partly discernment:

- 27's alias arm is new discernment.
- 27's per-fetch arm attributes an existing `fetch-verify.py` CONFLICT to a row.
- 28's checker is the C2 counter under another name.

Both checkers stay green on mutants that break their own criterion text. No committed receipt carries the 27/28 red/green or the C1 "after" value. That is the R18-V2 pattern this round recorded, now applied to criteria 27 and 28 themselves.

Axes: (a) count reproduces; (b) red real at `9c54c56`; (c) green at tip by re-run; (d) discernment beyond the counter: new red, independence from C2, mutant survival; (e) honesty of the miss and receipt binding (criterion 24).

## 1. Re-run (read-only, lane tree = tip `01b8094`)

| command | output | exit |
|---|---|---|
| `python3 .ufo/waves/round-17/measure.py 9c54c56` | `c1 {criteria 26, lesson_cited 18, score 6.9231}` | 0 |
| `python3 .ufo/waves/round-17/measure.py 01b80946…` | `c1 {criteria 28, lesson_cited 20, score 7.1429}` | 0 |
| `python3 -I .ufo/waves/round-19/anchor-durability.py 9c54c56` | `FLAGGED S084 S094` (S094 `PER_FETCH_DIGEST — 5 distinct 200 digests … matched by credited digest 50c1ac25…`), `receipt_files=49` | 1 |
| same, `df84807` / `01b8094` | `mined=81 durable=81 … flagged=0`, `receipt_files=57` | 0 / 0 |
| `python3 -I .ufo/waves/round-19/supersede-sweep.py 9c54c56` | `files=13 pointed=2 stale=11` | 1 |
| same, `df84807` / `01b8094` | `files=13 pointed=13 stale=0` | 0 / 0 |

Producer bytes:
- `anchor-durability.py` is `9e66dce8…` at both `df84807` and `01b8094`, and the worktree is equal.
- `supersede-sweep.py` is `fd7c31df…`; the ledger is `87644b58…`.
- Neither tool exists at `17661e0`. `git show` failed there, so the `e3b0c442…` I got is the empty-input digest, not a value.
- Both tools first appear at `df84807` (`git log --diff-filter=A`).

Other checks:
- QUALITY is append-only: `git diff 9c54c56 01b8094 -- corpus/QUALITY.md` has no `-` body lines.
- `lessons/round-19.md` (with `## Mistakes`) lands in the same commit as criteria 27/28 (`01b8094`), so criterion 8 is satisfied.
- The cited `R18-V1/V3/V4` tokens exist in `round-18-verifier-spotcheck.md`.
- Arithmetic: 20/28 = 7.1429, +0.2198 over 6.9231; the target 21/29 = 7.2414 is not met.

Verdict on (a)–(c): **holds.**
- The 9c54c56 reds rest on 49 receipt files already committed at 9c54c56. They are not self-made.
- The S094 rotation (5 distinct 200 digests) and the 11 stale walker files are real defects in baseline bytes.

## 2. Counterexamples (scratch clone `/tmp/c1w2`, mutant commits only there)

**F1 — no committed receipt for the 27/28 red/green or for C1 = 20/28 (criterion 24 applied to the round's own criteria; same class as R18-V2).**
- `corpus/QUALITY.md:178-180` states "Red at `9c54c56`: `FLAGGED S084 S094` … exit 1. Green at `df84807`: `flagged=0`".
- `:187-188` states the same for supersede-sweep.
- Neither cites a receipt. `git grep -l -E "tool=\S*(anchor-durability|supersede-sweep)|…tool_sha256" 01b8094` → no match (rc=1).
- `.ufo/waves/round-19/evidence/` at tip holds only `census-before`, `fresh-pins-before(-recut)`, `gate-swap-*`, `measure-before.json.txt` and `tw-recall-before(-recut)`. It has no `measure-after` and no anchor or sweep receipt.
- `receipt-claims.json` has no claim for criteria 27 or 28.
- By contrast, criterion 24's own green arm cites `receipt-check` `EXPECT_SUMMARY 21/21` (`QUALITY.md:159-161`).
- My re-run agrees with the narrated values, so this is a **binding defect, not a false value**. It is fixable.

**F2 — criterion 28's checker equals the C2 counter and does not guard the round's other two supersessions.**
- The ledger `.ufo/waves/round-19/supersessions.json` holds exactly one entry: `walker-2.17.2`, rows S090/S096. That is the C2 set.
- Round 19 itself superseded S094→S097 and S084→S098 (`lessons/round-19.md:45-49`), and neither is in the ledger.
- Mutant A2 (`/tmp/c1w2` `1c2df58`):
  - deletes the S094→S097 pointer (`theme-route-r18.md:167`) and the S084→S098 pointer (`walker-route-r18.md:327`);
  - reverts both head `source:` tokens to the rejected rows (S094 ×2 and S084 ×2 now on line 1).
- `theme-route-r18.md:158,162` and `walker-route-r18.md:33` (`docs.rs/xdg/latest/…`) then state the superseded values with no pointer. That breaks criterion 28's text.
- Result: `supersede-sweep.py HEAD` → `pointed=13 stale=0`, exit 0; `anchor-durability.py HEAD` → `flagged=0`, exit 0.
- So 28's green arm is the C2 movement re-read. It is not independent evidence for C1. This is the w1 finding, still open; the QUALITY limit at `:188-190` covers only file granularity.

**F3 — criterion 27's checker clears rows that its own text rejects.** All runs use the committed `9e66dce8…` copy at `/tmp/c1w2-ad.py`.

| mutant | change | result | criterion-27 reading |
|---|---|---|---|
| B1 (on `9c54c56`) | S084 anchor gains "(the crate walker 2.17.0 calls)" | `S084 durable — alias segment latest pinned by version 2.17.0` | a different project's version, and the superseded old value, counts as a pin (`TAG_RE` matches any `N.N` anywhere in the anchor, lines 78/126-128) |
| B2 (on `9c54c56`) | S084 URL `docs.rs/xdg/latest/…` → `docs.rs/xdg/*/…` (docs.rs's semver-latest alias) | `durable — … page digest, not shown to rotate`, exit 0 | the alias check is spelling-bound (`ALIAS_SEGMENTS`, line 70) |
| C (on tip) | S098 anchor reduced to `extracted src/base_directories.rs:446-457`, with no checksum and no commit | `S098 durable — no alias segment and no digest credited`, exit 0 | the "registry checksum / content id" clause has no checker arm |

At the real tip, `S032 S033 S034 S035` (status `mined`, used by `xdg-portal-routing-r12.md`) are anchored only by section names plus "accessed 2026-10-19". The checker prints `durable — no assigned class fired; anchor dates the access`. None of these is "tag/commit-pinned bytes with sha256, a content-addressed id, or a registry checksum".

So "Green at `df84807`: flagged=0" is a checker green, not "criterion 27 holds". The disclosed limit (`QUALITY.md:181-182`, "cannot tell a reproducible page that has never been fetched twice") does not name:
- that the token `durable` means "unflagged";
- the any-`N.N` pin;
- the missing positive arm.

This is criterion-23-style token precision. A future sentence citing "durable=81" as reproducibility would overclaim.

**F4 — honesty of the miss: holds.**
- `corpus/lessons/round-19.md:62-63`: "QUALITY: 27 and 28 only; R18-V2 recorded as an application of 24 (CriticC1). C1 therefore misses its pre-registered ≥21/29 target."
- R18-V2 is recorded un-numbered at `QUALITY.md:192-204`, as w1 CriticC1 advised. Folding it was correct, because 24's own checker already gives the red (`MISSING_PROVENANCE`).
- The tip has no SCORECARD round-19 results row and no LOG round-19 entry (`git grep 20/28` outside reports → none), so the final wording is [UNK].
- The fraction rises with any appended cited line while it is below 1. The counter alone cannot show discernment; the discernment judgement above is the evidence.

## 3. Discernment ledger

| criterion | new red that no existing check produced at `9c54c56` | independent of C2/C3 | mutant survivors |
|---|---|---|---|
| 27 alias arm | yes: S084 (fetch-verify credits it, w1 CriticC1) | yes | B1, B2 |
| 27 per-fetch arm | partial: `fetch-verify.py` already exits 1 with CONFLICT on the tree URL; new is only the row attribution (lesson M1 "captured-by" admits this) | yes | none found; deleting the digest yields a content-id row, which the criterion permits |
| 27 positive clause | not checked | — | C; real S032-S035 |
| 28 | yes: 11 stale (the PROTOCOL rule had no check) | **no**: the ledger is the C2 set | A2; w1's file-level mutant `48012dad` |

Net: +2 is about one criterion's worth of new discernment (27 alias plus row attribution), and one criterion that turns the C2 counter into a check.

## 4. Smallest safe corrections (none change a counter)

1. Cut header-bound receipts and add them to `receipt-claims.json`:
   - anchor-durability at `9c54c56` (red) and `01b8094` (green);
   - supersede-sweep at the same two revisions;
   - `measure.py` c1 at `01b8094`.

   Then reference them in an append-only line under 27/28. The SCORECARD results row cites `measure-after` before stating 20/28.
2. Add append-only limits under 27:
   - `durable` means "no class fired";
   - any `N.N`, date or 40-hex anywhere in the anchor clears an alias (B1);
   - only the literal alias tokens are recognised (B2);
   - no registry-checksum or content-id arm exists (C);
   - S032-S035 pass unflagged.
3. Ledger the S094→S097 and S084→S098 supersessions in `supersessions.json`, or state under 28 that its checker covers only the walker-pin entry and that its green is the C2 counter (A2).
4. SCORECARD results: C1 20/28 = 7.1429 (+0.2198), target ≥21/29 **missed**. State that 28's green is not independent of C2.

## Limits

- I did not run the gate, any selftest, `fetch-verify.py`, `receipt-check.py`, the tripwire or the frozen tools. The fetch-verify overlap is taken from w1 `CriticC1.md`, not re-run [UNK at tip].
- Mutants exist only in `/tmp/c1w2` (branches `mut` = `82670a7`, `1c2df58`; `mutB` = `4e3865f` B1, `a15be7d` B2; `mutC` = `b81b350`). The checker copy is `/tmp/c1w2-ad.py` (`9e66dce8…`).
- No network fetch. Whether `docs.rs/xdg/*/` serves the same bytes as `latest` is [INFERENCE] from docs.rs's documented semver alias; it is not measured.
- Whether S016/S017/S029/S031 "page modified" dates satisfy CORPUS.md's "publication date" is left to w1's concession; I did not re-litigate it.
- The final SCORECARD/LOG wording of C1 is not yet committed [UNK].

## Installs

none
