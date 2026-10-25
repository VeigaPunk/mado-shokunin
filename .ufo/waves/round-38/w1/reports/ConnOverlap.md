# ConnOverlap — sibling-overlap scan: Hyprland request socket / hyprctl flags / upstream IPC ceilings

Agent: L1Mado38.ConnOverlap (connector, leaf — no subagents spawned).
Lane: mado-shokunin. HEAD at scan: `3f14bd2d7c3aa067091bc52e63fb8abdd944c3b8` (`git rev-parse HEAD`).
Fleet scope swept: 21 lanes' `PROVINCE.md` (all lanes that have one), 19 `SKILL.md`, all 21 `corpus/` trees, plus kama/tsukuroi/kaidoku coverage maps.
Bounds kept: lane production files read-only; nothing installed; no git state touched (read-only `rev-parse`/`status` only); no socket connected.

## §1 What was attacked and how

Two questions: (A) does any sibling lane claim the Hyprland request socket, hyprctl flags, or upstream IPC ceilings (contested scope)? (B) under which declared mado surface does round-38's request-socket theme sit, and does `PROVINCE.md` need a line naming the request socket's bound half?

Commands actually run (all read-only):

- `git rev-parse HEAD` → `3f14bd2d7c3aa067091bc52e63fb8abdd944c3b8`; `git status --porcelain` (see §5).
- grep, case-insensitive, pattern `hyprctl|socket\.sock|hyprland`, over all 21 `*-shokunin/PROVINCE.md` + 19 `*-shokunin/SKILL.md` (explicit paths; the `*-shokunin/` mid-path glob form returns no matches in the grep tool — first two attempts with that form were false negatives, re-run with enumerated paths).
- Same pattern over all 21 `*-shokunin/corpus/` trees (two paginated passes, 32 hit files total).
- grep `socket` / `ipc|request socket|event.?socket|XDG_RUNTIME` over `mado-shokunin/PROVINCE.md` (81 lines).
- Read: `PROVINCE.md`, `.ufo/waves/round-38/registration.md`, `corpus/knowledge/{ipc-contract-r25,request-socket-live-bound-r8,hyprctl-flags-r28,request-limits-upstream-r31}.md`, tsukuroi/kama/kaidoku province+skill hit contexts.

## §2 Findings — contested scope: EMPTY

**Verdict: PASS (uncontested). No sibling lane claims any of the three surfaces.** The complete inventory of fleet hits, each classified:

| # | Location | Text (abridged, exact at cited line) | Classification |
|---|---|---|---|
| 1 | `tsukuroi-shokunin/PROVINCE.md:124` (OUT-004) | "Mado owns the Hyprland, waybar, walker and terminal configuration plane, themes/wallpapers and screen/idle behavior." | Tsukuroi routes the plane OUT to mado — corroborates exclusivity, claims nothing. Same row duplicated at `tsukuroi-shokunin/corpus/knowledge/adjacency-anchors-r19.md:84` and `.json:55-58`, anchored to `mado-shokunin/PROVINCE.md:3-16`. |
| 2 | `kumitate-shokunin/SKILL.md:616` | bind-oracle = "requested **mount** binds — not the Hyprland `mado-binds.py` keybind file" | Explicit disclaimer. Reinforced at `kumitate-shokunin/corpus/knowledge/mount-order-and-bind-scope.md:15` ("it is not mado's Hyprland keybinding table or `mado-binds.py`") and `counter-amendment-discipline.md:82-83`. |
| 3 | `kotoba-shokunin/corpus/knowledge/sibling-overlap-census-round49.md:82` | row `mado … SKILL.md:8 "desktop & compositor craft playbook — the Hyprland/waybar/walker/terminal config plane"`, overlap column `no` | Kotoba's own round-49 fleet census already records mado's claim as uncontested. |
| 4 | `game-dev-2d-shokunin/corpus/live/r79-boundary-exec/run_love_probe.py:42` | `subprocess.run(["hyprctl", "clients", "-j"], …)` | **Nearest adjacency, still not a claim**: a historical one-off read probe inside a round-79 evidence script. Not in game-dev-2d's PROVINCE.md (their province/skill have zero Hyprland hits); not the request grammar, flags, or bounds. Flagged for awareness, no conflict. |
| 5 | audio / mori / tabi / kama / kengaku / kagi / chousa / tameshi / tsukuroi corpus hits (remaining 28 files) | e.g. `app-Hyprland-*` systemd scopes in OOM journals (`tsukuroi …/oom-event-plane.md:35`), `xdg-desktop-portal-hyprland` as a PipeWire client (`audio …/pactl-clients.txt:3`), SOCKS-proxy socket docs (`mori …/S175.src:2273`), tameshi's PATH-stub `hyprctl` mutation scenarios (`tameshi …/mutation-case-mado-verify.md:48` — method owner for mado's own harness, consumed read-only per `mado PROVINCE.md:28`) | Incidental process/package/journal evidence about the desktop, not claims on the IPC plane. |

Coverage maps checked per assignment: **tsukuroi** — its coverage map is the OUT/ADJ table in `PROVINCE.md:110-127` + `adjacency-anchors-r19.*`; row OUT-004 covers only the *config plane* half of mado's claim (anchor range `PROVINCE.md:3-16`); no row mentions sockets/IPC at all. **kama** — all socket language is TCP/HTTP model-endpoint probing (`ss -ltn`, registered ports, `PROVINCE.md:34`, `SKILL.md:46,130,135`); no Hyprland/AF_UNIX-IPC claim. **kaidoku** — only mention is its own sandbox limitation ("AF_UNIX sockets reachable", `SKILL.md:608`) and verb-coverage of its own evidence verbs; no desktop claim.

**Conclusion: mado's round-38 request-socket ground is exclusive. Nothing to reconcile with a sibling; no contested scope exists at file:line level.**

## §3 Findings — where the theme sits in mado's PROVINCE.md, and the gap

Exact current lines (HEAD `3f14bd2d`, `PROVINCE.md`, 81 lines total):

- `:3-4` — "**Domain:** desktop & compositor craft — the Hyprland/waybar/walker configuration plane and display behavior on this host."
- `:6-9` — "**Owns (surfaces):** `~/.config/hypr/` (hyprland.conf, keybinds, rules, animations), `~/.config/waybar/`, `~/.config/walker/`, terminal emulator configs … screen/idle behavior (hypridle/hyprlock where present)."
- `:13-15` — "**Refuses:** secrets in configs (shape-only, → kagi), model endpoints (→ kama), model quality (→ kengaku). Never mutates a running compositor state; every claim is file-byte- or screenshot-verified."
- `:28` — mado-verify.sh row: "… and `hyprctl` read verbs only (version, instances, configerrors, getoption, binds, monitors, layers) …"
- `:29` — mado-binds.py row: "… no compositor, socket, network or environment beyond `HOME` …"
- `:30` — mado-anims.py row: "… no compositor, socket, network or environment variables …"
- `:39` — "… It still writes nothing, opens no socket and runs no process; run it on trees you mean to read."

Grep evidence for the gap: pattern `ipc|request socket|event.?socket|XDG_RUNTIME` over `PROVINCE.md` → **0 matches**; every `socket` occurrence (`:29`, `:30`, `:39`) is a *negative* disclaimer about a tool. **The theme sits under no declared surface.** It rides only the generic Domain line via corpus knowledge: the held two-socket contract (`corpus/knowledge/ipc-contract-r25.md` — request socket `$XDG_RUNTIME_DIR/hypr/[HIS]/.socket.sock`, §1), the round-38 bound entry, the flags entry, and the ceilings entry — each self-described as "a new edge class under the held IPC contract". Meanwhile `registration.md` §"Not claimed" states "no socket is connected, no request is sent" — the lane's real stance — but that stance is stated in a wave file, not in the province.

**Does PROVINCE need a line naming the request socket's bound half? Finding: YES, narrowly (see §4).** Two concrete failure modes the silence permits:

1. **Re-framing regression.** The bound half is *temporal, not volumetric* — `corpus/knowledge/request-socket-live-bound-r8.md` §1: "`int ret = poll(pollfds, 1, 5000);`", "a 1023-byte chunk loop (`:2274` …), the request is the accumulation of the chunks, with no byte bound anywhere in the handler"; entry title: "The request socket's live bound is a five-second timeout, not a byte cap". A future wave reading only the province (whose only socket language is "opens no socket") has nothing pointing at this held bound and can re-commit the exact volumetric misframing r8 corrects — or re-litigate it against `request-limits-upstream-r31.md`'s upstream-ahead ceilings (`REQUEST_LIMIT = 1024 * 1024`, `FOLLOW_QUEUE_LIMIT = 64 * 1024`, from a post-0.56.2 revision that 404s at the host tag), which are *upstream declarations*, not host facts.
2. **Fleet routing hole.** Tsukuroi's OUT-004 anchors mado's claim to `PROVINCE.md:3-16` — the config-plane half only. The runtime-IPC knowledge half is anchored nowhere in the fleet: a scope question ("who holds the request-socket contract?") currently resolves to *nobody* in every lane's paperwork, which is how siblings absorb or orphan a theme.

## §4 Proposed move (one bounded proposal)

**Append-only province refinement paragraph** (round-scoped, applied by the lane's editor through the normal refinement channel — NOT a wave-1 write; wave-1 bounds kept me read-only and I touched nothing), e.g. after the round-36 refinements:

> **Round-38 refinement (append-only; no new write surface, no live authority):** the lane holds documentation/source-read ground on the compositor's IPC plane under the Domain line — the request socket (`$XDG_RUNTIME_DIR/hypr/[HIS]/.socket.sock`) and its bound half: the live bound is the five-second poll timeout with 1023-byte chunk accumulation (`corpus/knowledge/request-socket-live-bound-r8.md`), upstream's later 1 MiB / 64 KiB ceilings are upstream-ahead declarations, not host facts (`request-limits-upstream-r31.md`), and the hyprctl flag vocabulary (`j`/`i`/`r`) is documented ground (`hyprctl-flags-r28.md`), all under the held contract (`ipc-contract-r25.md`). No socket is ever connected and no request is sent; `tools/mado-verify.sh` keeps the read-verb enumeration of its row; this is knowledge ground, not a probed surface.

**Affected axes:** coverage (+ declared ground now names held ground — the "new edge class under the held IPC contract" framing becomes visible at scope level); navigation (+ the IPC knowledge half becomes attributable fleet-wide, closing the OUT-004 half-anchor hole). None harmed: calibration and operability instruments are untouched (no counter, gate, or manifest byte changes — the freeze set in `registration.md` lists the counters/gate/manifest/fetch receipts/live triplet/assimilation scratch and does **not** include `PROVINCE.md`); no write surface or live authority is widened (the line codifies the existing "no socket is connected" stance).

**Second-order trace:** runtime — none (prose only); substrate — none (matches observed practice; `ipc-contract-r25.md` §3 already records "No socket was connected"); verification — the discrimination gate and both counters are outside the edit; sibling anchors — tsukuroi's OUT-004 anchors lines `3-16`, an append lands after line 81, so no sibling anchor shifts (append-only is anchor-safe); kotoba's round-49 census quotes `SKILL.md:8`, also untouched.

**Risks:** (1) over-claim wording ("owns the socket") would imply live authority the registration explicitly declines — mitigated by the "documentation/source-read ground; no socket is ever connected" phrasing; (2) misreading as new `mado-verify.sh` verbs — mitigated by pointing at the tools row's existing enumeration; (3) scheduling — must not be attributed to wave-1 (production-file bounds); the lane's own pattern is round-scoped append-only refinements (round-19/23/25/27/36 precedents in this file).

**Verification for whoever applies it:** re-run the two province greps in §3 (expect the 0-match gap before, the new paragraph after); re-run the discrimination command from `registration.md` (expect `correct=19/19 verdict=TARGET_MET`, unchanged); confirm `git diff` of `PROVINCE.md` is append-only (no prior line edited, first changed line ≥ old EOF+1).

## §5 Observed state (reported, not judged)

`git status --porcelain` at scan time: ` M quality/check-r38-discrimination.py` — an uncommitted working-tree modification to a file in the registration's freeze set — plus untracked `.ufo/waves/round-38/w1/reports/RevEntryLimits.md`, `RevScorecardMath.md`, and `w1/scratch/`. Out of my scope to attribute or evaluate; routed to Main for whoever owns freeze integrity.

Installs: none. Bounds: no lane production file written; my only fleet-root writes are this report and one stray `nil` placeholder file created by a malformed tool call and deleted in the same minute (`rm /home/vgpnk/Projects/shokunin/nil` → gone; no other file created or modified anywhere).
