#!/usr/bin/env python3
"""Drive the hyprlang oracle and the frozen reference over the targeted edge cases.

For each case: write <case>.conf, run the oracle (host hyprlang 0.6.8) and the reference
(l1-draft/mado-devices.py), then compare the expected XKB names / scroll factor / device
block names and record whether the reference declared the case unmodelled (unsupported>0).
"""
import json
import os
import shlex
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ORACLE = os.path.join(HERE, "oracle")
REF = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/l1-draft/mado-devices.py"
WORK = os.path.join(HERE, "work")

DEVICES = {
    "mice": [
        {"name": "mouseA", "scrollFactor": 1.00},
        {"name": "touchpadB", "scrollFactor": -1.00},
    ],
    "keyboards": [
        {"name": "kbdX", "layout": "de", "variant": "", "options": "", "model": "", "rules": ""},
        {"name": "kbdY", "layout": "fr", "variant": "", "options": "", "model": "", "rules": ""},
        {"name": "hl-virtual-keyboard-1", "layout": "us", "variant": "", "options": "", "model": "", "rules": ""},
    ],
}

NAMES = ["kbdX", "kbdY", "kbdY2", "kbd$X", "0", "", "mouseA", "hl-virtual-keyboard-1"]

CASES = {
    "C00-normal-agree": "device {\n    name = kbdX\n    kb_layout = de\n}\n",
    "C01-first-key-not-name": "device {\n    kb_layout = de\n    name = kbdX\n}\n",
    "C02-second-name": "device {\n    name = kbdX\n    kb_layout = de\n    name = kbdY\n    kb_variant = intl\n}\n",
    "C03-bracket-then-name": "device[kbdX]:name = kbdY\ndevice[kbdX]:kb_layout = de\ndevice[kbdY]:kb_variant = intl\n",
    "C04-flat-key-outside": "device:kb_layout = de\n",
    "C05-flat-after-close": "device {\n    name = kbdX\n    kb_layout = de\n}\ndevice:kb_variant = intl\n",
    "C06-space-bracket": "device {\n    name = kbdX\n    kb_layout = de\n}\ndevice [kbdX]\ndevice:kb_variant = intl\n",
    "C07-brackets-in-value": "device {\n    name = kbdX\n    kb_layout = de[foo]\n}\n",
    "C08-input-bracket": "input[x]:kb_layout = de\n",
    "C09-nested-block": "misc {\n    device {\n        name = kbdX\n        kb_layout = de\n    }\n}\n",
    "C10-hash-hash-end": "device {\n    name = kbdX\n    kb_layout = de ##\n}\n",
    "C11-triple-hash": "device {\n    name = kbdX\n    kb_layout = de ###\n}\n",
    "C12-hash-after-double": "device {\n    name = kbdX\n    kb_variant = a##b#c\n}\n",
    "C13-continuation-into-comment": "device {\n    name = kbdX\n    kb_layout = de \\\n# tail comment\n}\n",
    "C14-final-continuation": "device {\n    name = kbdX\n    kb_layout = de \\\n",
    "C15-empty-rhs": "device {\n    name = kbdX\n    kb_layout =\n}\n",
    "C16-scroll-1e-40": "device {\n    name = mouseA\n    scroll_factor = 1e-40\n}\n",
    "C17-scroll-0x10": "device {\n    name = mouseA\n    scroll_factor = 0x10\n}\n",
    "C18-scroll-leading-space": "device {\n    name = mouseA\n    scroll_factor =  1.5\n}\n",
    "C19-scroll-plus-dot5e1": "device {\n    name = mouseA\n    scroll_factor = +.5e1\n}\n",
    "C20-scroll-1e39": "device {\n    name = mouseA\n    scroll_factor = 1e39\n}\n",
    "C21-variable-after-use": "device {\n    name = kbdX\n    kb_layout = $layout\n}\n$layout = de\n",
    "C22-dollar-in-name": "device {\n    name = kbd$X\n    kb_layout = de\n}\n",
    # --- extras
    "E01-second-name-only": "device {\n    name = kbdX\n    name = kbdY\n}\n",
    "E02-bare-hyprlang-comment": "#hyprlang\ndevice {\n    name = kbdX\n    kb_layout = de\n}\n",
    "E03-hyprlang-if-skip": "#hyprlang if $NOSUCHVAR\ndevice {\n    name = kbdX\n    kb_layout = de\n}\n#hyprlang endif\n",
    "E04-duplicate-blocks": "device {\n    name = kbdX\n    kb_layout = de\n}\ndevice {\n    name = kbdX\n    kb_layout = fr\n}\n",
    "E05-global-scroll": "input:scroll_factor = 2.0\ndevice {\n    name = mouseA\n}\n",
    "E06-scroll-clamp-200": "device {\n    name = mouseA\n    scroll_factor = 200\n}\n",
    "E07-flat-name-two-line": "device:name = kbdX\ndevice:kb_layout = de\n",
    "E08-global-inside-block": "device {\n    name = kbdX\n    input:kb_layout = de\n}\n",
    "E09-nested-then-key": "device {\n    name = kbdX\n    foo {\n    }\n    kb_variant = intl\n}\n",
    "E10-braces-on-one-line": "device { name = kbdX }\n",
    "E11-crlf": "device {\r\n    name = kbdX\r\n    kb_layout = de\r\n}\r\n",
    "E12-close-with-comment": "device {\n    name = kbdX\n    kb_layout = de\n} # done\n",
    "E13-empty-sentinel": "device {\n    name = kbdX\n    kb_variant = [[EMPTY]]\n}\n",
    "E14-stray-close": "}\ndevice {\n    name = kbdX\n    kb_layout = de\n}\n",
    "C23-final-continuation-no-nl": "device {\n    name = kbdX\n    kb_layout = de \\",
    "C24-final-continuation-then-blank": "device {\n    name = kbdX\n    kb_layout = de \\\n\n",
    "C25-hash-in-comment-order": "device {\n    name = kbdX\n    kb_layout = de##x#y\n}\n",
    "E16-empty-name": "device {\n    name =\n    kb_layout = de\n}\n",
    "C26-scroll-inf": "device {\n    name = mouseA\n    scroll_factor = inf\n}\n",
    "C27-scroll-nan": "device {\n    name = mouseA\n    scroll_factor = nan\n}\n",
    "C28-scroll-trailing-junk": "device {\n    name = mouseA\n    scroll_factor = 1.5x\n}\n",
    "C29-firstkey-then-name-then-key": "device {\n    kb_layout = de\n    name = kbdX\n    kb_variant = intl\n}\n",
    "C30-firstkey-no-name": "device {\n    kb_layout = de\n}\n",
    "C31-double-bracket-lhs": "device[a][b]:kb_layout = de\n",
    "C32-space-bracket-key": "device [kbdX]:kb_layout = de\n",
    "C33-input-space-bracket": "input [x]:kb_layout = de\n",
    "C34-flat-name-stray-close": "device:name = kbdX\n}\ndevice:kb_layout = de\n",
    "C35-continuation-swallows-brace": "device {\n    name = kbdX\n    kb_layout = de \\\n}\n",
    "E17-block-key-not-modelled": "device {\n    name = mouseA\n    sensitivity = 0.5\n    kb_layout = de\n}\n",
    "E15-unclosed-block": "device {\n    name = kbdX\n    kb_layout = de\n",
}


def run(cmd, **kw):
    p = subprocess.run(cmd, capture_output=True, text=True, **kw)
    return p.returncode, p.stdout, p.stderr


def oracle(conf, names):
    return run([ORACLE, conf] + names)


def reference(conf):
    return run(["python3", "-I", REF, "--devices", os.path.join(WORK, "devices.json"), "--config", conf])


def parse_oracle(out):
    """-> (parse_error, cats[(name,setlist)], fields{name:{field:projected}}, scroll{name:(explicit,float)})"""
    err = None
    cats = []
    fields = {}
    scroll = {}
    for line in out.splitlines():
        if line.startswith("ORACLE_PARSE:"):
            err = line
        elif line.startswith("ORACLE_CAT:"):
            body = line[len("ORACLE_CAT: "):]
            nm = body.split(" name=", 1)[1]
            jtxt = nm[: nm.index(" exists=")]
            s = body.split(" set=", 1)[1]
            cats.append((json.loads(jtxt), json.loads(s)))
        elif line.startswith("ORACLE_FIELD:"):
            body = line[len("ORACLE_FIELD: "):]
            nm_j = body[body.index("name=") + 5:]
            name = json.loads(nm_j[: nm_j.index(" field=")])
            field = body.split(" field=", 1)[1].split(" ")[0]
            proj_j = body.split(" projected=", 1)[1]
            fields.setdefault(name, {})[field] = json.loads(proj_j)
        elif line.startswith("ORACLE_SCROLL:"):
            body = line[len("ORACLE_SCROLL: "):]
            nm_j = body[body.index("name=") + 5:]
            name = json.loads(nm_j[: nm_j.index(" explicit=")])
            ex = int(body.split(" explicit=", 1)[1].split(" ")[0])
            fl = body.split(" float=", 1)[1].split(" resolved=")[0]
            scroll[name] = (ex, fl)
    return err, cats, fields, scroll


TOK = None


def parse_ref(out):
    import re as _re
    global TOK
    if TOK is None:
        TOK = _re.compile(r'(\w+)=("(?:[^"\\]|\\.)*"|[^\s]+)')
    kbs, mice, blocks, last = {}, [], [], None
    for line in out.splitlines():
        if line.startswith("MADO_DEV_KEYBOARD:"):
            d = {}
            for k, v in TOK.findall(line):
                try:
                    d[k] = json.loads(v)
                except Exception:
                    d[k] = v
            kbs[d["name"]] = d
        elif line.startswith("MADO_DEV_MOUSE:"):
            d = {}
            for k, v in TOK.findall(line):
                try:
                    d[k] = json.loads(v)
                except Exception:
                    d[k] = v
            mice.append((d["name"], d))
        elif line.startswith("MADO_DEV_BLOCK:"):
            d = dict(TOK.findall(line))
            blocks.append((json.loads(d["name"]), int(d["keys"])))
        elif line.startswith("MADO_DEVICES:"):
            last = line
    return kbs, mice, blocks, last


def main():
    os.makedirs(WORK, exist_ok=True)
    with open(os.path.join(WORK, "devices.json"), "w") as f:
        json.dump(DEVICES, f)
    results = {}
    for cid, conf in CASES.items():
        path = os.path.join(WORK, cid + ".conf")
        with open(path, "w", newline="") as f:
            f.write(conf)
        rc_o, out_o, err_o = oracle(path, NAMES)
        rc_r, out_r, err_r = reference(path)
        oerr, cats, fields, scroll = parse_oracle(out_o)
        kbs, mice, blocks, last = parse_ref(out_r)
        unsup = int(last.split("unsupported=")[1].split(" ")[0]) if last else -1
        verdict = last.split("verdict=")[1] if last else "?"
        # per-keyboard expected-name comparison (only when the reference claims to model it)
        kb_cmp = {}
        for nm, d in kbs.items():
            o = fields.get(nm)
            if o is None:
                kb_cmp[nm] = "no-oracle-name"
                continue
            refv = {k: d.get(k) for k in ("layout", "variant", "options", "model", "rules")}
            orav = {k: o.get("kb_" + k) for k in ("layout", "variant", "options", "model", "rules")}
            same = refv == orav
            kb_cmp[nm] = "same" if same else "DIFF %s vs %s" % (refv, orav)
        names_ref = [b[0] for b in blocks]
        names_ora = [c[0] for c in cats]
        results[cid] = {
            "oracle_rc": rc_o,
            "oracle_err": oerr,
            "oracle_stderr": err_o.strip(),
            "ref_rc": rc_r,
            "ref_unsupported": unsup,
            "ref_verdict": verdict,
            "ref_stderr": err_r.strip(),
            "ref_blocks": names_ref,
            "oracle_cats": names_ora,
            "blocks_same": names_ref == names_ora,
            "kb_cmp": kb_cmp,
            "oracle_fields": fields,
            "oracle_scroll": scroll,
            "ref_mice": mice,
            "oracle_out": out_o,
            "ref_out": out_r,
        }
    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(results, f, indent=1, sort_keys=True)
    # ---- classification: state divergences at line granularity, then by ref support
    import math
    for cid, r in results.items():
        diverged = []
        for nm, st in r["kb_cmp"].items():
            if st != "same":
                diverged.append("kb:" + nm)
        for nm, d in r["ref_mice"]:
            ex, fl = r["oracle_scroll"].get(nm, (0, "<nullptr>"))
            if fl == "<nullptr>" or ex != 1:
                exp = -1.0
            else:
                f = float(fl)
                exp = min(max(f, 0.0), 100.0)
            refv = d.get("scroll_factor")
            if refv is None:
                continue
            if not (math.isfinite(exp) is False) :
                want = "%.2f" % exp
            else:
                want = repr(exp)
            try:
                refnorm = "%.2f" % float(refv)
            except Exception:
                refnorm = str(refv)
            if want != refnorm:
                diverged.append("mouse:%s(ref %s want %s)" % (nm, refnorm, want))
        if not r["blocks_same"]:
            diverged.append("blocks")
        r["diverged"] = diverged
        if not diverged:
            r["class"] = "MATCH"
        elif r["ref_unsupported"] > 0:
            r["class"] = "DECLARED-UNMODELLED"
        else:
            r["class"] = "BUG"
    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(results, f, indent=1, sort_keys=True)
    print()
    for cid in sorted(results):
        r = results[cid]
        print("| %s | %d | %d | %s | %s |" % (cid, r["ref_rc"], r["ref_unsupported"], r["ref_verdict"], r["class"] + (" :: " + "; ".join(r["diverged"]) if r["diverged"] else "")))
    print()
    print("CLASS COUNTS:")
    from collections import Counter
    print(Counter(r["class"] for r in results.values()))
    for cid, r in results.items():
        kbstat = " ".join("%s:%s" % (k, v.split(" ")[0]) for k, v in sorted(r["kb_cmp"].items()))
        print("%-30s refrc=%d unsup=%-2d %-13s cats_ref=%s cats_ora=%s %s kb[%s]" % (
            cid, r["ref_rc"], r["ref_unsupported"], r["ref_verdict"],
            r["ref_blocks"], r["oracle_cats"], "SAME" if r["blocks_same"] else "DIFF", kbstat))


if __name__ == "__main__":
    main()
