# Seat-local forger/blind-spot experiments on scratch copies of the base tree (never the lane).
import os, subprocess, shutil, sys, tarfile, io
ROOT = "/fast/scratch/hyaku/mado-r56/R56RevC3Contract"
WORK = ROOT + "/work"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REV = "13f0acbe3a15da2d9c08357a576d91dcadc85273"
ENV = {"PATH": os.environ["PATH"], "HOME": WORK, "TMPDIR": WORK, "LC_ALL": "C"}
base_tar = subprocess.run(["git", "-C", LANE, "archive", REV, "corpus"], env=ENV, capture_output=True, check=True).stdout
BASE = WORK + "/base-tree"
if os.path.exists(BASE): shutil.rmtree(BASE)
os.makedirs(BASE)
tarfile.open(fileobj=io.BytesIO(base_tar)).extractall(BASE)

def mk(name, edits):
    D = subprocess.run(["mktemp", "-d", "-p", ROOT], capture_output=True, text=True, check=True).stdout.strip()
    shutil.rmtree(D); shutil.copytree(BASE, D, symlinks=True)
    subprocess.run(["git", "-C", D, "init", "-q"], env=ENV, check=True)
    top = subprocess.run(["git", "-C", D, "rev-parse", "--show-toplevel"], env=ENV, capture_output=True, text=True, check=True).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(D), (top, D)
    for fn in edits: fn(D)
    subprocess.run(["git", "-C", D, "add", "-A"], env=ENV, check=True)
    subprocess.run(["git", "-C", D, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "-m", name], env=ENV, check=True)
    out = subprocess.run(["python3", "-I", ROOT + "/c3_v.py", D, "HEAD", WORK, "--dump"], env=ENV, capture_output=True, text=True)
    print(f"[{name}] {out.stdout.strip() or out.stderr.strip()}")
    shutil.rmtree(D)

def rd(D, p): return open(os.path.join(D, p), encoding="utf-8").read()
def wr(D, p, s): open(os.path.join(D, p), "w", encoding="utf-8").write(s)

def m_base(D): pass
def m_unclosed_fence(D):
    p = "corpus/knowledge/arc-synthesis.md"; wr(D, p, "```\n" + rd(D, p))
def m_zwsp_split(D):
    p = "corpus/knowledge/closeout-r11.md"; wr(D, p, rd(D, p).replace("S090", "S\u200b090").replace("S096", "S\u200b096"))
def m_move_subdir(D):
    os.makedirs(os.path.join(D, "corpus/knowledge/archive"))
    shutil.move(os.path.join(D, "corpus/knowledge/walker-deep.md"), os.path.join(D, "corpus/knowledge/archive/walker-deep.md"))
def m_symlink_entry(D):
    os.remove(os.path.join(D, "corpus/knowledge/walker-deep.md"))
    os.symlink("walker-deep-r9.md", os.path.join(D, "corpus/knowledge/walker-deep.md"))
def m_source_line16(D):
    # dispatcher-r51 already has its source: line at 19 (outside first 15); add an unregistered id there
    p = "corpus/knowledge/hyprland-dispatcher-dispatch-r51.md"; s = rd(D, p).split("\n")
    s[18] = s[18] + " S999"; wr(D, p, "\n".join(s))
def m_source_line1_control(D):
    p = "corpus/knowledge/arc-synthesis.md"; s = rd(D, p).split("\n")
    s[0] = s[0] + " S999"; wr(D, p, "\n".join(s))
def m_mixed_fence(D):
    wr(D, "corpus/knowledge/zz-fence-test.md",
       "verified-at: 2026-10-28\n```\n~~~\nS091 cited inside a ``` block closed by ~~~ only\n```\n")
def m_plain_new_entry_cite(D):
    wr(D, "corpus/knowledge/zz-plain-test.md", "verified-at: 2026-10-28\nplain cite S091 here\n")
def m_html_comment(D):
    p = "corpus/knowledge/closeout-r11.md"; wr(D, p, rd(D, p) + "\n<!-- S030 -->\n")

for name, fn in [("base", m_base), ("unclosed-fence-line1", m_unclosed_fence), ("zwsp-split-S090-S096", m_zwsp_split),
                 ("move-to-subdir", m_move_subdir), ("symlink-entry", m_symlink_entry),
                 ("S999-after-line15-source", m_source_line16), ("control-S999-line1-source", m_source_line1_control),
                 ("mixed-fence-tilde-closes", m_mixed_fence), ("control-plain-new-entry-cite", m_plain_new_entry_cite),
                 ("control-html-comment-cite", m_html_comment)]:
    mk(name, [fn])
