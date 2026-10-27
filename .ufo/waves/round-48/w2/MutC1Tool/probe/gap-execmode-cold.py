"""MutC1Tool probe 2: the COLD side of the same rule (pin x:964 `command -v "$XTE__EXEC0"`).

One tree, no cache: list names foot.desktop then kitty.desktop; bin/foot exists but is chmod 0644 (a package that
lost its exec bit), bin/kitty is 0755. The pin must skip foot (its Exec word does not resolve) and select kitty; a
tool whose _execable() tests existence instead of executability selects foot. Measured with the counter's own
Box/prepare/run_case, so the numbers are the ones clause f would compute.
"""
import importlib.util
import json
import os
import random
import sys

C, DRAFT, MUT, WORK, OUT = sys.argv[1:6]
spec = importlib.util.spec_from_file_location("c1r48", C)
c1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c1)

case = {
    "id": "COLD-GAP-EXEC-MODE", "class": "probe-cold",
    "env": {"XDG_CONFIG_HOME": "$ROOT/home/.config", "XDG_CONFIG_DIRS": "$ROOT/etc/xdg",
            "XDG_DATA_HOME": "$ROOT/home/.local/share", "XDG_DATA_DIRS": "$ROOT/usr/share",
            "XDG_CURRENT_DESKTOP": "Hyprland"},
    "files": {
        "home/.config/hyprland-xdg-terminals.list": "foot.desktop\nkitty.desktop\n",
        "usr/share/applications/foot.desktop":
            "[Desktop Entry]\nType=Application\nCategories=TerminalEmulator;\nExec=foot\n",
        "usr/share/applications/kitty.desktop":
            "[Desktop Entry]\nType=Application\nCategories=TerminalEmulator;\nExec=kitty\n",
    },
    "exec": ["bin/foot", "bin/kitty"],
    "args": ["--print-cmd"],
    "mtime": c1.PINNED_MTIME,
    "after": {"modes": {"bin/foot": "420"}, "mtime": c1.PINNED_MTIME},
}
res = {}
for tag, tool in (("draft", DRAFT), ("mutant", MUT)):
    work = os.path.join(WORK, tag)
    os.makedirs(work, exist_ok=True)
    box = c1.Box(work, tool)
    ok, o_norm, why, state, cold = c1.run_case(box, case, "A", random.Random(4848))
    res[tag] = {"clause_f_ok": ok, "why": why, "oracle": list(o_norm), "state": state, "trips": len(box.trips)}
    print("%s: f_ok=%s state=%s oracle=%r why=%s" % (tag, ok, state, o_norm, why))
json.dump(res, open(OUT, "w"), indent=1, sort_keys=True)
