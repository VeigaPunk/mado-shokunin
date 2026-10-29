"""R56W2MutC2ToolB: candidate fixtures that each target one NON-equivalent survivor.

Each entry: mutant id -> list of (fid, spec). spec = {"args": [...], "files": {name: text | ("link", target)},
"dirs": [...]}. "{FX}" in args is replaced by the staged fixture path by the harness.
Surrogate-escaped names (\\udcXX) are raw bytes on disk.
"""

H = "hyprland.conf"
DR = "{FX}"


def std(main_text, files=None, dirs=None, extra_args=None):
    args = ["--config", "{FX}/tree/%s" % H, "--display-root", DR]
    if extra_args:
        args += extra_args
    f = {H: main_text}
    f.update(files or {})
    return {"args": args, "files": f, "dirs": dirs or []}


CANDS = {
    # m01: `~x.conf` must expand as --home + "x.conf" (tilde without a following slash)
    "m01": [("K01", {"args": ["--config", "{FX}/tree/hyprland.conf", "--display-root", DR,
                              "--home", "{FX}/tree/home"],
                     "files": {H: "source = ~x.conf\n", "homex.conf": "a = 1\n"}, "dirs": ["home"]})],
    # m07: `**` is an ordinary `*` in python glob without recursive=True
    "m07": [("K02", std("source = conf.d/**/*.conf\n",
                        {"conf.d/a.conf": "a = 1\n", "conf.d/sub/b.conf": "b = 2\n"}))],
    # m08: bytewise order: a name whose first byte is 0x80 (raw) sorts before U+0100 (UTF-8 C4 80)
    "m08": [("K03", std("source = conf.d/*.conf\n",
                        {"conf.d/\udc80.conf": "a = 1\n", "conf.d/\u0100.conf": "b = 2\n"}))],
    # m14: an inaccessible match must end the line's matches (return), not skip one (continue);
    # the dangling link must sort FIRST (F10 has it last, where return and continue agree)
    "m14": [("K04", std("source = conf.d/*.conf\n",
                        {"conf.d/a.conf": ("link", "missing-target.conf"), "conf.d/b.conf": "b = 2\n"}))],
    # m18, m21: a dangling MAIN config symlink: realpath strict fails (no canonical), lexists true (type=file)
    "m18": [("K05", {"args": ["--config", "{FX}/tree/hyprland.conf", "--display-root", DR],
                     "files": {H: ("link", "missing.conf")}, "dirs": []})],
    # m25: a MAIN config that is a symlink to a directory: typed dir (mask DIR), canonical watch present
    "m25": [("K06", {"args": ["--config", "{FX}/tree/hyprland.conf", "--display-root", DR],
                     "files": {H: ("link", "realdir")}, "dirs": ["realdir"]})],
    # m31, m36, m95: display root given through a symlink; config printed under the link path
    "m31": [("K07", {"args": ["--config", "{FX}/tree/lnk/hyprland.conf", "--display-root", "{FX}/tree/lnk"],
                     "files": {"real/hyprland.conf": "a = 1\n", "lnk": ("link", "real")}, "dirs": []})],
    # m30: display root given with a trailing slash, through the symlink
    "m30": [("K08", {"args": ["--config", "{FX}/tree/lnk/hyprland.conf", "--display-root", "{FX}/tree/lnk/"],
                     "files": {"real/hyprland.conf": "a = 1\n", "lnk": ("link", "real")}, "dirs": []})],
    # m96: config under the real path, display root given through the symlink (realpath prefix must match)
    "m96": [("K09", {"args": ["--config", "{FX}/tree/real/hyprland.conf", "--display-root", "{FX}/tree/lnk"],
                     "files": {"real/hyprland.conf": "a = 1\n", "lnk": ("link", "real")}, "dirs": []})],
    # m94: the display root equal to a printed path itself (DIR == path) prints $ROOT
    "m94": [("K10", {"args": ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}/tree/hyprland.conf"],
                     "files": {H: "a = 1\n"}, "dirs": []})],
    # m49: a backslash on the option line makes it unsupported (value `true\` must not be accepted)
    "m49": [("K11", std("misc:disable_autoreload = true\\\n"))],
    # m51: a key that merely starts with `source` is not a source line
    "m51": [("K12", std("sourcex = a.conf\n", {"a.conf": "a = 1\n"}))],
    # m55: a comment line ending in `{` must not open a category
    "m55": [("K13", std("# x {\nmisc:disable_autoreload = 1\n"))],
    # m56: a leading NBSP is not stripped (python strip() strips it, the WS set does not)
    "m56": [("K14", std("\u00a0misc:disable_autoreload = 1\n"))],
    # m105: partition at the FIRST '=' (a later '=' is part of the value, here a comment)
    "m105": [("K15", std("misc:disable_autoreload = 1 # a=b\n"))],
    # m101: a non-string option key with an integer value must be skipped (mutant crashes: unhashable)
    "m101": [("K16", {"args": ["--config", "{FX}/tree/hyprland.conf", "--display-root", DR,
                               "--getoption", "{FX}/tree/go.json"],
                      "files": {H: "a = 1\n", "go.json": '{"option": [1], "int": 0}\n'}, "dirs": []})],
    # m114: an argument value is literal: a trailing space names a different (missing) path
    "m114": [("K17", {"args": ["--config", "{FX}/tree/hyprland.conf ", "--display-root", DR],
                      "files": {H: "a = 1\n"}, "dirs": []})],
    # m64, m109: a self-sourcing config reaching 262143 entries (pristine OK), with the value 1 so no watch lines
    "m64": [("K18", std("source = hyprland.conf\nsource = hyprland.conf\nmisc:disable_autoreload = 1\n"))],
    # m65: exactly 262145 add attempts: pristine raises too_large on the last add (len 262144 >= cap),
    # the `>` mutant appends it
    "m65": [("K19", std("source = self.conf\nsource = self.conf\nsource = leaf.conf\nsource = leaf.conf\n"
                        "misc:disable_autoreload = 1\n",
                        {"self.conf": "source = self.conf\nsource = self.conf\n", "leaf.conf": "a = 1\n"}))],
}

# shared fixtures: the same tree kills several mutants of the same behaviour point
CANDS["m21"] = CANDS["m18"]     # dangling main config: lexists -> type=file (mutant prints type=missing)
CANDS["m36"] = CANDS["m31"]     # display root given through a symlink: root[:-1] matches nothing
CANDS["m95"] = CANDS["m31"]     # display root given through a symlink: root[1:] is relative
CANDS["m109"] = CANDS["m64"]    # 262143 entries: cap 131072 raises too_large
CANDS["m09"] = [("K20", std("source = " + "*/" * 1100 + "x\n"))]  # glob RecursionError: caught by pristine
