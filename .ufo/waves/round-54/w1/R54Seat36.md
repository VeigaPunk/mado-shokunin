# R54Seat36 — C2 host-join boundary review (item 36)

Axes: coverage, operability. Scope: PRED-C2-r54 host-join clause and frozen host set only. No host reads or producer execution.

## Findings

### High — allowed citations do not prove the claimed host join or line content

Frozen clause (c) accepts at least two citations among the finite host set; registration lists `~/.local/share/omarchy/default/hypr/autostart.conf:1-6`, `~/.config/hypr/bindings.conf:2`, and `~/.local/share/omarchy/bin/omarchy-toggle-idle:9` (registration.md:71-76; claims-frozen.md:63-65). This makes membership in a list sufficient for the counter's host-join leg; it does not require evidence of the referenced line's bytes, that the line actually invokes `uwsm-app`, or a semantic edge from the cited declaration to the entry's facts.

Two exact joins and their evidentiary limits:
- `~/.local/share/omarchy/default/hypr/autostart.conf:1`: frozen fetch README describes this as `exec-once = uwsm-app -- hypridle` (round-54/fetch/README.txt:17); existing sourced corpus likewise identifies the launch declaration (corpus/knowledge/idle-lock-plane.md:109-112). It supports a declared idle launcher, not that this launcher supplies the environment export described by S375.
- `~/.config/hypr/bindings.conf:2`: corpus/knowledge/terminal-route-r17.md:81,103-105 describes the declared `uwsm-app -- xdg-terminal-exec` binding and explicitly leaves how the wrapper alters environment unknown. It supports a declared terminal launcher, not observed process environment or terminal startup success.

The evidence boundary forbids host/config reads and the frozen predicate constrains the counter's inputs (claims-frozen.md:82-84); therefore this is a coverage/overclaim risk, not a request to add forbidden live host checks. The lane may report these as host-declaration joins only, explicitly not as runtime verification or proof that environment behavior was exercised at either callsite. Existing documentation itself marks the wrapper environment unknown (terminal-route-r17.md:103-105), demonstrating why broader wording would overclaim.

Distinct from a duplicate-citation counting ambiguity: the attack is valid, distinct registered locations whose target facts do not follow from the declarations. Frozen controls enumerate quote, registry, provenance, index, commit, and no-join failures (registration.md:78-87), but no control challenges inference from a valid join citation to runtime/environment behavior.

## Commands / evidence

- Read `.ufo/waves/round-54/claims-frozen.md` lines 55-65, 82-84 and `.ufo/waves/round-54/registration.md` lines 71-90.
- Read `.ufo/waves/round-54/fetch/README.txt` line 17.
- Read `corpus/knowledge/terminal-route-r17.md` lines 81, 103-105 and `corpus/knowledge/idle-lock-plane.md` lines 109-112.
- Literal search: `grep` via repository search for `autostart.conf|bindings.conf|toggle-idle|uwsm-app-environment` across frozen round-54 evidence, C2 wave reports, and corpus knowledge/SOURCES. Results included cited paths above; it also surfaced R54Seat22's distinct duplicate-location ambiguity (w1/R54Seat22.md:5-19). Search is discovery only, not semantic proof.
- No host/config reads, capture, producer execution, or mutations performed. No tools installed or updated.

Attack predicate: PRED-C2-r54 clause (c), checking whether the required joins' declared citations can be mistaken for evidence that host runtime/environment behavior is verified. Verdict: contract constrains only citation membership/count, so runtime/environment conclusions from those joins are unsupported; phrase joins narrowly as declarations.