#!/bin/bash
# w1/ExecCloneRecipe - every quote this report carries is checked against a receipt by this script.
# Run from the seat directory: bash receipts/verify-quotes.sh
set -u
cd "$(dirname "$0")/.." || exit 1
n=0; bad=0
q() { # file fragment
  n=$((n+1))
  if grep -qF -- "$2" "$1"; then printf 'OK   %-34s %s\n' "$1" "$2"; else printf 'MISS %-34s %s\n' "$1" "$2"; bad=$((bad+1)); fi
}
q receipts/clone-recipes/summary.txt 'cal.bin bytes=2097152'
q receipts/clone-recipes/summary.txt '== clone-full-1024 cap_kib=1024 cap_bytes=1048576 rc=128'
q receipts/clone-recipes/clone-full-1024.log 'error: unable to write file .ufo/waves/round-20/w2/AdvCrash/fixtures/huge_bash_cmd.jsonl'
q receipts/clone-recipes/clone-full-1024.log 'fatal: unable to checkout working tree'
q receipts/clone-recipes/clone-full-2048.log 'error: unable to write file .ufo/waves/round-20/w2/CorpusDiffIndependent/corpus-diff-results.json'
q receipts/clone-recipes/archive-all-1024.log 'tar: .ufo/waves/round-20/w2/CorpusRuntime/full-sweep.jsonl: Wrote only 1536 of 10240 bytes'
q receipts/clone-recipes/archive-all-1024.log 'huge_eval_comment.jsonl: Cannot write: File too large'
q receipts/clone-recipes/archive-all-2048.log 'evidence/corpus-comparison.json: Cannot write: File too large'
q receipts/clone-recipes/sparse-1024.log "write error: File too large"
q receipts/clone-recipes/readtree-index.txt 'readtree cap_kib=2048 rc=128'
q receipts/clone-recipes/verify-extracted.txt '== archive-all-1024/c regular_files_present=22247 size_mismatches=24'
q receipts/clone-recipes/verify-extracted.txt '== archive-all-2048/c regular_files_present=22247 size_mismatches=14'
q receipts/clone-recipes/verify-extracted.txt '== noclone-archive-1024 regular_files_present=126 size_mismatches=0'
q receipts/clone-recipes/verify-extracted.txt '== archive-paths-1024/c regular_files_present=126 size_mismatches=0'
q receipts/clone-recipes/verify-extracted.txt '== sparse-v4-2048/c regular_files_present=158 size_mismatches=0'
q receipts/clone-recipes/blobs-gt-1mib.txt '4207542 .ufo/waves/round-20/w2/CorpusRuntime/full-sweep.jsonl'
q receipts/clone-recipes/blobs-gt-2mib.txt '2167818 .ufo/waves/round-20/w2/CorpusDiffIndependent/corpus-diff-results.json'
q receipts/ref.txt 'PRED-C1-r48-v2: cold=190/190 warm=228/228 explained=418/418 generated=230/230 selftest=ok readonly=ok tool=present verdict=TARGET_MET'
q receipts/ref.txt 'clause=r trips=0'
q receipts/M-WRITE.txt 'write:mkdir("/tmp/r49-w1-00tkhse0", 0700) = 0'
q receipts/M-WRITE.txt 'trips=14840'
q receipts/M-FORK.txt 'clone(child_stack=NULL, flags=CLONE_CHILD_CLEARTID'
q receipts/M-FORK.txt 'trips=2969'
q receipts/M-SOCKET.txt 'connect(3, {sa_family=AF_UNIX, sun_path="/r49-w1-no-such.soc'
q receipts/M-SOCKET.txt 'trips=8907'
for t in M-WRITE M-FORK M-SOCKET; do
  q receipts/$t.txt 'readonly=fail tool=present verdict=TARGET_MISSED'
  q receipts/$t.txt 'cold=190/190 warm=228/228 explained=418/418 generated=230/230 selftest=ok'
done
q receipts/operator-before.txt '~/.cache/xdg-terminal-exec sha256=ddd94f6bca4bcd42c426da9bbeb9955ca5d77b8778b4e290fcfffcc984a1b3d5 size=190 mtime=1793069967'
q receipts/operator-after.txt '~/.cache/xdg-terminal-exec sha256=ddd94f6bca4bcd42c426da9bbeb9955ca5d77b8778b4e290fcfffcc984a1b3d5 size=190 mtime=1793069967'
q receipts/mutants.diff 'def _r49_probe():'
echo "checked=$n missing=$bad"
exit $([ "$bad" -eq 0 ] && echo 0 || echo 1)
