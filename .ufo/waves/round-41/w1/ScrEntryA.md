# ScrEntryA — C2 entry, Draft A (round 41, w1)

STATUS: complete for this seat. Draft written, every quote and every simulated clause checked. One
integration dependency on the L1 (a new fetch receipt for the held row S037) is flagged below with its
fallback.

## What was produced

| path | what it is |
|---|---|
| `.ufo/waves/round-41/w1/ScrEntryA/hyprland-focus-grab-r41.md` | the entry draft (destination `corpus/knowledge/hyprland-focus-grab-r41.md`, the L1 copies it) |
| `.ufo/waves/round-41/w1/ScrEntryA/gates.txt` | 8 ready `GATE …` lines (column 0) for `corpus/lessons/round-41.md` `## Gate` |
| `.ufo/waves/round-41/w1/ScrEntryA/s037-installed-version.txt` | the S037 Gate receipt, to be committed at `.ufo/waves/round-41/fetch/xdph-installed-version.txt` |
| `.ufo/waves/round-41/w1/ScrEntryA/check-quotes.py` | verifies all 30 quotes against their receipts with the counter's `norm()` |
| `.ufo/waves/round-41/w1/ScrEntryA/check-entry.py` | simulates clauses b, g, h over the draft (the real counter needs a committed rev) |
| `.ufo/waves/round-41/w1/ScrEntryA/make-gates.py` | emits and verifies `gates.txt` against the counter's `GATE_RE` |
| `.ufo/waves/round-41/w1/ScrEntryA/quotes.txt` | the last quote-check transcript (`ids=8 quotes=30 failed=0`) |
| `.ufo/waves/round-41/w1/ScrEntryA/entry-check.txt` | the last clause-simulation transcript (`SIMULATED b/g/h -> OK`) |

No tracked file was edited; no git/jj mutation; nothing written outside the seat directory.

## Behaviour of the draft

Five parts, in the order the assignment named them:

1. **§1 protocol surface (S283)** — both interfaces, the five requests and the `cleared` event as a
   table, plus the transition rule ("empty -> non-empty starts") quoted from `commit`.
2. **§2 compositor semantics (S284)** — the grab object allocates a `CSeatGrab` with keyboard and
   pointer, installs it on the seat, finishes itself from the seat-grab callback with `finish(true)`,
   sends `cleared` only when the flag is set, and runs the three-state surface machine; a surface
   destroy routes to `eraseSurface` → `commit(true)`, so destruction cannot re-add.
3. **§3 host advertisement (S289, S286, S037)** — one advert of `hyprland_focus_grab_manager_v1 (ver 1)`
   at `2026-10-25T13:36:24-03:00` pid 1952; the portal logs every global and binds ten named ones, none
   of them this manager; `focus` occurs once in the whole journal (the advert line itself).
4. **§4 client lifecycle (S285)** — quickshell defers the protocol call into `pendingAdditions` +
   `commitRequired`, commits inside `sync()` under a transaction guard, flips `active` after a commit,
   and mirrors `cleared` back to `active = false`.
5. **§5 rule-level counterpart (S287, S288)** — issue #565's `silent` workspace rule, the "steal it
   momentarily" report, the compositor's own "Tried to set workspace silent rule to a nofocus window!"
   log line and the 2022 "fixed in b09f157"; the README's statement that the protocol set exists because
   wayland-protocols is slow to change.

Plus §6 the required `question | where the answer lives | state` table (12 rows) and §7 the limits.

Header: 8 `source:` lines inside the first 20 lines (S283–S289 new, S037 held), `verified-at: 2026-10-25`,
`recheck: 90d - …`, `ground:`, `Lane: mado-shokunin. Round: 41.`, `assimilated-from:` naming the two
package entries and excluding `focus-control-surfaces-r28` §3 (localized channel).

The census line appears exactly once, outside fences, as its own line:

```
journal sessions=2 adverts=78 interfaces=63 focus_grab=1
```

## Evidence exercised this seat

- **Receipt hashes re-computed** (`sha256sum` over `.ufo/waves/round-41/fetch/*`): `focus-grab-v1.xml`
  `0bc60c14…c0285b4`, `Hyprland-FocusGrab.cpp` `53b762f7…b092aff1`, `quickshell-grab.cpp`
  `6f7cecf1…a301a40`, `xdph-PortalManager.cpp` `15c3e39c…091ea55`, `issue-565.html` `148a9053…679d1dc`,
  `protocols-README.md` `3c700763…7aa6323`, `xdph-journal.txt` `bf8fa91a…600aaf7`.
- **Journal census re-derived** with the counter's own ADVERT/BOOT grammar (a local re-implementation,
  not the counter): sessions 2 (pid 1918, 15 adverts, a slice that opens mid-stream; pid 1952, 63
  adverts), adverts 78, distinct names in the latest session 63, `hyprland_focus_grab_manager_v1`
  adverts 1, no duplicate name in the latest session. Matches the declared census line exactly.
- **Portal bind set counted**: `CPortalManager::onGlobal` spans `xdph-PortalManager.cpp:85-261` and holds
  10 `_interface.name` branches (screencopy, global shortcuts, input capture, xdg-output, toplevel
  export, `wl_output`, dmabuf, `wl_shm`, foreign toplevel, toplevel mapping).
- **Portal does not use it**: `grep -in focus xdph-PortalManager.cpp` exits 1; `grep -c focus
  xdph-journal.txt` is 1, on the advert line.
- **Host compositor identity**: `hyprctl version` (the only hyprctl verb run) printed
  `Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f` — the
  same commit S284 is pinned at. Recorded in §3 as a dated measurement, not a registry row.
- **Installed portal identity (S037)**: read-only read of
  `/var/lib/pacman/local/xdg-desktop-portal-hyprland-1.4.1-2/desc` (sha256 `7bf2f8be…c9445a5`) —
  `1.4.1-2`. No pacman command was run.
- **Base absence re-checked**: `grep -rli 'focus_grab\|focus-grab\|focus grab' corpus PROVINCE.md
  SKILL.md tools` exits 1; `window-rule-effects-getprop.md` and `workspace-rules-r27.md` carry no
  `focus` line, `rule-attribution-r24.md`'s only hit is the block rule name `jetbrains-focus`.
- **Quotes**: 30 quotes, all 8 ids, all ≤ 25 words, all verbatim under the counter's `norm()`, all
  distinct; `check-quotes.py` exit 0 (`quotes=30 failed=0`).
- **Simulated clauses**: `check-entry.py` — b pass (8 ids, `verified-at`, `recheck` matches
  `^90d\s`), g pass for all 8 ids (the Gate quote sits on a line that names the id, outside fences),
  h pass (one census line, counts equal to the parsed journal), no localized-channel string, `S290`
  not cited. `exit=0`.

## Gates I did not run (and why)

- `python3 -I quality/counters/c2-r41-focus-entry.py --repo . --rev <rev>` — needs a committed revision;
  the draft is untracked, and committing is the L1's. `check-entry.py` simulates b/g/h only.
- Clauses c, d, e, f, i depend on other seats' files (`corpus/SOURCES.md` rows, the lesson `## Gate`,
  `corpus/README.md` index) and were not run.

## Integration dependencies (L1)

1. **S037's Gate receipt is new.** The counter requires each cited id's Gate receipt to be committed
   under `.ufo/waves/round-41/fetch/`, and no round-41 receipt carries the installed release identity.
   Copy `.ufo/waves/round-41/w1/ScrEntryA/s037-installed-version.txt` (1442 B, sha256
   `4294737aa884fd84c2e2a6bf642efa71c281bc480df4f07eb64009d812157ea8`) to
   `.ufo/waves/round-41/fetch/xdph-installed-version.txt` byte-identically; `gates.txt` already names
   that path.
   **Scope caveat (also stated in the entry, §3):** this receipt grounds the *installed* package version
   (1.4.1-2), not S037's release-page anchor; the tag `v1.4.1` / commit `cc8e5ef` remain S037's own row
   and were not re-fetched this round. ScrRowsDraft confirmed the receipt satisfies clause d
   independently (1442 B ≥ 512 B, distinct path and sha, quote present under `norm()`).
   **Routed to the L1:** ScrLessonSkeleton verified the sha and the quote but declined to copy the file
   (its write scope is its seat dir; a tenth receipt is a freeze-adjacent decision), so the copy and the
   commit of `fetch/xdph-installed-version.txt` are the L1's to make. The lesson draft carries the exact
   landable S037 line in a comment above `## Gate` and mistake M41-6 recording why the receipt is required.
   Clause i lines the lesson now holds: `ADMIT merge/mado/knowledge/corpus/knowledge/focus-grab-protocol-live-on-host-r14.md as corpus/knowledge/hyprland-focus-grab-r41.md`,
   plus two REFUSE lines (`privileged-client-surface-r29.md`; `focus-control-surfaces-r28.md` on its
   section 3 localized channel).
   **Fallback if refused:** delete the `source: S037` line from the entry header and the S037 paragraph
   in §3, and drop the S037 GATE line; S037's used-by must then not list the entry. Everything else
   stands — the entry then cites 7 ids (all new) and still satisfies clause c's `>= 2` new ids and
   clause h's single own-work row.
2. **S290 is not cited** by this draft (input capture appears only through S286's bind branch). S290's
   used-by must not list this entry; ScrRowsDraft was told.
3. Gate lines: `gates.txt`, one per id, column 0, not indented — told to ScrLessonSkeleton together with
   the clause-i `ADMIT`/`REFUSE` requirement. The lesson side confirmed it now carries the seven committed
   lines plus the three clause-i lines, states that the landed `## Gate` must hold exactly eight GATE lines
   (those seven + S037), and holds S037's landable line in a comment above the section. Its re-runnable
   verifier for the L1: `python3 -I .ufo/waves/round-41/w1/ScrLessonSkeleton/quotes.py --repo . --rev <data
   commit> --lesson corpus/lessons/round-41.md` (reads 7 now, 8 once S037's receipt is committed).

## Findings worth the judge's attention

- **The portal's non-use is the strongest single fact in §3**: the advert exists because `onGlobal`
   logs every global before branching, and the file has no `focus` string at all. A reader who assumes
  "advertised to the portal" means "the portal can use it" is wrong, and the entry says so with both
  halves (log line + absent bind).
- **The first journal session is a slice, not a session.** 15 adverts against 63; treating the two as
  comparable would understate the compositor's global set. The entry states this instead of quoting a
  raw total.
- **`finish(false)` in the destructor vs `finish(true)` in the seat-grab callback** is the asymmetry
  quickshell's comment leans on ("the protocol will always send cleared() when the grab is deactivated,").
  It is why the entry's §2 and §4 have to be read together.
- **Issue #565 is a 2022 record** and cannot support a 0.56.2 behaviour claim; §5 uses it only for "the
  rule layer decides focus and can be wrong", and §6/§7 mark the current-release question UNK.

## Out of scope / not done

- No Wayland client was run, no compositor socket opened, no input injected: no live grab, no bind
  attribution, no focus transition measured.
- `CSeatGrab`'s own routing (how an outside event is dropped or forwarded) was not read; §2 marks it UNK.
- No claim about sandbox/permission gating beyond "the receipts show none".
- The staged package and the Japanese-channel section of `focus-control-surfaces-r28` were not opened
  for content; only the registration's exclusion was applied.

## Tooling

No tool was installed or updated this seat: everything ran on the system `python3` with the standard
library (`hashlib`, `html`, `re`) plus coreutils (`sha256sum`, `grep`, `awk`, `ls`). No pacman, no
package transaction, no `-Sy`/`-Syu`.
