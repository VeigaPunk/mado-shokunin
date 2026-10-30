# R56W3RevAuditA2C — post-correction sentence-to-pin audit

Attacked: C1 entry K13–K18 and their event-loop/refresher/callback prose, including the five named corrected sentences. Revision: `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`, not the working tree. Axes: single-line entailment, surrounding-function correctness, inference/observation honesty, frozen-contract preservation. No entry, predicate, counter or tracked file edited. All findings below are recommendations, not admission decisions.

## Findings, by severity

All substantive findings **weaken the sourced-content claim**; none demonstrates failure of the frozen lexical C1 predicate. Do not alter that predicate to accommodate these findings; any predicate change is ROUTED to round 57.

### F1 — weakens the claim: the lab did not see a write-close event for touch

Entry `corpus/knowledge/hyprland-config-autoreload-r56.md:137` says the wave-1 lab saw one event per save for an “in-place, truncating or touching write.” The cited canonical `.ufo/waves/round-56/w1/R56ScoutInotifyLab/raw-output.txt` explicitly distinguishes these inputs:

```text
=== [a1] regular file + FILE_MASK: in-place write (open/append/close) ===
    [file-watch] IN_CLOSE_WRITE
=== [a2] regular file + FILE_MASK: truncate-write (open 'wb' = O_TRUNC) ===
    [file-watch] IN_CLOSE_WRITE
=== [a5] regular file + FILE_MASK: touch (utimensat) ===
  after touch: NONE
```

Input showing the defect: the cited lab's a5 `touch (utimensat)` case, using FILE_MASK=0x2000008. This is an existing receipt, not a new host experiment.

Correction: “The lab saw one IN_CLOSE_WRITE for an in-place or truncating write, but no event for touch (utimensat), on kernel 7.2.11.”

### F2 — weakens the claim: no mask filter does not mean every event reaches reload

Entry line 137 says `onInotifyEvent` calls the callback once per event, “so every event kind, including ... IN_IGNORED, reaches reload().” The deciding pin is `Hyprland-ConfigWatcher.cpp:100-107`:

```cpp
const auto WD = std::ranges::find_if(m_watches, [wd = ev->wd](const auto& e) { return e.wd == wd; });
if (WD == m_watches.end())
    Log::logger->log(Log::ERR, "CConfigWatcher: got an event for wd {} which we don't have?!", ev->wd);
else
    m_watchCallback(SConfigWatchEvent{
        .file = WD->file,
    });
```

Input showing the distinction: a well-formed event whose `wd` is not in `m_watches`; it takes the log-only branch, not the callback. An IN_IGNORED queued by removing an old watch during `setWatchList` can be such an event after the old list is cleared (lines 45–49). This latter sequence is source inference, not a newly observed runtime event.

Correction: “Each well-formed event whose wd still matches an m_watches entry invokes the callback regardless of mask, including IN_IGNORED; unmatched events only log an error.”

The rename-over sentence at line 138 should retain the same qualification: a matching IN_IGNORED invokes the callback; absence of a mask filter alone is not sufficient.

### F3 — weakens the claim: corrected inaccessible sentence excludes real error paths

Entry line 40 now says status failure for a glob result happens “only for a dangling symlink” and a missing literal target “never gets here.” The prior P13 correction was copied too strongly. Pin `Hyprland-legacy-ConfigManager.cpp:1824-1833` has two distinct operations and no protection between them:

```cpp
for (size_t i = 0; i < glob_buf->gl_pathc; i++) {
    auto value = absolutePath(glob_buf->gl_pathv[i], m_configCurrentPath);
    std::error_code ec;
    auto file_status = std::filesystem::status(value, ec);
    if (ec) {
        ...
        return "source= file " + value + " is inaccessible!";
    }
```

Counterexample input/state sequence [INFERENCE]: a regular literal target exists when glob returns it, then is removed before status; the returned pathname is missing at status and takes the inaccessible return without being a dangling symlink. Permission changes and other status errors are also not excluded by this function. No race experiment was run.

Correction: “A target absent when glob runs normally yields no match, while any subsequent status error—including a dangling symlink or a path disappearing after glob—returns inaccessible before that entry is appended.”

### F4 — weakens the claim: refresh scheduling and list rebuilding are conditional

Entry line 26 says scheduleRefresh “queues the refresh with doLater” and therefore the watch list is rebuilt “after every reload() from ... m_configPaths.” Pin `Hyprland-PropRefresher.cpp:31-40`:

```cpp
m_propsTripped |= prop;
if (!m_scheduled && g_pEventLoopManager) {
    m_scheduledRefreshSeq = g_pEventLoopManager->doLater(...);
    m_scheduled = true;
}
```

Pin `Hyprland-ConfigWatcher.cpp:33-34`:

```cpp
static const auto PDISABLEAUTORELOAD = CConfigValue<Config::INTEGER>("misc:disable_autoreload");
setWatchList(*PDISABLEAUTORELOAD ? std::vector<std::string>{} : Config::mgr()->getConfigPaths());
```

Inputs/states showing the distinctions: `g_pEventLoopManager == nullptr` queues nothing at this call; `m_scheduled == true` merges reasons into an existing refresh; `misc:disable_autoreload != 0` rebuilds an empty list, not the config-path list. The source does not prove one distinct list rebuild per reload. The existing “inference” label is good but does not cure the overstatement.

Correction: “A completed reload requests REFRESH_ALL; a queued or newly schedulable refresh then updates watches, clearing them when disable_autoreload is non-zero and otherwise rebuilding them from the then-current config paths (source inference, not observed).”

### F5 — weakens the claim: K14 and K16 exceed their one-line anchors

See the row table below. K14's own-descriptor claim requires another pin/function; K16's callee behavior is outside its quoted line and omits the disabled branch. Their first clauses are supported, but a conjunction is not single-line supported merely because one clause is.

### F6 — cosmetic scope qualifications in the path-list prose

- Entry line 46 says setWatchList records “one m_watches entry per list entry (52–73).” Lines 59–62 append the primary entry and 67–71 append another for a symlink. The ordinary repeated-regular-file example and the corrected same-inode/same-wd distinction are sound. Correction: “setWatchList records a primary m_watches entry per path, plus a canonical-target entry for qualifying symlinks, so repeated regular-file paths produce repeated entries rather than distinct kernel watches.”
- Entry line 47 says “no parent directory is ever watched.” For the ordinary regular-file main config and regular-file source paths this is the intended inference, but `resetHLConfig` adds the main path unconditionally (legacy 779), and ConfigWatcher 54–57 explicitly supports directory watches. Input/state counterexample [INFERENCE]: the main config path is itself a directory containing the missing target. Correction: “For a regular-file main config and regular-file sources, the watcher adds no containing-directory watch to detect a missing source being created later.”

## Required K13–K18 verdict table

“Pin lines” below refer to the canonical `.ufo/waves/round-56/fetch/` files; complete reviewed bodies are preserved in the deliverable directory. SUPPORTED means the whole numbered source line supports the proposition, not merely that a frozen substring shares identifiers. Surrounding functions were read, not just quote matches.

| row | verdict | pin lines | correction |
|---|---|---|---|
| K13 | SUPPORTED | EventLoopManager.cpp:128: `wl_event_loop_add_fd(m_wayland.loop, FD.get(), WL_EVENT_READABLE, configWatcherWrite, nullptr)`; full enterLoop 124–140 confirms FD validity guard at 127. | — |
| K14 | OVERREACH | EventLoopManager.cpp:71: `Config::watcher()->onInotifyEvent();` shows the no-argument invocation; callback 70–73 does not use its fd/mask/data arguments, but the own-descriptor read occurs in **ConfigWatcher.cpp:83**: `read(m_inotifyFd.get(), buffer.data(), buffer.size())`, not the quoted line/function. | “This line calls onInotifyEvent on the watcher returned by Config::watcher(), with no arguments.” |
| K15 | SUPPORTED | PropRefresher.cpp:148: `if (m_propsTripped & REFRESH_CONFIG_WATCHER)`; refreshProp body 55–159 confirms the immediately guarded update. | — |
| K16 | OVERREACH | PropRefresher.cpp:149: `Config::watcher()->update();` shows only the call; **ConfigWatcher.cpp:34** selects `std::vector<std::string>{}` versus `Config::mgr()->getConfigPaths()` using disable_autoreload. | “This guarded statement calls update on the object returned by Config::watcher().” |
| K17 | SUPPORTED | legacy-ConfigManager.cpp:1079: `Config::watcher()->setOnChange([this](const CConfigWatcher::SConfigWatchEvent& e) {`; full init 1077–1087 confirms registration in init, callback reload at 1081, and an initial reload outside the callback at 1084. | — |
| K18 | SUPPORTED | legacy-ConfigManager.cpp:1080: `Log::logger->log(Log::DEBUG, "CConfigManager: file {} modified, reloading", e.file);`; the full pinned line, unlike the short frozen message substring, shows DEBUG and e.file explicitly. | — |

Counts: 4 SUPPORTED, 2 OVERREACH, 0 UNSUPPORTED. These are entailment verdicts, not counter results.

## Prose coverage and the five corrected sentences

| entry location / sentence group | scoped audit result |
|---|---|
| Chain 4, line 23: readable registration; callback route; wd lookup; stored file rather than name | Supported by EventLoopManager 70–73, 124–140 and ConfigWatcher 80–111, provided registration is understood under its valid-FD guard and callbacks under the matched-wd branch. No event-name read occurs. |
| Chain 5, line 24: callback installation, log, reload | Supported by full init 1077–1087, including reload at 1081. No claim that log output independently proves modification is needed. |
| Chain 6, line 25: reload/reset/parse/postConfigReload; REFRESH_ALL request | Supported by full reload 726–751 and postConfigReload 970–1075. The request is not proof that an asynchronous refresh already ran. |
| Chain 7, line 26: watcher-bit guard; bit 8; uint16 max; OR aggregation | Supported by PropRefresher.cpp 29–42, 55–159 and .hpp 9–24; arithmetic is explicitly identified. Scheduling and “every reload” require F4. The final source-derived consequence is explicitly labelled inference. |
| Corrected missing-target/inaccessible, line 40 | Nomatch-before-status ordering is correct for a target already absent at glob time; exclusivity and “never” fail under F3. |
| Corrected duplicate watches, line 46 | Same-inode versus duplicate userspace records is a real improvement, supported by ConfigWatcher 45–73 and inotify(7) 89–92, 293–302; exact-one-record wording needs F6. No membership/deduplication test appears in the complete source/watch loops. |
| Corrected glob collation, line 70 | Properly bounded to the glibc observations in prior audit G02/G05; explicitly leaves Hyprland locale/libc linkage unpinned. No new glibc experiment performed. |
| Corrected HOME-unset, line 54 | MiscFunctions 61–83 shows getenv and string construction, and handleSource 1802–1855 has no catch. libstdc++ exception behavior is explicitly attributed to the prior R06 observation, not asserted as a pinned fact about Hyprland's build. ENVHOME is static: the observation concerns its first initialization, not every later environment change. |
| Limits failure paths, line 136 | Supported: invalid inotify constructor returns; enterLoop tests validity; add-watch results are unchecked; complete onInotifyEvent has no overflow branch. |
| Limits reload per event, line 137 | F1 and F2: the touch observation and universal callback implication are not supported. “Could call reload several times” remains a properly modal source consequence for multiple matched events. |
| Corrected rename-over IN_IGNORED, line 138 | Canonical wave-1 lab a4 explicitly observes IN_IGNORED after rename-over and no later event from the dead watch; source predicts a reload only if that wd still matches. Entry correctly says the lab is not Hyprland and labels post-reload consequences inference; F2 supplies the missing match condition. |
| Limits source-only / legacy-provider / no live reload framing, lines 133, 135, 140–142 | Preserves the distinction between pinned source, historical captures and live behavior. These limitations do not justify F1's misquotation or F2/F4's universal statements. Historical /proc measurements and the runtime-keyword path are outside K13–K18 and were not independently re-measured. |

## Commands, receipts, and null checks

Read `claims-frozen-v2.md`, `registration-v2.md` first and registration.md §C1. Tried `read xd://lsp` before source investigation: output `No such tool: xd://lsp`; consequently no LSP status/references/definition/diagnostics could run. The fallback is manual numbered-function reading; literal scans below are NOT semantic caller proof.

Canonical data was obtained with these exact argument forms (all successful, no git mutations):

```text
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:corpus/knowledge/hyprland-config-autoreload-r56.md
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:.ufo/waves/round-56/w2/R56W2RevProsePath.md
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:.ufo/waves/round-56/w1/R56ScoutInotifyLab/raw-output.txt
```

For each of the seven pin paths listed in `canonical-sha256.txt`, used `subprocess.check_output(['git','-C',lane,'show',rev+':'+path])` from the Python evaluation tool, with lane/rev exactly as above. That exported only scoped evidence blobs, not a mirror. The receipt includes the decisive numbered lines. No shell pipeline, compiler, compositor, new fixture/runtime or host probe was used.

Null-check code actually run over the canonical captured watcher body:

```python
watcher = (out/'Hyprland-ConfigWatcher.cpp').read_text().splitlines()[79:111]
for token in ['ev->mask', 'IN_Q_OVERFLOW', 'ev->name']:
    hits = [i+80 for i,s in enumerate(watcher) if token in s]
```

Actual output:

```text
STATIC_LITERAL_SCAN ConfigWatcher.cpp:80-111 'ev->mask' -> []
STATIC_LITERAL_SCAN ConfigWatcher.cpp:80-111 'IN_Q_OVERFLOW' -> []
STATIC_LITERAL_SCAN ConfigWatcher.cpp:80-111 'ev->name' -> []
Prior lab touch result: True
```

The last boolean checks that the canonical old receipt contains `after touch: NONE`, not that a new touch experiment ran. No null result is used to imply that the callback is unconditional.

Deliverables, all under `/home/vgpnk/Projects/shokunin/mado-shokunin/`:

- `.ufo/waves/round-56/w3/R56W3RevAuditA2C.md` (this report).
- `.ufo/waves/round-56/w3/R56W3RevAuditA2C/canonical-sha256.txt` (eight original blob hashes and paths).
- Same directory: canonical entry plus seven scoped pin blobs; `decisive-excerpts.txt`; `prior-lab.txt`; `prior-prose-audit.md`.

## Residual risk / verification gaps

No Hyprland build/run, save/reload, host reads, race reproduction, C1 counter, harness, or whole-repo diagnostics ran. This seat audits source entailment and canonical historical receipts, not runtime behavior or numerical predicate attainment. K18 is supported by the complete pinned source line; its shorter frozen quote alone does not establish its argument. The corrected libc and libstdc++ sentences have historical attribution, not fresh reproduction. No scratch files were created; therefore none require removal. No tools installed or upgraded. No non-author independence claimed.

Self-evaluation: accuracy 4/5 (race/scheduling counterexamples are source inferences, not live reproductions); completeness 4/5 (all six assigned rows and named corrections covered; historical /proc observations deliberately not re-measured); clarity 4/5 (row and prose findings separated, but evidence is lengthy); actionability 5/5 (one-sentence corrections and exact pin locations); conciseness 4/5 (receipt detail retained for reproducibility). Overall 4.2/5. Main improvements would be a separately authorized runtime reproduction of the conditional error paths and semantic diagnostics if an LSP device becomes available; neither is claimed here. The user should find the scope and unrun checks explicit.
