# RevFetchReceiptContract — fetch-receipt rule review (round 18)

author: MadoR18.RevFetchReceiptContract (reviewer, non-author)
date: 2026-10-20
revision audited: `d3a0000` plus the uncommitted `.ufo/waves/round-18/fetch/`
tree as it stood at 15:39–15:53Z (297 receipts at the verifier run, 301 at the
last count, 21 seat dirs; seats kept writing while this review ran). The lane
has not integrated yet, so every receipt below is worktree state, not a
committed revision; the closure command is written to read a revision.

## TL;DR

- **A seat can fabricate a receipt; nothing in `mado-fetch-receipt-v1` stops
  it.** Every field is self-asserted and the body is seat-authored bytes. What
  makes a receipt *checkable* is external to the JSON: a committed body whose
  sha256 and byte count match the receipt, a URL on a host the seat cannot
  write, and a closure-time re-fetch of that URL (or of the tag's commit URL)
  returning the same bytes. The row's anchor sha and quote then bind the
  receipt to the claim.
- **The landed verifier does not yet implement the external half, and has two
  blocking join holes.** `.ufo/waves/round-18/fetch-verify.py` never reads
  `http_status` (`:57-96`, `:206`): a 404/error page is a verified `ok`
  receipt, and a row can be `receipted` by URL alone (`:226-233`) or by a
  borrowed sha alone. Live at the 296-receipt snapshot:
  `SUMMARY receipts=296 ok=296 bad=0` while five receipts are 404s. In a /tmp
  fixture a 404 URL produced `ROW S099 receipted` + `QUOTE S099 ok` + exit 0,
  and a row naming a different URL but carrying another receipt's sha produced
  `ROW S902 receipted` + exit 0.
- **No tag→commit binding exists.** 0 receipts carry `tag_commit` (0 at 297
  and at 301); 196 raw
  URLs are tag refs and 14 are commit refs. A closure that re-fetches the tag
  sees a digest mismatch when a tag moves, but cannot tell a moved tag from a
  corrupted receipt unless it resolves `git ls-remote` and fetches the commit
  URL. The rule says "record the tag→commit" but the schema has no field for it.
- **The verification act is itself unreceipted.** `fetch-verify.py` reads the
  worktree (`Path.glob`) and prints no `tool_sha256` or `measured_commit`. That
  is the R17-V1 class again: a verifier output with no revision binding.
- **Host ownership is unpoliced.** `measure.py:254-258` accepts any `https://`
  source cell of kind docs/spec/code containing the surface keyword.
  `benz.gitbook.io` (third-party GitBook) passed "walker" in this wave; the
  fetch layer cannot repair a mis-tiered row. C2 needs an official-host rule
  or an L1-recorded ownership justification.
- **Storage consistency is clean.** 297–301 receipts, 292–296 `ok`, 5 `negative`
  (404), 0 sha/bytes/missing mismatches under a stricter local check. That
  proves receipt↔body consistency, not provenance; provenance is the re-fetch
  plus the upstream host.

Verdict: **the v1 rules are a necessary paper trail, not yet a checkable
one.** Blocking for C2 until (a) `fetch-verify.py` gates on `http_status` and
requires sha **and** target for a row, (b) every tag receipt records
`tag_commit`, and (c) the closure command below is run at the integrated
revision and its output committed.

## 1. What a receipt can and cannot prove

| layer | evidence | proves | does not prove |
|---|---|---|---|
| storage | committed body + receipt sha/bytes | the body bytes exist in the lane and the JSON describes them | that the body came from the URL |
| upstream | re-fetch of `url` (and `final_url`) at closure | the same bytes are served by that URL now | that the seat fetched them, or when |
| version | tag→commit + re-fetch of `raw.../<commit>/...` | the bytes are the content of that commit | that the tag pointed there at fetch time unless `tag_commit` was recorded |
| claim | row anchor full sha + byte count + quote at declared anchor | the row cites these bytes and this sentence | that the sentence is current upstream (volatile pages) |
| act | `fetched_at`, `tool` | a self-declared time and client | nothing independently; no trusted timestamp |

For immutable content (raw commit, raw tag + recorded `tag_commit`, a released
crate file), upstream + version layers are strong. For HTML docs, wikis,
GitHub release pages, AUR pages, GitBooks, and generated archives, the digest
is a snapshot, not a reproducible identity: the committed body + declared
anchor is the evidence, and the re-fetch can only report drift.

## 2. Blocking findings (fix before the C2 closure uses receipts)

### F1. `http_status` is ignored; a 404 error page is a verified receipt

`fetch-verify.py:57-96` checks schema, body existence, bytes, sha. It never
reads `http_status`; `:206` counts only that local status. Live run at the
296-receipt snapshot printed `SUMMARY receipts=296 ok=296 bad=0`, including:

| receipt | status | bytes | body |
|---|---|---|---|
| `NoteTheme:6` | 404 | 195690 | GitHub HTML error page (`github.com/swaywm/swaybg/tree/v1.2.2/doc`) |
| `NoteTheme:7` | 404 | 14 | `404: Not Found` |
| `NoteTheme:15` | 404 | 14 | `404: Not Found` |
| `SrcElephantProviders:19` | 404 | 14 | `404: Not Found` |
| `SrcThemeAlternates:5` | 404 | 0 | empty (Arch Wiki raw missing) |

Row join (`:226-233`) uses those verified receipts without a status gate, and
the quote search (`:240-265`) searches any matched body. Fixture proof: a
receipt with `http_status:404`, body `404: Not Found`, URL
`.../walker/v2.17.2/nope`, and a SOURCES row naming that URL produced:

```
FETCH Forger/nope ok
ROW S099 receipted
QUOTE S099 ok
SUMMARY receipts=1 ok=1 bad=0 rows=1 unreceipted=0 quotes=1 quote_bad=0
(exit 0)
```

A 404 page can therefore satisfy a row and even its quote if the quote text is
error-page text. This is exactly the R17-V3 "invented row" class.

Fix: `http_status == 200` is required for credit; 4xx/5xx/3xx are `negative`
receipts (honest failures, never row support). Quote search only over 200
bodies. Add `FETCH ... negative` to the output and keep negatives out of
`ROW receipted`.

### F2. Row join is `sha-in-anchor OR url-equal`; each disjunct alone is forgeable

`fetch-verify.py:229-233`:

```python
if isinstance(sha, str) and sha and sha in anchor:
    matched.append(entry)
    continue
if rec.get("url") in urls or rec.get("final_url") in urls:
    matched.append(entry)
```

- **URL-only** is F1: a 404/wrong body with the right URL passes.
- **SHA-only** lets a row name URL A while copying the sha of a receipt for URL
  B. The bytes are real, but not at the named source. Fixture proof: row S902
  names `raw.../walker/dddd.../none` and carries the sha of
  `raw.../walker/aaaa.../README.md`; the landed verifier printed
  `ROW S902 receipted` and exit 0.

Fix: require **both** (i) the row anchor sha equals the receipt sha (full 64
hex or a >=16-hex prefix) and (ii) the row URL names the same canonical target
as `url`/`final_url` (`raw.githubusercontent.com/<owner>/<repo>/<ref>/<path>`
or `github.com/<owner>/<repo>/{blob,raw,tree}/<ref>/<path>`, compared on
owner/repo/ref/path). No anchor sha → `UNRECEIPTED` (not "trust the URL").
Host rows with no https URL (S059/S060/S071 pattern) are not fetch rows: skip
them in the fetch join and verify them as file bytes at the revision.

### F3. No URL→sha consistency rule; a forged body for a real URL passes

`fetch-verify.py` has no cross-receipt check. CriticC2 already demonstrated a
forged body saved under the real walker README URL: when merged with the
genuine `NoteWalker/` receipts for that URL, the run stayed `ok` (28/28) and
the URL→sha conflict was silent. With two or more seats fetching the same
tag/raw URL, disagreement is a strong tamper signal and costs nothing to check.

Fix: group by (normalized) `url` (and by `final_url`); if two receipts for the
same URL carry different sha256, print `URLCONFLICT <url>` and exit 1. For the
load-bearing C2 row, prefer the sha that >=2 independent seat dirs agree on
(the current wave already has such agreement for walker README/config and
omarchy theme-set/bg-next); a single-seat URL is acceptable only when the
closure re-fetch matches it.

### F4. No tag→commit binding in the receipt

The rule says "record the tag→commit via `git ls-remote`" (`gen_w1.py:32`),
but `mado-fetch-receipt-v1` has no field for it and none of the 297 receipts
contains one. The wave has 196 raw tag refs vs 14 commit refs. Consequences:

- Re-fetch at a tag is a pointer read. If the tag moves, the digest differs;
  without the commit you cannot distinguish "tag moved" from "body corrupted".
- A closure-time `ls-remote` records the commit *now*, not the commit the seat
  read. It is a post-hoc pin, still useful, but not proof of the fetch.

Fix: add `tag` and `tag_commit` (and the peeled/tag-object if annotated) to the
receipt for every raw tag URL. The closure resolves `refs/tags/<tag>` and
`refs/tags/<tag>^{}`, requires the recorded commit to match, fetches
`raw.../<commit>/<path>`, and reports `TAG_MOVED` when the tag URL digest
differs but the commit URL digest matches the receipt. This is implemented in
Appendix A and tested with a fake tag move.

### F5. The verifier reads the worktree and prints no revision

`fetch-verify.py` uses `Path(fetch_root).glob` and never resolves a git
revision; its output has no `measured_commit` and no tool sha. Run after the
worktree changes and the receipt of the verification no longer describes the
measured bytes. This is the R17-V1 pattern (receipt without
`tool_sha256`/`measured_commit`) applied to the verifier itself.

Fix: read every receipt and body with `git show <REV>:<path>` at a named
revision, print a first line
`RECEIPT tool=mado-fetch-closure.py tool_sha256=<hex> measured_commit=<full> utc=<Z>`,
and write the output to a committed evidence path at the integrated revision.
Appendix A does this; `fetch-verify.py` should adopt the same header and a
`--rev` option (or be retired in favor of the closure script).

## 3. Rule-level gaps: fabrication, variance, redirects, size

### F6. Redirects are recorded but never re-checked

30/297 receipts have `final_url != url`:

| pair | n | cause observed |
|---|---|---|
| `github.com` → `raw.githubusercontent.com` | 17 | `github.com/<owner>/<repo>/raw/...`; the omarchy org moved `basecamp` → `omacom`, so final is `raw.githubusercontent.com/omacom/...` |
| `api.github.com` → `api.github.com` | 6 | `/repos/basecamp/omarchy/...` redirects to `/repositories/994093166/...` |
| `github.com` → `github.com` | 4 | tree/discussion pages normalize the path |
| `www.ssp.sh`, `wiki.hypr.land`, `benz.gitbook.io` | 3 | trailing-slash normalization |

`curl -sSL -w '%{http_code} %{url_effective}'` records the final URL but not
the redirect count, and the rule does not require the closure to compare it.
A redirect can land on a login/consent/404 page with HTTP 200; only the quote
or digest check catches that. A seat can also transcribe any `final_url`; the
re-fetch is the first place the lie is exposed.

Fix: re-fetch `url` with `--proto '=https' --proto-redir '=https'
--max-redirs 5`, compare the effective URL to `final_url` (exact, modulo a
trailing slash), and on non-200 fall back to `final_url` (old-org routes may
expire). Record `num_redirects` in v2. Never accept a `final_url` with
userinfo or a token query.

### F7. Per-fetch variance by source class (the digest is not one policy)

| class | snapshot count | digest reproducible on re-fetch | closure policy |
|---|---|---|---|
| raw commit | 14 | yes (commit immutable) | exact sha |
| raw tag | 196 | until the tag moves; tag is a pointer | resolve tag→commit; exact sha at commit; `TAG_MOVED` if tag differs |
| `api.github.com` ref/commit/tree | 21 | yes for the body; 60 req/h unauthenticated; `truncated:true` possible | exact sha; `truncated` must be false for a complete-listing claim; 403/429 = exit 2 |
| `github.com` HTML (release/tree/discussion) | 23 | no (markup/nonces/relative dates) | volatile: quote in committed body; report drift |
| wiki/learn.omacom/docs.rs/AUR/Arch wiki/GitBook/market/ssp/YouTube oEmbed | ≈45 | no (live pages/APIs) | volatile: quote in committed body; drift is freshness, not evidence failure |
| `static.crates.io` crate archive | 1 | yes for a published version | exact sha |
| `codeload.github.com` tar.gz | 1 | **not guaranteed** (generated archive) | archive/volatile; pin member file hashes, never the tarball alone |

The schema has no `kind` field, so every checker has to guess by host/path.
Add `kind` (`raw` | `api` | `html` | `archive`) and make the re-fetch policy
explicit. A codeload tarball at a tag is not the same evidence as a raw file at
that tag; it is a generated container.

### F8. Size cap is unenforced and truncation is unchecked

The rule caps each body at 1 MiB (1,048,576 bytes) and says "skip and report
larger bodies". No checker enforces it; `fetch-verify.py` would accept a
5 MiB body. Current largest body is 401,538 B (`tree.json`); the codeload
tarball is 165,438 B. A partial download (`curl` rc 18/28/63) can leave a
short body whose sha/bytes are self-consistent; the rule does not forbid it.
GitHub tree JSON can also carry `"truncated": true`, which a hash check cannot
see.

Fix: reject `bytes > 1048576`; use `--max-filesize 1048576` and treat curl
exit 63 as `TOO_LARGE`; do not record partial/range fetches as receipts (or
label `partial: true` and never use them for a complete-file claim); require
`truncated == false` in committed tree JSON; skip and report larger sources
instead of truncating.

### F9. The literal slug regex is already violated by valid evidence

The rule's `slug = [a-z0-9._-]+` is violated by 13 receipts at the 297
snapshot (14 at 301):
`README.md`, `Cargo.toml`, `Cargo.lock`, `swaybg-v1.2.2-README.md`,
`elephant-v2.22.1-README.md`, `*.body`, etc. The security property is not
lowercase; it is "one basename inside the seat dir, no `/`, no `..`, a regular
file". A strict checker written to the letter would reject this wave's real
bodies.

Fix: define `body` as `[A-Za-z0-9][A-Za-z0-9._-]*` with no `..`, no `/`, no
leading dot; require the path resolves to a regular file (not a symlink) in
the same seat dir; require unique (seat, body) with one sha. Keep case.

### F10. "Quote at a body line" is ambiguous for HTML

The rule says "Quote ≤25 words verbatim with a body line anchor". For
`wiki.hypr.land` the committed body is raw HTML, but the round-17 rows' anchors
are lines of the tag-stripped `<article>` text (`S063`/`S064` anchor cells say
so). Test on the backfilled bodies:

- `S063` quote `command to run when receiving a dbus lock event`:
  `mode=text` (tag-strip + entity-decode + whitespace collapse) → `receipted`;
  `mode=line, line=13` (raw HTML line) → `QUOTE_MISSING`.
- `S066` quote `if (MEMBER == "Lock") {` at raw file line 473 → `receipted`.

So a closure that assumes one coordinate system either false-fails HTML rows or
cannot claim line precision. The note must declare the anchor coordinate per
source (`file-line` vs `article-text`), or commit a normalized text derivative
with its own sha and the command that produced it. The quote check must select
the corresponding mode; `line` on raw HTML is not a valid check.

### F11. Host ownership is the remaining "upstream" hole

`measure.py:254-258` requires only that the row's source cell contain
`https://`, that kind is docs/spec/code, and that the surface keyword appear in
source or scope. `SrcWalkerDocsSite`'s 11 receipts include 6 on
`benz.gitbook.io/walker/` (third-party GitBook); `omarchytheme.com` (2),
`omarchythemes.dev` (2), `omarchypulse.com` (1), `draculatheme.com` (1) and
`www.ssp.sh` (1) are also third-party. A row for the third-party GitBook with
kind `docs`, tier `A`, scope containing "walker" satisfies T4 and can carry P3
by itself.

Receipts cannot fix this: a third-party page can be fetched honestly. The
closure must either require an official project host for the T4 row
(`raw.githubusercontent.com/<project>/<repo>`, `github.com/<project>/<repo>`,
or the project's official docs domain) or require L1 to record the ownership
judgment in the row. Recommend an explicit host allowlist for T4 with an L1
escape recorded in `teaches`/`scope`; do not let "any https" stand for
"upstream".

### F12. Round-17 backfill and host rows

`FetchBackfillR17/` now has 10 receipts for `S056-S058` and `S063-S069`; the
bodies match the recorded row shas (e.g. S056 `c7a1a8bb…` 14762 B, S063
`b45c03dc…` 254750 B). This is the offline half of R17-V3 for those rows and
should be credited; it does not retroactively prove the round-17 fetch act, and
the receipts still have no `tag_commit` (S056/S057/S058 are tag URLs).
`S059`, `S060`, `S071` are host-file rows with no https URL; the rule correctly
does not fetch them, but `fetch-verify.py` prints them `UNRECEIPTED`. That is a
false failure for host rows. The closure skips them (prints
`ROW ... host/no-url`) and checks their file sha separately.

### F13. Orphans and "append-only" before the commit

Five bodies are not referenced by any receipt at the snapshot
(`MadoR18.SrcWalkerThemes/walker-ls-remote-v2.17.2.txt`,
`walker-tree-api.json`, `SrcOmarchyThemeHooks/tree.json`,
`SrcOmarchyWalker/git-ls-remote-tags.txt`, `FetchBackfillR17/quote-check.json`).
They are not evidence and should not be read as such. More important: the whole
`fetch/` tree is still untracked (`?? .ufo/waves/round-18/fetch/`), and
`.gitignore` contains only `.ufo/interactive-sessions/` and `.ufo/state/`.
"Append-only" is nominal until L1 commits; only the final commit is a witness,
and git history will not show whether a seat rewrote a line before that commit.
The closure must read the committed revision, not the worktree.

### F14. Time/tool fields, and what "fabricated" still passes

All receipts at the snapshot carried times in the 15:40–15:52Z window and
`curl 8.23.0 (x86_64…)`;
the format and round window checks are clean. A seat can still write any time
inside the window and any curl version; there is no trusted timestamp. A
fabricated body with a real upstream URL is defeated only by re-fetch; a
fabricated body on a host the seat controls (own GitHub repo, gist, personal
site) is confirmed by re-fetch and is not a provenance tie at all. The v1 rule
says "no session/private URLs" but does not forbid seat-controlled hosts.

Fix: deny gist/pastebin/terminal-upload hosts, require an official project host
for load-bearing rows, and treat "unknown host" as a warning that L1 must
justify. Accept that time/tool remain self-asserted; do not cite them as
independent facts.

## 4. Snapshot audit (15:39–15:51Z, worktree)

| check | result |
|---|---|
| receipts / seat dirs | 297 at 15:51Z; 301 at 15:53Z / 21 |
| local consistency (schema, body, bytes, sha) | 0 bad; 292 ok + 5 negative |
| negative statuses | 5 × 404 (listed in F1) |
| `final_url != url` | 30 (F6) |
| tag refs / commit refs | 196 / 14 |
| receipts with `tag_commit` or commit field | 0 |
| timestamps / tool | all within 15:40–15:52Z (seats kept writing); all `curl 8.23.0` |
| largest body | 401,538 B (tree.json, under 1 MiB) |
| slug regex violations (`[a-z0-9._-]+`) | 13 at 297; 14 at 301 |
| bodies without a receipt | 5 |
| `fetch-verify.py` live result | `receipts=296 ok=296 bad=0`, exit 0, including the five 404s |
| C2 notes/drafts at snapshot | not written yet; the P3/P5 sources could not be audited |

The two load-bearing facts for the report: the local corpus is internally
consistent, and the landed verifier's `ok` count is not a provenance count.

## 5. Exact closure re-check command

The checker is Appendix A (tested prototype sha256
`ec2bd8f4e290e3a9a7f3f560fbd13f59f23b5c7cb9e7975e304e5153a21223e0`).
Save it as `/tmp/mado-fetch-closure.py` (or commit it as a lane tool if L1
adopts it). Run at the integrated revision, after the `fetch/` tree is
committed:

```bash
cd /home/vgpnk/Projects/shokunin/mado-shokunin
REV=$(git rev-parse refs/heads/master)          # or the closure commit
TOOL_SHA=$(sha256sum /tmp/mado-fetch-closure.py | cut -d' ' -f1)

# 1. Offline: receipt<->body, status, size, row sha+target, quotes.
MADO_TOOL_SHA="$TOOL_SHA" \
MADO_ROWS=S072,S073,S074,S075,S076,S077,S078,S079,S080,S081 \
MADO_QUOTES=.ufo/waves/round-18/fetch-quotes.json \
python3 -I /tmp/mado-fetch-closure.py "$PWD" "$REV" \
  | tee /tmp/fetch-closure-offline.txt

# 2. Upstream: re-fetch, tag resolve, final-url compare (network; no auth/cookies).
MADO_REFETCH=1 MADO_TOOL_SHA="$TOOL_SHA" \
MADO_ROWS=S072,S073,S074,S075,S076,S077,S078,S079,S080,S081 \
MADO_QUOTES=.ufo/waves/round-18/fetch-quotes.json \
python3 -I /tmp/mado-fetch-closure.py "$PWD" "$REV" \
  | tee /tmp/fetch-closure-refetch.txt
```

Exit: 0 all receipts `ok`/`negative` with every listed row `receipted` and
quote found; 1 any bad receipt, URL/ref mismatch, unreceipted row, or missing
quote; 2 could-not-evaluate (missing revision, unreadable body, tag unresolved
when needed, HTTP 403/429).

`fetch-quotes.json` is the three-way join the notes must supply: one entry per
credited row, `text` ≤25 words, and the coordinate mode:

```json
{"S072": {"text": "…", "mode": "line", "line": 84},
 "S073": {"text": "…", "mode": "text"}}
```

`line` is a 1-based line of the raw committed body (raw files, code, scd);
`text` is a tag-stripped, entity-decoded, whitespace-collapsed substring
(wiki/HTML docs); `substr` is a raw byte substring for plain text. Without a
quote entry the row fails `QUOTE_UNCHECKED` unless `MADO_QUOTES_OPTIONAL=1`.

Expected first line and tail:

```
RECEIPT tool=mado-fetch-closure.py tool_sha256=<64> measured_commit=<full sha> utc=<Z>
...
ROW S072 receipted
...
SUMMARY receipts=297 ok=292 negative=5 bad=0 errors=0 warnings=17 could_not=0
MADO_FETCH_CLOSURE: PASS
```

Tested, and what was not:

- Live worktree snapshot: `receipts=297 ok=292 negative=5 bad=0 errors=0
  warnings=17 could_not=0`, `PASS`, exit 0. This is the offline half only.
- `/tmp/rfr-fix`: 404 row → `NEGATIVE_ONLY`; borrowed-sha/different-URL row →
  `URL_MISMATCH`; wrong quote → `QUOTE_MISSING`; tampered body →
  `BYTES,SHA`; exit 1. Landed `fetch-verify.py` on the same fixture:
  `ROW S902 receipted`, exit 0 (F2).
- `/tmp/rfr-refetch` with controlled fake `curl`/`git` wrappers:
  `IDENTICAL`, `TAG_MOVED` (tag URL changed, commit URL matched the receipt),
  `VOLATILE_DRIFT`, `UPSTREAM_404`, `RATELIMIT` (exit 2).
- S063 HTML quote `mode=text` → `receipted`; same quote `mode=line` →
  `QUOTE_MISSING`; S066 raw line 473 → `receipted` (F10).
- **No live upstream re-fetch was run in this review.** Doing so would open
  web sources and require adding receipts outside my write scope; the network
  path was exercised only with deterministic fake `curl`/`git` wrappers. L1
  must run step 2 for real at closure.

## 6. Minimal contract amendments (backward compatible for this wave)

1. **Status gate.** `http_status == 200` is credit-eligible; 4xx/5xx/3xx are
   `negative` receipts and never support a row. Quote checks use 200 bodies
   only. (F1)
2. **Row join = sha AND target.** Require the row anchor's full 64-hex sha
   (or a ≥16-hex prefix) to equal the receipt sha, and the row URL to name the
   same canonical GitHub owner/repo/ref/path (or the same non-GitHub URL,
   trailing slash ignored). URL-only and sha-only matches fail. (F2)
3. **URL→sha conflict.** Two receipts for the same normalized URL with
   different sha → `URLCONFLICT`, exit 1; for the load-bearing row prefer a
   sha agreed by ≥2 seat dirs. (F3)
4. **Tag pin.** Add `tag` and `tag_commit` (plus tag-object sha if annotated)
   to every raw tag receipt; the closure resolves `refs/tags/<tag>` and
   `^{}`, fetches the commit URL, and reports `TAG_MOVED` when the tag URL
   differs but the commit URL matches. (F4)
5. **Revision binding.** Every closure output starts with
   `RECEIPT tool_sha256=… measured_commit=… utc=…` and is committed at that
   revision. (F5, criterion 24 shape)
6. **Kind/variance.** Add `kind` (`raw`/`api`/`html`/`archive`). Raw and
   published crate files require exact sha; API may be exact but is
   rate-limited and must report `truncated`; HTML/wiki/GitBook/AUR/YouTube are
   volatile (quote in committed body, drift reported); codeload archives are
   volatile/generated (pin member hashes, not the tarball). (F7)
7. **Redirects.** Record `num_redirects`; re-fetch must compare effective URL
   to `final_url`; on non-200 try `final_url`; `--proto '=https'
   --proto-redir '=https' --max-redirs 5`; reject userinfo/token queries. (F6)
8. **Size/partial/truncation.** Enforce ≤1,048,576 B; no partial/range
   receipts; `truncated == false` for complete tree listings; skip and report
   larger bodies. (F8)
9. **Body name.** Basename `[A-Za-z0-9][A-Za-z0-9._-]*`, no `..`/`/`/leading
   dot, regular file in the seat dir, unique (seat, body) with one sha. Keep
   case (the lowercase-only rule is already violated by valid evidence). (F9)
10. **Anchor coordinate.** Declare `file-line` vs `article-text` per source;
    for HTML either commit a normalized text derivative with its own sha, or
    check the quote as a normalized substring and do not claim line precision
    on raw HTML. (F10)
11. **Official-host rule for T4.** The "upstream" row must be on the project's
    own GitHub/raw or official docs host; third-party GitBook/blog/AUR/market
    pages are supplementary. Record any exception in the row. (F11)
12. **Host rows are not fetch rows.** Rows with no https URL are verified by
    `git show REV:<path>` sha, not by `fetch-verify.py`; the fetch join skips
    them (prints `host/no-url`) rather than `UNRECEIPTED`. (F12)

The landed `fetch-verify.py` can adopt (1)-(5) with small edits; (6)-(11) are
schema/consumer changes for the next wave. Until then, Appendix A is the
closure command and `fetch-verify.py` is a storage-consistency check only.

## 7. Residual risk and verification gaps

- **Act/time are not provable.** `fetched_at`/`tool` are self-declared. A
  re-fetch at closure proves current upstream bytes, not that the seat fetched
  them then. Do not cite the act as a fact; cite the body, URL, and re-fetch.
- **Volatile pages have no post-hoc proof.** A committed HTML/GitBook/AUR body
  + quote is a snapshot assertion. If the page changed, drift is expected and
  the committed body remains the only evidence; the closure reports drift but
  cannot distinguish a stale fetch from a forged one. Prefer raw tag/commit
  sources for C2's load-bearing row.
- **Tag moves before `tag_commit` exists.** The 196 tag receipts have no
  recorded commit; a closure can detect a moved tag but cannot prove the seat
  read the commit it later resolves. Treat the old rows as content-valid at
  their recorded sha, not as version-proof.
- **Seat-controlled hosts defeat re-fetch.** A gist/own repo/personal site is
  fetchable and self-consistent. The deny list catches the obvious ones;
  "unknown host" needs L1 judgment. A seat can also use a real upstream URL
  and copy bytes from elsewhere; the URL→sha conflict and multi-seat agreement
  checks are the only defenses, and neither is a proof.
- **API rate limit.** `api.github.com` allows 60 unauthenticated requests/hour;
  the closure must treat 403/429 as could-not-evaluate (exit 2), not as a
  mismatch. The wave already has 21 API receipts; a repeated closure can hit
  the limit.
- **Codeload archive.** The tar.gz digest is not a stable identity
  [INFERENCE: generated archive; the closure's first live re-fetch will show
  whether GitHub's generation is byte-stable]. Pin the extracted member file
  shas, not the tarball.
- **Interpretation of "supports a row."** The C2 counter (`measure.py`) does
  not read receipts; it credits whatever L1 types. The receipts are an external
  closure check, not part of rubric V. The C2 claim is only as strong as the
  closure actually running the command above at the integrated revision and
  committing its output; the instrument itself remains blind to an invented
  row.

## Appendix A — tested closure checker

Save as `/tmp/mado-fetch-closure.py`; sha256
`ec2bd8f4e290e3a9a7f3f560fbd13f59f23b5c7cb9e7975e304e5153a21223e0`.
It is read-only (no lane writes), stdlib-only, and runs under `python3 -I`.

```python
#!/usr/bin/env python3
"""mado fetch-receipt closure check (proposal, tested on /tmp fixtures).

Usage:
  python3 -I mado-fetch-closure.py LANE REV
env:
  MADO_WORKTREE=1      read the working tree instead of git objects (provisional)
  MADO_REFETCH=1       re-fetch every recorded URL and compare
  MADO_ROWS=S072,...   credited SOURCES rows to join
  MADO_QUOTES=path     JSON {SID: {text, mode: line|substr|text, line: N}}
  MADO_QUOTES_OPTIONAL=1
  MADO_SINCE=UTC       earliest acceptable fetched_at (default round-18 pre-reg)
  MADO_MAX_URLS=N      cap refetch (0 = all)
  MADO_QUIET=1         print only failures/negatives/summary
exit 0 all pass, 1 any bad/unreceipted row, 2 could-not-evaluate.
"""
import sys, os, re, json, hashlib, subprocess, tempfile, datetime, collections, ipaddress, html
from urllib.parse import urlsplit

LANE = os.path.abspath(sys.argv[1])
REV = sys.argv[2] if len(sys.argv) > 2 else 'refs/heads/master'
WORKTREE = os.environ.get('MADO_WORKTREE') == '1'
REFETCH = os.environ.get('MADO_REFETCH') == '1'
QUIET = os.environ.get('MADO_QUIET') == '1'
ROWS = [x.strip() for x in os.environ.get('MADO_ROWS', '').split(',') if x.strip()]
QUOTES = os.environ.get('MADO_QUOTES', '')
QUOTES_OPTIONAL = os.environ.get('MADO_QUOTES_OPTIONAL') == '1'
SINCE = os.environ.get('MADO_SINCE', '2026-10-20T15:34:00Z')
MAXURLS = int(os.environ.get('MADO_MAX_URLS', '0') or 0)

BASE = '.ufo/waves/round-18/fetch'
CAP = 1048576
SCHEMA = 'mado-fetch-receipt-v1'
REQ = ('schema', 'url', 'final_url', 'http_status', 'fetched_at', 'bytes',
       'sha256', 'body', 'tool')
KNOWN_HOSTS = {
    'raw.githubusercontent.com', 'github.com', 'api.github.com',
    'gitlab.freedesktop.org', 'wayland.freedesktop.org', 'wayland-book.com',
    'wiki.hypr.land', 'hypr.land', 'learn.omacom.io', 'docs.rs',
    'static.crates.io', 'crates.io', 'aur.archlinux.org', 'wiki.archlinux.org',
    'swaywm.org', 'omarchytheme.com', 'www.ssp.sh', 'world.hey.com',
    'www.youtube.com', 'youtube.com', 'codeload.github.com',
}
DENY_HOSTS = {
    'gist.github.com', 'gist.githubusercontent.com', 'pastebin.com', 'paste.ee',
    '0x0.st', 'transfer.sh', 'file.io', 'termbin.com', 'ix.io', 'dpaste.com',
    'dpaste.org', 'hastebin.com', 'controlc.com', 'rentry.co', 'paste.rs',
    'bin.disroot.org', 'privatebin.net', 'localhost',
}
OFFICIAL_HOSTS = KNOWN_HOSTS - {'omarchytheme.com', 'www.ssp.sh',
                                 'world.hey.com', 'www.youtube.com', 'youtube.com',
                                 'codeload.github.com'}
ALLOW_HOSTS = {h.strip() for h in os.environ.get('MADO_ALLOW_HOSTS', '').split(',') if h.strip()}
TOKEN_KEYS = {'token', 'access_token', 'auth', 'authorization', 'session',
              'sessionid', 'sig', 'signature', 'x-amz-signature',
              'x-amz-credential'}

errors, warnings, could_not = [], [], []
records = []


def out(line):
    print(line)


def pbad(where, msg):
    errors.append(where + ' ' + msg)
    out('BAD %s %s' % (where, msg))


def pwarn(where, msg):
    warnings.append(where + ' ' + msg)
    if not QUIET:
        out('WARN %s %s' % (where, msg))


def note(line):
    if not QUIET:
        out(line)


def git(args, binary=False):
    p = subprocess.run(['git', '-C', LANE] + args, capture_output=True)
    if p.returncode != 0:
        return None, p
    return (p.stdout if binary else p.stdout.decode('utf-8', 'replace')), p


entries = {}
if WORKTREE:
    root = os.path.join(LANE, BASE)
    if not os.path.isdir(root):
        out('MADO_FETCH_CLOSURE: no fetch dir at %s' % root)
        sys.exit(2)
    for dp, _dn, fn in os.walk(root):
        for f in fn:
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, LANE)
            if os.path.islink(p):
                mode = '120000'
            elif os.stat(p).st_mode & 0o111:
                mode = '100755'
            else:
                mode = '100644'
            entries[rel] = ('wt', p, mode)
else:
    data, p = git(['ls-tree', '-r', '-z', REV, '--', BASE], binary=True)
    if data is None:
        out('MADO_FETCH_CLOSURE: cannot read %s:%s (exit %s)'
            % (REV, BASE, p.returncode))
        sys.exit(2)
    for rec in data.split(b'\0'):
        if not rec:
            continue
        meta, path = rec.split(b'\t', 1)
        mode, _typ, obj = meta.decode().split()
        entries[path.decode()] = ('git', obj, mode)


def rd(path):
    kind, ref, mode = entries[path]
    if mode == '120000':
        raise ValueError('symlink: ' + path)
    if kind == 'wt':
        with open(ref, 'rb') as fh:
            return fh.read()
    data, p = git(['show', '%s:%s' % (REV, path)], binary=True)
    if data is None:
        raise IOError('git show %s:%s exit %s' % (REV, path, p.returncode))
    return data


def rd_any(path):
    if WORKTREE:
        with open(os.path.join(LANE, path), 'rb') as fh:
            return fh.read()
    data, p = git(['show', '%s:%s' % (REV, path)], binary=True)
    if data is None:
        out('MADO_FETCH_CLOSURE: cannot read %s:%s (exit %s)'
            % (REV, path, p.returncode))
        sys.exit(2)
    return data


def check_url(u, tag):
    try:
        sp = urlsplit(u)
    except Exception:
        pbad(tag, 'UNPARSABLE %r' % u)
        return False
    ok = True
    if sp.scheme != 'https':
        pbad(tag, 'NOT_HTTPS %s' % u); ok = False
    if sp.username or sp.password:
        pbad(tag, 'USERINFO %s' % u); ok = False
    if sp.fragment:
        pbad(tag, 'FRAGMENT %s' % u); ok = False
    host = (sp.hostname or '').lower()
    if not host:
        pbad(tag, 'NO_HOST %s' % u); ok = False
    elif host in DENY_HOSTS:
        pbad(tag, 'SEAT_CONTROLLED_HOST %s' % u); ok = False
    else:
        try:
            ip = ipaddress.ip_address(host)
            pbad(tag, 'IP_LITERAL %s' % u); ok = False
        except ValueError:
            pass
        if host not in KNOWN_HOSTS:
            pwarn(tag, 'HOST_UNKNOWN %s' % host)
    for k in urlsplit(u).query.split('&'):
        if k.split('=', 1)[0].lower() in TOKEN_KEYS:
            pbad(tag, 'TOKEN_QUERY %s' % u); ok = False
    return ok


def parse_time(ts):
    try:
        return datetime.datetime.fromisoformat(ts.replace('Z', '+00:00'))
    except Exception:
        return None


if not WORKTREE:
    revout, _rp = git(['rev-parse', REV])
    rev_full = revout.strip() if revout else REV
else:
    rev_full = 'WORKTREE'
tool_sha = os.environ.get('MADO_TOOL_SHA', '')
if not tool_sha:
    try:
        with open(os.path.abspath(sys.argv[0]), 'rb') as _fh:
            tool_sha = hashlib.sha256(_fh.read()).hexdigest()
    except Exception:
        tool_sha = 'UNPINNED'
print('RECEIPT tool=mado-fetch-closure.py tool_sha256=%s measured_commit=%s utc=%s'
      % (tool_sha, rev_full,
         datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')))

receipts = sorted(p for p in entries if p.endswith('/receipts.jsonl'))
if not receipts:
    out('MADO_FETCH_CLOSURE: no receipts.jsonl at %s'
        % ('worktree' if WORKTREE else REV))
    sys.exit(2)

seen_body = {}
for rp in receipts:
    seat = rp.split('/')[-2]
    raw = rd(rp)
    text = raw.decode('utf-8', 'replace')
    for ln, line in enumerate(text.splitlines(), 1):
        where = '%s:%d' % (rp, ln)
        if not line.strip():
            pbad(where, 'EMPTY_LINE')
            continue
        try:
            d = json.loads(line)
        except Exception as e:
            pbad(where, 'JSON %s' % e)
            continue
        if not isinstance(d, dict):
            pbad(where, 'NOT_OBJECT')
            continue
        badd = []
        if d.get('schema') != SCHEMA:
            badd.append('SCHEMA')
        for k in REQ:
            if k not in d:
                badd.append('MISSING_KEY_' + k)
        if 'http_status' in d and (not isinstance(d['http_status'], int)
                                   or isinstance(d['http_status'], bool)):
            badd.append('TYPE_http_status')
        if 'bytes' in d and (not isinstance(d['bytes'], int)
                             or isinstance(d['bytes'], bool)):
            badd.append('TYPE_bytes')
        if badd:
            pbad(where, ','.join(badd))
            continue
        url, fin, status = d['url'], d['final_url'], d['http_status']
        check_url(url, where + ' url')
        if fin != url:
            check_url(fin, where + ' final_url')
        else:
            check_url(fin, where + ' final_url')
        ts = d['fetched_at']
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z', ts):
            badd.append('TIME_FORMAT')
        else:
            dt = parse_time(ts)
            lo = parse_time(SINCE)
            hi = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=300)
            if dt is None or dt < lo or dt > hi:
                badd.append('TIME_RANGE')
        if not (isinstance(d['tool'], str) and re.match(r'curl \d+\.\d+', d['tool'])):
            badd.append('TOOL')
        body = d['body']
        if not isinstance(body, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', body) or '..' in body:
            pbad(where, 'SLUG %r' % body)
            continue
        bp = os.path.dirname(rp) + '/' + body
        if bp not in entries:
            pbad(where, 'MISSING_BODY ' + bp)
            continue
        if entries[bp][2] == '120000':
            pbad(where, 'SYMLINK_BODY ' + bp)
            continue
        try:
            data = rd(bp)
        except Exception as e:
            pbad(where, 'READ_BODY %s' % e)
            continue
        sha = hashlib.sha256(data).hexdigest()
        if len(data) != d['bytes']:
            badd.append('BYTES')
        if len(data) > CAP:
            badd.append('TOO_LARGE')
        if not re.fullmatch(r'[0-9a-f]{64}', str(d['sha256'])) or sha != d['sha256']:
            badd.append('SHA')
        if status == 200:
            state = 'ok'
        elif status in (403, 404, 410, 429):
            state = 'negative'
        else:
            badd.append('HTTP_%d' % status)
            state = 'bad'
        if badd:
            pbad(where, ','.join(badd))
            state = 'bad'
        key = (seat, body)
        if key in seen_body and seen_body[key] != sha:
            pbad(where, 'BODY_COLLISION %s' % body)
            state = 'bad'
        seen_body[key] = sha
        rec = dict(seat=seat, where=where, url=url, final_url=fin,
                   status=status, sha=d['sha256'], bytes=d['bytes'], body=body, bodypath=bp,
                   state=state, data=data)
        records.append(rec)
        if state != 'ok' or not QUIET:
            extra = ''
            if url != fin:
                extra += ' REDIRECT'
            out('FETCH %s/%s %s%s' % (seat, body, state, extra))

# orphan bodies and seat dirs without receipts
refd = {r['bodypath'] for r in records}
seats_with_receipts = {rp.split('/')[-2] for rp in receipts}
for path, (_kind, _ref, mode) in sorted(entries.items()):
    if not path.startswith(BASE + '/'):
        continue
    rel = path[len(BASE) + 1:]
    seat = rel.split('/')[0]
    if path.endswith('/receipts.jsonl'):
        continue
    if path not in refd:
        pwarn(path, 'ORPHAN_BODY')
    if seat not in seats_with_receipts:
        pwarn(seat, 'SEAT_NO_RECEIPTS')

# ---------------- refetch ----------------
def fetch_one(url):
    fd, tmp = tempfile.mkstemp()
    os.close(fd)
    fmt = '%{http_code}\t%{url_effective}\t%{num_redirects}\t%{size_download}'
    cmd = ['curl', '-sSL', '--max-time', '60', '--max-filesize', str(CAP),
           '--proto', '=https', '--proto-redir', '=https', '--max-redirs', '5',
           '--retry', '2', '--retry-delay', '1', '-o', tmp, '-w', fmt, url]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except Exception as e:
        return dict(rc=999, status=0, final=url, redirs=0, size=0, data=b'',
                    err=str(e))
    data = b''
    if os.path.exists(tmp):
        with open(tmp, 'rb') as fh:
            data = fh.read()
        os.unlink(tmp)
    line = ''
    for cand in p.stdout.splitlines():
        if cand.strip():
            line = cand
    parts = line.split('\t')
    try:
        status = int(parts[0])
        final = parts[1]
        redirs = int(parts[2])
        size = int(parts[3])
    except Exception:
        status, final, redirs, size = 0, url, 0, len(data)
    return dict(rc=p.returncode, status=status, final=final, redirs=redirs,
                size=size, data=data, err=p.stderr.strip())


def raw_parts(u):
    sp = urlsplit(u)
    seg = sp.path.strip('/').split('/')
    if sp.hostname == 'raw.githubusercontent.com' and len(seg) >= 4:
        return seg[0], seg[1], seg[2], '/'.join(seg[3:])
    if sp.hostname == 'github.com' and len(seg) >= 5 and seg[2] == 'raw':
        return seg[0], seg[1], seg[3], '/'.join(seg[4:])
    return None


_tag_cache = {}


def resolve_tag(owner, repo, ref):
    key = (owner, repo, ref)
    if key in _tag_cache:
        return _tag_cache[key]
    pat = 'refs/tags/' + ref
    p = subprocess.run(['git', 'ls-remote', 'https://github.com/%s/%s' % (owner, repo),
                        pat, pat + '^{}'], capture_output=True, text=True, timeout=90)
    direct = peeled = None
    if p.returncode == 0:
        for ln in p.stdout.splitlines():
            try:
                sha, name = ln.split('\t', 1)
            except ValueError:
                continue
            if name.endswith('^{}'):
                peeled = sha
            elif name == pat:
                direct = sha
    commit = peeled or direct
    _tag_cache[key] = (commit, bool(peeled), p.returncode, p.stderr.strip())
    return _tag_cache[key]


def norm_html(b):
    s = b.decode('utf-8', 'replace')
    s = re.sub(r'(?is)<(script|style)\b.*?</\1>', ' ', s)
    s = re.sub(r'(?s)<[^>]+>', ' ', s)
    s = html.unescape(s)
    return re.sub(r'\s+', ' ', s)


if REFETCH:
    groups = collections.OrderedDict()
    for r in records:
        if r['state'] == 'ok':
            groups.setdefault(r['url'], []).append(r)
    done = 0
    for url, rs in groups.items():
        if MAXURLS and done >= MAXURLS:
            break
        done += 1
        res = fetch_one(url)
        if res['status'] != 200 and rs[0]['final_url'] != url:
            res2 = fetch_one(rs[0]['final_url'])
            if res2['status'] == 200:
                note('REFETCH VIA_FINAL %s -> %s' % (url, rs[0]['final_url']))
                res = res2
        if res['rc'] == 63:
            pbad(url, 'REFETCH_TOO_LARGE')
            continue
        if res['status'] in (403, 429):
            could_not.append(url)
            out('RATELIMIT %s status=%d' % (url, res['status']))
            continue
        if res['status'] != 200:
            for r in rs:
                if raw_parts(url) or raw_parts(r['final_url']):
                    pbad(r['where'], 'UPSTREAM_%d %s' % (res['status'], url))
                else:
                    pwarn(r['where'], 'UPSTREAM_%d (volatile) %s'
                          % (res['status'], url))
            continue
        h = hashlib.sha256(res['data']).hexdigest()
        rp = raw_parts(res['final']) or raw_parts(url)
        tagmsg = ''
        commit = None
        if rp:
            owner, repo, ref, rest = rp
            if re.fullmatch(r'[0-9a-f]{40}', ref):
                commit = ref
            else:
                commit, peeled, rc, err = resolve_tag(owner, repo, ref)
                if commit:
                    tagmsg = ' tag=%s/%s@%s commit=%s peeled=%s' % (
                        owner, repo, ref, commit, peeled)
                    note('TAG %s/%s %s %s%s' % (owner, repo, ref, commit,
                                                ' peeled' if peeled else ''))
                else:
                    pwarn(url, 'TAG_UNRESOLVED %s/%s@%s rc=%s' % (owner, repo, ref, rc))
        for r in rs:
            same = (h == r['sha'])
            finaldrift = (res['final'] != r['final_url'])
            if same:
                out('REFETCH %s/%s IDENTICAL%s%s'
                    % (r['seat'], r['body'], tagmsg,
                       ' FINAL_URL_DRIFT' if finaldrift else ''))
                if finaldrift:
                    pwarn(r['where'], 'FINAL_URL_DRIFT now=%s recorded=%s'
                          % (res['final'], r['final_url']))
            elif rp:
                if commit:
                    curl_commit = ('https://raw.githubusercontent.com/%s/%s/%s/%s'
                                   % (rp[0], rp[1], commit, rp[3]))
                    cres = fetch_one(curl_commit)
                    if (cres['status'] == 200
                            and hashlib.sha256(cres['data']).hexdigest() == r['sha']):
                        pbad(r['where'], 'TAG_MOVED %s -> %s' % (url, commit))
                        out('REFETCH %s/%s TAG_MOVED commit=%s'
                            % (r['seat'], r['body'], commit))
                    else:
                        pbad(r['where'], 'UPSTREAM_DIVERGED commit=%s' % commit)
                        out('REFETCH %s/%s UPSTREAM_DIVERGED' % (r['seat'], r['body']))
                else:
                    pbad(r['where'], 'UPSTREAM_DIVERGED (unresolved tag)')
            else:
                pwarn(r['where'], 'VOLATILE_DRIFT')
                out('REFETCH %s/%s VOLATILE_DRIFT' % (r['seat'], r['body']))

def canon_url(u):
    sp = urlsplit(u)
    host = (sp.hostname or '').lower()
    seg = sp.path.strip('/').split('/')
    if host == 'raw.githubusercontent.com' and len(seg) >= 4:
        return ('gh', seg[0].lower(), seg[1].lower(), seg[2], '/'.join(seg[3:]))
    if host == 'github.com' and len(seg) >= 5 and seg[2] in ('blob', 'raw', 'tree'):
        return ('gh', seg[0].lower(), seg[1].lower(), seg[3], '/'.join(seg[4:]))
    return ('url', u.rstrip('/'))


def same_target(rowurl, rec):
    a = canon_url(rowurl)
    if a in (canon_url(rec['url']), canon_url(rec['final_url'])):
        return True
    return False


# ---------------- SOURCES row join ----------------
if ROWS:
    src = rd_any('corpus/SOURCES.md').decode('utf-8', 'replace')
    inreg = False
    table = {}
    for line in src.splitlines():
        if line.startswith('## '):
            inreg = line.strip() == '## Registry'
            continue
        if not inreg or not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.split('|')]
        if len(cells) == 13 and re.fullmatch(r'S\d{3,}', cells[1]):
            if cells[1] in table:
                pbad('SOURCES', 'DUPLICATE_ID ' + cells[1])
            table[cells[1]] = cells
    quotes = {}
    if QUOTES:
        with open(QUOTES, encoding='utf-8') as fh:
            quotes = json.load(fh)
    for sid in ROWS:
        cells = table.get(sid)
        if not cells:
            pbad('ROW ' + sid, 'NO_ROW')
            out('ROW %s NO_ROW' % sid)
            continue
        source, tier, anchor, status = cells[2], cells[4], cells[6], cells[8]
        usedby = cells[11] if len(cells) > 11 else ''
        if status != 'mined':
            pbad('ROW ' + sid, 'STATUS_%s' % status)
        if tier != 'A':
            pbad('ROW ' + sid, 'TIER_%s' % tier)
        if usedby in ('', '—', '-'):
            pbad('ROW ' + sid, 'NO_USED_BY')
        m = re.search(r'https://[^\s|)\]]+', source)
        if not m:
            out('ROW %s host/no-url (no fetch required)' % sid)
            continue
        rowurl = m.group(0).rstrip('.,;')
        rowhost = (urlsplit(rowurl).hostname or '').lower()
        if rowhost not in OFFICIAL_HOSTS and rowhost not in ALLOW_HOSTS:
            pbad('ROW ' + sid, 'HOST_NOT_OFFICIAL %s' % rowhost)
        shas = re.findall(r'(?<![0-9a-f])[0-9a-f]{16,64}(?![0-9a-f])', anchor)
        rowsha = max(shas, key=len) if shas else None
        if status != 'mined':
            pwarn('ROW ' + sid, 'STATUS_%s' % status)
        cands = []
        for r in records:
            if not rowsha:
                continue
            if len(rowsha) < 64:
                match = r['sha'].startswith(rowsha)
            else:
                match = (r['sha'] == rowsha)
            if match:
                cands.append(r)
        if not cands:
            if rowsha:
                pbad('ROW ' + sid, 'NO_SHA_MATCH %s' % rowsha[:16])
                out('ROW %s NO_SHA_MATCH' % sid)
            else:
                pbad('ROW ' + sid, 'NO_SHA_IN_ANCHOR')
                out('ROW %s NO_SHA_IN_ANCHOR' % sid)
            continue
        okc = [r for r in cands if r['state'] == 'ok']
        if not okc:
            pbad('ROW ' + sid, 'NEGATIVE_ONLY')
            out('ROW %s NEGATIVE_ONLY' % sid)
            continue
        pick = okc[0]
        mb = re.search(r'(?<![0-9])([0-9]{1,9})\s*(?:bytes|B)\b', anchor)
        if mb and int(mb.group(1)) != pick['bytes']:
            pbad('ROW ' + sid, 'BYTES_IN_ANCHOR %s vs %s' % (mb.group(1), pick['bytes']))
        url_note = ''
        if not same_target(rowurl, pick):
            pbad('ROW ' + sid, 'URL_MISMATCH %s' % rowurl)
            out('ROW %s URL_MISMATCH' % sid)
            continue
        if rowurl not in (pick['url'], pick['final_url']):
            url_note = ' url-note'
        q = quotes.get(sid)
        if q:
            text = q.get('text', '')
            mode = q.get('mode', 'substr')
            if len(text.split()) > 25:
                pbad('ROW ' + sid, 'QUOTE_WORDS>25')
            try:
                if mode == 'line':
                    lines = pick['data'].decode('utf-8', 'replace').splitlines()
                    n = int(q.get('line', 0))
                    hit = 1 <= n <= len(lines) and text in lines[n - 1]
                elif mode == 'text':
                    hit = text in norm_html(pick['data'])
                else:
                    hit = text.encode('utf-8') in pick['data']
            except Exception as e:
                hit = False
                pwarn('ROW ' + sid, 'QUOTE_ERROR %s' % e)
            if not hit:
                pbad('ROW ' + sid, 'QUOTE_MISSING mode=%s' % mode)
                out('ROW %s QUOTE_MISSING' % sid)
                continue
        elif not QUOTES_OPTIONAL:
            pbad('ROW ' + sid, 'QUOTE_UNCHECKED')
            out('ROW %s QUOTE_UNCHECKED' % sid)
            continue
        else:
            pwarn('ROW ' + sid, 'QUOTE_UNCHECKED')
        out('ROW %s receipted%s' % (sid, url_note))

for r in records:
    if r['state'] == 'bad':
        pass
nbad = sum(1 for r in records if r['state'] == 'bad')
nneg = sum(1 for r in records if r['state'] == 'negative')
nok = sum(1 for r in records if r['state'] == 'ok')
out('SUMMARY receipts=%d ok=%d negative=%d bad=%d errors=%d warnings=%d could_not=%d'
    % (len(records), nok, nneg, nbad, len(errors), len(warnings), len(could_not)))
if could_not:
    sys.exit(2)
if errors:
    sys.exit(1)
out('MADO_FETCH_CLOSURE: PASS')
sys.exit(0)
```
