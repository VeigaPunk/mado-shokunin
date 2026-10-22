#!/usr/bin/env python3
"""Write AttackPerf's inert scope-chain stress fixtures (eval JSONL data).

The eval source is data. This generator only writes it and checks that it
compiles to an AST (compile with PyCF_ONLY_AST); it never executes it.
"""
from __future__ import annotations

import ast
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIXTURE_DIR = ROOT / "fixtures"
TIMESTAMP = "2026-10-22T00:00:00.000Z"


def nested_defs(depth: int = 95, siblings: int = 4) -> str:
    """depth nested defs, each with `siblings` sibling defs; each level calls
    its siblings and the next level and returns it (the closure escapes)."""
    lines = ["import subprocess"]
    for level in range(depth):
        pad = "    " * level
        lines.append(f"{pad}def d{level}():")
        inner = pad + "    "
        for k in range(siblings):
            lines.append(f"{inner}def s{level}_{k}():")
            lines.append(f"{inner}    return {k}")
    pad = "    " * depth
    lines.append(f"{pad}subprocess.run(['pacman', '-Q', 'r23-perf-nest'])")
    for level in range(depth - 1, -1, -1):
        inner = "    " * (level + 1)
        if level + 1 < depth:
            lines.append(f"{inner}d{level + 1}()")
        for k in range(siblings):
            lines.append(f"{inner}s{level}_{k}()")
        if level + 1 < depth:
            lines.append(f"{inner}return d{level + 1}")
        else:
            lines.append(f"{inner}return None")
    lines.append("d0()")
    return "\n".join(lines)


def forwarder_chain(length: int = 400) -> str:
    lines = ["import subprocess",
             "def launch(argv):",
             "    subprocess.run(argv)",
             "def fwd0(cb, argv):",
             "    return cb(argv)"]
    for i in range(1, length):
        lines.append(f"def fwd{i}(cb, argv):")
        lines.append(f"    return fwd{i - 1}(cb, argv)")
    lines.append(f"fwd{length - 1}(launch, ['pacman', '-Q', 'r23-perf-forward'])")
    return "\n".join(lines)


def module_helper_chain(length: int = 2000, literals: int = 0) -> str:
    """Module helpers h0..h{n-1}, each with a caller-local PKG shadow, each
    calling the next; the last reads the module global PKG. `literals` adds
    that many module-level scalar globals before the helpers."""
    lines = ["import subprocess", "PKG = 'r23-perf-chain'"]
    lines.extend(f"g{i:05d} = {i}" for i in range(literals))
    for i in range(length - 1):
        lines.append(f"def h{i}():")
        lines.append("    PKG = 'r23-perf-shadow'")
        lines.append(f"    return h{i + 1}()")
    lines.append(f"def h{length - 1}():")
    lines.append("    subprocess.run(['pacman', '-Q', PKG])")
    lines.append("h0()")
    return "\n".join(lines)


def escape_fixpoint_loop(aliases: int = 300, calls: int = 60) -> str:
    """A receiver whose callback reaches its call through a reverse-ordered
    alias chain inside a loop (one alias step per iteration at run time);
    called `calls` times with a module callback."""
    names = [f"a{i}" for i in range(1, aliases + 1)]
    lines = ["import subprocess",
             "def launch(argv):",
             "    subprocess.run(argv)",
             "def recv(cb, argv):",
             "    " + " = ".join(names) + " = None",
             f"    for _ in range({aliases}):"]
    for i in range(aliases, 1, -1):
        lines.append(f"        a{i} = a{i - 1}")
    lines.append("        a1 = cb")
    lines.append(f"    a{aliases}(argv)")
    for _ in range(calls):
        lines.append("recv(launch, ['pacman', '-Q', 'r23-perf-escape'])")
    return "\n".join(lines)


def escape_fixpoint_unused(aliases: int = 300, calls: int = 60) -> str:
    """Same receiver shape, but the reverse alias chain sits in a nested def
    that is never called; recv calls cb directly."""
    lines = ["import subprocess",
             "def launch(argv):",
             "    subprocess.run(argv)",
             "def recv(cb, argv):",
             "    def unused():"]
    for i in range(aliases, 1, -1):
        lines.append(f"        a{i} = a{i - 1}")
    lines.append("        a1 = cb")
    lines.append(f"        a{aliases}()")
    lines.append("    cb(argv)")
    for _ in range(calls):
        lines.append("recv(launch, ['pacman', '-Q', 'r23-perf-escape'])")
    return "\n".join(lines)


FIXTURES = {
    "nested-defs-95x5": (nested_defs, {"depth": 95, "siblings": 4}),
    "forwarder-chain-400": (forwarder_chain, {"length": 400}),
    "module-helper-chain-2000": (module_helper_chain, {"length": 2000}),
    "escape-fixpoint-loop-300x60": (escape_fixpoint_loop, {"aliases": 300, "calls": 60}),
    "escape-fixpoint-unused-300x60": (escape_fixpoint_unused, {"aliases": 300, "calls": 60}),
}


def record(name: str, code: str) -> bytes:
    rec = {
        "type": "message",
        "id": f"r23-attackperf-{name}",
        "timestamp": TIMESTAMP,
        "message": {
            "role": "assistant",
            "content": [{
                "type": "toolCall",
                "id": f"eval-r23-attackperf-{name}",
                "name": "eval",
                "arguments": {"language": "py", "code": code},
            }],
        },
    }
    return (json.dumps(rec, ensure_ascii=True, separators=(",", ":")) + "\n").encode("utf-8")


def main(argv: list[str]) -> int:
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    selected = argv or list(FIXTURES)
    manifest = {}
    for name in selected:
        if name in FIXTURES:
            fn, kwargs = FIXTURES[name]
        else:  # name=<builder>:<k>=<v>,... for scaling series
            builder, _, spec = name.partition(":")
            fn = {"loop": escape_fixpoint_loop, "unused": escape_fixpoint_unused,
                  "nest": nested_defs, "fwd": forwarder_chain,
                  "chain": module_helper_chain}[builder]
            kwargs = {k: int(v) for k, v in (p.split("=") for p in spec.split(","))}
        code = fn(**kwargs)
        compile(code, "<fixture>", "exec", flags=ast.PyCF_ONLY_AST, dont_inherit=True)
        data = record(name.replace(":", "-").replace(",", "-").replace("=", ""), code)
        path = FIXTURE_DIR / (name.replace(":", "-").replace(",", "-").replace("=", "") + ".jsonl")
        path.write_bytes(data)
        manifest[path.name] = {"builder": fn.__name__, "params": kwargs,
                               "source_lines": code.count("\n") + 1,
                               "bytes": len(data),
                               "sha256": hashlib.sha256(data).hexdigest()}
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
