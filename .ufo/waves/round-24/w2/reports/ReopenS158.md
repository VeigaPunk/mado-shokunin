# Reopen S158 — HyprCtl.cpp (mined SOURCES row)

Attacked item: SOURCES.md row S158 at lane rev `39c596307333b8ca0a1e42b3f3b9a748bb8b208b` and the two claim
rows that cite it, A10 and A11, in `corpus/knowledge/rule-attribution-r24.md`. I re-fetched the pinned URL,
re-hashed the committed fetch bytes, resolved the pin through both `git ls-remote` and the local clone, and
re-read the cited lines in the pinned bytes. Nothing was edited outside this report.

Conventions: "row" = the SOURCES record; "note" = `rule-attribution-r24.md`; "bytes" = the file content at the
pinned commit. `sha256:` labelled hashes throughout.

## 1. Row record (corpus/SOURCES.md:170)

| field | value |
|---|---|
| id | S158 |
| source | HyprCtl.cpp |
| URL | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp |
| kind / status | code / mined, opened 2026-10-23, recheck `on-release` |
| claim lines | `src/debug/HyprCtl.cpp:346-484, 613-630, 647-723, 1463-1645, 2003-2044 @ efb5099…` |
| sha256 (row) | `sha256:798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa` |
| bytes (row) | 97582 B |
| used-by | corpus/knowledge/rule-attribution-r24.md |

The row is byte-identical at `39c5963` and in the worktree; the note is likewise byte-identical
(`sha256:90a15fb89dd74a2f77ebf2c700354208f8f664f8394e61ad0fa216c283b25f66` at rev = worktree), and the A10/A11
lines match exactly at both places.

## 2. Independent fetch vs row vs committed fetch bytes

- `curl -sSL` of the pinned raw URL (exit 0) → `/fast/scratch/hyaku/mado-r24/w2/s158/S158.raw`:
  **97582 bytes**, `sha256:798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa` — equal to the
  row's hash and byte count.
- `cmp` against `.ufo/waves/round-24/fetch/S158.bin` → **IDENTICAL**.
- Committed blob at the lane rev: `git show 39c5963:.ufo/waves/round-24/fetch/S158.bin | sha256sum` →
  `798b7c6c…91fa`, 97582 bytes. The committed bytes are exactly the pinned-URL content; no self-made bytes.
- Three-way agreement: **row = committed fetch = live raw fetch**.

## 3. Pin resolution

- Remote: `git ls-remote https://github.com/hyprwm/Hyprland refs/tags/v0.56.2` →
  `efb50993780079460b0cbed1363e2166a2de1d9f refs/tags/v0.56.2`. The 40-hex pin is the v0.56.2 tag tip.
- Local clone `/fast/scratch/hyaku/mado-r24/src/Hyprland-v0.56.2` (`origin` = https://github.com/hyprwm/Hyprland):
  `git cat-file -t efb5099…` → `commit`; `git tag --points-at efb5099…` → `v0.56.2`;
  `git show efb5099…:src/debug/HyprCtl.cpp | sha256sum` → `798b7c6c…91fa`, 97582 bytes. Clone blob = refetch.
- The pin is a commit, not a moving branch: no re-point risk inside this recheck.

## 4. Frozen-counter interaction (diagnostic only)

`python3 -I .ufo/waves/round-24/c1/count.py 39c5963… --offline` (diagnostic; the counted mode is the receipt
mode) returns **A10 PASS_ROW, A11 PASS_ROW**, `PASS_ROW=23/26`, `distinct_sources=14`, `readme_indexed=True`,
`TARGET_MET`. For S158 the `--offline` path reads the committed bin, whose hash I independently matched against a
live raw fetch above, so the offline pass for A10/A11 is corroborated by network bytes, not merely assumed.
I did **not** run the counted (re-fetch-all) mode; that is the C1 seat's receipt, not this item.

## 5. Per-row judgments

### A10 — "Each `clients` JSON entry includes its tags, sourced from that window's `m_ruleApplicator` tag keeper."

Quote: `const auto tags = w->m_ruleApplicator->m_tagKeeper.getTags();`

- **(a) verbatim: holds.** Byte-exact single-line occurrence, 1 hit, `src/debug/HyprCtl.cpp:347`; 5 words,
  whitespace-collapse also 1 hit; 0 altered characters.
- **(b) true, no overreach: holds.** `clientsRequest` (458-484) loops windows and calls
  `CHyprCtl::getWindowData` per window (467, 478). `getWindowData` is 376-456; its JSON branch (376-435)
  declares `"tags": [{}]` at :415 and fills it with `getTagsData(w, format)` at :433. `getTagsData` (346-354)
  starts with exactly the quoted line and folds the keeper's tags into a comma-separated list. So every JSON
  entry that is emitted carries the key, and its values come from `w->m_ruleApplicator->m_tagKeeper` — the
  claim's exact
  wording. No overreach: the claim is restricted to JSON entries (normal format also carries `tags: {}` at
  :452, which does not weaken it), and it makes no claim about which rule assigned a tag. The only scope limit
  (unmapped windows are skipped unless the request passes `all`, :461-463) does not touch "each entry".
- **(c) attribution content: holds.** The row locates the tag observable's source in the rule applicator's tag
  keeper. That is the substrate of the note's positive attribution route ("give the rule a unique `tag` effect,
  then read `tags` in `hyprctl clients`") and is used that way in the note's answer table; the note is explicit
  that per-rule provenance is still not observed, so the row is not stretched into an identity claim.

**A10: holds on (a), (b), (c).**

### A11 — "The `getprop` opacity branch tests `PROP` and passes the selected window's `m_ruleApplicator` alpha to `alphaToString`."

Quote: `if (PROP == "opacity") return alphaToString(PWINDOW->m_ruleApplicator->alpha(), true);`

- **(a) verbatim (whitespace-collapsed): holds, with a transparency note.** There is **no** exact single-line
  substring (byte-exact count 0) because the source spans two lines:
  `:1565  else if (PROP == "opacity")` / `:1566      return alphaToString(PWINDOW->m_ruleApplicator->alpha(), true);`
  The quote joins them with one space and drops the leading `else`. Whitespace-collapsed count = 1; no character
  inside the quoted fragment is altered. This satisfies the frozen v2 predicate ("occurs verbatim
  (whitespace-collapsed)") and is a contiguous source fragment, but it is not a single-line byte-exact quote —
  anyone restating the round as "single-line exact quotes" would be wrong about A11.
- **(b) true, no overreach: holds.** `dispatchGetProp` spans exactly 1463-1645 (closing brace at :1645).
  `PWINDOW` is the selector result `Desktop::viewState()->query().selector(WINREGEX).runWindow()` at :1472
  (guarded by `window not found` at :1474-1475), so "the selected window" is literal. `alphaToString` is the
  lambda declared at :1493 taking `COverridableVar<SAlphaValue>& alpha, bool getAlpha`; the branch at :1565-1566
  passes `PWINDOW->m_ruleApplicator->alpha()` and `true`. The command is registered as
  `{"getprop", false, dispatchGetProp}` at :2032. The claim omits the `true`/`getAlpha` flag and does not say
  which of the two values is rendered — omissions, not contradictions.
- **(c) attribution content: holds (negative half).** The claim shows that the readable opacity is the rule
  applicator's merged `COverridableVar` value. The note's answer table uses A11 for exactly the row "applied
  value of one property … what it shows: the applicator's current value … what it does not show: which rule, or
  whether a rule set it at all". The claim sentence itself is a read-path fact rather than an identity claim;
  the attribution conclusion lives one line up in the note, and the note states that conclusion correctly. If
  someone presented A11 alone as proving "no rule identity is exposed", that would need the note's other rows
  (A5-A8); the note does in fact lean on them, so no overreach in the note as written.

**A11: holds on (a) under the frozen collapse rule, (b), and (c) as the negative-half route.**

## 6. Row-level prose and anchors

- Anchors checked against the bytes: 346-484 = `getTagsData` :346-354 through `clientsRequest` :458-484
  (closing brace :485); 613-630 = `workspaceRulesRequest` :613-630 (closing brace :631, final brace outside the
  range); 647-723 = `layersRequest` :647-723 (closing brace inside the range); 1463-1645 =
  `dispatchGetProp` exactly; 2003-2044 = the `CHyprCtl::CHyprCtl()` registration block (`workspacerules` :2005,
  `clients` :2007, `layers` :2010, `getprop` :2032, `startHyprCtlSocket()` :2044). All five ranges land on the
  described material; `layersRequest` closes at :723 and the constructor holds 39 `registerCommand` calls.
- Row description "`clients` JSON tags, `getprop` property response, `layers` output, registered rule-list
  commands": all four are present in the bytes at the cited ranges.
- Row note "no dedicated window/layer attribution verb appears in the registration sweep": the constructor
  registers 39 commands; there is no window-rule or layer-rule listing verb, and `workspacerules` covers
  workspace rules only (`getAllWorkspaceRules()`). True as scoped ("in the registration sweep").
- The note's negative-sweep citation `src/debug/HyprCtl.cpp:1548-1553` for "getprop renders the applicator
  value" lands exactly on the `windowPropToString` lambda (:1548-1553), which renders `prop.valueOrDefault()` —
  accurate, not an off-by-N anchor.

## 7. Adjacent observation (not scored here)

The 3 non-passing rows in the offline counter run are A5, A7, A8, all failed as `quote-off-topic` — a
`TOPIC_RE` word-boundary artifact on quotes built from identifiers such as `PRIORITY_WINDOW_RULE`,
`RULE_PROP_NONE` and `m_dynamicTags` (underscores defeat `\brules?\b`). That is a counter-scope limit, not a
defect in those rows, and it does not involve S158. Recorded only because it explains the 23/26 headline without
the rows being wrong.

## 8. Verdict

VERDICT: holds

S158 holds end to end: the live raw fetch reproduces the row's `sha256:798b7c6c…91fa` and 97582 B, byte-identical
to the committed `fetch/S158.bin` and to the clone blob at `efb5099…`; the pin resolves as the `v0.56.2` tag tip
by both `git ls-remote` and the local clone; both citing rows (A10, A11) quote real bytes and state true,
non-overreaching facts; both are used by the note as attribution-route evidence (positive tag route, and the
negative applied-value route), with the caveat that A11's quote is a two-line whitespace-collapsed fragment that
drops a leading `else`, and A11 is the weaker of the two on attribution content because its conclusion lives in
the note's answer table rather than in the claim cell.

## 9. Residual gaps

- A11's quote is not single-line byte-exact (see §5a). Under the frozen predicate this is allowed; recorded so
  the round is not described as "byte-exact quotes" without qualification.
- A10/A11 were judged against the source read path only. Whether the host actually emits `tags` for every window
  and what `getprop opacity` returns live is out of this item (the note's host join says 4/4 windows carry the
  key, key list only).
- No counter counted-mode run; the S158 row's network leg was verified by my own curl, which is the same
  operation counted mode performs for this row.
- No tool installs or updates were made (curl, git, coreutils, python3 pre-existing). No host commands beyond
  read-only file/git/curl work; no package manager, no jj, no writes outside this report and
  `/fast/scratch/hyaku/mado-r24/w2/s158/`.

