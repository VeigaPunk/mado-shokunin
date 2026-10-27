#!/usr/bin/env python3
"""Check every self-test keymap against the judge, on three paths.

For each self-test case that carries a keymap and both contract flags:

  raw     the keymap text in mado-keysym.py's --selftest (what the self-test parses)
  compiled  `xkbcli compile-keymap` output for that raw text (what the judge gets)

runs (1) the judge on `compiled`, (2) mado-keysym.py on `compiled`, (3) mado-keysym.py on `raw`,
and requires the three stdout/rc triples to be identical. Cases where the case itself expects a
refusal (exit 2/1) are checked against the judge only when the judge has the same flags.

Usage: validate_synthetic.py <workdir> <receipt-file>
"""
import importlib.util
import os
import subprocess
import sys

COMPILE = "/usr/lib/xkbcommon/xkbcli-compile-keymap"
JUDGE = "/usr/lib/xkbcommon/xkbcli-how-to-type"
HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "mado-keysym.py")

spec = importlib.util.spec_from_file_location("mado_keysym", TOOL)
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)


def main():
    work = sys.argv[1]
    receipt = sys.argv[2]
    home = os.path.join(work, "home")
    cache = os.path.join(work, "cache")
    for path in (home, os.path.join(home, ".config"), cache, os.path.join(work, "lang")):
        os.makedirs(path, exist_ok=True)
    env = {"PATH": "/usr/bin", "HOME": home, "XDG_CONFIG_HOME": os.path.join(home, ".config"),
           "XDG_CACHE_HOME": cache, "LC_ALL": "C"}
    lines = []
    failures = []
    for index, (name, keymap_text, argv_tail, expected_stdout, expected_rc) in enumerate(
            tool._cases()):
        if not isinstance(keymap_text, str) or keymap_text in ("MISSING", ""):
            lines.append("%-34s skip (no keymap text)" % name)
            continue
        raw_path = os.path.join(work, "%03d-raw.kmap" % index)
        compiled_path = os.path.join(work, "%03d.kmap" % index)
        with open(raw_path, "w", encoding="utf-8") as handle:
            handle.write(keymap_text)
        with open(raw_path, "rb") as handle:
            compiled = subprocess.run([COMPILE], stdin=handle, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE, env=env)
        if compiled.returncode != 0:
            failures.append((name, "compile", compiled.returncode,
                             compiled.stderr.decode("utf-8", "replace").splitlines()[:2]))
            lines.append("%-34s COMPILE FAILED" % name)
            continue
        with open(compiled_path, "wb") as handle:
            handle.write(compiled.stdout)

        def judge(path):
            return subprocess.run([JUDGE, "--keymap=" + path] + list(argv_tail),
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)

        def ours(path):
            return subprocess.run([sys.executable, "-I", TOOL, "how-to-type", "--keymap", path]
                                  + list(argv_tail), stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, env=env)

        j_compiled = judge(compiled_path)
        o_compiled = ours(compiled_path)
        o_raw = ours(raw_path)
        ok = (j_compiled.stdout == o_compiled.stdout
              and j_compiled.returncode == o_compiled.returncode == o_raw.returncode
              and o_compiled.stdout == o_raw.stdout)
        lines.append("%-34s judge_rc=%d ours_compiled_rc=%d ours_raw_rc=%d %s"
                     % (name, j_compiled.returncode, o_compiled.returncode, o_raw.returncode,
                        "ok" if ok else "DIFF"))
        if not ok:
            failures.append((name, "diff", j_compiled.stdout, o_compiled.stdout, o_raw.stdout))

    with open(receipt, "w", encoding="utf-8") as handle:
        handle.write("# each self-test keymap: judge(compiled) == ours(compiled) == ours(raw)\n")
        for line in lines:
            handle.write(line + "\n")
    for failure in failures[:20]:
        print("FAIL", failure[0], failure[1])
        if len(failure) > 3:
            print("  judge:", (failure[2] or b"")[:400])
            print("  compiled:", (failure[3] or b"")[:400])
            print("  raw:", (failure[4] or b"")[:400])
        else:
            print(" ", failure[2], failure[3])
    print("%d cases, %d failures" % (len(lines), len(failures)))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
