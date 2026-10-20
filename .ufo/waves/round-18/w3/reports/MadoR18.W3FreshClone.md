# MadoR18.W3FreshClone — residual non-author checks (round 18, final `a210241`)

Role: UFO-FSD reviewer, non-author. Target: lane `mado-shokunin`, branch
`master`, final commit `a210241b5429fb3c3f9ad23f42863d6e6d9e5845`
(earlier `d9a5a18` baseline, `4c103b5` integration, `abfbf35` receipts,
`be886a3` wave-2 integration). Method: fresh `git clone` to `/tmp/w3fresh`,
`git checkout a210241`, every command run there; read-only git only; no jj;
no delegation. Install/update: none (`gitleaks` already at `/usr/bin`).

**Verdict: no divergence from the SCORECARD round-18 measured results.** All
four required commands reproduce exactly, and every harm-watch count and
capability control I could run reproduces. Three low-severity documentation
drifts and one medium write-scope defect are recorded below; none changes a
measured claim.

## 1. Required checks (exact commands, cwd `/tmp/w3fresh`)

### 1.1 receipt-check
```
$ python3 -I .ufo/waves/round-18/receipt-check.py
RECEIPT r17-tripwire-r13 MISSING_PROVENANCE
RECEIPT r17-tripwire-r14 MISSING_PROVENANCE
RECEIPT r17-tripwire-r15 MISSING_PROVENANCE
RECEIPT r17-tripwire-r16 MISSING_PROVENANCE
RECEIPT r17-tripwire-anchor-r15 MISSING_PROVENANCE
RECEIPT r17-tripwire-pacmanlog-join MISSING_PROVENANCE
RECEIPT r18-fixture-ok ok
RECEIPT r18-fixture-bad-sha SHA_MISMATCH
RECEIPT r18-fixture-stale-rev SHA_MISMATCH
RECEIPT r18-fixture-stale-tool STALE
RECEIPT r18-fixture-nonancestor NOT_ANCESTOR
RECEIPT r18-fixture-producer-mismatch PRODUCER_MISMATCH
RECEIPT r18-tripwire-r13 ok
RECEIPT r18-tripwire-r14 ok
RECEIPT r18-tripwire-r15 ok
RECEIPT r18-tripwire-r16 ok
RECEIPT r18-tripwire-anchor-r15 ok
RECEIPT r18-tripwire-frozen-match ok
RECEIPT r18-tripwire-frozen-tampered ok
RECEIPT r18-tripwire-frozen-before ok
RECEIPT r18-measure-after ok
EXPECT_SUMMARY: 21/21
EXIT=0
```
**MATCH** with SCORECARD ("21/21 exit 0 with 6 round-17 reds
`MISSING_PROVENANCE`, `STALE`/`SHA_MISMATCH` controls"). The 21 printed
lines equal the 21 claims in `.ufo/waves/round-18/receipt-claims.json`
(6 r17 + 6 fixtures + 5 r18 re-cut + 3 frozen + 1 measure-after).

### 1.2 fetch-verify on the 21 credited rows
```
$ python3 -I .ufo/waves/round-18/fetch-verify.py --sources corpus/SOURCES.md \
    --rows S072,S073,S074,S075,S076,S077,S078,S079,S080,S081,S082,S083,S084,\
S085,S086,S087,S088,S089,S092,S093,S094
...
CONFLICT https://github.com/basecamp/omarchy/tree/v3.8.4/themes/matte-black sha256=3b18a612…,50c1ac25…,6b355a46…,8bfaba24…,de57cbaf…
CONFLICT https://github.com/basecamp/omarchy/tree/v3.8.4/themes/matte-black/backgrounds sha256=267618a4…,2d22e126…,369f9439…,9e1160a0…
CONFLICT https://github.com/omacom/omarchy/tree/v3.8.4/themes/matte-black sha256=3b18a612…,50c1ac25…,6b355a46…,8bfaba24…,de57cbaf…
CONFLICT https://github.com/omacom/omarchy/tree/v3.8.4/themes/matte-black/backgrounds sha256=267618a4…,2d22e126…,369f9439…,9e1160a0…
ROW S072 receipted … ROW S089 receipted
ROW S092 receipted … ROW S094 receipted
SUMMARY receipts=424 ok=329 bad=0 digest_only=95 non200=0 conflicts=4 \
rows=21 unreceipted=0 quotes=0 quote_bad=0
EXIT=1
```
**MATCH**: 21/21 rows receipted; the only failure cause is the four
per-fetch GitHub tree-HTML digests from S094's secondary anchor (basecamp and
`omacom` rename), exactly M7. `bad=0`, `non200=0`, `unreceipted=0`. Host
rows S090/S091/S095 are excluded from the row list by design; asking for
them alone prints `ROW S090|S091|S095 host/no-url` and still exits 1 solely
because the same 4 global conflicts remain.

### 1.3 token-join-check
```
$ python3 -I .ufo/waves/round-18/token-join-check.py a210241
RECEIPTS files=49 lines=424 seats=49 rows=95
JOIN S072 web receipts=9 sha=9755f955d5c4… anchor=ok seats=…
… (S072-S089, S092-S094: every line anchor=ok)
JOIN S090 host (anchor is a file-byte digest)
JOIN S091 host (anchor is a file-byte digest)
NOTE corpus/knowledge/walker-route-r18.md source_lines=1 tokens=20 unique=20 web=18 host=2 gaps=0
JOIN S092 web receipts=4 sha=68ed5503298f… anchor=ok …
JOIN S093 web receipts=7 sha=79069c8018a7… anchor=ok …
JOIN S094 web receipts=4 sha=dbdd13a629aa… anchor=ok …
JOIN S095 host (anchor is a file-byte digest)
NOTE corpus/knowledge/theme-route-r18.md source_lines=1 tokens=4 unique=4 web=3 host=1 gaps=0
SUMMARY rev=a210241b5429fb3c3f9ad23f42863d6e6d9e5845 notes=2 tokens=24 \
unique=24 web=21 host=3 gaps=0
RESULT PASS
EXIT=0
```
**MATCH**: 24 unique tokens, 21 web joins with receipt sha inside the row
anchor, 3 host rows, 0 gaps. `RECEIPTS lines=424` agrees with fetch-verify's
`receipts=424`.

### 1.4 measure at the final commit
```
$ python3 .ufo/waves/round-17/measure.py a210241
c1 {criteria: 26, lesson_cited: 18, score: 6.9231}
c2 {count: 6, score: 10.0, u_routes: 7, u_routes_seen: U1..U7, rejected: []}
c3 {tool_present: true, sha256: c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd}
EXIT=0
```
**MATCH** with SCORECARD (c1 18/26 = 6.9231, c2 6/6 = 10.0).
Re-measured the before/after points in the same clone:
`d9a5a18` → c1 15/23 = 6.5217, c2 4/6 = 6.6667, u 7;
`be886a3` → c1 18/26 = 6.9231, c2 6/6 = 10.0 (identical to `a210241`, as
declared). A block-level ("semantic") count over QUALITY.md gives 18/23 at
`d9a5a18` and 21/26 at `a210241`, matching SCORECARD's semantic row.

## 2. Additional non-author reproductions (all at `a210241` unless noted)

| Claim | Command | Observed |
|---|---|---|
| gate selftest 389/389 | `bash tools/mado-verify.sh --selftest` | `MADO_SELFTEST: 389/389 assertions passed`, exit 0 |
| gate moved 372 → 389 (+17, none dropped) | `git show d9a5a18:tools/mado-verify.sh > /tmp/gate-d9.sh; bash /tmp/gate-d9.sh --selftest` | `MADO_SELFTEST: 372/372 assertions passed`, exit 0 |
| OM9/OM10 UNKNOWN-with-rc bite | `grep -n 'OM9\|OM10' tools/mado-verify.sh` | scenarios at 811-840 assert `UNKNOWN`, `rc=128`, and `st_not_has … "local edit"` |
| red-before `git show` rc=128 | read `evidence/gate-rc-redbefore.txt` §1 | old gate prints FAIL "local edit" against `e3b0c44298fc…`, exit 1 |
| regression 10/10 PASS | `MADO_VERIFY_HARNESS=/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh bash tools/mado-verify.sh --regression` | `MADO_REGRESSION: PASS`, `killed=10/10 flips=0 inconclusive=0`, target pin `20714096…` match=yes, exit 0 (93.9 s) |
| classifier 52/52 | `python3 -I tools/mado-action-plan.py --selftest` | `SELFTEST_SUMMARY: 52/52 passed`, exit 0 |
| tripwire scan suites | `--selftest .ufo/waves/round-17/tripwire/{core,compound,hardening,w2-regressions}` and `.ufo/waves/round-18/tripwire/r18-failsafe` | 9/9, 16/16, 33/33, 30/30, 1/1, all exit 0 |
| frozen suite 31/31 | `python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-18/tripwire/frozen` | `SELFTEST_SUMMARY: 31/31 passed`; `SELFTEST_SCRIPT_SHA256: c1ae45a7…` |
| abfbf35 tool 17/31 | `git show abfbf35:tools/mado-tripwire.py > /tmp/tw-abf.py; python3 -I /tmp/tw-abf.py --selftest …/frozen` | `17/31 passed`, 14 named failures; script sha `c87a31ef…` |
| `--frozen` usage at baseline | `git show d9a5a18:tools/mado-tripwire.py > /tmp/tw-d9.py; python3 -I /tmp/tw-d9.py --frozen .ufo/waves/round-18/frozen` | usage + `MADO_TRIPWIRE: could_not_evaluate`, exit 2 |
| frozen match | `python3 -I tools/mado-tripwire.py --frozen .ufo/waves/round-18/frozen` | `frozen_match`, 5 inputs ok, exit 0 |
| one-byte tamper | copy, append one byte to `inputs/r15-libinput-events.jsonl`, rerun | `snapshot_tampered`, `inputs[0].ok=false`, exit 2 |
| frozen provenance match | `python3 -I .ufo/waves/round-18/frozen-provenance-check.py` | `MADO_FROZEN_PROVENANCE: match`, 228 indexed sources, exit 0 |
| mutant bite 6/6 | `python3 -I .ufo/waves/round-18/measure-mutants.py` | `bites 6, no_bite [], expectations_met 6, baselines_agree true`, exit 0; each record has `diff_sha256`, `instrument_sha256`, loose `a280b3ab…`, tight `de4c422b…` |
| navigation 34/34 | extract the `### Counting command` bash block from SCORECARD (`sha256 8b59b503…` = the receipt's `tool_sha256`) and `REV=<rev> bash -s` | `d9a5a18` 32/32 exit 0; `be886a3` 34/34; `a210241` 34/34; missing/dangling/duplicates 0 |
| sources 71 → 95 (A 64 → 88; mined 56 → 80) | parse `## Registry` at both revisions | `d9a5a18` rows 71 / A 64 / mined 56; `a210241` 95 / 88 / 80 |
| QUALITY append-only | `git diff --numstat d9a5a18 a210241 -- corpus/QUALITY.md` | `39 0` (39 added, 0 removed); criteria 24-26 plus the wave-2 correction appended at the tail |
| one canonical measure instrument | `git show REV:.ufo/waves/round-17/measure.py \| sha256sum` for `d9a5a18,4c103b5,be886a3,a210241` | `de4c422b…` at all four |
| labelled tool shas | `git show REV:tools/mado-tripwire.py \| sha256sum` | `962919ce…` d9a5a18; `c87a31ef…` 4c103b5 and abfbf35; `c1ae45a7…` be886a3 and a210241 |
| gate shas / pins | blob shas; `PIN_MADO` in gate | `fba82a66…` at d9a5a18 → `c9fb0cef…` at final; `PIN_MADO='20714096…'`, `TABLE_MADO` 10 KILLED |
| 24/24 non-author re-opens agree | compare each lesson `- GATE \| Sxxx …` sha to the `GATE` line in `w2/reports/ReopenSxxx.md` | 24 lesson lines, 24 report files, 0 mismatches; all 24 report GATE lines contain `agree:` |
| retained bodies licensed | cross-check every `receipts.jsonl` line against `fetch/RETENTION.json` | 424 receipt lines = 329 present bodies + 95 absent; every present body has `retain=commit` and a `license`; every absent body is `retain=digest-only`; 0 mismatches (RETENTION carries 432 entries = those 424 + 8 `.nocommit`/extra rows) |
| gitleaks clean | `gitleaks detect --source .ufo/waves/round-18/fetch --no-git --redact --no-banner` | `no leaks found`, 4.05 MB, exit 0 |
| census exit 0, three historical W04 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` | S030/S042/S045 W04 + `mado ok`, exit 0 (byte-identical to `harm-census-validate.txt`) |
| host pacman line | `sed -n '3161,3169p' /var/log/pacman.log` | `pacman -U …/zcode-3.16.2…` at `13:23:08-0300`, `pacman -D --asexplicit` at `13:23:09`; matches the lesson's operator-owned `[UNK]` actor claim |
| final delta scope | `git diff --stat be886a3 a210241` | 31 files, +1175/−0, only `evidence/`, `SCORECARD.md`, `corpus/lessons/round-18.md`, `LOG.md` |
| ancestry / tip | `git merge-base --is-ancestor …`; `git rev-parse master a210241` | d9a5a18, 4c103b5, be886a3 all ancestors; master = a210241 |
| quotes in credited bodies | `fetch-verify --quote` for S072/S077/S094 | `QUOTE … ok`; S092's body sha `68ed5503…` and S094's `dbdd13a6…` equal the row anchors |
| S093 secondary-URL quote | direct read of committed `fetch/ReopenS093/autostart.conf` | sha `acb6a668…` (row's secondary anchor) and line 5 contains the GATE quote |

Note: `fetch-verify --quote 'S093=…'` returns `NOT_FOUND` by design, because
the quote lives in `autostart.conf`, a secondary URL of row S093, and the
tool searches only bodies crediting the row's **first** URL. Verified
directly instead; this is a tool limit, not a false lane claim.

## 3. Findings

### 3.1 MEDIUM — `measure-mutants.py` writes the real lane from a fresh clone; registered write scope is false

- Code: `.ufo/waves/round-18/measure-mutants.py:42`
  `LANE_DEFAULT = Path('/home/vgpnk/Projects/shokunin/mado-shokunin')`;
  `:502` `out = args.out or (lane / OUT_DEFAULT)`; `:652-655` mkdir +
  `os.replace(tmp, out)`. The docstring at `:19` says "the lane is only read
  through git".
- Registry: `SKILL.md:571` write scope for `mado-measure-mutants`:
  "`/tmp` git clones only; never the lane".
- Reproduction (this review, from `/tmp/w3fresh`):
  `python3 -I .ufo/waves/round-18/measure-mutants.py` printed
  `wrote /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/evidence/measure-mutants.json`
  and changed that tracked file
  `58929eea…` → `0f861091…` (only run metadata differ: `generated_at`,
  workdir, argv, per-run mutant commit shas; semantics stayed 6/6,
  `no_bite []`).
- Consequence: a non-author reproducing criterion 25's runnable check
  silently mutates the author's checkout — the M5 misroot class — and the
  registry's write-scope cell cannot be relied on. The committed evidence is
  not invalidated (`diff_sha256` per mutant, both instrument shas, 6/6
  bites), but the check is not clone-safe as documented.
- Remedy: default `--out` relative to the script's own checkout
  (`Path(__file__).resolve().parents[3]`) and/or refuse a `--lane` that
  differs from the script root without an explicit `--out`; correct the
  SKILL write-scope cell.
- Restoration: I rewrote the file from
  `git show a210241:…/measure-mutants.json`; sha returned to
  `58929eea…`; `git status --porcelain` in the lane was empty at 16:30Z
  immediately after the restore. At 16:37Z the lane showed uncommitted
  appends by other seats (SCORECARD.md, SKILL.md, receipt-claims.json;
  mtimes 16:35:24–16:36:25Z), not written by this seat — see §5.

### 3.2 LOW — frozen-suite case count in the registry is stale (17 vs 31)

`SKILL.md:566` self-test cell: "… `--selftest
.ufo/waves/round-18/tripwire/frozen` (17 mode-frozen cases; exit and
first-line outcome)". The landed suite prints `SELFTEST_SUMMARY: 31/31
passed`, and SCORECARD itself records "frozen suite 31/31 (the `abfbf35`
tool 17/31)". The 17 is the pre-`TwFrozenHarden` count; the wave-2 hardening
added 14 cases. No measurement is wrong; the registry row should say 31 (or
"31 after hardening"). Concurrent sibling work observed while this review
ran already appends exactly that erratum to SKILL.md (uncommitted at 16:35Z);
I did not integrate it, and my clone stays at committed `a210241`.

### 3.3 LOW — SCORECARD overstates receipt formatting ("first line")

`SCORECARD.md:991-992`: "Every receipt's first line names `tool_sha256` and
`measured_commit` (QUALITY 24)." Counterexamples in the same claim set:
the six round-17 reds (`MADO_TRIPWIRE: findings` / `# Round-17 …`) and three
authored fixtures whose first line is a `#` comment
(`receipt-fixtures/ok-receipt.txt`, `producer-mismatch-receipt.txt`,
`stale-rev-receipt.txt`); the final
`evidence/final/tripwire-pacmanlog-join.txt` carries its producer on line 4.
The mechanism is deliberate: `receipt-check.py:89-97` requires the `tool=`
token only when the first line starts with `RECEIPT`, while
`tool_sha256`/`measured_commit` are searched over the whole text, and a
fixture's second/third lines do carry them. QUALITY 24 itself does not
require a first-line format, so the checker is not wrong — the prose is
unscoped and should say "every green re-cut receipt" or "every receipt that
claims a producer". Concurrent sibling work observed while this review ran
appends a matching correction to SCORECARD.md (16:36Z, uncommitted); it also
extends `receipt-claims.json` from 21 to 33 claims binding the
`evidence/final/` receipts. I did not integrate either change.

### 3.4 LOW — pre-registered C3 says the registry row "moves probe → gate"; landing adds a new gate row

`SCORECARD.md:974`: "the registry row moves `probe` → `gate`". At `d9a5a18`
no `mado-tripwire-frozen` row exists (`git show d9a5a18:SKILL.md` has zero
matches), and at final the `mado-tripwire` `--scan` row explicitly **stays**
a probe while `mado-tripwire-frozen` is added as a gate row. The results
table's "gate entry" wording is accurate; only the pre-registered mechanism
sentence describes a move that did not happen.

## 4. Residual risk and verification gaps

- Live behaviour, rendered UI and running binaries remain `[UNK]`: every row
  reproduced here is documentary or host-bytes, and no compositor, input or
  process probe was run (host pause). C2's 6/6 is saturation of its finite
  rubric, not behaviour coverage.
- `fetch-verify --quote` cannot check a quote located in a secondary-URL
  body (S093); those quotes need direct body reads.
- The regression re-run used the current sibling harness
  `fb6d86d5…`, while `evidence/regression-recut.txt` records `0673d2e5…`.
  The receipt marks the harness as provenance, not gated; the gated target
  pin `20714096…`, the 10-defect spec sha, and the 10/10 table all matched.
- M8 (14 wave-2 seats ended without a report) is not verifiable from lane
  bytes; no transcript audit was performed here.
- `RETENTION.json` has 432 entries against 424 receipt lines (8 extra
  digest-only/`.nocommit` rows). This is a different denominator than the
  SCORECARD's 329/95 receipt counts, not a contradiction.

## 5. Contract / incidents

- One lane write occurred, caused by finding 3.1: the documented
  `measure-mutants.py` command wrote the real lane's evidence file. It was
  restored byte-exact (`58929eea…`); `git status --porcelain` in the lane was
  empty at 16:30Z immediately afterwards. Disclosed rather than hidden.
- At 16:37Z the live lane had uncommitted modifications by other seats:
  `SCORECARD.md` +17/−0, `SKILL.md` +15/−0, `receipt-claims.json` +97/−0
  (mtimes 16:35:24–16:36:25Z), plus this report's `w3/` directory. None of
  those tracked changes are mine; they are append-only corrections from
  concurrent residual-check seats and were not reviewed or integrated here.
  All measurements in this report are bound to committed `a210241`.
- No jj command, no git write command, no delegation, no `agent://all`.
- No forbidden host command: no pacman/yay/paru/makepkg or package query, no
  sudo, systemctl, journalctl, hyprctl, walker, elephant, swaybg, omarchy,
  screenshot or input probe. `/var/log/pacman.log` and config trees were
  read as bytes; `tools/mado-verify.sh` was run only as `--selftest` and
  `--regression`.
- Installs/upgrades performed: none.

## 6. Commands run (complete)

Required: `python3 -I .ufo/waves/round-18/receipt-check.py`;
`python3 -I .ufo/waves/round-18/fetch-verify.py --sources corpus/SOURCES.md
--rows S072…S089,S092,S093,S094` (also the S090/S091/S095 variant and four
`--quote` variants); `python3 -I .ufo/waves/round-18/token-join-check.py
a210241`; `python3 .ufo/waves/round-17/measure.py {d9a5a18,be886a3,a210241}`.

Additional: `git clone`, `git checkout`, `git rev-parse`,
`git merge-base --is-ancestor`, `git show`, `git diff`,
`git diff --numstat`, `git ls-tree` (via scripts), `git status --porcelain`;
`bash tools/mado-verify.sh --selftest`; the same gate extracted from
`d9a5a18`; `MADO_VERIFY_HARNESS=… bash tools/mado-verify.sh --regression`;
`python3 -I tools/mado-action-plan.py --selftest`;
`python3 -I tools/mado-tripwire.py --selftest` on the five suites;
`--frozen` on the committed snapshot and on an exact one-byte tampered copy;
the `d9a5a18` and `abfbf35` tools on the frozen suite/CLI;
`python3 -I .ufo/waves/round-18/frozen-provenance-check.py`;
`python3 -I .ufo/waves/round-18/measure-mutants.py` (once);
the SCORECARD counting block via `REV=… bash -s`;
`gitleaks detect --source .ufo/waves/round-18/fetch --no-git`;
`sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`;
`sha256sum`/`sed`/`grep`/`awk`-class file reads over committed bytes and
`/var/log/pacman.log`; plus the restoration
`git show a210241:…measure-mutants.json > .ufo/…/measure-mutants.json`.
