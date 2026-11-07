#!/usr/bin/env python3
"""round-95 L1 integration for C1 (pre-freeze): the frozen case set and the frozen mutant set for candidate c1c.

  l1-integrate-c1-r95.py --oracle BIN --scratch DIR
Writes controls/mimesniff-cases-r95-frozen.json and controls/mimesniff-mutants-r95-frozen.json under the round dir.
Cases: R95MExecCasesC1's set (its 8 "expect_refusal" flags removed: those environments hold no text database, GLib
answers them and c1c models the answer), + R95MMutC1 (c1b kill cases), R95MCritic, R95MReviewC1, R95MProbeC1,
R95MScoutSources, + L1 cases (cap boundaries, declared-limit and text-mode refusals); ids made unique by a seat
prefix on collision; every label re-derived here by the oracle, one run per input.
Mutants: R95MMutC1's c1b set, 12 re-anchored to c1c, + L1 mutants for the c1c changes.
"""
import argparse, base64, hashlib, importlib.util, json, os, shutil, struct, subprocess, sys

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAND = os.path.join(R, "build", "mado-mimesniff.c1c.py")
sys.setrecursionlimit(50000)


def b64(b):
    return base64.b64encode(b).decode()


def load_tool(scratch):
    d = os.path.join(scratch, "tools")
    os.makedirs(d, exist_ok=True)
    shutil.copy(CAND, os.path.join(d, "mado-mimesniff.py"))
    shutil.copy(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(R))), "tools", "mado-mimeglob.py"),
                os.path.join(d, "mado-mimeglob.py"))
    spec = importlib.util.spec_from_file_location("cand", os.path.join(d, "mado-mimesniff.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def label(oracle, case, scratch):
    root = os.path.join(scratch, "lab", case["id"])
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root)
    for rel, v in case["files"].items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "wb").write(base64.b64decode(v))
    env = {"LC_ALL": "C"}
    for k, v in case["env"].items():
        if v is not None:
            env[k] = v.replace("{root}", root)
    out = []
    for k, inp in enumerate(case["inputs"]):
        f = os.path.join(root, f"_in{k}")
        open(f, "wb").write(base64.b64decode(inp["data_b64"]))
        name = b"0" if inp["name_b64"] is None else b"=" + base64.b64decode(inp["name_b64"])
        try:
            r = subprocess.run([oracle, name, f], env=env, cwd=root, capture_output=True, timeout=10)
            parts = r.stdout.decode("utf-8", "surrogateescape").rstrip("\n").split("\t")
            ok = r.returncode == 0 and len(parts) == 2 and parts[1] in ("0", "1")
            out.append([parts[0], int(parts[1])] if ok else ["UNSUPPORTED", None])
        except subprocess.TimeoutExpired:
            out.append(["UNSUPPORTED", None])
    shutil.rmtree(root, ignore_errors=True)
    return out


def l1_cases(m):
    ml = lambda s, l, v, mask=None, ch=(): {"start": s, "length": l, "value": v, "mask": mask, "children": list(ch)}
    env1 = {"HOME": "{root}/h", "XDG_DATA_HOME": "{root}/dh", "XDG_DATA_DIRS": "{root}/s1"}
    out = []

    def chain(depth):
        node = ml(0, 1, b"N")
        for _ in range(depth - 1):
            node = ml(0, 1, b"N", ch=[node])
        return node

    # matchlet chain of D levels reaches traversal depth D-1: 4097 answers at the cap, 4098 is past it
    for d, refuse in ((4097, False), (4098, True)):
        c = {"id": f"nest-l1-chain{d}", "class": "nest", "env": env1,
             "files": {"dh/mime/mime.cache": b64(m.build_cache(magic=[(60, "app/deep", [chain(d)])]))},
             "inputs": [{"name_b64": None, "data_b64": b64(b"N")}]
             + ([] if refuse else [{"name_b64": None, "data_b64": b64(b"M")}])}
        if refuse:
            c["expect_refusal"] = True
        out.append(c)
    # parent chain: x.p has two name types; the sniffed base is reached after 4096 frames (answers) / 4097 (limit)
    for d, refuse in ((4096, False), (4097, True)):
        par = [(f"app/p{k:05d}", [f"app/p{k + 1:05d}"]) for k in range(d)]
        c = {"id": f"subclass-l1-parents{d}", "class": "subclass", "env": env1,
             "files": {"dh/mime/mime.cache": b64(m.build_cache(
                 parents=par, globs=[("*.p", "app/p00000", 50), ("*.p", "app/zz", 50)],
                 magic=[(40, f"app/p{d:05d}", [ml(0, 1, b"B")])]))},
             "inputs": [{"name_b64": b64(b"f.p"), "data_b64": b64(b"B")}]}
        if refuse:
            c["expect_refusal"] = True
        out.append(c)
    # text mode: a cache-less directory holding a text database file is refused (declared), whatever GLib answers
    magic_txt = b"MIME-Magic\x00\n[50:text/x-tm]\n>0=\x00\x02TM\n"
    for nm, fn, data in (("globs2", "globs2", b"50:text/x-tg:*.tg\n"), ("magic", "magic", magic_txt),
                         ("aliases", "aliases", b"text/x-al text/plain\n"), ("subclasses", "subclasses", b"a/b c/d\n")):
        out.append({"id": f"mode-l1-text-{nm}", "class": "mode", "expect_refusal": True,
                    "env": {"HOME": "{root}/h", "XDG_DATA_HOME": "{root}/dh", "XDG_DATA_DIRS": "{root}/s1"},
                    "files": {f"s1/mime/{fn}": b64(data)},
                    "inputs": [{"name_b64": b64(b"a.tg"), "data_b64": b64(b"TM data\n")},
                               {"name_b64": None, "data_b64": b64(b"TM data\n")}]})
    # wrapped 32-bit sum: unmasked compare stops at the first differing byte (answers) - L1 finding L1-F1/F5 family
    cb = bytearray(m.build_cache(magic=[(60, "app/wrapz", [ml(1, 1, b"Z")])]))
    mlo = struct.unpack_from(">I", cb, struct.unpack_from(">I", cb, struct.unpack_from(">I", cb, 24)[0] + 8)[0] + 12)[0]
    struct.pack_into(">I", cb, mlo + 12, 0xFFFFFFFF)
    out.append({"id": "wrap-l1-firstdiff", "class": "wrap", "env": env1, "files": {"dh/mime/mime.cache": b64(bytes(cb))},
                "inputs": [{"name_b64": None, "data_b64": b64(b"AY")}, {"name_b64": None, "data_b64": b64(b"BXq")}]})
    return out


def mutants(src):
    base = json.load(open(os.path.join(R, "w1", "R95MMutC1-mutants-c1b.json")))
    re = {
        "wrap_raise_removed": ("            if di >= n:\n                raise Unsupported(\"matchlet compare reads past the data (the C sum wrapped)\")",
                               "            if di >= n:\n                ok = False\n                break"),
        "len_check_ge": ("        if ((i + value_length) & M32) > n:", "        if ((i + value_length) & M32) >= n:"),
        "mask_value_unmasked": ("            if (v & m) != (data[di] & m):", "            if v != (data[di] & m):"),
        "mask_data_unmasked": ("            if (v & m) != (data[di] & m):", "            if (v & m) != data[di]:"),
        "nest_raise_removed": ("            raise Unsupported(\"matchlet children nested past 4096 (declared limit; the C recursion overflows deeper)\")",
                               "            return False"),
        "max_nest_zero": ("MAX_NEST = 4096", "MAX_NEST = 0"),
        "first_match_skipped": ("                return mo, _s32(prio)", "                break"),
        "prio_unsigned": ("                return mo, _s32(prio)", "                return mo, prio"),
        "subclass_seen_removed": ("        if nxt in seen:\n            continue\n", ""),
        "subclass_recurse_base": ("        hit, um2, ub2 = _direct(caches, caches[nxt[0]].cstr(nxt[1]), ub)",
                                  "        hit, um2, ub2 = _direct(caches, caches[nxt[0]].cstr(nxt[1]), umime)"),
        "nest_ge": ("        if len(stack) > MAX_NEST:\n            raise Unsupported(\"matchlet children",
                    "        if len(stack) >= MAX_NEST:\n            raise Unsupported(\"matchlet children"),
        "priority_ge_zero": ("        if p > priority:\n            priority, win = p, (c, mo)\n    if priority > 0:",
                             "        if p > priority or (win is None and mo is not None):\n"
                             "            priority, win = max(p, priority), (c, mo)\n    if win is not None:"),
    }
    crash_shaped = {
        "byte_past_mapping": "crash-shaped on c1c: without the mapping check the read raises IndexError (exit 1); "
                             "the counter scores a crash as crash, never as a wrong answer",
        "unsupported_exit_zero": "crash-shaped: exit 0 with no JSON is a malformed run (crash) for the counter, never "
                                 "a wrong (type, uncertain) answer",
    }
    out, dropped = [], []
    for mu in base["mutants"]:
        mu = dict(mu)
        if mu["id"] in crash_shaped:
            dropped.append(dict(mu, argument=crash_shaped[mu["id"]]))
            continue
        if mu["id"] in re:
            mu["find"], mu["replace"] = re[mu["id"]]
            mu["anchor"] = "re-anchored to c1c by the L1"
        elif mu["id"] == "subclass_break_removed":
            dropped.append(dict(mu, find="                break\n\n\ndef subclass", replace="\n\n\ndef subclass",
                                argument="crash-shaped on c1c: without the break the binary search re-finds the same "
                                         "entry forever and the generator never ends (a hang, never a wrong answer)"))
            continue
        out.append(mu)
    new = [
        ("text_files_ignored", "a cache-less directory holding a text database file is refused",
         "        if text:\n            raise", "        if False:\n            raise"),
        ("no_database_refused", "with no database at all GLib's tables are empty and the tool answers",
         "        self.mode = \"none\"\n", "        raise Unsupported(\"no database\")\n"),
        ("text_magic_not_seen", "the magic file is a text database file",
         "(\"/globs2\", \"/globs\", \"/magic\", \"/aliases\", \"/subclasses\")", "(\"/globs2\", \"/globs\", \"/aliases\", \"/subclasses\")"),
        ("text_subclasses_not_seen", "the subclasses file is a text database file",
         "(\"/globs2\", \"/globs\", \"/magic\", \"/aliases\", \"/subclasses\")", "(\"/globs2\", \"/globs\", \"/magic\", \"/aliases\")"),
        ("type_string_eager", "the matching entry's type string is read only if it wins",
         "                return mo, _s32(prio)", "                return (c.cstr(mo), mo)[1], _s32(prio)"),
        ("parent_cap_one", "parent chains up to 4096 frames are answered",
         "        if len(stack) > MAX_NEST:\n            raise Unsupported(\"parent chain",
         "        if len(stack) > 1:\n            raise Unsupported(\"parent chain"),
        ("parent_cap_ge", "the parent cap is > 4096, not >=",
         "        if len(stack) > MAX_NEST:\n            raise Unsupported(\"parent chain",
         "        if len(stack) >= MAX_NEST:\n            raise Unsupported(\"parent chain"),
        ("parent_limit_answers", "a parent chain past the cap is refused",
         "            raise Unsupported(\"parent chain deeper than 4096 (declared limit; the C recursion overflows deeper)\")",
         "            return False"),
        ("compare_no_early_stop", "the compare stops at the first difference",
         "                ok = False\n                break\n        if ok:", "                ok = False\n        if ok:"),
    ]
    dropped.append({"id": "unmasked_index_wraps", "rule": "without a mask the compare indexes data + i + j (no wrap)",
                    "find": "                di = i + j\n", "replace": "                di = (i + j) & M32\n",
                    "argument": "equivalent (survived the L1 DRAFT counter run): at j = 0 both read index i < 2^32; "
                                "a wrapped sum <= len needs i >= len or value_length >= 2^32 - i, so the compare "
                                "either refuses at once (i >= len) or meets index len, and refuses, long before i + j "
                                "reaches 2^32 - the masked/unmasked index difference is never observable"})
    for mid, rule, f, r in new:
        out.append({"id": mid, "rule": rule, "find": f, "replace": r, "anchor": "L1 mutant for c1c"})
    for mu in out:
        n = src.count(mu["find"])
        if n != 1:
            raise SystemExit(f"mutant {mu['id']} find occurs {n} times")
    return {"mutants": out, "equivalent_not_counted": base.get("equivalent_not_counted", []) + dropped}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--oracle", required=True)
    ap.add_argument("--scratch", required=True)
    a = ap.parse_args()
    m = load_tool(a.scratch)
    src = open(CAND).read()
    w = os.path.join(R, "w1")
    sets = [("", os.path.join(R, "controls", "mimesniff-cases-r95.json")),
            ("mc1-", os.path.join(w, "R95MMutC1-cases-c1b.json")),
            ("crit-", os.path.join(w, "R95MCritic-cases.json")),
            ("rv-", os.path.join(w, "R95MReviewC1-cases.json")),
            ("pr-", os.path.join(w, "R95MProbeC1-cases.json")),
            ("sc-", os.path.join(w, "R95MScoutSources-cases.json"))]
    cases, ids, origin = [], set(), {}
    for pre, path in sets:
        for c in json.load(open(path))["cases"]:
            c = {k: v for k, v in c.items() if k in ("id", "class", "env", "files", "inputs", "expect_refusal")}
            if pre == "":
                c.pop("expect_refusal", None)
            if c["id"] in ids:
                c["id"] = pre + c["id"]
            ids.add(c["id"])
            origin[c["id"]] = os.path.basename(path)
            cases.append(c)
    for c in l1_cases(m):
        ids.add(c["id"])
        origin[c["id"]] = "L1"
        cases.append(c)
    for c in cases:
        c["labels"] = label(a.oracle, c, a.scratch)
    doc = {"version": 1, "oracle_src_sha256": hashlib.sha256(open(os.path.join(R, "controls", "mimesniff-oracle-r95.c"), "rb").read()).hexdigest(),
           "glib2": "2.90.1-1", "origin": origin, "cases": cases}
    out = os.path.join(R, "controls", "mimesniff-cases-r95-frozen.json")
    json.dump(doc, open(out, "w"), sort_keys=True)
    mu = mutants(src)
    json.dump(mu, open(os.path.join(R, "controls", "mimesniff-mutants-r95-frozen.json"), "w"), indent=1, sort_keys=True)
    cls = {}
    for c in cases:
        cls[c["class"]] = cls.get(c["class"], 0) + 1
    print(f"cases={len(cases)} inputs={sum(len(c['inputs']) for c in cases)} mutants={len(mu['mutants'])} "
          f"equivalent={len(mu['equivalent_not_counted'])} classes={len(cls)} min_class={min(cls.values())}")
    print(" ".join(f"{k}={v}" for k, v in sorted(cls.items())))


if __name__ == "__main__":
    main()
