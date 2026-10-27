# Falsify21 — C2 source proposition entailment

## Deliverables
- `.ufo/waves/round-52/w1/Falsify21.md` — scoped falsification report.
## Findings

**Reproduced: yes — material proposition-to-source entailment failure.** Attacked item: C2, frozen proposition mapping/support condition (“every material factual proposition is mapped” with a support rationale), specifically the claim at entry line 206 that `sendshortcut` invalid-argument handling is a “config-time error.”

The entry (`corpus/knowledge/hyprland-dispatcher-dispatch-r51.md:203-206`) cites `Hyprland-legacy-DispatcherTranslator.cpp:532-535`. The pinned source bytes show `sendshortcut(const std::string& args)` constructs `CVarList2`, then returns `SDispatchResult{success=false, error="sendshortcut: invalid args"}` when the field count differs. That is a result returned from the dispatcher implementation, not a config parser rejection. By contrast, the pinned config parser (`Hyprland-legacy-ConfigManager.cpp:1594-1598`) performs `m_dispatchers.find(HANDLER)` and rejects an unknown dispatcher name. Those are distinct failure sites and the source does not support calling the sendshortcut result config-time.

**Reproducible setup / command:** Read the already available pinned source and entry; no producer, runtime, scratch fixture, or host access used.

```text
read /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/knowledge/hyprland-dispatcher-dispatch-r51.md:203-206
read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-51/fetch/Hyprland-legacy-DispatcherTranslator.cpp:531-535
read /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-51/fetch/Hyprland-legacy-ConfigManager.cpp:1594-1598
```

Actual result: the first source range executes argument-count validation inside `sendshortcut` and returns an action result; the separate config parser range rejects an unknown handler. The material claim is contradicted by the pinned source evidence. Existing independent source-truth review recorded the same mismatch (`.ufo/waves/round-51/w2/RevC2EntryTruth/entry-truth.md:58-64`); this probe independently re-read the entry and relevant pin bytes.

This falsifies the semantic support for this proposition, not the frozen structural predicate or any counter output. No C2 counter was invoked. No sources were opened from the network this round; source URL for S365 as recorded by the entry: `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/DispatcherTranslator.cpp`; access date is not applicable (local frozen pin only). No scratch was created, so no scratch cleanup was required. No tools installed.

## Deliverables
- `.ufo/waves/round-52/w1/Falsify21.md`

## Report
- `.ufo/waves/round-52/w1/Falsify21.md`
