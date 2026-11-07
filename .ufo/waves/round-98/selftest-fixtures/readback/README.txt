readback fixtures -- round-98 C2 counter selftest (PRED-C2-r98-v1, v2 predicate)

Synthetic mini-repos; every authored file is ASCII. Each directory is a repo
root the gate accepts via --repo DIR (it reads corpus/SOURCES.md and
corpus/knowledge/*.md). All fixture rows carry status "mined" unless named.

  clean/     S001,S002 acknowledge alpha; S003 acknowledges beta. Gate: exit 0,
             findings=0, rows=3, entries=2.
  r4/        clean with S001's used-by cell emptied; alpha cites S001 -> gate
             reports exactly one finding: R4 S001
             entry=corpus/knowledge/alpha.md.            (status-aware: rows
             here are mined; rejected/queued rows never fire R4)
  r1/        clean with S001's recheck cell set to a path; exactly one R1 S001
             recheck=corpus/knowledge/alpha.md.
  r3/        clean with a dangling member appended to S001's used-by; exactly
             one R3 S001 path=corpus/knowledge/ghost-missing.md.
  planted/   byte products of the counter's own transforms over
             clean/corpus/SOURCES.md and its alpha.md (FIXTURE_SPECS):
               SOURCES-r4-stripped-usedby.md   strip-usedby  S001
               SOURCES-r1-path-in-recheck.md   recheck-path S001
                                               corpus/knowledge/alpha.md
               SOURCES-r3-dangling-usedby.md   append-usedby S001
                                               corpus/knowledge/ghost-missing.md
               KNOWLEDGE-r5-phantom-id-alpha.md
                                               append-entry-id alpha S999
               SOURCES-r6-duplicate-row.md     duplicate-row S001
             ct05 asserts byte equality; regenerate from
             c2-r98-sources-readback.py by running planted_products() over the
             clean fixture with FIXTURE_SPECS.
  basepair/  base/ = unrepaired (S001,S002 used-by empty; alpha cites S001/S002
             -> independent status-aware pass counts 2 mismatches);
             rev/ = repaired (both name alpha -> 0 mismatches, repaired == 2,
             added_paths == 2, entry/row sets equal, citation supersets hold);
             rev-delete-cite/ (alpha drops its S001 citation -> citation
             supersets broken), rev-reword/ (alpha rewords to the already
             acknowledged S003 -> repaired < base pairs), rev-shotgun/ (every
             row names beta too -> added_paths != repaired), rev-no-beta/
             (beta.md deleted -> entry-path set changed). The four no-work
             shapes score unrepaired through the same repair_legs() body the
             counter's measure uses (ct14-ct17).
  shapes/    parser shapes the frozen frontmatter scope requires:
             yaml/     entry frontmatter fenced with --- and a source: block
                       of "  - S001 / - S002" list items -> exactly one
                       R4 S002 entry=corpus/knowledge/alpha-yaml.md
             wrapped/  wrapped continuation line carries the S002 citation ->
                       exactly one R4 S002 entry=corpus/knowledge/alpha-wrap.md
             pathtoken/ receipt path .ufo/waves/round-37/fetch/S213.receipt.txt
                       and S214-x are NOT citations -> findings=0

The real-scale planted controls (5 products + the committed always-clean stub
gate + manifest.json) live in ../../controls/readback-planted/ and are cut by
`c2-r98-sources-readback.py --emit-planted DIR` from the measured --rev bytes.
