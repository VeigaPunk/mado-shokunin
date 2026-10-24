# Round-32 C1 — recheck prose stripped from staged cells

For the round-32 `## Gate` block of `corpus/lessons/round-32.md`.

Rule (registration item 10.3): staged campaign `recheck` cells carry prose — a
cadence token followed by a free-text instruction and a run receipt — which is
not a valid census recheck (ISO date, `NNd`, or symbolic cadence). Each cell was
reduced to its leading cadence token; the tokens chosen are cadences the lane
registry already uses (`on-release`, `on-compositor-release`; S043, and the
r25–r31 rows). The stripped suffix is recorded verbatim below so the recheck
instruction is not lost — it describes what the cadence actually checks.

| id | staged recheck cell (verbatim) | kept token | stripped prose (verbatim) |
|---|---|---|---|
| S186 | `on-release — re-pull the file and compare sha256 (expect prefix 535bc4c385a06162) (ran 2026-10-23)` | `on-release` | `— re-pull the file and compare sha256 (expect prefix 535bc4c385a06162) (ran 2026-10-23)` |
| S187 | `on-compositor-release — re-fetch the page and re-diff its event table against the pinned upstream source (ran 2026-10-23)` | `on-compositor-release` | `— re-fetch the page and re-diff its event table against the pinned upstream source (ran 2026-10-23)` |
| S188 | `on-release — re-pull the file and compare sha256 (expect prefix c830ce0717f92776) (ran 2026-10-23)` | `on-release` | `— re-pull the file and compare sha256 (expect prefix c830ce0717f92776) (ran 2026-10-23)` |
| S189 | `on-compositor-release — re-pull at the host's tag and re-check formatEvent (ran 2026-10-23)` | `on-compositor-release` | `— re-pull at the host's tag and re-check formatEvent (ran 2026-10-23)` |
| S196 | `on-compositor-release — re-fetch and re-diff the dispatcher list against the pinned upstream source (ran 2026-10-23)` | `on-compositor-release` | `— re-fetch and re-diff the dispatcher list against the pinned upstream source (ran 2026-10-23)` |

Notes:

- The backticks above quote the staged text; the staged cells themselves contain
  no backticks around the sha256 prefixes (`(expect prefix 535bc4c385a06162)`
  verbatim). `formatEvent` is backtick-quoted in the staged S189 cell; that cell
  reads ``re-check `formatEvent` `` verbatim.
- `on-release` vs `on-compositor-release` distinction preserved from staging:
  `on-release` pins a fixed commit/tag artifact (re-pull and compare bytes);
  `on-compositor-release` tracks the compositor's own release line (re-check at
  the host's tag, or re-diff the version-matched docs page).
- The `(ran 2026-10-23)` run receipts describe the campaign's staging date; the
  L1 re-grounded all five rows in this round (opened 2026-10-24, fetch bytes in
  `.ufo/waves/round-32/fetch/`).
