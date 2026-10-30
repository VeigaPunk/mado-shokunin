# R56W3ExecReverifyC1

Attack: frozen C1 predicate and 12-control harness at the content tip; base-revision absence check.

Commands and exact output are in `R56W3ExecReverifyC1/receipts/c1-a2.txt`. The extracted tip tree was committed in an isolated fresh scratch repository (`0eb8962441cfbe540d3f9de95f7f7c94ceb39bf5`) because an archive does not retain the source repository's commit objects. The exact requested revision therefore cannot be resolved by the counter in that repo; scoring used the commit of the archived tree.

Frozen sentence verdicts:
- `MADO_AUTORELOAD_ENTRY rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 TARGET_MET`: MET on archived tip tree, rc 0.
- `MADO_R56_CONTROLS claim=c1 good=ok controls=12/12 verdict=OK`: MET on archived tip tree, rc 0.
- Base `13f0acbe3a15da2d9c08357a576d91dcadc85273`: not verifiable as requested. It is not an object in the archive-derived repo; exact output `setup error: rev does not resolve to a commit: 13f0acbe3a15da2d9c08357a576d91dcadc85273`, rc 2. This does not establish the requested entry-absent behavior.

No counter/harness deviation was observed on the archived tip. No build, lint, formatter or separate tests were run. No tool installed. Scratch retained only under `/fast/scratch/hyaku/mado-r56/R56W3ExecReverifyC1/`; deliverable receipt: `.ufo/waves/round-56/w3/R56W3ExecReverifyC1/receipts/c1-a2.txt`.

Risk/blocker: base-check target revision absent from the fresh archive repository; base entry-absent result remains unverified. The receipt includes the exact attempted command and failure.