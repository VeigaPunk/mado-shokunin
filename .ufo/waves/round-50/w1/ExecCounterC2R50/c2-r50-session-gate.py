#!/usr/bin/env python3
"""c2-r50-session-gate.py — PRED-C2-r50: the session-material gate detects its covered shapes.

Draft for `quality/counters/c2-r50-session-gate.py` (mado round 50, w1 build). The
instrument scores the gate that a revision installs at
``quality/check-session-material.py``: it reads the gate's bytes with
``git show <rev>:quality/check-session-material.py`` (never the working tree),
writes them under ``--work``, and runs them with ``python3 -I`` in an isolated
HOME/XDG/TMPDIR sandbox.

Clauses (all four must hold for ``TARGET_MET``):

``s``  the gate's own ``--selftest`` passes (``N/N`` with ``N >= 94``) and every
       v2 selftest case name is still present. The 69 v2 names are the case
       names the v2 gate at base ``8ae47b95`` prints; the list is embedded below
       and its sha256 is pinned (``V2_CASE_NAMES_SHA256``), with the seat-dir
       copy ``v2-selftest-cases.txt``.
``r``  RED: K >= 40 nonce-generated fixture git repositories (fresh identity,
       toplevel asserted, under ``--work``), each holding exactly one instance
       of one covered shape — the four structural R7 forms (grep-style
       ``path:LINE:`` home prefix, listing header ``path:``, quoted path on a
       tool diagnostic line, home path inside an ``ls -l`` row), the R8
       owner/group column equal to the account, and the R9 >= 2 column-0
       exec-cache fields. Every red repository must yield the expected rule,
       at least one finding and a non-zero exit under the gate's default scope.
``g``  GREEN: K >= 40 counter-shape repositories (``~/`` and ``$HOME/`` forms, a
       home path inside a prose sentence, numeric ids in an ``ls -ln`` row, one
       cache field only, indented usage text) must yield zero findings and exit
       0.
``d``  the default scope sees a file outside ``.ufo/``: a repository whose only
       red instance sits at ``docs/receipt.txt`` is detected with no ``--scope``
       and is clean under ``--scope ufo`` when the gate accepts that flag.

Names and paths are synthetic by construction (``someoneNNN`` home users,
``fixtureNNNN`` accounts, word paths), so a receipt never carries the real
account or a host path. Fixture repositories live under ``--work`` and are
removed when the run ends; the gate copy stays at ``--work/gates/``.

The last line is::

    PRED-C2-r50: selftest=94/94 names=69/69 red=42/42 green=44/44 scope=seen \
verdict=TARGET_MET rev=<full commit>

with exit 0 for ``TARGET_MET``, 1 for ``TARGET_MISSED`` and 2 for a setup
error (bad ``--work``, unreadable gate). ``names`` is the v2 case-name subset
count, so a gate that keeps ``94/94`` while renaming a v2 case still misses.

``--work`` (and an inherited ``TMPDIR``) under ``/tmp``, ``/var/tmp`` or
``/dev/shm`` is refused with exit 2, as is a ``--work`` under the invoking
``HOME`` (never point sandbox state at home state). So is a missing gate at the
revision.

Usage:
  python3 -I c2-r50-session-gate.py --repo REPO --rev REV --work DIR --nonce N
"""

import argparse
import hashlib
import os
import random
import re
import shutil
import subprocess
import sys

TOOL = "c2-r50-session-gate.py"
GATE_REL = "quality/check-session-material.py"
BASE_REV = "8ae47b957034ae21012bbf09173cca2c48be345e"
BASE_GATE_SHA256 = "82c9053ae2e8b7db2fb8c0e195c32b8b151a593cf9412dcae3589427ac2dfa6f"
V2_CASE_NAMES_SHA256 = "38a8b2c647665b68ae4d3b7692e7ffaf9ca959fc1cdfe03b21deb5bd8097e725"
MIN_SELFTEST_CASES = 94
MIN_REPOS = 40
RUN_TIMEOUT = 180
FORBIDDEN_WORK = ("/tmp", "/var/tmp", "/dev/shm")

R7 = "R7_HOME_PATH_PREFIX"
R8 = "R8_ACCOUNT_COLUMN"
R9 = "R9_EXEC_CACHE"

# The 69 case names the v2 gate (`git show 8ae47b95:quality/check-session-material.py`,
# sha256 82c9053a...) prints for `--selftest`, sorted; sha256 of the newline-joined
# list is V2_CASE_NAMES_SHA256 and the same bytes are in `v2-selftest-cases.txt`.
V2_CASE_NAMES = (
    "e2e-empty-ufo-clean",
    "e2e-exit-1-on-findings",
    "e2e-fixture-files-count",
    "e2e-negative-repo-exit-0",
    "e2e-no-rule-can-be-dropped",
    "e2e-outside-ufo-not-scanned",
    "e2e-positive-files-rules",
    "e2e-projected-tree-passes",
    "e2e-r6-hits-every-carrier",
    "e2e-r6-output-never-holds-value",
    "e2e-scope-all-sees-outside-ufo",
    "e2e-summary-format",
    "prose-serial-unmarked-kept",
    "r1-class-only-not-a-finding",
    "r1-embedded-fenced-one-client",
    "r1-empty-title-not-a-finding",
    "r1-monitor-rule-line-clean",
    "r1-prose-keys-not-a-finding",
    "r1-seven-key-projection-clean",
    "r1-whole-file-two-clients",
    "r2-prose-without-pid-clean",
    "r2-two-process-rows",
    "r3-empty-serial-clean",
    "r3-monitor-identity",
    "r4-inline-paths-clean",
    "r4-limit-threshold-inclusive-at-12",
    "r4-three-entry-listing-under-limit",
    "r4-twelve-entry-listing",
    "r5-detail-masks-token",
    "r5-glued-to-prefix-clean",
    "r5-iso-timestamp-clean",
    "r5-json-serial-without-ident",
    "r5-lowercase-run-clean",
    "r5-prose-serial",
    "r5-prose-without-serial-clean",
    "r5-table-cell-serial",
    "r5-two-letter-capital-run-clean",
    "r6-absent-clean",
    "r6-detail-counts-only",
    "r6-exact-in-prose",
    "r6-exact-shape-independent",
    "rules-partition-is-waivable-plus-serial",
    "self-source-serial-rules-clean",
    "serials-from-json-empty-ignored",
    "serials-from-json-one-value",
    "serials-from-json-rejects-garbage",
    "serials-from-json-short-ignored",
    "waiver-exit-0-and-count-line",
    "waiver-fixture-waived",
    "waiver-gate-copy-mismatch-rejected",
    "waiver-gate-copy-waived",
    "waiver-marker-cannot-name-serial-rule",
    "waiver-no-waivers-flag-keeps-finding",
    "waiver-path-outside-waves-rejected",
    "waiver-per-rule-only-listed-rule",
    "waiver-real-serial-marked-file-kept",
    "waiver-real-values-rejected",
    "waiver-registry-in-ufo-refused",
    "waiver-serial-rejection-is-printed",
    "waiver-serial-rule-not-waivable",
    "waiver-sha-mismatch-rejected",
    "waiver-tamper-after-waiver-keeps-finding",
    "waiver-title-bare-demo-rejected",
    "waiver-title-case-only-rejected",
    "waiver-title-example-domain-rejected",
    "waiver-title-probe-prefix-rejected",
    "waiver-title-reserved-exact-waived",
    "waiver-title-reserved-prefix-waived",
    "waiver-unregistered-rejected",
)

# Red families: the covered shapes of R7-R9 (shapes.md §2, draft selftest).
RED_FAMILIES = ("r7-prefix", "r7-header", "r7-diag", "r7-row", "r8-account", "r9-cache")
# Green families: the shapes the gate must never flag.
GREEN_FAMILIES = (
    "g-tilde",
    "g-dollar-home",
    "g-prose",
    "g-numeric-ids",
    "g-one-field",
    "g-indented-usage",
    "g-masked-prefix",
)

WORDS = (
    "alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel",
    "india", "juliet", "kilo", "lima", "mike", "november", "oscar", "papa",
    "quebec", "romeo", "sierra", "tango", "uniform", "victor", "whiskey",
    "xray", "yankee", "zulu",
)

SELFTEST_CASE_RE = re.compile(r"^SELFTEST (?:ok|FAIL) case=(\S+)")
SELFTEST_TOTAL_RE = re.compile(r"^SELFTEST: passed=(\d+)/(\d+) failed=(\d+)")


class CounterError(Exception):
    pass


def _die(message):
    sys.stderr.write("%s: error: %s\n" % (TOOL, message))
    raise SystemExit(2)


def forbidden_root(path):
    """Return the forbidden prefix *path* sits under, or None."""
    real = os.path.realpath(os.path.abspath(path))
    for bad in FORBIDDEN_WORK:
        if real == bad or real.startswith(bad + os.sep):
            return bad
    return None


def child_env(work):
    """Environment for every child: identity, cache and temp state under *work*."""
    home = os.path.join(work, "home")
    return {
        "PATH": os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin"),
        "HOME": home,
        "XDG_CACHE_HOME": os.path.join(home, ".cache"),
        "XDG_CONFIG_HOME": os.path.join(home, ".config"),
        "XDG_DATA_HOME": os.path.join(home, ".local", "share"),
        "XDG_STATE_HOME": os.path.join(home, ".local", "state"),
        "TMPDIR": os.path.join(work, "tmp"),
        "LC_ALL": "C",
        "LANG": "C",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_TERMINAL_PROMPT": "0",
    }


def prepare_work(work):
    for leaf in ("tmp", "gates", os.path.join("home", ".cache"),
                 os.path.join("home", ".config"), os.path.join("home", ".local", "share"),
                 os.path.join("home", ".local", "state")):
        os.makedirs(os.path.join(work, leaf), exist_ok=True)


def git(env, repo, *args, what="git"):
    proc = subprocess.run(
        ["git", "-C", repo] + list(args),
        capture_output=True, env=env, timeout=RUN_TIMEOUT,
    )
    if proc.returncode != 0:
        raise CounterError(
            "%s failed (%s): %s" % (what, " ".join(args[:2]),
                                    proc.stderr.decode("utf-8", "replace").strip()[:300])
        )
    return proc.stdout


def resolve_rev(env, repo, rev):
    out = git(env, repo, "rev-parse", "--verify", rev + "^{commit}", what="rev-parse")
    return out.decode("ascii", "replace").strip()


def read_gate(env, repo, rev):
    path = "%s:%s" % (rev, GATE_REL)
    try:
        data = git(env, repo, "show", path, what="git show")
    except CounterError as exc:
        _die("%s not readable at %s: %s" % (GATE_REL, rev, exc))
    if not data.strip():
        _die("%s is empty at %s" % (GATE_REL, rev))
    return data


def run_cmd(argv, env, work):
    try:
        proc = subprocess.run(argv, capture_output=True, env=env, cwd=work,
                              timeout=RUN_TIMEOUT)
    except subprocess.TimeoutExpired:
        return {"rc": None, "out": "", "err": "timeout after %ds" % RUN_TIMEOUT}
    return {
        "rc": proc.returncode,
        "out": proc.stdout.decode("utf-8", "replace"),
        "err": proc.stderr.decode("utf-8", "replace"),
    }


def run_selftest(interp, gate, env, work):
    result = run_cmd([interp, "-I", gate, "--selftest"], env, work)
    names = []
    passed = total = failed = None
    for line in result["out"].splitlines():
        match = SELFTEST_CASE_RE.match(line)
        if match is not None:
            names.append(match.group(1))
            continue
        match = SELFTEST_TOTAL_RE.match(line)
        if match is not None:
            passed, total, failed = (int(match.group(1)), int(match.group(2)),
                                     int(match.group(3)))
    result.update(names=names, passed=passed, total=total, failed=failed)
    return result


def run_gate(interp, gate, env, work, repo, account=None, scope=None):
    argv = [interp, "-I", gate, "--repo", repo, "--rev", "HEAD"]
    if account:
        argv += ["--account", account]
    if scope:
        argv += ["--scope", scope]
    result = run_cmd(argv, env, work)
    findings = 0
    files = None
    rules = set()
    for line in result["out"].splitlines():
        if line.startswith("FINDING "):
            findings += 1
            for token in line.split():
                if token.startswith("rule="):
                    rules.add(token[len("rule="):])
        elif line.startswith("SESSION_MATERIAL:"):
            for token in line.split():
                if token.startswith("files="):
                    try:
                        files = int(token[len("files="):])
                    except ValueError:
                        files = None
    result.update(findings=findings, files=files, rules=rules)
    return result


def make_repo(env, root, name, relpath, content):
    repo = os.path.join(root, name)
    os.makedirs(repo, exist_ok=True)
    git(env, repo, "init", "-q", what="init")
    top = git(env, repo, "rev-parse", "--show-toplevel", what="toplevel").decode(
        "utf-8", "replace").strip()
    if os.path.realpath(top) != os.path.realpath(repo):
        raise CounterError("fixture toplevel %r != %r" % (top, repo))
    target = os.path.join(repo, relpath)
    os.makedirs(os.path.dirname(target) or repo, exist_ok=True)
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(content)
    git(env, repo, "add", "-A", what="add")
    git(env, repo, "-c", "user.name=mado-fixture", "-c", "user.email=fixture@shokunin.invalid",
        "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null",
        "commit", "-q", "-m", "fixture", what="commit")
    top = git(env, repo, "rev-parse", "--show-toplevel", what="toplevel").decode(
        "utf-8", "replace").strip()
    if os.path.realpath(top) != os.path.realpath(repo):
        raise CounterError("fixture toplevel moved to %r" % (top,))
    return repo


def synthetic_home(rng):
    return "/home/someone%03d" % rng.randrange(100, 1000)


def synthetic_account(rng):
    return "fixture%04d" % rng.randrange(1000, 10000)


def red_shape(family, rng):
    """Return {rel, content, rule, account} for one instance of one red shape."""
    home = synthetic_home(rng)
    word = rng.choice(WORDS)
    rel = "receipts/scan-%s-%s.txt" % (word, rng.randrange(100, 999))
    if family == "r7-prefix":
        content = "%s/Projects/%s/%s.py:%d: SyntaxWarning: invalid escape sequence\n" % (
            home, word, word, rng.randrange(2, 400))
        return {"rel": rel, "content": content, "rule": R7, "account": None}
    if family == "r7-header":
        sub = rng.choice((".local/share/applications", ".cache/xdg-terminal-exec",
                          "Documents/%s" % word, ".config/%s" % word))
        return {"rel": rel, "content": "%s/%s/:\n" % (home, sub), "rule": R7,
                "account": None}
    if family == "r7-diag":
        content = 'xkbcommon: INFO: could not open "%s/.config/%s.kc"\n' % (home, word)
        return {"rel": rel, "content": content, "rule": R7, "account": None}
    if family == "r7-row":
        content = "-rw-r--r-- 1 root root %d Oct 26 19:50 %s/%s.txt\n" % (
            rng.randrange(100, 900000), home, word)
        return {"rel": rel, "content": content, "rule": R7, "account": None}
    if family == "r8-account":
        account = synthetic_account(rng)
        content = "-rw-r--r-- 1 %s %s %d Oct 26 19:50 xdg-terminal-exec\n" % (
            account, account, rng.randrange(100, 900000))
        return {"rel": rel, "content": content, "rule": R8, "account": account}
    if family == "r9-cache":
        content = "--dir=%s/%s\n--title=%s window title\n" % (home, word, word)
        return {"rel": rel, "content": content, "rule": R9, "account": None}
    raise CounterError("unknown red family %r" % (family,))


def green_shape(family, rng):
    """Return {rel, content} for one instance of one counter-shape."""
    home = synthetic_home(rng)
    user = home.rsplit("/", 1)[1]
    word = rng.choice(WORDS)
    rel = "notes/%s-%d.txt" % (word, rng.randrange(100, 999))
    if family == "g-tilde":
        return {"rel": rel, "content": "Copied ~/Projects/%s to ~/Backups/%s and stopped.\n"
                % (word, word)}
    if family == "g-dollar-home":
        return {"rel": rel, "content":
                "The config sits at $HOME/.config/hypr/hyprland.conf and "
                "$HOME/.config/waybar/config.\n"}
    if family == "g-prose":
        return {"rel": rel, "content":
                "The tool wrote %s/%s.txt then %s/%s.txt and moved on.\n"
                % (home, word, home, word)}
    if family == "g-numeric-ids":
        return {"rel": rel, "content": "-rw-r--r-- 1 %d %d %d Oct 26 19:50 xdg-terminal-exec\n"
                % (rng.randrange(1000, 2000), rng.randrange(1000, 2000),
                   rng.randrange(100, 900000))}
    if family == "g-one-field":
        return {"rel": rel, "content": "--title=%s window title\n" % word}
    if family == "g-indented-usage":
        return {"rel": rel, "content":
                "  --dir=DIR      where the command runs\n"
                "  --title=TITLE  window title\n"}
    if family == "g-masked-prefix":
        return {"rel": rel, "content":
                "~/Projects/%s/%s.py:12: SyntaxWarning: invalid escape sequence\n"
                % (word, word)}
    raise CounterError("unknown green family %r" % (family,))


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog=TOOL,
        description="PRED-C2-r50: score the session-material gate at a revision.",
    )
    parser.add_argument("--repo", required=True, help="git repository holding the gate")
    parser.add_argument("--rev", required=True, help="revision whose gate bytes are scored")
    parser.add_argument("--work", required=True,
                        help="sandbox dir (HOME, XDG_*, TMPDIR and fixtures live here)")
    parser.add_argument("--nonce", required=True, type=int,
                        help="nonce seeding the fixture names, paths and counts")
    args = parser.parse_args(argv)

    bad = forbidden_root(args.work)
    if bad is not None:
        _die("--work %r is under %s; use a scratch dir" % (args.work, bad))
    invoking_home = os.environ.get("HOME")
    if invoking_home:
        home_real = os.path.realpath(os.path.abspath(invoking_home))
        work_real = os.path.realpath(os.path.abspath(args.work))
        if work_real == home_real or work_real.startswith(home_real + os.sep):
            _die("--work is under the invoking home (~); point it at a scratch dir "
                 "outside home state")
    inherited = os.environ.get("TMPDIR")
    if inherited:
        bad = forbidden_root(inherited)
        if bad is not None:
            _die("TMPDIR %r is inherited under %s; unset it" % (inherited, bad))

    work = os.path.realpath(os.path.abspath(args.work))
    os.makedirs(work, exist_ok=True)
    prepare_work(work)
    env = child_env(work)
    interp = sys.executable or "python3"

    rev = resolve_rev(env, args.repo, args.rev)
    gate_bytes = read_gate(env, args.repo, args.rev)
    gate_sha = hashlib.sha256(gate_bytes).hexdigest()
    gate = os.path.join(work, "gates", "gate-%s.py" % gate_sha[:12])
    with open(gate, "wb") as handle:
        handle.write(gate_bytes)
    supports_account = b"--account" in gate_bytes
    supports_scope = b'"--scope"' in gate_bytes

    print("PRED-C2-r50-GATE: rev=%s sha256=%s bytes=%d interp=%s account=%s scope=%s"
          % (rev, gate_sha, len(gate_bytes), os.path.basename(interp),
             "flag" if supports_account else "no-flag",
             "flag" if supports_scope else "no-flag"))

    # ---- clause s
    selftest = run_selftest(interp, gate, env, work)
    got_names = set(selftest["names"])
    wanted = set(V2_CASE_NAMES)
    present = len(wanted & got_names)
    missing = sorted(wanted - got_names)
    if selftest["passed"] is None:
        selftest_ok = False
        selftest_token = "crashed"
    else:
        passed, total, failed = selftest["passed"], selftest["total"], selftest["failed"]
        selftest_ok = (failed == 0 and passed == total and total >= MIN_SELFTEST_CASES
                       and not missing)
        selftest_token = "%d/%d" % (passed, total)
    print("PRED-C2-r50-SELFTEST: passed=%s failed=%s cases=%d rc=%r"
          % (selftest_token, selftest["failed"], len(selftest["names"]), selftest["rc"]))
    print("PRED-C2-r50-NAMES: v2_expected=%d present=%d missing=%d%s"
          % (len(wanted), present, len(missing),
             "" if not missing else " first=" + missing[0]))

    rng = random.Random(args.nonce)
    k_red = MIN_REPOS + (abs(args.nonce) % 5)
    k_green = MIN_REPOS + ((abs(args.nonce) // 7) % 5)
    fixtures = os.path.join(work, "fixtures-%d" % abs(args.nonce))
    if os.path.isdir(fixtures):
        shutil.rmtree(fixtures, ignore_errors=True)
    os.makedirs(fixtures)

    try:
        # ---- clause r: one instance of one covered shape per repository
        red_ok = 0
        red_by_family = dict((name, [0, 0]) for name in RED_FAMILIES)
        for index in range(k_red):
            family = RED_FAMILIES[index % len(RED_FAMILIES)]
            shape = red_shape(family, rng)
            repo = make_repo(env, fixtures, "red-%03d-%s" % (index, family),
                             shape["rel"], shape["content"])
            account = shape["account"]
            if account:
                gate_account = account if supports_account else None
            else:
                gate_account = synthetic_account(rng) if supports_account else None
            result = run_gate(interp, gate, env, work, repo, account=gate_account)
            ok = (result["rc"] not in (0, None) and result["findings"] >= 1
                  and shape["rule"] in result["rules"])
            red_by_family[family][0] += 1 if ok else 0
            red_by_family[family][1] += 1
            if ok:
                red_ok += 1
            else:
                print("RED_MISS repo=red-%03d-%s rule=%s rc=%r findings=%d rules=%s"
                      % (index, family, shape["rule"], result["rc"], result["findings"],
                         ",".join(sorted(result["rules"])) or "-"))
        print("PRED-C2-r50-RED: ok=%d/%d families=%s"
              % (red_ok, k_red,
                 " ".join("%s=%d/%d" % (name, red_by_family[name][0], red_by_family[name][1])
                          for name in RED_FAMILIES)))

        # ---- clause g: the counter-shapes stay clean
        green_ok = 0
        green_by_family = dict((name, [0, 0]) for name in GREEN_FAMILIES)
        neutral_account = synthetic_account(rng)
        for index in range(k_green):
            family = GREEN_FAMILIES[index % len(GREEN_FAMILIES)]
            shape = green_shape(family, rng)
            repo = make_repo(env, fixtures, "green-%03d-%s" % (index, family),
                             shape["rel"], shape["content"])
            result = run_gate(interp, gate, env, work, repo,
                              account=neutral_account if supports_account else None)
            ok = (result["rc"] == 0 and result["findings"] == 0
                  and (result["files"] or 0) >= 1)
            green_by_family[family][0] += 1 if ok else 0
            green_by_family[family][1] += 1
            if ok:
                green_ok += 1
            else:
                print("GREEN_MISS repo=green-%03d-%s rc=%r files=%r findings=%d rules=%s"
                      % (index, family, result["rc"], result["files"],
                         result["findings"],
                         ",".join(sorted(result["rules"])) or "-"))
        print("PRED-C2-r50-GREEN: ok=%d/%d families=%s"
              % (green_ok, k_green,
                 " ".join("%s=%d/%d" % (name, green_by_family[name][0], green_by_family[name][1])
                          for name in GREEN_FAMILIES)))

        # ---- clause d: the default scope sees a file outside .ufo/
        scope_shape = red_shape("r7-prefix", rng)
        scope_shape["rel"] = "docs/receipt.txt"
        scope_repo = make_repo(env, fixtures, "scope-outside-ufo", scope_shape["rel"],
                               scope_shape["content"])
        scope_default = run_gate(interp, gate, env, work, scope_repo,
                                 account=synthetic_account(rng) if supports_account else None)
        default_ok = (scope_default["findings"] >= 1 and scope_default["rc"] not in (0, None))
        ufo_note = "not-probed"
        scope_ok = default_ok
        if supports_scope:
            scope_ufo = run_gate(interp, gate, env, work, scope_repo, scope="ufo")
            ufo_clean = (scope_ufo["findings"] == 0 and scope_ufo["rc"] == 0
                         and scope_ufo["files"] == 0)
            ufo_note = "%d files findings=%d rc=%r" % (
                scope_ufo["files"] if scope_ufo["files"] is not None else -1,
                scope_ufo["findings"], scope_ufo["rc"])
            scope_ok = scope_ok and ufo_clean
        print("PRED-C2-r50-SCOPE: default_files=%s default_findings=%d default_rc=%r ufo=%s"
              % (scope_default["files"], scope_default["findings"], scope_default["rc"],
                 ufo_note))
    finally:
        shutil.rmtree(fixtures, ignore_errors=True)

    verdict = "TARGET_MET" if (selftest_ok and red_ok == k_red and k_red >= MIN_REPOS
                               and green_ok == k_green and k_green >= MIN_REPOS
                               and scope_ok) else "TARGET_MISSED"
    print("PRED-C2-r50: selftest=%s names=%d/%d red=%d/%d green=%d/%d scope=%s "
          "verdict=%s rev=%s"
          % (selftest_token, present, len(wanted), red_ok, k_red, green_ok, k_green,
             "seen" if scope_ok else "blind", verdict, rev))
    return 0 if verdict == "TARGET_MET" else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except CounterError as exc:
        _die(str(exc))
