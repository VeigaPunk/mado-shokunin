#!/usr/bin/env python3
"""mado-action-plan.py — fail-closed static action-plan safety gate (mado r16 / C2).

Classifies a *declared* JSON action plan against a JSON safety policy.
This is a bounded declared-plan classifier: it inspects ``kind`` labels and
the lexical basename of ``argv[0]`` only (pure string operation; supplied
executables are never resolved, executed, or probed). The gate NEVER
executes supplied argv, NEVER evaluates shell syntax, and NEVER inspects
host state. It is not a sandbox, not arbitrary shell analysis, not a
command allowlist, and not enforcement. ``plan_safe`` means only the
absence of the finite findings below — it is NOT a statement about
credential, probe, privacy, or host safety. Wrappers, indirection, and
argv[0] values outside the finite deny list remain unclassified.

Plan schema (mado-action-plan-v1):
    {"schema": "mado-action-plan-v1",            # optional, exact if present
     "actions": [{"kind": "<string>",
                  "argv": ["<string>", ...]}, ...]}
Only ``kind`` and ``argv`` keys are allowed inside an action; unknown keys
are malformed. ``actions`` may be empty (safe plan).

Policy: the gate pins the required policy in code (PINNED_POLICY). The
supplied policy must match it exactly: ``paused`` must be the boolean
``true``, ``kinds`` must be exactly the six pinned kinds with their pinned
dispositions, and ``paused_scope``/``deny_executables`` must equal the
pinned sets. A policy that removes a denial, allows package-install (or
any mutation kind), adds a kind, or carries unknown keys is malformed.
Declared allow kinds (read-source, repo-write) additionally require a
nonempty argv whose argv[0] basename is not in ``deny_executables``.

JSON input is strict: duplicate keys, non-finite numbers (NaN/Infinity),
malformed UTF-8, unreadable paths, directories, FIFOs, devices, and other
non-regular inputs all fail closed with exit 2 and no traceback.

Verdict API (stdout, two lines):
    MADO_PLAN: <finding>
    {"schema": "mado-action-plan-verdict-v1", "finding": "<finding>",
     "exit": <int>, "action_index": <int|null>, "action_kind": <str|null>,
     "detail": "<str>"}

Exit codes / findings (vocabulary agreed with safety-cases.json):
    0  plan_safe                    every declared action allowed
    1  blocked_action_kind:<kind>   kind declared deny / denied by pause
    1  denied_executable:<basename> allowed kind, argv[0] basename denied
                                    (first basename wins; lexical only)
    1  unknown_action_kind          kind absent from policy (fail closed)
    1  empty_argv                   allowed kind, argv empty or argv[0] blank
    2  plan_malformed               plan unreadable / not regular file /
                                    not strict JSON / schema violation
    2  policy_malformed             policy unreadable / not regular file /
                                    not strict JSON / not the exact
                                    code-pinned policy
    2  snapshot_tampered            frozen input digest mismatch or unreadable
                                    input (--frozen)
    2  frozen_error                 frozen expected.json unreadable/malformed
    0  frozen_match                 --frozen inputs intact, verdict matches
    1  frozen_verdict_mismatch      --frozen inputs intact, verdict differs

Malformed plan/policy is checked before action classification; multi-action
plans report the first refusing action in declared order.

Modes:
    --plan PATH --policy PATH   evaluate one plan against one policy
                                (policy is validated before the plan)
    --frozen DIR                DIR holds plan.json, policy.json, expected.json;
                                both input digest pins are mandatory
    --selftest                  self-invocation fixtures, pinned expectations
"""

import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile

# ---------------------------------------------------------------- constants

F_PLAN_SAFE = "plan_safe"
F_BLOCKED_KIND = "blocked_action_kind"     # rendered blocked_action_kind:<k>
F_DENIED_EXEC = "denied_executable"        # rendered denied_executable:<exe>
F_UNKNOWN_KIND = "unknown_action_kind"
F_EMPTY_ARGV = "empty_argv"
F_PLAN_MALFORMED = "plan_malformed"
F_POLICY_MALFORMED = "policy_malformed"
F_SNAPSHOT_TAMPERED = "snapshot_tampered"
F_FROZEN_ERROR = "frozen_error"
F_FROZEN_MATCH = "frozen_match"
F_FROZEN_MISMATCH = "frozen_verdict_mismatch"

EXIT_OK, EXIT_DENY, EXIT_ERROR = 0, 1, 2

PLAN_SCHEMA = "mado-action-plan-v1"
POLICY_SCHEMA = "mado-action-plan-policy-v1"
VERDICT_SCHEMA = "mado-action-plan-verdict-v1"
FROZEN_SCHEMA = "mado-action-plan-frozen-v1"

# Exact code-pinned policy. A supplied policy must match this semantically:
# denials cannot be removed, allow kinds cannot be added, and mutation kinds
# (including package-install) can never become allowed.
PINNED_PAUSED_SCOPE = frozenset({
    "package-install",
    "service-mutate",
    "compositor-mutate",
    "input-capture",
})
PINNED_DENY_EXECUTABLES = frozenset({
    "pacman", "yay", "paru", "systemctl", "hyprctl", "omarchy",
    "libinput", "evtest", "sudo", "sh", "bash", "env",
})
PINNED_KINDS = {
    "read-source": {"disposition": "allow", "argv_nonempty": True},
    "repo-write": {"disposition": "allow", "argv_nonempty": True},
    "package-install": {"disposition": "deny", "argv_nonempty": False},
    "service-mutate": {"disposition": "deny", "argv_nonempty": False},
    "compositor-mutate": {"disposition": "deny", "argv_nonempty": False},
    "input-capture": {"disposition": "deny", "argv_nonempty": False},
}

_PLAN_KEYS = frozenset({"schema", "actions"})
_ACTION_KEYS = frozenset({"kind", "argv"})
_POLICY_KEYS = frozenset(
    {"schema", "paused", "paused_scope", "deny_executables", "kinds"})
_KIND_RULE_KEYS = frozenset({"disposition", "argv_nonempty"})
_EXPECTED_KEYS = frozenset(
    {"schema", "plan_sha256", "policy_sha256",
     "expected_finding", "expected_exit"})


# ----------------------------------------------------------------- verdicts

def _emit(finding, code, action_index=None, action_kind=None, detail=""):
    verdict = {
        "schema": VERDICT_SCHEMA,
        "finding": finding,
        "exit": code,
        "action_index": action_index,
        "action_kind": action_kind,
        "detail": detail,
    }
    print(f"MADO_PLAN: {finding}")
    print(json.dumps(verdict, sort_keys=True))
    return code


# ------------------------------------------------------------------- inputs

def _read_regular(path):
    """Read a regular file only, once. Symlinks (O_NOFOLLOW), FIFOs,
    devices, dirs, sockets and other non-regular inputs are rejected;
    O_NOCTTY prevents terminal capture. The fd is fstat'd and the read is
    bounded: growth past the stat size is an error, not silent truncation.
    Returns (bytes, error)."""
    flags = (os.O_RDONLY | os.O_NONBLOCK | os.O_NOCTTY
             | getattr(os, "O_NOFOLLOW", 0))
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        return None, f"unreadable: {exc.strerror or exc}"
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            return None, "not a regular file"
        if st.st_size > 16 * 1024 * 1024:
            return None, "input exceeds 16 MiB bound"
        chunks = []
        total = 0
        while True:
            try:
                chunk = os.read(fd, 1 << 20)
            except BlockingIOError:
                continue
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > st.st_size:
                return None, "file grew during bounded read"
        return b"".join(chunks), None
    except OSError as exc:
        return None, f"unreadable: {exc.strerror or exc}"
    finally:
        os.close(fd)


def _strict_pairs(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError(f"duplicate key {key!r}")
        obj[key] = value
    return obj


def _reject_constant(name):
    raise ValueError(f"non-finite constant {name!r}")


def _parse_json_bytes(raw):
    """Strict JSON parse of bytes already read. Returns (obj, error)."""
    try:
        text = raw.decode("utf-8")
        obj = json.loads(
            text,
            object_pairs_hook=_strict_pairs,
            parse_constant=_reject_constant,
        )
    except Exception as exc:  # malformed bytes are data, never a traceback
        return None, f"invalid JSON: {exc}"
    return obj, None


def _load_json(path):
    """Read + strict-parse a regular file. Returns (obj, error)."""
    raw, err = _read_regular(path)
    if err:
        return None, err
    return _parse_json_bytes(raw)


def _sha256(path):
    raw, err = _read_regular(path)
    if err:
        return None, err
    return hashlib.sha256(raw).hexdigest(), None


def _is_str_list(value):
    return isinstance(value, list) and all(isinstance(v, str) for v in value)


# ------------------------------------------------------------ policy checks

def _validate_policy(policy):
    """Return (normalized, error). Only the exact pinned policy is valid."""
    if not isinstance(policy, dict):
        return None, "policy is not a JSON object"
    unknown = set(policy) - _POLICY_KEYS
    if unknown:
        return None, f"policy has unknown keys: {sorted(unknown)}"
    if "schema" in policy and policy["schema"] != POLICY_SCHEMA:
        return None, f"policy.schema must be {POLICY_SCHEMA!r}"
    paused = policy.get("paused")
    if not (type(paused) is bool and paused is True):
        return None, "policy.paused must be exactly the boolean true"
    paused_scope = policy.get("paused_scope")
    if not _is_str_list(paused_scope):
        return None, "policy.paused_scope must be a list of strings"
    if len(set(paused_scope)) != len(paused_scope):
        return None, "policy.paused_scope contains duplicates"
    if set(paused_scope) != PINNED_PAUSED_SCOPE:
        return None, "policy.paused_scope must equal the pinned mutation kinds"
    deny_executables = policy.get("deny_executables")
    if not _is_str_list(deny_executables):
        return None, "policy.deny_executables must be a list of strings"
    if len(set(deny_executables)) != len(deny_executables):
        return None, "policy.deny_executables contains duplicates"
    if set(deny_executables) != PINNED_DENY_EXECUTABLES:
        return None, ("policy.deny_executables must equal the pinned "
                      "executable deny list")
    kinds = policy.get("kinds")
    if not isinstance(kinds, dict):
        return None, "policy.kinds must be an object"
    if set(kinds) != set(PINNED_KINDS):
        return None, ("policy.kinds must be exactly the pinned kinds "
                      "(cannot remove denials or add kinds)")
    normalized_kinds = {}
    for name, pinned_rule in PINNED_KINDS.items():
        rule = kinds[name]
        if not isinstance(rule, dict):
            return None, f"kinds[{name}] must be an object"
        unknown = set(rule) - _KIND_RULE_KEYS
        if unknown:
            return None, f"kinds[{name}] has unknown keys: {sorted(unknown)}"
        disposition = rule.get("disposition")
        if disposition != pinned_rule["disposition"]:
            return None, (f"kinds[{name}].disposition must be "
                          f"{pinned_rule['disposition']!r}")
        argv_nonempty = rule.get("argv_nonempty", False)
        if not isinstance(argv_nonempty, bool):
            return None, f"kinds[{name}].argv_nonempty must be a boolean"
        if argv_nonempty != pinned_rule["argv_nonempty"]:
            return None, (f"kinds[{name}].argv_nonempty must be "
                          f"{pinned_rule['argv_nonempty']}")
        normalized_kinds[name] = dict(pinned_rule)
    return {
        "paused": True,
        "paused_scope": PINNED_PAUSED_SCOPE,
        "deny_executables": PINNED_DENY_EXECUTABLES,
        "kinds": normalized_kinds,
    }, None


def _validate_plan(plan):
    """Return (actions, error). Whole-plan schema check, fail closed."""
    if not isinstance(plan, dict):
        return None, "plan is not a JSON object"
    unknown = set(plan) - _PLAN_KEYS
    if unknown:
        return None, f"plan has unknown keys: {sorted(unknown)}"
    if "schema" in plan and plan["schema"] != PLAN_SCHEMA:
        return None, f"plan.schema must be {PLAN_SCHEMA!r}"
    actions = plan.get("actions")
    if not isinstance(actions, list):
        return None, "plan.actions must be a list"
    for i, action in enumerate(actions):
        if not isinstance(action, dict):
            return None, f"actions[{i}] is not an object"
        unknown = set(action) - _ACTION_KEYS
        if unknown:
            return None, f"actions[{i}] has unknown keys: {sorted(unknown)}"
        kind = action.get("kind")
        if not isinstance(kind, str):
            return None, f"actions[{i}].kind must be a string"
        argv = action.get("argv")
        if not _is_str_list(argv):
            return None, f"actions[{i}].argv must be a list of strings"
    return actions, None


def _basename(arg0):
    """Pure-string basename; never resolves or touches the filesystem."""
    stripped = arg0.strip()
    if not stripped:
        return ""
    return stripped.rstrip("/").rsplit("/", 1)[-1]


def _classify(actions, policy):
    """Return (finding, code, action_index, action_kind, detail)."""
    paused = policy["paused"]
    paused_scope = policy["paused_scope"]
    deny_exec = policy["deny_executables"]
    kinds = policy["kinds"]
    for i, action in enumerate(actions):
        kind = action["kind"]
        argv = action["argv"]
        rule = kinds.get(kind)
        if rule is None:
            return (F_UNKNOWN_KIND, EXIT_DENY, i, kind,
                    f"actions[{i}] kind {kind!r} not in policy")
        if paused and kind in paused_scope:
            return (f"{F_BLOCKED_KIND}:{kind}", EXIT_DENY, i, kind,
                    f"actions[{i}] kind {kind!r} denied by paused policy")
        if rule["disposition"] != "allow":
            return (f"{F_BLOCKED_KIND}:{kind}", EXIT_DENY, i, kind,
                    f"actions[{i}] kind {kind!r} disposition deny")
        if rule["argv_nonempty"] and not argv:
            return (F_EMPTY_ARGV, EXIT_DENY, i, kind,
                    f"actions[{i}] argv must be nonempty")
        exe = _basename(argv[0]) if argv else ""
        if not exe:
            return (F_EMPTY_ARGV, EXIT_DENY, i, kind,
                    f"actions[{i}] argv[0] is empty")

        if exe in deny_exec:
            return (f"{F_DENIED_EXEC}:{exe}", EXIT_DENY, i, kind,
                    f"actions[{i}] executable {exe!r} denied for {kind!r}")
    return (F_PLAN_SAFE, EXIT_OK, None, None,
            "passed finite kind/argv[0] screen; not permission or safety")


# -------------------------------------------------------------------- modes

def _evaluate_raw(plan_raw, policy_raw):
    """Classify bytes already read; returns
    (finding, code, index, kind, detail). Policy first, then plan."""
    policy, err = _parse_json_bytes(policy_raw)
    if err:
        return (F_POLICY_MALFORMED, EXIT_ERROR, None, None,
                f"policy: {err}")
    policy, err = _validate_policy(policy)
    if err:
        return (F_POLICY_MALFORMED, EXIT_ERROR, None, None,
                f"policy: {err}")
    plan, err = _parse_json_bytes(plan_raw)
    if err:
        return (F_PLAN_MALFORMED, EXIT_ERROR, None, None,
                f"plan: {err}")
    actions, err = _validate_plan(plan)
    if err:
        return (F_PLAN_MALFORMED, EXIT_ERROR, None, None,
                f"plan: {err}")
    return _classify(actions, policy)


def _evaluate(plan_path, policy_path):
    """Read each file once and classify those exact bytes."""
    policy_raw, err = _read_regular(policy_path)
    if err:
        return (F_POLICY_MALFORMED, EXIT_ERROR, None, None,
                f"policy {policy_path}: {err}")
    plan_raw, err = _read_regular(plan_path)
    if err:
        return (F_PLAN_MALFORMED, EXIT_ERROR, None, None,
                f"plan {plan_path}: {err}")
    return _evaluate_raw(plan_raw, policy_raw)


def run_evaluate(plan_path, policy_path):
    finding, code, idx, kind, detail = _evaluate(plan_path, policy_path)
    return _emit(finding, code, idx, kind, detail)


def run_frozen(root):
    """Verify both pinned input digests, then replay and compare verdict."""
    root = os.path.abspath(root)
    expected_path = os.path.join(root, "expected.json")
    plan_path = os.path.join(root, "plan.json")
    policy_path = os.path.join(root, "policy.json")
    expected, err = _load_json(expected_path)
    if err:
        return _emit(F_FROZEN_ERROR, EXIT_ERROR,
                     detail=f"expected.json: {err}")
    if not isinstance(expected, dict):
        return _emit(F_FROZEN_ERROR, EXIT_ERROR,
                     detail="expected.json is not a JSON object")
    unknown = set(expected) - _EXPECTED_KEYS
    if unknown:
        return _emit(F_FROZEN_ERROR, EXIT_ERROR,
                     detail=f"expected.json unknown keys: {sorted(unknown)}")
    if "schema" in expected and expected["schema"] != FROZEN_SCHEMA:
        return _emit(F_FROZEN_ERROR, EXIT_ERROR,
                     detail=f"expected.json schema must be {FROZEN_SCHEMA!r}")
    for key in ("plan_sha256", "policy_sha256",
                "expected_finding", "expected_exit"):
        if key not in expected:
            return _emit(F_FROZEN_ERROR, EXIT_ERROR,
                         detail=f"expected.json missing mandatory key {key}")
    plan_pin = expected["plan_sha256"]
    policy_pin = expected["policy_sha256"]
    want_finding = expected["expected_finding"]
    want_exit = expected["expected_exit"]
    for key, pin in (("plan_sha256", plan_pin),
                     ("policy_sha256", policy_pin)):
        if not (isinstance(pin, str) and len(pin) == 64
                and all(c in "0123456789abcdefABCDEF" for c in pin)):
            return _emit(F_FROZEN_ERROR, EXIT_ERROR,
                         detail=f"expected.json {key} must be 64 hex chars")
    if not (isinstance(want_finding, str)
            and type(want_exit) is int):
        return _emit(F_FROZEN_ERROR, EXIT_ERROR,
                     detail="expected.json field types invalid")
    # The expected pair must be a reachable evaluate-mode verdict.
    valid_pairs = {
        (0, "plan_safe"), (1, "unknown_action_kind"), (1, "empty_argv"),
        (2, "plan_malformed"), (2, "policy_malformed"),
    }
    valid_pairs.update(
        (1, "blocked_action_kind:" + kind) for kind in PINNED_PAUSED_SCOPE)
    valid_pairs.update(
        (1, "denied_executable:" + name) for name in PINNED_DENY_EXECUTABLES)
    ok_pair = (want_exit, want_finding) in valid_pairs
    if not ok_pair:
        return _emit(F_FROZEN_ERROR, EXIT_ERROR,
                     detail=f"expected.json pair "
                            f"{want_exit}/{want_finding!r} is unreachable")
    inputs = {}
    for label, path, pin in (("plan.json", plan_path, plan_pin),
                             ("policy.json", policy_path, policy_pin)):
        raw, rerr = _read_regular(path)
        if rerr:
            return _emit(F_SNAPSHOT_TAMPERED, EXIT_ERROR,
                         detail=f"{label} unreadable: {rerr}")
        digest = hashlib.sha256(raw).hexdigest()
        if digest.lower() != pin.lower():
            return _emit(F_SNAPSHOT_TAMPERED, EXIT_ERROR,
                         detail=f"{label} sha256 {digest} != pinned {pin}")
        inputs[label] = raw
    # Both input digests verified; classify the SAME bytes that were hashed
    # (single read per file — no re-open, no TOCTOU window).
    got_finding, got_code, _, _, _ = _evaluate_raw(
        inputs["plan.json"], inputs["policy.json"])
    if got_finding == want_finding and got_code == want_exit:
        return _emit(F_FROZEN_MATCH, EXIT_OK,
                     detail=f"frozen verdict {want_finding}/{want_exit} matched")
    return _emit(F_FROZEN_MISMATCH, EXIT_DENY,
                 detail=(f"frozen expected {want_finding}/{want_exit} "
                         f"but got {got_finding}/{got_code}"))


def _parse_verdict(stdout):
    """Return the verdict JSON object from gate stdout, or None."""
    for line in stdout.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                obj = json.loads(line)
            except ValueError:
                continue
            if isinstance(obj, dict) and "finding" in obj:
                return obj
    return None


def _parse_finding(stdout):
    verdict = _parse_verdict(stdout)
    return verdict.get("finding") if verdict else None


# ------------------------------------------------------------------ selftest

def _canonical_policy():
    return {
        "schema": POLICY_SCHEMA,
        "paused": True,
        "paused_scope": sorted(PINNED_PAUSED_SCOPE),
        "deny_executables": sorted(PINNED_DENY_EXECUTABLES),
        "kinds": {
            "read-source": {"disposition": "allow", "argv_nonempty": True},
            "repo-write": {"disposition": "allow", "argv_nonempty": True},
            "package-install": {"disposition": "deny"},
            "service-mutate": {"disposition": "deny"},
            "compositor-mutate": {"disposition": "deny"},
            "input-capture": {"disposition": "deny"},
        },
    }


def _self_invoke(script, *args, cwd):
    """Isolated self-invocation: -I, shell=False, DEVNULL stdin, bounded
    timeout, temp cwd, minimal env (only what the interpreter needs)."""
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin")}
    return subprocess.run(
        [sys.executable, "-I", script, *args],
        shell=False, stdin=subprocess.DEVNULL,
        capture_output=True, text=True, timeout=60, cwd=cwd, env=env)


def run_selftest():
    """Self-invocation fixtures. Each case pins literal expected constants."""
    script = os.path.realpath(__file__)
    base_policy = _canonical_policy()

    def plan(*actions):
        return {"schema": PLAN_SCHEMA, "actions": list(actions)}

    def action(kind, argv):
        return {"kind": kind, "argv": argv}

    def policy_with(**mutations):
        p = _canonical_policy()
        p.update(mutations)
        return p

    # (name, plan_obj_or_raw_bytes, policy_obj_or_raw_bytes_or_"__DIR__",
    #  expected_exit, expected_finding)
    cases = [
        ("safe-read-repo",
         plan(action("read-source", ["cat", "corpus/SOURCES.md"]),
              action("repo-write", ["edit", "SKILL.md"])),
         base_policy, 0, "plan_safe"),
        ("empty-actions",
         plan(), base_policy, 0, "plan_safe"),
        ("unlisted-argv0-unscreened",
         plan(action("read-source", ["python3", "-c", "print(1)"])),
         base_policy, 0, "plan_safe"),
        ("omarchy-prefix-unscreened",
         plan(action("read-source", ["omarchy-pkg-add", "libinput"])),
         base_policy, 0, "plan_safe"),
        ("package-install-libinput",
         plan(action("package-install",
                     ["sudo", "pacman", "-S", "--needed", "--noconfirm",
                      "libinput", "libinput-tools"])),
         base_policy, 1, "blocked_action_kind:package-install"),
        ("service-mutate",
         plan(action("service-mutate", ["systemctl", "restart", "x"])),
         base_policy, 1, "blocked_action_kind:service-mutate"),
        ("compositor-mutate",
         plan(action("compositor-mutate", ["hyprctl", "reload"])),
         base_policy, 1, "blocked_action_kind:compositor-mutate"),
        ("input-capture",
         plan(action("input-capture", ["evtest"])),
         base_policy, 1, "blocked_action_kind:input-capture"),
        ("unknown-kind",
         plan(action("net-fetch", ["curl", "https://x"])),
         base_policy, 1, "unknown_action_kind"),
        ("first-refusal-wins",
         plan(action("read-source", ["cat", "x"]),
              action("service-mutate", ["systemctl", "restart", "x"]),
              action("package-install", ["pacman", "-S", "y"])),
         base_policy, 1, "blocked_action_kind:service-mutate", 1),
        ("read-disguised-pacman",
         plan(action("read-source", ["/usr/bin/pacman", "-Sp", "libinput"])),
         base_policy, 1, "denied_executable:pacman"),
        ("read-sudo",
         plan(action("read-source", ["sudo", "cat", "corpus/SOURCES.md"])),
         base_policy, 1, "denied_executable:sudo"),
        ("read-shell",
         plan(action("read-source", ["bash", "-c", "cat x"])),
         base_policy, 1, "denied_executable:bash"),
        ("repo-env-wrapper",
         plan(action("repo-write", ["env", "X=1", "edit", "f"])),
         base_policy, 1, "denied_executable:env"),
        ("read-empty-argv",
         plan(action("read-source", [])),
         base_policy, 1, "empty_argv"),
        ("read-blank-argv0",
         plan(action("read-source", ["  ", "x"])),
         base_policy, 1, "empty_argv"),
        ("plan-not-object",
         b'["not","an","object"]', base_policy, 2, "plan_malformed"),
        ("plan-missing-argv",
         plan({"kind": "read-source"}),
         base_policy, 2, "plan_malformed"),
        ("plan-nonstring-argv",
         plan({"kind": "read-source", "argv": ["cat", 7]}),
         base_policy, 2, "plan_malformed"),
        ("plan-action-unknown-key",
         plan({"kind": "read-source", "argv": ["cat", "x"], "note": "y"}),
         base_policy, 2, "plan_malformed"),
        ("plan-duplicate-key",
         b'{"actions": [], "actions": []}',
         base_policy, 2, "plan_malformed"),
        ("plan-nonfinite",
         b'{"actions": [{"kind": "read-source", "argv": [NaN]}]}',
         base_policy, 2, "plan_malformed"),
        ("plan-bad-utf8",
         b'\xff\xfe{"actions":[]}',
         base_policy, 2, "plan_malformed"),
        ("plan-is-directory",
         "__DIR__", base_policy, 2, "plan_malformed"),
        ("policy-not-object",
         plan(action("read-source", ["cat", "x"])),
         b'["bad"]', 2, "policy_malformed"),
        ("policy-missing-paused",
         plan(action("read-source", ["cat", "x"])),
         {"kinds": base_policy["kinds"],
          "paused_scope": sorted(PINNED_PAUSED_SCOPE),
          "deny_executables": sorted(PINNED_DENY_EXECUTABLES)},
         2, "policy_malformed"),
        ("policy-paused-false",
         plan(action("read-source", ["cat", "x"])),
         policy_with(paused=False), 2, "policy_malformed"),
        ("policy-paused-string",
         plan(action("read-source", ["cat", "x"])),
         policy_with(paused="true"), 2, "policy_malformed"),
        ("policy-allows-package-install",
         plan(action("package-install", ["pacman", "-Sp", "x"])),
         policy_with(kinds={
             **{k: dict(v) for k, v in PINNED_KINDS.items()},
             "package-install": {"disposition": "allow"},
         }), 2, "policy_malformed"),
        ("policy-removes-denial-kind",
         plan(action("read-source", ["cat", "x"])),
         policy_with(kinds={
             k: dict(v) for k, v in PINNED_KINDS.items()
             if k != "input-capture"
         }), 2, "policy_malformed"),
        ("policy-adds-allow-kind",
         plan(action("read-source", ["cat", "x"])),
         policy_with(kinds={
             **{k: dict(v) for k, v in PINNED_KINDS.items()},
             "net-fetch": {"disposition": "allow"},
         }), 2, "policy_malformed"),
        ("policy-unknown-key",
         plan(action("read-source", ["cat", "x"])),
         policy_with(notes=["unexpected"]), 2, "policy_malformed"),
        ("policy-shrunk-deny-exec",
         plan(action("read-source", ["sudo", "cat", "x"])),
         policy_with(deny_executables=sorted(
             PINNED_DENY_EXECUTABLES - {"sudo"})), 2, "policy_malformed"),
        ("policy-shrunk-paused-scope",
         plan(action("read-source", ["cat", "x"])),
         policy_with(paused_scope=["package-install"]),
         2, "policy_malformed"),
        ("policy-before-plan",
         b'\xff\xfe{"actions":[]}',  # malformed plan
         b'["bad"]',                  # malformed policy wins
         2, "policy_malformed"),
        ("policy-paused-one",
         plan(action("read-source", ["cat", "x"])),
         policy_with(paused=1), 2, "policy_malformed"),
        ("policy-paused-null",
         plan(action("read-source", ["cat", "x"])),
         policy_with(paused=None), 2, "policy_malformed"),
        ("blocked-kind-empty-argv",
         plan(action("package-install", [])),
         base_policy, 1, "blocked_action_kind:package-install", 0),
        ("unknown-kind-empty-argv",
         plan(action("net-fetch", [])),
         base_policy, 1, "unknown_action_kind", 0),
        ("denied-before-blocked-order",
         plan(action("read-source", ["sudo", "cat", "x"]),
              action("package-install", ["pacman", "-S", "y"])),
         base_policy, 1, "denied_executable:sudo", 0),

        ("plan-is-symlink",
         "__SYMLINK__", base_policy, 2, "plan_malformed"),
        ("plan-is-fifo",
         "__FIFO__", base_policy, 2, "plan_malformed"),
        ("malformed-later-beats-denied",
         {"schema": PLAN_SCHEMA, "actions": [
             {"kind": "package-install", "argv": ["pacman", "-S", "x"]},
             {"kind": "read-source"}]},
         base_policy, 2, "plan_malformed"),
    ]

    passed, failed = 0, []
    with tempfile.TemporaryDirectory(prefix="mado-plan-selftest-") as tmp:
        # Snapshot own code bytes once into the private tmp dir and invoke
        # that copy, so a concurrent mid-run edit can't drift the script
        # under the subprocesses.
        script_raw, serr = _read_regular(script)
        if serr:
            print(f"SELFTEST_ERROR cannot read own script: {serr}")
            return 1
        script_copy = os.path.join(tmp, "mado-action-plan-selftest.py")
        with open(script_copy, "wb") as fh:
            fh.write(script_raw)
        print("SELFTEST_SCRIPT_SHA256: "
              f"{hashlib.sha256(script_raw).hexdigest()}")
        # Target for the symlink fixture (a harmless valid plan).
        link_target = os.path.join(tmp, "link-target.json")
        with open(link_target, "w", encoding="utf-8") as fh:
            json.dump(plan(), fh)
        for entry in cases:
            name, plan_obj, policy_obj, want_code, want_finding = entry[:5]
            want_index = entry[5] if len(entry) > 5 else "__NA__"
            plan_path = os.path.join(tmp, f"{name}.plan.json")
            policy_path = os.path.join(tmp, f"{name}.policy.json")
            for path, obj in ((plan_path, plan_obj),
                              (policy_path, policy_obj)):
                if obj in ("__DIR__", "__SYMLINK__", "__FIFO__"):
                    continue  # special path kinds resolved below
                if isinstance(obj, bytes):
                    with open(path, "wb") as fh:
                        fh.write(obj)
                else:
                    with open(path, "w", encoding="utf-8") as fh:
                        json.dump(obj, fh)
            if plan_obj == "__DIR__":
                plan_path = tmp  # directory input must exit 2, no traceback
            elif plan_obj == "__SYMLINK__":
                os.symlink(link_target, plan_path)  # O_NOFOLLOW must reject
            elif plan_obj == "__FIFO__":
                os.mkfifo(plan_path)  # non-regular must reject, no blocking

            proc = _self_invoke(script_copy, "--plan", plan_path,
                                "--policy", policy_path, cwd=tmp)
            verdict = _parse_verdict(proc.stdout)
            got_finding = verdict.get("finding") if verdict else None
            ok = (proc.returncode == want_code
                  and got_finding == want_finding
                  and (want_index == "__NA__" or verdict is not None
                       and verdict.get("action_index") == want_index)
                  and "Traceback" not in proc.stderr)
            status = "PASS" if ok else "FAIL"
            print(f"SELFTEST {status} {name}: want {want_code}/{want_finding} "
                  f"got {proc.returncode}/{got_finding}")
            if ok:
                passed += 1
            else:
                failed.append(name)

        # --- frozen-mode fixtures (also self-invocation) -----------------
        def write_frozen(name, plan_obj, policy_obj, expect_finding,
                         expect_code, tamper_plan=False, tamper_policy=False,
                         drop_pin=None, mutate=None):
            d = os.path.join(tmp, f"frozen-{name}")
            os.makedirs(d)
            plan_b = json.dumps(plan_obj, sort_keys=True).encode("utf-8")
            policy_b = json.dumps(policy_obj, sort_keys=True).encode("utf-8")
            expected = {
                "schema": FROZEN_SCHEMA,
                "plan_sha256": hashlib.sha256(plan_b).hexdigest(),
                "policy_sha256": hashlib.sha256(policy_b).hexdigest(),
                "expected_finding": expect_finding,
                "expected_exit": expect_code,
            }
            if drop_pin:
                expected.pop(drop_pin)
            if mutate:
                mutate(expected)
            if tamper_plan:
                plan_b = plan_b + b"\n#tampered\n"
            if tamper_policy:
                policy_b = policy_b + b"\n#tampered\n"
            with open(os.path.join(d, "plan.json"), "wb") as fh:
                fh.write(plan_b)
            with open(os.path.join(d, "policy.json"), "wb") as fh:
                fh.write(policy_b)
            with open(os.path.join(d, "expected.json"), "w",
                      encoding="utf-8") as fh:
                json.dump(expected, fh)
            return d

        frozen_cases = [
            ("frozen-match",
             write_frozen("match",
                          plan(action("read-source", ["cat", "f"])),
                          base_policy, "plan_safe", 0),
             0, "frozen_match"),
            ("frozen-denied-match",
             write_frozen("denied",
                          plan(action("package-install",
                                      ["pacman", "-S", "libinput"])),
                          base_policy, "blocked_action_kind:package-install",
                          1),
             0, "frozen_match"),
            ("frozen-tampered-plan",
             write_frozen("tampered",
                          plan(action("read-source", ["cat", "f"])),
                          base_policy, "plan_safe", 0, tamper_plan=True),
             2, "snapshot_tampered"),
            ("frozen-missing-pin",
             write_frozen("missing-pin",
                          plan(action("read-source", ["cat", "f"])),
                          base_policy, "plan_safe", 0,
                          drop_pin="policy_sha256"),
             2, "frozen_error"),
            ("frozen-verdict-mismatch",
             write_frozen("mismatch",
                          plan(action("package-install",
                                      ["pacman", "-S", "libinput"])),
                          base_policy, "plan_safe", 0),
             1, "frozen_verdict_mismatch"),
            ("frozen-tampered-policy",
             write_frozen("tampered-policy",
                          plan(action("read-source", ["cat", "f"])),
                          base_policy, "plan_safe", 0, tamper_policy=True),
             2, "snapshot_tampered"),
            ("frozen-invalid-pair",
             write_frozen("invalid-pair",
                          plan(action("read-source", ["cat", "f"])),
                          base_policy, "plan_safe", 7),
             2, "frozen_error"),
            ("frozen-empty-finding",
             write_frozen("empty-finding",
                          plan(action("read-source", ["cat", "f"])),
                          base_policy, "", 0),
             2, "frozen_error"),
            ("frozen-nonhex-pin",
             write_frozen("nonhex",
                          plan(action("read-source", ["cat", "f"])),
                          base_policy, "plan_safe", 0,
                          mutate=lambda e: e.update(plan_sha256="zz" * 32)),
             2, "frozen_error"),
        ]


        for name, d, want_code, want_finding in frozen_cases:
            proc = _self_invoke(script_copy, "--frozen", d, cwd=tmp)
            got_finding = _parse_finding(proc.stdout)
            ok = (proc.returncode == want_code
                  and got_finding == want_finding
                  and "Traceback" not in proc.stderr)
            status = "PASS" if ok else "FAIL"
            print(f"SELFTEST {status} {name}: want {want_code}/{want_finding} "
                  f"got {proc.returncode}/{got_finding}")
            if ok:
                passed += 1
            else:
                failed.append(name)

    total = len(cases) + len(frozen_cases)
    print(f"SELFTEST_SUMMARY: {passed}/{total} passed"
          + (f" failed={failed}" if failed else ""))
    return 0 if not failed else 1


# --------------------------------------------------------------------- main

def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="mado-action-plan.py",
        description="Fail-closed static declared-action-plan safety gate.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--plan", metavar="PATH",
                       help="action plan JSON (requires --policy)")
    group.add_argument("--frozen", metavar="DIR",
                       help="frozen snapshot dir with expected.json")
    group.add_argument("--selftest", action="store_true",
                       help="run self-invocation fixture assertions")
    parser.add_argument("--policy", metavar="PATH",
                        help="safety policy JSON (required with --plan)")
    args = parser.parse_args(argv)
    try:
        if args.selftest:
            if args.policy is not None:
                parser.error("--policy is not valid with --selftest")
            return run_selftest()
        if args.frozen is not None:
            if args.policy is not None:
                parser.error("--policy is not valid with --frozen")
            if not args.frozen:
                parser.error("--frozen requires a directory path")
            return run_frozen(args.frozen)
        if not args.policy:
            parser.error("--plan requires --policy")
        return run_evaluate(args.plan, args.policy)
    except Exception as exc:
        # Fail closed: any unexpected internal error becomes exit 2,
        # never an exit-1 traceback.
        mode = ("selftest" if args.selftest
                else "frozen" if args.frozen else "evaluate")
        finding = F_FROZEN_ERROR if args.frozen else F_PLAN_MALFORMED
        return _emit(finding, EXIT_ERROR,
                     detail=f"unexpected internal {mode} error: "
                            f"{type(exc).__name__}: {exc}")


if __name__ == "__main__":
    sys.exit(main())
