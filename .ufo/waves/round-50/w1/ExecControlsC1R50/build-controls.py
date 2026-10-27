#!/usr/bin/env python3
"""Section-9 do-nothing control bundle for the mado round-50 C1 counter (PRED-C1-r50).

Builds one scratch clone per control, holds the control at the *counter's own declared paths*
(for the frozen round-50 counter those are the round-50 paths: ENTRY under corpus/knowledge,
pins under .ufo/waves/round-50/fetch/, receipts under .ufo/waves/round-50/receipts/, lesson
corpus/lessons/round-50.md), commits it, and scores that commit with the counter. The
counter's path constants are read from its source, so the same bundle works unchanged on the
round-49 counter (c2-r49-bind-entry.py, whose ENTRY/FETCH/RECEIPTS/LESSON are the round-49
ones) and on the frozen round-50 port.

    build-controls.py --counter PATH --repo LANE --rev REV --work DIR [--base BASE]
                      [--only NAME[,NAME...]] [--logdir DIR] [--keep] [--timeout SECS]

Controls (one line of output each: name, final counter line, exit):

    BASE         nothing added (empty commit): the do-nothing case.
    STUB         an entry with a valid provenance head (three real registry ids,
                 verified-at, recheck) and one sentence.
    HELD         corpus/knowledge/keybind-rule-semantics.md section 2.3 pasted under a
                 provenance head with real registry ids: held text, no new ground.
    OLDPATHS     the round-49 candidate entry, rows and receipt unchanged, left at the
                 round-49 paths (corpus/knowledge/hyprland-bind-key-match-r49.md and
                 .ufo/waves/round-49/receipts/), so a counter that names round-50 paths
                 does not see them. On the round-49 counter those are its own paths.
    NOLIVE       the same candidate held at the counter's declared paths, minus the live
                 receipt (file removed, entry line kept).
    NOROWS       the same candidate at the counter's paths, minus the registry rows.
    FORGEDQUOTE  the same candidate with one step quote altered by one word.
    BRANCHURL    the same candidate with one row URL's ref replaced by `main`.

Nothing in the lane is written: every clone is made with `git clone --shared` from LANE into
WORK, the control is committed there under a throwaway identity, and the counter is run with
HOME/XDG_* under WORK and TMPDIR=WORK/tmp. A WORK dir under /tmp, /var/tmp or /dev/shm, or
inside LANE, is refused. Exit 0 iff every control scored TARGET_MISSED with exit 1; 1 if any
control was admitted; 2 if a control run was a setup failure or left no final line.
"""
import argparse
import ast
import hashlib
import os
import re
import shutil
import subprocess
import sys

CONTROLS = ("BASE", "STUB", "HELD", "OLDPATHS", "NOLIVE", "NOROWS",
            "FORGEDQUOTE", "BRANCHURL")
R50 = {
    "ENTRY": "corpus/knowledge/hyprland-bind-key-match-r50.md",
    "REGISTRY": "corpus/SOURCES.md",
    "README": "corpus/README.md",
    "LESSON": "corpus/lessons/round-50.md",
    "FETCH": ".ufo/waves/round-50/fetch/",
    "HELD_FETCH": ".ufo/waves/round-46/fetch/",
    "RECEIPTS": ".ufo/waves/round-50/receipts/",
}
CAND_ENTRY = ".ufo/waves/round-49/candidate/hyprland-bind-key-match-r49.md"
CAND_ROWS = ".ufo/waves/round-49/candidate/rows.md"
R49_RECEIPT = ".ufo/waves/round-49/receipts/binds-live-r49.txt"
ENTRY_R49 = "corpus/knowledge/hyprland-bind-key-match-r49.md"
RECEIPTS_R49 = ".ufo/waves/round-49/receipts/"
HELD_DOC = "corpus/knowledge/keybind-rule-semantics.md"
HELD_HEAD = "### 2.3 "
ROW_RE = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")
CLAUSE_RE = re.compile(r"clauses=([a-z]:\d+(?: [a-z]:\d+)*)")
BAD_WORK = ("/tmp", "/var/tmp", "/dev/shm")
ENV_GIT = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
GITC = ("-c", "core.hooksPath=/dev/null", "-c", "core.fsmonitor=false",
        "-c", "commit.gpgsign=false")


class Fail(Exception):
    pass


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def display(path):
    """`~` for the home directory: receipts never carry an absolute home path."""
    home = os.path.expanduser("~")
    if path == home or path.startswith(home + os.sep):
        return "~" + path[len(home):]
    return path


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, env=ENV_GIT)


def git_out(repo, *args):
    p = git(repo, *args)
    if p.returncode != 0:
        raise Fail("git %s: %s" % (" ".join(args), p.stderr.decode("utf-8", "replace").strip()))
    return p.stdout


def blob_at(lane, rev, path):
    """bytes of PATH at REV (tracked), else the lane worktree copy, else None."""
    p = git(lane, "show", "%s:%s" % (rev, path))
    if p.returncode == 0:
        return p.stdout
    with_path = os.path.join(lane, path)
    if os.path.isfile(with_path):
        with open(with_path, "rb") as f:
            return f.read()
    return None


def counter_consts(path):
    src = open(path, encoding="utf-8").read()
    out = {}
    for name in tuple(R50) + ("PRED", "BASE_DEFAULT", "MIN_ID", "OPENED", "HELD"):
        m = re.search(r"^%s\s*=\s*(.+)$" % name, src, re.M)
        if not m:
            continue
        try:
            out[name] = ast.literal_eval(m.group(1).strip())
        except (ValueError, SyntaxError):
            pass
    return out


def check_paths(args, lane):
    if not os.path.isfile(args.counter):
        raise Fail("counter not found: %s" % args.counter)
    if not os.path.isdir(lane):
        raise Fail("repo not found: %s" % lane)
    git_out(lane, "rev-parse", "--show-toplevel")
    if not os.path.isabs(args.work):
        raise Fail("--work must be an absolute path")
    work = os.path.realpath(args.work)
    for bad in BAD_WORK:
        if work == bad or work.startswith(bad + os.sep):
            raise Fail("work dir under %s refused: %s" % (bad, display(work)))
    lane_real = os.path.realpath(lane)
    if work == lane_real or work.startswith(lane_real + os.sep):
        raise Fail("work dir inside the scored repo refused: %s" % display(work))
    os.makedirs(work, exist_ok=True)
    return work


def control_env(work):
    env = dict(os.environ)
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(key, None)
    for key in ("HOME", "XDG_CONFIG_HOME", "XDG_CACHE_HOME", "XDG_DATA_HOME", "XDG_STATE_HOME"):
        p = os.path.join(work, "home", key.lower())
        os.makedirs(p, exist_ok=True)
        env[key] = p
    env["TMPDIR"] = os.path.join(work, "tmp")
    os.makedirs(env["TMPDIR"], exist_ok=True)
    return env


def put(clone, rel, data):
    base = os.path.realpath(clone)
    p = os.path.realpath(os.path.join(base, rel))
    if not p.startswith(base + os.sep):
        raise Fail("control path escapes its clone: %s" % rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as f:
        f.write(data if isinstance(data, bytes) else data.encode("utf-8"))


def drop(clone, rel):
    p = os.path.join(os.path.realpath(clone), rel)
    if os.path.isfile(p):
        os.remove(p)


def registry_ids(text):
    out = []
    for line in text.split("\n"):
        m = ROW_RE.match(line)
        if m and m.group(1) not in out:
            out.append(m.group(1))
    return out


def append_rows(text, rows_text):
    lines = text.split("\n")
    try:
        start = next(i for i, l in enumerate(lines) if l.strip() == "## Registry")
    except StopIteration:
        raise Fail("registry has no `## Registry` section")
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")),
               len(lines))
    last = start
    for i in range(start + 1, end):
        if ROW_RE.match(lines[i]):
            last = i
    rows = [r.rstrip("\r") for r in rows_text.split("\n") if r.strip()]
    if last == start:
        rows = [""] + rows
    lines[last + 1:last + 1] = rows
    return "\n".join(lines)


def held_section(text):
    lines = text.split("\n")
    start = next((i for i, l in enumerate(lines) if l.startswith(HELD_HEAD)), None)
    if start is None:
        raise Fail("held document has no section 2.3")
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("### ")
                or lines[i].startswith("## ")), len(lines))
    return "\n".join(lines[start:end]).rstrip("\n")


def head_block(ids, opened):
    out = ["source: %s - control fixture reference to an existing registry row" % i
           for i in ids]
    return out + ["verified-at: %s" % opened, "recheck: 30d", ""]


def insert_gate(text, block):
    """insert admit lines into the existing `## Gate` section (append it when absent)."""
    lines = text.split("\n")
    start = next((i for i, l in enumerate(lines) if l.strip() == "## Gate"), None)
    if start is None:
        return text.rstrip("\n") + "\n\n## Gate\n\n" + block + "\n"
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")),
               len(lines))
    while end > start + 1 and not lines[end - 1].strip():
        end -= 1
    lines[end:end] = [""] + block.split("\n")
    return "\n".join(lines)


def build(name, clone, ctx):
    """materialise one control inside CLONE."""
    entry = ctx["paths"]["ENTRY"]
    if name == "BASE":
        return
    if name == "STUB":
        text = ["# Stub control: the bind key field (control fixture, not a claim)", ""]
        text += head_block(ctx["ids"], ctx["opened"])
        text += ["The key field of a bind line is compared as a keysym name."]
        put(clone, entry, "\n".join(text) + "\n")
        return
    if name == "HELD":
        text = ["# Held section 2.3 under a provenance head (control fixture)", ""]
        text += head_block(ctx["ids"], ctx["opened"])
        text += [ctx["held"], ""]
        put(clone, entry, "\n".join(text) + "\n")
        return
    # the OLDPATHS family: the round-49 candidate, unchanged except for the named delta.
    # OLDPATHS stays where the round-49 material actually lives; every other member is the
    # same candidate held at the paths the counter declares (so it can reach the clauses).
    entry = ENTRY_R49 if name == "OLDPATHS" else ctx["paths"]["ENTRY"]
    body = ctx["cand_entry"]
    rows = ctx["cand_rows"]
    if name == "FORGEDQUOTE":
        before = 'The "best" case-insensitive match is the lower-case keysym name.'
        after = 'The "best" case-sensitive match is the lower-case keysym name.'
        if body.count(before) != 1:
            raise Fail("forgery target occurs %d times" % body.count(before))
        body = body.replace(before, after)
    if name == "BRANCHURL":
        ref = "/efb50993780079460b0cbed1363e2166a2de1d9f/"
        lines = rows.split("\n")
        first = next((i for i, l in enumerate(lines) if ROW_RE.match(l)), None)
        if first is None or ref not in lines[first]:
            raise Fail("no row URL with the pinned ref")
        lines[first] = lines[first].replace(ref, "/main/", 1)
        rows = "\n".join(lines)
    put(clone, entry, body)
    if name != "NOROWS":
        put(clone, ctx["paths"]["REGISTRY"], append_rows(ctx["registry"], rows))
    receipt = (RECEIPTS_R49 if name == "OLDPATHS" else ctx["paths"]["RECEIPTS"]) \
        + os.path.basename(R49_RECEIPT)
    if name == "NOLIVE":
        drop(clone, receipt)
    else:
        put(clone, receipt, ctx["receipt"])


def build_probe(name, clone, ctx):
    """FULL: the candidate assembled as a landing would (index row + Gate lines).

    Not a control: it establishes that a passing substrate exists, so a miss by every
    control is a property of the controls, not an unsatisfiable counter.
    """
    build("OLDPATHS", clone, ctx)
    put(clone, ctx["paths"]["README"],
        ctx["readme"].rstrip("\n") + "\n" + ctx["readme_row"] + "\n")
    put(clone, ctx["paths"]["LESSON"], insert_gate(ctx["lesson"], ctx["gate_block"]))


def commit(clone, name):
    top = os.path.realpath(git_out(clone, "rev-parse", "--show-toplevel")
                           .decode().strip())
    if top != os.path.realpath(clone):
        raise Fail("clone toplevel %s != %s" % (top, clone))
    git_out(clone, "add", "-A")
    args = ["-C", clone, *GITC, "-c", "user.name=control",
            "-c", "user.email=control@control.invalid", "commit", "-q",
            "-m", "control: %s" % name]
    if name == "BASE":
        args.append("--allow-empty")
    p = subprocess.run(["git", *args], capture_output=True, env=ENV_GIT)
    if p.returncode != 0:
        raise Fail("commit failed: %s" % p.stderr.decode("utf-8", "replace").strip())
    return git_out(clone, "rev-parse", "HEAD").decode().strip()


def final_line(out):
    lines = [l for l in out.splitlines() if l.strip()]
    return lines[-1] if lines else ""


def first_fail(final):
    m = CLAUSE_RE.search(final)
    if not m:
        return "none" if final else "no-output"
    if "SETUP" in final:
        return "setup"
    vec = dict(kv.split(":") for kv in m.group(1).split())
    for letter in sorted(vec):
        if vec[letter] == "0":
            return letter
    return "none"


def score(counter, clone, base, work, name, timeout):
    cmd = [sys.executable, "-I", counter, "--repo", clone, "--rev", "HEAD"]
    if base:
        cmd += ["--base", base]
    p = subprocess.run(cmd, capture_output=True, env=control_env(work), cwd=work,
                       timeout=timeout)
    out = p.stdout.decode("utf-8", "replace")
    err = p.stderr.decode("utf-8", "replace")
    log = out + (("\n[stderr]\n" + err) if err.strip() else "")
    return p.returncode, out, log


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", default=None)
    ap.add_argument("--base", default=None)
    ap.add_argument("--only", default=None)
    ap.add_argument("--logdir", default=None)
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--probe", action="store_true",
                    help="also score FULL (candidate + index row + Gate lines): a positive "
                         "substrate probe, excluded from the all-missed verdict")
    ap.add_argument("--timeout", type=int, default=900)
    args = ap.parse_args()
    lane = os.path.abspath(args.repo)
    if not args.work:
        tmp = os.environ.get("TMPDIR")
        if not tmp:
            raise Fail("--work absent and TMPDIR unset: a /tmp work dir is not runnable")
        args.work = os.path.join(tmp, "build-controls")
    work = check_paths(args, lane)
    counter = os.path.abspath(args.counter)
    rev = git_out(lane, "rev-parse", "--verify", "--quiet", args.rev + "^{commit}") \
        .decode().strip()
    if not rev:
        raise Fail("unresolved revision %s" % args.rev)
    consts = counter_consts(counter)
    paths = {k: consts.get(k, R50[k]) for k in R50}
    base = args.base or consts.get("BASE_DEFAULT")
    if base:
        base = git_out(lane, "rev-parse", "--verify", "--quiet", base + "^{commit}") \
            .decode().strip()
    opened = consts.get("OPENED", "2026-10-27")
    cand_entry = blob_at(lane, rev, CAND_ENTRY)
    cand_rows = blob_at(lane, rev, CAND_ROWS)
    receipt = blob_at(lane, rev, R49_RECEIPT)
    registry = blob_at(lane, rev, paths["REGISTRY"])
    readme = blob_at(lane, rev, paths["README"])
    lesson = blob_at(lane, rev, paths["LESSON"])
    held_doc = blob_at(lane, rev, HELD_DOC)
    for label, val in (("candidate entry", cand_entry), ("candidate rows", cand_rows),
                       ("round-49 receipt", receipt), ("registry", registry),
                       ("readme", readme), ("held document", held_doc)):
        if val is None:
            raise Fail("substrate missing at %s: %s" % (rev[:12], label))
    reg_text = registry.decode("utf-8", "replace")
    ids = registry_ids(reg_text)[-3:]
    if len(ids) < 3:
        raise Fail("registry holds fewer than three rows")
    row_ids = [m.group(1) for m in
               (ROW_RE.match(l) for l in cand_rows.decode("utf-8", "replace").split("\n"))
               if m]
    if not row_ids:
        raise Fail("candidate rows carry no rows")
    entry_name = os.path.basename(paths["ENTRY"])
    gate_block = "\n".join(
        "- **%s admit** control fixture; opened %s." % (i, opened) for i in row_ids)
    ctx = {
        "paths": paths,
        "ids": ids,
        "opened": opened,
        "held": held_section(held_doc.decode("utf-8", "replace")),
        "cand_entry": cand_entry.decode("utf-8", "replace"),
        "cand_rows": cand_rows.decode("utf-8", "replace"),
        "receipt": receipt,
        "registry": reg_text,
        "readme": readme.decode("utf-8", "replace"),
        "lesson": (lesson or b"## Gate\n").decode("utf-8", "replace"),
        "readme_row": "| `knowledge/%s` (control fixture, round 50) | control fixture for the "
                      "section-9 do-nothing bundle | %s |" % (entry_name, "%s-%s" % (
                          row_ids[0], row_ids[-1])),
        "gate_block": gate_block,
    }
    logdir = os.path.abspath(args.logdir) if args.logdir else os.path.join(work, "logs")
    os.makedirs(logdir, exist_ok=True)
    only = [n.strip().upper() for n in args.only.split(",")] if args.only else list(CONTROLS)
    for n in only:
        if n not in CONTROLS:
            raise Fail("unknown control %s" % n)
    print("BUILD-CONTROLS: counter=%s sha256=%s rev=%s base=%s entry=%s fetch=%s "
          "receipts=%s lesson=%s substrate=%s rows=%d" % (
              display(counter), sha256(open(counter, "rb").read()), rev, base or "-",
              paths["ENTRY"], paths["FETCH"], paths["RECEIPTS"], paths["LESSON"],
              CAND_ENTRY, len(row_ids)))
    met, setup = [], []

    def run_one(name, builder, kind="CONTROL"):
        clone = os.path.join(work, "clone-%s" % name.lower())
        if os.path.exists(clone):
            shutil.rmtree(clone)
        try:
            p = subprocess.run(["git", *GITC, "clone", "-q", "--shared", lane, clone],
                               capture_output=True, env=ENV_GIT)
            if p.returncode != 0:
                raise Fail("clone failed: %s" % p.stderr.decode("utf-8", "replace"))
            git_out(clone, "checkout", "-q", "--detach", rev)
            if os.path.realpath(git_out(clone, "rev-parse", "--show-toplevel")
                                .decode().strip()) != os.path.realpath(clone):
                raise Fail("clone identity check failed for %s" % name)
            builder(name, clone, ctx)
            commit(clone, name)
            rc, out, log = score(counter, clone, base, work, name, args.timeout)
        finally:
            if not args.keep:
                shutil.rmtree(clone, ignore_errors=True)
        with open(os.path.join(logdir, name.lower() + ".log"), "w", encoding="utf-8") as f:
            f.write(log)
        final = final_line(out)
        verdict = "TARGET_MET" if "verdict=TARGET_MET" in final else (
            "TARGET_MISSED" if "verdict=TARGET_MISSED" in final else
            ("SETUP" if "SETUP" in final or rc == 2 else "NO-VERDICT"))
        print("%s name=%s exit=%d verdict=%s first_fail=%s final=%s" % (
            kind, name, rc, verdict, first_fail(final), final))
        return verdict, rc

    for name in only:
        verdict, rc = run_one(name, build)
        if verdict == "TARGET_MET":
            met.append(name)
        elif verdict != "TARGET_MISSED" or rc != 1:
            setup.append(name)
    if args.probe:
        run_one("FULL", build_probe, kind="PROBE")
    print("BUILD-CONTROLS: controls=%d met=%d not_missed=%s not_runnable=%s verdict=%s" % (
        len(only), len(met), ",".join(met) or "-", ",".join(setup) or "-",
        "ALL_MISSED" if not met and not setup else (
            "NOT_MISSED" if met else "NOT_RUNNABLE")))
    if not only:
        return 2
    if setup:
        return 2
    return 1 if met else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Fail as exc:
        print("BUILD-CONTROLS: SETUP %s" % exc)
        sys.exit(2)
