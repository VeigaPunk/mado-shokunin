# R4b (round 48 w1, seat ExecErrataR45) — the round-45 errata, worded to keep the frozen C2 verdict

**Verdict: the block is ready and green.** `.ufo/waves/round-48/w1/ExecErrataR45/block.md` (51 lines,
sha256 `7865c15e07bce4a3e63d11372909d71ef89e47f7e8f94e7bc3568e47c179ae22`) carries all six confirmed
corrections (E1-E6 of the round-47 w2 seat), is append-only, and leaves both frozen round-45 admission
counters at `admitted=1/1 verdict=TARGET_MET` before and after the append, at the round-45 freeze rev, at
the round-48 base and at the lane tip. Two negative controls with the same machinery print
`admitted=0/1 verdict=TARGET_MISSED` with clause `g:0` — the instrument still bites.

Nothing in the lane was edited: `git diff --stat` in the lane is empty, the entry is byte-identical
(`sha256 128df1bd…9c7b`) and all proof work happened in throwaway clones.

## 1. What the frozen instrument punishes (the round-47 H1, re-derived)

`PRED-C2-r45` clause `g` (docstring `quality/counters/c2-r45-monitor-entry.py:37`) requires that
"EVERY unfenced line naming a cited id" carries that id's Gate quote and computed locator. The code is
`all_body_lines_bound()` (`quality/counters/c2-r45-monitor-entry.py:286`, `-v2.py:308`), wired into
`cl["g"]` (`:612`, `-v2.py:665`). The round-47 as-drafted block put one source id in prose —
`block-as-drafted.md:34` reads "(S303), so the `monitor =` line form is gone on main" — with neither
quote nor locator, so `g` flips to 0.

**The fix is one token: the block never names a source id.** In this block E6 says "the legacy handler
file the entry's source list names" (`block.md:48`). That is mechanically checked, not assumed: the
verifier's first tripwire greps the block for `\b[Ss]\d{3,}\b` and finds none.

Five more tripwires are checked the same way, because they are the other ways an append can drop a
clause: no census token with a value (v2 clause `h`/T1), no fence marker (v2 clause `b`/T3), no
`source:`/`verified-at:`/`recheck:` line (clause `b`), no `BAD_LOC` marker (clause `i`), and the
one-leading-blank-line-then-H2 shape (21/21 existing errata headings).

## 2. Proof on a scratch clone — receipts

Command (scratch dir passed explicitly; the trap deletes it):

```
bash .ufo/waves/round-48/w1/ExecErrataR45/counter-append-test.sh \
     /fast/scratch/hyaku/mado-r48/ExecErrataR45 <block.md> <seat>/receipts
```

`receipts/counter-append-test.txt` (clone `--shared --no-checkout` of the lane, `rev-parse --show-toplevel`
asserted equal to the clone, `checkout --detach`, append, `git add` the entry, commit with
`-c user.name=seat -c user.email=seat@scratch.invalid`):

| rev | state | `PRED-C2-r45` | `PRED-C2-r45-v2` |
|---|---|---|---|
| `4d22eeb` (round-45 freeze) | baseline | `admitted=1/1 TARGET_MET` exit 0 | `admitted=1/1 TARGET_MET` exit 0 |
| `4d22eeb` + block (`6308308`) | after | `admitted=1/1 TARGET_MET` exit 0 | `admitted=1/1 TARGET_MET` exit 0 |
| `579f694` (round-48 base) | baseline | `admitted=1/1 TARGET_MET` exit 0 | `admitted=1/1 TARGET_MET` exit 0 |
| `579f694` + block (`a2b0dde`) | after | `admitted=1/1 TARGET_MET` exit 0 | `admitted=1/1 TARGET_MET` exit 0 |
| `5ff1674` (lane tip) | baseline | `admitted=1/1 TARGET_MET` exit 0 | `admitted=1/1 TARGET_MET` exit 0 |
| `5ff1674` + block (`91683db`) | after | `admitted=1/1 TARGET_MET` exit 0 | `admitted=1/1 TARGET_MET` exit 0 |

Every row prints `clauses=a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1`. The appended entry is 158 lines,
`sha256 73a6c4ac…1ffa0e` at all three revs (identical bytes: the block is a pure append on an unchanged
landed prefix).

Negative controls (same clone, same commit path, at `579f694`):

| control | `PRED-C2-r45` | v2 |
|---|---|---|
| this block with `(S303)` put back into E6 | `a:1 b:1 c:1 d:1 e:1 f:1 g:0 … admitted=0/1 TARGET_MISSED` exit 1 | same, `g:0` |
| the round-47 block as drafted | `… g:0 … admitted=0/1 TARGET_MISSED` exit 1 | same, `g:0` |

The first control isolates the one difference: every other byte of the block is the text that measures
`MET`, so clause `g` is the only thing the id touches.

## 3. The round-48 locator check (every line the block cites)

`python3 -I .ufo/waves/round-48/w1/ExecErrataR45/verify-locators.py --repo . --block <block.md>` →
`RESULT: checks_failed=0` (`receipts/verify-locators.txt`, 100+ lines). It is run twice more inside the
append test against the appended trees at `579f694` and at the lane tip — `checks_failed=0` both times.

Direction of the check: the block's numbers are never trusted. For each citation the verifier prints the
cited range from the pinned receipt plus that receipt's sha256 and line count; for each quoted anchor it
recomputes the line with a line scan and requires that line to sit inside a range the *same bullet*
cites. Result highlights (all `cited OK`):

- `Hyprland-Monitor.cpp` (round-45 fetch, sha `9cf88e15…`): `:302` = `m_enabled = true;`, `:389` = the only
  `monitor.added.emit`, `:275` = `if (monitorRule.m_disabled) {`, `:283` = `m_enabled = false;`,
  `:286` = `return;`, `:264` = `if (m_enabled && !monitorRule.m_disabled) {`, `:108` = `void
  CMonitor::onConnect(bool noRule) {`, `:271` = the already-enabled `return;`, `:836-837` = the three
  negated bounds, `:838-839` = the custom-mode push, `:903` = `m_refreshRate = mode->refreshRate / 1000.f;`,
  `:250` = `m_description = m_output->description;`, `:255-256` = the short-description build.
- `Hyprland-macros.hpp:40` = `#define DELTALESSTHAN(a, b, delta) (abs((a) - (b)) < (delta))`.
- `Hyprland-Monitor-efb5099.hpp:357` = `bool m_enabled = false;` (round-47 w1 pin, sha `4e9d8847…`).
- `hyprland-ConfigManager-hpp-a9902ea.hpp:27-28` = `enum eConfigManagerType : uint8_t {` / `CONFIG_LUA,`
  (round-47 w2 pin, sha `389365c4…`); `CONFIG_LEGACY` occurs 0 times in that header.
- `hyprland-main-cfg-a9902ea.cpp` (`src/config/ConfigManager.cpp`): `:30` and `:33` =
  `g_mgr = makeUnique<Lua::CConfigManager>();`, `Legacy` occurs 0 times, exactly two instantiations.
- `aqua-Output.hpp:258` = `name, description, make, model, serial;`; `aqua-DRM-v0.15.1.cpp:2101` =
  `output->description = std::format("{} {} {} ({})", make, model, serial, szName);`; `description`
  occurs 0 times in `aqua-Wayland-v0.15.1.cpp`, `aqua-Headless-v0.15.1.cpp`, `aqua-Output-v0.15.1.cpp`
  (their `createOutput` is at `:168`, `:187`).
- `hyprland-LuaBindingsConfigRules-a9902ea.cpp:80` = `inline constexpr SMonitorFieldDesc MONITOR_FIELDS[] = {`;
  `hyprland-lua-cfg-a9902ea.cpp:809-810` = `scheduleReload();` / `ensureMonitorStatus();`.
- Receipts: `live-monitors-host-l1.txt` line 4 = `# tool sha256 c6ac5fc2…`; `live-monitors-host-r45.txt`
  line 4 = `# tool sha256 2f007417…`, line 7 = `verdict=AGREE`, line 8 = `verdict=OK`, line 9 = `exit=0`.
  `tools/mado-monitors.py` at `4d22eeb` hashes to `2f007417…f5609`.
- Entry lines (computed, not typed): `:18` (`recheck:` / "upstream main already drops …"), `:84`
  (`Hyprland-Monitor.cpp:264 and …:389`), `:96` (`live-monitors-host-l1.txt`), `:98` (`99.997`/`0.003`),
  `:100` (`UNK` … `59.99`), `:106` (Wayland/headless description), `:107` (`hyprland line form`).
- Pin integrity: the fourteen round-45 fetch pins are 14/14 byte-identical to
  `.ufo/waves/round-45/receipts/fetch-sha256.txt`, so the locators are read against pinned bytes.
- Append-only: the verifier recomputes `sha256` of the entry **up to the first `## Errata` heading** and
  requires `128df1bd…9c7b`; the whole-file hash differs only because of the appended block.

## 4. The six corrections in the block

| # | entry line | what the block corrects | how it is verified |
|---|---|---|---|
| E1 | `:84` | `Hyprland-Monitor.cpp:264` is the already-enabled branch (applies, returns at `:271`), not the veto; the veto is `:275`-`:287`, and the emit is the single `:389` reached via `:302` | anchors `:302`/`:275`/`:283` recomputed; emit count is exactly 1 across the pins, at `:389` |
| E2 | `:96` | the cited host receipt is the L1 draft (`c6ac5fc2…`), not the landed tool; the landed tool at `4d22eeb` is `2f007417…` and its own receipt prints the same lines | tool hash recomputed (`git show`), four receipt lines bound |
| E3 | `:98` | the 100 Hz branch is closed (`0.003 < 1`, equal pixel sizes ⇒ push at `:838-839` cannot run); only the UNK paragraph at `:100` remains | `:836-837`, `:903`, macros `:40` recomputed |
| E4 | `:18` | the pin holds; **added: the `CONFIG_LEGACY` enumerator is removed from `ConfigManager.hpp` (`:27-28`), not from the `.cpp`** — the `.cpp` keeps only `Lua::CConfigManager` (`:30`, `:33`) | commit pin: sha, date, message, 29 files, legacy manager removed with 2184 deletions, raw file 14-byte `404: Not Found` |
| E5 | `:106` | the landed wording ("builds its description differently") is false: no non-DRM backend builds one; the field stays empty | `description` count 0 in three backend/source pins, only DRM at `:2101` assigns; `:250`/`:255-256` recomputed |
| E6 | `:107` | the claim holds within that scope: the Lua binding parses monitor rules, so `monitor =` (the grammar) is what is gone | `MONITOR_FIELDS[]` at `:80`, manager drive at `:809-810` |

E4 is where this block goes beyond the round-47 draft: that draft's E4 bullet still said "the
`Legacy`/`CONFIG_LEGACY` selection in `src/config/ConfigManager.cpp`", which is the imprecision its own
H3 flagged. `block.md` names the header for the enumerator and cites the header pin. `receipts/block-diff.txt`
is the diff against round-47's `block-fixed.md`: E4 wording, the explicit `entry line`/`receipt line`
convention, the concrete UNK reference, and one lead-in line naming where the pin copies live.

## 5. Risks, residuals, and what integration must not do

1. **Integrate at the round-48 tip, not at `4d22eeb`.** The counters pass at `4d22eeb`, but the block
   cites round-47 pins under `.ufo/waves/round-47/w1/ScrErrataR45/pins/` and
   `.ufo/waves/round-47/w2/ExecErrataR45/pins/`, which are tracked only from `579f694` on. Appended at
   `4d22eeb`, the block's citations would point at paths that do not exist there (the counters would not
   notice; a reader would).
2. **The frozen predicates do not bind the block's citations.** Clauses `a`-`j` read the entry's ids,
   census line, README row and surfaces; no clause reads an errata bullet's `file:line`. The locator
   proof here is a seat receipt, not a counter — a w2 attacker could change a cited number inside the
   errata and both counters would stay `MET`. The seat verifier is the only instrument that catches that.
3. **The verifier's anchor rule is deliberately narrow** (quoted spans with a space and ≥ 12 normalized
   characters). Single tokens such as `createOutput`, `CONFIG_LEGACY`, `monitor =` and `monitor.added.emit`
   are covered by the dedicated absence/uniqueness checks instead, not by the anchor rule.
4. **Shortened locators.** E1/E3 use the shorthand `:283`, `:286`, `:271` after a full file name; the
   verifier carries the file context, a cold reader must too. The heading keeps "stands as landed at
   4d22eeb" although the append happens later — that is the point of the sentence (the landed text is
   what is being corrected, and it is byte-identical at every rev tested).
5. **Scope discipline.** No lane file, counter, fixture, registry row or README row was touched; no
   host service, compositor, package transaction or GUI program was used; no tool was installed this seat;
   the scratch tree `/fast/scratch/hyaku/mado-r48/ExecErrataR45` is deleted by the script's trap (verified
   absent afterwards). Commit identity in the clone is `seat <seat@scratch.invalid>` and
   `rev-parse --show-toplevel` was asserted before the first commit.

## 6. Files in this seat directory

| file | what it is |
|---|---|
| `block.md` | the deliverable: 51 lines, appended with `cat block.md >> corpus/knowledge/hyprland-monitor-rule-r45.md` |
| `verify-locators.py` | the round-48 locator check (entry lines, pin lines, anchors, absences, pin integrity, append-only prefix, six tripwires) |
| `receipts/verify-locators.txt` | its run on the lane tree: `RESULT: checks_failed=0` |
| `counter-append-test.sh` | clone + baseline + append + commit + both counters + two controls + locator check in the appended tree |
| `receipts/counter-append-test.txt` | six `TARGET_MET` rows, two `TARGET_MISSED` controls, two `checks_failed=0` locator runs |
| `receipts/block-diff.txt` | diff and sha256 against round-47's `block-fixed.md` |
