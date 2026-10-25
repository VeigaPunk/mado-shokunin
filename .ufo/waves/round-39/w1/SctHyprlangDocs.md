# SctHyprlangDocs — S218 source opening (mado round 39, wave 1)

Seat: `SctHyprlangDocs` (leaf scout; no subagents, no background jobs, no tools installed).
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Writes made: **this report** and the receipt
`.ufo/waves/round-39/w1/SctHyprlangDocs/S218.bin` — nothing else (verified below).
Host safety: no pacman, no service/compositor mutation, no socket connect, no input injection;
host config trees read-only (read only, bytes copied into the receipt, never written back).

## What was asked

Open the S218 source — Hyprland configuration/option-syntax documentation — fetch the bytes to
`.ufo/waves/round-39/w1/SctHyprlangDocs/S218.bin` with a sha256, and record the exact anchor
(section/line) plus a ≤25-word quote grounding the **last-declarer / option-syntax** claim,
access date 2026-10-25. If the page is unreachable, try the pinned raw.githubusercontent
equivalent and record both attempts.

## Attempt 1 (the URL named in the task) — UNREACHABLE (HTTP 404)

```
$ curl -sS -L --max-time 40 -A "Mozilla/5.0 (X11; Linux x86_64)" \
    -o /tmp/S218_vars.html https://wiki.hypr.land/Configuring/Variables/
HTTP_STATUS=404   (exit 0, 924 bytes — Hextra 404 page, not documentation)
```

The wiki was restructured on 2026-08-29 (wiki commit `cba1dbc509d3ab753cd1dbf48e50b7df25297ed9`,
"major wiki restructure, minor fixes, rewording (#1616)"); the old `Configuring/Variables/`
route is gone. Current `sitemap.xml` (14 127 B, fetched 2026-10-25) lists no `variables` page
under `/configuring/`; the option table now lives at
`https://wiki.hypr.land/configuring/core/config-options/` and the hyprlang syntax page at
`https://wiki.hypr.land/hypr-ecosystem/dev/hyprlang/`.

## Attempt 2 (pinned raw.githubusercontent equivalent of the *current* hyprlang page) — REACHABLE (HTTP 200)

```
$ curl -sS -L --max-time 40 -o /tmp/pin_main_hyprlang.md \
    https://raw.githubusercontent.com/hyprwm/hyprland-wiki/026b282bdde916bb7ce77689857f40cf1e829e82/content/hypr-ecosystem/dev/hyprlang.md
HTTP=200   4772 bytes   sha256 8ce3d33ea39757ed7316fd4146d0b0fed975c79fca1ab912153e5ed1acc9e60e
```

(`026b282bdde916bb7ce77689857f40cf1e829e82` = hyprland-wiki `main` HEAD at 2026-10-25T09:15:08Z.)
The same file at the pre-restructure commit `263edbb1cc1ed4a30ebf5347179b52a5b009468f`
(2026-08-26) is at `content/Hypr Ecosystem/hyprlang.md`: HTTP 200, 4788 bytes,
sha256 `d46c00b36f42a33111378e2a57aea9dbb805314089ece57977e28b6f805b81c4`.
Both pinned revisions carry the option-overwrite sentence verbatim (`:22` and `:21`
respectively; the only difference on that sentence is where the line wraps). The two files
otherwise differ only in line wrapping, backtick styling, the front-matter `weight`
(103 → 40) and one comma in the "Categories" sentence — i.e. the same prose.
The receipted 0.56.0 rendering carries the *older* wording
("Categories can be regular, and \"special\"."), so it corresponds to the pre-restructure
markdown revision, as expected for an archived version page.

## Attempt 3 (the rendered wiki page) — REACHABLE (HTTP 200); **this is the receipted bytes**

```
$ curl -sS -L --max-time 40 -A "Mozilla/5.0" -o /tmp/x_0.56.0_Hypr-Ecosystem_hyprlang_.html \
    https://wiki.hypr.land/0.56.0/Hypr-Ecosystem/hyprlang/
HTTP=200   283101 bytes
sha256 218da390ac96bc9452090eaf74f36f7e5f61897502b22c201fc875ea82c2a0f8
```

Also fetched (HTTP 200), for era pinning and cross-checking, not receipted:

| URL | bytes | sha256 | page revision |
|---|---|---|---|
| `https://wiki.hypr.land/0.56.0/Hypr-Ecosystem/hyprlang/` (receipted) | 283 101 | `218da390ac96bc9452090eaf74f36f7e5f61897502b22c201fc875ea82c2a0f8` | "Last updated on March 31, 2026" |
| `https://wiki.hypr.land/hypr-ecosystem/dev/hyprlang/` (live, post-restructure) | 284 891 | `a29cc41a889e7fe3e70ba558c922ab2fce3b702def8f0ed722a8aefe18f30892` | "Last updated on October 25, 2026" |
| `https://wiki.hypr.land/0.54.0/Configuring/Keywords/` | 146 383 | `0740a0c47416623ff822c69033a25db5314ee2a0eb8fc2a41fc70af77b2a603d` | "Last updated on November 18, 2025" |
| `https://wiki.hypr.land/0.56.0/Configuring/Basics/Variables/` | 364 905 | `400d18195020316c25e1874e567d868458b69e342a019b3ec8da6211d7222801` | "Last updated on July 17, 2026" |
| `https://wiki.hypr.land/0.56.0/Configuring/Start/` | 276 051 | — | (Lua-era; `require()` replaces `source =`) |

**Receipt written**: `.ufo/waves/round-39/w1/SctHyprlangDocs/S218.bin`
(283 101 bytes, sha256 `218da390ac96bc9452090eaf74f36f7e5f61897502b22c201fc875ea82c2a0f8`,
verified after copy: `sha256sum` matches the fetched file byte-for-byte).

## Why the 0.56.0 archive copy and not the live page — era matching

The host runs **Hyprland 0.56.2** (`hyprctl version` → "Tag: v0.56.2, commits: 7661",
commit `efb50993780079460b0cbed1363e2166a2de1d9f`, built 2026-08-05; `pacman -Q hyprland` →
`0.56.2-4`, `hyprlang` → `0.6.8-5`), and its config is **hyprlang-era**, not Lua-era:
`~/.config/hypr/hyprland.conf` uses `source = ~/.config/...` lines and `~/.config/hypr/*.conf`
uses `general { … }` blocks — no `.lua` file exists in `~/.config/hypr/`
(`ls ~/.config/hypr/*.lua` → "no lua").
`https://wiki.hypr.land/0.56.0/Configuring/Basics/Variables/` even says "Looking for the old
hyprlang syntax? Check the 0.54 wiki pages." The 0.56.0 archive's hyprlang page is therefore
the era-correct rendering of the hyprlang option syntax the host actually parses; the live
page is the same prose under the post-restructure route. Both are recorded; the receipt is
the 0.56.0 archive copy.

## The anchor and the quote (≤25 words)

**Primary anchor (the last-declarer / option-syntax claim)** — rendered page
`https://wiki.hypr.land/0.56.0/Hypr-Ecosystem/hyprlang/`:

- Section: **`## Syntax` → `### Line Style`** (permalink id `line-style`; the h3 carries
  `<span class="hx:absolute hx:-mt-20" id="line-style">` and `<a href="#line-style" …>`).
- Line: **rendered-text line 478** of the tag-stripped text extraction
  (heading `## Line Style` at extracted line 471); in the raw HTML the sentence is at
  **byte offset 255 777**, **raw HTML line 2887**, inside the `<p>` that begins at byte 255 680.
- Same sentence in the pinned raw source: `content/Hypr Ecosystem/hyprlang.md:22`
  (commit `263edbb1…`) and `content/hypr-ecosystem/dev/hyprlang.md:21` (commit `026b282b…`).
- Quote (18 words):

  > "Options can be specified only once (if you do it more times, the previous one will be overwritten)"

**Secondary anchor (variables + comments syntax, same page)** — `## Syntax` →
`### Defining variables` (extracted line 501) and `### Comments` (extracted line 512; the
comments sentence at extracted line 513):

  > "Comments are started with the # character."  (and: "If you want to escape it … you can use ##.")

**Tertiary anchor (the `source` include + LINEAR ordering — the actual include semantics of
the hyprlang era)** — `https://wiki.hypr.land/0.54.0/Configuring/Keywords/`,
section **`## Sourcing (multi-file)`** (extracted heading line 250; the `source`-keyword sentence
at 251, the `source =` examples at 253–254, the LINEAR note at 257; raw HTML byte offset
126 989 for the sentence, raw HTML line 1457):

  > "Please note it's LINEAR. Meaning lines above the source = will be parsed first, then lines inside …"

## What the source teaches (and its tier)

**Tier A — official project documentation** (wiki.hypr.land, the Hyprland project's own wiki;
the same page is the source repository's `content/` markdown, so the wording is
version-controlled, not prose-in-a-blog).

1. **Option syntax is `COMMAND = VALUE` on one line**, the command being either a *variable*
   (an option) or a *keyword* (a command): "Every config line is a command followed by a value."
2. **Last-declarer wins, and the wiki states it as an overwrite of the previous value** — the
   quoted "specified only once … the previous one will be overwritten" is the documented
   last-declarer rule *inside one category*.
3. **Includes are the `source` keyword, and they are LINEAR** — lines above a `source =` are
   parsed first, then the sourced file's lines, then the lines below. Together with (2) this
   gives the cross-file last-declarer order that a config-tree option resolver needs.
4. **Variables are `$NAME = value`**, referenced as `$NAME`, with `{{ }}` arithmetic and
   `# hyprlang if` conditional blocks; **comments start with `#`**, escaped as `##`.

This is the ground the round-39 C2/C3 option-ownership table (`tools/mado-options.py`,
`corpus/knowledge/config-option-table-r39.md`) needs: the *documented* rule is that the
effective value of an option is the last declaration in parse order, and parse order across
`source`-included files is linear.

### Corroboration from the host's own installed code (context, not the S218 row)

Read-only inspection of the pinned upstream sources at the host's commit
(`efb50993780079460b0cbed1363e2166a2de1d9f` / `hyprwm/hyprlang` `main`):

- `hyprlang/src/config.cpp`, `CConfig::configSetValueSafe` — the option value is looked up by
  the fully-qualified name `category:name` in `impl->values`; when the name is already
  present the existing entry is reused and its value is re-set
  (`VALUEIT->second.m_bSetByUser = true;` at the end of the function) — i.e. a later
  declaration overwrites the earlier one. Variables behave the same way
  (`CConfig::parseVariable`: `if (IT != impl->variables.end()) IT->value = rhs;`).
- `Hyprland/src/config/legacy/ConfigManager.cpp` — the compositor's own `source` handler
  (`handleSource`, line 1802 ff; registered at line 614 as `m_config->registerHandler(&::handleSource, "source", {false});`)
  expands globs, skips directories and refuses non-regular files (lines 1811–1847).

[INFERENCE] The documented "previous one will be overwritten" plus LINEAR `source` ordering
is the same rule the code implements (lookup-by-name, re-set on redeclaration); the code read
is consistent with the wiki text but the wiki text remains the cited S218 row.

## Unknowns / limits

- The SOURCES row's `kind` for this page (`docs`) and the exact row id (S218) belong to the
  C3 row writer — this seat only opened the source and fixed the anchor/quote/sha256.
- The receipted bytes are the **0.56.0 archive** rendering. The live page
  (`a29cc41a…`) contains the same two sentences but differs in surrounding prose and in the
  page revision date; a counter that pins the live URL would need a separate receipt.
- The "last-declarer" phrase in the task is a lane vocabulary item; the wiki's own wording is
  "the previous one will be overwritten". No page uses the literal phrase "last declarer";
  the *Lua-era* page uses a different wording — "the latest line will always shadow all
  previous lines" (`content/configuring/core/config-options.md:35`, commit `026b282b…`,
  sha256 `cea4d393ae9faf3efba24348042dc839e72e53312f8f649537793a7200b9371d`) — which is
  **not** the host's era and must not be cited as the host's semantics.
- `standards.hypr.land` (linked from the hyprlang page as its developer docs) does not
  resolve from this host (`curl: (6) Could not resolve host: standards.hypr.land`), so that
  secondary pointer could not be opened.

## Write-scope audit

```
$ git status --porcelain            # lane repo, read-only inspection
?? .ufo/waves/round-39/w1/           # my seat dir: S218.bin (new) + this report
?? .ufo/waves/round-39/w1-dispatch.json, w1-plan.err, …  # orchestrator files, not mine
?? quality/counters/c3-r39-options.py, tools/mado-options.py   # other seats' work, not mine
```

No tracked file was edited; no git/jj index operation was run in the lane; no file was written
outside `.ufo/waves/round-39/w1/SctHyprlangDocs/` (the receipt) and this report. Scratch
(`/tmp/*.html`, `/tmp/*.md`, `/tmp/*.json`) stayed under `/tmp`.

## Summary

| Item | Result |
|---|---|
| Named URL `wiki.hypr.land/Configuring/Variables/` | HTTP 404 (page removed by the 2026-08-29 wiki restructure) — attempt 1 recorded |
| Pinned raw.githubusercontent equivalent (`hyprland-wiki@026b282b…/content/hypr-ecosystem/dev/hyprlang.md`) | HTTP 200, 4772 B, sha256 `8ce3d33e…` — attempt 2 recorded |
| Rendered page receipted | `wiki.hypr.land/0.56.0/Hypr-Ecosystem/hyprlang/`, HTTP 200, 283 101 B, sha256 `218da390…` |
| Receipt | `.ufo/waves/round-39/w1/SctHyprlangDocs/S218.bin`, sha256 `218da390ac96bc9452090eaf74f36f7e5f61897502b22c201fc875ea82c2a0f8` |
| Anchor | `## Syntax` → `### Line Style` (`id="line-style"`), rendered-text line 478, raw HTML byte 255 777 / line 2887 |
| Quote (18 words) | "Options can be specified only once (if you do it more times, the previous one will be overwritten)" |
| Tier | A (official project documentation) |
| Access date | 2026-10-25 |
| Tools installed | none |
