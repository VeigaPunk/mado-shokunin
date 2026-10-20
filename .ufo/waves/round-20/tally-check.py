#!/usr/bin/env python3
"""Round-20 criterion-30 count re-derivation checker (R19-V2/V4/V5).

A count stated in a SCORECARD, lesson or report claim is re-derived at the
measured revision by a cited command. Each registry entry binds a stated
number to the committed line that states it and to a derivation that is one
of this file's own subcommands; the checker compares the two numbers.

Usage:
  tally-check.py REGISTRY [--set all|red|green] [--rev REV] [--expect]
  tally-check.py receipt-files   --rev REV --path PATH [--schema NAME]
  tally-check.py pointer-token   --counter-rev REV --rev REV --token TOKEN
                                 [--counter PATH]
  tally-check.py selftest-labels --old REV --new REV --label-regex RE
                                 [--path PATH] [--function NAME]
                                 [--fail-helper NAME]

Registry (tally-claims.json): {"schema": "mado-tally-claims-v1",
"red": [entry, ...], "green": [entry, ...]}, each entry

  {"id": "<[A-Za-z0-9._:-]+, unique>",
   "statement": {"rev": "<40-hex lane commit, or REV>",
                 "path": "<lane-relative path>",
                 "line_regex": "<Python regex with a (?P<stated>...) group>"},
   "stated": <int>,
   "derive": {"argv": ["python3", "-I", ".ufo/waves/round-20/tally-check.py",
                       "<subcommand>", ...],
              "extract_regex": "(?m)^<count key>=(\\d+)...; group 1 or (?P<derived>...)"},
   "note": "<what is counted, and how>"}

REV stands for the checker's --rev (the measured revision), so a corrected
statement can be registered before the commit that lands it exists; any
other revision in the registry is a full 40-hex hash (never a branch).

For each selected entry:
1. `git show <rev>:<path>` must contain exactly one line (split on "\\n",
   numbered like `grep -n`) matching line_regex: none -> ERROR (statement
   absent at rev), several -> ERROR (ambiguous). The `stated` group is
   required and must quote `stated` (digits, or an English number word such
   as "ten"), else ERROR: the number is read from the statement, never only
   from the registry.
2. derive.argv must be `python3 -I .ufo/waves/round-20/tally-check.py
   <subcommand> ...` -- a committed helper, never an ad hoc command. Every
   value after --rev/--counter-rev/--old/--new is 40-hex or REV; no
   --path/--counter value may be the statement's own file; a --token value
   must occur as a word in the statement line. extract_regex must begin
   `(?m)^<key>=` with <key> one of the subcommand's count keys (COUNT_KEYS),
   so a derived number is always a named count, never a digit picked out of
   a label, hash or timestamp. The derive runs with cwd = lane; extract_regex
   must match its stdout exactly once, and that group is the derived integer.
   A nonzero derive exit -> ERROR.
3. Prints `MATCH|MISMATCH|ERROR <id> stated=<s> derived=<d>` (derived=none
   on ERROR) and one indented detail line (set, expectation, resolved
   statement location, count key, the derive as run), then
   `TALLY_SUMMARY: ...` and `EXPECT_SUMMARY: k/n`, where k counts entries on
   their set's side: red -> MISMATCH, green -> MATCH.

Exit: 0 every selected entry MATCH; 1 any MISMATCH (no ERROR); 2 any ERROR,
a malformed registry, or an empty selection -- nothing re-derived is never a
pass. "red" holds stale statements (each must MISMATCH, so `--set red` exits
1); "green" holds corrected statements (each must MATCH, `--set green` exits
0). A red entry that MATCHes is invisible in an exit 1 shared with other reds;
EXPECT_SUMMARY shows it, and --expect makes it the exit code instead: 0 every
entry on its set's side, 1 otherwise, 2 any ERROR.

Subcommands (exit 0 printed, 2 could-not-evaluate) read committed bytes only
(`git rev-parse`, `git show`, `git ls-tree` inside the lane); nothing taken
from a revision is executed and no host state is read or touched:

receipt-files   The number of files a committed tripwire receipt scanned: the
                receipt must hold exactly one JSON line whose "schema" is
                --schema (default mado-tripwire-verdict-v1) and whose "files"
                is a list; prints files=len(files), distinct_paths,
                jsonl_paths and the receipt's own RECEIPT header provenance.
pointer-token   The round-19 C2 counter's file set, re-derived from the
                counter's committed text (parsed with ast, never executed):
                its PIN_REV, OLD and POINTER constants, and its in_scope
                predicate, which must be AST-identical to `in_scope` below
                (else exit 2). Denominator = in-scope paths at PIN_REV whose
                bytes contain OLD. At --rev a file's pointer lines are the
                lines (str.splitlines, as the counter numbers them) matching
                POINTER; first_line counts files whose FIRST pointer line
                contains \\bTOKEN\\b, any_line files with the token on ANY
                pointer line, current files with any pointer line.
selftest-labels Labeled assertion occurrences in one shell function body
                (default `selftest()` of tools/mado-verify.sh) at --old and
                --new, and their multiset difference. The body is tokenized
                as shell text (quotes, $( ), ${ }, backticks, comments, line
                continuations; here-document bodies skipped). Each helper
                defined inside the body gets the label position that reaches
                --fail-helper (whose own label is $1) by following its body's
                positional arguments; a labeled assertion is a call, in the
                body outside helper definitions, to a helper with a resolved
                position, and its label is that argument with quotes removed
                and nothing expanded. removed_* counts old - new restricted
                to labels matching --label-regex; removed_all_* is
                unrestricted.
"""

import argparse
import ast
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve()
LANE = HERE.parents[3]  # .ufo/waves/round-20/tally-check.py -> lane root
SELF = HERE.relative_to(LANE).as_posix()
SUBCOMMANDS = ("receipt-files", "pointer-token", "selftest-labels")
DERIVE_TIMEOUT = 300
REV_SHAPE = re.compile(r"[0-9a-f]{7,40}|refs/heads/[A-Za-z0-9._/-]+")
ID_SHAPE = re.compile(r"[A-Za-z0-9._:-]+")
NUMBER_WORDS = {w: n for n, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve "
    "thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}


class Unevaluable(Exception):
    """Could not evaluate: a git read failed or an input is malformed."""


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    r = subprocess.run(
        ["git", "-C", str(LANE), *args],
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
    )
    if r.returncode != 0:
        raise Unevaluable(f"git {' '.join(args)} exited {r.returncode}")
    return r.stdout


def commit(rev):
    """Full hash of a lane commit; revisions are hex or refs/heads/<name>."""
    if not isinstance(rev, str) or not REV_SHAPE.fullmatch(rev):
        raise Unevaluable(f"revision {rev!r} is not 7-40 hex or refs/heads/<name>")
    return git("rev-parse", "--verify", "--quiet", rev + "^{commit}").decode().strip()


def lane_path(path):
    if (not isinstance(path, str) or not path or path.startswith(("/", "-"))
            or ".." in path.split("/")):
        raise Unevaluable(f"path {path!r} is not lane-relative")
    return path


def show(rev, path):
    """Bytes of <rev>:<path>; rev must already be a full commit hash."""
    return git("show", f"{rev}:{lane_path(path)}")


def show_or_none(rev, path):
    try:
        return show(rev, path)
    except Unevaluable:
        return None


def parse_number(text):
    t = str(text).strip().lower().replace(",", "")
    if t.isdigit():
        return int(t)
    if t in NUMBER_WORDS:
        return NUMBER_WORDS[t]
    raise Unevaluable(f"{text!r} is not a number")


# --- receipt-files ----------------------------------------------------------

def cmd_receipt_files(a):
    rev = commit(a.rev)
    blob = show(rev, a.path)
    text = blob.decode("utf-8", errors="replace")
    verdicts = []
    for line in text.split("\n"):
        s = line.strip()
        if not s.startswith("{"):
            continue
        try:
            obj = json.loads(s)
        except ValueError:
            continue
        if (isinstance(obj, dict) and obj.get("schema") == a.schema
                and isinstance(obj.get("files"), list)):
            verdicts.append(obj)
    if len(verdicts) != 1:
        raise Unevaluable(f"{a.path}@{rev}: {len(verdicts)} {a.schema} objects, want 1")
    files = verdicts[0]["files"]
    paths = [f.get("path") if isinstance(f, dict) else None for f in files]
    named = [p for p in paths if isinstance(p, str)]
    head = text.split("\n", 1)[0]
    prov = dict(re.findall(r"\b(tool|tool_sha256|measured_commit|utc)=(\S+)", head)
                if head.startswith("RECEIPT") else [])
    print(f"receipt={a.path}")
    print(f"rev={rev}")
    print(f"receipt_sha256={sha256(blob)}")
    for key in ("tool", "tool_sha256", "measured_commit", "utc"):
        print(f"header_{key}={prov.get(key, '-')}")
    print(f"schema={a.schema}")
    print(f"files={len(files)}")
    print(f"distinct_paths={len(set(named))}")
    print(f"jsonl_paths={sum(p.endswith('.jsonl') for p in named)}")
    print(f"pathless_entries={len(files) - len(named)}")
    counts = verdicts[0].get("counts")
    if isinstance(counts, dict):
        print("counts=" + json.dumps(counts, sort_keys=True, separators=(",", ":")))


# --- pointer-token ----------------------------------------------------------

# AST-identical copy of in_scope in .ufo/waves/round-19/fresh-pins.py at
# 1f7f995; pointer-token refuses a counter whose predicate differs.
def in_scope(p):
    return ((p.startswith("corpus/knowledge/") and p.endswith(".md"))
            or p in ("corpus/README.md", "SKILL.md", "PROVINCE.md")
            or p.startswith("tools/"))


def module_defs(source, label):
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise Unevaluable(f"{label}: {exc}") from None
    consts, funcs = {}, {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            funcs[node.name] = node
        elif (isinstance(node, ast.Assign) and len(node.targets) == 1
              and isinstance(node.targets[0], ast.Name)):
            consts[node.targets[0].id] = node.value
    return consts, funcs


def same_function(f, g):
    return (ast.dump(f.args) == ast.dump(g.args)
            and [ast.dump(s) for s in f.body] == [ast.dump(s) for s in g.body])


def cmd_pointer_token(a):
    crev = commit(a.counter_rev)
    src = show(crev, a.counter)
    where = f"{a.counter}@{crev}"
    consts, funcs = module_defs(src.decode("utf-8"), where)

    def text_const(name):
        node = consts.get(name)
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        raise Unevaluable(f"{where}: {name} is not a string constant")

    pin_rev, old = text_const("PIN_REV"), text_const("OLD")
    node = consts.get("POINTER")
    if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
            and node.func.attr == "compile" and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "re" and len(node.args) == 1 and not node.keywords
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)):
        raise Unevaluable(f"{where}: POINTER is not re.compile(<string>)")
    pointer = re.compile(node.args[0].value)
    _, mine = module_defs(HERE.read_text(encoding="utf-8"), SELF)
    if "in_scope" not in funcs or not same_function(funcs["in_scope"], mine["in_scope"]):
        raise Unevaluable(f"{where}: in_scope differs from {SELF}:in_scope")

    pin = commit(pin_rev)
    denom = sorted(p for p in git("ls-tree", "-r", "--name-only", pin).decode().splitlines()
                   if in_scope(p) and old.encode() in show(pin, p))
    rev = commit(a.rev)
    token = re.compile(r"\b" + re.escape(a.token) + r"\b")
    rows = []
    for p in denom:
        blob = show_or_none(rev, p)
        if blob is None:
            rows.append((p, None, [], []))
            continue
        lines = blob.decode(errors="replace").splitlines()
        hits = [i + 1 for i, ln in enumerate(lines) if pointer.search(ln)]
        rows.append((p, True, hits, [h for h in hits if token.search(lines[h - 1])]))
    n = len(rows)
    print(f"counter={a.counter}")
    print(f"counter_rev={crev}")
    print(f"counter_sha256={sha256(src)}")
    print(f"pin_rev={pin}")
    print(f"old_token={old}")
    print(f"pointer_regex={pointer.pattern}")
    print(f"rev={rev}")
    print(f"token={a.token}")
    print(f"denominator={n}")
    print(f"current={sum(bool(h) for _, _, h, _ in rows)}/{n}")
    print(f"first_line={sum(bool(h) and h[0] in t for _, _, h, t in rows)}/{n}")
    print(f"any_line={sum(bool(t) for _, _, _, t in rows)}/{n}")
    for p, present, hits, tok in rows:
        if present is None:
            print(f"file {p} absent")
            continue
        first = hits[0] if hits else "-"
        print(f"file {p} pointer_lines={len(hits)} first={first} "
              f"first_has_token={'yes' if hits and hits[0] in tok else 'no'} "
              f"token_lines={','.join(map(str, tok)) or '-'}")


# --- selftest-labels: just enough shell grammar to find helper calls -------

class Incomplete(Exception):
    """The text ends inside a quote, an expansion or a line continuation."""


class ShellError(Unevaluable):
    """The function body could not be tokenized or resolved."""


OPERATORS = (";;&", ";;", ";&", "&&", "||", "|&", ";", "|", "&", "(", ")", "\n")
WORD_BREAK = frozenset(" \t\n;&|()")
RESERVED_PREFIX = frozenset({"if", "then", "else", "elif", "do", "while", "until", "!", "time"})
RESERVED_END = frozenset({"fi", "done", "esac"})
ASSIGNMENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(\[[^]]*\])?\+?=")
POSITIONAL = re.compile(r"\$\{?([1-9])\}?(?![0-9])")


def _single(s, i):
    k = s.find("'", i)
    if k < 0:
        raise Incomplete
    return k + 1


def _until(s, i, end):
    """Index after the first unescaped `end` from i ($'...' bodies, backticks)."""
    while i < len(s):
        if s[i] == "\\":
            i += 2
        elif s[i] == end:
            return i + 1
        else:
            i += 1
    raise Incomplete


def _double(s, i):
    """Double-quoted body from i: (index after the closing quote, unquoted text)."""
    out = []
    while i < len(s):
        c = s[i]
        if c == "\\":
            if i + 1 >= len(s):
                raise Incomplete
            d = s[i + 1]
            if d != "\n":
                out.append(d if d in '$`"\\' else c + d)
            i += 2
        elif c == '"':
            return i + 1, "".join(out)
        elif c == "$":
            j = _dollar(s, i)
            out.append(s[i:j])
            i = j
        elif c == "`":
            j = _until(s, i + 1, "`")
            out.append(s[i:j])
            i = j
        else:
            out.append(c)
            i += 1
    raise Incomplete


def _dollar(s, i):
    """s[i] == "$": index after the expansion (callers keep its raw text)."""
    nxt = s[i + 1:i + 2]
    if nxt == "(":
        return _nested(s, i + 2, "(", ")")
    if nxt == "{":
        return _nested(s, i + 2, "{", "}")
    if nxt == "'":
        return _until(s, i + 2, "'")
    return i + 1


def _nested(s, i, opener, closer):
    """Body of $( ), $(( )), ${ } or <( ) from i: index after the matching closer."""
    depth = 1
    while i < len(s):
        c = s[i]
        if c == "\\":
            i += 2
        elif c == "'":
            i = _single(s, i + 1)
        elif c == '"':
            i = _double(s, i + 1)[0]
        elif c == "`":
            i = _until(s, i + 1, "`")
        elif c == "$":
            i = _dollar(s, i)
        else:
            if c == opener:
                depth += 1
            elif c == closer:
                depth -= 1
                if depth == 0:
                    return i + 1
            i += 1
    raise Incomplete


def _heredoc_at(s, i):
    return s.startswith("<<", i) and not s.startswith("<<<", i)


def _word(s, i):
    """One word from i: (index after it, value with quotes removed, quoted?)."""
    out, quoted, start = [], False, i
    while i < len(s):
        c = s[i]
        prev = s[i - 1] if i > start else ""
        if c in "<>" and s[i + 1:i + 2] == "(":
            j = _nested(s, i + 2, "(", ")")  # process substitution
            out.append(s[i:j])
            i = j
        elif c == "<" and i > start and _heredoc_at(s, i):
            break  # the caller reads the here-document operator
        elif c in WORD_BREAK:
            if c == "&" and (prev in ("<", ">") or (i == start and s.startswith("&>", i))):
                out.append(c)  # >&2, 2>&1, &>file
                i += 1
            else:
                break
        elif c == "\\":
            if i + 1 >= len(s):
                raise Incomplete
            if s[i + 1] != "\n":
                out.append(s[i + 1])
                quoted = True
            i += 2
        elif c == "'":
            j = _single(s, i + 1)
            out.append(s[i + 1:j - 1])
            quoted = True
            i = j
        elif c == '"':
            j, body = _double(s, i + 1)
            out.append(body)
            quoted = True
            i = j
        elif c == "$":
            j = _dollar(s, i)
            out.append(s[i:j])
            i = j
        elif c == "`":
            j = _until(s, i + 1, "`")
            out.append(s[i:j])
            i = j
        else:
            out.append(c)
            i += 1
    return i, "".join(out), quoted


def _tokens(s):
    """Tokens of shell text: ([(kind, value, quoted)], [(heredoc delimiter, strip tabs)])."""
    toks, docs, i = [], [], 0
    while i < len(s):
        c = s[i]
        if c in " \t":
            i += 1
        elif c == "\\" and i + 1 == len(s):
            raise Incomplete
        elif c == "\\" and s[i + 1] == "\n":
            i += 2
        elif c == "#":
            k = s.find("\n", i)
            i = len(s) if k < 0 else k
        elif _heredoc_at(s, i):
            j = i + 2
            strip = s.startswith("-", j)
            j += strip
            while j < len(s) and s[j] in " \t":
                j += 1
            j, delim, _ = _word(s, j)
            if not delim:
                raise ShellError(f"here-document without a delimiter: {s[i:i + 40]!r}")
            docs.append((delim, strip))
            toks.append(("redir", "<<" + delim, False))
            i = j
        else:
            op = None if s.startswith("&>", i) else next(
                (o for o in OPERATORS if s.startswith(o, i)), None)
            if op:
                toks.append(("op", op, False))
                i += len(op)
                continue
            j, value, quoted = _word(s, i)
            if j == i:
                raise ShellError(f"tokenizer stalled at {s[i:i + 40]!r}")
            toks.append(("word", value, quoted))
            i = j
    return toks, docs


def _logical_lines(lines, start):
    """(1-based first line, tokens) from lines[start:], joining spans, skipping heredocs."""
    i = start
    while i < len(lines):
        first, buf = i, lines[i]
        while True:
            try:
                toks, docs = _tokens(buf)
                break
            except Incomplete:
                i += 1
                if i >= len(lines):
                    raise ShellError(f"unterminated construct from line {first + 1}") from None
                buf += "\n" + lines[i]
        i += 1
        for delim, strip in docs:
            while True:
                if i >= len(lines):
                    raise ShellError(f"unterminated here-document {delim} from line {first + 1}")
                body = lines[i].lstrip("\t") if strip else lines[i]
                i += 1
                if body == delim:
                    break
        yield first + 1, toks


def function_calls(lines, func):
    """Simple commands in `func() { ... }`: (first, last, defs, [(line, owner, name, args)])."""
    head = re.compile(r"\s*" + re.escape(func) + r"\s*\(\s*\)\s*\{")
    start = next((k for k, ln in enumerate(lines) if head.match(ln)), None)
    if start is None:
        raise ShellError(f"no {func}() definition")
    depth, stack, pending, defs, calls = 0, [], None, {}, []
    for ln, toks in _logical_lines(lines, start):
        cmd, k = True, 0
        while k < len(toks):
            kind, val, quoted = toks[k]
            if kind == "op":
                cmd = True
                k += 1
                continue
            if kind == "redir" or not cmd:
                k += 1
                continue
            if not quoted and val == "{":
                depth += 1
                if pending is not None:
                    stack.append((pending, depth))
                    defs[pending] = ln
                    pending = None
                k += 1
                continue
            if not quoted and val == "}":
                if stack and stack[-1][1] == depth:
                    stack.pop()
                    if not stack:
                        return start + 1, ln, defs, calls
                depth -= 1
                cmd = False
                k += 1
                continue
            if not quoted and val in RESERVED_PREFIX:
                k += 1
                continue
            if not quoted and val in RESERVED_END:
                cmd = False
                k += 1
                continue
            if not quoted and val == "function" and k + 1 < len(toks) and toks[k + 1][0] == "word":
                pending = toks[k + 1][1]
                k += 2
                if toks[k:k + 2] == [("op", "(", False), ("op", ")", False)]:
                    k += 2
                continue
            if toks[k + 1:k + 3] == [("op", "(", False), ("op", ")", False)]:
                pending = val
                k += 3
                continue
            if not quoted and ASSIGNMENT.match(val) and k + 1 < len(toks) and toks[k + 1][0] == "word":
                k += 1  # assignment prefix: the next word is the command
                continue
            j, args = k + 1, []
            while j < len(toks) and toks[j][0] != "op":
                if toks[j][0] == "word":
                    args.append(toks[j][1])
                j += 1
            calls.append((ln, stack[-1][0] if stack else None, val, args))
            cmd, k = False, j
    raise ShellError(f"{func}() from line {start + 1} is never closed")


def label_positions(defs, calls, func, fail_helper):
    """Label argument position of each helper defined inside func()."""
    if fail_helper not in defs:
        raise ShellError(f"{fail_helper}() is not defined inside {func}()")
    bodies = {}
    for _, owner, name, args in calls:
        if owner in defs and owner != func:
            bodies.setdefault(owner, []).append((name, args))
    pos = {fail_helper: 1}

    def resolve(h, seen):
        if h in pos:
            return pos[h]
        if h in seen:
            return None
        found = set()
        for name, args in bodies.get(h, ()):
            if name not in defs or name in (h, func):
                continue
            p = resolve(name, seen | {h})
            if p is None or p > len(args):
                continue
            m = POSITIONAL.match(args[p - 1])
            if m:
                found.add(int(m.group(1)))
        if len(found) > 1:
            raise ShellError(f"{h}(): label reaches {fail_helper} from positions {sorted(found)}")
        pos[h] = found.pop() if found else None
        return pos[h]

    for h in defs:
        if h != func:
            resolve(h, frozenset())
    return {h: p for h, p in pos.items() if p}


def assertion_labels(rev, path, func, fail_helper):
    blob = show(rev, path)
    lines = blob.decode("utf-8", errors="replace").split("\n")
    first, last, defs, calls = function_calls(lines, func)
    positions = label_positions(defs, calls, func, fail_helper)
    labels, unlabeled = [], 0
    for ln, owner, name, args in calls:
        if owner != func or name not in positions:
            continue
        p = positions[name]
        if p > len(args):
            unlabeled += 1
        else:
            labels.append((args[p - 1], ln))
    others = sorted(d for d in defs if d != func and d not in positions)
    return {"blob": sha256(blob), "first": first, "last": last, "positions": positions,
            "labels": labels, "unlabeled": unlabeled, "others": others}


def label_id(label):
    m = re.match(r"[A-Za-z][A-Za-z0-9]*", label)
    return m.group(0) if m else "-"


def cmd_selftest_labels(a):
    try:
        rx = re.compile(a.label_regex)
    except re.error as exc:
        raise Unevaluable(f"--label-regex: {exc}") from None
    inv = {}
    for side, r in (("old", a.old), ("new", a.new)):
        rev = commit(r)
        inv[side] = (rev, assertion_labels(rev, a.path, a.function, a.fail_helper))
    old = Counter(lbl for lbl, _ in inv["old"][1]["labels"])
    new = Counter(lbl for lbl, _ in inv["new"][1]["labels"])
    removed, added = old - new, new - old
    chosen = Counter({lbl: c for lbl, c in removed.items() if rx.search(lbl)})
    print(f"path={a.path} function={a.function} fail_helper={a.fail_helper}")
    for side in ("old", "new"):
        rev, d = inv[side]
        print(f"{side}={rev} blob_sha256={d['blob']} block={d['first']}-{d['last']} "
              f"occurrences={len(d['labels'])} distinct={len({lbl for lbl, _ in d['labels']})} "
              f"unlabeled_calls={d['unlabeled']}")
        print(f"{side}_label_positions="
              + ",".join(f"{h}:{p}" for h, p in sorted(d["positions"].items())))
        print(f"{side}_helpers_without_label={','.join(d['others']) or '-'}")
    print(f"removed_all_occurrences={sum(removed.values())}")
    print(f"removed_all_distinct={len(removed)}")
    print(f"added_all_occurrences={sum(added.values())}")
    print(f"added_all_distinct={len(added)}")
    print(f"label_regex={a.label_regex}")
    print(f"removed_occurrences={sum(chosen.values())}")
    print(f"removed_distinct={len(chosen)}")
    print(f"removed_unmatched_occurrences={sum(removed.values()) - sum(chosen.values())}")
    old_lines = {}
    for lbl, ln in inv["old"][1]["labels"]:
        old_lines.setdefault(lbl, []).append(ln)
    for lbl in sorted(removed):
        print(f"removed {removed[lbl]}x {'matched' if lbl in chosen else 'unmatched'} "
              f"old_lines={','.join(map(str, old_lines[lbl]))} "
              f"label={json.dumps(lbl, ensure_ascii=False)}")
    ids = Counter()
    for lbl, c in added.items():
        ids[label_id(lbl)] += c
    print("added_by_id=" + ",".join(f"{k}:{v}" for k, v in sorted(ids.items())))


# --- registry check ---------------------------------------------------------

FULL_HEX = re.compile(r"[0-9a-f]{40}")
PLACEHOLDER = "REV"
REV_FLAGS = frozenset({"--rev", "--counter-rev", "--old", "--new"})
SOURCE_FLAGS = frozenset({"--path", "--counter"})
COUNT_KEYS = {
    "receipt-files": ("files", "distinct_paths", "jsonl_paths", "pathless_entries"),
    "pointer-token": ("denominator", "current", "first_line", "any_line"),
    "selftest-labels": ("removed_occurrences", "removed_distinct",
                        "removed_unmatched_occurrences", "removed_all_occurrences",
                        "removed_all_distinct", "added_all_occurrences", "added_all_distinct"),
}
EXTRACT_KEY = re.compile(r"\(\?m\)\^([a-z_]+)=")
EXPECT = {"red": "MISMATCH", "green": "MATCH"}


def pinned(rev, measured):
    """A registry revision: a full 40-hex commit, or REV (the checker's --rev)."""
    if rev == PLACEHOLDER:
        if measured is None:
            raise Unevaluable(f"entry reads at {PLACEHOLDER}; pass --rev")
        return measured
    if not (isinstance(rev, str) and FULL_HEX.fullmatch(rev)):
        raise Unevaluable(f"revision {rev!r} is neither 40-hex nor {PLACEHOLDER}")
    return commit(rev)


def check_statement(st, measured):
    """(rev, path, line number, line, stated text) of the one matching line."""
    if not isinstance(st, dict):
        raise Unevaluable("statement is not an object")
    rev = pinned(st.get("rev"), measured)
    path = lane_path(st.get("path"))
    blob = show(rev, path)
    try:
        rx = re.compile(st.get("line_regex"))
    except (re.error, TypeError) as exc:
        raise Unevaluable(f"line_regex: {exc}") from None
    if "stated" not in rx.groupindex:
        raise Unevaluable("line_regex has no (?P<stated>...) group")
    hits = []
    for n, line in enumerate(blob.decode("utf-8", errors="replace").split("\n"), 1):
        m = rx.search(line)
        if m:
            hits.append((n, line, m))
    if not hits:
        raise Unevaluable(f"statement absent: no line of {path}@{rev} matches line_regex")
    if len(hits) > 1:
        raise Unevaluable(f"statement ambiguous: {len(hits)} lines of {path}@{rev} match "
                          f"(first: {','.join(str(n) for n, _, _ in hits[:10])})")
    n, line, m = hits[0]
    if m.group("stated") is None:
        raise Unevaluable("the (?P<stated>...) group did not participate in the match")
    return rev, path, n, line, m.group("stated")


def derive_plan(dv, measured, statement_path, statement_line):
    """The derive argv as it will run (REV resolved) and its count key."""
    if not isinstance(dv, dict):
        raise Unevaluable("derive is not an object")
    argv = dv.get("argv")
    if not (isinstance(argv, list) and len(argv) >= 4 and all(isinstance(x, str) for x in argv)):
        raise Unevaluable("derive.argv is not a list of at least 4 strings")
    if (argv[0] != "python3" or argv[1] != "-I" or (LANE / argv[2]).resolve() != HERE
            or argv[3] not in SUBCOMMANDS):
        raise Unevaluable(f"derive.argv is not `python3 -I {SELF} <{'|'.join(SUBCOMMANDS)}> ...`")
    run = list(argv)
    for k in range(4, len(argv)):
        flag, value = argv[k - 1], argv[k]
        if flag in REV_FLAGS:
            run[k] = pinned(value, measured)
        elif flag in SOURCE_FLAGS and value == statement_path:
            raise Unevaluable(f"derive reads the statement file {value} itself")
        elif flag == "--token" and not re.search(r"\b" + re.escape(value) + r"\b", statement_line):
            raise Unevaluable(f"--token {value} does not occur in the statement line")
    text = dv.get("extract_regex")
    m = EXTRACT_KEY.match(text) if isinstance(text, str) else None
    if not m or m.group(1) not in COUNT_KEYS[argv[3]]:
        raise Unevaluable(f"extract_regex must begin (?m)^<key>= with <key> in "
                          f"{','.join(COUNT_KEYS[argv[3]])}")
    return run, m.group(1)


def run_derive(dv, run):
    try:
        rx = re.compile(dv["extract_regex"])
    except re.error as exc:
        raise Unevaluable(f"extract_regex: {exc}") from None
    try:
        r = subprocess.run([sys.executable, "-I", str(HERE), *run[3:]], cwd=LANE,
                           stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, timeout=DERIVE_TIMEOUT)
    except subprocess.TimeoutExpired:
        raise Unevaluable(f"derive exceeded {DERIVE_TIMEOUT}s") from None
    if r.returncode != 0:
        err = r.stderr.decode("utf-8", errors="replace").strip().splitlines()
        raise Unevaluable(f"derive exited {r.returncode}: {err[-1] if err else ''}")
    found = list(rx.finditer(r.stdout.decode("utf-8", errors="replace")))
    if len(found) != 1:
        raise Unevaluable(f"extract_regex matched {len(found)} times, want 1")
    m = found[0]
    return parse_number(m.group("derived") if "derived" in rx.groupindex else m.group(1))


def check(registry, which, rev_arg, expect_mode):
    measured = None
    if rev_arg is not None:
        try:
            measured = commit(rev_arg)
        except Unevaluable as exc:
            print(f"TALLY_REGISTRY_ERROR: --rev: {exc}")
            return 2
    try:
        raw = Path(registry).read_bytes()
        reg = json.loads(raw)
        if not isinstance(reg, dict):
            raise ValueError("not a JSON object")
    except (OSError, ValueError) as exc:
        print(f"TALLY_REGISTRY_ERROR: {registry}: {exc}")
        return 2
    print(f"TALLY_REGISTRY: {registry} sha256={sha256(raw)} set={which} rev={measured or '-'}")
    entries = []
    for name in (("red", "green") if which == "all" else (which,)):
        group = reg.get(name, [])
        if not isinstance(group, list):
            print(f"TALLY_REGISTRY_ERROR: {registry}: {name!r} is not a list")
            return 2
        entries += [(name, e) for e in group]
    if not entries:
        print(f"TALLY_REGISTRY_ERROR: {registry}: no entries in set {which}")
        return 2
    seen, tally, met = set(), Counter(), 0
    for k, (name, e) in enumerate(entries, 1):
        e = e if isinstance(e, dict) else {}
        eid, stated, derived = e.get("id"), e.get("stated"), None
        where, run, key = "", None, None
        try:
            if not (isinstance(eid, str) and ID_SHAPE.fullmatch(eid)) or eid in seen:
                raise Unevaluable("id missing, malformed or duplicated")
            seen.add(eid)
            if not isinstance(stated, int) or isinstance(stated, bool):
                raise Unevaluable("stated is not an integer")
            rev, path, line, text, quoted = check_statement(e.get("statement"), measured)
            where = f"statement {path}:{line}@{rev}"
            if parse_number(quoted) != stated:
                raise Unevaluable(f"stated={stated} but the statement says {quoted!r}")
            run, key = derive_plan(e.get("derive"), measured, path, text)
            derived = run_derive(e["derive"], run)
            status = "MATCH" if derived == stated else "MISMATCH"
        except Unevaluable as exc:
            status, derived = "ERROR", None
            where = f"{where}; error: {exc}" if where else f"error: {exc}"
        tally[status] += 1
        met += status == EXPECT[name]
        label = eid if isinstance(eid, str) and ID_SHAPE.fullmatch(eid) else f"entry#{k}"
        print(f"{status} {label} stated={stated} derived={'none' if derived is None else derived}")
        print(f"  set={name} expect={EXPECT[name]} {where}"
              + (f" | key={key} | derive: {shlex.join(run)}" if run else ""))
    print(f"TALLY_SUMMARY: set={which} n={len(entries)} match={tally['MATCH']} "
          f"mismatch={tally['MISMATCH']} error={tally['ERROR']}")
    print(f"EXPECT_SUMMARY: {met}/{len(entries)}")
    if tally["ERROR"]:
        return 2
    if expect_mode:
        return 0 if met == len(entries) else 1
    return 1 if tally["MISMATCH"] else 0


def main(argv):
    if len(argv) > 1 and argv[1] in SUBCOMMANDS:
        p = argparse.ArgumentParser(prog="tally-check.py")
        sub = p.add_subparsers(dest="cmd", required=True)
        s = sub.add_parser("receipt-files")
        s.add_argument("--rev", required=True)
        s.add_argument("--path", required=True)
        s.add_argument("--schema", default="mado-tripwire-verdict-v1")
        s.set_defaults(run=cmd_receipt_files)
        s = sub.add_parser("pointer-token")
        s.add_argument("--counter", default=".ufo/waves/round-19/fresh-pins.py")
        s.add_argument("--counter-rev", required=True)
        s.add_argument("--rev", required=True)
        s.add_argument("--token", required=True)
        s.set_defaults(run=cmd_pointer_token)
        s = sub.add_parser("selftest-labels")
        s.add_argument("--path", default="tools/mado-verify.sh")
        s.add_argument("--function", default="selftest")
        s.add_argument("--fail-helper", default="st_bad")
        s.add_argument("--old", required=True)
        s.add_argument("--new", required=True)
        s.add_argument("--label-regex", required=True)
        s.set_defaults(run=cmd_selftest_labels)
        a = p.parse_args(argv[1:])
        try:
            a.run(a)
        except Unevaluable as exc:
            print(f"could_not_evaluate: {exc}", file=sys.stderr)
            return 2
        return 0
    p = argparse.ArgumentParser(prog="tally-check.py")
    p.add_argument("registry")
    p.add_argument("--set", choices=("all", "red", "green"), default="all")
    p.add_argument("--rev", help="the measured revision that REV stands for")
    p.add_argument("--expect", action="store_true",
                   help="exit 0 iff every entry lands on its set's side (red MISMATCH, green MATCH)")
    a = p.parse_args(argv[1:])
    return check(a.registry, a.set, a.rev, a.expect)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
