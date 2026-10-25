# ScrSkillProvince — round 41, w1 (report)

Status: **complete**. Drafts written; SKILL.md and PROVINCE.md untouched (frozen, L1 integrates).

## Behavior (what was produced)

Two deliverables, both in my seat directory, each carrying the verbatim row/paragraph text plus
the exact insertion anchor (file, section heading, neighbouring line numbers at HEAD
`cd950ec781149040cc73d71cd67c2b67452e7724`):

1. `.ufo/waves/round-41/w1/ScrSkillProvince/skill-rows.md`
   - **Anchor A — probe-table row.** `SKILL.md` `### Read-only probes` (heading line 202; header
     204, separator 205, last row 221 = `grim -t ppm -`). Insert after **221**, before blank 222
     and `### Mutating commands` (223). New row → line 222.
   - **Anchor B — decision-table row.** `SKILL.md` `### Claim-first routing` (heading 142; header
     144, separator 145, last row 156 = `Bar runtime facts`). Insert after **156**, before blank
     157 and `### Divergence vocabulary` (158). New row → line 157.
   - Both rows carry: the command, what is read (the portal journal, not a socket), the full exit
     map (0 OK · 1 MISSING_EXPECTED · 3 NO_SESSIONS · 2 SETUP usage/unreadable/too_large/bad_expect
     · 5 SETUP journalctl_unusable/journalctl_failed/journalctl_too_large), and real sample output.
   - Section header "all executed 2026-10-14 unless cited" needs no edit: my row is cited
     (round-41), the same way the `hyprctl layers` and `grim` rows are.
2. `.ufo/waves/round-41/w1/ScrSkillProvince/province-row.md`
   - **Anchor C — tool-inventory row.** `PROVINCE.md` table header 22, separator 23, rows 24-30
     (last = `tools/mado-anims.py`, line 30), blank 31, round-23 correction paragraph 32. Insert
     after **30** (new line 31). Row states reads (journal file ≤ 8 MiB, or the stdout of exactly
     one allowlisted program with fixed argv / `/dev/null` stdin / 4-var env), writes (stdout only;
     selftest inside a private temp dir), and the owner/adjacency line.
   - **Anchor D — scope-check paragraph.** New `## Round-41 addendum — advertised Wayland globals
     and focus-grab clients (append-only)` appended after line **95** (PROVINCE.md is 95 lines;
     Round-38 addendum opens at 84). Append-only keeps every existing line number, matching
     `6068feb` (round-38 addendum).
   - Scope check, stated with anchors: **in province** = (1) the advertised set as the portal
     logged it (`xdph-PortalManager.cpp:85` `CPortalManager::onGlobal`, log at `:88`;
     `xdph-journal.txt:117`), (2) Hyprland's own protocols at a pinned revision
     (`protocols-README.md:17`, `Hyprland-FocusGrab.hpp:59`, `focus-grab-v1.xml:39,60,121`),
     (3) the rule-level counterpart is already owned (`keybind-rule-semantics.md:225,229,232`;
     PROVINCE.md:6-12). **Adjacency, report never absorb** = a client's grab lifecycle
     (`quickshell-grab.cpp:78,98`), security/bug-tracker literature (`issue-565.html` title), and
     the *exercise* of privileged capabilities. **Out** = the localized-documentation channel
     (PROVINCE.md:73-76; `PRED-C2-r41-v1` clause i forbids `amgsk.dev`/`zhihu`/`/zh`/`/ja`).

## Gates (what I actually ran — nothing else is claimed)

| Gate | Command | Result |
|---|---|---|
| Reference on the committed journal | `python3 .ufo/waves/round-41/c1/ctl-ref-tool.py.txt --journal-file .ufo/waves/round-41/fetch/xdph-journal.txt` | rc 0, stderr empty, 66 lines; receipt `ref-run-journal.txt` sha256 `dda94374…` |
| Reference `--diff` | same + `--diff` | rc 0, 67 lines; `added` 63 / `removed` 8 / `ver_changed` `-`; receipt `ref-run-diff.txt` sha256 `3b3637a4…` |
| `--expect` present | `--expect hyprland_focus_grab_manager_v1` | rc 0, `expected_missing=- verdict=OK` |
| `--expect` absent | `--expect zwlr_screencopy_manager_v2` | rc 1, `expected_missing=zwlr_screencopy_manager_v2 verdict=MISSING_EXPECTED` |
| Reference `--selftest` | `--selftest` | rc 0, `MADO_GLOBALS_SELFTEST: 47/47 passed` (contract floor `n >= 25`) |
| Deliverable absence | `git cat-file -e HEAD:tools/mado-globals.py` | rc 128, `fatal: path 'tools/mado-globals.py' does not exist in 'HEAD'` |
| Journal pin | `sha256sum`, `wc -l` on `fetch/xdph-journal.txt` | `bf8fa91a…`, 153 lines |
| Reference passes the counter | read `.ufo/waves/round-41/receipts/ctl-c1.txt:1` | `control=P-reference expect=MET got=MET correct=1` … `fixtures=24/24 tool=present verdict=TARGET_MET` |
| Quote verifier (mine) | `python3 .ufo/waves/round-41/w1/ScrSkillProvince/verify-quotes.py` | **`QUOTE_CHECK: items=25 failed=0`**, exit 0 → `quote-check.txt` |
| Row well-formedness | cell-count split on unescaped `\|` | probe row 3 cells, decision row 4 cells, province rows 3 cells each |

The quote verifier greps each lifted string at its named source line **and** in the draft that
presents it (whitespace-normalised, markdown `\|` un-escaped), and enforces the ≤ 25-word limit.
Not run, therefore not claimed: `PRED-C1-r41-v1`, `PRED-C2-r41-v1`, `ctl/run-c1-controls.py`,
`ctl/run-c2-controls.py`, any build/lint, the deliverable tool itself (it does not exist).

## Touched surfaces

- Written (my seat only): `.ufo/waves/round-41/w1/ScrSkillProvince/{skill-rows.md,
  province-row.md, verify-quotes.py, ref-run-journal.txt, ref-run-diff.txt, ref-selftest.txt,
  git-absent-head.txt, quote-check.txt}` and this report `.ufo/waves/round-41/w1/ScrSkillProvince.md`.
- Read-only: `SKILL.md`, `PROVINCE.md`, `quality/counters/c1-r41-globals.py:1-120`,
  `quality/counters/c2-r41-focus-entry.py:1-80`, `receipts/ctl-c1.txt`, `receipts/ctl-c2.txt`,
  `registration.md`, the `fetch/` receipts, `corpus/knowledge/keybind-rule-semantics.md`,
  `git ls-tree/cat-file/rev-parse/log` (read-only).
- Not touched: SKILL.md, PROVINCE.md, the counters, the controls, the reference, `registration.md`,
  `fetch/`, the jj/git index, the fleet repo, the shokuknow checkout, host config trees.
  No git/jj mutation, no pacman, no compositor/socket/Wayland client, no journal verb other than
  the allowed read-only form (and only via the reference's fixed argv).
- Tooling installed: **none** (no tool was needed).

## Findings (each names what it attacks or supports)

1. **PROVINCE.md's tool inventory is stale — supports a decision on where the new row goes.**
   `PROVINCE.md:32` claims the table "covers every tracked file under `tools/`", but rows 24-30
   are 7 while `git ls-tree --name-only HEAD tools/` returns 10: `mado-eventq.py`,
   `mado-options.py`, `mado-wsrules.py` are tracked and unlisted. Appending `mado-globals.py` as
   "row 8 of 7" would repeat the defect; the draft offers the addendum (Anchor D) as the
   alternative and asks the L1 to disclose whichever it picks.
2. **The portal log site is line 85, not 86 — corrected in my own draft; a caution for C2 seats.**
   `xdph-PortalManager.cpp:85` is `void CPortalManager::onGlobal(...)`, `:86` is
   `const std::string INTERFACE = interface;`, `:88` is the `Debug::log` call. My first draft
   cited `:86` for the signature; the verifier caught it (`src=NO`) and every reference is now
   `:85`. Any entry that cites "onGlobal at :86" is off by one.
3. **The 30-second timeout is the reference's choice, not the contract's — constrains the row
   wording.** The docstring fixes the argv, stdin, env, 8 MiB caps and the failure classes, but
   only says "a timeout is `SETUP journalctl_failed`"; `timeout=30` appears at
   `ctl-ref-tool.py.txt:182` and no fixture exercises it (declared residual: "a hang (`--live`
   timeout) is not exercised"). My row therefore says "a bounded timeout", not "30 s" — otherwise
   the SKILL row would state a bound the counter does not enforce.
4. **The `--diff` line is 1902 bytes — a table cell cannot carry it.** My draft carries the real
   `removed`/`ver_changed` fields, the first two and last added names, and an explicit
   `<61 more names>` elision marker that is labelled as my marker, not tool output. The full line
   is in `ref-run-diff.txt`.
5. **The sample is the reference's, and that is sound only because the counter is byte-exact.**
   `PRED-C1-r41-v1` compares rc and stdout byte-exactly against its model over 24 fixtures and the
   reference passes 24/24 (`ctl-c1.txt:1`), so the landed tool must reproduce these bytes. The
   draft says this explicitly and marks that the deliverable was never run (it is absent at HEAD).
6. **Scope check is consistent with the C2 predicate.** Clause i of `PRED-C2-r41-v1` forbids a
   cited location containing `amgsk.dev`, `zhihu`, `/zh`, `/ja`; the province paragraph states the
   same exclusion through PROVINCE.md:73-76, so the entry and the province file cannot drift apart
   on the localized-channel rule.
7. **Class is a name→class table, not behaviour — constrains the tag.** 38 of the 63 latest-session
   names fall to `other`; the decision row is tagged `[OBS]` for "as logged" and `[UNK]` for what
   any client does with a global, because the journal is the portal's registry view only
   (`xdph-PortalManager.cpp:85-88`), not another client's.

## Out-of-scope items (left to other seats / the L1)

- Applying the rows to SKILL.md / PROVINCE.md (frozen; L1 is the only integrator).
- Building `tools/mado-globals.py` (C1 seat) and writing
  `corpus/knowledge/hyprland-focus-grab-r41.md` (C2 seat) — the latter is still absent at HEAD
  (`ls` → no such file), so no draft here cites its contents.
- Registry rows S283+, `corpus/README.md` index row, the lesson `## Gate`, QUALITY entries.
- Repairing the stale PROVINCE tool inventory (finding 1) — reported, not repaired.

## Artifact paths

- `.ufo/waves/round-41/w1/ScrSkillProvince.md` (this report)
- `.ufo/waves/round-41/w1/ScrSkillProvince/skill-rows.md`
- `.ufo/waves/round-41/w1/ScrSkillProvince/province-row.md`
- `.ufo/waves/round-41/w1/ScrSkillProvince/verify-quotes.py`, `quote-check.txt`
- `.ufo/waves/round-41/w1/ScrSkillProvince/ref-run-journal.txt`, `ref-run-diff.txt`,
  `ref-selftest.txt`, `git-absent-head.txt`
