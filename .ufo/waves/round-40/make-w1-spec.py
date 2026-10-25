#!/usr/bin/env python3
"""Generates .ufo/waves/round-40/w1-spec.json (64 seats, one v2 wave).

Run: python3 make-w1-spec.py  (writes next to itself, lane-relative reportDir).
"""
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
W = LANE + "/.ufo/waves/round-40"
FETCH = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-40/fetch"
FREEZE = "5e7e88525cc539563de7746361b2650802e81809"
BASE = "9fc511ddce708327377161202f358ce37dc266ba"
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
mado round 40 (hyaku run 7, 2026-10-25), inline v2 wave w1 (64 seats). Lane repo: %(L)s
Claims are FROZEN at %(W)s/registration.md (freeze commit %(F)s, base %(B)s) - read it first. Two claims:
- C1 operability (capability acquisition): tools/mado-options.py gains `--live` (+ `--hyprctl PATH`, `--probe KEY`): one
  `hyprctl getoption -j KEY` per declared key, native replies (forms int|float|str|custom, or the text `no such option`)
  compared after host-style conversion; exit 5 on compositor failure naming the key; exit 2 on a hostile probe key.
  Frozen counter quality/counters/c1-r40-live.py (PRED-C1-r40-v1): target fixtures=13/13 TARGET_MET; base 0/13.
  Throwaway reference tool: %(W)s/c1/ctl-ref-tool.py.txt (a CONTROL, never delivered). Controls: %(W)s/ctl/run-c1-controls.py.
- C2 coverage (sourced): corpus/knowledge/hyprctl-getoption-native-forms-r40.md + registry rows (held S162, S173 re-opened;
  >=2 new rows incl. one own-work census receipt). Frozen counter quality/counters/c2-r40-forms-entry.py (PRED-C2-r40-v1,
  clauses a-h); target admitted=1/1; base 0/1. Controls: %(W)s/ctl/run-c2-controls.py.
Provisional facts (from the L1 prototype; every seat re-derives what it relies on, none is evidence until re-opened):
- host Hyprland 0.56.2 (commit efb50993780079460b0cbed1363e2166a2de1d9f), hyprlang 0.6.8 (installed, headers present).
- the static table of the host tree has 70 option keys (python3 -I tools/mado-options.py --home $HOME); native
  `hyprctl getoption -j KEY` replies are one JSON object {"option":K,"set":B,"<form>":V}, form in int|float|str|custom;
  an unknown key prints `no such option` with exit 0. Captured forms over the 70 keys: int 44, float 5, custom 13, str 8
  (%(W)s/c1/native-capture.jsonl).
- gradient values print as `<hex ARGB, lowercase unpadded> ... <N>deg`; Hyprland v0.56.2 src/config/legacy/ConfigManager.cpp
  ~103-170 (gradient handler) clears colours and sets the angle only when a `deg` token is present; src/config/shared/
  complex/ComplexDataTypes.hpp CGradientValueData::toString / CCssGapData / CFontWeightConfigValueData.
- host finding: theme hyprland.conf declares `$activeBorderColor = rgb(e68e0d)` and `col.active_border = $activeBorderColor`;
  the defaults tree declared the same key earlier with `rgba(33ccffee) rgba(00ff99ee) 45deg`; live reads `ffe68e0d 45deg`
  (the angle is inherited). Under that model the reference tool labels all 70 keys: 62 agreement, 8 agreement*, 0 mismatch.
# Write scope and safety
- Write ONLY inside %(L)s. NEVER write/edit the fleet repo (/home/vgpnk/Projects/shokunin except as your task names),
  sibling lanes, templates/, scripts/, MANIFEST.json, .ufo/state/, .ufo/watchdog.log, .scratch/, or the lane's jj/git index.
  Never run mutating git/jj anywhere in the lane or the fleet (no add/commit/push/checkout/reset/stash/describe/bookmark).
  Read-only git (log/show/diff/status/rev-parse/ls-tree/cat-file) is fine.
- Write ONLY to your own seat directory %(W)s/w1/<YourSeatName>/ (create it), plus any explicit destination your task names
  (receipts named by the task go to %(W)s/fetch/). Never edit an existing tracked file; the L1 is the only integrator.
  Write your Report file FIRST (a short status), then refine it; a seat that dies without a report is a dead seat.
- Every `Report:` trailer path is relative to %(L)s - write it at %(L)s/<that path>.
- Host safety: pacman is PAUSED host-wide - never run pacman or any package transaction. No host-service or compositor
  mutation, no input injection, no socket connect of your own. The ONLY compositor verbs allowed are the read-only
  `hyprctl getoption -j <key>`, `hyprctl version`, `hyprctl descriptions -j`; never `keyword`, `dispatch`, `reload`, `setprop`,
  `--batch`. Host config trees are READ-ONLY: copy their bytes into evidence, never into config trees; shape-only for secrets.
- Git fixtures (run-6 incident): any fixture repo is `D=$(mktemp -d) && git -C "$D" init -q`, every later git call names
  `-C "$D"`, and `git -C "$D" rev-parse --show-toplevel` must equal `$D` before the first commit; never `git commit` with
  a throwaway identity anywhere else. Use /tmp (mktemp -d) for scratch; clean it up.
- Tooling authorization (operator, 2026-10-19): install tools that help the task (read /home/vgpnk/.omp/agent/RULES.md
  first; official channels only: uv tool / npx / official binaries in ~/.local/bin; never pacman, never -Sy/-Syu/-U/-R).
  Record tool/version/channel/reason in your report.
- Seat tool state: your tools start at the fleet root, not the lane: use absolute paths everywhere.
- You are a leaf: no subagent dispatch, no background jobs, no spawning.
- Every finding names what it attacks or supports (a path:line, a command and its output, or a hash). Never fabricate:
  an unrun check has not passed.
"""

def sub(t):
    for k, v in (("%(L)s", LANE), ("%(W)s", W), ("%(F)s", FREEZE), ("%(D)s", FETCH),
                 ("%(B)s", BASE)):
        t = t.replace(k, v)
    return t


CONTEXT = sub(CONTEXT)
items = []


def seat(name, role, target, task):
    items.append({
        "name": name, "role": role,
        "prompt": sub(GODSPEED + "# Target\n" + target.strip() +
                      "\n# Task\n" + task.strip() + "\n")})



# ------------------------------------------------------------ executors (20)
seat("ExecToolLive", "executor",
     "Deliverable candidate for C1: the production `--live` tool.",
     """Copy %(W)s/c1/ctl-ref-tool.py.txt (the reference control) and the BASE tool %(L)s/tools/mado-options.py into
%(W)s/w1/ExecToolLive/ and build the DELIVERABLE candidate `mado-options.py` there: reference `--live` / `--hyprctl` /
`--probe` behaviour, docstring updated (modes, native forms, conversion rules, the angle-inheritance rule, exit 5 and exit
2 contracts, the read-only verb list), the unused `--getoption FILE` path KEPT unchanged, and the hermetic `--selftest`
extended from 71 to AT LEAST 85 assertions that exercise the new path: native forms (int/float/str/custom/no such option),
every conversion (0x hex, rgba 8-hex, rgba(r,g,b,a), rgb 6-hex, rgb(r,g,b), true/on/yes prefixes, false/off/no, negative
int, float), gradient with/without angle and with an inherited angle, gap 1-4 values, font weight names (case-insensitive),
shadowed declarers (agreement*), set=false, live-default via --probe, failure exit 5 naming the key, malformed reply,
missing program, hostile probe (-x, empty), exact argv (only getoption -j KEY), config root unchanged. The selftest builds a
stub hyprctl inside its private temp dir and prints `MADO_OPTIONS_SELFTEST: k/n passed`. Python stdlib only; no socket/
urllib/http. Verify: `python3 -I <your file> --selftest` exits 0 with k==n>=85, and score it with the frozen counter:
`cd %(L)s && python3 -I quality/counters/c1-r40-live.py --repo . --rev %(F)s --tool <your file>` (clauses a,g,b should hold;
clause k reads the committed capture; expect fixtures=13/13). Report the two outputs verbatim. Do NOT edit the frozen
counter or the reference.""")
seat("ExecToolIndep", "executor",
     "Differential implementation for C1: an independent `--live` merge written from the spec only.",
     """WITHOUT reading %(W)s/c1/ctl-ref-tool.py.txt or quality/counters/c1-r40-live.py, read only %(W)s/registration.md C1, the BASE tool
%(L)s/tools/mado-options.py and the hyprlang v0.6.8 / Hyprland v0.56.2 sources (raw.githubusercontent.com; commit
efb50993780079460b0cbed1363e2166a2de1d9f: src/config/legacy/ConfigManager.cpp, src/config/shared/complex/ComplexDataTypes.hpp;
hyprlang tag v0.6.8 src/config.cpp:185-264), and write your own `--live` implementation as a patch of a copy of the BASE
tool in %(W)s/w1/ExecToolIndep/mado-options.py. Then score it with the frozen counter (allowed now):
`cd %(L)s && python3 -I quality/counters/c1-r40-live.py --repo . --rev %(F)s --tool <your file>` and report every failing
fixture line verbatim (a failing fixture is a finding about the spec or the counter, not a defect of yours, unless you
can show otherwise). Also diff your conversion table against the counter's reference model (hl_int, gradient_text, gap_text,
WEIGHTS) and list every disagreement.""")
seat("ExecOracleHlInt", "executor",
     "Oracle for C1's integer conversion: the real hyprlang v0.6.8 parser versus the counter's Python model.",
     """hyprlang 0.6.8 is installed with headers (pkg-config hyprlang). Write a small C++ program in %(W)s/w1/ExecOracleHlInt/
that registers an INT option, parses `x = <spelling>` through Hyprlang::CConfig for a corpus of >=150 spellings (0x hex,
rgba(8 hex), rgba(r,g,b,a) incl. alpha 1/0.8/0.4/0.5, rgb(6 hex), rgb(r,g,b), true/on/yes/false/off/no incl. prefix forms like
`yes, please :)` and `on # c`, negative and plain decimals, junk) and prints the stored integer or the parse error. Then run the
Python model `hl_int` from %(L)s/quality/counters/c1-r40-live.py on the same corpus and list EVERY disagreement (value or
error-vs-value). Save corpus, outputs and the diff. If the real library cannot be linked, compile the static function
configStringToInt (hyprlang v0.6.8 src/config.cpp:185-264, fetched read-only) standalone and say so.""")
seat("ExecAllOptionsForms", "executor",
     "Survey the compositor's native getoption forms over EVERY option, not just the 70 declared keys.",
     """Obtain the list of all option names (`hyprctl descriptions -j`, falling back to ConfigValues.cpp at the host commit),
run `hyprctl getoption -j <name>` for each name (serially; read-only), and write %(W)s/w1/ExecAllOptionsForms/forms.tsv
(name, form, set, value) plus a summary: count per form, every key whose reply has none or more than one of int/float/str/custom,
every reply that is not one JSON object, and the keys the frozen capture could not have contained. State plainly whether the
counter's assumption of exactly four forms holds over the whole option set.""")
seat("ExecLiveCensus", "executor",
     "Census receipt candidate for C2's own-work row (clause h format).",
     """Using the reference tool %(W)s/c1/ctl-ref-tool.py.txt (copy it to /tmp as mado-options-ref.py) run
`python3 -I mado-options-ref.py --home $HOME --live` on the host. Write %(W)s/w1/ExecLiveCensus/census-receipt.txt in exactly the
format the C2 counter's clause h parses: a line `forms int=A float=B str=C custom=D` (count of native reply forms among the declared
keys) and a line `labels agreement=W agreement*=X mismatch=Y config-only=Z live-default=V`, plus per-label key lists, the
host Hyprland version, hyprlang version, a placeholder line `tool sha256 <TOOLSHA>` and the 8 keys with more than one declarer
with owner file:line of each declarer. Also write a second variant where the reference's angle-inheritance is switched off (patch a
copy) and list the keys that flip to mismatch (expected: general:col.active_border, group:col.border_active). Report the counts.""")
seat("ExecCaptureStable", "executor",
     "Stability of the committed native capture (clause k).",
     """Re-capture `hyprctl getoption -j KEY` for the 70 keys of `python3 -I %(L)s/tools/mado-options.py --home $HOME` three times at
one-minute spacing (read-only), and diff each against %(W)s/c1/native-capture.jsonl (sha256 1fe39c05...). Report every key whose reply
changed between captures and whether any change alters the form of that key. Save the three captures in your seat dir.""")
seat("ExecFetchComplexTypes", "executor",
     "Source receipt for the new C2 row: Hyprland ComplexDataTypes.hpp at the host commit.",
     """Fetch https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/complex/ComplexDataTypes.hpp
(curl -sSL, record HTTP status and date) to %(D)s/complex-data-types-efb5099.bin (exact bytes). Write %(W)s/w1/ExecFetchComplexTypes/quotes.md:
sha256 of the file, then for each of these facts a located quote of 3-25 words that occurs verbatim in the bytes, with line number:
(1) the gradient toString format (`{}deg`), (2) the gradient reset() setting the angle to 0, (3) CCssGapData 1-4 value expansion,
(4) the font weight table including ultraheavy, (5) the weight parser falling back to 400 outside 100..1000. Do not paraphrase a quote;
verify each with grep -F on the saved bytes and paste the command output.""")
seat("ExecFetchConfigMgr", "executor",
     "Source receipt for held row S162 re-opened: ConfigManager.cpp gradient handler.",
     """Fetch https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/ConfigManager.cpp
to %(D)s/config-manager-efb5099.bin (exact bytes; record HTTP status, date, sha256). Write %(W)s/w1/ExecFetchConfigMgr/quotes.md: the file
sha256, and located quotes (3-25 words, verbatim, with line numbers, each verified with grep -F) for: the gradient handler clearing
colours (`DATA->m_colors.clear();`), the angle being set only when a `deg` token is present, and the max-colours-10 guard. Also report
whether the held row S162 (grep -n '^| S162 ' %(L)s/corpus/SOURCES.md) still names this URL and commit, and whether the bytes
equal the round-39 receipt %(L)s/.ufo/waves/round-39/fetch/S162-r39.bin (sha256 compare).""")
seat("ExecFetchHyprlang", "executor",
     "Source receipt for held row S173 re-opened: hyprlang config.cpp configStringToInt.",
     """Fetch https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp to %(D)s/hyprlang-config-v0.6.8.bin (exact bytes; record HTTP status,
date, sha256). Write %(W)s/w1/ExecFetchHyprlang/quotes.md: located quotes (3-25 words, verbatim, line numbers, grep -F verified) for: the rgba( branch,
the rgb( branch, the true/on/yes branch returning 1, the false/off/no branch returning 0, and the `0x` hex branch. Report whether held row S173
(grep -n '^| S173 ' %(L)s/corpus/SOURCES.md) names this URL and whether the bytes equal the round-39 receipt .ufo/waves/round-39/fetch/S173-r39.bin.""")
seat("ExecFetchK2Sources", "executor",
     "Receipts for the assimilation candidate K2 (host-producer-outputs-r29): the omarchy v3.8.4 indicator scripts.",
     """Fetch https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/default/waybar/indicators/screen-recording.sh and .../notification-silencing.sh
to %(D)s/omarchy-v3.8.4-screen-recording.bin and %(D)s/omarchy-v3.8.4-notification-silencing.bin (exact bytes; HTTP status, date, sha256), and copy the host
files (read-only) ~/.local/share/omarchy/default/waybar/indicators/{screen-recording,notification-silencing}.sh to %(D)s/host-indicator-*.bin; compare host vs
upstream (cmp). Write %(W)s/w1/ExecFetchK2Sources/quotes.md with located quotes (3-25 words, verbatim, grep -F verified, line numbers) naming what each script probes
(`pgrep -f ... gpu-screen-recorder`, `makoctl mode`). Check the candidate text at /home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/host-producer-outputs-r29.md
for each quote it carries and mark each REPRODUCED / ABSENT / DIFFERENT. Source repo shokuknow is read-only: never write there.""")
seat("ExecK2HostReads", "executor",
     "Host-side reads for K2: the two host-local producers and the config.",
     """Read-only: record sha256 and size of ~/.config/waybar/config.jsonc, resolve ~/.local/bin/gkeep and ~/.local/bin/ai-usage (readlink -f, size, sha256,
first 12 lines shape-only; redact anything secret-shaped), the custom/gkeep and custom/ai-usage blocks of config.jsonc (exec, interval, return-type),
`pgrep -f '^gpu-screen-recorder'` result, `makoctl mode`, and the cache file ~/.cache/ai-usage/status.json metadata ONLY (key names, no values that look like
tokens, and whether its updated_at is within 24h). Save all into %(W)s/w1/ExecK2HostReads/host-reads.txt and %(D)s/host-k2-reads.txt (the latter the evidence the
entry may quote; exclude volatile timestamps from any line you propose as a quote - the round-39 closure refused a quote whose timestamp rotated).
Compare each statement of the candidate K2 (/home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/host-producer-outputs-r29.md) with today's host state: still true / changed.""")
seat("ExecAssimIdGuard", "executor",
     "Id-collision guard for the assimilation (addendum section 10), with the proof.",
     """Run the section-10 guard exactly: A=%(W)s/assimilation; extract 0-3-space-indented registry ids of %(L)s/corpus/SOURCES.md to $A/reg-ids and of
/home/vgpnk/Projects/shokuknow/merge/mado/SOURCES.append.md to $A/staged-ids, `comm -12` to $A/collisions. Prove the guard once: build a scratch registry copy
with an indented row `  | S002 |` against a staged copy holding S002 and show the guard prints S002 (and that the column-zero-only pattern would not). Write
both id lists' counts, the collision count and the ids, the renumber map candidate for the K2 ids (by DOCUMENT, not arithmetic: list the staged id -> source URL ->
next free lane id), and your commands/outputs to %(W)s/w1/ExecAssimIdGuard/guard.md. Do not write the real assimilation files other than $A/{reg-ids,staged-ids,collisions}.""")
seat("ExecQuarantineSlice", "executor",
     "Quarantine slice for mado (register read-only), re-derived and hand-checked where reachable.",
     """Derive the slice with the section-10 command: R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md; awk -F'|' -v l='mado'
'$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R" > %(W)s/assimilation/quarantine-slice (every line carries an S-id).
For each row that the K2/K1 candidates cite, fetch the cited source and locate the quote (present -> adopt with your located anchor; absent -> refuse with the
fabrication class; volatile/rotated -> unverifiable, NOT fabrication; unreachable -> unverifiable). Write %(W)s/w1/ExecQuarantineSlice/verdicts.md (one row per
slice entry: id, source, verdict, evidence) - rows you cannot reach are marked unverifiable, never guessed. Never write into /home/vgpnk/Projects/shokuknow.""")
seat("ExecWatchdogTable", "executor",
     "considerthese proposal (2026-10-25 #2): dead attempts and dirty closures for mado, from the watchdog digests.",
     """Read-only: /home/vgpnk/Projects/shokunin/.ufo/watchdog.log and the lane's corpus/lessons/round-*-verifier-spotcheck.md. Build %(W)s/w1/ExecWatchdogTable/table.md: one row per
mado round from 32 to 39 with attempts (launch lines), dead attempts (`lane-dead-no-report`), completion time, and whether the round-N spot-check names leftover
working-tree files (quote the spot-check line). Give the counting commands (grep -c ...) beside each number. Do not interpret beyond the counts.""")
seat("ExecScratchMirror", "executor",
     "A reusable scratch mirror + census gate for the registry append (section 10: scratch validation before the append).",
     """Write %(W)s/w1/ExecScratchMirror/mirror-validate.sh: given an append-block file and a list of knowledge files, it creates `V=$(mktemp -d)` (never in the lane), copies
%(L)s/corpus (SOURCES.md, README.md, knowledge/, lessons/) into $V/corpus, appends the block into the `## Registry` table (before the blank line ending the table), copies the
listed knowledge files at their repo-relative paths, and runs /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$V/corpus/SOURCES.md" printing its
output and exit code. Prove it: a block with one valid row exits 0; a block repeating an existing id exits non-zero with E03; a block repeating an existing URL prints W04/E04
as the census defines. Save the three runs' output.""")
seat("ExecHarmChecks", "executor",
     "Round-start harm baselines beyond the committed receipts.",
     """Run and save (each with exit code) into %(W)s/w1/ExecHarmChecks/: `python3 -I %(L)s/quality/check-index.py --repo %(L)s --rev %(B)s`,
`python3 -I %(L)s/quality/check-index-rows.py --help` (then the documented invocation at the base), `python3 -I %(L)s/quality/check-evidence-pointers.py --help` (then the documented
invocation), `bash %(L)s/tools/mado-verify.sh --no-live` summary line only, and `python3 -I %(L)s/tools/mado-options.py --selftest` (base: expect 71/71). State which
checks the L1 should re-run at the end and with which exact command lines.""")
seat("ExecMutBaseline", "executor",
     "Run the frozen control harnesses at the freeze commit from a clean sandbox clone.",
     """In `S=$(mktemp -d)` clone the lane read-only (`git clone -q %(L)s $S/lane`, then `git -C $S/lane rev-parse --show-toplevel` equals $S/lane; checkout detached %(F)s with
`git -C $S/lane -c advice.detachedHead=false checkout -q %(F)s`) and there run `python3 -I .ufo/waves/round-40/ctl/run-c2-controls.py` and
`python3 -I .ufo/waves/round-40/ctl/run-c1-controls.py` (expect CTL_C2 21/21, CTL_C1 18/18; MADO_CTL_REV may need to be %(F)s since `master` resolves to the clone's branch).
Report both outputs verbatim, timings, and any difference from the committed receipts %(W)s/receipts/ctl-c{1,2}.txt. Remove the sandbox.""")
seat("ExecHostSourceGraph", "executor",
     "Independent derivation of the 8 shadowed keys and their declarers.",
     """Without using tools/mado-options.py, derive from the host tree bytes (~/.config/hypr/hyprland.conf and every `source =` it reaches, depth-first, in order, with variable
expansion as hyprlang does) every option key declared more than once, listing each declarer (file:line, value as written). Compare with the 8 `agreement*` keys the L1 expects
(`python3 -I %(L)s/tools/mado-options.py --home $HOME` gives the last declarer; the L1's reference census says 8 shadowed keys). Report the set difference in both directions.""")
seat("ExecStubFidelity", "executor",
     "Fidelity of the counter's stub hyprctl against the real one.",
     """Read quality/counters/c1-r40-live.py's STUB and the argv contract. For 12 keys covering all four forms and one absent key, compare the stub's reply bytes shape against the real
`hyprctl getoption -j KEY` reply byte-for-byte shape (whitespace, trailing newline, key order, spacing before `}`: the real reply is `{"option": "k", "int": 1, "set": true }`),
and test that the reference tool and the BASE `--getoption`-less code parse the REAL reply text (feed the real reply bytes through the same json parsing). Report any shape the
stub cannot emit that the real binary does (e.g. spaces, newlines, non-ASCII, quoted newlines in str values).""")
seat("ExecHostCompose", "executor",
     "Compose the host findings table for the lesson from the census and the declarer derivation.",
     """Build %(W)s/w1/ExecHostCompose/host-table.md: for each of the 62 + 8 labelled keys that matter to an operator (colours, gaps, borders, rounding, blur, animations enabled,
input, misc), one row: key, declared (as written), live (native form and value), label, owner file:line. Use the reference tool (copy of %(W)s/c1/ctl-ref-tool.py.txt in /tmp) for the
data; flag the two angle-inheritance rows. Keep it to facts the data shows; no recommendations.""")

# --------------------------------------------------------------- scribes (12)
seat("ScrFormsEntryA", "scribe",
     "Draft A of corpus/knowledge/hyprctl-getoption-native-forms-r40.md (operator-reader decision table).",
     """Write %(W)s/w1/ScrFormsEntryA/entry.md following the lane's entry shape (read corpus/knowledge/config-option-table-r39.md and corpus/QUALITY.md first): header lines
`source: S### - ...` (use placeholders S_FORMS_1.. for new rows; held rows are S162 and S173), `verified-at: 2026-10-25`, `recheck: on-change`; OBS/INF/UNK-tagged sections:
what `hyprctl getoption -j` answers (four forms + `no such option`), per-form conversion table, gradient angle inheritance with the host's two rows as the worked example, what
this does NOT license (runtime `keyword` overrides are outside; nothing is claimed about options the host never declares). Every OBS line carries a quote slot written as
`<<QUOTE S_ID: ...>>` for the L1 to fill from the executors' located quotes (%(W)s/w1/ExecFetch*/quotes.md, read them when present). Reuse nothing unverified; keep it under 140 lines.""")
seat("ScrFormsEntryB", "scribe",
     "Draft B of the same entry (parser-semantics ordering), written independently of draft A.",
     """Write %(W)s/w1/ScrFormsEntryB/entry.md under the same shape rules as above but organised as the parser sees it: declaration -> handler -> stored value -> toString -> getoption reply -> label.
Do not read %(W)s/w1/ScrFormsEntryA. Use `<<QUOTE S_ID: ...>>` slots. Keep it under 140 lines. State at the end which claims rest on the host census (own-work) versus upstream bytes.""")
seat("ScrSourcesRowsForms", "scribe",
     "Registry rows for C2: draft in the lane's 11-column schema.",
     """Read %(L)s/corpus/SOURCES.md (header, rows S162, S173, S218-S220 as models) and CORPUS.md section SOURCES.md in /home/vgpnk/Projects/shokunin. Draft in %(W)s/w1/ScrSourcesRowsForms/rows.md: (a) the NEW row
for Hyprland ComplexDataTypes.hpp at efb5099 (kind code, tier A, status mined, opened 2026-10-25, recheck on-change, used-by corpus/knowledge/hyprctl-getoption-native-forms-r40.md), (b) the NEW own-work row for the
live census receipt (anchor names the receipt path .ufo/waves/round-40/fetch/ and the tool sha placeholder), (c) the used-by EXTENSION text for S162 and S173 (cells 1-10 byte-equal; only cell 11 grows) shown as old->new cell 11.
No cell contains a `|`. Use placeholders for ids; the L1 assigns the next free ids (note the registry already holds ids up to S277).""")
seat("ScrLessonGate", "scribe",
     "Draft the round-40 lesson `## Gate` block.",
     """Draft %(W)s/w1/ScrLessonGate/gate.md in the shape of %(L)s/corpus/lessons/round-39.md `## Gate`: GATE lines `GATE <id> receipt=<path> sha256=<64 hex> quote="<q>"` as templates for the rows
C2 cites (placeholders for sha/quote the L1 fills), plus the assimilation ledger: candidates K1 host-bar-producers-r28.md, K2 host-producer-outputs-r29.md, each with scope check against PROVINCE.md, a QUALITY bar
check (read corpus/QUALITY.md criteria 1-64), held-coverage check against waybar-walker-semantics.md, verdict slot, reason and flip condition; D2 correction note for the round-39 S224 label ("refused (fabrication
class)" -> unverifiable: rotated volatile timestamp). Leave verdict slots open where the executors' evidence is not in yet; never invent a verdict.""")
seat("ScrMistakes", "scribe",
     "Draft `## Mistakes` for the round-40 lesson from this round's own errors and round-39's.",
     """Read %(L)s/corpus/lessons/round-39.md, round-39-verifier-spotcheck.md and the L1's work trail: the C1 counter generator's first draft let mutants M03 (bool exactness) and M05 (3-value gap)
SURVIVE the controls until the generator guaranteed one quirk spelling of every type per tree (receipt trail: .ufo/waves/round-40/receipts/ctl-c1.txt before/after is not committed for the first run - the L1 states it); the
L1's first reference model mis-expanded 3-value gaps (2 of 8 generated fixtures failed); the angle-inheritance finding came from a naive-compare run that mislabelled 14 of 70 keys. Draft 3-4 mistake rows
(class - evidence pointer - captured-by - fix) and a candidate QUALITY.md criterion 65 text (the class: a mutation survives because the generator under-samples a spelling class; fix: each generated tree must carry a
quirk spelling of every type, and the controls list a mutant for each) citing the lesson, in %(W)s/w1/ScrMistakes/mistakes.md. The fix counts only once shown able to fail - name the control that fails.""")
seat("ScrScorecard", "scribe",
     "Draft the SCORECARD round-40 section (claims table, capabilities, planned round 41).",
     """Model on %(L)s/SCORECARD.md `## Round 39` (line ~2423) and its Capabilities table. Draft %(W)s/w1/ScrScorecard/scorecard-r40.md: claims table (C1 operability, C2 coverage) with before->after slots, counting commands exactly
as in registration.md, capability row `live option-table merge` (what it can now do; evidence pointers; first-working round 40), harm-watch slots, sources/saturation line slots, `### Planned (round 41; intent only)` slot.
Use `<<AFTER ...>>` slots for every measured number; invent none. Also draft the LOG.md `## Round 40` entry (model on the `## Round 39` entry of LOG.md) in %(W)s/w1/ScrScorecard/log-r40.md: dated bullets for the freeze (%(F)s), wave w1, data commits (`<<HASH>>` slots), the host finding (angle inheritance), the assimilation outcome (slots), the considerthese item, errata (D2).""")
seat("ScrReadmeIndex", "scribe",
     "Draft the corpus/README.md index row, coverage-map text and Frontier line for the C2 entry.",
     """Model on the round-39 row for `knowledge/config-option-table-r39.md` in %(L)s/corpus/README.md (the row MUST begin with the column-zero text ``| `knowledge/hyprctl-getoption-native-forms-r40.md` `` - one
literal space after the pipe). Draft in %(W)s/w1/ScrReadmeIndex/index.md: the row, the matching coverage-map line(s), and a `## Frontier` sentence for round 40 (what moved onto sourced ground: native reply forms and
conversions; what stays unknown: runtime `keyword` overrides, options the host never declares, Lua-era config). Check `python3 -I %(L)s/quality/check-index-rows.py --help` for row fidelity rules and obey them.""")
seat("ScrSkillTable", "scribe",
     "Draft the SKILL.md decision-table rows for the new `--live` mode.",
     """Read the existing `mado-options.py` rows/sections of %(L)s/SKILL.md (grep -n 'mado-options' SKILL.md) and draft in %(W)s/w1/ScrSkillTable/skill-rows.md the additive text: a row for `--live` (command, what it prints,
exit codes 0/2/3/4/5, the read-only verb it runs, when to use it vs `--getoption FILE`), an error-signature row for each exit code, and the angle-inheritance reading rule (agreement* vs mismatch). Additive only;
no existing text is edited.""")
seat("ScrProvinceRow", "scribe",
     "Draft the PROVINCE.md refinement for `--live` (new read surface: the compositor's getoption verb).",
     """Read the PROVINCE.md tool table and the `mado-options.py` row if present (grep -n 'mado-options' %(L)s/PROVINCE.md). Draft in %(W)s/w1/ScrProvinceRow/province.md an append-only `Round-40 refinement`
paragraph stating: `--live` runs exactly `hyprctl getoption -j KEY` (a read verb of the request socket) per declared key and per `--probe`, never any other verb, writes nothing, standard library only, and is
therefore an owned read surface under the existing `Never mutates a running compositor state` rule; who the adjacent lanes are (tsukuroi: compositor package; none owns the verb). Keep the existing boundary wording.""")
seat("ScrAssimK2", "scribe",
     "Draft re-grounded K2 (host-producer-outputs) entry if the scope check admits it, else the refusal text.",
     """Read /home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/host-producer-outputs-r29.md (read-only), PROVINCE.md, corpus/QUALITY.md, corpus/knowledge/waybar-walker-semantics.md (what is already held about
the same modules). Write %(W)s/w1/ScrAssimK2/verdict-and-draft.md: (1) scope/held/quality check with evidence, (2) a verdict slot (ADMIT/REFUSE) with your recommendation, (3) if ADMIT: a re-grounded entry draft that
carries ONLY statements you can tie to the executors' receipts (%(D)s/ and %(W)s/w1/ExecFetchK2Sources/, ExecK2HostReads/ when present) with `<<QUOTE>>` slots and NO volatile timestamp line as a quote, keeping the campaign's
OBS/INF/UNK tags; (4) if REFUSE: reason and flip condition.""")
seat("ScrConsidertheseLesson", "scribe",
     "Draft the considerthese-mining paragraph (2026-10-25 proposal 2) for the round-40 lesson.",
     """Read %(L)s/considerthese/2026-10-25.md (proposals only; never edit it) and %(W)s/w1/ExecWatchdogTable/table.md when present. Draft in %(W)s/w1/ScrConsidertheseLesson/mined.md: the proposal text quoted with its date,
the lane's grounding (what the watchdog log actually shows, with the counting commands), the disposition (lands as a lesson table; no QUALITY criterion unless a mistake backs it), and which later proposals remain open.""")
seat("ScrReportDraft", "scribe",
     "Draft the round-40 report skeleton with every required section and evidence slots.",
     """Model on /home/vgpnk/Projects/shokunin/.ufo/reports/round-39/mado.md (read it). Draft %(W)s/w1/ScrReportDraft/report-skeleton.md with sections in the order the prompt requires: Work performed (open by naming the two claims),
Landed changes, Before -> after measurements, Sources & frontier, Trend verdicts, SHONEN (one line per box of the lane SHONEN.md, four boxes, each [~] with a pointer or [ ]), plus Stale-lane, Tool installs and Open L0 questions
lines. Evidence slots `<<...>>` only; invent nothing. Also list the seat-role mix table placeholders.""")

# ------------------------------------------------------------- simplifier (1)
seat("SimpMergeUnify", "simplifier",
     "YAGNI review of the reference `--live` merge against the BASE `merge_rows`.",
     """The reference %(W)s/c1/ctl-ref-tool.py.txt adds `merge_live`/`native_equal`/`hl_int` beside the BASE `merge_rows`/`values_equal`. Produce %(W)s/w1/SimpMergeUnify/unified.py (a copy of the reference) in which the two
merges share one labeller (label rules in one function; the live-source differs only in how rows get (form, value, set)) and every duplicated conversion helper is deleted where the BASE helper already does the job, WITHOUT changing
behaviour: `python3 -I quality/counters/c1-r40-live.py --repo %(L)s --rev %(F)s --tool <your file>` must still print fixtures=13/13, and `--getoption FILE` mode outputs byte-identical rows to the BASE tool on the
selftest's own fixtures. Report the line counts before/after and what you deleted.""")

# ------------------------------------------------------- reviewers (8)
seat("RevC1Counter", "reviewer", "Attack counter c1-r40-live.py (frozen).",
     """Read %(L)s/quality/counters/c1-r40-live.py at %(F)s. Find: any path to TARGET_MET for a tool that does not resolve/convert (a do-nothing path), any clause that can pass vacuously, any place the counter trusts the tool's
output without cross-checking (e.g. labels from rows it can fabricate), any hole in the argv/no-write checks, determinism problems (REV-seeded generator, time, ordering), and a universal clause in the docstring that the counter does not
enumerate. For each, give a concrete tool or fixture that would exploit it and RUN it (write the exploit in %(W)s/w1/RevC1Counter/ and score it with --tool).""")
seat("RevC2Counter", "reviewer", "Attack counter c2-r40-forms-entry.py (frozen).",
     """Read %(L)s/quality/counters/c2-r40-forms-entry.py at %(F)s and the controls harness. Build and score (in `D=$(mktemp -d)` git fixtures per the safety rules) at least 6 NEW mutants of the admitted fixture
that the 20 shipped mutants do not cover (e.g. receipt carries the sha but not on a line of its own, forms/labels lines present in the receipt but with different spacing than the entry copy, two own-work new rows, `used-by` as a
substring of a longer path, quote 2 words, README row inside a code fence) and report which pass wrongly. Each exploit that passes is a finding.""")
seat("RevFreezeOrder", "reviewer", "Attack the freeze: nothing in it is data, everything declared is complete.",
     """Compare `git -C %(L)s show --stat %(F)s` with registration.md: every counter, control, receipt and the capture named there is in the commit; no delivered tool, entry, registry row or Gate line is in it; run the
criterion-64 style check: every counter path the registration names exists at %(F)s and the counting commands in registration.md run as written against the base (paste outputs). Check the registration for universal clauses
("all", "every", "no harm anywhere") the counters do not enumerate, and for after-states that are not one concrete value.""")
seat("RevModelVsSource", "reviewer", "Attack the counter's reference model against the upstream sources.",
     """Fetch hyprlang v0.6.8 src/config.cpp and Hyprland efb5099 ComplexDataTypes.hpp / ConfigManager.cpp (raw.githubusercontent.com). Check line by line that `hl_int`, `gradient_text` (incl. the inherited-angle rule), `gap_text`
and WEIGHTS in %(L)s/quality/counters/c1-r40-live.py match the C++: rounding of alpha (std::round * 255 then uint8 cast), the rgba comma form precedence over the 8-hex form, `starts_with("on")` catching spellings like `only`, negative
numbers, isNumber(...) rules, `no` prefix catching `normal`/`north` etc. List every place the Python model and the source differ, each with line numbers on both sides.""")
seat("RevHostCensus", "reviewer", "Independent re-derivation of the host census.",
     """Without the L1's tool, write your own throwaway resolver in /tmp (hyprlang rules: depth-first source, last declarer wins, variables) OR use `hyprctl getoption -j` plus grep over the config trees, and independently decide for the 70
keys of `python3 -I %(L)s/tools/mado-options.py --home $HOME`: does live equal the last declared value after host conversion? Report your own counts (agree / differ) and list the keys where you disagree with the provisional census (62 / 8 / 0).
Save script and outputs in %(W)s/w1/RevHostCensus/.""")
seat("RevAngleClaim", "reviewer", "Attack the angle-inheritance claim (the host finding).",
     """The claim: the gradient handler leaves `m_angle` untouched when a redeclaration has no `deg` token, so a later declarer inherits the earlier declarer's angle. Verify it from the C++ (ConfigManager.cpp handler + the
persistence of `*data` across calls in hyprlang: how CConfig stores/reuses the custom value's data pointer; read hyprlang v0.6.8 src/config.cpp custom-value handling) and from the host (`hyprctl getoption -j general:col.active_border`
vs the declarer chain). Try to REFUTE it: find a host key where an earlier declarer had an angle and the last has none but live shows 0deg, or the reverse. State what would falsify it and whether the evidence does.""")
seat("RevSeparability", "reviewer", "Attack separability and axis naming of the two claims.",
     """Judge registration.md against the shokunin protocol (/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/AXES.md and PROTOCOL.md claim-sizing rules): are C1 and C2 causally separable (can each verify without the other
having landed? run the counters against synthetic states), do they name distinct axes by the surface the round changes (not by the number produced), does C2's counter count rows a sourceless fixture also counts (quality-not-coverage trap),
is a do-nothing control present for each. Report each objection with the rule's text.""")
seat("RevToolSafety", "reviewer", "Attack the reference/BASE tool's read-only discipline for `--live`.",
     """Review %(W)s/c1/ctl-ref-tool.py.txt `native_query`/`merge_live`: the program path comes from `--hyprctl`, keys from the config tree and `--probe`. Find command-injection or argument-injection routes (a config key beginning with `-`, a key with
whitespace/newline, a key from a hostile config, environment influence, timeouts, huge replies, unbounded output, a `--hyprctl` that is a directory), and any way the tool could run a verb other than `getoption -j KEY`. Write exploit
attempts against a stub in /tmp and report each result.""")

# -------------------------------------------------------------- critics (4)
seat("CritC1Cheat", "critic", "Build the cheapest cheat for C1.",
     """Write the cheapest tool that scores TARGET_MET on %(L)s/quality/counters/c1-r40-live.py WITHOUT truly converting values from native forms (e.g. one that reads the generated config and echoes the stub's reply table, or memorises the
conversion outputs per REV). Score it with --tool and the committed capture. If it passes, the counter is wrong - say which clause to repair and how. If you cannot, say what each attempt tripped on.""")
seat("CritC2Cheat", "critic", "Build the cheapest cheat for C2.",
     """In a `D=$(mktemp -d)` git fixture (rules above) build the cheapest set that scores admitted=1/1 on %(L)s/quality/counters/c2-r40-forms-entry.py without any real source being opened (invented receipts, a dummy tool of 3 lines).
It is the declared residual; the question is how cheap, and whether any CHEAPER path than the declared residual exists (e.g. reusing round-39 receipts, reusing held rows as the 'new' ids).""")
seat("CritGeneratorCoverage", "critic", "Attack the generator: which real spellings/forms can a wrong tool get right on it?",
     """List the spelling classes in the host's real config trees (grep the default/user/theme/toggle values per type) and the classes the generator emits. Name every real class the generator never emits (e.g. `rgba(r,g,b,a)` with alpha not
exactly representable, `0x` hex in a gradient, 4-value gaps with negatives, float with exponent, int options spelled `1.0`, vec2/strings with spaces) and for each write a tool mutation that is wrong only on that class and show it still scores 13/13.""")
seat("CritClaimWording", "critic", "Attack the wording of the claims for overreach.",
     """Read registration.md and look for statements the counters do not verify (e.g. 'host census 62/8/0', 'inherits the angle', 'reaches 13/13 so the fixtures are reachable'), universal clauses, a residual that understates, or an after-state
that a later reading could narrow. Propose the exact edit for each (as text) but do not edit the file.""")

# ------------------------------------------------------- mutation-testers (4)
seat("MutC1Controls", "mutation-tester", "Mutate the reference tool beyond the 16 shipped mutants.",
     """Write >=10 NEW single-defect mutants of %(W)s/c1/ctl-ref-tool.py.txt (e.g. alpha rounded by int() instead of round(), prefix test `startswith('on')` removed, `rgb(` comma form requires 3 ints, gradient angle parsed with float, font weight lower-case dropped, probe de-duplication dropped, non-zero hyprctl status ignored only for probes, `no such option` matched by substring, JSON reply with extra whitespace rejected) and score each with `python3 -I %(L)s/quality/counters/c1-r40-live.py --repo %(L)s --rev %(F)s --tool <mutant>`. A mutant at 13/13 is a SURVIVOR: list each with the one-line change and what spelling/path would kill it.""")
seat("MutC2Controls", "mutation-tester", "Mutate the C2 counter itself.",
     """Copy %(L)s/quality/counters/c2-r40-forms-entry.py to /tmp and mutate ONE rule at a time (drop clause g, loosen quote word cap to 40, accept `candidate` status, accept opened != date, skip held-row byte-equality, skip the sha compare, ignore lesson path)
then run %(W)s/ctl/run-c2-controls.py against each mutant counter (edit its COUNTER path in a /tmp copy of the harness). A mutant counter that still gets 21/21 is a control gap: report which shipped control should have caught it and does not.""")
seat("MutSelftestFixtures", "mutation-tester", "Mutation-test the base tool's selftest against live-merge defects (preparation for the delivered selftest).",
     """Take the reference tool %(W)s/c1/ctl-ref-tool.py.txt and its own `--selftest` (71 base assertions). Apply the 16 mutants listed in %(W)s/ctl/run-c1-controls.py MUTANTS and run each mutant's `--selftest`: which mutants does the 71-assertion selftest already kill (none are expected, since the base selftest predates `--live`)? List the survivors: each one is a requirement for an assertion the delivered selftest must add.""")
seat("MutAxisGates", "mutation-tester", "Mutation-test the axis/index gates the harm watch relies on.",
     """The harm watch relies on `quality/check-index.py` and `quality/check-axis-scores.py`. In a sandbox clone (rules above) add a fake knowledge entry without an index row and check check-index fails; delete a README row and check it fails;
change a published axis score and check check-axis-scores reports a mismatch. Report each mutation, command, output and exit code. A gate that does not fail is a finding.""")

# --------------------------------------------------------------- sentinels (2)
seat("SentLiveVerbs", "sentinel", "Security review of the `--live` verb surface.",
     """Review the reference tool and the stub contract as a security reviewer: what can the tool execute (path from `--hyprctl`), what influences the child's environment (inherit? HYPRLAND_INSTANCE_SIGNATURE, PATH), is `getoption -j KEY` safe for any KEY
a hostile config can create (keys come from files the operator may not fully control: `source =` of an absolute path), output size limits, timeouts. Produce a short risk table with severity and the exact mitigation the delivered tool should carry.""")
seat("SentEvidenceLeak", "sentinel", "Review round evidence for secret-shaped or host-private leakage.",
     """The round commits host receipts (native capture, census, host reads of waybar/ai-usage). Scan %(W)s/ (as it exists while you work; re-scan at the end) and the candidate sources in /home/vgpnk/Projects/shokuknow/merge/mado/ for tokens, API keys, emails, absolute private paths beyond
/home/vgpnk, session ids, and the ai-usage cache's content. Report file:line and the redaction needed, never print a secret value (shape-only).""")

# -------------------------------------------------------------- connectors (5)
seat("ConnCrossClaim", "connector", "Cross-claim pattern finder.",
     """Find places where C1 and C2 touch the same bytes or concepts (the capture, the tool sha, the census lines, angle inheritance) and any ordering hazard when the L1 lands them (e.g. the C2 own-work receipt must name the sha of the tool committed at the data
commit; the entry must repeat the receipt's two count lines verbatim; the C1 counter's clause k reads the capture at REV). Produce the ordered integration checklist the L1 should follow, with the exact commands.""")
seat("ConnSiblingOverlap", "connector", "Sibling-lane overlap scan (read-only).",
     """Read /home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md headers and the fleet MISSION/AXES to find sibling lanes that could own the getoption/option-table surface or the Waybar producers (tsukuroi, mori, kama, tameshi ...). Report any overlap with mado's `--live`
verb or the K1/K2 assimilation scope with file:line evidence. Never write outside your seat dir.""")
seat("ConnEvidenceResolve", "connector", "Evidence-pointer resolver for the claims.",
     """List every evidence pointer the registration and the counters' docstrings cite (paths, commits, line numbers, URLs) and check each resolves at %(F)s: `git cat-file -e`, file:line existence, URL HTTP status (HEAD only). Report unresolved ones.""")
seat("ConnSourcePatterns", "connector", "Cross-source pattern finder for the C2 entry.",
     """Across the held entries (config-option-table-r39.md, hyprctl-verification-layer.md, hyprctl-flags-r28.md, dispatcher-surface-and-request-grammar-r26.md) and the round-40 candidate facts, find overlaps and contradictions about `getoption` replies,
`set` semantics and label vocabulary (agreement / agreement* / mismatch / config-only / live-default). Report where the new entry must supersede, cite or amend (never rewrite) a held statement, with file:line pointers.""")
seat("ConnRunState", "connector", "Run-state and inherited-state scan.",
     """List uncommitted/untracked state in the lane (git status read-only), inherited files not authored by this round (operator sweeps, round-*-aggregator-*, round-39-verifier-spotcheck.md), the open `corpus/lessons/operator-*.md` teachings and whether QUALITY.md/SKILL.md reflects each (grep), and the round-39 spot-check routed items D1-D3 with their status. Report.""")

# ----------------------------------------------------------------- scouts (6)
seat("ScoutOptionTypes", "scout", "Option types in the host's ConfigValues.cpp.",
     """Fetch src/config/values/ConfigValues.cpp at efb5099 and list the registered option TYPES (MS<Gradient>, MS<Bool>, MS<Float>, MS<Int>, MS<StringValue>, MS<Vec2> ...) with counts and the getoption JSON form each type produces per `src/debug/HyprCtl.cpp`
(getoption handler; line numbers). Report any type whose reply form is not int|float|str|custom, with the HyprCtl.cpp lines.""")
seat("ScoutGetoptionHandler", "scout", "HyprCtl.cpp getoption handler.",
     """In Hyprland efb5099 src/debug/HyprCtl.cpp locate the getoption handler (JSON branch and text branch): exact output format strings, the `no such option` path and its exit status, the `set` field's meaning, how complex types print. Report with quotes (<=25 words) and line numbers.""")
seat("ScoutHeldCoverage", "scout", "Held coverage of the C2 ground.",
     """grep the lane corpus (knowledge/*.md, SOURCES.md, lessons) for getoption, `custom`, `"set"`, gradient, deg, `no such option`, `agreement*`, config-option-table-r39. Report what is already held, so C2's entry adds new ground only; list the exact overlap lines.""")
seat("ScoutK1K2Held", "scout", "Held coverage for the assimilation candidates K1/K2.",
     """For each fact of /home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/host-bar-producers-r28.md and host-producer-outputs-r29.md (read-only) find whether the lane already holds it (waybar-walker-semantics.md, waybar-walker-plane.md, config-health-report-r3.md,
idle-lock-offered-in-the-bar-r15.md, waybar-observation-boundaries-r16.md). Table: fact | held? | where (file:line) | new ground?""")
seat("ScoutMergeRest", "scout", "Survey the rest of the mado package for the NEXT round (read-only).",
     """Read /home/vgpnk/Projects/shokuknow/merge/mado/MERGE-REPORT.md and list the knowledge entries not yet adopted by the lane (compare with %(L)s/corpus/knowledge/), grouped by theme, with the PROVINCE.md scope verdict per theme in one line each (refuse zh/ja-localization channel material per PROVINCE.md). Name the best next theme and why.""")
seat("ScoutHyprctlDocs", "scout", "Official documentation of `hyprctl getoption` for the host era.",
     """Open the 0.54.0/0.56.0 wiki pages on Using hyprctl (wiki.hypr.land/<ver>/Configuring/Advanced-and-Cool/Using-hyprctl/) and report what each documents about `getoption` (flags, JSON, set field), with <=25-word located quotes and HTTP status/date. Compare with the lane's held row S016.""")

# ------------------------------------------------------------- revengers (2)
seat("RevengerGetoptionFormat", "revenger", "Reverse-engineer why the base `--getoption FILE` format is not the compositor's.",
     """The BASE tool's `--getoption FILE` expects `{key: {value, custom_type, set}}` - not the native reply. Trace the round-39 history (git log -S, lessons, the wave's seat reports under .ufo/waves/round-39/) to find where that format came from, who normalised the dump, and whether any held entry
(hyprctl-verification-layer.md `agreement`/`live-default` pairs) used a different normalisation. Report the original intent and any held statement the native forms contradict.""")
seat("RevengerNaiveMismatch", "revenger", "Reconstruct the 14-of-70 naive mismatch and what it would have taught a reader.",
     """Reproduce the naive run: normalise the native replies to the base `--getoption` format and run the BASE tool. List the 14 mismatch rows with the cause class of each (colour rgb/rgba vs ARGB, bool prose `yes, please :)`, weight names, gradient angle, int-colour forms). Report what a reader
would wrongly conclude without the conversion table.""")

import collections as _c; print(len(items), dict(_c.Counter(i["role"] for i in items)))
assert len(items) == 64, len(items)
spec = {"wave": "w1", "context": CONTEXT, "reportDir": ".ufo/waves/round-40/w1",
        "items": items}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "w1-spec.json")
with open(out, "w") as fh:
    json.dump(spec, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
import collections
print(len(items), dict(collections.Counter(i["role"] for i in items)))
