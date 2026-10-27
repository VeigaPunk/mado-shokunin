#!/usr/bin/env python3
"""gen.py -- nonce generator for C1 clause g: (RMLVO, keysym) cases.

The generator draws a case from a *frozen* snapshot of ``xkbcli list``
(models, layouts, variants, option groups) plus a keysym from
``xkbcommon-keysyms.h``.  Keysyms are weighted towards the keysyms that are
actually present in the case's compiled keymap: the caller parses the keymap
(``parse_keymap``) and passes the resulting ``(name, count)`` pool to
``gen_case``/``gen_keysym``.  Everything is drawn from a ``random.Random``
instance handed in by the caller, so a seed fixes the case list.

Determinism contract
--------------------
* No module-level RNG, no clock, no environment, no subprocess, no file write.
* All candidate collections are sorted before any draw, so the case list does
  not depend on dict/set iteration order.
* Weighted picks walk an explicit cumulative sum over ``rng.random()``; no
  version-dependent helper (``random.choices``/``shuffle``) is used.

Pins (libxkbcommon 1.13.2-1, xkeyboard-config 2.48-1)
-----------------------------------------------------
=========================  ==================================================
``/usr/lib/xkbcommon/xkbcli-how-to-type``
                           ``f6c0b122ad90c9e30086653517c51f4b2203b6c7c07bcbc89c71e55ab2927e54``
``/usr/lib/xkbcommon/xkbcli-compile-keymap``
                           ``43b924f68651500e022c74371515154f8c50a2e087defa6b834cc5d41fd77250``
``xkbcommon-keysyms.h``
                           ``13023369f65a17411606084e3e09557b4886aeb15f89affba4aaa86490a463f3``
``xkbcli-list.txt`` (snapshot, this seat dir)
                           ``2666867f599d0a0ca9c0047d011cc5f86012a66a4e141f59ca5b33a6bbe6c760``
=========================  ==================================================

The snapshot is stored next to this file as ``xkbcli-list.txt``; the keysym
header copy is stored as ``xkbcommon-keysyms.h``.  Both digests are verified on
load and a mismatch aborts (no silent drift between count-time runs).

Usage
-----
    python3 gen.py snapshot-check           # digests + parsed census
    python3 gen.py selftest                 # pure-stdlib self checks, no judge
    python3 gen.py cases --seed 4901 --n 400
    python3 gen.py cases --seed 4901 --n 400 --compile  # weight on real keymaps
    python3 gen.py case --seed 4901         # one case

``--compile`` runs the pinned ``xkbcli-compile-keymap`` (absolute path, clean
environment) and captures its stdout in memory to build the presence pool; it
writes no file.  Without ``--compile`` the keysym comes from the header pool
only and the case is marked ``"present_weighted": false``.

Naive baseline
--------------
``naive_stdout`` models a "first match only, no modifiers" reader of the
compiled keymap: it reports the first (keycode asc, layout asc, level asc)
occurrence of the keysym, always with an empty modifier mask, rc 0.  The
harness uses it to show how much of the corpus a naive instrument would pass.
"""

import argparse
import hashlib
import json
import os
import random
import re
import sys

SNAPSHOT_SHA256 = "2666867f599d0a0ca9c0047d011cc5f86012a66a4e141f59ca5b33a6bbe6c760"
HEADER_SHA256 = "13023369f65a17411606084e3e09557b4886aeb15f89affba4aaa86490a463f3"
JUDGE_PATH = "/usr/lib/xkbcommon/xkbcli-how-to-type"
JUDGE_SHA256 = "f6c0b122ad90c9e30086653517c51f4b2203b6c7c07bcbc89c71e55ab2927e54"
COMPILE_PATH = "/usr/lib/xkbcommon/xkbcli-compile-keymap"
COMPILE_SHA256 = "43b924f68651500e022c74371515154f8c50a2e087defa6b834cc5d41fd77250"

SEAT_DIR = os.path.dirname(os.path.abspath(__file__))
SNAPSHOT_PATH = os.path.join(SEAT_DIR, "xkbcli-list.txt")
HEADER_PATH = os.path.join(SEAT_DIR, "xkbcommon-keysyms.h")

# Census of the frozen snapshot / header, asserted by snapshot-check and selftest.
EXPECTED_MODELS = 184
EXPECTED_LAYOUT_RECORDS = 598
EXPECTED_DISTINCT_LAYOUTS = 99
EXPECTED_NONEMPTY_VARIANTS = 499
EXPECTED_OPTION_GROUPS = 22
EXPECTED_OPTIONS = 217
EXPECTED_HEADER_DEFINES = 2638

TABLE_HEADER = "KEYCODE  KEY NAME  LAYOUT   LAYOUT NAME          LEVEL#  MODIFIERS"
# Column widths measured on the pinned judge's stdout (see ExecGen.md).
# The judge pads each column to width-1 and then writes one separator
# space, so a layout name over 20 chars keeps the separator and pushes
# the following columns right (measured: "Ukrainian (Windows Enhanced) 1").
ROW_FMT = "{code:<8} {name:<9} {layout:<8} {layout_name:<20} {level:<7} {mods}"
# A layout name longer than the 20-wide column pushes the level and
# mask columns right by one space per extra character, so rows are
# parsed by shape, not by fixed offsets.
_ROW_RX = re.compile(r"^(\d+)\s+(\S+)\s+(\d+)\s+(.+?)\s+(\d+)\s+(\[.*\])$")

# Layouts the generator draws first (host-relevant + broad script coverage;
# 'custom' is excluded: it needs user-supplied symbols).
PREFERRED_LAYOUTS = {
    "us": 14, "br": 8, "de": 8, "fr": 6, "gb": 5, "es": 5, "it": 3, "pt": 3,
    "ru": 4, "pl": 3, "se": 2, "no": 2, "dk": 2, "fi": 2, "nl": 2, "cz": 2,
    "hu": 2, "tr": 2, "gr": 2, "il": 1, "ara": 1, "jp": 2, "kr": 1, "ca": 2,
    "ch": 2, "be": 2, "at": 1, "ie": 1, "lt": 1, "lv": 1, "ee": 1, "si": 1,
    "hr": 1, "sk": 1, "ro": 1, "bg": 1, "ua": 1, "by": 1, "th": 1, "vn": 1,
}
PREFERRED_MODELS = {"pc105": 42, "pc104": 16, "pc101": 10, "pc102": 6, "pc86": 3, "pc104alt": 3}

# Option groups whose options are plain symbol/type additions.  Excluded on
# purpose: 'custom' and 'solaris' (compat redefinitions), 'japan'/'korean'
# (layout-specific symbol sets), 'terminate' (server action), 'grp*' with a
# single layout (no-op that muddies the mask set), 'mod_led'/'grp_led'.
ALLOWED_OPTION_GROUPS = (
    "lv2", "lv3", "lv5", "altwin", "ctrl", "caps", "keypad", "kpdl",
    "Compose", "nbsp", "currencysign", "compat",
)

MODEL_TAIL_SHARE = 20      # weight of "any other model from the snapshot"
LAYOUT_TAIL_SHARE = 2      # weight of "any other layout from the snapshot"
MULTI_LAYOUT_P = 0.15
VARIANT_P = 0.45

# keysym draw mix (the remainder is the numeric-form draw)
P_PRESENT_WEIGHTED = 0.70
P_PRESENT_UNIFORM = 0.10
P_HEADER_UNIFORM = 0.05
# Weight bonus for a keysym occurrence that is not plain layout-1 level-1.
# A symbol that only sits at level 1 of the first layout is the class a
# first-match/no-modifier reader also gets; the counter wants the rest.
HARD_BONUS = 20


# --------------------------------------------------------------------------
# pins
# --------------------------------------------------------------------------

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_pinned(path, want, label):
    try:
        got = sha256_file(path)
    except OSError as exc:
        raise SystemExit("gen.py: cannot read %s %s: %s" % (label, path, exc))
    if got != want:
        raise SystemExit(
            "gen.py: %s digest mismatch\n  path %s\n  want %s\n  got  %s"
            % (label, path, want, got)
        )
    return path


# --------------------------------------------------------------------------
# frozen snapshot: xkbcli list
# --------------------------------------------------------------------------

class Snapshot(object):
    """Parsed frozen ``xkbcli list`` output."""

    __slots__ = ("models", "layout_records", "option_groups", "digest")

    def __init__(self, models, layout_records, option_groups, digest):
        self.models = models                  # [name]
        self.layout_records = layout_records  # [(layout, variant, description)]
        self.option_groups = option_groups    # [(group, [(option, allows_multiple)])]
        self.digest = digest

    def variants_of(self, layout):
        return [v for (lay, v, _d) in self.layout_records if lay == layout and v]

    def distinct_layouts(self):
        seen = []
        for (lay, _v, _d) in self.layout_records:
            if lay not in seen:
                seen.append(lay)
        return seen

    def options_of(self, group):
        for name, opts in self.option_groups:
            if name == group:
                return [o for (o, _m) in opts]
        return []


_SECTION_RX = re.compile(r"^([a-z_]+):$")


def load_snapshot(path=SNAPSHOT_PATH, verify=True):
    if verify:
        _read_pinned(path, SNAPSHOT_SHA256, "snapshot")
    with open(path, "r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    models = []
    layout_records = []
    option_groups = []   # [ [group, [[opt, allows_multiple]]] ]
    section = None
    in_options = False
    for line in lines:
        m = _SECTION_RX.match(line)
        if m:
            section = m.group(1)
            in_options = False
            continue
        if section == "models":
            m = re.match(r"^- name: (\S+)\s*$", line)
            if m:
                models.append(m.group(1))
        elif section == "layouts":
            m = re.match(r"^- layout: '([^']*)'$", line)
            if m:
                layout_records.append([m.group(1), "", ""])
                in_options = False
                continue
            m = re.match(r"^  variant: '([^']*)'$", line)
            if m and layout_records:
                layout_records[-1][1] = m.group(1)
                continue
            m = re.match(r"^  description: '(.*)'$", line)
            if m and layout_records:
                layout_records[-1][2] = m.group(1)
        elif section == "option_groups":
            m = re.match(r"^- name: '([^']*)'$", line)
            if m:
                option_groups.append([m.group(1), []])
                in_options = False
                continue
            if line.strip() == "options:":
                in_options = True
                continue
            m = re.match(r"^  - name: '([^']*)'$", line)
            if m and in_options and option_groups:
                option_groups[-1][1].append([m.group(1), False])
                continue
            m = re.match(r"^    allows_multiple: (true|false)$", line)
            if m and in_options and option_groups and option_groups[-1][1]:
                option_groups[-1][1][-1][1] = (m.group(1) == "true")
    snap = Snapshot(
        models,
        [(str(a), str(b), str(c)) for (a, b, c) in layout_records],
        [(g, [(o, m) for (o, m) in opts]) for (g, opts) in option_groups],
        SNAPSHOT_SHA256 if verify else sha256_file(path),
    )
    if verify:
        check_snapshot_census(snap)
    return snap


def check_snapshot_census(snap):
    problems = []
    if len(snap.models) != EXPECTED_MODELS:
        problems.append("models %d != %d" % (len(snap.models), EXPECTED_MODELS))
    if len(snap.layout_records) != EXPECTED_LAYOUT_RECORDS:
        problems.append("layout records %d != %d" % (len(snap.layout_records), EXPECTED_LAYOUT_RECORDS))
    if len(snap.distinct_layouts()) != EXPECTED_DISTINCT_LAYOUTS:
        problems.append("distinct layouts %d != %d" % (len(snap.distinct_layouts()), EXPECTED_DISTINCT_LAYOUTS))
    nonempty = sum(1 for (_l, v, _d) in snap.layout_records if v)
    if nonempty != EXPECTED_NONEMPTY_VARIANTS:
        problems.append("non-empty variants %d != %d" % (nonempty, EXPECTED_NONEMPTY_VARIANTS))
    if len(snap.option_groups) != EXPECTED_OPTION_GROUPS:
        problems.append("option groups %d != %d" % (len(snap.option_groups), EXPECTED_OPTION_GROUPS))
    total_opts = sum(len(o) for (_g, o) in snap.option_groups)
    if total_opts != EXPECTED_OPTIONS:
        problems.append("options %d != %d" % (total_opts, EXPECTED_OPTIONS))
    if problems:
        raise SystemExit("gen.py: snapshot census drift: " + "; ".join(problems))


# --------------------------------------------------------------------------
# keysym header
# --------------------------------------------------------------------------

_DEFINE_RX = re.compile(r"^#define XKB_KEY_(\S+)\s+0x([0-9a-fA-F]+)")
_UNICODE_KEY_RX = re.compile(r"^U([0-9A-Fa-f]{4,6})$")
_HEX_TOKEN_RX = re.compile(r"^0x([0-9A-Fa-f]+)$")


class Keysyms(object):
    """Names and values parsed from xkbcommon-keysyms.h (file order kept)."""

    __slots__ = ("names", "by_name", "by_value", "digest")

    def __init__(self, names, by_name, by_value, digest):
        self.names = names        # [name] in header order
        self.by_name = by_name    # name -> value
        self.by_value = by_value  # value -> [name] in header order
        self.digest = digest

    def first_name(self, value):
        """The name the judge prints for a value.

        libxkbcommon's get_name order: table name, then a synthesised Unicode
        name ``U%04X`` for a Unicode keysym (0x01000000|cp, cp >= 0x100), then
        the ``0x%08x`` placeholder for a value with no name at all.
        """
        names = self.by_value.get(value)
        if names:
            return names[0]
        if value & 0xFF000000 == 0x01000000:
            cp = value & 0x00FFFFFF
            if 0x100 <= cp <= 0x10FFFF:
                return "U%04X" % cp
        return "0x%08x" % value

    def value_of(self, token):
        """Keysym value of a compiled-keymap symbol token, or None.

        Compiled keymaps name symbols three ways: a header name (``slash``),
        a Unicode keysym (``U2032`` -> 0x1002032), and a raw value with no name
        (``0x0100002b``).  All three are legal how-to-type arguments.
        """
        value = self.by_name.get(token)
        if value is not None:
            return value
        m = _UNICODE_KEY_RX.match(token)
        if m:
            cp = int(m.group(1), 16)
            return cp if cp <= 0xFF else 0x01000000 | cp
        m = _HEX_TOKEN_RX.match(token)
        if m:
            return int(m.group(1), 16)
        return None


def load_keysyms(path=HEADER_PATH, verify=True):
    if verify:
        _read_pinned(path, HEADER_SHA256, "keysym header")
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    names = []
    by_name = {}
    by_value = {}
    for line in text.splitlines():
        m = _DEFINE_RX.match(line)
        if not m:
            continue
        name = m.group(1)
        value = int(m.group(2), 16)
        names.append(name)
        by_name[name] = value
        by_value.setdefault(value, []).append(name)
    if verify and len(names) != EXPECTED_HEADER_DEFINES:
        raise SystemExit(
            "gen.py: header defines %d != %d" % (len(names), EXPECTED_HEADER_DEFINES)
        )
    return Keysyms(names, by_name, by_value, HEADER_SHA256 if verify else sha256_file(path))


# --------------------------------------------------------------------------
# compiled keymap view
# --------------------------------------------------------------------------

_KEYCODE_RX = re.compile(r"^\s*<([A-Z0-9_+]+)>\s*=\s*(\d+)\s*;")
_KEY_SINGLE_RX = re.compile(r"^\s*key <([A-Z0-9_+]+)>\s*\{\s*\[\s*(.*?)\s*\]\s*\}\s*;")
_KEY_BLOCK_RX = re.compile(r"^\s*key <([A-Z0-9_+]+)>\s*\{\s*$")
_SYMBOLS_RX = re.compile(r"^\s*symbols\[(\d+)\]=\s*\[\s*(.*?)\s*\]\s*,?\s*$")
_GROUP_NAME_RX = re.compile(r'^\s*name\[(\d+)\]="(.*)"\s*;')
_BLOCK_RX = re.compile(r'^xkb_([a-z]+) "')


class KeymapView(object):
    """What the generator needs from a compiled keymap (format 1 or 2)."""

    __slots__ = ("keycodes", "group_names", "keys", "sha256")

    def __init__(self, keycodes, group_names, keys, sha):
        self.keycodes = keycodes    # key name -> keycode
        self.group_names = group_names  # group index (1-based) -> name
        self.keys = keys            # key name -> [[symbol, ...] per group]
        self.sha256 = sha

    def present(self):
        """[(keysym name, occurrence count)] sorted by name, NoSymbol dropped."""
        counts = {}
        for _key, groups in self.keys.items():
            for symbols in groups:
                for sym in symbols:
                    if sym and sym != "NoSymbol":
                        counts[sym] = counts.get(sym, 0) + 1
        return sorted(counts.items())

    def present_with_hard(self):
        """[(name, count, hard_count)]; hard = not layout 1 level 1.

        A symbol that only sits at plain level 1 of the first layout is the
        easy class: one row, empty mask.  Everything else (Shift/AltGr level,
        group > 1) needs a modifier mask or a second layout row, which is what
        separates a real reader from a first-match reader.
        """
        counts = {}
        hard = {}
        for _key, groups in self.keys.items():
            for gi, symbols in enumerate(groups, start=1):
                for li, sym in enumerate(symbols, start=1):
                    if not sym or sym == "NoSymbol":
                        continue
                    counts[sym] = counts.get(sym, 0) + 1
                    if gi > 1 or li > 1:
                        hard[sym] = hard.get(sym, 0) + 1
        return [(name, counts[name], hard.get(name, 0)) for name in sorted(counts)]

    def present_weighted(self, hard_bonus=HARD_BONUS):
        """[(name, weight)] for the keysym draw.

        ``weight = count + hard_bonus * hard_count`` -- still "keysyms present
        in the keymap", ordered by how many direct-access rows a reader has to
        get right.  ``hard_bonus=0`` gives the plain occurrence weighting.
        """
        return [(name, count + hard_bonus * hard)
                for (name, count, hard) in self.present_with_hard()]


def parse_keymap(text, sha=None):
    keycodes = {}
    group_names = {}
    keys = {}
    section = None
    block_key = None
    block_groups = None
    for line in text.splitlines():
        if block_key is not None:
            m = _SYMBOLS_RX.match(line)
            if m:
                idx = int(m.group(1))
                while len(block_groups) < idx:
                    block_groups.append([])
                block_groups[idx - 1] = [
                    s.strip() for s in m.group(2).split(",") if s.strip()
                ]
                continue
            if line.strip() in ("};", "}"):
                keys[block_key] = block_groups
                block_key = None
                block_groups = None
                continue
            continue
        m = _BLOCK_RX.match(line)
        if m:
            section = m.group(1)
            continue
        if section == "keycodes":
            m = _KEYCODE_RX.match(line)
            if m:
                keycodes[m.group(1)] = int(m.group(2))
            continue
        if section != "symbols":
            continue
        m = _GROUP_NAME_RX.match(line)
        if m:
            group_names[int(m.group(1))] = m.group(2)
            continue
        m = _KEY_SINGLE_RX.match(line)
        if m:
            keys[m.group(1)] = [[s.strip() for s in m.group(2).split(",") if s.strip()]]
            continue
        m = _KEY_BLOCK_RX.match(line)
        if m:
            block_key = m.group(1)
            block_groups = []
            continue
    if sha is None:
        sha = hashlib.sha256(text.encode("utf-8", "surrogateescape")).hexdigest()
    return KeymapView(keycodes, group_names, keys, sha)


# --------------------------------------------------------------------------
# draws
# --------------------------------------------------------------------------

def weighted_pick(rng, items, weights):
    """Explicit cumulative weighted pick; deterministic for a given RNG stream."""
    if not items:
        raise ValueError("weighted_pick: empty candidate list")
    total = 0
    for w in weights:
        if w < 0:
            raise ValueError("weighted_pick: negative weight")
        total += w
    if total <= 0:
        return items[rng.randrange(len(items))]
    r = rng.random() * total
    acc = 0
    for item, w in zip(items, weights):
        acc += w
        if r < acc:
            return item
    return items[-1]


def _preferred_pool(mapping, available):
    names = sorted(n for n in mapping if n in available)
    return names, [mapping[n] for n in names]


def gen_rmlvo(rng, snap):
    """Draw (rules, model, layout, variant, options) from the frozen snapshot."""
    models = snap.models
    pref_models, pref_model_w = _preferred_pool(PREFERRED_MODELS, set(models))
    tail_models = sorted(m for m in models if m not in PREFERRED_MODELS)
    names = pref_models + tail_models
    weights = pref_model_w + [MODEL_TAIL_SHARE / len(tail_models)] * len(tail_models) if tail_models \
        else pref_model_w
    model = weighted_pick(rng, names, weights)

    layouts = [lay for lay in snap.distinct_layouts() if lay != "custom"]
    pref_layouts, pref_layout_w = _preferred_pool(PREFERRED_LAYOUTS, set(layouts))
    tail_layouts = sorted(lay for lay in layouts if lay not in PREFERRED_LAYOUTS)
    lnames = pref_layouts + tail_layouts
    lweights = pref_layout_w + [LAYOUT_TAIL_SHARE / len(tail_layouts)] * len(tail_layouts) \
        if tail_layouts else pref_layout_w
    first = weighted_pick(rng, lnames, lweights)

    if rng.random() < MULTI_LAYOUT_P:
        second = first
        for _ in range(8):
            second = weighted_pick(rng, lnames, lweights)
            if second != first:
                break
        if second == first:
            second = "us" if first != "us" else "de"
        return {
            "rules": "evdev",
            "model": model,
            "layout": first + "," + second,
            "variant": "",
            "options": [],
        }

    variant = ""
    variants = sorted(snap.variants_of(first))
    if variants and rng.random() < VARIANT_P:
        variant = variants[rng.randrange(len(variants))]

    groups = sorted(g for g in ALLOWED_OPTION_GROUPS if snap.options_of(g))
    k_roll = rng.random()
    k = 0 if k_roll < 0.45 else (1 if k_roll < 0.80 else 2)
    chosen = []
    pool = list(groups)
    for _ in range(min(k, len(pool))):
        gi = rng.randrange(len(pool))
        group = pool.pop(gi)
        opts = sorted(snap.options_of(group))
        chosen.append(opts[rng.randrange(len(opts))])
    return {
        "rules": "evdev",
        "model": model,
        "layout": first,
        "variant": variant,
        "options": chosen,
    }


def gen_keysym(rng, present=None, keysyms=None):
    """Draw a keysym ARG.

    ``present`` is ``[(name, count)]`` from the case's compiled keymap.  With it,
    the draw is weighted towards keysyms present in that keymap (weight =
    number of key/level occurrences).  Without it only the header pool is used.
    """
    if keysyms is None:
        keysyms = load_keysyms()
    present = list(present or [])
    pnames = [n for (n, _c) in present]
    pweights = [c for (_n, c) in present]
    roll = rng.random()
    if pnames and roll < P_PRESENT_WEIGHTED:
        name = weighted_pick(rng, pnames, pweights)
        return _name_case(name, keysyms, "present-weighted")
    if pnames and roll < P_PRESENT_WEIGHTED + P_PRESENT_UNIFORM:
        name = pnames[rng.randrange(len(pnames))]
        return _name_case(name, keysyms, "present-uniform")
    if roll < P_PRESENT_WEIGHTED + P_PRESENT_UNIFORM + P_HEADER_UNIFORM:
        name = keysyms.names[rng.randrange(len(keysyms.names))]
        return _name_case(name, keysyms, "header-uniform")
    if pnames:
        name = weighted_pick(rng, pnames, pweights)
    else:
        name = keysyms.names[rng.randrange(len(keysyms.names))]
    value = keysyms.value_of(name)
    if value is None:
        raise ValueError("unresolvable keysym token %r" % name)
    if value <= 9 or rng.random() < 0.5:
        arg = "0x%x" % value
    else:
        arg = "%d" % value
    return {
        "arg": arg,
        "name": name,
        "value": value,
        "form": "numeric",
        "mode": "numeric-" + ("present" if pnames else "header"),
        "in_keymap": name in set(pnames),
        "header_name": name in keysyms.by_name,
    }


def _name_case(name, keysyms, mode):
    value = keysyms.value_of(name)
    if value is None:
        raise ValueError("unresolvable keysym token %r" % name)
    return {
        "arg": name,
        "name": name,
        "value": value,
        "form": "name",
        "mode": mode,
        "in_keymap": mode.startswith("present"),
        "header_name": name in keysyms.by_name,
    }


def gen_case(rng, present=None, snap=None, keysyms=None, index=None):
    """Draw one (RMLVO, keysym) case.

    ``gen_case(rng)`` with no ``present`` pool is a pure header draw.  A caller
    that compiles the case's keymap first draws the RMLVO with ``gen_rmlvo``,
    parses the compiled keymap, and then calls ``gen_case_with(rng, rmlvo,
    present=...)`` so the keysym is weighted to keysyms present in *that* keymap.
    """
    return gen_case_with(rng, None, present=present, snap=snap,
                         keysyms=keysyms, index=index)


def gen_case_with(rng, rmlvo, present=None, snap=None, keysyms=None, index=None):
    if snap is None:
        snap = load_snapshot()
    if keysyms is None:
        keysyms = load_keysyms()
    if rmlvo is None:
        rmlvo = gen_rmlvo(rng, snap)
    ks = gen_keysym(rng, present=present, keysyms=keysyms)
    case = {
        "index": index,
        "rules": rmlvo["rules"],
        "model": rmlvo["model"],
        "layout": rmlvo["layout"],
        "variant": rmlvo["variant"],
        "options": list(rmlvo["options"]),
        "keysym_arg": ks["arg"],
        "keysym_name": ks["name"],
        "keysym_value": ks["value"],
        "keysym_form": ks["form"],
        "keysym_draw": ks["mode"],
        "present_weighted": bool(present),
        "multi_layout": "," in rmlvo["layout"],
    }
    return case


def compile_argv(case):
    argv = [
        COMPILE_PATH,
        "--rules", case["rules"],
        "--model", case["model"],
        "--layout", case["layout"],
    ]
    if case["variant"]:
        argv += ["--variant", case["variant"]]
    if case["options"]:
        argv += ["--options", ",".join(case["options"])]
    return argv


def how_to_type_argv(case, keymap_path):
    return [
        JUDGE_PATH,
        "--keymap=" + keymap_path,
        "--disable-compose",
        "--keysym", case["keysym_arg"],
    ]


# --------------------------------------------------------------------------
# naive baseline: first match only, no modifiers
# --------------------------------------------------------------------------

def parse_judge_rows(stdout):
    """Rows of the judge's ``=== Direct access ===`` table as dicts."""
    rows = []
    state = None
    for line in stdout.splitlines():
        if line == "=== Direct access ===":
            state = "pre"
            continue
        if state is None or not line.strip():
            continue
        if state == "pre":
            state = "rows"          # the column header line
            continue
        m = _ROW_RX.match(line)
        if not m:
            raise ValueError("gen.py: unparsed judge row %r" % line)
        rows.append({
            "keycode": int(m.group(1)),
            "key_name": m.group(2),
            "layout": int(m.group(3)),
            "layout_name": m.group(4),
            "level": int(m.group(5)),
            "modifiers": m.group(6),
        })
    return rows


def format_row(keycode, key_name, layout, layout_name, level, modifiers):
    mods = "[ %s ]" % modifiers if modifiers else "[ ]"
    return ROW_FMT.format(
        code=keycode, name=key_name, layout=layout,
        layout_name=layout_name, level=level, mods=mods,
    )


def naive_stdout(view, keysyms, keysym_value):
    """What a first-match, no-modifier reader prints (stdout only, rc 0)."""
    name = keysyms.first_name(keysym_value) or "NoSymbol"
    lines = [
        "keysym: %s (0x%04x)" % (name, keysym_value),
        "",
        "=== Direct access ===",
        "",
        TABLE_HEADER,
    ]
    for key_name in sorted(view.keys, key=lambda k: (view.keycodes.get(k, 1 << 30), k)):
        groups = view.keys[key_name]
        for gi, symbols in enumerate(groups, start=1):
            for li, sym in enumerate(symbols, start=1):
                if sym and keysyms.value_of(sym) == keysym_value:
                    lines.append(format_row(
                        view.keycodes.get(key_name, 0), key_name, gi,
                        view.group_names.get(gi, ""), li, "",
                    ))
                    return "\n".join(lines) + "\n"
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------

def selftest():
    checks = []

    def ok(label, cond):
        checks.append((label, bool(cond)))

    snap = load_snapshot()
    keysyms = load_keysyms()
    ok("snapshot digest", snap.digest == SNAPSHOT_SHA256)
    ok("header digest", keysyms.digest == HEADER_SHA256)
    ok("models", len(snap.models) == EXPECTED_MODELS)
    ok("layout records", len(snap.layout_records) == EXPECTED_LAYOUT_RECORDS)
    ok("distinct layouts", len(snap.distinct_layouts()) == EXPECTED_DISTINCT_LAYOUTS)
    ok("header defines", len(keysyms.names) == EXPECTED_HEADER_DEFINES)
    ok("header names unique", len(set(keysyms.names)) == len(keysyms.names))
    ok("aliases exist", any(len(v) > 1 for v in keysyms.by_value.values()))
    ok("slash value", keysyms.by_name.get("slash") == 0x2F)
    ok("Return value", keysyms.by_name.get("Return") == 0xFF0D)

    # determinism: same seed, fresh RNG objects, identical streams
    def stream(seed, n):
        rng = random.Random(seed)
        return [json.dumps(gen_case(rng, index=i, snap=snap, keysyms=keysyms),
                           sort_keys=True) for i in range(n)]

    a = stream(4901, 200)
    b = stream(4901, 200)
    c = stream(4902, 200)
    ok("determinism (same seed)", a == b)
    ok("seed sensitivity", a != c)
    ok("distinct cases", len(set(a)) == len(a))

    # shape and policy of 4000 RMLVO draws
    rng = random.Random(7)
    rmlvos = [gen_rmlvo(rng, snap) for _ in range(4000)]
    ok("rules always evdev", all(r["rules"] == "evdev" for r in rmlvos))
    ok("models from snapshot", all(r["model"] in set(snap.models) for r in rmlvos))
    layout_ok = True
    variant_ok = True
    options_ok = True
    allowed = set(ALLOWED_OPTION_GROUPS)
    opt_group = {}
    for gname, opts in snap.option_groups:
        for oname, _m in opts:
            opt_group[oname] = gname
    for r in rmlvos:
        parts = r["layout"].split(",")
        if any(p not in set(snap.distinct_layouts()) for p in parts):
            layout_ok = False
        if r["variant"]:
            if len(parts) != 1 or r["variant"] not in snap.variants_of(parts[0]):
                variant_ok = False
        groups_used = []
        for opt in r["options"]:
            grp = opt_group.get(opt)
            if grp not in allowed or opt not in snap.options_of(grp):
                options_ok = False
            groups_used.append(grp)
        if len(groups_used) != len(set(groups_used)):
            options_ok = False
    ok("layouts from snapshot", layout_ok)
    ok("variants belong to their layout", variant_ok)
    ok("options from allowed groups, one per group", options_ok)
    ok("multi-layout draw happens", any("," in r["layout"] for r in rmlvos))
    ok("variants drawn", any(r["variant"] for r in rmlvos))

    # keysym draw honours a presence pool
    present = [("slash", 9), ("Return", 1), ("dead_acute", 3)]
    rng = random.Random(11)
    draws = [gen_keysym(rng, present=present, keysyms=keysyms) for _ in range(2000)]
    present_names = {n for (n, _c) in present}
    weighted = [d for d in draws if d["mode"] == "present-weighted"]
    ok("present-weighted draws exist", len(weighted) > 900)
    ok("present-weighted names in pool", all(d["name"] in present_names for d in weighted))
    slash_share = sum(1 for d in weighted if d["name"] == "slash") / float(len(weighted))
    ok("weights follow counts (slash 9/13)", 0.62 < slash_share < 0.76)
    ok("all args non-empty", all(d["arg"] for d in draws))
    ok("numeric form draws exist", any(d["form"] == "numeric" for d in draws))
    ok("no numeric 0..9 as decimal", all(
        not (d["form"] == "numeric" and d["arg"].isdigit() and int(d["arg"]) <= 9)
        for d in draws))

    # keymap parsing + naive baseline on a synthetic keymap
    fixture = "\n".join([
        "xkb_keymap {",
        'xkb_keycodes "t" {',
        "\t<ESC> = 9;",
        "\t<AD01> = 24;",
        "\t<AD02> = 25;",
        "\t<AB11> = 97;",
        "};",
        'xkb_symbols "t" {',
        '\tname[1]="Test Layout";',
        "\tkey <ESC>  {\t[ Escape ] };",
        "\tkey <AD01> {\t[ q, Q ] };",
        "\tkey <AD02> {\t[ w, w, slash, slash ] };",
        "\tkey <AB11> {\t[ slash, question ] };",
        "};",
        "};",
    ])
    view = parse_keymap(fixture)
    ok("parse keycodes", view.keycodes.get("AD01") == 24 and view.keycodes.get("AB11") == 97)
    ok("parse group name", view.group_names.get(1) == "Test Layout")
    ok("parse key symbols", view.keys["AD02"][0] == ["w", "w", "slash", "slash"])
    ok("present pool", view.present() == [("Escape", 1), ("Q", 1), ("q", 1),
                                          ("question", 1), ("slash", 3), ("w", 2)])
    ok("present hard pool", view.present_with_hard() == [
        ("Escape", 1, 0), ("Q", 1, 1), ("q", 1, 0), ("question", 1, 1),
        ("slash", 3, 2), ("w", 2, 1)])
    ok("present_weighted(0) == present", view.present_weighted(0) == view.present())
    ok("present_weighted bonus", view.present_weighted(6) == [
        ("Escape", 1), ("Q", 7), ("q", 1), ("question", 7), ("slash", 15), ("w", 8)])
    naive = naive_stdout(view, keysyms, 0x2F)
    ok("naive first match is AD02 level 3", naive.splitlines()[-1].startswith("25       AD02      1        Test Layout          3"))
    ok("naive single row", len(parse_judge_rows(naive)) == 1)
    ok("naive mask empty", parse_judge_rows(naive)[0]["modifiers"] == "[]" or
       parse_judge_rows(naive)[0]["modifiers"] == "[ ]")

    # judge row parser round-trips the pinned judge's own sample (measured
    # from --keysym slash on the br keymap, keymap sha efd487a3...)
    sample = "\n".join([
        "keysym: slash (0x002f)", "",
        "=== Direct access ===", "",
        TABLE_HEADER,
        "24       AD01      1        Portuguese (Brazil)  3       [ Mod5 LevelThree ]",
        "97       AB11      1        Portuguese (Brazil)  1       [ ]",
    ])
    rows = parse_judge_rows(sample)
    ok("judge sample rows", len(rows) == 2)
    ok("judge sample row1", rows[0] == {
        "keycode": 24, "key_name": "AD01", "layout": 1,
        "layout_name": "Portuguese (Brazil)", "level": 3,
        "modifiers": "[ Mod5 LevelThree ]",
    })
    ok("judge sample row2", rows[1]["keycode"] == 97 and rows[1]["modifiers"] == "[ ]")
    ok("format_row matches judge bytes",
       format_row(24, "AD01", 1, "Portuguese (Brazil)", 3, "Mod5 LevelThree")
       == sample.splitlines()[5])

    # symbol tokens as the compiler emits them: header name, U-name, raw value
    ok("value_of header name", keysyms.value_of("slash") == 0x2F)
    ok("value_of U-name", keysyms.value_of("U2032") == 0x1002032)
    ok("value_of U-name below 0x100", keysyms.value_of("U00e9") == 0xE9)
    ok("value_of raw hex token", keysyms.value_of("0x0100002b") == 0x100002B)
    ok("value_of unknown", keysyms.value_of("nosuchsym") is None)
    ok("first_name placeholder", keysyms.first_name(0x2032) == "0x00002032")
    ok("first_name U-name synthesis", keysyms.first_name(0x1002032) == "U2032")
    ok("first_name U-name below 0x100 is a placeholder",
       keysyms.first_name(0x100002B) == "0x0100002b")
    ok("first_name above Unicode is a placeholder",
       keysyms.first_name(0x110000) == "0x00110000")

    # long layout names shift the level/mask columns (measured on the judge's
    # own rows for layout 'us' variant 'workman-intl' and 'cz' 'dvorak-ucw')
    wide = "\n".join([
        "=== Direct access ===", "",
        TABLE_HEADER,
        "38       AC01      1        English (Workman, intl., with dead keys) 2       [ Shift ]",
        "69       FK03      1        English (Colemak-DH Wide) 1       [ Mod1 Alt Meta ]",
        "109      LNFD      1        Czech (US, Dvorak, UCW support) 1       [ ]",
    ])
    wrows = parse_judge_rows(wide)
    ok("wide row count", len(wrows) == 3)
    ok("wide row name", wrows[0]["layout_name"] == "English (Workman, intl., with dead keys)")
    ok("wide row level", wrows[0]["level"] == 2 and wrows[0]["modifiers"] == "[ Shift ]")
    ok("wide row mask order", wrows[1]["modifiers"] == "[ Mod1 Alt Meta ]")
    ok("wide row empty mask", wrows[2]["modifiers"] == "[ ]" and wrows[2]["keycode"] == 109)
    ok("format_row keeps the separator after a wide layout name",
       format_row(623, "I623", 1, "Ukrainian (Windows Enhanced)", 1, "")
       == "623      I623      1        Ukrainian (Windows Enhanced) 1       [ ]")
    ok("format_row short name width",
       len(format_row(24, "AD01", 1, "Portuguese (Brazil)", 3, "Mod5 LevelThree")) == 76)

    failed = [label for (label, cond) in checks if not cond]
    for (label, cond) in checks:
        sys.stdout.write("%s %s\n" % ("ok  " if cond else "FAIL", label))
    sys.stdout.write("GEN_SELFTEST: %d/%d passed\n" % (len(checks) - len(failed), len(checks)))
    return 0 if not failed else 1


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def snapshot_check(snapshot_path=SNAPSHOT_PATH, header_path=HEADER_PATH):
    snap = load_snapshot(snapshot_path)
    keysyms = load_keysyms(header_path)
    print("snapshot %s sha256 %s" % (snapshot_path, snap.digest))
    print("models %d" % len(snap.models))
    print("layout_records %d" % len(snap.layout_records))
    print("distinct_layouts %d" % len(snap.distinct_layouts()))
    print("nonempty_variants %d" % sum(1 for (_l, v, _d) in snap.layout_records if v))
    print("option_groups %d" % len(snap.option_groups))
    print("options %d" % sum(len(o) for (_g, o) in snap.option_groups))
    print("allowed_option_groups %d" % len([g for g in ALLOWED_OPTION_GROUPS if snap.options_of(g)]))
    print("keysym_header %s sha256 %s" % (header_path, keysyms.digest))
    print("keysym_defines %d" % len(keysyms.names))
    print("keysym_values %d" % len(keysyms.by_value))
    print("keysym_aliases %d" % (len(keysyms.names) - len(keysyms.by_value)))
    return 0


def _compile_keymap(rmlvo):
    """Compile the case's keymap with the pinned tool (in memory, clean env)."""
    import subprocess
    env = {"PATH": "/usr/bin"}
    proc = subprocess.run(
        compile_argv(rmlvo), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, env=env, timeout=120,
    )
    if proc.returncode != 0:
        raise SystemExit(
            "gen.py: compile-keymap rc=%d for %r\n%s"
            % (proc.returncode, rmlvo, proc.stderr.decode("utf-8", "replace")[:400])
        )
    return proc.stdout.decode("utf-8", "replace")


def iter_cases(seed, n, compile_fn=None, snap=None, keysyms=None,
               weighting="difficulty", hard_bonus=HARD_BONUS):
    """Yield ``(case, keymap_text_or_None)`` for a seed.

    ``compile_fn`` maps an RMLVO dict to compiled keymap text; when given, the
    keysym draw is weighted on the keysyms present in that keymap
    (``weighting="difficulty"``: ``count + hard_bonus*hard``, default;
    ``weighting="plain"``: occurrence count only).  The draw order is fixed:
    RMLVO, (compile), keysym -- so the same seed, compile function and
    weighting reproduce the same case list at count time.
    """
    rng = random.Random(seed)
    if snap is None:
        snap = load_snapshot()
    if keysyms is None:
        keysyms = load_keysyms()
    if weighting not in ("difficulty", "plain"):
        raise ValueError("weighting must be 'difficulty' or 'plain'")
    for i in range(n):
        rmlvo = gen_rmlvo(rng, snap)
        text = None
        present = None
        if compile_fn is not None:
            text = compile_fn(rmlvo)
            view = parse_keymap(text)
            present = view.present_weighted(
                hard_bonus if weighting == "difficulty" else 0)
        case = gen_case_with(rng, rmlvo, present=present, snap=snap,
                             keysyms=keysyms, index=i)
        if present is not None:
            case["present_pool_size"] = len(present)
        case["weighting"] = weighting if present is not None else None
        yield case, text


def emit_cases(seed, n, do_compile=False, snap=None, keysyms=None,
               weighting="difficulty"):
    for case, _text in iter_cases(seed, n,
                                  compile_fn=_compile_keymap if do_compile else None,
                                  snap=snap, keysyms=keysyms, weighting=weighting):
        sys.stdout.write(json.dumps(case, sort_keys=True) + "\n")


def main(argv):
    ap = argparse.ArgumentParser(description="nonce generator for C1 clause g")
    ap.add_argument("--snapshot", default=SNAPSHOT_PATH, help=argparse.SUPPRESS)
    ap.add_argument("--keysyms", default=HEADER_PATH, help=argparse.SUPPRESS)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("snapshot-check")
    sub.add_parser("selftest")
    p_cases = sub.add_parser("cases")
    p_cases.add_argument("--seed", type=int, required=True)
    p_cases.add_argument("--n", type=int, default=400)
    p_cases.add_argument("--compile", action="store_true",
                         help="weight keysyms on the compiled keymap (runs the pinned compile-keymap)")
    p_cases.add_argument("--weighting", choices=("difficulty", "plain"),
                         default="difficulty")
    p_case = sub.add_parser("case")
    p_case.add_argument("--seed", type=int, default=1)
    p_case.add_argument("--compile", action="store_true")
    p_case.add_argument("--weighting", choices=("difficulty", "plain"),
                        default="difficulty")
    args = ap.parse_args(argv)

    snap = load_snapshot(args.snapshot)
    keysyms = load_keysyms(args.keysyms)
    if args.cmd == "snapshot-check":
        return snapshot_check(args.snapshot, args.keysyms)
    if args.cmd == "selftest":
        return selftest()
    if args.cmd == "cases":
        emit_cases(args.seed, args.n, args.compile, snap=snap, keysyms=keysyms,
                   weighting=args.weighting)
        return 0
    if args.cmd == "case":
        for case, _text in iter_cases(args.seed, 1,
                                      compile_fn=_compile_keymap if args.compile else None,
                                      snap=snap, keysyms=keysyms,
                                      weighting=args.weighting):
            sys.stdout.write(json.dumps(case, sort_keys=True) + "\n")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
