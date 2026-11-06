# R90MConnector — cross-axis and assimilation scan (round 90)

Seat: R90MConnector, leaf. Base revision `5041acf99e27263872bf0441ad5f9d4316152605`. Round cache read:
`.ufo/waves/round-90/claims-declaration-r90.md`, the C1/C2 candidates and counters, the four control files, the oracle,
`corpus/lessons/round-90.md` (in-flight), and the lane registry. Every counter/selftest run below is **DRAFT**
(`--draft-tool` / `--draft-check` / candidate `--selftest`), never a measurement; nothing was written under
`.ufo/waves/round-90/receipts/`. Scratch: `/fast/scratch/hyaku/mado-r90/R90MConnector`, created and removed
(verified absent in the final listing of `/fast/scratch/hyaku/mado-r90/`). No tool installed.

## 1. Assimilation (§10) — staged merge package `shokuknow/merge/mado`

### Id-collision check (the exact command from the seat item)

```
A=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-90/assimilation; mkdir -p "$A"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' .../corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' .../SOURCES.append.md | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"
comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"
```

Result (rc 0): **reg=435, staged=147, collisions=94**. Outputs: `.ufo/waves/round-90/assimilation/{reg-ids,staged-ids,collisions}`.

- Colliding staged ids: `S203-S221`, `S253`, `S258`, `S277-S349` (19+1+1+73 = 94).
- Non-colliding staged ids: `S222-S252`, `S254-S257`, `S259-S276` (53).
- The collisions are real content collisions, not just id reuse in the abstract: lane `S203` is the omarchy first-run
  installer (`corpus/SOURCES.md:205`), while staged `S203` is the Hyprland IPC page (`SOURCES.append.md:7`). Lane
  `S277` is the chonkstep measurement at `chriskearney/chonkstep` (`SOURCES.md:223`), staged `S277` is the same
  document under `iconidentify/chonkstep` with different row text. Lane
  `S329` is the Desktop Entry specification (`SOURCES.md:278`), staged `S329` is the XDPH registry handler
  (`SOURCES.append.md:133`).
- The merge report's own premise is stale: it says "lane registry currently holds **192** rows; first staged id is
  **S203**" (`MERGE-REPORT.md:9`), but the lane now holds 435 rows through `S500` (round-89 closure). The staged id
  space has already been consumed by later rounds.
- Duplication is not only id-shaped: 14 of the 105 unique staged URLs already appear in `corpus/SOURCES.md` under other
  ids (e.g. the Hyprland v0.56.2 `EventManager.cpp`, Waybar 0.15.0 `window.cpp`, omarchy v3.8.4 indicator scripts), and
  11 of the 69 staged knowledge targets already exist under the same path (e.g.
  `corpus/knowledge/dispatcher-semantics-r25.md`, `idle-lock-chain-armed-r14.md`,
  `request-socket-live-bound-r8.md`). The package's target list is also stale where it names files the lane never
  created this way (`focus-grab-protocol-live-on-host-r14.md` is listed; the lane holds `hyprland-focus-grab-r41.md`).

### Keyword scan (xdg-desktop-portal, portals.conf, screen sharing, GKeyFile, receipts/commit-ordering)

`grep -icE` over `MERGE-REPORT.md` + `SOURCES.append.md`: `xdg-desktop-portal` 1, `portals.conf` 0, `screen.?shar` 0,
`GKeyFile`/`gkeyfile` 0, `receipt` 0, `commit.order` 0.

The single staged entry is:

- **`S329`** — "xdg-desktop-portal-hyprland 1.4.1 — the registry handler that logs every interface the compositor
  offers", URL `.../xdg-desktop-portal-hyprland/master/src/core/PortalManager.cpp` (`SOURCES.append.md:133`).
  It is redundant against the lane's own **`S286`**, the same file pinned at **tag v1.4.1** (`corpus/SOURCES.md:235`),
  and it is *less* pinned: `master` is a moving alias, which the lane's tag-pin discipline (r88 S494; M87-2) rejects.

### Recommendation: **adopt none**

Reasons, in order: (1) 94/147 id collisions with different sources would corrupt the registry; (2) the only
portal-adjacent row (`S329`) is already held at a stricter, tag-pinned id (`S286`), and its URL is an unpinned master
alias; (3) nothing in the package speaks to C1's routing surface (`portals.conf`, GKeyFile, selection rules) or C2's
receipt/commit-ordering defect — the package predates both surfaces; (4) 11 knowledge targets already exist, so the
"append/copy" instructions would duplicate or clobber lane text. If the operator later wants a staged row, it must be
renumbered into the free range after `S500` and re-pinned; that is integration work the L1 owns, not this round.

## 2. Overlap — what C1 touches

### `corpus/knowledge/xdg-portal-routing-r12.md`

- The note holds a hand-derived routing table with **16** public-interface rows (`:43-62`), including
  **`Settings`** (`:61`) and **`Secret`** (`:62`). The declaration's basis sentence is wrong on two counts:
  "a hand-derived routing table for 14 interfaces" (`claims-declaration-r90.md:14`) and "it does not list Secret,
  Background, Wallpaper, RemoteDesktop, Clipboard, Usb, Settings" (`:16`). Secret and Settings are listed; the other
  five are absent. **Correct lines 14-16 before the freeze.** This does not weaken C1: the note is an inference
  (`xdg-portal-routing-r12.md:11`) and has no tool, no `none`/`*`/UseIn/last-resort rules and no multi-directory
  precedence; C1's draft run scores the note's rule at `r12_rule_correct=20/92`.
- C1 also *supersedes a named UNK*: the note's `Secret` row says "No matching preferred candidate evidenced"
  (`:62`). The production binary's own label for the host replica is `Secret -> []` (no backend): the last-resort
  backend (gtk) does not implement Secret, so the UNK becomes a measured `no-backend` decision. The opposite case is
  `Settings`, labelled `['gtk']` with reason `config` — the find-all rule the note does not model. After the freeze the
  note's recheck clause should point at `tools/mado-portals.py` as the re-runnable form — an L1 integration edit to
  `corpus/`, outside this seat's write scope.

### `tools/mado-globals.py` and the shared PROVINCE row

- `tools/mado-globals.py` (`PROVINCE.md:31`) reads the `xdg-desktop-portal-hyprland` journal: one `MADO_GLOBAL:` line
  per Wayland global the portal's registry callback logged (`SKILL.md:157,224,324`). That is the portal's *advertised
  interfaces/globals*, not the *configured backend per interface*. C1 is complementary, not overlapping: the journal
  says what a backend offers, C1 says what the configuration selects. No tool change is implied in either direction.
- `SKILL.md:559` answers "Which portal backend serves this?" with the round-12 rule text. Once the tool lands that
  row should route to `python3 tools/mado-portals.py`; the declaration's D2 covers "registry rows for the r87-r90
  counters and the two new instruments" but does **not** name `tools/mado-portals.py`. Extend D2 to include the tool,
  or the freeze lands a tracked tool absent from both the skill route and PROVINCE's inventory.

### PROVINCE row — drafted

The round-23 refinement states the inventory covers every tracked file under `tools/` (`PROVINCE.md:35`), so the tool
needs a row at the end of that table (after `tools/mado-watchplan.py`, `PROVINCE.md:33`). Draft text, matching the
table's grammar and the candidate's actual contract (`build/mado-portals.c1.py:1-58,489-494,581-594`; `--selftest`
uses one `tempfile.TemporaryDirectory` and passed 19/19):

```
| `tools/mado-portals.py` | the bytes of every `*.portal` descriptor and `<desktop>-portals.conf`/`portals.conf` file under the roots it is given — `--portal-dir` (one directory) or the xdg-desktop-portal search roots `--config-home`/`--config-dirs`/`--data-home`/`--data-dirs` plus `--sysconfdir`/`--datadir`, defaulting to the process environment (`XDG_CURRENT_DESKTOP`, `XDG_DESKTOP_PORTAL_DIR`, `XDG_CONFIG_HOME`, `XDG_CONFIG_DIRS`, `XDG_DATA_HOME`, `XDG_DATA_DIRS`); files read whole; symlinks followed as xdg-desktop-portal follows them; no D-Bus, no socket, no process, no compositor, no config write | nothing — stdout only (`MADO_PORTAL: <interface> -> <backend[,backend]>|none (<reason>)` per interface, `MADO_PORTALS:` summary; `--json` one object); `--selftest` writes only inside a private temporary directory it removes | mado, round 90 (read-only prediction of the backend xdg-desktop-portal 1.22.1 selects for each of the 21 `org.freedesktop.impl.portal.*` interfaces; not runtime dispatch, backend health or consent — the portal frontend remains the authority); the operator applies any config change |
```

## 3. `considerthese/2026-11-06.md` proposals 1-7 against round 90

| # | proposal | status | evidence |
|---|---|---|---|
| 1 | Carry a survivor ledger across quiet days | **acted, continued** | The r87 survivors M03/M05/M06/M08/M10 were carried byte-equal into the r88 mutant set (`claims-declaration-r88.md:65`) and killed there (`corpus/lessons/round-88.md:108`: `22/22 killed`). The r89 survivors RS01/RS05/RS12 are routed into r90 as `tools/mado-mako.py --selftest` cases (declaration routed item D3). |
| 2 | Always quote verdict before score | **acted; moot for r90** | `c1-r89-mako-regex.py:203` emits `score_scope=finite-cases`; the r90 counters print no `score=` at all (counts only, `c1-r90:272`, `c2-r90:164-166`). |
| 3 | Read-only live check of `mado-mako.py` against João's theme files | **partially acted; specific comparison open** | r88 C1 replayed the host's `core.ini` chain (`receipt-base-host-config-r88.txt`; QUALITY 146). r90 repeats the discipline for portals: the oracle is the production binary, and the draft run scores 92/92 against its labels. The makoctl-vs-resolver comparison the proposal names is still not done. |
| 4 | Widen desktop coverage past bar + mako | **acted on the routing half** | C1 is the portal plane the r88 lesson named uncovered. Still open from the proposal: `xdph.conf` (screen-share picker — `SKILL.md:85` remains the only pointer), clipboard, window-rule live match (only inventory/effect reads), non-bar exclusive surfaces, hypridle volatility. |
| 5 | Verify QUALITY 145 has an instrument | **open** | `quality/check-wave-done.py` exists (54,002 B) and QUALITY 103 binds its receipt (`corpus/QUALITY.md:569,572`), but no instrument reads a *claim row's* settlement state, which is 145's subject. C2 is receipt presence, not wave telemetry; r90 does not close 145. |
| 6 | Keep fetching LOG/SCORECARD by round header | **process, N/A** | Habit, not a lane artifact; continued here (targeted greps only). |
| 7 | Ask João about the tracked `eventq-live-ss.txt` receipts | **open** | Both paths are still tracked at the base revision (`git -C <lane> ls-files .ufo/waves/round-37/receipts/eventq-live-ss.txt .ufo/waves/round-38/receipts/eventq-live-ss.txt` returned both). Removal is a tree decision; outside every seat's write scope. |

## 4. Patterns — shared failure classes with rounds 86-89

### 4.1 Crash-is-not-a-kill (r88) — both r90 counters regress it (the mistake to mine)

Round 88 fixed this class in its C1 counter: `c1-r88-mako-fields.py:202-208` defines `CRASH_PREFIXES` and states "a
crash is not a kill"; `:279-281` prints `crashed-not-killed`; `:563-566` selftests it. The r88 lesson records it as a
medium finding, "fixed (crash-is-not-a-kill, both counters)".

Round 90's counters do not have the guard:

- C1: `run_tool` returns `None` on a non-zero exit or bad JSON (`c1-r90-portal-routing.py:97-112`), `case_correct(None)`
  is False (`:114-116`), and any first failing case marks the mutant killed (`:249-255`). A mutant that breaks the
  import therefore "kills" on every case.
- C2: `run_check` judges only rc/missing/cited (`c2-r90-receipt-presence.py:42-51`), `evaluate` marks an expectation
  failed on any mismatch (`:75-86`), and any failed expectation marks the mutant killed (`:138-139`). A check that
  crashes without output fails the first expectation (D88 expects rc 1 **and** a missing set).

Reproduced with a doctored mutant file (DRAFT run, temp files under this seat's scratch):

```
# C1: {"id":"X-crash","find":"IFACES = [IMPL + \".\" + n for n in (","replace":"raise SystemExit(2)\n..."}
mutant X-crash killed by d01-host-replica (import-time crash)
MADO_PORTAL_ROUTING: DRAFT_TARGET_MET ... cases=92 correct=92 mutants=32 killed=32 ...
# C2: {"id":"X-crash","find":"from __future__ import annotations","replace":"raise SystemExit(1)"}
mutant X-crash killed by D88 (import-time crash)
MADO_RECEIPT_PRESENCE: DRAFT_TARGET_MET ... expectations=15 met=15 mutants=14 killed=14 ...
```

The frozen 31/13 mutant sets are all killed by genuine cases in the draft run (C1 `M33` by `x02`, C2 `K13` by
`W10`), so this is latent for the current bytes — but the instrument cannot tell a semantic kill from a crash, which
is exactly the class r88 admitted and fixed. **Pre-freeze repair:** classify a mutant whose execution does not yield a
well-formed verdict on a sentinel case as `crashed-not-killed` (no kill credit), add the one-line selftest, and keep
the printed `killed` count unchanged for the frozen set. Mirror `c1-r88-mako-fields.py:202-208/563-566`.

### 4.2 Declared-vs-counted mutant population (M86-6, r83/r89)

C1 separates the two equivalent mutants into a top-level `equivalent_not_counted` list (M07 `*` does not stop the list,
M11 UseIn desktop order) with arguments, while `mutants` holds the 31 counted ones; the counter uses
`len(mutants)` (`c1-r90:231,270`) and prints `mutants=31`. This is consistent, but the receipt cannot show the
exclusion. Cheap hardening: print `mutants_counted=31 equivalents_not_counted=2` from the same JSON so a later reader
cannot re-count 33 (the r83/r89 arithmetic-failure shape). Pure formatting; no predicate change.

### 4.3 Label provenance and pins (M87-2, M87-5)

C1 labels cases with the production binary and records **both** `host_tail_sha256` and `oracle_binary_sha256`
(`controls/portal-cases-r90.json` top level). The counter verifies the config tail (`c1-r90:227-230`, plus the
`/etc/xdg-desktop-portal` absence guard) but **never reads `oracle_binary_sha256`**. A package upgrade between
labelling and scoring would leave the labels bound to a different binary while the run still reports `TARGET_MET`.
Either verify the binary digest at score time (one `sha256sum` of `/usr/lib/xdg-desktop-portal`) or name it in the
declaration's limits. This is the r87-M87-2 class (a pin named but not the bytes it was computed from) in its mildest
form. Pins for cases and mutants are present and enforced (`:218-221`), and the tool itself must be the `--rev` blob
(r89 M87-5's "pin-free fixture set" class is otherwise closed).

### 4.4 Fixture construction and schema drift (M90-1, M88-2)

M90-1 (r90's own lesson) already mined the host-file-without-final-newline merge; the fix control
`controls/check-fixture-lines-r90.py` exists, and it passes on the frozen file:
`python3 -I controls/check-fixture-lines-r90.py controls/portal-cases-r90.json` → `FIXTURE_LINES: cases=92 merged=0
verdict=CLEAN`, rc 0. C2's fixture builder asserts the
fixture toplevel and commits with an in-fixture identity (`c2-r90:56-72`), matching the fixture rules.

One residue of the r88 c51 class (an unknown arg key refused by the loader) is *not* present in C1: `materialise`
reads only `desktop`, `mode`, `files` (`c1-r90:70-95`) and ignores unknown case keys, and the loader checks only for
`oracle`/`oracle_reason` (`:222-223`). A typo'd intent key would produce a case that still runs and is labelled
truthfully but tests something else silently — the same shape as M90-1. Low risk; a per-mode allowed-key check would
close it.

## 5. Other risks / second-order effects

1. **Declaration basis error** (lines 14-16): 16 interfaces, Settings and Secret listed. Fix before freeze; the claim
   itself is intact (no tool at base; the note's rule scores 20/92).
2. **Tool absent from governance**: `tools/mado-portals.py` is not in D2, and PROVINCE has only the `mado-globals` row.
   Draft row in §2; extend D2 to the tool.
3. **C2 scope excludes `.ufo/reports/`**: `RECORD_FILES` (`check-receipt-presence.c2.py:39`) covers SCORECARD, LOG,
   QUALITY, README, lessons and knowledge, not round reports. Round-89's report commit is separate from the records
   commit, so the check would not catch a report citing an uncommitted receipt. Name the limit or add
   `.ufo/reports/round-*/*.md`.
4. **C1 `next(...)` on `d01-host-replica`** (`c1-r90:257`): a renamed/absent case id raises `StopIteration` (traceback,
   rc 1) instead of the declared SetupError rc 2. One-line fix.
5. **`host_table_correct` is a label-diversity control, not a tool**: it counts cases whose oracle vector equals the
   host replica (`c1-r90:258`), so it guards against a host-only case set rather than scoring a "host table" tool. The
   receipt prints it, so this is transparent; it should be described that way if the declaration is amended.

## 6. Commands run (DRAFT runs labelled)

| command | result / exit |
|---|---|
| collision check (exact item command) | rc 0; reg=435 staged=147 collisions=94; `assimilation/*` written |
| keyword greps over `MERGE-REPORT.md` + `SOURCES.append.md` | rc 0; only `S329` (xdg-desktop-portal); all other patterns 0 |
| URL/knowledge-target overlap (python over the two registries) | rc 0; 14/105 URLs, 11/69 targets already held |
| `python3 -I build/mado-portals.c1.py --selftest` | rc 0; `MADO_PORTALS_SELFTEST: checks=19 failed=0` |
| `python3 -I controls/check-fixture-lines-r90.py controls/portal-cases-r90.json` | rc 0; `FIXTURE_LINES: cases=92 merged=0 verdict=CLEAN` |
| `c1-r90-portal-routing.py --draft-tool ...` (pins recomputed) | **rc 3 (DRAFT)**; `DRAFT_TARGET_MET cases=92 correct=92 mutants=31 killed=31 r12_rule_correct=20 host_table_correct=10 base_tool=absent base_correct=0` |
| `c2-r90-receipt-presence.py --draft-check ...` | **rc 3 (DRAFT)**; `DRAFT_TARGET_MET expectations=15 met=15 defects_detected=2/2 mutants=13 killed=13 base_check=absent base_defects_detected=0/2 always_ok_met=7/15 always_missing_met=0/15` |
| crash-mutant reproduction, C1 / C2 (doctored copies in scratch) | **rc 3 (DRAFT)** both; `X-crash killed by d01-host-replica` / `killed by D88`; `killed=32/32` / `14/14` |
| scratch removal | `/fast/scratch/hyaku/mado-r90/` no longer lists `R90MConnector` |

No measurement, no receipt under `.ufo/waves/round-90/receipts/`, no install, no mutation outside this seat's scratch.
