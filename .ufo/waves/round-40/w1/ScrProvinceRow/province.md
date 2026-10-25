# Round-40 refinement — draft for `PROVINCE.md` (append-only, seat ScrProvinceRow)

**Provenance.** Target: `PROVINCE.md` at lane rev
`e2b51d3b3f79768282914d57c1fa32cc85dcb06a` (95 lines; the round-23 tool table has
**7** ``| `tools/`` rows and **no `mado-options.py` row** — `grep -n 'mado-options'
PROVINCE.md` returns no match, exit 1). Round 39 landed the tool without a table row,
so the paragraph below names its read surface for the same reason the round-23 table
names the other `tools/` instruments. The text is append-only: it is inserted after the
`## Round-38 addendum`, edits no existing line, and leaves `:13-16` (the
`Never mutates a running compositor state` rule) byte-identical.

## The paragraph (append verbatim)

**Round-40 refinement (append-only; C1 operability — one named read verb, no new write surface):** the
round-23 table carries no `tools/mado-options.py` row (round 39 landed the tool; `grep -n 'mado-options'
PROVINCE.md` finds none), so its read surface is named here. With `--live`, the tool issues exactly one
`hyprctl getoption -j KEY` per declared key of the resolved table and one per `--probe KEY` — the request
socket's read verb, the same verb `tools/mado-verify.sh` already runs (`:28`; e.g.
`hyprctl -j getoption general:gaps_out`) — and never any other verb: `keyword`, `dispatch`, `reload`,
`setprop` and `--batch` are outside it. The tool never connects to the socket itself; it runs the
compositor's own client (`--hyprctl PATH`, default `hyprctl`) as a child process and compares the native
reply forms (`int`, `float`, `str`, `custom`, or the text `no such option`) after host-style conversion; a
probe key with no declarer becomes a `live-default` row. `--getoption FILE` is unchanged: a read of a
caller-supplied JSON dump, no program run. `--live` writes nothing — stdout only (one JSON array); its
`--selftest` writes only ephemeral fixtures inside a private temporary directory it removes on exit — and
imports only the Python standard library (`argparse glob json os shutil stat subprocess sys tempfile`). A
compositor failure (non-zero exit, malformed reply or unknown reply form) stops the run with exit 5 and a
message naming the key; a probe key that is empty or begins with `-` is refused with exit 2 before any
program runs. The boundary at `:13-16` is unchanged and is not widened: `--live` is an owned read surface
under the existing rule "Never mutates a running compositor state" — a named instrument for it, not an
exception to it — and the round-38 addendum's "no socket is ever connected, no request is sent" (`:92-93`)
stays scoped to those knowledge files, as it already was beside the `mado-verify.sh` row that runs the same
verb. Adjacent lanes: tsukuroi owns the compositor *package* (its version, install and unit
state; nothing of the option table and nothing of the verb), and no sibling lane's province names the verb
(`grep -ln 'hyprctl' */PROVINCE.md` in the fleet root → `mado-shokunin/PROVINCE.md` only); the operator
still applies any change the table recommends.

## Notes for the L1 integrator

- Placement: append after the `## Round-38 addendum` block (current `:82-95`); do not renumber or reflow
  the existing table or refinements.
- Grounding per clause (full citations in `.ufo/waves/round-40/w1/ScrProvinceRow.md`): the argv
  `[hyprctl, "getoption", "-j", KEY]` and the hostile-probe refusal at
  `.ufo/waves/round-40/c1/ctl-ref-tool.py.txt:623-641` (`native_query`: the exact argv
  `[hyprctl, "getoption", "-j", key]` at :625), `:708-712` (hostile-probe refusal before any run),
  `:686-726` (`main`: exit 5 at :725); the verb already owned by the
  `mado-verify.sh` row at `PROVINCE.md:28` and its invocation at `tools/mado-verify.sh:3455`; the rule at
  `PROVINCE.md:13-16`; the request-socket identity at `corpus/knowledge/ipc-contract-r25.md:36-39`.
- The paragraph describes the surface the frozen registration declares
  (`registration.md` §C1). If the *delivered* tool's argv or exit map differs from that, the delivered
  bytes win and this paragraph must be corrected to them before it is appended — the draft asserts
  nothing about a delivered `--live` (lane rev `e2b51d3` has none: `grep -n '"--live"' tools/mado-options.py`
  → no match; the tool is round-39's `461f8c3c…` build with `--getoption` only).
- Nothing here widens a write surface, admits a new config tree, or claims a live read was taken by this
  seat: this seat ran no compositor verb.
