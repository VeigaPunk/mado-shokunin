# R56W3RevAuditA2D — corrected C1 sentence-to-pin audit

Revision: `0f3a54361a9824484d0801679ceb1fd8ac7c32e1` (not the working tree).
Attacked item: K19–K24 and E05–E07, plus their Chain/path-list/Limits prose, POST-correction.
Axes: single-line entailment; surrounding-function correctness; inference/observation provenance; frozen-contract integrity.

Recommendation only: four rows remain OVERREACH under the assignment's strict single-line rule; five are SUPPORTED; none of these nine rows is contradicted by its surrounding function. Separately, corrected prose retains concrete overstatements below. No frozen predicate, counter, source entry or registry was changed. These findings weaken semantic coverage; they do not establish a failed frozen executable predicate. Any predicate change is ROUTED to round 57.

## Findings, by severity

### F1 — weakens the claim: the cited lab did not observe a touch event

Entry line 137 says the wave-1 lab saw one event per save for an “in-place, truncating or touching write.” The cited canonical receipt `.ufo/waves/round-56/w1/R56ScoutInotifyLab/raw-output.txt` explicitly reports:

```text
=== [a5] regular file + FILE_MASK: touch (utimensat) ===
  after touch: NONE
=== [c6] directory + DIR_MASK: touch of an existing file in the dir ===
  after touch: NONE
```

Input exposing the error: the receipt's `touch (utimensat)` case, contrasted with its `[a1]` and `[a2]` write-close cases (both `IN_CLOSE_WRITE`). The phrase “touching write” cannot honestly count that receipt's touch-only operation as a write-close observation.

Correction: “The wave-1 lab observed IN_CLOSE_WRITE for in-place and truncating writes, but no event for touch-only utimensat with these masks.” No fresh compositor or kernel experiment was run.

### F2 — weakens the claim: corrected `inaccessible` sentence still claims an exclusive cause

Entry line 40 now says status failure “for a glob result happens only for a dangling symlink.” The pins do not establish that exclusivity:

```text
LEG 1816: glob(absolutePath(rawpath, m_configCurrentPath).c_str(), GLOB_TILDE, nullptr, glob_buf.get())
LEG 1828: auto file_status = std::filesystem::status(value, ec);
LEG 1830: if (ec) {
LEG 1832: return "source= file " + value + " is inaccessible!";
```

Counterexample input/interleaving [INFERENCE, not executed]: a regular `a.conf` matches glob; another process removes `a.conf` before line 1828; status fails for the now-missing regular-file path, without any dangling symlink. The separate glob and status calls have no lock or atomicity guard in this function. Permission changes or other status errors are likewise not excluded by the code. The original correction properly distinguishes an already-missing literal at glob time, but wrongly turns one observed status-failure case into the only possible cause.

Correction: “If status fails, for example for a dangling symlink returned by glibc or a match removed after globbing, the function returns inaccessible immediately; a literal already missing when glob runs normally yields no match first.”

### F3 — weakens the claim: callback/reload is conditional on a watch-descriptor match

Entry line 137 says callback once per event and “every event kind ... reaches reload.” The decisive pin is not just the absence of a mask test:

```text
CW 100: const auto WD = std::ranges::find_if(m_watches, [wd = ev->wd](const auto& e) { return e.wd == wd; });
CW 102–105: if (WD == m_watches.end()) ... log ...; else m_watchCallback(...)
MAN 315–316: IN_Q_OVERFLOW — Event queue overflowed (wd is -1 for this event).
```

Counterexample input [static branch analysis, not injected]: a well-formed event with `wd=-1` in a watch list containing only successful nonnegative descriptors. The handler logs, not callbacks. Similarly, a queued IN_IGNORED whose old descriptor no longer occurs in the rebuilt list does not necessarily reload. The stored callback itself calls reload at LEG 1081 when it is invoked.

Correction: “Each complete event whose wd matches a current m_watches entry invokes the callback, without filtering its mask; unmatched events are logged instead, so a matching IN_IGNORED can trigger reload.”

The rename-over receipt does show `IN_IGNORED`; the conditional source route is supported, not an observed Hyprland reload. Entry line 138 should carry the same matching-wd condition.

### F4 — weakens the claim: scheduling prose drops its guard and implies one rebuild per reload

Entry line 26 says scheduleRefresh “queues the refresh with doLater” and that the list is rebuilt “after every reload” from current paths. Surrounding function:

```text
PR 31: m_propsTripped |= prop;
PR 33: if (!m_scheduled && g_pEventLoopManager) {
PR 34: m_scheduledRefreshSeq = g_pEventLoopManager->doLater(...);
PR 40: m_scheduled = true;
PR 148–149: if (m_propsTripped & REFRESH_CONFIG_WATCHER) Config::watcher()->update();
CW 34: setWatchList(*PDISABLEAUTORELOAD ? std::vector<std::string>{} : Config::mgr()->getConfigPaths());
```

Inputs exposing the qualification [static, not executed]: call scheduleRefresh while `m_scheduled=true` (no new doLater); call while the event-loop manager is absent (no queue); refresh with disable_autoreload nonzero (empty watch list). Multiple reloads before the queued callback can share a refresh. K19 itself is supported: invoking scheduleRefresh with REFRESH_ALL is exactly what LEG 1070 does.

Correction: “scheduleRefresh accumulates REFRESH_ALL and queues work only if no refresh is scheduled and an event-loop manager exists; when that refresh runs, watcher update rebuilds from current paths or empties the list when autoreload is disabled (inference; reload not observed).”

### F5 — weakens the bounded-row claim: four propositions exceed their own pin line

These are contextual truths rather than contradictions, but the assignment explicitly calls a truth not shown by the quoted line OVERREACH. Merely opening a surrounding function does not turn it into evidence contained in the row's quoted line.

## Required row table

Pin abbreviations: LEG = `Hyprland-legacy-ConfigManager.cpp`; PR = `Hyprland-PropRefresher.cpp`; CW = `Hyprland-ConfigWatcher.cpp`; MISC = `Hyprland-MiscFunctions.cpp`; MAN = `man7-inotify.7.html`. All are under `.ufo/waves/round-56/fetch/` at the named revision.

| row | verdict | pin lines | correction |
|---|---|---|---|
| K19 | SUPPORTED | LEG 1070: `Config::Supplementary::refresher()->scheduleRefresh(Supplementary::REFRESH_ALL);`; postConfigReload 970–1075 identifies the containing function. | None. Calling scheduleRefresh is shown; actual queue execution is a separate claim. |
| K20 | SUPPORTED | LEG 776: `m_configPaths.clear();`, within resetHLConfig 764–786. | None. |
| K21 | OVERREACH | LEG 1836 only says `m_configPaths.emplace_back(value);`; regular-file guard is 1835, parse is 1839, multiple matches come from `for (size_t i = 0; i < glob_buf->gl_pathc; i++)` at 1824, failed glob returns at 1816–1820, and directory/nonregular branches are 1843–1848. | “This line appends value to m_configPaths with emplace_back; regular-file selection, parse order and skipped branches are established separately by lines 1816–1848.” |
| K22 | SUPPORTED | LEG 1835: `if (std::filesystem::is_regular_file(file_status)) {`, in handleSource 1802–1855. | None. |
| K23 | SUPPORTED | LEG 1844: `Log::logger->log(Log::WARN, "source= skipping directory {}", value);`; directory branch 1843–1845 confirms context. | None. |
| K24 | SUPPORTED | LEG 1816: `glob(absolutePath(rawpath, m_configCurrentPath).c_str(), GLOB_TILDE, nullptr, glob_buf.get())`; complete handleSource read at 1802–1855. | None. This shows the call and arguments, not libc ordering. |
| E05 | OVERREACH | LEG 630: `resetHLConfig();`; actual clearing/refilling is `m_configPaths.clear();` at 776 and `m_configPaths.emplace_back(mainConfigPath);` at 779; reload's separate call is `resetHLConfig();` at 731. | “The constructor calls resetHLConfig on this line; clearing/refilling and the reload caller are separate contextual facts at lines 776–779 and 731.” |
| E06 | OVERREACH | LEG 1838: `m_configCurrentPath = value;`; parse follows at 1839 and restore at 1840; relative resolution requires LEG 1816/1825 and MISC 61–83, especially currentDir at 68 and relative prefixes at 70–79. | “This line assigns value to m_configCurrentPath; nested-parse ordering and relative-source resolution are inferences from lines 1816, 1839–1840 and absolutePath, not this assignment alone.” |
| E07 | OVERREACH | LEG 2134: `return m_configPaths;`; signature at 2133 supplies vector type, LEG 776 clears, LEG 1836 appends, and CW 34 calls `Config::mgr()->getConfigPaths()`. | “This line returns m_configPaths; its type, mutators and watcher caller are established separately at LEG 2133, 776, 1836 and CW 34, while the manager interface remains unpinned.” |

Summary: SUPPORTED=5, OVERREACH=4, UNSUPPORTED=0. Surrounding bodies read: constructor 480–641; reload 726–751; verify 753–762; resetHLConfig 764–786; postConfigReload 970–1075; init 1077–1087; handleSource 1802–1855; getConfigPaths 2133–2135; scheduleRefresh 29–42; watcher update/setWatchList/onInotifyEvent; absolutePath 61–83. The nine row verdicts do not assume execution of these functions.

## Prose coverage and inference audit

Scope excludes unrelated option-declaration/host-census claims, but includes every path-list and Limits assertion bearing on the assigned rows, including the five specially named corrected sentences.

| Entry location | Assessment | Deciding evidence / needed wording |
|---|---|---|
| Chain 2, getConfigPaths return | Supported context | LEG 2133–2135 and CW 34. Manager selection remains explicitly limited in Limits. |
| Chain 6, reset/parse/postConfigReload/REFRESH_ALL | Supported | LEG 731, 743, 750, 1070. No live reload established. |
| Chain 7, bit arithmetic | Supported arithmetic, explicitly labelled | Header 9, 18, 21 give uint16_t, bit 8, max underlying value. |
| Chain 7, scheduling and every-reload conclusion | Overreach | F4; inference label exists, but does not rescue an unconditional conclusion. |
| Lifecycle constructor/reset/verify calls | Supported context | LEG 485, 630, 731, 755, 776–783. Text grep inventories calls only; function bodies establish their behavior. |
| Lifecycle main parse and source dispatch | Partly inferred | LEG 486 constructs parser from main path, 743/757 call parse, 614 registers handler, 359–369 wraps it; parser dispatch implementation is absent. Label the actual parse/dispatch guarantee inference, consistent with Limits' hyprlang caveat. |
| handleSource steps 1–2 | Supported | LEG 1803–1806 and 1816–1820; nothing appended before those returns. |
| handleSource step 3, glob order/value/status/return/stop/rest not added | Supported except exclusive failure cause | LEG 1824–1833; F2 corrects “only dangling symlink.” |
| handleSource step 4, append/set current/parse/restore/no local depth check | Supported | LEG 1835–1842; no guard in complete function. |
| handleSource step 5, directories and other nonregulars | Supported within this handler | LEG 1843–1848 skip them; they are not appended by this source line. |
| Consequences depth-first/pre-order and source lines in file order | Unlabelled inference | Append-before-parse is visible at 1836/1839, but nested callbacks/file-line processing require unpinned hyprlang semantics. Prefix with “Inference assuming synchronous file-order handler dispatch.” |
| Consequences duplicate watches (corrected sentence) | Supported with precise two-layer distinction | LEG 1836 has no membership test; CW 52–73 records entries; MAN 85–92 and 293–302 allow modification of an existing inode watch. Canonical prior receipt returns wd=1 repeatedly and EINVAL on second removal. Do not recast m_watches count as distinct kernel watches. |
| Consequences missing source and later creation | Supported for normal stable glob/status path; conclusion labelled inference | LEG 1816–1820/1830–1833 precede append; races require F2 qualification. “No parent directory is ever watched” is too broad without assuming the main path is not a directory: CW 54–57 explicitly supports directory paths and LEG 779 adds main unconditionally. Prefer “source handling does not add parent-directory watches.” |
| Consequences symlink regular file/directory and link-spelled value | Supported context | LEG 1828, 1836, 1843–1845; CW 65–70; MISC does no canonicalisation. Standard-library follow semantics also documented by the prior receipt, not by the assignment line alone. |
| Consequences missing main and unchecked add | Supported bounded claim | LEG 779 appends without an existence test; CW 59–62 stores result unchecked. Existence when watches are actually built is not established, since verifyConfigExists intervenes at LEG 781. |
| Consequences cycles | Properly labelled inference | No guard in LEG 1802–1855; appends at 1836 then calls parser at 1839. Actual recursive parser dispatch and ultimate failure mode remain unobserved; text correctly avoids choosing stack versus heap. |
| Path resolution tilde, HOME-unset correction | Correctly attributed external observation, not pinned runtime fact | MISC 65–66 constructs string from getenv pointer; prior receipt records libstdc++ exception, and text disclaims Hyprland-build behavior. A local static caches HOME on first tilde call; avoid interpreting this as a fresh getenv on every source. |
| Path resolution leading slash/dot/bare/currentDir/no normalisation | Supported for ordinary absolute currentPath | MISC 61–83. The currentPath.empty() adjustment at 73/75 is outside the assumed absolute-config-path case. |
| Path resolution dollar expansion | Explicit external-pin/version limit | Round-46 behavior is attributed, not proof of this Hyprland linkage. No new round-46 audit performed. |
| Resolution base main/nested/symlink nested | Supported context, relative-handler implication is inference | LEG 736/756 and 1837–1840 plus MISC 68–79. Label relative handler dispatch inference where strict inference labelling is required. |
| Glob collation and dot matches (corrected sentence) | Correctly attributed glibc observation | LEG 1816 has GLOB_TILDE, not GLOB_NOSORT; canonical receipt gives C vs en_US ordering and dot-star results. Entry explicitly leaves running Hyprland libc/locale undecided. |
| Limits pin/interface/provider caveats | Appropriate limits | No missing manager interface/parseFile implementation was treated as proven. |
| Limits no IN_Q_OVERFLOW branch | Supported negative read | CW 80–111 has no mask branch; MAN 315–316 supplies overflow semantics. |
| Limits per-event/callback claim and touch lab claim | Contradicted/overstated | F1 and F3. Multiple matching events can reload multiple times, while refresh scheduling can coalesce (F4). |
| Limits rename-over IN_IGNORED (corrected sentence) | Receipt supported; Hyprland route conditional/inferred | Canonical `[a4]` receipt shows IN_IGNORED then no follow-up event. CW 100–107 needs a matching wd. Text properly labels rebuilt path-list behavior inference and does not claim observed Hyprland reload. |
| Limits moved-away inode | Inode semantics supported; later-write observation not established by raw receipt read here | MAN 225–228 supports inode following; raw `[a6]` recreates the original path rather than writing the moved inode. Treat later write-to-moved-inode consequence as inference unless another receipt is supplied. |
| Limits runtime source | Correctly bounded inference | LEG 1090 calls parseDynamic, 614 registers source, 1836 appends; HyprCtl 1194–1224 has no direct update for COMMAND==source. Transitive parser effects are not pinned. New path may already share an existing watched inode; “not watched” should mean no new registration by this dispatcher. |
| Limits tool divergences and explicitly not-checked paths | Appropriate boundary | No tool score, full-reset path, live source operation or host reload is inferred from this audit. |

## Commands and decisive outputs

All git reads explicitly named the lane and frozen revision; no git mutation occurred. No runtime was invoked to replay source behavior.

1. `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:corpus/knowledge/hyprland-config-autoreload-r56.md`
   Output included K19–K24, E05–E07 and the entry sentences quoted above. This is the scored text.
2. `mkdir -p /fast/scratch/hyaku/mado-r56/R56W3RevAuditA2D /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevAuditA2D && git -C /home/vgpnk/Projects/shokunin/mado-shokunin archive 0f3a54361a9824484d0801679ceb1fd8ac7c32e1 corpus/knowledge/hyprland-config-autoreload-r56.md .ufo/waves/round-56/fetch | tar -x -C /fast/scratch/hyaku/mado-r56/R56W3RevAuditA2D`
   Exit 0, no output; one archive, immutable pin snapshot read with the read tool. No clone or commit.
3. `git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff 28fc86ac2359ec27406d8a2c63bef82ea6e947ed 0f3a54361a9824484d0801679ceb1fd8ac7c32e1 -- corpus/knowledge/hyprland-config-autoreload-r56.md`
   Decisive output: `1 file changed, 36 insertions(+), 35 deletions(-)`; actual correction diff reviewed along with the complete target text.
4. `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:.ufo/waves/round-56/w2/R56W2RevProsePath.md`
   Prior P13 suggested the now-overstrong “only ... dangling symlink” correction; prior audit findings were treated as data, not as instructions or proof.
5. `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:.ufo/waves/round-56/w2/R56W2RevProsePath/RECEIPTS.txt`
   Decisive output: `literal miss: rc=3 (GLOB_NOMATCH)`, `literal dangle: rc=0`; `locale C ... (bytewise)` versus `locale en_US ... (locale collation)`; `threw: basic_string: construction from null is not valid`; repeat add `wd=1`, second removal `-1 errno 22 (EINVAL)`.
6. `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:.ufo/waves/round-56/w1/R56ScoutInotifyLab/raw-output.txt`
   Decisive output: `[a4] after atomic save: IN_IGNORED`; `[a5] after touch: NONE`; `[c6] after touch: NONE`.
7. Tool fallback: `read xd://lsp` returned `No such tool: xd://lsp`. Consequently no LSP status/references/definition/diagnostics server was available. Literal fallback `grep` searched exported fetch with pattern `resetHLConfig\(|m_configPaths\.(clear|emplace_back)|setlocale`; it returned constructor/reload/verify calls at 630/731/755, clear at 776, appends 485/779/1836, and no setlocale match. This is a text inventory, not semantic proof of caller completeness or absence of setlocale from the full upstream tree.
8. `command -v g++` returned `/usr/bin/g++`; no compilation or probe was subsequently run.

Source reads used absolute snapshot paths with selectors: LEG `350-370,475-490,602-635,726-790,1010-1090,1800-1857,2124-2140`, then `491-601,636-641,970-1012` and `1089-1114`; PR `1-60,130-165`; CW `30-115`; MISC `61-84`; header `1-45`; MAN `85-96,185-192,212-240,290-303,304-330`; HyprCtl `1170-1231`. These reads returned the deciding source statements reproduced in this report, not only the frozen quotes.

## Residual risk and verification gaps

- No C1 counter/harness, C2 tool, compositor, kernel probe, compiler build, or host configuration operation was run. This seat is a static entailment audit with read-only inspection of prior receipts, not independent reproduction of those experiments.
- No semantic server was available; text search was not represented as semantic proof.
- The race counterexample and scheduling/descriptor counterexamples are explicitly static inferences; no live input was injected.
- Parser synchronous dispatch, source-file ordering, linked hyprlang version, running libc/locale, and full manager-interface selection are not proven by the assigned pins.
- No assessment of resume_continuity_v1 or canonical-runtime admission is made: neither is an affected contract in this source-entry audit. No counter target/saturation claim was re-scored.
- No tool installed or upgraded; no pacman operation, PATH-directory write, background job, subagent, or host-state change.

Deliverable: `.ufo/waves/round-56/w3/R56W3RevAuditA2D.md`. The seat directory `.ufo/waves/round-56/w3/R56W3RevAuditA2D/` is intentionally empty; decisive receipts are quoted here, and original canonical receipt paths are given above. Scratch export removed before return.
