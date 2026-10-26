#!/bin/sh
# re-derives the slice, residue joins, and quote locators (read-only)
W=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-44/w1/ScoutQuarantine
R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
K=/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge
Q=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-44/assimilation/quarantine-slice
set -e
awk -F'|' -v l='mado' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' $R | cmp - $Q && echo "slice == quarantine-slice (13 rows)"
echo "register sha256 $(sha256sum $R | cut -c1-64) lines $(wc -l < $R)"
RES="gkeep-rendered-geometry-chain-r9 gkeep-client-size-request-r12 gkeep-rendered-geometry-record-r13 gkeep-rendered-geometry-record-r14 gkeep-geometry-never-recorded-r15 gkeep-element-rules-r30 glyph-and-geometry-r31"
n=0; for f in $RES; do for i in 189 195 199 200 201 205 209 222 223 224 225 228 235; do grep -qE "\bS$i\b" $K/$f.md && { echo HIT $f S$i; n=$((n+1)); }; done; done; echo "id hits in 7 residue files: $n"
for u in EventManager arch-wiki-docs-zh 2604.18860 interwikimap ai-usage cn-export 149787804 lxyoucan; do c=$(cat $(for f in $RES; do echo $K/$f.md; done) | grep -c "$u" || true); echo "source-token $u hits: $c"; done
grep -n 'eventString = std::format' $W/EventManager.cpp.efb5099
grep -n 'opacity 0.80 \$& 0.80 \$& 1,class' $W/csdn-149787804.proxy.txt
grep -n 'S216\|S219' $K/glyph-and-geometry-r31.md
grep -n 'could not be fetched, so no quote was checked' $R | head -2
grep -n 'the gate block named no locator' $R | head -1
