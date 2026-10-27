#!/usr/bin/env python3
"""RevGateV3 round-50 w1: rebuild the nonce red/green fixture repos.

Usage: python3 nonce-fixture-builder.py SCRATCH-DIR
Creates SCRATCH-DIR/nonce-fixture (red+green classes) and SCRATCH-DIR/nonce-probe
(evasion classes). Every identity is synthetic. Run the gates with
--repo <dir> --rev HEAD --scope all; for the R8 rows pass --account nxacct7.
Never commit raw output of these fixtures beyond rule/count lines.
"""
import os, shutil, subprocess, sys

S = os.path.abspath(sys.argv[1])
U, A = "nxreviewer7", "nxacct7"

def repo(name, files):
    root = os.path.join(S, name)
    shutil.rmtree(root, ignore_errors=True)
    for rel, text in files.items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as fh:
            fh.write(text)
    for args in (["init", "-q"], ["add", "-A"]):
        subprocess.run(["git", "-C", root] + args, check=True)
    subprocess.run(["git", "-C", root, "-c", "user.name=fixture",
                    "-c", "user.email=fixture@invalid", "commit", "-qm", "fx"],
                   check=True)
    top = subprocess.run(["git", "-C", root, "rev-parse", "--show-toplevel"],
                         check=True, capture_output=True, text=True).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(root), top
    return root

R = ".ufo/waves/rx/receipts/"
fix = repo("nonce-fixture", {
    R+"leak-grep.txt":   ("/home/%s/proj/wave/log.txt:41:computed step\n"
                          "/home/%s/proj/wave/log.txt:42:second step\n"
                          "/home/%s/proj/wave/log.txt:43:third step\n") % (U, U, U),
    R+"leak-header.txt": "/home/%s/backups/tue/:\n    f1.txt\n    f2.txt\n" % U,
    R+"leak-diag.txt":   'git: fatal: cannot chdir to "/home/%s/x": No such file or directory\n' % U,
    R+"leak-ls.txt":     "-rw-r--r-- 1 %s %s 512 Oct 26 09:15 /home/%s/notes/a.txt\n" % (A, A, U),
    R+"leak-cache.txt":  ("--title=nx window one\n--working-directory=/home/%s\n"
                          "--app-id=nx.term\n") % U,
    "docs/red-outside.txt": "/home/%s/elsewhere/cfg.txt:9:located line outside ufo\n" % U,
    R+"green-tilde.md":  ("Wrote the config under ~/notes/a.txt and set $HOME/.config/foo.\n"
                          "The shell expanded ~ to the home prefix; ~ alone means home.\n"),
    R+"green-prose-paths.md": ("I moved /home/%s/a.txt aside, then /home/%s/b.txt and "
                               "/home/%s/c.txt were fine.\n") % (U, U, U),
    R+"green-numeric-ids.txt": ("-rw-r--r-- 1 1000 1000 512 Oct 26 09:15 /srv/build/plan.txt\n"
                                "uid=1000 gid=1000 groups=1000\n"),
    R+"green-indented-usage.txt": ("usage: nxtool [options]\n  --title=TITLE      window title\n"
                                   "  --working-directory=DIR\n"),
    R+"green-one-field.txt": "--title=only one doc line\n",
    R+"green-other-owner.txt": "-rw-r--r-- 1 root root 244104 Oct 20 09:39 /var/log/pacman.log\n",
})
probe = repo("nonce-probe", {
    R+"miss-spaced-path.txt": "/home/%s/my notes/f.txt:7:content with space in path\n" % U,
    R+"miss-single-quote.txt": "apt: error: cannot stat '/home/%s/x': No such file\n" % U,
    R+"miss-colon-path.txt": "/home/%s/a:b.txt:3:colon inside name\n" % U,
    R+"green-diag-upper-prog.txt": 'Git: fatal: cannot chdir to "/home/%s/y": No such file\n' % U,
})
print(fix)
print(probe)
