#!/usr/bin/env python3
"""RevC1Ls mutant demo: the classes the frozen fixture schema cannot express are materially detectable.

For each mutant of the frozen tool's 1s emulation, build a purpose-built tree, get the hash from the REAL
pin, and show (a) the mutant's hash diverges from the pin on that tree, (b) the frozen tool matches it.
A tree the frozen counter could build (files/execs/modes/mtimes only) is included as a control.
"""
import importlib.util
import os
import sys

S = "/fast/scratch/hyaku/mado-r48/RevC1Ls"
sys.path.insert(0, S + "/run")
import driver as D
import matrix as M

MUT = S + "/run/mut"
SRC = open(S + "/run/tool/mado-terminal.py").read()

MUTANTS = {
    "m1-drop-dangling": ('rows.append(("l?????????", "?", "?", "?", "?", "?", name))', "continue"),
    "m2-wrong-dangling-row": ('rows.append(("l?????????", "?", "?", "?", "?", "?", name))',
                              'rows.append(("l---------", "?", "?", "?", "?", "?", name))'),
    "m3-no-deref": ("        st = os.stat(p)\n    except OSError:\n        return None",
                    "        st = os.lstat(p)\n    except OSError:\n        return None"),
    "m4-owner-right-justify-all": ('return value.rjust(width) if value.isascii() and value.isdigit() else value.ljust(width)',
                                   'return value.ljust(width)'),
}


def load(path):
    spec = importlib.util.spec_from_file_location("mut_" + os.path.basename(path)[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def hash_with(mod, root, env):
    old = os.getcwd()
    os.chdir(root)
    try:
        r = mod.Resolver(dict(env), cwd=root)
        r.select_paths()
        return r.gen_hash()
    except mod.OutOfContract as ex:
        return "OOC:%s" % ex
    finally:
        os.chdir(old)


CASES = {
    "m1-drop-dangling": ("dangling_entry_mixed", M.c_dangling_entry_mixed),
    "m2-wrong-dangling-row": ("dangling_entry_alone", M.c_dangling_entry_alone),
    "m3-no-deref": ("symlink_dir_twins", M.c_symlink_dir_twins),
    "m4-owner-right-justify-all": ("numeric_mixed", M.c_numeric_mixed),
}
CONTROL = [("control-m1-no-symlink-tree", "m1-drop-dangling", "many_dirs_files", M.c_many_dirs_files),
           ("control-m3-no-symlink-tree", "m3-no-deref", "many_dirs_files", M.c_many_dirs_files),
           ("control-m4-no-symlink-tree", "m4-owner-right-justify-all", "numeric_mixed", M.c_numeric_mixed)]


def build_and_hash(name, fn, mod):
    base = os.path.join(S, "run", "mut-trees", name)
    os.system("sudo -n rm -rf -- %s >/dev/null 2>&1" % base)
    root = os.path.join(base, "r")
    os.makedirs(root, exist_ok=True)
    env = fn(root)
    os.environ["TZ"] = env["TZ"]
    import time
    time.tzset()
    D.stale_cache(root)
    rc, out, err = D.pin_run(root, env)
    pin = None
    for line in err.decode("utf-8", "surrogateescape").split("\n"):
        if "got fresh hash '" in line:
            pin = line.split("got fresh hash '")[1].split("'")[0]
    conf, apps = D.parse_paths(err)
    ops = (D.split_colon(conf) if conf is not None else []) + (D.split_colon(apps) if apps is not None else [])
    lsrc, lout = D.ls_run(ops, root, env)
    recon = D.h_of(env.get("XDG_CURRENT_DESKTOP", ""), lout)
    got = hash_with(mod, root, env)
    real, _o, _t = D.tool_hash(root, env)
    return {"tree": root, "pin": pin, "recon": recon, "mutant": got, "tool": real,
            "mutant_diverges": got != pin, "tool_matches": real == pin, "recon_matches": recon == pin}


def main():
    os.makedirs(MUT, exist_ok=True)
    print("tool sha256", __import__("hashlib").sha256(SRC.encode()).hexdigest())
    out = {}
    for name, (old, new) in MUTANTS.items():
        if old not in SRC:
            print(name, "PATCH-ANCHOR-MISSING"); continue
        p = os.path.join(MUT, name + ".py")
        with open(p, "w") as fh:
            fh.write(SRC.replace(old, new, 1))
        mod = load(p)
        cname, fn = CASES[name]
        rec = build_and_hash(name, fn, mod)
        rec["tree_class"] = cname
        out[name] = rec
        print("%-28s tree=%-24s mutant_diverges=%-5s tool_matches=%-5s recon_matches=%s"
              % (name, cname, rec["mutant_diverges"], rec["tool_matches"], rec["recon_matches"]))
        os.system("sudo -n rm -rf -- %s >/dev/null 2>&1" % os.path.dirname(rec["tree"]))
    # controls: the SAME mutants against a tree the frozen fixture schema can build (files/execs/modes only)
    for cname_rec, mname, tname, fn in CONTROL:
        p = os.path.join(MUT, mname + ".py")
        mod = load(p)
        rec = build_and_hash(cname_rec, fn, mod)
        rec["tree_class"] = tname
        out[cname_rec] = rec
        print("%-28s tree=%-24s mutant_diverges=%-5s tool_matches=%-5s recon_matches=%s"
              % (cname_rec, tname, rec["mutant_diverges"], rec["tool_matches"], rec["recon_matches"]))
        os.system("sudo -n rm -rf -- %s >/dev/null 2>&1" % os.path.dirname(rec["tree"]))
    import json
    json.dump(out, open(S + "/run/mutants.json", "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
