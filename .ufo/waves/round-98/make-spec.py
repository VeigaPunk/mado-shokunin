#!/usr/bin/env python3
"""Build the round-98 w1 wave spec (mado, hyaku run 15)."""
import json

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
W = LANE + "/.ufo/waves/round-98"
DECL = W + "/claims-declaration-r98.md"
BASE = "35f3ce808788b11c063309b1b5ad0192754795ea"

CONTEXT = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim - let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

Round mado 98 (hyaku run 15, attempt 1), ONE v1 wave w1, 11 seats (build + falsifiers). Lane root (absolute): [[LANE]]. L1 MadoR98 holds the planner seat and integrates everything after this wave settles. Base revision [[BASE]] (branch master).
READ FIRST, it is the contract you build for or attack: [[DECL]]. The predicate sentences there are frozen by the L1 after this wave; you may attack them, never widen them. Read also [[LANE]]/corpus/QUALITY.md (160-169), [[LANE]]/SKILL.md (the registry table near the end), [[LANE]]/corpus/SOURCES.md (rows S504-S527 for the MIME plane) and [[LANE]]/corpus/lessons/round-97.md.
SOURCES: the L1's round-98 fetch receipt is [[W]]/receipts/sources-open-r98.txt and the fetched bytes are in [[W]]/fetch/ (gdesktopappinfo.c, gshell.c, exec-variables.html). Use ONLY rows already in the registry or URLs the L1 opened this round. Any other URL you cite must be fetched with `curl -sSL -o <file> -w '%{http_code} %{url_effective}'` and counts only at HTTP 200 (QUALITY 164); a 301 is a transport event, never the page.
Write scope: only your own files (named in your item), your report under [[W]]/w1/, and - where your item says so - a receipt or control under [[W]]/receipts/ or [[W]]/controls/. Every `Report:` trailer path is relative to [[LANE]] - write it at [[LANE]]/<that path>. Never write tools/, quality/, corpus/, the git index, jj state, the fleet repo or a sibling lane; the L1 lands every committed artifact through the lane helper. Seats never commit, push, or run a mutating git/jj command anywhere. Never run `agent://all`.
Scratch: S=$HYAKU_SCRATCH/mado-r98/<YourName> (HYAKU_SCRATCH defaults to /fast/scratch/hyaku; `mkdir -p` it and pass it explicitly, never rely on an inherited TMPDIR). /tmp only for files under 50 MB. Delete your scratch dir before you yield (`trap 'rm -rf -- "$S"' EXIT`; copy receipts into the wave dir first).
Tooling: you may install or upgrade tools that help the task - read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate, record tool/version/channel/reason in your report). ALL pacman transactions are PAUSED host-wide (mado r15 libinput incident): install via `uv tool`/`npx`/an official binary in ~/.local/bin, or file an L0 question; never `-Sy`, `-Syu`, `-U`, `-R`, downgrade or restart a host service. Never mutate host sysctls, never sudo.
Read-only by construction: every probe is read-only; no compositor mutation, no config write, no service restart, no network beyond the fetch list. NEVER launch a host application: the only process a seat may start is the fixture probe child of a case root it built itself (`gio launch <case-root desktop> <case-root file>`), and only under the seat's scratch dir. Never write ~/.config, never read ~/.ssh, ~/.gnupg, agent.db or any credential material.
Structural rules for any Python you write (QUALITY 162/165): stdlib only; no subprocess, socket, network or ctypes beyond libc in the *submitted candidate* (the oracle harness, the counter and the gate may spawn `gio` / the probe - they are instruments, not candidates; say which is which in your report); no shelling out to `file`, `gio`, `xdg-mime` or any library to answer a modelled question in the candidate. ASCII only in committed artifacts.
Facts of the ground (measured this round): glib2 2.90.1-1; `/usr/bin/gio` is the C1 oracle (`gio launch DESKTOP-FILE [FILE-ARG...]`); the probe child records its own argv. The desktop file's Exec line is expanded by gdesktopappinfo.c:2700-2750 then parsed by g_shell_parse_argv (gshell.c).
CASE HYGIENE: never pass an empty or unchecked variable to `git -C`; any fixture repo is `D=$(mktemp -d) && git -C "$D" init -q` and every later git call names `-C "$D"`; assert `git -C "$D" rev-parse --show-toplevel` equals `$D` before any mutating git command. Never commit anywhere.

## Shared contract 1 - the C1 candidate's CLI

`[[LANE]]/tools/mado-execargv.py` (target path; the in-wave draft is [[W]]/build/mado-execargv.py, owned by R98MExecTool):

```
mado-execargv.py DESKTOP [FILE...] [--json]
mado-execargv.py --selftest
```

It models GIO 2.90.1's launch-argv construction for one desktop file and a list of arguments:
`expand_application_parameters` (gdesktopappinfo.c:2701-2746), `expand_macro` (:2580-2700),
`expand_macro_single` (:2507-2555), `expand_macro_uri` (:2557-2578), then `g_shell_parse_argv`
(gshell.c). Output on stdout:

```
MADO_EXECARGV: argc=3
ARGV[0]=/abs/probe
ARGV[1]=one
ARGV[2]=/abs/f1.txt
```

exit 0 on success; 2 on a refusal with one line `MADO_EXECARGV: ERROR <cause> detail=<...>` (causes:
`no-exec` - the desktop file has no Exec key; `desktop-file` - not a key file / no [Desktop Entry]
group / no Type=Application; `exec-parse` - g_shell_parse_argv would fail). `--json` prints one JSON
object `{"argc":N,"argv":[...]}` (or `{"error":"<cause>","detail":"..."}`). `--selftest` runs its own
checks over fixtures it builds under a temp dir and prints `MADO_EXECARGV_SELFTEST: checks=N failed=M`
(exit 0 green / 1 failed).

## Shared contract 2 - the C1 case file

JSON `{"version":1,"oracle":"gio launch + probe child argv","gio_sha256":"<sha of /usr/bin/gio>","glib2":"2.90.1-1","classes":[<the 16 class names in the declaration's order>],"cases":[...]}`.
Case: `{"id":"<class>-NN-<slug>","class":"<one of the 16>","desktop":{"Name":"...","Icon":"<str>"|null,"Type":"Application","Exec":"...","Path":"<rel or null>","Terminal":true|false|null,"Hidden":true|false|null},"args":[{"kind":"file","path":"<rel>"}|{"kind":"uri","uri":"<abs uri>"}],"files":{"<rel>":"<base64 bytes>"},"expect":{"argc":N,"argv":["<argv0>",...]}}`.
Rules: `{probe}` in `Exec` is substituted with the absolute path of the probe script the counter
writes into the case root (`probe.sh`, mode 0755, records `ARGC=<n>` then `A<i>=<value>` lines to
`<probe>.out`); `{root}` in any path is the case root. `files` keys ending `/` are directories.
Every `expect` is recorded by `/usr/bin/gio` at the freeze (build the root, run
`env -i LC_ALL=C HOME={root}/h PATH=/usr/bin:/bin gio launch <desktop> <args...>`, read the probe's
`.out`, map it to `{"argc","argv"}`), never written by the author. A case whose `gio launch` exits
nonzero or writes no `.out` is a REFUSAL case: `expect` is `{"error":"<the cause the tool must
print>"}` and the tool must exit 2. 16 classes, >=3 cases each, >=60 cases total.

## Shared contract 3 - the C2 gate's CLI and finding format

`[[LANE]]/quality/check-sources-readback.py` (target path; in-wave draft [[W]]/build/check-sources-readback.py):

```
check-sources-readback.py --repo DIR [--json]
check-sources-readback.py --selftest
```

Reads `<DIR>/corpus/SOURCES.md` (rows with 0-3 leading spaces, 11 columns) and every
`<DIR>/corpus/knowledge/*.md` entry's `source:` frontmatter line. Findings, one per line:
`SOURCES_READBACK: FINDING <rule> <id> <detail>` with rules `R1 recheck-path`,
`R2 usedby-outside-corpus`, `R3 usedby-missing`, `R4 entry-cites-unacknowledged`,
`R5 entry-cites-missing-row`, `R6 duplicate-id`. Result line:
`SOURCES_READBACK: rows=N entries=M findings=K`. Exit 0 clean / 1 findings / 2 setup (missing
registry, unreadable entry). `--json` prints `{"rows":N,"entries":M,"findings":[{"rule","id","detail"}]}`.
`--selftest` builds fixture registries under a temp dir and prints
`SOURCES_READBACK_SELFTEST: checks=N failed=M` plus one `SOURCES_READBACK_SELFTEST_FAIL: <id>` per
failing check; >=10 stable check ids (never line numbers).

## Shared contract 4 - the counter selftest schema

A counter's `--selftest` mode runs its own checks over committed fixtures and asserts, per check, an
exit code and a stable finding id; it prints `MADO_COUNTER_SELFTEST_FAIL: <id>` per failing check and
`MADO_COUNTER_SELFTEST: checks=N failed=0`, exit 0 green / 1 failed / 2 could-not-evaluate.
"""


def item(name, role, body):
    for k, v in (("[[LANE]]", LANE), ("[[W]]", W), ("[[DECL]]", DECL), ("[[BASE]]", BASE)):
        body = body.replace(k, v)
    return {"name": name, "role": role, "prompt": body}


items = []

items.append(item("R98MScoutExec", "scout", """Own: [[W]]/w1/R98MScoutExec.md and [[W]]/receipts/scout-exec-r98.txt. S=$HYAKU_SCRATCH/mado-r98/R98MScoutExec.
Reconnaissance of the C1 surface, read-only, no candidate edits. 1. Re-open the three fetched sources in [[W]]/fetch/ and verify the receipt's digests (sha256) and the located quotes. 2. From gdesktopappinfo.c, list every rule of the launch-argv construction with file:line: the `%` walk (`expand_application_parameters`), each `expand_macro` case (`u f d n U F D N i c k m %`, and the absent default), the `force_file_uri`/`#` rule, the no-substitution `%f` append, and the `g_shell_parse_argv` call. 3. From gshell.c, list the tokenizer's rules with file:line (whitespace split, single quotes, double quotes and which backslash escapes they honour, backslash outside quotes, unterminated quote, empty argument) and `g_shell_quote`'s rule. 4. From exec-variables.html, quote the documented field codes and note every place GLib 2.90.1 departs from the document (start with `%d`/`%n`/`%N` documented Deprecated but implemented, and the `%i` "two arguments" wording). 5. Enumerate the reachable edge classes and map each to the declaration's 16 classes; name any class the declaration misses, with a probe that shows it is reachable (`gio launch` on a case-root fixture you build under S; never a host application). 6. Attack the declaration's C1 rules 1-5: name every sentence the source contradicts, with the line. Report a rule table (rule -> line -> observed) and a class table (class -> probe -> observed argv)."""))

items.append(item("R98MExecOracle", "executor", """Own: [[W]]/controls/execargv-probe-r98.py (the oracle case builder), [[W]]/controls/execargv-cases-r98.json (the frozen case draft), [[W]]/controls/execargv-fresh-r98.py (the fresh generator) and [[W]]/w1/R98MExecOracle.md. S=$HYAKU_SCRATCH/mado-r98/R98MExecOracle.
Build the C1 oracle per Shared contract 2. 1. `execargv-probe-r98.py`: given a case dict, materialise the case root (files from base64, directories for keys ending '/', the probe script `probe.sh` 0755 that writes `ARGC=`/`A<i>=` to `$0.out`, the desktop file from the case's `desktop` block with `{probe}`/`{root}` substituted), run `env -i LC_ALL=C HOME=<root>/h PATH=/usr/bin:/bin /usr/bin/gio launch <desktop> <args...>` with a 10 s timeout, read the probe's `.out`, and print the case's `expect` (`{"argc","argv"}` or `{"error":"<cause>"}` when gio exits nonzero / writes nothing). Record `/usr/bin/gio` sha256 in the file header. 2. `execargv-cases-r98.json`: the 16 classes `plain f F u-file u-uri u-anchor U-mixed d n i c k pct bad quote path`, >=3 cases each, >=60 total, every `expect` produced by the builder (never hand-written). Cover: `%f` with 0/1/2 args; `%F` with 0/1/3; `%u` with a file arg, an http URI and a `file://...#frag` URI; `%U` mixed; `%i` with and without Icon; `%c` with a Name carrying a quote and a space; `%k`; `%%`, a trailing `%`, `%z`/`%q`; Exec quoting `"a b"`, `'a b'`, `a\\ b`, an unterminated quote (a refusal case); a file arg whose name carries a space and one carrying `'`; `%d`/`%n`; a no-field-code Exec with 2 args (only the first is used); a `Hidden=true` and a missing-Exec refusal case. 3. `execargv-fresh-r98.py`: `--seed HEX --dir D --out F --count N` builds N seeded fresh cases (random Exec patterns from the modelled grammar, random arg counts and names) under D and writes one JSON line per case with its oracle `expect`, labels measured at generation time. Report: the class census, the total, the gio pin, and a 12-case dry run of the generator."""))

items.append(item("R98MExecTool", "executor", """Own: [[W]]/build/mado-execargv.py (the C1 candidate draft) and [[W]]/w1/R98MExecTool.md. S=$HYAKU_SCRATCH/mado-r98/R98MExecTool.
Implement the candidate exactly to Shared contract 1 and the declaration's C1 rules 1-5. Stdlib only, no subprocess, no sibling import. Read the desktop file as bytes, decode UTF-8 with `surrogateescape`, parse the `[Desktop Entry]` group (key=value, `\\s`/`\\n`/`\\t`/`\\r`/`\\\\` unescapes, the first group only, a duplicate key keeps the first), then: walk the Exec line (a trailing `%` is literal; `%X` expands; every other byte is copied), expand each code exactly as `expand_macro` does (one-arg codes consume one argument and append `g_shell_quote(value)`; list codes consume all and space-join; `%u`/`%U` force the file path when the URI has a local path and no `#`; `%i` appends `--icon ` + quoted Icon; `%c` quoted Name; `%k` quoted desktop path; `%m` nothing; `%%` a literal `%`; unknown nothing), append ` ` + one `%f` expansion when no argument was consumed and arguments were given, then tokenize with the `g_shell_parse_argv` grammar (whitespace, single quotes literal, double quotes honouring `\\"` and `\\\\` only, backslash outside quotes, unterminated quote -> `exec-parse` refusal). `g_shell_quote` is always `'...'` with `'` -> `'\\''`. Refusals per contract 1. `--selftest` with >=12 stable checks over fixtures it builds under a temp dir. Report the rule-to-line map and a 20-case run against the oracle cases (the counter is R98MExecCounter's; use its case file draft if it exists, else your own probes)."""))

items.append(item("R98MExecCounter", "executor", """Own: [[W]]/build/c1-r98-execargv.py (the C1 counter draft) and [[W]]/w1/R98MExecCounter.md. S=$HYAKU_SCRATCH/mado-r98/R98MExecCounter.
Write the C1 counter to the declaration's predicate PRED-C1-r98-v1 exactly. argparse flags: `--repo --rev --base-rev --cases --expect-cases-sha256 --mutants --expect-mutants-sha256 --genseed --expect-genseed-sha256 --expect-tool-sha256 --expect-gio-sha256 --scratch-root`. Behaviour: (a) materialise the measured revision's `tools/mado-execargv.py` with `git show <rev>:<path>` into a scratch tree (never write the lane); verify its sha256 against the pin (`tool_pin=ok`), SETUP_ERROR on mismatch; (b) build every frozen case root under `--scratch-root` from the case file, run the candidate on each with `env -i PATH= LC_ALL=C HOME=<root>/h` (empty PATH, so no library can be shelled out to), compare `argc`/`argv` exactly, print `correct=<n>/<cases>` and one `MISMATCH <id> expected=... got=...` line per miss; (c) apply every mutant to a scratch copy, re-run over the frozen cases, a kill is a parsed wrong answer or a missing line (a crashing mutant is `crashed_not_killed`, not a kill), print `killed=<n>/<mutants>` and `class_kills=<k>/16`; (d) run the fresh generator at a measurement-time seed (`os.urandom`, or `MADO_R98_FRESH_SEED`), build its roots, score, print `fresh=<n>/<total> fresh_seed=<hex>`; (e) score the controls: a naive space-split model and a no-expansion model (both written by the counter itself, <=30 lines each) must score fewer than the total, and a memoriser (the frozen answers keyed by case id) must score 0 on the fresh leg; (f) run the candidate's `--selftest` and require `checks>=12 failed=0`; (g) `--selftest` mode per Shared contract 4 (>=10 stable ids). Result line `MADO_EXECARGV_COUNT: TARGET_MET|TARGET_MISSED rev=<rev> ...`; rc 0/1/2."""))

items.append(item("R98MExecGate", "executor", """Own: [[W]]/build/check-sources-readback.py (the C2 gate draft), [[W]]/build/c2-r98-sources-readback.py (the C2 counter draft), [[W]]/selftest-fixtures/readback/ (fixtures), [[W]]/controls/readback-planted/ (the planted-defect registries) and [[W]]/w1/R98MExecGate.md. S=$HYAKU_SCRATCH/mado-r98/R98MExecGate.
Build the C2 gate and counter per Shared contracts 3-4 and the declaration's PRED-C2-r98-v1. 1. Gate: parse the registry (0-3 leading spaces, 11 columns), parse every `corpus/knowledge/*.md` `source:` frontmatter line, implement R1-R6 exactly, `--json`, `--selftest` with >=10 stable ids, exit 0/1/2. 2. Counter: at `--base-rev` print `base_gate=absent` (`git cat-file -e <base>:quality/check-sources-readback.py`) and the counter's own independent R4 pass over the base registry (`base_mismatches=<n>` with the list); at `--rev` verify the gate pin, run the gate (`findings=0`, `rows`/`entries` equal the counter's own parse), re-run the independent R4 pass (`repaired == base_mismatches`), run the planted copies (one stripped used-by cell -> exactly one R4; one path in a recheck cell -> exactly one R1; one dangling used-by -> exactly one R3), and reject an always-clean stub gate (`stub_flagged`); run the fleet census `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` and require exit 0 (W-codes allowed); `--selftest` per contract 4. Result line `MADO_SOURCES_READBACK_COUNT: TARGET_MET|TARGET_MISSED ...`; rc 0/1/2. 3. Planted registries under `controls/readback-planted/` are copies of the base registry with the named single defect; commit them as evidence. Report the base mismatch list (the 23 ids/entries) and the planted controls' exact output."""))

items.append(item("R98MScribe", "scribe", """Own: [[W]]/w1/drafts/gio-exec-argv-r98.md (the entry draft), [[W]]/w1/drafts/sources-rows-r98.md (the row draft) and [[W]]/w1/R98MScribe.md. S=$HYAKU_SCRATCH/mado-r98/R98MScribe.
Draft the knowledge entry `corpus/knowledge/gio-exec-argv-r98.md` (target path; the L1 lands it) for the C1 surface, and the SOURCES rows it needs. 1. Read [[W]]/fetch/gdesktopappinfo.c, gshell.c, exec-variables.html and the declaration; every rule in the entry cites a located line (file:line + <=25-word quote) of one of them or an oracle-labelled probe row. 2. Structure: scope and provenance; the desktop-file read; the `%` walk; the field-code table (code -> line -> what it appends -> measured example); the `force_file_uri`/`#` rule; the no-substitution `%f` rule; `g_shell_quote`; the `g_shell_parse_argv` grammar; the refusals; the spec-vs-implementation deltas (`%d`/`%n`/`%N` deprecated but implemented, `%i` "two arguments", `%f` "single file even if multiple selected"); a measured-probe section (each row: command, observed argv); the named limits. 3. Row draft: one row for gdesktopappinfo.c (new scope on the file S518/S521/S505/S526 hold - a W04 duplicate URL is expected), one for gshell.c, one for the Desktop Entry Specification's Exec section (the S523/S525 pattern: locator, digest, size, HTTP status), and a new scope on S527 for `gio launch`. Each row: id placeholder, source, kind, tier, scope, anchor (file:line + digest), teaches (<=25 words), status `mined`, opened 2026-11-07, recheck `180d`, used-by `corpus/knowledge/gio-exec-argv-r98.md`. 4. Also draft the lesson's `## Gate` rows-touched block: which held rows gain the new entry in `used-by` (the C1 rows the entry cites). No measured cell you did not measure: mark the L1's receipt cells as `{L1}`."""))

items.append(item("R98MConnector", "connector", """Own: [[W]]/w1/R98MConnector.md and [[W]]/receipts/connector-sweep-r98.txt. S=$HYAKU_SCRATCH/mado-r98/R98MConnector.
Sibling-overlap scan and adjacency, read-only. 1. Read every `/home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md` (20 lanes) and grep each lane's `corpus/knowledge/` for the C1 surface: `Exec` field codes, `%f`/`%U`, `g_shell_parse_argv`, desktop-entry launch, `gio launch`. Report per lane: claims the surface / adjacent / silent, with the file:line. 2. Same for the C2 surface: a SOURCES read-back, registry citation consistency, `used-by` cells - does any sibling lane own it? 3. Cross-source pattern: does the desktop-entry spec's Exec grammar connect to a surface this lane already holds (the r91 default-application plane, r92 xdg-open's resolver, r94 name->type)? Name the join and what it now makes answerable (e.g. "which argv `xdg-open` would build for a file" vs "which file xdg-open would open"). 4. Report the frontier/adjacency verdict: is the C1 surface contested, and does the C2 gate duplicate a fleet instrument (`scripts/sources-census.sh`)? Quote the census's own E09/E11 lines to show what it does not check."""))

items.append(item("R98MReviewC1", "reviewer", """Own: [[W]]/w1/R98MReviewC1.md and [[W]]/receipts/review-c1-r98.txt. S=$HYAKU_SCRATCH/mado-r98/R98MReviewC1.
Attack C1 without editing the candidate. 1. Re-derive the oracle independently on >=20 cases (a sample across the 16 classes, chosen by id) by building the roots yourself from the frozen case file and running `env -i LC_ALL=C HOME=... PATH=/usr/bin:/bin /usr/bin/gio launch ...`; compare with the frozen `expect`; every mismatch is a finding. 2. Run the candidate on the same 20 and diff against the oracle. 3. Score the cheapest no-work controls yourself: a 20-line `Exec.split()` model and a no-expansion model, over the frozen cases; the declaration's control claim must be true (strictly fewer than the total). 4. Probe the predicate's attack surface: `%u` with a `file://` URI carrying `#`, `%U` mixed, `%f` with 2 args, a trailing `%`, `%z`, an unterminated quote, a Name carrying `'`, a file arg carrying a space, `Hidden=true`, a missing Exec; each probe: build the case, run gio and the candidate, report both. 5. Attack the counter's kill rule: is a crashing mutant counted as a kill? is a case whose gio run is nondeterministic frozen? Report every disagreement with the declaration's predicate sentence, and the exact sentence to change before the freeze."""))

items.append(item("R98MCriticC2", "critic", """Own: [[W]]/w1/R98MCriticC2.md and [[W]]/receipts/critic-c2-r98.txt. S=$HYAKU_SCRATCH/mado-r98/R98MCriticC2.
Falsify C2. 1. Re-derive the 23 base mismatches yourself with your own parser (independent of the counter's): list every id/entry pair; state whether each is a genuine read-back defect or a legitimate citation the rule should not require (a row cited in an entry's body but not its `source:` frontmatter is NOT a defect; a row cited in frontmatter and absent from used-by IS). 2. Attack the gate's rules: build fixture registries that should pass (a row with used-by `-`, a rejected row, a lesson-only used-by path, a row cited by a lesson) and ones that should fail (each of R1-R6); report every false positive and false negative. 3. Attack the counter's discrimination: does the always-clean stub get caught? does a gate that only implements R1 pass the planted R4? does the `repaired == base_mismatches` clause become vacuous if base_mismatches is 0? 4. Attack the do-nothing control: could a no-work round reach `findings=0` (e.g. by deleting the entries' `source:` lines instead of repairing the cells)? Name every loophole and the sentence to add before the freeze. 5. Check the declaration's C2 before-number against your own count; if it differs, say by how much and why."""))

items.append(item("R98MMutC1", "mutation-tester", """Own: [[W]]/controls/execargv-mutants-r98.json (the mutant draft) and [[W]]/w1/R98MMutC1.md. S=$HYAKU_SCRATCH/mado-r98/R98MMutC1.
Build the frozen mutant population against the C1 tool draft ([[W]]/build/mado-execargv.py): >=60 counted mutants, each `{"id","find","replace","class","expect":"kill"}` with `find` occurring exactly once in the non-selftest code, plus `not_observable` and `equivalents` lists, each with a written argument. Cover every one of the 16 classes with at least one counted mutant: one-arg vs list codes swapped, `%u` force_file_uri dropped, the `#` bypass dropped, the no-substitution `%f` append dropped, `%i`'s `--icon ` dropped, `%c`/`%k` quoting dropped, `%%` -> nothing, unknown code -> the literal `%X`, trailing `%` dropped, single-quote escaping wrong (`'` not `'\\''`), double-quote backslash handling, unterminated quote accepted, whitespace split on quoted spaces, `%d`/`%n` unimplemented, `Hidden` accepted, missing-Exec not refused, `exec-parse` not refused, argv[0] dropped. Prove each mutant kills: apply it to a scratch copy, run the candidate over the frozen cases, a kill is a parsed wrong answer (a crash is not a kill). Report the kill table, the class coverage, and every non-killer with its argument."""))

items.append(item("R98MMutC2", "mutation-tester", """Own: [[W]]/controls/readback-mutants-r98.json (the mutant draft) and [[W]]/w1/R98MMutC2.md. S=$HYAKU_SCRATCH/mado-r98/R98MMutC2.
Build the mutant population for the C2 gate ([[W]]/build/check-sources-readback.py): >=30 counted mutants, each `{"id","find","replace","rule","expect":"kill"}` with `find` occurring exactly once in the non-selftest code, plus `not_observable`/`equivalents` with arguments. Cover every rule R1-R6: the recheck-path test inverted, the `corpus/` prefix test dropped, the existence test dropped, the used-by membership test inverted, the frontmatter parser narrowed to the first id, the duplicate-id test dropped, the exit code 1 -> 0, the result-line count wrong, a finding line's rule token wrong. Prove each mutant kills: apply it to a scratch copy, run the gate over the committed registry AND over the planted-defect copies ([[W]]/controls/readback-planted/), a kill is a missing or wrong finding (a crash is not a kill). Also attack the counter: does it catch a gate whose `--selftest` prints green without running? Report the kill table per rule and every non-killer with its argument."""))

spec = {
    "wave": "w1",
    "reportDir": ".ufo/waves/round-98/w1",
    "maxLanes": 16,
    "context": CONTEXT,
    "items": items,
}
out = W + "/w1-spec.json"
with open(out, "w") as f:
    json.dump(spec, f, indent=1)
print(out, len(items), "items", sum(len(i["prompt"]) for i in items), "prompt bytes")
