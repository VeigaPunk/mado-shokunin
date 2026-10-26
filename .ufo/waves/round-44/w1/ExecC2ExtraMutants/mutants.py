#!/usr/bin/env python3
"""Clause mutants of the ExecC2ExtraMutants positive fixture (PRED-C2-r44).

Each mutant is ONE defect applied to the positive commit, committed, scored
with the frozen counter, saved as a patch, then the tree is reset. Usage:
  python3 mutants.py /abs/path/to/fixture/repo
"""
import os
import re
import subprocess
import sys

SEAT = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
BASE = "6a1a90528fe533cadee506a9fa3e9d13d15cc41f"
COUNTER = os.path.join(LANE, "quality/counters/c2-r44-gkeep-size-request.py")
ENTRY = "corpus/knowledge/hyprland-gkeep-size-request-r44.md"
LESSON = "corpus/lessons/round-44.md"
README = "corpus/README.md"
SOURCES = "corpus/SOURCES.md"

C1 = "gkeep client default_size=420x500 size_request_calls=0 application_id=org.omarchy.gkeep"
C2 = "hyprland sendWindowSize xdg_setSize=1 x11_configure=1"

G_S164 = ('GATE S164 receipt=.ufo/waves/round-44/fetch/Hyprland-Window.cpp '
          'sha256=d735d454cc4b7983f19626514d310669047da46780c509ffae68ccf072211ded '
          'quote="const auto REPORTSIZE = realToReportSize();"')
G_S298 = ('GATE S298 receipt=.ufo/waves/round-44/fetch/Hyprland-XDGShell.cpp '
          'sha256=d90b534c9097ab573f606c2dad4b5fab6dc31c4ca13240c43ef0bb74da7ed0c0 '
          'quote="m_stateUpdate = g_pEventLoopManager->doLaterLock([this] { configure(); });"')
G_S299 = ('GATE S299 receipt=.ufo/waves/round-44/fetch/xdg-shell.xml '
          'sha256=7ba7f9c8473deee674cb1f154a18abd0bb0cc072604fc055b0c15e459fc4c7df '
          'quote="This configure event asks the client to resize its toplevel surface or to change its state."')
G_S300 = ('GATE S300 receipt=.ufo/waves/round-44/fetch/gdktoplevel-wayland.c '
          'sha256=0ee384588284574ee64fa08e45c73149b3ff2d20816d80cf3e055821bb867fbe '
          'quote="if (saved_size && !fixed_size && was_fixed_size)"')
G_S301 = ('GATE S301 receipt=.ufo/waves/round-44/fetch/gkeep-ui.py '
          'sha256=07a3c4a50bf2154edc82f531b1cf2cc3c6e7067e9f2f02d5a4b4d9d27fe5d66a '
          'quote="window.set_default_size(420, 500) self.board = Board(window)"')
ADMIT = ("ADMIT merge/mado/knowledge/corpus/knowledge/gkeep-client-size-request-r12.md "
         "as corpus/knowledge/hyprland-gkeep-size-request-r44.md")
REFUSE = ("REFUSE merge/mado/knowledge/corpus/knowledge/gkeep-geometry-never-recorded-r15.md "
          "reason=its journal route never names the configure the client receives, so the size "
          "it calls unobservable is in fact sent and acked; flip once a pinned source shows the "
          "configure skipped for a mapped window")
R_S298 = ("| S298 | Hyprland v0.56.2 xdg shell implementation - how a toplevel size request "
          "becomes a scheduled configure - ")
README_ROW_START = "| `knowledge/hyprland-gkeep-size-request-r44.md`"


def git(repo, *args, check=True):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    if check and p.returncode != 0:
        raise SystemExit("git %s failed: %s %s" % (args, p.stdout, p.stderr))
    return p.stdout


def ed(repo, path, old, new, count=1):
    full = os.path.join(repo, path)
    text = open(full).read()
    n = text.count(old)
    if n != count:
        raise SystemExit("edit target count %d != %d in %s: %r" % (n, count, path, old[:70]))
    open(full, "w").write(text.replace(old, new))


def line(text):
    return text + "\n"


def find_line(repo, path, prefix):
    for l in open(os.path.join(repo, path)):
        if l.startswith(prefix):
            return l
    raise SystemExit("no line starting %r in %s" % (prefix, path))


def row_for(repo, sid):
    for l in open(os.path.join(repo, SOURCES)):
        if l.startswith("| " + sid + " |"):
            return l
    raise SystemExit("row %s not found" % sid)


# --- mutants: (name, one-line defect statement, [ops]) -----------------------
# op = (path, old, new) applied with the count assertion inside ed().
def mutants(repo):
    s164 = row_for(repo, "S164")
    s298 = row_for(repo, "S298")
    s299 = row_for(repo, "S299")
    s300 = row_for(repo, "S300")
    s301 = row_for(repo, "S301")
    rd = [l for l in open(os.path.join(repo, README)) if l.startswith(README_ROW_START)][0]
    return [
        ("01-header-verified-at-pushed",
         "verified-at moved out of the 20-line header window",
         [(ENTRY, "verified-at: 2026-10-26\n", ""),
          (ENTRY, "\n## What this entry does not establish",
           "\nverified-at: 2026-10-26\n\n## What this entry does not establish")]),
        ("02-source-outside-window",
         "a sixth source: line outside the header window",
         [(ENTRY, "\n## What this entry does not establish",
           "\nsource: S300 - repeated source note\n\n## What this entry does not establish")]),
        ("03-ghost-id",
         "an S### token that is not a cited id",
         [(ENTRY, "\n## What this entry does not establish",
           "\nSee S999 for the case this entry leaves open.\n\n## What this entry does not establish")]),
        ("04-verified-at-wrong",
         "verified-at names a different date",
         [(ENTRY, "verified-at: 2026-10-26", "verified-at: 2026-10-25")]),
        ("05-recheck-invalid",
         "recheck is not a date / NNd / on-* token",
         [(ENTRY, "recheck: 90d - ", "recheck: whenever - ")]),
        ("06-row-status-queued",
         "S298 registry status is queued, not mined",
         [(SOURCES, "reuses the serial | mined | 2026-10-26 |",
           "reuses the serial | queued | 2026-10-26 |")]),
        ("07-row-usedby-missing",
         "S301 used-by does not name the entry",
         [(SOURCES, "by any reported size | mined | 2026-10-26 | 90d | " + ENTRY + " |",
           "by any reported size | mined | 2026-10-26 | 90d | \u2014 |")]),
        ("08-row-opened-wrong",
         "S299 opened 2026-10-25, not the freeze date",
         [(SOURCES, "applied only at the client's ack | mined | 2026-10-26 |",
           "applied only at the client's ack | mined | 2026-10-25 |")]),
        ("09-row-ten-cells",
         "S300 row loses the tier cell (10 cells)",
         [(SOURCES, "gdktoplevel-wayland.c | code | A |", "gdktoplevel-wayland.c | code |")]),
        ("10-row-badloc",
         "S300 anchor cell carries a localized-documentation marker",
         [(SOURCES, "the saved-size comment and restore |",
           "the saved-size comment and restore (zhihu) |")]),
        ("11-s164-anchor-cell",
         "held S164 anchor cell edited (cells 1-9 differ from base)",
         [(SOURCES, s164, s164.replace("src/desktop/view/Window.cpp:103-108,141-146",
                                       "src/desktop/view/Window.cpp:103-109,141-146"))]),
        ("12-s164-status-cell",
         "held S164 status cell edited to queued",
         [(SOURCES, s164, s164.replace("| mined | 2026-10-23 |", "| queued | 2026-10-23 |"))]),
        ("13-s164-usedby-dropped",
         "held S164 used-by drops its base item",
         [(SOURCES, "corpus/knowledge/rule-attribution-r24.md, " + ENTRY, ENTRY)]),
        ("14-gate-sha-wrong",
         "S298 Gate sha256 has one hex digit changed",
         [(LESSON, G_S298, G_S298.replace("d90b534c9097ab57", "d90b534c9097ab58"))]),
        ("15-gate-quote-in-comment",
         "S164 Gate quote is a // comment in the receipt",
         [(LESSON, G_S164,
           G_S164.replace("const auto REPORTSIZE = realToReportSize();",
                          "TODO: this should be decoupled from setWindowSize IMO")),
          (ENTRY, "`const auto REPORTSIZE = realToReportSize();` (Hyprland-Window.cpp:1741)",
           "`TODO: this should be decoupled from setWindowSize IMO` (Hyprland-Window.cpp:1738)")]),
        ("16-gate-quote-twice",
         "S164 Gate quote occurs twice in the receipt",
         [(LESSON, G_S164,
           G_S164.replace("const auto REPORTSIZE = realToReportSize();",
                          "Animation::mgr()->createAnimation(Vector2D(0, 0), pWindow->sizeAnimation(),")),
          (ENTRY, "`const auto REPORTSIZE = realToReportSize();` (Hyprland-Window.cpp:1741)",
           "`Animation::mgr()->createAnimation(Vector2D(0, 0), pWindow->sizeAnimation(),` (Hyprland-Window.cpp:111)")]),
        ("17-gate-quote-too-long",
         "S164 Gate quote is 29 words (limit 25)",
         [(LESSON, G_S164,
           G_S164.replace("const auto REPORTSIZE = realToReportSize();",
                          "const auto REPORTPOS = realToReportPosition(); const auto REPORTSIZE = realToReportSize(); "
                          "if (!force && m_pendingReportedSize == REPORTSIZE && (m_reportedPosition == REPORTPOS || "
                          "!m_isX11)) return; m_reportedPosition = REPORTPOS; m_pendingReportedSize = REPORTSIZE;")),
          (ENTRY, "`const auto REPORTSIZE = realToReportSize();` (Hyprland-Window.cpp:1741)",
           "`const auto REPORTPOS = realToReportPosition(); const auto REPORTSIZE = realToReportSize(); "
           "if (!force && m_pendingReportedSize == REPORTSIZE && (m_reportedPosition == REPORTPOS || "
           "!m_isX11)) return; m_reportedPosition = REPORTPOS; m_pendingReportedSize = REPORTSIZE;` "
           "(Hyprland-Window.cpp:1739)")]),
        ("18-gate-quote-word-boundary",
         "S300 Gate quote starts inside a word",
         [(LESSON, G_S300,
           G_S300.replace('quote="if (saved_size', 'quote="f (saved_size')),
          (ENTRY, "`if (saved_size && !fixed_size && was_fixed_size)` (gdktoplevel-wayland.c:656)",
           "`f (saved_size && !fixed_size && was_fixed_size)` (gdktoplevel-wayland.c:656)")]),
        ("19-locator-off-by-one",
         "S300 claim locator off by one (657)",
         [(ENTRY, "(gdktoplevel-wayland.c:656)", "(gdktoplevel-wayland.c:657)")]),
        ("20-locator-wrong-start",
         "S301 claim locator starts one line late (477)",
         [(ENTRY, "(gkeep-ui.py:476-477)", "(gkeep-ui.py:477)")]),
        ("21-census-x11-count",
         "census line reports x11_configure=0",
         [(ENTRY, C2, "hyprland sendWindowSize xdg_setSize=1 x11_configure=0")]),
        ("22-census-client-size",
         "client census line reports 421x500",
         [(ENTRY, C1, C1.replace("420x500", "421x500"))]),
        ("23-census-fenced",
         "the two census lines are inside a fence",
         [(ENTRY, C1 + "\n" + C2 + "\n", "```\n" + C1 + "\n" + C2 + "\n```\n")]),
        ("24-census-duplicated",
         "the sendWindowSize census line appears twice",
         [(ENTRY, C2 + "\n", C2 + "\n" + C2 + "\n")]),
        ("25-readme-row-missing",
         "no README index row for the entry",
         [(README, rd, "")]),
        ("26-readme-row-doubled",
         "two README index rows for the entry",
         [(README, rd, rd + rd)]),
        ("27-admit-round43-file",
         "ADMIT names gkeep-size-to-real-size-r11.md, outside STAGED",
         [(LESSON, "knowledge/gkeep-client-size-request-r12.md as",
           "knowledge/gkeep-size-to-real-size-r11.md as")]),
        ("28-admit-target-wrong",
         "ADMIT target is not the entry path",
         [(LESSON, "as corpus/knowledge/hyprland-gkeep-size-request-r44.md",
           "as corpus/knowledge/other-r44.md")]),
        ("29-refuse-no-flip",
         "REFUSE reason loses its flip word",
         [(LESSON, "flip once a pinned source shows", "flip provided a pinned source shows")]),
        ("30-refuse-short",
         "REFUSE reason shorter than 20 characters",
         [(LESSON, REFUSE, "REFUSE merge/mado/knowledge/corpus/knowledge/gkeep-geometry-never-recorded-r15.md reason=short note")]),
        ("31-refuse-same-as-admit",
         "REFUSE names the same staged file as ADMIT",
         [(LESSON, "knowledge/gkeep-geometry-never-recorded-r15.md reason=",
           "knowledge/gkeep-client-size-request-r12.md reason=")]),
        ("32-gate-indented",
         "S300 Gate line indented (outside column 0)",
         [(LESSON, G_S300, "  " + G_S300)]),
        ("33-gate-outside-section",
         "S301 Gate line moved out of ## Gate into the next section",
         [(LESSON, G_S301 + "\n", ""),
          (LESSON, "read-only)\n\nThe staged",
           "read-only)\n\n" + G_S301 + "\n\nThe staged")]),
        ("34-gate-duplicated",
         "two Gate lines for S298",
         [(LESSON, G_S298, G_S298 + "\n" + G_S298)]),
        ("35-gate-receipt-round43-dir",
         "S164 Gate receipt names the round-43 fetch dir (same bytes, wrong dir)",
         [(LESSON, "receipt=.ufo/waves/round-44/fetch/Hyprland-Window.cpp",
           "receipt=.ufo/waves/round-43/fetch/Hyprland-Window.cpp")]),
        ("36-pin-uncited",
         "the gdktoplevel-wayland.c pin loses its Gate line",
         [(LESSON, G_S300 + "\n", "")]),
        ("37-source-line-dropped",
         "S301 left out of the header source list",
         [(ENTRY, "source: S301 - own-work: the full ~/Projects/gkeep/gkeep/ui.py at gkeep 133b867, pinned at .ufo/waves/round-44/fetch/gkeep-ui.py - what the app declares\n", "")]),
        ("38-body-line-extra-id",
         "the S299 claim line also names S164",
         [(ENTRY, "**OBS** S299 - the protocol calls", "**OBS** S299 and S164 - the protocol calls")]),
        ("39-body-line-in-fence",
         "the S300 claim line sits inside a fence",
         [(ENTRY, "**OBS** S300 - the GTK toplevel configure handler",
           "```\n**OBS** S300 - the GTK toplevel configure handler"),
          (ENTRY, "(lines 681-682), which is the size the toolkit will arrange to.",
           "(lines 681-682), which is the size the toolkit will arrange to.\n```")]),
        ("40-row-duplicate",
         "S301 has two registry rows",
         [(SOURCES, s301, s301 + s301)]),
        ("41-row-loc-collision",
         "S299 registry location is S300's location",
         [(SOURCES, s299, re.sub(
             r"https://gitlab\.freedesktop\.org/wayland/wayland-protocols/-/raw/1\.49/stable/xdg-shell/xdg-shell\.xml",
             "https://gitlab.gnome.org/GNOME/gtk/-/raw/4.24.1/gdk/wayland/gdktoplevel-wayland.c", s299))]),
        ("42-claim-line-dropped",
         "no entry line carries the S301 claim (source line only)",
         [(ENTRY, find_line(repo, ENTRY, "**OBS** S301"), "")]),
        ("43-too-few-source-lines",
         "header lists three ids, below the four-id floor",
         [(ENTRY, find_line(repo, ENTRY, "source: S298"), ""),
          (ENTRY, find_line(repo, ENTRY, "source: S299"), "")]),
        ("44-refuse-missing",
         "the Gate has an ADMIT and no REFUSE",
         [(LESSON, find_line(repo, LESSON, "REFUSE "), "")]),
        ("45-s164-row-removed",
         "the held S164 registry row is deleted",
         [(SOURCES, s164, "")]),
        ("46-census-line-removed",
         "the client census line is deleted",
         [(ENTRY, C1 + "\n", "")]),
        ("47-usedby-renamed",
         "S298 used-by names a path that is not the entry",
         [(SOURCES, "reuses the serial | mined | 2026-10-26 | 90d | " + ENTRY + " |",
           "reuses the serial | mined | 2026-10-26 | 90d | " + ENTRY[:-3] + " |")]),
        ("48-cross-receipt-quote",
         "S164 Gate quote also occurs in the S298 receipt",
         [(LESSON, G_S164,
           G_S164.replace("const auto REPORTSIZE = realToReportSize();",
                          "switch (edges) { case")),
          (ENTRY, "`const auto REPORTSIZE = realToReportSize();` (Hyprland-Window.cpp:1741)",
           "`switch (edges) { case` (Hyprland-Window.cpp:84)")]),
        # --- semantic probes: defects a syntactic predicate may not see ---
        ("49-misread-quote",
         "the S300 prose asserts the opposite of the quote it cites (true quote, true locator)",
         [(ENTRY, "a non-zero width and height with a non-fixed state is stored as `next_layout.configured_width`",
           "a non-zero width and height is ignored by the toolkit unless the state is fixed, so it is discarded as `next_layout.configured_width`")]),
        ("50-row-kind-ownwork",
         "S300's kind cell says own-work for an upstream file",
         [(SOURCES, "gdktoplevel-wayland.c | code | A |", "gdktoplevel-wayland.c | own-work | A |")]),
        ("51-census-prefix-hides-claim",
         "a line starting `hyprland sendWindowSize ` names S299 with no quote and no locator",
         [(ENTRY, C2 + "\n", C2 + "\nhyprland sendWindowSize S299 is the document that licenses this whole section\n")]),
    ]


def score(repo):
    p = subprocess.run([sys.executable, "-I", COUNTER, "--repo", repo, "--rev", "HEAD",
                        "--base", BASE], capture_output=True, text=True, cwd=LANE)
    last = [l for l in p.stdout.splitlines() if l.startswith("PRED-C2-r44:")]
    cl = [l for l in p.stdout.splitlines() if "clauses=" in l]
    return p.returncode, (last[-1] if last else "<no final line>"), (cl[-1] if cl else "")


def main():
    repo = os.path.abspath(sys.argv[1])
    pos = git(repo, "rev-parse", "HEAD").strip()
    if git(repo, "status", "--porcelain").strip():
        raise SystemExit("fixture tree not clean")
    outdir = os.path.join(SEAT, "mutants")
    os.makedirs(outdir, exist_ok=True)
    rows = []
    for name, defect, ops in mutants(repo):
        git(repo, "reset", "-q", "--hard", pos)
        for path, old, new in ops:
            ed(repo, path, old, new)
        git(repo, "add", "-A")
        git(repo, "-c", "user.name=mado-exec", "-c", "user.email=exec@seat.invalid",
            "commit", "-q", "-m", "mutant: " + name)
        rc, last, cl = score(repo)
        diff = git(repo, "diff", pos, "HEAD")
        with open(os.path.join(outdir, name + ".patch"), "w") as fh:
            fh.write(diff)
        admitted = "admitted=1" in last and "TARGET_MET" in last
        rows.append((name, defect, "ADMITTED" if admitted else "refused", last, cl))
        print("%-28s %s  %s" % (name, "SURVIVOR" if admitted else "killed", cl.split("clauses=")[-1].split(" admitted")[0] if cl else last))
        sys.stdout.flush()
    git(repo, "reset", "-q", "--hard", pos)
    with open(os.path.join(SEAT, "scores.tsv"), "w") as fh:
        fh.write("mutant\tdefect\tverdict\tfinal\tclauses\n")
        for r in rows:
            fh.write("\t".join(r) + "\n")
    surv = [r for r in rows if r[2] == "ADMITTED"]
    print("\n%d mutants, %d survivors" % (len(rows), len(surv)))
    for r in surv:
        print("SURVIVOR:", r[0], "-", r[1])


if __name__ == "__main__":
    main()
