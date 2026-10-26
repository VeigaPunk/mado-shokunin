# SentPrivacyW2 — how the session-material sweep was run

Target: session material in the round-47 wave files **before** they are committed
(window titles, process tables, monitor serials/descriptions, home-directory listings, tokens,
and the neighbouring classes the gate does not have: environment dumps, instance signatures,
host cache records, hostname).

`LANE` below is the lane root this seat ran in; every path in `findings.md` is lane-relative.
Scratch is `$S=/fast/scratch/hyaku/mado-r47/SentPrivacyW2` and is deleted when the seat closes —
nothing in this directory cites a scratch path or a `/tmp` path as evidence.

## 1. Instruments

| # | what | command |
|---|---|---|
| 1 | gate selftest | `TMPDIR=$S python3 -I $LANE/quality/check-session-material.py --selftest` → `gate-selftest.txt` |
| 2 | gate on a snapshot of the wave dir | see §2 → `gate-run.txt` |
| 3 | class sweep (G1-G11) | `python3 -I $LANE/.ufo/waves/round-47/w1/SentPrivacy/sweep-privacy.py --worktree $LANE/.ufo/waves/round-47 --live-json $S/live-monitors.json --examples 6` → `sweep-redacted.txt` |
| 4 | live-value match (booleans) | own pass over every text blob; live values from the process environment, `hyprctl monitors -j` (read verb) and `/proc/sys/kernel/hostname` → `live-value-compare.txt` |
| 5 | class census + locators | own pass over every text blob → `ledger.tsv`, `class-summary.txt` |

`hyprctl monitors -j` is the only compositor read used; no `dispatch`, no `output`, no GUI, no
resolver run, no package transaction, nothing written outside the lane seat dir and scratch.

## 2. Gate run over the wave dir (reproducible)

```sh
S=/fast/scratch/hyaku/mado-r47/SentPrivacyW2          # any scratch dir
D=$S/gateclone
git clone -q --shared --no-checkout $LANE "$D"
test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"
git -C "$D" checkout -q --detach d7527d608ad2b2e3cc398fdde34db7947b254a1a   # the frozen rev
cp -a $LANE/.ufo/waves/round-47 "$D/.ufo/waves/"
git -C "$D" add -A .ufo/waves/round-47
git -C "$D" -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m snapshot
python3 -I $LANE/quality/check-session-material.py --repo "$D" --rev HEAD
```

The gate reads blobs from the object database, so this scores exactly what a commit would carry.
`gate-run.txt` records the clone rev, the file count, the finding lines and the summary.

## 3. Control run (the gate's blind spots)

Same clone, second commit, with a `CTL/` directory of synthetic controls (no live value in any of
them); the matrix is `gate-controls.tsv` and the raw gate output is `gate-controls-run.txt` and
`gate-controls-run2.txt`.

```sh
# in the clone: write the controls under .ufo/waves/round-47/w2/CTL/, then
git -C "$D" add .ufo/waves/round-47 && git -C "$D" -c user.name=seat \
  -c user.email=seat@scratch.invalid commit -q -m ctl
python3 -I $LANE/quality/check-session-material.py --repo "$D" --rev HEAD | grep 'CTL'
```

Expected and observed: only `p1-raw-dump.json` (a plain JSON client list) is reported
(`R1_CLIENT_DUMP count=2`). Every other control — gzip container, Python repr, TSV, human block,
`ps` table, `ss` without `-p`, monitor object without a serial, five path lines, MAC objects,
empty-class title, 20001 objects, >16 MiB, symlink — is **clean**. That is the falsification:
the gate detects the raw shape, not the classes.

## 4. Self-check

The final snapshot in §2 includes this directory. `gate-run.txt` records
`0` finding lines naming `w2/SentPrivacyW2`, so this seat adds nothing to the wave dir's
finding count. Receipts hold locators, classes, booleans and line numbers — never a value.
