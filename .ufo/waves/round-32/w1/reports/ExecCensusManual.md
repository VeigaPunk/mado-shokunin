# ExecCensusManual — mado corpus/SOURCES.md frozen census

**Run:** 2026-10-24 · cwd `/home/vgpnk/Projects/shokunin/mado-shokunin` · lane `mado`
**Target:** `corpus/SOURCES.md` (159,383 bytes, mtime 2026-10-24 03:56 — unmodified by this task)
**Source of commands:** `/home/vgpnk/Projects/shokunin/CORPUS.md` §"SOURCES.md — where a shokunin learns" → "Census" (frozen contract v1, kaika 2026-10-19). The fenced block carries 7 commands; all 7 ran verbatim.
**Transcripts:** `.ufo/waves/round-32/scratch/ExecCensusManual/01…08-*.txt`

## Row count: 185

## Verbatim transcripts

### (1) rows (spacing-tolerant)

```sh
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
185
```

### (2) malformed rows — must print 0

```sh
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
0
```

### (3) tier histogram

```sh
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
A=178 B=1 C=6 
```

### (4) status histogram

```sh
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
mined=166 queued=10 rejected=9 
```

### (5) duplicate ids — must print nothing

```sh
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d
(no output)
```

### (6) enum violations and tier inflation — must print nothing

```sh
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' corpus/SOURCES.md
(no output)
```

### (7) mined rows whose used-by paths do not exist — must print nothing

```sh
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
(no output)
```

### Maintained CLI (same moment)

```sh
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
mado	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
mado	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
exit=0
```

## Findings

- **Registry is clean against the frozen v1 checks**: 185 rows, 0 malformed, 0 duplicate ids, 0 enum violations, 0 tier inflation, 0 missing used-by paths. Histograms sum to 185 (178+1+6 = 166+10+9).
- **Maintained CLI verdict: `ok`, exit 0**, with 7 informational `W04` duplicate-url-across-scopes warnings — the same canonical URL carried on distinct rows under distinct scopes. Contract v1 does not forbid this (dedup key is `id`, not URL); recorded here as signal, not defect. Pairs: S030/S045 (hypr.land window-rules), S120/S121 (cpython executionmodel.rst).
- **Tier skew:** 178/185 rows are A (96.2%) — high but legal; tier inflation check only fires on `community` A rows, of which there are none. Whether the skew reflects honest curation is out of this task's scope.
- No writes to `corpus/SOURCES.md`. No subagent dispatched (leaf bounds).
