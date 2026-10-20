# ReopenS069 — falsification report (hyprlock README row)

Item: S069 `hyprlock README @ v0.9.6` —
https://raw.githubusercontent.com/hyprwm/hyprlock/v0.9.6/README.md
(lines 5, 19; sha256 `83096def1a9760088ee6508d550f9498aab959176ae50f90720a57fe838f50f3`).
Lane HEAD attacked: `988b858bd6049bc709807534fd725c05264f7e60`
(`git rev-parse HEAD`, read-only). No lane mutation; no installs (report at end).

## Axes attacked

1. Byte reproducibility — fresh fetch vs the recorded digest.
2. Anchor truth — is the gate quote / line-19 claim actually at the stated lines.
3. Citation fidelity — every claim the `used-by` note makes from S069.
4. Row contract — kind/tier/status/columns/census and the round-17 gate line.
5. Load-bearing — does any C2 claim depend on this row being right.

## Evidence (read-only; commands and results)

- Fetch 2026-10-20: `curl` → HTTP 200, 1458 bytes, 60 lines.
  `sha256 83096def1a9760088ee6508d550f9498aab959176ae50f90720a57fe838f50f3`
  — scripted equality with `corpus/SOURCES.md:81` and `corpus/lessons/round-17.md:56`
  (`row digest ok True` / `gate digest ok True`), not eyeballed.
- Line 5 exact bytes: `" - Uses the ext-session-lock protocol"` — gate quote
  `Uses the ext-session-lock protocol` is an exact substring; no negation or
  qualifier is elided by the quote.
- Line 19 exact bytes: `[See the wiki](https://wiki.hyprland.org/Hypr-Ecosystem/hyprlock/)`
  — the file's only wiki link (`grep -n wiki` → line 19 only); target is the
  hyprlock page, not hypridle.
- "Older wiki domain" corroborated live: `curl -I https://wiki.hyprland.org/Hypr-Ecosystem/hyprlock/`
  → `HTTP/2 301`, `location: https://wiki.hypr.land/Hypr-Ecosystem/hyprlock/`
  (2026-10-20 14:54 UTC). The old domain is a legacy alias, so the row's
  "older domain" wording is observed behaviour, not adjective drift.
- Tag binding: `curl -I https://github.com/hyprwm/hyprlock/archive/refs/tags/v0.9.6.tar.gz`
  → `302` to `codeload.github.com/.../refs/tags/v0.9.6`; a `refs/tags/v0.9.6`
  ref exists, so the raw URL is tag-pinned, not a branch of the same name.
- Row shape: 11 columns; contract census awk → `malformed rows: 0`; registry
  70 rows / 70 unique ids; no second S069 and the URL appears once in SOURCES
  and once in the lesson. Counts are computed from the lane-HEAD bytes
  (`git show HEAD:corpus/SOURCES.md`, sha256 `931a8375b88e7936b84c9f49f72ef40cceb478f93b885d1d40642b2ce7fa0f60`).
- Workspace observation (not a finding): a sibling seat appended an
  uncommitted `S071` row to `corpus/SOURCES.md` while this check ran. S069 is
  byte-identical at HEAD and in the worktree, so no verified byte above moved.
- Round arithmetic recomputed from the registry: tier A 63 / C 6 / B 1; status
  mined 55 / queued 8 / rejected 7 — matches the lesson's claimed
  `55 → 70, A 51 → 63, C 3 → 6, mined 43 → 55, rejected 4 → 7, queued 8`.
- Tier A: contract (kaika SOURCES-CONTRACT-v1 §Shape) admits "official docs"
  as A; the row is the project's own README at a pinned tag, same shape as
  sibling S065 (hypridle README, A).
- Scope verified in bytes: features lines 4-12 (line 5 quoted), docs pointer
  line 19, build deps lines 30-44 (cairo, hyprgraphics, hyprlang, hyprutils,
  hyprwayland-scanner, mesa, pam, pango, sdbus-cpp >= 2.0.0, wayland-client,
  wayland-protocols, xkbcommon). File has LF endings (0 CR bytes).

## Citing-note check (`corpus/knowledge/idle-lock-route-r17.md`)

- line 25: legend `[LR:n]` = file line of this exact URL — anchor semantics
  are declared, so `[LR:5]`/`[LR:19]` are correctly interpretable.
- line 1: `S069 …/hyprlock/v0.9.6/README.md (Features, Docs)` — the two sections
  named are exactly the two lines used.
- line 61: `Protocol: "Uses the ext-session-lock protocol" [LR:5]` — verbatim,
  exact anchor; no stronger protocol claim (version, compositor support,
  behaviour) is attributed to S069.
- line 62: `Drift: hyprlock README links the wiki at wiki.hyprland.org [LR:19]`
  — verbatim domain, exact anchor; marked "Documentary only", consistent with
  the round's no-observation boundary.
- No other `S069` or `[LR:*]` citation exists in the lane (grep over `corpus/`
  and `.ufo/waves/round-17/`, excluding this report). `corpus/README.md:42`
  cites the range S063–S069, consistent with this row's existence and P6 use.

## Two observations that do not falsify (recorded, not counterexamples)

N1 — the gate's parenthetical counts the line, not the quote. `(5 words)` equals
`wc -w` of the full line including the Markdown bullet (`-` counts as a token);
the quoted text alone is 4 tokens. Same convention reproduces sibling S056
(fetched `v0.14.3` README:166 `- Each entry…` → 12 tokens; quote alone → 11;
the lesson says 12). The ≤25-word gate holds under either count. No claim in
the row or note depends on the count.

N2 — scope/anchor asymmetry: the scope cell names build deps, but the anchor
cell records only lines 5, 19. The deps are present at 30-44 (verified above).
The contract requires the anchor, and the gate quote, to ground `teaches`
(SOURCES-CONTRACT-v1 Rule 1), and `teaches` is fully anchored at 5 and 19; so
this is an anchor-completeness nit, not a false claim or a contract breach.

## Load-bearing check (replicated predicate; not a `measure.py` run)

`measure.py` credits P6 only if a head `source:` token resolves to a row that is
mined, tier A, lists the note in `used-by`, has an `https://` source, kind
docs/spec/code, and a P6 keyword (`hypridle|hyprlock|idle|session-lock`) in its
source+scope cells. Replaying that predicate over SOURCES.md gives
`S063, S064, S065, S066, S067, S068, S069`. Deleting S069 leaves six
qualifiers, so C2's P6 credit is not single-sourced on this row: even a
hypothetical S069 defect could not flip P6. [INFERENCE from the read predicate
plus computed row set; no measurement executed here by assignment.]

## Verdict

Attack failed. No counterexample exists for S069's URL, digest, quote, anchor,
tier, status, scope, or for any claim the citing note makes at `[LR:5]` and
`[LR:19]`; the gate line reproduces exactly and the tag is real. The two nits
above are labelling/completeness issues that change no admitted claim.

Residual unknown: whether `v0.9.6` is an annotated or lightweight tag — the
GitHub API answered `rate limit exceeded` for unauthenticated `git/ref/tags`;
tag existence is independently shown by the archive ref, and the distinction
does not affect any row claim.

Installs: none. Files written by this seat: this report only. No git/jj
mutation, no package/system/compositor probes; host files untouched.
