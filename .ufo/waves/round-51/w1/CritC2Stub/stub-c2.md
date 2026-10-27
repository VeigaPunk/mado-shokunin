# C2 maximal-overlap stub critique

## Axes

- **Coverage:** lexical novelty gate does not establish that the content teaches the requested dispatcher surface.
- **Operability:** a deterministic per-file overlap counter is reproducible, but its broad baseline can penalize harmless cross-references.

## Candidate stub used for the lexical probe

This intentionally strips the round-50 key-match entry down to generic dispatcher-path language, then adds two proposed new source citations and three held citations. The two new rows are *proposed*, not claimed registered: the round-51 fetch directory and S364–S379 registry rows were absent at review time. Their quoted lines below are real, exact lines in the committed round-50 Hyprland pin, which is byte-pinned to v0.56.2; L1 can transfer/re-pin them under the round-51 manifest. No pin or registry identity is fabricated.

> # From a keybind dispatcher string to Hyprland 0.56.2 dispatch execution
>
> source: proposed S364 — Hyprland 0.56.2 `src/managers/KeybindManager.cpp`, pinned bytes `.ufo/waves/round-50/fetch/Hyprland-KeybindManager.cpp`, quote `m_dispatchers.find(k->handler)` (line 785).
>
> source: proposed S365 — same pinned file, quote `DISPATCHER->second(k->arg);` (line 154).
>
> held: `corpus/knowledge/dispatcher-semantics-r25.md:30` — dispatcher construction describes, rather than invokes, an action.
>
> held: `corpus/knowledge/hyprland-bind-key-match-r50.md:57` — the bind parser splits the configuration value into comma arguments.
>
> held: `corpus/knowledge/ipc-contract-r25.md:38` — the request socket is used for hyprctl-like requests.
>
> Hyprland parses a keybind configuration into a stored dispatcher string and argument, then resolves the dispatcher through the manager registry when processing the key event. The dispatcher argument is split with the bind parser’s comma-argument handling; special submap cases alter how the remaining argument text is preserved. The `hyprctl dispatch` request path uses the same dispatcher lookup and argument handling but enters through the IPC request handler rather than a key event. This entry concerns dispatcher-name lookup and execution, not which key symbol or modifier mask matches.

This candidate is *not* an acceptable sourced entry: proposed S364/S365 do not independently support all the assertions, especially argument splitting, submap exceptions and hyprctl dispatch parity. It is a useful adversarial lexical stub precisely because shallow generic wording can clear a lexical threshold without teaching those mechanisms.

## Actual shingle computation

Computed in scratch from the stub above and `corpus/knowledge/hyprland-bind-key-match-r50.md` bytes. Tokenization: lowercase Unicode `\w+` word tokens; contiguous word 8-grams; compare distinct-shingle sets; overlap reported as intersection / stub distinct shingles (the entry-side fraction is also given).

```
r50_shingles=4658
stub_shingles=189
intersection=0
stub_fraction=0.0000 (0.00%)
r50_fraction=0.0000 (0.00%)
```

The actual lexical result is far below 30%; it does not depend on selecting a convenient near-threshold paraphrase. The probe's computation used both texts directly (no hand-entered counts). This is only one baseline file; the frozen clause requires every base knowledge file and all recursive round candidate files.

## Answers / recommendation to L1

1. **Different-surface overlap is not inherently a violation.** A dispatcher-execution note can legitimately share standard terms or cite a key-match note; a high score against a different topic does not establish recycling. Conversely, this probe gets 0% against the key-match entry while remaining an inadequate explanation of the new surface. Therefore overlap is a useful lexical alarm, not a novelty or coverage oracle. Clause (c)'s literal “every `corpus/knowledge/*.md`” is overbroad if interpreted as a semantic prohibition: it can penalize standard terminology, factual prerequisites, and explicit cross-references. But silently changing it to same-surface-only changes the frozen predicate and creates a gaming route: authors can evade the checker by relabeling/splitting a surface. Keep the frozen wording for this round; amend future policy only by defining a defensible surface taxonomy and pairwise exclusions/normalization, while preserving candidate-inclusive comparisons and independent human semantic review. Never claim a high different-surface hit alone falsifies novelty.
2. **Recommendation: KEEP clause (c) unchanged in this wave; CHANGE interpretation and future design, not the frozen predicate.** Preserve the explicit 30% per-file ceiling and candidate-inclusive baseline (the latter directly fixes the round-50 omission). Require the human reviewer to inspect high-hit pairs and distinguish copied substance from legitimate overlap. This adversarial candidate measured 0/189 stub shingles shared with r50 (0.00%), yet communicates little beyond a generic pipeline; the number supports that the lexical detector cannot substitute for content review, not that the baseline should be waived. The requested actual dispatcher chain must still be grounded in the new pinned rows (at least parsing/splitting, lookup/execution, submap special handling, and hyprctl path); do not admit this stub on lexical compliance alone.

## Evidence boundary

- Frozen limit and baseline are claims.md:59–63; base is `6ca8c559a4a3d6d361101592116eea2bc7452437`.
- The round-50 entry is `corpus/knowledge/hyprland-bind-key-match-r50.md`; the old verifier reported candidate-derived recycling in the round-50 spot-check, §2, lines 37–38.
- Real code anchors in the round-50 pin: `m_dispatchers.find(k->handler)` at line 785 and `DISPATCHER->second(k->arg);` at line 154. They are suitable research leads, not round-51 source-row/pin evidence.
