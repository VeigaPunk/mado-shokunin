# SourcesRowShape — S056+ row/gate shape and the census acceptance path

Seat: MadoR17.SourcesRowShape (scout). Date 2026-10-20.
Assigned question: read `corpus/SOURCES.md` rows S047–S055 and
`corpus/lessons/round-16.md` §Gate, then state the exact row/gate shape new
S056+ rows must follow (11 columns, tier, anchor with SHA-256, used-by,
rejected-row reason/flip, gate quote ≤25 words) and the checks
`scripts/sources-census.sh validate` performs, so L1 can integrate drafts
without a census failure.

Method and bounds: file bytes only (`read`, `grep`, `awk`, `sed -n`, `wc`);
every census rule below is **read from the script source**, not executed —
this seat ran no census, no `measure.py`, no package/service/live command, and
installed/updated no tool. Baseline corpus is the working tree carrying
round-16 state: 55 rows, tier A/B/C = 51/1/3, status mined/queued/rejected =
43/8/4 (`awk` census over `corpus/SOURCES.md`).

## 0. The checklist in one block

| # | Requirement | Fails if wrong |
|---|---|---|
| 1 | Row sits inside the section headed exactly `## Registry` | E12 |
| 2 | Exactly 11 pipe-delimited columns (awk `NF` = 13) | E01 |
| 3 | No pipe character inside a cell, not even backslash-escaped | E01 |
| 4 | Row starts at 0–3 leading spaces, never 4+ | silently dropped (no code) |
| 5 | id is `S` + 3 or more digits; never `S056-pending` | E02 |
| 6 | id is unused | E03 |
| 7 | `kind` ∈ `spec docs paper code tool dataset talk book community own-work` | E05 |
| 8 | `tier` = `A` for coverage rows (and A + `community` is banned) | E10 |
| 9 | `status` ∈ `queued mined rejected` | E07 |
| 10 | `opened` is a real ISO date ≤ today's UTC date | E08 |
| 11 | `recheck` is ISO date, `NNd`, or a symbolic cadence | E09 |
| 12 | Every `used-by` token of a **mined** row exists at lane root | E11 |
| 13 | No new URL collision in the same `scope` (or say `supersedes S###`) | E04 |
| 14 | `used-by` path string is byte-exactly `corpus/knowledge/<note>.md` | C2 join (silent) |
| 15 | The note's first 15 lines carry `source:` naming that id and `surface: P<n>` | C2 join (silent) |

## 1. Canonical row shape

Header (`corpus/SOURCES.md:11`), 11 columns, pipe-delimited, one space of
padding at each pipe by convention:

```text
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
```

`corpus/SOURCES.md:9` is `## Registry`; the table body is lines 13–67 and
S055 is the current last row (`:67`). Append new rows after it, before
`:69 ## Paths`.

Why NF = 13: `row_pass()` runs `gawk -F'|'` (`sources-census.sh:574-577`), so
a well-formed row splits into `["", id, …, used-by, ""]` = 11 cells + 2 empty
ends. `E01` prints `fields=%d` with `NF-2` (`:635-636`), i.e. the column count.
Verified on the live file: S047–S055 all report `NF=13`.

Cell rules that matter operationally:

- **No pipe in any cell.** `\|` is still a field separator to awk — an escaped
  pipe is an E01, not an escape. Use `;`, `,`, `/`, `§`, `—`.
- **No stray table under `## Registry`.** Every non-separator table row in
  that section increments `rows` and is validated (`:632-676`); a prose table
  pasted there yields E02 for each row.
- **Indentation 0–3 spaces.** The parser strips `^ {0,3}` and ignores lines
  with 4+ leading spaces as code (`:615`, header comment `:39-41`). A
  4-space-indented row is **silently lost** from `rows` and from validation —
  the dangerous case, because the census stays green while coverage fails.
- **The heading must read exactly `Registry`.** `trim(substr(line,3))=="Registry"`
  (`:614-618`). `## Registry table` or `## Sources` puts every following row
  outside the section ⇒ E12 on each.

## 2. Field rules, in the order the checker reads them

| Col | Field | Rule for S056+ | Census code |
|---|---|---|---|
| 1 | `id` | `^S[0-9]{3,}$`; reserved range S056–S069; assign sequentially, no reuse (`round-16.md` §Gate: "Any future source receives the next unused id") | E02, E03 |
| 2 | `source` | Short title + the canonical URL (or lane/system path) as plain text. **Do not wrap the URL in `<…>`**: `url_of()` captures `https?://[^[:space:]\|]+` (`:600-607`) and would keep the trailing `>`, silently defeating duplicate detection. First URL in the cell is the one compared | E04, W04 |
| 3 | `kind` | enum `spec\|docs\|paper\|code\|tool\|dataset\|talk\|book\|community\|own-work` (`:655-656`). Wiki pages ⇒ `docs`; tagged upstream source ⇒ `code` or `spec`; host files / retained evidence ⇒ `own-work` | E05 |
| 4 | `tier` | `A` for every row intended to support C2. Observed S047–S055 are all `A`. `community` at A is an error | E06, E10 |
| 5 | `scope` | One phrase naming the bounded question and its limit ("…, not observed host behaviour"). Compared **verbatim** for E04 | E04, W04 |
| 6 | `anchor` | §3 below | — |
| 7 | `teaches` | §4 below | W02 |
| 8 | `status` | `mined` only once the reciprocal note is on disk; otherwise `queued` with `used-by —` | E07, W03 |
| 9 | `opened` | `2026-10-20` (today, UTC). Must not be later than the census `--today` | E08 |
| 10 | `recheck` | `on-release` for tag-pinned upstream (26 rows use it); `on-change` for host files; `NNd` also legal. Symbolic form must match `^[A-Za-z][A-Za-z0-9 _-]*$` | E09 |
| 11 | `used-by` | §5 below; `—` (U+2014) only when nothing uses the row | E11, W03 |

## 3. Anchor cell — the accepted style, with SHA-256

Two forms are in force (S047–S055). Both are one cell, semicolon-separated,
no pipes.

**Remote / tagged artifact** — revision selector, named sections or symbols
with line ranges, then the raw-byte digest:

```text
tag <TAG>; <section/symbol list>; raw sha256 <64 lowercase hex>
```

Observed:
- `S048`: `tag 1.49; wp_color_manager_v1 supported_* and done; output get_image_description; surface set_image_description; wp_image_description_info_v1 target_luminance; raw sha256 18a2678e3352c3be3fbeed20005d48852b7235d0d78f08b9c987a0b8e91449f9`
- `S053`: `tag 0.15.0; DESCRIPTION, CONFIGURATION exec/return-type/interval/signal, RETURN-TYPE, FORMAT REPLACEMENTS; raw sha256 efb6a63a3d7f125840d4c4a49956664070f36231724e7aa0fa281e6d2de30d82`
- `S047`: `a741f0ac5d655338a5100fc34bc8cec87d237346; manager/head descriptions and zwlr_output_configuration_v1 test/apply/succeeded/failed/cancelled; raw sha256 65b0f82a6cf129bf1a1c31a2428795abd33886c15ddd5f3ad97e5922d7bdc3a7`

Rules:
- The digest is of the **raw bytes fetched**, full 64 lowercase hex. Do not
  copy the truncated 16-hex style of S001–S004; S047–S054 all use full digests
  (`grep -oE 'sha256 [0-9a-f]+' | awk '{print length($2)}'` ⇒ 64, zero
  uppercase).
- Tag/commit is mandatory; a section name without a revision is not an anchor
  (`SOURCES.md` §Search-log errata: "anchor = section plus revision").
- The cell says what the source does **not** establish. Every S047–S054 anchor
  or `teaches` cell carries that limit ("not observed host behaviour",
  "not binary-source equivalence"). A tag's source never proves the host
  binary; host versions stay `[UNK]` (no package queries this round).

**Local / own-work artifact** — path, line anchor, and either a capture
timestamp or the revision that recorded it:

```text
<lane-or-abs path>[:lines]; <what was read>; <captured_utc … | reopened YYYY-MM-DD | file recorded in <40-hex>>
```
- `S055`: `R15-V1/V2 and Gate and correction evidence :161-162,254-277; file recorded in 32c4fda8…, which is this round's reading baseline`
- `S049`: `captured_utc 2026-10-20T04:10:03Z; globals records versus top-level probe/tool/compositor/session_binding; reopened 2026-10-20`
- Host file rows (S020 precedent) use `path:line-line` for each file.

A host-bytes row (`own-work`) has no `http` URL, so `url_of()` returns empty
and the row is exempt from E04/W04 by construction — but it is still subject
to E11 and to the C2 join.

## 4. `teaches` and rejected rows

Accepted rows: one sentence that names the distinction the source grounds,
then the explicit non-claim. Examples to imitate:

- `S051`: `supersedes S007 — list-devices reports built-in defaults, debug-events requires explicit options, record captures context-independent kernel events, replay creates a virtual device; these are different observation/action layers`
- `S054`: `Parsing, formatting, visibility and GTK label update are distinct stages; producer success alone cannot establish user-visible pixels`

Rejected rows are kept as taste evidence (contract rule 1, `S004`) and must
carry reason **and** flip in the `teaches` cell:

```text
REJECTED: <measured reason, with the command or re-measure>; flip: <the condition that would admit it>
```

`supersedes S### —` goes first when the row supersedes an earlier one. Observed:
- `S011`: `REJECTED: verdicts are integrator-recorded axis keys with no claim binding; re-measured 2026-10-19: 45 improved keys via jq, 28 manifest-only against SCORECARD.md:11-26 (dossier §2.2 matched). flip: verdict keys bound to per-round re-runnable output plus the claimed axis named`
- `S045`: `supersedes S030 — REJECTED: duplicate S017 for overlapping current-wiki syntax scope; flip: an independently justified distinct pinned scope after collision review`

Mechanics: `W02` only requires `length(teaches) >= 8` (`:671-672`), so the
observed convention is stricter than the checker; the E04 exemption needs the
literal lowercase token `supersedes S` + exactly three digits (`:647-650`).
A rejected row is exempt from E04 (`url_scope_nonrejected` is only set by
non-rejected rows, `:651-654`) but still produces W04 when it reuses a URL at
a different scope — that is the retained S030/S042/S045 warning set.

## 5. `used-by` and the C2 join (the part that fails silently)

Two independent consumers read the same cell, with different strictness. Both
must pass.

**Census E11** (`sources-census.sh:538-572`, applied at `:721`): only for
`status = mined`; the cell is split on `,`, each token trimmed, `—` and empty
tokens skipped, then tested as `[ -e "$lane_root/$token" ]`.
- Must be **lane-root relative**: `corpus/knowledge/x.md`. `knowledge/x.md`
  resolves to `mado-shokunin/knowledge/x.md` and fails.
- Must be a bare path: backticks, a trailing `.`, `(…)`, or a leading `~`
  all fail.
- An absolute path fails (`$dir/$abs` is not the absolute path).
- Comma-separated is fine and is how multi-use rows are written
  (`S017`, `S049`).

**Rubric V / `measure.py`** (`.ufo/waves/round-17/measure.py:106-121,157-176`):
`used_by(row, path)` is exact string membership after `split(',')` and `strip()`,
compared against the `git ls-tree` path, i.e. `corpus/knowledge/<note>.md`.
- `./corpus/knowledge/x.md` passes E11 but **fails the join** — use no prefix.
- The registry dict only takes rows where `len(cells) == 13` and
  `re.fullmatch(r'S\d{3,}', cells[1])`, so an E01 row is also invisible to the
  score.
- `mined_a()` additionally requires `cells[8] == 'mined'` and `cells[4] == 'A'`.
- The note side: `source:` and `surface:` must be at column 0 within the first
  15 lines; `re.findall(r'S\d{3}')` means `S056-pending` still counts as
  `S056` **in the note**, but the row id itself must be exactly `S056`.

Note prerequisites that gate whether a mined row actually covers a province
(`measure.py:122-208`): `surface: P<n>` in the first 15 lines, all four
headings present with exact text — `## Upstream contract`,
`## Host declaration`, `## Safe observation`, `## Unexercised behavior` — and
at least one `[UNK]` inside the last one. The landed
`corpus/knowledge/terminal-route-r17.md` meets all four (headings at :14,
:59, :91, :103; five `[UNK]`).

Legacy rows still work through `covers: U1/U2→P1`, `U7→P2`
(`measure.py:125`), but still require the same mined/tier-A/used-by join.

`—` is U+2014. A typed hyphen `-` is not skipped by E11; it is tested as a
path and fails.

## 6. Gate block shape (§Gate for round 17)

`lessons/round-16.md` §Gate is the template. A round's gate section must
contain, in this order:

1. **Candidates considered** — the bounded question and the options weighed,
   including the ones rejected for safety (producer execution, live UI,
   package install).
2. **Admit / reject / flip prose** — what is admitted locally, what is
   rejected with its reason, and the exact condition that would flip each
   rejection. Round 16: "Flip for rendered behavior requires a separately
   authorized actual UI task; flip for host recovery requires the operator's
   decision, not a lane verdict."
3. **One block per opened row**, with all of:
   - bold id and the URL (angle brackets are fine **here**, in prose; they are
     not fine in the SOURCES `source` cell);
   - the section or symbol, and the **raw file line number**;
   - the quote, verbatim from the raw bytes (not from rendered HTML/pages),
     in curly quotes;
   - an explicit word count. Round-16 fixes the method: "Counts use
     `len(quote.split())`"; S053's quote is "Thirteen whitespace words",
     S055's "Eleven whitespace words", S054's one-token code quote is "One
     token". Every quote is ≤ 25; a single code token counts as one, and
     scdoc emphasis (`*custom*`) stays inside one token;
   - where the digest/byte binding lives (round 16:
     `evidence/source-bindings.json`), with the byte count;
   - the bounded claim and its `[UNK]` remainder.
4. **No cell churn statement** — new rows are `mined` only through their
   reciprocal note/lesson paths; no existing row's `teaches`/`anchor` is
   rewritten. `status`, `recheck`, `used-by` may change in place and each
   old→new is logged in that round's lesson (`SOURCES.md` preamble, rule
   recorded at `:5-7`).
5. **The search unit** — "The source search unit is three opened source
   locations, not seat count." (round-16 wording), so the count in the report
   matches the census delta.
6. **What is not admitted** — tagged source ≠ installed binary; docs ≠
   observed behaviour; ownership/reason/flip for anything rejected.

Rows are only `mined` when the note exists and the join is reciprocal; a row
whose note is not landed yet stays `queued` with `used-by —` (round-16 kept
that discipline: "New rows are mined only through their reciprocal
note/lesson used-by paths").

## 7. What `sources-census.sh validate` checks

Invocation used for this lane (round-16 verifier precedent):

```bash
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --root /home/vgpnk/Projects/shokunin mado
```

`mado` resolves from `shokunin.conf:56` (`mado|mado-shokunin|…`) to the lane
dir; an explicit lane directory also works and labels output with the
directory basename.

| Code | Exact trigger in the script | Effect |
|---|---|---|
| E01 | Registry row with `NF != 13` (`:635-637`) | exit 1; row then skipped for the remaining checks |
| E02 | id not `^S[0-9]{3,}$` (`:637,640`) | exit 1 |
| E03 | id already seen in this file (`:641`) | exit 1 |
| E04 | same normalized URL **and** same `scope` text as a prior non-rejected row, this row not `rejected`, and `teaches` lacks `supersedes S[0-9]{3}` (`:647-650`) | exit 1 |
| E05 | `kind` outside the 10-value enum (`:655-656`) | exit 1 |
| E06 | `tier` not `A\|B\|C` (`:657`) | exit 1 |
| E07 | `status` not `queued\|mined\|rejected` (`:658-659`) | exit 1 |
| E08 | `opened` not a real ISO date, or later than `--today` (`:660-662`) | exit 1 |
| E09 | `recheck` not ISO date, not `NNd`, not `^[A-Za-z][A-Za-z0-9 _-]*$` (`:663-666`) | exit 1 |
| E10 | `tier==A && kind==community` (`:668`) | exit 1 |
| E11 | `mined` row, used-by token ≠ `—`/empty, and `$lane/$token` absent (`:538-572`) | exit 1 |
| E12 | table row matching `^\| *S[0-9]{3,} *\|` while the current `##` section is not `Registry` (`:619-621`) | exit 1 |
| W01 | `tier==C && mined && used-by != —` (`:669-670`) | printed only |
| W02 | `rejected && length(teaches) < 8` (`:671-672`) | printed only |
| W03 | `mined && used-by == —` (`:673-674`) | printed only |
| W04 | identical normalized URL first seen under a different `scope` (`:643-645`) | printed only |

URL normalization (`url_of`, `:600-607`): first `https?://…` run, fragment
stripped, one trailing `/` stripped, scheme dropped, **host lowercased only**
(path stays case-sensitive). Consequence: two rows for the same page with
different fragments or host case are the same URL; rows with no URL never
collide.

Output lines are TSV `<lane>\t<code>\t<detail>`; a lane with no E-codes also
emits `<lane>\tok\t<path>`. Exit status (`:803-805`): **1** if any `E` code,
**2** if the registry file is missing or usage/env fails, **0** otherwise —
warnings never change the status, and a W-only lane still prints `ok`.

Current expected output for the mado lane is therefore the three retained
warnings plus `ok` and exit 0:

```text
mado	W04	S030 duplicate url … across scopes
mado	W04	S042 duplicate url … across scopes
mado	W04	S045 duplicate url … across scopes
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
```

Any additional W04 after integration is a merge smell (a second row on a URL
already present at another scope), not a failure — but it should be justified
in the lesson, as S030/S042/S045 are.

Two invocation traps:
- **Never pass a stale `--today`.** The default is `date -u +%F`. Copying the
  script's selftest form `--today 2026-10-19` against this lane would emit
  E08 for all 16 rows opened 2026-10-20 (S040–S055) and any new one.
- `--out` is truncated at the start of each invocation (`:699`), so re-runs do
  not accumulate; use distinct paths for before/after receipts anyway.

## 8. Integration pre-flight (exact, copy-pasteable)

Run from the lane root, **after** SOURCES.md and the notes are written and
**before** the census; steps 1–4 are plain greps/awk and were verified
false-positive-free on the current corpus by this seat.

```bash
cd /home/vgpnk/Projects/shokunin/mado-shokunin

# 1. Shape: every row 11 columns; print the new ids' tier/status.
awk -F'|' '/^\| *S[0-9]{3,} /{id=$2;t=$5;s=$9;gsub(/ /,"",id);gsub(/ /,"",t);gsub(/ /,"",s);
  printf "%s NF=%d tier=%s status=%s\n",id,NF,t,s}' corpus/SOURCES.md | tail -n 8

# 2. E11 pre-flight: every mined used-by token exists at lane root.
awk -F'|' '/^\| *S[0-9]{3,} /{id=$2;s=$9;u=$12;gsub(/ /,"",id);gsub(/ /,"",s);
  gsub(/^[ \t]+|[ \t]+$/,"",u); if(s=="mined"){k=split(u,a,",");
  for(i=1;i<=k;i++){p=a[i];gsub(/^[ \t]+|[ \t]+$/,"",p);
  if(p!="—"&&p!="")print id"\t"p}}}' corpus/SOURCES.md |
while IFS=$'\t' read -r id p; do [ -e "$p" ] || echo "PREFLIGHT-E11 $id missing $p"; done

# 3. E12 pre-flight: no row-shaped line outside ## Registry.
awk '/^ {0,3}##[ \t]/{sec=substr($0,4)}
     /^ {0,3}\|[ \t]*S[0-9]{3,}[ \t]*\|/{ if (sec!="Registry") print NR": "substr($0,1,60) }' corpus/SOURCES.md

# 4. No draft markers left.
grep -n 'S0xx-pending\|S0[0-9][0-9]-pending\|TODO\|TBD' corpus/SOURCES.md \
  corpus/knowledge/*-r17.md

# 5. The authoritative check (L1/verifier runs this; exit 0 and a `mado ok` line required).
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --root /home/vgpnk/Projects/shokunin mado; echo "exit=$?"

# 6. Receipt counters for the report (census mode prints counts, not verdicts).
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census \
  --root /home/vgpnk/Projects/shokunin mado
```

Then measure — but note `measure.py` reads **git revisions**
(`git ls-tree`/`git show`), so the notes and SOURCES rows must be committed
before the C2 reading, whereas the census above reads the working tree.

## 9. Round-17-specific facts L1 needs now

Observed in the working tree at read time:

- `corpus/knowledge/terminal-route-r17.md` has landed (8464 B). Its head is
  exactly the required shape: `source:` at **line 1** citing
  `S056-pending`…`S060-pending`, `verified-at:` line 2, `recheck:` line 3,
  `surface: P4` line 4; all four rubric headings and five `[UNK]`.
- It therefore **provisionally consumes five ids, S056–S060**, not two. The
  ids must be assigned consistently with those tokens (or renumbered in both
  the note and the rows), and `-pending` must be stripped from the note's
  `source:` line only if the ids are treated as final; the rubric tolerates
  the suffix, the census would not (ids live only in SOURCES.md, so this is a
  hygiene step, not a census risk, unless a row id is pasted with it).
- Digests already measured in that note, usable directly in the row anchors
  (all 64 lowercase hex):
  - S056 xdg-terminal-exec `README.md` @ v0.14.3 — `c7a1a8bb711e44e4a19ca0a3c943f13a8e53d5fbb6c752e08cb186d5995a9d40`, 14762 B
  - S057 xdg-terminal-exec script @ v0.14.3 — `89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac`, 44020 B
  - S058 Alacritty `extra/man/alacritty.5.scd` @ v0.17.0 — `e444fa45fb7045a61538383c7e588c63e260b9151cb3c8c4dddb742b7a0c4107`, 28787 B
  - S059 host bytes — `bindings.conf` `e574a1ed08535e31deeafe2a26432c6862bb101e8c45d5a6b3f997d7dc810581`; `~/.config/xdg-terminals.list` `d035da571a6bfc7d626d4a88846ea86a8adb6f6662f1f8b4abe2330e53ceb71b`; `alacritty.toml` `695301c86577c808a94a01a4227bfaab3dbbe9a394a9954032f6173adec824f8`
  - S060 `/usr/share/xdg-terminal-exec/xdg-terminals.list` — `a2b5bf691c44aa2557b54df513cc0a9f9f06633468b13e723b208e0b41fef034`, 1053 B
  These are read from the note, not re-fetched by this seat.
- Expected census delta if five rows land as `mined` with
  `used-by: corpus/knowledge/terminal-route-r17.md`: rows **55 → 60**,
  tier.A **51 → 56**, mined **43 → 48**, queued/rejected unchanged
  (W03 would fire five times if `used-by` is left `—`).
- P6 rows are not yet drafted: `corpus/knowledge/idle-lock-route-r17.md`,
  `.ufo/waves/round-17/drafts/NoteIdle-rows.md` and
  `…/NoteTerminal-rows.md` were absent at read time. The same shape applies;
  the clause in item 11 fixes the note head as `source:` … `surface: P6`.
- Existing `corpus/knowledge/idle-lock-plane.md`, `terminals-and-omarchy.md`,
  `theme-wallpaper-plane.md` have **no** `source:` line anywhere, so they
  cannot be made "covered" by adding a row whose `used-by` names them. The
  new P4/P6 notes are the covered entries; the old notes stay linked from the
  notes/README, not used as `used-by` targets for coverage.
- Because `used-by` is a comma list, one row may name both a new route note
  and a lesson where the row is taught; but if any listed path does not exist
  at integration time the census fails, so land notes first.

## 10. Remaining unknowns

- P6's rows and ids: the note and its row draft were absent, so their URLs,
  kind and digest set are unverified here.
- Whether S056 and S057 are distinct URLs (README vs script under the same
  tag) — expected distinct by path; not verified at row level, and both would
  be `code`/`docs` rather than `community` (E10).
- `sources-census.sh` and `measure.py` were **read, not executed** by this
  seat (no-test-execution bound); every rule above is a source reading. The
  authoritative result is the verifier's single run.
- Host installed versions and any live idle/lock or terminal behaviour remain
  `[UNK]`; no package query, `hyprctl`, `systemctl`, `libinput`, terminal
  launch or screenshot was performed.

No tools were installed or updated by this seat.
