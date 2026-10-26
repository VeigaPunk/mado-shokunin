# R4b — round-45 errata re-verified by command (round-47 w2, seat ExecErrataR45)

Target: the six erratum blocks drafted by w1 seat `ScrErrataR45` in
`.ufo/waves/round-47/w1/ScrErrataR45/errata.md`, for the entry
`corpus/knowledge/hyprland-monitor-rule-r45.md` (sha256 `128df1bd1055fcbb…9c7b`, identical on disk and at
`4d22eeb`). Method: every corrected fact re-derived from the fourteen round-45 pins
(`.ufo/waves/round-45/fetch/`), the w1 pins, this seat's own pins, and the frozen counters; every locator
computed with `grep -n`/`awk NR==`. Nothing in the lane was edited; nothing was run against a changed config.

**Verdicts: 6/6 erratum subjects CONFIRMED, 0 refuted — but the block as drafted cannot be appended: it
turns the frozen round-45 admission counter from `TARGET_MET` to `TARGET_MISSED` (H1 below).**

| # | unit | subject | verdict |
|---|---|---|---|
| E1 | `entry:84` | mis-located monitor-added veto | **CONFIRMED** — corrected citation is exact |
| E2 | `entry:96` | wrong provenance (L1 draft receipt cited for the landed tool) | **CONFIRMED** — replacement receipt exists, is committed, prints the same lines |
| E3 | `entry:98` | hedge "not proof of which branch ran" | **CONFIRMED** — branch is closed by source + dump |
| E4 | `entry:18` | a9902ea pin | **CONFIRMED**, one sub-claim **WRONG** in the prose (H3) |
| E5 | `entry:106` | non-DRM descriptions | **CONFIRMED, stronger** — proved over the whole tag |
| E6 | `entry:107` | line form removed, rules survive | **CONFIRMED**, but its wording is what breaks the counter (H1) |

Reproduce everything: `python3 -I .ufo/waves/round-47/w2/ExecErrataR45/verify-r45-errata.py`
→ `RESULT: mismatches=0` (102 lines, `receipts/verify-r45-errata.txt`), and
`bash .ufo/waves/round-47/w2/ExecErrataR45/counter-append-test.sh <work> <block-as-drafted.md> <block-fixed.md>`
→ `receipts/counter-append-test.txt`.

---

## H1 — BLOCKER: appending the block as drafted drops the entry out of PRED-C2-r45

The E6 bullet is the only line of the append block that names a source id, and it names it in prose:

```
block-as-drafted.md:34:  (S303), so the `monitor =` line form is gone on main. Monitor rules are not: ...
```

`quality/counters/c2-r45-monitor-entry.py` (and its `-v2` sibling) implement clause g through
`all_body_lines_bound()`, which requires **every** unfenced entry line naming a cited id — other than its
`source:` line — to carry that id's Gate quote and locator. The appended line names `S303` and carries
neither, so `g` flips to 0 and the entry is no longer admitted:

```
$ bash .ufo/waves/round-47/w2/ExecErrataR45/counter-append-test.sh <work> block-as-drafted.md block-fixed.md
== 1. baseline: frozen entry, no errata ==
PRED-C2-r45: admitted=1/1 verdict=TARGET_MET rev=4d22eeb66c2835af8aaa3fac6ad838fa616aa663
PRED-C2-r45-v2: admitted=1/1 verdict=TARGET_MET rev=4d22eeb66c2835af8aaa3fac6ad838fa616aa663
== verbatim-block-no-blank-line (rev 2bb69e30) ==
PRED-C2-r45: admitted=0/1 verdict=TARGET_MISSED rev=2bb69e3073793dd837a83afd024a5483ae687a5f
PRED-C2-r45-v2: admitted=0/1 verdict=TARGET_MISSED rev=2bb69e3073793dd837a83afd024a5483ae687a5f
== verbatim-block-with-blank-line (rev 050c516a) ==
PRED-C2-r45: admitted=0/1 verdict=TARGET_MISSED rev=050c516adc1f9989f24ee1347ae1e79fd7225317
PRED-C2-r45-v2: admitted=0/1 verdict=TARGET_MISSED rev=050c516adc1f9989f24ee1347ae1e79fd7225317
== fixed-block (rev 418d66c5) ==
PRED-C2-r45: admitted=1/1 verdict=TARGET_MET rev=418d66c58f94cbdc8c966b2200cef97469c961d7
PRED-C2-r45-v2: admitted=1/1 verdict=TARGET_MET rev=418d66c58f94cbdc8c966b2200cef97469c961d7
```

(The verbatim rows print `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:0 h:1 i:1 j:1 admitted=0` in
`receipts/counter-append-test.txt`; the short hashes differ between runs because every run makes fresh commits.
The test clones the lane read-only into `<work>`, checks out `4d22eeb`, appends, commits with a scratch
identity after asserting `rev-parse --show-toplevel` equals the clone, and runs both frozen counters. Baseline
and fixed variants are green; both verbatim variants are red, with or without the blank line.)

**Fix (one token, nothing else):** drop the id from the E6 bullet — it reads
"(the handler row the entry's source list cites)" in `block-fixed.md` — and prepend the blank line of H2. That
exact text is `block-fixed.md` (38 lines, ready to `cat >>` the entry); it scores `admitted=1/1 TARGET_MET` on
both counters, and `receipts/block-diff.txt` is the two-line diff against the drafted block.

## H2 — shape: the block starts with an H2 and no blank line (cosmetic, convention-breaking)

- The entry ends at line 107 inside the `## Limits` list, with a final `\n` (`last byte 0x0a`), eight
  column-0 H2 sections, and no errata section of its own — appending at the end is the right place and shifts
  no earlier line.
- All 21 existing `## Errata` headings under `corpus/knowledge/` are preceded by a blank line (21/21,
  recomputed); `block-as-drafted.md` starts with the heading, `block-fixed.md` starts with the blank line.
- This is hygiene, not breakage: `cmark` renders `## Errata` as its own `<h2>` with all six E bullets as list
  items in both shapes (`h2=9 li=10`), so no parser swallows it into the `## Limits` list.
- The block's own locators are all pin/receipt lines, never entry lines, so appending cannot invalidate them;
  the table above the block cites `entry:18/84/96/98/106/107`, which appending also leaves in place.

## H3 — E4 prose WRONG: the `CONFIG_LEGACY` enumerator is not in `ConfigManager.cpp`

The errata *body* (`w1/ScrErrataR45/errata.md:92-93`) says the commit "drops the `Legacy::CConfigManager`
selection and the `CONFIG_LEGACY` enum from `src/config/ConfigManager.cpp`". The commit's own patch splits it:

```
src/config/ConfigManager.cpp   -        case CONFIG_LEGACY: return "hyprlang";
src/config/ConfigManager.hpp   -        CONFIG_LEGACY = 0,
```

and `ConfigManager.hpp` at `a9902ea` (pin `pins/hyprland-ConfigManager-hpp-a9902ea.hpp`, sha256
`389365c4…9712`) keeps `enum eConfigManagerType : uint8_t {` at line 27 with `CONFIG_LUA` only. The `.cpp`
loses the *case* and the two `Legacy::CConfigManager` selections; the *enumerator* is removed from the
header. Corrected wording: "the `Legacy::CConfigManager` selection and the `case CONFIG_LEGACY:` in
`src/config/ConfigManager.cpp`, and the enumerator in `src/config/ConfigManager.hpp`". The appended block is
already accurate on this point (`block-fixed.md:24-25`, "the `Legacy`/`CONFIG_LEGACY` selection in
`src/config/ConfigManager.cpp`"), so only the prose above the block needs the fix. Everything else in E4
holds: commit `a9902ea65f461af868497c4e74fed798ade0b1b0`, `2026-07-22T16:35:10Z`,
`config: remove legacy config support (#15539)`, `src/config/legacy/ConfigManager.cpp` removed with 2184
deletions, the raw file 14 bytes `404: Not Found`, and the main manager instantiating only
`Lua::CConfigManager` at lines 30 and 33.

## E1 — CONFIRMED (`entry:84`)

`CMonitor::onConnect` opens at `Hyprland-Monitor.cpp:108`; `:264` is the already-enabled branch that applies
the rule (`:266`) and `return`s at `:271`; the disabled veto is `:275` → `m_enabled = false;` (`:283`) →
`return;` (`:286`); a fresh monitor is `m_enabled = false;` (`Hyprland-Monitor-efb5099.hpp:357`), so an
enabled rule falls through `:302` to the single emit at `:389`
(`Event::bus()->m_events.monitor.added.emit(m_self.lock());`). Re-grepped across every `.cpp`/`.hpp` in the
fourteen pins: exactly one `monitor.added.emit`, at `Hyprland-Monitor.cpp:389`; the listener is
`Hyprland-MonitorState.cpp:25`. The corrected citation `:275-287` + `:389` (with `:302`) is exact and the
claim is unchanged. No early `return` exists between `:302` and `:389` (the only `return` tokens there sit
inside `none_of`/`count_if` lambdas at `:328`/`:331`).

## E2 — CONFIRMED (`entry:96`)

`live-monitors-host-l1.txt:1` runs `l1-draft/mado-monitors.py` and `:4` records `# tool sha256 c6ac5fc2…`;
`.ufo/waves/round-45/l1-draft/mado-monitors.py` hashes to exactly that, so the receipt is honest but is not a
receipt of the landed tool. The landed tool is `2f007417…f5609` at `4d22eeb`, at base `60edb66e`, and on
disk; `live-monitors-host-r45.txt` records `# tool sha256 2f007417…` (`:4`) and prints `verdict=AGREE` (`:7`),
`verdict=OK` (`:8`), `exit=0` (`:9`) with the same config hash line (`:3`, `69c9d899…`) and the same
`MADO_MON_RULE`/`MADO_MON_OUTPUT`/`MADO_MONITORS` lines. That receipt is committed at the freeze
(`git cat-file -e 4d22eeb:.ufo/waves/round-45/receipts/live-monitors-host-r45.txt` succeeds; added in
`ee6659b`), so the replacement citation is durable. The sentence's substance stands.

## E3 — CONFIRMED (`entry:98`)

The push is guarded by three negated strict bounds of 1 px / 1 px / 1 Hz
(`Hyprland-Monitor.cpp:836-837`; `DELTALESSTHAN` is `abs((a) - (b)) < (delta)` at `Hyprland-macros.hpp:40`).
`addBest3Modes` sorts best-first, keeps three and inserts them reversed
(`requestedModes.insert_range(requestedModes.end(), sortedModes | std::views::reverse);`), so
`requestedModes.back()` is the mode closest to the request — here the applied `3440x1440@99.997`
(`live-monitors-host-l1.txt:11`, `"refreshRate": 99.997`; rule at `:6`, `mode=3440x1440@100.00`). All three
negations are therefore false: `|99.997-100.000| = 0.003 < 1`, both pixel dimensions equal, so the
`requestedModes.push_back(` at `:838` cannot run and no custom 100 Hz mode was tried. Had it run it would be
tried first (`:878`, reverse iteration) and an accepted custom mode would have set `m_refreshRate` to
100.000 at `:903` — the dump shows 99.997, so the branch is closed by source plus dump. A fresh read-only
`hyprctl -j monitors all` still reports `refreshRate 99.997` (`receipts/host-shape.txt`).

## E4 — CONFIRMED except H3 (`entry:18`)

Pin facts recomputed from `pins/hyprland-commit-a9902ea.json` (sha256 `c33ba383…0639`): sha
`a9902ea65f461af868497c4e74fed798ade0b1b0`, committer date `2026-07-22T16:35:10Z`, message
`config: remove legacy config support (#15539)`, 29 files, `src/config/legacy/ConfigManager.cpp`
`status=removed`, `deletions=2184`; `legacy-cfg-a9902ea.txt` is the 14-byte `404: Not Found`;
`hyprland-main-cfg-a9902ea.cpp` has no `Legacy` occurrence and only the two `Lua::CConfigManager`
instantiations at lines 30 and 33. Claim stands. Only the enum's location is mis-stated (H3).

## E5 — CONFIRMED, and the universal form is proved over the whole tag (`entry:106`)

Grepping every `.cpp`/`.hpp` of the aquamarine v0.15.1 tarball
(`pins/aquamarine-v0.15.1.tar.gz`, sha256 `2f9de98c…96f2`) yields exactly three `description` occurrences:

```
include/aquamarine/output/Output.hpp:258   std::string ... name, description, make, model, serial;   (whitespace collapsed)
src/backend/drm/DRM.cpp:2101               output->description = std::format("{} {} {} ({})", make, model, serial, szName);
src/backend/drm/DRM.cpp:2104               ...log(AQ_LOG_DEBUG, std::format("drm: Description {}", output->description));   (abridged)
```

`src/backend/Wayland.cpp`, `src/backend/Headless.cpp`, `src/backend/Null.cpp`, `src/backend/Backend.cpp`
and `src/output/Output.cpp` contain none; `createOutput` in the Wayland and headless backends only names the
output (`:168-181`, `:187-200`). Hyprland then copies the empty field at `Hyprland-Monitor.cpp:250` and
builds the short description from make/model/serial at `:255`. So a non-DRM output gets empty descriptions
because no backend builds one — not because one is built differently, exactly as E5 says. The block's
parenthetical "Not observed on this host, whose only output is DRM" is supported read-only: one monitor, with
`make`/`model`/`serial`/`description` all non-empty (lengths only in `receipts/host-shape.txt`; only
`DRM.cpp:2101` assigns a description, so non-empty implies DRM).

## E6 — CONFIRMED, subject to H1 (`entry:107`)

The commit that removes the legacy manager is the file S303 cites (`entry:4`), and that file registers the
keyword: `Hyprland-legacy-ConfigManager.cpp:606`
`m_config->registerHandler(&::handleMonitor, "monitor", {false});`. Rules survive on main: the Lua binding
includes the shared parser (`LuaBindingsConfigRules.cpp:20`, `#include "../../shared/monitor/Parser.hpp"`),
declares `MONITOR_FIELDS[]` at `:80` feeding `CMonitorRuleParser`, and the Lua manager still drives the rule
manager (`hyprland-lua-cfg-a9902ea.cpp:809-810`, `scheduleReload();` / `ensureMonitorStatus();`). So the
`monitor =` grammar is what is gone, exactly as the sentence says.

## Notes that are not holes

- **S1 (`90d`)** is re-confirmed directly. The first REST attempt this seat returned
  `403 API rate limit exceeded`; the retry returned the same body w1 recorded —
  `"No commit found for SHA: 90d"`, `http_code=422` — against `http_code_full=200` for a full 40-hex sha, and
  the HTML path agrees (`commit/90d` → `404`, `commit/efb5099` → `200`) (`receipts/90d-probe.txt`). Action
  unchanged: pin a concrete revision or drop the parenthetical.
- **Header wording**: "the round-45 w2 entry as landed at `4d22eeb`". The entry actually landed in
  `ee6659b90f7bf69aa03283dba804dd90081b7ff5` (2026-10-26 16:47:11 -0300); `4d22eeb` is the later tip-receipt
  commit that still holds the identical bytes (`git show 4d22eeb:… | sha256sum` = `128df1bd…9c7b`). No
  content error; "unchanged since `ee6659b` / at the `4d22eeb` freeze" would be exact.
- **The w1 draft's own verifier** re-runs clean: `python3 -I .ufo/waves/round-47/w1/ScrErrataR45/verify.py`
  → `RESULT: mismatches=0` (`receipts/w1-verify-rerun.txt`), and all 16 of its pins match its `PINS.md`.

## What the L1 should do

1. Append `block-fixed.md`, not the fenced block as drafted (H1) — or apply the single-token fix by hand.
2. Keep the leading blank line (H2) so the appended heading matches all 21 existing errata headings.
3. Fix the E4 prose (H3): the appended block's own E4 wording is already accurate, but the paragraph above it
   names the wrong file for the `CONFIG_LEGACY` enumerator.
4. Optionally re-run `quality/counters/c2-r45-monitor-entry.py --repo <lane> --rev <rev>` after integration:
   the entry must stay `admitted=1/1 TARGET_MET`.

## Evidence index (all under `.ufo/waves/round-47/w2/ExecErrataR45/`)

| artifact | what it is |
|---|---|
| `verify-r45-errata.py` / `receipts/verify-r45-errata.txt` | re-derives every erratum and the shape checks; `RESULT: mismatches=0` |
| `counter-append-test.sh` / `receipts/counter-append-test.txt` | the clone-and-append experiment against both frozen round-45 counters (H1) |
| `block-as-drafted.md`, `block-fixed.md` | the block verbatim from `errata.md`, and the same block ready to append |
| `receipts/host-shape.txt` | read-only `hyprctl -j monitors all` shape check (lengths only) |
| `receipts/90d-probe.txt` | the `90d` re-probe: REST `422` + `http_code_full=200`, HTML `404` vs control `200` |
| `receipts/w1-verify-rerun.txt` | the w1 verifier re-run, `mismatches=0` |
| `pins/` + `pins/PINS.md` | this seat's four pins, URLs and sha256 |
