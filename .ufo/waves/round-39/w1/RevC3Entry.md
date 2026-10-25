# RevC3Entry — C3 knowledge-entry review (round 39, w1, 2026-10-25)

Scope: `.ufo/waves/round-39/w1/ScrKnowledgeEntry/config-option-table-r39.md` (4013 B) vs
`registration.md:73-84` (frozen first), the wave dispatch spec, ExecAssimFetches receipts,
and `tools/mado-options.py` source. No `lsp` device is mounted in this session (not in my
tool inventory) — all checks are source/text-level; I executed no counter and no repo tool.
Only this file was written.

## Verified passes

1. **Provenance trio first** (entry :1-3): `source: S218, S219` / `verified-at: 2026-10-25`
   (today) / `recheck: on-release`. `on-release` is valid held vocabulary
   (`corpus/knowledge/hyprctl-flags-r28.md:11`, `request-limits-upstream-r31.md:11`,
   `request-socket-live-bound-r8.md:11`, `hyprland-config-era-r12.md:5`).
2. **S218 receipt + quote independently verified**: `sha256sum
   w1/ExecAssimFetches/S218.bin` → `400d18195020316c25e1874e567d868458b69e342a019b3ec8da6211d7222801`
   (matches lesson GATE S218, `w1/ScrLesson/round-39.md:33`); grep for
   `invocations, each one will update just what you pass into it.` → 1 hit, exit 0; full
   rendered form `You are allowed multiple <code>hl.config()</code> invocations, each one
   will update just what you pass into it.` present (raw HTML carries inline `<code>` tags,
   as the lesson spot-check states).
3. **S219 located quote verified**: `tools/mado-options.py:2` is exactly
   `mado-options.py - static resolver of the config-tree option table.`
4. **Falsifiable consequence present** (§Source graph, "A falsifiable consequence:"):
   theme vs `ai-usage.conf` attribution + removal flip, "assuming no still-later declaration".
5. **Limits stated**: ordering-rule-not-runtime-release disclaimer; "static parser boundary,
   not a complete implementation of every hyprlang syntax feature"; divergence labels
   "describe the comparison of the supplied inputs"; missing-dump-entries epistemics;
   static ≠ live health. §Evidence and limits is compliant in shape.
6. **Universal-clause scan** (every/always/never/all): besides the M2 lead sentence below,
   remaining universals are scoped negations ("not a claim that every Hyprland runtime
   release loads every user's files…", "Missing dump entries are not evidence…").
7. **check-index readiness**: `ROW_RE = ^\| `knowledge/([^`]+\.md)`` at column zero
   (`quality/check-index.py:12`); `evaluate()` requires exactly one matching README row per
   `corpus/knowledge/*.md` blob at the measured rev (:100-118). `config-option-table-r39`
   appears 0× in `corpus/README.md` today and the entry blob is not yet at
   `corpus/knowledge/` → no duplicate/dangling possible yet. A single column-zero row
   `| `knowledge/config-option-table-r39.md` (…, round 39) | … | … |` landing in the same
   commit as the entry passes (harm-watch 55/55 → 56/56). Any leading whitespace or
   backtick variation breaks `ROW_RE` — keep the exact held row shape.

## Defects

### B1 — blocker (quote grounding): OBS lines carry no located Gate quotes
Entry :43-45 *describe* the quotes ("consult its located Gate quote…") instead of quoting.
The dispatch (w1-spec.json, ScrKnowledgeEntry item) requires each `**OBS**` line naming the
id **next to one of its located Gate quotes**. Both quotes are now available and verified
(passes 2-3). Fill verbatim:
- OBS S218 → `"You are allowed multiple hl.config() invocations, each one will update just
  what you pass into it."` (rendered-verbatim; note the `<code>` tag caveat as the lesson
  spot-check does).
- OBS S219 → `"mado-options.py - static resolver of the config-tree option table."`
  (`tools/mado-options.py:2`).
Also OBS S219's description says the quote "describes the static config-tree table and
optional `getoption` merge" — the quoted docstring line covers only the static table; the
merge is a later docstring section (`tools/mado-options.py:13+`). Keep the description to
what the quote says.

### B2 — blocker (factual): the `##` parser-boundary paragraph misdescribes the resolver
§Parsing boundaries: "The parser recognizes the `##` section/comment convention as
structural context rather than treating those lines as settings". The tool has **no `##`
section convention**. Actual behavior (`tools/mado-options.py`): a line whose first char is
`#` is a comment; if it starts with `# hyprlang` it carries directives (noerror, if/endif
nesting) (:286-294, :337-339); **`##` inside a value is the escape for a literal `#`** —
fixture `color = ##000000` → value `#000000` (:626, checks :836-837); trailing comments are
stripped (`col.inactive_border = rgba(595959aa) # trailing comment dropped`, :615/:838-840).
The entry states none of this and its sentence would mislead a reader into treating `##` as
a section marker while missing the in-value escape. Rewrite the paragraph on these three
behaviors (grounded by S219 own-work).

### M1 — major: the layer list is presented as resolver precedence; the resolver has none
§Source graph: "Its table layers are applied in this order: 1 built-in defaults; 2 theme
files; 3 user configuration files; 4 toggles glob; 5 `ai-usage.conf`. Later layers override
earlier declarations… This is an ordering rule of this resolver…". Code: ownership is
last-declarer in `source =` traversal order (`declare()` overwrites per declaration,
:261-277); layer names are path-derived labels only (:59-63, :215-232); the docstring's own
layer enumeration differs in order and adds `theme, root` (:8-9). The fixed order is the
HOST root file's source order (held MADO-1 include-order measurement; fixture
hyprland.conf :581-587 sources `ai-usage.conf` last), not a resolver rule. Consequence: the
entry's falsifiable theme-vs-ai-usage consequence holds on this host's graph but would be
false for a tree sourcing `ai-usage.conf` before the theme. Rewrite: "last declarer in the
traversed graph owns" (already present, keep as the mechanism); present the ordered list as
this host's root-file source order citing the held MADO-1 ground; add the missing `root`
layer (hyprland.conf's own settings; fixture `expected.json` layer `"root"`) and `other`.

### M2 — minor: one bare universal + an unsupported S218 attribution
- "Comments are not option declarations." (§Parsing boundaries lead) — universal as
  written; rescope to the parser ("the parser treats comment lines as structural context,
  not declarations") so it rests on S219's own-work behavior (B2's rewrite covers it).
- OBS S218 calls the source "the syntax reference for interpreting option assignments and
  comment/section lines" — the located S218 quote (hl.config() merge) grounds assignment
  merge semantics, not comment/section lines. Trim the attribution to what the quote
  supports, or that clause stays ungrounded.

### m1 — minor: exclusion list narrower than the tool's
Entry excludes "bind, animation, workspace, and rule declarations"; the tool also excludes
exec/exec-once, monitor, env, bezier, layerrule (docstring :5-7, exclusion set :82-85).
Under the entry's list a reader would expect `monitor = …`/`env = …` rows. Align the list.

### m2 — minor: variable expansion under-described
The resolver substitutes in-scope hyprlang variables in displayed values (fixture checks:
`general:inactive_gap` ← `$activeBorderColor` :829-831; `input:repeat_rate`
variable-in-user-file :841-842). The entry's hedge ("should not be mistaken for an
independently expanded runtime value unless the resolver explicitly reports expansion") is
safe but should state this explicitly.

## Landing blockers / verification gaps (not entry-text defects)

1. `quality/counters/c4-r39-options-entry.py` does not exist (read → not found;
   `glob quality/counters/*r39*` → only `c3-r39-options.py`). PRED-C4-r39-v1 is unrunnable;
   the `registration.md:79-84` counting command cannot execute. C3 `admitted=1/1` is
   unmeasurable until it lands.
2. `corpus/SOURCES.md` has no S218/S219 rows (grep `S21[89]` → 0 matches); drafts sit at
   `w1/ScrSourcesRows/rows.md`, with the S219 row marked INCOMPLETE pending a
   committed-bytes hash. Lesson Gate lines exist in draft only
   (`w1/ScrLesson/round-39.md:33-34`).
3. `corpus/README.md` has no row for the entry (grep → 0) and the entry is not yet at
   `corpus/knowledge/`; both must land in the same commit for check-index (pass 7).
4. **S219 receipt binding stale**: lesson GATE S219 `sha256=9787b53b…cf59` (37180 B at
   draft time) vs current worktree `tools/mado-options.py` =
   `cee78d99de2e3420572aa028f439240ac12e5eb6d595de75e2fc62e5ea9ce61e` (37358 B, mtime
   2026-10-25 16:10). The quoted :2 text is unchanged, but the data tip must re-hash
   (`git show <data-tip>:tools/mado-options.py | sha256sum`); until the data commit exists
   the S219 GATE line cannot bind committed bytes (openly declared in the lesson).

## Residual risk

- No `lsp` device available in this session → semantic checks are source/text reads, not
  LSP cross-references; no counter/tool execution by me (reviewer scope; execution belongs
  to ExecOptionsTool / Build8C340).
- The tool file is still moving (hash changed within the wave window); B2/M1 findings are
  pinned to worktree bytes `cee78d99…` at ~2026-10-25 16:1x.
- Once B1 is applied, the OBS quotes match the lesson GATE fence byte-for-byte; the entry
  itself intentionally does not restate receipts/anchors (lesson is the binding record).

**Verdict: NOT ADMITTED as drafted.** B1 + B2 must be fixed before landing; M1 rewrite
strongly recommended. After B1, both citations are quote-grounded against verified
receipts; after B2/M1 the body's behavioral claims match the cited own-work source.
