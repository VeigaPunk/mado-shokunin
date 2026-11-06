#!/usr/bin/env python3
"""Round-91 C2 expectation-set builder.

Lane-round expectations come from an independent labels file (R91MExecGate,
`seat-reports-labels-r91.json`, built with plain git without opening the check);
fixtures are the L1's F* set plus the labels file's own fixtures (G*).
Usage: gen-c2-set-r91.py LABELS.json ROUNDS... > seat-reports-set-r91.json
"""
from __future__ import annotations

import json
import sys

REV = "cc0381db585cc44c3dfc13ced807409c32c45bb0"
W = ".ufo/waves/round-7"


def disp(*tasks) -> str:
    return json.dumps({"taskCall": {"context": "c", "tasks": list(tasks)}})


def t(name: str, path: str | None, plain: bool = False) -> dict:
    if path is None:
        return {"name": name, "agent": "scout", "task": "no trailer"}
    if plain:
        return {"name": name, "agent": "critic", "task": f"do it\nReport: {path}\n"}
    return {"name": name, "agent": "scout", "task": f"Own: {path}\n\nReport: write your scoped findings to {path}"}


F = [
    ("F01-present", {f"{W}/w1-dispatch.json": disp(t("A", f"{W}/w1/A.md")), f"{W}/w1/A.md": "x"}, [7], 0, []),
    ("F02-missing", {f"{W}/w1-dispatch.json": disp(t("A", f"{W}/w1/A.md"), t("B", f"{W}/w1/B.md")),
                     f"{W}/w1/A.md": "x"}, [7], 1, ["SR01"]),
    ("F03-empty", {f"{W}/w1-dispatch.json": disp(t("A", f"{W}/w1/A.md")), f"{W}/w1/A.md": ""}, [7], 1, ["SR02"]),
    ("F04-unsafe-dotdot", {f"{W}/w1-dispatch.json": disp(t("A", "../escape.md"))}, [7], 1, ["SR03"]),
    ("F05-unsafe-absolute", {f"{W}/w1-dispatch.json": disp(t("A", "/etc/hostname"))}, [7], 1, ["SR03"]),
    ("F06-untrailed", {f"{W}/r1-dispatch.json": disp(t("A", None))}, [7], 1, ["SR04"]),
    ("F07-plain-missing", {f"{W}/r1-dispatch.json": disp(t("A", f"{W}/r1/A.md", plain=True))}, [7], 1, ["SR01"]),
    ("F08-plain-present", {f"{W}/r1-dispatch.json": disp(t("A", f"{W}/r1/A.md", plain=True)), f"{W}/r1/A.md": "y"},
     [7], 0, []),
    ("F09-rendered-beats-plain", {f"{W}/w1-dispatch.json": disp({"name": "A", "agent": "scout", "task":
        f"Report: {W}/w1/plain.md\n\nReport: write your scoped findings to {W}/w1/A.md"}), f"{W}/w1/plain.md": "x"},
     [7], 1, ["SR01"]),
    ("F10-last-rendered-wins", {f"{W}/w1-dispatch.json": disp({"name": "A", "agent": "scout", "task":
        f"Report: write your scoped findings to {W}/w1/old.md\nReport: write your scoped findings to {W}/w1/A.md"}),
        f"{W}/w1/old.md": "x"}, [7], 1, ["SR01"]),
    ("F11-no-dispatch-rc2", {f"{W}/w1/A.md": "x"}, [7], 2, []),
    ("F12-bad-json-rc2", {f"{W}/w1-dispatch.json": "{"}, [7], 2, []),
    ("F13-no-taskcall-rc2", {f"{W}/w1-dispatch.json": json.dumps({"wave": "w1"})}, [7], 2, []),
    ("F14-all-two-rounds", {f"{W}/w1-dispatch.json": disp(t("A", f"{W}/w1/A.md")), f"{W}/w1/A.md": "x",
                            ".ufo/waves/round-8/w1-dispatch.json": disp(t("B", ".ufo/waves/round-8/w1/B.md"))},
     None, 1, ["SR01"]),
    ("F15-round-filter", {f"{W}/w1-dispatch.json": disp(t("A", f"{W}/w1/A.md")), f"{W}/w1/A.md": "x",
                          ".ufo/waves/round-8/w1-dispatch.json": disp(t("B", ".ufo/waves/round-8/w1/B.md"))},
     [7], 0, []),
    ("F16-two-waves", {f"{W}/w1-dispatch.json": disp(t("A", f"{W}/w1/A.md")), f"{W}/w1/A.md": "x",
                       f"{W}/w2-dispatch.json": disp(t("B", f"{W}/w2/B.md"), t("C", f"{W}/w2/C.md")),
                       f"{W}/w2/C.md": "z"}, [7], 1, ["SR01"]),
    ("F17-report-is-directory", {f"{W}/w1-dispatch.json": disp(t("A", f"{W}/w1/A.md")), f"{W}/w1/A.md/x": "x"},
     [7], 1, ["SR01"]),
    ("F18-symlinked-report", {f"{W}/w1-dispatch.json": disp(t("A", f"{W}/w1/A.md")), f"{W}/w1/real.md": "x",
                              f"{W}/w1/A.md": {"symlink": "real.md"}}, [7], 1, ["SR03"]),
    ("F19-all-without-any-dispatch-rc2", {f"{W}/w1/A.md": "x"}, None, 2, []),  # R91MReviewC2 F3
    ("F20-prose-report-line-untrailed", {f"{W}/r1-dispatch.json": disp({"name": "A", "agent": "critic",
        "task": "Report: findings go in the usual place\n"})}, [7], 1, ["SR04"]),
]
# F21-F28: R91MMutC2 §4 survivors (MC09, MC29, MC38, MC39, MC42, MC44, MC45) — fixtures with verbatim scope args
ARGS = [
    ("F21-dotdot-inside-a-name-is-safe", {f"{W}/w1-dispatch.json": disp(t("A", f"{W}/w1/a..b.md")),
                                          f"{W}/w1/a..b.md": "x"}, ["--round", "7"], 0, [], {}),
    ("F22-verdict-missing-in-summary", {f"{W}/w1-dispatch.json": disp(t("A", f"{W}/w1/A.md"))}, ["--round", "7"], 1,
     ["SR01"], {"verdict": "MISSING", "missing": 1, "seats": 1}),
    ("F23-inline-mention-is-not-a-trailer", {f"{W}/w1-dispatch.json": disp({"name": "A", "agent": "scout", "task":
        f"see above; Report: write your scoped findings to {W}/w1/A.md\n"}), f"{W}/w1/A.md": "x"}, ["--round", "7"],
     1, ["SR04"], {}),
    ("F24-trailing-prose-is-not-a-trailer", {f"{W}/w1-dispatch.json": disp({"name": "A", "agent": "scout", "task":
        f"Report: write your scoped findings to {W}/w1/A.md (see note)\n"}), f"{W}/w1/A.md": "x"}, ["--round", "7"],
     1, ["SR04"], {}),
    ("F25-tasks-object-rc2", {f"{W}/w1-dispatch.json": json.dumps({"taskCall": {"tasks": {"a": 1}}})},
     ["--round", "7"], 2, [], {}),
    ("F26-no-scope-rc2", {f"{W}/w1-dispatch.json": disp(t("A", f"{W}/w1/A.md")), f"{W}/w1/A.md": "x"}, [], 2, [], {}),
    ("F27-all-and-round-rc2", {f"{W}/w1-dispatch.json": disp(t("A", f"{W}/w1/A.md")), f"{W}/w1/A.md": "x"},
     ["--all", "--round", "7"], 2, [], {}),
    ("F28-verdict-ok-in-summary", {f"{W}/w1-dispatch.json": disp(t("A", f"{W}/w1/A.md")), f"{W}/w1/A.md": "x"},
     ["--round", "7"], 0, [], {"verdict": "OK", "present": 1, "untrailed": 0}),
]
# rev-mode fixtures: the same trees committed in a throwaway repository and read with --rev HEAD
GIT = [
    ("H01-rev-symlinked-report", {f"{W}/w1-dispatch.json": disp(t("A", f"{W}/w1/A.md")), f"{W}/w1/real.md": "x",
                                  f"{W}/w1/A.md": {"symlink": "real.md"}}, [7], 1, ["SR03"]),
    ("H02-rev-empty-report", {f"{W}/w1-dispatch.json": disp(t("A", f"{W}/w1/A.md")), f"{W}/w1/A.md": ""}, [7], 1,
     ["SR02"]),
    ("H03-rev-present-outside-waves", {f"{W}/w1-dispatch.json": disp(t("A", "notes/A.md")), "notes/A.md": "x"}, [7],
     0, []),
    ("H04-rev-missing", {f"{W}/w1-dispatch.json": disp(t("A", f"{W}/w1/A.md"))}, [7], 1, ["SR01"]),
]


def main() -> int:
    labels = json.load(open(sys.argv[1], encoding="utf-8"))
    rounds = [int(x) for x in sys.argv[2:]]
    byround = {r["round"]: r for r in labels["rounds"]}
    revs = []
    for n in rounds:
        r = byround[n]
        bad = r["missing"] or r["empty"] or r["unsafe"] or r["untrailed"]
        revs.append({"id": f"R{n}", "rev": REV, "round": n, "rc": 1 if bad else 0,
                     "missing": r["missing"], "empty": r["empty"], "unsafe": r["unsafe"],
                     "untrailed": r["untrailed"], "seats": r["seats"], "trailered": r["trailered"]})
    tot = labels["totals"]
    miss = tot["counts"]["missing"]
    allx = {"id": "ALL", "rev": REV, "rc": 1 if miss else 0, "sr01": miss, "seats": tot["seats"]}
    fixtures = [{"id": i, "files": f, "rounds": r, "rc": rc, "ids": ids} for i, f, r, rc, ids in F]
    fixtures += [{"id": i, "files": f, "rounds": r, "rc": rc, "ids": ids, "git": True} for i, f, r, rc, ids in GIT]
    fixtures += [{"id": i, "files": f, "args": a, "rc": rc, "ids": ids, "summary": s} for i, f, a, rc, ids, s in ARGS]
    for g in labels.get("fixtures", []):
        argv = g["argv"]
        rounds_g = None if "--all" in argv else [int(argv[i + 1]) for i, x in enumerate(argv) if x == "--round"]
        fixtures.append({"id": "G-" + g["id"], "files": g["files"], "dirs": g.get("dirs", []), "rounds": rounds_g,
                         "rc": g["expected_rc"], "ids": g["expected_finding_ids"],
                         "summary": g.get("expected_summary") or {}})
    json.dump({"note": "Round-91 C2 frozen expectation set (lane rounds labelled by R91MExecGate at "
               f"{REV}; F* fixtures by the L1; G-* fixtures by R91MExecGate).", "revisions": revs, "all": allx,
               "fixtures": fixtures}, sys.stdout, indent=1, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
