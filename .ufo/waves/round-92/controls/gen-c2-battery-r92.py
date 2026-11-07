#!/usr/bin/env python3
"""Round-92 C2 battery — fixtures for the five round-91 residual gate defects (R91MResidC2 F1-F5) plus
positive controls the base gate already passes.  Expectations are written here from the defect
reports' stated correct behaviour, never from running the check.

Fixture spec: {"id", "class", "mode": "worktree"|"rev", "files": {rel: spec}, "args": [...],
               "expect": {"rc", "ids" (multiset, sorted), "contains" [substr...], "summary" {field: int},
                          "fields": int (whitespace fields of every SR line, optional), "lines": int (optional)}}
optional "gitlinks": {rel: sha} (rev mode: a 160000 index entry added after `git add -A`)
spec: {"text": s} | {"json": obj} (written with json.dumps, ensure_ascii=False) | {"symlink": target}
      ({OUTSIDE} = a directory outside the fixture holding A.md; {SIBLING} = <tree>-sibling, outside the tree
      but sharing its path as a string prefix, holding A.md) | {"fifo": true} | {"dir": true}
Every run's stdout must be ASCII (the F2 rule) and finish within the counter's timeout (the F4 rule).
"""
import json
import sys

W = ".ufo/waves/round-7"
W8 = ".ufo/waves/round-8"


def task(name, path):
    body = f"Own: {path}\n" if path else "no trailer\n"
    if path:
        body += f"\nReport: write your scoped findings to {path}"
    return {"name": name, "agent": "scout", "task": body}


def disp(*ts):
    return {"json": {"taskCall": {"context": "c", "tasks": list(ts)}}}


B = []


def fx(id_, cls, mode, files, args, rc, ids=(), contains=(), summary=None, fields=None, lines=None, gitlinks=None):
    e = {"rc": rc, "ids": sorted(ids), "contains": list(contains)}
    if summary:
        e["summary"] = summary
    if fields:
        e["fields"] = fields
    if lines:
        e["lines"] = lines
    item = {"id": id_, "class": cls, "mode": mode, "files": files, "args": args, "expect": e}
    if gitlinks:
        item["gitlinks"] = gitlinks
    B.append(item)


R7 = ["--round", "7"]
SYM = "dispatch is a symlink"
# F1 — a dispatch stored as a symlink is refused (rc 2) in both modes, never skipped
two = {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/w1/A.md")), f"{W}/w1/A.md": {"text": "x"},
       f"{W}/real.json": disp(task("B", f"{W}/w2/B.md")), f"{W}/w2-dispatch.json": {"symlink": "real.json"}}
fx("F1-01-rev-second-wave-link", "F1", "rev", two, R7, 2, contains=[SYM])
fx("F1-02-worktree-second-wave-link", "F1", "worktree", two, R7, 2, contains=[SYM])
fx("F1-03-rev-only-wave-link", "F1", "rev", {f"{W}/real.json": disp(task("B", f"{W}/w1/B.md")),
                                             f"{W}/w1-dispatch.json": {"symlink": "real.json"}}, R7, 2, contains=[SYM])
fx("F1-04-rev-all-link-in-round-8", "F1", "rev", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/w1/A.md")),
                                                  f"{W}/w1/A.md": {"text": "x"},
                                                  f"{W8}/real.json": disp(task("B", f"{W8}/w1/B.md")),
                                                  f"{W8}/w1-dispatch.json": {"symlink": "real.json"}}, ["--all"], 2,
   contains=[SYM])
fx("F1-05-rev-dangling-link", "F1", "rev", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/w1/A.md")),
                                            f"{W}/w1/A.md": {"text": "x"}, f"{W}/w2-dispatch.json": {"symlink": "gone.json"}},
   R7, 2, contains=[SYM])
# added after w1 (R92MReviewC2 findings 1-2): a directory, a symlink to a directory, a gitlink at a dispatch path
ok2 = {f"{W}/w2-dispatch.json": disp(task("B", f"{W}/w2/B.md")), f"{W}/w2/B.md": {"text": "b"}}
fx("F1-06-worktree-dir-dispatch", "F1", "worktree", dict(ok2, **{f"{W}/w1-dispatch.json": {"dir": True}}), R7, 2,
   contains=["not a regular file"])
fx("F1-07-worktree-link-to-dir-dispatch", "F1", "worktree", dict(ok2, **{f"{W}/d": {"dir": True},
                                                                       f"{W}/w1-dispatch.json": {"symlink": "d"}}), R7, 2,
   contains=[SYM])
fx("F1-09-rev-dir-dispatch", "F1", "rev", dict(ok2, **{f"{W}/w1-dispatch.json/x": {"text": "x"}}), R7, 2,
   contains=["not a regular file"])
fx("F1-08-rev-gitlink-dispatch", "F1", "rev", dict(ok2), R7, 2, contains=["not a regular file"],
   gitlinks={f"{W}/w1-dispatch.json": "1111111111111111111111111111111111111111"})
# F2 — every line ASCII, a seat and a path are one token each
fx("F2-01-name-with-space", "F2", "worktree", {f"{W}/r1-dispatch.json": disp({"name": "A b", "task": f"Report: {W}/r1/A.md\n"})},
   R7, 1, ["SR01"], fields=5)
fx("F2-02-name-with-newline", "F2", "worktree", {f"{W}/r1-dispatch.json": disp({"name": "A\nSR02 empty x", "task":
                                                                               f"Report: {W}/r1/A.md\n"})},
   R7, 1, ["SR01"], fields=5, lines=2)
fx("F2-03-non-ascii-path", "F2", "worktree", {f"{W}/r1-dispatch.json": disp({"name": "A", "task": f"Report: {W}/r1/\u00e9t\u00e9.md\n"})},
   R7, 1, ["SR01"], fields=5)
fx("F2-04-lone-surrogate-path", "F2", "worktree", {f"{W}/r1-dispatch.json": {"raw": '{"taskCall": {"context": "c", "tasks": '
                                                                                   '[{"name": "A", "task": "Report: ' + W + '/r1/\\udcff.md\\n"}]}}'}},
   R7, 1, ["SR01"], fields=5)
fx("F2-05-name-with-tab-rev", "F2", "rev", {f"{W}/r1-dispatch.json": disp({"name": "A\tB", "task": f"Report: {W}/r1/A.md\n"})},
   R7, 1, ["SR01"], fields=5)
# F3 — a repeated --round counts once
fx("F3-01-round-twice", "F3", "worktree", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/w1/A.md"))}, R7 + R7, 1, ["SR01"],
   summary={"rounds": 1, "waves": 1, "seats": 1, "missing": 1})
fx("F3-02-round-twice-rev", "F3", "rev", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/w1/A.md")),
                                          f"{W8}/w1-dispatch.json": disp(task("B", f"{W8}/w1/B.md")),
                                          f"{W8}/w1/B.md": {"text": "y"}}, R7 + ["--round", "8"] + R7, 1, ["SR01"],
   summary={"rounds": 2, "waves": 2, "seats": 2, "missing": 1, "present": 1})
fx("F3-03-round-thrice-ok", "F3", "worktree", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/w1/A.md")),
                                               f"{W}/w1/A.md": {"text": "x"}}, R7 * 3, 0,
   summary={"rounds": 1, "waves": 1, "seats": 1, "present": 1})
# F4 — a FIFO (or other non-regular file) at a dispatch path is a setup error, not a hang
fx("F4-01-fifo-only-wave", "F4", "worktree", {f"{W}/w1-dispatch.json": {"fifo": True}}, R7, 2, contains=["not a regular file"])
fx("F4-02-fifo-second-wave", "F4", "worktree", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/w1/A.md")),
                                                f"{W}/w1/A.md": {"text": "x"}, f"{W}/w2-dispatch.json": {"fifo": True}},
   R7, 2, contains=["not a regular file"])
fx("F4-03-fifo-all", "F4", "worktree", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/w1/A.md")),
                                        f"{W}/w1/A.md": {"text": "x"}, f"{W8}/w1-dispatch.json": {"fifo": True}},
   ["--all"], 2, contains=["not a regular file"])
# F5 — a report reached through a parent symlink that leaves the repository is SR03 in --worktree
fx("F5-01-parent-link-outside", "F5", "worktree", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/out/A.md")),
                                                   f"{W}/out": {"symlink": "{OUTSIDE}"}}, R7, 1, ["SR03"])
fx("F5-02-grandparent-link-outside", "F5", "worktree", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/g/out/A.md")),
                                                        f"{W}/g": {"symlink": "{OUTSIDE}/.."}}, R7, 1, ["SR03"])
fx("F5-03-parent-link-outside-and-ok", "F5", "worktree", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/out/A.md"),
                                                                                        task("B", f"{W}/w1/B.md")),
                                                          f"{W}/out": {"symlink": "{OUTSIDE}"}, f"{W}/w1/B.md": {"text": "b"}},
   R7, 1, ["SR03"], summary={"present": 1, "unsafe": 1})
fx("F5-04-parent-link-to-prefix-sibling", "F5", "worktree", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/sib/A.md")),
                                                            f"{W}/sib": {"symlink": "{SIBLING}"}}, R7, 1, ["SR03"])
# P — behaviour the base already has; a fix must keep it (blanket refusal and blanket quoting fail here)
fx("P-01-worktree-ok", "P", "worktree", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/w1/A.md")), f"{W}/w1/A.md": {"text": "x"}},
   R7, 0, summary={"present": 1})
fx("P-02-rev-missing", "P", "rev", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/w1/A.md"), task("B", f"{W}/w1/B.md")),
                                    f"{W}/w1/A.md": {"text": "x"}}, R7, 1, ["SR01"],
   contains=[f"SR01 missing round-7/w1 B {W}/w1/B.md"])
fx("P-03-rev-symlinked-report", "P", "rev", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/w1/A.md")),
                                             f"{W}/w1/real.md": {"text": "x"}, f"{W}/w1/A.md": {"symlink": "real.md"}},
   R7, 1, ["SR03"])
fx("P-04-untrailed-and-empty", "P", "worktree", {f"{W}/r1-dispatch.json": disp(task("A", None), task("B", f"{W}/r1/B.md")),
                                                 f"{W}/r1/B.md": {"text": ""}}, R7, 1, ["SR02", "SR04"])
fx("P-05-parent-link-inside", "P", "worktree", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/alias/A.md")),
                                                f"{W}/real/A.md": {"text": "x"}, f"{W}/alias": {"symlink": "real"}},
   R7, 0, summary={"present": 1})
fx("P-06-rev-parent-link-outside", "P", "rev", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/out/A.md")),
                                                f"{W}/out": {"symlink": "{OUTSIDE}"}}, R7, 1, ["SR01"])
fx("P-07-plain-name-unquoted", "P", "worktree", {f"{W}/w1-dispatch.json": disp(task("Seat-1", f"{W}/w1/S.md"))}, R7, 1,
   ["SR01"], contains=[f"SR01 missing round-7/w1 Seat-1 {W}/w1/S.md"])
fx("P-08-rev-all-ok", "P", "rev", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/w1/A.md")), f"{W}/w1/A.md": {"text": "x"},
                                   f"{W8}/w1-dispatch.json": disp(task("B", f"{W8}/w1/B.md")), f"{W8}/w1/B.md": {"text": "y"}},
   ["--all"], 0, summary={"rounds": 2, "waves": 2, "present": 2})

if __name__ == "__main__":
    json.dump({"fixtures": B}, open(sys.argv[1], "w", encoding="utf-8"), indent=1, ensure_ascii=True)
    print(f"wrote {len(B)} fixtures")
