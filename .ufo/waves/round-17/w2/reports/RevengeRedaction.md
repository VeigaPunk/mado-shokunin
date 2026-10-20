# Mado R17 W2 — RevengeRedaction

Attack: is the redaction in `evidence/tripwire-r1*.txt` real, and did any secret-shaped
value survive? Lane HEAD `988b858` (pushed). Read-only; **installs: none**.

## Answer in one line

**There are zero `<redacted>` occurrences in the five named files** (and in all ten
`tripwire-*.txt` receipts), so no replaced-token kind can be listed for them; and
**no credential-shaped value survived** in any field. The attack fails on both prongs.
The markers that do exist in round 17 live in the sibling `oracle-*.json` evidence and
every one of the 15 replaced a benign identifier (VCS SHA or filename stem), not a secret.

## 1. Scope and what the glob actually selects

`evidence/tripwire-r1*.txt` → 5 files; each is `MADO_TRIPWIRE: <label>` on line 1 and the
verdict JSON on line 2. Worktree bytes are identical to the blobs committed in `988b858`
(`git show HEAD:… | sha256sum` compared per file: all five match).

| file | bytes | sha256 (first 16) | findings | scanned files |
|---|---|---|---|---|
| `tripwire-r13.txt` | 24000 | `81f0632d3868092a` | 33 | 33 |
| `tripwire-r14.txt` | 31314 | `033bdd9419d4a786` | 50 | 33 |
| `tripwire-r15.txt` | 102349 | `fa186db1c8937cbc` | 208 | 65 |
| `tripwire-r16.txt` | 32940 | `496700fc0b7bc609` | 2 | 97 |
| `tripwire-r17-w1.txt` | 23470 | `793bf4cf4120789b` | 0 | 70 |

293 findings, 298 `files[]` entries, `schema = mado-tripwire-verdict-v1`.

## 2. Occurrence inventory

- Raw byte grep `<redacted>`: **0** in each of the five files; **0** across all ten
  `tripwire-*.txt` (adds `anchor-r15`, `pacmanlog-join`, `selftest-core`,
  `selftest-compound`, `selftest-hardening`).
- Spelling sweep for any alternate marker (`redact*`, `[redacted]`, `***`, `censored`,
  `[hidden]`, `<hidden>`): **0 hits anywhere**. There is no differently-spelled marker.
- Parsed-JSON sweep: every `findings[].command` value inspected individually → 0 contain
  the marker.

So: nothing was replaced in these files. There is no source-transcript line that a marker
points at, and therefore no "kind of token it replaced" to enumerate for this glob.

### Why the zero is structural, not luck

`tools/mado-tripwire.py` at `988b858`:

- `SECRET_PATTERNS` (`:89-94`): (1) `://user:pass@` userinfo, (2) `AKIA[0-9A-Z]{16}`,
  (3) **any** `[A-Za-z0-9_\-]{32,}` run.
- `redact()` (`:101-105`) applies those in order, then non-printable→`?`, then truncates
  to `MAX_COMMAND = 240`.
- `redact(text)` is wired into the only place a command is emitted —
  `"argv0": argv0, "command": redact(text)` at `:687`.

Measured on the emitted data:

- Longest contiguous `[A-Za-z0-9_\-]` run inside **any** of the 293 emitted `command`
  values: **27** (`r15`), 19 (`r14`), 18 (`r13`), 6 (`r16`). All below 32, so pattern 3
  cannot fire on any of them.
- Longest `command` length: **164** chars (`r14`), 162 (`r15`), 79 (`r13`), 18 (`r16`) —
  the 240-char truncation never engaged, so nothing was hidden by truncation either.
- Patterns 1 and 2 have no match in any emitted command.
- Idempotence test: re-running the tool's own three patterns over all 293 emitted commands
  changes **0** of them. Nothing the tool's own rule set would have caught survived.

### Why the leak surface is even smaller than the marker count suggests

`findings[].command` is `text = " ".join(seg)` for **one simple-command segment**
(`classify_segment`, `:368-379`), not the whole logical line. A secret sitting in a sibling
segment of the same command (e.g. `pacman -Q foo && curl https://user:pass@host`, or
`pacman -Q x && PGPASSWORD=… psql`) is never copied into the verdict at all. Verified on a
`/tmp` fixture: only the violating segment appears.

## 3. Secret-shaped values that survived — full list, kinds only

Detectors run over **every field of every record plus the raw file bytes**: userinfo URL,
`AKIA…`, 32+ runs, JWT, `Bearer`, `Authorization: Basic`, `PASSWORD/PASSWD/SECRET/TOKEN/
API_KEY/ACCESS_KEY=…`, `PGPASSWORD`/`MYSQL_PWD`, `--password`/`-p`, `x-api-key`/
`access_token`, URL `?key=/token=/sig=/auth=`, `BEGIN … PRIVATE KEY`, `ghp_*/sk-*`, e-mail.
**Credential-shaped matches: 0.**

High-entropy tokens that *are* present, with the field that scopes them and their kind
(values never reproduced):

1. `files[].sha256` — 64-hex content digests of the scanned `.jsonl` (298). Public digests.
2. `files[].path`, `findings[].file` — session directory `…/2026-10-20T…Z_<uuid>/…` plus
   `-Projects-shokunin`; the timestamp+UUID is one 60-char `[A-Za-z0-9_-]` run. Operator
   path, not a credential.
3. `findings[].tool_call_id` — provider call IDs. 29 distinct values ≥40 chars:
   `0_tool_<uuid>` (40) and `call_<32hex>|fc_<32hex>` (91). Longest run 53. These runs are
   exactly the class pattern 3 would replace: applying `redact()` record-wide would alter
   **334 non-command fields** (38/78/214/4 for r13/r14/r15/r16). They are call identifiers,
   not secrets — but they show redaction is field-scoped to `command`, not record-scoped.
4. `pacman -Qo <path>` arguments that trip a loose base64 detector (10 hits: r14 ×3,
   r15 ×7) — all filesystem paths (`/usr/share/wayland-*`, `…/xkbcommon.h`, `libinput.1.gz`).
   False positives, not encoded material.

No e-mail address, no key material, no authorization header value, no URL userinfo in any
field. The C3 anchor receipt `tripwire-anchor-r15.txt` is also marker-free and its
`line 54 / call_38165` command renders in full as an ordinary `sudo pacman -S …` install
line with no embedded secret.

## 4. Where the marker *does* exist in round 17 (adjacent evidence, outside the named glob)

`evidence/oracle-r13-r14.json` (7), `oracle-r15.json` (6), `oracle-r16.json` (2) — 15
markers total. Each was joined back to its source transcript line (root = the file's
`session_dir` / `scope.scan_root`, plus the `MadoR14/`-`MadoR15/`-`MadoR16/` subdirectory)
and the replaced token was recovered by anchoring on the 20 chars before/after the marker.
Kinds only:

| replaced token kind | count | context |
|---|---|---|
| 40-hex git commit SHA | 6 | ref position in `raw.githubusercontent.com/…/<sha>/…` and GitLab `…?ref=<sha>` / `…/raw/<sha>/…` |
| filename / path stem, 19–61 chars | 9 | protocol `.xml` stem, generated `.hpp` stem, `corpus/knowledge/*.md` stem, session directory name, 33-char stems |

Zero credentials. So in round-17 evidence the redactor fired **only** on benign
identifiers, because pattern 3 is a pure length heuristic: a 40-hex VCS SHA and a
33-char filename are indistinguishable from a token to it. This is over-redaction
(evidence legibility loss), not a leak.

## 5. Latent blind spots (proven on /tmp fixtures; none observed in shipped evidence)

Ran the permitted tool `python3 -I …/mado-tripwire.py --scan /tmp/redactfix/*.jsonl` on
synthetic transcripts whose violating segment carries a fake secret:

- Fires correctly: `https://alice:<pw>@host` → `https://<redacted>@host`;
  `AWS_ACCESS_KEY_ID=AKIA…` → `<redacted>`; 32+ run (`ghp_…`, 40-hex SHA, 32-char filename)
  → `<redacted>`; a benign 32-char `.so` filename is also redacted (over-redaction).
- Does **not** fire: `PGPASSWORD=hunter2`, `Authorization: Basic <18-char b64>`,
  `Authorization: Bearer <18-char token>` — all survive verbatim, because none contains a
  32-char run and none is `://user:pass@` or `AKIA…`.

Consequence: the pattern set is length-biased — it removes long hashes/refs/filenames and
publishes short credentials. That is a real weakness of the mechanism, but it is **not an
observed leak** in the five named files, where no such value was ever emitted.

## 6. Verdict and confidence

- **Attack failed.** No `<redacted>` occurrence exists in `tripwire-r1*.txt`, so there is
  no replaced-token kind to report for them; and no secret-shaped credential survived in
  the files' bytes or in any field.
- The absence of markers is provable from the data (max run 27 < 32 threshold; no
  userinfo/AKIA; 0 changes under re-redaction), not merely an unexamined gap.
- Two findings worth carrying as observations, not as leaks: (a) redaction is applied to
  `command` only, so 334 other fields would change if it were record-scoped (call IDs,
  session UUIDs); (b) in sibling `oracle-*` evidence all 15 markers replaced benign SHAs or
  filename stems, and short-credential forms pass through untouched.
- Confidence: high for "zero markers / no credential survived" (byte grep, parsed-JSON
  walk, detector sweep, idempotence test, source-line join all agree). Medium-high for the
  kind attribution of the 15 adjacent markers: prefix/suffix anchoring is exact for all 15,
  but 2 of the 9 stems could not be distinguished between "filename" and "path component"
  beyond their character class.

Method limits: lane files untouched; only the contract-permitted `--scan` was executed
(against a `/tmp` fixture, never the lane); no package manager, compositor, or session tool
was invoked at all.
