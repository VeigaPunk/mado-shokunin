# R56W3RevLiveBoundary — host-boundary sweep, attempt 2

Attacked item: host non-mutation, permitted host-read scope, credential non-disclosure, and sibling-domain boundaries in **every committed w1/w2 report and its associated artifacts/receipts**, at `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`. This is an author-seat recommendation, not admission or a non-author closure.

Axes: host non-mutation; credential non-disclosure; exhaustive pinned-evidence coverage; reproducibility. Frozen v2 claims and registration were read first, followed by v1 registration and pinned PROVINCE. No predicate, counter, target or kill rule changed.

## Findings, by severity

### D1 — weakens the claim: recorded host/sibling-read boundary discipline (not a frozen predicate failure)

The unsandboxed historical `R56W2CritC2Cheat` crawl did not stay within caller-provided fixtures or the own-compositor fd/fdinfo read surface. Its implementation reads **arbitrary process cmdlines** and traverses other seats' and sibling domains' scratch directories:

- `.ufo/waves/round-56/w2/R56W2CritC2Cheat/cheats/e-crawl.py:25-27`: `for p in sorted(glob.glob("/proc/[0-9]*/cmdline")):` followed by `parts = open(p, "rb").read().split(b"\0")`.
- Same file `:36-50`: roots derived from those process arguments plus `/fast/scratch` and `/tmp`; `os.walk(r)` followed by reads of matching `args.json`, `expected.out` and `expected.rc`.
- Actual receipt `.ufo/waves/round-56/w2/R56W2CritC2Cheat/receipts/crumbs-e-crawl-nobwrap.txt:2-4`:
  ```
  proc works: 50
  root done: /fast/scratch/hyaku/kaidoku-r50/l1/score visited=18158
  hit crawl: /fast/scratch/hyaku/mado-r56/R56W2MutC2ToolA/work/h/c2-export-1qiysmny/.ufo/waves/round-56/fixtures/c2/F01
  ```
- Report `R56W2CritC2Cheat.md:26,41` explicitly attributes the successful replay to the sibling seat's export. The receipt also records `chousa-r63` and `souji-r42` traversal at lines 9-11.

This demonstrates broader read activity, not a host mutation or sibling-domain knowledge absorption. It weakens an unqualified all-seats-within-read-boundary statement. It does **not** change or falsify the frozen C2 output predicate. Route any boundary-policy adjudication separately; no remediation was applied.

### Blocking host-mutation findings: none demonstrated

No recorded **executed** `hyprctl keyword`, `dispatch`, `reload`, host kill/signal, service mutation, or write under host `.config`/`.local` was found. Recorded round-56 live invocations use `getoption` and `version`, both read verbs. Other vocabulary is not silently ignored: all matching lines are quoted with location and candidate severity in the receipt.

Dangerous literal strings are present as data, not executed commands. Examples:
- `w1/R56ScoutOmarchy.md:83,85,92,117,136` quotes upstream scripts' reload/keyword, `pkill`, config writes and service restart. Its sections 2-3 explicitly identify source greps and a source-behavior table; these are not seat execution receipts.
- `w1/R56RevCoverage/assigned-grep-base.txt:2-4,8` contains historical source excerpts naming reload and the operator-only boundary.
- `w2/R56W2RevAuditC/receipts/02-false-propositions.txt:9` contains an intentionally false proposition about SIGHUP, not a signal invocation.

No blocking finding is inferred merely from those quotations. Treating artifact content as commands would incorrectly convert source inspection into compositor mutation.

## Credential sweep

The three exact patterns were extracted without execution from pinned `tools/mado-tripwire.py:301-305`:
1. URL user/password before `@`: **0 matching lines**.
2. AWS access-key shape `AKIA` plus 16 uppercase/digits: **0**.
3. `[A-Za-z0-9_\-]{32,}`: **12,213 matching lines**, 1,483 distinct strings in regular evidence blobs. Reviewed non-hex strings are document/function identifiers, separators, fixture names and Hyprland instance signatures; the rest are hex digests/revisions. This deliberately broad pattern is not itself credential evidence.

Additional contextual/prefix scan (private-key headers, GitHub/OpenAI/Anthropic/Google token shapes, bearer authorization, password/API-key/access-token/client-secret assignments): **0 matching lines**. No credential material was identified in the 76 seat reports or their associated evidence. All fixed-pattern values are suppressed in the produced receipt; no credential-shaped value is reproduced there. Shape scans cannot prove absence of unrecognized credentials.

## Exact commands and decisive output

Read-only pinned export (one archive, consumed in memory; regular files initially materialized in own scratch for specialized-tool triage; symlink contents scanned as link text without following them):

```sh
git -C /home/vgpnk/Projects/shokunin/mado-shokunin archive 0f3a54361a9824484d0801679ceb1fd8ac7c32e1 .ufo/waves/round-56/w1 .ufo/waves/round-56/w2 tools/mado-tripwire.py
```

The archive bytes were saved to the explicitly named own-scratch `evidence.tar`. Main sweep, `TMPDIR=/fast/scratch/hyaku/mado-r56/R56W3RevLiveBoundary`, cwd that same scratch directory:

```sh
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevLiveBoundary/boundary-sweep.py /fast/scratch/hyaku/mado-r56/R56W3RevLiveBoundary/evidence.tar /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevLiveBoundary/receipts/boundary-a2.txt
```

Exit **0**:
```
BOUNDARY_SWEEP reports=76 files=1714 symlinks=9 totals={'fixed3': 12213, 'hyprctl': 4155, 'config': 5533, 'state': 1506, 'write_candidate': 27, 'proc': 115}
D1: broad /proc cmdline and sibling scratch reads recorded; no executed host mutation demonstrated.
Credential-specific matches=0
```

The 76 reports are **43 w1 + 33 w2**, consistent with the disclosed two missing attempt-1 reports. Counts are matching lines with overlapping categories, not counts of executed commands. The exhaustive scan includes nested historical corpus copies rather than omitting them.

Initial specialized `grep` calls used patterns `SECRET|REDACT|sk-|Bearer|ghp_|AKIA|token` on exported `tools/mado-tripwire.py`, and `hyprctl|/proc/|kill\b|pkill\b|killall\b|systemctl|\.config/|\.local/|signal\b` on exported top-level w1/w2 reports. Shell grep/awk pipelines were **not run**: specialized grep output is capped, so the reproducible Python sweep above provided complete per-file accounting and every matching line. All patterns and per-file SHA256/byte counts are in the receipt.

## Residual risks and verification gaps

- Artifacts record assertions and selected receipts, not complete historical tool-call transcripts. Null results mean **no recorded violation detected**, not proof that an omitted command never ran.
- `w2/R56W2RevProcFdinfo.md:103-105` reports the compositor's `HOME` from its environment, beyond the named fd/fdinfo read surface. The exact environment-read command is not retained, so authorization and extent of exposure could not be verified. Only HOME is printed; no credential is demonstrated.
- `w2/R56W2Sentinel/probes/probe_bwrap.py:9-23` contains attempted sensitive-path reads inside an explicit bwrap sandbox; source presence alone does not demonstrate successful host reads. No sensitive content is retained in the scanned artifacts.
- Historical copied documentation mentions read verbs outside this seat's allowlist (`clients`, `animations`, etc.). These were not treated as round-56 live invocations. No independent host probe was run by this seat.
- LSP prerequisite: `read xd://lsp` returned **No such tool**. Semantic references/definition/diagnostics were unavailable; this is a byte/text audit, not semantic absence proof.
- No claim counters, harnesses, selftests, live host commands or compositor probes were run; outside this seat's assignment. No software installed or updated. No git/jj mutation, delegation or background job.

## Deliverables

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevLiveBoundary/receipts/boundary-a2.txt` — exact sweep command, all regexes, every file's verdict/hash, every matching line with severity and safe redaction.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevLiveBoundary/boundary-sweep.py` — reproducible read-only archive scanner.
- This report. Own scratch was removed before yield after retaining the receipt.

Self-evaluation (1-5): accuracy 4 (historical execution evidence is incomplete); completeness 4 (all pinned artifacts scanned, unavailable historical transcripts remain); clarity 4 (full raw hit receipt is necessarily large); actionability 4 (D1 has exact input/implementation/receipt pointers, historical read authorization remains unverified); conciseness 4 (separate exhaustive receipt keeps findings bounded). Overall 4.0. Improvements: retain full historical command transcripts and seat-specific read grants for stronger boundary adjudication. Would the user agree? The result is explicitly evidence-bounded, not a blanket safety certification.
