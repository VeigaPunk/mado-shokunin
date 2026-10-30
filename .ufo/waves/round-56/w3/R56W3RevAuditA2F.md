# R56W3RevAuditA2F — post-correction sentence-to-pin audit

## Scope and method

Attacked C1 entry `corpus/knowledge/hyprland-config-autoreload-r56.md` at **0f3a54361a9824484d0801679ceb1fd8ac7c32e1**, specifically H01–H03, E02–E04, Host reads, and their Chain/path-list/Limits prose, including the five named corrected sentences. Axes: proposition entailment; single-line traceability; honest host observations/inference; frozen-contract preservation. Read claims-frozen-v2.md, registration-v2.md and original registration.md before examining the entry. Read the actual entry diff from 28fc86ac2359ec27406d8a2c63bef82ea6e947ed to the assigned revision.

Exported the entry and pins **once** with read-only `git archive`; all numbered code evidence below is from that export, not the lane working tree. Read the complete ConfigWatcher.cpp (including both functions), complete dispatchKeyword function (1160–1258), complete handleSource (1802–1855), complete absolutePath (61–83), and complete captured host records. Pin shorthand: CW = `.ufo/waves/round-56/fetch/Hyprland-ConfigWatcher.cpp`; HC = same directory `Hyprland-HyprCtl.cpp`; LEG = `Hyprland-legacy-ConfigManager.cpp`; MAN = `man7-inotify.7.html`.

LSP unavailable: `read xd://lsp` returned `No such tool: xd://lsp`; consequently status, references, definition and diagnostics could not run. Text searches/function reads are fallback evidence, not semantic-server proof. No tools installed. No lane tracked file, git state, host configuration or compositor state modified.

## Findings, by severity

All substantive findings below **weaken the sourced/entailment claim**, not the frozen lexical predicate: registration-v2 explicitly excludes entailment from the counter. No frozen predicate, target or kill rule is changed or proposed for change.

### F1 — E02's “no later event can match” is contradicted by the pinned overflow event

**Severity: weakens the claim.** Entry line 122 adds an absolute assertion absent from the older E02. Counterexample input: `m_watches` contains a failed add entry `{wd=-1,file="missing.conf"}`, and the kernel supplies `{wd=-1,mask=IN_Q_OVERFLOW,len=0}`. MAN 315–316 explicitly says `IN_Q_OVERFLOW` has `wd` -1. CW 100 compares only `e.wd == wd`; CW 102–107 calls the callback on a match without checking the mask. The failed-add entry therefore **can** match the overflow event; LEG 1079–1082 then calls reload. This is a static consequence of the canonical code, not a claim that the running compositor overflowed.

Deciding quotes:
- CW 60: `.wd   = inotify_add_watch(m_inotifyFd.get(), path.c_str(), mask),`
- CW 100: `const auto WD = std::ranges::find_if(m_watches, [wd = ev->wd](const auto& e) { return e.wd == wd; });`
- CW 104–106: `else` / `m_watchCallback(SConfigWatchEvent{` / `.file = WD->file,`
- MAN 315–316: `IN_Q_OVERFLOW` / `Event queue overflowed (wd is -1 for this event).`

Correction: “The unchecked add result is stored in .wd even on failure; a -1 entry is not a valid file watch, but the handler's descriptor-only comparison can match it to an IN_Q_OVERFLOW event.”

### F2 — the corrected inaccessible sentence still falsely says “only” dangling symlinks

**Severity: weakens the claim.** Entry line 41 says status failure for a glob match “happens only for a dangling symlink.” A self-referential symlink is not dangling: it produces **ELOOP**, not ENOENT. A new isolated glibc probe returned the loop path as a successful GLOB_TILDE match, then following status failed with ELOOP. The same status failure branch (LEG 1828–1833) does not restrict the error to ENOENT. Races and permission changes are further possible failures, but are not needed for this counterexample.

Exact new probe output:
```
glob GLOB_TILDE missing.conf: rc=3 matches=0
glob GLOB_TILDE loop.conf: rc=0 matches=1
  match=loop.conf; lstat=symlink:True
  status follows symlink: errno=40 ELOOP
```
The status observation above is `os.stat` on the glibc-returned match, not an execution of Hyprland or C++ `std::filesystem::status`; the mapped C++ branch is a source-reading inference. Deciding code is `auto file_status = std::filesystem::status(value, ec);` (1828) followed by `if (ec)` / return `inaccessible` (1830–1833), with no error-class restriction.

Correction: “If status fails for a glob match—for example a dangling or looping symlink, or a path that becomes inaccessible after glob—the function returns inaccessible immediately; a literal target already absent at glob time normally fails at the preceding no-match return.”

### F3 — Limits overstates callback-per-event and misreports the cited touching-write receipt

**Severity: weakens the claim.** Entry line 137 says the callback runs “once per event” and “every event kind ... reaches reload()”; CW 90–98 rejects malformed events and CW 102–103 **logs rather than calling back for an unmatched descriptor**. Concrete valid input: an overflow event with wd=-1 and only successful positive-wd watches. It is read, finds no watch, and logs; it does not reload. IN_IGNORED reaches the callback only while its descriptor remains represented. A mask-insensitive handler is not an unconditional callback.

The same sentence says the wave-1 lab saw one event for a “touching write.” Its cited canonical `w1/R56ScoutInotifyLab/raw-output.txt` explicitly records:
```
=== [a5] regular file + FILE_MASK: touch (utimensat) ===
  after touch: NONE
=== [c6] directory + DIR_MASK: touch of an existing file in the dir ===
  after touch: NONE
```
If “touching write” meant some different write operation, that operation is not identified by the cited receipt; the actual touch cases say NONE.

Correction: “Each well-formed event whose descriptor matches a recorded watch invokes the callback regardless of mask, including matched IN_IGNORED events; the lab observed IN_CLOSE_WRITE for ordinary/truncating writes but no event for touch(utimensat).”

### F4 — two extra rows still exceed their single-line anchors

**Severity: weakens single-line traceability, not a false whole-function account.** E03's negative assertion about ignoring the event name requires CW 80–111; E04's legacy-only guard requires HC 1162–1165. Neither is established by the quoted line alone. Both are OVERREACH under the assignment's expressly single-line verdict rule; the surrounding functions support them. Corrections in the table retain only what the anchor shows, leaving the broader supported facts in prose with multi-line citations.

### F5 — Chain step 3 calls unchecked removal attempts successful removals

**Severity: cosmetic precision.** Entry line 22 says setWatchList “removes every old watch.” CW 45–47 merely calls inotify_rm_watch unchecked; the corrected duplicate-watch paragraph itself explains the second removal fails, and a kernel-removed IN_IGNORED watch is already absent. Correction: “setWatchList attempts to remove every recorded watch descriptor, ignores removal failures, then clears its records.”

## Required row table

Verdicts are for the **whole proposition cell**, not just its first clause. SUPPORTED means the cited pin line shows it; OVERREACH means surrounding code is required; UNSUPPORTED means a clause is contradicted.

| row | verdict | pin lines | correction |
|---|---|---|---|
| H01 | SUPPORTED | host-getoption.json:1: `{"option": "misc:disable_autoreload", "int": 0, "set": false }`; live read agrees. | — |
| H02 | SUPPORTED | host-sources.txt:10: `source = ~/.config/omarchy/current/theme/hyprland.conf`; full captured list read, and live main-file line 13 agrees. | — |
| H03 | SUPPORTED | host-version.json:3: `"commit": "efb50993780079460b0cbed1363e2166a2de1d9f",`; complete version record read and live record agrees. | — |
| E02 | UNSUPPORTED | CW:59–62 stores the unchecked add result; CW:100 compares only wd; CW:102–107 invokes callback when matched; MAN:315–316 specifies overflow wd=-1, contradicting “no later event can match.” | This line stores inotify_add_watch's return value unchecked in the recorded watch's .wd field. |
| E03 | OVERREACH | CW:106 `.file = WD->file,` shows the assignment; matching requires CW:100–104, callback context CW:105–107, and “event name ignored” a negative read of CW:80–111. | This line copies WD->file into the callback event's .file field. |
| E04 | OVERREACH | HC:1190 `std::string retval = mgr->parseKeyword(COMMAND, VALUE);` shows the call; legacy-only restriction is HC:1162–1165, and input parsing HC:1167–1186. | This line calls mgr->parseKeyword with COMMAND and VALUE and stores its returned string in retval. |

## Prose coverage and five correction checks

| location / sentence group | result and evidence |
|---|---|
| Chain step 3: removal, primary add, canonical add, stored link path | F5 for successful-removal wording; otherwise CW 45–73 supports attempts, selected masks, second canonical add, and `.file = path` at 70. |
| Chain step 4: wd matching, stored path, kernel name unread | Whole-function reading supports it for matched events; CW 100–107. The negative claim about name is true over CW 80–111, not solely E03's anchor. No `ev->name` read appears. |
| Path-list main-path paragraph citing E02 | True about storing an unchecked result (LEG 776–781; CW 52–73), but does not rescue E02's stronger no-match assertion. No claim made here that a missing main path remains missing after verifyConfigExists. |
| Host reads paragraph and Limits Host records | All named counts/line numbers and final-component lstat types agree: 18 directives, Omarchy defaults on live lines 4–12, theme on 13, nested envs source on 3, gum.env.conf regular file (not final-component symlink). H captures are correctly limited to capture-time values. |
| Limits parser-selection assumption | HC 1162–1165 supports legacy restriction; the entry explicitly disclaims pinned selection logic and labels its legacy assumption. |
| Limits failure paths | CW 21–26, EventLoopManager 127–128 support invalid-FD handling; CW 60 has unchecked add; CW 80–111 has no overflow-mask branch. Supported. |
| Limits reload-per-event | F3: missing descriptor-match qualification and contradicted touch receipt. No coalescing appears in CW 80–111, so the qualified possibility of multiple reloads is reasonable static inference, not a host observation. |
| Limits runtime source via E04 | HC 1190 reaches parseKeyword for a valid legacy keyword request; LEG 1089–1090 calls parseDynamic; entry labels the unpinned handler-dispatch bridge as inference. HC full dispatchKeyword has no watcher update for COMMAND==source; eventual-watching conclusion is expressly labelled inference. Supported as qualified. |
| **Corrected missing-target/inaccessible sentence** | Still false in its new “only dangling” clause: F2. Missing literal no-match part is confirmed by new rc=3 observation. |
| **Corrected duplicate watches sentence** | Improved and supported: LEG 1836 plus CW 52–73 records duplicates; MAN 85–92, 293–302 establish new-vs-existing watch/mask modification. Committed prior receipt records the same wd three times and second removal EINVAL. This was not re-executed on the host. |
| **Corrected glob collation sentence** | Appropriately distinguishes glibc observation from unpinned Hyprland libc/locale and the tool's declared divergence; LEG 1816 has GLOB_TILDE without GLOB_NOSORT. Canonical prior receipts distinguish C/C.utf8 bytewise from en_US collation and show dot-star returning dot/dot-dot. Not rerun here. |
| **Corrected rename-over IN_IGNORED sentence** | Canonical lab a4 explicitly shows IN_IGNORED and no follow-up event; MAN 307–310 supports removed-watch meaning. Reload reachability is a **static inference conditional on wd still matching**, not an observed Hyprland reload; label that condition on the first reachability clause as well as the later path-list clause. The lab's moved-away a6 follow-up writes the recreated original path, not the moved inode, so “still fires on a later write to that inode” is an inode-semantics inference, not demonstrated by a6's output. |
| **Corrected HOME-unset/libstdc++ sentence** | Correctly separates string precondition violation, the prior libstdc++ observation, and unknown Hyprland-build result; MiscFunctions 64–66 and complete LEG 1802–1855 support no local catch. The cited prior committed receipt prints `threw: basic_string: construction from null is not valid`. Not rerun here. The static ENVHOME is read on first initialization, so this concerns HOME unset at that initialization, not an assertion that later environment changes refresh it. |

For the renamed-file inference wording, suggested single sentence: “The lab observed rename-over IN_IGNORED; if its wd still matches a recorded entry, the mask-insensitive handler would reload (source inference), whereas later writes to a moved inode are predicted by inode-based watch semantics rather than demonstrated by that lab's recreated-path follow-up.”

## Commands, evidence and null checks

Exact canonical extraction:
```
mkdir -p /fast/scratch/hyaku/mado-r56/R56W3RevAuditA2F/tree /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3RevAuditA2F
git -C /home/vgpnk/Projects/shokunin/mado-shokunin archive 0f3a54361a9824484d0801679ceb1fd8ac7c32e1 corpus/knowledge/hyprland-config-autoreload-r56.md .ufo/waves/round-56/fetch/ | tar -x -C /fast/scratch/hyaku/mado-r56/R56W3RevAuditA2F/tree
```
Exit 0, no output. Actual change inspection:
```
git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff 28fc86ac2359ec27406d8a2c63bef82ea6e947ed 0f3a54361a9824484d0801679ceb1fd8ac7c32e1 -- corpus/knowledge/hyprland-config-autoreload-r56.md
```
Exit 0; 36 insertions, 35 deletions. The new E02 no-later-event clause and the updated inaccessible clause were reviewed, not assumed repaired because their predecessors changed.

Host null checks: `hyprctl getoption misc:disable_autoreload -j`, `hyprctl version -j`, `stat -c '%F %n' /home/vgpnk/.config/hypr/hyprland.conf /home/vgpnk/.config/omarchy/current/theme/gum.env.conf`, and the isolated `python3 -I` probe all exited 0. Decisive output in **receipts.txt**: option 0; commit matches H03; both named final components regular; 18 source-prefix lines at 4–13,16–20,23,29,32; nested envs line 3 matches. No host-content/count/type discrepancy found by these commands. Shell `grep -c '^source'` and `sed` version-line projection were not run: specialized grep supplied matches; Python counted them; full JSON was read instead of shell paging. All semantic equivalents were exercised, with this literal-command deviation disclosed.

## Deliverables, residual risks and gaps

- Report: `.ufo/waves/round-56/w3/R56W3RevAuditA2F.md`.
- Receipt: `.ufo/waves/round-56/w3/R56W3RevAuditA2F/receipts.txt`.
- Reproducer: `.ufo/waves/round-56/w3/R56W3RevAuditA2F/probe.py` (fixed seat scratch path, creates and removes its own child fixture).
- Entire seat scratch removed before yield. No fixture git repository or commit was created.

Not run: C1/C2/C3 counters/harnesses (outside this seat's semantic audit); actual Hyprland save/reload/keyword; compositor overflow injection; C++ build or direct C++ filesystem probe; new libc-collation/null-string/inotify lab reruns; `/proc` or journal reads (not authorized for this seat). Overflow dispatch findings are canonical-code deductions, not an executed compositor experiment. Historical libc and kernel observations were checked against committed receipts, not freshly reproduced except the missing/loop glob probe. No resume, same-identity rerouting, saturation or runtime-admission changes exist in this scoped entry; no claim about those unrelated contracts is made.

Frozen predicate status is **not re-scored**. Recommendation: correct the false prose and narrow extra-row single-line propositions without changing frozen definitions; the findings do not authorize integration or admission. No tracked edit made.

Self-evaluation (1–5): accuracy 4 (overflow path static, not injected); completeness 4 (historical libc/kernel probes read but not rerun); clarity 4 (single-line vs whole-function support explicitly separated); actionability 5 (counterexamples, exact locations and replacement sentences supplied); conciseness 4 (required sentence coverage makes report longer). Mean 4.2. Highest-value improvement would be an isolated direct C++ status probe, not touching Hyprland; current report explicitly distinguishes the Python syscall observation from the C++ inference.
