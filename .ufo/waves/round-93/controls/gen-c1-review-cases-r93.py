#!/usr/bin/env python3
"""Round-93 C1 (L1): fold R93MReviewC1's 53 fixtures plus L1 cases into one unlabelled byte-class file.

Classes (the counter's byte subset is a, b, n):
  n  — a NUL byte in a portals.conf or .portal line (GKeyFile reads a line as a C string; R93MReviewC1 F1/F2)
  a  — invalid UTF-8 in a name or an unread group (R93MReviewC1 "coverage cases"), and continuation bytes
       after a group line's ']' (g_utf8_find_next_char skips them; L1 cases g93-*)
  ws — CR/CRLF, BOM, group trailers, escapes, Encoding, name validity, whole-file cases (regression)
Usage: gen-c1-review-cases-r93.py --fixtures R93MReviewC1-fixtures.json --out FILE
"""
import argparse
import copy
import json


def klass(cid: str) -> str:
    if cid.startswith("r93-nul-") or cid.startswith("r93-encoding-nul"):
        return "n" if cid.startswith("r93-nul-") else "ws"
    if cid in ("r93-encoding-later-group2", "r93-key-name-byte-e9", "r93-group-name-byte-e9",
               "r93-group-header-invalid-e9"):
        return "a"
    return "ws"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    fx = json.load(open(a.fixtures, encoding="utf-8"))
    out = []
    for c in fx:
        c = copy.deepcopy(c)
        c["class"] = klass(c["id"])
        out.append(c)
    base = next(c for c in fx if c["id"] == "r93-nul-config-value-tail")
    conf = "[preferred]\ndefault=kde\n"
    extra = {
        # continuation bytes after ']' are skipped by g_utf8_find_next_char (group accepted)
        "g93-group-bracket-cont80": ("portals.conf", "[preferred]\udc80\ndefault=kde\n", "a"),
        "g93-group-bracket-space-contbf": ("portals.conf", "[preferred] \udcbf\ndefault=kde\n", "a"),
        "g93-group-bracket-tab-cont-tab": ("portals.conf", "[preferred]\t\udc9a\t\ndefault=kde\n", "a"),
        # a lead byte after ']' is a character start: the line is not a group (control)
        "g93-group-bracket-lead-c3": ("portals.conf", "[preferred]\udcc3\ndefault=kde\n", "a"),
        "g93-portal-group-bracket-cont": ("kde.portal", None, "a"),
        # NUL shapes the review reasoned but did not materialise
        "n93-nul-name-then-bracket": ("portals.conf", "[pref\x00x]\ndefault=kde\n", "n"),
        "n93-nul-two-brackets": ("portals.conf", "[preferred]]\x00\ndefault=kde\n", "n"),
        "n93-nul-after-bracket-then-bracket": ("portals.conf", "[preferred]\x00x]y\ndefault=kde\n", "n"),
        "n93-nul-key-tail-space": ("portals.conf", "[preferred]\ndefault=kde \x00 x\n", "n"),
        "n93-nul-value-start": ("portals.conf", "[preferred]\ndefault= \x00kde\n", "n"),
        "n93-nul-comment-glued": ("portals.conf", "#\x00[x]\n" + conf, "n"),
        # an invalid byte >= 0xF5 in a read [preferred] key, with a default that would otherwise win (R93MMutC1 §5.3)
        "g93-a-ff-read-iface-key": ("portals.conf", "[preferred]\ndefault=gnome\n"
                                    "org.freedesktop.impl.portal.FileChooser=kde\udcff\n", "a"),
        "g93-a-f8-read-iface-key": ("portals.conf", "[preferred]\ndefault=gnome\n"
                                    "org.freedesktop.impl.portal.FileChooser=kde\udcf8\n", "a"),
    }
    for cid, (name, body, cl) in extra.items():
        c = copy.deepcopy(base)
        c["id"] = cid
        c["class"] = cl
        if body is None:
            kde = c["files"]["kde.portal"]
            c["files"]["kde.portal"] = kde.replace("[portal]\n", "[portal]\udca0\n", 1)
            c["files"]["portals.conf"] = conf
        else:
            c["files"][name] = body
        out.append(c)
    ids = [c["id"] for c in out]
    assert len(ids) == len(set(ids)), "duplicate id"
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump({"cases": out}, fh, ensure_ascii=True, indent=1)
    print(f"GENREV cases={len(out)} " + " ".join(f"{k}={sum(c['class'] == k for c in out)}" for k in ("a", "n", "ws")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
