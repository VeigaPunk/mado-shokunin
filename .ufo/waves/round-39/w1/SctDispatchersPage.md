# SctDispatchersPage — open the S220 source (0.56.0 Dispatchers page)

Scope: independently open `https://wiki.hypr.land/0.56.0/Configuring/Basics/Dispatchers/`,
keep the bytes as the S220 receipt, record the anchor + a ≤25-word quote grounding the
dispatcher-surface claim, access date 2026-10-25, and confirm the guessed alternative URL
`/0.56.0/Configuring/Advanced-and-Cool/Dispatchers/` answers 404.

Tier A. Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Seat dir: `.ufo/waves/round-39/w1/SctDispatchersPage/`.
Read-only elsewhere: no config tree, no compositor, no socket, no git/jj mutation.
No tools installed (curl + coreutils already present; nothing needed).

---

## 1. Fetch of the S220 source (HTTP 200)

```
$ mkdir -p /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-39/w1/SctDispatchersPage
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-39/w1/SctDispatchersPage
$ curl -sS -L -w '\n__HTTP_CODE__=%{http_code}\n__URL_EFF__=%{url_effective}\n__CONTENT_TYPE__=%{content_type}\n' \
      -o S220.bin -D S220.headers 'https://wiki.hypr.land/0.56.0/Configuring/Basics/Dispatchers/'
__HTTP_CODE__=200
__URL_EFF__=https://wiki.hypr.land/0.56.0/Configuring/Basics/Dispatchers/
__CONTENT_TYPE__=
EXIT=0
```

Response headers (captured to `S220.headers`, then deleted — only `S220.bin` is kept as
the receipt, per "do NOT write any other file"):

```
HTTP/2 200
date: Sun, 25 Oct 2026 19:09:26 GMT
content-length: 297863
server: cloudflare
cf-cache-status: DYNAMIC
strict-transport-security: max-age=0; includeSubDomains
```

**Receipt:** `.ufo/waves/round-39/w1/SctDispatchersPage/S220.bin`

```
$ sha256sum S220.bin
f9b51362f2440e02999089a255c5d7f3feb103f3cdeb6124c86a9f285c14b6e2  S220.bin
$ stat -c '%n %s bytes' S220.bin
S220.bin 297863 bytes
```

- **URL:** https://wiki.hypr.land/0.56.0/Configuring/Basics/Dispatchers/
- **HTTP status:** 200 (final URL unchanged — no redirect)
- **Size:** 297863 B
- **sha256:** `f9b51362f2440e02999089a255c5d7f3feb103f3cdeb6124c86a9f285c14b6e2`
- **Access date:** 2026-10-25
- **Page revision stamp:** `article:modified_time` = `2026-07-15T23:56:15+02:00`;
  footer "Last updated on <time datetime="2026-07-15T23:56:15.000Z">July 15, 2026</time>"
- **Canonical:** `<link rel="canonical" href="https://wiki.hypr.land/0.56.0/Configuring/Basics/Dispatchers/">`

### 1a. Digest is stable (not a stale CDN artifact) — three extra fetches

```
$ for u in "…/Basics/Dispatchers/" "…/Basics/Dispatchers/?cb=$(date +%s%N)" "…/Basics/Dispatchers/?r=$RANDOM"; do
    curl -sS -L -H 'Cache-Control: no-cache' -o /tmp/rb.html -w 'code=%{http_code} size=%{size_download} ' "$u"
    sha256sum /tmp/rb.html
  done
code=200 size=297863 f9b51362f2440e02999089a255c5d7f3feb103f3cdeb6124c86a9f285c14b6e2  /tmp/rb.html
code=200 size=297863 f9b51362f2440e02999089a255c5d7f3feb103f3cdeb6124c86a9f285c14b6e2  /tmp/rb.html
code=200 size=297863 f9b51362f2440e02999089a255c5d7f3feb103f3cdeb6124c86a9f285c14b6e2  /tmp/rb.html
```

All four fetches (plain, cache-busted, two distinct query strings) return the identical
297863 B / same digest. **The bytes are byte-stable.**

### 1b. Cross-check against the lane's own earlier receipt of the same page

The lane already holds the same URL from round 32 (`corpus/SOURCES.md` row **S196**):

```
$ sha256sum .ufo/waves/round-32/fetch/S196.bin
f9b51362f2440e02999089a255c5d7f3feb103f3cdeb6124c86a9f285c14b6e2  .ufo/waves/round-32/fetch/S196.bin
```

**Byte-identical to the round-32 S196 receipt** — the 0.56.0 path is a frozen
documentation snapshot, unchanged between 2026-10-24 and 2026-10-25. The S220 row is
therefore a *re-open* of an already-held source (which is what the round-39 assimilation
note asks for: "each cited source re-opened this round (the 0.56.0 Dispatchers page → row
S220)"), not a new page.

### 1c. The unversioned current page differs (scoped claim, not the same bytes)

```
$ curl -sS -L -o /tmp/unver.html -w 'code=%{http_code} size=%{size_download}\n' \
      'https://wiki.hypr.land/Configuring/Basics/Dispatchers/'
code=200 size=271123
$ sha256sum /tmp/unver.html
eed1fdc21eb9f2691b8df264228f5ad7c5096620bc50149a8d0f3696d973a71d  /tmp/unver.html
$ grep -o 'Last updated on <time[^>]*>[^<]*' /tmp/unver.html | head -1
Last updated on <time datetime=2026-08-26T14:50:40.000Z">August 26, 2026</time>
```

The current (unversioned) page is a different document (271123 B, rev 2026-08-26) but
carries the same two quoted sentences (both verified present in `/tmp/unver.html`), so the
S220 claim is not version-fragile. **S220's receipt must stay the versioned 0.56.0 bytes.**

---

## 2. Anchor and quote grounding the dispatcher-surface claim

### Anchor

`#dispatchers` — the first `h2` on the page, `<h2>Dispatchers<span class="hx:absolute
hx:-mt-20" id="dispatchers"></span>` at **receipt line 2936**. The section it opens is
the one that carries the dispatcher-surface statement and the `hl.bind()` / `hl.dispatch()`
API sentence.

Full heading/anchor inventory of the receipt (id → text), for a locator that wants a
finer anchor:

| anchor id | heading | receipt line |
|---|---|---|
| `#dispatchers` | Dispatchers (h2) | 2936 |
| `#parameter-explanation` | Parameter explanation (h3) | 2939 |
| `#window` / `#workspace` / `#direction` / `#monitor` | param rows (h4) | — |
| `#dispatchers-1` | Dispatchers (h2, the API reference) | 2999 |
| `#general` | General (h3) — `hl.dsp.` table | 3000 |
| `#window-1` | Window (h3) — `hl.dsp.window.` | 3097 |
| `#workspace-1` | Workspace (h3) — `hl.dsp.workspace.` | 3233 |
| `#group` | Group (h3) — `hl.dsp.group.` | 3261 |
| `#cursor` | Cursor (h3) — `hl.dsp.cursor.` | 3301 |
| `#workspace-selectors`, `#special-workspace`, `#executing-with-rules`, `#set_prop`, `#fullscreenstate` | remaining h2s | — |

### Quote (10 words, verbatim, no entity handling needed)

> "Their purpose is to be fed into hl.bind() or hl.dispatch()."

- Byte-exact in the receipt: `Their purpose is to be fed into <code>hl.bind()</code> or
  <code>hl.dispatch()</code>.` — occurrence count **1**, at receipt **line 2938**
  (byte offset 262855), inside the `#dispatchers` section.
- Rendered text (tags stripped, entities unescaped): **rendered line 261**,
  "contents are not guaranteed to be stable at all. Their purpose is to be fed into
  hl.bind() or hl.dispatch() ."
- The paragraph it ends is the dispatcher-surface definition: "Dispatchers return tables
  that describe an action you want to make. They do not invoke any action immediately,
  and their contents are not guaranteed to be stable at all." (rendered lines 260-261).
  No HTML entity appears anywhere in the quoted span (checked: no `&` in bytes
  262891-263100), so the quote is verbatim in both raw and rendered form.

### Second quote offered — the Lua-API sentence named in the task (10 words)

> "Since Hyprland 0.55, hyprlang is deprecated in favor of lua."

- Byte-exact, occurrence count **5** in the receipt (once in `<meta name="description">`,
  once in `og:description`, once in `twitter:description`, once in `itemprop="description"`,
  and once in the **body** at receipt **line 2931**).
- Rendered text line **256**.
- **Anchor caveat (measured, not assumed):** this sentence sits in the page's top
  "Note" callout, which is *before* the first `h2` and therefore carries **no `id` of
  its own** (the only `id` in that region is `favicon-svg` in `<head>`). The nearest
  resolvable in-page anchor is therefore `#dispatchers` (line 2936), and the callout is
  not addressable by a fragment of its own. Recorded so the registry row does not claim
  a `#note`-style anchor that does not exist on the page.
- This sentence establishes the *Lua-era* of the surface (hyprlang deprecated since
  0.55 in favour of lua), which is what pairs with the `hl.bind()`/`hl.dispatch()`
  sentence above: the dispatcher surface on the 0.56.0 line is a **Lua** surface.

### Supporting quote for the `hl.dsp.` group table (1 occurrence)

> "hl.dsp. contains:"

- byte-exact `hl.dsp.</code> contains:` at receipt **line 3001**, under the `#general`
  anchor; rendered text line **302** (the same rendered line the held r26 entry cites
  for its S196 quote). `hl.dsp.window.` (:3097), `hl.dsp.workspace.` (:3233),
  `hl.dsp.group.` (:3261), `hl.dsp.cursor.` (:3301) follow.

### Proposed S220 registry row (fields only — **not written**; SOURCES.md is not mine to edit)

```
| S220 | Hyprland wiki — Dispatchers (0.56.0), re-opened — https://wiki.hypr.land/0.56.0/Configuring/Basics/Dispatchers/ | docs | A | The dispatcher surface as published for the host's release line: the Lua API sentence and the hl.dsp.* groups | `#dispatchers` (h2, receipt line 2936); quote "Their purpose is to be fed into hl.bind() or hl.dispatch()." (receipt line 2938, rendered line 261); second quote "Since Hyprland 0.55, hyprlang is deprecated in favor of lua." (body receipt line 2931, rendered line 256, in the top Note callout, no id of its own); "hl.dsp. contains:" (receipt line 3001, `#general`); page revision "Last updated on July 15, 2026"; 297863 B sha256 f9b51362f2440e02999089a255c5d7f3feb103f3cdeb6124c86a9f285c14b6e2; receipt .ufo/waves/round-39/w1/SctDispatchersPage/S220.bin; opened 2026-10-25 | ... | mined | 2026-10-25 | 90d | corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md |
```

Note for whoever writes the row: the lane's registry **already carries S196** for this
exact URL with the same sha256 (`f9b51362…`), and `corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md`
already cites S196 at `verified-at: 2026-10-24`. S220 is the round-39 re-open row; the
row should say so ("re-opened"), not present the page as newly discovered. Also note the
held r26 entry's `source:` block and the staged amendment
(`/home/vgpnk/Projects/shokuknow/merge/mado/amendments/corpus/knowledge/dispatcher-surface-and-request-grammar-r26.md`,
read-only) name the page under **two different ids** — the held entry says **S196**, the
staged amendment says **S213** — while the round-39 registration says the re-open row is
**S220**. Three ids for one URL; the registry row number to use is the round-39 one
(S220), and the amendment's `S213` label will need to be re-pointed when the amendment is
appended.

---

## 3. The guessed alternative URL — CONFIRMED 404

```
$ curl -sS -L -o /dev/null -w 'alt_code=%{http_code} alt_url=%{url_effective}\n' \
      'https://wiki.hypr.land/0.56.0/Configuring/Advanced-and-Cool/Dispatchers/'
alt_code=404 alt_url=https://wiki.hypr.land/0.56.0/Configuring/Advanced-and-Cool/Dispatchers/
EXIT=0
```

With the body kept, for the record:

```
$ curl -sS -L -o /tmp/alt404.html -D /tmp/alt404.h -w 'code=%{http_code} size=%{size_download}\n' \
      'https://wiki.hypr.land/0.56.0/Configuring/Advanced-and-Cool/Dispatchers/'
code=404 size=924
$ head -1 /tmp/alt404.h
HTTP/2 404
$ sha256sum /tmp/alt404.html
95b0e4c9fe4f6eb294c526fda0c01bbedd8f93591d1ddbaa16cae6fb8b7a7346  /tmp/alt404.html
```

The 924-byte body is the wiki's own error page (`<h1 class=hextra-error-h1 …>404</h1>`),
not a soft-404 with content — there is no dispatcher text in it.

- **Status of the guessed alternative URL: HTTP 404** (both with and without the
  trailing slash: `…/Advanced-and-Cool/Dispatchers` → 404 as well).
- **Structural confirmation:** the 0.56.0 sidebar's own `Advanced and Cool` section
  contains no Dispatchers child. The complete set of `/0.56.0/Configuring/Advanced-and-Cool/*`
  links in the receipt is: `Animations`, `Devices`, `Environment-variables`,
  `Expanding-functionality`, `Gestures`, `Multi-GPU`, `Notifications`, `Performance`,
  `Permissions`, `Tearing`, `Uncommon-tips-and-tricks`, `Using-hyprctl`, `Virtual-GPU`,
  `XWayland` — **no Dispatchers**. The only Dispatchers link anywhere in the 0.56.0
  navigation is `/0.56.0/Configuring/Basics/Dispatchers/`. So the 404 is not a moved
  page: under 0.56.0 the Dispatchers page lives under **Basics**, and the queue's guess
  was wrong about the section.

This confirms the amendment's §1 OBS ("The queue's guessed URL … answers 404") against a
fresh fetch on 2026-10-25.

---

## 4. Files written

| path | what |
|---|---|
| `.ufo/waves/round-39/w1/SctDispatchersPage/S220.bin` | the S220 receipt bytes (297863 B, sha256 `f9b51362…6e2`) |
| `.ufo/waves/round-39/w1/SctDispatchersPage.md` | this report |

Nothing else was written. `S220.headers` was captured during the fetch and then deleted
so that only the named receipt remains. Scratch (`/tmp/rb.html`, `/tmp/unver.html`,
`/tmp/alt404.html`, `/tmp/alt404.h`) is outside the lane. No tracked file was edited; no
git/jj command other than read-only `git status --porcelain` / `git rev-parse HEAD`
(`457d1b125932c1e0d797061a2156b917bcd7edaa`). No pacman or package transaction was run —
no tools were installed, none were needed.

---

## 5. Findings

- **F1 (INFO) The 0.56.0 Dispatchers page is byte-stable and already held.** The
  2026-10-25 fetch (297863 B, sha256 `f9b51362f2440e02999089a255c5d7f3feb103f3cdeb6124c86a9f285c14b6e2`)
  is byte-identical to the lane's round-32 S196 receipt and to the sibling seat's
  round-39 receipt. Four independent fetches (one plain, one cache-busted, two with
  distinct query strings) all return that digest. A S220 row is a re-open receipt, not a
  new discovery, and the registry row should say so.
- **F2 (INFO, benign) Three different row ids name this one URL.** The held
  `dispatcher-surface-and-request-grammar-r26.md` says **S196**; the staged amendment
  says **S213**; the round-39 registration says the re-open row is **S220**. The SOURCES
  registry has **S196** (with the identical sha256) and no S213/S218/S219/S220 rows.
  Whoever writes the S220 row should mark it a re-open of S196 and re-point the
  amendment's `S213` label; otherwise the amendment and the entry will cite the same
  page under different ids.
- **F3 (INFO) The Lua-API sentence has no anchor of its own.** "Since Hyprland 0.55,
  hyprlang is deprecated in favor of lua." lives in the top "Note" callout, before the
  first `h2`, in a container with no `id`. Any registry locator naming it must use
  `#dispatchers` (nearest resolvable anchor) rather than a `#note` fragment — the
  fragment does not exist on the page. The `hl.bind()`/`hl.dispatch()` sentence, by
  contrast, sits under a real `#dispatchers` anchor.
- **F4 (INFO) The guessed URL's 404 is structural.** `…/Advanced-and-Cool/Dispatchers/`
  → 404 (924-byte wiki error page), and the 0.56.0 nav's `Advanced and Cool` section has
  no Dispatchers child at all; only `Basics/Dispatchers/` exists. The staged amendment's
  §1 OBS is confirmed on 2026-10-25.
- **F5 (INFO, claim-robustness) The claim does not depend on the version pin.** The
  current unversioned page (271123 B, rev 2026-08-26) carries both quoted sentences
  verbatim, so the dispatcher-surface statement survives the 0.56.0 → current drift; only
  the *bytes* pinned by S220 are version-specific, which is why the receipt keeps the
  versioned fetch.
