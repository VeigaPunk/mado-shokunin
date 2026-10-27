# R54W2Seat27 — w2 falsification, item 27: "Toggle committed evidence"

- Seat: R54W2Seat27 (w2, round 54, lane mado-shokunin). Base `e25149fec8152a3aabd2b18a0ee8663b23cf65aa`; HEAD at measurement time `350d30e4ec5531f65ce99a57efeb8216f38e678a` (frozen freeze commit; no wave has committed since).
- Item 27: *Toggle committed evidence. Check committed pin coverage for `omarchy-toggle-idle:9`; distinguish L1 pre-freeze read from revision-bound bytes. Cite frozen contract lines, exact pin spans and relevant w1 report.*
- All git invocations below are read-only object reads against the lane repo. No lane/fleet/sibling/source edits, no git/jj mutation, no host reads, no installs (RULES.md read in w1; nothing installed this wave).
- Scratch `/fast/scratch/hyaku/mado-r54/R54W2Seat27` created (`mkdir -p`, `df`: 580G free, no ENOSPC) and removed before yield; no fixture was needed — every check is a committed-object read.

## Verdict (one line per question)

| question | verdict |
|---|---|
| committed pin coverage for `omarchy-toggle-idle:9` in round 54 | **ABSENT** — the committed round-54 evidence set contains no bytes and no hash for the file; only prose |
| is the frozen predicate damaged by that absence? | **No** — clause (c) is a citation-count leg over the entry text; the counter's frozen input set contains no host bytes, so PRED-C2-r54 is structurally satisfiable with `:9` byte-unbacked in-lane |
| pinned command re-run | **NOT RUN/absent** — `quality/counters/c2-r54-uwsm-entry.py` does not exist at HEAD or in the working tree |
| L1 pre-freeze read vs revision-bound bytes | the `:9` content assertion (`uwsm-app -- hypridle`) originates from the L1's live host read recorded as prose in `fetch/README.txt:18`; the only *revision-bound* artifacts are a round-17 full digest **without preimage** plus round-32/35 prose — a digest cannot authenticate a line number |

## 1. Frozen contract lines cited

- `claims-frozen.md:57-59` — the C2 claim surface includes "the idle re-arm through `uwsm-app`".
- `claims-frozen.md:62-65` — predicate clause (c): "the entry carries at least two host **join citations** among the frozen host set of `registration.md`" (citation leg, not a byte leg).
- `claims-frozen.md:66-68` — before-state: at base the entry is absent and the predicate is TARGET_MISSED by absence.
- `claims-frozen.md:81-84` — causal separability: "C2 reads only … `corpus/knowledge/uwsm-app-environment-r54.md`, `corpus/README.md` (its row), rows S375–S377 of `corpus/SOURCES.md` and `.ufo/waves/round-54/fetch/`." **No host file is a counter input.**
- `registration.md:4-6` — the freeze was made "after opening every C2 source itself" by the L1 (the three uwsm URLs, per `fetch/README.txt`).
- `registration.md:71-76` — entry requirement; frozen host set ends at line 76: `` `~/.local/share/omarchy/bin/omarchy-toggle-idle:9`. ``
- `registration.md:80` — C2-CTL-6 mutates the **entry text** ("entry text carries none of the frozen host set"); no control ever pins host bytes.

## 2. Committed round-54 pin coverage: absent

```
$ git -C <lane> ls-tree --name-only HEAD .ufo/waves/round-54/fetch/
.ufo/waves/round-54/fetch/README.txt
.ufo/waves/round-54/fetch/SHA256SUMS.txt
.ufo/waves/round-54/fetch/uwsm-0.27.1-README.md
.ufo/waves/round-54/fetch/uwsm-0.27.1-main.py
.ufo/waves/round-54/fetch/uwsm-0.27.1-uwsm-app.1.scd
```
`SHA256SUMS.txt` has exactly 3 lines (`1874fb83…` README, `7dd63632…` main.py, `3982503d…` uwsm-app.1.scd) — **no omarchy file**. The three pins contain 0 occurrences of `hypridle` and 0 of `toggle` (`grep -c` on each → `0`), so the uwsm pins cannot cover the host join either. The only round-54 statement of `:9`'s content is prose in the L1 manifest, `fetch/README.txt:18`:

> `~/.local/share/omarchy/bin/omarchy-toggle-idle:9` (`uwsm-app -- hypridle`). See `../registration.md` C2 fixture inventory.

## 3. Whole-history preimage search: no committed bytes anywhere

```
$ git ls-tree -r --name-only HEAD | grep -in toggle     # 23 paths, identical list at base e25149fe
… all 23 are toggles/*.conf fixture/state files (rounds 39/45/47/48), none is omarchy-toggle-idle
$ git ls-tree -r --name-only HEAD | grep -E 'bin[_-]?omarchy-toggle|bin/omarchy-toggle'
(no output, exit=1)
$ git log --all --oneline -- '*toggle*' | head
097046ac / 89a1c168 / dd2e827e (round-49) / 3e6c848a (round-48) / a7fe2b11 /
9bddd6ac (round-47) / d17dc0b3 / 7c0b0035 (round-45) / aa276406 / 50ffe8a1   — toggles fixtures only
$ git log --all -S 'omarchy-toggle-idle' --oneline | head -20
350d30e4 (this freeze: registration.md + fetch/README.txt prose), 7769a160, 826b2037, ce4c4b96,
fa672cbe, 097046ac, dd2e827e, 0d49768c, d40189c9, 7f793280, dbc8176c, 8ac15c41, ccdce5f7,
58466627, 72847ef6, 6876bba1, 91f0a2b8, 50ffe8a1, b6078c3e, e5206ca6                       — prose introductions
```
`git grep 'toggle-idle' HEAD --` hits (30 shown of ~50, all identical classes at base): round-16/17 reports (prose), round-18 fetch — `bin_omarchy-menu:212` (caller line), `default_hypr_bindings_utilities.conf:30` (keybind caller), `tree.json:2424` ×3 (upstream *path listing* only), round-32 knowledge and its control/fixture copies (prose + truncated hash), round-35 reports (prose). Round-18's fetched omarchy tree contains `bin_omarchy`, `bin_omarchy-system-lock`, `bin_omarchy-launch-walker`, `bin_omarchy-menu` — **no `bin_omarchy-toggle-idle`**; upstream existence is proven by `tree.json` metadata, the bytes were never fetched.

## 4. What revision-bound evidence does exist (earlier rounds)

| committed artifact | what it binds |
|---|---|
| `.ufo/waves/round-17/w1/reports/HostIdleFiles.md:118-119` (committed; `git grep -l '11979b4d4198526445'` → this file and RevReadmeFrontier.md only) | full sha256 `11979b4d4198526445ee124a66ce1d2b5607b9f62ad01a516f22bba66256b284` (13 L), under the header "existence + digest only (**bodies not read this pass**)" |
| `.ufo/waves/round-35/w2/reports/RevReadmeFrontier.md` | same full digest (prose) |
| `.ufo/waves/round-32/assimilation/validate/corpus/knowledge/idle-lock-plane.md:95,:266` | truncated digest `11979b4d4198`, 316 B / 13 L; "`omarchy-toggle-idle:5-11` toggles by `pgrep`/`pkill -x hypridle` vs `uwsm-app -- hypridle`" (line-content prose) |
| round-32 `waybar-walker-semantics.md:139`, `waybar-walker-plane.md:97`, `config-health-report-r3.md:203` | `:13` = `pkill -RTMIN+9 waybar` (prose) |
| `.ufo/waves/round-35/w2/reports/SentProvenance.md:279` | "`omarchy-toggle-idle:9` runs `uwsm-app -- hypridle`" (prose) |
| `.ufo/waves/round-54/fetch/README.txt:18` | the L1 pre-freeze live-host read, `:9` (`uwsm-app -- hypridle`) — **prose in the manifest, unpinned** |

**The hash has no committed preimage.** Nothing in the lane can recompute `11979b4d…`, so nothing can distinguish `:9` from any other line of the 13-line script; the `:9` assignment rests on prose consensus (round-35) plus the L1's unreproducible freeze-time read.

## 5. L1 pre-freeze read vs revision-bound bytes

- **L1 pre-freeze read**: `registration.md:4-6` + `fetch/README.txt:16-19` — the L1 opened the three uwsm sources *and* read the host join points live on 2026-10-27, recording `:9` content as text. This observation is revision-bound **only as a sentence**: it has no pin file, no hash row, and is not re-derivable by any wave seat (host reads are forbidden by the lane bounds). A future host-side drift of that file is undetectable from the revision.
- **Revision-bound bytes**: none for `omarchy-toggle-idle` at any revision (§3). The round-54 revision binds exactly three upstream uwsm files; every byte-backed claim about the toggle script stops at round-17's digest.
- Contrast with the sibling joins (measured in w1, still true): `default/hypr/autostart.conf` lines are backed by **seven committed copies** sharing sha256 `acb6a66862033edd26ad98e453cc8d894388c6a2e374b491bc4061d55f7a0441` (rounds 18/39), and `~/.config/hypr/bindings.conf:2` by round-39 host-tree copies with sha256 `e574a1ed08535e31deeafe2a26432c6862bb101e8c45d5a6b3f997d7dc810581`. The toggle join is the **only** member of the frozen host set (`registration.md:74-76`) with zero committed bytes — it is the weakest of the eight, while the seven-line autostart set carries its own contradiction (frozen `:6` is the polkit agent, monitor-watch is at `:9` in all seven copies; w1 R54Seat27 F7, R54Seat07 F5).

## 6. Exact pin spans (the three real round-54 pins)

| row | frozen locator | measured span in pin (this wave, `grep -n`) |
|---|---|---|
| S375 | `uwsm-0.27.1-README.md:117-118` | quote starts `:117` (`- Difference between environment state before and after preparation is exported`) and completes `:119` (`implementation is used)`) — frozen locator is off by one line (w1 F2 confirmed) |
| S376 | `uwsm-0.27.1-uwsm-app.1.scd:60` | `:60` = `*uwsm-app* client sends arguments to uwsm's app daemon via a pipe. Upon` — frozen quote present only after stripping scdoc `*…*` emphasis (w1 F1 confirmed) |
| S377 | `uwsm-0.27.1-main.py:3714` | `:3714` = `unit_name = f"app-{desktop_unit_substring}-{cmd_unit_substring}-{random_hex(8)}.{app_unit_type}"` verbatim; near-collision `:3716` is the `@`-variant, so a 2-line locator drift lands on a different true line |
| `omarchy-toggle-idle:9` | `registration.md:76` | **no pin exists; no span is checkable in-lane** (§3-§4) |

## 7. Predicate impact (coverage finding, not a contract edit)

1. Clause (c) (`claims-frozen.md:63-65`) counts **citations in the entry text**; C2-CTL-6 (`registration.md:80`) only removes those strings from the entry. No frozen leg or control requires host bytes, so a TARGET_MET is reachable while the `:9` join is byte-unbacked.
2. The counter is defined (separability, `claims-frozen.md:82-84`) to read only entry/README/SOURCES/fetch-pins — it **structurally cannot** verify `omarchy-toggle-idle:9`. By design the host-set leg is a paperwork-consistency leg, not an evidence leg.
3. Falsification value: if the landed entry spends one of its two required joins on `omarchy-toggle-idle:9`, half of clause (c)'s minimum rests on an unpinned freeze-time read + a digest whose preimage the lane never held. The two alternatives that are byte-backed (`autostart.conf:1`/`:2`, `bindings.conf:2`) suffice for clause (c) without the toggle join — an entry author has no need to touch the unverifiable join, and the frozen contract does not force one. This is a coverage/evidence-quality finding on the claim, to be weighed as-is; the frozen files are not editable post-dispatch and nothing here proposes an edit.
4. If the round later wants `:9` to be more than prose, the pre-data path is a pin (bytes + sha256) under a NEW versioned registration — not a predicate edit (freeze rule, `claims-frozen.md:5-8`).

## 8. Pinned command: NOT RUN/absent

```
$ git -C <lane> ls-tree --name-only HEAD quality/counters | grep -c r54
0
$ ls <lane>/quality/counters | grep -c r54
0
```
`quality/counters/c2-r54-uwsm-entry.py` (and the C1 twin) does not exist at HEAD or in the working tree — the newest committed counter is `c2-r51-dispatch-entry.py`. The frozen predicate command therefore cannot be re-run this wave: **NOT RUN/absent**, and per the frozen before-state (`claims-frozen.md:66-68`) the predicate remains TARGET_MISSED by absence.

## 9. Lane-state observations (read-only, recorded not judged)

- Working tree at w2 time: `M corpus/SOURCES.md` (+5 lines) plus untracked wave dirs/lesson. The staged diff adds S375 and S377 marked **`rejected`** (out-of-province screen) and S376 queued as insufficient; its stop note says the reviewer "opened … the static host files named by registration" and that "registration's host-anchor summary also conflicts with the opened autostart file" — no row or pin was added for `omarchy-toggle-idle` (`git diff corpus/SOURCES.md | grep -in toggle` → no hits, exit 1).
- The w1 draft entry `corpus/knowledge/uwsm-app-environment-r54.md` is no longer present (`ls corpus/knowledge | grep r54` → exit 1); no r54 file is committed under `corpus/knowledge` either.
- `git status --porcelain` count: 11 entries; HEAD unchanged at `350d30e4` since before w1 evidence.

## 10. Relevant w1 reports

- **R54Seat27.md** (my w1 report) — §4 F7: seven committed autostart copies (`acb6a668…`), frozen `:6` wrong, monitor-watch at `:9`; `git ls-files | grep -i toggle-idle` empty → "the frozen `omarchy-toggle-idle:9` join has no committed bytes in the lane"; §4b records R54Seat07's independent confirmation.
- **R54Seat07.md** — §3.3 "`omarchy-toggle-idle:9` — prose only, no bytes" (lines 169-178: no SOURCES row, no hash row named there, only `SentProvenance.md:279` and `config-health-report-r3.md:203` prose; "A counter cannot distinguish `:9` from any other line"); findings table F6 (Medium) and F7 (bindings byte-backed, `e574a1ed…`).
- This wave adds to both: the **full** digest *does* exist committed (round-17 `HostIdleFiles.md:119`, plus round-35 `RevReadmeFrontier.md`), so the precise gap is *preimage* absence, not hash absence — and round-18's `tree.json:2424` proves upstream existence without bytes.

## 11. Commands and outputs (summary; full outputs inline above)

`git rev-parse HEAD`; `git log --oneline -8`; `git status --porcelain`; `git ls-tree` (HEAD, base; fetch/, round-54/, w1/, quality/counters); `git grep` for `toggle-idle` / `uwsm-app -- hypridle` / `11979b4d4198…` at HEAD and base; `git log --all -- '*toggle*'`; `git log --all -S 'omarchy-toggle-idle'`; `git diff corpus/SOURCES.md`; `grep -c 'hypridle|toggle'` over the three pins; `grep -n` for the three quote spans; `df -h /fast/scratch`. Every exit code is shown inline; none failed except the intentional absent-pattern greps (exit 1, shown).

## Housekeeping

- Scratch `/fast/scratch/hyaku/mado-r54/R54W2Seat27`: created empty, **removed** before yield (`rmdir` → success). No fixture, no writes, no ENOSPC.
- Observed leftover (not mine to touch, reported per bounds): w1 scratch `/fast/scratch/hyaku/mado-r54/R54Seat27` still exists — belongs to the wave-1 seat identity, left as found.
- No tool installed or updated; no git/jj mutation; no lane, sibling, fleet or host file touched besides this named report.

Report: .ufo/waves/round-54/w2/R54W2Seat27.md
