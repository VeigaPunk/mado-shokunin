# SentPrivacy — privacy scan of the round-51 wave dir (w1, round 51)

**Verdict: PASS — no commit blocker.** `.ufo/waves/round-51/` carries no rule-4 session material
that this seat could find, and the two items it did find are (a) a pathname already tracked in the
lane at base and (b) a gitignored `.pyc` that proves a gate blind spot rather than a leak.

## Gate verdict (pasted)

`quality/check-session-material.py` reads a *committed* revision, so the untracked wave dir was
snapshotted into a throwaway repo in seat scratch (lane left untouched):

```
files=164  pyc_staged=0
SESSION_MATERIAL: files=164 findings=0 rev=124f48c83471ada589773d736585fac223e91d0f
gate_exit=0
# re-run after this report's final revision:
SESSION_MATERIAL: files=175 findings=0 rev=341ca00db4641fe547ff800c16dca00082f74526
gate_exit=0
```

Four snapshots (58 / 73 / 115 / 164 → 175 files) as seats kept landing work, all `findings=0`; the
last applies the lane's own `.gitignore`, so it models what the L1 would actually commit.

**The detector works** — a seeded canary copy fired every class: `R1_CLIENT_DUMP`,
`R2_PROC_TABLE`, `R3_MONITOR_IDENT`, `R4_HOME_LISTING`, `R7_HOME_PATH_PREFIX` (all four forms),
`R8_ACCOUNT_COLUMN`, `R9_EXEC_CACHE` (`EXIT=1`). A malformed prefix canary correctly did *not*
fire, so it is not over-firing.

## Lane baseline is red, pre-existing

Same gate on the lane's own tracked tree at `3ac316426497e8649bffedc88d28241d9bc71c52`:
`files=24196 findings=241`, `WAIVED findings=49 files=47`, `EXIT=1` (`receipts/gate-lane-head.txt`).
So the wave adds nothing, **but no wave-DONE receipt may cite a green lane-wide gate** — only an
unchanged-or-better count against this baseline. Two of those findings are the round-38 class in
tracked instruments the C1 ledger will point at: `quality/counters/c2-r37-eventq.py` (9
`R2_PROC_TABLE` rows) and `quality/counters/c2-r38-eventq.py` (12).

## Per-file hand-check

- **Home paths:** 84 occurrences on 54 lines in 19 files, one account only. Surfaces:
  `/home/…/Projects/shokunin` 64 (declared fleet+lane), `/home/…/Projects/shokuknow` 15
  (declared read-only), `/home/…/.omp/agent/RULES.md` 4 (named by the dispatch) — **one out of
  surface**: `w1/ScoutQuarantine/quarantine-verdicts.md:26`, the `S224` register URL
  `<home>/.cache/ai-usage/status.json`. INFO, non-blocking: already tracked verbatim at base in
  `corpus/lessons/round-34.md:62`; masking it in the seat file is the L1's call (not my file).
- **Process/socket tables, monitor serials, window titles, clipboard, credentials, IP/MAC/e-mail,
  localhost/RFC1918:** 0 each. The 16 `token=` hits are the dispatch's own sentence about
  secret-shaped material — an instruction, not a value. The `serial`/`initialTitle` literals in
  the pins are upstream `HyprCtl.cpp` format strings.
- **Non-text blobs (the gate's blind spot, §2e of the scan):**
  `w1/ExecLedgerCounter/fixtures/__pycache__/build-fixtures.cpython-314.pyc` (18 640 B) embeds
  the absolute source path plus source mtime/size. **Not a commit risk** — `.gitignore:3` ignores
  `__pycache__/`, `git check-ignore -v` confirms this exact path, `git ls-files '*.pyc'` is empty.
  Remediation: delete the `__pycache__/` before the wave-DONE snapshot and never `git add -f` a
  pyc; optionally add a binary-blob rule to the gate (tracked-file change → L1).

## Fetch pins

- **Round-51 pins landed mid-seat** at `w1/ExecFetchDispatch/fetch/` (14 pins + `SHA256SUMS` +
  `fetch-manifest.json`, generator `fetch-all.sh`, anchor list `anchors.txt`). Hand-checked clean:
  raw.githubusercontent.com only at pinned revs, `sha256sum -c --quiet SHA256SUMS` re-verified all
  14 independently, **no self-row** (D4/M50-9 structurally prevented by an explicit check at
  `fetch-all.sh:104`), no `/home`, no serial/title object, no live capture, no binaries, no local
  annotations inside the pinned bytes.
- Canonical `.ufo/waves/round-51/fetch/` still **absent** — whoever copies the pins there must copy
  bytes unchanged (a re-fetch voids the digests the C2 predicate binds to). Re-run the gate after.
- **Round-50 pins** (inherited): upstream sources + `binds-live-r50.txt`, which I verified is
  shape-only (version line, 192 binds by key form, modmask histogram, 14 keycodes, raw JSON
  digest only, no title/device/path). Clean. Its `SHA256SUMS` self-row (D4) is a correctness
  defect, not privacy; round-50 bytes must not be edited.
- Adjacent, not privacy: `fetch-all.sh:59` falls back to `mktemp -d "${TMPDIR:-/tmp}/…"` — honours
  `TMPDIR` and takes `--scratch`, but the `/tmp` default is the scratch-rule shape
  `w1/ExecDiskHygiene/hygiene-scan.py` flags as REVIEW. Routed for that seat's reviewer.

## Discipline

No lane/fleet/shokuknow tracked file written; no mutating git outside my own scratch fixtures
(toplevel asserted for each); no compositor socket contact, no `hyprctl` — so `--serial-from-host`
(R6) is deliberately unarmed, with R5's serial-shape scan at 0. Scratch
`/fast/scratch/hyaku/mado-r51/SentPrivacy/` deleted; receipts copied first. No tool installed.

## Deliverables
- `.ufo/waves/round-51/w1/SentPrivacy/privacy-scan.md`
- `.ufo/waves/round-51/w1/SentPrivacy/receipts/gate-final.txt`
- `.ufo/waves/round-51/w1/SentPrivacy/receipts/gate-final2.txt`
- `.ufo/waves/round-51/w1/SentPrivacy/receipts/gate-final5.txt`
- `.ufo/waves/round-51/w1/SentPrivacy/receipts/gate-final6.txt`
- `.ufo/waves/round-51/w1/SentPrivacy/receipts/gate-wave.txt`
- `.ufo/waves/round-51/w1/SentPrivacy/receipts/gate-lane-head.txt`
- `.ufo/waves/round-51/w1/SentPrivacy/receipts/gate-canary.txt`
- `.ufo/waves/round-51/w1/SentPrivacy/receipts/gate-canary2.txt`
- `.ufo/waves/round-51/w1/SentPrivacy/receipts/final-filelist.txt`
- `.ufo/waves/round-51/w1/SentPrivacy/receipts/final-manifest.txt`
- `.ufo/waves/round-51/w1/SentPrivacy/receipts/final6-filelist.txt`

Report: .ufo/waves/round-51/w1/SentPrivacy.md
