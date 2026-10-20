#!/usr/bin/env python3
"""mado-tripwire — post-hoc tripwire over OMP session transcripts (JSONL).

Classifies commands a seat *issued* in assistant `toolCall` blocks:
`bash` (arguments.command) and python `eval` (arguments.code: `!` shell
lines, `%%bash` cells and literal subprocess/os/tool.bash spawns parsed with
`ast`, never executed). Classes: host_mutation, package_query, live_probe,
tool_install, vcs_write. tool_install names tool-acquisition channels that are
not pacman: `uv tool install|upgrade|uninstall|run`, `uv pip install`, `uvx`,
`pip`/`pipN install`, `pipx install|inject|run|upgrade|reinstall|uninstall`,
`npx`, `npm exec|x`, `npm -g install|update|uninstall`, `cargo
install|uninstall` and `python -m pip ...`. It is a separate, permit-able
class and never host_mutation: `--permit tool_install` covers the whole class,
so the rule string (`uv:tool-install`, `pip:install`, `npx`, ...) is what
distinguishes one channel from another, and a `sudo` prefix on the same
command is still reported separately as host_mutation. Only the forms above
are classified; for example pnpm, yarn, bun, brew, nix, `uv sync`, `uv python
install`, `go install`, `gem install`, `cargo binstall`, `deno install -g`,
`uv run --with`, `pnpm dlx`, `npm --global=true` and plain downloads are not,
and variable indirection (`$UV tool install ...`) is invisible here, as is
the difference between a venv/`--user` install and a system one.

Limits (stated, not hidden):
- Detection after the fact only. It is not interception, prevention, a
  sandbox or host repair; it cannot stop a command and says nothing about
  commands outside the files it is given.
- "Issued" is not "executed": toolResult records are ignored on purpose
  (a successful harmful call and a refused one both count).
- `clean` means no finding in the covered forms. It never means "no host
  command ran": non-literal spawn arguments (counted as unparsed_spawns),
  JavaScript eval cells (eval_unparsed), scripts written then run, aliases,
  helpers defined in one text and called from another, python -c bodies,
  other tools and other sessions are not analysed. Pair a verdict with a
  /var/log/pacman.log window count.
- A function defined earlier in the SAME text and called there with literal
  arguments has its body classified with those arguments substituted: $1..$9
  and $@/$* for shell functions, positional parameters for python `def`.
  Nothing is substituted unless the call text states it literally, so a
  resolved finding names a command the transcript spells out. A helper body
  that is defined but never called is still read as before.
- A call to a bare name this text resolves neither to a same-text helper
  nor to a spawn function, handed a literal `['prog', ...]` argv list that
  classifies as a host command, is reported as a lead: the argv is stated
  outright, but whether that helper executes it is not visible, so a helper
  that only formats or logs that argv is reported too (an imported helper
  whose body lives in another file is a lead for the same reason). Pure
  data calls (`print`, `json.dumps`, ...) are exempt (PURE_ARG_CALLS); a
  call to a name this text DOES define contributes no lead when its
  arguments are not all literal, and only positional argv lists are read
  (a keyword `args=[...]` is a miss).
- Variable recipes are resolved only when the text fixes them: a name bound
  by a straight-line module-level assignment to a literal-only expression
  (str, `+`, two-argument `str.replace`, or a list of those), earlier in the
  same cell or in an earlier cell of the same py kernel in the same
  transcript (eval state persists; a `reset` cell, an exec/globals/import *
  statement from that point on, or any other binding forgets the name).
  Anything else stays unparsed_spawns. A shell function body defined in one
  text and called in another is not resolved.
- vcs_write covers version-control writes in a jj-colocated lane: `git` runs
  whose subcommand is add, commit, stash, checkout, switch, reset, pull,
  push, restore, rebase, merge or cherry-pick (rule `git:<sub>`; `stash
  list|show` stays clean), and `jj` runs that write or snapshot the working
  copy (rule `jj:<sub>`): the mutating subcommands commit, new, describe,
  squash, rebase, abandon, undo, edit, restore, split, duplicate, absorb,
  bookmark set/move/create/delete, op restore/revert and git push/fetch, and
  every other subcommand without an exact `--ignore-working-copy` token,
  because jj snapshots the working copy on all of them (`help` and
  `--version` excepted). A jj-lane.sh helper invocation is not a finding.
  Anything else on the `git` side (fetch, revert, tag, branch, clean,
  worktree, gc, config) and `git` subcommands hidden in aliases, shell
  functions or scripts are outside the class.
- shlex is not bash: exotic quoting can hide a command from the parser.
- Transcript text is data. Nothing in it is followed or executed.

CLI:
  mado-tripwire.py --scan PATH [PATH ...] [--permit CLASS ...]
  mado-tripwire.py --frozen DIR        (DIR/expected.json, digest-pinned replay)
  mado-tripwire.py --selftest DIR      (DIR/expected.json)
Exit: 0 no unpermitted finding (--scan) / pinned verdict reproduced
(--frozen); 1 at least one unpermitted finding / frozen verdict mismatch;
2 could-not-evaluate (usage, refused/unreadable path, no .jsonl, invalid
line, internal error; --frozen also: malformed expected.json, tampered or
unpinned snapshot). Exit 2 wins over 1.
First line: MADO_TRIPWIRE: clean | permitted_only | findings | could_not_evaluate
            MADO_TRIPWIRE_FROZEN: frozen_match | frozen_verdict_mismatch |
            frozen_error | snapshot_tampered | unpinned_legacy
--frozen proves a committed snapshot still reproduces the pinned verdict over
pinned bytes. It validates its pin before replay: inputs must be a non-empty
list of `inputs/<name>.jsonl` paths that resolve inside DIR (a symlinked
DIR/inputs, an escaping path, a leaf symlink or an unlisted `*.jsonl` is
snapshot_tampered), and every expected/known line must name a listed input,
be in range and non-blank, with no known-miss/expected overlap and a
reachable exit/label pair; an unreachable pin is frozen_error, never a failed
verdict. It does not prove the snapshot was copied faithfully from the
transcript it names: provenance is the snapshot author's claim, not checked.

--selftest DIR runs DIR/expected.json cases. A `mode: "frozen"` case needs
name, args (one DIR), want_exit and want_label, and may assert want_missing /
want_extra counts of the verdict's missing_findings / extra_findings (default
0); it also pins the verdict schema, outcome and exit, not only line 1.
"""
import ast
import hashlib
import json
import os
import re
import shlex
import stat
import subprocess
import sys
from collections import Counter

CLASSES = ("host_mutation", "package_query", "live_probe", "tool_install",
           "vcs_write")
SHELLS = {"bash", "sh", "zsh", "dash"}
ELEVATE = {"sudo", "doas", "pkexec", "run0"}
SUDO_ARG_OPTS = {"-u", "-g", "-h", "-p", "-C", "-D", "-r", "-t", "-U", "-T",
                 "--user", "--group", "--host", "--prompt", "--chdir"}
WRAPPERS = {"command", "exec", "nohup", "setsid", "builtin", "stdbuf"}
KEYWORDS = {"if", "then", "elif", "else", "fi", "for", "while", "until", "do",
            "done", "case", "esac", "time", "!", "{", "}", "function"}
SEPARATORS = {";", "&&", "||", "|", "&", "|&", ";;", "(", ")", "\n"}
REDIRECTS = {">", ">>", "<", "<<", "<<<", ">&", "<&", ">|", "&>", "&>>", "<>"}
XARGS_ARG_OPTS = {"-I", "-n", "-P", "-d", "-a", "-E", "-s", "-L", "-i", "--arg-file",
                  "--max-args", "--max-procs", "--delimiter", "--max-lines", "--max-chars",
                  "--eof", "--replace"}

JJ_WRITE = {"commit", "new", "describe", "squash", "rebase", "abandon", "undo",
            "edit", "restore", "split", "duplicate", "absorb"}
JJ_BOOKMARK_WRITE = {"set", "move", "create", "delete"}
JJ_OP_WRITE = {"restore", "revert"}
JJ_GIT_WRITE = {"push", "fetch"}
JJ_NO_SNAPSHOT = {"help", "version"}  # no working copy is read or written
JJ_ARG_OPTS = {"-R", "--repository", "--at-op", "--color", "--config",
               "--config-toml", "-T", "--template"}
JJ_SUB_ARG_OPTS = {"-r", "--revision", "-T", "--template", "--at-op", "--config",
                   "--color", "--repository", "-R"}
GIT_WRITE = {"add", "commit", "stash", "checkout", "switch", "reset", "pull",
             "push", "restore", "rebase", "merge", "cherry-pick"}
GIT_ARG_OPTS = {"-C", "-c", "--git-dir", "--work-tree", "--namespace",
                "--exec-path", "--super-prefix", "--config-env"}

SYSTEMCTL_QUERY = {"status", "show", "is-active", "is-enabled", "is-failed",
                   "is-system-running", "list-units", "list-unit-files",
                   "list-dependencies", "list-timers", "list-sockets",
                   "list-jobs", "list-machines", "cat", "get-default", "help",
                   "show-environment"}
SYSTEMCTL_ARG_OPTS = {"-t", "-p", "-n", "-H", "-M", "--type", "--property",
                      "--lines", "--host", "--machine", "--state"}
LOGINCTL_MUTATE = {"lock-session", "unlock-session", "lock-sessions",
                   "unlock-sessions", "terminate-session", "terminate-user",
                   "terminate-seat", "kill-session", "kill-user",
                   "enable-linger", "disable-linger", "activate", "attach",
                   "flush-devices"}
HYPRCTL_MUTATE = {"dispatch", "keyword", "reload", "kill", "setcursor",
                  "switchxkblayout", "seterror", "notify", "dismissnotify",
                  "plugin", "output", "setprop", "hyprpaper", "hyprsunset",
                  "eval"}
HYPRCTL_ARG_OPTS = {"-i", "--instance"}
OMARCHY_MUTATE = ("restart", "refresh", "install", "update", "remove",
                  "theme-set", "toggle", "launch", "pkg-", "lock", "wake", "reboot",
                  "shutdown", "logout", "-set", "reset", "setup", "snapshot", "sudo",
                  "hibernat", "config", "plymouth", "enable", "disable", "suspend")
HOST_MUTATION_BINS = {"pkill", "killall", "mkinitcpio", "bootctl",
                      "grub-mkconfig", "systemd-inhibit", "reboot", "poweroff",
                      "shutdown", "halt", "systemd-run", "su"}
PACKAGE_QUERY_BINS = {"expac", "pactree", "checkupdates", "pacman-conf"}
LIVE_PROBE_BINS = {"journalctl", "libinput", "evtest", "wayland-info", "wev",
                   "wlr-randr", "grim", "slurp", "hyprpicker", "busctl",
                   "dbus-send", "gdbus", "notify-send", "makoctl", "waybar",
                   "walker", "hypridle", "hyprlock", "alacritty", "pgrep",
                   "pidof", "xdg-terminal-exec", "wpctl", "brightnessctl",
                   "hyprpaper", "hyprsunset", "uwsm", "uwsm-app", "ps", "dmesg",
                   "wl-paste"}
PIP_RE = re.compile(r"^pip[0-9.]*$")
UV_ARG_OPTS = {"-C", "--directory", "--project", "--color", "--python", "-p",
               "--config-file", "--cache-dir", "--index-url",
               "--extra-index-url", "--find-links", "-f",
               "--allow-insecure-host", "--config-setting",
               "--python-preference"}
PIP_ARG_OPTS = {"--log", "--proxy", "--proxy-user", "--cert", "--client-cert",
                "--cache-dir", "--timeout", "--retries", "--exists-action",
                "--trusted-host", "--keyring-provider", "--use-feature",
                "--use-deprecated", "--python"}
PIPX_ARG_OPTS = {"--python", "-p", "--spec", "--pip-args", "--suffix",
                 "--backend"}
NPX_ARG_OPTS = {"-p", "--package", "-c", "--call", "--node-options",
                "--registry", "--cache"}
NPM_ARG_OPTS = {"--prefix", "--registry", "--userconfig", "--globalconfig",
                "--cache", "--loglevel", "--location", "--workspace", "-w",
                "--omit", "--include", "--otp", "--before", "--script-shell",
                "--tag"}
CARGO_ARG_OPTS = {"--color", "-Z", "--config", "--target-dir",
                  "--manifest-path", "--explain"}
SPAWN_FUNCS = {"run", "call", "check_call", "check_output", "Popen",
               "getoutput", "getstatusoutput"}
SHELL_STRING_FUNCS = {"os.system", "os.popen", "subprocess.getoutput",
                      "subprocess.getstatusoutput",
                      "asyncio.create_subprocess_shell"}
REFUSED_NAMES = re.compile(r"^agent\.db", re.I)  # only .jsonl files are ever opened
SECRET_PATTERNS = (
    re.compile(r"(?<=://)[^/\s:@]+:[^/\s@]+(?=@)"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"[A-Za-z0-9_\-]{32,}"),
)
MAX_COMMAND = 240


class CouldNotEvaluate(Exception):
    pass


NESTED = {"eval_unparsed": 0, "unparsed_spawns": 0}  # python bodies reached from shell


def nested_eval(code):
    hits, un_eval, un_spawn = classify_eval(code, "py")
    NESTED["eval_unparsed"] += un_eval
    NESTED["unparsed_spawns"] += un_spawn
    return hits


def redact(text):
    for pat in SECRET_PATTERNS:
        text = pat.sub("<redacted>", text)
    text = "".join(ch if ch.isprintable() or ch in "\n\t" else "?" for ch in text)
    return text[:MAX_COMMAND]


# ---------------------------------------------------------------- shell ---

def logical_lines(text):
    """Split a command string into logical lines.

    A line ends at a newline only when its quotes balance; backslash-newline
    joins lines; heredoc bodies are returned separately with their marker
    line so they are treated as data unless fed to a shell.
    """
    text = text.replace("\\\n", " ")
    raw = text.split("\n")
    out = []  # (line, heredoc_bodies)
    i = 0
    while i < len(raw):
        acc = raw[i]
        i += 1
        while True:
            try:
                shlex.split(acc, comments=True)
                break
            except ValueError:
                if i >= len(raw):
                    break
                acc += "\n" + raw[i]
                i += 1
        bodies = []
        for m in re.finditer(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1", acc):
            delim = m.group(2)
            body = []
            while i < len(raw):
                ln = raw[i]
                i += 1
                if ln.strip() == delim:
                    break
                body.append(ln)
            bodies.append("\n".join(body))
        out.append((acc, bodies))
    return out


def strip_comment(line):
    """Drop a bash comment: '#' at word start, outside quotes, not escaped."""
    quote = None
    i = 0
    while i < len(line):
        ch = line[i]
        if quote:
            if ch == "\\" and quote == '"':
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch == "\\":
            i += 2
            continue
        elif ch in ("'", '"'):
            quote = ch
        elif ch == "#" and (i == 0 or line[i - 1] in " \t\n;&|()<>"):
            return line[:i]
        i += 1
    return line


def tokenize(line):
    line = strip_comment(line)
    lex = shlex.shlex(line, posix=True, punctuation_chars=";&|()<>")
    lex.whitespace_split = True
    lex.whitespace = " \t\r"
    lex.commenters = ""  # comments removed quote-aware by strip_comment()
    return list(lex)


def segments(tokens):
    seg = []
    skip_next = False
    for i, tok in enumerate(tokens):
        if skip_next:
            skip_next = False
            continue
        nxt = tokens[i + 1] if i + 1 < len(tokens) else ""
        if tok.isdigit() and nxt and set(nxt) <= set("<>&"):
            continue  # file-descriptor number of a redirection (2>/dev/null)
        if tok in SEPARATORS or tok == "\n" or (tok and set(tok) <= set(";&|()") and
                                                 set(tok) & set(";|()")):
            if seg:
                yield seg
            seg = []
        elif tok in REDIRECTS or (tok and set(tok) <= set("<>&|")):
            skip_next = not tok.endswith("&") or tok in (">&", "<&")
        else:
            seg.append(tok)
    if seg:
        yield seg


def substitutions(line):
    """Bodies of $(...) and backticks outside single quotes."""
    found = []
    in_single = False
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == "'" and not in_single:
            j = line.find("'", i + 1)
            # a single quote inside double quotes is literal; approximate
            dq_before = line.count('"', 0, i) % 2 == 1
            if not dq_before:
                i = (j + 1) if j != -1 else len(line)
                continue
        if line.startswith("$(", i) and not line.startswith("$((", i):
            depth, j = 1, i + 2
            while j < len(line) and depth:
                if line[j] == "(":
                    depth += 1
                elif line[j] == ")":
                    depth -= 1
                j += 1
            found.append(line[i + 2:j - 1])
            i = j
            continue
        if ch == "`":
            j = line.find("`", i + 1)
            if j != -1:
                found.append(line[i + 1:j])
                i = j + 1
                continue
        i += 1
    return found


def strip_prefix(seg):
    seg = list(seg)
    changed = True
    while seg and changed:
        changed = False
        head = seg[0]
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", head) or head in KEYWORDS:
            seg.pop(0)
            if head == "time":
                while seg and seg[0] in ("-p", "--"):
                    seg.pop(0)
            changed = True
            continue
        base = os.path.basename(head)
        if base == "command" and len(seg) > 1 and seg[1] in ("-v", "-V"):
            return []  # lookup only, nothing is executed
        if base in WRAPPERS:
            seg.pop(0)
            while seg and seg[0].startswith("-") and seg[0] != "--":
                opt = seg.pop(0)
                if (base == "exec" and opt == "-a") or (base == "stdbuf" and opt in ("-i", "-o", "-e")):
                    if seg:
                        seg.pop(0)
            if seg and seg[0] == "--":
                seg.pop(0)
            changed = True
        elif base == "env":
            seg.pop(0)
            while seg and (seg[0].startswith("-") or re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", seg[0])):
                opt = seg.pop(0)
                if opt == "--":
                    break
                if opt in ("-S", "--split-string") and seg:
                    try:
                        seg = shlex.split(seg.pop(0)) + seg  # payload is a command line
                    except ValueError:
                        pass
                    break
                if opt.startswith("--split-string="):
                    try:
                        seg = shlex.split(opt.split("=", 1)[1]) + seg
                    except ValueError:
                        pass
                    break
                if opt in ("-u", "-C", "--unset", "--chdir") and seg:
                    seg.pop(0)
            changed = True
        elif base == "nice":
            seg.pop(0)
            if seg and seg[0] in ("-n", "--adjustment") and len(seg) > 1:
                seg = seg[2:]
            elif seg and (re.match(r"^-\d+$", seg[0]) or re.match(r"^-n-?\d+$", seg[0])
                          or seg[0].startswith("--adjustment=")):
                seg.pop(0)
            changed = True
        elif base == "ionice":
            seg.pop(0)
            while seg and seg[0].startswith("-"):
                opt = seg.pop(0)
                if opt in ("-c", "-n", "-p") and seg:
                    seg.pop(0)
            changed = True
        elif base == "timeout":
            seg.pop(0)
            while seg and seg[0].startswith("-"):
                opt = seg.pop(0)
                if opt in ("-s", "-k", "--signal", "--kill-after") and seg:
                    seg.pop(0)
            if seg and seg[0] == "--":
                seg.pop(0)
            if seg:
                seg.pop(0)  # duration
            if seg and seg[0] == "--":
                seg.pop(0)
            changed = True
        elif base == "xargs":
            seg.pop(0)
            while seg and seg[0].startswith("-"):
                opt = seg.pop(0)
                if opt in XARGS_ARG_OPTS and seg:
                    seg.pop(0)
            changed = True
        elif base == "flock":
            seg.pop(0)
            payload = None
            while seg and seg[0].startswith("-"):
                opt = seg.pop(0)
                if opt in ("-w", "-E", "--timeout", "--conflict-exit-code") and seg:
                    seg.pop(0)
            if seg:
                seg.pop(0)  # lock file or fd
            if seg and seg[0] in ("-c", "--command") and len(seg) > 1:
                payload = seg[1]
            if payload is not None:
                try:
                    seg = shlex.split(payload)
                except ValueError:
                    seg = payload.split()
            changed = True
    return seg


def first_verb(args, arg_opts):
    skip = False
    for a in args:
        if skip:
            skip = False
            continue
        if a in arg_opts:
            skip = True
            continue
        if a.startswith("-"):
            continue
        return a
    return None


def sub_verb(args, verb):
    """First positional after `verb`, skipping flags and their argument values."""
    try:
        rest = args[args.index(verb) + 1:]
    except ValueError:
        return None
    skip = False
    for a in rest:
        if skip:
            skip = False
            continue
        if a in JJ_SUB_ARG_OPTS:
            skip = True
            continue
        if a.startswith("-"):
            continue
        return a
    return None


def ignores_working_copy(args):
    """True when an exact --ignore-working-copy precedes any `--` separator."""
    head = args[:args.index("--")] if "--" in args else args
    return "--ignore-working-copy" in head


def classify_jj(args):
    """Rule for a `jj` run that writes or snapshots the working copy, else None."""
    verb = first_verb(args, JJ_ARG_OPTS)
    if verb is None:  # `jj`, `jj --version`, `jj --help`: nothing is touched
        return None
    if verb in JJ_WRITE:
        return "jj:" + verb
    if verb == "bookmark":
        if sub_verb(args, verb) in JJ_BOOKMARK_WRITE:
            return "jj:bookmark"
    elif verb == "op":
        if sub_verb(args, verb) in JJ_OP_WRITE:
            return "jj:op"
    elif verb == "git":
        if sub_verb(args, verb) in JJ_GIT_WRITE:
            return "jj:git"
    elif verb in JJ_NO_SNAPSHOT:
        return None
    return None if ignores_working_copy(args) else "jj:" + verb


def classify_git(args):
    """Rule for a `git` write, else None (reads and unclassified subcommands)."""
    verb = first_verb(args, GIT_ARG_OPTS)
    if verb == "stash" and sub_verb(args, verb) in ("list", "show"):
        return None  # read-only stash inspection
    return "git:" + verb if verb in GIT_WRITE else None


def classify_pacman(argv0, args):
    op = None
    long_ops = {"--sync": "S", "--query": "Q", "--remove": "R",
                "--upgrade": "U", "--database": "D", "--files": "F",
                "--deptest": "T", "--version": "V"}
    for a in args:
        if a.startswith("--"):
            name = a.split("=", 1)[0]
            hits = [k for k in long_ops if k.startswith(name)] if len(name) > 3 else []
            if len(hits) == 1 and op is None:  # getopt_long accepts unique prefixes
                op = (a, long_ops[hits[0]])
        elif a.startswith("-") and len(a) > 1 and a[1:].isalpha():
            letters = [c for c in a[1:] if c.isupper()]
            if letters and op is None:
                op = (a, letters[0])
    flags = set()
    for a in args:
        if a.startswith("-") and not a.startswith("--") and a[1:].isalpha():
            flags.update(a[1:])
        elif a in ("--refresh", "--sysupgrade", "--downloadonly", "--clean"):
            flags.add({"--refresh": "y", "--sysupgrade": "u",
                       "--downloadonly": "w", "--clean": "c"}[a])
        elif a in ("--print", "--search", "--info", "--list", "--groups"):
            flags.add({"--print": "p", "--search": "s", "--info": "i",
                       "--list": "l", "--groups": "g"}[a])
    if op is None:
        # Fail safe: an operator the parser could not read (`-$o`, `--typo`,
        # bare `pacman`) must never land in a permitted class.
        return ("host_mutation", argv0)
    tok, letter = op
    rule = "%s:%s" % (argv0, tok)
    if letter == "F" and "y" in flags:
        return ("host_mutation", rule)  # -Fy refreshes the files database
    if letter in ("Q", "F", "T", "V"):
        return ("package_query", rule)
    if letter in ("R", "U", "D"):
        return ("host_mutation", rule)
    if letter == "S":
        if flags & set("yuwc"):
            return ("host_mutation", rule)
        if flags & set("silgp"):
            return ("package_query", rule)
        return ("host_mutation", rule)
    return ("host_mutation", rule)


SHELL_IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
SHELL_EXPANSION = re.compile(r"[$\x60*?\[{~\n]")


def last_unquoted(text, target):
    """Index of the last occurrence of target outside quotes, or -1."""
    quote, i, last = None, 0, -1
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == "\\" and quote == '"':
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch == "\\":
            i += 2
            continue
        elif ch in ("'", '"'):
            quote = ch
        elif ch == target:
            last = i
        i += 1
    return last


def heredoc_attached(line, bodies):
    """A raw line with its heredoc bodies and delimiters put back in place.

    `logical_lines` returns a heredoc body beside its marker line; a function
    body rebuilt from marker lines alone would re-parse the marker and swallow
    the following body lines as a bogus heredoc.
    """
    for m, body in zip(re.finditer(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1", line), bodies):
        line += "\n" + body + "\n" + m.group(2)
    return line


def shell_functions(pairs):
    """Definitions visible in one command text: {name: (start, body_text)}.

    Only `name() { ... }` and `function name { ... }` are read, only when the
    closing `}` is present in the same text, and a name defined twice is
    dropped: neither its body nor its call site is then interpreted. The body
    is the raw text between the braces: token text would lose quoting, and a
    body re-parsed without its quotes splits `python3 -c "...; ..."` and
    `sh -c '...'` into words bash never saw.
    """
    funcs, dup = {}, set()
    i = 0
    while i < len(pairs):
        line = pairs[i][0]
        try:
            toks = tokenize(line) if line.strip() else []
        except ValueError:
            i += 1
            continue
        name = None
        if toks and toks[0] == "function" and len(toks) > 1 and SHELL_IDENT.match(toks[1]):
            name = toks[1]
        elif len(toks) > 1 and SHELL_IDENT.match(toks[0]) and toks[1] in ("()", "("):
            after = toks[1:]
            if after[:1] == ["()"]:
                after = after[1:]
            elif after[:2] == ["(", ")"]:
                after = after[2:]
            else:
                after = None
            if after is not None and after[:1] == ["{"]:
                name = toks[0]
        if name is None:
            i += 1
            continue
        raw = strip_comment(line)
        m = re.match(r"^\s*(?:function\s+)?%s\s*(?:\(\s*\))?\s*\{" % re.escape(name), raw)
        if not m:
            i += 1  # tokens and raw text disagree: no body, never a guess
            continue
        start = i
        end = len(raw.rstrip())
        if end and raw.rstrip().endswith("}") and last_unquoted(raw, "}") == end - 1:
            body = raw[m.end():end - 1]
            i += 1
        else:
            head = heredoc_attached(raw[m.end():], pairs[i][1])
            parts = [head] if head.strip() else []
            j, closed = i + 1, False
            while j < len(pairs):
                ln, bodies2 = pairs[j]
                try:
                    t2 = tokenize(ln) if ln.strip() else []
                except ValueError:
                    t2 = ln.split()
                rawln = strip_comment(ln).rstrip()
                if (t2 and t2[-1] == "}" and rawln.endswith("}")
                        and last_unquoted(rawln, "}") == len(rawln) - 1):
                    if rawln[:-1].strip():
                        parts.append(rawln[:-1])
                    closed = True
                    break
                parts.append(heredoc_attached(ln, bodies2))
                j += 1
            if not closed:
                i += 1
                continue
            body = "\n".join(parts)
            i = j + 1
        if name in funcs:
            dup.add(name)
        funcs[name] = (start, body)
    for name in dup:
        funcs.pop(name, None)
    return funcs


def shell_expand(body, args):
    """Substitute literal positional arguments into a function body.

    $1..$9 and $@/$* are replaced outside single quotes (bash never expands
    there); inside double quotes the value is inserted unquoted, elsewhere it
    is shell-quoted. A positional the call did not supply yields None.
    """
    out, i, quote = [], 0, None
    words = " ".join(shlex.quote(a) for a in args)
    body = body.replace('"$@"', words).replace('"${@}"', words)  # one word per argument
    while i < len(body):
        ch = body[i]
        if quote == "'":
            if ch == "'":
                quote = None
            out.append(ch)
            i += 1
            continue
        if ch == "\\" and i + 1 < len(body):
            out.append(body[i:i + 2])
            i += 2
            continue
        if ch in ("'", '"'):
            quote = None if ch == quote else (ch if quote is None else quote)
            out.append(ch)
            i += 1
            continue
        if ch == "$":
            m = re.match(r"\$(?:\{([0-9]+|[@*])\}|([0-9@*]))", body[i:])
            if m:
                key = m.group(1) or m.group(2)
                if key in ("@", "*"):
                    out.append(shlex.join(args))
                elif 1 <= int(key) <= len(args):
                    val = args[int(key) - 1]
                    out.append(val if quote == '"' else shlex.quote(val))
                else:
                    return None
                i += m.end()
                continue
        out.append(ch)
        i += 1
    return "".join(out)


def leading_tokens(args, arg_opts, count):
    """First `count` non-option tokens as (index, token), skipping option values."""
    out = []
    skip = False
    for i, a in enumerate(args):
        if skip:
            skip = False
            continue
        if a == "--":
            break  # operands after -- are not verbs
        if a in arg_opts:
            skip = True
            continue
        if a.startswith("-"):
            continue
        out.append((i, a))
        if len(out) >= count:
            break
    return out


def has_operand(args, arg_opts):
    """True if a non-option token remains once option values and flags are skipped."""
    skip = False
    for i, a in enumerate(args):
        if skip:
            skip = False
            continue
        if a == "--":
            return i + 1 < len(args)
        if a in arg_opts:
            skip = True
            continue
        if a.startswith("-"):
            continue
        return True
    return False


def package_run(args):
    """True for a package-run form: a `--package`/`-p` selector or a trailing operand."""
    return any(a in ("-p", "--package") for a in args) or has_operand(args, NPX_ARG_OPTS)


def npm_global(args):
    for i, a in enumerate(args):
        if a in ("--global", "--location=global"):
            return True
        if a == "--location" and i + 1 < len(args) and args[i + 1] == "global":
            return True
        if a == "-g" or (a.startswith("-") and not a.startswith("--")
                         and a[1:].isalpha() and "g" in a[1:]):
            return True
    return False


def classify_installer(argv0, args):
    """Return (class, rule) for a tool-acquisition channel, else None.

    Only the argv0-level forms named in the module docstring are classified;
    same-channel tools (pnpm, yarn, bun, brew, nix) are deliberately not.
    """
    if argv0 == "uv":
        verbs = [v for _, v in leading_tokens(args, UV_ARG_OPTS, 2)]
        if len(verbs) == 2 and verbs[0] == "tool" and verbs[1] in (
                "install", "upgrade", "uninstall", "run"):
            return ("tool_install", "uv:tool-%s" % verbs[1])
        if verbs[:2] == ["pip", "install"]:
            return ("tool_install", "uv:pip-install")
        return None
    if argv0 == "uvx":
        return ("tool_install", "uvx") if has_operand(args, NPX_ARG_OPTS) else None
    if PIP_RE.match(argv0):
        verbs = [v for _, v in leading_tokens(args, PIP_ARG_OPTS, 1)]
        if verbs == ["install"]:
            return ("tool_install", "%s:install" % argv0)
        return None
    if argv0 == "pipx":
        verbs = [v for _, v in leading_tokens(args, PIPX_ARG_OPTS, 1)]
        if verbs and verbs[0] in ("install", "inject", "run", "upgrade",
                                  "reinstall", "uninstall"):
            return ("tool_install", "pipx:%s" % verbs[0])
        return None
    if argv0 == "npx":
        return ("tool_install", "npx") if package_run(args) else None
    if argv0 == "npm":
        lead = leading_tokens(args, NPM_ARG_OPTS, 1)
        verb = lead[0][1] if lead else None
        rest = args[lead[0][0] + 1:] if lead else []
        if verb in ("exec", "x"):
            return ("tool_install", "npm:exec") if package_run(rest) else None
        if verb in ("install", "i", "add"):
            return ("tool_install", "npm:install-global") if npm_global(args) else None
        if verb in ("update", "up", "upgrade"):
            return ("tool_install", "npm:update-global") if npm_global(args) else None
        if verb in ("uninstall", "unlink", "remove", "rm", "un", "r"):
            return ("tool_install", "npm:uninstall-global") if npm_global(args) else None
        return None
    if argv0 == "cargo":
        rest = list(args)
        while rest and re.fullmatch(r"\+[A-Za-z0-9_.-]+", rest[0]):
            rest = rest[1:]  # rustup toolchain override precedes the subcommand
        verbs = [v for _, v in leading_tokens(rest, CARGO_ARG_OPTS, 1)]
        verb = verbs[0] if verbs else None
        if verb == "install" and "--list" not in rest:
            return ("tool_install", "cargo:install")
        if verb == "uninstall":
            return ("tool_install", "cargo:uninstall")
        return None
    return None


def classify_shell(text, depth=0):
    """Return a list of (class, rule, argv0, segment_text, unparsed)."""
    if depth > 8 or not text or not text.strip():
        return []
    pairs = logical_lines(text)
    funcs = shell_functions(pairs)
    out = []
    for idx, (line, bodies) in enumerate(pairs):
        unparsed = False
        try:
            toks = tokenize(line)
        except ValueError:
            toks = line.split()
            unparsed = True
        fed_to_shell = False
        fed_to_python = False
        for seg in segments(toks):
            out.extend(classify_segment(seg, depth, unparsed))
            s = strip_prefix(seg)
            base = os.path.basename(s[0]) if s else ""
            defn = funcs.get(base)
            if (defn is not None and idx > defn[0] and len(s) > 1
                    and not any(SHELL_EXPANSION.search(a) for a in s[1:])):
                expanded = shell_expand(defn[1], s[1:])
                if expanded is not None:
                    out.extend(classify_shell(expanded, depth + 1))
            if base in SHELLS and not any(
                    a.startswith("-") and "c" in a and not a.startswith("--") for a in s[1:]):
                fed_to_shell = True
            if re.fullmatch(r"python[0-9.]*", base) and (
                    "-" in s[1:] or not [a for a in s[1:] if not a.startswith("-")]):
                fed_to_python = True
        for inner in substitutions(line):
            out.extend(classify_shell(inner, depth + 1))
        for body in bodies:
            if fed_to_shell:
                out.extend(classify_shell(body, depth + 1))
            elif fed_to_python:
                out.extend(nested_eval(body))
    return out


def classify_segment(seg, depth, unparsed):
    seg = strip_prefix(seg)
    if not seg:
        return []
    argv0 = os.path.basename(seg[0])
    args = seg[1:]
    text = " ".join(seg)
    suffix = "/unparsed" if unparsed else ""
    hits = []

    def hit(cls, rule):
        hits.append((cls, rule + suffix, argv0, text))

    if argv0 in ELEVATE:
        hit("host_mutation", argv0)
        rest = list(args)
        while rest and rest[0].startswith("-"):
            opt = rest.pop(0)
            if opt == "--":
                break
            if opt in SUDO_ARG_OPTS and rest:
                rest.pop(0)
        if rest:
            hits.extend(classify_segment(rest, depth + 1, unparsed))
        return hits
    if argv0 == "su":
        hit("host_mutation", "su")
        if "-c" in args and args.index("-c") + 1 < len(args):
            hits.extend(classify_shell(args[args.index("-c") + 1], depth + 1))
        return hits
    if argv0 == "systemd-run":
        hit("host_mutation", "systemd-run")
        rest = list(args)
        while rest and rest[0].startswith("-"):
            opt = rest.pop(0)
            if opt in ("-p", "-u", "-E", "-M", "-H", "--property", "--unit") and rest:
                rest.pop(0)
        if rest:
            hits.extend(classify_segment(rest, depth + 1, unparsed))
        return hits
    if argv0 in SHELLS:
        for idx, a in enumerate(args):
            if a.startswith("-") and not a.startswith("--") and "c" in a:
                if idx + 1 < len(args):
                    hits.extend(classify_shell(args[idx + 1], depth + 1))
                break
        return hits
    if argv0 == "eval":
        return classify_shell(" ".join(args), depth + 1)
    if re.fullmatch(r"python[0-9.]*", argv0):
        # -c/-m is an interpreter option; the first operand (a script) ends
        # options. Reading -m anywhere in argv misreads a script's arguments
        # (`python3 tool.py -m ps` is not `python3 -m ps`).
        i = 0
        while i < len(args):
            a = args[i]
            if a in ("-W", "-X", "--check-hash-based-pycs"):
                i += 2
                continue
            if a.startswith("-m") and not a.startswith("--"):
                mod, rest = (a[2:], args[i + 1:]) if len(a) > 2 else (
                    (args[i + 1], args[i + 2:]) if i + 1 < len(args) else (None, []))
                if mod:
                    hits.extend(classify_segment([mod] + rest, depth + 1, unparsed))
                return hits
            if a.startswith("-c") and not a.startswith("--"):
                code = a[2:] if len(a) > 2 else (
                    args[i + 1] if i + 1 < len(args) else None)
                return hits + (nested_eval(code) if code else [])
            if not a.startswith("-") or a == "-":
                break
            i += 1
        if "-c" in args:  # legacy: a -c after a script operand was always read
            j = args.index("-c")
            if j + 1 < len(args):
                return hits + nested_eval(args[j + 1])
        return hits
    if argv0 == "jj":
        rule = classify_jj(args)
        if rule is not None:
            hit("vcs_write", rule)
        return hits
    if argv0 == "git":
        rule = classify_git(args)
        if rule is not None:
            hit("vcs_write", rule)
        return hits
    if argv0 in ("pacman", "yay", "paru"):
        cls, rule = classify_pacman(argv0, args)
        hit(cls, rule)
        return hits
    if argv0 in PACKAGE_QUERY_BINS:
        hit("package_query", argv0)
        return hits
    if argv0 == "paccache":
        hit("package_query" if "-d" in args or "--dryrun" in args else "host_mutation", argv0)
        return hits
    if argv0 == "makepkg":
        if any(a in ("-i", "--install", "-s", "--syncdeps") or
               (a.startswith("-") and not a.startswith("--") and ("i" in a or "s" in a))
               for a in args):
            hit("host_mutation", argv0)
        return hits
    found = classify_installer(argv0, args)
    if found is not None:
        hit(*found)
        return hits
    if argv0 == "systemctl":
        verb = first_verb(args, SYSTEMCTL_ARG_OPTS)
        if verb is None or verb in SYSTEMCTL_QUERY:
            hit("live_probe", "systemctl:%s" % (verb or "list-units"))
        else:
            hit("host_mutation", "systemctl:%s" % verb)
        return hits
    if argv0 == "loginctl":
        verb = first_verb(args, {"-H", "-M", "-n", "-p", "-P", "-o", "--host", "--machine",
                                 "--lines", "--property", "--output", "--signal", "-s"})
        hit("host_mutation" if verb in LOGINCTL_MUTATE else "live_probe",
            "loginctl:%s" % (verb or "list-sessions"))
        return hits
    if argv0 == "hyprctl":
        if "--batch" in args:
            i = args.index("--batch")
            if i + 1 < len(args):
                for part in args[i + 1].split(";"):
                    if part.strip():
                        hits.extend(classify_segment(["hyprctl"] + part.split(), depth + 1, unparsed))
            return hits
        verb = first_verb(args, HYPRCTL_ARG_OPTS)
        hit("host_mutation" if verb in HYPRCTL_MUTATE else "live_probe",
            "hyprctl:%s" % (verb or "help"))
        return hits
    if argv0 == "kill":
        if args and args[0] in ("-0", "-l", "-L", "--list", "-s0"):
            return hits  # existence test or signal listing only (first argument)
        hit("host_mutation", "kill")
        return hits
    if argv0 in HOST_MUTATION_BINS:
        hit("host_mutation", argv0)
        return hits
    if argv0 == "omarchy":
        hit("host_mutation", "omarchy")  # dispatcher: routes to arbitrary omarchy-* helpers
        return hits
    if argv0.startswith("omarchy-"):
        hit("host_mutation" if any(k in argv0 for k in OMARCHY_MUTATE) else "live_probe", argv0)
        return hits
    if argv0 in LIVE_PROBE_BINS:
        hit("live_probe", argv0)
        return hits
    return hits


# ----------------------------------------------------------------- eval ---

def dotted(node):
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
        return ".".join(reversed(parts))
    if isinstance(node, ast.Await):
        return dotted(node.value)
    return None


LITERAL_MISS = object()
OPAQUE_PY_CALLS = {"exec", "eval", "globals", "locals", "vars", "__import__",
                   "compile", "setattr", "delattr"}
OPAQUE_PY_DOTTED = OPAQUE_PY_CALLS | {"builtins." + n for n in OPAQUE_PY_CALLS}
MATCH_BINDERS = tuple(getattr(ast, n) for n in ("MatchAs", "MatchStar", "MatchMapping")
                      if hasattr(ast, n))
TYPE_ALIAS = getattr(ast, "TypeAlias", None)


def target_names(target):
    """Names a binding target assigns; attribute/subscript targets bind none."""
    if isinstance(target, ast.Name):
        return {target.id}
    if isinstance(target, (ast.Tuple, ast.List)):
        names = set()
        for elt in target.elts:
            names |= target_names(elt)
        return names
    if isinstance(target, ast.Starred):
        return target_names(target.value)
    return set()


def module_binding(stmt):
    """The single-name straight-line module assignment in stmt, else None."""
    if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and \
            isinstance(stmt.targets[0], ast.Name):
        return stmt.targets[0].id, stmt.value
    if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name) and \
            stmt.value is not None:
        return stmt.target.id, stmt.value
    return None


def literal_value(node, env):
    """The literal value an expression denotes, else LITERAL_MISS.

    The one resolver both consumers share: module-level variable recipes
    (spawn arguments, folded against the cell environment) and same-text
    helper arguments (folded against bound parameters). Only shapes whose
    value the text itself fixes are folded: a str/int/float/bool/None
    constant, a resolvable name, str + str, a two-argument str.replace on
    resolvable strings, and a list/tuple of folded values. Anything else is
    LITERAL_MISS and the caller counts the spawn as unparsed, never guesses.
    """
    if isinstance(node, ast.Constant) and (
            node.value is None or isinstance(node.value, (str, int, float, bool))):
        return node.value
    if isinstance(node, ast.Name):
        return env.get(node.id, LITERAL_MISS)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left, right = literal_value(node.left, env), literal_value(node.right, env)
        if isinstance(left, str) and isinstance(right, str):
            return left + right
        return LITERAL_MISS
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and \
            node.func.attr == "replace" and len(node.args) == 2 and not node.keywords:
        base = literal_value(node.func.value, env)
        old, new = literal_value(node.args[0], env), literal_value(node.args[1], env)
        if isinstance(base, str) and isinstance(old, str) and isinstance(new, str):
            return base.replace(old, new)
        return LITERAL_MISS
    if isinstance(node, (ast.List, ast.Tuple)):
        values = [literal_value(elt, env) for elt in node.elts]
        if all(v is not LITERAL_MISS for v in values):
            return values
    return LITERAL_MISS


def argv_strings(value):
    """The strings of a folded literal argv list/tuple, else None."""
    if isinstance(value, list) and value and all(isinstance(v, str) for v in value):
        return value
    return None


def module_unsafe_names(tree):
    """Module-level names whose value cannot be tracked by straight-line
    assignment: conditional/loop/tuple/augmented/import/del/walrus targets,
    scope definitions, comprehension targets and global/nonlocal aliases."""
    simple = {id(stmt) for stmt in tree.body if module_binding(stmt) is not None}
    unsafe = set()

    def scan(node):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                unsafe.add(child.name)
                for inner in ast.walk(child):  # a `global x` in any scope rebinds x
                    if isinstance(inner, (ast.Global, ast.Nonlocal)):
                        unsafe.update(inner.names)
                continue  # other body bindings are local to that scope
            if isinstance(child, ast.Lambda):
                continue
            if isinstance(child, ast.Assign):
                if id(child) not in simple:
                    for target in child.targets:
                        unsafe.update(target_names(target))
            elif isinstance(child, ast.AnnAssign):
                if id(child) not in simple:
                    unsafe.update(target_names(child.target))
            elif isinstance(child, ast.AugAssign):
                unsafe.update(target_names(child.target))
            elif isinstance(child, (ast.For, ast.AsyncFor, ast.comprehension)):
                unsafe.update(target_names(child.target))
            elif isinstance(child, ast.withitem) and child.optional_vars is not None:
                unsafe.update(target_names(child.optional_vars))
            elif isinstance(child, ast.ExceptHandler) and child.name:
                unsafe.add(child.name)
            elif isinstance(child, (ast.Import, ast.ImportFrom)):
                for alias in child.names:
                    if alias.name != "*":
                        unsafe.add(alias.asname or alias.name.split(".")[0])
            elif isinstance(child, ast.Delete):
                for target in child.targets:
                    unsafe.update(target_names(target))
            elif isinstance(child, ast.NamedExpr):
                unsafe.update(target_names(child.target))
            elif isinstance(child, (ast.Global, ast.Nonlocal)):
                unsafe.update(child.names)
            elif MATCH_BINDERS and isinstance(child, MATCH_BINDERS):
                name = getattr(child, "name", None) or getattr(child, "rest", None)
                if name:
                    unsafe.add(name)
            elif TYPE_ALIAS is not None and isinstance(child, TYPE_ALIAS):
                unsafe.add(child.name.id)
            scan(child)

    scan(tree)
    return unsafe


def scoped_call_ids(tree):
    """Ids of calls lexically inside a def/lambda body or a class body.

    Those run later (or in another namespace), so the module-level value at
    the definition point need not be the value they see: only literals
    written inside the call itself are resolved for them.
    """
    ids = set()

    def defer(nodes):
        for node in nodes:
            for inner in ast.walk(node):
                if isinstance(inner, ast.Call):
                    ids.add(id(inner))

    def scan(node):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                defer(child.body)
            elif isinstance(child, ast.Lambda):
                defer([child.body])
            elif isinstance(child, ast.ClassDef):
                defer(child.body)
            else:
                scan(child)

    scan(tree)
    return ids


def opaque_module_mutation(tree):
    """True when eager module/class-scope code can rebind names behind the
    resolver's back (exec/eval/globals/locals/vars/builtins or import *)."""
    def scan(node):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
                continue
            if isinstance(child, ast.ImportFrom) and any(a.name == "*" for a in child.names):
                return True
            if isinstance(child, ast.Call) and (dotted(child.func) or "") in OPAQUE_PY_DOTTED:
                return True
            if scan(child):
                return True
        return False

    return scan(tree)


def opaque_statement(stmt):
    """True when stmt itself, executed in order, rebinds names for what follows.

    A def only defines a name (its body runs later, if at all), so it clears
    nothing; every other statement is walked for the same eager rebinding the
    whole-cell check looked for, so a class body's exec still counts.
    """
    if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
        return False
    if isinstance(stmt, ast.ImportFrom) and any(a.name == "*" for a in stmt.names):
        return True
    return opaque_module_mutation(stmt)


PURE_ARG_CALLS = {  # never spawns: never report a literal argv list handed to it
    "print", "list", "tuple", "set", "dict", "sorted", "reversed", "repr", "str",
    "bytes", "len", "any", "all", "min", "max", "sum", "enumerate", "zip", "map",
    "filter", "open", "exec", "eval", "compile", "isinstance", "getattr", "hasattr",
    "setattr", "iter", "next", "input",
}


def bind_literal(fn, call, env=None):
    """Bind a same-text `def` helper's parameters to literal call arguments.

    Arguments are folded with the shared resolver against `env`, which holds
    only parameters bound by an enclosing same-text helper call: a module
    variable is never substituted into a helper body, so a binding always
    names an argument the call text itself states. Defaults are folded at the
    definition site, where no call parameter is in scope.
    """
    env = {} if env is None else env
    if fn.args.vararg or fn.args.kwarg or any(isinstance(a, ast.Starred) for a in call.args):
        return None
    params = [a.arg for a in fn.args.posonlyargs + fn.args.args]
    if len(call.args) > len(params):
        return None
    bound = {}
    for name, node in zip(params, call.args):
        value = literal_value(node, env)
        if value is LITERAL_MISS:
            return None
        bound[name] = value
    for k in call.keywords:
        if k.arg is None or k.arg not in params or k.arg in bound:
            return None
        value = literal_value(k.value, env)
        if value is LITERAL_MISS:
            return None
        bound[k.arg] = value
    first_default = len(params) - len(fn.args.defaults)
    for idx, name in enumerate(params):
        if name in bound:
            continue
        if idx < first_default:
            return None  # a required parameter the call does not state
        value = literal_value(fn.args.defaults[idx - first_default], {})
        if value is LITERAL_MISS:
            return None
        bound[name] = value
    return bound


def classify_eval(code, language, env=None):
    """Return (hits, eval_unparsed, unparsed_spawns).

    `env` is the literal environment of the transcript's py kernel (one dict
    per scanned file); it is updated in place so a later eval cell resolves a
    name an earlier cell bound, and it is the environment spawn arguments are
    folded against. A name entered here was bound by exactly one
    straight-line module-level assignment to a literal-only expression.
    """
    if language and language not in ("py", "python"):
        return [], 1, 0
    hits = []
    lines = code.split("\n")
    if lines and lines[0].strip().startswith("%%bash"):
        return classify_shell("\n".join(lines[1:])), 0, 0
    py = []
    for ln in lines:
        s = ln.strip()
        m = re.match(r"^\s*(?:[A-Za-z_][A-Za-z0-9_]*\s*=\s*)?!(.*)$", ln)
        if m and not s.startswith("!="):
            hits.extend(classify_shell(m.group(1)))
            py.append(re.match(r"^\s*", ln).group(0) + "pass")
        elif s.startswith("%"):
            py.append(re.match(r"^\s*", ln).group(0) + "pass")
        else:
            py.append(ln)
    try:
        tree = compile("\n".join(py), "<eval>", "exec",
                       flags=ast.PyCF_ONLY_AST | ast.PyCF_ALLOW_TOP_LEVEL_AWAIT,
                       dont_inherit=True)
    except Exception:  # SyntaxError, ValueError, MemoryError, RecursionError: never executed
        return hits, 1, 0
    if env is None:
        env = {}
    unsafe = module_unsafe_names(tree)
    for name in unsafe:
        env.pop(name, None)
    scoped = scoped_call_ids(tree)
    from_subprocess = set()
    aliases = {"sp": "subprocess"}  # bound name -> canonical dotted prefix
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name in ("subprocess", "os", "asyncio") and a.asname:
                    aliases[a.asname] = a.name
        elif isinstance(node, ast.ImportFrom) and node.module in ("subprocess", "os", "asyncio"):
            for a in node.names:
                if a.name == "*":
                    continue
                aliases[a.asname or a.name] = "%s.%s" % (node.module, a.name)
                if node.module == "subprocess":
                    from_subprocess.add(a.asname or a.name)
    call_env = {}  # call id -> module literal env at its statement
    for stmt in tree.body:
        for node in ast.walk(stmt):
            if isinstance(node, ast.Call):
                call_env[id(node)] = dict(env)
        if opaque_statement(stmt):
            env.clear()  # exec/globals/import * here rebinds names behind the resolver
        binding = module_binding(stmt)
        if binding is not None:
            name, value = binding
            resolved = LITERAL_MISS if name in unsafe else literal_value(value, env)
            if resolved is LITERAL_MISS:
                env.pop(name, None)
            else:
                env[name] = resolved
    funcs = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and not node.decorator_list:
            funcs[node.name] = None if node.name in funcs else (node.lineno, node)
    funcs = {k: v for k, v in funcs.items() if v is not None}
    spawn_hits, unparsed = spawn_scan(list(ast.walk(tree)), aliases, from_subprocess,
                                      {}, funcs, 0, call_env, scoped)
    hits.extend(spawn_hits)
    return hits, 0, unparsed


def helper_argv_leads(node, env):
    """Classify literal argv lists handed to a call this text does not define.

    Only what the call states is read: inline literals and parameters bound
    by an enclosing same-text helper call, never a module variable.
    """
    out = []
    for a in node.args:
        vals = argv_strings(literal_value(a, env))
        if vals is not None:
            out.extend(classify_shell(shlex.join(vals)))
    return out


def spawn_scan(nodes, aliases, from_subprocess, env, funcs, depth=0,
               call_env=None, scoped=frozenset()):
    """Classify spawn calls, resolving literal calls to same-text helpers.

    `env` is the helper-binding environment: empty at module scope, the bound
    parameters inside a same-text helper body. `call_env`/`scoped` carry the
    cell's module literal environment per call (a deferred call, inside a
    def/lambda/class body, resolves no module name). A call to a name this
    text neither defines nor imports contributes one lead per literal argv
    list it is handed: the argv is stated outright, the helper's body is not
    visible here.
    """
    hits, unparsed = [], 0
    for node in nodes:
        if not isinstance(node, ast.Call):
            continue
        cenv = env if call_env is None else (
            {} if id(node) in scoped else call_env[id(node)])
        helper = funcs.get(node.func.id) if isinstance(node.func, ast.Name) else None
        if helper is not None and node.lineno > helper[0] and depth < 4:
            bound = bind_literal(helper[1], node, env)
            if bound is not None:
                body = [n for n in ast.walk(helper[1]) if isinstance(n, ast.Call)]
                inner, _ = spawn_scan(body, aliases, from_subprocess, bound, funcs, depth + 1)
                hits.extend(inner)
            continue  # the helper body was counted where that body is defined
        name = dotted(node.func) or ""
        head, _, rest = name.partition(".")
        if head in aliases:
            name = aliases[head] + ("." + rest if rest else "")
        tail = name.rsplit(".", 1)[-1]
        is_sub = (name.startswith(("subprocess.", "sp.")) and tail in SPAWN_FUNCS) or \
                 (name == tail and tail in from_subprocess and tail in SPAWN_FUNCS)
        is_shell_fn = name in SHELL_STRING_FUNCS
        is_exec = name in ("asyncio.create_subprocess_exec", "os.execvp", "os.execv",
                           "os.spawnlp", "os.execlp")
        is_tool = name in ("tool.bash",)
        if not (is_sub or is_shell_fn or is_exec or is_tool):
            if (isinstance(node.func, ast.Name) and helper is None
                    and name not in PURE_ARG_CALLS):
                hits.extend(helper_argv_leads(node, env))
            continue
        if is_tool:
            arg = node.args[0] if node.args else None
            cmd = None
            if isinstance(arg, ast.Dict):
                for k, v in zip(arg.keys, arg.values):
                    if isinstance(k, ast.Constant) and k.value == "command":
                        value = literal_value(v, cenv)
                        if isinstance(value, str):
                            cmd = value
            if cmd is None:
                unparsed += 1
            else:
                hits.extend(classify_shell(cmd))
            continue
        if is_exec:
            vals = [literal_value(a, cenv) for a in node.args]
            if vals and all(isinstance(v, str) for v in vals):
                hits.extend(classify_shell(shlex.join(vals)))
            else:
                unparsed += 1
            continue
        arg = node.args[0] if node.args else None
        shell_kw = True
        for k in node.keywords:  # non-literal shell= is treated as shell
            if k.arg == "shell":
                flag = literal_value(k.value, cenv)
                shell_kw = flag is LITERAL_MISS or bool(flag)
        value = literal_value(arg, cenv) if arg is not None else LITERAL_MISS
        argv = argv_strings(value)
        if argv is not None:
            hits.extend(classify_shell(shlex.join(argv)))
        elif isinstance(value, str):
            hits.extend(classify_shell(value) if (is_shell_fn or shell_kw)
                        else classify_shell(shlex.quote(value)))
        else:
            unparsed += 1
    return hits, unparsed


# ----------------------------------------------------------------- scan ---

def refuse_path(path):
    try:
        st = os.lstat(path)
    except OSError:
        raise CouldNotEvaluate("unreadable path: %s" % path)
    if stat.S_ISLNK(st.st_mode):
        raise CouldNotEvaluate("refused symlink: %s" % path)
    real = os.path.realpath(path)
    agent = os.path.realpath(os.path.expanduser("~/.omp/agent"))
    sessions = os.path.join(agent, "sessions")
    if (real == agent or real.startswith(agent + os.sep)) and not (
            real == sessions or real.startswith(sessions + os.sep)):
        raise CouldNotEvaluate("refused path outside ~/.omp/agent/sessions: %s" % path)
    if REFUSED_NAMES.search(os.path.basename(real)):
        raise CouldNotEvaluate("refused file name: %s" % path)
    return st


def discover(paths):
    files = []
    for p in paths:
        st = refuse_path(p)
        if stat.S_ISDIR(st.st_mode):
            def onerror(err):
                raise CouldNotEvaluate("unreadable directory: %s" % err.filename)
            for root, dirs, names in os.walk(p, onerror=onerror, followlinks=False):
                dirs.sort()
                for n in sorted(names):
                    if n.endswith(".jsonl"):
                        files.append(os.path.join(root, n))
        elif stat.S_ISREG(st.st_mode):
            if not p.endswith(".jsonl"):
                raise CouldNotEvaluate("not a .jsonl file: %s" % p)
            files.append(p)
        else:
            raise CouldNotEvaluate("not a regular file or directory: %s" % p)
    if not files:
        raise CouldNotEvaluate("no .jsonl file found")
    seen, unique = set(), []
    for f in files:  # the same file reached twice is scanned once
        key = os.path.realpath(f)
        if key not in seen:
            seen.add(key)
            unique.append(f)
    return unique


def reject_constant(value):
    raise ValueError("non-standard JSON constant %s" % value)


def scan_file(path):
    st = refuse_path(path)
    if not stat.S_ISREG(st.st_mode):
        raise CouldNotEvaluate("not a regular file: %s" % path)
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError:
        raise CouldNotEvaluate("unreadable file: %s" % path)
    entry = {"path": path, "sha256": hashlib.sha256(data).hexdigest(),
             "lines": 0, "bash_calls": 0, "eval_calls": 0,
             "eval_unparsed": 0, "unparsed_spawns": 0}
    findings = []
    raw_lines = data.split(b"\n")
    if raw_lines and raw_lines[-1] == b"":
        raw_lines.pop()
    entry["lines"] = len(raw_lines)
    envs = {}  # language kernel -> literal env, carried across this file's cells
    for lineno, raw in enumerate(raw_lines, 1):
        if not raw.strip():
            continue
        try:
            obj = json.loads(raw.decode("utf-8"), parse_constant=reject_constant)
        except (ValueError, UnicodeDecodeError, RecursionError) as exc:
            raise CouldNotEvaluate("%s:%d invalid line (%s)" % (path, lineno, type(exc).__name__))
        if not isinstance(obj, dict) or "type" not in obj:
            raise CouldNotEvaluate("%s:%d unknown record shape" % (path, lineno))
        if obj.get("type") != "message":
            continue
        msg = obj.get("message")
        if not isinstance(msg, dict) or msg.get("role") != "assistant":
            continue
        content = msg.get("content")
        if not isinstance(content, list):
            continue
        for item in content:
            if not isinstance(item, dict) or item.get("type") != "toolCall":
                continue
            name = item.get("name")
            args = item.get("arguments") if isinstance(item.get("arguments"), dict) else {}
            NESTED["eval_unparsed"] = NESTED["unparsed_spawns"] = 0
            if name == "bash":
                entry["bash_calls"] += 1
                cmd = args.get("command")
                hits = classify_shell(cmd) if isinstance(cmd, str) else []
            elif name == "eval":
                entry["eval_calls"] += 1
                code = args.get("code")
                if not isinstance(code, str):
                    continue
                language = args.get("language")
                env = None
                if language in (None, "py", "python"):
                    if args.get("reset") is True:  # fresh kernel: nothing carries in
                        envs["py"] = {}
                    env = envs.setdefault("py", {})
                hits, un_eval, un_spawn = classify_eval(code, language, env)
                entry["eval_unparsed"] += un_eval
                entry["unparsed_spawns"] += un_spawn
            else:
                continue
            entry["eval_unparsed"] += NESTED["eval_unparsed"]
            entry["unparsed_spawns"] += NESTED["unparsed_spawns"]
            seen = set()
            for cls, rule, argv0, text in hits:
                key = (cls, rule)
                if key in seen:
                    continue
                seen.add(key)
                findings.append({
                    "file": path, "line": lineno,
                    "tool_call_id": str(item.get("id", "")),
                    "timestamp": obj.get("timestamp") if isinstance(obj.get("timestamp"), str) else str(obj.get("timestamp")),
                    "tool": name, "class": cls, "rule": rule,
                    "argv0": argv0, "command": redact(text),
                })
    return entry, findings


def scan(paths):
    files = discover(paths)
    entries, findings = [], []
    for f in files:
        e, fs = scan_file(f)
        entries.append(e)
        findings.extend(fs)
    counts = {c: sum(1 for f in findings if f["class"] == c) for c in CLASSES}
    return entries, findings, counts


def verdict_of(findings, permit):
    """(exit, label, unpermitted) — one authority for --scan and --frozen."""
    unpermitted = sum(1 for f in findings if f["class"] not in permit)
    code = 1 if unpermitted else 0
    label = "clean" if not findings else ("findings" if unpermitted else "permitted_only")
    return code, label, unpermitted


def emit(label, payload):
    print("MADO_TRIPWIRE: %s" % label)
    print(json.dumps(payload, ensure_ascii=True, sort_keys=True))


def run_scan(paths, permit):
    try:
        entries, findings, counts = scan(paths)
    except CouldNotEvaluate as exc:
        emit("could_not_evaluate", {"schema": "mado-tripwire-verdict-v1", "exit": 2,
                                    "error": str(exc), "files": [], "findings": [],
                                    "counts": {c: 0 for c in CLASSES},
                                    "permitted": sorted(permit), "unpermitted": 0})
        return 2
    code, label, unpermitted = verdict_of(findings, permit)
    emit(label, {"schema": "mado-tripwire-verdict-v1", "exit": code, "files": entries,
                 "findings": findings, "counts": counts,
                 "permitted": sorted(permit), "unpermitted": unpermitted})
    return code


# ------------------------------------------------------------- frozen ---

FROZEN_SCHEMA = "mado-tripwire-frozen-v1"
FROZEN_LABELS = ("clean", "permitted_only", "findings")
FROZEN_PAIRS = {(0, "clean"), (0, "permitted_only"), (1, "findings")}
FROZEN_PATH = re.compile(r"inputs/[A-Za-z0-9._-]+\.jsonl")


def tool_sha256():
    try:
        with open(os.path.abspath(__file__), "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return None


def emit_frozen(outcome, expected_sha, inputs, missing, extra,
                scan_exit, scan_label, error=None):
    payload = {
        "schema": "mado-tripwire-frozen-verdict-v1",
        "outcome": outcome,
        "exit": (0 if outcome == "frozen_match"
                 else 1 if outcome == "frozen_verdict_mismatch" else 2),
        "tool_sha256": tool_sha256(),
        "expected_sha256": expected_sha,
        "inputs": inputs,
        "missing_findings": missing,
        "extra_findings": extra,
        "scan_exit": scan_exit,
        "scan_label": scan_label,
    }
    if error is not None:
        payload["error"] = error
    print("MADO_TRIPWIRE_FROZEN: %s" % outcome)
    print(json.dumps(payload, ensure_ascii=True, sort_keys=True))
    return payload["exit"]


def frozen_error(message, expected_sha, inputs, outcome="frozen_error"):
    return emit_frozen(outcome, expected_sha, inputs, [], [], None, None, message)


FROZEN_KEYS = frozenset(("schema", "inputs", "permit", "expected_exit",
                         "expected_label", "expected_findings", "known_misses"))


def unique_pairs(pairs):
    """object_pairs_hook: a repeated JSON key is a baseline error, never last-wins."""
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError("duplicate key %r" % key)
        seen[key] = value
    return seen


def validate_frozen(spec):
    """Return (error, pinned) for a mado-tripwire-frozen-v1 spec object.

    Shape and reachability are checked before any input is read: a pin that no
    scan could ever reproduce (empty inputs, a path outside `inputs/<name>.jsonl`,
    a duplicate, a class outside CLASSES, an exit/label pair the verdict cannot
    take, a label contradicting its findings, a listed file that is not an
    input, a known miss on an expected line) is a baseline error, not a failed
    verdict.
    """
    if spec.get("schema") != FROZEN_SCHEMA:
        return "bad schema", None
    unknown = sorted(set(spec) - FROZEN_KEYS)
    if unknown:
        return "unknown expected.json key(s): %s" % ", ".join(unknown), None
    inputs = spec.get("inputs")
    if not isinstance(inputs, list) or not inputs:
        return "inputs is not a non-empty list", None
    listed = {}
    for e in inputs:
        if not isinstance(e, dict) or not isinstance(e.get("path"), str) or not e["path"]:
            return "bad inputs entry", None
        if not FROZEN_PATH.fullmatch(e["path"]):
            return "input path is not inputs/<name>.jsonl: %s" % e["path"], None
        if os.path.normpath(e["path"]) in listed:
            return "duplicate input path: %s" % e["path"], None
        listed[os.path.normpath(e["path"])] = e["path"]
        if "sha256" in e and not isinstance(e["sha256"], str):
            return "bad inputs sha256", None
    permit = spec.get("permit")
    if not isinstance(permit, list) or any(not isinstance(c, str) for c in permit):
        return "permit is not a list of classes", None
    if set(permit) - set(CLASSES):
        return "unknown permit class", None
    permit = set(permit)
    want_exit = spec.get("expected_exit")
    if type(want_exit) is not int or want_exit not in (0, 1):
        return "bad expected_exit", None
    want_label = spec.get("expected_label")
    if not isinstance(want_label, str) or want_label not in FROZEN_LABELS:
        return "bad expected_label", None
    if (want_exit, want_label) not in FROZEN_PAIRS:
        return "unreachable exit/label pair: %d/%s" % (want_exit, want_label), None
    want = spec.get("expected_findings")
    if not isinstance(want, list):
        return "expected_findings is not a list", None
    for w in want:
        if (not isinstance(w, dict) or not isinstance(w.get("file"), str)
                or type(w.get("line")) is not int or w["line"] < 1
                or not isinstance(w.get("class"), str)
                or not isinstance(w.get("rule"), str)):
            return "bad expected_findings entry", None
        if w["class"] not in CLASSES:
            return "unknown class in expected_findings: %s" % w["class"], None
        if os.path.normpath(w["file"]) not in listed:
            return "expected_findings names an unlisted input: %s" % w["file"], None
    if want_label == "clean":
        if want:
            return "clean baseline lists expected_findings", None
    elif not want:
        return "%s baseline lists no expected_findings" % want_label, None
    elif want_label == "permitted_only" and any(c not in permit for c in
                                               (w["class"] for w in want)):
        return "permitted_only baseline lists a class outside permit", None
    elif want_label == "findings" and not any(w["class"] not in permit for w in want):
        return "findings baseline lists no class outside permit", None
    known = spec.get("known_misses", [])
    if not isinstance(known, list):
        return "known_misses is not a list", None
    for k in known:
        if (not isinstance(k, dict) or not isinstance(k.get("file"), str)
                or type(k.get("line")) is not int or k["line"] < 1
                or ("note" in k and not isinstance(k["note"], str))):
            return "bad known_misses entry", None
        if os.path.normpath(k["file"]) not in listed:
            return "known_misses names an unlisted input: %s" % k["file"], None
    overlap = ({(os.path.normpath(w["file"]), w["line"]) for w in want}
               & {(os.path.normpath(k["file"]), k["line"]) for k in known})
    if overlap:
        f, ln = sorted(overlap)[0]
        return "known_misses overlaps expected_findings: %s:%d" % (f, ln), None
    return None, {"inputs": inputs, "permit": permit, "exit": want_exit,
                  "label": want_label, "findings": want, "known": known}


def validate_reachable(pinned, stats):
    """Return an error when a pinned line cannot exist in the pinned bytes.

    stats maps a listed input path to its per-line non-blank flags; it is
    computed from the same bytes that matched the pin, so this check cannot be
    raced by a rewrite between hashing and scanning.
    """
    for w in pinned["findings"]:
        lines = stats[os.path.normpath(w["file"])]
        if w["line"] > len(lines):
            return "expected_findings line %d is past the end of %s" % (
                w["line"], w["file"])
        if not lines[w["line"] - 1]:
            return "expected_findings line %d of %s is blank" % (w["line"], w["file"])
    for k in pinned["known"]:
        lines = stats[os.path.normpath(k["file"])]
        if k["line"] > len(lines):
            return "known_misses line %d is past the end of %s" % (
                k["line"], k["file"])
        if not lines[k["line"] - 1]:
            return "known_misses line %d of %s is blank" % (k["line"], k["file"])
    return None


def frozen_snapshot(directory, entries):
    """Return (outcome, report, stats); outcome None when every input matches.

    report[i]["ok"] means that input itself is a listed non-symlink regular
    file that resolves inside DIRECTORY and whose bytes digest-match its pin;
    it is computed per entry even when another entry fails, so a verdict shows
    exactly which bytes were verified. stats maps a verified input path to its
    per-line non-blank flags, so pin reachability is judged on the pinned bytes.
    Failure priority: path/containment/regularity and unlisted files, then an
    unpinned entry (legacy), then bytes that do not match their pin.
    """
    real_dir = os.path.realpath(directory)
    report = [{"path": e["path"],
               "sha256": e["sha256"] if isinstance(e.get("sha256"), str) else None,
               "ok": False} for e in entries]
    paths_ok, bad_paths = [], False
    for e in entries:
        rel = e["path"]
        real = os.path.realpath(os.path.join(directory, rel))
        good = real == real_dir or real.startswith(real_dir + os.sep)
        if good:
            try:
                st = os.lstat(os.path.join(directory, rel))
            except OSError:
                good = False
            else:
                good = not stat.S_ISLNK(st.st_mode) and stat.S_ISREG(st.st_mode)
        paths_ok.append(good)
        bad_paths = bad_paths or not good
    listed = {os.path.normpath(e["path"]) for e in entries}
    # Resolve DIR/inputs the way the kernel will before testing it: `DIR`,
    # `DIR/` and `DIR/.` name one directory, so a lexical test answers for the
    # spelling, not for the directory (round-18 finding F2). The walk root
    # stays spelled so relative paths remain relative to DIRECTORY.
    idir = os.path.join(directory, "inputs")
    real_inputs = os.path.join(real_dir, "inputs")
    if os.path.islink(idir) or os.path.realpath(idir) != real_inputs:
        # a symlinked inputs/ replays bytes outside the pin
        bad_paths = True
        paths_ok = [False for _ in paths_ok]  # every listed path is under inputs/
    elif os.path.isdir(idir):
        def onerror(err):
            raise CouldNotEvaluate("unreadable snapshot directory: %s" % err.filename)
        try:
            for root, dirs, names in os.walk(idir, onerror=onerror, followlinks=False):
                dirs.sort()
                for n in sorted(names):
                    if not n.endswith(".jsonl"):
                        continue
                    rel = os.path.normpath(os.path.relpath(os.path.join(root, n), directory))
                    if rel not in listed:
                        bad_paths = True
        except CouldNotEvaluate:
            bad_paths = True  # an unlistable inputs dir cannot prove completeness
    unpinned = any("sha256" not in e for e in entries)
    bad_bytes = False
    stats = {}
    for idx, e in enumerate(entries):
        if not paths_ok[idx] or "sha256" not in e:
            continue
        try:
            with open(os.path.join(directory, e["path"]), "rb") as fh:
                data = fh.read()
        except OSError:
            bad_bytes = True
            continue
        report[idx]["ok"] = (hashlib.sha256(data).hexdigest()
                             == e["sha256"].strip().lower())
        if report[idx]["ok"]:
            raw = data.split(b"\n")
            if raw and raw[-1] == b"":
                raw.pop()
            stats[os.path.normpath(e["path"])] = [bool(r.strip()) for r in raw]
        bad_bytes = bad_bytes or not report[idx]["ok"]
    if bad_paths:
        return "snapshot_tampered", report, stats
    if unpinned:
        return "unpinned_legacy", report, stats
    if bad_bytes:
        return "snapshot_tampered", report, stats
    return None, report, stats


def frozen_dir_symlinked(directory):
    """True when DIRECTORY is named through a symlink.

    Every spelling that reaches one directory (`DIR`, `DIR/`, `DIR/.`,
    `DIR/inputs/..`, `link/../evil`) is judged by kernel resolution, so a
    trailing component cannot launder a symlinked DIR (round-18 finding F2).
    A symlink above DIR is host layout, not snapshot identity, and is allowed.
    """
    real_dir = os.path.realpath(directory)
    path = directory if os.path.isabs(directory) else os.path.join(os.getcwd(),
                                                                   directory)
    prefix = os.sep
    for part in path.split(os.sep):
        if not part:
            continue
        prefix = os.path.join(prefix, part)
        if os.path.islink(prefix) and os.path.realpath(prefix) == real_dir:
            return True
    return False


def run_frozen(directory):
    if frozen_dir_symlinked(directory):
        return frozen_error("frozen directory is a symlink", None, [],
                            outcome="snapshot_tampered")
    try:
        with open(os.path.join(directory, "expected.json"), "rb") as fh:
            raw = fh.read()
    except OSError:
        return frozen_error("expected.json unreadable", None, [])
    expected_sha = hashlib.sha256(raw).hexdigest()
    try:
        spec = json.loads(raw.decode("utf-8"), parse_constant=reject_constant,
                          object_pairs_hook=unique_pairs)
    except (ValueError, UnicodeDecodeError) as exc:
        return frozen_error("expected.json not JSON (%s)" % type(exc).__name__,
                            expected_sha, [])
    if not isinstance(spec, dict):
        return frozen_error("expected.json is not an object", expected_sha, [])
    err, pinned = validate_frozen(spec)
    if err:
        return frozen_error(err, expected_sha, [])
    bad, report, stats = frozen_snapshot(directory, pinned["inputs"])
    if bad == "unpinned_legacy":
        return frozen_error("input entry without sha256", expected_sha, report,
                            outcome="unpinned_legacy")
    if bad:
        return frozen_error("snapshot does not match its pin", expected_sha,
                            report, outcome="snapshot_tampered")
    err = validate_reachable(pinned, stats)
    if err:
        return frozen_error(err, expected_sha, report)
    findings = []
    for e in pinned["inputs"]:
        try:
            entry, hits = scan_file(os.path.join(directory, e["path"]))
        except CouldNotEvaluate as exc:
            return frozen_error(str(exc), expected_sha, report)
        if entry["sha256"] != e["sha256"].strip().lower():
            return frozen_error("snapshot changed during scan: %s" % e["path"],
                                expected_sha, report, outcome="snapshot_tampered")
        for f in hits:
            f["file"] = e["path"]
            findings.append(f)
    scan_exit, scan_label, _ = verdict_of(findings, pinned["permit"])

    def key(f):
        return (f["file"], f["line"], f["class"], f["rule"])

    got = Counter(key(f) for f in findings)
    expected = Counter(key(w) for w in pinned["findings"])
    missing = expected - got
    # A finding on a known-miss line is necessarily `extra`: validate_frozen
    # refuses a pin that also expects that (file, line).
    extra = got - expected
    missing_rows = [dict(zip(("file", "line", "class", "rule"), k))
                    for k in sorted(missing.elements())]
    extra_rows = [dict(zip(("file", "line", "class", "rule"), k))
                  for k in sorted(extra.elements())]
    mismatch = (scan_exit != pinned["exit"] or scan_label != pinned["label"]
                or bool(missing) or bool(extra))
    outcome = "frozen_verdict_mismatch" if mismatch else "frozen_match"
    return emit_frozen(outcome, expected_sha, report, missing_rows, extra_rows,
                       scan_exit, scan_label)


# ------------------------------------------------------------- selftest ---

def run_selftest(directory):
    try:
        with open(os.path.join(directory, "expected.json"), encoding="utf-8") as fh:
            spec = json.load(fh)
        cases = spec["cases"]
        assert spec.get("schema") == "mado-tripwire-selftest-v1"
        assert isinstance(cases, list) and cases
    except (OSError, ValueError, KeyError, AssertionError, TypeError) as exc:
        print("SELFTEST_SUMMARY: 0/0 malformed expected.json (%s)" % type(exc).__name__)
        return 2
    passed, failed = 0, []
    me = os.path.abspath(__file__)
    for case in cases:
        try:
            name = case["name"]
            mode = case.get("mode", "scan")
            if mode == "frozen":
                if not isinstance(case["want_label"], str):
                    raise KeyError("want_label")
                want_missing = case.get("want_missing", 0)
                want_extra = case.get("want_extra", 0)
                if type(want_missing) is not int or type(want_extra) is not int:
                    raise KeyError("want_missing")
                argv = [sys.executable, "-I", me, "--frozen",
                        os.path.join(directory, case["args"][0])]
                want_exit = case["want_exit"]
                want_label = case["want_label"]
            elif mode == "scan":
                argv = [sys.executable, "-I", me, "--scan"] + [
                    os.path.join(directory, a) for a in case["args"]]
                if case.get("permit"):
                    argv += ["--permit"] + list(case["permit"])
                want_exit = case["want_exit"]
                want = case["want_findings"]
            else:
                raise KeyError("mode")
        except (KeyError, TypeError, IndexError):
            print("SELFTEST_SUMMARY: malformed case")
            return 2
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=120)
        out = proc.stdout.split("\n")
        got_exit = proc.returncode
        if mode == "frozen":  # want_findings is ignored in this mode
            want_first = "MADO_TRIPWIRE_FROZEN: " + want_label
            verdict = None
            try:
                verdict = json.loads(out[1])
            except (IndexError, ValueError):
                pass
            detail = None
            if isinstance(verdict, dict):
                miss = verdict.get("missing_findings")
                extra_rows = verdict.get("extra_findings")
                if isinstance(miss, list) and isinstance(extra_rows, list):
                    detail = (verdict.get("outcome"), verdict.get("exit"),
                              len(miss), len(extra_rows))
            ok = (got_exit == want_exit and out[0] == want_first
                  and isinstance(verdict, dict)
                  and verdict.get("schema") == "mado-tripwire-frozen-verdict-v1"
                  and detail == (want_label, want_exit, want_missing, want_extra))
            if ok:
                passed += 1
                print("CASE %s ok" % name)
            else:
                failed.append(name)
                print("CASE %s FAIL want=%s got=%s" % (
                    name, (want_exit, want_first, want_missing, want_extra),
                    (got_exit, out[0] if out else "", detail)))
            continue
        try:
            verdict = json.loads(out[1])
        except (IndexError, ValueError):
            verdict = None
        use_file = any("file" in w for w in want)
        def key(f, from_want):
            return (f["class"], f["rule"], f["line"],
                    (f.get("file", "") if from_want else os.path.basename(f["file"])) if use_file else "")
        got = sorted(key(f, False) for f in (verdict or {}).get("findings", []))
        exp = sorted(key(w, True) for w in want)
        first_ok = out[0].startswith("MADO_TRIPWIRE: ") if out else False
        ok = verdict is not None and first_ok and got_exit == want_exit and got == exp
        if ok and "want_label" in case:
            ok = out[0] == "MADO_TRIPWIRE: " + case["want_label"]
        if ok and "want_error_contains" in case:
            ok = case["want_error_contains"] in str((verdict or {}).get("error", ""))
        if ok and "want_ids" in case:  # tool_call_id attribution, in finding order
            ok = [f["tool_call_id"] for f in verdict["findings"]] == case["want_ids"]
        if ok:
            passed += 1
            print("CASE %s ok" % name)
        else:
            failed.append(name)
            print("CASE %s FAIL want=%s got=%s" % (name, (want_exit, exp), (got_exit, got)))
    print("SELFTEST_SCRIPT_SHA256: %s" % hashlib.sha256(open(me, "rb").read()).hexdigest())
    print("SELFTEST_SUMMARY: %d/%d passed failed=%s" % (passed, len(cases), failed))
    return 0 if not failed else 1


def main(argv):
    if len(argv) == 2 and argv[0] == "--selftest":
        return run_selftest(argv[1])
    if len(argv) == 2 and argv[0] == "--frozen":
        return run_frozen(argv[1])
    if not argv or argv[0] != "--scan":
        print("usage: mado-tripwire.py --scan PATH [PATH ...] [--permit CLASS ...] | "
              "--frozen DIR | --selftest DIR", file=sys.stderr)
        emit("could_not_evaluate", {"schema": "mado-tripwire-verdict-v1", "exit": 2,
                                    "error": "usage", "files": [], "findings": [],
                                    "counts": {c: 0 for c in CLASSES}, "permitted": [],
                                    "unpermitted": 0})
        return 2
    rest = argv[1:]
    permit = set()
    if "--permit" in rest:
        i = rest.index("--permit")
        permit = set(rest[i + 1:])
        rest = rest[:i]
        if not permit or not permit <= set(CLASSES):
            emit("could_not_evaluate", {"schema": "mado-tripwire-verdict-v1", "exit": 2,
                                        "error": "unknown permit class", "files": [],
                                        "findings": [], "counts": {c: 0 for c in CLASSES},
                                        "permitted": [], "unpermitted": 0})
            return 2
    if not rest:
        emit("could_not_evaluate", {"schema": "mado-tripwire-verdict-v1", "exit": 2,
                                    "error": "no path", "files": [], "findings": [],
                                    "counts": {c: 0 for c in CLASSES}, "permitted": [],
                                    "unpermitted": 0})
        return 2
    return run_scan(rest, permit)


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except SystemExit:
        raise
    except BaseException as exc:  # never let an internal error read as "findings"
        if sys.argv[1:2] == ["--frozen"]:
            frozen_error("internal %s" % type(exc).__name__, None, [])
            sys.exit(2)
        print("MADO_TRIPWIRE: could_not_evaluate")
        print(json.dumps({"schema": "mado-tripwire-verdict-v1", "exit": 2,
                          "error": "internal %s" % type(exc).__name__, "files": [],
                          "findings": [], "counts": {c: 0 for c in CLASSES},
                          "permitted": [], "unpermitted": 0}, ensure_ascii=True))
        sys.exit(2)
