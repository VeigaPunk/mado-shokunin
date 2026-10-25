# CritLiterature — restated reject for `two-literature-drift-r26.md`

Task: round-33-verifier-spotcheck routed defect 3 — "Restate the literature
reject against the opened file's ids (S210/S211 CSDN), not S199."

## What the staged file actually cites

Opened: `/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/two-literature-drift-r26.md`
(112 lines, verified 2026-10-24). Its `source:` header block declares exactly
four ids:

```
source: S206 — https://mirror.sjtu.edu.cn/archlinux-cn/aarch64/arch-wiki-docs-zh-cn-20260901-1-any.pkg.tar.zst — `§ 使用 → hyprctl 和 IPC` — package `arch-wiki-docs-zh-cn-20260901-1`
source: S209 — https://wiki.archlinux.org/index.php?title=Hyprland&action=raw — `[[Category:Wayland compositors]]` — page fetch 2026-10-23
source: S210 — https://blog.csdn.net/2301_76324845/article/details/149787804 — `§ windowrules.conf 修改` — post `149787804`
source: S211 — https://blog.csdn.net/lxyoucan/article/details/164457293 — `§ hl.bind` — post `164457293`
```

Full id list carried by the file: **S206, S209, S210, S211**, plus one inline
mention of **S190** at `§2` ("wave-1 row S190") — an internal cross-reference,
not a declared source. `S199` appears nowhere in the file.

## The defect restated

Round-32 lesson `corpus/lessons/round-32.md:51` rejected the entry as
`(S195, S198, S199)`; round-33 lesson `corpus/lessons/round-33.md:18-19`
repeated the reject naming `S199` as "a community tier-C source". S195/S198/
S199 are ids from the round-32 *staged row register*, not ids inside this
file — the entry's real community tier-C rows are S210 and S211 (both CSDN
blog posts). The reject verdict stands on both grounds
(round-33-verifier-spotcheck: `agree`); only the cited id is stale.

## Restated reject (proposed correction)

> - Reject: `two-literature-drift-r26.md` (S206, S209, S210, S211).
>   Documentation localization is outside PROVINCE.md — the entry's subject is
>   how the Chinese and Japanese ArchWiki translations lag the English article,
>   a translation-lag surface that teaches nothing about mado's province, "the
>   Hyprland/waybar/walker configuration plane and display behavior on this
>   host" (PROVINCE.md domain line; no localization surface is claimed as of
>   round 34). Its tier reason: S210 and S211 are CSDN blog posts, kind
>   `community`, tier C, and tier C is never sole support for an admitted
>   entry (CORPUS.md tier rule). Flip: a desktop/compositor surface cited only
>   from tier A or B, opened by this lane.

## Evidence

- Staged file `source:` block quoted above, file read in full 2026-10-24.
- `corpus/lessons/round-33-verifier-spotcheck.md:110` — "the lesson's `S199`
  id is not in the opened file (it cites S206, S209, S210, S211). The reject
  stands; the id is stale."
- `corpus/lessons/round-33-verifier-spotcheck.md:123` — routed defect 3
  (this task).
- PROVINCE.md domain line: "desktop & compositor craft — the Hyprland/
  waybar/walker configuration plane and display behavior on this host";
  `Refuses:` list contains no localization surface.
