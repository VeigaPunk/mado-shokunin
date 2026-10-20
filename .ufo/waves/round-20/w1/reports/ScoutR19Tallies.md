# ScoutR19Tallies — all three routed round-19 tallies re-derive exactly; the "155" is prose-only, and 12/154 scan digests are now stale

Scope: the three numbers routed by the closure (`corpus/lessons/round-19-verifier-spotcheck.md:59`, `:88`, `:125`) against the lane's own lesson (`corpus/lessons/round-19.md:108`, `:124`). Everything below is measured from committed bytes or from the receipt file; no gate, selftest, scan, fixture, or transcript content was executed. Scratch tools live in `/tmp/r20-scout-tallies/`; the only lane write is this report.

Revisions used (resolved with `git rev-parse --verify REV^{commit}` in the lane):

```text
1f7f995caa25627db804e996cccd87fe38a3a1b6   1f7f995  (round-19 tip named by the round-20 context)
9c54c56a6a7528675027b7f628f97a1b8d1b8e8d   9c54c56  (pre-round baseline)
b435568540f9a28f4f7bb902af8dbe6a5b084dfe   b435568  (reviewed round tip in the closure)
7b4839d31d60af5bac40e3e74aec70e928601dfc   7b4839d  (final round-19 gate revision)
```

Tool identity check first, because the seat-scan receipt names the tool that produced it:

```console
$ git show 1f7f995:tools/mado-tripwire.py > /tmp/r20-scout-tool-1f7f995.py
$ sha256sum /tmp/r20-scout-tool-1f7f995.py
367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d  /tmp/r20-scout-tool-1f7f995.py
```

That equals the receipt's `tool_sha256=367be947…` (receipt line 1), so the receipt's tool identity is verified against the named revision.

## Tally 1 — transcript count: 154, not 155

Receipt: `mado-shokunin/.ufo/waves/round-19/evidence/final/tripwire-seat-scan.txt` (117,738 bytes, 8 lines, JSON on line 7). Recorded command targets the seat directory `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR19`, `utc=2026-10-20T18:29:35Z`, `measured_commit=0fa412525f8e9f9a7489276da3e35f07637919b9`, `--permit tool_install`.

```console
$ find <MadoR19 dir> -maxdepth 1 -type f -name '*.jsonl' | wc -l
154
$ find <MadoR19 dir> -maxdepth 1 -type f | wc -l
308
$ find <MadoR19 dir> -maxdepth 1 -type f -name '*.md' | wc -l
154
$ find <MadoR19 dir> -maxdepth 1 -type d | wc -l
1
$ python3 -I /tmp/r20-scout-tallies/tally1-files.py
receipt_header: RECEIPT tool=tools/mado-tripwire.py tool_sha256=367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d measured_commit=0fa412525f8e9f9a7489276da3e35f07637919b9 utc=2026-10-20T18:29:35Z cmd=p
json_schema: mado-tripwire-verdict-v1 exit: 1
counts: {"host_mutation": 0, "live_probe": 3, "package_query": 0, "tool_install": 0, "vcs_write": 164}
files_listed: 154 unique_paths: 154
disk_jsonl: 154 disk_all_regular_files: 308 disk_md: 154
subdirs: 0
listed_not_on_disk: 0
on_disk_not_listed: 0
digest_mismatch: 12 of 154
  MadoR19.GateFreshJj.jsonl: receipt_lines=509 now_lines=571
  MadoR19.RevRubricVRisk.jsonl: receipt_lines=166 now_lines=170
  MadoR19.ReviewDeltaCarry.jsonl: receipt_lines=83 now_lines=98
  MadoR19.ReviewFrozen19.jsonl: receipt_lines=89 now_lines=90
  MadoR19.ReviewGateF6F9.jsonl: receipt_lines=74 now_lines=104
  MadoR19.ReviewHarmTool.jsonl: receipt_lines=75 now_lines=76
  MadoR19.ReviewJjFinal.jsonl: receipt_lines=82 now_lines=97
  MadoR19.ReviewLandedTool.jsonl: receipt_lines=65 now_lines=134
  MadoR19.ReviewLessonRows.jsonl: receipt_lines=100 now_lines=282
  MadoR19.ReviewQualityNote.jsonl: receipt_lines=89 now_lines=103
  MadoR19.ReviewRepinTool.jsonl: receipt_lines=85 now_lines=90
  MadoR19.ReviewSourcesRows.jsonl: receipt_lines=83 now_lines=110
sibling_main_transcript: /home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07/MadoR19.jsonl exists= True bytes= 3143206
```

Observed:

- The receipt lists **154 unique files**; the scanned directory now holds **exactly those 154 `.jsonl` files** (set difference 0 in both directions, 0 subdirectories). The scanner only ever opens `*.jsonl` (`/tmp/r20-scout-tool-1f7f995.py:1504`, `if n.endswith(".jsonl")`), so the 154 `.md` sidecars are correctly not transcripts. The `counts` object matches the lesson's prose exactly (`host_mutation` 0, `package_query` 0, `tool_install` 0, `live_probe` 3, `vcs_write` 164, exit 1).
- Therefore the closure's `:125` figure **154 is correct**, and `corpus/lessons/round-19.md:124`'s "155 round-19 transcripts" is not reproducible from the recorded scan path. The only adjacent transcript not in that path is the sibling orchestrator transcript `/…/MadoR19.jsonl` (3,143,206 B, outside `MadoR19/`) [INFERENCE: plausible origin of the +1; not proven].
- New limit not recorded by the closure: **12 of 154 receipt digests no longer match**, and every one of the 12 has grown (`receipt_lines` < current lines). Transcripts kept appending after the 18:29:35Z scan, so the receipt's per-file `sha256` is a point-in-time record and cannot be re-verified for those 12 files today. The file *count* is unaffected.
- [UNK] I cannot observe the directory listing as it stood at 18:29:35Z; I can only show the receipt's 154 paths are exactly the current 154. Directory mtime is `2026-10-20 16:05:04 -0300` (19:05:04Z), later than the scan, consistent with post-scan sidecar creation/appends.

## Tally 2 — S096 credit over the fresh-pins 13: any-line 8/13, first-line 6/13, five S090-only files

Counter used unmodified for the denominator: `python3 -I .ufo/waves/round-19/fresh-pins.py 1f7f995` reports `denominator=13 current=13 score=10.0` (same 13 paths). Credit test is the counter's own regex (`fresh-pins.py:28`, `POINTER = re.compile(r"2\.17\.2.*\bS\d{3}\b|\bS\d{3}\b.*2\.17\.2")`) plus `\bS096\b` on that same line.

```console
$ python3 -I /tmp/r20-scout-tallies/tally2-s096.py 1f7f995
rev=1f7f995 commit=1f7f995caa25627db804e996cccd87fe38a3a1b6 denominator=13
  SKILL.md: qualifying_lines=[573, 1853, 1855, 1856, 1857, 1858, 1859, 1860, 1861, 1862, 1863, 1864, 1865, 1891] first=573 anyS096=True firstS096=True tokens=['S073', 'S084', 'S090', 'S091', 'S094', 'S096']
  corpus/README.md: qualifying_lines=[44, 137, 138] first=44 anyS096=True firstS096=False tokens=['S072', 'S091', 'S096']
  corpus/knowledge/arc-synthesis.md: qualifying_lines=[392] first=392 anyS096=False firstS096=False tokens=['S090']
  corpus/knowledge/closeout-r11.md: qualifying_lines=[299] first=299 anyS096=False firstS096=False tokens=['S090']
  corpus/knowledge/config-health-report-r3.md: qualifying_lines=[1009] first=1009 anyS096=False firstS096=False tokens=['S090']
  corpus/knowledge/remaining-planes-census.md: qualifying_lines=[338, 340] first=338 anyS096=True firstS096=True tokens=['S090', 'S096']
  corpus/knowledge/walker-deep-r9.md: qualifying_lines=[403, 412, 415] first=403 anyS096=True firstS096=True tokens=['S090', 'S091', 'S096']
  corpus/knowledge/walker-deep.md: qualifying_lines=[622, 623, 630] first=622 anyS096=True firstS096=True tokens=['S073', 'S090', 'S091', 'S096']
  corpus/knowledge/walker-live-surface.md: qualifying_lines=[305, 312] first=305 anyS096=True firstS096=True tokens=['S090', 'S096']
  corpus/knowledge/walker-route-r18.md: qualifying_lines=[1, 327, 328] first=1 anyS096=True firstS096=False tokens=['S072', 'S073', 'S074', 'S075', 'S076', 'S077', 'S078', 'S079', 'S080', 'S081', 'S082', 'S083', 'S084', 'S085', 'S086', 'S087', 'S088', 'S089', 'S090', 'S091', 'S096', 'S098']
  corpus/knowledge/waybar-walker-plane.md: qualifying_lines=[479] first=479 anyS096=False firstS096=False tokens=['S090']
  corpus/knowledge/waybar-walker-semantics.md: qualifying_lines=[467, 477] first=467 anyS096=False firstS096=False tokens=['S090']
  tools/mado-verify.sh: qualifying_lines=[56, 67, 104, 1329, 1997, 3364] first=56 anyS096=True firstS096=True tokens=['S090', 'S096']
ANY-LINE S096: 8/13
FIRST-LINE S096: 6/13
NO S096 (S090-only pointers): 5/13 -> ['corpus/knowledge/arc-synthesis.md', 'corpus/knowledge/closeout-r11.md', 'corpus/knowledge/config-health-report-r3.md', 'corpus/knowledge/waybar-walker-plane.md', 'corpus/knowledge/waybar-walker-semantics.md']
```

Snapshot series under the same definition (same 13 files, same regex):

```console
$ for REV in 9c54c56 df84807 01b8094 61eaa07 1f7f995 b435568; do echo "== $REV"; python3 -I /tmp/r20-scout-tallies/tally2-s096.py "$REV" | tail -3; done
== 9c54c56
ANY-LINE S096: 0/13
FIRST-LINE S096: 0/13
NO S096 (S090-only pointers): 13/13 -> ['SKILL.md', 'corpus/README.md', 'corpus/knowledge/arc-synthesis.md', 'corpus/knowledge/closeout-r11.md', 'corpus/knowledge/config-health-report-r3.md', 'corpus/knowledge/remaining-planes-census.md', 'corpus/knowledge/walker-deep-r9.md', 'corpus/knowledge/walker-deep.md', 'corpus/knowledge/walker-live-surface.md', 'corpus/knowledge/walker-route-r18.md', 'corpus/knowledge/waybar-walker-plane.md', 'corpus/knowledge/waybar-walker-semantics.md', 'tools/mado-verify.sh']
== df84807
ANY-LINE S096: 7/13
FIRST-LINE S096: 6/13
== 01b8094
ANY-LINE S096: 7/13
FIRST-LINE S096: 6/13
== 61eaa07
ANY-LINE S096: 8/13
FIRST-LINE S096: 6/13
== 1f7f995
ANY-LINE S096: 8/13
FIRST-LINE S096: 6/13
== b435568
ANY-LINE S096: 8/13
FIRST-LINE S096: 6/13
```
(At df84807/01b8094 six files have no S096 — `corpus/README.md` plus the five listed below — because the two "reserved/pending" rows already carried an S096 denial token that the any-line test counts; later corrections turned them positive.)

Observed:

- 8 any-line files: `SKILL.md`, `corpus/README.md`, `remaining-planes-census.md`, `walker-deep-r9.md`, `walker-deep.md`, `walker-live-surface.md`, `walker-route-r18.md`, `tools/mado-verify.sh` — exactly the closure's `:59` list, at `1f7f995` and again at `b435568`.
- 6 first-line files: the same set minus `corpus/README.md` (first qualifying line `:44` carries the `S072`/`S091` span; S096 is at `:137`/`:138`) and minus `walker-route-r18.md` (first qualifying line `:1` is the `source:` header, S072–S091 + S098; S096 is at `:328`).
- 5 files with no S096 on any qualifying line, each carrying `S090` on its single/first pointer line: `arc-synthesis.md:392`, `closeout-r11.md:299`, `config-health-report-r3.md:1009`, `waybar-walker-plane.md:479`, `waybar-walker-semantics.md:467`. Exactly the closure's five.
- The lesson's "5 of 13 credited files name S096 on the crediting line" (`round-19.md:108`) is **not** an any-line or first-line count at any measured revision. Its provenance is `w2/reports/RerunC2.md` §2, measured at `01b8094`, whose tally is explicitly "S096 cited as evidence **5/13**" (it excludes the two rows that *denied* S096 — `remaining-planes-census:338`, `walker-live-surface:305` — and README's span-only line). At `01b8094` the plain any-line count was already 7 and first-line 6; at the tip the two denial rows were corrected to positive S096 and README gained S096, moving any-line to 8. So the closure is right that 5/13 must not be reused, and the precise reason is a definition change plus snapshot drift, not a simple miscount at one revision.

## Tally 3 — OM10 assertions removed: nine occurrences, eight distinct; OM10A six + OM10B eight added

```console
$ git show 9c54c56:tools/mado-verify.sh > /tmp/r20-scout-om10-9c54c56.sh
$ git show 7b4839d:tools/mado-verify.sh > /tmp/r20-scout-om10-7b4839d.sh
$ sha256sum /tmp/r20-scout-om10-*.sh
c9fb0cef3e081dc878d69f8e20c148429bdfbdce949f8afaed705db957ea42b5  /tmp/r20-scout-om10-9c54c56.sh
050efc720599345a73bdce6c1d13d50eadeee9769c2ece02462223d0156703f1  /tmp/r20-scout-om10-7b4839d.sh
```

(The `7b4839d` digest equals the gate hash the closure binds at `:90` and says is unchanged at `b435568`.)

Census rule A = the eight labelled assertion helpers (`st_eq`, `st_has`, `st_not_has`, `st_rows`, `st_row_has`, `st_row_detail`, `st_row_exact`, `st_counts_agree`; label is the first argument except for the last four, where it is the last argument), with backslash-continuations joined. Rule B = A minus the three helper-internal calls whose label is a bare parameter (`$1`/`$2`/`$5`), plus the four direct `st_bad "<literal>"` failure-branch assertions [INFERENCE: this is the rule that reproduces the closure's totals; verified by exact arithmetic fit].

```console
$ python3 /tmp/r20-scout-tallies/tally3-labels.py /tmp/r20-scout-om10-9c54c56.sh /tmp/r20-scout-om10-7b4839d.sh
== /tmp/r20-scout-om10-9c54c56.sh
  defA occurrences=389 distinct_labels=369 distinct_(helper,label)=370
  st_bad sites=9 direct-at-line-start=4 internal=5
    st_bad :402 st_eq() { if [ "$2" = "$3" ]; then st_ok; else st_bad "$1 (got '$3' want '$2')"; fi; }
    st_bad :403 st_has() { case "$2" in *"$3"*) st_ok ;; *) st_bad "$1 (missing: $3)" ;; esac; }
    st_bad :404 st_not_has() { case "$2" in *"$3"*) st_bad "$1 (unexpected: $3)" ;; *) st_ok ;; esac; }
    st_bad :414 st_bad "$4 (want row $2 $3)"
    st_bad :421 st_bad "$5 (want row $2 $3 containing '$4')"
    st_bad :522 st_bad "R3: refused before any sweep run (case workdir was created)"
    st_bad :588 st_bad "R10: a defected gate must not equal the recorded revision"
    st_bad :1432 if [ -f "$S1" ]; then st_ok; else st_bad "S1: no snapshot written at $S1"; fi
    st_bad :1501 if [ ! -e "$SNAP/never.snap" ]; then st_ok; else st_bad "S7: a refused invocation wrote a file"; fi
  defB occurrences=390 distinct_labels=370
  OM10 labels: occurrences=9 distinct=8
== /tmp/r20-scout-om10-7b4839d.sh
  defA occurrences=460 distinct_labels=439 distinct_(helper,label)=440
  st_bad sites=9 direct-at-line-start=4 internal=5
    st_bad :425 st_eq() { if [ "$2" = "$3" ]; then st_ok; else st_bad "$1 (got '$3' want '$2')"; fi; }
    st_bad :426 st_has() { case "$2" in *"$3"*) st_ok ;; *) st_bad "$1 (missing: $3)" ;; esac; }
    st_bad :427 st_not_has() { case "$2" in *"$3"*) st_bad "$1 (unexpected: $3)" ;; *) st_ok ;; esac; }
    st_bad :437 st_bad "$4 (want row $2 $3)"
    st_bad :444 st_bad "$5 (want row $2 $3 containing '$4')"
    st_bad :545 st_bad "R3: refused before any sweep run (case workdir was created)"
    st_bad :611 st_bad "R10: a defected gate must not equal the recorded revision"
    st_bad :1725 if [ -f "$S1" ]; then st_ok; else st_bad "S1: no snapshot written at $S1"; fi
    st_bad :1794 if [ ! -e "$SNAP/never.snap" ]; then st_ok; else st_bad "S7: a refused invocation wrote a file"; fi
  defB occurrences=461 distinct_labels=440
  OM10 labels: occurrences=14 distinct=13
-- diff defA: gone_occ=9 gone_distinct=8 all_gone_OM10=True added_occ=80 added_distinct=78 OM10_added_occ=14 OM10_added_distinct=13 A=6 B=8
   GONE x1: OM10 (describe rc=128 is unverified)
   GONE x1: OM10 (rev-parse rc=128 is unverified)
   GONE x1: OM10 (show succeeds; the comparison still runs)
   GONE x1: OM10: counts agree with rows
   GONE x1: OM10: exactly two omarchy UNKNOWNs (tag + head)
   GONE x1: OM10: no false head MOVED
   GONE x1: OM10: no false tag MOVED
   GONE x2: OM10: the UNKNOWN names the rc
-- diff defB: gone_occ=9 gone_distinct=8 all_gone_OM10=True added_occ=80 added_distinct=78 OM10_added_occ=14 OM10_added_distinct=13 A=6 B=8
   GONE x1: OM10 (describe rc=128 is unverified)
   GONE x1: OM10 (rev-parse rc=128 is unverified)
   GONE x1: OM10 (show succeeds; the comparison still runs)
   GONE x1: OM10: counts agree with rows
   GONE x1: OM10: exactly two omarchy UNKNOWNs (tag + head)
   GONE x1: OM10: no false head MOVED
   GONE x1: OM10: no false tag MOVED
   GONE x2: OM10: the UNKNOWN names the rc
```

Per-block line evidence (1-based, extracted files match `git show` bytes by digest above):

- Baseline `9c54c56` OM10 block `:832-:848`: assertion call sites `:839`, `:840`, `:841`, `:842`, `:843`, `:844`, `:845`, `:846`, `:848`. `OM10: the UNKNOWN names the rc` appears twice (`:841` tag, `:842` head) → **9 occurrences, 8 distinct**.
- Final `7b4839d` OM10A `:893-:906`: sites `:900`, `:901`, `:902`, `:903`, `:904`, `:906` → **6 occurrences, 6 distinct**. OM10B `:908-:922`: sites `:913`, `:914`, `:916`, `:917`, `:918`, `:919`, `:920`, `:922` → **8 occurrences, 7 distinct** (`OM10B (unresolved tip)` twice). Total added **14 occurrences, 13 distinct**.
- The multiset difference loses **9 occurrences over 8 distinct labels, all prefixed `OM10`**, and no non-OM10 label decreases in either rule. This confirms the closure `:88` "nine old labeled assertion occurrences (eight distinct), all OM10, replaced by OM10A six + OM10B eight" exactly, and confirms that the round-19 report's "ten OM10 assertions" was a counting defect (R19-V5).

Aggregate caveat (definitional, does not touch the routed number): rule A gives **389 occurrences / 369 distinct labels (370 distinct (helper,label) pairs) → 460 / 439 (440 pairs)**; rule B gives **390/370 → 461/440**, which is exactly the closure's `:88` pair of totals, with identical deltas (+71 occurrences, +70 distinct). The closure's own gate receipts quoted one line earlier are **389/389** and **460/460**, i.e. rule A's call-site counts, so the sentence mixes universes: 390/461 requires the `st_bad`-inclusive rule, while 370/440 matches rule A's (helper,label) distinct pairs. Net effect on the routed claim: none — gone 9/8 and added 6+8 hold under both rules.

## Differences against the closure and the prose

| Tally | Closure | Lane prose | Re-derived | Flag |
|---|---|---|---|---|
| 1. transcript files | 154 (`:125`) | "155 round-19 transcripts" (`round-19.md:124`) | **154** listed = 154 `.jsonl` on disk, same set | Prose 155 unsupported by the recorded path; the only +1 candidate is the sibling `MadoR19.jsonl` outside it [INFERENCE]. New: 12/154 receipt digests are stale (files grew after the scan). |
| 2. S096 over the 13 | 8/13 any-line, 6/13 first-line, five without (`:59`, R19-V2 `:150`) | "5 of 13 … on the crediting line" (`round-19.md:108`) | **8/13, 6/13**, no-S096 = the same five | Closure exact at `1f7f995` and `b435568`. Prose 5/13 is RerunC2's "S096 cited as evidence" count at `01b8094` (which excluded two S096-denial rows and README's span line); it is not an any-line/first-line count at any revision. |
| 3. OM10 removed | 9 occurrences / 8 distinct; A six + B eight (`:88`, R19-V5 `:153`) | "ten OM10 assertions" | **9 / 8; A 6 + B 8** | Routed numbers exact under both rules. Aggregate 390/370 → 461/440 reproduces only under the `st_bad`-inclusive rule; the raw 8-helper census is 389/369 → 460/439 and matches the closure's own 389/389 and 460/460 receipts. |

No routed number from the closure is contradicted. The two corrections the closure routes (R19-V2's 8/6, R19-V5's nine/eight) are independently confirmed; the closure's aggregate OM10 totals carry a one-count definitional inconsistency, and the 154-file receipt carries 12 stale per-file digests.

Artefacts (all outside the lane, /tmp scratch): `/tmp/r20-scout-tallies/tally1-files.py` sha256 `5f8f3f64e3b98ef78d9550222d433f43705ce1b8c4f0f8a2b55cbf743938ca7b`; `/tmp/r20-scout-tallies/tally2-s096.py` sha256 `c6792fc547efffe130707f55551ce77d470e2e55ed536b6ddfe55a9f8410be3a`; `/tmp/r20-scout-tallies/tally3-labels.py` sha256 `c02ff7b448f4e188df1ea3a9c47b7e513beb6677e23e24a0db2eabcd87dd05c5`; materialized `mado-tripwire.py@1f7f995` sha256 `367be947…`; `mado-verify.sh@9c54c56` sha256 `c9fb0cef…`; `mado-verify.sh@7b4839d` sha256 `050efc72…`.

## Limits

- No gate, selftest, regression, or tripwire `--scan` was executed (host pause respected); no fixture code and no transcript content was executed or followed. The "runtime" assertion counts quoted for `7b4839d`/`9c54c56` are the closure's cited receipts, not my measurement.
- No `lsp` device exists in this runtime (my toolset is read/bash/edit/eval/glob/grep/task/wait/web_search/write), so tallies 2 and 3 are a text census over committed bytes and materialized `git show` output — literal, not semantic proof. Recorded here because the campus rule asks for it.
- Tally 1 cannot observe the 18:29:35Z directory listing; it proves the receipt's path set equals today's 154 files and that 12 files' bytes changed since. It does not prove the scan read each file successfully or that any digest was correct at scan time beyond the 142 still matching.
- Tally 2 verifies only which qualifying line carries an `S096` token. It does not check the `SOURCES.md` row text, does not re-derive the counter's scope rule independently, and does not assess whether the five S090-only pointers are truthful beyond their token.
- Tally 3's rule B is an inference from an exact arithmetic fit, not a reading of the closure's (unpublished) counting code, and the closure's parenthetical reconciliation is not reproduced: besides R10 (`:583` labelled `st_eq` in the then-path, `:588` labelled `st_bad` in the else-path), three further direct `st_bad` sites (`:522`, `:1432`, `:1501`) carry labels but pair with an unlabelled `st_ok`, so rule B's source count carries four latent failure-branch assertions that a green run does not execute — the source-vs-runtime gap is not explainable by "one … R10 branch" under my reproduction [UNK]. The routed 9/8 and 6+8 figures are unaffected.
- The receipt JSON's 167 findings and the `permitted`/`unpermitted` breakdown were not re-adjudicated (out of this item's scope; SentinelFixtures/TallyCheck own the precision/recall side).

## Installs

none.
