# PROVINCE.md insertion text — round 43 (seat `ScrSkillProvince`)

Draft only. Nothing here edits `PROVINCE.md` (sha256
`372b93f960f8360e7c62aca0cfd7508417f69e0c895562d90ad38a4d2f893cea` at this seat's read, 2026-10-26; clean in
`git status`). The L1 integrates.

## Tool row

**Insert as a new line after line 31** (`| tools/mado-globals.py | …`), i.e. as the new last row of the
`| Tool | Reads | Writes | Owner and adjacent lanes |` table (rows 24-31); line 32 is blank and line 33 is the
`**Round-23 wave-2 correction …**` paragraph.

```markdown
| `tools/mado-geometry.py` | the bytes of one or more caller-supplied Hyprland config files (`--rules`, each read whole, 1048576 B cap; a missing, unreadable, directory, FIFO or any non-regular path is a setup error) and one caller-supplied `hyprctl clients -j` dump (`--clients`, a regular file or `-` for standard input, at most 1048577 B, UTF-8 JSON holding a list of objects); no compositor socket, no Wayland client, no network, no config tree, no process started | nothing — stdout only (`MADO_GEOM_RULE:`, `MADO_GEOM_CLIENT:`, `MADO_GEOMETRY:` lines); `--selftest` writes only inside a private temporary directory it removes on exit | mado, round 43 (a read-only join of a rule's declared size against the goal box the compositor prints; it never reads the compositor itself — the caller supplies the dump — and an AGREE verdict says nothing about the rendered size, the client's own request or which rule wrote the box; the operator applies any rule change) |
```

## Why this cell wording, not another

- **Reads.** Both inputs are caller-supplied bytes, exactly as the frozen contract states them (counter docstring
  `quality/counters/c1-r42-geometry.py:7-10`, reference `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt:10-12`). The row
  must not say "reads the compositor": the tool has no socket and starts no process, which is the property the
  safe-probe fence cares about (SKILL.md safety rule 1, the hyprctl read-verb whitelist).
- **Writes.** Same shape as the `mado-globals.py` row above it: nothing, plus a `--selftest` that writes only inside a
  private temporary directory it removes. That is what the tool does at this seat's read of the reference; if the build
  seat's implementation differs, the row is the thing to correct, not the tool.
- **Owner.** The adjacent-owner cell keeps the lane's standard shape: mado owns the instrument; the operator applies any
  change; no sibling lane is named because none holds this surface (sibling scan
  `.ufo/waves/round-43/w1/ConnSiblingOverlap/overlap.md` §1/§4: zero overlaps fleet-wide; game-dev-2d reads the same
  `clients -j` verb for presence fields only, not `size`).
- The row does **not** claim the tool is a desktop surface: like `mado-binds.py`/`mado-anims.py` it is a static join of
  bytes, and the compositor half is a dump the caller took with a whitelisted read verb.
