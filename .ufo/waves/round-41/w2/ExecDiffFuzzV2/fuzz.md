# ExecDiffFuzzV2 — differential fuzz of the delivered tool vs `PRED-C1-r41-v2`'s model

Round 41 (hyaku 7), inline v2 wave w2, lane `mado-shokunin`.
Seat dir: `.ufo/waves/round-41/w2/ExecDiffFuzzV2/`.
Attacks: **the delivered `tools/mado-globals.py`** (DATA commit
`07f2641696b5ac73de1404ea737a9f27e9819aa1`) versus **the v2 model**
(`quality/counters/c1-r41-globals-v2.py` at the same commit) on hostile inputs.

## Method

- `fuzz.py` loads the frozen counter with `importlib` (`main()` never called)
  and reuses its own grammar (`model_out`, `model_sessions`, `gen_fixture`,
  `sample_journal`, `rng_for`, `maxvert`, `ts_of`, `line`, `SHORT`,
  `T1/T2`, `MAX_BYTES`, `TABLE`).
- The tool under test is the DATA-commit `tools/mado-globals.py`, copied
  byte-identically into the seat (`tool-under-test.py`, sha256
  `286c051f…f55e` — identical to the v2 reference `c1/ctl-ref-tool-v2.py.txt`).
- Every mutant journal runs on both sides: `C1.model_out(raw.decode("utf-8","replace"), expects, diff)`
  vs `python3 -I <tool> --journal-file <mutant> [--expect …] [--diff]`,
  compared on **rc + stdout bytes**, stderr required empty on rc 0/1/3/4
  (the counter's own `judge`). `--expect`/`--diff` argv drawn from 6 modes.

## Runs (exact commands)

```
# 1. quick smoke (systematic set + structural + CLI)
python3 -I fuzz.py --quick --jobs 8      # mutants=81 disagreements=0

# 2. full sweep: 13 seeds x 31 mutators x 12 variants + 81 systematic
python3 -I fuzz.py --jobs 8              # mutants=4845 disagreements=0

# 3. harness teeth: same sweep against four one-sentence-wrong variants
python3 -I variants.py
```

## Result 1 — tool vs model: 0 disagreements in 4845 mutants

`fuzz-receipt.txt`: `fuzz: mutants=4845 disagreements=0`, `classes={}`.
Seeds (13): the committed own-work journal `fetch/xdph-journal.txt`, `gen0..gen7`
(encoded exactly as `score_gen`), `sample_journal` n=1,2,3, and a hand-built
v2-classes journal (`v2mix`: 9→10 versions, 123456/1234567, 0xA0 host byte,
`[log]`, `011`/`11`, repeated boot id, Arabic-Indic digits, non-ASCII names,
`-o short` lines mixed in).

31 mutators (≥ 12 variants each): byte flip/insert/delete; line
delete/dup/swap; CR / CRLF; boot insertion (incl. duplicate ids); pid flips;
version digits (`0…1000000`, `1234567`, Arabic-Indic); name lengths 0/1/127/128/129/130;
invalid UTF-8 (lone `\xff`/`\xfe`/`\xc3`, CESU-surrogate, truncated 4-byte);
no trailing NL; boot-only; NUL; spacing (`[LOG] |`/`   |`/tab, `got` vs `Got`,
wrong program); leading/trailing text; timestamp shape; host bytes (`\xff`,
`\xc3`, `\xa0`, tab, 200 chars); reverse; double; append boot; truncate;
alien `-o` blobs; invalid UTF-8 in host/pid slots; extreme version pairs; boot
id mangling.

Systematic sweeps: name-length boundaries with/without `--diff`; version tokens
incl. `999999`/`1000000` and Arabic-Indic; version pairs `9→10`,
`999999→1000000`, `000001→1`, `1→01`, `123456→123457`; pid pairs `1952/01952`,
`0/00`, `007/7`, `011/11`, `1/01`; invalid UTF-8 in host/pid positions; 13
alien `-o` shapes alone and mixed with a valid session; empty/malformed files;
boot variants (31/32/33 hex, upper, trailing `---`).

**Why 0 is structural, not luck:** the tool's grammar is the counter's grammar —
`ADVERT.pattern == ADV_RE.pattern`, `BOOT.pattern == BOOT_RE.pattern`,
`NAME` regex identical, `CLASSES/CLASS_OF == TABLE` (27 names, 10 classes),
measured by `python3 -I` inspection (see receipt `regex-equality` probe below).
The task's v2 classes all fall inside that shared grammar, so any divergence
would show; none did.

## Result 2 — structural (contract) probes, all pass

`fuzz-receipt.txt`:

| probe | want | got |
|---|---|---|
| FIFO as `--journal-file` | `SETUP unreadable` rc 2 | same (no hang) |
| symlink → FIFO | `SETUP unreadable` rc 2 | same |
| directory | `SETUP unreadable` rc 2 | same |
| symlink → directory | `SETUP unreadable` rc 2 | same |
| symlink → regular file | rc 0, census | same |
| dangling symlink | `SETUP unreadable` rc 2 | same |
| missing path | `SETUP unreadable` rc 2 | same |
| empty file | `NO_SESSIONS` rc 3 | same |
| exactly 8388608 B (`x`+`\n`) | rc 3 | same (parses) |
| 8388609 B | `SETUP too_large` rc 2 | same |
| growing file (writer appends past cap under read) | cap at 8 MiB, rc 2 | same, returns |
| stalling regular file (writer holds fd open, no more data) | returns; no hang | rc 3 `NO_SESSIONS` (read hits EOF; regular-file reads never block on a silent writer) |
| file-mode spawn check (journalctl stub on PATH) | no spawn | no spawn |

## Result 3 — CLI surface

12 cases pass (usage/bad_expect/unknown/abbrev/`--diff=1`/`--expect` 0,129,non-ASCII,dash,
128-char-OK with exact model stdout). Two inherited (v1-known) ambiguities
re-measured on the v2 tool, not treated as defects:

- `--journal-file ""` → `SETUP usage` rc 2 (empty value counts as absent),
- `--journal-file "" --live --journalctl <stub>` → runs the live program
  (stub executed, rc 0). Contract "exactly one of --journal-file/--live":
  empty string is treated as not-given; the same reading as the v1 reference.
- `--expect=-x` → `SETUP bad_expect` rc 2 (contract reading; the v1
  reference answered `usage` here — the ambiguity is resolved differently but
  harmlessly by the delivered tool).

## Result 4 — harness teeth (the negatives are measurements)

Quick corpus re-run against four one-sentence-wrong variants of the delivered
tool (`variants.py`; receipts `fuzz-receipt-<name>.py.txt`):

| variant | one sentence changed | disagreements (of 81) | minimised demo |
|---|---|---|---|
| `ascii-digits` | `[0-9]` → `\d` (regex sites) | 2 | `(ver ١)` → want `UNRECOGNIZED_FORMAT` rc 4, got a session rc 0/1 |
| `str-max` | `max(ent[1], ver)` → lexicographic | 2 | `(ver 9)` then `(ver 10)` → want `ver=10`, got `ver=9` |
| `int-pid` | `pid != pid` → `int(pid) != int(pid)` | 5 | `[1952]` then `[01952]` → want 2 sessions, got 1 |
| `splitlines` | `split("\n")` → `splitlines()` | 2 | `…Got interface: wl_seat (ver 1)\r` → want rc 4, got a session |

So the sweep is sensitive to exactly the sentences the v2 fixtures are meant to
pin (vernum0/pidzeros0/asciidigits0/unrec0), and silent on the delivered tool
over the same corpus.

## No defect found

Everything measured is consistent with the v2 predicate and the delivered tool:
no disagreement between the tool and the counter's model on 4845 hostile
mutants (≥ 3000 required), no violation of the structural/CLI contract checks,
and the v2-specific classes (ignored-shape counting, FIFO/symlink/FIFO paths,
growing file, 128/129 names, versions 999999/1000000, invalid UTF-8 in
host/pid, 8 MiB boundary) behave as the contract and the model state.

## Interpreter

System `python3` 3.14.8; no tool installs (no changes to host, no pacman run).
All writes inside this seat dir; the lane and fleet are untouched.
