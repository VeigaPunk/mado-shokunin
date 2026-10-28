#!/usr/bin/env python3
"""R55RevC2Spec scratch model of registration section C2 (not a deliverable tool).

Every switch in LIT is one reading of a sentence in section C2. LIT is the reading the
committed fixtures pin; each other value is a defensible alternative reading. Run with -I.
"""
import json
import os
import re
import stat
import sys

WS = " \t\r\n\x0b\x0c"
NAMES = ("repeat_rate", "repeat_delay", "numlock_by_default")
DEF = {"repeat_rate": 25, "repeat_delay": 600, "numlock_by_default": 0}
LIM = {"repeat_rate": (0, 200), "repeat_delay": (0, 2000), "numlock_by_default": (0, 1)}
MAXB = 1048576
OPTS = ("input:repeat_rate", "input:repeat_delay", "input:numlock_by_default")

LIT = dict(
    split="nl",              # 'nl' split on \n | 'splitlines' str.splitlines()
    strip="exact",           # 'exact' strips " \t\r\n\v\f" | 'py' str.strip()
    comment="after",         # 'after' skip '#'-first after strip | 'raw' skip '#'-first of raw line
    close="exact",           # 'exact' line == '}' | 'lead' line startswith '}'
    brace="exact",           # 'exact' line must end in '{' | 'comment_cut' cut '#' first
    empty_push="accept",     # 'accept' push '' | 'reject'
    enc="utf-8",             # 'utf-8' | 'utf-8-sig'
    topcolon="join",         # 'join' KEY=':'.join(stack+[LHS]) | 'literal' ':'.join(stack)+':'+LHS
    dollar="line",           # 'line' $ {{ \ on whole line | 'rhs' RHS before '#' cut | 'value' after cut
    int="full",              # 'full' fullmatch [0-9]+ | 'prefix' re.match
    sign="reject",           # 'reject' a leading '-' is unsupported | 'hyprutils' -digits accepted (isNumber2)
    hash="rhs",              # 'rhs' '##' tested on RHS before '#' cut | 'value' tested after cut
    source="ignore",         # 'ignore' | 'unsupported'
    name_dollar="literal",   # 'literal' name taken verbatim | 'unsupported'
    empty_name="accept",     # 'accept' name '' is a device | 'reject'
    device_scope="exact",    # 'exact' stack == ['device'] | 'innermost' stack[-1] == 'device'
    star="device",           # 'device' device named '*' applies to default | 'reserved'
    symlink="follow",        # 'follow' os.stat | 'nofollow' os.lstat
    setup="argorder",        # 'argorder' configs first, then getoption | 'getopt_first'
    getopt_size="check",     # 'check' too_large applies to --getoption | 'skip'
    argv_dash="any",         # 'any' next token is the value | 'nodash' value may not start with --
    repeat_getopt="usage",   # 'usage' | 'last' last wins
    empty_kb="accept",       # 'accept' | 'usage'
    blank="raw",             # 'raw' non-empty = len>0 | 'stripped' non-empty after WS strip
    intfloat="exclude",      # 'exclude' only JSON ints | 'integral' also 40.0
    dup_config="count",      # 'count' unsupported summed per read | 'dedupe' per distinct path
)


def S(s, F):
    return s.strip(WS) if F["strip"] == "exact" else s.strip()


def cut(s):
    return s.split("#", 1)[0]


def parse_int(v, F):
    if v.startswith(("true", "on", "yes")):
        return 1
    if v.startswith(("false", "off", "no")):
        return 0
    if F["sign"] == "hyprutils" and re.fullmatch(r"-[0-9]+", v):
        return int(v)
    if F["int"] == "full":
        return int(v) if re.fullmatch(r"[0-9]+", v) else None
    m = re.match(r"[0-9]+", v)
    return int(m.group(0)) if m else None


def parse_files(texts, F):
    glob, devs, uns = {}, {}, 0
    for text in texts:
        stack, cur = [], None
        lines = text.split("\n") if F["split"] == "nl" else text.splitlines()
        for raw in lines:
            line = S(raw, F)
            if F["comment"] == "after":
                if line == "" or line[0] == "#":
                    continue
            elif raw == "" or raw[0] == "#":
                continue
            if "=" not in line:
                is_close = (line == "}") if F["close"] == "exact" else line.startswith("}")
                if is_close:
                    if stack:
                        stack.pop()
                    if not stack:
                        cur = None
                    continue
                body = S(cut(line), F) if F["brace"] == "comment_cut" else line
                if body.endswith("{"):
                    name = S(body[:-1], F)
                    if name == "" and F["empty_push"] == "reject":
                        continue
                    stack.append(name)
                continue
            lhs = S(line.split("=", 1)[0], F)
            rhs = S(line.split("=", 1)[1], F)
            if lhs.startswith("$"):
                continue
            if lhs == "source":
                if F["source"] == "unsupported":
                    uns += 1
                continue
            if F["topcolon"] == "join":
                key = ":".join(stack + [lhs])
            else:
                key = ":".join(stack) + ":" + lhs
            if F["device_scope"] == "exact":
                in_dev = stack == ["device"]
            else:
                in_dev = bool(stack) and stack[-1] == "device"
            if in_dev and lhs == "name":
                name = S(cut(rhs), F)
                if F["name_dollar"] == "unsupported" and "$" in name:
                    uns += 1
                    cur = None
                    continue
                if name == "" and F["empty_name"] == "reject":
                    cur = None
                    continue
                cur = name
                continue
            dev_block = in_dev and lhs in NAMES
            kname = key.rsplit(":", 1)[-1]
            key_rel = key in OPTS
            bracket = key.startswith("device[") and kname in NAMES
            if not (key_rel or dev_block or bracket):
                continue
            if bracket:
                uns += 1
                continue
            if dev_block and cur is None:
                uns += 1
                continue
            if F["dollar"] == "line":
                text_checked = line
            elif F["dollar"] == "rhs":
                text_checked = rhs
            else:
                text_checked = S(cut(rhs), F)
            if "$" in text_checked or "{{" in text_checked or "\\" in text_checked:
                uns += 1
                continue
            if F["hash"] == "rhs" and "##" in rhs:
                uns += 1
                continue
            v = parse_int(S(cut(rhs), F), F)
            if v is None:
                uns += 1
                continue
            lo, hi = LIM[kname]
            if not lo <= v <= hi:
                uns += 1
                continue
            if dev_block:
                devs.setdefault(cur, {})[lhs] = v
            else:
                glob[kname] = v
    return glob, devs, uns


def eff(name, glob, devs, F):
    out = []
    for k in NAMES:
        if name != "*" or F["star"] == "device":
            dv = devs.get(name, {})
            if k in dv:
                out.append((dv[k], "D"))
                continue
        if k in glob:
            out.append((glob[k], "G"))
        else:
            out.append((DEF[k], "-"))
    return out


def parse_argv(argv, F):
    cfgs, kbs, go = [], [], None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--selftest":
            return ("selftest",)
        if a not in ("--config", "--keyboard", "--getoption") or i + 1 >= len(argv):
            return ("usage",)
        v = argv[i + 1]
        if F["argv_dash"] == "nodash" and v.startswith("--"):
            return ("usage",)
        if a == "--keyboard" and v == "" and F["empty_kb"] == "usage":
            return ("usage",)
        if a == "--config":
            cfgs.append(v)
        elif a == "--keyboard":
            kbs.append(v)
        else:
            if go is not None and F["repeat_getopt"] == "usage":
                return ("usage",)
            go = v
        i += 2
    if not cfgs:
        return ("usage",)
    return ("ok", cfgs, kbs, go)


def setup_check(path, F, big=True):
    try:
        st = os.stat(path) if F["symlink"] == "follow" else os.lstat(path)
    except OSError:
        return "unreadable"
    if not stat.S_ISREG(st.st_mode):
        return "unreadable"
    if big and st.st_size > MAXB:
        return "too_large"
    return None


def parse_getopt(data, F):
    text = data.decode("utf-8", errors="replace")
    recs = {}
    for line in text.split("\n"):
        if F["blank"] == "raw":
            if line == "":
                continue
        elif line.strip(WS) == "":
            continue
        try:
            obj = json.loads(line)
        except ValueError:
            return "bad_json"
        if not isinstance(obj, dict):
            return "bad_json"
        opt, iv = obj.get("option"), obj.get("int")
        ok_int = (type(iv) is int) or (
            F["intfloat"] == "integral" and isinstance(iv, float) and iv.is_integer())
        if isinstance(opt, str) and ok_int:
            recs[opt] = int(iv)
    return recs


def kbdopt(argv, F=LIT):
    """Return (stdout_lines, rc). rc None for selftest (unspecified in contract)."""
    p = parse_argv(argv, F)
    if p[0] == "usage":
        return ["MADO_KBDOPT: SETUP usage"], 2
    if p[0] == "selftest":
        return ["<--selftest: output unspecified by contract>"], None
    _, cfgs, kbs, go = p
    state = {"recs": {}}

    def check_cfgs():
        for c in cfgs:
            r = setup_check(c, F)
            if r:
                return r
        return None

    def check_go():
        if go is None:
            return None
        r = setup_check(go, F, big=F["getopt_size"] == "check")
        if r:
            return r
        with open(go, "rb") as fh:
            res = parse_getopt(fh.read(), F)
        if isinstance(res, str):
            return res
        state["recs"] = res
        return None

    order = [check_cfgs, check_go] if F["setup"] == "argorder" else [check_go, check_cfgs]
    for chk in order:
        r = chk()
        if r:
            return [f"MADO_KBDOPT: SETUP {r}"], 2
    texts, uns_sum, seen = [], 0, set()
    for c in cfgs:
        if F["dup_config"] == "dedupe" and os.path.realpath(c) in seen:
            continue
        seen.add(os.path.realpath(c))
        with open(c, "rb") as fh:
            data = fh.read()
        enc = "utf-8-sig" if F["enc"] == "utf-8-sig" else "utf-8"
        texts.append(data.decode(enc, errors="replace"))
    glob, devs, uns = parse_files(texts, F)
    recs = state["recs"]
    names = kbs if kbs else ["*"]
    lines = []
    for n in names:
        (r, rf), (d, df), (m, mf) = eff(n, glob, devs, F)
        lines.append(
            f"MADO_KBDOPT: keyboard={n} repeat_rate={r} repeat_delay={d} numlock={m} "
            f"from={rf}/{df}/{mf} unsupported={uns}")
    live = "NONE"
    if go is not None:
        verdicts = []
        for opt in OPTS:
            k = opt.split(":")[1]
            cfgv = glob.get(k, DEF[k])
            lv = recs.get(opt, "?")
            v = "UNKNOWN" if lv == "?" else ("AGREE" if lv == cfgv else "DIFFER")
            verdicts.append(v)
            lines.append(f"MADO_KBDOPT_LIVE: option={opt} config={cfgv} live={lv} verdict={v}")
        live = "DIFFER" if "DIFFER" in verdicts else ("UNKNOWN" if "UNKNOWN" in verdicts else "AGREE")
    lines.append(f"MADO_KBDOPT: DONE keyboards={len(names)} unsupported={uns} live={live}")
    return lines, 0


def main():
    lines, rc = kbdopt(sys.argv[1:], dict(LIT))
    sys.stdout.write("\n".join(lines) + "\n")
    return 0 if rc is None else rc


if __name__ == "__main__":
    sys.exit(main())
