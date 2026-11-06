#!/usr/bin/env python3
# mado-mako.py - read-only resolver for mako's effective settings for one notification.
#
# Source: mako 1.11.0 manual, /usr/share/man/man5/mako.5.gz
# (sha256 f717848f47cc7739d4bddbcc08c133a32e0d7dface7d1769882da1a0150477ba).
# Line numbers below refer to the decompressed roff source, numbered with `nl -ba`.
#
# Semantic choices and the manual line each one traces to:
#   L16-17   Config lives at ~/.config/mako/config or $XDG_CONFIG_HOME/mako/config. The tool
#            reads only the --config path the caller names; --home supplies the ~ expansion.
#   L24      Empty lines and lines beginning with # are ignored.
#   L26-52   Global configuration options: max-history (L28), sort (L37), include (L45).
#   L45-50   include=<path>: the path must be absolute or start with ~/ ; any other form is refused.
#            The target must be a regular file (a non-regular target is refused), a missing target
#            is refused, and an include cycle is refused. Included content is read at the position
#            of the directive, and an included file starts again in the global section.
#   Containment (lane stance, not a mako rule; mako itself opens any absolute include): an include
#            is read only when its fully resolved path (every symlink and .. resolved, realpath)
#            lies inside a declared read root: --home and each --read-root, both absolute, each
#            root itself resolved with realpath. An include that resolves outside every root is
#            refused before its contents are opened (the path is resolved only to test
#            containment), and the resolved path is what is opened. The --config file itself is
#            named by the caller and is not subject to the roots. Named limits: a concurrent writer
#            under a root can swap a component between the check and the open (TOCTOU); hardlinks
#            and bind mounts are not symlinks and are not seen; a root that holds secrets is read
#            as declared (containment bounds the read set, it does not classify content).
#   L53-161  Binding options (on-button-*, on-touch, on-notify) and their action grammar.
#   L162-418 Style options; group-by (L371), max-visible (L381), output (L389), layer (L400),
#            anchor (L410) are style options.
#   L419-423 Criteria sections [..] hold binding and style options only.
#   L431-434 A criteria section matches when all of its fields match; unlisted fields are not considered.
#   L435-437 Criteria apply in file order; the last matching occurrence of an option wins.
#   L443-444 app-name is a plain string field, compared for equality (regex needs the ~ suffix, L450).
#   L459     urgency is one of low, normal, critical; upstream types.c parse_urgency compares them
#            case-insensitively and also accepts high as critical, so a criteria value is mapped
#            that way before it is compared; any other value is refused.
#   L469-471 mode: the section applies only while that mode is enabled.
#   L447-457 summary and body are exact string fields. summary~ and body~ are POSIX extended regex
#            fields: upstream criteria.c compiles the value with regcomp(REG_EXTENDED | REG_NOSUB) and
#            matches with regexec (unanchored search). The tool calls the same libc regcomp/regexec
#            through ctypes, never Python re (Python re is not POSIX ERE). mako never calls
#            setlocale (no call anywhere in the v1.11.0 tree), so it matches in the C locale every
#            C program starts in; the tool sets LC_ALL=C before its first regcomp. A value regcomp
#            rejects is refused (upstream rejects the criteria); summary with summary~ (or body with
#            body~) in one section is refused (criteria.c "Cannot set both"). A regexec error other
#            than REG_NOMATCH is a non-match, as in criteria.c match_regex_criteria.
#   L443-445,461-463 app-icon, category, desktop-entry: plain string fields compared for equality
#            (upstream criteria.c v1.11.0 match_criteria uses strcmp for each).
#   L465-467 actionable and expiring are boolean fields; L510-516 a value may be true/false, 0/1, or a
#            bare word, where a leading ! negates. Upstream types.c parse_boolean compares true/false
#            case-insensitively (strcasecmp) and 1/0 exactly; any other value is refused.
#            A criteria field whose notification input was not supplied is refused, never guessed.
#   L474-495 Second-pass fields (grouped, group-index, hidden, output, anchor) are outside the model
#            and refused.
#   L497-508 Criteria values may be quoted with double quotes; a backslash escapes the next character
#            inside and outside quotes (criteria.c parse_criteria QUOTE_ESCAPE/ESCAPE states); only a
#            space separates tokens; no spaces around '='.
#   L510-516 Bare tokens other than actionable/expiring (grouped, hidden, ...) are outside the model.
#   L519-522 Defaults form the base of resolution; the global section overrides them; criteria override both.
#   L540-552 invisible is a criteria-only style option (default 0).
#   L581     Global option lines may put spaces around '=' (margin = 10,20,5).
#   L614-621 Modes: the initial list holds the single mode "default" (deprecated).
#   L633-634 makoctl -a adds a mode to the list; --mode values are added to the initial list.
#   L557     Colours are #RRGGBB or #RRGGBBAA.
#   L569-573 Directional values: 1 to 4 comma-separated integers.
#   L37-38   sort: +/-time or +/-priority.
#   L266,311,320,328,363,545  Boolean options are documented as 0|1; upstream config.c parses them with
#            types.c parse_boolean, so true/false (any case) are accepted too. The effective value
#            is reported in the manual's 0|1 form.
#   L296-301 icon-location: left, right, top, bottom. L348-352 text-alignment: left, center, right.
#   L400-407 layer: background, bottom, top, overlay. L410-416 anchor: nine positions.
#   L252-263 progress-color: [over|source] colour.
#   Defaults: the "Default:" line of each option in the manual (L34 .. L552).
#
# Usage: python3 -I tools/mado-mako.py --config PATH [--home DIR] [--app-name NAME]
#        [--app-icon S] [--summary S] [--body S] [--category S] [--desktop-entry S]
#        [--urgency {low,normal,critical}] [--actionable {true,false}] [--expiring {true,false}]
#        [--mode NAME ...]
#        [--read-root DIR ...]   (extra trusted roots for include= targets; --home is always one)
#        python3 -I tools/mado-mako.py --selftest --scratch-root DIR
# Exit: 0 when resolution ran (refusals allowed); 2 on setup error (bad arguments, missing or unreadable config).

import argparse
import ctypes
import ctypes.util
import json
import locale
import os
import re
import shutil
import stat
import sys
import tempfile

URGENCIES = ("low", "normal", "critical")
INITIAL_MODES = ("default",)  # L620-621

BINDING_KEYS = ("on-button-left", "on-button-middle", "on-button-right", "on-touch", "on-notify")
STYLE_KEYS = (
    "font", "background-color", "text-color", "width", "height", "outer-margin", "margin",
    "padding", "border-size", "border-color", "border-radius", "progress-color", "icons",
    "max-icon-size", "icon-path", "icon-location", "icon-border-radius", "markup", "actions",
    "history", "format", "text-alignment", "default-timeout", "ignore-timeout", "group-by",
    "max-visible", "output", "layer", "anchor",
)
GLOBAL_ONLY_KEYS = ("max-history", "sort")  # L28, L37
CRITERIA_ONLY_KEYS = ("invisible",)  # L545
GLOBAL_KEYS = BINDING_KEYS + STYLE_KEYS + GLOBAL_ONLY_KEYS
CRITERIA_KEYS = BINDING_KEYS + STYLE_KEYS + CRITERIA_ONLY_KEYS
MODELLED_FIELDS = ("app-name", "app-icon", "summary", "body", "urgency", "category",
                   "desktop-entry", "actionable", "expiring", "mode")
STRING_INPUT_FIELDS = ("app-icon", "summary", "body", "category", "desktop-entry")
BOOLEAN_FIELDS = ("actionable", "expiring")
REGEX_FIELDS = {"summary~": "summary", "body~": "body"}  # criteria.c summary_pattern / body_pattern
REG_EXTENDED = 1  # /usr/include/regex.h
REG_NOSUB = 1 << 3  # /usr/include/regex.h
REGEX_T_BYTES = 256  # glibc x86-64 sizeof(regex_t) is 64; oversized on purpose
_LIBC = []


def _libc():
    """libc regcomp/regexec/regfree, loaded once, in the C locale mako runs in."""
    if not _LIBC:
        locale.setlocale(locale.LC_ALL, "C")
        lib = ctypes.CDLL(ctypes.util.find_library("c"))
        lib.regcomp.argtypes = (ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int)
        lib.regcomp.restype = ctypes.c_int
        lib.regexec.argtypes = (ctypes.c_void_p, ctypes.c_char_p, ctypes.c_size_t, ctypes.c_void_p,
                                ctypes.c_int)
        lib.regexec.restype = ctypes.c_int
        lib.regfree.argtypes = (ctypes.c_void_p,)
        lib.regfree.restype = None
        _LIBC.append(lib)
    return _LIBC[0]


def posix_ere_compile(pattern):
    """regcomp(pattern, REG_EXTENDED | REG_NOSUB) as criteria.c does; the compiled buffer or None."""
    raw = pattern.encode("utf-8", "surrogateescape")
    if b"\x00" in raw:
        return None
    lib = _libc()
    buf = ctypes.create_string_buffer(REGEX_T_BYTES)
    if lib.regcomp(buf, raw, REG_EXTENDED | REG_NOSUB) != 0:
        return None
    return buf


def posix_ere_search(compiled, text):
    """regexec(compiled, text, 0, NULL, 0) == 0, as criteria.c match_regex_criteria."""
    return _libc().regexec(compiled, text.encode("utf-8", "surrogateescape"), 0, None, 0) == 0


def posix_ere_free(compiled):
    _libc().regfree(compiled)


DEFAULTS = {
    "max-history": "5", "sort": "-time",
    "on-button-left": "invoke-default-action", "on-button-middle": "none",
    "on-button-right": "dismiss", "on-touch": "dismiss", "on-notify": "none",
    "font": "monospace 10", "background-color": "#285577FF", "text-color": "#FFFFFFFF",
    "width": "300", "height": "100", "outer-margin": "0", "margin": "10", "padding": "5",
    "border-size": "2", "border-color": "#4C7899FF", "border-radius": "0",
    "progress-color": "over #5588AAFF", "icons": "1", "max-icon-size": "64", "icon-path": "",
    "icon-location": "left", "icon-border-radius": "0", "markup": "1", "actions": "1",
    "history": "1", "format": "<b>%s</b>\\n%b", "text-alignment": "left",
    "default-timeout": "0", "ignore-timeout": "0", "group-by": "none", "max-visible": "5",
    "output": "", "layer": "top", "anchor": "top-right", "invisible": "0",
}

ENUMS = {
    "sort": ("+time", "-time", "+priority", "-priority"),
    "text-alignment": ("left", "center", "right"),
    "icon-location": ("left", "right", "top", "bottom"),
    "layer": ("background", "bottom", "top", "overlay"),
    "anchor": ("top-right", "top-center", "top-left", "bottom-right", "bottom-center",
               "bottom-left", "center-right", "center-left", "center"),
}
BOOL_KEYS = ("icons", "markup", "actions", "history", "ignore-timeout", "invisible")
INT_KEYS = ("max-history", "width", "height", "max-icon-size", "border-size",
            "icon-border-radius", "max-visible", "default-timeout")
DIRECTIONAL_KEYS = ("outer-margin", "margin", "padding", "border-radius")
COLOR_KEYS = ("background-color", "text-color", "border-color")
ACTION_WORDS = ("none", "dismiss", "dismiss-all", "dismiss-group", "invoke-action",
                "invoke-default-action", "exec")
HEX_COLOR = re.compile(r"#[0-9A-Fa-f]{6}(?:[0-9A-Fa-f]{2})?")

REFUSED = object()


def check_value(key, value):
    """Return None when value is valid for key, otherwise the reason it is not."""
    if key in BOOL_KEYS:
        return None if parse_boolean(value) is not None else "expects 0, 1, true or false"
    if key in INT_KEYS:
        return None if re.fullmatch(r"-?[0-9]+", value) else "expects an integer"
    if key in DIRECTIONAL_KEYS:
        parts = [part.strip() for part in value.split(",")]
        if 1 <= len(parts) <= 4 and all(re.fullmatch(r"[0-9]+", part) for part in parts):
            return None
        return "expects 1 to 4 comma-separated integers"
    if key in COLOR_KEYS:
        return None if HEX_COLOR.fullmatch(value) else "expects #RRGGBB or #RRGGBBAA"
    if key == "progress-color":
        words = value.split()
        if len(words) == 2 and words[0] in ("over", "source"):
            words = words[1:]
        ok = len(words) == 1 and HEX_COLOR.fullmatch(words[0]) is not None
        return None if ok else "expects [over|source] #RRGGBB[AA]"
    if key in ENUMS:
        return None if value in ENUMS[key] else "expects one of " + ", ".join(ENUMS[key])
    if key in BINDING_KEYS:
        words = value.split()
        if not words or words[0] not in ACTION_WORDS:
            return "unknown action"
        if words[0] == "dismiss" and any(word != "--no-history" for word in words[1:]):
            return "dismiss takes only --no-history"
        if words[0] in ("none", "invoke-default-action") and len(words) > 1:
            return words[0] + " takes no argument"
        if words[0] in ("invoke-action", "exec") and len(words) < 2:
            return words[0] + " needs an argument"
        return None
    return None


def parse_boolean(value):
    """Upstream types.c parse_boolean: true/false case-insensitive, 1/0 exact; None otherwise."""
    lowered = value.lower()
    if lowered == "true" or value == "1":
        return True
    if lowered == "false" or value == "0":
        return False
    return None


def parse_urgency(value):
    """Upstream types.c parse_urgency: low/normal/critical case-insensitive, high means critical."""
    word = value.lower()
    if word == "high":
        return "critical"
    return word if word in URGENCIES else None


def normalize(key, value):
    """Report a validated boolean option in the manual's 0|1 form; other values unchanged."""
    if key in BOOL_KEYS:
        return "1" if parse_boolean(value) else "0"
    return value


def tokenize(body):
    """Split a criteria header into (key, value) pairs; value is None for a bare token.

    Quoting and escapes follow L497-508: double quotes group text; inside quotes \\" and \\\\
    are escapes; outside quotes a backslash escapes the next character. Only the first '='
    of a token splits key from value. Returns (tokens, error)."""
    tokens = []
    word = []
    key = None
    started = False
    in_quote = False

    def end_word():
        nonlocal key, word, started
        if started:
            if key is None:
                tokens.append(("".join(word), None))
            else:
                tokens.append((key, "".join(word)))
        key, word, started = None, [], False

    i = 0
    while i < len(body):
        char = body[i]
        if in_quote:
            if char == "\\":
                if i + 1 >= len(body):
                    return [], "dangling backslash inside a quote (criteria.c: unmatched quote)"
                word.append(body[i + 1])
                i += 2
                continue
            if char == '"':
                in_quote = False
            else:
                word.append(char)
            i += 1
            continue
        if char == '"':
            in_quote = True
            started = True
        elif char == "\\":
            if i + 1 >= len(body):
                return [], "dangling backslash"
            word.append(body[i + 1])
            started = True
            i += 2
            continue
        elif char == " ":
            end_word()
        elif char == "=" and key is None:
            key = "".join(word)
            word = []
            started = True
        else:
            word.append(char)
            started = True
        i += 1
    if in_quote:
        return [], "unterminated quote"
    end_word()
    return tokens, None


class _State:
    def __init__(self, home, app_name, urgency, modes, inputs=None, flags=None):
        self.home = home
        self.app_name = app_name
        self.urgency = urgency
        self.modes = modes
        self.inputs = dict(inputs or {})
        self.flags = dict(flags or {})
        self.global_values = {}
        self.sections = []
        self.applied = []
        self.refusals = []
        self.stack = []
        self.roots = []

    def within_roots(self, real):
        for root in self.roots:
            prefix = root if root.endswith(os.sep) else root + os.sep
            if real == root or real.startswith(prefix):
                return True
        return False

    def refuse(self, where, reason):
        self.refusals.append(where + ": " + reason)

    def load(self, path):
        try:
            with open(path, encoding="utf-8") as handle:
                lines = handle.read().splitlines()
        except (OSError, UnicodeDecodeError) as exc:
            self.refuse(path, "unreadable config: " + str(exc))
            return
        section = None  # None means the global section
        for lineno, raw in enumerate(lines, 1):
            where = path + ":" + str(lineno)
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("["):
                if not line.endswith("]"):
                    self.refuse(where, "section header is not closed with ']'")
                    section = REFUSED
                else:
                    section = self.open_section(line[1:-1], where)
                continue
            if "=" not in line:
                self.refuse(where, "line is not key=value")
                continue
            key, value = (part.strip() for part in line.split("=", 1))
            if section is REFUSED:
                continue
            if key == "include":
                if section is not None:
                    self.refuse(where, "include is only valid in the global section")
                else:
                    self.include(value, where)
                continue
            if section is None:
                self.global_option(key, value, where)
            else:
                self.criteria_option(section, key, value, where)

    def open_section(self, body, where):
        tokens, error = tokenize(body)
        if error:
            self.refuse(where, "criteria: " + error)
            return REFUSED
        fields = []
        for key, value in tokens:
            if value is None and key in BOOLEAN_FIELDS:
                value = "true"  # L514 [actionable]
            elif value is None and key.startswith("!") and key[1:] in BOOLEAN_FIELDS:
                key, value = key[1:], "false"  # L516 [!actionable]
            if key == "urgency" and value is not None and parse_urgency(value) is not None:
                value = parse_urgency(value)  # types.c parse_urgency
            if value is None:
                self.refuse(where, "criteria token '" + key + "' has no '=value' "
                            "(bare tokens other than actionable/expiring are outside the model; "
                            "spaces around '=' are refused)")
                return REFUSED
            if key not in MODELLED_FIELDS:
                self.refuse(where, "criteria field '" + key + "' is outside the model (refused)")
                return REFUSED
            # criteria.c apply_criteria_field assigns each token in turn: a repeated field keeps the
            # value of its last occurrence (it is not an error upstream).
            fields = [(name, kept) for name, kept in fields if name != key]
            fields.append((key, value))
        verdict = self.evaluate(fields, where)
        if verdict is None:
            return REFUSED
        section = {"header": body, "where": where, "verdict": verdict, "options": []}
        self.sections.append(section)
        if verdict == "match":
            self.applied.append("section:[" + body + "]")
        return section

    def evaluate(self, fields, where):
        """Return 'match', 'nomatch', or None when the section is refused (reason recorded)."""
        for key, value in fields:
            if key == "urgency" and value not in URGENCIES:
                self.refuse(where, "urgency '" + value + "' is not low, normal or critical")
                return None
            if key in BOOLEAN_FIELDS and parse_boolean(value) is None:
                self.refuse(where, key + " '" + value + "' is not true, false, 1 or 0")
                return None
        names = [key for key, _ in fields]
        for key, plain in REGEX_FIELDS.items():
            if key in names and plain in names:
                self.refuse(where, "criteria sets both " + plain + " and " + key
                            + " (criteria.c: cannot set both)")
                return None
        compiled = {}
        try:
            for key, value in fields:
                if key in REGEX_FIELDS:
                    pattern = posix_ere_compile(value)
                    if pattern is None:
                        self.refuse(where, key + " " + repr(value)
                                    + " is not a valid POSIX extended regex (regcomp refused it)")
                        return None
                    compiled[key] = pattern
            return self.decide(fields, where, compiled)
        finally:
            for pattern in compiled.values():
                posix_ere_free(pattern)

    def decide(self, fields, where, compiled):
        """Match the validated fields against the notification; regex fields use compiled[key]."""
        mismatch = False
        undecided = []
        for key, value in fields:
            if key == "mode":
                mismatch = mismatch or value not in self.modes
            elif key == "urgency":
                if self.urgency is None:
                    undecided.append("--urgency")
                else:
                    mismatch = mismatch or self.urgency != value
            elif key == "app-name":
                if self.app_name is None:
                    undecided.append("--app-name")
                else:
                    mismatch = mismatch or self.app_name != value
            elif key in STRING_INPUT_FIELDS:
                have = self.inputs.get(key)
                if have is None:
                    undecided.append("--" + key)
                else:
                    mismatch = mismatch or have != value
            elif key in BOOLEAN_FIELDS:
                want = parse_boolean(value)
                have = self.flags.get(key)
                if have is None:
                    undecided.append("--" + key + " (boolean)")
                else:
                    mismatch = mismatch or have != want
            elif key in REGEX_FIELDS:
                have = self.inputs.get(REGEX_FIELDS[key])
                if have is None:
                    undecided.append("--" + REGEX_FIELDS[key])
                else:
                    mismatch = mismatch or not posix_ere_search(compiled[key], have)
        if mismatch:
            return "nomatch"
        if undecided:
            self.refuse(where, "criteria needs " + ", ".join(undecided)
                        + " to decide the match; section not applied")
            return None
        return "match"

    def global_option(self, key, value, where):
        if key in CRITERIA_ONLY_KEYS:
            self.refuse(where, "'" + key + "' is criteria-only; not valid in the global section")
            return
        if key not in GLOBAL_KEYS:
            self.refuse(where, "unknown global option '" + key + "'")
            return
        reason = check_value(key, value)
        if reason:
            self.refuse(where, key + "=" + repr(value) + ": " + reason)
            return
        self.global_values[key] = normalize(key, value)

    def criteria_option(self, section, key, value, where):
        if key in GLOBAL_ONLY_KEYS:
            self.refuse(where, "global-only option '" + key + "' in a criteria section")
            return
        if key not in CRITERIA_KEYS:
            self.refuse(where, "unknown criteria option '" + key + "'")
            return
        reason = check_value(key, value)
        if reason:
            self.refuse(where, key + "=" + repr(value) + ": " + reason)
            return
        section["options"].append((key, normalize(key, value)))

    def include(self, value, where):
        if value.startswith("~/") and self.home is None:
            self.refuse(where, "include ~/ needs --home (no implicit HOME fallback)")
            return
        if value.startswith("~/"):
            value = "~/" + value[2:].lstrip("/")  # config.c joins "$HOME/" + rest: ~//x stays under HOME
            target = os.path.join(self.home, value[2:])
        elif value.startswith("/"):
            target = value
        else:
            self.refuse(where, "include path must be absolute or start with ~/: " + repr(value))
            return
        if target.endswith("/"):
            self.refuse(where, "include target is not a regular file: " + target + " (trailing /)")
            return
        try:
            real = os.path.realpath(target)
        except ValueError as exc:
            self.refuse(where, "include path is not a valid path: " + repr(value) + " (" + str(exc) + ")")
            return
        if not self.within_roots(real):
            self.refuse(where, "include resolves outside the declared read roots: " + target
                        + " -> " + real + " (declare it with --read-root to read it)")
            return
        try:
            info = os.stat(real)
        except OSError as exc:
            self.refuse(where, "include target missing or unreadable: " + target
                        + " (" + str(exc.strerror) + ")")
            return
        if not stat.S_ISREG(info.st_mode):
            self.refuse(where, "include target is not a regular file: " + target)
            return
        if real in self.stack:
            self.refuse(where, "include cycle: " + target)
            return
        self.applied.append("include:" + target)
        self.stack.append(real)
        self.load(real)
        self.stack.pop()


def resolve(config, home, app_name, urgency, modes, inputs=None, flags=None, read_roots=()):
    """Resolve effective settings for one notification. config must already be resolved once."""
    state = _State(home, app_name, urgency, modes, inputs, flags)
    roots = [os.path.realpath(home)] if home else []
    roots.extend(os.path.realpath(root) for root in read_roots)
    state.roots = roots
    state.stack.append(config)
    state.load(config)
    effective = dict(DEFAULTS)
    effective.update(state.global_values)
    applied = list(state.applied)
    if state.global_values:
        applied.insert(0, "global-section")
    for section in state.sections:
        if section["verdict"] == "match":
            for key, value in section["options"]:
                effective[key] = value
    return {"effective": effective, "applied": applied, "refusals": state.refusals}


def setup_error(message):
    print("mado-mako: setup error: " + message, file=sys.stderr)
    return 2


def _write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def selftest(scratch_root):
    if not os.path.isdir(scratch_root):
        return setup_error("--scratch-root is not a directory: " + scratch_root)
    work = tempfile.mkdtemp(prefix="mako-selftest-", dir=scratch_root)
    checks = []

    def check(name, ok):
        checks.append((name, bool(ok)))

    def run(name, config, app_name=None, urgency=None, modes=(), extra=None, inputs=None, flags=None,
            roots=None):
        base = os.path.join(work, name)
        os.makedirs(base)
        cfg = os.path.join(base, "config")
        _write(cfg, config.replace("@BASE@", base))
        for rel, text in (extra or {}).items():
            if isinstance(text, tuple):  # ("symlink", target relative to base)
                os.makedirs(os.path.dirname(os.path.join(base, rel)), exist_ok=True)
                os.symlink(os.path.join(base, text[1]), os.path.join(base, rel))
            else:
                _write(os.path.join(base, rel), text)
        os.makedirs(os.path.join(base, "home"), exist_ok=True)
        read_roots = (base,) if roots is None else tuple(os.path.join(base, r) for r in roots)
        return resolve(os.path.realpath(cfg), os.path.join(base, "home"), app_name, urgency,
                       set(INITIAL_MODES) | set(modes), inputs, flags, read_roots)

    try:
        r = run("global", "width=500\nmargin = 10,20,5\n# comment\n\n")
        check("global option overrides default", r["effective"]["width"] == "500")
        check("spaces around = in global lines (L581)", r["effective"]["margin"] == "10,20,5")
        check("default kept when unset (L519-522)", r["effective"]["anchor"] == "top-right")
        check("comment and blank lines ignored (L24)", r["refusals"] == [])

        app = "[app-name=foo]\nbackground-color=#000000FF\n"
        r = run("appname", app, app_name="foo")
        check("app-name criteria applies on match (L443)", r["effective"]["background-color"] == "#000000FF")
        r = run("appname-miss", app, app_name="bar")
        check("app-name criteria skipped on mismatch (L431-434)",
              r["effective"]["background-color"] == "#285577FF")
        r = run("quoted", '[app-name="Google Chrome"]\ninvisible=1\n', app_name="Google Chrome")
        check("quoted criteria value (L497-503)", r["effective"]["invisible"] == "1")
        r = run("escaped", "[app-name=Google\\ Chrome]\ninvisible=1\n", app_name="Google Chrome")
        check("backslash-escaped space in criteria (L506)", r["effective"]["invisible"] == "1")
        r = run("last-wins", "[app-name=foo]\nwidth=111\n[urgency=critical]\nwidth=222\n",
                app_name="foo", urgency="critical")
        check("later matching criteria wins (L435-437)", r["effective"]["width"] == "222")
        r = run("mode-off", "[mode=dnd]\ninvisible=1\n")
        check("mode criteria needs enabled mode (L469-471)", r["effective"]["invisible"] == "0")
        r = run("mode-on", "[mode=dnd]\ninvisible=1\n", modes=["dnd"])
        check("mode criteria applies when enabled (L633)", r["effective"]["invisible"] == "1")
        r = run("default-mode", "[mode=default]\nwidth=77\n")
        check("initial mode default is enabled (L620-621)", r["effective"]["width"] == "77")
        r = run("urgency-miss", "[urgency=low]\nwidth=77\n", urgency="critical")
        check("urgency mismatch skipped (L459)", r["effective"]["width"] == "300")
        r = run("urgency-alias", "[urgency=HIGH]\nwidth=77\n[urgency=Low]\nheight=7\n", urgency="critical")
        check("urgency criteria casefold and high = critical (types.c parse_urgency)",
              r["effective"]["width"] == "77" and r["effective"]["height"] == "100" and r["refusals"] == [])
        r = run("repeat-last-wins", "[app-name=a app-name=b]\nwidth=78\n[actionable !actionable]\nheight=8\n",
                app_name="b", flags={"actionable": False})
        check("a repeated criteria field keeps its last value (criteria.c apply_criteria_field)",
              r["effective"]["width"] == "78" and r["effective"]["height"] == "8" and r["refusals"] == [])
        r = run("rel-include", "include=core.ini\n")
        check("relative include refused (L45-50)",
              any("absolute" in s for s in r["refusals"]) and r["applied"] == [])
        r = run("abs-include", "include=@BASE@/core.ini\n", extra={"core.ini": "max-history=9\nwidth=640\n"})
        check("absolute include applied (L45)",
              r["effective"]["width"] == "640" and r["refusals"] == []
              and any(a.startswith("include:") for a in r["applied"]))
        r = run("tilde-include", "include=~/core.ini\n", extra={"home/core.ini": "height=55\n"})
        check("tilde include expands via --home (L48)", r["effective"]["height"] == "55")
        r = run("missing-include", "include=@BASE@/nope.ini\n")
        check("missing include refused (L45-50)", len(r["refusals"]) == 1 and "missing" in r["refusals"][0])
        r = run("dir-include", "include=@BASE@/adir\n", extra={"adir/x": ""})
        check("non-regular include target refused (L45-50)",
              any("not a regular file" in s for s in r["refusals"]))
        r = run("cycle", "include=@BASE@/config\n")
        check("include cycle refused (L45-50)", any("cycle" in s for s in r["refusals"]))
        r = run("unmodelled", "[summary=hello]\nwidth=1\n")
        check("unmodelled criteria field refused, not applied (L447)",
              any("summary" in s for s in r["refusals"]) and r["effective"]["width"] == "300")
        r = run("no-input", "[app-name=foo]\nwidth=1\n")
        check("criteria needing missing input refused, not applied",
              any("--app-name" in s for s in r["refusals"]) and r["effective"]["width"] == "300")
        r = run("bad-urgency", "[urgency=loud]\nwidth=1\n")
        check("invalid urgency value refused (L459)", any("loud" in s for s in r["refusals"]))
        r = run("unknown-global", "bogus=1\nwidth=42\n")
        check("unknown global key refused, others still applied",
              len(r["refusals"]) == 1 and r["effective"]["width"] == "42")
        r = run("invisible-global", "invisible=1\n")
        check("invisible refused in global section (L540-545)",
              any("criteria-only" in s for s in r["refusals"]) and r["effective"]["invisible"] == "0")
        r = run("include-in-criteria", "[app-name=x]\ninclude=/etc/hosts\n", app_name="x")
        check("include inside criteria refused (L45)", any("global section" in s for s in r["refusals"]))
        r = run("spaced-criteria", "[app-name = foo]\nwidth=1\n", app_name="foo")
        check("spaces around = in criteria refused (L507)",
              any("=value" in s for s in r["refusals"]) and r["effective"]["width"] == "300")
        r = run("bad-anchor", "anchor=middle\n")
        check("enumerated value validated (L410-416)",
              len(r["refusals"]) == 1 and r["effective"]["anchor"] == "top-right")
        r = run("unterminated", '[app-name="foo]\nwidth=1\n', app_name="foo")
        check("unterminated quote refused (L497-508)", any("unterminated" in s for s in r["refusals"]))
        r = run("regex-field", "[summary~=hel+o]\nwidth=1\n", inputs={"summary": "say helllo"})
        check("summary~ is an unanchored POSIX ERE search (L450, criteria.c regexec)",
              r["effective"]["width"] == "1" and r["refusals"] == [])
        r = run("regex-class", "[summary~=^[[:digit:]]+$]\nwidth=2\n[body~=\\\\d]\nheight=3\n",
                inputs={"summary": "2026", "body": "d"})
        check("POSIX bracket class matches and \\d is a literal d, not Python's digit class",
              r["effective"]["width"] == "2" and r["effective"]["height"] == "3" and r["refusals"] == [])
        r = run("regex-locale", "[summary~=^.$]\nwidth=4\n", inputs={"summary": "\u00e9"})
        check("regex matches bytes in the C locale: one '.' does not span a two-byte UTF-8 character",
              r["effective"]["width"] == "300" and r["refusals"] == [])
        r = run("regex-quote-escape", '[summary~="1\\.0"]\nwidth=5\n', inputs={"summary": "1x0"})
        check("a backslash inside quotes escapes the next character before regcomp (parse_criteria)",
              r["effective"]["width"] == "5" and r["refusals"] == [])
        r = run("regex-invalid", "[summary~=a(b]\nwidth=6\n", inputs={"summary": "a(b"})
        check("a pattern regcomp rejects is refused, not applied",
              any("regcomp" in s for s in r["refusals"]) and r["effective"]["width"] == "300")
        r = run("regex-both", "[summary=x summary~=x]\nwidth=7\n", inputs={"summary": "x"})
        check("summary with summary~ in one section is refused (criteria.c cannot set both)",
              any("both" in s for s in r["refusals"]) and r["effective"]["width"] == "300")
        r = run("regex-no-input", "[body~=x]\nwidth=8\n")
        check("a regex field without its input is refused, not applied",
              any("--body" in s for s in r["refusals"]) and r["effective"]["width"] == "300")
        exact = "[summary=hello category=im.received]\nwidth=9\n"
        r = run("string-fields", exact, inputs={"summary": "hello", "category": "im.received"})
        check("summary and category exact match applies (L447, L461)", r["effective"]["width"] == "9")
        r = run("string-fields-miss", exact, inputs={"summary": "Hello", "category": "im.received"})
        check("summary is case-sensitive exact match (L447)", r["effective"]["width"] == "300")
        r = run("string-field-no-input", "[desktop-entry=org.foo]\nwidth=9\n")
        check("string field without input refused, not applied",
              any("--desktop-entry" in s for s in r["refusals"]) and r["effective"]["width"] == "300")
        r = run("bool-bare", "[actionable]\nwidth=9\n", flags={"actionable": True})
        check("bare boolean field matches true (L514)", r["effective"]["width"] == "9")
        r = run("bool-negated", "[!actionable]\nwidth=9\n", flags={"actionable": True})
        check("negated bare boolean skips a true notification (L516)", r["effective"]["width"] == "300")
        r = run("bool-casefold", "[expiring=FALSE]\nwidth=9\n", flags={"expiring": False})
        check("boolean value case-insensitive (types.c parse_boolean)", r["effective"]["width"] == "9")
        r = run("bool-invalid", "[expiring=yes]\nwidth=9\n", flags={"expiring": True})
        check("invalid boolean value refused (L510)",
              any("expiring 'yes'" in s for s in r["refusals"]) and r["effective"]["width"] == "300")
        r = run("bool-no-input", "[expiring=false]\nwidth=9\n")
        check("boolean field without its flag refused, not applied",
              any("--expiring" in s for s in r["refusals"]) and r["effective"]["width"] == "300")
        r = run("bool-bare-other", "[grouped]\nwidth=9\n")
        check("bare second-pass token refused (L474-479)", any("grouped" in s for s in r["refusals"]))
        r = run("option-bool-word", "[mode=do-not-disturb]\ninvisible=true\n[mode=do-not-disturb app-name=n]\n"
                "invisible=False\n", app_name="n", modes=["do-not-disturb"])
        check("option booleans accept true/false any case, reported 0|1 (config.c parse_boolean)",
              r["effective"]["invisible"] == "0" and r["refusals"] == [])
        r = run("option-bool-bad", "icons=yes\n")
        check("option boolean outside true/false/0/1 refused",
              len(r["refusals"]) == 1 and r["effective"]["icons"] == "1")
        r = run("global-only-in-criteria", "[app-name=x]\nmax-history=2\n", app_name="x")
        check("max-history refused in criteria (L28)",
              any("global-only" in s for s in r["refusals"]) and r["effective"]["max-history"] == "5")
        escape = {"home/inc.ini": ("symlink", "outside/secret.ini"), "outside/secret.ini": "width=666\n"}
        r = run("escape-symlink", "include=~/inc.ini\n", extra=escape, roots=())
        check("symlinked include escaping --home refused, not read (containment)",
              any("outside the declared read roots" in s for s in r["refusals"])
              and r["effective"]["width"] == "300")
        r = run("escape-declared", "include=~/inc.ini\n", extra=escape, roots=("outside",))
        check("escaping include read once its root is declared with --read-root",
              r["effective"]["width"] == "666" and r["refusals"] == [])
        r = run("escape-dotdot", "include=~/../outside/secret.ini\n",
                extra={"outside/secret.ini": "width=666\n"}, roots=())
        check("~/.. include escaping --home refused (containment)",
              any("outside the declared read roots" in s for s in r["refusals"])
              and r["effective"]["width"] == "300")
        r = run("inside-symlink", "include=~/inc.ini\n",
                extra={"home/inc.ini": ("symlink", "home/real/core.ini"), "home/real/core.ini": "width=444\n"},
                roots=())
        check("symlinked include resolving inside --home is read",
              r["effective"]["width"] == "444" and r["refusals"] == [])
        r = run("prefix-sibling", "include=@BASE@/home-evil/x.ini\n",
                extra={"home-evil/x.ini": "width=666\n"}, roots=())
        check("a sibling sharing the --home prefix is outside the root",
              any("outside the declared read roots" in s for s in r["refusals"])
              and r["effective"]["width"] == "300")
        r = run("nul-include", "include=~/a\x00b\n", roots=())
        check("an include path with a NUL byte is refused, not a crash",
              any("not a valid path" in s for s in r["refusals"]))
        r = run("double-slash", "include=~//inc.ini\n", extra={"home/inc.ini": "width=321\n"}, roots=())
        check("~//x stays under --home (config.c joins $HOME/ + rest)", r["effective"]["width"] == "321")
        r = run("trailing-slash", "include=~/inc.ini/\n", extra={"home/inc.ini": "width=321\n"}, roots=())
        check("an include path with a trailing / is refused", r["effective"]["width"] == "300"
              and any("trailing" in s for s in r["refusals"]))
        r = run("symlinked-root", "include=@BASE@/rootlink/x.ini\n",
                extra={"rootlink": ("symlink", "outside"), "outside/x.ini": "width=432\n"}, roots=("rootlink",))
        check("a symlinked read root counts as its resolved target", r["effective"]["width"] == "432"
              and r["refusals"] == [])
    finally:
        shutil.rmtree(work)

    failed = [name for name, ok in checks if not ok]
    for name in failed:
        print("FAIL " + name, file=sys.stderr)
    print("MADO_MAKO_SELFTEST: checks=" + str(len(checks)) + " failed=" + str(len(failed)), file=sys.stderr)
    return 0 if not failed else 1


def main(argv):
    parser = argparse.ArgumentParser(prog="mado-mako.py")
    parser.add_argument("--config")
    parser.add_argument("--home")
    parser.add_argument("--app-name")
    parser.add_argument("--urgency", choices=URGENCIES)
    for field in STRING_INPUT_FIELDS:
        parser.add_argument("--" + field)
    for field in BOOLEAN_FIELDS:
        parser.add_argument("--" + field, choices=("true", "false"))
    parser.add_argument("--mode", action="append", default=[])
    parser.add_argument("--read-root", action="append", default=[])
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--scratch-root")
    args = parser.parse_args(argv)

    if args.selftest:
        if not args.scratch_root:
            return setup_error("--selftest requires --scratch-root")
        return selftest(args.scratch_root)
    if not args.config:
        return setup_error("--config is required")
    config = os.path.realpath(args.config)
    try:
        info = os.stat(config)
    except OSError as exc:
        return setup_error("cannot stat --config: " + str(exc.strerror))
    if not stat.S_ISREG(info.st_mode):
        return setup_error("--config is not a regular file (after symlink resolution)")
    if not os.access(config, os.R_OK):
        return setup_error("--config is not readable")

    home = args.home
    for name, path in [("--home", home)] + [("--read-root", root) for root in args.read_root]:
        if path is not None and not os.path.isabs(path):
            return setup_error(name + " must be an absolute path: " + repr(path))
    modes = set(INITIAL_MODES) | set(args.mode)
    inputs = {field: getattr(args, field.replace("-", "_")) for field in STRING_INPUT_FIELDS}
    inputs = {field: value for field, value in inputs.items() if value is not None}
    flags = {field: getattr(args, field) == "true" for field in BOOLEAN_FIELDS
             if getattr(args, field) is not None}
    result = resolve(config, home, args.app_name, args.urgency, modes, inputs, flags, args.read_root)
    print(json.dumps(result, sort_keys=True))
    print("MADO_MAKO: resolved=" + str(len(result["effective"]))
          + " refusals=" + str(len(result["refusals"])), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
