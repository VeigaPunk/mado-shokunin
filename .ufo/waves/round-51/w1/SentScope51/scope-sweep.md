# Round 51 w1 — scope & safety sweep (SentScope51)

Scope: every file written under `.ufo/waves/round-51/w1/` (and its seat dirs) by
the wave's 43 seats, scanned mid/late wave against four assigned checks plus the
declaration-integrity check that decides whether a seat's report points at
anything. Read-only against the lane: no tracked file, config plane, sibling
lane or host service was touched, and no git/jj mutation was run anywhere except
inside throwaway fixtures under `/fast/scratch/hyaku/mado-r51/SentScope51/`.

Tool: `check-scope.py` (this seat) — hermetic `--selftest`, 12/12 cases pass
(`receipts/selftest.txt`), honours `--scratch`/`TMPDIR`, writes nothing to a tmp
literal.

Snapshot of record: `receipts/sweep-final.txt`, 2026-10-27T10:07:15Z, 253 files
under round-51. The wave was still writing during the sweep, so the seat-written
set grew 155 → 177 → 238 → 253 files across passes; the checks were
re-run on each snapshot and every verdict below held at each one. Lane HEAD
stayed `3ac316426497e8649bffedc88d28241d9bc71c52` throughout
(`receipts/write-scope.txt`) — no seat committed anything.

## Verdict per check

| # | Check | Verdict | Evidence |
|---|-------|---------|----------|
| 1 | Nothing written outside the wave / seat dirs | **PASS** | `receipts/write-scope.txt`, `receipts/sweep-final.txt` |
| 2 | No secret-shaped material in pins or receipts | **PASS** (0 hits, 0 private locators) | `receipts/session-gate.txt`, `receipts/sweep-final.txt` |
| 3 | No hardcoded `/tmp` in drafted tools | **PASS** (0 defects, 6 classified review lines) | `receipts/sweep-final.txt` |
| 4 | Fetch pins are upstream bytes only, no private paths | **PASS with two routed items** | `receipts/pins-verify.txt`, `receipts/pins-verify-scr.txt` |
| 5 | Declarations resolve to files, none escape the wave | **PASS so far** — 2 declared paths still absent while seats run | `receipts/sweep-final.txt` |

## 1. Write scope

`git status --porcelain --untracked-files=all` in the lane (snapshot
2026-10-27T10:02:57Z, 163 untracked entries):

- untracked **outside** `.ufo/waves/round-51/`: **none**.
- untracked outside `.ufo/waves/round-51/w1/`: exactly one —
  `.ufo/waves/round-51/w1.ready.dispatched`, the L1 dispatch marker (inside the
  round dir; not a seat write).
- tracked modifications, staged changes, deletions: **none** in every pass
  (1 through 7). The tracked tree is still bit-identical to HEAD, so no seat wrote
  a tracked path.
- ignored entries inside round-51: one seen at pass 5 —
  `w1/ExecLedgerCounter/fixtures/__pycache__/` (a fixture run's bytecode cache,
  git-ignored so it could never be committed); gone again by the final pass.
- structure: registry `members` = 43, seat reports = 43, seat dirs = 43, exact
  one-to-one match — no dead seat, no orphan dir, no straggler report.
- lane size: `round-51/w1` 2.1 M total at the final pass, no file above 2 M.

Host side effects outside the repo, checked directly (no mtime change in the
last 180 min): `~/.config/{hypr,waybar,walker,omarchy,alacritty,kitty,foot}`,
`~/.local/bin`, `/home/vgpnk/Projects/shokuknow`. Fleet-root
`/home/vgpnk/Projects/shokunin` shows only two untracked items, both foreign to
this round (`.scratch/closure-mado-r50.json`, `.ufo/reports/round-61/kake.md`).

Pre-existing `/tmp` residue, **not** this wave: 676 `w5-mado-m52-selftest.*`
dirs, 175 M, oldest 2026-10-26T12:34Z — a prior wave's fixture driver never
cleaned up. Routed as an observation only (outside round-51 write scope).

## 2. Secret / session-material shapes

Two independent instruments agree:

- `quality/check-session-material.py` over a scratch fixture containing **all
  untracked round-51 files** — `files=155 findings=0` on the first snapshot and
  `files=241 findings=0` on the last, exit 0 both times
  (`receipts/session-gate.txt`). The gate was run read-only against the lane
  (`--rev`) and against the fixture; the lane's working tree was not modified.
- Baseline for that comparison, so the zero is interpretable: the gate exits 1
  at the round base `6ca8c559` with `findings=241 waived=49` and at HEAD
  `3ac31642` with the identical `findings=241 waived=49`
  (`receipts/session-gate-base.txt`, `receipts/session-gate-head.txt`). The 241
  are the gate's own fixtures and older waves' probe bodies, present before w1;
  they are unchanged by this wave. **w1 adds zero findings.**
- `check-scope.py` shape scan over the wave (op:// refs, gh/gho/ghs/ghp, sk-,
  AKIA, xox*, PRIVATE KEY blocks, Bearer, JWT, basic-auth URLs; loopback/RFC1918
  URLs, file://, ssh://, tailnet names): `secret_hits=0 private_locators=0`.
  The only earlier hits were the scanner's own rule literals, which the tool now
  skips by paren-tracked `re.compile(` block.

Paths that look private but are not secrets: `/home/vgpnk/...` appears in prose
and CLI examples (`w1/RevRouted50/routed-d1-d4.md`) and as `--repo` defaults in
drafted tools (`ExecLedgerCounter/fixtures/build-fixtures.py:232`,
`ExecControlsC2/controls-c2/drive-controls-c2.py:100`) and one hardcoded seat
constant (`ExecControlsC1/controls-c1/verify-controls.py:8`,
`SEAT = "/home/vgpnk/.../ExecControlsC1"`). No receipt reproduces tool output
containing a home path, account column, serial or window title. The hardcoded
`SEAT` constant is a portability wart (the verifier cannot run from a copy), not
a privacy leak — routed as low severity.

## 3. Scratch rule (hardcoded `/tmp`)

`tmp_defects=0`. All 20 drafted `.py`/`.sh` instruments were scanned with
literals classified rather than counted:

- tmpish literals found, all in **refusal or sandbox position**, not as write
  targets: `ExecLedgerGate/check-tool-ledger.py:69`
  (`REFUSED_WORK_PREFIXES = ("/tmp", "/var/tmp", "/dev/shm")`),
  `ExecControlsC1/controls-c1/check-tool-ledger.py:322` (same refusal band),
  `ExecDiskHygiene/selftest-probe.py:36` (`TMPISH = (...)` table).
- `mkdtemp(...)` without `dir=`: `ExecFetchDispatch/verify-anchors.py:100`
  (`args.scratch or tempfile.mkdtemp(prefix=...)`) and
  `ExecLedgerCounter/fixtures/build-fixtures.py:183`
  (`args.work or $TMPDIR or tempfile.mkdtemp()`). Both honour `TMPDIR` by
  construction and both accept an explicit scratch argument, so neither is a
  rule-4 defect.
- every instrument either accepts `--work`/`--scratch` or writes nothing:
  `verify-quotes.py` states and honours "no writes, no network, no /tmp";
  `make-fixture.py` variants take explicit `--fixture` paths.

## 4. Fetch pins

Two pin sources exist, both still inside seat dirs (`.ufo/waves/round-51/fetch/`
does not exist yet — see routed items).

`w1/ExecFetchDispatch/fetch/` — 19 upstream files + `SHA256SUMS` +
`fetch-manifest.json` (the set was 14 pins when the sweep started; the seat
extended it mid-wave):

- `sha256sum -c SHA256SUMS`: 19/19 OK.
- Independent manifest cross-check: for all 19, the recomputed git blob sha1
  (`sha1("blob <len>\\0" + bytes)`) equals the manifest's `git_blob_sha1`, so the
  bytes are bound to the claimed upstream revisions —
  `efb50993780079460b0cbed1363e2166a2de1d9f` (Hyprland, 12 files),
  `a21e87b878e72ee5dfd375899e8b2ad0d0c4c0e1` (Hyprutils, 4),
  `d5f07c60e16fe03744aabb76e492117b7f7c4679` (hyprland-wiki, 3); sha256 and byte
  counts also match. 19/19, 0 mismatches.
- transport is `raw.githubusercontent.com` only — every URL in the manifest is
  that host, and no `file://`, remote-shell URL, loopback, `/home`,
  `/fast/scratch` or `/srv` string appears anywhere in the pin set
  (`local_refs=0`).
- `SHA256SUMS` carries **no self row and no manifest row** — the D4/M50-9 rule
  (digest pins only) is honoured in the new manifest, and
  `fetch-manifest.json` says so explicitly (`sums_self_row`).

`w1/ScrDispatchEntry/fetch/Hyprland-SharedDefs.hpp` — one extra pin, **no
manifest**:

- Re-fetched upstream read-only: byte-identical to
  `.../Hyprland/efb5099…/src/SharedDefs.hpp`
  (`sha256 0b40cc83f827587f3a94260ca89d4464150dc2b45de2b9331e3d1876cafe0087`),
  so the byte provenance is upstream. Verdict: **PIN_UNMANIFESTED**, not
  PIN_SUBSTITUTED.
- Filename hazard: the local name implies `src/managers/SharedDefs.hpp`, which
  404s at that revision (my first re-fetch attempt failed on exactly that
  assumption). A later seat re-fetching by filename would get a 404 and could
  wrongly conclude the pin is unreachable.

Synthetic pin fixture: `w1/ExecControlsC2/controls-c2/fixtures/scaffold/files/.ufo/waves/round-51/fetch/`
is a control fixture (the "entry citing rows with no pins" MISS case). It is
scanned for local paths (`0`) and is deliberately exempt from the manifest
requirement — a fixture must not be held to the pin contract.

## 5. Declaration integrity (mid-wave, not a freeze verdict)

228 declarations parsed from 43 reports (169 at pass 7, 112 at pass 5), 0
resolving outside the wave dir — no seat declared a path it wrote into the
tracked tree. 2 declared paths are not yet on disk (down from 12 an hour
earlier); both belong to a seat that is still running:

- `ScrDispatchEntry.md` → `…/ScrDispatchEntry/held-citations.md`
- `ScrDispatchEntry.md` → `…/ScrDispatchEntry/pin-manifest.md`

They are pending, not absent, at this snapshot; a declared-but-missing path at
freeze is an ABSENT defect under QUALITY 101, so L1 must re-run this check at
the freeze tip (`check-scope.py --lane <lane> --wave .ufo/waves/round-51`). Full
list per pass in `receipts/sweep-pass5.txt`, `sweep-pass6.txt`, `sweep-final.txt`
§[E].

One ambiguity worth naming: `ExecFetchDispatch.md` declares
`…/ExecFetchDispatch/fetch-manifest.json` while the file lives at
`…/ExecFetchDispatch/fetch/fetch-manifest.json`. If L1 copies pins to
`.ufo/waves/round-51/fetch/`, the declared seat path will not exist — either the
report or the integration copy has to pick one location.

## Routed items (for L1, smallest fix first)

1. **PIN_UNMANIFESTED** — before freeze, `ScrDispatchEntry/fetch/Hyprland-SharedDefs.hpp`
   needs a `SHA256SUMS` row and a manifest entry naming
   `src/SharedDefs.hpp` (not `src/managers/…`), with the sha256 above.
2. **Pin path** — claims C2 binds rows to pins "under `.ufo/waves/round-51/fetch/`";
   that directory does not exist yet. Pins currently live in
   `ExecFetchDispatch/fetch/` and `ScrDispatchEntry/fetch/`. Consolidate and
   checksum once, then the C2 counter's clause (b) can resolve them.
3. **Declaration ambiguity** — `ExecFetchDispatch.md` manifest path (above);
   resolve before the freeze re-run so the sweep's absent count reaches 0.
4. **Hygiene, cosmetic** — either take a `--seat` argument in
   `ExecControlsC1/controls-c1/verify-controls.py` or accept that it is
   host-specific (its `SEAT` constant is an absolute lane path).
5. **Observation, outside round 51** — 175 M of `w5-mado-m52-selftest.*` dirs in
   `/tmp` (676 dirs) from a prior wave's fixture driver; nothing in w1 created
   them, and disk guard reports `/fast/scratch/hyaku` at 64% (289.3 G free), so
   no action is urgent.

## Receipts

- `receipts/selftest.txt` — `check-scope.py --selftest`, 12/12.
- `receipts/write-scope.txt` — git status snapshot, HEAD, ignored entries.
- `receipts/sweep-pass5.txt`, `receipts/sweep-pass6.txt` — intermediate snapshots
  (177 and 237 files).
- `receipts/sweep-final.txt` — full sweep output (253 files, 2026-10-27T10:07:15Z).
- `receipts/session-gate.txt` — gate over the 155- and 241-file seat snapshots
  (`findings=0` both).
- `receipts/session-gate-base.txt`, `receipts/session-gate-head.txt` — gate at
  base and HEAD (241 findings / 49 waived at both: pre-existing).
- `receipts/pins-verify.txt` — sha256 + git-blob binding for the 14-file pin set.
- `receipts/pins-verify-scr.txt` — upstream byte-identity check for the extra pin.
