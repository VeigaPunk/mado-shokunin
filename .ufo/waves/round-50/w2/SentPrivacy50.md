# SentPrivacy50 — privacy shape of the round-50 committed bytes (w2, falsify)

Seat `SentPrivacy50` (sentinel, leaf — no dispatch), mado round 50 / w2, 2026-10-27. Attacked: the whole round-50 tree at
`b4a79843cc2545bbe800db9322e58f6e00436629` (landed tip), with the installed v3 gate
`quality/check-session-material.py` sha256 `ffdc9d62c387050e016cf9d0eaacbf87f37d6647021cbd2c492eb6328dddbb61` (identical at
tip and at data `906178b6`; equals the frozen registration hash). Every number below is a command output; every
`Report:`-relative path named here exists in this seat dir. Nothing reproduces a host value: account → `<ACCOUNT>`,
`/home/<ACCOUNT>` → `<HOME>`, and no title, device name, serial, program name or path text is printed.

Scratch `/fast/scratch/hyaku/mado-r50/SentPrivacy50/` (`git clone -q --shared`, `git -C … rev-parse --show-toplevel`
printed the clone path before any use; `TMPDIR`, `HOME`, `XDG_*` inside it; `ulimit -f 65536` on every writer shell). Tool
installs: none.

## 0. Verdict

1. **The gate's claim holds, and the lane is red anyway.** At `b4a79843`, `--scope all --account <account>`:
   `files=23920 findings=235`, `SESSION_MATERIAL_WAIVED: findings=49 files=47`, rc 1 — every rule family fires, no rule is
   silently dropped, and no finding is emitted outside `.ufo/`, `corpus/`, `quality/` (0 in `tools/`, `SCORECARD.md`,
   `LOG.md`). Nothing here falsifies `PRED-C2-r50`; the frozen predicate scores fixture families, and I re-proved the
   families it names with independent fixtures (§5).
2. **Four RAW values landed in round-50 committed bytes, and the gate sees one of them:**
   F1 two absolute home paths in `receipts/census-before.txt:19` / `census-after.txt:20` (gate: 0 findings), F2 two `ls -l`
   rows carrying the account in the owner/group columns of `w1/ScrCorrectionsR50/receipts/d2-seat-state.txt:58-59`
   (gate: `R8_ACCOUNT_COLUMN rows=2` — the round's only true-positive privacy finding, and w1 had already recorded it
   before the data commit), F3 two **new** `corpus/` lesson lines carrying an absolute home path (gate: 0 findings).
3. **The census pair therefore does not meet "counts and digests only".** `binds-live-r50.txt`, `axis-base.txt` and
   `operator-state-before.txt` do (counts, sha256, sizes, `~`-masked paths, one entry count; §4). The after-ledger is not
   committed at this rev at all (F6).
4. **Instrument defect found by running the gate twice:** a `kind=gate-copy` waiver is honoured at base and rejected at the
   tip with the same gate bytes and the same blob, because the waiver compares the copy against the gate *at the scored
   rev* — so bumping the gate silently invalidates every historical copy (−3 waivers, +3 findings), and the copy that is
   byte-identical to the new gate has no registry row (+3 more). 7 new findings vs base, 1 of them real (F5).
5. No device name, window title, monitor serial, process table, exec-cache record or Hyprland instance signature appears in
   any round-50 committed file: R1/R3/R5/R9 round-50 count is 0 (the three R1/R2/R3 hits are a gate copy's own positive
   fixtures), a serial-shape scan of the whole wave dir returns 0 tokens, and `"title"`/`"serial"` JSON fields exist only
   inside the gate copy's selftest constants.

## 1. The run (receipts: `gate-v3-all-at-*.txt`; `raw-values-additions-and-negatives.txt` for the added-line check and the
negative scans)

| rev | command | result |
|---|---|---|
| `b4a79843` (tip) | `python3 -I quality/check-session-material.py --repo <clone> --rev b4a79843 --scope all --account <account>` | `files=23920 findings=235`, waived 49/47, rc 1 |
| `906178b6` (data) | same, `--rev 906178b6` | `findings=235`, waived 49/47, rc 1 — identical tally |
| `8ae47b95` (base) | same, `--rev 8ae47b95` | `findings=228`, waived 52/48, rc 1 |

Rule tally at the tip: `R1=42 R2=42 R3=15 R4=3 R7=49 R8=55 R9=4 R5=25` (sum 235). R6 was **not** exercised: it needs
`--serial-from-host`, which runs `hyprctl monitors all -j`, and that verb is outside this seat's read allowlist
(`version|binds -j|getoption|devices -j`). That is a declared limit of this evidence, not a pass.

## 2. Classification of the 235 findings (rule × path prefix, shape-only)

Full table in `receipts/classification.txt`. Summary:

| prefix | R1 | R2 | R3 | R4 | R5 | R7 | R8 | R9 | total |
|---|---|---|---|---|---|---|---|---|---|
| `.ufo/waves/round-50/` (expected lane) | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | **4** |
| `.ufo/waves/<older round>/` (round-13…49 — **outside** the permitted lane list) | 40 | 38 | 13 | 3 | 22 | 49 | 54 | 4 | **223** |
| `corpus/` (expected lane) | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | **3** |
| `quality/` (expected lane) | 1 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | **5** |
| `tools/`, `SCORECARD.md`, `LOG.md` | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |

- **Outside the permitted lanes: 223**, all under `.ufo/waves/round-13 … round-49` (per-round counts in the receipt:
  round-48 41, round-35 26, round-47 25, round-37/round-43 23 each, round-46 22, round-32 18, round-23 12, round-45 9,
  round-44 5, round-49 4, eight rounds ≤2). None is new this round; they are prior-round fixtures, gate copies and receipts
  that the round-50 freeze inherited. **Zero findings exist outside `.ufo/`, `corpus/`, `quality/`** — so the v3 widening to
  `--scope all` finds material outside `.ufo/` and nothing outside the three expected roots.
- The three `corpus/` R5 hits are pre-existing serial-shaped prose tokens in `config-health-report-r3.md` (last touched
  round 19), `hyprctl-verification-layer.md` (round 26) and `hyprland-config-plane.md` (probation round 2) — not round-50
  bytes.
- The five `quality/` hits are the gate's own positive fixtures (`quality/check-session-material.py` R1/R2/R3) plus two
  older counters' `ss` transcript fixtures (`c2-r37-eventq.py` rows=9, `c2-r38-eventq.py` rows=12). The gate is red on
  itself by construction; the round-50 tally therefore is not a leak tally (F5).

Round-50's four findings, by path and rule:

| file | rule | detail | classification |
|---|---|---|---|
| `w1/ExecGateV3/check-session-material.py` | R1 / R2 / R3 | `objects=4`, `rows=3`, `objects=1` | the wave copy of the gate, **byte-identical** to the installed gate (`ffdc9d62…`), and its embedded selftest constants; unwaived |
| `w1/ScrCorrectionsR50/receipts/d2-seat-state.txt` | R8 | `rows=2` | **real red**: two `ls -la` rows with the account in owner/group (F2) |

## 3. RAW values in committed round-50 files

Census command (masked output, `receipts/raw-value-census-masked.txt`):
`git grep -o -F <needle> b4a79843 -- '.ufo/waves/round-50/'` for needle = the invoking account and `/home/`.

| needle | occurrences | files |
|---|---|---|
| account name | **354** | 43 |
| `/home/` literal | **482** | 62 |

Distribution (both needles, 836 occurrences): `.ufo/waves/round-50/w1-spec.json` 274 and `w1-dispatch.json` 274 (137 of each
needle — the seat prompts quote the lane's absolute path), other top-level wave files 26 (`make-w1-spec.py` 20,
`registration.md` 4, `w1.ready` 2 — 10+10, 2+2 and 1+1 per needle), `w1/<seat>/` trees 254, `receipts/` 4, `freeze/` 4.

**Receipt-content raw values (the ones that matter).** Occurrence counts, masked lines quoted ≤25 words:

- **F1 — `receipts/census-before.txt:19`, `receipts/census-after.txt:20`** — a tab-joined record row
  `mado→ok→/home/<ACCOUNT>/Projects/shokunin/mado-shokunin/corpus/SOURCES.md`. Raw absolute home path in the committed
  round record; introduced by `13631f24` (before, `git log --diff-filter=A`) and by the freeze `470bfd77` (after). The gate
  reports **0 findings** for both files. Severity: medium — the path discloses the account name and the lane location, and
  it is exactly the class this round's C2 moved; it is *inside the gate's declared blind class*
  (`quality/check-session-material.py:186`, "a path in a non-``ls`` row"), so it is not a claim violation — but the lane's
  own convention (`~` in receipts, `SKILL.md:343` rule 4) is broken in a committed receipt.
- **F2 — `w1/ScrCorrectionsR50/receipts/d2-seat-state.txt:58-59`** — two `drwxr-xr-x 1 <ACCOUNT> <ACCOUNT> … .` / `..` rows
  (`ls -la` of a seat directory), plus a prose home path on line 1. `R8_ACCOUNT_COLUMN rows=2`. Present at the data commit
  `906178b6` and at the tip. w1's own sentinel recorded this exact red as a must-fix *before* the data commit
  (`.ufo/waves/round-50/w1/SentPrivacy.md:28`, detailed at `:88`); the fix did not land, so the freeze ships a red it had
  already named. Five account occurrences in the file: the prose path on line 1 and two owner/group columns on each of the
  two rows.
- **F3 — two lines added this round in `corpus/`:** `corpus/lessons/round-49.md` (the D8 erratum's counting command,
  `L=/home/<ACCOUNT>/…`) and `corpus/lessons/round-50.md:87` (the census command, `--root /home/<ACCOUNT>/…`). Both are
  `git diff 8ae47b95 b4a79843` **additions** (`grep '^+' | grep -F /home/<ACCOUNT>` = 2, both listed). The gate reports 0
  findings on both. Severity: low — a command in a code span, but it is a home path in committed bytes added by this round.
- **F4 — a systematic, unmasked-command convention break in w1 receipt/log trees** (per-file counts from the census
  receipt; `acct`+`home` occurrences): each `ExecC1Cheats/logs/*.txt` carries 1+1 — one `lane=/home/<ACCOUNT>/…` field on its
  `clause=meta` line — and `logs/summary.txt` 12+12, including two `sha256sum` output rows whose second column is an absolute
  home path (a digest row that is not digest-only); `ScrRowsR50/census-r50.txt` 4+4 (a `$ cmd` transcript), `d3-figure.txt`
  2+2, `criteria-red-green.txt` 0+8, `ExecLiveR50.md` 4+4, `ExecHostGuardR50.md` 1+3, `ExecFetchR50/fetch-all.sh` 1+1
  (`LANE=${LANE:-/home/…}`), `SentHostState.md` 1+2, and one pair each in `CritC2Scope.md`, `CritGateLesson.md`,
  `ScrCorrectionsR50/corrections.md`, `ScoutCensus.md`, `ScrRowsR50/rows.md`, `SentScratch.md`. All are `$ cmd` /
  `field=value` / variable-default echoes: structural-enough that the lane masks them with `~` elsewhere
  (`operator-state-*.txt`), and the gate is blind to them by design (§5, fixture E). Severity: low per file, medium as a
  class — it is the lane convention, not a host secret, but it makes the account name readable in 43 committed files.

**Not found (negative results, each a rule with 0 round-50 hits):** device name (`switch:` appears only as a *form name* in
`corpus/knowledge/hyprland-bind-key-match-r50.md:50,71,107` and as upstream source in `fetch/` pins), window title
(`"title"` only in the gate copy's fixtures), monitor serial (R5 round-50 = 0; independent shape scan
`[0-9]{2,6}[A-Z]{3,8}[0-9]{3,7}` over `.ufo/waves/round-50/` = 0 tokens), process table (R2 round-50 = 0 outside the gate
copy), exec-cache record (R9 round-50 = 0), instance signature (`instance:`/`instance=` = 0; the one
`/run/user/N/hypr/INSTANCE/.socket.sock` hit is a **masked** trace placeholder in
`w1/SentHostState/receipts/hyprctl-readonly.txt:8`), and home listing (R4 round-50 = 0).

## 4. The host receipts carry counts and digests only — except the census pair

`receipts/host-receipts-shape.txt` (line counts, needle counts, trackedness; no content printed):

| receipt | lines | `/home/` | account | serial shape | verdict |
|---|---|---|---|---|---|
| `receipts/binds-live-r50.txt` | 34 | 0 | 0 | 0 | **PASS** — version line, method, 192-bind count split, modmask histogram, one sha256 over the 90,401 raw bytes (not embedded), the keycode list, 3-stability note |
| `receipts/axis-base.txt` | 5 | 0 | 0 | 0 | **PASS** — three axis rows, `checked=3 mismatched=0`, rev |
| `receipts/operator-state-before.txt` | 7 | 0 | 0 | 0 | **PASS** — `~`-masked paths + sha256/size/mtime + one entry count |
| `receipts/operator-state-after.txt` | — | — | — | — | **not committed at `b4a79843`** (untracked, F6) |
| `receipts/census-before.txt` / `census-after.txt` | 20 / 21 | **1** | **1** | 0 | **FAIL** — one record row carries a raw absolute home path (F1) |

`binds-live-r50.txt` also passes the two harder tests: its only line matching `device|description=|dispatcher=` is its own
negative claim (line 33, "no device name, window title, dispatcher argument, bind description or home path appears in this
file"), and the digest it publishes (`9a47199e…`) is a digest, not a value.

## 5. Blindness re-proved with independent fixtures (`receipts/gate-blindspot-fixtures.txt`)

Six throwaway repos, `git init`, `rev-parse --show-toplevel` asserted, fake account `sandboxuser`, fake home
`/home/sandboxuser`, gate = installed bytes:

| fixture | content | gate |
|---|---|---|
| A | one tab-joined record row `mado→ok→/home/sandboxuser/x/corpus/SOURCES.md` | `findings=0` — **blind to F1's shape** |
| B | 12 distinct bare `/home/...` lines | `R4_HOME_LISTING count=12 distinct_paths=12 limit=10` — caught |
| C | `path:LINE: text` (grep-n prefix) | `R7_HOME_PATH_PREFIX forms=prefix:1` — caught |
| D | the committed `census-before.txt` bytes, account masked to the fake user | `findings=0` — **the committed file is invisible** |
| E | `cd /home/sandboxuser/Projects/x && python3 …` (a receipt's `$ cmd` echo) | `findings=0` — **blind to F4's shape** |
| F | `--dir=/home/sandboxuser/projects` single field (cache record) | `findings=0` — R9 needs two record fields |

So the three frozen families the predicate names are real discriminators (B, C and the R8 live hit), and the two shapes this
round actually committed (A/D, E) are outside the gate by construction. The gate's own "deliberate limits" paragraph names
the class (`quality/check-session-material.py:186`, "a path in a non-``ls`` row") but with `stat` as the example, not a tab-joined census row — a reader cannot infer
that the round's own census shape is uncovered.

## 6. F5 — a gate bump silently un-waives every historical gate copy

`receipts/waiver-regression.txt`. Three facts, each a command: the installed gate at base is `82c9053a…` (v2) and at the tip
`ffdc9d62…` (v3); the round-48 gate copy is byte-identical (`82c9053a…`) at both revs; and the registry row that covers it
(`quality/session-material-waivers.txt:49`, `kind=gate-copy`) is *honoured* at base and *rejected* at the tip with
`reason=gate-source-mismatch`. Cause at `quality/check-session-material.py:902-909` (with `:265` `DEFAULT_GATE_SOURCE`):
the copy is compared against `quality/check-session-material.py` **at the scored revision**, so every historical copy loses
its waiver the moment the gate changes — and the copy that is byte-identical to the new gate has no registry row, so it is
a finding as well.

Net at the tip vs base (set difference of the two runs): **7 new findings, 0 gone** — 3 the invalidated round-48 copy, 3
the unregistered round-50 wave copy, 1 the real `d2-seat-state.txt` red. Consequence for the round record: the published
`findings=235` contains **6 findings that are the gate's own test data** (`quality/check-session-material.py` 3 +
`w1/ExecGateV3/check-session-material.py` 3), and the count grows monotonically with every gate version. Not a falsification
of C2 (the predicate scores nonce fixtures, and both nonce runs are consistent with it), but it is a measurement defect an
L1 should not carry forward: either waive by (path, digest, rules) without the rev-time gate compare, or register the new
copy at the same commit the gate lands.

## 7. F6 — four freeze-cited receipts are not committed at `b4a79843`

`git ls-files --error-unmatch` fails and `git status --porcelain .ufo/waves/round-50/receipts/` shows `??` for:
`receipts/selftests.txt`, `receipts/check100-r50.txt`, `receipts/check101-w1.txt`, `receipts/operator-state-after.txt`.
They exist in the lane working tree only, so they are not citable evidence at any rev and are absent from a clone of the
tip — the after-ledger, the 94/94 + 45/45 + 58/58 selftest receipt and both QUALITY-criteria receipts (100, 101) cannot be
replayed by a w2 seat. Severity: medium for provenance, none for privacy (the working-tree after-ledger is itself
`~`-masked, sha256+size+mtime+count only).

## 8. Residuals and limits of this seat

- R6 (`--serial-from-host`) unexercised: it needs `hyprctl monitors all -j`, outside this seat's read allowlist. A host
  monitor serial is therefore *not* excluded by this receipt, only by R5's shape rule (0 round-50 tokens).
- The gate reads tracked bytes only: untracked/ignored round-50 files (F6) are unscored.
- Text rules only; binary blobs (NUL in the first 8 KiB) and the tail of any blob >16 MiB are skipped by the gate's own
  declaration. No tracked round-50 blob is near that cap (largest is 324,906 B, `fetch/xkbcommon-ks_tables.h`), so the size
  cut is unreachable this round; binary skipping is not, and I did not enumerate binary blobs.
- I read the wave dir at the rev through `git grep`/`git show`; I never wrote a tracked file, never ran a mutating git
  command in the lane or the fleet, and never launched a GUI program or a mutating compositor verb.
- No remediation applied: the L1 owns the fix. Smallest fixes, in order: add the v3 `kind=gate-copy` row for
  `w1/ExecGateV3/check-session-material.py`; mask the two census rows' `mado ok` tail to `~`; replace
  `d2-seat-state.txt`'s two `ls -la` rows with `ls -ln`; commit (or drop) the four untracked receipts; mask the two new
  `corpus/lessons/` command paths.
