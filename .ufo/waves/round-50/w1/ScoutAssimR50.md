# ScoutAssimR50 — findings

## Assimilation scope

- The staged package contains 69 knowledge entries across rounds 1–16, but its report identifies no staged Hyprland bind/keysyms/keymaps entry and no session-material/privacy entry; keyword scan of the report shows only unrelated "binding" descriptions. **No staged theme matches C1 or C2.** Province scope: `PROVINCE.md:3-16` owns desktop/compositor config (including Hyprland keybinds) and says config trees are read-only; session-material privacy is repository evidence hygiene rather than a desktop/compositor surface. No PROVINCE.md was included in the staged package; read lane `PROVINCE.md`.
- Item-10 id extraction (same patterns as prompt) outputs are saved under `.ufo/waves/round-50/w1/ScoutAssimR50/assimilation/`: registry IDs 288, staged IDs 147, intersection/collisions 94. Therefore adoption cannot use staged IDs as-is; renumbering must be by source/document, not arithmetic. The guard fixture with indented `  | S002 |` row gave reg=1, staged=1, collisions=1 (nonempty), proving the 0–3-space pattern catches it.
- Quarantine awk output: 13 data rows, and all 13 carry S-ids. Six are `payload-absent` (S189, S195, S201, S205, S224, S228); seven are unchecked prose classes (S199, S200, S209, S222, S223, S225, S235: source could not be fetched / no locator). This is a derived slice only; no rows were hand-checked or adopted.

## Reflection proposal

`considerthese/2026-10-26.md` is the latest reflection. Round 45 already mapped proposal 1 (privacy check on new receipts) to `quality/check-session-material.py` and QUALITY 85; round 48 reports proposal 6 landed as QUALITY 99. Proposal 2 was refused in round 47 because its draft live-state tool ledger had wrong rows; proposal 3 landed as QUALITY 90 in round 46. Proposal 1 is the one recommendation to ground this round: C2 does implement its core direction by upgrading the session-material gate for structural home-path, account-owner/group, exec-cache and out-of-`.ufo/` material, with nonce-generated red/green fixtures and selftest (`claims.md:24-31`). It is not a general same-day scan of each day's newly written `.ufo/**/receipts/`, nor a notification workflow; its stated scope is the enumerated shapes and generated fixtures. Record only that bounded coverage, not the broader proposal as fully implemented.

## Captured outputs / evidence files

Command outputs: `reg-ids=288 staged-ids=147 collisions=94`; `guard fixture: reg=1 staged=1 collisions=1`; `quarantine rows=13 all-id-lines=13`. Files: `assimilation/reg-ids`, `staged-ids`, `collisions`, `guard-registry`, `guard-reg-ids`, `guard-staged-ids`, `guard-collisions`, `quarantine-slice`.
