#!/usr/bin/env python3
"""c1-r52-ledger.py — candidate counter implementing the frozen C1-r52 predicates.

Checks, as literally named in .ufo/waves/round-52/registration.md:
  1. population row uniqueness (one row per population path, no duplicate paths)
  2. resolvable evidence pointer (a pointer path exists at the revision)
  3. non-self pointer (pointer path differs from the ledger path)
  4. description containing instrument-specific functional context
     (implementation: non-placeholder, unique description, >=6 words,
      >=1 activity verb, >=2 description tokens present in the instrument bytes)

Verdict TARGET_MET requires population>0, rows==population, and zero defects.

This is EVIDENCE for a falsification seat: it reproduces the check set the frozen
claim describes, so a no-work ledger can be tested against it. It is not a
delivered lane artifact.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import uuid

LEDGER_REL = "quality/tool-ledger.md"
EMPHASIS = "`*_ \t"
LINE_ANCHOR = re.compile(r":\d+(?:-\d+)?$")
PLACEHOLDER = re.compile(r"^[\s\-–—_*`.]+$")
BACKTICK = re.compile(r"`([^`\n]+)`")
VERBS = {
    "read", "reads", "parse", "parses", "resolve", "resolves", "print", "prints",
    "check", "checks", "run", "runs", "emit", "emits", "join", "joins", "compute",
    "computes", "census", "report", "reports", "verify", "verifies", "audit",
    "audits", "classify", "classifies", "diff", "diffs", "scan", "scans",
    "validate", "validates", "compare", "compares", "walk", "walks",
}
STOP = {
    "the", "and", "for", "with", "from", "that", "this", "into", "over", "only",
    "line", "lines", "when", "then", "than", "each", "per", "via", "one", "two",
}


class SetupError(Exception):
    pass


def git(repo, *args):
    proc = subprocess.run(("git", "-C", repo) + args, capture_output=True)
    if proc.returncode != 0:
        raise SetupError("git %s failed: %s" % (" ".join(args),
                        proc.stderr.decode("utf-8", "replace").strip()[:300]))
    return proc.stdout


def resolve(repo, rev):
    return git(repo, "rev-parse", "--verify", "--quiet", rev + "^{commit}").decode().strip()


def clone_at(repo, rev, work):
    clone = os.path.join(work, "clone-" + uuid.uuid4().hex[:10])
    git(work, "clone", "-q", "--shared", "--no-checkout", repo, clone)
    git(clone, "-c", "advice.detachedHead=false", "checkout", "-q", "--detach", rev)
    top = git(clone, "rev-parse", "--show-toplevel").decode().strip()
    if os.path.realpath(top) != os.path.realpath(clone):
        raise SetupError("clone toplevel mismatch")
    return clone


def population(paths):
    pop = []
    for path in paths:
        if "__pycache__" in path or path.endswith((".pyc", ".pyo")):
            continue
        if path.startswith("tools/"):
            pop.append(path)
            continue
        for root in ("quality/counters/", "quality/"):
            if not path.startswith(root):
                continue
            rest = path[len(root):]
            if rest and "/" not in rest and rest.endswith(".py") and not rest.startswith("."):
                pop.append(path)
            break
    return sorted(set(pop))


def parse_rows(text):
    rows, fenced = [], False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if fenced or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        first = cells[0].strip(EMPHASIS) if cells else ""
        if not first or "/" not in first or first.startswith(":") or set(first) <= set("-: "):
            continue
        rows.append({
            "path": first,
            "desc": cells[1] if len(cells) > 1 else "",
            "pointer": " | ".join(cells[2:]) if len(cells) > 2 else "",
        })
    return rows


def tokens(cell):
    found = BACKTICK.findall(cell)
    if not found:
        found = re.split(r"[,;]|\s+", cell)
    out = []
    for token in found:
        token = token.strip(EMPHASIS)
        token = re.sub(r"^\./", "", token)
        token = LINE_ANCHOR.sub("", token)
        if not token or token.startswith(("/", "~", "$")):
            continue
        if any(ch in token for ch in "<>():#?*\"'"):
            continue
        if "/" not in token and not re.search(r"\.(md|py|sh|json|txt|ya?ml)$", token):
            continue
        out.append(token)
    return out


def words(text):
    return [w for w in re.findall(r"[A-Za-z][A-Za-z0-9_.-]+", text or "")
            if len(w) >= 3]


def describe(rows, files, blobs, ledger_rel, strict_verb=False):
    seen, descs = set(), {}
    counts = {"uncovered": 0, "dangling": 0, "bad_pointer": 0, "self_pointer": 0,
              "no_context": 0, "dup": 0}
    details = []
    pop = population(sorted(files))
    in_pop = set(pop)
    for row in rows:
        path = row["path"]
        if path not in in_pop:
            counts["dangling"] += 1
            details.append("dangling path=%s" % path)
            continue
        if path in seen:
            counts["dup"] += 1
            details.append("dup path=%s" % path)
            continue
        seen.add(path)
        ptr_tokens = tokens(row["pointer"])
        resolved, selfp, bad = False, False, True
        for token in ptr_tokens:
            if token not in files:
                continue
            if token == ledger_rel:
                selfp = True
            if os.path.basename(path).encode() in blobs[token]:
                resolved = True
                bad = False
        if selfp:
            counts["self_pointer"] += 1
            details.append("self_pointer path=%s pointer=%r" % (path, row["pointer"][:80]))
        if not resolved:
            counts["bad_pointer"] += 1
            details.append("bad_pointer path=%s pointer=%r" % (path, row["pointer"][:100]))
        desc = row["desc"].strip(EMPHASIS)
        key = re.sub(r"\s+", " ", desc.lower())
        dup_desc = key in descs
        descs[key] = path
        src = blobs.get(path, b"").lower()
        dw = [w.lower() for w in words(desc)]
        shared = [w for w in dw if w not in STOP and w.encode() in src]
        verb = any(w in VERBS for w in dw)
        if (not desc or PLACEHOLDER.match(desc) or len(dw) < 6 or dup_desc
                or len(set(shared)) < 2 or (strict_verb and not verb)):
            counts["no_context"] += 1
            details.append("no_context path=%s desc=%r shared=%d dup=%s" % (
                path, desc[:70], len(set(shared)), dup_desc))
    missing = sorted(in_pop - seen)
    counts["uncovered"] = len(missing)
    details.extend("uncovered path=%s" % p for p in missing)
    return pop, counts, details


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--ledger", default=LEDGER_REL)
    ap.add_argument("--work", required=True)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--strict-verb", action="store_true")
    args = ap.parse_args(argv)

    work = os.path.abspath(args.work)
    os.makedirs(work, exist_ok=True)
    if args.selftest:
        return selftest(work)

    clone = None
    try:
        repo = os.path.abspath(args.repo)
        rev = resolve(repo, args.rev)
        clone = clone_at(repo, rev, work)
        files = set(git(clone, "ls-tree", "-r", "--name-only", rev)
                    .decode("utf-8", "surrogateescape").splitlines())
        files.discard("")
        if args.ledger not in files:
            print("C1_R52: verdict=TARGET_MISSED ledger=absent rev=%s" % rev)
            return 1
        blobs = {}
        for rel in sorted(files):
            if rel.endswith((".md", ".py", ".sh", ".json", ".txt", ".yml", ".yaml")):
                try:
                    blobs[rel] = git(clone, "show", "%s:%s" % (rev, rel))
                except SetupError:
                    blobs[rel] = b""
        ledger = blobs.get(args.ledger, git(clone, "show", "%s:%s" % (rev, args.ledger)))
        rows = parse_rows(ledger.decode("utf-8", "replace"))
        pop, counts, details = describe(rows, files, blobs, args.ledger, args.strict_verb)
        for line in details:
            print("detail: %s" % line)
        clean = (len(pop) > 0 and len(rows) == len(pop)
                 and not any(counts.values()))
        print("C1_R52: population=%d ledger_rows=%d uncovered=%d dangling=%d "
              "bad_pointer=%d self_pointer=%d no_context=%d dup=%d verdict=%s rev=%s"
              % (len(pop), len(rows), counts["uncovered"], counts["dangling"],
                 counts["bad_pointer"], counts["self_pointer"], counts["no_context"],
                 counts["dup"], "TARGET_MET" if clean else "TARGET_MISSED", rev[:12]))
        return 0 if clean else 1
    except SetupError as exc:
        print("C1_R52: setup=error detail=%s" % exc, file=sys.stderr)
        return 2
    finally:
        if clone and os.path.isdir(clone):
            shutil.rmtree(clone, ignore_errors=True)


def selftest(work):
    """Two inline cases: a laundered no-work ledger (green) and the frozen
    control shape (red). Prints an explicit red/green receipt."""
    green_ledger = "\n".join([
        "| instrument | description | accountability pointer |",
        "|---|---|---|",
        "| `tools/x.py` | Read-only status helper for x.py; reads config bytes and prints one stable line | `quality/inventory.md` |",
    ])
    red_ledger = "\n".join([
        "| Tool | Reads | Writes | Owner and adjacent lanes |",
        "|---|---|---|---|",
        "| tools/x.py | quality/tool-ledger.md (commentary only) | nothing | generic accountability pointer to this ledger itself |",
        "| tools/x.py | quality/tool-ledger.md (commentary only) | nothing | generic accountability pointer to this ledger itself |",
    ])
    files = {"tools/x.py", "quality/inventory.md", "quality/tool-ledger.md"}
    blobs = {"tools/x.py": b"status config bytes prints line", "quality/inventory.md": b"x.py",
             "quality/tool-ledger.md": green_ledger.encode()}
    ok = 0
    pop, counts, _ = describe(parse_rows(green_ledger), files, blobs, "quality/tool-ledger.md")
    if pop and len(parse_rows(green_ledger)) == len(pop) and not any(counts.values()):
        print("selftest green: 4/4 checks pass on the laundered ledger")
        ok += 1
    pop, counts, _ = describe(parse_rows(red_ledger), files, blobs, "quality/tool-ledger.md")
    if any(counts.values()):
        print("selftest red: control shape rejected (%s)" % ", ".join(
            "%s=%d" % (k, v) for k, v in sorted(counts.items()) if v))
        ok += 1
    print("selftest: %d/2 cases ok" % ok)
    return 0 if ok == 2 else 1


if __name__ == "__main__":
    sys.exit(main())
