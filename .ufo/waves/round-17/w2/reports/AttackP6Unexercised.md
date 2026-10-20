# AttackP6Unexercised — round 17 wave 2 (critic)

Target: `corpus/knowledge/idle-lock-route-r17.md` (the "route" below) at lane HEAD `988b858`, against `corpus/knowledge/idle-lock-plane.md` §11 (the "plane" below) and the C2 claim "rubric V 2/6 → 4/6 (P6 new)".
Method: I read lane files and git blobs. I fetched the seven tag-pinned raw files and both wiki pages again with `curl`, into `/tmp/ap6`. Host files were read as bytes only (`cat`, `sed`, `sha256sum`, `grep`). I ran `measure.py 988b858` and one mutant measure in a `/tmp` clone. I ran `sources-census.sh validate`. Installs: none. No live probes, no pacman/sudo/systemctl/hyprctl.

Axes: **I1** implied observed behaviour · **I2** implied host version or protocol support · **I3** `[UNK]` completeness vs plane §11 · **I4** honesty of the "P6 covered" label · **I5** provenance integrity (hashes and anchors).

## Verdict summary

| # | Attack | Result | Axes |
|---|---|---|---|
| A | S066 raw digest recorded in SOURCES and the lesson gate | **Counterexample**: one hex digit is wrong | I5 |
| B | `[UNK]` list complete relative to plane §11 | **Counterexample**: 4 of 8 items have no disposition, and one citation is false | I3, I5 |
| C | Route implies observed behaviour | **Partial counterexample**: three unstated inferences and one under-read source path. No outright observation claim | I1 |
| D | Route implies host version or protocol support | **Attack failed**: hedged correctly | I2 |
| E | "surface: P6 covered" is an honest label | **Holds only structurally**: a mutant that claims observation is still counted as covered | I4 |
| F | Host hashes, code anchors, pacman.log join | **Attack failed**: everything re-verifies | I5 |

## A. S066 digest mismatch (false provenance)

- Recorded value: `2dd4d73d4f5cd57ed5a2e7d10d630bdcfa0dbdd87e7a9819bb1d1cdd4dfb2d75`. It appears at `corpus/SOURCES.md:78` (S066 anchor cell) and at `corpus/lessons/round-17.md:53` (§ Gate).
- Observed value: `curl https://raw.githubusercontent.com/hyprwm/hypridle/v0.1.8/src/core/Hypridle.cpp` on 2026-10-20 gives `2dd4d73d6f5cd57ed5a2e7d10d630bdcfa0dbdd87e7a9819bb1d1cdd4dfb2d75`. Character 9 is `6` in the file and `4` in the record.
- Three wave-1 seat reports independently recorded the correct `…6f5c…` value:
  - `w1/reports/SrcHypridleSrc.md:20` (29880 B, 735 L)
  - `SrcIdleNotifyProto.md:87` (checked with `cmp` against the tarball member)
  - `SrcLogindLock.md:23`
- The wrong digit enters at `drafts/NoteIdle-rows.md:25`. It then propagates to `gen_w2.py:50`, the SOURCES row, and the lesson gate.
- Every other S063–S069 digest matches my fetch exactly.
- Impact:
  - The route's head (lines 2–3) sends rechecks to "compare raw SHA-256 with corpus/SOURCES.md S063-S069". That comparison will report false drift for S066, the code row that carries most of the route's `[HC:n]` anchors.
  - `sources-census.sh validate` reports `mado ok`, and `measure.py` does not hash cited rows. Nothing in the gate caught it.
- Smallest correction: an erratum line in `lessons/round-17.md` and a one-digit fix in the S066 anchor cell (`4f5c` → `6f5c`).

## B. `[UNK]` completeness vs plane §11 (plane:327-345)

| §11 item | Route disposition | Finding |
|---|---|---|
| 1 why hypridle not running | route:129 | Stale. It calls this "not running at probe time" and ignores plane E2 (plane:364-382): hypridle was observed launched by autostart in a fresh session, then absent again. Its claim "This note **adds** the declared start route" is false novelty, because plane §3 (plane:110-111) already records `default/hypr/autostart.conf:1` as `[OBS]`, and so does `hyprland-config-plane.md:157-158,189-190`. |
| 2 live transitions / ≈302 s | route:124-125 | Present. |
| 3 who writes logind `IdleHint`/`LockedHint` | **absent** | No disposition at all. |
| 4 configs parse cleanly | **absent** | Not addressed, yet route:86 and :98 ("Not set, so defaults apply") assume the files load. The item was narrowable from sources: every key in host `hypridle.conf` is registered at v0.1.8 (`src/config/ConfigManager.cpp:59-75`), and every key in `hyprlock.conf` is registered at v0.9.6 (`ConfigManager.cpp:236-258`, with `shadow_passes` coming from the `SHADOWABLE` macro at :235-239, and :244-253 for general/auth). |
| 5 cursor restore if hyprlock is killed under `cursor:invisible` | **absent; false citation** | route:125 cites "`idle-lock-plane.md` §11 items 2, **5**" for "listener firing and on-resume execution". Item 5 is the screensaver-trap cursor question (plane:338-341), not on-resume. |
| 6 `inhibit_sleep = 3` | route:127 | Present, but understated (see C4). |
| 7 waybar idle indicator rendering | **absent** | Wave-1 `ExistingIdleNotes.md:242` said "already bounded; do not reopen". The route should still name the disposition (X-C01 "every item is named with its state", `ExistingIdleNotes.md:155`). |
| 8 multi-monitor | route:133 | Present. |

- Wave-1 had already prepared dispositions for 3, 4, 5 and 7 (`ExistingIdleNotes.md:238-242`). The final note dropped them without saying so.
- Route:12 claims §11 "is the open list this note narrows", so the gap is an omission inside the note's own stated scope.
- Smallest correction: one `[UNK]` line per missing item with its disposition:
  - 3: contract-only, not narrowed.
  - 4: keys registered at tag, parse unobserved.
  - 5: not narrowed.
  - 7: bounded by S053/S054.

  Also fix the route:125 citation to "item 2". Change route:129 to cite plane E2 and drop "adds".

## C. Implied observation or unstated inference (I1)

No sentence asserts that something was observed on the host. The disclaimers at route:8-10 hold. Four places, however, state host behaviour from bytes without the needed anchor or label:

1. **Command-to-path binding.**
   - route:73-75 says `omarchy-system-lock` is "called by hypridle.conf:2-3, 17". The config uses bare names; resolution to `~/.local/share/omarchy/bin/` depends on hypridle's runtime `PATH`.
   - The only declaration is `~/.config/uwsm/env:5` (`export PATH=$OMARCHY_PATH/bin:$PATH:$HOME/.local/bin`), which the route does not cite. The process environment is unobserved.
   - Correction: cite `uwsm/env:5`, mark the binding `[INF]`, and add `[UNK]` for the runtime PATH.
2. **Shell semantics.**
   - route:83 ("the env var suppresses the display-off branch") and route:87 (`pidof hyprlock || …`) only work if hypridle runs commands through a shell.
   - That is true at the tag: `Hypridle.cpp:289` `CProcess proc("/bin/sh", {"-c", args})`. The route never cites it.
   - Correction: add `[HC:289]`.
3. **Defaults and authority.**
   - route:86 and :98 take defaults from the "Latest git" wiki and apply them to a v0.1.8 / v0.9.6 host. route:130 itself says wiki-to-tag agreement is `[UNK]`.
   - I checked the tag sources. The values agree: hypridle `ConfigManager.cpp:68-75` (ignore_* = 0, on_lock/unlock = "", inhibit_sleep = 2), and hyprlock `ConfigManager.cpp:244-253`. So the content survives, but the cited authority is the unpinned wiki.
   - route:98 lists "`grace` not set: defaults apply [LW:37, 49, 54]". `grace` is not a config key at v0.9.6: there is no `grace` string in `src/config/ConfigManager.cpp`. It is CLI-only (`--grace`, route:57, [LW:16]), and none of the cited anchors cover it. This is a category error.
4. **Under-read `inhibit_sleep = 3` path.**
   - When `lockNotifier` is null, case 3 (`Hypridle.cpp:128-130`) leaves `m_inhibitSleepBehavior` unassigned. The member is an enum with no initializer (`Hypridle.hpp:67-71`), and the constructor (`Hypridle.cpp:16-22`) does not set it.
   - Per the tag source, the fallback is indeterminate, not a clean "does not wait". route:41 and :127 frame it as binary.
   - Separately, route:41 attributes the label "wait until locked" to [HW:22-26]. The wiki table says "3: lock notify". The phrase comes from the HC:128 comment and the host hypridle.conf:5 comment.
   - Correction: one clause on route:127 citing HH:67-71 and HC:128-130.

## D. Host version and protocol support (I2) — attack failed

- **Protocol claims:**
  - route:61 cites upstream statements only ([LR:5] ext-session-lock, [HR:5] ext-idle-notify-v1).
  - Host lock-notify support stays `[UNK]` (route:127).
  - The precondition is quoted verbatim ([HC:104-107] matches).
- **Version claims:**
  - route:109 binds the tags to `/var/log/pacman.log:1792` (`hypridle 0.1.7-10 -> 0.1.8-2`) and `:1798` (`hyprlock 0.9.6-1 -> 0.9.6-3`). I re-read both lines; they are the last hypridle/hyprlock lines in a 3160-line log.
  - The route explicitly declines a running-binary claim (route:109, :134). That is more conservative than the plane's earlier `pacman -Q` reading (plane:113), and does not contradict it.

## E. Is "surface: P6 covered" honest? (I4)

- **Reporting prose is honest.**
  - `corpus/README.md:42` reads "Documentary upstream contract … Declared timings are not observed behaviour".
  - `README.md:120` says "**documentary** sourced ground".
  - The rubric was pre-declared as documentary (`gen_w1.py:14`, "two NEW sourced documentary route notes").
- **The counted label is grade-blind. Mutant proof:**
  - In a `/tmp/ap6/lane` clone at `988b858`, I kept the route's 15-line head and replaced the body. The new body had a content-free `## Upstream contract` and a `## Host declaration` claiming "hypridle observed running; listener fired at 150 s on this host (OBSERVED)", "hyprlock took the session lock; hyprland-lock-notify-v1 supported", and "host binary is hypridle 0.1.8". `## Unexercised behavior` held a single `- [UNK] nothing`.
  - After committing, `measure.py HEAD` returned `count 4`, P6 `covered: True` (`reason: surface: P6`), and `rejected: []`.
  - So rubric V passes any note with the right headings, ≥3 lines per section, one `[UNK]`, and a mined tier-A upstream row.
  - It cannot tell documentary claims from observed ones. It does not check `[UNK]` completeness against the plane's open list (B). It does not verify cited digests (A).
- **The "4/6" mixes evidence grades.** It adds two documentary-only routes (P4, P6) to legacy P1/P2 credit under one undifferentiated count.
- Classification: this is a tradeoff the judge must weigh, not a defect in the note. "P6 covered" is honest only as "P6 documentary-route present (rubric V, structural)". Every honesty property of the actual note rests on prose that the instrument does not judge.
- Smallest correction: carry the grade into the claim and receipt, for example "C2 4/6 (P4, P6 documentary; host behaviour `[UNK]`)". A future rubric could reject `observed|OBS\]` tokens outside `[UNK]` lines in `surface:` notes. Do not widen the instrument this round.

## F. Re-verifications that held (attacks failed)

- **Host bytes.** All nine digests at route:70-78 match current bytes: the seven table files, `~/.config/hypr/autostart.conf` `5ace1701…`, and `hyprland.conf` `ce7483f3…`. Line counts match (lock 33, wake 9, screensaver 59, default autostart 16). The quoted lines `hypridle.conf:2-5,9-19`, `omarchy-system-lock:8-33`, `omarchy-system-wake:8-9`, `default autostart.conf:1` and `hyprland.conf:4` match exactly.
- **Code anchors.** All `[HC:n]` anchors match their cited lines: 58, 70, 71, 74, 104-107, 120, 128-129, 301, 327, 346-348, 352, 402, 404, 433, 473, 477-478, 480, 485, 493, 504, 509-510, 600, 601, 617, 626. Also [HH:23], [HH:26], [HM:61], [HR:5, 16, 20, 28-29, 62] and [LR:5, 19].
- **Wiki bytes.** The raw sha256 values match S063/S064 (`b45c03dc…`, `f69cff6b…`).
- **Caveat on wiki anchors (I5, minor).** The `[HW:n]`/`[LW:n]` "tag-stripped `<article>` text, one line per block" form has no committed extractor. My independent strip of the same bytes puts "3 makes your system wait" at line 27 (route [HW:33]) and "On Arch Linux, by default" at line 76 (route [LW:84]). Re-anchoring at recheck time is therefore underdetermined. Correction: pin the extractor or switch to quote-only anchors.

## Smallest safe correction set (all text-only, no instrument widening)

1. Fix the S066 digest (`4f5c` → `6f5c`) in `SOURCES.md:78` and `lessons/round-17.md:53`, with an erratum.
2. Add `[UNK]` dispositions for §11 items 3, 4, 5 and 7. Fix the route:125 citation ("items 2, 5" → "item 2"). Make route:129 cite plane E2 and drop "adds".
3. Cite `~/.config/uwsm/env:5` and `[HC:289]` for the PATH and shell assumptions. Remove `grace` from route:98's defaults line. Add the HH:67-71 indeterminate-fallback clause to route:127.
4. Report C2 as "4/6, P4/P6 documentary-only".
