# MadoR19.RerunFetchVerify — partial

Attacked the round-19 fetch-receipt claim by running the round-18 verifier twice: once over the
worktree (the naive invocation) and once over the committed bytes of
`01b80946d92b26370d3012a7da655d00dd135154` extracted with `git archive` to `/tmp`. Then I
recomputed every body digest straight from git objects and independently re-fetched the two
credited URLs.

## Verdict

- **Committed bodies re-hash: holds for the 13 bodies that are actually committed.** All 13
  tracked bodies at the tip reproduce their receipt `sha256` and `bytes` from git blobs.
- **Digest-only bodies reported as such: breaks.** The verifier never reads
  `.ufo/waves/round-19/fetch/.gitignore` (`fetch-verify.py:73` reads only `RETENTION.json`;
  none exists in round-19). No round-19 receipt carries `"retain": "digest-only"`. Both runs
  print `digest_only=0`. In the worktree the 29 gitignored bodies print `ok` (indistinguishable
  from committed bodies); on the committed tree the same 29 print `MISSING`, not `DIGEST_ONLY`.
- **S097 credit: holds.** Full 64-hex sha `dbdd13a6…01786` is in the anchor
  (`corpus/SOURCES.md:109`) and in the committed receipt `SrcS094/colors.toml` whose body is
  committed and re-hashed at the tip. Independent curl: 200, 461 B, same sha.
- **S098 credit: holds only over uncommitted worktree bytes.** On the committed tip the
  verifier prints `ROW S098 UNRECEIPTED body-unverified`: every S098 crate body
  (`DeltaWalkerCli/xdg-3.0.0.crate`, `FrontierRows/xdg-3.0.0.crate`,
  `SrcS084/xdg-3.0.0.crate`, and the untracked `RevRubricVRisk/xdg-3.0.0.crate`) is
  gitignored or untracked, so none is in the commit and none is recognized as digest-only.
  Independent curl: 200, 15,821 B, sha `2fb43323…585b5`, which is the anchor digest
  (`corpus/SOURCES.md:110`) — the fact is true, the committed proof chain is not recognized.
- **Receipt set is not clean at the tip:** `receipts=45 ok=13 bad=32 digest_only=0`, rc=1.
  The worktree run is `receipts=48 ok=45 bad=3 digest_only=0 conflicts=4`, rc=1.

## Commands and outputs

### 1. Silly invocation over the worktree (round-19 fetch root)

```
python3 -I .ufo/waves/round-18/fetch-verify.py \
  --fetch-root .ufo/waves/round-19/fetch [--sources corpus/SOURCES.md --rows S097,S098]
```

Non-ok lines, every one:

```
FETCH HtmlAnchorSweep/s061-archwiki-oldid-1.txt MISSING
FETCH HtmlAnchorSweep/s061-archwiki-oldid-2.txt MISSING
FETCH HtmlAnchorSweep/s061-archwiki-oldid-3.txt MISSING
CONFLICT https://github.com/basecamp/omarchy/tree/v3.8.4/themes/matte-black sha256=78707accce18d8e0d644e9f799362b65814eb75d03b6ea25d3eb47a21d863911,da9070069ea2f44aa68f297d7bd77d08b705479c16a3cc2f7ae9542ae81bf130
CONFLICT https://github.com/basecamp/omarchy/tree/v3.8.4/themes/matte-black/backgrounds sha256=36bfe79b3840e734b317f8151eddea8d809519a9208d95a4352db97deef83c9e,fc8035008c6412feff6854dcb39103dee37e405e443c9dfa904b31486fcbaf96
CONFLICT https://github.com/omacom/omarchy/tree/v3.8.4/themes/matte-black sha256=78707…,da9070…
CONFLICT https://github.com/omacom/omarchy/tree/v3.8.4/themes/matte-black/backgrounds sha256=36bfe7…,fc8035…
SUMMARY receipts=48 ok=45 bad=3 digest_only=0 non200=0 conflicts=4 rows=2 unreceipted=0 quotes=0 quote_bad=0
EXIT=1
```

Rows: `ROW S097 receipted`, `ROW S098 receipted`. Without `--rows`: `ok=45 bad=3
digest_only=0 conflicts=0` and EXIT=1.

Evidence that the 3 `MISSING` bodies are declared digest-only only in prose:
`.ufo/waves/round-19/fetch/HtmlAnchorSweep/WITHHELD.md:1-8` says the three
`s061-archwiki-oldid-{1,2,3}.txt` bodies "remain the digest-only record of the fetches".
`git check-ignore -v` on all three: `NOT-IGNORED`. They are absent from
`fetch/.gitignore:1-30`, absent from the commit, and their receipts
(`fetch/HtmlAnchorSweep/receipts.jsonl:13,14,19`) carry no `retain` key, so the verifier has
no way to classify them. This falsifies the wave-1 acceptance sentence at
`.ufo/waves/round-19/w1/reports/SentinelVcsFixtures.md:160`
("`git check-ignore -v` covers every digest-only body, and `fetch-verify.py` over round-19
prints `DIGEST_ONLY`, not `MISSING`, for the 3 withheld receipts") on both halves.

### 2. Only the committed bytes of the tip

```
git archive --format=tar 01b80946d92b26370d3012a7da655d00dd135154 .ufo/waves/round-19/fetch \
  | tar -x -C /tmp/fv19-tree
python3 -I .ufo/waves/round-18/fetch-verify.py \
  --fetch-root /tmp/fv19-tree/.ufo/waves/round-19/fetch \
  --sources corpus/SOURCES.md --rows S097,S098
```

```
SUMMARY receipts=45 ok=13 bad=32 digest_only=0 non200=0 conflicts=0 rows=2 unreceipted=1
ROW S097 receipted
ROW S098 UNRECEIPTED body-unverified
EXIT=1
```

The tip contains 23 files under `fetch/` (`git ls-tree -r … .ufo/waves/round-19/fetch | wc -l`
= 23), 13 of them bodies. The 32 `MISSING` receipts are:

- 29 bodies present only as gitignored local files: `CriticC1/{wiki-hypridle-1,wiki-hypridle-2,
  docsrs-xdg-latest-1,docsrs-xdg-latest-2}.html`; `DeltaWalkerCli/xdg-3.0.0.crate`;
  `FrontierRows/xdg-3.0.0.crate`; `HtmlAnchorSweep/{s094-tree-a-1,s094-tree-a-2,s094-tree-b-1,
  s094-tree-b-2,s063-hypridle-1,s063-hypridle-2,s064-hyprlock-1,s064-hyprlock-2,
  s084-docsrs-latest-1,s084-docsrs-latest-2,s084-docsrs-300,s061-archwiki-raw}.html`,
  `HtmlAnchorSweep/s062-linuxjunkies.html`, `HtmlAnchorSweep/s062-linuxjunkies-2.html`,
  `HtmlAnchorSweep/s062-linuxjunkies-3.html`, `HtmlAnchorSweep/s061-archwiki-api.json`;
  `MadoR19.UnpinnedUrlSweep/{xdg-latest,xdg-3.0.0,hypridle,hypridle-repeat,hyprlock,
  screencast-v6}.html`; `SrcS084/xdg-3.0.0.crate`.
- 3 absent-everywhere bodies: `HtmlAnchorSweep/s061-archwiki-oldid-{1,2,3}.txt`.

Notably `conflicts=0` here is **not** an all-clear: `build_conflicts` skips entries whose status
is not `ok`/`DIGEST_ONLY` (`fetch-verify.py:215`), so removing every tree-page body from the
commit also removes the four R18-V1 URL conflicts from the report. On the worktree those same
receipts are `ok` and the four conflicts appear. A committed-tip run therefore hides the very
durable-anchor signal the rule exists to emit.

### 3. Committed-byte re-hash audit (independent of the tool)

For each of the 48 receipts I resolved `<tip>:<path>` with `git cat-file -p` and hashed the
blob (script in /tmp, output summarized):

- `tracked-ok` 13/13: `DeltaWalkerCli/{v2.17.0,v2.17.2}-{src_main.rs,src_data.rs,Cargo.toml}`,
  `DeltaWalkerConfig/resources-config-{v2.17.0,v2.17.1,v2.17.2,commit-a515085}.toml`,
  `SrcS084/{walker-v2.17.2-Cargo.lock,walker-v2.17.2-src-config.rs}`, `SrcS094/colors.toml`.
  Every committed blob's sha256 and byte length equal the receipt.
- `ignored` 29: not in the commit (matches the `MISSING` list above).
- `local-only` 3: `RevRubricVRisk/{omarchy-v3.8.4-matte-black-colors.toml,
  walker-v2.17.2-Cargo.lock, xdg-3.0.0.crate}` — the whole seat directory is untracked
  (`git status --porcelain` → `?? .ufo/waves/round-19/fetch/RevRubricVRisk/`; `git ls-tree` at
  the tip → 0 files). The worktree run reports those three receipts `ok`, so the `ok=45`
  figure silently includes 3 receipts and 3 bodies that do not exist at `01b8094`.

### 4. S097 / S098 credit chain

| row | anchor line | anchor digest | receipt | body committed? | verifier |
|---|---|---|---|---|---|
| S097 | `corpus/SOURCES.md:109` (`raw themes/matte-black/colors.toml sha256 dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786`) | full sha present | `SrcS094/receipts.jsonl:1` (200, 461 B, `dbdd13a6…01786`, url `…/v3.8.4/themes/matte-black/colors.toml`) | yes, `tracked-ok` | `ROW S097 receipted` in both runs |
| S098 | `corpus/SOURCES.md:110` (`xdg 3.0.0, checksum 2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5; … crate 15,821 B sha256 2fb43323…585b5`) | full sha present twice | `SrcS084/receipts.jsonl:2` and 3 siblings (200, 15,821 B, `2fb43323…585b5`) | no (all gitignored/untracked) | receipted on worktree, `UNRECEIPTED body-unverified` on committed tip |

`DIGEST_RE` requires ≥16 hex, so the 12-hex git blob prefix `colors.toml 5e1a8ccae846…` in the
S097 anchor cannot grant credit; the credit comes from the explicit full-sha clause quoted
above. So the credit is not accidental-prefix noise.

Independent fetches (`curl`, no auth; bodies under `/tmp/fv19`, never in the lane):

```
fetched_at=2026-10-20T18:03:55Z url=https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml http=200 bytes=461 sha256=dbdd13a629aac86daa0f01ad03b66429d9e4b303758ea464c8bcc917a5601786
fetched_at=2026-10-20T18:03:55Z url=https://static.crates.io/crates/xdg/xdg-3.0.0.crate http=200 bytes=15821 sha256=2fb433233f2df9344722454bc7e96465c9d03bff9d77c248f9e7523fe79585b5
```

Both match receipt and anchor exactly.

### 5. Supersession wording

`fetch-verify.py` has no status/supersession awareness; it prints
`ROW S094 receipted` and `ROW S084 receipted` for `--rows S094,S084` even though both rows are
status `rejected` at the tip (`corpus/SOURCES.md:96` and `:106`, status cell =
`rejected`). That does not falsify "S094/S084 now rejected", but "receipted" from this tool
must never be read as "accepted"; the rejection lives only in the registry status cell and in
`supersessions.json` (which lists walker 2.17.0→2.17.2 only, no S094/S084 entry).

## Root causes (path:line)

- `fetch-verify.py:73` `RETENTION_NAME = "RETENTION.json"`; `:89-112` `load_retention` reads
  only that file from the fetch root. Round-19 has none (`ls
  .ufo/waves/round-19/fetch/RETENTION.json` → ENOENT), and `.gitignore:1-30` is invisible to
  the verifier.
- `fetch-verify.py:118-121` `is_digest_only` requires `(seat, body)` in that retention set or
  `rec["retain"] == "digest-only"`; all 48 receipts have no `retain` field.
- `fetch-verify.py:132-135`: missing body without a retention entry is `MISSING`; `DIGEST_ONLY`
  is unreachable in this tree, hence `digest_only=0` at `:454-456`.
- `fetch-verify.py:215` and `:239`: non-`ok`/non-`DIGEST_ONLY` receipts are dropped from
  conflict detection and credit. Consequences: committed-tip conflicts collapse to 0; S098
  loses all credit.
- `fetch-verify.py:251-262` `uncredited_reason` labels S098 `body-unverified`, which hides that
  the actual cause is "body not committed and not registered digest-only".

## What would make it honest

1. A committed `fetch/RETENTION.json` (or `"retain":"digest-only"` on each receipt) covering
   the 29 `.gitignore` bodies and the three `s061-archwiki-oldid-*.txt` bodies, and a
   verifier that reads it; only then does `DIGEST_ONLY` replace both the false `ok` and the
   false `MISSING`.
2. State credited receipts with their commit status: S097 is backed by a committed body;
   S098 is backed by an uncommitted, gitignored crate body only, and the tip verifier says
   `UNRECEIPTED`.
3. Never quote `receipts=48 ok=45` as a committed-tip result: 45 ok = 13 committed +
   29 ignored + 3 untracked-seat receipts.

## Limits

- Only rows S097, S098 (plus S094/S084 for the supersession wording) were joined; I did not
  re-run all row joins over `corpus/SOURCES.md`.
- Receipt `http_status` and timestamps are self-declared. I independently re-fetched the two
  credited URLs only; current bodies match the anchors, which is consistent with, not proof
  of, the round-19 fetch-time claim (colors.toml sits behind a tag that upstream could move;
  crates.io versions are immutable). [INFERENCE]
- The worktree may have advanced during the run; all tip claims were read from `git` at
  `01b80946d92b26370d3012a7da655d00dd135154`, and the untracked wave-2 `RevRubricVRisk` seat
  was reported as found.
- I did not run the gate, jj, or any mutating lane command; host pause respected.
- No installs were needed or made.

## Installs

none
