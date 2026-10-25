# ScoutHyprctlDocs — official documentation of `hyprctl getoption` for the host era

Seat: `round-40 / hyaku run 7 / w1 / ScoutHyprctlDocs`.
Scope: the 0.54.0 and 0.56.0 official wiki pages of *Using hyprctl*, what each
documents about `getoption` (flags, JSON, `set` field), located quotes, HTTP
status/date — compared with the lane's held row **S016**.
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
All compositor reads below used the allowed read-only verb
`hyprctl getoption -j <key>` / `hyprctl getoption <key>` only; no socket of my
own, no mutating verb, no package transaction.

Report: .ufo/waves/round-40/w1/ScoutHyprctlDocs.md

---

## 0. Bottom line for the two claims

| Question | Answer |
|---|---|
| Does the wiki document the four native reply forms (`int`/`float`/`str`/`custom`)? | **No** — the string `no such option`, `"set"`, `"option"`, `custom type` occur **0 times** in the normalized text of all three pages. |
| Does the wiki document the `set` field? | **No.** Neither the JSON reply shape nor `set` is documented anywhere on the page. |
| Does the wiki document the invocation form of `getoption`? | **Yes** — one line in the `Info` code block plus one paragraph on the option-name spelling. |
| Does the wiki's option-name spelling work on this host? | **No for 0.56.0/latest** (dot form → `no such option`); **yes for 0.54.0** (colon form). |
| Is held row S016 still accurate? | **Yes** — it is scoped to the *unversioned* page's `#getprop` section only, and that page still reads `Latest git` / `Last updated on August 26, 2026`. It does **not** cover `getoption`. |

**Consequence for C2:** the wiki is admissible as a source for the *invocation
form* of `getoption` (and for the flag vocabulary already held by S221), but it
**cannot** be cited as documentation of the native forms, of the `set` field, or
of the `no such option` reply. A C2 row built on a wiki page for the
native-forms entry would be citing a source that does not contain the claim.

---

## 1. Pages opened (HTTP status, date, bytes, digest)

Fetched 2026-10-25 with `curl -sS -L -D <hdr> -o <file>`; the wiki serves no
`Last-Modified` header, so the page's own revision date is the rendered footer
line `Last updated on <date>`.

| URL | HTTP | response `date:` header | bytes | sha256 |
|---|---|---|---|---|
| `https://wiki.hypr.land/0.54.0/Configuring/Using-hyprctl/` | **200** | Sun, 25 Oct 2026 20:50:47 GMT | 172 023 | `3f02dc8e4634111d1938d005c11cccd98a61b43ebddbd011b3ad674ce773cc29` |
| `https://wiki.hypr.land/0.56.0/Configuring/Advanced-and-Cool/Using-hyprctl/` | **200** | Sun, 25 Oct 2026 20:49:51 GMT | 306 865 | `35046ba0dc1dd1db4b1e8548e7e6a0be9f0ffc0051c055f66ddee5451879d30a` |
| `https://wiki.hypr.land/Configuring/Advanced-and-Cool/Using-hyprctl/` (unversioned = "Latest git") | **200** | Sun, 25 Oct 2026 20:51:03 GMT | 281 934 | `24c3987dd95986ef306edf14804c4a959c5846d4a105d70bb1d58f6b78c6b468` |
| `https://wiki.hypr.land/0.55.0/Configuring/Advanced-and-Cool/Using-hyprctl/` (cross-check) | 200 | Sun, 25 Oct 2026 20:49:58 GMT | 298 308 | `12cb63ae59eadcb82b4c7c7b1daa083a06322caffc0c8ef5f620db6454f0a985` |
| `https://wiki.hypr.land/0.53.0/Configuring/Using-hyprctl/` (cross-check) | 200 | — | 215 767 | — |
| **`https://wiki.hypr.land/0.54.0/Configuring/Advanced-and-Cool/Using-hyprctl/`** (the URL shape in my brief) | **404** | Sun, 25 Oct 2026 20:49:39 GMT | 924 (error page) | — |
| `https://wiki.hypr.land/latest/Configuring/Advanced-and-Cool/Using-hyprctl/` | 404 | — | 924 | — |

**Path correction (matters for any new row):** in the 0.54.0 archive the page
lives at `/0.54.0/Configuring/Using-hyprctl/`, **not** under
`/Advanced-and-Cool/`; the `Advanced and Cool` section grouping appears from
0.55.0 onward. The wiki version selector
(`https://wiki.hypr.land/version-selector/`, HTTP 200) lists versions
0.16.0 … **0.56.0** — there is no 0.56.2 wiki version, so 0.56.0 is the newest
published archive.

**Byte-identity result (useful for C2 receipts):** the 0.56.0 page I fetched is
**byte-identical** to the lane's already-held round-38 receipt
`.ufo/waves/round-38/fetch/S221.bin` (`cmp` → identical; 306 865 B, sha256
`35046ba0…`). The 0.56.0 page therefore needs **no new fetch** — the held
receipt already pins those bytes.

Captured pages are kept in my seat dir (not in `fetch/`, since my brief named
no receipt destination):
`.ufo/waves/round-40/w1/ScoutHyprctlDocs/wiki-0.54.0-using-hyprctl.html`,
`…/wiki-0.56.0-using-hyprctl.html`, `…/wiki-latest-using-hyprctl.html`
(digests as in the table above).

---

## 2. What the **0.54.0** page documents about `getoption`

Page revision: **"Last updated on February 21, 2026"** (§ footer).
Located quotes (all ≤25 words; each verified present in the page's normalized
text — tags/scripts stripped, entities decoded, whitespace collapsed — the same
normalization `quality/counters/c2-r40-forms-entry.py` applies to a receipt):

* `Info` code block (§Info):
  > "getoption [option] - gets the config option status (values)"
* paragraph immediately after the `Info` block:
  > "the option name should be written as section:option"
* same paragraph, example line:
  > "hyprctl getoption general:border_size"
* same paragraph, nested-section example:
  > "hyprctl getoption input:touchpad:disable_while_typing"
* `§Flags` flag list:
  > "j -> output in JSON"
  > "i -> select instance (id or index in hyprctl instances)"
* `§Batch`:
  > "You can also use --batch to specify a batch of commands to execute."
* `Info` code block, sibling command:
  > "descriptions - returns a JSON with all config options, their descriptions and types."
* page footer:
  > "Last updated on February 21, 2026"

**Absent from 0.54.0 (measured, not inferred):** the JSON reply shape, the
`set` field, the four native form names, and the failure text
`no such option` — 0 hits each. The `§Flags` list of 0.54.0 has **`j` and `i`
only** (no `r`); 0.55.0+ adds `r`.

---

## 3. What the **0.56.0** page documents about `getoption`

Page revision: **"Last updated on June 13, 2026"**. Byte-identical to the held
S221 receipt (above).

* `Info` code block (§Info):
  > "getoption [option] - gets the config option status (values)"
* paragraph immediately after the `Info` block:
  > "the option name should be written as section.option"
* same paragraph, example line:
  > "hyprctl getoption general.border_size"
* same paragraph, nested-section example:
  > "hyprctl getoption input.touchpad.disable_while_typing"
* `§Flags` flag list (three flags):
  > "j -> output in JSON"
  > "r -> force state refresh after issuing commands (e.g. layout or rule changes)"
* `§Batch`:
  > "You can use the legacy --batch flag to issue multiple commands separated with a ;."
* `Info` code block:
  > "descriptions - returns a JSON with all config options, their descriptions and types."
* page footer:
  > "Last updated on June 13, 2026"

**Absent from 0.56.0 (measured):** identical to 0.54.0 — no JSON reply shape,
no `set` field, no native form names, no `no such option`. The page has **no
`getoption` heading anchor at all**: the anchor ids are
`content, commands, eval, repl, dispatch, reload, kill, setcursor, output,
switchxkblayout, seterror, getprop, notes, notify, dismissnotify, info, batch,
flags`. So a row citing this page's `getoption` text must anchor on **`#info`**
(or `#flags` for the flag list) — there is no `#getoption` fragment to cite.

### 2.3 → 3: the spelling change between 0.54.0 and 0.56.0
0.53.0 and 0.54.0 use the **colon** form (`section:option`); 0.55.0, 0.56.0 and
the unversioned page use the **dot** form (`section.option`). Verified on the
0.55.0 page too: "the option name should be written as section.option".

---

## 4. Host-era cross-check (read-only `hyprctl getoption`)

Host: Hyprland **0.56.2**, commit `efb50993780079460b0cbed1363e2166a2de1d9f`
(`hyprctl version`), hyprlang **0.6.8**, `.conf` (legacy hyprlang) config tree.

**The 0.56.0 wiki's own example does not work on this host:**

```
$ hyprctl getoption -j general.border_size
no such option
$ hyprctl getoption -j general:border_size
{"option": "general:border_size", "int": 0, "set": true }
$ hyprctl getoption -j input.touchpad.disable_while_typing
no such option
$ hyprctl getoption -j general:col.active_border
{"option": "general:col.active_border", "custom": "ffe68e0d 45deg", "set": true }
```

Full sweep over the 70 declared keys of the frozen capture
(`.ufo/waves/round-40/c1/native-capture.jsonl`): **70/70 keys are colon-form**;
re-probing each of the 70 in dot form yields `no such option` **70/70 times**;
re-probing in colon form succeeds 70/70.

Why (source, pinned commit `efb5099`):
* `src/config/legacy/ConfigManager.cpp:1169-1184` — the legacy manager looks the
  key up **verbatim**: `m_config->getConfigValuePtr(val.c_str())`. The registered
  names are colon-form (`src/config/values/ConfigValues.cpp:168`:
  `MS<Int>("general:border_size", …)`).
* `src/config/lua/ConfigManager.cpp:1136-1141` — the **Lua-era** manager maps
  `:` → `.` (`luaConfigValueName`) and, at `:1030-1051`, accepts either spelling.
  The wiki's dot spelling therefore documents the **Lua config surface**, not the
  legacy `.conf` surface this host runs.
* `src/debug/HyprCtl.cpp:1647-1673` (`dispatchGetOption`) — the key is taken from
  the request and passed to `Config::mgr()->getConfigValue(curitem)`; a miss
  returns the literal string `"no such option"` (`:1670`), exit status 0 (measured
  on host for both `-j` and plain form).

**Practical consequence for C1's `--live`:** a tool built from the 0.56.0 wiki
would send `general.border_size` and read `no such option` for every key. The
key spelling that works on this host is the **colon** spelling — the same
spelling the 0.54.0 page documents and the same spelling the frozen capture
already uses.

---

## 5. Native forms: what the source actually admits vs what the host emits

This bears directly on C1's and C2's phrase "native replies (forms
int|float|str|custom)".

`src/debug/HyprCtl.cpp` (v0.56.2) `dispatchGetOption` JSON branch (`:1700-1723`)
contains **nine** format branches, not four:
`int`, `bool`, `float`, `vec2`, `str`, `custom` (×2: `void*` and
`Config::IComplexConfigValue`), `css`, `gradient`, `font_weight`; the plain
branch (`:1676-1699`) prints `int:`, `bool:`, `float:`, `vec2:`, `str:`,
`custom type:`, `css gap data:`, `gradient data:`, `font weight data:` followed
by `set: {bool}`.

On this host only **four** of those JSON keys ever appear, because the legacy
hyprlang path yields `Hyprlang::INT/FLOAT/STRING/CUSTOMTYPE`:
`animations:enabled` (a `bool` in the wiki's own Variables table) comes back as
`{"int": 1}`; `general:col.active_border` (declared `gradient`) comes back as
`{"custom": "ffe68e0d 45deg"}`; `group:groupbar:gaps_in` (declared `css_gaps`)
comes back as `{"int": 5}` while `general:gaps_in` comes back as
`{"custom": "0 0 0 0"}`.

⇒ **A claim of the form "the compositor's native forms are int|float|str|custom"
is true of this host's legacy path, false of the source in general.** The entry
should say "the four forms observed on this host's legacy `.conf` path", and the
source row should record the nine branches the handler admits.

The wiki's *Variables* pages carry a **different** type vocabulary again
(`bool, int, float, str, string, color, gradient, vec2, css_gaps, font_weight`),
and it does **not** predict the native reply key. Measured over the 61 capture
keys whose leaf name maps to exactly one wiki table row:

| wiki declared type | native reply key | rows |
|---|---|---|
| bool | int | 21 |
| int | int | 17 |
| gradient | custom | 8 |
| str | str | 6 |
| float | float | 4 |
| font_weight | custom | 2 |
| color | int | 2 |
| string | str | 1 |

(Source of the wiki column: `https://wiki.hypr.land/0.56.0/Configuring/Basics/Variables/`,
HTTP 200, 364 905 B, sha256 `400d18195020316c25e1874e567d868458b69e342a019b3ec8da6211d7222801`;
the 0.54.0 twin is `/0.54.0/Configuring/Variables/`, 230 663 B, sha256
`930ead523a898d5e766abadeff7c1bb48ae40ccc32bd77ff81e5ba61bba637ea`.)

---

## 6. Comparison with the lane's held row **S016**

Held row, verbatim (`corpus/SOURCES.md:28`):

> `| S016 | Using hyprctl — https://wiki.hypr.land/Configuring/Advanced-and-Cool/Using-hyprctl/ | docs | A | Current wiki's getprop purpose and invocation form | #getprop; page marked Latest git; modified 2026-08-26; opened 2026-10-19 | Separates the current documented property-read command from command effects; does not pin host behavior | mined | 2026-10-19 | 90d | corpus/knowledge/window-rule-effects-getprop.md |`

Re-checked 2026-10-25 against the same URL:

| S016 element | Measured now | Verdict |
|---|---|---|
| URL `https://wiki.hypr.land/Configuring/Advanced-and-Cool/Using-hyprctl/` | HTTP 200, 281 934 B | holds |
| "page marked Latest git" | `Latest git` appears in the page header nav | holds |
| "modified 2026-08-26" | footer `Last updated on August 26, 2026` | holds |
| anchor `#getprop` | `id=getprop` present on the `getprop` `<h3>` | holds |
| scope "getprop purpose and invocation form" | the page's `getprop` section still reads "Gets a property value of a window." | holds |
| "does not pin host behavior" | consistent with everything below | holds |

**What S016 does *not* cover:** `getoption`. Its scope is `getprop` only, and
the unversioned page's `getoption` material is the `Info` line plus the
dot-spelling paragraph. Re-using S016 for a `getoption` claim would be a scope
mutation; a *new* row (or a held-row re-open) is required.

**Re-check timing:** S016's `recheck` is `90d` from opened 2026-10-19 → due
2027-01-17; my reading does not yet force a re-open.

---

## 7. Constraints this places on a C2 registry row (checked against the frozen counter)

`quality/counters/c2-r40-forms-entry.py` clauses (c), (d), (e) interact with the
registry as it stands. What I verified against the live `corpus/SOURCES.md`:

**Clause (e)** — a new id's *location* (the last whitespace-separated token of
cell 1) must occur in **no other** registry row. Current occupancy:

| location token | held by |
|---|---|
| `https://wiki.hypr.land/Configuring/Advanced-and-Cool/Using-hyprctl/` | **S016** |
| `https://wiki.hypr.land/0.56.0/Configuring/Advanced-and-Cool/Using-hyprctl/` | **S221** |
| `https://wiki.hypr.land/0.54.0/Configuring/Using-hyprctl/` | **FREE** |
| `https://wiki.hypr.land/0.55.0/Configuring/Advanced-and-Cool/Using-hyprctl/` | **FREE** |
| `https://wiki.hypr.land/0.56.0/Configuring/Basics/Variables/` | **FREE** |
| `https://wiki.hypr.land/0.54.0/Configuring/Variables/` | **FREE** |
| `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/lua/ConfigManager.cpp` | **FREE** |
| `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/main/content/configuring/core/advanced-configuration/using-hyprctl.md` | token FREE (but see note) |

Note on the wiki raw-markdown URL: the held row **S167** uses the *same file*
pinned at commit `c66e8de21f5ecdc4bc5e278e7d94800ea10957af`; I fetched that
pinned blob and it is **byte-identical to `main` HEAD** (sha256
`95d8b8422a1fd25229bfe350e05624d8a318c746803efb7f3893015bf7c417f0`, 8 239 B), so
the file has not changed since that pin. A row citing `main` would satisfy
clause (e) on the token test but restate an already-held source — the honest
choice is the free, genuinely new location (the **0.54.0** Using-hyprctl page,
or the Lua ConfigManager source).

**Clause (c)** — a held id keeps cells 1-10 byte-equal to its BASE row; a new
id must carry `opened 2026-10-25`. At BASE (`9fc511d`) S016 and S221 already
exist with their current cells (verified with
`git show 9fc511d:corpus/SOURCES.md`), so both may be cited as held rows
without rewriting; ≥2 of the cited ids must be new.

**Clause (d)** — each cited id needs a `GATE <id> receipt=<path> sha256=<64hex>
quote="<q>"` line in `corpus/lessons/round-40.md` §Gate, the receipt committed
under `.ufo/waves/round-40/fetch/`, the digest matching, and the quote (3-25
words) occurring in the receipt's normalized text. Quote candidates I verified
against the counter's own `norm()` on the captured bytes: all of §2/§3's
quotes are 3-25 words and match; the only candidate that failed the 3-word
minimum was the two-word nav label `Latest git` (use `Hyprland Wiki Latest git`
— 4 words — instead, also verified present).

---

## 8. Findings, separated by class

**Observed (measured on this host / in these bytes)**

1. `https://wiki.hypr.land/0.54.0/Configuring/Advanced-and-Cool/Using-hyprctl/`
   → **404**; the 0.54.0 page is at `/0.54.0/Configuring/Using-hyprctl/` → 200.
   *(attacks any row citing the brief's URL shape; supports the 0.54.0 URL I give)*
2. 0.54.0 documents colon option names; 0.55.0/0.56.0/latest document dot
   option names. *(attacks any "the wiki says X" claim spanning versions)*
3. `hyprctl getoption -j general.border_size` → `no such option`;
   `hyprctl getoption -j general:border_size` → the JSON reply. 70/70 dot-form
   probes fail; 70/70 colon-form probes succeed. *(attacks the wiki's 0.56.0
   example as a host instruction; supports colon spelling for C1's `--live`)*
4. `no such option` / `"set"` / `"option"` / `custom type` appear **0 times** in
   the normalized text of the 0.54.0, 0.56.0 and unversioned pages. *(attacks
   any wiki-cited native-forms or `set` claim; supports sourcing them from
   HyprCtl.cpp + the host capture)*
5. The 0.56.0 page has no `getoption` anchor; anchors are
   `… getprop, notes, notify, dismissnotify, info, batch, flags`. *(supports
   anchoring a row on `#info`)*
6. `dispatchGetOption` (v0.56.2 `src/debug/HyprCtl.cpp:1700-1723`) admits nine
   JSON keys; the host's legacy path emits four. *(attacks "the native forms
   are exactly four" as a source-level claim)*
7. The wiki Variables type column does not predict the native reply key
   (bool→int 21×, gradient→custom 8×, color→int 2×, font_weight→custom 2×).
   *(attacks a docs→form derivation)*
8. The wiki's `descriptions` line promises "types"; the host's
   `hyprctl descriptions -j` output has keys
   `current, default, description, map, max, min, name` — **no `type`** — and
   the pinned `jsonify` in `src/config/values/ConfigValues.cpp:28-147` emits no
   `type` key either. *(attacks the wiki's "types" wording as a host fact)*
9. The 0.56.0 page I fetched is byte-identical to the held
   `.ufo/waves/round-38/fetch/S221.bin`. *(supports reusing that receipt)*
10. The wiki repo's `using-hyprctl.md` is byte-identical at `main` HEAD and at
    S167's pinned commit (`95d8b842…`, 8 239 B). *(supports "already held")*

**Inference (labelled)**

11. The dot-vs-colon split tracks the config-language era: the dot form is what
    the **Lua** manager accepts (`luaConfigValueName`, `:`→`.`), the colon form
    is what the **legacy hyprlang** manager accepts verbatim. The host runs
    legacy `.conf`, hence colon. The wiki pages were re-worded to the Lua-era
    naming from 0.55.0 on. Confidence: high (source + host behaviour agree);
    the wiki's own rationale is not stated.

**Unresolved / not established**

12. Whether upstream would accept *both* spellings on a Lua-configured 0.56.2
    host — the Lua manager's dual lookup suggests yes, but no Lua-configured
    host exists here to test; not measured, so not claimed.
13. Which wiki revision produced the 0.56.0 archive text: the wiki repo has
    only one commit for the restructured path (`cba1dbc509d3`, 2026-08-29) and
    the pre-restructure path's history ends 2025-07-24 (`pages -> content`);
    the archive-vs-commit mapping for intermediate versions is not exposed by
    the API I used. The page-level "Last updated on" footer is the only
    revision signal for the archives.
14. Whether `hyprctl getoption` on the host accepts a key with an embedded
    space (`"general:border size"`) — measured `no such option`, consistent with
    `nextItem()` splitting on the first space (`HyprCtl.cpp:1650-1665`); not
    further characterised.

---

## 9. Recommendations to the integrator (L1)

1. **C2 — do not cite the wiki for the native forms.** The wiki pages contain no
   `set` field, no form names and no error text. Source the four observed forms
   from the pinned `HyprCtl.cpp` (`dispatchGetOption`, `:1647-1723`) plus the
   own-work host census receipt; the wiki may be cited for the *invocation
   form* only.
2. **C2 — a wiki row is still available and genuinely new** at
   `https://wiki.hypr.land/0.54.0/Configuring/Using-hyprctl/` (location token
   free; anchor `#info`; page revision "Last updated on February 21, 2026";
   receipt bytes already in my seat dir, sha256 `3f02dc8e…`). Its teaching
   content: the *hyprlang-era* spelling of a `getoption` key, which is the
   spelling that works on this host — and the contrast with the 0.56.0 page's
   dot spelling. Quote candidates (3-25 words, verified): "the option name
   should be written as section:option", "hyprctl getoption general:border_size",
   "Last updated on February 21, 2026".
   If instead the L1 wants the 0.56.0 page, note that its location token is
   **already held by S221** — that row must be re-opened (cells 1-10 unchanged)
   rather than duplicated.
3. **C1 — keep the colon spelling.** The `--live` implementation must send
   colon-form keys; the wiki's 0.56.0 example would make every probe return
   `no such option`. The frozen capture's 70 keys are already colon-form, so
   the tool and the capture agree.
4. **C2 — phrase the forms claim host-scoped**: "four forms observed on this
   host's legacy `.conf` path", with the source row recording the nine branches
   the handler admits, so the entry is not falsified by the pinned source.
5. `S016` needs no change; it is scoped to `#getprop` on the unversioned page
   and still reads as recorded.

## 10. Tooling

No tool was installed or updated (nothing in this task needed one). Used:
`curl 8.23.0` (system, OpenSSL 3.6.5) and `python3 3.14.8` (system) for
fetching, header capture, digests and text normalization. No pacman or other
package transaction was run.

## 11. Scope compliance

* Written only under
  `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-40/w1/ScoutHyprctlDocs/`
  plus this report at
  `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-40/w1/ScoutHyprctlDocs.md`.
* No tracked file, no `fetch/` file, no registry, lesson, counter, tool or
  config tree was edited; no git/jj write anywhere; only read-only
  `git show`/`rev-parse` was used against the lane.
* Compositor verbs run: `hyprctl getoption -j <key>`, `hyprctl getoption <key>`,
  `hyprctl version`, `hyprctl descriptions -j` — read-only. No `keyword`,
  `dispatch`, `reload`, `setprop` or `--batch`. No socket of my own was
  connected; no host config bytes were copied.
* Scratch: `/tmp` only (fetched HTML), left in place for byte-identity checks.

Report: .ufo/waves/round-40/w1/ScoutHyprctlDocs.md
