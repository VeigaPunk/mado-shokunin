#!/usr/bin/env python3
"""check-freeze-order.py -- was the round freeze committed strictly before the wave launched?

  python3 -I check-freeze-order.py --repo PATH --rev REV --round N --wave W [--work DIR]
  python3 -I check-freeze-order.py --selftest --work DIR

Reads git objects only (rev-list / log / ls-tree / cat-file); never touches a working tree,
index or ref.  Nothing is written except by --selftest, which builds scratch repos under --work.

FREEZE set: the files that exist at REV among
  .ufo/waves/round-N/{claims-frozen.md,registration.md,frozen-tables.json}
(claims-frozen.md and registration.md are required).
FREEZE commit: the earliest commit on the first-parent chain from REV at which every file of
the FREEZE set exists with the same blob id as at REV.  If a freeze file's blob at REV differs
from the blob at its first appearance on that chain -> freeze_edited:<file>.
LAUNCH: createdAt of .ufo/waves/round-N/<W>/swarm-registry.json at REV.
Verdict OK iff the freeze commit's COMMITTER time is strictly earlier than LAUNCH.  Author time
is never read for the verdict.

One stdout line:
  MADO_FREEZE_ORDER: round=<N> wave=<W> freeze=<12-hex|none> freeze_time=<ISO|none> launch=<ISO|none> verdict=<OK|FAIL> reason=<ok|freeze_after_launch|freeze_edited:<file>|no_freeze|no_registry>
Exit 0 OK, 1 FAIL, 2 setup error (line: `MADO_FREEZE_ORDER: SETUP <reason>`).

Declared limits (R55CritChronology, round 55): the committer date is author-controllable (a backdated
GIT_COMMITTER_DATE reads OK); `createdAt` is the swarm registry's plan time, not the orchestrator's dispatch time; an edit
to a freeze file that is later reverted leaves the blob equal and reads OK; a rebased freeze commit gets a new committer
time and can read FAIL (round 55's own freeze was rewritten by the lane helper from 59e3763f to 54dacbd8 two seconds
later, both before any registry). This instrument refutes a late freeze on honest dates; it does not prove an honest one.
"""
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

REQUIRED = ("claims-frozen.md", "registration.md")
OPTIONAL = ("frozen-tables.json",)


class Setup(Exception):
    pass


def git_env(work):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["LC_ALL"] = "C"
    if work:
        env["TMPDIR"] = work
    return env


def git(repo, args, work=None, extra_env=None, check=True):
    env = git_env(work)
    if extra_env:
        env.update(extra_env)
    p = subprocess.run(["git", "-C", repo] + args, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, env=env)
    if check and p.returncode != 0:
        raise Setup("git_failed:" + " ".join(args[:2]))
    return p


def parse_iso(s):
    """ISO-8601 with Z or +hh:mm offset, optional fraction -> aware datetime; None if bad."""
    if not isinstance(s, str):
        return None
    m = re.fullmatch(r"(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2}:\d{2})(?:\.(\d+))?(Z|[+-]\d{2}:?\d{2})", s.strip())
    if not m:
        return None
    d, t, frac, tz = m.groups()
    frac = ((frac or "") + "000000")[:6]
    if tz == "Z":
        tz = "+00:00"
    elif ":" not in tz:
        tz = tz[:3] + ":" + tz[3:]
    try:
        dt = datetime.fromisoformat("%sT%s.%s%s" % (d, t, frac, "+00:00"))
    except ValueError:
        return None
    return dt


def blobs_at(repo, commit, paths, work):
    """{path: blob id} for the paths existing as regular blobs in commit's tree."""
    p = git(repo, ["ls-tree", "-z", commit, "--"] + paths, work)
    out = {}
    for rec in p.stdout.split(b"\0"):
        if not rec:
            continue
        meta, _, path = rec.partition(b"\t")
        mode, typ, oid = meta.decode().split()
        if typ == "blob":
            out[path.decode()] = oid
    return out


def check(repo, rev, rnd, wave, work):
    """Returns (fields dict, exit code)."""
    if not os.path.isdir(repo):
        raise Setup("repo_not_found")
    r = git(repo, ["rev-parse", "--verify", "--quiet", rev + "^{commit}"], work, check=False)
    if r.returncode != 0:
        raise Setup("rev_not_found")
    tip = r.stdout.decode().strip()
    base = ".ufo/waves/round-%s" % rnd
    f = {"round": rnd, "wave": wave, "freeze": "none", "freeze_time": "none",
         "launch": "none", "verdict": "FAIL", "reason": ""}

    at_rev = blobs_at(repo, tip, [base + "/" + n for n in REQUIRED + OPTIONAL], work)
    if any(base + "/" + n not in at_rev for n in REQUIRED):
        f["reason"] = "no_freeze"
        return f, 1
    fset = [p for p in (base + "/" + n for n in REQUIRED + OPTIONAL) if p in at_rev]

    # Commits on the first-parent chain that change any freeze path, oldest first.  The state
    # of the freeze paths can only change at these commits, so the freeze commit is one of them.
    p = git(repo, ["log", "--first-parent", "--full-history", "--format=%H", tip, "--"] + fset, work)
    changers = list(reversed(p.stdout.decode().split()))
    freeze = first_any = None
    first_seen = {}
    for c in changers:
        have = blobs_at(repo, c, fset, work)
        for path, oid in have.items():
            first_seen.setdefault(path, oid)
        if first_any is None and all(x in have for x in fset):
            first_any = c
        if all(have.get(x) == at_rev[x] for x in fset):
            freeze = c
            break
    edited = [x for x in fset if first_seen.get(x) != at_rev[x]]
    anchor = freeze or first_any
    if anchor is None:
        # files exist at REV but never all together on the first-parent chain (cannot happen
        # for a linear tip; defensive for odd merges)
        f["reason"] = "no_freeze"
        return f, 1
    ct = git(repo, ["show", "-s", "--format=%cI", anchor], work).stdout.decode().strip()
    f["freeze"] = anchor[:12]
    f["freeze_time"] = ct
    if edited:
        f["reason"] = "freeze_edited:" + edited[0].rsplit("/", 1)[1]
        # launch still reported when readable
    reg = git(repo, ["cat-file", "blob", "%s:%s/%s/swarm-registry.json" % (tip, base, wave)],
              work, check=False)
    launch_raw = launch_dt = None
    if reg.returncode == 0:
        import json
        try:
            doc = json.loads(reg.stdout.decode("utf-8", "replace"))
            launch_raw = doc.get("createdAt") if isinstance(doc, dict) else None
            launch_dt = parse_iso(launch_raw)
        except ValueError:
            pass
    if launch_dt is not None:
        f["launch"] = launch_raw
    if edited:
        return f, 1
    if launch_dt is None:
        f["reason"] = "no_registry"
        return f, 1
    if parse_iso(ct) < launch_dt:
        f["verdict"], f["reason"] = "OK", "ok"
        return f, 0
    f["reason"] = "freeze_after_launch"
    return f, 1


def render(f):
    return ("MADO_FREEZE_ORDER: round=%s wave=%s freeze=%s freeze_time=%s launch=%s verdict=%s reason=%s"
            % (f["round"], f["wave"], f["freeze"], f["freeze_time"], f["launch"], f["verdict"], f["reason"]))


# ---------------------------------------------------------------- selftest
def selftest(work):
    import json
    import shutil
    import tempfile
    base_dir = tempfile.mkdtemp(prefix="freeze-selftest-", dir=work)
    fails = []
    n = [0]

    def mk():
        d = os.path.realpath(tempfile.mkdtemp(dir=base_dir))
        subprocess.run(["git", "-C", d, "init", "-q", "--initial-branch=main"], check=True,
                       env=git_env(work))
        top = git(d, ["rev-parse", "--show-toplevel"], work).stdout.decode().strip()
        assert os.path.realpath(top) == d, "scratch repo toplevel mismatch"
        return d

    def commit(d, files, committer, author=None, msg="c", rm=()):
        for rel, content in files.items():
            p = os.path.join(d, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w") as fh:
                fh.write(content)
        for rel in rm:
            os.remove(os.path.join(d, rel))
        env = {"GIT_COMMITTER_DATE": committer, "GIT_AUTHOR_DATE": author or committer}
        git(d, ["add", "-A"], work, env)
        git(d, ["-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q",
                "--allow-empty", "-m", msg], work, env)
        return git(d, ["rev-parse", "HEAD"], work).stdout.decode().strip()

    B = ".ufo/waves/round-9"
    FZ = {B + "/claims-frozen.md": "claims\n", B + "/registration.md": "reg\n",
          B + "/frozen-tables.json": "{}\n"}

    def reg(created):
        return {B + "/w1/swarm-registry.json": json.dumps({"schema": "x", "createdAt": created}) + "\n"}

    def run(d, label, want_line_re, want_rc, wave="w1"):
        try:
            f, rc = check(d, "HEAD", "9", wave, work)
            line = render(f)
        except Setup as e:
            line, rc = "SETUP " + str(e), 2
        ok = re.fullmatch(want_line_re, line) is not None and rc == want_rc
        print("%s %s rc=%d\n    %s" % ("PASS" if ok else "FAIL", label, rc, line))
        if not ok:
            fails.append(label)
            print("    expected /%s/ rc=%d" % (want_line_re, want_rc))

    H = r"[0-9a-f]{12}"
    # 1 OK
    d = mk()
    commit(d, FZ, "2026-10-27T10:00:00-03:00")
    commit(d, reg("2026-10-27T14:00:00.000Z"), "2026-10-27T11:30:00-03:00", msg="launch")
    run(d, "OK (freeze 13:00Z < launch 14:00Z, committer offset -03:00)",
        r"MADO_FREEZE_ORDER: round=9 wave=w1 freeze=%s freeze_time=2026-10-27T10:00:00-03:00 "
        r"launch=2026-10-27T14:00:00.000Z verdict=OK reason=ok" % H, 0)

    # 2 freeze_after_launch
    d = mk()
    commit(d, reg("2026-10-27T14:05:25.338Z"), "2026-10-27T11:05:00-03:00", msg="registry first")
    commit(d, FZ, "2026-10-27T11:11:10-03:00")
    run(d, "freeze_after_launch (freeze 14:11:10Z > launch 14:05:25Z)",
        r"MADO_FREEZE_ORDER: round=9 wave=w1 freeze=%s freeze_time=2026-10-27T11:11:10-03:00 "
        r"launch=2026-10-27T14:05:25.338Z verdict=FAIL reason=freeze_after_launch" % H, 1)

    # 3 equal time is not strictly earlier
    d = mk()
    commit(d, FZ, "2026-10-27T11:00:00-03:00")
    commit(d, reg("2026-10-27T14:00:00.000Z"), "2026-10-27T12:00:00-03:00")
    run(d, "equal time -> FAIL freeze_after_launch",
        r"MADO_FREEZE_ORDER: round=9 .* verdict=FAIL reason=freeze_after_launch", 1)

    # 4 freeze_edited (registration.md changed after first appearance)
    d = mk()
    commit(d, FZ, "2026-10-27T10:00:00-03:00")
    commit(d, {B + "/registration.md": "reg edited\n"}, "2026-10-27T10:30:00-03:00", msg="edit")
    commit(d, reg("2026-10-27T16:00:00.000Z"), "2026-10-27T11:00:00-03:00")
    run(d, "freeze_edited:registration.md (freeze= the edit commit: earliest commit whose blobs all equal REV's)",
        r"MADO_FREEZE_ORDER: round=9 wave=w1 freeze=%s freeze_time=2026-10-27T10:30:00-03:00 "
        r"launch=2026-10-27T16:00:00.000Z verdict=FAIL reason=freeze_edited:registration.md" % H, 1)

    # 4b edit then revert: blob equals first appearance again -> not edited, freeze = first commit
    d = mk()
    c1 = commit(d, FZ, "2026-10-27T10:00:00-03:00")
    commit(d, {B + "/claims-frozen.md": "other\n"}, "2026-10-27T10:10:00-03:00")
    commit(d, {B + "/claims-frozen.md": "claims\n"}, "2026-10-27T10:20:00-03:00")
    commit(d, reg("2026-10-27T16:00:00.000Z"), "2026-10-27T11:00:00-03:00")
    run(d, "edit-then-revert (documented: blob-equality, freeze=%s)" % c1[:12],
        r"MADO_FREEZE_ORDER: round=9 wave=w1 freeze=%s .*verdict=OK reason=ok" % c1[:12], 0)

    # 5 no_freeze: registration.md missing
    d = mk()
    commit(d, {B + "/claims-frozen.md": "claims\n"}, "2026-10-27T10:00:00-03:00")
    commit(d, reg("2026-10-27T16:00:00.000Z"), "2026-10-27T11:00:00-03:00")
    run(d, "no_freeze (registration.md absent)",
        r"MADO_FREEZE_ORDER: round=9 wave=w1 freeze=none freeze_time=none launch=none verdict=FAIL reason=no_freeze", 1)

    # 6 no_registry: file absent; and malformed createdAt
    d = mk()
    commit(d, FZ, "2026-10-27T10:00:00-03:00")
    run(d, "no_registry (swarm-registry.json absent)",
        r"MADO_FREEZE_ORDER: round=9 wave=w1 freeze=%s freeze_time=\S+ launch=none verdict=FAIL reason=no_registry" % H, 1)
    d = mk()
    commit(d, FZ, "2026-10-27T10:00:00-03:00")
    commit(d, reg("yesterday"), "2026-10-27T11:00:00-03:00")
    run(d, "no_registry (createdAt unparsable)",
        r"MADO_FREEZE_ORDER: round=9 wave=w1 freeze=%s freeze_time=\S+ launch=none verdict=FAIL reason=no_registry" % H, 1)

    # 7 author/committer trap A: author EARLIER than launch, committer LATER -> FAIL
    d = mk()
    commit(d, reg("2026-10-27T14:00:00.000Z"), "2026-10-27T11:00:00-03:00", msg="registry")
    commit(d, FZ, committer="2026-10-27T12:00:00-03:00", author="2026-10-27T08:00:00-03:00")
    run(d, "TRAP author 11:00Z < launch 14:00Z but committer 15:00Z > launch -> FAIL",
        r"MADO_FREEZE_ORDER: round=9 wave=w1 freeze=%s freeze_time=2026-10-27T12:00:00-03:00 "
        r"launch=2026-10-27T14:00:00.000Z verdict=FAIL reason=freeze_after_launch" % H, 1)

    # 7b trap B: author LATER than launch, committer EARLIER -> OK
    d = mk()
    commit(d, FZ, committer="2026-10-27T09:00:00-03:00", author="2026-10-27T20:00:00-03:00")
    commit(d, reg("2026-10-27T14:00:00.000Z"), "2026-10-27T11:00:00-03:00")
    run(d, "TRAP author 23:00Z > launch but committer 12:00Z < launch -> OK",
        r"MADO_FREEZE_ORDER: round=9 wave=w1 freeze=%s freeze_time=2026-10-27T09:00:00-03:00 "
        r"launch=2026-10-27T14:00:00.000Z verdict=OK reason=ok" % H, 0)

    # 8 freeze files arrive in different commits: freeze = the later one
    d = mk()
    commit(d, {B + "/claims-frozen.md": "claims\n"}, "2026-10-27T10:00:00-03:00")
    c2 = commit(d, {B + "/registration.md": "reg\n"}, "2026-10-27T13:00:00-03:00")
    commit(d, reg("2026-10-27T14:00:00.000Z"), "2026-10-27T12:00:00-03:00")
    run(d, "split freeze: registration.md lands 16:00Z after launch -> FAIL (freeze=%s)" % c2[:12],
        r"MADO_FREEZE_ORDER: round=9 wave=w1 freeze=%s freeze_time=2026-10-27T13:00:00-03:00 "
        r"launch=\S+ verdict=FAIL reason=freeze_after_launch" % c2[:12], 1)

    # 9 frozen-tables.json optional: absent -> still OK; present-but-edited -> edited
    d = mk()
    commit(d, {k: v for k, v in FZ.items() if not k.endswith(".json")}, "2026-10-27T10:00:00-03:00")
    commit(d, reg("2026-10-27T14:00:00.000Z"), "2026-10-27T11:00:00-03:00")
    run(d, "frozen-tables.json absent is allowed", r".* verdict=OK reason=ok", 0)
    d = mk()
    commit(d, FZ, "2026-10-27T10:00:00-03:00")
    commit(d, {B + "/frozen-tables.json": "{\"a\":1}\n"}, "2026-10-27T10:30:00-03:00")
    commit(d, reg("2026-10-27T14:00:00.000Z"), "2026-10-27T11:00:00-03:00")
    run(d, "freeze_edited:frozen-tables.json", r".* verdict=FAIL reason=freeze_edited:frozen-tables.json", 1)

    # 10 freeze arrives via merge of a side branch: first-parent sees the merge commit
    d = mk()
    commit(d, {"README": "x\n"}, "2026-10-27T09:00:00-03:00")
    git(d, ["checkout", "-q", "-b", "side"], work)
    commit(d, FZ, "2026-10-27T09:30:00-03:00", msg="side freeze")
    git(d, ["checkout", "-q", "main"], work)
    commit(d, {"main.txt": "m\n"}, "2026-10-27T09:40:00-03:00")
    env = {"GIT_COMMITTER_DATE": "2026-10-27T13:00:00-03:00", "GIT_AUTHOR_DATE": "2026-10-27T13:00:00-03:00"}
    git(d, ["-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "merge", "-q", "--no-ff", "-m", "merge", "side"], work, env)
    m = git(d, ["rev-parse", "HEAD"], work).stdout.decode().strip()
    commit(d, reg("2026-10-27T14:00:00.000Z"), "2026-10-27T11:00:00-03:00")
    run(d, "merged-in freeze: first-parent freeze = merge commit %s (16:00Z) -> FAIL" % m[:12],
        r"MADO_FREEZE_ORDER: round=9 wave=w1 freeze=%s freeze_time=2026-10-27T13:00:00-03:00 "
        r"launch=\S+ verdict=FAIL reason=freeze_after_launch" % m[:12], 1)

    # 11 setup errors
    run(os.path.join(base_dir, "nonexistent"), "setup: missing repo", r"SETUP repo_not_found", 2)
    try:
        check(d, "no-such-rev", "9", "w1", work)
        print("FAIL setup: bad rev not rejected")
        fails.append("bad rev")
    except Setup as e:
        print("PASS setup: bad rev -> SETUP %s rc=2" % e)

    shutil.rmtree(base_dir, ignore_errors=True)
    if fails:
        print("MADO_FREEZE_ORDER_SELFTEST: FAIL %d failed: %s" % (len(fails), "; ".join(fails)))
        return 1
    print("MADO_FREEZE_ORDER_SELFTEST: OK")
    return 0


def main(argv):
    a = {}
    i = 0
    flags = {"--repo", "--rev", "--round", "--wave", "--work"}
    selft = False
    while i < len(argv):
        t = argv[i]
        if t == "--selftest":
            selft = True
            i += 1
        elif t in flags and i + 1 < len(argv) and t not in a:
            a[t] = argv[i + 1]
            i += 2
        else:
            print("MADO_FREEZE_ORDER: SETUP usage")
            return 2
    work = a.get("--work")
    if work is not None:
        if not os.path.isdir(work):
            print("MADO_FREEZE_ORDER: SETUP work_not_a_directory")
            return 2
        work = os.path.realpath(work)
    if selft:
        if len(a) != (1 if work else 0) or not work:
            print("MADO_FREEZE_ORDER: SETUP usage")
            return 2
        return selftest(work)
    if not all(k in a for k in ("--repo", "--rev", "--round", "--wave")) \
            or not re.fullmatch(r"[0-9]+", a["--round"]) or not re.fullmatch(r"[A-Za-z0-9_.-]+", a["--wave"]) \
            or a["--wave"] in (".", ".."):
        print("MADO_FREEZE_ORDER: SETUP usage")
        return 2
    try:
        f, rc = check(a["--repo"], a["--rev"], a["--round"], a["--wave"], work)
    except Setup as e:
        print("MADO_FREEZE_ORDER: SETUP %s" % e)
        return 2
    print(render(f))
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
