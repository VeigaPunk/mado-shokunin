# FetchVerify — receipt verifier for round-18 fetches

Seat: MadoR18.FetchVerify (executor, leaf). Scope: one script + this report.

## Delivered

| path | sha256 | note |
|---|---|---|
| `.ufo/waves/round-18/fetch-verify.py` | `f0e91f10649685544d534e4610302f2180a5ac42a92ffde5d154af6ec2cc10e3` | stdlib only, `python3 -I` clean |

No other lane file touched; no tool installed or upgraded. No lane gate was run.

## Behaviour

Default fetch root is resolved from the script's own location
(`<script dir>/fetch`), so it works from any cwd:

```
python3 -I .ufo/waves/round-18/fetch-verify.py
```

It walks `<fetch-root>/*/receipts.jsonl` (sorted), skips blank lines, and per
receipt line prints exactly one:

```
FETCH <seat>/<body> ok|BAD_SHA|BAD_BYTES|MISSING|BAD_SCHEMA|BAD_JSON
```

Checks, in order: schema == `mado-fetch-receipt-v1` and a safe `body` slug
(no absolute path, no `..`, no `/`) → `BAD_SCHEMA`; body file present →
`MISSING`; `os.stat().st_size` equals the integer `bytes` → `BAD_BYTES`;
sha256 of the body equals `sha256` → `BAD_SHA`. Failure lines append
`want=… got=…` after the status token. Unparseable JSONL lines are
`<line N> BAD_JSON`.

Optional SOURCES join and quote check:

```
python3 -I .ufo/waves/round-18/fetch-verify.py \
  --sources corpus/SOURCES.md --rows S072,S073 \
  --quote 'S072=<verbatim text>' --quote 'S073=<other text>'
```

- `ROW <id> receipted|UNRECEIPTED` — a row is receipted when at least one
  receipt **whose body verified ok** either has a `sha256` appearing literally
  in the row's anchor cell (11-column table, cell 6) or has `url`/`final_url`
  exactly equal to a URL in the row's source cell (cell 2).
- `QUOTE <id> ok|NOT_FOUND|UNRECEIPTED` — the UTF-8 text occurs in at least one
  body of the row's matched receipts. Quote-only row ids are validated against
  SOURCES.md but do not emit a `ROW` line.
- A listed row id absent from SOURCES.md is a usage error, not a silent
  `UNRECEIPTED` (drafts writing `S0xx-pending` cannot be credited by accident).
- Summary: `SUMMARY receipts=N ok=N bad=N rows=N unreceipted=N quotes=N quote_bad=N`.
- Exit 0 when every receipt ok, every listed row receipted and every quote
  found; 1 on any bad receipt / unreceipted row / missing quote; 2 on usage
  (missing `--sources` for `--rows`/`--quote`, bad quote spec, unknown row id,
  fetch root not a directory).

## Retained evidence (all commands run 2026-10-20, /tmp fixtures)

Fixture `/tmp/fv-3092` (2 seats: one ok body, one ok + one missing body, one
byte-short body with wrong sha, one correct-length wrong-sha body, one
non-JSON line) and `/tmp/fv-clean` (clean + empty `receipts.jsonl` seat),
`/tmp/fv-evil` (hostile body paths), `/tmp/fv-badrow` (row whose only receipt
fails sha):

```
$ python3 -I .ufo/waves/round-18/fetch-verify.py --fetch-root /tmp/fv-3092/fetch \
    --sources /tmp/fv-3092/SOURCES.md --rows S072,S073,S074 --quote 'S073=bravo'
FETCH SeatA/body.txt ok
FETCH SeatB/body.txt ok
FETCH SeatB/absent.txt MISSING
FETCH SeatB/wrongsha.txt BAD_BYTES want=3 got=15
FETCH SeatB/wrongsha.txt BAD_SHA want=000…000 got=d9a23f75…
FETCH SeatB/<line 5> BAD_JSON
ROW S072 receipted
ROW S073 receipted
ROW S074 UNRECEIPTED
QUOTE S073 ok
SUMMARY receipts=6 ok=2 bad=4 rows=3 unreceipted=1 quotes=1 quote_bad=0
exit=1

$ … --fetch-root /tmp/fv-clean/fetch --sources /tmp/fv-clean/SOURCES.md \
    --rows S080,S081 --quote 'S081=quote here'
FETCH S1/a.txt ok
ROW S080 receipted        # matched by url https://e.org/x
ROW S081 receipted        # matched by url https://e.org/y (final_url)
QUOTE S081 ok
SUMMARY receipts=1 ok=1 bad=0 rows=2 unreceipted=0 quotes=1 quote_bad=0
exit=0

$ … --fetch-root /tmp/fv-evil/fetch
FETCH E/<line 1> BAD_SCHEMA bad-body-field     # body "/etc/passwd"
FETCH E/<line 2> BAD_SCHEMA bad-body-field     # body "../x.txt"
FETCH E/<line 3> BAD_SCHEMA bad-body-field     # body "sub/x.txt"
FETCH E/x.txt BAD_SHA want=aa got=73cb3858…
FETCH E/x.txt BAD_BYTES want='2' got=2        # string bytes field
exit=1

$ … --fetch-root /tmp/fv-badrow/fetch --sources /tmp/fv-badrow/SOURCES.md \
    --rows S090 --quote 'S090=body'
FETCH Q/b.txt BAD_SHA …
ROW S090 UNRECEIPTED       # bad body never credits a row
QUOTE S090 UNRECEIPTED
exit=1

usage paths: --rows without --sources → 2; bad --quote spec → 2;
unknown row id → 2 (before any FETCH output); missing fetch root → 2.
```

Real tree, read-only snapshot at 2026-10-20T15:45:32Z (21 seat dirs, 294
receipt lines, wave still writing):

```
$ cd /tmp && python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/fetch-verify.py | tail -1
SUMMARY receipts=294 ok=294 bad=0 rows=0 unreceipted=0 quotes=0 quote_bad=0
exit=0
```

Real SOURCES join against the rows that currently carry round-18 receipted
URLs/sha256 (S056–S069, round-17 backfill rows):

```
$ python3 -I .ufo/waves/round-18/fetch-verify.py --sources corpus/SOURCES.md \
    --rows S056,S057,S058,S063,S064,S065,S066,S067,S068,S069 --quote 'S063=inhibit_sleep'
ROW S056 receipted … ROW S069 receipted     # all 10
QUOTE S063 ok
SUMMARY receipts=288 ok=288 bad=0 rows=10 unreceipted=0 quotes=1 quote_bad=0
exit=0
```
(the 288 vs 294 delta is the wave writing receipts between the two runs.)

## Risks / limits

- **Snapshot, not a lock.** Seats write `receipts.jsonl` and bodies while this
  runs; a line read mid-write is `BAD_JSON`, a receipt whose body lands later
  is `MISSING`. Re-run after the wave settles for the verdict that counts.
- **Anchor credit is literal.** Only a full 64-hex `sha256` appearing verbatim
  in the anchor cell credits by hash. Truncated anchors (`sha256 abcd…`) credit
  only through URL equality. Extending to truncated prefixes was deliberately
  not done (collision/false-credit risk).
- **URL credit is exact string equality** against URLs found in the source
  cell, after stripping trailing `).,;:!`. Redirect-only equivalence is covered
  by `final_url`; no normalization of `http`/`https` or trailing slash.
- **S072–S099 do not exist yet** in `corpus/SOURCES.md` (L1 assignment), so
  `--rows S072` currently exits 2 `row S072 not found`. That is intended: it
  must fail loud until the row lands.
- Verifier checks receipt self-consistency (body bytes/sha), not that the URL
  was fetched with a pinned tag or that the body supports a quote's meaning;
  quote matching is byte-substring only.
- No blockers.
