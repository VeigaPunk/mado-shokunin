#!/usr/bin/env python3
"""Round-56 w2 mutation driver for tools/mado-watchplan.py (seat R56W2MutC2ToolA).

Mutates COPIES of the tool in a scratch git repo (never the lane), runs the UNCHANGED oracle for each mutant:
  * quality/check-r56-controls.py --claim c2  (18 committed fixtures + 8 revealed hold-out fixtures)
  * the tool's own --selftest
Verdict: KILLED if either oracle fails; SURVIVED if both pass; EQUIVALENT if the mutant's output is
byte-identical to the pristine tool's on every fixture (then it is not a real defect).

Usage: python3 -I mutate.py --repo DIR --work DIR --out DIR
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

TOOL_REL = "tools/mado-watchplan.py"
SAFE_PATH = "/usr/local/bin:/usr/bin:/bin"

# (id, area, one-line old, one-line new)
MUTANTS = [
    # ---- argument parsing / setup reasons --------------------------------
    ("M01", "args", '    if len(argv) % 2:\n        raise Setup("usage")',
     '    if len(argv) % 2 == 0:\n        raise Setup("usage")'),
    ("M02", "args", '        if flag not in ("--config", "--home", "--display-root", "--getoption") or flag in opts:',
     '        if flag not in ("--config", "--home", "--display-root", "--getoption"):'),
    ("M03", "args", '    if "--config" not in opts:\n        raise Setup("usage")',
     '    if "--config" in opts:\n        raise Setup("usage")'),
    ("M04", "args", '        if not value.startswith("/"):\n            raise Setup("usage")',
     '        if not value.startswith("/") and False:\n            raise Setup("usage")'),
    ("M05", "args", '        if flag not in ("--config", "--home", "--display-root", "--getoption") or flag in opts:',
     '        if flag not in ("--config", "--home", "--display-root", "--getoption") or opts:'),

    # ---- size / depth / entry bounds -------------------------------------
    ("M06", "bounds", "MAX_BYTES = 1048576", "MAX_BYTES = 1048575"),
    ("M07", "bounds", "MAX_BYTES = 1048576", "MAX_BYTES = 1048577"),
    ("M08", "bounds", "MAX_DEPTH = 16", "MAX_DEPTH = 15"),
    ("M09", "bounds", "MAX_DEPTH = 16", "MAX_DEPTH = 17"),
    ("M10", "bounds", "MAX_ENTRIES = 262144", "MAX_ENTRIES = 16"),
    ("M11", "bounds", "    if len(data) > MAX_BYTES:\n        raise Setup(\"too_large\")",
     "    if len(data) >= MAX_BYTES:\n        raise Setup(\"too_large\")"),
    ("M12", "bounds", "        data = fh.read(MAX_BYTES + 1)", "        data = fh.read(MAX_BYTES)"),
    ("M13", "bounds", "                if depth + 1 > MAX_DEPTH:", "                if depth + 1 >= MAX_DEPTH:"),
    ("M14", "bounds", "                if depth + 1 > MAX_DEPTH:", "                if depth + 1 > MAX_DEPTH + 1:"),
    ("M15", "bounds", "                    self.parse_file(target, depth + 1)", "                    self.parse_file(target, depth)"),

    # ---- comment / brace stack -------------------------------------------
    ("M16", "stack", '            if not line or line[0] == "#":\n                continue',
     '            if not line or line[0] == ";":\n                continue'),
    ("M17", "stack", '            if not line or line[0] == "#":\n                continue',
     '            if not line:\n                continue'),
    ("M18", "stack", '                if line == "}":\n                    if stack:\n                        stack.pop()',
     '                if line == "}":\n                    if stack is not None:\n                        stack.pop()'),
    ("M19", "stack", '                elif line.endswith("{"):\n                    stack.append(line[:-1].strip(WS))',
     '                elif line.endswith("{"):\n                    stack.append(line[:-1])'),
    ("M20", "stack", '                elif line.endswith("{"):\n                    stack.append(line[:-1].strip(WS))',
     '                elif line.startswith("{"):\n                    stack.append(line[:-1].strip(WS))'),
    ("M21", "stack", '            key = ":".join(stack) + ":" + lhs if stack else lhs',
     '            key = ":".join(stack) + ":" + lhs'),
    ("M22", "stack", '            if lhs == "source":\n                if stack:',
     '            if lhs == "source":\n                if not stack:'),

    # ---- `=` split ------------------------------------------------------
    ("M23", "eqsplit", '            lhs, _, rhs = line.partition("=")\n            lhs, rhs = lhs.strip(WS), rhs.strip(WS)',
     '            rhs, _, lhs = line.partition("=")\n            lhs, rhs = lhs.strip(WS), rhs.strip(WS)'),
    ("M24", "eqsplit", '            lhs, _, rhs = line.partition("=")\n            lhs, rhs = lhs.strip(WS), rhs.strip(WS)',
     '            lhs, _, rhs = line.partition("=")\n            lhs, rhs = rhs.strip(WS), lhs.strip(WS)'),
    ("M25", "eqsplit", '                self.source(rhs.split("#", 1)[0].strip(WS), path, number, depth)',
     '                self.source(rhs.split("#", 1)[0], path, number, depth)'),
    ("M26", "eqsplit", '            ok, number_text = config_int(rhs.split("#", 1)[0].strip(WS))',
     '            ok, number_text = config_int(rhs.split("#", 1)[0])'),

    # ---- unsupported rules ------------------------------------------------
    ("M27", "unsupported", '            if "$" in line or "{" in line or "\\\\" in line or "##" in rhs:',
     '            if "{" in line or "\\\\" in line or "##" in rhs:'),
    ("M28", "unsupported", '            if "$" in line or "{" in line or "\\\\" in line or "##" in rhs:',
     '            if "$" in line or "\\\\" in line or "##" in rhs:'),
    ("M29", "unsupported", '            if "$" in line or "{" in line or "\\\\" in line or "##" in rhs:',
     '            if "$" in line or "{" in line or "##" in rhs:'),
    ("M30", "unsupported", '            if "$" in line or "{" in line or "\\\\" in line or "##" in rhs:',
     '            if "$" in line or "{" in line or "\\\\" in line:'),

    # ---- value parsing ---------------------------------------------------
    ("M31", "value", '    if value.startswith(("true", "on", "yes")):', '    if value.startswith(("true", "on")):'),
    ("M32", "value", '    if value.startswith(("false", "off", "no")):', '    if value.startswith(("false", "off")):'),
    ("M33", "value", "    if DIGITS.fullmatch(value):", "    if DIGITS.match(value):"),
    ("M34", "value", '        return True, value.lstrip("0") or "0"', '        return True, value.lstrip("0")'),
    ("M35", "value", '    return False, ""', '    return True, "0"'),
    ("M36", "value", '    off = value is not None and bool(value.strip("0"))',
     '    off = value is not None and bool(value)'),
    ("M37", "value", '        if self.value is not None and self.value.strip("0"):',
     '        if self.value is not None:'),
    ("M38", "value", '            if ok:\n                self.value = number_text',
     '            if ok and number_text != "0":\n                self.value = number_text'),

    # ---- source handling --------------------------------------------------
    ("M39", "source", '        if len(raw) < 2:\n            self.event_error(via, raw, "bogus")',
     '        if len(raw) < 1:\n            self.event_error(via, raw, "bogus")'),
    ("M40", "source", '        if len(raw) < 2:\n            self.event_error(via, raw, "bogus")',
     '        if len(raw) < 3:\n            self.event_error(via, raw, "bogus")'),
    ("M41", "source", '        if (raw[0] == "~" and self.home is None) or "\\\\" in raw:',
     '        if (raw[0] == "~" and self.home is None):'),
    ("M42", "source", '        matches = expand(absolute_path(raw, cur, self.home))',
     '        matches = expand(raw)'),
    ("M43", "source", '        if not matches:\n            self.event_error(via, raw, "nomatch")',
     '        if matches is None:\n            self.event_error(via, raw, "nomatch")'),
    ("M44", "source", '                self.event_error(via, raw, "inaccessible")\n                return',
     '                self.event_error(via, raw, "inaccessible")\n                continue'),
    ("M45", "source", '                self.event_error(via, raw, "inaccessible")\n                return',
     '                self.event_error(via, raw, "nomatch")\n                return'),
    ("M46", "source", '            elif stat.S_ISDIR(mode):', '            elif stat.S_ISREG(mode):'),
    ("M47", "source", '                self.events.append("MADO_WATCH: SKIP via=%s path=%s reason=directory" % (via, self.show(target)))',
     '                self.events.append("MADO_WATCH: SKIP via=%s path=%s reason=nonregular" % (via, self.show(target)))'),
    ("M48", "source", '        via = "%s:%d" % (self.show(cur), number)', '        via = "%s:%d" % (cur, number)'),

    # ---- watch list -------------------------------------------------------
    ("M49", "watch", '            if os.path.isdir(path):\n                kind, mask = "dir", MASK_DIR',
     '            if os.path.isfile(path):\n                kind, mask = "dir", MASK_DIR'),
    ("M50", "watch", '            elif os.path.lexists(path):\n                kind, mask = "file", MASK_FILE',
     '            elif os.path.exists(path):\n                kind, mask = "file", MASK_FILE'),
    ("M51", "watch", '                kind, mask = "missing", MASK_FILE', '                kind, mask = "missing", MASK_DIR'),
    ("M52", "watch", '            if os.path.islink(path):\n                try:', '            if not os.path.islink(path):\n                try:'),
    ("M53", "watch", '                out.append(("canonical", canonical, "file", MASK_CANON, via))',
     '                out.append(("primary", canonical, "file", MASK_CANON, via))'),
    ("M54", "watch", '            out.append(("primary", path, kind, mask, via))',
     '            out.append(("primary", path, kind, MASK_FILE, via))'),

    # ---- display-root -----------------------------------------------------
    ("M55", "display", '            if path == prefix or path.startswith(prefix + "/"):',
     '            if path.startswith(prefix):'),
    ("M56", "display", '            given = root[:-1] if root.endswith("/") else root', '            given = root'),
    ("M57", "display", '                self.prefixes.append(os.path.realpath(root))',
     '                self.prefixes.append(root)'),
    ("M58", "display", '        plan.show(plan.config), "off" if off else "on",',
     '        plan.config, "off" if off else "on",'),

    # ---- getoption / live --------------------------------------------------
    ("M59", "live", '        if not isinstance(obj, dict):\n            raise Setup("bad_json")',
     '        if not isinstance(obj, (dict, list)):\n            raise Setup("bad_json")'),
    ("M60", "live", '        if isinstance(option, str) and type(value) is int:\n            live[option] = value',
     '        if isinstance(option, str) and isinstance(value, int):\n            live[option] = value'),
    ("M61", "live", '            live[option] = value', '            live.setdefault(option, value)'),
    ("M62", "live", '    return live.get(OPTION)', '    return live.get(OPTION, 0)'),
    ("M63", "live", '        if not stat.S_ISREG(os.stat(path).st_mode):\n            raise Setup("unreadable")',
     '        if False:\n            raise Setup("unreadable")'),

    # ---- header / DONE counters --------------------------------------------
    ("M64", "counters", '        len(plan.entries), plan.unsupported, plan.errors)]',
     '        len(plan.entries) + 1, plan.unsupported, plan.errors)]'),
    ("M65", "counters", '        len(plan.entries), plan.unsupported, plan.errors)]',
     '        len(plan.entries), plan.errors, plan.errors)]'),
    ("M66", "counters", '        len(plan.entries), plan.unsupported, plan.errors)]',
     '        len(plan.entries), plan.unsupported, plan.unsupported)]'),
    ("M67", "counters", '        len(watches), plan.unsupported, plan.errors, verdict))',
     '        len(plan.entries), plan.unsupported, plan.errors, verdict))'),
    ("M68", "counters", '        len(watches), plan.unsupported, plan.errors, verdict))',
     '        len(watches), plan.errors, plan.errors, verdict))'),
    ("M69", "counters", '        verdict = "UNKNOWN" if live is None else ("AGREE" if live == config_flag else "DIFFER")',
     '        verdict = "UNKNOWN" if live is None else ("AGREE" if live != config_flag else "DIFFER")'),
    ("M70", "counters", '        config_flag = 1 if off else 0', '        config_flag = 0 if off else 1'),

    # ================= batch 2: neighbours of the batch-1 survivors =================
    # --- comment / brace stack neighbourhood ---
    ("M71", "stack", '            if not line or line[0] == "#":\n                continue',
     '            if not line or line[0] == "#" or line[0] == ";":\n                continue'),
    ("M72", "stack", '            if not line or line[0] == "#":\n                continue',
     '            if not line or line[0] == "#" or len(line) == 1:\n                continue'),
    ("M73", "stack", '                if line == "}":\n                    if stack:\n                        stack.pop()',
     '                if line == "}":\n                    if len(stack) > 0:\n                        stack.pop()'),
    ("M74", "stack", '                elif line.endswith("{"):\n                    stack.append(line[:-1].strip(WS))',
     '                elif line.endswith("{"):\n                    stack.append(line[:-1].strip(WS))\n                    stack.append("")'),
    ("M75", "stack", '            key = ":".join(stack) + ":" + lhs if stack else lhs',
     '            key = ":".join(stack) + ":" + lhs if stack else ":" + lhs'),
    ("M76", "stack", '            lhs, rhs = lhs.strip(WS), rhs.strip(WS)',
     '            lhs, rhs = lhs.strip(WS), rhs.strip(WS + "!")'),
    ("M77", "stack", '            if lhs == "source":\n                if stack:',
     '            if lhs == "source":\n                if len(stack) > 0:'),

    # --- unsupported-rule neighbourhood (the `$`/`{`/`\\`/`##` cluster) ---
    ("M78", "unsupported", '            if "$" in line or "{" in line or "\\\\" in line or "##" in rhs:',
     '            if "$" in line or "{" in line or "\\\\" in line or "##" in line:'),
    ("M79", "unsupported", '            if "$" in line or "{" in line or "\\\\" in line or "##" in rhs:',
     '            if "$" in rhs or "{" in line or "\\\\" in line or "##" in rhs:'),
    ("M80", "unsupported", '            if "$" in line or "{" in line or "\\\\" in line or "##" in rhs:',
     '            if "$" in line[0:1] or "{" in line or "\\\\" in line or "##" in rhs:'),
    ("M81", "unsupported", '            if lhs.startswith("$"):\n                continue',
     '            if lhs.startswith("$") and len(lhs) > 1:\n                continue'),
    ("M82", "unsupported", '            if lhs.startswith("$"):\n                continue',
     '            if lhs.startswith("$"):\n                self.unsupported += 1\n                continue'),

    # --- source-handling neighbourhood (abort vs continue, glob, ordering) ---
    ("M83", "source", '        if not matches:\n            self.event_error(via, raw, "nomatch")\n            return',
     '        if not matches:\n            self.event_error(via, raw, "nomatch")'),
    ("M84", "source", '        matches = expand(absolute_path(raw, cur, self.home))\n        if not matches:',
     '        matches = expand(absolute_path(raw, cur, self.home))\n        matches = list(reversed(matches))\n        if not matches:'),
    ("M85", "source", '            target = absolute_path(match, cur, self.home) if match else match',
     '            target = absolute_path(match, cur, self.home)'),
    ("M86", "source", '                mode = os.stat(target).st_mode',
     '                mode = os.lstat(target).st_mode'),
    ("M87", "source", '            if stat.S_ISREG(mode):\n                self.add_entry(target, via)',
     '            if stat.S_ISREG(mode):\n                self.add_entry(target, via)\n                self.events.append("MADO_WATCH: SKIP via=%s path=%s reason=nonregular" % (via, self.show(target)))'),
    ("M88", "source", '        if (raw[0] == "~" and self.home is None) or "\\\\" in raw:',
     '        if (raw[0] == "~" and self.home is None) or "\\\\" in raw or "/" in raw:'),

    # --- watch-list neighbourhood (lexists/exists, canonical, masks) ---
    ("M89", "watch", '            elif os.path.lexists(path):\n                kind, mask = "file", MASK_FILE',
     '            elif os.path.isfile(path):\n                kind, mask = "file", MASK_FILE'),
    ("M90", "watch", '            if os.path.islink(path):\n                try:\n                    canonical = os.path.realpath(path, strict=True)',
     '            if os.path.islink(path):\n                try:\n                    canonical = os.path.realpath(path)'),
    ("M91", "watch", '                out.append(("canonical", canonical, "file", MASK_CANON, via))',
     '                out.append(("canonical", canonical, "file", MASK_CANON, "main")'),
    ("M92", "watch", '            out.append(("primary", path, kind, mask, via))',
     '            out.append(("primary", path, kind, mask, via))\n            if os.path.islink(path):\n                out.append(("canonical", path, "file", MASK_CANON, via))'),
    ("M93", "watch", '            if os.path.isdir(path):\n                kind, mask = "dir", MASK_DIR',
     '            if os.path.isdir(path):\n                kind, mask = "dir", MASK_DIR if False else MASK_FILE'),

    # --- display-root neighbourhood ---
    ("M94", "display", '            given = root[:-1] if root.endswith("/") else root',
     '            given = root[:-1] if root.endswith("/") else root + "/"'),
    ("M95", "display", '            if path == prefix or path.startswith(prefix + "/"):\n                return "$ROOT" + path[len(prefix):]',
     '            if path == prefix or path.startswith(prefix + "/"):\n                return "$ROOT" + path[len(prefix) + 1:]'),
    ("M96", "display", '                self.prefixes.append(os.path.realpath(root))',
     '                self.prefixes.append(os.path.realpath(root) + "/")'),

    # --- getoption / live neighbourhood ---
    ("M97", "live", '        if not stat.S_ISREG(os.stat(path).st_mode):\n            raise Setup("unreadable")',
     '        if not stat.S_ISREG(os.stat(path).st_mode) and stat.S_ISDIR(os.stat(path).st_mode):\n            raise Setup("unreadable")'),
    ("M98", "live", '        option, value = obj.get("option"), obj.get("int")',
     '        option, value = obj.get("option"), obj.get("int", obj.get("value"))'),
    ("M99", "live", '    return live.get(OPTION)', '    return live.get(OPTION, None)'),
    ("M100", "live", '        if not line:\n            continue\n        try:',
     '        if not line:\n            continue\n        if line.startswith("#"):\n            continue\n        try:'),
    ("M101", "live", '        if isinstance(option, str) and type(value) is int:\n            live[option] = value',
     '        if isinstance(option, str) and type(value) is int and value >= 0:\n            live[option] = value'),

    # --- counters neighbourhood ---
    ("M102", "counters", '        len(plan.entries), plan.unsupported, plan.errors)]',
     '        len(plan.entries), plan.unsupported, plan.errors + 1)]'),
    ("M103", "counters", '        len(watches), plan.unsupported, plan.errors, verdict))',
     '        len(watches), plan.unsupported + 1, plan.errors, verdict))'),
    ("M104", "counters", '        verdict = "UNKNOWN" if live is None else ("AGREE" if live == config_flag else "DIFFER")',
     '        verdict = "UNKNOWN" if live is None else ("AGREE" if live == int(config_flag) else "DIFFER")'),
    ("M105", "counters", '    for k, (role, path, kind, mask, via) in enumerate(watches, 1):',
     '    for k, (role, path, kind, mask, via) in enumerate(watches, 0):'),
]


def git(repo, *args, check=True):
    p = subprocess.run(["git", "-C", repo] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       stdin=subprocess.DEVNULL)
    if check and p.returncode != 0:
        raise RuntimeError("git %s failed (rc=%d): %s / %s" % (
            " ".join(args[:2]), p.returncode, p.stderr.decode("utf-8", "replace").strip(),
            p.stdout.decode("utf-8", "replace").strip()))
    return p


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def run_oracle(repo, rev, work, ctl_path):
    env = {"PATH": SAFE_PATH, "HOME": work, "TMPDIR": work, "LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"}
    p = subprocess.run([sys.executable, "-I", ctl_path, "--claim", "c2", "--repo", repo, "--rev", rev,
                        "--work", os.path.join(work, "h")], cwd=work, env=env, stdin=subprocess.DEVNULL,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
    return p.stdout.decode("utf-8", "replace").strip(), p.stderr.decode("utf-8", "replace").strip(), p.returncode


def run_selftest(tool_path, work):
    env = {"PATH": SAFE_PATH, "HOME": work, "TMPDIR": work, "LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"}
    p = subprocess.run([sys.executable, "-I", tool_path, "--selftest"], cwd=work, env=env, stdin=subprocess.DEVNULL,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
    return p.stdout.decode("utf-8", "replace").strip(), p.stderr.decode("utf-8", "replace").strip(), p.returncode


def parse_c2(line):
    out = {"fixtures": None, "holdout": None, "verdict": None}
    for part in line.split():
        if part.startswith("fixtures="):
            out["fixtures"] = part.split("=", 1)[1]
        elif part.startswith("holdout="):
            out["holdout"] = part.split("=", 1)[1]
        elif part.startswith("verdict="):
            out["verdict"] = part.split("=", 1)[1]
    return out


def main(argv):
    repo = work = out = None
    i = 0
    while i < len(argv):
        k = argv[i]
        if k == "--repo":
            repo = argv[i + 1]; i += 2
        elif k == "--work":
            work = argv[i + 1]; i += 2
        elif k == "--out":
            out = argv[i + 1]; i += 2
        else:
            print("usage: --repo DIR --work DIR --out DIR"); return 2
    os.makedirs(work, exist_ok=True)
    os.makedirs(out, exist_ok=True)
    top = git(repo, "rev-parse", "--show-toplevel").stdout.decode().strip()
    if os.path.realpath(top) != os.path.realpath(repo):
        print("refusing: repo toplevel %s != %s" % (top, repo)); return 2
    ctl_path = os.path.join(repo, "quality", "check-r56-controls.py")
    pristine = open(os.path.join(repo, TOOL_REL), "rb").read()
    base_sha = sha256_bytes(pristine)
    records = []
    # pristine baseline
    git(repo, "add", TOOL_REL)
    rev = git(repo, "rev-parse", "HEAD").stdout.decode().strip()
    line, err, rc = run_oracle(repo, rev, work, ctl_path)
    st_out, st_err, st_rc = run_selftest(os.path.join(repo, TOOL_REL), work)
    base = {"id": "BASE", "area": "-", "old": "-", "new": "-", "sha256": base_sha, "blob": "-",
            "rev": rev, "c2_line": line, "c2_rc": rc, "selftest_rc": st_rc, "selftest_line": st_out.splitlines()[-1] if st_out else "",
            "verdict": "PRISTINE"}
    records.append(base)
    open(os.path.join(out, "baseline.txt"), "w").write(
        "MADO_WATCH_SELFTEST: %s\n%s\nrc=%d\n%s\n" % (st_out.splitlines()[-1] if st_out else "", line, rc, err))
    for mid, area, old, new in MUTANTS:
        text = pristine.decode("utf-8")
        cnt = text.count(old)
        if cnt != 1:
            records.append({"id": mid, "area": area, "old": old, "new": new, "verdict": "SKIPPED-AMBIGUOUS",
                            "note": "old snippet occurs %d times" % cnt})
            continue
        mutated = text.replace(old, new).encode("utf-8")
        path = os.path.join(repo, TOOL_REL)
        with open(path, "wb") as fh:
            fh.write(mutated)
        git(repo, "add", TOOL_REL)
        git(repo, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "-m", "mutant " + mid)
        rev = git(repo, "rev-parse", "HEAD").stdout.decode().strip()
        blob = git(repo, "rev-parse", "HEAD:" + TOOL_REL).stdout.decode().strip()
        c2_line, c2_err, c2_rc = run_oracle(repo, rev, work, ctl_path)
        st_out, st_err, st_rc = run_selftest(path, work)
        parsed = parse_c2(c2_line)
        fixtures_ok = parsed["fixtures"] == "18/18"
        holdout_ok = parsed["holdout"] == "8/8"
        c2_ok = c2_rc == 0 and fixtures_ok and holdout_ok
        st_ok = st_rc == 0
        if c2_ok and st_ok:
            verdict = "SURVIVED"
        else:
            verdict = "KILLED"
        rec = {"id": mid, "area": area, "old": old, "new": new, "sha256": sha256_bytes(mutated), "blob": blob,
               "rev": rev, "c2_line": c2_line, "c2_rc": c2_rc, "c2_stderr": c2_err,
               "selftest_rc": st_rc, "selftest_line": st_out.splitlines()[-1] if st_out else "",
               "selftest_stderr": st_err,
               "fixtures_ok": fixtures_ok, "holdout_ok": holdout_ok, "verdict": verdict}
        records.append(rec)
        with open(os.path.join(out, "receipts", "%s.txt" % mid), "w") as fh:
            fh.write("== %s (%s)\nold: %s\nnew: %s\nsha256: %s\nblob: %s\nc2(rc=%d): %s\nselftest(rc=%d): %s\nverdict: %s\n"
                     % (mid, area, old.strip(), new.strip(), rec["sha256"], blob, c2_rc, c2_line, st_rc,
                        rec["selftest_line"], verdict))
        print("%s %-8s %-11s %s" % (mid, area, verdict, c2_line))
    # restore the pristine tool bytes
    with open(os.path.join(repo, TOOL_REL), "wb") as fh:
        fh.write(pristine)
    git(repo, "add", TOOL_REL)
    git(repo, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "-m", "restore pristine tool")
    final = open(os.path.join(repo, TOOL_REL), "rb").read()
    assert sha256_bytes(final) == base_sha, "restore failed"
    with open(os.path.join(out, "results.json"), "w") as fh:
        json.dump({"base_sha256": base_sha, "records": records}, fh, indent=1, sort_keys=True)
    with open(os.path.join(out, "results.tsv"), "w") as fh:
        fh.write("id\tarea\tverdict\tc2_line\tselftest_line\tsha256\tblob\n")
        for r in records:
            fh.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (r["id"], r.get("area", "-"), r["verdict"],
                                                      r.get("c2_line", "-"), r.get("selftest_line", "-"),
                                                      r.get("sha256", "-"), r.get("blob", "-")))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
