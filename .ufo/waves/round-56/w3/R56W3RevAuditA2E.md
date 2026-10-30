# R56W3RevAuditA2E — post-correction sentence-to-pin audit

## Scope, axes, method

Attacked: **C1 corrected K25–K30 and E01**, their citing Chain/path-resolution prose, and the five specifically named corrections in the path-list/Glob/Limits sections. Revision: `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`, not the working tree. Axes: single-line entailment; truth against the surrounding function; inference/observation boundaries; reproducible evidence. No predicates, tracked files, host state or git state changed. This is an author-side review recommendation, not independent admission or a changed frozen judgment.

Read claims-frozen-v2.md and registration-v2.md first, then registration.md §C1. The counter's lexical predicate does not prove entailment (registration-v2:82–84); none of the findings below demonstrates failure of that mechanical predicate. No blocking-the-frozen-claim finding. Findings weaken the sourced narrative unless marked cosmetic. Changes to frozen predicates would be ROUTED, not applied.

LSP unavailable: `read xd://lsp` returned `No such tool: xd://lsp`; no server/status/references/definition/diagnostics route was mounted. Thus this is a git-object/manual-function audit, not semantic-reference proof. Literal searches below are only supplemental. No other runtime invoked.

## Row verdicts

Pin names below mean `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/fetch/<name>` **as git blobs at the revision above**. Entry line numbers are at that revision. All seven surrounding contexts were read, including complete `absolutePath` (61–83), `dispatchKeyword` (1160–1258), `reloadRequest` (1260–1279), and the inotify event/flag descriptions surrounding both man-page anchors.

| row | verdict | pin lines | correction |
|---|---|---|---|
| K25 | SUPPORTED | MiscFunctions.cpp:65: `static const char* const ENVHOME = getenv("HOME");`; context 64–66 | None; static initialization captures the pointer on first execution of this branch. |
| K26 | SUPPORTED | MiscFunctions.cpp:68: `auto currentDir = currentPath.substr(0, currentPath.find_last_of('/'));`; context 61–83 | None; this is text slicing, not canonicalization. |
| K27 | OVERREACH | HyprCtl.cpp:1223: `if (COMMAND.contains("misc:disable_autoreload"))`; **1224**: `Config::watcher()->update();` | “This guard tests whether COMMAND contains the misc:disable_autoreload substring.” |
| K28 | SUPPORTED | HyprCtl.cpp:1276: `Config::mgr()->reload();`; enclosing handler 1260–1279, non-full-reset branch | None. |
| K29 | SUPPORTED | man7-inotify.7.html:185–186: `IN_CLOSE_WRITE` / `File opened for writing was closed.`; event-mask context 168–189 | None; opening for writing need not imply data was changed. |
| K30 | SUPPORTED | man7-inotify.7.html:258–262, especially 262: `Don't dereference <i>pathname</i> if it is a symbolic link.` | None. |
| E01 | UNSUPPORTED as literally worded; also exceeds its quoted line | MiscFunctions.cpp:**64**: `if (value[0] == '~') {`; **65**: `static const char* const ENVHOME = getenv("HOME");`; **66**: `value.replace(0, 1, std::string(ENVHOME));`; complete function 61–83 contains no user-lookup operation | “This call replaces one byte at offset zero of value with std::string(ENVHOME).” |

**K27 (entry:104), weakens:** the proposition concedes that its update-call clause is not shown by the quoted line; that concession does not make it single-line-supported under this assignment. The behavior is supported by 1223–1224 together. Keep that behavior in the prose, with its two-line citation.

**E01 (entry:121), cosmetic locator defect plus grounding overreach:** “the tilde tested one line earlier” is false: the test is two lines earlier; line 65 initializes ENVHOME. The no-user-lookup and `~user` consequences are correct function-level readings, explicitly acknowledged in the row, but are not shown by the quote alone. The correction above removes both issues without changing any frozen anchor.

## Findings by severity

### Weakens the sourced claim

**F1 — “only for a dangling symlink” remains false after correction (entry:40).**

Input/counterexample [INFERENCE, not executed]: `source = /abs/tree/*.conf`; glob returns ordinary regular `/abs/tree/a.conf`, then another process unlinks that file before the loop's `status` call. The source performs separate operations with no atomicity or revalidation guarantee:

- legacy ConfigManager.cpp:1816: `glob(absolutePath(rawpath, m_configCurrentPath).c_str(), GLOB_TILDE, nullptr, glob_buf.get())`
- :1824–1828: iterate saved matches, then `std::filesystem::status(value, ec)`.
- :1830–1832: **any** `ec` returns `"source= file " + value + " is inaccessible!"`.

A non-symlink glob match can therefore fail status. Permission changes between those operations are another possible cause. The normal initially absent literal case correctly returns NOMATCH; it does not prove exclusivity of dangling symlinks after a successful glob.

Correction: **“If status fails—for example for a dangling symlink or a match removed after globbing—the function returns inaccessible immediately, before appending that entry.”** Also qualify “A missing literal target never gets here” as a target already absent when glob is evaluated.

**F2 — callback-on-every-event overstates the actual guard (entry:137).**

The sentence says `onInotifyEvent` “calls the callback once per event” and “every event kind ... reaches reload()”. ConfigWatcher.cpp:100 searches current `m_watches` by `ev->wd`; :102–103 only logs on no match, and only :104–107 invokes the callback. Input [INFERENCE, not injected]: an `IN_Q_OVERFLOW` event with wd=-1 while all current watch descriptors are successful nonnegative registrations; man7-inotify.7.html:315–316 explicitly specifies `wd is -1`. Such an event cannot reach the callback. An IN_IGNORED queued for a watch already removed from `m_watches` is likewise not guaranteed to match. The absence of a mask test is true but does not eliminate the wd guard.

Correction: **“For each well-formed event whose wd matches a current m_watches entry, the handler invokes the callback without testing the event mask, including IN_IGNORED; unmatched descriptors are logged instead.”** The rename-over reload prediction at entry:138 should explicitly retain this matched-watch condition and be labelled source-derived inference, rather than an observed Hyprland result.

**F3 — the claimed touching-write lab observation is not supported by the cited lab (entry:137).**

Exact text: “the wave-1 lab saw one event per save for an in-place, truncating or touching write”. The cited committed lab instead records:

- `.ufo/waves/round-56/w1/R56ScoutInotifyLab/raw-output.txt:32–35`: `=== [a5] ... touch (utimensat) ===` / `after touch: NONE`.
- same file:93–96: directory-mask touch likewise `after touch: NONE`.
- `.ufo/waves/round-56/w1/R56ScoutInotifyLab.md:101`: “a mtime-only touch is” followed by its distinction from close-write cases.

If “touching write” means some different operation opening a writable descriptor, no such observation is identified by this sentence. K29 does not equate utimensat with close-write.

Correction: **“The wave-1 lab observed IN_CLOSE_WRITE for in-place and truncating writes, but no event for an mtime-only touch with these masks.”**

**F4 — K27 single-line entailment:** described in the row table; function behavior is correct, single-line grounding is not.

### Cosmetic

**F5 — E01's test is two lines earlier, not one:** described in the row table. Its function-level explanation also exceeds its quote under the requested audit rubric.

## Prose coverage and corrected-sentence disposition

This table covers the citing sentences in this seat's range; neighboring claims about K01–K24/E02–E09 are context, not a replacement audit of the other seats' assigned rows.

| Entry location / sentence group | Disposition |
|---|---|
| Chain:27 keyword immediate update and ordinary hyprctl reload | Supported by HyprCtl.cpp:1160–1258 and 1260–1279; legacy-only guard at 1162–1163 is stated in Limits:135. `contains`, not equality, is the actual keyword test. Command registration at 2028 binds reloadRequest. Full-reset is honestly excepted at :142. |
| Chain:28 close-write definition; no-dereference definition | SUPPORTED by man:185–186 and 258–262. |
| Chain:28 symlink link/target coverage; prior lab observation; author intent unavailable | Function-level synthesis supported by ConfigWatcher.cpp:55–70; lab raw:44–49 reports only canonical-watch IN_CLOSE_WRITE on write-through. Design-intent limitation is honest. This is source/lab synthesis, not a host reload observation. |
| Path-list:40 corrected inaccessible/missing-target sentences | F1: normal initially missing target correction is useful, but the new “only” excludes TOCTOU failures without basis. |
| Path-list:46 corrected duplicate-watch sentences | Correct distinction: repeated m_watches entries versus one kernel watch for the same inode. Watcher:45–73 and man:85–92, 293–302 support it; prior receipts show wd=1 repeated and second removal EINVAL. These describe successful same-inode adds, not a guarantee that every add succeeds. |
| Path-resolution:54 first-byte replacement; ~/x and ~user/x examples; no lookup/no inserted slash | Correct function-level reading of Misc:64–66 and complete 61–83, with a valid HOME string. E01's separate locator mistake remains. |
| Path-resolution:54 GLOB_TILDE interaction | Correct for the normal absolute HOME value: replacement precedes glob (legacy:1816). This is code-derived, not a runtime probe. |
| Path-resolution:54 HOME-unset correction and build limitation | Null construction/precondition and uncaught local path are consistent with Misc:65–66 and legacy:1802–1855. The libstdc++ observation is explicitly attributed, and the Hyprland-build gap is preserved. Prior RECEIPTS:26–28 says `threw: basic_string: construction from null is not valid`. Precisely, this concerns HOME at first initialization of the static; changing HOME after that does not re-run getenv. No fresh libc++/libstdc++ test was run here. |
| Path-resolution:55–60 leading slash, ./, ../, dot names, bare names, curdir slicing and no normalization | Supported by complete Misc:61–83; no extra defect found. Bare `..` takes the fallback branch. Assumes the caller's nonempty, valid path context. |
| Resolution-base:64–66 main/nested/link base | Consistent with legacy:736,756,1825,1837–1840 and Misc:68–79. These are source-derived consequences; main-path absoluteness/provider and parseFile internals remain outside round-56 pins as Limits says. |
| Glob:70 corrected collation and dot-match paragraph | `GLOB_TILDE` only at legacy:1816 means no GLOB_NOSORT. Actual collation/dot behavior is attributed to glibc observations, not pinned Hyprland's libc/locale. Prior RECEIPTS:6–12 supports bytewise C order, different en_US order, dot-star including dot/dot-dot. No new run; build uncertainty correctly retained. |
| Limits:135 relevant legacy premise and external-library gap | Appropriately separates function pins from unpinned declarations/build tie. |
| Limits:137 mask-independent callbacks and reported write cases | F2 and F3. No event-mask read is true; callback-per-event and touching-write evidence are overstatements. |
| Limits:138 corrected rename-over vs move-away sentences | Kernel-plane correction supported: raw lab:24–30 says rename-over => IN_IGNORED then no follow-up event; man:225–228 inode semantics; prior lab report:88 says a write to moved inode produces IN_CLOSE_WRITE. Claimed Hyprland reload remains inference and must respect F2's wd condition. Rebuild effects are explicitly labelled inference, not host observation. |
| Limits:139 runtime source, append and lack of direct watcher update | Dispatch branch 1194–1208 and 1223–1224 supports no direct update for COMMAND=source; parseDynamic handler routing and eventual-watch statement are explicitly labelled inference. Other indirect refresh behavior is not established by this branch alone. |
| Limits:141 tool-divergence list; :142 untraced full-reset/registration | Tool differences are explicitly not entry facts. Full-reset exclusion is honest; registration was read here at 2028. No new defect. |

## Exact commands and decisive output

Primary reproducible command actually run (exit 0):

```sh
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevAuditA2E/read-pins.py
```

The reader exclusively obtains source bytes with:

```sh
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:.ufo/waves/round-56/fetch/Hyprland-MiscFunctions.cpp
```

and the identical argv template for Hyprland-HyprCtl.cpp, Hyprland-ConfigWatcher.cpp, Hyprland-legacy-ConfigManager.cpp and man7-inotify.7.html. It prints numbered selected ranges and target-entry lines from the same revision. Decisive output is quoted above; pin SHA256 output:

```text
Hyprland-MiscFunctions.cpp 065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9
Hyprland-HyprCtl.cpp 798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa
Hyprland-ConfigWatcher.cpp 8383b8abf43159986bc4127ad7a4416fbf1c3527bf388fa1ce052c28c40d516c
Hyprland-legacy-ConfigManager.cpp 9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b
man7-inotify.7.html 79f5ab18e2fc423631cf4949ef82ca1384844353ea11a4dba42e1a77e8fdd8fd
LITERAL_SEARCH ev->mask: NO HITS
LITERAL_SEARCH ev->name: NO HITS
LITERAL_SEARCH IN_Q_OVERFLOW: NO HITS
LITERAL_SEARCH absolutePath getpwnam: NO HITS
LITERAL_SEARCH absolutePath getpwuid: NO HITS
LITERAL_SEARCH absolutePath realpath: NO HITS
```

These null searches were supplementary to complete body reads, not semantic absence proofs. Prior evidence was read with the same `git -C ... show REV:path` command for `.ufo/waves/round-56/w2/R56W2RevProsePath.md`, `w2/R56W2RevProseLimits.md`, `w2/R56W2RevProsePath/RECEIPTS.txt`, `w1/R56ScoutInotifyLab.md` and `w1/R56ScoutInotifyLab/raw-output.txt`; outputs quoted in F3 and the coverage table are historical receipts, not fresh observations.

## Residual risks / checks not run

- No compositor execution, config save, reload, keyword, /proc scan, host service change, tool install, build, counter/harness run or new libc experiment. No claim that this seat reverified the numeric at-final receipt. No canonical-runtime/resume/saturation implementation exists within this assigned documentation slice; those general review axes were not exercised.
- F1 and F2 counterexamples are static source-derived inputs/event timelines, not dynamic reproductions. Host build/libc tie, current HOME behavior, kernel behavior on other builds and indirect runtime-source refresh routes remain unverified.
- Host-capture prose and round-46 hyprlang version claims are outside these assigned seven rows; historical receipt attribution was checked where needed for the five named corrections, not independently recreated.
- Scratch was unnecessary: no clone, fixture, temporary file or scratch directory created, hence nothing left to remove. Only the required report and its reader were written in this seat's allowed deliverable paths.

Deliverables (absolute):
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevAuditA2E.md`
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevAuditA2E/read-pins.py`

Self-evaluation: accuracy 4/5 (counterexamples static, honestly labelled); completeness 4/5 (seven rows and named corrections covered, no fresh libc/kernel experiment); clarity 4/5 (separate row/prose criteria); actionability 5/5 (line-specific one-sentence corrections); conciseness 4/5 (coverage table adds length required for audit). Overall 4.2/5. Best improvement: a separately authorized fixture reproduction of the stat race; no source edit proposed here.
