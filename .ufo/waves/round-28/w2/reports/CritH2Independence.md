# CritH2Independence — ranked read-only findings

## Scope / axes / availability
- Axes protected: C1 operability (mutation validity and independence); calibration/provenance of the claimed evidence. No coverage or score improvement is claimed.
- Root: `/home/vgpnk/Projects/shokunin/mado-shokunin`; references below are relative to that root.
- Neither H2 nor refpub nor their seals existed at inspection. Directory reads found only `c2/count.py` and `c1/{count.py,__pycache__,synthetic-home}`. This is a construction/scorer critique, not an inspection of returned rows.
- Frozen registration read first; frozen counters and all implementation files left unchanged. No H1 directory, H1 seal contents, or another seat's returned rows were read.
- Evidence aliases: F = `.ufo/waves/round-27/c2/count-v2.py`; L = `.ufo/waves/round-28/c1/count.py`; R = `.ufo/waves/round-28/registration.md`.
- Subject aliases: C1 = `.ufo/waves/round-26/c1/count-v2.py`; C2 = `.ufo/waves/round-26/c2/count.py`; Q = `.ufo/waves/round-26/quality/check-population.py`.

## Complete validity / passing-rule inventory
1. F:116-121 accepts rows only from a JSON list; each row must be a dict, `file` in the three SUBJECTS, `old`/`new` strings, and `old != new`. An id is not required or required unique. A non-list JSON value silently yields no rows.
2. F:122-127: `old` must occur exactly once in the pristine subject read from REV; replace that occurrence once.
3. F:128-132 implements the advertised “compiles” rule with **only `ast.parse(nb)`**, catching SyntaxError. Actual compilation is not performed.
4. F:133-135 requires `ast.dump(edited_tree) != ast.dump(pristine_tree)`; this proves neither a behavioral change nor a distinct mutant class.
5. F:136-141,190-193: edited-byte SHA256 must differ from every pristine subject, all accepted W rows, and every previously accepted H/B row in this invocation. W must have exactly 15 valid rows and no invalids. There is no W/H AST-uniqueness check or cross-invocation H2/refpub uniqueness check.
6. F:195-211: `--heldout` requires a seal; only top-level `*.json` are included. Their sorted basenames must equal seal dictionary keys; every file is read once and its raw SHA256 must match. Only two-token seal lines are consumed; duplicate names overwrite earlier entries. This is byte integrity, not independent authorship, completeness against an external inventory, or chronology.
7. F:212-220: filenames ending `-benign.json` classify all accepted rows as B; other JSON filenames classify them as H. B uses exactly the same structural/AST/byte checks as H. No independent behavior-preservation proof is checked.
8. F:226-233,245-261: pristine A/B plus two generated benign edits per subject plus every accepted B must exit 0. B must contain >=3 valid rows, >=1 per subject. All 15 W must be killed. H requires >=6 valid rows, >=2 per subject, and >=ceil(0.75*h_valid) kills. Any non-None, nonzero suite status counts as a kill, including setup/compiler failures and timeouts.
9. L:157-175 additionally compares each local seal with its committed blob at REV; H2 requires the frozen counter's success; refpub requires success, >=9 valid H rows, all killed, and minimum >=2 per subject. The JSON bodies themselves are not checked for presence at REV.
10. Invalid H/B rows are printed and omitted, not fatal (F:218-222,260-264). Therefore an author can include bad shape, wrong old occurrence count, parse failure, pristine-equivalent AST, duplicate bytes, or invalid JSON and still pass if enough accepted rows remain. A seal mismatch itself cannot pass these legs.

## Ranked findings and exposing fixtures
### 1. High — un-compilable programs count as valid killed mutants (implementation defect)
- Evidence: F:129 is `tree = ast.parse(nb)`; F:131 labels only parse errors `INVALID does not compile`; F:251 is `ok = rc is not None and rc != 0`.
- Python's official documentation explicitly says `return 42` generates a valid AST but cannot compile outside a function; `ast.parse()` does no scoping checks: https://docs.python.org/3/library/ast.html#ast.parse (opened this review).
- Concrete H rows: C1 old `NCASES = 40`, new `NCASES = 40\nreturn 281`; C2 old `NARITH = 30`, new `NARITH = 30\nreturn 281`; Q old `import sys`, new `import sys\nreturn 281`. Give each a unique id and repeat with `282` for H2, or `283`, `284`, `285` for refpub (two/three rows per subject).
- These anchors are top-level and present in the public subjects (C1:49; C2:32; Q:40). Their ASTs differ and bytes are distinct from W/pristine/each other. No file is executable Python.
- Suite A catches subject import exceptions and returns 1 (`quality/counter-selftest.py:395-398,495-503`); suite B fails checker syntax errors (`quality/population-suite.py:349-411`). Both outcomes are credited as kills by F.
- [INFERENCE, not run] With otherwise passing W/green prerequisites and three genuine B edits (one per subject), these sets satisfy H2/refpub entirely through compiler rejection, without exercising mutant judgments.
- Smallest safe correction: mandatory independent `compile(edited_bytes, subject, "exec")` preflight, without executing subjects; reject these rows. Do not edit the frozen scorer; any successor behavior must remain separately identified.

### 2. High — byte novelty can recycle W and duplicate the two sets (independence gap)
- Evidence: only pristine AST is compared (F:133); `seen` is freshly initialized per run (F:190); L invokes the scorer separately for H2 and refpub (L:160,169).
- Concrete rows, each with a different trailing `# r28-<set>-<id>`: C1 old `met = npass == len(built)` -> `met = npass * 10 >= 9 * len(built) # r28-h2-c1-a`; C2 old `EMBED_MIN = 12` -> `EMBED_MIN = 1000 # r28-h2-c2-a`; Q old `registered = populations[pred]` -> `registered = den # r28-h2-q-a`.
- These are the already-public W faults `c1-pass-90pct`, `c2-embed-min-1000`, `q37-M1-ignore-registered` (W JSON:17-21,52-56,66-70), merely comment-salted. Two variants per subject give H2 six rows; three give refpub nine. Each edited AST equals its corresponding W AST, not pristine.
- [INFERENCE, not run] Behavioral suites that kill those W faults also kill these equivalent faults; this adds no new failure class. Identical H2/refpub files also pass separate invocations' uniqueness checks. Neither observation alleges any actual author's misconduct.
- Smallest safe correction: independent public-source fault-class/normalized-AST audit across W, H2, and refpub before evidential use. Byte hashes alone cannot substantiate independent rotation. Public refpub is a regression set, not an independent holdout.

### 3. High — a “benign” row can be a surviving mutant (label/oracle circularity)
- Concrete Q row in `q-benign.json`: old `registered = populations[pred]`; new `registered = populations[pred] + (pred == "PRED-R28-UNTESTED")`.
- Evidence: suite B's complete FIXTURES list (`quality/population-suite.py:102-225`) contains no such predicate. F:217,230-231 trusts the filename and suite acceptance; it never proves the edit preserves behavior.
- Exposing registration: `**PRED-R28-UNTESTED** target cases_pass=1/1\n`; receipt: `CASE X PASS\nPRED-R28-UNTESTED cases_pass=1/1\n`.
- [INFERENCE, not run] Pristine accepts; the edited checker rejects because registered becomes 2. Existing suite fixtures are unaffected, so the row can count as valid green B despite being a real defect. Complete the B minimum with harmless assignments on C1/C2, e.g. append a fresh unused constant after `NCASES = 40` / `NARITH = 30`.
- Smallest safe correction: independently review B transformations and retain an explicit preservation rationale/witness domain. A finite suite cannot certify universal equivalence; do not promote B acceptance into such a claim.

### 4. Medium — seal provenance and committed-body assertions exceed what is checked
- Evidence: F:199-211 hashes only the submitted JSON inventory; L:158-174 compares only the seal blob against REV. R:99-106 separately promises public-source construction, restricted information, before-run sealing, and committed sets.
- Exposing fixture: commit a correct seal, leave the matching JSON files only in the working tree, and run L at that REV. Or seal a selectively retained easy subset while omitting difficult rows entirely. The byte checks have no independent expected inventory, author boundary, timestamp, or subject/suite-binding obligation to detect these cases.
- [INFERENCE, not run] These can pass the legs although the first is not reconstructible from committed set bytes and neither proves independent preregistered construction. The scorer's printed REV/subject/suite hashes identify the run, but are not construction evidence.
- Smallest safe correction: verify every sealed JSON body exists at REV with matching bytes; retain an independently recorded expected inventory and a pre-deciding-run seal commit tied to subject/suite identities. Process provenance remains a separate audit obligation, not a property supplied by SHA256.

### 5. Medium — bad submissions may disappear without failing the leg (fail-open validity accounting)
- Concrete fixture: add a sealed row C1 old `NCASES = 40`, new `NCASES = 40 # comment-only`; it fails pristine-AST inequality, but an otherwise passing set remains passing. Duplicate an accepted row, use an absent old string, or add malformed JSON for equivalent omission. A JSON file containing `{}` silently contributes zero rows and zero invalids (F:116).
- Evidence: `invalid=len(hbad)` is printed (F:263-264), but `hbad` is absent from `met` (F:260-261). W, in contrast, rejects invalids (F:192-193).
- Smallest safe correction: construction audit must reconcile every submitted row and require no invalids; do not describe the whole submitted inventory as valid based on the leg's success.

### 6. Bounded tradeoff, not an all-row counting bug — per-subject kill coverage is not required
- Exact code (F:256-261):
```python
hv = len(H)
need = math.ceil(0.75 * hv)
h_subj = min(sum(1 for _, f, _ in H if f == x) for x in SUBJECTS)
b_subj = min(sum(1 for _, f, _ in B if f == x) for x in SUBJECTS)
met = (tally["GREEN"] == ng and len(B) >= MIN_B and b_subj >= 1 and tally["W"] == len(W)
       and hv >= MIN_H and h_subj >= MIN_H_SUBJ and tally["H"] >= need)
```
- Answer: `h_min_per_subject` counts **accepted valid H rows**, not all submitted rows and not only killed rows: H is populated from `load_rows`'s `got` (F:218-219). Invalid padding cannot satisfy the minimum.
- Exposing H2 fixture: three killed comment-salted C1 W rows + three killed C2 W rows + two surviving Q rows made by `import sys` -> `import sys\n_r28_neutral_q1 = 1` / `_r28_neutral_q2 = 2`. [INFERENCE, not run] Eight valid rows, six kills, minimum two: the frozen aggregate threshold permits zero Q kills. The neutral H rows also illustrate that AST difference does not prove mutant semantics.
- Refpub's all-killed rule prevents this particular survivor dilution. The H2 aggregate allowance is explicit in R:37-40, not a defect to silently “fix” in frozen code. Smallest safe correction: report per-subject killed/valid alongside the frozen result and do not infer balanced efficacy or saturation from it; reject that stronger inference, not rewrite the registered threshold.

## Commands / failures / written files
- Only process command: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse master` — exit 0; output verbatim: `4f610066efd90804b055c42ae20c41a7f44404f9`.
- Availability tool: `glob` on absolute `.../round-28/c2/heldout2*;.../round-28/c1/refpub*` — successful tool response, verbatim: `No files found matching pattern`. File reads, targeted searches, and official documentation retrieval are not shell commands and supply the evidence cited above.
- No scorer, suite, compiler, compositor, build, test, judge, alternate runtime, or install was run. No measured passing/killing values are claimed; fixture outcomes above are explicitly static inferences. No checks failed; the absence of set artifacts prevented row-level review and was handled by the requested construction-rule attack.
- Sole written file: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-28/w2/reports/CritH2Independence.md`. No scratch files, code edits, or runtime state changes.
