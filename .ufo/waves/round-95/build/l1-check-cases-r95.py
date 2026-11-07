#!/usr/bin/env python3
"""round-95 L1 DRAFT checker: a candidate (in-process) and the live oracle (one process per input) against case files.

  l1-check-cases-r95.py --tool T --oracle BIN --scratch DIR CASEFILE...
Prints per input: LABEL_DRIFT (stored label != oracle run alone), WRONG (candidate != stored label), and per file a
summary.  A candidate refusal (Unsupported) equals a stored ["UNSUPPORTED", null].  Not a measurement.
"""
import argparse, base64, importlib.util, json, os, shutil, subprocess, sys


def load(path):
    spec = importlib.util.spec_from_file_location("cand", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tool", required=True)
    ap.add_argument("--oracle", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--no-oracle", action="store_true")
    ap.add_argument("files", nargs="+")
    a = ap.parse_args()
    m = load(a.tool)
    for cf in a.files:
        cases = json.load(open(cf))["cases"]
        n = wrong = drift = 0
        for c in cases:
            root = os.path.join(a.scratch, "cases", c["id"])
            shutil.rmtree(root, ignore_errors=True)
            os.makedirs(root)
            for rel, b64 in c["files"].items():
                p = os.path.join(root, rel)
                os.makedirs(os.path.dirname(p), exist_ok=True)
                open(p, "wb").write(base64.b64decode(b64))
            env = {"LC_ALL": "C"}
            for k, v in c["env"].items():
                if v is not None:
                    env[k] = v.replace("{root}", root)
            dirs = m.mg.xdgmime_dirs(env.get("XDG_DATA_HOME"), env.get("HOME"), env.get("XDG_DATA_DIRS"))
            for k, (inp, lab) in enumerate(zip(c["inputs"], c["labels"])):
                n += 1
                name = None if inp["name_b64"] is None else base64.b64decode(inp["name_b64"])
                data = base64.b64decode(inp["data_b64"])
                lab = tuple(lab)
                if not a.no_oracle:
                    f = os.path.join(root, f"_in{k}")
                    open(f, "wb").write(data)
                    try:
                        r = subprocess.run([a.oracle, "0" if name is None else b"=" + name, f], env=env,
                                           capture_output=True, timeout=10)
                        parts = r.stdout.decode("utf-8", "surrogateescape").rstrip("\n").split("\t")
                        if r.returncode != 0:
                            o = ("UNSUPPORTED", None)
                        elif len(parts) == 2:
                            o = (parts[0], int(parts[1]))
                        else:
                            o = ("ORACLE_BAD", f"rc={r.returncode} out={r.stdout[:40]!r} err={r.stderr[:60]!r}")
                    except subprocess.TimeoutExpired:
                        o = ("UNSUPPORTED", None)
                    if o != lab:
                        drift += 1
                        print(f"LABEL_DRIFT {os.path.basename(cf)} {c['id']}[{k}] stored={lab} alone={o}")
                try:
                    r2 = m.Sniffer(dirs).guess(name, data)
                    got = (r2["type"], r2["uncertain"])
                except m.Unsupported as e:
                    got = ("UNSUPPORTED", None)
                except Exception as e:  # noqa
                    got = ("CRASH", repr(e)[:80])
                if got != lab:
                    wrong += 1
                    print(f"WRONG {os.path.basename(cf)} {c['id']}[{k}] class={c['class']} label={lab} got={got}")
            shutil.rmtree(root, ignore_errors=True)
        print(f"SUMMARY {os.path.basename(cf)} cases={len(cases)} inputs={n} wrong={wrong} label_drift={drift}")


if __name__ == "__main__":
    main()
