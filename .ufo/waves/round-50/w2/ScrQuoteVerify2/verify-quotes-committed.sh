#!/usr/bin/env bash
# verify-quotes-committed.sh — round 50, wave w2 seat ScrQuoteVerify2.
#
# Port of .ufo/waves/round-50/w1/ScrRowsR50/verify-quotes.sh with two changes:
#   (1) it never reads the lane worktree: every pin is materialised from
#       `git show <REV>:.ufo/waves/round-50/fetch/<file>` and the admit lines from
#       `git show <REV>:corpus/lessons/round-50.md` — the COMMITTED bytes at REV;
#   (2) the admit set is PARSED out of the committed lesson instead of a hard-coded table,
#       each admit line is resolved to a `## Registry` row of corpus/SOURCES.md at REV, the
#       row's anchor must cover the admitted pin line, the row's stated pin sha256 must equal
#       the committed pin blob, and the row's status/opened/used-by must match the lesson.
# It then checks
#   §2 every `source:` line of corpus/knowledge/hyprland-bind-key-match-r50.md: the row
#      exists, and every line of that row's pin files cited in the entry lies inside one of
#      the row's registered anchors;
#   §3 every located quote `` `quote`(alias:line[-line]) `` in the entry: the quote is a
#      literal substring of the committed pin at the cited line (or inside the cited range),
#      and the cited line is inside an anchor of some registry row that names that pin;
#   §4 the committed pins against the row digests and against fetch/SHA256SUMS.
#
# Read-only. Usage:
#   REV=<rev> bash verify-quotes-committed.sh [--work DIR]
set -u
REV=${REV:-b4a79843cc2545bbe800db9322e58f6e00436629}
LANE=${LANE:-/home/vgpnk/Projects/shokunin/mado-shokunin}
SCRATCH_ROOT=${SCRATCH_ROOT:-/fast/scratch/hyaku/mado-r50/ScrQuoteVerify2}
WORK=$SCRATCH_ROOT/run
if [ "${1:-}" = "--work" ]; then WORK=$2; fi
ulimit -f 65536 2>/dev/null || true
mkdir -p "$WORK/pins" || exit 2

TOP=$(git -C "$LANE" rev-parse --show-toplevel 2>/dev/null) || { echo "ERROR: not a git tree: $LANE" >&2; exit 2; }
[ "$TOP" = "$LANE" ] || { echo "ERROR: toplevel $TOP != $LANE" >&2; exit 2; }
git -C "$LANE" cat-file -e "$REV^{commit}" 2>/dev/null || { echo "ERROR: rev absent: $REV" >&2; exit 2; }

fin=0
git -C "$LANE" show "$REV:corpus/lessons/round-50.md"                       > "$WORK/lesson.md" || fin=1
git -C "$LANE" show "$REV:corpus/knowledge/hyprland-bind-key-match-r50.md" > "$WORK/entry.md"  || fin=1
git -C "$LANE" show "$REV:corpus/SOURCES.md"                              > "$WORK/sources.md" || fin=1
[ "$fin" = 0 ] || { echo "ERROR: cannot read committed blobs at $REV" >&2; exit 2; }
for p in $(git -C "$LANE" ls-tree --name-only "$REV" .ufo/waves/round-50/fetch/); do
  git -C "$LANE" show "$REV:$p" > "$WORK/pins/${p##*/}" || fin=1
done
[ "$fin" = 0 ] || { echo "ERROR: cannot materialise pins at $REV" >&2; exit 2; }
awk '/^## Registry/{f=1;next} /^## /{f=0} f' "$WORK/sources.md" > "$WORK/registry.md"
[ -s "$WORK/registry.md" ] || { echo "ERROR: empty registry section" >&2; exit 2; }

echo "REV=$REV  (committed bytes; lane worktree never read for evidence)"
echo "blob lesson=$(sha256sum "$WORK/lesson.md" | cut -d' ' -f1)"
echo "blob entry=$(sha256sum "$WORK/entry.md" | cut -d' ' -f1)"
echo "blob sources=$(sha256sum "$WORK/sources.md" | cut -d' ' -f1)"
echo "pins=$(ls "$WORK/pins" | wc -l)"
echo

fail=0
row_of()     { grep -F "| $1 |" "$WORK/registry.md" | head -1; }
cell()       { printf '%s\n' "$1" | awk -F'|' -v n="$2" '{print $n}'; }
pin_files_of(){ cell "$1" 7 | grep -oE '\.ufo/waves/round-50/fetch/[A-Za-z0-9._-]+' | sed 's#.*/##' | sort -u; }
# covers FILE LINE ANCHORCELL — whole-file anchor supported
covers() {
  printf '%s\n' "$3" | grep -qF -- "$1 whole file" && return 0
  printf '%s\n' "$3" | grep -oE "[A-Za-z0-9._-]*$(printf '%s' "$1" | sed 's/\./\\./g'):[0-9]+(-[0-9]+)?" \
  | awk -F: -v L="$2" '{ r=$2; n=split(r,a,"-"); lo=a[1]+0; hi=(n>1)?a[2]+0:lo; if (L+0>=lo && L+0<=hi) ok=1 } END{ exit ok?0:1 }'
}
covers_range() { # FILE LO HI CELL
  for x in $(seq "$2" "$3"); do covers "$1" "$x" "$4" || return 1; done; return 0
}

# ---------------------------------------------------------------- §1 admit lines
echo "== §1 Gate admit lines (committed lesson) vs committed pins + registry =="
n=0; a_pass=0
while IFS= read -r line; do
  n=$((n+1)); bad=""
  id=$(printf '%s' "$line"     | sed -n 's/^- \*\*\(S[0-9]\{1,\}\) admit\*\*.*/\1/p')
  pin=$(printf '%s' "$line"    | grep -oE '\.ufo/waves/round-50/fetch/[A-Za-z0-9._-]+:[0-9]+' | head -1)
  url=$(printf '%s' "$line"    | sed -n 's/.*URL: \([^;]*\);.*/\1/p')
  own=$(printf '%s' "$line"    | sed -n 's/.*Source: \(\.ufo\/[^ ]*\) (own-work.*/\1/p')
  quote=$(printf '%s' "$line"  | sed -n 's/^[^»]*»//; s/«.*//p')
  stated=$(printf '%s' "$line" | sed -n 's/.*(\([0-9]\{1,\}\) words).*/\1/p')
  [ -n "$id" ]     || { echo "FAIL unparsed admit line: ${line:0:60}"; fail=$((fail+1)); continue; }
  [ -n "$pin" ]    || bad="$bad pin-token-missing"
  [ -n "$quote" ]  || bad="$bad quote-token-missing"
  [ -n "$stated" ] || bad="$bad wordcount-token-missing"
  [ -n "$url$own" ] || bad="$bad url-and-source-missing"
  printf '%s' "$line" | grep -qF 'opened 2026-10-27' || bad="$bad date-missing"

  file=""; lineno=""
  if [ -n "$pin" ]; then
    file=$(basename "${pin%:*}"); lineno=${pin##*:}
    [ -f "$WORK/pins/$file" ] || bad="$bad pin-file-absent"
    if [ -f "$WORK/pins/$file" ] && [ -n "$quote" ]; then
      sed -n "${lineno}p" "$WORK/pins/$file" | grep -qF -- "$quote" || bad="$bad quote-not-at-$file:$lineno"
    fi
  fi
  if [ -n "$quote" ]; then
    wa=$(printf '%s' "$quote" | wc -w)
    [ "$wa" -le 25 ] || bad="$bad over-25"
    [ "$wa" = "$stated" ] || bad="$bad wordcount-${wa}!=${stated}"
    printf '%s' "$line" | grep -qF -- "$quote" || bad="$bad quote-not-verbatim-in-line"
  fi

  row=$(row_of "$id")
  if [ -z "$row" ]; then
    bad="$bad no-registry-row"
  else
    if [ -n "$url" ]; then printf '%s' "$row" | grep -qF -- "$url" || bad="$bad row-source-url-mismatch"
    elif [ -n "$own" ]; then printf '%s' "$row" | grep -qF -- "$own" || bad="$bad row-source-path-mismatch"; fi
    acell=$(cell "$row" 7)
    if [ -n "$pin" ]; then
      covers "$file" "$lineno" "$acell" || bad="$bad anchor-uncovers-$file:$lineno"
      dig=$(printf '%s' "$row" | grep -oE 'sha256:[0-9a-f]{64}' | head -1 | sed 's/^sha256://')
      act=$(sha256sum "$WORK/pins/$file" 2>/dev/null | cut -d' ' -f1)
      [ -z "$dig" ] || [ "$dig" = "$act" ] || bad="$bad row-pin-digest-mismatch"
    fi
    st=$(cell "$row" 9  | tr -d ' \t'); op=$(cell "$row" 10 | tr -d ' \t'); used=$(cell "$row" 12)
    [ "$st" = "mined" ] || bad="$bad status-$st"
    [ "$op" = "2026-10-27" ] || bad="$bad opened-$op"
    case "$id" in
      S357|S358) exp=corpus/lessons/round-50.md ;;
      *)         exp=corpus/knowledge/hyprland-bind-key-match-r50.md ;;
    esac
    printf '%s' "$used" | grep -qF -- "$exp" || bad="$bad used-by-lacks-$exp"
  fi

  if [ -z "$bad" ]; then
    printf 'PASS %s %s:%s (%s words; row anchor covers; pin digest equals row)\n' "$id" "$file" "$lineno" "$stated"; a_pass=$((a_pass+1))
  else
    printf 'FAIL %s %s:%s%s\n' "$id" "${file:-?}" "${lineno:-?}" "$bad"; fail=$((fail+1))
  fi
done < <(grep '^- \*\*S[0-9]* admit\*\*' "$WORK/lesson.md")

echo "admit lines: parsed=$n pass=$a_pass/$n"
[ "$n" = 12 ] || { echo "FAIL admit-line count $n != 12"; fail=$((fail+1)); }
rej=$(grep -c '^- \*\*REJECT' "$WORK/lesson.md")
echo "reject lines: $rej/5"
[ "$rej" = 5 ] || { echo "FAIL reject-line count $rej != 5"; fail=$((fail+1)); }
echo

# ---------------------------------------------------------------- §2 source: lines
echo "== §2 entry 'source:' lines vs registry rows and anchor coverage =="
allcites=$(grep -oE '[A-Za-z0-9._-]+\.[A-Za-z0-9]+:[0-9]+(-[0-9]+)?' "$WORK/entry.md" | sort -u)
s_pass=0; s_n=0
while IFS= read -r rec; do
  s_n=$((s_n+1))
  ln=${rec%%:*}; line=${rec#*:}
  id=$(printf '%s' "$line" | sed -n 's/^source: \(S[0-9]\{1,\}\).*/\1/p')
  bad=""
  if [ -z "$id" ]; then echo "FAIL entry:$ln source-line-unparsed"; fail=$((fail+1)); continue; fi
  row=$(row_of "$id")
  if [ -z "$row" ]; then bad="$bad no-registry-row"; else
    acell=$(cell "$row" 7)
    pfiles=$(pin_files_of "$row")
    miss=""
    while IFS= read -r c; do
      [ -n "$c" ] || continue
      cf=$(basename "${c%%:*}"); cr=${c#*:}; lo=${cr%%-*}; hi=${cr##*-}
      printf '%s\n' "$pfiles" | grep -qxF -- "$cf" || continue
      covers_range "$cf" "$lo" "$hi" "$acell" || miss="$miss ${cf}:${cr}"
    done <<< "$allcites"
    [ -z "$miss" ] || bad="$bad cites-outside-row-anchors:$miss"
  fi
  if [ -z "$bad" ]; then echo "PASS entry:$ln $id -> row resolves; every cited line inside its anchors"; s_pass=$((s_pass+1))
  else echo "FAIL entry:$ln $id$bad"; fail=$((fail+1)); fi
done < <(grep -n '^source: ' "$WORK/entry.md")
echo "source lines: $s_pass/$s_n pass"
echo

# ---------------------------------------------------------------- §3 located quotes
echo '== §3 entry located quotes (`quote`(alias:line[-line])) vs committed pins =='
q=0; qok=0; qanchor=0; npin=0
rows_ids=$(grep -oE '^\| S[0-9]+ ' "$WORK/registry.md" | sed 's/^| //;s/ $//')
while IFS= read -r tok; do
  q=$((q+1))
  loc=${tok##*(}; loc=${loc%)}
  quote=${tok#\`}; quote=${quote%\`\(*}
  f=${loc%%:*}; rest=${loc#*:}; f=${f##*/}; lo=${rest%%-*}; hi=${rest##*-}
  if [ ! -f "$WORK/pins/$f" ]; then npin=$((npin+1)); printf 'SKIP %s (not a pin file)\n' "$loc"; continue; fi
  bad=""
  found=0
  for x in $(seq "$lo" "$hi"); do
    sed -n "${x}p" "$WORK/pins/$f" | grep -qF -- "$quote" && { found=1; break; }
  done
  [ "$found" = 1 ] || bad="$bad quote-not-at-$loc"
  covrow=""
  while IFS= read -r rid; do
    r=$(row_of "$rid"); [ -n "$r" ] || continue
    printf '%s' "$(cell "$r" 7)" | grep -qF -- "$f:" || continue
    covers_range "$f" "$lo" "$hi" "$(cell "$r" 7)" && { covrow=$rid; break; }
  done <<< "$rows_ids"
  [ -n "$covrow" ] || bad="$bad no-anchor-covers-$loc"
  if [ -z "$bad" ]; then
    qok=$((qok+1)); qanchor=$((qanchor+1))
  else
    printf 'FAIL %s:%s%s  quote=%.70s\n' "$f" "$lo" "$bad" "$quote"; fail=$((fail+1))
  fi
done < <(grep -oP '`[^`]*`\([A-Za-z0-9._-]+:[0-9]+(?:-[0-9]+)?\)' "$WORK/entry.md")
echo "located quote tokens=$q  pin-cite quotes at cited line=$((q-npin))  quote+anchor pass=$qok  non-pin skips=$npin"
echo

# ---------------------------------------------------------------- §4 pin digests
echo "== §4 committed pins vs fetch/SHA256SUMS and vs row digests =="
su_bad=0; su_n=0
while read -r dig name; do
  [ -n "${name:-}" ] || continue
  [ "$name" = "SHA256SUMS" ] && continue
  su_n=$((su_n+1))
  act=$(sha256sum "$WORK/pins/$name" | cut -d' ' -f1)
  [ "$dig" = "$act" ] || { echo "FAIL SHA256SUMS $name $dig != $act"; su_bad=$((su_bad+1)); }
done < "$WORK/pins/SHA256SUMS"
echo "SHA256SUMS entries checked=$su_n mismatched=$su_bad"
fail=$((fail+su_bad))
echo

if [ "$fail" -eq 0 ]; then echo '---'; echo 'ALL COMMITTED QUOTES, ROWS AND ANCHORS VERIFIED'; exit 0; fi
echo '---'; echo "FAILED: $fail"
exit 1
