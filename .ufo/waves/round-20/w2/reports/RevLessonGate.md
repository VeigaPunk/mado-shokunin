# RevLessonGate — partly falsified: Gate evidence is sound, but its registry counts omit required command/date provenance

## Findings

### Medium — Round-20 count claims do not meet the corpus count format

`/home/vgpnk/Projects/shokunin/CORPUS.md:34-38` requires any corpus count to be written as `<number> — <command> <date>`. `corpus/lessons/round-20.md:51-54` gives `Rows 98 → 112 (tier A 91 → 105; mined 81 → 95)` without a command or a date attached to those counts. The lesson's header date at line 5 does not make the counts conform to the required format. The values are correct, but the recorded claim is not reproducible as required. Include the census command(s) and date next to the counts.

Evidence (isolated clone):

```sh
git show 28c6837:corpus/SOURCES.md | awk -F'|' '/^\\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\\|/ {rows++; t=$5; gsub(/[[:space:]]/,"",t); tier[t]++; s=$9; gsub(/[[:space:]]/,"",s); status[s]++} END {printf "rows=%d",rows; for(k in tier) printf " tier.%s=%d",k,tier[k]; for(k in status) printf " status.%s=%d",k,status[k]; print ""}'
awk -F'|' '/^\\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\\|/ {rows++; t=$5; gsub(/[[:space:]]/,"",t); tier[t]++; s=$9; gsub(/[[:space:]]/,"",s); status[s]++} END {printf "rows=%d",rows; for(k in tier) printf " tier.%s=%d",k,tier[k]; for(k in status) printf " status.%s=%d",k,status[k]; print ""}' /tmp/mado-r20w2-RevLessonGate/corpus/SOURCES.md
```

Output:

```text
rows=98 tier.A=91 tier.B=1 tier.C=6 status.mined=81 status.queued=8 status.rejected=9
rows=112 tier.A=105 tier.B=1 tier.C=6 status.mined=95 status.queued=8 status.rejected=9
```

The lesson's stated deltas are therefore true; the unreported totals are unchanged: tier B 1, tier C 6, queued 8, rejected 9. Hashes: lesson `bf55c34db05e47a1499e67567df0d2a8841a4337da26c25a46a10c03e1e324e0`; current `SOURCES.md` `ff69dcc8c76f55eb1968092fa7486e53a1024c855e7249702880b2a100664b1e`; baseline `28c6837:SOURCES.md` `ccaff539b159a7c0a431f873193e7d0969bda3d0996b1debad1cc4939315b67c`.

## Checks that held

- `corpus/lessons/round-20.md:36-49` has one URL, 2026-10-20 access date, and located quote for each new row S099-S112. I checked the cited excerpts against the saved fetched source bodies; each is under the 25-word cap. The relevant `fetch/<seat>/receipts.jsonl` entries record successful source fetches dated 2026-10-20 (the CPython discovery log also records 404s for the wrong candidate path, while the accepted S105 path is a successful fetch). Examples: S099 quote at `fetch/SrcGitCommitDoc/git-commit-v2.56.0.adoc:379-381`; S110 at `fetch/SrcBashErrexit/bashref.texi:5940-5941`; S112 at `fetch/SrcUnshare/user_namespaces.7:277-280`.
- `corpus/lessons/round-20.md:51-53` accurately says no existing-row status/recheck/used-by updates occurred. The read-only diff from `28c6837` to `a4046a8216080d4004de3f268c62cf142095ac07` reports `14  0  corpus/SOURCES.md` and `99  0  corpus/lessons/round-20.md`: S099-S112 are additions only; no existing registry row was rewritten. New rows' `mined`, recheck, and used-by values match the lesson's stated additions.
- The corpus change has SHA-256 `ff69dcc8c76f55eb1968092fa7486e53a1024c855e7249702880b2a100664b1e`; the Gate's lesson SHA-256 is `bf55c34db05e47a1499e67567df0d2a8841a4337da26c25a46a10c03e1e324e0`.

## Limits

No `lsp` device is mounted (`read xd://lsp` returned “No such tool”), so LSP status/references/definitions/diagnostics were unavailable; no grep was used. I relied on the committed lesson/registry and the locally saved source bodies and fetch receipts; I did not perform fresh network fetches.

## Installs

none
