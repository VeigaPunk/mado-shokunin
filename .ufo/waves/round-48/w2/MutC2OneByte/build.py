#!/usr/bin/env python3
"""Build the C2 replay commits without a worktree (git plumbing only).

The lane tracks files above the 1 MiB per-file bound this seat must keep, so the
replay tree is never checked out: the base tree is read into the index, the
round-48 draft bytes are hashed in from the lane, and each mutant is one blob
replacement committed on top. The frozen counter reads revisions with git show.

usage: build.py <clone-dir> <scratch-dir>
prints "<mutant> <rev>" lines, base overlay first as M0_base_overlay.
"""
import hashlib
import os
import subprocess
import sys

L = "/home/vgpnk/Projects/shokunin/mado-shokunin"
W = L + "/.ufo/waves/round-48"
BASE = "579f694b45c797a9c39761fdb4f9e0a1b71b3585"
ENTRY = "corpus/knowledge/xkb-keymap-compile-r48.md"
RECEIPT = ".ufo/waves/round-48/receipts/xkbcli-compile-keymap-r48.txt"
D, S = sys.argv[1], sys.argv[2]

ENV = dict(os.environ)
ENV.update({"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
            "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"})


def git(*args, inp=None):
    p = subprocess.run(["git", "-C", D, *args], input=inp, capture_output=True,
                       env=ENV)
    if p.returncode != 0:
        raise SystemExit("git %s failed: %s" % (" ".join(args), p.stderr.decode()))
    return p.stdout


def blob(data):
    return git("hash-object", "-w", "--stdin", inp=data).decode().strip()


def get_tree(sha):
    """name -> (mode, type, sha) for a tree object (or {} for a missing tree)."""
    if sha is None:
        return {}
    out = git("ls-tree", "-z", sha)
    entries = {}
    for rec in out.split(b"\0"):
        if not rec:
            continue
        meta, name = rec.split(b"\t", 1)
        mode, typ, obj = meta.decode().split()
        entries[name.decode()] = (mode, typ, obj)
    return entries


def write_tree(entries):
    data = b""
    for name, (mode, typ, obj) in entries.items():
        data += ("%s %s %s\t" % (mode, typ, obj)).encode() + name.encode() + b"\0"
    return git("mktree", "-z", inp=data).decode().strip()


def add_blob(tree_sha, parts, blob_sha):
    """Return a tree sha with parts/... pointing at blob_sha (tree surgery)."""
    entries = get_tree(tree_sha)
    head = parts[0]
    if len(parts) == 1:
        entries[head] = ("100644", "blob", blob_sha)
    else:
        cur = entries.get(head)
        entries[head] = ("040000", "tree",
                         add_blob(cur[2] if cur else None, parts[1:], blob_sha))
    return write_tree(entries)


def commit(parent, changes, msg):
    parent_tree = git("rev-parse", parent + "^{tree}").decode().strip()
    tree = parent_tree
    for path, data in changes.items():
        tree = add_blob(tree, path.split("/"), blob(data))
    return git("commit-tree", tree, "-p", parent, "-m", msg).decode().strip()


def show(path):
    return git("show", "%s:%s" % (BASE, path))


def insert_after(text, anchor_prefix, block):
    lines = text.split("\n")
    idx = [k for k, l in enumerate(lines) if l.startswith(anchor_prefix)]
    if not idx:
        raise SystemExit("anchor missing: %r" % anchor_prefix)
    i = idx[-1]
    lines[i + 1:i + 1] = block
    return "\n".join(lines)


def overlay():
    """path -> bytes for every file the c2-mirror recipe lands on the base tree."""
    out = {}
    for name in sorted(os.listdir(W + "/fetch")):
        out[".ufo/waves/round-48/fetch/" + name] = open(W + "/fetch/" + name, "rb").read()
    out[RECEIPT] = open(W + "/receipts/xkbcli-compile-keymap-r48.txt", "rb").read()
    out[".ufo/waves/round-48/tools/make-xkb-receipt.sh"] = \
        open(W + "/tools/make-xkb-receipt.sh", "rb").read()
    out[ENTRY] = open(W + "/l1-draft/xkb-keymap-compile-r48.md", "rb").read()
    rows = open(W + "/l1-draft/rows-c2.md").read().rstrip("\n").split("\n")
    out["corpus/SOURCES.md"] = insert_after(
        show("corpus/SOURCES.md").decode(), "| S339 |", rows).encode()
    rr = open(W + "/l1-draft/readme-row.md").read().rstrip("\n")
    out["corpus/README.md"] = insert_after(
        show("corpus/README.md").decode(),
        "| `knowledge/xdg-terminal-selection-r47.md`", [rr]).encode()
    return out


MUT = {
    "M1a_quote_wrong_line": [
        ("sub", "entry", "at xkbcommon-rules.c:1297 - a name",
         "at xkbcommon-rules.c:1298 - a name"),
    ],
    "M1b_quote_true_unsupported": [
        ("sub", "entry", "`Couldn't find file \\\"%s/%.*s\\\" in include paths` "
         "at xkbcommon-include.c:355",
         "`LogIncludePaths(ctx);` at xkbcommon-include.c:353-358"),
    ],
    "M1c_quote_other_pin": [
        ("sub", "entry", "`const char * const root = "
         "xkb_context_include_path_get_system_path(ctx);`",
         "`xkb_symbols \"nodeadkeys\" {`"),
    ],
    "M2a_locator_unbound_shift": [
        ("sub", "entry", "(xkbcommon-rules.c:520-527)", "(xkbcommon-rules.c:500-507)"),
    ],
    "M2b_locator_dup_shift": [
        ("sub", "entry", "at xkbcommon-rules.c:530 - the truncation",
         "at xkbcommon-rules.c:457 - the truncation"),
    ],
    "M2c_locator_no_occurrence": [
        ("sub", "entry", "at xkbcommon-include.c:501 - the XKB-661",
         "at xkbcommon-include.c:505 - the XKB-661"),
    ],
    "M3a_receipt_diag_id_swap": [
        ("sub", "receipt",
         "xkbcommon: ERROR: [XKB-338] Couldn't find file \"symbols/zz\" in include paths\n"
         "xkbcommon: ERROR: [XKB-338] 1 include paths searched:\n"
         "xkbcommon: ERROR: [XKB-338] \t/usr/share/xkeyboard-config-2\n"
         "xkbcommon: ERROR: [XKB-338] 3 include paths could not be added:\n"
         "xkbcommon: ERROR: [XKB-338] \t/home/vgpnk/.config/xkb\n"
         "xkbcommon: ERROR: [XKB-338] \t/home/vgpnk/.xkb\n"
         "xkbcommon: ERROR: [XKB-338] \t/etc/xkb\n"
         "xkbcommon: ERROR: [XKB-661] Couldn't process include statement for 'zz'",
         "xkbcommon: ERROR: [XKB-661] Couldn't find file \"symbols/zz\" in include paths\n"
         "xkbcommon: ERROR: [XKB-661] 1 include paths searched:\n"
         "xkbcommon: ERROR: [XKB-661] \t/usr/share/xkeyboard-config-2\n"
         "xkbcommon: ERROR: [XKB-661] 3 include paths could not be added:\n"
         "xkbcommon: ERROR: [XKB-661] \t/home/vgpnk/.config/xkb\n"
         "xkbcommon: ERROR: [XKB-661] \t/home/vgpnk/.xkb\n"
         "xkbcommon: ERROR: [XKB-661] \t/etc/xkb\n"
         "xkbcommon: ERROR: [XKB-338] Couldn't process include statement for 'zz'"),
        ("sub", "receipt", "[XKB-661] Couldn't process include statement for 'br(nope)'",
         "[XKB-338] Couldn't process include statement for 'br(nope)'"),
    ],
    "M3b_receipt_rc_change": [
        ("sub", "receipt", "ERROR: Couldn't create xkb keymap\nrc=1\n\n"
         "--- unknown variant on a known layout",
         "ERROR: Couldn't create xkb keymap\nrc=0\n\n"
         "--- unknown variant on a known layout"),
    ],
    "M3c_receipt_probe_name_swap": [
        ("sub", "receipt", "[XKB-661] Couldn't process include statement for 'br(nope)'",
         "[XKB-661] Couldn't process include statement for 'br(caps)'"),
    ],
    "M3d_receipt_diag_text_swap": [
        ("sub", "receipt", "[XKB-769] Abandoning symbols file \"(unnamed map)\"\n"
         "xkbcommon: ERROR: Failed to compile xkb_symbols\n"
         "xkbcommon: ERROR: [XKB-822] Failed to compile keymap\n"
         "ERROR: Couldn't create xkb keymap\nrc=1\n\n"
         "--- unknown variant on a known layout",
         "[XKB-769] Abandoning symbols file \"pc\"\n"
         "xkbcommon: ERROR: Failed to compile xkb_symbols\n"
         "xkbcommon: ERROR: [XKB-822] Failed to compile keymap\n"
         "ERROR: Couldn't create xkb keymap\nrc=1\n\n"
         "--- unknown variant on a known layout"),
    ],
    "M4a_remove_obs_statement": [
        ("delline", "entry", "**OBS** S344: `Layout not provided, but variant set to"),
    ],
    "M4b_remove_receipt_statement": [
        ("delline", "entry", "| `--options nope:nope` | XKB-595"),
    ],
    "M4c_remove_step9": [
        ("dline_prefix", "entry", "9. **Which diagnostics are visible.**"),
    ],
    "M2d_registry_locator_shift": [
        ("sub", "registry", "xkbcommon-rules.c:520-527", "xkbcommon-rules.c:500-507"),
    ],
    "M4d_remove_registry_row": [
        ("delline", "registry", "| S344 |"),
    ],
}
TARGET = {"entry": ENTRY, "receipt": RECEIPT, "registry": "corpus/SOURCES.md"}


def apply(blobs, name):
    out = dict(blobs)
    for op in MUT[name]:
        target = TARGET[op[1]]
        text = out[target].decode()
        if op[0] == "sub":
            old, new = op[2], op[3]
            if text.count(old) != 1:
                raise SystemExit("%s: match=%d for %r" % (name, text.count(old), old[:70]))
            text = text.replace(old, new)
        elif op[0] == "delline":
            lines = text.split("\n")
            idx = [k for k, l in enumerate(lines) if op[2] in l]
            if len(idx) != 1:
                raise SystemExit("%s: delline matches=%d" % (name, len(idx)))
            del lines[idx[0]]
            text = "\n".join(lines)
        elif op[0] == "dline_prefix":
            lines = text.split("\n")
            idx = [k for k, l in enumerate(lines) if l.startswith(op[2])]
            if len(idx) != 1:
                raise SystemExit("%s: dline_prefix matches=%d" % (name, len(idx)))
            del lines[idx[0]]
            text = "\n".join(lines)
        else:
            raise SystemExit("bad op %r" % (op,))
        out[target] = text.encode()
    return out


def land(parent, blobs, msg, only=None):
    """Commit the given blobs on top of parent; only= limits to those paths."""
    changes = {p: d for p, d in blobs.items() if only is None or p in only}
    return commit(parent, changes, msg)


base_blobs = overlay()
overlay_rev = land(BASE, base_blobs, "c2-base")
print("base=%s overlay_rev=%s" % (BASE, overlay_rev))
diff = git("diff", "--name-status", BASE, overlay_rev).decode()
open(S + "/overlay-diff.txt", "w").write(diff)

acc = open(S + "/digests.txt", "w")
for path in sorted(base_blobs):
    acc.write("%s %s %d\n" % (hashlib.sha256(base_blobs[path]).hexdigest(),
                              path, len(base_blobs[path])))
acc.close()

print("M0_base_overlay %s" % overlay_rev)
for name in MUT:
    try:
        mutated = apply(base_blobs, name)
    except SystemExit as exc:
        print("APPLY-FAILED %s %s" % (name, exc))
        continue
    rev = land(overlay_rev, mutated, name, only={TARGET[op[1]] for op in MUT[name]})
    print("%s %s" % (name, rev))
    with open(S + "/mutant-" + name + ".diff", "w") as fh:
        for op in MUT[name]:
            fh.write("%s %s\n" % (op[0], TARGET[op[1]]))
            for field in op[2:]:
                fh.write("  %r\n" % (field,))
