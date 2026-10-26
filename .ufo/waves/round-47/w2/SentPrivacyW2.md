# SentPrivacyW2 — session material in the round-47 wave files (w2 falsify, 2026-10-26)

Seat dir: `.ufo/waves/round-47/w2/SentPrivacyW2/` (`findings.md`, `README.md`, `ledger.tsv`,
`class-summary.txt`, `blind-spots.tsv`, `gate-controls.tsv`, `gate-run.txt`, `gate-selftest.txt`,
`sweep-redacted.txt`, `live-value-compare.txt`). Values are never written: every locator is
`path:line` plus a class.

## Verdict

**The wave dir holds no live window title, no live monitor identity and no credential**, and the
frozen gate is intact (blob identical at `d7527d6` and at the lane tip; selftest 22/22). But:

1. **Six classes of session material are present in files the gate reports clean**, the two
   worst being a live environment dump and a host cache record with nanosecond times.
2. **The gate cannot see eleven shapes**, each proven with a control in a scratch clone
   (binary container, 20000-object cap, 16 MiB cap, human block, TSV, `ps` table, `ss` without
   `-p`, monitor object without a serial, five path lines, MAC objects, symlink).
3. **The wave dir cannot pass its own gate**: 4 findings land in it, all gate self-matches
   (3 in the w1 copy of the gate, 1 in a w2 probe script). The lane gate has no waiver, so the
   data commit carries them; state them rather than "fix" the gate after data.

Every hole below is reproducible before the data commit, which is what this wave is for.

## Instruments

| instrument | result |
|---|---|
| `quality/check-session-material.py --selftest` | `SELFTEST: passed=22/22 failed=0` |
| same gate, `--repo <clone> --rev HEAD` on the wave-dir snapshot | 4 findings under the wave dir, 0 naming this seat, 119 tree-wide (115 pre-existing) |
| `w1/SentPrivacy/sweep-privacy.py --worktree <wave>` | G1=6/11, G2=418/5519, G3=11/12, G10=11/22, G11=2/5; G4/G5/G7/G9=0 |
| own census (10 classes, locators only) | `ledger.tsv` rows=289 over 1217 text blobs |
| own live-value match (booleans) | `live-value-compare.txt` |

## Findings (path:line, class, instrument status)

| # | sev | locator | class | gate | sweep |
|---|---|---|---|---|---|
| F1 | med-high | `w1/ExecLive/receipts/live-host.txt:10-28` (session keys at `:18,19,20,21,22,23,24,25,26,27`); `w2/CritUwsm/{daemon,hyprland,manager}-env` (3 × 19 keys); `w1/SentHost/receipts/ambient-cache-env.txt:5-6` | live environment dump; four values equal the live ones verbatim | **0** | G1, 2 of the 7 keys the round's own P5 forbids |
| F2 | med | `w1/ExecLive/receipts/live-host.txt` — 13 distinct account paths, 0 whole-line | home inventory above R4's own limit | **0** (R4 needs whole lines) | G2 fires but over-counts 6× |
| F3 | med | `w1/ExecLive/receipts/live-host.txt:109-121`; `w1/SentHost/receipts/host-cache-observed.txt:3-5,9`; `w1/ExecLive/receipts/raw/scratch-cache.txt:1-4`; `w2/CritUwsm/cacheA-content` | host resolver cache: path, sha256, nanosecond mtime, body; the size change dates another seat's host write | **0** | G11 needs the epoch form → blind |
| F4 | med | `w1/ScrToolLedger/receipts/live-receipts.txt:10`; 6 × `w1/ExecControls/c2/<CTL>/files/corpus/SOURCES.md:222` | instance signature in full (`40hex_pid_timestamp`), stale, already public at `corpus/SOURCES.md:222` | **0** | G3 files it as a uid path (understated) |
| F5 | med | controls `c1..c14` in `gate-controls.tsv` | eleven gate shapes unseen (table below) | see table | - |
| F6 | low | `w1/ExecStraceTrip/receipts/trace-*.txt:1`; `w1/CritOracle/execve-{cold,warm}.log:1`; `w1/ExecRefA/receipts/strace-*.txt:3` | raw strace with pid and argv (P8) | **0** | G10 |
| F7 | low | `w1/ScrEntry/receipts/live-print.txt:16`; `w1/ScrMistakes/receipts/pyc-state.txt:3`, `r2-state.txt:5-12`; `w1/ScrToolLedger/receipts/absence.txt:14` | `ls -l` line: owner+group, size, exact time | **0** | none |
| F8 | low | `w2/SentC1Sandbox/sandbox-probe.json` (hostname field), `w2/SentC1Sandbox.md` | live hostname (w2 seat, still writing) | **0** | none |
| F9 | low | 240 files / 1327 occurrences of an account-rooted path; top carriers are the machine-written `w1-spec.json`, `w2-spec.json`, `*-dispatch.json`, `*-results.json`, `registration.md`, `make-*.py` | account segment | **0** (by construction) | G2, inflated |
| F10 | — | 0 files | clean: no live client dump (the only class+title objects are 4 synthetic selftest fixtures in the w1 gate copy), no live monitor serial/description/make/model (4/4 unequal to this host), no live instance signature, no credential shape, no MAC, no inventory | — | G4/G5/G7/G9 = 0 |

## Gate holes proven by control (F5)

`p1-raw-dump.json` (plain JSON client list) → `R1_CLIENT_DUMP count=2`: the gate catches the raw
shape. Zero findings for: gzip container (binary skip), Python repr, TSV table, hyprctl human
block, `ps` table, `ss` without `-p`, monitor object without a serial, five whole-line paths,
synthetic MAC objects, empty-class title, 20001 objects before the dump (**silent**: `truncated`
is printed only when something already matched), >16 MiB blob (silent), symlink (scanned as its
target string). Remediations in `blind-spots.tsv`, each one line of gate code.

## Smallest remediation before the data commit

1. F1: in `w1/ExecLive/receipts/live-host.txt` keep only the seven resolver variables (P5's list)
   and `$HOME/...`; drop the seat/session/vt/state lines. Same edit for the three `w2/CritUwsm`
   env files (their owner can do it while it is still w2).
2. F3: keep cache **shape** (size, mode, `mtime=<age class>`), drop the body, the nanosecond time
   and the second hash; delete `w2/CritUwsm/cacheA-content` or reduce it to field lengths.
3. F4: write `<SIG>` in the six control copies and cut the ledger quote at
   `/run/user/<uid>/hypr/`.
4. F6/F7/F8: reduce strace to `execve("<basename>")` counts, drop the `ls -l` lines, drop the
   hostname field.
5. F2/F5/F11: state in the data commit that (a) R4's whole-line form is why a 13-path inventory
   reads clean, (b) 4 findings in the wave dir are gate self-matches, (c) `__pycache__/` drops
   files from the copy. No gate edit after data — the freeze holds.

## Reproduction

`README.md` §2 (gate over a wave-dir snapshot at `d7527d6`) and §3 (the control commit). Clone,
copy, `git add`, commit with a scratch identity, run the gate — about 3 s per run, no network, no
resolver, no compositor verb, no GUI. Scratch (`/fast/scratch/hyaku/mado-r47/SentPrivacyW2`) is
deleted at seat close; no receipt cites a scratch or `/tmp` path. No tool was installed or
upgraded (nothing needed); no package transaction was attempted.
