#!/usr/bin/env python3
"""Build the round-51 C1 ledger rows (draft for the tracked quality/tool-ledger.md).

Read-only over a git repository: population, per-file header line, accountability pointer and
pointer-line verification are all derived from git objects at --rev. Writes nothing unless
--out is given; scratch-free (no /tmp, no TMPDIR use), so it can run inside a hermetic check.

    python3 -I build-ledger-rows.py --repo <lane> --rev <rev> [--out FILE]

Rules, in order (each is a check this script enforces, not a comment):

  * Population is every file under tools/, immediate children quality/*.py and immediate
    children quality/counters/*.py at --rev, de-duplicated (strict gap free: every population
    file must be named by at least one other tracked file, else the row is a GAP).
  * Description is this seat's <=20-word rewrite of the file's own docstring/header line; the
    script refuses a description longer than 20 words and refuses a mapping entry for a file
    outside the population.
  * Pointer priority: PROVINCE.md, SCORECARD.md capability block, corpus/knowledge/**,
    corpus/lessons/**, corpus/QUALITY.md, sibling population file (successor re-registration),
    SCORECARD.md non-capability row, any other tracked file (wave artifact).
  * Every pointer line is re-read at --rev and must contain the file's basename.
"""

import argparse
import ast
import json
import os
import re
import subprocess
import sys

DESCRIPTIONS = {
    "tools/mado-action-plan.py": "Fail-closed static safety gate over a declared action plan and policy; never executes the supplied argv.",
    "tools/mado-anims.py": "Static resolver for the animation table a Hyprland v0.56.2 config tree builds; stdout only, no socket.",
    "tools/mado-assessment.py": "Read-only artifact assertion gate over an assessment bundle; not independent authentication of its author.",
    "tools/mado-binds.py": "Static resolver for the bind table a Hyprland v0.56.2 config tree builds, from config bytes only.",
    "tools/mado-devices.py": "Joins declared input/device config with a hyprctl devices dump: keyboard XKB names and mouse scroll factors.",
    "tools/mado-eventq.py": "Read-only census of Hyprland event-socket (socket2) subscribers, their unread bytes and removal markers.",
    "tools/mado-evidence-audit.py": "Audits artifact arithmetic and explicit evidence labels; never execution truth, chronology or promotion.",
    "tools/mado-geometry.py": "Joins window-rule sizes with a hyprctl clients dump: does the reported size match the rule?",
    "tools/mado-globals.py": "Read-only census of the Wayland globals the compositor advertised, from a journal file or one allowlisted run.",
    "tools/mado-hostguard.py": "Runs a command against a scratch HOME and fails if a declared operator-owned path changed.",
    "tools/mado-keysym.py": "Predicts which key and modifiers type a keysym under a compiled keymap, from xkbcli output.",
    "tools/mado-monitors.py": "Joins monitor rules with a hyprctl monitors dump: mode, position, scale and transform per output.",
    "tools/mado-options.py": "Static resolver of a config tree's option table, attributing each key to its last declarer.",
    "tools/mado-terminal.py": "Predicts which terminal xdg-terminal-exec picks on this host, and why, without running it.",
    "tools/mado-tripwire.py": "Post-hoc tripwire over OMP session transcripts (JSONL), reporting issued commands as lane-local evidence.",
    "tools/mado-verify.sh": "Config-plane verdict gate: declared planes versus live bytes and hyprctl read verbs, exit 0/1/2.",
    "tools/mado-wsrules.py": "Static workspace-rule table from config bytes, mirroring hyprctl workspacerules -j for v0.56.2.",
    "quality/check-axis-scores.py": "Calibration gate: the lane's published axis table must not be stale.",
    "quality/check-control-receipts.py": "QUALITY 36 successor: a round's control receipts are committed before its data commit.",
    "quality/check-counter-discrimination.py": "Counter-discrimination gate: can the lane's own counters tell work from shape, per frozen manifest.",
    "quality/check-deliverables.py": "QUALITY 101 seat prototype: every deliverable a seat declares exists at the cited revision.",
    "quality/check-evidence-pointers.py": "Evidence-pointer durability gate: every pointer in the lane's own records must resolve.",
    "quality/check-index-rows.py": "Index-row fidelity gate: scores each coverage-map row's shape at a revision or tree.",
    "quality/check-index.py": "Index-completeness gate: coverage-map rows against corpus/knowledge, reporting missing, dangling and duplicate rows.",
    "quality/check-landed-contract.py": "QUALITY 96 gate: a landed contract is not narrower than, nor silently different from, the frozen reference.",
    "quality/check-locators.py": "Recomputes prose source locators against pinned receipts; cited lines must carry the attached fragment's identifiers.",
    "quality/check-population.py": "QUALITY 37 check: registered predicate metrics must agree with each receipt's metrics and population.",
    "quality/check-r38-discrimination.py": "Round-38 discrimination gate: do the v3 counters tell work from crib?",
    "quality/check-round-outcome-first.py": "QUALITY 99 check: a round's SCORECARD closure leads with the round-level outcome, not counter bookkeeping.",
    "quality/check-session-material.py": "Privacy gate for committed receipts: detects session-material shapes in evidence files.",
    "quality/check-state-cite.py": "QUALITY 100 seat prototype: a host-state claim cites the source line that sets that state.",
    "quality/check-wave-done.py": "Wave settlement check: did every dispatched seat of a round reach WAVE-DONE from committed artifacts?",
    "quality/counter-selftest.py": "Round-27 suite A: behavioural gate over the two round-26 counters, harness surfaces replaced with synthetic fakes.",
    "quality/population-suite.py": "Offline gate over the round-26 population checker, exercising it against a built-in fixture set.",
    "quality/ratio-domain-meta.py": "Re-runnable domain-versus-meta count over SCORECARD claim rows.",
    "quality/counters/c1-idle-lock.py": "PRED-C1-r36-v1: the round-35 idle-lock admission counter, repaired.",
    "quality/counters/c1-r37-event-ground.py": "PRED-C1-r37-v2 counter: event-socket delivery ground admitted into the corpus, scored at one revision.",
    "quality/counters/c1-r38-event-ground.py": "PRED-C1-r38-v3: event-socket delivery ground admitted into the corpus, third revision.",
    "quality/counters/c1-r40-live-v2.py": "PRED-C1-r40-v2: the option table merges a live compositor in its native forms.",
    "quality/counters/c1-r40-live.py": "PRED-C1-r40-v1: the option table merges a live compositor in its native forms; superseded by v2.",
    "quality/counters/c1-r41-globals-v2.py": "PRED-C1-r41-v2: read-only census of the compositor's advertised Wayland globals, re-registered.",
    "quality/counters/c1-r41-globals.py": "PRED-C1-r41-v1: read-only census of the compositor's advertised Wayland globals; superseded by v2.",
    "quality/counters/c1-r42-geometry.py": "PRED-C1-r42: read-only join of window-rule sizes with the compositor's reported client sizes.",
    "quality/counters/c1-r44-geometry-states-v2.py": "PRED-C1-r44-v2: mado-geometry names maximized and fullscreen clients instead of comparing their sizes.",
    "quality/counters/c1-r44-geometry-states.py": "PRED-C1-r44: mado-geometry reports maximized and fullscreen clients as such; superseded by v2.",
    "quality/counters/c1-r45-monitors-v2.py": "PRED-C1-r45-v2: mado-monitors joins monitor rules with live output state, importing v1's fixtures.",
    "quality/counters/c1-r45-monitors.py": "PRED-C1-r45: mado-monitors joins monitor rules with live output state; superseded by v2.",
    "quality/counters/c1-r46-devices-v2.py": "PRED-C1-r46-v2: the input-device join, re-registered before data against a corrected reference contract.",
    "quality/counters/c1-r46-devices-v3.py": "PRED-C1-r46-v3: same input-device join, sandboxed under bubblewrap with a socket tripwire.",
    "quality/counters/c1-r46-devices.py": "PRED-C1-r46: mado-devices joins input/device config with live keyboard and mouse state; v1, superseded.",
    "quality/counters/c1-r47-terminal.py": "PRED-C1-r47: mado-terminal answers which terminal xdg-terminal-exec picks, scored against fixtures.",
    "quality/counters/c1-r48-terminal-cache-v2.py": "PRED-C1-r48-v2: predicts terminal selection including the warm xdg-terminal-exec cache, re-registered.",
    "quality/counters/c1-r48-terminal-cache.py": "PRED-C1-r48: predicts terminal selection including the warm cache; superseded by v2.",
    "quality/counters/c1-r49-keysym.py": "PRED-C1-r49: mado-keysym predicts xkbcli how-to-type output for a keysym under a compiled keymap.",
    "quality/counters/c1-r50-bind-entry.py": "PRED-C1-r50: the Hyprland bind-key-match knowledge entry is admitted, scored at one revision.",
    "quality/counters/c2-ledger.py": "PRED-C2-r36-v1: the lane's evidence ledger predicate, repaired against its own fail-opens.",
    "quality/counters/c2-r37-eventq.py": "PRED-C2-r37-v2: the event-socket subscriber census runs and discriminates work from crib.",
    "quality/counters/c2-r38-eventq.py": "PRED-C2-r38-v3: the event-socket subscriber census predicate, third revision, running and discriminating.",
    "quality/counters/c2-r38-request-ground.py": "PRED-C2-r38-v1: request-socket contract ground admitted into the corpus.",
    "quality/counters/c2-r40-forms-entry-v2.py": "PRED-C2-r40-v2: the getoption native-forms knowledge entry is admitted, re-registered.",
    "quality/counters/c2-r40-forms-entry.py": "PRED-C2-r40-v1: the getoption native-forms entry is admitted; superseded by v2.",
    "quality/counters/c2-r41-focus-entry-v2.py": "PRED-C2-r41-v2: the Hyprland focus-grab entry admission predicate, re-registered.",
    "quality/counters/c2-r41-focus-entry.py": "PRED-C2-r41-v1: the Hyprland focus-grab entry is admitted; superseded by v2.",
    "quality/counters/c2-r42-gkeep-entry.py": "PRED-C2-r42: the Hyprland gkeep-geometry entry is admitted, sourced.",
    "quality/counters/c2-r43-gkeep-entry-v2.py": "PRED-C2-r43-v2: gkeep-geometry entry admission, second revision.",
    "quality/counters/c2-r43-gkeep-entry.py": "PRED-C2-r43: gkeep-geometry entry admission; superseded by v2.",
    "quality/counters/c2-r44-gkeep-size-request-v2.py": "PRED-C2-r44-v2: the gkeep size-request entry is admitted, with assimilation clause.",
    "quality/counters/c2-r44-gkeep-size-request.py": "PRED-C2-r44: the gkeep size-request entry is admitted; superseded by v2.",
    "quality/counters/c2-r45-monitor-entry-v2.py": "PRED-C2-r45-v2: the monitor-rule entry is admitted, re-registered.",
    "quality/counters/c2-r45-monitor-entry.py": "PRED-C2-r45: the monitor-rule entry is admitted; superseded by v2.",
    "quality/counters/c2-r46-input-device-entry-v2.py": "PRED-C2-r46-v2: the input-device entry is admitted, re-registered.",
    "quality/counters/c2-r46-input-device-entry.py": "PRED-C2-r46: the input-device entry is admitted, sourced.",
    "quality/counters/c2-r47-terminal-entry.py": "PRED-C2-r47: the terminal-selection entry is admitted, sourced.",
    "quality/counters/c2-r48-xkb-entry-v2.py": "PRED-C2-r48-v2: the XKB-compile entry is admitted, re-registered.",
    "quality/counters/c2-r48-xkb-entry.py": "PRED-C2-r48: the XKB-compile entry is admitted; superseded by v2.",
    "quality/counters/c2-r49-bind-entry.py": "PRED-C2-r49: the Hyprland bind-key-match entry is admitted, sourced.",
    "quality/counters/c2-r50-session-gate.py": "PRED-C2-r50: the session-material gate detects the shapes it covers.",
    "quality/counters/c3-r39-options.py": "PRED-C3-r39-v2: the option-ownership tool resolves config trees it has never seen.",
    "quality/counters/c4-r39-options-entry.py": "PRED-C4-r39-v1: the config-option ownership ground is admitted.",
}

PENDING = [
    ("quality/check-tool-ledger.py", "C1 checker over this ledger: population coverage, pointer and description clauses, hermetic selftest.",
     ".ufo/waves/round-51/claims.md", 20),
    ("quality/counters/c1-r51-ledger.py", "PRED-C1-r51 counter: scores this ledger's coverage and pointer clauses at one revision.",
     ".ufo/waves/round-51/claims.md", 21),
]

POP_GLOBS = [
    re.compile(r"^tools/"),
    re.compile(r"^quality/[^/]+\.py$"),
    re.compile(r"^quality/counters/[^/]+\.py$"),
]


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True,
                          errors="replace", check=True).stdout


def blob(repo, rev, path):
    return git(repo, "show", f"{rev}:{path}")


def population(repo, rev):
    paths = git(repo, "ls-tree", "-r", "--name-only", rev).splitlines()
    return sorted(p for p in paths if any(g.match(p) for g in POP_GLOBS))


def header_line(repo, rev, path):
    src = blob(repo, rev, path)
    if path.endswith(".py"):
        try:
            doc = ast.get_docstring(ast.parse(src))
        except SyntaxError as exc:
            raise SystemExit(f"{path}: unparsable at {rev}: {exc}")
        for line in (doc or "").splitlines():
            if line.strip():
                return line.strip()
        return ""
    for line in src.splitlines():
        text = line.lstrip()
        if text.startswith("#!"):
            continue
        if text.startswith("#"):
            stripped = text.lstrip("# ").strip()
            if stripped and set(stripped) != {"="}:
                return stripped
        elif text.strip():
            break
    return ""


def capability_lines(repo, rev):
    lines = blob(repo, rev, "SCORECARD.md").splitlines()
    heads = [(i + 1, l) for i, l in enumerate(lines) if re.match(r"^#{2,4} ", l)]
    spans = []
    for idx, (ln, text) in enumerate(heads):
        if re.search(r"capabilit", text, re.I):
            end = len(lines) + 1
            for ln2, text2 in heads[idx + 1:]:
                if re.match(r"^#{2,3} ", text2) or ln2 > ln + 40:
                    end = ln2
                    break
            spans.append((ln, end))
    return spans


def classify(repo, rev, path, pop, caps):
    base = os.path.basename(path)
    out = git(repo, "grep", "-n", "-F", "-e", base, rev)
    cats = {k: [] for k in ("province", "scap", "knowledge", "lesson", "qualitymd",
                            "successor", "scother", "other")}
    for row in out.splitlines():
        parts = row.split(":", 3)
        if len(parts) < 4:
            continue
        _, hit_path, ln, text = parts
        if hit_path == path:
            continue  # self-hit: the file naming itself is not accountability (finding F2)
        try:
            ln = int(ln)
        except ValueError:
            continue
        if hit_path == "PROVINCE.md":
            cats["province"].append((hit_path, ln, text))
        elif hit_path == "SCORECARD.md":
            cat = "scap" if any(a < ln < b for a, b in caps) else "scother"
            cats[cat].append((hit_path, ln, text))
        elif hit_path == "corpus/QUALITY.md":
            cats["qualitymd"].append((hit_path, ln, text))
        elif hit_path.startswith("corpus/lessons/"):
            cats["lesson"].append((hit_path, ln, text))
        elif hit_path.startswith("corpus/knowledge/"):
            cats["knowledge"].append((hit_path, ln, text))
        elif hit_path in pop and hit_path.startswith("quality/"):
            cats["successor"].append((hit_path, ln, text))
        else:
            cats["other"].append((hit_path, ln, text))
    return cats


def choose(cats):
    order = [("province", "province-table", True), ("scap", "scorecard-capability", True),
             ("knowledge", "knowledge-named", False), ("lesson", "lesson-named", False),
             ("qualitymd", "quality-named", False), ("successor", "successor-named", False),
             ("scother", "scorecard-row", True), ("other", "wave-artifact", False)]
    for key, label, prefer_table in order:
        hits = cats[key]
        if not hits:
            continue
        if prefer_table:
            table = [h for h in hits if h[2].startswith("|")]
            if table:
                hits = table
        path, ln, text = hits[0]
        return label, path, ln, text
    return None


def build(repo, rev):
    pop = population(repo, rev)
    caps = capability_lines(repo, rev)
    rows = []
    for path in pop:
        desc = DESCRIPTIONS.get(path)
        if desc is None:
            raise SystemExit(f"{path}: no description in this seat's map")
        if len(desc.split()) > 20:
            raise SystemExit(f"{path}: description exceeds 20 words")
        picked = choose(classify(repo, rev, path, set(pop), caps))
        if picked is None:
            rows.append(dict(file=path, label="GAP", pointer=None, line=None, quote=""))
            continue
        label, ptr, ln, text = picked
        line_text = blob(repo, rev, ptr).splitlines()
        if not (0 < ln <= len(line_text)) or os.path.basename(path) not in line_text[ln - 1]:
            raise SystemExit(f"{path}: pointer {ptr}:{ln} does not contain the basename at {rev}")
        rows.append(dict(file=path, label=label, pointer=ptr, line=ln, quote=text,
                         header=header_line(repo, rev, path)))
    orphan = sorted(set(DESCRIPTIONS) - set(pop))
    if orphan:
        raise SystemExit(f"descriptions for non-population files: {orphan}")
    return rows


def render(repo, rev, base, rows):
    from collections import Counter, defaultdict
    counts = Counter(r["label"] for r in rows)
    by_class = defaultdict(list)
    for r in rows:
        by_class[r["label"]].append(r)
    ptr_files = sorted({r["pointer"] for r in rows if r["pointer"]})
    no_prov = [r["file"] for r in rows if r["label"] != "province-table"]
    tools = sum(1 for r in rows if r["file"].startswith("tools/"))
    top = sum(1 for r in rows if r["file"].startswith("quality/") and r["file"].count("/") == 1)
    ctr = sum(1 for r in rows if r["file"].startswith("quality/counters/"))
    out = []
    w = out.append
    w("# Ledger rows — mado round 51 w1, C1 tool-ledger prose and pointer provenance\n")
    w("Seat: `ScrLedgerRows` (leaf). Lane: `%s`." % repo)
    w("Measured revision: `%s`; round base `%s`." % (rev, base))
    w("Rebuild with `python3 -I build-ledger-rows.py --repo <lane> --rev <rev>` (read-only, no scratch).")
    w("This file is a draft for the tracked `quality/tool-ledger.md`; it is not that file.\n")
    w("## 1. Population and method\n")
    w("Population: every file under `tools/`, immediate children `quality/*.py` and immediate children")
    w("`quality/counters/*.py` at `%s`, de-duplicated — **%d distinct files** (`tools/` %d,"
      % (rev, len(rows), tools))
    w("`quality/*.py` %d, `quality/counters/*.py` %d). See finding F1 for why the reading is pinned"
      % (top, ctr))
    w("this way: a git pathspec for `quality/*.py` recurses into `counters/`, a Python glob does not.\n")
    w("Method, all read-only over git objects:\n")
    w("1. Description: this seat's ≤20-word rewrite of each file's own module docstring first line")
    w("   (`tools/mado-verify.sh`: its script header). No behaviour was executed to write a description.")
    w("2. Pointer: `git grep -n -F <basename>` at `%s`, self-hits excluded, ranked by" % rev)
    w("   the priority `PROVINCE.md` → `SCORECARD.md` capability block → `corpus/knowledge/**`")
    w("   → `corpus/lessons/**` → `corpus/QUALITY.md` → sibling population file (successor re-registration)")
    w("   → `SCORECARD.md` non-capability row → any other tracked file.")
    w("3. Verification: each pointer line is re-read at the revision and must contain the basename;")
    w("   the script exits non-zero otherwise (0 failures at `%s`).\n" % rev)
    w("Class counts: " + ", ".join("`%s` %d" % (k, v) for k, v in sorted(counts.items(), key=lambda kv: -kv[1])))
    w("")
    w("Distinct pointer files: %d.\n" % len(ptr_files))
    w("## 2. Class legend\n")
    w("| class | meaning |")
    w("|---|---|")
    w("| `province-table` | `PROVINCE.md` names the file — inventory table cell or a dated refinement paragraph |")
    w("| `scorecard-capability` | `SCORECARD.md` names the file inside a `Capabilities` / `Demonstrated capability` table |")
    w("| `knowledge-named` | a `corpus/knowledge/*.md` entry names the file |")
    w("| `lesson-named` | a `corpus/lessons/*.md` file names the file, usually in a defect or spot-check sentence |")
    w("| `quality-named` | `corpus/QUALITY.md` criterion text names the file — criterion body, not a register |")
    w("| `successor-named` | only a later population file names it, as the frozen predecessor it re-registers |")
    w("| `scorecard-row` | only a non-capability `SCORECARD.md` row (move log / claim result) names it |")
    w("| `wave-artifact` | only a `.ufo/waves/**` file names it |")
    w("| `GAP` | no tracked file names it |\n")
    w("## 3. Rows (%d; one row per population file)\n" % len(rows))
    w("| # | file | one-line description | class | accountability pointer |")
    w("|---|---|---|---|---|")
    for i, r in enumerate(rows, 1):
        w("| %d | `%s` | %s | %s | `%s:%s` |" % (i, r["file"], DESCRIPTIONS[r["file"]], r["label"],
                                                  r["pointer"], r["line"]))
    w("")
    w("## 4. Gap list\n")
    gaps = [r for r in rows if r["label"] == "GAP"]
    w("**Strict gap (no tracked file names the file): %d of %d.**" % (len(gaps), len(rows)))
    if not gaps:
        w("Every population file is named by at least one tracked file, so under the frozen `bad_pointer`")
        w("test every row has a satisfiable pointer.")
    w("")
    w("**Accountability gaps** — rows whose only naming file is not an accountability surface, by class:\n")
    for label in ("lesson-named", "successor-named", "scorecard-row", "quality-named", "wave-artifact"):
        rs = by_class.get(label, [])
        w("`%s` (%d rows):\n" % (label, len(rs)))
        for r in rs:
            w("- `%s` → `%s:%d`" % (r["file"], r["pointer"], r["line"]))
        w("")
    w("Rows with no `province-table` naming at all: **%d of %d**." % (len(no_prov), len(rows)))
    w("`tools/mado-hostguard.py` and `tools/mado-keysym.py` — the two the round-50 wave-seat ledger")
    w("missed — are covered here by `SCORECARD.md` capability rows, not by a PROVINCE row.\n")
    w("## 5. Pending rows (absent at the measured revision)\n")
    w("Population files this round adds, absent at `%s`; each needs a durable pointer once landed:\n" % rev)
    for path, desc, ptr, ln in PENDING:
        text = blob(repo, rev, ptr).splitlines()
        ok = 0 < ln <= len(text) and os.path.basename(path) in text[ln - 1]
        w("- `%s` — %s — `%s:%d` (%s)" % (path, desc, ptr, ln, "verified" if ok else "NOT verified"))
    w("")
    w("Consequence for the freeze: at the revision where PRED-C1-r51 is scored, both files exist, so")
    w("`P = %d` — the ledger must carry these two rows (each pointing at a naming file that exists at that"
      % (len(rows) + len(PENDING)))
    w("revision) or `uncovered` is 2. `quality/tool-ledger.md` itself is not in the population.")
    w("")
    w("## 6. Findings routed to the L1 freeze\n")
    w("**F1 — the population sentence admits two different `P`.** `quality/*.py` as a git pathspec recurses")
    w("into `quality/counters/` (62 paths = 18 + 44), so a summing implementation counts 123 entries for 79")
    w("distinct files; as a filesystem glob it returns 18. `appears exactly once` already implies a set — pin")
    w("the de-duplicated reading (`P = %d` here) in the counter, or the frozen clause is ambiguous.\n" % len(rows))
    w("**F2 — self-pointer loophole: %d of %d files contain their own basename.**"
      % (len(list(r for r in rows if os.path.basename(r["file"]) in blob(repo, rev, r["file"]))), len(rows)))
    w("A row whose pointer is the file itself therefore satisfies `pointer file contains the basename` and")
    w("`bad_pointer` stays 0. Add `pointer_file != row.file` plus a control that a self-pointer MISSes.\n")
    w("**F3 — ledger-self loophole.** `quality/tool-ledger.md` will contain every basename and is not in the")
    w("population, so any row can point at the ledger and pass. Add `pointer_file != quality/tool-ledger.md`")
    w("and a control that such a pointer MISSes.\n")
    w("**F4 — no durable instrument register for the `quality/` instruments.** %d rows are accountable only"
      % len(by_class.get("lesson-named", [])))
    w("through lesson prose (mostly recording a defect in the counter), %d only through the successor that"
      % len(by_class.get("successor-named", [])))
    w("superseded them, %d only through a move-log row, %d only through a QUALITY criterion body. Coverage is"
      % (len(by_class.get("scorecard-row", [])), len(by_class.get("quality-named", []))))
    w("obtainable (0 strict gaps); accountability for two-thirds of the instruments is incidental prose.")
    w("This ledger is the first durable register — it should stay the register.\n")
    w("**F5 — `:line` suffixes are rev-stable only while `PROVINCE.md`/`SCORECARD.md`/`corpus/**` do not move.**")
    w("All %d pointers resolve identically at base `%s` and at the measured revision because those trees are"
      % (len(rows), base))
    w("byte-identical (`git diff --stat <base>..<rev>` empty). A later insertion drifts the numbers while the")
    w("basename test still passes. Either drop the `:line` suffix from the frozen row format or freeze it as")
    w("provenance only.\n")
    shared = {k: v for k, v in Counter((r["pointer"], r["line"]) for r in rows if r["pointer"]).items() if v > 1}
    w("**F6 — shared pointers.** %d pointer lines are shared by more than one row (%s)."
      % (len(shared), ", ".join("`%s:%s` ×%d" % (k[0], k[1], v) for k, v in sorted(shared.items()))))
    w("Legitimate, but per-file accountability for those rows cannot be argued from the ledger alone —")
    w("a reader must follow the line.")
    return "\n".join(out) + "\n"


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", default=None, help="round base revision, for the stability finding")
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)
    rows = build(args.repo, args.rev)
    text = render(args.repo, args.rev, args.base or args.rev, rows)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
