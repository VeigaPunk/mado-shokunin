# ReviewRowSchema — round-32 w1 · append-block row schema review

Scope: review of the transformed append block
`.ufo/waves/round-32/assimilation/append-block.md` (5 rows: S186, S187, S188,
S189, S196) against the frozen contract `CORPUS.md` §"SOURCES.md — where a
shokunin learns" (contract v1, kaika, frozen) and the maintained checker
`scripts/sources-census.sh` (header error codes E01–E12, W01–W04; script read
only, not modified). Independent verification: `sources-census.sh validate`
plus the seven frozen manual census commands run verbatim over the scratch
mirror `.ufo/waves/round-32/assimilation/validate/corpus/SOURCES.md`.

Date context: `date -u` = 2026-10-24 23:09 UTC; the census script defaults
`--today` to `date -u +%F` = 2026-10-24.

## Verdict

**All five rows PASS every enumerated cell check.** Zero refused cells.
The maintained validator on the scratch mirror exits **1** — every one of its
12 `E11` findings names a `used-by` path that lives **outside `corpus/`**
(`tools/`, `SKILL.md`, `quality/`, `.ufo/waves/`) on pre-existing rows
(S096/S173/S174/S178–S182/S184/S185). The mirror copies only `corpus/`, so
those paths dangle inside it; all seven exist on the live lane root (listed
below). None of the five appended rows triggers any E/W code.

One sequencing fact, not a schema defect: the three `used-by` targets exist in
the mirror but **not yet** in the live lane root (they land with the append —
this is the ordering question scoped to the ReviewGatesExist seat):

- `corpus/knowledge/ipc-contract-r25.md` — exists under `validate/`, absent from lane root
- `corpus/knowledge/dispatcher-semantics-r25.md` — exists under `validate/`, absent from lane root
- `corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md` — exists under `validate/`, absent from lane root

## Per-row checks

Cell dump (verbatim, awk -F'|' fields 2/4/5/9/10/11/12, trimmed):

```
row 1 (S186): id=<S186> kind=<docs> tier=<A> status=<mined> opened=<2026-10-24> recheck=<on-release> used-by=<corpus/knowledge/ipc-contract-r25.md>
row 2 (S187): id=<S187> kind=<docs> tier=<A> status=<mined> opened=<2026-10-24> recheck=<on-compositor-release> used-by=<corpus/knowledge/ipc-contract-r25.md>
row 3 (S188): id=<S188> kind=<docs> tier=<A> status=<mined> opened=<2026-10-24> recheck=<on-release> used-by=<corpus/knowledge/dispatcher-semantics-r25.md>
row 4 (S189): id=<S189> kind=<code> tier=<A> status=<mined> opened=<2026-10-24> recheck=<on-compositor-release> used-by=<corpus/knowledge/ipc-contract-r25.md>
row 5 (S196): id=<S196> kind=<docs> tier=<A> status=<mined> opened=<2026-10-24> recheck=<on-compositor-release> used-by=<corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md>
```

| row | NF==13 | no `\|` in cell | id `S[0-9]{3,}` | kind enum | tier enum | community≠A | status enum | opened valid ≤ today | recheck valid | used-by exists (mirror) | not W03 | not W01 | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S186 | PASS | PASS | PASS `S186` | PASS `docs` | PASS `A` | PASS (docs) | PASS `mined` | PASS `2026-10-24` | PASS `on-release` | PASS `corpus/knowledge/ipc-contract-r25.md` | PASS | PASS | **PASS** |
| S187 | PASS | PASS | PASS `S187` | PASS `docs` | PASS `A` | PASS (docs) | PASS `mined` | PASS `2026-10-24` | PASS `on-compositor-release` | PASS `corpus/knowledge/ipc-contract-r25.md` | PASS | PASS | **PASS** |
| S188 | PASS | PASS | PASS `S188` | PASS `docs` | PASS `A` | PASS (docs) | PASS `mined` | PASS `2026-10-24` | PASS `on-release` | PASS `corpus/knowledge/dispatcher-semantics-r25.md` | PASS | PASS | **PASS** |
| S189 | PASS | PASS | PASS `S189` | PASS `code` | PASS `A` | PASS (code) | PASS `mined` | PASS `2026-10-24` | PASS `on-compositor-release` | PASS `corpus/knowledge/ipc-contract-r25.md` | PASS | PASS | **PASS** |
| S196 | PASS | PASS | PASS `S196` | PASS `docs` | PASS `A` | PASS (docs) | PASS `mined` | PASS `2026-10-24` | PASS `on-compositor-release` | PASS `corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md` | PASS | PASS | **PASS** |

Check notes:

- **NF==13**: `awk -F'|'` on `append-block.md` prints `NF=13` for all 5 lines;
  fields 13/14 are the empty edge fields of the leading/trailing `|` (no cell
  past column 12). `wc -l` = 5 lines; block carries no header/separator —
  correct for insertion into an existing Registry table.
- **No literal or escaped `|`**: `NF==13` proves no raw pipe inside a cell;
  `grep -nF '\|' append-block.md` prints nothing. The only backslashes are
  `>>DATA\n` literals inside S187/S189 anchor/teaches cells — not pipe
  escapes, not field separators.
- **opened `2026-10-24`**: valid ISO date (gawk `mktime` round-trip), equal to
  `TODAY` → not in the future under the census epoch check.
- **recheck**: `on-release` / `on-compositor-release` match the validator's
  symbolic-cadence regex `^[A-Za-z][A-Za-z0-9 _-]*$` (no digits first). Both
  tokens carry lane precedent: live registry uses `on-release` 131×,
  `on-compositor-release` 1×. The stripped prose suffixes are preserved
  verbatim in `assimilation/recheck-prose-stripped.md` per the transform spec.
- **used-by**: single path per row; all three resolve under the mirror
  (`validate/corpus/knowledge/`); absent from the live lane root (see Verdict).
- **W03 / W01**: every row `mined` with non-`—` `used-by` → no W03; no tier-C
  row at all → W01 vacuously clear. No `rejected` row → W02 n/a.
- **Duplicates**: ids unique within the block; absent from live registry
  (`grep -c '| S186 |' corpus/SOURCES.md` etc. all print `0`), consistent with
  ExecCollisionGuard's `collisions.txt` (empty).
- **Mirror insertion**: each appended line in
  `validate/corpus/SOURCES.md` is byte-identical to the append-block line
  (grep `| S### |` + string compare per row → `identical` ×5); S186 sits at
  mirror line 198 inside `## Registry` (heading at line 9, `## Paths` at 204).

## Independent verification 1 — maintained validator on the mirror

Command (exact):

```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-32/assimilation/validate/corpus/SOURCES.md
```

Output (verbatim):

```
file	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
file	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
file	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
file	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
file	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
file	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
file	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
file	E11	S096 missing used-by tools/mado-verify.sh
file	E11	S096 missing used-by SKILL.md
file	E11	S173 missing used-by tools/mado-binds.py
file	E11	S174 missing used-by tools/mado-binds.py
file	E11	S178 missing used-by tools/mado-wsrules.py
file	E11	S179 missing used-by tools/mado-wsrules.py
file	E11	S180 missing used-by tools/mado-wsrules.py
file	E11	S181 missing used-by tools/mado-wsrules.py
file	E11	S182 missing used-by tools/mado-wsrules.py
file	E11	S184 missing used-by .ufo/waves/round-29/registration.md
file	E11	S185 missing used-by quality/check-index.py
file	E11	S185 missing used-by .ufo/waves/round-30/registration.md
EXIT:1
```

## Independent verification 2 — frozen manual census commands (CORPUS.md §Census, verbatim)

Run from `…/assimilation/validate/` so `corpus/SOURCES.md` resolves to the
mirror (its mirror-root `used-by` paths then resolve identically to how they
will on the lane root once the knowledge files land).

```
# rows
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
190

# malformed rows (must print 0)
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
0

# tier histogram
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
A=183 B=1 C=6 

# status histogram
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
mined=171 queued=10 rejected=9 

# duplicate ids (must print nothing)
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d
(empty)

# enum violations and tier inflation (must print nothing)
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' corpus/SOURCES.md
(empty)

# mined rows whose used-by paths do not exist (must print nothing)
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
missing: tools/mado-verify.sh
missing: SKILL.md
missing: tools/mado-binds.py
missing: tools/mado-binds.py
missing: tools/mado-binds.py
missing: tools/mado-wsrules.py
missing: tools/mado-wsrules.py
missing: tools/mado-wsrules.py
missing: tools/mado-wsrules.py
missing: .ufo/waves/round-29/registration.md
missing: quality/check-index.py
missing: .ufo/waves/round-30/registration.md
```

Reading: mirror rows 190 = live 185 (ExecCensusManual) + 5 appended; tier
183+1+6 = status 171+10+9 = 190; live was A=178 mined=166 → +5A, +5mined, as
staged. The 12 `missing:` lines are the same mirror-coverage artifact as the
validator's E11 block — all are pre-existing rows citing paths outside
`corpus/`; every one of those paths exists on the live lane root:

```
exists-live  tools/mado-verify.sh
exists-live  SKILL.md
exists-live  tools/mado-binds.py
exists-live  tools/mado-wsrules.py
exists-live  .ufo/waves/round-29/registration.md
exists-live  quality/check-index.py
exists-live  .ufo/waves/round-30/registration.md
```

The seven W04 duplicate-url-across-scopes lines are informational (script
header: warnings never change status) and identical to the live-lane validate
run reported by ExecCensusManual.

## Bottom line

Block is schema-clean and mirror-insertion is faithful: five rows, every
enumerated check green, ids disjoint from S001–S185. The only gate-relevant
facts carried forward: (a) the append must land together with the three
`corpus/knowledge/` files, else the live registry trips E11 on all five rows;
(b) a fuller mirror (repo root, not just `corpus/`) would silence the 12
pre-existing used-by findings unrelated to this block.
