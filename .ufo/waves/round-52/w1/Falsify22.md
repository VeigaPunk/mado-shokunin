# Falsify22 — C2 proposition-map completeness attack

Seat: Falsify22 (falsification item 22). Target axis pair: coverage + operability.
Lane repo: `/home/vgpnk/Projects/shokunin/mado-shokunin`, base `85d57a818c3707397e21c840b6498b105ba798aa` (HEAD at investigation time; only `.ufo/waves/round-52/` untracked).
Sources read first: `.ufo/waves/round-52/claims-frozen.md`, `.ufo/waves/round-52/registration.md`, plus `/home/vgpnk/.omp/agent/RULES.md` (tooling authorization; no installs needed or performed).

## Attacked clause (named item/predicate)

C2 frozen predicate, `registration.md`:

> "Frozen condition: at least four substantive propositions; each maps to an opened-this-round `S###` row, a pin path/revision and exact located quote <=25 words, with a written support rationale; **every material factual proposition is mapped**. A counter checks proposition count, row/pin/quote bindings and index; outside reviewer judges source truth."

and `claims-frozen.md`:

> "each material factual proposition maps to a pinned source quote <=25 words and explicit support rationale … A new committed counter checks proposition count, row/pin/quote bindings and **complete mapping**"

**Attacked predicate:** "every material factual proposition is mapped" / the counter's "complete mapping" check.

**Failure mode (directionality of the binding check):** the only mechanically operable reading of "complete mapping" is map→source — every proposition *in the author-declared map* binds to a verifying row/pin/quote. The converse direction, body→map (every material factual proposition *in the entry body* appears in the map), requires enumerating factual propositions in free prose, i.e. automated semantic entailment — which the claim itself excludes ("This is not automated semantic-entailment proof"). An entry can therefore declare exactly the minimum four propositions with perfect bindings while carrying additional material factual claims outside the map — including false ones — and pass every counter check named in the frozen predicate. The residual guard is the human "outside reviewer samples actual source truth," which per `registration.md` samples the mapped set; nothing assigns the reviewer an exhaustive body scan.

## Structural evidence in the committed base counter (observed, source bytes)

`quality/counters/c2-r51-dispatch-entry.py` at base, `clause_b` (lines 378-428): the iteration unit is the entry's *source lines* — `rowids` is built from `SRC_RE.match(line)` over entry prose (lines 390-396), then each cited row is bound via `bind_row` (line 419). Verification runs cited-row → registry/pin/quote. No code path iterates entry-body claims to require a citation per claim; clauses (a) index row, (c) novelty shingles, (d) held citations are likewise claim-direction-free. The r52 counter spec (`w1-dispatch.json` seat `C2CounterDraft`: "Check proposition mapping/count, row/pin/quote bindings and index path; semantic entailment requires outside review") inherits exactly this directionality.

## Reproducible setup and command

Seat-local fixture in scratch `/fast/scratch/hyaku/mado-r52/Falsify22/` (created, used, cleaned; disk guard: 598G free on `/fast`), receipts copied to the seat dir before cleanup:

1. `fixture-entry.md` — an entry-shaped document with a `## Propositions` table declaring four propositions, each bound to a round-51-opened row (S364/S366/S367/S368), a round-51 fetch pin, and a located quote (13/5/5/3 words, all <=25) that verifies byte-exactly against the pinned bytes in `.ufo/waves/round-51/fetch/`; plus an `## Observations` section containing one extra material factual proposition **outside the map**: "the socket verb lowercases the name before the table lookup, so `hyprctl dispatch EXEC xterm` reaches the same callable as `hyprctl dispatch exec xterm`".
2. `falsify22_driver.py` — replicates the frozen counter checks (count >=4; row opened; pin present; quote <=25 words; quote verifies whitespace-collapsed inside the pinned file; index row names the entry), then runs the completeness scan.
3. `fixture-README.md` — index stub naming the entry.

Command: `cd /fast/scratch/hyaku/mado-r52/Falsify22 && python3 falsify22_driver.py` (run 2026-10-27; captured in `run-output.txt`).

## Actual result

- Counter checks: `[1] proposition count: 4 declared -> PASS`; P1-P4 all `opened=PASS pin_present=PASS quote_words<=25=PASS quote_verifies=PASS`; `[5] index -> PASS`; **counter verdict: TARGET_MET**.
- Completeness scan: unmapped material factual proposition present in body: `True`; represented in declared map: `False`; **counter detected it: `False`**.
- Truth of the smuggled claim against pinned bytes: `.ufo/waves/round-51/fetch/Hyprland-HyprCtl.cpp:1143-1150` shows `dispatchRequest` splitting at the first space and calling `g_pKeybindManager->m_dispatchers.find(DISPATCHSTR)` with **no case folding**; only the bind parse path folds (`std::ranges::transform(HANDLER, HANDLER.begin(), ::tolower);` in `Hyprland-legacy-ConfigManager.cpp:1592`). Constructor keys are lowercase literals (`Hyprland-KeybindManager.cpp:42-112`), so `EXEC` over the socket misses and returns `Invalid dispatcher` (`HyprCtl.cpp:1150-1151`). **The smuggled proposition is false per the source bytes** and sits unmapped in an entry that passes every frozen counter check.

## Reproduced: yes

The bypass is reproduced at seat-local fixture level against the locally pinned source bytes. It is a design-level property of the frozen predicate (map→source directionality + excluded semantic entailment), not dependent on the still-in-flight r52 counter implementation: any counter whose checks are limited to the frozen list cannot detect the unmapped proposition, and the frozen no-work control (`controls/c2-do-nothing.md`, absent entry) exercises none of this — it only proves absence at base.

## Dissent / honest limits

- The claim text partially anticipates this: "This is not automated semantic-entailment proof" and the outside-reviewer clause. The attack does not refute C2's achievability; it falsifies the stronger operational reading that "complete mapping" is counter-verifiable. Scoring should not credit the counter with completeness — only with binding correctness of declared propositions.
- The fixture reuses round-51 rows/pins for machinery demonstration only; it is not a corpus candidate and claims no novelty.
- Detection of the smuggled claim by the outside reviewer remains possible in principle (human full-body review); the attack shows the counter provides no mechanical backstop and the registration's "samples actual source truth" wording does not require exhaustive body coverage.
- Round-51 fetch bytes were read locally (`.ufo/waves/round-51/fetch/`, committed in-repo); no live reads, no host/config mutation, no package transactions. Source-only boundary respected.

## Deliverables

- `.ufo/waves/round-52/w1/Falsify22.md` — this report
- `.ufo/waves/round-52/w1/Falsify22/fixture-entry.md` — fixture entry with smuggled unmapped false proposition
- `.ufo/waves/round-52/w1/Falsify22/falsify22_driver.py` — replicated counter checks + completeness scan driver
- `.ufo/waves/round-52/w1/Falsify22/run-output.txt` — captured driver output (TARGET_MET + undetected false claim)

Report trailer (all paths relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`, written under that root):
`.ufo/waves/round-52/w1/Falsify22.md`
`.ufo/waves/round-52/w1/Falsify22/fixture-entry.md`
`.ufo/waves/round-52/w1/Falsify22/falsify22_driver.py`
`.ufo/waves/round-52/w1/Falsify22/run-output.txt`
