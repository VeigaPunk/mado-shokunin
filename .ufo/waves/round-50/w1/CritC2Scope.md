# CritC2Scope — C2 novelty and scope attack

## Verdict
C2 is a real frontier/core transition only for the integrated bind-matching chain, not for every individual term. At the round-50 base, several supposedly novel terms already occur in corpus (and `resolve_binds_by_sym` is explicitly held out in PROVINCE). The novelty predicate MUST NOT treat presence of those strings as new ground. The round-49 candidate also re-states already-held claims explicitly, while citing them honestly; distinguish consolidation from new coverage.

## Term census (read-only git grep)
Compared `03e4ae76aff7a4be59cb69970dd553baa319695a` and `8ae47b957034ae21012bbf09173cca2c48be345e`, searching the five requested terms in `corpus/`, `SKILL.md`, `PROVINCE.md`.

At round-49 base 03e4ae76:
- `resolve_binds_by_sym`: PROVINCE.md:114 says the keybind keymap is not part of the join; corpus/knowledge/hyprland-input-devices-r46.md:71 says the join does not check binds unless the option is enabled.
- `code:`: corpus/knowledge/bind-table-r25.md:46 documents `parseKey` mapping `code:N` to keycode; corpus/knowledge/keybind-rule-semantics.md:108 lists `code:` keycode examples.
- `xkb_state_key_get_one_sym`, `m_xkbTranslationState`, and `CASE_INSENSITIVE`: no hits in the requested paths at this base.

At round-50 base 8ae47b957:
- All the above occurrences persist.
- New in the base lesson corpus: corpus/lessons/round-49-verifier-spotcheck.md:91 quotes `xkb_state_key_get_one_sym` and `m_xkbTranslationState` in its verification of S352; :94 contains `resolve_binds_by_sym`; :101 contains the same option term.
- corpus/lessons/round-49.md:15 records the S352 state-selection expression including `m_xkbTranslationState`; :23 records `resolve_binds_by_sym` as absent from an ArchWiki reject. Neither occurrence supplies the integrated explanation claimed by the candidate.
- `CASE_INSENSITIVE` has no occurrence under the requested paths at the round-50 base.
- `code:` also occurs incidentally in walker-route-r18.md:86 (“Failure modes in code:”), which is a string hit, not keycode ground.

## Candidate sentence-level overlap / contested scope
Compared against `.ufo/waves/round-49/candidate/hyprland-bind-key-match-r49.md` (round-50 C1 is designated a port of this carried candidate).

1. Candidate header and steps 1–3 cover handler/parse/store behavior. This is not fully new: `bind-table-r25.md:46` already states parseKey's `code:N` mapping, and `keybind-rule-semantics.md:108` already lists keycode forms. New value is the source-pinned parse order, boundary distinction, empty-key/catchall and match-time storage connection. Claiming all key-form semantics as novel would overstate.
2. Steps 4–5, observations at 79 and 83–84, establish case-insensitive lookup and libxkbcommon's preference. These terms/claims are absent at both bases in requested paths, so they are the clearest novel sub-surface; `CASE_INSENSITIVE` itself is not a previously held sentence.
3. Steps 6–9 and observations 80/88 explain the selected key state, global translation state, layout behavior and option. At round-50 base, the literal state-selection expression and option already occur in the round-49 lesson/spotcheck, while the round-46 knowledge says bind resolution is outside its join. The candidate's detailed sourced chain and explanation of the distinction are new, but the bare term and selected expression are not. The candidate also says it is sourced and notes held S318/S319 rather than re-registering them; do not count those held facts as fresh evidence.
4. Steps 10–12 on modifier mask construction/comparison are the candidate's new integrated treatment, but held source S319 and the old input-device entry's explicit boundary remain relevant. It must not imply that the entire per-device input join or modifier-state record is newly discovered.
5. Steps 13–17 on branch order, keycode offset, non-keyboard paths, shadowing and dispatch are the widest new scope. The requested base term census alone cannot prove absence of these concepts elsewhere (the census is exact for the five strings, not a semantic corpus-wide search). Candidate references existing keybind-rule-semantics §2.3 and `xkb-keymap-compile-r48` as neighbors at line 19, but no excerpt was available here to establish sentence-by-sentence equivalence. Treat novelty for these as integrated Hyprland-0.56.2 behavior, not as proof that every general keybind concept is new.
6. Host section (lines 95–130) mixes a sourced mechanism with observations and predictions. Lines 120/124 explicitly label consequences as predictions and limit non-tested statements, which is good provenance; those predictions are not host observations. Live receipt facts (192 total / partition and option value) are also held evidence from round 49, not new at round-50 base unless freshly recaptured this round. Do not use the carried receipt alone to claim current live-state novelty.
7. Candidate line 19 states the old knowledge entry held key forms only at `[INF-docs]` level and the round-46 entry explicitly excludes bind resolution. This accurately frames a frontier boundary, but it is a restatement of held scope, not novel content.

## Sibling ownership check
No bind/keymap ownership by sibling lane was established from local evidence: the broad fleet grep found no sibling `PROVINCE.md` or README with an explicit bind/keymap ownership declaration. It found unrelated occurrences in fleet history, quarantined source dumps and other-lane artifacts, which are not ownership evidence. This is a bounded negative search, not proof of no sibling claim. Candidate's own lane statement is mado-shokunin; recommend freeze records the searched sibling files/lanes or leaves cross-lane exclusivity unclaimed.

## Smallest safe correction
In the round-50 C1 novelty clause, enumerate as held at base: `resolve_binds_by_sym` (PROVINCE.md:114; round-46 entry :71), `code:` keycode mapping (bind-table-r25.md:46 and keybind-rule-semantics.md:108), plus the round-49 lesson's occurrence of `xkb_state_key_get_one_sym` / `m_xkbTranslationState` (lesson spotcheck :91 and lesson :15). Score novelty on the new, pinned integrated matcher chain and its case/name, mask, branch-order and consequence explanations, with explicit held-fact/citation treatment; make no blanket claim that the component words or concepts were absent. Identify host capture facts as prior receipt unless re-captured. Do not alter the round-49 artifacts.

## Evidence commands / output
`git -C /home/vgpnk/Projects/shokunin/mado-shokunin grep -n -E 'resolve_binds_by_sym|xkb_state_key_get_one_sym|m_xkbTranslationState|code:|CASE_INSENSITIVE' <revision> -- corpus SKILL.md PROVINCE.md` was run for both base revisions; outputs are enumerated above. Candidate source read: `.ufo/waves/round-49/candidate/hyprland-bind-key-match-r49.md`, especially lines 15–20, 38–53, 55–73, 75–89, 95–130.
