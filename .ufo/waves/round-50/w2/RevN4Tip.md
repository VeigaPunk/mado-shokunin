# RevN4Tip — round-50 w2 FALSIFY: axis-table and evidence-pointer sanity at the tip

Attack rev: `b4a79843cc2545bbe800db9322e58f6e00436629` (landed tip). Base: `8ae47b957034ae21012bbf09173cca2c48be345e`.
Method: read-only `git clone -q --shared` of the lane under `/fast/scratch/hyaku/mado-r50/RevN4Tip/lane`; every command run
against the clone with explicit rev; TMPDIR under my scratch. No lane/fleet writes; no host state touched.
Evidence files in this seat dir: `axis-at-tip.txt`, `index-base-vs-tip.txt`, `path-check.txt`, `frozen-sha256-at-tip.txt`, `commit-range.txt`.

## Verdict lines

**(a) Axis command at the tip — FAIL: navigation STALE (mismatched=1, exit=1).** The tip form does NOT print MATCH for
all 3 axes; it names the mismatch. Re-ran the `receipts/axis-base.txt` command form
(`python3 -I quality/check-axis-scores.py --repo <clone> --rev b4a79843…`):
`navigation published=65/65 derived=66/66 verdict=STALE`; `calibration 86/86 MATCH`; `operability 12/12 MATCH`;
`MADO_AXIS: checked=3 mismatched=1 rev=b4a79843…`, exit 1 (`axis-at-tip.txt`). Root cause: the round's C1 data commit
`906178b6` added the indexed knowledge entry `corpus/knowledge/hyprland-bind-key-match-r50.md`, so
`quality/check-index.py` derives `indexed=66/66` at the tip vs `65/65` at base (`index-base-vs-tip.txt`), but the last
axis publication in SCORECARD.md (line 2722, `Axis table re-derived at e5d0130d… navigation 65/65`) predates the round
and no Round-50 SCORECARD section / re-publication exists at the tip. The claims.md premise ("published axis table sits
tied at its maximum at base") held at base only; at the landed tip the lane's own calibration gate is red. The tip
integration commit `b4a79843` (wave-done receipts) did not re-derive the axis table.

**(b) Cited-path resolution at the tip — PASS with one broken lane citation and one declared forward pointer.**
Extracted every path token from `corpus/lessons/round-50.md` and `.ufo/waves/round-50/registration.md` (at the tip) and
tested each with `git cat-file -e b4a79843:<path>`; second pass for prefix-less seat-artifact tokens
(`full log: path-check.txt`). Result: 49/49 substantive citations resolve, except:
- **BROKEN (dead evidence pointer):** `scripts/sources-census.sh:618-624`, cited in `corpus/lessons/round-50.md` (M50-3
  evidence). No `scripts/` tree exists anywhere in the lane at the tip; the file exists only at the fleet root
  (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, verified present). From the lane root the citation is dead.
- **FORWARD POINTER (not a defect, does not resolve at attack rev):** `.ufo/waves/round-50/w2/ScoutAssimQuarantine/` —
  the `w2/` tree does not exist at the tip; the lesson itself declares these hand-checks as wave-w2 work.
- **EXTERNAL (expected outside-lane):** `merge/mado/`, `MERGE-REPORT.md` — staged shokuknow checkout, read-only.
- Seat citations `w1/CritC1Args`, `w1/RevC1Counter`, `w1/ExecCounterC1R50`, `w1/ExecCounterC2R50`, `w1/ExecGateV3`,
  `w1/ExecDoNothing`, `w1/ExecHostGuardR50`, `w1/ScrQualityR50`, `w1/SentScratch`, `w1/ExecWaveDone`, `w1/ScoutCensus.md`,
  `make-w1-spec.py`, `ScrRowsR50/verify-quotes.sh`, `quotes-verified.txt`, `ExecFetchR50/cmp-verify.txt`,
  `ExecFetchR50/rows-digest-binding.txt` all resolve under `.ufo/waves/round-50/`.
Frozen-artifact integrity at the tip: all 7 sha256 values named in registration's freeze table match the blobs at
`b4a79843` exactly (`frozen-sha256-at-tip.txt`), incl. `tools/mado-hostguard.py` = `fdaa5c2e…` and the v3 gate
`quality/check-session-material.py` = `ffdc9d62…`. The pins dir `.ufo/waves/round-50/fetch/` holds exactly 16 files
incl. `binds-live-r50.txt` and `SHA256SUMS`, as claimed.

**(c) tools/README/ledger consistency — PASS; no inventory file exists to contradict.** `tools/mado-hostguard.py` and
`tools/mado-keysym.py` are both present at the tip (`git ls-tree tools/`). No `tools/README.md` exists, and README.md
mentions neither tool (0 hits) — there is no per-directory inventory; the only ledger-style mentions are consistent:
registration.md names hostguard with its sha256 (matches, see b); lesson round-50 names `tools/mado-keysym.py` as the
judge program (S357/S358); SCORECARD.md:2730-2743 and LOG.md:2547 record mado-keysym.py as the round-49 capability.
Nothing claims a tool that is absent, and both present tools are where the freeze/lesson say they are.

**(d) Commit range `8ae47b95…b4a79843` — exactly the round's 7 commits, no foreign commits** (`commit-range.txt`),
newest first:
1. `b4a79843` round-50: wave-done gate integration receipts (r49 OK, r50 OK at 8dbbf61a)
2. `8dbbf61a` round-50: restore w1-results.json agent field (seat role) from w1-dispatch.json after run-9 wrap-up nulling; lossy record now contract-valid (output null + note)
3. `470bfd77` round-50: freeze (registration, frozen-counter receipts at 906178b6, do-nothing controls, wave-done/state-cite receipts)
4. `906178b6` round-50: C1 data (bind key match entry, rows S352-S363, pins, live receipt) + C2 data (session-material gate v3) + wave-done/state-cite/deliverables instruments + hostguard + QUALITY 100-102 + lesson
5. `d7c33df8` hyaku run9 wrap-up: round-50 counter drafts for inheritance
6. `1b37a59e` hyaku run9 wrap-up: round-49/50 wave state for inheritance
7. `13631f24` round-50: claims declared (C1 bind key match entry, C2 session-material gate v3) + round-start receipts

All four freeze-named commits are present (claims `13631f24`, data `906178b6`, freeze `470bfd77`, repair `8dbbf61a`);
`1b37a59e`/`d7c33df8` are the run-9 wrap-up inheritance commits on the round's own timeline; the tip is the wave-done
integration. No out-of-round commit is in the range.

## Findings (severity order)

1. **(a) HIGH — the lane's calibration gate fails at the landed tip.** `quality/check-axis-scores.py` at `b4a79843`
   reports `navigation published=65/65 derived=66/66 verdict=STALE`, `checked=3 mismatched=1`, exit 1: the round indexed
   a new knowledge entry (66/66) but never re-published the axis table (still 65/65 from round 49). Attacks the round's
   honesty about its own gate state at the tip; the L1 should note the axis table as stale in the round report or
   re-derive it at integration.
2. **(b) LOW — dead evidence pointer in the committed lesson.** `corpus/lessons/round-50.md` (M50-3) cites
   `scripts/sources-census.sh:618-624`, which does not exist in the lane at the tip (fleet-root-only path).

## Residual risk / verification gaps

- The axis STALE verdict depends on `check-index.py` counting the new entry as navigation-grounded; I confirmed the
  count change 65→66 and the added file (`corpus/knowledge/hyprland-bind-key-match-r50.md`, +135 lines in
  `git diff --stat base..tip`) but did not enumerate all 66 index rows.
- Path extraction was regex-based over the two named files; prose mentions without path shape (bare seat names in
  parentheses) were checked only for the ones carrying an artifact reference.
- No counters were re-scored (out of scope for this seat); the findings are independent of C1/C2 admission.

No tools were installed or upgraded for this seat (nothing new needed; git + python3 only).
