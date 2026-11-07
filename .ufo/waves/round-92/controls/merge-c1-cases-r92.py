#!/usr/bin/env python3
"""Round-92 C1: merge the L1 hand cases with the w1 seats' cases into one unlabelled frozen-to-be set.

  merge-c1-cases-r92.py OUT SOURCE.json...
A case leaves the set only by a DECLARED scope rule of the tool (its docstring), tested on the case's own bytes —
never by running the tool:
  type    an asked type (with '/', not '-'-leading, not '--version') with a byte outside RFC 6838 restricted-name
  help    an asked type `--help` or `--manual`
  nul     a file holding a NUL byte
  env     XDG_UTILS_REALPATH_BACKEND / XDG_UTILS_DEBUG_LEVEL set, or PATH absent
  trader  an executable named qtxdg-mat / ktraderclient / ktraderclient5 in the fixture
  nousr   a PATH without /usr/bin (the declared assumption: PATH reaches GNU coreutils/grep/gawk)
Duplicate ids keep the first.  Every dropped case is printed with its rule.
"""
import base64
import json
import re
import sys

TYPE = re.compile(r"[A-Za-z0-9!#$&^_.+/-]+")


def rule(c: dict) -> str | None:
    for t in c["types"]:
        if t in ("--help", "--manual"):
            return "help"
        if t == "--version" or t == "" or t.startswith("-") or "/" not in t:
            continue
        if not TYPE.fullmatch(t):
            return "type"
    env = c["env"]
    if "PATH" not in env or env.get("XDG_UTILS_REALPATH_BACKEND") or env.get("XDG_UTILS_DEBUG_LEVEL"):
        return "env"
    if "/usr/bin" not in env["PATH"].split(":"):
        return "nousr"
    for rel, spec in c.get("files", {}).items():
        data = None
        if "b64" in spec:
            data = base64.b64decode(spec["b64"])
        elif "text" in spec:
            data = spec["text"].encode("utf-8", "surrogateescape")
        if data is not None and b"\0" in data:
            return "nul"
        if rel.rsplit("/", 1)[-1] in ("qtxdg-mat", "ktraderclient", "ktraderclient5"):
            return "trader"
    return None


def main() -> int:
    out, srcs = sys.argv[1], sys.argv[2:]
    seen: set[str] = set()
    cases = []
    dropped = {}
    for src in srcs:
        doc = json.load(open(src, encoding="utf-8"))
        for c in doc["cases"]:
            if c["id"] in seen:
                print(f"duplicate-id {c['id']} in {src}: kept the first")
                continue
            seen.add(c["id"])
            r = rule(c)
            if r:
                dropped[r] = dropped.get(r, 0) + 1
                print(f"out-of-scope {r} {c['id']}")
                continue
            c = {k: v for k, v in c.items() if k != "expect"}
            c.setdefault("group", c["id"].split("-")[0])
            cases.append(c)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"cases": cases}, fh, indent=1, ensure_ascii=True)
        fh.write("\n")
    print(f"merged {len(cases)} cases; dropped {dropped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
