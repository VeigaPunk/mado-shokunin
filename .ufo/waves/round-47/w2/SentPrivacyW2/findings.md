# Session-material findings — round-47 wave files (before the data commit)

Seat `SentPrivacyW2`, wave `w2` (falsify), 2026-10-26. Scope: every file under
`.ufo/waves/round-47` at scan time (w1, w2, receipts, ctl, fetch, l1-draft, assimilation).

Rules applied: `SKILL.md:343-344` ("Session material stays shape-only"), the gate's own docstring
(`quality/check-session-material.py:1-56`, rules R1-R4), and the round's proposed MADO-47-PRIV
P1-P10 (`w1/SentPrivacy/report.md:82-127`). **Values are never printed here**: locators are
`path:line` and class only; the two receipts that compare live values print booleans.

Instruments (both run, both receipts in this dir):

| instrument | command | result |
|---|---|---|
| privacy gate | `quality/check-session-material.py --selftest` | `SELFTEST: passed=22/22 failed=0` (`gate-selftest.txt`) |
| privacy gate | `--repo <clone> --rev HEAD` on a snapshot of the wave dir | 4 findings under `.ufo/waves/round-47`, all gate self-matches; 115 elsewhere (`gate-run.txt`) |
| class sweep | `w1/SentPrivacy/sweep-privacy.py --worktree <wave>` | G1=6/11, G2=418/5519, G3=11/12, G10=11/22, G11=2/5; G4/G5/G7/G9=0 (`sweep-redacted.txt`) |
| live-value match | own pass, booleans only | env/monitor/hostname/signature (`live-value-compare.txt`) |
| class census | own pass, locators only | 10 classes, 289 file-class rows (`ledger.tsv`, `class-summary.txt`) |

Wave-dir census at scan time: 1217 text blobs, 14.3 MB, manifest digest
`f8ecb22c453ce16381ad8c96fe15ac2574bc33bb9f476e2ac6f0629f9f8cd620` at the earlier snapshot;
the final snapshot is pinned in `gate-run.txt` (wave dir keeps growing while w2 seats run).

## F1 — live session environment dumped into a receipt (medium-high)

- `w1/ExecLive/receipts/live-host.txt:10-28` — 17 `XDG_*`/`HOME` assignments lifted from the live
  session. Session-identifying keys: `:18` runtime dir, `:19` seat, `:20` seat path, `:21`
  session class, `:22` session desktop, `:23` session id, `:24` session path, `:25` session type,
  `:26` state home, `:27` virtual terminal.
- Four of them (`XDG_RUNTIME_DIR`, `XDG_SEAT_PATH`, `XDG_SESSION_PATH`, `XDG_STATE_HOME`) equal the
  **live host values verbatim** (`live-value-compare.txt`), not placeholders.
- Same class, w2 and live right now: `w2/CritUwsm/daemon-env`, `w2/CritUwsm/hyprland-env`,
  `w2/CritUwsm/manager-env` — three 19-key environment dumps.
  `w1/SentHost/receipts/ambient-cache-env.txt:5-6` — two ambient assignments.
- Gate R1-R4: **0 findings**. Sweep G1: fires on 2 of the keys the round's own P5 forbids
  (its regex lists session-id and runtime-dir only), so the instrument under-reports the rule it
  is used to certify.
- Impact: the receipt is declared shape-only (`live-host.txt:7`); an environment dump is exactly
  what P5 (`w1/SentPrivacy/report.md:96-103`) forbids, and it is the residue a careless live run
  leaves behind. Smallest remediation: keep only the seven resolver variables the fixture schema
  needs (`XDG_CURRENT_DESKTOP`, `XDG_CONFIG_HOME`, `XDG_CONFIG_DIRS`, `XDG_DATA_HOME`,
  `XDG_DATA_DIRS`, `HOME`, `PATH`) and write `$HOME/...`; drop the seat/session/vt lines.

## F2 — a 13-entry home inventory that R4 cannot see (medium)

- `w1/ExecLive/receipts/live-host.txt` carries **13 distinct** account-rooted paths
  (`:11,13,16,26,28,33,38,44,53,60,62,63,64,71,77,79,89,109,116,145,147,158,167`), which is above
  R4's own limit of 10, yet R4 reports `count=0` — its `HOME_PATH_RE` requires the path to be the
  **whole line**, and every one of these sits inside a sentence.
- Control `c6-inv5.txt` (five whole-line paths) is clean, as designed; the hole is the form, not
  the threshold.
- The sweep over-counts the same class: at my re-run 5420 lines matched its `G2_HOME_PATH`, of
  which 907 carry the real account segment and the rest are the redaction form `/home/.local/...`
  read as an account name (`blind-spots.tsv` H15). A G2 number is therefore not a leak metric.
- Remediation: fire R4 on >10 distinct account paths per blob regardless of position, print the
  number, and exclude `.local|.config|.cache` from the sweep's account names.

## F3 — host resolver cache recorded with nanosecond times and body (medium)

- `w1/ExecLive/receipts/live-host.txt:109-121` — cache path, byte size, sha256, **mtime with
  nanoseconds and timezone**, and the cache body field by field (key, exec, path, id, action,
  argument fields).
- `w1/SentHost/receipts/host-cache-observed.txt:3-5` — two observation timestamps, the size change
  between them (190 -> 168 bytes) and a second sha256; `:9` names how many desktop ids the body
  carries. The size change dates a **host write by another seat** to the minute.
- `w1/ExecLive/receipts/raw/scratch-cache.txt:1-4` — the scratch cache body.
- `w2/CritUwsm/cacheA-content` — a 188-byte, 11-line cache body committed as a file (mode 600).
- Class: the last selection plus operator activity time. P7/P9 (`w1/SentPrivacy/report.md:109-121`)
  says shape only, never the body, never an exact time.
- Gate: 0 findings. Sweep G11 fires on the epoch form only (2 files: `w1/ExecCache/receipts/
  probe.log:25,197`, scratch cache epochs, low) — human dates with nanoseconds are invisible to
  both instruments (`blind-spots.tsv` H14).

## F4 — instance signature re-published in full (medium)

- Shape `/run/user/<uid>/hypr/<40 hex>_<pid>_<timestamp>` in 7 files:
  `w1/ScrToolLedger/receipts/live-receipts.txt:10` (a quoted round-38 receipt line) and
  `w1/ExecControls/c2/{REF,EMPTY,FORGED-QUOTE,BRANCH-URL,INDEX-NOT-CHAIN,RECEIPT-ABSENT}/files/
  corpus/SOURCES.md:222`.
- Not equal to the live value (stale pid/timestamp), so this is not an addressable socket today;
  the same value is already public at `corpus/SOURCES.md:222` in the base tree.
- P4 says never print it in full, not even truncated; a quote is a commit. Gate: 0 findings.
  Sweep G3 fires (12 occurrences) but files it as a uid path, understating the class.
- Remediation: write `<SIG>` in the six control copies and cut the ledger quote at
  `/run/user/<uid>/hypr/`.

## F5 — gate holes, each with a control (medium; the substantive falsification)

Controls live in a scratch clone (`gate-controls.tsv`, `gate-controls-run.txt`,
`gate-controls-run2.txt`); each control file is synthetic. Observed:

| hole | control | gate |
|---|---|---|
| H1 binary skip: a blob with a NUL byte in the first 8 KiB is never decoded | `c1-gz-dump.json.gz` | 0 findings |
| H2 object cap: 20000 objects per blob, and `truncated` is printed **only when something already matched** | `c12-many-objects.txt` | 0 findings, no warning |
| H3/H5 text cap: >16 MiB is scanned for R2/R4 only | `c13-over16mib.txt` | 0 findings, no warning |
| H4 JSON-only: human blocks and TSV tables | `c14-human-clients.txt`, `c10-fenced-tsv.txt`, `c2-py-repr.txt` | 0 findings |
| H6 R2 needs the `ss -p` program/pid column | `c3-ps-table.txt`, `c4-ss-nop.txt` | 0 findings |
| H7 R3 needs a serial in the same object | `c5-monitor-name.json` | 0 findings |
| H8 R4 whole-line form (see F2) | `c6-inv5.txt` | 0 findings |
| H9 empty class (declared) | `c9-title-noclass.json` | 0 findings |
| H10 no MAC rule anywhere | `c8-devices-mac.json` | 0 findings |
| H11 a symlink is scanned as its target string | `c11-symlink.json` | the link is invisible; the target is found only because it is committed too |
| H12 no rule for a title inside a sentence | `c7-prose-title.txt` | 0 findings |

Positive control in the same commit: `p1-raw-dump.json` -> `R1_CLIENT_DUMP count=2`. The gate
detects the raw shape; every hole above is a shape it cannot see.

Reproduce: `README.md` §"Control run".

## F6 — raw strace with pid and argv (low)

10 files: `w1/ExecStraceTrip/receipts/trace-{bad-fork,bad-subprocess,clean,threads}.txt:1`,
`w1/CritOracle/execve-{cold,warm}.log:1`, `w1/ExecRefA/receipts/strace-{print,selftest}.txt:3`,
`w1/SentHost/receipts/exec-argv.txt` (deduplicated counts — the sweep's G10 false-positives on it).
P8 asks for one `execve("<basename>")` per line, no pid, no argv. Gate: 0. Sweep G10: 11 files.

## F7 — `ls -l` lines (owner, group, exact time) (low)

`w1/ScrEntry/receipts/live-print.txt:16`, `w1/ScrMistakes/receipts/pyc-state.txt:3`,
`w1/ScrMistakes/receipts/r2-state.txt:5-12`, `w1/ScrToolLedger/receipts/absence.txt:14`. The line
carries the account name twice (owner and group), the size and the file time. No rule and no sweep
class covers it.

## F8 — hostname (low, w2 live)

`w2/SentC1Sandbox/sandbox-probe.json` (a `hostname` field with the live value) and
`w2/SentC1Sandbox.md`. Two files at scan time; the seat was still writing. No rule in the gate and
no class in the sweep (`blind-spots.tsv` H13).

## F9 — account segment (low, systematic)

240 files / 1327 occurrences of an account-rooted absolute path at scan time. Top carriers are
machine-written orchestration files (`w1-spec.json`, `w2-spec.json`, `w1-dispatch.json`,
`w2-dispatch.json`, `w1-results.json`, `registration.md`, `make-w1-spec.py`, `make-w2-spec.py`),
then the c2 control trees and the seat reports. Gate-blind by construction (R4 is a listing rule);
the sweep counts it but inflates it (F2). Remediation is P1's `$HOME/...`, applied to the files the
L1 intends to commit; a scrub of a receipt must be followed by re-running that receipt's own
locator check, because several seats verify quotes against absolute paths.

## F10 — clean results (supporting evidence, not findings)

- **No live client dump**: exactly 1 file in the wave dir carries objects with a non-empty class
  and a title (`w1/ExecSessionMarker/check-session-material.py`, 4 objects, all synthetic
  selftest fixtures). Independently confirmed by a scanner that does not share the gate's
  fast-path, and by `ls`-free grep for the human block form (0).
- **No live monitor identity**: 0 files match the live serial, description, make or model
  (`live-value-compare.txt`). The `REAL_MONITORS` fixture in the ExecSessionMarker copy is a
  plausible Dell string, **not** this host's (field-by-field inequality, 4/4).
- **No live instance signature**: the live 61-character signature appears in 0 files; the shape
  that appears 7 times is stale (F4).
- **No credential shape**: 0 matches for cloud-key prefixes, PEM headers, `Bearer`/`api_key`/
  `password`/`secret` assignments (`class-summary.txt`: no SECRET row).
- **No MAC, no application inventory**: sweep G7=0, G9=0.
- **Gate integrity**: the gate blob is identical at the frozen rev and at the lane tip
  (`d7527d6:quality/check-session-material.py` = `9bddd6a:...` = working tree,
  sha256 `889f8f057bf04fc76ed93dd7ee86e3b0bd9fc1dca3a6bfb712c672da4646e3fb`), and its selftest
  passes 22/22 — the gate the round froze is the gate that runs.

## F11 — commit hygiene for the L1 (medium)

- The wave dir **cannot pass its own gate**: 4 findings land in `.ufo/waves/round-47` —
  `w1/ExecSessionMarker/check-session-material.py` (R1 4 objects, R2 3 rows, R3 1 object) and
  `w2/RevSessionMarker/probes/probe_bigfile.py` (R2 1 row). All four are the gate's own pattern
  text or its own synthetic fixtures inside a copy; none is live material. The lane gate has no
  waiver mechanism (the w1 seat's 1599-line variant does, but it is not the frozen gate), so the
  data commit will carry 4 self-match findings. State them; do not "fix" the gate after data.
- `.gitignore:3` (`__pycache__/`) silently drops 5 files from the round dir (3 `.pyc` under
  `l1-draft/`, `ctl/`, `w2/CritC2Forgery/`). A `git add -A` copy of the wave dir is therefore not
  1:1; nothing secret rides there, but no seat may cite a `.pyc` as committed evidence.
- This seat's own directory is clean under the gate (0 finding lines, `gate-run.txt`), so this
  report adds nothing to the 4.
