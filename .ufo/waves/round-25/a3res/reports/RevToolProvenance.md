PROVENANCE: finding: config-directed absolute/environment source paths can read outside --home; A vs B agree 5/5

## Finding — source traversal is not confined to `--home`

`tools/mado-binds.py:159-162` seeds config variables from all of `os.environ`. The parser substitutes variables before dispatching `source` (`:402-424`); `absolute_path` returns an absolute source path unchanged (`:336-344`); `handle_source` globs/stats matches and sends regular files to `parse_file` (`:358-370`, `:440-444`). The root itself is also passed through `os.path.realpath` (`:485-489`), so a symlinked root can resolve outside the supplied home.

I reproduced both paths using fixtures only under `/fast/scratch/hyaku/mado-r25a3/res/RevToolProvenance/`: a literal absolute `source = /.../outside.conf` and `source = $EXTERNAL_CONFIG` each caused A and B to emit a bind defined in a sibling file outside `--home`. This is an external-read capability and means the strict property “all reads are beneath `--home`” is false. It is activated by the config’s declared source graph, not by an autonomous scan, and is consistent with Hyprland-style source resolution. A config could name `/proc/...` the same way; I found no direct `/proc` access or case-label probing in the tool itself.

## Provenance checks

- The reviewed A bytes are the landed `ef94763c6a75d1b0860091b19bb61c9bd7cda9e3` tool, SHA-256 `9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950`; the lane working-tree file has the same hash. This matches `evidence/c1-after-v4-ef94763c.txt:3`. The receipt records the v4 run at seed `ed0d8a943980d2f2`, `cases_pass=41/41`, `embed_hits=0` (`:4-6,49-51`).
- A's imports are only `glob`, `json`, `os`, `stat`, and `sys`. Source review and targeted searches found no base64/zlib/hex decoding, snapshot digest/hash code, network client, socket, subprocess, process launch, `/proc`/`mountinfo` access, `cwd`/argv-label inspection, or path-name-based case branching. Bind dispatcher text such as `exec` is parsed and emitted, not executed.
- The long constant at `:41-54` is the dispatcher-name grammar table, not a list of operator args/descriptions. A live `hyprctl binds -j` read during this review contained 192 entries; among its 248 distinct arg/description strings of length >=12, none occurred verbatim in A or B source. The v4 receipt independently records zero embed hits.
- Caveat on the lexical embed check: A spells the dispatcher as adjacent literals `"resize" "windowpixel"` (`:54`), which Python joins at runtime; B uses the same split. The current live capture had no arg/description containing `resizewindowpixel`, and the joined value is a dispatcher name rather than captured operator data. This is not evidence of an embedded bind table, but it demonstrates that a raw-source substring scan does not detect assembled constants.

## A vs B comparison

I imported the pinned `count-v3.py` generator (SHA-256 `8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375`) with `python3 -I -B`, built five fresh seeded trees using its `synth()` and `hard()` functions, and ran both implementations through its `run_tool()` sandbox wrapper. No oracle or nested compositor was used. Both implementations matched the generator's expected bind multiset on every tree, and their ordered JSON tables were identical on all five:

| Tree | Seed | A/B result | Binds |
|---|---|---|---:|
| SYNTH | `a13a281c7c4d6771` | identical; both match model | 15 |
| HARD | `314727e04c8f025a` | identical; both match model | 17 |
| SYNTH | `2adc415d396f3a65` | identical; both match model | 14 |
| HARD | `3adad1ddd6a945bc` | identical; both match model | 23 |
| HARD | `f7dced52e1fd558a` | identical; both match model | 25 |

B SHA-256: `778499d29ede8424ab79076641ac9a63a38132076ef43f8640e3f59a0160c304`.

## Residual risk and verification gaps

The five generated trees are a sample, not exhaustive. They do not include `# hyprlang if` directives: A's `truthy()` (`:129-136`) treats `"2"` as false, whereas B's condition handling (`ExecBindToolB/mado-binds.py:196`) treats any nonempty value other than `0/false/no/off` as true. Thus the observed 5/5 comparison does not establish agreement for conditional-comment semantics. The outside-home source test was intentionally config-directed; I did not test every symlink, glob, or environment-variable path variant.