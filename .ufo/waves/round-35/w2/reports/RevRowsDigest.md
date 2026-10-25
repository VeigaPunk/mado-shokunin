# RevRowsDigest — receipt digests vs anchor cells vs frozen.json (PRED-C1-r35-v1)

Seat: reviewer (leaf, no dispatch). Round 35, wave 2 — falsify. Date: 2026-10-25.
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Everything below is read-only on the
lane; every mutation lives under
`.ufo/waves/round-35/scratch/RevRowsDigest/`. Repro driver:
`.ufo/waves/round-35/scratch/RevRowsDigest/run.sh`; captured output:
`.../scratch/RevRowsDigest/evidence.txt`.

## Axes

1. **Digest fidelity** — does each receipt's bytes hash to `frozen.json.receipts[<id>].sha256`?
2. **Anchor fidelity** — does the live registry row's anchor cell carry the digest of the
   file that anchor names (not of another file)?
3. **Freeze integrity** — did any cited file's bytes change after the freeze commit, and did
   the anchor cells themselves exist at freeze?
4. **Clause fidelity** — does the counter's `digest-match` clause test what its `why` says?

## 3-column table (recomputed sha256 vs anchor cell vs frozen.json)

Command: `for s in S203..S210; do sha256sum .ufo/waves/round-35/fetch/$s.receipt.txt; done`
plus the anchor cell of each row (column 6 of `corpus/SOURCES.md`, header-indexed — cells are
`id|source|kind|tier|scope|anchor|teaches|status|opened|recheck|used-by`).

| id (receipt) | recomputed sha256 (working tree) | anchor cell digest = frozen.json |
|---|---|---|
| S203 | `1b7fa87ffe933990ee59acf3629ffbe3a90106bc9ebcce082237f7f495dd1646` | yes — identical |
| S204 | `4cd5ba6518e4a6d950fcb510d2482e33be78abb20d22bef41d21a66f7d1c54ad` | yes — identical |
| S205 | `f3387bfcbac79016034be38bab6548ae31df5860e5aafaa03105aca84b08ae1a` | yes — identical |
| S206 | `1d30e4a999b53d5288369edc7573d7ceee0aef99570a55d781c4625440a938d5` | yes — identical |
| S207 | `81c33e7926f0bad071d31e9fc67e1d06967e3142da40ea3c93b16510b0adec59` | yes — identical |
| S208 | `6e72f0db3d7bbfecf4096b0aa22f716f417c00caa50b6d3319106387d6ce4654` | yes — identical |
| S209 | `a170c7a50b9305b3448fc85ecddb0d7b1f1c3ff5e42c78cdc2d07718c3bdd27c` | yes — identical |
| S210 | `ef282e386cdfb686fd331f4ed2fa7f0a33faf3ef4714844639b3eee4790b8726` | yes — identical |

8/8 recompute; 8/8 anchor cells equal the frozen digest **and** the row names its own
receipt path. Live data is clean on axes 1 and 2. Supplementary evidence (axis 3), from
`evidence.txt` §1–§2:

| id | worktree == frozen | `git cat-file -p HEAD:…receipt` == frozen | worktree == HEAD |
|---|---|---|---|
| S203–S210 (all 8) | OK | OK | identical (`git diff HEAD --numstat -- .ufo/waves/round-35/fetch/` empty) |

So on the live tree the answer to "does any row's anchor cite a file whose bytes changed
after freeze?" is **no** — and for the receipts it is *proven*, not sampled: the bytes in
commit `19e4ab3` (the freeze commit) hash to the same digest as the bytes on disk.

## Findings

### F1 — HIGH (confirms and extends w1 `CritVacuous`): `digest-match` tests a frozen literal, not the file

`c1/count.py:174` computes `digest = hashlib.sha256(blob).hexdigest()` and never reads it
(`grep -cw digest c1/count.py` → `1`). The only anchor test is `c1/count.py:192`
`receipt["sha256"] in cs[5]` — substring containment of the *frozen* digest in the anchor
cell. Receipt bytes are never hashed into the verdict.

Falsifier **m1** (`run.sh` §3): append `\nMUTATED-AFTER-FREEZE\n` to
`S210.receipt.txt` (actual sha becomes `32754fd8…e84488`, frozen stays `ef282e38…0b8726`),
leave the anchor and `frozen.json` untouched:

```
$ python3 -I .ufo/waves/round-35/c1/count.py --root .../scratch/RevRowsDigest/m1 \
    --frozen .ufo/waves/round-35/c1/frozen.json
PRED-C1-r35-v1 closed_entries=3 closed_rows=8 open_cites=0 verdict=TARGET_MET
exit=0
```

C1 therefore **cannot answer** the freeze question on axis 3; its digest clause is a
self-quotation of the registry. Fix: `and digest == receipt["sha256"]` (one token, turns
line 174 from dead code into the clause the ledger claims).

### F2 — HIGH (new): the anchor's *named* file is not bound to the digest it carries

Clause text: "the row's anchor cell carries the sha256 of **the named receipt**". The
implementation never parses which file the anchor names. Two falsifiers, both `TARGET_MET`
exit 0:

- **m2** — S207's anchor rewritten to name `S208.receipt.txt` while keeping S207's frozen
  digest (`81c33e79…`). A reader sees a digest that is not S208's; the counter sees
  `receipt["sha256"] in cs[5]` and closes the row.
- **m3** — S209's anchor rewritten to name no file at all
  (`section per-copy handler count; anonymous sha256 a170c7a5…`). Still `TARGET_MET`.

So a "digest of the wrong file" is accepted whenever the frozen literal is present anywhere
in the cell, with or without a path. w1 `ExecDigest`'s statement that "each anchor also names
the same receipt path it hashes" is true of the live data by inspection, but is **not
enforced** — it is an observation, not a clause. Consider making it one (require the anchor
to contain `fetch/<sid>.receipt.txt` adjacent to the digest, e.g. a strict
`receipt <path> sha256 <hex>` grammar).

### F3 — MEDIUM (new): digests of host files inside anchor cells are unverified and unpinned

Five anchor cells also carry host-file digests (S203 `omarchy-first-run`, S205
`hypridle.conf`, S206 `config.jsonc`, S207 `idle.sh`, S208 `omarchy-menu`). No counter hashes
those. Falsifier **m4**: replace S206's `config.jsonc` digest with `idle.sh`'s digest →
`TARGET_MET` exit 0.

Live values are correct as measured now, and their mtimes predate the freeze:

| id | file | bytes claimed / actual | sha256 actual | anchor digest | mtime |
|---|---|---|---|---|---|
| S203 | `…/omarchy/bin/omarchy-first-run` | 1089 / 1089 | `20508471…a062630` | equal | 2026-10-03T17:42 |
| S205 | `~/.config/hypr/hypridle.conf` | — / 765 | `e7d3b8dd…07de41` | equal | 2026-10-03T17:44 |
| S206 | `~/.config/waybar/config.jsonc` | 6354 / 6354 | `a408a33d…aae829` | equal | 2026-10-17T17:02 |
| S207 | `…/indicators/idle.sh` | 159 / 159 | `6d8d2c11…f0f1750` | equal | 2026-10-03T17:42 |
| S208 | `…/omarchy/bin/omarchy-menu` | 33017 / 33017 | `d196b086…a0f79d` | equal | 2026-10-03T17:42 |

All five are pre-freeze (`freeze_epoch` = 2026-10-24T23:23:32), so no cited host file changed
after freeze either. But because these files live outside git, the anchor digest is their
*only* pin and C1 never checks it; a wrong digest silently passes (m4).

### F4 — MEDIUM (freeze shape; by design, but the residual risk is real): the anchor cells did not exist at freeze

```
$ git show HEAD:corpus/SOURCES.md | grep -cE '^\| S2(0[3-9]|10) '
0
$ grep -cE '^\| S2(0[3-9]|10) ' corpus/SOURCES.md
8
$ git diff HEAD --numstat -- corpus/SOURCES.md
8       0       corpus/SOURCES.md
```

The 8 rows are additions-only, uncommitted (` M corpus/SOURCES.md`), visible in the jj working
snapshot `d2b6972` (child of `19e4ab3`, kept at `refs/jj/keep/d2b6972…`). Round-35
`registration.md` §Non-negotiables says the predicates are frozen *before the data lands*, so
post-freeze data is intended. The consequence still belongs on the record: no commit pins the
anchor bytes, so `closed_rows=8` holds only for the current uncommitted tree, and the only
freeze-grade pin is `frozen.json`'s receipt digest — which F1 shows is not compared to
receipt bytes. Committing the registry append (as round 34 did for its data) would close this.

### F5 — MEDIUM (new): `frozen.json` itself is unpinned; digest re-pointing is accepted

The counter checks only that `predicate` and `target` strings match, then trusts every digest
in the file. Falsifier **m5**: mutate `S208.receipt.txt` (new sha `2b1a0387…95c43e`),
re-point both the anchor cell *and* the `S208` digest inside a copy of `frozen.json`:
`TARGET_MET`, exit 0. This is not a counter bug — a re-freeze must change the spec — but it
means "anchor digest == file bytes" can be restored by editing two unversioned files in
lockstep. Any integrity claim over C1 must name `19e4ab3` (where `frozen.json` and all eight
receipts are committed) as the pin, not `frozen.json` alone.

## Non-findings (checked, clean)

- No live anchor carries a wrong-file digest: all eight receipt digests match the bytes of the
  file their row names, and all five host-file digests match the files they name.
- No receipt is a symlink or multiply-linked: `stat -c '%h %F'` → `nlink=1 regular file` for all
  eight, so `read_regular`'s regular-file gate is satisfied by the real data.
- No receipt row is duplicated or cross-cited: each `fetch/S2xx.receipt.txt` appears in exactly
  one registry row (`S203→205`, …, `S210→212`), and each row has 11 cells.
- Control `controls/c1-digest` is honest *for the clause as implemented*: its S210 anchor is
  `sha256 000…0`, instrumented run shows `digest_in_anchor=False` and only that clause flips
  (`closed_rows=7 open_cites=1`, exit 1). The gap is the clause's wording (F1/F2), not a fake
  control.

## Residual risk and verification gaps

- The digest pin is only as strong as git's unmodified-ness: `git diff HEAD` empty for
  `fetch/` is a working-tree comparison, not a signed attestation; no GPG/signature verified.
- mtimes were used only as corroboration for host files; the receipts' freeze claim rests on
  the `HEAD` blob hashes, not on mtimes.
- Out of scope for this seat: gate-quote substrings and word bounds, `used-by` token sets,
  recheck cadence, the three entries' post-freeze bytes (mtime 2026-10-25T03:25:52, other
  seats), and C2. Not exercised here, not claimed.
- Tooling: no installs or upgrades performed (only `python3 -I`, `git`, `sha256sum`, `stat`,
  `grep`, `awk` already present). No `pacman` transaction was attempted.

## Verdict

For the live data: **PASS on axes 1–2** (8/8 receipts recompute, 8/8 anchors carry the digest
of the file they name, and the receipts are byte-identical to the freeze commit), **PASS on
axis 3 for the receipts** (no post-freeze byte change; no cited host file post-dates freeze),
with the caveat that the anchor rows themselves are post-freeze, uncommitted additions.
For the counter: **FAIL on axis 4** — the `digest-match` clause neither hashes the receipt nor
binds the anchor's named path, so a receipt mutated after freeze (m1), an anchor naming the
wrong file (m2), an anchor naming no file (m3), a wrong host-file digest (m4), and a doubly
re-pointed `frozen.json` (m5) all still print `TARGET_MET` with exit 0. The claim's live numbers
are currently corroborated by out-of-band git evidence, not by the predicate itself.
