# R56W3RevLessonGate — draft Gate audit

**Recommendation: S396 ADMIT-WITH-EDITS; S397 ADMIT-WITH-EDITS.** These are recommendations on an unintegrated draft, not admissions or a claim verdict. No tracked lane file was changed.

Axes: pin identity, located short quotations, scoped entailment, truthful registry status, frozen C3 compatibility, census validity.

## Findings, by severity

### Weakens the claim: both rows hide lesson reliance; the stated C3 reason is false

Input: `.ufo/waves/round-56/attempt2/s396-s397-draft.md:5-9,13,21` proposes `queued` and `used-by —` because the lesson cites the sources but purportedly a lesson path would trip `extra`.

`/home/vgpnk/Projects/shokunin/CORPUS.md:103-108` explicitly allows **lessons** in `used-by` and defines `mined` as cited by at least one listed path. Therefore, when integrated with the citing lesson, both rows should be `mined` with that actual repo-relative lesson path. `queued / —` is defensible only while neither an entry nor a lesson cites them, not for the integration described by this draft.

At frozen revision `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`, `quality/counters/c3-r56-used-by.py:51,181-200` recognizes only `corpus/knowledge/[A-Za-z0-9_.-]+\.md` in cell 11. Its `extra` expression at line 280 never receives lesson paths. The registration agrees (`registration.md:166-173`). A probe of the actual frozen parser produced:

```
frozen parse_registry draft: {b'S396': set(), b'S397': set()}
frozen parse_registry lesson-listed: {b'S396': set(), b'S397': set()}
frozen parse_registry knowledge-ghost: {b'S396': {b'corpus/knowledge/no-such-entry.md'}, b'S397': {b'corpus/knowledge/no-such-entry.md'}}
```

**Required edits:** replace the introductory C3 rationale; integrate both rows as `mined` and list the real citing lesson. Do not widen the frozen counter or predicate. C3 ignoring lesson paths is a disclosed measurement boundary, not an integration obstacle.

### Weakens the claim: S396 omits the per-instance qualifier

Draft line 13 teaches an unqualified unique descriptor/one-watch-per-inode rule. Pin lines 89 and 91 expressly scope it to **this inotify instance**; separate instances can monitor the same inode independently.

**Required edits:** add “within the same inotify instance” to the taught reuse/uniqueness claim and scope; change the anchor from isolated `88,93` to `88-94`, which includes the qualifier and returned-descriptor conclusion.

### Cosmetic / precision: S397 anchor omits fields it teaches

Draft line 21 cites `160,164,171` but its `ino` and `sdev` definitions occur at 166 and 168-169, and the monitored-file conclusion continues at 161. The content is supported by the same pin, not invented.

**Required edit:** anchor `160-172` (and `74-77` for the explicit read-access explanation if retaining “readable without touching it”). The source documents descriptor metadata, not proof that a particular live process has exactly 40 watches or an atomic snapshot. Keep 40/40 as the separately evidenced comparison context, not as a man-page result.

## Answers to the draft's four questions

1. **Quote location/length:** yes, each explicitly designated Gate quote is 9 whitespace-delimited words and is located exactly at the claimed line after stripping HTML markup: S396 line 88; S397 line 160. Contextual fragments are also present at the named lines. Do not concatenate all S396 quoted fragments into one Gate quote: that totals 30 words. A more directly useful single Gate quote is the 21-word text at 93-94: “already being watched (perhaps via a different link to the same object), then the descriptor for the existing watch is returned.” Full grounding requires the anchor/qualifier edits above.
2. **Status/used-by:** wrong for the proposed citing-lesson integration under CORPUS; the frozen C3 parser ignores lesson paths, so a real lesson path does **not** trip `extra`.
3. **Tier/kind/scope:** `docs`, tier B is conservative and does not overreach. S396 needs per-instance scope. S397 supplies generic field semantics, not the empirical 40/40 result.
4. **Shape/order:** each proposed row has exactly 11 cells / 12 delimiter pipes, with no extra pipe embedded in a cell. At the named revision there are 332 registry rows, last/max ID S395; neither proposed ID exists. S396/S397 are the next IDs. Correctly staged scratch census accepts the appended rows, exit 0.

## Exercised evidence

Independent concurrent fetch commands (each exit 0, no stderr):

```
curl --fail --location --silent --show-error --output /fast/scratch/hyaku/mado-r56/R56W3RevLessonGate/man7-inotify_add_watch.2.html https://man7.org/linux/man-pages/man2/inotify_add_watch.2.html
curl --fail --location --silent --show-error --output /fast/scratch/hyaku/mado-r56/R56W3RevLessonGate/man7-proc_pid_fdinfo.5.html https://man7.org/linux/man-pages/man5/proc_pid_fdinfo.5.html
```

Python hashlib of independently fetched bytes:

- S396: 11,345 bytes, 258 lines; `98fe7feb381fa2687e8a3962e6d78a49cb1ad07c543f93449dcb42d6712c3d6d` — exact draft match.
- S397: 14,694 bytes, 366 lines; `f9e12387bf013d7c016f0015de5801932022a2fe6786d53e1cc84c385952d8a1` — exact draft match.

Audit invoked with `python3 -I /fast/scratch/hyaku/mado-r56/R56W3RevLessonGate/audit.py`. Frozen registry and parser came from `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:<path>`. One read-only `git archive ... corpus` supplied initial staging. The first census run exited 1 because that partial staging omitted existing tool/quality used-by targets; this is a staging failure, not a draft defect. After retrieving all 79 referenced mined paths from the same revision (none absent), the assigned command was:

```
TMPDIR=/fast/scratch/hyaku/mado-r56/R56W3RevLessonGate /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /fast/scratch/hyaku/mado-r56/R56W3RevLessonGate/census/corpus/SOURCES.md
# exit 0
file ok /fast/scratch/hyaku/mado-r56/R56W3RevLessonGate/census/corpus/SOURCES.md
```

Existing W01/W04 warnings are preserved in the receipt; no S396/S397 warning or error appeared. No full C1/C2/C3 counter or live compositor check was run: this seat audits draft source rows only. No tools installed. LSP is unavailable (`xd://lsp`: “No such tool”); source inspection and the actual parser probe are the fallback evidence, not semantic LSP claims.

## Deliverables and residual risk

All below are under `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevLessonGate/`:

- `receipts/gate-a2.txt` — commands, exact decisive output, source-line context, word counts, parser probe, and both census attempts.
- `receipts/man7-inotify_add_watch.2.html`, `receipts/man7-proc_pid_fdinfo.5.html` — independently fetched source bytes.
- `receipts/SOURCES-appended.md` — scratch registry candidate copied before cleanup; not an integration.

Scratch was removed. The later integrated lesson path, edited rows and final-tip census/counter remain unverified because they do not yet exist in this audited draft. C3 does not validate lesson back-references; do not claim otherwise. No runtime/saturation/resume behavior is changed or asserted by these source rows.

Self-evaluation: accuracy 4 (explicit single-quote versus contextual-fragment distinction); completeness 4 (future integration cannot be checked); clarity 4 (receipt preserves a failed staging attempt); actionability 5 (per-row edits specified); conciseness 4 (full command evidence is in the receipt). Overall 4.2/5. Highest-value improvement is applying the status/rationale correction before integration; the user should agree the draft audit itself is complete.
