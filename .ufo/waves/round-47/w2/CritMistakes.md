# CritMistakes — w2 FALSIFY report (round 47)

Seat: CritMistakes · lane: mado-shokunin · wave w2 (FALSIFY, policy v1) · 2026-10-26 · tip `9bddd6ac`.
Full findings and receipts: `.ufo/waves/round-47/w2/CritMistakes/findings.md` (+ `receipts/`).

## Verdict

All six mined rows (M47-1..M47-6) are **shown able to fail** (red case exists; most also green) and their
classes are right. Two corrections: M47-6 should be double-tagged `landing`/`survivor` (M46-13's fix landed
on only 2 of 3 counters and the pyc gap recurs); M47-3's fix needs an extra step — the gate at HEAD already
flags the wave's own drafted marker material (`w1/ExecSessionMarker/check-session-material.py`, R3
serial+ident), so a naive "install marker → findings=0" cannot reach 0 while those files are committed.
The four new mistakes are added (N1-N4): seat runaway write (class `scope`, no instrument measured scratch
sizes — current scratch already has one w2 seat > 2G), host cache rewrite (SentHost F2b, restored
byte-identically), misrooted SentHost dir (existed untracked at `.ufo/waves/round-47/SentHost/`, rev
`c24adef2`, footprint receipt; since moved to `w1/SentHost`), and the w1 C2 counter coupling (draft ran
`tools/mado-terminal.py`; L1's committed clause f binds `resolver_sha256=` and never runs our tool — verified
in code and by the entry-only POS control).

Proposed criteria 91-92 are runnable with red+green demonstrated; 93-95 are red-demonstrated, green pending
the fix landing. Criterion 94 has no shipped script and needs one L1 convention decision.

## Key evidence (receipts in seat dir)

- check91: red DIFFER + green AGREE re-run (`verify-check91.txt`).
- check92: at HEAD `ExecStofOracle` is clean (L1 R2 removed the 3,282,451 B file, digest committed) —
  `verify-check92.txt`, `verify-footprint.txt`.
- session-material gate: `findings=115` rc=1 at `c24adef2`; `findings=118` rc=1 at HEAD (`verify-session-gate.txt`).
- C2 decoupling: draft lines `w1/ExecCounterC2/c2-r47-terminal-entry.py:73,116,629-633` vs committed
  `quality/counters/c2-r47-terminal-entry.py:68-73` (no `TOOL` extraction); POS control `ctl-pos.txt` `admitted=1/1`.
- Host cache: `w1/SentHost/report.md` F2b + receipts `host-cache-observed.txt`, `cache-restored.txt` (190 B,
  sha256 `f497ed05…`, mtime 17:42:25 restored).
- Scratch sizes: `du -sh /fast/scratch/hyaku/mado-r47/*` at 19:39 — `CritC2Forgery` 2.5G > 2G (`verify-scratch-sizes.txt`).

## Safety

No host writes, no resolver execution, no mutating git/jj; scratch `/fast/scratch/hyaku/mado-r47/CritMistakes`
created and deleted; no installs needed (no tool installed).
