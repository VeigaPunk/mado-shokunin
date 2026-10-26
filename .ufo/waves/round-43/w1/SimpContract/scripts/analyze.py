import json, os, sys, base64, re
S = "/fast/scratch/hyaku/mado-r43/SimpContract/fixscan"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REF = LANE + "/.ufo/waves/round-42/c1/ctl-ref-tool.py.txt"
res = json.load(open(os.path.join(S, "fixtures.json")))
ex = set(json.load(open(os.path.join(S, "executed-lines.json"))))
src = open(REF).read().splitlines()

def runs():
    for f in res:
        for r in f["runs"]:
            yield f["fixture"], r

def rules_bytes(r):
    out = []
    for name, ent in r["files"].items():
        if name.endswith(".conf") or name.startswith("r"):
            if "b64" in ent:
                out.append((name, base64.b64decode(ent["b64"])))
    return out

def clients_bytes(r):
    for name, ent in r["files"].items():
        if name in ("c.json", "big.json", "cb.json") and "b64" in ent:
            return base64.b64decode(ent["b64"])
    return None

stats = {}
def bump(k, v=None):
    stats.setdefault(k, {"n": 0, "where": []})
    stats[k]["n"] += 1
    if v and v not in stats[k]["where"]:
        stats[k]["where"].append(v)

for fx, r in runs():
    argv = r["argv"]
    out = r["out"]
    setup = "MADO_GEOMETRY: SETUP" in out
    # a) flags order in a run that produced a report (not usage)
    if "--clients" in argv and "--rules" in argv and argv.index("--rules") < argv.index("--clients"):
        if not (setup and out.strip().endswith("usage")):
            bump("valid_run_with_rules_before_clients", fx)
        bump("any_run_with_rules_before_clients", fx)
    # b) invalid utf-8 in a rules file
    for name, raw in rules_bytes(r):
        text = None
        try:
            raw.decode("utf-8"); text = "ok"
        except UnicodeDecodeError:
            bump("rules_file_with_invalid_utf8", fx + ":" + name)
    # c) runs with >= 2 --rules ending in SETUP
    nrule = argv.count("--rules")
    if nrule >= 2:
        bump("run_with_two_or_more_rules", fx)
        if setup:
            bump("setup_failure_with_two_or_more_rules", fx)
    # d) BADSIZE on a non-floating client
    for ln in out.splitlines():
        if ln.startswith("MADO_GEOM_CLIENT: "):
            fl = ln.split(" floating=")[1].split(" ")[0]
            v = ln.split(" verdict=")[-1]
            if v == "BADSIZE" and fl == "false":
                bump("client_badsize_and_not_floating", fx)
    # e) duplicate address key
    cb = clients_bytes(r)
    if cb:
        for m in re.finditer(rb"\{[^{}]*\}", cb):
            if m.group(0).count(b'"address"') > 1:
                bump("duplicate_address_key", fx)
        if cb.count(b'"address"') > 0:
            bump("any_address_key", fx)
    # f) a path argument with mode 000
    for a in argv:
        if a.startswith("/") and os.path.exists(a):
            try:
                if (os.stat(a).st_mode & 0o777) == 0:
                    bump("mode000_path", fx)
            except OSError:
                pass
    # g) zero-argument size line
    for name, raw in rules_bytes(r):
        try:
            text = raw.decode("utf-8", "replace")
        except Exception:
            continue
        if re.search(r"^\s*windowrule[ \t]*=[ \t]*size[ \t]*$", text, re.M):
            bump("bare_size_effect_no_args", fx + ":" + name)
        if re.search(r"^\s*windowrule[ \t]*=[ \t]*$", text, re.M):
            bump("empty_body_rule_line", fx + ":" + name)
    # h) stdin too_large / boundary
    raw = base64.b64decode(r["stdin_b64"]) if r["stdin_b64"] else b""
    if len(raw) > 1048576:
        bump("stdin_over_max", fx)
    if len(raw) == 1048576:
        bump("stdin_exactly_max", fx)

print("== dimension coverage over the 37 fixtures ==")
for k in sorted(stats):
    print("%-40s %3d  %s" % (k, stats[k]["n"], ",".join(stats[k]["where"][:6]) + ("..." if len(stats[k]["where"]) > 6 else "")))

print("\n== reference lines never executed (149 executed) ==")
for i, line in enumerate(src, 1):
    if i not in ex and line.strip() and not line.strip().startswith("#"):
        print("%4d %s" % (i, line))
