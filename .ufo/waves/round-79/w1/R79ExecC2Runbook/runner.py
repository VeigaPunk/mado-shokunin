#!/usr/bin/env python3
"""R79ExecC2Runbook — independent C2 runbook execution audit (own parser, no counter).

1. Parse SKILL.md `### Executable runbook rows (round 79)` with an own cell splitter
   that handles `\|`, and record each row's line number.
2. Check binding direction: every row claimed by exactly one case (equality), every
   case's skill_anchor equal to its row's unescaped command cell; report strict-prefix
   ambiguities.
3. Execute every row verbatim from the lane root and score it against the case's own
   committed expectation; compare case by case with the frozen counter receipt.
4. Independently hash the tree-bound files against the measured revision blobs.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
SCRATCH = "/fast/scratch/hyaku/mado-r79/R79ExecC2Runbook"
CONTROLS = os.path.join(LANE, ".ufo/waves/round-79/controls/c2-runbook-cases-r79.json")
CARRIED = os.path.join(LANE, ".ufo/waves/round-78/controls/c2-runbook-cases-r78.json")
RECEIPT = os.path.join(LANE, ".ufo/waves/round-79/receipts/measurement-c2-r79.txt")
SECTION = "### Executable runbook rows (round 79)"
REV = "5eb8f20fe291603c74973fa94cc55723ac8089a4"

SHAPE_KINDS = ("json_object_fields", "array_fields", "int4", "levels_dump", "int_range",
               "sorted_unique", "regex", "refusal", "lines_shape")


def split_cells(line):
    """Markdown table row split on unescaped pipes; \\| becomes a literal pipe."""
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
    """[(cell, lineno)] of the runbook section's command cells, in row order."""
    rows, inside = [], False
    for lineno, line in enumerate(skill.splitlines(), 1):
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
            continue
        rows.append((cell, lineno))
    return rows


def build_env():
    env = dict(os.environ)
    env["LC_ALL"] = "C"
    env["LANG"] = "C"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
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
    return env


def run(argv, cwd, env, timeout=120):
    proc = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, stdin=subprocess.DEVNULL,
                          timeout=timeout)
    return proc.returncode, proc.stdout.decode("utf-8", "replace")


def json_text(text):
    try:
        return json.loads(text)
    except (ValueError, TypeError):
        return None


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
    raise SystemExit("unknown field type %r" % kind)


def fields_ok(item, schema):
    if not isinstance(item, dict):
        return False
    for key, kind in schema.get("fields", {}).items():
        if key not in item or not type_ok(item[key], kind):
            return False
    return True


def matches(kind, value, rc, stdout):
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
    if kind == "int_range":
        lo, hi = value
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
        return fields_ok(json_text(text), value)
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
    raise SystemExit("unknown expectation kind %r" % kind)


def refusal_matches(kind, value, rc, stdout):
    if kind != "refusal":
        return matches(kind, value, rc, stdout)
    return rc == value["rc"] and ("ERROR (stage=%s " % value.get("stage", "model")) in stdout


def case_correct(case, rc, stdout):
    def okay(r, out):
        return refusal_matches(case["kind"], case["value"], r, out)
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
    """Receipt-style masking: never quote a JSON dump (serials/descriptions)."""
    if kind in ("json_object_fields", "array_fields", "int4", "levels_dump"):
        return "rc=%d json-bytes=%d" % (rc, len(stdout))
    text = stdout.rstrip("\n")
    if kind == "lines_shape":
        lines = text.splitlines()
        return "rc=%d lines=%d" % (rc, len(lines))
    if len(text) > 100:
        text = text[:97] + "..."
    return "rc=%d out=%r" % (rc, text)


def sha256_file(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    env = build_env()
    report = {"rev": REV}

    with open(os.path.join(LANE, "SKILL.md"), encoding="utf-8") as fh:
        skill = fh.read()
    rows = command_rows(skill)
    report["section_found"] = SECTION in skill
    report["row_count"] = len(rows)
    report["rows"] = [{"lineno": ln, "cell": cell} for cell, ln in rows]

    with open(CONTROLS, encoding="utf-8") as fh:
        control = json.load(fh)
    cases = control["cases"]
    report["case_count"] = len(cases)

    # --- binding direction: equality, exactly one case per row, one row per case
    binding = []
    for case in cases:
        hits = [i for i, (cell, _) in enumerate(rows) if cell == case["skill_anchor"]]
        binding.append({"name": case["name"], "anchor_rows": hits,
                        "anchor_equals_argv": case["skill_anchor"] == " ".join(case["argv"])
                        if case["argv"][0] != "/bin/sh" else
                        case["skill_anchor"] == case["argv"][2]})
    report["binding"] = binding
    report["every_row_bound"] = sorted({h["anchor_rows"][0] for h in binding
                                       if len(h["anchor_rows"]) == 1}) == list(range(len(rows)))
    report["all_single_bind"] = all(len(h["anchor_rows"]) == 1 for h in binding)
    report["all_anchor_equals_cell"] = all(len(h["anchor_rows"]) == 1 and
                                           rows[h["anchor_rows"][0]][0] == next(
                                               c["skill_anchor"] for c in cases
                                               if c["name"] == h["name"])
                                           for h in binding)

    # --- strict-prefix ambiguity between row cells (equality-bound, so advisory)
    prefixes = []
    for i, (a, _) in enumerate(rows):
        for j, (b, _) in enumerate(rows):
            if i != j and b.startswith(a) and b != a:
                prefixes.append({"shorter_row": i, "longer_row": j,
                                 "shorter": a[:60], "longer": b[:60]})
    report["prefix_ambiguities"] = prefixes

    # --- carried-field freeze check (independent re-derivation)
    with open(CARRIED, encoding="utf-8") as fh:
        carried_cases = json.load(fh)["cases"]
    drift = []
    for index, case in enumerate(carried_cases):
        for key in case:
            if key == "skill_anchor":
                continue
            if cases[index].get(key) != case[key]:
                drift.append({"index": index, "name": case["name"], "field": key})
        if set(cases[index]) - {"skill_anchor"} != set(case) - {"skill_anchor"}:
            drift.append({"index": index, "name": case["name"], "field": "<field-set>"})
    report["carried_field_drift"] = drift
    report["carried_names"] = [c["name"] for c in carried_cases]

    # --- execute every row verbatim from the lane root
    live = []
    for case in cases:
        cell, lineno = rows[binding[[b["name"] for b in binding].index(case["name"])]
                            ["anchor_rows"][0]]
        argv = ["/bin/sh", "-c", cell]
        rc, stdout = run(argv, LANE, env)
        good = case_correct(case, rc, stdout)
        live.append({"name": case["name"], "row": rows.index((cell, lineno)),
                     "lineno": lineno, "kind": case["kind"],
                     "match": good, "observed": observed(case["kind"], rc, stdout)})
    report["live"] = live

    # --- compare with the frozen counter receipt, case by case
    receipt = {}
    with open(RECEIPT, encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r"MADO_R79_PROBE: name=(\S+) row=(\d+) kind=(\S+) match=(yes|no) (.*)$",
                         line.rstrip("\n"))
            if m:
                receipt[m.group(1)] = {"row": int(m.group(2)), "kind": m.group(3),
                                       "match": m.group(4) == "yes", "rest": m.group(5)}
    cmp_rows = []
    for entry in live:
        r = receipt.get(entry["name"])
        cmp_rows.append({
            "name": entry["name"],
            "row_agrees": bool(r) and r["row"] == entry["row"],
            "kind_agrees": bool(r) and r["kind"] == entry["kind"],
            "match_agrees": bool(r) and r["match"] == entry["match"],
            "observed_equal": bool(r) and r["rest"] == entry["observed"],
            "mine": entry["observed"], "receipt": r["rest"] if r else None})
    report["receipt_comparison"] = cmp_rows
    report["receipt_runbook_line"] = [ln.rstrip("\n") for ln in open(RECEIPT, encoding="utf-8")
                                      if ln.startswith("MADO_R79_RUNBOOK:")][0]

    # --- independent tree-bound hashing (working tree vs measured rev blobs)
    tree = {}
    for path in ("SKILL.md", "tools/mado-barfoot.py"):
        blob = subprocess.run(["git", "-C", LANE, "show", REV + ":" + path],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        tree[path] = {"work": sha256_file(os.path.join(LANE, path)),
                      "rev": hashlib.sha256(blob.stdout).hexdigest(),
                      "equal": sha256_file(os.path.join(LANE, path)) ==
                      hashlib.sha256(blob.stdout).hexdigest()}
    fixture_paths = sorted({p for c in cases for p in c.get("fixtures", [])})
    tree["_fixture_count"] = len(fixture_paths)
    tree["_fixtures_all_equal"] = True
    for path in fixture_paths:
        blob = subprocess.run(["git", "-C", LANE, "show", REV + ":" + path],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        eq = sha256_file(os.path.join(LANE, path)) == hashlib.sha256(blob.stdout).hexdigest()
        tree["_fixtures_all_equal"] = tree["_fixtures_all_equal"] and eq
        if not eq:
            tree.setdefault("_fixtures_unequal", []).append(path)
    report["tree_hashes"] = tree

    with open(os.path.join(SCRATCH, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1, ensure_ascii=False)

    print("rows=%d cases=%d single_bind=%s every_row_bound=%s anchor==cell=%s "
          "carried_drift=%d prefix_pairs=%d"
          % (report["row_count"], report["case_count"], report["all_single_bind"],
             report["every_row_bound"], report["all_anchor_equals_cell"],
             len(drift), len(prefixes)))
    for entry in live:
        print("LIVE: name=%s row=%d kind=%s match=%s %s"
              % (entry["name"], entry["row"], entry["kind"],
                 "yes" if entry["match"] else "no", entry["observed"]))
    mismatches = [c for c in cmp_rows
                  if not (c["row_agrees"] and c["kind_agrees"] and c["match_agrees"])]
    print("receipt: probes=%d row/kind/match disagreements=%d observed_string_diffs=%d"
          % (len(cmp_rows), len(mismatches),
             sum(1 for c in cmp_rows if not c["observed_equal"])))
    for c in cmp_rows:
        if not c["observed_equal"]:
            print("OBS-DIFF: name=%s mine=%s receipt=%s" % (c["name"], c["mine"], c["receipt"]))
    print("tree: %s" % json.dumps({k: v for k, v in tree.items()
                                   if not k.startswith("_")}, sort_keys=True))
    print("fixtures_all_equal=%s fixture_count=%d"
          % (tree["_fixtures_all_equal"], tree["_fixture_count"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
