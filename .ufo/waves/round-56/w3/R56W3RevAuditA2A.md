# R56W3RevAuditA2A — post-correction sentence-to-pin audit

Attacked item: C1 entry `corpus/knowledge/hyprland-config-autoreload-r56.md`, K01–K05, E08–E09, and their Chain/path-list/Limits prose, at **0f3a54361a9824484d0801679ceb1fd8ac7c32e1**. No entry edits, git mutations, host-config changes, delegated work, or compositor commands. This is an author-seat review recommendation, not non-author closure or admission.

Axes: sentence entailment; single-line citation precision; explicit inference/observation boundaries; reproducible evidence; zero lane/host mutation outside assigned deliverables. Frozen v2 claims/registration were read first; v1 §C1 was read for unchanged rules. No predicates, targets, counters or kill rules were changed.

## Findings, by severity

All findings below **weaken the claim's semantic/source-level account**, not its frozen lexical predicate. No blocking-counter finding is claimed; counters were not run. Frozen-predicate changes, if desired, are routed to round 57.

### F1 — corrected inaccessible sentence still falsely restricts status errors

Location: entry **line 40**, path-list step 3: “If it fails, which for a glob result happens **only for a dangling symlink** …”.

Input: `source = /absolute/path/loop.conf`, with `loop.conf -> loop.conf`. A self-referential symlink is not a link to a nonexistent pathname. Fresh libc probe returned:

```text
PROBE self-referential symlink: glob_rc=0 matches=1
STAT: errno=40 name=ELOOP
LSTAT: symlink exists; its target is itself, not a missing pathname
```

Deciding pin: `Hyprland-legacy-ConfigManager.cpp:1828–1833`:

```cpp
auto file_status = std::filesystem::status(value, ec);
if (ec) {
    Log::logger->log(Log::ERR, "source= file from glob result is inaccessible ({}): {}", ec.message(), value);
    return "source= file " + value + " is inaccessible!";
}
```

There is no ENOENT-only restriction. Permission failures and disappearance between glob and status are additional [INFERENCE] counterexamples; they were not exercised. The fresh probe exercises libc glob + Python's stat syscall, not Hyprland or C++ filesystem itself; the pin supplies the generic C++ error-code branch.

Correction: **“If status fails for a returned match—for example a dangling or looping symlink, an inaccessible target, or a path that disappeared after glob—the function immediately returns ‘inaccessible’; an initially missing literal normally fails at glob first.”**

### F2 — Limits incorrectly routes every event to reload

Location: entry **line 137**: “calls the callback once per event … so every event kind … reaches reload()”.

Counterexample input: a well-formed `IN_Q_OVERFLOW` event (`wd = -1`) when all stored watch descriptors are valid nonnegative descriptors. `man7-inotify.7.html:315–316` explicitly says `wd` is -1 for overflow. `Hyprland-ConfigWatcher.cpp:100–107` instead says:

```cpp
const auto WD = std::ranges::find_if(m_watches, [wd = ev->wd](const auto& e) { return e.wd == wd; });
if (WD == m_watches.end())
    Log::logger->log(Log::ERR, "CConfigWatcher: got an event for wd {} which we don't have?!", ev->wd);
else
    m_watchCallback(SConfigWatchEvent{ .file = WD->file, });
```

Thus unmatched events log and do not invoke the callback. Malformed records also break out at lines 90–97. Conversely, because failed adds are stored with wd -1, overflow **can** spuriously match a failed-add entry; that is [INFERENCE] from lines 59–62 and 100–107, not a runtime result. Mask-agnostic dispatch is true only after descriptor matching.

Correction: **“For each well-formed event whose wd matches a stored entry, the handler calls the callback without filtering its mask, including IN_IGNORED; unmatched descriptors only log an error.”**

No overflow was generated and no Hyprland event was injected.

### F3 — refresh inference overlooks conditional/coalesced scheduling

Location: entry **line 26**, Chain step 7: “queues the refresh with doLater” and “watch list is therefore rebuilt after every reload()”.

Deciding pin `Hyprland-PropRefresher.cpp:31–40`:

```cpp
m_propsTripped |= prop;
if (!m_scheduled && g_pEventLoopManager) {
    m_scheduledRefreshSeq = g_pEventLoopManager->doLater(...);
    m_scheduled = true;
}
```

`refreshProp` updates the watcher at 148–149, then clears scheduled state and bits at 154–156. Input/control-flow counterexample: two `reload()` calls before the queued refresher executes yield one scheduled refresh, not a rebuild after each reload; without an event-loop manager the call only accumulates bits. These are [INFERENCE] traces of the pin, not executed Hyprland scenarios. The entry labels its conclusion inference, but that does not justify the unconditional “every”.

Correction: **“Reload requests the watcher refresh bit; when an event-loop manager exists, at most one pending refresh is queued, and its execution rebuilds from the then-current paths, potentially coalescing several reloads (inference; not observed).”**

### F4 — declaration prose states an unpinned argument interpretation as settled

Location: entry **lines 12 and 20**: “Bool, default false”. K01 itself acknowledges the default interpretation is outside the pinned declaration. `Hyprland-ConfigValues.cpp:492` proves `MS<Bool>(..., false, {.refresh = ...})`, but the pins do not provide the `MS`/Bool constructor contract establishing the third argument as the default. This is a support gap, not a claim that the actual default differs.

Correction: **“The Bool declaration supplies false as its third argument and REFRESH_CONFIG_WATCHER as its refresh field; interpreting that argument as the default requires the unpinned declaration contract.”**

## Required row table

Verdicts apply the requested **single pinned source-line** standard, not merely truth somewhere in the surrounding function/header. OVERREACH below can be factually correct across multiple cited locations. Full source line, not just the frozen substring, is considered; e.g. K01's line visibly includes `MS<Bool>`.

| row | verdict | pin lines | correction |
|---|---|---|---|
| K01 | OVERREACH (unpinned declaration-contract location) | ConfigValues.cpp:492: `MS<Bool>("misc:disable_autoreload", "If true, the config will not reload automatically on save.", false, {.refresh = Supplementary::REFRESH_CONFIG_WATCHER})`; line 1 only includes `ConfigValues.hpp`, not its contents. Bool/help/third argument are supported; the assertion that the default contract is in that header is not shown. | The Bool declaration supplies the stated help text and false as its third argument; the pinned line does not establish the argument's default-value semantics. |
| K02 | SUPPORTED | ConfigValues.cpp:492: `{.refresh = Supplementary::REFRESH_CONFIG_WATCHER}`. | — |
| K03 | SUPPORTED | ConfigWatcher.cpp:33: `static const auto PDISABLEAUTORELOAD = CConfigValue<Config::INTEGER>("misc:disable_autoreload");`; containing update body is 32–35. | —; “caches” describes the static CConfigValue object, not proof that its numeric value is frozen. |
| K04 | SUPPORTED | ConfigWatcher.cpp:34: `setWatchList(*PDISABLEAUTORELOAD ? std::vector<std::string>{} : Config::mgr()->getConfigPaths());`. | — |
| K05 | OVERREACH (context + explicitly labelled external inference) | ConfigWatcher.cpp:46: `inotify_rm_watch(m_inotifyFd.get(), watch.wd);`; per-entry iteration is line 45, clear is line 49; inotify duplicate/remove semantics are not on line 46. | This line invokes inotify_rm_watch with m_inotifyFd and watch.wd and discards its return value; per-entry iteration and duplicate-removal failure require the surrounding loop and inotify semantics. |
| E08 | OVERREACH (cross-pin expansion, not a false bit value) | PropRefresher.hpp:18: `REFRESH_CONFIG_WATCHER = (1 << 8),`; attachment/test are ConfigValues.cpp:492 and PropRefresher.cpp:148, not the quoted line. | This enum line defines REFRESH_CONFIG_WATCHER as bit 8; its option attachment and refresher test are separate cross-pin facts in K02 and K15. |
| E09 | OVERREACH (true across header, not the single line) | PropRefresher.hpp:21: `REFRESH_ALL = std::numeric_limits<std::underlying_type_t<ePropRefreshProp>>::max(),`; the needed `enum ePropRefreshProp : uint16_t` is line 9, and bit 8 is line 18. | REFRESH_ALL is assigned the underlying type's maximum on line 21; using uint16_t from line 9 implies all sixteen bits, including bit 8, are set (arithmetic inference). |

Summary: **3 SUPPORTED, 4 OVERREACH, 0 UNSUPPORTED** under the single-line rubric. K05/E08/E09 are contextual overreach rather than contradiction; E09 correctly discloses its earlier-line dependency. K01's header-location assertion was not fetched or promoted to established fact.

## Prose coverage and corrected-sentence disposition

Entry line numbers below refer exclusively to the scored revision. Grouped cells cover all clauses in that scoped line; “supported” means source-supported unless an explicit external observation boundary is described.

| section / entry lines | disposition and deciding evidence |
|---|---|
| Chain 1 / 20 | Bool/help/refresh supported by ConfigValues.cpp:492; default semantics gap F4. |
| Chain 2 / 21 | Static object and conditional list supported by ConfigWatcher.cpp:32–35; getConfigPaths body 2133–2135 supports return of m_configPaths. Actual CConfigValue dereference implementation is unpinned; no proof of frozen numeric-value caching. |
| Chain 3 / 22 | Masks, add attempts, canonical guard, stored link spelling supported by ConfigWatcher.cpp:45–73. “removes every old watch” should read “attempts to remove every stored entry's wd”, because failures are unchecked (also acknowledged elsewhere in entry). |
| Chain 4 / 23 | Registration/callback supported by EventLoopManager.cpp:70–73,127–128 and ConfigWatcher.cpp:80–111; the entry's preceding “finds each watch” context matters: callback only on a match. No event-name read in the entire function. |
| Chain 5–6 / 24–25 | Callback/reload/reset/parse/post-refresh calls supported by legacy ConfigManager.cpp:1077–1084,726–751,1070. |
| Chain 7 / 26 | Enum arithmetic supported across header:9,18,21 and explicitly labelled arithmetic; watcher guard supported at refresher:148–149; unconditional scheduling/rebuild wording F3. |
| Chain 8 / 27 | disable-autoreload substring guard and update supported by HyprCtl.cpp:1223–1224; reload call is the cited 1276. Legacy-only keyword applicability is disclosed in Limits/E04. |
| Chain 9 / 28 | Link versus canonical-target mask reading follows ConfigWatcher.cpp:55,60,65–70 plus cited inotify semantics; authors' intent appropriately disclaimed. Wave-1 observation is attributed, not treated as a compositor test here. |
| Path lifecycle / 33–35 | Direct constructor/reset/parse/handler/wrapper statements supported by legacy:485,630,731,755,764–786,359–369,614. “Nothing is patched incrementally” must retain the reload/verify scope: handleSource itself appends during runtime keyword parsing, as Limits acknowledges. File parsing internals remain the declared unpinned dependency. |
| handleSource / 38–42 | Bogus/glob early returns, iteration, regular append-before-parse, path save/restore, no local depth check, directory/nonregular skips supported by full legacy:1802–1855. Only-dangling error restriction is false: F1. Initially absent literal versus disappearing-after-glob distinction is missing. |
| Consequences / 45 | Append-before-recursion supported by legacy:1836–1840; across-source-line/file-order traversal is an **unlabelled inference requiring parseFile's ordering**, whose implementation the entry admits is outside round-56 pins. Correction: label depth-first/pre-order as inference conditional on synchronous, file-order parseFile processing. |
| Consequences / 46 | Corrected duplicates sentence distinguishes multiple m_watches entries from one kernel watch; supported by watcher:45–73 and inotify:85–92,298–302. Duplicate-removal failure is external/kernel inference (K05 marks it as such); older repeated-wd observation is attributed. No new duplicate-watch trial run here. |
| Consequences / 47–50 | Missing-before-glob path is excluded; link spellings retained; directory sources skipped; main path appended before verification; unchecked add is supported. Created-later conclusion is labelled inference. “No parent directory is ever watched” needs the ordinary-regular-main-config scope: an unconditional main path that is itself a directory can receive directoryMask (watcher:54–57). No filesystem invariant in the pinned watcher prevents that. |
| Consequences / 51 | No visited/depth guard in local handler; stack/heap growth and failure uncertainty explicitly labelled inference, not execution. Underlying parser recursion guard remains unpinned. |
| Path resolution / 54 | HOME replace and no lookup supported by MiscFunctions.cpp:61–83. Corrected null-string sentence cleanly distinguishes C++ precondition, prior libstdc++ observation and unknown Hyprland-build consequence. Caveat: getenv is static/first-use; “HOME unset” must mean unset at first tilde expansion, not a later environment change. |
| Path resolution / 55–60 | Absolute/relative/dot branches and textual currentDir supported by MiscFunctions.cpp:67–82, with nonempty absolute currentPath as the normal source-path context. No normalization call in the function. |
| Path resolution / 61 | Absence of RAW dollar expansion supported by entire absolutePath function. Round-46 hyprlang/version assertions are outside this row range and not independently rechecked; version-link uncertainty is explicitly disclosed. |
| Resolution base / 64–66 | Assign/restore/link-spelling reasoning supported by legacy:736,756,1825,1837–1840 plus absolutePath; relative nested-path conclusion is a cross-function inference, not explicitly labelled here. Correction: label that derivation inference, conditional on parseFile invoking the source handler synchronously. |
| Host paragraph / 68 | Historical capture/live-count assertions do not cite this seat's target rows and were not freshly verified; no host reads performed. Not promoted to fresh evidence. |
| Glob paragraph / 70 | Corrected glibc/C-locale/collation and dot-entry text is explicitly attributed to earlier observations and does not assert the running compositor's libc/locale. Round-56 pin legacy:1816 proves only flag selection; libc/locale observations were not repeated. |
| Limits / 133–135 | Source/runtime distinction and unpinned-declaration/provider assumptions appropriately disclosed; historical host fdinfo claims are outside this seat's authorized /proc scope and not reverified. |
| Limits / 136 | Invalid inotify-init handling, valid-FD event-loop guard, unchecked add and no dedicated overflow branch supported by watcher:21–26,59–62,80–111 and EventLoopManager:127–128. |
| Limits / 137 | Mask not inspected is true; all-events-to-reload is false: F2. Multiple matching records can produce multiple callbacks; no reload coalescing in this handler (do not confuse scheduled refresh coalescing in F3). |
| Limits / 138 | Corrected rename-over IN_IGNORED claim is attributed to kernel lab, not live Hyprland; mask-independent callback is supported only for matching wd (F2 qualification). Reload/list outcome is explicitly inference; stale-watch rm attempt supported by watcher:45–47. The named earlier rename lab was not rerun. |
| Limits / 139 | parseKeyword route/source branch and lack of watcher update in that branch supported by HyprCtl.cpp:1180–1227; handler invocation and later-update conclusion appropriately labelled inference. |
| Limits / 140–142 | Historical host records, model-only divergences and explicitly untraced full-reset/registration/verify tail do not claim fresh runtime proof. These are declared boundaries, not proof of untraced behavior. |

Five specifically requested corrections: **missing-target/inaccessible still has F1; duplicates is now properly distinguished; glob collation is properly observational/conditional; rename-over IN_IGNORED needs the matching-wd qualification in F2; HOME-unset libstdc++ consequence is properly observational with first-use caveat.**

## Commands, evidence, and null-result boundaries

LSP: attempted `read xd://lsp` before text exploration; returned **“No such tool: xd://lsp”**. No LSP server/device was available, so references/definition/diagnostics could not run. No grep output is offered as semantic proof; this audit used direct git-object function bodies.

Initial fixed-tree read:

```bash
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:corpus/knowledge/hyprland-config-autoreload-r56.md
```

Output included the corrected K01–K05/E08–E09 cells and all Chain/path/Limits sentences quoted above. Frozen contracts were read at the assignment's absolute paths using the read tool. Earlier `w2/R56W2RevProsePath.md` was read for attribution, not as an instruction or replacement verdict.

Exact reproducible evidence command (exit 0, stderr empty):

```bash
TMPDIR=/fast/scratch/hyaku/mado-r56/R56W3RevAuditA2A python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevAuditA2A/audit-evidence.py
```

The driver prints every exact `git -C <lane> show <rev>:<pin>` command, numbered surrounding function/enum bodies, target prose, and fresh glob-loop result. libc probe uses flags=0 on an absolute, non-tilde path; GLOB_TILDE is immaterial for that input. Evidence is from git objects at the specified revision, not working-tree pins. No archive/clone created.

Null results: full watcher function output from that command, ConfigWatcher.cpp:80–111, contains **no mask read or IN_Q_OVERFLOW-specific branch**; it does contain the wd-match guard, preventing a false negative claim about dispatch filtering. Full absolutePath:61–83 contains **no user lookup or realpath/normalization call**. These are bounded negative function reads, not whole-project absence claims. No claim of “no actionable finding” is made: F1–F4 remain recommendations.

Decisive scratch cleanup output:

```text
SCRATCH: removed /fast/scratch/hyaku/mado-r56/R56W3RevAuditA2A
EXIT: 0
```

## Residual risk / verification gaps

No Hyprland build/run/save/reload, C1 counter/harness, live host inspection, overflow injection, duplicate-removal trial, HOME-null trial, libc collation trial, or rename-over trial was performed by this seat. Prior attributed lab observations were inspected in the earlier prose report but not rerun. Native C++ status on the looping symlink was not separately compiled; generic error handling is established by the pin and fresh syscall behavior by the libc/stat probe. Default-value declaration contract, hyprlang parse order/version tie, and historical host fdinfo remain outside the pinned evidence verified here. No tool installed/upgraded; no PATH directory, service, host config or tracked lane file modified.

Deliverables (relative to lane):
- `.ufo/waves/round-56/w3/R56W3RevAuditA2A.md` — this report.
- `.ufo/waves/round-56/w3/R56W3RevAuditA2A/audit-evidence.py` — reproducible read-only pin/libc evidence driver (scratch-local symlink only, finally cleanup).
- `.ufo/waves/round-56/w3/R56W3RevAuditA2A/evidence.txt` — exact commands, full selected source/prose output, probe and exit receipt.

Self-evaluation: accuracy 4/5 (native C++ error reproduction not run); completeness 4/5 (historical host observations deliberately not reverified outside seat permissions); clarity 4/5 (strict single-line overreach is separated from factual contradiction); actionability 5/5 (input, pin branches and replacement sentences supplied); conciseness 4/5 (sentence coverage table is necessarily long). Overall 4.2/5. Highest-value improvement would be a separate authorized native-C++ ELOOP check, not more compositor testing. Would the user agree: the concrete residual F1 and guarded-dispatch F2 are directly checkable without changing frozen predicates.
