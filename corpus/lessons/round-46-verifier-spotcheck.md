author: hyaku closure (non-author integrator, @m_opus)

# mado round 46 — non-author closure spot-check (attempt 1)

Lane HEAD before `b22ea56bff2faec39ce9ff75d2107eaf4612ecbe`, after `edc147898e9de3c4e40f003277f20dbf67f18956`.
Driver digest (`.ufo/watchdog.log`, mutable — copied here):
`2026-10-26T17:03:35-03:00 launch mado round=46 pgid=2085458 driver=hyaku-inline attempt=1` /
`2026-10-26T18:28:19-03:00 complete mado round=46; hyaku-inline attempt=1` (one launch, one completion).
I did not author the round. Re-checks ran on committed bytes (`git show`/`git ls-tree`/`git grep` at the cited revisions), on upstream
raw files re-fetched 2026-10-26, and read-only on the host (`hyprctl devices -j` captured into a `/tmp` scratch file, configs copied
there; nothing in `~/.config` written). The deliverable `tools/mado-devices.py` ran from committed bytes
(`git show edc1478:tools/mado-devices.py`, sha256 `3a80368997120503…`, equal to the tool hash in `receipts/live-devices-host-r46.txt:1`).
The two claim counters (`quality/counters/c1-r46-devices-v3.py`, `c2-r46-input-device-entry-v2.py`) have no row in the `SKILL.md`
`## Gate registry` (rows end at `mado-axis-scores` `:769` and `mado-session-material` `:770`), so I ran them as measurements, as the
round-45 closure did. I did not execute the registered gates `mado-axis-scores` or `mado-session-material`; their committed evidence is
verified instead. `git status --porcelain` in the lane was unchanged by my runs (one pre-existing untracked file, below).

## 1. Step-1 conformance

| check | command | observed |
|---|---|---|
| report committed by lane identity | `git log --format='%an <%ae> %H %cI' -- .ufo/reports/round-46/mado.md` (fleet repo) | `mado-shokunin <mado@shokunin.local> b25732fc0747ac6efcdb96015eb0ff2db759eccc 2026-10-26T18:27:52-03:00` |
| report lands after the lane commit | commit times | lane tip `edc1478` 18:26:38, report 18:27:52, driver `complete` 18:28:19 → commit-then-report holds |
| prompt committed, template contract | `git log -- .ufo/prompts/mado-round-46.md`; `diff <(sed -n 1,140p prompt) templates/round-prompt.md` | `mado-shokunin 1a7a6925` 17:03:34 (before launch 17:03:35); the diff shows only `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/`{{AXES}}` substitutions (lines 1, 5-6, 46, 61, 65, 69, 101, 133, 135, 139); §6 hyaku addendum and §7 scratch discipline follow; axes string equals `shokunin.conf:56` (`coverage + operability (desktop and compositor craft)`) |
| SHONEN heading | report `## SHONEN` | present, 4 lines, all `[~]` with pointers |
| cited commits exist + ancestors of `master` | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> refs/heads/master` for b22ea56, 8c5434c6, e0be61e4, 2bcc335f, 7f793280, fb6a1fee, 1001bda0, 9879964f, edc14789 | all 9 `commit`, all ancestors; the 8 round commits are authored by `mado-shokunin` |
| pushed | `scripts/hyaku/jj-lane.sh state …`; `git ls-remote origin refs/heads/master` | `branch=master local=remote=edc14789… ahead=0 behind=0 head=detached tracked=0 untracked=1`; remote `edc14789…` |
| leftovers | `git status --porcelain` | `?? .ufo/waves/round-46/w1/ExecStofOracle/receipts/out.json.rows.tsv` (3.3 MB; disclosed in the report; the seat `report.md` and `out.json` summary are committed) → R2 |
| L2 floor / round size | `jq '{seats, n:(.results\|length), nulls}' .ufo/waves/round-46/w1-results.json`; `git ls-tree --name-only edc1478 .ufo/waves/round-46/w1/ \| grep -c '\.md$'` | `seats=66 n=66 nulls=0`; 66 seat reports — inside the 64-128 band; the round-45 D5 `output: null` gap did not recur |
| real report, not a marker | `git diff --numstat b22ea56 edc1478` | outside `.ufo/`: 17 files +11560/−0; whole round 0 deletions → status `ok` |
| freeze integrity | `git diff --stat 7f793280 edc1478 -- quality/counters/c1-r46-devices-v3.py quality/counters/c1-r46-fixtures-v2.json quality/counters/c2-r46-input-device-entry-v2.py .ufo/waves/round-46/registration-v2.md .ufo/waves/round-46/registration-v3.md` | empty; `git log` shows each counter added only in its freeze commit (v3 `7f793280`, v2 counters/fixtures `2bcc335f`); tool and entry first appear in the data commit `1001bda0` and are not touched after |
| round-45 routed items | lesson `## Round-45 closure items` | D1 run (11 w1 seats on the round-45 data); D2 corrected in M46-10; D3 registry row present (`SKILL.md:770`), marker not installed; D4 digest committed; D5 noted; D6 open (third deferral) → R4 |

## 2. Per-claim re-check

| claim | plain measurement (base → tip) | observed | reported | ruling |
|---|---|---|---|---|
| C1 operability (capability) — `tools/mado-devices.py` | `git cat-file -e <rev>:tools/mado-devices.py`; `git show edc1478:tools/mado-devices.py \| wc -l \| sha256sum` | base absent → tip present, 641 lines, sha256 `3a803689…` = live receipt | same | **verified** |
| C1 counter (re-measured, fresh nonce) | `python3 -I quality/counters/c1-r46-devices-v3.py --repo . --rev <rev> --work /tmp/mado-r46-close.Tiu1/<rev>` | base `fixtures=0/110 generated=0/150 selftest=fail readonly=fail tool=absent verdict=TARGET_MISSED` (seeds 46,1529015958); tip `edc1478` `fixtures=110/110 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET` (seeds 46,1593941714), `clause=r trips=0` | base/`1001bda`/`9879964` receipts identical in shape | **verified** |
| C1 fixtures | `git show edc1478:quality/counters/c1-r46-fixtures-v2.json \| jq length` | 110 | 110 | **verified** |
| C1 controls (evidence-verified) | `receipts/ctl-c1-v3.txt` (commit `fb6a1fee`) | 42 `CTL_C1v3` lines; `VERDICT: PASS (controls scoring TARGET_MET: 0 of 40; reference met: 1)`, exit 0; the v2 FAIL (`2 of 40`) is committed beside it (`ctl-c1-v2.txt`) and drove the v3 re-freeze before data | same | **verified** |
| C1 live (SHONEN box 2) | `python3 -I md.py --devices dev.json --config om.conf --config user.conf` (copies of the two host configs; dump captured 2026-10-26) | `keyboards=9 agree=9 … virtual=0 mice=4 mice_differ=0 … verdict=OK`; the receipt's 10th keyboard (`hl-virtual-keyboard-fcitx5`, VIRTUAL) is absent from today's dump, as `SKILL.md` warns (the VK exists only while the input method holds it) | `keyboards=10 agree=9 virtual=1 … OK` | **verified** (host state differs only by the VK) |
| C1 independent of the tool | `hyprctl devices -j \| jq '{kb, mice, layouts, opts, sf}'`; `grep -n kb_layout\|kb_options\|scroll_factor` on both configs | 9 keyboards, 4 mice, layouts `["br"]`, options `["compose:caps"]`, scrollFactor `[-1.00]`; user conf sets `kb_layout = br` over omarchy's `us`; the only `scroll_factor = 0.4` sits inside `touchpad { }` (`input.conf:34`) | AGREE ×9, mice −1.00 | **agree** |
| C1 can fail | same run with `kb_layout = br`→`de` in a scratch copy; then a `device { name = Razer DeathAdder V2 … }` block appended | `agree=0 differ=9 verdict=DIFFER` exit 1; `MADO_DEV_BLOCK: name="Razer DeathAdder V2" … verdict=NO_SUCH_DEVICE`, `verdict=STALE_BLOCK` exit 4 (the exit map at `SKILL.md:2112-2113`) | — | **verified** |
| C1 read-only | `grep -nE '^(import\|from) \|subprocess\|socket\|os\.system\|Popen\|open\('` on the tip tool | imports json, math, fractions, os, re, stat, struct, sys; one `os.open(path, O_RDONLY\|O_NONBLOCK)` at `:139`; `socket`/`subprocess` only in the docstring at `:30` | "starts no process, opens no socket" | **verified** |
| C1 selftest | `python3 -I md.py --selftest` (committed bytes) | `MADO_DEVICES_SELFTEST: 59/59 passed` | 59/59 | **verified** |
| C2 coverage (sourced) — `corpus/knowledge/hyprland-input-devices-r46.md` | `git cat-file -e`; `git ls-tree --name-only <rev> corpus/knowledge/ \| grep -c '\.md$'`; `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | entry absent → present; knowledge 62 → 63; rows 252 → 262; `git diff b22ea56 edc1478 -- corpus/SOURCES.md` removes 0 lines; S316-S325 all 13-field, kind code×9/docs×1, tier A, `mined`, opened 2026-10-26, used-by the entry | same | **verified** |
| C2 ground absent at base | `git grep -n -E 'applyConfigToKeyboard\|getDeviceString\|deviceConfigExists\|getConfigValueSafeDevice\|scrollFactor\|m_keymapOverridden' <rev> -- corpus SKILL.md` | base exit 1 (no hit); tip hits in SKILL.md, README, SOURCES, the entry, the lesson | `receipts/c2-ground-base.txt` exit 1 | **verified** |
| C2 counter (re-measured) | `python3 -I quality/counters/c2-r46-input-device-entry-v2.py --repo . --rev <rev>` | base `clauses a-k all 0 admitted=0/1 TARGET_MISSED`; tip `edc1478` `clauses a-k all 1 admitted=1/1 TARGET_MET` | same | **verified** |
| C2 controls (evidence-verified) | `receipts/ctl-c2-v2.txt` (commit `7f793280`) | `CTL_C2v2 VERDICT: PASS (wrong=0 of 22; positive admitted=1)`, exit 0 | same | **verified** |
| C2 entry head and pins | `git show edc1478:<entry> \| head -16`; upstream re-fetch of HyprCtl.cpp `:763-773`, IKeyboard.cpp `:108-115`, MiscFunctions.cpp `:777-789` | provenance block first: 10 `source: S316…S325` lines, `verified-at: 2026-10-26`, `recheck: on-release …`, `ground:`; each re-read range carries the stated mechanism (`m_scrollFactor.value_or(-1)` with `{:.2f}`; `layout = "us"` after a failed compile; space/newline/comma → `-` plus `tolower`) | — | **agree** |
| C2 entry live sentence | `grep -n live-devices-host corpus/knowledge/hyprland-input-devices-r46.md`; `head -4 receipts/live-devices-host-l1.txt` | `:57` cites `receipts/live-devices-host-l1.txt`, produced by `l1-draft/mado-devices.py` (sha256 `b229efd0…`) over one config, not the landed tool (`3a803689…`, two configs, `live-devices-host-r46.txt`); both receipts print the same summary line, so the sentence's content holds | — | **defect R1** (citation layer, QUALITY 24; same class as M46-5) |

Evidence-verified only (registered gates, not executed): `receipts/axis-base.txt` `MADO_AXIS: checked=3 mismatched=0 rev=b22ea56…`
(navigation 62/62, calibration 73/73, operability 12/12); `receipts/axis-tip.txt` `checked=3 mismatched=0 rev=9879964…` (63/63, 77/77,
12/12); `receipts/axis-data.txt` `mismatched=2` at `1001bda` — the declared two-phase window (publication follows in `9879964`).
`9879964..edc1478` adds only receipts. `quality/check-session-material.py` exits 1 at the data commit (`receipts/session-material-data.txt`:
`files=18363 findings=115`; 18 in round-46 seat files, the lane's synthetic count) — red, reported by the lane → R3.

Harm watch: `git diff b22ea56 edc1478 -- SCORECARD.md` is a pure append (+29: Round 46 section, claim table, capability row, sources,
axis line, planned). The whole round deletes 0 lines. Axis inputs re-derived plainly: knowledge 62 → 63 (navigation 62/62 → 63/63);
QUALITY gains 87-90 (+4 = calibration 73 → 77). No axis harmed.

## 3. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| operability | improved | C1 re-measured: tool absent → present; counter v3 110/110 + 150/150 MET at the tip under my own nonce; live OK, a DIFFER exit 1 and a STALE_BLOCK exit 4 reproduced on scratch configs; selftest 59/59 |
| coverage | improved | C2 re-measured: entry 0 → 1, knowledge 62 → 63, rows 252 → 262, ground grep exit 1 at base, counter 1/1 MET at the tip, sampled pins byte-equal to upstream |
| depth | unchanged | SKILL gains one tool section with a verdict/exit table; not a declared claim and no held table re-graded |
| freshness | unchanged | new pins opened 2026-10-26 with an on-release recheck naming the Lua-era break; no held claim re-verified as stale and fixed in place |
| calibration | unchanged | v1 → v2 → v3 re-registration before data with controls 0 of 40 / 0 of 22; axis fraction stays 1.0 (73/73 → 77/77); R1 shows criterion 24 missed on the lane's own new entry |
| adjacency | unchanged | PROVINCE refinement only; `w1/ConnSiblings.md` for sibling overlap; nothing absorbed |

## 4. Discernment spot-check (`corpus/lessons/round-46.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `GATE S317` / row S317 | admit (tier A, `code`) | `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp` re-fetched: sha256 `9db68cf4…` = gate line; quote verbatim at `:1119` | **agree** | The set-by-user test with a non-empty fallback is the exact device-first-then-global rule the entry's step 3 states; primary code at the host's revision. |
| `GATE S321` / row S321 | admit (tier A, `code`) | `…/efb50993…/src/helpers/MiscFunctions.cpp` re-fetched: sha256 `06541824…` = gate line; `case ',': return '-';` at `:782` inside `deviceNameToInternalString` (`:777-789`, also `tolower`) | **agree** | The normalizer is the only source of the dump's device names; the scope (name normalization) is narrow and the quote grounds it. |
| `GATE S325` / row S325 | admit (tier A, `docs`) | `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/ecc06f3b6605e453c0ad533d979fccbefff788ef/content/Configuring/Keywords.md` re-fetched: sha256 `11c0842c…` = row and gate line; quote at `:67-68` | **agree** | Docs restate the code rule (S317); tier A is right for "what the maintainers document" and the row scopes it to the hyprlang era. |
| REJECT hyprland-wiki `content/Configuring/Keywords.md` at main | reject | same path on `main` → HTTP 404; `content/configuring/core/devices.md` at main documents `hl.device({ name = …, sensitivity = … })` (Lua) | **agree** | The page no longer exists at main and the replacement describes a config plane this host does not run; the pin at `ecc06f3` is the right authority. |
| REJECT Hyprland `src/devices/Keyboard.cpp` | reject | `…/efb50993…/src/devices/Keyboard.cpp` re-fetched: 56 lines, `grep -cE 'getDeviceString\|setKeymap\|kb_layout\|keymap'` → 0; `updateXkbStateWithKey` at `:41` | **agree** | Event wiring only, no config read or keymap compile; it cannot move any step of the chain. |

SOURCES row re-opened for its quote: S325 — `It's worth noting that ONLY values explicitly changed will be overwritten.` (11 words, ≤25) present at
`Keywords.md:67` of the pinned revision; the row's anchor (`:64-94`, override sentence `:66-68`) and sha256 match the re-fetch.
Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → W04 ×7 (S030, S042,
S045, S097, S119, S120, S121) + W01 S277 + W04 S303, S307, S317, S318, S320, S321, S324 (held URLs under new scopes), `mado ok`, exit 0 —
the five new W04 lines the report names, identical to `receipts/census-after.txt`.

## 5. Trend verdicts

- **expansion: improved** — one capability shown running (my live run plus DIFFER and STALE_BLOCK probes), one knowledge entry on ground
  absent at base (ground grep exit 1; knowledge 62 → 63), rows 252 → 262, all re-fetched pins byte-equal to upstream today.
- **quality: unprovable-but-better** — as the named non-author reviewer: the round-45 data finally got its falsification wave (11 seats;
  `w1/CritW2Entry.md`: 72/78 sentence units supported, 71/71 quotes found), both round-46 instruments were broken by w1 and re-frozen
  before data, and the C1 v2 counter was caught by its own controls. But the round-45 entry's six non-supported units are recorded in the
  lesson, not corrected, and the new entry repeats the M46-5 provenance slip (R1): no held entry was superseded and one re-check partly
  failed — better, not countably improved. Not `harmed`: every finding is marked in a committed lesson and the sentences' content holds.
- **discernment: improved** — 5/5 sampled gate decisions (three admits, two rejects) agree on outside re-reading; the lane withdrew its
  own v1 and v2 predicates on evidence. Limit: the lane's QUALITY 24 did not catch R1 in its own new entry.

Closure: status `ok`, **admitted=true**, verdict `admitted` — both claims verify, no axis harmed.

## 6. Routed defects (lane fixes next round)

1. R1 — `corpus/knowledge/hyprland-input-devices-r46.md:57` attributes the live join to `receipts/live-devices-host-l1.txt`, whose
   producer is `l1-draft/mado-devices.py` (sha256 `b229efd0…`, one config), not the landed tool (`3a803689…`, two configs,
   `receipts/live-devices-host-r46.txt`); the sentence also says "one `input` block in `~/.config/hypr/input.conf`" while the landed run
   passes the omarchy default first. Append an erratum citing the r46 receipt — the exact M46-5 class the round itself mined.
2. R2 — untracked `.ufo/waves/round-46/w1/ExecStofOracle/receipts/out.json.rows.tsv` (3.3 MB) sits in the lane worktree (repeat of
   round-45 D4): commit a digest line beside the seat's `out.json` and remove the file, or state its retention.
3. R3 — `mado-session-material` is red at the data commit (`findings=115`, exit 1; 18 in round-46 seat files): install the drafted
   synthetic-fixture marker (`w1/ExecSessionTriage/`) and the prose serial rule (`w1/ExecSerialRule/`), shown able to fail both ways
   (SCORECARD Round 46 planned 2).
4. R4 — carried open: S290-S297 supersession (round-44 D6, M46-16; third deferral), round-44 `w2/ConnCalibration` errata, and the
   round-45 entry's six sentence units (`w1/CritW2Entry.md` F1 mis-located `:84b`, F2 provenance `:96`, F3 wrong `:98`, F4 unpinned
   `:18b`/`:106`/`:107`) — land each as an appended erratum (SCORECARD Round 46 planned 1 and 3).

SHONEN boxes remain `[~]`. Box 2 (end-to-end live run) is reproducible by a non-author — I reproduced `agree=9 … verdict=OK` and the
DIFFER/STALE_BLOCK exits from committed bytes — and box 3 held for me: the `SKILL.md:2107-2117` command ran as written with no oral
context. Promotion review is operator-owned. Operator note (carried from the report, M46-10): the host monitor serial sits in three held
entries and 21 round-32/37 wave files; removal from pushed history is the operator's decision.
