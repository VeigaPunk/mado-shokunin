# R56W3ExecWaveEvidence — attempt 2

**Attack:** wave-evidence integrity: report inventory, stopped seats, deleted leftovers, current untracked inventory.

## Findings and evidence

- At `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`, parsed `w1-results.json` names 43 seats. Each corresponding `w1/<seat>.md` passed `git cat-file -e`; none missing. The result objects' report files are present; report sizes were not separately established as nonzero.
- `w2/swarm-registry.json` has 35 members. Every report exists except `R56W2MutC3Counter.md` and `R56W2MutC2Harness.md`; each absent lookup returned 128. No `.ufo/waves/round-56/w2-results.json` exists (lookup rc=128).
- Dead-seat disposition: 33 registry members have report evidence and are recorded as `settled` in the receipt table; the two missing-report seats are `stopped`, with no report evidence. See `R56W3ExecWaveEvidence/receipts/wave-evidence-a2.txt` for named table and checks.
- The committed w2 tree scan found no >1 MiB `c3-fill-all/SOURCES.md` copy; SOURCES variants in the scan were 288,467–292,183 bytes. **The non-UTF-8 fixture absence remains unverified:** attempting a guessed `Ā.conf` path returned rc=0 and a tree listing exposed a quoted non-UTF-8 filename under the m08 fixture. Exact target identity therefore is uncertain; this is not evidence that the deleted attempt-1 leftover remains, only that this seat could not confirm its absence via the guessed path.

Severity: no wave-report inventory defect beyond the two known stopped seats (documented missing evidence); the non-UTF-8 leftover check is unresolved, not classified as a defect. No other defect identified.

## Current untracked lane paths

`git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain` reported:

- `.ufo/waves/round-56/attempt2/`
- `.ufo/waves/round-56/fetch/man7-inotify_add_watch.2.html`
- `.ufo/waves/round-56/fetch/man7-proc_pid_fdinfo.5.html`
- `.ufo/waves/round-56/make-w3-spec.py`
- `.ufo/waves/round-56/receipts/attempt2-l1.txt`
- `.ufo/waves/round-56/receipts/census-before-a2.txt`
- `.ufo/waves/round-56/w3-dispatch.json`
- `.ufo/waves/round-56/w3-run.err`
- `.ufo/waves/round-56/w3-spec.json`
- `.ufo/waves/round-56/w3.ready`
- `.ufo/waves/round-56/w3.ready.partial`
- `.ufo/waves/round-56/w3/`

These were observed existing operator/wave artifacts and were not changed. Exact command: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain` (rc=0).

## Deliverables and limits

- Receipt: `.ufo/waves/round-56/w3/R56W3ExecWaveEvidence/receipts/wave-evidence-a2.txt`
- Report: `.ufo/waves/round-56/w3/R56W3ExecWaveEvidence.md`
- No tracked lane files or git state changed. No tests/build/lint run. The m08 non-UTF-8 fixture's exact path/absence could not be verified; no other check was blocked.
