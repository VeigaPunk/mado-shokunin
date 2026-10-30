# R56W3RevAuditA2B — corrected C1 sentence-to-pin audit

## Scope, axes, and recommendation

Attacked: K06–K12 and their mask/add-watch/canonical-watch/callback prose in Chain, path-list and Limits, including the five specifically named corrections. Revision: `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`; entry: `corpus/knowledge/hyprland-config-autoreload-r56.md`. All entry and source judgments below use a single archive of that revision, not the working tree. Read claims-frozen-v2.md, registration-v2.md and registration.md before auditing. No entry or predicate edits.

Axes: factual entailment, exact-line anchoring, error-path coverage, inference/observation honesty, reproducibility. Findings below are recommendations only, not an admission or a predicate judgment. No finding requires widening or changing a frozen predicate. This is an author-side scoped audit, not non-author closure.

**Result:** two substantive prose defects weaken source-level coverage, plus four strict single-line row overreaches and two bounded prose qualifications. No frozen-counter failure was established or claimed.

LSP prerequisite: `read xd://lsp` returned `No such tool: xd://lsp`; no server/status/references/definition/diagnostics interface was available. Used direct immutable pin reads, not grep as semantic proof. No grep-based absence claim is made.

## Findings by severity

### F1 — weakens the claim: the corrected “only dangling symlink” sentence is still false

Entry line 40 says status failure “for a glob result happens only for a dangling symlink.” `Hyprland-legacy-ConfigManager.cpp:1827–1833` tests **any** error code, not ENOENT or symlink identity:

```text
1827: std::error_code ec;
1828: auto file_status = std::filesystem::status(value, ec);
1830: if (ec) {
1831: ... "source= file from glob result is inaccessible ({}): {}", ec.message(), value);
1832: return "source= file " + value + " is inaccessible!";
```

Concrete input 1: `loop.conf -> loop.conf`, passed as a literal glob pattern. Native glibc `glob(..., GLOB_TILDE, ...)` returns rc 0 and that path; following status fails ELOOP, not a dangling-target ENOENT. Concrete input 2: an ordinary regular file is successfully globbed, then removed before status; status fails ENOENT without any symlink. The pin has no synchronization between glob and status. Isolated probe output:

```text
symlink-cycle: glob(flags=GLOB_TILDE) rc=0 matches=['/fast/scratch/hyaku/mado-r56/R56W3RevAuditA2B/isolated-probe/loop.conf']
stat follows symlinks: errno=40 Too many levels of symbolic links
regular-disappears-after-glob: glob(flags=GLOB_TILDE) rc=0 matches=['/fast/scratch/hyaku/mado-r56/R56W3RevAuditA2B/isolated-probe/ordinary.conf']
stat follows symlinks: errno=2 No such file or directory
```

The probe exercises native glibc glob plus following `os.stat`, not Hyprland or its C++ error-code overload; connecting these inputs to the pinned unconditional `if (ec)` is source inference. The error branch itself is explicit.

One-sentence correction: **“Any status error, including a dangling link, a symlink cycle, or a path becoming inaccessible/disappearing after glob expansion, returns ‘inaccessible’ before the failed path is appended and stops the remaining matches.”** The stable missing-literal no-match correction remains valid; do not undo it.

### F2 — weakens the claim: Limits drops the descriptor-match precondition

Entry line 137 says `onInotifyEvent` “calls the callback once per event” and “every event kind, including ... IN_IGNORED, reaches reload().” Chain line 23 already references the matched watch, and K12 correctly distinguishes a matched watch. Limits does not.

Deciding pin, `Hyprland-ConfigWatcher.cpp`:

```text
100: const auto WD = std::ranges::find_if(m_watches, [wd = ev->wd](const auto& e) { return e.wd == wd; });
102: if (WD == m_watches.end())
103:     Log::logger->log(Log::ERR, "CConfigWatcher: got an event for wd {} which we don't have?!", ev->wd);
104: else
105:     m_watchCallback(SConfigWatchEvent{
106:         .file = WD->file,
107:     });
```

Counterexample input to this control flow: current `m_watches = [{wd:7,file:"a.conf"}]`, event `{wd:6,mask:IN_IGNORED,len:0}`. The search returns end, logs and does **not** invoke the callback. No mask check is necessary for this rejection. A queued IN_IGNORED from an old removed watch can lack a current descriptor match after rebuilding the list (inference from cleanup at 45–49 and re-add at 59–71). `man7-inotify.7.html:307–310` explicitly includes removals by `inotify_rm_watch` among sources of IN_IGNORED. Another specified input is `{wd:-1,mask:IN_Q_OVERFLOW}` with the above valid-watch list; man lines 315–316 specify wd -1. This input also logs without reload. These are static branch counterexamples, not a replay of the compositor.

One-sentence correction: **“For each well-formed event whose wd still matches a current m_watches entry, the handler invokes the callback once without filtering the mask, so a matched IN_IGNORED can reach reload(); unmatched descriptors only produce a diagnostic.”**

Entry line 138's rename-over conclusion needs the same qualification: a removal event for the still-listed watch reaches the callback; the absence of a mask check alone does not prove an arbitrary IN_IGNORED event reloads. The corrected distinction between kernel observations and unobserved Hyprland reload consequences is otherwise sound.

### F3 — cosmetic/anchoring: four K rows exceed the physical line in a strict single-line audit

The row heading promises a bounded reading of a single line. K10–K12 are accurate in the surrounding function but need other lines for their contextual assertions; K09 should describe an add attempt, not guaranteed registration. Full details and corrections are in the required table below. This is not a claim that their full-function behavior is false.

### F4 — weakens the claim if read without its ordinary-file assumption: “no parent directory is ever watched”

Entry line 47's broad assertion is not guaranteed by these pins. `resetHLConfig` unconditionally appends the main path at legacy line 779; watcher lines 54–60 accept a directory and select the directory mask. A main config argument that names the parent directory is not excluded by the pinned watch-list code. The negative statement should be about **adding parents of sourced paths**, rather than every possible directory watch. This qualification was already noted, but not repaired, by the earlier prose audit P26.

Correction: **“The watcher adds no separate parent-directory watch for a missing source target, so with an ordinary-file main config it has no such directory watch to observe later creation (inference).”** This is a source-contract qualification, not a demonstrated normal-host failure.

### F5 — cosmetic: duplicate-watch prose still says one entry per list entry

Entry line 46 says `setWatchList` “records one m_watches entry per list entry (52–73).” Lines 59–62 append the primary entry, and lines 67–71 append another entry for a successfully resolved symlink. For `paths=["link.conf"]` with a regular target, there are two `m_watches` entries. The corrected distinction between repeated records and one kernel watch per inode is otherwise supported by the inotify pin.

Correction: **“setWatchList records one primary m_watches entry per list entry, plus a canonical entry for each successfully resolved symlink; repeated adds for the same inode reuse the kernel watch.”**

## Required row table

Convention: “pin line” means the entire physical source line at the named locator, not only the frozen substring. Thus K07/K08 are SUPPORTED: both propositions explicitly disclose what their quoted prefixes omit, and the physical lines show those bits. Under a stricter substring-only convention those disclosed additions would also be OVERREACH; that is not the convention used here. Contextual clauses requiring a different physical line are marked OVERREACH, as requested.

CW = `.ufo/waves/round-56/fetch/Hyprland-ConfigWatcher.cpp` at the audited revision.

| row | verdict | pin lines | correction |
|---|---|---|---|
| K06 | SUPPORTED | CW54: `const bool isDirectory = std::filesystem::is_directory(path, ecDir);` | — |
| K07 | SUPPORTED | CW55: `const uint32_t fileMask = IN_CLOSE_WRITE \| IN_DONT_FOLLOW;` | —; quoted-prefix limitation is expressly disclosed. |
| K08 | SUPPORTED | CW56: `const uint32_t directoryMask = fileMask \| IN_CREATE \| IN_DELETE \| IN_MOVED_TO \| IN_MOVED_FROM;` | —; quoted-prefix limitation is expressly disclosed. |
| K09 | OVERREACH | CW60: `.wd = inotify_add_watch(m_inotifyFd.get(), path.c_str(), mask),`; CW59–62 store the result without checking success. | This line calls inotify_add_watch on path.c_str() with mask on m_inotifyFd and stores the returned descriptor. |
| K10 | OVERREACH | CW67: `if (!ec && !ec2 && IS_SYMLINK) {`; the canonical-watch action is on CW68–69, not CW67. | This condition requires both ec and ec2 to be clear and IS_SYMLINK to be true. |
| K11 | OVERREACH | CW69: `.wd = inotify_add_watch(m_inotifyFd.get(), CANONICAL.c_str(), IN_CLOSE_WRITE),`; “second” is established by the earlier append at CW59–62. | This line calls inotify_add_watch on CANONICAL.c_str() with IN_CLOSE_WRITE as its only mask argument. |
| K12 | OVERREACH | CW105: `m_watchCallback(SConfigWatchEvent{`; “for a matched watch” is established by CW100–104, not CW105. | This line invokes m_watchCallback with an SConfigWatchEvent initializer. |

No K06–K12 proposition was found contradicted in its surrounding function; K09's unconditional registration wording is stronger than the actual unchecked call. The other strict anchoring findings are cosmetic, not changes to mask or callback semantics.

## Sentence audit of the affected prose

Entry line numbers refer to the archived entry. Each cell separates direct code, inference and inherited observations; grouped clauses below cover the mask/watch/callback sentences and the five named corrected items, not unrelated K01–K05/K13–K30 claims.

| entry location / sentence or clause | disposition | deciding evidence / qualification |
|---|---|---|
| Chain 3, line 22: cleanup and clear; is_directory selects file/directory mask | Supported as control flow | CW45–57; “removes” means attempts because return values are unchecked. |
| Chain 3: add path watch | Supported as an attempt only | CW59–62; actual success is not checked (same issue as K09; Limits discloses it). |
| Chain 3: symlink/canonical condition, second add, IN_CLOSE_WRITE | Supported as conditional attempts | CW64–71. The prose does not explicitly name ec2 but successful is_symlink and CW67 supply that requirement. |
| Chain 3: second watch carries link path | Supported | CW70 `.file = path`; not `.file = CANONICAL`. |
| Chain 4, line 23: readable event route, read, descriptor search, callback with stored file | Supported with match precondition | EventLoopManager70–72,127–128; CW80–107. Duplicate descriptors select the first match via find_if, not all records. |
| Chain 4: event name never read; reported path is stored watch path | Supported for delivered callbacks | Entire CW80–111 reads ev->wd and ev->len but never ev->name; CW106 copies WD->file. |
| Chain 9, line 28: IN_CLOSE_WRITE and IN_DONT_FOLLOW meanings | Supported | MAN185–186 and MAN258–262. IN_DONT_FOLLOW is an add-time flag, not an assertion that the target is unwatched. |
| Chain 9: symlink primary watches link; second watches target | Supported conditional source reading | CW55,60,65–70 + MAN261–262; both adds can fail. It does not establish design intent; sentence correctly declines to infer that intent. |
| Chain 9: lab saw link silent/target fire | Historical observation, not re-exercised | Explicitly attributed to wave 1; no host symlink write was performed by this seat. |
| Path list, line 40: glob order, value, following status | Supported | LEG1824–1828; following-status semantics are the standard-library contract, not implementation code pinned here. |
| Path list, line 40: status failure only dangling; inaccessible return | First clause false, return supported | F1; LEG1830–1833 handles every ec. |
| Path list, line 40: missing literal exits at no-match; failed entry not appended and rest skipped | Supported for a stable missing literal; error control flow supported | LEG1816–1820,1830–1836; disappearance after expansion is the F1 race exception. |
| Consequences, line 46: no dedup; file reached twice listed twice | Supported | LEG1835–1839, no membership guard in full handleSource; CW52–73 has no duplicate-path guard. |
| Consequences, line 46: one record per entry | Overstrong count | F5; canonical records add another for symlinks. |
| Consequences, line 46: same inode reuses kernel watch, later removal unchecked | Supported source/man inference | MAN85–92,276–302; CW45–47. Historical wd=1 lab result is attributed and was not rerun. |
| Consequences, line 47: missing target not listed; no parent ever; later creation unseen | Stable nomatch supported; universal directory claim overreaches; last clause labelled inference | F4; LEG779 and CW54–57 permit a directory as main path. |
| Consequences, line 48: symlink-to-file spelling retained; link and canonical watches | Supported conditional attempts | LEG1825,1828,1835–1839 and CW59–71. No canonical replacement of value occurs. |
| Consequences, line 49: directory symlink skipped | Supported via following status | LEG1828,1843–1845. |
| Consequences, line 50: missing main path appended; same loop; unchecked add | Supported at list/add level | LEG779 precedes verifyConfigExists at 781; CW52–62. Missingness at later watch time is not established by this ordering. |
| HOME correction, line 54: substitution and unset construction | Correctly bounded, with a static-cache qualification | MISC64–66 caches getenv on first tilde call; unset at that initialization yields the null construction. Later HOME changes need not be seen. Throws claim is explicitly a prior libstdc++ observation, not a pinned Hyprland-build result. No catch appears in full LEG1802–1855. |
| Glob correction, line 70: ordering and dot matches | Correctly qualified libc observation, not proved by the source pin alone | LEG1816 has GLOB_TILDE without GLOB_NOSORT; text explicitly leaves libc/locale linkage unknown and attributes glibc tests to wave 2. No new locale claim made. |
| Limits, line 134: IN_DONT_FOLLOW not confirmed by observed mask 0x8 | Honest add-flag/observation separation | MAN258–262 describes extra bits specified when adding; CW55/60 show the add flag. Historical fdinfo/inode match not independently rechecked in this seat. |
| Limits, line 135: missing headers/provider linkage and legacy assumption | Honest limitation | CW includes ConfigWatcher.hpp/ConfigManager.hpp rather than providing their declarations; do not promote unpinned linkage to an observed fact. |
| Limits, line 136: init failure, unchecked add, no overflow branch | Supported | CW21–26,59–62,80–111; EventLoopManager127–128 guards descriptor validity. |
| Limits, line 137: every event invokes callback/reloads | False without wd match | F2; CW100–107. No mask filtering and no coalescing are true negative reads of CW80–111, not a guarantee of callback for an unmatched event. |
| Limits, line 137: several events could cause several reloads; kernel lab counts | Possibility inference supported, historical counts not rerun | CW87–110 and LEG1079–1082; claim is “could,” not an observed compositor reload count. |
| Limits, line 138: inode basis, rename-over IN_IGNORED, moved inode retains watch | Inode basis supported; precise save sequence explicitly inherited lab observation | MAN225–228,307–310; not a test on running Hyprland. |
| Limits, line 138: rename-over event reaches reload; reload/list consequences | Needs F2 match qualification; latter inference explicitly labelled | CW100–107; LEG1079–1082,731,743,750 and source no-match branch. No claim that rename-over reload was observed is warranted. |

## Commands, evidence and deliverables

Exact read-only revision acquisition command (exit 0, no output):

```sh
mkdir -p /fast/scratch/hyaku/mado-r56/R56W3RevAuditA2B /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevAuditA2B && git -C /home/vgpnk/Projects/shokunin/mado-shokunin archive 0f3a54361a9824484d0801679ceb1fd8ac7c32e1 corpus/knowledge/hyprland-config-autoreload-r56.md .ufo/waves/round-56/fetch .ufo/waves/round-56/w2/R56W2RevProsePath.md | tar -x -C /fast/scratch/hyaku/mado-r56/R56W3RevAuditA2B
```

Actual correction diff inspected (read-only):

```sh
git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff 28fc86ac2359ec27406d8a2c63bef82ea6e947ed 0f3a54361a9824484d0801679ceb1fd8ac7c32e1 -- corpus/knowledge/hyprland-config-autoreload-r56.md
```

Decisive output: `1 file changed, 36 insertions(+), 35 deletions(-)`; includes corrected masks, dangling-only error text, duplicate-watch distinction, HOME/glob qualifications and Limits. All judgments use the complete archived corrected text, not the display's shortened diff lines.

Probe command (exit 0; exact output quoted under F1 and in status-counterexamples.txt):

```sh
env TMPDIR=/fast/scratch/hyaku/mado-r56/R56W3RevAuditA2B python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevAuditA2B/status-probe.py
```

An initial exploratory version was executed in the tool's persistent Python evaluation kernel (not an explicitly `-I` child); the reproducible receipt was then overwritten by the above `python3 -I` run. Both runs used only assigned scratch fixtures. Reported decisive probe output is from the isolated child.

Null results: the full `git show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:corpus/knowledge/hyprland-config-autoreload-r56.md` followed by complete archived CW37–74/CW80–111 reads found no contradictory mask values, no use of ev->name, no ev->mask filter, and no add-watch return check. These are direct source inspections, not executable tests or semantic LSP evidence. They are preserved with line numbers in pin-excerpts.txt.

All deliverable paths below are relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`:

- `.ufo/waves/round-56/w3/R56W3RevAuditA2B.md` — this report.
- `.ufo/waves/round-56/w3/R56W3RevAuditA2B/pin-excerpts.txt` — numbered immutable entry/source evidence.
- `.ufo/waves/round-56/w3/R56W3RevAuditA2B/status-probe.py` — reproducible native-glob/following-stat counterexamples.
- `.ufo/waves/round-56/w3/R56W3RevAuditA2B/status-counterexamples.txt` — isolated probe receipt.

## Residual risks and verification gaps

- No Hyprland build/run/reload, no compositor/config/service change, and no live /proc or journal access. The seat was not authorized for those host sources.
- No C1/C2/C3 counter, controls harness or full selftest run; this is source entailment auditing, not re-scoring. No conclusion about saturation, same-identity runtime rerouting, or resume_continuity_v1: those mechanisms are outside this entry/diff.
- Prior lab results for rename-over, duplicate wd, libstdc++ null-string construction, libc collation and host fdinfo are explicitly inherited observations; they were not silently counted as new tests. Only the two glob/status counterexamples were newly exercised.
- No frozen predicate changed, no admission verdict, no tracked-file edit, no git mutation, no delegation/background job, no installation/update, no PATH-directory write. Existing tools suffice.
- Assigned scratch was removed after preserving these receipts; only named report/deliverable paths remain.

Self-evaluation: accuracy 4/5 (native status probe is not the C++ overload); completeness 4/5 (historical host/lab claims retained as unverified observations); clarity 4/5 (strict physical-line convention is disclosed); actionability 5/5 (specific pin locations, counterexample inputs and one-sentence corrections); conciseness 4/5 (sentence coverage makes the report longer). Overall 4.2/5. Highest-value independent follow-ups are the C++ status overload on the same loop and an unmatched-wd event replay in an isolated watcher harness; neither is required to see the pinned unconditional error/match branches. The user should agree that the report distinguishes newly exercised evidence from source inference and inherited observation.
