# RevEntryFlags — sentence-level audit of `hyprctl-flags-r28.md` vs receipt S221.bin

Wave 1, round 38. Scope: the entry at `corpus/knowledge/hyprctl-flags-r28.md`
(48 lines, cited by line below), its receipts, the amend-chain claim against
`dispatcher-surface-and-request-grammar-r26.md` §3, and header schema vs sibling
entries. Read-only; nothing modified.

Receipt pin: `.ufo/waves/round-38/fetch/S221.bin` — 306,865 B, sha256
`35046ba0dc1dd1db4b1e8548e7e6a0be9f0ffc0051c055f66ddee5451879d30a`
(computed; matches lesson GATE S221 and the SOURCES.md S221 digest). Page: HTML,
title "Using hyprctl – Hyprland Wiki" (S221.bin:11), `0.56.0` markers ×221.

## Verdict

All three OBS quotes are verbatim in the receipt bytes (each verified by grep).
The two INF claims are faithful readings; their bases are real, but both cite the
wrong section of `ipc-contract-r25.md` (§2 instead of §1). The amend-chain
claim overstates: r26 §3 contains no open item on per-flag semantics. The two
UNK claims are accurate as scoped. Findings below by severity.

## Findings

### F1 (moderate) — Mis-cited internal sections in both INFs (entry:18-23, 31-34)

- entry:23 cites `knowledge/ipc-contract-r25.md` **§2** for the request grammar
  `[flags]/command args` (S186:19). The grammar is established in
  `ipc-contract-r25.md` **§1** (line 42: `> "Basically, write \`[flags]/command args\`." (S186:19)`); §2 is "The event socket (documented)" (line 54) and never mentions flags.
- entry:32 cites `ipc-contract-r25.md` **§2** for "the request socket's
  synchronous evaluation". That claim is in §1 (lines 44-47, quote at 47: "Hyprland evaluates connections to this socket completely synchronously…"); §2 has no synchronous-evaluation claim.

The cited facts exist, but at §1, not §2 — both section pointers are wrong.
Substantive content verified: `[flags]/command args` = S186.bin:19
(round-32/fetch, raw wiki markdown, line 19 = "Basically, write `[flags]/command args`."),
synchronous sentence = S186.bin:22 (`synchronously, which means that any unclosed
connections *will cause Hyprland to freeze*…`) and S187.bin:2855 (`<p>Hyprland
evaluates connections to this socket completely synchronously,…`).

### F2 (moderate) — Amend-chain claim: r26 §3 has no "per-flag semantics" open item (entry:4-6)

The entry asserts r26 §3's "open item was the per-flag semantics". Full read of
`dispatcher-surface-and-request-grammar-r26.md` (78 lines) shows §3 (lines 59-69)
contains an OBS (grammar is a flag-prefixed command line, S186:19; event socket
framing; dispatcher is not a socket request) and an INF (two surfaces; `event`
bridge). There is no open-item marker in §3 — no "open", "gap", "pending",
"per-flag" wording anywhere in the file — and §4 "What this entry does not claim"
(lines 71-78) lists only: nothing dispatched/observed; name list not exhaustive;
revision-string caveat. The amendment is real in substance (r26 §3 only exercised
the `[flags]` grammar, never the flag semantics), but the specific claim "whose
open item was the per-flag semantics" is not supported by the amended entry's
text; the open-item framing is not stated there. The corresponding SOURCES.md
S221 row ('"amending dispatcher-surface-and-request-grammar-r26.md §3"') and the
lesson (line 34) are similarly silent on an explicit open item.

### F3 (low) — "The three documented flags" heading overreaches the page (entry:13, 15-16)

§1 body is correctly scoped to the `flag list:` block, but the heading "The
three documented flags" reads as a page-wide count. The same page documents a
fourth flag: S221.bin:3375 `You can use the legacy <code>--batch</code> flag to
issue multiple commands separated with a <code>;</code>.` — the word "flag" is
the page's own. The OBS/INF below the heading are not wrong (they are scoped to
the `flag list:` block), but in the heading is broader than the receipt supports.

Also noted: S221.bin:3376-3381 — the `§ Flags` section prose is "You can specify
flags for the request like this:" + syntax block `hyprctl -j monitors` (line
3380). The entry's INF "j changes the reply's encoding / i chooses which
compositor instance answers / r asks… to re-read its state" is a faithful reading
of the three descriptions.

## Verified-passing claims

- **OBS §1 quote set (entry:15-16)** — verbatim after `&gt;` unescaping; the
  entry discloses the unescaping (entry:47-48). Receipt lines, in the `flag list:`
  block (paragraph at S221.bin:3392, chroma <code> block immediately after,
  3394-3397):
  - 3395 `j -&gt; output in JSON` → `j -> output in JSON` ✓
  - 3396 `i -&gt; select instance (id or index in hyprctl instances)` ✓
  - 3397 `r -&gt; force state refresh after issuing commands (e.g. layout or rule changes)` ✓
  - exactly three line spans in the block; "the flag list as three flags" ✓
  - "inside the page's `flag list:` code block" — `flag list:` is in fact the
    `<p>` label (3392) for the immediately-following code block; faithful.
- **OBS §2 quote (entry:27-29)** — verbatim in receipt at 14, 49, 56 (meta
  description + body copies): `hyprctl calls will be dispatched by the compositor
  synchronously, meaning any spam of the utility will cause slowdowns.` ✓ (the
  sentence continues past the quote with `It’s recommended to use --batch…`
  — outside the quoted span). "same page warns" ✓.
- **INF §1 substance** — no fact asserted beyond the three descriptions and the
  grammar (S186:19); interpretation is sound. Section pointer wrong (F1).
- **INF §2 substance** — S187.bin:2855 confirms the synchronous-evaluation
  sentence on the 0.56.0 IPC page; the "price… paid on a synchronously served
  socket" inference is in-bounds. Section pointer wrong (F1).
- **UNK §3 first (entry:38-41)** — accurate as scoped: no round-38 artifact
  reads per-flag server handling; the flag-stripping lines S158.bin:2068-2096
  (`// process flags for non-batch requests`; `// remove flags and separator so
  we can compare the rest of the string`) were not read by the lane this round
  (r8 cites S158 only for the accept loop: line 21 `5000`/`poll`; entry 17
  `accept loop answers differently (S158)`), and they strip the flag segment
  generically — they say nothing about what the server does with `j`/`i`/`r`
  individually. The second clause ("a leading flag segment is stripped before the
  dispatcher name is matched") is asserted as contract content: `ipc-contract-r25.md`
  contains no "strip" statement (grep -i strip → no hits; it only records the
  `[flags]/command args` grammar); the stripping fact is only in S158 (fetched
  this round) — so the attribution "the IPC contract established" is loose, the
  fact itself is real and in-round. No contradiction of the UNK.
- **UNK §3 second (entry:41-42)** — accurate: lesson finding 2 (
  `corpus/lessons/round-38.md` "Findings" item 2) states the same UNK verbatim,
  and nothing in round 38 inspected host config for flagged requests. The lesson
  explicitly documents it as "an explicit UNK in `hyprctl-flags-r28.md` §3" ✓.

## Header schema vs siblings

- `source:` (entry:8) — same shape as siblings (r31/r8/r26/ipc-contract):
  `S<n> — <url> — section — provenance`. URL matches receipt (title at
  S221.bin:11; URL canonical). "fetched 2026-10-25" matches receipt mtime
  2026-10-25 10:52 ✓ and SOURCES.md row ("mined | 2026-10-25").
- `verified-at: 2026-10-25` (entry:9) — bare ISO date; matches sibling values
  (`2026-10-24`/`2026-10-25` bare) ✓.
- `recheck: on-release` (entry:10) — cadence token; matches r31/r8 and
  hyprland-config-era-r12.md (`on-release`) ✓ — and the correction block
  (entry:44-46) documents the package draft's prose cell was collapsed to the
  schema token. The promised run note in the round-38 lesson: the lesson contains
  no note about the recheck cell or the package run note (grep `run note|recheck`
  over `corpus/lessons/round-38.md` → no hits). The correction's pointer "the run
  note lives in the round-38 lesson" (entry:46) does not resolve to any such
  content — the lesson instead carries the GATE block, the adoption ledger, and
  findings. Either the run note was dropped, or it lives somewhere the pointer
  does not name. Dangling pointer within the entry itself.
- `ground:` (entry:11) — "a new edge class under the held IPC contract" matches
  the r31/r8 house style verbatim ✓; the held-contract path
  `knowledge/ipc-contract-r25.md` resolves ✓.
- No `## Gate` heading in r28 (consistent with r8/r31 — none of the three
  re-grounded request-socket entries has one; digest pinning lives in
  `corpus/SOURCES.md` rows and the lesson GATE block — both present for S221 ✓).
- Header lines themselves: no bare-ISO/cadence violation found.

## Cross-file observations (out of this lane's edit scope, for the registry/scribe peers)

1. `corpus/SOURCES.md` S221 row (line 220) states size "35046 B" — the receipt is
   306,865 B (35046 is the sha256 prefix, likely pasted as size). Digest itself
   matches. Flag for RevRegistry.
2. `corpus/SOURCES.md` S221 row also states page revision "Last updated on May 2,
   2026" — the receipt's revision is `<time datetime="2026-06-13T19:18:41.000Z">June 13, 2026</time>` (S221.bin:3413). The row's revision string is wrong (it is the IPC page S187's revision, S187.bin:3136 "May 2, 2026"). Flag for RevRegistry.
3. The entry's source line does not carry the revision string, so the entry
   itself is not affected by (2); the entry makes no revision claim ✓.

## Items impossible as written / not covered

- None blocked. I did not open the host's `~/.zsh_history` (out of bounds per
  lesson finding 4) and did not inspect the host's config for flagged requests —
  consistent with the entry's own UNK; no evidence contradicts it.
- No installs were made (no tool needed beyond grep/sed/sha256sum/awk).

## Residual risk / verification gaps

- r26 §3's open-item framing cannot be shown true (F2) — the only way it could
  be true is if the shokuknow package draft (not in-lane) contained that marker
  and the lane's "Amends" line copied it; the lane-side text does not record it.
- S221.bin has four copies of the synchronous warning (lines 14, 27-28, 49, 56,
  2902); the quote was verified against the body sentence, not the meta
  description — same bytes, no ambiguity.
