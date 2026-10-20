# ReviewPacman — `classify_pacman` falsification (round 17, wave 2)

Agent: `MadoR17.ReviewPacman`. Lane root `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Target revision: `988b858bd6049bc709807534fd725c05264f7e60` (C3, pushed).
Artifact: `tools/mado-tripwire.py`, 818 lines, sha256
`4ced68d33ad4db5b86cb8b7cbacbb7f7052fc324ac7ae6672e5459f8a94d4c44`
(worktree bytes == `git show 988b858:tools/mado-tripwire.py`; also the
`SELFTEST_SCRIPT_SHA256` printed by every suite run below).
Scope: `classify_pacman` (lines 292–331) and its dispatch in
`classify_segment` (line 422: `if argv0 in ("pacman","yay","paru")`).
Installs: **none**. No pacman/yay/paru/systemctl/hyprctl invocation, no
sudo/doas, no live probe; man pages and the pacman binary were read as
file bytes, plus `readelf -Ws` (static symbol read, no execution).

## 1. Verdict first

The C3 capability claims I was pointed at **survive in full**:

| Claim | Reproduced |
|---|---|
| selftests core **9/9** | `SELFTEST_SUMMARY: 9/9 passed failed=[]` |
| compound **16/16** | `SELFTEST_SUMMARY: 16/16 passed failed=[]` |
| hardening **33/33** | `SELFTEST_SUMMARY: 33/33 passed failed=[]` |
| anchor exit **1** at `MadoR15.LibinputEvents.jsonl:54` `call_38165` | `MADO_TRIPWIRE: findings`, `exit` 1, two findings at line 54 |
| 4/4 pacman.log join (classification side) | all four quoted commands classify `host_mutation` as the receipt says |

What does **not** survive is a stronger, unstated implication: that
`classify_pacman` implements pacman's operation/flag matrix. It does not.
I found **3 false-negative families** (host mutation reported as
`package_query`) and **4 false-positive families** (read-only form
reported as `host_mutation`), all reproduced with synthetic JSONL under
`/tmp/w2-reviewpacman/` against the exact instrument bytes.

Crucially, **none of them changes an unpermitted verdict**: every
`pacman`/`yay`/`paru` invocation I tried still emits ≥1 finding, so a
no-`--permit` scan still exits 1 (`SKILL.md:529` mandates no `--permit`
while the pause holds). The false negatives flip exit 1→0 **only** under
`--permit package_query`, which is demonstrated in §4 but is not a run
this round permits citing as clean (`SKILL.md:580`).

## 2. Method

One JSONL record per case, exactly the shape `scan_file` consumes:

```json
{"type":"message","id":"m","timestamp":"2026-10-20T15:00:00.000Z","message":{"role":"assistant","content":[{"type":"toolCall","id":"c1","name":"bash","arguments":{"command":"pacman -Fy"}}]}}
```

`python3 -I tools/mado-tripwire.py --scan /tmp/w2-reviewpacman/cases/<file>.jsonl`
per case, verdict parsed from line 2, exit code recorded. Ground truth is
`pacman.8` / `yay.8` read from `/usr/share/man/man8/*.gz` (quoted below);
`getopt_long(3)` and `getopt(3)` read from `/usr/share/man/man3/`.
Coverage sweep: every operation letter `D F Q R S T U V` × the documented
flag letters for that operation, single- and two-flag clusters = **216
clusters**, plus the long-option equivalents and the named cases.

## 3. Findings

Severity legend: **S2** wrong mutation/query class whose consequence is
reachable (permit-flip demonstrated); **S3** same class error with a
narrower trigger; **S4** false alarm in the safe direction (query read as
mutation). None reachable family changes an unpermitted exit code.

### F1 — S2: `-F` + refresh (`-Fy`) is a database write reported as a query

Code path: the flags loop (lines 306–314; `flags.update(a[1:])` at 309)
collects `y`, but line 321
(`if letter in ("Q","F","T","V"): return ("package_query", rule)`)
returns before the `-S` flag logic at 325–330 ever reads `flags`. The
`y` flag is therefore only consulted for `-S`.

| input | expected | got (class / rule) |
|---|---|---|
| `pacman -Fy` | host_mutation | **package_query** / `pacman:-Fy` |
| `pacman -Fyy` | host_mutation | **package_query** / `pacman:-Fyy` |
| `pacman -F --refresh` | host_mutation | **package_query** / `pacman:-F` |
| `pacman --files --refresh` | host_mutation | **package_query** / `pacman:--files` |
| `yay -Fy` | host_mutation | **package_query** / `yay:-Fy` |
| `paru -Fy` | host_mutation | **package_query** / `paru:-Fy` |
| `pacman -Sy` (control) | host_mutation | host_mutation / `pacman:-Sy` |

Ground truth: `pacman.8`, FILE OPTIONS (APPLY TO `-F`), `-y, --refresh`:
“Download fresh package file databases (repo.files) from the server.” The
same flag under SYNC OPTIONS is already `host_mutation` in this tool, so
this is an internal inconsistency, not a definitional judgement call.
Consequence: reproduced exit 1 (no permit) → **exit 0, label
`permitted_only`** with `--permit package_query` (see §4).

Reachability caveat: the write needs root; `sudo`/`doas`/`pkexec`/`run0`/
`su` add their own `host_mutation` finding (`sudo pacman -Fy` yields
`sudo` host_mutation **plus** `pacman:-Fy` package_query), so a successful
privileged refresh cannot produce a finding-free scan. This is a class
error, not a missed host event in the unpermitted configuration.

### F2 — S3: an attached short-option argument hijacks operation detection

Code path: line 302 admits **every** dash token longer than one
character, line 303 collects all uppercase letters in that token, and
lines 304–305 take the first as the operation — without knowing which
short options consume an argument:

```python
letters = [c for c in a[1:] if c.isupper()]
if letters and op is None:
    op = (a, letters[0])
```

| input | expected | got (class / rule) |
|---|---|---|
| `pacman -b/tmp/Q -S foo` | host_mutation / `pacman:-S` | **package_query** / `pacman:-b/tmp/Q` |
| `pacman -r/mnt/T7 -U ./x.pkg` | host_mutation / `pacman:-U` | **package_query** / `pacman:-r/mnt/T7` |
| `pacman -b /tmp/Q -S foo` (separated form) | host_mutation | host_mutation / `pacman:-S` (correct) |

Ground truth: `pacman.8` documents `-b, --dbpath <path>` and
`-r, --root <path>`; `/usr/bin/pacman` imports `getopt_long@GLIBC_2.2.5`
and `optarg@GLIBC_2.2.5` (`readelf -Ws /usr/bin/pacman`), and
`getopt(3)` states the argument may be “the following text in the same
argv-element, or the text of the following argv-element”. The hijack is
attachment-specific: `-b /path` is safe, `-b/path` is not.

Consequence: same permit flip as F1 (`pacman -b/tmp/Q -S foo`, exit
1→0 under `--permit package_query`, demonstrated). Realism: an attached
`-b`/`-r` whose path contains `Q/F/T/V` (e.g. a `T7` mount) is uncommon;
grade the acceptance of the attached form **[INFERENCE]** from
getopt/getopt_long (pacman itself was not executed under the host pause).

### F3 — S3: abbreviated long operations are invisible

| input | expected | got (class / rule) |
|---|---|---|
| `pacman --syn --noconfirm foo` | host_mutation | **package_query** / `pacman` |
| `pacman --upgr ./x.pkg.tar.zst` | host_mutation | **package_query** / `pacman` |
| `pacman --rem foo` | host_mutation | **package_query** / `pacman` |
| `pacman --dat --asdeps foo` | host_mutation | **package_query** / `pacman` |
| `pacman --fi --refresh` | host_mutation | **package_query** / `pacman` |
| `pacman --sync --print foo` (control) | package_query | package_query / `pacman:--sync` |

The rule is the bare argv0, proving `op is None` fell through to line
318 (`return ("package_query", argv0)`). Ground truth: pacman imports
`getopt_long` (above); `getopt_long(3)`: “Long option names may be
abbreviated if the abbreviation is unique or is an exact match for some
defined option.” `--syn`, `--upgr`, `--rem`, `--dat`, `--fi` are unique
prefixes of `--sync`, `--upgrade`, `--remove`, `--database`, `--files`.
I also tested `--sy`: it is **ambiguous** (`--sync`/`--sysupgrade`) and
is rejected by getopt_long, so I do not count it as a defect — the tool's
`package_query` for `--sy` describes a command that cannot mutate.
Same privilege gating as F1.

### F4 — S4 (safe direction): documented read-only forms reported as `host_mutation`

| input | expected | got |
|---|---|---|
| `pacman -Dk foo` / `pacman -D --check` | package_query | **host_mutation** / `pacman:-Dk`, `pacman:-D` |
| `pacman -Rp foo`, `-Rcp`, `-Rdp`, `-Rnp`, `-Rps`, `-Rpu` | package_query | **host_mutation** |
| `pacman -Up foo`, `-Udp`, `-Unp`, `-U --print` | package_query | **host_mutation** / `pacman:-Up` |
| `pacman -Sup`, `-Spu`, `-Sup --print-format %n` | package_query | **host_mutation** |
| `pacman -S --print-format %n foo` | package_query | **host_mutation** / `pacman:-S` |
| `pacman -Sh foo` | package_query (syntax help) | **host_mutation** / `pacman:-Sh` |
| `yay -Ps`, `yay -P -s`, `yay -Pc` | package_query | **host_mutation** |
| `paru -Ps` | package_query | **host_mutation** [INFERENCE: paru not installed] |

Ground truth: `pacman.8` `-p, --print`: “Only print the targets instead of
performing the actual operation (sync, remove or upgrade)”; `--print-format`
“Implies --print”; DATABASE OPTIONS `-k, --check`: “Check the local
package database is internally consistent”; `-h, --help`: “Display syntax
for the given operation”. `yay.8`: `-P, --show` “Perform yay specific
print operations”, `-s, --stats` “Displays information about installed
packages and system health”, `-c, --complete` prints the completion list.
The code's `silgp` set (line 328) models `-p` only for `-S`, and only for
the literal `-p`/`--print` token — `--print-format` is not in the flags
loop (lines 309–314).

These are false alarms, not missed mutations; they matter for precision
and for any permitted-query run, where a documented dry-run
(`pacman -Sup`, `pacman -U --print`, `pacman -Dk`) reads as a mutation.

Coverage sweep summary: **216** documented single/two-flag clusters →
**22** class diffs, all inside the four families above: F+y 6, D+k 2,
R+p 6, S+p(-u) 5, U+p 3. The long-option form (`--database`/`--files`/
`--query`/`--remove`/`--sync`/`--deptest`/`--upgrade`/`--version` × the
same flag letters, 216 clusters) yields the identical 22 diffs with the
same split, so the defect is in the operation dispatch, not the token
spelling.

## 4. Permit-flip demonstration (consequence, not a round verdict)

| command | no `--permit` | `--permit package_query` |
|---|---|---|
| `pacman -Sy` | exit 1, `findings` | exit 1, `findings` |
| `pacman -Fy` | exit 1, `findings` | **exit 0, `permitted_only`** |
| `pacman -b/tmp/Q -S foo` | exit 1, `findings` | **exit 0, `permitted_only`** |
| `pacman -b /tmp/Q -S foo` | exit 1, `findings` | exit 1, `findings` |
| `pacman -Dk` | exit 1, `findings` | exit 1, `findings` |
| `yay` | exit 1, `findings` | exit 1, `findings` |

Under the round's mandated no-permit usage (`SKILL.md:529`) every row is
exit 1, so the class errors cannot launder a scan into `clean`.

## 5. Coverage gap in the three suites

The passing suites pin only these pacman rules — `core`: `-S`, `-Qi`,
`-Si`, `-Sp`, `-Fl`; `compound`: `-S`, `-Syu`, `-U`, `-R`, `-Q`, `-Qq`;
`hardening`: `-S`, `-Sw`, `-Sp`, `-Q`, `-Qi`, `-R` (rule strings
extracted from the three `expected.json` files, duplicates across cases
collapsed). **No case exercises** `-F`+`y`, `-D`+`k`, `-T`, `-Rp`/`-Up`/
`-Sup`, `-P` stats, an abbreviated long operation, or an attached
short-option argument.
So 9/9, 16/16, 33/33 are true but are not evidence for the op/flag
matrix; the defects in §3 sit entirely outside the pinned branches.

## 6. Claims that survived, precisely

- Selftests at the pinned bytes: 9/9, 16/16, 33/33; script sha
  `4ced68d…4c44`, identical to the committed revision and to the three
  `evidence/tripwire-selftest-*.txt` receipts.
- Anchor: scan of
  `…/2026-10-20T01-48-55-258Z_01a156ff-…/MadoR15/MadoR15.LibinputEvents.jsonl`
  → `MADO_TRIPWIRE: findings`, exit 1, transcript sha256
  `78388d42cf08a3cb9ba7c73ab479e5ea7ec92a50ba66163d614423b5a8a7c74f`,
  173 lines, 14 bash calls, counts
  `{"host_mutation":2,"live_probe":1,"package_query":5}`. Line 54,
  `call_38165`, `2026-10-20T07:25:16.905Z`, command
  `sudo pacman -S --needed --noconfirm libinput libinput-tools` →
  `host_mutation/sudo` **and** `host_mutation/pacman:-S`. This byte-for-byte
  matches `evidence/tripwire-anchor-r15.txt`.
- The five `package_query` findings in that named transcript are
  `-Qi`, `-Si`, `-Fl`, `-Sp`, `-Ql` — all genuinely read-only. **No live
  instance of F1/F2/F3 appears in the transcript my item names**; the
  defects are latent, not exhibited there.
- Join receipt (`evidence/tripwire-pacmanlog-join.txt`): the four quoted
  commands (three `pacman -S …`, one `pacman -Sw …`) all classify
  `host_mutation` exactly as the receipt states. I did **not** re-verify
  the timestamp join against the other seats' transcripts — those files
  are not named by this item.

## 7. Residual risk and verification gaps

- pacman/yay/paru were never executed (host pause), so F2/F3 acceptance
  of `-b/path` and `--syn` is static evidence (`readelf` import +
  `getopt(3)`/`getopt_long(3)`), not observed behavior. Marked
  [INFERENCE] where it matters.
- All three false-negative families are privilege-gated; every elevation
  mechanism the tool knows (`sudo`, `doas`, `pkexec`, `run0`, `su`, plus
  `systemd-run`) adds a separate `host_mutation`, so no finding-free scan
  for a *successful* mutation was found.
- `paru` is absent from this host (`/usr/bin/paru` missing); `paru -Ps`
  is graded [INFERENCE]. `yay` bare invocation and `yay --help` are
  mapped to `host_mutation` by the no-op default (lines 316–317); if yay
  prints usage there, that is a safe-direction false positive, but its
  runtime behavior was not executed and is unverified.
- Occurrence granularity (adjacent, not classification): findings are
  deduped per `(class, rule)` per tool call, so `pacman -Q a; pacman -Q b`
  yields one finding; exit code is unaffected.
- Only synthetic `/tmp` inputs and the one named transcript were read;
  no lane file was modified. No commits, no git/jj mutation.

## 8. Reproduction appendix

```sh
# per-case
python3 -I tools/mado-tripwire.py --scan /tmp/w2-reviewpacman/cases/<case>.jsonl
# selftests
python3 -I tools/mado-tripwire.py --selftest .ufo/waves/round-17/tripwire/{core,compound,hardening}
# static ground truth used (file bytes only)
zcat /usr/share/man/man8/pacman.8.gz     # -p/-y/-k/-h semantics quoted above
zcat /usr/share/man/man8/yay.8.gz        # -P/--show, -s/--stats
zcat /usr/share/man/man3/getopt_long.3.gz /usr/share/man/man3/getopt.3.gz
readelf -Ws /usr/bin/pacman | grep -E 'getopt|optarg'
```
