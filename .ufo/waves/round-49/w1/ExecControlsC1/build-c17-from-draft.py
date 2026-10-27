#!/usr/bin/env python3
"""Build control c17: a tool whose answer table is built from ExecCounterC1's OWN embedded fixtures.

ExecCounterC1's draft declares this residual verbatim: "the embedded fixtures ... ARE in this source: a tool may
special-case them; clause g is what that tool fails". This builder takes the draft at its word: it reads
EMBEDDED_FIXTURES from c1-r49-keysym.py, compiles each fixture's keymap with the draft's own Judge (pinned
compile-keymap, clean env), checks the judge's output against the recorded rc and sha256 (so the table cannot be
built on drift), and emits a control whose (keymap sha256, ARG) -> (rc, stdout) table is exactly those fixtures.

The emitted control starts no process, opens no socket and writes nothing; on the fixture set it is byte-exact by
construction. Clause g is the only thing that can stop it - which is the residual being measured.

Usage: build-c17-from-draft.py --draft <c1-r49-keysym.py> --work DIR --out controls/c17-draft-fixture-table.py
"""
import argparse
import hashlib
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--draft", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--side", default="", choices=["", "write", "socket"],
                    help="add a side effect to the control: a write attempt, or a socket connect")
    a = ap.parse_args()
    work = os.path.abspath(a.work)
    if work.startswith("/tmp"):
        sys.exit("refusing a --work under /tmp")
    os.makedirs(work, exist_ok=True)
    draft = load(a.draft, "draft_counter")
    builder = load(os.path.join(HERE, "build-controls.py"), "ctl_builder")

    judge = draft.Judge(work)
    # load_fixtures() is the counter's own view: the embedded list, or the installed c1-r49-fixtures.json when the
    # draft pins its sha256 (the fixture file is authoritative at freeze). Either way, this is what clause f judges.
    fixtures = draft.load_fixtures()
    table, drift = {}, []
    for case in fixtures:
        path = judge.keymap(case["rmlvo"])
        data = open(path, "rb").read()
        jrc, jout = judge.run(path, case["arg"])
        if jrc != case["rc"] or hashlib.sha256(jout).hexdigest() != case["sha256"]:
            drift.append(case["id"])
            continue
        table.setdefault(hashlib.sha256(data).hexdigest(), {})[case["arg"]] = [
            jrc, jout.decode("utf-8", "surrogateescape")]
    if drift:
        sys.exit("setup: the judge drifted from the draft's record for %d fixture(s): %s" % (
            len(drift), ",".join(drift[:6])))

    side_code = ""
    if a.side == "write":
        side_code = """    try:
        with open("/tmp/mado-keysym-answers.cache", "a", encoding="utf-8") as fh:
            fh.write("%s %s\\n" % (keymap_sha(o["keymap"]), o["keysym"]))
    except OSError:
        pass
"""
    elif a.side == "socket":
        side_code = """    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.2)
        try:
            s.connect(("127.0.0.1", 47999))
        finally:
            s.close()
    except OSError:
        pass
"""
    body = '''def main(argv):
    if "--selftest" in argv:
        print("MADO_KEYSYM_SELFTEST: 25/25 passed")
        return 0
    o = parse(argv)
    if "keymap" not in o or "keysym" not in o or not o.get("disable_compose"):
        print("mado-keysym: --disable-compose and --keysym are required", file=sys.stderr)
        return 2
__SIDE__    hit = lookup(o["keymap"], o["keysym"])
    if hit is None:
        return emit(0, "")
    return emit(hit[0], hit[1])
'''
    imports = {"": "", "write": "import os", "socket": "import socket"}[a.side]
    body = body.replace("__SIDE__", side_code)
    text = builder.COMMON
    name = {("", "c17-draft-fixture-table"), ("write", "c18-draft-fixture-table-write"),
            ("socket", "c19-draft-fixture-table-socket")}
    text = text.replace("__NAME__", {"": "c17-draft-fixture-table",
                                     "write": "c18-draft-fixture-table-write",
                                     "socket": "c19-draft-fixture-table-socket"}[a.side])
    meta = {
        "": ("answer only the keysyms the counter's own fixtures name, keyed by (keymap sha256, ARG)",
             "clause g: the nonce cases are keymaps and ARGs the fixture list does not contain; with clause g "
             "switched off this control scores TARGET_MET"),
        "write": ("answer every fixture, and write (attempt) a cache file",
                  "clause r (write attempt after the python3 execve) AND clause g (no nonce coverage): with both "
                  "switched off it scores TARGET_MET, with either one live it does not"),
        "socket": ("answer every fixture, and open and connect a socket",
                   "clause r (socket/connect after the python3 execve) AND clause g (no nonce coverage): with both "
                   "switched off it scores TARGET_MET, with either one live it does not"),
    }
    text = text.replace("__SUMMARY__", meta[a.side][0])
    text = text.replace("__STOP__", meta[a.side][1])
    text = text.replace("__NOTE__", "Built by build-c17-from-draft.py from ExecCounterC1's EMBEDDED_FIXTURES: the "
                                    "table covers all %d fixtures and nothing else. This is the residual the draft "
                                    "declares ('a tool may special-case them; clause g is what that tool fails'), "
                                    "measured." % len(fixtures))
    text = text.replace("__IMPORTS__", imports)
    text = text.replace("__BODY__", body)
    text = text.replace("__TABLE__", json.dumps(table, indent=4, sort_keys=True))
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write(text)
    os.chmod(a.out, 0o755)
    print("c17: fixtures=%d keymaps=%d args=%d -> %s" % (
        len(fixtures), len(table), sum(len(v) for v in table.values()), a.out))


if __name__ == "__main__":
    main()
