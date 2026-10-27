#!/usr/bin/env python3
"""census.py - compile >=200 keymaps from random RMLVO names with the pinned
libxkbcommon 1.13.2 `xkbcli compile-keymap` (clean environment, scratch HOME)
and census every syntax construct the serializer actually emits, using
parse.py.

Usage:
  census.py --work DIR --out DIR [--count N] [--seed S]

  --work  scratch work dir.  A dir under /tmp or /var/tmp is REFUSED
          (operator directive: no /tmp work dirs).  Defaults to $TMPDIR.
  --out   receipt dir (a seat dir); the driver copies receipts from there.

Outputs (in --out):
  census.txt            construct<TAB>total<TAB>keymaps_with<TAB>example
  census-keymaps.tsv    one row per compiled keymap: id, RMLVO, sha256, stats
  compile-log.txt       one row per attempt: id, rc, bytes, stderr class
  manifest.json         entries + stats (input for verify.py)
  pins.sha256           digests of the binaries and xkbcli list input

The RMLVO draw is seeded and reproducible from (--seed, xkbcli list bytes).
"""

import argparse
import collections
import hashlib
import json
import os
import random
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import parse as kap  # noqa: E402

COMPILE = "/usr/lib/xkbcommon/xkbcli-compile-keymap"
COMPILE_SHA256 = ("43b924f68651500e022c74371515154f8c50a2e087defa6b834cc5d41fd77250")
HOW_TO_TYPE = "/usr/lib/xkbcommon/xkbcli-how-to-type"
HOW_TO_TYPE_SHA256 = ("f6c0b122ad90c9e30086653517c51f4b2203b6c7c07bcbc89c71e55ab2927e54")
KEYSYM_HEADER = "/usr/include/xkbcommon/xkbcommon-keysyms.h"
KEYSYM_HEADER_SHA256 = ("13023369f65a17411606084e3e09557b4886aeb15f89affba4aaa86490a463f3")

TMP_ROOTS = ("/tmp", "/var/tmp")

# Every construct parse.py can accept.  The census prints a row for each one,
# so a construct that never occurs is visible as a zero and not as silence.
CONSTRUCTS = [
    "section_xkb_keycodes", "section_xkb_types", "section_xkb_compatibility",
    "section_xkb_symbols",
    "section_xkb_keycodes_quoted", "section_xkb_types_quoted",
    "section_xkb_compatibility_quoted", "section_xkb_symbols_quoted",
    "section_xkb_keycodes_bare", "section_xkb_types_bare",
    "section_xkb_compatibility_bare", "section_xkb_symbols_bare",
    "kc_minimum", "kc_maximum", "kc_key", "kc_alias", "kc_indicator",
    "types_virtual_modifiers", "types_vmod_explicit_mapping", "types_type",
    "types_modifiers", "types_map_entry", "types_preserve_entry",
    "types_level_name",
    "compat_global", "compat_global_useModMapMods", "compat_global_repeat",
    "compat_interpret", "compat_action", "compat_action_block",
    "compat_indicator", "compat_virtual_modifiers",
    "compat_block_virtualModifier", "compat_block_useModMapMods",
    "compat_block_repeat", "action_call",
    "symbols_name_group", "symbols_key", "symbols_key_simple",
    "symbols_symbols_group", "symbols_type_default", "symbols_type_group",
    "symbols_actions_group", "symbols_repeat", "symbols_virtualMods",
    "symbols_groupsClamp", "symbols_groupsRedirect", "symbols_modifier_map",
    "symbols_modifier_map_key", "symbols_key_no_symbols",
    "level", "level_single", "level_multi", "level_empty",
    "level_multi_keysym", "level_nosymbol_dropped", "level_trailing_trimmed",
    "level_cleared_by_type",
    "keysym_token", "keysym_named", "keysym_unicode", "keysym_hex",
    "keysym_decimal", "keysym_nosymbol",
    "string", "string_nonascii", "escape_newline", "escape_backslash",
    "escape_octal",
    "cell_single", "cell_empty", "cell_multi",
    "judge_cell_reachable", "judge_cell_unreachable",
    "judge_unreachable_level0", "judge_unreachable_levelN", "type_none_entry",
    "keyname", "mask_modifier", "mask_none", "mask_numeric",
    "type_undefined_fallback", "types_duplicate_name", "kc_duplicate_name",
    "symbols_key_duplicate", "symbols_key_unknown_in_keycodes",
]

LAYOUT_RE = re.compile(r"^- layout: '([^']*)'")
VARIANT_RE = re.compile(r"^  variant: '([^']*)'")
OPTGROUP_RE = re.compile(r"^- name: '([^']*)'")
OPTION_RE = re.compile(r"^  - name: '([^']*)'")
MODEL_RE = re.compile(r"^- name: '?([^']*)'?$")
LAYOUT_SPECIFIC_RE = re.compile(r"^    layout-specific: (true|false)")


def kap_keysym_check(header):
    """Compare parse.is_keypad_spelling() with xkb_keysym_is_keypad()'s value
    range over every XKB_KEY_* define in the header."""
    import re as _re
    names = {}
    with open(header, encoding="utf-8") as f:
        for line in f:
            if not line.startswith("#define"):
                continue
            m = _re.match(r"#define\s+XKB_KEY_(\w+)\s+(0x[0-9A-Fa-f]+|\d+)", line)
            if m:
                raw = m.group(2)
                names[m.group(1)] = int(raw, 16) if raw.lower().startswith("0x") else int(raw, 10)
    mism = []
    for name, value in names.items():
        truth = kap.KP_MIN <= value <= kap.KP_MAX
        got = kap.is_keypad_spelling(name)
        if truth != got:
            mism.append(name)
    kp_names = [n for n in names if n.startswith("KP_")]
    return {"defines": len(names), "kp_defines": len(kp_names),
            "mismatches": sorted(mism)[:10], "mismatch_count": len(mism)}


def die(msg):
    print("census: " + msg, file=sys.stderr)
    raise SystemExit(2)


def check_work(path):
    if not path:
        die("--work is required (or set TMPDIR); no implicit work dir")
    real = os.path.realpath(path)
    for root in TMP_ROOTS:
        if real == root or real.startswith(root + "/"):
            die("refusing work dir under %s: %s" % (root, real))
    if os.path.commonpath([real, "/"]) == "/" and real.count("/") < 2:
        die("refusing suspicious work dir %s" % real)
    os.makedirs(real, exist_ok=True)
    return real


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def clean_env(home):
    return {
        "PATH": "/usr/bin",
        "HOME": home,
        "XDG_CACHE_HOME": os.path.join(home, ".cache"),
        "XDG_CONFIG_HOME": os.path.join(home, ".config"),
        "XDG_DATA_HOME": os.path.join(home, ".local", "share"),
        "XDG_STATE_HOME": os.path.join(home, ".local", "state"),
        "LC_ALL": "C",
    }


def run(argv, env, cwd):
    return subprocess.run(argv, env=env, cwd=cwd, stdin=subprocess.DEVNULL,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          timeout=60)


def parse_list(text):
    """Parse `xkbcli list` (YAML-ish, no yaml module in stdlib guarantee)."""
    models = []
    layouts = []          # (layout, variant)
    options = []          # (name, layout_specific)
    section = None
    cur_layout = None
    cur_opt = None
    for line in text.splitlines():
        if line in ("models:", "layouts:", "option_groups:"):
            section = line[:-1]
            continue
        if section == "models":
            m = MODEL_RE.match(line)
            if m:
                models.append(m.group(1))
        elif section == "layouts":
            m = LAYOUT_RE.match(line)
            if m:
                cur_layout = [m.group(1), ""]
                layouts.append(cur_layout)
                continue
            m = VARIANT_RE.match(line)
            if m and cur_layout is not None:
                cur_layout[1] = m.group(1)
        elif section == "option_groups":
            m = OPTGROUP_RE.match(line)
            if m:
                cur_opt = [m.group(1), False]
                continue
            m = OPTION_RE.match(line)
            if m:
                cur_opt = [m.group(1), False]
                options.append(cur_opt)
                continue
            m = LAYOUT_SPECIFIC_RE.match(line)
            if m and cur_opt is not None:
                cur_opt[1] = (m.group(1) == "true")
    return models, layouts, options


def draw(rng, models, by_layout, options):
    rules = rng.choices(["evdev", "evdev", "evdev", "evdev", "base", "xorg"],
                        k=1)[0]
    model = "pc105" if rng.random() < 0.75 else rng.choice(models)
    n = rng.choices([1, 2, 3], weights=[55, 30, 15], k=1)[0]
    names = rng.sample(sorted(by_layout), n)
    variants = []
    for name in names:
        variants.append(rng.choice(by_layout[name]))
    nopt = rng.choices([0, 1, 2, 3, 4], weights=[25, 30, 25, 15, 5], k=1)[0]
    opts = rng.sample([o[0] for o in options], nopt) if nopt else []
    return {"rules": rules, "model": model,
            "layout": ",".join(names), "variant": ",".join(variants),
            "options": ",".join(opts)}


def rmlvo_argv(rmlvo):
    argv = [COMPILE, "--rules", rmlvo["rules"], "--model", rmlvo["model"],
            "--layout", rmlvo["layout"]]
    if rmlvo["variant"].strip(","):
        argv += ["--variant", rmlvo["variant"]]
    if rmlvo["options"]:
        argv += ["--options", rmlvo["options"]]
    return argv


def stderr_class(stderr):
    text = stderr.decode("utf-8", "replace")
    ids = re.findall(r"XKB-(\\d+)", text)
    if ids:
        return "XKB-" + ",".join(sorted(set(ids)))
    first = text.splitlines()[0] if text.splitlines() else ""
    return ("ERROR:" + first[:60]) if first else ""


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default=os.environ.get("TMPDIR"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--count", type=int, default=240)
    ap.add_argument("--seed", type=int, default=49)
    args = ap.parse_args(argv[1:])

    work = check_work(args.work)
    out = os.path.abspath(args.out)
    os.makedirs(out, exist_ok=True)
    home = os.path.join(work, "home")
    os.makedirs(os.path.join(home, ".config"), exist_ok=True)
    env = clean_env(home)

    # -- pins ---------------------------------------------------------
    got = sha256_file(COMPILE)
    if got != COMPILE_SHA256:
        die("compile-keymap sha256 %s != pin %s" % (got, COMPILE_SHA256))
    got_h2t = sha256_file(HOW_TO_TYPE)
    header_sha = sha256_file(KEYSYM_HEADER)
    list_run = run(["/usr/lib/xkbcommon/xkbcli-list"], env, work)
    if list_run.returncode != 0:
        die("xkbcli list failed rc=%d: %r" % (list_run.returncode, list_run.stderr[:200]))
    list_bytes = list_run.stdout
    # keysym classifier cross-check: the spelling-based is_keypad() must agree
    # with the value range over every canonical name in the pinned header.
    kp = kap_keysym_check(KEYSYM_HEADER)

    with open(os.path.join(out, "pins.sha256"), "w") as f:
        f.write("compile-keymap %s %s\n" % (got, COMPILE))
        f.write("how-to-type %s %s\n" % (got_h2t, HOW_TO_TYPE))
        f.write("keysyms-header %s %s\n" % (header_sha, KEYSYM_HEADER))
        f.write("xkbcli-list %s <stdout of xkbcli-list>\n"
                % hashlib.sha256(list_bytes).hexdigest())

    models, layouts, options = parse_list(list_bytes.decode("utf-8", "replace"))
    if not models or not layouts or not options:
        die("xkbcli list parse produced models=%d layouts=%d options=%d"
            % (len(models), len(layouts), len(options)))
    by_layout = collections.defaultdict(list)
    for name, variant in layouts:
        by_layout[name].append(variant)

    rng = random.Random(args.seed)
    kmdir = os.path.join(work, "keymaps")
    os.makedirs(kmdir, exist_ok=True)

    attempts = []
    entries = []
    cells = []
    attempt = 0
    target = args.count
    max_attempts = target * 2
    while len(entries) < target and attempt < max_attempts:
        attempt += 1
        rmlvo = draw(rng, models, by_layout, options)
        argv_c = rmlvo_argv(rmlvo)
        res = run(argv_c, env, work)
        cid = "km%03d" % attempt
        cls = stderr_class(res.stderr)
        attempts.append({"id": cid, "rc": res.returncode,
                         "bytes": len(res.stdout), "stderr_class": cls,
                         "rmlvo": rmlvo})
        if res.returncode != 0 or not res.stdout:
            continue
        text = res.stdout.decode("utf-8")
        try:
            km, counts, stats = kap.parse_census(text)
        except (kap.OutOfContract, kap.ParseError) as exc:
            die("%s: parse.py rejected serializer output: %s: %s"
                % (cid, type(exc).__name__, exc))
        path = os.path.join(kmdir, cid + ".xkb")
        with open(path, "wb") as f:
            f.write(res.stdout)
        counts["keymap"] += 1
        entries.append({"id": cid, "path": path, "rmlvo": rmlvo,
                        "sha256": stats["sha256"], "stats": stats,
                        "counts": dict(counts)})
        cells.append(counts)

    if len(entries) < target:
        die("only %d/%d keymaps compiled rc=0 in %d attempts"
            % (len(entries), target, attempt))

    total = collections.Counter()
    keymaps_with = collections.Counter()
    for counts in cells:
        for key in counts:
            total[key] += counts[key]
            keymaps_with[key] += 1
    # Constructs that parse.py accepts but no keymap used.
    for key in CONSTRUCTS:
        total.setdefault(key, 0)
        keymaps_with.setdefault(key, 0)

    # Aggregate model stats.
    stats_total = collections.Counter()
    groups_hist = collections.Counter()
    levels_hist = collections.Counter()
    width_hist = collections.Counter()
    type_names = collections.Counter()
    examples = {}
    for e in entries:
        st = e["stats"]
        for key in ("keys", "types", "group_slots", "level_slots",
                    "group_explicit_type",
                    "group_inferred_type", "cells", "distinct_spellings",
                    "bytes", "lines"):
            stats_total[key] += st[key]
        stats_total["max_groups"] = max(stats_total["max_groups"], st["max_groups"])
        stats_total["max_levels"] = max(stats_total["max_levels"], st["max_levels"])
        for k, v in json.loads(json.dumps(st["groups_hist"])).items():
            groups_hist[int(k)] += v
        for k, v in st["levels_hist"].items():
            levels_hist[int(k)] += v
        for k, v in st["inferred_width_hist"].items():
            width_hist[int(k)] += v
        for t in st.get("type_names", []):
            type_names[t] += 1
        if len(examples) == 0:
            km = kap.parse(open(e["path"], encoding="utf-8").read())
            for name, val in km.section_names.items():
                examples["section_" + name] = str(val)
            examples["types_type"] = ",".join(t.name for t in km.types[:4])
            spellings = km.distinct_spellings()
            for kind in ("named", "unicode", "hex"):
                hit = [s for s in spellings if kap.spelling_class(s) == kind]
                examples["keysym_" + kind] = hit[0] if hit else "-"
            defaults = [k.name + "=" + k.default_type for _, k in km.resolved_keys()
                        if k.default_type]
            examples["symbols_type_default"] = defaults[0] if defaults else "-"
            grouped = [k.name + ":" + str(g + 1) + "=" + grp.type_name
                       for _, k in km.resolved_keys()
                       for g, grp in sorted(k.groups.items()) if grp.type_name]
            examples["symbols_type_group"] = grouped[0] if grouped else "-"
            repeats = [k.name + "=" + str(k.repeat) for _, k in km.resolved_keys()
                       if k.repeat]
            examples["symbols_repeat"] = repeats[0] if repeats else "-"
            vmods = [k.name + "=" + str(k.virtual_mods)
                     for _, k in km.resolved_keys() if k.virtual_mods]
            examples["symbols_virtualMods"] = vmods[0] if vmods else "-"
            multi = [str((kc, g, lvl)) for (kc, g, lvl, syms) in km.table()
                     if len(syms) > 1]
            examples["level_multi"] = multi[0] if multi else "-"
            if km.aliases:
                an = sorted(km.aliases)[0]
                examples["kc_alias"] = "<%s> = <%s>" % (an, km.aliases[an])
            if km.group_names:
                g1 = sorted(km.group_names)[0]
                examples["symbols_name_group"] = km.group_names[g1]
    failed = [a for a in attempts if a["rc"] != 0]

    with open(os.path.join(out, "compile-log.txt"), "w") as f:
        f.write("# id\trc\tbytes\tstderr_class\trules\tmodel\tlayout\tvariant\toptions\n")
        for a in attempts:
            r = a["rmlvo"]
            f.write("%s\t%d\t%d\t%s\t%s\t%s\t%s\t%s\t%s\n"
                    % (a["id"], a["rc"], a["bytes"], a["stderr_class"] or "-",
                       r["rules"], r["model"], r["layout"], r["variant"],
                       r["options"] or "-"))

    with open(os.path.join(out, "census-keymaps.tsv"), "w") as f:
        f.write("# id\tsha256\tbytes\tlines\tkeys\tgroup_slots\tmax_groups\t"
                "max_levels\tlevel_slots\tcells\tdistinct_spellings\texplicit\tinferred\t"
                "rules\tmodel\tlayout\tvariant\toptions\n")
        for e in entries:
            st = e["stats"]
            r = e["rmlvo"]
            f.write("%s\t%s\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%s\t%s\t%s\t%s\t%s\n"
                    % (e["id"], e["sha256"], st["bytes"], st["lines"], st["keys"],
                       st["group_slots"], st["max_groups"], st["max_levels"],
                       st["level_slots"], st["cells"], st["distinct_spellings"],
                       st["group_explicit_type"], st["group_inferred_type"],
                       r["rules"], r["model"], r["layout"], r["variant"],
                       r["options"] or "-"))

    with open(os.path.join(out, "census.txt"), "w") as f:
        f.write("# serialized-keymap syntax census, mado round 49 w1 ExecKeymapParse\n")
        f.write("compile-keymap= %s sha256=%s\n" % (COMPILE, got))
        f.write("how-to-type= %s sha256=%s\n" % (HOW_TO_TYPE, got_h2t))
        f.write("keysyms-header= %s sha256=%s\n" % (KEYSYM_HEADER, header_sha))
        f.write("xkbcli-list sha256=%s models=%d layout-variant-pairs=%d "
                "layouts=%d options=%d\n"
                % (hashlib.sha256(list_bytes).hexdigest(), len(models),
                   len(layouts), len(by_layout), len(options)))
        f.write("attempts=%d compiled_rc0=%d failed=%d seed=%d target=%d\n"
                % (len(attempts), len(entries), len(failed), args.seed, target))
        f.write("keymaps=%d bytes_total=%d keys_total=%d group_slots=%d "
                "level_slots=%d cells_total=%d distinct_spellings_total=%d\n"
                % (len(entries), stats_total["bytes"], stats_total["keys"],
                   stats_total["group_slots"], stats_total["level_slots"],
                   stats_total["cells"], stats_total["distinct_spellings"]))
        f.write("max_groups=%d max_levels=%d explicit_type_groups=%d "
                "inferred_type_groups=%d\n"
                % (stats_total["max_groups"], stats_total["max_levels"],
                   stats_total["group_explicit_type"],
                   stats_total["group_inferred_type"]))
        f.write("groups_hist " + json.dumps({str(k): v for k, v in sorted(groups_hist.items())}) + "\n")
        f.write("levels_hist " + json.dumps({str(k): v for k, v in sorted(levels_hist.items())}) + "\n")
        f.write("inferred_width_hist " + json.dumps({str(k): v for k, v in sorted(width_hist.items())}) + "\n")
        f.write("type_definitions " + json.dumps({k: v for k, v in sorted(type_names.items())}) + "\n")
        f.write("keysym_classifier " + json.dumps(kp) + "\n")
        f.write("\nconstruct\ttotal\tkeymaps_with\texample\n")
        for key in sorted(set(total) | set(CONSTRUCTS)):
            example = examples.get(key, "-")
            f.write("%s\t%d\t%d\t%s\n" % (key, total[key], keymaps_with[key], example))

    with open(os.path.join(out, "manifest.json"), "w") as f:
        json.dump({"seed": args.seed, "count": len(entries),
                   "compile": COMPILE, "compile_sha256": got,
                   "how_to_type": HOW_TO_TYPE,
                   "how_to_type_sha256": got_h2t,
                   "keysyms_header": KEYSYM_HEADER,
                   "keysyms_header_sha256": header_sha,
                   "entries": entries}, f, indent=1)

    print("census: attempts=%d compiled=%d failed=%d keymaps=%d"
          % (len(attempts), len(entries), len(failed), len(entries)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
