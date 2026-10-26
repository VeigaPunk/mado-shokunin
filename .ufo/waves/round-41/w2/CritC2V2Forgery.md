# CritC2V2Forgery — w2 (FALSIFY) — forgeries against PRED-C2-r41-v2

Lane `mado-shokunin`, round 41 wave w2. Full detail, diffs and run logs:
`.ufo/waves/round-41/w2/CritC2V2Forgery/forgeries.md` (+ `forge.py`,
`realseed.py`, `quoteaudit.py`, `dump.py`, `*-run.txt`, `forged-artifacts.txt`,
`pinall-harm.txt`).

**Scored with** `git show 07f2641:quality/counters/c2-r41-focus-entry-v2.py`
(sha256 `a2226deb860230111b8835a4a76db69d3186c5f85ad7c67cbec972ea2ef6438c`).
Ten receipts re-hashed = `PINS` = working tree. Baselines: the frozen counter on
the lane at `07f2641` → `admitted=1/1 verdict=TARGET_MET` rc 0; the control's own
genuine fixture → `1/1`; the real-seeded fixture (real DATA tree, no forgery) →
`1/1`.

## Verdict

- **The claim at its registered strength holds:** the landed entry is admitted,
  `1/1`, at the DATA commit. I found no forgery that makes the counter *reject*
  the real data — every attack is an attack on what admission *means*.
- **10 of 10 real-seeded forgeries are admitted** (`admitted=1/1`), covering all
  seven shapes the task named plus three more. Two of them are removable at zero
  data cost (T4); one data defect (D1) should be fixed before the round lands.

## D1 — DATA defect, fix before landing: the protocol request count is wrong

`corpus/knowledge/hyprland-focus-grab-r41.md:115` (the §6 decision table):

> `| What can a client ask for? | S283: two interfaces, five requests, one event (§1) | OBS |`

The pinned XML has **six** `<request>` elements and one `<event>`:

```
$ grep -c '<request name=' .ufo/waves/round-41/fetch/focus-grab-v1.xml   → 6
$ grep -o '<request name="[a-z_]*"' …  → create_grab, destroy, add_surface,
                                         remove_surface, commit, destroy
$ grep -c '<event name=' …              → 1
```

The entry contradicts itself: its own §1 table (entry:25-31) lists **six**
request rows and entry:21 says "the manager has exactly two requests" plus a
grab with four. The same error sits at a second site, `corpus/SOURCES.md:232`,
scope cell: "The two interfaces, four requests and one event that define a focus
grab".

**Fix (two tokens):** entry:115 `five` → `six`; `SOURCES.md:232`
`four requests` → `six requests` (or scope that cell explicitly to
`hyprland_focus_grab_v1`, which is the only interface with four). No predicate
reads a count, so nothing else follows.

## Predicate open defects (report, do not re-register)

All ten real-seeded forgeries are `admitted=1/1` under the frozen counter; the
synthetic set agrees. Column "catcher" = the clause that *should* see it.

| # | forgery, and what it attacks | catcher | tightening |
|---|---|---|---|
| RA | entry:19 — a quote from the protocol XML re-labelled as Hyprland 0.56.2's seat behaviour | none (clause g = token presence) | none non-forgeable |
| RB | entry:69 — S286's real log-call quote on "the portal binds the focus-grab manager" (refuted by `grep -in focus xdph-PortalManager.cpp` → rc 1) | none | none non-forgeable |
| RC | `SOURCES.md:232-233` + lesson:25-26 + entry:19,43 — S283/S284 swap receipts, locations, quotes; the entry is then self-contradictory (entry:21 still calls S283 the manager) | none; clause e's binding moves with the swap | partial T1 |
| RC2 | same swap, `source:` prose swapped too (internally consistent) | none | **none** — needs an external id authority |
| RD | lesson:34 — `ADMIT … focus-grab-mouse-target-r11.md`, a staged file the entry never assimilates (entry:15 names r14/r28) | clause i (STAGED membership only) | T2 (needs one fixture line) |
| RE | entry:110-199 — 90 invented uncited lines; the 9 checked lines untouched (genuine entry: 9 of 136 lines checked = 6.6 %; forged: 9 of 226 = 4.0 %) | none (no volume/ratio clause) | none (T5 harms) |
| RF | lesson:32 + entry:73 — S037's receipt replaced by a Japanese localized document while the row keeps its neutral GitHub URL | clause i BAD_LOC (rows only) + clause d (held not pinned) | **T4: exact, kills it** |
| RG | lesson:32 + entry:73 — S037's receipt **invented** ("the portal binds … for every client") | clause d (held ids exempt from PINS) | **T4: exact, kills it** |
| RH | entry:63 — the pinned journal cited for "both sessions advertise … once each"; the journal has one advert, line 117, pid 1952 | clause h (census line only) | none non-forgeable |
| RG2 | entry:111 — invented citation `S999a` (no word boundary after the digits) | clause b ghost scan | cheap widening |

RA/RB/RH are the declared quote-to-claim residual, measured rather than
asserted. RF/RG are the declared held-id residual — and they are **removable
now**, see T4. RC/RC2 are an undeclared identity hole.

## Tightenings, priced against the genuine artifacts

- **T4 — pin every cited receipt (the actionable one).** Remove clause d's
  `if i in new_ids:` guard and add the held receipt to `PINS`
  (`xdph-installed-version.txt` = `4294737aa884fd84c2e2a6bf642efa71c281bc480df4f07eb64009d812157ea8`,
  already committed pre-data; its `desc` sha256 `7bf2f8be…` verifies against the
  host file). Measured: `P-real-seed admitted=1/1`; `RF` and `RG`
  `admitted=0/1 clauses=… d:0 g:0`; and the patched counter against the real
  lane at `07f2641` still `admitted=1/1 verdict=TARGET_MET` (`pinall-harm.txt`,
  patched sha `90b1f5db…`). **Zero cost on this round's data.** It is a
  predicate change, so it is a v3 item, not a post-data patch.
- **T2 — bind ADMIT to the entry's own provenance:** every `ADMIT` path must
  occur in the entry's `assimilated-from:` line. Real seed bound; RD unbound.
  Cost: the frozen control fixture has no `assimilated-from:` line, so T2 also
  rejects the exemplar (one line added there).
- **T1 — bind `source:` prose to the receipt:** each `source: S### - text` line
  must contain its receipt basename or its location's last component. Real
  entry 0 failing; RC 2 failing; **RC2 defeats it**; the control fixture fails
  all 8 (terse prose). Partial.
- **T3 — localized receipts.** `BAD_LOC` cannot be moved onto receipt bytes:
  `/ja` occurs in the genuine `issue-565.html`
  (`…/assets/ja9-b94de714266ba389.js`) and would reject S287. A **CJK-range
  scan** works: real receipts 0 failing, RF 134 code points → rejected.
  Heuristic, not exact.
- **T5 — citation per paragraph (rejected):** 7 paragraphs of the real entry
  carry no id (entry:57, 67, 79, 93, 107, 109, 130). It would reject the landed
  data.
- **T-ghost — widen to `[Ss]\d{3,}[A-Za-z0-9_]*`:** real entry and control
  fixture 0 extra tokens, RG2 caught. Cheap, partial (`S 999` evades).

## No defect found (checks that held, with the command that ran them)

1. **Quote attribution, systematic** (`quoteaudit.py`, the counter's own
   normalizers): 36 quoted spans on entry lines — **31** in a cited receipt of
   their own line's id, **0** misattributed source quotes. The other 5 are the
   entry's own scare-quotes (entry:51 "grab active, nothing committed";
   entry:130; entry:132) and entry:39's two XML terms, which that line
   attributes to "The XML" explicitly.
2. **Pins on new ids:** invented receipt for S283, S283's Gate quote taken from
   S284's receipt, S283's receipt overwritten with S284's bytes → all
   `admitted=0/1 … d:0`.
3. **Census arithmetic:** `adverts=78` → `79` → `admitted=0/1 … h:0`. A cited
   id with no row (`S291`) → `admitted=0/1 … b:0 c:0 d:0 g:0 h:0`.
4. **Journal prose claims** (entry:61-67) all hold: 15 adverts pid 1918 opening
   `2026-10-25T13:16:45-03:00`, 63 in pid 1952, 63 distinct names, boot marker
   line 78, "Stopped Portal service" line 76, "Gathering exported interfaces"
   after "XDG_CURRENT_DESKTOP set to Hyprland" lines 82-83.
5. **Portal claims:** `grep -in focus xdph-PortalManager.cpp` rc 1; `grep -ic
   focus xdph-journal.txt` → 1; ten `INTERFACE ==` branches, nine binds — so
   entry:69's "ten named branches" and `SOURCES.md:235`'s "nine it binds" are
   both right.
6. **Host claims:** `hyprctl version` → `Hyprland 0.56.2 built from branch
   v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f` (entry:77);
   `git grep -lEi 'focus_grab|focus-grab|focus grab' ab2bfaa -- corpus
   PROVINCE.md SKILL.md tools` rc 1 (entry:109).

## Observations (not defects)

- **O1** entry:73's S037 Gate quote `"%NAME% xdg-desktop-portal-hyprland
  %VERSION% 1.4.1-2"` is a whitespace-collapsed rendering of the `desc` fields,
  not a literal line; clause d's declared normalization allows it. Rendering it
  as `%NAME%: xdg-desktop-portal-hyprland, %VERSION%: 1.4.1-2` keeps it inside
  the 3-25 word rule and stops a reader taking it for a literal.
- **O2** the held receipt is a 1442 B seat-authored shell transcript (`$ ls -d`,
  `$ sha256sum`, `$ cat`), not the raw `desc`. Its claimed `desc` sha256
  `7bf2f8be…` verifies against the host file, so it is honest — but clause d's
  "a saved journal, not a tool's report" rule has no held-id counterpart;
  pinning (T4) makes the bytes immutable without making them raw.

## Seat hygiene

- Wrote only `.ufo/waves/round-41/w2/CritC2V2Forgery/` and this report;
  `git status --porcelain` shows no tracked file touched. Fixture repos were
  `mktemp -d` + `git init -q`, all calls `-C`, identity via `-c`, toplevel
  checked by the control's own `commit_all`; scratch removed.
- Host safety: read-only `git show`/`git grep`/`git status`; one `hyprctl
  version`; read-only file reads of `/var/lib/pacman/local/…/desc`; no pacman,
  no installs, no journal verbs, no compositor/Wayland connection.
- Tooling: python3 stdlib + git only; nothing installed.
