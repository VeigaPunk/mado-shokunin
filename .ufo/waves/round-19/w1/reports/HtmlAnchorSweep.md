# HtmlAnchorSweep — R18-V1 is real and unique to S094; only S084 shares a mutable-object defect, the other four HTML-digest rows reproduce

Scope: the criterion R18-V1 ground truth only — which `corpus/SOURCES.md` rows at
`17661e0fa83f978fb659f5bb8fef47f0969f6945` credit a sha256 of an HTML page / tree-blob
page / API listing / docs site, and whether committed fetch receipts prove per-fetch
digest drift. Face facts only; verdicts on C1/C2/C3 belong to L1.

## Question and method

1. `git show 17661e0:corpus/SOURCES.md` (310 lines, 95 rows S001–S095) parsed as 11-column
   pipe rows. Every row whose `anchor` (or `source`, for S094) carries a 64-hex digest was
   classified by the *object* the digest covers: raw tagged file, host file, tarball,
   repo snapshot, or HTML/docs/tree page. 44 rows carry a full 64-hex digest in `anchor`
   (S001–S004/S011 carry truncated digests of repo-owned files); 6 cover an HTML/docs/tree
   object and are in scope below. No row credits a digest over a GitHub **blob** page or an
   **API listing** — blob-page rows (S005, S018) cite a commit/tag, not a digest.
2. Receipt census: `.ufo/waves/round-18/fetch/*/receipts.jsonl` = 49 files; round-19
   sibling files = 7 at scan time; round-17 has **no** `fetch/` directory (its bytes live
   only in `round-17/w1|w2/reports/*`), so S061/S062 have no machine receipt by
   construction. At final count: 56 pre-existing files, 450 receipt lines, 282 URLs (sibling
   seats are still appending, so these are lower bounds).
3. Grouped every `url` across all receipts and counted **distinct sha256 among HTTP 200**
   rows. Exactly **2** URLs have ≥2 distinct 200 digests — both S094 tree listings
   (finding A); this stayed at 2 across every re-count. My 19 receipts are in
   `.ufo/waves/round-19/fetch/HtmlAnchorSweep/receipts.jsonl` (19 valid JSON lines).
4. Ambiguous cases were settled by fresh curl fetches under the round-19 fetch contract
   (bodies + JSONL receipts at `.ufo/waves/round-19/fetch/HtmlAnchorSweep/`).

## Table — all six in-scope rows (S094 split by URL)

| id | URL credited with the digest | digest(s) | receipts agree? | real defect? |
|---|---|---|---|---|
| S061 | `https://wiki.archlinux.org/index.php?title=Alacritty&action=raw` (raw **wikitext**, not HTML) | `c39c563d…4600bb` (cited); reproduced 1/1 at 8,275 B | **yes** — no round-17 receipts exist; my fetch reproduces the cited digest, and `api.php…Alacritty` returns `revid 869789, 2026-03-23T05:20:49Z`, the revid the row names | **no** — byte-stable raw text for the named revid. Caveat: the row's proposed flip (`oldid=`-pinned) is bot-walled (finding C) |
| S062 | `https://linuxjunkies.org/guides/configure-alacritty` (HTML) | `08608a0b…bec2c653` (cited) | **yes** — 3 fresh fetches, all 90,051 B and `08608a0b…` (mine `:15,:16,:17`); the row's own note that a *different* digest `bf875a25…350ab90a` did not reproduce is a historical byte state, absent from all receipts | **no for the anchor** — the cited digest reproduces 3/3 today; but the row's sentence "raw bytes differ per fetch" is **not reproduced** (finding D). Row is `rejected` on a version error, so the digest carries no claim |
| S063 | `https://wiki.hypr.land/Hypr-Ecosystem/hypridle/` (docs-site HTML) | `b45c03dc…83f640` (cited) | **yes** — 5 receipts, one digest: `round-18/fetch/FetchBackfillR17/receipts.jsonl:4`, `round-19/fetch/CriticC1/receipts.jsonl:1,3`, mine `:5,:6` (254,750 B each) | **no** — 2/2 same digest; not per-fetch variable. Mutable content is handled by its 90d recheck |
| S064 | `https://wiki.hypr.land/Hypr-Ecosystem/hyprlock/` (docs-site HTML) | `f69cff6b…97eabf5` (cited) | **yes** — 3 receipts, one digest: `round-18/fetch/FetchBackfillR17/receipts.jsonl:5`, mine `:7,:8` (291,777 B each) | **no** — 2/2 same digest |
| S084 | `https://docs.rs/xdg/latest/xdg/struct.BaseDirectories.html` (docs-site HTML, **mutable alias**) | `0291cfe6…b50f9f0d` (cited, 105,537 B); same crate at `/xdg/3.0.0/` = `adaec7c3…08762f6` (105,205 B) | **yes on the bytes** — 10 receipts, one digest (`NoteWalker:24`, `MadoR18.RevengeTarballRepro:5,6`, `ReviewWalkerUpstream:18`, `ReopenS084:1`, `MadoR18.ReviewSourcesRows:2`, `CriticC1:2,4`, mine `:9,:10`) — but they agree on an **alias page** | **yes (R18-V4 class)** — the digest identifies `/latest/` markup, not a crate version; versioned bytes differ (finding B) |
| S094 | `https://github.com/basecamp/omarchy/tree/v3.8.4/themes/matte-black` | `50c1ac25…e302ef` (cited) + **6 more** 200 digests = **7 distinct** | **no** | **yes — R18-V1, proven by committed receipts alone** |
| S094 | `https://github.com/basecamp/omarchy/tree/v3.8.4/themes/matte-black/backgrounds` | `9e1160a0…d32575` (cited) + **5 more** 200 digests = **6 distinct** | **no** | **yes — same defect** |

`corpus/SOURCES.md:106` is byte-identical at baseline `9c54c56` and at `17661e0`
(`git diff --stat 9c54c56 17661e0 -- corpus/SOURCES.md` prints nothing), and the two digest
literals occur nowhere else under `corpus/` (`git grep` at `17661e0 -- corpus/` returns only
line 106). A red-before check on this criterion can therefore key off
`9c54c56:corpus/SOURCES.md:106`.

## Finding A — S094 tree-listing digests are per-fetch wrapper bytes (decisive)

URL `…/tree/v3.8.4/themes/matte-black`, all HTTP 200, all same logical page:

| receipt | bytes | sha256 | fetched_at |
|---|---|---|---|
| `round-18/fetch/NoteTheme/receipts.jsonl:4` (cited) | 229,027 | `50c1ac253df17986…` | 15:40:32Z |
| `round-18/fetch/ReopenS094/receipts.jsonl:2` | 229,036 | `6b355a468bfde1e3…` | 16:00:00Z |
| `round-18/fetch/ReopenS094/receipts.jsonl:3` | 229,036 | `3b18a612e8288e58…` | **16:00:00Z (same second)** |
| `round-18/fetch/ReviewThemeUpstream/receipts.jsonl:13` | 229,036 | `de57cbaf2f46a581…` | 16:05:33Z |
| `round-18/fetch/MadoR18.ReviewSourcesRows/receipts.jsonl:4` | 229,026 | `8bfaba248412fff8…` | 16:03:10Z |
| `round-19/fetch/HtmlAnchorSweep/receipts.jsonl:1` | 229,097 | `78707accce18d8e0…` | 2026-10-20T17:07Z |
| `round-19/fetch/HtmlAnchorSweep/receipts.jsonl:2` | 229,098 | `da9070069ea2f44a…` | 2026-10-20T17:07Z |

`…/backgrounds`: `9e1160a0…` (cited, `NoteTheme:16`), `267618a4…` (`ReopenS094:4`),
`369f9439…` (`ReviewThemeUpstream:14`), `2d22e126…` (`ReviewSourcesRows:5`), `36bfe79b…`
and `fc803500…` (mine `:3,:4`) — 6 distinct.

Two receipts in the **same second with identical byte length and different digests**
(`ReopenS094:2,3`) is the cleanest possible proof that the bytes vary per request and not on
content change. Content is in fact constant: extracting the embedded tree JSON
(`"name":…,"path":"themes/matte-black…"`) from **all seven** bodies yields one identical
name-set (10 entries for the theme tree, 14 for `backgrounds`) — the differing bytes are the
GitHub per-request wrapper (CSRF/meta/cache-buster). Also `final_url` on every receipt is
`https://github.com/omacom/omarchy/tree/…` (the `basecamp→omacom` rename redirect), so the
credited URL is not even the URL finally served.

Consequence for S097: the file **names** the row lists are stable and legitimately
re-derivable from every fetched body, but the two tree digests are invalid anchors and must
not be carried forward in any form. Per-fetch HTML, API listings and docs pages are never
digest anchors (round-18 lesson M7), and the same-second pair is the receipt that proves it
without inference.

## Finding B — S084: stable today, but the digest anchors an alias (R18-V4)

`/latest/` and `/3.0.0/` differ by 332 B of permalink/menu markup (
`round-19/fetch/HtmlAnchorSweep/s084-docsrs-latest-1.html` vs `s084-docsrs-300.html`); both
bodies embed `{"name": "xdg", "version": "3.0.0"}`, so the documented content is the same
xdg 3.0.0 reference. The cited digest is reproducible (10 receipts — 8 pre-existing, 2
fresh — identical) **while `latest` still resolves to 3.0.0**, and the digest is guaranteed
to stop reproducing on the next xdg release — exactly the freshness failure R18-V4 names. The support row should cite either the versioned page digest
(`adaec7c3…08762f6`, 105,205 B, also already receipted 5×) or, better, the crate tarball
`https://static.crates.io/crates/xdg/xdg-3.0.0.crate` (15,821 B,
`2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5`,
`round-18/fetch/SrcWalkerConfigPaths/receipts.jsonl:3`), which is a versioned binary artifact
and matches the reserved S098 shape.

## Finding C — Arch Wiki `oldid=` pinning is bot-walled; `action=raw` is not

S061's proposed flip is "oldid-pinned tier-C cross-check". Three fetches of
`…index.php?title=Alacritty&oldid=869789&action=raw` returned **HTTP 200 with an Anubis
anti-bot challenge HTML** (7,469 / 7,469 / 7,468 B; `e7983df2…`, `2e04311c…`, `fda76acf…`;
mine `:13,:14,:19`), not wikitext — the challenge carries a per-request nonce, so those
three digests also differ. Those three challenge bodies embed the request's public IP and
were therefore **withheld** from the lane (`fetch/HtmlAnchorSweep/WITHHELD.md`); the claim
rests on the receipts plus the challenge title, not on quoting the bodies. The plain
`…&action=raw` URL returns the real wikitext (8,275 B,
`c39c563d…`, mine `:12`), and the API (`mine :18`) confirms that raw text is revid 869789's
current bytes (`revid 869789, 2026-03-23T05:20:49Z`).
So the row's digest and revid attribution are **correct today**, but (i) a future edit breaks
the digest because the URL is unpinned, and (ii) the stated pinned re-fetch route is
unreachable with curl. Anything in the round-19 gate that treats "HTTP 200 + digest" as a
success needs to reject challenge pages; 200 is not evidence of the expected body.

## Finding D — S062: the anchor reproduces; the "dynamic page" sentence does not

Three fetches of `https://linuxjunkies.org/guides/configure-alacritty` all returned
90,051 B and `08608a0bafb9bb7b4cea2a7970dbc2f926946976c7f9eb23a1d30249bec2c653`
(mine `:15,:16,:17`), i.e. the row's anchor digest is reproducible now and matched the
round-17 report (`round-17/w2/reports/ReopenS062.md` table). The row's anchor sentence
"dynamic page: raw bytes differ per fetch (CDN token; the recorded `bf875a25…350ab90a` is
not reproducible)" is therefore too strong as written for present behavior: the observed
non-reproducibility belongs to a *different* recorded digest, not to the cited one. This does
not touch the verdict (S062 is rejected for a version error, not for its bytes), and no
round-17 receipts.jsonl exists for it.

## What this means for the routed defect

- R18-V1 is **real, and it is exactly one row**: S094 (`corpus/SOURCES.md:106`), two tree
  URLs, 7 and 6 distinct 200 digests. It is the only SOURCES row where committed receipts
  themselves show digest drift without fresh fetching. S097 must replace both digests.
- Of the five other HTML/docs-site digest rows, four reproduce byte-for-byte on fresh
  fetches (S061 raw wikitext, S062, S063, S064) and one (S084) reproduces but is the
  separate R18-V4 alias defect. A blanket "all HTML digests are broken" claim would be false
  on today's evidence; a per-fetch-stability check keyed to receipts would be red only for
  the S094 URLs (and would remain green for S063/S064/S084-latest, which is correct).
- Suggested red-before predicate for C1 (runnable on `9c54c56` artifact): fail if any
  `SOURCES.md` anchor credits a sha256 and the URL, across all committed
  `fetch/*/receipts.jsonl`, has ≥2 distinct 200 digests. At `9c54c56` this is red on line 106
  only; it needs no network and cannot be gamed by a single agreeing fetch.

## Limits

- The three Anubis challenge bodies (`s061-archwiki-oldid-{1,2,3}.txt`) were withheld from
  the lane after SentinelVcsFixtures flagged an embedded request IP; their receipts remain
  digest-only, so the exact challenge markup cannot be re-inspected in-lane.
- Did not audit round-17 byte provenance for S061/S062 beyond the two reports named — no
  receipts.jsonl existed for those URLs, so their historical digests cannot be machine-checked.
- Did not test GitHub **blob** page digest behavior (no SOURCES row credits one); the tree
  result does not automatically extend to `/blob/` pages without a receipt.
- The S094 body comparison used the embedded `"name"/"path"` JSON only; other wrapper
  differences (CSRF tokens, cache-buster, other rendered markup) were not enumerated beyond
  the byte/digest drift and the identical name-sets.
- Did not evaluate whether S097's eventual replacement anchor is admitted by QUALITY; the
  recommendation is evidence-shaped, not a claim decision.
- Did not fetch beyond the listed candidates; no host binaries, logs, or live gate touched.
- `oldid` bot-wall behavior may be transient/rate-limit-sensitive; observed 3/3 behind the
  same challenge.

## Installs

none (curl 8.23.0, python3, coreutils only; no package or tool changes).
