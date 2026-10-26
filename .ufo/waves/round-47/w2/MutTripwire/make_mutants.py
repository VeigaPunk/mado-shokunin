#!/usr/bin/env python3
"""MutTripwire mutant generator.

Builds single-behaviour, rare-path mutants of the L1 reference
.ufo/waves/round-47/l1-draft/mado-terminal.py. Each mutant:
  - inserts ONE module-level helper `_mut()` that performs exactly one
    forbidden behaviour (os.system / subprocess / socket / fork+exec /
    fork-only / fork-context multiprocessing),
  - calls `_mut()` at exactly ONE rare-path trigger site,
  - swallows every exception inside `_mut()` so all counter-compared
    behaviour (stdout, rc, stderr-free) stays identical to the reference.
Outputs: mutants/Mxx-*.py, receipts/Mxx.diff, receipts/manifest.json.
"""
import difflib
import hashlib
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
REF = LANE + "/.ufo/waves/round-47/l1-draft/mado-terminal.py"
SEAT = LANE + "/.ufo/waves/round-47/w2/MutTripwire"
MUTDIR = SEAT + "/mutants"
RCPT = SEAT + "/receipts"

HELPERS = {
    "os.system": (
        "def _mut():\n"
        "    try:\n"
        "        os.system(\":\")\n"
        "    except Exception:\n"
        "        pass\n"
    ),
    "subprocess": (
        "def _mut():\n"
        "    try:\n"
        "        import subprocess\n"
        "        subprocess.run([\"/bin/sh\", \"-c\", \"exit 0\"],\n"
        "                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)\n"
        "    except Exception:\n"
        "        pass\n"
    ),
    "subprocess.Popen": (
        "def _mut():\n"
        "    try:\n"
        "        import subprocess\n"
        "        _p = subprocess.Popen([\"/bin/sh\", \"-c\", \"exit 0\"],\n"
        "                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)\n"
        "        _p.wait()\n"
        "    except Exception:\n"
        "        pass\n"
    ),
    "socket": (
        "def _mut():\n"
        "    try:\n"
        "        import socket\n"
        "        _s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n"
        "        try:\n"
        "            _s.connect((\"127.0.0.1\", 1))\n"
        "        except OSError:\n"
        "            pass\n"
        "        _s.close()\n"
        "    except Exception:\n"
        "        pass\n"
    ),
    "fork-exec": (
        "def _mut():\n"
        "    try:\n"
        "        _pid = os.fork()\n"
        "        if _pid == 0:\n"
        "            try:\n"
        "                os.execv(\"/bin/sh\", [\"sh\", \"-c\", \"exit 0\"])\n"
        "            except Exception:\n"
        "                os._exit(127)\n"
        "        else:\n"
        "            os.waitpid(_pid, 0)\n"
        "    except Exception:\n"
        "        pass\n"
    ),
    "fork-only": (
        "def _mut():\n"
        "    try:\n"
        "        _pid = os.fork()\n"
        "        if _pid == 0:\n"
        "            os._exit(0)\n"
        "        os.waitpid(_pid, 0)\n"
        "    except Exception:\n"
        "        pass\n"
    ),
    "multiprocessing": (
        "def _mut():\n"
        "    try:\n"
        "        import multiprocessing\n"
        "        _p = multiprocessing.get_context(\"fork\").Process(target=lambda: None)\n"
        "        _p.start()\n"
        "        _p.join()\n"
        "    except Exception:\n"
        "        pass\n"
    ),
}

HELPER_ANCHOR = "\ndef main(argv):\n"

TRIGGERS = {
    "selftest-start": (
        '    base = tempfile.mkdtemp(prefix="mado-terminal-selftest.", dir=os.environ.get("TMPDIR") or None)\n',
        '    base = tempfile.mkdtemp(prefix="mado-terminal-selftest.", dir=os.environ.get("TMPDIR") or None)\n'
        "    _mut()\n",
    ),
    "explain-plain": (
        '    verdict = "OK" if ok else "NO_TERMINAL"\n',
        '    verdict = "OK" if ok else "NO_TERMINAL"\n'
        "    if observed is None:\n"
        "        _mut()\n",
    ),
    "explain-observed": (
        '        rc = 0 if verdict == "AGREE" else 1\n',
        '        rc = 0 if verdict == "AGREE" else 1\n'
        "        _mut()\n",
    ),
    "print-cmd": (
        '        elif a == "--print-cmd":\n'
        '            pdata.append("cmd")\n',
        '        elif a == "--print-cmd":\n'
        '            pdata.append("cmd")\n'
        "            _mut()\n",
    ),
    "action-accepted": (
        "                if self.action_listed:\n"
        "                    read_exec = True\n"
        "                    status = 0\n",
        "                if self.action_listed:\n"
        "                    read_exec = True\n"
        "                    status = 0\n"
        "                    _mut()\n",
    ),
    "selftest-100th": (
        "    cases = selftest_cases()\n"
        "    passed = 0\n"
        "    try:\n"
        "        for i, (name, files, execs, args, want_out, want_rc, envkw) in enumerate(cases):\n",
        "    cases = selftest_cases()\n"
        "    passed = 0\n"
        "    _mut_n = [0]\n"
        "    try:\n"
        "      for _mut_rep in range(3):\n"
        "        passed = 0\n"
        "        for i, (name, files, execs, args, want_out, want_rc, envkw) in enumerate(cases):\n"
        "            _mut_n[0] += 1\n"
        "            if _mut_n[0] == 100:\n"
        "                _mut()\n",
    ),
}

MUTANTS = [
    ("M01", "os.system", "selftest-start"),
    ("M02", "os.system", "explain-plain"),
    ("M03", "subprocess", "print-cmd"),
    ("M04", "subprocess.Popen", "explain-observed"),
    ("M05", "socket", "print-cmd"),
    ("M06", "socket", "action-accepted"),
    ("M07", "fork-exec", "selftest-start"),
    ("M08", "fork-exec", "explain-plain"),
    ("M09", "fork-only", "selftest-start"),
    ("M10", "fork-only", "print-cmd"),
    ("M11", "multiprocessing", "explain-plain"),
    ("M12", "multiprocessing", "selftest-100th"),
]


def main():
    os.makedirs(MUTDIR, exist_ok=True)
    os.makedirs(RCPT, exist_ok=True)
    src = open(REF, "rb").read().decode("utf-8")
    assert src.count(HELPER_ANCHOR) == 1, "helper anchor not unique"
    manifest = []
    for mid, beh, trig in MUTANTS:
        helper = HELPERS[beh]
        anch, repl = TRIGGERS[trig]
        out = src.replace(HELPER_ANCHOR, "\n" + helper + HELPER_ANCHOR, 1)
        assert out.count(anch) == 1, "%s: trigger anchor %r not unique" % (mid, trig)
        line_no = out[: out.index(anch)].count("\n") + 1
        out = out.replace(anch, repl, 1)
        path = "%s/%s-%s-%s.py" % (MUTDIR, mid, beh.replace(".", "-"), trig)
        with open(path, "wb") as fh:
            fh.write(out.encode("utf-8"))
        compile(out, path, "exec")  # mutants must at least be syntactically valid
        diff = list(difflib.unified_diff(src.splitlines(True), out.splitlines(True),
                                         "reference", mid, n=2))
        with open("%s/%s.diff" % (RCPT, mid), "w", encoding="utf-8") as fh:
            fh.writelines(diff)
        added = sum(1 for l in diff if l.startswith("+") and not l.startswith("+++"))
        manifest.append({
            "id": mid, "file": os.path.relpath(path, LANE),
            "behaviour": beh, "trigger": trig,
            "sha256": hashlib.sha256(out.encode("utf-8")).hexdigest(),
            "trigger_site_first_line": line_no, "added_lines": added,
        })
        print("%s behaviour=%s trigger=%s lines=%d sha256=%s" % (
            mid, beh, trig, added, manifest[-1]["sha256"][:16]))
    with open(RCPT + "/manifest.json", "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=1)
    print("manifest: %d mutants" % len(manifest))


if __name__ == "__main__":
    main()
