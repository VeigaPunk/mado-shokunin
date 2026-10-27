#!/bin/bash
# MutC2Replay - round 48 w2 - PRED-C2-r48 clause_r replay-bypass probe.
# Attack: does clause_r measure the host's real pinned xkbcli, or accept a fake
# selected via PATH shim (mutant A) or via XKB_CONFIG_ROOT passed to the real
# binary (mutant B)? All mutation happens inside this disposable scratch clone.
# Build is plumbing-only (mktree surgery, no index, no worktree) to respect the
# 1 MB/file bound: largest driver-written file is the 242 KB modified SOURCES.md.
set -u
ulimit -f 2048

L=/home/vgpnk/Projects/shokunin/mado-shokunin
W=$L/.ufo/waves/round-48
CNT=$L/quality/counters/c2-r48-xkb-entry.py
S=/fast/scratch/hyaku/mado-r48/MutC2Replay
SEAT=$W/w2/MutC2Replay
mkdir -p "$S" "$SEAT"
trap 'rm -rf -- "$S"' EXIT

HEAD0=$(git -C "$L" rev-parse HEAD)
echo "lane_head_before=$HEAD0"
echo "scratch=$S"

D=$S/m/clone
mkdir -p "$S/m" "$S/replay" "$S/bin"
git clone -q --shared --no-checkout "$L" "$D" || { echo "clone FAILED"; exit 3; }
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "toplevel assert FAILED"; exit 3; }

python3 - "$D" "$S" "$W" <<'PYEOF'
import subprocess, sys
d, s, w = sys.argv[1:4]

def g(*a, inp=None):
    r = subprocess.run(["git", "-C", d, *a], input=inp, capture_output=True)
    if r.returncode != 0:
        sys.exit("git %s failed: %s" % (a, r.stderr.decode()[:300]))
    return r.stdout

def entries(tree):
    out = []
    for line in g("ls-tree", tree).decode().splitlines():
        meta, name = line.split("\t", 1)
        out.append([meta, name])
    return out

def mtree(ents):
    inp = "".join("%s\t%s\n" % (m, n) for m, n in ents)
    return g("mktree", inp=inp.encode()).decode().strip()

def upsert(ents, name, meta):
    return sorted([e for e in ents if e[1] != name] + [[meta, name]],
                  key=lambda e: (e[1].rstrip("/"), e[1]))

def blob_sha(path, content_bytes):
    open(s + "/" + path.rsplit("/", 1)[-1], "wb").write(content_bytes)
    return g("hash-object", "-w", "--stdin",
             inp=content_bytes).decode().strip()

BASE = "579f694b45c797a9c39761fdb4f9e0a1b71b3585"
TIP = "3e6c848a0e1bbc9c7058226b86d0faefc5351c9d"
RECEIPT = ".ufo/waves/round-48/receipts/xkbcli-compile-keymap-r48.txt"

# ---------- pristine overlay ----------
src = g("cat-file", "blob", BASE + ":corpus/SOURCES.md")
rows = open(w + "/l1-draft/rows-c2.md", "rb").read().rstrip(b"\n")
t = src.decode().split("\n")
i = max(k for k, l in enumerate(t) if l.startswith("| S339 |"))
t[i + 1:i + 1] = rows.decode().split("\n")
src_sha = blob_sha("SOURCES-new.md", "\n".join(t).encode())

rd = g("cat-file", "blob", BASE + ":corpus/README.md")
rr = open(w + "/l1-draft/readme-row.md", "rb").read().rstrip(b"\n")
t = rd.decode().split("\n")
i = max(k for k, l in enumerate(t) if l.startswith("| `knowledge/xdg-terminal-selection-r47.md`"))
t[i + 1:i + 1] = [rr.decode()]
rd_sha = blob_sha("README-new.md", "\n".join(t).encode())

entry_sha = blob_sha("entry.md", open(w + "/l1-draft/xkb-keymap-compile-r48.md", "rb").read())

root = entries(BASE + "^{tree}")
def lookup(ents, name):
    return next(e for e in ents if e[1] == name)[0].split()[2]

# corpus subtree: replace SOURCES.md + README.md, add knowledge/xkb-keymap-compile-r48.md
corpus = entries(lookup(root, "corpus"))
knowledge = entries(lookup(corpus, "knowledge"))
knowledge = upsert(knowledge, "xkb-keymap-compile-r48.md", "100644 blob " + entry_sha)
k_sha = mtree(knowledge)
corpus = upsert(upsert(corpus, "SOURCES.md", "100644 blob " + src_sha),
                "README.md", "100644 blob " + rd_sha)
corpus = upsert(corpus, "knowledge", "040000 tree " + k_sha)
corpus_sha = mtree(corpus)

# .ufo/waves subtree: add round-48 from TIP
ufo_sha = lookup(root, ".ufo")
ufo = entries(ufo_sha)
waves_sha = lookup(ufo, "waves")
waves = entries(waves_sha)
tip_r48 = g("rev-parse", TIP + ":.ufo/waves/round-48").decode().strip()
waves = upsert(waves, "round-48", "040000 tree " + tip_r48)
waves_sha2 = mtree(waves)
ufo = upsert(ufo, "waves", "040000 tree " + waves_sha2)
ufo_sha2 = mtree(ufo)

root2 = upsert(upsert(root, "corpus", "040000 tree " + corpus_sha),
               ".ufo", "040000 tree " + ufo_sha2)
root_tree = mtree(root2)
c0 = g("-c", "user.name=t", "-c", "user.email=t@t", "commit-tree", root_tree,
       "-m", "mutc2-pristine").decode().strip()
print("replay_rev_pristine=" + c0)

open(s + "/commit0", "w").write(c0 + "\n")
open(s + "/receipt-path", "w").write(RECEIPT + "\n")
PYEOF
[ -f "$S/commit0" ] || { echo "pristine build FAILED"; exit 3; }
C0=$(cat "$S/commit0")
RECEIPT_PATH=$(cat "$S/receipt-path")
git -C "$D" update-ref refs/heads/mutc2 "$C0"
git -C "$D" symbolic-ref HEAD refs/heads/mutc2
echo "head_is_pristine=$(git -C "$D" rev-parse HEAD)"

REALDIG=$(git -C "$D" cat-file blob "$C0:$RECEIPT_PATH" | sed -n 's/^\([0-9a-f]\{64\}\)[ \t][ \t]*host\.keymap$/\1/p' | head -1)
echo "receipt_digest_before=$REALDIG"

TMPDIR="$S/replay" python3 -I "$CNT" --repo "$D" --rev HEAD > "$S/out-baseline.txt" 2>&1
echo "baseline_exit=$?"
grep -E 'clause=r|verdict=' "$S/out-baseline.txt" | tail -3

xkbcli compile-keymap --layout br --options compose:caps > "$S/host-real.keymap" 2>"$S/host-real.err"
echo "live_real_digest=$(sha256sum "$S/host-real.keymap" | cut -d" " -f1) bytes=$(wc -c < "$S/host-real.keymap")"

# ---------- mutant commits: replace receipt blob in the committed tree ----------
mutant_commit() { # mutant_commit <new-receipt-file> <label>
  RSHA=$(git -C "$D" hash-object -w "$1")
  python3 - "$D" "$RSHA" "$RECEIPT_PATH" <<'PYEOF'
import subprocess, sys
d, rsha, rp = sys.argv[1:4]
def g(*a, inp=None):
    r = subprocess.run(["git", "-C", d, *a], input=inp, capture_output=True)
    assert r.returncode == 0, r.stderr
    return r.stdout
def ents(t): return [l.split("\t", 1) for l in g("ls-tree", t).decode().splitlines()]
def lookup(e_, n): return next(x for x in e_ if x[1] == n)[0].split()[2]
def mk(e_):
    inp = "".join("%s\t%s\n" % (m, n) for m, n in sorted(e_, key=lambda x: x[1]))
    return g("mktree", inp=inp.encode()).decode().strip()
def swap(tree_sha, segs, blob):
    e_ = ents(tree_sha)
    if len(segs) == 1:
        e_ = [x for x in e_ if x[1] != segs[0]]
        e_.append(["100644 blob " + blob, segs[0]])
        return mk(e_)
    child = lookup(e_, segs[0])
    nc = swap(child, segs[1:], blob)
    e_ = [x for x in e_ if x[1] != segs[0]]
    e_.append(["040000 tree " + nc, segs[0]])
    return mk(e_)
root = ents("HEAD^{tree}")
rp_segs = rp.split("/")
new_root = swap("HEAD^{tree}", rp_segs, rsha)
c = g("-c", "user.name=t", "-c", "user.email=t@t", "commit-tree", new_root,
      "-m", "mutant").decode().strip()
g("update-ref", "refs/heads/mutc2", c)
g("symbolic-ref", "HEAD", "refs/heads/mutc2")
print(c)
PYEOF
}

# ---------- Mutant A: fake xkbcli first in PATH + forged receipt digest ----------
python3 - "$D" "$S" "$RECEIPT_PATH" <<'PYEOF'
import hashlib, subprocess, sys
d, s, rp = sys.argv[1:4]
b = (b"xkb_keymap {\n"
     b"\t// MutC2Replay forged replay bytes - never produced by /usr/bin/xkbcli\n"
     b"};\n")
open(s + "/forged.keymap", "wb").write(b)
h = hashlib.sha256(b).hexdigest()
t = subprocess.run(["git", "-C", d, "cat-file", "blob", "HEAD:" + rp],
                   capture_output=True, check=True).stdout.decode()
t2, n = __import__("re").subn(r"(?m)^[0-9a-f]{64}(\s+host\.keymap)$", h + r"\1", t)
assert n == 1, "digest line count=%d" % n
open(s + "/receipt-A.txt", "w").write(t2)
open(s + "/digestA.txt", "w").write(h + "\n")
print("forged_digest_A=" + h)
PYEOF
cat > "$S/bin/xkbcli" <<'SHEOF'
#!/bin/sh
# MutC2Replay scratch shim (mutant A) - lives only in /fast/scratch, never installed.
# Fakes the PRED-C2-r48 clause_r replay: positive compile -> forged bytes (rc 0);
# the three negative probes -> rc 1/1/0 with the required stderr markers.
case "$1" in
compile-keymap)
  case "$*" in
  *--test*)
    case "$*" in
    *"--layout zz"*)
      echo "xkbcommon: ERROR: [XKB-338] Couldn't find file \"symbols/zz\" in include paths" >&2
      exit 1 ;;
    *"--variant nope"*)
      echo "xkbcommon: ERROR: [XKB-661] Couldn't process include statement for 'br(nope)'" >&2
      exit 1 ;;
    *"nope:nope"*)
      echo "xkbcommon: ERROR: [XKB-595] Unrecognized RMLVO option \"nope:nope\" was ignored" >&2
      exit 0 ;;
    esac
    exit 1 ;;
  *)
    cat "$FORGED_KEYMAP"
    exit 0 ;;
  esac ;;
esac
exec /usr/bin/xkbcli "$@"
SHEOF
chmod +x "$S/bin/xkbcli"
CA=$(mutant_commit "$S/receipt-A.txt" mutc2-A-forged-digest)
echo "replay_rev_A=$CA"

env PATH="$S/bin:$PATH" FORGED_KEYMAP="$S/forged.keymap" TMPDIR="$S/replay" \
  python3 -I "$CNT" --repo "$D" --rev HEAD > "$S/out-A-fake-path.txt" 2>&1
echo "mutA_fake_exit=$?"
grep -E 'clause=r|verdict=' "$S/out-A-fake-path.txt" | tail -3

env TMPDIR="$S/replay" python3 -I "$CNT" --repo "$D" --rev HEAD > "$S/out-A-control.txt" 2>&1
echo "mutA_control_exit=$?"
grep -E 'clause=r|verdict=' "$S/out-A-control.txt" | tail -3

# ---------- Mutant A2: forged digest consistently in entry + receipt (full bypass attempt) ----------
REALHEX="efd487a399201523540f4e5bbf81818be3183f6d9957c2f2b12469a2cf6fce81"
FAKEHEX=$(cat "$S/digestA.txt")
python3 - "$D" "$S" <<PYEOF
import subprocess, sys
d, s = sys.argv[1:4]
real, fake = "$REALHEX", "$FAKEHEX"
def g(*a, inp=None):
    r = subprocess.run(["git", "-C", d, *a], input=inp, capture_output=True)
    assert r.returncode == 0, r.stderr
    return r.stdout
def ents(t): return [l.split("\t", 1) for l in g("ls-tree", t).decode().splitlines()]
def lookup(e_, n): return next(x for x in e_ if x[1] == n)[0].split()[2]
def mk(e_):
    inp = "".join("%s\t%s\n" % (m, n) for m, n in sorted(e_, key=lambda x: x[1]))
    return g("mktree", inp=inp.encode()).decode().strip()
def swap(tree_sha, segs, blob):
    e_ = ents(tree_sha)
    if len(segs) == 1:
        e_ = [x for x in e_ if x[1] != segs[0]]
        e_.append(["100644 blob " + blob, segs[0]])
        return mk(e_)
    child = lookup(e_, segs[0])
    nc = swap(child, segs[1:], blob)
    e_ = [x for x in e_ if x[1] != segs[0]]
    e_.append(["040000 tree " + nc, segs[0]])
    return mk(e_)
ENTRY = "corpus/knowledge/xkb-keymap-compile-r48.md"
t = g("cat-file", "blob", "HEAD:" + ENTRY).decode()
n_entry = t.count(real)
assert n_entry >= 1, "entry does not state the real digest"
open(s + "/entry-A2.md", "w").write(t.replace(real, fake))
esha = g("hash-object", "-w", "--stdin", inp=(t.replace(real, fake)).encode()).decode().strip()
new_root = swap("HEAD^{tree}", ENTRY.split("/"), esha)
c = g("-c", "user.name=t", "-c", "user.email=t@t", "commit-tree", new_root,
      "-m", "mutant-A2").decode().strip()
g("update-ref", "refs/heads/mutc2", c)
print(c)
PYEOF
git -C "$D" symbolic-ref HEAD refs/heads/mutc2
CA2=$(git -C "$D" rev-parse HEAD)
echo "replay_rev_A2=$CA2 entry_digest_edits=$FAKEHEX"

env PATH="$S/bin:$PATH" FORGED_KEYMAP="$S/forged.keymap" TMPDIR="$S/replay" \
  python3 -I "$CNT" --repo "$D" --rev HEAD > "$S/out-A2-fake-path.txt" 2>&1
echo "mutA2_fake_exit=$?"
grep -E 'clause=r|verdict=' "$S/out-A2-fake-path.txt" | tail -3

env TMPDIR="$S/replay" python3 -I "$CNT" --repo "$D" --rev HEAD > "$S/out-A2-control.txt" 2>&1
echo "mutA2_control_exit=$?"
grep -E 'clause=r|verdict=' "$S/out-A2-control.txt" | tail -3

# ---------- Mutant B: real /usr/bin/xkbcli, XKB_CONFIG_ROOT carried into the replay ----------
# context.c:231 honors XKB_CONFIG_ROOT; a nonexistent root falls back with a
# warning, so the probe below only documents fallback. The bypass needs an
# EXISTING replacement root with modified data.
XKB=$(readlink -f /usr/share/X11/xkb)
echo "xkb_data_root=$XKB"
env XKB_CONFIG_ROOT="$S/emptyroot" xkbcli compile-keymap --layout br --options compose:caps \
  > "$S/b-probe.out" 2>"$S/b-probe.err"
echo "xkb_config_root_nonexistent_fallback_rc=$? (empty stderr at default log level)"

python3 - "$D" "$S" "$XKB" <<'PYEOF'
import hashlib, os, re, shutil, subprocess, sys
d, s, xkb = sys.argv[1:4]
def g(*a, inp=None):
    r = subprocess.run(["git", "-C", d, *a], input=inp, capture_output=True)
    assert r.returncode == 0, r.stderr
    return r.stdout
root = s + "/xkbroot"
shutil.copytree(xkb, root,
                ignore=shutil.ignore_patterns("*.xml", "*.lst", "*.dtd", "README"))
p = root + "/symbols/br"
t = open(p).read()
n = t.count("Portuguese")
open(p, "w").write(t.replace("Portuguese", "PortugueseX"))
env = dict(os.environ); env["XKB_CONFIG_ROOT"] = root
q = subprocess.run(["xkbcli", "compile-keymap", "--layout", "br",
                    "--options", "compose:caps"], capture_output=True, env=env)
assert q.returncode == 0, q.stderr
h = hashlib.sha256(q.stdout).hexdigest()
open(s + "/host-b.keymap", "wb").write(q.stdout)
ENTRY = "corpus/knowledge/xkb-keymap-compile-r48.md"
RECEIPT = ".ufo/waves/round-48/receipts/xkbcli-compile-keymap-r48.txt"
rt = g("cat-file", "blob", "HEAD:" + RECEIPT).decode()
cur = re.search(r"(?m)^([0-9a-f]{64})\s+host\.keymap$", rt).group(1)
assert h != cur, "replacement root produced the same digest"
et = g("cat-file", "blob", "HEAD:" + ENTRY).decode()
assert et.count(cur) >= 1, "entry does not state the current digest"
et2 = et.replace(cur, h)
rt2, k = re.subn(r"(?m)^%s(\s+host\.keymap)$" % cur, h + r"\1", rt)
assert k == 1, k
def ents(tr): return [l.split("\t", 1) for l in g("ls-tree", tr).decode().splitlines()]
def lookup(e_, nm): return next(x for x in e_ if x[1] == nm)[0].split()[2]
def mk(e_):
    inp = "".join("%s\t%s\n" % (m, nm) for m, nm in sorted(e_, key=lambda x: x[1]))
    return g("mktree", inp=inp.encode()).decode().strip()
def swap(tr, segs, blob):
    e_ = ents(tr)
    if len(segs) == 1:
        e_ = [x for x in e_ if x[1] != segs[0]]
        e_.append(["100644 blob " + blob, segs[0]])
        return mk(e_)
    child = lookup(e_, segs[0])
    nc = swap(child, segs[1:], blob)
    e_ = [x for x in e_ if x[1] != segs[0]]
    e_.append(["040000 tree " + nc, segs[0]])
    return mk(e_)
esha = g("hash-object", "-w", "--stdin", inp=et2.encode()).decode().strip()
rsha = g("hash-object", "-w", "--stdin", inp=rt2.encode()).decode().strip()
nr = swap("HEAD^{tree}", ENTRY.split("/"), esha)
nr = swap(nr, RECEIPT.split("/"), rsha)
c = g("-c", "user.name=t", "-c", "user.email=t@t", "commit-tree", nr,
      "-m", "mutant-B").decode().strip()
g("update-ref", "refs/heads/mutc2", c)
open(s + "/digestB.txt", "w").write(h + "\n")
print("symbols_br_edits=%d root_digest_B=%s (prev=%s)" % (n, h, cur))
print(c)
PYEOF
if [ -s "$S/digestB.txt" ]; then
  git -C "$D" symbolic-ref HEAD refs/heads/mutc2
  CB=$(git -C "$D" rev-parse HEAD)
  echo "replay_rev_B=$CB"
  env XKB_CONFIG_ROOT="$S/xkbroot" TMPDIR="$S/replay" \
    python3 -I "$CNT" --repo "$D" --rev HEAD > "$S/out-B-xkbroot.txt" 2>&1
  echo "mutB_xkbroot_exit=$?"
  grep -E 'clause=r|verdict=' "$S/out-B-xkbroot.txt" | tail -3
  env TMPDIR="$S/replay" python3 -I "$CNT" --repo "$D" --rev HEAD > "$S/out-B-control.txt" 2>&1
  echo "mutB_control_exit=$?"
  grep -E 'clause=r|verdict=' "$S/out-B-control.txt" | tail -3
else
  echo "mutB skipped: replacement root did not yield a distinct digest"
fi

# ---------- evidence ledger ----------
{
  echo "receipt_digest_before(pristine)=$REALDIG"
  echo "digest_A(forged)=$(cat "$S/digestA.txt" 2>/dev/null)"
  echo "digest_B(forged)=$(cat "$S/digestB.txt" 2>/dev/null)"
  echo "live_real_binary=/usr/bin/xkbcli $(xkbcli --version 2>&1)"
  echo "live_real_digest=$(sha256sum "$S/host-real.keymap" 2>/dev/null | cut -d" " -f1)"
} > "$S/digest-ledger.txt"

# ---------- lane integrity + evidence copy (before trap cleanup) ----------
HEAD1=$(git -C "$L" rev-parse HEAD)
[ "$HEAD0" = "$HEAD1" ] && echo "lane_head_unchanged=$HEAD1" || echo "LANE HEAD CHANGED: $HEAD1"
cp "$S/out-baseline.txt" "$S/out-A-fake-path.txt" "$S/out-A-control.txt" "$SEAT/"
cp "$S"/out-A2-*.txt "$SEAT/" 2>/dev/null
cp "$S/bin/xkbcli" "$SEAT/xkbcli-shim-mutA.sh"
cp "$S/digest-ledger.txt" "$SEAT/digest-ledger.txt"
cp "$S/host-real.keymap" "$SEAT/host-real.keymap" 2>/dev/null
cp "$S/b-probe.err" "$SEAT/b-probe.err" 2>/dev/null
cp "$S"/out-B-*.txt "$SEAT/" 2>/dev/null
cp "$S"/digestA.txt "$S"/digestB.txt "$SEAT/" 2>/dev/null
cp "$S/host-b.keymap" "$SEAT/host-b.keymap" 2>/dev/null
echo "largest_files:"
find "$S" -maxdepth 2 -type f -printf '%s %p\n' 2>/dev/null | sort -rn | head -3
echo "scratch_total=$(du -sh "$S" 2>/dev/null | cut -f1)"
echo "seat_copy:"
ls -la "$SEAT" | tail -n +2
echo "DRIVER DONE"
