# Seat MutC1Fixtures — w2 falsify (round 47): C1 fixture sensitivity

**Task:** make >= 20 one-rule mutants of the L1 reference
`.ufo/waves/round-47/l1-draft/mado-terminal.py`, beyond the 17 V-* controls of
`ctl/run-c1-controls.py`, score each with the frozen counter
`quality/counters/c1-r47-terminal.py` (fixed nonce 47) on freeze
`d7527d608ad2b2e3cc398fdde34db7947b254a1a`; survivors = rules the 190 fixtures + 150 nonce cases
do not exercise; propose (and verify with the pinned real script) a kill fixture for each.

**Result: 22 mutants made and scored (all patches assert 1:1, all compile, selftest preserved where
noted); 11 survived at nonce 47; 2 are equivalent mutants (no kill exists); 9 are genuine counter
blind spots, each demonstrated against the pinned resolver (sha256
89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac — also present as the host's
/usr/bin/xdg-terminal-exec, re-verified during every count by the counter's PIN_SHA256 check).**

Seat materials: `mutants.py` (definitions), `drive.py` (scoring harness), `verify.py` /
`verify_batch.py` / `probe.py` / `probe-explain-cache.py` (kill-verification harnesses),
`fixtures-proposed/*.json` (9 kill fixtures), `receipts/` (counter outputs per run + verify
outputs + probes), `results.json` (all verdicts, nonce 47 and 424242).

## Method (reproducible)

Scoring, one candidate per commit in a scratch clone (per the seat recipe; git only in scratch):

```
S=/fast/scratch/hyaku/mado-r47/MutC1Fixtures; D=$S/clone
git clone -q --shared --no-checkout /home/vgpnk/Projects/shokunin/mado-shokunin "$D"
test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"
git -C "$D" checkout -q --detach d7527d608ad2b2e3cc398fdde34db7947b254a1a
cp <candidate> "$D/tools/mado-terminal.py"
git -C "$D" add tools/mado-terminal.py
git -C "$D" -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m cand
TMPDIR=$S python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r47-terminal.py \
  --repo "$D" --rev HEAD --work $S/w --nonce 47
```

Baseline: pristine reference → `TARGET_MET` (fixtures=190/190 explained=190/190 generated=150/150
selftest=ok readonly=ok tool=present), rc 0, at nonce 47 and 424242 (receipts
`mut-REF-baseline.txt`, `mut-REF-baseline@424242.txt`).

Kill verification: the same counter sandbox (`Box`/`run_case` of the counter module) materializes the
proposed fixture at fresh roots and runs (a) the pinned resolver, (b) the pristine reference, (c) the
mutant; `ref_ok=True` (reference == oracle) and `mut_ok=False` (mutant != oracle) = KILLS (receipts
`verify-*.txt`). Probes for rules the fixture schema cannot express run the same sandbox with custom
env / chmod.

## Mutant table (22; one-rule, REF.replace(old,new,1))

Scored at nonce 47 (fixed) and again at 424242 for survivors. Source hash = sha256 of the mutated tool.

| id | rule undone (locator in reference) | @47 | @424242 | killed by |
|---|---|---|---|---|
| REF-baseline | — | **MET** | **MET** | — |
| I-SPLIT-IFS-TRAILING | `split_ifs` keeps trailing empty field (l1-draft:193-198) | MISSED | — | fixtures t8 (clause f+x), generated #42 |
| I-READSPLIT-APPID | `--app-id=`/`--title=`/`--dir=` value parsed with plain split (run_print) | **SURVIVED** | SURVIVED | gap (killed by proposed k-readsplit-appid) |
| I-TOK-QUOTED-ESC-NONSPECIAL | tokenizer keeps `\x` literal inside double quotes (tokenize) | **SURVIVED** | SURVIVED | gap (killed by k-tok-quoted-esc-nonspecial2) |
| I-EXPAND-UNKNOWN-KEEP | expand_str keeps backslash before unknown escape (expand_str) | MISSED | — | fixture t11 (clause f+x) |
| I-NOTSHOWIN-LISTED | NotShowIn applied to listed entries too (check_entry_key) | MISSED | — | generated #34 |
| I-TRYEXEC-ABS-CWD | absolute TryExec resolved via cwd-join | **SURVIVED** | SURVIVED | equivalent mutant (`os.path.join(a, abs)` returns abs) |
| I-PATH-EMPTY-SKIP | empty PATH element doesn't mean cwd (command_v) | **SURVIVED** | SURVIVED | gap (probe; unkillable by fixture schema) |
| I-ALIAS-EXCLUDED-UNREG | excluded-id alias not registered (find_entry_paths) | MISSED | — | selftest + fixtures f4/l1-exclusion (clause s/f/x) |
| I-CONTENT-LAST-NL | --print-content drops final newline (run_print) | MISSED | — | fixtures + generated #16 |
| I-TEST-WITH-PRINT | --test bypasses print-option early return (run_print) | **SURVIVED** | SURVIVED | gap (killed by k-test-with-print) |
| I-PRINTCMD-EMPTY-DELIM | empty `--print-cmd=` delimiter = empty, not newline | **SURVIVED** | SURVIVED | gap (killed by k-printcmd-empty-delim) |
| I-READSPLIT-MULTI-TRAILING | read_split drops trailing delimiter whenever at end (read_split) | MISSED | — | generated #72 |
| I-ACTION-ID-UNDERSCORE | action id allows `_` (valid_action_id) | MISSED | — | generated #96 |
| I-COMMANDV-FUNCTIONS | script functions invisible to command -v (command_v) | **SURVIVED** | MISSED | gap at 47; generated kills at 424242 (nonce-fragile) |
| I-EXPLAIN-CACHE-SWAP | explain `cache=` field flipped | **SURVIVED** | SURVIVED | gap (probe; clause x never reads cache=) |
| I-LIST-UNREADABLE-SKIP | unreadable list skipped instead of errexit exit 1 (read_config_paths) | **SURVIVED** | SURVIVED | gap (probe; schema has no file mode) |
| I-TOK-SQUOTE-IN-DQUOTE | single quote inside double quotes ends tokenizing (tokenize) | **SURVIVED** | SURVIVED | gap (killed by k-tok-squote-in-dquote) |
| I-EXECARG-EQ-ONLY | option loop breaks only on `-e`, not on the entry's execarg | **SURVIVED** | SURVIVED | equivalent mutant (`-x` is dropped as unknown option anyway) |
| I-HOLD-IGNORE-FLAG | hold arg inserted even without `--hold` (run_print) | MISSED | — | clause x (fixtures s6/v3/v4) |
| I-EXECARG-EMPTY-INSERT | empty execarg still inserted (run_print) | MISSED | — | generated #35 |
| I-DESKTOP-ORDER-REV | desktop list order reversed (make_paths) | MISSED | — | fixtures c1/c2 (clause x) + generated #47 |
| I-DIRECTIVE-LAST-WINS | /execarg_compat|strict last-wins (read_config_paths) | MISSED | — | generated #28 |

Killed mutants prove the counter DOES exercise those rules (clause as listed). The 11 survivors at
nonce 47 are the coverage findings.

## Findings: rules the counter does not exercise (9 genuine)

Each finding: rule, what the counter misses, the verified kill.

### 1. `--app-id=`/`--title=`/`--dir=` value with a trailing `=` (I-READSPLIT-APPID)
Reference uses `read_split` (bash `IFS== read -r` semantics: a trailing `=` with no other `=` is
dropped). Mutant uses plain split. Counter missed it (no fixture/generated argv has `--app-id=x=`;
only `--title=x=` in the selftest, which drives clause s, plus... it is not in the 190 fixtures).
Kill (verified): `fixtures-proposed/k-readsplit-appid.json` — `X-TerminalArgAppId=--class=` entry +
`--app-id=x=`:
```
VERIFY k-readsplit-appid
  oracle rc=0 stdout='foot\n--class=x\n'
  ref_ok=True  mut_ok=False  mut_why=oracle=(0, 'foot\n--class=x\n') tool=(0, 'foot\n--class=x=\n')
```
### 2. Tokenizer quoted escape of a non-special char (I-TOK-QUOTED-ESC-NONSPECIAL)
Inside double quotes, `\s` (surviving expand_str as `\\s` in the entry) must yield `s`, not `\s`.
The counter never feeds a backslash that survives expand_str into the tokenizer. Kill (verified):
`k-tok-quoted-esc-nonspecial2.json` (Exec=`foot "a\\sb"`):
```
VERIFY k-tok-quoted-esc-nonspecial2
  oracle rc=0 stdout='foot\nasb\n'  ref_ok=True  mut_ok=False
```
### 3. `--test` combined with print options (I-TEST-WITH-PRINT)
The real script prints the id and returns; a reordered test-print writes the test block too. Kill
(verified): `k-test-with-print.json`:
```
VERIFY k-test-with-print
  oracle rc=0 stdout='foot.desktop\n'  ref_ok=True  mut_ok=False
```
### 4. Empty `--print-cmd=` delimiter (I-PRINTCMD-EMPTY-DELIM)
v0.14.3 prints words separated by newlines (empty delimiter behaves as `\n`); the mutant concatenates.
Kill (verified): `k-printcmd-empty-delim.json`:
```
VERIFY k-printcmd-empty-delim
  oracle rc=0 stdout='foot\n-e\na\nb'  ref_ok=True  mut_ok=False  tool='foot-eab'
```
### 5. `command -v` over script functions (I-COMMANDV-FUNCTIONS) — nonce-fragile
TryExec=read_cache (a script function) passes; with functions removed it fails. At nonce 47 the
150 generated cases never hit it (survived); at 424242 they do (MISSED). Kill (verified):
`k-commandv-functions.json`:
```
VERIFY k-commandv-functions
  oracle rc=0 stdout='foot.desktop\n'  ref_ok=True  mut_ok=False  tool=(1, '')
```
### 6. Single quote inside double quotes (I-TOK-SQUOTE-IN-DQUOTE)
`Exec=foot "a'b"` → word `a'b`; the mutant's tokenizer bails. Kill (verified): `k-tok-squote-in-dquote.json`:
```
VERIFY k-tok-squote-in-dquote
  oracle rc=0 stdout="foot\na'b\n"  ref_ok=True  mut_ok=False  tool="foot\na\n"
```
### 7. PATH empty element = cwd (I-PATH-EMPTY-SKIP) — harness gap
`command -v` must consult cwd for an empty PATH element. **The counter can never see this:** `case_env`
force-sets PATH=`<root>/bin:/oracle/bin` for every fixture/generated case. Probe (verified, same sandbox,
custom env PATH=`<root>/bin::/oracle/bin`, executable `./foot` at cwd):
```
PROBE PATH-EMPTY: oracle=(0, 'foot.desktop\n') ref=(0, 'foot.desktop\n') mutant=(1, '')
```
Fix proposal: let `case_env` honor a fixture-supplied PATH, or add a PATH field to the fixture schema.
### 8. Unreadable list file ⇒ errexit exit 1 (I-LIST-UNREADABLE-SKIP) — schema gap
The fixture schema has no file-mode field (`materialize` writes everything 0644; only execs get 0755),
so an unreadable `*xdg-terminals.list` cannot be built. Probe (verified, list chmod 000):
```
PROBE2B LIST-UNREADABLE: oracle=(1, '') ref=(1, '') mutant=(0, 'foot.desktop\n')
```
Fix proposal: a `mode` field (or `chmod` list) in the fixture schema.
### 9. explain `cache=` field (I-EXPLAIN-CACHE-SWAP) — clause-x gap
Clause x parses only `selected=`, `path=`, `verdict=` from the final `MADO_TERM:` line
(counter `explain_case`); `cache=` and `cmd=` are never compared. Probe (verified):
```
CACHE_FILE=False ref=...cache=absent verdict=OK mut=...cache=present verdict=OK
CACHE_FILE=True  ref=...cache=present verdict=OK mut=...cache=absent verdict=OK
```
No fixture can kill this (print modes never emit cache); propose extending clause x to pin `cache=`
(and `cmd=`, equally unchecked — the same mutation would be invisible there).

Equivalent mutants (survive trivially; no kill exists): **I-TRYEXEC-ABS-CWD** (`os.path.join(cwd, abs)`
returns abs in Python — `command_v` behavior is unchanged) and **I-EXECARG-EQ-ONLY** (an entry-equality
option `-x` is dropped by the unknown-option path anyway, and the execarg is re-inserted from the entry).

## Environment / tooling
No tools installed (operator rule): python3/git/bwrap/strace pre-existing; no pacman, no package
transaction. All runs under `/fast/scratch/hyaku/mado-r47/MutC1Fixtures` (own seat scratch; deleted at
cleanup), XDG_CACHE_HOME always inside the sandbox roots (counter `case_env`); resolver runs only via
the counter's `--print-*` bwrap sandbox. No lane/fleet writes except this seat dir and this report.
No subagents, no background jobs, no external terminals.

## Receipts (seat dir `receipts/`)
`mut-REF-baseline[-@424242].txt`, `mut-<id>[@424242].txt` (23 × 2), `verify-k-*.txt` (9), probe
outputs in `probe.py`/`probe-explain-cache.py` transcripts above. `results.json` holds every verdict
incl. nonce-424242 reruns.
