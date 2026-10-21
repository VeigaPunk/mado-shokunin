# FalsifyC104 — C1 case CX4NonlocalMutation (round-22 wave-2, author-lane advisory)

Seat: MadoR22.FalsifyC104 · Date: 2026-10-21 · Delivered revision: `71228fd582d6d9338d7916cc64e69bd4c2e928b5` ("round-22: distinguish fixture inventory names from snapshot API paths"), confirmed in jj ancestry; working copy is an empty child commit `34333a37e143`. Advisory only; no admission granted by this report.

## Verdict: AGREE (oracle green stands; independent semantic reasoning concurs with the sealed classification)

## Measurement (single authorized scanner child, 384MiB/15s caps, inert parse only)

- Command: `python3 -I .ufo/waves/round-22/oracle/measure.py --tool tools/mado-tripwire.py --case CX4NonlocalMutation`
- Runner exit `0`, status `complete`, totals pass 1/1. Scanner child exit `0`, stderr empty.
- Receipts (own dir): `.ufo/waves/round-22/w2/receipts/FalsifyC104/{result.json,argv.txt,exit.txt,stdout.txt,stderr.txt,pre.sha256,post.sha256}`. `diff pre.sha256 post.sha256` → identical, no drift.
- Hashes before == after: tool `36fdc459…badce` (matches fixed identity), fixture `1d0e790d…69e2` (matches sealed `input_sha256`), runner measure.py `41b021bb…28c7`, expected.json `b5cd4cf3…4357` (matches pin file and fixed identity). Runner-verified `integrity_before == integrity_after`; population sha `04616857…86ad`. Audit tool `277eced2…fca` also matches its fixed identity (untouched).

## Sealed truth (expected.json, group proposal; proposal source `d82343f9…e06` preserved, CriticScope CX4)

`expected_kind=uncertain`, `want=[]`, `require_signal=true`, `accept_exact_want=[{host_mutation, "pacman -S r22-cx4-nonlocal", observed}]`, `forbid_commands_any_tier=["pacman -Q r22-cx4-nonlocal"]`, `forbid_observed_commands=["pacman -Q r22-cx4-nonlocal"]`. Sealed rationale: nonlocal cell rebinding through a sibling inner call is filed uncertain (outside CaptureLocalReassign / prefix-replay forms); the `-Q` factory argument is stale and never runs, forbidden at every tier; uncertainty with an explicit signal is a valid outcome.

## Independent semantics (my reasoning, not derived from green)

In the single eval cell, `make(argv)` closes `run` over `argv`'s cell; `retarget` declares `nonlocal argv`, so `argv = new` rebinds `make`'s cell; `retarget(["pacman","-S","r22-cx4-nonlocal"])` executes inside `make` before `return run`. Hence `runner()` invokes `run` reading the cell at call time: the only dynamically executed host command is `pacman -S r22-cx4-nonlocal`. The `-Q` binding never reaches `subprocess.run`. This matches the sealed rationale; the case is a deliberate boundary fixture, not an exact-form claim.

## Observed tool behavior (actual)

- `findings=[]`, `observed_findings=0`, `lead_findings=0` — zero rows at every tier; stale `-Q` absent from observed, lead, and all counters.
- File row: `eval_calls=1`, `eval_unparsed=0`, `unparsed_spawns=1`, `sha256=1d0e790d…` (identity matches sealed input; path resolves to the fixture).
- Banner `MADO_TRIPWIRE: clean`, structured exit 0. Oracle pass branch: not `accept_exact_want` (rows empty); it passes via `require_signal` — oracle computes `unparsed = eval_unparsed + unparsed_spawns = 1 > 0` as the uncertainty signal, no observed rows, no forbidden hits, `reasons=[]`.

## Falsification axes — none fires

- **False observed/lead argv**: none; the stale `-Q` command appears nowhere. ✓
- **Lost true command**: the exact `-S` row is not printed, but the sealed truth files this case uncertain precisely because nonlocal sibling-call rebinding is outside the supported exact forms (supported-forms.md: "later nonlocal cell mutation … may prevent exact static reconstruction … Boundary fixtures may require uncertainty/no-stale-observation"). `accept_exact_want` is an optional alternative pass path, not a demand. ✓
- **Wrong identity**: no invented rows; scanner-reported digest and path match the sealed fixture exactly. ✓
- **Lifetime**: tool asserts nothing about the cell/rebinding; it declines (unparsed spawn) rather than claiming a wrong frame. No false lifetime claim to falsify. ✓
- **Conditional target**: not exercised — single unconditional `runner()` call in one cell. n/a.
- **Parsed-clean ambiguity**: the only residual concern, resolved by the tool's own frozen contract (docstring lines 32–37): "clean means no finding in the covered forms. It never means 'no host command ran': non-literal spawn arguments (counted as unparsed_spawns) … are not analysed." The structured payload retains the machine-readable uncertainty (`unparsed_spawns=1`), which is precisely what the oracle consumes; `eval_unparsed=0` coherently reflects that the eval cell parsed while its spawn argument is non-literal. The banner is form-scoped, not a false cleanliness claim. ✓

## Scope and residual risk

- This green is **not** semantics proof that the tool reconstructed the nonlocal rebinding — it did not; it truthfully emitted "one spawn whose argv I cannot statically resolve" and invented nothing. My agreement is that this is the correct sealed classification for THIS fixture under the pre-seal boundary rules.
- One-case scope: the runner validated full population integrity (52 raw / 50 eligible proposals + 7 supplemental originals, sealed proposal digests re-verified) but executed only CX4; no verdict is expressed on the other 56 cases, the 175-case historical floor, the 1356-fixture removal comparison, or C2.
- `accept_exact_want` pass path is untested by this case (the tool took the signal path). Whether the tool could ever produce the exact observed `-S` row is unmeasured here and unassigned.
- No new source-shaped probes run (none assigned); r21 red receipts and streak untouched; no install performed; no production/fixture edits (reads + own receipts + this report only).
