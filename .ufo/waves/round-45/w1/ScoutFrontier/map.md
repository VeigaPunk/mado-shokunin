# ScoutFrontier map — where the monitor plane sits (lane HEAD ebdba13f, read-only)

All line numbers computed with `grep -n` / `sed -n` on the working tree at `ebdba13f`.

## 1. Held ground the new entry touches (what is already said about monitors)

| Where | Text (<=25 words) | Relation to C1/C2 |
|---|---|---|
| `SKILL.md:75` | `Monitor layout / scale / position` -> `monitors.conf:10`; live `DP-1 3440x1440@99.997; config declares @100` | the host fact the tool's AGREE/refresh tolerance must reproduce (live run receipts/live-monitors-host-l1.txt) |
| `SKILL.md:179` (S3 row) | `F4-F10 (grok-bot absent; monitor 99.997 vs 100; ...` | the held "EDID nominal quantization [INF]" class: entry's refresh_tolerance=1 is the sourced replacement; do not edit the held row, add a dated pointer only |
| `corpus/knowledge/output-colour-boundaries-r14.md` (108 L) | Decision table + `## Unexercised feature behavior`: `monitor-rule HDR/ICC settings and output-power behavior remain unexercised` | the only held monitor/output entry. It is the *protocol* route (wlr-output-management, colour-management-v1); it never reads a `monitor =` line, `MonitorRule.hpp`, or `hyprctl monitors all -j`. Header shape to mirror: `source:` / `verified-at:` / `recheck:` / `covers:` lines, then H1, decision table, then `Rejected candidates`. Its safety caveat (S050: `setDisableHead` -> `scheduleReload()`; output-management transaction = mutation-class) is why the new tool must stay file+dump-only. |
| `corpus/knowledge/hyprctl-verification-layer.md` (README:15 row) | 9 non-getoption pairs incl. monitors | held point sample of `hyprctl monitors`, not a rule-to-state join |

No held entry covers the `monitor =` line grammar, the 1/120 scale correction, refresh tolerance, or mirror/transform keys: C2's grep claim at base exits 1 (`receipts/c2-ground-base.txt`).

## 2. Frontier text the new entry moves

`corpus/README.md`, `## Frontier` starts at line 105. Two held phrases cover this plane:

1. **Line 128-132 (round-12 bullet), exact line 131:**
   `  Still open: rule *attribution*, output-management behavior, the input debugging`
   -> "output-management behavior" is the phrase a monitor-rule chain narrows (the rule->state half, not the wlr-output-management protocol half, which round 14 already took).
2. **Line 136-139 (round-14 bullet), exact lines 137-139:**
   `Output test/apply,` / `runtime state agreement, colour/HDR rendering and physical accuracy remain` / `unknown; this is neither full U5 feature coverage nor a hardware-health verdict.`
   -> "runtime state agreement" is the one item round 45 moves, and only for the declared-rule vs `hyprctl monitors all -j` field set (mode, position, scale, transform, mirror). Still open after it (keep verbatim): output test/apply, colour/HDR rendering, physical accuracy, hotplug, `keyword monitor` runtime overrides, `monitorv2`/Lua `hl.monitor` grammar if the entry does not source it.

Do NOT rewrite lines 131/137-139 (held, append-only convention; r21 correction at 193-195 shows how corrections are appended). The bullet list (107-191) stopped getting per-round bullets after round 40 (line 107: `- Round 40 moves the ...`, the topmost, newest-first); rounds 43/44 were added as **`###` subsections at the file's tail**, not bullets:
   - `### Round-43 rule-size versus reported-size route` at line 295 (one bullet, 296-302)
   - `### Round-44 gkeep size-request route` at line 304 (one bullet, 305-320; file ends at 320 with `unmeasured.`)
   Mirror this: append `### Round-45 monitor-rule route` after line 320 with one bullet: "Moves the round-14 open item 'runtime state agreement' (line 137-139) and the round-12 'output-management behavior' (line 131) onto sourced ground for the monitor-rule chain: `[entry link]`, rows S302-S310, instrumented by `tools/mado-monitors.py` (AGREE/DIFFER/DISABLED/UNRULED). Still open: ...". (Alternatively a new line-107-style bullet at the top; the tail-subsection form is the r43/r44 precedent.)

## 3. README index row shape (`## Coverage map`, table lines 9-72)

- Table header `| Note | Holds | Sources |` (line 9-10); newest rows are at the bottom: line 71 = r43 geometry row, line 72 = r44 row (last row; blank line 73; `## Quality bar` at 74). **Insert the new row after line 72.**
- Counter clause f (`quality/counters/c2-r45-monitor-entry.py:614-615`): regex `^\| \`knowledge/hyprland-monitor-rule-r45\.md\`` must match **exactly one** unfenced, column-0 line. So the row must start `| \`knowledge/hyprland-monitor-rule-r45.md\``; never reproduce that prefix elsewhere (e.g. in a table inside a code fence is fine, in a second row is not).
- Shape (3 cells; r43/r44 precedent, lines 71-72):
  `| \`knowledge/hyprland-monitor-rule-r45.md\` (MADO-R45-1, round 45; <theme/successor note>) | <What it holds: the chain from the \`monitor =\` line (parser keys, default refresh 60 / tolerance 1, scale step 1/120, 89-step search) to \`hyprctl monitors all -j\` (json refresh 5 decimals); tool \`tools/mado-monitors.py\`; host: one output DP-1, AGREE/OK>. | S302, S303, S304, S305, S306, S307, S308, S309, S310 |`
  The r43/r44 third cell is a bare id list (`S290, S291, ... S158`), r39/r40 likewise; older rows use `source:` + `[SOURCES](SOURCES.md)` prose (line 39 r14 row, line 56 r24 row). Use the bare id list (newest convention). L1's draft already inserts the row via `l1-draft/build-pos.py:97-99` (`k = max(i ... startswith("| \`knowledge/hyprland-gkeep-size-request-r44.md\`"))`, insert at k+1) with text `| \`knowledge/hyprland-monitor-rule-r45.md\` (MADO-R45-1, round 45) | draft | S302-S310 |` - a placeholder, to be replaced by the real Holds text (the counter checks only the prefix).
- Row length: r43/r44 rows run 1.5-3 kB on one line; no counter bound beyond clause f.
- Province-route table (`## Province routes`, lines 81-90): row 1 `Hyprland config, binds, rules and display` (line ~83) is the display route; its Evidence cell lists "dated `getoption`, binds and monitor reads" - optional dated pointer, not required by any counter.

## 4. SKILL.md: where the tool and its exit map belong (mirror round-43/44 mado-geometry)

| Table / section | Existing geometry/globals line(s) | New-tool content to add |
|---|---|---|
| `### Claim-first routing` table (heading line 142, rows to 158) | **line 158** (geometry; last row; blank 159; `### Divergence vocabulary` at 160). Line 157 = globals row. | add a row after 158: `Does the monitor rule a config declares match what the compositor reports for that output?` / `two read-only inputs, no new verb: file bytes (the monitor = lines) + hyprctl live (monitors all -j)` / `hyprctl monitors all -j \| python3 tools/mado-monitors.py --dump - --rules <file>` (flag names per the draft docstring `l1-draft/mado-monitors.py`, not guessed) / tag `[OBS]` for both printed sides; hotplug, apply, rendered output, colour stay `[UNK]` |
| `### Read-only probes` table (heading line 204; rows 206-225) | **line 224** = globals row, **line 225** = geometry row (last row; blank 226; `### Advertised Wayland globals` at 227). Row shape: `` `cmd` \| what it answers + verdict set + \`--selftest\` \| host run date, verbatim MADO_ line, rc; per-verdict licence in § "..." `` | add a row after 225 with the real host run line from `receipts/live-monitors-host-l1.txt` (AGREE, verdict OK, rc 0) |
| Section `### Rule size versus reported size` (line 246, ends 312; next `### Mutating commands` at 314) | line 248-252 intro (inputs, output lines); 254-258 support ceiling; 260-270 chain citation; **per-verdict licence table 272-283** (header `\| Verdict \| Licenses \| Does not license \|`); **exit map line 284-285** (`Exit map: 0 \`OK\` · 1 \`DIFFER\` ...`, then `5 \`NOT_COMPARED\` (round 44).`); 286-292 round-44 addendum; 295-300 host-run block; 307-312 known limit + `timeout 5` advice | add a sibling `### Monitor rule versus reported monitor` section after line 312 (before line 314), same skeleton: intro paragraph, support ceiling, per-verdict licence table (AGREE / DIFFER / DISABLED / UNRULED + top verdicts NO_RULES / NOT_COMPARED / NO_MATCHING_MONITOR), exit map `0 OK · 1 DIFFER · 3 NO_MATCHING_MONITOR · 4 NO_RULES · 5 NOT_COMPARED` plus the SETUP code per the docstring, then the verbatim host run. Exit numbers MUST be copied from the reference docstring, not from this memo |
| Round-14 section (line 520 `### Output/colour and source-target boundaries`, 520-556) | line 3-5 of that section links `output-colour-boundaries-r14.md` | optional one-sentence cross-pointer: the rule->state join lives in the r45 entry; the protocol caveat (S050) still bars any apply/test client |
| Gate registry (`## Gate registry`, line 684; mado-verify row 693) | geometry/globals are NOT registered here (grep `mado-geometry` finds only 158, 225, 248-311) | do not register the new tool in the gate registry; mirror geometry |
| Who-owns table (`:75`) | monitor row | optional: append `(see monitor-rule route)`; held row stays |

No SKILL.md frontmatter / standing-rule change is needed (geometry added none).

## 5. PROVINCE.md tool-table row shape

- Table at lines 22-32: header `| Tool | Reads | Writes | Owner and adjacent lanes |` (22-23); rows 24-32; **line 32 = `tools/mado-geometry.py` (last row)**; line 33 blank; the round-23 correction paragraph follows. Insert the new row after line 32. Round-43 and 44 wrote no PROVINCE refinement paragraph beyond the single row (row 32 already carries `Round 44:` as inline suffix inside the Owner cell); so a row alone mirrors precedent.
- Cell shape (geometry row, line 32):
  1. `` `tools/mado-monitors.py` ``
  2. Reads: the bytes of the caller-supplied config files (cap, regular files only; missing/unreadable/directory/FIFO refused as setup error) and one caller-supplied `hyprctl monitors all -j` dump (regular file or `-`, size cap, UTF-8 JSON list of objects) ; `no compositor socket, no Wayland client, no network, no config tree, no process started` - the latter is mandated by clause r of the frozen counter (no hyprctl/journalctl/wlr-randr/wayland-info run). Fill the caps from the reference docstring.
  3. Writes: `nothing — stdout only (` the tool's MADO_ line prefixes `)`; `--selftest` writes nothing and opens only the fixed paths it lists (geometry: `/nonexistent/none`, `/`, `/dev/null`).
  4. Owner: `mado, round 45 (a read-only join of a declared \`monitor =\` rule against the output the compositor prints; never reads the compositor itself — the caller supplies the dump — AGREE says nothing about rendered output, panel timing, hotplug or which file's rule won; the operator applies any rule change)`; cite the live-run finding path once, as geometry cites `SentLiveRun/findings.md F3`.
- The lane's `hyprctl` whitelist (PROVINCE.md:28 mado-verify row; `SKILL.md:326` read-verb whitelist) lists `monitors`; `monitors all -j` is permitted by the round-45 task text, but the whitelist wording at `SKILL.md:326` says only `monitors` - flag for the L1 whether to add `monitors all` there (append-only note).

## 6. What the counters do and do not read (separability)

- C2 clause f reads README only for the one entry row. C2 reads the entry, `corpus/SOURCES.md`, the lesson, README and pins. SKILL.md, PROVINCE.md and the Frontier are **not read by either counter**; they are paperwork for the L1's data commit, scoreless but part of the registration's coverage + operability story (axes: coverage = frontier move, operability = tool + SKILL routing).
- Frontier edits are therefore free of counter risk; the one trap is README clause f (exactly one column-0 row with the prefix, fenced blocks removed).

## 7. Gaps / unknowns

- I did not read `l1-draft/entry.md` body or the reference docstring beyond what the pointer cites; exit-code numbers and CLI flag names for the SKILL rows must be lifted from the docstring, not from the registration's `NO_RULES 4 | NOT_COMPARED 5 | DIFFER 1 | NO_MATCHING_MONITOR 3 | OK 0` shorthand alone (that shorthand does match the geometry exit pattern: 3 = no match, 4 = no rules, 5 = not compared).
- `SKILL.md:326` whitelist text not read past the first line; `monitors all` extension is a decision for the L1.
- Commands used: `grep -n -E '^#{1,3} ' SKILL.md`; `sed -n` ranges on README.md 1-320, SKILL.md 140-325 and 520-556, PROVINCE.md 1-97; `git log --oneline -1` = `ebdba13f`. No host command run.
