#!/usr/bin/env python3
"""Build the round-51 C2 control fixture (scratch-only, never the lane).

The fixture is a --no-hardlinks clone of the lane at a scratch path, a branch cut at the round
base, and one commit that holds:

  * the round-50 entry bytes at corpus/knowledge/hyprland-dispatcher-dispatch-r51.md, plus a
    source block (two new rows, quotes and pin bindings), a pin manifest and three held
    citations - so clauses (a), (b) and (d) can be met by construction;
  * registry rows S364/S365 (status mined, opened 2026-10-27) and their fetch pins;
  * the index row in corpus/README.md.

The point of the control is clause (c): the entry body IS the round-50 entry body, which is
also a corpus/knowledge file at the frozen base, so the shingle overlap can only be near 100%.
A run against this tree must therefore print admitted=0/1 verdict=TARGET_MISSED and fail
clause (c) alone.
"""
import argparse
import os
import shutil
import subprocess
import sys

ENTRY = "corpus/knowledge/hyprland-dispatcher-dispatch-r51.md"
R50 = "corpus/knowledge/hyprland-bind-key-match-r50.md"
SOURCES = "corpus/SOURCES.md"
README = "corpus/README.md"
FETCH = ".ufo/waves/round-51/fetch"
PINS = ("Hyprland-KeybindManager.cpp", "Hyprland-legacy-ConfigManager.cpp")

SRC_BLOCK = """
## Fixture source block (control)

source: S364 - Hyprland 0.56.2 dispatcher table, `src/managers/KeybindManager.cpp` @ `efb50993` - `const auto DISPATCHER = m_dispatchers.find(k->mouse ? "mouse" : k->handler);`(Hyprland-KeybindManager.cpp:785)
source: S365 - Hyprland 0.56.2 hyprlang bind handler lookup, `src/config/legacy/ConfigManager.cpp` @ `efb50993` - `const auto DISPATCHER = g_pKeybindManager->m_dispatchers.find(HANDLER);`(Hyprland-legacy-ConfigManager.cpp:1594)

| pin | file | row |
|---|---|---|
| Hyprland-KeybindManager.cpp | src/managers/KeybindManager.cpp | S364 |
| Hyprland-legacy-ConfigManager.cpp | src/config/legacy/ConfigManager.cpp | S365 |

held: corpus/knowledge/keybind-rule-semantics.md:66 keys=dispatcher,params
held: corpus/knowledge/bind-table-r25.md:60 keys=hyprctl,binds
held: corpus/knowledge/hyprland-input-devices-r46.md:71 keys=resolve_binds_by_sym
"""

ROWS = (
    "| S364 | Hyprland 0.56.2 dispatcher table - https://raw.githubusercontent.com/hyprwm/"
    "Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/KeybindManager.cpp | code | "
    "A | the dispatcher table looked up once a bind fires | Hyprland-KeybindManager.cpp:785 @ "
    "commit efb50993780079460b0cbed1363e2166a2de1d9f; pin .ufo/waves/round-51/fetch/"
    "Hyprland-KeybindManager.cpp | the event path finds the fired bind's handler in the "
    "dispatcher table | mined | 2026-10-27 | on-release | "
    "corpus/knowledge/hyprland-dispatcher-dispatch-r51.md |\n"
    "| S365 | Hyprland 0.56.2 hyprlang bind handler lookup - https://raw.githubusercontent.com/"
    "hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/"
    "ConfigManager.cpp | code | A | the parse-time dispatcher check on a bind line | "
    "Hyprland-legacy-ConfigManager.cpp:1594 @ commit "
    "efb50993780079460b0cbed1363e2166a2de1d9f; pin .ufo/waves/round-51/fetch/"
    "Hyprland-legacy-ConfigManager.cpp | an unknown dispatcher is refused at parse time | mined "
    "| 2026-10-27 | on-release | corpus/knowledge/hyprland-dispatcher-dispatch-r51.md |\n"
)

INDEX_ROW = (
    "| `knowledge/hyprland-dispatcher-dispatch-r51.md` (MADO-R51-1, round 51; Hyprland "
    "dispatcher dispatch) | Fixture control row: the round-50 entry bytes at the round-51 path, "
    "with a source block, pin manifest and held citations. | rows S364-S365 |\n"
)

# A body written for the satisfiability control only: distinct wording, so a run that meets
# clauses (a), (b) and (d) can also meet (c). It is fixture data, never an admitted entry.
PASS_BODY = """
## Control body (synthetic, non-admissible)

A bind line names four fields, and the fourth field is the dispatcher. At parse time Hyprland
lowercases that field and looks it up once; a miss aborts the whole line with an error naming the
offending word. Nothing about the argument is validated at that moment: the tail after the third
comma is kept as one opaque string and stored beside the handler name.

Runtime is where the string stops being opaque. When the key event path decides a bind has fired,
it takes the stored handler, finds the same table entry again, and calls the function stored under
that key, handing it the untouched argument text. The callee, not the parser, decides how the
argument is carved: some entries read the whole tail, some split on commas, some split once and
treat the remainder as free text, and a few treat it as a number or refuse it. That asymmetry
explains a class of configuration mistakes: a syntactically valid line can parse cleanly, appear
in the bind listing, and still do nothing useful because the chosen handler cannot read the
argument it was given.

Submaps change the lookup only by adding a filter, not by changing which table is consulted. A
bind created while a submap is current is tagged with that submap name; the event path compares
the active name against the tag before it considers the handler at all. The catch-all key is
refused outside a submap, so the tag and the catch-all restriction arrive together.

The hyprctl path reaches the same table from outside the event loop. Its request parser splits the
command line on spaces, treats the first token as a handler name, and hands the remaining words to
that handler as separate strings. A handler therefore sees two shapes for what a user thinks of as
one argument: the single stored tail when a key fires, and a token list when an operator types the
command. Those shapes are not interchangeable, and a dispatcher that joins its tokens with spaces
is not the same as one that never saw them split.

Release and long-press forms keep the handler but move the moment of invocation: the table entry
still resolves at parse time, while the call waits for the matching phase of the key lifecycle.
Suppression and consumption are decided by the event path around the call, not by the handler
itself.

Three consequences follow for anyone reading a configuration plane. First, the handler name is the
only part of the fourth field that is checked before the key is pressed. Second, the argument
grammar belongs to the handler, so a table of dispatchers is really a table of argument grammars.
Third, the same stored text has different parsers depending on whether it arrived from a key or
from a socket request.
"""


def run(cwd, *args):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if p.returncode != 0:
        sys.exit("fixture: %s failed: %s\n%s" % (" ".join(args), p.stdout, p.stderr))
    return p.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--fixture", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--mode", choices=("control", "pass"), default="control")
    args = ap.parse_args()
    lane = os.path.abspath(args.lane)
    fixture = os.path.abspath(args.fixture)
    if os.path.exists(fixture):
        shutil.rmtree(fixture)
    os.makedirs(os.path.dirname(fixture), exist_ok=True)
    run(os.path.dirname(fixture), "git", "clone", "--no-hardlinks", "--no-checkout",
        "--quiet", lane, fixture)
    top = run(fixture, "git", "rev-parse", "--show-toplevel").strip()
    assert os.path.realpath(top) == os.path.realpath(fixture), top
    run(fixture, "git", "checkout", "-q", "-B", "fixture", args.base)

    def read(rel):
        with open(os.path.join(fixture, rel), "rb") as fh:
            return fh.read()

    def write(rel, data):
        path = os.path.join(fixture, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as fh:
            fh.write(data)

    head = "" if args.mode == "pass" else read(R50).decode()
    entry = (head + SRC_BLOCK + (PASS_BODY if args.mode == "pass" else "")).encode()
    write(ENTRY, entry)

    src = read(SOURCES).decode()
    lines = src.splitlines(keepends=True)
    at = max(i for i, l in enumerate(lines) if l.startswith("| S363 |")) + 1
    assert lines[at].startswith("| S364") is False
    lines.insert(at, ROWS)
    write(SOURCES, "".join(lines).encode())

    rd = read(README).decode()
    rlines = rd.splitlines(keepends=True)
    at = max(i for i, l in enumerate(rlines) if l.startswith("| `knowledge/hyprland-bind-key-match-r50.md`")) + 1
    rlines.insert(at, INDEX_ROW)
    write(README, "".join(rlines).encode())

    for pin in PINS:
        write(FETCH + "/" + pin, read(".ufo/waves/round-50/fetch/" + pin))

    run(fixture, "git", "-c", "user.name=ExecCounterC2", "-c", "user.email=fixture@shokunin.local",
        "add", "-A")
    run(fixture, "git", "-c", "user.name=ExecCounterC2",
        "-c", "user.email=fixture@shokunin.local", "commit", "-q", "-m",
        "round-51 C2 control fixture: round-50 entry bytes at the C2 path + rows S364/S365")
    print(run(fixture, "git", "rev-parse", "HEAD").strip())


if __name__ == "__main__":
    main()
