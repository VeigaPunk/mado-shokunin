# RcArtifactOnlyAssessmentIn1464 — C2 ledger attack on CapArtifactOnlyAssessmentIn1464 (a3w1)

Independent re-derivation of the a3w1 ledger line for SCORECARD.md:1464 at base
`41cc04c8d593837a0d5078bffaacdaa163d12897`. Reviewed report:
`.ufo/waves/round-25/a3w1/reports/CapArtifactOnlyAssessmentIn1464.md`. Own sandbox clone at
`/fast/scratch/hyaku/mado-r25a3/rc/CapArtifactOnlyAssessmentIn1464` (cloned with `GIT_DIR`/`GIT_WORK_TREE`/
`GIT_INDEX_FILE` unset via `env -u`, detached at `41cc04c8`, deleted after verification). No lane/fleet git/jj
writes; no installs; no `hyprctl`; all started processes finished.

## Commands run (own re-run)

```
mkdir -p /fast/scratch/hyaku/mado-r25a3/rc
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin \
  /fast/scratch/hyaku/mado-r25a3/rc/CapArtifactOnlyAssessmentIn1464
cd /fast/scratch/hyaku/mado-r25a3/rc/CapArtifactOnlyAssessmentIn1464
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git checkout -q --detach 41cc04c8
git rev-parse HEAD          -> 41cc04c8d593837a0d5078bffaacdaa163d12897
git status --porcelain      -> empty (0 lines)
sha256sum tools/mado-assessment.py -> 66aefd03f25d834fbfcfee6b295c1c032f01b2a94ca321396b7558cca59de9d4
PYTHONDONTWRITEBYTECODE=1 timeout 600 prlimit --as=4000000000 python3 -I tools/mado-assessment.py \
  --selftest .ufo/waves/round-21/assessment-fixtures > run1.txt 2>run1.err   -> exit=0
(same again) -> run2.txt                                                     -> exit=0
```

## Independent re-derived ledger line

| SCORECARD.md:1464 | artifact-only assessment integrity | Validate declared chronology/order, input/expectation hashes, historical rejection disclosure, four canonical SHONEN subjects, without C1; distinguish clean/failed/could-not-evaluate | observed at `41cc04c8`: **works** — exit 0, `pass=20 total=20 code=0 result=selftest finding_ids=["assessment_oracle_match"]`, `tool_sha256=66aefd03…`, `seal_sha256=99516c34…`, stdout 9,225 B single line `sha256:1e58c91ba5a5f6c84f4e2619cab4453b691604d38bdef1465a5def86c11ede98`, two runs byte-identical, stderr 0 B | `cd <sandbox> && PYTHONDONTWRITEBYTECODE=1 timeout 600 prlimit --as=4000000000 python3 -I tools/mado-assessment.py --selftest .ufo/waves/round-21/assessment-fixtures` | `:1586` round-24 status table `works` at `8e5d9369`; `:1570` declares that table supersedes earlier implied `works`; `:1472` C2 disposition bounds it ("improved… bounded capability; round admission remains false"), consistent — it bounds admission, not the demonstrated behavior |

## Per-case re-derivation (my own parse of run1.txt)

All 20 cases `pass=true`, `got` matches `want` in every case. Case ids, exits, results and finding ids are
byte-for-byte identical to the report's §C table (verified line by line, including `baseline_valid`/`clean`,
three `history_*`/`historical_target_rewritten`, `shonen_x_with_named_nonauthor`/`clean`,
`round20_wrong_topic_shonen`/`wrong_topic_shonen`, `round20_canonical_shonen_corrected`/`clean`).

## Findings

1. **F1 (trivial, arithmetic slip):** report §C "Derived per-case view" counts the want-level classes as
   "3 clean, 9 failed, 8 could-not-evaluate". My own `Counter` over the run's `want.result` gives
   **3 clean, 10 failed, 7 could-not-evaluate** (and identically over `got.result`). The report's own per-case
   table immediately below the sentence lists 10 `failed` and 7 `could-not-evaluate`, so the table is right and
   the summary sentence is an off-by-one transcription slip. Cosmetic; does not change the ledger line.
2. Everything else reproduces exactly:
   - Row location and content at `41cc04c8`: `:1460` heading `### Capabilities demonstrated this round` (round 21),
     `:1462` header, `:1464` row, command `python3 -I tools/mado-assessment.py --selftest
     .ufo/waves/round-21/assessment-fixtures`, first-working round `21` — verbatim match.
   - Revision: sandbox HEAD `41cc04c8d593837a0d5078bffaacdaa163d12897`, porcelain clean; tool sha256
     `66aefd03…` equals the round-21 measured value quoted at `SCORECARD.md:1446` and the `gate_sha256` key
     inside `assessment-independence-a6cef89.json`.
   - Key output: exit 0; stdout one 9,225-byte JSON line; `sha256:1e58c91b…1ede98`; `code=0 result=selftest
     pass=20 total=20 finding_ids=["assessment_oracle_match"] tool_sha256=66aefd03… seal_sha256=99516c34…`;
     two runs byte-identical; stderr empty. Byte-identical to the report's claims.
   - Evidence-pointer receipts: all four `.ufo/waves/round-21/evidence/final/assessment-{delivered,
     independence,mutation,na}-a6cef89.json` present at `41cc04c8` (`git cat-file -e`).
   - Superseding pointers: `:1570` supersession sentence and `:1586` round-24 `works` row verified verbatim;
     `:1472` C2 disposition verified verbatim (bounds admission, does not contradict the row's technical claim).
     No later text at `41cc04c8` reports this capability failing/removed.
3. **No copied-not-run evidence:** the report's verbatim stdout head, byte count, sha256 and case table all
   match a fresh execution I performed myself; claim of two byte-identical runs is plausible and reproduced
   (my two runs are also byte-identical). The reported wall time (0.984 s) is plausible (my runs <1 s each).
4. **No wrong revision, no overclaim on the row itself:** the report correctly scopes the claim to `41cc04c8`,
   explicitly disclaims re-executing independence/mutation runners and says nothing about tip behavior.
5. Residual caveat (inherited, not a defect of this report): the row's `works` is a fixture-suite fact; the
   report itself notes this and the row's own text disclaims authentication/evidence sufficiency.

## Cleanup

`rm -rf /fast/scratch/hyaku/mado-r25a3/rc/CapArtifactOnlyAssessmentIn1464` — clone deleted (verified by `ls`;
only sibling seats' clones and my `run{1,2}.{txt,err}` receipts remain). `pgrep -af
'mado-assessment|CapArtifactOnlyAssessmentIn1464'` -> no match.

## Verdict

RECHECK CapArtifactOnlyAssessmentIn1464: agree — works status, exit 0, 9,225 B stdout `sha256:1e58c91b…1ede98`,
pass=20/20, command form and `:1586`/`:1570` superseding pointers all reproduce at `41cc04c8`; one trivial
arithmetic slip (want-class counts "9 failed, 8 could-not-evaluate" should be 10/7) that does not affect the
ledger line.
