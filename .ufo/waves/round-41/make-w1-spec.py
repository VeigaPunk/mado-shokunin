#!/usr/bin/env python3
"""Generates .ufo/waves/round-41/w1-spec.json (34 seats, v1 wave: build + first falsifiers).

Run: python3 make-w1-spec.py  (writes next to itself, lane-relative reportDir).
"""
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
W = LANE + "/.ufo/waves/round-41"
FREEZE = "60c3914154333180450d5da27ba222d5763cc56a"
BASE = "ab2bfaab661c846d1de9d58c01651cd156a13949"
PKG = "/home/vgpnk/Projects/shokuknow/merge/mado"
GODSPEED = (
    "/skill:godspeed\n\nYou are a Godspeed-enabled subagent.\n\n"
    "1. **Name the axes.**\n2. **Iterate cheap, in parallel.**\n"
    "3. **Keep moves that improve any axis and harm none.**\n"
    "4. **Don't aim \u2014 let the frontier walk itself.**\n\n"
    "## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls "
    "concurrently in large batches. Do not serialize what can run in "
    "parallel. Do not output philosophical reasoning or verbose plans. Act "
    "directly via tool calls.\n\n")

CONTEXT = """# Goal
mado round 41 (hyaku run 7, 2026-10-25), inline v1 wave w1 of two (34 seats: build + first falsifiers). Lane repo: %(L)s
Claims are FROZEN at %(W)s/registration.md (freeze commit %(F)s, base %(B)s) - read it first. Two claims:
- C1 operability (capability acquisition): a new tool `tools/mado-globals.py` - read-only census of the Wayland globals the compositor
  advertised to its desktop portal (xdg-desktop-portal-hyprland), parsed from the user journal
  (`journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso`): sessions, per-global version/count, a fixed class
  decision table, `--diff`, `--expect NAME`, `--live` (one allowlisted program, exact argv, bounded output), `--selftest`.
  Frozen counter quality/counters/c1-r41-globals.py (PRED-C1-r41-v1; its docstring IS the tool's contract): target fixtures=24/24
  TARGET_MET; base 0/24 (tool absent). Reference control (NOT deliverable): %(W)s/c1/ctl-ref-tool.py.txt (24/24 MET, selftest 47/47).
  Controls: %(W)s/ctl/run-c1-controls.py (47 controls, receipt %(W)s/receipts/ctl-c1.txt 47/47).
- C2 coverage (sourced): corpus/knowledge/hyprland-focus-grab-r41.md - the Hyprland focus-grab protocol as a focus-control surface: the
  compositor-side semantics, its advertisement on this host (own-work journal census), a real client's grab lifecycle, the rule-level
  counterpart. Frozen counter quality/counters/c2-r41-focus-entry.py (PRED-C2-r41-v1, clauses a-i); target admitted=1/1; base 0/1.
  Controls: %(W)s/ctl/run-c2-controls.py (41 controls, receipt %(W)s/receipts/ctl-c2.txt 41/41).
Pre-fetched source receipts (the L1 fetched them 2026-10-25; each seat re-opens what it relies on) in %(W)s/fetch/:
  focus-grab-v1.xml, input-capture-v1.xml, protocols-README.md (hyprwm/hyprland-protocols @ cd1aba6bd78775825eb230b3a4274c48b6705eb7),
  quickshell-grab.cpp (quickshell-mirror/quickshell @ 9b0f339b19057f4731bf3b48293307d7ef241671 src/wayland/hyprland/focus_grab/grab.cpp),
  xdph-PortalManager.cpp (hyprwm/xdg-desktop-portal-hyprland tag v1.4.1 src/core/PortalManager.cpp), Hyprland-FocusGrab.cpp/.hpp
  (hyprwm/Hyprland @ efb50993780079460b0cbed1363e2166a2de1d9f src/protocols/), issue-565.html (github.com/hyprwm/Hyprland/issues/565),
  xdph-journal.txt (own work: `journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso`, 153 lines, sha256
  bf8fa91a321197277cf9c1260d17524e9ddf862f7f76ddf440fc057aa600aaf7: 2 sessions, 78 adverts, 63 distinct globals in the latest session,
  one advert of hyprland_focus_grab_manager_v1 (ver 1) at 2026-10-25T13:36:24-03:00 pid 1952).
Provisional facts (from the L1; every seat re-derives what it relies on, none is evidence until re-opened):
- host Hyprland 0.56.2 (commit efb50993780079460b0cbed1363e2166a2de1d9f); installed xdph v1.4.1 (held row S037); the lane's
  registry tops at S282 (219 rows); new rows continue at S283 (append-only, 11-column schema, status `mined`, opened 2026-10-25).
- the lane holds NO focus-grab knowledge at base (grep for focus_grab / focus-grab / focus grab over corpus, PROVINCE.md, SKILL.md, tools is empty).
- PROVINCE.md lines ~68-80 exclude localized (Chinese/Japanese) documentation-channel material: the staged
  `focus-control-surfaces-r28` section 3 (Japanese blog, amgsk.dev) is out of province; the entry must not cite it.
- the staged package is %(P)s (READ-ONLY; never run a campaign tool there; read bytes only).
# Write scope and safety
- Write ONLY inside %(L)s. NEVER write/edit the fleet repo (/home/vgpnk/Projects/shokunin except as your task names), sibling lanes,
  templates/, scripts/, MANIFEST.json, .ufo/state/, .ufo/watchdog.log, .scratch/, the shokuknow checkout, or the lane's jj/git index.
  Never run mutating git/jj anywhere in the lane or the fleet (no add/commit/push/checkout/reset/stash/describe/bookmark). Read-only git
  (log/show/diff/status/rev-parse/ls-tree/cat-file) is fine.
- Write ONLY to your own seat directory %(W)s/w1/<YourSeatName>/ (create it), plus any explicit destination your task names. Never edit an
  existing tracked file (the counters, controls, registration, reference, fetch receipts are FROZEN); the L1 is the only integrator.
  Write your Report file FIRST (a short status), then refine it; a seat that dies without a report is a dead seat.
- Every `Report:` trailer path is relative to %(L)s - write it at %(L)s/<that path>.
- Host safety: pacman is PAUSED host-wide - never run pacman or any package transaction. No host-service or compositor mutation, no input
  injection, no Wayland-client or compositor-socket connection of your own (so no wayland-info, no hyprctl except `hyprctl version`). The
  ONLY journal verb allowed is read-only `journalctl --user -u <unit> --no-pager -o short-iso [-b N | --list-boots]`; no `journalctl --vacuum`/`--rotate`/`--flush`.
  Host config trees and binaries are READ-ONLY.
- Git fixtures (run-6 incident): any fixture repo is `D=$(mktemp -d) && git -C "$D" init -q`, every later git call names `-C "$D"`, and
  `git -C "$D" rev-parse --show-toplevel` must equal `$D` before the first commit; never `git commit` with a throwaway identity anywhere
  else. Use /tmp (mktemp -d) for scratch; clean it up.
- Tooling authorization (operator, 2026-10-19): install tools that help the task (read /home/vgpnk/.omp/agent/RULES.md first; official
  channels only: uv tool / npx / official binaries in ~/.local/bin; never pacman, never -Sy/-Syu/-U/-R). Record tool/version/channel/reason in your report.
- Seat tool state: your tools start at the fleet root, not the lane: use absolute paths everywhere.
- You are a leaf: no subagent dispatch, no background jobs, no spawning (an executor MAY spawn one read-only labrat probe).
- Every finding names what it attacks or supports (a path:line, a command and its output, or a hash). Never fabricate: an unrun check has
  not passed. Quotes lifted from a source are <= 25 words, located (file:line or section), and verified by a script that greps your receipt.
"""


def sub(t):
    for k, v in (("%(L)s", LANE), ("%(W)s", W), ("%(F)s", FREEZE), ("%(B)s", BASE),
                 ("%(P)s", PKG)):
        t = t.replace(k, v)
    return t


CONTEXT = sub(CONTEXT)
items = []


def seat(name, role, target, task):
    items.append({
        "name": name, "role": role,
        "prompt": sub(GODSPEED + "# Target\n" + target.strip() +
                      "\n# Task\n" + task.strip() + "\n")})


# ------------------------------------------------------------ executors (14)
seat("ExecToolIndep", "executor",
     "Differential implementation for C1: an independent tool written from the contract only.",
     """WITHOUT reading %(W)s/c1/ctl-ref-tool.py.txt, read only the docstring of %(L)s/quality/counters/c1-r41-globals.py (the contract) and write your
own `mado-globals.py` in %(W)s/w1/ExecToolIndep/ (stdlib only; selftest k==n>=25 printing `MADO_GLOBALS_SELFTEST: k/n passed`, with teeth: a flipped
comparison in your parser must fail it). Then score it: `cd %(L)s && python3 -I quality/counters/c1-r41-globals.py --repo . --rev %(F)s --tool <your file>`
and report every failing fixture line verbatim (a failing fixture is a finding about the contract text or the counter unless you show your file is wrong).
Then diff your behaviour against the reference on 300 random journals (use the generator functions of the counter by importing it with importlib; the
counter's model_out is the judge) and list every disagreement with the contract sentence that decides it.""")
seat("ExecDiffFuzz", "executor",
     "Differential fuzz of the reference tool against the counter's model.",
     """Import %(L)s/quality/counters/c1-r41-globals.py with importlib (never execute main). Take the committed journal %(W)s/fetch/xdph-journal.txt and the
counter's gen_fixture outputs as seeds; produce >= 3000 mutated journals (byte flips, line deletions/duplications/swaps, CR/LF changes, boot-line
insertions at every position, pid flips, version digits at the 1/6/7-digit boundaries, 127/128/129-char names, invalid UTF-8, a line without trailing newline, a
file of only boot lines, NUL bytes) and run the reference %(W)s/c1/ctl-ref-tool.py.txt (copy it to your seat dir as .py) on each with `python3 -I`, comparing stdout/rc with
`model_out`. Write the harness to %(W)s/w1/ExecDiffFuzz/. Report every disagreement class (minimised input, expected, got) - each is a bug in the tool, the model
or the contract text.""")
seat("ExecLiveHost", "executor",
     "Host receipt for C1: the reference tool's `--live` against the running desktop.",
     """Copy the reference to %(W)s/w1/ExecLiveHost/mado-globals.py. Run `python3 -I mado-globals.py --live --diff` and `--live --expect hyprland_focus_grab_manager_v1
--expect zwlr_virtual_pointer_manager_v1 --expect no_such_global_v9` three times (the third verdict must be MISSING_EXPECTED rc 1), and `--journal-file` on a fresh
`journalctl --user -u xdg-desktop-portal-hyprland --no-pager -o short-iso` capture; compare the three outputs for stability and `--live` against the committed
%(W)s/fetch/xdph-journal.txt (note any drift since the capture: more sessions, more adverts). Save the verbatim outputs, the exit codes, the tool sha256 and the
class table counts to %(W)s/w1/ExecLiveHost/live-census.txt. Also run it with `PATH=/nonexistent` (journalctl not found -> exit 5) and with `--journalctl /bin/true` (exit 0
journal empty -> NO_SESSIONS rc 3).""")
seat("ExecJournalHistory", "executor",
     "Why the first journal session lists only 8 interfaces.",
     """In %(W)s/fetch/xdph-journal.txt session 1 (pid 1918, 2026-10-25T13:16:45) holds 15 adverts / 8 distinct names while session 2 (pid 1952) holds 63. Find out why from
READ-ONLY host evidence: `journalctl --list-boots`, `journalctl --user --disk-usage`, `journalctl --user -u xdg-desktop-portal-hyprland -b -1 --no-pager -o short-iso | wc -l`,
the user journal's retention config (`/etc/systemd/journald.conf*`, read only), the unit's start lines (`-o short-iso` lines of other levels for the same unit, `systemctl --user status
xdg-desktop-portal-hyprland --no-pager` is a read verb and allowed), and xdph's own advert code (%(W)s/fetch/xdph-PortalManager.cpp onGlobal). Decide: truncated by rotation, a
partial registry (portal restarted early), or the portal really bound a smaller registry. State which, with the evidence, and what a reader of the census must NOT conclude
from session 1. Write %(W)s/w1/ExecJournalHistory/finding.md.""")
seat("ExecJournalFormat", "executor",
     "Journal output variants the tool's grammar could misparse.",
     """The tool's ADVERT grammar assumes `-o short-iso` (see the counter docstring). Using read-only `journalctl --user -u xdg-desktop-portal-hyprland` with `-o short`, `-o short-iso`,
`-o short-iso-precise`, `-o short-full`, `-o json`, `-o cat` (only these read verbs) and `-b 0`, `-b -1`, `--since`, `--no-hostname` against the live user journal, record the exact line
shape of one advert and of the boundary lines (`-- Boot ... --`, `-- No entries --`, `-- Journal begins at ...`) for each, `journalctl --version`, and which of them the contract grammar
accepts (run the reference on each capture). Report any shape a user could plausibly pass via `--journal-file` that the grammar silently ignores while the file still holds adverts
(a silent NO_SESSIONS on a non-empty advert file is the failure class). Write %(W)s/w1/ExecJournalFormat/finding.md with the captures (<= 3 lines each).""")
seat("ExecHostFocusGrab", "executor",
     "Which software on this host can bind the focus-grab protocol.",
     """Read-only: scan executables and libraries for the focus-grab protocol name (`hyprland_focus_grab_manager_v1`, `hyprland_focus_grab_v1`, `focus-grab`) with `grep -l -a` (or
`strings`) over /usr/bin, /usr/lib (compiled clients, quickshell/Qt wayland plugins, GTK/layer-shell helpers), ~/.local/bin, ~/.local/share, /opt, and the Omarchy/walker/waybar/mako/
hyprlock/hypridle/vicinae binaries by name (resolve each with `command -v`; `readlink -f`). Report: which files contain the string (path, size, owning package from `pacman -Qo` is
FORBIDDEN - use `file`/`readlink` and the file path only), whether any running process maps a matching file (read `/proc/<pid>/maps` of the host's own processes only, read-only),
and the honest negative if none. State clearly that holding the string is evidence of capability, not of use. Write %(W)s/w1/ExecHostFocusGrab/finding.md.""")
seat("ExecSrcFocusGrab", "executor",
     "Compositor-side facts for the C2 entry: Hyprland's focus-grab implementation.",
     """Read %(W)s/fetch/Hyprland-FocusGrab.cpp, Hyprland-FocusGrab.hpp and focus-grab-v1.xml (re-fetch the three raw URLs yourself, compare sha256 with the receipts). Extract the
protocol's behaviours with located quotes <= 25 words: the interface and request list; what `create_grab`, `add_surface`, `remove_surface`, `commit` and `destroy` do; how the grab whitelist is
stored; what a `commit` with an empty whitelist does; when and why the compositor sends `cleared`; which input (pointer/keyboard/touch) the grab redirects and what happens to focus of
surfaces outside the whitelist; how it interacts with other grabs; the file/line of each. Verify every quote with a script (grep the receipt, print the line number). Write
%(W)s/w1/ExecSrcFocusGrab/facts.md as a table `fact | quote | file:line | sha256 of file`, and list what the source does NOT say.""")
seat("ExecSrcClients", "executor",
     "Client-side and tracker facts for the C2 entry.",
     """Re-fetch and read %(W)s/fetch/quickshell-grab.cpp (a real client's grab lifecycle: sync, cleared handling), xdph-PortalManager.cpp (the portal's registry handler, what it does with
`hyprland_focus_grab_manager_v1`: nothing, or binds?), and issue-565.html (strip the HTML with a script; extract the title, the expected/actual text, the reported config line, the issue state,
the date). Report located quotes <= 25 words with file:line for each (the issue: the text node and its order). State what the portal does NOT do with the focus-grab manager (it only logs the
advert; verify against onGlobal). Write %(W)s/w1/ExecSrcClients/facts.md table `fact | quote | locator | sha256`.""")
seat("ExecSrcProtocols", "executor",
     "Verify the class table names against real protocol definitions.",
     """The counter docstring's class table names 33 globals. For EACH name find the protocol XML that defines the interface (wayland-protocols, wlr-protocols, hyprland-protocols pinned at
cd1aba6bd78775825eb230b3a4274c48b6705eb7, KDE where relevant) by fetching raw files (pin commits via `git ls-remote`), and print `name | defined in (repo@commit:path) | interface line`. Report
any name that does not exist as an interface (a typo in the table = a defect in the frozen predicate; do not fix, report). Also read %(W)s/fetch/protocols-README.md and input-capture-v1.xml and
extract <= 25-word located quotes for what the README says the repository is, and what input-capture grants. Write %(W)s/w1/ExecSrcProtocols/facts.md.""")
seat("ExecAssimIdGuard", "executor",
     "Assimilation id-collision guard (item 10), in scratch, proved on an indented row.",
     """Run the prompt's id-collision procedure verbatim into %(W)s/assimilation/ (the lane-side directory; never into the shokuknow checkout): reg-ids from %(L)s/corpus/SOURCES.md,
staged-ids from %(P)s/SOURCES.append.md with the 0-3 leading-space pattern `^ {0,3}\\|[[:space:]]*S[0-9]{3,}`, `comm -12` -> collisions. PROVE the guard once: build a scratch registry copy with an
indented row `  | S002 |` and show `collisions` is nonempty for it while the column-zero-only pattern is empty. Then: the staged ids that belong to the FOCUS theme (the rows cited by the staged files
focus-control-surfaces-r28, focus-grab-*-r8..r15, privileged-client-surface-r29, compositor-focus-manipulation-literature-r26, wayland-input-security-literature-r8 via their `source:` lines) and the
renumber map by DOCUMENT (URL -> new id S283+), never by arithmetic. Paste both id lists and the collision count. Write %(W)s/assimilation/id-guard.md.""")
seat("ExecQuarantineSlice", "executor",
     "Quarantine slice (item 10) for lane mado, and a hand-check of the focus-theme rows.",
     """Derive the slice exactly as the prompt does (`awk -F'|' -v l='mado' ... absent-defect-register.md`) into %(W)s/assimilation/quarantine-slice (read-only source; every line must
carry an S-id). Report the row count and, for each slice row whose id is cited by a FOCUS-theme staged file, fetch the cited source and locate the quote: present -> adopt with the anchor you
located; absent -> refuse (fabrication class); a prose class cell ("could not be fetched", "named no locator") -> mark `unverifiable` (not fabrication). Verdict per row with the located quote
(<= 25 words) and access date 2026-10-25. Write %(W)s/assimilation/quarantine-verdicts.md.""")
seat("ExecHarmChecks", "executor",
     "Harm baselines at the freeze commit.",
     """In a throwaway checkout (`D=$(mktemp -d)`, `git clone -q %(L)s "$D/lane"`, verify toplevel, checkout %(F)s detached with `git -C "$D/lane" checkout -q %(F)s` - a clone you own, never the lane) run and
capture verbatim: `bash tools/mado-verify.sh --selftest`, `python3 -I tools/mado-options.py --selftest`, `python3 -I quality/check-index.py --rev %(F)s --repo .`, `python3 -I quality/check-index-rows.py`
(read their usage first), `python3 -I quality/check-axis-scores.py --repo . --rev %(F)s`, `python3 -I tools/mado-eventq.py --selftest` if it exists, and `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin mado`. These are the harm baselines the round compares against at the data commit. Write %(W)s/w1/ExecHarmChecks/baseline.md with commands, exit codes and the counted
lines. Clean the clone.""")
seat("ExecC1ExtraMutants", "executor",
     "Extra single-defect mutants of the C1 reference: find the counter's blind spots.",
     """Read %(W)s/ctl/run-c1-controls.py (47 controls) first. Then write >= 25 NEW single-edit mutants of %(W)s/c1/ctl-ref-tool.py.txt that are NOT in that list (e.g. session key uses host not pid,
boot id taken from the wrong line, `latest` is the longest session, class counts include repeats, `first` taken from the last line, count counts distinct only, the --expect names compared case-insensitively,
`MADO_GLOBAL` lines emitted for every session, trailing space in a line, exit code of MISSING_EXPECTED when --diff is given, `--diff` compares first vs last, version compares as strings, 128-char names allowed
but 129 truncated, empty file with --expect gives OK, file read as latin-1, `[LOG]` matched case-insensitively, journalctl env adds HOME, program resolved relative to cwd ...). Score each with
`python3 -I %(L)s/quality/counters/c1-r41-globals.py --repo %(L)s --rev %(F)s --tool <mutant>` (use your own scratch copies) and list every mutant that scores TARGET_MET or fixtures=24/24 (a survivor = a missing
fixture class) with the fixture that would kill it. Equivalent mutants are named as such with a proof. Write %(W)s/w1/ExecC1ExtraMutants/survivors.md and the mutants under your seat dir.""")
seat("ExecC2ExtraMutants", "executor",
     "Extra mutants of the C2 admitted fixture: find the counter's blind spots.",
     """Read %(W)s/ctl/run-c2-controls.py (41 controls) and the docstring of %(L)s/quality/counters/c2-r41-focus-entry.py. Import the control runner's functions (importlib, never run its main) and write >= 20 NEW
mutants of the admitted set G not in that list (e.g. recheck cell prose, 10-cell row, S-id lowercase, id cited twice, two entry lines for one id, quote with different case, quote crossing two lines, GATE line with extra
fields, receipt path with `..`, receipt a symlink-like path, a verified-at in the second 20 lines, source: line after line 20, README row for a different name, an own-work row whose journal is >= thresholds only by
duplicated sessions, a journal with `[LOG] |` single-space lines counted, ADMIT line indented, REFUSE reason of exactly 19/20 characters, an admit naming a path with spaces ...). Score each in a fixture repo built exactly as
`score()` does (D=$(mktemp -d) with -C D) and list every mutant that scores admitted=1/1 (survivor) with the clause that should kill it. Write %(W)s/w1/ExecC2ExtraMutants/survivors.md.""")

# ------------------------------------------------------------ scribes (8)
ENTRY_SHAPE = """Entry shape (follow the lane's existing entries, e.g. %(L)s/corpus/knowledge/hyprctl-getoption-native-forms-r40.md and host-bar-producer-census-r40.md): title; `Lane: mado-shokunin. Round: 41.`;
header lines within the FIRST 20 lines: >= 4 `source: S### - <url or path> - <section> - <pin>` lines, `verified-at: 2026-10-25`, `recheck: 90d - <what to re-pull>` , `ground: <coverage-map pointer>`; sections with
**OBS** (observed, one <= 25-word located quote per cited id, on one line naming the id, e.g. `**OBS** ... (S287):` then `> "quote"` is NOT enough - the id and the quote must be on the SAME line),
**INF** (inference, `Basis:` named) and **UNK** (unknown) tags; one standalone line `journal sessions=2 adverts=78 interfaces=63 focus_grab=1` (outside any fence, exactly once) reporting the own-work journal census. The new
ids are S283.. in the order you cite them (the rows draft by ScrRowsDraft uses the same order: focus-grab-v1.xml S283, Hyprland FocusGrab.cpp S284, quickshell grab.cpp S285, xdph PortalManager.cpp S286, issue #565 S287,
hyprland-protocols README S288, the own-work journal receipt S289 (kind own-work, location .ufo/waves/round-41/fetch/xdph-journal.txt); input-capture-v1.xml S290 only if you cite it). Cite at least one held id if it
fits (S037 xdph release). Never cite the Japanese/Chinese documentation channel (PROVINCE.md). Every quote must be a verbatim <= 25-word substring of the receipt in %(W)s/fetch/ (a script greps it before you write).
Draft to %(W)s/w1/<YourSeatName>/hyprland-focus-grab-r41.md."""
seat("ScrEntryA", "scribe",
     "Draft A of the C2 entry: full scope (protocol, host advertisement, client lifecycle, rule counterpart).",
     ENTRY_SHAPE + """
Scope A: five parts - (1) the protocol's interfaces and requests (xml), (2) the compositor-side semantics (FocusGrab.cpp), (3) the host advertisement (own-work journal; the portal logs but does not use it), (4) a real client's lifecycle
(quickshell), (5) the rule-level counterpart and the tracker evidence (issue #565), plus a decision table `question | where the answer lives | state (OBS/INF/UNK)`.""")
seat("ScrEntryB", "scribe",
     "Draft B of the C2 entry: host-first scope.",
     ENTRY_SHAPE + """
Scope B: lead with the host evidence (what this compositor advertises, the 63-global latest session and the class decision table of the counter docstring as an INF layer: which advertised globals let a client grab focus, synthesize input,
capture input, lock the session - state it as classification of names, not capability proof), then the focus-grab protocol and its client lifecycle, then the rule counterpart. Keep it under 120 lines.""")
seat("ScrEntryC", "scribe",
     "Draft C of the C2 entry: minimal, strictest reading of 'one fact one quote'.",
     ENTRY_SHAPE + """
Scope C: minimal - only facts that survive a hostile quote check: the interface/request names, the compositor's grab/clear behaviour, the advertisement line and census, the portal's handler. No inference beyond one INF per section,
every UNK named. Under 70 lines.""")
seat("ScrRowsDraft", "scribe",
     "Draft the SOURCES.md registry rows for the C2 entry.",
     """Read %(L)s/corpus/SOURCES.md (header, 11-column schema, the last 10 rows S273-S282 for style, and the CORPUS.md SOURCES contract in /home/vgpnk/Projects/shokunin/CORPUS.md section 'SOURCES.md - where a shokunin learns').
Draft rows S283-S290 (ids in the order stated in the entry shape: focus-grab-v1.xml S283, Hyprland FocusGrab.cpp S284, quickshell grab.cpp S285, xdph PortalManager.cpp S286, issue #565 S287, hyprland-protocols README S288, own-work journal
S289, input-capture-v1.xml S290) in exactly the registry's schema: id | `title - <location>` | kind | tier | scope | anchor | teaches | status `mined` | opened `2026-10-25` | recheck (ISO date, `NNd` or `on-*`; NO prose, NO `|`
inside any cell, no escaped pipes) | used-by `corpus/knowledge/hyprland-focus-grab-r41.md`. The location (last whitespace token of cell 1) must be unique in the registry (grep every URL against the current registry first). Also
list the used-by additions for held rows the entry cites (old->new, e.g. S037). Write %(W)s/w1/ScrRowsDraft/rows.md and a `rows-block.txt` containing only the table rows.""")
seat("ScrLessonSkeleton", "scribe",
     "Draft the round-41 lesson skeleton.",
     """Read %(L)s/corpus/lessons/round-40.md (structure) and %(L)s/corpus/lessons/round-40-verifier-spotcheck.md (routed defects). Draft %(W)s/w1/ScrLessonSkeleton/round-41.md with: round intent (registration freeze %(F)s, C1/C2, shape: two v1 waves),
`## Gate` with the GATE-line pattern for ids S283-S290 (placeholders `<sha>` are NOT allowed in the final: write the shape with a comment line outside the section) and the `ADMIT <staged path> as corpus/knowledge/hyprland-focus-grab-r41.md`
and `REFUSE <staged path> reason=<>=20 chars>` lines (refuse candidates: privileged-client-surface-r29.md; focus-control-surfaces-r28.md section 3 Japanese channel), `## Mistakes` with candidate M41 entries (class | evidence pointer |
captured-by | fix) mined from: the round-40 spot-check routed defects (untracked w1.ready.dispatched; tip axis receipt uncommitted; ConnCrossClaim wrote to another round's path M40-6; v1 predicates falsified after seats scored),
and this round's own pre-wave findings (read %(W)s/receipts/*, e.g. M09 mutant equivalent under a redundant dedupe until both edits were made). A fix counts only once shown able to fail - name the control that proves it.""")
seat("ScrSkillProvince", "scribe",
     "SKILL.md and PROVINCE.md row drafts.",
     """Read the shape of %(L)s/SKILL.md (grep -n '^## \\|^### ' first; do not read it whole) and PROVINCE.md. Draft (a) the SKILL.md rows for the new tool: a probe-table row and a decision-table row (command, what it reads, exit map,
sample output from the committed fetch/ journal run through the reference), (b) a PROVINCE.md surface row/paragraph for 'advertised Wayland globals and focus-grab clients' with the scope check (what is in province: the compositor's advertised set
and Hyprland's own protocols; what is adjacency: client applications' use of them, security literature). Write %(W)s/w1/ScrSkillProvince/skill-rows.md and province-row.md with the exact insertion anchors (line numbers of the neighbouring rows).""")
seat("ScrQualityCriteria", "scribe",
     "Draft QUALITY.md criteria 69+ from this round's mistakes.",
     """Read the last 20 lines of %(L)s/corpus/QUALITY.md (criteria 60-68 style: rule, `Check:`, `Shown able to fail:`, `(lesson: lessons/round-N.md#mistakes M..)`) and the pre-wave state in %(W)s/registration.md and %(W)s/receipts/. Draft criteria 69-72
from real, evidenced mistakes (round-40 routed defects: an uncommitted tip receipt; a dispatch marker left untracked; a seat report written under another round; an equivalent mutant created by redundant code), each with a Check command that can
fail and the control or fixture that shows it can (cite the committed control name). No criterion without a mistake behind it. Write %(W)s/w1/ScrQualityCriteria/criteria.md.""")
seat("ScrConsiderthese", "scribe",
     "Mine ONE still-unimplemented considerthese proposal (item 10).",
     """Read %(L)s/considerthese/2026-10-25.md (latest file; its 'Self-improvement suggestions (proposals only)') and the earlier files' proposals; determine which proposals are still unimplemented at the freeze (grep QUALITY.md, SKILL.md, tools/ and
lessons for the implementation; round 40 already mined proposal 2 as a table). Choose ONE not yet implemented, ground it through the lane's bar (the reflection is a pointer, not evidence: open what it points at, e.g. count the commits or
watchdog lines it cites), and draft its landing form: a lesson section, a QUALITY.md criterion or a SOURCES row citing `considerthese/2026-10-25.md` + the date, with the command that reproduces its numbers. Write
%(W)s/w1/ScrConsiderthese/proposal.md (chosen proposal, why, evidence, the exact text to land).""")

# ------------------------------------------------------------ scouts (3)
seat("ScoutPackageFocus", "scout",
     "Survey the staged focus-theme package: verdict per entry.",
     """Read (read-only) %(P)s/MERGE-REPORT.md and the staged files whose names contain focus-grab, focus-control, privileged-client, compositor-focus, wayland-input-security, upstream-input-holds (under %(P)s/knowledge/corpus/knowledge/). Table:
file | claims in one line | cited rows | PROVINCE.md scope (in / adjacency / out: localized-doc channel, generic Wayland security, host-local app geometry) | held already? (grep the lane corpus) | verdict (admit / refuse / hold) with reason. Mark which
entries' measurements depend on `lanes/mado/roundN/fetch/...` private receipts the lane cannot re-open (those cannot be admitted as written). Name the single best admit set for ONE entry. Write %(W)s/w1/ScoutPackageFocus/survey.md.""")
seat("ScoutHeldOverlap", "scout",
     "Held coverage that overlaps the planned focus-grab entry.",
     """grep the lane corpus (corpus/knowledge/*.md, SOURCES.md, lessons, SKILL.md, PROVINCE.md, plans) for: xdg-desktop-portal-hyprland, xdph, 'Got interface', layer-shell, input-capture, xdg_activation, no_focus, no_initial_focus, silent, follow_mouse,
foreign-toplevel, wayland protocol boundaries, security_context. Report what is held (file:line) so the entry adds new ground only and cites held rows where it overlaps; list every statement of the planned entry's topics that the lane already makes (a
contradiction check against the compositor-side source in %(W)s/fetch/Hyprland-FocusGrab.cpp). Write %(W)s/w1/ScoutHeldOverlap/overlap.md.""")
seat("ScoutMergeRest", "scout",
     "Survey the rest of the mado package for the next round.",
     """Read %(P)s/MERGE-REPORT.md and compare with %(L)s/corpus/knowledge/ (what the lane holds after round 40 plus the focus theme of round 41). Group the remaining staged entries by theme (gkeep geometry; idle/lock series; socket client
contract; two-literature/Chinese wiki; uwsm/app lifecycle; weather/update producers; others) with the PROVINCE.md scope verdict per theme in one line each, which staged entries cite private receipts, and the best next theme and why. Write
%(W)s/w1/ScoutMergeRest/themes.md.""")

# ------------------------------------------------------------ connectors (2)
seat("ConnSiblingOverlap", "connector",
     "Sibling-overlap scan (read-only) for the focus-grab and globals ground.",
     """Read-only: scan the OTHER lanes' repos under /home/vgpnk/Projects/shokunin/*-shokunin/ (grep -ril, never edit) for focus-grab, `Got interface`, xdph, wayland global names (`zwlr_virtual_pointer`, `hyprland_input_capture`), and tools that parse
journalctl output. Report overlaps, adjacent claims and any contradiction with the plan in %(W)s/registration.md; say which lane would arbitrate (adjacency axis) and whether C1/C2 duplicate a sibling's held fact. Write %(W)s/w1/ConnSiblingOverlap/overlap.md.""")
seat("ConnCrossClaim", "connector",
     "Cross-claim and cross-source pattern finder.",
     """Check separability of C1 and C2 as registered (no counter reads the other claim's files; the own-work row of C2 is a saved journal parsed by C2's own parser) and find cross-source patterns: the same global named in the journal (own work), the protocol XML,
the compositor source and the client source - which statements agree, which are only implied, where a reader could mistake an advert for a use. List contradictions between the staged package claims and the sources in %(W)s/fetch/. Write
%(W)s/w1/ConnCrossClaim/cross.md (a claims-vs-sources matrix).""")

# ------------------------------------------------------------ reviewers (3)
seat("RevC1Counter", "reviewer",
     "Attack the frozen C1 counter.",
     """Read %(L)s/quality/counters/c1-r41-globals.py end to end and attack it (read-only; build cheats in your seat dir): is the judge's model a faithful transcription of its own docstring (compare each sentence with the code)? Which docstring sentences have NO
fixture that exercises them (list them)? Can a tool read the judge's stub payload without running it, discover the nonce, distinguish file mode from live mode, or detect the sandbox and special-case it? Does the sandbox hide everything the docstring says (check the
binds: scratch, tool dir, mark dir rw)? Is any fixture vacuous (passes for a tool that only prints the model for the first line)? Each finding: severity, the exact line, a reproduction. Write %(W)s/w1/RevC1Counter/findings.md.""")
seat("RevC2Counter", "reviewer",
     "Attack the frozen C2 counter.",
     """Read %(L)s/quality/counters/c2-r41-focus-entry.py end to end against its docstring (clauses a-i) and the control runner %(W)s/ctl/run-c2-controls.py. Which sentence of the docstring has no mutant that kills it? Can a fabricated entry
with real-looking receipts pass (name the cheapest forgery and its size)? Is clause i's localized-channel test a substring heuristic that a rename defeats? Does clause h's own parser agree with the C1 predicate grammar (same regexes)? Findings with severity, line, reproduction. Write
%(W)s/w1/RevC2Counter/findings.md.""")
seat("RevRefTool", "reviewer",
     "Code and safety review of the reference tool.",
     """Read %(W)s/c1/ctl-ref-tool.py.txt (it will likely be the delivered tool): correctness against the counter docstring, the `--live` path (argv, env, stdin, timeout, output cap, program resolution incl. TOCTOU between stat and exec, a PATH entry that is relative or empty, a
symlinked program, a directory named journalctl), parsing edge cases (names that are Python keywords, ver 000001, huge counts), exit codes, stdout vs stderr discipline, behaviour on a FIFO or a directory passed to --journal-file (hang? crash with traceback?), non-UTF-8 paths. Each
finding: severity, line, repro command and output. Write %(W)s/w1/RevRefTool/findings.md.""")

# ------------------------------------------------------------ critics (2)
seat("CritC1Cheat", "critic",
     "Cheat tools against the C1 counter: can TARGET_MET be reached without doing the work?",
     """Write >= 6 cheat tools in %(W)s/w1/CritC1Cheat/ and score each with `python3 -I %(L)s/quality/counters/c1-r41-globals.py --repo %(L)s --rev %(F)s --tool <cheat>`: (1) a tool that finds the stub's base64 payload by reading the stub script (when it is run for --live the real
journalctl stub is on PATH) and prints the model for it; (2) a tool that discovers file-mode vs live-mode and replays previously seen outputs; (3) one that parses the journal with a different session rule that coincides on every fixture; (4) one that shells out via an allowed import
(`subprocess`) to python/awk to do the work in a way clause g does not see; (5) a selftest-echo + minimal parser; (6) a tool that reads the fixture's expected output from a sibling path; (7) anything cleverer you find. Report which scored MET, which fixtures they passed, and the cheapest remedy
for each survivor. Do NOT edit the counter.""")
seat("CritC2Cheat", "critic",
     "Forgeries against the C2 counter.",
     """Build >= 6 fixture repos as `run-c2-controls.py` does (D=$(mktemp -d) with -C D; import its functions, never run main) containing a FABRICATED entry that the counter admits (1/1): invented but self-consistent receipts of >= 512 bytes, an invented journal that parses to the entry's
`journal` line, an ADMIT/REFUSE pair naming files that do not exist, a localized-channel source hidden behind a redirect URL, a quote that is a substring of boilerplate shared by all receipts, a registry row whose location differs by one character from a held row, etc. Report
each forgery, its size in bytes, the clause that should have caught it, and a concrete tightening that does not reject the genuine set (the genuine receipts are in %(W)s/fetch/). Write %(W)s/w1/CritC2Cheat/forgeries.md.""")

# ------------------------------------------------------------ mutation testers (2)
seat("MutC1CounterGates", "mutation-tester",
     "Mutate the C1 counter itself: do the controls notice a regressed counter?",
     """Make >= 15 single-edit mutants of %(L)s/quality/counters/c1-r41-globals.py in your seat dir (drop a clause, loosen a regex, skip the stdin pipe, remove the canary env, skip the marker check, accept rc mismatch, ignore stderr, change TOTAL, drop the sandbox, make
b2 always pass ...). For each, run the control runner %(W)s/ctl/run-c1-controls.py with `--counter <mutant>` (it takes the counter path; use `--only` to restrict to the controls that should react) and report which mutants the controls fail to notice (a counter regression the committed controls cannot see). Write
%(W)s/w1/MutC1CounterGates/matrix.md: mutant | edit | killed by which control | survivor?""")
seat("MutSelftestFixtures", "mutation-tester",
     "Mutation-test the reference tool's selftest and the counter's fixtures together.",
     """Enumerate every comparison, constant and branch of %(W)s/c1/ctl-ref-tool.py.txt (use `ast`), apply each as a single mutant (>= 60 mutants), and run (a) the tool's own `--selftest`, (b) the counter against it. Report mutants that survive BOTH (undetected by selftest and by the 24 fixtures), and mutants killed only by the
selftest or only by the fixtures. For each undetected mutant say whether it is equivalent (proof) or a missing check, and name the assertion or fixture that would kill it. Write %(W)s/w1/MutSelftestFixtures/matrix.md.""")

import collections as _c
assert len(items) == 34, len(items)
print(len(items), dict(_c.Counter(i["role"] for i in items)))
spec = {"wave": "w1", "context": CONTEXT, "reportDir": ".ufo/waves/round-41/w1",
        "items": items}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "w1-spec.json")
with open(out, "w") as fh:
    json.dump(spec, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
