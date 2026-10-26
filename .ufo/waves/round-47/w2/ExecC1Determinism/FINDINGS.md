# ExecC1Determinism — C1 determinism: readdir order, filesystem, locale (round 47, wave w2, FALSIFY)

Seat: leaf executor, policy v1. Claim under attack: **C1 (operability)** — `tools/mado-terminal.py` reproduces
xdg-terminal-exec v0.14.3's selection; frozen counter `quality/counters/c1-r47-terminal.py` (PRED-C1-r47), claim frozen at
`d7527d608ad2b2e3cc398fdde34db7947b254a1a` over base `60edb66e2f1cb90acc6e9442fc93ded0ca42d750`. No data commit exists.
Judge used: the real pinned script `.ufo/waves/round-47/fetch/xdg-terminal-exec`, sha256
`89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac`, in bwrap (the counter's own sandbox).

**Verdict of this seat: no determinism drift found in the count or in the reference tool; one *coverage* hole found in
the frozen fixture set — clause f/x are blind to the readdir axis, so a tool that sorts directory entries instead of
reading the filesystem order passes all 190 fixtures and all 190 explain checks.** Details and repros below.

## What was run (candidate = the L1 reference, unchanged)

```
D=$(mktemp -d -p /fast/scratch/hyaku/mado-r47/ExecC1Determinism)
git clone -q --shared --no-checkout /home/vgpnk/Projects/shokunin/mado-shokunin "$D"
test "$(git -C "$D" rev-parse --show-toplevel)" = "$D"
git -C "$D" checkout -q --detach d7527d608ad2b2e3cc398fdde34db7947b254a1a
cp .ufo/waves/round-47/l1-draft/mado-terminal.py "$D/tools/mado-terminal.py"      # sha256 762d042c…6c08
git -C "$D" add tools/mado-terminal.py
git -C "$D" -c user.name=seat -c user.email=seat@scratch.invalid commit -q -m cand # 6a893cbb4f4ff2e1b130ba403affe053e2dad9a6
python3 -I quality/counters/c1-r47-terminal.py --repo "$D" --rev HEAD --work <W> --nonce 4242
```

| run | `--work` filesystem | nonce | result | wall |
|---|---|---|---|---|
| xfs-1 | `/fast/scratch/...` (xfs) | 4242 | `fixtures=190/190 explained=190/190 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET`, exit 0 | 56.5 s |
| xfs-2 | same xfs dir, repeat | 4242 | same line, exit 0 | 46.0 s |
| tmpfs-1 | `/dev/shm/ExecC1Determinism/w` (tmpfs) | 4242 | same line, exit 0 | 51.8 s |

Receipts: `counts/run-xfs-1.txt`, `counts/run-xfs-2.txt`, `counts/run-tmpfs-1.txt` (full clause=f/x/g output, 196 lines each).
`diff` of the three (timing lines removed) is **empty**: `diff -q a.txt b.txt` and `diff -q a.txt c.txt` both IDENTICAL.
Per-fixture results, explain results, generated-case results and the readonly trip count (`trips=0`) do not move with the
filesystem or a repeat run.

## 1. Readdir order is real, and the reference tool models it correctly (supports the claim)

The resolver builds its fallback list by prepending each `find` hit (`xdg-terminal-exec:790`, quote verified by
`verify-quotes.sh`), and `find` runs with `LC_ALL=C` over readdir order (`xdg-terminal-exec:795`). So the fallback order —
and, when two candidates are valid, the *selected id* — is the reverse of readdir order.

Two valid entries, no list file, created `zeta` then `alpha` (`repro-readdir-order.sh`):

```
== /fast/scratch/.../order fstype=xfs        == /dev/shm/.../order fstype=tmpfs
-- find -L order:                            -- find -L order:
zeta.desktop                                  alpha.desktop
alpha.desktop                                 zeta.desktop
-- pin  LANG=C.UTF-8: alpha.desktop           -- pin  LANG=C.UTF-8: zeta.desktop
-- pin  LANG=en_US.UTF-8: alpha.desktop       -- pin  LANG=en_US.UTF-8: zeta.desktop
-- tool LANG=C.UTF-8: alpha.desktop           -- tool LANG=C.UTF-8: zeta.desktop
```

Selection flips with the filesystem; the reference tool (`.ufo/waves/round-47/l1-draft/mado-terminal.py:506`,
`os.scandir`, and `:493` prepend, exactly the resolver's rule) follows the *live* order on both, so it agrees with the pin
either way. Receipt: `receipt-repro1-readdir-order.txt`. This is the correct behaviour for the claim: the tool is
filesystem-honest, not fixture-fitted.

## 2. No frozen fixture depends on readdir order — and that is the hole

- A rebuild of `quality/counters/c1-r47-fixtures.json` with `--work` on tmpfs is **byte-identical**:
  `4836cc1d9e493af7bf15fa52f6e6855fe71c5c27911880847da668e1e313dd86` for both files, `BYTE_IDENTICAL`, `kept=190 dropped=0`,
  4.8 s. Receipt: `receipt-repro3-fixture-rebuild.txt`. The two filesystems produce exactly reversed readdir order for the
  same creation sequence (section 1), so any order-dependent case would have flipped its recorded `expect`. None did.
- Census `fixtures-order-census.txt`: 50 fixtures have a directory with >= 2 `.desktop` files; only 12 of those have no
  list file, and in every one of the 12 the losing sibling is rejected on another key (Hidden / Type / Categories /
  TryExec / Exec absence / OnlyShowIn), so the winner is order-invariant. Machine proof is the byte-identical rebuild.
- The sorted mutant proves the coverage gap directly. One line changed in the reference —
  `names = [de.name for de in os.scandir(cur)]` -> `names = sorted(de.name for de in os.scandir(cur))` (commit
  `fe59b4cfe492e0b2b654b509d187fd0cd9d4bf68`) — scores:

| nonce | clause f | clause x | clause g | verdict |
|---|---|---|---|---|
| 4242 | **190/190** | **190/190** | 149/150 | TARGET_MISSED (exit 1) |
| 4747 | **190/190** | **190/190** | 146/150 | TARGET_MISSED (exit 1) |

  The only detector is a random clause-g case. At nonce 4242 that case is `g012`, and it is genuinely
  filesystem-sensitive: same tree, same creation order, `repro-g012.py`,
  xfs -> `--print-id` = `vendor-xterm.desktop`, `--test -e ls` = `xterm -x -e ls`;
  tmpfs -> `--print-id` = `xterm.desktop`, `--test -e ls` = `xterm -e ls`.
  Receipt: `receipt-repro2-g012.txt`; failed runs: `counts/run-mut-sorted-n4242.txt`, `counts/run-mut-sorted-n4747.txt`.

So a candidate that "stabilises" the walk (a natural simplification — `os.scandir` order is documented as arbitrary)
passes 190/190 pinned fixtures and 190/190 explain checks under every nonce, and is caught only if the 150 random cases
happen to contain a two-valid-candidate tree. At the two nonces measured that happened, but nothing in the frozen design
guarantees it: the fixture half contributes **zero** readdir coverage, while the contract's step 4 makes readdir order the
core of the fallback rule.

### Why the builder could not have caught it

`ctl/build-fixtures.py:70` varies only path depth (`"x" * (k + 1)`) and keeps all three probe roots on one filesystem;
the stability test at `:76` (`if len(set(res)) != 1`) therefore cannot see a filesystem-order dependence. An
order-dependent `expect` would have been frozen silently. Mitigation if a v2 is registered: build once more with `--work`
on a second filesystem (tmpfs) and drop or set-value any case that differs; and either give order-sensitive cases a
set-valued `expect` (`{either id}`) or run the drift check against the live oracle only — a single recorded scalar would
make the count itself filesystem-bound, i.e. it would return `SETUP … oracle drifted` (exit 2, `c1-r47-terminal.py:445`)
on tmpfs, which is not a `TARGET_MISSED` and not in the counting command's stated preconditions.

## 3. Locale axis: no drift (supports the claim)

- Clause f runs each fixture twice: variant A `LANG=C.UTF-8`, variant B `LANG=en_US.UTF-8` at a deeper random root
  (`c1-r47-terminal.py:233`, `:237`); both equal the recorded expect on both filesystems (190/190 in every run), so no
  fixture output moves with the locale.
- The pin neutralises collation itself: `LC_ALL=C gen_hash`, `LC_ALL=C read_config_paths`, `LC_ALL=C read_entry_path`,
  `LC_ALL=C find -L` (`xdg-terminal-exec:185`, `:357`, `:974`, `:795`).
- Direct probe (`repro-readdir-order.sh`, both filesystems): `LANG=C.UTF-8` and `LANG=en_US.UTF-8` give the same id and
  the same exit status. `en_US.UTF-8` is really installed and really selected (`receipt-locale.txt`:
  `python3 -c 'locale.setlocale(LC_ALL,"en_US.UTF-8")'` -> `en_US.UTF-8`, `LC_ALL=en_US.UTF-8 locale charmap` -> `UTF-8`),
  so variant B is not silently a C-locale run on this host; `tr_TR.UTF-8` is absent (locale error), so a Turkish-collation
  probe was not possible and is not claimed.

## 4. Hygiene

- Every resolver invocation used `--print-*` (never a bare launch) and set `XDG_CACHE_HOME` inside the scratch root. The
  host cache `~/.cache/xdg-terminal-exec` still has mtime `2026-10-26 17:42:25`, i.e. untouched by this seat (first run
  19:1x).
- All work lived under `/fast/scratch/hyaku/mado-r47/ExecC1Determinism` (xfs) and `/dev/shm/ExecC1Determinism` (tmpfs);
  both removed. Clone, mutant commits and the pin copy were scratch-only; nothing outside the seat dir and this report was
  written in the lane. No package manager, no compositor call, no GUI.
- No tools installed or upgraded.

## Residual limits of this seat

- Only two filesystems were exercised (xfs insertion order, tmpfs reverse-insertion). ext4/btrfs hash order was not
  available inside the write scope; the two exercised orders are exact reverses, which brackets the axis.
- No fixture uses symlinks, so `find -L` loop/`-type` behaviour against the tool's `(st_dev, st_ino)` ancestor check was
  not part of this axis and is not claimed.
- The mutant is one simplification (`sorted`); other order-blind models (e.g. sorting by id, or caching a fixed list) are
  the same coverage question and were not each scored.
- Clause-g detection frequency was measured at two nonces only (1/150 and 4/150 failing cases); no probability is claimed
  beyond those observations.

## Files in this directory

- `counts/run-xfs-1.txt`, `counts/run-xfs-2.txt`, `counts/run-tmpfs-1.txt` — the three reference counts.
- `counts/run-mut-sorted-n4242.txt`, `counts/run-mut-sorted-n4747.txt` — the sorted mutant, both nonces.
- `counts/summary.txt` — one verdict line per count.
- `receipt-repro1-readdir-order.txt` — selection flip across xfs/tmpfs, locale probe, tool agreement.
- `receipt-repro2-g012.txt` — generated case `g012` of nonce 4242 flips across filesystems.
- `receipt-repro3-fixture-rebuild.txt` — tmpfs rebuild byte-identical to the frozen fixtures.
- `receipt-locale.txt` — locale availability (`en_US.UTF-8` present, `tr_TR.UTF-8` absent).
- `fixtures-order-census.txt` — per-directory candidate census of the 190 fixtures.
- `repro-readdir-order.sh`, `repro-g012.py`, `repro-fixture-rebuild.sh`, `verify-quotes.sh`, `verify-quotes.txt` —
  reproducible drivers and the computed locators for every quote above.
