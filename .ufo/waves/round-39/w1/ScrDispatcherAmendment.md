# ScrDispatcherAmendment — round-39 w1 report (scribe, leaf)

## Deliverable

- `corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md` — held entry, NOT
  touched (read-only; no edit performed).
- Drafted append block: `.ufo/waves/round-39/w1/ScrDispatcherAmendment/dispatcher-amendment-section.md`
  (4907 B) — a dated amendment section (2026-10-25) to be APPENDED to the held entry
  by the lane helper; the held text stays untouched.
- Only two files written this seat: the amendment draft above and this report. No
  other path inside or outside the lane was written.

## Evidence and commands (all read-only in the lane)

- Lane tip at write time: `git rev-parse HEAD` → `457d1b125932c1e0d797061a2156b917bcd7edaa`.
  `git status --porcelain | wc -l` → 8 (pre-existing uncommitted lane work; untouched).
- S018 held receipt re-opened: `.ufo/waves/round-24/fetch/S158.bin` (committed
  round-24 fetch of HyprCtl.cpp@efb5099). `sha256sum` → `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa`,
  byte-equal to the S018 SOURCES row hash (pinned commit
  `efb50993780079460b0cbed1363e2166a2de1d9f`). Line numbers in the draft are the
  upstream line numbers at that commit.
- S220 fetch receipt: `.ufo/waves/round-39/w1/ExecAssimFetches/S220.bin`. `sha256sum`
  → `f9b51362f2440e02999089a255c5d7f3feb103f3cdeb6124c86a9f285c14b6e2`
  (297,863 B; identical to held S196 fetch bytes; page revision "Last updated on July
  15, 2026"). The ExecAssimFetches report was not published at write time, so the S220
  quotes/anchors were taken directly from the shared `S220.bin` artifact (raw HTML
  line anchors), independently verifiable.
- Quote extraction: `sed -n '<n>p'` on S158.bin and S220.bin (exit 0); token counts
  via `awk '{print NF}'` after `tr -s ' '` — all quotes ≤25 whitespace tokens:
  S018:1131=10, S018:1132=6, S018:1149=5, S018:1151=3, S018:1310=14,
  S018:2096=19, S220 first sentence=10, S220 second=11.

## Quote map in the draft

| Anchor (S018 = HyprCtl.cpp@efb5099) | Ground |
| --- | --- |
| 1149 `g_pKeybindManager->m_dispatchers.find(DISPATCHSTR)` | registry resolution |
| 1151 `return "Invalid dispatcher";` | unknown-name error |
| 1131-1132 Lua wrap `return hl.dispatch({})` | Lua-config dispatch path |
| 1309-1310 `dispatchBatch` split ignoring `;` in brackets | batch grammar |
| 2096 flag-segment strip in `CHyprCtl::getReply` | flag preprocessing |
| S220.bin raw 2936-2938 `#dispatchers` section | 0.56.0 page existence + Lua table consumption |

## Content requirements — status

- Dated block: header `## Amendment — re-grounded dispatcher surface and request-socket
  resolution (2026-10-25)`.
- Provenance trio + verifying date: `source:` S018 and S220 (with pins/hashes),
  `verified-at: 2026-10-25`, `recheck: on-release`.
- Gate: reopening method for both sources with hashes.
- UNK statements included: per-flag semantics unenumerated (S018:2085-2093 observable
  switch-setting only); host config flag usage uninspected (no host config tree opened);
  static parse ≠ live health. No universal clauses; claims are falsifiable and located.

## Safety

- No pacman/package transaction (host-wide pause respected; RULES.md read; no tool
  install was needed — no installs recorded).
- No git/jj mutation; no fleet/sibling/template/scripts/MANIFEST.json/state/watchdog
  paths touched; no socket connect; no compositor or host config mutation.

## Limits

- The S220 quote sentence is taken from the shared fetch bin, not from the executor's
  report (unpublished); if the executor records a different sentence for S220, the
  draft's raw-line anchors still verify against S220.bin.
- Line numbers in the draft are upstream line numbers via the byte-identical S158.bin;
  the draft states this equivalence in its Gate.
