#!/usr/bin/env python3
"""Critic builder: cheapest do-nothing / skip-the-work variants for C1 and C3, each committed in a fresh scratch repo.

python3 -I mk_variants.py --scratch /fast/scratch/hyaku/mado-r56/R56CritDoNothing --out <deliverable dir>
Reads the freeze copy (BASE_DIR in scratch), writes each variant as a new scratch repo, runs the critic's checkers
(c1_check.py / c3_check.py, written from registration.md), prints one line per variant and deletes the scratch repo.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile

ap = argparse.ArgumentParser()
ap.add_argument("--scratch", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--only", default="")
A = ap.parse_args()
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c3_check as C3  # noqa: E402  (critic's own checker module, same contract text)

S = A.scratch
BASE = open(os.path.join(S, "BASE_DIR")).read().strip()
ENTRY = "corpus/knowledge/hyprland-config-autoreload-r56.md"
ENV = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "GIT_CONFIG_NOSYSTEM": "1", "LC_ALL": "C"}
REG_RE = re.compile(r"^ {0,3}\|\s*S[0-9]{3,}\s*\|")
SID_RE = re.compile(r"(?<![A-Za-z0-9])S[0-9]{3}(?![0-9])")
TOK_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}")


def git(d, *a, check=True):
    r = subprocess.run(["git", "-C", d, *a], capture_output=True, env=ENV)
    if check and r.returncode:
        raise SystemExit(f"git {a} failed: {r.stderr.decode()}")
    return r.stdout


def newrepo(name):
    d = tempfile.mkdtemp(prefix=name + ".", dir=S)
    git(d, "init", "-q")
    top = git(d, "rev-parse", "--show-toplevel").decode().strip()
    assert top == d, (top, d)
    subprocess.run(f"git -C {BASE} archive HEAD | tar -x -C {d}", shell=True, check=True, env=ENV)
    return d


def commit(d):
    git(d, "add", "-A")
    git(d, "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "commit", "-qm", "variant")
    return git(d, "rev-parse", "HEAD").decode().strip()


def rd(d, p):
    return open(os.path.join(d, p), encoding="utf-8").read()


def wr(d, p, t):
    os.makedirs(os.path.dirname(os.path.join(d, p)), exist_ok=True)
    open(os.path.join(d, p), "w", encoding="utf-8").write(t)


def freeze_tables(d):
    return json.loads(rd(d, ".ufo/waves/round-56/frozen-tables.json"))


# ---------------- C1 variants ----------------

def c1_entry(d, placeholder=False):
    c1 = freeze_tables(d)["c1"]
    K, H = c1["k"], c1["h"]
    lines = ["# Hyprland config auto-reload on 0.56.2 (critic junk control)", "",
             "source: " + " ".join(c1["new_row_ids"]), "verified-at: 2026-10-28", "recheck: 90d", "",
             "## Rows", "", "| id | proposition | src | pin:line | quote |", "| --- | --- | --- | --- | --- |"]
    for r in K + H:
        rid, pin, line, q = r["id"], r["pin"], r["line"], r["quote"]
        src = r.get("sid", "host")
        ident = TOK_RE.findall(q)[0]
        if placeholder:
            prop = (f"placeholder proposition text for row {rid}, not a claim about any source line" if rid.startswith("K")
                    else f"placeholder host proposition {rid}, not a read")
        elif rid.startswith("K"):
            prop = f"{rid} pins line {line} of the pinned source and says that {ident} is part of the config reload path."
        else:
            prop = f"{rid} is a host read of the pinned host dump and says that {ident} is set in the live config."
        lines.append(f"| {rid} | {prop} | {src} | {pin}:{line} | `{q}` |")
    wr(d, ENTRY, "\n".join(lines) + "\n")


def c1_registry(d):
    c1 = freeze_tables(d)["c1"]
    rev = c1["commit"]
    text = rd(d, "corpus/SOURCES.md").split("\n")
    last = max(i for i, l in enumerate(text) if REG_RE.match(l))
    new = []
    for sid in c1["new_row_ids"]:
        pin = c1["rows"][sid]
        suffix = c1["pin_suffix"][pin]
        ks = [r for r in c1["k"] if r["pin"] == pin]
        base = suffix.rsplit("/", 1)[-1]
        lo, hi = min(r["line"] for r in ks), max(r["line"] for r in ks)
        if pin.startswith("Hyprland-"):
            url = f"https://raw.githubusercontent.com/hyprwm/Hyprland/{rev}/{suffix}"
        else:
            url = f"https://man7.org/linux/man-pages/{suffix}"
        new.append(f"| {sid} | junk {pin} - {url} | code | A | junk scope | {base}:{lo}-{hi} | junk teaches | mined | 2026-10-28 | 90d | {ENTRY} |")
    text[last + 1:last + 1] = new
    wr(d, "corpus/SOURCES.md", "\n".join(text))


def c1_readme(d):
    t = rd(d, "corpus/README.md")
    if not t.endswith("\n"):
        t += "\n"
    t += f"| `knowledge/hyprland-config-autoreload-r56.md` (junk control) | junk | S383 |\n"
    wr(d, "corpus/README.md", t)


C1_VARIANTS = {
    # the cheapest entry that copies the frozen quotes, fills minimal propositions and fabricates registry rows
    "c1-junk-full": [lambda d: c1_entry(d), lambda d: c1_registry(d), lambda d: c1_readme(d)],
    # same entry, no fabricated registry rows (checks that registry legs bind)
    "c1-junk-no-registry": [lambda d: c1_entry(d), lambda d: c1_readme(d)],
    # contract control 2 (placeholder propositions) with the same registry and index, must fail tok/content
    "c1-placeholder-full": [lambda d: c1_entry(d, placeholder=True), lambda d: c1_registry(d), lambda d: c1_readme(d)],
}


# ---------------- C3 variants ----------------

def reg_lines(d):
    return rd(d, "corpus/SOURCES.md").split("\n")


def c3_fill_all(d):
    entries = C3.entries_at(d, ENV, "HEAD") if False else sorted(
        os.path.join("corpus/knowledge", f) for f in os.listdir(os.path.join(d, "corpus/knowledge")) if f.endswith(".md"))
    out = []
    for l in reg_lines(d):
        if REG_RE.match(l):
            cells = C3_cells(l)
            cells[10] = " ".join(entries)
            l = "| " + " | ".join(cells) + " |"
        out.append(l)
    wr(d, "corpus/SOURCES.md", "\n".join(out))


def C3_cells(l):
    s = l.strip()
    s = s[1:] if s.startswith("|") else s
    s = s[:-1] if s.endswith("|") else s
    return [c.strip() for c in s.split("|")]


def c3_comment_line(d):
    out = []
    for l in reg_lines(d):
        out.append(l)
        if REG_RE.match(l):
            out.append("<!-- r56 critic control: back-reference line -->")
    wr(d, "corpus/SOURCES.md", "\n".join(out))


def c3_comment_cell(d):
    out = []
    for l in reg_lines(d):
        if REG_RE.match(l):
            cells = C3_cells(l)
            cells[10] = cells[10] + " <!-- back-reference -->"
            l = "| " + " | ".join(cells) + " |"
        out.append(l)
    wr(d, "corpus/SOURCES.md", "\n".join(out))


def registry_and_entries(d):
    rows = C3.registry(rd(d, "corpus/SOURCES.md"))
    ents = {}
    for f in sorted(os.listdir(os.path.join(d, "corpus/knowledge"))):
        if f.endswith(".md"):
            ents["corpus/knowledge/" + f] = rd(d, "corpus/knowledge/" + f)
    return rows, ents


def strip_refs_outside_fences(text, drop):
    """replace S### tokens for which drop(token) is true, on lines outside fenced blocks."""
    out, fence = [], None
    for l in text.split("\n"):
        m = C3.FENCE_RE.match(l)
        if fence is None and m:
            fence = m.group(1)[0]
            out.append(l)
            continue
        if fence is not None:
            if m and m.group(1)[0] == fence:
                fence = None
            out.append(l)
            continue
        out.append(SID_RE.sub(lambda mm: "[ref]" if drop(mm.group(0)) else mm.group(0), l))
    return "\n".join(out)


def c3_delete_missing_cites(d):
    rows, ents = registry_and_entries(d)
    used = {sid: set(C3.USED_RE.findall(rs[0][10])) for sid, rs in rows.items()}
    for path, text in ents.items():
        cites = C3.cites(text)
        drop = lambda s, p=path: s in rows and p not in used[s] and s in cites  # noqa: E731
        wr(d, path, strip_refs_outside_fences(text, drop))


def c3_strip_all(d):
    rows, ents = registry_and_entries(d)
    for path, text in ents.items():
        wr(d, path, strip_refs_outside_fences(text, lambda s: True))
    out = []
    for l in reg_lines(d):
        if REG_RE.match(l):
            cells = C3_cells(l)
            cells[10] = "—"
            l = "| " + " | ".join(cells) + " |"
        out.append(l)
    wr(d, "corpus/SOURCES.md", "\n".join(out))


C3_VARIANTS = {
    "c3-fill-all": c3_fill_all,
    "c3-comment-line-per-row": c3_comment_line,
    "c3-comment-in-cell-per-row": c3_comment_cell,
    "c3-delete-missing-cites": c3_delete_missing_cites,
    "c3-strip-all-citations": c3_strip_all,
}


def run_checker(d, name, script, work):
    r = subprocess.run([sys.executable, "-I", os.path.join(HERE, script), "--repo", d, "--rev", "HEAD", "--work", work],
                       capture_output=True, text=True, env=ENV)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def main():
    os.makedirs(A.out, exist_ok=True)
    results = []
    jobs = [(n, f, "c1_check.py") for n, f in C1_VARIANTS.items()] + [(n, f, "c3_check.py") for n, f in C3_VARIANTS.items()]
    for name, build, script in jobs:
        if A.only and A.only not in name:
            continue
        d = newrepo(name)
        if name.startswith("c1") or name.startswith("c3"):
            # variant steps applied in order, each reads the working tree
            if isinstance(build, list):
                for step in build:
                    step(d)
            else:
                build(d)
        rev = commit(d)
        work = os.path.join(S, name + "-work")
        os.makedirs(work, exist_ok=True)
        rc, out, err = run_checker(d, name, script, work)
        line = f"{name}: rc={rc} {out}" + (f"  [stderr: {err}]" if err else "")
        print(line)
        results.append(line)
        if os.environ.get("KEEP"):
            dst = os.path.join(A.out, "artifacts", name)
            shutil.rmtree(dst, ignore_errors=True)
            os.makedirs(dst, exist_ok=True)
            for rel in ("corpus/knowledge", "corpus/SOURCES.md", "corpus/README.md"):
                src = os.path.join(d, rel)
                if os.path.isdir(src):
                    shutil.copytree(src, os.path.join(dst, rel))
                elif os.path.isfile(src):
                    shutil.copy(src, os.path.join(dst, os.path.basename(rel)))
        shutil.rmtree(d, ignore_errors=True)
        shutil.rmtree(work, ignore_errors=True)
    with open(os.path.join(A.out, "variants-run.txt"), "a", encoding="utf-8") as f:  # noqa
        f.write("\n".join(results) + "\n")


if __name__ == "__main__":
    main()
