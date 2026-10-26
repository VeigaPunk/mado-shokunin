# CritC2V2Forgery — forgeries against PRED-C2-r41-v2 (w2, FALSIFY)

Seat: `CritC2V2Forgery`, round 41 wave w2. Lane `mado-shokunin`.
Everything below is a run, not a reading. Seat dir:
`.ufo/waves/round-41/w2/CritC2V2Forgery/` (`forge.py`, `realseed.py`,
`quoteaudit.py`, `dump.py`, `forge-run.txt`, `realseed-run.txt`,
`tighten-run.txt`, `quoteaudit-run.txt`, `forged-artifacts.txt`).

## What was scored, and with what

- **Counter:** `git show 07f2641:quality/counters/c2-r41-focus-entry-v2.py`,
  sha256 `a2226deb860230111b8835a4a76db69d3186c5f85ad7c67cbec972ea2ef6438c`.
  Run as `python3 -I <copy> --repo <fixture> --rev <after> --base <base>`.
- **Receipts:** the ten files under `.ufo/waves/round-41/fetch/` at the DATA
  commit; every one re-hashed and equal to the counter's `PINS`
  (`Hyprland-FocusGrab.cpp 53b762f7…`, `focus-grab-v1.xml 0bc60c14…`,
  `xdph-journal.txt bf8fa91a…`, …) and to the working tree.
- **Two fixture sets, same construction as `.ufo/waves/round-41/ctl/run-c2-v2-controls.py`**
  (`mktemp -d`, `git init -q`, every call `-C D`, throwaway identity via `-c`,
  toplevel verified by the control's own `commit_all`):
  1. **synthetic** (`forge.py`): the control module is imported read-only and
     its genuine fixture `admitted()` is the starting point — 10 forgeries.
  2. **real-seeded** (`realseed.py`): base = `ab2bfaa`'s `corpus/SOURCES.md`
     + `corpus/README.md`; after = the **real DATA tree** (entry, registry,
     lesson, README, all ten receipts) with **exactly one forgery** applied —
     10 forgeries. This is the set the findings below cite, because it attacks
     the landed bytes rather than a stand-in.
- **Baselines:** `P-genuine` (synthetic) `admitted=1/1`; `P-real-seed`
  `admitted=1/1`; the frozen counter run directly against the lane repo at
  `07f2641` also `admitted=1/1 verdict=TARGET_MET`, rc 0.

The frozen predicate admits the landed data. Nothing here changes that; the
findings bound **what admission means**.

## Result: 10 of 10 real-seeded forgeries are admitted

| # | forgery (what it attacks) | frozen counter | clause that should catch it | tightening |
|---|---|---|---|---|
| RA | entry:19 — a quote from the protocol XML re-labelled as Hyprland 0.56.2's seat behaviour | **ADMITTED** | none; clause g tests token presence only | none non-forgeable (declared residual) |
| RB | entry:69 — S286's real log-call quote on the inference "the portal binds the focus-grab manager" | **ADMITTED** | none | none non-forgeable (declared residual) |
| RC | `SOURCES.md:232-233` + lesson:25-26 + entry:19,43 — S283 and S284 swap receipts, locations and quotes (id swap) | **ADMITTED** | none; clause e's binding moves with the swap | partial: T1 (catches the naive swap only) |
| RC2 | as RC, with the `source:` prose swapped too (internally consistent id swap) | **ADMITTED** | none | **none** — needs an external id authority |
| RD | lesson:34 — `ADMIT … focus-grab-mouse-target-r11.md`, a staged file the entry never assimilates | **ADMITTED** | clause i (STAGED membership only) | T2 (needs one line in the fixture) |
| RE | entry:110-199 — 90 invented uncited lines; the 9 mechanically checked lines are unchanged | **ADMITTED** | none (no volume/ratio clause) | none (T5 harms the real entry) |
| RF | lesson:32 (GATE S037) + entry:73 — S037's receipt replaced by a Japanese localized document; the row keeps its neutral GitHub URL | **ADMITTED** | clause i BAD_LOC (rows only) + clause d (held not pinned) | **T4 (pin-all): exact, kills it** |
| RG | lesson:32 (GATE S037) + entry:73 — S037's receipt **invented** ("the portal binds … for every client") | **ADMITTED** | clause d (held ids are not pinned) | **T4 (pin-all): exact, kills it** |
| RH | entry:63 — the pinned journal cited for "both portal sessions advertise … once each"; the journal says one advert, line 117, pid 1952 | **ADMITTED** | clause h (census line only) | none non-forgeable |
| RG2 | entry:111 — an invented citation `S999a` in plain sight | **ADMITTED** | clause b ghost scan | cheap: widen the token to `[Ss]\d{3,}\w*` |

Synthetic set: the same ten, all `admitted=1/1` (`forge-run.txt`), plus the
three negatives below.

## Per-forgery detail (real-seeded; diff in `forged-artifacts.txt`)

**RA — XML quote as compositor behaviour.** Entry:19 becomes
`**OBS** S283 (Hyprland 0.56.2's seat enforcement, measured this round): "This
interface restricts input focus to a specified whitelist of surfaces" …`. The
quote is genuinely in S283's receipt, so clauses d and g pass; nothing in a–i
reads the claim. `PRED-C2-r41-v2: admitted=1/1 verdict=TARGET_MET`. This is the
residual the docstring names ("a real receipt can be cited for a claim it does
not support"). **No non-forgeable tightening:** any mechanical proxy (a keyword
before the quote, a file-type-to-verb table) is defeated by rewording the claim
while keeping the same quote.

**RB — true quote, false inference.** Entry:69 becomes "the portal binds the
focus-grab manager and hands it to every client, logging it first with
`Debug::log(LOG, " | Got interface: {} (ver {})", INTERFACE, version);`" — the
receipt at `xdph-PortalManager.cpp:85-88` says the opposite of the inference
(the string is logged before any branch, and `grep -in focus
xdph-PortalManager.cpp` exits 1). Admitted. Same residual, no tightening.

**RC — id swap.** `S283` takes the `FocusGrab.cpp` URL, receipt, quote and
entry line; `S284` takes the XML's. Clause e still holds because the location's
last component and the receipt name move together (`focusgrab.cpp` ⊆
`hyprland-focusgrab.cpp`; `focus-grab-v1.xml` ⊆ `hyprland-focus-grab-v1.xml`),
clause d holds because each quote is in its new receipt, clause g holds because
each line carries its new quote. The forged entry is **self-contradictory** —
entry:19 now says S283 is `CFocusGrab::CFocusGrab` while entry:21 (untouched)
still says "**OBS** S283 (`hyprland_focus_grab_manager_v1`, version 1): the
manager has exactly two requests" — and the counter cannot see it: clause g
needs *one* line per id. `admitted=1/1`.
*Partial tightening T1:* require each `source: S### - <text>` header line to
contain the id's receipt basename or its location's last path component. On the
real seed: genuine **0 failing**, RC **2 failing** (S283 prose says
"hyprland-protocols focus-grab-v1.xml", receipt is `Hyprland-FocusGrab.cpp`).
**RC2 defeats it** (0 failing) because the attacker renames consistently. T1
also fails all 8 lines of the frozen control fixture (its `source:` prose is
terse: "protocol xml", "compositor"), so it is a v3 change, not a v2 patch.

**RD — ADMIT for the wrong staged file.** Lesson:34 becomes `ADMIT
merge/mado/knowledge/corpus/knowledge/focus-grab-mouse-target-r11.md as
corpus/knowledge/hyprland-focus-grab-r41.md` while the entry's own provenance
line (entry:15) names `focus-grab-protocol-live-on-host-r14.md` and
`focus-control-surfaces-r28.md`. Clause i checks only that the path is in
STAGED, that the target is this entry and that the REFUSE target differs —
all true. `admitted=1/1`.
*Tightening T2:* every `ADMIT` path must occur in the entry's
`assimilated-from:` line. Real seed **bound=True**; RD **bound=False**. The
cost is honest and small: the frozen control fixture has no `assimilated-from:`
line, so T2 also rejects it (`bound=False`) — one line added to the fixture,
i.e. a v3 change.

**RE — 90 % prose.** 90 uncited lines inserted at entry:110. Of the genuine
entry's 136 unfenced lines the counter mechanically checks **9** (the eight
Gate-quote lines + the census line) = **6.6 %**; after the forgery it checks 9
of 226 = **4.0 %**. `admitted=1/1`.
*Tightening T5 (priced, rejected):* "every prose paragraph must cite an id"
fails on the real entry — **7 paragraphs** carry no `S###`: entry:57, 67, 79,
93, 107, 109 and 130 (the §7 bullet). It would reject the landed data.

**RF — localized material re-hosted under a neutral URL.** S037's row keeps
`https://github.com/hyprwm/xdg-desktop-portal-hyprland/releases/tag/v1.4.1`;
the receipt bytes become a Japanese article whose quotable line is
`フォーカス グラブ ホワイトリスト は 独自 の プロトコル です` (3+ whitespace
tokens, so the 3–25 word rule passes). `BAD_LOC` is applied to **rows only**
(`for j … row_text`), so clause i is blind; the row is neutral. `admitted=1/1`.
*Why the marker list cannot simply be moved to receipt bytes:* `BAD_LOC`
contains `/ja`, and the genuine `issue-565.html` receipt contains
`https://github.githubassets.com/assets/ja9-b94de714266ba389.js` — applying the
list to receipt text would reject the real S287 receipt (`tighten-run.txt`
`T3 … failing=1 [('S287', ['/ja'], 0)]`).
*Tightening that does work:* a **CJK-range scan** of receipt text. Real
receipts: **0 failing** (S287 has 0 CJK code points); RF: **134** → rejected.
It is a heuristic (base64 or romanized text evades), but it is cheap and
harmless.

**RG — fabricated held receipt.** S037's receipt replaced by invented release
notes containing "the portal binds hyprland_focus_grab_manager_v1 for every
client", the entry quoting it, the Gate line re-sha'd. Held ids are exempt from
`PINS` (`if i in new_ids:` in clause d), so any 512-byte file passes.
`admitted=1/1`. Note the control fixture's own "genuine" S050 receipt is
already built this way (`ctl/run-c2-v2-controls.py:108` renders it from
`FILLER`), and control P is expected to score 1/1.
*Tightening T4 (exact, zero data cost):* drop clause d's held-id exemption and
add the held receipt to `PINS` — the L1 already committed it before the data
(`xdph-installed-version.txt`, 1442 B, `4294737a…`; its `desc` sha256
`7bf2f8be…` verifies against the host file). Measured with a patched counter
(guard removed + one PINS entry):
`P-real-seed admitted=1/1`, `RF admitted=0/1 clauses=… d:0 g:0`,
`RG admitted=0/1 clauses=… d:0 g:0`; and the patched counter against the lane
repo at `07f2641` still reads `admitted=1/1 verdict=TARGET_MET`
(`pinall-harm.txt`; patched counter sha256 `90b1f5db…`). **This is the
one finding that is both fatal and removable at zero cost** — but it is a
predicate change, so it cannot land after the data commit (no third
registration); it is an open defect of v2.

**RH — pinned journal, unsupported claim.** A line is added at entry:63 saying
both sessions advertise the interface once each. The pinned receipt refutes it:
`grep -n hyprland_focus_grab_manager_v1 xdph-journal.txt` → one hit, line 117,
pid 1952; the 1918 session has 15 adverts and none is the grab. Clause h checks
only the census line's arithmetic. `admitted=1/1`. **No tightening:** any rule
that cross-checks entry prose against the journal must parse prose; the census
line is the only machine-checkable projection of the journal, and the entry
legitimately discusses both sessions in prose (entry:65,67).

**RG2 — ghost token.** `**OBS** S999a the seat manager forwards pointer motion
…` is admitted: the ghost scan is `\b[Ss]\d{3,}\b`, and `S999a` has no word
boundary after the digits, so the token is invisible to clause b and to clause
g. *Tightening:* `[Ss]\d{3,}[A-Za-z0-9_]*` — real entry **0 extra tokens**,
control fixture **0**, RG2 **1** (`S999a`). Cheap and harmless; partial
(`S 999` still evades).

## Data findings (defects fixed before the round lands)

**D1 — the decision table miscounts the protocol's requests.**
`corpus/knowledge/hyprland-focus-grab-r41.md:115` reads

> `| What can a client ask for? | S283: two interfaces, five requests, one event (§1) | OBS |`

The pinned XML has **six** `<request>` elements and **one** `<event>`:

```
$ grep -c '<request name=' .ufo/waves/round-41/fetch/focus-grab-v1.xml   → 6
$ grep -o '<request name="[a-z_]*"' …  → create_grab, destroy, add_surface,
                                         remove_surface, commit, destroy
$ grep -c '<event name=' …              → 1  (cleared)
```

The entry contradicts itself: its own §1 table (entry:25-31) lists six request
rows, and entry:21 says "the manager has exactly two requests" plus a grab with
four. The registry row has the same error at a second site —
`corpus/SOURCES.md:232`, scope cell: "The two interfaces, four requests and one
event that define a focus grab". **Fix:** entry:115 "five" → "six";
`SOURCES.md:232` "four requests" → "six requests" (or scope it explicitly to
`hyprland_focus_grab_v1`, which is the only interface that has four).
Severity: factual, quoted against a pinned receipt, one token in each of two
files. No predicate reads a count, so no predicate change follows.

## Observations on the data (not defects, but worth the L1's eye)

- **O1 — S037's Gate quote is a rendering, not a line.** Entry:73 quotes
  `"%NAME% xdg-desktop-portal-hyprland %VERSION% 1.4.1-2"`. The receipt holds
  the pacman `desc` fields on separate lines (`%NAME%` / value / `%VERSION%` /
  value); the counter's whitespace collapse (declared for non-HTML receipts)
  makes the rendering match. The claim is true; a reader cannot tell the quote
  is joined. Cheap repair: render it as `%NAME%: xdg-desktop-portal-hyprland,
  %VERSION%: 1.4.1-2` (still inside 3–25 words, still present after collapse).
- **O2 — the held receipt is a seat transcript.** `xdph-installed-version.txt`
  is 1442 B of shell transcript (`$ ls -d …`, `$ sha256sum …`, `$ cat …`)
  authored by seat `ScrEntryA`, not the raw `desc`. Its claimed sha256
  `7bf2f8be…` verifies against `/var/lib/pacman/local/xdg-desktop-portal-hyprland-1.4.1-2/desc`
  (read-only), so the transcript is honest here. But clause d's own-work rule
  ("a saved journal, not a tool's report") has no counterpart for held ids;
  pinning (T4) makes the bytes immutable without making them raw.

## No defect found (checks that held, with the command that ran them)

1. **Quote attribution, systematic.** `quoteaudit.py`: every double-quoted
   span on every unfenced entry line checked against the normalized text of the
   receipts its Gate lines bind, using the counter's own normalizers. 36 spans:
   **31** in a cited receipt of their own line's id; **0** misattributed source
   quotes. The 5 others are the entry's own scare-quotes — entry:51 "grab
   active, nothing committed", entry:130 "a grab works on this host", entry:132
   "the rule layer decides focus and can be wrong" — and entry:39's
   `"implementation-defined criteria"` / `"similar action"`, which that line
   explicitly attributes to "The XML" ("The XML enumerates neither, and S284 is
   read below …"). The 31 include every line-wrapped claim that line-based grep
   misses (`if (anyCommitted) start(); else finish(true);`, `if
   (g_pSeatManager->m_seatGrab == m_grab) …`, the three XML sentences, the
   README sentence): all present after the counter's normalization.
2. **Pins bind new ids.** `NF1` invented receipt for S283, `NF2` S283's Gate
   quote taken from S284's receipt, `NF3` S283's receipt overwritten with S284's bytes and quote (pin + quote exclusivity) — all
   `admitted=0/1 clauses=… d:0`. (`forge-run.txt`.)
3. **Census arithmetic.** `RN1` (`adverts=78` → `79`) → `admitted=0/1 … h:0`.
4. **Cited id with no row.** `RN2` (`S289` → `S291` in a `source:` line) →
   `admitted=0/1 … b:0 c:0 d:0 g:0 h:0`.
5. **Journal prose claims verified** against the pinned receipt: 15 adverts in
   pid 1918 (opening `2026-10-25T13:16:45-03:00`), 63 in pid 1952, 63 distinct
   names in the latest session, boot marker at line 78, "Stopped Portal service
   (Hyprland implementation)." at line 76, "Gathering exported interfaces"
   after "XDG_CURRENT_DESKTOP set to Hyprland" at lines 82-83 — every number in
   entry:61-67 holds.
6. **Portal claims:** `grep -in focus xdph-PortalManager.cpp` → rc 1 (no hit);
   `grep -ic focus xdph-journal.txt` → 1; ten `INTERFACE ==` branches and nine
   binds — entry:69's "ten named branches" and `SOURCES.md:235`'s "nine it
   binds" are both right.
7. **Host claims:** `hyprctl version` → `Hyprland 0.56.2 built from branch
   v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f`, matching
   entry:77; `git grep -lEi 'focus_grab|focus-grab|focus grab'
   ab2bfaa -- corpus PROVINCE.md SKILL.md tools` → rc 1, matching entry:109.

## Verdict

- The frozen predicate's claim at its registered strength — the entry is
  admitted, `1/1`, at the DATA commit — **holds**; I could not make it reject
  the landed data.
- Admission is weaker than "sourced". Ten forgeries are admitted, covering all
  seven shapes the task named. Three of them (RA, RB, RH) are the declared
  quote-to-claim residual; two (RF, RG) are the declared held-id residual and
  are **removable now at zero data cost** by T4; one (RE) is the same residual
  at scale; RC/RC2 are an undeclared identity hole with no non-forgeable fix;
  RD needs T2 plus one fixture line; RG2 has a cheap partial fix.
- Nothing here is a reason to reject the DATA except **D1** (two one-token
  fixes). The predicate findings are **open defects of PRED-C2-r41-v2**, to be
  reported, not re-registered (no third registration after data).
