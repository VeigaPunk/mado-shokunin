# ScrEntryC — Draft C of the C2 entry (minimal, one fact one quote)

Seat: `ScrEntryC` (scribe, leaf — no subagent dispatch). Round 41, wave w1. Lane `mado-shokunin`.
Read-only throughout: no compositor, portal, Wayland or package verb; no `journalctl` run by this seat
(the journal is the L1's saved receipt); no mutating git/jj; no writes outside this seat's directory
and its `Report:` file. Tool installs: none.

## Behavior

Draft C of the C2 entry, written to
`.ufo/waves/round-41/w1/ScrEntryC/hyprland-focus-grab-r41.md`: 66 lines, five OBS-bearing sections
(protocol surface, compositor side, advertisement on this host, one real client, rule-level counterpart),
three named unknowns, one INF per section, and one closing "what this does not license" list.

Shape delivered, against the seat's checklist:

| item | value |
|---|---|
| title + `Lane:` line | present (lines 1, 13) |
| `source:` lines in the first 20 lines | 7 — S283, S284, S285, S286, S287, S288, S289, in that order |
| `verified-at:` | `2026-10-25` (line 10) |
| `recheck:` | `90d - …` (line 11, matches `^(\d{4}-\d{2}-\d{2}\|\d+d\|on-[a-z-]+)(\s\|$)`) |
| `ground:` | line 15 |
| census line | `journal sessions=2 adverts=78 interfaces=63 focus_grab=1`, once, outside any fence (line 37; the entry has no fences at all) |
| tags | `**OBS**` 7, `**INF**` 5 (one per section), `**UNK**` 3 (each named) |
| cited ids | S283–S289 only; no S290; **no held id** (see Findings 1) |

One quote per cited id, on the single entry line that names the id (the strictest reading of
"one fact one quote"); no other quoted material anywhere in the entry. The 7 strings are exactly the
ones `ScrRowsDraft` published (IRC, this wave) so the lesson's `## Gate` lines bind clause g:

| id | receipt | line in receipt | quote (words) |
|---|---|---|---|
| S283 | `fetch/focus-grab-v1.xml` | `:62-63` (entry cites `:39-124`) | "This interface restricts input focus to a specified whitelist of surfaces" (11) |
| S284 | `fetch/Hyprland-FocusGrab.cpp` | `:20` (entry cites `:18-21`) | `m_grab->m_keyboard = true;` (3) |
| S285 | `fetch/quickshell-grab.cpp` | `:78` | "the protocol will always send cleared() when the grab is deactivated," (11) |
| S286 | `fetch/xdph-PortalManager.cpp` | `:88` (entry cites `:88`, `:90-122`) | `Got interface: {} (ver {})` (5) |
| S287 | `fetch/issue-565.html` | `:706` (entry cites `:706`, `:656`, `:659`) | "Tried to set workspace silent rule to a nofocus window!" (10) |
| S288 | `fetch/protocols-README.md` | `:17` | "for grabbing input focus, primarily for complex context menus" (9) |
| S289 | `fetch/xdph-journal.txt` | `:117` | `Got interface: hyprland_focus_grab_manager_v1 (ver 1)` (5) |

## Gates (what this seat actually ran)

1. **Quote check, re-runnable**: `python3 .ufo/waves/round-41/w1/ScrEntryC/verify-quotes.py` →
   receipt `.ufo/waves/round-41/w1/ScrEntryC/verify-quotes.txt`, rc 0. It copies the counter's `norm()`
   (tags/scripts/styles stripped, entities decoded, whitespace collapsed) and its census regex/parser,
   and prints, per id: quote verbatim in the receipt, exactly one entry line naming the id and carrying
   the quote, 3–25 words. Output:

       lines=66 sources_in_head=S283,S284,S285,S286,S287,S288,S289
       clause_b verified-at=True recheck=True ok=True
       clause_h census_lines=1 matches=1 computed=(2, 78, 63, 1) entry=(2, 78, 63, 1) ok=True
       clause_dg id=S283 … ok=True   (S284..S289 likewise ok=True)
       ALL_QUOTES_OK=True cited=S283,S284,S285,S286,S287,S288,S289

2. **Census re-derived, not copied**: the saved journal was parsed with the counter's own grammar
   (`ADV_RE`, `BOOT_RE`, session rule) — 2 sessions (pids 1918 and 1952, 15 and 63 adverts),
   78 adverts total, 63 distinct names in the latest session, 1 advert of
   `hyprland_focus_grab_manager_v1` (ver 1) at `2026-10-25T13:36:24-03:00`, pid 1952. The entry's
   census line equals those numbers.

3. **Location check**: every `file:line` the entry cites was printed from the receipt and matches
   (`awk`/`sed` over the frozen fetch bytes): xml `:39`,`:44`,`:52`,`:60`,`:79`,`:91`,`:105`,`:115`,`:121`,
   description `:62-63` and `:72-76`; `Hyprland-FocusGrab.cpp` `:18-21`,`:22`,`:31`,`:58`,`:137-142`,`:141`;
   `quickshell-grab.cpp` `:74-90`,`:78`,`:98`; `xdph-PortalManager.cpp` `:88`,`:90-122` (the quoted
   branch at `:99`); `issue-565.html` `:656`,`:659`,`:706`; `protocols-README.md` `:17`;
   `xdph-journal.txt` `:117`.

4. **Province**: no localized-documentation channel is cited (no `amgsk.dev`, `zhihu`, `/zh`, `/ja`);
   read `PROVINCE.md:60-80` before choosing sources.

**Not run, and not claimed**: the frozen counter `quality/counters/c2-r41-focus-entry.py` was not run.
It scores a committed revision and needs the registry rows (S283–S289), the lesson's `## Gate` and the
`corpus/README.md` index row to exist at that revision; nothing of this seat's work is committed, and
committing is the L1's act. Draft C is therefore a draft that satisfies clauses b, d, g, h as far as a
single file can, and is silent on a, c, e, f, i (rows, lesson, README, commit).

## Touched surfaces

- `.ufo/waves/round-41/w1/ScrEntryC/hyprland-focus-grab-r41.md` (new, the draft)
- `.ufo/waves/round-41/w1/ScrEntryC/verify-quotes.py` (new, the re-runnable check)
- `.ufo/waves/round-41/w1/ScrEntryC/verify-quotes.txt` (new, its output receipt)
- `.ufo/waves/round-41/w1/ScrEntryC.md` (this report)
- One peer message to `ScrRowsDraft` (cited ids, held-id refusal, confirmation of the 7 gate strings).
- Nothing else: no edit to the counters, controls, registration, reference tool, fetch receipts,
  `corpus/SOURCES.md`, the lesson, the README, or the lane's git/jj index.

## Findings

1. **No held id fits, and S037 is the reason.** Clause d wants, per cited id, a committed receipt under
   `.ufo/waves/round-41/fetch/` with that sha256, distinct per id. S037's location is the v1.4.1 release
   URL and no release-notes receipt exists in `fetch/`; using `xdph-PortalManager.cpp` for S037 would
   either collide with S286's receipt (paths must be distinct) or attach a source-file receipt to a
   release-URL row. Both are dishonest provenance, so S037 (and S041/S043/S052/S162) are not cited.
   The seat's "cite a held id if it fits" therefore resolves to "it does not fit"; the frozen counter's
   clause c accepts a new-only id set (`len(new_ids) >= 2`).
2. **The portal advertises but does not use the global.** `grep -ci focus` over
   `fetch/xdph-PortalManager.cpp` is 0; `onGlobal` logs every global (`:88`) and binds a fixed set of
   names (`:90-122`). The journal's single advert is therefore evidence of the compositor's offer to
   that connection, not of use — the entry states this as INF with both receipts as basis.
3. **`cleared` is conditional in the compositor.** `finish(bool sendCleared)` (`:58`) is called with
   `false` from the destructor (`:31`) and with `true` from the seat-grab callback (`:22`) and from a
   commit that empties the whitelist (`:141`). Destroying the grab object sends no `cleared`; the XML's
   "regardless of cause" describes the compositor-cancelled case only. Stated as INF, both sites cited.
4. **Quote alignment matters more than quote strength.** This seat's own first draft used
   `void CFocusGrab::finish(bool sendCleared) {` for S284 and
   `if (INTERFACE == hyprland_input_capture_manager_v1_interface.name)` for S286 — both verbatim and
   both stronger facts, but the lesson's `## Gate` will carry `ScrRowsDraft`'s strings, and clause g
   matches the gate quote against the entry line. The draft was rewritten to the published strings so
   the wave's gate cannot miss; the weaker quote is paid for by citing the surrounding lines.
5. **Issue #565 is a 2022 rule report, not a protocol fact.** Its log line shows the rule engine
   refusing focus ("Tried to set workspace silent rule to a nofocus window!"), which is the rule-level
   counterpart; the entry marks the 0.56.2 question UNK and refuses any measurement claim.
6. **Minimality cost, stated**: draft C drops the class-decision-table material (draft B's INF layer),
   the input-capture protocol (S290), and the `.hpp`/request-argument detail. It also gives the
   protocol's `cleared` semantics only one sentence (§2 INF); a reader wanting the seat-grab internals
   must open S284 `:46-52`, which the entry cites but does not quote.
7. **S287's closure date is not a structured field (correction from `ScrRowsDraft`, applied).**
   `grep -o '"closedAt":"[^"]*"'` over `fetch/issue-565.html` is empty; the receipt carries
   `"createdAt":"2022-08-23T14:03:55Z"`, `"state":"CLOSED"` and `"stateReason":"COMPLETED"`. The
   rendered sentence "closed this as completed on Aug 25, 2022" is not a contiguous byte string
   (raw `grep "closed this as"` is empty — the words are split by tags), and `Aug 25, 2022` occurs
   3× inside `relative-time` elements attached to comments. The header now reads
   `createdAt 2022-08-23, state CLOSED reason COMPLETED, replies dated 2022-08-25`, and the UNK says
   "closed as completed" with no closure date. Checked after the correction: `verify-quotes.py` rc 0,
   66 lines, all 7 quotes still ok.

## Artifacts

- Draft: `.ufo/waves/round-41/w1/ScrEntryC/hyprland-focus-grab-r41.md`
- Check: `.ufo/waves/round-41/w1/ScrEntryC/verify-quotes.py`
- Check receipt: `.ufo/waves/round-41/w1/ScrEntryC/verify-quotes.txt`
- Frozen inputs read: `.ufo/waves/round-41/registration.md`, `quality/counters/c2-r41-focus-entry.py`
  (contract), `corpus/knowledge/hyprctl-getoption-native-forms-r40.md`,
  `corpus/knowledge/host-bar-producer-census-r40.md`, `corpus/SOURCES.md:49` (S037),
  `PROVINCE.md:60-80`, and the nine files in `.ufo/waves/round-41/fetch/`.
