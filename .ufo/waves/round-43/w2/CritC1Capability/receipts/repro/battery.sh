#!/bin/bash
# CritC1Capability — every claim sentence of the C1 tool run as an input. cwd = scratch, G = tool copy.
G=/fast/scratch/hyaku/mado-r43/CritC1Capability/mado-geometry.py
cd fx || exit 1
say(){ printf '%s\n' "$*"; }
r(){ label=$1; shift; out_="$("$@" 2>err.tmp)"; rc=$?; say "### $label"; say "\$ $*"; say "$out_"; say "stderr_bytes=$(wc -c <err.tmp) exit=$rc"; say ""; }
r "selftest" python3 $G --selftest
r "no-args/usage" python3 $G
r "rules-too_large(1048577B)" python3 $G --clients c_agree.json --rules pad1048577.conf
r "rules-exact-1048576B-accepted" python3 $G --clients c_agree.json --rules pad1048576.conf
r "rules-missing" python3 $G --clients c_agree.json --rules /nonexistent/none
r "rules-directory" python3 $G --clients c_agree.json --rules dir
r "rules-FIFO" python3 $G --clients c_agree.json --rules fifo
r "rules-chardev(/dev/null)" python3 $G --clients c_agree.json --rules /dev/null
r "rules-devzero(/dev/zero)" python3 $G --clients c_agree.json --rules /dev/zero
chmod 000 noperm.conf
r "rules-perm000" python3 $G --clients c_agree.json --rules noperm.conf
chmod 600 noperm.conf
r "rules-symlink_to_regular" python3 $G --clients c_agree.json --rules link.conf
r "clients-FIFO" python3 $G --clients fifo --rules ctl.conf
r "clients-too_large(1048577B-file)" python3 $G --clients pad1048577.conf --rules ctl.conf
r "clients-exact-1048576B" python3 $G --clients c1048576.json --rules ctl.conf
r "bad_json-object" python3 $G --clients notlist.json --rules ctl.conf
r "exit0-AGREE" python3 $G --clients c_agree.json --rules ctl.conf
r "exit1-DIFFER" python3 $G --clients c_differ.json --rules ctl.conf
r "exit3-NO_MATCHING_CLIENT" python3 $G --clients c_nomatch.json --rules ctl.conf
r "exit4-NO_SIZE_RULES" python3 $G --clients c_agree.json --rules empty.conf
r "windowrulev2-ignored-counted-nowhere" python3 $G --clients emptylist.json --rules v2only.conf
r "match:tag-unsupported" python3 $G --clients emptylist.json --rules tagrule.conf
r "match:title-conjunction-unsupported" python3 $G --clients emptylist.json --rules titlematch.conf
r "bracket-class-unsupported" python3 $G --clients emptylist.json --rules bracket.conf
r "regex-201-chars-unsupported" python3 $G --clients emptylist.json --rules d201.conf
r "regex-200-chars-supported" python3 $G --clients emptylist.json --rules d200.conf
r "duplicate-clients-flag" python3 $G --clients c_agree.json --clients c_agree.json --rules ctl.conf
r "dangling-flag" python3 $G --clients c_agree.json --rules
r "bogus-flag" python3 $G --clients c_agree.json --rules ctl.conf --bogus x
r "abbreviated-flag" python3 $G --client c_agree.json --rules ctl.conf
r "selftest-with-args" python3 $G --selftest --rules ctl.conf
r "two-files-last-size-wins(30x40 last)" python3 $G --clients c_agree.json --rules r10.conf --rules r30.conf
r "two-files-last-size-wins(10x20 last)" python3 $G --clients c_agree.json --rules r30.conf --rules r10.conf
r "tab-separated-rule" python3 $G --clients c_agree.json --rules tabs.conf
r "no-trailing-newline" python3 $G --clients c_agree.json --rules noeol.conf
r "BOM-prefixed-rule-line(vendor BOM)" python3 $G --clients c_agree.json --rules bom.conf
say "### stdin-1048577-bytes"
head -c 1048577 /dev/zero | tr '\0' ' ' | python3 $G --clients - --rules ctl.conf > o.tmp 2> err.tmp; rc=$?; cat o.tmp; say "stderr_bytes=$(wc -c <err.tmp) exit=$rc"; say ""
say "### stdin-1048576-bytes-valid"
python3 -c "import sys;sys.stdout.write('[{\"class\":\"a\",\"size\":[10,20],\"floating\":true,\"mapped\":true}]'.ljust(1048576,' '))" | python3 $G --clients - --rules ctl.conf > o.tmp 2> err.tmp; rc=$?; cat o.tmp; say "stderr_bytes=$(wc -c <err.tmp) exit=$rc"; say ""
rm -f err.tmp o.tmp
