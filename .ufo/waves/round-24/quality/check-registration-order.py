#!/usr/bin/env python3
"""Round-24 quality check: registration order for a lane round (M23-4, M23-7).

Usage:
    python3 -I check-registration-order.py --round N [--repo PATH]
                                           [--base REV] [--tip REV] [--json]

Reads only git history (git log, rev-list, diff-tree, show) with
GIT_OPTIONAL_LOCKS=0; it never writes to the repository.

Rule (LANE ROUND):
  exit 1 if any commit changing tools/ precedes the first commit that adds a
  registered discovery/attack population for the round; exit 0 otherwise;
  exit 2 when the history cannot be evaluated.

Definitions, in the order the checker applies them.

Round window
  Commits in BASE..TIP, ordered by `git rev-list --reverse --topo-order`.
  When BASE is omitted, the window starts at the parent of the oldest commit
  reachable from TIP whose subject starts with `round-N` (a word boundary, so
  `round-23 verifier spot-check` belongs to round 23); TIP defaults to HEAD.
  When the oldest round-named commit is the root commit, the window is the
  whole history reachable from TIP (constructed histories). When no commit
  names the round, an explicit --base is required and the checker exits 2
  without one, so a mistyped round number cannot silently scan all history.
  Explicit --base/--tip override the inference.

tools/ change
  A commit whose diff against its first parent adds, modifies, deletes or
  renames any path under `tools/`.

Registered discovery/attack population
  A commit that adds, under `.ufo/waves/round-N/`, at least one discovery or
  attack case and the registration that names it:
    - attack fixture: a `.jsonl`/`.json` case under a path segment containing
      `attack` (case-insensitive), e.g.
      `.ufo/waves/round-23/w2/out/AttackLateCell/fixtures/*.jsonl`;
    - carry/ or frozen/ population: case files (`.jsonl` anywhere under the
      population directory, or `.json` under a fixtures/cases/inputs segment)
      plus a manifest
      (`manifest*`, `expected*`, `registration*`, `readme*` with a
      .json/.md/.txt suffix) added in the same commit under the same
      population directory; the lane convention (round-24 registration section
      6) is that carry/ holds the round's registered discovery population;
    - repair/ population: same case+manifest requirement, and the manifest
      must itself declare the population as discovery or attack (the words
      `discovery` or `attack`). A repair-target set is not an independent
      discovery population: round-23 `repair/expected.json` declares
      `schema: mado-r23-repair-set-v1` and names neither word, so it does not
      satisfy this arm.
  A marker directory counts only at the first or second path segment under the
  round (`.ufo/waves/round-N/frozen/...` or `.ufo/waves/round-N/tripwire/
  frozen/...`), and paths that nest another wave tree (a `snapshot` segment or
  a `.ufo` segment below the round root) are ignored: copied trees are not the
  round's own registered population. Case files are `.jsonl`/`.json` (the
  fixture form used by rounds 22-24).

Comparison
  Violation iff the earliest tools/ commit strictly precedes the earliest
  population commit, or a tools/ commit exists and no population commit does.
  A population that lands in the same commit as the earliest tools/ change
  does not strictly precede it; the checker passes it with a note.

Exit codes: 0 pass, 1 violation, 2 cannot evaluate.
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

CASE_EXTS = {".jsonl", ".json"}
MANIFEST_RE = re.compile(r"(?i)^(manifest|expected|registration|readme)([._-].*)?\.(json|md|txt)$")
MARKERS = ("carry", "frozen", "repair")
DISCOVERY_WORDS = re.compile(r"(?i)\b(discovery|attack)")


def git(repo, *args):
    env = dict(os.environ)
    env["GIT_OPTIONAL_LOCKS"] = "0"
    proc = subprocess.run(
        ["git", "-C", str(repo), "--no-pager", *args],
        capture_output=True, text=True, env=env,
    )
    if proc.returncode != 0:
        raise RuntimeError("git " + " ".join(args) + " failed: " + proc.stderr.strip())
    return proc.stdout


def infer_round(repo, rev, round_no):
    """(found, base-or-None, newest matching commit) on the first-parent chain.

    base is None when the oldest round-named commit is the root commit: the
    whole reachable history is then the round's window."""
    out = git(repo, "log", "--first-parent", "-n", "20000",
              "--format=%H%x1f%P%x1f%cI%x1f%s", rev)
    rows = []
    for line in out.splitlines():
        if not line:
            continue
        sha, parents, cdate, subject = line.split("\x1f", 3)
        rows.append({"sha": sha, "parents": parents.split(), "date": cdate, "subject": subject})
    pattern = re.compile(r"^round-%d(?!\d)" % round_no)
    hits = [r for r in rows if pattern.match(r["subject"])]
    if not hits:
        return False, None, None
    newest = hits[0]
    oldest = hits[-1]
    base = oldest["parents"][0] if oldest["parents"] else None
    return True, base, newest["sha"]


def window_commits(repo, base, tip):
    rng = "%s..%s" % (base, tip) if base else tip
    out = git(repo, "rev-list", "--reverse", "--topo-order", rng)
    return [line.strip() for line in out.splitlines() if line.strip()]


def commit_meta(repo, sha):
    out = git(repo, "show", "-s", "--format=%cI%x1f%s", sha).strip()
    cdate, subject = out.split("\x1f", 1)
    return cdate, subject


def changed_paths(repo, sha):
    """[(status, path)] for the diff against the first parent (or root)."""
    out = git(repo, "diff-tree", "--no-commit-id", "--name-status", "-r", "-M", "--root", sha)
    rows = []
    for line in out.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        status, paths = parts[0], parts[1:]
        for p in paths:
            rows.append((status, p))
    return rows


def file_at(repo, sha, path):
    return git(repo, "show", "%s:%s" % (sha, path))


def population_evidence(repo, sha, round_no, changes):
    """([(kind, [paths])], [rejected population notes]) for this commit."""
    root = ".ufo/waves/round-%d/" % round_no
    attack = []
    dirs = {}
    for status, path in changes:
        if not status.startswith("A") or not path.startswith(root):
            continue
        rel = path[len(root):]
        segs = rel.split("/")
        if "snapshot" in segs or ".ufo" in segs:
            continue
        name = segs[-1]
        ext = os.path.splitext(name)[1].lower()
        is_attack = any("attack" in s.lower() for s in segs[:-1])
        if is_attack and (ext == ".jsonl" or (ext == ".json" and
                          any(s.lower() == "fixtures" for s in segs[:-1]))):
            attack.append(path)
            continue
        for i, seg in enumerate(segs[:2]):
            if seg in MARKERS:
                key = (seg, "/".join(segs[: i + 1]))
                slot = dirs.setdefault(key, {"cases": [], "manifests": []})
                if MANIFEST_RE.match(name):
                    slot["manifests"].append(path)
                elif ext == ".jsonl" or (ext == ".json" and any(
                        s.lower() in ("fixtures", "cases", "inputs") for s in segs[:-1])):
                    slot["cases"].append(path)
                break
    out = []
    rejected = []
    for (marker, sub), slot in sorted(dirs.items()):
        if not slot["manifests"] or not slot["cases"]:
            rejected.append({"kind": marker, "dir": root + sub,
                             "reason": "case files and a manifest were not both added"})
            continue
        if marker == "repair":
            declared = "".join(file_at(repo, sha, m) for m in slot["manifests"])
            if not DISCOVERY_WORDS.search(declared):
                rejected.append({"kind": marker, "dir": root + sub,
                                 "reason": "manifest declares a repair set, not a "
                                           "discovery/attack population"})
                continue
        out.append((marker, slot["cases"] + slot["manifests"]))
    if attack:
        out.append(("attack-fixture", sorted(attack)))
    return out, rejected


def evaluate(repo, round_no, base, tip):
    meta = {"round": round_no, "repo": str(repo), "base": base, "tip": tip}
    if base is None:
        found, inferred_base, inferred_tip = infer_round(repo, tip or "HEAD", round_no)
        if not found:
            meta["error"] = ("no commit naming round-%d is reachable from %s; "
                             "pass --base" % (round_no, tip or "HEAD"))
            return 2, meta
        base = inferred_base
        meta["base"] = base
        meta["base_inferred"] = "commit" if base else "root"
        if tip is None:
            tip = inferred_tip
            meta["tip_inferred"] = inferred_tip
    if tip is None:
        tip = "HEAD"
    meta["tip"] = tip
    commits = window_commits(repo, base, tip)
    meta["window"] = "%s..%s" % (base or "(root)", tip)
    meta["commits"] = len(commits)

    first_tools = None
    first_pop = None
    pop_hits = []
    tools_hits = []
    ignored = []
    for index, sha in enumerate(commits):
        paths = changed_paths(repo, sha)
        tool_paths = sorted({p for status, p in paths if p.startswith("tools/")})
        if tool_paths and first_tools is None:
            cdate, subject = commit_meta(repo, sha)
            first_tools = {"sha": sha, "index": index, "date": cdate,
                           "subject": subject, "paths": tool_paths[:12],
                           "paths_total": len(tool_paths)}
        elif tool_paths:
            tools_hits.append(sha)
        pops, rejected = population_evidence(repo, sha, round_no, paths)
        for note in rejected:
            ignored.append(dict(note, sha=sha))
        if pops:
            cdate, subject = commit_meta(repo, sha)
            entry = {"sha": sha, "index": index, "date": cdate, "subject": subject,
                     "kind": pops[0][0],
                     "paths": sorted({p for _, ps in pops for p in ps})[:12],
                     "paths_total": len({p for _, ps in pops for p in ps})}
            pop_hits.append(entry)
            if first_pop is None:
                first_pop = entry

    meta["first_tools"] = first_tools
    meta["first_population"] = first_pop
    meta["later_populations"] = [h["sha"] for h in pop_hits[1:]]
    meta["later_tools"] = tools_hits
    meta["ignored_populations"] = ignored

    if first_tools is None:
        meta["verdict"] = "GREEN"
        meta["reason"] = "no commit in the window changes tools/"
        return 0, meta
    if first_pop is None:
        meta["verdict"] = "RED"
        meta["reason"] = ("tools/ changed at %s but no commit in the window adds a "
                          "registered discovery/attack population" % first_tools["sha"])
        return 1, meta
    if first_pop["index"] < first_tools["index"]:
        meta["verdict"] = "GREEN"
        meta["reason"] = ("first registered discovery/attack population %s precedes the "
                          "first tools/ change %s" % (first_pop["sha"], first_tools["sha"]))
        return 0, meta
    if first_tools["index"] < first_pop["index"]:
        meta["verdict"] = "RED"
        meta["reason"] = ("first tools/ change %s precedes the first registered "
                          "discovery/attack population %s (%s)"
                          % (first_tools["sha"], first_pop["sha"], first_pop["kind"]))
        return 1, meta
    meta["verdict"] = "GREEN"
    meta["reason"] = ("population %s and the earliest tools/ change land in the same "
                      "commit; neither strictly precedes the other" % first_pop["sha"])
    return 0, meta


def emit(meta, as_json):
    if as_json:
        print(json.dumps(meta, indent=2, sort_keys=True))
        return
    if "error" in meta:
        print("round=%s error=%s" % (meta["round"], meta["error"]))
        return
    print("round=%s repo=%s" % (meta["round"], meta["repo"]))
    print("window=%s commits=%d" % (meta["window"], meta["commits"]))
    tools = meta["first_tools"]
    if tools:
        print("first-tools-change=%s %s %r paths=%s%s"
              % (tools["sha"], tools["date"], tools["subject"],
                 ",".join(tools["paths"]),
                 "" if tools["paths_total"] <= len(tools["paths"])
                 else " (+%d more)" % (tools["paths_total"] - len(tools["paths"]))))
    else:
        print("first-tools-change=none")
    pop = meta["first_population"]
    if pop:
        print("first-registered-discovery-attack-population=%s %s %r kind=%s paths=%s%s"
              % (pop["sha"], pop["date"], pop["subject"], pop["kind"],
                 ",".join(pop["paths"]),
                 "" if pop["paths_total"] <= len(pop["paths"])
                 else " (+%d more)" % (pop["paths_total"] - len(pop["paths"]))))
    else:
        print("first-registered-discovery-attack-population=none")
    if meta["later_tools"]:
        print("later-tools-changes=%s" % ",".join(meta["later_tools"]))
    if meta["later_populations"]:
        print("later-populations=%s" % ",".join(meta["later_populations"]))
    for note in meta.get("ignored_populations", []):
        print("ignored-population=%s kind=%s dir=%s reason=%s"
              % (note["sha"], note["kind"], note["dir"], note["reason"]))
    print("verdict=%s reason=%s" % (meta["verdict"], meta["reason"]))


def main(argv):
    parser = argparse.ArgumentParser(
        description="exit 1 when a round's tools/ change precedes its first "
                    "registered discovery/attack population")
    parser.add_argument("--round", type=int, required=True, dest="round_no")
    parser.add_argument("--repo", default=str(Path(__file__).resolve().parents[4]))
    parser.add_argument("--base", default=None)
    parser.add_argument("--tip", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    repo = Path(args.repo).resolve()
    try:
        git(repo, "rev-parse", "--git-dir")
    except (RuntimeError, FileNotFoundError) as exc:
        print(json.dumps({"error": str(exc)}) if args.json
              else "error: %s" % exc)
        return 2
    try:
        code, meta = evaluate(repo, args.round_no, args.base, args.tip)
    except RuntimeError as exc:
        meta = {"round": args.round_no, "repo": str(repo), "error": str(exc)}
        emit(meta, args.json)
        return 2
    emit(meta, args.json)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
