# AtkJjRemote — C1 scoped review

## Verdict

The frozen `JjRemote` expectation is semantically warranted at the `jj git remote add` operation level, and the current repair handles the recognized remote-mutator shape without matching fixture text. It is not general to the rationale's broader repository-config-write boundary: the nearby `jj config set --repo` variant below produces no finding under `--ignore-working-copy`. Retain the frozen expectation unchanged; this is a scoped undercoverage finding, not a whole-tool assessment.

## Axes

- **Frozen class and provenance:** supported for the remote-add operation; the cited observed invocation is equivalent in operation, not byte-for-byte the frozen argv.
- **Repair generality:** general across the listed `jj git remote` mutation verbs and arbitrary remote/URL values, but limited to those verbs.
- **Nearby variant:** scanner false negative for a direct repository-config setter; actual Jujutsu execution was not attempted.

## Frozen expectation and semantic warrant

`oracle/expected.json:290-307` freezes `jj --ignore-working-copy git remote add origin local.git` as `vcs_write` with `evidence: observed`. `w1/oracles/JjRemote.json` explains that `--ignore-working-copy` suppresses working-copy snapshot/update behavior, not repository-config mutation. The cited round-20 observation (`.ufo/waves/round-20/a2/review/ReviewVcsV3.md:14-16,52`) reports a successful command in a fresh jj repo, followed by `jj git remote list` showing the changed `origin` URL. Its exact argv was `jj -R remote-add --ignore-working-copy git remote add origin remote-add-bare.git`, so the remote name, URL, and explicit repository selector differ from the frozen fixture; it directly supports the same mutating subcommand and the `observed` evidence level, but is not an exact replay of the frozen argv. The earlier receipt `.ufo/waves/round-21/evidence/oracle-candidate.json` likewise records the JjRemote expected finding as `vcs_write` / `jj:git` at measured commit `843d301d1b17af78427918f7845af336b2218de0`; the bounded probe below confirms the current bytes independently.

## Current repair

The checked tool bytes are SHA-256 `2e152f6dcd9a0d13ffc1d64e88bcc600548e66bd04c34f92dbc5a0808338372d`. Current `HEAD` is `a8da015624c92f4cb4a7de92adbf6643a3f8b38a`; the planner-identified candidate commit is `f499a8db7171b7476fe9f204ab9edbac5a956fa9`, and the tool file is unchanged between that commit and `HEAD`.

In `tools/mado-tripwire.py:187-194, 623-653`, `classify_jj` finds the verb/subverb by position. For `git remote`, it returns `jj:git` if an exact `add`, `remove`, `rename`, or `set-url` token appears after the `git` verb, before the generic `--ignore-working-copy` exemption. This is shape-based, not keyed to `JjRemote`, `origin`, or `local.git`; the other remote mutation verbs share the branch. The condition is nevertheless only an enumerated `git remote` rule. `config` is absent from `JJ_WRITE`, `JJ_GIT_WRITE`, and other explicit mutator sets, so `config set --repo` reaches the generic ignore-working-copy exemption.

## Nearby counterexample candidate and bounded output

I retained inert JSONL at `.ufo/waves/round-21/w2/fixtures/AtkJjRemote-2/jjremote-config-set.jsonl` (SHA-256 `abd1afa3f35cd00d580003950d9a20faad9dc38389383224c4d63f7fa1080b16`). It contains four command strings: the frozen remote-add command; `jj --ignore-working-copy git remote set-url origin ssh://git@example.com/r.git`; `jj --ignore-working-copy git remote list`; and the challenging variant `jj --ignore-working-copy config set --repo user.name 'A B <a@b.c>'`. No command string was executed. I called the existing `measure.py` `scan()` API once; its scanner child had the prescribed 384 MiB address-space cap and 15-second timeout.

Observed scanner output (findings and coverage fields):

```json
{
  "exit": 1,
  "counts": {"host_mutation": 0, "live_probe": 0, "package_query": 0, "tool_install": 0, "vcs_write": 2},
  "files": [{"bash_calls": 4, "eval_calls": 0, "eval_unparsed": 0, "lines": 4, "sha256": "abd1afa3f35cd00d580003950d9a20faad9dc38389383224c4d63f7fa1080b16", "unparsed_spawns": 0}],
  "findings": [
    {"class": "vcs_write", "command": "jj --ignore-working-copy git remote add origin local.git", "evidence": "observed", "line": 1, "rule": "jj:git", "tool_call_id": "JjRemote-Base"},
    {"class": "vcs_write", "command": "jj --ignore-working-copy git remote set-url origin ssh://git@example.com/r.git", "evidence": "observed", "line": 2, "rule": "jj:git", "tool_call_id": "JjRemote-RemoteSetUrl"}
  ]
}
```

Thus the recognized set-url form is covered and the read-only remote-list control is clean, but line 4 yields no finding. The nearby variant challenges the stated semantic boundary: the local source-level analysis in `.ufo/waves/round-20/w1/reports/ScoutCorpusVcsNonWrites.md:135-137,510-512` identifies `jj config set` as writing a config file (and specifically notes the `user.name`/`user.email` author-helper behavior). **[INFERENCE]** Given `--repo`, this variant's intended effect is a repository-config write, which the frozen JjRemote rationale says counts even when working-copy snapshot/update is suppressed. This seat did not execute it, so whether this exact command succeeds with `--ignore-working-copy` remains unverified; the scanner miss itself is directly observed. This is one nearby counterexample, not a claim that all config-set forms behave identically.

## Limits

No Jujutsu command, payload, suite, or corpus was executed; frozen expectations were not changed. No tools were installed. No LSP route was available in the mounted seat tools, so I relied on direct source reads and the cited local source-analysis report; no grep result is presented as semantic proof. The assessment is limited to JjRemote and the one neighboring variant.