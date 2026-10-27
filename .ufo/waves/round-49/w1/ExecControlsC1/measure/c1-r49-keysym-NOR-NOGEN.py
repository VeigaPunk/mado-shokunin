#!/usr/bin/env python3
"""PRED-C1-r49 - tools/mado-keysym.py predicts what `xkbcli how-to-type --disable-compose --keysym` prints.

Draft for the round-49 freeze (wave w1). The judge is the pinned libxkbcommon 1.13.2 tool; no reference
implementation of ours judges anything. The tool is `tools/mado-keysym.py` at the scored revision REV:

    mado-keysym.py how-to-type --keymap FILE --disable-compose --keysym ARG

must print exactly what the pinned how-to-type prints on STDOUT for the same serialized keymap and ARG, and
exit with its exit status. FILE is a keymap SERIALIZED by the pinned `xkbcli compile-keymap` from
xkeyboard-config RMLVO names (default format), never a raw XKB source. Without `--disable-compose`, or without
`--keysym`, the tool refuses (exit 2): compose sequences and the character/code-point interpretation are out
of contract.

Scores one committed revision REV of --repo (revision-addressed git reads with ambient GIT_* removed; nothing
in the repository is written; scratch only under --work, which must lie outside the repository, this counter's
lane and that lane's parent directory, and outside /tmp and /var/tmp). TARGET_MET iff every clause holds:
  t  TOOL is a regular blob (mode 100644 or 100755) at REV. The file is read with `git show REV:TOOL`; the
     working tree is never consulted.
  s  tool self-checks at REV, in the sandbox:
       - `python3 -I TOOL --selftest` exits 0 within 120 s, its last non-empty stdout line is exactly
         `MADO_KEYSYM_SELFTEST: N/N passed` (ASCII digits) with N >= 25 and N == N;
       - the two documented refusals exit 2 without printing a table: `how-to-type --keymap FILE --keysym
         slash` (no --disable-compose) and `how-to-type --keymap FILE --disable-compose` (no --keysym).
  f  every fixture (the pinned `c1-r49-fixtures.json` when installed beside the counter, else the embedded
     fallback list) is judged at count time:
     the counter compiles the fixture's keymap with the pinned compile-keymap in a clean env (env -i-like:
     PATH=/usr/bin, HOME and XDG_CONFIG_HOME in --work, LC_ALL=C - no user xkb include path exists), runs the
     pinned how-to-type, and requires the tool's exit status and STDOUT BYTES to equal the judge's. A fixture
     whose judge result no longer matches its record is a SETUP error (the judge or the fixture drifted), not
     a tool failure. stderr is never compared.
  g  GEN = 0   # WEAKENED g and r cases drawn from NONCE by gen_case(): RMLVO from a frozen, pre-validated pool (xkeyboard-config
     layouts/variants and option strings compiled successfully when this counter was written), ARG from a
     pool of keysym names, numeric forms, absent-but-valid names and invalid names. Each case is judged at
     count time exactly like a fixture; NONCE is --nonce (default: drawn from os.urandom and printed), so the
     cases cannot be precomputed. A generated RMLVO that no longer compiles is a SETUP error.
  r  read-only, no process: every tool run (selftest, refusals, fixtures, generated) is executed under
     `strace -f -qq -e trace=<TRACE_SET> -o <file outside the sandbox> bwrap ...`; after the line recording
     the execve of the sandboxed python3, ANY further traced event of these kinds is a trip:
       - a process started or a socket made/connected: execve, execveat, socket, socketpair, connect, fork,
         vfork, clone, clone3 (by the tool or anything it forks);
       - a write ATTEMPT, successful or not: open/openat/openat2 whose flags carry O_WRONLY, O_RDWR,
         O_CREAT, O_TRUNC or O_APPEND (quoted path strings are blanked before the flags are read), or any
         creat, mkdir(at), rmdir, unlink(at), rename(at/at2), link(at), symlink(at), truncate, ftruncate,
         mknod(at) call. The mounts are read-only, so the trace, not the tree, sees the attempt.
     The one exception is the clause-s `--selftest`: it is documented as writing its cases under $TMPDIR
     (a fresh tmpfs), so write attempts whose every absolute quoted path lies under /tmp are excused for that
     run only; a write elsewhere (or one whose target cannot be read off the trace line) is still a trip, and
     process/socket trips still count. readonly=ok iff trips=0 over all runs.
  i  isolation (mount allowlist, stated as the mount set - path absence is bwrap's business, not a clause):
     every tool run is `bwrap --unshare-all --die-with-parent --new-session --clearenv` with a fresh root
     whose mounts are exactly:
       `/` (bwrap tmpfs), `/usr` (tmpfs), `/usr/lib` (tmpfs) carrying ONLY python's runtime: the stdlib
       directory (`dir(os.__file__)`, read-only), an empty tmpfs over its `site-packages` (system
       third-party packages are not visible), the shared libraries named by `ldd` over the interpreter AND
       over every stdlib extension module in `lib-dynload` (so any stdlib import works; each library is
       bound at the SONAME path ldd printed and at its realpath), `/usr/bin/python3` (the interpreter,
       read-only), `/lib` and `/lib64` as symlinks to `usr/lib`; a setup error if that closure ever names
       libxkbcommon or an xkbcli binary;
       `/usr/include/xkbcommon/xkbcommon-keysyms.h` (read-only, pinned by HEADER_SHA256) - the only keysym
       data source a runtime table may come from; a tool that embeds the table simply does not read it;
       `/fixture/keymap.xkb` (read-only, the one compiled keymap of the case; absent for --selftest);
       `/oracle/tool.py` (read-only, the tool blob read from REV); `/dev` (bwrap tmpfs with device nodes);
       `/proc` (fresh pid namespace); `/tmp` (fresh tmpfs, the selftest's scratch).
     NO network: --unshare-all makes a net namespace with no host interface. NO host /usr/lib beyond the
     named runtime, so libxkbcommon and the xkbcli binaries are NOT present inside the sandbox; a tool cannot
     emulate the judge by loading the judge's library (ctypes included) or running its binary. The env inside
     is exactly PATH=/usr/bin, LC_ALL=C, HOME=/nonexistent, TMPDIR=/tmp.
Final line: `PRED-C1-r49: fixtures=K/F generated=G/N selftest=<ok|fail> readonly=<ok|fail>
tool=<present|absent> verdict=TARGET_MET|TARGET_MISSED`; exit 0 iff TARGET_MET, 1 if missed, 2 on setup
failure. Clause lines `PRED-C1-r49 clause=<x> ...` precede it (rev= and nonce= ride on clause=meta).
Read-only git is used; no process or network is started on the host by the counter itself except git, the
sandbox launcher, strace and the pinned judge, all on the count side.

Residuals (declared):
 - the tool's refusal path is scored only by exit status and the absence of a `=== Direct access ===` line;
   the wording of its usage/error message is out of contract (how-to-type's own usage names argv[0], so its
   stderr is not comparable anyway).
 - `--keysym` arguments that begin with `-` are not generated (the tool's own CLI parser and the judge's
   getopt would disagree for reasons unrelated to the keymap), and `--disable-compose`/`--keysym` repeated
   or reordered is not scored.
 - the tool must read a serialized keymap: raw XKB sources with includes, a keymap on stdin (`--keymap -`),
   and `--format 1` are out of contract.
 - the sandbox exposes the host python3 build (its stdlib tree) read-only; a tool that stores a precomputed
   answer table inside its own source is the "cached table" control, not a residual (fixtures and nonce
   cases are not in the repo... except the embedded fixtures, which ARE in this source: a tool may special-
   case them; clause g is what that tool fails, and the frozen fixture file substitution below closes it).
 - /proc/1/cmdline inside the sandbox shows the bwrap argv, hence the host --work path as a string; and
   /proc exposes the fresh pid namespace's own processes only.
 - the sandbox's /usr/lib carries the interpreter's and every stdlib extension module's `ldd` closure plus the
   stdlib tree, with site-packages shadowed by an empty tmpfs. Any Python 3 stdlib import therefore works
   (base64/binascii -> libz, _ssl -> libssl/libcrypto, ctypes -> libffi, sqlite3, lzma, ...), while libxkbcommon
   and the xkbcli binaries are still absent: `Box.python_libs()` refuses a closure that names them. Third-party
   site-packages code is not importable, and no stdlib module reaches the judge.
 - fixture source: the w1 fixture file `.ufo/waves/round-49/w1/ExecFixtures/fixtures-counter.json` (633 cases,
   sha256 81836bfba624a0a4344c4787f7058219b45554fbcfc2da9d797846d96610e393) is installed beside this counter
   as `c1-r49-fixtures.json` and pinned by SHA256_FIXTURES; a missing or mismatching file is a setup error. The
   57 embedded cases are the fallback used only when SHA256_FIXTURES is emptied (e.g. the file is not
   installed); an installed file is then ignored.
"""
import argparse
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True

PRED = "PRED-C1-r49"
HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = "tools/mado-keysym.py"
JUDGE = "/usr/lib/xkbcommon/xkbcli-how-to-type"
JUDGE_SHA256 = "f6c0b122ad90c9e30086653517c51f4b2203b6c7c07bcbc89c71e55ab2927e54"
COMPILE = "/usr/lib/xkbcommon/xkbcli-compile-keymap"
COMPILE_SHA256 = "43b924f68651500e022c74371515154f8c50a2e087defa6b834cc5d41fd77250"
HEADER = "/usr/include/xkbcommon/xkbcommon-keysyms.h"
HEADER_SHA256 = "13023369f65a17411606084e3e09557b4886aeb15f89affba4aaa86490a463f3"
SELFTEST_MIN = 25
GEN = 0   # WEAKENED g and r
NAME_FIXTURES = "c1-r49-fixtures.json"
SHA256_FIXTURES = "81836bfba624a0a4344c4787f7058219b45554fbcfc2da9d797846d96610e393"
ENV_GIT = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
PROC_SET = ("execve", "execveat", "socket", "socketpair", "connect", "fork", "vfork", "clone", "clone3")
OPEN_SET = ("open", "openat", "openat2")
WRITE_SET = ("creat", "mkdir", "mkdirat", "rmdir", "unlink", "unlinkat", "rename", "renameat", "renameat2", "link",
             "linkat", "symlink", "symlinkat", "truncate", "ftruncate", "mknod", "mknodat")
TRACE_SET = "trace=" + ",".join(PROC_SET + OPEN_SET + WRITE_SET)
WRITE_FLAGS = re.compile(r"\bO_(WRONLY|RDWR|CREAT|TRUNC|APPEND)\b")
QUOTED = re.compile(r'"(?:[^"\\]|\\.)*"')
SELFTEST_LINE = re.compile(r"^MADO_KEYSYM_SELFTEST: (\d+)/(\d+) passed$")


def tmp_write(rest):
    """True iff a write-attempt trace line names only absolute paths under /tmp (the selftest's scratch)."""
    paths = [p[1:-1] for p in QUOTED.findall(rest)]
    absolute = [p for p in paths if p.startswith("/")]
    return bool(absolute) and all(p == "/tmp" or p.startswith("/tmp/") for p in absolute)


RMLVO_KEYS = ("rules", "model", "layout", "variant", "options")
DEFAULTS = {"rules": "evdev", "model": "pc105"}

# ------------------------------------------------------------------------------------------------ fixtures
# (id, class, RMLVO, ARG, recorded exit status, sha256 of the judge's stdout). Recorded on this host on
# 2026-10-27 with the pinned judge; clause f re-derives both at count time and a mismatch is a SETUP error.
EMBEDDED_FIXTURES = [
    ("HOST-slash", "HOST", {"layout": "br", "options": "compose:caps"}, "slash", 0,
     "3d895204319dae0c18a405e8a2b232b67279f91c35b05c8440f64415c5bb0be2"),
    ("HOST-return", "HOST", {"layout": "br", "options": "compose:caps"}, "Return", 0,
     "9697ab0c8eef8f4d042041b2ac8c78056826f95092a98c24ec9455909f4f99c3"),
    ("HOST-dead-acute", "HOST", {"layout": "br", "options": "compose:caps"}, "dead_acute", 0,
     "db6868871018674aeb912d08cd9d495faddf6f9053dc42975124d3c3eceab208"),
    ("HOST-l3", "HOST", {"layout": "br", "options": "compose:caps"}, "ISO_Level3_Shift", 0,
     "b181628de2f829690d7b28f27da8b3d087831ae3800d500d4b1bb57912d2b8f6"),
    ("HOST-num-hex", "NUMERIC", {"layout": "br", "options": "compose:caps"}, "0x2f", 0,
     "3d895204319dae0c18a405e8a2b232b67279f91c35b05c8440f64415c5bb0be2"),
    ("HOST-num-dec", "NUMERIC", {"layout": "br", "options": "compose:caps"}, "47", 0,
     "3d895204319dae0c18a405e8a2b232b67279f91c35b05c8440f64415c5bb0be2"),
    ("HOST-xf86-mute", "XF86", {"layout": "br", "options": "compose:caps"}, "XF86AudioMute", 0,
     "a815c2dbd97e5c728b7a6dddba197905057962b1b9d850a8f9f1f76e7ff3c894"),
    ("HOST-kp1", "KEYPAD", {"layout": "br", "options": "compose:caps"}, "KP_1", 0,
     "c2d5172101950fe674ed1adff6a9252df7873fc0f2aa7f736bb0faf0fcc5414d"),
    ("HOST-escape", "FUNCTION", {"layout": "br", "options": "compose:caps"}, "Escape", 0,
     "d0cf7e53defeb5806c34e42d4eb53319ba92b5300fb44200a546d25998361875"),
    ("HOST-question", "PUNCT", {"layout": "br", "options": "compose:caps"}, "question", 0,
     "e82795f868d4d66df8ab0bcb22253fd9d15d92d18a5fb2b75fab1df8c4566457"),
    ("HOST-nosym", "INVALID", {"layout": "br", "options": "compose:caps"}, "nosuchsym", 2,
     "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    ("HOST-NoSymbol", "INVALID", {"layout": "br", "options": "compose:caps"}, "NoSymbol", 2,
     "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    ("HOST-zero", "INVALID", {"layout": "br", "options": "compose:caps"}, "0x0", 2,
     "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    ("HOST-uplus", "INVALID", {"layout": "br", "options": "compose:caps"}, "U+002F", 2,
     "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    ("HOST-Unicode", "NUMERIC", {"layout": "br", "options": "compose:caps"}, "0x1000e9", 0,
     "3bf291997c00d080a87306c5e14bd47ee7de1ddbe17fc4f7a3f541dd2eeaabd0"),
    ("MULTI-slash", "MULTI", {"layout": "br,us", "options": "grp:alt_shift_toggle"}, "slash", 0,
     "e957f7bf97379fb34580ec36abb613c5e44522f33681bb7fd02d658e9cbd890e"),
    ("MULTI-a", "LETTERS", {"layout": "br,us", "options": "grp:alt_shift_toggle"}, "a", 0,
     "be1a58edc4ef2ef269b1c01bc9d2f800d4e53539ac0b9210a6475a57a09a5d55"),
    ("MULTI-cyrillic", "ABSENT", {"layout": "br,us", "options": "grp:alt_shift_toggle"}, "Cyrillic_a", 0,
     "c7d5c0aa36c6c941ca2ee5698ec970fd74b3123e0ca9ef77f4e5d2972032a9ed"),
    ("MULTI-F1", "FUNCTION", {"layout": "br,us", "options": "grp:alt_shift_toggle"}, "F1", 0,
     "1b6ed7f8a59181a33d9b0df0bd7e63d57d6fe445d8c3f88ca0779fea94d0de40"),
    ("MULTI-z-3l", "MULTI", {"layout": "us,ru,de", "variant": ",,"}, "z", 0,
     "22ba5a862b3354e040460484d443dfc5c4ac0fc22d95fd03891ca42bce1044ad"),
    ("MULTI-cyr-3l", "MULTI", {"layout": "us,ru,de", "variant": ",,"}, "Cyrillic_a", 0,
     "d5e0b551d7d6b8dbbeca60b5276b0691e0951276b3797c0bdfd5353bbc53edaf"),
    ("MULTI-de-ue", "MULTI", {"layout": "us,ru,de", "variant": ",,"}, "udiaeresis", 0,
     "78dcd5a8dbfe66ca1e742cd0dd38536141e83dfb02321a8da44d41b8b74d8fe2"),
    ("VAR-nodead-apos", "VARIANT", {"layout": "br", "variant": "nodeadkeys"}, "apostrophe", 0,
     "8926f66885f6fd5f31535dfce81126dfab764c5463cb60dda54f837aa709970e"),
    ("VAR-nodead-dead", "ABSENT", {"layout": "br", "variant": "nodeadkeys"}, "dead_acute", 0,
     "8147dd4b3593111799fcdf1c9aedb13a26f98b64d8ba944445dcfb38c2adf5ed"),
    ("VAR-dvorak-slash", "VARIANT", {"layout": "us", "variant": "dvorak"}, "slash", 0,
     "0ee72b36f3587459cdc3a418663e8c38c734c3c4ef3fd7247ef1e1e6d2624215"),
    ("VAR-dvorak-a", "VARIANT", {"layout": "us", "variant": "dvorak"}, "a", 0,
     "7b89dcd9d9e9a67194df8de40027aecc23d1c3b921ee1eff40cd05cf3d8c8644"),
    ("VAR-intl-dead", "DEAD", {"layout": "us", "variant": "intl"}, "dead_acute", 0,
     "bf35a2b15b6ef6f07291edb929da83b04f2ba75f5f3d9f5084616aa77642ffb3"),
    ("OPT-lv3", "MODIFIER", {"layout": "us", "options": "lv3:ralt_switch"}, "ISO_Level3_Shift", 0,
     "86e930e1507f661415db9e6b5f634570e1edf58655c9215dc41973c3dfe1e62a"),
    ("OPT-lv3-euro", "OPTIONS", {"layout": "us", "options": "lv3:ralt_switch"}, "EuroSign", 0,
     "2d7f2b7e8dfd045ec5e01c6d04e09bf24fc25253c7c77f3896d816bedaca12b3"),
    ("OPT-caps-esc", "MODIFIER", {"layout": "us", "options": "caps:escape"}, "Escape", 0,
     "886ab3540f22158f183f4dfa83433d106863e8db3c74211799ac2dab3bac1590"),
    ("OPT-caps-lock", "MODIFIER", {"layout": "us", "options": "caps:escape"}, "Caps_Lock", 0,
     "646e725293d7af3a909957949472e94dae215752e196bd2e63ce1452a5d312fd"),
    ("OPT-altwin", "MODIFIER", {"layout": "de", "options": "altwin:swap_lalt_lwin"}, "Alt_L", 0,
     "fd965e418655e16966456a212f8d2bd5d7a7c8eed8d45e108fbba0dc842f7d49"),
    ("OPT-altwin-super", "MODIFIER", {"layout": "de", "options": "altwin:swap_lalt_lwin"}, "Super_L", 0,
     "fbfc2f72ea9f3cf24214cec3985b07c073ae32436317fe6d965f77d3e23053cc"),
    ("SYM-a", "LETTERS", {"layout": "us"}, "a", 0,
     "0ab59d6d766107905db7a91b72587a181490a6a261be9bda1c42aabe527bbab6"),
    ("SYM-A", "LETTERS", {"layout": "us"}, "A", 0,
     "994a4c24f75ec31e0afc7ce481fcaa7c120d676236381f70a69e1329f71303bb"),
    ("SYM-1", "DIGITS", {"layout": "us"}, "1", 0,
     "5a5c4f4a493c5ce982ec163af001c034e0dc5821a9dc848d9b6fe90b92c7029c"),
    ("SYM-exclam", "DIGITS", {"layout": "us"}, "exclam", 0,
     "c65b366e39a60691a98fd30b2a50b5f17507f140fce8cd4268b669f1476de049"),
    ("SYM-slash", "PUNCT", {"layout": "us"}, "slash", 0,
     "f3274966f747b020846336b1fc6a00906f927af9f430529a39fd771a826b8c9f"),
    ("SYM-question", "PUNCT", {"layout": "us"}, "question", 0,
     "493983463d8a570100580b972a4c7e163c5910be988d3000391ea48929684655"),
    ("SYM-backslash", "PUNCT", {"layout": "us"}, "backslash", 0,
     "40c58be466daad9fef6b774393168e20a43bcb80055e786b407840e38b0c7443"),
    ("SYM-bar", "PUNCT", {"layout": "us"}, "bar", 0,
     "a2bb195741337d327590d9bd00469ff6dfa0ab130125fdc7140581858e8570eb"),
    ("SYM-at", "PUNCT", {"layout": "us"}, "at", 0,
     "e9c2c3e169631a07eff78c074dbe66251db277edc0539f074051cab003276a76"),
    ("SYM-shift", "MODIFIER", {"layout": "us"}, "Shift_L", 0,
     "e4d29493db8678690978cab8b081842d2dd7506dac0429fce73b37abd892f0a0"),
    ("SYM-super", "MODIFIER", {"layout": "us"}, "Super_L", 0,
     "b6d5385387768b94785ecd45e7df049aac28197cb4f0d1656aec59ae8c3e975e"),
    ("SYM-kpadd", "KEYPAD", {"layout": "us"}, "KP_Add", 0,
     "ca8754c7e18462e9772c07a86afa08e811c7237ac57139318dbbc74025501683"),
    ("SYM-tab", "FUNCTION", {"layout": "us"}, "Tab", 0,
     "dbc66352703c3bf562f6a0b8d2d85cddc38816098bc99210c13e6278d9ed480c"),
    ("SYM-bksp", "FUNCTION", {"layout": "us"}, "BackSpace", 0,
     "a7e5ed349dcfb8e8f2427f9a78b1e4b5c5c858ca729858e726052ed5bb2f9b38"),
    ("SYM-F35-absent", "ABSENT", {"layout": "us"}, "F35", 0,
     "d3fd9c9c987d2ca3d035c1e792775e4a565b76a7d04d3b5339591d273d757ed4"),
    ("SYM-bright", "XF86", {"layout": "us"}, "XF86MonBrightnessDown", 0,
     "6c6189e8d76ad2b5cc379b627a147c8c729c8ec837c0538ff7c3c47c9b3017b9"),
    ("SYM-xf86sleep", "XF86", {"layout": "us"}, "XF86Sleep", 0,
     "d1dde15b6ef98de5d3c31eb10b6964b6ee6af3d106844313fb150fa295c17c93"),
    ("SYM-period", "PUNCT", {"layout": "us"}, "period", 0,
     "6d28df547e5ffb70ba1520601f78270fec20660fec8a918daac03a93c14a71c4"),
    ("SYM-0-dec", "NUMERIC", {"layout": "us"}, "0x7f", 0,
     "8578bd6f22f4bf4e601fd0a41964bee9275c3b2714fe46915d0409e41746332f"),
    ("SYM-return-num", "NUMERIC", {"layout": "us"}, "0xff0d", 0,
     "f4cff64f15be634a2190bc6642ca679ce68939765e6dadb90ebe97c89463fc3a"),
    ("CASE-lower", "CASE", {"layout": "us"}, "return", 2,
     "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    ("CASE-SLASH", "CASE", {"layout": "us"}, "SLASH", 2,
     "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    ("CASE-Q", "BIND", {"layout": "us"}, "Q", 0,
     "dd30c3558233c689a9e4dd48e2dafd78a3eee40ca17fa5a10332c97172ad7d5e"),
    ("CASE-W", "BIND", {"layout": "us"}, "W", 0,
     "836dd091b2b1ae34b4fb2cfcf948cf5c1491da72a996db79775e3a39ec8a5433"),
]

# Frozen pool: every pair/option below compiled with the pinned compile-keymap when this counter was written.
LAYOUT_PAIRS = [
    ("us", None), ("us", "dvorak"), ("us", "intl"), ("us", "colemak"), ("us", "workman"), ("us", "altgr-intl"),
    ("br", None), ("br", "nodeadkeys"), ("br", "abnt2"), ("de", None), ("de", "nodeadkeys"), ("fr", None),
    ("fr", "oss"), ("ru", None), ("ru", "phonetic"), ("ru", "typewriter"), ("es", None), ("gb", None),
    ("it", None), ("pt", None), ("pl", None), ("se", None), ("dk", None), ("no", None), ("fi", None),
    ("ca", None), ("ch", "fr"), ("ch", "de"), ("gr", None), ("tr", None), ("jp", None), ("kr", None),
    ("il", None), ("hu", None), ("cz", None), ("latam", None), ("nl", None), ("be", None), ("at", None),
    ("ie", None), ("is", None), ("lt", None), ("lv", None), ("ee", None), ("si", None), ("sk", None),
    ("ro", None), ("bg", None), ("hr", None), ("rs", None), ("ua", None), ("vn", None), ("in", None),
    ("th", None), ("br,us", None), ("us,ru,de", ",,"), ("de,fr", None), ("us,us", ",dvorak"),
    ("gb", "intl"), ("fr", "bepo"), ("de", "neo"),
]
OPTIONS = [None, "lv3:ralt_switch", "caps:escape", "grp:alt_shift_toggle", "compose:caps",
           "altwin:swap_lalt_lwin", "lv3:ralt_switch,compose:caps", "ctrl:nocaps", "grp:win_space_toggle",
           "terminate:ctrl_alt_bksp", "lv3:switch", "compose:ralt", "grp:shifts_toggle",
           "caps:ctrl_modifier", "ctrl:swapcaps"]
NAMES = ["a", "A", "b", "z", "slash", "backslash", "bar", "question", "at", "period", "comma", "minus",
         "equal", "Return", "Tab", "BackSpace", "Escape", "Delete", "Home", "End", "Up", "Down", "Left",
         "Right", "F1", "F2", "F12", "F35", "KP_0", "KP_1", "KP_Add", "KP_Decimal", "KP_Enter",
         "KP_Separator", "dead_acute", "dead_grave", "dead_tilde", "dead_diaeresis", "Shift_L", "Shift_R",
         "Control_L", "Control_R", "Alt_L", "Alt_R", "Super_L", "Super_R", "Caps_Lock", "Num_Lock",
         "ISO_Left_Tab", "ISO_Level3_Shift", "Mode_switch", "XF86AudioMute", "XF86AudioRaiseVolume",
         "XF86AudioLowerVolume", "XF86MonBrightnessUp", "XF86MonBrightnessDown", "XF86Sleep", "XF86Display",
         "XF86WLAN", "EuroSign", "sterling", "yen", "cent", "section", "degree", "mu", "plusminus",
         "multiply", "divide", "onehalf", "ae", "AE", "oslash", "Oslash", "udiaeresis", "Adiaeresis",
         "ssharp", "eacute", "egrave", "ccedilla", "ntilde", "Cyrillic_a", "Cyrillic_A", "Cyrillic_ya",
         "Greek_alpha", "Greek_Omega", "Arabic_alef", "Hebrew_alef", "Thai_a", "Hangul_A", "Hiragana_A", "0"]
ABSENT = ["Cyrillic_a", "Greek_alpha", "Hebrew_alef", "Arabic_alef", "Thai_a", "Hangul_A", "F35",
          "XF86Sleep", "KP_Delete", "Georgian_a"]
INVALID = ["nosuchsym", "return", "SLASH", "U+002F", "0x0", "Nope", "slash_", ""]


class Setup(Exception):
    pass


def git(repo, *args):
    p = subprocess.run(["git", "-C", repo, *args], capture_output=True, env=ENV_GIT)
    return p.stdout if p.returncode == 0 else None


def lane_root():
    """The lane directory: the nearest ancestor holding SKILL.md, tools/ and quality/."""
    p = os.path.realpath(HERE)
    while p != "/":
        if all(os.path.exists(os.path.join(p, x)) for x in ("SKILL.md", "tools", "quality")):
            return p
        p = os.path.dirname(p)
    raise Setup("lane root (SKILL.md/tools/quality) not found above %s" % HERE)


def beside(name):
    """A counter-side data file: beside this counter when installed, else where the lane keeps counters."""
    p = os.path.join(HERE, name)
    if os.path.isfile(p):
        return p
    return os.path.join(lane_root(), "quality", "counters", name)


def under(p, root):
    p, root = os.path.realpath(p), os.path.realpath(root)
    return p == root or p.startswith(root.rstrip("/") + "/")


def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def pinned_file(path, sha, what):
    try:
        got = file_sha256(path)
    except OSError:
        raise Setup("missing %s (%s)" % (what, path))
    if got != sha:
        raise Setup("%s sha256 %s, pinned %s" % (what, got, sha))
    return path


# ------------------------------------------------------------------------------------------------ fixtures
def check_fixture(case, name):
    if not isinstance(case, dict):
        raise Setup("%s: fixture is not an object" % name)
    if set(case) != {"id", "class", "rmlvo", "arg", "rc", "sha256"}:
        raise Setup("%s: fixture keys %r" % (name, sorted(case)))
    if not isinstance(case["rmlvo"], dict) or set(case["rmlvo"]) - set(RMLVO_KEYS):
        raise Setup("%s: fixture %s: bad rmlvo" % (name, case["id"]))
    if not isinstance(case["arg"], str) or not isinstance(case["rc"], int):
        raise Setup("%s: fixture %s: bad arg/rc" % (name, case["id"]))
    if not re.fullmatch(r"[0-9a-f]{64}", str(case["sha256"])):
        raise Setup("%s: fixture %s: bad sha256" % (name, case["id"]))
    return case


def embedded_fixtures():
    return [check_fixture({"id": i, "class": c, "rmlvo": r, "arg": a, "rc": rc, "sha256": s}, "embedded")
            for (i, c, r, a, rc, s) in EMBEDDED_FIXTURES]


def load_fixtures():
    """The embedded list, or the installed fixture file when SHA256_FIXTURES pins one (freeze-time switch)."""
    if not SHA256_FIXTURES:
        fx = embedded_fixtures()
        print("%s clause=meta fixtures=embedded n=%d" % (PRED, len(fx)))
        return fx
    path = beside(NAME_FIXTURES)
    try:
        blob = open(pinned_file(path, SHA256_FIXTURES, NAME_FIXTURES), "rb").read()
    except OSError as e:
        raise Setup("fixture file unreadable: %s" % e)
    try:
        fx = json.loads(blob.decode())
    except ValueError as e:
        raise Setup("fixture file is not JSON: %s" % e)
    if not isinstance(fx, list) or not fx:
        raise Setup("fixture file is not a non-empty list")
    if len(fx) < len(EMBEDDED_FIXTURES):
        raise Setup("fixture file has %d cases, fewer than the embedded %d" % (len(fx), len(EMBEDDED_FIXTURES)))
    return [check_fixture(c, NAME_FIXTURES) for c in fx]


# ------------------------------------------------------------------------------------------------ judge
class Judge:
    """The pinned compile-keymap + how-to-type, in a clean env (HOME/XDG in --work, no user include path)."""

    def __init__(self, work):
        self.work = work
        self.home = os.path.join(work, "judge-home")
        self.cfg = os.path.join(work, "judge-cfg")
        self.kmdir = os.path.join(work, "keymaps")
        for d in (self.home, self.cfg, self.kmdir):
            os.makedirs(d, exist_ok=True)
        pinned_file(JUDGE, JUDGE_SHA256, "how-to-type")
        pinned_file(COMPILE, COMPILE_SHA256, "compile-keymap")
        pinned_file(HEADER, HEADER_SHA256, "xkbcommon-keysyms.h")
        self.cache = {}

    def env(self):
        return {"PATH": "/usr/bin", "HOME": self.home, "XDG_CONFIG_HOME": self.cfg, "LC_ALL": "C"}

    def keymap(self, rmlvo):
        key = tuple((k, rmlvo.get(k)) for k in RMLVO_KEYS)
        if key in self.cache:
            return self.cache[key]
        argv = [COMPILE, "--rules", rmlvo.get("rules") or DEFAULTS["rules"],
                "--model", rmlvo.get("model") or DEFAULTS["model"]]
        for f in ("layout", "variant", "options"):
            if rmlvo.get(f) is not None:
                argv += ["--" + f, rmlvo[f]]
        try:
            p = subprocess.run(argv, capture_output=True, timeout=60, cwd=self.work, env=self.env())
        except subprocess.TimeoutExpired:
            raise Setup("compile-keymap timed out for %r" % (rmlvo,))
        if p.returncode != 0 or not p.stdout:
            raise Setup("compile-keymap failed (%d) for %r: %s" % (
                p.returncode, rmlvo, p.stderr.decode("utf-8", "surrogateescape")[:200]))
        path = os.path.join(self.kmdir, hashlib.sha256(p.stdout).hexdigest()[:24] + ".xkb")
        if not os.path.exists(path):
            with open(path, "wb") as fh:
                fh.write(p.stdout)
        self.cache[key] = path
        return path

    def run(self, keymap_path, arg):
        try:
            p = subprocess.run([JUDGE, "--keymap=" + keymap_path, "--disable-compose", "--keysym", arg],
                               capture_output=True, timeout=60, cwd=self.work, env=self.env())
        except subprocess.TimeoutExpired:
            raise Setup("how-to-type timed out on %r" % (arg,))
        return p.returncode, p.stdout


# ------------------------------------------------------------------------------------------------ sandbox
class Box:
    """The tool sandbox: python runtime + the keymap + the keysym header, nothing else (see clause i)."""

    def __init__(self, work, tool_path):
        self.work = work
        self.bwrap = shutil.which("bwrap")
        self.strace = shutil.which("strace")
        if not self.bwrap:
            raise Setup("bwrap missing")
        if not self.strace:
            raise Setup("strace missing")
        self.tool = tool_path
        self.python = os.path.realpath(sys.executable)
        self.stdlib = os.path.dirname(os.path.realpath(os.__file__))
        if not os.path.isdir(self.stdlib):
            raise Setup("python stdlib dir not found (%s)" % self.stdlib)
        self.libs = self.python_libs()
        self.trips = []

    def python_libs(self):
        """The shared libraries the interpreter and every stdlib extension module need (loader included).

        `ldd <python3>` alone is not enough: stdlib extensions in `lib-dynload` carry their own dependencies
        (e.g. `binascii` -> libz, `_ssl` -> libssl/libcrypto), and the contract is "Python 3 stdlib only", so
        every stdlib module the interpreter ships must be importable inside the sandbox. Nothing outside that
        closure is bound: in particular no libxkbcommon and no xkbcli binary.
        """
        targets = [self.python]
        dyn = os.path.join(self.stdlib, "lib-dynload")
        if os.path.isdir(dyn):
            targets += sorted(os.path.join(dyn, f) for f in os.listdir(dyn) if f.endswith(".so"))
        try:
            p = subprocess.run(["ldd"] + targets, capture_output=True, timeout=120,
                               env={"PATH": "/usr/bin", "LC_ALL": "C"})
        except (OSError, subprocess.TimeoutExpired) as e:
            raise Setup("ldd failed: %s" % e)
        libs = []
        for line in p.stdout.decode().splitlines():
            m = re.search(r"=>\s+(/\S+)", line)
            if m:
                # The loader looks up the SONAME path ldd printed (often a symlink such as libz.so.1);
                # bind that path AND its realpath, because bwrap mounts files, not the directory tree.
                libs.append(m.group(1))
                real = os.path.realpath(m.group(1))
                if real != m.group(1):
                    libs.append(real)
        if not libs:
            raise Setup("ldd named no shared library for %s" % self.python)
        for lib in libs:
            if "xkbcommon" in lib or lib.endswith("/xkbcli"):
                raise Setup("the runtime closure names a judge component: %s" % lib)
        return sorted(set(libs))

    def prefix(self, keymap_path):
        a = [self.bwrap, "--unshare-all", "--die-with-parent", "--new-session", "--clearenv",
             "--tmpfs", "/", "--tmpfs", "/usr", "--tmpfs", "/usr/lib",
             "--ro-bind", self.stdlib, self.stdlib,
             "--tmpfs", os.path.join(self.stdlib, "site-packages")]
        for lib in self.libs:
            a += ["--ro-bind", lib, lib]
        a += ["--symlink", "usr/lib", "/lib", "--symlink", "usr/lib", "/lib64",
              "--ro-bind", self.python, "/usr/bin/python3",
              "--ro-bind", self.tool, "/oracle/tool.py",
              "--ro-bind", HEADER, HEADER,
              "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp", "--chdir", "/",
              "--setenv", "PATH", "/usr/bin", "--setenv", "LC_ALL", "C",
              "--setenv", "HOME", "/nonexistent", "--setenv", "TMPDIR", "/tmp"]
        if keymap_path:
            a += ["--ro-bind", keymap_path, "/fixture/keymap.xkb"]
        return a

    def run(self, keymap_path, args, timeout=120, writes_ok=False):
        """Returns (rc, stdout, stderr). Every run is traced; write attempts are excused only for --selftest."""
        argv = self.prefix(keymap_path) + ["/usr/bin/python3", "-I", "/oracle/tool.py"] + list(args)
        fd, trace = tempfile.mkstemp(dir=self.work, prefix="trace-")
        os.close(fd)
        # WEAKENED r: no strace, no tripwire
        argv = argv
        try:
            p = subprocess.run(argv, capture_output=True, timeout=timeout, env={"PATH": "/usr/bin"})
            res = (p.returncode, p.stdout.decode("utf-8", "surrogateescape"),
                   p.stderr.decode("utf-8", "surrogateescape"))
        except subprocess.TimeoutExpired:
            res = (124, "", "")
        # WEAKENED r: trace not read
        if trace:
            os.unlink(trace)
        return res

    def check_trace(self, path, writes_ok=False):
        try:
            lines = open(path, encoding="latin-1").read().splitlines()
        except OSError:
            self.trips.append("trace-missing")
            return
        seen = False
        py_pid = None
        trip = re.compile(r"^(%s)\(" % "|".join(PROC_SET))
        wtrip = re.compile(r"^(%s)\(" % "|".join(WRITE_SET))
        otrip = re.compile(r"^(%s)\(" % "|".join(OPEN_SET))
        for ln in lines:
            pid, _, rest = ln.partition(" ")
            rest = rest.strip()
            # strace attach noise ("???", "<detached ...>") and resume/exit tails are not new invocations.
            # The python3 execve may be split (`<unfinished ...>` then `<... execve resumed>`).
            if not seen:
                if 'execve("/usr/bin/python3"' in rest:
                    py_pid = pid
                    seen = rest.endswith("= 0")
                elif pid == py_pid and rest.startswith("<... execve resumed>"):
                    seen = rest.endswith("= 0")
                continue
            if rest.startswith("<..."):
                continue
            if trip.match(rest):
                self.trips.append(rest[:60])
            elif wtrip.match(rest) or (otrip.match(rest) and WRITE_FLAGS.search(QUOTED.sub('""', rest))):
                if writes_ok and tmp_write(rest):
                    continue
                self.trips.append("write:" + rest[:60])
        if not seen:
            self.trips.append("python-execve-not-seen")
        os.unlink(path)


# ------------------------------------------------------------------------------------------------ generator
def gen_case(rng, k):
    layout, variant = rng.choice(LAYOUT_PAIRS)
    rmlvo = {"rules": "evdev", "model": "pc105", "layout": layout}
    if variant is not None:
        rmlvo["variant"] = variant
    opt = rng.choice(OPTIONS)
    if opt is not None:
        rmlvo["options"] = opt
    r = rng.random()
    if r < 0.60:
        arg = rng.choice(NAMES)
    elif r < 0.75:
        v = rng.randrange(0x20, 0x100)
        arg = rng.choice(["0x%02x" % v, str(v)])
    elif r < 0.85:
        arg = "0x1000%04x" % rng.randrange(0, 0x3000)
    elif r < 0.92:
        arg = rng.choice(ABSENT)
    else:
        arg = rng.choice(INVALID)
    return {"id": "g%03d" % k, "class": "generated", "rmlvo": rmlvo, "arg": arg}


# ------------------------------------------------------------------------------------------------ clauses
def selftest_clause(box):
    rc, out, _err = box.run(None, ["--selftest"], timeout=120, writes_ok=True)
    last = ""
    for line in out.split("\n"):
        if line.strip():
            last = line.strip()
    m = SELFTEST_LINE.match(last)
    ok = bool(m) and rc == 0 and m.group(1) == m.group(2) and int(m.group(1)) >= SELFTEST_MIN
    print("%s clause=s selftest rc=%d last=%r %s" % (PRED, rc, last[:120], "ok" if ok else "fail"))
    return ok


def refusal_clause(box, keymap_path):
    ok = True
    why = []
    for name, args in (("no-disable-compose", ["how-to-type", "--keymap", "/fixture/keymap.xkb", "--keysym",
                                               "slash"]),
                       ("no-keysym", ["how-to-type", "--keymap", "/fixture/keymap.xkb", "--disable-compose"])):
        rc, out, _err = box.run(keymap_path, args)
        good = rc == 2 and "=== Direct access ===" not in out
        if not good:
            ok = False
            why.append("%s: rc=%d table=%s" % (name, rc, "yes" if "=== Direct access ===" in out else "no"))
    print("%s clause=s refusals=%s%s" % (PRED, "ok" if ok else "fail", "" if ok else " " + "; ".join(why)))
    return ok


def run_case(box, judge, case):
    """Judge one case: (ok, why)."""
    km = judge.keymap(case["rmlvo"])
    j_rc, j_out = judge.run(km, case["arg"])
    t_rc, t_out, _t_err = box.run(km, ["how-to-type", "--keymap", "/fixture/keymap.xkb", "--disable-compose",
                                       "--keysym", case["arg"]])
    ok = (t_rc == j_rc and t_out.encode("utf-8", "surrogateescape") == j_out)
    why = "" if ok else "arg=%r judge=%d/%d tool=%d/%d" % (
        case["arg"], j_rc, len(j_out), t_rc, len(t_out.encode("utf-8", "surrogateescape")))
    return ok, why, j_rc, j_out


def score(repo, rev, work, nonce):
    full = git(repo, "rev-parse", "--verify", rev + "^{commit}")
    if full is None:
        raise Setup("bad rev %r" % (rev,))
    full = full.decode().strip()
    fx = load_fixtures()
    print("%s clause=meta rev=%s nonce=%d lane=%s fixtures=%d" % (PRED, full, nonce, lane_root(), len(fx)))
    ls = git(repo, "ls-tree", full, "--", TOOL)
    fields = ls.split() if ls else []
    present = len(fields) >= 3 and fields[0] in (b"100644", b"100755") and fields[1] == b"blob"
    print("%s clause=t tool=%s" % (PRED, "present" if present else "absent"))
    if not present:
        print("%s: fixtures=0/%d generated=0/%d selftest=fail readonly=fail tool=absent verdict=TARGET_MISSED" % (
            PRED, len(fx), GEN))
        return 1
    tdir = tempfile.mkdtemp(dir=work, prefix="tool-")
    tool = os.path.join(tdir, "tool.py")
    blob = git(repo, "show", "%s:%s" % (full, TOOL))
    if blob is None:
        raise Setup("git show %s:%s failed" % (full, TOOL))
    with open(tool, "wb") as fh:
        fh.write(blob)
    judge = Judge(work)
    print("%s clause=j judge=%s compile=%s header=%s" % (
        PRED, JUDGE_SHA256[:16], COMPILE_SHA256[:16], HEADER_SHA256[:16]))
    box = Box(work, tool)
    print("%s clause=i python=%s stdlib=%s libs=%d site_packages=hidden net=none" % (
        PRED, os.path.basename(os.path.realpath(sys.executable)), box.stdlib, len(box.libs)))
    s_ok = selftest_clause(box)
    first_km = judge.keymap(fx[0]["rmlvo"])
    refusal_ok = refusal_clause(box, first_km)
    f_ok = 0
    drift = []
    for case in fx:
        j_rc, j_out = judge.run(judge.keymap(case["rmlvo"]), case["arg"])
        if j_rc != case["rc"] or hashlib.sha256(j_out).hexdigest() != case["sha256"]:
            drift.append(case["id"])
        ok, why, _jrc, _jout = run_case(box, judge, case)
        f_ok += ok
        print("%s clause=f fixture=%s class=%s %s%s" % (
            PRED, case["id"], case["class"], "pass" if ok else "FAIL", "" if ok else " " + why))
    print("%s clause=f fixtures=%d/%d" % (PRED, f_ok, len(fx)))
    if drift:
        raise Setup("the judge drifted from %d recorded fixture(s): %s" % (len(drift), ",".join(drift[:5])))
    grng = random.Random(nonce)
    g_ok = 0
    first_fail = None
    for k in range(GEN):
        case = gen_case(grng, k)
        ok, why, _r, _o = run_case(box, judge, case)
        g_ok += ok
        if not ok:
            print("%s clause=g case=%s FAIL rmlvo=%r %s" % (PRED, case["id"], case["rmlvo"], why))
            if first_fail is None:
                first_fail = (case["id"], why)
    print("%s clause=g generated=%d/%d%s" % (PRED, g_ok, GEN, "" if first_fail is None else
                                             " first_fail=%r" % (first_fail,)))
    readonly = "ok" if not box.trips else "fail"
    print("%s clause=r trips=%d %s" % (PRED, len(box.trips), ";".join(sorted(set(box.trips)))[:300]))
    selftest = "ok" if (s_ok and refusal_ok) else "fail"
    met = present and selftest == "ok" and readonly == "ok" and f_ok == len(fx) and g_ok == GEN
    print("%s: fixtures=%d/%d generated=%d/%d selftest=%s readonly=%s tool=%s verdict=%s" % (
        PRED, f_ok, len(fx), g_ok, GEN, selftest, readonly, "present" if present else "absent",
        "TARGET_MET" if met else "TARGET_MISSED"))
    return 0 if met else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--nonce", type=int, default=None)
    a = ap.parse_args()
    nonce = a.nonce if a.nonce is not None else int.from_bytes(os.urandom(4), "big")
    try:
        if not os.path.isdir(a.work):
            raise Setup("work dir missing")
        work_root = os.path.realpath(a.work)
        for bad in ("/tmp", "/var/tmp"):
            if under(work_root, bad):
                raise Setup("work dir under %s (SentScratch: use a scratch filesystem)" % bad)
        tmp = os.environ.get("TMPDIR")
        if tmp and under(tmp, "/tmp"):
            raise Setup("TMPDIR is under /tmp (SentScratch: set TMPDIR outside /tmp)")
        for h in sorted({os.path.realpath(a.repo), lane_root(), os.path.dirname(lane_root())}):
            if under(work_root, h):
                raise Setup("work dir inside a hidden path %s" % h)
        if under(work_root, "/run") or under(work_root, "/proc") or under(work_root, "/dev"):
            raise Setup("work dir under /run, /proc or /dev")
        work = tempfile.mkdtemp(dir=work_root, prefix="c1r49-")
        try:
            return score(a.repo, a.rev, work, nonce)
        finally:
            shutil.rmtree(work, ignore_errors=True)
    except Setup as e:
        print("%s: SETUP %s" % (PRED, e))
        return 2


if __name__ == "__main__":
    sys.exit(main())
