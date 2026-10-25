#!/usr/bin/env bash
# RevC1Tip reproduction. Reads the lane tree; writes only under this scratch dir.
set -u
L=/home/vgpnk/Projects/shokunin/mado-shokunin
S=$L/.ufo/waves/round-35/scratch/RevC1Tip
C=$L/.ufo/waves/round-35/c1/count.py
F=$L/.ufo/waves/round-35/c1/frozen.json
CENSUS=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
run(){ echo "\$ python3 -I $C --root $1 --frozen $F"; python3 -I "$C" --root "$1" --frozen "$F"; echo "rc=$?"; }

echo '## 0 hashes'
sha256sum "$C" "$F" "$L/.ufo/waves/round-35/c2/count.py" "$L/.ufo/waves/round-35/c2/frozen.json"
echo '## 0b HEAD blob hashes vs worktree'
cd "$L" || exit 2
for p in .ufo/waves/round-35/c1/count.py .ufo/waves/round-35/c1/frozen.json; do
  printf '%s  HEAD:%s\n' "$(git cat-file -p HEAD:"$p" | sha256sum | cut -d' ' -f1)" "$p"
  printf '%s  worktree:%s\n' "$(sha256sum "$p" | cut -d' ' -f1)" "$p"
done

echo '## 1 assigned command, verbatim'
echo '$ cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I .ufo/waves/round-35/c1/count.py --root . --frozen .ufo/waves/round-35/c1/frozen.json; echo rc=$?'
( cd "$L" && python3 -I .ufo/waves/round-35/c1/count.py --root . --frozen .ufo/waves/round-35/c1/frozen.json; echo "rc=$?" )

echo '## 1b cwd-independent run with absolute paths'
( cd /tmp && python3 -I "$C" --root "$L" --frozen "$F"; echo "rc=$?" )

echo '## 1c determinism, three consecutive runs'
for i in 1 2 3; do ( cd "$L" && python3 -I .ufo/waves/round-35/c1/count.py --root . --frozen .ufo/waves/round-35/c1/frozen.json; echo "run$i rc=$?" ); done

echo '## 2 minimal rebuild of the scored tree'
rm -rf "$S/tree"; mkdir -p "$S/tree/corpus/knowledge" "$S/tree/.ufo/waves/round-35/fetch"
cp "$L/corpus/SOURCES.md" "$S/tree/corpus/SOURCES.md"
cp "$L"/corpus/knowledge/idle-lock-never-asked-r12.md "$L"/corpus/knowledge/idle-lock-chain-armed-r14.md "$L"/corpus/knowledge/idle-lock-offered-in-the-bar-r15.md "$S/tree/corpus/knowledge/"
cp "$L"/.ufo/waves/round-35/fetch/S20[3-9].receipt.txt "$L"/.ufo/waves/round-35/fetch/S210.receipt.txt "$S/tree/.ufo/waves/round-35/fetch/"
run "$S/tree"

echo '## 3 F1: receipt bytes rotated after freeze (S206), anchors untouched'
rm -rf "$S/m1"; cp -r "$S/tree" "$S/m1"
printf '\nTAMPER: bytes changed after freeze\n' >> "$S/m1/.ufo/waves/round-35/fetch/S206.receipt.txt"
echo "actual sha256: $(sha256sum "$S/m1/.ufo/waves/round-35/fetch/S206.receipt.txt" | cut -d' ' -f1)"
echo "frozen sha256: 1d30e4a999b53d5288369edc7573d7ceee0aef99570a55d781c4625440a938d5"
run "$S/m1"

echo '## 4 negative controls (counter must be failable)'
rm -rf "$S/m2"; cp -r "$S/tree" "$S/m2"
python3 - "$S/m2/corpus/SOURCES.md" <<'PY'
import sys,re
p=sys.argv[1]; lines=open(p).read().splitlines(True); out=[]; n=0
for ln in lines:
    if n==0 and re.match(r"^ {0,3}\|\s*S206\s*\|", ln):
        ln=ln.replace("| mined |","| queued |",1); n=1
    out.append(ln)
open(p,'w').write("".join(out)); print("status_columns_mutated=",n)
PY
echo '-- M2 status mined->queued'; run "$S/m2"

rm -rf "$S/m3"; cp -r "$S/tree" "$S/m3"
python3 - "$S/m3/corpus/knowledge/idle-lock-offered-in-the-bar-r15.md" <<'PY'
import sys
p=sys.argv[1]; out=[]
for ln in open(p).read().splitlines(True):
    if ln.startswith("gate-quote: S207 "): ln="gate-quote: S207 "+" ".join(["word"]*26)+"\n"
    out.append(ln)
open(p,'w').write("".join(out))
PY
echo '-- M3 S207 quote padded to 26 words'; run "$S/m3"

rm -rf "$S/m5"; cp -r "$S/tree" "$S/m5"
python3 - "$S/m5/corpus/knowledge/idle-lock-chain-armed-r14.md" <<'PY'
import sys
p=sys.argv[1]; out=[]
for ln in open(p).read().splitlines(True):
    if ln.startswith("gate-quote: S205 "): ln="gate-quote: S205 located: this sentence is absent from the receipt entirely\n"
    out.append(ln)
open(p,'w').write("".join(out))
PY
echo '-- M5 S205 quote not a receipt substring'; run "$S/m5"

rm -rf "$S/m4"; cp -r "$S/tree" "$S/m4"
python3 - "$S/m4/corpus/SOURCES.md" <<'PY'
import sys,re
p=sys.argv[1]; lines=open(p).read().splitlines(True); out=[]; n=0
for ln in lines:
    if re.match(r"^ {0,3}\|\s*S208\s*\|", ln):
        ln=ln.rstrip("\n").rstrip(); assert ln.endswith("|")
        ln=ln[:-1]+", corpus/knowledge/idle-lock-never-asked-r12.md |\n"; n+=1
    out.append(ln)
open(p,'w').write("".join(out)); print("usedby_extra_mutations=",n)
PY
echo '-- M4 S208 used-by gains a foreign entry'; run "$S/m4"

rm -rf "$S/m7"; cp -r "$S/tree" "$S/m7"
rm "$S/m7/.ufo/waves/round-35/fetch/S209.receipt.txt"
echo '-- M7 S209 receipt deleted'; run "$S/m7"

rm -rf "$S/m8"; cp -r "$S/tree" "$S/m8"
python3 - "$S/m8/corpus/SOURCES.md" <<'PY'
import sys,re
p=sys.argv[1]; lines=open(p).read().splitlines(True); out=[]
for ln in lines:
    if re.match(r"^ {0,3}\|\s*S210\s*\|", ln):
        ln=ln.replace("ef282e386cdfb686fd331f4ed2fa7f0a33faf3ef4714844639b3eee4790b8726","0"*64)
    out.append(ln)
open(p,'w').write("".join(out))
PY
echo '-- M8 S210 anchor digest zeroed (mirrors committed c1-digest control)'; run "$S/m8"

echo '## 5 F2: the only S206 row moved outside ## Registry'
rm -rf "$S/m9"; cp -r "$S/tree" "$S/m9"
python3 - "$S/m9/corpus/SOURCES.md" <<'PY'
import sys,re
p=sys.argv[1]; lines=open(p).read().splitlines(True)
row=[l for l in lines if re.match(r"^ {0,3}\|\s*S206\s*\|", l)]
assert len(row)==1
out=[]
for l in lines:
    if re.match(r"^ {0,3}\|\s*S206\s*\|", l): continue
    out.append(l)
    if l.startswith("## Leads (unopened)"): out.extend(["\n", row[0]])
open(p,'w').write("".join(out))
print("registry_section_ends_at:", min(i+1 for i,l in enumerate(out) if l.startswith("## Paths")))
print("s206_row_now_at:", [i+1 for i,l in enumerate(out) if re.match(r"^ {0,3}\|\s*S206\s*\|",l)])
PY
run "$S/m9"

echo '## 6 F3: committed HEAD bytes only (git archive; committed counter + committed frozen spec)'
echo "HEAD=$( cd "$L" && git rev-parse --short HEAD )"
rm -rf "$S/headtree2"; mkdir -p "$S/headtree2"
( cd "$L" && git archive HEAD corpus/SOURCES.md \
    corpus/knowledge/idle-lock-never-asked-r12.md \
    corpus/knowledge/idle-lock-chain-armed-r14.md \
    corpus/knowledge/idle-lock-offered-in-the-bar-r15.md \
    .ufo/waves/round-35/fetch .ufo/waves/round-35/c1 | tar -x -C "$S/headtree2" )
echo "\$ python3 -I $S/headtree2/.ufo/waves/round-35/c1/count.py --root $S/headtree2 --frozen $S/headtree2/.ufo/waves/round-35/c1/frozen.json"
python3 -I "$S/headtree2/.ufo/waves/round-35/c1/count.py" --root "$S/headtree2" --frozen "$S/headtree2/.ufo/waves/round-35/c1/frozen.json"; echo "rc=$?"

echo '## 7 independent re-derivation (own parser, no import of count.py)'
( cd "$L" && python3 -I "$S/independent_c1.py" . .ufo/waves/round-35/c1/frozen.json; echo "rc=$?" )
