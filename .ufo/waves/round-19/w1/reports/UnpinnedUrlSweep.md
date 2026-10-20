# MadoR19.UnpinnedUrlSweep — S084 confirmed as the routed defect; one unrouted sibling (S035); the other 21 alias rows are pinned, non-version-specific, or unused

## Question and denominator

- Ground truth is `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 17661e0:corpus/SOURCES.md` — 95 rows `S001`–`S095`, blob `2b8dd7c07db67eb2e748760bfd7ffbc6dad0a903`, working copy sha256 `9552071c0b286075ffabb3a7ea1373e8dbaef5e6c37f906d2620ae83454f26de`. Line numbers below are lines in that blob.
- Candidate class: URL is a moving alias — literal `latest`/`main`/`master`/`HEAD`, a wiki page, or a generated/unversioned docs site. **23 rows match.** The 2 literal `latest` rows are S007 and S084; the 1 literal `main` row is S005; no URL uses `master`/`HEAD`.
- Defect rule used for the last column, taken from this lane's own Gate (`corpus/lessons/round-18.md:33-36`): unversioned docs sites are admissible only for non-version-specific support; HTML is not sole support where its bytes are not reproducible; commit/tag/revid or a reproducible content digest are the admitted pins. **Real defect = moving URL + no durable pin in the anchor + used as support for a version- or release-bound claim.** This is stated because an alias alone is not a defect (S005/S042 are pinned by commit; the wiki rows are dated, non-version-specific statements).

## Table — every unversioned-alias row at 17661e0

| id | URL | pin in anchor | version-specific use? | real defect? |
|---|---|---|---|---|
| S005 (:17) | https://gitlab.freedesktop.org/wayland/wayland-protocols/-/blob/main/README.md | commit `3dac056d` (2026-01-16, last commit touching README.md); the note cites `blob/3dac056d…` (wayland-protocol-boundaries-r13.md:1) | no — protocol-phase policy, not a host/release claim | no |
| S006 (:18) | https://wayland.freedesktop.org/extras.html | none — "opened 2026-10-19" only | no — queued, `used-by —` | no (superseded by S042) |
| S007 (:19) | https://wayland.freedesktop.org/libinput/doc/latest/tools.html | none — `latest`; "libinput 1.32.0 documentation" is a label, not a tag/revision | no — queued, `used-by —`; S051 supplies tag 1.32.0 | no — but the same shape as S084; a trap if mined |
| S008 (:20) | https://wayland-book.com/introduction/high-level-design.html | none — "opened 2026-10-19" | no — queued, unused | no |
| S009 (:21) | https://wayland.freedesktop.org/architecture.html | none — "opened 2026-10-19" | no — queued, unused | no |
| S010 (:22) | https://wayland.app/protocols/ | none — "opened 2026-10-19" | no — queued; community discovery index, row says never sole support | no |
| S016 (:28) | https://wiki.hypr.land/Configuring/Advanced-and-Cool/Using-hyprctl/ | dated revision — page "Latest git", modified 2026-08-26 | no — current-wiki purpose/invocation; note says it does not pin host behavior | no |
| S017 (:29) | https://wiki.hypr.land/Configuring/Basics/Window-Rules/ | dated revision — modified 2026-08-26 | no — explicitly scoped to that wiki era; note labels it current-doc, not the 0.56.2 parser (window-rule-effects-getprop.md:36) | no |
| S029 (:41) | https://wiki.hypr.land/Configuring/Start/ | dated revision — modified 2026-08-26 | no — current-wiki path/status; note says not evidence about the installed binary | no |
| S030 (:42) | https://wiki.hypr.land/Configuring/Basics/Window-Rules/ | dated revision — modified 2026-08-26 | no — rejected duplicate of S017, unused | no |
| S031 (:43) | https://wiki.hypr.land/Hypr-Ecosystem/xdg-desktop-portal-hyprland/ | dated revision — modified 2026-08-26 | no — role/Fallback description, not release-bound | no |
| S032 (:44) | https://flatpak.github.io/xdg-desktop-portal/docs/ | access date only (2026-10-19), no revision/digest | no — frontend/backend model | no — weakest anchor class, admissible for non-version-specific use |
| S033 (:45) | https://flatpak.github.io/xdg-desktop-portal/docs/portals.conf.html | access date only | no — config precedence | no — weak anchor |
| S034 (:46) | https://flatpak.github.io/xdg-desktop-portal/docs/requests.html | access date only | no — request lifecycle | no — weak anchor |
| S035 (:47) | https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.ScreenCast.html | access date only; page self-declares "version 6", but no revision/digest | **yes** — the note reads it as "the current interface as v6" and joins it to the host's observed `version=6` (xdg-portal-routing-r12.md:25,:80) | **YES (latent)** — same class as S084, not routed by the round-18 verifier |
| S036 (:48) | https://flatpak.github.io/xdg-desktop-portal/docs/doc-org.freedesktop.portal.RemoteDesktop.html | access date only; "interface version 2" is a content label | no — queued, `used-by —` | no — trap if mined |
| S042 (:54) | https://wayland.freedesktop.org/extras.html | commit `8923a199` (2026-01-15, page source revision); note cites it | no — discovery-tool purpose, no behavior | no |
| S043 (:55) | https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_registry | installed `wayland 1.26.0-1` XML `:117-177`; note records sha256 `cc860987…`, also pinned by S052 at tag 1.26.0 | yes — core registry semantics at the installed 1.26.0 | no — the row/note name the local XML, not the HTML, as authority (wayland-protocol-boundaries-r13.md:86-90) |
| S045 (:57) | https://wiki.hypr.land/Configuring/Basics/Window-Rules/ | dated revision — modified 2026-08-26 | no — rejected duplicate, unused | no |
| S061 (:73) | https://wiki.archlinux.org/title/Alacritty | revid `869789` (2026-03-23) + raw sha256 `c39c563d…` | no — rejected, no version pin, unused | no |
| S063 (:75) | https://wiki.hypr.land/Hypr-Ecosystem/hypridle/ | raw HTML sha256 `b45c03dc…`; reproduced 2/2 re-fetches 2026-10-20 | no — row explicitly says not version-pinned to v0.1.8 | no |
| S064 (:76) | https://wiki.hypr.land/Hypr-Ecosystem/hyprlock/ | raw HTML sha256 `f69cff6b…`; re-fetch 2026-10-20 equals the row | no — documented defaults, not release-bound | no |
| S084 (:96) | https://docs.rs/xdg/latest/xdg/struct.BaseDirectories.html | saved-HTML sha256 `0291cfe6…` only (reproduces 3/3 to date) — no crate version, tag or commit; URL is `latest` | **yes** — supports walker v2.17.2's config search through the xdg crate that version locks (Cargo.lock 3.0.0); the row names no version | **YES — R18-V4 confirmed** (durability, not content) |

## S084 — the routed defect is real, and it is durability rather than a wrong claim

Evidence: `corpus/SOURCES.md:96`; body `.ufo/waves/round-19/fetch/MadoR19.UnpinnedUrlSweep/xdg-latest.html`; receipt `…/receipts.jsonl` line 1; `corpus/lessons/round-18.md:64`; `corpus/lessons/round-18-verifier-spotcheck.md:120`.

- Re-fetch 2026-10-20T17:07:22Z: HTTP 200, 105,537 B, sha256 `0291cfe6cd80b67fe6e4b276aae8323650d77dbfb88b1f3c9d0ff150b50f9f0d` — exactly the row's digest. The page currently serves `xdg-3.0.0`; located quote, body `:357`: "Searches `XDG_CONFIG_HOME` and then `XDG_CONFIG_DIRS`." (7 words). The claim is true today.
- The version is real and is the consumer's version: walker v2.17.2 `Cargo.lock:2705-2708` pins `name = "xdg"`, `version = "3.0.0"`, `checksum = "2fb433…"`; the crate body fetched by the SrcS084 seat (`fetch/SrcS084/xdg-3.0.0.crate`) has sha256 `2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5`, equal to that lock checksum.
- Why it is still a defect: the URL alias moves at the next xdg release and the anchor names no version, so after that point the digest cannot be reproduced from the row and a reader cannot distinguish 3.0.0 from newer. The row supports a release-bound route (`corpus/knowledge/walker-route-r18.md:33`, `:79-80`, `:293-294`), which is the Gate's excluded category "unversioned docs sites as version-specific support" (`corpus/lessons/round-18.md:35`).
- Concrete repair caveat: re-pointing to `https://docs.rs/xdg/3.0.0/xdg/struct.BaseDirectories.html` is **not** a drop-in re-pin. That page is 200 / 105,205 B / sha256 `adaec7c3…`, and the same prose sits at `:299`, `:303`, `:354`; the row's `:302` maps to `has_runtime_directory`, not the `XDG_CONFIG_HOME` default. Re-pointing the URL would require re-cutting every `XD` line anchor. S098's Cargo.lock + crate-tarball row is the durable support; a versioned docs URL is only a secondary convenience.

## S035 — an unrouted sibling of the same class

Evidence: `corpus/SOURCES.md:47`; body `…/fetch/MadoR19.UnpinnedUrlSweep/screencast-v6.html`; receipt line 6; `corpus/knowledge/xdg-portal-routing-r12.md:25,:80`; `corpus/lessons/round-18.md:35`.

- Re-fetch 2026-10-20T17:10:21Z: HTTP 200, 55,559 B, sha256 `b02ae540…`; located quote, body `:351`: "This documentation describes version 6 of this interface." (8 words). The v6 claim is true today.
- The row's anchor is section names + "interface version 6" + "accessed 2026-10-19" — no document revision, tag or digest. The URL is a generated docs page with no version segment, so a later interface-v7 rebuild lands on the same URL. Its use is version-bound: the note calls it "the current interface as v6" and joins it to the host's observed `version=6`.
- Severity is lower than S084: the anchor names the interface version, so a v7 page is at least detectable as drift; today's content is correct. It was not routed by the round-18 verifier. Fix shape: pin the portal XML at the `xdg-desktop-portal` release matching the installed frontend (or the interface XML inside that release) with `file:line`, the same shape as S035's sibling rows S052/S053/S054.

## Neutralized rows and live traps

- **Pinned despite an alias URL:** S005 and S042 (commit-pinned anchors, and the knowledge note cites the commit URL); S043 (installed 1.26.0 XML is named as authority and digest-pinned in the note, with S052 as an independent tag-1.26.0 pin); S061 (revid + raw digest); S063/S064 (reproducible raw-HTML digests: hypridle `b45c03dc…` twice, hyprlock `f69cff6b…` once, both equal to the rows).
- **Dated wiki rows:** S016/S017/S029/S030/S031/S045 carry the page-declared "modified 2026-08-26" revision and are used only as current-wiki/era-labeled statements, never as host-version evidence. No defect; S030/S045 are rejected.
- **Unversioned docs with access-date-only anchors:** S032/S033/S034 are non-version-specific (model, config precedence, request lifecycle) and therefore admissible under the Gate rule, but they are the weakest anchors in the corpus: no revision and no digest.
- **Queued/unused traps:** S007 (`doc/latest`) and S036 (docs site, interface v2) have the S084 shape but no live support (`used-by —`); S007 is already superseded by S051's tag-1.32.0 row, S006 by S042. Do not mine them without re-pointing.
- **Examined and excluded as not aliases:** S021/S024/S025/S027 are dated release announcements with release-versioned paths (`update53`, `update55`, `update56`, `26_lua`) and dated anchors; S012/S062/S070 are specific community articles (all rejected; S070 records per-fetch byte drift itself); S013 contains a literal `HEAD` in its anchor but is a local file with the full commit `133b867…`; S018/S022/S023/S026/S028/S037–S040/S046–S058/S065–S069/S072–S083/S085–S089/S092–S094 carry a tag, commit or version segment in the URL. S094's defect is a different class (per-fetch HTML digests, R18-V1), not an alias.

## Limits

- Did not re-fetch every row. Bodies actually fetched and receipted: docs.rs `latest`, docs.rs `3.0.0`, hypridle ×2, hyprlock, ScreenCast docs. All other "pin" cells are read from `SOURCES.md` anchors and the cited knowledge notes, not re-measured.
- Did not run `git ls-remote` to re-verify the commit hashes `3dac056d`/`8923a199` upstream, nor checksum the wiki pages behind S016/S017/S029/S031 to confirm the 2026-08-26 modification dates.
- Did not test whether the flatpak docs site keeps v6 text after a v7 release; the S035 defect rests on URL mutability, and the "rebuilt from the project's current docs" premise is `[INFERENCE]` from the URL shape (no version segment) and Sphinx build footer.
- No `lsp` server was used: the question is about registry rows and documentation pages, not code symbols; there is no file/symbol for `definition`/`references` to answer, and no semantic-code claim is made here. Text inspection of source files is quoted as file content, not as semantic proof.
- Did not check `used-by` claims outside the three notes cited, did not run any gate/suite/census, and did not edit any lane file. Fetch receipts and bodies are under `.ufo/waves/round-19/fetch/MadoR19.UnpinnedUrlSweep/`.

## Installs

none
