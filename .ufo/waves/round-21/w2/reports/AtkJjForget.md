# AtkJjForget — C1 scoped review

## Verdict

The frozen `JjForget` expectation is semantically warranted. The repair is general for the canonical `jj bookmark <mutator>` shape, not keyed to the fixture text, but a nearby built-in-alias spelling still evades it. Retain the frozen expectation; the alias miss is a separate repair opportunity.

## Axes

- **Semantic classification / provenance:** pass for the frozen canonical command.
- **Rule generality:** pass for canonical bookmark mutation subcommands; the parser uses command position and a shared verb set rather than the case ID or exact string.
- **Command-form coverage:** fail for the tested default alias `b` form.

## Frozen expectation and repair

`oracle/expected.json:256-269` freezes the exact command `jj --ignore-working-copy bookmark forget probe` as one `vcs_write` with `evidence: observed`; the fixture contains that exact Bash tool-call command. The class and evidence are supported by the committed round-20 `ReviewVcsV3.md:14-20,53`: in a fresh test repository, the command exited successfully and the bookmark created immediately before it was absent from the subsequent bookmark listing. That is a repository-state mutation even though `--ignore-working-copy` prevents the working-copy snapshot/update. I did not execute the VCS command.

The current source bytes have SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d` (L1 identified the candidate commit as `f499a8db7171b7476fe9f204ab9edbac5a956fa9`). In `tools/mado-tripwire.py:187-192`, `forget` is in `JJ_BOOKMARK_WRITE`; `classify_jj` locates the command verb/subverb and returns `jj:bookmark` for that set at lines 623-638, before its generic `--ignore-working-copy` exemption at line 653. This correctly repairs the exact canonical shape and also covers the other listed bookmark-mutating verbs without fixture-specific branching. The candidate receipt records the exact expected finding for JjForget.

## Nearby counterexample

I wrote inert JSONL at `.ufo/waves/round-21/w2/fixtures/AtkJjForget/alias-b.jsonl` (SHA-256 `414913c4d8174c3a62f0014bb0e9cf73bf15671c042c658af6ccf175ef81dc88`) with the command text `jj --ignore-working-copy b forget probe`. Jujutsu's official [CLI reference](https://docs.jj-vcs.dev/latest/cli-reference/) identifies `bookmark` as having the default alias `b`; under that documented default, this is the same bookmark-forget mutation. The source itself also lists `b` among jj's default aliases (`mado-tripwire.py:198-206`).

Bounded scanner-only output, using the existing `measure.py` `scan()` API (the scanner child has the API's 384 MiB address-space cap and 15-second timeout):

```json
{"exit": 0, "payload": {"counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 0}, "exit": 0, "files": [{"bash_calls": 1, "eval_calls": 0, "eval_unparsed": 0, "lines": 1, "path": "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w2/fixtures/AtkJjForget/alias-b.jsonl", "sha256": "414913c4d8174c3a62f0014bb0e9cf73bf15671c042c658af6ccf175ef81dc88", "unparsed_spawns": 0}], "findings": [], "lead_findings": 0, "observed_findings": 0, "permitted": [], "schema": "mado-tripwire-verdict-v1", "unpermitted": 0}, "stderr": ""}
```

Source reason: the parsed verb is `b`, so it does not enter the `verb == "bookmark"` branch; with `--ignore-working-copy`, the fallback returns `None`. The local source notes that default aliases may be redefined without that configuration being visible (`mado-tripwire.py:98-106`), so this counterexample is specifically grounded in the documented default-alias configuration, not an assertion about arbitrary user alias files.

**Smallest safe correction:** recognize the documented default `b` spelling as `bookmark` in the jj verb classification, then reuse the existing `JJ_BOOKMARK_WRITE` check; keep the working-copy exemption behavior unchanged. Preserve the source's configuration caveat: without config evidence, do not claim that every user-defined `b` alias is a bookmark command.

## Limits

Only the inert scanner-only variant was run; no command in the fixture, VCS operation, suite, or corpus was executed. Expectations were not changed. No tools were installed.