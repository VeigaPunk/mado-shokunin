# Reopen S154 — Hyprland rule engine header (mined SOURCES row)

Scope: SOURCES.md row S154 at lane HEAD `39c596307333b8ca0a1e42b3f3b9a748bb8b208b` (round base
`8e5d93691e2f7baa3d4a0a61c9428e5acb5d2122`). The row is `mined` and one claim row (A2) in
`corpus/knowledge/rule-attribution-r24.md` cites it. Everything below was re-derived from the pinned bytes; the
row record and the note are byte-identical at HEAD and in the worktree (`diff` of `git show HEAD:<path>` vs the
file: SAME_ROW, SAME_NOTE).

## 1. Row record (corpus/SOURCES.md:166)

| field | value |
|---|---|
| id | S154 |
| source | Hyprland rule engine header |
| URL | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/desktop/rule/Engine.hpp |
| kind | code |
| claim lines | src/desktop/rule/Engine.hpp:11-20 @ efb50993780079460b0cbed1363e2166a2de1d9f |
| sha256 (row) | `sha256:ee1b0e64c970c62ada2110935de4afb4b8023838244732520c2695dd50e7de19` |
| bytes (row) | 707 B |
| description | "Declares register/unregister/update/cleanup APIs, a const-vector rules() accessor, and the private m_rules vector" |
| status / opened | mined / 2026-10-23 |
| recheck | on-release |
| used-by | corpus/knowledge/rule-attribution-r24.md |

## 2. Independent fetch vs committed bytes vs row metadata

- Fetched the pinned raw URL myself (`curl -sSL`, exit 0) to `/fast/scratch/hyaku/mado-r24/w2/S154.refetch.bin`.
- sha256 of fetched bytes: `ee1b0e64c970c62ada2110935de4afb4b8023838244732520c2695dd50e7de19` — identical to the row.
- Byte count: **707** — identical to the row's "707 B"; raw file content is 30 lines, ends after `}` with a
  trailing newline.
- `cmp` fetched bytes vs committed `.ufo/waves/round-24/fetch/S154.bin` → **IDENTICAL** (worktree file: 707 B,
  same sha256).
- Committed blob at HEAD: `git show 39c5963:.ufo/waves/round-24/fetch/S154.bin | sha256sum` →
  `ee1b0e64…de19`, 707 bytes, `git ls-tree` → blob `b0ea118e7f7d4554ad0f65c4f9c4881323e9db4a`. The committed
  fetch bytes are exactly the pinned-URL content.

## 3. Pin resolution

- Remote: `git ls-remote https://github.com/hyprwm/Hyprland 'refs/tags/v0.56.2*'` →
  `efb50993780079460b0cbed1363e2166a2de1d9f refs/tags/v0.56.2`. The pinned commit is the v0.56.2 tag tip.
- Local clone `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2`: `git cat-file -t efb5099…` → `commit`;
  `git rev-parse v0.56.2^{commit}` → `efb5099…`; blob size of `efb5099:src/desktop/rule/Engine.hpp` → 707.
  `git show v0.56.2:src/desktop/rule/Engine.hpp | cmp - S154.refetch.bin` → CLONE_BYTES_IDENTICAL.
- Anchor cell `:11-20` matches exactly: line 11 `registerRule(SP<IRule>&&)`, 12–13 the two
  `unregisterRule` overloads, 14 `updateAllRules`, 15 `cleanExecRules`, 16 `clearAllRules`, 17 `rules()`,
  18 blank, 19 `private:`, 20 `m_rules`. The description cell ("register/unregister/update/cleanup APIs, a
  const-vector rules() accessor, and the private m_rules vector") is accurate to those bytes; "cleanup" covers
  `cleanExecRules`/`clearAllRules`, slightly loose but not a claim.

## 4. Claim row A2 under test (corpus/knowledge/rule-attribution-r24.md:36)

> | A2 | The header declares a `rules` accessor and keeps `m_rules` as the engine's private vector. | S154 | "const std::vector<SP<IRule>>& rules(); private: std::vector<SP<IRule>> m_rules;" |

### (a) Quote occurs verbatim — holds

The file's exact bytes contain, after whitespace collapsing (the frozen predicate's test):

```
const std::vector<SP<IRule>>& rules(); private: std::vector<SP<IRule>> m_rules;
```

This is a contiguous span of the file: line 17 `const std::vector<SP<IRule>>& rules();`, line 18 blank,
line 19 `private:`, line 20 `std::vector<SP<IRule>> m_rules;`. Nothing is skipped or reordered; only indentation
and the blank line/newline are collapsed. Quote length 6 words (≤25) and it contains the topic token `rules`.

### (b) Claim true of the bytes, no overreach — holds

- `rules()` is declared in the `public:` section as `const std::vector<SP<IRule>>& rules();` — an accessor
  returning a const reference to the rule vector. (It is a non-const member function; the claim says
  "accessor", not "const method", so it does not misstate this.)
- `m_rules` is the sole data member, declared after `private:` as `std::vector<SP<IRule>> m_rules;`. "keeps
  m_rules as the engine's private vector" is exactly what the bytes say; there is no second container and no
  public exposure of the member itself.
- Nothing in the claim asserts callers, lifetime, thread-safety, or that `rules()` is the only channel — so no
  overreach.

### (c) Row says something about rule attribution — FAILS

The row states a declaration inventory: an accessor exists and the vector member is private. It contains no
sentence about *which rule produced an effect*, and none about *what exposes rule identity* to an observer.
Contrast the note's own attribution routes, none of which cite A2: applied value (A11), workspace-rule listing
(A24), tag route (A10, A22), named-handle enable/disable (A12–A14, A23), per-property rule mask (A5–A8), logs
(A18). The `rules()` call site that matters to the note is A4 on S155
(`for (const auto& r : ruleEngine()->rules())`); S154 only declares it. The SOURCES description itself labels
the row "Rule engine API and private storage declaration" — generic rule mechanics by the row's own words.

The strongest defence available — "the `rules()` accessor is what exposes rule objects (hence identity) to
in-process code" — is an inference the claim does not make; it would need a row like "rule identity is
reachable only by enumerating `rules()` in-process, never through hyprctl/Lua/socket2". A2 does not say that.

## 5. Counter interaction — A2 passes C1 v2 while being off-axis

- Quote topic test: `c1/count.py:37` topic regex `\b(?:window ?rules?|…|rules?|…)\b` matches the literal
  token `rules` inside the quoted declaration (count.py:111-112 `quote-off-topic` is not raised).
- Claim-anchor clause: backticked `rules` (5 chars) and `m_rules` (7 chars) both occur in the quote, so the
  v2 anchor clause passes.
- Consequence: A2 is counted in `PASS_ROW` — the row demonstrates in the real data the limit the registration
  already records for CtlC1OffTopic ("the counter cannot judge whether a claim is supported"). Here it is
  stronger than unsupported: the claim is true but not on the attribution axis. The counter is satisfied by a
  C++ identifier that happens to contain "rules".
- This does not endanger the target (≥6 rows from ≥3 distinct S### rows): S153/S155–S168 supply the rest.
  It does mean the note's "26 claim rows" overstates attribution coverage by at least this row. Whether A1
  (S153, "registerRule appends each rule to m_rules") is likewise generic mechanics is outside my assignment;
  by inspection it reads the same way, so the same misfit may affect a second row — flagged, not adjudicated.

## 6. Verdict

VERDICT: partial — the S154 pin, sha256, byte count, committed fetch bytes and anchor all hold exactly
(independently re-fetched: `ee1b0e64…de19`, 707 B, byte-identical; remote/tag and local clone both resolve
`efb5099…`); A2's quote occurs verbatim whitespace-collapsed and its claim is true of the bytes with no
overreach, so (a) and (b) hold; but (c) fails: A2 is an API/storage declaration with no rule-attribution
content, and it is cited by none of the note's attribution routes — it is a filler row that the frozen C1 v2
predicate nonetheless counts.

## 7. Residual risk / verification gaps

- Pin resolution tested via the local clone's object store **and** remote `git ls-remote` tag lookup; no
  force-push scenario remains untested for the tag itself.
- I did not run `c1/count.py` (counted mode re-fetches all 14 sources; outside this seat's item). The
  predicate interaction in §5 is read from the counter source at HEAD, not from an execution receipt; the
  invariant clauses (`rules` topic token, backticked-id anchor) are literal.
- No tool installs or updates were made (curl, git, coreutils, python3 pre-existing). No host commands were run
  beyond read-only git/curl; no jj, no package manager, no writes outside this report and
  `/fast/scratch/hyaku/mado-r24/w2/`.
