#!/usr/bin/env python3
# c2-r98-sources-readback.py -- round-98 C2 counter: SOURCES read-back predicate.
#
# Predicate PRED-C2-r98-v1 (frozen after the round-98 critic findings; the
# gate reports R1/R3/R4/R5/R6 as findings, R2 is a plain-mode note only):
#
#   TARGET_MET iff, at --rev, quality/check-sources-readback.py is the frozen
#   candidate (gate_pin=ok), its --selftest is green (checks=N failed=0,
#   N >= 10) with stable finding ids, and
#   (i)  at --base-rev the gate is absent (git cat-file -e
#        <base>:quality/check-sources-readback.py -> absent, printed
#        base_gate=absent) while the counter's own independent status-aware R4
#        pass over the base registry counts base_mismatches, which must equal
#        --expect-base-mismatches (21), and --base-rev must differ from --rev;
#   (ii) at --rev the gate runs on an extracted --rev tree whose
#        corpus/SOURCES.md sha256 equals git show <rev>:corpus/SOURCES.md and
#        reports findings=0 with rows/entries equal to the counter's own parse;
#   (iii) the repair is complete row -> entry: the independent status-aware R4
#        pass over --rev counts 0, every base mismatch's row now names that
#        entry, the entry-path set at --rev equals the base set, each entry's
#        citation set at --rev is a superset of its base set, and the number
#        of used-by paths added at --rev equals repaired;
#   (iv) the gate fails closed on planted defects cut from the --rev
#        registry: one stripped used-by cell -> exactly one R4 naming the
#        planted entry, one path in a recheck cell -> exactly one R1, one
#        dangling used-by -> exactly one R3, one duplicated id -> exactly one
#        R6, one missing row -> exactly one R5, each with the planted id and
#        exit 1, and a committed always-clean stub gate is rejected
#        (stub_flagged=1);
#   (v)  the fleet census still validates the registry
#        (sources-census.sh validate --root FLEET mado, exit 0; W allowed).
#   rc 0 TARGET_MET, 1 TARGET_MISSED, 2 SETUP_ERROR.
#
# The four no-work shapes from the do-nothing control (delete citations,
# delete entries, reword to an acknowledged row, shotgun acknowledgements)
# all score unrepaired through (iii)'s legs; the counter selftest drives the
# same decision body over committed fixtures for each shape.
#
# CLI:
#   c2-r98-sources-readback.py --repo DIR --rev REV --base-rev REV
#                              --expect-gate-sha256 SHA256
#                              --expect-base-mismatches N
#                              [--gate PATH] [--planted-dir DIR]
#                              [--fleet-root DIR] [--scratch-root DIR]
#                              [--json]
#   c2-r98-sources-readback.py --emit-planted DIR [--repo DIR] [--rev REV]
#   c2-r98-sources-readback.py --selftest [--fixtures DIR] [--gate PATH]
#                                 [--scratch-root DIR]
#
# --rev accepts a git rev or the literal "worktree".  For a commit the gate
# runs on a tree extracted with git archive and the registry sha256 is
# checked against git show; for worktree the gate runs on a scratch copy of
# the working corpus and the sha is checked against the file.  --planted-dir
# points at the committed planted copies; when given, every copy must be
# byte-identical to the counter's own transform of the --rev bytes (else
# SETUP_ERROR planted-drift) and the committed stub gate is used; without it
# the transforms are derived at run time.
#
# Instrument status (structural rules): this counter is a harness, not a
# candidate.  It spawns git, the gate (python3 -I) and the fleet census
# (bash); the gate it runs is the submitted candidate and spawns nothing.
# All other code is stdlib only, ASCII only, no network, no ctypes.
#
# The independent read-back below is a deliberately parallel reimplementation
# of the entry->row pass (its own parser, not an import of the gate), so a
# shared parsing bug cannot hide in both.

import argparse
import hashlib
import io
import json
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

PROG = "c2-r98-sources-readback.py"
COUNT_LINE = "MADO_SOURCES_READBACK_COUNT: %s %s"
GATE_REL = "quality/check-sources-readback.py"
REG_REL = "corpus/SOURCES.md"
EMPTY_CELLS = ("", "-", "\u2014")
CHAIN_RE = re.compile(r"(?<![A-Za-z0-9])(S\d{3,}(?:/S\d{3,})+)(?![A-Za-z0-9])")
SOLO_RE = re.compile(r"(?<![A-Za-z0-9/])(S\d{3,})(?![A-Za-z0-9._\-])")
KEY_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*:")
GITENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")

# Planted-defect specs cut from the --rev registry/entries.  Each transform
# rewrites exactly one cell/line; every other byte is kept.  kind "registry"
# products replace corpus/SOURCES.md; kind "entry" products replace the named
# corpus/knowledge/*.md file.
PLANTED = [
    {"short": "r1", "file": "SOURCES-r1-path-in-recheck.md", "kind": "registry",
     "spec": ("recheck-path", "S511",
              "corpus/knowledge/mime-magic-sniff-r95.md"),
     "rule": "R1", "id": "S511",
     "detail": "recheck=corpus/knowledge/mime-magic-sniff-r95.md"},
    {"short": "r3", "file": "SOURCES-r3-dangling-usedby.md", "kind": "registry",
     "spec": ("append-usedby", "S132",
              "corpus/knowledge/readback-planted-dangling-r98.md"),
     "rule": "R3", "id": "S132",
     "detail": "path=corpus/knowledge/readback-planted-dangling-r98.md"},
    {"short": "r4", "file": "SOURCES-r4-stripped-usedby.md", "kind": "registry",
     "spec": ("strip-usedby", "S484"),
     "rule": "R4", "id": "S484",
     "detail": "entry=corpus/knowledge/bar-footprint-surface-band-r83.md"},
    {"short": "r5",
     "file": "KNOWLEDGE-r5-phantom-id-mako-fields-containment-r88.md",
     "kind": "entry",
     "spec": ("append-entry-id",
              "corpus/knowledge/mako-fields-containment-r88.md", "S999"),
     "rule": "R5", "id": "S999",
     "detail": "entry=corpus/knowledge/mako-fields-containment-r88.md"},
    {"short": "r6", "file": "SOURCES-r6-duplicate-row.md", "kind": "registry",
     "spec": ("duplicate-row", "S511"),
     "rule": "R6", "id": "S511", "detail": "count=2"},
]
# Same transforms at fixture scale, for --selftest over committed fixtures.
FIXTURE_SPECS = [
    {"file": "SOURCES-r4-stripped-usedby.md", "kind": "registry",
     "spec": ("strip-usedby", "S001"), "rule": "R4", "id": "S001",
     "detail": "entry=corpus/knowledge/alpha.md"},
    {"file": "SOURCES-r1-path-in-recheck.md", "kind": "registry",
     "spec": ("recheck-path", "S001", "corpus/knowledge/alpha.md"),
     "rule": "R1", "id": "S001",
     "detail": "recheck=corpus/knowledge/alpha.md"},
    {"file": "SOURCES-r3-dangling-usedby.md", "kind": "registry",
     "spec": ("append-usedby", "S001",
              "corpus/knowledge/ghost-missing.md"),
     "rule": "R3", "id": "S001",
     "detail": "path=corpus/knowledge/ghost-missing.md"},
    {"file": "KNOWLEDGE-r5-phantom-id-alpha.md", "kind": "entry",
     "spec": ("append-entry-id", "corpus/knowledge/alpha.md", "S999"),
     "rule": "R5", "id": "S999",
     "detail": "entry=corpus/knowledge/alpha.md"},
    {"file": "SOURCES-r6-duplicate-row.md", "kind": "registry",
     "spec": ("duplicate-row", "S001"), "rule": "R6", "id": "S001",
     "detail": "count=2"},
]

STUB_SOURCE = (
    "#!/usr/bin/env python3\n"
    "import json, sys\n"
    "# always-clean stub gate (counter control): claims findings=0 for any\n"
    "# input; the planted-defect legs must reject it (stub_flagged=1).\n"
    "if \"--json\" in sys.argv:\n"
    "    print(json.dumps({\"rows\": 1, \"entries\": 1, \"findings\": []}))\n"
    "else:\n"
    "    print(\"SOURCES_READBACK: rows=1 entries=1 findings=0\")\n"
    "sys.exit(0)\n"
)


class SetupError(Exception):
    pass


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def is_separator(cells):
    return all(c and set(c) <= set("-:") for c in cells)


def usedby_members(cell):
    c = cell.strip()
    if c in EMPTY_CELLS:
        return []
    return [posixpath.normpath(m.strip()) for m in c.split(",") if m.strip()]


def token_ids(text):
    out = []
    spans = []
    for m in CHAIN_RE.finditer(text):
        out.extend(m.group(1).split("/"))
        spans.append(m.span())
    for m in SOLO_RE.finditer(text):
        if any(a <= m.start() < b for a, b in spans):
            continue
        out.append(m.group(1))
    return out


def block_ids(text):
    ids = []
    started = False
    in_block = False
    for raw in text.splitlines():
        if not started:
            if raw.startswith("source:"):
                started = True
                in_block = True
                ids.extend(token_ids(raw[len("source:"):]))
            continue
        if not in_block:
            continue
        stripped = raw.strip()
        if (stripped == "" or raw.startswith("---") or raw.startswith("#")
                or KEY_RE.match(raw)):
            in_block = False
            continue
        ids.extend(token_ids(raw))
    return ids


def registry_rows(text):
    rows = []
    in_reg = False
    for raw in text.splitlines():
        body = raw.lstrip(" ")
        indent = len(raw) - len(body)
        if body.startswith("##") and not body.startswith("###"):
            in_reg = body.strip() == "## Registry"
            continue
        if not in_reg or indent > 3 or not body.startswith("|"):
            continue
        cells = [c.strip() for c in body.strip("|").split("|")]
        if len(cells) != 11 or not cells[0] or cells[0] == "id":
            continue
        if is_separator(cells):
            continue
        rows.append(cells)
    return rows


def readback(reg_text, entries):
    """Independent status-aware pass.

    Returns (r4_pairs, r5_pairs, acked, row_ids, row_count, cites) where
    r4_pairs are (id, entry_path) pairs over rows with status mined, acked
    maps row id -> set of normpath'd used-by members, and cites maps
    normpath'd entry path -> set of cited ids.
    """
    rows = registry_rows(reg_text)
    acked = {}
    row_ids = []
    status = {}
    for cells in rows:
        acked.setdefault(cells[0], set()).update(usedby_members(cells[10]))
        if cells[0] not in status:
            row_ids.append(cells[0])
            status[cells[0]] = cells[7]
    cites = {}
    r4, r5 = [], []
    for rel, text in entries.items():
        ekey = posixpath.normpath(rel)
        ids = block_ids(text)
        cites[ekey] = set(ids)
        for sid in ids:
            if sid not in acked:
                r5.append((sid, rel))
            elif status.get(sid) == "mined" and ekey not in acked[sid]:
                if (sid, ekey) not in r4:
                    r4.append((sid, ekey))
    return r4, r5, acked, row_ids, len(rows), cites


def repair_legs(base_reg, base_entries, rev_reg, rev_entries):
    """The (iii) decision body, shared by measure and --selftest."""
    b4, _, back, bids, bn, bcites = readback(base_reg, base_entries)
    r4, _, rack, rids, rn, rcites = readback(rev_reg, rev_entries)
    repaired = sum(1 for sid, ep in b4 if ep in rack.get(sid, ()))
    added = [(rid, m) for rid in rack
             for m in rack[rid] - back.get(rid, set())]
    superset_bad = [p for p in bcites
                    if not rcites.get(p, set()) >= bcites[p]]
    return {
        "base_pairs": b4,
        "rev_pairs": r4,
        "repaired": repaired,
        "repaired_ok": repaired == len(b4) and not r4,
        "entry_set_ok": set(bcites) == set(rcites),
        "row_set_ok": set(bids) == set(rids),
        "superset_ok": not superset_bad,
        "superset_bad": superset_bad,
        "added_paths": len(added),
        "added_ok": len(added) == repaired,
        "base_rows": bn,
        "rev_rows": rn,
    }


def transform_registry(reg_bytes, spec):
    """Rewrites exactly one cell of exactly one registry row (or duplicates
    one row); every other byte is kept."""
    kind, row_id = spec[0], spec[1]
    text = reg_bytes.decode("utf-8")
    out = []
    hit = False
    in_reg = False
    for line in text.splitlines(keepends=True):
        body = line.rstrip("\r\n")
        eol = line[len(body):]
        stripped = body.lstrip(" ")
        indent = len(body) - len(stripped)
        if stripped.startswith("##") and not stripped.startswith("###"):
            in_reg = stripped.strip() == "## Registry"
            out.append(line)
            continue
        if not hit and in_reg and indent <= 3 and stripped.startswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if (len(cells) == 11 and cells[0] == row_id and cells[0] != "id"
                    and not is_separator(cells)):
                if kind == "strip-usedby":
                    cells[10] = ""
                elif kind == "recheck-path":
                    cells[9] = spec[2]
                elif kind == "append-usedby":
                    cur = cells[10].strip()
                    base = "" if cur in EMPTY_CELLS else cur
                    cells[10] = (base + "," if base else "") + spec[2]
                elif kind == "duplicate-row":
                    out.append(line)
                    out.append("| " + " | ".join(cells) + " |" + eol)
                    hit = True
                    continue
                else:
                    raise SetupError("transform-kind %s" % kind)
                out.append("| " + " | ".join(cells) + " |" + eol)
                hit = True
                continue
        out.append(line)
    if not hit:
        raise SetupError("transform-row-not-found %s" % row_id)
    return "".join(out).encode("utf-8")


def transform_entry(entry_bytes, spec):
    """append-entry-id: appends " <id>" to the entry's first source: line."""
    kind, rel, sid = spec[0], spec[1], spec[2]
    if kind != "append-entry-id":
        raise SetupError("transform-kind %s" % kind)
    text = entry_bytes.decode("utf-8")
    out = []
    hit = False
    for line in text.splitlines(keepends=True):
        if not hit and line.startswith("source:"):
            body = line.rstrip("\r\n")
            out.append(body + " " + sid + line[len(body):])
            hit = True
            continue
        out.append(line)
    if not hit:
        raise SetupError("transform-source-line-not-found %s" % rel)
    return "".join(out).encode("utf-8")


def planted_products(reg_bytes, entries_map, specs):
    """[(corpus_rel_path, bytes)] for each planted spec."""
    products = []
    for ps in specs:
        if ps["kind"] == "registry":
            products.append(("SOURCES.md", transform_registry(reg_bytes,
                                                              ps["spec"])))
        else:
            rel = ps["spec"][1]
            data = entries_map[rel]
            products.append((posixpath.relpath(rel, "corpus"),
                             transform_entry(data, ps["spec"])))
    return products


# ------------------------------------------------------------------ git io ---
def git_run(repo, argv, must=True):
    p = subprocess.run(["git", "-C", repo] + argv, env=GITENV,
                       capture_output=True)
    if must and p.returncode != 0:
        raise SetupError("git-failed %s: %s"
                         % (" ".join(argv),
                            p.stderr.decode("utf-8", "replace").strip()[:200]))
    return p


def git_read(repo, rev, rel):
    p = git_run(repo, ["show", "%s:%s" % (rev, rel)], must=False)
    if p.returncode != 0:
        return None
    return p.stdout


def git_exists(repo, rev, rel):
    return git_run(repo, ["cat-file", "-e", "%s:%s" % (rev, rel)],
                   must=False).returncode == 0


def git_knowledge_entries(repo, rev):
    p = git_run(repo, ["ls-tree", "-r", "--name-only", rev,
                       "--", "corpus/knowledge"])
    out = {}
    for line in p.stdout.decode("utf-8", "replace").splitlines():
        rel = line.strip()
        if rel.endswith(".md"):
            data = git_read(repo, rev, rel)
            if data is None:
                raise SetupError("git-entry-missing %s" % rel)
            out[rel] = data.decode("utf-8", "replace")
    return out


def disk_knowledge(tree):
    kdir = os.path.join(tree, "corpus", "knowledge")
    if not os.path.isdir(kdir):
        raise SetupError("missing-entry-dir %s" % kdir)
    out = {}
    for name in sorted(os.listdir(kdir)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(kdir, name)
        if not os.path.isfile(path):
            continue
        try:
            with open(path, "rb") as fh:
                out["corpus/knowledge/" + name] = fh.read().decode("utf-8")
        except (OSError, UnicodeDecodeError):
            raise SetupError("unreadable-entry corpus/knowledge/" + name)
    return out


def read_bytes(path):
    try:
        with open(path, "rb") as fh:
            return fh.read()
    except OSError as exc:
        raise SetupError("unreadable %s" % path)


# --------------------------------------------------------------- gate run ----
def run_gate(gate_path, repo_dir, cwd):
    p = subprocess.run([sys.executable, "-I", gate_path,
                        "--repo", repo_dir, "--json"],
                       capture_output=True, cwd=cwd)
    obj = None
    for line in p.stdout.decode("utf-8", "replace").splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                obj = json.loads(line)
            except ValueError:
                obj = None
    return p.returncode, obj, p.stdout.decode("utf-8", "replace"), \
        p.stderr.decode("utf-8", "replace")


def gate_selftest_leg(gate_path, cwd):
    """Runs the gate's --selftest; returns (ok, checks, failed)."""
    p = subprocess.run([sys.executable, "-I", gate_path, "--selftest"],
                       capture_output=True, cwd=cwd)
    n = m = -1
    for line in p.stdout.decode("utf-8", "replace").splitlines():
        if line.startswith("SOURCES_READBACK_SELFTEST:"):
            parts = line.split()
            for i, tok in enumerate(parts):
                if tok.startswith("checks="):
                    n = int(tok[len("checks="):])
                if tok.startswith("failed="):
                    m = int(tok[len("failed="):])
    ok = p.returncode == 0 and m == 0 and n >= 10
    return ok, n, m


def one_planted(obj, rule, pid, detail):
    return (obj is not None and len(obj.get("findings", [])) == 1
            and obj["findings"][0].get("rule") == rule
            and obj["findings"][0].get("id") == pid
            and obj["findings"][0].get("detail") == detail)


def build_planted_tree(base_tree, products, scratch, name):
    dest = os.path.join(scratch, "planted-" + name)
    shutil.copytree(os.path.join(base_tree, "corpus"),
                    os.path.join(dest, "corpus"))
    for rel, data in products:
        with open(os.path.join(dest, "corpus", rel), "wb") as fh:
            fh.write(data)
    return dest


def resolve_rev_tree(repo, rev, scratch):
    """Extracted --rev tree; returns (tree, registry_bytes, pin_state)."""
    dest = os.path.join(scratch, "revtree")
    if rev == "worktree":
        src = os.path.join(repo, "corpus")
        if not os.path.isfile(os.path.join(src, "SOURCES.md")):
            raise SetupError("missing-registry %s"
                             % os.path.join(src, "SOURCES.md"))
        shutil.copytree(src, os.path.join(dest, "corpus"))
    else:
        os.makedirs(os.path.join(dest, "corpus"), exist_ok=True)
        p = subprocess.run(["git", "-C", repo, "archive", "--format=tar",
                            rev, "corpus"], env=GITENV, capture_output=True)
        if p.returncode != 0:
            raise SetupError("git-archive-failed %s" % rev)
        with tarfile.open(fileobj=io.BytesIO(p.stdout)) as tf:
            tf.extractall(dest)
    reg = read_bytes(os.path.join(dest, REG_REL))
    if rev == "worktree":
        want = reg  # the copy must equal the file it was copied from
        pin = "worktree-copy"
    else:
        want = git_read(repo, rev, REG_REL)
        if want is None:
            raise SetupError("registry-missing-at-rev %s" % REG_REL)
        pin = "git-show"
    if sha256(reg) != sha256(want):
        raise SetupError("rev-tree-pin corpus/SOURCES.md sha mismatch")
    return dest, reg, pin


def resolve_gate(args, repo, rev, scratch):
    if args.gate:
        data = read_bytes(args.gate)
        pinned = os.path.join(scratch, "gate.py")
        with open(pinned, "wb") as fh:
            fh.write(data)
        return data, pinned
    if rev == "worktree":
        path = os.path.join(repo, GATE_REL)
        if not os.path.isfile(path):
            raise SetupError("gate-absent %s" % path)
        return read_bytes(path), path
    data = git_read(repo, rev, GATE_REL)
    if data is None:
        raise SetupError("gate-absent-at-rev %s" % GATE_REL)
    pinned = os.path.join(scratch, "gate.py")
    with open(pinned, "wb") as fh:
        fh.write(data)
    return data, pinned


# ------------------------------------------------------------ measurement ----
def measure(args, out):
    repo = os.path.abspath(args.repo)
    if not os.path.isdir(repo):
        raise SetupError("repo-not-a-dir %s" % repo)
    if args.base_rev == args.rev:
        raise SetupError("--base-rev equals --rev")
    scratch = args.scratch_root or tempfile.mkdtemp(prefix="c2-readback-r98-")
    os.makedirs(scratch, exist_ok=True)
    facts = {}
    problems = []

    def emit(line):
        out.write(line + "\n")

    # -- (i) base leg ------------------------------------------------------
    base = args.base_rev
    emit("base_rev=%s" % base)
    if git_exists(repo, base, GATE_REL):
        emit("base_gate=present")
        problems.append("base_gate=present")
    else:
        emit("base_gate=absent")
    base_reg_b = git_read(repo, base, REG_REL)
    if base_reg_b is None:
        raise SetupError("base-registry-missing %s" % REG_REL)
    base_entries = git_knowledge_entries(repo, base)
    legs = repair_legs(base_reg_b.decode("utf-8"), base_entries,
                       base_reg_b.decode("utf-8"), base_entries)
    facts["base_mismatches"] = len(legs["base_pairs"])
    match = facts["base_mismatches"] == args.expect_base_mismatches
    emit("base_mismatches=%d expect=%d match=%s"
         % (facts["base_mismatches"], args.expect_base_mismatches,
            "ok" if match else "MISMATCH"))
    for sid, ep in legs["base_pairs"]:
        emit("BASE_MISMATCH %s %s" % (sid, ep))
    if not match:
        problems.append("base_mismatches=%d expect=%d"
                        % (facts["base_mismatches"],
                           args.expect_base_mismatches))

    # -- (ii) rev leg: pin + extracted tree + gate run ----------------------
    rev = args.rev
    emit("rev=%s" % rev)
    gate_bytes, gate_path = resolve_gate(args, repo, rev, scratch)
    emit("gate_source=%s" % gate_path)
    if sha256(gate_bytes) != args.expect_gate_sha256.lower():
        emit("gate_pin=mismatch")
        problems.append("gate_pin=mismatch")
    else:
        emit("gate_pin=ok")
    tree, reg_bytes, pin = resolve_rev_tree(repo, rev, scratch)
    emit("rev_registry_sha256=%s" % sha256(reg_bytes))
    emit("rev_tree_pin=%s" % pin)
    reg_text = reg_bytes.decode("utf-8")
    tree_entries = disk_knowledge(tree)
    own_r4, own_r5, _, _, own_rows, _ = readback(reg_text, tree_entries)
    gok, gn, gm = gate_selftest_leg(gate_path, scratch)
    emit("gate_selftest=%s checks=%d failed=%d"
         % ("ok" if gok else "FAIL", gn, gm))
    if not gok:
        problems.append("gate_selftest checks=%d failed=%d" % (gn, gm))
    grc, gobj, _, gerr = run_gate(gate_path, tree, scratch)
    if gobj is None:
        raise SetupError("gate-run-failed rc=%d %s" % (grc, gerr.strip()[:200]))
    gfind = gobj.get("findings", [])
    emit("gate_findings=%d rows=%d entries=%d gate_rc=%d"
         % (len(gfind), gobj.get("rows", -1), gobj.get("entries", -1), grc))
    rows_ok = gobj.get("rows") == own_rows
    entries_ok = gobj.get("entries") == len(tree_entries)
    emit("rows_match=%s" % ("ok" if rows_ok else "mismatch want=%d" % own_rows))
    emit("entries_match=%s" % ("ok" if entries_ok else
                               "mismatch want=%d" % len(tree_entries)))
    if gfind:
        problems.append("gate_findings=%d" % len(gfind))
    if not rows_ok:
        problems.append("rows_match")
    if not entries_ok:
        problems.append("entries_match")

    # -- (iii) repair legs (row -> entry) -----------------------------------
    legs = repair_legs(base_reg_b.decode("utf-8"), base_entries,
                       reg_text, tree_entries)
    facts.update({k: v for k, v in legs.items() if k != "base_pairs"})
    emit("rev_mismatches=%d" % len(legs["rev_pairs"]))
    if legs["rev_pairs"]:
        problems.append("rev_mismatches=%d" % len(legs["rev_pairs"]))
    emit("entry_set=%s" % ("ok" if legs["entry_set_ok"] else "CHANGED"))
    if not legs["entry_set_ok"]:
        problems.append("entry_set")
    emit("row_set=%s" % ("ok" if legs["row_set_ok"] else "CHANGED"))
    if not legs["row_set_ok"]:
        problems.append("row_set")
    emit("citations_superset=%s" % ("ok" if legs["superset_ok"] else
                                    "BROKEN first=%s"
                                    % ",".join(legs["superset_bad"][:3])))
    if not legs["superset_ok"]:
        problems.append("citations_superset")
    emit("added_paths=%d" % legs["added_paths"])
    emit("added_paths_match=%s" % ("ok" if legs["added_ok"] else
                                   "MISMATCH want=%d" % legs["repaired"]))
    if not legs["added_ok"]:
        problems.append("added_paths=%d want=%d"
                        % (legs["added_paths"], legs["repaired"]))
    emit("repaired=%d/%d" % (legs["repaired"], len(legs["base_pairs"])))
    if not legs["repaired_ok"]:
        problems.append("repaired=%d/%d"
                        % (legs["repaired"], len(legs["base_pairs"])))

    # -- (iv) planted defects + committed stub ------------------------------
    planted_dir = args.planted_dir
    stub_path = None
    if planted_dir:
        entries_map = {}
        for rel, text in tree_entries.items():
            entries_map[rel] = text.encode("utf-8")
        for ps in PLANTED:
            want = os.path.join(planted_dir, ps["file"])
            if not os.path.isfile(want):
                raise SetupError("planted-missing %s" % want)
            got = planted_products(reg_bytes, entries_map, [ps])[0][1]
            if read_bytes(want) != got:
                raise SetupError("planted-drift %s" % ps["file"])
        emit("planted_sync=ok")
        committed_stub = os.path.join(planted_dir,
                                      "stub-always-clean-gate.py")
        if os.path.isfile(committed_stub):
            stub_path = os.path.join(scratch, "stub_gate.py")
            with open(stub_path, "wb") as fh:
                fh.write(read_bytes(committed_stub))
            emit("stub_source=%s" % committed_stub)
    else:
        emit("planted_sync=derived")
    if stub_path is None:
        stub_path = os.path.join(scratch, "stub_gate.py")
        with open(stub_path, "w", encoding="utf-8") as fh:
            fh.write(STUB_SOURCE)
        emit("stub_source=derived")
    products_ok = 0
    planted_by_short = {}
    for ps in PLANTED:
        prod = planted_products(reg_bytes, {rel: text.encode("utf-8")
                                            for rel, text
                                            in tree_entries.items()},
                                [ps])
        ptree = build_planted_tree(tree, prod, scratch, ps["short"])
        planted_by_short[ps["short"]] = ptree
        prc, pobj, _, perr = run_gate(gate_path, ptree, scratch)
        ok = prc == 1 and one_planted(pobj, ps["rule"], ps["id"],
                                      ps["detail"])
        products_ok += 1 if ok else 0
        emit("planted_%s=%s" % (ps["short"], "ok" if ok else
                                "FAIL rc=%d out=%s" % (prc,
                                                       perr.strip()[:80])))
    emit("planted=%d/5" % products_ok)
    if products_ok != 5:
        problems.append("planted=%d/5" % products_ok)
    src, sobj, _, _ = run_gate(stub_path, planted_by_short["r4"], scratch)
    stub_caught = not (src == 1 and sobj is not None
                       and len(sobj.get("findings", [])) == 1)
    emit("stub_flagged=%d" % (1 if stub_caught else 0))
    if not stub_caught:
        problems.append("stub_flagged=0")

    # -- (v) fleet census ---------------------------------------------------
    fleet = args.fleet_root
    census = os.path.join(fleet, "scripts", "sources-census.sh")
    if not os.path.isfile(census):
        raise SetupError("census-missing %s" % census)
    crc = subprocess.run(["bash", census, "validate", "--root", fleet,
                          "mado"], capture_output=True, cwd=scratch).returncode
    emit("census=%s" % ("ok" if crc == 0 else "exit=%d" % crc))
    if crc != 0:
        problems.append("census")

    verdict = "TARGET_MET" if not problems else "TARGET_MISSED"
    emit(COUNT_LINE % (verdict, " ".join(problems) if problems
                       else "all-legs-green"))
    facts["verdict"] = verdict
    facts["problems"] = problems
    facts["base_mismatch_list"] = [[s, e] for s, e in legs["base_pairs"]]
    return (0 if not problems else 1), facts


# ------------------------------------------------------------ emit planted ---
def emit_planted(args, out):
    repo = os.path.abspath(args.repo)
    rev = args.rev or "worktree"
    scratch = tempfile.mkdtemp(prefix="c2-readback-r98-emit-")
    _tree, reg_bytes, _pin = resolve_rev_tree(repo, rev, scratch)
    if rev == "worktree":
        entries_map = disk_knowledge(_tree)
        entries_map = {rel: text.encode("utf-8")
                       for rel, text in entries_map.items()}
    else:
        entries_map = {rel: data for rel, data
                       in git_knowledge_entries(repo, rev).items()}
    dest = args.emit_planted
    os.makedirs(dest, exist_ok=True)
    for ps, (rel, data) in zip(PLANTED,
                               planted_products(reg_bytes, entries_map,
                                                PLANTED)):
        with open(os.path.join(dest, ps["file"]), "wb") as fh:
            fh.write(data)
    stub = os.path.join(dest, "stub-always-clean-gate.py")
    if not os.path.isfile(stub):
        with open(stub, "w", encoding="utf-8") as fh:
            fh.write(STUB_SOURCE)
    manifest = {
        "schema": "mado-r98-readback-planted-v2",
        "source_registry": REG_REL,
        "source_sha256": sha256(reg_bytes),
        "rev": rev,
        "tool_sha256": sha256(read_bytes(os.path.abspath(sys.argv[0]))),
        "products": [
            {"file": ps["file"], "kind": ps["kind"], "kind_spec": ps["spec"][0],
             "target": ps["spec"][1],
             "payload": ps["spec"][2] if len(ps["spec"]) > 2 else "",
             "expect_rule": ps["rule"], "expect_id": ps["id"],
             "expect_detail": ps["detail"]}
            for ps in PLANTED
        ],
        "stub": "stub-always-clean-gate.py",
    }
    with open(os.path.join(dest, "manifest.json"), "w",
              encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=1, sort_keys=True)
        fh.write("\n")
    out.write("MADO_SOURCES_READBACK_PLANTED: wrote=%d dir=%s source_sha256=%s\n"
              % (len(PLANTED), dest, manifest["source_sha256"]))
    return 0


def transform_matches(reg_bytes, entries_map, ps, data):
    if ps["kind"] == "registry":
        return transform_registry(reg_bytes, ps["spec"]) == data
    return transform_entry(entries_map[ps["spec"][1]], ps["spec"]) == data


# ---------------------------------------------------------------- selftest ---
def find_path(candidates, want_file=True):
    for c in candidates:
        if c and (os.path.isfile(c) if want_file else os.path.isdir(c)):
            return c
    return None


def discover_fixtures(args):
    if args.fixtures:
        return args.fixtures if os.path.isdir(args.fixtures) else None
    here = os.path.dirname(os.path.abspath(__file__))
    return find_path([
        os.path.join(here, "..", "selftest-fixtures", "readback"),
        os.path.join(here, "..", "..", ".ufo", "waves", "round-98",
                     "selftest-fixtures", "readback"),
        os.path.join(os.path.abspath(args.repo), ".ufo", "waves", "round-98",
                     "selftest-fixtures", "readback") if args.repo else None,
    ], want_file=False)


def discover_gate(args, repo):
    if args.gate:
        return args.gate if os.path.isfile(args.gate) else None
    here = os.path.dirname(os.path.abspath(__file__))
    return find_path([
        os.path.join(here, "check-sources-readback.py"),
        os.path.join(here, "..", "check-sources-readback.py"),
        os.path.join(repo, GATE_REL),
    ])


def counter_selftest(args, out):
    scratch = args.scratch_root or tempfile.mkdtemp(prefix="c2-readback-r98-st-")
    os.makedirs(scratch, exist_ok=True)
    checks = []
    state = {}

    def check(cid):
        def deco(fn):
            checks.append((cid, fn))
            return fn
        return deco

    fx = discover_fixtures(args)
    gate = discover_gate(args, os.path.abspath(args.repo))
    failed = []
    if fx is None:
        out.write("MADO_COUNTER_SELFTEST_FAIL: fixtures-missing\n")
        out.write("MADO_COUNTER_SELFTEST: checks=0 failed=1 detail="
                  "could-not-evaluate\n")
        return 2
    if gate is None:
        out.write("MADO_COUNTER_SELFTEST_FAIL: gate-missing\n")
        out.write("MADO_COUNTER_SELFTEST: checks=0 failed=1 detail="
                  "could-not-evaluate\n")
        return 2

    clean_reg = read_bytes(os.path.join(fx, "clean", REG_REL))
    clean_entries = disk_knowledge(os.path.join(fx, "clean"))

    def variant(name):
        root = os.path.join(fx, "basepair", name)
        reg = read_bytes(os.path.join(root, REG_REL)).decode("utf-8")
        ents = disk_knowledge(root)
        return reg, ents

    @check("ct01-gate-clean-exit0")
    def _():
        rc, obj, _, err = run_gate(gate, os.path.join(fx, "clean"), scratch)
        assert rc == 0 and obj is not None, (rc, obj, err)
        assert obj["findings"] == [], obj
        state["clean_obj"] = obj

    @check("ct02-gate-r4-exit1-stable-id")
    def _():
        rc, obj, _, err = run_gate(gate, os.path.join(fx, "r4"), scratch)
        assert rc == 1, (rc, obj, err)
        assert obj["findings"] == [
            {"rule": "R4", "id": "S001",
             "detail": "entry=corpus/knowledge/alpha.md"}], obj

    @check("ct03-gate-r1-exit1-stable-id")
    def _():
        rc, obj, _, err = run_gate(gate, os.path.join(fx, "r1"), scratch)
        assert rc == 1, (rc, obj, err)
        assert obj["findings"] == [
            {"rule": "R1", "id": "S001",
             "detail": "recheck=corpus/knowledge/alpha.md"}], obj

    @check("ct04-gate-r3-exit1-stable-id")
    def _():
        rc, obj, _, err = run_gate(gate, os.path.join(fx, "r3"), scratch)
        assert rc == 1, (rc, obj, err)
        assert obj["findings"] == [
            {"rule": "R3", "id": "S001",
             "detail": "path=corpus/knowledge/ghost-missing.md"}], obj

    @check("ct05-planted-derivation-byte-stable")
    def _():
        for ps in FIXTURE_SPECS:
            want = read_bytes(os.path.join(fx, "planted", ps["file"]))
            if ps["kind"] == "registry":
                got = transform_registry(clean_reg, ps["spec"])
            else:
                got = transform_entry(
                    clean_entries[ps["spec"][1]].encode("utf-8"), ps["spec"])
            assert want == got, ps["file"]

    @check("ct06-planted-legs-fixture-scale")
    def _():
        emap = {rel: text.encode("utf-8")
                for rel, text in clean_entries.items()}
        for ps in FIXTURE_SPECS:
            prod = planted_products(clean_reg, emap, [ps])
            ptree = build_planted_tree(os.path.join(fx, "clean"), prod,
                                       scratch,
                                       "fx-" + ps["file"].rsplit(".", 1)[0])
            prc, pobj, _, perr = run_gate(gate, ptree, scratch)
            assert prc == 1, (ps["file"], prc, pobj, perr)
            assert one_planted(pobj, ps["rule"], ps["id"], ps["detail"]), \
                (ps["file"], pobj)

    @check("ct07-always-clean-stub-rejected")
    def _():
        stub = os.path.join(scratch, "stub_gate.py")
        with open(stub, "w", encoding="utf-8") as fh:
            fh.write(STUB_SOURCE)
        emap = {rel: text.encode("utf-8")
                for rel, text in clean_entries.items()}
        prod = planted_products(clean_reg, emap, [FIXTURE_SPECS[0]])
        ptree = build_planted_tree(os.path.join(fx, "clean"), prod,
                                   scratch, "fx-stub")
        rc, obj, _, _ = run_gate(stub, ptree, scratch)
        assert not (rc == 1 and obj is not None
                    and len(obj.get("findings", [])) == 1), (rc, obj)

    @check("ct08-basepair-mismatch-and-repair-count")
    def _():
        base_reg = read_bytes(os.path.join(fx, "basepair", "base",
                                           REG_REL)).decode("utf-8")
        base_ents = disk_knowledge(os.path.join(fx, "basepair", "base"))
        rev_reg = read_bytes(os.path.join(fx, "basepair", "rev",
                                          REG_REL)).decode("utf-8")
        rev_ents = disk_knowledge(os.path.join(fx, "basepair", "rev"))
        legs = repair_legs(base_reg, base_ents, rev_reg, rev_ents)
        assert len(legs["base_pairs"]) == 2, legs["base_pairs"]
        assert not legs["rev_pairs"], legs["rev_pairs"]
        assert legs["repaired"] == 2, legs
        assert legs["entry_set_ok"] and legs["row_set_ok"], legs
        assert legs["superset_ok"], legs
        assert legs["added_paths"] == 2 and legs["added_ok"], legs

    @check("ct09-gate-setup-exit2")
    def _():
        empty = os.path.join(scratch, "empty")
        os.makedirs(empty, exist_ok=True)
        rc, obj, _, err = run_gate(gate, empty, scratch)
        assert rc == 2, (rc, obj, err)

    @check("ct10-rows-entries-agreement")
    def _():
        rows = registry_rows(clean_reg.decode("utf-8"))
        obj = state["clean_obj"]
        assert obj["rows"] == len(rows), (obj["rows"], len(rows))
        assert obj["entries"] == len(clean_entries), (obj["entries"],
                                                      len(clean_entries))

    @check("ct11-gate-yaml-list-shape")
    def _():
        rc, obj, _, err = run_gate(gate, os.path.join(fx, "shapes", "yaml"),
                                   scratch)
        assert rc == 1 and obj is not None, (rc, obj, err)
        assert obj["findings"] == [
            {"rule": "R4", "id": "S002",
             "detail": "entry=corpus/knowledge/alpha-yaml.md"}], obj

    @check("ct12-gate-wrapped-line-shape")
    def _():
        rc, obj, _, err = run_gate(gate, os.path.join(fx, "shapes", "wrapped"),
                                   scratch)
        assert rc == 1 and obj is not None, (rc, obj, err)
        assert obj["findings"] == [
            {"rule": "R4", "id": "S002",
             "detail": "entry=corpus/knowledge/alpha-wrap.md"}], obj

    @check("ct13-gate-path-token-shape")
    def _():
        rc, obj, _, err = run_gate(gate,
                                   os.path.join(fx, "shapes", "pathtoken"),
                                   scratch)
        assert rc == 0 and obj is not None, (rc, obj, err)
        assert obj["findings"] == [], obj

    @check("ct14-nowork-delete-citation-unrepaired")
    def _():
        reg, ents = variant("rev-delete-cite")
        legs = repair_legs(read_bytes(os.path.join(fx, "basepair", "base",
                                                   REG_REL)).decode("utf-8"),
                           disk_knowledge(os.path.join(fx, "basepair",
                                                       "base")),
                           reg, ents)
        assert not legs["superset_ok"], legs

    @check("ct15-nowork-reword-unrepaired")
    def _():
        reg, ents = variant("rev-reword")
        legs = repair_legs(read_bytes(os.path.join(fx, "basepair", "base",
                                                   REG_REL)).decode("utf-8"),
                           disk_knowledge(os.path.join(fx, "basepair",
                                                       "base")),
                           reg, ents)
        assert legs["repaired"] < len(legs["base_pairs"]), legs

    @check("ct16-nowork-shotgun-unrepaired")
    def _():
        reg, ents = variant("rev-shotgun")
        legs = repair_legs(read_bytes(os.path.join(fx, "basepair", "base",
                                                   REG_REL)).decode("utf-8"),
                           disk_knowledge(os.path.join(fx, "basepair",
                                                       "base")),
                           reg, ents)
        assert not legs["added_ok"], legs

    @check("ct17-nowork-delete-entry-unrepaired")
    def _():
        reg, ents = variant("rev-no-beta")
        legs = repair_legs(read_bytes(os.path.join(fx, "basepair", "base",
                                                   REG_REL)).decode("utf-8"),
                           disk_knowledge(os.path.join(fx, "basepair",
                                                       "base")),
                           reg, ents)
        assert not legs["entry_set_ok"], legs

    @check("ct18-gate-selftest-green-leg")
    def _():
        ok, n, m = gate_selftest_leg(gate, scratch)
        assert ok, (n, m)
        assert n >= 10 and m == 0, (n, m)

    for cid, fn in checks:
        try:
            fn()
        except AssertionError as exc:
            failed.append(cid)
            out.write("MADO_COUNTER_SELFTEST_FAIL: %s %s\n" % (cid, exc))
        except Exception as exc:  # noqa: BLE001 - report and continue
            failed.append(cid)
            out.write("MADO_COUNTER_SELFTEST_FAIL: %s %r\n" % (cid, exc))
    out.write("MADO_COUNTER_SELFTEST: checks=%d failed=%d\n"
              % (len(checks), len(failed)))
    return 1 if failed else 0


# --------------------------------------------------------------------- main --
def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    ap = argparse.ArgumentParser(prog=PROG)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev")
    ap.add_argument("--base-rev", dest="base_rev")
    ap.add_argument("--expect-gate-sha256", dest="expect_gate_sha256")
    ap.add_argument("--expect-base-mismatches", dest="expect_base_mismatches",
                    type=int)
    ap.add_argument("--gate")
    ap.add_argument("--planted-dir", dest="planted_dir")
    ap.add_argument("--emit-planted", dest="emit_planted")
    ap.add_argument("--fleet-root", dest="fleet_root",
                    default="/home/vgpnk/Projects/shokunin")
    ap.add_argument("--scratch-root", dest="scratch_root")
    ap.add_argument("--fixtures")
    ap.add_argument("--json", action="store_true", dest="as_json")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return counter_selftest(args, sys.stdout)
    if args.emit_planted:
        try:
            return emit_planted(args, sys.stdout)
        except SetupError as exc:
            sys.stderr.write("%s: SETUP_ERROR %s\n" % (PROG, exc))
            return 2
    for req, name in ((args.rev, "--rev"), (args.base_rev, "--base-rev"),
                      (args.expect_gate_sha256, "--expect-gate-sha256"),
                      (args.expect_base_mismatches,
                       "--expect-base-mismatches")):
        if req is None:
            sys.stderr.write("usage: %s --repo DIR --rev REV --base-rev REV "
                             "--expect-gate-sha256 SHA256 "
                             "--expect-base-mismatches N | --emit-planted DIR"
                             " | --selftest\n" % PROG)
            return 2
    if not re.fullmatch(r"[0-9a-fA-F]{64}", args.expect_gate_sha256):
        sys.stderr.write("%s: SETUP_ERROR --expect-gate-sha256 not sha256\n"
                         % PROG)
        return 2
    try:
        if args.as_json:
            buf = io.StringIO()
            rc, facts = measure(args, buf)
            facts["rc"] = rc
            sys.stdout.write(json.dumps(facts, sort_keys=True,
                                        default=list) + "\n")
            return rc
        rc, _ = measure(args, sys.stdout)
        return rc
    except SetupError as exc:
        sys.stdout.write(COUNT_LINE % ("SETUP_ERROR", str(exc)))
        sys.stdout.write("\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
