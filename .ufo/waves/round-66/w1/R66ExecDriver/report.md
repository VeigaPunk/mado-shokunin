# R66ExecDriver — calibration / operability

## Changed draft
- `.ufo/waves/round-66/w1/R66ExecDriver/quality/counters/c2-r66-landing-instrument.py` → integrate as `quality/counters/c2-r66-landing-instrument.py`.
- No production changes, commits, host configuration changes, or tool installations.

The new driver pins `--rev` to a commit SHA, reads only committed regular blobs for the instrument and its three frozen dependencies, strips all inherited `GIT_*` variables from git and leg children, runs selftest and landing, and passes `--round 66 --citecheck-paths <real --repo>/.ufo/waves/round-66/receipts`. Both producer rcs must be zero; the landing output must carry exactly one matching GREEN summary and one zero-rc witness per leg. The standing instrument owns child-marker validation. Missing artifacts produce TARGET_MISSED/1; unsafe setup exits 2. Scratch rejects tmp-family roots and symlink ancestors, uses exclusive private directories, and removes private work in finally. Stdout/stderr and command/rc sidecars survive under declared scratch for caller retention.

Peer landing draft inspected after availability notification: `.ufo/waves/round-66/w1/R66ExecLanding/landing-counters.sh`. Its summary/leg witnesses are compatible; canonicalizing the revision prevents false negatives for short SHA or HEAD. No post-score predicate expansion.

## Commands, rc, exact retained evidence
Run from the seat's Python eval harness, using absolute paths and no lane git writes:

1. `python3 .ufo/waves/round-66/w1/R66ExecDriver/quality/counters/c2-r66-landing-instrument.py --repo <lane> --rev eafd500fa7be76dca59e729435e231a5032cc037 --scratch-root /fast/scratch/hyaku/mado-r66/R66ExecDriver`
   - rc **1**; `selftest=0 landing=2 green=no verdict=TARGET_MISSED`.
   - Frozen baseline selftest **19/19**, rc **0**. Actual baseline landing rc **2**, stderr `landing-counters.sh: unknown argument: --round`.
   - Exact leg bytes and argv/rc: `evidence/c2r66-crfq47my.{selftest,landing}{,.err,.command}.log` in this seat directory.
2. In-memory focused contract harness: rc **0**, **14 checks passed**. Covers complete/partial/duplicate/conflicting/wrong-revision GREEN witnesses, missing/nonzero leg witnesses, `/tmp`, `/var/tmp`, `/dev/shm`, symlink-ancestor escape, missing artifact TARGET_MISSED/1, and inherited invalid `GIT_DIR`/`GIT_WORK_TREE` isolation. Exact case list, commands, results: `evidence/targeted-checks.txt`.
3. Final revised driver with `--rev eafd500f`, otherwise command 1, and invalid inherited `GIT_DIR`/`GIT_WORK_TREE`: rc **1**, `selftest=0 landing=2 green=no verdict=TARGET_MISSED`. Asserted child argv contains full frozen SHA, explicit round 66 and repo-derived receipts path. Exact command/result: `evidence/short-revision.txt`; corresponding final leg logs retained alongside baseline logs.

All evidence paths above are relative to `.ufo/waves/round-66/w1/R66ExecDriver/`; all are committed-path-ready. Scratch `/fast/scratch/hyaku/mado-r66/R66ExecDriver` was removed after retaining evidence; observed absent. Selftest-created fixture repos were confined there. No fixture was created directly by this seat outside the standing instrument selftest. No whole-repo build, lint or formatter run.

## Limitations / parent gate
- The real **candidate** four-leg GREEN cannot be claimed: the peer draft is not a committed candidate revision, and this seat may not integrate or commit. Parent must run this driver against its integrated revision with committed round-66 receipts; this report records baseline TARGET_MISSED, not candidate success.
- LSP unavailable: no LSP device is exposed in this seat; source inspection used read/grep.
- Runtime tmp/symlink checks provide bounded filesystem guarantees, not protection against a concurrently hostile actor replacing ancestors after checks. Child authenticity is the standing instrument's bounded structural contract, not cryptographic proof.
- Extracting/running the explicitly assigned frozen used-by dependency was required; its historical source material was not read for research.

## Self-assessment
Accuracy 4/5: exact baseline evidence retained; candidate GREEN remains unobserved. Completeness 4/5: driver and bounded checks complete; integrated candidate gate belongs to L1. Clarity 4/5: integration path and blocked gate explicit. Actionability 4/5: single production draft, peer argv/summary compatible. Conciseness 4/5: logs retained separately. Overall 4.0/5. Highest-impact next action is the committed candidate run, not a new predicate.
