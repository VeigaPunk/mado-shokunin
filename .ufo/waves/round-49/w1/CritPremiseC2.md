# CritPremiseC2 — complete

**Verdict:** C2 is sound that press-time key translation/matching is open at base and not covered by another lane's province. It is not sound to imply all key-field handling is open: `bind-table-r25.md` already grounds parser grammar, `parseKey` behavior, and accepted key representation. Correct by explicitly citing/reusing that held ground and scoping new coverage to runtime matching. The specified Hyprland 0.56.2 commit contains the relevant implementation; source pins/registry rows and committed live receipt were not yet present when reviewed.

Detailed counterexample, evidence, impacted axes, source hashes/locators, and smallest safe correction: `.ufo/waves/round-49/w1/CritPremiseC2/findings.md`.

**Impacted axes:** coverage (duplicate/omitted authority risk); operability (key and modifiers interpretation depends on exact matching semantics). No edits to tracked files, source registry, or entry were made. No checks beyond the listed read-only source and host queries are claimed.
