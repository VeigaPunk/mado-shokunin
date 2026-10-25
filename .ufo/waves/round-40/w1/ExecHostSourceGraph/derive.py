#!/usr/bin/env python3
"""Independent derivation of the host Hyprland option-declaration graph.

Walks ~/.config/hypr/hyprland.conf depth-first in source order, expanding every
`source =` (glob-aware, ~ expanded) at the point it appears, tracking hyprlang
variables ($name) at use time and category nesting via braces. Records every
`key = value` declaration with its dotted option path, file:line and the value
exactly as written, plus the value after variable expansion.

No use of tools/mado-options.py. Standard library only. Read-only on the host tree.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.expanduser("~/.config/hypr/hyprland.conf")

# Directives that are keywords in Hyprland's config grammar, not option keys.
KEYWORDS = {
    "source", "exec", "exec-once", "exec-shutdown", "env", "monitor", "bind",
    "bindm", "bindl", "binde", "bindr", "bindn", "bindt", "unbind", "submap",
    "windowrule", "layerrule", "workspace", "bezier", "animation", "plugin",
    "permission", "hyprlang", "blurls", "debug:log_level", "cursor:no_hardware_cursors",
}

# Rule blocks: their members are rule fields, not config options.
RULE_BLOCKS = {"windowrule", "layerrule"}
# bind/bindd/bindmd/bindeld/... and unbind: keybinding directives, not options.
BIND_RE = re.compile(r"^(?:un)?bind[a-z]*$")

DECL_RE = re.compile(r"^\s*([A-Za-z0-9_.:-]+)\s*=\s*(.*)$")
VAR_RE = re.compile(r"^\s*\$([A-Za-z0-9_]+)\s*=\s*(.*)$")
VAR_USE = re.compile(r"\$([A-Za-z0-9_]+)")
BLOCK_OPEN = re.compile(r"^\s*([A-Za-z0-9_.:-]+)\s*\{\s*(?:#.*)?$")
BLOCK_CLOSE = re.compile(r"^\s*\}\s*(?:#.*)?$")


def strip_comment(line):
    out, i, inq = [], 0, None
    while i < len(line):
        c = line[i]
        if inq:
            out.append(c)
            if c == inq:
                inq = None
        elif c in "\"'":
            inq = c
            out.append(c)
        elif c == "#":
            break
        else:
            out.append(c)
        i += 1
    return "".join(out).rstrip()


def expand(value, variables):
    """hyprlang variable substitution: iterative until fixpoint, variables defined
    earlier in the walk are visible; unknown variables are left verbatim."""
    cur = value
    for _ in range(16):
        new = VAR_USE.sub(lambda m: variables.get(m.group(1), m.group(0)), cur)
        if new == cur:
            break
        cur = new
    return cur


class Walker:
    def __init__(self):
        self.variables = {}
        self.stack = []            # category path components
        self.decls = []            # (order, key, file, line, raw, expanded)
        self.files = []            # walked files in order
        self.directives = []       # non-option keyword declarations (for the audit)
        self.cycles = []
        self.order = 0
        self.excluded = {"bind": 0, "rule-field": 0, "keyword": {}}

    def key_of(self, name):
        parts = [p for p in self.stack if p]
        return ":".join(parts + [name]) if parts else name

    def walk(self, path, depth=0, parent=None):
        real = os.path.realpath(path)
        if depth > 32:
            self.cycles.append((path, "depth>32"))
            return
        try:
            with open(real, "r", encoding="utf-8", errors="surrogateescape") as fh:
                lines = fh.read().splitlines()
        except OSError as exc:
            self.files.append({"path": path, "error": str(exc)})
            return
        self.files.append({"path": path, "real": real, "lines": len(lines), "depth": depth})
        for lineno, rawline in enumerate(lines, 1):
            line = strip_comment(rawline)
            if not line.strip():
                continue
            m = VAR_RE.match(line)
            if m:
                self.variables[m.group(1)] = expand(m.group(2).strip(), self.variables)
                continue
            m = BLOCK_OPEN.match(line)
            if m and not DECL_RE.match(line):
                self.stack.append(m.group(1))
                continue
            if BLOCK_CLOSE.match(line):
                if self.stack:
                    self.stack.pop()
                else:
                    self.directives.append(("unbalanced-close", path, lineno, line.strip()))
                continue
            m = DECL_RE.match(line)
            if not m:
                self.directives.append(("unparsed", path, lineno, line.strip()))
                continue
            name, value = m.group(1), m.group(2).strip()
            if BIND_RE.match(name):
                self.excluded["bind"] += 1
            if set(self.stack) & RULE_BLOCKS:
                self.excluded["rule-field"] += 1
            if name in KEYWORDS or BIND_RE.match(name) or (set(self.stack) & RULE_BLOCKS):
                self.excluded["keyword"][name] = self.excluded["keyword"].get(name, 0) + 1
                if name == "source":
                    target = expand(value, self.variables)
                    expanded = os.path.expanduser(target)
                    if not os.path.isabs(expanded) and parent:
                        expanded = os.path.join(os.path.dirname(parent), expanded)
                    matches = sorted(glob.glob(expanded)) if any(c in expanded for c in "*?[") else (
                        [expanded] if os.path.exists(expanded) else [])
                    self.directives.append(("source", path, lineno, target, matches))
                    for sub in matches:
                        self.walk(sub, depth + 1, real)
                else:
                    self.directives.append((name, path, lineno, value))
                continue
            self.order += 1
            self.decls.append({
                "order": self.order,
                "key": self.key_of(name),
                "file": path,
                "line": lineno,
                "raw": value,
                "expanded": expand(value, self.variables),
            })


def main():
    w = Walker()
    w.walk(ROOT, 0, None)
    dupes = {}
    for d in w.decls:
        dupes.setdefault(d["key"], []).append(d)
    out = {
        "root": ROOT,
        "files": w.files,
        "variables_final": w.variables,
        "n_declarations": len(w.decls),
        "n_distinct_keys": len(dupes),
        "duplicates": {k: v for k, v in sorted(dupes.items()) if len(v) > 1},
        "declarations": w.decls,
        "directive_kinds": sorted({d[0] for d in w.directives}),
        "unparsed": [d for d in w.directives if d[0] in ("unparsed", "unbalanced-close")],
        "sources": [d for d in w.directives if d[0] == "source"],
        "excluded": w.excluded,
    }
    json.dump(out, sys.stdout, indent=1)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
