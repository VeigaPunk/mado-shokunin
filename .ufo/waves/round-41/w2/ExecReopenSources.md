# ExecReopenSources — wave w2 report (round 41)

Seat: ExecReopenSources. Attack target: registry rows S283–S289 (+ S037 re-open) and the Gate quotes (CORPUS.md rule 1).
Data commit read: `07f2641696b5ac73de1404ea737a9f27e9819aa1`. Detailed table and reproductions: `.ufo/waves/round-41/w2/ExecReopenSources/rows.md`.

## What I did

For every row S283..S289 and S037, re-opened the source myself: re-fetched each raw URL named in `expus/SOURCES.md`
(`curl -sSL`, all HTTP 200), compared sha256 against the fetch receipt and the row; re-fetched the S287 issue page;
re-read the saved S289 journal and re-ran the read-only `journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso` snapshot; read the S037 installed package record
(`cat /var/lib/pacman/local/xdg-desktop-portal-hyprland-*/desc`) and confirmed the tag commit/release date via the GitHub API.
Checked each Gate quote (verbatim, ≤25 words, located), each row anchor, `teaches` support, tier/kind under CORPUS.md, and the recheck cadence.

## Findings

- **S283–S285, S288, S289, S037: no defect.** Fresh fetches are byte-identical to receipts (sha256 == row digests); anchors, teaches, tiers (spec/A, code/A, code/B, docs/A, own-work/A, docs/A) are right; S289's journal census is reproducible byte-for-byte today (153 lines / 19130 B; markers at lines 78 and 117; sessions=2, adverts=78, latest=63 distinct, focus_grab=1); S037 installed record = xdg-desktop-portal-hyprland 1.4.1-2 (desc sha256 `7bf2f8be…` matches receipt), tag `cc8e5ef` (commit), released 2026-07-29.
- **F1 (minor, row-level) — S286 anchor enumeration is incomplete.** The row anchor lists nine bind branches but the implementation has a tenth: `foreign_toplevel` (`src/core/PortalManager.cpp:249`), which the entry's own §3 correctly lists and the journal confirms binds (`[toplevel] Activated, bound to 55cc6bdd08d0`, line 12). Scope/teaches "which nine it binds" counts only the nine direct `wl_registry_bind` sites. Recommend the anchor enumerate all ten branches (or state "nine direct registry binds plus a foreign-toplevel manager").
- **F3 (note) — S289 recheck=`on-change` is outside CORPUS.md's enumerated cadences** (`90d`/`180d`/`on-release`; CORPUS.md:105-106). Precedented minor systemic (round-17 ReopenS065 D3); accepted by validator policy. Not a new defect.
- **Quote precision (no content misquote):** 12/31 entry quotes are not byte-verbatim substrings — they match only under whitespace normalization (XML prose, C++ statements split across lines, README wrapping), including the GATE quotes for S283. S287's expected-behavior sentence exists only with markdown backticks (`silent`) and a longer tail (entry quote is the backtick-stripped truncated fragment). S037's gate quote is composed from two separate desc fields. All quotes are ≤25 words and faithful; this is the strict-narrow-verbatim reading of rule 1, consistent with earlier rounds' strictness notes.
- **S287 page is dynamic, benign:** fresh fetch differs from receipt only in the `fetch-nonce` meta token (first diff byte 26145; size 475169 vs 475170). Every content claim (quotes, CLOSED/COMPLETED, created `2022-08-23T14:03:55Z`, replies `2022-08-25`) is present in both.

## Reproduction highlights

- Re-fetch + `sha256sum`: S283 `0bc60c14…`, S284 `53b762f7…`, S285 `6f7cecf1…`, S286 `15c3e39c…`, S288 `3c700763…` — all equal receipt and row digests. S287 `cb60a026…` (dynamic nonce only).
- `journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso | wc -l` → 153; snapshot cmp-identical to receipt.
- `cat /var/lib/pacman/local/xdg-desktop-portal-hyprland-*/desc` → 1.4.1-2; `sha256sum` → `7bf2f8beeadf189be54460a72700f81722d9be78884a0a8ee56a46a70c9445a5`.
- API: `published_at 2026-07-29T21:06:01Z`, tag object `cc8e5ef8fb2acef3db488b9a33b0c48c2a4ee204`.
- `hyprctl version` → 0.56.2 @ `efb50993780079460b0cbed1363e2166a2de1d9f` (matches S284 pin and entry INF).
- `grep -cin 'focus' fresh/PortalManager.cpp` → 0 (rc 1); journal `focus` occurrences → exactly 1.

## Risks / blockers

- None. No tracked files edited; only my seat dir `.ufo/waves/round-41/w2/ExecReopenSources/` written. No tool installs (used curl/python3/git-readonly/journalctl-readonly). No labrat spawned; leaf-only.
- If F1 is accepted, the S286 row anchor/scope wording needs an L1 integration edit (row-level, not data bytes).

Report: .ufo/waves/round-41/w2/ExecReopenSources.md
