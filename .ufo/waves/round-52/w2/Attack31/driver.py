#!/usr/bin/env python3
"""Attack31 discrimination battery: landed counter vs W1 draft counter.

Builds a 'green-variant' fixture inside the scratch clone at
/fast/scratch/hyaku/mado-r52/Attack31/repo: the committed landed round-52 state
(entry + S370-S373 rows + README + fetch/), repaired ONLY where both counters
would otherwise disagree for reasons outside this seat's target (table column
order for the landed regex, pin manifest / id-citation / anchor-fetch-root
shape for the draft counter, contiguous P16 quote). Then applies one mutation
per commit and records both counters' verdicts.
"""
import os
import re
import subprocess
import sys

REPO = "/fast/scratch/hyaku/mado-r52/Attack31/repo"
WORK = "/fast/scratch/hyaku/mado-r52/Attack31/work"
OUT = "/fast/scratch/hyaku/mado-r52/Attack31/receipts"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
LANDED_COUNTER = "quality/counters/c2-r52-proposition-entry.py"
DRAFT_COUNTER = LANE + "/.ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py"
ENTRY = "corpus/knowledge/hyprland-synthetic-dispatch-r52.md"
REG = "corpus/SOURCES.md"
FETCH_SHA = {
    "Hyprland-legacy-DispatcherTranslator.cpp":
    "7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771",
    "Hyprland-ConfigActions.cpp":
    "a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637",
    "Hyprland-ConfigActions.hpp":
    "746c6f517620eb039afbfbb9a4a0e2d5ba1c5eb117bcc8f396173f63091b7073",
    "Hyprland-KeybindManager.cpp":
    "8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40",
}
REV = "efb50993780079460b0cbed1363e2166a2de1d9f"


def git(*args):
    p = subprocess.run(["git", "-C", REPO, *args], capture_output=True, text=True)
    return p


def top():
    t = git("rev-parse", "--show-toplevel").stdout.strip()
    assert os.path.realpath(t) == os.path.realpath(REPO), t


def write_rel(rel, text):
    p = os.path.join(REPO, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as fh:
        fh.write(text)


def read_rel(rel):
    with open(os.path.join(REPO, rel)) as fh:
        return fh.read()


def commit(msg):
    top()
    git("add", "-A")
    p = git("-c", "user.email=att31@scratch", "-c", "user.name=Attack31",
            "commit", "-qm", msg)
    assert p.returncode == 0, p.stderr


def reset_green():
    top()
    git("reset", "--hard", "-q", "GREEN")


def run_counter(script, tag, extra=None):
    os.makedirs(WORK, exist_ok=True)
    cmd = ["python3", "-I", script, "--repo", REPO, "--rev", "HEAD",
           "--work", WORK]
    if extra:
        cmd += extra
    if script == DRAFT_COUNTER:
        cmd += ["--entry", ENTRY]
    else:
        cmd += ["--entry", ENTRY]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.stdout + p.stderr + "exit=%d\n" % p.returncode


def green_entry_text():
    """Landed entry, table reordered to satisfy BOTH grammars, P16 made contiguous,
    and a single prose line that references every id (draft clause e)."""
    src = read_rel(ENTRY)
    lines = src.splitlines()
    head, table, tail = [], [], []
    state = "head"
    for ln in lines:
        if state == "head" and ln.startswith("| ID"):
            state = "table"
            continue
        if state == "table":
            if ln.startswith("|"):
                if ln.startswith("|---"):
                    continue
                table.append(ln)
                continue
            state = "tail"
            tail.append(ln)
            continue
        (head if state == "head" else tail).append(ln)
    rows = []
    for ln in table:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        pid, claim, sid, pinanchor, quote, sclass, why = cells
        # P16's landed quote splices :1554 and :1558 non-contiguously; the
        # contiguous licensed quote is the :1554 call alone.
        if pid == "P16":
            pinanchor = "Hyprland-ConfigActions.cpp:1554"
            quote = "g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);"
        pin = pinanchor
        rows.append("| %s | %s | %s | %s | %s | %s | %s |"
                    % (pid, sid, claim, pin, pinanchor, quote, why))
    out = head
    out.append("| ID | Source row | Proposition | Pin:anchor | Anchor | "
               "Quote (<=25 words) | Why it supports |")
    out.append("|---|---|---|---|---|---|---|")
    out += rows
    out.append("")
    out.append("sourced: P01-P18")
    out += tail
    return "\n".join(out) + "\n"


def green_registry_text():
    """Landed registry with anchor cells carrying fetch-root pin paths (draft (c))."""
    src = read_rel(REG)
    repl = {
        "S370": ("DispatcherTranslator.cpp:531-627",
                 "Hyprland-legacy-DispatcherTranslator.cpp"),
        "S371": ("ConfigActions.cpp:1530-1616",
                 "Hyprland-ConfigActions.cpp"),
        "S372": ("ConfigActions.hpp:114-117",
                 "Hyprland-ConfigActions.hpp"),
        "S373": ("KeybindManager.cpp:221-242",
                 "Hyprland-KeybindManager.cpp"),
    }
    for sid, (span, pin) in repl.items():
        old = "%s @ %s; r52 fetch SHA256 %s" % (span, REV, FETCH_SHA[pin])
        new = ("%s @ %s; pin .ufo/waves/round-52/fetch/%s sha256:%s"
               % (span, REV, pin, FETCH_SHA[pin]))
        assert old in src, (sid, old)
        src = src.replace(old, new)
    return src


def stage_green():
    write_rel(ENTRY, green_entry_text())
    write_rel(REG, green_registry_text())
    commit("green-variant: landed content, both-grammar table, fixed anchors")


def mutate_and_run(name, fn, note=""):
    reset_green()
    fn()
    commit("mutant " + name)
    land = run_counter(os.path.join(REPO, LANDED_COUNTER), name)
    draft = run_counter(DRAFT_COUNTER, name)
    with open(os.path.join(OUT, "m-%s.txt" % name), "w") as fh:
        fh.write("== mutant %s == %s\n\n-- landed counter --\n%s\n-- draft counter --\n%s"
                 % (name, note, land, draft))
    lv = "MET" if "verdict=TARGET_MET" in land else ("SETUP" if "setup" in land else "MISS")
    dv = "MET" if "verdict=TARGET_MET" in draft else ("SETUP" if "setup" in draft else "MISS")
    print("%-26s landed=%-5s draft=%-5s" % (name, lv, dv))
    return lv, dv


def edit_entry(fn):
    write_rel(ENTRY, fn(read_rel(ENTRY)))


def edit_reg(fn):
    write_rel(REG, fn(read_rel(REG)))


def main():
    landed = git("rev-list", "--all", "--grep",
                 "stage landed r52 state").stdout.split()[0]
    top()
    git("reset", "--hard", "-q", landed)
    git("tag", "-f", "GREEN")
    stage_green()
    git("tag", "-f", "GREEN")
    land = run_counter(os.path.join(REPO, LANDED_COUNTER), "green")
    draft = run_counter(DRAFT_COUNTER, "green")
    with open(os.path.join(OUT, "m-green.txt"), "w") as fh:
        fh.write("-- landed --\n%s\n-- draft --\n%s" % (land, draft))
    print("%-26s landed=%-5s draft=%-5s" % ("green",
          "MET" if "verdict=TARGET_MET" in land else "MISS",
          "MET" if "verdict=TARGET_MET" in draft else "MISS"))

    # -- mutants ----------------------------------------------------------
    def m_dup_claim():
        # exact duplicate claim: P17 repeats P04's claim text
        def f(t):
            p04 = re.search(r"\| P04 \| S370 \| ([^|]+) \|", t).group(1)
            return re.sub(r"(\| P17 \| S370 \| )[^|]+( \|)", r"\g<1>" + p04 + r"\g<2>", t)
        edit_entry(f)
    mutate_and_run("dup-claim", m_dup_claim,
                   "P17 claim := P04 claim verbatim")

    def m_near_dup_claim():
        def f(t):
            return t.replace("can invoke its delegate twice for a successful repeat state",
                             "may run its delegate a second time on success")
        edit_entry(f)
    mutate_and_run("near-dup-claim", m_near_dup_claim,
                   "P17 claim paraphrases P04 (semantic duplicate, distinct key)")

    def m_dup_quote():
        def f(t):
            p04q = re.search(r"\| P04 \| S370 \|[^|]+\|[^|]+\|[^|]+\| ([^|]+) \|",
                             t).group(1)
            return re.sub(
                r"(\| P17 \| S370 \|[^|]+\|[^|]+\|[^|]+\| )[^|]+( \|)",
                lambda m: m.group(1) + p04q + m.group(2), t)
        edit_entry(f)
    mutate_and_run("dup-quote", m_dup_quote,
                   "P17 quote := P04 quote verbatim (same fact, same quote)")

    def m_fab_quote():
        def f(t):
            return t.replace(
                'if (STATE != "down" && STATE != "repeat" && STATE != "up")',
                "the moon is made of green cheese and crackers")
        edit_entry(f)
    mutate_and_run("fab-quote", m_fab_quote,
                   "P02 quote := fabricated 8-word sentence, pin/anchor untouched")

    def m_phantom_pin():
        def f(t):
            return t.replace(
                "| P02 | S370 | The accepted state strings are `down`, `repeat`, `up`; others are rejected. | Hyprland-legacy-DispatcherTranslator.cpp:597-598 | Hyprland-legacy-DispatcherTranslator.cpp:597-598 |",
                "| P02 | S370 | The accepted state strings are `down`, `repeat`, `up`; others are rejected. | Hyprland-NoSuchFile.cpp:10-12 | Hyprland-NoSuchFile.cpp:10-12 |")
        edit_entry(f)
    mutate_and_run("phantom-pin", m_phantom_pin,
                   "P02 pin := nonexistent file")

    def m_unmapped_cited():
        def f(t):
            row = ("| S374 | Hyprland 0.56.2 executor spawn surface - "
                   "https://raw.githubusercontent.com/hyprwm/Hyprland/%s/"
                   "src/supplementary/executor/Executor.cpp | code | A | "
                   "exec downstream spawn | Executor.cpp:1-50 @ %s; "
                   "pin .ufo/waves/round-52/fetch/Hyprland-legacy-DispatcherTranslator.cpp "
                   "sha256:%s | opened but never mapped | mined | 2026-10-27 | "
                   "on-release | corpus/knowledge/hyprland-synthetic-dispatch-r52.md |"
                   % (REV, REV, FETCH_SHA["Hyprland-legacy-DispatcherTranslator.cpp"]))
            return t.replace("## Paths", row + "\n\n## Paths")
        edit_reg(f)
        edit_entry(lambda t: t.replace("sourced: P01-P18",
                                       "sourced: P01-P18; also opened S374"))
    mutate_and_run("unmapped-cited", m_unmapped_cited,
                   "fresh mined row S374 used-by entry, prose-cited, mapped by no proposition")

    def m_unmapped_uncited():
        def f(t):
            row = ("| S375 | Hyprland 0.56.2 shortcuts inhibit gate - "
                   "https://raw.githubusercontent.com/hyprwm/Hyprland/%s/"
                   "src/protocols/ShortcutsInhibit.cpp | code | A | "
                   "inhibit gate state | ShortcutsInhibit.cpp:1-40 @ %s; "
                   "pin .ufo/waves/round-52/fetch/Hyprland-KeybindManager.cpp "
                   "sha256:%s | opened but never mapped or cited | mined | 2026-10-27 | "
                   "on-release | corpus/knowledge/hyprland-synthetic-dispatch-r52.md |"
                   % (REV, REV, FETCH_SHA["Hyprland-KeybindManager.cpp"]))
            return t.replace("## Paths", row + "\n\n## Paths")
        edit_reg(f)
    mutate_and_run("unmapped-uncited", m_unmapped_uncited,
                   "fresh mined row S375 used-by entry, NEITHER cited NOR mapped")

    def m_orphan_prop():
        def f(t):
            row = ("| P19 | S370 | sendkeystate returns the delegate result. | "
                   "Hyprland-legacy-DispatcherTranslator.cpp:621-622 | "
                   "Hyprland-legacy-DispatcherTranslator.cpp:621-622 | "
                   "result.success) result = sendshortcut(modifiedArgs); | "
                   "The dispatcher hands back the delegate result verbatim. |")
            return t.replace("\n\nsourced: P01-P18",
                             "\n" + row + "\n\nsourced: P01-P18")
        edit_entry(f)
    mutate_and_run("orphan-prop", m_orphan_prop,
                   "P19 mapped inside table but never drawn on by prose")

    def m_missing_row():
        edit_entry(lambda t: t.replace("| P05 | S370 |", "| P05 | S399 |"))
    mutate_and_run("missing-row", m_missing_row,
                   "P05 maps a row that does not exist (control)")

    def m_index_removed():
        def f(t):
            return re.sub(r"^\| `knowledge/hyprland-synthetic-dispatch-r52\.md`[^\n]*\n",
                          "", t, count=1, flags=re.M)
        write_rel("corpus/README.md", f(read_rel("corpus/README.md")))
    mutate_and_run("index-removed", m_index_removed,
                   "README index row deleted (control)")

    def m_single_row():
        edit_entry(lambda t: t.replace("| S371 |", "| S370 |")
                                .replace("| S372 |", "| S370 |")
                                .replace("| S373 |", "| S370 |"))
    mutate_and_run("single-row", m_single_row,
                   "all 18 propositions rest on one row")

    def m_row_reuse():
        # prop maps to a round-51 row; used-by patched so substring checks pass
        edit_entry(lambda t: t.replace(
            "| P05 | S370 |", "| P05 | S364 |"))
        edit_reg(lambda t: t.replace(
            "corpus/knowledge/hyprland-dispatcher-dispatch-r51.md |\n",
            "corpus/knowledge/hyprland-dispatcher-dispatch-r51.md, "
            "corpus/knowledge/hyprland-synthetic-dispatch-r52.md |\n", 1))
    mutate_and_run("row-reuse", m_row_reuse,
                   "P05 maps S364 (opened round 51); row stays at base too")

    def m_rowmeta_spoof():
        # status=queued, opened=2026-10-25, but 'mined' and the date live in teaches
        def f(t):
            old = ("| mined | 2026-10-27 | on-release | "
                   "corpus/knowledge/hyprland-synthetic-dispatch-r52.md |")
            i = t.find("| S372 |")
            j = t.find("\n", i)
            row = t[i:j]
            spoof = row.replace("| mined | 2026-10-27 |",
                                "| queued | 2026-10-25 |").replace(
                "identifies action-state field used by implementation",
                "identifies action-state field used by implementation; "
                "mined status landed 2026-10-27")
            return t[:i] + spoof + t[j:]
        edit_reg(f)
    mutate_and_run("rowmeta-spoof", m_rowmeta_spoof,
                   "S372 status=queued opened=2026-10-25 with mined/2026-10-27 in teaches")

    def m_quote_26w():
        def f(t):
            return t.replace(
                "CVarList2 ARGS(args, 4); if (ARGS.size() != 4)",
                "CVarList2 ARGS(args, 4); if (ARGS.size() != 4) "
                "return error invalid args sendkeystate takes exactly four "
                "comma separated fields and rejects every other count now")
        edit_entry(f)
    mutate_and_run("quote-26w", m_quote_26w,
                   "P01 quote := 26 words (control: both should catch)")

    def m_empty_claim():
        def f(t):
            return re.sub(r"(\| P02 \| S370 \|) [^|]+ (\|)",
                          r"\g<1>   \g<2>", t)
        edit_entry(f)
    mutate_and_run("empty-claim", m_empty_claim,
                   "P02 claim cell blanked")


    print("\nreceipts in", OUT)


if __name__ == "__main__":
    main()
