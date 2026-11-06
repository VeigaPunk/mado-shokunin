#!/usr/bin/env python3
"""Round-91 C1 fresh-leg fuzzer: unlabelled MIME cases (schema mime-cases-r91-v1, group "fresh").

Deterministic: `generate(seed, n)` is a pure function of the integer seed, so the
measurement-time fresh leg (`seed` = the first 8 hex digits of the measured
tool's sha256) is reproducible but unknown to the tool under test.

Each case randomises, over the fixture-only XDG roots:
  * 1-3 XDG_CONFIG_DIRS entries and 1-3 XDG_DATA_DIRS entries (plus the user
    config/data homes);
  * XDG_CURRENT_DESKTOP: valid tokens, an invalid token, empty tokens, unset;
  * the PATH list (with or without /usr/bin, with or without the fixture bin/);
  * [Default Applications] / [Added Associations] / [Removed Associations] in
    mimeapps.list, each dir's `<desktop>-mimeapps.list`, defaults.list and
    mimeinfo.cache across the config and data dirs;
  * desktop files: valid, Hidden=true/1/false, Type=Link, missing TryExec
    program, missing Exec program, unbalanced-quote Exec, no Exec, empty Exec,
    a file GKeyFile cannot parse, a first group that is not [Desktop Entry],
    and files one directory deep (id `<sub>-<name>.desktop`);
  * aliases/subclasses text files (with and without a final newline);
  * occasional malformed list lines (junk line, key before any group, group
    trailing garbage, bad escape in a value, locale-suffixed key, CRLF);
  * 1-4 asked MIME types from a small vocabulary, so alias/parent collisions
    happen.

Stdlib only.  `python3 fuzz-gen-r91.py SEED N` prints
{"schema": "mime-cases-r91-v1", "cases": [...]} on stdout.  Labels come only
from controls/mime-oracle-r91.py.
"""
from __future__ import annotations

import json
import random
import sys

SCHEMA = "mime-cases-r91-v1"

DESKTOPS = [
    None, "", "Hyprland", "GNOME", "KDE",
    "Hyprland:GNOME", "GNOME:Hyprland", "GNOME:Hyprland:KDE",
    "Hypr/land:GNOME", "::GNOME", "KDE::bad/x", "X-Y_Z", "hyprland",
    "Hyprland:", ":", "KDE:hyprland",
]

TYPES = [
    "text/plain", "image/png", "application/pdf", "text/x-c", "app/x",
    "text/x-old", "x-scheme-handler/http", "video/mp4", "inode/directory",
    "application/octet-stream", "text/x-doc", "audio/mpeg",
]

APP_IDS = ["a.desktop", "b.desktop", "c.desktop", "d.desktop"]

PATHS = [
    ["bin", "/usr/bin"], ["bin", "/usr/bin"], ["bin", "/usr/bin"],
    ["/usr/bin"], ["bin"],
]

STATES = [
    "valid", "valid", "valid", "valid",
    "hidden", "hidden-1", "hidden-false",
    "link", "tryexec-missing", "exec-missing", "bad-quote", "no-exec",
    "empty-exec", "garbage", "other-group-first", "tryexec-tool", "exec-tool",
    "path-tryexec-work", "path-tryexec-bin", "path-exec-work", "path-valid",
]
# States that need a fixture program: the desktop file's Path= is the working
# dir GLib searches before PATH (gdesktopappinfo.c :1961-1975).
NEEDED_PROGRAMS = {
    "path-tryexec-work": ["work/wtool"],
    "path-exec-work": ["work/wtool"],
    "path-tryexec-bin": ["bin/btool"],
    "tryexec-tool": ["bin/mado-tool"],
    "exec-tool": ["bin/mado-tool"],
}

ALIAS_PAIRS = [
    ("text/x-old", "text/plain"), ("app/x", "app/y"),
    ("text/x-doc", "text/x-c"), ("audio/x-mp3", "audio/mpeg"),
    ("image/x-png", "image/png"),
]
PARENT_PAIRS = [
    ("text/x-c", "text/plain"), ("app/x", "app/y"),
    ("text/x-doc", "application/pdf"), ("video/mp4", "application/octet-stream"),
    ("app/x", "text/plain"), ("text/x-old", "text/x-c"),
]


def _tokens(desktop: str | None) -> list[str]:
    """The desktop tokens GLib accepts (validate_xdg_desktop) and lowercases."""
    if desktop is None:
        return []
    out = []
    for t in desktop.split(":"):
        if t and all(c.isascii() and (c.isalnum() or c in "-_") for c in t):
            out.append(t.lower())
    return out


def _desktop_text(state: str) -> str:
    head = "[Desktop Entry]\n"
    body = "Type=Application\nName=X\n"
    if state == "link":
        return head + "Type=Link\nName=X\nURL=https://example.invalid/\n"
    if state == "other-group-first":
        return "[Other]\nx=1\n" + head + body + "Exec=sh %f\n"
    if state == "valid":
        return head + body + "Exec=sh %f\n"
    if state == "hidden":
        return head + body + "Exec=sh %f\nHidden=true\n"
    if state == "hidden-1":
        return head + body + "Exec=sh %f\nHidden=1\n"
    if state == "hidden-false":
        return head + body + "Exec=sh %f\nHidden=false\n"
    if state == "tryexec-missing":
        return head + body + "TryExec=mado-no-such-prog\nExec=sh %f\n"
    if state == "exec-missing":
        return head + body + "Exec=mado-no-such-prog %u\n"
    if state == "bad-quote":
        return head + body + 'Exec=sh "%f\n'
    if state == "no-exec":
        return head + body
    if state == "empty-exec":
        return head + body + "Exec=\n"
    if state == "garbage":
        return head + body + "Exec=sh %f\ngarbage line\n"
    if state == "tryexec-tool":
        return head + body + "TryExec=mado-tool\nExec=sh %f\n"
    if state == "exec-tool":
        return head + body + "Exec=mado-tool %f\n"
    if state == "path-tryexec-work":
        return head + body + "Path=work\nTryExec=wtool\nExec=sh %f\n"
    if state == "path-tryexec-bin":
        return head + body + "Path=work\nTryExec=btool\nExec=sh %f\n"
    if state == "path-exec-work":
        return head + body + "Path=work\nExec=wtool %f\n"
    if state == "path-valid":
        return head + body + "Path=work\nExec=sh %f\n"
    raise ValueError(state)


def _value(rng: random.Random, ids: list[str]) -> str:
    r = rng.random()
    if r < 0.06:
        return ""
    if r < 0.12:
        return "zz.desktop"
    v = ";".join(rng.sample(ids, rng.randint(1, min(3, len(ids)))))
    if rng.random() < 0.30:
        v += ";"
    if rng.random() < 0.06:
        v += " "
    return v


def _key_line(rng: random.Random, t: str, ids: list[str]) -> str:
    if rng.random() < 0.06:
        return f"{t}={rng.choice(ids)}\\q.desktop"
    sep = rng.choices(["=", " = ", "   =   ", "=\t"], weights=[80, 10, 5, 5])[0]
    key = t + rng.choice(["[de]", "[de_DE.UTF-8]", "[C]"]) if rng.random() < 0.10 else t
    return f"{key}{sep}{_value(rng, ids)}"


def _kinds(rng: random.Random, default_p: float = 0.60, added_p: float = 0.50,
           removed_p: float = 0.40) -> list[str]:
    out = []
    if rng.random() < default_p:
        out.append("Default Applications")
    if rng.random() < added_p:
        out.append("Added Associations")
    if rng.random() < removed_p:
        out.append("Removed Associations")
    if not out:
        out.append("Default Applications")
    return out


MALFORMED = ["none"] * 12 + ["junk-line", "key-before-group", "group-trailing",
                             "encoding", "duplicate-group"]


def _groups_text(rng: random.Random, asked: list[str], ids: list[str],
                 kinds: list[str], malformed: str, collide: tuple[str, str] | None = None) -> str:
    blocks: list[tuple[str | None, list[str]]] = []
    for name in kinds:
        keys = rng.sample(asked, rng.randint(1, min(2, len(asked))))
        lines = []
        for t in keys:
            lines.append(_key_line(rng, t, ids))
            if rng.random() < 0.05:
                lines.append(_key_line(rng, t, ids))  # duplicate key: last value wins
        blocks.append((name, lines))
    if collide and blocks and rng.random() < 0.55:
        # a duplicate key whose two names unalias to one type: GLib's
        # g_key_file_get_keys returns the key at *both* file positions, while the
        # last value wins in the lookup map (gkeyfile.c).
        src, dst = collide
        picks = rng.sample(ids, min(3, len(ids)))
        while len(picks) < 3:
            picks.append(picks[-1])
        name, lines = blocks[0]
        blocks[0] = (name, lines + [f"{src}={picks[0]}", f"{dst}={picks[1]}", f"{src}={picks[2]}"])
    if malformed == "junk-line":
        blocks.append((None, ["garbage line"]))
    elif malformed == "key-before-group":
        blocks.insert(0, (None, [f"text/plain={rng.choice(ids)}"]))
    elif malformed == "group-trailing" and blocks:
        name, lines = blocks[0]
        blocks[0] = (name + " x", lines)
    elif malformed == "encoding":
        blocks.insert(0, ("Default Applications", ["Encoding=ISO-8859-1"]))
    elif malformed == "duplicate-group" and blocks:
        blocks.append(blocks[0])
    out = []
    for name, lines in blocks:
        if name is not None:
            out.append(f"[{name}]\n")
        out.append("".join(line + "\n" for line in lines))
    return "".join(out)


def _cache_text(rng: random.Random, asked: list[str], ids: list[str]) -> str:
    lines = []
    for t in rng.sample(asked, rng.randint(1, min(2, len(asked)))):
        v = ";".join(rng.sample(ids, rng.randint(1, min(3, len(ids))))) + ";"
        lines.append(f"{t}={v}")
    text = "[MIME Cache]\n" + "".join(line + "\n" for line in lines)
    if rng.random() < 0.20:
        text += "[Removed Associations]\n" + f"{rng.choice(asked)}={rng.choice(ids)}\n"
    return text


def _defaults_text(rng: random.Random, asked: list[str], ids: list[str]) -> str:
    text = "[Default Applications]\n" + f"{rng.choice(asked)}={_value(rng, ids)}\n"
    if rng.random() < 0.25:
        text += "[Added Associations]\n" + f"{rng.choice(asked)}={rng.choice(ids)}\n"
    return text


def _pairs_text(rng: random.Random, pairs: list[tuple[str, str]]) -> str:
    text = "".join(f"{a} {b}\n" for a, b in pairs)
    if rng.random() < 0.15:
        text = text.rstrip("\n")  # no final newline: xdgmime chops the last byte
    if rng.random() < 0.10:
        text += "malformed-no-space\n"
    if rng.random() < 0.08:
        text += "# comment line\n"
    return text


def _make_case(rng: random.Random, seed: int, k: int) -> dict:
    n_cfg = rng.randint(1, 3)
    n_data = rng.randint(1, 3)
    config_dirs = [f"etc{i}" for i in range(n_cfg)]
    data_dirs = [f"sys{i}" for i in range(n_data)]
    droots = ["home"] + data_dirs
    roots = {"config_home": "cfg", "config_dirs": config_dirs,
             "data_home": "home", "data_dirs": data_dirs}
    desktop = rng.choice(DESKTOPS)
    tokens = _tokens(desktop)
    path = list(rng.choice(PATHS))

    files: dict[str, object] = {}

    ids = rng.sample(APP_IDS, rng.randint(2, 4))
    ref = {a: a for a in ids}
    if rng.random() < 0.35:
        ids.append("vendor/e.desktop")
        ref["vendor/e.desktop"] = "vendor-e.desktop"
    list_ids = [ref[a] for a in ids]

    def place(aid: str, dr: str) -> None:
        state = rng.choice(STATES)
        files[f"{dr}/applications/{aid}"] = _desktop_text(state)
        for prog in NEEDED_PROGRAMS.get(state, []):
            files[prog] = {"text": "#!/bin/sh\n", "exec": True}

    for aid in ids:
        ndest = 1 if rng.random() < 0.70 else 2
        for di in rng.sample(range(len(droots)), min(ndest, len(droots))):
            place(aid, droots[di])
    if "vendor/e.desktop" in ids and rng.random() < 0.35:
        # same desktop id as the subdirectory file, in another data dir
        place("vendor-e.desktop", rng.choice(droots))

    asked = rng.sample(TYPES, rng.randint(1, 4))
    collide = rng.choice(ALIAS_PAIRS) if rng.random() < 0.40 else None
    if collide is not None:
        for member in collide:
            if member not in asked:
                if len(asked) < 4:
                    asked.append(member)
                else:
                    asked[rng.randrange(len(asked))] = member

    for cd in ["cfg"] + config_dirs:
        if rng.random() < 0.80:
            text = _groups_text(rng, asked, list_ids, _kinds(rng), rng.choice(MALFORMED), collide)
            if rng.random() < 0.07:
                text = text.replace("\n", "\r\n")
            files[f"{cd}/mimeapps.list"] = text
        for tok in tokens:
            if rng.random() < 0.35:
                text = _groups_text(rng, asked, list_ids,
                                    _kinds(rng, 0.70, 0.30, 0.30), "none", collide)
                files[f"{cd}/{tok}-mimeapps.list"] = text

    for dr in droots:
        appdir = f"{dr}/applications"
        if rng.random() < 0.50:
            text = _groups_text(rng, asked, list_ids, _kinds(rng), rng.choice(MALFORMED), collide)
            files[f"{appdir}/mimeapps.list"] = text
        if rng.random() < 0.40:
            files[f"{appdir}/defaults.list"] = _defaults_text(rng, asked, list_ids)
        if rng.random() < 0.60:
            files[f"{appdir}/mimeinfo.cache"] = _cache_text(rng, asked, list_ids)
        for tok in tokens:
            if rng.random() < 0.15:
                files[f"{appdir}/{tok}-mimeapps.list"] = _groups_text(
                    rng, asked, list_ids, ["Default Applications"], "none", collide)

    if collide is not None or rng.random() < 0.60:
        pairs = rng.sample(ALIAS_PAIRS, rng.randint(1, 2))
        if collide is not None and collide not in pairs:
            pairs[0] = collide
        text = _pairs_text(rng, pairs)
        if rng.random() < 0.12:
            # longer than xdgmime's fgets(line, 255): the line splits into two pairs
            text += "app/" + "x" * rng.choice([80, 240, 250]) + " text/plain\n"
        pick = rng.sample(droots, 1) if rng.random() < 0.70 else rng.sample(droots, min(2, len(droots)))
        for r in pick:
            files[f"{r}/mime/aliases"] = text
        # Deliberately NO duplicate alias source in two dirs: the text-mode
        # match is bsearch over a qsort'ed array (xdgmimealias.c:94,147) and
        # for equal keys that order is unspecified, so such a case has no
        # oracle answer the tool could be required to reproduce.
    if rng.random() < 0.60:
        text = _pairs_text(rng, rng.sample(PARENT_PAIRS, rng.randint(1, 2)))
        pick = rng.sample(droots, 1) if rng.random() < 0.70 else rng.sample(droots, min(2, len(droots)))
        for r in pick:
            files[f"{r}/mime/subclasses"] = text

    return {
        "id": f"fz-{seed}-{k:03d}",
        "group": "fresh",
        "desktop": desktop,
        "path": path,
        "roots": roots,
        "files": files,
        "types": asked,
    }


def generate(seed: int, n: int) -> list[dict]:
    """Return n deterministic, unlabelled cases for the integer seed."""
    rng = random.Random(seed)
    return [_make_case(rng, seed, k) for k in range(n)]


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: fuzz-gen-r91.py SEED N", file=sys.stderr)
        return 2
    seed, n = int(argv[1]), int(argv[2])
    json.dump({"schema": SCHEMA, "cases": generate(seed, n)}, sys.stdout, indent=1, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
