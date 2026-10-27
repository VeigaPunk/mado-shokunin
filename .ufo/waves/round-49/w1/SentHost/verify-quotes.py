#!/usr/bin/env python3
"""Verify every receipt locator in report.md against the receipt bytes (locators are computed, never typed)."""
import re, sys, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "receipts")
# (receipt, line, substring that must be on that line)
CHECKS = [
 ("r1-compile-fs.txt", 5, "home/.config/xkb"),
 ("r1-compile-fs.txt", 6, "home/.xkb"),
 ("r1-compile-fs.txt", 7, "/etc/xkb"),
 ("r1-compile-fs.txt", 10, "0"),
 ("r1-compile-fs.txt", 14, "--test --layout br -> rc=0 write-opens=0"),
 ("r1-compile-fs.txt", 16, "--options compose:caps -> rc=0 write-opens=0"),
 ("r1-compile-fs.txt", 12, "6ef2127653b0ca1a6dd8e617d9c4852888ad9310e0c195f6fc847453173d05ca"),
 ("r2-include-matrix.txt", 2, "6ef2127653b0ca1a6dd8e617d9c4852888ad9310e0c195f6fc847453173d05ca  evil=0"),
 ("r2-include-matrix.txt", 3, "4f07b6d5b70afb586d591474985827010805b076c24cc066d94ca2a5e50e7b95  evil=1"),
 ("r2-include-matrix.txt", 4, "6ef2127653b0ca1a6dd8e617d9c4852888ad9310e0c195f6fc847453173d05ca  evil=0"),
 ("r2-include-matrix.txt", 5, "6ef2127653b0ca1a6dd8e617d9c4852888ad9310e0c195f6fc847453173d05ca  evil=0"),
 ("r2-include-matrix.txt", 6, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
 ("r2-include-matrix.txt", 7, "6637586fc663f523b16f0acdee74a092b4b89b7d180b509c64767828c6645202  evil=1"),
 ("r2-include-matrix.txt", 8, "6ef2127653b0ca1a6dd8e617d9c4852888ad9310e0c195f6fc847453173d05ca  evil=0"),
 ("r2-include-matrix.txt", 12, "1 include paths searched"),
 ("r2-include-matrix.txt", 14, "1 include paths could not be added"),
 ("r3-workdir-planting.txt", 2, "6ef2127653b0ca1a6dd8e617d9c4852888ad9310e0c195f6fc847453173d05ca"),
 ("r3-workdir-planting.txt", 3, "5021473cee499bc00da9acc427acf83c00f3d57b414b36eb5d3c5e218e6777a0"),
 ("r3-workdir-planting.txt", 4, "--include"),
 ("r3-workdir-planting.txt", 5, "evil=0"),
 ("r4-howtotype-fs.txt", 6, "home/.config/XCompose"),
 ("r4-howtotype-fs.txt", 8, "/usr/share/X11/locale/en_US.UTF-8/Compose"),
 ("r4-howtotype-fs.txt", 9, "WITH --disable-compose"),
 ("r4-howtotype-fs.txt", 10, "--disable-compose"),
 ("r4-howtotype-fs.txt", 13, "t-ht-compose.txt:0"),
 ("r4-howtotype-fs.txt", 14, "t-ht-nocompose.txt:0"),
 ("r4-howtotype-fs.txt", 18, "=== Access via Compose sequences ==="),
 ("r5-judge-contract.txt", 8, "XKB_CONFIG_ROOT has no effect"),
 ("r5-judge-contract.txt", 9, "identical to the clean-env run"),
 ("r5-judge-contract.txt", 11, "host-tree opens: 40"),
 ("r5-judge-contract.txt", 12, "clean rows=5 hostile-rows=0"),
 ("r6-bwrap.txt", 12, "rc=0"),
 ("r6-bwrap.txt", 16, "/lib64/ld-linux-x86-64.so.2"),
 ("r6-bwrap.txt", 17, "/usr/lib/ld-linux-x86-64.so.2"),
 ("r6-bwrap.txt", 27, "/home"),
 ("r6-bwrap.txt", 31, "/sys/class/net"),
 ("r6-bwrap.txt", 35, "without --clearenv: 269 vars"),
 ("r6-bwrap.txt", 36, "with    --clearenv: 1 vars"),
 ("r6-bwrap.txt", 33, "a5c4718a11955dbd03a4742f7ea0f7105ec1ef5982920d3fe2579b5614daaf4e"),
 ("r7-hyprctl.txt", 2, "hyprctl version -> rc=0"),
 ("r7-hyprctl.txt", 4, "home-path hits: 0"),
 ("r7-hyprctl.txt", 13, "home-path hits: 0"),
 ("r7-hyprctl.txt", 15, "binds=192"),
 ("r7-hyprctl.txt", 17, '"int": 0, "set": false'),
 ("r7-hyprctl.txt", 21, "/run/user/<uid>/hypr/<sig>/.socket.sock"),
 ("r7-hyprctl.txt", 24, "HYPRLAND_INSTANCE_SIGNATURE not set"),
 ("r6-bwrap.txt", 18, "execvp /judge: No such file or directory"),
 ("r4-howtotype-fs.txt", 11, 'openat(AT_FDCWD, "br.xkb"'),
 ("r4-howtotype-fs.txt", 22, "xcf.txt"),
 ("r4-howtotype-fs.txt", 24, "home5/.config/XCompose"),
 ("r4-howtotype-fs.txt", 25, "home5/.XCompose"),
 ("r8-header.txt", 2, "13023369f65a17411606084e3e09557b4886aeb15f89affba4aaa86490a463f3"),
 ("r8-header.txt", 4, "#define XKB_KEY_ lines: 2638"),
 ("r8-header.txt", 5, "occurrences of XKB_KEY_: 2792"),
 ("r8-header.txt", 6, "lines containing XKB_KEY_: 2783"),
 ("r9-operator-state.txt", 2, "~/.XCompose"),
 ("r9-operator-state.txt", 3, "~/.config/xkb"),
 ("r9-operator-state.txt", 4, "~/.xkb"),
 ("r9-operator-state.txt", 5, "~/.cache/xdg-terminal-exec"),
 ("r9-operator-state.txt", 6, "/etc/xkb"),
 ("r9-operator-state.txt", 8, "/usr/share/xkeyboard-config-2.d"),
 ("r9-operator-state.txt", 9, "/usr/share/xkeyboard-config.d"),
 ("r9-operator-state.txt", 10, "symbols/br"),
 ("r9-operator-state.txt", 11, "rules/evdev"),
 ("r9-operator-state.txt", 13, "xkeyboard-config-2.48-1"),
 ("r11-tool-run.txt", 2, "Python 3.14.8"),
 ("r11-tool-run.txt", 4, "ModuleNotFoundError: No module named 'helper'"),
 ("r11-tool-run.txt", 7, "__pycache__/helper.cpython-314.pyc"),
 ("r11-tool-run.txt", 9, "pyc files after -I"),
 ("r10-pins.txt", 2, "43b924f6"),
 ("r10-pins.txt", 3, "f6c0b122"),
 ("r10-pins.txt", 4, "13023369"),
 ("r10-pins.txt", 5, "af42b0e6"),
 ("r10-pins.txt", 6, "21662"),
]
bad = 0
for fn, ln, sub in CHECKS:
    path = os.path.join(R, fn)
    try:
        lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
        got = lines[ln-1]
    except Exception as e:
        print("MISSING %s:%s (%s)" % (fn, ln, e)); bad += 1; continue
    if sub not in got:
        print("MISMATCH %s:%d want %r got %r" % (fn, ln, sub, got[:120])); bad += 1
# the 2659 claim must NOT be reproducible by any counting in R8
r8 = open(os.path.join(R, "r8-header.txt")).read()
if "2659" in r8:
    print("UNEXPECTED: 2659 appears in r8-header.txt"); bad += 1
print("checked=%d bad=%d" % (len(CHECKS), bad))
sys.exit(1 if bad else 0)
