# SentPrivacy — privacy scan of the round-51 wave dir (w1, round 51, 2026-10-27)

Question: does the round-51 wave directory carry raw session material — the class SKILL rule 4
keeps out of the public repo, the class of the round-38 (`r38`) 190 KB `ss`-table incident —
**before** the L1 commits it?

Answer: **no.** The gate reports `findings=0` over four snapshots of `.ufo/waves/round-51/`
(58 → 164 files as the seats landed work; the last is the committable set with the lane's own
`.gitignore` applied). A hand-check of every class the gate cannot see — out-of-surface host
paths, account names, live-state receipts, **non-text blobs** — finds one INFO pathname that is
already tracked in the lane at base, and one gitignored `.pyc` that embeds a host path the text
gate structurally cannot see (§2e). Neither is a commit blocker.

## 1. Gate verdict (exact)

`quality/check-session-material.py` reads a *committed* revision from the git object database, so
the (currently untracked) wave dir was snapshotted into a throwaway repository under the seat
scratch root and scanned there. Nothing in the lane was written.

```
$ TMPDIR=<scratch> python3 -I quality/check-session-material.py --repo <scratch>/final5 --rev HEAD --scope all
SESSION_MATERIAL: files=164 findings=0 rev=124f48c83471ada589773d736585fac223e91d0f
gate_exit=0
# re-run after this report's final revision: files=175 findings=0
#   (receipts/gate-final6.txt, rev=341ca00db4641fe547ff800c16dca00082f74526)
```

Snapshots of the same wave, each clean, as the seats kept landing files (`final5` is the one that
matters: it applies the lane's own `.gitignore`, so its 164 files are the **committable set** —
the `.pyc` of §2e is correctly excluded, `pyc_staged=0`):

| snapshot | files | findings | receipt |
|---|---|---|---|
| 09:57Z (before any seat prose) | 58 | 0 | `receipts/gate-wave.txt` |
| 09:59Z (+ C2 pins, seat reports) | 73 | 0 | `receipts/gate-final.txt` |
| 10:0xZ (+ 42 more seat files, incl. this report) | 115 | 0 | `receipts/gate-final2.txt` |
| 10:1xZ (lane `.gitignore` applied) | 164 | 0 | `receipts/gate-final5.txt` |
| 10:2xZ (this report's final revision, `.gitignore` applied) | 175 | 0 | `receipts/gate-final6.txt` |

- The `rev=` values are **fixture-local**, not lane history. Content digest of the 73-file sorted
  `sha256sum` manifest: `ccb33753d2565b489eb57e755587a186563393d672b09d9eb9b4a7f2dcda5cd7`
  (`receipts/final-manifest.txt`, alongside `receipts/final-filelist.txt`).
- The wave directory is still growing while w1 seats write, so no snapshot is final: §6 is the
  re-run that covers the integration tip. What the four runs establish is that nothing landing in
  the wave directory in this interval adds a finding — the class, not one lucky byte count.

### 1a. The gate is not blind here — negative control

A clean verdict is only worth the detector behind it. A copy of the snapshot was seeded with one
synthetic leak per rule and rescanned; every planted class fired:

| planted shape | rule that fired |
|---|---|
| `hyprctl clients -j` element (`class` + `title`) in prose/fence | `R1_CLIENT_DUMP` |
| `ss -xpa` socket row carrying a program name and its pid | `R2_PROC_TABLE` |
| monitor object with `serial` + `description` | `R3_MONITOR_IDENT` |
| 11 bare `/home/<u>/…` path lines | `R4_HOME_LISTING` (`distinct_paths=11 limit=10`) |
| `/home/<u>/…:41:` grep prefix, `ls -R` header, tool diagnostic, `ls -l` row | `R7_HOME_PATH_PREFIX` (all four forms) |
| `ls -l` row owned by the account | `R8_ACCOUNT_COLUMN` |
| xdg-terminal-exec cache record | `R9_EXEC_CACHE` |

Receipts: `receipts/gate-canary.txt`, `receipts/gate-canary2.txt` (each `EXIT=1`). A deliberately
malformed prefix canary (home path *after* a `file:LINE:` colon) did **not** fire — correct: R7
defines the prefix form as a line *starting* with the home path, so the detector is not
over-firing either.

### 1b. Baseline: the tracked tree at lane HEAD is *not* clean

Same gate, same flags, on the lane's own tracked tree at `3ac316426497e8649bffedc88d28241d9bc71c52`:

```
SESSION_MATERIAL_RULES: R1_CLIENT_DUMP=42 R2_PROC_TABLE=42 R3_MONITOR_IDENT=15 R4_HOME_LISTING=3 R7_HOME_PATH_PREFIX=50 R8_ACCOUNT_COLUMN=57 R9_EXEC_CACHE=4 R5_SERIAL_PROSE=28
SESSION_MATERIAL_WAIVED: findings=49 files=47
SESSION_MATERIAL: files=24196 findings=241 rev=3ac316426497e8649bffedc88d28241d9bc71c52
```

`EXIT=1` (`receipts/gate-lane-head.txt`). Consequences to state plainly:

1. The wave's `findings=0` is a strict improvement over the tree it lands in, and the wave adds
   nothing to the 241.
2. **A wave-DONE privacy receipt cannot cite a green lane-wide gate at the integration tip** —
   it can only cite an unchanged-or-better count against this baseline. Anything else would be
   fabricated readiness.
3. Two of those pre-existing findings are the exact round-38 class in *tracked instruments*:
   `quality/counters/c2-r37-eventq.py` (9 `R2_PROC_TABLE` rows) and
   `quality/counters/c2-r38-eventq.py` (12). They are C1 ledger population members this round, so
   the round-51 tool ledger will point at tools that embed `ss` rows. Out of this seat's write
   scope (report-only), but the ledger's accountability pointers should not be read as a privacy
   endorsement of the pointed-at file.

## 2. Hand-check: what the gate structurally cannot see

### 2a. Home paths outside the lane's declared surfaces

Latest sweep (147-file snapshot, taken 10:0xZ): 84 `/home/<user>` occurrences on 54 lines in 19
files, all one account (`vgpnk`); no other `/home/<user>` exists anywhere. Distinct prefixes:

| prefix | count | surface |
|---|---|---|
| `/home/vgpnk/Projects/shokunin[/…]` | 64 | declared (fleet root + lane) |
| `/home/vgpnk/Projects/shokuknow[/…]` | 12 (+3 prose continuations) | declared read-only checkout |
| `/home/vgpnk/.omp/agent/RULES.md` | 4 | named by the dispatch's own tooling directive |
| `<home>/.cache/ai-usage` | **1** | **out of surface** |

Per-file counts over the earlier 73-file snapshot (66 occurrences, 41 lines, 10 files), unchanged
in kind by the later files — each newcomer repeats the lane surface:

| file | occ / lines | note |
|---|---|---|
| `w1-spec.json` | 17 / 6 | dispatch context/prompts; one JSON line carries several paths |
| `w1-dispatch.json` | 17 / 6 | same text, dispatched copy |
| `make-w1-spec.py` | 11 / 11 | dispatch generator literals: lane, fleet, shokuknow, `.omp` rules, scratch |
| `w1/CritBaseC2/base-c2-receipt.txt` | 7 / 7 | absolute lane paths inside recorded commands |
| `w1/RevWaveDone/wavedone-analysis.md` | 7 / 4 | lane + `/fast/scratch/hyaku/mado-r51/<seat>` (declared) |
| `w1/RevRouted50/routed-d1-d4.md` | 3 / 3 | lane paths inside `cd` / `--repo` examples |
| `w1.ready` | 1 / 1 | absolute dispatch path (lane) |
| `receipts/census-before.txt` | 1 / 1 | lane path as a third column of an `ok` row (lane surface) |
| `w1/RevC1Base/base-c1-receipt.txt` | 1 / 1 | lane path in a recorded command |
| `w1/ScoutQuarantine/quarantine-verdicts.md` | **1 / 1** | `<home>/.cache/ai-usage/status.json` (out of surface) |

Files that arrived later and also carry a lane path, checked individually — `w1/ExecFetchDispatch/
receipts/verify.txt` (2), `w1/ExecControlsC1/controls-c1/actual-run/ctl-e-lane-base.txt` (1),
`w1/ExecControlsC2/controls-c2/drive-controls-c2.py` (1),
`w1/ExecLedgerCounter/fixtures/build-fixtures.py` (1),
`w1/ExecLedgerPopulation/population.json` (1), `w1/RevengerLedger/ledger-rootcause.md` (1),
`w1/ScrLedgerRows/ledger-rows.md` (1), `w1/ScrLesson51.md` + `w1/ScrLesson51/round-51.md` (3 + 1),
`w1/SentPrivacy/privacy-scan.md` (4, this file's recipe and surface table) — every one a lane or
declared-checkout path in a recorded command, never a listing.

No listing shape exists (R4 = 0), and none of the four R7 structural shapes occurs
(prefix/header/diag/row = 0) — so nothing here is a `find`/`ls` dump or a pasted `grep -n` block.
Masked forms (`~/`, `$HOME/`) appear 6 times in the dispatch text; the convention the lane's own
probes use is present, just not universal.

### 2b. The one out-of-surface path (INFO, non-blocking)

`w1/ScoutQuarantine/quarantine-verdicts.md:26` records the absent-defect register row `S224` whose
URL is a host-private cache file: `<home>/.cache/ai-usage/status.json` (path masked here on
purpose). Disposition:

- It is a **single prose-form pathname in a register quote**, not a listing, not a capture, not a
  payload.
- It is **already tracked at base**, verbatim, in `corpus/lessons/round-34.md:62` (and echoed in
  `corpus/lessons/round-39*.md`, prior `ScoutQuarantine` reports, and the register itself in the
  read-only shokuknow checkout). The wave therefore adds no new exposure; it repeats an accepted
  one.
- The register row is quoted *because* the seat had to say the capture is unverifiable. Removing
  the path would remove the reason for the verdict.

Recommendation (L1's call, not a blocker): if the lane wants the compliant form everywhere, mask
it as `<home>/.cache/ai-usage/status.json` in the seat file. I did not edit a sibling seat's file.

### 2c. Classes with zero occurrences (frozen snapshot, 73 files)

| class | probe | hits |
|---|---|---|
| process table / pids | `ss -xpa` socket rows, program+pid columns | 0 |
| socket / runtime dir | `/run/user/<n>`, wayland/hypr instance signatures | 0 |
| monitor identity | monitor JSON objects (serial + description/make/model), window-title keys | 0 (the `serial`/`initialTitle` key literals inside the fetched HyprCtl.cpp are upstream format strings, not leaked identities) |
| window titles / clipboard | `wl-paste`, `cliphist`, `grim`, screenshots | 0 |
| live hypr state | `hyprctl binds`, bind dumps, live receipts | 0 |
| credentials | key/secret/token literals, private keys, `op://` refs | 0 (the 16 `token=` matches are the dispatch's own sentence "secret-shaped material (session tokens, op:// refs…)" — the *instruction*, not a value) |
| network identity | IPv4, MAC, e-mail, `@host.tld` | 0 |
| non-public URLs | `localhost`, `127.0.0.1`, RFC1918 | 0 |
| binaries / non-UTF-8 / symlinks / oversize | `-size +100k`, `iconv`, `-type l` | **1 non-text blob — see §2e** (no symlink, no file over 100 KB; largest text 97 KB, `Hyprland-HyprCtl.cpp`) |

URLs present are public and are register citations: `wiki.hypr.land`, `raw.githubusercontent.com`
(Hyprland `efb50993`), `wiki.archlinux.org`, `mirror.sjtu.edu.cn`, `arxiv.org`, `blog.csdn.net`.

### 2d. Account-name exposure

The account literal appears only inside paths (§2a). The lane's tracked tree already carries it in
5 872 files at base, so it is pre-existing and not a wave delta. No `ls -l` owner/group column
(`R8`) occurs in the wave.

### 2e. Non-text blobs: the gate's blind spot, and the one thing it missed here

`check-session-material.py` scores *text* shapes (line prefixes, listings, JSON objects). A
compiled blob carrying a home path is invisible to it. The wave directory contains exactly such a
blob:

```
w1/ExecLedgerCounter/fixtures/__pycache__/build-fixtures.cpython-314.pyc   18 640 bytes
  embedded: /home/<lane>/.ufo/waves/round-51/w1/ExecLedgerCounter/fixtures/build-fixtures.py
  embedded: source mtime 2026-10-27T10:01:34Z, source size 14 601 bytes (pyc header)
```

- **Gate verdict on it: none.** `grep -I` treats it as binary, R4/R7 are line-shape rules over
  text, so the scan reports `findings=0` while the blob holds an absolute home path. This is a
  property of the gate, not of this file.
- **Commit risk: none.** The lane's `.gitignore:3` ignores `__pycache__/`, and
  `git check-ignore -v` confirms this exact path is ignored; `git ls-files '*.pyc'` is empty, so no
  `.pyc` is tracked anywhere in the lane. The L1 must simply not `git add -f` it.
- **Why it still matters.** (i) The wave-DONE receipt's `findings=0` needs the qualifier "over
  text blobs"; stated without it, it is a false claim about the directory. (ii) Any future
  non-ignored compiled artifact — a fixture `__pycache__` under a path the ignore rule does not
  cover, an archive, a `.zip` of fixtures — would commit a host path with the gate green.

Smallest remediation, in order: delete `w1/ExecLedgerCounter/fixtures/__pycache__/` before the
wave-DONE snapshot (it is stale output, not a deliverable); keep `.gitignore:3`; and, if the lane
wants the class closed at the gate, extend `check-session-material.py` with a binary-blob rule
(`strings`-style home-path and serial scan for any blob that fails UTF-8 decoding) — that is a
tracked-file change and belongs to the L1, not to this seat.

## 3. Fetch pins

Round-51's pins **landed while this seat ran** (`w1/ExecFetchDispatch/fetch/`, 14 files, written
06:59Z). They were absent at my first snapshot and present at my third, so both states are
recorded: the earlier absence, and the hand-check of what arrived.

### 3a. Round-51 pins — hand-checked, clean

`w1/ExecFetchDispatch/fetch/` carries 11 Hyprland files (`KeybindManager.{cpp,hpp}`,
`legacy-DispatcherTranslator.{cpp,hpp}`, `legacy-ConfigManager.cpp`, `ConfigManager.{cpp,hpp}`,
`ConfigActions.{cpp,hpp}`, `HyprCtl.cpp`, `docs/hyprctl.1.rst`), 3 hyprland-wiki pages
(`Dispatchers`, `Binds`, `Using-hyprctl`), plus `SHA256SUMS` and `fetch-manifest.json`; the
generator `w1/ExecFetchDispatch/fetch-all.sh` and the anchor list `anchors.txt` sit beside it.

| check | result |
|---|---|
| provenance | every row of `fetch-manifest.json` names `raw.githubusercontent.com` at pinned revisions (Hyprland `efb50993…`, wiki `d5f07c60…`); transport is `curl -fsSL` to that host only |
| digests | `sha256sum -c --quiet SHA256SUMS` → all 14 match (independent re-check, not the manifest's own `blob_verified` claim) |
| self-row | `SHA256SUMS` names **no** `SHA256SUMS` row; `fetch-all.sh` explicitly refuses one (`grep -q ' SHA256SUMS$'` → exit 6), so D4/M50-9 is structurally prevented for this pin set |
| host-private bytes | no `/home/`, `/tmp`, `/etc/`, serial+description object, socket row, `pid=`, e-mail, IP, MAC, or credential literal in any pin, `anchors.txt`, or `fetch-all.sh` |
| local annotation | no `mado`/`round-51`/seat marker inside the pinned bytes, i.e. the fetches were not hand-edited |
| live capture | **none** — this pin set is upstream-source-only; nothing captured host state (unlike round-50's `binds-live-r50.txt`) |
| shape hygiene | no binaries, no executable mode, all files UTF-8 |

The two `"serial"` / four `initialTitle` occurrences are in `Hyprland-HyprCtl.cpp` (`"serial":
"{}",` at `:237`) — upstream JSON format strings, not leaked identities; R3 correctly does not
fire because no object carries a serial *value* with an identifying key.

Remaining obligation for the copy into the canonical location: `claims.md` names the pins under
`.ufo/waves/round-51/fetch/`, which **does not exist yet** (`test -e` → absent at every snapshot).
Whoever copies `w1/ExecFetchDispatch/fetch/*` there must copy the bytes unchanged — a re-fetch or
re-serialization would void the digests above, and the C2 predicate binds cited lines to these
exact files. Re-run the gate after the copy (§6).

### 3b. Round-50 pins (inherited by C2 per claims.md) — clean

The 17 files under `.ufo/waves/round-50/fetch/` are upstream sources (Hyprland `ConfigValues`,
`IKeyboard`, `InputManager`, `KeybindManager`, legacy `ConfigManager`; xkbcommon sources; two wiki
pages) plus one live receipt, `binds-live-r50.txt`. That receipt is shape-only and I verified the
claim rather than trusting its trailer: a `hyprctl version` line, 192 binds by key form, a
`modmask` histogram, 14 keycodes, and an explicit statement that the raw 90 401-byte JSON is
**not embedded** (only its sha256 `9a4719…`). No device name, title, dispatcher argument, bind
description, or home path appears in it. `grep` over the pin directory finds no home path, no
socket row, no serial/title object.

### 3c. D4/M50-9 is a correctness defect, not a privacy one

Round-50's `fetch/SHA256SUMS` still lists itself (`bb21f728…  SHA256SUMS`), the self-row D4
routes. A file that hashes itself cannot verify itself — but it carries no host-private byte.
Recorded so the two routed items are not conflated; the fix belongs to the receipt owner, and per
the wave contract the round-50 bytes must not be edited.

### 3d. Adjacent observation (not privacy, routed to whoever owns scratch discipline)

`w1/ExecFetchDispatch/fetch-all.sh:59` defaults its staging dir to
`mktemp -d "${TMPDIR:-/tmp}/…"`: it honours `TMPDIR` and takes `--scratch`, but falls back to
`/tmp`. Under the operator scratch directive a probe script's *default* should not be `/tmp`.
`w1/ExecDiskHygiene/hygiene-scan.py` (landed in the same wave) has a `REVIEW` verdict class
covering exactly this shape — flagging so the L1 can route it to that seat's reviewer rather than
discover it at integration.

## 4. Fixture discipline

- Scratch root: `/fast/scratch/hyaku/mado-r51/SentPrivacy/` (snapshot repos, canaries, receipts);
  wiped at seat end, receipts copied here first.
- The throwaway repositories are fixture-local: each `git rev-parse --show-toplevel` was asserted
  equal to its own scratch dir before `git add`/`commit`; no lane, fleet, or shokuknow git state
  was touched by a mutating command. Read-only `git grep`/`ls-tree` only in the lane.
- `TMPDIR` was pointed at the scratch root for every gate run.
- The compositor config planes were read as bytes only: no socket connection, no service touched,
  no `hyprctl` call. **Consequence:** `--serial-from-host` (R6, exact-serial substring) is
  deliberately **unarmed**, because reading the live monitor serial requires `hyprctl`. R5's
  serial-shape scan ran and found 0 in the wave. R6 remains an L1-side option at integration (§6).

## 5. Verdict

| axis | verdict |
|---|---|
| wave dir vs. rule-4 session material (gate) | **PASS** — `files=164 findings=0` over the committable set (58/73/115/164 across four snapshots), canary-proven detector |
| hand-check: out-of-surface host paths | **PASS (1 INFO)** — one pre-existing, already-tracked cache pathname in an `S224` register quote |
| hand-check: process/socket tables, monitor identity, titles, credentials, network identity | **PASS** — 0 occurrences each |
| round-51 fetch pins | **PASS** — 14 upstream-only pins, digests re-verified by `sha256sum -c`, no self-row, no live capture |
| non-text blobs | **PASS with a caveat** — one `.pyc` with an embedded host path; gitignored, not committed; gate blind to it (§2e) |
| round-50 pins (inherited) | **PASS** — upstream bytes + one verified shape-only live receipt |
| lane-tree baseline | **RED, pre-existing** — 241 findings / 49 waived at `3ac3164`; no wave delta |

Nothing in the wave is a commit blocker. The residual risks, in order: (i) the pins must be
copied to `.ufo/waves/round-51/fetch/` byte-for-byte, not re-fetched; (ii) a wave-clean gate is
not a lane-clean gate (241 pre-existing findings); (iii) the gate reads only text, so a compiled
or archived artifact would pass it while carrying a home path — delete `__pycache__/` and do not
`git add -f` a `.pyc`.

## 6. Re-run at the integration tip (L1)

The wave keeps growing after any snapshot, so the receipt that counts is the one at the tip.
Writes only to a scratch dir; lane read-only:

```sh
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin      # declared lane surface
WORK=/fast/scratch/hyaku/mado-r51/<seat>              # TMPDIR + fixture root
mkdir -p "$WORK/snap/wave"
cp -a "$LANE/.ufo/waves/round-51/." "$WORK/snap/wave/"
cp "$LANE/.gitignore" "$WORK/snap/.gitignore"   # model what the lane would actually commit
cd "$WORK/snap" && git init -q . && git add -A
git -c user.name=scan -c user.email=scan@localhost -c commit.gpgsign=false commit -qm snapshot
test "$(git rev-parse --show-toplevel)" = "$WORK/snap"     # fixture guard
cd "$LANE"
TMPDIR="$WORK" python3 -I quality/check-session-material.py \
    --repo "$WORK/snap" --rev HEAD --scope all --account "$(id -un)"
# expected: SESSION_MATERIAL: files=<n> findings=0 ... , exit 0
# optional exact-serial arm, only where hyprctl is permitted:
#   ... --serial-from-host
```

Compare against `receipts/gate-lane-head.txt` (241 findings at `3ac3164`); the wave must not raise
that count. Then delete `$WORK`.

## Deliverables
- `.ufo/waves/round-51/w1/SentPrivacy/privacy-scan.md`
- `.ufo/waves/round-51/w1/SentPrivacy/receipts/gate-final.txt`
- `.ufo/waves/round-51/w1/SentPrivacy/receipts/gate-wave.txt`
- `.ufo/waves/round-51/w1/SentPrivacy/receipts/gate-lane-head.txt`
- `.ufo/waves/round-51/w1/SentPrivacy/receipts/gate-final2.txt`
- `.ufo/waves/round-51/w1/SentPrivacy/receipts/gate-final5.txt`
- `.ufo/waves/round-51/w1/SentPrivacy/receipts/gate-final6.txt`
- `.ufo/waves/round-51/w1/SentPrivacy/receipts/final6-filelist.txt`
- `.ufo/waves/round-51/w1/SentPrivacy/receipts/gate-canary.txt`
- `.ufo/waves/round-51/w1/SentPrivacy/receipts/gate-canary2.txt`
- `.ufo/waves/round-51/w1/SentPrivacy/receipts/final-filelist.txt`
- `.ufo/waves/round-51/w1/SentPrivacy/receipts/final-manifest.txt`

Report: .ufo/waves/round-51/w1/SentPrivacy.md
