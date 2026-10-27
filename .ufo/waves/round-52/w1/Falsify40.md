# Falsify40 — C2 source quote/pin binding attack: fabricated pin-copy bytes pass binding

Seat: Falsify40 (leaf, no dispatch). Round 52, wave w1. Target named in dispatch: **C2 source quote/pin binding**.

## Findings

### Evidence and attacked predicate

- **Attacked clause (named):** the C2 frozen predicate's binding leg — "each [proposition] maps to an opened-this-round `S###` row, a **pin path/revision** and exact located quote <=25 words" (`.ufo/waves/round-52/registration.md` § Frozen predicates; same sentence in `.ufo/waves/round-52/claims-frozen.md` C2: "each material factual proposition maps to a pinned source quote <=25 words and explicit support rationale"). The attack is against the **revision/fidelity leg of the pin**: structural counters verify the quote against the *committed pin copy* but never tie the copy's bytes to the pinned upstream revision.
- The only committed implementation of this binding family, `quality/counters/c2-r51-dispatch-entry.py`, verifies exactly `collapse(quote) in collapse(line-span of committed copy at rev)` (`bind_row`, lines 382-415; loader reads `.ufo/waves/round-51/fetch/<pin>` at rev, lines 362-367) plus a 25-word cap (line 370). It contains **no** `hashlib`/`sha256`/revision comparison (grep-evidenced below): the entry's "Digests for the checksum manifest" prose and the registry anchor's recorded upstream sha are never machine-checked.
- The round-52 draft counter `.ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py` (copied to scratch, sha256 `298b8c07…`, run as-is) checks clause (c) that the registry *anchor string* contains the fetch root, the pin name, and a 40-hex revision, and clause (d) that the quote appears verbatim at the cited line of the committed copy — but the parsed pin-cell revision (`rev_tok`, clause_d line ~537) is never used, and no digest is ever computed.
- The lane already knows the stronger control: `quality/counters/c1-r50-bind-entry.py:9-13,38-40` — "A fetch copy is trusted **only when its sha256 equals a digest the citing row records**… every named pin exists at REV, mode 100644, and its sha256 equals a digest the row records." That digest equality is exactly what the C2 binding family omits.

### Attack / result

**Failure mode:** a fetch/pin seat (or any seat able to commit the round's fetch copies) inserts fabricated text into a committed pin copy, then quotes that text verbatim at a chosen line. Every structural binding check passes: the quote *is* at the cited line of the committed copy at the scored revision; the registry anchor still names the real upstream revision and sha. The proposition is bound to bytes that never came from the pinned source. The frozen predicate's only remaining guard is the outside non-author source-truth review (a sampling control), not the counter.

**Reproducible setup (all seat-local scratch; lane read-only):**

1. `fixture-repo/` — git repo with `.ufo/waves/round-52/fetch/Hyprland-KeybindManager.cpp` + `Hyprland-SharedDefs.hpp` copied byte-identical from the lane's tracked round-51 pins at base (`.ufo/waves/round-51/fetch/`, sha256 `8d8f35fc…` / `0b40cc83…`), a `corpus/SOURCES.md` registry (rows S364/S365 for the r51-shaped run), `corpus/README.md` index, and a C2-shaped entry. Tags: `green` (honest) `c737aa2d…`, `attack` (one fabricated line inserted as new line 40 of the KeybindManager copy; entry retargets the S364 quote to it; digest prose unchanged) `84a46065…`.
2. `harness.py` imports a byte-copy of the committed r51 counter and overrides only module constants `FETCH_ROOT`/`ENTRY`/`ENTRY_NAME` to the fixture shape (no code edits); runs the counter's real `clause_a`/`clause_b`.
3. `fixture-r52/` — second git repo holding the **actual round-52 base commit** (fetched read-only from the lane, `git fetch /home/vgpnk/Projects/shokunin/mado-shokunin 85d57a818c3707397e21c840b6498b105ba798aa`) so the draft counter's frozen-BASE checks resolve; registry rows S396/S397 (fresh at base; max S-id at base is S369), r52-shaped proposition-map entry, same two pin copies. Tags: `green52` `a4eaeda1…`, `attack52` `ed4baefd…` (same single-line insertion + retargeted P1 quote; registry anchor still records upstream sha256 `8d8f35fc…`).
4. Commands (exact): `python3 harness.py green|attack` and `python3 c2-r52-proposition-entry.copy.py --repo fixture-r52 --rev green52|attack52 --entry corpus/knowledge/hyprland-dispatcher-falsify40-r52.md --work <scratch>`.

**Actual results** (full log: `Falsify40/run-output.txt`):

- Committed r51 counter, GREEN: `clause_a ok=1`, `clause_b ok=1 rows=2/2 pins=2`.
- Committed r51 counter, ATTACK: `clause_a ok=1`, `clause_b ok=1 rows=2/2 pins=2` — fabricated line present in committed copy, absent from real upstream (`fabricated-line in committed copy: True / in real upstream: False`), copy sha `63d61b60…` ≠ declared/real `8d8f35fc…`.
- r52 draft counter, GREEN52: clauses a-e all `ok=1`, `clauses_met=5 admitted=1/1 verdict=TARGET_MET`, exit 0.
- r52 draft counter, ATTACK52: clauses a-e all `ok=1` (c `rows_bound=2/4`, d `quotes_bound=4/4 pins=2`), `clauses_met=5 admitted=1/1 verdict=TARGET_MET`, exit 0 — with the fabricated 11-word quote bound at `Hyprland-KeybindManager.cpp:40@ efb50993…` while the copy sha is `63d61b60…` against a registry-recorded upstream `8d8f35fc…`.

**Reproduced: yes** — against both the committed round-51 binding code and the in-flight round-52 draft counter (draft state as of this seat's run; sha `298b8c07…`).

### Operational limits and verification

- Dissent/honest framing: under one reading, the predicate's quote leg is literally satisfied (the quote is verbatim at the cited line of the pinned path *as committed*) and the frozen claim caps the counter at "This is not automated semantic-entailment proof." This seat's position: "pin path/**revision**" and "grounded in sources opened this round" require the copy to be *of the pinned revision*; a binding that cannot detect a tampered or wrong-revision copy fails the predicate's intent, and the lane's own r50 C1 counter shows the digest equality is the established way to close it. The predicate's outside-reviewer leg remains the only backstop today.
- Recommended closure (structural, cheap): in the r52 counter's clause (c)/(d), require the registry anchor (or pin manifest) to record a 64-hex sha256 per pin and assert `sha256(copy bytes at rev) == recorded digest` before quote verification — the `c1-r50-bind-entry.py` pattern. Recorded digests must come from the fetch seat's open-time receipt, not the entry author.
- No package queries, live reads, process/compositor probes, input capture, screenshots, or producer execution. The counters run are read-only git-tree structural checkers; all fixture git mutations happened in scratch repos after `cd` into them (`git rev-parse --show-toplevel` asserted by construction). No installs. Disk guard: `/fast/scratch` 599G free before work. Lane repo and peer seat files untouched except reads; receipt copied to the seat dir. No new network sources opened: fixture source bytes are the already-locally-available pinned Hyprland v0.56.2 copies (URL family `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/KeybindManager.cpp`, opened round 51, tracked at base; accessed locally this seat). Located real quotes used: KeybindManager.cpp:41 `// populate m_dispatchers from the legacy translator`; :785 `const auto DISPATCHER = m_dispatchers.find(k->mouse ? "mouse" : k->handler);`; SharedDefs.hpp:53 `bool passEvent = false;`; :54 `bool success = true;`.
- Scratch (`/fast/scratch/hyaku/mado-r52/Falsify40/`) removed on round close per seat policy; fixtures rebuildable from the commands above.

## Deliverables
- `.ufo/waves/round-52/w1/Falsify40.md` (this report)
- `.ufo/waves/round-52/w1/Falsify40/run-output.txt` (full harness + counter outputs, sha contrasts, attack probe json)

Report: `.ufo/waves/round-52/w1/Falsify40.md`
