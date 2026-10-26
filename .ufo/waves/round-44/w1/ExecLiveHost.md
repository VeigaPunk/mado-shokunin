# ExecLiveHost — round 44 w1: C1 on the running desktop (reported, not scored)

Seat `ExecLiveHost`, lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, base
`6a1a90528fe533cadee506a9fa3e9d13d15cc41f`, claims freeze `e2289516a9a857f55cda7be635933e89b931c3da`.
Host Hyprland 0.56.2 at `efb50993780079460b0cbed1363e2166a2de1d9f`, kernel 7.2.11-arch1-1,
monitor DP-1 3440x1440 reserved `[0,26,0,0]`. Reads 2026-10-26T13:53-03:00; projected to shape-only form and the receipt rebuilt at
2026-10-26T14:10:20-0300.

**Receipt:** `.ufo/waves/round-44/w1/ExecLiveHost/live-states.txt`, sha256
`9f6fa83a5dfedefc16d0b3b5f98985fd709169c5da86f35290f2eb912453edb0`, 400 lines; the
receipt carries tool output verbatim with exit codes and sha256s; the three `hyprctl` dumps are
shape-only projections of the raw reads (raw sha256 in `raw-dumps.sha256`, raw bytes not
retained). Quote locators in it are computed
at build time and re-checked by `verify-quotes.py` (last run: `VERIFY_QUOTES: PASS (0 failures)`).

Only the four allowed read verbs were issued: `hyprctl version`, `clients -j`, `monitors -j`,
`workspaces -j`. No dispatch/keyword/reload/setprop/--batch/output/plugin/kill. No write outside
the seat dir; no tool installed; read-only `git show` for the round-43 baseline; scratch dir
(`/fast/scratch/hyaku/mado-r44/ExecLiveHost`) removed.

## What was run

| step | command | result |
|---|---|---|
| tool copy | `cp .ufo/waves/round-44/c1/ctl-ref-tool.py.txt w1/ExecLiveHost/mado-geometry.py` | sha256 `8e871a00fcf1a615e3683ebe5204f67cfe679182ff15d008b83fed34131c788d`, byte-identical to the reference |
| r43 baseline | `git show 6a1a9052…:tools/mado-geometry.py` → `mado-geometry-r43.py` | sha256 `e3c2e471505932f797a98ee2aa9ab1b04fc919f2140509282ef8472498135a99`, `grep 'fullscreen'` = 0 hits |
| A live join | `hyprctl clients -j \| python3 -I mado-geometry.py --clients - --rules ~/.config/hypr/gkeep.conf` | **rc 3**, stderr 0 bytes, `verdict=NO_MATCHING_CLIENT` |
| B live bytes, matching rule | same tools vs `live-bytes.conf` (real Alacritty, 1720x1414) | both rc 0, **byte-identical stdout** |
| C state dumps | `make-state-dumps.py` → `fs2.json`, `max1.json`; both tools × both dumps | see table |
| D before/after | computed from C | `fs2`: r43 `DIFFER` (rc 1) → new `FULLSCREEN` (rc 0); `max1`: r43 `DIFFER` (rc 1) → new `MAXIMIZED` (rc 0) |
| F pins | locators scanned from `fetch-c1/`, hashes vs `receipts/fetch-sha256.txt` | three pins re-hashed, all `matches receipt` |
| G selftests | `--selftest` both tools | new `91/91 passed` rc 0; r43 `73/73 passed` rc 0 |

## Findings

**F1 — the live desktop has no gkeep window, and the tool says so without inventing a match.**
3 mapped clients (`grok-bot`, `Alacritty`, `zcode`), `matched=0`, `clients=3`, `unmapped=0`,
`verdict=NO_MATCHING_CLIENT` rc 3 on both tools. The rules file parses as `rules=1 float_rules=1
other=1 unsupported=0` — the `other=1` is the `center on` line, i.e. the tool is not silently
eating a rule effect it does not model. This is the assignment's expected pre-state, and the round-43 tool prints the
identical summary on the same bytes (both runs are in the receipt: section A over stdin, the
round-43 tool on the same dump in section C).

**F2 — the live dump carries both state fields, typed as integers.**
After the shape-only projection (below), every client still carries `fullscreen` and
`fullscreenClient` as JSON `int`, all `0`, plus
`fullscreenHandler: "default"`. Distinct `fullscreen` values across the dump: `[0]`. So the
contract's "JSON integer 1 or 2, not bool, not float" input shape is what Hyprland 0.56.2 actually
emits; today's live clients take the `fsmode = 0` path. (No maximized/fullscreen window was open,
so the non-zero live path is not observed — see "not established".) The two fields and
`fullscreenHandler` are in the projection on purpose: they are the C1 subject, not session material.

**F3 — the two state dumps use this host's real boxes.**
Monitor box `3440x1440`; work area = monitor box minus reserved = `3440x1414`. Live corroboration
on real bytes: the tiled `zcode` client occupies `[3440, 1414]` at `[0, 26]`, i.e. exactly the
work-area box the maximized dump encodes. `fs2.json` = `3440x1440`/`fullscreen: 2`;
`max1.json` = `3440x1414` at `(0, 26)`/`fullscreen: 1`; both `floating: true`, class
`org.omarchy.gkeep`, built from the projected 10-key live client record (`at` set to the pinned
box origin: monitor origin for fullscreen, origin plus top reserved for maximized).

**F4 — the round-43 false report is reproduced, and the new tool removes it.**
Both dumps: round-43 tool emits `verdict=DIFFER`, `differ=1`, rc 1 and no state words; the new
tool emits `verdict=FULLSCREEN` / `MAXIMIZED`, `differ=0`, and the summary gains
` maximized=<n> fullscreen=<n>` (`maximized=0 fullscreen=1` and `maximized=1 fullscreen=0`
respectively), rc 0. This is the claim's core before/after on state-shaped inputs that match the
host's own geometry.

**F5 — no harm where no client is in a state.**
On the live dump with a rule that matches a real tiled client, both tools print byte-identical
stdout (`verdict=TILED`, rc 0, no `maximized=`/`fullscreen=` words). Supports the frozen no-harm
clause r and the summary byte-identity requirement when `maximized + fullscreen == 0`.

**F6 — the field the tool reads is the internal mode, per the pins.**
`fetch-c1/Hyprland-HyprCtl.cpp:410` declares `"fullscreen": {},` and the value fed to it at
`fetch-c1/Hyprland-HyprCtl.cpp:431` is `getFullscreenModes(w).internal`;
`fetch-c1/Hyprland-HyprCtl.cpp:411` declares `"fullscreenClient": {},` fed at
`fetch-c1/Hyprland-HyprCtl.cpp:432` from `.client`. The mode enum is
`FSMODE_NONE = 0,` (`fetch-c1/Hyprland-FullscreenController.hpp:13`),
`FSMODE_MAXIMIZED,` (`fetch-c1/Hyprland-FullscreenController.hpp:14`),
`FSMODE_FULLSCREEN,` (`fetch-c1/Hyprland-FullscreenController.hpp:15`); `internal` and `client`
both start at `FSMODE_NONE` (`fetch-c1/Hyprland-FullscreenController.hpp:34`,
`fetch-c1/Hyprland-FullscreenController.hpp:35`). Box assignment: `FULLSCREEN` →
`MONITOR->logicalBox()` at `fetch-c1/Hyprland-FullscreenHandler.cpp:192` and again in the sync
path at `fetch-c1/Hyprland-FullscreenHandler.cpp:222`; `MAXIMIZED` →
`workArea(target->floating())` at `fetch-c1/Hyprland-FullscreenHandler.cpp:196`, sync path
`workArea(FS_TARGET->floating())` at `fetch-c1/Hyprland-FullscreenHandler.cpp:238`. All three
pins re-hash to the values in `receipts/fetch-sha256.txt`. This grounds both the dump geometries in
F3 and the tool's choice of `fullscreen` over `fullscreenClient`.

**F7 — an independent capture of the same desktop projects to the same bytes.**
Another seat captured the same desktop separately (`w1/ExecIndepB/receipt-live-clients.json`, raw
sha256 `5ead9176…`, 2619 bytes) against this seat's raw (`931ed70a…`, 2619 bytes). After projection
the two files are byte-identical (`983c3a17…`, 1108 bytes, verified with `cmp`), so every kept field
matched across the two captures and the raw delta lies entirely outside the kept fields. What the
delta was cannot be re-diffed here — both raw byte sets are deleted by the shape-only rule — but the
safety seat observed the peer dump's terminal title differing before projection, which is the
expected session material (raw size equality is consistent with it, not proof of it).

## Shape-only projection and run bounds (fix for the wave's safety review)

`SentLiveReads` flagged two defects in this seat dir; both are fixed here:

- **Window titles in committed evidence.** The first receipt embedded the raw `hyprctl clients -j`
  dump (32 keys per client: `title`, `initialTitle`, `pid`, `stableId`, …) and the two fixtures were
  copies of a live client, so terminal titles would have entered lane history. SKILL.md:332 is
  explicit: `clients` for length/tags, never window titles. `project-dumps.py` now projects the three
  dumps to the read fields only — clients to `address, mapped, class, floating, size, at, monitor,
  fullscreen, fullscreenClient, fullscreenHandler` (the round-43 precedent
  `fetch/host-clients-r43.json` shape plus the three state fields C1 is about), monitors to geometry
  with `serial`, `make`, `model`, `description`, modes and the colour fields dropped, workspaces
  without `lastwindow`/`lastwindowtitle`. The raw bytes are not retained; `raw-dumps.sha256` keeps
  their sha256 (`931ed70a…` clients, `f1894f45…` monitors, `bdc9791e…` workspaces).
  `projection-invariance.txt` shows the loss is outside what the tool reads: raw and projected
  clients give byte-identical stdout under both tools. The fixtures were rebuilt from the projected
  record (10 keys each) and keep the same verdicts.
- **Unbounded harness.** The builder's `run()` now passes `timeout=30`; a run that exceeds it is
  recorded as rc 124 with a TIMEOUT marker, never as a verdict. SKILL.md:300 documents the shell
  form: `timeout 5 python3 tools/mado-geometry.py --clients - --rules <file>`, exit 124 = no
  verdict. The live gkeep regex is a plain anchored literal, so this is a bound against a future
  rule file, not a change in today's evidence.

## Not established (declared)

- **No live maximized/fullscreen window.** No gkeep (or any) window was maximized or fullscreen
  while I read the desktop, so the box↔mode mapping is the pinned source's fact plus a synthetic
  (live-shaped) dump, not an observed live pair. Opening gkeep and pressing the keys is the
  operator's move, not mado's.
- **X11 branch untested live.** The one X11 client (`grok-bot`, `xwayland: true`) was in no state;
  gkeep is a Wayland/xdg client per the C2 pins.
- **Scored status: none.** This seat produces host evidence only; the counted instrument is
  `c1-r44-geometry-states.py` on the data commit, which I did not run (out of seat scope) and which
  the registration's kill rule governs.
- The two dumps are hand-made: only their template bytes come from the host. They are labelled as
  such in section C of the receipt.

## Files written (all inside the seat dir)

`mado-geometry.py` (reference copy, `8e871a00…`), `mado-geometry-r43.py` (`e3c2e471…`),
`project-dumps.py` (shape-only projector, `59f8f99c…`), `make-state-dumps.py`,
`build-live-states.py`, `verify-quotes.py`, `live-states.txt` (`9f6fa83a…`), `verify-quotes.out`,
`live-{clients,monitors,workspaces}.json` (projections `983c3a17…`, `a0fa6f2b…`, `4e4fb150…`),
`raw-dumps.sha256` (`33c1b5f6…`, raw hashes only), `project-dumps.out`,
`projection-invariance.txt` (`33efbb47…`), `live-clients.err`, `live-run-ref.{out,err,rc}`,
`fs2.json` (`f8833448…`), `max1.json` (`f37c3a5a…`), `live-bytes.{conf,out}` for both tools,
`runs.raw`, `dumps-built.txt`, `r43-extract.err`.
No file outside `w1/ExecLiveHost/` and this report was created or modified.

## Risk / residuals

- If a maximized or fullscreen client appears later, rerun section A's exact command; the tool's
  verdict for gkeep would then flip from `NO_MATCHING_CLIENT` to `FULLSCREEN`/`MAXIMIZED` and the
  summary gains the state pair — the same behaviour F4 shows on the dumps.
- `hyprctl` reports `size` from `GEOMETRIC_GOAL` (`fetch-c1/Hyprland-HyprCtl.cpp:427` and
  `fetch-c1/Hyprland-HyprCtl.cpp:428` feed the `size` pair), so a mid-animation size is possible in
  principle; every read here was steady-state (no transition ran during the reads).
- The verifier's `verify-quotes.out` changes whenever it is rerun (it is excluded from the receipt's
  own file listing for that reason); `verify-quotes.py` is the reproducible artifact.
