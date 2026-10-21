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
the difference between a venv/`--user` install and a system one. An exact
`-h`/`--help` before any `--` on the uv/pip/cargo install, upgrade and
uninstall forms prints help and is not a finding; run forms (uvx, npx, `uv
tool run`, pipx run, npm exec) hand it to the fetched package and stay one.

Limits (stated, not hidden):
- Detection after the fact only. It is not interception, prevention, a
  sandbox or host repair; it cannot stop a command and says nothing about
  commands outside the files it is given.
- "Issued" is not "executed": toolResult records are ignored on purpose
  (a successful harmful call and a refused one both count).
- `clean` means no finding in the covered forms. It never means "no host
  command ran": non-literal spawn arguments (counted as unparsed_spawns),
  JavaScript eval cells (eval_unparsed), scripts written then run, shell
  aliases (never expanded, even when defined in the scanned text), other
  tools and other sessions are not analysed. `python -c` bodies are parsed
  like eval cells. Pair a verdict with a /var/log/pacman.log window count.
- A visible Python `def`/`async def`/lambda called with literal arguments
  (a starred argument only when its value is a literal list/tuple) is
  followed through its body with those values bound: the called helper and
  up to three helpers it calls in turn (four bodies deep), including
  definitions from earlier py eval cells of the same file unless a `reset`
  intervenes; an explicit `__init__` and a directly resolved visible class
  method are followed. Rows found that way are `observed`; a coroutine
  created without a direct `await` is followed, but its rows are `lead`
  (it runs only if something schedules it).
- A visible body this path does not follow but the executed text still
  reaches is swept, and every row in it is a `lead`: a def, lambda or class
  handed on as a value (thread target, callback, decorator, returned
  closure, `asyncio.run(...)` argument), an inline or immediately invoked
  lambda, the dunder methods of a constructed or used class
  (`__enter__`/`__exit__`, `__del__`, `__post_init__`, ...), a recursive
  call, a call past the depth above or past 2000 followed calls per cell,
  and a call whose arguments cannot be bound. A swept body's parameters are
  unknown, and each body is swept once per cell. A Python body nothing in
  the executed text references establishes no execution path and gives no
  row. Shell function bodies are different: `f() { cmd; }` is classified
  as if `cmd` ran, called or not, and `$1..$9` and `$@/$*` are substituted
  where the function is called.
- A literal positional `['prog', ...]` argv passed to an unresolved bare
  name or to a callable imported from outside the standard library is a
  `lead`, as is a literal argv (or, for `system`/`popen` or a `shell=`
  call, a literal command string) handed to a spawn-named method
  (`run`, `call`, `Popen`, `check_output`, `system`, `popen`, ...) of an
  object or module the scan cannot resolve, and literal argv handed beside
  a spawn callable to the call that receives it (`Thread(target=
  subprocess.run, args=(argv,))`). Builtins and callables of standard
  library modules that cannot start a process, run code text or call back
  (everything but PROCESS_STDLIB; `os.path` is allowed) are pure while not
  rebound: data passed to them gives no row. A same-command `lead` is
  dropped when the same tool call already has it `observed`. Dynamic
  dispatch (`getattr`, `importlib` other than a literal
  `import_module('name')`), metaclass/descriptor behavior and inherited
  methods are not resolved. Every finding carries `evidence: observed|lead`.
- Variable recipes are resolved only when the text fixes them: a name bound
  by a straight-line module-level assignment to a literal-only expression
  (str, `+`, two-argument `str.replace`, or a list of those), earlier in the
  same cell or in an earlier cell of the same py kernel in the same
  transcript (eval state persists; a `reset` cell, an exec/import * or a
  globals()/locals()/vars() result used other than for a read from that
  point on, or any other binding forgets the name).
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
  `--version` excepted). The subcommand is located by position, so a global
  option value spelling a verb (`jj -R git git push`) does not hide it. A
  jj-lane.sh helper invocation is not a finding. Anything else on the `git`
  side (fetch, revert, tag, branch, clean, worktree, gc, config) and `git`
  subcommands hidden in aliases or scripts are outside the class (a shell
  function body is classified where it is defined, see above).
- A run that only prints help or simulates is not a vcs_write. jj: an exact
  `-h`/`--help` before any `--`, ahead of the subcommand or after one in
  JJ_HELP_VERBS (jj 0.45.1 built-ins, which config cannot shadow, and the
  default aliases b/ci/desc/st, whose redefinition is not visible here):
  clap answers it before the workspace is loaded and never takes a separate
  `--help` as an option value (`-m --help` is a usage error, `-m=--help` a
  message). Any other verb may be a config alias that forwards `--help`
  past `util exec --`, so it stays a finding. `jj git push --dry-run`
  pushes nothing but still snapshots, so it is a write unless
  --ignore-working-copy is given.
  git: `git -h|--help <sub>` and `-h`/`--help` as a flag anywhere among the
  subcommand's options (usage; a leading `<sub> --help` becomes `git help
  <sub>`), `git commit` with --dry-run/--short/--porcelain/--long/-z and
  `git add|push` with -n/--dry-run, each read last-wins against its --no-
  form; a short-option cluster counts letter by letter (`add -nv` is `-n
  -v`) up to a value-taking letter. Option values are skipped with
  GIT_VALUE_OPTS (git 2.56.0 separate-value options, long ones also by
  abbreviation), so `commit -m -h` and `commit -m --dry-run` stay writes;
  `commit -n` is --no-verify, and an abbreviated negation (`--no-dry`) or
  dry-run (`--dry`) keeps the finding, as does an ambiguous abbreviation
  git itself would reject.
  A dry run still runs the pre-push hook and `commit --dry-run` may store
  unreferenced objects; neither moves a ref, the index or the worktree.
  None of these exemptions (nor the installer `--help` one, nor
  `--ignore-working-copy`) applies in an unparsed segment (rule suffix
  `/unparsed`: shlex failed and the line was split on whitespace, so its
  tokens may belong to the next command): `git checkout x; bash -c 'git
  grep -ohE …'` stays a checkout even though `-ohE` holds an `h`.
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
--scan JSON includes findings with evidence markers and the integer totals
`observed_findings` and `lead_findings`; a lead remains under `findings`.
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
0); it also pins the verdict schema, outcome and exit, not only line 1. A
scan case may specify `evidence` in wanted findings; it is compared when any
wanted finding specifies it.
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
JJ_BOOKMARK_WRITE = {"set", "move", "create", "delete", "forget", "rename", "track", "untrack"}
JJ_OP_WRITE = {"restore", "revert", "abandon"}
JJ_GIT_WRITE = {"push", "fetch", "import", "export", "init", "clone"}
JJ_NO_SNAPSHOT = {"help", "version"}  # no working copy is read or written
JJ_ARG_OPTS = {"-R", "--repository", "--at-op", "--color", "--config",
               "--config-toml", "-T", "--template"}
JJ_SUB_ARG_OPTS = {"-r", "--revision", "-T", "--template", "--at-op", "--config",
                   "--color", "--repository", "-R"}
JJ_HELP_FLAGS = {"-h", "--help"}
# jj 0.45.1 subcommands whose -h/--help clap answers: the `jj help` list, clap
# aliases op/evolution-log, hidden debug/obslog and default aliases b/ci/desc/st.
JJ_HELP_VERBS = frozenset(
    "abandon absorb arrange b bisect bookmark ci commit config converge debug "
    "desc describe diff diffedit duplicate edit evolog evolution-log file fix "
    "gerrit git help interdiff log metaedit new next obslog op operation "
    "parallelize prev rebase redo resolve restore revert root run show sign "
    "simplify-parents sparse split squash st status tag undo unsign util "
    "version workspace".split())
GIT_WRITE = {"add", "commit", "stash", "checkout", "switch", "reset", "pull",
             "push", "restore", "rebase", "merge", "cherry-pick"}
GIT_ARG_OPTS = {"-C", "-c", "--git-dir", "--work-tree", "--namespace",
                "--exec-path", "--super-prefix", "--config-env"}
# Options that take a SEPARATE value, which parse-options hands the next
# argument even when it starts with `-` (git 2.56.0 `git <sub> --help-all`;
# stash is the union over its subcommands).
GIT_VALUE_OPTS = {verb: frozenset(opts.split()) for verb, opts in {
    "add": "--chmod --inter-hunk-context --pathspec-from-file --unified -U",
    "commit": "--author --cleanup --date --file --fixup --inter-hunk-context "
              "--message --pathspec-from-file --reedit-message --reuse-message "
              "--squash --template --trailer --unified -C -F -U -c -m -t",
    "stash": "--inter-hunk-context --label-base --label-ours --label-theirs "
             "--message --pathspec-from-file --to-ref --unified -U -m",
    "checkout": "--conflict --inter-hunk-context --orphan --pathspec-from-file "
                "--unified -B -U -b",
    "switch": "--conflict --create --force-create --orphan -C -c",
    "reset": "--inter-hunk-context --pathspec-from-file --unified -U",
    "pull": "--cleanup --deepen --depth --negotiation-include "
            "--negotiation-restrict --negotiation-tip --refmap --server-option "
            "--shallow-exclude --shallow-since --strategy --strategy-option "
            "--upload-pack -X -o -s",
    "push": "--exec --push-option --receive-pack --recurse-submodules --repo -o",
    "restore": "--conflict --inter-hunk-context --pathspec-from-file --source "
               "--unified -U -s",
    "rebase": "--empty --exec --onto --strategy --strategy-option --trailer "
              "--whitespace -C -X -s -x",
    "merge": "--cleanup --file --into-name --message --strategy "
             "--strategy-option -F -X -m -s",
    "cherry-pick": "--cleanup --empty --mainline --strategy --strategy-option "
                   "-X -m",
}.items()}
# Negations that undo a dry run; an abbreviation of one keeps the finding.
GIT_DRY_NEGATIONS = {"add": ("--no-dry-run",), "push": ("--no-dry-run",),
                     "commit": ("--no-dry-run", "--no-short", "--no-porcelain",
                                "--no-long", "--no-null")}

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


def verb_index(args, arg_opts):
    """Index of the first positional, skipping flags and the values of arg_opts."""
    skip = False
    for i, a in enumerate(args):
        if skip:
            skip = False
            continue
        if a in arg_opts:
            skip = True
            continue
        if a.startswith("-"):
            continue
        return i
    return None


def first_verb(args, arg_opts):
    i = verb_index(args, arg_opts)
    return None if i is None else args[i]


def sub_verb(args, i):
    """First positional after the verb at args[i], skipping flags and their
    argument values. The index, not the verb's text, anchors the search: a
    global option value may spell the verb (`jj -R git git push`)."""
    rest = args[i + 1:]
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


def before_dashdash(args):
    """The tokens ahead of the first `--` (everything after it is an operand)."""
    return args[:args.index("--")] if "--" in args else args


def ignores_working_copy(args):
    """True when an exact --ignore-working-copy precedes any `--` separator."""
    return "--ignore-working-copy" in before_dashdash(args)


def jj_prints_help(args, i):
    """True when clap answers this jj run with help or a usage error before
    any workspace load: an exact -h/--help before any `--`, ahead of the
    subcommand args[i] or after a JJ_HELP_VERBS one."""
    head = before_dashdash(args)
    if any(a in JJ_HELP_FLAGS for a in head[:i]):
        return True
    return args[i] in JJ_HELP_VERBS and any(a in JJ_HELP_FLAGS for a in head[i + 1:])


def classify_jj(args, exempt=True):
    """Rule for a `jj` run that writes or snapshots the working copy, else None.

    exempt=False (an unparsed segment, whose tokens may belong to the next
    command) applies no help, dry-run or --ignore-working-copy exemption."""
    i = verb_index(args, JJ_ARG_OPTS)
    if i is None:  # `jj`, `jj --version`, `jj --help`: nothing is touched
        return None
    if exempt and jj_prints_help(args, i):
        return None
    verb = {"b": "bookmark", "ci": "commit", "desc": "describe", "st": "status"}.get(args[i], args[i])
    if verb in JJ_WRITE:
        return "jj:" + verb
    if verb == "bookmark":
        if sub_verb(args, i) in JJ_BOOKMARK_WRITE:
            return "jj:bookmark"
    elif verb == "op":
        if sub_verb(args, i) in JJ_OP_WRITE:
            return "jj:op"
    elif verb == "git":
        sub = sub_verb(args, i)
        if sub in JJ_GIT_WRITE and not (
                exempt and sub == "push" and "--dry-run" in before_dashdash(args)):
            return "jj:git"  # a dry-run push only snapshots (rule below)
        if sub == "remote" and any(a in ("add", "remove", "rename", "set-url") for a in args[i + 1:]):
            return "jj:git"
    elif verb == "config" and sub_verb(args, i) in ("set", "unset", "edit"):
        return "jj:config"
    elif verb == "workspace" and sub_verb(args, i) in ("add", "forget", "update-stale"):
        return "jj:workspace"
    elif verb in JJ_NO_SNAPSHOT:
        return None
    return None if exempt and ignores_working_copy(args) else "jj:" + verb


def git_option_flags(verb, rest):
    """Option tokens git's parse-options reads after `verb`, in order.

    A GIT_VALUE_OPTS option (a long one also by unique abbreviation, or a
    short cluster ending in one) takes the next token as its value even when
    it starts with `-`; that value is skipped. A short cluster yields one flag
    per letter (`-nv` is `-n -v`) up to a value-taking letter, whose rest of
    the cluster is its value. `--`/`--end-of-options` stop.
    """
    takes = GIT_VALUE_OPTS.get(verb, frozenset())
    flags, value = [], False
    for a in rest:
        if value:
            value = False
        elif a in ("--", "--end-of-options"):
            break
        elif a.startswith("--"):
            flags.append(a)
            value = "=" not in a and any(t.startswith(a) for t in takes)
        elif a.startswith("-") and a != "-":
            for j, c in enumerate(a[1:], 1):
                flags.append("-" + c)
                if "-" + c in takes:
                    value = j == len(a) - 1
                    break
    return flags


def git_prints_or_simulates(verb, pre, rest):
    """True when `git PRE verb REST` only prints usage/help or is a dry run."""
    skip = False
    for a in pre:  # `git -h <sub>`, `git --help <sub>`
        if skip:
            skip = False
        elif a in GIT_ARG_OPTS:
            skip = True
        elif a in ("-h", "--help"):
            return True
    flags = git_option_flags(verb, rest)
    if "-h" in flags or "--help" in flags:  # usage, or `git help <verb>` if leading
        return True
    if verb == "commit" or verb == "add" and any(
            flag in ("-N", "--intent-to-add") for flag in flags):
        return False  # simulated commit/index preparation can still write
    negations = GIT_DRY_NEGATIONS.get(verb)
    if negations is None:
        return False
    dry = fmt = null = False
    for f in flags:
        if any(n.startswith(f) and n != f for n in negations):
            return False  # an abbreviated negation: not modelled, stays a write
        if (f.startswith("--dry") and "--dry-run".startswith(f)) or (f == "-n" and verb != "commit"):
            dry = True  # commit -n is --no-verify
        elif f == "--no-dry-run":
            dry = False
        elif verb == "commit" and f in ("--short", "--porcelain", "--long"):
            fmt = True  # a status format implies --dry-run
        elif verb == "commit" and f in ("--no-short", "--no-porcelain", "--no-long"):
            fmt = False
        elif verb == "commit" and f in ("-z", "--null"):
            null = True  # -z selects porcelain, hence a dry run
        elif verb == "commit" and f == "--no-null":
            null = False
    return dry or fmt or null


def classify_git(args, exempt=True):
    """Rule for a `git` write, else None (reads, unclassified subcommands,
    help/usage and dry runs). exempt=False (an unparsed segment) applies no
    help or dry-run exemption: a later command's `-h`/`-n` may sit in it."""
    i = verb_index(args, GIT_ARG_OPTS)
    verb = None if i is None else args[i]
    if verb not in GIT_WRITE:
        return None
    if verb == "stash" and sub_verb(args, i) in ("list", "show"):
        return None  # read-only stash inspection
    if exempt and git_prints_or_simulates(verb, args[:i], args[i + 1:]):
        return None
    return "git:" + verb


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
        end = last_unquoted(raw, "}") + 1
        if end > m.end():
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


HELP_EXEMPT_INSTALLS = {"uv:tool-install", "uv:tool-upgrade", "uv:tool-uninstall",
                        "uv:pip-install", "cargo:install", "cargo:uninstall"}


def classify_installer(argv0, args, exempt=True):
    """Return (class, rule) for a tool-acquisition channel, else None.

    Only the argv0-level forms named in the module docstring are classified;
    same-channel tools (pnpm, yarn, bun, brew, nix) are deliberately not. For
    the install/uninstall verbs of uv, pip and cargo an exact `-h`/`--help`
    before any `--` prints help and installs nothing (clap, optparse; round
    20, held-out fx8/fx9). Run forms (uvx, npx, `uv tool run`, pipx run, npm
    exec) pass a trailing `--help` to the package they fetch: no exemption.
    """
    rule = classify_installer_rule(argv0, args)
    if exempt and rule is not None and (
            rule[1] in HELP_EXEMPT_INSTALLS
            or (PIP_RE.match(argv0) and rule[1].endswith(":install"))) \
            and any(a in ("-h", "--help") for a in before_dashdash(args)):
        return None
    if exempt and rule is not None and rule[1] == "uv:tool-run":
        positionals = leading_tokens(args, UV_ARG_OPTS, 3)
        run_index = positionals[1][0] if len(positionals) >= 2 else len(args)
        operand_index = positionals[2][0] if len(positionals) >= 3 else len(args)
        help_args = before_dashdash(args[run_index + 1:operand_index])
        if any(a in ("-h", "--help") for a in help_args) \
                and not any(a in ("--from", "--with", "--with-editable") for a in args):
            return None  # help before PACKAGE belongs to uv, not the fetched tool
    return rule


def classify_installer_rule(argv0, args):
    """The tool_install rule for argv0/args, before the help exemption."""
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
            if (defn is not None and idx >= defn[0]
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
        rule = classify_jj(args, exempt=not unparsed)
        if rule is not None:
            hit("vcs_write", rule)
        return hits
    if argv0 == "git":
        rule = classify_git(args, exempt=not unparsed)
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
    found = classify_installer(argv0, args, exempt=not unparsed)
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

    The resolver serves module variable recipes (folded against the per-cell
    literal environment) and visible-helper arguments (folded against the
    call-site literal environment and bound parameters). It folds primitive
    constants, resolvable names, str concatenation/replace, literal
    lists/tuples/dicts, and starred list/tuple elements whose iterated values
    are themselves literal. Other shapes remain unresolved, never guessed.
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
        values = []
        for elt in node.elts:
            if isinstance(elt, ast.Starred):
                expanded = literal_value(elt.value, env)
                if not isinstance(expanded, (list, tuple)):
                    return LITERAL_MISS
                values.extend(expanded)
            else:
                value = literal_value(elt, env)
                if value is LITERAL_MISS:
                    return LITERAL_MISS
                values.append(value)
        return values
    if isinstance(node, ast.Dict):
        pairs = [(literal_value(key, env), literal_value(value, env))
                 for key, value in zip(node.keys, node.values)]
        if all(isinstance(key, str) and value is not LITERAL_MISS
               for key, value in pairs):
            return dict(pairs)
    return LITERAL_MISS


def literal_node(value):
    """Represent captured literal arguments as valid inert AST, never evaluate."""
    if isinstance(value, (list, tuple)):
        return ast.List(elts=[literal_node(item) for item in value], ctx=ast.Load())
    if isinstance(value, dict):
        return ast.Dict(keys=[literal_node(key) for key in value],
                        values=[literal_node(item) for item in value.values()])
    return ast.Constant(value=value)


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


NAMESPACE_CALLS = {"globals", "locals", "vars"}
NAMESPACE_READERS = {"print", "len", "repr", "str", "sorted", "list", "tuple", "set",
                     "frozenset", "dict", "any", "all", "bool", "iter", "enumerate",
                     "format", "id", "type", "hash"}


def namespace_read_only(parent, call):
    """True when a globals()/locals()/vars() result is only read where it is
    made: discarded, subscripted for a value, tested with `in`, or handed to a
    builtin that only reads it. Any other use may write a name through it."""
    if isinstance(parent, ast.Expr):
        return True
    if isinstance(parent, ast.Subscript) and parent.value is call:
        return isinstance(parent.ctx, ast.Load)
    if isinstance(parent, ast.Compare):
        others = [item for item in [parent.left] + parent.comparators if item is not call]
        return bool(others) and all(isinstance(item, ast.Dict) and not item.keys for item in others)
    return (isinstance(parent, ast.Call) and isinstance(parent.func, ast.Name)
            and parent.func.id in NAMESPACE_READERS
            and any(arg is call for arg in parent.args))


def opaque_module_mutation(tree):
    """True when eager module/class-scope code can rebind names behind the
    resolver's back (exec/eval/builtins rebinding, import *, or a
    globals()/locals()/vars() result used other than for a read)."""
    def scan(node):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
                continue
            if isinstance(child, ast.ImportFrom) and any(a.name == "*" for a in child.names):
                return True
            if isinstance(child, ast.Call) and (dotted(child.func) or "") in OPAQUE_PY_DOTTED:
                if not (dotted(child.func).rsplit(".", 1)[-1] in NAMESPACE_CALLS
                        and namespace_read_only(node, child)):
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


PURE_ARG_CALLS = {  # known builtin callables that do not execute a command
    "print", "list", "tuple", "set", "frozenset", "dict", "type",
    "sorted", "reversed", "repr", "str", "bytes", "len", "any", "all",
    "min", "max", "sum", "enumerate", "zip", "map", "filter", "open",
    "abs", "ascii", "bin", "bool", "bytearray", "callable", "chr",
    "classmethod", "complex", "divmod", "float", "format", "hash", "hex",
    "id", "int", "issubclass", "memoryview", "object", "oct", "ord", "pow",
    "property", "range", "round", "slice", "staticmethod", "super", "vars",
    "dir", "exit", "quit",
    "exec", "eval", "compile", "isinstance", "getattr", "hasattr",
    "setattr", "iter", "next", "input",
}
PURE_STDLIB_MODULES = {
    "collections", "itertools", "operator", "string", "enum",
    "textwrap", "dataclasses",
}
PURE_STDLIB_EXACT = {
    "json.dumps", "pprint.pformat", "pprint.pprint",
    "shlex.join", "shlex.quote", "shlex.split", "typing.NamedTuple",
    "subprocess.list2cmdline",  # argv -> string formatter (S115); never spawns
}
# Finite process/callback inventory, not a proof of module-wide purity.
# Exact formatters and implicit-protocol/callback handling below cover the
# supported transcript forms. S119 supersedes S113's universal inference:
# stdlib membership alone cannot establish that a callable never executes code.
PROCESS_STDLIB = frozenset("""
    os posix nt subprocess pty asyncio multiprocessing concurrent ctypes
    webbrowser pydoc distutils runpy code codeop importlib builtins sys
    threading signal atexit sched weakref contextlib unittest pdb bdb timeit
    profile cProfile trace idlelib tkinter turtle turtledemo ensurepip venv
    zipapp pickle marshal shelve socketserver http xmlrpc site imaplib uuid logging
""".split())
PURE_STDLIB_ALLOW = ("os.path.",)
STDLIB_NAMES = frozenset(getattr(sys, "stdlib_module_names", ()))


def pure_stdlib_path(path):
    if (path in PURE_STDLIB_EXACT
            or any(path.startswith(module + ".") for module in PURE_STDLIB_MODULES)
            or path.startswith("functools.")
            or path.startswith(PURE_STDLIB_ALLOW)
            or (path.startswith("builtins.")
                and path.rsplit(".", 1)[-1] in PURE_ARG_CALLS)):
        return True
    top, dot, _ = path.partition(".")
    return (bool(dot) and top in STDLIB_NAMES and not top.startswith("_")
            and top not in PROCESS_STDLIB)


def spawn_path(path):
    tail = path.rsplit(".", 1)[-1]
    return ((path.startswith("subprocess.") and tail in SPAWN_FUNCS)
            or path in SHELL_STRING_FUNCS
            or path in ("asyncio.create_subprocess_exec", "os.execvp", "os.execv",
                        "os.spawnlp", "os.execlp", "tool.bash",
                        "imaplib.IMAP4_stream", "uuid._get_command_stdout"))


def class_method_info(class_node, method_name, bindings=None, seen=()):
    if not isinstance(class_node, ast.ClassDef) or id(class_node) in seen:
        return None
    for member in class_node.body:
        if (isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef))
                and member.name == method_name):
            static = any((dotted(decorator) or "").rsplit(".", 1)[-1] == "staticmethod"
                         for decorator in member.decorator_list)
            class_method = any((dotted(decorator) or "").rsplit(".", 1)[-1] == "classmethod"
                               for decorator in member.decorator_list)
            return {"kind": "helper", "node": member,
                    "skip_first": not static, "class_node": class_node,
                    "bound_kind": "class" if class_method else
                    "instance" if not static else None}
        if isinstance(member, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == method_name
                for target in member.targets) and isinstance(member.value, ast.Call):
            descriptor = member.value
            if bindings is not None and descriptor.args and \
                    callable_info(descriptor.func, bindings).get("name") == "functools.partialmethod":
                wrapped = callable_info(descriptor.args[0], bindings)
                if wrapped.get("kind") == "helper":
                    return dict(wrapped, skip_first=True, class_node=class_node,
                                bound_kind="instance", fixed_nodes=descriptor.args[1:],
                                fixed_keywords=descriptor.keywords)
    if bindings is not None:
        for base in class_node.bases:
            info = bindings.get(base.id, {}) if isinstance(base, ast.Name) else {}
            if info.get("kind") == "class":
                method = class_method_info(info.get("node"), method_name, bindings,
                                           seen + (id(class_node),))
                if method is not None:
                    return method
    return None


def callable_info(node, bindings):
    """Resolve a callable against the binding in effect at this call site."""
    if isinstance(node, ast.Lambda):
        return {"kind": "helper", "node": node}
    if isinstance(node, ast.Subscript):
        container = node.value
        if isinstance(container, ast.Name):
            container = bindings.get(container.id, {}).get("container")
        index = literal_value(node.slice, {})
        if index is LITERAL_MISS:
            return {"kind": "unresolved"}
        if isinstance(container, ast.Dict):
            for key, value in zip(container.keys, container.values):
                if literal_value(key, {}) == index:
                    return callable_info(value, bindings)
        if isinstance(container, (ast.List, ast.Tuple)) and isinstance(index, int):
            if -len(container.elts) <= index < len(container.elts):
                return callable_info(container.elts[index], bindings)
    if isinstance(node, ast.Name):
        bound = bindings.get(node.id)
        if bound is not None:
            if bound.get("kind") == "instance":
                method = class_method_info(bound.get("node"), "__call__", bindings)
                return method or bound
            return bound
        if node.id in PURE_ARG_CALLS:
            return {"kind": "pure", "name": node.id}
        return {"kind": "unresolved", "name": node.id}
    if isinstance(node, ast.Call):
        constructor = callable_info(node.func, bindings)
        if constructor.get("name") == "typing.cast" and len(node.args) == 2:
            return callable_info(node.args[1], bindings)
        if constructor.get("name") == "functools.partial" and node.args:
            wrapped = callable_info(node.args[0], bindings)
            if wrapped.get("kind") == "helper":
                return dict(wrapped, fixed_nodes=node.args[1:], fixed_keywords=node.keywords)
        if constructor.get("kind") in ("class", "instance"):
            method = class_method_info(constructor.get("node"), "__call__", bindings)
            if method is not None:
                return method
        if constructor.get("kind") == "helper" and isinstance(
                constructor.get("node"), (ast.FunctionDef, ast.AsyncFunctionDef)):
            outer = constructor["node"]
            local = {part.name: part for part in outer.body
                     if isinstance(part, (ast.FunctionDef, ast.AsyncFunctionDef))}
            returned = next((part.value.id for part in outer.body
                             if isinstance(part, ast.Return) and isinstance(part.value, ast.Name)), None)
            if returned in local:
                return {"kind": "helper", "node": local[returned],
                        "capture_owner": outer, "capture_call": node}
            returned_call = next((part.value for part in outer.body
                                  if isinstance(part, ast.Return) and isinstance(part.value, ast.Call)
                                  and callable_info(part.value.func, bindings).get("name") == "functools.partial"), None)
            if returned_call is not None:
                wrapped = callable_info(returned_call, bindings)
                if wrapped.get("kind") == "helper":
                    return dict(wrapped, capture_owner=outer, capture_call=node)
    if isinstance(node, ast.Attribute):
        class_info = None
        if isinstance(node.value, ast.Call):
            class_info = callable_info(node.value.func, bindings)
        elif isinstance(node.value, ast.Name):
            class_info = bindings.get(node.value.id)
        if class_info is not None and class_info.get("kind") == "scheduled" and node.attr == "start":
            return dict(class_info, kind="thread_start")
        if class_info is not None:
            if class_info.get("kind") == "instance":
                method = class_method_info(class_info.get("node"), node.attr, bindings)
                if method is not None:
                    return method
            elif class_info.get("kind") == "class":
                method = class_method_info(class_info.get("node"), node.attr, bindings)
                if method is not None:
                    return method
    raw = dotted(node)
    if not raw:
        return {"kind": "unresolved"}
    head, _, rest = raw.partition(".")
    bound = bindings.get(head)
    if bound is not None:
        if bound.get("kind") != "module":
            return {"kind": "unresolved"}
        path = bound.get("module", "") + ("." + rest if rest else "")
        if spawn_path(path):
            return {"kind": "spawn", "name": path}
        if pure_stdlib_path(path):
            return {"kind": "pure", "name": path}
        return {"kind": "external", "name": path}
    if head == "sp":
        raw = "subprocess." + rest
    if spawn_path(raw):
        return {"kind": "spawn", "name": raw}
    if pure_stdlib_path(raw):
        return {"kind": "pure", "name": raw}
    return {"kind": "unresolved", "name": raw}


def assignment_binding(node, bindings, env):
    """Classify one assigned value without evaluating transcript code."""
    if isinstance(node, (ast.Lambda, ast.FunctionDef, ast.AsyncFunctionDef)):
        return {"kind": "helper", "node": node}
    if isinstance(node, ast.ClassDef):
        return {"kind": "class", "node": node}
    if isinstance(node, ast.Name):
        bound = bindings.get(node.id)
        if bound is not None:
            return dict(bound)
        if node.id in PURE_ARG_CALLS:
            return {"kind": "pure", "name": node.id}
        return {"kind": "unknown"}
    if isinstance(node, ast.Attribute):
        if isinstance(literal_value(node.value, env), str):
            return {"kind": "pure", "name": "str." + node.attr}
        return dict(callable_info(node, bindings))
    if isinstance(node, ast.Call):
        info = callable_info(node.func, bindings)
        if info.get("name") in ("threading.Thread", "threading.Timer"):
            keywords = {keyword.arg: keyword.value for keyword in node.keywords if keyword.arg}
            timer = info["name"] == "threading.Timer"
            target = keywords.get("function" if timer else "target",
                node.args[1] if len(node.args) > 1 else None)
            args_index, kwargs_index = (2, 3) if timer else (3, 4)
            arguments = keywords.get("args", node.args[args_index] if len(node.args) > args_index else None)
            options = keywords.get("kwargs", node.args[kwargs_index] if len(node.args) > kwargs_index else None)
            return {"kind": "scheduled", "node": node,
                    "target": callable_info(target, bindings) if target is not None else {"kind": "unknown"},
                    "args": literal_value(arguments, env) if arguments is not None else (),
                    "kwargs": literal_value(options, env) if options is not None else {}}
        if info.get("name") == "operator.methodcaller" and node.args:
            return {"kind": "methodcaller", "method": literal_value(node.args[0], env),
                    "args": [literal_value(arg, env) for arg in node.args[1:]],
                    "keywords": {keyword.arg: literal_value(keyword.value, env)
                                 for keyword in node.keywords if keyword.arg is not None}}
        returned = callable_info(node, bindings)
        if returned.get("kind") == "helper":
            return returned
        if info.get("name") == "importlib.import_module" and len(node.args) == 1 \
                and not node.keywords:
            module = literal_value(node.args[0], env)
            if isinstance(module, str) and module and not module.startswith("."):
                return {"kind": "module", "module": module}
        if info.get("kind") == "pure" and info.get("name") == "functools.partial" \
                and node.args:
            wrapped = callable_info(node.args[0], bindings)
            if wrapped.get("kind") == "spawn":
                return {
                    "kind": "spawn", "name": wrapped["name"],
                    "partial_args": [literal_value(a, env) for a in node.args[1:]],
                    "partial_keywords": {
                        k.arg: literal_value(k.value, env)
                        for k in node.keywords if k.arg is not None
                    },
                }
        if info.get("kind") == "pure" and info.get("name") in (
                "collections.namedtuple", "typing.NamedTuple"):
            return {"kind": "class"}
        if info.get("kind") == "class":
            return {"kind": "instance", "node": info.get("node")}
        if info.get("kind") == "pure":
            return {"kind": "value"}
        return {"kind": "unknown"}
    if isinstance(node, (ast.List, ast.Tuple, ast.Dict)):
        return {"kind": "value", "container": node}
    if isinstance(node, (ast.Constant, ast.Set, ast.BinOp, ast.UnaryOp, ast.JoinedStr)):
        return {"kind": "value"}
    return {"kind": "unknown"}


def update_bindings(stmt, bindings, env):
    """Apply this statement's module-level name bindings in execution order."""
    if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
        bindings[stmt.name] = {"kind": "helper", "node": stmt}
        for decorator in reversed(stmt.decorator_list):
            wrapped = callable_info(ast.Call(func=decorator,
                args=[ast.Name(id=stmt.name, ctx=ast.Load())], keywords=[]), bindings)
            if wrapped.get("kind") == "helper":
                bindings[stmt.name] = wrapped
        return
    if isinstance(stmt, ast.ClassDef):
        bindings[stmt.name] = {"kind": "class", "node": stmt}
        return
    if isinstance(stmt, ast.Import):
        for alias in stmt.names:
            name = alias.asname or alias.name.split(".")[0]
            module = alias.name if alias.asname else alias.name.split(".")[0]
            bindings[name] = {"kind": "module", "module": module}
        return
    if isinstance(stmt, ast.ImportFrom):
        for alias in stmt.names:
            if alias.name == "*":
                continue
            name = alias.asname or alias.name
            path = (stmt.module + "." + alias.name) if stmt.module else alias.name
            if spawn_path(path):
                bindings[name] = {"kind": "spawn", "name": path}
            elif pure_stdlib_path(path):
                bindings[name] = {"kind": "pure", "name": path}
            else:
                bindings[name] = {"kind": "external", "name": path}
        return
    if isinstance(stmt, (ast.Assign, ast.AnnAssign)):
        value = stmt.value
        resolved = assignment_binding(value, bindings, env) if value is not None \
            else {"kind": "unknown"}
        targets = stmt.targets if isinstance(stmt, ast.Assign) else [stmt.target]
        names = set().union(*(target_names(target) for target in targets))
        for name in names:
            bindings[name] = (dict(resolved) if all(isinstance(target, ast.Name) for target in targets)
                              else {"kind": "unknown"})
        return
    if isinstance(stmt, ast.Delete):
        for target in stmt.targets:
            for name in target_names(target):
                if name in PURE_ARG_CALLS:
                    bindings.pop(name, None)
                else:
                    bindings[name] = {"kind": "deleted"}
        return
    if isinstance(stmt, (ast.AugAssign, ast.NamedExpr)):
        target = stmt.target
        for name in target_names(target):
            bindings[name] = {"kind": "unknown"}
        return
    # A branch/loop may or may not bind a name. Do not keep an earlier
    # exemption or helper as if the execution were straight-line.
    def visit(current):
        if isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if current is not stmt:
                bindings[current.name] = {"kind": "unknown"}
            return
        if isinstance(current, ast.Lambda):
            return
        if isinstance(current, (ast.Assign, ast.AnnAssign, ast.AugAssign,
                                ast.NamedExpr, ast.Delete)):
            targets = (current.targets if isinstance(current, ast.Assign)
                       else [current.target] if hasattr(current, "target")
                       else current.targets)
            for target in targets:
                for name in target_names(target):
                    bindings[name] = {"kind": "unknown"}
        elif isinstance(current, (ast.Import, ast.ImportFrom)):
            for alias in current.names:
                if alias.name != "*":
                    bindings[alias.asname or alias.name.split(".")[0]] = {
                        "kind": "unknown"}
        elif isinstance(current, (ast.For, ast.AsyncFor, ast.comprehension)):
            for name in target_names(current.target):
                bindings[name] = {"kind": "unknown"}
        elif isinstance(current, ast.withitem) and current.optional_vars is not None:
            for name in target_names(current.optional_vars):
                bindings[name] = {"kind": "unknown"}
        elif isinstance(current, ast.ExceptHandler) and current.name:
            bindings[current.name] = {"kind": "unknown"}
        elif isinstance(current, (ast.Global, ast.Nonlocal)):
            for name in current.names:
                bindings[name] = {"kind": "unknown"}
        elif MATCH_BINDERS and isinstance(current, MATCH_BINDERS):
            name = getattr(current, "name", None) or getattr(current, "rest", None)
            if name:
                bindings[name] = {"kind": "unknown"}
        for child in ast.iter_child_nodes(current):
            visit(child)
    visit(stmt)


def eager_calls(nodes):
    """Calls executed when these statements run, in source pre-order, and the
    callable references they hand on.

    A reference is a name or attribute loaded as a value rather than called
    here (paired with the call that receives it as an argument, if any), a
    bare decorator, or a lambda not bound by a plain assignment. Deferred
    bodies are skipped. The walk is iterative, so expression depth cannot
    exhaust the interpreter stack.
    """
    calls, refs = [], []
    skip, parents, assigned = set(), {}, set()
    stack = list(reversed(list(nodes)))
    while stack:
        node = stack.pop()
        if isinstance(node, (ast.With, ast.AsyncWith)):
            for item in node.items:
                refs.extend((item.context_expr, ("protocol", method))
                            for method in ("__enter__", "__exit__"))
        elif isinstance(node, (ast.For, ast.AsyncFor)):
            refs.append((node.iter, ("protocol", "__iter__")))
            names = target_names(node.target)
            if any(isinstance(part, ast.Call) and isinstance(part.func, ast.Name)
                   and part.func.id in names for stmt in node.body for part in ast.walk(stmt)):
                for part in ast.walk(node.iter):
                    parents[id(part)] = "invoke"
        elif isinstance(node, ast.Compare):
            refs.append((node.left, ("protocol", "__eq__")))
        elif isinstance(node, ast.BinOp):
            method = {ast.Add: "__add__", ast.Sub: "__sub__", ast.Mult: "__mul__",
                      ast.Div: "__truediv__", ast.MatMult: "__matmul__",
                      ast.Mod: "__mod__", ast.BitOr: "__or__", ast.BitAnd: "__and__"}.get(type(node.op))
            if method:
                refs.append((node.left, ("protocol", method)))
        elif isinstance(node, ast.Subscript) and isinstance(node.ctx, ast.Load):
            refs.append((node.value, ("protocol", "__getitem__")))
        elif isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Load):
            refs.append((node.value, ("protocol", "__getattr__")))
        if isinstance(node, ast.Call):
            for arg in node.args + [keyword.value for keyword in node.keywords]:
                refs.append((arg, ("argument_protocol", node)))
            if isinstance(node.func, ast.Name) and node.func.id in ("isinstance", "issubclass") and len(node.args) > 1:
                refs.append((node.args[1], ("metaclass_protocol",
                    "__instancecheck__" if node.func.id == "isinstance" else "__subclasscheck__")))
            if isinstance(node.func, ast.Name) and node.func.id in ("print", "repr", "str", "iter", "list", "tuple"):
                for arg in node.args:
                    refs.append((arg, ("protocol", "__repr__" if node.func.id == "repr"
                                      else "__str__" if node.func.id in ("str", "print") else "__iter__")))
            if not isinstance(node.func, (ast.Name, ast.Attribute)):
                for part in ast.walk(node.func):
                    parents[id(part)] = "invoke"
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                refs.append((base, ("protocol", "__init_subclass__")))
            for decorator in node.decorator_list:
                if isinstance(decorator, (ast.Name, ast.Attribute, ast.Call)):
                    refs.append((decorator, "decorator"))
                    skip.add(id(decorator))
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for expr in node.decorator_list:
                if isinstance(expr, (ast.Name, ast.Attribute, ast.Call)):
                    refs.append((expr, "decorator"))  # applied, not a stored value
                    skip.add(id(expr))
            children = list(node.decorator_list) + [
                expr for expr in node.args.defaults + node.args.kw_defaults
                if expr is not None]
        elif isinstance(node, ast.Lambda):
            if id(node) not in assigned and id(node) in parents:
                refs.append((node, parents[id(node)]))
            children = [expr for expr in node.args.defaults + node.args.kw_defaults
                        if expr is not None]
        else:
            if isinstance(node, ast.Call):
                calls.append(node)
                if id(node) in parents:
                    refs.append((node, parents[id(node)]))
                skip.add(id(node.func))
                for arg in node.args + [keyword.value for keyword in node.keywords]:
                    parents.setdefault(id(arg.value if isinstance(arg, ast.Starred) else arg), node)
            elif isinstance(node, (ast.Assign, ast.AnnAssign)) and \
                    isinstance(node.value, ast.Lambda):
                assigned.add(id(node.value))  # a binding; its calls are followed
            elif isinstance(node, ast.Attribute):
                skip.add(id(node.value))
                if isinstance(node.ctx, ast.Load) and id(node) not in skip and id(node) in parents:
                    refs.append((node, parents[id(node)]))
            elif isinstance(node, ast.Name):
                if isinstance(node.ctx, ast.Load) and id(node) not in skip and id(node) in parents:
                    refs.append((node, parents[id(node)]))
            children = ([node.value] if isinstance(node, ast.AnnAssign) and node.value is not None
                        else [] if isinstance(node, ast.AnnAssign)
                        else list(ast.iter_child_nodes(node)))
        stack.extend(reversed(children))
    return calls, refs


def bind_literal(fn, call, env=None, skip_first=False):
    """Bind literal helper arguments and retain unknown values as unresolved.

    A starred argument binds only when its value is a literal list/tuple
    (`run(*['pacman', '-Q'])`); any other starred argument leaves the call
    unbound (None)."""
    env = {} if env is None else env
    values = []
    for arg in call.args:
        if isinstance(arg, ast.Starred):
            expanded = literal_value(arg.value, env)
            if not isinstance(expanded, (list, tuple)):
                return None
            values.extend(expanded)
        else:
            values.append(literal_value(arg, env))
    all_params = [arg.arg for arg in fn.args.posonlyargs + fn.args.args]
    offset = 1 if skip_first else 0
    params = all_params[offset:]
    vararg = fn.args.vararg.arg if fn.args.vararg else None
    kwarg = fn.args.kwarg.arg if fn.args.kwarg else None
    kwonly_params = [arg.arg for arg in fn.args.kwonlyargs]
    keyword_params = {arg.arg for arg in fn.args.args + fn.args.kwonlyargs}
    if len(values) > len(params) and vararg is None:
        return None
    bound = {all_params[0]: None} if skip_first and all_params else {}
    for name, value in zip(params, values):
        bound[name] = value
    extra_args = values[len(params):]
    if vararg is not None:
        bound[vararg] = extra_args
    extra_keywords = {}
    for keyword in call.keywords:
        value = literal_value(keyword.value, env)
        if keyword.arg is None:
            if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
                return None
            for key, item in value.items():
                if key in bound:
                    return None
                if key in keyword_params:
                    bound[key] = item
                elif kwarg is not None:
                    extra_keywords[key] = item
                else:
                    return None
        elif keyword.arg in keyword_params:
            if keyword.arg in bound:
                return None
            bound[keyword.arg] = value
        elif kwarg is not None:
            if extra_keywords is not LITERAL_MISS:
                extra_keywords[keyword.arg] = value
        else:
            return None
    if kwarg is not None:
        bound[kwarg] = extra_keywords
    elif extra_keywords:
        return None
    first_default = len(all_params) - len(fn.args.defaults)
    for index, name in enumerate(params, offset):
        if name in bound:
            continue
        if index < first_default:
            return None
        bound[name] = literal_value(fn.args.defaults[index - first_default], {})
    for name, default in zip(kwonly_params, fn.args.kw_defaults):
        if name not in bound:
            if default is None:
                return None
            bound[name] = literal_value(default, {})
    return bound


def prepare_eval_calls(statements, env, bindings):
    """Snapshot literals and bindings at each statement, then retain its updates.

    Returns the statements' eager calls and references and, for every call,
    name, attribute and lambda, the literal environment and bindings in effect
    at its statement (one shared snapshot per statement; never mutated)."""
    tree = ast.Module(body=statements, type_ignores=[])
    unsafe = module_unsafe_names(tree)
    for name in unsafe:
        env.pop(name, None)
    call_env, binding_env = {}, {}
    # Retain snapshots only for inspected eager calls/references, not every
    # literal assignment in a wide shallow cell.
    calls, refs = [], []
    for stmt in statements:
        stmt_calls, stmt_refs = eager_calls([stmt])
        calls.extend(stmt_calls)
        refs.extend(stmt_refs)
        if stmt_calls or stmt_refs:
            stmt_env, stmt_bindings = dict(env), dict(bindings)
            for node in stmt_calls + [ref for ref, _ in stmt_refs]:
                call_env[id(node)] = stmt_env
                binding_env[id(node)] = stmt_bindings
        if opaque_statement(stmt):
            env.clear()
            bindings.clear()
            for name in PURE_ARG_CALLS:
                bindings[name] = {"kind": "unknown"}
        binding = module_binding(stmt)
        if binding is not None:
            name, value = binding
            resolved = LITERAL_MISS if name in unsafe else literal_value(value, env)
            if resolved is LITERAL_MISS:
                env.pop(name, None)
            else:
                env[name] = resolved
        update_bindings(stmt, bindings, env)
    return calls, refs, call_env, binding_env


def awaited_call_ids(statements):
    return {id(node.value) for stmt in statements for node in ast.walk(stmt)
            if isinstance(node, ast.Await) and isinstance(node.value, ast.Call)}

def classify_eval(code, language, env=None, bindings=None):
    """Return hits and unparsed counters; both Python environments persist per file."""
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
    except Exception:
        return hits, 1, 0
    env = {} if env is None else env
    bindings = {} if bindings is None else bindings
    calls, refs, call_env, binding_env = prepare_eval_calls(tree.body, env, bindings)
    found, unparsed = spawn_scan(
        calls, {}, bindings, 0, call_env, binding_env, awaited_call_ids(tree.body),
        refs, new_scan_context())
    hits.extend(found)
    return hits, 0, unparsed


def helper_argv_leads(node, env):
    """Mark literal argv passed to a callee whose body is not visible."""
    out = []
    for arg in node.args:
        vals = argv_strings(literal_value(arg, env))
        if vals is not None:
            out.extend(tuple(hit) + ("lead",)
                       for hit in classify_shell(shlex.join(vals)))
    return out


def spawn_attr_leads(node, env):
    """Lead rows for a spawn-named method of an object the scan cannot resolve
    (`sp = other; sp.run([...])`): a literal argv, or a literal command string
    when the method takes one (`system`/`popen`) or `shell=` is not literal false."""
    out = helper_argv_leads(node, env)
    value = literal_value(node.args[0], env) if node.args else LITERAL_MISS
    if isinstance(value, str):
        shell = next((literal_value(k.value, env) for k in node.keywords
                      if k.arg == "shell"), False)
        if node.func.attr in ("system", "popen") or shell is not False:
            out.extend(tuple(hit) + ("lead",) for hit in classify_shell(value))
    return out


def callback_argv_leads(call, env, shell_string=False):
    """Lead rows for literal argv handed, beside a spawn callable, to the call
    that receives it (`Thread(target=subprocess.run, args=(argv,))`); for a
    shell-string callable (`os.system`) also its literal command strings."""
    out = []
    pending = [literal_value(arg.value if isinstance(arg, ast.Starred) else arg, env)
               for arg in call.args]
    pending += [literal_value(keyword.value, env) for keyword in call.keywords]
    while pending:
        value = pending.pop(0)
        vals = argv_strings(value)
        if vals is not None:
            out.extend(tuple(hit) + ("lead",) for hit in classify_shell(shlex.join(vals)))
        elif isinstance(value, (list, tuple)):
            pending.extend(value)
        elif isinstance(value, dict):
            pending.extend(value.values())
        elif shell_string and isinstance(value, str):
            out.extend(tuple(hit) + ("lead",) for hit in classify_shell(value))
    return out


DESCENT_LIMIT = 4  # nested helper bodies followed with bound literals
DESCENT_BUDGET = 2000  # helper descents per cell; past it, bodies are swept


def new_scan_context():
    """Per-cell state: bodies already swept, helpers being followed, descents."""
    return {"swept": set(), "stack": [], "descents": 0}


def callable_params(fn):
    spec = fn.args
    names = [arg.arg for arg in spec.posonlyargs + spec.args + spec.kwonlyargs]
    return names + [arg.arg for arg in (spec.vararg, spec.kwarg) if arg is not None]


def sweep_body(owner, bindings, ctx, depth, class_node=None, bound_kind=None):
    """Lead rows for a visible body that may run on a path this scan does not
    follow with bound literals: a callable handed on as a value, a scheduled
    coroutine, a bare decorator, a dunder of a constructed or used class, an
    inline lambda, a recursive or over-budget helper, or a call whose
    arguments cannot be bound. Its parameters are unknown; every row it finds
    is a `lead`. Each body is swept at most once per cell and never while it
    is being followed; a body nothing references stays silent."""
    if id(owner) in ctx["swept"] or id(owner) in ctx["stack"]:
        return [], 0
    ctx["swept"].add(id(owner))
    if isinstance(owner, ast.ClassDef):
        return sweep_class(owner, bindings, ctx, depth, dunders_only=False)
    body = [owner.body] if isinstance(owner, ast.Lambda) else owner.body
    body_bindings = dict(bindings)
    for name in callable_params(owner):
        body_bindings[name] = {"kind": "parameter"}
    positional = owner.args.posonlyargs + owner.args.args
    if class_node is not None and bound_kind and positional:
        body_bindings[positional[0].arg] = {"kind": bound_kind, "node": class_node}
    calls, refs, call_env, binding_env = prepare_eval_calls(body, {}, body_bindings)
    ctx["stack"].append(id(owner))
    try:
        found, unparsed = spawn_scan(calls, {}, body_bindings, depth + 1, call_env,
                                     binding_env, awaited_call_ids(body), refs, ctx)
    finally:
        ctx["stack"].pop()
    return [tuple(hit[:4]) + ("lead",) for hit in found], unparsed


def sweep_class(class_node, bindings, ctx, depth, dunders_only, exclude=()):
    """Sweep a class's methods; only its dunders for a constructed or used
    instance (`__enter__`/`__exit__`, `__del__`, `__post_init__`, ...)."""
    hits, unparsed = [], 0
    for member in class_node.body:
        if not isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef)) or \
                id(member) in exclude:
            continue
        if dunders_only and not (member.name.startswith("__")
                                 and member.name.endswith("__")):
            continue
        info = class_method_info(class_node, member.name) or {}
        found, missed = sweep_body(member, bindings, ctx, depth, class_node,
                                   info.get("bound_kind"))
        hits.extend(found)
        unparsed += missed
    return hits, unparsed


def follow_helper(helper, node, cenv, cbindings, ctx, depth, skip_first=False,
                  class_node=None, bound_kind=None):
    """Follow one helper call with its literal arguments bound (`observed`
    rows), or None when it is not followed: recursion, depth or budget spent,
    or arguments that cannot be bound."""
    if id(helper) in ctx["stack"] or depth >= DESCENT_LIMIT or \
            ctx["descents"] >= DESCENT_BUDGET:
        return None
    bound = bind_literal(helper, node, cenv, skip_first=skip_first)
    if bound is None:
        return None
    ctx["descents"] += 1
    body_nodes = [helper.body] if isinstance(helper, ast.Lambda) else helper.body
    body_bindings = dict(cbindings)
    body_bindings.update({
        name: {"kind": "parameter" if value is LITERAL_MISS else "value"}
        for name, value in bound.items()
    })
    positional = helper.args.posonlyargs + helper.args.args
    defaults = dict(zip((arg.arg for arg in positional[-len(helper.args.defaults):]),
                        helper.args.defaults)) if helper.args.defaults else {}
    supplied = {parameter.arg: argument for parameter, argument in zip(
        positional[1:] if skip_first else positional, node.args)}
    supplied.update({keyword.arg: keyword.value for keyword in node.keywords if keyword.arg})
    for parameter in callable_params(helper):
        argument = supplied.get(parameter, defaults.get(parameter))
        if argument is not None:
            resolved = assignment_binding(argument, cbindings, cenv)
            if resolved.get("kind") in ("helper", "spawn", "class", "instance"):
                body_bindings[parameter] = resolved
    if class_node is not None and bound_kind:
        params = helper.args.posonlyargs + helper.args.args
        if params:
            body_bindings[params[0].arg] = {"kind": bound_kind, "node": class_node}
    body_env = dict(cenv)
    body_env.update(bound)
    calls, refs, body_call_env, body_binding_env = prepare_eval_calls(
        body_nodes, body_env, body_bindings)
    ctx["stack"].append(id(helper))
    try:
        return spawn_scan(calls, body_env, body_bindings, depth + 1, body_call_env,
                          body_binding_env, awaited_call_ids(body_nodes), refs, ctx)
    finally:
        ctx["stack"].pop()


def spawn_scan(nodes, env, bindings, depth=0, call_env=None, binding_env=None,
               awaited_calls=None, refs=(), ctx=None):
    """Follow visible helper calls and classify reachable spawn calls; sweep
    referenced bodies the call path does not follow (see sweep_body)."""
    hits, unparsed = [], 0
    resolved_callees = set()
    awaited_calls = set() if awaited_calls is None else awaited_calls
    ctx = new_scan_context() if ctx is None else ctx

    def take(result):
        nonlocal unparsed
        hits.extend(result[0])
        unparsed += result[1]

    for node in nodes:
        if not isinstance(node, ast.Call):
            continue
        cenv = env if call_env is None else call_env.get(id(node), {})
        cbindings = bindings if binding_env is None else binding_env.get(id(node), {})
        info = callable_info(node.func, cbindings)
        if isinstance(node.func, ast.Attribute) and node.func.attr == "start" and isinstance(node.func.value, ast.Call):
            scheduled = assignment_binding(node.func.value, cbindings, cenv)
            if scheduled.get("kind") == "scheduled":
                info = dict(scheduled, kind="thread_start")
        if info.get("kind") == "thread_start":
            local_bindings = dict(cbindings)
            local_bindings["__mado_thread_target__"] = info["target"]
            arguments = info["args"] if info["args"] is not None else ()
            options = info["kwargs"] if info["kwargs"] is not None else {}
            if isinstance(arguments, (list, tuple)) and isinstance(options, dict) and all(isinstance(key, str) for key in options):
                invocation = ast.Call(func=ast.Name(id="__mado_thread_target__", ctx=ast.Load()),
                    args=[literal_node(value) for value in arguments],
                    keywords=[ast.keyword(arg=key, value=literal_node(value))
                              for key, value in options.items()])
                take(spawn_scan([invocation], cenv, local_bindings, depth + 1, ctx=ctx))
            else:
                unparsed += 1
            continue
        if info.get("kind") == "methodcaller" and node.args and isinstance(info.get("method"), str):
            callee = node.args[0] if info["method"] == "__call__" else ast.Attribute(
                value=node.args[0], attr=info["method"], ctx=ast.Load())
            invocation = ast.Call(func=callee,
                args=[literal_node(value) for value in info["args"]],
                keywords=[ast.keyword(arg=key, value=literal_node(value))
                          for key, value in info["keywords"].items()])
            take(spawn_scan([invocation], cenv, cbindings, depth + 1, ctx=ctx))
            continue
        if isinstance(node.func, ast.Call) and node.args:
            builder = node.func
            builder_info = callable_info(builder.func, cbindings)
            if builder_info.get("name") == "operator.methodcaller" and builder.args:
                method = literal_value(builder.args[0], cenv)
                if isinstance(method, str):
                    callee = node.args[0] if method == "__call__" else ast.Attribute(
                        value=node.args[0], attr=method, ctx=ast.Load())
                    invocation = ast.Call(func=callee, args=builder.args[1:], keywords=builder.keywords)
                    take(spawn_scan([invocation], cenv, cbindings, depth + 1, ctx=ctx))
                    continue
        helper = info.get("node")
        if info.get("capture_owner") is not None:
            captured = bind_literal(info["capture_owner"], info["capture_call"], cenv)
            if captured is not None:
                captured_env, captured_bindings = dict(cenv), dict(cbindings)
                captured_env.update(captured)
                prefix = []
                for statement in info["capture_owner"].body:
                    if isinstance(statement, ast.Return):
                        break
                    prefix.append(statement)
                prepare_eval_calls(prefix, captured_env, captured_bindings)
                cenv, cbindings = captured_env, captured_bindings
        config_arg = (node.args[0] if node.args else
                      next((keyword.value for keyword in node.keywords if keyword.arg == "config"), None))
        if info.get("name") == "logging.config.dictConfig" and config_arg is not None:
            if isinstance(config_arg, ast.Name):
                config_arg = cbindings.get(config_arg.id, {}).get("container")
            if not isinstance(config_arg, ast.Dict):
                continue
            sections = {key.value: value for key, value in zip(config_arg.keys, config_arg.values)
                        if isinstance(key, ast.Constant) and isinstance(key.value, str)}
            incremental = literal_value(sections.get("incremental", ast.Constant(value=False)), cenv)
            if incremental is True:
                continue  # incremental mode changes existing levels, not factories
            for section in ("formatters", "filters", "handlers"):
                entries = sections.get(section)
                if not isinstance(entries, ast.Dict):
                    continue
                for config in entries.values:
                    if not isinstance(config, ast.Dict):
                        continue
                    values = {key.value: value for key, value in zip(config.keys, config.values)
                              if isinstance(key, ast.Constant) and isinstance(key.value, str)}
                    factory = values.get("()")
                    if factory is not None:
                        invocation = ast.Call(func=factory, args=[],
                            keywords=[ast.keyword(arg=key, value=value) for key, value in values.items() if key not in ("()", ".")])
                        result = spawn_scan([invocation], cenv, cbindings, depth + 1, ctx=ctx)
                        if incremental is LITERAL_MISS:
                            result = ([tuple(hit[:4]) + ("lead",) for hit in result[0]], result[1])
                        take(result)
            continue
        if info.get("kind") == "helper" and helper is not None:
            if id(helper) in ctx["stack"]:  # recursion: the body is already in scan
                hits.extend(callback_argv_leads(
                    node, cenv, any(isinstance(part, ast.Call)
                        and (dotted(part.func) or "") in SHELL_STRING_FUNCS
                        or isinstance(part, ast.keyword) and part.arg == "shell"
                        and isinstance(part.value, ast.Constant) and part.value.value is True
                        for part in ast.walk(helper))))
                continue
            bound_node = node
            if info.get("fixed_nodes") or info.get("fixed_keywords"):
                bound_node = ast.Call(func=node.func,
                    args=list(info.get("fixed_nodes", ())) + node.args,
                    keywords=list(info.get("fixed_keywords", ())) + node.keywords)
            result = follow_helper(helper, bound_node, cenv, cbindings, ctx, depth,
                                   info.get("skip_first", False),
                                   info.get("class_node"), info.get("bound_kind"))
            if result is not None and isinstance(helper, ast.AsyncFunctionDef) \
                    and id(node) not in awaited_calls:
                # a coroutine created here runs only if something schedules it
                result = ([tuple(hit[:4]) + ("lead",) for hit in result[0]], result[1])
            if result is None:  # not followed: sweep the body instead
                result = sweep_body(helper, cbindings, ctx, depth,
                                    info.get("class_node"), info.get("bound_kind"))
            resolved_callees.update(id(part) for part in ast.walk(node.func))
            take(result)
            continue
        if info.get("kind") == "helper":
            continue
        if info.get("kind") == "class":
            if isinstance(helper, ast.ClassDef):
                init_info = class_method_info(helper, "__init__", cbindings)
                init = init_info.get("node") if init_info else None
                followed = ()
                if init is not None:
                    result = follow_helper(init, node, cenv, cbindings, ctx, depth, True,
                                           helper, "instance")
                    if result is not None:
                        followed = (id(init),)
                        take(result)
                if any((dotted(decorator.func if isinstance(decorator, ast.Call) else decorator) or "")
                       .rsplit(".", 1)[-1] == "dataclass" for decorator in helper.decorator_list):
                    post = class_method_info(helper, "__post_init__", cbindings)
                    if post is not None:
                        take(sweep_body(post["node"], cbindings, ctx, depth, helper, "instance"))
                # Construction does not invoke every operator/context dunder.
                for member in helper.body:
                    if isinstance(member, ast.FunctionDef) and member.name in ("__new__", "__del__"):
                        take(sweep_body(member, cbindings, ctx, depth, helper, "instance"))
            continue
        if info.get("kind") in ("pure", "value"):
            continue
        if info.get("kind") in ("unresolved", "external", "deleted",
                                "unknown", "parameter"):
            if isinstance(node.func, ast.Name):
                hits.extend(helper_argv_leads(node, cenv))
            elif isinstance(node.func, ast.Attribute) and (
                    node.func.attr in SPAWN_FUNCS
                    or node.func.attr in ("system", "popen")):
                hits.extend(spawn_attr_leads(node, cenv))
            continue
        if info.get("name") == "uuid._get_command_stdout":
            values = [literal_value(arg, cenv) for arg in node.args]
            if values and all(isinstance(value, str) for value in values):
                hits.extend(tuple(hit[:4]) + ("lead",)
                            for hit in classify_shell(shlex.join(values)))
            else:
                unparsed += 1
            continue
        name = info.get("name", "")
        tail = name.rsplit(".", 1)[-1]
        is_sub = name.startswith("subprocess.") and tail in SPAWN_FUNCS
        is_shell_fn = name in SHELL_STRING_FUNCS
        is_exec = name in ("asyncio.create_subprocess_exec", "os.execvp", "os.execv",
                           "os.spawnlp", "os.execlp")
        is_tool = name == "tool.bash"
        if not (info.get("kind") == "spawn" or is_sub or is_shell_fn or is_exec or is_tool):
            continue
        fixed_args = info.get("partial_args", [])
        call_args = list(fixed_args)
        for arg in node.args:
            if isinstance(arg, ast.Starred):
                values = literal_value(arg.value, cenv)
                if isinstance(values, (list, tuple)):
                    call_args.extend(values)
                else:
                    call_args.append(LITERAL_MISS)
            else:
                call_args.append(literal_value(arg, cenv))
        call_kwargs = dict(info.get("partial_keywords", {}))
        for keyword in node.keywords:
            value = literal_value(keyword.value, cenv)
            if keyword.arg is None and isinstance(value, dict):
                call_kwargs.update(value)
            elif keyword.arg is not None:
                call_kwargs[keyword.arg] = value
        if is_tool:
            arg = node.args[0] if node.args else None
            cmd = None
            if isinstance(arg, ast.Dict):
                for key, value in zip(arg.keys, arg.values):
                    if isinstance(key, ast.Constant) and key.value == "command":
                        value = literal_value(value, cenv)
                        if isinstance(value, str):
                            cmd = value
            if cmd is None:
                unparsed += 1
            else:
                hits.extend(classify_shell(cmd))
            continue
        if is_exec:
            if call_args and all(isinstance(value, str) for value in call_args):
                hits.extend(classify_shell(shlex.join(call_args)))
            else:
                unparsed += 1
            continue
        shell_kw = call_kwargs.get("shell", True)
        if shell_kw is LITERAL_MISS:
            shell_kw = True
        value = call_args[0] if call_args else call_kwargs.get("args", LITERAL_MISS)
        argv = argv_strings(value)
        if argv is not None:
            hits.extend(classify_shell(argv[0] if argv else "") if name == "imaplib.IMAP4_stream"
                        else classify_shell(shlex.join(argv)))
        elif isinstance(value, str):
            hits.extend(classify_shell(value) if (is_shell_fn or bool(shell_kw))
                        else classify_shell(shlex.quote(value)))
        else:
            unparsed += 1
    for ref, parent in refs:
        if parent == "invoke" and id(ref) in resolved_callees:
            continue
        rbindings = bindings if binding_env is None else binding_env.get(id(ref), {})
        if isinstance(parent, tuple):
            mode, method = parent
            if mode == "argument_protocol":
                consumer = callable_info(method.func, rbindings).get("name", "")
                if consumer == "json.dumps" and any(
                        keyword.arg == "default" and keyword.value is ref for keyword in method.keywords):
                    callback = callable_info(ref, rbindings)
                    if callback.get("kind") == "helper":
                        take(sweep_body(callback["node"], rbindings, ctx, depth))
                if consumer not in ("shlex.join", "collections.deque", "list", "tuple", "set",
                                     "frozenset", "sorted", "sum", "any", "all", "min", "max"):
                    continue
                method = "__iter__"
            receiver = (callable_info(ref.func, rbindings) if isinstance(ref, ast.Call)
                        else rbindings.get(ref.id, {}) if isinstance(ref, ast.Name) else {})
            target = receiver.get("node")
            if receiver.get("kind") == "class" and not isinstance(ref, ast.Call) and \
                    method != "__init_subclass__" and isinstance(target, ast.ClassDef):
                meta = next((keyword.value for keyword in target.keywords if keyword.arg == "metaclass"), None)
                receiver = rbindings.get(meta.id, {}) if isinstance(meta, ast.Name) else {}
                target = receiver.get("node")
                mode = "metaclass_protocol"
            if receiver.get("kind") == "instance" or isinstance(ref, ast.Call) and receiver.get("kind") == "class" \
                    or mode == "metaclass_protocol" and receiver.get("kind") == "class" \
                    or method == "__init_subclass__" and receiver.get("kind") == "class":
                info = class_method_info(target, method, rbindings)
                if info is None and method == "__str__":
                    info = class_method_info(target, "__repr__", rbindings)
                if info is not None:
                    take(sweep_body(info["node"], rbindings, ctx, depth,
                                    info.get("class_node"), info.get("bound_kind")))
            continue
        if parent not in ("decorator", "invoke"):
            parent_info = callable_info(parent.func, rbindings)
            parent_name = parent_info.get("name", "")
            # Value-only builtins/formatters and partial construction do not
            # execute function bodies or a class's instance methods.
            higher_order = parent_name in ("map", "filter", "sorted", "min", "max", "functools.reduce")
            if parent_info.get("kind") in ("pure", "value") and not higher_order:
                continue
            if parent_info.get("kind") == "class":
                continue
        if isinstance(parent, ast.Call):
            pinfo = callable_info(parent.func, rbindings)
            if pinfo.get("name") in ("threading.Thread", "threading.Timer"):
                continue  # explicit/aliased start calls own the captured target
        if isinstance(ref, ast.Lambda):
            take(sweep_body(ref, rbindings, ctx, depth))
            continue
        info = callable_info(ref, rbindings)
        kind, target = info.get("kind"), info.get("node")
        if kind == "helper" and target is not None:
            take(sweep_body(target, rbindings, ctx, depth,
                            info.get("class_node"), info.get("bound_kind")))
        elif kind == "class" and isinstance(target, ast.ClassDef):
            take(sweep_body(target, rbindings, ctx, depth))
        elif kind == "instance" and isinstance(target, ast.ClassDef):
            take(sweep_class(target, rbindings, ctx, depth, True))
        elif kind == "spawn" and isinstance(parent, ast.Call):
            penv = env if call_env is None else call_env.get(id(parent), {})
            hits.extend(callback_argv_leads(
                parent, penv, info.get("name", "") in SHELL_STRING_FUNCS))
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
    envs = {}  # literal environments persist across this file's Python cells
    binding_envs = {}  # visible Python bindings persist until reset in this file
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
                env = bindings = None
                if language in (None, "py", "python"):
                    if args.get("reset") is True:
                        envs["py"] = {}
                        binding_envs["py"] = {
                            key: {"kind": "reset_unbound"}
                            for key in binding_envs.get("py", {})}
                    env = envs.setdefault("py", {})
                    bindings = binding_envs.setdefault("py", {})
                hits, un_eval, un_spawn = classify_eval(code, language, env, bindings)
                entry["eval_unparsed"] += un_eval
                entry["unparsed_spawns"] += un_spawn
            else:
                continue
            entry["eval_unparsed"] += NESTED["eval_unparsed"]
            entry["unparsed_spawns"] += NESTED["unparsed_spawns"]
            unique_hits = {}
            observed = {tuple(result[:4]) for result in hits
                        if (result[4] if len(result) > 4 else "observed") == "observed"}
            for result in hits:
                cls, rule, argv0, text = result[:4]
                evidence = result[4] if len(result) > 4 else "observed"
                if evidence == "lead" and tuple(result[:4]) in observed:
                    continue  # the same command is already observed in this call
                key = (cls, rule, evidence, text)
                if key not in unique_hits:
                    unique_hits[key] = (cls, rule, argv0, text, evidence)
            for cls, rule, argv0, text, evidence in unique_hits.values():
                findings.append({
                    "file": path, "line": lineno,
                    "tool_call_id": str(item.get("id", "")),
                    "timestamp": obj.get("timestamp") if isinstance(obj.get("timestamp"), str) else str(obj.get("timestamp")),
                    "tool": name, "class": cls, "rule": rule,
                    "argv0": argv0, "command": redact(text),
                    "evidence": evidence,
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
                                    "observed_findings": 0, "lead_findings": 0,
                                    "permitted": sorted(permit), "unpermitted": 0})
        return 2
    code, label, unpermitted = verdict_of(findings, permit)
    observed = sum(1 for finding in findings
                   if finding.get("evidence", "observed") == "observed")
    leads = sum(1 for finding in findings if finding.get("evidence") == "lead")
    emit(label, {"schema": "mado-tripwire-verdict-v1", "exit": code, "files": entries,
                 "findings": findings, "counts": counts,
                 "observed_findings": observed, "lead_findings": leads,
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
        use_evidence = any("evidence" in w for w in want)
        def key(f, from_want):
            return (f["class"], f["rule"], f["line"],
                    (f.get("file", "") if from_want else os.path.basename(f["file"])) if use_file else "",
                    (f.get("evidence", "observed") if use_evidence else ""))
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
                                    "counts": {c: 0 for c in CLASSES},
                                    "observed_findings": 0, "lead_findings": 0,
                                    "permitted": [], "unpermitted": 0})
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
                                        "observed_findings": 0, "lead_findings": 0,
                                        "permitted": [], "unpermitted": 0})
            return 2
    if not rest:
        emit("could_not_evaluate", {"schema": "mado-tripwire-verdict-v1", "exit": 2,
                                    "error": "no path", "files": [], "findings": [],
                                    "counts": {c: 0 for c in CLASSES},
                                    "observed_findings": 0, "lead_findings": 0,
                                    "permitted": [], "unpermitted": 0})
        return 2
    return run_scan(rest, permit)


STACK_BYTES = 512 * 1024 * 1024
RECURSION_LIMIT = 50000


def run_with_stack(fn, *args):
    """Run fn on a thread with a deep stack and a raised recursion limit, so
    the recursive AST helpers and the parser reach far deeper (well-formed)
    expressions than the default 1000-frame limit before any RecursionError."""
    import threading
    result = {}

    def target():
        try:
            result["value"] = fn(*args)
        except BaseException as exc:  # re-raised on the calling thread
            result["error"] = exc

    import resource
    ceiling = resource.getrlimit(resource.RLIMIT_AS)[0]
    stack_bytes = STACK_BYTES
    if ceiling != resource.RLIM_INFINITY and ceiling <= STACK_BYTES:
        stack_bytes = min(64 * 1024 * 1024, max(8 * 1024 * 1024, ceiling // 4))
    threading.stack_size(stack_bytes)
    sys.setrecursionlimit(RECURSION_LIMIT)
    worker = threading.Thread(target=target)
    worker.start()
    worker.join()
    if "error" in result:
        raise result["error"]
    return result["value"]


if __name__ == "__main__":
    try:
        sys.exit(run_with_stack(main, sys.argv[1:]))
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
                          "observed_findings": 0, "lead_findings": 0,
                          "permitted": [], "unpermitted": 0}, ensure_ascii=True))
        sys.exit(2)
