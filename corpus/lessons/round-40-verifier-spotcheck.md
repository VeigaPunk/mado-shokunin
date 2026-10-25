author: hyaku closure (non-author integrator, @m_sonnet)

# Round 40 verifier spot-check (mado) - non-author closure

Measured against lane HEAD `fb49621074518333d855a2664ba5884c381079ad` (base `9fc511ddce708327377161202f358ce37dc266ba`), 2026-10-25. Driver digest (`.ufo/watchdog.log`, mutable): `2026-10-25T17:21:15-03:00 launch mado round=40 pgid=1571576 driver=hyaku-inline attempt=1` / `2026-10-25T19:22:57-03:00 complete mado round=40; hyaku-inline attempt=1`. Re-checks ran in a throwaway `git clone` of the lane at `fb49621` under `/tmp` (the lane tree was not touched).

## 1. Conformance (step 1)

| check | command | observed | result |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-40/mado.md` | `mado-shokunin 6e3b2846038be409836f14fba954ce14562f737d` | ok |
| SHONEN heading, one line per box | read report `## SHONEN` | 4 boxes, 4 lines, all `[~]` (none claims `[x]`) | ok |
| cited lane commits are ancestors of `master` | `git merge-base --is-ancestor <h> master` for 5e7e885, e2b51d3, 3721d54, 212d811, c96cf6d, 8122293, 91f0a2b, 3c80537, fb49621, 9fc511d | all `anc` | ok |
| pushed | `jj-lane.sh state` ; `git ls-remote origin refs/heads/master` | `local=remote=fb49621... ahead=0 behind=0`; remote ref `fb49621...` | ok |
| leftovers | `git status --porcelain` | one untracked `.ufo/waves/round-40/w1.ready.dispatched` (dispatch marker, no round work) | defect, status-neutral |
| prompt carries template contract | `.ufo/prompts/mado-round-40.md` headings | §1 MISSION/AXES, §2 claims, §2b frontier, §3 L2 floor, §4 report contract, §5 commit scope, §6 hyaku addendum | ok |
| real report, not a marker | 64-seat wave, 438 files / +131805 lines between base and tip, tool + 2 entries + 5 rows | real work | status `ok` |

Defects (status-neutral): (a) untracked `w1.ready.dispatched` left in the lane; (b) the report states `MADO_AXIS checked=3 mismatched=0 at fb49621` but only `receipts/axis-base.txt` (rev `9fc511d`) is committed under round-40 receipts - the tip axis run has no committed receipt (Evidence standard); (c) `ConnCrossClaim` wrote to a path of another round (disclosed M40-6).

## 2. Claims (step 2)

Counters are claim counters over committed bytes, not registered gates; I re-ran them in the clone with fresh nonces (they sandbox via bwrap and use a judge-held fake compositor) and also made plain measurements of my own. Re-measured vs evidence-verified is stated per row.

### C1 operability (capability acquisition): `tools/mado-options.py --live`

| item | reported | my measurement | match |
|---|---|---|---|
| tool sha256 at tip | `63b5ebd9...ef13` | `sha256sum tools/mado-options.py` -> `63b5ebd9446405ad0b29a79940244b45b145312cddb30b5e827250ed571fef13` (and `git diff --stat 91f0a2b fb49621 -- tools/` empty) | yes |
| tool selftest | 211/211 | `python3 -I tools/mado-options.py --selftest` -> `MADO_OPTIONS_SELFTEST: 211/211 passed` (base 71/71 in `ExecHarmChecks/05-...out`) | yes |
| v2 counter before | `fixtures=0/19 TARGET_MISSED` | `python3 -I quality/counters/c1-r40-live-v2.py --repo . --rev 9fc511d` -> `fixtures=0/19 tool=present verdict=TARGET_MISSED ... nonce=acaa0d7dcf6e8330` | yes |
| v2 counter after | `19/19 TARGET_MET` | same counter `--rev 91f0a2b` -> `fixtures=19/19 ... verdict=TARGET_MET ... nonce=35a126304f681969` (fresh nonce; lane's was `239e2809b1850614`), exit 0 | yes |
| live half (not a counter) | `62 agreement / 8 agreement* / 0 mismatch`, 70 declared keys, set true for 70 | `python3 -I tools/mado-options.py --home $HOME --live` against the running Hyprland (`HYPRLAND_INSTANCE_SIGNATURE` set) -> 70 rows, `{'agreement': 62, 'agreement*': 8}`, 70 `set` | yes |
| counter frozen before data | v2 counters, registration-v2 unchanged freeze -> tip | `git diff --stat 8122293 fb49621 -- quality/counters/c1-r40-live-v2.py quality/counters/c2-r40-forms-entry-v2.py .ufo/waves/round-40/registration-v2.md` empty; freeze `19:12:13` precedes data `19:20:13` | yes |
| controls | `CTL_C1V2 57/57`, `CTL_C2V2 33/33` | committed receipts `receipts/ctl-c1-v2.txt`, `ctl-c2-v2.txt` tails (evidence-verified, not re-executed) | yes |

Honest caveats the report already discloses and I confirm: the v1 predicates scored the same tool `13/13` but `TARGET_MISSED` (clause g import allowlist; `receipts/c1-v1-after-data.txt`, evidence-verified); the v2 predicates were written after the wave's seats had scored v1 (commits 3721d54..c96cf6d, 18:32-19:00, after wave dispatch e2b51d3 17:47) and the delivered tool is the byte-identical reference committed at freeze. This is a pre-registration tuned loop, not a clean pass; the freeze did precede data and the counters did not move after it. Verdict: **improved** (a capability the lane could not do at base - the base tool exits `rc=2` on `--live`).

### C2 coverage (sourced): `corpus/knowledge/hyprctl-getoption-native-forms-r40.md`

| item | reported | my measurement | match |
|---|---|---|---|
| counter before/after | `admitted=0/1` -> `1/1 TARGET_MET` | `c2-r40-forms-entry-v2.py --rev 9fc511d` -> `admitted=0/1 TARGET_MISSED`; `--rev 91f0a2b` -> `clauses=a..h:1 admitted=1`, `admitted=1/1 TARGET_MET` | yes |
| content, because the report itself says a fabricated self-consistent set passes | 353 options: int 264 / float 34 / str 28 / custom 21 / vec2 6; `set` true 70, false 283 | python over `w1/ExecAllOptionsForms/raw-census.jsonl` stdout JSON -> `Counter({'int': 264, 'float': 34, 'str': 28, 'custom': 21, 'vec2': 6})`, `set {False: 283, True: 70}`; and `grep -ao 'MS<[A-Za-z0-9:]*>'` over the committed S215 blob -> Bool 174, Int 84, Color 6 (=264), Float 34, String 28, Gradient 16 + CssGap 3 + FontWeight 2 (=21), Vec2 6 | yes, derived two independent ways |
| sources | S158, S162, S173, S180, S181, S215, S278, S279 | S158 vec2 line re-found at `HyprCtl.cpp:1708/1711` (below) | yes |
| rows | 214 -> 219 | `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` -> 219 at tip, 214 at `9fc511d` | yes |
| knowledge entries | 56 -> 58 (2 new) | `ls corpus/knowledge/*.md \| wc -l` 58 at tip, `git ls-tree ... \| grep -c .md` 56 at base; all 58 linked from `corpus/README.md` (loop count 58) | yes |

Verdict: **improved**. Residual named by the lane (admitted=1/1 measures admission wiring) is covered here by the independent content derivation above.

### Harm check (owned axes)

`git diff 9fc511d fb49621 -- SCORECARD.md` adds 21 lines only (Round 40 section; no existing line changed). `MADO_SELFTEST 460/460`, `MADO_VERIFY CLEAN (29 pass)`, base `MADO_AXIS checked=3 mismatched=0` are in committed `w1/ExecHarmChecks/` (evidence-verified, not executed - lane gates). Plain re-measures: index coverage 58/58 entries linked; `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` -> 7 W04 lines (S030, S042, S045, S097, S119, S120, S121) + 1 W01 (S277) + `mado ok`, exit 0 - identical to `receipts/census-before.txt` and `census-after.txt`; `QUALITY.md` diff is +8 lines (criteria 65-68 only, appended).

### Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| operability | improved | C1: new capability, re-measured 0/19 -> 19/19, live census 62/8/0 re-measured |
| coverage | improved | C2: two new entries on uncovered ground, content derived from raw census + S215 blob |
| navigation | unchanged | 58/58 indexed (re-counted); the tip `MADO_AXIS` receipt is uncommitted (defect b) but the plain count agrees |
| calibration | unchanged | no calibration claim; `SCORECARD.md` diff touches no calibration line |

## 3. Discernment spot-check (step 3)

| item | decision | re-opened source | agree? | reason |
|---|---|---|---|---|
| S280 omarchy `screen-recording.sh` (round-40 admit, successor entry) | admit | `curl https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/default/waybar/indicators/screen-recording.sh` | **agree** | sha256 `28491cd3...c63c` equals the row; the quote `if pgrep -f "^gpu-screen-recorder" >/dev/null; then` (9 words) is present at line 3; S281's sha256 `312900d1...de69` also matches live bytes |
| S158 HyprCtl vec2 line (admit, quote ≤25 words) | admit | `curl .../hyprwm/Hyprland/efb5099.../src/debug/HyprCtl.cpp` | **agree** | sha256 `798b7c6c...b91fa` equals the row; `R"({{"option": "{}", "vec2": [{},{}], "set": {} }})"` found at lines 1708 and 1711 (the lane's "note the space before the closing brace" is accurate) |
| S282 own-work quote `"exec": "~/.local/bin/gkeep waybar",` | admit | host `~/.config/waybar/config.jsonc` | **agree** | the live config still declares `ai-usage waybar`, `gkeep waybar`, `idle.sh`, `notification-silencing.sh`, `screen-recording.sh`, `weather.sh`, `omarchy-update-available`, `omarchy-voxtype-status` (8 exec lines; seven JSON producers is consistent) |
| K2 `host-producer-outputs-r29.md` as written | **reject** | `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/host-producer-outputs-r29.md`; host `~/.cache/ai-usage/status.json`; `pgrep -a hypridle` | **agree** | D1 "five producers" vs 8 exec lines/7 JSON on the host; D2 its own third "empty" member is the idle chip, which it says shows text, and it blames "no hypridle runs" while `pgrep -a hypridle` prints `1680 /usr/bin/hypridle`; D3 it quotes a rotating `updated_at: 2026-10-23T22:52:44Z`, the file now reads `2026-10-25T22:22:49Z` |
| K1 `host-bar-producers-r28` | reject as held | not re-opened (package copy and lane's held rows only read via the ledger) | no rule | could not independently re-grade; graded `unprovable`, not harmed |
| S224 label corrected to "unverifiable" | correction | not re-opened | no rule | outside the sampled pair; not re-measured |

Newly written `SOURCES.md` row re-opened: S280 and S281 (≤25-word quote check above), S278 quote `getoption [option] - gets the config option status (values)` is 9 words; `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` -> `mado ok`, exit 0.

Result: the sampled admits (S280/S281, S158, S282) and the sampled reject (K2) all agree with the lane's gate.

## 4. Trend verdicts

- **expansion: improved** - 2 admitted entries on new ground (native reply forms incl. the fifth form `vec2`, angle inheritance, host bar-producer census), 5 `mined` rows each cited by an entry, one capability row (`live option-table merge`).
- **quality: improved** - the wave falsified v1 and became 90 controls; entries re-derived in two independent ways (above); cost: v2 predicates were authored after seats scored v1 (disclosed). No admitted entry failed its re-check.
- **discernment: improved** - K2 refusal confirmed on three of its five defects against live host state (re-measured), admits confirmed byte-for-byte; criteria 65-68 each cite an M40 mistake.

## 5. Admission

Every claim verifies; no axis is harmed. Admitted.

## 6. Routed defects (next round)

1. Remove or commit the untracked `.ufo/waves/round-40/w1.ready.dispatched`.
2. Commit the tip axis receipt the report cites (`MADO_AXIS ... rev=fb49621...`) under `receipts/`.
3. The v1 counter's `TARGET_MISSED` for the same tool stays operator-ruled; next round runs the independent re-run of both v2 counters with fresh nonces (planned item 2) - done here once (nonce `35a126304f681969`), commit that as lane evidence.
4. SHONEN boxes: all four stay `[~]`; this spot-check is an outside verifier for the discernment/operability items but SKILL.md decision tables, PROVINCE rows and a cross-domain-bleed check were not re-measured, so nothing here is promotable by the operator yet.
