# R56W3ExecCrit107Build — criterion 107

## Attack and implementation

Attacked the committed QUALITY criterion 107 checker behavior at lane revision `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`. Implemented `quality/check-anchor-cover.py` in this seat's deliverable directory only. It reads the entry, registry, and named pin blobs via `git cat-file` at the selected revision; scans table rows outside fenced blocks and HTML comments for any third-cell `S` id; treats malformed pin cells as violations; rejects absent/duplicate registry IDs and invalid names; applies identifier-prefix-bounded name occurrence and locator parsing, cover checks, and pin EOF bounds; emits `ANCHOR_COVER` lines and the `CHECK107` summary; returns 0/1/2 for OK/failure/setup error. All checker writes are confined to `--work`.

## Execution evidence

GREEN command:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ExecCrit107Build/quality/check-anchor-cover.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev 0f3a54361a9824484d0801679ceb1fd8ac7c32e1 --entry corpus/knowledge/hyprland-config-autoreload-r56.md --work /fast/scratch/hyaku/mado-r56/R56W3ExecCrit107Build
```

Output: `CHECK107: rows=39 covered=39 miss=0 verdict=OK`; exit 0. Full stdout: `.../R56W3ExecCrit107Build/receipts/green.txt`.

Round-55 RED command used the same checker, repo, and work path with `--rev 63f48dc1b240b707c5ab9d634e2395ab90e1540c --entry corpus/knowledge/hyprland-keyboard-repeat-numlock-r55.md`.

Output: `ANCHOR_COVER: row=K14 sid=S318 line=280 name=ConfigValues.cpp locators=271-279;296 eof=unchecked verdict=MISS reason=no-cover`; `ANCHOR_COVER: row=K17 sid=S052 line=2741 name=wayland.xml locators=none eof=unchecked verdict=MISS reason=no-cover`; `CHECK107: rows=32 covered=25 miss=7 verdict=FAIL`; exit 1. Full stdout: `.../R56W3ExecCrit107Build/receipts/red-r55.txt`.

## Registry mutants

Built each mutant in its own scratch Git repo under `/fast/scratch/hyaku/mado-r56/R56W3ExecCrit107Build/`. Before first commit, asserted `git -C <repo> rev-parse --show-toplevel` equaled that scratch repo. Committed each with `git -C <repo> -c user.name=ctl -c user.email=ctl@ctl commit`; source entry, registry and named pin blobs were populated from the committed green revision. Ran each using:

```text
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3ExecCrit107Build/quality/check-anchor-cover.py --repo <mutant-scratch-repo> --rev HEAD --entry corpus/knowledge/hyprland-config-autoreload-r56.md --work <mutant-work-dir>
```

All seven mutations failed with rc 1 and the rows they affect:

- Widen past EOF: K03-K12 and E02; `reason=past-eof`.
- Narrow below a K row: K12; `reason=no-cover`.
- Drop NAME: K03-K12 and E02; `locators=none`, `reason=no-cover`.
- Reversed range: K12; `reason=no-cover` (reversed interval covers no line).
- Identifier-prefixed NAME: K03-K12 and E02; `locators=none`, `reason=no-cover`.
- Malformed pin cell: K01; `line=492`, `reason=malformed-pin`.
- Duplicate registry ID: K03-K12 and E02; `reason=dup-id`.

Full per-mutant stdout/rc files: `.../R56W3ExecCrit107Build/receipts/mutant-<name>.txt`; combined decisive lines and rc values: `.../R56W3ExecCrit107Build/receipts/mutants.md`.

## Findings, severity, limits

No defects found against the requested criterion. The committed round-56 entry passes the stated all-row criterion; the round-55 example and each required mutant fail as specified. No frozen claim or lane-tracked file was changed. No build, lint, formatter, or separate project test suite was run; the requested checker executions and mutant receipts were run. No blocker remains.

## Deliverables

- `.ufo/waves/round-56/w3/R56W3ExecCrit107Build/quality/check-anchor-cover.py`
- `.ufo/waves/round-56/w3/R56W3ExecCrit107Build/receipts/green.txt`
- `.ufo/waves/round-56/w3/R56W3ExecCrit107Build/receipts/red-r55.txt`
- `.ufo/waves/round-56/w3/R56W3ExecCrit107Build/receipts/mutants.md`
- `.ufo/waves/round-56/w3/R56W3ExecCrit107Build/receipts/mutant-*.txt` (seven individual rc/stdout receipts)
