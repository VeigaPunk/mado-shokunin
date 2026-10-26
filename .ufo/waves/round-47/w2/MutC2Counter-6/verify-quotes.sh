#!/usr/bin/env bash
# Quote verification for MutC2Counter.md: every source quote in the report must
# appear in its named source at its stated lines (locators computed via grep -n).
set -u
ctr=/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r47-terminal-entry.py
run=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/ctl/c2/run-controls.py
reg=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/registration.md
rec=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47/w2/MutC2Counter-6
ok=1
chk() { # chk <file> <line> <quote>
  if ! grep -n -F -q "$3" "$1"; then echo "MISSING QUOTE in $1: $3"; ok=0; fi
}
chk "$run" 4 "Every mutation is a commit in the scratch clone \$S/ctl (POS tree + one defect)"
chk "$ctr" 26 "b  provenance head, unfenced lines inside the first 20 raw lines: >= 2 distinct"
chk "$ctr" 383 "if ref in BRANCH_REFS:"
chk "$ctr" 385 'if ref != TAG and not re.fullmatch(r"[0-9a-f]{7,40}", ref):'
chk "$ctr" 737 "if not pins:"
chk "$ctr" 766 "if show(repo, base, ENTRY) is not None:"
chk "$reg" 26 "clause f now binds the entry's sentence to a committed capture of the resolver"
# receipt tokens
chk "$rec/harness/pristine.log" 0 "PRED-C2-r47: admitted=1/1 verdict=TARGET_MET rev=6e83dee58ffed8b3de38a3d8a3d518834e72d59a"
chk "$rec/probes/probe-b-verifiedat.log" 0 "clauses=a:1 b:0 c:1 d:1 e:1 f:1 g:1 h:1 i:1 admitted=0"
chk "$rec/probes/probe-b-ghost.log" 0 "clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 admitted=1"
chk "$rec/results.json" 0 '"verdict": "SURVIVED"'
if [ "$ok" = 1 ]; then echo "ALL QUOTES VERIFIED"; else echo "QUOTE VERIFICATION FAILED"; exit 1; fi
