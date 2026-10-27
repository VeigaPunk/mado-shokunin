#!/usr/bin/env python3
"""Seat harness: edge cases the RMLVO corpus cannot reach.

A. ``format1`` -- a keymap compiled with ``--format 1`` (no canonical virtual
   modifier mappings in the text).  Shows what the *load* format does: the judge
   loads with format 2 (``DEFAULT_INPUT_KEYMAP_FORMAT``), which gives an unbound
   virtual modifier the canonical mapping ``1 << index``, so ``mods.py``'s
   ``fmt_v2`` table is the one that matches the judge even for format-1 text.
B. ``none``    -- ``virtual_modifiers M = none;`` plus a type naming ``M``: the
   entry is deactivated (``entry_is_active``) and, because its mapping is 0, ``M``
   is named in *every* printed mask.
C. ``synth``   -- duplicate ``map[none]`` entries (duplicate rows), ``map[none]= 3``
   (an active empty-mask entry that suppresses the level-1 empty mask), and a type
   with 102 entries for one level (the 100-mask cap of ``tools/how-to-type.c:27``).
   Keys carry Unicode keysyms no xkeyboard-config layout uses, so the judge rows
   belong to the synthetic keys alone.

Writes only the receipt and its scratch keymap files.
"""

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import diff_mods as dm  # noqa: E402
import mods  # noqa: E402

CATEGORIES = ("mask_mismatch", "nlevels_mismatch", "table_mismatch",
              "judge_mismatch", "judge_rc", "missing_key", "cell_mismatch")


def fresh_stats():
    return {"keymaps": 0, "rows": 0, "cells": 0, "table_mismatch": 0,
            "cell_mismatch": 0, "mask_mismatch": 0, "nlevels_mismatch": 0,
            "layout_mismatch": 0, "missing_key": 0, "judge_runs": 0,
            "judge_rows": 0, "judge_mismatch": 0, "judge_rc": 0, "keys": 0,
            "type_names": set()}


def compile_text(layout, options, work, env_home, fmt=None, variant=None):
    args = [dm.COMPILE, "--layout", layout]
    if variant:
        args += ["--variant", variant]
    if options:
        args += ["--options", options]
    if fmt is not None:
        args += ["--format", str(fmt)]
    env = {"PATH": dm.CLEAN_PATH, "HOME": env_home,
           "XDG_CONFIG_HOME": os.path.join(env_home, ".config")}
    p = subprocess.run(args, capture_output=True, env=env, cwd=work, timeout=120)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.decode()[:400])
    return p.stdout.decode()


def section_bounds(text, section):
    m = re.search(r"(xkb_%s)(\s*\"[^\"]*\")?\s*\{" % section, text)
    if not m:
        raise RuntimeError("no section " + section)
    open_index = m.end() - 1
    close = dm._match_brace(text, open_index)
    return m, open_index, close


def insert_after_vmods(text, payload):
    """Insert a type block just after the types section's virtual_modifiers line."""
    _m, open_index, close = section_bounds(text, "types")
    body = text[open_index:close]
    vmods = re.search(r"virtual_modifiers[^;]*;", body)
    if not vmods:
        raise RuntimeError("no virtual_modifiers line")
    at = open_index + vmods.end()
    return text[:at] + "\n" + payload + text[at:]


def insert_in_symbols(text, payload):
    """Append key statements at the end of the symbols section: for a key that
    already exists there, the last definition wins, so the synthetic type is the
    one that takes effect."""
    _m, open_index, close = section_bounds(text, "symbols")
    return text[:close] + payload + text[close:]


def add_vmod_both(text, name_spec):
    """Append ``name_spec`` (e.g. ``TestVmod=none``) to both virtual_modifiers lines."""
    out, count = [], 0
    for line in text.splitlines(True):
        if line.lstrip().startswith("virtual_modifiers") and line.rstrip().endswith(";"):
            out.append(line.rstrip("\n").rstrip(";").rstrip() + "," + name_spec + ";\n")
            count += 1
        else:
            out.append(line)
    if count != 2:
        raise RuntimeError("expected 2 virtual_modifiers lines, saw %d" % count)
    return "".join(out)


def run_block(lib, kc, syms_table, text, work, env_home, fmt_v2=True,
              trace_keys=()):
    path = os.path.join(work, "edge.xkb")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    stats = fresh_stats()
    bad = []
    parsed, types, key_types, names, masks = dm.compare_keymap(
        lib, text, kc, syms_table, stats, bad, fmt_v2=fmt_v2)
    dm.judge_layer(lib, work, text, parsed, key_types, names, masks,
                   syms_table, stats, bad, env_home, 0)
    lines = ["rows=%d keys=%d judge_runs=%d judge_rows=%d"
             % (stats["rows"], stats["keys"], stats["judge_runs"],
                stats["judge_rows"])]
    for label in CATEGORIES:
        lines.append("  %-16s %d" % (label, stats[label]))
    for item in bad[:8]:
        lines.append("  " + repr(item)[:400])
    km = lib.keymap(text)
    gt = lib.gt(km)
    for kname in trace_keys:
        rows = [row for row in gt if row[1] == kname]
        lines.append("  trace %-6s type=%-12s levels=%s"
                     % (kname,
                        key_types.get(kname, [{}])[0].get("name")
                        if key_types.get(kname) else "?",
                        {row[4]: [mods.format_modifiers(m, names, masks)
                                  for m in row[5]] for row in rows}))
    return lines, stats, path


def main(argv):
    work, receipt = argv[1], argv[2]
    os.makedirs(work, exist_ok=True)
    env_home = os.path.realpath(os.path.join(work, "home"))
    os.makedirs(os.path.join(env_home, ".config"), exist_ok=True)
    lib = dm.Lib(dm.LIBPATH)
    kc = dm.KeysymClass(lib)
    syms_table = dm.load_keysyms()
    lines = ["# mods.py edge cases vs the pinned judge "
             "(%s, load format 2)" % os.path.basename(dm.JUDGE), ""]
    totals = 0

    # ------------------------------------------------------------- A. format 1
    text = compile_text("br", "compose:caps", work, env_home, fmt=1)
    vmods_line = [ln.strip() for ln in text.splitlines()
                  if ln.lstrip().startswith("virtual_modifiers")][0]
    lines.append("## A. format-1 keymap (`--format 1`)")
    lines.append("virtual_modifiers line: %s" % vmods_line)
    for fmt in (1, 2):
        names, masks = lib.mods_table(lib.keymap(text, fmt=fmt))
        lines.append("  library load format %d: %s" % (fmt, list(zip(names[8:], masks[8:]))))
    parsed = dm.parse_keymap(text)
    for fmt_v2 in (True, False):
        names, masks, _ = dm.build_tables(parsed, fmt_v2=fmt_v2)
        lines.append("  model fmt_v2=%-5s: %s" % (fmt_v2, list(zip(names[8:], masks[8:]))))
    block, stats, _path = run_block(lib, kc, syms_table, text, work, env_home,
                                    fmt_v2=True)
    totals += sum(stats[k] for k in CATEGORIES)
    lines += ["  judge differential (model fmt_v2=True): " + block[0]] + block[1:]
    lines.append("")

    # ------------------------------------------------------- B. `= none` vmod
    base = compile_text("us", None, work, env_home)
    text = add_vmod_both(base, "TestVmod=none")
    text = insert_after_vmods(text, """
\ttype "EDGE_none_vmod" {
\t\tmodifiers= Shift+TestVmod;
\t\tmap[Shift]= 2;
\t\tmap[TestVmod]= 2;
\t\tmap[Shift+TestVmod]= 2;
\t\tlevel_name[1]= "Base";
\t\tlevel_name[2]= "Shift";
\t};
""")
    text = insert_in_symbols(text, """
\tkey <FK01> {
\t\ttype= "EDGE_none_vmod",
\t\tsymbols[1]= [ U1F700, U1F701 ]
\t};
""")
    lines.append("## B. `virtual_modifiers TestVmod=none` with a type naming it")
    block, stats, path = run_block(lib, kc, syms_table, text, work, env_home,
                                   trace_keys=("FK01",))
    totals += sum(stats[k] for k in CATEGORIES)
    lines += block
    rows, out, err, rc = dm.run_judge(path, "U1F700", env_home)
    lines.append("  judge U1F700 rc=%d rows=%s" % (rc, rows))
    kt = dm.build_json_types(dm.parse_keymap(text),
                             *dm.build_tables(dm.parse_keymap(text))[:2],
                             {n: i for i, n in enumerate(
                                 dm.build_tables(dm.parse_keymap(text))[0])}
                             )["EDGE_none_vmod"]
    lines.append("  model: entries=%s" % [
        {"mods": e["mods"], "level": e["level"], "active": mods.entry_is_active(e)}
        for e in kt["entries"]])
    lines.append("  model: level1 masks=%r level2 masks=%r"
                 % (mods.mods_for_level(kt, 0), mods.mods_for_level(kt, 1)))
    lines.append("")

    # --------------------------------------------------------- C. type edges
    cap_entries = []
    names_all = ["Shift", "Lock", "Control", "Mod1", "Mod2", "Mod3", "Mod4",
                 "Mod5", "NumLock", "Alt", "LevelThree", "Super", "LevelFive",
                 "Meta"]
    for mask in range(1, 1 << len(names_all)):
        picked = [names_all[i] for i in range(len(names_all)) if mask >> i & 1]
        if len(picked) > 3:
            continue
        cap_entries.append("+".join(picked))
        if len(cap_entries) == 102:
            break
    text = insert_after_vmods(base, """
\ttype "EDGE_dup" {
\t\tmodifiers= none;
\t\tmap[none]= 1;
\t\tmap[none]= 1;
\t\tlevel_name[1]= "Any";
\t};
\ttype "EDGE_none3" {
\t\tmodifiers= Shift;
\t\tmap[none]= 3;
\t\tmap[Shift]= 2;
\t\tlevel_name[1]= "Base";
\t\tlevel_name[2]= "Shift";
\t\tlevel_name[3]= "Empty";
\t};
\ttype "EDGE_cap" {
\t\tmodifiers= Shift+Lock+Control+Mod1+Mod2+Mod3+Mod4+Mod5+NumLock+Alt+LevelThree+Super+LevelFive+Meta;
""" + "".join("\t\tmap[%s]= 2;\n" % c for c in cap_entries) + """\t\tlevel_name[1]= "Base";
\t\tlevel_name[2]= "Many";
\t};
\ttype "EDGE_names" {
\t\tmodifiers= Shift;
\t\tmap[Shift]= 2;
\t\tlevel_name[1]= "Base";
\t\tlevel_name[2]= "Shift";
\t\tlevel_name[3]= "Phantom3";
\t\tlevel_name[4]= "Phantom4";
\t};
\ttype "EDGE_clamp" {
\t\tmodifiers= Shift;
\t\tmap[Shift]= 2;
\t\tmap[Shift+Control]= 2;
\t\tlevel_name[1]= "Base";
\t\tlevel_name[2]= "Shift";
\t};
""")
    text = insert_in_symbols(text, """
\tkey <FK01> {
\t\ttype= "EDGE_dup",
\t\tsymbols[1]= [ U1F700, U1F701 ]
\t};
\tkey <FK02> {
\t\ttype= "EDGE_none3",
\t\tsymbols[1]= [ U1F702, U1F703, U1F704 ]
\t};
\tkey <FK03> {
\t\ttype= "EDGE_cap",
\t\tsymbols[1]= [ U1F705, U1F706 ]
\t};
\tkey <FK04> {
\t\ttype= "EDGE_names",
\t\tsymbols[1]= [ U1F708, U1F709, U1F70A, U1F70B ]
\t};
\tkey <FK05> {
\t\ttype= "EDGE_clamp",
\t\tsymbols[1]= [ U1F70C, U1F70D ]
\t};
""")
    lines.append("## C. synthetic types: duplicate map[none], map[none]= 3, 102-entry cap")
    block, stats, path = run_block(lib, kc, syms_table, text, work, env_home,
                                   trace_keys=("FK01", "FK02", "FK03", "FK04",
                                                "FK05"))
    totals += sum(stats[k] for k in CATEGORIES)
    lines += block
    parsed = dm.parse_keymap(text)
    tnames, tmasks = dm.build_tables(parsed)[:2]
    nti = {n: i for i, n in enumerate(tnames)}
    types = dm.build_json_types(parsed, tnames, tmasks, nti)
    for tname in ("EDGE_dup", "EDGE_none3", "EDGE_cap", "EDGE_names",
                  "EDGE_clamp"):
        kt = types[tname]
        cells = {level: mods.level_cells(kt, level, tnames, tmasks)
                 for level in range(mods.num_levels(kt))}
        lines.append("  %-11s num_levels=%d entries=%d cells=%s"
                     % (tname, mods.num_levels(kt), len(kt["entries"]),
                        {k: (v[:3] + (["..."] if len(v) > 3 else []), len(v))
                         for k, v in cells.items()}))
    for sym in ("U1F700", "U1F702", "U1F704", "U1F705", "U1F706", "U1F708",
                "U1F70B", "U1F70C", "U1F70D"):
        rows, _out, _err, rc = dm.run_judge(path, sym, env_home)
        lines.append("  judge %-7s rc=%d rows=%d first=%s"
                     % (sym, rc, len(rows), rows[:2]))
    lines.append("")

    # ------------------------------------------------------- D. host sample
    text = compile_text("br", "compose:caps", work, env_home)
    path = os.path.join(work, "host.xkb")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    lines.append("## D. host sample keymap (br, compose:caps) -- the C1 contract sample")
    parsed = dm.parse_keymap(text)
    tnames, tmasks, _nti = dm.build_tables(parsed)
    ktype_map = dm.model_types(parsed, dm.build_json_types(parsed, tnames, tmasks,
                                                           {n: i for i, n in
                                                            enumerate(tnames)}),
                               kc, syms_table)
    for sym in ("slash", "Return", "nosuchsym"):
        rows, out, err, rc = dm.run_judge(path, sym, env_home)
        lines.append("  judge --keysym %-10s rc=%d rows=%s"
                     % (sym, rc, [(r[1], r[3], r[4]) for r in rows]))
        if err.strip():
            lines.append("    stderr: %s" % err.strip().splitlines()[0][:120])
    lines.append("  model modifier cells per level, AD01 (FOUR_LEVEL_SEMIALPHABETIC):")
    for level in range(4):
        lines.append("    level %d: %r" % (level + 1,
                                           mods.level_cells(ktype_map["AD01"][0],
                                                            level, tnames, tmasks)))
    lines.append("  model modifier cells per level, AB11:")
    for level in range(4):
        lines.append("    level %d: %r" % (level + 1,
                                           mods.level_cells(ktype_map["AB11"][0],
                                                            level, tnames, tmasks)))
    lines.append("")

    lines.append("TOTAL_MISMATCHES %d" % totals)
    text_out = "\n".join(lines) + "\n"
    with open(receipt, "w", encoding="utf-8") as fh:
        fh.write(text_out)
    print(text_out)
    return 1 if totals else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
