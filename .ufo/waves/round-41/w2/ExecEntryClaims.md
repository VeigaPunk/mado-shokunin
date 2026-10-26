# Seat report — ExecEntryClaims (round 41, wave w2, mado-shokunin)

Seat type: executor (attack). Assignment: attack every OBS/INF line of the landed entry
`corpus/knowledge/hyprland-focus-grab-r41.md` (DATA commit
`07f2641696b5ac73de1404ea737a9f27e9819aa1`) against the receipts and the host.
Full check table: `.ufo/waves/round-41/w2/ExecEntryClaims/claims.md`.

## Findings (scoped)

**1 defect found (minor, wording) — F1, entry line 85 (§4, OBS on `FocusGrab::addWaylandWindow`):**
"adding a window records it and *defers* the protocol call" is overstated: in
`fetch/quickshell-grab.cpp:65-69` the client sends `add_surface` **immediately** (line 66)
before appending to `pendingAdditions`; only the `commit` is deferred. The quoted string is
verbatim and "`sync()` is the only place that commits" is true (:75). No protocol fact is
broken (decision-table row L122 stays correct), but the sentence misstates the deferral point.
Suggested wording: "records it and defers the commit (`add_surface` is sent immediately)".
This is a DATA-level wording defect for the L1 to integrate; it does not touch any claim
about the protocol, the compositor, the host, or the counts.

**Everything else: no defect found.** All quoted strings, `file:line` locators, counts,
pins, host facts, and UNK designations verified.

## Evidence (exact)

- Counts (recomputed by script over `fetch/xdph-journal.txt`): portal sessions=2
  (pids 1918, 1952); adverts 15 + 63 = 78; distinct names session 2 = 63 with zero
  duplicates; distinct names session 1 = 8; `hyprland_focus_grab_manager_v1` adverts = 1
  (ver 1, journal:117); case-insensitive "focus" in whole journal = 1 (the advert line).
- `grep -in focus xdph-PortalManager.cpp` exits 1 (no "focus" anywhere in the portal file);
  `onGlobal` is lines 85-261 with the log line at :88, exactly ten bind branches
  (:90, :95, :99, :102, :108, :113, :122, :246, :249, :257), none a focus-grab manager.
- `hyprctl version` (host): "Hyprland 0.56.2 built from branch v0.56.2 at commit
  efb50993780079460b0cbed1363e2166a2de1d9f" — exact substring; same commit as S284 pin.
- Installed package: `/var/lib/pacman/local/xdg-desktop-portal-hyprland-1.4.1-2/desc`
  sha256 `7bf2f8be…` (matches receipt), `%NAME% xdg-desktop-portal-hyprland`,
  `%VERSION% 1.4.1-2`.
- Upstream pin byte-identity: git fetch at the exact pins → `git show FETCH_HEAD:<path>`
  sha256 equals local receipt for S283 (xml), S284 (cpp+hpp), S285 (grab.cpp), S286
  (PortalManager.cpp @ v1.4.1), S288 (README.md); S289 journal sha256 `bf8fa91a…` ✓.
- Issue #565 receipt: `"state":"CLOSED"`, createdAt 2022-08-23T14:03:55Z, maintainer
  "fixed in b09f157" on Aug 26, 2022; all four body/log quotes present verbatim.
- Base-lane INF (at `ab2bfaab…`): master grep exits 1; `window-rule-effects-getprop.md`
  and `workspace-rules-r27.md` have no `focus` line; `rule-attribution-r24.md` single hit
  = line 81 (`jetbrains-focus`).
- UNK audit: all five UNKs are genuinely unanswerable from the receipts under lane/host
  constraints (no SeatManager.cpp in receipts; no own Wayland client or input injection
  permitted; issue #565 predates 0.56 line).

## Commands (all read-only; in claims.md §4)

`git show 07f2641…:corpus/knowledge/hyprland-focus-grab-r41.md`; `sha256sum *` in fetch/;
python3 count script on xdph-journal.txt; `grep -in focus` on PortalManager.cpp (exit 1);
`hyprctl version`; `sha256sum /var/lib/pacman/local/…-1.4.1-2/desc`; `git fetch --depth 1`
+ `git show` byte-compares for the five pins; `git grep` at base for the §5 INF.

## Tooling / installs

None. No package or tool installed (only pre-existing git, python3, sha256sum, grep).

## Risks / blockers

- GitHub issue HTML has not been byte-compared to a fresh fetch (non-deterministic page);
  its content, state, and dates were verified in-place.
- The §5 grep was verified at the stated base commit, not the working tree (the working tree
  now contains the entry itself, which legitimately matches the pattern).
- No blockers. Assignment complete; L1 to integrate F1 (optional wording fix).
