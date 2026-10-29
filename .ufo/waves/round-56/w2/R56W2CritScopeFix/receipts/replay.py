import importlib.util, re, json, subprocess, sys
W = "/fast/scratch/hyaku/mado-r56/R56W2CritScopeFix/work"
L = "/home/vgpnk/Projects/shokunin/mado-shokunin"
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
C56 = load("c1r56", W + "/c1r56.py")
DR = load("draft", L + "/.ufo/waves/round-56/w1/R56RevQuality/check-anchor-cover.py")
scope_covers = C56.scope_covers
URL = re.compile(r"https?://\S+")
def cells(line):
    s = line.strip()
    if s.startswith("|"): s = s[1:]
    if s.endswith("|"): s = s[:-1]
    return [c.strip() for c in s.split("|")]
def reg_rows(path):
    out = {}
    for line in open(path, encoding="utf-8"):
        if re.match(r"^\s{0,3}\|\s*S[0-9]{3,}\s*\|", line):
            c = cells(line); out[c[0]] = c
    return out
def entry_rows(path):
    out = []
    for n, line in enumerate(open(path, encoding="utf-8"), 1):
        if not line.lstrip().startswith("|"): continue
        c = cells(line)
        if len(c) >= 4 and re.fullmatch(r"S[0-9]{3}", c[2]) and re.fullmatch(r"[^:\s]+:[0-9]+", c[3]):
            f, ln = c[3].rsplit(":", 1)
            out.append((c[0], c[2], f, int(ln)))
    return out
def pin_lines(rev, name):
    r = subprocess.run(["git", "-C", L, "cat-file", "blob", f"{rev}:.ufo/waves/round-56/fetch/{name}"], capture_output=True)
    if r.returncode: return None
    return len(r.stdout.split(b"\n"))
def replay(entry, reg, rev=None, tag=""):
    R = reg_rows(reg); rows = entry_rows(entry); res = []
    for rid, sid, f, ln in rows:
        if sid not in R: res.append((rid, sid, ln, "no-reg")); continue
        c = R[sid]; urls = URL.findall(c[1])
        base = urls[-1].rstrip(").,;").rsplit("/", 1)[-1] if urls else None
        nl = pin_lines(rev, f) if rev else None
        if rev and nl is None:
            nl = pin_lines(rev, f.replace("Hyprland-", "", 0))  # same name
        cov_url = scope_covers(c[5], base, ln, nl) if base else False
        cov_c4 = scope_covers(c[5], f, ln, nl)
        d_ok, d_loc = DR.covers(c[5], base, ln) if base else (False, "none")
        res.append((rid, sid, ln, f"url_base={base} nlines={nl} counter_scope(url)={cov_url} counter_scope(cell4={f})={cov_c4} draft_covers={d_ok}"))
    return res
if __name__ == "__main__":
    which = sys.argv[1]
    if which == "r55":
        res = replay(W + "/entry-r55.md", W + "/sources-r55.md", None)
    else:
        res = replay(W + "/entry-r56.md", W + "/sources-r56.md", "28fc86ac2359ec27406d8a2c63bef82ea6e947ed")
    for r in res: print(*r)
    print("rows", len(res))
