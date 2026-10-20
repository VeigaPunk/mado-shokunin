# InputDraft — candidate U6 note (round 15, mado-r15-w1)

Leaf executor. Deliverable: `.ufo/waves/round-15/input-draft.txt` (candidate note
body only; no corpus, registry, SKILL, SCORECARD or LOG edit by this seat).
Absolute draft path:
`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-15/input-draft.txt`.

## Final source reconciliation (parent-directed)

The original dispatch reserved "S051 libinput tools docs" and "S052 Wayland core
XML". Parent's final IDs supersede that numbering and my draft follows them:

- **S051** = libinput 1.32.0 `doc/user/tools.rst` at immutable tag 1.32.0.
  Immutable source, not the moving `latest/tools.html`. It **supersedes S007**;
  S007 stays queued historical and is cited nowhere.
- **S052** = Wayland core `protocol/wayland.xml` at tag 1.26.0, scoped to
  `wl_seat`/`wl_pointer`/`wl_keyboard`. Distinct input scope from S043
  (`wl_registry`); the distinct-scope overlap review is parent-owned, recorded
  as manually reviewed.
- No S051/S052 duplicate was created for the installed XML or the HTML page.

## Exact retained evidence

| Item | Value |
|---|---|
| S051 URL | `https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.32.0/doc/user/tools.rst` |
| S051 revision | tag `1.32.0`; tag object `c7e6fe66f509ba2eda680c28aa64795987b49e7c`; peeled commit `5cf833b572f5a33663888da321dce0ba1abd82a2` |
| S051 bytes | 16990 (`curl … \| wc -c`); sha256 `53264328664493c0fc7074722650ba42afcf8b30c94ce7cc94157544b654ff5f` |
| S051 anchors | `§Helper tools` :1-32; `§libinput list-devices` :34-79; `§libinput list-kernel-devices` :81-128; `§libinput debug-events` :130-201; `§libinput record and libinput replay` :204-388 |
| S052 URL | `https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml` |
| S052 revision | tag `1.26.0`; tag object `5f430e41167dd359b70fb5e9f584ba2dc058e4cc`; peeled commit `87cc8a8728a923fc57938faa81ba0e74f34ecdc7` |
| S052 bytes | 168656; sha256 `cc860987e54f8d85c940e97fa1270c69b6e4ad31fbcf5a7f00107ce1157f5e07` |
| S052 anchors | `wl_seat` :2004-2137 (capabilities :2030, get_keyboard :2075, missing_capability :2026), `wl_pointer` :2138-2572 (enter :2197, motion :2224, button :2244, frame :2313), `wl_keyboard` :2573-2753 (keymap :2600, enter :2614, leave :2635, key :2669) |
| Byte equality | Upstream tag 1.26.0 raw XML sha256 equals installed `/usr/share/wayland/wayland.xml` (`wayland 1.26.0-1`); file equality only, not compositor-binary equivalence |

The draft's head-15 header carries the provenance trio (`source:`,
`verified-at:`, `recheck:`) and exactly one `covers: U6`. Only S051 and S052
appear in the source line, so the reciprocal join is both directions once the
two rows name the integrated note in `used-by`.

All 18 quotes were checked against the pinned bytes; each is ≤25 words
(maximum 22). RST emphasis/inline-literal markup is rendered as plain text;
wording is otherwise verbatim.

## Suggested registry cells (L1 applies, append-only)

Proposed integrated path for both `used-by` cells:
`corpus/knowledge/input-layer-boundaries-r15.md`.

S051 (new row, tier A docs, status `mined`): source `libinput 1.32.0 helper
tools source — https://gitlab.freedesktop.org/libinput/libinput/-/raw/1.32.0/doc/user/tools.rst`;
anchor `tag 1.32.0 (tag c7e6fe66… → commit 5cf833b5…); §Helper tools :31-32,
§libinput-list-devices :45-46, §libinput-debug-events :141-143,
§libinput-record :220-277 (section :204-388); 16990 bytes, sha256 53264328…`;
teaches `list-devices reports libinput defaults not desktop configuration;
record captures kernel events and obscures key codes; replay creates a virtual
device — observation and injection classes are distinct`; recheck `on-release`.

S052 (new row, tier A spec, status `mined`): source `Wayland core input
interfaces — https://gitlab.freedesktop.org/wayland/wayland/-/raw/1.26.0/protocol/wayland.xml`;
anchor `tag 1.26.0 (tag 5f430e41… → commit 87cc8a87…); wl_seat :2004-2137,
wl_pointer :2138-2572, wl_keyboard :2573-2753; 168656 bytes,
sha256 cc860987…; bytes equal installed XML (wayland 1.26.0-1)`;
teaches `capability events gate object creation; v5+ objects created before an
added-capability event stay inert; focus is surface-scoped; key codes need a
keymap; button codes come from Linux input headers; delivery is not proven`;
recheck `on-release`.

S007 is left `queued` with no cell mutation. If L1 instead re-purposes S016 for
the compositor `getoption`/`devices` route, its scope/used-by change must be
logged old→new in the round-15 lesson. This draft deliberately does not cite
S016: its registered scope is `getprop`-only, so the draft names the wiki
`#info` route as an unexecuted pointer outside the two-source join.

## Package-drift record (honest)

Static query `pacman -Q libinput wayland` read `libinput 1.31.3-1` at the first
check in this wave and `1.32.0-1` at recheck; `wayland 1.26.0-1` both times.
This seat installed/upgraded nothing and ran no package command. The change is
another actor's; its provenance is outside this report. The documentation tag
and host package now share 1.32.0, but **no running-compositor, loaded-library
or delivered-event equivalence** is claimed; that remains `[UNK]`. The draft
states the transition and the non-equivalence explicitly.

## Safety and scope receipts

- Read-only only: two HTTPS raw-source fetches, `sha256sum`, `wc -c`,
  `pacman -Q`, `git ls-remote`, local XML `grep`/`sed` reads.
- Not run: any `libinput` subcommand, sudo, `/dev/input/*` access, event
  observation/recording/replay/injection, `hyprctl`, compositor reload or
  configuration write, IME client, kernel/DRM diagnosis, tests, linters,
  formatters, gates, smoke runs or live probes.
- No credential/auth file and no `~/.omp/agent/agent.db*` opened; no `omp` CLI;
  no delegation or `agent://all`.
- No tooling installed or updated; nothing to log under the tooling directive.
- Files written by this seat: the draft above and this report only.

## Risks / blockers for integration

1. **Reciprocal join path**: S051/S052 `used-by` must exactly match the final
   note path and the note's `source:` line must keep both IDs; a rename without
   updating `used-by` breaks the join. Source line must remain within the first
   15 lines.
2. **U6 facet check**: round-15 `measure.py` is not yet written when this draft
   was produced. The draft satisfies the stated rubric headings, exactly
   `covers: U6`, `[UNK]` in `## Unexercised delivery`, and the S051/S052 join;
   the builder should not add a U5-style body-facet requirement.
3. **Compositor-policy row**: it is distinguished but source-unjoined by design.
   Widening S016 to `#info` is an L1 decision needing an old→new mutation log;
   the draft avoids an unregistered widened claim.
4. **Version drift**: package now 1.32.0-1, but any host-behavior statement
   about the running compositor remains unproved. Do not promote the matching
   version number into a delivery or behavior fact.
