#!/usr/bin/env python3
"""Round-56 wave-2 seat R56W2MutC2ToolB: mutation test of tools/mado-watchplan.py.

Oracle = the unchanged C2 harness (quality/r56_ctl_c2.py at the frozen rev, staged layout of
registration-v2 E6, 26 fixtures: 18 committed + 8 hold-out) AND the tool's own --selftest.

The lane is never touched: the tool is mutated only in COPIES inside --work.
Usage:  python3 -I mutate.py --repo REPO --rev REV --work DIR --out DIR [--only ID[,ID...]] [--jobs N]
"""
import argparse
import json
import multiprocessing
import os
import re
import shutil
import subprocess
import sys
import time

SAFE_PATH = "/usr/local/bin:/usr/bin:/bin"
COMMITTED_IDS = ["F%02d" % i for i in range(1, 19)]
HOLDOUT_IDS = ["H%02d" % i for i in range(1, 9)]
TOOL_REL = "tools/mado-watchplan.py"
# the lane paths the C2 harness reads at rev (the archive of the whole lane is 584 MB)
NEEDED_PATHS = ["tools/mado-watchplan.py", "quality", ".ufo/waves/round-56/fixtures",
                ".ufo/waves/round-56/ctl", ".ufo/waves/round-56/frozen-tables-v2.json"]

# ---------------------------------------------------------------- mutants
# (id, area, anchor line(s), replacement, note)
M = [
    # ---- absolute_path
    ("m01", "absolute_path", "    if raw[0] == \"~\":", "    if raw[0] == \"~\" and raw[1:2] == \"/\":",
     "tilde only expands when a slash follows"),
    ("m02", "absolute_path", "            return parent + raw[2:]", "            return parent + raw[3:]",
     "off-by-one in the ../ branch"),
    ("m03", "absolute_path", "        if raw.startswith(\"./\"):", "        if raw.startswith(\".//\"):",
     "./ branch never taken"),
    ("m04", "absolute_path", "        return curdir + \"/\" + raw", "        return curdir + raw",
     "bare/dot path loses its separator"),
    ("m05", "absolute_path", "            pos = curdir.rfind(\"/\")", "            pos = curdir.rfind(\"/\") + 1",
     "off-by-one on the parent directory bound"),
    ("m06", "absolute_path", "        return home + raw[1:]", "        return home + raw[1:] if home is not None else raw",
     "tilde with home=None falls through"),
    # ---- glob
    ("m07", "glob", "        found = glob.glob(pattern)", "        found = glob.glob(pattern, recursive=True)",
     "recursive glob enables ** semantics"),
    ("m08", "glob", "        return sorted(found, key=bytewise)", "        return sorted(found)",
     "bytewise order replaced by code-point order"),
    ("m09", "glob", "    except (OSError, ValueError, RecursionError, re.error):", "    except (OSError, ValueError):",
     "re.error/RecursionError no longer swallowed"),
    ("m10", "glob", "            self.event_error(via, raw, \"nomatch\")", "            self.event_error(via, raw, \"no-match\")",
     "nomatch reason renamed"),
    ("m11", "glob", "        matches = expand(absolute_path(raw, cur, self.home))", "        matches = expand(raw)",
     "glob pattern not made absolute"),
    # ---- stat error handling
    ("m12", "stat", "                self.event_error(via, raw, \"inaccessible\")", "                self.event_error(via, raw, \"nomatch\")",
     "inaccessible downgraded to nomatch"),
    ("m13", "stat", "                mode = os.stat(target).st_mode", "                mode = os.lstat(target).st_mode",
     "stat replaced by lstat (symlink not followed)"),
    ("m14", "stat", "                self.event_error(via, raw, \"inaccessible\")\n                return",
     "                self.event_error(via, raw, \"inaccessible\")\n                continue",
     "the rest of the line's matches is no longer skipped"),
    ("m15", "stat", "            except (OSError, ValueError):\n                self.event_error(via, raw, \"inaccessible\")",
     "            except OSError:\n                self.event_error(via, raw, \"inaccessible\")",
     "ValueError no longer caught"),
    # ---- symlink canonical watch
    ("m16", "canonical", "            if os.path.islink(path):", "            if False:",
     "canonical watch never emitted"),
    ("m17", "canonical", "                out.append((\"canonical\", canonical, \"file\", MASK_CANON, via))",
     "                out.append((\"canonical\", canonical, \"file\", MASK_FILE, via))",
     "canonical watch carries the primary mask"),
    ("m18", "canonical", "                    canonical = os.path.realpath(path, strict=True)",
     "                    canonical = os.path.realpath(path)", "realpath no longer strict"),
    ("m19", "canonical", "                except (OSError, ValueError, RuntimeError):", "                except (OSError, ValueError):",
     "RuntimeError no longer caught"),
    ("m20", "canonical", "                out.append((\"canonical\", canonical, \"file\", MASK_CANON, via))",
     "                out.append((\"canonical\", canonical, \"file\", MASK_CANON, \"main\"))",
     "canonical watch loses its via"),
    # ---- dir/file/missing typing
    ("m21", "typing", "            elif os.path.lexists(path):", "            elif os.path.exists(path):",
     "lexists replaced by exists (dangling symlink becomes missing)"),
    ("m22", "typing", "                kind, mask = \"missing\", MASK_FILE", "                kind, mask = \"missing\", MASK_DIR",
     "missing watch carries the directory mask"),
    ("m23", "typing", "                kind, mask = \"missing\", MASK_FILE", "                kind, mask = \"file\", MASK_FILE",
     "missing watch typed as file"),
    ("m24", "typing", "                kind, mask = \"dir\", MASK_DIR", "                kind, mask = \"dir\", MASK_FILE",
     "directory watch carries the file mask"),
    ("m25", "typing", "            if os.path.isdir(path):", "            if os.path.isdir(path) and not os.path.islink(path):",
     "symlink to a directory typed as file"),
    # ---- duplicate handling
    ("m26", "duplicates", "        len(plan.entries), plan.unsupported, plan.errors)]",
     "        len(set(p for p, _ in plan.entries)), plan.unsupported, plan.errors)]",
     "paths= counts distinct paths"),
    ("m27", "duplicates", "        len(plan.entries), plan.unsupported, plan.errors)]",
     "        len(plan.entries) + 1, plan.unsupported, plan.errors)]", "paths= count off by one"),
    ("m28", "duplicates", "        for path, via in self.entries:", "        for path, via in self.entries[:-1]:",
     "last entry dropped"),
    ("m29", "duplicates", "            out.append((\"primary\", path, kind, mask, via))",
     "            out.append((\"primary\", path, kind, mask, \"main\"))", "primary watch loses its via"),
    # ---- --display-root
    ("m30", "display-root", "            given = root[:-1] if root.endswith(\"/\") else root", "            given = root",
     "trailing slash of display-root kept"),
    ("m31", "display-root", "            self.prefixes.append(given)", "            pass",
     "the given text of display-root is not a prefix"),
    ("m32", "display-root", "                self.prefixes.append(os.path.realpath(root))", "                self.prefixes.append(root)",
     "display-root realpath not used as prefix"),
    ("m33", "display-root", "            if path == prefix or path.startswith(prefix + \"/\"):",
     "            if path.startswith(prefix):", "prefix match without a path-separator boundary"),
    ("m34", "display-root", "            return \"$ROOT\" + path[len(prefix):]", "            return \"$ROOT\" + path[len(prefix) + 1:]",
     "$ROOT suffix drops a character"),
    ("m35", "display-root", "            return \"$ROOT\" + path[len(prefix):]", "            return \"$ROOT/\" + path[len(prefix):]",
     "$ROOT gains a separator"),
    ("m36", "display-root", "            given = root[:-1] if root.endswith(\"/\") else root", "            given = root[:-1]",
     "display-root always loses its last character"),
    # ---- getoption parsing and verdicts
    ("m37", "getoption", "    gdata = read_getoption(opts[\"--getoption\"]) if \"--getoption\" in opts else None",
     "    gdata = read_getoption(opts[\"--getoption\"]) if \"--getoption\" in opts else b\"\"",
     "no --getoption behaves like an empty dump"),
    ("m38", "getoption", "        if isinstance(option, str) and type(value) is int:",
     "        if isinstance(option, str) and isinstance(value, int):", "bool accepted as an int value"),
    ("m39", "getoption", "        if not isinstance(obj, dict):", "        if not isinstance(obj, (dict, list)):",
     "JSON arrays accepted as records"),
    ("m40", "getoption", "        except (ValueError, RecursionError):", "        except ValueError:",
     "RecursionError no longer caught"),
    ("m41", "getoption", "        obj = json.loads(line, parse_constant=_no_constant)", "        obj = json.loads(line)",
     "NaN/Infinity accepted"),
    ("m42", "getoption", "        if not line:\n            continue", "        if not line:\n            break",
     "a blank line ends the dump scan"),
    ("m43", "getoption", "    return live.get(OPTION)", "    return live.get(OPTION, 0)", "an absent option reads as 0"),
    ("m44", "getoption", "        verdict = \"UNKNOWN\" if live is None else (\"AGREE\" if live == config_flag else \"DIFFER\")",
     "        verdict = \"UNKNOWN\" if live is None else (\"AGREE\" if live != config_flag else \"DIFFER\")",
     "AGREE and DIFFER swapped"),
    ("m45", "getoption", "        config_flag = 1 if off else 0", "        config_flag = 0 if off else 1", "config flag inverted"),
    ("m46", "getoption", "    off = value is not None and bool(value.strip(\"0\"))", "    off = value is not None",
     "any set value counts as off"),
    ("m47", "getoption", "        if self.value is not None and self.value.strip(\"0\"):", "        if self.value is not None:",
     "a zero value empties the watch list"),
    ("m48", "getoption", "            ok, number_text = config_int(rhs.split(\"#\", 1)[0].strip(WS))",
     "            ok, number_text = config_int(rhs)", "comment not cut from an option value"),
    ("m49", "getoption", "            if \"$\" in line or \"{\" in line or \"\\\\\" in line or \"##\" in rhs:",
     "            if \"$\" in line or \"{\" in line or \"##\" in rhs:", "backslash no longer unsupported"),
    # ---- config grammar
    ("m50", "grammar", "                if stack:\n                    self.unsupported += 1",
     "                if False:\n                    self.unsupported += 1", "source inside a category no longer unsupported"),
    ("m51", "grammar", "            if lhs == \"source\":", "            if lhs.startswith(\"source\"):",
     "a key merely starting with source is a source"),
    ("m52", "grammar", "            key = \":\".join(stack) + \":\" + lhs if stack else lhs", "            key = lhs",
     "category stack ignored in the key"),
    ("m53", "grammar", "                    if stack:\n                        stack.pop()",
     "                    if stack or True:\n                        stack.pop()", "pop without an emptiness guard"),
    ("m54", "grammar", "                    stack.append(line[:-1].strip(WS))", "                    stack.append(line)",
     "category name keeps its brace"),
    ("m55", "grammar", "            if not line or line[0] == \"#\":", "            if not line:", "comment lines are parsed"),
    ("m56", "grammar", "            line = raw_line.strip(WS)", "            line = raw_line.strip()",
     "strip uses the wider default set"),
    ("m57", "grammar",
     "        for number, raw_line in enumerate(data.decode(\"utf-8\", errors=\"replace\").split(\"\\n\"), 1):",
     "        for number, raw_line in enumerate(data.decode(\"utf-8\", errors=\"replace\").split(\"\\n\"), 0):",
     "line numbers start at 0"),
    ("m58", "grammar", "                self.source(rhs.split(\"#\", 1)[0].strip(WS), path, number, depth)",
     "                self.source(rhs.split(\"#\", 1)[0], path, number, depth)", "source path not stripped"),
    # ---- limits
    ("m59", "limits", "                if depth + 1 > MAX_DEPTH:", "                if depth + 1 >= MAX_DEPTH:",
     "depth cap off by one"),
    ("m60", "limits", "MAX_DEPTH = 16", "MAX_DEPTH = 15", "depth cap lowered"),
    ("m61", "limits", "MAX_BYTES = 1048576", "MAX_BYTES = 1048575", "size limit lowered"),
    ("m62", "limits", "        data = fh.read(MAX_BYTES + 1)", "        data = fh.read(MAX_BYTES)",
     "one byte too few is read to detect oversize"),
    ("m63", "limits", "    if len(data) > MAX_BYTES:", "    if len(data) >= MAX_BYTES:", "size comparison off by one"),
    ("m64", "limits", "MAX_ENTRIES = 262144", "MAX_ENTRIES = 1024", "entry cap lowered"),
    ("m65", "limits", "        if len(self.entries) >= MAX_ENTRIES:", "        if len(self.entries) > MAX_ENTRIES:",
     "entry cap comparison off by one"),
    # ---- usage
    ("m66", "usage", "    if len(argv) % 2:", "    if len(argv) % 2 == 0:", "argument parity inverted"),
    ("m67", "usage",
     "        if flag not in (\"--config\", \"--home\", \"--display-root\", \"--getoption\") or flag in opts:",
     "        if flag not in (\"--config\", \"--home\", \"--display-root\", \"--getoption\") and flag in opts:",
     "a repeated flag is accepted"),
    ("m68", "usage", "        if not value.startswith(\"/\"):", "        if not value.startswith(\"/\") and False:",
     "a relative argument value is accepted"),
    ("m69", "usage", "    if \"--config\" not in opts:", "    if \"--config\" in opts:", "config requirement inverted"),
    # ---- second wave: second operator on the same behaviour points
    ("m70", "absolute_path", "    if raw[0] == \"/\":", "    if raw[0] != \"/\":", "absolute-path test inverted"),
    ("m71", "absolute_path", "        if raw.startswith(\"../\"):", "        if raw.startswith(\"..\"):",
     "../ prefix widened to any two dots"),
    ("m72", "absolute_path", "        if raw.startswith(\"./\"):", "        if raw.startswith(\".\"):",
     "./ prefix widened to any dot"),
    ("m73", "absolute_path", "    pos = cur.rfind(\"/\")", "    pos = cur.rfind(\"/\") - 1", "directory bound off by one"),
    ("m74", "absolute_path", "        return home + raw[1:]", "        return home + raw[1:].lstrip(\"/\")",
     "tilde home joined without a separator"),
    ("m75", "absolute_path", "    curdir = cur[:pos] if pos >= 0 else cur", "    curdir = cur[:pos] if pos > 0 else cur",
     "directory bound off by one"),
    ("m76", "absolute_path", "            parent = curdir[:pos] if pos >= 0 else curdir",
     "            parent = curdir[:pos] if pos > 0 else curdir", "parent bound off by one"),
    ("m77", "glob", "        found = glob.glob(pattern)", "        found = glob.glob(pattern, recursive=False)",
     "explicitly non-recursive glob"),
    ("m78", "glob", "        return sorted(found, key=bytewise)", "        return sorted(found, key=bytewise, reverse=True)",
     "bytewise order reversed"),
    ("m79", "glob", "        found = glob.glob(pattern)", "        found = glob.glob(pattern, include_hidden=True)",
     "hidden files included in the glob"),
    ("m80", "stat", "            if stat.S_ISREG(mode):", "            if not stat.S_ISREG(mode):", "regular-file test inverted"),
    ("m81", "stat", "            elif stat.S_ISDIR(mode):", "            elif not stat.S_ISDIR(mode):", "directory test inverted"),
    ("m82", "stat", "            target = absolute_path(match, cur, self.home) if match else match",
     "            target = match", "match not made absolute"),
    ("m83", "stat", "        if len(raw) < 2:", "        if len(raw) < 1:", "bogus threshold lowered"),
    ("m84", "stat", "        if len(raw) < 2:", "        if len(raw) < 3:", "bogus threshold raised"),
    ("m85", "canonical", "                out.append((\"canonical\", canonical, \"file\", MASK_CANON, via))",
     "                out.append((\"canonical\", canonical, \"file\", MASK_CANON, path))", "canonical via replaced by the path"),
    ("m86", "canonical", "            if os.path.islink(path):", "            if not os.path.islink(path):",
     "symlink test inverted"),
    ("m87", "canonical", "            out.append((\"primary\", path, kind, mask, via))",
     "            out.append((\"primary\", path, kind, mask, canonical))", "primary watch via replaced by a canonical name"),
    ("m88", "typing", "            if os.path.isdir(path):", "            if os.path.isfile(path):", "directory test replaced by file test"),
    ("m89", "typing", "            elif os.path.lexists(path):", "            elif os.path.islink(path):",
     "existence test replaced by a symlink test"),
    ("m90", "typing", "                kind, mask = \"dir\", MASK_DIR", "                kind, mask = \"missing\", MASK_DIR",
     "directory watch typed as missing"),
    ("m91", "duplicates", "        for path, via in self.entries:", "        for path, via in reversed(self.entries):",
     "entry order reversed"),
    ("m92", "duplicates", "        for path, via in self.entries:", "        for path, via in self.entries[1:]:",
     "first entry dropped"),
    ("m93", "duplicates", "        self.entries.append((path, via))", "        self.entries.append((via, path))",
     "entry tuple order swapped"),
    ("m94", "display-root", "            if path == prefix or path.startswith(prefix + \"/\"):",
     "            if path.startswith(prefix + \"/\"):", "the prefix itself no longer matches"),
    ("m95", "display-root", "            given = root[:-1] if root.endswith(\"/\") else root", "            given = root[1:]",
     "display-root loses its first character"),
    ("m96", "display-root", "                self.prefixes.append(os.path.realpath(root))",
     "                self.prefixes.append(os.path.realpath(root) + \"/\")", "realpath prefix gains a separator"),
    ("m97", "getoption", "    live = live_value(gdata) if gdata is not None else None",
     "    live = live_value(gdata) if gdata else None", "an empty dump is treated as no dump"),
    ("m98", "getoption", "    if gdata is not None:", "    if gdata:", "the LIVE line is emitted for an empty dump"),
    ("m99", "getoption", "        option, value = obj.get(\"option\"), obj.get(\"int\")",
     "        option, value = obj.get(\"option\"), obj.get(\"value\")", "the dump's key is renamed"),
    ("m100", "getoption", "        live[option] = value", "        live.setdefault(option, value)",
     "the first record of an option wins"),
    ("m101", "getoption", "        if isinstance(option, str) and type(value) is int:",
     "        if not isinstance(option, str) or type(value) is int:", "the record filter inverted"),
    ("m102", "getoption", "    off = value is not None and bool(value.strip(\"0\"))",
     "    off = value is not None and bool(value.strip(\"0\").strip(\" \"))", "a space-padded zero is not off"),
    ("m103", "grammar", "            if lhs.startswith(\"$\"):", "            if not lhs.startswith(\"$\"):",
     "the variable rule inverted"),
    ("m104", "grammar", "            lhs, rhs = lhs.strip(WS), rhs.strip(WS)", "            lhs, rhs = lhs.strip(WS), rhs",
     "the right-hand side is not stripped"),
    ("m105", "grammar", "            lhs, _, rhs = line.partition(\"=\")", "            lhs, _, rhs = line.rpartition(\"=\")",
     "the last '=' splits instead of the first"),
    ("m106", "grammar", "            if key != OPTION:", "            if key == OPTION:", "the option-key test inverted"),
    ("m107", "grammar", "            if ok:", "            if not ok:", "the value-accept test inverted"),
    ("m108", "grammar", "            if \"$\" in line or \"{\" in line or \"\\\\\" in line or \"##\" in rhs:",
     "            if \"$\" in rhs or \"{\" in rhs or \"\\\\\" in rhs or \"##\" in rhs:",
     "the unsupported-value test moved from the line to the RHS"),
    ("m109", "limits", "        if len(self.entries) >= MAX_ENTRIES:", "        if len(self.entries) >= MAX_ENTRIES // 2:",
     "entry cap halved"),
    ("m110", "limits", "                if depth + 1 > MAX_DEPTH:", "                if depth + 1 > MAX_DEPTH + 1:",
     "depth cap raised"),
    ("m111", "limits", "MAX_BYTES = 1048576", "MAX_BYTES = 2097152", "size limit doubled"),
    ("m112", "limits", "    if len(data) > MAX_BYTES:", "    if len(data) > 0:", "the size limit is never applied"),
    ("m113", "usage", "    if len(argv) % 2:", "    if len(argv) % 2 != 2:", "the argument count test changed"),
    ("m114", "usage", "        opts[flag] = value", "        opts[flag] = value.strip()", "the argument value is stripped"),
    ("m115", "watchlist", "        out = []\n        if self.value is not None and self.value.strip(\"0\"):",
     "        out = []\n        if self.value is not None and self.value.strip(\"1\"):", "a value of 1 does not empty the watch list"),
    ("m116", "watchlist", "        if self.value is not None and self.value.strip(\"0\"):",
     "        if self.value is not None and self.value.strip(\"0\") != \"\":", "the watch-list gate always fires"),
    ("m117", "watchlist", "            out.append((\"primary\", path, kind, mask, via))",
     "            out.append((\"primary\", os.path.realpath(path), kind, mask, via))",
     "the primary watch prints the realpath"),
]

_W = {}


def _init(repo, rev, work, wid):
    _W["orig"] = repo
    _W["rev"] = rev
    _W["work"] = work
    _W["env"] = {"PATH": SAFE_PATH, "HOME": work, "TMPDIR": work, "LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"}
    _W["python"] = shutil.which("python3", path=SAFE_PATH)
    # per-worker slim copy of the lane paths the harness reads at rev (scratch only)
    wroot = os.path.join(work, "w%02d" % (os.getpid() % 1000))
    os.makedirs(wroot, exist_ok=True)
    repo = os.path.join(wroot, "repo")
    shutil.rmtree(repo, ignore_errors=True)
    os.makedirs(repo)
    subprocess.run(["git", "-C", repo, "init", "-q", "--template="], env=_W["env"])
    arc = subprocess.run(["git", "-C", _W["orig"], "archive", "--format=tar", rev, "--"] + NEEDED_PATHS,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(["tar", "-x", "--no-same-owner", "-C", repo, "-f", "-"], input=arc.stdout,
                   stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, env=_W["env"])
    subprocess.run(["git", "-C", repo, "add", "-A"], env=_W["env"])
    subprocess.run(["git", "-C", repo, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "-m", "base"],
                   env=_W["env"])
    _W["repo"] = repo
    _W["wrev"] = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"], stdout=subprocess.PIPE,
                                env=_W["env"]).stdout.decode().strip()
    _W["wroot"] = wroot
    # fixture export for the per-fixture breakdown (scratch copy of the lane's fixtures)
    export = os.path.join(wroot, "export")
    shutil.rmtree(export, ignore_errors=True)
    os.makedirs(export)
    arc3 = subprocess.run(["git", "-C", _W["orig"], "archive", "--format=tar", rev, "--",
                            ".ufo/waves/round-56/fixtures"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(["tar", "-x", "--no-same-owner", "-C", export, "-f", "-"], input=arc3.stdout,
                   stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, env=_W["env"])
    # the unchanged harness, imported from the rev
    hsrc = subprocess.run(["git", "-C", repo, "show", "%s:quality/r56_ctl_c2.py" % _W["wrev"]],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
    hpath = os.path.join(wroot, "r56_ctl_c2_harness.py")
    with open(hpath, "wb") as fh:
        fh.write(hsrc)
    sys.path.insert(0, wroot)
    import r56_ctl_c2_harness as H
    _W["H"] = H


def _run(cmd, cwd=None, timeout=300):
    return subprocess.run(cmd, cwd=cwd, env=_W["env"], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, timeout=timeout)


def _one(job):
    mid, area, old, new, note = job
    t0 = time.time()
    repo, rev, env, python, H = _W["repo"], _W["rev"], _W["env"], _W["python"], _W["H"]
    wroot = _W["wroot"]
    pristine = subprocess.run(["git", "-C", _W["orig"], "show", "%s:%s" % (rev, TOOL_REL)],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("utf-8")

    def invalid(detail):
        return {"id": mid, "area": area, "note": note, "old": old, "new": new, "verdict": "INVALID",
                "detail": detail, "seconds": round(time.time() - t0, 2)}

    if old not in pristine:
        return invalid("anchor not found: %r" % old)
    if pristine.count(old) != 1:
        return invalid("anchor not unique (%d hits)" % pristine.count(old))
    mutated = pristine.replace(old, new)
    if len(mutated.split("\n")) != len(pristine.split("\n")):
        return invalid("mutation changes the line count")
    ndiff = sum(1 for a, b in zip(pristine.split("\n"), mutated.split("\n")) if a != b)
    if ndiff != 1:
        return invalid("mutation changes %d lines" % ndiff)

    mdir = os.path.join(wroot, "mut", mid)
    shutil.rmtree(mdir, ignore_errors=True)
    os.makedirs(mdir)
    mtool = os.path.join(mdir, "mado-watchplan.py")
    with open(mtool, "w", encoding="utf-8") as fh:
        fh.write(mutated)
    syn = _run([python, "-m", "py_compile", mtool], timeout=60)
    if syn.returncode != 0:
        return invalid("syntax error: %s" % syn.stderr.decode()[:200])

    # oracle leg 1: the tool's own --selftest (unchanged oracle, mutated tool)
    st = _run([python, "-I", mtool, "--selftest"], cwd=mdir, timeout=300)
    st_out = st.stdout.decode("utf-8", "replace").strip().split("\n")
    st_pass = st.returncode == 0
    st_line = next((l for l in st_out if l.startswith("MADO_WATCH_SELFTEST")), "")
    st_fail = [l for l in st_out if "FAIL" in l]

    # oracle leg 2: the C2 harness over the 26 fixtures, staged (registration-v2 E6)
    shutil.copyfile(mtool, os.path.join(repo, TOOL_REL))
    subprocess.run(["git", "-C", repo, "add", "-A"], env=env)
    subprocess.run(["git", "-C", repo, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-q", "-m", mid],
                   env=env)
    mrev = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"], stdout=subprocess.PIPE, env=env).stdout.decode().strip()
    hwork = os.path.join(wroot, "harness", mid)
    shutil.rmtree(hwork, ignore_errors=True)
    os.makedirs(hwork, exist_ok=True)
    hp = _run([python, "-I", os.path.join(repo, "quality/r56_ctl_c2.py"), "--repo", repo, "--rev", mrev,
               "--work", hwork], cwd=hwork, timeout=600)
    hline = hp.stdout.decode("utf-8", "replace").strip()
    mm = re.search(r"fixtures=(\d+)/18 holdout=(\d+)/8 holdout_commit=(\w+) controls=(\d+)/4 verdict=(\w+)", hline)
    harness_ok = bool(mm) and mm.group(5) == "TARGET_MET"
    npass = int(mm.group(1)) + int(mm.group(2)) if mm else 0

    # per-fixture breakdown with the harness's own staged runner (which fixture caught it)
    export = os.path.join(wroot, "export")
    per = {}
    score_root = os.path.join(wroot, "score", mid)
    shutil.rmtree(score_root, ignore_errors=True)
    os.makedirs(score_root, exist_ok=True)
    for label, root, ids in (("committed", os.path.join(export, ".ufo/waves/round-56/fixtures/c2"), COMMITTED_IDS),
                             ("holdout", os.path.join(export, ".ufo/waves/round-56/fixtures/c2-holdout"), HOLDOUT_IDS)):
        for fid in ids:
            sub = os.path.join(score_root, label, fid)
            os.makedirs(sub, exist_ok=True)
            per[fid] = H.score(python, mtool, export, root, [fid], env, sub, True)
    failed = sorted(k for k, v in per.items() if v != 1)

    verdict = "KILLED" if (not st_pass or not harness_ok) else "SURVIVED"
    rec = {"id": mid, "area": area, "note": note, "old": old, "new": new, "verdict": verdict,
           "selftest_rc": st.returncode, "selftest_line": st_line, "selftest_failures": st_fail[:8],
           "fixtures_passed": npass, "fixtures_failed": failed, "harness_line": hline, "harness_ok": harness_ok,
           "mutant_rev": mrev, "seconds": round(time.time() - t0, 2)}
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", default=None)
    ap.add_argument("--jobs", type=int, default=8)
    args = ap.parse_args()

    work = os.path.realpath(args.work)
    out = os.path.realpath(args.out)
    os.makedirs(work, exist_ok=True)
    os.makedirs(out, exist_ok=True)

    todo = [m for m in M if not args.only or m[0] in args.only.split(",")]
    jobs = args.jobs
    ctx = multiprocessing.get_context("spawn")
    with ctx.Pool(jobs, initializer=_init, initargs=(args.repo, args.rev, work, 0)) as pool:
        results = []
        for rec in pool.imap_unordered(_one, todo):
            results.append(rec)
            if rec["verdict"] == "INVALID":
                print("%s INVALID %s" % (rec["id"], rec.get("detail", "")), flush=True)
            else:
                print("%s %-8s %-13s selftest=%-4s fixtures=%2d/26 harness=%s" % (
                    rec["id"], rec["verdict"], rec["area"],
                    "ok" if rec["selftest_rc"] == 0 else "FAIL", rec["fixtures_passed"],
                    "TARGET_MET" if rec["harness_ok"] else "MISSED"), flush=True)

    results.sort(key=lambda r: r["id"])
    with open(os.path.join(out, "mutation-results.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
    with open(os.path.join(out, "mutation-results.tsv"), "w", encoding="utf-8") as fh:
        fh.write("id\tarea\tverdict\tselftest\tfixtures_passed\tnote\n")
        for r in results:
            fh.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (
                r["id"], r.get("area", ""), r["verdict"],
                "ok" if r.get("selftest_rc") == 0 else "FAIL(rc=%s)" % r.get("selftest_rc"),
                r.get("fixtures_passed", "-"), r.get("note", "").replace("\t", " ")))
    nk = sum(1 for r in results if r["verdict"] == "KILLED")
    ns = sum(1 for r in results if r["verdict"] == "SURVIVED")
    ni = sum(1 for r in results if r["verdict"] == "INVALID")
    print("TOTAL killed=%d survived=%d invalid=%d of %d" % (nk, ns, ni, len(results)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
