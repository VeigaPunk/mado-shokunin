import os, subprocess, sys, tempfile, json
L = "/home/vgpnk/Projects/shokunin/mado-shokunin"
R = "57584ed67716340b3d466fa04333ac0bab3fb79e"
BASE = "3b55b6e91e40f455dd56b2985e4ffc087ada92d5"
ENTRY = "corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md"
W = "/fast/scratch/hyaku/mado-r55/R55W2CritC3Stale"
COUNTER = W + "/c3-committed.py"
ENV = {"PATH": "/usr/bin:/bin", "LC_ALL": "C", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}
D = tempfile.mkdtemp(prefix="c3atk-", dir=W)
os.makedirs(D + "/.git/objects/info", exist_ok=True)
subprocess.run(["git", "-C", D, "init", "-q"], check=True, env=ENV)
top = subprocess.run(["git", "-C", D, "rev-parse", "--show-toplevel"], stdout=subprocess.PIPE, env=ENV).stdout.decode().strip()
assert os.path.realpath(top) == os.path.realpath(D), (top, D)
open(D + "/.git/objects/info/alternates", "w").write(L + "/.git/objects\n")

def g(*a, inp=None, idx=None):
    env = dict(ENV)
    if idx: env["GIT_INDEX_FILE"] = idx
    p = subprocess.run(["git", "-C", D] + list(a), input=inp, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    if p.returncode: raise RuntimeError(" ".join(a) + ": " + p.stderr.decode())
    return p.stdout

base_entry = g("cat-file", "blob", BASE + ":" + ENTRY)
good_entry = g("cat-file", "blob", R + ":" + ENTRY)
assert good_entry.startswith(base_entry)
lines = good_entry.split(b"\n")
idxs = [i for i, l in enumerate(lines) if l.startswith(b"| P23 | P19 |")]
assert len(idxs) == 1, idxs
P23I = idxs[0]
REAL = lines[P23I]
cells = REAL.split(b"|")
assert cells[0] == b"" and cells[-1] == b"", cells[-1]
HEAD = "`Actions::pass` sends modifier state (`sendKeyboardMods`) before its delivery branch and clears it after that branch. The branch tests `m_passPressed`. When `m_passPressed == 1`, a non-mouse key sends a keyboard key PRESSED and a mouse button sends a pointer button PRESSED. When `m_passPressed == 0`, a non-mouse key sends a keyboard key RELEASED and a mouse button sends a pointer button RELEASED. "
ELSE_FALSE = "When `m_passPressed` is any other value (the `else` arm), the branch sends only a keyboard key RELEASED and never a keyboard key PRESSED."
ELSE_FALSE2 = "When `m_passPressed` is any other value (the `else` arm), keyboard keys are never sent; a mouse button sends a pointer button PRESSED and then a pointer button RELEASED."
TAIL_TRUE = " A keyboard key PRESSED is sent "
def with_prop(prop, compact=False, pieces=None):
    c = list(cells)
    c[3] = (" " + prop + " ").encode("utf-8")
    if compact:
        return b"|" + b"|".join(x.strip() for x in c[1:-1]) + b"|"
    return b"|".join(c)

def variant_line(prop, **kw):
    return with_prop(prop, **kw)

V = {}
V["V0_real_true_row (control)"] = (REAL, None)
V["V1_else_only_RELEASED_false"] = (variant_line(HEAD + ELSE_FALSE), None)
V["V2_else_keyboard_never_false"] = (variant_line(HEAD + ELSE_FALSE2), None)
V["V3_cyrillic_o_only_when_restates_P19"] = (variant_line(HEAD + ELSE_FALSE + TAIL_TRUE + "sent".join([""," "]) if False else HEAD + ELSE_FALSE + TAIL_TRUE + "\u043en" + "ly when `m_passPressed == 1`."), None)
V["V4_zwsp_only_when"] = (variant_line(HEAD + ELSE_FALSE + TAIL_TRUE + "on\u200bly\u200b when `m_passPressed == 1`.".replace("on\u200bly\u200b when", "only\u200bwhen")), None)
V["V5_nbsp_only_when"] = (variant_line(HEAD + ELSE_FALSE + TAIL_TRUE + "only\u00a0when `m_passPressed == 1`."), None)
V["V6_html_entity_only_when"] = (variant_line(HEAD + ELSE_FALSE + TAIL_TRUE + "only&#32;when `m_passPressed == 1`."), None)
V["V7_double_space_only_when"] = (variant_line(HEAD + ELSE_FALSE + TAIL_TRUE + "only  when `m_passPressed == 1`."), None)
V["V8_tab_only_when"] = (variant_line(HEAD + ELSE_FALSE + TAIL_TRUE + "only\twhen `m_passPressed == 1`."), None)
V["V9_upper_tab_ONLY_WHEN"] = (variant_line(HEAD + ELSE_FALSE + TAIL_TRUE + "ONLY\tWHEN `m_passPressed == 1`."), None)
V["V10_fullwidth_only_when"] = (variant_line(HEAD + ELSE_FALSE + TAIL_TRUE + "\uff4f\uff4e\uff4c\uff59 \uff37\uff48\uff45\uff4e `m_passPressed == 1`."), None)
V["V11_compact_spacing_false"] = (variant_line(HEAD + ELSE_FALSE, compact=True), None)
V["V12_ASCII_only_when_control"] = (variant_line(HEAD + ELSE_FALSE + TAIL_TRUE + "only when `m_passPressed == 1`."), None)
V["V13_ASCII_ONLY_WHEN_control"] = (variant_line(HEAD + ELSE_FALSE + TAIL_TRUE + "ONLY WHEN `m_passPressed == 1`."), None)
V["V14_nbsp_in_eq_one_negative"] = (variant_line(HEAD.replace("== 1", "==\u00a01") + ELSE_FALSE), None)
V["V15_lowercase_PRESSED_negative"] = (variant_line((HEAD + ELSE_FALSE).replace("PRESSED", "Pressed")), None)
# split across a line break inside the P23 row: row cannot span lines in markdown; counter reads it as a non-row
half = (HEAD + ELSE_FALSE)[: len(HEAD) // 2].encode()
rest = (HEAD + ELSE_FALSE)[len(HEAD) // 2:].encode()
V["V16_row_split_across_line_break"] = ((b"| P23 | P19 | " + half + b"\n" + rest + b" | S371 | Hyprland-ConfigActions.cpp:1554-1576 | Q01 to Q13 below | direct |"), None)
V["V17_true_row_plus_prose_only_newline_when (stale split)"] = (REAL, "\nA keyboard key PRESSED is sent only\nwhen `m_passPressed == 1` in the if arm, as P19 said.\n")
V["V18_false_row_plus_prose_only_newline_when"] = (variant_line(HEAD + ELSE_FALSE), "\nA keyboard key PRESSED is sent only\nwhen `m_passPressed == 1`, and the else arm sends only a keyboard key RELEASED.\n")
V["V19_false_row_plus_P19_sentence_verbatim (stale control)"] = (variant_line(HEAD + ELSE_FALSE), "\n`Actions::pass` sends modifier state before its delivery branch; it sends a PRESSED keyboard key only when `m_passPressed == 1` and the key is not a mouse button.\n")

def build(name, rowline, extra):
    ls = list(lines)
    ls[P23I] = rowline
    out = b"\n".join(ls)
    if extra:
        out = out.rstrip(b"\n") + b"\n" + extra.encode("utf-8")
    idx = D + "/idx-%d" % abs(hash(name)) 
    if os.path.exists(idx): os.unlink(idx)
    g("read-tree", R, idx=idx)
    sha = g("hash-object", "-w", "--stdin", inp=base_entry[:0] + out).decode().strip()
    g("update-index", "--add", "--cacheinfo", "100644,%s,%s" % (sha, ENTRY), idx=idx)
    tree = g("write-tree", idx=idx).decode().strip()
    c = g("-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit-tree", tree, "-p", R, "-m", name).decode().strip()
    return c, out

results = []
commits = {}
for name, (rowline, extra) in V.items():
    c, out = build(name, rowline, extra)
    commits[name] = c
    wd = W + "/w-" + name.split("_")[0]
    os.makedirs(wd, exist_ok=True)
    p = subprocess.run([sys.executable, "-I", COUNTER, "--repo", D, "--rev", c, "--work", wd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV)
    line = p.stdout.decode().strip()
    blk = out[len(base_entry):]
    stale_pre = (b"only when" in blk.lower())
    sw = out.split(b"\n")
    diff_n = sum(1 for a, b in zip(lines, sw) if a != b) + abs(len(sw) - len(lines))
    print("%-55s rc=%d stale_substr=%s changed_lines=%d\n    %s" % (name, p.returncode, stale_pre, diff_n, line or p.stderr.decode()[:300]))
    results.append({"name": name, "commit": c, "rc": p.returncode, "line": line, "stale_substr": stale_pre, "changed_lines": diff_n})
json.dump(commits, open(W + "/commits.json", "w"), indent=1)
json.dump(results, open(W + "/results.json", "w"), indent=1, ensure_ascii=False)
open(W + "/entry-V1.bin", "wb").write(g("cat-file", "blob", commits["V1_else_only_RELEASED_false"] + ":" + ENTRY))
print("DIR", D)
