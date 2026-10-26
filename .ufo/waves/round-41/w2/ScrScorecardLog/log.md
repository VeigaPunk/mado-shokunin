# Draft — LOG.md `## Round 41` block

Drafted by seat `ScrScorecardLog` (wave w2) for L1 integration. Place after the round-40 block (currently at `LOG.md:2460-2465`), replacing nothing.

---

## Round 41 — mado-globals and the focus-grab entry (2026-10-25, attempt 1)

- Freeze `60c3914` (v1 registration, C1/C2 counters, controls, base receipts, source receipts) → wave `w1` (34 seats, dispatch `cd950ec`) falsified the v1 predicates before any data — C1: 8 of 12 cheats scored TARGET_MET (live-stub bytes readable without running it, a plaintext journal copy on disk, b2 path/fingerprint escapes, clause-g `getattr`/kwargs, a child interpreter, `\w` name coincidence), 13 of 42 extra single-defect mutants survived, a FIFO journal hung, live output buffered without bound; C2: 9 of 9 forgeries admitted, 29 of 45 extra mutants survived → v2 predicates, controls (98 C1 / 67 C2) and the reference frozen at `294c6679` (`registration-v2.md`) before data.
- Data `07f2641`: `tools/mado-globals.py` (byte-identical to the v2 reference, sha256 `286c051f…`), the entry `corpus/knowledge/hyprland-focus-grab-r41.md` (Draft A with two one-id-per-line fixes), registry rows S283–S289 (+ S037 used-by), `corpus/README.md` row, lesson `corpus/lessons/round-41.md`, and the fetch receipt `fetch/xdph-installed-version.txt` (the held-row S037 receipt; M41-6 fix).
- Measurements at the data commit, recorded at `9919e16` in `receipts/`: C1 v2 `fixtures=39/39 verdict=TARGET_MET` exit 0; C2 v2 `admitted=1/1 verdict=TARGET_MET` exit 0; the superseded v1 predicates disclosed: C1 `fixtures=6/24 verdict=TARGET_MISSED` (the delivered tool is the v2 reference; contract changed), C2 `admitted=1/1`.
- Motivating evidence: the staged focus-control theme (successor to `focus-grab-protocol-live-on-host-r14.md`; base gap: `git grep -lEi 'focus_grab\|focus-grab\|focus grab'` empty at base); the w1 falsification findings above; the host receipts (Hyprland 0.56.2 `efb5099`, xdph v1.4.1); the live census reproduced by `ExecLiveHost` (2 sessions, 63 interfaces in the latest, one focus-grab advert ver 1).
- Wave facts: w1 34 seats; the orchestrator kernel restart mid-wave lost the results-JSON outputs (the seat reports under `w1/` are retained); w2 34 seats (falsify) dispatched after the data commit at `9919e16`; M41-3 (the dispatch marker is untracked again) and M41-4 (the tip axis receipt is still open) remain open.
