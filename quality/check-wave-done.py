#!/usr/bin/env python3
"""check-wave-done.py -- did every wave of a round reach WAVE-DONE?

Question answered: for round ``N`` at a revision, is there a committed
``<wave>-results.json`` for every committed ``.ufo/waves/round-N/<wave>.ready``,
and does every seat in it carry a terminal status? This is the mechanical form
of round-49 defect D2: the round-49 report was filed with 7 w1 seats unsettled
and no WAVE-DONE, and the closure could only read that out of prose.

Input: a git repository and a revision. Every file is read from the object
database (``git ls-tree`` + ``git show <rev>:<path>``); the working tree is
never read, so the gate scores committed bytes at any revision of a clone
without checkout. The gate never writes to the repository and needs no scratch
space. ``--selftest`` is the only mode that writes, and it refuses a work dir
under ``/tmp``, ``/var/tmp`` or ``/dev/shm``, and inside a home directory: a
fixture is a git repository with commits, so under a home it would be home state
(round-48 M48-10), and a killed run would leave it there. The home rule reads
``$HOME`` *and* the passwd home for the uid, and an absent or empty ``$HOME`` is an
error -- a rule that reads only ``$HOME`` is switched off by unsetting it, and its
own proof would disappear with it. The selftest asserts its exact case count
(``SELFTEST_CHECKS``) for the same reason.

The results-file contract (derived, not invented)
-------------------------------------------------
Two sources, both checked:

* the fleet dispatcher that writes the file, ``scripts/hyaku/inline-dispatcher.py:289-296``
  (fleet root, not this lane): one record per seat with the keys ``name``,
  ``agent``, ``output`` and ``note``, where ``note`` is ``None`` when the output
  was retained and the kernel-restart note when it was not; the document is
  ``{"lane", "round", "wave", "seats", "results"}``, and ``finalize`` writes it
  only when every seat has settled, beside the dispatch file;
* the round prompt's run-7 handoff block (``.ufo/prompts/mado-round-<N>.md``,
  "Inline spawn handoff"): "per seat: name, agent, id, status, final output".

Those two disagree: the prompt names an ``id`` and a ``status`` field, and the
dispatcher writes neither. Every ``*-results.json`` committed in this lane's
history (rounds 39-48, plus ``round-48/a4r1``) carries exactly the dispatcher's
four keys and no ``status``: a record there is terminal because the file only
exists after ``finalize``, not because a field says so. The gate therefore
scores *observable* terminal states, and accepts an explicit ``status`` string
if a future dispatcher writes one -- unknown values fail rather than pass, so
that drift becomes a finding instead of a silent OK.

Per-seat state, in this order (``name``/``agent`` first: a record without them
is not a seat record):

===========================  =============================================  ============
condition                    state                                           terminal
===========================  =============================================  ============
``name`` missing/empty       ``name-missing``                                no
``name`` not a plain id      ``name-malformed``                              no
``agent`` missing/empty      ``agent-missing``                               no
``name`` already seen        ``name-duplicate``                              no
``status`` = ``settled``     ``settled``                                     yes
``status`` = ``output-unavailable``  ``settled`` (lossy)                     yes
``status`` dead value        ``seat-dead`` (``failed``, ``error``,           yes (dead)
                             ``dead``, ``killed``, ``cancelled``,
                             ``canceled``, ``timeout``)
``status`` other string      ``status-unknown`` (value printed)              no
no ``status``: non-empty     ``settled``                                     yes
   string ``output``
no ``status``: ``output``    ``settled`` (lossy)                             yes
   null + non-empty ``note``
no ``status``: ``output``    ``output-empty``                                no
   null/blank, no ``note``
no ``status``: ``output``    ``output-type``                                 no
   not a string/None
===========================  =============================================  ============

A *settled* seat is one the orchestrator took a final answer from, including the
lossy kernel-restart case (the record exists, the output was not retained); a
*dead* seat failed terminally. Both are terminal answers, and only settled ones
count towards ``settled=``.

Wave verdict (``OK`` only when every check holds)
-------------------------------------------------
* the ``.ready`` marker parses as JSON -- it is the launch marker the prompt
  defines (``ready-unparsable``; a malformed marker does not un-launch a wave);
* a results file exists at the revision (``results-missing``);
* it parses as a JSON object whose ``results`` is a list (``results-unparsable``,
  ``results-shape``) and the list is non-empty (``results-empty``);
* its ``lane`` is ``mado`` and its ``round``/``wave`` agree with the path and
  ``--round`` (``results-identity``; this is the mado gate, so another lane's
  results file in a mado wave dir is a finding, not a pass), and its ``seats``
  integer equals ``len(results)`` (``results-count``);
* every seat is settled (``seats-not-terminal``, one ``SEAT`` line each);
* when the wave's dispatch file is readable at the revision, the results seat
  set equals the dispatch ``taskCall.tasks`` name set (``dispatch-mismatch``);
  when no dispatch file is readable the wave line prints ``dispatched=-`` and
  the gate declares that limit -- seat coverage is then unconfirmed, and saying
  so is the honest answer (``dispatch-unparsable`` covers a dispatch file that
  is present but is not the expected shape).

A wave with no ``.ready`` file was never launched by this handoff, so it is not
scored. That is also the gate's scope: it scores the inline-spawn era, whose
launch marker is the committed ``.ready``. A round whose waves were launched by
the older dispatch bridge (rounds <= 38 in this lane) carries no ``.ready`` at
all, so it reads ``waves=0`` and a ``SCOPE`` line saying the round is *out of
scope*, not settled, so ``waves=0`` never reads as a clean round.

Output, one line per launched wave::

    WAVE wave=w1 ready=1 results=present seats=41 dispatched=41 settled=41 verdict=OK reason=none
    WAVE wave=w2 ready=1 results=absent seats=0 dispatched=- settled=0 verdict=MISSING reason=results-missing

one ``SEAT`` line per non-settled seat (seat names are not session material)::

    SEAT wave=w1 name=ExecFoo state=output-empty:null-no-note

one ``NOTE`` line per structural detail that has no place in the reason token,
one ``ORPHAN`` line per ``<wave>-results.json`` with no ``.ready`` beside it
(printed, never fatal: a stale results file is not a launched wave), one
``SCOPE`` line when the round has no launch marker at all::

    SCOPE round=42 markers=0 note=no-launch-marker: committed evidence without a .ready; ...
    SCOPE round=50 markers=0 note=round-absent: no committed evidence of this round at the revision

then the summary line, exactly::

    MADO_WAVE_DONE: round=49 waves=1 settled=0 verdict=MISSING

``waves=`` counts the launched waves (``.ready`` files) and ``settled=`` the
waves with verdict ``OK``. A round with no launched wave prints ``waves=0`` and
``verdict=MISSING``: "nothing was launched" is not "everything completed".

Exit status: 0 verdict OK, 1 verdict MISSING, 2 usage or git error (an
unresolvable ``--rev``, a ``--repo`` that is not a git repository, a bad
``--round``, a refused work dir).

Usage::

    check-wave-done.py --repo <dir> --rev <rev> --round N
    check-wave-done.py --selftest [--work <dir>] [--verbose]
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

WAVE_DIR = ".ufo/waves/round-%d"
READY_SUFFIX = ".ready"
RESULTS_SUFFIX = "-results.json"
DISPATCH_SUFFIX = "-dispatch.json"

# Recognised explicit `status` values, should a dispatcher ever write one.
SETTLED_STATUS = frozenset({"settled", "output-unavailable"})
DEAD_STATUS = frozenset({"failed", "error", "dead", "killed", "cancelled", "canceled",
                         "timeout"})

REFUSED_WORK_PREFIXES = ("/tmp", "/var/tmp", "/dev/shm")

# The exact number of assertions --selftest must make. A case that silently disappears (an
# env-dependent skip, a removed fixture) turns into a failure instead of a smaller green run.
SELFTEST_CHECKS = 58

NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
UNSAFE_DETAIL_RE = re.compile(r"[^A-Za-z0-9._-]+")

GIT_ENV_KEYS = ("PATH", "SYSTEMROOT")


class GateError(Exception):
    """A condition that makes the question unanswerable (exit 2)."""


def git_env(home=None):
    """Environment for read-only git calls: no user/system config, no locale drift."""
    env = {k: os.environ[k] for k in GIT_ENV_KEYS if k in os.environ}
    env.setdefault("PATH", "/usr/bin:/bin")
    env["HOME"] = home or os.environ.get("HOME") or "/nonexistent"
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["GIT_CONFIG_SYSTEM"] = os.devnull
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["LC_ALL"] = "C"
    return env


def run_git(repo, args):
    cmd = ["git", "-C", repo] + list(args)
    proc = subprocess.run(cmd, capture_output=True, env=git_env())
    if proc.returncode != 0:
        raise GateError("%s exited %d: %s" % (" ".join(cmd), proc.returncode,
                                              proc.stderr.decode("utf-8", "replace").strip()))
    return proc.stdout


def resolve_rev(repo, rev):
    if not rev or not rev.strip():
        raise GateError("--rev is empty")
    out = run_git(repo, ["rev-parse", "--verify", "--end-of-options", rev + "^{commit}"])
    sha = out.decode().strip()
    if not re.fullmatch(r"[0-9a-f]{40}([0-9a-f]{24})?", sha):
        raise GateError("--rev %r did not resolve to one commit (%r)" % (rev, sha))
    return sha


def check_repo(repo):
    if not os.path.isdir(repo):
        raise GateError("--repo %r is not a directory" % repo)
    run_git(repo, ["rev-parse", "--git-dir"])


def read_blob(repo, sha, path):
    """Committed bytes of `path` at commit `sha`; GateError when absent."""
    return run_git(repo, ["show", "%s:%s" % (sha, path)])


def try_read_blob(repo, sha, path):
    try:
        return read_blob(repo, sha, path)
    except GateError:
        return None


def blobs_at(repo, sha, path):
    """Every blob path at `sha` under `path` (files only), repo-relative."""
    if not path.endswith("/"):
        path += "/"
    out = run_git(repo, ["ls-tree", "-r", "-z", "--name-only", "--full-tree", sha, "--", path])
    return [p for p in out.decode("utf-8", "replace").split("\0") if p]


def sanitize(text):
    return UNSAFE_DETAIL_RE.sub("_", str(text)).strip("_")[:60] or "none"


def seat_state(rec):
    """(state, detail) for one results record; state 'settled' means settled."""
    if not isinstance(rec, dict):
        return "record-type", type(rec).__name__
    name = rec.get("name")
    if not isinstance(name, str) or not name.strip():
        return "name-missing", None
    if not NAME_RE.match(name.strip()):
        return "name-malformed", None
    agent = rec.get("agent")
    if not isinstance(agent, str) or not agent.strip():
        return "agent-missing", name.strip()
    if "status" in rec and rec["status"] is not None:
        st = rec["status"]
        if not isinstance(st, str):
            return "status-unknown", type(st).__name__
        key = st.strip().lower()
        if key in SETTLED_STATUS:
            return "settled", key
        if key in DEAD_STATUS:
            return "seat-dead", key
        return "status-unknown", key
    out = rec.get("output")
    if out is None:
        note = rec.get("note")
        if isinstance(note, str) and note.strip():
            return "settled", "lossy"
        return "output-empty", "null-no-note"
    if isinstance(out, str):
        if out.strip():
            return "settled", "output"
        return "output-empty", "blank-output"
    return "output-type", type(out).__name__


def parse_results(blob, wave, rnd):
    """(records, reasons, detail) for a results blob; records None on a shape failure."""
    try:
        doc = json.loads(blob.decode("utf-8", "replace"))
    except ValueError as exc:
        return None, ["results-unparsable"], sanitize(exc)
    if not isinstance(doc, dict):
        return None, ["results-shape"], type(doc).__name__
    recs = doc.get("results")
    if not isinstance(recs, list):
        return None, ["results-shape"], type(recs).__name__
    reasons = []
    if doc.get("wave") != wave:
        reasons.append("results-identity")
    if doc.get("round") != rnd:
        reasons.append("results-identity")
    if doc.get("lane") != "mado":
        reasons.append("results-identity")
    seats = doc.get("seats")
    if not isinstance(seats, int) or isinstance(seats, bool) or seats != len(recs):
        reasons.append("results-count")
    return recs, reasons, None


def dispatch_head(repo, sha, wave, round_dir, ready_doc):
    """(names, source) from the wave's dispatch file at `sha`; names None when unreadable."""
    candidates = [round_dir + "/" + wave + DISPATCH_SUFFIX]
    ref = (ready_doc or {}).get("dispatch") if isinstance(ready_doc, dict) else None
    if isinstance(ref, str) and ref:
        if os.path.isabs(ref):
            # A scratch dispatch path is not in the object database; only its
            # basename can name the committed copy beside the ready marker.
            candidates.append(round_dir + "/" + os.path.basename(ref))
        else:
            candidates.append(ref.lstrip("/"))
            candidates.append(round_dir + "/" + os.path.basename(ref))
    for cand in dict.fromkeys(candidates):
        blob = try_read_blob(repo, sha, cand)
        if blob is None:
            continue
        try:
            parsed = json.loads(blob.decode("utf-8", "replace"))
        except ValueError:
            return None, cand
        tasks = ((parsed or {}).get("taskCall") or {}).get("tasks")
        if not isinstance(tasks, list):
            return None, cand
        names = []
        for task in tasks:
            if not isinstance(task, dict) or not isinstance(task.get("name"), str):
                return None, cand
            names.append(task["name"])
        return names, cand
    return None, None


def check_wave(repo, sha, rnd, round_dir, blob_path):
    """(wave line, seat lines, note lines, settled?) for one launched wave."""
    wave = os.path.basename(blob_path)[:-len(READY_SUFFIX)]
    reasons = []
    notes = []
    seat_lines = []

    ready_blob = try_read_blob(repo, sha, blob_path)
    ready_doc = None
    if ready_blob is not None:
        try:
            ready_doc = json.loads(ready_blob.decode("utf-8", "replace"))
        except ValueError:
            ready_doc = None
    if not isinstance(ready_doc, dict):
        reasons.append("ready-unparsable")

    res_blob = try_read_blob(repo, sha, round_dir + "/" + wave + RESULTS_SUFFIX)
    seats = 0
    settled = 0
    seat_names = []

    if res_blob is None:
        reasons.append("results-missing")
        recs = None
    else:
        recs, hard, detail = parse_results(res_blob, wave, rnd)
        reasons.extend(hard)
        if detail:
            notes.append("NOTE wave=%s reason=results-unparsable detail=%s" % (wave, detail))
        if recs is None:
            recs = None
        else:
            seats = len(recs)
            if not recs:
                reasons.append("results-empty")
            seen = set()
            for rec in recs:
                state, detail = seat_state(rec)
                name = rec.get("name") if isinstance(rec, dict) else None
                if isinstance(name, str) and name.strip():
                    key = name.strip()
                    if key in seen and state == "settled":
                        state, detail = "name-duplicate", key
                    seen.add(key)
                if state == "settled":
                    settled += 1
                    seat_names.append(name.strip() if isinstance(name, str) else "")
                else:
                    tag = state if not detail else "%s:%s" % (state, detail)
                    seat_lines.append("SEAT wave=%s name=%s state=%s"
                                      % (wave, name if isinstance(name, str) else "-", tag))
            if settled != seats:
                reasons.append("seats-not-terminal")

    names_d, src = dispatch_head(repo, sha, wave, round_dir, ready_doc)
    dispatched = "-"
    if src is not None and names_d is None:
        reasons.append("dispatch-unparsable")
        dispatched = "unparsable"
    if names_d is not None:
        dispatched = str(len(names_d))
        if recs is not None:
            missing = [n for n in names_d if n not in seat_names]
            extra = [n for n in seat_names if n not in names_d]
            if missing or extra:
                reasons.append("dispatch-mismatch")
                seat_lines.append("SEAT wave=%s state=dispatch-mismatch missing=%d extra=%d"
                                  % (wave, len(missing), len(extra)))

    reasons = list(dict.fromkeys(reasons))
    ok = not reasons
    line = ("WAVE wave=%s ready=1 results=%s seats=%d dispatched=%s settled=%d verdict=%s reason=%s"
            % (wave, "present" if res_blob is not None else "absent", seats, dispatched,
               settled, "OK" if ok else "MISSING", "none" if ok else "+".join(reasons)))
    return line, seat_lines, notes, ok


def scan(repo, sha, rnd):
    """(wave lines, seat lines, notes, orphan lines, waves, settled) for one round."""
    round_dir = WAVE_DIR % rnd
    depth = round_dir.count("/") + 1
    paths = blobs_at(repo, sha, round_dir)
    ready = sorted(p for p in paths
                   if p.count("/") == depth and p.endswith(READY_SUFFIX))
    results = sorted(p for p in paths
                     if p.count("/") == depth and p.endswith(RESULTS_SUFFIX))

    wave_lines, seat_lines, note_lines = [], [], []
    waves = settled = 0
    for path in ready:
        line, seats, notes, ok = check_wave(repo, sha, rnd, round_dir, path)
        wave_lines.append(line)
        seat_lines.extend(seats)
        note_lines.extend(notes)
        waves += 1
        settled += 1 if ok else 0

    launched = {os.path.basename(p)[:-len(READY_SUFFIX)] for p in ready}
    orphan_lines = ["ORPHAN results=%s reason=no-ready" % os.path.basename(p)
                    for p in results
                    if os.path.basename(p)[:-len(RESULTS_SUFFIX)] not in launched]
    if not ready:
        # No launch marker: either the round left no committed evidence at all, or
        # its waves were launched by a path this gate does not score (the pre-handoff
        # dispatch bridge, rounds <= 38 in this lane). Say which; never let waves=0
        # read as a clean round.
        if paths:
            scope_lines = ["SCOPE round=%d markers=0 note=no-launch-marker: "
                           "committed evidence without a .ready; this gate scores the "
                           "inline-spawn handoff only, so the round is out of scope, "
                           "not settled" % rnd]
        else:
            scope_lines = ["SCOPE round=%d markers=0 note=round-absent: no committed "
                           "evidence of this round at the revision" % rnd]
    else:
        scope_lines = []
    return wave_lines, seat_lines, note_lines, orphan_lines, scope_lines, waves, settled


def run_check(args):
    check_repo(args.repo)
    if args.round < 0:
        raise GateError("--round must be >= 0 (got %d)" % args.round)
    sha = resolve_rev(args.repo, args.rev)
    (wave_lines, seat_lines, note_lines, orphan_lines, scope_lines,
     waves, settled) = scan(args.repo, sha, args.round)
    for line in wave_lines + seat_lines + note_lines + orphan_lines + scope_lines:
        print(line)
    verdict = "OK" if (waves > 0 and settled == waves) else "MISSING"
    print("MADO_WAVE_DONE: round=%d waves=%d settled=%d verdict=%s"
          % (args.round, waves, settled, verdict))
    return 0 if verdict == "OK" else 1


# --------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------

class Suite:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.passed = 0
        self.failed = []

    def check(self, name, ok, detail=""):
        if ok:
            self.passed += 1
            if self.verbose:
                print("ok   %s %s" % (name, detail))
        else:
            self.failed.append((name, detail))
            print("FAIL %s %s" % (name, detail))

    def report(self):
        total = self.passed + len(self.failed)
        if total != SELFTEST_CHECKS:
            self.failed.append(("selftest-count",
                                "expected=%d got=%d" % (SELFTEST_CHECKS, total)))
            total = self.passed + len(self.failed)
        for name, detail in self.failed:
            print("FAILED: %s %s" % (name, detail))
        print("MADO_WAVE_DONE_SELFTEST: %d/%d passed" % (self.passed, total))
        return 0 if not self.failed else 1


def passwd_home():
    """The passwd home for the current uid, or None when the platform has no passwd db."""
    try:
        import pwd
    except ImportError:
        return None
    try:
        return pwd.getpwuid(os.getuid()).pw_dir
    except (KeyError, OSError):
        return None


def home_roots():
    """Every home this process could write under: $HOME (required, non-empty) and the passwd home.

    A rule that reads only $HOME is skippable by unsetting the variable, and the gate's own
    home-refusal cases would then vanish with it and still report success. So an absent or
    empty $HOME is an error, not "no home to compare", and the passwd home is checked too.
    """
    env_home = os.environ.get("HOME")
    if not env_home or not env_home.strip():
        raise GateError("HOME is unset or empty: the home rule cannot be checked, and an absent "
                        "HOME must not switch it off (set HOME and point --work at a scratch "
                        "filesystem)")
    roots = []
    for cand in (env_home, passwd_home()):
        if not cand:
            continue
        real = os.path.realpath(cand)
        if real != os.sep and real not in roots:
            roots.append(real)
    return roots


def resolve_work(explicit):
    cand = explicit or os.environ.get("TMPDIR")
    if not cand:
        raise GateError("--selftest needs --work <dir> or a TMPDIR outside /tmp, /var/tmp, "
                        "/dev/shm and the home directory")
    real = os.path.realpath(cand)
    for bad in REFUSED_WORK_PREFIXES:
        if real == bad or real.startswith(bad + os.sep):
            raise GateError("refusing work dir under %s (got %s): use a scratch filesystem"
                            % (bad, real))
    for home in home_roots():
        # Fixtures are git repositories with commits and files: under a home they are
        # home state (round-48 M48-10), and a SIGKILL leaves them there.
        if real == home or real.startswith(home + os.sep):
            raise GateError("refusing work dir inside the home directory (got ~%s): use a "
                            "scratch filesystem" % real[len(home):])
    os.makedirs(real, exist_ok=True)
    return tempfile.mkdtemp(prefix="wave-done-selftest.", dir=real)


class Fixture:
    """A throwaway git repository holding wave markers, dispatch files and results."""

    def __init__(self, root, name):
        self.root = root
        self.path = os.path.join(root, name)
        os.makedirs(self.path, exist_ok=False)
        self.home = os.path.join(root, "home-" + name)
        for sub in ("", ".cache", ".config", ".local/share", ".local/state"):
            os.makedirs(os.path.join(self.home, sub), exist_ok=True)
        self.env = git_env(self.home)
        self.env.update({"TMPDIR": self.root,
                         "XDG_CACHE_HOME": os.path.join(self.home, ".cache"),
                         "XDG_CONFIG_HOME": os.path.join(self.home, ".config"),
                         "XDG_DATA_HOME": os.path.join(self.home, ".local", "share"),
                         "XDG_STATE_HOME": os.path.join(self.home, ".local", "state")})
        self.git(["init", "-q"])
        top = self.git(["rev-parse", "--show-toplevel"]).decode().strip()
        if os.path.realpath(top) != os.path.realpath(self.path):
            raise GateError("fixture toplevel %r != %r" % (top, self.path))

    def git(self, args):
        cmd = ["git", "-C", self.path,
               "-c", "user.name=Wave Done Selftest",
               "-c", "user.email=selftest@example.invalid",
               "-c", "commit.gpgsign=false",
               "-c", "tag.gpgsign=false"] + list(args)
        proc = subprocess.run(cmd, capture_output=True, env=self.env)
        if proc.returncode != 0:
            raise GateError("fixture git %s: %s" % (" ".join(args),
                                                    proc.stderr.decode("utf-8", "replace").strip()))
        return proc.stdout

    def write(self, rel, content):
        full = os.path.join(self.path, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        data = content if isinstance(content, bytes) else content.encode()
        with open(full, "wb") as fh:
            fh.write(data)

    def commit(self, files, msg):
        for rel, content in sorted(files.items()):
            self.write(rel, content)
            self.git(["add", "--", rel])
        self.git(["commit", "-q", "-m", msg])
        return self.git(["rev-parse", "HEAD"]).decode().strip()


def results_doc(round_no, wave, records, seats=None, lane="mado"):
    return json.dumps({"lane": lane, "round": round_no, "wave": wave,
                       "seats": len(records) if seats is None else seats,
                       "results": records}, indent=1)


def dispatch_doc(names):
    return json.dumps({"taskCall": {"tasks": [{"name": n, "agent": "executor", "task": "x"}
                                              for n in names]}})


def seat(name, agent="executor", output="final answer", note=None, **extra):
    rec = {"name": name, "agent": agent, "output": output, "note": note}
    rec.update(extra)
    return rec


def invoke(repo, rev, rnd, work):
    """Run this file in check mode as a child process; (rc, stdout+stderr)."""
    cmd = [sys.executable, "-I", os.path.abspath(__file__),
           "--repo", repo, "--rev", rev, "--round", str(rnd)]
    env = git_env(os.path.join(work, "child-home"))
    os.makedirs(env["HOME"], exist_ok=True)
    proc = subprocess.run(cmd, capture_output=True, env=env, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def summary_line(out):
    for line in reversed(out.strip().splitlines()):
        if line.startswith("MADO_WAVE_DONE:"):
            return line
    return ""


def first_line(out, prefix):
    for line in out.strip().splitlines():
        if line.startswith(prefix):
            return line
    return ""


def selftest(work, verbose=False):
    suite = Suite(verbose)
    rd = ".ufo/waves/round-49"
    lossy_note = ("orchestrator kernel restarted mid-wave; seat output was delivered to the "
                  "orchestrator session but not retained - read the seat report file")

    # A -- the round-49 shape: a launched wave and no results file (defect D2).
    a = Fixture(work, "r49-shape")
    sha = a.commit({rd + "/w1.ready": json.dumps({"lane": "mado", "round": 49, "wave": "w1",
                                                  "dispatch": "/scratch/x/w1-dispatch.json",
                                                  "l1": "MadoR49"}),
                    rd + "/w1-dispatch.json": dispatch_doc(["ExecA", "ExecB"])},
                   "round 49 wave 1 launched, no results")
    rc, out = invoke(a.path, sha, 49, work)
    suite.check("r49-exit-1", rc == 1, "rc=%d" % rc)
    suite.check("r49-summary",
                summary_line(out) == "MADO_WAVE_DONE: round=49 waves=1 settled=0 verdict=MISSING",
                summary_line(out))
    suite.check("r49-wave-line",
                first_line(out, "WAVE ") == ("WAVE wave=w1 ready=1 results=absent seats=0 "
                                             "dispatched=2 settled=0 verdict=MISSING "
                                             "reason=results-missing"),
                first_line(out, "WAVE "))
    suite.check("r49-no-seat-lines", first_line(out, "SEAT ") == "", first_line(out, "SEAT "))

    # B -- every seat settled.
    b = Fixture(work, "settled")
    sha = b.commit({rd + "/w1.ready": "{}",
                    rd + "/w1-dispatch.json": dispatch_doc(["ExecA", "ExecB"]),
                    rd + "/w1-results.json": results_doc(49, "w1", [seat("ExecA"), seat("ExecB")])},
                   "results present, both settled")
    rc, out = invoke(b.path, sha, 49, work)
    suite.check("settled-exit-0", rc == 0, "rc=%d" % rc)
    suite.check("settled-summary",
                summary_line(out) == "MADO_WAVE_DONE: round=49 waves=1 settled=1 verdict=OK",
                summary_line(out))
    suite.check("settled-wave-line",
                first_line(out, "WAVE ").endswith("seats=2 dispatched=2 settled=2 verdict=OK "
                                                  "reason=none"),
                first_line(out, "WAVE "))

    # C -- the lossy kernel-restart record is terminal.
    c = Fixture(work, "lossy")
    sha = c.commit({rd + "/w1.ready": "{}",
                    rd + "/w1-results.json": results_doc(49, "w1", [seat("ExecA"),
                                                                    seat("ExecB", output=None,
                                                                         note=lossy_note)])},
                   "one seat lossy-terminal")
    rc, out = invoke(c.path, sha, 49, work)
    suite.check("lossy-exit-0", rc == 0 and summary_line(out).endswith("verdict=OK"),
                summary_line(out))
    suite.check("lossy-counts-settled", "settled=2" in first_line(out, "WAVE "),
                first_line(out, "WAVE "))

    # D -- a record with no output and no note is not terminal.
    d = Fixture(work, "output-empty")
    sha = d.commit({rd + "/w1.ready": "{}",
                    rd + "/w1-results.json": results_doc(49, "w1", [seat("ExecA"),
                                                                    seat("ExecB", output=None)])},
                   "null output without note")
    rc, out = invoke(d.path, sha, 49, work)
    suite.check("output-empty-exit-1", rc == 1, "rc=%d" % rc)
    suite.check("output-empty-seat-line",
                "SEAT wave=w1 name=ExecB state=output-empty:null-no-note" in out,
                first_line(out, "SEAT "))
    suite.check("output-empty-reason", first_line(out, "WAVE ").endswith("reason=seats-not-terminal"),
                first_line(out, "WAVE "))

    d2 = Fixture(work, "blank-output")
    sha = d2.commit({rd + "/w1.ready": "{}",
                     rd + "/w1-results.json": results_doc(49, "w1", [seat("ExecA", output="   ")])},
                    "whitespace-only output")
    rc, out = invoke(d2.path, sha, 49, work)
    suite.check("blank-output-exit-1",
                rc == 1 and "state=output-empty:blank-output" in out, summary_line(out))

    d3 = Fixture(work, "output-type")
    sha = d3.commit({rd + "/w1.ready": "{}",
                     rd + "/w1-results.json": results_doc(49, "w1", [seat("ExecA", output={"x": 1})])},
                    "output is not a string")
    rc, out = invoke(d3.path, sha, 49, work)
    suite.check("output-type-exit-1",
                rc == 1 and "state=output-type:dict" in out, summary_line(out))

    # E -- structural failures.
    e = Fixture(work, "unparsable")
    sha = e.commit({rd + "/w1.ready": "{}", rd + "/w1-results.json": "{not json"},
                   "broken results")
    rc, out = invoke(e.path, sha, 49, work)
    suite.check("unparsable-exit-1",
                rc == 1 and "reason=results-unparsable" in out, summary_line(out))
    suite.check("unparsable-note", first_line(out, "NOTE ") != "", first_line(out, "NOTE "))

    e2 = Fixture(work, "shape")
    sha = e2.commit({rd + "/w1.ready": "{}",
                     rd + "/w1-results.json": json.dumps({"lane": "mado", "round": 49,
                                                          "wave": "w1", "seats": 1,
                                                          "results": "nope"})},
                    "results is not a list")
    rc, out = invoke(e2.path, sha, 49, work)
    suite.check("shape-exit-1", rc == 1 and "reason=results-shape" in out, summary_line(out))

    e3 = Fixture(work, "identity")
    sha = e3.commit({rd + "/w1.ready": "{}",
                     rd + "/w1-results.json": results_doc(48, "w1", [seat("ExecA")])},
                    "results document names the wrong round")
    rc, out = invoke(e3.path, sha, 49, work)
    suite.check("identity-exit-1", rc == 1 and "results-identity" in out, summary_line(out))

    e4 = Fixture(work, "count")
    sha = e4.commit({rd + "/w1.ready": "{}",
                     rd + "/w1-results.json": results_doc(49, "w1", [seat("ExecA")], seats=3)},
                    "seats field disagrees with the results list")
    rc, out = invoke(e4.path, sha, 49, work)
    suite.check("count-exit-1", rc == 1 and "results-count" in out, summary_line(out))

    e4b = Fixture(work, "lane")
    sha = e4b.commit({rd + "/w1.ready": "{}",
                      rd + "/w1-results.json": results_doc(49, "w1", [seat("ExecA")],
                                                           lane="souji")},
                     "results document belongs to another lane")
    rc, out = invoke(e4b.path, sha, 49, work)
    suite.check("lane-exit-1", rc == 1 and "results-identity" in out, summary_line(out))

    e5 = Fixture(work, "dupes")
    sha = e5.commit({rd + "/w1.ready": "{}",
                     rd + "/w1-results.json": results_doc(49, "w1", [seat("ExecA"),
                                                                     seat("ExecA")])},
                    "the same seat twice")
    rc, out = invoke(e5.path, sha, 49, work)
    suite.check("dupes-exit-1", rc == 1 and "state=name-duplicate:ExecA" in out,
                summary_line(out))

    e6 = Fixture(work, "ready-broken")
    sha = e6.commit({rd + "/w1.ready": "not json at all",
                     rd + "/w1-results.json": results_doc(49, "w1", [seat("ExecA")])},
                    "launch marker is not JSON")
    rc, out = invoke(e6.path, sha, 49, work)
    suite.check("ready-unparsable-exit-1", rc == 1 and "reason=ready-unparsable" in out,
                summary_line(out))

    # F -- explicit status vocabulary (the prompt's contract shape).
    f = Fixture(work, "status-settled")
    sha = f.commit({rd + "/w1.ready": "{}",
                    rd + "/w1-results.json": results_doc(
                        49, "w1", [seat("ExecA", status="settled", id="seat-1")])},
                   "prompt-contract record carrying status and id")
    rc, out = invoke(f.path, sha, 49, work)
    suite.check("status-settled-exit-0", rc == 0, summary_line(out))

    f2 = Fixture(work, "status-failed")
    sha = f2.commit({rd + "/w1.ready": "{}",
                     rd + "/w1-results.json": results_doc(49, "w1", [seat("ExecA"),
                                                                     seat("ExecB",
                                                                          status="failed")])},
                    "one seat failed terminally")
    rc, out = invoke(f2.path, sha, 49, work)
    suite.check("status-failed-exit-1",
                rc == 1 and "state=seat-dead:failed" in out, summary_line(out))

    f3 = Fixture(work, "status-unknown")
    sha = f3.commit({rd + "/w1.ready": "{}",
                     rd + "/w1-results.json": results_doc(49, "w1", [seat("ExecA",
                                                                          status="in-flight")])},
                    "unknown status value")
    rc, out = invoke(f3.path, sha, 49, work)
    suite.check("status-unknown-exit-1",
                rc == 1 and "state=status-unknown:in-flight" in out, summary_line(out))

    f4 = Fixture(work, "agent-missing")
    sha = f4.commit({rd + "/w1.ready": "{}",
                     rd + "/w1-results.json": results_doc(49, "w1", [{"name": "ExecA",
                                                                      "output": "x"}])},
                    "record without an agent")
    rc, out = invoke(f4.path, sha, 49, work)
    suite.check("agent-missing-exit-1",
                rc == 1 and "state=agent-missing:ExecA" in out, summary_line(out))

    # G -- seat coverage against the dispatch file.
    g = Fixture(work, "dispatch-mismatch")
    sha = g.commit({rd + "/w1.ready": "{}",
                    rd + "/w1-dispatch.json": dispatch_doc(["ExecA", "ExecC"]),
                    rd + "/w1-results.json": results_doc(49, "w1", [seat("ExecA")])},
                   "a dispatched seat never reported")
    rc, out = invoke(g.path, sha, 49, work)
    suite.check("dispatch-mismatch-exit-1",
                rc == 1 and "reason=dispatch-mismatch" in out, summary_line(out))
    suite.check("dispatch-mismatch-counts",
                "state=dispatch-mismatch missing=1 extra=0" in out, first_line(out, "SEAT "))

    g2 = Fixture(work, "dispatch-absent")
    sha = g2.commit({rd + "/w1.ready": "{}",
                     rd + "/w1-results.json": results_doc(49, "w1", [seat("ExecA")])},
                    "results with no dispatch file at this revision")
    rc, out = invoke(g2.path, sha, 49, work)
    suite.check("dispatch-absent-exit-0", rc == 0, summary_line(out))
    suite.check("dispatch-absent-declared", "dispatched=-" in first_line(out, "WAVE "),
                first_line(out, "WAVE "))

    g3 = Fixture(work, "dispatch-from-ready")
    sha = g3.commit({rd + "/w1.ready": json.dumps({"dispatch": "/scratch/seat/w1-dispatch.json"}),
                     rd + "/w1-dispatch.json": dispatch_doc(["ExecA"]),
                     rd + "/w1-results.json": results_doc(49, "w1", [seat("ExecA")])},
                    "ready names a scratch dispatch path; the committed copy is used")
    rc, out = invoke(g3.path, sha, 49, work)
    suite.check("dispatch-from-ready", rc == 0 and "dispatched=1" in first_line(out, "WAVE "),
                first_line(out, "WAVE "))

    # H -- two waves, one settled.
    h = Fixture(work, "two-waves")
    sha = h.commit({rd + "/w1.ready": "{}", rd + "/w2.ready": "{}",
                    rd + "/w1-results.json": results_doc(49, "w1", [seat("ExecA")])},
                   "wave 2 still in flight")
    rc, out = invoke(h.path, sha, 49, work)
    suite.check("two-waves-exit-1", rc == 1, "rc=%d" % rc)
    suite.check("two-waves-summary",
                summary_line(out) == "MADO_WAVE_DONE: round=49 waves=2 settled=1 verdict=MISSING",
                summary_line(out))
    suite.check("two-waves-order", first_line(out, "WAVE ").startswith("WAVE wave=w1"),
                first_line(out, "WAVE "))
    suite.check("two-waves-w2-line",
                [l for l in out.splitlines() if l.startswith("WAVE wave=w2")][0].endswith(
                    "results=absent seats=0 dispatched=- settled=0 verdict=MISSING "
                    "reason=results-missing"),
                [l for l in out.splitlines() if l.startswith("WAVE wave=w2")][0])

    # I -- nothing launched; a results file with no ready; another round.
    i = Fixture(work, "no-ready")
    sha = i.commit({rd + "/w2-results.json": results_doc(49, "w2", [seat("ExecA")])},
                   "results without a launched wave")
    rc, out = invoke(i.path, sha, 49, work)
    suite.check("no-ready-exit-1",
                rc == 1 and summary_line(out) ==
                "MADO_WAVE_DONE: round=49 waves=0 settled=0 verdict=MISSING",
                summary_line(out))
    suite.check("no-ready-orphan",
                "ORPHAN results=w2-results.json reason=no-ready" in out, out.strip()[:120])
    suite.check("no-ready-scope",
                first_line(out, "SCOPE ").startswith("SCOPE round=49 markers=0 "
                                                     "note=no-launch-marker:"),
                first_line(out, "SCOPE "))

    i2 = Fixture(work, "other-round")
    sha = i2.commit({".ufo/waves/round-48/w1.ready": "{}"}, "another round only")
    rc, out = invoke(i2.path, sha, 49, work)
    suite.check("round-absent-exit-1",
                rc == 1 and summary_line(out) ==
                "MADO_WAVE_DONE: round=49 waves=0 settled=0 verdict=MISSING",
                summary_line(out))
    suite.check("round-absent-scope",
                first_line(out, "SCOPE ").startswith("SCOPE round=49 markers=0 "
                                                    "note=round-absent:"),
                first_line(out, "SCOPE "))

    i3 = Fixture(work, "dispatched-marker")
    sha = i3.commit({rd + "/w1.ready.dispatched": "2026-10-27T00:00:00\n{}",
                     rd + "/w1-results.json": results_doc(49, "w1", [seat("ExecA")])},
                    "only the taken-marker copy is committed, not the launch marker")
    rc, out = invoke(i3.path, sha, 49, work)
    suite.check("dispatched-marker-not-a-launch",
                rc == 1 and summary_line(out).endswith("waves=0 settled=0 verdict=MISSING")
                and "ORPHAN results=w1-results.json reason=no-ready" in out,
                summary_line(out))

    # J -- committed bytes only: the working tree is never read, --rev pins the bytes.
    j = Fixture(work, "worktree-invisible")
    good = j.commit({rd + "/w1.ready": "{}",
                     rd + "/w1-results.json": results_doc(49, "w1", [seat("ExecA")])},
                    "good results committed")
    j.write(rd + "/w1-results.json", "{ this worktree copy is garbage")
    rc_tree, out_tree = invoke(j.path, good, 49, work)
    suite.check("worktree-not-read", rc_tree == 0, summary_line(out_tree))

    bad = j.commit({rd + "/w1-results.json": "{ still garbage"}, "garbage results committed")
    rc_old, out_old = invoke(j.path, good, 49, work)
    rc_new, out_new = invoke(j.path, bad, 49, work)
    suite.check("rev-pins-bytes", rc_old == 0 and rc_new == 1,
                "%s | %s" % (summary_line(out_old), summary_line(out_new)))

    # K -- usage and argument errors (exit 2), and the work-dir refusal.
    child_home = os.path.join(work, "child-home")
    os.makedirs(child_home, exist_ok=True)
    for label, argv in (
            ("no-repo", ["--rev", "HEAD", "--round", "49"]),
            ("no-rev", ["--repo", b.path, "--round", "49"]),
            ("no-round", ["--repo", b.path, "--rev", "HEAD"]),
            ("bad-round", ["--repo", b.path, "--rev", "HEAD", "--round", "nope"]),
            ("selftest-plus-repo", ["--selftest", "--repo", b.path]),
    ):
        proc = subprocess.run([sys.executable, "-I", os.path.abspath(__file__)] + argv,
                              capture_output=True, env=git_env(child_home), text=True)
        suite.check("usage-%s-exit-2" % label, proc.returncode == 2,
                    "rc=%d %s" % (proc.returncode, proc.stderr.strip().splitlines()[-1:]))

    proc = subprocess.run([sys.executable, "-I", os.path.abspath(__file__),
                           "--repo", b.path, "--rev", "0" * 40, "--round", "49"],
                          capture_output=True, env=git_env(child_home), text=True)
    suite.check("unresolvable-rev-exit-2", proc.returncode == 2, "rc=%d" % proc.returncode)

    proc = subprocess.run([sys.executable, "-I", os.path.abspath(__file__),
                           "--repo", os.path.join(work, "not-a-repo"),
                           "--rev", "HEAD", "--round", "49"],
                          capture_output=True, env=git_env(child_home), text=True)
    suite.check("not-a-repo-exit-2", proc.returncode == 2, "rc=%d" % proc.returncode)

    for bad_dir in ("/tmp/wave-done-selftest", "/var/tmp/wave-done-selftest",
                    "/dev/shm/wave-done-selftest"):
        try:
            resolve_work(bad_dir)
            refused, detail = False, "accepted"
        except GateError as exc:
            refused, detail = True, str(exc)[:60]
        suite.check("refuse-work-%s" % bad_dir.strip("/").replace("/", "-"), refused, detail)

    home = os.environ.get("HOME")
    if home and os.path.realpath(home) != os.sep:
        for label, cand in (("home-root", home),
                            ("home-sub", os.path.join(home, "wave-done-selftest")),
                            ("passwd-home-sub",
                             os.path.join(passwd_home() or home, "wave-done-selftest"))):
            try:
                resolve_work(cand)
                refused, detail = False, "accepted"
            except GateError as exc:
                refused, detail = True, str(exc)[:60]
            suite.check("refuse-work-%s" % label, refused, detail)

    # A rule that reads only $HOME is switched off by unsetting the variable, and its own two
    # cases above would vanish with it. Both directions are pinned: an absent HOME is an error
    # whatever the candidate, and the passwd home still refuses while HOME is absent.
    for label, cand in (("home-unset-pwdir", passwd_home() or work),
                        ("home-unset-safe-dir", work)):
        saved = os.environ.pop("HOME", None)
        try:
            try:
                resolve_work(cand)
                refused, detail = False, "accepted"
            except GateError as exc:
                refused, detail = True, str(exc)[:60]
        finally:
            if saved is not None:
                os.environ["HOME"] = saved
            else:
                os.environ.pop("HOME", None)
        suite.check("refuse-work-%s" % label, refused, detail)

    return suite.report()


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="check-wave-done.py",
        description="Score WAVE-DONE for every launched wave of a round, from committed bytes.")
    parser.add_argument("--repo", help="git repository (read-only)")
    parser.add_argument("--rev", help="revision whose committed bytes are scored")
    parser.add_argument("--round", type=int, help="round number: scans .ufo/waves/round-N")
    parser.add_argument("--selftest", action="store_true", help="run the hermetic fixture suite")
    parser.add_argument("--work", help="scratch dir for --selftest (or TMPDIR); /tmp is refused")
    parser.add_argument("--verbose", action="store_true", help="print every passing selftest case")
    args = parser.parse_args(argv)

    if args.selftest:
        if args.repo or args.rev or args.round is not None:
            parser.error("--selftest takes only --work/--verbose")
        try:
            work = resolve_work(args.work)
        except GateError as exc:
            sys.stderr.write("check-wave-done.py: %s\n" % exc)
            return 2
        try:
            return selftest(work, args.verbose)
        finally:
            shutil.rmtree(work, ignore_errors=True)

    if not args.repo or not args.rev or args.round is None:
        parser.error("--repo, --rev and --round are required (or use --selftest)")
    try:
        return run_check(args)
    except GateError as exc:
        sys.stderr.write("check-wave-done.py: %s\n" % exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
