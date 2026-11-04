# R81ScribeLesson — findings (round 81, seat scribe)

Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`. Read-only throughout; no git/jj mutation; no
install. Base `c702094a`, freeze `0e2ccd2a`, tip seen at the end `f3eb70c7`. Deliverable:
`lesson-draft.md` (this directory) and the report `w1/R81ScribeLesson.md`.

Every command below is quoted with its exact argv; the lines that matter are literal output.

## 1. The shape I copied

```
$ sed -n '1,30p' /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-80.md
# mado round 80 — the composition under the band, and two matcher classes (2026-11-04, hyaku run 15)
…
## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
```

The r80 lesson's table is `id · class · evidence pointer · captured-by · fix (shown able to fail)`,
followed by a `## Gate (sources opened this round)` block with a census paragraph and a five-column
row table. The draft uses that shape; it also keeps r80's post-table sweeps.

## 2. Candidate (a) — the entity-escaping rule: **confirmed**

```
$ omarchy menu keybindings --print | cut -c36- | grep -c '&'
2
rc=0
$ omarchy menu keybindings --print | cut -c36- | grep -n '&'
17: → Pop window out (float & pin)
147: → omarchy-hw-external-monitors &amp;&amp; omarchy-hyprland-monitor-internal off
rc=0
$ omarchy menu keybindings --print | wc -l
193
```

Full receipt `amp-grep.txt`. The payload's escaping block is real and per action:

```
$ sed -n '150,166p' /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-80/fetch/S473.txt
155:        # Escape XML entities
156:        gsub(/&/, "\\&amp;", action);
157:        gsub(/</, "\\&lt;", action);
158:        gsub(/>/, "\\&gt;", action);
159:        gsub(/"/, "\\&quot;", action);
160:        gsub(/'"'"'/, "\\&apos;", action);
164:        printf "%-35s → %s\n", key_combo, action;
```

So the escaping is what the *code* does; the *printed* output still carries a bare `&` at line 17.
The frozen case pins both spellings as positive samples:

```
$ grep -n 'Pop window out\|Terminal &amp' /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-81/controls/make-c2-cases-r81.py
56:                    {"rc": 0, "out": block(bad=(0, " \u2192 Pop window out (float & pin)"))},
57:                    {"rc": 0, "out": block(bad=(0, " \u2192 Terminal &amp;&amp; log"))}],
```

and the generator's docstring states the rule (`controls/make-c2-cases-r81.py:9`: "The host payload
does **not** escape every ampersand (one action carries a bare `&`), so the grammar binds the
separator and the action's shape, never the entity text"). The narrowed matcher accepts both:

```
$ python3 matcher-probe.py
action bare-& : True
action &amp;   : True
```

The pre-fix case is **not** in any committed tree, and I did not find it in scratch either:

```
$ git -C /fast/scratch/hyaku/mado-r81/sandbox log --oneline -6
1dd44e95 r81 skill rows v2
457a9b9a r81 tool+skill sandbox
9dd96085 r81 tool sandbox
c702094a round-80 verifier spot-check (integrator, hyaku): non-author admit/reject
…
$ for c in 9dd96085 457a9b9a 1dd44e95; do git -C /fast/scratch/hyaku/mado-r81/sandbox ls-tree -r --name-only $c | grep -c 'quality/counters/c2-r81'; done
0
0
0
$ git -C /fast/scratch/hyaku/mado-r81/sandbox status --porcelain
(empty)
```

The sandbox commits each hold 127 older counter files from the lane clone, but no r81 counter. The
draft therefore marks the red state *reconstructed*, not observed — the same discipline r80 M80-1
demanded of a quoted receipt line.

## 3. Candidate (b) — `pgrep` `.strip()`: **confirmed**

```
$ grep -n 'stdout.strip()\|stdout.rstrip' /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r81-runbook.py
404:        text = stdout.strip()
411:        text = stdout.rstrip("\n")
```

Line 404 is the `is_active` branch (a state word, no padding in `systemctl` output); line 411 is
`pid_state`. The frozen negative and the probe:

```
$ grep -n ' 1720' /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-81/controls/c2-runbook-cases-r81.json
942:     "out": " 1720\n",

$ python3 matcher-probe.py
pid '1720\n'  : True
pid ' 1720\n' : False
pid '1720\n1721\n': True
pid '' rc1   : True
STRIP variant on negative ' 1720\n': True
frozen negative would then MATCH -> case incorrect: True
```

`special_matches` is the counter's own function, imported from the frozen file; the strip variant is
a four-line re-implementation in the probe. The negative is what kills the `pid-numeric-blind`
mutant: with `numeric = True` the padded line reaches `in_range`, which filters on `line.isdigit()`,
so the all() is vacuously true and the negative matches.

## 4. Candidate (c) — the r80 §11 attribution: **formula right, boundary wrong**

The r80 sentence and the tool it described:

```
$ sed -n '186,200p' /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/bar-footprint-composition-r80.md
1. **Centring past a negative tie (1 px).** `arranged_box` uses r79's integer formula
   `(bounds.size - size + 1) // 2`, which equals `CBox::round`'s result only when the tie's absolute
   coordinate is non-negative. A 1001-wide panel with both horizontal anchors on a 1000-wide monitor
   at the layout origin gives `-0.5` in the source (`round` → `-1`, width `1002`) and `0` in the
   tool. Needs `w > bounds.w` **and** a negative absolute tie; every frozen box fits its bounds.

$ git show dd4f844c:tools/mado-barfoot.py | sed -n '503p'
        x = bounds["x"] + (bounds["w"] - w + 1) // 2  # Hyprland centres in doubles, rounds once
$ git show dd4f844c:tools/mado-barfoot.py | sed -n '513p'
        y = bounds["y"] + (bounds["h"] - h + 1) // 2
```

The formula attribution is exactly right for the r80 tool, and `w` is never recomputed on that
branch (the only `w =` assignment is the `w == 0` allocation branch). The probe compares that
formula with a faithful `std::round` (half away from zero) over bounds 1..60 × width 1..70:

```
$ python3 tie-probe.py
disagreements: 1200
first 6: [(1, 2, -0.5, (0, 2), (-1, 3)), (1, 4, -1.5, (-1, 4), (-2, 5)), …]
negative ties that AGREE: 1170
first 4: [(1, 3, -1.0, (-1, 3), (-1, 3)), (1, 5, -2.0, (-2, 5), (-2, 5)), …]
counterexample bw=1000 w=1002: (-1, 1002) (-1, 1002) tie -1.0
brief case bw=1000 w=1001: (0, 1001) (-1, 1002) tie -0.5
all disagreements have tie<0 and fractional .5: True
probe_rc=0
```

So the r80 sentence's *only-when* is falsified by 1,170 negative-integer-tie agreements; the
divergence is exactly the negative **half-integer** tie (odd `bounds - size` with `size > bounds`).
The brief's 1001-wide instance reproduces exactly. This is a real (small) claim-boundary error in the
r80 entry; it does not move any frozen case, and the r81 declaration states only the instance.

## 5. A third mistake the brief did not name — the frozen C2 counter's docstring

```
$ grep -n 'cases=24\|PRED-C2-r79-v1\|round 79\|round-78\|twenty-two' /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r81-runbook.py
2:"""mado — PRED-C2-r79-v1: execute the runbook rows with per-row bindings and refusal shapes.
5:`### Executable runbook rows (round 79)` — the row's command cell must equal the case's
6:command, and each row is bound by exactly one case (the round-78 table bound three cases to
15:The seventeen round-78 cases are carried with their command, expectation, churn and negative
22:committed rows. The held round-78 rule — rc 0 and the output equal to one frozen value — is
24:construction (the printed `control_all` is an observation over all twenty-two cases, never a
27:Counting command (round 79):
30:      --carried .ufo/waves/round-78/controls/c2-runbook-cases-r78.json --scratch-root DIR
32:Contract: MADO_R81_RUNBOOK: cases=24 executed=24 matched=24 shapes=19/19 anchors=24/24
$ sed -n '51,54p' /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r81-runbook.py
CASES = 26
CARRIED = 24
SHAPES = 21
MUTANTS = 23
$ git show 0e2ccd2a:quality/counters/c2-r81-runbook.py | sha256sum
1bc9ca40a47aa05baa0ff59fc689595bdcecaa282d997ab3f9e38d340e01681f  -
$ grep -n 'MADO_R81_RUNBOOK:' /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-81/receipts/measurement-c2-r81.txt
52:MADO_R81_RUNBOOK: cases=26 executed=26 matched=26 shapes=21/21 anchors=26/26 rows=26/26 control_new=0/2 mutants=23 killed=23 verdict=TARGET_MET rev=0e2ccd2a8692825cac534f57246053b276be9f13 tree=bound
```

The frozen blob (sha256 `1bc9ca40…`, the file's own hash in the receipt's `MADO_R81_CONTROLS`-adjacent
declaration) carries the stale text; the code and the receipt disagree with its own contract line.
This is the M80-1/M80-3 class surviving into a frozen instrument. It is a documentation defect only:
`CASES`/`SHAPES`/`MUTANTS` are the values the predicate uses.

## 6. The landed lesson, and the one sentence this seat corrects

The L1 landed a round-81 lesson at `f3eb70c7` before this seat settled. I read it and checked its
checkable cells:

```
$ grep -n 'S224/S228/S231 ids collide' corpus/lessons/round-81.md
47:its S224/S228/S231 ids collide, and its 6354 B host-config claim is a 2026-10-23 read the r80

$ comm -12 lane.ids pkg.ids | wc -l
94
$ for id in S214 S219 S224 S228 S231: lane / pkg / collision
S214 lane=1 pkg=1 coll=1
S219 lane=1 pkg=1 coll=1
S224 lane=0 pkg=1 coll=0
S228 lane=0 pkg=1 coll=0
S231 lane=0 pkg=1 coll=0
```

`lane.ids` is `grep -oE '^\| *S[0-9]{3,}' corpus/SOURCES.md` piped through `sort -u` (414 ids);
`pkg.ids` the same over `SOURCES.append.md` (147 ids); `collisions` is the committed file under
`.ufo/waves/round-81/assimilation/`. The count 94 is right; the sentence's three ids are not among
them — the **parent** entry's `S214`/`S219` are. That becomes M81-5 in the draft, and the Gate's
assimilation paragraph states the corrected reason.

The landed lesson's other cells I could check hold: `grep -c 'if zone == -1'
tools/mado-barfoot.py` → `0` (with `if spec["exclusive"] == -1` at `:773`), and
`grep -rc 'preview_scale' .ufo/waves/round-80/fetch/S470.bin .ufo/waves/round-79/fetch/S464.bin`
→ `0` in both. Its M81-2 sentence "the sandbox run scored the negative as matching" has **no
artifact I can find**: the sandbox commits hold no r81 counter (above), the sandbox worktree is
clean, and `/fast/scratch/hyaku/mado-r81/l1/` holds only the seven C1 fixture dirs
(`overflow-tie`, `corner-edge`, `allfour-edge`, `parallel-edge`, `dyn-band`, `left-dock`,
`left-dock2`). If the L1 holds that log elsewhere it must be cited; otherwise the sentence is
`[INFERENCE]` like the reconstruction in this draft.

## 7. Gate

Census, both ends (full output `census.txt`):

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
… (standing W04 duplicates, W01 S277) …
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
census_rc=0
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
414
$ grep -nE '^\|[[:space:]]*S47[89][[:space:]]*\|' corpus/SOURCES.md
430:| S478 | hyprutils v0.14.0 — src/math/Box.cpp — https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.0/src/math/Box.cpp | code | A | … | `    double newW     = x + w - roundedX;` (at `:54`) | mined | 2026-11-04 | on-release | corpus/knowledge/bar-footprint-rounding-auto-r81.md |
431:| S479 | Hyprland v0.56.2 — CMakeLists.txt — https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/CMakeLists.txt | code | A | … | `set(HYPRUTILS_MINIMUM_VERSION 0.14.0)` (at `:150`) | mined | 2026-11-04 | on-release | corpus/knowledge/bar-footprint-rounding-auto-r81.md |
s47x_rc=0
```

Round start was 412 rows / exit 0 per the declaration and `receipts/census-start-r81.txt`; the
re-run at `f3eb70c7` is 414 / exit 0 because the L1 appended S478/S479 while this seat worked. Pins:

```
$ cd .ufo/waves/round-81/fetch && sha256sum -c sha256-r81.txt
S478.bin: OK
S479.bin: OK
verify_rc=0
$ grep -n 'w = std::round(newW);' S478.bin
59:    w = std::round(newW);
$ grep -n 'set(HYPRUTILS_MINIMUM_VERSION' S479.bin
150:set(HYPRUTILS_MINIMUM_VERSION 0.14.0)
```

Host cross-check, which fixes the rows' inference class (`host-check.txt`):

```
$ pacman -Q hyprutils
hyprutils 0.14.2-1
$ wc -c /home/vgpnk/.config/waybar/config.jsonc
6354 /home/vgpnk/.config/waybar/config.jsonc
$ sha256sum /home/vgpnk/.local/share/omarchy/default/waybar/indicators/idle.sh
6d8d2c11d3c3b15fa0aa31a830410c98d9e630a7683a9cedffb888d10f0f1750  …/idle.sh
$ grep -n 'pgrep -x hypridle' /home/vgpnk/.local/share/omarchy/default/waybar/indicators/idle.sh
3:if pgrep -x hypridle >/dev/null; then
$ python3 -c "…"   # module arrays
modules-left 2
modules-center 8
modules-right 8
```

Assimilation sample (full derivation `assimilation.txt`): admit on content
`knowledge/corpus/knowledge/host-bar-producers-r28.md` (the three checks above hold; landing gated by
its dangling parent and the 94-id renumber), reject
`knowledge/corpus/knowledge/host-bar-and-idle-binding-r26.md` §1 (`eight of the eleven visible
elements` vs its own 18-name enumeration and the host's 2 + 8 + 8; the r28 table supersedes it).

## 8. Findings

- **F1 (MEDIUM, corrected here).** The landed Gate's reject sample names the wrong colliding ids
  (`corpus/lessons/round-81.md:47`): S224/S228/S231 are free; the parent's S214/S219 collide. Fix =
  the M81-5 row + the corrected Gate paragraph in `lesson-draft.md`.
- **F2 (MEDIUM, live hazard).** The frozen C2 instrument is tree-bound to the *measured* revision:
  `quality/counters/c2-r81-runbook.py:651-655` raises Setup when the working tree's `SKILL.md` or
  `tools/mado-barfoot.py` differs from `--rev`'s blob. At `f3eb70c7` the tree's SKILL.md is
  `25b87bf0…` while `0e2ccd2a:SKILL.md` is `08213132…` (`tree-drift.txt`), so re-running the frozen
  command at `--rev 0e2ccd2a` now exits 2. Any re-measurement must name a rev whose SKILL.md bytes
  are in the tree (the landing tip), or carry the receipt's own caveat.
- **F3 (LOW).** The C2 counter's `--selftest` (88/88) has no unit check for either new kind:
  `grep -n 'special_matches("action_column"\|special_matches("pid_state"\|matches("action_column"\|matches("pid_state"' quality/counters/c2-r81-runbook.py` → no match (rc 1). The two matchers are
  exercised only by the frozen cases' samples/negatives and the seven new mutants — adequate, but
  not what the tally suggests.
- **F4 (INFO).** `receipts/measurement-c1-r81-at-tip.txt` was 0 bytes and untracked at my read
  (a seat writing it). Not my file; noted so the L1 does not cite an empty receipt.
- **F5 (LOW).** The landed lesson's M81-2 says "the sandbox run scored the negative as matching";
  no artifact under the sandbox or `/fast/scratch/hyaku/mado-r81/l1` supports it (see §6). Cite the
  log or mark it reconstructed.
- **F6 (INFO).** The instrument docstrings are inconsistent: the C1 counter's says `PRED-C1-r81-v1`
  with an r81 narrative; the C2 counter's still says `PRED-C2-r79-v1` and the r80 contract numbers
  (M81-3). The C2 receipt and constants are correct; only the prose is stale.

## 9. Out of scope / not done

- No instrument, control set, declaration, SKILL.md or LOG.md edit (report-only seat).
- I did not re-run either counting command end to end: the C2 one is blocked by F2's tree binding,
  the C1 one is an executor's duty and its receipt is committed. The receipts I quote are the
  committed ones.
- No install or upgrade was needed (tooling authorization unused).

## 10. Receipts in this directory

`amp-grep.txt`, `census.txt`, `counter-docstring.txt`, `source-pins.txt`, `tree-drift.txt`,
`assimilation.txt`, `host-check.txt`, `r80-boundary.txt`, `matcher-probe.py` + `matcher-probe.out`,
`tie-probe.py` + `tie-probe.out`, `lesson-draft.md`.

Scratch `/fast/scratch/hyaku/mado-r81/R81ScribeLesson` was removed after the probes were copied here.

STATUS: ok
