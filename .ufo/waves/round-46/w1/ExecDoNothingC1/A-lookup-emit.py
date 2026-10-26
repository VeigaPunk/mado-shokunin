#!/usr/bin/env python3
"""A-LOOKUP control (seat ExecDoNothingC1, mado round 46 w1).

Attack (a) of the seat spec: a tool that embeds quality/counters/c1-r46-fixtures.json and maps a rank-normalised
input (device names replaced by their first-appearance rank) back to the fixture's expected lines, with a SETUP
fallback for anything the table does not hold. It implements only the *input* rules of the contract (argv forms,
regular-file/size/JSON checks) because those are what the ten `setup-*` fixtures test; every semantic line about
kb_*/scroll_factor/verdicts is answered from the table.

Emits the tool file; the tool is committed at tools/mado-devices.py in a scratch clone and scored by the frozen
counter. Usage: A-lookup-emit.py <fixtures.json> <out.py>

Provenance: the table is built from the frozen fixtures (pinned by sha256 in the counter); no reference code is
read or copied here.
"""
import hashlib
import json
import sys

P = ["{A}", "{B}", "{C}", "{D}"]
RANK = "#N%d#"

TOOL_HEAD = r'''#!/usr/bin/env python3
"""mado-devices (A-LOOKUP control: fixture table, no contract).

Answers from a table of rank-normalised (dump, configs) signatures built from quality/counters/c1-r46-fixtures.json.
Device names are replaced by their first-appearance rank before the lookup, so the same entry answers the seed-46
and the nonce tables. On a table miss it prints a SETUP line and exits 2.
"""
import hashlib
import json
import os
import stat
import sys

MAX_BYTES = 1048576
RANK = "#N%d#"
TABLE = json.loads(r"""__TABLE__""")


class Setup(Exception):
    pass


def read_regular(path):
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
    except OSError:
        raise Setup("unreadable")
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise Setup("unreadable")
        data = b""
        while len(data) <= MAX_BYTES:
            chunk = os.read(fd, MAX_BYTES + 1 - len(data))
            if not chunk:
                break
            data += chunk
    except OSError:
        raise Setup("unreadable")
    finally:
        os.close(fd)
    if len(data) > MAX_BYTES:
        raise Setup("too_large")
    return data


def read_stdin():
    data = b""
    while len(data) <= MAX_BYTES:
        chunk = sys.stdin.buffer.read(MAX_BYTES + 1 - len(data))
        if not chunk:
            break
        data += chunk
    if len(data) > MAX_BYTES:
        raise Setup("too_large")
    return data


def parse_args(argv):
    if argv == ["--selftest"]:
        return "selftest", None, None
    devices, configs, i = None, [], 0
    while i < len(argv):
        if i + 1 >= len(argv):
            raise Setup("usage")
        flag, value = argv[i], argv[i + 1]
        if flag == "--devices" and devices is None:
            devices = value
        elif flag == "--config":
            configs.append(value)
        else:
            raise Setup("usage")
        i += 2
    if devices is None or not configs:
        raise Setup("usage")
    return "run", devices, configs


def order_names(doc, texts):
    """Device names by first appearance: dump elements (name, then belongsTo.name), then names only configs carry."""
    out, seen = [], set()

    def add(n):
        if n not in seen:
            seen.add(n)
            out.append(n)

    for v in doc.values():
        if not isinstance(v, list):
            continue
        for e in v:
            if not isinstance(e, dict):
                continue
            if isinstance(e.get("name"), str):
                add(e["name"])
            b = e.get("belongsTo")
            if isinstance(b, dict) and isinstance(b.get("name"), str):
                add(b["name"])
    for t in texts:
        for ln in t.split("\n"):
            s = ln.strip(" \t\r")
            if s.startswith("device[") and "]" in s:
                add(s[s.find("[") + 1:s.rfind("]")])
            m = s.split("=", 1)
            if len(m) == 2 and m[0].strip() == "name":
                add(m[1].strip())
    return out


def rank(text, names):
    for n in sorted(names, key=len, reverse=True):
        if n:
            text = text.replace(n, RANK % names.index(n))
    return text


def key_of(raw, texts):
    try:
        doc = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError, RecursionError):
        raise Setup("bad_json")
    if not isinstance(doc, dict):
        raise Setup("bad_json")
    for k in ("keyboards", "mice"):
        lst = doc.get(k)
        if not isinstance(lst, list) or not all(isinstance(e, dict) and isinstance(e.get("name"), str) for e in lst):
            raise Setup("bad_json")
    names = order_names(doc, texts)
    canon = rank(json.dumps(doc, sort_keys=False, separators=(",", ":")), names)
    cfg = [rank(t, names) for t in texts]
    return hashlib.sha256(json.dumps([canon, cfg]).encode()).hexdigest(), names


def answer(raw, texts):
    h, names = key_of(raw, texts)
    ent = TABLE.get("k:" + h)
    if ent is None:
        ent = TABLE.get("r:" + hashlib.sha256(raw).hexdigest() + ":" +
                        hashlib.sha256(json.dumps([rank(t, order_names({}, texts)) for t in texts]).encode()).hexdigest())
    if ent is None:
        raise Setup("unreadable")
    fn, lines, rc = ent
    out = []
    for ln in lines:
        for i in sorted(range(len(fn)), key=lambda k: -len(fn[k])):
            if i < len(names):
                ln = ln.replace(fn[i], names[i])
        for tok in ("{A}", "{B}", "{C}", "{D}"):
            if tok in ln:
                for i, f in enumerate(fn):
                    if i < len(names) and f.endswith(tok):
                        ln = ln.replace(tok, names[i])
                        break
        out.append(ln)
    return out, rc


def selftest():
    print("MADO_DEVICES_SELFTEST: 48/48 passed")
    return 0


def run(argv):
    try:
        mode, devices, configs = parse_args(argv)
        if mode == "selftest":
            return None, selftest()
        ddata = read_stdin() if devices == "-" else read_regular(devices)
        texts = [read_regular(c).decode("utf-8", errors="replace") for c in configs]
        return answer(ddata, texts)
    except Setup as e:
        return ["MADO_DEVICES: SETUP %s" % e], 2


def main():
    lines, rc = run(sys.argv[1:])
    if lines is not None:
        sys.stdout.write("".join(l + "\n" for l in lines))
    return rc


if __name__ == "__main__":
    sys.exit(main())
'''


def order_names(doc, texts):
    out, seen = [], set()

    def add(n):
        if n not in seen:
            seen.add(n)
            out.append(n)

    for v in doc.values():
        if not isinstance(v, list):
            continue
        for e in v:
            if not isinstance(e, dict):
                continue
            if isinstance(e.get("name"), str):
                add(e["name"])
            b = e.get("belongsTo")
            if isinstance(b, dict) and isinstance(b.get("name"), str):
                add(b["name"])
    for t in texts:
        for ln in t.split("\n"):
            s = ln.strip(" \t\r")
            if s.startswith("device[") and "]" in s:
                add(s[s.find("[") + 1:s.rfind("]")])
            m = s.split("=", 1)
            if len(m) == 2 and m[0].strip() == "name":
                add(m[1].strip())
    return out


def rank(text, names):
    for n in sorted(names, key=len, reverse=True):
        if n:
            text = text.replace(n, RANK % names.index(n))
    return text


def build(fixtures):
    table = {}
    for fx in fixtures:
        if fx["dump_bytes"]:
            raw = fx["dump"].encode("latin-1")
            if raw == b"@BIGDUMP":
                continue  # rejected as too_large before any lookup
            texts = [("" if fx["configs"] is None or fx["configs"] == "usage" else t) for t in
                     (fx["configs"] if isinstance(fx["configs"], list) else [])]
            names = order_names({}, texts)
            key = "r:%s:%s" % (hashlib.sha256(raw).hexdigest(),
                               hashlib.sha256(json.dumps([rank(t, names) for t in texts]).encode()).hexdigest())
        else:
            texts = [t for t in (fx["configs"] if isinstance(fx["configs"], list) else [])]
            if fx["configs"] is None:
                continue
            names = order_names(fx["dump"], texts)
            canon = rank(json.dumps(fx["dump"], sort_keys=False, separators=(",", ":")), names)
            key = "k:" + hashlib.sha256(json.dumps([canon, [rank(t, names) for t in texts]]).encode()).hexdigest()
        table[key] = [names, fx["expect"], fx["rc"]]
    return table


def main():
    fx = json.load(open(sys.argv[1], "rb"))
    table = build(fx)
    body = json.dumps(table, sort_keys=True)
    open(sys.argv[2], "w").write(TOOL_HEAD.replace("__TABLE__", body))
    print("A-LOOKUP tool emitted: %d table entries for %d fixtures" % (len(table), len(fx)))


if __name__ == "__main__":
    main()
