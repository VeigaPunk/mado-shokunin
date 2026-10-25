# ConnFrontierFit — round-38 wave-1: frontier-route fit-check

Seat: `L1Mado38.ConnFrontierFit` (connector). Date: 2026-10-25. Lane bounds kept:
lane read-only; writes = this report + `/tmp/mado38-ConnFrontierFit/`. No installs. No
socket connection, no request sent, no compositor/config/service/package mutation.

## 1. What I attacked

The round-38 Frontier route paragraph `corpus/README.md:276-285` ("### Round-38
request-socket bound route") — whether it accurately states what moved and what stays
open, checked against the three entries it names, the registration's declared claims,
and the round-37 route it parallels. Then the mapping (PROVINCE.md surface row;
arc-synthesis.md §6 item). Then the round-39 next-surface proposal.

## 2. Fit-check verdicts

| # | Route claim (README line) | Verdict | Evidence |
|---|---|---|---|
| 1 | "A second new edge class under the held IPC contract ... moves onto sourced ground" (:278) | **PASS** | All three entries' `ground:` lines say "a new edge class under the held IPC contract (`knowledge/ipc-contract-r25.md`)" (hyprctl-flags-r28.md:11, request-socket-live-bound-r8.md:12, request-limits-upstream-r31.md:12). "Second" parallels round-37's "A new edge class under the held IPC contract" (README:246): event socket first, request socket second. Counter-backed at the current tip: re-ran the frozen C2 counter (source read first — it writes nothing: only `git show`/`ls-tree` reads and prints): `PRED-C2-r38-v1 admitted=3/3 verdict=TARGET_MET rev=bb1adce40fdbe9de9b2040f70bc64cee7a0ab0c5 base=f6e3247f...` exit 0. Committed discrimination receipt `.ufo/waves/round-38/receipts/after-discrimination-v3.txt:20`: `MADO_R38_DISCRIMINATION: controls=19 correct=19/19 verdict=TARGET_MET`. Context already on record (not my finding): LOG.md round-38 errata — at the frozen pair (`58e55ec`) the gate scores 18/19 (C1 counter patched post-freeze `859d0cf`; manifest patched post-data `b6c1d31`); the landed pair is a *new predicate*, with a re-registration ruling routed to the non-author closure. "All TARGET_MET at HEAD" holds for the landed pair. |
| 2 | "What the request socket publishes ([flags])" (:280) | **PASS** | hyprctl-flags-r28.md §1: exactly three flags, verbatim from S221's `flag list:` block (receipt lines 3392-3397: `j -&gt; output in JSON`, `i -&gt; select instance (id or index in hyprctl instances)`, `r -&gt; force state refresh...`). The flags vocabulary moved. |
| 3 | "what actually bounds a request on it — a five-second poll timeout, not a byte cap, read at the host's own commit" (:280-282) | **PASS** | request-socket-live-bound-r8.md §1: `int ret = poll(pollfds, 1, 5000);` (S158 @ host's own commit `efb50993`), 1023-byte chunk loop, "no byte bound anywhere in the handler"; INF: "the live bound ... is **temporal, not volumetric**". The route's wording is that finding. |
| 4 | "what upstream now declares at a later revision ([upstream ceilings])" (:283) | **PASS** | request-limits-upstream-r31.md §1: `REQUEST_LIMIT = 1024 * 1024`, `FOLLOW_QUEUE_LIMIT = 64 * 1024` at `src/ipc/s1/Unix.cpp` @ `a1c2428`; UNK (:40): file 404s at the host's tag — later-revision caveat stated. |
| 5 | "The package's claimed S272/S276 ids map to held rows S158/S187 (byte-identical re-fetches), and the host transport stat lands as row S258" (:284) | **PASS** (byte-identity independently verified) | `sha256sum`: `.ufo/waves/round-38/fetch/S158.bin` = `798b7c6c...` = `.ufo/waves/round-24/fetch/S158.bin` (held since round 24); `S187.bin` = `136e5511...` = `.ufo/waves/round-32/fetch/S187.bin`. Lesson assimilation table: S272→S158, S276→S187, S212a→S258. SOURCES rows S221/S253/S258/S277 carry matching sha256s. |
| 6 | "no Frontier bullet above is moved by it" (:278) | **PASS** | Checked every Frontier bullet (README:104-274): rendered UI / Waybar module text / Walker socket protocol / dispatcher behaviour / per-window rule effects — untouched (no request sent); idle/lock, gate residual, errata, promotion — untouched. The exclusion matches round-37's: "the 'Walker socket protocol' item is the launcher's own sockets, not the compositor's event socket" (README:247-249). |
| 7 | "Still open: no socket was connected and no request was sent; the effective request-size bound under the host's build stays unmeasured" (:284-285) | **PASS, but incomplete (F2)** | Matches the entries' UNKs: live-bound:51 (effective bound unmeasured; measuring would mean sending an oversized request — declined) and upstream:40 (nothing measured against a live socket; connecting is outside the lane's authority). **F2 (minor):** the open-list omits the two UNKs hyprctl-flags-r28.md §3 declares (:38, :41): server-side handling of each flag, and whether the host's own configuration ever issues a flagged request. The round-37 route listed its entries' unknowns; the round-38 route lists two of four. Not false — a subset. (Registration's "Not claimed" covers only the socket half, consistent with the route.) |

**F1 (minor; entry-level, not route-level).** hyprctl-flags-r28.md §3's premise — "the IPC contract established that a leading flag segment is stripped before the dispatcher name is matched" — is not established by the entry it names: `ipc-contract-r25.md` holds only the grammar quote (S186:19, :42) and the synchronous-freeze quote (S186:21-23, :44-45); `dispatcher-surface-and-request-grammar-r26.md:61-64` has the grammar-prefixed line only; the S186/S187 pages give the grammar shape, not stripping. The stripping fact **is** in ground the round already holds — S158 getReply: `:2068` `// process flags for non-batch requests`, `:2096` `request = request.substr(sepIndex + 1); // remove flags and separator so we can compare the rest of the string` — but the flags entry cites only S221. Fix is a one-line re-point (→ S158 getReply), no retraction. The route paragraph itself does not repeat the claim.

## 3. Mapping

### PROVINCE.md surface row: **none increments — and that is accurate, not a gap.**

- The P-surface taxonomy is the round-17 rubric V list (SCORECARD.md:856-859): "PROVINCE.md owned surfaces P1 Hyprland config tree, P2 Waybar, P3 Walker, P4 terminal-emulator configs, P5 themes/wallpapers, P6 screen/idle". Saturated 6/6 since round 18 (SCORECARD.md:1011). No P7 exists lane-wide (`grep '\bP7\b'` → only defect/mutant ids in old rounds).
- None of the three round-38 entries carries a `surface:`/`covers:` marker (grep over `corpus/knowledge/`: `surface: P` appears only in idle-lock-route-r17/P6, terminal-route-r17/P4, terminal-trees-r23/P4, theme-route-r18/P5, walker-route-r18/P3; `covers: U` only in the rounds 12-16 entries).
- The IPC theme was deliberately landed outside the surface rubric: round-32 registration §C1 titles it "the Hyprland IPC two-socket contract, frontier → core" — coverage-map rows, not surface rows. Rounds 37/38 add edge classes under that held theme. The request socket is the compositor's runtime IPC endpoint (`/run/user/1000/hypr/<HIS>/.socket.sock`), not one of the six owned config trees; PROVINCE.md's rule "Never mutates a running compositor state" is why the lane reads the contract from code/docs and declines to exercise it.
- The increment the route *does* correspond to is the coverage-map rows: three new rows MADO-R38-1/2/3 (README coverage-map table), consistent with the counter's clause e. The "Province routes — choose a surface" table's Hyprland row is the nearest navigation row, but that table's declared scope is "inherited 2026-10-14 evidence" — the IPC entries are not that, so omitting them there is consistent.

### arc-synthesis.md §6 item: **closes none; advances the channel contract under "dispatcher behaviour".**

- The §6 gap ledger (arc-synthesis.md:290-307) has 12 rows; none is the request socket. The route's "no Frontier bullet above is moved" is consistent — nothing in §6 closes.
- Nearest item: `| dispatcher behaviour | no keystroke injection allowed — [INF-docs] only (r2, 24 dispatchers) |`. The request socket is exactly the injection channel that constraint fences; round-38's ground sharpens *why* it stays fenced — the channel is synchronously evaluated with a five-second poll timeout (S187 quote in live-bound §1; S186:21-23 in ipc-contract §1), so any behavioural probe would be a live compositor interaction the lane declines. **Advance, not closure.**
- Explicitly NOT "walker socket protocol" (§6): that row is the launcher's own sockets (README:247-249; inherited by the round-38 route).
- U-items: U1-U7 were all closed by rounds 12-16, and the U1-U7 fraction is retired (SCORECARD.md:223-226: "its denominator was the fixed U1–U7 uncovered-ground list, five of whose items have since been closed"); the live coverage record is the per-round frontier rows (SCORECARD.md:226-227). The round-38 entries claim no U item. Answer to "(U?)": no U item — the U denominator is retired.

## 4. Round-39 proposal — next request-socket surface

**Proposal: the request socket's handling chain at the host's own commit — client-side flag translation and batch assembly, server-side flag semantics — plus the host's flagged-usage census.** This closes both UNKs hyprctl-flags-r28.md §3 declares and extends the grammar entry with `[[BATCH]]` mechanics. It merges two of the assignment's three options (server-side flag handling + `[[BATCH]]`) because they live in the same held bytes; the third (usage sweep) becomes the host half and is **non-empty** (below).

Ranking rationale: server-side handling + batch reuse pin-bound first-party bytes at the host's own commit (near-zero new fetches); the usage sweep alone would be a thin standalone claim (a census without the semantics to interpret it); `[[BATCH]]` alone duplicates half of the first.

### Sources that would ground it

Already held (pin-bound receipts; zero new fetches for the server half):

- **S158** — `src/debug/HyprCtl.cpp` @ host commit `efb50993` (receipt sha `798b7c6c...`):
  - `:2068-2096` `getReply` flag loop: `:2085` `j`→FORMAT_JSON, `:2087` `r`→`reloadAll`, `:2089` `a`→`m_currentRequestParams.all`, `:2091` `c`→`sysInfoConfig`; `:2069` `if (!request.starts_with("[[BATCH]]") && request.contains("/"))` — batch bypasses flag processing; `:2096` strip `request.substr(sepIndex + 1)` before command matching. → `a`/`c` are server-handled but **absent** from the published flag list (S221 lists exactly j/i/r); published `i` has **no** server-side branch anywhere in the receipt (grep `'i'`/`instance` → only the socket-path line :2331) — `i` is client-side.
  - `:2041` `registerCommand(SHyprCtlCommand{"[[BATCH]]", false, dispatchBatch});`; `:1309-1332` dispatchBatch: `:1312` `request.substr(9)`, `:1314` DELIMITER `"\n\n\n"`, split on `;` at bracket-depth 0 with each element re-entering `getReply` (`:1326`), trailing delimiter trimmed (`:1332`).
  - `:2127` `Config::monitorRuleMgr()->scheduleReload();` (+ layout matcher and input config updates) — the concrete body of the `r` flag's server-side price, behind hyprctl-flags §2's synchronous-dispatch warning.
- **S221** — 0.56.0 hyprctl page (receipt sha `35046ba0...`): `flag list:` publishes exactly j/i/r (:3392-3397); `rollinglog ... supports -f/--follow` (:3339). The published-vs-handled vocabulary delta is measurable from held bytes.
- **S277** — chonkstep (tier C, receipt sha `ff561fe0...`): `:84-85` "There is no length prefix or newline. `j` requests JSON. Batch requests start with `[[BATCH]]` and use `;` separators." — the tier-C cross-check for batch grammar.
- **S258** — host stat receipt (sha `fcc60820...`): instance dir `/run/user/1000/hypr/efb50993..._1792804449_426444678` — the host anchor for the `i` story (one socket dir per instance).
- **S253** — held; grep shows `src/ipc/s1/Unix.cpp` has **no** flag/FORMAT handling — the flags story is host-commit-specific; the entry must pin S158's commit and keep the upstream-ahead caveat (the round-38 pattern).

One new source row (tier A, code, one fetch): **`hyprctl/src/main.cpp` @ `efb50993`** — fetched to scratch this seat to pin the path: HTTP 200, 17,168 B, sha256 `f6b0d1fcfc6695194c70964250591a35ffe90274309303d8f5fd0ac6f8c1c93f` (path confirmed from the commit tree; `hyprctl/main.cpp` 404s). Client-side anchors:
- `:480` `fullRequest = fullArgs + "/" + fullRequest;` — the client builds the `[flags]/command` request;
- `:413-437` parse chain: `-j`→fullArgs "j", `-r`→"r", `-a`→"a", `-c/--config`→"c", `-f/--follow`→"f" (rollinglog-only, :489-492), `--batch`→marker, `--instance`/`-i`→overrideInstance, `-q/--quiet`→quiet (client-only);
- `:347` `std::string rq = "[[BATCH]]" + commands;` and `:517` `if (fullRequest.contains("/--batch")) batchRequest(fullRequest, json);` — `--batch` is a client marker; the socket sees `[[BATCH]]`;
- `:494-513` `-i` resolves a signature or an index against the local `instances()` list and picks the socket dir (`:230` `socketPath = getRuntimeDir() + "/" + instanceSignature + "/.socket.sock"`) — `i` never reaches the server;
- `:483-487` `instances` is HIS-independent, handled entirely client-side.

Host half (own-work census; new receipt rows in the S258 pattern). Preliminary probe this seat (counts/shapes only): 36 files under `~/.config/waybar`, `~/.config/hypr`, `~/.local/share/omarchy` contain `hyprctl`; **flagged invocations exist in 2 files, 3 sites**:
- `~/.local/share/omarchy/bin/omarchy-hyprland-window-pop` → `hyprctl -q --batch \` (2 sites);
- `~/.local/share/omarchy/bin/omarchy-menu-keybindings` → `hyprctl -j binds |`.
So the §3 UNK "whether the host's own configuration ever issues a flagged request" has a preliminary **YES** — and the flags used (`-q`, `--batch`) are client-only options absent from the published socket flag list, exactly the vocabulary-vs-usage delta this entry would pin. The round-39 seat must redo this as a receipted census (sha256-bound, like S258) and may also sweep the unflagged shapes (`hyprctl dispatch` ×21, `monitors` ×20, `keyword` ×11, `reload` ×9, …) for the grammar entry's host-usage column. The shell-history census stays OUT (lesson finding 4: `~/.zsh_history` is outside the lane's own-work boundary).

Bounds: the whole surface is code-read + file census — no socket connection, no request sent, no compositor/config mutation; the `r` flag's reload side-effects are read from code, never fired.

Entry shape: amend `hyprctl-flags-r28.md` §3 (both UNKs → answered; fold in F1's re-point) and extend `dispatcher-surface-and-request-grammar-r26.md` (or a new `request-flag-handling-r39.md`) with the client/server handling chain and `[[BATCH]]` mechanics. Counter: reuse the c2-r38 pattern (pin-bound receipts + located quotes + lineage) with the new pin row for `hyprctl/src/main.cpp`.

**Competing claimant (named for the planner):** round-37 SCORECARD "Planned (round 38)" item 2 parked "the config-option table (who owns each key, checked against getoption)" from considerthese/2026-10-24 — round 38 did not take it; it is still the lane's own earlier-ranked next desktop surface. The request-socket theme has momentum (rounds 32→37→38, all sources held, counter pattern reusable), but the planner should choose, not accumulate.

## 5. Installs

None. (Tooling directive satisfied: curl/git/python3 were already present; nothing installed.)

## 6. Scratch

`/tmp/mado38-ConnFrontierFit/`: `tree.json` (GitHub tree @ `efb50993`, 347,495 B), `client-main.cpp` (`hyprctl/src/main.cpp` @ `efb50993`, 17,168 B, sha256 `f6b0d1fc...`), `hyprctl-main.cpp` (14-byte 404 body from the first, wrong path guess — superseded by `hyprctl/src/main.cpp`).
