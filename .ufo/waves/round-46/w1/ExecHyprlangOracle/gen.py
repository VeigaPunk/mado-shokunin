#!/usr/bin/env python3
"""Random config generator for the round-46 C1 contract differential test (ExecHyprlangOracle).

Two grammars:
  clean - the forms the reference (`l1-draft/mado-devices.py`) models without counting `unsupported`:
          flat `input:kb_*`, `input { ... }` (a nested touchpad, a deeper wrapper), `device { name = X ... }`,
          `device[X] { ... }`, `device[X]:k = v`, one `device:name = X` selector per case, merges and duplicate
          names, `[[EMPTY]]`, empty RHS, unknown keys, nesting, `#`/`##` comments, backslash continuations, CRLF,
          blank/noise lines, an unclosed category at EOF.
  raw   - clean pieces plus exactly one piece from a tag list of forms the reference counts `unsupported`
          (directives, `$`, `{{ }}`, interior backslash, a selector-less `device:k`, a block whose first key is
          not `name`, a rename, inf/nan/hex/subnormal scroll factors, and a flat `device:k` after a bracket line or
          after a file that ended with an unclosed device block). One tag per case makes the attribution exact.

Devices are just names: the oracle is queried by name, the same way `expected_names` is.
Pieces are kept whole when the case is split into 1-3 files, so structure stays balanced.
"""
import random

DEV_KEYS = ("kb_layout", "kb_variant", "kb_options", "kb_model", "kb_rules", "kb_file", "scroll_factor")
IRRELEVANT = ("sensitivity", "natural_scroll", "tap-to-click", "accel_profile", "rotation", "enabled", "unknown_key")

VALUES = {
    "kb_layout": ["us", "de", "br", "fr", "us,de", "dvorak", "", "[[EMPTY]]", " gb", "ca", "de,us,fr", "x y"],
    "kb_variant": ["intl", "azerty", "", "[[EMPTY]]", "nodeadkeys", "intl,azerty"],
    "kb_options": ["compose:caps", "grp:alts_toggle", "compose:caps,grp:alts_toggle", "", "[[EMPTY]]", "a##b", "x # y",
                   "caps:escape#tail"],
    "kb_model": ["pc105", "pc104", "", "[[EMPTY]]", "microsoft"],
    "kb_rules": ["evdev", "base", "", "[[EMPTY]]", "xorg"],
    "kb_file": ["~/x.xkb", "/tmp/none.xkb", "", "[[EMPTY]]", "relative.xkb"],
}
SF = ["0.5", "2", "-3", "250", "0", "100", "1e2", "0.7x", "  4 ", ".5", "5.", "1e-1", "+2.5", "0.005", "100.005",
      "99.999", "-0", "00012", "2.675", "1.005", "0.495", "-0.0", "1e0", "1E+2", "3.0e-2", "100.0049999",
      "1.2345678901234567890", "50.555", "0.015", "12x34", "0.1e1"]
FX_SPECIAL = ["inf", "-inf", "nan", "0x10", "0X1p3", "1e-40", "1e-45", "5e-39", "1.1754943508222875e-38",
              "1.1754943e-38", "1e999", "-1e999", "1e-999", "  inf  ", "+nan"]
NAMES = ["kbd", "kbd2", "Kbd", "razer-deathadder", "Razer DeathAdder", "hl-virtual-keyboard-fcitx5", "mouse",
         "touchpad-1", "x,y", "", "k b", "k.b", "hl-virtual-keyboard", "kbd-1"]
COMMENTS = ["# note", "#", "# a##b", "# x # y", "  # tail"]
NOISE = ["", "   ", "}\t", "garbage", "=", "device", "\t"]
RAWTAGS = ("directive", "variable", "expression", "backslash", "flat-no-selector", "block-first-not-name", "rename",
           "float-special", "bracket-then-flat", "crossfile-unclosed", "selector-then-block",
           "crlf-continuation")


def name_pool(rng, k):
    return rng.sample(NAMES, k)


def dev_pairs(rng, n):
    out = []
    for _ in range(n):
        if rng.random() < 0.25:
            key = rng.choice(IRRELEVANT)
            val = rng.choice(["1", "0", "2", "adaptive", "[[EMPTY]]", ""])
        else:
            key = rng.choice(DEV_KEYS)
            val = rng.choice(SF if key == "scroll_factor" else VALUES[key])
        out.append((key, val))
    return out


def stmt_input_block(rng, deep=False):
    lines = ["input {"]
    for _ in range(rng.randrange(0, 4)):
        k = rng.choice(["kb_layout", "kb_variant", "kb_options", "kb_model", "kb_rules", "kb_file"])
        lines.append("  %s = %s" % (k, rng.choice(VALUES[k])))
    if rng.random() < 0.4:
        lines += ["  touchpad {", "    scroll_factor = %s" % rng.choice(["0.4", "1", "2", "-1"]), "  }"]
    lines.append("}")
    if deep:
        return ["general {"] + ["  " + l for l in lines] + ["}"]
    return lines


def stmt_device_block(rng, name):
    lines = ["device {", "  name = %s" % name]
    for k, v in dev_pairs(rng, rng.randrange(0, 5)):
        lines.append("  %s = %s" % (k, v))
    if rng.random() < 0.15:
        lines += ["  nested {", "    kb_layout = de", "  }"]
    lines.append("}")
    return lines


def stmt_bracket_block(rng, name):
    lines = ["device[%s] {" % name]
    for k, v in dev_pairs(rng, rng.randrange(0, 4)):
        lines.append("  %s = %s" % (k, v))
    lines.append("}")
    return lines


def stmt_bracket_flat(rng, name):
    return ["device[%s]:%s = %s" % (name, k, v) for k, v in dev_pairs(rng, rng.randrange(1, 4))]


def stmt_selector(rng, name):
    out = ["device:name = %s" % name]
    for k, v in dev_pairs(rng, rng.randrange(0, 3)):
        out.append("device:%s = %s" % (k, v))
    return out


def stmt_flat_global(rng):
    k = rng.choice(["kb_layout", "kb_variant", "kb_options", "kb_model", "kb_rules", "kb_file"])
    if rng.random() < 0.15:
        return ["input:%s[%s] = %s" % (k, rng.choice(["g1", "x", ""]), rng.choice(VALUES[k]))]
    return ["input:%s = %s" % (k, rng.choice(VALUES[k]))]


def clean_piece(rng, names, allow_selector=True):
    r = rng.random()
    if r < 0.20:
        return stmt_flat_global(rng)
    if r < 0.38:
        return stmt_input_block(rng, deep=rng.random() < 0.2)
    if r < 0.62:
        return stmt_device_block(rng, rng.choice(names))
    if r < 0.74:
        return stmt_bracket_block(rng, rng.choice(names))
    if r < 0.88:
        return stmt_bracket_flat(rng, rng.choice(names))
    return stmt_device_block(rng, rng.choice(names))


def raw_piece(rng, names, tag):
    n = rng.choice(names) or "k"
    if tag == "directive":
        return ["# hyprlang if SOMEVAR"] + stmt_flat_global(rng) + ["# hyprlang endif"]
    if tag == "variable":
        return ["$lay = de", "input:kb_layout = $lay"]
    if tag == "expression":
        return ["input:kb_layout = {{ 1 + 2 }}"]
    if tag == "backslash":
        return ["input:kb_options = a\\{b"]
    if tag == "flat-no-selector":
        return ["device:kb_layout = de", "device:kb_file = /x"]
    if tag == "block-first-not-name":
        return ["device {", "  kb_layout = de", "  name = %s" % n, "}"]
    if tag == "rename":
        return ["device {", "  name = a", "  name = %s" % n, "  kb_layout = de", "}"]
    if tag == "float-special":
        return ["device[%s]:scroll_factor = %s" % (n, rng.choice(FX_SPECIAL))]
    if tag == "bracket-then-flat":
        return ["device[%s]:kb_layout = fr" % n, "device:kb_file = /x"]
    if tag == "crlf-continuation":
        return ["input:kb_model = pc1\\", "05"]
    if tag == "selector-then-block":
        return ["device:name = %s" % n, "device {", "  name = %s" % (rng.choice(names) or "k"), "  kb_layout = de", "}"]
    return ["device {", "  name = %s" % n, "  kb_layout = de"]  # crossfile-unclosed


def decorate(rng, lines, crlf=False):
    out = []
    for ln in lines:
        if ln and rng.random() < 0.30:
            ln = ln + " " + rng.choice(COMMENTS)
        if "=" in ln and len(ln) > 2 and not crlf and rng.random() < 0.12 and not ln.endswith("\\"):
            i = rng.randrange(1, len(ln))
            out.append(ln[:i] + "\\")
            out.append(ln[i:])
            continue
        out.append(ln)
    return out


def split_pieces(rng, pieces, nfiles):
    if nfiles <= 1 or len(pieces) < nfiles:
        return [pieces]
    cuts = sorted(rng.sample(range(1, len(pieces)), nfiles - 1))
    out, prev = [], 0
    for c in cuts:
        out.append(pieces[prev:c])
        prev = c
    out.append(pieces[prev:])
    return out


def build_case(rng, cid, raw):
    names = name_pool(rng, rng.randrange(2, 7))
    tag = rng.choice(RAWTAGS) if raw else None
    pieces = []
    for _ in range(rng.randrange(1, 7)):
        if rng.random() < 0.10:
            pieces.append([rng.choice(NOISE)])
        pieces.append(clean_piece(rng, names))
    special = rng.random()
    if not raw and special < 0.10:
        pieces.append(["device {", "  name = %s" % rng.choice(names), "  kb_layout = de"])
    elif not raw and special < 0.22:
        # a top-level `device:name = X` selector, last, so no later block renames it
        pieces.append(stmt_selector(rng, rng.choice(names)))
    nfiles = 1 if (raw and tag == "crossfile-unclosed") else rng.choices([1, 2, 3], weights=[6, 3, 1])[0]
    groups = split_pieces(rng, pieces, nfiles)
    if raw:
        if tag == "crossfile-unclosed":
            # file 0 keeps an unclosed device block, file 1 opens with a selector-less `device:k`
            groups = [groups[0] + [["device {", "  name = %s" % (rng.choice(names) or "k"), "  kb_layout = de"]],
                      [["device:kb_file = /x"]]]
        else:
            groups = groups + [[raw_piece(rng, names, tag)]]
    crlf = rng.random() < 0.2 or tag == "crlf-continuation"
    eol = "\r\n" if crlf else "\n"
    files = []
    for g in groups:
        lines = []
        for p in g:
            lines += p
        lines = decorate(rng, lines, crlf)
        files.append(eol.join(lines) + (eol if lines else ""))
    query = list(dict.fromkeys(names + [n for n in NAMES if n][:0] + rng.sample([n for n in NAMES if n], 2)))
    return {"id": cid, "files": files, "names": query, "tag": tag}


def generate(seed=46, n_clean=3200, n_raw=400):
    rng = random.Random(seed)
    cases = []
    for i in range(n_clean):
        cases.append(build_case(rng, "c%05d" % i, False))
    for i in range(n_raw):
        cases.append(build_case(rng, "r%05d" % i, True))
    return cases
