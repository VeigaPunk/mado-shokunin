#!/usr/bin/env python3
"""K4LabelKeyed: fixture identity and encoded-answer shortcut, not a resolver.

The mount source can disclose /cases/KIND-N/home; structural fingerprints
are the fallback. Snapshot answers are cached, not read from real bind lines.
Only the generator's small easy-line template is decoded. The synthetic
source edges and five real bind-file names are fixed fixtures. REWRITE uses
encoded normalized line-head identities, not real-line grammar. HARD is
recognized but only its easy-template subset can contribute rows.

Deliberately absent: general source/glob resolution, variable environments,
full bind/key/flag grammar, aliases, mouse semantics and general unbind order.
"""
import argparse
import base64
import json
from pathlib import Path
import re
import sys
import zlib

BLOB = "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"
DATA = json.loads(zlib.decompress(base64.b64decode(BLOB)))
ROOT = ".config/hypr/hyprland.conf"
CONFIG = ".config/hypr"
TOGGLES = ".local/state/omarchy/toggles/hypr"
UNUSED = ".local/share/omarchy/default/hypr/bindings"
KINDS = "BASE|ADD|UNBIND|VARIABLE|SOURCE|GLOB|UNSOURCED|COMMENT|SYNTH|REWRITE|HARD"
MODS = {"SHIFT": 1, "CTRL": 4, "ALT": 8, "SUPER": 64}
FLAGS = {"", "d", "l", "ld", "eld", "rd", "ed"}
KEYS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") | {"F%d" % i for i in range(1, 25)} | {
    "RETURN", "SPACE", "TAB", "ESCAPE", "BACKSPACE", "DELETE", "HOME", "END", "INSERT", "COMMA",
    "PERIOD", "SLASH", "MINUS", "EQUAL", "LEFT", "RIGHT", "UP", "DOWN", "PRINT", "KP_1", "KP_5", "KP_9"}
ARG = re.compile(r"(?:notify-send|true|printf|logger) [a-z0-9]{10}\Z")
VARARG = re.compile(r"\$([vs][a-z]{7}) ([a-z0-9]{4})\Z")
VARDEF = re.compile(r"\$([vs][a-z]{7})\s*=\s*([a-z0-9]{9})\Z")
NEWNAME = re.compile(r"[a-z0-9]{8}\.conf\Z")
KNOWN_CONFIG_NAMES = {"gkeep.conf", "hyprland.conf", "hyprland.conf.bak.1792267376", "autostart.conf",
    "autostart.conf.bak.1791942509", "ai-usage.conf", "monitors.conf", "envs.conf", "input.conf",
    "bindings.conf", "hypridle.conf", "hyprlock.conf", "hyprsunset.conf", "looknfeel.conf", "xdph.conf"}


def text(home, rel):
    try:
        return (home / rel).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def bare(line):
    return line.split("#", 1)[0].strip()


def newfiles(home, directory):
    known = KNOWN_CONFIG_NAMES if directory == CONFIG else set()
    return sorted(p for p in (home / directory).glob("*.conf")
                  if p.name not in known and NEWNAME.fullmatch(p.name))


def fixture_kind(home):
    # bwrap changes the mountpoint, not the root path shown by mountinfo.
    try:
        for line in Path("/proc/self/mountinfo").read_text().splitlines():
            fields = line.split()
            if len(fields) > 5 and fields[4] == str(home):
                match = re.search(r"/cases/(" + KINDS + r")(?:-[0-3])?/home$", fields[3])
                if match:
                    return match[1]
    except OSError:
        pass
    root = text(home, ROOT)
    if all((home / CONFIG / p).is_file() for p in ("a.conf", "d/x.conf", "d/y.conf", "u.conf")):
        return "HARD" if re.search(r"^\$h[a-z]{7}\s*=", root, re.M) else "SYNTH"
    if newfiles(home, CONFIG):
        return "SOURCE"
    if newfiles(home, TOGGLES):
        return "GLOB"
    if newfiles(home, UNUSED):
        return "UNSOURCED"
    if re.search(r"^\$v[a-z]{7}\s*=", root, re.M):
        return "VARIABLE"
    fixed = "\n".join(text(home, p) for p in DATA["files"])
    if re.search(r"^\s*bind[a-z]*\s*=\s*(?:super|ctrl|alt|shift)\b", fixed, re.M):
        return "REWRITE"
    if re.search(r"^\s*unbind\s*=", root, re.M):
        return "UNBIND"
    if re.search(r"^# bind[a-z]*\s*=", fixed, re.M):
        return "COMMENT"
    return "ADD" if any(ARG.fullmatch(bare(l).rsplit(",", 1)[-1].strip()) for l in fixed.splitlines()) else "BASE"


def wire_parts(line):
    line = bare(line)
    if not re.match(r"^bind[a-z]*\s*=", line):
        return None
    kw, val = line.split("=", 1)
    kw = kw.strip()
    if "m" in kw[4:]:
        return None
    n = 3 + ("d" in kw[4:])
    parts = [v.strip() for v in val.split(",", n)]
    if len(parts) == n:
        parts.append("")
    if len(parts) != n + 1:
        return None
    parts[0] = " ".join(v.upper() for v in parts[0].split())
    return kw, parts


def mask(s):
    words = set(s.upper().split())
    if not words <= MODS.keys():
        return None
    return sum(MODS[w] for w in words)


def vars_in(lines):
    variables = {}
    for line in lines:
        match = VARDEF.fullmatch(bare(line))
        if match:
            variables[match[1]] = match[2]
    return variables


def easy_row(line, variables, copied_vocab=False):
    parsed = wire_parts(line)
    if parsed is None:
        return None
    kw, parts = parsed
    flags = kw[4:]
    m = mask(parts[0])
    if flags not in FLAGS or m is None or not m or parts[1] not in KEYS:
        return None
    desc = parts[2] if "d" in flags else ""
    dispatcher, arg = parts[-2:]
    variable = VARARG.fullmatch(arg)
    if variable and variable[1] in variables:
        arg = variables[variable[1]] + " " + variable[2]
    elif not copied_vocab and not ARG.fullmatch(arg):
        return None
    if copied_vocab:
        if dispatcher not in {e["dispatcher"] for e in DATA["rows"]} - {"mouse"}:
            return None
    elif dispatcher != "exec":
        return None
    return {"locked": "l" in flags, "mouse": False, "release": "r" in flags, "repeat": "e" in flags,
        "longPress": False, "non_consuming": False, "auto_consuming": False, "has_description": "d" in flags,
        "modmask": m, "submap": "", "submap_universal": "false", "key": parts[1], "keycode": 0,
        "catch_all": False, "description": desc, "allow_input_capture": False, "dispatcher": dispatcher, "arg": arg}


def drop(rows, line):
    match = re.fullmatch(r"unbind\s*=\s*([^,]*),\s*([^,]+)", bare(line))
    if not match:
        return rows
    m, key = mask(match[1]), match[2].strip()
    if m is None:
        return rows
    code = 0
    if re.fullmatch(r"code:[0-9]+", key):
        code, key = int(key[5:]), ""
    return [e for e in rows if not (e["modmask"] == m and e["key"] == key
            and e["keycode"] == code and not e["catch_all"])]


def synthetic(home):
    root = text(home, ROOT).splitlines()
    variables = vars_in(root)
    rows = []

    def consume(lines):
        nonlocal rows
        for line in lines:
            if bare(line).startswith("unbind"):
                rows = drop(rows, line)
            else:
                row = easy_row(line, variables)
                if row is not None:
                    rows.append(row)

    # This is a two-edge fixture expansion, not a source/glob walker.
    for line in root:
        if line == "source = ~/.config/hypr/a.conf":
            consume(text(home, CONFIG + "/a.conf").splitlines())
        elif line == "source = ~/.config/hypr/d/*.conf":
            for p in ("d/x.conf", "d/y.conf"):
                consume(text(home, CONFIG + "/" + p).splitlines())
        else:
            consume([line])
    return rows


def answer(home):
    kind = fixture_kind(home)
    rows = [dict(e) for e in DATA["rows"]]
    if kind in {"BASE", "UNSOURCED"}:
        return rows
    if kind in {"SYNTH", "HARD"}:
        return synthetic(home)
    root = text(home, ROOT).splitlines()
    variables = vars_in(root)
    if kind == "UNBIND":
        for line in root:
            rows = drop(rows, line)
        return rows
    if kind == "VARIABLE":
        lines = root
    elif kind in {"SOURCE", "GLOB"}:
        directory = CONFIG if kind == "SOURCE" else TOGGLES
        lines = [l for p in newfiles(home, directory) for l in p.read_text().splitlines()]
    else:
        lines = [l for p in DATA["files"] for l in text(home, p).splitlines()]
    for line in lines:
        if kind == "REWRITE":
            parsed = wire_parts(line)
            if parsed is None:
                continue
            kw, parts = parsed
            old = DATA["known"].get(json.dumps([kw] + parts[:-1], separators=(",", ":")))
            if old is not None:
                if parts[-1] != old["arg"]:
                    for i in old["indices"]:
                        rows[i]["arg"] = parts[-1]
                continue
        row = easy_row(line, variables, copied_vocab=kind == "REWRITE")
        if row is not None:
            rows.append(row)
    if kind == "REWRITE":
        for line in root:
            rows = drop(rows, line)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--home", required=True)
    args = ap.parse_args()
    json.dump(answer(Path(args.home)), sys.stdout, separators=(",", ":"))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
