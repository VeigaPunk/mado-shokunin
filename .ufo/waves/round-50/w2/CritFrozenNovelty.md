# CritFrozenNovelty — w2 (FALSIFY, policy v1) seat report

Seat: CritFrozenNovelty (lane member, leaf; no subagent dispatch, no installs).
Target: C1 novelty/ground clause (i) and the held-fact enumeration in the entry's ground paragraph; clause j's seven topics vs the mechanism.
Base: `8ae47b957034ae21012bbf09173cca2c48be345e`. Attack rev: `b4a79843cc2545bbe800db9322e58f6e00436629` (landed tip).
Work: clone `--shared` at `/fast/scratch/hyaku/mado-r50/CritFrozenNovelty/lane` (TMPDIR under the same scratch); every git call `-C`'d; receipt copied to the seat dir, scratch deleted.

## Verdict

**C1's novelty claim is overstated (fixable entry-text defect, evidence-backed).** The four-term GROUND tuple the counter checks is clean at base, but the freeze re-based that tuple off the known-held terms (registration.md C1 note admits it), and the entry's own ground paragraph under-enumerates what is held: at least one load-bearing "new chain" fact — `stringToModMask`'s uppercase-then-substring semantics — was already on the lane's ground at base and is nowhere in the enumeration. 4 of clause j's 7 topics rest on mechanism strings/facts present at base. The frozen counter is blind to all of this: it scores `TARGET_MET` at the attack rev (rc=0). I do not score claims; the evidence below is for the L1.

## F1 — `git grep -F <term> <base> -- corpus` for every term treated as new

Command shape: `git -C <clone> grep -F -n -e <term> 8ae47b957034ae21012bbf09173cca2c48be345e -- corpus`. Entry at attack rev sha256 = frozen `ae8f8d4d…977` (verified: `git cat-file blob | sha256sum`), so the landed bytes are the attacked bytes.

**Counter's GROUND tuple — all four absent at base (rc=1 each):** `xkb_state_key_get_layout`, `m_modifiersState`, `keysym_to_name`, `xkb_keysym_get_name`. No novelty error inside the tuple itself.

**Terms the entry/counter treat as new but which ARE present under corpus/ at base (novelty errors per the task's rule):**

| term / fact | base location (verified) | where the entry/counter treats it as new |
|---|---|---|
| `m_resolveBindsBySym` | `corpus/lessons/round-49.md:15`; `corpus/lessons/round-49-verifier-spotcheck.md:91` | entry step 6/9; clause-j topic `state` pattern |
| `m_xkbSymState` | same two lines | entry steps 6–7; topic `state` |
| full ternary `… ? pKeyboard->m_xkbSymState : m_xkbTranslationState` (KeybindManager.cpp:369) | `round-49.md:15` (located example, 2026-10-27); quoted verbatim inside the :369 line at `round-49-verifier-spotcheck.md:91` | entry step 6 headline claim ("which keysym of the pressed key enters the comparison") |
| "only `m_xkbState`/`m_xkbSymState` get `update_mask` (`IKeyboard.cpp:379/382/422`)" | `round-49-verifier-spotcheck.md:91` (the spotcheck's own sweep result) | entry step 7 ("it is **never** given a modifier or group update") |
| `xkb_state_key_get_one_sym` | `round-49-verifier-spotcheck.md:91`; `round-49.md:15` | entry step 6 (enumerated as held by the ground paragraph, but see F2) |
| `key.starts_with("code:")` | quoted verbatim at `corpus/knowledge/bind-table-r25.md:46` | entry step 2; topic `code-form` |
| `parseKey` four-outcome chain incl. `isNumber(key) && std::stoi(key) > 9` | `bind-table-r25.md:46` (same line, three more quotes) | entry step 2 |
| `catchall` (incl. submap refusal quote) | `bind-table-r25.md:46`; `:52` | entry steps 2–3 |
| `stringToModMask` + "uppercasing then substring-matching tokens, making token order immaterial" | `bind-table-r25.md:42`; `:44` | entry step 10 |
| `SUPER SHIFT` / `SUPER_SHIFT` / `SUPER+SHIFT` equivalence, "mod order is not significant" | `corpus/knowledge/keybind-rule-semantics.md:69` | entry step 10 |
| `ignoreMods` | `bind-table-r25.md:33` (`case 'i': ignoreMods = true`) | entry step 12; topic `mask` pattern (`!k->ignoreMods`) |
| keysym.c:268 "best case-insensitive match" line | `round-49.md:17`; `round-49-verifier-spotcheck.md:92` | entry step 5; topic `case` semantics |

Absent at base (genuinely new at API level): `xkb_keysym_from_name`, `XKB_KEYSYM_CASE_INSENSITIVE`, `KBKEYLOWER`, `m_lastMods`, `getDeviceInt` (all rc=1 / files=0), and the four-tuple above. `state`/`case`/`mask` as bare topic labels trivially match many files — irrelevant; the mechanism strings above are the substance.

## F2 — the ground paragraph's enumeration vs what is held (named held fact)

Entry ground paragraph (`corpus/knowledge/hyprland-bind-key-match-r50.md`, `ground:` line) enumerates exactly three held items: the `resolve_binds_by_sym` name (PROVINCE.md:114; hyprland-input-devices-r46.md:71 — both verified at base), the `code:` keycode mapping (bind-table-r25.md:46; keybind-rule-semantics.md:108 — verified), and the `xkb_state_key_get_one_sym` / `m_xkbTranslationState` occurrence (round-49-verifier-spotcheck.md:91; round-49.md:15 — verified).

**Held fact it still claims as new:** `stringToModMask`'s uppercases-then-substring, order-immaterial semantics. Entry step 10 presents it as part of the new chain — "It is a substring test, not a token test" — yet bind-table-r25.md:44 already held "uppercasing then substring-matching tokens, making token order immaterial", and keybind-rule-semantics.md:69 already held that `SUPER SHIFT`/`SUPER_SHIFT`/`SUPER+SHIFT` are the same mask with order not significant. Neither is enumerated. Corroborating omissions of the same kind: (b) the state-choice ternary and the update_mask sweep (steps 6–7) — the paragraph cites round-49.md:15 for the one_sym occurrence while that very line carries the whole ternary; (c) `parseKey`'s bare-number `> 9` keycode rule (step 2, pitched as "a split the wiki does not spell out") — held verbatim at bind-table-r25.md:46, of which the paragraph concedes only "the `code:` keycode mapping".

## F3 — clause j's seven topics vs the mechanism

All seven TOPICS regexes match their named pins at real matcher lines (verified by a read of the pinned bytes at the attack rev):

- `state` → KeybindManager.cpp:369; `case` → :711; `mask` → :652; `code-form` → legacy-ConfigManager.cpp:1484; `zero-mod-sym-state` → IKeyboard.cpp:382,422; `depressed-mask` → InputManager.cpp:1711; `option-read` → InputManager.cpp:1224.

So the topics are mechanism-true, not filler words — each names a load-bearing line of the match chain. The defect is provenance, not correspondence: per F1, the strings/facts under `state`, `mask`, `code-form`, and `zero-mod-sym-state` (and `case`'s quoted keysym.c:268 line) were already on the lane's ground at base; only `depressed-mask` (`m_lastMods = MODS.depressed`) and `option-read`'s `getDeviceInt` call are new at the API level, with `case` new only in its Hyprland-side call form.

## F4 — instrument blind spot (fixable vs rejectable)

Frozen counter run at the attack rev on the clone: `TMPDIR=<scratch> python3 -I quality/counters/c1-r50-bind-entry.py --repo <clone> --rev b4a79843…` → final line `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 r:1 admitted=1/1 verdict=TARGET_MET`, rc 0 (full receipt: `w2/CritFrozenNovelty/c1-at-attack-rev.txt`; clause i prints `ground_present=2/4`). Clause i only checks the 4-term tuple — deliberately re-based per registration ("Clause i GROUND tuple re-based because the round-49 closure text itself quotes the round-49 terms … under corpus/"). The freeze therefore knew the ground was wider than the tuple and narrowed the instrument instead of the claim.

**Impacted axes:** coverage (C1 sourced-expansion: the "frontier → core" move is partially false provenance); operability untouched. Counter byte-integrity and receipts are unaffected.

**Smallest safe correction:** entry-text, not counter, not kill — extend the ground paragraph to enumerate `stringToModMask` semantics (bind-table-r25.md:42,44; keybind-rule-semantics.md:69), the ternary/update_mask sweep (round-49.md:15; round-49-verifier-spotcheck.md:91), and `parseKey`'s `> 9` rule (bind-table-r25.md:46), and narrow the novelty sentence to what is actually new (the libxkbcommon `from_name`/state internals, the branch order, the live receipt). If the L1 wants instrument-level coverage, clause i's GROUND tuple could be widened — but that is a freeze change, out of this seat's scope.

## Deliverables

- `mado-shokunin/.ufo/waves/round-50/w2/CritFrozenNovelty.md` (this report)
- `mado-shokunin/.ufo/waves/round-50/w2/CritFrozenNovelty/c1-at-attack-rev.txt` (frozen-counter receipt at the attack rev, rc=0)

No tools installed. No lane/fleet/scratch writes outside the seat dir and scratch (scratch clone + tmp removed after the receipt copy).
