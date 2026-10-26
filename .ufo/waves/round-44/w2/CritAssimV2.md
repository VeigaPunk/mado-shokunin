# CritAssimV2 — the landed admission decisions (mado round 44, w2)

Seat: critic of the assimilation decisions as landed at `e4678921` (base `6a1a9052`), against
`.ufo/waves/round-44/registration-v2.md` (`03fa5c61`). Read: the entry, `corpus/lessons/round-44.md`
(`## Gate`, the ledger, M44-1), the five residue files (`r12`, `r13`, `r14`, `r15`, `r9`), the five
round-44 pins, `w1/CritAssimilation.md`, `w1/ScoutStagedResidue.md`, and the rows `S164`, `S165`,
`S295`, `S296`, `S297`, `S301`.

Every quote below is re-found at its computed locator by `quote-check.py` → `quote-check.txt`
(`QUOTE-CHECK: 33/33 passed`). Line numbers were computed with `grep -n`
(`landed-locators.txt`, `residue-line-numbers.txt`); pin bytes are `pin-readings.txt`, `clamp.txt`,
`axes-and-final.txt`; byte proofs are `admit-bytes.txt`; flip tests are `flip-reachability.txt`,
`round24-sweep-check.txt`; held-row ground is `s165-precedence.txt`, `r9-held-ground.txt`.

## Answers to the three questions

**1. Is the r12 ADMIT justified — what of r12 survives?** Yes, and it is the least-lossy decision of the
round. The two re-groundings are byte facts, not tag names: the pin `fetch/Hyprland-Window.cpp` hashes
`d735d454…`, equal to the lane's held receipt `.ufo/waves/round-24/fetch/S164.bin` and to S164's row
digest (`admit-bytes.txt`); `fetch/gkeep-ui.py` hashes `07a3c4a5…`, equal to
`git -C ~/Projects/gkeep show 133b867:gkeep/ui.py` (same receipt). What survives **in the entry**:

| r12 claim (computed locator) | in the entry |
|---|---|
| `sendWindowSize` → `realToReportSize` → `setSize` → `m_pendingSizeAcks` (r12:24,26,28) | entry:30, same path plus the X11 branch |
| gkeep's declarations: default size, no `set_size_request`, `button.ink` minima (r12:41-47) | entry:56, plus `set_decorated(False)` |
| the observation is still missing (r12:65-68) | entry's "does not establish" list |
| "`xdg_toplevel.set_size`" (r12:31) | excluded; corrected to the configure event (entry:69) |
| the ack as a client size channel (r12:34-35) | excluded; replaced by the `onAck` reading (entry:38-40) |
| "no minimum-size request will adopt the size" / "The chain is now complete" / "The rendered geometry of a gkeep window is 420×500" (r12:52,59,62) | excluded; replaced by the GTK hint reading (entry:48-52) and UNK |

No true r12 claim is dropped. One gap remains on the ADMIT's product — F6 below.

**2. Is each REFUSE reason true and its flip reachable?**

| file | reason true? | flip reachable/sufficient? | finding |
|---|---|---|---|
| r13 | **half**: true of `onAck`, false about "its Window.cpp half" being carried | reachable, and it is the right flip for the S320 absence only | F2 |
| r14 | **false**: a second, uncited ground (§2) carries part of the absence claim | the stated flip fires but leaves §2 unsourced — insufficient | F3 |
| r15 | true in substance | reachable only under an unstated scope; wrong as worded | F4 |
| r9 | **partly false**: one of the "two distinctive links" is already held as S165 | insufficient: firing it still leaves S292/S293 absent by the reason's own second clause | F1, F5 |

**3. Does refusing r9 lose its fetchClass link?** Yes — the **claim** is lost, not the source. `fetchClass`
is inside this round's pin at `Hyprland-Window.cpp:1502-1508` (`return m_xdgSurface->m_toplevel->m_state.appid;`,
`:1505`; the X11 branch returns the XWayland appid, `:1508`), but no `corpus/knowledge` text states the
class-is-app_id join: `grep -rn "fetchClass" corpus/ SKILL.md PROVINCE.md quality/ tools/` returns two
hits, both lessons (`round-43.md:79`, `round-44.md:65`). The r43 entry asserts the join as an INF
(`corpus/knowledge/hyprland-gkeep-geometry-r43.md:24`) citing no source, and the r44 entry asserts no
join at all (its only `application_id` is the census line, entry:58).

## Findings

### F1 — HIGH — r9: the refusal drops a pinned-link claim, and the ledger's coverage sentence is false
**Attacks** `corpus/lessons/round-44.md:65`, whose last quality column reads
"the successor covers the class-is-app_id link from a pinned file instead", and
`corpus/lessons/round-44.md:40`.

**Evidence.** r9 states the join and its limit: r9:26-31 (`fetchClass` → `m_state.appid`), r9:41-44
(`match:class` tested against the Wayland `app_id`), r9:69 ("never mentions `app_id` (0 occurrences in
the page)"), r9:80-86 (X11 branch). The r44 successor carries none of it: `grep -n "fetchClass\|app_id\|match:class\|class" corpus/knowledge/hyprland-gkeep-size-request-r44.md`
→ one hit, line 58, the census line. The join is therefore lost as a statement while its source is now a
pin — the reverse of the round-43 row that refused r9 because `fetchClass` was outside the pins
(`round-43.md:79`).

**Impacted axis.** coverage (C2's booked axis: a sourced claim leaves the corpus); calibration (a
decision row asserting coverage it does not have). Navigation count 61/61 is unaffected.

**Smallest safe correction.** Replace the `:65` clause with:
"…plus two round-9 lane receipts that do not exist here; the successor does not carry the
class-is-app_id link, whose source is the pinned `Window.cpp` at `:1502-:1508` (outside S164's frozen
locator cell, `corpus/SOURCES.md:176`)". If the L1 prefers to carry the claim instead, add one sentence
to entry §5 naming no cited id (so clause g stays quiet): "the compositor's class for a native Wayland
surface is the xdg app_id (`Hyprland-Window.cpp:1505`), and for an X11 surface the XWayland appid
(`:1508`)".

### F2 — MEDIUM — r13: "superseded by held S164" is true only of `onAck`; the ledger claims more
**Attacks** `corpus/lessons/round-44.md:37` ("its Window.cpp half is superseded by held S164") and
`corpus/lessons/round-44.md:62` ("its two `Window.cpp` sources (onAck, the map request log line) are
pinned here and are what the successor cites").

**Evidence.** The successor cites `onAck` (entry:38) and makes no log claim at all — `grep -rn "Map
request dispatched" corpus/knowledge/` → 0, and the entry contains no "log"/"journal"/"DEBUG" token. The
map line is in the same pin (`Hyprland-Window.cpp:2515`, `Map request dispatched, monitor {}, …`) and is
already attested in-lane by the round-43 oracle log
(`.ufo/waves/round-43/w1/ExecOracleGkeep/20-observation.txt:11`: `window size: [420.00000, 500.00000]`).
So the *claim* r13 §2 records is one citation away, not one journal sweep away; the flip named
(a host-journal sweep) restores r13 §3, not §2.

**Impacted axis.** coverage; calibration (a reason asserting a supersession the successor does not make).

**Smallest safe correction.** `:62` → "its `onAck` source (`Window.cpp:1514-1528`) is what the successor
cites; its map-request log line (`Window.cpp:2515`) is in the same pin and is attested in-lane by
`.ufo/waves/round-43/w1/ExecOracleGkeep/20-observation.txt:11`, which the successor does not cite". The
`:37` clause → "its `onAck` half is carried by the successor and its map-line half waits on a citation,
not on S320".

### F3 — MEDIUM/HIGH — r14: "carries the entire absence claim" is false, and the flip cannot cure it
**Attacks** `corpus/lessons/round-44.md:38`.

**Evidence.** r14 has exactly one source line (r14:9, S326). Its §2 carries a second absence claim with
no id and no locator: "The keys in its note records are exactly three — `body`, `created`, `id`"
(r14:45-46), generalised at r14:49-51 to "both now measured and both empty on this host". The sweep
receipt is absent from the lane, so §2 cannot be checked from it at all. Re-running the sweep as the flip
requires would leave §2 uncited — the file would still fail the refusal's own quality bar.

**Impacted axis.** coverage; calibration.

**Smallest safe correction.** `:38` → "reason=its absence claim rests on two grounds, one whole-journal
sweep at a package path outside this lane (S326) and an uncited gkeep note-store survey (its §2), neither
present in this lane's bytes; flip if the sweep is re-run and committed under this lane's receipts and
§2's note-store keys are committed as a receipt or struck".

### F4 — MEDIUM — r15: the flip's scope contradicts the lane's bytes
**Attacks** `corpus/lessons/round-44.md:39` ("flip if a lane-committed sweep over this lane's own
artifacts reproduces it").

**Evidence.** The reason itself is sound (r15:7 is its only source; the "never" over a corpus from one
sweep is the M43-9 class, as the ledger says). The flip is not: the package sweep's shape — 16 `.bin`
files — is reproduced exactly by `.ufo/waves/round-24/fetch/*.bin` (16 files) and a case-sensitive
`grep -c "gkeep"` over them returns 0 for every file (`flip-reachability.txt`), so the flip works **only**
at that scope. Over "this lane's own artifacts" it does not: `git grep -l "gkeep" HEAD -- .ufo/waves | wc -l`
→ 1529. A case-insensitive sweep of the same 16 files returns 5 (all `m_tagKeeper`/`TagKeeper`
substrings: `S155.bin:70`, `S156.bin:12`, `S157.bin:408`, `S158.bin:347`, `S161.bin:63`), so the flip
also has a built-in false positive that must be named.

**Impacted axis.** coverage; calibration.

**Smallest safe correction.** `:39` flip → "flip if a lane-committed, case-sensitive sweep of the same 16
`.bin` files in `.ufo/waves/round-24/fetch/` reproduces it".

### F5 — MEDIUM — r9: one of the "two distinctive links" is already held, so the flip is mis-specified
**Attacks** `corpus/lessons/round-44.md:40` ("its two distinctive links need the GTK default-size
documentation page and the window-rules wiki, neither pinned this round").

**Evidence.** The wiki half is false. r9's S287 (r9:11) quotes two things, both present in the lane's
held row S165 (`corpus/SOURCES.md:177`, receipt `.ufo/waves/round-24/fetch/S165.bin`):
"Resizes a floating window." (`S165.bin:82`) and "the _last_ match takes precedence" (`S165.bin:318`,
inside S165's declared range `315-342`). r9's S292 rule line (r9:39) is byte-identical to
`.ufo/waves/round-43/fetch/host-gkeep.conf:4`. The only link that is neither pinned nor held is S286
(`docs.gtk.org`). A flip requiring "both pages … get a row" would demand a second row for a document
already rowed (S165) — the duplicate-row form that closure item 2 in `corpus/lessons/round-44.md`
records as census E04 in the same scope and a W04 per row in another.

**Impacted axis.** coverage; calibration.

**Smallest safe correction.** `:40` → "reason=its GTK default-size page (`S286`) is neither pinned nor
held, its window-rules claims are already held as S165 (`.ufo/waves/round-24/fetch/S165.bin:82,318`) and
its S292 rule line is held as S295 (`.ufo/waves/round-43/fetch/host-gkeep.conf:4`), and its round-9
receipts are absent from this lane; flip if the GTK page is pinned and gets a row, S292 is re-grounded to
S295/S296, and its S293 log route is withdrawn".

### F6 — MEDIUM — the ADMIT's product: the entry calls a pinned answer "not among the pins"
**Attacks** `corpus/knowledge/hyprland-gkeep-size-request-r44.md:40` ("outside this entry's pins") and
`:79` ("not among the pins").

**Evidence.** Both lines say the post-ack commit behaviour is outside the pins, but the S164 pin
contains it: `commitWindow()` (`Hyprland-Window.cpp:2714`) clamps a floating, non-fullscreen xdg window
to the client's declared bounds on every commit —
`clampWindowSize(MINSIZE, MAXSIZE…` (`:2746`), with `layoutMinSize`/`layoutMaxSize`
(`Hyprland-XDGShell.cpp:467-483`) reading the client's `set_min_size`/`set_max_size`, which GTK sends at
`gdktoplevel-wayland.c:1333-1334`. This is the compositor-side half of the minimum channel r12 denied
(r12:52) and which `w1/CritAssimilation` §1 row 5 flagged; the entry carries the GTK half (entry §4) and
drops this one. The two "(not among the pins)" phrases are also imprecise: the file **is** the pin; the
specific comparison (buffer vs acked size) is what the file does not make.

**Impacted axis.** coverage (the C2 entry's own claim accuracy); calibration.

**Smallest safe correction.** Replace entry:79 with: "What Hyprland does when a client commits a buffer
whose size differs from the acked one: the pin compares the two nowhere, and on every commit a floating,
non-fullscreen window is clamped to the client's declared minimum and maximum
(`Hyprland-Window.cpp:2742-2747`; `Hyprland-XDGShell.cpp:467-483`)." Replace the parenthetical at
entry:40 with "(the pin compares the buffer with the acked size nowhere)". Both sentences name no cited
id, so clause g is not triggered; if the L1 instead names S164, the line must carry S164's Gate quote.

## What I verified and left alone

- S311→S164 and S312→S301 are byte-proven (`admit-bytes.txt`); the ADMIT's re-grounding claim is true.
- The three r12 sentences the entry says it corrects are exactly r12:31, r12:34-35, r12:52-53/59-62, and
  the entry's "What the staged predecessor said" bullets (entry:69,71,73) match them.
- Gate: five `GATE S…` lines; three quotes are raw substrings of their receipts and two span source lines
  (`xdg-shell.xml:1149-1153`, `gkeep-ui.py:475-476`) and match under whitespace normalisation
  (`gate-normalized.txt`; the S301 span is disclosed in the lesson).
- The four decisive receipts and r9's two package receipts are absent from this lane:
  `git ls-tree -r --name-only HEAD | grep -c '^lanes/'` → 0, and no `round-9` wave dir exists.
- The scope calls ("in") for r12/r13/r14/r15/r9 are consistent with the upstream-code/app-source ground;
  no scope defect found.
- I did not execute either counter; the receipts are read, not re-run.

## Open predicate defect (no re-registration after data)

`PRED-C2-r44-v2` clause i scores the decisions' **shape** only — one `ADMIT`, ≥1 `REFUSE … reason=` of
≥4 distinct words with a flip word (counter docstring `:52-55`) — and the ledger rows are never read: the
counter scans only `section(lesson, "## Gate")` (`quality/counters/c2-r44-gkeep-size-request-v2.py:467`).
Every defect above therefore passes the counter at `e4678921`: a reason may name coverage the successor
does not have (F1), a supersession it does not make (F2), an "entire claim" a second section carries
(F3), and a flip whose test contradicts the lane's bytes (F4). This is M44-1's class in the other
direction — M44-1 taught the ADMIT to cite the successor's receipts, not to check what each REFUSE says
about it. Candidate criterion for the next registration: cross-check every REFUSE/ledger clause that
asserts coverage or a flip against the successor's bytes and the held rows. No re-registration now.

## Seat state

- Receipts (seat dir `.ufo/waves/round-44/w2/CritAssimV2/`): `quote-check.py`, `quote-check.txt` (33/33),
  `gate-and-pin-checks.txt`, `gate-normalized.txt`, `admit-bytes.txt`, `base-ground.txt`,
  `pin-readings.txt`, `clamp.txt`, `entry-unk-check.txt`, `entry-and-r12-locators.txt`, `axes-and-final.txt`, `landed-locators.txt`,
  `residue-locators.txt`, `residue-line-numbers.txt`, `residue-quotes.txt`, `r9-held-ground.txt`,
  `s165-precedence.txt`, `map-line-in-lane.txt`, `flip-reachability.txt`, `round24-sweep-check.txt`,
  `r15-counterexample.txt`, `sources-rows.txt`, `final-checks.txt`.
- Tools installed: **none**. Scratch `/fast/scratch/hyaku/mado-r44/CritAssimV2/` created, nothing written,
  removed before this report; every cited receipt is in the seat dir.
- No write outside the seat dir; no git/jj mutation (read-only `ls-tree`, `grep`, `show`, `diff`,
  and one read-only `git -C ~/Projects/gkeep show`); no compositor or host-service call.
