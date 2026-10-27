#!/usr/bin/env python3
"""Build a seat-local fixture git repo modelling the round-52 C2 shape.

Commit 1 ("base"): registry, README, fetch pins — no new entry.
Commit 2 ("data"): adds corpus/knowledge/hyprland-dispatcher-execution-r52.md
  - 4 declared propositions, each bound to an opened-this-round S### row,
    a pin path/line, an exact located quote <=25 words, and a rationale
  - 1 smuggled mechanistic factual claim in body prose with NO mapping
All file bytes are seat-local under the scratch dir. Source bytes copied
read-only from the lane's round-51 fetch pins (Hyprland @ efb50993).
"""
import os
import shutil
import subprocess
import sys

SCRATCH = "/fast/scratch/hyaku/mado-r52/Falsify38"
FIX = os.path.join(SCRATCH, "fixture")
PINSRC = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-51/fetch"
PINS = [
    "Hyprland-KeybindManager.cpp",
    "Hyprland-HyprCtl.cpp",
    "Hyprland-legacy-DispatcherTranslator.cpp",
    "Hyprland-SharedDefs.hpp",
]

REGISTRY = """# source registry (fixture)

| id | source | tier | status | opened | used-by |
|---|---|---|---|---|---|
| S370 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/KeybindManager.cpp | A | mined | 2026-10-27 | knowledge/hyprland-dispatcher-execution-r52.md |
| S371 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/debug/HyprCtl.cpp | A | mined | 2026-10-27 | knowledge/hyprland-dispatcher-execution-r52.md |
| S372 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/DispatcherTranslator.cpp | A | mined | 2026-10-27 | knowledge/hyprland-dispatcher-execution-r52.md |
| S373 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/SharedDefs.hpp | A | mined | 2026-10-27 | knowledge/hyprland-dispatcher-execution-r52.md |
"""

README = """# corpus (fixture)

| entry | note |
|---|---|
| knowledge/hyprland-dispatcher-execution-r52.md | dispatcher execution, round-52 fixture |
"""

# Entry body: 4 declared propositions (P1..P4) fully bound; P5-SMUGGLE is a
# mechanistic factual claim in body prose with no row/pin/quote/rationale.
ENTRY = """# Dispatcher execution (round-52 fixture entry)

lane: mado-shokunin. round: 52. verified-at: 2026-10-27.

## Source rows

source: S370 - Hyprland 0.56.2 dispatcher map, the press-time call - `const auto DISPATCHER = m_dispatchers.find(k->mouse ? "mouse" : k->handler);`(Hyprland-KeybindManager.cpp:785)
source: S371 - Hyprland 0.56.2 hyprctl dispatch request, the socket lookup - `m_dispatchers.find(DISPATCHSTR)`(Hyprland-HyprCtl.cpp:1149)
source: S372 - Hyprland 0.56.2 legacy translator refusal of an unknown name - `Bad dispatcher`(Hyprland-legacy-DispatcherTranslator.cpp:32)
source: S373 - Hyprland 0.56.2 dispatch result defaults - `passEvent = false`(Hyprland-SharedDefs.hpp:53)

## Pin manifest

| pin | file | row |
|---|---|---|
| Hyprland-KeybindManager.cpp | src/managers/KeybindManager.cpp | S370 |
| Hyprland-HyprCtl.cpp | src/debug/HyprCtl.cpp | S371 |
| Hyprland-legacy-DispatcherTranslator.cpp | src/config/legacy/DispatcherTranslator.cpp | S372 |
| Hyprland-SharedDefs.hpp | src/SharedDefs.hpp | S373 |

## Proposition map

| proposition | row | pin | quote | rationale |
|---|---|---|---|---|
| P1: a press resolves the dispatcher name through the string-keyed map, rewriting mouse binds to the mouse name | S370 | Hyprland-KeybindManager.cpp | `const auto DISPATCHER = m_dispatchers.find(k->mouse ? "mouse" : k->handler);` | the find key is the stored handler, or the literal mouse name when the bind carries the mouse flag |
| P2: the socket dispatch verb reaches the same table with the stripped request string | S371 | Hyprland-HyprCtl.cpp | `m_dispatchers.find(DISPATCHSTR)` | HyprCtl resolves the dispatch request through the identical m_dispatchers member, so socket and press share one table |
| P3: an unknown name is refused before any implementation runs | S372 | Hyprland-legacy-DispatcherTranslator.cpp | `Bad dispatcher` | the translator entry point checks membership first and returns this error without calling a mapped function |
| P4: a dispatcher that sets no flag returns passEvent false by default | S373 | Hyprland-SharedDefs.hpp | `passEvent = false` | the result struct default leaves the event unswallowed unless a dispatcher sets passEvent true |

## Mechanism notes

Under sustained key repeat load the dispatcher table is rehashed every sixty
seconds to keep the press path latency flat. This maintenance pass is internal
to the keybind manager and is not observable from the socket verb.
"""


def git(*args):
    subprocess.run(["git", "-C", FIX] + list(args), check=True,
                   capture_output=True, env={"PATH": os.environ["PATH"],
                                             "HOME": os.environ["HOME"]})


def write(path, text):
    full = os.path.join(FIX, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as fh:
        fh.write(text)


def main():
    if os.path.exists(FIX):
        shutil.rmtree(FIX)
    os.makedirs(FIX)
    git("init", "-q", "-b", "main")
    git("config", "user.email", "falsify38@fixture.local")
    git("config", "user.name", "Falsify38 fixture")
    git("config", "commit.gpgsign", "false")

    write("corpus/README.md", README)
    write("corpus/SOURCES.md", REGISTRY)
    fetchdir = os.path.join(FIX, ".ufo/waves/round-52/fetch")
    os.makedirs(fetchdir, exist_ok=True)
    for pin in PINS:
        shutil.copyfile(os.path.join(PINSRC, pin), os.path.join(fetchdir, pin))
    git("add", "-A")
    git("commit", "-q", "-m", "base: registry, readme, fetch pins; entry absent")
    base = subprocess.run(["git", "-C", FIX, "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()

    write("corpus/knowledge/hyprland-dispatcher-execution-r52.md", ENTRY)
    git("add", "-A")
    git("commit", "-q", "-m", "data: new dispatcher execution entry with 4 bound propositions")
    data = subprocess.run(["git", "-C", FIX, "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()

    with open(os.path.join(SCRATCH, "fixture-revs.txt"), "w") as fh:
        fh.write("base=%s\ndata=%s\n" % (base, data))
    print("base=%s" % base)
    print("data=%s" % data)


if __name__ == "__main__":
    sys.exit(main())
