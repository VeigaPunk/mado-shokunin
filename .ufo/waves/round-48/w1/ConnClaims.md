# ConnClaims — pre-freeze checklist (round 48, w1) — findings

Full report: `.ufo/waves/round-48/w1/ConnClaims/report.md`. This is the scoped summary.

## What the freeze commit must contain
- `registration.md` v1: base `579f694b…`; claims C1 (warm-cache) / C2 (xkb-keymap-compile-r48); lowest-axis rule (quality trend behind); premise corrections from w1; routed-items section.
- Counters: `quality/counters/c1-r48-terminal-cache.py` (clauses a/s/f/g/x/i/r; explain compares id+path+**cmd** and reports `cache=<absent|hit|stale|invalid|disabled>`; HOME unset = pin behaviour; sandbox clause = enumerated mounts + "no host path outside it is bound"; `mkdtemp`+`O_NOFOLLOW` observed-capture, OSError ⇒ clause-x fail, never abort) and `quality/counters/c2-r48-xkb-entry.py` (entry/provenance/pins/quotes/steps/live xkbcli receipt/README row/held rows S318-S319 cited, never re-claimed/census terms).
- Fixtures (schema v2 final): round-47 schema + `mtime`, `prime`, `after`, `cache`; `expect` always from 3 identical pin runs; classes for warm-hit (warm ≠ cold), invalidation (mtime/size/name/dir/desktop/exec[0]/hash), malformed (no terminator, line-50 limit, bad hash), disabled (`XTE_CACHE_ENABLED=false`, `/disable_cache`), M47-10 H1/H2 (non-regular `*.desktop` paths incl. FIFO; option-like `Exec[0]`/`TryExec`), D3 ordered two-candidates-in-one-dir.
- Pins under `fetch/` (sha256 + tag/commit URL); reference `l1-draft/mado-terminal.py` (extended) — **not yet drafted** (only `lsemu.py` exists); controls battery incl. warm-cache cheats (QUALITY 86/87); base receipts at `579f694b` (c1-before, c2-before, c2-ground, census-before, axis, fetch-sha256, h12-style cache parity); session-material marker installed with clean-state receipt (QUALITY 93).

## Separability (must land with the freeze)
- C1 reads only `tools/mado-terminal.py`; C2 reads only entry/rows/README/pins/receipts; entry-only tree admitted, tool-only tree misses (shown both ways by w2). Counter imports pinned model from `--work` copy, never from the scored tree (QUALITY 95); fixture builder runs the pin, never the tool.

## Recurring closure defects — key fixes
- D1: freeze embeds the contract text; landed tool docstring must byte-equal the reference at data commit; HOME unset modelled as pin.
- D2: report numbers emitted by instruments at the tip revision; receipt committed beside each claim.
- D3: every w2 seat finding routed in the lesson; ordered-dir fixtures in schema v2.
- D4: erratum line + locator-verification script before data; locators computed, never typed.
- M47-10 / CritC1Explain / SentC1Sandbox F1-F4: covered by the counter clauses above.
- R4b: append `block-fixed.md`; re-run frozen round-45 counters post-append (must stay TARGET_MET).

## Fresh w1 risks (fix before freeze)
- `ExecAxisBase/receipts/c1-r47-base.txt` is empty (needs a real before-run).
- `ExecD2Receipt` session-material receipt ran with a fleet-root-relative path (rc=2); use absolute lane path.
- `l1-draft/` has no extended reference tool yet.
