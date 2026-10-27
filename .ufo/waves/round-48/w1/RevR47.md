# RevR47 — review of the round-47 closure routing (round-48 w1)

Status: COMPLETE 2026-10-26. Full review with evidence: `.ufo/waves/round-48/w1/RevR47/review.md`
(probe outputs in `RevR47/probes/`).

## Verdicts on the routed items (base 579f694b)
- D1 CONFIRMED (frozen docstring `.ufo/waves/round-47/l1-draft/mado-terminal.py@d7527d608ad2…` :84-87
  lacks HOME unset / FIFO / symlink loops; landed `tools/mado-terminal.py@d40189c9` :85-88, :410,
  :526-529 add them; registration.md:30-31 freezes the l1-draft docstring). Unfixed at base; routed.
- D2 CONFIRMED (fleet report 6fd13912 `.ufo/reports/round-47/mado.md:104`; no `findings=128` in the
  lane at d40189c9, rc 1; committed ExecSessionMarker receipts hold 115/136/139, never 128). Routed.
- D3 CONFIRMED (`w2/ExecC1Determinism.md:9-11`; committed mutant receipts 190/190+190/190 with
  generated 149/150 @nonce 4242 and 146/150 @4747; no readdir mention in lesson or report at base).
  Routed.
- D4 CONFIRMED (entry :95 cites terminal-route-r17.md:150-151; text at :149-150; byte-identical at
  579f694b; the entry's other r17 locators :76/:88 are correct). Routed.
- Carried: R3 armed (seat + Mut/RevSessionMarker present), R4b matches H1/H2/H3 of ExecErrataR45
  (block-fixed.md keeps PRED-C2-r45 MET), M47-10 = the 9 MutC1Fixtures blind spots, CritC1Explain
  and SentC1Sandbox F1-F4 verified against their committed reports. All covered by round-48 claims.

## Defects not in the closure (new)
1. MEDIUM — D1's routed fix wording drops the pin's condition: "HOME unset ⇒ pin exit 1, empty
   stdout" holds only when any of XDG_CACHE_HOME/XDG_CONFIG_HOME/XDG_DATA_HOME is unset (measured:
   `env -i` → rc 1 at :148; cache var unset → rc 1 at :172; all three set with HOME unset → rc 0,
   stdout `alacritty`). This host's session sets all three, and the r47 tool refuses HOME-unset
   unconditionally (exit 2, :410). Freeze must state the condition or C1-r48 re-introduces the
   divergence.
2. MEDIUM (freeze-time) — the declared fixture schema v2 (mtime/prime/after/cache) still cannot
   express three routed kill classes: MutC1Fixtures #7 (PATH field missing), #8 (file mode missing),
   ExecC1Diff H1 (non-regular shadow paths). New counter's clause x must compare `cmd=` AND `cache=`;
   SentC1Sandbox F4 remediation must carry into it; F1-F3 clause-i wording restated before freeze.
3. LOW — spotcheck §6.1 cites the frozen reference as `l1-draft/mado-terminal.py@d7527d60`; the
   committed path is `.ufo/waves/round-47/l1-draft/mado-terminal.py`.

## Also verified
Closure commit = spotcheck lesson only (+146/0); knowledge 63→64; S-rows 262→276 (top S339, no
S340) at base; pin sha256 89f2be9a… / 1499 lines / 23 functions exact; landed tool bytes =
d40189c9 blob (b84d5c4f…); H1 fix live-reproduced at tip (pin and tool both rc=1, empty stdout on
the directory-shadow tree). No lane counter executed; resolver only with `--print-*` + scratch
cache; no tools installed; scratch deleted after copying probe outputs into the seat dir.
