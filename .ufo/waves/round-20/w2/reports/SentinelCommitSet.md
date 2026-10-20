# SentinelCommitSet — partly falsified: no credential/transcript hits, but path and email privacy candidates remain

Axes: credentials/tokens; IPv4; personal email; private home paths; copied transcript-line metadata.

## Findings

### S1 — Low, potential privacy disclosure — home-path review hits

Exploit path: a reader of a published commit can scrape local home-directory path strings and infer account or checkout layout. The supplied scanner classifies these as `REVIEW`, not confirmed findings; whether each value is a real private path rather than a synthetic/documentation value is [UNK]. Smallest remediation: replace unnecessary off-Projects home paths with neutral placeholders before publication, or have the owner confirm that the cited paths are intentionally public.

Evidence: `git diff --name-only 1f7f995 a4046a8` returned 563 paths. The clone was at `a4046a8216080d4004de3f268c62cf142095ac07`; staged bytes from that commit were 563 regular files (3,049,666 bytes), zero symlinks. The committed `SentinelFixtures.md` scan script (SHA-256 `ea22f0c96736c47da88f029f471d0fd92efcb9ca3fb9752f76afeca4d38b5476`) reported `patterns: fail=0 review=239`; of those, 234 were `home-path-outside-Projects` reviews. Locations (values omitted):

- `LOG.md`:39,79,131,239,696,1329; `SCORECARD.md`:13,15,17,488,1029,1116,1147; `SKILL.md`:49,53,55,65,73,75,76,80,81,82,83,84,85,86,87,88,89,91,112,113,114,115,116,118,119,188,212,223,269,292,309,367,373,390,403,886,887,888,889,902,935,1077,1396,1847,1848,1849,1850,1851,1852.
- `.ufo/waves/round-20/gen_w1.py`:14,27,48; `.ufo/waves/round-20/precision/expected.json`:2935; `.ufo/waves/round-20/w1/dispatch.json`:547,632,667,672,842,957; `.ufo/waves/round-20/w1/spec.json`:3,90,125,130,300,415; `.ufo/waves/round-20/w1/cases/CaseAdoptW2/cases.json`:781; `.ufo/waves/round-20/w1/corpus/pre-vs-harmed.json`:1.
- `.ufo/waves/round-20/w1/drafts/ScribeProvince.md`:10; `.ufo/waves/round-20/w1/drafts/ScribeShonen.md`:6; `.ufo/waves/round-20/w1/reports/CaseAdoptW2.md`:36,49,185; `CaseDryRunBash.md`:74,118,119; `CaseHelpBash.md`:183; `CaseShadowing.md`:196; `CaseWrapperForms.md`:138; `ConnSiblingIsolation.md`:9; `CorpusDiff.md`:13; `CriticNoHarmDiff.md`:7; `RevengeInnsHarness.md`:9,14,31; `ScoutCorpusLeads.md`:10,159.
- `.ufo/waves/round-20/w1/reports/ScoutCorpusVcsNonWrites.md`:25,29,79,80,144,286,306,316,317,318,328,329,330,334,335,336,337,338,339,340,341,342,343,344,345,346,347,348,349,350,351,352,360,363,365,367,368,369,370,371,372,373,379,380,381,382,383,384,385,386,387,388,389,390,391,393,394,407,408,417,419,420,421,422,423,424,425,426,427,428,435,436,437,438,440,441,443,445,446,447,448,449,450,459,473,474,481,488; `ScoutJjHelpEmpirical.md`:5; `ScoutR19Tallies.md`:26,59; `ScoutRuleBMap.md`:128; `ScribeQuality.md`:8.
- `.ufo/waves/round-20/w1/reports/SentinelFixtures.md`:3,31,41,42,51,60,167; `SentinelPause20.md`:15,31,35,41,146,149; `SrcBashErrexit.md`:39,44; `SrcJjHelp.md`:12; `TwVcsHelp.md`:116,148,222.
- `corpus/README.md`:12,13,14,15,17,18,42,43; `corpus/SOURCES.md`:26,32,71,83,84,92,96,97,103,107,109,110; `tools/mado-tripwire.py`:1951,1955.

### S2 — Low, unresolved privacy review — email-shaped values

Exploit path: public readers can use an email-shaped identifier to correlate an author/source with other accounts. The check reported these as non-synthetic-by-its-allowlist `REVIEW` entries, not hard findings; whether any is personal or identifying is [UNK]. Smallest remediation: replace any unnecessary personal address with a role/source reference after owner review.

Evidence: five `email` review locations, no values reproduced: `.ufo/waves/round-20/fetch/SrcJjHelp/receipts.jsonl:7`; `.ufo/waves/round-20/w1/reports/SrcJjHelp.md:93,136,150`; `corpus/SOURCES.md:116`.

### No detected credential, IP, or copied transcript-line findings

Evidence: the pinned-config Gitleaks scan of all 563 staged files used gitleaks 8.30.1 (`/usr/bin/gitleaks` SHA-256 `ef931a755d99f66e78923685cde6b475e16f2eda0e044ede2f396421d1984ef3`) and explicit `[extend] useDefault = true` config (SHA-256 `27630a96d6c55755cc37620f3933d5cab94b1eb78a726a32e11212972525d76e`). Command used `--ignore-gitleaks-allow --redact --exit-code 3 --report-format json`; output: `report_entries=0`, `gitleaks_rc=0`. The `SentinelFixtures.md` script also completed with `patterns: fail=0 review=239` and `prelanding-scan: targets=1 fail=0`; its generated-canary Gitleaks self-test therefore passed. No token/key-shape, IPv4, or copied transcript marker finding was emitted.

## Limits

- Gitleaks and the supplied fallback patterns are heuristic; a clean scan does not prove absence of every credential or identify whether the five email-shaped candidates are personal. Their ownership/context is [UNK].
- The copied-transcript marker check is the supplied script's JSONL fixture check; this report does not claim full semantic identification of transcript text in arbitrary prose or binaries.
- The scan covers the final committed bytes named by `git diff --name-only 1f7f995 a4046a8`, not paths added and later removed within the range, other refs, or later working-tree changes.
- No matched secret, path value, or email value is reproduced here.

## Installs

none; gitleaks 8.30.1 was already installed. No package or tool was installed or updated.