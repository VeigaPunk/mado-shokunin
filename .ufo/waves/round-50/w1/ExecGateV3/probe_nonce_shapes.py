#!/usr/bin/env python3
"""probe_nonce_shapes.py — nonce-generated fixture repos against the v3 gate.

Usage: probe_nonce_shapes.py GATE SCRATCH

This is the install-readiness probe, not the round-50 C2 counter: it builds two
throwaway git repositories under *SCRATCH* with values drawn from
``os.urandom`` (a home user, an account name, a cache title and a program name
that never existed before this run), then asks the gate two questions.

  red   the four covered shape classes — structural home path (prefix, header,
        diagnostic, ``ls`` row), the account owner/group column, exec-cache
        record fields, and material placed outside ``.ufo/`` — each on its own
        file, scanned through the *default* scope with ``--account NONCE``.
        Expect exit 1 and one finding line per carrier file.
  green ``~/`` and ``$HOME/`` located lines, a path quoted in prose, a path in
        a sentence, numeric ``ls`` ids, a root-owned row, a single cache field,
        run without ``--scope`` and without ``--account``. Expect exit 0.

Every run asserts that no nonce value reached stdout: the gate prints counts,
file paths and masked shapes only, and the account is never printed.

The fixture repository is asserted to be its own toplevel before its first
commit; both fixtures are committed with a throwaway identity passed as ``-c``
so no global git config is read or written. Nothing is written outside
*SCRATCH*.
"""
import os
import subprocess
import sys

GATE = os.path.abspath(sys.argv[1])
SCRATCH = os.path.abspath(sys.argv[2])

USER = "u" + os.urandom(5).hex()
ACCOUNT = "a" + os.urandom(5).hex()
TITLE = "Wn" + os.urandom(4).hex() + " Portal"
PROG = "probe" + os.urandom(3).hex()

RED = {
    # (file, rule, body)
    "receipts/grep.txt": (
        "R7",
        "\n".join([
            "/home/%s/.config/hypr/input.conf:5:  kb_layout = us" % USER,
            "/home/%s/.config/hypr/input.conf:8:  kb_variant = intl" % USER,
        ]) + "\n"),
    "receipts/flat-listing.txt": (
        "R7",
        "\n".join([
            "/home/%s/.local/share/applications:" % USER,
            "total 8",
            "-rw-r--r-- 1 1000 1000 87 Oct 27 10:00 term.desktop",
        ]) + "\n"),
    "receipts/diagnostic.txt": (
        "R7",
        "\n".join([
            'xkbcommon: INFO: Include path failed: "/home/%s/.xkb" (No such file)' % USER,
            '%s: note: "/home/%s/.cache" is absent' % (PROG, USER),
        ]) + "\n"),
    ".ufo/waves/nonce/w1/Seat/receipts/ls-row.txt": (
        "R7",
        "-rw-r--r-- 1 1000 1000 12 Oct 27 10:00 /home/%s/xdg-terminals.list\n" % USER),
    ".ufo/waves/nonce/w1/Seat/receipts/ls-owner.txt": (
        "R8",
        "\n".join([
            "-rw-r--r-- 1 %s %s  12 Oct 27 10:00 xdg-terminals.list" % (ACCOUNT, ACCOUNT),
            "drwxr-xr-x 1 %s %s  58 Oct 27 10:00 applications" % (ACCOUNT, ACCOUNT),
        ]) + "\n"),
    ".ufo/waves/nonce/w1/Seat/receipts/cache.txt": (
        "R9",
        "\n".join([
            "0" * 32,
            "/usr/bin/term",
            "--title=%s" % TITLE,
            "--working-directory=/home/%s" % USER,
            "--app-id=term",
        ]) + "\n"),
}

GREEN = {
    "receipts/masked.txt": "\n".join([
        "~/.config/hypr/input.conf:5:  kb_layout = us",
        "$HOME/.cache/log.txt:3: wrote 1 entry",
    ]) + "\n",
    "receipts/prose.txt": "\n".join([
        "The entry lives at `/home/%s/.config/hypr/input.conf`, in prose." % USER,
        "I read /home/%s/.cache/log.txt and it held one entry." % USER,
        'the tool said "/home/%s/.xkb" was missing.' % USER,
    ]) + "\n",
    "receipts/numeric.txt": "\n".join([
        "-rw-r--r-- 1 1000 1000 12 Oct 27 10:00 xdg-terminals.list",
        "-rw-r--r-- 1 root root 244104 Oct 20 09:39 /var/log/pacman.log",
        "Pass `--title=` to leave the title alone.",
    ]) + "\n",
}


def _git(root, *args):
    return subprocess.run(["git", "-C", root, *args], check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          text=True).stdout.strip()


def _repo(name, files):
    root = os.path.join(SCRATCH, name)
    os.makedirs(root, exist_ok=True)
    for relpath, text in files.items():
        target = os.path.join(root, relpath)
        os.makedirs(os.path.dirname(target) or root, exist_ok=True)
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(text)
    _git(root, "init", "-q")
    _git(root, "add", "-A")
    _git(root, "-c", "user.name=fixture", "-c", "user.email=fixture@scratch.invalid",
         "commit", "-q", "-m", "nonce fixture")
    top = _git(root, "rev-parse", "--show-toplevel")
    if os.path.realpath(top) != os.path.realpath(root):
        raise SystemExit("fixture toplevel %r != %r" % (top, root))
    return root


def _scan(root, extra):
    cmd = [sys.executable, "-I", GATE, "--repo", root, "--rev", "HEAD",
           "--no-waivers", *extra]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          timeout=300)
    return (proc.returncode,
            proc.stdout.decode("utf-8", "replace"),
            proc.stderr.decode("utf-8", "replace"),
            cmd)


def main():
    failures = []
    red_root = _repo("nonce-red", dict((path, body) for path, (_r, body) in RED.items()))
    green_root = _repo("nonce-green", GREEN)

    code, out, err, cmd = _scan(red_root, ("--account", ACCOUNT))
    print("== red rc=%d cmd=%s" % (code, " ".join(cmd[3:])))
    for line in out.splitlines():
        print("   " + line)
    if code != 1:
        failures.append("red rc=%d" % code)
    found = {}
    for line in out.splitlines():
        if line.startswith("FINDING file="):
            path = line.split("file=", 1)[1].split()[0]
            rule = line.split("rule=", 1)[1].split()[0]
            found[path] = rule
    for path, (tag, _body) in sorted(RED.items()):
        want = {"R7": "R7_HOME_PATH_PREFIX",
                "R8": "R8_ACCOUNT_COLUMN",
                "R9": "R9_EXEC_CACHE"}[tag]
        got = found.get(path)
        print("   expect %-48s %s got=%s %s" % (path, want, got,
                                                "ok" if got == want else "MISS"))
        if got != want:
            failures.append("%s want=%s got=%s" % (path, want, got))
    if "SESSION_MATERIAL: files=%d" % len(RED) not in out:
        failures.append("red files count: %r" % (out.splitlines()[-1:] or [],))

    code, out, err, cmd = _scan(green_root, ())
    print("== green rc=%d cmd=%s" % (code, " ".join(cmd[3:])))
    for line in out.splitlines():
        print("   " + line)
    if code != 0:
        failures.append("green rc=%d" % code)
    if "findings=0" not in out:
        failures.append("green not clean")

    for label, text in (("green", out), ):
        for secret in (USER, ACCOUNT, TITLE, PROG):
            if secret and secret in text:
                failures.append("%s stdout carries a nonce value" % label)

    # The account must also be silent on the *red* run: re-read that output.
    _code, red_out, _err, _cmd = _scan(red_root, ("--account", ACCOUNT))
    for secret in (USER, ACCOUNT, TITLE, PROG):
        if secret and secret in red_out:
            failures.append("red stdout carries a nonce value")
    print("PROBE: failures=%d" % len(failures))
    for item in failures:
        print("   FAIL %s" % item)
    return 0 if not failures else 1


sys.exit(main())
