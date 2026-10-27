# SentPrivacy — privacy of the round-49 evidence and of the round-50 w1 tree

Seat `SentPrivacy` (sentinel, leaf), round 50 / w1. Carried item from `.ufo/waves/round-49/w2-items.json` (never dispatched in
round 49; routed by the round-49 closure D1), retargeted as the ticket states: scan what round 49 **committed** under
`.ufo/waves/round-49/` at `13631f24050f22db92bf5bd33e0f4d014192992e` (the round-50 claims commit, which contains the whole
round-49 tree), scan the round-50 tree, and run the installed gate (v2, `82c9053a…`) and the v3 draft (`ffdc9d62…`) with
`--scope all` on a scratch clone at that revision. Nothing below reproduces a host value: classes, file paths and counts only.

Everything is measured. Receipts are in `.ufo/waves/round-50/w1/SentPrivacy/receipts/`: `gate-v2-scope-all-at-13631f24.txt`,
`gate-v3-scope-all-at-13631f24.txt`, `gate-v2-round50-precommit.txt`, `gate-v3-round50-precommit.txt`,
`gate-v2-synthetic-binds-fixture.txt`, `gate-v3-synthetic-binds-fixture.txt`, `scan-round49-at-13631f24.json`,
`scan-round50-tree.json`, `scan-evidence-privacy.py`, `binds-raw-shape.txt`, `ancestry-and-presence.txt`,
`waiver-gate-copy-test.txt`, `host-surface-scan.txt`, `locators.txt`, `gate-runs.txt`. Scratch
`/fast/scratch/hyaku/mado-r50/SentPrivacy` held the clone and the fixture repos, with `HOME`/`XDG_*`/`TMPDIR` inside it; the
host was read with `hyprctl version|devices -j` only. Tool installs: none.

## 0. Verdict

1. **One committed red, and it is still at the tip: the complete `hyprctl binds -j` dump.**
   `.ufo/waves/round-49/w1/ScrSkill/receipts/binds-raw.json`, 90,401 B, sha256 `9a47199e…00c779`, added by the round-49
   freeze commit `dd2e827e`, still present at the data commit `430d2569`, at the round-49 closure tip `8ae47b95` and at
   `13631f24` (`ancestry-and-presence.txt`). It is exactly the artifact the round's own privacy seat flagged as **I-1** in
   `.ufo/waves/round-49/w1/SentPrivacy/report.md:155` — **in the same commit that added the dump** — and the data commit did
   not remove it. Nothing else committed under `.ufo/waves/round-49/` is a red.
2. **Neither gate can see that class.** v2 and v3 both score **0 findings** on the live blob (no `FINDING` line in either
   `--scope all` receipt names it) and **0 findings, rc 0** on a scratch repository whose only file is a binds-shaped dump
   (`gate-v2/v3-synthetic-binds-fixture.txt`). So round-49's actual leak would have passed any freeze-time gate run.
3. **Two round-50 items must be fixed before the data commit, not after:** `w1/ScrCorrectionsR50/receipts/d2-seat-state.txt`
   carries two `ls -l` rows with the account in the owner/group columns (v3 `R8_ACCOUNT_COLUMN rows=2`), and the wave copy
   `w1/ExecGateV3/check-session-material.py` adds three findings unless it ships with its `kind=gate-copy` waiver at the same
   time the gate is installed.
4. The other classes are clean: no device names, window titles, process tables, cache records, private IPs/MACs, or
   structural home paths (`path:LINE:`, listing header, quoted diagnostic, `ls -l` row) in round-49 or in round-50 so far.

## 1. The committed raw binds dump (F1 — highest severity)

| | |
|---|---|
| path | `.ufo/waves/round-49/w1/ScrSkill/receipts/binds-raw.json` |
| identity | git blob `40b9285a…`, content sha256 `9a47199e…00c779`, 90,401 B, 192 records, 18 fields |
| introduced | `dd2e827e` (round-49 freeze), absent at base `03e4ae76` (`git log --diff-filter=A`) |
| still present | `430d2569` (data), `602e39e3`, `8ae47b95` (closure tip), `13631f24` (round-50 claims) |
| provenance | `.ufo/waves/round-49/w1/ScrSkill/receipts/binds-summary.txt:2` records the capture command; `w1/ScrSkill.md:108` lists the file as a seat artifact |
| waiver | none: `.ufo/waves/round-49/` holds no `.synthetic` sidecar and the registry has no line for it |

What it carries (counts only, `binds-raw-shape.txt`): 192 bind records, 24 distinct dispatchers, **104 `exec` binds with 104
non-empty command arguments** (136 distinct, up to 107 chars, 83 multi-word, 10 with a URL substring, 3 with a shell chain,
19 with quotes/regex), **190 non-empty `description` values** (185 distinct, up to 36 chars), **2 `switch:on|off:` keys whose
suffix is a 10-character switch device name**, 14 distinct keycodes and the full modmask distribution. No `/home/` or `~` in
any argument, and no absolute path, so the leak is the workflow plane — commands, descriptions, device name, keymap — not a
file path.

Why it is a red rather than a taste question: SKILL.md rule 4 keeps the session and config plane shape-only
(`SKILL.md:33`, `:343`), and the same round's other seats respected that — `w1/ExecBindsLive/receipts/binds-receipt.txt` and
round-50's `w1/ExecLiveR50/binds-live-r50.txt` are the compliant form (sha256 of the capture, counts, histogram; the raw JSON
explicitly not embedded). `w1/ScoutHeld.md:48` states the rule the dump breaks.

Smallest remediation (round-50 erratum/fix; round-49 bytes are not rewritten):
- replace the blob at the tip with a shape-only derivative — the sibling receipts are the model — or with a tombstone that
  names the git blob and the content digest and states that the raw capture is not part of the public record;
- append the erratum to `corpus/lessons/round-50.md` naming the path, the committing revision `dd2e827e` and the fact that
  history retains the blob, so any future publish/rewrite decision is operator-visible (`origin` is a local path today —
  `.git/config`, not tracked — so nothing is published yet);
- note for the freeze: this is the class the gate has no rule for (§2), so it must not be claimed as caught.

## 2. The gate gap this exposes (F2 — instrument finding for C2)

Measured, not inferred:

- v2 and v3 read the blob at the real revision and emit no finding: round-49 subset of the two `--scope all` runs is v2 3
  findings / v3 4, and every one of them is a **gate copy's own selftest constants** (R1/R2/R3) plus one masked-sample
  receipt (§4). `grep -c binds-raw gate-*.txt` = 0 in both.
- On a clean synthetic repository whose only tracked file is a 6-record binds-shaped JSON dump, both gates report
  `files=1 findings=0`, rc 0.

Cause: no rule is keyed on a bind record. R1 needs `class`+`title`, R3 needs `serial`+an identity field, R4/R7 are line- and
path-shaped, R8 is an owner column, R9 is cache-record text. v3's declared-limits paragraph (`check-session-material.py:168`)
does not name the bind record as uncovered, so a reader of the gate believes this class is out of scope for a reason — it is
out of scope by omission.

For `PRED-C2-r50`: either add `R10_BIND_RECORD` (a JSON array/objects carrying `dispatcher` **and** (`arg` or `modmask` or
`keycode`), counted per file, values never printed) to the covered shape set, or name the omission in the limits paragraph and
in the freeze — but then the round-50 lesson may not read "the lane's evidence-privacy gate covers the round's planes".
Round-50's own live receipts are the green counter-shape for this rule (shape-only, sha256 header, no `arg`/`description`).

## 3. Round-50: two items to fix before the data commit

**F3 — account columns in `w1/ScrCorrectionsR50/receipts/d2-seat-state.txt:58-59` (S2, pre-commit).** Two `ls -l` rows carry
the account in the owner and group columns (4 occurrences); the same file's line 1 also writes the lane's absolute path into a
prose header. v3 scores `R8_ACCOUNT_COLUMN count=2 detail=rows=2` on a pre-commit snapshot; v2 scores nothing (the class is
new in v3). Regenerate the two rows with `ls -ln` (v3's own doc names it as the compliant form, `:62`) or replace them with a
count, and write the lane path as `~` — otherwise the round-50 data commit adds a self-inflicted red under the very gate C2
installs.

**F4 — the wave copy of the gate needs its waiver in the same commit (S3, pre-commit).** `w1/ExecGateV3/check-session-material.py`
is byte-identical to the v3 draft (`ffdc9d62…`); v2 and v3 both score its selftest constants as R1/R2/R3. Measured waiver
mechanics (`waiver-gate-copy-test.txt`): `kind=gate-copy` works **only** once `quality/check-session-material.py` is
byte-identical to it, i.e. after the C2 install — then 3 `WAIVER` lines appear and the wave copy stops firing; `kind=fixture`
is **refused** for it (its constants are not all in the reserved namespace). So the C2 data commit must carry the sidecar, the
registry line in `quality/session-material-waivers.txt`, and the install together. Also measured: the installed gate source
**always** fires R1/R2/R3 on itself under `--scope all` and **cannot** be waived (W1 restricts registry paths to
`.ufo/waves/`), so scope-all can never be green at any revision — a C2 counter must not assert that it can.

## 4. Two further classes the freeze should record

**F5 — the lane's own masking convention is a v3 false positive (S3).** `w1/ExecSessionShapes/receipts/base-new-rule-samples.txt`
masks every home path to a one-letter placeholder before printing (`sample_shapes.py:30`) — the file contains no account name
and no real home path — yet v3 reports `R7_HOME_PATH_PREFIX forms=prefix:2,diag:1 paths=2` on it (`locators.txt` §4, lines 17
and 19). The green shape set therefore lacks "masked placeholder form", and a seat that follows the round-49 triage
convention produces findings while a seat that writes nothing produces none. Either exempt a placeholder segment
(`/home/<one-letter>`, `/home/<user>`, `/home/$USER`) or declare `~` as the only accepted masking and say so in the round-50
prompt.

**F6 — machine hostname (S4, class not in the round-49 table).** `w1/ScrSkill/receipts/hyprctl-version-options.txt:2` writes a
`host:` metadata line with the 8-character hostname (the tool's own output does not carry it; the seat added it). One
occurrence, one file; round-50's counterpart omits it. Not in the prompt's enumerated set, so this is a class-list gap, not a
breach: add "machine identifier" to the class list and mask it (`host: <redacted>`), which the round-50 live receipts already
do.

## 5. Smaller items

- **F7 pasted bind line (S4).** `w1/ConnClaims.md:205` and `w1/ConnClaims/report.md:204` carry one `bind = MOD, KEY, exec, CMD`
  line with the key and command in clear (class R49-10 in the round-49 table; both gates miss it). It matches the shape of a
  host bind, so render it as `bind = SUPER, <key>, exec, <command>`. Round-50 has none.
- **F8 account name in prose/metadata (S4, convention drift).** 108 round-49 files carry the account name inside the lane path,
  236 lines, **0 structural** — i.e. no `path:LINE:` prefix, no listing header, no quoted diagnostic, no `ls -l` row anywhere
  under round-49 (`scan-round49-at-13631f24.json`; the round-49 seat's own count was 277 before the late seats landed). The
  forms are `lane=<lane path>` metadata fields and `$ git -C <lane path>` command transcripts. R7 exempts prose by design.
  Round-50 so far: 48 files / 192 lines over 414 files at scan time, again 0 structural. Two consequences: (a) the convention
  "write `~` for the home directory in receipts" is not followed by any seat, and (b) the **L1's own spec generator hardcodes
  the absolute lane path**, so every round's `w1-spec.json`/`w1-dispatch.json` carries it (54 occurrences over 46 lines each in
  round-49;
  the same in round-50 `make-w1-spec.py:12`). If that path is meant to stay out of the public record, fix the generator, not
  the seats.
- **F9 bytecode (S4).** Two `__pycache__/*.pyc` blobs exist in the round-50 tree (`w1/ExecC1Cheats`, `w1/ExecCounterC2R50`).
  They embed the absolute lane home path (1 and 2 occurrences; one 107-character, 11-segment path), and the gate skips binaries
  by declared design, so it would never report them. Both are matched by `.gitignore:3 __pycache__/` (confirmed with
  `git check-ignore`), so they commit only if forced — delete them at seat end and never `git add -f` a seat's `__pycache__`.
  Round-49's committed tree has no binary blob at all.

## 6. Classes measured clean (with the command that says so)

- **Device names**: 14 distinct tokens read with `hyprctl devices -j` (values withheld). Zero capture-borne hits in round-49 or
  round-50; the only matches for any token are pinned upstream wiki pages (`fetch/wiki-Variables.md` and its 5 copies in
  round-49, 2 fetches in round-50) — the wiki's own documented example name.
- **Window titles**: no clients-shaped JSON outside gate selftest constants; no jq-projected `class|title` table in any
  `.txt/.log/.out/.tsv`.
- **Process tables**: 0 `ss` rows, 0 `ps`/`pgrep` headers in receipts; `users:((` appears only in gate constants and in
  checker/probe sources that search for it.
- **Cache text**: 0 record-field pairs (`--title=`, `--working-directory=`, `--app-id=`) in round-49 or round-50; cache touch
  points are digests and masked `~/.cache/…` mentions only. v3's 4 R9 findings are all round-47.
- **Network identity**: 0 private IPv4 literals, 0 MAC-shaped tokens.
- **Monitor serials**: round-49 clean under R3 and R5; v2's and v3's R5 findings are the three held `corpus/knowledge/` entries
  (pre-existing, outside this wave).
- **Structural home paths**: 0 in either wave (`structural_prefix/header/diag/lsrow/bare` all zero).

## 7. Gate tallies for the freeze to cite

| run | v2 | v3 |
|---|---|---|
| `--scope all` at `13631f24` | `files=23274 findings=121` (waived 52) | `files=23274 findings=228` (waived 52) |
| per-rule | R1=40 R2=40 R3=13 R4=3 R5=25 | + R7=49 R8=54 R9=4 |
| round-49 subset | 3 (gate copy) | 4 (gate copy + masked-sample R7) |
| round-50 pre-commit snapshot | 3 (gate copy) | 4 (gate copy + `d2-seat-state` R8) |
| synthetic binds fixture | `files=1 findings=0` rc 0 | `files=1 findings=0` rc 0 |

The 107-finding delta between v2 and v3 on the same revision is exactly the three new rules; none of it is round-49 material
except the masked-sample false positive in §4.

## 8. What I did not do, and the limits of this pass

- I did not run the round-50 counters, the v3 selftest, or any `w2` grading; I did not run a do-nothing control (D4 belongs to
  another seat).
- I did not read `hyprctl clients` (not on the allowed list), so the window-title class is covered by shape and by the gates'
  R1, not by a live title census.
- I did not re-measure the round-49 seat's 24-probe class table; I re-measured its live instances at the committed revision and
  report only what the committed bytes show.
- Round-50 is a live wave: the tree scan is a snapshot (414 files, taken during w1), and seat receipts written after it are not
  in `scan-round50-tree.json`.
