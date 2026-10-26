#!/usr/bin/env python3
"""Generates .ufo/waves/round-47/w2-spec.json (round 47, wave w2 = FALSIFY, policy v1, band 32-64).

Run: python3 make-w2-spec.py. Every item attacks one frozen instrument, draft or routed item of the round and names it.
"""
import collections
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("w1spec", os.path.join(HERE, "make-w1-spec.py"))
_src = open(os.path.join(HERE, "make-w1-spec.py")).read()
SCOPE = _src[_src.index("# Write scope and safety"):_src.index('"""\n\n\ndef sub(t):')]
GODSPEED = _src[_src.index('GODSPEED = (') + len('GODSPEED = ('):_src.index('"directly via tool calls.\\n\\n")')]
GODSPEED = eval("(" + GODSPEED + '"directly via tool calls.\\n\\n")')

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
W = LANE + "/.ufo/waves/round-47"
BASE = "60edb66e2f1cb90acc6e9442fc93ded0ca42d750"
FREEZE = "d7527d608ad2b2e3cc398fdde34db7947b254a1a"
SCR = "/fast/scratch/hyaku/mado-r47"
PKG = "/home/vgpnk/Projects/shokuknow/merge/mado"

CONTEXT = """# Goal
mado round 47 (hyaku run 9, 2026-10-26), wave w2 = FALSIFY (policy v1). Lane repo: %(L)s (desktop and compositor craft; axes coverage +
operability). Wave w1 (41 seats, build) has returned; its seat reports are in %(W)s/w1/. The L1 FROZE both claims at commit %(F)s
(base %(B)s): read %(W)s/registration.md FIRST. No data commit exists yet: tools/mado-terminal.py and
corpus/knowledge/xdg-terminal-selection-r47.md are absent from the lane. Your job is to BREAK what is frozen and what is drafted - a hole
found now re-registers v2 before data; a hole found after data is an honest miss. Report every hole with a reproducible command.
- C1 operability (capability): tools/mado-terminal.py re-implements xdg-terminal-exec v0.14.3's selection (print / explain [--observed] /
  --selftest), no process, no socket. Contract = docstring of the L1 reference %(W)s/l1-draft/mado-terminal.py. Frozen counter
  %(L)s/quality/counters/c1-r47-terminal.py (PRED-C1-r47: clauses a s f x g i r; judge = the REAL pinned script %(W)s/fetch/xdg-terminal-exec,
  sha256 89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac, run in bwrap; fixtures quality/counters/c1-r47-fixtures.json = 190,
  built by %(W)s/ctl/build-fixtures.py; controls %(W)s/ctl/run-c1-controls.py, receipt %(W)s/receipts/ctl-c1.txt).
  Score a candidate tool: `D=$(mktemp -d -p %(S)s/<YourSeatName>); git clone -q --shared --no-checkout %(L)s "$D";
  test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"; git -C "$D" checkout -q --detach %(F)s; cp <candidate> "$D/tools/mado-terminal.py";
  git -C "$D" add tools/mado-terminal.py; git -C "$D" -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m cand;
  mkdir -p %(S)s/<YourSeatName>/w; python3 -I %(L)s/quality/counters/c1-r47-terminal.py --repo "$D" --rev HEAD --work %(S)s/<YourSeatName>/w [--nonce N]`
  (about 70 s and 4-8 cores per run: run at most 2 counts at once). Target fixtures=190/190 explained=190/190 generated=150/150 selftest=ok
  readonly=ok tool=present TARGET_MET; base MISSED.
- C2 coverage (sourced): corpus/knowledge/xdg-terminal-selection-r47.md. Frozen counter %(L)s/quality/counters/c2-r47-terminal-entry.py
  (PRED-C2-r47 clauses a-i; clause f = the selection half of the round-17 [UNK] answered by a committed capture of the resolver with
  `resolver_sha256=`; L1-changed from the w1 draft so it never runs our tool). Controls %(W)s/ctl/c2/ (build-control.py makes an entry-only
  positive tree; needs C2R47_WORK=<scratch> holding pins/xdg-terminal-exec-0.14.3/ = the extracted tag tarball
  https://codeload.github.com/Vladimir-csp/xdg-terminal-exec/tar.gz/refs/tags/v0.14.3, sha256 82ac2dfdb357361d15f5163cdeb3cfd457bbb30bf5d2e14436393f493bd32afe),
  receipts %(W)s/receipts/ctl-c2/. Count: `python3 -I %(L)s/quality/counters/c2-r47-terminal-entry.py --repo <repo> --rev <rev>`.
  The data drafts: entry %(W)s/w1/ScrEntry/entry.md, rows %(W)s/w1/ScrRows/rows.md + %(W)s/w1/ScoutSpecs/, live capture %(W)s/w1/ExecLive/.
- Routed round-46 items drafted in w1: R1 %(W)s/w1/ScrErrataR1/, R2 %(W)s/w1/ExecR2Digest/, R3 %(W)s/w1/ExecSessionMarker/, R4
  %(W)s/w1/ExecSupersede/, %(W)s/w1/ScrErrataR45/, %(W)s/w1/ScrErrataCal/; mistakes %(W)s/w1/ScrMistakes/; tool ledger %(W)s/w1/ScrToolLedger/.
Incidents to respect: a w1 seat (ExecRefB) ran away writing ~590 GB into its scratch - bound every file you write (head -c, timeout) and
NEVER pass an empty argv element to xdg-terminal-exec (its option loop spins forever); a w1 run rewrote the host cache
~/.cache/xdg-terminal-exec - every resolver run sets XDG_CACHE_HOME into your scratch.
""" + SCOPE.replace("w1/<YourSeatName>", "w2/<YourSeatName>")


def sub(t):
    for k, v in (("%(L)s", LANE), ("%(W)s", W), ("%(B)s", BASE), ("%(F)s", FREEZE), ("%(P)s", PKG), ("%(S)s", SCR)):
        t = t.replace(k, v)
    return t


CONTEXT = sub(CONTEXT)
items = []


def seat(name, role, target, task):
    items.append({"name": name, "role": role,
                  "prompt": sub(GODSPEED + "# Target\n" + target.strip() + "\n# Task\n" + task.strip() +
                                "\nWrite your findings to %(W)s/w2/" + name + "/ and your Report file.\n")})


# ---------------------------------------------------------------- C1 instrument attacks
seat("CritC1Cheat", "critic", "PRED-C1-r47 (quality/counters/c1-r47-terminal.py): meet it without implementing the resolver.",
     """Build and score (recipe in context) the cheapest tools you can think of that reach TARGET_MET without modelling the selection:
reading the answer from anything visible inside the sandbox (the case tree, /proc, argv, env, timing, the oracle's leftovers), a lookup
table keyed by the case, detecting fixture ids, etc. For each: the candidate file, the counter summary line, and which clause stopped it
(or that none did - a hole).""")
seat("SentC1Sandbox", "sentinel", "Clause i of PRED-C1-r47: the bwrap allowlist root.",
     """List exactly what a tool sees inside the counter's sandbox (write a probe tool that prints the visible tree, mounts, env, /proc
contents, fds; score it so it runs inside). Is anything of the oracle tree, the pin, the fixtures file, the lane or the host home reachable?
Can the tool write anything that a later run (oracle or tool) reads? Report each leak with the probe output.""")
seat("SentC1Tripwire", "sentinel", "Clause r of PRED-C1-r47: strace around bwrap counts process starts and sockets.",
     """Try to start a process or open a socket from a candidate tool without a trip: vfork/clone3+execve, posix_spawn, io_uring, execveat
via ctypes, a forked child that execs after the parent exits, os.fork + exec from a thread, a socket via ctypes syscall(), socketcall,
memfd + fexecve, `#!` tricks, LD_PRELOAD-like env (bwrap clearenv), signals that kill strace. Score each attempt with the counter and report
trips=N for each. A bypass is a hole.""")
seat("CritC1Explain", "critic", "Clause x of PRED-C1-r47: explain + --observed.",
     """Find tools whose `explain` passes clause x while being wrong or dishonest in a way that matters to an operator (wrong trace,
wrong cache field, AGREE on a capture that differs only in the cmd line, path with ':action', NO_TERMINAL exit codes). Build candidates from
the reference with one change each, score them, report which pass.""")
seat("MutC1Counter", "mutation-tester", "The counter's own code: does each clause fail when it should?",
     """Mutate %(L)s/quality/counters/c1-r47-terminal.py in a scratch copy (never the tracked file; point --repo at a clone): drop the drift
check, compare stdout only, ignore rc, skip variant B, reuse the oracle tree for the tool, drop the explain DIFFER probe, accept a trip, lower
SELFTEST_MIN, parse the selftest line loosely. For each mutant, run the controls runner logic you need (or a subset of the controls) and say
whether some control or reference run reveals it. Mutants no run reveals are holes in the evidence.""")
seat("MutC1Fixtures", "mutation-tester", "Fixture sensitivity: which reference rules do the 190 fixtures + 150 nonce cases miss?",
     """Make >= 20 one-rule mutants of %(W)s/l1-draft/mado-terminal.py beyond the 17 V-* of %(W)s/ctl/run-c1-controls.py (e.g. IFS splitting
of empty fields, read_split for --app-id, tokenizer quoted escapes, de_expand_str unknown escapes, OnlyShowIn empty desktop, NotShowIn, TryExec
absolute path, PATH empty element = cwd, alias of an excluded id, action split first/last colon, print-content of a file without final
newline, --test with print-id, --print-cmd= empty delimiter, \\c in --print-cmd=, the test-mode ordering). Score each (fixed nonce 47).
Survivors = rules the counter does not exercise; for each propose the fixture JSON that would kill it (verify with the real script).""")
seat("ExecC1IndepA", "executor", "Is the C1 contract executable without oral context?",
     """Without reading %(W)s/l1-draft/mado-terminal.py's code (read ONLY its docstring) and without w1 seat files, write your own
tools/mado-terminal.py from the docstring + /usr/bin/xdg-terminal-exec, score it with the frozen counter (recipe), iterate up to 3 times,
report the summary lines and every place the docstring was wrong or insufficient.""")
seat("ExecC1IndepB", "executor", "Second independent rebuild of C1 from the contract.",
     """Same as a sibling seat but independent: do not read other seats' files. Implement from the docstring of %(W)s/l1-draft/mado-terminal.py
and the script only; score with the counter; report docstring errors/omissions with the script lines that show them.""")
seat("ExecC1Nonce", "executor", "Stability of PRED-C1-r47 on the reference.",
     """Install the reference %(W)s/l1-draft/mado-terminal.py in a scratch clone at %(F)s and run the counter with 5 different nonces (2 at a
time max) plus one with the default random nonce; report every summary line, wall time, any FAIL line, and any trip. A reference failure is a
contract error or a flaky judge - find which.""")
seat("ExecC1Determinism", "executor", "Judge determinism: readdir order, filesystem, locale.",
     """Run the counter on the reference twice with the same nonce and with --work on two different filesystems (your /fast scratch and a
tmpfs under /dev/shm/<YourSeatName> - remove it after); also build the fixtures on tmpfs with %(W)s/ctl/build-fixtures.py --out <scratch
file> and diff against quality/counters/c1-r47-fixtures.json. Report any drift and which fixtures depend on readdir order.""")
seat("ExecC1Diff", "executor", "Contract errors: differential fuzz of the reference against the real script.",
     """Extend %(W)s/ctl/l1-fuzz.py (or write your own) to grammar areas it does not cover: symlinked desktop files and dirs, unreadable files
(chmod 000 inside scratch), NUL bytes, CR, very long lines, multiple [Desktop Entry] groups, Exec with every escape, XDG vars with empty
components and trailing slashes, XTE_EXECARG_COMPAT / XTE_CACHE_ENABLED env, --print-content, --test, unknown options. >= 3000 cases,
sandboxed like the counter or with a restricted PATH; report every disagreement as a minimal case + script lines.""")
seat("RevC1Counter", "reviewer", "Code review of quality/counters/c1-r47-terminal.py against registration.md.",
     """Read the counter and %(W)s/registration.md: does the code do what the docstring and the registration say (clause by clause)? Find
mismatches (e.g. what counts as a trip, the drift check placement, variant B construction, cache isolation, stdout decoding, timeouts,
cleanup, --work guards, /tmp use). Each finding with path:line and a repro where possible.""")
seat("RevC1Reference", "reviewer", "The reference vs the script, line by line.",
     """Walk /usr/bin/xdg-terminal-exec from line 1 to 1499 and mark each branch as modelled / declared out of contract / missing in
%(W)s/l1-draft/mado-terminal.py (cite reference lines). Pay attention to IFS leaks, errexit paths, read semantics, the heredoc reads, printf
%%b, the option loop, print-content. List missing branches with a case that shows the difference on the real script.""")
seat("CritC1Contract", "critic", "False sentences in the C1 contract docstring.",
     """Take each sentence of the docstring of %(W)s/l1-draft/mado-terminal.py and test it against the real script with a scratch case. List
sentences that are false or misleading (with the case and both outputs) and those that are untestable.""")
seat("SentC1Host", "sentinel", "Running the tool's explain on this host: is it safe and read-only?",
     """Review %(W)s/l1-draft/mado-terminal.py for host risk when an operator runs `explain` on the real ~/.config and data dirs: symlink
loops, FIFOs as list files (does the tool block on open?), huge files, /proc paths in XDG vars, device files, permission errors. Build each
hostile case in scratch, run the tool with a timeout, report hangs/crashes/writes. Also check it never writes a file (strace -e trace=openat
with O_WRONLY/O_CREAT on a scratch run).""")
seat("MutTripwire", "mutation-tester", "Clause r detection rate: inject forbidden behaviour into the reference.",
     """Make >= 10 variants of the reference that each do one forbidden thing only in rare paths (only when --print-cmd, only for fixtures
with an action, only on the 100th run, only in explain, only in --selftest) - os.system, subprocess, socket, os.fork+exec, multiprocessing.
Score each; report which the counter misses (a trip count of 0 with the behaviour exercised is a hole).""")
seat("ExecSeparability", "executor", "C1/C2 separability, both ways, on the frozen instruments.",
     """Build two scratch trees at %(F)s: (1) tool-only = the reference at tools/mado-terminal.py; (2) entry-only = the C2 positive control
built by %(W)s/ctl/c2/build-control.py (see context for C2R47_WORK). Score both trees with both counters; expected C1 MET/C2 MISSED and C1
MISSED/C2 MET. Report the four summary lines.""")
# ---------------------------------------------------------------- C2 instrument and draft attacks
seat("CritC2Forgery", "critic", "PRED-C2-r47: admit an entry that teaches nothing or lies.",
     """Starting from the C2 positive control (ctl/c2/build-control.py), forge entries that the counter admits but a reader should refuse:
a chain whose steps cite real lines but state false mechanisms, quotes from comments only, a capture typed by hand, a README row pointing
elsewhere, rows whose scope sentence is false, re-claimed held ground with renamed terms. Score each; report admitted forgeries outside the
declared residuals of %(W)s/registration.md.""")
seat("RevC2Counter", "reviewer", "Code review of quality/counters/c2-r47-terminal-entry.py incl. the L1 clause-f change.",
     """Review the counter clause by clause against its docstring and %(W)s/registration.md; especially the L1-rewritten clause_f (diff it
against %(W)s/w1/ExecCounterC2/c2-r47-terminal-entry.py), pin resolution by stem, quote matching, the ground terms. Findings with path:line
and repro.""")
seat("MutC2Counter", "mutation-tester", "Mutation test of PRED-C2-r47.",
     """Mutate the C2 counter in scratch (drop each clause in turn, loosen the ref-pin check, accept any recheck, skip held rows, skip the
resolver_sha256 check) and run %(W)s/ctl/c2/run-controls.py against each mutant (edit a scratch copy's C path). Report mutants no control
kills.""")
seat("CritEntryContent", "critic", "The entry draft's sentences against the script.",
     """Read %(W)s/w1/ScrEntry/entry.md sentence by sentence; check each mechanism claim against /usr/bin/xdg-terminal-exec at the cited
lines (and by a scratch run where cheap). Classify: supported / mis-located / wrong / unpinned. Note also the behaviours the C1 fixtures
show that the entry omits (carried-over keys between candidates, the read-loop exit status, command -v on aliases/builtins). Write a table.""")
seat("ExecEntryQuotes", "executor", "Every quote and locator of the entry draft, by script.",
     """Write a checker that extracts every backticked/quoted span + locator from %(W)s/w1/ScrEntry/entry.md and verifies it against the pins
in %(W)s/fetch/ (xdg-terminal-exec, README.md, xdg-terminals.list) at the stated lines; also every `xdg-terminal-exec:N[-M]` locator is in
range and the cited line contains the named function/variable. Report failures.""")
seat("ExecRows", "executor", "Re-open every candidate SOURCES row of the round.",
     """For each candidate row in %(W)s/w1/ScrRows/rows.md and %(W)s/w1/ScoutSpecs/ (and ScoutOmarchy if any): fetch the URL today, sha256,
compare with the row, grep the located quote at its stated lines; check the URL is tag/commit pinned and that the row has 11 cells with no
`|` inside a cell. Then mirror %(L)s/corpus into scratch, append the rows after S325, run
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md` and paste output + exit.""")
seat("ScoutPinRecheck", "scout", "Are the pins the bytes upstream serves today?",
     """Re-fetch the three pins in %(W)s/fetch/ from their v0.14.3 URLs and the tag tarball; compare sha256 with %(W)s/receipts/fetch-sha256.txt;
confirm the tag still points at 065925df9f419008159258ae169018bfd23df71b (git ls-remote). Report.""")
seat("CritPremise2", "critic", "The corrected premises in registration.md.",
     """Attack the 'Premise corrections from w1' section of %(W)s/registration.md: is the selection half of the round-17 [UNK] really open
at base (or already answered by the round-17 cache bytes at terminal-route-r17.md:123-127)? Do the four ground terms of C2 clause i prove
new ground or just new spelling? Is any C2 'new ground' item actually held elsewhere in the lane (git grep at %(B)s)? Findings + fixes.""")
# ---------------------------------------------------------------- routed items
seat("MutSessionMarker", "mutation-tester", "R3: the session-material marker gate draft fails both ways?",
     """Read %(W)s/w1/ExecSessionMarker.md and its gate copy. In scratch clones: plant a real-shaped client dump / process table / monitor
serial in an unmarked file, in a marked file, and in a registry-named file with real content; also mark a file that is not synthetic.
Each must exit 1. Mutate the marker logic (accept any marked file, skip R3 in marked files) and show the planted cases catch it. Report.""")
seat("RevSessionMarker", "reviewer", "R3: code review of the marker gate and registry.",
     """Review %(W)s/w1/ExecSessionMarker/ (gate, registry, selftest) against round-46 closure R3 (%(L)s/corpus/lessons/round-46-verifier-spotcheck.md
section 6) and SKILL rule 4: is any waiver broader than synthetic fixtures? Does the lane tip read green for the right reason? Never print a
serial value.""")
seat("RevSupersede", "reviewer", "R4a: the S290-S297 supersession block.",
     """Check %(W)s/w1/ExecSupersede/ against %(L)s/CORPUS.md rule 2 and the census: append-only, ids not colliding with S326+, quotes
re-located today, mirror census exit 0. Report what must change before it lands.""")
seat("ExecErrataR45", "executor", "R4b: verify each round-45 erratum draft by command.",
     """For every erratum in %(W)s/w1/ScrErrataR45/: run the command that shows the corrected fact (pins in %(L)s/.ufo/waves/round-45/fetch/ or
re-fetch), paste output; mark CONFIRMED / WRONG. Also check the append-only shape against the entry's end.""")
seat("ExecErrataR1", "executor", "R1: verify the round-46 erratum draft by command.",
     """For %(W)s/w1/ScrErrataR1/: re-derive the two receipts' producing tools (sha256 in their heads vs `git show <rev>:tools/mado-devices.py |
sha256sum` and the l1-draft) and the config count; mark each sentence of the erratum CONFIRMED / WRONG.""")
seat("ExecErrataCal", "executor", "R4c: verify the ConnCalibration errata by command.",
     """For %(W)s/w1/ScrErrataCal/: run each truth command over committed bytes; mark CONFIRMED / WRONG; flag any erratum whose target line no
longer exists.""")
seat("ExecR2Check", "executor", "R2: verify the digest of the untracked round-46 file.",
     """Re-derive every number in %(W)s/w1/ExecR2Digest/ (sha256, bytes, lines, per-class counts) from
%(L)s/.ufo/waves/round-46/w1/ExecStofOracle/receipts/out.json.rows.tsv (read-only, do not move it). CONFIRMED / WRONG per number.""")
seat("ExecToolLedger", "executor", "considerthese proposal 2: is the live-state tool ledger true?",
     """For every row of %(W)s/w1/ScrToolLedger/ledger.md: check the receipt path exists in git, the round, the verdict text in the receipt,
and run each tool's --selftest (read-only). Count rows wrong.""")
seat("ExecSkillSection", "executor", "The SKILL section draft, run as written.",
     """Run every command of %(W)s/w1/ScrSkill/section.md exactly as written (substituting the reference %(W)s/l1-draft/mado-terminal.py for
tools/mado-terminal.py; XDG_CACHE_HOME in scratch; never launch a terminal). Report each command's output and every place an operator would get
stuck or mislead.""")
seat("CritMistakes", "critic", "The round's mined mistakes: are the fixes able to fail?",
     """Read %(W)s/w1/ScrMistakes/mistakes.md. For each proposed fix/QUALITY criterion: is it shown able to fail (a case where it fires)? Is
the class right? Add the mistakes this round already made (seat runaway write, host cache rewrite, misrooted SentHost dir at
%(W)s/SentHost if it existed, w1 draft C2 counter coupling C2 to C1). Write a corrected table.""")
seat("RevengerCache", "revenger", "The resolver cache: what the hotkey run actually uses on this host.",
     """From the script (:179-298, :1179) and %(W)s/w1/ExecCache/ and %(W)s/w1/RevengerUwsm/: reconstruct whether the hotkey's run reads the
cache or resolves cold, using read-only checks (md5 recomputation of the hash input in scratch with LC_ALL=C ls -LRl of the same paths;
compare with line 1 of ~/.cache/xdg-terminal-exec WITHOUT modifying it). Conclude whether the cold capture equals what the hotkey uses today.""")
seat("CritUwsm", "critic", "Attack the RevengerUwsm conclusion.",
     """Read %(W)s/w1/RevengerUwsm/ and test its claim about the environment `uwsm-app --` gives the resolver (read-only: code reading,
`systemctl --user show-environment` restricted to XDG_*/PATH keys). Is any selection-relevant variable different? Findings with evidence.""")
seat("ConnW1Ledger", "connector", "Every w1 finding mapped to the freeze.",
     """Read all %(W)s/w1/*.md reports. Build a ledger: finding (seat, id) -> addressed by registration.md / by the counters / open. List open
findings that should block data or force a v2 re-registration.""")
seat("ConnPatterns", "connector", "Cross-round patterns: do round-45/46 freeze breaks recur here?",
     """Compare %(W)s/registration.md with %(L)s/.ufo/waves/round-46/registration-v2.md and -v3.md: which round-46 break classes (ambient
reference copy, deletable marker, absolute-path binaries, inherited pipe, self-receipt, uncited pinned rows, indented code) have an analogue
here and is it closed? Report per class.""")
seat("SentPrivacyW2", "sentinel", "Session material in the round's wave files before they are committed.",
     """Scan every file under %(W)s (w1/, receipts/, ctl/) for session material: window titles, process tables, monitor serials, home-directory
listings, tokens; also run `python3 -I %(L)s/quality/check-session-material.py --selftest` and the gate logic on a scratch clone with the wave
dir copied in. Report path:line and class only, never values.""")
seat("ScoutMisroot", "scout", "Misrooted round-47 seat files in the fleet root.",
     """Read-only: `git -C /home/vgpnk/Projects/shokunin status --porcelain` and list any untracked path whose content names mado round 47 or a
round-47 seat; check /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-47 for files outside w1/, w2/, ctl/, receipts/, fetch/,
l1-draft/, assimilation/. Never move or delete anything. Report.""")

seat("ExecLiveDryRun", "executor", "The live receipt the round will land: shape, privacy, AGREE.",
     """On this host, read-only, with XDG_CACHE_HOME in your scratch: capture `xdg-terminal-exec --print-id --print-path --print-cmd` stdout to
a scratch file, then run `python3 -I %(W)s/l1-draft/mado-terminal.py explain --observed <capture>` (same env). Report the MADO_TERM line, the
exit code, every trace line class (paths may name ~/.local/share/applications - say whether that is a session-material finding under
%(L)s/quality/check-session-material.py rules), and run the C2 clause-f checks of the frozen counter by hand on your receipt shape.""")
seat("ExecRegistryMirror", "executor", "All registry changes of the round together, before any append.",
     """Mirror %(L)s/corpus in scratch; apply in order the S290-S297 supersession draft (%(W)s/w1/ExecSupersede/) and the new rows
(%(W)s/w1/ScrRows/rows.md); run the census validate on the mirror (paste output + exit); run the prompt's id-collision guard against
%(P)s/SOURCES.append.md on the mirror; report collisions and E-codes.""")
seat("ExecFixtureMap", "executor", "Which script branches do the frozen C1 fixtures reach?",
     """Instrument a scratch copy of /usr/bin/xdg-terminal-exec with `set -x`-style line tracing (bash: PS4='+${LINENO} ' and `bash -x`), run
it on every fixture of %(L)s/quality/counters/c1-r47-fixtures.json (materialized in scratch, XDG_CACHE_HOME in scratch, restricted PATH, a
timeout per run), and report per-line hit counts: which executable lines of the script no fixture reaches.""")
n = len(items)
assert 32 <= n <= 64, n
assert len({i["name"] for i in items}) == n
roles = collections.Counter(i["role"] for i in items)
print(n, dict(roles))
spec = {"wave": "w2", "context": CONTEXT, "reportDir": ".ufo/waves/round-47/w2", "items": items}
with open(os.path.join(HERE, "w2-spec.json"), "w") as fh:
    json.dump(spec, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
