# CritC1Predicate — attack on the frozen C1 v2 predicate (round 24, wave 1)

Role: critic (leaf; no spawns). Target: `.ufo/waves/round-24/c1/count.py`
(sha256:`b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66`, `COUNTER_VERSION = v2`).
Question asked: construct the cheapest note that reaches `TARGET_MET` without establishing anything
about rule attribution, beyond the seven control shapes already scored. Verdict first, then the artifact,
the evidence, the hole, the impacted axes, and the smallest safe correction.

## Verdict

**ATTACK_MEETS_TARGET: yes.** Under the frozen counted mode (`MADO_LANE=<sandbox clone>`, refetch, no
`--offline`) the cheapest note I could build scores

```
PASS_ROW=6  distinct_sources=3  readme_indexed=True  verdict=TARGET_MET  (exit 0)
```

from **one 4,465-byte wiki page about udev device paths**, with six claims that are true but vacuous
restatements (“the quoted line says …”), no window/layer-rule attribution fact anywhere, and (in the
strongest variant) the entire note and its README index hidden inside HTML comments so they render as
nothing. The counter is faithful to the frozen sentence it implements — the defect is in what the
sentence measures, not in the code's fidelity to it. The three “distinct S### rows” are three
registrations of the same URL+sha256, which the fleet census only warns about (`W04`, exit 0). A variant
with three genuinely distinct URLs and sha256 values (E) also scores `TARGET_MET`, so the gap is not merely
id-stacking: the quoted lines are lexical homonyms (“udev rules”, “pin matches”, “fallback rule”) and the
claims are tautologies.

## What I did (exact commands, all read-only outside the sandbox)

```sh
LANE=/fast/scratch/hyaku/mado-r24/crit-c1p/lane
mkdir -p /fast/scratch/hyaku/mado-r24/crit-c1p/{fetch,receipts}
cd /fast/scratch/hyaku/mado-r24/crit-c1p
timeout 60 curl -fsSL 'https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/extra/multi-gpu.md' -o fetch/CritC1Predicate-1.bin
sha256sum fetch/CritC1Predicate-1.bin   # sha256:824da1a7848a31a9d970958ca46e2024266ea72272de53ca107a1d6a7d3d8fd4, 4465 B
timeout 60 curl -fsSL 'https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/hyprland-plugins/development/plugin-guidelines.md' -o fetch/CritC1Predicate-2.bin
timeout 60 curl -fsSL 'https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/monitors/_index.md' -o fetch/CritC1Predicate-3.bin
sha256sum fetch/CritC1Predicate-{1,2,3}.bin   # full sha256 digests in the Evidence section

env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q \
  /home/vgpnk/Projects/shokunin/mado-shokunin "$LANE"
# sandbox pinned at lane 81955bd5f04878320b93e60246a146901cdfd2cf (r24 tip at clone time)

# variant A: plain note, 3 SOURCES rows, README coverage row
git -C "$LANE" add corpus/knowledge/rule-attribution-r24.md
git -C "$LANE" -c user.name=crit -c user.email=crit@local commit -qam "r24 critic C1: six tautological rows, one wiki page, three S ids"   # 6d5f28b
MADO_LANE="$LANE" python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-24/c1/count.py HEAD

# variant B: note body wrapped in <!-- --> (renders empty)
# variant C: README coverage row also wrapped in <!-- -->
# variant D: S962 anchor cell changed to a nonexistent line range (:900-901 of a 102-line file)
# variant E: three distinct documents (S960/S970/S971), plain note, commit 50396e5b
# after each: same counter command; final variant D and E also:
scripts/sources-census.sh validate --file "$LANE/corpus/SOURCES.md" --today 2026-10-23
cmark "$LANE/corpus/knowledge/rule-attribution-r24.md"        # render check
```

Only lane write: this report. All other artifacts live under `/fast/scratch/hyaku/mado-r24/crit-c1p/`.

## Counterexample artifact (variant A; 1,432 B, sha256:`870ad65cf9a0a6bcca999c016a72f1569911f2c9d2865916338295fe636a44b0`)

`corpus/knowledge/rule-attribution-r24.md`:

```markdown
# Rule attribution (round 24, C1) — six verbatim fragments

Six rows transcribed from one hyprland-wiki page about udev rules and PCI matching. Nothing
below records which Hyprland window or layer rule produced an applied effect, or what upstream
offers to tell about one; window/layer attribution stays [UNK].

| id | claim | source | quote |
|---|---|---|---|
| A1 | The quoted fragment reads due to the matching `06:00.0` from the first command. | S960 | "due to the matching `06:00.0` from the first command." |
| A2 | The quoted line states It's possible to use udev rules to create reliable symlinks for cards. | S960 | "It's possible to use udev rules to create reliable symlinks to particular device cards." |
| A3 | The quoted example shows we can create a udev rule at a path inside rules.d. | S961 | "we can create a udev rule at `/etc/udev/rules.d/amd-igpu-dev-path.rules` programmatically" |
| A4 | The quoted assignment sets RULE_PATH to `/etc/udev/rules.d/amd-igpu-dev-path.rules` for the udev rule. | S961 | "RULE_PATH="/etc/udev/rules.d/amd-igpu-dev-path.rules"" |
| A5 | The quoted instruction says Then, reload the udev rules with a trailing colon. | S962 | "Then, reload the udev rules with:" |
| A6 | The quoted sentence begins For example, to create a symlink to an AMD card at the path. | S962 | "For example, to create a symlink to an AMD card at the path `/dev/dri/amd-igpu`, we can create a udev rule" |
```

The three SOURCES rows (all `mined`, opened `2026-10-23`, `on-release`, used-by the note, **same URL and
same sha256**; only the free-text `scope`/`anchor`/`teaches` cells differ, which is what keeps census `E04`
(duplicate URL+scope) from firing):

```markdown
| S960 | hyprland-wiki `content/configuring/extra/multi-gpu.md` (@ c66e8de2) — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/extra/multi-gpu.md | docs | A | multi-GPU device paths, the matching PCI-id walk-through | content/configuring/extra/multi-gpu.md:35 @ c66e8de2, sha256:824da1a7848a31a9d970958ca46e2024266ea72272de53ca107a1d6a7d3d8fd4, 4465 B | how a device path is matched to a PCI id in one sentence | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S961 | hyprland-wiki `content/configuring/extra/multi-gpu.md` (@ c66e8de2) — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/extra/multi-gpu.md | docs | A | multi-GPU device paths, the udev rule-file creation example | content/configuring/extra/multi-gpu.md:66-71 @ c66e8de2, sha256:824da1a7848a31a9d970958ca46e2024266ea72272de53ca107a1d6a7d3d8fd4, 4465 B | what one udev rule assignment names on disk | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
| S962 | hyprland-wiki `content/configuring/extra/multi-gpu.md` (@ c66e8de2) — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/extra/multi-gpu.md | docs | A | multi-GPU device paths, the udev reload instruction | content/configuring/extra/multi-gpu.md:900-901 @ c66e8de2, sha256:824da1a7848a31a9d970958ca46e2024266ea72272de53ca107a1d6a7d3d8fd4, 4465 B | the reload step that follows rule creation | mined | 2026-10-23 | on-release | corpus/knowledge/rule-attribution-r24.md |
```

(The `:900-901` in S962 is the fabricated-anchor variant D; its byte count/sha256 are still correct.)
S960–S971 are sandbox ids only; the note and rows are attack artifacts, not a corpus proposal.

README coverage row (variant A):

```markdown
| `knowledge/rule-attribution-r24.md` (MADO-R24-C1, round 24) | Hyprland rule attribution route: six verbatim fragments from one hyprland-wiki page on udev device-path rules and PCI matching; no window/layer rule attribution fact is recorded, and what upstream offers to tell stays UNK. | S960–S962 in [SOURCES](SOURCES.md); recheck 2027-01-23. |
```

## Evidence (receipts under `/fast/scratch/hyaku/mado-r24/crit-c1p/receipts/`)

Source bytes opened for this attack (ordinary curl, pinned commit, no challenge or access control):

- URL: `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/extra/multi-gpu.md`
- local receipt `fetch/CritC1Predicate-1.bin`, 4,465 B,
  sha256:`824da1a7848a31a9d970958ca46e2024266ea72272de53ca107a1d6a7d3d8fd4`
- line anchors used: `:35` (matching PCI id), `:66` (udev rules → device symlinks), `:67` (udev rule file
  creation), `:71` (`RULE_PATH=` assignment), `:83` (reload instruction). Bytes equal the read-only clone
  `/fast/scratch/hyaku/mado-r24/src/hyprland-wiki` file byte-for-byte (sha256 equality checked).
- No claim about the host is made or implied; host Hyprland 0.56.2 behaviour stays `[UNK]`.

Counter runs (frozen v2, counted/refetch mode; full transcripts = the `*.txt` receipts):

Base do-nothing, revision `81955bd5f04878320b93e60246a146901cdfd2cf` (`base-do-nothing.txt`):

```
counter_version=v2 revision=81955bd5f04878320b93e60246a146901cdfd2cf mode=refetch note_present=False rows=0 PASS_ROW=0 distinct_sources=0 readme_indexed=False verdict=TARGET_NOT_MET counter_sha256=b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66
counter_exit=1
```

Variant A — plain note, revision `6d5f28b1f741e650d254479ac34249cebd91bb3d` (`A-plain.txt`):

```
A1	S960	PASS_ROW	-
A2	S960	PASS_ROW	-
A3	S961	PASS_ROW	-
A4	S961	PASS_ROW	-
A5	S962	PASS_ROW	-
A6	S962	PASS_ROW	-
counter_version=v2 revision=6d5f28b1f741e650d254479ac34249cebd91bb3d mode=refetch note_present=True rows=6 PASS_ROW=6 distinct_sources=3 readme_indexed=True verdict=TARGET_MET counter_sha256=b2f37c571455e3aecedef3605cbf5d7844ce2ab7a273a9cb36cc57fec37efc66
counter_exit=0
```

Variant B — note rows inside `<!-- -->`, revision `f49035b5e799e014f672a7e6940eeb134902758c`
(`B-commented-note.txt`): identical `PASS_ROW=6 distinct_sources=3 readme_indexed=True
verdict=TARGET_MET`, exit 0. `cmark corpus/knowledge/rule-attribution-r24.md` emits 26 B,
`<!-- raw HTML omitted -->`; rendered bytes contain zero occurrences of `udev` (`C-note-rendered.html`).

Variant C — README coverage row also inside `<!-- -->`, revision
`c4609226ce4f1d34c5ff7e0f999da092d383708f` (`C-commented-both.txt`): identical `TARGET_MET`; the rendered
README contains zero occurrences of `MADO-R24-C1` (`D-readme-rendered.html`).

Variant D — S962 anchor cell `:900-901` on a 102-line file, revision
`7bc7b18408394a9201e467842238c031c3c5cdca` (`D-fabricated-anchor.txt`): identical `TARGET_MET`.
Fleet census on the same file (`D-census.txt`):

```
file	W04	S961 duplicate url raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/extra/multi-gpu.md across scopes
file	W04	S962 duplicate url raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/extra/multi-gpu.md across scopes
file	ok	/fast/scratch/hyaku/mado-r24/crit-c1p/lane/corpus/SOURCES.md
census_exit=0
```

Variant E — three genuinely distinct documents, revision
`50396e5b02575c50c2e70af75f1a794aedcc34d1` (`E-three-docs.txt`): note 1,487 B
sha256:`1c883d09349485b81c187a3e094824af1b9b9884558eb2459034c4be364c2aee` uses S960
(multi-gpu.md sha256:`824da1a7848a31a9d970958ca46e2024266ea72272de53ca107a1d6a7d3d8fd4`), S970
(plugin-guidelines.md sha256:`99ebec8a1e6c6bc89412c9f56673012a524b672cae7c09065d69f26d1ada9ab9`) and S971
(monitors/_index.md sha256:`2633184089d8d1f80898f4701cf80543e6fa92d033266fa8b6a96a3acfd6279f`) — three URLs,
three digests. Counter: `PASS_ROW=6 distinct_sources=3 readme_indexed=True verdict=TARGET_MET`, exit 0
(`E-census.txt` is byte-identical to `D-census.txt`, exit 0: the retained S960/S961 rows still draw the same
`W04`). So a “distinct sha256 per row” rule alone does not close the hole.

The six E rows (header prose replaced; S970/S971 rows carry the URL+sha+anchor given above):

```markdown
| A1 | The quoted fragment reads due to the matching `06:00.0` from the first command. | S960 | "due to the matching `06:00.0` from the first command." |
| A2 | The quoted line states It's possible to use udev rules to create reliable symlinks for cards. | S960 | "It's possible to use udev rules to create reliable symlinks to particular device cards." |
| A3 | The quoted line says If no pin matches, latest git will be used. | S970 | "If no pin matches, latest git will be used." |
| A4 | The quoted advice says It's always advised to use the API entries whenever possible. | S970 | "It's always advised to use the API entries whenever possible, as they are guaranteed stability as long as the version matches." |
| A5 | The quoted monitor line says Leaving the `output` empty will define a fallback rule. | S971 | "Leaving the `output` empty will define a fallback rule to use when no other rules match." |
| A6 | The quoted sentence says you may only use one of these rules per monitor. | S971 | "you may only use one of these rules per monitor in the config." |
```

Receipt hashes: `base-do-nothing.txt` sha256:`0e15270a328fa57c29b600467364c72081e3d0d2000c716032c60efdf67293e0`,
`A-plain.txt` sha256:`0a312b3de8614cb2a36912c75333100e6ce02ef302f5cf73695b82f94651c08b`,
`B-commented-note.txt` sha256:`a0b1d0444f46658def70f81447f3eddf8fa77c8041763f643d85edd2c7d4efb7`,
`C-commented-both.txt` sha256:`df1f189f47ce3e667d2314f86d4a599a803827e0d47bd65fee9ada984630d8eb`,
`D-fabricated-anchor.txt` sha256:`7b7c7ecd7901bbff21d06f2610db87205a9543dacd093c5c3884592b71e872e8`,
`D-census.txt` sha256:`e3b594f29ad0855ea0bfb26ceeb0985a300bcf9975df0a6ad01b24b66ab7d0f3`,
`C-note-rendered.html` sha256:`99e7812074860a429ddaa1aa5f3784ce470562a0def36f69c875bbc6fcda82db`,
`D-readme-rendered.html` sha256:`87b23a7a623e68eac2b1f7d5d42a847fc4eb0941adbfe256fd8ea3961c325f70`,
`E-three-docs.txt` sha256:`b97d0a26702f149c1171e9b229becca760a947e8efb6132ececc23bc2c7079ae`,
`E-census.txt` sha256:`e3b594f29ad0855ea0bfb26ceeb0985a300bcf9975df0a6ad01b24b66ab7d0f3` (byte-identical to `D-census.txt`).

## The hole (five clauses of v2, each shown exploited)

1. **“≥ 3 distinct S### rows” counts row ids, not documents.**
   `distinct = sorted({r["source"] for r in passing})` (`c1/count.py:159`) dedupes S ids only. S960/S961/S962
   are three ids over one URL and one sha256, so `distinct_sources=3` while the note has exactly one
   document. Nothing in the predicate or code requires distinct URL or distinct `sha256:` per passing row.
   The census does not stop it: same URL with different `scope` text is `W04`, a warning, and the lane's own
   SOURCES already carries seven such rows (S030, S042, S045, S097, S119, S120, S121; S030 and S045 share
   one URL). The no-harm guard
   (`sources-census.sh validate` exit 0) therefore passes on this shape. Variant E shows that a
   distinct-URL+sha256 rule is necessary but not sufficient: three genuinely distinct documents (three
   distinct digests) still pass 6/6; the load-bearing defects are items 2 and 3.

2. **The “rule-topic word” gate is lexical, so off-topic homonyms pass.**
   `TOPIC_RE` (`c1/count.py:37`) accepts bare `rules?`, `match(?:es|ing)?`, `props?`, `tags?`. In the
   counterexample the quotes contain “rules” only as *udev* rules or monitor fallback rules, and
   “match(es/ing)” only as a PCI-address match, a git-pin match, or “when no other rules match” — nothing
   about window/layer rule attribution. A quote can also be any window of a line: A6 and A3 are two
   overlapping substrings of the same sentence (`:67`), and duplicate detection is exact-string only
   (`q in seen_quotes`), so one sentence yields two “distinct” quotes.

3. **The claim-anchor clause is satisfied by a tautology.**
   `anchored()` (`c1/count.py:46`) only needs a ≥4-word run of the quote inside the claim, or one backticked
   ≥4-char identifier from it. Every claim here is “The quoted <fragment/line/example/instruction> reads/
   states/shows/sets/begins <4+ words of the quote>”: true of the bytes, anchored, and worth nothing. The
   clause was added to kill *unrelated* claims (CtlC1LabelShortcut) but a claim that quotes the line back at
   the reader is trivially related and trivially passes. This is the “known v2 limit” named for
   CtlC1OffTopic in the registration, but no scored control demonstrates a *passing* note; here is one, and
   the note can even state in its own header that window/layer attribution stays `[UNK]` and still pass.

4. **The scan is Markdown-unaware, so the note and its index can be invisible.**
   Rows are matched line-by-line over raw `git show` bytes (`ROW_RE`, `c1/count.py:38,160`); nothing strips
   HTML comments or fenced code blocks. Variants B/C put all six rows and the README coverage row inside
   `<!-- -->`; `cmark` renders the note as an empty document and the README row does not render at all, yet
   `note_present=True`, `rows=6`, `readme_indexed=True`, `TARGET_MET`.

5. **SOURCES metadata beyond status/opened/used-by/URL/sha is never read.**
   The counter reads `row[7]`, `row[8]`, `row[10]` and searches the whole row for a sha256
   (`c1/count.py:124-137`); `row[5]`, the `<path>:<lines>` anchor cell, is never consulted. Variant D sets
   S962's anchor to `:900-901` of a 102-line file and the counter is unchanged; the census validates ids,
   enums, dates and used-by existence but no anchor cell either. False provenance inside a passing row is
   therefore free.

These are beyond the seven control shapes: none produced a *passing* note whose sources collapse to one
document (C1QuoteSplice registered one wiki page under two ids but scored 1/0), and none tested a restatement
claim (the off-topic control's claims were unsupported and failed v2 on the anchor), comment-hidden rows or
index, or a fabricated anchor span.

## Impacted axes

- **Coverage (C1), primary.** `PASS_ROW`/`TARGET_MET` does not measure “rule attribution moved onto
  documentary sourced ground”; it measures well-formed rows over any one to three legitimate but off-topic
  documents. A data seat
  (or a future lane) can land a note that scores 6/6 while adding zero attribution knowledge. The C1 verdict
  for round 24 must not rest on the counter alone.
- **Provenance / duplicate authority.** Three S ids over one sha256 create the appearance of three
  corroborating sources; the note's header itself can deny attribution and still pass. Any wave-2 “three
  distinct sources” sentence in a report or README needs a `sha256sum` recomputation per row.
- **Note visibility.** A passing note can be an empty rendered page. Reviewing the file bytes is not the same
  as reviewing the rendered corpus.
- Not impacted: C2, `tools/`, host safety. No source claim here says anything about Hyprland behaviour.

## Smallest safe correction

Frozen predicates cannot change after the control receipts, so this is two layers: a review gate that works
**now**, and a v3 predicate delta for the next round. Both are mechanical.

Apply now, in wave 2, to any note offered against C1 (no predicate edit, no re-scoring):

1. `sha256sum` the bytes re-fetched for every S row the note cites; require **≥ 3 distinct sha256 values**,
   not ≥ 3 S ids. Reject notes whose cited rows collapse to fewer than three documents. Necessary, not
   sufficient (variant E: three distinct documents, three digests, still `TARGET_MET`).
2. Read the note **as rendered** (strip `<!-- … -->` and fenced blocks first); reject if the claim rows are
   not visible prose.
3. Reject a claim that is a quotation frame plus the quote (“The quoted … reads/states/shows/begins/says
   <quote words>”). Each admitted claim must name a rule-application/attribution mechanism or an explicitly
   stated upstream absence (window rule, layer rule, getprop, rule name/id/index) **and** an effect or a
   limit — this is exactly the QUALITY bar “falsifiable, source-cited”.
4. Check each quote lies inside the S row's `<path>:<lines>` span at the pinned commit.

For the v3 predicate (next round; not applicable to r24's frozen count), smallest code deltas:

- `distinct_sources` = number of distinct `sha256` digests among passing rows (optionally also distinct
  normalized URLs), computed per passing row rather than from `r["source"]`.
- Strip HTML comments and fenced code blocks from note and README before `ROW_RE`/index matching.
- Parse the SOURCES anchor cell (`path:lines @ pin`) and assert the whitespace-collapsed quote occurs inside
  those lines of the fetched bytes; require the anchor path to equal the URL path.
- Tighten `TOPIC_RE` to a rule-context class (`window ?rules?|windowrules?(?:v2)?|layerrules?|layer ?rules?|getprop`)
  in both quote and claim; drop bare `rules?|props?|tags?|match(es|ing)?`.
- Optional if (1) lands: cap passing rows per S id at 2, so one page cannot supply six rows.

The correction that actually closes the semantic gap is (3), together with the rule-context gate on both
quote and claim; variant E shows (1) alone leaves a three-document, three-digest note that still passes with
tautologies. The rest close the mechanical shortcuts (duplicate authority, invisible text, false anchors)
that make a vacuous note look like coverage.

## What the bytes do not establish

The three wiki pages are about udev rules and persistent DRI device paths for multi-GPU systems, plugin API
stability advice, and monitor output fallback rules. None says anything about Hyprland window or layer rule
evaluation, rule identity, applied-effect attribution, or what `hyprctl` can report about a rule. Nothing
here demonstrates host behaviour, and no host read was taken;
the host running Hyprland 0.56.2 remains unmeasured for this question in this report. The only thing
demonstrated is that frozen v2 scores a zero-knowledge note as `TARGET_MET`.
