# RevGateV3 — round-50 w1: attack of the session-material gate v3 (carried round-49 w2 item)

Verdict: **the candidate passes the item's checks; 1 freeze-time obligation, no candidate defect found.**
Artifact attacked: `.ufo/waves/round-50/w1/ExecGateV3/check-session-material.py`, sha256
`ffdc9d62c387050e016cf9d0eaacbf87f37d6647021cbd2c492eb6328dddbb61`, 2149 lines — **byte-identical to the
round-49 draft** `.ufo/waves/round-49/w1/ExecSessionShapes/check-session-material.py` (diff = 0 lines), so both
targets collapse into one artifact; all round-49 ExecSessionShapes receipts apply to it unchanged. Installed v2 at
base `8ae47b957034ae21012bbf09173cca2c48be345e` measured sha256 `82c9053ae2e8b7db2fb8c0e195c32b8b151a593cf9412dcae3589427ac2dfa6f`
= the sha claims.md names. All runs in scratch (`/fast/scratch/hyaku/mado-r50/RevGateV3/`, removed after receipts
were copied), sandboxed HOME/XDG_*/TMPDIR, PATH restricted to git+python3 (no hyprctl reachable); no pacman, no
host mutation; no tools installed.

## Checks the item names — all pass, from live runs

1. **Selftest.** Candidate `--selftest --verbose`: `passed=94/94 failed=0`, rc 0 (receipts/selftest-v3-verbose.txt).
   Installed v2 at base: `passed=69/69 failed=0`, rc 0 (receipts/selftest-v2-verbose.txt).
2. **Every v2 selftest case still present.** Case names extracted from my own runs: v2=69 distinct, v3=94 distinct,
   `missing_in_v3=0` (receipts/cases-v2.txt, cases-v3.txt). Reproduces the seat's receipts/case-names.txt (69/94/0).
3. **New rules fire on red, stay silent on green — on MY OWN nonce fixtures** (not the seat's; builder saved as
   receipts/nonce-fixture-builder.py). One committed fixture repo, 13 files, synthetic identities only:
   - v2 `--scope all`: rc=0, findings=0 — blind to every red class (receipts/nonce-v2-all.txt); reproduces
     claims.md's "v2 reports 0 findings" with independent shapes.
   - v3 `--scope all --account <nonce>`: rc=1, 8 findings, exactly the reds:
     R7 prefix×3 / header×1 / diag×1 / row×1, R8 rows on an owner-matching row AND on two group-only rows
     (`root <acct>` and `<acct> root`), R9 fields=3, plus the structural form in `docs/` **outside `.ufo/`**.
     Every green file clean: `~`/`$HOME` prose, paths quoted in prose, numeric-id `ls -ln` rows, indented usage
     text, one-field doc line, other-owner `ls -l` (receipts/nonce-v3-all-account.txt).
   - v3 `--scope ufo`: the outside-`.ufo/` red disappears (files 13→12, 5 findings) — scope behaviour correct
     (receipts/nonce-v3-ufo.txt). v3's default scope is `all`; v2's default is `ufo` (v2 lane scan without --scope:
     files=22998 = the ufo count).
   - No values leak: grep for both nonce identities across all four gate outputs = 0 hits.
4. **Delta vs base is what the registry row says.** claims.md C2 (registration.md does not exist yet; freeze after
   w1). At base, same tree, same env: v2-all findings=121, v3-all findings=228 — delta is **exactly**
   R7=49 + R8=54 + R9=4; old-rule (path,rule) pairs added/removed by v3: **0 / 0**; every new-rule file sits under
   `.ufo/waves/` (94 files). All four R7 forms occur in the base findings (prefix/header/diag/row all non-zero in
   the per-file detail breakdown). ufo-scoped delta likewise 113→220 = the same +107.
5. **No false positives on `~`/`$HOME` prose.** 2646 tracked base files quote `~/` or `$HOME`; exactly 7 of them
   also carry new-rule findings, and shape-only classification (gate's own regexes, values masked) shows all 7 are
   genuine structural shapes, none flagged for the tilde form: an `ls -l` capture with invoking-account-owned rows
   (R8, round-35 scratch-evidence), a grep-located home path in a registry capture (R7, round-35), three
   grep-located lane paths in a checks receipt (R7, round-46), unindented cache-record field lines with trivial
   values (R9, round-47 live-print), and three byte-equal `xkbcli compile-keymap` captures with 9 grep-located
   `input.conf` lines + 2 diagnostic lines each (R7, round-48 ×3). The other 2639 tilde-quoting files carry zero
   new-rule findings.

## Findings by severity

- **F1 [medium — freeze-time obligation, not a candidate bug]** Installing the candidate *invalidates the 3
  existing `kind=gate-copy` waivers*: on a scratch overlay commit (base tree + candidate as
  `quality/check-session-material.py`) the gate rejects them as `gate-source-mismatch` — waived drops 52/48 →
  49/47 and findings rise 228 → 231 (receipts/overlay-v3-all.txt vs base-scan-v3-all.txt). This is the tamper
  protection working as designed; the L1 must refresh the gate-copy row in `quality/session-material-waivers.txt`
  in the freeze commit or the round-50 freeze reports 3 findings v2 did not.
- **F2 [low — latent silent-miss class]** `decode()` truncates any blob at MAX_TEXT=16 MiB with no note; content
  past the cut is never scanned. Measured: a 16,777,281-byte fixture with a structural form past 16 MiB → rc=0,
  findings=0 (receipts/nonce-v3-trunc.txt). Latent only: the largest tracked base blob is 4,207,542 B, 0 files over
  the limit. A one-line "truncated" note in emit() would close the silence.
- **F3 [low — measured R7 evasion classes]** Four red shapes score 0 findings (receipts/nonce-v3-probe.txt):
  grep-located path containing a space; diagnostic path in single quotes; path containing `:` before the `:line:`
  suffix; quoted home path behind a capitalized program prefix (`Git:`). None belongs to the frozen green set —
  they are red shapes the four R7 forms do not cover. Candidate defects? No (the frozen shape set is the four
  forms), but PRED-C2-r50 fixture design should not present them as covered.
- **F4 [info]** R8 keys on the invoking account (or `--account`); with no resolvable account it is inert with a
  stderr note. A counter running under a different uid must pass `--account` or it silently loses the 54 base R8
  findings.
- **F5 [info]** R9 fires on shape alone: round-47 `ScrSkill/live-print.txt` goes red on unindented
  `--working-directory=/tmp`-class lines with trivial values. In-band by the frozen shape set; disposition is L1's
  (a waiver would be refused — `/tmp` fails the W4 home-user namespace).
- **F6 [info]** v2's CLI has no `--account` (argparse rc=2) — v3-only flag; wrappers must not be shared between
  versions.

## Verified-good (host guard + waiver machinery)

Selftest under fake HOME/XDG_*, PATH without hyprctl: 94/94 and **0 files written** under the fake home/cache/config
(it never touches host serials or the real home; fixture commits use `-c user.name=selftest -c user.email=…` and
assert fixture toplevel). Output surface is value-free by construction (emit prints counts, key *names*, form
counts, and masks only). Waiver chain is strict: sidecar marker + registry row + sha equality + rule-list equality +
kind equality + W4 reserved namespaces; serial rules (R5/R6) never waivable; 24 waiver selftest cases pass.

## Residual risk / gaps

I did not run the seat's `fixture_e2e.py`/`mutate.py` (MutGateV3's lane) or fuzz the JSON rules R1–R3 beyond the
selftest; `--serial-from-host` is unexercised (hyprctl monitors is not on this seat's allowed-read list — the gate's
host path rests on selftest fixtures + code read only). Delta is measured against base `8ae47b95`, not a future
freeze commit; F1 tells the freeze what will move.

## Evidence index (all under my seat dir, all `test -f` verified)

`.ufo/waves/round-50/w1/RevGateV3/receipts/`: selftest-v2-verbose.txt, selftest-v3-verbose.txt, cases-v2.txt,
cases-v3.txt, base-scan-v2-all.txt, base-scan-v2-ufo.txt, base-scan-v3-all.txt, base-scan-v3-ufo.txt,
overlay-v3-all.txt, nonce-v2-all.txt, nonce-v3-all.txt, nonce-v3-ufo.txt, nonce-v3-probe.txt,
nonce-v3-all-account.txt, nonce-v2-all-account.txt, nonce-v3-trunc.txt, nonce-fixture-builder.py.
Lane-relative paths only; no account name, no raw binds/serials/home values anywhere in this report or the receipts.
