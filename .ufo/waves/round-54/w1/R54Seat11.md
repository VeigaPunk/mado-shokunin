# R54Seat11 — uwsm-app environment frontier reconnaissance

## Axes
Coverage: whether the assigned frontier is genuinely open and distinguishable from adjacent sourced claims. Operability: whether static evidence supports a safe, bounded statement without asserting host runtime behavior.

## Finding
**Observed:** Frozen C2 explicitly assigns coverage to `uwsm-app`'s environment on the owned launcher chain: `claims-frozen.md:46-53`; its predicate requires a new sourced entry, indexed and linked to S375–S377, plus at least two citations from a fixed host set (`claims-frozen.md:55-75`; `registration.md:55-76`). The current coverage map still lists “`uwsm-app`'s environment” among open items alongside terminal process start and warm-cache path (`corpus/README.md:116`). Existing `terminal-route-r17.md:103-105` explicitly states the wrapper is not sourced there and its environment effect is `[UNK]`. Thus the specific wrapper environment gap is not already claimed closed by the cited terminal-selection entry.

The prescribed source evidence is present as committed pins under `.ufo/waves/round-54/fetch/` (README, `main.py`, and man-page files are named by `registration.md:57-65`). The registration identifies the distinct source dimensions: environment export after preparation (S375), app-daemon arguments via pipe (S376), and generated unit name (S377). These are upstream contract facts, not proof of what environment a particular host process received.

Adjacent coverage is substantial but different: `corpus/knowledge/idle-lock-plane.md` documents `uwsm-app` launch declarations and explicitly describes host/process material, while `corpus/knowledge/xdg-terminal-selection-r47.md` covers terminal selection and retains wrapper environment as unknown. `corpus/knowledge/remaining-planes-census.md` describes consumer scopes; it does not, by that citation alone, establish the wrapper's environment transformation contract. The host joins frozen for the new entry are config declarations (`registration.md:71-76`), not permission to inspect live state; no host/config/domain reads or producer execution were performed here.

## Novelty and ownership overlap
The novelty is narrow and credible: upstream `uwsm-app` environment/launch contract, joined to already-declared owned launcher lines, while preserving runtime delivery as unknown. It is not a new terminal-selection account, idle daemon state measurement, or compositor environment capture. Sibling ownership is distinct by registration: C2 owns the entry and its source rows; C1 is the errata verifier (`claims-frozen.md:13-44`). The wave registry places R54Seat11 among wave-1 members (`.ufo/waves/round-54/w1/swarm-registry.json:68-73`), but the visible JSON excerpt does not disclose its role/item field; I make no claim about other seat assignments. I did not inspect sibling reports, so report-level overlap remains unresolved.

## Distinct failure/input
Independent coverage-map attack: **environment inheritance versus exported environment is a boundary ambiguity.** A source statement that changes the systemd user manager (and possibly D-Bus activation environment) after preparation does not by itself prove the launched command's process environment, and a daemon-pipe statement does not prove that every launch route takes that path. A sourced entry should attribute each claim strictly to its quoted mechanism and avoid collapsing manager activation state, app-daemon request transport, generated unit naming, and the eventual child environment into one assertion. This is distinct from the frozen control mutations (forged quote, unregistered ID, missing provenance, missing index row, wrong commit, no host joins) in `registration.md:78-87`; no control was executed.

## Confidence and unresolved gaps
High confidence that the README frontier and R47 note leave the wrapper-environment subject explicitly open and that frozen registration separates the source-grounded C2 item from C1. This is static corpus evidence only. Unresolved: exact scope of the pinned upstream statements beyond the registration's located excerpts, whether sibling scouts found other overlapping drafts, and actual host process environment/runtime delivery. No speculative host behavior asserted.

## Commands and outputs
- `read skill://godspeed` — returned the Godspeed skill instructions.
- `read .../claims-frozen.md` — read frozen C1/C2 contracts; relevant C2 lines 46–75.
- `read .../registration.md` — read source-row contract, host join set and controls; relevant lines 55–90.
- `glob .../.ufo/waves` — confirmed round-54 fetch pins and wave artifacts exist; no host reads.
- `glob .../corpus` — listed coverage corpus and knowledge entries, including named adjacent notes.
- `grep 'uwsm-app|coverage map|frontier|environment' corpus; round-47` — found README frontier line 116 and R47 terminal boundary at `terminal-route-r17.md:103-105`, plus adjacent notes listed above. This is literal search evidence, not semantic callgraph evidence.
- `read .../swarm-registry.json` — showed members R54Seat01–37 with R54Seat11 at lines 68–73; selected field elided by reader, so role/item not established.
- `read /home/vgpnk/.omp/agent/RULES.md` — read install policy; no tool installed/updated.

## Report trailer
Lane-relative report: `.ufo/waves/round-54/w1/R54Seat11.md`. No tracked lane edits, fixture creation, git/jj mutation, producer execution, host/config/service/compositor mutation, package query, or tool update. No scratch artifacts created.