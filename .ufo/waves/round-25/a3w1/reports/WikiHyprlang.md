# WikiHyprlang — pinned hyprlang page source report

## Behavior and findings

Opened the hyprlang page from the Hyprland wiki pinned at `c66e8de21f5ecdc4bc5e278e7d94800ea10957af`. The pinned ecosystem index links to `./dev/hyprlang`; the fetched page is `content/hypr-ecosystem/dev/hyprlang.md`.

The page documents that `#` starts comments, `##` escapes a literal `#` into the line, and configuration supports regular and special categories. A static bind resolver must not treat every `#` as an unconditional comment delimiter: the documented escaped form contributes a literal hash to the line. The page also shows categories as blocks and special categories with keys, but does not describe bind-specific category handling.

The page contains no `source` occurrence and does not document `source =` file selection, include/glob behavior, or how Hyprland constructs the bind table. Consequently, it supports C1's config-syntax parsing context but is not evidence for source-graph resolution or the expected 18-field bind output. Its contents do not mention a specific Hyprland or hyprlang release; the source identity here is the pinned wiki commit.

## Source metadata and located quotes

- Raw URL: `https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/hypr-ecosystem/dev/hyprlang.md`
- Local capture: `.ufo/waves/round-25/fetch/a3w1/WikiHyprlang.bin`
- SHA-256: `8ce3d33ea39757ed7316fd4146d0b0fed975c79fca1ab912153e5ed1acc9e60e`
- Size: 4,772 bytes; 193 lines (below the 2 MB limit).

1. `content/hypr-ecosystem/dev/hyprlang.md:74` — “Comments are started with the `#` character.”  
   This teaches a resolver that `#` starts comment handling, while the following escape rule constrains where it can truncate a line.
2. `content/hypr-ecosystem/dev/hyprlang.md:76` — “If you want to escape it (put an actual `#` and not start a comment) you can use `##`.”  
   This teaches that a static resolver must distinguish escaped literal hashes from comment starts when parsing bind lines.
3. `content/hypr-ecosystem/dev/hyprlang.md:77` — “It will be turned into a single `#` that _will_ be a part of your line.”  
   This teaches that `##` is transformed into a literal hash in the parsed line, rather than merely suppressing comment handling.
4. `content/hypr-ecosystem/dev/hyprlang.md:27` — “Categories can be regular or "special".”  
   This teaches that the configuration language has category constructs; the page's examples show block and keyed-special forms, but do not specify their bind-table effects.

The four quotes were checked against the downloaded UTF-8 bytes after collapsing whitespace; each quote is at most 25 words.

## Draft SOURCES row

| S? | hyprlang syntax page — https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/hypr-ecosystem/dev/hyprlang.md | docs | A | Hyprlang syntax relevant to bind-file parsing: comments, escaped hashes, and categories; not source-graph behavior | `content/hypr-ecosystem/dev/hyprlang.md:18-21,25-51,72-77 @ c66e8de21f5ecdc4bc5e278e7d94800ea10957af, sha256:8ce3d33ea39757ed7316fd4146d0b0fed975c79fca1ab912153e5ed1acc9e60e, 4772 B` | Documents comment and `##` escape rules plus category syntax relevant to parsing config lines; does not describe `source =` traversal or Hyprland bind-table construction | mined | 2026-10-23 | on-release | corpus/knowledge/bind-table-r25.md |

The URL does not duplicate any row in `corpus/SOURCES.md`; an exact-URL search of the full file returned no matches. In particular, the recent Hyprland/wiki rows S153–S168 cover different source files and URLs.

## Fetch and validation evidence

Fetch command:

```sh
timeout 60 curl -fsSL 'https://raw.githubusercontent.com/hyprwm/hyprland-wiki/c66e8de21f5ecdc4bc5e278e7d94800ea10957af/content/hypr-ecosystem/dev/hyprlang.md' -o '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/fetch/a3w1/WikiHyprlang.bin'; rc=$?; printf 'exit=%s\n' "$rc"
```

Observed output:

```text
exit=0
```

Metadata command and observed output:

```sh
sha256sum .ufo/waves/round-25/fetch/a3w1/WikiHyprlang.bin && wc -c -l .ufo/waves/round-25/fetch/a3w1/WikiHyprlang.bin
```

```text
8ce3d33ea39757ed7316fd4146d0b0fed975c79fca1ab912153e5ed1acc9e60e  .ufo/waves/round-25/fetch/a3w1/WikiHyprlang.bin
 193 4772 .ufo/waves/round-25/fetch/a3w1/WikiHyprlang.bin
```

Python quote validation decoded the captured bytes as UTF-8, collapsed `\s+` to a single space in the document and each quote, asserted each quote was a substring, checked its source line, and asserted no quote exceeded 25 words. Output:

```text
QUOTE_OK line=74 words=7
QUOTE_OK line=76 words=19
QUOTE_OK line=77 words=16
QUOTE_OK line=27 words=6
bytes=4772 lines=193 quotes=4
```

The exact-URL search of `corpus/SOURCES.md` returned `No matches found`.

## Gates, touched surfaces, and limits

- **Source-opening gate:** met for the pinned hyprlang page; fetched bytes, hash, line anchors, and four checked quotes are recorded above. This item does not establish source inclusion semantics or actual Hyprland bind-table behavior.
- **C1 control/counter and implementation:** not run; no control program or resolver was built. No C1 control verdict is claimed.
- **C2, host behavior, and nested Hyprland oracle:** not run or claimed.
- **Touched surfaces:** the required page capture `.ufo/waves/round-25/fetch/a3w1/WikiHyprlang.bin` and this report only. No file in `corpus/` or product code was edited; no tools were installed.
- **Known limit:** source/include behavior is not documented on this page and must be supported by another opened source; this report makes no claim about it.

Report: `.ufo/waves/round-25/a3w1/reports/WikiHyprlang.md`
