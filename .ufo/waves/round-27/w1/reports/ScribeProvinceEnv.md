# ScribeProvinceEnv — round-27 w1 report

## Behavior and findings

Prepared a prose-only draft for the routed M26-10 corrections. The proposed append-only paragraph supersedes only the stale environment-seeding claim in the Round-25 residual correction: since `a496b02a`, process-environment-only `$NAME` references remain literal and `source = $VAR` is not followed through an environment value. It preserves the distinct finding that absolute `source =` paths are still followed. The draft also contains the requested `tools/mado-wsrules.py` inventory row and the exact proposed bind-tool docstring paragraph.

Search command run at the requested revision:

`git grep -n -i 'environ\|environment' 5ddc5885 -- PROVINCE.md corpus tools/mado-binds.py`

The bind-tool-related hits are listed in the draft: `PROVINCE.md:29,36-39`; `corpus/lessons/round-25-verifier-spotcheck.md:90-93`; `corpus/lessons/round-25.md:76-79`; `corpus/lessons/round-26-verifier-spotcheck.md:107-119,207-213`; and `corpus/lessons/round-26.md:91-98`. `PROVINCE.md:30` is a false positive about `tools/mado-anims.py`; the README and knowledge hits (`corpus/README.md:218`, `corpus/knowledge/animation-table-r26.md:96-98`) also describe that separate animation-table tool, not bind-tool seeding. The draft records these as out of scope. The current bind-tool docstring has no environment-limit paragraph (`tools/mado-binds.py:2-10`); source inspection of `State` and `main` (`:567-582`, `:884-905`) shows an initially empty config-variable table and no process-environment initialization. These are source-inspection findings, not a runtime test.

## Gates and safety

No build, tests, counters, or Hyprland instances were run; this assignment was prose drafting only. No tooling was installed. No lane product file was edited. The requested coredump count command was run before and after; both outputs were `1338`, delta `0`:

`timeout 30 prlimit --as=4000000000 -- coredumpctl list --no-pager --no-legend | grep -c /usr/bin/Hyprland`

The `git grep` output contained the matching lines; its exit status was not displayed by the tool interface. The draft-directory creation command `timeout 10 prlimit --as=4000000000 -- mkdir -p .ufo/waves/round-27/drafts` produced no output.

## Touched surfaces and out of scope

Created only the requested prose draft and this report. `PROVINCE.md`, `tools/mado-binds.py`, README, knowledge pages, counters, harness, and mutant sets were not changed. No claim is made that either proposed documentation change has been applied or tested.

## Artifacts

- `.ufo/waves/round-27/drafts/province-r27.md` — proposed correction paragraph, proposed workspace-rule row, sweep inventory, and exact docstring paragraph.
- `.ufo/waves/round-27/w1/reports/ScribeProvinceEnv.md` — this report.
