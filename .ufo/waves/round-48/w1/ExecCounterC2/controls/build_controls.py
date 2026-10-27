#!/usr/bin/env python3
"""Build the POS + control tree for PRED-C2-r48 in the seat scratch dir."""
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/mado-r48/ExecCounterC2"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
BASE = "579f694b45c797a9c39761fdb4f9e0a1b71b3585"
REPO = os.path.join(S, "repo")
PINS = os.path.join(S, "pins")
GITID = ["-c", "user.name=ExecCounterC2", "-c", "user.email=exec@local",
         "-c", "commit.gpgsign=false"]


def run(*args, **kw):
    return subprocess.run(list(args), capture_output=True, text=True, **kw)


def git(*args):
    p = run("git", "-C", REPO, *args)
    if p.returncode != 0:
        raise SystemExit("git %s failed: %s" % (" ".join(args), p.stderr))
    return p.stdout


ENTRY = """# From the `kb_*` names to a compiled keymap: which XKB names this host accepts

source: S340 - libxkbcommon 1.13.2 rules compiler, RMLVO matching and the ignored-name warnings (pin `.ufo/waves/round-48/fetch/libxkbcommon-rules.c`)
source: S341 - libxkbcommon 1.13.2 context, the default include-path order and the system root (pin `.ufo/waves/round-48/fetch/libxkbcommon-context.c`)
source: S342 - xkeyboard-config 2.48 symbols/br, the Brazil layout's default section and its named variants (pin `.ufo/waves/round-48/fetch/xkeyboard-config-symbols-br`)
verified-at: 2026-10-26
recheck: on-release
ground: the RMLVO-to-keymap compile on this host, measured read-only with xkbcli 1.13.2 against xkeyboard-config 2.48; held neighbours: the stored names and the fallback in hyprland-input-devices-r46.md (rows S318-S319)
Lane: mado-shokunin. Round: 48. Recheck trigger: libxkbcommon or xkeyboard-config changes on the host; re-run `xkbcli compile-keymap` for the names and re-hash the keymap.

## What the evidence licenses

| question | where the answer lives | state |
|---|---|---|
| which names the config hands the compiler | step 1 | sourced (held rows S318-S319) |
| how a layout name becomes a symbols section | steps 2 and 4 | sourced |
| which include paths are searched, in which order | step 3 | sourced |
| which unknown names fail the compile and which are dropped | step 5 and the host matrix | sourced, executed |
| how a failed compile maps onto Hyprland's `us` fallback | step 6 | sourced (held) |

## The chain, step by step

1. The config names. Hyprland stores `kb_layout`, `kb_variant`, `kb_options` and `kb_rules` as strings (Hyprland-ConfigValues.cpp:271-279), so the compiler is handed RMLVO names, not files.
2. Rules first. The rules compiler matches every layout, variant and option name against the ruleset and logs the unmatched ones (libxkbcommon-rules.c:2048-2066).
3. Include paths. The compile searches `$XDG_CONFIG_HOME/xkb`, `$HOME/.config/xkb`, `$HOME/.xkb`, the extra path and then the system root (libxkbcommon-context.c:243-280), so a user symbols file can shadow the packaged one.
4. Symbols section. The layout name selects `symbols/<layout>` and the variant selects a `xkb_symbols "<variant>"` section inside it; `br`'s default is the abnt2 section (xkeyboard-config-symbols-br:3-4).
5. Failure or warning. A missing symbols file or section aborts the compile; an unmatched option is dropped with a logged warning (libxkbcommon-rules.c:2063).
6. Hyprland's fallback. When the compile fails, the keyboard falls back to `us` rather than keeping the rejected names (Hyprland-IKeyboard.cpp:101-116); the round-46 note holds the full step.

## Observations (upstream bytes, read-only)

- The warning is one of four sibling messages, each emitted only for an unmatched non-empty name: `Unrecognized RMLVO option`, libxkbcommon-rules.c:2063.
- An unmatched layout is logged with the same shape: `Unrecognized RMLVO layout`, libxkbcommon-rules.c:2053.
- The user include paths accept an empty `XDG_CONFIG_HOME` and report it: `Accept empty string, which may be unintentional and should be reported`, libxkbcommon-context.c:255.
- When `XDG_CONFIG_HOME` is unset the fallback is announced in the source: `XDG_CONFIG_HOME fallback is $HOME/.config/`, libxkbcommon-context.c:263.
- The Brazil layout's own header says what it is: `Keyboard layouts for Brazil.`, xkeyboard-config-symbols-br:1.
- The default section is named: `xkb_symbols "abnt2"`, xkeyboard-config-symbols-br:4.

## This host

The host config's names are layout `br` and options `compose:caps`. A read-only run of `xkbcli compile-keymap --layout br --options compose:caps` on xkbcli 1.13.2 (libxkbcommon 1.13.2-1) exits rc 0 and prints a 2090-line keymap whose sha256 is efd487a39920152354f0... (full digest and line count in `.ufo/waves/round-48/receipts/xkb-live.txt`).
The negative matrix, same receipt: unknown layout `--layout zz` rc 1 (XKB-338).
An unknown variant `--layout br --variant nope` rc 1 (XKB-661).
An unknown option `--layout br --options nope:nope` rc 0 with XKB-595 "Unrecognized RMLVO option ... was ignored".

## Symptom to cause

| symptom | cause | check |
|---|---|---|
| a keyboard prints `us` though the config names `br` | the compile failed and the fallback kept the old names | step 6; run `xkbcli compile-keymap --layout br` |
| a variant name is silently ignored | the variant does not exist in that layout | step 5 and the XKB-661 line in the receipt |

## Limits

- The compile is read-only: it says what libxkbcommon would build, not what the running compositor has loaded; a runtime `hyprctl switchxkblayout` is not observed here.
- No compositor mutation and no input injection were performed; the host's `hyprctl devices -j` keymap fields are the round-46 join's ground, not this entry's.
- The rules path is the packaged one; a user rules file under `$XDG_CONFIG_HOME/xkb` changes the result and is [UNK] for this host.
"""

RECEIPT = """# xkbcli compile-keymap live receipt (read-only, 2026-10-26)
xkbcli --version: 1.13.2
libxkbcommon 1.13.2-1

case: host names (kb_layout = br, kb_options = compose:caps)
args=--layout br --options compose:caps
rc=0
keymap_sha256=efd487a399201523540f4e5bbf81818be3183f6d9957c2f2b12469a2cf6fce81
keymap_lines=2090

case: unknown layout
args=--layout zz
rc=1
first_error=XKB-338 Couldn't find file "symbols/zz"

case: unknown variant
args=--layout br --variant nope
rc=1
first_error=XKB-661 Couldn't process include statement for 'br(nope)'

case: unknown option
args=--layout br --options nope:nope
rc=0
first_error=XKB-595 Unrecognized RMLVO option "nope:nope" was ignored
"""

RULES_SHA = "04dfd93468369de226b47c94475c1df93a41ce85bdd698c761312a38204e42a8"
CTX_SHA = "e6547abb657d27cdb42907d254d9bdd047435db8b5f59bb88fe69a315b84b8b7"
BR_SHA = "8cf65550e08b598407d5f7317f297e186561a94c866ab95d0c9a8737ef3bf35e"

ROWS = (
    "| S340 | libxkbcommon 1.13.2 rules compiler - RMLVO matching and the ignored-name "
    "warnings - https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/"
    "src/xkbcomp/rules.c | code | A | How layout, variant, model and option names are "
    "matched, and what happens to an unmatched one | libxkbcommon-rules.c:2048-2066 "
    "unmatched model/layout/variant/option warnings, libxkbcommon-rules.c:2087-2097 "
    "explicit layout count @ tag xkbcommon-1.13.2, 74868 B sha256:%s; receipt "
    ".ufo/waves/round-48/fetch/libxkbcommon-rules.c | An unmatched non-empty name is "
    "logged and then ignored; the option message is XKB-595 | mined | 2026-10-26 | "
    "on-release | corpus/knowledge/xkb-keymap-compile-r48.md |" % RULES_SHA,
    "| S341 | libxkbcommon 1.13.2 context - the default include-path order - "
    "https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/"
    "context.c | code | A | The order in which the default include paths are appended, "
    "and the system root | libxkbcommon-context.c:243-280 default include paths, "
    "libxkbcommon-context.c:317-318 system root @ tag xkbcommon-1.13.2, 22059 B "
    "sha256:%s; receipt .ufo/waves/round-48/fetch/libxkbcommon-context.c | User paths "
    "come before the extra path and the system root, so a user file shadows the packaged "
    "one | mined | 2026-10-26 | on-release | "
    "corpus/knowledge/xkb-keymap-compile-r48.md |" % CTX_SHA,
    "| S342 | xkeyboard-config 2.48 symbols/br - the Brazil layout's sections - "
    "https://gitlab.freedesktop.org/xkeyboard-config/xkeyboard-config/-/raw/"
    "xkeyboard-config-2.48/symbols/br | code | A | The default section of the br layout "
    "and the named variants beside it | xkeyboard-config-symbols-br:1-4 default section, "
    "xkeyboard-config-symbols-br:47-50 a named variant @ tag xkeyboard-config-2.48, "
    "19592 B sha256:%s; receipt .ufo/waves/round-48/fetch/xkeyboard-config-symbols-br | "
    "The default section is the abnt2 one; a variant name selects a named section in the "
    "same file | mined | 2026-10-26 | on-release | "
    "corpus/knowledge/xkb-keymap-compile-r48.md |" % BR_SHA,
)

README_ROW = (
    "| `knowledge/xkb-keymap-compile-r48.md` (R48-1) | Which `kb_layout`/`kb_model`/"
    "`kb_variant`/`kb_options` names compile on this host: RMLVO rules to components, the "
    "include-path order, the names that abort the compile versus the ones dropped with a "
    "warning, and how a failure maps onto Hyprland's `us` fallback; read-only "
    "`xkbcli compile-keymap` receipt with three negative probes. | "
    "[Source and recheck](knowledge/xkb-keymap-compile-r48.md): rows S340-S342, the host "
    "matrix and the receipt; re-run `xkbcli compile-keymap` for the host names. |\n"
)


def write(rel, data, mode="w"):
    path = os.path.join(REPO, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, mode) as fh:
        fh.write(data)
    return path


def insert_before_heading(rel, heading, block):
    path = os.path.join(REPO, rel)
    with open(path) as fh:
        lines = fh.readlines()
    out, done = [], False
    for line in lines:
        if not done and line.startswith(heading):
            out.append(block)
            done = True
        out.append(line)
    if not done:
        raise SystemExit("heading %s not found in %s" % (heading, rel))
    with open(path, "w") as fh:
        fh.writelines(out)


def commit(msg):
    git("add", "-A")
    git(*GITID, "commit", "-q", "-m", msg)
    return git("rev-parse", "HEAD").strip()


def pos_tree():
    write("corpus/knowledge/xkb-keymap-compile-r48.md", ENTRY)
    insert_before_heading("corpus/SOURCES.md", "## Paths", "\n".join(ROWS) + "\n\n")
    insert_before_heading("corpus/README.md", "## Frontier", README_ROW + "\n")
    write(".ufo/waves/round-48/receipts/xkb-live.txt", RECEIPT)
    for name in ("libxkbcommon-rules.c", "libxkbcommon-context.c",
                 "xkeyboard-config-symbols-br"):
        shutil.copyfile(os.path.join(PINS, name),
                        write_placeholder(".ufo/waves/round-48/fetch/" + name))


def write_placeholder(rel):
    path = os.path.join(REPO, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def mutate(rev, name, fn, msg):
    git("checkout", "-q", "-B", "ctl-" + name, rev)
    fn()
    return commit(msg)


def main():
    if os.path.isdir(REPO):
        shutil.rmtree(REPO)
    p = run("git", "clone", "-q", "--shared", LANE, REPO)
    if p.returncode != 0:
        raise SystemExit("clone failed: %s" % p.stderr)
    top = git("rev-parse", "--show-toplevel").strip()
    if os.path.realpath(top) != os.path.realpath(REPO):
        raise SystemExit("clone toplevel mismatch: %s" % top)
    git("checkout", "-q", "--detach", BASE)
    pos_tree()
    pos = commit("POS: minimal entry-only tree for PRED-C2-r48")
    print("POS", pos)

    def edit(rel, old, new, count=1):
        def fn():
            path = os.path.join(REPO, rel)
            with open(path) as fh:
                text = fh.read()
            if text.count(old) < 1:
                raise SystemExit("mutation target absent in %s: %r" % (rel, old[:60]))
            with open(path, "w") as fh:
                fh.write(text.replace(old, new, count))
        return fn

    E = "corpus/knowledge/xkb-keymap-compile-r48.md"
    R = ".ufo/waves/round-48/receipts/xkb-live.txt"
    controls = {
        "QUOTE": (edit(E, "Keyboard layouts for Brazil.", "Keyboard layouts for Brasil."),
                  "control QUOTE: quote not verbatim in its pin"),
        "RANGE": (edit(E, "libxkbcommon-context.c:255", "libxkbcommon-context.c:9999"),
                  "control RANGE: quote locator beyond its pin"),
        "BRANCH": (edit("corpus/SOURCES.md",
                        "libxkbcommon/xkbcommon-1.13.2/src/xkbcomp",
                        "libxkbcommon/main/src/xkbcomp"),
                   "control BRANCH: row URL on a branch ref"),
        "PIN": (edit("corpus/SOURCES.md", RULES_SHA, "a" * 64),
                "control PIN: row digest does not match the fetch copy"),
        "HELD": (edit("corpus/SOURCES.md",
                      "corpus/knowledge/hyprland-input-devices-r46.md |\n| S319",
                      "corpus/knowledge/hyprland-input-devices-r46.md changed |\n| S319"),
                 "control HELD: held row S318 moved"),
        "RECEIPT-absent": (lambda: os.remove(os.path.join(REPO, R)),
                           "control RECEIPT-absent: cited receipt deleted"),
        "RECEIPT-contradicts": (edit(R, "args=--layout zz\nrc=1",
                                     "args=--layout zz\nrc=0"),
                                "control RECEIPT-contradicts: receipt rc contradicts the entry"),
        "NOSTEPS": (edit(E, "5. Failure or warning.", "Failure or warning."),
                    "control NOSTEPS: one step unnumbered"),
    }
    for name, (fn, msg) in controls.items():
        rev = mutate(pos, name, fn, msg)
        print(name, rev)
    with open(os.path.join(S, "revs.txt"), "w") as fh:
        fh.write("BASE %s\nPOS %s\n" % (BASE, pos))
        for name in controls:
            fh.write("%s %s\n" % (name, git("rev-parse", "ctl-" + name).strip()))


if __name__ == "__main__":
    main()
