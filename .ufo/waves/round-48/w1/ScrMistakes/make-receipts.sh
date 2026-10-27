#!/bin/bash
# Receipt producer for seat ScrMistakes (round 48, w1). Read-only over the lane; writes only
# inside this seat directory. Every receipt is the command line, its stdout+stderr and its rc.
set -u
cd /home/vgpnk/Projects/shokunin/mado-shokunin || exit 1
S=.ufo/waves/round-48/w1/ScrMistakes
R=$S/receipts
mkdir -p "$R"
REPORT=/home/vgpnk/Projects/shokunin/.ufo/reports/round-47/mado.md
FR=d7527d608ad2b2e3cc398fdde34db7947b254a1a
TIP=d40189c924e01dc1cbe290474eb4256d343590d4
FROZEN=.ufo/waves/round-47/l1-draft/mado-terminal.py

run() {   # run <receipt> <command string>
  local out="$1"; shift
  { echo "\$ $*"; echo; eval "$@" 2>&1; echo "rc=$?"; } > "$R/$out"
}

# ---------------------------------------------------------------- M48-1 / criterion 96 (D1)
{
  echo '$ sha256sum of the frozen reference at the freeze commit and of the landed tool'
  echo "frozen  $(git show $FR:$FROZEN | sha256sum)"
  echo "landed  $(sha256sum tools/mado-terminal.py)"
  echo
  echo '$ diff -u <frozen lines 78-90> <landed lines 79-91>   (the out-of-contract paragraph)'
  diff -u <(git show $FR:$FROZEN | sed -n '78,90p') <(sed -n '79,91p' tools/mado-terminal.py)
  echo
  echo '$ grep -n "Also out of contract" (frozen bytes at the freeze commit, landed bytes at the tip)'
  git show $FR:$FROZEN | grep -n 'Also out of contract'
  grep -n 'Also out of contract' tools/mado-terminal.py
  echo
  echo '$ the frozen contract sentence in the registration (C1 Residuals, declared)'
  grep -n 'Residuals (declared)' .ufo/waves/round-47/registration.md
  sed -n '52,56p' .ufo/waves/round-47/registration.md
  echo
  echo '$ the landed behaviour the frozen text does not name (FIFO refusal is new after the freeze)'
  diff -u <(git show $FR:$FROZEN) tools/mado-terminal.py | grep -n 'S_ISFIFO\|symlink loops\|HOME unset'
  echo
  echo '$ the HOME-unset raise: present in the frozen bytes, absent from the frozen list'
  git show $FR:$FROZEN | grep -n 'raise OutOfContract'
  grep -n 'raise OutOfContract' tools/mado-terminal.py
} > "$R/d1-contract-delta.txt" 2>&1

run check96-run.txt 'echo "## RED: the landed tool against the frozen reference"; python3 -I '$S'/check96.py --repo . --frozen-rev '$FR' --frozen '$FROZEN' --landed tools/mado-terminal.py; echo "rc=$?"; echo; echo "## GREEN 1: the same delta registered by an appended erratum"; python3 -I '$S'/check96.py --repo . --frozen-rev '$FR' --frozen '$FROZEN' --landed tools/mado-terminal.py --registered '$S'/controls/registered-96.txt; echo "rc=$?"; echo; echo "## GREEN 2: the frozen reference scored as its own landed file (no delta)"; python3 -I '$S'/check96.py --repo . --frozen-rev '$FR' --frozen '$FROZEN' --landed '$FROZEN'; echo "rc=$?"'

# ---------------------------------------------------------------- M48-2 / criterion 97 (D2)
{
  echo '$ the report line that states the number (fleet report, committed 6fd1391)'
  grep -n 'findings=' "$REPORT"
  echo
  echo "\$ git grep -n 'findings=128' $TIP"
  git grep -n 'findings=128' $TIP; echo "rc=$? (1 = no line anywhere in the lane at the tip)"
  echo
  echo "\$ git grep -l 'findings=136' $TIP -- .ufo/waves/round-47 | wc -l   # a receipted sibling number"
  git grep -l 'findings=136' $TIP -- .ufo/waves/round-47 | wc -l
  echo
  echo '$ every findings= line in a receipt of the round'
  git grep -n -F 'findings=' $TIP -- .ufo/waves/round-47/receipts .ufo/waves/round-47/w1/ExecSessionMarker/receipts
  echo
  echo "## criterion 69's own instrument on the same report (it reads rev= tokens only)"
  python3 -I .ufo/waves/round-41/w1/ScrQualityCriteria/check69.py --repo . --rev $TIP --report "$REPORT" --receipts .ufo/waves/round-47/receipts --text; echo "rc=$?"
} > "$R/d2-report-number.txt" 2>&1

run check97-run.txt 'echo "## RED: the round-47 report against every round-47 receipt"; python3 -I '$S'/check97.py --repo . --rev '$TIP' --report '"$REPORT"' --receipts .ufo/waves/round-47 --text --quiet-ok; echo "rc=$?"; echo; echo "## GREEN: the same report with the one number corrected to a receipted value"; python3 -I '$S'/check97.py --repo . --rev '$TIP' --report '$S'/controls/report-97-fixed.md --receipts .ufo/waves/round-47 --text --quiet-ok; echo "rc=$?"'

# ---------------------------------------------------------------- M48-3 / criterion 98 (D3)
{
  echo '$ the seat finding the closure routed as D3, and the report/lesson that never name the seat'
  sed -n '9,11p' .ufo/waves/round-47/w2/ExecC1Determinism.md
  echo '$ grep -c ExecC1Determinism <report> <lesson>'
  printf 'report=%s lesson=%s\n' "$(grep -c ExecC1Determinism "$REPORT")" "$(grep -c ExecC1Determinism corpus/lessons/round-47.md)"
  echo
  echo '$ the closure routing it (round-47-verifier-spotcheck.md section 6, item 3)'
  grep -n 'readdir-order blind spot' corpus/lessons/round-47-verifier-spotcheck.md
  echo
  echo '$ a second unrouted finding of the same class: MutC2Counter coverage holes'
  sed -n '40,41p' .ufo/waves/round-47/w2/MutC2Counter.md
  printf 'report=%s lesson=%s\n' "$(grep -c MutC2Counter "$REPORT")" "$(grep -c MutC2Counter corpus/lessons/round-47.md)"
  echo
  echo '$ a third: MutC1Counter surviving mutants'
  sed -n '15,18p' .ufo/waves/round-47/w2/MutC1Counter.md
  printf 'report=%s lesson=%s\n' "$(grep -c MutC1Counter "$REPORT")" "$(grep -c MutC1Counter corpus/lessons/round-47.md)"
  echo
  echo '$ the w1 axis finding, also unnamed (the population is not w2-only)'
  sed -n '71,72p' .ufo/waves/round-47/w1/ExecAxisBase.md
  printf 'report=%s lesson=%s\n' "$(grep -c ExecAxisBase "$REPORT")" "$(grep -c ExecAxisBase corpus/lessons/round-47.md)"
} > "$R/d3-routing.txt" 2>&1

run check98-run.txt 'echo "## RED: every w2 seat that states a blind spot, a coverage hole or a surviving mutant"; python3 -I '$S'/check98.py --repo . --rev '$TIP' --seats .ufo/waves/round-47/w2 --lesson corpus/lessons/round-47.md --report '"$REPORT"' --report-text; echo "rc=$?"; echo; echo "## the same scan over the w1 seats"; python3 -I '$S'/check98.py --repo . --rev '$TIP' --seats .ufo/waves/round-47/w1 --lesson corpus/lessons/round-47.md --report '"$REPORT"' --report-text; echo "rc=$?"; echo; echo "## GREEN: the report with the four finding seats routed by name"; python3 -I '$S'/check98.py --repo . --rev '$TIP' --seats .ufo/waves/round-47/w2 --lesson corpus/lessons/round-47.md --report '$S'/controls/report-98-routed.md --report-text; echo "rc=$?"'

# ---------------------------------------------------------------- M48-4 / criterion 99 (D4)
{
  echo '$ the cited text: the [UNK] bullet at 149 and its continuation at 150'
  awk 'NR>=148 && NR<=151 {printf "%d: %s\n", NR, $0}' corpus/knowledge/terminal-route-r17.md
  echo
  echo '$ the entry line that cites 150-151'
  grep -n 'terminal-route-r17.md:150-151' corpus/knowledge/xdg-terminal-selection-r47.md
  echo
  echo "$ criterion 77's own instrument on that entry: it reads 0 locators"
  python3 -I quality/check-locators.py --fetch .ufo/waves/round-43/fetch corpus/knowledge/xdg-terminal-selection-r47.md; echo "rc=$?"
  echo
  echo '$ the unqualified README.md locators and the three files that basename matches'
  grep -n 'README.md:[0-9]' corpus/knowledge/xdg-terminal-selection-r47.md
  wc -l README.md .ufo/waves/round-47/fetch/README.md corpus/README.md
  echo
  echo '$ the pin declaration that is the only way to resolve them'
  sed -n '4p' corpus/knowledge/xdg-terminal-selection-r47.md
} > "$R/d4-locator.txt" 2>&1

run check99-run.txt 'echo "## RED: the entry as landed"; python3 -I '$S'/check99.py --repo . --rev '$TIP' --citing corpus/knowledge/xdg-terminal-selection-r47.md --fetch .ufo/waves/round-47/fetch; echo "rc=$?"; echo; echo "## GREEN: the same entry with the range corrected to 149-150 and the README locators qualified"; python3 -I '$S'/check99.py --repo . --rev '$TIP' --citing '$S'/controls/entry-99-fixed.md --citing-text --fetch .ufo/waves/round-47/fetch; echo "rc=$?"'

# ---------------------------------------------------------------- M48-5 / criterion 100 (M47-7)
{
  echo '$ the round-47 mistake row: mined, class provider, captured-by none'
  grep -n 'M47-7' corpus/lessons/round-47.md
  sed -n '189,193p' corpus/lessons/round-47.md
  echo
  echo '$ the criteria landed from that lesson cite M47-1..M47-6 only'
  grep -n 'lesson: lessons/round-47.md#mistakes' corpus/QUALITY.md
  echo
  echo "\$ grep -c 'M47-7' corpus/QUALITY.md"
  grep -c 'M47-7' corpus/QUALITY.md
  echo
  echo '$ the only bound either wave stated: a prose ceiling in the seat context'
  python3 - <<'PY'
import json, re
for tag, path in (("r47", ".ufo/waves/round-47/w1-spec.json"),
                  ("r48", ".ufo/waves/round-48/w1-spec.json")):
    s = json.dumps(json.load(open(path)))
    for m in re.finditer(r"[^\"]{0,40}keep it under[^\"]{0,90}", s):
        print(tag, ":", m.group(0))
PY
  echo
  echo '$ no enforced bound in either dispatch'
  grep -c 'ulimit' .ufo/waves/round-47/w1-spec.json .ufo/waves/round-48/w1-spec.json
} > "$R/m47-7-mined.txt" 2>&1

run check100-run.txt 'echo "## RED 1: the round-47 w1 spec"; python3 -I '$S'/check100.py --spec .ufo/waves/round-47/w1-spec.json; echo "rc=$?"; echo; echo "## RED 2: this round-48 w1 spec (the class recurs in the round that mines it)"; python3 -I '$S'/check100.py --spec .ufo/waves/round-48/w1-spec.json; echo "rc=$?"; echo; echo "## GREEN: a dispatch that carries the command the seat runs"; python3 -I '$S'/check100.py --spec '$S'/controls/spec-100-capped.json; echo "rc=$?"'

# ---------------------------------------------------------------- near duplicates and the sweep
{
  echo '$ the highest numbered criterion in QUALITY.md'
  grep -oE '^[0-9]+\.' corpus/QUALITY.md | tail -1
  echo
  for n in 52 69 77 90 93 94 95; do
    echo "--- criterion $n (first 4 lines)"
    awk -v n="$n" '$0 ~ "^"n"\\." {p=1} p {print; if (++c==4) exit}' corpus/QUALITY.md
  done
  echo
  echo '$ criterion 77 instrument scope: names that exist in the fetch directory only'
  grep -n 'fetch' quality/check-locators.py | sed -n '1,14p'
  echo
  echo '$ no existing criterion compares a landed contract text to the frozen one (grep freeze)'
  grep -n 'freeze' corpus/QUALITY.md | cut -c1-150
  echo
  echo '$ no existing criterion bounds a seat writer (grep bounded|scratch|file size)'
  grep -n 'bounded resource\|scratch measurement\|file-size' corpus/QUALITY.md | cut -c1-150
} > "$R/near-duplicates.txt" 2>&1

{
  echo '$ every round-45/46/47 mistake row whose captured-by is none'
  grep -n 'captured-by:.*none' corpus/lessons/round-4[567].md
  echo
  echo '$ which criteria cite each of those lessons'
  grep -n 'lesson: lessons/round-4[567].md#mistakes' corpus/QUALITY.md | sed 's/  */ /g'
  echo
  echo '$ round-46 rows whose class no criterion cites'
  grep -n 'M46-6\|M46-11' corpus/QUALITY.md; echo "rc=$?"
} > "$R/unmined-sweep.txt" 2>&1

echo "receipts written:"
ls -l "$R"
