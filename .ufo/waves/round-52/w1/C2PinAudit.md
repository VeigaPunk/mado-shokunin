# C2PinAudit — candidate source pin/proposition matrix audit

Verdict: the candidate matrix (seat C2EntryDraft, slug `hyprland-synthetic-key-dispatch-r52`) is mechanically sound at the audited revision — 17/17 proposition quotes verbatim at their anchors, ≤25 words, all four pins byte-identical across the round-52 re-fetch and the committed round-51 manifest, and every support/rationale line cite I checked resolves to true bytes. One wording-level unsupported fact remains (P12 / md-P16 delivery-destination phrasing), plus admission steps that are correctly still open. No claim or predicate was edited by this seat.

## Deliverables

- `.ufo/waves/round-52/w1/C2PinAudit.md` (this report)
- `.ufo/waves/round-52/w1/C2PinAudit/pin-proposition-audit.md` (detailed per-proposition audit: digests, quote/anchor table, support-cite verification, findings)
- `.ufo/waves/round-52/w1/C2PinAudit/pin-audit-receipt.txt` (independent checker receipt, first revision, r51 pins)
- `.ufo/waves/round-52/w1/C2PinAudit/pin-audit-receipt-r52.txt` (independent checker receipt, current TSV vs round-52 fetch: FAIL=0 rows=17)
- `.ufo/waves/round-52/w1/C2PinAudit/r52-fetch-digests.txt` (my recomputed sha256 of the round-52 fetch payloads)
- `.ufo/waves/round-52/w1/C2PinAudit/cited-lines.txt` (pin-byte excerpts for every cited line range)

## What was verified (independent of the draft's own checker)

- **Quotes/anchors/lengths:** all 17 TSV propositions P01–P17 pass: whitespace-collapsed verbatim in the cited anchor of the round-52 fetch bytes, ≤25 whitespace words (max 22, P09). The four `source:`-line quotes: S370 exact at DispatcherTranslator.cpp:592, S371 exact at ConfigActions.cpp:1554; S372/S373 are collapsed-whitespace prefixes of hpp:114 / KeybindManager.cpp:221 (correct under the draft's stated rule). Draft census (17 propositions, 0 over 25 words, 0 not found) reproduced.
- **Pin identity:** all four round-52 re-fetched files sha256-equal to `round-51/fetch/SHA256SUMS` and to the seat's `fetch/verify.txt`; URLs pinned at immutable commit `efb50993780079460b0cbed1363e2166a2de1d9f`. The "opened this round" grounding gap in the first revision (r51 pins only) is materially closed by this re-fetch; registry admission (S370–S373 appended with opened 2026-10-27) remains the data seat's step — verified absent from `corpus/SOURCES.md`, which ends at S369.
- **Support claims:** every rationale/chain/State-claims/OBS line cite verified in bytes, including :600 init, :624 restore before the single exit, :559-560/:576 cache miss-guard/hit path, :561-571 no-break scan, CA :1465-1522 (last-event check contrast), :1534/:1537-1552/:1554/:1556-1569/:1576/:1578-1579/:1581-1596, twin :1601-1616 (held), hpp :36/:62-64/:114-117, KeybindManager.cpp :221-242, hpp :149, HyprCtl.cpp :1151, plus the recon-note cites (DT :4/:66/:73 Executor; KM :643/:844-851 inhibit gate) and held cross-refs (bind-table-r25:42, S162, r51 :197-198 verbatim, wiki-gap 0/0/0).

## Findings

1. **[Low] Unsupported-fact wording:** P12 ("An empty third field means the focused surface") and the md's P16 ("delivers to the current focus") assert a delivery destination no cited pin establishes; the pins license empty→nullptr and no focus move/restore (verified). The draft's own Limits exclude the receiving client, and the TSV P16 wording is already the licensed form. Align P12/P16-md before landing. Sole surviving defect from this audit.
2. **[Info] Registry collisions:** S370≡S365, S371≡S367, S373≡S364 (same URL+commit); S372 is the only new URL (hpp denied a row in r51 under rule 4). The cited regions are new relative to S365's r51 anchors — the distinct-scope case QUALITY.md:34 (rule 17) sends to explicit review; data seat must record it. RegistryContract independently lists the same collisions.
3. **[Info] Quote uniqueness:** P16's quote occurs 28× in ConfigActions.cpp; the anchor disambiguates. Counter/truth-sampler must locate by anchor, not by quote string.
4. **[Info] `KeybindManager.hpp:149` (OBS cite) was not re-fetched in round 52**; its cite rests on the r51 pin. Harmless for an unrowed observation; add a pin-path qualifier when landing.
5. **[Revision note, honesty]** The first revision I read (16 mapped propositions vs TSV 18, two chain claims unmapped in the md table, census "16", no round-52 fetch) had real matrix defects; all were fixed by the seat mid-audit (17 propositions, unified table, `fetch/` + verify.txt). Findings 1–4 are what survives that revision. Both receipts are kept.

## Residual risk and verification gaps

Semantic entailment and source-truth sampling are out of scope here by the frozen claim (independent non-author reviewer); this audit does not make them true. Counter behavior is untested by this seat. I did not fetch any URL myself; identity rests on two local digests agreeing plus the immutable commit recorded in each URL. The draft was still being edited during the audit; the audited snapshot is described at the top of `pin-proposition-audit.md` — re-run the receipt script if the table changes again.

## Evidence and limitations

- Frozen contract: `claims-frozen.md`, `registration.md` (C2 predicate, lines 12–15).
- Audited candidate: `.ufo/waves/round-52/w1/C2EntryDraft/{entry-draft.md,proposition-map.tsv,quotes-check.txt,fetch/,check-quotes.py}`.
- Pin ground: `.ufo/waves/round-51/fetch/` (+`SHA256SUMS`), `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md:195-200`, `corpus/knowledge/bind-table-r25.md:42`, `corpus/SOURCES.md` (S162, S364-S369, no S370+), `corpus/QUALITY.md:34`.
- All commands were local reads/grep/sha256/python on already-local bytes; no install, no package query, no live read/probe/screenshot/producer execution, no network fetch by this seat, no git/jj mutation, no tracked-file writes outside this seat dir and report. Scratch `/fast/scratch/hyaku/mado-r52/C2PinAudit/` cleaned on exit; receipt copies live in the seat dir. Disk guard: 600G free before work, no ENOSPC.
- No report is a vote; nothing here scores either claim. Attacks name their item: P12/md-P16 wording; S370-S373 admission preconditions; P16 anchor-vs-quote uniqueness.

## Report

- `.ufo/waves/round-52/w1/C2PinAudit.md`
