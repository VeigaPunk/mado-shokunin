# ScoutS221 — independent re-open of the hyprctl flags source (S221)

Scope: re-fetch `https://wiki.hypr.land/0.56.0/Configuring/Advanced-and-Cool/Using-hyprctl/`
independently of the round-38 L1, compare against the pinned receipt
`.ufo/waves/round-38/fetch/S221.bin`, extract the `flag list:` block and the
synchronous-dispatch warning verbatim, and check whether
`corpus/knowledge/hyprctl-flags-r28.md`'s three flag quotes are verbatim
(accounting for HTML entities).

Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin` (LANE).
Scratch: `/tmp/mado38-ScoutS221/`. No lane production file was modified.

---

## 1. Re-fetch and byte comparison

```
$ mkdir -p /tmp/mado38-ScoutS221 && cd /tmp/mado38-ScoutS221
$ curl -sSL -o live-hyprctl.html -w 'HTTP %{http_code} final=%{url_effective} bytes=%{size_download}\n' \
    'https://wiki.hypr.land/0.56.0/Configuring/Advanced-and-Cool/Using-hyprctl/'
HTTP 200 final=https://wiki.hypr.land/0.56.0/Configuring/Advanced-and-Cool/Using-hyprctl/ bytes=306865

$ cp LANE/.ufo/waves/round-38/fetch/S221.bin pinned.bin
$ cmp pinned.bin live-hyprctl.html && echo "CMP: identical"
CMP: identical

$ sha256sum pinned.bin live-hyprctl.html
35046ba0dc1dd1db4b1e8548e7e6a0be9f0ffc0051c055f66ddee5451879d30a  pinned.bin
35046ba0dc1dd1db4b1e8548e7e6a0be9f0ffc0051c055f66ddee5451879d30a  live-hyprctl.html

$ stat -c '%n %s bytes' pinned.bin live-hyprctl.html
pinned.bin 306865 bytes
live-hyprctl.html 306865 bytes
```

**Both sha256 = `35046ba0dc1dd1db4b1e8548e7e6a0be9f0ffc0051c055f66ddee5451879d30a`, both 306865 B.**

The brief anticipated "moved bytes" because the wiki is a living page. **No bytes
moved.** The 0.56.0 path is a version-pinned documentation snapshot, so it is
stable. I confirmed the fetch is not a stale CDN artifact:

```
$ curl -sSL -H 'Cache-Control: no-cache' -H 'Pragma: no-cache' \
    -o bust.html "https://wiki.hypr.land/0.56.0/Configuring/Advanced-and-Cool/Using-hyprctl/?cb=$(date +%s%N)"
$ sha256sum bust.html
35046ba0dc1dd1db4b1e8548e7e6a0be9f0ffc0051c055f66ddee5451879d30a  bust.html

$ for i in 1 2; do curl -sSL ".../Using-hyprctl/?r=$RANDOM$i" | sha256sum; done
35046ba0dc1dd1db4b1e8548e7e6a0be9f0ffc0051c055f66ddee5451879d30a  -
35046ba0dc1dd1db4b1e8548e7e6a0be9f0ffc0051c055f66ddee5451879d30a  -
```

Three independent fetches (plain, cache-busted, two distinct query strings) all
return the pin's digest. `HTTP/2 400` on `HEAD` requests is a Cloudflare
behaviour of the site (it rejects `HEAD`), not a content change — `GET` returns
200 with the identical body.

**PASS — the pinned receipt is byte-exact what the wiki serves today.**

---

## 2. The `flag list:` block, extracted verbatim

Raw HTML (receipt line 3396 area; `<p>flag list:</p>` at raw offset 303038, and
`flag list:` occurs exactly once in the whole page):

```html
<p>flag list:</p>
<div class="hextra-code-block ..."><div><div class="highlight"><pre tabindex="0" class="chroma"><code class="language-txt" data-lang="txt"><span class="line"><span class="cl">j -&gt; output in JSON\n</span></span><span class="line"><span class="cl">i -&gt; select instance (id or index in hyprctl instances)\n</span></span><span class="line"><span class="cl">r -&gt; force state refresh after issuing commands (e.g. layout or rule changes)</span></span></code></pre></div></div>
```

Tags stripped and HTML entities unescaped (`&gt;` → `>`), the code block renders
as exactly three lines:

```
j -> output in JSON
i -> select instance (id or index in hyprctl instances)
r -> force state refresh after issuing commands (e.g. layout or rule changes)
```

The `Flags` section heading that contains it: `<h2>Flags<span class="hx:absolute hx:-mt-20" id="flags">`
— so the entry's `§ Flags` locator resolves to a real anchor on the page.

---

## 3. The synchronous-dispatch warning, extracted verbatim

Body occurrence, receipt lines 2901-2903:

```html
2901:     <div class="hx:mt-6 hx:leading-7 hx:first:mt-0"><p><em>hyprctl</em> calls will be dispatched by the compositor <em>synchronously</em>, meaning
2902: any spam of the utility will cause slowdowns. It&rsquo;s recommended to use <code>--batch</code>
2903: for many control calls, and limiting the amount of info calls.</p>
```

Rendered text (tags stripped, entities unescaped):

> hyprctl calls will be dispatched by the compositor synchronously, meaning any spam of the utility will cause slowdowns.

The same sentence also appears byte-exact three more times in the receipt's
`<meta name="description">`, `og:description` and `twitter:description` blocks
(receipt lines 14, 49, 56), so the quoted substring is present 3× byte-exactly:

```
$ python3 -c "… raw.count(b'hyprctl calls will be dispatched by the compositor synchronously, meaning any spam of the utility will cause slowdowns.')"
3
```

Note `It&rsquo;s` → `It’s` is the only entity in the warning paragraph, and it
falls *after* the quoted sentence, so the entry's quote needs no entity
handling at all. The entry's §1 flag quotes, by contrast, do need `&gt;` →
`>` handling — and the entry says so explicitly ("HTML `&gt;` unescaped").

---

## 4. Are the entry's three flag quotes verbatim?

`corpus/knowledge/hyprctl-flags-r28.md` §1 quotes three flags. I extracted the
page's block and compared string-for-string after entity unescaping:

```
MATCH  'j -> output in JSON'
MATCH  'i -> select instance (id or index in hyprctl instances)'
MATCH  'r -> force state refresh after issuing commands (e.g. layout or rule changes)'
```

**PASS — all three are verbatim.** The entry's warning quote is also verbatim:
joining the entry's markdown line-wrapped quote and comparing to the page
sentence gives `entry warning quote joined == page quote: True`.

### 4b. The `--batch` disclosure anchor

The entry's closing paragraph claims "The page also names a fourth, legacy,
`--batch` flag (S221 `:3375`)". Checked against the receipt:

```
$ awk 'NR==3375' LANE/.ufo/waves/round-38/fetch/S221.bin
    <a href="#batch" class="subheading-anchor" aria-label="Permalink for this section"></a></h2><p>You can use the legacy <code>--batch</code> flag to issue multiple commands separated with a <code>;</code>.</p
```

**PASS** — line 3375 carries the legacy `--batch` sentence, and it is in the
`Batch` section, outside the `Flags`/`flag list:` block, exactly as the entry
says. The `flag list:` block itself has exactly three lines, so "three flags"
is right.

---

## 5. Does today's page still say what the entry claims?

**YES.** Every OBS-level claim in `hyprctl-flags-r28.md` that is sourced to
S221 is supported by the bytes I fetched today:

| Entry claim | Status |
|---|---|
| §1 OBS: page publishes the flag list as three flags `j`/`i`/`r`, inside the `flag list:` code block | **supported** — block has exactly those three lines |
| §1 OBS: `j -> output in JSON` | **verbatim** |
| §1 OBS: `i -> select instance (id or index in hyprctl instances)` | **verbatim** |
| §1 OBS: `r -> force state refresh after issuing commands (e.g. layout or rule changes)` | **verbatim** |
| §2 OBS: page warns "hyprctl calls will be dispatched by the compositor synchronously, meaning any spam of the utility will cause slowdowns." | **verbatim** |
| header: source locator `§ Flags` | **resolves** — `<h2>Flags … id="flags">` |
| closing note: legacy `--batch` at `:3375` | **supported** — line 3375 |

The 0.56.0 page is a frozen documentation snapshot: I also fetched the
*unversioned* current page (`https://wiki.hypr.land/Configuring/Advanced-and-Cool/Using-hyprctl/`,
281934 B, `24c3987dd95986ef306edf14804c4a959c5846d4a105d70bb1d58f6b78c6b468`,
"Last updated on August 26, 2026"). Its `flag list:` block carries the
**identical three flag lines** and its Batch section still carries the same
legacy `--batch` sentence, so the entry's substance is not even version-fragile.

---

## 6. Findings

### F1 (LOW — already fixed at HEAD; was in the landed round-38 data) — S221 registry size cell was a digest prefix, not a byte count

`corpus/SOURCES.md` S221 originally claimed `35046 B`. The receipt is
**306865 B**. `35046` is exactly the first five hex characters of S221's own
sha256 `35046ba0…` — a paste slip, not a measurement.

This was already found and fixed in-seat (`b8400aa`, "registry row corrections
(sizes/anchors/stamp/S277 URL)"). At HEAD the row reads:

```
... @ page revision "Last updated on June 13, 2026", 306865 B sha256 `35046ba0dc1dd1db4b1e8548e7e6a0be9f0ffc0051c055f66ddee5451879d30a`; receipt .ufo/waves/round-38/fetch/S221.bin ...
```

Both cells now match what I independently measured. **No action needed**; I
record it because the correction is a post-freeze edit, and because the same
class of defect is still live in sibling rows I did not re-check.

Independently: the S221 row's **page-revision stamp was also wrong** before the
seat fix — it claimed `"Last updated on May 2, 2026"`, which is S187's (the IPC
page) revision, not S221's. S221's page says **June 13, 2026** (confirmed in
the receipt: `article:modified_time` = `2026-06-13T19:18:41+03:00`,
`<time datetime="2026-06-13T19:18:41.000Z">June 13, 2026</time>`). I confirmed
May 2, 2026 belongs to the *IPC* page by fetching it independently:
`curl … https://wiki.hypr.land/0.56.0/IPC/` → sha256
`136e5511fba5524a5cb1685668429ee28f7a2710c70104441eeb2b674f6a37a4` (byte-identical
to the pinned `S187.bin`) with `Last updated on May 2, 2026`. So the two
versioned wiki rows were initially stamped with each other's revision. Both are
correct at HEAD; the S187 row still legitimately says May 2, 2026.

### F2 (MEDIUM — live now, affects the entry's §3 UNK) — the entry's UNK says the server-side handling was "not re-read this round", but the lane already holds the server-side parser, and it contradicts the entry's framing

`hyprctl-flags-r28.md` §3:

> **UNK** The server-side handling of each flag was not re-read this round — the
> IPC contract established that a leading flag segment is stripped before the
> dispatcher name is matched, not what the server then does with `j`, `i` or `r`.

Two problems, both checkable against bytes the lane already holds:

**(a) The UNK's premise is false — the server-side handling *was* in the round's
hands.** `S158` is `src/debug/HyprCtl.cpp` at the host's own commit
`efb50993`, and I confirmed the round-38 receipt
`.ufo/waves/round-38/fetch/S158.bin` is byte-identical to upstream
(`sha256 798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa`,
97582 B). That file contains the server-side flag parser in
`CHyprCtl::getReply`:

```
S158.bin:2062: std::string CHyprCtl::getReply(std::string request) {
S158.bin:2068:     // process flags for non-batch requests
S158.bin:2069:     if (!request.starts_with("[[BATCH]]") && request.contains("/")) {
S158.bin:2085:             if (c == 'j')
S158.bin:2086:                 format = eHyprCtlOutputFormat::FORMAT_JSON;
S158.bin:2087:             else if (c == 'r')
S158.bin:2088:                 reloadAll = true;
S158.bin:2089:             else if (c == 'a')
S158.bin:2090:                 m_currentRequestParams.all = true;
S158.bin:2091:             else if (c == 'c')
S158.bin:2092:                 m_currentRequestParams.sysInfoConfig = true;
S158.bin:2096:             request = request.substr(sepIndex + 1); // remove flags and separator so we can compare the rest of the string
```

So the server accepts **four** flag letters (`j`, `r`, `a`, `c`), not the
three the page publishes — `a` and `c` are undocumented in the wiki's
`flag list:` block, and the page's `i` is **not** a server-side flag at all
(`'i'` appears nowhere in the parser). The host's own `hyprctl --help`
corroborates: `-i`/`--instance` is a *client-side* option ("use a specific
instance"), alongside `--quiet (-q)`, another client-side flag the page's
`flag list:` block does not list. The entry's OBS text is about what the
*page publishes*, so it is not wrong as written — but the entry's §1 INF
"the flags are *client-facing output and targeting modifiers*" over-reaches,
because `j` and `r` are handled *server-side* inside `getReply` while `i` is
handled client-side by the CLI before the request is even sent.

**(b) The UNK says "the IPC contract established that a leading flag segment is
stripped before the dispatcher name is matched".** `corpus/knowledge/ipc-contract-r25.md`
does not establish that. Grepping it for the claim returns **nothing**:

```
$ grep -c -iE "strip|leading|prefix|segment|remove" corpus/knowledge/ipc-contract-r25.md
0
```

The only flags-related line in r25 is `42: > "Basically, write `[flags]/command args`." (S186:19)`.
The stripping fact the entry attributes to r25 is in fact established by
**S158** (the `request.substr(sepIndex + 1)` line above) — which the lane
holds and which r8 and r31 already cite. So the entry's UNK cites the wrong
document for its own premise, and simultaneously declares the fact unmeasured
when the lane's own pinned receipt measures it.

**Bearing on the round's claim:** C2's domain counter's clause `l` (lineage)
does not test any of this — it only checks that four phrase stems appear in
the entry body. The counter passed the entry at 3/3 both before and after my
mutations of the entry's quotes (see §7). The entry is *true* about the page;
the issue is that it is imprecise about the server side and points at the wrong
document. This is a knowledge-quality finding, not a claim failure: C2's
target set is the three entries' admission, and the entries are admitted
correctly with respect to their sources.

### F3 (MEDIUM — live now, same class as F2) — the entry's §1 INF mis-states what `r` does, and the lane's own receipt contradicts it

The entry says `r` "asks the compositor to re-read its state after a mutating
command so the reply reflects the new state." S158 shows the opposite order:
the reply string is produced first, and the reload happens *after* the reply
has been computed.

```
S158.bin:2107:        result = cmd->fn(format, request);      <- reply computed
S158.bin:2126:    if (reloadAll) {                              <- reload happens AFTER
S158.bin:2127:        Config::monitorRuleMgr()->scheduleReload();
S158.bin:2128:        Layout::Supplementary::algoMatcher()->updateWorkspaceLayouts();
...
S158.bin:2163:    return result;
```

`reloadAll` is applied at `:2126`, i.e. after `result` is built at `:2107`/`:2118`
and before `return result;` at `:2163`. So `r` refreshes compositor state
*after* the reply was rendered; it does not make "the reply reflect the new
state" for that request. The page's own wording is weaker and safer
("force state refresh **after issuing commands**"), which the entry's INF
sharpens into a claim the source does not support. The entry also says the
refresh follows "a mutating command" — upstream, `reloadAll` is triggered by
the flag's presence, not by the command being mutating.

I flag this because it is a claim the lane can check and currently does not:
S158 is already a pinned, Gate-quoted source in this very round.

### F4 (LOW — counter gap, live now) — the domain counter does not bind the *entry's* quotes to the receipt; it binds only its own Gate quote

`quality/counters/c2-r38-request-ground.py` clause `g` requires the receipt's
**Gate quote** to appear verbatim in the entry body
(`stated = stated or quote in body`), and clause `f` requires the two *surface
tokens* (`"select instance"`, `"force state refresh"`) to appear in both the
entry and the receipt. Neither clause requires the entry's **other two** flag
quotes, nor the warning sentence, to be verbatim.

Demonstrated in a sandbox clone (`/tmp/mado38-ScoutS221/sb`, clone of LANE at
`ff81aaf`; all mutations committed inside the sandbox only — LANE untouched):

| Sandbox mutation to `corpus/knowledge/hyprctl-flags-r28.md` | Counter result |
|---|---|
| `j -> output in JSON` → `j -> output in JSON, i.e. JSON output` (non-verbatim paraphrase) | `a=1 b=1 c=1 d=1 e=1 f=1 g=1 l=1 … ok=1` — **still TARGET_MET** |
| warning OBS replaced by a paraphrase (drops the verbatim quote, keeps the lineage phrase) | `… ok=1` — **still TARGET_MET** |
| warning OBS **deleted outright** and replaced with a fabricated claim ("the page warns that heavy utility use can hurt performance"), dropping the lineage phrase too | `lineage=3/3 … ok=1` — **still TARGET_MET** |
| `j` flag quote **removed entirely** | `lineage=2/3 … ok=0` — caught, but only by the lineage floor, not by any quote check |
| `S221.bin` receipt mutated (`i -> select instance …` → `i -> MUTATED FLAG TEXT`) | `d=0 f=0 g=0 … ok=0` — caught (receipt binding works) |
| SOURCES S221 locator cell forged (`sha256` → `deadbeef…`, size → `999999 B`, stamp → `"Last updated on January 1, 1999"`) | `… ok=1` — **still TARGET_MET** |

The last row is the important one: **the counter never checks the `SOURCES.md`
locator cell's sha256/size/stamp against the receipt.** It checks only the
`Gate` line in `corpus/lessons/round-38.md` (clause `d`), which is a different
file with a different field. That is precisely why the bad `35046 B` / wrong
revision stamp in the S221 row could sit undetected from the data commit
`245065c` until a wave-1 reviewer read it — the counter was structurally
incapable of noticing. The fleet census validator does not check sizes either
(`grep -c "sha256" scripts/sources-census.sh` → 0), so no other gate covered it.

Note also that the counter's own `LINEAGE` phrase list for this entry contains
four phrases but requires only `NEED = 3` of them
(`LINEAGE = {"corpus/knowledge/hyprctl-flags-r28.md": (3, [...])},` — the
fourth phrase, `"dispatched by the compositor synchronously"`, is *not* present
in the entry at all, since the entry words it as "dispatched by the compositor
synchronously" split across a markdown line break inside the code span; the
normaliser strips `*` and backticks but not newlines, so the phrase misses).
So the floor is satisfiable without the warning's wording being present.

---

## 7. Verdict per assigned item

| # | Item | Verdict |
|---|---|---|
| 1 | Independent re-fetch to `/tmp/mado38-ScoutS221/` | **PASS** — HTTP 200, 306865 B, sha256 `35046ba0dc1dd1db4b1e8548e7e6a0be9f0ffc0051c055f66ddee5451879d30a` |
| 2 | `cmp` with `LANE/.ufo/waves/round-38/fetch/S221.bin` | **PASS** — byte-identical, no bytes moved (3 independent fetches incl. cache-bust) |
| 3 | Extract `flag list:` block verbatim | **PASS** — three lines, extracted above |
| 4 | Extract synchronous warning verbatim | **PASS** — extracted above; byte-exact ×3 in the receipt |
| 5 | Entry's three flag quotes verbatim (entities handled) | **PASS** — all three exact match after `&gt;`→`>` |
| 6 | Does today's page still say what the entry claims? | **YES** — every S221-sourced OBS holds; the unversioned current page carries the identical block and warning |
| 7 | F1 — S221 size/revision cells | **fixed at HEAD**; was wrong at the landed data commit (`35046 B` = digest prefix; stamp was S187's "May 2, 2026"). Verified corrected to `306865 B` / "June 13, 2026" |
| 8 | F2 — entry's §3 UNK mis-cites r25 for the strip fact and calls the server-side handling unmeasured while the lane holds it (S158) | **FINDING (MEDIUM)** |
| 9 | F3 — entry's §1 INF over-states `r` ("so the reply reflects the new state"); S158 shows the reload runs *after* the reply is built | **FINDING (MEDIUM)** |
| 10 | F4 — the domain counter never binds the `SOURCES.md` locator sha/size/stamp, and only one of the entry's four quotes is gate-bound | **FINDING (MEDIUM, counter gap)** |

---

## 8. Notes on method and bounds

- **No lane production file was modified.** All mutations were made in
  `/tmp/mado38-ScoutS221/sb`, a `git clone --no-local` of LANE at `ff81aaf`
  (`git -C sb -c user.name=s -c user.email=s@i commit`). LANE's own `jj`/git
  state was never touched; `git status --porcelain` in LANE shows only the
  untracked wave-1 report files, all of them written by other agents.
- **No raw socket was opened** (no `socat`/`nc`/python socket), and **no
  compositor/config/service/package was mutated.** Two hyprctl **read** verbs
  were run, both permitted by the bounds: `hyprctl --help` and `hyprctl version`.
  `hyprctl --help` is client-local — its description strings are embedded in
  `/usr/bin/hyprctl` (`strings /usr/bin/hyprctl | grep -c "Gets the active window
  name and its properties"` → 1), so no request was made for it. `hyprctl
  version`, however, **is** compositor-served: upstream registers it as a
  request (`src/debug/HyprCtl.cpp:2011` `registerCommand(SHyprCtlCommand{"version",
  true, versionRequest});`, handler at `:1089-1091` → `Helpers::SystemInfo::getVersion`),
  and the format string `"Hyprland {} built from branch {} at commit {} {} ({})."`
  lives in `src/helpers/SystemInfo.cpp:72`, **not** in the client binary
  (`strings /usr/bin/hyprctl | grep -c "built from branch"` → 0). So that one
  read verb did traverse the host's request socket as a normal, side-effect-free
  `version` request. I flag it explicitly rather than leave it ambiguous: it
  was a permitted read verb, it sent no request data beyond the literal word
  `version`, and it changed no compositor state — but it was a socket round
  trip, not a local binary read.
- **No tool was installed** — `curl`, `python3`, `awk`, `sed`, `sha256sum`,
  `cmp` and `git` from the base system were sufficient. No pacman transaction
  was run (paused host-wide per the operator directive).
- Privacy: only digests, byte counts, and page/heading text are quoted; no
  journal lines or window titles.
- Upstream cross-checks used `raw.githubusercontent.com` at the pinned commits
  (`efb50993…`, `a1c2428f…`) and `wiki.hypr.land`; the GitHub REST API was
  rate-limited (403), so tree listings were not available — but every source
  file I needed was fetchable directly by path, and each was checked by digest
  against the lane's own pinned receipt rather than by path.
