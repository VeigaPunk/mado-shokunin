#!/usr/bin/env python3
"""mado C1 judge harness -- the pinned how-to-type oracle.

Contract
--------
    oracle(rmlvo, arg, work) -> (keymap_bytes, stdout, stderr, rc)

    keymap_bytes   stdout of the pinned xkbcli-compile-keymap for ``rmlvo``
    stdout         stdout of the pinned xkbcli-how-to-type for ``arg``
    stderr         stderr of that same run (diagnostics only -- see "Channels")
    rc             exit status of that same run

Exact argv, in this order (nothing else is added, nothing is reordered):

    1. /usr/lib/xkbcommon/xkbcli-compile-keymap
         [--rules RULES] [--model MODEL] [--layout LAYOUT]
         [--variant VARIANT] [--options OPTIONS]
       (flags emitted only for RMLVO components that are not None, in that
        order; no --include*, no --enable-environment-names, no --format)

    2. /usr/lib/xkbcommon/xkbcli-how-to-type
         --keymap=<work>/keymap.xkb --disable-compose --keysym ARG

Child environment -- exactly these four names, nothing else inherited:

    PATH=/usr/bin  HOME=<work>/home  XDG_CONFIG_HOME=<work>/cfg  LC_ALL=C

That is ``env -i PATH=/usr/bin HOME=... XDG_CONFIG_HOME=... LC_ALL=C``
byte-for-byte (execve with a freshly built vector); ``selfcheck`` proves each
name is load-bearing, which is why the vector is built rather than filtered.

Channels
--------
Only **stdout + rc** are a byte-comparable contract.  stderr embeds argv[0]
inside the usage text (``Usage: /usr/lib/xkbcommon/xkbcli-how-to-type ...``)
and, on include-path failure, the absolute include list -- so it changes with
the binary spelling and with the work-dir path.  It is returned for diagnosis,
never for equality.

Behavior on a keymap the judge cannot parse is *not* special-cased here: the
oracle reports the pinned binary's own (stdout, stderr, rc) verbatim.
Measured on this host (libxkbcommon 1.13.2-1): rc 1, 0 bytes of stdout,
``xkbcommon: ERROR: [XKB-822] Failed to parse input xkb file`` then
``ERROR: Failed to create XKB keymap`` on stderr.  A tool under test must
reproduce stdout+rc; it cannot be excused from a malformed fixture.

Pins
----
Every run re-hashes both binaries and refuses on mismatch:
  xkbcli-compile-keymap 43b924f68651500e022c74371515154f8c50a2e087defa6b834cc5d41fd77250
  xkbcli-how-to-type    f6c0b122ad90c9e30086653517c51f4b2203b6c7c07bcbc89c71e55ab2927e54

Work dir
--------
``work`` is a directory owned by the caller.  This module creates it if
missing and writes only ``work/keymap.xkb``, ``work/home/`` and ``work/cfg/``.
It refuses a work dir under /tmp, /var/tmp or /dev/shm, and it refuses to run
when a user XKB tree (``cfg/xkb``, ``home/.config/xkb``, ``home/.xkb``) already
exists in it -- either would change the compiled keymap (measured: a single
``cfg/xkb/symbols/br`` file changes the keymap digest).

Python 3 stdlib only.  Spawns exactly the two pinned binaries; no socket, no
network, no shell.

Self-check (the receipt this module emits):

    python3 -I oracle.py selfcheck --work <scratch>/sc

"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

# --------------------------------------------------------------------------
# pins

COMPILE_KEYMAP = "/usr/lib/xkbcommon/xkbcli-compile-keymap"
COMPILE_KEYMAP_SHA256 = (
    "43b924f68651500e022c74371515154f8c50a2e087defa6b834cc5d41fd77250"
)
HOW_TO_TYPE = "/usr/lib/xkbcommon/xkbcli-how-to-type"
HOW_TO_TYPE_SHA256 = (
    "f6c0b122ad90c9e30086653517c51f4b2203b6c7c07bcbc89c71e55ab2927e54"
)

PINNED = (
    (COMPILE_KEYMAP, COMPILE_KEYMAP_SHA256),
    (HOW_TO_TYPE, HOW_TO_TYPE_SHA256),
)

RMLVO_FLAGS = (
    ("rules", "--rules"),
    ("model", "--model"),
    ("layout", "--layout"),
    ("variant", "--variant"),
    ("options", "--options"),
)
RMLVO_KEYS = tuple(k for k, _ in RMLVO_FLAGS)

KEYMAP_NAME = "keymap.xkb"
DEFAULT_TIMEOUT = 60.0

# work dirs that make a receipt uncitable (operator directive 2026-10-25)
FORBIDDEN_WORK = ("/tmp", "/var/tmp", "/dev/shm")


class OracleError(RuntimeError):
    """Base class for every harness refusal / failure."""


class PinMismatch(OracleError):
    """A pinned binary's sha256 is not the frozen one."""


class CompileError(OracleError):
    """xkbcli-compile-keymap did not produce a keymap."""


class WorkDirRefused(OracleError):
    """The work dir is unusable (tmpfs, poisoned XKB tree, or a file)."""


class JudgeTimeout(OracleError):
    """A pinned binary exceeded its deadline."""


# --------------------------------------------------------------------------
# pins / hashing


def sha256_file(path: str | os.PathLike) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


_PINS_VERIFIED = False


def verify_pins(*, cached: bool = True) -> dict[str, str]:
    """Re-hash both pinned binaries; return {path: sha256} or raise."""
    global _PINS_VERIFIED
    if cached and _PINS_VERIFIED:
        return {path: digest for path, digest in PINNED}
    observed: dict[str, str] = {}
    for path, expected in PINNED:
        try:
            actual = sha256_file(path)
        except OSError as exc:
            raise PinMismatch(f"cannot hash pinned binary {path}: {exc}") from exc
        if actual != expected:
            raise PinMismatch(
                f"pin mismatch for {path}: expected {expected}, got {actual}"
            )
        observed[path] = actual
    _PINS_VERIFIED = True
    return observed


# --------------------------------------------------------------------------
# work dir


def resolve_work(work: str | os.PathLike) -> Path:
    path = Path(work).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    path = path.resolve()
    for bad in FORBIDDEN_WORK:
        bad_path = Path(bad)
        if path == bad_path or bad_path in path.parents:
            raise WorkDirRefused(
                f"work dir {path} is under {bad}; use a scratch dir "
                "(TMPDIR/'--work' must not be tmpfs)"
            )
    if path.exists() and not path.is_dir():
        raise WorkDirRefused(f"work dir {path} exists and is not a directory")
    path.mkdir(parents=True, exist_ok=True)
    return path


def _assert_clean_state(work: Path) -> None:
    """Refuse a work dir whose HOME/XDG tree could shadow the XKB config."""
    for rel in ("cfg/xkb", "home/.config/xkb", "home/.xkb"):
        candidate = work / rel
        if candidate.exists():
            raise WorkDirRefused(
                f"work dir {work} already carries a user XKB tree ({rel}); "
                "it changes the compiled keymap -- use a fresh work dir"
            )


def clean_env(work: Path) -> dict[str, str]:
    """The exact child environment: four names, nothing inherited."""
    home = work / "home"
    cfg = work / "cfg"
    home.mkdir(parents=True, exist_ok=True)
    cfg.mkdir(parents=True, exist_ok=True)
    return {
        "PATH": "/usr/bin",
        "HOME": str(home),
        "XDG_CONFIG_HOME": str(cfg),
        "LC_ALL": "C",
    }


# --------------------------------------------------------------------------
# core


def _run(argv: list[str], env: dict[str, str], cwd: Path) -> tuple[bytes, bytes, int]:
    try:
        completed = subprocess.run(
            argv,
            env=env,
            cwd=str(cwd),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=DEFAULT_TIMEOUT,
        )
    except subprocess.TimeoutExpired as exc:
        raise JudgeTimeout(f"{argv[0]} exceeded {DEFAULT_TIMEOUT}s") from exc
    return completed.stdout, completed.stderr, completed.returncode


def _as_rmlvo(rmlvo) -> dict[str, str]:
    if rmlvo is None:
        return {}
    if not hasattr(rmlvo, "items"):
        raise TypeError("rmlvo must be a mapping or None")
    unknown = sorted(set(rmlvo) - set(RMLVO_KEYS))
    if unknown:
        raise ValueError(f"unknown RMLVO component(s): {', '.join(unknown)}")
    out: dict[str, str] = {}
    for key in RMLVO_KEYS:
        value = rmlvo.get(key)
        if value is None:
            continue
        if not isinstance(value, str) or not value or "\0" in value:
            raise ValueError(f"RMLVO component {key!r} must be a non-empty string")
        out[key] = value
    return out


def compile_argv(rmlvo) -> list[str]:
    names = _as_rmlvo(rmlvo)
    argv = [COMPILE_KEYMAP]
    for key, flag in RMLVO_FLAGS:
        if key in names:
            argv.extend((flag, names[key]))
    return argv


def judge_argv(keymap_path: Path, arg: str) -> list[str]:
    return [
        HOW_TO_TYPE,
        f"--keymap={keymap_path}",
        "--disable-compose",
        "--keysym",
        arg,
    ]


def compile_keymap(rmlvo, work: str | os.PathLike) -> bytes:
    """Compile ``rmlvo`` with the pinned compile-keymap; return the keymap bytes."""
    verify_pins()
    root = resolve_work(work)
    _assert_clean_state(root)
    env = clean_env(root)
    argv = compile_argv(rmlvo)
    stdout, stderr, rc = _run(argv, env, root)
    if rc != 0:
        raise CompileError(
            f"compile-keymap failed (rc={rc}) for {_as_rmlvo(rmlvo)}: "
            f"argv={argv!r} stderr={stderr.decode('utf-8', 'replace')[-800:]!r}"
        )
    if not stdout:
        raise CompileError(f"compile-keymap produced no keymap for {_as_rmlvo(rmlvo)}")
    return stdout


def judge(
    keymap_bytes: bytes, arg: str, work: str | os.PathLike
) -> tuple[bytes, bytes, int]:
    """Run the pinned how-to-type on ``keymap_bytes``; return (stdout, stderr, rc)."""
    verify_pins()
    if not isinstance(keymap_bytes, (bytes, bytearray)):
        raise TypeError("keymap_bytes must be bytes")
    if not isinstance(arg, str) or not arg or "\0" in arg:
        raise ValueError("arg must be a non-empty string without NUL")
    root = resolve_work(work)
    _assert_clean_state(root)
    env = clean_env(root)
    keymap_path = root / KEYMAP_NAME
    keymap_path.write_bytes(bytes(keymap_bytes))
    argv = judge_argv(keymap_path, arg)
    return _run(argv, env, root)


def oracle(rmlvo, arg: str, work: str | os.PathLike):
    """(keymap_bytes, stdout, stderr, rc) for one (RMLVO, keysym-arg) case."""
    keymap_bytes = compile_keymap(rmlvo, work)
    stdout, stderr, rc = judge(keymap_bytes, arg, work)
    return keymap_bytes, stdout, stderr, rc


# --------------------------------------------------------------------------
# demonstration fixtures (NOT the frozen counter fixtures; the L1 freezes
# those.  These exist so the harness has a measurable floor.)

CASES = (
    ("us-return", {"layout": "us"}, "Return"),
    ("us-space", {"layout": "us"}, "space"),
    ("us-slash", {"layout": "us"}, "slash"),
    ("us-a", {"layout": "us"}, "a"),
    ("us-A", {"layout": "us"}, "A"),
    ("us-exclam", {"layout": "us"}, "exclam"),
    ("us-at", {"layout": "us"}, "at"),
    ("us-numbersign", {"layout": "us"}, "numbersign"),
    ("us-eurosign", {"layout": "us"}, "EuroSign"),
    ("us-eacute", {"layout": "us"}, "eacute"),
    ("us-u00e9", {"layout": "us"}, "U00e9"),
    ("us-u20ac", {"layout": "us"}, "U20AC"),
    ("us-dead-acute", {"layout": "us"}, "dead_acute"),
    ("us-lvl3", {"layout": "us"}, "ISO_Level3_Shift"),
    ("us-hex-return", {"layout": "us"}, "0xff0d"),
    ("us-dec-13", {"layout": "us"}, "13"),
    ("us-hex-space", {"layout": "us"}, "0x20"),
    ("us-iso-left-tab", {"layout": "us"}, "ISO_Left_Tab"),
    ("us-tab", {"layout": "us"}, "Tab"),
    ("us-backspace", {"layout": "us"}, "BackSpace"),
    ("us-kp-enter", {"layout": "us"}, "KP_Enter"),
    ("us-shift-l", {"layout": "us"}, "Shift_L"),
    ("us-f1", {"layout": "us"}, "F1"),
    ("us-nosymbol", {"layout": "us"}, "NoSymbol"),
    ("us-nosuchsym", {"layout": "us"}, "nosuchsym"),
    ("br-slash", {"layout": "br"}, "slash"),
    ("br-return", {"layout": "br"}, "Return"),
    ("br-dead-acute", {"layout": "br"}, "dead_acute"),
    ("br-q", {"layout": "br"}, "q"),
    ("br-Q", {"layout": "br"}, "Q"),
    ("br-compose-caps", {"layout": "br", "options": "compose:caps"}, "slash"),
    ("br-compose-caps-multi-key",
     {"layout": "br", "options": "compose:caps"}, "Multi_key"),
    ("br-multi-key", {"layout": "br"}, "Multi_key"),
    ("br-compose-ralt", {"layout": "br", "options": "compose:ralt"}, "slash"),
    ("br-nodeadkeys-dead-acute",
     {"layout": "br", "variant": "nodeadkeys"}, "dead_acute"),
    ("br-nodeadkeys-acute",
     {"layout": "br", "variant": "nodeadkeys"}, "acute"),
    ("br-abnt2-slash", {"layout": "br", "model": "abnt2"}, "slash"),
    ("de-z", {"layout": "de"}, "z"),
    ("de-y", {"layout": "de"}, "y"),
    ("de-adiaeresis", {"layout": "de"}, "adiaeresis"),
    ("de-ssharp", {"layout": "de"}, "ssharp"),
    ("de-nodeadkeys-acute",
     {"layout": "de", "variant": "nodeadkeys"}, "acute"),
    ("de-lvl3-euro", {"layout": "de", "options": "lv3:ralt_switch"}, "EuroSign"),
    ("fr-a", {"layout": "fr"}, "a"),
    ("fr-dead-grave", {"layout": "fr"}, "dead_grave"),
    ("fr-lvl3-euro", {"layout": "fr", "options": "lv3:ralt_switch"}, "EuroSign"),
    ("ru-cyrillic-a", {"layout": "ru"}, "Cyrillic_a"),
    ("ru-cyrillic-A", {"layout": "ru"}, "Cyrillic_A"),
    ("ru-grp-toggle",
     {"layout": "ru", "options": "grp:alt_shift_toggle"}, "Cyrillic_a"),
    ("jp-yen", {"layout": "jp"}, "yen"),
    ("gb-sterling", {"layout": "gb"}, "sterling"),
    ("es-ntilde", {"layout": "es"}, "ntilde"),
    ("pt-ccedilla", {"layout": "pt"}, "ccedilla"),
    ("it-egrave", {"layout": "it"}, "egrave"),
    ("no-oslash", {"layout": "no"}, "oslash"),
    ("se-odiaeresis", {"layout": "se"}, "odiaeresis"),
    ("pl-aogonek", {"layout": "pl"}, "aogonek"),
    ("tr-dotlessi", {"layout": "tr"}, "dotlessi"),
    ("gr-greek-alpha", {"layout": "gr"}, "Greek_alpha"),
    ("in-rupee", {"layout": "in"}, "rupee"),
    ("us-intl-dead-acute", {"layout": "us", "variant": "intl"}, "dead_acute"),
    ("us-dvorak-apostrophe", {"layout": "us", "variant": "dvorak"}, "apostrophe"),
    ("us-colemak-e", {"layout": "us", "variant": "colemak"}, "e"),
    ("us-pc104-slash", {"layout": "us", "model": "pc104"}, "slash"),
    ("us-apple-slash", {"layout": "us", "model": "apple"}, "slash"),
    ("us-rules-base-return", {"layout": "us", "rules": "base"}, "Return"),
    ("us-ctrl-nocaps-return",
     {"layout": "us", "options": "ctrl:nocaps"}, "Return"),
    ("us-caps-escape-escape",
     {"layout": "us", "options": "caps:escape"}, "Escape"),
    ("us-lvl3-ralt", {"layout": "us", "options": "lv3:ralt_switch"},
     "ISO_Level3_Shift"),
    ("br-hex-slash", {"layout": "br"}, "0x2f"),
    ("br-hex-return", {"layout": "br"}, "0xff0d"),
    ("defaults-return", {}, "Return"),
)

# environment vectors whose *child-side* presence the selfcheck measures
LOCALE_VECTORS = (
    {"LC_ALL": "C"},
    {"LC_ALL": "C.UTF-8"},
    {"LC_ALL": "en_US.UTF-8"},
    {"LC_ALL": "pt_BR.UTF-8"},
    {"LANG": "en_US.UTF-8"},
    {"LANG": "tr_TR.UTF-8"},
    {},  # neither LC_ALL nor LANG
)

POISON_SYMBOLS = """default partial alphanumeric_keys
xkb_symbols "basic" {
    include "us(basic)"
    name[Group1]= "Poisoned";
};
"""


# --------------------------------------------------------------------------
# selfcheck


def _scrub(text: str, work: Path) -> str:
    return text.replace(str(work), "<work>")


def _digest(data: bytes) -> str:
    return sha256_bytes(data)[:16]


def _short_argv(argv: list[str], work: Path) -> str:
    return " ".join(_scrub(a, work) for a in argv)


def _selfcheck(work: str | os.PathLike, reps: int, cost_n: int) -> int:
    root = resolve_work(work)
    out: list[str] = []

    def emit(line: str = "") -> None:
        out.append(_scrub(line, root))

    emit("# mado round 49 w1 ExecOracle -- C1 judge harness selfcheck")
    emit(f"# generated: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}")
    emit(f"# python: {sys.version.split()[0]}  stdlib only")
    emit(f"# work: <work>  (scratch; sanitized in this receipt)")
    emit()

    emit("== 1. pins ==")
    pins = verify_pins(cached=False)
    for path, expected in PINNED:
        emit(f"pin {path} sha256={pins[path]} expected={expected} "
             f"{'ok' if pins[path] == expected else 'MISMATCH'}")
    for package in ("libxkbcommon", "xkeyboard-config"):
        installed = sorted(
            path.name
            for path in Path("/var/lib/pacman/local").glob(f"{package}-[0-9]*")
        )
        emit(f"package {package}: {', '.join(installed) or 'not found'} "
             "(read-only package-database directory listing)")
    emit()

    emit("== 2. exact argv (case us-return) ==")
    sample_dir = root / "argv" / "us-return"
    sample_env = clean_env(sample_dir)
    emit(f"compile: {_short_argv(compile_argv(CASES[0][1]), root)}")
    emit(f"judge:   {_short_argv(judge_argv(sample_dir / KEYMAP_NAME, CASES[0][2]), root)}")
    emit(f"env:     {_short_argv([f'{k}={v}' for k, v in sorted(sample_env.items())], root)}")
    emit()

    emit(f"== 3. determinism: {len(CASES)} cases x {reps} runs ==")
    emit("case rc km out err reps identical")
    identical = 0
    failures: list[str] = []
    for label, rmlvo, arg in CASES:
        case_dir = root / "cases" / label
        triples = []
        for _ in range(reps):
            keymap_bytes, stdout, stderr, rc = oracle(rmlvo, arg, case_dir)
            triples.append(
                (_digest(keymap_bytes), _digest(stdout), _digest(stderr), rc)
            )
        same = all(item == triples[0] for item in triples)
        identical += 1 if same else 0
        if not same:
            failures.append(label)
        emit(f"{label} rc={triples[0][3]} km={triples[0][0]} out={triples[0][1]} "
             f"err={triples[0][2]} reps={reps} identical={'yes' if same else 'NO'}")
    emit(f"summary: {identical}/{len(CASES)} cases identical over {reps} runs")
    if failures:
        emit(f"FAILED: {', '.join(failures)}")
    emit()

    emit(f"== 4. cost per call (n={cost_n}) ==")
    cost_dir = root / "cost"
    oracle_ms: list[float] = []
    compile_ms: list[float] = []
    judge_ms: list[float] = []
    for index in range(cost_n):
        rmlvo = {"layout": "br", "options": "compose:caps"} if index % 2 else {"layout": "us"}
        arg = "slash" if index % 2 else "Return"
        started = time.perf_counter()
        keymap_bytes = compile_keymap(rmlvo, cost_dir / f"c{index}")
        mid = time.perf_counter()
        judge(keymap_bytes, arg, cost_dir / f"c{index}")
        ended = time.perf_counter()
        compile_ms.append((mid - started) * 1000.0)
        judge_ms.append((ended - mid) * 1000.0)
        oracle_ms.append((ended - started) * 1000.0)

    def stats(values: list[float]) -> str:
        ordered = sorted(values)
        median = ordered[len(ordered) // 2]
        return (f"median={median:.2f}ms min={ordered[0]:.2f}ms "
                f"max={ordered[-1]:.2f}ms")

    emit(f"oracle: {stats(oracle_ms)}")
    emit(f"compile: {stats(compile_ms)}")
    emit(f"judge: {stats(judge_ms)}")
    emit()

    emit("== 5. environment isolation ==")
    env_dir = root / "env"
    base_rmlvo = {"layout": "br", "options": "compose:caps"}
    # (a) parent-side variables must not reach the children
    baseline = oracle(base_rmlvo, "slash", env_dir / "baseline")
    parent_keys = {
        "XKB_CONFIG_ROOT": "/nonexistent",
        "XKB_CONFIG_EXTRA_PATH": "/nonexistent",
        "XKB_DEFAULT_RULES": "evdev",
        "XKB_DEFAULT_MODEL": "pc105",
        "XKB_DEFAULT_LAYOUT": "de",
        "XKB_DEFAULT_VARIANT": "nodeadkeys",
        "XKB_DEFAULT_OPTIONS": "compose:ralt",
        "XKB_LOG_LEVEL": "debug",
    }
    saved = {key: os.environ.get(key) for key in parent_keys}
    try:
        os.environ.update(parent_keys)
        polluted = oracle(base_rmlvo, "slash", env_dir / "polluted-parent")
    finally:
        for key, value in saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
    emit("a) parent env carries XKB_CONFIG_ROOT=/nonexistent, "
         "XKB_CONFIG_EXTRA_PATH=/nonexistent, all XKB_DEFAULT_*, XKB_LOG_LEVEL=debug")
    emit(f"   baseline km={_digest(baseline[0])} out={_digest(baseline[1])} rc={baseline[3]}")
    emit(f"   polluted km={_digest(polluted[0])} out={_digest(polluted[1])} rc={polluted[3]}")
    emit(f"   identical={'yes' if baseline == polluted else 'NO'} (env -i holds)")

    # (b) ... while the same vectors do reach a binary when they are passed
    #     to the child on purpose: proof the vector is load-bearing.
    #     (libxkbcommon falls back to DFLT_XKB_LEGACY_ROOT when the canonical
    #      root cannot be appended, so one bogus root alone is not enough.)
    raw_dir = resolve_work(env_dir / "raw")
    emit("b) child env forced per variant (compile --layout br --options compose:caps):")
    for index, (label, extra) in enumerate((
        ("XKB_CONFIG_ROOT=/nonexistent", {"XKB_CONFIG_ROOT": "/nonexistent"}),
        ("XKB_CONFIG_EXTRA_PATH=/nonexistent", {"XKB_CONFIG_EXTRA_PATH": "/nonexistent"}),
        ("both=/nonexistent", {"XKB_CONFIG_ROOT": "/nonexistent",
                               "XKB_CONFIG_EXTRA_PATH": "/nonexistent"}),
        ("XKB_CONFIG_ROOT='' + XKB_CONFIG_EXTRA_PATH=/nonexistent",
         {"XKB_CONFIG_ROOT": "", "XKB_CONFIG_EXTRA_PATH": "/nonexistent"}),
    ), start=1):
        variant_dir = resolve_work(raw_dir / f"v{index}")
        variant_env = clean_env(variant_dir)
        variant_env.update(extra)
        stdout, stderr, rc = _run(compile_argv(base_rmlvo), variant_env, variant_dir)
        first = stderr.decode("utf-8", "replace").splitlines()[0] if stderr else ""
        emit(f"   {label}: rc={rc} stdout_bytes={len(stdout)} "
             f"first_stderr={_scrub(first, root)!r}")

    # (c) a user XKB tree in XDG_CONFIG_HOME changes the compiled keymap ...
    poison_dir = resolve_work(env_dir / "poison")
    poison_cfg = poison_dir / "xkb" / "symbols"
    poison_cfg.mkdir(parents=True, exist_ok=True)
    (poison_cfg / "br").write_text(POISON_SYMBOLS, encoding="utf-8")
    raw_poison_env = clean_env(raw_dir / "poison")
    raw_poison_env["XDG_CONFIG_HOME"] = str(poison_dir)
    poisoned_stdout, _, poisoned_rc = _run(compile_argv({"layout": "br"}), raw_poison_env, raw_dir / "poison")
    clean_stdout, _, clean_rc = _run(
        compile_argv({"layout": "br"}), clean_env(raw_dir / "clean"), raw_dir / "clean"
    )
    emit("c) child XDG_CONFIG_HOME pointing at a cfg/xkb/symbols/br override")
    emit(f"   poisoned rc={poisoned_rc} km={_digest(poisoned_stdout)}")
    emit(f"   clean    rc={clean_rc} km={_digest(clean_stdout)}")
    emit(f"   identical={'yes' if poisoned_stdout == clean_stdout else 'NO'} "
         "(why cfg/ must be an empty scratch dir)")
    # ... and the oracle is immune because it always points XDG_CONFIG_HOME at
    # its own empty cfg/:
    poisoned_parent = resolve_work(env_dir / "poisoned-parent-cfg")
    (poisoned_parent / "cfg" / "xkb" / "symbols").mkdir(parents=True, exist_ok=True)
    (poisoned_parent / "cfg" / "xkb" / "symbols" / "br").write_text(POISON_SYMBOLS, encoding="utf-8")
    try:
        oracle({"layout": "br"}, "slash", poisoned_parent)
        clean_cfg_run = "ok"
    except WorkDirRefused as exc:
        clean_cfg_run = f"refused: {type(exc).__name__}"
    emit(f"   oracle() with a poisoned cfg/xkb already in its work dir -> {clean_cfg_run}")

    # (d) XKB_LOG_LEVEL reaches stderr of a deliberately polluted child
    raw_log_env = clean_env(raw_dir / "log")
    keymap_path = raw_dir / "log" / KEYMAP_NAME
    keymap_path.write_bytes(clean_stdout)
    quiet = _run(judge_argv(keymap_path, "slash"), raw_log_env, raw_dir / "log")
    raw_log_env["XKB_LOG_LEVEL"] = "debug"
    noisy = _run(judge_argv(keymap_path, "slash"), raw_log_env, raw_dir / "log")
    emit("d) XKB_LOG_LEVEL=debug handed to the child on purpose")
    emit(f"   quiet  rc={quiet[2]} stdout={_digest(quiet[0])} stderr_bytes={len(quiet[1])}")
    emit(f"   noisy  rc={noisy[2]} stdout={_digest(noisy[0])} stderr_bytes={len(noisy[1])}")
    emit(f"   stdout+rc identical={'yes' if (quiet[0], quiet[2]) == (noisy[0], noisy[2]) else 'NO'}; "
         f"stderr identical={'yes' if quiet[1] == noisy[1] else 'NO'} "
         "(stderr is diagnostics, never contract)")
    emit()

    emit("== 6. keymap-file edge cases: what the judge does (no special-casing) ==")
    good_dir = root / "malformed" / "source"
    good = compile_keymap({"layout": "br"}, good_dir)
    variants = {
        "truncated-half": good[: len(good) // 2],
        "truncated-final-bytes": good[:-8],
        "trailing-garbage": good + b"\n!!! not xkb !!!\n",
        "trailing-line-comment": good + b"// trailing line comment\n",
        "trailing-block-comment": good + b"/* trailing block comment */\n",
        "empty": b"",
        "plain-text": b"hello\n",
        "missing-file": None,
    }
    emit("variant rc stdout_bytes stderr_lines last_stderr")
    for name, payload in variants.items():
        case_dir = resolve_work(root / "malformed" / name)
        env = clean_env(case_dir)
        path = case_dir / KEYMAP_NAME
        if payload is None:
            if path.exists():
                path.unlink()
        else:
            path.write_bytes(payload)
        stdout, stderr, rc = _run(judge_argv(path, "Return"), env, case_dir)
        lines = stderr.decode("utf-8", "replace").splitlines()
        emit(f"{name} rc={rc} stdout_bytes={len(stdout)} stderr_lines={len(lines)} "
             f"last={lines[-1] if lines else ''!r}")
    emit()

    emit("== 7. locale sensitivity (compile + judge, --disable-compose) ==")
    locale_dir = root / "locale"
    reference = None
    for vector in LOCALE_VECTORS:
        env = clean_env(locale_dir)
        env.update(vector)
        keymap_stdout, keymap_stderr, keymap_rc = _run(
            compile_argv({"layout": "br", "options": "compose:caps"}), env, locale_dir
        )
        path = locale_dir / KEYMAP_NAME
        path.write_bytes(keymap_stdout)
        stdout, stderr, rc = _run(judge_argv(path, "slash"), env, locale_dir)
        triple = (
            _digest(keymap_stdout), _digest(stdout), _digest(stderr),
            keymap_rc, rc,
        )
        if reference is None:
            reference = triple
        label = str(vector) if vector else "{} (no LC_ALL/LANG)"
        emit(f"{label} compile_rc={keymap_rc} km={triple[0]} out={triple[1]} "
             f"err={triple[2]} rc={triple[4]} same_as_C={'yes' if triple == reference else 'NO'}")
    emit("note: how-to-type calls setlocale(LC_ALL, \"\") but with --disable-compose "
         "the compose table is never loaded, so locale does not reach the output; "
         "compile-keymap is locale-invariant over the same seven vectors")
    emit()

    emit("== 8. work-dir and argument guards ==")
    for bad in ("/tmp/oracle-probe", "/var/tmp/oracle-probe"):
        try:
            resolve_work(bad)
            emit(f"{bad}: ACCEPTED (unexpected)")
        except WorkDirRefused as exc:
            emit(f"{bad}: refused ({exc})")
    guards = (
        ("empty keysym arg", lambda: judge(b"x", "", root / "guards")),
        ("NUL in keysym arg", lambda: judge(b"x", "a\0b", root / "guards")),
        ("unknown RMLVO key", lambda: compile_keymap({"layouts": "us"}, root / "guards")),
        ("empty RMLVO value", lambda: compile_keymap({"layout": ""}, root / "guards")),
    )
    for label, call in guards:
        try:
            call()
            emit(f"{label}: ACCEPTED (unexpected)")
        except (WorkDirRefused, ValueError, TypeError) as exc:
            emit(f"{label}: refused ({type(exc).__name__})")
    emit()

    emit("== 9. why --disable-compose is in the contracted argv ==")
    compose_dir = resolve_work(root / "compose")
    keymap_bytes = compile_keymap({"layout": "br", "options": "compose:caps"}, compose_dir)
    path = compose_dir / KEYMAP_NAME
    path.write_bytes(keymap_bytes)
    xcompose = compose_dir / "XCompose"
    xcompose.write_text('<Multi_key> <a> : "X"\n', encoding="utf-8")
    env_plain = clean_env(compose_dir)
    env_custom = dict(env_plain)
    env_custom["XCOMPOSEFILE"] = str(xcompose)
    on_plain = _run([HOW_TO_TYPE, f"--keymap={path}", "--keysym", "U0058"], env_plain, compose_dir)
    on_custom = _run([HOW_TO_TYPE, f"--keymap={path}", "--keysym", "U0058"], env_custom, compose_dir)
    off_plain = _run(judge_argv(path, "U0058"), env_plain, compose_dir)
    off_custom = _run(judge_argv(path, "U0058"), env_custom, compose_dir)
    emit("compose ON  (no --disable-compose): "
         f"plain out={_digest(on_plain[0])} custom-XCOMPOSEFILE out={_digest(on_custom[0])} "
         f"identical={'yes' if on_plain[0] == on_custom[0] else 'NO'}")
    emit("compose OFF (contracted argv):      "
         f"plain out={_digest(off_plain[0])} custom-XCOMPOSEFILE out={_digest(off_custom[0])} "
         f"identical={'yes' if off_plain[0] == off_custom[0] else 'NO'}")
    emit("note: with compose enabled XCOMPOSEFILE (and $XDG_CONFIG_HOME/XCompose, "
         "$HOME/.XCompose, XLOCALEDIR) become stdout inputs; --disable-compose removes "
         "that whole class (pinned src/compose/paths.c)")
    emit()

    emit("== 10. /usr/bin/xkbcli wrapper vs the pinned binary, and stdin ==")
    wrapper_argv = ["/usr/bin/xkbcli", "how-to-type", f"--keymap={path}",
                    "--disable-compose", "--keysym", "slash"]
    direct = _run(judge_argv(path, "slash"), env_plain, compose_dir)
    wrapped = _run(wrapper_argv, env_plain, compose_dir)
    emit(f"direct  rc={direct[2]} stdout={_digest(direct[0])} stderr={_digest(direct[1])}")
    emit(f"wrapper rc={wrapped[2]} stdout={_digest(wrapped[0])} stderr={_digest(wrapped[1])}")
    emit(f"stdout+rc+stderr identical="
         f"{'yes' if (direct[0], direct[1], direct[2]) == (wrapped[0], wrapped[1], wrapped[2]) else 'NO'}")
    piped = subprocess.run(
        judge_argv(path, "slash"), env=env_plain, cwd=str(compose_dir),
        input=b"garbage\n", stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=DEFAULT_TIMEOUT,
    )
    emit(f"stdin=garbage-pipe rc={piped.returncode} stdout={_digest(piped.stdout)} "
         f"same_as_DEVNULL={'yes' if piped.stdout == direct[0] else 'NO'}")
    emit()

    emit("== 11. work-dir path independence and the stderr caveat ==")
    left = resolve_work(root / "paths" / "left")
    right = resolve_work(root / "paths" / "right")
    left_kb = compile_keymap({"layout": "br"}, left)
    right_kb = compile_keymap({"layout": "br"}, right)
    left_run = judge(left_kb, "slash", left)
    right_run = judge(right_kb, "slash", right)
    emit(f"compile br in two work dirs: km {_digest(left_kb)} vs {_digest(right_kb)} "
         f"identical={'yes' if left_kb == right_kb else 'NO'}")
    emit(f"judge slash in two work dirs: out {_digest(left_run[0])} vs {_digest(right_run[0])} "
         f"rc {left_run[2]}/{right_run[2]} "
         f"same={'yes' if (left_run[0], left_run[2]) == (right_run[0], right_run[2]) else 'NO'}")
    # a missing keymap file puts the *path* in stderr -> stderr is not comparable
    for target in (left, right):
        keymap_file = target / KEYMAP_NAME
        if keymap_file.exists():
            keymap_file.unlink()
    missing_left = _run(judge_argv(left / KEYMAP_NAME, "Return"), clean_env(left), left)
    missing_right = _run(judge_argv(right / KEYMAP_NAME, "Return"), clean_env(right), right)
    emit(f"missing keymap file: rc {missing_left[2]}/{missing_right[2]}, "
         f"stderr identical={'yes' if missing_left[1] == missing_right[1] else 'NO'} "
         "(stderr embeds the work path -- never compare it)")
    emit()

    emit("== 12. summary ==")
    emit(f"cases={len(CASES)} reps={reps} identical={identical}/{len(CASES)}")
    emit(f"pins_ok={'yes' if not failures and pins else 'no'}")
    emit("contract channels: stdout+rc (byte-equal); stderr diagnostic only")
    emit("")

    sys.stdout.write("\n".join(out))
    return 0 if identical == len(CASES) and not failures else 1


# --------------------------------------------------------------------------
# CLI


def _parse_rmlvo_args(args) -> dict[str, str]:
    names = {}
    for key in RMLVO_KEYS:
        value = getattr(args, key)
        if value is not None:
            names[key] = value
    return names


def _emit_stream(data: bytes) -> None:
    sys.stdout.buffer.write(data)
    sys.stdout.flush()


def main(argv: list[str]) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        prog="oracle.py",
        description="C1 judge harness: pinned xkbcli compile-keymap + how-to-type",
    )
    sub = parser.add_subparsers(dest="verb", required=True)

    sub.add_parser("pins", help="hash both pinned binaries")

    for verb in ("compile", "run", "judge"):
        node = sub.add_parser(verb)
        node.add_argument("--work", required=True)
        for key, flag in RMLVO_FLAGS:
            node.add_argument(flag, dest=key, default=None)
        if verb in ("run", "judge"):
            node.add_argument("--keysym", required=True, dest="arg")
        if verb == "compile":
            node.add_argument("--out", default=None)
        if verb == "judge":
            node.add_argument("--keymap", required=True)

    check = sub.add_parser("selfcheck")
    check.add_argument("--work", required=True)
    check.add_argument("--reps", type=int, default=3)
    check.add_argument("--cost-n", type=int, default=50, dest="cost_n")

    args = parser.parse_args(argv)

    try:
        if args.verb == "pins":
            for path, digest in sorted(verify_pins(cached=False).items()):
                print(f"{digest}  {path}")
            return 0
        if args.verb == "compile":
            keymap_bytes = compile_keymap(_parse_rmlvo_args(args), args.work)
            if args.out:
                Path(args.out).write_bytes(keymap_bytes)
                print(f"{sha256_bytes(keymap_bytes)}  {args.out}")
            else:
                _emit_stream(keymap_bytes)
            return 0
        if args.verb == "judge":
            keymap_bytes = Path(args.keymap).read_bytes()
            stdout, stderr, rc = judge(keymap_bytes, args.arg, args.work)
            _emit_stream(stdout)
            sys.stderr.buffer.write(stderr)
            return rc
        if args.verb == "run":
            keymap_bytes, stdout, stderr, rc = oracle(
                _parse_rmlvo_args(args), args.arg, args.work
            )
            _emit_stream(stdout)
            sys.stderr.buffer.write(stderr)
            print(f"# km_sha256={sha256_bytes(keymap_bytes)} rc={rc}", file=sys.stderr)
            return 0
        if args.verb == "selfcheck":
            return _selfcheck(args.work, args.reps, args.cost_n)
    except (OracleError, TypeError, ValueError) as exc:
        print(f"oracle: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
