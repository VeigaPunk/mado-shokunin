# round 80 — `## Mistakes` (draft for adoption, prose only)

Sources read: `corpus/lessons/round-79.md` (rows M79-1…M79-8) and
`corpus/lessons/round-79-verifier-spotcheck.md` §1, §4 and §6 (routed defects D1–D5). Every row
below was re-derived from committed bytes on 2026-11-04; every fix names a command and its observed
exit code on the pre-fix bytes and on the fixed bytes. No lane file was edited by this seat.

## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M80-1 | reference-drift: the round-79 report's C1 after-cell quotes `tool_selftest=44/44 … verdict=TARGET_MET rc 0 at d6be05ef` while citing `receipts/measurement-final-r79.txt`, whose committed line 41 prints `tool_selftest=50/50 … rev=999a4a3f`; 44/44 at `d6be05ef` is the R1 receipt `receipts/measurement-c1-r79-repair.txt:38` | `.ufo/reports/round-79/mado.md:95` (after-cell) against `.ufo/waves/round-79/receipts/measurement-final-r79.txt:41` and `.ufo/waves/round-79/receipts/measurement-c1-r79-repair.txt:38` | round-79 non-author verifier spot-check §1(a) and §6.1 (D1); QUALITY 118 replays a declared command, and nothing compared a quoted receipt line with the file it names | the round-80 report carries the erratum pair (superseded text and corrected text, each with its own receipt) and every Before→after cell is run through a citation probe before filing. Shown able to fail: the probe on the filed r79 report exits 1 printing `cell=44/44@d6be05ef receipt=50/50@999a4a3f`, and exits 0 on a copy whose after-cell reads `50/50` at `999a4a3f` (scratch fixture of the corrected cell; the erratum itself lands with the r80 report) |
| M80-2 | attribution: S467's rejection reason said the page "documents the line syntax only", while the committed fetch states the stacking in prose one paragraph below the syntax line | `.ufo/waves/round-45/fetch/wiki-Monitors.md:179` (the `monitor = name, addreserved, TOP, BOTTOM, LEFT, RIGHT` syntax) and `:183` — `the reserved area to add. This does stack on top of the calculated reserved area`; filed row `corpus/SOURCES.md` S467 (rejected 2026-11-04) | round-79 non-author verifier spot-check §1(b), §4 (row S467) and §6.2 (D2): the reason was written from the syntax line alone, and no rule required the reject reason to quote the passage it denies | S475 appended at `corpus/SOURCES.md:426` with `teaches` opening `supersedes S467 —`, narrowing to "dead live URL, no revision pin, tier-B prose only" and quoting `:183`; the filed S467 row stays (append-only). Shown able to fail: a probe requiring exactly one row that opens `supersedes S467 —`, states the three narrowed clauses, anchors `:183` and does not assert "line syntax only" exits 1 on `git show 6c302a53:corpus/SOURCES.md` (`supersede-rows=0`) and 0 on the landed `corpus/SOURCES.md` (`narrowed`) |
| M80-3 | number-drift: LOG.md's round-79 entry says "Seven mined" while the lesson carries eight `## Mistakes` rows | `LOG.md:3928` ("Seven mined in `corpus/lessons/round-79.md`") against `corpus/lessons/round-79.md:15-22` (eight rows, M79-1…M79-8) | round-79 non-author verifier spot-check §1(c) and §6.3 (D3); no counter compares a LOG sentence with the lesson table it summarises | a `## Corrections (round 80, append-only)` block at `LOG.md:3955` names the eight (landed in `b65f3227`); the dated entry is not rewritten. Shown able to fail: a probe that counts the rows and requires a later correction naming that count exits 1 on `git show 6c302a53:LOG.md` (`rows=8 correction=no`) and 0 on `git show b65f3227:LOG.md` (`rows=8 correction=yes`) |
| M80-4 | scope: `.ufo/waves/round-79/fetch/S468.bin` and `S469.bin` read as registry ids but have neither a `SOURCES.md` row nor a line in the wave's manifest | `.ufo/waves/round-79/fetch/` (12 `S*` stems) against `.ufo/waves/round-79/fetch/sha256-r79.txt` (10 entries, no `S468`/`S469`); the files are cited by name at `.ufo/reports/round-79/mado.md:211` ("pinned as `S468`/`S469`") and `corpus/lessons/round-79.md:20` (`S469.bin:92-101`) | round-79 non-author verifier spot-check §1(d) and §6.4 (D4); `sources-census.sh` validates registry rows, not file names inside a wave dir | new ids start at S470: S470–S474 are the five pins in `.ufo/waves/round-80/fetch/sha256-r80.txt` (`sha256sum -c` 5/5 OK, no self-entry) and S475 is the supersede row; S468/S469 stay rowless. Why a fix and not a renumber: the two files were fetched in r79 with no recorded open, the filed report and lesson M79-6 already cite `S468`/`S469` by file name in append-only text, and registry ids are append-ordered — a retroactive row would bless bytes no round opened and seat an id below the wave that cites it. Shown able to fail: a probe requiring every fetch stem of a wave to be registered or manifested exits 1 on the r79 wave (`unlisted=['S468', 'S469']`) and 0 on the r80 wave (`unlisted=[]`, 5/5 manifested), and it flips back to 1 if S468 or S469 ever gains a row |
| M80-5 | landing: the r79 wave's `R79ExecC1Tool` settled with no report file; its `out.txt` (73 OK / 0 FAIL against the pre-R2 tool) is the only trace | `.ufo/waves/round-79/w1/R79ExecC1Tool/` holds `drive.py`, `mado-barfoot.py`, `out.txt` and no `.md`; 13 of the 14 seats filed `w1/<name>.md` | round-79 non-author verifier spot-check §1 (wave paragraph) and §6.5 (D5); the seat prompt required only a report trailer | every r80 seat receives the findings contract in the shared assignment text (`w1-spec.json` `context`: "Your findings file is …/w1/<your-name>/findings.md" and "- End your findings.md with `STATUS: ok …, partial … blocked` plus one line of what is missing"); 12 of 14 task bodies repeat it. One canonical path — `w1/<name>/findings.md` — with the runner's `Report:` trailer `w1/<name>.md` pointing at it, because the wave carries both paths and at 08:46 one seat had filed only the trailer. Shown able to fail: the landing check exits 1 on the r79 wave with exactly one missing report (`R79ExecC1Tool`) and is the gate the r80 wave closes on (at 08:46, mid-flight: 12 reports not yet filed, 0 missing STATUS lines among the two seats that had filed) |

Sweep for a sixth: `grep -n 'TODO\|FIXME\|XXX' tools/mado-barfoot.py
quality/counters/c1-r80-multisurface.py quality/counters/c2-r80-runbook.py` → no output, `rc=1`
(2026-11-04, at the freeze; the r79 sweep covered the r79 trio, this one the r80 trio — both empty).

## The fixes, verbatim (run from the lane root; exit code is the evidence)

```sh
# M80-1 — every cell that cites a receipt and quotes a tally must match that receipt's own line.
python3 - /home/vgpnk/Projects/shokunin/.ufo/reports/round-79/mado.md <<'PY'
import re,sys
line=[l for l in open(sys.argv[1]) if 'measurement-final-r79' in l and 'tool_selftest=' in l][0]
cell=[c for c in line.split('|') if 'measurement-final-r79' in c][0]
want=re.search(r'tool_selftest=(\d+/\d+)',cell).group(1)
rev=re.search(r'at `([0-9a-f]{8})`',cell).group(1)
rec=[l for l in open('.ufo/waves/round-79/receipts/measurement-final-r79.txt') if l.startswith('MADO_R79_BARFOOT')][0]
got=re.search(r'tool_selftest=(\d+/\d+)',rec).group(1)
grev=re.search(r'rev=([0-9a-f]{8})',rec).group(1)
print(f'cell={want}@{rev} receipt={got}@{grev}')
sys.exit(0 if (want,rev)==(got,grev) else 1)
PY
# filed r79 bytes: cell=44/44@d6be05ef receipt=50/50@999a4a3f → rc 1
# the same argv on a copy whose after-cell reads 50/50 at 999a4a3f: rc 0

# M80-2 — exactly one narrowed supersede row for S467, anchored at :183.
python3 - corpus/SOURCES.md <<'PY'
import re,sys
rows=[l for l in open(sys.argv[1]) if re.match(r'^\|\s*S\d+\s*\|',l) and 'supersedes S467' in l]
if len(rows)!=1: print(f'supersede-rows={len(rows)}'); sys.exit(1)
low=rows[0].lower()
ok=all(w in low for w in ('dead live url','no revision pin','prose only')) and ':183' in rows[0] and 'line syntax only' not in low
print('narrowed' if ok else 'reason not narrowed'); sys.exit(0 if ok else 1)
PY
# landed corpus/SOURCES.md: narrowed → rc 0
# git show 6c302a53:corpus/SOURCES.md as the argv: supersede-rows=0 → rc 1

# M80-3 — the row count and the latest count statement must agree.
python3 - LOG.md <<'PY'
import re,sys
rows=len(re.findall(r'(?m)^\| M79-\d+ ',open('corpus/lessons/round-79.md').read()))
log=open(sys.argv[1]).read().splitlines()
corr=[i for i,l in enumerate(log) if 'Round-79 count' in l]
block=' '.join(log[corr[-1]:corr[-1]+3]) if corr else ''
ok=bool(corr) and str(rows) in block and re.search(r'\beight\b',block,re.I)
print(f'rows={rows} correction={"yes" if corr else "no"}'); sys.exit(0 if ok else 1)
PY
# LOG.md (landed b65f3227): rows=8 correction=yes → rc 0
# git show 6c302a53:LOG.md as the argv: rows=8 correction=no → rc 1

# M80-4 — no fetch stem without a row or a manifest line; a leftover never gains a row.
python3 - .ufo/waves/round-80 <<'PY'
import glob,os,re,sys
src=open('corpus/SOURCES.md').read(); w=sys.argv[1]
man=open(glob.glob(w+'/fetch/sha256-r*.txt')[0]).read()
def listed(s):
    return re.search(r'(?m)^\|\s*'+s+r'\s*\|',src) or re.search(r'(?m)\s'+s+r'\.(bin|txt)$',man)
bad=[s for s in sorted(os.path.splitext(os.path.basename(p))[0] for p in glob.glob(w+'/fetch/S*')) if not listed(s)]
blessed=[s for s in ('S468','S469') if re.search(r'(?m)^\|\s*'+s+r'\s*\|',src)]
print(f'unlisted={bad} retroactive_rows={blessed}'); sys.exit(1 if bad or blessed else 0)
PY
# round-80 wave: unlisted=[] retroactive_rows=[] → rc 0 (manifest 5/5, sha256sum -c OK)
# the same argv with .ufo/waves/round-79: unlisted=['S468', 'S469'] → rc 1
# the probe also flips to rc 1 if S468 or S469 ever gains a registry row (retroactive_rows)

# M80-5 — every seat has a STATUS-terminated report; canonical path first.
miss=0
for d in $(python3 -c "import json;print(' '.join(i['name'] for i in json.load(open('.ufo/waves/round-80/w1-spec.json'))['items']))"); do
  f=.ufo/waves/round-80/w1/$d/findings.md; [ -f "$f" ] || f=.ufo/waves/round-80/w1/$d.md
  if [ -f "$f" ] && grep -q '^STATUS: \(ok\|partial\|blocked\)' "$f"; then :; else echo "missing $d"; miss=1; fi
done
exit $miss
# round-80 wave at 08:46: 12 seats not yet filed, 0 missing STATUS among the two that had → rc 1
# the wave closes when this prints nothing and exits 0
# r79 control: the same loop with the STATUS clause dropped (r79 had no STATUS rule) prints
#   "missing R79ExecC1Tool" alone → rc 1; with the r80 STATUS clause applied retroactively it
#   flags all 14, which is why the STATUS line is an r80 criterion and not an r79 defect
```

Named limit on M80-5: the wave has two report paths by construction (the runner prints
`Report: …/w1/<name>.md`; the seat bounds name `…/w1/<name>/findings.md` and require the `STATUS:`
line), and `w1-spec.json`'s context points at the directory form. A landing check that looks at one
path alone can miss a seat that filed only the other; the canonical path is `findings.md`, the
trailer file points at it.
