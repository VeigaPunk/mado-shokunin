#!/usr/bin/env python3
"""Generate --scan fixtures for AdvVcsForms: one JSONL transcript per command."""
import json, os

OUT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w2/AdvVcsForms/fixtures"

def bash_record(cmd):
    return {"type": "message", "id": "m", "timestamp": "2026-10-20T00:00:00.000Z",
            "message": {"role": "assistant", "content": [
                {"type": "toolCall", "id": "c1", "name": "bash",
                 "arguments": {"command": cmd}}]}}

def eval_record(code, lang="py"):
    return {"type": "message", "id": "m", "timestamp": "2026-10-20T00:00:00.000Z",
            "message": {"role": "assistant", "content": [
                {"type": "toolCall", "id": "c1", "name": "eval",
                 "arguments": {"language": lang, "code": code}}]}}

CASES = [
    # name, record, ground truth (write|nowrite|boundary), note
    ("git-add-nv", bash_record("git add -nv ."), "nowrite", "cluster -nv is a real dry run"),
    ("git-add-An", bash_record("git add -An ."), "nowrite", "cluster -An is a real dry run"),
    ("git-add-vn", bash_record("git add -vn ."), "nowrite", "cluster -vn dry run"),
    ("git-add-nvf", bash_record("git add -nvf ."), "nowrite", "cluster -nvf dry run"),
    ("git-add-Nn", bash_record("git add -Nn ."), "nowrite", "-N -n: index untouched"),
    ("git-add--dry", bash_record("git add --dry ."), "nowrite", "unique abbrev of --dry-run"),
    ("git-add-dry-nodry", bash_record("git add --dry-run --no-dry-run ."), "write", "last-wins: real write"),
    ("git-add-nodry-dry", bash_record("git add --no-dry-run --dry-run ."), "nowrite", "last-wins: dry"),
    ("git-add--dry-run-eq-false", bash_record("git add --dry-run=false ."), "nowrite", "git errors: takes no value"),
    ("git-add--no-dry", bash_record("git add --no-dry ."), "write", "abbrev of --no-dry-run: write"),
    ("git-add-n-v-sep", bash_record("git add -n -v ."), "nowrite", "separate flags dry"),
    ("git-add-pn", bash_record("git add -pn ."), "nowrite", "git rejects -p with -n"),
    ("git-dash-n-add", bash_record("git -n add ."), "nowrite", "git rejects global -n"),
    ("git-commit-an", bash_record("git commit -an -m c1"), "write", "-a -n = --all --no-verify"),
    ("git-commit-am", bash_record("git commit -am c2"), "write", "write"),
    ("git-commit-zn", bash_record("git commit -zn -m c4"), "nowrite", "cluster -zn: -z => dry"),
    ("git-commit-z-m", bash_record("git commit -z -m c4b"), "nowrite", "-z selects porcelain"),
    ("git-commit-porcelain-m", bash_record("git commit --porcelain -m c5"), "nowrite", "porcelain implies dry"),
    ("git-commit-porcelain-nodry", bash_record("git commit --porcelain --no-dry-run -m c6"), "nowrite", "--no-dry-run cannot undo --porcelain-implied dry"),
    ("git-commit-nodry-porcelain", bash_record("git commit --no-dry-run --porcelain -m c7"), "nowrite", "same, reversed order"),
    ("git-commit-porcel", bash_record("git commit --porcel -m c8"), "nowrite", "abbrev of --porcelain: dry"),
    ("git-commit-dry-nodry", bash_record("git commit --dry-run --no-dry-run -m c9"), "write", "last-wins real write"),
    ("git-commit-m-n", bash_record("git commit -m -n"), "write", "-n is the message value"),
    ("git-commit-a-m-h", bash_record("git commit -am c10 -h"), "nowrite", "usage"),
    ("git-commit-uno-n", bash_record("git commit -uno -n -m c14"), "write", "-u no + -n no-verify"),
    ("git-commit-s-m", bash_record("git commit -s -m c18"), "write", "signoff write"),
    ("git-commit-dry-run-eq-false", bash_record("git commit --dry-run=false -m c19"), "nowrite", "git errors"),
    ("git-commit--no-dry", bash_record("git commit --no-dry -m c20"), "write", "abbrev negation write"),
    ("git-push-porcelain-n", bash_record("git push --porcelain -n"), "nowrite", "dry-run push; hook runs"),
    ("git-push-porcelain", bash_record("git push --porcelain"), "write", "--porcelain alone is a real push"),
    ("git-push-nv", bash_record("git push -nv"), "nowrite", "cluster -nv dry"),
    ("git-push-dry-nodry", bash_record("git push --dry-run --no-dry-run"), "write", "last-wins real push"),
    ("git-push-nodry-dry", bash_record("git push --no-dry-run --dry-run"), "nowrite", "last-wins dry"),
    ("git-push--dry", bash_record("git push --dry"), "nowrite", "abbrev of --dry-run"),
    ("git-push-dry-run-eq-false", bash_record("git push --dry-run=false"), "nowrite", "git errors"),
    ("git-push--no-dry", bash_record("git push --no-dry"), "write", "abbrev negation push"),
    ("git-push-repo-dry", bash_record("git push --repo --dry-run"), "nowrite", "--dry-run is the --repo value; git errors"),
    ("git-checkout-n", bash_record("git checkout -n seed.txt"), "nowrite", "git rejects -n"),
    ("git-stash-push", bash_record("git stash push -m st1"), "write", "stash push writes"),
    ("git-alias-x-commit", bash_record("git -c alias.x=commit x -m c15"), "boundary", "alias-to-builtin commits; declared out"),
    ("git-clean-f", bash_record("git clean -f"), "boundary", "worktree mutation; declared out"),
    ("git-revert", bash_record("git revert --no-edit HEAD"), "boundary", "declared out"),
    ("jj--help-describe", bash_record("jj --help describe"), "nowrite", "top-level help"),
    ("jj-describe-h-m", bash_record("jj describe -h -m x"), "nowrite", "describe help"),
    ("jj-describe-m-h", bash_record("jj describe -m -h"), "nowrite", "clap error exit 2"),
    ("jj-root", bash_record("jj root"), "nowrite", "no wc snapshot measured"),
    ("jj-config-list", bash_record("jj config list"), "nowrite", "no wc snapshot measured"),
    ("jj-util-config-schema", bash_record("jj util config-schema"), "nowrite", "no wc snapshot measured"),
    ("jj-util-exec-true", bash_record("jj util exec -- true"), "nowrite", "no wc snapshot measured"),
    ("jj-util-exec-git-status", bash_record("jj util exec -- git status"), "nowrite", "payload read-only; no wc snapshot"),
    ("jj-describe-dry", bash_record("jj describe --dry-run -m x"), "nowrite", "clap error exit 2"),
    ("jj-git--dry-run-push", bash_record("jj git --dry-run push"), "nowrite", "clap error exit 2"),
    ("jj-git-fetch-dry", bash_record("jj git fetch --dry-run"), "nowrite", "clap error exit 2"),
    ("jj-git-push-dd-iwc", bash_record("jj git push --dry-run -- --ignore-working-copy"), "nowrite", "clap error exit 2"),
    ("jj-git-push-dry", bash_record("jj git push --dry-run"), "write", "snapshots wc (mut=yes measured)"),
    ("jj-git-push-dry-iwc", bash_record("jj git push --dry-run --ignore-working-copy"), "nowrite", "dry + iwc: nothing"),
    ("jj-git-push-iwc-dry", bash_record("jj git push --ignore-working-copy --dry-run"), "nowrite", "same flags, reversed"),
    ("jj-git-push-b-main", bash_record("jj git push -b main"), "write", "real push to file:// remote"),
    ("jj-iwc-describe", bash_record("jj --ignore-working-copy describe -m hi"), "write", "describe writes even with iwc"),
    ("jj-describe-iwc", bash_record("jj describe --ignore-working-copy -m hi"), "write", "describe writes even with iwc"),
    ("jj-op-log", bash_record("jj op log"), "write", "snapshots wc first"),
    ("jj-file-list", bash_record("jj file list"), "write", "snapshots wc"),
    ("jj-iwc-log", bash_record("jj --ignore-working-copy log"), "nowrite", "iwc honoured"),
    ("jj-log-iwc", bash_record("jj log --ignore-working-copy"), "nowrite", "iwc honoured"),
    ("jj-prev", bash_record("jj prev"), "write", "snapshots wc (then errors)"),
    # eval surfaces
    ("eval-list-add-nv", eval_record('import subprocess\nsubprocess.run(["git", "add", "-nv", "."])'), "nowrite", "literal list argv, clustered -nv"),
    ("eval-system-push-porcelain", eval_record('import os\nos.system("git push --porcelain")'), "write", "shell string real push"),
    ("eval-bang-commit-zn", eval_record('!git commit -zn -m c4'), "nowrite", "bang magic, clustered -zn"),
    ("eval-pct-pct-bash-add-An", eval_record('%%bash\ngit add -An .'), "nowrite", "%%bash cell, clustered -An"),
    ("eval-list-jj-root", eval_record('import subprocess\nsubprocess.run(["jj", "root"])'), "nowrite", "jj root via spawn"),
    ("eval-list-alias", eval_record('import subprocess\nsubprocess.run(["git", "-c", "alias.x=commit", "x", "-m", "c"])'), "boundary", "alias via spawn; declared out"),
    ("eval-list-commit-porcelain-nodry", eval_record('import subprocess\nsubprocess.run(["git", "commit", "--porcelain", "--no-dry-run", "-m", "c"])'), "nowrite", "sticky dry measured"),
]

os.makedirs(OUT, exist_ok=True)
manifest = []
for name, rec, truth, note in CASES:
    path = os.path.join(OUT, name + ".jsonl")
    with open(path, "w") as f:
        f.write(json.dumps(rec) + "\n")
    manifest.append({"case": name, "truth": truth, "note": note})
with open(os.path.join(OUT, "manifest.json"), "w") as f:
    json.dump(manifest, f, indent=1)
print("wrote", len(manifest), "cases")
