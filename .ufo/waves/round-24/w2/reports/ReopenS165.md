# ReopenS165 — SOURCES row S165 re-open (wave 2, round 24)

Reviewer: MadoR24.ReopenS165. Scope: exactly SOURCES row S165
(`corpus/SOURCES.md:177`) at `39c596307333b8ca0a1e42b3f3b9a748bb8b208b`, and the four
claim rows citing it (A19–A22) in `corpus/knowledge/rule-attribution-r24.md`.

## 1. Pin and byte fidelity — all checks pass

Row S165 claims:
- URL: `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/configuring/core/rules/window-rules.md`
- sha256 `9ecff146ada23ba11f44b0ddbda15bf82bb3b32bcec29f98388466def101ed95`, 16200 B
- ranges: `content/configuring/core/rules/window-rules.md:6-15, 22-44, 63-64, 132-134, 229-238, 315-342`

Re-fetched myself (curl, raw.githubusercontent.com, pinned URL):
- live bytes: sha256 `9ecff146ada23ba11f44b0ddbda15bf82bb3b32bcec29f98388466def101ed95`, 16200 B
- lane committed fetch `.ufo/waves/round-24/fetch/S165.bin`: sha256
  `9ecff146ada23ba11f44b0ddbda15bf82bb3b32bcec29f98388466def101ed95`, 16200 B
- `git show c66e8de:content/configuring/core/rules/window-rules.md` in read-only clone
  `/fast/scratch/hyaku/mado-r24/src/hyprland-wiki`: sha256 `9ecff146ada23ba11f44b0ddbda15bf82bb3b32bcec29f98388466def101ed95`

All four agree exactly (row = plane fetch = live bytes = pin blob). File has 344 lines; all cited ranges are in-bounds.

Pin resolution (both methods):
- local clone: commit `c66e8de21f5ecdc4bc5e278e7d94800ea10957af` exists (tree reachable,
  `cat-file -t` = commit), dated 2026-10-22 14:52:44 +0200, subject
  "configuring/code-snippetes: fix a var and a note mistake (#1683)".
- `git ls-remote https://github.com/hyprwm/hyprland-wiki`: `c66e8de…` is currently **HEAD
  and refs/heads/main** — the pin resolves to the live main tip. (Residual risk: any future
  main push moves the ref; the pinned commit itself is immutable and stable.)

## 2. Per-row verdicts (A19–A22)

Quote matching method: byte substring search over the live bytes; for multi-line quotes, exact
whitespace-collapsed join of the cited contiguous lines, verified token-identical (no word added,
dropped, or reordered).

### A19 — `partial`
Claim: "The documented `hl.window_rule` syntax shows optional `name`, `match`, and `effect` fields."

- (a) Quote vs bytes: NOT a literal substring. The quote is the exact whitespace-collapsed join of
  contiguous lines 9–15 (15/15 tokens identical), which lives inside the cited range 6–15. It passes
  the frozen C1 predicate's "verbatim (whitespace-collapsed)" norm, but fails a literal-byte verbatim
  reading. Recorded as a formatting nuance, not a misquote.
- (b) Truth/overreach: the syntax block marks only `name?` (the `?` optional marker) as optional.
  Neither `match` nor `effect` carries an optional marker in the quote, and no other line in this page
  (whole-file scan for optional/required/parameter) marks `match`/`effect` optional. The claim asserts
  all three fields are optional → **overreach on `match` and `effect`**. The bytes support "the syntax
  shows `name?`/`match`/`effect` fields", not "optional … match, and effect".
- (c) Attribution: the row is declaration syntax (generic mechanics); the `name` field is the
  identity-bearing construct behind named-rule handles, but the claim sentence itself says nothing about
  which rule produced an effect or what exposes rule identity. Weak/incidental attribution link.

### A20 — `partial`
Claim: "The wiki says effects marked as _dynamic_ are re-evaluated whenever the matching property of the window changes."

- (a) Quote is a literal single-line substring at line 315 (also corroborated by line 134
  "Dynamic effects are re-evaluated every time a property changes."). Verbatim ✓.
- (b) TRUE of the quoted bytes; no overreach.
- (c) Attribution: dynamic re-evaluation timing is effect-application mechanics — it identifies no
  rule, exposes no rule identity, and is not used in the note's attribution-answer table. Fails the
  "rule attribution rather than generic rule mechanics" test.

### A21 — `holds`
Claim: "The wiki states effects are processed top to bottom, and the _last_ match takes precedence."

- (a) Quote is a literal single-line substring at line 318. Verbatim ✓.
- (b) TRUE of the quoted bytes; no overreach.
- (c) Attribution: precedence/ordering is the attribution-by-reasoning mechanism — the note explicitly
  cites A21 for "Ordering still decides which value wins … last match wins", i.e. it answers *which
  rule's effect is the observed one*. Meets the test.

### A22 — `holds`
Claim: "The page states dynamic tags have a suffix of `*` and tells readers to check window tags with `hyprctl clients`."

- (a) Quote is NOT a literal substring; it is the exact whitespace-collapsed join of contiguous lines
  231–233 (20/20 tokens identical), inside cited range 229–238. Passes the frozen predicate's
  whitespace-collapse norm; fails a literal-byte reading. Same formatting nuance as A19.
- (b) TRUE of the quoted bytes (both sentences present, joined verbatim); no overreach.
- (c) Attribution: the tag route is the note's documented "which rule fired on a window" mechanism —
  `hyprctl clients` exposes rule-produced tag state and the `*` suffix marks rule-made dynamic tags.
  Meets the test.

## 3. Findings by severity

1. **[medium] A19 overreach (C1 truth)**: the claim's "optional … `match`, and `effect`" is not
   supported by the cited bytes; only `name?` carries the optional marker. The row asserts more than
   the source shows. The frozen counter still counts A19 (anchor clause satisfied), so this is a
   reviewer finding the counter cannot see — exactly the wave-2 mandate.
2. **[low] A20 off-topic-ish (C1 attribution)**: quote and truth are clean, but the claim is generic
   evaluation mechanics, not rule attribution. The note itself does not use A20 in its attribution
   answer table. Borderline; reported so main can weigh it against the rest of C1.
3. **[info] A19/A22 literal-verbatim nuance**: both rows' quotes are whitespace-collapsed joins, not
   literal substrings. Content is token-identical and contiguous, and the frozen predicate defines
   verbatim as whitespace-collapsed, so this is not a defect under the counted rule — recorded for
   precision, not as a failure.

No finding against hash fidelity, byte count, or pin resolution — all exact.

## 4. Residual risk / verification gaps

- "Optional" semantics of `match`/`effect`: I scanned this page only. S168 (`_index.md`, 953 B)
  was not opened here; if another page defines the `?` convention or field optionality, A19's wording
  could have a second support point. Assignee-scope limited to S165; whoever owns S168 may cross-check.
- The C1 counter's own run at tip (23/26) was not re-run here (read-only seat, no counter execution
  requested); quote/anchoring facts above were checked directly against bytes.
- Pin-to-HEAD status is time-of-check; the commit object remains valid regardless.

## Verification log
- `curl` fetch of pinned URL → `sha256sum`/`wc -c` (live bytes)
- `sha256sum`/`wc -c` on `fetch/S165.bin`
- `git show <pin>:<path> | sha256sum` in read-only src clone
- `git ls-remote` (HEAD + refs/heads/main)
- python3 (timeout 60) substring/whitespace-collapse/token checks, line-range dumps
- `read` of SOURCES.md:177, registration.md (frozen predicate), rule-attribution-r24.md:1-50

No installs performed. No lane files edited; no git/jj write commands run.
