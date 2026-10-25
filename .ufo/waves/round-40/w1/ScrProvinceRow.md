# ScrProvinceRow — PROVINCE.md refinement draft for `--live` (round-40, inline v2 w1)

Seat: `ScrProvinceRow` (leaf scribe; no dispatch, no background jobs).
Deliverable: an append-only `Round-40 refinement` paragraph for `PROVINCE.md`, drafted at
`.ufo/waves/round-40/w1/ScrProvinceRow/province.md`. **No tracked file was edited** — the L1 is the only
integrator, so the paragraph is a draft to append, not an applied change.

## 1. What was read (pinned)

| Fact | Command / path | Output |
|---|---|---|
| Lane rev at this seat | `git rev-parse HEAD` (lane root) | `e2b51d3b3f79768282914d57c1fa32cc85dcb06a` |
| No tracked file touched by this seat | `git status --porcelain` | only untracked `?? .ufo/waves/round-40/{assimilation,fetch,w1,w1.ready}` |
| `PROVINCE.md` size | `wc -l PROVINCE.md` | `95` |
| Tool table row count | ``grep -c '^| `tools/' PROVINCE.md`` | `7` |
| `mado-options.py` row present? | `grep -n 'mado-options' PROVINCE.md` | **no match, exit 1** |
| Boundary rule | `PROVINCE.md:13-16` | "**Refuses:** … Never mutates a running compositor state; every claim is file-byte- or screenshot-verified." |
| Addendum placement | `PROVINCE.md:82-95` | `## Round-38 addendum — request-socket knowledge ground (append-only)` is the current tail |
| Tool bytes at this rev | `sha256sum tools/mado-options.py` | `461f8c3c245bdfb6dcaac068a5ab378326c75dc91992b8012f9ca0e5019fb03a` (round-39 build; same sha as the S219 receipt cited in `corpus/lessons/round-39-verifier-spotcheck.md:41`) |
| `--live` present at this rev? | `grep -n '"--live"' tools/mado-options.py` | **no match, exit 1** (the tool carries `--getoption FILE` only) |

Frozen claims read first: `.ufo/waves/round-40/registration.md` (§C1 deliverable, exit map, controls,
harm watch).

## 2. Clause → grounding of the drafted paragraph

| Drafted clause | Grounding (path:line, command) |
|---|---|
| the round-23 table has no `tools/mado-options.py` row | `grep -n 'mado-options' PROVINCE.md` → exit 1; `grep -c '^\| \`tools/' PROVINCE.md` → 7 |
| exactly one `hyprctl getoption -j KEY` per declared key and one per `--probe` | `.ufo/waves/round-40/c1/ctl-ref-tool.py.txt:623-641` (`native_query`), argv literal `[hyprctl, "getoption", "-j", key]` at `:625`; `merge_live` at `:644-683` queries every row then every probe |
| `--hyprctl PATH`, default `hyprctl`; `--probe` repeatable | same file `:695` (`parser.add_argument("--hyprctl", default="hyprctl")`), `:696` (`action="append"`) |
| "the request socket's read verb", "same verb `mado-verify.sh` already runs (`:28`)" | `PROVINCE.md:28` row text: "`hyprctl` read verbs only (version, instances, configerrors, **getoption**, binds, monitors, layers)"; live invocation `tools/mado-verify.sh:3455` → `hyprctl -j getoption general:gaps_out` |
| request-socket identity | `corpus/knowledge/ipc-contract-r25.md:36-39`: the request socket "is used for hyprctl-like requests" |
| never any other verb (`keyword`, `dispatch`, `reload`, `setprop`, `--batch` outside) | the only subprocess call in the reference is `native_query`'s getoption argv (`:625`); the round-40 boundary list is the frozen registration's host-safety set |
| never connects to the socket itself; runs the compositor's client as a child | `ctl-ref-tool.py.txt:625` (`subprocess.run([hyprctl, …])`); consistent with `PROVINCE.md:92-93` (knowledge work connects no socket) |
| native forms `int|float|str|custom` / `no such option`; host-style conversion; `live-default` | `ctl-ref-tool.py.txt:623-641` (reply-form parsing); `tools/mado-options.py:454-491` (`values_equal`, `load_live`), `:510-518` (`live-default`) |
| `--getoption FILE` unchanged (file read, no program) | `tools/mado-options.py:537-538,556-558` (`load_live` path); docstring `:19-20` |
| writes nothing — stdout only, one JSON array | `tools/mado-options.py:565` (`sys.stdout.write(json.dumps(rows))`), `:50-51` exit map |
| `--selftest` temp fixtures removed on exit | `tools/mado-options.py:594` (`tempfile.mkdtemp(prefix="mado-options-st-")`), `:1035-1036` (`shutil.rmtree(tmp, ignore_errors=True)` in `finally`) |
| standard library only | `tools/mado-options.py:48` ("subprocess is used in the read path; Python stdlib only"), imports `:69-77` = `argparse glob json os shutil stat subprocess sys tempfile` |
| exit 5 on compositor failure naming the key | `ctl-ref-tool.py.txt:623-641` (every failure raises with the key in the message), `:725` (`return 5`) |
| exit 2 on a hostile probe key, before any program runs | `ctl-ref-tool.py.txt:708-712` (`if not k or k.startswith("-"): … return 2`), reached before `merge_live` |
| owned read surface under the existing rule, boundary not widened | `PROVINCE.md:13-16` quoted verbatim; the paragraph adds an instrument, not an exception |
| adjacent lane: tsukuroi owns the compositor *package* | `../tsukuroi-shokunin/PROVINCE.md:3-4` domain = "host operability & system repair … package state, systemd, drivers/firmware, boot health"; `:124` OUT-004/ADJ-03 routes the hypr config plane to mado |
| no sibling lane's province names the verb | `grep -ln 'hyprctl' */PROVINCE.md` from the fleet root → `mado-shokunin/PROVINCE.md` only |

## 3. Behavior of the draft

- One bold-lead paragraph in the house style (`**Round-40 refinement (append-only; …):**`), placed after
  `## Round-38 addendum`; no existing line renumbered, reflowed or reworded.
- It states the required facts: exactly `hyprctl getoption -j KEY` per declared key and per `--probe`, no
  other verb, writes nothing, standard library only, owned read surface under
  "Never mutates a running compositor state"; adjacent lanes named (tsukuroi: compositor package; none owns
  the verb).
- Two additions beyond the minimum, each grounded: (a) the round-38 addendum's "no socket is ever
  connected" is explicitly left scoped to its knowledge files — the pre-existing `mado-verify.sh` row
  already runs the same verb beside it, so this is continuity, not a new reading; (b) the exit map
  (5 / 2) because the province accounts for the instrument's failure surface.

## 4. Findings

1. **Province inventory gap (attacks the round-23 wave-2 rule).** `PROVINCE.md:32` says the table "covers
   every tracked file under `tools/`", but round 39 landed `tools/mado-options.py` (tracked, sha
   `461f8c3c…`) with no row (`grep -n 'mado-options' PROVINCE.md` → exit 1). The drafted paragraph names
   the tool's read surface, which closes the operability part; a full row (Reads/Writes/Owner columns) is
   still missing and is the integrator's decision, not this seat's.
2. **Apparent tension with `PROVINCE.md:92-93` (supports the boundary wording).** The round-38 addendum
   says "no socket is ever connected, no request is sent" of the *knowledge* files; `--live` sends a
   request through the compositor's own client. The addendum is already scoped that way beside the
   `mado-verify.sh` row (`:28`), so the paragraph restates the scope instead of editing the addendum.
3. **Exit 5 is a free slot (supports §C1's exit map).** `tools/mado-options.py:50-51` maps 0/2/3/4/1;
   nothing collides with 5.
4. **The draft is surface-descriptive only.** At `e2b51d3` there is no `--live` in the tool, so the
   paragraph is written against the frozen registration's §C1 contract and the never-delivered reference
   control (`c1/ctl-ref-tool.py.txt`, a CONTROL). If the delivered bytes differ in argv or exit map, the
   delivered bytes win; the draft says so in its own integrator note.

## 5. Touched surfaces / out of scope

- Written: `.ufo/waves/round-40/w1/ScrProvinceRow/province.md` and this report only.
- Not touched: `PROVINCE.md` itself, any tracked file, `tools/`, `quality/`, `corpus/`, `.ufo/state/`,
  fleet paths other than read-only `tsukuroi-shokunin/PROVINCE.md` and `*/PROVINCE.md` greps, no git/jj
  mutation (read-only `rev-parse`/`status` only).
- No compositor verb was run by this seat (no `hyprctl` call of any kind); no package operation; no tool
  installed, so no tool/version/channel record is owed.
- No gate was run: C1/C2 counters, `--selftest`, axis checks and the harm watch are the L1's verification,
  not this seat's.

## 6. Artifacts

- Draft to append: `.ufo/waves/round-40/w1/ScrProvinceRow/province.md`
- This report: `.ufo/waves/round-40/w1/ScrProvinceRow.md`
