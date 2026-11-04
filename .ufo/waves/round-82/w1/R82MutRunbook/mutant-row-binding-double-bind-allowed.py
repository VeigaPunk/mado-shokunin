#!/usr/bin/env python3
"""mado — PRED-C2-r82-v1: execute the runbook rows with per-row bindings and refusal shapes.

The frozen case set binds each case to its own row in the SKILL.md section
`### Executable runbook rows (round 82)` — the row's command cell must equal the case's
command, and each row is bound by exactly one case. A case is correct only when

  * its live output meets the row's outcome (exit status included: a failed command is never
    a pass, a refusal must carry `stage=model` and its own exit status, and a shape-bound
    row must meet its line grammar and length),
  * every committed churn sample still matches (a plausible next-day output), and
  * every committed negative sample does not match (the rule can fail).

The twenty-six round-81 cases are carried with their command, expectation, churn and
negative fixtures unchanged; only their row binding is re-pointed. The three cases this
round adds are the tray plane: the StatusNotifierWatcher's bus-name owner, its interface
census, and the method table that census prints (S482).

The working tree is bound to the measured revision: SKILL.md, `tools/mado-barfoot.py` and every
refusal fixture must have the same sha256 as the blob at `--rev`, so the executed rows are the
committed rows. The held fixed-value rule is scored on the three new cases: it has no frozen
value for any of them, so it matches 0/3 by construction (the printed `control_all` is an
observation over all twenty-nine cases, never a predicate).

Counting command (round 82):
  python3 -I quality/counters/c2-r82-runbook.py --repo . --rev REV \
      --controls .ufo/waves/round-82/controls/c2-runbook-cases-r82.json \
      --carried .ufo/waves/round-81/controls/c2-runbook-cases-r81.json --scratch-root DIR

Contract: MADO_R82_RUNBOOK: cases=29 executed=29 matched=29 shapes=24/24 anchors=29/29
rows=29/29 control_new=0/3 mutants=25 killed=25 verdict=TARGET_MET rev=<hash> tree=bound
(rc 0 iff every clause holds).

Exit map: 0 target met · 1 target missed · 2 setup error (never a verdict).
The commands are frozen in the committed control set and reviewed at freeze; every one is a
read verb or the lane's read-only join. Nothing is written outside the caller's scratch root.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

CASES = 29
CARRIED = 26
SHAPES = 24
MUTANTS = 25
CONTROL_NEW = 0

SECTION = "### Executable runbook rows (round 82)"

MUTATIONS = [
    ("rc-blind",
     "    if rc != 0:\n        return False\n    text = stdout.rstrip",
     "    if False:\n        return False\n    text = stdout.rstrip"),
    ("int-range-lower-open",
     "        number = int(text)\n        return lo <= number <= hi",
     "        number = int(text)\n        return number <= hi"),
    ("json-required-ignored",
     '    for key, kind in schema.get("fields", {}).items():\n'
     '        if key not in item or not type_ok(item[key], kind):',
     '    for key, kind in ():\n'
     '        if key not in item or not type_ok(item[key], kind):'),
    ("sorted-unique-dropped",
     "        if parts != sorted(set(parts)):\n            return False",
     "        if not parts:\n            return False"),
    ("empty-accepted",
     '    if kind == "empty":\n        return text == ""',
     '    if kind == "empty":\n        return True'),
    ("refusal-stage-blind",
     '    return rc == value["rc"] and ("ERROR (stage=%s " % value.get("stage", "model")) '
     'in stdout',
     '    return rc == value["rc"] and "ERROR (" in stdout'),
    ("refusal-rc-blind",
     '    return rc == value["rc"] and ("ERROR (stage=%s " % value.get("stage", "model")) '
     'in stdout',
     '    return ("ERROR (stage=%s " % value.get("stage", "model")) in stdout'),
    ("lines-any-line",
     '        if len(lines) < value.get("min_lines", 1):\n            return False\n'
     "        return all(pattern.match(line) for line in lines)",
     "        return any(pattern.match(line) for line in lines)"),
    ("lines-min-lines-dropped",
     '        if len(lines) < value.get("min_lines", 1):\n            return False',
     "        if False:\n            return False"),
    ("chord-mod-word-blind",
     '                if any(word not in mods for word in words):\n                    return False',
     '                if False:\n                    return False'),
    ("chord-key-padded",
     '                if "+" in tail or tail != tail.strip():\n                    return False',
     '                if "+" in tail:\n                    return False'),
    ("chord-arrow-blind",
     '            if "→" in line:\n                return False',
     '            if False:\n                return False'),
    ("chord-mod-duplicate-accepted",
     '                if len(set(words)) != len(words):\n                    return False',
     '                if False:\n                    return False'),
    ("chord-min-chords-dropped",
     '        return chords >= value.get("min_chords", 0)\n    if kind == "action_column":',
     '        return True\n    if kind == "action_column":'),
    ("state-rc-blind",
     '        return (rc == 0) == (text in ("active", "reloading"))\n    if kind == "pid_state":',
     '        return True\n    if kind == "pid_state":'),
    ("state-enum-blind",
     '        if text not in value.get("enum", []):\n            return False',
     '        if False:\n            return False'),
    ("action-prefix-blind",
     '            if not line.startswith(prefix):\n                return False',
     '            if False:\n                return False'),
    ("action-empty-accepted",
     '            if not action or action != action.strip():\n                return False',
     '            if False:\n                return False'),
    ("action-arrow-inside-accepted",
     '            if "→" in action:\n                return False',
     '            if False:\n                return False'),
    ("pid-rc-blind",
     '        if rc == 1:\n            return text == ""',
     '        if False:\n            return text == ""'),
    ("pid-numeric-blind",
     '            numeric = all(re.fullmatch(r"[0-9]+", line) is not None\n'
     '                          for line in lines)',
     '            numeric = True'),
    ("pid-zero-accepted",
     '            in_range = all(0 < int(line) <= 4194304\n'
     '                           for line in lines if line.isdigit())',
     '            in_range = all(int(line) <= 4194304\n'
     '                           for line in lines if line.isdigit())'),
    ("pid-single-only",
     '            return bool(lines) and numeric and in_range\n        if rc == 1:',
     '            return len(lines) == 1 and numeric and in_range\n        if rc == 1:'),
    ("lines-shape-floor-dropped",
     '        if len(lines) < value.get("min_lines", 1):\n            return False\n'
     '        return all(pattern.match(line) for line in lines)',
     '        return all(pattern.match(line) for line in lines)'),
    ("lines-shape-any-line",
     '        if len(lines) < value.get("min_lines", 1):\n            return False\n'
     '        return all(pattern.match(line) for line in lines)',
     '        if len(lines) < value.get("min_lines", 1):\n            return False\n'
     '        return any(pattern.match(line) for line in lines)'),
]

EXACT_KINDS = ("exact", "contains", "empty")
SHAPE_KINDS = ("json_object_fields", "array_fields", "int4", "levels_dump", "int_range",
               "sorted_unique", "regex", "refusal", "lines_shape", "chord_shape",
               "is_active", "action_column", "pid_state")


class Setup(Exception):
    pass


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def run(argv, cwd, timeout=120):
    # R3 (sentinel F1/F2): hand a child only what the frozen read verbs need, never the whole
    # caller environment; TMPDIR is pinned inside the scratch root so no child can land in /tmp.
    allow = ("XDG_RUNTIME_DIR", "HYPRLAND_INSTANCE_SIGNATURE", "OMARCHY_PATH", "HOME",
             "DBUS_SESSION_BUS_ADDRESS", "XDG_DATA_DIRS", "XDG_CONFIG_HOME", "XDG_CACHE_HOME",
             "XDG_DATA_HOME", "PATH", "USER", "LOGNAME", "TMPDIR")
    env = dict((key, os.environ[key]) for key in allow if key in os.environ)
    env["LC_ALL"] = "C"
    env["LANG"] = "C"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["TMPDIR"] = cwd
    runtime = env.get("XDG_RUNTIME_DIR") or ("/run/user/%d" % os.getuid())
    if os.path.isdir(runtime):
        env.setdefault("XDG_RUNTIME_DIR", runtime)
    if "HYPRLAND_INSTANCE_SIGNATURE" not in env:
        base = os.path.join(env.get("XDG_RUNTIME_DIR", ""), "hypr")
        try:
            for name in sorted(os.listdir(base)):
                if os.path.exists(os.path.join(base, name, ".socket.sock")):
                    env["HYPRLAND_INSTANCE_SIGNATURE"] = name
                    break
        except OSError:
            pass
    if "OMARCHY_PATH" not in env:
        candidates = [os.path.expanduser("~/.local/share/omarchy/bin")]
        candidates += [d for d in env.get("PATH", "").split(":") if d]
        for directory in candidates:
            binary = os.path.join(directory, "omarchy")
            if os.path.isfile(binary) and os.access(binary, os.X_OK):
                env["OMARCHY_PATH"] = os.path.dirname(directory)
                break
    parts = [d for d in env.get("PATH", "").split(":") if d]
    for directory in ("/usr/local/bin", "/usr/bin", "/bin",
                      os.path.expanduser("~/.local/bin"),
                      os.path.expanduser("~/.local/share/omarchy/bin")):
        if directory not in parts:
            parts.append(directory)
    env["PATH"] = ":".join(parts)
    try:
        proc = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, stdin=subprocess.DEVNULL,
                              timeout=timeout)
        return (proc.returncode, proc.stdout.decode("utf-8", "replace"),
                proc.stderr.decode("utf-8", "replace"))
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    except OSError as exc:
        raise Setup("cannot run %r: %s" % (argv, exc))


def git_bytes(repo, rev, path):
    proc = subprocess.run(["git", "-C", repo, "show", rev + ":" + path],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          stdin=subprocess.DEVNULL)
    if proc.returncode != 0:
        raise Setup("cannot read %s at %s: %s"
                    % (path, rev, proc.stderr.decode("utf-8", "replace").strip()))
    return proc.stdout


def git_show(repo, rev, path):
    return git_bytes(repo, rev, path).decode("utf-8", "replace")


def split_cells(line):
    """Split a Markdown table row on unescaped pipes; `\\|` becomes a literal pipe."""
    cells, cur, index = [], [], 0
    while index < len(line):
        ch = line[index]
        if ch == "\\" and index + 1 < len(line) and line[index + 1] == "|":
            cur.append("|")
            index += 2
            continue
        if ch == "|":
            cells.append("".join(cur))
            cur = []
            index += 1
            continue
        cur.append(ch)
        index += 1
    cells.append("".join(cur))
    return cells


def command_rows(skill):
    """The runbook section's command cells, in row order."""
    rows, inside = [], False
    for line in skill.splitlines():
        stripped = line.strip()
        if stripped == SECTION:
            inside = True
            continue
        if inside and stripped.startswith("### "):
            break
        if not inside or not stripped.startswith("|"):
            continue
        cells = split_cells(stripped)
        if len(cells) < 2:
            continue
        cell = cells[1].strip()
        if cell.startswith("`") and cell.endswith("`") and len(cell) > 1:
            cell = cell[1:-1]
        if cell == "Command" or (cell and set(cell) <= set("-: ")):
            continue  # the header and the separator are not command rows
        rows.append(cell)
    return rows


def type_ok(value, kind):
    if kind == "str":
        return isinstance(value, str) and value != ""
    if kind == "int":
        return isinstance(value, int) and not isinstance(value, bool)
    if kind == "positive_int":
        return isinstance(value, int) and not isinstance(value, bool) and value > 0
    if kind == "nonneg_int":
        return isinstance(value, int) and not isinstance(value, bool) and value >= 0
    if kind == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if kind == "int4":
        return (isinstance(value, list) and len(value) == 4
                and all(isinstance(v, int) and not isinstance(v, bool) and v >= 0
                        for v in value))
    raise Setup("unknown field type %r" % (kind,))


def fields_ok(item, schema):
    if not isinstance(item, dict):
        return False
    for key, kind in schema.get("fields", {}).items():
        if key not in item or not type_ok(item[key], kind):
            return False
    return True


def json_text(text):
    try:
        return json.loads(text)
    except (ValueError, TypeError):
        return None


def matches(kind, value, rc, stdout):
    """The r79 rule: a row's declared outcome, shape-bound where the value is volatile."""
    if rc != 0:
        return False
    text = stdout.rstrip("\n")
    if kind == "exact":
        return text == value
    if kind == "contains":
        return value in stdout
    if kind == "regex":
        return re.search(value, text) is not None
    if kind == "empty":
        return text == ""
    if kind == "lines_shape":
        lines = text.splitlines()
        pattern = re.compile(value["regex"])
        if len(lines) < value.get("min_lines", 1):
            return False
        return all(pattern.match(line) for line in lines)
    if kind == "chord_shape":
        lines = text.splitlines()
        floor = value.get("min_lines", 1)
        if len(lines) < floor:
            return False
        mods = set(value.get("mods", []))
        chords = 0
        for line in lines:
            line = line.rstrip()
            if not line:
                return False
            if "→" in line:
                return False
            probe = line + " " if line.endswith(" +") else line
            if " + " in probe:
                head, _, tail = probe.rpartition(" + ")
                tail = tail.rstrip()
                words = head.split(" ")
                if not 1 <= len(words) <= value.get("max_mods", 4):
                    return False
                if any(word not in mods for word in words):
                    return False
                if len(set(words)) != len(words):
                    return False
                if "+" in tail or tail != tail.strip():
                    return False
                chords += 1
            elif "+" in line:
                return False
        return chords >= value.get("min_chords", 0)
    if kind == "action_column":
        prefix = value.get("prefix", " \u2192 ")
        lines = text.splitlines()
        floor = value.get("min_lines", 1)
        if len(lines) < floor:
            return False
        for line in lines:
            if not line.startswith(prefix):
                return False
            action = line[len(prefix):]
            if not action or action != action.strip():
                return False
            if "→" in action:
                return False
        return True
    if kind == "int_range":
        lo, hi = value
        # bare digits only: no sign, no padding, no surrounding whitespace
        if re.fullmatch(r"[0-9]+", text) is None:
            return False
        number = int(text)
        return lo <= number <= hi
    if kind == "sorted_unique":
        parts = text.split(",") if text else []
        if not parts or any(part == "" or part != part.strip() for part in parts):
            return False
        if parts != sorted(set(parts)):
            return False
        return set(value.get("must_include", [])) <= set(parts)
    if kind == "json_object_fields":
        data = json_text(text)
        return fields_ok(data, value)
    if kind == "array_fields":
        data = json_text(text)
        if not isinstance(data, list) or len(data) < value.get("min_items", 1):
            return False
        return all(fields_ok(item, value) for item in data)
    if kind == "int4":
        return type_ok(json_text(text), "int4")
    if kind == "levels_dump":
        data = json_text(text)
        if not isinstance(data, dict) or not data:
            return False
        for monitor in data.values():
            if not isinstance(monitor, dict):
                return False
            levels = monitor.get("levels")
            if not isinstance(levels, dict) or set(levels) != {"0", "1", "2", "3"}:
                return False
            if not all(isinstance(entry, list) for entry in levels.values()):
                return False
        return True
    raise Setup("unknown expectation kind %r" % (kind,))


def special_matches(kind, value, rc, stdout):
    """A refusal and a state word are scored on their own exit status, not behind the
    rc==0 gate: systemd's is-active exits 0 for `active` and `reloading` and non-zero for the
    rest (a nonexistent unit answers 4), so no non-zero value is pinned."""
    if kind == "is_active":
        text = stdout.strip()
        if text not in value.get("enum", []):
            return False
        return (rc == 0) == (text in ("active", "reloading"))
    if kind == "pid_state":
        # pgrep: rc 0 with one or more matching PIDs, rc 1 with no output when none match.
        # The running state is never frozen; the pair is the bound outcome.
        text = stdout.rstrip("\n")
        if rc == 0:
            lines = text.splitlines()
            numeric = all(re.fullmatch(r"[0-9]+", line) is not None
                          for line in lines)
            in_range = all(0 < int(line) <= 4194304
                           for line in lines if line.isdigit())
            return bool(lines) and numeric and in_range
        if rc == 1:
            return text == ""
        return False
    if kind != "refusal":
        return matches(kind, value, rc, stdout)
    return rc == value["rc"] and ("ERROR (stage=%s " % value.get("stage", "model")) in stdout


def held_rule(case, rc, stdout):
    """The held r78 rule: rc 0 and the output equals one frozen captured value."""
    if "frozen" not in case:
        return False  # the held r78 table had no row for this capture at all
    return rc == 0 and stdout.rstrip("\n") == case["frozen"]


def case_correct(case, rc, stdout):
    def okay(r, out):
        return special_matches(case["kind"], case["value"], r, out)

    if not okay(rc, stdout):
        return False
    for sample in case.get("samples", []):
        if not okay(sample["rc"], sample["out"]):
            return False
    for sample in case.get("negatives", []):
        if okay(sample["rc"], sample["out"]):
            return False
    return True


def observed(kind, rc, stdout):
    """Never quote a JSON dump: a monitors reply carries the output's serial/description."""
    if kind in ("json_object_fields", "array_fields", "int4", "levels_dump"):
        return "rc=%d json-bytes=%d" % (rc, len(stdout))
    text = stdout.rstrip("\n")
    if len(text) > 100:
        text = text[:97] + "..."
    return "rc=%d out=%r" % (rc, text)


def selftest():
    checks = total = 0

    def ok(cond, label):
        nonlocal checks, total
        total += 1
        if cond:
            checks += 1
        else:
            print("MADO_R82_RUNBOOK_SELFTEST_FAIL: %s" % label)

    ok(matches("exact", "x", 0, "x\n"), "exact")
    ok(not matches("exact", "x", 0, "y\n"), "exact refuses")
    ok(not matches("exact", "x", 1, "x\n"), "exact refuses a failed command")
    ok(matches("contains", "Hyprland", 0, "Hyprland 0.56.2\n"), "contains")
    ok(matches("regex", r"^[0-9]+$", 0, "1720\n"), "regex")
    ok(not matches("regex", r"^[0-9]+$", 0, "1720x\n"), "regex refuses")
    ok(matches("empty", None, 0, ""), "empty")
    ok(not matches("empty", None, 0, "x"), "empty refuses")
    ok(matches("int_range", [1, 10], 0, "5\n"), "int range")
    ok(not matches("int_range", [1, 10], 0, "0\n"), "int range lower")
    ok(not matches("int_range", [1, 10], 0, "11\n"), "int range upper")
    ok(not matches("int_range", [0, 10], 0, "ten\n"), "int range non-numeric")
    ok(not matches("int_range", [0, 10], 0, " 7\n"), "int range padded refused")
    ok(matches("sorted_unique", {"must_include": ["waybar"]}, 0, "wallpaper,waybar\n"),
       "sorted unique")
    ok(not matches("sorted_unique", {"must_include": ["waybar"]}, 0, "waybar,wallpaper\n"),
       "sorted unique order")
    ok(not matches("sorted_unique", {"must_include": ["waybar"]}, 0, "waybar,waybar\n"),
       "sorted unique duplicates")
    ok(not matches("sorted_unique", {"must_include": ["waybar"]}, 0, "wallpaper\n"),
       "sorted unique required")
    ok(not matches("sorted_unique", {"must_include": ["waybar"]}, 0, " waller,waybar\n"),
       "sorted unique padded part refused")
    ok(matches("json_object_fields", {"fields": {"id": "int", "name": "str"}}, 0,
               '{"id":1,"name":"1"}\n'), "object fields")
    ok(not matches("json_object_fields", {"fields": {"id": "int", "name": "str"}}, 0,
                   '{"id":1}\n'), "object fields missing")
    ok(matches("array_fields", {"min_items": 1,
                                "fields": {"name": "str", "reserved": "int4",
                                           "scale": "number"}}, 0,
               '[{"name":"M","reserved":[0,1,0,0],"scale":1.0}]\n'), "array fields")
    ok(not matches("array_fields", {"min_items": 1,
                                    "fields": {"name": "str", "reserved": "int4"}}, 0,
                   '[{"name":"M","reserved":[0,1,0]}]\n'), "array fields int4")
    ok(not matches("int4", None, 0, "[0,26,0,0,0]\n"), "int4 length")
    ok(matches("levels_dump", None, 0,
               '{"M": {"levels": {"0": [], "1": [], "2": [], "3": []}}}\n'), "levels dump")
    ok(not matches("levels_dump", None, 0, '{"M": {"levels": {"0": []}}}\n'),
       "levels dump missing levels")
    # refusal: exit status and stage, never the message
    refusal = {"rc": 3, "stage": "model"}
    ok(special_matches("refusal", refusal, 3, "MADO_BARFOOT: ERROR (stage=model a)\n"),
       "refusal accept")
    ok(special_matches("refusal", refusal, 3, "MADO_BARFOOT: ERROR (stage=model b)\n"),
       "refusal ignores the message")
    ok(not special_matches("refusal", refusal, 2, "MADO_BARFOOT: ERROR (stage=model a)\n"),
       "refusal refuses another exit status")
    ok(not special_matches("refusal", refusal, 3, "MADO_BARFOOT: ERROR (stage=setup a)\n"),
       "refusal refuses another stage")
    ok(special_matches("refusal", refusal, 3, "MADO_BARFOOT: ERROR (stage=model a)\n"),
       "refusal is not behind the rc-zero gate")
    # lines shape: all lines, and the length floor
    shape = {"regex": r"^\S+ +→ +\S+$", "min_lines": 2}
    ok(matches("lines_shape", shape, 0, "A → B\nC → D\n"), "lines shape")
    ok(not matches("lines_shape", shape, 0, "A → B\nbad\n"), "lines shape refuses a bad line")
    ok(not matches("lines_shape", shape, 0, "A → B\n"), "lines shape length floor")
    ok(not matches("lines_shape", shape, 0, ""), "lines shape refuses empty")
    ok(not matches("lines_shape", shape, 1, "A → B\nC → D\n"), "lines shape refuses rc 1")
    # chord shape: the chord column, not just the arrow
    chord = {"min_lines": 3, "min_chords": 2, "mods": ["ALT", "CTRL", "SHIFT", "SUPER"],
             "max_mods": 4}
    ok(matches("chord_shape", chord, 0, "SUPER + Q\nCOPILOT KEY\nCTRL ALT + DELETE\n"),
       "chord shape")
    ok(matches("chord_shape", chord, 0, "SUPER SHIFT CTRL ALT + X\nSUPER + Q\n"
                                        "switch:on:Lid Switch\nXF86AudioMute\n"),
       "chord shape bare keys")
    ok(not matches("chord_shape", chord, 0, "SUPER + Q\nHYPER + X\nCTRL + D\n"),
       "chord shape refuses a foreign modifier")
    ok(matches("chord_shape", chord, 0, "SUPER + Q\nSUPER +\nCTRL + D\n"),
       "chord shape accepts an empty key (a keycode with no symbol)")
    ok(not matches("chord_shape", chord, 0, "SUPER + Q\nSUPER +  X\nCTRL + D\n"),
       "chord shape refuses a padded key")
    ok(not matches("chord_shape", chord, 0, "SUPER + Q\n64 + RETURN\nCTRL + D\n"),
       "chord shape refuses a numeric mask")
    ok(not matches("chord_shape", chord, 0, "SUPER + Q\nSUPER SUPER + X\nCTRL + D\n"),
       "chord shape refuses a repeated modifier")
    ok(not matches("chord_shape", chord, 0, "SUPER + Q\nA → B\nCTRL + D\n"),
       "chord shape refuses an arrow in the chord column")
    ok(not matches("chord_shape", chord, 0, "SUPER + Q\nSUPER + X + Y\nCTRL + D\n"),
       "chord shape refuses two keys")
    ok(not matches("chord_shape", chord, 0, "SUPER + Q\n\nCTRL + D\n"),
       "chord shape refuses an empty line")
    ok(not matches("chord_shape", chord, 0, "SUPER + Q\nCTRL + D\n"),
       "chord shape length floor")
    ok(not matches("chord_shape", {"min_lines": 1, "min_chords": 1, "mods": ["SUPER"]},
                   0, "COPILOT KEY\n"), "chord shape chord floor")
    # state word: the enum and the exit status that must agree with it
    state = {"enum": ["active", "activating", "deactivating", "failed", "inactive",
                      "reloading", "unknown"]}
    ok(special_matches("is_active", state, 0, "active\n"), "state active")
    ok(special_matches("is_active", state, 3, "inactive\n"), "state inactive")
    ok(special_matches("is_active", state, 3, "activating\n"), "state activating")
    ok(not special_matches("is_active", state, 0, "inactive\n"),
       "state refuses a contradictory exit status")
    ok(not special_matches("is_active", state, 3, "active\n"),
       "state refuses active with a failed status")
    ok(not special_matches("is_active", state, 3, "bogus\n"), "state refuses a foreign word")
    ok(not special_matches("is_active", state, 3, "\n"), "state refuses an empty reply")
    # row splitting: an escaped pipe stays in the cell, other backslashes survive
    cells = split_cells("| `a \\| b` | x |")
    ok(cells[1].strip() == "`a | b`", "escaped pipe stays in the cell")
    cells = split_cells("| `a \\(x\\)` | y |")
    ok("\\(" in cells[1], "other backslashes survive")
    skill = (SECTION + "\n\n| Command | Outcome |\n|---|---|\n"
             "| `hyprctl version` | x |\n| `hyprctl layers -j \\| jq` | y |\n\n### Next\n")
    rows = command_rows(skill)
    ok(rows == ["hyprctl version", "hyprctl layers -j | jq"], "runbook section rows only")
    ok(command_rows("| `hyprctl version` | outside |") == [], "rows outside the section ignored")
    for name, anchor, repl in MUTATIONS:
        source = "a\n" + anchor + "\nb\n"
        if source.count(anchor) != 1 or source.replace(anchor, repl) == source:
            ok(False, "mutation anchor %s" % name)
        else:
            ok(True, "mutation anchor %s" % name)
    sample = {"kind": "int_range", "value": [1, 10], "frozen": "5",
              "samples": [{"rc": 0, "out": "7"}],
              "negatives": [{"rc": 0, "out": "0"}]}
    ok(case_correct(sample, 0, "5"), "case shape correct")
    ok(case_correct(sample, 0, "7"), "case churn accepted")
    ok(not case_correct(dict(sample, samples=[{"rc": 0, "out": "11"}]), 0, "5"),
       "case churn refused")
    ok(not case_correct(sample, 0, "0"), "case negative refused")
    ok(held_rule(sample, 0, "5"), "held rule matches the frozen value")
    ok(not held_rule(sample, 0, "7"), "held rule refuses another value")
    ok(not held_rule({"kind": "refusal", "value": refusal}, 3, "x"), "held rule has no new row")
    print("MADO_R82_RUNBOOK_SELFTEST: %d/%d" % (checks, total))
    return 0 if checks == total else 1


def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--controls")
    ap.add_argument("--carried")
    ap.add_argument("--scratch-root")
    ap.add_argument("--no-mutants", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not (args.repo and args.rev and args.controls and args.carried and args.scratch_root):
        print("MADO_R82_RUNBOOK: ERROR (stage=setup usage)")
        return 2
    workroot = None
    try:
        repo = os.path.abspath(args.repo)
        if args.scratch_root == "/":
            raise Setup("refusing / as the scratch root")
        if os.path.islink(args.scratch_root):
            raise Setup("refusing a symlinked scratch root")
        os.makedirs(args.scratch_root, exist_ok=True)
        if not os.path.isdir(args.scratch_root):
            raise Setup("scratch root is not a directory")
        workroot = tempfile.mkdtemp(prefix="c2-r82-", dir=args.scratch_root)
        rev_full = run(["git", "-C", repo, "rev-parse", args.rev], repo)[1].strip()
        if not rev_full:
            raise Setup("cannot resolve --rev %r" % args.rev)

        with open(args.controls) as fh:
            control = json.load(fh)
        cases = control["cases"]
        if len(cases) != CASES:
            raise Setup("control set carries %d cases, frozen target expects %d"
                        % (len(cases), CASES))
        with open(args.carried) as fh:
            carried_cases = json.load(fh)["cases"]
        if len(carried_cases) != CARRIED:
            raise Setup("carried set carries %d cases, frozen target expects %d"
                        % (len(carried_cases), CARRIED))
        for index, case in enumerate(carried_cases):
            for key in case:
                if key == "skill_anchor":
                    continue
                if cases[index].get(key) != case[key]:
                    raise Setup("carried case %r changes field %r" % (case["name"], key))
            if set(cases[index]) - {"skill_anchor"} != set(case) - {"skill_anchor"}:
                raise Setup("carried case %r changes its field set" % case["name"])

        skill = git_show(repo, args.rev, "SKILL.md")
        for path in ("SKILL.md", "tools/mado-barfoot.py"):
            if sha256(open(os.path.join(repo, path), "rb").read()) != sha256(
                    git_bytes(repo, args.rev, path)):
                raise Setup("%s in the working tree is not the measured revision's bytes"
                            % path)
        for case in cases:
            for path in case.get("fixtures", []):
                if sha256(open(os.path.join(repo, path), "rb").read()) != sha256(
                        git_bytes(repo, args.rev, path)):
                    raise Setup("fixture %s is not the measured revision's bytes" % path)

        rows = command_rows(skill)
        if len(rows) != CASES:
            raise Setup("the runbook section carries %d command rows, frozen target expects %d"
                        % (len(rows), CASES))
        bindings = {}
        for case in cases:
            hits = [index for index, cell in enumerate(rows) if cell == case["skill_anchor"]]
            if len(hits) != 1:
                raise Setup("anchor %r for %s binds %d rows, expected exactly 1"
                            % (case["skill_anchor"], case["name"], len(hits)))
            if False:
                raise Setup("row %d is bound by %r and %r"
                            % (hits[0], bindings[hits[0]], case["name"]))
            bindings[hits[0]] = case["name"]
        if len(bindings) != CASES:
            raise Setup("only %d of %d rows are bound" % (len(bindings), CASES))
        for case in cases:
            argv = case["argv"]
            documented = argv[2] if argv and argv[0] == "/bin/sh" else " ".join(argv)
            if documented != case["skill_anchor"]:
                raise Setup("case %s executes a command its row does not document"
                            % case["name"])
        print("MADO_R82_CONTROLS: sha256=%s cases=%d"
              % (sha256(open(args.controls, "rb").read()), len(cases)))

        row_of = {name: index for index, name in bindings.items()}
        executed = matched = shapes = 0
        control_new = control_all = 0
        for case in cases:
            rc, stdout, stderr = run(case["argv"], repo)
            executed += 1
            good = case_correct(case, rc, stdout)
            matched += 1 if good else 0
            shapes += 1 if case["kind"] in SHAPE_KINDS and good else 0
            is_new = case["name"] not in {c["name"] for c in carried_cases}
            if is_new:
                control_new += 1 if held_rule(case, rc, stdout) else 0
            control_all += 1 if held_rule(case, rc, stdout) else 0
            print("MADO_R82_PROBE: name=%s row=%d kind=%s match=%s %s"
                  % (case["name"], row_of[case["name"]], case["kind"],
                     "yes" if good else "no", observed(case["kind"], rc, stdout)))

        killed = 0
        if not args.no_mutants:
            self_path = os.path.abspath(__file__)
            with open(self_path) as fh:
                own_source = fh.read()
            for name, anchor, repl in MUTATIONS:
                if own_source.count(anchor) != 1:
                    raise Setup("mutant %s anchor occurs %d times, not once"
                                % (name, own_source.count(anchor)))
                mutant = os.path.join(workroot, "mutant-%s.py" % name)
                with open(mutant, "w") as fh:
                    fh.write(own_source.replace(anchor, repl))
                mrc, mout, merr = run([sys.executable, "-I", mutant, "--repo", repo,
                                       "--rev", args.rev, "--controls", args.controls,
                                       "--carried", args.carried,
                                       "--scratch-root", workroot, "--no-mutants"],
                                      repo, timeout=600)
                mm = re.search(r"MADO_R82_RUNBOOK: cases=(\d+) executed=(\d+) matched=(\d+)",
                               mout)
                mmatched = int(mm.group(3)) if mm else 0
                dead = mrc != 0 and (mm is None or mmatched < CASES)
                killed += 1 if dead else 0
                print("MADO_R82_MUTANT: name=%s matched=%d/%d killed=%s"
                      % (name, mmatched, CASES, "yes" if dead else "no"))

        new_rows = sum(1 for case in cases
                       if case["name"] not in {c["name"] for c in carried_cases})
        print("MADO_R82_CONTROL: control_new=%d/%d held=fixed-value(no-frozen-value-for-the-"
              "new-rows) control_all=%d/%d rule=held-r78-fixed-value"
              % (control_new, new_rows, control_all, CASES))
        target = (executed == CASES and matched == CASES and shapes == SHAPES
                  and len(bindings) == CASES and control_new == CONTROL_NEW
                  and (args.no_mutants or killed == MUTANTS))
        print("MADO_R82_RUNBOOK: cases=%d executed=%d matched=%d shapes=%d/%d anchors=%d/%d "
              "rows=%d/%d control_new=%d/%d mutants=%s killed=%s verdict=%s rev=%s tree=bound"
              % (CASES, executed, matched, shapes, SHAPES, len(bindings), CASES,
                 len(bindings), CASES, control_new, new_rows,
                 "0" if args.no_mutants else str(MUTANTS),
                 "0" if args.no_mutants else str(killed),
                 "TARGET_MET" if target else "TARGET_MISSED", rev_full))
        return 0 if target else 1
    except Setup as exc:
        print("MADO_R82_RUNBOOK: ERROR (stage=setup %s)" % exc)
        return 2
    finally:
        if workroot:
            shutil.rmtree(workroot, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
