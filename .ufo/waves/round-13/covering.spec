# round-13 named-set diagnostics and fail-closed parser-boundary mutants
# Separate from the byte-preserved historical D1-D9/R1 spec.
@defect P1 | suppress local extra-member detection
@old     if [ -z "${lexp["$x"]:-}" ]; then
@new     if false; then

@defect P2 | suppress local missing-member naming
@old       lmiss="$lmiss $xq"
@new       :

@defect P3 | suppress source extra-member naming
@old       [ -n "${tdecl["$t"]:-}" ] || tset="$tset extra: $t"
@new       :

@defect P4 | suppress source missing-member naming
@old       [ -n "${tseen["$t"]:-}" ] || tset="$tset missing: $t"
@new       : # mutant: source missing-member guard suppressed

@defect P5 | suppress include-graph extra-member naming
@old       [ -n "${declared["$i"]:-}" ] || sdiff="$sdiff extra: $i"
@new       :

@defect P6 | suppress empty-source naming without reintroducing an invalid associative key
@old       if [ -z "$i" ]; then sdiff="$sdiff extra: ''"; continue; fi
@new       : # mutant: empty-member naming suppressed

@defect P7 | ignore conditional hyprlang directives
@old     hyprd=$(grep -nE '^[[:space:]]*#[[:space:]]*hyprlang' "$f" | head -1)
@new     hyprd=''

@defect P8 | drop gkeep from the local expected set
@old   LOCAL+=(gkeep)
@new   : # mutant: gkeep dropped
