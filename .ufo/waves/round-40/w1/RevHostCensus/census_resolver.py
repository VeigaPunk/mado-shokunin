#!/usr/bin/env python3
"""RevHostCensus -- independent host census for mado r40 w1.

Own implementation, written without reading tools/mado-options.py or the L1
reference tool's logic (the reference tool's *label vocabulary* is quoted in
the frozen registration and used only as the comparison partition).

Model, derived from the live compositor (Hyprland 0.56.2 efb5099, hyprlang
0.6.8) and the host config trees only:

  * config walk: depth-first `source =`, ~ expansion, glob expansion sorted,
    hyprlang variables global + sequential (parse-time) substitution,
    brace sections fold to dotted keys, last declarer wins;
  * host conversion per native form (form observed via my own
    `hyprctl getoption -j` capture):
      int     -> hyprlang configStringToInt semantics: 0x hex, decimal,
                 true/on/yes -> 1, false/off/no -> 0, rgb(r,g,b)/rgba hex
                 -> packed 0xAARRGGBB; leading yes/no-family token tolerated
                 (observed: `animations:enabled = yes, please :)` -> int 1,
                 set=true on the host);
      float   -> float(text);
      str     -> raw text;
      custom  -> gradient: colors as lowercase unpadded AARRGGBB tokens,
                 angle `<n>deg`, colors cleared and angle kept when a later
                 declaration has no `deg` token (state mutated per option in
                 declaration order); gaps: CSS 1-4-token expansion;
                 font weight: name -> numeric weight.
  * labels (lane divergence vocabulary):
      agreement   live == converted declared, set=true, one declarer
      agreement*  same, but the key has >1 declarer in the tree
      mismatch    live != converted declared, or set=false despite declarer

Reads: $HOME/.config/hypr/hyprland.conf tree, a live capture jsonl.
Writes: census.jsonl + a stdout summary. Stdlib only, no writes to configs.
"""

import glob
import json
import os
import re
import sys

HOME = os.path.expanduser("~")
ROOT = os.path.join(HOME, ".config", "hypr", "hyprland.conf")

# ---------------------------------------------------------------- parsing

def strip_comment(line):
    out, inq, q = [], False, ""
    for ch in line:
        if inq:
            out.append(ch)
            if ch == q:
                inq = False
            continue
        if ch in "\"'":
            inq, q = True, ch
            out.append(ch)
            continue
        if ch == "#":
            break
        out.append(ch)
    return "".join(out)


def resolve_vars(val, vars_):
    for _ in range(40):
        new = re.sub(
            r"\$([A-Za-z_][A-Za-z0-9_]*)",
            lambda m: vars_.get(m.group(1), m.group(0)),
            val,
        )
        if new == val:
            return new
        val = new
    return val


DECLS = []            # (dotted key, expanded raw value, file, lineno)
MISSING_SOURCES = []  # (path, why)

def parse(path, vars_):
    path = os.path.realpath(os.path.expanduser(path))
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError as e:
        MISSING_SOURCES.append((path, str(e)))
        return
    stack = []
    for n, raw in enumerate(text.splitlines(), 1):
        line = strip_comment(raw).strip()
        if not line:
            continue
        m = re.match(r"^\$([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$", line)
        if m:  # global, sequential (parse-time) substitution
            vars_[m.group(1)] = resolve_vars(m.group(2).strip(), vars_)
            continue
        m = re.match(r"^source\s*=\s*(.+)$", line)
        if m:
            tgt = os.path.expanduser(resolve_vars(m.group(1).strip(), vars_))
            matches = sorted(glob.glob(tgt)) or [tgt]
            for t in matches:
                parse(t, vars_)
            continue
        if line.endswith("{"):
            stack.append(line[:-1].strip())
            continue
        if line == "}":
            if stack:
                stack.pop()
            continue
        m = re.match(r"^([A-Za-z0-9_:.]+)\s*=\s*(.*)$", line)
        if m:
            key = m.group(1).strip()
            val = resolve_vars(m.group(2).strip(), vars_)
            full = ":".join(stack + [key]) if stack else key
            DECLS.append((full, val, path, n))
            continue
        # positional directives (bind, exec-once, monitor, env, bezier,
        # animation, windowrule, ...) carry none of the 70 dotted options

# ---------------------------------------------------------------- conversion

def cs2i(s):
    """hyprlang v0.6.8 configStringToInt semantics (observed + S173)."""
    s = s.strip()
    if s[:2].lower() == "0x":
        return int(s, 16)
    m = re.match(r"^rgba?\(([^)]*)\)$", s)
    if m:
        h = m.group(1).strip().lower()
        if len(h) == 6:
            return int("ff" + h, 16)
        if len(h) == 8:  # RRGGBBAA -> 0xAARRGGBB
            return int(h[6:8] + h[0:6], 16)
    try:
        return int(s, 10)
    except ValueError:
        pass
    low = s.lower()
    if low in ("true", "on", "yes"):
        return 1
    if low in ("false", "off", "no"):
        return 0
    tok = re.split(r"[\s,]", low)[0]  # host tolerates trailing text ("yes, please :)")
    if tok in ("true", "on", "yes"):
        return 1
    if tok in ("false", "off", "no"):
        return 0
    raise ValueError(f"unconvertible int: {s!r}")


WEIGHTS = {
    "thin": 100, "extralight": 200, "ultralight": 200, "light": 300,
    "normal": 400, "regular": 400, "medium": 500, "semibold": 600,
    "demibold": 600, "bold": 700, "extrabold": 800, "ultrabold": 800,
    "black": 900, "heavy": 900, "ultraheavy": 1000,
}

def conv_weight(decl):
    d = decl.strip().lower()
    if d in WEIGHTS:
        return str(WEIGHTS[d])
    return str(cs2i(decl))


def conv_gradient_seq(decls_in_order):
    """Host model: each declaration clears colors; angle persists when the
    declaration has no `deg` token. Returns final toString form."""
    cols, angle = [], 0.0
    for decl, _file, _n in decls_in_order:
        new_cols = []
        for tok in decl.split():
            m = re.match(r"^rgba?\(([^)]*)\)$", tok)
            if m:
                h = m.group(1).strip().lower()
                if len(h) == 6:
                    new_cols.append("ff" + h)
                elif len(h) == 8:
                    new_cols.append(h[6:8] + h[0:6])
                else:
                    raise ValueError(f"gradient color {tok!r}")
                continue
            if tok.endswith("deg"):
                angle = float(tok[:-3])
                continue
            if tok[:2].lower() == "0x":
                new_cols.append(f"{int(tok, 16):08x}")
                continue
            raise ValueError(f"gradient token {tok!r}")
        cols = new_cols
    return " ".join(cols + [f"{angle:g}deg"])


def conv_gaps(decl):
    vals = [cs2i(p) for p in decl.split()]
    if len(vals) == 1:
        t = r = b = l = vals[0]
    elif len(vals) == 2:
        t = b = vals[0]
        l = r = vals[1]
    elif len(vals) == 3:
        t, lr, b = vals
        l = r = lr
    else:
        t, r, b, l = vals[:4]
    return f"{l} {t} {r} {b}"


def convert(key, form, decls_in_order):
    """Convert the last-declared value chain to the native form."""
    if form == "int":
        return str(cs2i(decls_in_order[-1][0]))
    if form == "float":
        return repr(float(decls_in_order[-1][0]))
    if form == "str":
        return decls_in_order[-1][0]
    # custom forms
    if "gaps_in" in key or "gaps_out" in key:
        return conv_gaps(decls_in_order[-1][0])
    if "font_weight" in key:
        return conv_weight(decls_in_order[-1][0])
    return conv_gradient_seq(decls_in_order)


def eq(form, a, b):
    if form in ("int",):
        return int(a) == int(b)
    if form == "float":
        return abs(float(a) - float(b)) < 1e-6
    return str(a) == str(b)

# ---------------------------------------------------------------- census

def main():
    live_path = sys.argv[1]
    out_path = sys.argv[2]

    parse(ROOT, {})
    by_key = {}
    order = []
    for k, v, f, n in DECLS:
        if k not in by_key:
            by_key[k] = []
            order.append(k)
        by_key[k].append((v, f, n))

    keys = [l.strip() for l in open(live_path, encoding="utf-8") if l.strip()]
    live = {}
    live_lines = open(live_path.replace("keylist.txt", "live.jsonl"), encoding="utf-8").read().splitlines()
    for k, l in zip(keys, live_lines):
        o = json.loads(l)
        form = [x for x in o if x not in ("option", "set")][0]
        live[k] = (form, o[form], bool(o["set"]))

    rows, counts = [], {"agreement": 0, "agreement*": 0, "mismatch": 0}
    no_decl, unconverted = [], []
    for k in sorted(keys):
        form, lval, lset = live[k]
        d = by_key.get(k)
        if not d:
            no_decl.append(k)
            continue
        try:
            cval = convert(k, form, d)
        except ValueError as e:
            unconverted.append((k, str(e)))
            continue
        if not eq(form, cval, str(lval)) or not lset:
            label = "mismatch"
        elif len(d) > 1:
            label = "agreement*"
        else:
            label = "agreement"
        counts[label] += 1
        rows.append({
            "key": k, "form": form, "decls": len(d),
            "declared_last": d[-1][0], "declared_files": [f"{os.path.relpath(f, HOME)}:{n}" for _, f, n in d],
            "converted": cval, "live": lval if not isinstance(lval, str) else lval,
            "set": lset, "agreement": label,
        })

    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(rows, fh, indent=1)

    print(f"census: checked={len(rows)} " +
          " ".join(f"{k}={v}" for k, v in counts.items()))
    print(f"decls-tracked-keys={len(by_key)} of live-keys={len(keys)}")
    if no_decl:
        print("NO-DECL:", no_decl)
    if unconverted:
        print("UNCONVERTED:", unconverted)
    if MISSING_SOURCES:
        print("MISSING-SOURCES:", MISSING_SOURCES)
    multi = sorted(k for k in by_key if len(by_key[k]) > 1 and k in live)
    print("multi-declarer keys:", multi)
    star = [r["key"] for r in rows if r["agreement"] == "agreement*"]
    mism = [r["key"] for r in rows if r["agreement"] == "mismatch"]
    print("agreement* keys:", star)
    print("mismatch keys:", mism)
    print("declared-keys-not-in-live:", sorted(k for k in by_key if k not in live))

if __name__ == "__main__":
    main()
