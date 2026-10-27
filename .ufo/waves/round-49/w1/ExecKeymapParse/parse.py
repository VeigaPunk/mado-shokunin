#!/usr/bin/env python3
"""parse.py - parse a libxkbcommon-1.13.2 SERIALIZED keymap and derive the
(keycode, layout, level) -> keysym table that `xkbcli how-to-type` implies.

Input contract
==============
The only accepted input is the text emitted by
`xkb_keymap_get_as_string2(keymap, <output format>, <flags>)` as produced by
the pinned `/usr/lib/xkbcommon/xkbcli-compile-keymap` with its default flags
(pretty-printed, unused types kept, output format = the input format = 2 /
TEXT_V2, i.e. `DEFAULT_KEYMAP_SERIALIZE_FLAGS` behind `xkbcli`).

That is NOT a raw XKB source tree.  Rejected with OutOfContract, because the
serializer never emits them:

  * `include`, `default`, `replace`, `augment`, `override` statements/prefixes
  * `xkb_geometry` sections (compile-keymap output has no geometry)
  * `#`, `//`, `/* */` comments
  * `$VAR` / `%`-style substitution or `!` flags
  * non-contiguous `symbols[GroupN]` / `type[GroupN]` indices (the serializer
    writes every group 1..num_groups in order, so a gap cannot come from it)
  * string escapes other than `\\n`, `\\\\` and the 5-char `\\0ooo` octal form
  * `action= { ... };` blocks holding action *fields*: the serializer only uses
    the block form to concatenate whole action calls (V2 multi-action levels)

Semantics modelled on libxkbcommon 1.13.2, the pinned judge:
  src/xkbcomp/keymap-dump.c  what the serializer can emit (and in what order)
  src/xkbcomp/keycodes.c     <NAME> = N, aliases
  src/xkbcomp/types.c        a type's num_levels = max(1, highest map[] level)
  src/xkbcomp/symbols.c      NoSymbol drop, trailing empty-level trim,
                             FindAutomaticType width rule, num_groups rule
  src/keymap.c               num_levels_for_key / get_syms_by_level boundaries
  tools/how-to-type.c        which cells reach the table (single keysym per
                             level, named keys, ascending keycode order)

Public API
==========
  parse(text) -> Keymap
  Keymap.table()          [(keycode, layout0, level0, [keysym, ...]), ...]
  Keymap.judge_cells()    the cells how-to-type really prints: one keysym
                          AND at least one modifier mask (keymap.c
                          xkb_keymap_key_get_mods_for_level); a level-0 cell
                          is shadowed when the key type has a printed
                          `map[none]= N` entry (numpad:mac's KEYPAD)
  Keymap.unreachable_cells() single-keysym cells with no mask
  Keymap.judge_positions(spelling)  rows the judge prints for one keysym
  Keymap.positions(name)  [(keycode, layout0, level0)] for one keysym spelling
  Keymap.distinct_spellings()
  census(text) -> Counter of serialized constructs
  parse_census(text) -> (Keymap, Counter, stats)

CLI
===
  parse.py selftest              inline assertions, exit 0 iff all pass
  parse.py dump FILE...          JSON tables + stats per file
  parse.py census FILE...        construct<TAB>count totals + per-file stats
"""

import collections
import hashlib
import json
import re
import sys

__all__ = [
    "OutOfContract", "ParseError", "Keymap", "parse", "census",
    "parse_census", "unescape", "spelling_class",
]


class OutOfContract(Exception):
    """The input uses a construct the pinned serializer never emits."""


class ParseError(Exception):
    """The input claims to be serializer output but is malformed."""


# ------------------------------------------------------------------- lexing

WORD_RE = re.compile(r"[A-Za-z0-9_]+")
IDENT_RE = re.compile(r"[A-Za-z0-9_]+\Z")
HEX_RE = re.compile(r"0[xX][0-9A-Fa-f]+\Z")
DEC_RE = re.compile(r"[0-9]+\Z")
UNICODE_SPELLING_RE = re.compile(r"U[0-9A-Fa-f]{4,6}\Z")
KEYNAME_RE = re.compile(r"[A-Za-z0-9_+\-]+\Z")
PUNCT = set("{}[]()=;,+-.*/!")

SECTIONS = ("xkb_keycodes", "xkb_types", "xkb_compatibility", "xkb_symbols")
OUT_OF_CONTRACT_SECTIONS = ("xkb_geometry",)

# keymap-dump.c check_write_string_literal()
ESCAPES_EMITTED = {"n": "\n", "\\": "\\"}


class Token:
    __slots__ = ("kind", "text", "value", "line", "col")

    def __init__(self, kind, text, value, line, col):
        self.kind = kind  # ident | number | string | keyname | punct | eof
        self.text = text
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return "Token(%s,%r,%d:%d)" % (self.kind, self.text, self.line, self.col)


def unescape(raw, line=0, col=0):
    """Decode a string body exactly as the serializer escapes it."""
    out = []
    i = 0
    n = len(raw)
    while i < n:
        c = raw[i]
        if c != "\\":
            out.append(c)
            i += 1
            continue
        if i + 1 >= n:
            raise OutOfContract("%d:%d: dangling backslash in string" % (line, col))
        e = raw[i + 1]
        if e in ESCAPES_EMITTED:
            out.append(ESCAPES_EMITTED[e])
            i += 2
            continue
        if e == "0":
            if i + 4 >= n:
                raise OutOfContract("%d:%d: short octal escape" % (line, col))
            digits = raw[i + 2:i + 5]
            if not re.fullmatch(r"[0-7]{3}", digits):
                raise OutOfContract("%d:%d: malformed octal escape \\0%s"
                                    % (line, col, digits))
            out.append(chr(int(digits, 8)))
            i += 5
            continue
        raise OutOfContract("%d:%d: escape \\%s is not emitted by the serializer"
                            % (line, col, e))
    return "".join(out)


KP_MIN = 0xFF80   # XKB_KEY_KP_Space
KP_MAX = 0xFFBD   # XKB_KEY_KP_Equal
# XKB_KEY_KP_BackTab is 0x1000ff75: the only canonical KP_* name outside
# [KP_Space, KP_Equal] (verified against the pinned header by census.py).
KP_NAME_OUTLIERS = {"KP_BackTab"}


def is_keypad_spelling(spelling):
    """xkb_keysym_is_keypad(ks) == KP_Space <= ks <= KP_Equal, decided from a
    serializer spelling: every keysym in that value range has a canonical KP_*
    name, and every KP_* name except KP_BackTab lies in the range."""
    kind = spelling_class(spelling)
    if kind == "named":
        return spelling.startswith("KP_") and spelling not in KP_NAME_OUTLIERS
    if kind == "hex":
        value = int(spelling, 16)
        return KP_MIN <= value <= KP_MAX
    if kind == "unicode":
        return KP_MIN <= 0x01000000 + int(spelling[1:], 16) <= KP_MAX
    return False


def spelling_class(spelling):
    if spelling == "NoSymbol":
        return "nosymbol"
    if HEX_RE.match(spelling):
        return "hex"
    if UNICODE_SPELLING_RE.match(spelling):
        return "unicode"
    return "named"


def lex(text, counts):
    toks = []
    i = 0
    n = len(text)
    line = 1
    col = 1

    def advance(k):
        nonlocal i, line, col
        chunk = text[i:i + k]
        nl = chunk.count("\n")
        if nl:
            line += nl
            col = len(chunk) - chunk.rfind("\n")
        else:
            col += k
        i += k

    while i < n:
        c = text[i]
        if c in " \t\r\n":
            advance(1)
            continue
        if c == "#" or text.startswith("//", i) or text.startswith("/*", i):
            raise OutOfContract("%d:%d: comment (never emitted)" % (line, col))
        if c == '"':
            start_line, start_col = line, col
            j = i + 1
            while True:
                if j >= n:
                    raise ParseError("%d:%d: unterminated string" % (start_line, start_col))
                if text[j] == "\\":
                    j += 2
                    continue
                if text[j] == '"':
                    break
                j += 1
            body = text[i + 1:j]
            for esc in re.finditer(r"\\(.)", body, re.S):
                e = esc.group(1)
                if e == "n":
                    counts["escape_newline"] += 1
                elif e == "\\":
                    counts["escape_backslash"] += 1
                elif e == "0":
                    counts["escape_octal"] += 1
                else:
                    raise OutOfContract("%d:%d: escape \\%s is not emitted by "
                                        "the serializer" % (start_line, start_col, e))
            counts["string"] += 1
            if any(ord(ch) > 0x7E for ch in body):
                counts["string_nonascii"] += 1
            value = unescape(body, start_line, start_col)
            toks.append(Token("string", text[i:j + 1], value, start_line, start_col))
            advance(j + 1 - i)
            continue
        if c == "<":
            start_line, start_col = line, col
            j = text.find(">", i + 1)
            if j < 0:
                raise ParseError("%d:%d: unterminated key name" % (start_line, start_col))
            inner = text[i + 1:j]
            if not KEYNAME_RE.match(inner):
                raise OutOfContract("%d:%d: key name <%s> outside "
                                    "[A-Za-z0-9_+-]+" % (start_line, start_col, inner))
            toks.append(Token("keyname", text[i:j + 1], inner, start_line, start_col))
            counts["keyname"] += 1
            advance(j + 1 - i)
            continue
        if c in PUNCT:
            toks.append(Token("punct", c, c, line, col))
            advance(1)
            continue
        m = WORD_RE.match(text, i)
        if m:
            word = m.group(0)
            if HEX_RE.match(word):
                toks.append(Token("number", word, int(word, 16), line, col))
            elif DEC_RE.match(word):
                toks.append(Token("number", word, int(word, 10), line, col))
            else:
                toks.append(Token("ident", word, word, line, col))
            advance(len(word))
            continue
        raise OutOfContract("%d:%d: character %r is not emitted by the serializer"
                            % (line, col, c))
    toks.append(Token("eof", "", None, line, col))
    return toks


# -------------------------------------------------------------- data model

class TypeDef:
    __slots__ = ("name", "num_levels", "map_entries", "preserve", "level_names",
                 "modifiers", "line")

    def __init__(self, name, line=0):
        self.name = name
        self.num_levels = 1     # types.c: KeyTypeInfo.num_levels starts at 1
        self.map_entries = []   # [(level1based, mask-string)]
        self.preserve = []      # [(mask-string, mask-string)]
        self.level_names = {}   # level1based -> string
        self.modifiers = None
        self.line = line

    def has_none_entry(self):
        """types.c prints map[None]= N only when N > 1 (level 1 entries with no
        preserve are omitted), so a parsed `map[none]= N` entry always targets a
        level >= 2.  keymap.c's level-0 special case suppresses the implicit
        empty mask when such an entry exists."""
        return any(mask == "none" for _, mask in self.map_entries)

    def targeted_levels(self):
        """1-based levels that some printed map entry targets, plus the
        implicit level 1 (unless a `none` entry shadows it)."""
        levels = {lvl for lvl, _ in self.map_entries}
        if not self.has_none_entry():
            levels.add(1)
        return levels

    def as_json(self):
        return {"name": self.name, "num_levels": self.num_levels,
                "map": self.map_entries, "preserve": self.preserve,
                "level_names": {str(k): v for k, v in self.level_names.items()},
                "modifiers": self.modifiers}


class Group:
    __slots__ = ("levels", "type_name", "has_symbols")

    def __init__(self):
        self.levels = []       # [[keysym spelling, ...], ...] trimmed
        self.type_name = None  # explicit type[GroupN]
        self.has_symbols = False

    def width(self):
        return len(self.levels)


class Key:
    __slots__ = ("name", "keycode", "groups", "default_type", "repeat",
                 "virtual_mods", "groups_clamp", "groups_redirect", "line")

    def __init__(self, name, keycode, line=0):
        self.name = name
        self.keycode = keycode
        self.groups = {}
        self.default_type = None
        self.repeat = None
        self.virtual_mods = None
        self.groups_clamp = False
        self.groups_redirect = None
        self.line = line


class Keymap:
    def __init__(self):
        self.keycodes = {}
        self.aliases = {}
        self.keycodes_min = None
        self.keycodes_max = None
        self.section_names = {}
        self.types = []            # definition order; types[0] is the fallback
        self.types_by_name = {}
        self.group_names = {}      # 1-based -> name
        self.keys = {}             # keycode -> Key
        self.modifier_maps = []    # [(modifier, [key name, ...])]
        self.counts = collections.Counter()
        self.stats = {}

    # -- resolution -------------------------------------------------
    def keycode_of(self, name):
        if name in self.keycodes:
            return self.keycodes[name]
        real = self.aliases.get(name)
        if real is None:
            return None
        if real in self.keycodes:
            return self.keycodes[real]
        real2 = self.aliases.get(real)
        if real2 is not None:
            return self.keycodes.get(real2)
        return None

    def default_type(self):
        return self.types[0] if self.types else TypeDef("ONE_LEVEL")

    def type_levels(self, type_name):
        t = self.types_by_name.get(type_name)
        if t is None:
            # symbols.c FindTypeForGroup: undefined type -> types[0]
            self.counts["type_undefined_fallback"] += 1
            return self.default_type().num_levels
        return t.num_levels

    @staticmethod
    def automatic_levels(width, default_levels):
        """symbols.c FindAutomaticType: 1 level for width<=1, 2 for width 2,
        4 for width 3..4; width>4 has no automatic type (falls back to
        types[0]).  Which concrete type is chosen does not matter here: every
        automatic type for a given width has exactly that many levels."""
        if width <= 1:
            return 1
        if width == 2:
            return 2
        if width <= 4:
            return 4
        return default_levels

    # -- model ------------------------------------------------------
    def resolved_keys(self):
        """(keycode, Key) in ascending keycode order - how-to-type walks
        min..max keycode and skips unnamed keys."""
        return [(kc, self.keys[kc]) for kc in sorted(self.keys)]

    def num_groups(self, key):
        """symbols.c: a group extends num_groups when it has levels left after
        the trailing-empty trim, or an explicit type."""
        n = 0
        for g in sorted(key.groups):
            grp = key.groups[g]
            has_explicit = grp.type_name is not None or key.default_type is not None
            if grp.width() > 0 or has_explicit:
                n = max(n, g + 1)
        return n

    def automatic_type_name(self, key, g):
        """symbols.c FindAutomaticType, at the granularity that matters: the
        automatic type for a width is 1/2/4 levels, and only the KEYPAD branch
        differs in which levels carry a modifier mask.  ALPHABETIC vs TWO_LEVEL
        and the FOUR_LEVEL_* family agree on `targeted_levels()`; census.py
        records `automatic_reachability_split=0` over the corpus, i.e. this
        granularity never hid a difference."""
        grp = key.groups.get(g)
        width = grp.width() if grp else 0
        syms0 = grp.levels[0][0] if grp and grp.levels and grp.levels[0] else ""
        syms1 = grp.levels[1][0] if grp and len(grp.levels) > 1 and grp.levels[1] else ""
        keypad = is_keypad_spelling(syms0) or is_keypad_spelling(syms1)
        if width <= 1:
            name = "ONE_LEVEL"
        elif width == 2:
            name = "KEYPAD" if keypad else "TWO_LEVEL"
        elif width <= 4:
            name = "FOUR_LEVEL_KEYPAD" if keypad else "FOUR_LEVEL"
        else:
            name = self.default_type().name
        if name not in self.types_by_name:
            name = self.default_type().name
        return name

    def group_type(self, key, g):
        grp = key.groups.get(g)
        explicit = None
        if grp is not None and grp.type_name is not None:
            explicit = grp.type_name
        elif key.default_type is not None:
            explicit = key.default_type
        if explicit is not None:
            return self.types_by_name.get(explicit) or self.default_type()
        return self.types_by_name.get(self.automatic_type_name(key, g)) or \
            self.default_type()

    def group_type_levels(self, key, g):
        grp = key.groups.get(g)
        width = grp.width() if grp else 0
        explicit = None
        if grp is not None and grp.type_name is not None:
            explicit = grp.type_name
        elif key.default_type is not None:
            explicit = key.default_type
        if explicit is not None:
            return self.type_levels(explicit)
        return self.automatic_levels(width, self.default_type().num_levels)

    def level_has_mask(self, key, g, level):
        """keymap.c xkb_keymap_key_get_mods_for_level returns at least one mask
        for this level (how-to-type prints a row only then).  Exact on the
        serialized text, because the judge re-parses that same text: the
        implicit empty mask for level 0 is suppressed by any printed `none`
        entry, and a level > 0 needs a printed entry targeting it."""
        td = self.group_type(key, g)
        return (level + 1) in td.targeted_levels()

    def table(self):
        """(keycode, layout0, level0, [spelling...]) in how-to-type's order.

        Levels are resized to the group type's num_levels exactly as
        symbols.c does (pad with empty levels, clear extras)."""
        rows = []
        for kc, key in self.resolved_keys():
            for g in range(self.num_groups(key)):
                grp = key.groups.get(g)
                levels = list(grp.levels) if grp else []
                nlev = self.group_type_levels(key, g)
                if len(levels) < nlev:
                    levels.extend([] for _ in range(nlev - len(levels)))
                elif len(levels) > nlev:
                    self.counts["level_cleared_by_type"] += len(levels) - nlev
                    levels = levels[:nlev]
                for level, syms in enumerate(levels):
                    rows.append((kc, g, level, list(syms)))
        return rows

    def single_rows(self):
        return [r for r in self.table() if len(r[3]) == 1]

    def judge_cells(self, spelling=None):
        """Cells how-to-type actually prints: one keysym AND at least one
        modifier mask for that level."""
        out = []
        for kc, key in self.resolved_keys():
            for g in range(self.num_groups(key)):
                grp = key.groups.get(g)
                levels = list(grp.levels) if grp else []
                nlev = self.group_type_levels(key, g)
                if len(levels) < nlev:
                    levels.extend([] for _ in range(nlev - len(levels)))
                elif len(levels) > nlev:
                    levels = levels[:nlev]
                for level, syms in enumerate(levels):
                    if len(syms) != 1:
                        continue
                    if not self.level_has_mask(key, g, level):
                        continue
                    if spelling is not None and syms[0] != spelling:
                        continue
                    out.append((kc, g, level, syms[0]))
        return out

    def positions(self, spelling):
        """Every single-keysym cell for this spelling (mask-independent)."""
        return [(kc, g, lvl) for (kc, g, lvl, syms) in self.table()
                if len(syms) == 1 and syms[0] == spelling]

    def judge_positions(self, spelling):
        """(keycode, layout0, level0) rows the judge prints for this spelling."""
        return [(kc, g, lvl) for (kc, g, lvl, _s) in self.judge_cells(spelling)]

    def unreachable_cells(self):
        """Single-keysym cells the judge does not print (no modifier mask)."""
        out = []
        for kc, key in self.resolved_keys():
            for g in range(self.num_groups(key)):
                grp = key.groups.get(g)
                levels = list(grp.levels) if grp else []
                nlev = self.group_type_levels(key, g)
                levels.extend([] for _ in range(max(0, nlev - len(levels))))
                for level, syms in enumerate(levels[:nlev]):
                    if len(syms) == 1 and not self.level_has_mask(key, g, level):
                        out.append((kc, g, level, syms[0]))
        return out

    def distinct_spellings(self):
        seen = set()
        out = []
        for (_, _, _, syms) in self.table():
            for s in syms:
                if s not in seen and s != "NoSymbol":
                    seen.add(s)
                    out.append(s)
        return out

    def as_json(self, include_table=True):
        d = {
            "keycodes": dict(sorted(self.keycodes.items())),
            "aliases": dict(sorted(self.aliases.items())),
            "keycodes_min": self.keycodes_min,
            "keycodes_max": self.keycodes_max,
            "section_names": self.section_names,
            "types": [t.as_json() for t in self.types],
            "group_names": {str(k): v for k, v in sorted(self.group_names.items())},
            "modifier_maps": [{"modifier": m, "keys": k}
                              for m, k in self.modifier_maps],
            "keys": [
                {"name": key.name, "keycode": kc,
                 "num_groups": self.num_groups(key),
                 "default_type": key.default_type,
                 "groups": [
                     {"index": g + 1,
                      "type": (key.groups[g].type_name if g in key.groups else None),
                      "levels": (key.groups[g].levels if g in key.groups else [])}
                     for g in range(self.num_groups(key))
                 ]}
                for kc, key in self.resolved_keys()
            ],
            "stats": self.stats,
            "counts": dict(sorted(self.counts.items())),
        }
        if include_table:
            d["table"] = [{"keycode": kc, "layout": g + 1, "level": lvl,
                           "syms": syms}
                          for (kc, g, lvl, syms) in self.table()]
        return d


# -------------------------------------------------------------- the parser

class Parser:
    def __init__(self, text):
        self.counts = collections.Counter()
        self.toks = lex(text, self.counts)
        self.i = 0
        self.km = Keymap()
        self.km.counts = self.counts

    # -- token helpers ----------------------------------------------
    def peek(self, k=0):
        return self.toks[self.i + k]

    def next(self):
        t = self.toks[self.i]
        self.i += 1
        return t

    def at(self, kind, text=None):
        t = self.peek()
        return t.kind == kind and (text is None or t.text == text)

    def at_close(self):
        return self.at("punct", "}")

    def err(self, tok, msg):
        return ParseError("%d:%d: %s (got %r)" % (tok.line, tok.col, msg, tok.text))

    def expect_punct(self, ch):
        t = self.next()
        if t.kind != "punct" or t.text != ch:
            raise self.err(t, "expected %r" % ch)
        return t

    def accept_punct(self, ch):
        if self.at("punct", ch):
            self.i += 1
            return True
        return False

    def expect_ident(self, word=None):
        t = self.next()
        if t.kind != "ident":
            raise self.err(t, "expected identifier%s" % (" %r" % word if word else ""))
        if word is not None and t.text != word:
            raise self.err(t, "expected %r" % word)
        return t

    def expect_number(self):
        t = self.next()
        if t.kind != "number":
            raise self.err(t, "expected number")
        return t.value

    def expect_string(self):
        t = self.next()
        if t.kind != "string":
            raise self.err(t, "expected string")
        return t.value

    def expect_keyname(self):
        t = self.next()
        if t.kind != "keyname":
            raise self.err(t, "expected <KEYNAME>")
        return t.value

    # -- grammar ----------------------------------------------------
    def parse(self):
        self.expect_ident("xkb_keymap")
        if self.at("string"):
            self.next()
        self.expect_punct("{")
        while not self.at_close():
            self.section()
        self.expect_punct("}")
        self.expect_punct(";")
        if self.peek().kind != "eof":
            raise self.err(self.peek(), "trailing tokens after xkb_keymap")
        self.finish()
        return self.km

    def section(self):
        t = self.next()
        if t.kind != "ident":
            raise self.err(t, "expected section header")
        name = t.text
        if name in OUT_OF_CONTRACT_SECTIONS:
            raise OutOfContract("%d:%d: %s section (compile-keymap never emits it)"
                                % (t.line, t.col, name))
        if name not in SECTIONS:
            raise self.err(t, "unknown section %r" % name)
        if self.at("string"):
            self.km.section_names[name] = self.next().value
            self.counts["section_%s_quoted" % name] += 1
        else:
            self.km.section_names[name] = None
            self.counts["section_%s_bare" % name] += 1
        self.counts["section_%s" % name] += 1
        self.expect_punct("{")
        {
            "xkb_keycodes": self.keycodes_body,
            "xkb_types": self.types_body,
            "xkb_compatibility": self.compat_body,
            "xkb_symbols": self.symbols_body,
        }[name]()
        self.expect_punct("}")
        self.expect_punct(";")

    # xkb_keycodes --------------------------------------------------
    def keycodes_body(self):
        while not self.at_close():
            t = self.peek()
            if t.kind == "keyname":
                self.next()
                name = t.value
                self.expect_punct("=")
                kc = self.expect_number()
                self.expect_punct(";")
                if name in self.km.keycodes:
                    self.counts["kc_duplicate_name"] += 1
                self.km.keycodes[name] = kc
                self.counts["kc_key"] += 1
                continue
            if t.kind != "ident":
                raise self.err(t, "expected keycodes statement")
            word = t.text
            self.next()
            if word == "minimum":
                self.expect_punct("=")
                self.km.keycodes_min = self.expect_number()
                self.expect_punct(";")
                self.counts["kc_minimum"] += 1
            elif word == "maximum":
                self.expect_punct("=")
                self.km.keycodes_max = self.expect_number()
                self.expect_punct(";")
                self.counts["kc_maximum"] += 1
            elif word == "indicator":
                self.expect_number()
                self.expect_punct("=")
                self.expect_string()
                self.expect_punct(";")
                self.counts["kc_indicator"] += 1
            elif word == "alias":
                alias = self.expect_keyname()
                self.expect_punct("=")
                real = self.expect_keyname()
                self.expect_punct(";")
                self.km.aliases[alias] = real
                self.counts["kc_alias"] += 1
            else:
                raise OutOfContract("%d:%d: keycodes statement %r is not emitted "
                                    "by the serializer" % (t.line, t.col, word))

    # xkb_types -----------------------------------------------------
    def masklist(self):
        """`none`, a numeric mask, or `A+B+...` of modifier names."""
        t = self.peek()
        if t.kind == "number":
            self.next()
            self.counts["mask_numeric"] += 1
            return "0x%x" % t.value
        if t.kind == "ident" and t.text == "none":
            self.next()
            self.counts["mask_none"] += 1
            return "none"
        parts = []
        while True:
            t = self.next()
            if t.kind != "ident":
                raise self.err(t, "expected modifier name")
            parts.append(t.text)
            self.counts["mask_modifier"] += 1
            if not self.accept_punct("+"):
                break
        return "+".join(parts)

    def types_body(self):
        while not self.at_close():
            t = self.peek()
            if t.kind != "ident":
                raise self.err(t, "expected types statement")
            word = t.text
            if word == "virtual_modifiers":
                self.next()
                self.vmod_list()
                self.expect_punct(";")
                self.counts["types_virtual_modifiers"] += 1
            elif word == "type":
                self.next()
                tname = self.expect_string()
                self.expect_punct("{")
                self.type_body(tname, t.line)
                self.expect_punct("}")
                self.expect_punct(";")
            else:
                raise OutOfContract("%d:%d: %r statement in xkb_types is not "
                                    "emitted by the serializer" % (t.line, t.col, word))

    def vmod_list(self):
        while True:
            self.expect_ident()
            if self.accept_punct("="):
                self.masklist()
                self.counts["types_vmod_explicit_mapping"] += 1
            if not self.accept_punct(","):
                break

    def type_body(self, name, line):
        td = TypeDef(name, line)
        self.counts["types_type"] += 1
        while not self.at_close():
            t = self.next()
            if t.kind != "ident":
                raise self.err(t, "expected type field")
            field = t.text
            if field == "modifiers":
                self.expect_punct("=")
                td.modifiers = self.masklist()
                self.expect_punct(";")
                self.counts["types_modifiers"] += 1
            elif field == "map":
                self.expect_punct("[")
                mask = self.masklist()
                self.expect_punct("]")
                self.expect_punct("=")
                lvl = self.expect_number()
                self.expect_punct(";")
                td.map_entries.append((lvl, mask))
                if lvl > td.num_levels:      # types.c AddMapEntry
                    td.num_levels = lvl
                self.counts["types_map_entry"] += 1
            elif field == "preserve":
                self.expect_punct("[")
                mask = self.masklist()
                self.expect_punct("]")
                self.expect_punct("=")
                preserved = self.masklist()
                self.expect_punct(";")
                td.preserve.append((mask, preserved))
                self.counts["types_preserve_entry"] += 1
            elif field == "level_name":
                self.expect_punct("[")
                lvl = self.expect_number()
                self.expect_punct("]")
                self.expect_punct("=")
                td.level_names[lvl] = self.expect_string()
                self.expect_punct(";")
                self.counts["types_level_name"] += 1
            else:
                raise OutOfContract("%d:%d: type field %r is not emitted by the "
                                    "serializer" % (t.line, t.col, field))
        if name in self.km.types_by_name:
            self.counts["types_duplicate_name"] += 1
        self.km.types.append(td)
        self.km.types_by_name[name] = td

    # xkb_compatibility ---------------------------------------------
    def compat_body(self):
        """Structurally parsed; the keysym table does not read compat, but the
        shapes are censused so a serializer drift shows up."""
        while not self.at_close():
            t = self.peek()
            if t.kind != "ident":
                raise self.err(t, "expected compatibility statement")
            head = t.text
            self.next()
            if self.accept_punct("."):
                dotted = self.expect_ident().text
                self.expect_punct("=")
                self.skip_simple_value()
                self.expect_punct(";")
                self.counts["compat_global_%s" % dotted] += 1
                self.counts["compat_global"] += 1
                continue
            if head == "interpret":
                self.counts["compat_interpret"] += 1
                self.interpret_head()
            elif head == "indicator":
                self.counts["compat_indicator"] += 1
                self.expect_string()
            elif head == "virtual_modifiers":
                self.vmod_list()
                self.expect_punct(";")
                self.counts["compat_virtual_modifiers"] += 1
                continue
            else:
                raise OutOfContract("%d:%d: compatibility statement %r is not "
                                    "emitted by the serializer" % (t.line, t.col, head))
            self.expect_punct("{")
            self.compat_block()
            self.expect_punct("}")
            self.expect_punct(";")

    def interpret_head(self):
        # <keysym>+<match>(<masklist>)   e.g. Shift_L+AnyOf(all)
        t = self.next()
        if t.kind not in ("ident", "number"):
            raise self.err(t, "expected interpret keysym")
        self.expect_punct("+")
        self.expect_ident()
        self.expect_punct("(")
        self.masklist()
        self.expect_punct(")")

    def skip_simple_value(self):
        while True:
            t = self.peek()
            if t.kind == "eof":
                raise self.err(t, "unterminated value")
            if t.kind == "punct" and t.text == ";":
                return
            if t.kind == "punct" and t.text in "{}":
                raise self.err(t, "unexpected brace in scalar value")
            self.next()

    def compat_block(self):
        while not self.at_close():
            t = self.next()
            if t.kind != "ident":
                raise self.err(t, "expected compatibility block field")
            field = t.text
            self.expect_punct("=")
            if field == "action":
                self.counts["compat_action"] += 1
                if self.accept_punct("{"):
                    # V2 multi-action block: whole action calls, comma separated
                    self.counts["compat_action_block"] += 1
                    while True:
                        self.action_call()
                        if not self.accept_punct(","):
                            break
                    self.expect_punct("}")
                else:
                    self.action_call()
                self.expect_punct(";")
            else:
                self.counts["compat_block_%s" % field] += 1
                self.skip_simple_value()
                self.expect_punct(";")

    def action_call(self):
        """`Name(args...)` with nested parentheses; args are not interpreted."""
        self.expect_ident()
        self.expect_punct("(")
        depth = 1
        while depth:
            x = self.next()
            if x.kind == "eof":
                raise self.err(x, "unterminated action call")
            if x.kind == "punct" and x.text == "(":
                depth += 1
            elif x.kind == "punct" and x.text == ")":
                depth -= 1
        self.counts["action_call"] += 1

    # xkb_symbols ---------------------------------------------------
    def symbols_body(self):
        while not self.at_close():
            t = self.peek()
            if t.kind != "ident":
                raise self.err(t, "expected symbols statement")
            word = t.text
            if word == "name":
                self.next()
                self.expect_punct("[")
                idx = self.expect_number()
                self.expect_punct("]")
                self.expect_punct("=")
                self.km.group_names[idx] = self.expect_string()
                self.expect_punct(";")
                self.counts["symbols_name_group"] += 1
            elif word == "key":
                self.next()
                self.key_def()
            elif word == "modifier_map":
                self.next()
                mod = self.expect_ident().text
                self.expect_punct("{")
                names = []
                while not self.at_close():
                    names.append(self.expect_keyname())
                    if not self.accept_punct(","):
                        break
                self.expect_punct("}")
                self.expect_punct(";")
                self.km.modifier_maps.append((mod, names))
                self.counts["symbols_modifier_map"] += 1
                self.counts["symbols_modifier_map_key"] += len(names)
            else:
                raise OutOfContract("%d:%d: symbols statement %r is not emitted "
                                    "by the serializer" % (t.line, t.col, word))

    def key_def(self):
        name_tok = self.peek()
        name = self.expect_keyname()
        kc = self.km.keycode_of(name)
        self.counts["symbols_key"] += 1
        key = Key(name, kc, name_tok.line)
        self.expect_punct("{")
        self.key_body(key)
        self.expect_punct("}")
        self.expect_punct(";")
        if kc is None:
            self.counts["symbols_key_unknown_in_keycodes"] += 1
            return
        if kc in self.km.keys:
            self.counts["symbols_key_duplicate"] += 1
        self.km.keys[kc] = key

    def key_body(self, key):
        saw_symbols = False
        while not self.at_close():
            t = self.peek()
            if t.kind == "punct" and t.text == "[":
                if saw_symbols:
                    raise OutOfContract("%d:%d: second anonymous symbol list in "
                                        "one key (serializer emits one per group)"
                                        % (t.line, t.col))
                grp = Group()
                grp.levels = self.level_list()
                grp.has_symbols = True
                key.groups[0] = grp
                self.counts["symbols_key_simple"] += 1
                saw_symbols = True
                self.accept_punct(",")
                continue
            if t.kind != "ident":
                raise self.err(t, "expected key field")
            field = t.text
            self.next()
            if field in ("type", "repeat", "virtualMods", "groupsRedirect",
                         "symbols", "actions"):
                if field in ("symbols", "actions"):
                    self.expect_punct("[")
                    idx = self.expect_number()
                    self.expect_punct("]")
                    self.expect_punct("=")
                    if field == "symbols":
                        grp = key.groups.get(idx - 1)
                        if grp is not None and grp.has_symbols:
                            raise OutOfContract("%d:%d: duplicate symbols[%d]"
                                                % (t.line, t.col, idx))
                        if grp is None:
                            grp = key.groups.setdefault(idx - 1, Group())
                        grp.levels = self.level_list()
                        grp.has_symbols = True
                        self.counts["symbols_symbols_group"] += 1
                    else:
                        self.action_level_list()
                        self.counts["symbols_actions_group"] += 1
                    self.accept_punct(",")
                    continue
                if field == "type":
                    if self.accept_punct("["):
                        idx = self.expect_number()
                        self.expect_punct("]")
                        self.expect_punct("=")
                        tname = self.expect_string()
                        grp = key.groups.setdefault(idx - 1, Group())
                        if grp.type_name is not None:
                            raise OutOfContract("%d:%d: duplicate type[%d]"
                                                % (t.line, t.col, idx))
                        grp.type_name = tname
                        self.counts["symbols_type_group"] += 1
                    else:
                        self.expect_punct("=")
                        if key.default_type is not None:
                            raise OutOfContract("%d:%d: duplicate type="
                                                % (t.line, t.col))
                        key.default_type = self.expect_string()
                        self.counts["symbols_type_default"] += 1
                    self.accept_punct(",")
                    continue
                self.expect_punct("=")
                if field == "repeat":
                    key.repeat = self.expect_ident().text
                    self.counts["symbols_repeat"] += 1
                elif field == "virtualMods":
                    key.virtual_mods = self.masklist()
                    self.counts["symbols_virtualMods"] += 1
                else:
                    key.groups_redirect = self.expect_number()
                    self.counts["symbols_groupsRedirect"] += 1
                self.accept_punct(",")
                continue
            if field == "groupsClamp":
                key.groups_clamp = True
                self.counts["symbols_groupsClamp"] += 1
                self.accept_punct(",")
                continue
            raise OutOfContract("%d:%d: key field %r is not emitted by the "
                                "serializer" % (t.line, t.col, field))
        if not saw_symbols and not any(g.has_symbols for g in key.groups.values()):
            self.counts["symbols_key_no_symbols"] += 1
        # Contiguity check (serializer emits every group in order).
        idxs = sorted(key.groups)
        if idxs and idxs != list(range(idxs[-1] + 1)):
            raise OutOfContract("%d:%d: non-contiguous group indices %s"
                                % (key.line, 0, idxs))

    def action_level_list(self):
        """`[ <action-call-or-group> (, ...)* ]`; action semantics are not
        needed for the keysym table, only the shape is validated."""
        self.expect_punct("[")
        while True:
            if self.accept_punct("]"):
                return
            if self.accept_punct("{"):
                while True:
                    self.action_call()
                    if not self.accept_punct(","):
                        break
                self.expect_punct("}")
            else:
                self.action_call()
            if not self.accept_punct(","):
                self.expect_punct("]")
                return

    def level_list(self):
        """`[ level (, level)* ]`; a level is a keysym or `{ sym, ... }`."""
        levels = []
        self.expect_punct("[")
        while True:
            if self.accept_punct("]"):
                break
            if self.accept_punct("{"):
                syms = []
                while True:
                    if self.accept_punct("}"):
                        break
                    syms.append(self.keysym_token())
                    if not self.accept_punct(","):
                        self.expect_punct("}")
                        break
                levels.append(syms)
                self.counts["level_multi_keysym"] += 1
            else:
                levels.append([self.keysym_token()])
            if not self.accept_punct(","):
                self.expect_punct("]")
                break
        cleaned = []
        for syms in levels:
            kept = [s for s in syms if s != "NoSymbol"]
            if len(kept) != len(syms):
                self.counts["level_nosymbol_dropped"] += len(syms) - len(kept)
            cleaned.append(kept)
        trimmed = len(cleaned)
        while trimmed and not cleaned[trimmed - 1]:
            trimmed -= 1
        if trimmed != len(cleaned):
            self.counts["level_trailing_trimmed"] += len(cleaned) - trimmed
        cleaned = cleaned[:trimmed]
        self.counts["level"] += len(cleaned)
        for syms in cleaned:
            if not syms:
                self.counts["level_empty"] += 1
            elif len(syms) == 1:
                self.counts["level_single"] += 1
            else:
                self.counts["level_multi"] += 1
        return cleaned

    def keysym_token(self):
        t = self.next()
        if t.kind not in ("ident", "number"):
            raise self.err(t, "expected keysym")
        self.counts["keysym_" + spelling_class(t.text)] += 1
        self.counts["keysym_token"] += 1
        return t.text

    # -- finalize ---------------------------------------------------
    def finish(self):
        km = self.km
        km.stats["keys"] = len(km.keys)
        km.stats["types"] = len(km.types)
        groups_hist = collections.Counter()
        levels_hist = collections.Counter()
        explicit = inferred = cells = 0
        inferred_width = collections.Counter()
        for kc, key in km.resolved_keys():
            n = km.num_groups(key)
            groups_hist[n] += 1
            for g in range(n):
                nlev = km.group_type_levels(key, g)
                levels_hist[nlev] += 1
                grp = key.groups.get(g)
                if (grp is not None and grp.type_name is not None) or \
                        key.default_type is not None:
                    explicit += 1
                else:
                    inferred += 1
                    inferred_width[grp.width() if grp else 0] += 1
                for syms in (grp.levels if grp else []):
                    cells += 1
                    if len(syms) == 1:
                        self.counts["cell_single"] += 1
                    elif not syms:
                        self.counts["cell_empty"] += 1
                    else:
                        self.counts["cell_multi"] += 1
        km.stats["groups_hist"] = {str(k): v for k, v in sorted(groups_hist.items())}
        km.stats["levels_hist"] = {str(k): v for k, v in sorted(levels_hist.items())}
        km.stats["keys_in_hist"] = sum(groups_hist.values())
        km.stats["group_slots"] = sum(n * c for n, c in groups_hist.items())
        km.stats["level_slots"] = sum(n * c for n, c in levels_hist.items())
        km.stats["group_explicit_type"] = explicit
        km.stats["group_inferred_type"] = inferred
        km.stats["inferred_width_hist"] = {str(k): v for k, v in
                                           sorted(inferred_width.items())}
        km.stats["cells"] = cells
        km.stats["distinct_spellings"] = len(km.distinct_spellings())
        km.stats["max_groups"] = max(groups_hist) if groups_hist else 0
        km.stats["max_levels"] = max(levels_hist) if levels_hist else 0
        km.stats["type_names"] = [t.name for t in km.types]
        km.stats["judge_cells"] = len(km.judge_cells())
        unreachable = km.unreachable_cells()
        km.stats["unreachable_cells"] = len(unreachable)
        self.counts["judge_cell_reachable"] += km.stats["judge_cells"]
        self.counts["judge_cell_unreachable"] += len(unreachable)
        for (kc, g, level, _sym) in unreachable:
            if level == 0:
                self.counts["judge_unreachable_level0"] += 1
            else:
                self.counts["judge_unreachable_levelN"] += 1
        for t in km.types:
            if t.has_none_entry():
                self.counts["type_none_entry"] += 1


def parse(text):
    return Parser(text).parse()


def parse_census(text):
    p = Parser(text)
    km = p.parse()
    data = text.encode("utf-8")
    km.stats["sha256"] = hashlib.sha256(data).hexdigest()
    km.stats["bytes"] = len(data)
    km.stats["lines"] = text.count("\n") + (0 if text.endswith("\n") else 1)
    return km, p.counts, km.stats


def census(text):
    _, counts, _ = parse_census(text)
    return counts


# --------------------------------------------------------------------- CLI

def _dump(files):
    out = []
    status = 0
    for path in files:
        with open(path, "rb") as f:
            text = f.read().decode("utf-8")
        try:
            km = parse(text)
        except (OutOfContract, ParseError) as exc:
            print("%s: %s: %s" % (path, type(exc).__name__, exc), file=sys.stderr)
            status = 1
            continue
        out.append({"file": path, "keymap": km.as_json()})
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
    sys.stdout.write("\n")
    return status


def _census(files):
    total = collections.Counter()
    per = []
    status = 0
    for path in files:
        with open(path, "rb") as f:
            text = f.read().decode("utf-8")
        try:
            _, counts, stats = parse_census(text)
        except (OutOfContract, ParseError) as exc:
            print("%s: %s: %s" % (path, type(exc).__name__, exc), file=sys.stderr)
            status = 1
            continue
        counts["keymap"] += 1
        for key in list(counts):
            total[key] += counts[key]
        per.append((path, stats, dict(counts)))
    for key in sorted(total):
        print("%s\t%d" % (key, total[key]))
    print("-- per keymap --")
    for path, stats, _ in per:
        print("%s\t%s" % (path, json.dumps(stats, sort_keys=True)))
    return status


def _selftest():
    cases = []

    def check(name, cond, detail=""):
        cases.append((name, bool(cond), detail))

    def rejects(name, text):
        try:
            parse(text)
        except (OutOfContract, ParseError):
            check(name, True)
        else:
            check(name, False, "accepted")

    text = """xkb_keymap {
xkb_keycodes "k" {
	minimum = 8;
	maximum = 255;
	<A> = 10;
	<B> = 11;
	<C> = 12;
	<D> = 13;
};
xkb_types "t" {
	virtual_modifiers Alt,Hyper=0x4000;
	type "ONE_LEVEL" {
		modifiers= none;
		level_name[1]= "Any";
	};
	type "TWO_LEVEL" {
		modifiers= Shift;
		map[Shift]= 2;
	};
	type "FOUR_LEVEL" {
		modifiers= Shift+LevelThree;
		map[Shift]= 2;
		map[LevelThree]= 3;
		map[Shift+LevelThree]= 4;
	};
};
xkb_compatibility "c" {
	interpret.useModMapMods= AnyLevel;
	interpret.repeat= False;
	interpret Shift_L+AnyOf(all) {
		virtualModifier= Alt;
		useModMapMods=level1;
		action= SetMods(modifiers=modMapMods,clearLocks);
	};
	interpret Any+AnyOfOrNone(all) {
		action= NoAction();
	};
};
xkb_symbols "s" {
	name[1]="One";
	key <A> { [ a, NoSymbol ] };
	key <B> { [ b, { c, d }, e ] };
	key <C> {
		type[1]= "FOUR_LEVEL",
		symbols[1]= [ f ]
	};
	key <D> { };
	modifier_map Shift { <A>, <B> };
};
};
"""
    km = parse(text)
    rows = {(kc, g, lvl): syms for (kc, g, lvl, syms) in km.table()}
    check("trailing-nosymbol-trim", rows.get((10, 0, 0)) == ["a"] and
          (10, 0, 1) not in rows)
    check("multi-keysym-level", rows.get((11, 0, 1)) == ["c", "d"])
    check("multi-pads-to-four", (11, 0, 3) in rows and rows[(11, 0, 3)] == [])
    check("explicit-type-pads", rows.get((12, 0, 3)) == [] and
          rows.get((12, 0, 0)) == ["f"])
    check("empty-key-no-groups", km.num_groups(km.keys[13]) == 0)
    check("type-levels", [t.num_levels for t in km.types] == [1, 2, 4])
    check("section-names", km.section_names["xkb_symbols"] == "s")
    check("group-name", km.group_names[1] == "One")
    check("modifier-map", km.modifier_maps == [("Shift", ["A", "B"])])
    check("positions", km.positions("a") == [(10, 0, 0)])
    check("distinct-spellings", km.distinct_spellings() ==
          ["a", "b", "c", "d", "e", "f"])
    check("counts-multi", km.counts["level_multi_keysym"] == 1)
    check("counts-trim", km.counts["level_trailing_trimmed"] == 1)
    check("counts-dropped", km.counts["level_nosymbol_dropped"] == 1)
    check("counts-interpret", km.counts["compat_interpret"] == 2)

    check("unescape-newline", unescape("a\\nb") == "a\nb")
    check("unescape-backslash", unescape("a\\\\b") == "a\\b")
    check("unescape-octal", unescape("a\\0042b") == 'a"b')
    try:
        unescape("a\\tb")
        check("unescape-rejects-tab", False)
    except OutOfContract:
        check("unescape-rejects-tab", True)

    rejects("comment-hash", "xkb_keymap {\n# hi\n};\n")
    rejects("comment-slash", "xkb_keymap {\n// hi\n};\n")
    rejects("comment-block", "xkb_keymap {\n/* hi */\n};\n")
    rejects("geometry", "xkb_keymap {\nxkb_geometry \"g\" {\n};\n};\n")
    rejects("include", "xkb_keymap {\nxkb_symbols \"s\" {\ninclude \"x\"\n};\n};\n")
    rejects("string-tab-escape",
            "xkb_keymap {\nxkb_symbols \"s\" {\nname[1]=\"a\\tb\";\n};\n};\n")
    rejects("group-gap",
            "xkb_keymap {\nxkb_keycodes \"k\" {\n<A> = 10;\n};\n"
            "xkb_symbols \"s\" {\nkey <A> { symbols[2]= [ a ] };\n};\n};\n")

    # reachability: a printed map[none]= 2 shadows level 1 (numpad:mac KEYPAD)
    text3 = """xkb_keymap {
xkb_keycodes "k" {
	<A> = 10;
};
xkb_types "t" {
	virtual_modifiers NumLock;
	type "ONE_LEVEL" {
		modifiers= none;
	};
	type "KEYPAD" {
		modifiers= none;
		map[none]= 2;
		level_name[2]= "Number";
	};
};
xkb_compatibility "c" {
};
xkb_symbols "s" {
	key <A> { [ KP_Home, KP_7 ] };
};
};
"""
    km3 = parse(text3)
    check("mac-keypad-level1-shadowed",
          km3.positions("KP_Home") == [(10, 0, 0)] and
          km3.judge_positions("KP_Home") == [])
    check("mac-keypad-level2-reachable",
          km3.judge_positions("KP_7") == [(10, 0, 1)])

    check("keypad-spelling", is_keypad_spelling("KP_Home") and
          not is_keypad_spelling("KP_BackTab") and
          is_keypad_spelling("0xff80") and not is_keypad_spelling("q"))
    check("spelling-class-named", spelling_class("dead_acute") == "named")
    check("spelling-class-unicode", spelling_class("U1F600") == "unicode")
    check("spelling-class-hex", spelling_class("0x1008ff13") == "hex")
    check("spelling-class-nosymbol", spelling_class("NoSymbol") == "nosymbol")
    check("spelling-class-digit-name", spelling_class("1") == "named")

    failed = [c for c in cases if not c[1]]
    for name, ok, detail in cases:
        print("%s %s%s" % ("PASS" if ok else "FAIL", name,
                           (" (" + detail + ")") if detail else ""))
    print("MADO_KEYMAP_PARSE_SELFTEST: %d/%d passed"
          % (len(cases) - len(failed), len(cases)))
    return 0 if not failed else 1


def main(argv):
    if len(argv) < 2:
        print("usage: parse.py {selftest|dump|census} FILE...", file=sys.stderr)
        return 2
    cmd = argv[1]
    if cmd == "selftest":
        return _selftest()
    if cmd == "dump":
        return _dump(argv[2:])
    if cmd == "census":
        return _census(argv[2:])
    print("unknown command %r" % cmd, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
