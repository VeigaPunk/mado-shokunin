#!/usr/bin/env python3
"""Kill-verification for ALL C2-claim survivors of the round-56 w2 mutation run (seat R56W2MutC2ToolA).

For every mutant the UNCHANGED C2 claim harness does not kill, build the smallest candidate fixture that separates
the mutant from the pristine tool, then run BOTH through the harness' own staged_run (bwrap sandbox, empty cwd,
staged tree, {FX} = <stage>) and compare stdout bytes and exit status.

Usage: python3 -I kill2.py --repo DIR --work DIR --out DIR
"""
import json
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mutate import MUTANTS, TOOL_REL  # noqa: E402

SAFE_PATH = "/usr/local/bin:/usr/bin:/bin"
BIG = 1048576

# proposal id -> (mutant id, description, files {relpath: bytes | ("symlink", target)}, args)
PROPOSALS = [
    # ---- the nine that survive BOTH the C2 claim harness and --selftest -------------
    ("K16", "M16", "a full-line comment is skipped and must not push the category stack",
     {"hyprland.conf": b"# note {\nmisc:disable_autoreload = 1\n"},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}"]),
    ("K17", "M17", "same: the `#` comment rule is part of the model",
     {"hyprland.conf": b"# note {\nmisc:disable_autoreload = 1\n"},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}"]),
    ("K27", "M27", "a `$` in the value line is unsupported: `on$x` must not parse as 1",
     {"hyprland.conf": b"misc:disable_autoreload = on$x\n"},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}"]),
    ("K28", "M28", "a `{` in the value line is unsupported: `on{` must not parse as 1",
     {"hyprland.conf": b"misc:disable_autoreload = on{\n"},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}"]),
    ("K29", "M29", "a backslash in the value line is unsupported: `off\\` must not parse as 0",
     {"hyprland.conf": b"misc:disable_autoreload = off\\\n"},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}"]),
    ("K44", "M44", "an inaccessible match aborts the REST of that line's matches (dangling symlink first)",
     {"hyprland.conf": b"source = mix/*.conf\n",
      "mix/a-broken.conf": ("symlink", "missing-target.conf"),
      "mix/z.conf": b"x = 1\n"},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}"]),
    ("K50", "M50", "a dangling symlink --config lexists -> type=file, not type=missing",
     {"hyprland.conf": ("symlink", "missing.conf")},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}"]),
    ("K56", "M56", "--display-root that is a symlink path with a trailing slash (the given text loses its `/`)",
     {"real/x.conf": b"x = 1\n",
      "link": ("symlink", "real"),
      "real/hyprland.conf": b"misc:disable_autoreload = 0\n"},
     ["--config", "{FX}/tree/link/hyprland.conf", "--display-root", "{FX}/tree/link/"]),
    ("K57", "M57", "the canonical watch path is printed through the display root's realpath",
     {"real/x.conf": b"x = 1\n",
      "lnk.conf": ("symlink", "real/x.conf"),
      "link": ("symlink", "real"),
      "hyprland.conf": b"source = lnk.conf\n"},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}/tree/link"]),
    ("K63", "M63", "--getoption on a non-regular but readable file is `unreadable`",
     {"hyprland.conf": b"misc:disable_autoreload = 0\n"},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}", "--getoption", "/dev/null"]),
    # ---- batch-2 survivors ------------------------------------------------------
    ("K71", "M71", "a `;`-first line is NOT a comment: it is an ordinary line",
     {"hyprland.conf": b"; note {\nmisc:disable_autoreload = 1\n"},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}"]),
    ("K73", "M73", "a stray `}` on an empty stack is ignored (the pop is guarded)",
     {"hyprland.conf": b"}\nmisc:disable_autoreload = 1\n"},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}"]),
    ("K76", "M76", "the value side of `=` is not stripped of `!`",
     {"hyprland.conf": b"misc:disable_autoreload = 1!\n"},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}"]),
    ("K77", "M77", "`source` inside a category is `unsupported` (the stack is non-empty)",
     {"hyprland.conf": b"misc {\n  source = x.conf\n}\n",
      "x.conf": b"a = 1\n"},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}"]),
    ("K78", "M78", "`##` in the VALUE is unsupported (and only in the value)",
     {"hyprland.conf": b"misc:disable_autoreload = 1 ## x\n"},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}"]),
    ("K79", "M79", "the `$` check applies to the whole LINE, not just the RHS",
     {"hyprland.conf": b"misc:disable_autoreload = 1 $ x\n"},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}"]),
    ("K80", "M80", "the `$` check applies to the whole LINE (a `$` in the LHS counts)",
     {"hyprland.conf": b"misc:disable_autoreload$ = 1\n"},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}"]),
    ("K81", "M81", "a `$`-prefixed LHS is ignored (the whole LHS, not a prefix of it)",
     {"hyprland.conf": b"$ = 1\nmisc:disable_autoreload = 1\n"},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}"]),
    ("K83", "M83", "a source line with no match still reports ERROR nomatch",
     {"hyprland.conf": b"source = nothing/*.conf\n"},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}"]),
    ("K85", "M85", "a glob match is re-absolutised against the file holding the line",
     {"hyprland.conf": b"source = ../out/*.conf\n",
      "out/a.conf": b"x = 1\n"},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}"]),
    ("K89", "M89", "a dangling symlink in the list is type=file (lexists, not isfile)",
     {"hyprland.conf": ("symlink", "missing.conf")},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}"]),
    ("K90", "M90", "the canonical watch uses the strict realpath (a broken link has no canonical watch)",
     {"hyprland.conf": ("symlink", "missing.conf")},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}"]),
    ("K94", "M94", "--display-root without a trailing slash is used as given",
     {"real/x.conf": b"x = 1\n",
      "link": ("symlink", "real"),
      "real/hyprland.conf": b"misc:disable_autoreload = 0\n"},
     ["--config", "{FX}/tree/link/hyprland.conf", "--display-root", "{FX}/tree/link"]),
    ("K97", "M97", "a non-regular --getoption file is `unreadable` (not only a directory)",
     {"hyprland.conf": b"misc:disable_autoreload = 0\n"},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}", "--getoption", "/dev/null"]),
    ("K98", "M98", "the live value comes from the `int` key only",
     {"hyprland.conf": b"misc:disable_autoreload = 0\n",
      "go.json": b'{"option": "misc:disable_autoreload", "value": 1}\n'},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}", "--getoption", "{FX}/tree/go.json"]),
    ("K99", "M99", "no record for the option in the dump is UNKNOWN (live=?), not a silent 0",
     {"hyprland.conf": b"misc:disable_autoreload = 0\n",
      "go.json": b'{"option": "misc:x", "int": 0}\n'},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}", "--getoption", "{FX}/tree/go.json"]),
    ("K101", "M101", "a negative live int is still a record (the option is present)",
     {"hyprland.conf": b"misc:disable_autoreload = 0\n",
      "go.json": b'{"option": "misc:disable_autoreload", "int": -1}\n'},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}", "--getoption", "{FX}/tree/go.json"]),
    ("K104", "M104", "AGREE/DIFFER compares the live int with the config flag",
     {"hyprland.conf": b"misc:disable_autoreload = 0\n",
      "go.json": b'{"option": "misc:disable_autoreload", "int": 1}\n'},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}", "--getoption", "{FX}/tree/go.json"]),
    # ---- the thirteen that the claim harness misses but --selftest catches -------------
    ("K04", "M04", "a relative --config path is a usage error",
     {"hyprland.conf": b"misc:disable_autoreload = 0\n"},
     ["--config", "rel.conf", "--display-root", "{FX}"]),
    ("K06", "M06", "a file of exactly 1048576 bytes is read (MAX_BYTES is inclusive)",
     {"hyprland.conf": b"#" * BIG},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}"]),
    ("K07", "M07", "a file of 1048577 bytes is too_large (MAX_BYTES is inclusive)",
     {"hyprland.conf": b"#" * (BIG + 1)},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}"]),
    ("K11", "M11", "a file of exactly 1048576 bytes is read (the bound is `>` not `>=`)",
     {"hyprland.conf": b"#" * BIG},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}"]),
    ("K12", "M12", "a file of 1048577 bytes is too_large (the read takes MAX_BYTES+1)",
     {"hyprland.conf": b"#" * (BIG + 1)},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}"]),
    ("K18", "M18", "a stray `}` on an empty stack is ignored (no crash)",
     {"hyprland.conf": b"}\nmisc:disable_autoreload = 1\n"},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}"]),
    ("K26", "M26", "the value is stripped of spaces before parsing (`1 # x` -> 1)",
     {"hyprland.conf": b"misc:disable_autoreload = 1 # x\n"},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}"]),
    ("K33", "M33", "a value that only STARTS with digits is not an int",
     {"hyprland.conf": b"misc:disable_autoreload = 1abc\n"},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}"]),
    ("K54", "M54", "a directory watch carries the directory mask",
     {"hyprland.conf": b"misc:disable_autoreload = 0\n"},
     ["--config", "{FX}/tree", "--display-root", "{FX}"]),
    ("K55", "M55", "--display-root is a PATH prefix, not a string prefix",
     {"sub/keep.conf": b"x = 1\n",
      "sub2/hyprland.conf": b"misc:disable_autoreload = 0\n"},
     ["--config", "{FX}/tree/sub2/hyprland.conf", "--display-root", "{FX}/tree/sub"]),
    ("K60", "M60", "a bool `int` in the getoption dump is ignored (UNKNOWN, not AGREE)",
     {"hyprland.conf": b"misc:disable_autoreload = 0\n",
      "go.json": b'{"option": "misc:disable_autoreload", "int": false}\n'},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}", "--getoption", "{FX}/tree/go.json"]),
    ("K62", "M62", "no record for the option in the dump is UNKNOWN, not AGREE",
     {"hyprland.conf": b"misc:disable_autoreload = 0\n",
      "go.json": b'{"option": "misc:x", "int": 0}\n'},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}", "--getoption", "{FX}/tree/go.json"]),
    ("K93", "M93", "a directory watch carries the directory mask",
     {"hyprland.conf": b"misc:disable_autoreload = 0\n"},
     ["--config", "{FX}/tree", "--display-root", "{FX}"]),
    ("K96", "M96", "the display root's realpath is used without a trailing slash",
     {"real/x.conf": b"x = 1\n",
      "link": ("symlink", "real"),
      "real/hyprland.conf": b"misc:disable_autoreload = 0\n"},
     ["--config", "{FX}/tree/link/hyprland.conf", "--display-root", "{FX}/tree/link"]),
]


def mutant_of(mid):
    for x in MUTANTS:
        if x[0] == mid:
            return x
    raise KeyError(mid)


def build_stage(files, stage):
    tree = os.path.join(stage, "tree")
    os.makedirs(tree)
    for rel, content in files.items():
        path = os.path.join(tree, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if isinstance(content, tuple):
            os.symlink(content[1], path)
        else:
            with open(path, "wb") as fh:
                fh.write(content)
    return tree


def staged_run(python, program, args, stage, cwd, env):
    """the harness' own staged_run (quality/r56_ctl_c2.py) - bwrap when available."""
    bwrap = shutil.which("bwrap", path=SAFE_PATH)
    if bwrap:
        cmd = [bwrap, "--unshare-all", "--die-with-parent", "--ro-bind", "/usr", "/usr", "--symlink", "usr/lib", "/lib",
               "--symlink", "usr/lib64", "/lib64", "--symlink", "usr/bin", "/bin", "--dev", "/dev",
               "--ro-bind", stage, stage, "--ro-bind", program, program, "--tmpfs", "/w", "--chdir", "/w",
               python, "-I", program] + args
        p = subprocess.run(cmd, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, timeout=120)
        return p.stdout, p.returncode, p.stderr.decode("utf-8", "replace")
    p = subprocess.run([python, "-I", program] + args, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    return p.stdout, p.returncode, p.stderr.decode("utf-8", "replace")


def main(argv):
    repo = work = out = None
    i = 0
    while i < len(argv):
        if argv[i] == "--repo":
            repo = argv[i + 1]; i += 2
        elif argv[i] == "--work":
            work = argv[i + 1]; i += 2
        elif argv[i] == "--out":
            out = argv[i + 1]; i += 2
        else:
            print("usage: --repo DIR --work DIR --out DIR"); return 2
    os.makedirs(work, exist_ok=True)
    os.makedirs(out, exist_ok=True)
    pristine_path = os.path.join(repo, TOOL_REL)
    pristine = open(pristine_path, "rb").read()
    python = shutil.which("python3", path=SAFE_PATH)
    results = []
    for kid, mid, desc, files, args in PROPOSALS:
        m = mutant_of(mid)
        text = pristine.decode("utf-8")
        if text.count(m[2]) != 1:
            print("%-6s %-5s SKIP (snippet occurs %d times)" % (kid, mid, text.count(m[2])))
            continue
        mutant = text.replace(m[2], m[3]).encode("utf-8")
        mpath = os.path.join(out, "mutant-%s.py" % kid)
        with open(mpath, "wb") as fh:
            fh.write(mutant)
        stage = os.path.join(work, "stage-%s" % kid)
        shutil.rmtree(stage, ignore_errors=True)
        os.makedirs(stage)
        build_stage(files, stage)
        cwd = os.path.join(work, "cwd-%s" % kid)
        shutil.rmtree(cwd, ignore_errors=True)
        os.makedirs(cwd)
        env = {"PATH": SAFE_PATH, "HOME": cwd, "TMPDIR": cwd, "LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"}
        argv_real = [a.replace("{FX}", stage) for a in args]
        po, prc, perr = staged_run(python, pristine_path, argv_real, stage, cwd, env)
        mo, mrc, merr = staged_run(python, mpath, argv_real, stage, cwd, env)
        killed = (po != mo) or (prc != mrc)
        rec = {"proposal": kid, "mutant": mid, "desc": desc,
               "files": {k: (["symlink", v[1]] if isinstance(v, tuple) else "bytes:%d" % len(v))
                         for k, v in files.items()},
               "args": args, "pristine_rc": prc, "mutant_rc": mrc, "killed": bool(killed),
               "pristine_out": po.decode("utf-8", "replace"), "mutant_out": mo.decode("utf-8", "replace"),
               "mutant_err": merr.strip().splitlines()[-1:] if merr.strip() else []}
        results.append(rec)
        with open(os.path.join(out, "%s.txt" % kid), "w") as fh:
            fh.write("== proposal %s for mutant %s: %s\nargs: %s\nfiles: %s\n" % (kid, mid, desc, args, rec["files"]))
            fh.write("-- pristine (rc=%d)\n%s" % (prc, po.decode("utf-8", "replace")))
            fh.write("-- mutant %s (rc=%d)\n%s" % (mid, mrc, mo.decode("utf-8", "replace")))
            if merr.strip():
                fh.write("-- mutant stderr tail: %s\n" % merr.strip().splitlines()[-1])
            fh.write("VERDICT: %s\n" % ("KILLS" if killed else "DOES NOT KILL"))
        print("%-6s %-5s %-9s %s" % (kid, mid, "KILLS" if killed else "NO-KILL", desc))
    with open(os.path.join(out, "kill-results.json"), "w") as fh:
        json.dump(results, fh, indent=1)
    nk = [r["proposal"] for r in results if not r["killed"]]
    print("\nproposals: %d, kills: %d, no-kill: %s" % (len(results), len(results) - len(nk), nk or "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
