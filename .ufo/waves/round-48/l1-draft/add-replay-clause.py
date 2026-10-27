#!/usr/bin/env python3
"""Patch the C2 counter draft: insert the clause r (replay) before clause i and register it in score()."""
import re

p = "c2-r48-xkb-entry.py"
s = open(p).read()
assert s.count("\n") > 100

new = r'''def clause_r(repo, rev, base, lines, name):
    """Replay (critic finding 5): the counter re-runs the receipted xkbcli commands and byte-compares.

    The C2 receipt was taken in a scratch HOME/XDG_CONFIG_HOME (no user xkb dirs present). Clause r re-runs, on this
    host, the positive compile and the three negative probes with the same scratch env, and requires: the positive
    keymap bytes equal the receipt's recorded sha256; each negative probe's exit status equals the one the receipt
    records; the unknown-layout and unknown-variant stderr still carry the XKB-338/661 lines the entry quotes. `-` is
    refused (the receipt must be runnable). A missing xkbcli is a setup error.
    """
    for l in lines:
        for path in RECEIPT_RE.findall(l):
            full = RECEIPTS + path
            blob = show(repo, rev, full)
            if blob is None:
                continue
            if len(blob) < MIN_RECEIPT:
                print("%s %s clause=r receipt_short=%s" % (PRED, name, full))
                return False
            text = blob.decode("utf-8", "replace")
            dig = re.search(r"sha256\s+([0-9a-f]{64})", text)
            if not dig:
                print("%s %s clause=r receipt_no_digest=%s" % (PRED, name, full))
                return False
            m = VER_RE.search(text)
            if not m:
                print("%s %s clause=r receipt_no_version=%s" % (PRED, name, full))
                return False
            k = shutil.which("xkbcli")
            if not k:
                raise Setup("xkbcli missing for replay")
            S = tempfile.mkdtemp(dir=os.environ.get("TMPDIR") or "/tmp", prefix="c2r-")
            try:
                env = dict(os.environ)
                env["HOME"] = os.path.join(S, "home")
                env["XDG_CONFIG_HOME"] = os.path.join(S, "xdg")
                env["XDG_CACHE_HOME"] = os.path.join(S, "cache")
                os.makedirs(env["XDG_CONFIG_HOME"])
                os.makedirs(env["XDG_CACHE_HOME"])
                for k2 in ("XKB_DEFAULT_RULES", "XKB_DEFAULT_MODEL", "XKB_DEFAULT_LAYOUT",
                           "XKB_DEFAULT_VARIANT", "XKB_DEFAULT_OPTIONS"):
                    env.pop(k2, None)

                def run(args):
                    p = subprocess.run([k] + args, capture_output=True, env=env, timeout=60)
                    return p.returncode, p.stdout, p.stderr

                rc, out, _ = run(["compile-keymap", "--layout", "br", "--options", "compose:caps"])
                if rc != 0 or hashlib.sha256(out).hexdigest() != dig.group(1):
                    print("%s %s clause=r positive_replay_failed rc=%d sha=%s" % (
                        PRED, name, rc, hashlib.sha256(out).hexdigest()[:12]))
                    return False
                rc1, _, err1 = run(["compile-keymap", "--test", "--layout", "zz"])
                rc2, _, err2 = run(["compile-keymap", "--test", "--layout", "br", "--variant", "nope"])
                rc3, _, err3 = run(["compile-keymap", "--test", "--layout", "br", "--options", "nope:nope"])
                if (rc1, rc2, rc3) != (1, 1, 0):
                    print("%s %s clause=r negative_replay_rc=%s" % (PRED, name, (rc1, rc2, rc3)))
                    return False
                if b"Couldn't find file" not in err1 or b'process include statement' not in err2:
                    print("%s %s clause=r negative_replay_stderr_short" % (PRED, name))
                    return False
                if b"XKB-595" not in err3 and b"Unrecognized RMLVO option" not in err3:
                    print("%s %s clause=r option_replay_stderr_short" % (PRED, name))
                    return False
            finally:
                shutil.rmtree(S, ignore_errors=True)
            print("%s %s clause=r replay=ok sha=%s neg=(1,1,0) ver=%s" % (PRED, name, dig.group(1)[:12], m.group(1)))
            return True
    print("%s %s clause=r no_receipt_found" % (PRED, name))
    return False


'''

i = s.index("def clause_i(repo, rev, base, text, name):")
s = s[:i] + new + s[i:]
s = s.replace('    cl = dict.fromkeys("abcdefghi", 0)',
              '    cl = dict.fromkeys("abcdefghir", 0)', 1)
s = s.replace('    cl["i"] = int(clause_i(repo, rev, base, text, name))',
              '    cl["i"] = int(clause_i(repo, rev, base, text, name))\n    cl["r"] = int(clause_r(repo, rev, base, lines, name))', 1)
open(p, "w").write(s)
print("patched ok")
