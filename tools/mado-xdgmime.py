#!/usr/bin/env python3
"""mado-xdgmime — what `xdg-mime query default TYPE` (xdg-utils 1.2.1) prints, without running it.

On Hyprland (and any session whose XDG_CURRENT_DESKTOP xdg-utils does not know) `xdg-open` asks
`xdg-mime query default TYPE` which `.desktop` file opens a type, and xdg-mime answers with its own
shell resolver (`defapp_generic`), not GLib's.  This tool replays that resolver over files only:

  1. `[Default Applications]` in `<dir>/<desktop>-mimeapps.list` then `<dir>/mimeapps.list`, for every
     desktop of XDG_CURRENT_DESKTOP (lowercased, `:`-split), over $XDG_CONFIG_HOME, $XDG_CONFIG_DIRS,
     then `$XDG_DATA_HOME/applications`, `$XDG_DATA_DIRS/applications`; the first line that starts with
     `TYPE=` in a file wins; its `;`-list is tried in order and the first id whose desktop file's first
     `Exec` word resolves (desktop_file_to_binary: vendor-dash split, `command -v`, `[ -e ]`) is printed;
  2. else the first `grep "TYPE="` line (a BRE, unanchored) of `<prefix>defaults.list` /
     `<prefix>mimeinfo.cache` per data dir, with prefix $XDG_MENU_PREFIX then "", no install check;
  3. else the `.desktop` file under `<data dir>/applications` (recursive) whose text contains
     `TYPE;` (a BRE) with the highest `InitialPreference` (first wins ties; absent = 0);
  4. else nothing (exit 0).
Shell semantics are modelled where the resolver relies on them: IFS field splitting and pathname
expansion of unquoted words (C locale, relative to the working directory), `read` without -r,
`echo` options, bash `command -v` (keywords, builtins and xdg-mime's own functions print their bare
name), GNU grep BRE, gawk `-v` escapes, bash `test -gt` integers, coreutils `basename`.

Scope (refused with rc 2 `unsupported`, never guessed): an asked type with a character outside RFC 6838
restricted-name ([A-Za-z0-9!#$&^_.+-] and the slash), an LXQt session with `qtxdg-mat` on PATH, a KDE
session (KDE_SESSION_VERSION 4/5) with `ktraderclient`/`ktraderclient5` on PATH, XDG_UTILS_REALPATH_BACKEND
set, XDG_UTILS_DEBUG_LEVEL set, a read file holding a NUL byte, `--help`/`--manual` as the type (xdg-mime prints its
usage text or manual page), PATH unset (bash's compiled-in default path).  A refusal ends the whole invocation (no
answer for any type named with it).  Assumed (not modelled): D-Bus has no
org.gnome.SessionManager owner and no X root window says xfce (true on a Hyprland session and with no
session bus); PATH reaches GNU coreutils/grep/gawk under their own names.

Read-only: the tool opens files and lists directories; it writes nothing and runs no program (`--selftest` writes
only ephemeral fixtures inside a private temporary directory it removes on exit).

Usage:
  mado-xdgmime.py [--json] [--cwd DIR] [--env NAME=VALUE ...] [--from-environ] [--] TYPE...
  mado-xdgmime.py --selftest      (12 checks whose expectations are installed-xdg-mime labels of round-92 cases)
`--env` sets one variable of the resolved environment (repeatable); `--from-environ` starts from this
process's environment instead of an empty one.  Text output: `TYPE<TAB>APP` or `TYPE<TAB>-` (no
answer); `--json`: {"results": [{"type", "default", "rc"}]} where default is the printed line (None when
nothing is printed) and rc is xdg-mime's exit status.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys

KEYWORDS = set("if then else elif fi case esac for select while until do done in function time { } ! [[ ]] coproc".split())
BUILTINS = set((". : [ alias bg bind break builtin caller cd command compgen complete compopt continue declare dirs "
                "disown echo enable eval exec exit export false fc fg getopts hash help history jobs kill let local "
                "logout mapfile popd printf pushd pwd read readarray readonly return set shift shopt source suspend "
                "test times trap true type typeset ulimit umask unalias unset wait").split())
FUNCTIONS = set(("manualpage usage DEBUG first_word binary_to_desktop_file desktop_file_to_binary exit_success "
                 "exit_failure_syntax exit_failure_file_missing exit_failure_operation_impossible "
                 "exit_failure_operation_failed exit_failure_file_permission_read exit_failure_file_permission_write "
                 "check_input_file check_vendor_prefix check_output_file check_common_commands detectDE "
                 "kfmclient_fix_exit_code has_display unoption_path xdg_realpath update_kde_cache update_mime_database "
                 "info_kde info_gnome info_lxqt info_generic make_default_kde make_default_lxqt make_default_generic "
                 "search_desktop_file defapp_fallback check_mimeapps_list defapp_generic defapp_kde "
                 "defapp_lxqt").split())
WS = b" \t\n"
EXEC = re.compile(rb"^Exec(\[[^]=]*\])?=")
# RFC 6838 section 4.2 restricted-name characters (plus the '/' xdg-mime requires): the only types modelled.  On these
# bytes the BRE "$MIME=" and gawk -v assignment reduce to: '.' any byte, '^' an anchor only at the start, every other
# byte literal (round-92 w1 R92MExecGrep: stacked quantifiers, intervals, collating classes and unknown gawk escapes
# behave by regex-engine rules this tool does not replay).
TYPE_CHARS = re.compile(rb"[A-Za-z0-9!#$&^_.+/-]+")


class Unsupported(Exception):
    pass


def fs(b: bytes) -> str:
    return os.fsdecode(b)


def bb(s: str) -> bytes:
    return os.fsencode(s)


# ------------------------------------------------------------------ shell word handling
def ifs_split(v: bytes, sep: bytes) -> list[bytes]:
    """Field splitting of an unquoted expansion with a single non-whitespace IFS character."""
    if v == b"":
        return []
    f = v.split(sep)
    if f[-1] == b"":
        f.pop()
    return f


def ws_split(v: bytes) -> list[bytes]:
    return [x for x in re.split(rb"[ \t\n]+", v) if x]


_CLASSES = {b"alpha": rb"A-Za-z", b"digit": rb"0-9", b"alnum": rb"A-Za-z0-9", b"upper": rb"A-Z", b"lower": rb"a-z",
            b"space": rb" \t\n\r\x0b\x0c", b"blank": rb" \t", b"punct": rb"!-/:-@\[-`{-~", b"xdigit": rb"0-9A-Fa-f",
            b"cntrl": rb"\x00-\x1f\x7f", b"print": rb"\x20-\x7e", b"graph": rb"\x21-\x7e", b"word": rb"A-Za-z0-9_"}


def _bracket(p: bytes, i: int, negchars: bytes) -> tuple[bytes, int] | None:
    """Parse a bracket expression starting after '[' at p[i]; return (python class, index after ']')."""
    j = i
    neg = False
    if j < len(p) and p[j:j + 1] in [bytes([c]) for c in negchars]:
        neg = True
        j += 1
    out = b""
    first = True
    while j < len(p):
        c = p[j:j + 1]
        if c == b"]" and not first:
            return (b"[" + (b"^" if neg else b"") + out + b"]", j + 1)
        first = False
        if c == b"[" and p[j + 1:j + 2] == b":":
            k = p.find(b":]", j + 2)
            if k < 0:
                out += re.escape(c)
                j += 1
                continue
            name = p[j + 2:k]
            if name not in _CLASSES:
                return None
            out += _CLASSES[name]
            j = k + 2
            continue
        if c in (b"\\",) and negchars == b"!^" and j + 1 < len(p):
            out += re.escape(p[j + 1:j + 2])
            j += 2
            continue
        if c == b"-" and out and j + 1 < len(p) and p[j + 1:j + 2] != b"]":
            out += b"-"
            j += 1
            continue
        out += re.escape(c)
        j += 1
    return None


def glob_rx(pat: bytes) -> re.Pattern | None:
    """bash pattern (one path component) -> regex; None when the component has no special char."""
    out = b""
    special = False
    i = 0
    while i < len(pat):
        c = pat[i:i + 1]
        if c == b"\\" and i + 1 < len(pat):
            out += re.escape(pat[i + 1:i + 2])
            i += 2
            continue
        if c == b"*":
            out += b".*"
            special = True
        elif c == b"?":
            out += b"."
            special = True
        elif c == b"[":
            r = _bracket(pat, i + 1, b"!^")
            if r is None:
                out += re.escape(c)
            else:
                out += r[0]
                i = r[1]
                special = True
                continue
        else:
            out += re.escape(c)
        i += 1
    if not special:
        return None
    try:
        return re.compile(b"(?s)" + out + b"\\Z")
    except re.error:
        return re.compile(b"(?!)")  # a reversed range: bash matches nothing, the word stays (R92MExecShell D1)


def pathexp(word: bytes, cwd: str) -> list[bytes]:
    """bash pathname expansion of one field (C locale, no nullglob, globskipdots).

    A backslash quotes the next byte, so a word whose only `*`/`?`/`[` are backslash-quoted is not globbed and stays
    as it is, backslashes included (round-92 w1 R92MReviewC1 F2)."""
    if not re.search(rb"(?:^|[^\\])(?:\\\\)*[*?[]", word):
        return [word]
    absolute = word.startswith(b"/")
    comps = word.split(b"/")
    if absolute:
        comps = comps[1:]
    cands = [b"/" if absolute else b""]
    for idx, comp in enumerate(comps):
        last = idx == len(comps) - 1
        nxt = []
        if comp == b"":
            for c in cands:
                if c in (b"", b"/") or os.path.isdir(os.path.join(cwd, fs(c))):
                    nxt.append(c if c.endswith(b"/") or c == b"" else c + b"/")
            cands = nxt
            continue
        rx = glob_rx(comp)
        for c in cands:
            base = os.path.join(cwd, fs(c)) if c else cwd
            if rx is None:
                lit = re.sub(rb"\\(.)", rb"\1", comp)
                p = c + (b"" if c.endswith(b"/") or c == b"" else b"/") + lit
                if os.path.lexists(os.path.join(cwd, fs(p))):
                    nxt.append(p)
                continue
            try:
                names = sorted(bb(n) for n in os.listdir(base))
            except OSError:
                continue
            for n in names:
                if n in (b".", b".."):
                    continue
                if n.startswith(b".") and not comp.startswith(b"."):
                    continue
                if not rx.match(n):
                    continue
                p = c + (b"" if c.endswith(b"/") or c == b"" else b"/") + n
                if not last and not os.path.isdir(os.path.join(cwd, fs(p))):
                    continue
                nxt.append(p)
        cands = nxt
        if not cands:
            break
    return cands if cands else [word]


def expand(words: list[bytes], cwd: str) -> list[bytes]:
    out = []
    for w in words:
        out += pathexp(w, cwd)
    return out


# ------------------------------------------------------------------ utilities as xdg-mime calls them
def basename(s: bytes) -> bytes:
    if s.startswith(b"-") and s != b"-":
        return b""  # coreutils: an option (or an invalid one) -> no usable output
    if s == b"":
        return b""
    t = s.rstrip(b"/")
    if t == b"":
        return b"/"
    return t.rsplit(b"/", 1)[-1]


def echo_out(arg: bytes) -> bytes:
    """`echo "$x"` in bash: an argument made of -n/-e/-E flags is an option."""
    if re.fullmatch(rb"-[neE]+", arg):
        return b"" if b"n" in arg else b"\n"
    return arg + b"\n"


def cmdsub(b: bytes) -> bytes:
    return b.rstrip(b"\n")


def readfile(path: str) -> bytes | None:
    try:
        st = os.stat(path)
        if stat.S_ISDIR(st.st_mode):
            return None
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError:
        return None
    if b"\0" in data:
        raise Unsupported(f"NUL byte in {path}")
    return data


def lines_of(data: bytes) -> list[bytes]:
    if data == b"":
        return []
    ls = data.split(b"\n")
    if ls[-1] == b"":
        ls.pop()
    return ls


def readable(p: str) -> bool:
    return os.access(p, os.R_OK)


def bre(pat: bytes) -> re.Pattern | None:
    """GNU grep basic regular expression (C locale) -> python bytes regex; None when grep rejects it."""
    out = b""
    i = 0
    at_start = True
    depth = 0
    n = len(pat)
    while i < n:
        c = pat[i:i + 1]
        if c == b"\\":
            if i + 1 >= n:
                return None
            d = pat[i + 1:i + 2]
            i += 2
            if d == b"(":
                out += b"("
                depth += 1
                at_start = True
                continue
            if d == b")":
                if depth == 0:
                    return None
                depth -= 1
                out += b")"
            elif d == b"|":
                out += b"|"
                at_start = True
                continue
            elif d == b"{":
                k = pat.find(b"\\}", i)
                if k < 0 or not re.fullmatch(rb"\d*(,\d*)?", pat[i:k]) or at_start:
                    return None
                out += b"{" + (b"0" if pat[i:k].startswith(b",") else b"") + pat[i:k] + b"}"
                i = k + 2
            elif d in (b"+", b"?"):
                out += b"\\" + d if at_start else d
            elif d == b"w":
                out += rb"[A-Za-z0-9_]"
            elif d == b"W":
                out += rb"[^A-Za-z0-9_]"
            elif d == b"s":
                out += rb"[ \t\n\r\x0b\x0c]"
            elif d == b"S":
                out += rb"[^ \t\n\r\x0b\x0c]"
            elif d == b"b":
                out += rb"\b"
            elif d == b"B":
                out += rb"\B"
            elif d == b"<":
                out += rb"\b(?=[A-Za-z0-9_])"
            elif d == b">":
                out += rb"\b(?<=[A-Za-z0-9_])"
            elif d == b"`":
                out += rb"\A"
            elif d == b"'":
                out += rb"\Z"
            elif d.isdigit() and d != b"0":
                out += b"\\" + d
            else:
                out += re.escape(d)
            at_start = False
            continue
        if c == b"*":
            out += b"\\*" if at_start else b"*"
            at_start = False
            i += 1
            continue
        if c == b"^" and at_start:
            out += b"^"
            i += 1
            continue
        if c == b"$" and (i + 1 == n or pat[i + 1:i + 3] in (b"\\)", b"\\|")):
            out += b"$"
            i += 1
            at_start = False
            continue
        if c == b"[":
            r = _bracket(pat, i + 1, b"^")
            if r is None:
                return None
            out += r[0]
            i = r[1]
            at_start = False
            continue
        if c == b".":
            out += b"."
        else:
            out += re.escape(c)
        at_start = False
        i += 1
    if depth:
        return None
    try:
        return re.compile(out)
    except (re.error, OverflowError):
        return None


def awk_v(s: bytes) -> bytes:
    """gawk -v assignment escape processing."""
    out = b""
    i = 0
    m = {b"n": b"\n", b"t": b"\t", b"r": b"\r", b"\\": b"\\", b'"': b'"', b"/": b"/", b"a": b"\a", b"b": b"\b",
         b"f": b"\f", b"v": b"\v"}
    while i < len(s):
        c = s[i:i + 1]
        if c != b"\\" or i + 1 >= len(s):
            out += c
            i += 1
            continue
        d = s[i + 1:i + 2]
        if d in m:
            out += m[d]
            i += 2
        elif d in b"01234567":
            j = i + 1
            while j < len(s) and j < i + 4 and s[j:j + 1] in b"01234567" and s[j:j + 1] != b"":
                j += 1
            out += bytes([int(s[i + 1:j], 8) & 0xFF])
            i = j
        elif d == b"x":
            j = i + 2
            while j < len(s) and j < i + 4 and s[j:j + 1] != b"" and s[j:j + 1] in b"0123456789abcdefABCDEF":
                j += 1
            if j == i + 2:
                out += b"x"
            else:
                out += bytes([int(s[i + 2:j], 16) & 0xFF])
            i = j
        else:
            out += d  # gawk drops the backslash of an unknown escape (warning on stderr)
            i += 2
    return out


def bash_int(s: bytes) -> int | None:
    """bash `test` integer: optional whitespace, sign, decimal digits, trailing whitespace; int64."""
    m = re.fullmatch(rb"[ \t\n\r\x0b\x0c]*([+-]?)([0-9]+)[ \t\n\r\x0b\x0c]*", s)
    if not m:
        return None
    v = int(m.group(2))
    if m.group(1) == b"-":
        v = -v
    if v > 2 ** 63 - 1 or v < -(2 ** 63):
        return None
    return v


def read_first(text: bytes) -> bytes:
    """`read first rest` (no -r, default IFS) on `text`, then `echo "$first"` captured."""
    chars: list[tuple[int, bool]] = []
    i = 0
    while i < len(text):
        c = text[i]
        if c == 0x5C:
            if i + 1 >= len(text):
                i += 1
                continue
            if text[i + 1] == 0x0A:
                i += 2
                continue
            chars.append((text[i + 1], True))
            i += 2
            continue
        if c == 0x0A:
            break
        chars.append((c, False))
        i += 1
    k = 0
    while k < len(chars) and not chars[k][1] and chars[k][0] in WS:
        k += 1
    first = bytearray()
    while k < len(chars) and not (not chars[k][1] and chars[k][0] in WS):
        first.append(chars[k][0])
        k += 1
    return cmdsub(echo_out(bytes(first)))


# ------------------------------------------------------------------ the resolver
class Resolver:
    def __init__(self, env: dict[bytes, bytes], cwd: str):
        self.env = env
        self.cwd = cwd

    def get(self, k: str) -> bytes:
        return self.env.get(bb(k), b"")

    def p(self, b: bytes) -> str:
        return os.path.join(self.cwd, fs(b)) if b else self.cwd

    def command_v(self, name: bytes) -> bytes:
        if name == b"":
            return b""
        if b"/" in name:
            q = self.p(name)
            return name if (os.access(q, os.X_OK) and not os.path.isdir(q)) else b""
        s = fs(name)
        if s in KEYWORDS or s in BUILTINS or s in FUNCTIONS:
            return name
        for d in self.get("PATH").split(b":"):
            cand = (d if d else bb(self.cwd)) + b"/" + name
            q = self.p(cand)
            if os.path.isfile(q) and os.access(q, os.X_OK):
                return cand
        return b""

    def exists_path(self, cmd: bytes) -> bool:
        return cmd != b"" and os.path.exists(self.p(cmd))

    def desktop_file_to_binary(self, app: bytes) -> bool:
        home = self.get("HOME")
        dh = self.get("XDG_DATA_HOME") or home + b"/.local/share"
        dd = self.get("XDG_DATA_DIRS") or b"/usr/local/share:/usr/share"
        desktop = basename(app)
        file_path = b""
        for d in expand(ifs_split(dh + b":" + dd, b":"), self.cwd):
            if not ((d != b"" and os.path.isdir(self.p(d + b"/applications"))) or os.path.isdir(self.p(d + b"/applnk"))):
                continue
            if b"-" in desktop:
                vendor = desktop[:desktop.rfind(b"-")]
                rest = desktop[desktop.find(b"-") + 1:]
                if readable(self.p(d + b"/applications/" + vendor + b"/" + rest)):
                    file_path = d + b"/applications/" + vendor + b"/" + rest
                elif readable(self.p(d + b"/applnk/" + vendor + b"/" + rest)):
                    file_path = d + b"/applnk/" + vendor + b"/" + rest
            if file_path == b"":
                indirs = [d + b"/applications/"] + self.subdirs(d + b"/applications/") + [d + b"/applnk/"] + \
                    self.subdirs(d + b"/applnk/")
                for indir in indirs:
                    f = indir + b"/" + desktop
                    if readable(self.p(f)):
                        file_path = f
                        break
            if file_path != b"" and readable(self.p(file_path)):
                data = readfile(self.p(file_path))
                text = b""
                for ln in lines_of(data or b""):
                    if EXEC.match(ln):
                        text += ln.split(b"=", 1)[1] + b"\n"
                cmd = self.command_v(read_first(text))
                return self.exists_path(cmd)
        return False

    def subdirs(self, prefix: bytes) -> list[bytes]:
        """`"$dir"/applications/*/` — non-hidden subdirectories, sorted; unmatched pattern stays literal."""
        base = self.p(prefix)
        try:
            names = sorted(bb(n) for n in os.listdir(base))
        except OSError:
            return [prefix + b"*/"]
        out = [prefix + n + b"/" for n in names if not n.startswith(b".") and os.path.isdir(os.path.join(base, fs(n)))]
        return out or [prefix + b"*/"]

    def desktop_glob(self, prefix: bytes) -> list[bytes]:
        """`"$dir/"*.desktop` — non-hidden names ending in .desktop, sorted; unmatched pattern stays literal."""
        try:
            names = sorted(bb(n) for n in os.listdir(self.p(prefix)))
        except OSError:
            return [prefix + b"*.desktop"]
        out = [prefix + n for n in names if not n.startswith(b".") and n.endswith(b".desktop")]
        return out or [prefix + b"*.desktop"]

    def check_mimeapps_list(self, mime: bytes, d: bytes) -> bytes | None:
        xcd = self.get("XDG_CURRENT_DESKTOP")
        for desktop in expand(ifs_split(xcd, b":"), self.cwd) + [b""]:
            prefix = bytes(c + 32 if 65 <= c <= 90 else c for c in desktop) + b"-" if desktop else b""
            path = d + b"/" + prefix + b"mimeapps.list"
            q = self.p(path)
            if not os.path.isfile(q):
                continue
            if not readable(q):
                continue
            data = readfile(q) or b""
            pre = awk_v(mime) + b"="
            indefault = False
            result = None
            for ln in lines_of(data):
                if ln.startswith(b"[Default Applications]"):
                    indefault = True
                elif ln.startswith(b"["):
                    indefault = False
                elif result is None and indefault and ln.startswith(pre):
                    result = ln[len(pre):]
            result = cmdsub(result + b"\n") if result is not None else b""
            if result:
                for app in expand(ifs_split(result, b";"), self.cwd):
                    if self.desktop_file_to_binary(app):
                        return echo_out(app)
        return None

    def grep_lines(self, rx: re.Pattern, path: bytes) -> list[bytes]:
        data = readfile(self.p(path))
        if data is None:
            return []
        return [ln for ln in lines_of(data) if rx.search(ln)]

    def search_desktop_file(self, rx: re.Pattern | None, d: bytes) -> bytes:
        out = b""
        if rx is not None:
            for f in self.desktop_glob(d + b"/"):
                if self.grep_lines(rx, f):
                    out += f + b"\n"
        for sub in self.subdirs(d + b"/"):
            if os.path.isdir(self.p(sub)):
                out += self.search_desktop_file(rx, sub)
        return out

    def initial_preference(self, x: bytes) -> bytes:
        data = readfile(self.p(x))
        if data is None:
            return b""
        out = b""
        for ln in lines_of(data):
            if b"InitialPreference=" in ln:
                f = ln.split(b"=")
                out += (f[1] if len(f) > 1 else b"") + b"\n"
        return cmdsub(out)

    def defapp_generic(self, mime: bytes) -> bytes:
        home = self.get("HOME")
        ch = self.get("XDG_CONFIG_HOME") or home + b"/.config"
        cd = self.get("XDG_CONFIG_DIRS") or b"/etc/xdg"
        dh = self.get("XDG_DATA_HOME") or home + b"/.local/share"
        dd = self.get("XDG_DATA_DIRS") or b"/usr/local/share/:/usr/share/"
        for d in expand(ifs_split(ch, b":") + ifs_split(cd, b":"), self.cwd):
            r = self.check_mimeapps_list(mime, d)
            if r is not None:
                return r
        datadirs = expand(ifs_split(dh, b":") + ifs_split(dd, b":"), self.cwd)
        for d in datadirs:
            r = self.check_mimeapps_list(mime, d + b"/applications")
            if r is not None:
                return r
        rx = bre(mime + b"=")
        for x in datadirs:
            for prefix in (self.get("XDG_MENU_PREFIX"), b""):
                first = None
                if rx is not None:
                    for f in (x + b"/applications/" + prefix + b"defaults.list",
                              x + b"/applications/" + prefix + b"mimeinfo.cache"):
                        hits = self.grep_lines(rx, f)
                        if hits:
                            first = f + b":" + hits[0]
                            break
                if first is None:
                    continue
                parts = first.split(b"=")
                v = parts[1] if len(parts) > 1 else first
                v = cmdsub(v.split(b";")[0] + b"\n")
                if v:
                    return echo_out(v)
        # defapp_fallback
        rx2 = bre(mime + b";")
        preference = -1
        desktop_file = b""
        for d in datadirs:
            for x in expand(ws_split(self.search_desktop_file(rx2, d + b"/applications")), self.cwd):
                v = bash_int(b"0" + self.initial_preference(x))
                if v is not None and v > preference:
                    preference = v
                    desktop_file = x
        if desktop_file:
            b = basename(desktop_file)
            return b + b"\n" if b else b""
        return b""

    def detect_lxqt(self) -> tuple[str, bool]:
        """Return (DE family, flatpak) as far as defapp dispatch cares: 'lxqt', 'kde' or 'generic'."""
        xcd = self.get("XDG_CURRENT_DESKTOP")
        known = None
        if xcd:
            if xcd in (b"Cinnamon", b"X-Cinnamon"):
                known = "cinnamon"
            elif xcd == b"ENLIGHTENMENT":
                known = "enlightenment"
            elif xcd.startswith(b"GNOME"):
                known = "gnome"
            elif xcd == b"KDE":
                known = "kde"
            elif xcd in (b"DEEPIN", b"Deepin", b"deepin"):
                known = "deepin"
            elif xcd == b"LXDE":
                known = "lxde"
            elif xcd == b"LXQt":
                known = "lxqt"
            elif xcd == b"MATE":
                known = "mate"
            elif xcd == b"XFCE":
                known = "xfce"
            elif xcd == b"X-Generic":
                known = "generic"
        de = known
        if de is None:
            if self.get("KDE_FULL_SESSION"):
                de = "kde"
            elif self.get("GNOME_DESKTOP_SESSION_ID"):
                de = "gnome"
            elif self.get("MATE_DESKTOP_SESSION_ID"):
                de = "mate"
            elif re.search(rb"(?m)^Enlightenment", self.get("DESKTOP")):
                de = "enlightenment"
            elif self.get("LXQT_SESSION_CONFIG"):
                de = "lxqt"
        if de is None:
            ds = self.get("DESKTOP_SESSION")
            if ds == b"gnome":
                de = "gnome"
            elif ds in (b"LXDE", b"Lubuntu"):
                de = "lxde"
            elif ds == b"MATE":
                de = "mate"
            elif ds in (b"xfce", b"xfce4", b"Xfce Session"):
                de = "xfce"
        if os.path.isfile(self.p(self.get("XDG_RUNTIME_DIR") + b"/flatpak-info")):
            de = "flatpak"
        return de or "", False

    def query(self, mime: bytes) -> tuple[bytes | None, int]:
        if mime in (b"--help", b"--manual"):
            raise Unsupported(f"{fs(mime)} prints the usage text")
        if mime == b"--version":
            return b"xdg-mime 1.2.1", 0
        if b"PATH" not in self.env:
            raise Unsupported("PATH unset (bash's compiled-in default path)")
        if mime == b"" or mime.startswith(b"-") or b"/" not in mime:
            return None, 1
        if not TYPE_CHARS.fullmatch(mime):
            raise Unsupported(f"type {fs(mime)!r} has characters outside RFC 6838 restricted-name (grep/gawk regex "
                              "engine behaviour on them is not modelled)")
        de, _ = self.detect_lxqt()
        if de == "kde":
            ksv = bash_int(self.get("KDE_SESSION_VERSION"))
            if ksv is not None and ksv < 6:
                trader = {b"4": "ktraderclient", b"5": "ktraderclient5"}.get(self.get("KDE_SESSION_VERSION"))
                if trader and self.command_v(bb(trader)):
                    raise Unsupported(f"KDE trader {trader} on PATH")
        if de == "lxqt":
            if self.command_v(b"qtxdg-mat"):
                raise Unsupported("qtxdg-mat on PATH")
            return None, 3
        out = self.defapp_generic(mime)
        if out == b"":
            return None, 0
        return (out[:-1] if out.endswith(b"\n") else out), 0


def selftest() -> int:
    """Each expectation is the installed xdg-mime's label of the round-92 frozen case named in the check."""
    import tempfile
    checks: list[tuple[str, bool]] = []
    with tempfile.TemporaryDirectory() as root:
        def w(rel: str, text: str, mode: int | None = None) -> None:
            p = os.path.join(root, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(text)
            if mode is not None:
                os.chmod(p, mode)

        def q(t: str, **extra: str) -> tuple[str | None, int]:
            env = {"HOME": f"{root}/home", "XDG_CONFIG_HOME": f"{root}/cfg", "XDG_CONFIG_DIRS": f"{root}/etc",
                   "XDG_DATA_HOME": f"{root}/data", "XDG_DATA_DIRS": f"{root}/share", "PATH": f"{root}/bin:/usr/bin",
                   "XDG_CURRENT_DESKTOP": "Hyprland"}
            env.update(extra)
            d, rc = Resolver({bb(k): bb(v) for k, v in env.items()}, root).query(bb(t))
            return (None if d is None else fs(d)), rc

        def app(id_: str, prog: str, where: str = "data/applications") -> None:
            w(f"{where}/{id_}", f"[Desktop Entry]\nType=Application\nExec={prog} %U\n")
            w(f"bin/{prog}", "#!/bin/sh\nexit 0\n", 0o755)

        da = "[Default Applications]\n"
        app("a.desktop", "a")
        app("h.desktop", "h")
        w("cfg/hyprland-mimeapps.list", da + "image/png=h.desktop\n")
        w("cfg/mimeapps.list", da + "text/plain=gone.desktop;a.desktop\nimage/png=a.desktop\nvideo/mp4=gone.desktop\nvideo/mp4=h.desktop\n"
          "text/html=a.desktop\r\nx-scheme-handler/x=t.desktop\n")
        w("etc/mimeapps.list", da + "video/mp4=a.desktop\n")
        w("data/applications/t.desktop", "[Desktop Entry]\nExec=true\n")
        w("share/applications/mimeinfo.cache", "[MIME Cache]\nxtext/csv=un.desktop;\napplication/q=-n;\n")
        w("share/applications/p1.desktop", "[Desktop Entry]\nMimeType=text/x-p;\n")
        w("share/applications/p2.desktop", "[Desktop Entry]\nMimeType=text/x-p;\nInitialPreference=5\n")
        checks += [
            ("m03 list: second id installed", q("text/plain") == ("a.desktop", 0)),
            ("m05 desktop-specific file first", q("image/png") == ("h.desktop", 0)),
            ("m09 only a file's first matching line counts; the next file is read", q("video/mp4") == ("a.desktop", 0)),
            ("m16 CR kept in the id", q("text/html") == (None, 0)),
            ("d09 Exec=true is a builtin: not installed", q("x-scheme-handler/x") == (None, 0)),
            ("f06 unanchored grep in mimeinfo.cache", q("text/csv") == ("un.desktop", 0)),
            ("f09 a cache value -n is an echo option", q("application/q") == (None, 0)),
            ("b02 InitialPreference picks", q("text/x-p") == ("p2.desktop", 0)),
            ("s01 LXQt: rc 3", q("text/plain", XDG_CURRENT_DESKTOP="LXQt") == (None, 3)),
            ("s05 no slash: rc 1", q("plain") == (None, 1)),
            ("s08 --version", q("--version") == ("xdg-mime 1.2.1", 0)),
        ]
        try:
            q("text/[a]")
            checks.append(("type outside RFC 6838 refused", False))
        except Unsupported:
            checks.append(("type outside RFC 6838 refused", True))
    failed = [n for n, ok in checks if not ok]
    for n in failed:
        print(f"MADO_XDGMIME_SELFTEST_FAIL: {n}")
    print(f"MADO_XDGMIME_SELFTEST: checks={len(checks)} failed={len(failed)}")
    return 1 if failed else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--cwd", default=None)
    ap.add_argument("--env", action="append", default=[])
    ap.add_argument("--from-environ", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("types", nargs="*")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.types:
        ap.error("name at least one TYPE (or --selftest)")
    env: dict[bytes, bytes] = dict(os.environb) if a.from_environ else {}
    for kv in a.env:
        if "=" not in kv:
            ap.error(f"--env needs NAME=VALUE: {kv}")
        k, v = kv.split("=", 1)
        env[bb(k)] = bb(v)
    for k in (b"XDG_UTILS_REALPATH_BACKEND", b"XDG_UTILS_DEBUG_LEVEL"):
        if env.get(k):
            print(f"mado-xdgmime: unsupported: {fs(k)} set", file=sys.stderr)
            return 2
    cwd = os.path.abspath(a.cwd or os.getcwd())
    r = Resolver(env, cwd)
    results = []
    try:
        for t in a.types:
            d, rc = r.query(bb(t))
            results.append({"type": t, "default": None if d is None else fs(d), "rc": rc})
    except Unsupported as e:
        print(f"mado-xdgmime: unsupported: {e}", file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps({"results": results}, ensure_ascii=True))
    else:
        for x in results:
            print(f"{x['type']}\t{x['default'] if x['default'] is not None else '-'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
