#!/usr/bin/env python3
"""Check the embedded keysym tables against the judge, name by name and value by value.

  * every XKB_KEY_ name of the pinned header: judge `--keysym NAME` vs keysym_from_name/get_name
  * a sample of numeric keysyms across the whole 0..XKB_KEYSYM_MAX range plus the Unicode ranges

Usage: validate_keysyms.py <workdir> <receipt-file>
"""
import importlib.util
import os
import re
import subprocess
import sys

JUDGE = "/usr/lib/xkbcommon/xkbcli-how-to-type"
HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "mado-keysym.py")
HEADER = "/usr/include/xkbcommon/xkbcommon-keysyms.h"

spec = importlib.util.spec_from_file_location("mado_keysym", TOOL)
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)

LINE = re.compile(r"^keysym: (.*) \((0x[0-9a-f]+)\)$")


def judge(env, keymap, argument):
    return subprocess.run([JUDGE, "--keymap=" + keymap, "--disable-compose", "--keysym", argument],
                          stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=env)


def first_line(payload):
    lines = payload.decode("utf-8", "surrogateescape").splitlines()
    return lines[0] if lines else ""


def ours(argument):
    value = tool.resolve_argument(argument)
    if value is None:
        return 2, ""
    name = tool.keysym_get_name(value)
    if name is None:
        return 1, ""
    return 0, "keysym: %s (%s)" % (name, tool._hex_keysym(value))


def main():
    work, receipt = sys.argv[1], sys.argv[2]
    home = os.path.join(work, "home")
    for path in (home, os.path.join(home, ".config"), os.path.join(work, "cache")):
        os.makedirs(path, exist_ok=True)
    env = {"PATH": "/usr/bin", "HOME": home, "XDG_CONFIG_HOME": os.path.join(home, ".config"),
           "XDG_CACHE_HOME": os.path.join(work, "cache"), "LC_ALL": "C"}
    keymap = os.path.join(work, "us.kmap")
    with open(keymap, "wb") as handle:
        subprocess.run(["/usr/lib/xkbcommon/xkbcli-compile-keymap", "--layout", "us"],
                       stdout=handle, stderr=subprocess.DEVNULL, env=env)

    names = []
    with open(HEADER, encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("#define XKB_KEY_"):
                names.append(line[len("#define XKB_KEY_"):].split()[0])

    values = list(range(0x00, 0x300))
    values += list(range(0x1000000, 0x1000300))
    values += list(range(0x10ff00, 0x110100))
    values += list(range(0x13b0, 0x13d0))
    values += [0, 1, 0x7f, 0x80, 0xff, 0xffbd, 0xffbe, 0x1008ffb8, 0x1008ffb9,
               0x12345678, 0x1fffffff, 0x20000000]
    step = 0x1001
    values += list(range(0x400, 0x1000000, step))
    values = sorted(set(values))

    failures = []
    for name in names:
        result = judge(env, keymap, name)
        observed = (result.returncode, first_line(result.stdout))
        mine = ours(name)
        if observed != mine:
            failures.append(("name", name, observed, mine))
    name_checked = len(names)

    value_checked = 0
    for value in values:
        argument = "0x%x" % value
        result = judge(env, keymap, argument)
        observed = (result.returncode, first_line(result.stdout))
        mine = ours(argument)
        value_checked += 1
        if observed != mine:
            failures.append(("value", argument, observed, mine))

    with open(receipt, "w", encoding="utf-8") as handle:
        handle.write("# embedded keysym tables vs the pinned judge\n")
        handle.write("# names=%d values=%d failures=%d\n"
                     % (name_checked, value_checked, len(failures)))
        for kind, argument, observed, mine in failures[:200]:
            handle.write("%s %s judge=%r ours=%r\n" % (kind, argument, observed, mine))
    for failure in failures[:20]:
        print("FAIL", failure)
    print("names=%d values=%d failures=%d" % (name_checked, value_checked, len(failures)))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
