# ScrToolLedger — the live-state tool ledger, every row re-derivable (round 49, w1)

Seat: `ScrToolLedger`. Target: `considerthese/2026-10-26.md` proposal 2, refused in round 47
(`corpus/lessons/round-47.md:336`) because the drafted ledger's rows were wrong (10 of 14: 4
substantive, 6 quote-only; `.ufo/waves/round-47/w2/ExecToolLedger.md` holes H1-H8). This seat
delivers the instrument the proposal needed: a ledger **generated** from git objects plus a checker
that re-derives every row and exits 1 on the first disagreement.

Base: `03e4ae76aff7a4be59cb69970dd553baa319695a`. Nothing here was run on the host; no compositor
call, no package transaction, no GUI program. No commit was made.

## 1. What was built

| file | what it is |
|---|---|
| `.ufo/waves/round-49/w1/ScrToolLedger/ledger.md` | the ledger: 12 rows + 3 exclusions, every quoted line copied out of git by the generator |
| `.ufo/waves/round-49/w1/ScrToolLedger/check-ledger.py` | the checker/generator: re-derives every row from `git ls-tree` / `cat-file` / `log` at a revision, emits the ledger (`--emit`), compares a committed copy to a fresh emit (`--ledger`), prints the candidate sweep (`--sweep`), and mutation-tests itself (`--probe`) |
| `.ufo/waves/round-49/w1/ScrToolLedger/receipts/` | the runs behind this report (§6) |

Reproduce, from the lane root:

```
python3 -I .ufo/waves/round-49/w1/ScrToolLedger/check-ledger.py --ledger \
    .ufo/waves/round-49/w1/ScrToolLedger/ledger.md      # re-derive + byte-compare, exit 0
python3 -I .ufo/waves/round-49/w1/ScrToolLedger/check-ledger.py --probe   # 7 mutations, all must fail
python3 -I .ufo/waves/round-49/w1/ScrToolLedger/check-ledger.py --sweep   # the candidate set per instrument
```

The checker is Python 3 stdlib. Its evidence comes from git objects only — `--rev` is honoured by
every lookup, no worktree path is opened for evidence, and the `--ledger` argument is only the file
to compare against. It writes nothing, starts no host program, opens no socket.

## 2. The instrument set and the rows

At the base there are **15** blobs under `tools/`: 12 rows, 3 listed exclusions (each quoted from
its own docstring). Classes are derived from the tool's bytes:

- `LIVE-PROBE` (4): `mado-eventq.py`, `mado-options.py`, `mado-globals.py`, `mado-verify.sh` — the
  tool itself runs a host program (`journalctl`, `hyprctl`, `ss`). The class literal must sit
  **outside** the module docstring.
- `LIVE-JOIN` (4): `mado-geometry.py`, `mado-monitors.py`, `mado-devices.py`, `mado-terminal.py` —
  the tool joins config bytes to a capture of the running system.
- `SESSION-RECORD` (1): `mado-tripwire.py` — reads OMP session transcripts.
- `CONFIG-SCORED` (3): `mado-binds.py`, `mado-anims.py`, `mado-wsrules.py` — config bytes only, but
  scored against a live capture; the receipt is the scored run.
- excluded: `mado-action-plan.py`, `mado-assessment.py`, `mado-evidence-audit.py` (each says in its
  own words that it consults no host state; the checker requires that sentence).

Row data (also emitted in `ledger.md` § Rows):

| instrument | class | bound receipt | round | bytes it ran |
|---|---|---|---|---|
| `mado-eventq.py` | LIVE-PROBE | `.ufo/waves/round-38/receipts/eventq-live.txt:8` | r38 | `436f550e` current |
| `mado-options.py` | LIVE-PROBE | `.ufo/waves/round-40/fetch/census-receipt.txt:7` | r40 | `63b5ebd9` current |
| `mado-globals.py` | LIVE-PROBE | `.ufo/waves/round-41/w1/ExecLiveHost/live-census.txt:89` | r41 | `61f101ae` **uncommitted** |
| `mado-geometry.py` | LIVE-JOIN | `.ufo/waves/round-44/w2/SentLiveRun/live-run.txt:7` | r44 | `1da3ddae` current |
| `mado-monitors.py` | LIVE-JOIN | `.ufo/waves/round-46/w1/ExecW2Monitors/live-runs.txt:35` | r46 | `2f007417` current |
| `mado-devices.py` | LIVE-JOIN | `.ufo/waves/round-46/w1/ExecIndepA/receipts/host-diff.txt:23` | r46 | none recorded |
| `mado-terminal.py` | LIVE-JOIN | `.ufo/waves/round-48/receipts/live-terminal-cache-r48.txt:8` | r48 | `14382047` current |
| `mado-verify.sh` | LIVE-PROBE | `.ufo/evidence/round-12/after.txt:80` | r12 | `ea798ad0` **stale** |
| `mado-tripwire.py` | SESSION-RECORD | `.ufo/waves/round-19/evidence/final/tripwire-seat-scan.txt:6` | r19 | `367be947` **stale** |
| `mado-binds.py` | CONFIG-SCORED | `.ufo/waves/round-25/evidence/c1-after-v4-ef94763c.txt:50` | r25 | `9efa1136` **stale** |
| `mado-anims.py` | CONFIG-SCORED | `.ufo/waves/round-26/evidence/c1-after-v2-2b3487f7.txt:51` | r26 | `2beda3f7` current |
| `mado-wsrules.py` | CONFIG-SCORED | `.ufo/waves/round-27/evidence/c1-after-20022a65.txt:49` | r27 | `dcf5c8c0` current |

Totals: 12 rows, 12 distinct receipts, 7 `current` / 3 `stale` / 1 `uncommitted` / 1 `none`.

## 3. Rules (implemented, not asserted)

1. **Instrument set** — every blob under `tools/` is a row or a listed exclusion; a tool that is
   neither fails the check.
2. **Receipt** — a file at the revision that (a) sits under a `receipts/`, `evidence/` or `fetch/`
   directory **or** has `live` in its basename, and (b) names the tool by basename or records one of
   the tool's committed digests. `fixtures/` subtrees and `*.py`/`*.sh` are excluded: a receipt is
   output, not a program or a test input.
3. **Newest** — the greatest committer date of the last commit touching the path at the revision.
   The bound receipt is the newest candidate that also carries the row's receipt marker (the
   command or header a run records) and its verdict pattern. Ties break on the path, deterministically.
4. **Verdict** — the one line matching the row's pattern; zero matches is a failure. `CONFIG-SCORED`
   rows require `verdict=TARGET_MET`, so the `before` control receipts cannot be bound (§4 F4).
5. **Bytes it ran** — the tool digest the receipt records, classified `current` / `stale` /
   `uncommitted` against every blob the path has had at or below the revision.
6. **Newer live-named file** — printed whenever it is not the bound receipt, even when it carries no
   verdict line (round-47 H1b's case). A live-named file qualifies only if it records the tool's
   digest or a command that runs the tool.
7. **Index of receipts** — a candidate that names more than one instrument is an index, not a run,
   and is skipped (§4 F3).

## 4. Findings

**F1 — Round-47's `globals` row is wrong in the opposite direction from its own claim (confirms
H2, quantified).** The r41 live census ran digest `61f101ae…`; no committed blob of
`tools/mado-globals.py` ever had it (the history holds only `286c051f`/`8db13340`). The truthful
status is not "no live receipt" but "a live run exists, at bytes that were never the committed
tool". The ledger says `uncommitted` and prints the digest.

**F2 — Round-47's `monitors` pointer is stale and `eventq`'s is stale in a subtler way (H1a/H1b).**
The newest live run of `mado-monitors.py` is `r46/w1/ExecW2Monitors/live-runs.txt` (two `MADO_MONITORS:`
lines, `verdict=OK`, digest `2f007417` = current bytes), not the r45 receipt the old ledger named.
For `mado-eventq.py` the newest live-named file is `r39/w1/ExecEventqSnapshot/eventq-live-census.txt`
(digest `436f550e`, no tool-output line); the ledger keeps the r38 receipt as the bound row because
it carries the verdict, and prints the r39 file with `0 line(s) match the verdict pattern`. A reader
sees both; nothing is hidden behind a "last run" claim.

**F3 — A naive newest-receipt rule binds a citation index.** `geometry`'s next-newest candidate was
`.ufo/waves/round-46/w1/ScrErrata/receipts/f3-skill-clients.txt`, which quotes the geometry
verdict (line 3) while checking SKILL.md and also names `mado-monitors.py`. It would have been reported as "the geometry receipt".
The one-instrument rule (rule 7) rejects it; the bound row is the r44 `w2/SentLiveRun/live-run.txt`
run instead. This is a new hole, not one of H1-H8.

**F4 — A naive `cases_pass=` rule binds a `before` control (new hole).** For `binds` and `wsrules`
the newest receipts by path are `c1-before-v4-41cc04c8.txt` and `c1v4-before-543f0445.txt`, both
real runs of the tool that print `cases_pass=0/41` and `verdict=TARGET_MISSED` on line 49
(`.ufo/waves/round-25/evidence/c1-before-v4-41cc04c8.txt:49`,
`.ufo/waves/round-27/evidence/c1v4-before-543f0445.txt:49`). Requiring
`verdict=TARGET_MET` in the pattern (rule 4) is what keeps a control run out of the row; the two
`after` receipts are the ones bound.

**F5 — Round-47's ledger omits one instrument and its own count is stale at the base.** That ledger
claims "14 tracked instruments" (`ledger.md:106`) and contains no `mado-terminal.py` row (0
occurrences). At the base there are 15 tools; `tools/mado-terminal.py` landed in `0c699605`, after
the ledger's commit `9bddd6ac` (`git merge-base --is-ancestor 9bddd6ac 0c699605` → true). The
instrument it missed has two live receipts (r47, r48). The lesson line's "0 wrong rows" target
therefore also needs "complete instrument set", which rule 1 enforces.

**F6 — Quote fidelity is now structural (H3).** The ledger contains no retyped quote: the checker
prints each verdict line from the object it names, and `--ledger` compares the committed file with a
fresh emit byte for byte. A hand-composed compression is impossible because no line is
composed by hand at all: the generator copies whatever the blob holds, including the fields
(here `lagging=0 missing_client=-`) that round-47's eventq row dropped.

**F7 — `none` is derived and the checker reads only the revision (H6).** `--rev` is honoured by
every lookup; no path is opened from the worktree. The one `none` (devices) means "the bound receipt
records no tool digest", which the sweep prints, not "no live evidence exists".

**F8 — `mado-devices.py`'s newest live run does not say which bytes ran.** `r46/w1/ExecIndepA/
receipts/host-diff.txt` is a genuine live run (`hyprctl devices -j` → tool, `verdict=OK`) but records
no digest of the tool it ran. The older `r46/receipts/live-devices-host-r46.txt` records
`3a803689…`. The row binds the newest and reports `none` for the bytes; the sweep shows the count.
If the lane wants "bytes it ran" always non-`none`, that is a receipt-format rule for the next
round, not a ledger trick.

## 5. Mapping to the round-47 refusal (H1-H8)

| hole | how this instrument closes it |
|---|---|
| H1 last-live-run wrong, `w1/`/`w2/` never searched | rule 2 scans every blob at the revision and only filters by *shape* (a `receipts/`/`evidence/`/`fetch/` segment or `live` in the basename); four of the twelve bound receipts are seat files under `w1/`/`w2/` (globals r41, geometry r44, monitors r46, devices r46), not round-level `receipts/` files |
| H2 `globals` "none" false | the row binds the r41 census and classifies its digest `uncommitted` (F1) |
| H3 8 of 21 quotes not verbatim | quotes are printed from blobs, never composed; `--ledger` enforces byte-identity with a fresh emit (F6) |
| H4 a red exercise recorded as "by design" | the analogous failure — a control run bound as the row — is closed by rule 4 (F4); a row with no qualifying receipt fails instead of degrading |
| H5 §9 transcript contradicting the receipt | counts in the ledger are emitted from the same derivation that is checked |
| H6 `none` not re-derivable, `--rev` reads the worktree | rule 5/`--rev`: every read is `git cat-file`/`ls-tree`/`log` at the revision; `none` is a derived digest status |
| H7 `eventq` journal unit misnamed | the reads column prints the tool's own line, `--journal-file \`journalctl --user -u wayland-wm@hyprland.desktop.service` (tool:68), and the class line prints the live invocation at tool:242 |
| H8 counts without commands | every count in the ledger is emitted; the sweep size per row is printed |

## 6. Gates run

Re-derivation and byte-comparison of the committed ledger (exit 0):

```
$ python3 -I .ufo/waves/round-49/w1/ScrToolLedger/check-ledger.py --ledger .ufo/waves/round-49/w1/ScrToolLedger/ledger.md
LEDGER rows=12 excluded=3 receipts=12 verdicts=12 current=7 stale=3 uncommitted=1 none=1
LEDGER-MATCH .ufo/waves/round-49/w1/ScrToolLedger/ledger.md
```

The same check inside a `git clone --shared` of the lane, so that no uncommitted file (this seat's
directory included) can contribute to the result; it emits the identical ledger and matches the
lane's copy:

```
$ python3 -I <lane>/.ufo/waves/round-49/w1/ScrToolLedger/check-ledger.py \
    --repo /fast/scratch/hyaku/mado-r49/ScrToolLedger/lane-clone --ledger <lane>/.../ledger.md
LEDGER rows=12 excluded=3 receipts=12 verdicts=12 current=7 stale=3 uncommitted=1 none=1
LEDGER-MATCH /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-49/w1/ScrToolLedger/ledger.md
```

Mutation gate — each line changes one claim in memory and the derivation must fail:

```
$ python3 -I .ufo/waves/round-49/w1/ScrToolLedger/check-ledger.py --probe
CAUGHT question-line-out-of-range
CAUGHT verdict-pattern-matches-nothing
CAUGHT reads-literal-invented
CAUGHT class-literal-only-in-prose
CAUGHT receipt-marker-unsatisfiable
CAUGHT declared-token-invented
CAUGHT duplicate-row
PROBE ok
```

Candidate sweep (`--sweep`, 66 lines in `receipts/sweep.txt`) prints, per instrument, the newest
five receipt-shaped files with their digest class, verdict-line count and marker flag — the audit
trail for every "newest" claim in the ledger.

Every bound receipt path is listed by `git ls-tree` at the base (`receipts/ls-tree.txt`, 12 lines,
all `100644 blob`).

This report's own table and quoted fragments are checked the same way: `verify-report.py` re-derives
each row's receipt path, locator line and digest prefix from the base objects and greps the nine
finding quotes, printing `REPORT-CLAIMS ok rows=12 fails=0` (`receipts/report-claims.txt`).

## 7. Artifacts

| path (under `.ufo/waves/round-49/w1/ScrToolLedger/`) | content |
|---|---|
| `ledger.md` | the generated ledger (12 rows + 3 exclusions + counts + gate self-test) |
| `check-ledger.py` | checker/generator |
| `receipts/probe.txt` | `--probe` output |
| `receipts/check.txt` | `--ledger` re-derivation + byte-compare |
| `receipts/clone-check.txt` | the same check inside a `--shared` clone of the base (no worktree files) |
| `receipts/ls-tree.txt` | `git ls-tree` lines for all 12 bound receipts |
| `receipts/sweep.txt` | the candidate sweep for all 12 instruments |
| `verify-report.py` | checks this report's row table (receipt path, locator line, digest prefix) and its finding quotes against the base objects |
| `receipts/report-claims.txt` | `verify-report.py` output: 12 rows + 12 quoted fragments, `fails=0` |

Pinned bytes of the two files the L1 would integrate (`sha256sum <path>`, 2026-10-27):

```
cd0b49cd0d9b3858f83c8938d316ddafd4c29acccead27876a70a3a5c0b52f8d  .ufo/waves/round-49/w1/ScrToolLedger/ledger.md
84c2445d9f82e576153155cf9825163a07d011b10a71f08ff2fc7c541dfe6981  .ufo/waves/round-49/w1/ScrToolLedger/check-ledger.py
```

## 8. Out of scope, limits

- No host probe: "the receipt records X" is not "the desktop does X today". `hyprctl` was not called
  by this seat.
- The ledger is not wired into `QUALITY.md`, `PROVINCE.md`, `README.md` or any gate: the L1 is the
  integrator and the round-47 criterion 91 is not mine to edit.
- The candidate rule is path-and-content based over git objects. A live run recorded only in a seat's
  prose report, or in a file that neither names the tool nor records its digest, is outside it; each
  row prints its sweep size so the boundary is auditable rather than implied.
- 47 untracked `*.synthetic` sidecars, the C1/C2 claims and the routed non-claim items are other
  seats' work; this seat touched none of them and wrote only its own directory and this report.
- No tool was installed or upgraded for this seat (nothing outside Python 3 stdlib and git was
  needed), so there is no tool line to record. The `--shared` clone used for the revision-only
  control lived under `/fast/scratch/hyaku/mado-r49/ScrToolLedger/` and is deleted at the end of
  the seat; the command above recreates it.
