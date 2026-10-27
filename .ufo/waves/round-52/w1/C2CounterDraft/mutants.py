#!/usr/bin/env python3
"""Mutation-test the draft C2 counter: one change per mutant, each must MISS with the
intended clause at ok=0.  A mutant that still passes is a hole in the counter.

Every mutant is a single-file edit committed on top of the green fixture, in a scratch clone
only.  The lane is never touched.

Usage:
    python3 mutants.py --lane <lane> --work <scratch> --fixture <fixture clone> \
        --counter <counter path>
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

ENTRY_REL = "corpus/knowledge/hyprland-dispatcher-action-effects-r52.md"
REVISION = "efb50993780079460b0cbed1363e2166a2de1d9f"


def git(repo, *args, check=True):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    if check and p.returncode != 0:
        raise SystemExit("git %s failed: %s" % (" ".join(args), p.stderr.strip()))
    return p


def assert_toplevel(repo, expect):
    top = git(repo, "rev-parse", "--show-toplevel").stdout.strip()
    if os.path.realpath(top) != os.path.realpath(expect):
        raise SystemExit("refusing to mutate: toplevel %s != %s" % (top, expect))


def read(path):
    with open(path) as fh:
        return fh.read()


def write(path, text):
    with open(path, "w") as fh:
        fh.write(text)


# ------------------------------------------------------------------ mutants
# Each mutant: (name, target clause, relpath, transform)

def m_index_row_removed(ctx):
    p = os.path.join(ctx, "corpus/README.md")
    lines = [l for l in read(p).splitlines() if "hyprland-dispatcher-action-effects-r52" not in l]
    write(p, "\n".join(lines) + "\n")


def m_only_three_props(ctx):
    """Drop two propositions: the map falls below the frozen minimum of four."""
    p = os.path.join(ctx, ENTRY_REL)
    out = []
    for l in read(p).splitlines():
        if l.startswith("| P4 ") or l.startswith("| P5 "):
            continue
        out.append(l)
    write(p, "\n".join(out) + "\n")


def m_row_not_mined(ctx):
    p = os.path.join(ctx, "corpus/SOURCES.md")
    out = []
    for l in read(p).splitlines():
        if l.startswith("| S370 "):
            l = l.replace("| mined |", "| queued |")
        out.append(l)
    write(p, "\n".join(out) + "\n")


def m_row_opened_earlier(ctx):
    p = os.path.join(ctx, "corpus/SOURCES.md")
    out = []
    for l in read(p).splitlines():
        if l.startswith("| S371 "):
            l = l.replace("| 2026-10-27 |", "| 2026-10-26 |")
        out.append(l)
    write(p, "\n".join(out) + "\n")


def m_row_reused_from_base(ctx):
    """Point a proposition at S364, a row that already existed at the frozen base."""
    p = os.path.join(ctx, ENTRY_REL)
    write(p, read(p).replace("| S370 | Hyprland-legacy-DispatcherTranslator.cpp:45-48 |",
                             "| S364 | Hyprland-legacy-DispatcherTranslator.cpp:45-48 |"))


def m_quote_not_at_pin(ctx):
    """A quote that reads plausibly but is not at the cited line."""
    p = os.path.join(ctx, ENTRY_REL)
    write(p, read(p).replace(
        "`return Desktop::viewState()->query().selector(arg).runWindow();`",
        "`return Desktop::viewState()->query().selector(window).runWindow();`"))


def m_quote_too_long(ctx):
    """A quote over the sentence's 25-word cap, so it could never be a located quote."""
    p = os.path.join(ctx, ENTRY_REL)
    long_quote = ("`const auto& [id, name, isAutoID] = getWorkspaceIDNameFromString(args); "
                  "and then the helper resolves the workspace and creates it when the "
                  "compositor holds no workspace with that id at all`")
    write(p, read(p).replace(
        "`const auto& [id, name, isAutoID] = getWorkspaceIDNameFromString(args);`", long_quote))


def m_pin_not_manifested(ctx):
    """A pin that no manifest row declares."""
    p = os.path.join(ctx, ENTRY_REL)
    text = read(p)
    out = []
    for l in text.splitlines():
        if l.startswith("| P3 "):
            l = l.replace("| S371 | Hyprland-legacy-DispatcherTranslator.cpp:52-53 |",
                          "| S371 | Hyprland-Other-File.cpp:52-53 |")
        out.append(l)
    write(p, "\n".join(out) + "\n")


def m_pin_file_absent(ctx):
    """A proposition pins a file that is not in the round's fetch root."""
    p = os.path.join(ctx, ENTRY_REL)
    text = read(p)
    out = []
    for l in text.splitlines():
        if l.startswith("| P3 "):
            l = l.replace("| S371 | Hyprland-legacy-DispatcherTranslator.cpp:52-53 |",
                          "| S371 | Hyprland-Absent.cpp:52-53 |")
        out.append(l)
    write(p, "\n".join(out) + "\n")


def m_pin_line_out_of_range(ctx):
    p = os.path.join(ctx, ENTRY_REL)
    write(p, read(p).replace(
        "| Hyprland-legacy-DispatcherTranslator.cpp:60 |",
        "| Hyprland-legacy-DispatcherTranslator.cpp:99999 |"))


def m_manifest_row_mismatch(ctx):
    """The manifest binds the pin to rows that do not include the one cited."""
    p = os.path.join(ctx, ENTRY_REL)
    write(p, read(p).replace(
        "DispatcherTranslator.cpp | S370, S371, S372 |",
        "DispatcherTranslator.cpp | S372 |"))


def m_used_by_other_entry(ctx):
    """The registry row's used-by names another entry, not this one."""
    p = os.path.join(ctx, "corpus/SOURCES.md")
    out = []
    for l in read(p).splitlines():
        if l.startswith("| S370 "):
            l = l.replace("corpus/knowledge/hyprland-dispatcher-action-effects-r52.md",
                          "corpus/knowledge/hyprland-dispatcher-dispatch-r51.md")
        out.append(l)
    write(p, "\n".join(out) + "\n")


def m_anchor_no_fetch_root(ctx):
    """The registry row's anchor does not point into this round's fetch root."""
    p = os.path.join(ctx, "corpus/SOURCES.md")
    out = []
    for l in read(p).splitlines():
        if l.startswith("| S371 "):
            l = l.replace(".ufo/waves/round-52/fetch/Hyprland-legacy-"
                          "DispatcherTranslator.cpp", ".ufo/waves/round-51/fetch/"
                          "Hyprland-legacy-DispatcherTranslator.cpp")
        out.append(l)
    write(p, "\n".join(out) + "\n")


def m_anchor_no_revision(ctx):
    """The registry row's anchor names no 40-hex revision."""
    p = os.path.join(ctx, "corpus/SOURCES.md")
    out = []
    for l in read(p).splitlines():
        if l.startswith("| S372 "):
            l = re.sub(r"@\s*[0-9a-f]{40}", "@ norevision", l)
        out.append(l)
    write(p, "\n".join(out) + "\n")


def m_unmapped_body_row(ctx):
    """The body cites a registry row that no proposition maps."""
    p = os.path.join(ctx, ENTRY_REL)
    text = read(p).replace(
        "source: S372 - legacy movewindow dispatcher argument preparation",
        "source: S373 - a row the body cites but maps to no proposition\n"
        "source: S372 - legacy movewindow dispatcher argument preparation")
    write(p, text)
    reg = os.path.join(ctx, "corpus/SOURCES.md")
    rows = read(reg).splitlines()
    rows.insert(max(i for i, r in enumerate(rows) if r.startswith("| S37")) + 1,
                "| S373 | fixture row the body cites but maps to no proposition | code | A | a "
                "row the entry names but grounds no proposition on | "
                "Hyprland-legacy-DispatcherTranslator.cpp:1 @ %s; pin "
                ".ufo/waves/round-52/fetch/Hyprland-legacy-DispatcherTranslator.cpp | a row | "
                "mined | 2026-10-27 | on-release | corpus/knowledge/"
                "hyprland-dispatcher-action-effects-r52.md |" % REVISION)
    write(reg, "\n".join(rows) + "\n")


def m_orphan_proposition(ctx):
    """A proposition mapped to a registry row the body never cites."""
    p = os.path.join(ctx, ENTRY_REL)
    out = []
    for l in read(p).splitlines():
        if l.startswith("| P5 "):
            l = l.replace("| S372 |", "| S373 |")
        out.append(l)
    write(p, "\n".join(out) + "\n")
    reg = os.path.join(ctx, "corpus/SOURCES.md")
    rows = read(reg).splitlines()
    rows.insert(max(i for i, r in enumerate(rows) if r.startswith("| S37")) + 1,
                "| S373 | fixture row the body never cites | code | A | a row no proposition "
                "is grounded on | Hyprland-legacy-DispatcherTranslator.cpp:1 @ %s; pin "
                ".ufo/waves/round-52/fetch/Hyprland-legacy-DispatcherTranslator.cpp | a row | "
                "mined | 2026-10-27 | on-release | corpus/knowledge/"
                "hyprland-dispatcher-action-effects-r52.md |" % REVISION)
    write(reg, "\n".join(rows) + "\n")
    # The body must not cite S373 either, or the unmapped-row check fires instead and the
    # orphan check is not the one under test.
    p2 = os.path.join(ctx, ENTRY_REL)
    text = read(p2).replace("P5: The `movewindow` dispatcher strips a trailing ` silent`",
                             "P5: An unrelated claim about a trailing ` silent`")
    write(p2, text)


def m_duplicate_quote(ctx):
    """Two propositions carry the same quote: padding the proposition count."""
    p = os.path.join(ctx, ENTRY_REL)
    out = []
    for l in read(p).splitlines():
        if l.startswith("| P3 "):
            l = l.replace("| S371 | Hyprland-legacy-DispatcherTranslator.cpp:52-53 |",
                          "| S371 | Hyprland-legacy-DispatcherTranslator.cpp:46-47 |")
            l = l.replace(
                "`const auto& [id, name, isAutoID] = getWorkspaceIDNameFromString(args);`",
                "`if (arg.empty() \\|\\| arg == \"active\")`")
        out.append(l)
    write(p, "\n".join(out) + "\n")


def m_support_empty(ctx):
    """A proposition with no written support rationale."""
    p = os.path.join(ctx, ENTRY_REL)
    out = []
    for l in read(p).splitlines():
        if l.startswith("| P2 "):
            cells = l.split(" | ")
            cells[-1] = " |"
            l = " | ".join(cells)
        out.append(l)
    write(p, "\n".join(out) + "\n")


MUTANTS = [
    ("index_row_removed", "a", "corpus/README.md", m_index_row_removed),
    ("only_three_propositions", "b", ENTRY_REL, m_only_three_props),
    ("row_not_mined", "c", "corpus/SOURCES.md", m_row_not_mined),
    ("row_opened_earlier", "c", "corpus/SOURCES.md", m_row_opened_earlier),
    ("row_reused_from_base", "c", ENTRY_REL, m_row_reused_from_base),
    ("quote_not_at_pin", "d", ENTRY_REL, m_quote_not_at_pin),
    ("quote_too_long", "d", ENTRY_REL, m_quote_too_long),
    ("pin_not_manifested", "d", ENTRY_REL, m_pin_not_manifested),
    ("pin_file_absent", "d", ENTRY_REL, m_pin_file_absent),
    ("pin_line_out_of_range", "d", ENTRY_REL, m_pin_line_out_of_range),
    ("manifest_row_mismatch", "d", ENTRY_REL, m_manifest_row_mismatch),
    ("used_by_other_entry", "c", "corpus/SOURCES.md", m_used_by_other_entry),
    ("anchor_no_fetch_root", "c", "corpus/SOURCES.md", m_anchor_no_fetch_root),
    ("anchor_no_revision", "c", "corpus/SOURCES.md", m_anchor_no_revision),
    ("unmapped_body_row", "e", ENTRY_REL, m_unmapped_body_row),
    ("orphan_proposition", "e", ENTRY_REL, m_orphan_proposition),
    ("duplicate_quote", "e", ENTRY_REL, m_duplicate_quote),
    ("support_empty", "b", ENTRY_REL, m_support_empty),
]


def run_counter(counter, repo, rev, work, entry=ENTRY_REL):
    env = dict(os.environ)
    env["TMPDIR"] = work
    p = subprocess.run([sys.executable, "-I", counter, "--repo", repo, "--rev", rev,
                        "--entry", entry, "--work", os.path.join(work, "w")],
                       capture_output=True, text=True, env=env)
    return p.returncode, p.stdout + p.stderr


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--fixture", required=True)
    ap.add_argument("--counter", required=True)
    ap.add_argument("--entry", default=ENTRY_REL)
    args = ap.parse_args(argv)

    work = os.path.abspath(args.work)
    os.makedirs(work, exist_ok=True)
    base_rev = git(args.fixture, "rev-parse", "HEAD").stdout.strip()

    # Green control first: the unmutated fixture must pass.
    rc, out = run_counter(args.counter, args.fixture, base_rev, work, args.entry)
    green_ok = rc == 0 and "verdict=TARGET_MET" in out
    print("MUTANTS: green rc=%d verdict_met=%s" % (rc, green_ok))
    if not green_ok:
        print(out)

    failures = 0
    # One scratch clone, reset between mutants: 18 clones of the lane is 18 chances to fail on
    # a transient filesystem error, and the mutation is the only thing that should change.
    clone = os.path.join(work, "mut-clone")
    if os.path.exists(clone):
        shutil.rmtree(clone)
    subprocess.run(["git", "clone", "--no-hardlinks", "--quiet", args.fixture, clone], check=True)
    assert_toplevel(clone, clone)
    green_rev = git(clone, "rev-parse", "HEAD").stdout.strip()
    for name, clause, relpath, fn in MUTANTS:
        git(clone, "reset", "--hard", "-q", green_rev)
        git(clone, "clean", "-qfdx")
        fn(clone)
        git(clone, "add", "-A")
        git(clone, "-c", "user.name=mut", "-c", "user.email=mut@localhost",
            "commit", "-q", "--allow-empty", "-m", "mutant: %s" % name)
        rev = git(clone, "rev-parse", "HEAD").stdout.strip()
        rc, out = run_counter(args.counter, clone, rev, work, args.entry)
        missed = [l for l in out.splitlines() if l.startswith("C2_R52: %s ok=0" % clause)]
        caught = rc != 0 and bool(missed)
        if not caught:
            failures += 1
        print("MUTANTS: %-24s want=%s rc=%d %s" % (name, clause, rc,
                                                   "CAUGHT" if caught else "ESCAPED"))
        for l in out.splitlines():
            if l.startswith("C2_R52: ") and " ok=0 " in l:
                print("    %s" % l)
    shutil.rmtree(clone, ignore_errors=True)

    print("MUTANTS: mutants=%d escaped=%d green_ok=%s" % (len(MUTANTS), failures, green_ok))
    return 0 if failures == 0 and green_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
