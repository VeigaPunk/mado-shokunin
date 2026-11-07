# L1 MadoR95 DRAFT findings on the c1 candidate (during w1; not measurements)

Probe: `/fast/scratch/hyaku/mado-r95/L1/edge.py` (synthetic caches via the candidate's build_cache, oracle
`controls/mimesniff-oracle-r95.c` compiled against glib2 2.90.1-1), 2026-11-07 ~08:15Z.

| probe | oracle | c1 candidate | verdict |
|---|---|---|---|
| prio 0x80000005 first in one cache, then prio 10 | text/plain 0 | text/plain 0 | agree (first match per cache; negative int never wins) |
| prio 0x80000005 in cache 1, prio 10 in cache 2 | a/low 0 | a/low 0 | agree |
| prio 0 match | text/plain 0 / octet-stream 1 | same | agree |
| range_start 0xFFFFFFFF length 2 (end wraps) | text/plain 0 | same | agree |
| range_length 0 | text/plain 0 | same | agree |
| value offset past the file, inside the last page | text/plain 0 / a/v 0 | same | agree (zero-filled page) |
| value offset 100000 past the page | text/plain 0 (rc 0) | UNSUPPORTED | UB read outside the mapping; GLib's answer depends on adjacent memory — exclude such cases (argument), never label them |
| child list fails the bounds check | text/plain 0 | same | agree |
| child list points at itself | SIGSEGV (rc -11) | UNSUPPORTED | agree (refusal) |
| range_start 0xFFFFFFF0, value 32 bytes, data 4 bytes | text/plain 0 | UNSUPPORTED | **c1 DEFECT L1-F1**: `i + value_length` wraps to 16 > len, so C returns FALSE; the candidate refuses before the wrapped comparison. Fix: refuse only when the wrapped sum is <= len (memcmp at data+i past the data). |
| x-desktop with a typeless name / NULL / x.desktop | text/plain 0, x-desktop 0, text/plain 0 | same | agree (the fixture cache has no `*.desktop` glob, so `x.desktop` is typeless too: any non-NULL name turns a sniffed x-desktop into text/plain) |
