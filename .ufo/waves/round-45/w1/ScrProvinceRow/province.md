# Round-45 PROVINCE.md draft — the `tools/mado-monitors.py` row and the refinement note

Seat `ScrProvinceRow` (round 45, hyaku run 9, w1). **Status: draft for the L1 `MadoR45`.**
`PROVINCE.md` is not edited by this seat: `git status --porcelain -- PROVINCE.md` is empty
(`receipts/lane-clean.txt`). Read at tip `ebdba13f7cb16d454763003d424398eec3bb2788` (97 lines,
9 tool-table rows at `PROVINCE.md:24-32`); freeze `22a8dedd02f507689c567777e0f20b5e645c8ce0`.

Every locator below is computed (`grep -n`) and re-checked by `verify.py` against the receipts in
`receipts/`; the last run is `receipts/verify.txt`. Quotes are ≤ 25 words and come from the sources
this round pins.

---

## 1. The table row

**Insertion point:** as the last row of the tool table, immediately after `tools/mado-geometry.py`
(`PROVINCE.md:32`; header `PROVINCE.md:22`; row count 9 → 10, `receipts/province-anchors.txt`).

| Tool | Reads | Writes | Owner and adjacent lanes |
|---|---|---|---|
| `tools/mado-monitors.py` | the bytes of every file the caller names with `--config` (one or more, read in argument order; each opened `O_RDONLY\|O_NONBLOCK` and required to be a regular file, so a missing, unreadable, directory, FIFO or device path is `SETUP unreadable`; 1048576 B cap; UTF-8 with errors replaced) and one caller-supplied `hyprctl monitors all -j` dump (`--monitors`, the same regular-file rules, or `-` for standard input at most 1048577 bytes, UTF-8 JSON holding a list of objects); it follows no `source =` line, expands no `$NAME`, reads no environment variable and discovers no config tree, so the caller names every file the lane means to read; no compositor socket, no Wayland client, no network, no process started — the dump is captured by the caller with a whitelisted read verb | nothing — stdout only (`MADO_MON_RULE:`, `MADO_MON_OUTPUT:` and one `MADO_MONITORS:` line; stderr empty on exits 0/1/3/4/5), or on setup failure exactly one `MADO_MONITORS: SETUP <reason>` line and exit 2; the verdict codes are `OK` 0, `DIFFER` 1, `NO_MATCHING_MONITOR` 3, `NO_RULES` 4, `NOT_COMPARED` 5; `--selftest` scores 33 in-memory cases (33/33, this seat's run 2026-10-26, `receipts/tool-contract.txt`), writes no file, opens only the fixed path `/nonexistent/x` read-only (the `/nonexistent/y` config is never reached) and starts no child process | mado, round 45 (the rule-to-live-state join over the owned `~/.config/hypr` rule plane; both inputs stay caller-supplied and read-only, so the operator captures the dump and applies any change); adjacent to `tools/mado-geometry.py` (`hyprctl clients -j`) and `tools/mado-wsrules.py` (`hyprctl workspacerules -j`) in the same config-to-live family, and to tsukuroi only for the compositor and hyprutils package versions that fix the parser — not for the rule plane |

**Conditional, stated plainly.** The tool is absent at BASE (`git ls-tree <base> -- tools/mado-monitors.py`
is empty) and absent at this seat's tip; the row becomes true only when C1 lands the tool at
`tools/mado-monitors.py` at the round-45 data commit. If C1 misses, omit the row and record the miss —
the counter's kill rule, not this draft, decides. If the landed tool's docstring differs from the
reference contract (`.ufo/waves/round-45/l1-draft/mado-monitors.py`), the row must be re-read against the
landed docstring before it is kept: the cells above describe the reference at the freeze, not the landing.

## 2. The refinement note (append at the end of `PROVINCE.md`, after line 97)

Integration: paste the paragraphs below into `PROVINCE.md` unquoted, at the end of the file. Recompute the one
`mado-monitors.py:15` locator if the landed docstring differs from the reference; if the L1 lands the gate at a
tracked `quality/` path, swap the three `check-session-material.py:<n>` locators for that path (the lines are the
same file, so re-run the `grep -n` before keeping the numbers).


**Round-45 refinement (append-only; one tool row and three record instruments; no new desktop surface):**
`tools/mado-monitors.py` joins the owned monitor-rule plane with one captured dump: it reads only the
files the caller names (`--config`) and one `hyprctl monitors all -j` dump (`--monitors`, or `-`), so it
connects no socket and starts no process, the operator captures the dump with a whitelisted read verb and
applies any change. The tool is "a join, not a blame"
(`.ufo/waves/round-45/l1-draft/mado-monitors.py:15`) — a runtime `hyprctl keyword monitor`, a
wlr-output-management client or a mode the output does not offer can move live state with no config byte
changing, and a `desc:` selector that matches only the dump's short description is reported unmatched.

The two round-45 counters are record instruments, named here for the same reason the round-23 refinement
names the `tools/` instruments — the province accounts for every tracked instrument it runs, and neither
touches a config plane, the compositor or a host service. `quality/counters/c1-r45-monitors.py`
(`PRED-C1-r45`) reads git objects at `--repo`/`--rev` with ambient `GIT_*` removed, extracts the tool blob
and runs it as a child process: its `--selftest` (60 s cap) and 49 seeded fixtures (10 s cap each), in
fresh directories under `--work` with environment exactly {PATH, LANG=C.UTF-8, HOME,
HYPRLAND_INSTANCE_SIGNATURE} and a PATH holding four marker-writing decoys — `hyprctl`, `journalctl`,
`wlr-randr`, `wayland-info` — that must never run (clause r). It writes only beneath the `--work`
directory it creates with `tempfile.mkdtemp` and removes on exit, and its default seed is 45.
`quality/counters/c2-r45-monitor-entry.py` (`PRED-C2-r45`) reads git objects at the revision of the entry,
`corpus/SOURCES.md`, `corpus/lessons/round-45.md`, `corpus/README.md` and the nine pinned files under
`.ufo/waves/round-45/fetch/`, recomputes sha256 and locator lines, and writes nothing; it demands the
census line `hyprland monitor-rule default_refresh=60 refresh_tolerance=1 scale_step=1/120 scale_search=89
json_refresh_decimals=5 line_keys=8` and binds seventeen surfaces to locators no wider than 30 lines.

**Conditional — the receipt privacy gate.** The w1 seat `ExecPrivacyGate` drafted
`.ufo/waves/round-45/w1/ExecPrivacyGate/check-session-material.py` (sha256
`9abd5d548683a7699a2ffb48f2e8ab660c413464db797c4042f62baeea0fbd33`, untracked at `ebdba13f`) toward
considerthese `2026-10-26.md` proposal 1 and round-44 closure D1: it reads every `.ufo/` file tracked at a
revision straight from the object database (`git ls-tree -r` plus `git cat-file --batch`; "the working tree
is never touched", `check-session-material.py:11`), scores four rules (client dumps with a non-empty
`title`/`initialTitle`, `ss` process-table rows, a monitor `serial` beside a description/make/model, and
home-path listings over `--home-limit`), and prints one `SESSION_MATERIAL: files=<n> findings=<n>
rev=<hash>` line with per-(file, rule) findings that carry "counts only — never a title, a program name, a
serial, a description or a home" (`check-session-material.py:51`), so its own receipt is safe to commit. It
writes nothing (its `--selftest` "builds positive and negative fixtures in a throwaway git"
repository under `$TMPDIR`, `check-session-material.py:46`). If the L1 lands it at a tracked `quality/`
path at the data commit, it belongs here as a record instrument that scores the lane's own receipts against
`SKILL.md:343` rule 4 ("Session material stays shape-only."), and reads no compositor, config plane or host
service. If it does not land, drop this paragraph: the province names tracked instruments only.

The round-45 entry `corpus/knowledge/hyprland-monitor-rule-r45.md` lands with the data commit as
source-read knowledge of the owned rule plane, on the round-38 addendum's pattern: nine pinned upstream
files are read as bytes and nothing is connected, dispatched or re-read from the host, so the entry adds no
write surface and no runtime capability.

**Declared limits.** A tool holding a model of the contract is an implementation of it
(`c1-r45-monitors.py:36`): the fixtures are the contract's cases, not Hyprland's runtime. The C1 read-only
clause sees PATH lookups only, so a tool that opened a socket directly would not be caught by it. No
round-45 counter reads the host: the dump in every fixture is synthesised, and C2's trust root is the nine
pins.

## 3. A coverage claim this draft does not silently repair

`PROVINCE.md:34` claims, in its own words, that "the inventory above covers every tracked file under" — the
scope claim the round-23 wave-2 correction makes. At `ebdba13f` three tracked tools have no row: `tools/mado-eventq.py`,
`tools/mado-options.py`, `tools/mado-wsrules.py` (`tools/` holds 12 files, the table 9 rows,
`receipts/province-anchors.txt`). That is a finding about the file, not part of this seat's scope. The L1
decides between adding the three rows and rewording the claim; the round-45 row above is correct either way,
and nothing in this draft changes the round-23 coverage sentence's meaning.

## 4. Quotes and locators

| quote (≤ 25 words) | source locator | receipt |
|---|---|---|
| a join, not a blame | `.ufo/waves/round-45/l1-draft/mado-monitors.py:15` | `receipts/quotes.txt` |
| It reads files and standard input only; it starts no process and opens no socket. | `.ufo/waves/round-45/l1-draft/mado-monitors.py:22` | `receipts/quotes.txt` |
| two-token form only; anything else is usage | `.ufo/waves/round-45/l1-draft/mado-monitors.py:24` | `receipts/quotes.txt` |
| MAX_BYTES = 1048576 | `.ufo/waves/round-45/l1-draft/mado-monitors.py:98` | `receipts/quotes.txt` |
| nothing in the lane is written; scratch only under | `quality/counters/c1-r45-monitors.py:5` | `receipts/quotes.txt` |
| read-only: PATH starts with a directory holding executables | `quality/counters/c1-r45-monitors.py:19` | `receipts/quotes.txt` |
| a tool holding a model of the contract is an implementation of it | `quality/counters/c1-r45-monitors.py:36` | `receipts/quotes.txt` |
| revision-addressed git reads, ambient GIT_* removed; nothing in the lane is | `quality/counters/c2-r45-monitor-entry.py:10` | `receipts/quotes.txt` |
| The seventeen surfaces: parseMode, parsePosition, parseScale (Parser.cpp); handleMonitor | `quality/counters/c2-r45-monitor-entry.py:54` | `receipts/quotes.txt` |
| hyprland monitor-rule default_refresh=60 refresh_tolerance=1 scale_step=1/120 scale_search=89 json_refresh_decimals=5 line_keys=8 | `.ufo/waves/round-45/l1-draft/entry.md:72` | `receipts/quotes.txt` |
| the working tree is never touched | `.ufo/waves/round-45/w1/ExecPrivacyGate/check-session-material.py:11` | `receipts/quotes.txt` |
| builds positive and negative fixtures in a throwaway git | `.ufo/waves/round-45/w1/ExecPrivacyGate/check-session-material.py:46` | `receipts/quotes.txt` |
| counts only — never a title, a program name, a serial, a description or a home | `.ufo/waves/round-45/w1/ExecPrivacyGate/check-session-material.py:51` | `receipts/quotes.txt` |
| the inventory above covers every tracked file under | `PROVINCE.md:34` | `receipts/quotes.txt` |
| the lane's own analysis instruments are named here so the province accounts for every tracked tool it runs | `PROVINCE.md:20` | `receipts/quotes.txt` |
| Session material stays shape-only. | `SKILL.md:343` | `receipts/quotes.txt` |

## 5. What this draft does not claim

- It does not claim the tool is installed, that C1 is TARGET_MET, or that any counter has been run by this
  seat beyond the reference tool's own in-memory `--selftest` (33/33) and the counts computed from the
  frozen counter modules (`49` fixtures, `17` surfaces, `9` pins) — `receipts/counters.txt`.
- It does not claim the privacy gate works: no selftest of the gate was run here, and the gate is
  untracked. Its paragraph is conditional for that reason.
- It does not name any host-session value: no window title, monitor serial, description, process row or
  home-directory listing appears in the row, the note or the receipts — `verify.py` tests this file for an
  absolute home-directory path, a socket-table row and a serial assignment, and refuses it (`receipts/verify.txt`).
