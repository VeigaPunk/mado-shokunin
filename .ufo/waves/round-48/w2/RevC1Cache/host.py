#!/usr/bin/env python3
"""Independent pin-vs-frozen-tool measurement of the xdg-terminal-exec v0.14.3 cache contract.

Pin: the round-47 fetch copy (sha256 checked) run as `/bin/sh <pin>` (host /bin/sh = bash 5.3).
Tool: .ufo/waves/round-48/l1-draft/mado-terminal.py (the frozen candidate) run as `python3 -I`.
One tree; the primed cache is rewritten per case. Nothing outside $S is written.
"""
import json, os, shutil, stat, subprocess, sys

L = "/home/vgpnk/Projects/shokunin/mado-shokunin"
PIN = os.path.join(L, ".ufo/waves/round-47/fetch/xdg-terminal-exec")
TOOL = os.path.join(L, ".ufo/waves/round-48/l1-draft/mado-terminal.py")
S = "/fast/scratch/hyaku/mado-r48/RevC1Cache"
T = os.path.join(S, "tree")
CACHE = os.path.join(T, ".rw", "cache", "xdg-terminal-exec")
TERM = "\x1eEND_OF_EXEC_USEP"

def pin_sha():
    import hashlib
    return hashlib.sha256(open(PIN, "rb").read()).hexdigest()

def build():
    shutil.rmtree(T, ignore_errors=True)
    for d in ("home/.config", "home/.local/share", "etc/xdg", "usr/share/applications", "bin", ".rw/cache"):
        os.makedirs(os.path.join(T, d), exist_ok=True)
    open(os.path.join(T, "home/.config/hyprland-xdg-terminals.list"), "w").write("foot.desktop\n")
    open(os.path.join(T, "usr/share/applications/foot.desktop"), "w").write(
        "[Desktop Entry]\nType=Application\nCategories=TerminalEmulator;\nExec=foot\n")
    p = os.path.join(T, "bin/foot")
    open(p, "w").write("#!/bin/sh\nexit 1\n")
    os.chmod(p, 0o755)

UNSET = object()
def env(cache_home=UNSET, extra=None):
    e = {"PATH": T + "/bin:/usr/bin:/bin", "HOME": T + "/home", "LANG": "C.UTF-8",
         "XDG_CURRENT_DESKTOP": "Hyprland", "XDG_CONFIG_HOME": T + "/home/.config",
         "XDG_CONFIG_DIRS": T + "/etc/xdg", "XDG_DATA_HOME": T + "/home/.local/share",
         "XDG_DATA_DIRS": T + "/usr/share"}
    if cache_home is UNSET:
        e["XDG_CACHE_HOME"] = T + "/.rw/cache"
    elif cache_home is not None:
        e["XDG_CACHE_HOME"] = cache_home
    if extra:
        e.update(extra)
    return e

def run_pin(args, e, debug=True):
    ee = dict(e)
    if debug:
        ee["XTE_DEBUG"] = "1"
    p = subprocess.run(["/bin/sh", PIN] + args, capture_output=True, env=ee, timeout=60)
    return p.returncode, p.stdout.decode("utf-8", "surrogateescape"), p.stderr.decode("utf-8", "surrogateescape")

def run_tool(args, e):
    p = subprocess.run([sys.executable, "-I", TOOL, "print"] + args, capture_output=True, env=e, timeout=60)
    return p.returncode, p.stdout.decode("utf-8", "surrogateescape"), p.stderr.decode("utf-8", "surrogateescape")

def run_explain(e):
    p = subprocess.run([sys.executable, "-I", TOOL, "explain"], capture_output=True, env=e, timeout=60)
    out = p.stdout.decode("utf-8", "surrogateescape")
    cache = "-"
    import re
    m = re.search(r"MADO_TERM: selected=.*?path=.*?cmd=.*?cache=(\S+) verdict=(\S+)\s*$", out, re.S)
    if m:
        cache = m.group(1)
    return p.returncode, out, cache

STATES = (("cache is actual", "hit"), ("cache is out-of-date", "stale"),
          ("invalid cache data", "invalid"), ("reached cache line limit", "invalid"),
          ("failed to get fresh hash", "invalid"), ("no cache data", "absent"), ("paths:", "disabled"))
def derive_state(err):
    for pat, st in STATES:
        if pat in err:
            return st
    return "-"

def prime():
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    if os.path.exists(CACHE):
        os.chmod(CACHE, 0o644)
        os.unlink(CACHE)
    rc, out, err = run_pin(["--print-cmd"], env(T + "/.rw/cache"))
    for _ in range(300):
        try:
            b = open(CACHE, "rb").read().decode("latin-1")
            if b.endswith("\n") and TERM in b:
                return b, rc, out, err
        except OSError:
            pass
        import time; time.sleep(0.01)
    raise SystemExit("prime failed: rc=%d out=%r err=%r" % (rc, out, err[-400:]))

def set_cache(text, mode=0o644):
    if text is None:
        if os.path.exists(CACHE):
            os.chmod(CACHE, 0o644); os.unlink(CACHE)
        return
    d = os.path.dirname(CACHE)
    os.chmod(d, 0o755)
    if os.path.exists(CACHE):
        os.chmod(CACHE, 0o644)
    open(CACHE, "wb").write(text.encode("latin-1"))
    os.chmod(CACHE, mode)

def cache_after():
    try:
        st = os.stat(CACHE)
    except OSError:
        return "absent"
    try:
        tail = open(CACHE, "rb").read()[-24:].decode("latin-1")
    except OSError as ex:
        tail = "<unreadable: %s>" % ex.strerror
    return "present mode=%o size=%d tail=%r" % (stat.S_IMODE(st.st_mode), st.st_size, tail)

def hdr(base):
    return "\n".join(base.split("\n")[:10])

def case(cid, cache, args, e=None, mode=0o644, note=""):
    e = e or env(T + "/.rw/cache")
    set_cache(cache, mode)
    trc, tout, terr = run_tool(args, e)          # tool first: the oracle rewrites the cache when it misses
    erc, eout, ecache = run_explain(e)
    set_cache(cache, mode)
    prc, pout, perr = run_pin(args, e)
    state = derive_state(perr)
    after = cache_after()
    return dict(id=cid, note=note, args=args, cache=("None" if cache is None else
              repr(cache[:400]) + ("...len=%d" % len(cache) if len(cache) > 400 else "")),
              pin=dict(rc=prc, stdout=pout, state=state, stderr_tail=perr.strip().splitlines()[-2:]),
              tool=dict(rc=trc, stdout=tout, stderr_tail=terr.strip().splitlines()[-2:]),
              explain=dict(rc=erc, cache=ecache, stderr_tail=terr.strip().splitlines()[-2:] if erc not in (0,1,3) else []),
              agree=(prc, pout, state) == (trc, tout, ecache),
              cache_after=after)

def main():
    build()
    base, prc, pout, perr = prime()
    ev = {"pin_sha256": pin_sha(), "prime": dict(rc=prc, stdout=pout, stderr_has_saved="saved cache" in perr,
                                                 cache=base)}
    lines = base.split("\n")[:-1]
    assert len(lines) == 11, len(lines)
    envA = lambda: env(T + "/.rw/cache")
    cases = []
    # --- baseline
    cases.append(case("A0-baseline-hit", base, ["--print-cmd"]))
    # --- unreadable cache file / directory
    cases.append(case("A1-cache-unreadable", base, ["--print-cmd"], mode=0o000))
    os.chmod(CACHE, 0o644)
    cd = os.path.dirname(CACHE)
    os.chmod(cd, 0o000)
    try:
        trc, tout, terr = run_tool(["--print-cmd"], envA())
        erc, eout, ecache = run_explain(envA())
        prc, pout, perr = run_pin(["--print-cmd"], envA())
        st = derive_state(perr)
        cases.append(dict(id="A2-cache-dir-unreadable", note="parent dir mode 000 (cache file still 0644)",
                          args=["--print-cmd"], cache="as A0",
                          pin=dict(rc=prc, stdout=pout, state=st, stderr_tail=perr.strip().splitlines()[-2:]),
                          tool=dict(rc=trc, stdout=tout, stderr_tail=terr.strip().splitlines()[-2:]),
                          explain=dict(rc=erc, cache=ecache),
                          agree=(prc, pout, st) == (trc, tout, ecache), cache_after="dir mode 000"))
    finally:
        os.chmod(cd, 0o755)
    # --- trailing newline / terminator edges
    cases.append(case("A3-no-trailing-newline", base.rstrip("\n"), ["--print-cmd"]))
    cases.append(case("A4-terminated-plus-unterminated-tail", base + "junk", ["--print-cmd"]))
    cases.append(case("A4b-terminated-plus-terminated-junk", base + "junk\n", ["--print-cmd"]))
    # --- 49 / 50 line boundary with a VALID hash and a valid cmd
    l49 = hdr(base) + "\n" + "\n".join(["x"] * 38) + "\nx" + TERM + "\n"
    l50 = hdr(base) + "\n" + "\n".join(["x"] * 39) + "\nx" + TERM + "\n"
    cases.append(case("A5-line49-terminator", l49, ["--print-cmd"],
                      note="lines=%d" % l49.count("\n")))
    cases.append(case("A6-line50-terminator", l50, ["--print-cmd"],
                      note="lines=%d" % l50.count("\n")))
    # --- multiline cached args (LF join from line 11)
    m2 = hdr(base) + "\nfoot\x1f--a\ntail" + TERM + "\n"
    m3 = hdr(base) + "\nfoot\x1f--a\n\nzx" + TERM + "\n"
    cases.append(case("A7-multiline-args-2", m2, ["--print-cmd"]))
    cases.append(case("A7b-multiline-args-2-test", m2, ["--test"]))
    cases.append(case("A7c-multiline-args-2-idpath", m2, ["--print-id", "--print-path"]))
    cases.append(case("A8-multiline-args-empty-middle", m3, ["--print-cmd"]))
    # --- action
    act = "\n".join(lines[:4] + ["srv"] + lines[5:]) + "\n"
    cases.append(case("A9-cached-action", act, ["--print-id", "--print-path", "--print-cmd"]))
    # --- empty fields
    e_cmd = "\n".join([lines[0], ""] + lines[2:]) + "\n"
    cases.append(case("A10-empty-cmd", e_cmd, ["--print-cmd"]))
    e_path = "\n".join(lines[:2] + [""] + lines[3:]) + "\n"
    cases.append(case("A11-empty-path", e_path, ["--print-path"]))
    cases.append(case("A11b-empty-path-content", e_path, ["--print-content"]))
    cases.append(case("A11c-empty-path-id", e_path, ["--print-id"]))
    e_hash = "\n".join([""] + lines[1:]) + "\n"
    cases.append(case("A12-empty-hash", e_hash, ["--print-cmd"]))
    e_id = "\n".join(lines[:3] + [""] + lines[4:]) + "\n"
    cases.append(case("A12b-empty-id-action", e_id, ["--print-id", "--print-path"]))
    # --- exec word-split corners
    term_only = "\n".join(lines[:10]) + "\n" + TERM + "\n"
    cases.append(case("A18-terminator-line11-empty-exec", term_only, ["--print-cmd"]))
    trail = "\n".join(lines[:10]) + "\nfoot\x1f--a\x1f" + TERM + "\n"
    cases.append(case("A19-exec-trailing-usep", trail, ["--print-cmd"]))
    lead = "\n".join(lines[:10]) + "\n\x1ffoot" + TERM + "\n"
    cases.append(case("A20-exec-leading-usep", lead, ["--print-cmd"]))
    # --- cache path default / empty XDG_CACHE_HOME
    homecache = os.path.join(T, "home/.cache")
    os.makedirs(homecache, exist_ok=True)
    shutil.copyfile(CACHE if os.path.exists(CACHE) else "/dev/null", os.path.join(homecache, "xdg-terminal-exec"))
    # prime into the default location with XDG_CACHE_HOME unset
    if os.path.exists(os.path.join(homecache, "xdg-terminal-exec")):
        os.unlink(os.path.join(homecache, "xdg-terminal-exec"))
    e_def = env(None)
    rc, out, err = run_pin(["--print-cmd"], e_def)
    import time
    for _ in range(300):
        p = os.path.join(homecache, "xdg-terminal-exec")
        if os.path.exists(p) and open(p, "rb").read().decode("latin-1").rstrip("\n").endswith(TERM):
            break
        time.sleep(0.01)
    dflt = open(os.path.join(homecache, "xdg-terminal-exec"), "rb").read().decode("latin-1")
    for cid, e2 in (("A13-default-cache-home", e_def), ("A14-empty-cache-home", env(""))):
        set_cache(base)
        trc, tout, terr = run_tool(["--print-cmd"], e2)
        erc, eout, ecache = run_explain(e2)
        set_cache(base)
        prc, pout, perr = run_pin(["--print-cmd"], e2)
        cases.append(dict(id=cid, note="cache at $HOME/.cache/xdg-terminal-exec", args=["--print-cmd"],
                          cache="primed default", pin=dict(rc=prc, stdout=pout, state=derive_state(perr),
                                                           stderr_tail=perr.strip().splitlines()[-2:]),
                          tool=dict(rc=trc, stdout=tout, stderr_tail=terr.strip().splitlines()[-2:]),
                          explain=dict(rc=erc, cache=ecache, stderr_tail=terr.strip().splitlines()[-2:] if erc not in (0,1,3) else []),
                          agree=(prc, pout, derive_state(perr)) == (trc, tout, ecache),
                          cache_after=cache_after()))
    # --- XTE_CACHE_ENABLED empty / false, and the /enable_cache directive
    lst = os.path.join(T, "home/.config/hyprland-xdg-terminals.list")
    for cid, extra, listtext in (
            ("A15-enabled-empty-no-directive", {"XTE_CACHE_ENABLED": ""}, "foot.desktop\n"),
            ("A16-enabled-empty-enable-directive", {"XTE_CACHE_ENABLED": ""}, "/enable_cache\nfoot.desktop\n"),
            ("A16b-enabled-empty-disable-directive", {"XTE_CACHE_ENABLED": ""}, "/disable_cache\nfoot.desktop\n"),
            ("A17-enabled-no", {"XTE_CACHE_ENABLED": "no"}, "foot.desktop\n"),
            ("A17b-enabled-banana-enable-directive", {"XTE_CACHE_ENABLED": "banana"}, "/enable_cache\nfoot.desktop\n")):
        open(lst, "w").write(listtext)
        e2 = env(T + "/.rw/cache", extra)
        set_cache(base)
        trc, tout, terr = run_tool(["--print-cmd"], e2)
        erc, eout, ecache = run_explain(e2)
        set_cache(base)
        prc, pout, perr = run_pin(["--print-cmd"], e2)
        st = derive_state(perr)
        after = cache_after()
        cases.append(dict(id=cid, note="list=%r env XTE_CACHE_ENABLED=%r" % (listtext, extra["XTE_CACHE_ENABLED"]),
                          args=["--print-cmd"], cache="as A0",
                          pin=dict(rc=prc, stdout=pout, state=st, stderr_tail=perr.strip().splitlines()[-3:]),
                          tool=dict(rc=trc, stdout=tout, stderr_tail=terr.strip().splitlines()[-3:]),
                          explain=dict(rc=erc, cache=ecache, stderr_tail=terr.strip().splitlines()[-2:] if erc not in (0,1,3) else []),
                          agree=(prc, pout, st) == (trc, tout, ecache),
                          cache_after=after))
    # --- cache path is a directory; NUL byte inside a cached field
    set_cache(None)
    os.makedirs(CACHE, exist_ok=True)
    trc, tout, terr = run_tool(["--print-cmd"], envA())
    erc, eout, ecache = run_explain(envA())
    prc, pout, perr = run_pin(["--print-cmd"], envA())
    cases.append(dict(id="A21-cache-is-directory", note="cache path is a directory", args=["--print-cmd"],
                      cache="<dir>", pin=dict(rc=prc, stdout=pout, state=derive_state(perr),
                                              stderr_tail=perr.strip().splitlines()[-2:]),
                      tool=dict(rc=trc, stdout=tout, stderr_tail=terr.strip().splitlines()[-2:]),
                      explain=dict(rc=erc, cache=ecache),
                      agree=(prc, pout, derive_state(perr)) == (trc, tout, ecache),
                      cache_after="dir (left in place)"))
    shutil.rmtree(CACHE, ignore_errors=True)
    nul3 = "\n".join(lines[:2] + [lines[2][:10] + "\x00" + lines[2][10:]] + lines[3:]) + "\n"
    cases.append(case("A22-nul-in-cached-path", nul3, ["--print-path"]))
    open(lst, "w").write("foot.desktop\n")
    ev["cases"] = cases
    json.dump(ev, open(os.path.join(S, "ev", "host-cases.json"), "w"), indent=1)
    for c in cases:
        print("-" * 100)
        print(c["id"], "|", c.get("note", ""))
        print("  args:", c["args"])
        print("  pin : rc=%s state=%s out=%r" % (c["pin"]["rc"], c["pin"]["state"], c["pin"]["stdout"]))
        if c["pin"].get("stderr_tail"): print("        stderr:", c["pin"]["stderr_tail"])
        print("  tool: rc=%s out=%r explain_cache=%s" % (c["tool"]["rc"], c["tool"]["stdout"],
                                                         (c.get("explain") or {}).get("cache")))
        print("  agree=%s  cache_after=%s" % (c.get("agree"), c.get("cache_after")))

main()
