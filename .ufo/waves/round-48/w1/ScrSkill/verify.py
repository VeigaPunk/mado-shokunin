#!/usr/bin/env python3
"""Verify every quoted fragment in section.md against the file:line it cites.

Read-only: opens files, prints PASS/FAIL. Run from the lane root:
    python3 .ufo/waves/round-48/w1/ScrSkill/verify.py
Exit 0 only when every check passes.
"""
import hashlib
import os
import sys

ROOT = "/home/vgpnk/Projects/shokunin/mado-shokunin"
PIN = ".ufo/waves/round-47/fetch/xdg-terminal-exec"
REC = ".ufo/waves/round-48/w1/ScrSkill/receipts"
SECTION = ".ufo/waves/round-48/w1/ScrSkill/section.md"
PIN_SHA = "89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac"

# (file, first_line, last_line, fragment)
CHECKS = [
    # the pinned resolver's cache path, as section.md cites it
    (PIN, 172, 172, 'XDG_CACHE_HOME=${XDG_CACHE_HOME:-"${HOME}/.cache"}'),
    (PIN, 173, 173, "XTE__CACHE_FILE=${XDG_CACHE_HOME}/xdg-terminal-exec"),
    (PIN, 194, 194, "echo 4"),
    (PIN, 200, 200, "LANG=C ls -LRl"),
    (PIN, 201, 201, "md5sum"),
    (PIN, 223, 223, "xte__line_limit=50"),
    (PIN, 247, 251, "END_OF_EXEC_USEP"),
    (PIN, 274, 274, 'if [ "$XTE__HASH" = "$xte__cached_hash" ] && command -v "$xte__cached_cmd" > /dev/null; then'),
    (PIN, 332, 332, '> "${XTE__CACHE_FILE}"'),
    (PIN, 337, 337, 'rm -f "${XTE__CACHE_FILE}"'),
    (PIN, 380, 380, "/disable_cache)"),
    (PIN, 1172, 1172, "XTE__CACHE_ENABLED=${XTE_CACHE_ENABLED-true}"),
    (PIN, 1179, 1179, 'if check_bool "${XTE__CACHE_ENABLED}" && read_cache; then'),
    (PIN, 1183, 1209, "find_entry || exit 1"),
    (PIN, 1368, 1368, "early bail out in some print modes"),
    (PIN, 1370, 1376, "exit 0"),
    (PIN, 1400, 1409, 'set -- "${XTE__DIRARG}${XTE__DIRVAL}" "$@"'),
    (PIN, 1455, 1457, 'save_cache "$1" &'),
    # my own receipt: the compile matrix the section's numbers come from
    (REC + "/xkbcli-matrix.txt", 1, 10**6, 'Couldn\'t find file "symbols/zz" in include paths'),
    (REC + "/xkbcli-matrix.txt", 1, 10**6, "Couldn't process include statement for 'br(nope)'"),
    (REC + "/xkbcli-matrix.txt", 1, 10**6, 'Unrecognized RMLVO option "nope" was ignored'),
    (REC + "/xkbcli-matrix.txt", 1, 10**6, 'Less layouts than variants: "br" vs. "intl,nope".'),
    (REC + "/xkbcli-matrix.txt", 1, 10**6, "f73b560f90bbfbe2169e1c946a967dbf"),
    (REC + "/xkbcli-matrix.txt", 1, 10**6, "stdout_bytes=73079"),
    (REC + "/xkbcli-matrix.txt", 1, 10**6, "stdout_bytes=76323"),
    (REC + "/xkbcli-matrix.txt", 1, 10**6, "stdout_bytes=77943"),
    (REC + "/xkbcli-matrix.txt", 1, 10**6, "stdout_bytes=78029"),
    (REC + "/xkbcli-matrix.txt", 1, 10**6, "stdout_bytes=82427"),
    (REC + "/xkbcli-matrix.txt", 1, 10**6, "br_rows=9"),
    (REC + "/xkbcli-matrix.txt", 1, 10**6, "zz_rows=0"),
    (REC + "/xkbcli-matrix.txt", 1, 10**6, "libxkbcommon 1.13.2-1"),
    (REC + "/xkbcli-matrix.txt", 1, 10**6, "xkeyboard-config 2.48-1"),
    (REC + "/xkbcli-matrix.txt", 1, 10**6, "/usr/share/xkeyboard-config-2"),
    (REC + "/xkbcli-matrix.txt", 1, 10**6, "/home/vgpnk/.config/xkb"),
    (REC + "/resolver-cache-locators.txt", 1, 10**6, "89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac"),
    # host files the section names
    ("/home/vgpnk/.config/hypr/input.conf", 10, 10, "kb_layout = br"),
    ("/home/vgpnk/.config/hypr/input.conf", 11, 11, "kb_options = compose:caps"),
    ("/home/vgpnk/.config/hypr/bindings.conf", 2, 2, 'xdg-terminal-exec --dir="$(omarchy-cmd-terminal-cwd)"'),
    # lane files the section points at
    ("SKILL.md", 2128, 2128, "FALLBACK"),
    ("SKILL.md", 2213, 2213, "a change has no effect"),
    ("corpus/knowledge/hyprland-input-devices-r46.md", 69, 69, "The XKB compile itself is not reproduced"),
    ("corpus/README.md", 112, 112, "the XKB compile itself"),
    ("tools/mado-terminal.py", 82, 86, "models the cold path"),
]


def lines(path):
    with open(path, encoding="utf-8", errors="replace") as handle:
        return handle.read().splitlines()


def main():
    fails = 0
    with open(os.path.join(ROOT, PIN), "rb") as handle:
        sha = hashlib.sha256(handle.read()).hexdigest()
    print(f"pin sha256 {sha} == {PIN_SHA}: {'PASS' if sha == PIN_SHA else 'FAIL'}")
    fails += sha != PIN_SHA

    cache = {}
    for path, first, last, frag in CHECKS:
        full = path if path.startswith("/") else os.path.join(ROOT, path)
        if full not in cache:
            cache[full] = lines(full)
        body = cache[full]
        window = body[first - 1:last]
        ok = any(frag in line for line in window)
        where = f"{path}:{first}-{last}"
        print(f"{'PASS' if ok else 'FAIL'} {where} :: {frag}")
        fails += not ok

    section = os.path.join(ROOT, SECTION)
    text = open(section, encoding="utf-8").read()
    after = text.count("<AFTER")
    print(f"INFO {SECTION}: {len(text)} bytes, {after} <AFTER> markers")
    sections = [line for line in text.splitlines() if line.startswith("## ")]
    print(f"INFO sections: {sections}")
    fails += len(sections) != 2
    print(f"RESULT {'PASS' if not fails else 'FAIL'} checks={len(CHECKS) + 1} failed={fails}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
