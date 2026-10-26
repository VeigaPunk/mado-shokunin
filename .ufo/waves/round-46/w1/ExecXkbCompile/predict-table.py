#!/usr/bin/env python3
"""Prediction table: for each declared-names set, what Hyprland 0.56.2 would store and print
(IKeyboard.cpp:99-115, HyprCtl.cpp:781-794), what the round-46 reference tool's rules join would
then say, and what a compile-based `--xkb` mode would predict before any dump exists.
Read-only: ctypes on libxkbcommon only, no process started.
"""
import sys
from importlib import import_module

sys.path.insert(0, ".")
probe = import_module("xkb-probe")

# id, rules, model, layout, variant, options  -- declared by the config
DECLARED = [
    ("host: br + compose:caps", "", "", "br", "", "compose:caps"),
    ("genuine us", "", "", "us", "", ""),
    ("no kb_* at all (defaults)", "", "", "", "", ""),
    ("typo layout zz", "", "", "zz", "", ""),
    ("typo layout brq", "", "", "brq", "", ""),
    ("us layout, typo variant zzz", "", "", "us", "zzz", ""),
    ("br layout, typo variant zzz", "", "", "br", "zzz", ""),
    ("br layout, missing variant nodeadkeys", "", "", "br", "nodeadkeys", ""),
    ("us layout, missing variant nodeadkeys", "", "", "us", "nodeadkeys", ""),
    ("invalid option only", "", "", "br", "", "notanoption:x"),
    ("host options + invalid option", "", "", "br", "", "compose:caps,notanoption:x"),
    ("typo rules zzz", "zzz", "", "br", "", ""),
    ("typo model zzz", "", "zzz", "br", "", ""),
    ("uppercase layout BR", "", "", "BR", "", ""),
    ("multi br,us + compose:caps", "", "", "br,us", "", "compose:caps"),
]


def verb(rules, model, layout, variant, options):
    return {"rules": rules, "model": model, "layout": layout, "variant": variant, "options": options}


def stored_after_setkeymap(layouts):
    """IKeyboard.cpp:107-115: on no keymap, stored rules become layout us and the rest empty."""
    if layouts is not None:
        return None  # rules unchanged
    return {"rules": "", "model": "", "layout": "us", "variant": "", "options": ""}


def join_verdict(expected, printed):
    """Reference tool order: AGREE (all five equal) then FALLBACK (printed is us + 4 empty) else DIFFER."""
    keys = ("layout", "variant", "options", "model", "rules")
    if all((expected.get(k) or "") == (printed.get(k) or "") for k in keys):
        return "AGREE"
    if printed.get("layout") == "us" and all(not (printed.get(k) or "") for k in keys if k != "layout"):
        return "FALLBACK"
    return "DIFFER"


def attribute(rules, model, layout, variant, options):
    """Which field alone, with the rest at their defaults, already fails to compile."""
    bad = []
    if layout and probe.compile_names("", "", layout, "", "") is None:
        bad.append("layout")
    if variant and probe.compile_names("", "", layout or "us", variant, "") is None:
        bad.append("variant")
    if options and probe.compile_names("", "", layout or "us", "", options) is None:
        bad.append("options")
    if rules and probe.compile_names(rules, "", layout or "us", variant, "") is None:
        bad.append("rules")
    if model and probe.compile_names("", model, layout or "us", "", "") is None:
        bad.append("model")
    return bad


def main():
    print("PREDICT: field columns -- compile | printed(layout/var/opt) | active_keymap | join | xkb-mode")
    mismatch = 0
    for cid, r, m, l, v, o in DECLARED:
        expected = verb(r, m, l, v, o)
        layouts = probe.compile_names(r, m, l, v, o)
        after = stored_after_setkeymap(layouts)
        printed = after if after is not None else expected
        jv = join_verdict(expected, printed)
        fb = probe.hyprland_fallback()
        xkb = "COMPILES name=%r" % (layouts[0] if layouts else None) if layouts is not None else "FAILS->fallback name=%r" % (fb[0] if fb else None)
        agree = (layouts is None) == (jv == "FALLBACK")
        mismatch += 0 if agree else 1
        print(
            "PREDICT: %-38s compile=%-5s printed=%s active_keymap=%r join=%-9s xkb=%-28s signals_agree=%s culprit=%s"
            % (
                cid,
                "yes" if layouts is not None else "NO",
                "%s/%r/%r" % (printed["layout"], printed["variant"], printed["options"]),
                (layouts[0] if layouts else (fb[0] if fb else None)),
                jv,
                xkb,
                agree,
                attribute(r, m, l, v, o) or "-",
            )
        )
    print("PREDICT: cases=%d join_vs_compile_disagreements=%d" % (len(DECLARED), mismatch))
    return 0 if mismatch == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
