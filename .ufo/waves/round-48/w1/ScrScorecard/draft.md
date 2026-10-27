# Round 48 — SCORECARD section draft, README index row, README Frontier bullet

Seat `ScrScorecard` (round 48, wave `w1` BUILD). Base `579f694b45c797a9c39761fdb4f9e0a1b71b3585`.
Nothing here is scored and nothing outside this seat dir is edited; the L1 integrates.

The three copy blocks below are the deliverable. `<UPPERCASE>` tokens are placeholders: each one is routed in
§4 (fill map) to the artifact that owns the number, and §5 lists the invariants a block must satisfy before it is
committed. Placeholders were used only where the value is produced by another seat or by the post-w1 base/after
run; every fact about the *base* tree is measured, in §1.

---

## 1. Anchors measured while drafting (read-only, at `579f694`)

| Fact | Command | Result |
|---|---|---|
| the C1 "before" tool is the round-47 tool | `python3 -I tools/mado-terminal.py --selftest` | `MADO_TERMINAL_SELFTEST: 43/43 passed`, exit 0 |
| registry size / top row at base | `grep -c '^\| S[0-9]' corpus/SOURCES.md` | `276`, tops at `S339` |
| the C2 entry is new | `git cat-file -e 579f694:corpus/knowledge/xkb-keymap-compile-r48.md` → rc `128`; `git grep -q xkb-keymap-compile 579f694 -- corpus/` → rc `1` | absent at base (the C2 counter's precondition) |
| the C1 counter is new | `git cat-file -e 579f694:quality/counters/c1-r48-terminal-cache.py` | rc `128` |
| the base open-ground lines this round answers | `git grep -n 'warm-cache path' 579f694 -- corpus/README.md` | `:110` (round-47 bullet, "Still open: … the warm-cache path …") |
| | `git grep -n 'XKB compile itself' 579f694 -- corpus/knowledge/hyprland-input-devices-r46.md` | `:69` (round-46 Limits) |
| the cache paragraph this round replaces | `grep -n 'Cache (out of contract)' tools/mado-terminal.py` | `:82` (paragraph `:82-85`) |
| duplicate-URL census at base | `awk '$2=="W04"' .ufo/waves/round-48/receipts/census-before.txt \| wc -l` | `17` |
| no assimilation theme exists | `ls merge` | `ls: cannot access 'merge': No such file or directory` |
| Frontier bullets are prepend-only | `git diff -U1 1001bda 0c699605 -- corpus/README.md` | one `+` index row, one `+` bullet, one `+` blank line, zero `-` content lines |
| the axis publication parser's tokens | `sed -n '60,68p' quality/check-axis-scores.py` | `navigation (\d+)/(\d+)`, `calibration resolved-active (\d+)/(\d+)`, `operability selftest (\d+)/(\d+)` |

---

## 2. SCORECARD.md — Round 48 section (insert after the Round-47 `### Planned (round 48; intent only)` block, i.e. after `SCORECARD.md:2697`)

<!-- BEGIN SCORECARD BLOCK -->

## Round 48 - mado-terminal warm cache and the XKB keymap entry (2026-10-26, attempt 1)

Claims declared at `579f694b45c797a9c39761fdb4f9e0a1b71b3585` (`.ufo/waves/round-48/claims.md`) before wave `w1` (`<W1-SEATS>` build seats); registration `.ufo/waves/round-48/registration.md` frozen at `<REG-SHA>` (base `579f694b`) after w1 and before wave `w2` (`<W2-SEATS>` falsify seats) and any data; no re-registration. Data commit `<DATA-SHA>`. Lowest-axis rule: every published axis tied at its maximum at base (`receipts/axis-base.txt`; the round-47 tip receipt `receipts/axis-tip.txt` reads `checked=3 mismatched=0`, and the base run must reproduce it, not be assumed), so no single axis was lowest; the trend furthest behind was **quality** (round-47 closure ruled it `unprovable-but-better` while every other trend was `improved`), so C1 is a quality-trend operability move and the routed round-47 defects D1-D4, R3 and R4b are worked as non-claim items.

| Claim / axis | Before -> after | Counting command | Self-verdict |
|---|---|---|---|
| C1 **operability** (capability acquisition) - `tools/mado-terminal.py` | `<C1-BEFORE-LINE>` exit `<C1-BEFORE-RC>` at base (`receipts/c1-before-base.txt`) -> `<C1-AFTER-LINE>` exit `<C1-AFTER-RC>` at `<DATA-SHA>` (`receipts/c1-after-data.txt`) | `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r48-terminal-cache.py --repo . --rev <rev> --work <scratch>` (`PRED-C1-r48`; judge = the real pinned xdg-terminal-exec v0.14.3, primed per case with a cold `--print-cmd` run and waited on, then re-run warm; the round-47 cold clause re-runs unchanged on `quality/counters/c1-r47-fixtures.json` as harm watch; controls `receipts/ctl-c1.txt` PASS wrong 0 of `<CTL-C1-N>`) | `<C1-VERDICT>` |
| C2 **coverage** (sourced) - `corpus/knowledge/xkb-keymap-compile-r48.md` | `admitted=0/1` exit 1 at base (`receipts/c2-before-base.txt`) -> `admitted=1/1 verdict=TARGET_MET` exit 0 at `<DATA-SHA>` (`receipts/c2-after-data.txt`) | `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r48-xkb-entry.py --repo . --rev <rev>` (`PRED-C2-r48`; controls `receipts/ctl-c2/` POS admitted, `<CTL-C2-N>` rejected; the entry's live receipt is `<XKB-LIVE-RECEIPT>`, carrying `<NEG>` negative probes) | `<C2-VERDICT>` |

Separable: `<SEP-POINTER>` (tool-only tree: C1 MET, C2 `0/1`; entry-only tree: C1 MISSED, C2 `1/1`).

### Capabilities (round 48)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| terminal selection versus the resolver, warm cache | answer what `xdg-terminal-exec` 0.14.3 selects when the cache file it wrote earlier is still trusted: parse `$XDG_CACHE_HOME/xdg-terminal-exec` (default `$HOME/.cache`, `:1179`; at most 49 lines, line 11+ until the `END_OF_EXEC_USEP` terminator, `:217-298`), recompute the `gen_hash` md5 over `XDG_CURRENT_DESKTOP` and a byte-exact `LC_ALL=C LANG=C ls -LRl` emulation of the colon-split `XTE__CONFIGS:XTE__APPLICATIONS_DIRS` operands (`:179-215`), accept the cache only when that digest equals line 1 and `command -v <line 2>` succeeds, honour `/disable_cache` and `XTE_CACHE_ENABLED`, and report `cache=<absent\|hit\|stale\|invalid\|disabled>` in its `MADO_TERM` line; `print` reproduces the resolver's stdout and exit status warm as well as cold, `explain --observed` compares a captured run, `cmd=` is compared, HOME unset is modelled as the pin (exit 1, empty stdout); starts no process, opens no socket, writes nothing (it never saves the cache the resolver would save) | `tools/mado-terminal.py` (selftest `<SELFTEST>`); `quality/counters/c1-r48-terminal-cache.py` `<C1-AFTER-LINE>` at `<DATA-SHA>`; live host run `<LIVE-RECEIPT>`; round-47 cold clause `<C1-COLD-CLAUSE>` on `quality/counters/c1-r47-fixtures.json` | 48 |
One row by the section's own rule: `SCORECARD.md:209` admits a capability row only for a capability demonstrated
*running*, which is the C1 instrument. The C2 entry is a sourced knowledge entry and enters through the README index
row (§3.1) instead — every round-40..47 section carries exactly one capability row (counted).

### Sources, saturation, planned

Sources 276 -> `<ROWS>` rows (S340-S`<TOP>` for the entry, tier `<TIERS>`, `mined`, opened 2026-10-26; `<DUP-ROWS>` repeat held URLs under new scopes and `<REJ-ROWS>` candidates were rejected with reasons: census W04 17 -> `<W04-AFTER>`). Knowledge entries 64 -> 65. Assimilation: none (no `merge/` theme in the tree; id guard `<IDGUARD>`; `<QUAR>` quarantined rows untouched). considerthese `2026-10-26.md` proposal `<CT-PROP>` -> `<CT-LANDING>` (QUALITY `<CT-CRIT>`). Mistakes M48-1..`<M48-M>`; QUALITY `<Q-LO>`-`<Q-HI>` (base tops at 95). Round-47 closure: D1 (`w1/ExecHomeUnset/`, contract text at `tools/mado-terminal.py:82-85` plus the lesson line and HOME unset in C1's contract: `<D1>`), D2 (`w1/ExecD2Receipt/`, an unreceipted session-material number re-derived at a named revision: `<D2>`), D3 (`w1/ExecFixturesV2/`, readdir-order cases in schema v2: `<D3>`), D4 (erratum below), R3 (`w1/ExecSessionMarker/`, synthetic-material marker installed and shown able to fail both ways: `<R3>`), R4b (`w1/ExecErrataR45/` H1, round-45 errata in a form that keeps the frozen round-45 counter's verdict: `<R4B>`), M47-10 (schema v2 H1/H2 non-regular paths and option-like `Exec`/`TryExec` words: `<H12>`), `w2/CritC1Explain.md` (`explain` `cmd=` compared: `<XM>`), `w2/SentC1Sandbox.md` F1-F4 (counter wording: `<F14>`). Saturation 9.0 / N=3 unchanged; retired: none.

Axis table re-derived at `<DATA-SHA>` (`receipts/axis-data.txt`): navigation `<NAV>`; calibration resolved-active `<CAL>`; operability selftest `<OPS>`.

### Errata (round 48) — round-47 closure D4: `xdg-terminal-selection-r47.md` Limits locator off by one (append-only; nothing above is rewritten; line text owned by `w1/ScrErrataD4/erratum.md`)

E1 (D4) `corpus/knowledge/xdg-terminal-selection-r47.md:95` cites `terminal-route-r17.md:150-151` for the `--dir=` sentence, which begins at `:149` and ends at `:150`: read `terminal-route-r17.md:149-150`; the entry's text is correct, the locator is one line low (the erratum is a locator correction, so it cannot move the frozen round-47 C2 verdict).

### Planned (round 49; intent only)

1. The cache half the tool still refuses: the save itself (`:1455-1458`, `save_cache "$1" &` at `:1457`), a real hotkey launch, `uwsm-app`'s environment and the selected terminal's own argument handling (the open list at `corpus/README.md:110`).
2. The per-device keymap half: `kb_file`, overridden keymaps, the error overlay's text and the per-device settings the dump never prints (the open list at `corpus/README.md:112`, `corpus/knowledge/hyprland-input-devices-r46.md:69-73`).
3. w2's findings against the frozen round-48 instruments (schema v2 predicate gaps, `explain` field coverage) as routed defects with their own receipts.

<!-- END SCORECARD BLOCK -->

**Note for the L1 (not part of the block):** the capability row lists the behaviour as `claims.md` shapes it. Before
commit, each technical clause must be re-read against its owning artifact — the C1 row's script line ranges against
`w1/ScrCacheDoc/docstring.md`'s computed ranges and the counter's clauses. The tool is the admitted object; this row is
its summary, so a clause that does not reconcile is dropped, not softened.

---

## 3. corpus/README.md — index row and Frontier bullet

### 3.1 Index row — insert as the last row of the Coverage map table (`corpus/README.md:75`, after the round-47 row, before the blank line at `:76`)

<!-- BEGIN README ROW -->

| `knowledge/xkb-keymap-compile-r48.md` (MADO-R48-1, round 48; input plane, the XKB compile) | Which `kb_rules`/`kb_model`/`kb_layout`/`kb_variant`/`kb_options` names compile into a keymap on this host (libxkbcommon 1.13.2, xkeyboard-config 2.48): the RMLVO-to-KcCGST component route through the rules file, the include-path order (`$XDG_CONFIG_HOME/xkb`, `$HOME/.xkb`, `/etc/xkb`, then the xkeyboard-config root), the names that fail the compile (unknown layout, unknown variant, unknown rules: exit 1) against the names dropped with a warning (unknown option: rc 0, diagnostic `XKB-595`; unknown model: rc 0), multi-layout variant alignment, and how a failed compile reaches Hyprland 0.56.2's `us` fallback (held rows S318/S319, not re-claimed); a live read-only `xkbcli compile-keymap` receipt for the host's names (`layout=br`, `options=compose:caps`) | S340-S`<TOP>` (opened 2026-10-26); S318/S319 held |

<!-- END README ROW -->

### 3.2 Frontier bullet — insert as the first bullet under `## Frontier` (`corpus/README.md:108`), above the round-47 bullet at `:110`

<!-- BEGIN README BULLET -->

- Round 48 moves two open halves onto executed ground: the warm-cache half of the P4 terminal-selection route ([terminal selection](knowledge/xdg-terminal-selection-r47.md)) — what `xdg-terminal-exec` 0.14.3 selects when the cache it wrote earlier is still trusted (the `gen_hash` md5 over `XDG_CURRENT_DESKTOP` and `ls -LRl`, the line-2 `command -v` gate, `/disable_cache`, `XTE_CACHE_ENABLED`), judged by the real primed script, with a read-only resolver (`tools/mado-terminal.py print|explain`) that starts no process and writes nothing — and the XKB compile ([keymap compile](knowledge/xkb-keymap-compile-r48.md), rows S340-S`<TOP>`): which `kb_*` names compile, fail or warn under libxkbcommon 1.13.2 / xkeyboard-config 2.48, and how that reaches Hyprland's `us` fallback (held S318/S319). Still open: whether a terminal process actually starts under the hotkey (launch half of the round-17 `[UNK]`), the cache the resolver saves, `uwsm-app`'s environment, the selected terminal's own argument handling, the per-device `kb_file` keymap, the error overlay's text, and the per-device settings the dump never prints.

<!-- END README BULLET -->

**Note for the L1 (not part of the blocks):** the index row's "Holds" cell summarises the entry, so every clause in it
(the include-path order, the fail-versus-warn split, the variant alignment, the `us` fallback join) must reconcile with
the entry's own numbered steps and locators; a clause the entry does not land is dropped from the cell rather than
softened. The row's Sources cell is `S340-S<TOP> (opened 2026-10-26); S318/S319 held`, the round-47 idiom at
`corpus/README.md:75`. The bullet is prepend-only: do not rewrite `:110`/`:112`, whose "Still open" lists this round
answers (measured in §1).

---

## 4. Fill map — every placeholder, its owner, and the substitution rule

| Token | Substituted from | Rule |
|---|---|---|
| `<W1-SEATS>`, `<W2-SEATS>` | `python3 -c 'import json;print(len(json.load(open(".ufo/waves/round-48/w1-spec.json"))["items"]))'` for w1; the w2 spec for w2 | w1 is `41` at draft time; re-derive at the freeze, do not transcribe |
| `<REG-SHA>`, `<DATA-SHA>` | the freeze commit and the data commit | full 40-hex, never a shortened suffix that is not a true suffix |
| `<C1-BEFORE-LINE>`, `<C1-BEFORE-RC>` | `receipts/c1-before-base.txt`, the counter's own last line at base | verbatim from `PRED-C1-r48: cold=… warm=… explained=… generated=… selftest=… readonly=… tool=… verdict=…`; the counter is owned by `w1/ExecCounterC1/` |
| `<C1-AFTER-LINE>`, `<C1-AFTER-RC>` | `receipts/c1-after-data.txt` | same line, same field order; `verdict=TARGET_MET` only if every clause met |
| `<C1-VERDICT>`, `<C2-VERDICT>` | the after receipts | `**TARGET_MET**` / `**TARGET_MISSED**`; no partial credit |
| `<CTL-C1-N>`, `<CTL-C2-N>` | `receipts/ctl-c1.txt`, `receipts/ctl-c2/` | the control battery's own pass/fail counts; a control that cannot fail is not a control |
| `<SEP-POINTER>` | the separability seat's report (`w1/ConnClaims`, `w1/ConnSiblings`, or the w2 equivalent) | must name one artifact; without it the two verdicts are not shown separable |
| `<SELFTEST>` | `python3 -I tools/mado-terminal.py --selftest` at `<DATA-SHA>` | base reads `43/43` (measured, §1); the extended tool's count is the landed one |
| `<C1-COLD-CLAUSE>` | the counter's cold-clause cell in `receipts/c1-after-data.txt` | the round-47 fixture file is reused unchanged; state the fraction, not "unchanged" |
| `<LIVE-RECEIPT>` | the committed live host run for the cache path | a cached-resolver capture, never a launch; shape-only (no titles, no device names) |
| `<XKB-LIVE-RECEIPT>` | the committed `xkbcli compile-keymap` receipt (`w1/ExecXkbLive/`) | must name `xkbcli`/libxkbcommon version, RMLVO names, rc, keymap sha256, and the `<NEG>` negative probes |
| `<NEG>` | the same receipt | count of negative probes whose rc the entry states (unknown layout 1, unknown variant 1, unknown option 0 + warning; the entry's own list) |
| `<ROWS>`, `<TOP>` | `w1/ScrRows/rows.md` | `276 + N` and `S(339+N)`; the row ids must be contiguous from S340 and match the registry after merge |
| `<TIERS>` | `w1/ScrRows/rows.md` | per-row tier list in the round-47 idiom ("tier A except S3xx tier B") |
| `<DUP-ROWS>`, `<REJ-ROWS>`, `<W04-AFTER>` | `w1/ScrRows/rows.md` + `receipts/census-before.txt` (17 W04 rows at base, §1) | duplicates named by id, rejections named by candidate, never "some" |
| `<IDGUARD>`, `<QUAR>` | `w1/ExecIdGuard/` | the guard's own counts |
| `<CT-PROP>`, `<CT-LANDING>`, `<CT-CRIT>` | `w1/ScrConsider/draft.md` | proposal number as in `considerthese/2026-10-26.md`; a refused proposal is recorded as refused |
| `<M48-M>`, `<Q-LO>`, `<Q-HI>` | `w1/ScrMistakes/mistakes.md`, `corpus/QUALITY.md` | ranges start at M48-1 and at criterion 96 (base tops at 95) |
| `<D1>` `<D2>` `<D3>` `<R3>` `<R4B>` (round-47 closure slots; `<D4>` is the errata line above, not a slot) | the owning seat's report: `w1/ExecHomeUnset/` (D1), `w1/ExecD2Receipt/` (D2), `w1/ExecFixturesV2/` (D3), `w1/ExecSessionMarker/` (R3), `w1/ExecErrataR45/` (R4b) | each slot states done+pointer or `open`; an `open` slot keeps the defect on the next round's Planned list |
| `<H12>` `<XM>` `<F14>` | `w1/ExecFixturesV2/` (schema v2 H1/H2), the w2 `CritC1Explain` counter clause, `w1/ExecCounterC1/` (F1-F4 wording) | as above; a counter wording fix is evidenced by the counter's own diff and its re-run, not by a claim |
| `<NAV>`, `<CAL>`, `<OPS>` | `receipts/axis-data.txt` (derived) and `quality/check-axis-scores.py` (published) | shape `A/B`; the published fraction must equal the derived one at `<DATA-SHA>` |

---

## 5. Invariants the blocks must satisfy before the SCORECARD/README commit

1. **No placeholder survives.** Every `<…>` is replaced; a leftover is a false record, and in the axis line it is a
   gate failure (the parser needs `\d+/\d+`).
2. **The axis publication stays the last one.** `quality/check-axis-scores.py` (its docstring and `published_fractions`)
   takes the *last* unquoted "Axis table re-derived at" in the body, 2000 characters of window. The round-48 line must
   be the final such phrase; any later mention of it (an erratum, a w2 correction) must be backticked or quoted, which
   the parser skips. Do not republish an older revision's fractions to "fix" a mismatch — re-derive.
3. **Append-only history.** The round-47 section, the round-47 index row (`corpus/README.md:75`) and the round-47
   Frontier bullet (`:110`) are not edited. The round-48 bullet supersedes the open items at `:110` ("the warm-cache
   path") and `:112` ("the XKB compile itself") by answering them, exactly as round 47 prepended its bullet without
   touching the round-46 one (measured in §1).
4. **Cells carry no `|`.** Both the SOURCES registry and the README tables split on the pipe; `<…>` values must be
   escaped or described (`absent|hit|stale|invalid|disabled` appears escaped as `\|` in the capability row).
5. **Quotes stay honest.** Any quoted source text kept in these blocks is ≤ 25 words with a computed `file:line`;
   paraphrases carry the locator too. The claim table's numbers are receipt lines, never reconstructions.
6. **Session material stays shape-only.** The live receipts named here hold a resolver decision, an rc and a sha256 —
   no window titles, no monitor serials, no input-device names beyond the keymap names a C2 sentence needs.
7. **The two claims stay separable.** The tool-only and entry-only trees are named; a claim whose after-verdict has no
   separability receipt stays `<C1-VERDICT>`/`<C2-VERDICT>`-free until it exists (round-44 N1 is the precedent for a
   published row that gave a pointer instead of a value — do not repeat it).

---

## 6. Out of scope for this seat

- No product file, counter, fixture, entry, registry row, lesson, QUALITY criterion or PROVINCE line is edited here;
  `SCORECARD.md` and `corpus/README.md` are the L1's to write.
- No verdict: `<C1-VERDICT>`/`<C2-VERDICT>` and every closure slot belong to the seats and the post-w1 runs that own them.
- The `### Errata` E1 line states the D4 correction only; its final wording and its sweep of the other
  `terminal-route-r17.md` locators are owned by `w1/ScrErrataD4/erratum.md`.
