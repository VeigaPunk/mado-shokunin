# ConnPatterns — round 47 w2 report (cross-round pattern seat)

Status: COMPLETE. Findings: `.ufo/waves/round-47/w2/ConnPatterns/findings.md`; receipts:
`.ufo/waves/round-47/w2/ConnPatterns/receipts/`.

## Bottom line
Round-46 break classes vs the round-47 freeze (`d7527d608ad2b2e3cc398fdde34db7947b254a1a`):

| class (round 46) | round 47 | closed? |
|---|---|---|
| C1 ambient reference copy | minimal bwrap root; pin only in oracle runs; embed/exec controls all MISSED | yes (embedded **in-process** copy is the declared legitimate capability channel) |
| C1 deletable marker | no marker exists; strace trace outside sandbox, fail-closed | yes |
| C1 absolute-path binaries | `/usr/bin` not mounted; selftest shares sandbox PATH | yes |
| C1 inherited pipe | no in-band tripwire; clause r = external strace | yes — but trace watches `execve,execveat,socket,socketpair,connect` only; a bare fork is invisible (`readonly=ok` for a forking tool, receipt `c1-fork-runpy.txt`). No scoring consequence under the declared residual; wording gap only |
| C2 self-receipt (F7) | receipts must be absent at base → authored with data; form-only checks | only via the declared non-author closure (weaker than round-46 v2's freeze-bytes check) |
| C2 uncited pinned rows (F5d) | HELD S056-S060 protected; **new uncited rows invisible** | **no — demonstrated**: falsified uncited S339 on the pinned README URL admitted 1/1 |
| C2 indented code (F8) | no unquoted-code check | **no — demonstrated**: invented indented C++ in the entry admitted 1/1 |

## Holes found (pre-data, re-registration candidates)
1. **F5d analogue (C2):** a data revision may add uncited registry rows on pinned URLs (round-46 fix E/F absent).
   Reproduced: POS + uncited falsified S339 → `admitted=1/1` (receipt `uncited-row-s339.txt`). Draft surface:
   rows register S326-S338 while the entry head cites only S326/S327.
2. **F8 analogue (C2):** indented code in no pin is unscanned. Reproduced: POS + invented indented block →
   `admitted=1/1` (receipt `indented-code-f8.txt`). Latent (draft has no such block).
3. **Clause r fork-blindness (C1, wording only):** trace set lacks clone/fork; a pure-Python child process is not
   observed. Reproduced: fork+runpy tool → `TARGET_MET`, `readonly=ok` (receipt `c1-fork-runpy.txt`). Safe today
   because embedding is declared legitimate, but "no process" overstates what `r` enforces.

Every count above was run on this host by this seat (revs in receipts); controls and pre-existing receipts cited in
findings.md. No lane file modified; scratch `/fast/scratch/hyaku/mado-r47/ConnPatterns` deleted at finish.
