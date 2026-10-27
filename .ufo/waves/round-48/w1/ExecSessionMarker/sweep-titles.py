#!/usr/bin/env python3
"""Classify every R1 title value at a revision against the old and new
namespace. Prints paths and pass/fail only -- never a title value."""
import importlib.util
import subprocess
import sys

repo, rev, gate_path = sys.argv[1], sys.argv[2], sys.argv[3]

spec = importlib.util.spec_from_file_location("gate", gate_path)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

OLD = __import__("re").compile(
    r"^(?:a live window title|another live window title|redacted)$"
    r"|^(?:synthetic|fixture|selftest|probe|example|demo)(?:[ -][A-Za-z0-9 ._-]{0,60})?$",
    __import__("re").IGNORECASE,
)
NEW = gate.SYNTH_TITLE_RE

files = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "--name-only", rev, ".ufo"],
                       stdout=subprocess.PIPE, check=True).stdout.decode().splitlines()
rows = []
for path in files:
    if not path.endswith((".json", ".txt", ".md", ".py", ".jsonl")):
        continue
    blob = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, path)],
                          stdout=subprocess.PIPE).stdout
    if b"\x00" in blob[:8192]:
        continue
    text = blob.decode("utf-8", "replace")
    if '"class"' not in text:
        continue
    values = gate.matched_values(gate.R1, text)
    if not values:
        continue
    old_ok = all(OLD.match(v.strip()) for _k, v in values)
    new_ok = all(NEW.match(v.strip()) for _k, v in values)
    rows.append((path, len(values), old_ok, new_ok))

print("TITLE_SWEEP files_with_r1=%d values=%d" % (len(rows), sum(r[1] for r in rows)))
print("TITLE_SWEEP old_pass=%d new_pass=%d lost=%d"
      % (sum(1 for r in rows if r[2]), sum(1 for r in rows if r[3]),
         sum(1 for r in rows if r[2] and not r[3])))
for path, _n, old_ok, new_ok in rows:
    if old_ok and not new_ok:
        print("LOST %s" % path)
    elif not old_ok and new_ok:
        print("GAINED %s" % path)
