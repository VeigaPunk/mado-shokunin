#!/usr/bin/env python3
"""Seat MutC2Receipt: build a worktree-less replay tree of the round-48 C2 draft and
run the frozen C2 counter over receipt/digest mutants.  Git plumbing only (mktree +
commit-tree), because the 1 MiB per-file guard forbids checking out the lane's big
fixtures.  Every path is absolute; every blob is < 1 MiB."""
import os
import subprocess
import sys

L = "/home/vgpnk/Projects/shokunin/mado-shokunin"
W = L + "/.ufo/waves/round-48"
R = "/fast/scratch/hyaku/mado-r48/MutC2Receipt"
REPO = R + "/m"
BASE = "579f694b45c797a9c39761fdb4f9e0a1b71b3585"
COUNTER = L + "/quality/counters/c2-r48-xkb-entry.py"
SEAT = L + "/.ufo/waves/round-48/w2/MutC2Receipt"
ENT = "corpus/knowledge/xkb-keymap-compile-r48.md"
REC = ".ufo/waves/round-48/receipts/xkbcli-compile-keymap-r48.txt"
TOOLS = ".ufo/waves/round-48/tools/make-xkb-receipt.sh"
FETCH = ".ufo/waves/round-48/fetch/"

ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
IENV = dict(ENV, GIT_AUTHOR_NAME="mado-seat", GIT_AUTHOR_EMAIL="seat@scratch.invalid",
            GIT_COMMITTER_NAME="mado-seat", GIT_COMMITTER_EMAIL="seat@scratch.invalid")


def git(*a, inp=None, check=True, env=None):
    p = subprocess.run(["git", "-C", REPO, *a], input=inp, capture_output=True,
                       env=env or ENV)
    if check and p.returncode != 0:
        raise SystemExit("git %s failed rc=%d err=%s" % (a, p.returncode, p.stderr[:400]))
    return p


def blob(data):
    return git("hash-object", "-w", "--stdin", inp=data).stdout.decode().strip()


def base_blob(path):
    return git("cat-file", "blob", BASE + ":" + path).stdout


def base_exists(path):
    return git("cat-file", "-e", BASE + ":" + path, check=False).returncode == 0


def ls_tree(dpath):
    ref = BASE + (":" + dpath if dpath else "")
    out = git("ls-tree", "-z", ref).stdout
    ents = []
    for rec in out.split(b"\0"):
        if not rec:
            continue
        meta, name = rec.split(b"\t", 1)
        mode, typ, sha = meta.split(b" ")
        ents.append((mode, typ, sha, name))
    return ents


def mktree(lines):
    return git("mktree", "-z", inp=b"\0".join(lines) + b"\0").stdout.strip().decode()


def build_tree(files, dirs, dpath=""):
    base_ents = ls_tree(dpath) if base_exists(dpath) else []
    lines, have = [], set()
    for mode, typ, sha, name in base_ents:
        child = (dpath + "/" + name.decode()) if dpath else name.decode()
        have.add(name)
        if child in files:
            lines.append(b"100644 blob " + files[child].encode() + b"\t" + name)
        elif child in dirs:
            sub = build_tree(files, dirs, child)
            lines.append(b"040000 tree " + sub.encode() + b"\t" + name)
        else:
            lines.append(mode + b" " + typ + b" " + sha + b"\t" + name)
    for child in sorted(dirs):
        parent, _, name = child.rpartition("/")
        if parent == dpath and name.encode() not in have:
            sub = build_tree(files, dirs, child)
            lines.append(b"040000 tree " + sub.encode() + b"\t" + name.encode())
    for child in sorted(files):
        parent, _, name = child.rpartition("/")
        if parent == dpath and name.encode() not in have:
            lines.append(b"100644 blob " + files[child].encode() + b"\t" + name.encode())
    return mktree(lines)


def make_commit(contents, parent, msg):
    files = {p: blob(b) for p, b in contents.items()}
    dirs = set()
    for p in contents:
        parts = p.split("/")[:-1]
        for i in range(1, len(parts) + 1):
            dirs.add("/".join(parts[:i]))
    tree = build_tree(files, dirs)
    return git("commit-tree", tree, "-p", parent, "-m", msg, env=IENV).stdout.decode().strip()


def clean_contents():
    c = {}
    c[ENT] = open(W + "/l1-draft/xkb-keymap-compile-r48.md", "rb").read()
    c[REC] = open(W + "/receipts/xkbcli-compile-keymap-r48.txt", "rb").read()
    c[TOOLS] = open(W + "/tools/make-xkb-receipt.sh", "rb").read()
    for name in sorted(os.listdir(W + "/fetch")):
        c[FETCH + name] = open(W + "/fetch/" + name, "rb").read()
    rows = open(W + "/l1-draft/rows-c2.md").read().rstrip("\n").split("\n")
    rr = open(W + "/l1-draft/readme-row.md").read().rstrip("\n")
    src = base_blob("corpus/SOURCES.md").decode().split("\n")
    i = max(k for k, l in enumerate(src) if l.startswith("| S339 |"))
    src[i + 1:i + 1] = rows
    c["corpus/SOURCES.md"] = "\n".join(src).encode()
    rdm = base_blob("corpus/README.md").decode().split("\n")
    i = max(k for k, l in enumerate(rdm)
            if l.startswith("| `knowledge/xdg-terminal-selection-r47.md`"))
    rdm[i + 1:i + 1] = [rr]
    c["corpus/README.md"] = "\n".join(rdm).encode()
    return c


def sub1(text, old, new, where):
    n = text.count(old)
    if n != 1:
        raise SystemExit("sub1 %s: count=%d for %r" % (where, n, old[:70]))
    return text.replace(old, new)


def subn(text, old, new, want, where):
    n = text.count(old)
    if n != want:
        raise SystemExit("subn %s: count=%d want=%d for %r" % (where, n, want, old[:70]))
    return text.replace(old, new)


def edit_block(text, marker_line, old, new, where, span=25):
    lines = text.split("\n")
    idx = [i for i, l in enumerate(lines) if l == marker_line]
    if len(idx) != 1:
        raise SystemExit("block %s: marker lines=%d %r" % (where, len(idx), marker_line))
    seen = 0
    for j in range(idx[0], min(len(lines), idx[0] + span)):
        if old in lines[j]:
            lines[j] = lines[j].replace(old, new)
            seen += 1
    if seen != 1:
        raise SystemExit("block %s: hits=%d for %r" % (where, seen, old[:70]))
    return "\n".join(lines)


def insert_after(text, anchor, newline, where):
    lines = text.split("\n")
    idx = [i for i, l in enumerate(lines) if anchor in l]
    if len(idx) != 1:
        raise SystemExit("insert %s: anchors=%d" % (where, len(idx)))
    lines.insert(idx[0] + 1, newline)
    return "\n".join(lines)


DIG = "efd487a399201523540f4e5bbf81818be3183f6d9957c2f2b12469a2cf6fce81"
DIG_BAD = "efd487a399201523540f4e5bbf81818be3183f6d9957c2f2b12469a2cf6fce82"
DECOY = "deadbeef" * 8  # 64 hex, no file on this host has this digest
POSCMD = "`xkbcli compile-keymap --layout br --options compose:caps`"
ZZROW = "| `--layout zz` | XKB-338 `symbols/zz`, XKB-661 `zz`, XKB-769, XKB-822 | rc 1 |"
OPTROW = ('| `--options nope:nope` | XKB-595 `Unrecognized RMLVO option "nope:nope" '
          'was ignored` | rc 0 |')
OPTLINE = 'xkbcommon: ERROR: [XKB-595] Unrecognized RMLVO option "nope:nope" was ignored'


def m_clean(c):
    return c


def mk(rec_edits=(), ent_edits=()):
    def f(c):
        c = dict(c)
        for fn in rec_edits:
            c[REC] = fn(c[REC].decode()).encode()
        for fn in ent_edits:
            c[ENT] = fn(c[ENT].decode()).encode()
        return c
    return f


MUTANTS = [
    ("M00-clean", "unmutated draft overlaid on base (positive control)", m_clean,
     "ADMIT"),
    ("M01-digest-receipt-only", "receipt host.keymap digest last nibble 1->2", mk(
        rec_edits=[lambda t: sub1(t, DIG + "  host.keymap", DIG_BAD + "  host.keymap", "rec dig")]),
     "MISS"),
    ("M02-digest-both", "same digest mutation in receipt and entry", mk(
        rec_edits=[lambda t: sub1(t, DIG + "  host.keymap", DIG_BAD + "  host.keymap", "rec dig")],
        ent_edits=[lambda t: sub1(t, DIG, DIG_BAD, "ent dig")]),
     "MISS"),
    ("M03-decoy-digest-after", "extra keymap-naming digest line in the positive window, "
     "entry cites the decoy; real host.keymap line untouched", mk(
        rec_edits=[lambda t: insert_after(t, DIG + "  host.keymap",
                                          "  keymap-body sha256 " + DECOY, "rec decoy")],
        ent_edits=[lambda t: sub1(t, DIG, DECOY, "ent decoy")]),
     "MISS-if-replay-binds"),
    ("M04-decoy-as-hostkeymap-after", "decoy planted as a second '<hex>  host.keymap' line "
     "after the real one, entry cites the decoy", mk(
        rec_edits=[lambda t: insert_after(t, DIG + "  host.keymap",
                                          DECOY + "  host.keymap", "rec decoy2")],
        ent_edits=[lambda t: sub1(t, DIG, DECOY, "ent decoy2")]),
     "MISS-if-replay-binds"),
    ("M05-hostkeymap-bogus-true-elsewhere", "host.keymap line carries a wrong digest, the true "
     "digest kept in another keymap line; entry keeps the true digest", mk(
        rec_edits=[lambda t: insert_after(t, DIG + "  host.keymap",
                                          "  keymap-body sha256 " + DIG, "rec true2"),
                   lambda t: sub1(t, DIG + "  host.keymap", DIG_BAD + "  host.keymap", "rec dig5")]),
     "MISS"),
    ("M06-argv-model-nope", "receipt's positive command gains '--model nope' (its real output "
     "digest cannot be the recorded one); entry quotes the mutated argv", mk(
        rec_edits=[lambda t: sub1(t, "/usr/bin/xkbcli compile-keymap --layout br --options compose:caps > host.keymap",
                                  "/usr/bin/xkbcli compile-keymap --layout br --model nope --options compose:caps > host.keymap",
                                  "rec argv")],
        ent_edits=[lambda t: sub1(t, POSCMD,
                                  "`xkbcli compile-keymap --layout br --model nope --options compose:caps`",
                                  "ent argv")]),
     "MISS-if-argv-bound"),
    ("M07-argv-extra-variant", "receipt's positive command gains '--variant ext'; entry quotes it", mk(
        rec_edits=[lambda t: sub1(t, "/usr/bin/xkbcli compile-keymap --layout br --options compose:caps > host.keymap",
                                  "/usr/bin/xkbcli compile-keymap --layout br --variant ext --options compose:caps > host.keymap",
                                  "rec argv7")],
        ent_edits=[lambda t: sub1(t, POSCMD,
                                  "`xkbcli compile-keymap --layout br --variant ext --options compose:caps`",
                                  "ent argv7")]),
     "MISS-if-argv-bound"),
    ("M08-entry-argv-us", "entry's positive command says '--layout us'; receipt untouched", mk(
        ent_edits=[lambda t: sub1(t, POSCMD,
                                  "`xkbcli compile-keymap --layout us --options compose:caps`",
                                  "ent us")]),
     "MISS"),
    ("M09-neg-rc-receipt-zz", "unknown-layout probe rc 1->2 in the receipt only", mk(
        rec_edits=[lambda t: edit_block(t, "--- unknown layout", "rc=1", "rc=2", "zz rc", span=15)]),
     "MISS"),
    ("M10-neg-rc-both-zz", "unknown-layout rc 1->2 in receipt and entry table", mk(
        rec_edits=[lambda t: edit_block(t, "--- unknown layout", "rc=1", "rc=2", "zz rc2", span=15)],
        ent_edits=[lambda t: sub1(t, ZZROW, ZZROW.replace("rc 1", "rc 2"), "ent zz")]),
     "MISS"),
    ("M11-neg-rc-entry-zz", "entry table rc 1->2 for --layout zz; receipt untouched", mk(
        ent_edits=[lambda t: sub1(t, ZZROW, ZZROW.replace("rc 1", "rc 2"), "ent zz2")]),
     "MISS"),
    ("M12-rc-drift-double", "a second rc=0 line added inside the unknown-layout block "
     "(rc drift toward a neighbour)", mk(
        rec_edits=[lambda t: insert_after(t, "--- unknown layout", "rc=0", "rec zz drift")]),
     "MISS"),
    ("M13-diag-id-option", "unknown-option diagnostic id XKB-595->596 in both receipt blocks and "
     "the entry row", mk(
        rec_edits=[lambda t: subn(t, '[XKB-595] Unrecognized RMLVO option',
                                  '[XKB-596] Unrecognized RMLVO option', 2, "rec id13")],
        ent_edits=[lambda t: sub1(t, OPTROW, OPTROW.replace("XKB-595", "XKB-596"), "ent id13")]),
     "MISS-if-id-bound"),
    ("M14-diag-all-595", "every XKB-595 in receipt and entry renamed to XKB-596", mk(
        rec_edits=[lambda t: subn(t, "XKB-595", "XKB-596", 4, "rec id14")],
        ent_edits=[lambda t: subn(t, "XKB-595", "XKB-596", 5, "ent id14")]),
     "MISS-if-id-bound"),
    ("M15-version-both", "version triple 1.13.2->1.13.3 in receipt package line and entry",
     mk(rec_edits=[lambda t: sub1(t, "libxkbcommon-1.13.2-1", "libxkbcommon-1.13.3-1", "rec ver")],
        ent_edits=[lambda t: sub1(t, "libxkbcommon 1.13.2-1", "libxkbcommon 1.13.3-1", "ent ver a"),
                   lambda t: sub1(t, "the same 1.13.2-1", "the same 1.13.3-1", "ent ver b")]),
     "MISS-if-version-bound"),
    ("M16-version-receipt-only", "receipt version 1.13.2->1.13.3; entry untouched", mk(
        rec_edits=[lambda t: sub1(t, "libxkbcommon-1.13.2-1", "libxkbcommon-1.13.3-1", "rec ver16")]),
     "MISS"),
    ("M17-entry-digest-bad", "entry's stated digest replaced; receipt untouched", mk(
        ent_edits=[lambda t: sub1(t, DIG, DIG_BAD, "ent dig17")]),
     "MISS"),
    ("M18-entry-option-rc", "entry table rc 0->2 for nope:nope; receipt untouched", mk(
        ent_edits=[lambda t: sub1(t, OPTROW, OPTROW.replace("rc 0", "rc 2"), "ent opt rc")]),
     "MISS"),
    ("M19-entry-pos-rc", "entry's positive sentence rc 0->2; receipt untouched", mk(
        ent_edits=[lambda t: sub1(t, "` returns rc 0, prints nothing", "` returns rc 2, prints nothing",
                                  "ent pos rc")]),
     "MISS"),
    ("M17b-entry-digest-first12", "entry's stated digest changes its first 12 hex (the prefix clause f "
     "actually compares); receipt untouched", mk(
        ent_edits=[lambda t: sub1(t, DIG, "000000000000" + DIG[12:], "ent dig17b")]),
     "MISS"),
    ("M26-entry-digest-other-window", "entry cites the receipt's XDG probe digest (a real hex64 in the "
     "receipt, outside every positive window); receipt untouched", mk(
        ent_edits=[lambda t: sub1(t, DIG,
                                  "49d957933ce19e9e00004ab6caf978c3701f174e251ba310ed8a66f911772676",
                                  "ent dig26")]),
     "MISS"),
    ("M27-decoy-digest-kccgst-window", "decoy keymap digest added to the separate KcCGST positive window, "
     "entry cites it; host.keymap line untouched", mk(
        rec_edits=[lambda t: insert_after(t,
                                          "$ /usr/bin/xkbcli compile-keymap --kccgst --layout br --options compose:caps",
                                          "  keymap-sha256 " + DECOY, "rec decoy27")],
        ent_edits=[lambda t: sub1(t, DIG, DECOY, "ent decoy27")]),
     "MISS-if-replay-binds"),
    ("M17c-entry-digest-tail", "entry's stated digest keeps the 12-hex prefix and changes all 52 "
     "remaining hex; receipt untouched", mk(
        ent_edits=[lambda t: sub1(t, DIG, DIG[:12] + "f" * 52, "ent dig17c")]),
     "MISS"),
    ("M04b-decoy-as-hostkeymap-before", "decoy planted as a '<hex>  host.keymap' line BEFORE the real "
     "one, entry cites the decoy", mk(
        rec_edits=[lambda t: sub1(t, DIG + "  host.keymap",
                                  DECOY + "  host.keymap\n" + DIG + "  host.keymap", "rec decoy4b")],
        ent_edits=[lambda t: sub1(t, DIG, DECOY, "ent decoy4b")]),
     "MISS"),
    ("M20-no-hostkeymap-line", "the '<64hex>  host.keymap' line is removed (the only line clause r can bind)",
     mk(rec_edits=[lambda t: sub1(t, DIG + "  host.keymap\n", "host.keymap body: 73079 bytes\n",
                                  "rec nokey")]),
     "MISS"),
    ("M21-argv-us-receipt-only", "receipt's positive command says '--layout us'; entry and digest untouched",
     mk(rec_edits=[lambda t: sub1(t, "/usr/bin/xkbcli compile-keymap --layout br --options compose:caps > host.keymap",
                                  "/usr/bin/xkbcli compile-keymap --layout us --options compose:caps > host.keymap",
                                  "rec argv21")]),
     "MISS"),
    ("M22-diag-receipt-only", "unknown-option id XKB-595->596 in both receipt blocks; entry still says 595",
     mk(rec_edits=[lambda t: subn(t, '[XKB-595] Unrecognized RMLVO option',
                                  '[XKB-596] Unrecognized RMLVO option', 2, "rec id22")]),
     "MISS-if-id-compared"),
    ("M23-diag-entry-only", "entry's unknown-option row XKB-595->596; receipt still says 595",
     mk(ent_edits=[lambda t: sub1(t, OPTROW, OPTROW.replace("XKB-595", "XKB-596"), "ent id23")]),
     "MISS-if-id-compared"),
    ("M24-neg-rc-variant-receipt", "unknown-variant probe rc 1->2 in the receipt only",
     mk(rec_edits=[lambda t: edit_block(t, "--- unknown variant on a known layout", "rc=1", "rc=2",
                                        "var rc", span=8)]),
     "MISS"),
    ("M25-argv-receipt-only-model-nope", "receipt's positive command gains '--model nope'; entry still quotes "
     "the plain command", mk(
        rec_edits=[lambda t: sub1(t, "/usr/bin/xkbcli compile-keymap --layout br --options compose:caps > host.keymap",
                                  "/usr/bin/xkbcli compile-keymap --layout br --model nope --options compose:caps > host.keymap",
                                  "rec argv25")]),
     "MISS-if-argv-bound"),
]


def run_counter(rev, outname):
    td = R + "/tmp/" + rev.replace("/", "_")
    os.makedirs(td, exist_ok=True)
    p = subprocess.run(["python3", "-I", COUNTER, "--repo", REPO, "--rev", rev],
                       capture_output=True, env=dict(ENV, TMPDIR=td))
    text = (p.stdout + p.stderr).decode("utf-8", "replace")
    with open(SEAT + "/" + outname, "w") as fh:
        fh.write(text)
    return p.returncode, text


def main():
    os.makedirs(SEAT, exist_ok=True)
    os.makedirs(R + "/tmp", exist_ok=True)
    gd = git("rev-parse", "--absolute-git-dir").stdout.decode().strip()
    if gd != REPO + "/.git":
        raise SystemExit("REPO ROOT MISMATCH: %s != %s/.git" % (gd, REPO))
    clean = clean_contents()
    ccommit = make_commit(clean, BASE, "c2-draft-clean")
    git("update-ref", "refs/mut/M00-clean", ccommit)
    want = [a for a in sys.argv[1:]] or [m[0] for m in MUTANTS]
    if "M00-clean" in want:
        rc, text = run_counter("refs/mut/M00-clean", "counter-M00-clean.txt")
        cl = [l for l in text.splitlines() if "clauses=" in l or "admitted=" in l]
        print("M00-clean exit=%d %s" % (rc, " || ".join(cl)))
        if rc != 0:
            print(text)
            return 1
    for mid, note, fn, expect in MUTANTS:
        if mid == "M00-clean" or mid not in want:
            continue
        contents = fn(clean)
        change = sum(1 for k in clean if contents[k] != clean[k])
        commit = make_commit(contents, ccommit, mid)
        git("update-ref", "refs/mut/" + mid, commit)
        rc, text = run_counter("refs/mut/" + mid, "counter-%s.txt" % mid)
        verdict = "ADMITTED" if rc == 0 else ("SETUP" if rc == 2 else "missed")
        fails = [l for l in text.splitlines()
                 if (" clause=" in l and ("rc_values" in l or "bad" in l or "disagree" in l
                                          or "missing" in l or "no_" in l or "failed" in l
                                          or "short" in l or "mismatch" in l or "ground" in l))
                 or l.startswith("PRED-C2-r48 SETUP")]
        cl = [l for l in text.splitlines() if "clauses=" in l]
        print("%-34s files=%d exit=%d %-9s expect=%s" % (mid, change, rc, verdict, expect))
        for l in (fails[:4] or cl):
            print("    " + l.strip()[:220])
    return 0


if __name__ == "__main__":
    sys.exit(main())
