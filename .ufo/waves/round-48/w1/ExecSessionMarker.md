# ExecSessionMarker — round 48 w1 R3: the synthetic-material marker installed at base, failing both ways

Seat: `ExecSessionMarker` (leaf; no subagents, no background jobs). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Base (lane tip at round start): **`579f694b45c797a9c39761fdb4f9e0a1b71b3585`**. Every clone and fixture lived
under `/fast/scratch/hyaku/mado-r48/ExecSessionMarker/` and was deleted before this seat finished. Nothing in the
lane was written outside `.ufo/waves/round-48/w1/ExecSessionMarker/` and this report; no tracked file was edited
(the L1 is the integrator). No serial, window title, program name or home path is printed anywhere below: every
gate line quoted is value-free by construction, and every locator was computed with `grep -n`, never typed.

Routed item (round-47 spot-check §6.2, `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-47-verifier-spotcheck.md:135-136`):
"R3 (marker install) stays open, routed again". Round-47 lessons `:220` record the same item as "not installed
this round: the marker gate is drafted and attacked … but replacing the registered gate plus 49 sidecars did not
fit the round". This seat delivers the final bytes **for the tree at this round's base**, not a re-draft.

## 1. What lands

| path (lane-relative) | what | sha256 |
|---|---|---|
| `quality/check-session-material.py` | gate v2: tracked gate `889f8f05…` (682 L) + the round-47 marker/serial layer + the F1/F5 corrections in §2; **1643 L**, selftest **69/69** | `82c9053ae2e8b7db2fb8c0e195c32b8b151a593cf9412dcae3589427ac2dfa6f` |
| `quality/session-material-waivers.txt` | **the install set**: 48 rows (47 `fixture`, 1 `gate-copy`) | `4d007fe8124523a1a8e2a021a182d5c65f0e99f74d3c69c7d3272289be12604e` |
| 48 × `<path>.synthetic` | the sidecars those rows name, lane-relative under `sidecars/` | sidecar set in `SHA256SUMS` |
| `SKILL.md:770` row | `skill-row.md` (replaces the round-46 row; new selftest count, namespace, install order, residuals) | `99f63b4b32acfc35ed94abc72b985403e9df13f5404924be1aad7409144f61cb` |
| `install.sh` | applies the three above to a lane checkout; never runs git, never commits | `b7b7813f24ee05a946375fc61a57796619e64591c2f74fb73684307358abfbec` |
| `verify-install.sh` | reproduces §3.5 from base bytes in a throwaway clone | `bd0600c5279d04d84059d8118594b24453bba97569ba2f7969ccf4ad3c97ef9a` |
| `triage.py`, `mark.py` | byte-identical copies of the tracked round-47 generator/helper (`1de5224d…`, `1581a99f…`); the registry can only hold rows the gate itself accepted | — |
| `gate-v2.diff` | the review diff: round-47 draft `a4a0a084…` → delivered bytes (four hunks: docstring W4b title namespace, docstring size limit, title regex, six selftest cases) | see `SHA256SUMS` |
| `sweep-titles.py` | the classification tool behind §2's title-namespace delta (paths and counts only) | `1582a1025f8ec85755c21f3b5b174986bbcc3dbc04bbb9d94c61af74d7476520` |
| `verify-claims.py` | asserts all 25 receipt-line claims and the report's numbers below (`CLAIMS_CHECK passed=35 failed=0`) | `15198c0835df8a0cd282befd1f53bf1d80c02bad82fc4ffebc3a305da5459542` |

Install: `sh .ufo/waves/round-48/w1/ExecSessionMarker/install.sh <lane-checkout>` then commit; §3.6 proves the
result from a fresh clone of the base. Registry row order is sorted; 45 rows are the round-45 monitor fixtures
(`.ufo/waves/round-45/w1/RevengerOmarchy/fixtures/…/mons.json`), 2 are the round-46 `CritW2Gate` pair, 1 is the
`gate-copy` row for this seat's own copy of the gate (`.ufo/waves/round-48/w1/ExecSessionMarker/check-session-material.py`,
which must land byte-identical — `install.sh` copies exactly these bytes).

## 2. The contract, and the two corrections to the round-47 draft

A marker is a **pair**, both read from the scanned revision: a tracked sidecar whose first line is
`SYNTHETIC-MATERIAL v1 kind=<fixture|gate-copy> rules=<R1-R4 csv> sha256=<64 hex>` and one line
`<path> <sha256> <rules> kind=<kind>` in `quality/session-material-waivers.txt`. A finding is waived only when
W1 path under `.ufo/waves/` and registry outside `.ufo/`; W2 sidecar grammar exact and sha256 = the target blob;
W3 the registry line repeats path/sha/rules/kind; W4a `gate-copy` ⇒ target byte-identical to the gate source;
W4b `fixture` ⇒ every matched value inside a reserved namespace. Serial rules are structurally outside the
surface (`MARKER_RE` accepts `R[1-4]_…` only; a serial finding on a marked file is refused before parsing).

What this seat changed on top of the audited draft (`a4a0a084…`, whose marker logic round-47 w2 `MutSessionMarker`
could not break and `RevSessionMarker` found one real laundering path plus four coverage/doc gaps, F1-F5):

- **F1 fixed — the title namespace is now exact.** `SYNTH_TITLE_RE` is
  `^(?:a live window title|another live window title|redacted)$|^(?:synthetic|fixture|selftest)[ -][A-Za-z0-9 ._-]{0,60}$`,
  case-sensitive, delimiter mandatory. The draft's alternative
  `^(?:synthetic|fixture|selftest|probe|example|demo)(?:[ -]…)?$` under `IGNORECASE` admitted bare real titles and
  any real title that merely began with one of six words. Control: the same fixture bytes (a client dump titled
  with the IANA reserved example domain) are **waived by the draft** and **refused by the delivered file** on the
  identical revision — `receipts/10-f1-control-draft-waives.txt:51` (`WAIVER … forged-real.json`) versus
  `receipts/09-c2-value-not-synthetic.txt:55` (`reason=value-not-synthetic:title-not-synthetic`). Six new selftest
  cases pin the boundary (`waiver-title-{example-domain,bare-demo,probe-prefix,case-only}-rejected`,
  `waiver-title-{reserved-prefix,reserved-exact}-waived`). Cost, measured against the real tree at base:
  `receipts/00a-title-sweep.txt` — 31 files carry R1 values, 123 values; 2 files pass the draft namespace
  (`old_pass=2`) and **0** pass the new one; both lost files are the round-46 `CritW2Gate` pair, whose titles are
  in the `Example…` family (`receipts/00b-title-families.txt`: `prefix:example+case`). They are therefore counted
  (class `title-not-synthetic`, reported as `rule-not-listed` after pass B narrows the sidecar), not waived.
- **F5 docstring corrected.** The old sentence ("Files larger than 16 MiB are scanned for R2/R4 only, and their
  object scan reports `truncated=True`") was wrong in both halves (round-47 w2 RevSessionMarker F5: every rule
  runs, only over the first 16 MiB; `truncated=True` belongs to the 20000-object limit). The delivered docstring
  states the blind half plainly. No behaviour change — the tail of a >16 MiB blob remains invisible by design,
  now declared.

Residuals carried **unchanged** and declared in the skill row: F2 (R3 needs a non-empty `serial` before
description/make/model are looked at — a description-only dump reads clean), F3 (registry/`--gate-source` paths
are caller-relocatable via flags; the pinned SKILL command uses defaults only), F4 (R1 is JSON-scoped, so a title
in prose is invisible). None of them is inside the marker's waiver surface, so none is laundered by this seat.

## 3. The measurement at base (all revisions named; all receipts in `receipts/`)

One scratch clone of the lane (`git clone -q --shared`, toplevel asserted equal to the clone before any commit,
scratch identity only), detached at base, then the commits in the table below plus three demo commits. "With and
without the marker" is the same gate bytes at consecutive revisions, so the delta is the marker layer and nothing else.

| # | state | rev | gate output | rc | receipt |
|---|---|---|---|---|---|
| 3.1 | base tree, **tracked** gate `889f8f05…` | `579f694…` | `files=19969 findings=128` (R1=33 R2=36 R3=57 R4=2) | 1 | `01-old-gate-at-base.txt:131` |
| 3.2 | + gate v2, **no sidecars, no registry** | `108cce5e…` | `files=19969 findings=149` (+21 `R5_SERIAL_PROSE`) | 1 | `02-v2-nomarkers.txt:152` |
| 3.3 | + registry (48 rows) and 47 sidecars | `0fb5340b…` | `SESSION_MATERIAL_WAIVED: findings=49 files=47`; `files=20016 findings=100` (R1=33 R2=34 R3=10 R4=2 R5=21) | 1 | `04-with-markers.txt:154-155` |
| 3.4 | 3.3 under `--no-waivers` | `0fb5340b…` | `findings=149` — **identical to 3.2**, so the drop 149 → 100 is the marker layer, not changed content | 1 | `05-no-waivers.txt:152` |
| 3.5 | fresh clone of base + `install.sh` (48 rows) + commit | `68b834ee…` | `WAIVED findings=49 files=47`; `files=20017 findings=100` — the delivered set reproduces 3.3 from base bytes (the 48th sidecar has no target, so it changes no finding) | 1 | `11-verify-install.txt:157-158` |

### 3.6 The four required demonstrations (same clone, one commit each)
The planted bytes are fabricated fixture text with reserved-namespace values; no host value is involved.

- **(a) synthetic fixture material marked → not counted.** A client dump at
  `.ufo/waves/round-48/w1/ExecSessionMarker/fixtures/synthetic-clients.json` with a valid sidecar + registry row:
  the gate prints `WAIVER file=…synthetic-clients.json rule=R1_CLIENT_DUMP kind=fixture`
  (`07-a-marked.txt:51`), prints **no** `FINDING` line for that path, and the total is back to 100
  (`07-a-marked.txt:156`, rev `76e2e24c…`). On a repository holding only that fixture the same state is exit 0 —
  selftest `waiver-fixture-waived` / `waiver-exit-0-and-count-line`.
- **(b) the same bytes unmarked → counted (fails).** The revision that adds those bytes without the marker pair,
  `5745373…`, differs from (a) by the marker alone: `FINDING …synthetic-clients.json rule=R1_CLIENT_DUMP count=1` at `06-b-unmarked.txt:153`, total
  101 (`:156`). (a) and (b) are the same bytes; the only delta is the marker.
- **(c) a real-looking value under a forged marker in a non-fixture path → still counted.** The same real-shaped
  client dump at `.ufo/reports/session-clients.json` with a *well-formed* sidecar and a matching registry row:
  `WAIVER_REJECTED … reason=path-outside-waves` (`08-c-forged-nonfixture.txt:52`) and the
  `FINDING …session-clients.json rule=R1_CLIENT_DUMP count=1` stands (`:55`), total 101 (`:158`, rev `99d2d3a9…`).
- **(c′) the same value inside a fixture path → still counted on the value.** Marker pair at
  `.ufo/waves/round-48/w1/ExecSessionMarker/fixtures/forged-real.json`:
  `reason=value-not-synthetic:title-not-synthetic` (`09-c2-value-not-synthetic.txt:55`), the finding stands
  (`:157`), total 102 (`:160`, rev `75a5359b…`). This is also the F1 regression case (§2).
- **(d) findings count before/after, named revisions.** 128 at `579f694…` under the tracked gate (3.1) → 149 at
  `108cce5e…` with the new rules and no marker (3.2) → **100 at `0fb5340b…` with the install set** (3.3), and 100
  again at `68b834ee…` from base bytes via `install.sh` (3.5). Waived 49 findings in 47 files, printed, never
  silent.

### 3.7 The as-landed tree (install set + this seat's own files)

A fourth clone of base with `install.sh` applied **and** this seat's whole directory plus this report committed:
`WAIVER …round-48/w1/ExecSessionMarker/check-session-material.py rule=R1_CLIENT_DUMP kind=gate-copy` (and R2, R3),
`SESSION_MATERIAL_WAIVED: findings=52 files=48`, `files=20095 findings=100` (`receipts/12-as-landed.txt:156-157`,
rev `7031e383…`, rc 1). The seat's 79 added files therefore add **zero** findings and lose none: the only file of the
seat that carries material is its copy of the gate, and the `gate-copy` row covers exactly it because
`install.sh` copies byte-identical bytes. If the L1 edits those bytes, the row fails closed (`gate-source-mismatch`)
and the three findings return — the row is not a general waiver.

## 4. What remains red at the install revision, and why that is the honest answer

The install state is **`findings=100`**, exit 1 (`04-with-markers.txt:155`), classified by the gate itself
(`triage-r48.tsv`, summary in `receipts/03-triage.txt`):

| class | findings | what it is |
|---|---|---|
| `real:identity:program-not-synthetic` | 31 | process rows naming real programs in round-37/38/39 receipts and the reports quoting them |
| `real:identity:title-not-synthetic` | 28 (+2 the F1 tightening now refuses, reported `rule-not-listed`) | real client titles in round-43/44/46/47 receipt files |
| `real:serial` (`R5_SERIAL_PROSE`) | 21 | the host monitor serial in prose, round-32/37 wave copies — operator-owned |
| `synthetic:stale-gate-copy` | 9 | three gate copies (`round-45/w1/ExecPrivacyGate`, `round-46/w1/ExecSessionTriage`, `round-47/w1/ExecSessionMarker`) that are not byte-identical to the installed gate: `kind=gate-copy` cannot apply, and W4b refuses their real-shaped selftest serial |
| `real:identity:serial-not-synthetic` | 6 | monitor dumps with literal serials |
| `real:identity:home-user-not-synthetic` | 2 | `/home/<real user>` listings |
| `real:identity:vendor-not-synthetic` | 1 | a monitor make outside the reserved words |

No green is claimed and none is reachable without removing real material. The stale gate copies can only be
closed by refreshing those tracked copies to the installed bytes or by accepting them — the integrator's call;
this seat did neither.

## 5. Selftest

`TMPDIR=<scratch>/tmp python3 -I check-session-material.py --selftest` → `SELFTEST: passed=69/69 failed=0`, exit 0
(`receipts/00-selftest.txt`). 63 are the round-47 draft's cases (unchanged), 6 are new title-namespace cases. The
file's own bytes carry no matchable serial (its serial fixtures are assembled from parts at run time, and R5/R6
self-scan cases still pass).

## 6. Safety, tooling, repro

No installs (Python 3.14 stdlib + git only; no `pacman`, no `uv` — the host-wide pause was respected), no
compositor access, no terminal or GUI program, no `xdg-terminal-exec`, no host config or cache touched, no host
session value read. Every clone asserted `git rev-parse --show-toplevel` equal to its own directory and committed
with a scratch identity; no mutating git command ran in the lane or the fleet. Scratch deleted; no receipt cites a
scratch or `/tmp` path as evidence.

```sh
S=/fast/scratch/hyaku/mado-r48/ExecSessionMarker; SEAT=…/.ufo/waves/round-48/w1/ExecSessionMarker
git clone -q --shared …/mado-shokunin "$S/clone" && git -C "$S/clone" checkout -q --detach 579f694b
TMPDIR="$S/tmp" python3 -I "$SEAT/check-session-material.py" --selftest
sh "$SEAT/verify-install.sh" /home/vgpnk/Projects/shokunin/mado-shokunin "$S"   # receipts/11
python3 -I "$SEAT/triage.py" --repo "$S/clone" --rev HEAD --registry "$S/reg.txt" --triage "$S/triage.tsv"
sh "$SEAT/install.sh" "$S/clone"        # then commit and run the gate; receipts 04/05
```

## 7. Evidence index

`receipts/00-selftest.txt`, `00a-title-sweep.txt`, `00b-title-families.txt`, `01-old-gate-at-base.txt`,
`02-v2-nomarkers.txt`, `03-triage.txt`, `04-with-markers.txt`, `05-no-waivers.txt`, `06-b-unmarked.txt`,
`07-a-marked.txt`, `08-c-forged-nonfixture.txt`, `09-c2-value-not-synthetic.txt`,
`10-f1-control-draft-waives.txt`, `11-verify-install.txt`, `12-as-landed.txt`; the classifier's output table
`triage-r48.tsv`; file hashes in `SHA256SUMS`. Every number in this report is a line of one of them.
