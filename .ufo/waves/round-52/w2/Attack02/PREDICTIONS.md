Attack02 — pre-registered predictions (written before any probe run)

Counter under test: .ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py
sha256 0fe862f116a789e8f6bebf38dea74b1f5ee20b3c810190ecf295621a3c34dc31 (847 lines)

Frozen clauses under attack:
  claims-frozen.md C1: "non-self resolvable evidence targets";
  registration.md C1: "validates ... resolvable evidence pointer, non-self pointer"
  and fails controls/c1-do-nothing.md "specifically for self-pointer/context defects".

Self-pointer implementation under test (measure(), lines ~346-383):
  pointer_self: for tokens in row["region"] (cells 3+), token must contain "/"
    and token == "quality/tool-ledger.md" or token == row path  (exact string equality)
  wide_self:    same test over row["cells"][1:], scored only when the row has no
    accountable target.
  path_tokens:  backticked spans, else bare words split on [\s,;]+ with ()[]<>"'
    stripped and trailing .,;: stripped; then "#frag" cut, leading "./" cut,
    LINE_SUFFIX (:N or :N-M) cut. No case folding, no slash collapsing, no
    basename resolution, no git mode check.

Prediction register (each P## predicts exact counter output before running):
  P00 fixture green baseline ....... TARGET_MET, all fields 0
  P01 real-lane green at base ...... TARGET_MET 82/82 all fields 0 (exit 0)
  P02 real-lane frozen control ..... self_pointer=1 generic_desc=1 TARGET_MISSED (exit 1)
  P03 `tool-ledger.md`+doc ......... self_pointer=0 generic_desc=0 TARGET_MET (LAUNDERED)
  P04 `alpha.py`+doc (own name) .... self_pointer=0 TARGET_MET (LAUNDERED)
  P05 `./tool-ledger.md`+doc ....... self_pointer=0 TARGET_MET (LAUNDERED)
  P06 `quality/tool-ledger.md)`+doc  self_pointer=0 TARGET_MET (LAUNDERED)
  P07 `quality/tool-ledger.md:x`+doc self_pointer=0 TARGET_MET (LAUNDERED)
  P08 bare `tool-ledger.md` alone .. bad_pointer=1 (misclassified, verdict still MISSED)
  P09 symlink->own file as pointer . self_pointer=0 TARGET_MET (LAUNDERED via git mode blindness)
  P10 symlink->ledger as pointer ... bad_pointer=1 (content names no basename)
  P11 4-cell control shape, bare basename in Reads
                                   ..... bad_pointer=1, self_pointer=0 (control signal is
                                        spelling-dependent; NOT the frozen defect class)
  P12 same 4-cell shape with full path in Reads
                                   ..... self_pointer=1 (confirms full-path spelling fires)
  P13 evidence cycle A->doc(B), B->doc(A)
                                   ..... TARGET_MET (predicate gap, both rows green)
  P14 shared registry doc for all rows
                                   ..... TARGET_MET (predicate gap, omnibus accepted)
  P15 `quality/tool-ledger.md`+doc (closed-hole regression)
                                   ..... self_pointer=1 TARGET_MISSED
  P16 counter --selftest ........... C1_R52_SELFTEST: 53/53 passed, exit 0

If P03-P07 or P09 come out TARGET_MET as predicted, the counter's non-self clause is
defeated by reference spelling / git-mode blindness: a circular accountability claim is
scored as meeting the frozen "non-self resolvable evidence" clause. P08/P10-P12 show the
same semantic defect is reported under the wrong field when it is caught at all, which
bears on the registration requirement that the frozen control fail "specifically for
self-pointer/context defects".
