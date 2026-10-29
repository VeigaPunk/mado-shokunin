#!/usr/bin/env python3
"""Build the per-mutant table for mutants.md from the receipts (merged-results.json, candidate-verify.json).

Classification of each survivor (see mutants.md section 4 for the arguments):
  EQUIVALENT      - argued unreachable / identical behaviour on Python 3.14.8 (no fixture can kill it)
  ROOT-LEVEL      - non-equivalent, needs a config file at a root-level path (cannot be staged); killed by the bwrap probe
  KILLED-BY-K##   - non-equivalent survivor; the candidate fixture K## kills it through the staged C2 harness path
"""
import json
import sys

EQUIV = {
    "m06": "`absolute_path` is only reached with `home=None` for a non-`~` raw; `source()` rejects `~` without --home first, and matched paths are absolute",
    "m15": "`os.stat(target)` never sees a NUL: targets are `glob` results, and `glob` returns [] for any NUL-bearing pattern (probed)",
    "m19": "CPython 3.13+ `realpath(strict=True)` raises OSError (ELOOP) on a loop, never RuntimeError (probed on 3.14.8)",
    "m77": "`glob.glob(pattern, recursive=False)` is the default; the mutant is the same call",
    "m82": "`glob` results start with `/` (the pattern is absolute), so `absolute_path(match)` is the identity",
    "m97": "`live_value(b\"\")` returns None, the same value the `None` branch gives",
    "m102": "`value` is produced by `config_int` and is only digits, so it never contains a space",
    "m104": "the unstripped RHS is only read by a `\"##\" in rhs` test (strip-invariant) and by two later `.strip(WS)` calls",
    "m108": "a line that holds `$`, `{` or a backslash only in its LHS fails the key test first: the only key that matters is `misc:disable_autoreload` (or `disable_autoreload` under `misc {`), which has none of those characters",
    "m116": "`value.strip(\"0\") != \"\"` is exactly the truthiness of that string",
}
ROOTLEVEL = {
    "m75": "`curdir` bound for a root-level cur (`/hyprland.conf`): pristine gives `/a.conf`, mutant `/hyprland.conf/a.conf`",
    "m76": "`../` bound for a cur whose directory is one level deep (`/sub/x.conf`): pristine gives `/a.conf`, mutant `/sub/a.conf`",
}


def main(merged_path, verify_path, out_path):
    merged = json.load(open(merged_path))
    ver = json.load(open(verify_path))
    kill_by = {}
    for r in ver:
        if r.get("verdict") == "KILLED":
            kill_by.setdefault(r["mutant"], []).append(r["fixture"])
    lines = ["| id | area | oracle (orig) | mutated line: old -> new | note | final status |",
             "|---|---|---|---|---|---|"]
    counts = {"killed_orig": 0, "surv_eq": 0, "surv_root": 0, "surv_k": 0, "surv_unkilled": 0}
    for r in merged:
        mid = r["id"]
        if r["verdict"] == "KILLED":
            oracle = []
            if r.get("selftest_rc") != 0:
                oracle.append("selftest")
            if not r.get("harness_ok"):
                oracle.append("fixtures %d/26" % r.get("fixtures_passed", 0))
            status = "killed by " + " + ".join(oracle)
            counts["killed_orig"] += 1
        else:
            oracle = "survived (selftest ok, 26/26)"
            if mid in EQUIV:
                status = "SURVIVED - EQUIVALENT: " + EQUIV[mid]
                counts["surv_eq"] += 1
            elif mid in ROOTLEVEL:
                status = "SURVIVED - non-equivalent, ROOT-LEVEL: " + ROOTLEVEL[mid] + " (killed by bwrap probe, root-level-probe.sh)"
                counts["surv_root"] += 1
            elif mid in kill_by:
                status = "SURVIVED - non-equivalent: KILLED-BY " + ",".join(kill_by[mid]) + " (verified via harness path)"
                counts["surv_k"] += 1
            else:
                status = "SURVIVED - non-equivalent: NO KILL FOUND"
                counts["surv_unkilled"] += 1
        old = r.get("old", "").strip().replace("|", "\\|").replace("\n", " / ")
        new = r.get("new", "").strip().replace("|", "\\|").replace("\n", " / ")
        lines.append("| %s | %s | %s | `%s` -> `%s` | %s | %s |" % (
            mid, r.get("area", ""), oracle if isinstance(oracle, str) else "; ".join(oracle),
            old, new, r.get("note", "").replace("|", "\\|"), status))
    open(out_path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(json.dumps(counts, sort_keys=True))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
