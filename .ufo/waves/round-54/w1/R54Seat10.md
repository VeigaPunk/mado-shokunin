# R54Seat10 — uwsm-app environment frontier recon

Axes: **coverage** (previously uncovered sourced behavior) and **operability** (a bounded, source-verifiable account). Item 10 recon only; no lane/corpus edits or host observation.

## Finding

The assigned frontier is real and narrowly novel: the corpus README explicitly lists “`uwsm-app`'s environment” as still open in the round-47 terminal-selection bullet. The committed round-17 terminal route independently marks the wrapper as unsourced and says its environment effect is unknown. Round 54's frozen C2 target matches this gap: it adds a sourced `uwsm-app` environment/launch-contract entry based on three pinned upstream excerpts, not a new host-environment measurement. **Confidence: high** for corpus novelty/scope, based on those explicit frontier statements and the frozen predicate.

The pinned evidence separates several contracts rather than establishing an observed environment value: S375 is specifically environment-state export after preparation to the systemd user manager (and conditionally D-Bus activation environment); S376 identifies client-to-daemon argument transport via pipe; S377 identifies the generated unit-name form for `scope`. Together these support a sourced account of launch preparation/dispatch and environment propagation. They do not, from these excerpts alone, establish which concrete variables this host's terminal receives or the selected terminal's own argument/environment handling. Keep those as boundaries, not inferred outcomes.

## Coverage-map and overlap

- `corpus/README.md:116` explicitly leaves `uwsm-app` environment open alongside actual terminal start and argument handling. The current C2 scope addresses the environment/launcher contract half; it does **not** close the separate end-to-end hotkey process-start or terminal argument-handling questions.
- `corpus/knowledge/terminal-route-r17.md:103-107` documents `bindings.conf:2` invoking `uwsm-app -- xdg-terminal-exec ...` and explicitly leaves the wrapper's environment effect unknown. This is direct complementary scope; the new account should be linked as sourced context, not recast as proof that the terminal ran.
- Existing idle-route material (e.g. `idle-lock-plane.md:110-114, 266-276`) and theme route material mention `uwsm-app` as a launcher in specific chains. They are consumer-specific declarations/observations, not this general sourced app-daemon/environment contract; cite as joins only where the frozen host set permits.
- Frozen C2 host join set is precise: autostart lines 1–6, bindings line 2, and `omarchy-toggle-idle:9` (registration.md:71-76). Those joins establish declared launcher call sites; they are not evidence of a host process's inherited environment.
- S375–S377 are already frozen and assigned to the new entry; do not duplicate/re-register them as round-52 correction-plane evidence (claims-frozen.md:46-53, registration.md:55-76).

## Distinct failure/input attack: quote-valid but scope-overclaiming entry

Attacked predicate: **PRED-C2-r54 clause (c), with clause (a)'s factual boundary in view** (claims-frozen.md:55-65). Distinct from the registered forged-quote, missing provenance, registry-ID, README-index, wrong-commit, and no-host-joins controls (registration.md:78-90): an entry can pass every pin/quote/host-join check yet falsely claim that S375 proves the concrete environment of the host-launched terminal, or that S376 proves launch success. The frozen checker requires source/index/provenance, row/quote/pin integrity and ≥2 host joins; it does not state a semantic scope/overclaim check for the entry prose. Such prose could therefore be accepted while asserting a conclusion outside the cited evidence. This is a **potential predicate blind spot**, not evidence that the submitted entry actually makes this claim; item authors should keep conclusions restricted to sourced general contract and label host-specific received variables/process outcome unmeasured.

Exact static evidence commands (lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`):

```text
read corpus/README.md:116
=> Still open: whether a terminal process actually starts under the hotkey ..., the warm-cache path, `uwsm-app`'s environment, and the selected terminal's own argument handling.
read corpus/knowledge/terminal-route-r17.md:103-107
=> `uwsm-app` launcher not sourced there; [UNK] how it alters the environment.
read .ufo/waves/round-54/claims-frozen.md:55-65
=> clause (a)-(d): indexed/provenance entry, 3 frozen rows/quotes/pins, ≥2 host joins, controls.
read .ufo/waves/round-54/registration.md:78-90
=> six listed C2 mutations; no prose-scope/overclaim mutation listed.
read .ufo/waves/round-54/fetch/uwsm-0.27.1-uwsm-app.1.scd:60-69
=> client sends args via pipe; daemon returns shell code; daemon avoids repeated Python startup.
read .ufo/waves/round-54/fetch/uwsm-0.27.1-main.py:3713-3718
=> generated `scope` and `service` unit-name forms.
```

All evidence above is committed static text/pins. No package queries, domain/host reads, producer execution, or host/config/service/compositor interaction. No tool installs/updates.