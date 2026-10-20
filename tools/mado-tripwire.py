#!/usr/bin/env python3
"""mado-tripwire — post-hoc tripwire over OMP session transcripts (JSONL).

Classifies commands a seat *issued* in assistant `toolCall` blocks:
`bash` (arguments.command) and python `eval` (arguments.code: `!` shell
lines, `%%bash` cells and literal subprocess/os/tool.bash spawns parsed with
`ast`, never executed). Classes: host_mutation, package_query, live_probe.

Limits (stated, not hidden):
- Detection after the fact only. It is not interception, prevention, a
  sandbox or host repair; it cannot stop a command and says nothing about
  commands outside the files it is given.
- "Issued" is not "executed": toolResult records are ignored on purpose
  (a successful harmful call and a refused one both count).
- `clean` means no finding in the covered forms. It never means "no host
  command ran": non-literal spawn arguments (counted as unparsed_spawns),
  JavaScript eval cells (eval_unparsed), scripts written then run, shell
  functions/aliases, python -c bodies, other tools and other sessions are
  not analysed. Pair a verdict with a /var/log/pacman.log window count.
- shlex is not bash: exotic quoting can hide a command from the parser.
- Transcript text is data. Nothing in it is followed or executed.

CLI:
  mado-tripwire.py --scan PATH [PATH ...] [--permit CLASS ...]
  mado-tripwire.py --selftest DIR      (DIR/expected.json)
Exit: 0 no unpermitted finding; 1 at least one unpermitted finding;
2 could-not-evaluate (usage, refused/unreadable path, no .jsonl, invalid
line, internal error). Exit 2 wins over 1.
First line: MADO_TRIPWIRE: clean | permitted_only | findings | could_not_evaluate
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

CLASSES = ("host_mutation", "package_query", "live_probe")
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


def tokenize(line):
    lex = shlex.shlex(line, posix=True, punctuation_chars=";&|()<>")
    lex.whitespace_split = True
    lex.whitespace = " \t\r"
    lex.commenters = ""  # '#' is a comment only at word start: handled in segments()
    return list(lex)


def segments(tokens):
    seg = []
    skip_next = False
    for i, tok in enumerate(tokens):
        if skip_next:
            skip_next = False
            continue
        if tok.startswith("#"):
            break  # comment to end of line (a word starting with '#')
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
        if argv0 in ("yay", "paru"):
            return ("host_mutation", argv0)
        return ("package_query", argv0)
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


def classify_shell(text, depth=0):
    """Return a list of (class, rule, argv0, segment_text, unparsed)."""
    if depth > 8 or not text or not text.strip():
        return []
    out = []
    for line, bodies in logical_lines(text):
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
    if re.fullmatch(r"python[0-9.]*", argv0) and "-c" in args:
        i = args.index("-c")
        if i + 1 < len(args):
            return nested_eval(args[i + 1])
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


def str_list(node):
    if isinstance(node, (ast.List, ast.Tuple)) and node.elts and all(
            isinstance(e, ast.Constant) and isinstance(e.value, str) for e in node.elts):
        return [e.value for e in node.elts]
    return None


def classify_eval(code, language):
    """Return (hits, eval_unparsed, unparsed_spawns)."""
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
    unparsed = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
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
            continue
        if is_tool:
            arg = node.args[0] if node.args else None
            cmd = None
            if isinstance(arg, ast.Dict):
                for k, v in zip(arg.keys, arg.values):
                    if isinstance(k, ast.Constant) and k.value == "command" and \
                            isinstance(v, ast.Constant) and isinstance(v.value, str):
                        cmd = v.value
            if cmd is None:
                unparsed += 1
            else:
                hits.extend(classify_shell(cmd))
            continue
        if is_exec:
            vals = [a.value for a in node.args if isinstance(a, ast.Constant) and isinstance(a.value, str)]
            if vals and len(vals) == len(node.args):
                hits.extend(classify_shell(shlex.join(vals)))
            else:
                unparsed += 1
            continue
        arg = node.args[0] if node.args else None
        shell_kw = any(k.arg == "shell" and not (isinstance(k.value, ast.Constant) and not k.value.value)
                       for k in node.keywords)  # non-literal shell= is treated as shell
        lst = str_list(arg) if arg is not None else None
        if lst is not None:
            hits.extend(classify_shell(shlex.join(lst)))
        elif isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            hits.extend(classify_shell(arg.value) if (is_shell_fn or shell_kw)
                        else classify_shell(shlex.quote(arg.value)))
        else:
            unparsed += 1
    return hits, 0, unparsed


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
                hits, un_eval, un_spawn = classify_eval(code, args.get("language"))
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


def scan(paths, permit):
    files = discover(paths)
    entries, findings = [], []
    for f in files:
        e, fs = scan_file(f)
        entries.append(e)
        findings.extend(fs)
    counts = {c: sum(1 for f in findings if f["class"] == c) for c in CLASSES}
    unpermitted = sum(1 for f in findings if f["class"] not in permit)
    return entries, findings, counts, unpermitted


def emit(label, payload):
    print("MADO_TRIPWIRE: %s" % label)
    print(json.dumps(payload, ensure_ascii=True, sort_keys=True))


def run_scan(paths, permit):
    try:
        entries, findings, counts, unpermitted = scan(paths, permit)
    except CouldNotEvaluate as exc:
        emit("could_not_evaluate", {"schema": "mado-tripwire-verdict-v1", "exit": 2,
                                    "error": str(exc), "files": [], "findings": [],
                                    "counts": {c: 0 for c in CLASSES},
                                    "permitted": sorted(permit), "unpermitted": 0})
        return 2
    code = 1 if unpermitted else 0
    label = "clean" if not findings else ("findings" if unpermitted else "permitted_only")
    emit(label, {"schema": "mado-tripwire-verdict-v1", "exit": code, "files": entries,
                 "findings": findings, "counts": counts,
                 "permitted": sorted(permit), "unpermitted": unpermitted})
    return code


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
            argv = [sys.executable, "-I", me, "--scan"] + [os.path.join(directory, a) for a in case["args"]]
            if case.get("permit"):
                argv += ["--permit"] + list(case["permit"])
            want_exit = case["want_exit"]
            want = case["want_findings"]
        except (KeyError, TypeError):
            print("SELFTEST_SUMMARY: malformed case")
            return 2
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=120)
        out = proc.stdout.split("\n")
        got_exit = proc.returncode
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
    if not argv or argv[0] != "--scan":
        print("usage: mado-tripwire.py --scan PATH [PATH ...] [--permit CLASS ...] | --selftest DIR",
              file=sys.stderr)
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
        print("MADO_TRIPWIRE: could_not_evaluate")
        print(json.dumps({"schema": "mado-tripwire-verdict-v1", "exit": 2,
                          "error": "internal %s" % type(exc).__name__, "files": [],
                          "findings": [], "counts": {c: 0 for c in CLASSES},
                          "permitted": [], "unpermitted": 0}, ensure_ascii=True))
        sys.exit(2)
