# ExecR2Check — R2 digest, every number re-derived (round 47, w2)

Target: `.ufo/waves/round-47/w1/ExecR2Digest/` (digest of the untracked round-46
`out.json.rows.tsv`). Judge source of truth: `.ufo/waves/round-46/w1/ExecStofOracle/receipts/out.json.rows.tsv`.

**Verdict: 1 WRONG numeral, 1 dead receipt, 1 receipt/digest inconsistency, 2 unverifiable-now residuals; every
identity, count and aggregate number CONFIRMED.** The wrong numeral is in the seat's analysis prose (§2), not in the
digest line (`§6`) the L1 commits — that line carries no contiguity claim (its only "16" characters are the
locator `diff.py:167` and the compiler `g++ 16.2.1`) and is number-for-number correct.

## 0. Premise failure — the file the seat had to read no longer exists

The w2 spec says "re-derive … from `…/out.json.rows.tsv` (read-only, do not move it)". It was already gone when w2
launched: the round-47 L1 removed it at `2026-10-26 19:16:55`, before `w2.ready` (19:34:34), with receipt
`.ufo/waves/round-47/receipts/r2-removed.txt` (committed in `9bddd6ac`, "R2 removal receipt"):

```
R2 (round-46 closure): removed untracked …/out.json.rows.tsv on 2026-10-26 by the round-47 L1 after digest.
sha256 6573f76b…d6d3238 bytes 3282451 lines 59395
```

Evidence of absence (all read-only):

```
$ stat --printf='%n %s\n' .ufo/waves/round-46/w1/ExecStofOracle/receipts/out.json.rows.tsv
stat: cannot stat '…/out.json.rows.tsv': No such file or directory (os error 2)
$ ls -la --time-style=full-iso .ufo/waves/round-46/w1/ExecStofOracle/receipts/ | head -3
drwxr-xr-x … 2026-10-26 19:16:55.186928611 -0300 .
$ find /home/vgpnk/Projects/shokunin/mado-shokunin -name out.json.rows.tsv        # (no output)
$ timeout 60 find /fast/scratch/hyaku -maxdepth 6 -name out.json.rows.tsv
/fast/scratch/hyaku/mado-r47/ExecR2Check/out.json.rows.tsv                        # my own reproduction only (since deleted)
$ git ls-tree -r --name-only HEAD -- .ufo/waves/round-46/w1/ExecStofOracle/receipts/out.json.rows.tsv   # (empty)
$ git ls-files --error-unmatch …/out.json.rows.tsv; echo $?
error: pathspec '…' did not match any file(s) known to git
1
```

So the seat can only verify the digest by **byte-reproducing** the removed file from the committed harness and
re-deriving every number from that reproduction plus the surviving committed `out.json`. That is exactly the
reproducibility claim the digest makes in §4/§6, and it holds exactly.

## 1. Reproduction (bit-for-bit) — command and output

```
S=/fast/scratch/hyaku/mado-r47/ExecR2Check; mkdir -p "$S"; cd "$S"
R=/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/w1/ExecStofOracle/receipts
cp "$R"/gen.py "$R"/stmt.cpp "$R"/diff.py .                 # 7378170e… / 55795cff… / b8d5c1a2…
g++ -std=c++23 -O1 -o stmt stmt.cpp
python3 -I gen.py cases.tsv                                  # cases=59394 categories=21
python3 -I diff.py cases.tsv ./stmt \
  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/l1-draft/mado-devices.py out.json
sha256sum out.json out.json.rows.tsv cases.tsv stmt
```

```
946ed60daefc26da105dc358cde1601446330b50279fb531f50ed9994a759627  out.json
6573f76b5a61c6d0270ae4bfb9b3f37d7e95825c6fbfb13858a78fe54d6d3238  out.json.rows.tsv
fb355339468e93d4dcaddd381dd40e6391921dc5ca6dc679b6287665ecee9273  cases.tsv
7606f8ef008d5577b337cdf274206d6936dfebe9f797cd3e8bb185b2dedd6295  stmt
  59395 3282451 out.json.rows.tsv
```

Toolchain on this host equals `receipts/versions.txt`: `g++ (GCC) 16.2.1 20260810`, `Python 3.14.8`. The
reference pin is `.ufo/waves/round-46/l1-draft/mado-devices.py` = `b229efd0…` (the digest writes the bare
`l1-draft/` prefix; round-47's `l1-draft/` holds only `mado-terminal.py`, so round-46 is the only resolution and it
is the one that reproduces both hashes).

My own verifier (written fresh, not the seat's `derive.py`) then re-derives every number from those bytes:

```
python3 -I .ufo/waves/round-47/w2/ExecR2Check/verify.py out.json.rows.tsv "$R/out.json" cases.tsv
```

`verify.txt` — 62 checks, 61 OK, 1 WRONG (finding H1). Its output is summarised below per claim.

## 2. Per-number result

### §1 File identity

| claim | got | status |
|---|---|---|
| sha256 `6573f76b5a61c6d0270ae4bfb9b3f37d7e95825c6fbfb13858a78fe54d6d3238` | identical | **CONFIRMED** (of the reproducible bytes; see H4) |
| bytes 3 282 451 | 3282451 | **CONFIRMED** |
| lines 59 395 = 1 header + 59 394 rows, LF, newline-terminated | LF count 59395, trailing `\n`, data rows 59394 | **CONFIRMED** |
| header `cat cls ref_line truth_line ref_printed truth_printed text` | byte-equal | **CONFIRMED** |
| UTF-8, no CR anywhere | decodes as UTF-8; `raw.count(b"\r")==0` | **CONFIRMED** |
| 11 rows carry U+00A0 | 11, at lines 47718, 47739, 47760, 47781, 47802, 47823, 47844, 47865, 47886, 47907, 47928; all `prefix`, all end with NBSP | **CONFIRMED** (exact list) |
| longest line 108 bytes, line 49142 | max over 59 395 lines = 108 at line 49142 | **CONFIRMED** |
| untracked (`??`), not gitignored (`git check-ignore` exit 1) | `check-ignore -v` exit 1; absent from HEAD tree and from the index | **CONFIRMED** (the literal `??` observation is gone, H4) |
| committed neighbour `out.json` 2 172 bytes, sha `946ed60d…` | 2172 bytes, `946ed60d…` | **CONFIRMED** |

### §2 Class / flip table (TSV alone)

Re-derived with `split("\t", 6)`; `top_flip` recomputed from `cls→kind` (`diff.py:139-150`) and `diff.py:123-135`.

| class | claimed (n, line, top, print) | got | status |
|---|---|---|---|
| same_value | 55 229, 0, 0, 0 | 55229, 0, 0, 0 | **CONFIRMED** |
| value_ulp_diff | 2 751, 2 751, 2 751, 2 751 | 2751, 2751, 2751, 2751 | **CONFIRMED** |
| both_unset | 1 294, 0, 0, 0 | 1294, 0, 0, 0 | **CONFIRMED** |
| ref_refuses_cpp_both_unset | 64, 0, 64, 0 | 64, 0, 64, 0 | **CONFIRMED** |
| ref_refuses_cpp_stores | 37, 29, 37, 37 | 37, 29, 37, 37 | **CONFIRMED** |
| other | 19, 19, 19, 19 | 19, 19, 19, 19 | **CONFIRMED** |
| totals | 59 394, 2 799, 2 871, 2 807 | 59394, 2799, 2871, 2807 | **CONFIRMED** |

The zero `print_differs` cells are a presentation of an *absent* key in committed `out.json` (`diff.py:159` only
creates the key on a difference); my dict comparison includes key absence and still reports the class dict
identical, so the digest's "identical dict" is exact, not approximate.

21 categories, counts and file order: all 21 numbers equal (`dec1 3051 … junk 2000`), first-appearance order identical.
`awk -F'\t' 'NR>1{c[$2]++}'` gives the same six class counts, as the digest asserts.

Category contiguity: **H1 — WRONG.**

### §3 Aggregates re-derived from the TSV and compared with committed `out.json`

| field | claimed | got | status |
|---|---|---|---|
| top-level key order | `cases,categories,classes,flips,examples,dump_json_breaks,dump_json_break_examples,trim_mismatch_unverified,reported_roundtrip_failures` | identical | **CONFIRMED** |
| `cases` / `categories` | 59 394 / 21 | equal | **CONFIRMED** |
| `classes` dict (all six, key-absence included) | identical | identical | **CONFIRMED** |
| `flips.total` + five `by_class` keys (19 / 64 / 29 / 8 / 2751) | 2 871 | identical strings and counts | **CONFIRMED** |
| `examples` 5 keys, 5-tuples, first 3 fields | keys yes, 3/5 yes | identical first-3 per key; committed lengths `{5}` | **CONFIRMED** |
| `dump_json_break_examples` 8 `nan` triples | identical | JSON-equal, in order | **CONFIRMED** (see H3) |
| `dump_json_breaks` | 8 | 8 rows with `truth_line=SETUP`; triples `(cat,text,truth_printed)` equal | **CONFIRMED** |
| `trim_mismatch_unverified` | 4 (`strip(WS) != strip(" \t\r\n")`) | 4 | **CONFIRMED** |
| `reported_roundtrip_failures` | 0 | 0 | **CONFIRMED** |
| `cpp_bits` of the `value_ulp_diff` example | 1 000 593 163 | 1000593163 | **CONFIRMED** |
| TSV = `rows` with `kind` dropped, nothing filtered/reordered | 59 394 rows = `cases`; text+cat sequence equals `cases.tsv` unescaped | **CONFIRMED** |
| `diff.py` locators 123-135, 139-150, 167, 185, 187, 188, 191 | `sed -n` shows the named construct on each line | **CONFIRMED** |
| `gen.py:140-145` emits the triple | lines 140/141/145 are the three `add(...)` calls, 142-144 the `"." in s` guard | **CONFIRMED** |
| `gen.py` fixed seed `random.Random(46)` | `gen.py:48` | **CONFIRMED** |
| `truth_printed` is the `std::format("{:.2f}", …)` render | `stmt.cpp:32` | **CONFIRMED** |

Their retained evidence is honest: re-running `receipts/derive.py` on my reproduction writes `rederived.json`
**byte-identical** to the committed copy (`cmp` exit 0, both sha256 `87be88b2…`), and `derive-rerun-stdout.txt` is
`diff`-identical to their `analysis.txt` (0 lines of difference; `field_count_hist` `{7: 59386, 8: 7, 10: 1}`,
`warn_rows_with_extra_cols=8`, class/flip/category tables all reproduced).

### §5 Consumer caveats

| claim | got | status |
|---|---|---|
| 8 rows with literal tabs in `text`, lines 47945-47949 / 48373 / 48374 / 48375, texts `\t5 \t5. \t.5 \t5.0 \t0.25 \t0.5 0.5\t \t\t0.5\t` | exactly those lines and texts (47945-47949 and 48373-48375 are `prefix` and `ws` respectively) | **CONFIRMED** |
| naive split gives NF 8 (7 rows), 10 (line 48375) | `[8,8,8,8,8,8,8,10]` | **CONFIRMED** |
| columns 1-6 stay correct, only `text` truncated | maxsplit-6 fields 1-6 equal naive fields 1-6 on all 8 rows; only field 7 differs | **CONFIRMED** |
| 11 NBSP rows, `prefix`'s `"\u00a0"` suffix (`gen.py:64`) | 11, all `prefix`, all NBSP-terminated; `gen.py:64` SUFFIXES holds `"\u00a0"` | **CONFIRMED** |
| no CR, no embedded newline | every record is one LF line, 0 CR | **CONFIRMED** |

### §6 The digest line the L1 commits

Every number in it re-derives: sha256, 3 282 451 bytes, 59 395 LF lines, header, six class counters with their
flip columns, 21 categories (`half3` 30 501, `dec2` 6 101), `flips.total` 2 871 with the five keys, 8 breaks with the
eight `nan` triples, `trim_mismatch_unverified` 4, `reported_roundtrip_failures` 0, and the reproducibility claim
(both hashes regenerate exactly). It carries no contiguity claim and no standalone "16" count (the only "16"
characters in it are the locator `diff.py:167` and the compiler `g++ 16.2.1`), so **H1 does not touch it**.

## 3. Holes

### H1 — WRONG: "16 of the 21 categories are contiguous blocks" (digest §2, `digest.md:46`)

The true count is **18** (21 − the three interleaved `dblround_*`), and the sentence contradicts its own next
clause ("followed by the contiguous `dblround_hand` … and `junk` …"). 16 is only the count of blocks *before* the
interleave; `dblround_hand` and `junk` are also single blocks.

```
$ cd /fast/scratch/hyaku/mado-r47/ExecR2Check  # after the §1 reproduction
$ python3 -I -c "
from collections import defaultdict
pos=defaultdict(list); f=open('out.json.rows.tsv',encoding='utf-8'); next(f)
for n,l in enumerate(f,start=2): pos[l.split('\t',1)[0]].append(n)
runs={c:1+sum(1 for a,b in zip(v,v[1:]) if b!=a+1) for c,v in pos.items()}
print('single-run:', sum(1 for r in runs.values() if r==1))
print('multi-run:', {c:r for c,r in runs.items() if r>1})"
single-run: 18
multi-run: {'dblround_above': 3000, 'dblround_at': 3000, 'dblround_below': 3000}
```

Per-category spans and maximal runs (`runs.txt`, same reproduction tree): `dec1` 2-3052, `dec2` 3053-9153, `dec3` 9154-11380, `dec4` 11381-12580,
`dec5` 12581-13780, `dec6` 13781-14980, `dec7` 14981-16180, `half3` 16181-46681, `half3r` 46682-47698, `prefix`
47699-48004, `exp` 48005-48313, `subnormal` 48314-48335, `hex` 48336-48349, `nonfinite` 48350-48369, `ws`
48370-48384, `longdigits` 48385-48391, `dblround_hand` 57392-57395, `junk` 57396-59395 — 18 single blocks.
Severity: analysis prose only; no derived number depends on it and the §6 landing line is unaffected. Fix: 18.

### H2 — the seat's own locator receipt is dead, not just stale

`receipts/verify-locators.sh` claims "`7/7 ok`" (`locators.txt`). Re-running it now:

```
$ sh .ufo/waves/round-47/w1/ExecR2Digest/receipts/verify-locators.sh "$PWD"
ok   rows-append            diff.py:167
ok   write-outjson          diff.py:185
ok   write-rows-tsv         diff.py:187
ok   write-header           diff.py:188
ok   write-row              diff.py:191
sed: can't read …/receipts/out.json.rows.tsv: No such file or directory
rc=2
```

Its sixth check (`chk tsv-header … "$T" 1`) depends on the removed file, so the receipt cannot be re-verified after
the removal the digest itself authorises; `locators.txt` is a pre-removal snapshot. The five `diff.py` locators do
hold (recomputed by `grep -n`), and the header check was independently satisfied by my reproduction (`verify.txt`
"A. header line exact bytes"). No number is wrong; the receipt should say it is a snapshot, or the header check
should be repointed at the reproduction.

### H3 — `analysis.txt` prints `equal=False` for `dump_json_break_examples` while the digest says "identical"

`receipts/analysis.txt`: `dump_json_break_examples … equal=False`, because their in-memory re-derivation keeps
tuples and the committed JSON has lists. `rederived.json` (the machine copy) lists them, and my independent
JSON-normalised comparison is equal, so the digest's "identical | yes" is right and the receipt line is a
type artefact. Worth one sentence if the L1 quotes `analysis.txt`; nothing to fix numerically.

### H4 — residuals that can no longer be re-observed (not defects in any number)

- `§4` "both byte-identical to the worktree copies (`cmp -s` exit 0)" and `§1` "`git status --porcelain` → `?? …`"
  were true of a file that no longer exists; they cannot be re-run. Mitigation observed: the claimed digests
  regenerate bit-for-bit from committed sources (`946ed60d…`, `6573f76b…`), the removal receipt records the same
  sha256/bytes/lines, and `check-ignore`/`ls-tree`/`ls-files` still prove "untracked and not ignored".
- Therefore the *removed inode itself* is confirmed only transitively: the L1's removal receipt could have been
  measured or copied from the digest (the text does not say). Given exact reproduction, a materially different file
  at that path is not credible, but I cannot exclude it by measurement — say so if the closure line is challenged.

## 4. What I ran vs what I did not

Ran: the three pipeline stages on local copies; `sha256sum`, `wc`, byte/UTF-8 scans; my `verify.py` (62 checks);
`awk` column cross-check; their `derive.py` re-run; their `verify-locators.sh` re-run; `sed -n`/`grep -n` on
`diff.py` and `gen.py`; `git ls-tree`, `git ls-files`, `git check-ignore` (read-only). Not run: any git/jj mutation,
any package transaction, any compositor or terminal command, any resolver run. No host config was read.

## Retained evidence (seat dir `.ufo/waves/round-47/w2/ExecR2Check/`)

- `verify.py` — the independent verifier (62 checks; `python3 -I verify.py <rows.tsv> <out.json> <cases.tsv>`).
- `verify.txt` — its full output (61 OK, 1 WRONG, the H1 line).
- `runs.txt` — per-category spans and maximal-run counts (H1's proof).
- `cmp-rederived.txt` — `rederived.json` byte equality: both copies sha256 `87be88b2…`.
- `repro-sha256.txt` — reproduction hashes (`out.json` 946ed60d…, `rows.tsv` 6573f76b…, `cases.tsv` fb355339…,
  `stmt` 7606f8ef…, sources, reference), plus `wc -c -l` of the reproduction.
- `derive-rerun-stdout.txt` — their `derive.py` re-run against my reproduction (byte-identical `rederived.json`).
- `diff-stdout.json` — `diff.py`'s own JSON on my reproduction.
- `locators-rerun.txt` — H2's failing run.
- `report.md` — seat status.

Scratch `/fast/scratch/hyaku/mado-r47/ExecR2Check/` (4.8 MB) is deleted at the end of this seat; no path under it
is cited as evidence.
