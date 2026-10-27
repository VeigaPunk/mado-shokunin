# MutC2Counter — exact commands (round 48, w2 FALSIFY, lane mado-shokunin)

All paths absolute. Every writer shell began with `ulimit -f 2048` (512-byte units; 1 MiB/file).
Scratch root `S=/fast/scratch/hyaku/mado-r48/MutC2Counter` (removed after the receipts were copied here).
The lane was never written; every lane read is object-addressed (`git show`, `git ls-tree`, `git grep`) or a
read of a committed file. `TMPDIR=$S/replay` for every counter run (clause r).

## 1. Replay tree (why sparse)

`git clone --shared` of the lane at BASE plus a full working-tree checkout fails under the 1 MiB/file cap: the
lane index is 2 771 712 B (`ls -l .git/index`). The clone is therefore built with a cone sparse checkout and
`index.sparse=true`, which keeps the index at 29 594 B:

    git clone -q --shared --no-checkout $L $D
    git -C $D config index.sparse true
    git -C $D sparse-checkout init --cone
    git -C $D sparse-checkout set corpus quality .ufo/waves/round-46/fetch \
        .ufo/waves/round-48/fetch .ufo/waves/round-48/receipts .ufo/waves/round-48/tools
    git -C $D checkout -q 579f694b45c797a9c39761fdb4f9e0a1b71b3585

No file in the sparse set exceeds 1 MiB (checked with `git ls-tree -r -l BASE -- <paths> | awk '$4+0>1048576'`).
The counter itself needs no working tree (it reads `git show REV:path`), so the sparse set only exists to let the
defect bytes be committed.

## 2. Draft overlay (recipe of l1-draft/c2-mirror.sh)

    cp .ufo/waves/round-48/fetch/*            $V0/.ufo/waves/round-48/fetch/
    cp .ufo/waves/round-48/receipts/xkbcli-compile-keymap-r48.txt \
                                              $V0/.ufo/waves/round-48/receipts/
    cp .ufo/waves/round-48/tools/make-xkb-receipt.sh $V0/.ufo/waves/round-48/tools/
    cp .ufo/waves/round-48/l1-draft/xkb-keymap-compile-r48.md $V0/corpus/knowledge/
    python3 $S/bin/integrate.py $V0          # 11 rows after S339, README index row after the r47 row
    git -C $V0 add -A && git -C $V0 -c user.name=mutc2 -c user.email=mutc2@scratch commit -qm draft-c2

V0 = c28505abcbc1204871fd82ab27b05cba8c5c0a3d.

## 3. Real counter (lane bytes, unmodified)

    TMPDIR=$S/replay python3 -I $L/quality/counters/c2-r48-xkb-entry.py --repo $V --rev HEAD [--base <V9base>]

sha256 of the scored counter: 4a0e6924eada0d12c70b4ce6e681a118896b93532e280ea3c15cc148b794a9f1.
Base control: `--repo $V0 --rev 579f694b --base 579f694b` → admitted=0/1 TARGET_MISSED, exit 1.

## 4. Counter mutants (one per clause; scratch copies only)

    cp quality/counters/c2-r48-xkb-entry.py $S/counters/m-<clause>.py   # then one textual edit each

The eight edits are in `mutants/counter-mutant.diff` (19 changed lines total, 8 `MUTANT` markers);
each mutant script is kept byte-for-byte in `mutants/`.

## 5. Matrix

    for m in <8 mutants>; do for n in 1..12; do <mutant> --repo $S/m/V$n --rev HEAD; done; done
    # V9 additionally --base 4f79087fc815b367eb3656e49f8e43e55bfdc035

Result table: `matrix.tsv`. It is the counter-mutant × defect-tree verdict grid (96 runs).

## 6. Scratch accounting

    largest single output file: out/mutant-diffs.txt            4 889 B
    largest file in scratch:    m/*/.ufo/waves/round-46/w1-results.json  373 905 B
    total scratch:              du -sh → 100 M (13 trees × ~7.6 M)
    `ulimit -f 2048` active in every writer shell; no write hit the limit.

Scratch was deleted after these receipts were copied here.
