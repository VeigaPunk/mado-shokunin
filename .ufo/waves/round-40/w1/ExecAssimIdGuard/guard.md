# §10 id-collision guard — evidence

Seat: ExecAssimIdGuard (round 40, w1). Source of the command: operator prompt
`/home/vgpnk/Projects/shokunin/.ufo/prompts/mado-round-40.md` §10, lines 475–483 (verbatim block
below). Contract clause it implements: `/home/vgpnk/Projects/shokunin/CORPUS.md:152-154`
("The maintained `scripts/sources-census.sh` CLI accepts 0–3 leading ASCII spaces before Markdown
table rows … The frozen manual census examples above assume column-zero input").

## 1. Command run (exactly the §10 block)

```bash
S=/home/vgpnk/Projects/shokuknow
A=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-40/assimilation; mkdir -p "$A"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md \
  | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$S/merge/mado/SOURCES.append.md" \
  | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"
comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"
```

Run output (counts via `wc -l`):

```
reg=214 staged=147 coll=22
```

Input hashes (the exact bytes the extractor read):

```
f99b6bf0c27008f947bc892564cfb374e95e82e96cf6f4f49d346baa54fb3e96  mado-shokunin/corpus/SOURCES.md
684efe8c23b8b64d789187dab61bfbf7c0dcef4f0428e447c94d7be4e73a27c0  shokuknow/merge/mado/SOURCES.append.md
```

Output hashes:

```
0ce5fd8f34ab6799b43d4d06b03a3296efad4cc1a7f280a01fd0dbcfff9d6b94  $A/reg-ids
079d7538022b0acf8bfadcd150b9db16a54bb550f190361454d4649054f0925d  $A/staged-ids
2a9b91330f473eb98f40d4cbead20bc89dd2764215bc38b21c9e66caafda96fb  $A/collisions
```

## 2. Id lists (both, complete)

- `$A/reg-ids` — **214** ids (214 registry rows, `grep -cE '^\s{0,3}\|[[:space:]]*S[0-9]{3,}'
  corpus/SOURCES.md` = 214; no duplicates: `uniq -d` empty):

```
S001..S189, S196, S201, S202, S203..S221, S253, S258, S277
```

  Expanded: S001–S189 (189), S196, S201, S202, S203–S221 (19), S253, S258, S277 = 214.
  Non-contiguous by design: 63 gaps, all below the max S277 (gaps 190–195, 197–200, 222–252,
  254–257, 259–276).

- `$A/staged-ids` — **147** ids, contiguous:

```
S203..S349
```

  (147 = 349 − 203 + 1; no duplicates: `uniq -d` empty.)

## 3. Collision count and ids

**22 collisions** (`$A/collisions`, nonempty → the §10 renumber rule is live for these ids):

```
S203 S204 S205 S206 S207 S208 S209 S210 S211 S212
S213 S214 S215 S216 S217 S218 S219 S220 S221
S253 S258 S277
```

Reading: the lane already holds staged ids S203–S221 (19 rows opened in earlier rounds) plus
S253, S258, S277. Any staged row among these must be renumbered in scratch before an append; the
lane registry is never rewritten (append-only, CORPUS.md rule 2).

## 4. Guard proof (scratch fixture, run once)

Fixture construction (`D=$(mktemp -d)` = `/tmp/idguard.xSuOKi`; no repo, no git, no write outside
`/tmp`):

```bash
D=$(cat /tmp/idguard.path)          # /tmp/idguard.xSuOKi
# scratch registry = the real header (SOURCES.md lines 1-12) + ONE 2-space-indented row:
sed -n '1,12p' mado-shokunin/corpus/SOURCES.md > "$D/SOURCES.scratch.md"
printf '  | S002 | scratch indented row - proof fixture | own-work | A | guard proof | fixture:1 @ scratch | an indented row is a census row, so a column-zero-only extractor misses it | queued | 2026-10-25 | 180d | — |\n' >> "$D/SOURCES.scratch.md"
# staged copy holding S002:
printf '| S002 | staged row - proof fixture | own-work | A | guard proof | fixture:1 @ scratch | staged collision fixture | queued | 2026-10-25 | 180d | — |\n' > "$D/staged.scratch.md"
```

(a) The scratch registry is census-valid — the indented row is a row, not code:

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$D/SOURCES.scratch.md" --today 2026-10-25
file	ok	/tmp/idguard.xSuOKi/SOURCES.scratch.md
census_exit=0
```

(b) The §10 guard (0–3 leading spaces) catches the collision:

```
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$D/SOURCES.scratch.md" | grep -oE 'S[0-9]+' | sort > "$D/reg-ids.scratch"
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$D/staged.scratch.md" | grep -oE 'S[0-9]+' | sort > "$D/staged-ids.scratch"
$ comm -12 "$D/reg-ids.scratch" "$D/staged-ids.scratch" > "$D/collisions.scratch"
reg-ids.scratch:
S002
staged-ids.scratch:
S002
collisions.scratch:
S002
coll_count=1
```

(c) The column-zero-only pattern false-greens it (the defect §10 names):

```
$ grep -oE '^\|[[:space:]]*S[0-9]{3,}' "$D/SOURCES.scratch.md" | grep -oE 'S[0-9]+' | sort > "$D/reg-ids.zero"
reg-ids.zero lines=0
$ comm -12 "$D/reg-ids.zero" "$D/staged-ids.scratch" > "$D/collisions.zero"
collisions.zero lines=0
```

Fixture hashes:

```
19d7b5acfd0d465eeb2f7bd584d4cb1a7049f8c419d2113a51592829590f6bd5  SOURCES.scratch.md
e73683dfd9dc584f51e915ae5c8ba968a953eb091a948257122455769ec14f5a  staged.scratch.md
f8d01e5667f90f1061416beeda117f0509eb2038fc96d63d3a6e59f37ca65828  reg-ids.scratch
f8d01e5667f90f1061416beeda117f0509eb2038fc96d63d3a6e59f37ca65828  staged-ids.scratch
f8d01e5667f90f1061416beeda117f0509eb2038fc96d63d3a6e59f37ca65828  collisions.scratch
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  collisions.zero   (empty)
```

Verdict: guard prints S002; the column-zero-only pattern prints nothing. The guard is proven for
this lane's first append under §10.

## 5. K2 renumber map candidate (by document, not arithmetic)

K2 = `merge/mado/knowledge/corpus/knowledge/host-producer-outputs-r29.md`; its `source:` lines
name S237–S241 (entry order). Collision test per id:

```
S237 reg=0 staged=1
S238 reg=0 staged=1
S239 reg=0 staged=1
S240 reg=0 staged=1
S241 reg=0 staged=1
```

So **K2 needs no renumber: identity** (S237–S241 are free in the lane; staged rows may be adopted
under their own ids). Next free lane id = **S278** (registry max S277; append-only, ids are never
reused, so gaps below the max are not candidates). Candidate map, only if a renumber were forced,
in the entry's document order — the URL is the evidence and the id follows it:

| staged id | source URL / path (evidence) | next free lane id (candidate) |
|---|---|---|
| S237 | https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/default/waybar/indicators/screen-recording.sh | S278 |
| S238 | https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/default/waybar/indicators/notification-silencing.sh | S279 |
| S239 | /home/vgpnk/.local/bin/gkeep | S280 |
| S240 | /home/vgpnk/.local/bin/ai-usage | S281 |
| S241 | /home/vgpnk/.cache/ai-usage/status.json | S282 |

Re-pointing rule if the map is ever used: the citation moves with the document, i.e. an entry's
`source:` line is rewritten to the id assigned to *that URL*, never to `old_id + offset`.

URL-level duplicate check (census E04, lane registry) — all five documents are absent from the
lane today, so identity adoption is also E04-clean:

```
screen-recording.sh          -> 0
notification-silencing.sh    -> 0
.local/bin/gkeep             -> 0
.local/bin/ai-usage          -> 0
.cache/ai-usage/status.json  -> 0
```

## 6. Bounds and tool state

- Writes: only `$A/{reg-ids,staged-ids,collisions}` (named by §10), this file, the seat report,
  and `/tmp/idguard.xSuOKi` scratch. No assimilation file other than the three named was written;
  no lane/fleet repo file edited; no git/jj command of any kind run (not even read-only); no
  compositor verb run; no package transaction.
- Tools installed: none (coreutils `grep`/`sort`/`comm`, plus the repo's own
  `scripts/sources-census.sh` read-only validate). Absolute paths used throughout.
- Scratch cleanup: `/tmp/idguard.xSuOKi` was removed after the hashes above were recorded
  (`ls -d` → "No such file or directory"); the fixtures survive only as the hashes and the
  commands in §4, which rebuild them byte-identically.
