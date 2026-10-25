# ScoutMergeRest — the rest of the `merge/mado/` package, surveyed for the next round

Seat: `ScoutMergeRest` · round 40, wave `w1` · **read-only survey** (no lane file touched; no
claim verdict stated by this seat) · date 2026-10-25.

**Question answered:** of the knowledge entries the shokunown package
`/home/vgpnk/Projects/shokuknow/merge/mado/` proposes, which are *not yet adopted* by the lane,
what are they, grouped by theme, what does `PROVINCE.md` say about each theme, and which theme
should the **next** round take?

Every finding below names what it attacks or supports (a path, a command and its output, or a
hash). Nothing here was inferred from a package claim without re-derivation.

---

## 1. Package census (measured, not read off the report)

| item | count | how measured |
|---|---|---|
| new-file knowledge entries | **65** | `ls /home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/*.md \| wc -l` → 65 |
| amendment files (targets the lane already holds) | **4** | `ls …/amendments/corpus/knowledge/*.md \| wc -l` → 4 |
| staged registry rows | **147** | regex `^\|\s*(S\d+)\s*\|` over `merge/mado/SOURCES.append.md` → 147 rows, ids S203–S349 |
| lane registry rows today | **214** | `grep -cE '^\|\s*S[0-9]+\s*\|' corpus/SOURCES.md` → 214; max id **S277** |
| staged ids that collide with a held lane id | **22** | `lane_ids ∩ staged_ids` → 22 (S203–S221, S253, S258, S277) |
| documents staged **twice or more** inside the package | **15** | URL-keyed duplicate scan of `SOURCES.append.md` (e.g. focus-grab XML under S229/S274/S294; arXiv 2604.18860 under S218/S280/S325; `gkeep/ui.py` under S255/S285/S312) |

`MERGE-REPORT.md` is accurate on the entry count (its table lists 69 = 65 + 4) but **stale on the
registry**: it says "lane registry currently holds **192** rows; first staged id is S203". The lane
holds **214** rows today and its ids run to **S277**. Consequence for any next round: the package's
id space is round-scoped and its documents are staged several times, so rows must be adopted
**by document under lane ids**, never appended wholesale.

**Defect in the merge report itself:** its "Rows whose source the lane's registry already holds"
table lists 8 rows but omits one — staged **S214** ≡ lane **S212** (both "Waybar 0.15.0 Hyprland
workspaces module", same URL, `SOURCES.append.md:18` vs `corpus/SOURCES.md:214`).

---

## 2. What the lane already holds of the package

- **7 of the 65** new-file entries share a filename with a lane-held entry (so a bulk copy would
  clobber lane text): `event-delivery-limits-r26.md`, `hyprctl-flags-r28.md`,
  `idle-lock-chain-armed-r14.md`, `idle-lock-never-asked-r12.md`, `idle-lock-offered-in-the-bar-r15.md`,
  `request-limits-upstream-r31.md`, `request-socket-live-bound-r8.md`. The lane's own versions are
  later and lane-authored (rounds 35–38) — e.g. `corpus/knowledge/idle-lock-chain-armed-r14.md`
  "Opened 2026-10-24 … hypridle runs as pid 1667".
- **58** entries are absent from `corpus/knowledge/` by name.
- Of those 58, **8 already carry a lane refusal verdict** in `corpus/lessons/`:
  `chinese-article-revision-r30` (r35 spot-check :171), `chinese-wiki-canonical-url-r28` and
  `zh-wiki-snapshot-semantics-r29` (r36 channel rule), `two-literature-drift-r26` (r32/33/34),
  `event-queue-host-measurement-r28` and `event-queue-journal-measurement-r29` (r37/r38),
  `socket-client-contract-measurements-r29` and `socket-modes-and-request-read-r30` (r38).
- **50 entries therefore carry no lane verdict at all** — that is the real "rest of the package".
- The **4 amendments**: `dispatcher-surface-and-request-grammar-r26.md` was adopted re-grounded in
  round 39 (`corpus/lessons/round-39.md` §Assimilation ledger); the other three were refused in
  round 38 — `ipc-contract-r25` and `dispatcher-semantics-r25` (no new ground vs. the lane's own
  files), `waybar-module-text-route-r25` (refuse as written: wrong anchors). I re-verified that
  refusal today against upstream Waybar 0.15.0: the fallback warning is at `backend.cpp:38`
  (amendment says `:31`), the 1024-byte buffer at `backend.cpp:115` (says `:88`), the `>` split at
  `backend.cpp:142` (says `:140`), and the window module registers **five** events at
  `window.cpp:27-31` (amendment claims two at `:25-26`).

---

## 3. The 50 un-adjudicated entries, grouped by theme

Counts are of the 50 entries with no lane verdict; the 8 refused ones are noted inside the themes.

### Theme A — Compositor focus mediation (the focus-grab protocol) — 13 entries
`focus-grab-seat-semantics-r8.md`, `focus-grab-observed-semantics-r9.md`,
`focus-grab-focus-selection-r10.md`, `focus-grab-mouse-target-r11.md`,
`focus-grab-whitelist-admission-r12.md`, `focus-grab-keyboard-routing-r13.md`,
`focus-grab-protocol-live-on-host-r14.md`, `focus-grab-has-no-client-here-r15.md`,
`focus-control-surfaces-r28.md`, `compositor-focus-manipulation-literature-r26.md`,
`privileged-client-surface-r29.md`, `wayland-input-security-literature-r8.md`,
`upstream-input-holds-and-the-lock-screen-r16.md` — 32 staged rows (S218, S227, S229, S230, S244,
S273–S275, S278–S280, S288, S293–S296, S306–S308, S313, S314, S317, S323–S325, S328–S332, S338, S349).

**PROVINCE verdict: IN, by analogy to the entries the lane already admits (`ipc-contract-r25.md`,
`wayland-protocol-boundaries-r13.md`): source-read knowledge of the compositor's own protocol at the
host's tag, read-only, never a mutation — but the two localized-channel rows must be dropped
(`S230` amgsk.dev, `S323` lightning-assist: "any documentation written in a localized channel" is
outside the province, PROVINCE.md round-36 refinement) and the host receipts must be re-taken
in-lane (see §5).**

### Theme B — Chinese/Japanese documentation channel — 11 un-adjudicated + 4 already refused
`chinese-hyprland-window-rules-r16.md`, `chinese-ipc-framing-absence-r13.md`,
`chinese-translation-drift-r31.md`, `chinese-wiki-ipc-section-r7.md`,
`chinese-wiki-revision-list-r7.md`, `cn-framing-coverage-r8.md`,
`japanese-counted-comparison-gone-r15.md`, `japanese-input-observation-methods-r14.md`,
`japanese-wayland-compositor-account-r16.md`, `two-literature-coverage-r25.md`,
`window-size-read-in-chinese-r16.md`; refused already: `chinese-article-revision-r30.md`,
`chinese-wiki-canonical-url-r28.md`, `zh-wiki-snapshot-semantics-r29.md`, `two-literature-drift-r26.md`.

**PROVINCE verdict: REFUSE the channel (PROVINCE.md round-36 refinement names it explicitly:
the Chinese/Japanese ArchWiki channel, its URLs, snapshot semantics, revision bookkeeping,
translation drift, and *any documentation written in a localized channel*); salvage the two
config-plane claims by re-sourcing them from the English upstream channel, which is admissible.**

### Theme C — The gkeep window-size chain (window-rule size effect) — 12 entries
`gkeep-geometry-unobservable-r8.md`, `gkeep-rendered-geometry-chain-r9.md`,
`gkeep-size-rule-application-r10.md`, `gkeep-size-to-real-size-r11.md`,
`gkeep-client-size-request-r12.md`, `gkeep-rendered-geometry-record-r13.md`,
`gkeep-rendered-geometry-record-r14.md`, `gkeep-geometry-never-recorded-r15.md`,
`gkeep-observation-route-r11.md`, `gkeep-element-rules-r30.md`, `glyph-and-geometry-r31.md`,
`weather-glyph-render-r7.md` — 25 staged rows.

**PROVINCE verdict: SPLIT — the derivation half is IN (the window-rule `size` effect is the lane's
own owned plane and its named open item "per-window rule effects", arc-synthesis §6 F1), the
"record" half is REFUSE-AS-WRITTEN (a null-channel measurement), and the rendered geometry itself
stays unobservable by the lane.**

### Theme D — Idle/lock chain and omarchy app lifecycle — 10 entries
`idle-lock-intent-mechanism-r8.md`, `idle-lock-intent-surface-r9.md`,
`idle-lock-intent-surfaces-r10.md`, `idle-lock-journal-evidence-r11.md`,
`idle-lock-runtime-state-r28.md`, `idle-toggle-and-daemon-lifecycle-r29.md`,
`host-idle-lock-chain-r7.md`, `host-bar-and-idle-binding-r26.md`, `uwsm-app-daemon-unit-r7.md`,
`update-check-and-app-lifecycle-r31.md` — 29 staged rows.

**PROVINCE verdict: mostly REFUSE as duplicate of lane-held ground (the lane already holds
`idle-lock-plane.md`, `idle-lock-route-r17.md`, `idle-lock-never-asked-r12.md`,
`idle-lock-chain-armed-r14.md`, `idle-lock-offered-in-the-bar-r15.md`); one REFUSE-AS-WRITTEN on a
stale premise; the omarchy update/app-lifetime rows are package- and service-state ground (tsukuroi)
and one of them rides a v4.5.0-rc1 tag upstream of the host's 3.8.3.**

### Theme E — The bar's producers — 3 entries
`host-bar-producers-r28.md`, `host-producer-outputs-r29.md`, `host-producer-current-outputs-r30.md`
— 11 staged rows.

**PROVINCE verdict: IN (the bar's config plane is owned) — but this is round 40's *own* registered
assimilation theme (`.ufo/waves/round-40/registration.md` §Frontier step: "theme 'the host's bar
producers' — `host-bar-producers-r28.md` and `host-producer-outputs-r29.md`"), so it is not
available as the next round's theme; only `host-producer-current-outputs-r30.md` remains open.**

### Theme F — Event socket / request socket — 1 un-adjudicated + 4 already refused
`host-request-socket-cap-r7.md` (already-refused: `event-queue-host-measurement-r28.md`,
`event-queue-journal-measurement-r29.md`, `socket-client-contract-measurements-r29.md`,
`socket-modes-and-request-read-r30.md`).

**PROVINCE verdict: CLOSED — the four refusals stand on facts that still hold (the
`debug:disable_logs` null channel and the vanished instance directory), and the fifth entry
("the request ceiling on this host is no ceiling at all") is superseded by the lane's adopted
`request-socket-live-bound-r8.md` §1 (1023-byte chunk loop, "no byte bound anywhere in the
handler") and `request-limits-upstream-r31.md`.**

---

## 4. What each theme is worth, and what would block it

**Theme A (focus-grab)** — every upstream source re-fetches **200 today**:
`hyprland-focus-grab-v1.xml` (5,447 B), `Hyprland/v0.56.2/src/protocols/FocusGrab.cpp` (6,242 B),
`FocusGrab.hpp`, `src/managers/SeatManager.cpp` (26,074 B), `PortalManager.cpp`, quickshell
`focus_grab/grab.cpp`, `hyprland-protocols` README. I re-derived the load-bearing claims at the
host's tag: `FocusGrab.cpp:20-21` `m_grab->m_keyboard = true;` / `m_pointer = true;`, `:50`
`g_pSeatManager->setGrab(m_grab);`, `:94-110` `refocusKeyboard()` (retained-vs-unspecified
selection over an `unordered_map`), `SeatManager.cpp:582-608` `refocusGrab()` (pointer-box test,
then `m_surfs.at(0)`), `:806-808` `CSeatGrab::accepts()`, `:255-266` `sendKeyboardKey()` (per-event
client-identity filter), `FocusGrab.hpp:51` `std::unordered_map<…> m_surfaces;` vs
`SeatManager.hpp:40` `std::vector<…> m_surfs;`. The protocol XML carries `create_grab`,
`add_surface`, `commit`, `destroy`, and the `cleared` event.
Two of the 13 entries need their host receipts re-taken in-lane (the campaign copies live outside
the lane): the r9 compositor-log scan (`lanes/mado/round9/fetch/host-compositor-log-scan.txt`) and
the r15 client sweep (`lanes/mado/round15/fetch/host-focus-grab-client-sweep.txt`). Both campaign
files exist (verified) and both are readable, but **r9's is stale**: its cited instance directory
`/run/user/1000/hypr/…_1792804449_426444678/` no longer exists — the host's current directory is
`/run/user/1000/hypr/…_1792946182_1509497283/`.
Host-side facts re-derivable read-only today: the symbol census reproduces
(`strings -a /usr/bin/Hyprland | grep -ci 'focus_grab\|focusgrab'` → **89**;
`grep -c CFocusGrabProtocol` → **21**), the installed header is present
(`/usr/include/hyprland/protocols/hyprland-focus-grab-v1.hpp`, 6,306 B), the portal's advertisement
line is in the journal (`journalctl --user | grep 'Got interface: hyprland_focus_grab_manager_v1'`
→ 1 line today, with the `xdg_toplevel_tag_manager_v1` control also present), and the client sweep
reproduces (`grep -rl 'hyprland_focus_grab'` over the swept dirs → only `/usr/bin/Hyprland`).
**Caveat for the next round:** the "no client on this host" claim is a *binary-string* census — a
negative — so it needs a positive probe per QUALITY 62; and the "advertised but unbound" claim
depends on the portal's source, which I re-checked (`grep -c hyprland_focus_grab` in
`PortalManager.cpp` → **0**; the `Got interface:` line is emitted at `PortalManager.cpp:91`).

**Theme C (gkeep size chain)** — upstream source is fetchable and the host bytes are readable:
`~/.config/hypr/gkeep.conf` (264 B) carries exactly the three rules
(`float on` / `center on` / `size 420 500`, `match:class ^(org.omarchy.gkeep)$`), the omarchy
tag-sizing collision the file's own comment names is real on this host
(`~/.local/share/omarchy/default/hypr/apps/system.conf:4`
`windowrule = size 875 600, match:tag floating-window`, same line in upstream v3.8.4), and
`gkeep/ui.py @133b867` shows `application_id="org.omarchy.gkeep"` (`:449`) and
`window.set_default_size(420, 500)` (`:476`).
**But two entries must be refused as written**, and the reason re-derives exactly:
`gkeep-rendered-geometry-record-r13/-r14` count the marker "Map request dispatched", which is a
**core-logger DEBUG** line (`Hyprland v0.56.2 src/desktop/view/Window.cpp:2515`
`Log::logger->log(Log::DEBUG, "Map request dispatched, …")`), their own "positive control"
"Refocused popup parent window" is **also** DEBUG
(`src/managers/SeatManager.cpp:741`), and this host ships
`debug:disable_logs` = **1** (`hyprctl getoption -j debug:disable_logs` →
`{"option": "debug:disable_logs", "int": 1, "set": false}`; upstream default true at
`src/config/values/ConfigValues.cpp:629`). The zero is a null channel — QUALITY criterion 62.
**Second defect in `gkeep-rendered-geometry-record-r14.md` §2:** it asserts the gkeep note store holds
exactly three keys (`body`, `created`, `id`), but its declared receipt
(`lanes/mado/round14/fetch/host-journal-map-log-alltime-sweep.txt`) contains **no** such content
(grep for `note|body|created` → 0 hits): an unsourced claim inside an entry.
The terminal observation stays out of reach either way — `hyprctl clients` shows no gkeep window and
the lane may not start one.

**Theme B salvage is cheap and real.** The two config-plane claims the Chinese entries carry are
available in the admissible English channel: the 0.56.0 window-rules page
(`https://wiki.hypr.land/0.56.0/Configuring/Basics/Window-Rules/`, 327,952 B, HTTP 200) contains
`no_focus`, `no_initial_focus` and the sentence "Resizes a floating window" (1 occurrence each);
the bind-flags page (`/configuring/core/binds/flags/`, 269,491 B, 200) contains `allow_input_capture`
("When input is captured by a client, this bind will still be processed.") and the `locked` row
("Will also work when an input inhibitor (e.g. a lock screen) is active."). The host's own v0.56.2
build carries the same semantics in code: `ConfigManager.cpp:1540` `case 'x': allowInputCapture = true;`,
`KeybindManager.cpp:635` `if (PROTO::inputCapture->isCaptured() && !k->allowInputCapture)`,
`KeybindManager.cpp:649` `if (!k->locked && g_pSessionLockManager->isSessionLocked())`.
Note the flags page is "Latest git", not the 0.56.0 archive (the 0.56.0 flags path 404s), so an
adoption must be era-labelled — QUALITY 15/16 — the way round 39 refused the 0.56.0 Variables page.
Also note the staged row S218 labels arXiv 2604.18860 "peer-reviewed-track"; the arXiv record itself
shows a **preprint** (cs.CR, v1 submitted 2026-04-20, no journal reference) — the DOI
`10.48550/arXiv.2604.18860` is an arXiv DOI, and the publisher DOI behind the DFRWS paper
(`10.1016/j.fsidi.2025.301921`) resolves 200 to Elsevier.

**Theme D specifics.** `idle-lock-runtime-state-r28.md`'s premise ("the daemon is **not running**")
is stale on this host today: `pgrep -ax hypridle` → **1680 /usr/bin/hypridle** (running) while
`systemctl --user is-active hypridle.service` → **inactive** — which is exactly the lane's own
held reading in `idle-lock-chain-armed-r14.md` ("the daemon runs inside a transient scope"). The
package's own later entry `host-idle-lock-chain-r7.md` already corrects that premise.

**Theme F specifics.** `host-request-socket-cap-r7.md`'s own-work row is a binary-string census of
the running binary; its claim is already covered by the adopted pair the lane holds.

---

## 5. Best next theme

**Theme A — the compositor focus-mediation cluster (13 entries, 32 staged rows) — is the best next
theme.** Why, in order of weight:

1. **It is the largest block of genuinely un-adjudicated, in-province ground in the package**
   (13 of the 50; the next largest, theme C, is 12 and two of those are refuse-as-written).
2. **The lane holds zero of it.** `grep -c 'focus_grab\|hyprland-protocols' corpus/SOURCES.md` → **0**;
   `grep -c FocusGrab` → 0; `grep -c SeatManager` → 0; `grep -c 2604.18860` → 0; and no entry under
   `corpus/knowledge/` mentions a focus grab. It is new ground, not duplication — except the small
   advertisement overlap the lane already holds in `wayland-protocol-boundaries-r13.md`
   (the round-13 registry capture lists `hyprland_focus_grab_manager_v1`).
3. **Every source re-fetches 200 today**, all pinned to the host's own tag or to a first-party
   repository, and I re-derived the mechanism claims from those bytes (§4) rather than trusting the
   package's quotes.
4. **It attaches to two lane-held items and one lane-open item**: the bind table's
   `allow_input_capture` field (`bind-table-r25.md:62`, and `tools/mado-binds.py:670/:724` already
   parse and emit it — the *semantics* are what the package supplies), the idle/lock plane
   (`idle-lock-plane.md`, `idle-lock-route-r17.md` — the `locked`-vs-capture distinction), and the
   named open item "per-window rule effects / focus dispatch" (arc-synthesis §6, F1).
5. **It is the one theme whose host facts are re-takeable read-only inside the lane** — journal
   advertisement line, binary symbol census, installed header, portal source — with no compositor
   mutation, no socket connect and no producer execution, which keeps it inside the lane's
   read-only charter.

**Two entry-level cautions to carry into the next round's registration, both verified above:**
(a) drop the localized-channel rows `S230` (amgsk.dev) and `S323` (lightning-assist) and drop the
`zh/ja`/CSDN rows; (b) re-take the two host receipts in-lane, and treat the "no client on this host"
and "advertised but unbound" claims as negatives that need a positive probe (QUALITY 62), because the
r9 receipt's cited instance directory no longer exists.

**Runner-up, if a *tool* is wanted rather than an entry:** Theme C's derivation half (the window-rule
`size` effect → real size chain) is the only remaining ground that could carry a
`tools/mado-*.py`-style static predictor beside `mado-binds.py` / `mado-anims.py` / `mado-wsrules.py`,
all of which are upstream-source models of Hyprland's own tables. But its terminal observation is
unreachable by this lane, so it should be scoped as "the size-effect model", not "the rendered
geometry".

---

## 6. Limits of this survey

- Read-only throughout: the lane repo was not modified except this report; the package and the
  campaign tree were read only. `git status --porcelain` in the lane shows only round-40 wave
  artefacts written by other seats.
- I did **not** re-fetch through a reader proxy (r.jina.ai) the CSDN pages; the three CSDN URLs
  answer **HTTP 521** to a plain client today (verified: `blog.csdn.net/2301_76324845/…`,
  `blog.csdn.net/lxyoucan/…`, `blog.csdn.net/gitblog_01188/…` → 521 each), and the campaign's own
  `lanes/mado/REJECTIONS.md` items 4/6/7 reject that class.
- I did not re-derive every quoted line of all 50 entries; verdicts rest on (a) the lane's registry
  and lessons, (b) re-fetch of each theme's upstream sources, and (c) the specific defects named in
  §4 with their anchors.
- The `mupuf` publication page and the HAL record for the Wayland-security literature were
  reachable (200) but not read in full; their tier/role in the package is unchanged by this survey.
- **Tool installs:** none. Every check used what the machine already had
  (`git`, `curl`, `python3`, `strings`, `journalctl`, `pgrep`, `systemctl --user`,
  `hyprctl getoption -j`, `tar`). No `pacman`, no mutating git/jj, no compositor mutation beyond
  `hyprctl getoption -j` and `hyprctl version`. Scratch (`/tmp/*.cpp`, `/tmp/hyprsrc`, the
  v0.56.2 tarball) was deleted.

**Report:** `.ufo/waves/round-40/w1/ScoutMergeRest.md`
