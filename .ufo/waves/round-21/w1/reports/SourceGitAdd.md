# SourceGitAdd — upstream source evidence

## Axes

- **C1 — operability residual repair:** supports precise treatment of the `git add` dry-run versus intent-to-add distinction in future oracle judgments.
- **C2 — calibration independent artifact integrity:** preserves a versioned, hash-identified upstream source artifact independent of tool measurements. This is source evidence, not a gate or calibration measurement.

## Located source

- URL: https://raw.githubusercontent.com/git/git/v2.56.0/builtin/add.c
- Accessed: 2026-10-21; version/tag: Git v2.56.0.
- Saved body: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/sources/SourceGitAdd/add.c` (20,606 bytes; 699 lines).
- SHA-256: `c96956fdbba0943e3458fd19eaad9e5a21e9953b42f03109abb17b023f76c09b`.
- Receipt: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/sources/SourceGitAdd/receipt.json`.
- Located quote (12 whitespace-separated code tokens), `builtin/add.c:572-573`:

  > `(show_only ? ADD_CACHE_PRETEND : 0) |`
  > `(intent_to_add ? ADD_CACHE_INTENT : 0) |`

The relevant anchors are `OPT__DRY_RUN(&show_only, ...)` at line 262; `OPT_BOOL('N', "intent-to-add", &intent_to_add, ...)` at line 276; the dry-run/intent flag selection at lines 571-574; and forwarding of flags to `add_file_to_index` in `add_files` at line 371. Thus this file shows that the two options select distinct flags which are forwarded into index handling.

## Scope and existing coverage

`builtin/add.c` alone does **not** show the object-store write/no-write implementation: it forwards the flags to `add_file_to_index`. The targeted search for direct object-writer identifiers in this file returned no matches. This source artifact therefore corroborates option and flag routing, but is not independent proof that intent-to-add writes an object or that dry-run writes none; the downstream implementation must be used for that conclusion. No command or snippet was executed.

According to `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md`, existing row **S100** covers the same behavioral distinction at v2.56.0: it records the `git add -n` documentation and `-N` boundary, cites `builtin/add.c:262` and `parse-options.h:568`, and records the `read-cache.c` no-write path plus the distinction that intent-to-add writes an object. This is adequate existing S-row coverage of the behavior as catalogued, but this seat did not reopen those downstream source files to independently revalidate the recorded path. S100 does not include this newly saved `builtin/add.c` body or its direct `--intent-to-add` / `ADD_CACHE_INTENT` anchors at lines 276 and 572-573. No SOURCES row was added; registration reserves new source IDs for L1.

## Limits

This is static evidence from the tagged upstream source only. It does not establish runtime behavior, host Git binary equivalence, or behavior of combined `--dry-run` and `--intent-to-add` without inspecting the downstream implementation. No tools were installed or updated.
