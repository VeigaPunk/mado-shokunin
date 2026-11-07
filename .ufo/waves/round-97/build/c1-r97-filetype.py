#!/usr/bin/env python3
"""Round-97 C1 counter - the PATH surface: what GIO 2.90.1 GLocalFileInfo.get_content_type
(glocalfileinfo.c:1300-1389) reports as standard::content-type / standard::fast-content-type
for a local path, as the installed `gio info` CLI answers it.

Frozen predicate PRED-C1-r97-v1 (verbatim from the declaration; the same sentence is the receipt label):
  TARGET_MET iff, at --rev, tools/mado-filetype.py is the frozen candidate (tool_sha256 ==
  --expect-tool-sha256, printed tool_pin=ok) and, run under an empty PATH through the audit launcher with
  the structural allowlist (no process, socket, network or non-libc dynamic import; the three sibling lane
  modules loaded by pinned path and allowed attributes only), it answers (i) every frozen case exactly
  (correct == cases) over the declared classes dir chr blk fifo sock zero empty sym brok nofollow follow
  certain uncertain fast readerr (15 classes, >=8 cases each) and classes == 15/15; (ii) every frozen mutant
  is killed and every class kills at least one mutant (killed == mutants, class_kills == 15/15); (iii) every
  fresh seeded case exactly (fresh == fresh_total, >=120, fixtures generated at measurement time by a frozen
  generator, labels from the same oracle); (iv) every file of the frozen host list exactly (host ==
  host_total, >=1500 paths over the host's own database and its special files); (v) the oracle is the
  installed gio (--expect-gio-sha256, and every frozen label was produced by this binary at the freeze);
  (vi) the controls stay behind: the do-nothing instrument (r94's name-only answer for every case) scores
  fewer than the total, a naive extension-table model fewer, the memoriser 0 on the fresh leg, and a
  library-asking forgery is rejected (audit_denials > 0); and (vii) the candidate's --selftest is green
  (checks=N failed=0, N >= 20).  rc 0 TARGET_MET, 1 TARGET_MISSED, 2 SETUP_ERROR.

Counter note on the structural clause (kept with the receipt): the candidate's --selftest must build an
AF_UNIX fixture to exercise the inode/socket stat branch, so `socket` is in the declared import allowlist
and the audit hook admits socket.__new__ for AF_UNIX only; connect/listen and every network family stay
audit-denied, and the import is declared, not silent.  No process spawn, no network, no non-libc dlopen.

Inputs (all sha256-pinned by --expect-*-sha256; SETUP_ERROR on any mismatch):
  --cases    {"version":1,"oracle":"gio info -a standard::content-type (and standard::fast-content-type)",
             "gio_sha256":<pin>,"glib2":"2.90.1-1","classes":[the 15 names in order],"cases":[...]}
             case: {"id","class","env":{"HOME":"{root}/h","XDG_DATA_HOME":"{root}/dh"|null,
                    "XDG_DATA_DIRS":"{root}/d1:{root}/d2"},"files":{rel:b64},
                    "mode":"follow|nofollow","attr":"full|fast",
                    "paths":[{"path":rel-or-abs,"type":"file|dir|fifo|sock|symlink|chardev|blkdev|
                              unreadable","target":symlink target}],"labels":[["<type>"]|["ERROR"],...]}
             files keys ending "/" are directories; ".." and absolute members are rejected; chardev/blkdev
             entries are absolute host paths (declared, never created); symlink targets may carry a
             "{root}" prefix substituted with the case root; an unreadable path is the declared file with
             mode 0.  Every label was produced by /usr/bin/gio at the freeze (ERROR only when gio exits
             nonzero and prints no attribute).  XDG_DATA_DIRS null is forbidden; HOME is exactly
             "{root}/h".  Per case at least one reachable mime/ tree must be declared in files OR the env
             points only at empty dirs (a none-database case).  1..12 paths per case, one label per path
             in order.  The scored answer for an ERROR-labelled path is the candidate's
             `MADO_FILETYPE: ERROR stat path=...` line plus overall exit 2 (the other paths are still
             answered - no path is lost).  Unstatable paths are otherwise outside the surface: no fresh
             case may carry an ERROR label (declaration rule 7).
  --mutants  {"version":1,"tool":"tools/mado-filetype.py","mutants":[{"id","class","find","replace"}]}
             find occurs exactly once in the pinned candidate bytes and is unique across mutants; id
             starts "<class>-"; class in the 15.  No equivalent/not_observable representation: a frozen
             non-killer fails the wave (killed == mutants).  A kill is a parsed wrong answer or a missing
             line over the frozen cases; a crashing mutant is NOT a kill (crashed_not_killed).
  --genseed  the frozen fresh-case generator; called inside the counter at measurement time as
             `python3 -I <genseed> --seed HEX --dir D --out F --count 140` (its PATH starts /usr/bin so
             its gio run resolves to the pinned oracle binary; scratch and output live in a secret
             sibling dir OUTSIDE the audit allowlist).  stdout is one JSON object per case with
             labels[] measured by that gio at generation time; paths gio refuses are dropped into
             dropped_paths, so no fresh label is ever ERROR.  The counter validates every case
             (contract 2, fresh rules) and scores the tool against labels[] of the same run.  The
             seed is drawn at measurement (os.urandom hex, or the MADO_R97_FRESH_SEED environment
             override for a reproducible run) and printed fresh_seed=...
  --host-list text file; '#' lines are the header, every other non-empty line is one host path whose raw
             bytes may carry \\xHH escapes.  >=1500 paths.  Fail-closed credential guard: a path whose
             basename or any component matches .ssh .gnupg agent.db credential keyring token secret
             .netrc hosts.yml auth id_rsa shadow passwd, or whose basename ends .pem/.key, or that is
             under ~/.config/{gh,anthropic,elevenlabs,omp} ~/.local/share/keyrings ~/.aws ~/.docker is
             refused (SETUP_ERROR, exit 2) before any host byte is read.  Case-root fixtures are exempt
             (built by the counter from committed base64).
  --host-db  {"version":1,"mode":"text|cache","source":{"dir":...},"files":[{"name","sha256"},...]}.
             mode text: every named file is copied from source.dir into <scratch>/hostdb/mime/, each
             sha256 verified, and the copy must hold no loadable mime.cache (>=40 bytes, version 1.1/1.2
             big-endian at bytes 0..3).  mode cache: source.dir is used read-only as the db root (the
             host's own database); mime.cache must exist there and be loadable.  The tool and gio see the
             same db root; prints host_db=<mode> files=<n>.
  --forgery  the frozen library-asking forgery; run under the launcher: rejected iff the audit denies it
             or the static conjunct flags it.

SETUP order (first failure wins; stable id= tokens on every SETUP_ERROR line):
  setup-pin-format (64-hex pins, 40-hex revs) -> setup-<cases|mutants|genseed|host-list|host-db|forgery>-missing
  -> setup-scratch-root -> setup-<name>-sha256 -> setup-rev-not-commit / setup-base-rev-not-commit /
  setup-base-has-tool -> setup-<tool|mimeglob|mimesniff|mimetext>-missing-at-rev / -sha256 ->
  setup-gio-missing / setup-gio-sha256 -> setup-envelope-* / setup-case-* / setup-census-* ->
  setup-mutants-* -> setup-host-list-parse / credential-shaped host path -> setup-host-db-*.

Legs: frozen (candidate under the launcher, one invocation per case, parsed MADO_FILETYPE lines +
MADO_FILETYPE_DIRS db value against the derived case db mode), fresh, host, mutant, selftest
(MADO_FILETYPE_SELFTEST: checks=N failed=0, N>=20, rc 0), controls: the name-only shim (generated
instrument that answers the pinned r94 name-only guess for every path, scored through the same parser),
the candidate run with --fast on every case (cheapest no-work proxy), a naive extension table with the
six fixed inode/* names (in-counter), the memoriser (label table keyed by the case fingerprint; sentinel
on a miss; 0 required on fresh), and the forgery.  audit_denials counts candidate-run denials and must
be 0; the forgery's own denials are printed as forgery_audit_denials and must be > 0 (or the static
conjunct flags the forgery).  Stdlib only in this counter; socket is used solely to create AF_UNIX
fixture files for sock cases; the counter never writes the lane.  ASCII only.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import socket
import stat as statmod
import subprocess
import sys
import sysconfig
import tempfile
from concurrent.futures import ThreadPoolExecutor

PRED = "PRED-C1-r97-v1"
PREFIX = "MADO_FILETYPE_COUNT:"
CLASSES = ("dir", "chr", "blk", "fifo", "sock", "zero", "empty", "sym", "brok", "nofollow",
           "follow", "certain", "uncertain", "fast", "readerr")
MIN_PER_CLASS = 8
MIN_CASES = 120          # 15 classes x >=8
MIN_FRESH_CASES = 120
MIN_HOST_PATHS = 1500
MIN_SELFTEST_CHECKS = 20
TOOL = "tools/mado-filetype.py"
SIBS = ("tools/mado-mimeglob.py", "tools/mado-mimesniff.py", "tools/mado-mimetext.py")
TOOL_NAME = "mado-filetype.py"
SIB_NAMES = ("mado-mimeglob.py", "mado-mimesniff.py", "mado-mimetext.py")
GLIB = "2.90.1-1"
GIO = "/usr/bin/gio"
UNKNOWN = "application/octet-stream"
MEMO_MISS = "application/x-mado-memoriser-miss"
TOOL_TIMEOUT = 30.0
GIO_TIMEOUT = 15.0
FRESH_RUN_TIMEOUT = 900.0
HOST_TOOL_CHUNK = 200
ORACLE_WORKERS = 16
TEXT_DB_FILES = ("magic", "globs", "globs2", "aliases", "subclasses", "icons", "generic-icons",
                 "XMLnamespaces")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")

# ---------------------------------------------------------------- credential guard (L1 r56 rule)

_CRED_SUB = re.compile(r"(\.ssh|\.gnupg|agent\.db|credential|keyring|token|secret|\.netrc|hosts\.yml"
                       r"|auth|id_rsa|shadow|passwd)", re.IGNORECASE)
_CRED_SUFFIX = re.compile(r"(\.pem|\.key)$", re.IGNORECASE)
_CRED_PREFIX = ("~/.config/gh", "~/.config/anthropic", "~/.config/elevenlabs", "~/.config/omp",
                "~/.local/share/keyrings", "~/.aws", "~/.docker")


def credential_hits(raw: str) -> bool:
    cands = [raw]
    if raw.startswith("~"):
        cands.append(os.path.expanduser(raw))
    parts: set[str] = set()
    for c in cands:
        parts.update(p for p in c.split("/") if p)
    for p in parts:
        if _CRED_SUB.search(p) or _CRED_SUFFIX.search(p):
            return True
    for c in cands:
        for pre in _CRED_PREFIX:
            if c == pre or c.startswith(pre + "/"):
                return True
    return False


# ---------------------------------------------------------------- small helpers

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: str) -> str:
    with open(p, "rb") as fh:
        return sha(fh.read())


def git_show(repo: str, rev: str, path: str) -> bytes | None:
    r = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def unb64(s: str) -> bytes:
    return base64.b64decode(s.encode("ascii"))


# ---------------------------------------------------------------- case db mode (the DIRS line)

def case_env(case: dict, root: str) -> dict[str, str | None]:
    e = case.get("env", {})
    out: dict[str, str | None] = {}
    for k in ("HOME", "XDG_DATA_HOME", "XDG_DATA_DIRS"):
        v = e.get(k)
        out[k] = None if v is None else v.replace("{root}", root)
    return out


def case_roots(case: dict) -> list[str]:
    env = case.get("env", {})
    roots = []
    dh = env.get("XDG_DATA_HOME")
    if dh is not None:
        roots.append(dh)
    else:
        home = env.get("HOME")
        if home is not None:
            roots.append(home.rstrip("/") + "/.local/share")
    dd = env.get("XDG_DATA_DIRS")
    if dd:
        roots.extend(dd.split(":"))
    out = []
    for r in roots:
        r = r.replace("{root}", "").strip("/")
        if r and not r.startswith("/"):
            out.append(r)
    return out


def concrete_roots(case: dict, root: str) -> list[str]:
    """The case's concrete XDG data roots: {root} templates resolved against the case root,
    absolute host roots passed through unchanged."""
    env = case_env(case, root)
    out = []
    dh = env.get("XDG_DATA_HOME")
    if dh is not None:
        out.append(dh)
    else:
        home = env.get("HOME")
        if home is not None:
            out.append(home.rstrip("/") + "/.local/share")
    dd = env.get("XDG_DATA_DIRS")
    if dd:
        out.extend(dd.split(":"))
    return out


def case_host_roots(case: dict) -> list[str]:
    """Absolute host roots the case env declares (the host's own database), if any."""
    env = case.get("env", {})
    out = []
    dh = env.get("XDG_DATA_HOME")
    if isinstance(dh, str) and dh.startswith("/"):
        out.append(dh)
    dd = env.get("XDG_DATA_DIRS")
    if isinstance(dd, str):
        out.extend(s for s in dd.split(":") if s.startswith("/"))
    return out


def _reachable(rel: str, roots: list[str]) -> bool:
    return any(rel == r or rel.startswith(r + "/") for r in roots)


def loadable_cache(data: bytes) -> bool:
    return len(data) >= 40 and int.from_bytes(data[0:2], "big") == 1 \
        and int.from_bytes(data[2:4], "big") in (1, 2)


def case_db_mode(case: dict, root: str = "") -> str:
    """'cache' | 'text' | 'none' - the db state the candidate's MADO_FILETYPE_DIRS line must report.
    Hermetic ({root}) roots are judged by the case's declared files; absolute host roots are judged by
    the live filesystem (read-only), exactly what the tool itself will see at runtime."""
    cache = text = False
    roots = case_roots(case)
    for rel, b64 in case.get("files", {}).items():
        if rel.endswith("/") or not _reachable(rel, roots):
            continue
        parts = rel.rsplit("/", 2)
        if len(parts) < 2 or parts[-2] != "mime":
            continue
        if parts[-1] == "mime.cache":
            try:
                if loadable_cache(unb64(b64)):
                    cache = True
            except Exception:
                pass
        elif parts[-1] in TEXT_DB_FILES:
            text = True
    for r in concrete_roots(case, root):
        if not os.path.isabs(r) or cache:
            continue
        try:
            with open(os.path.join(r, "mime", "mime.cache"), "rb") as fh:
                data = fh.read()
        except OSError:
            data = b""
        if loadable_cache(data):
            cache = True
            break
        if any(os.path.exists(os.path.join(r, "mime", fn)) for fn in TEXT_DB_FILES):
            text = True
    return "cache" if cache else ("text" if text else "none")


# ---------------------------------------------------------------- case materialisation

class CaseError(Exception):
    pass


def materialise_case(case: dict, root: str) -> list[str]:
    """Build the case tree under root; return the absolute scored paths in label order."""
    os.makedirs(root, exist_ok=True)
    for rel, b64 in case.get("files", {}).items():
        p = os.path.join(root, rel)
        parent = os.path.dirname(p.rstrip("/"))
        if parent:
            os.makedirs(parent, exist_ok=True)
        if rel.endswith("/"):
            os.makedirs(p, exist_ok=True)
        else:
            with open(p, "wb") as fh:
                fh.write(unb64(b64))
    out = []
    for ent in case.get("paths", []):
        t = ent["type"]
        rp = ent["path"]
        if t in ("chardev", "blkdev"):
            st = os.lstat(rp)
            want = statmod.S_ISCHR if t == "chardev" else statmod.S_ISBLK
            if not want(st.st_mode):
                raise CaseError(f"path {rp} is not a {t} on this host")
            out.append(rp)
            continue
        p = os.path.join(root, rp)
        if t == "dir":
            os.makedirs(p, exist_ok=True)
        elif t in ("file", "unreadable"):
            if not os.path.isfile(p):
                raise CaseError(f"path {rp} of type {t} is not a declared regular file")
            if t == "unreadable":
                os.chmod(p, 0)
        elif t == "fifo":
            os.mkfifo(p, 0o644)
        elif t == "sock":
            if os.path.lexists(p):
                os.unlink(p)
            s = socket.socket(socket.AF_UNIX)
            try:
                s.bind(p)
            finally:
                s.close()
        elif t == "symlink":
            parent = os.path.dirname(p.rstrip("/"))
            if parent:
                os.makedirs(parent, exist_ok=True)
            os.symlink(ent["target"].replace("{root}", root), p)
        else:
            raise CaseError(f"unknown path type {t!r}")
        out.append(p if os.path.isabs(rp) else os.path.join(root, rp))
    return out


# ---------------------------------------------------------------- the gio oracle

class Gio:
    """The installed gio CLI: one `gio info -a <attr> [-n] <path>` per path under env -i.
    Returns the attribute value, or None when gio exits nonzero and prints no attribute (ERROR)."""

    def __init__(self, binary: str):
        self.binary = binary

    def label(self, path: str, env_extra: dict[str, str | None], attr: str, nofollow: bool,
              timeout: float = GIO_TIMEOUT) -> str | None:
        attrname = "standard::fast-content-type" if attr == "fast" else "standard::content-type"
        argv = [self.binary, "info", "-a", attrname]
        if nofollow:
            argv.append("-n")
        argv.append(os.fsdecode(path) if isinstance(path, bytes) else path)
        env = {"LC_ALL": "C"}
        for k, v in env_extra.items():
            if v is not None:
                env[k] = v
        try:
            r = subprocess.run(argv, capture_output=True, timeout=timeout, env=env)
        except (OSError, subprocess.TimeoutExpired):
            return None
        if r.returncode != 0:
            return None
        m = re.search(rf"^\s*{re.escape(attrname)}: ?([^\r\n]*)\s*$",
                      r.stdout.decode("utf-8", "surrogateescape"), re.M)
        if m is None:
            return None
        return m.group(1)


# ---------------------------------------------------------------- validation

def _rel_ok(rel: str) -> bool:
    if not rel or rel.startswith("/") or "\x00" in rel:
        return False
    body = rel.rstrip("/")
    if not body:
        return rel.endswith("/")      # a bare "/" root entry is a directory
    return not any(p in ("..", "") for p in body.split("/"))


def validate_case_common(c: dict, fresh: bool) -> tuple[str, str] | None:
    """Contract-2 rules shared by the frozen and fresh sets; None = ok, else (setup_id, detail)."""
    cid = c.get("id", "?")
    env = c.get("env", {})
    if not isinstance(env, dict) or set(env) - {"HOME", "XDG_DATA_HOME", "XDG_DATA_DIRS"}:
        return (f"setup-case-{cid}-env", "env keys must be exactly HOME/XDG_DATA_HOME/XDG_DATA_DIRS")
    if env.get("XDG_DATA_DIRS") is None:
        return (f"setup-case-{cid}-dirs", "XDG_DATA_DIRS null (unset) is forbidden in cases")
    if env.get("HOME") != "{root}/h":
        return (f"setup-case-{cid}-home", f"HOME {env.get('HOME')!r} != '{{root}}/h'")
    dh = env.get("XDG_DATA_HOME")
    if dh is not None and not (isinstance(dh, str) and (dh.startswith("{root}/") or
                                                        (dh.startswith("/") and not credential_hits(dh)))):
        return (f"setup-case-{cid}-dh",
                f"XDG_DATA_HOME {dh!r} is not a {{root}} template, null, or a declared host root")
    dd = env.get("XDG_DATA_DIRS")
    if not isinstance(dd, str) or not dd:
        return (f"setup-case-{cid}-dirs", f"XDG_DATA_DIRS {dd!r} is empty")
    for seg in dd.split(":"):
        if not seg or not (seg.startswith("{root}/") or
                           (seg.startswith("/") and not credential_hits(seg))):
            return (f"setup-case-{cid}-dirs",
                    f"XDG_DATA_DIRS segment {seg!r} is neither a {{root}} template nor a declared "
                    "host root")
    if c.get("mode") not in ("follow", "nofollow"):
        return (f"setup-case-{cid}-mode", f"mode {c.get('mode')!r} not follow|nofollow")
    if c.get("attr") not in ("full", "fast"):
        return (f"setup-case-{cid}-attr", f"attr {c.get('attr')!r} not full|fast")
    paths = c.get("paths")
    labels = c.get("labels")
    if not isinstance(paths, list) or not (1 <= len(paths) <= 12):
        return (f"setup-case-{cid}-paths", f"{len(paths) if isinstance(paths, list) else '?'} paths, need 1..12")
    if not isinstance(labels, list) or len(labels) != len(paths):
        return (f"setup-case-{cid}-labels", "one label per path, in order")
    files = c.get("files", {})
    if not isinstance(files, dict):
        return (f"setup-case-{cid}-files", "files must be an object")
    declared_dirs = set()
    for rel in files:
        if not isinstance(rel, str) or not _rel_ok(rel):
            return (f"setup-case-{cid}-escape", f"files member {rel!r} escapes the case root")
        if rel.endswith("/"):
            declared_dirs.add(rel.rstrip("/"))
        else:
            try:
                unb64(files[rel])
            except Exception:
                return (f"setup-case-{cid}-b64", f"files member {rel!r} is not base64")
    for i, ent in enumerate(paths):
        if not isinstance(ent, dict):
            return (f"setup-case-{cid}-path", f"path {i} malformed")
        t = ent.get("type")
        rp = ent.get("path")
        if t not in ("file", "dir", "fifo", "sock", "symlink", "chardev", "blkdev", "unreadable"):
            return (f"setup-case-{cid}-path", f"path {i} type {t!r} unknown")
        if not isinstance(rp, str) or not rp:
            return (f"setup-case-{cid}-path", f"path {i} empty")
        if t in ("chardev", "blkdev"):
            if not os.path.isabs(rp):
                return (f"setup-case-{cid}-device", f"{t} path {rp!r} must be an absolute host path")
            try:
                st = os.lstat(rp)
            except OSError:
                return (f"setup-case-{cid}-device", f"{t} path {rp!r} missing on this host")
            want = statmod.S_ISCHR(st.st_mode) if t == "chardev" else statmod.S_ISBLK(st.st_mode)
            if not want:
                return (f"setup-case-{cid}-device", f"{t} path {rp!r} has the wrong device kind")
        else:
            if rp.startswith("/") or not _rel_ok(rp):
                return (f"setup-case-{cid}-escape", f"path {i} {rp!r} escapes the case root")
        if t == "symlink":
            tgt = ent.get("target")
            if not isinstance(tgt, str) or not tgt:
                return (f"setup-case-{cid}-target", f"symlink {i} has no target")
        if t in ("file", "unreadable") and rp not in files:
            return (f"setup-case-{cid}-file", f"path {i} {rp!r} of type {t} is not declared in files")
        lab = labels[i]
        if not (isinstance(lab, list) and len(lab) == 1):
            return (f"setup-case-{cid}-label", f"label {i} is not a one-element list")
        if lab[0] == "ERROR":
            if fresh:
                return ("setup-fresh-error-label",
                        f"fresh case {cid}: an unstatable path is outside the surface (rule 7)")
        elif not isinstance(lab[0], str) or not lab[0]:
            return (f"setup-case-{cid}-label", f"label {i} malformed")
    # database rule: >=1 reachable hermetic mime/ tree, or the env points only at empty dirs; a case
    # whose env declares a host root (the host's own database) is exempt from the empty-dir rule
    roots = case_roots(c)
    has_mime = any(not rel.endswith("/") and _reachable(rel, roots) and rel.rsplit("/", 2)[-2] == "mime"
                   for rel in files)
    if not has_mime and not case_host_roots(c):
        for r in roots:
            if r not in declared_dirs:
                return (f"setup-case-{cid}-db",
                        f"no reachable mime/ tree and the env root {r!r} is not a declared empty dir")
    return None


def validate_cases(cases_data: dict, expect_gio_sha: str) -> list[tuple[str, str]]:
    errs: list[tuple[str, str]] = []
    if cases_data.get("version") != 1:
        errs.append(("setup-envelope-version", f"case file version {cases_data.get('version')!r} != 1"))
    oracle = cases_data.get("oracle")
    if not isinstance(oracle, str) or not oracle.startswith("gio info -a standard::"):
        errs.append(("setup-envelope-oracle", f"oracle {oracle!r} is not the gio info contract"))
    if cases_data.get("gio_sha256") != expect_gio_sha:
        errs.append(("setup-envelope-gio", "case file gio_sha256 != --expect-gio-sha256 (labels came "
                                           "from another binary)"))
    if cases_data.get("glib2") != GLIB:
        errs.append(("setup-envelope-glib2", f"glib2 {cases_data.get('glib2')!r} != {GLIB}"))
    if cases_data.get("classes") != list(CLASSES):
        errs.append(("setup-envelope-classes", "classes != the frozen 15 in declaration order"))
    cases = cases_data.get("cases")
    if not isinstance(cases, list) or len(cases) < MIN_CASES:
        errs.append(("setup-census-total",
                     f"{len(cases) if isinstance(cases, list) else '?'} cases, contracted >= {MIN_CASES}"))
        return errs
    for c in cases:
        cid = c.get("id", "?")
        cls = c.get("class")
        if cls not in CLASSES:
            errs.append(("setup-envelope-class", f"case {cid}: class {cls!r} not in the frozen 15"))
            continue
        if not isinstance(cid, str) or not cid.startswith(cls + "-") \
                or not cid[len(cls) + 1:len(cls) + 2].isdigit():
            errs.append(("setup-envelope-id", f"case {cid}: id does not start with '{cls}-NN-'"))
        e = validate_case_common(c, fresh=False)
        if e is not None:
            errs.append(e)
        if len(errs) > 20:
            errs.append(("setup-envelope-many", "...more"))
            return errs
    per_class = {k: sum(1 for c in cases if c.get("class") == k) for k in CLASSES}
    for k in CLASSES:
        if per_class[k] < MIN_PER_CLASS:
            errs.append(("setup-census-class", f"class {k} has {per_class[k]} cases < {MIN_PER_CLASS}"))
    return errs


def validate_mutants(mutants_data: dict, src: str) -> list[tuple[str, str]]:
    errs: list[tuple[str, str]] = []
    if mutants_data.get("version") != 1:
        errs.append(("setup-mutants-version", f"version {mutants_data.get('version')!r} != 1"))
    if mutants_data.get("tool") != TOOL:
        errs.append(("setup-mutants-tool", f"tool {mutants_data.get('tool')!r} != {TOOL}"))
    muts = mutants_data.get("mutants")
    if not isinstance(muts, list) or not muts:
        errs.append(("setup-mutants-empty", "no mutants"))
        return errs
    seen_ids: set[str] = set()
    seen_finds: set[str] = set()
    for m in muts:
        mid = m.get("id", "?")
        cls = m.get("class")
        find = m.get("find")
        rep = m.get("replace")
        if cls not in CLASSES:
            errs.append(("setup-mutants-class", f"mutant {mid}: class {cls!r} not in the frozen 15"))
            continue
        if not isinstance(mid, str) or not mid.startswith(cls + "-"):
            errs.append(("setup-mutants-id", f"mutant {mid}: id does not start with '{cls}-'"))
        if mid in seen_ids:
            errs.append(("setup-mutants-id", f"mutant id {mid} duplicated"))
        seen_ids.add(mid)
        if not isinstance(find, str) or not find or not isinstance(rep, str) or find == rep:
            errs.append(("setup-mutants-anchor", f"mutant {mid}: empty find/replace or find == replace"))
            continue
        n = src.count(find)
        if n != 1:
            errs.append(("setup-mutants-anchor", f"mutant {mid}: find occurs {n} times in the candidate"))
        if find in seen_finds:
            errs.append(("setup-mutants-anchor", f"mutant {mid}: find duplicated across mutants"))
        seen_finds.add(find)
        if len(errs) > 20:
            errs.append(("setup-mutants-many", "...more"))
            return errs
    return errs


# ---------------------------------------------------------------- structural conjunct (static)

_OK_IMPORTS = {"__future__", "argparse", "base64", "errno", "hashlib", "importlib.util", "io", "json",
               "os", "re", "socket", "stat", "struct", "sys", "tempfile"}
# socket is allowed as an import because the candidate's --selftest builds an AF_UNIX fixture to
# exercise the inode/socket stat branch; the audit hook admits socket.__new__ for AF_UNIX only and
# denies every network family, connect and listen
_BAD_OS = re.compile(r"^(system|popen|exec\w*|spawn\w*|posix_spawn\w*|fork\w*)$")
_BAD_NAMES = {"eval", "exec", "compile", "__import__", "getattr", "setattr", "delattr", "vars", "globals",
              "locals", "breakpoint", "import_module", "reload"}
# the declared attribute lists: what the candidate may touch on each pinned sibling module
# (mg._libc is allowed only as the receiver of .setlocale - the carve-out below)
_SIB_ATTRS = {
    "mado-mimeglob.py": {"Unsupported", "Resolver", "xdgmime_dirs", "g_path_get_basename", "esc", "oob",
                         "_LC_ALL"},
    "mado-mimesniff.py": {"Sniffer", "esc", "build_cache", "looks_like_text", "mime_type_for_data",
                          "cache_magic_lookup", "subclass"},
    "mado-mimetext.py": {"Unsupported", "Sniffer", "xdgmime_dirs", "esc", "looks_like_text"},
}


def static_check(src: bytes) -> list[str]:
    """Findings that make static_structural FAIL (empty list = ok): no process, socket, network or
    non-libc dynamic import; exactly one spec_from_file_location per sibling (filename constant in the
    location argument); sibling module attributes limited to the declared lists; no dunder or dynamic
    attribute access; no os.system/popen/exec*/spawn*/fork*."""
    import ast
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return [f"syntax:{e.lineno}"]
    bad: list[str] = []
    parent: dict[int, ast.AST] = {}
    for node in ast.walk(tree):
        for ch in ast.iter_child_nodes(node):
            parent[id(ch)] = node
    spec_calls = []                       # ast.Call sites of spec_from_file_location
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for al in node.names:
                if al.name not in _OK_IMPORTS:
                    bad.append(f"import:{al.name}:{node.lineno}")
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "") != "__future__":
                bad.append(f"import-from:{node.module}:{node.lineno}")
        elif isinstance(node, ast.Name) and node.id in _BAD_NAMES:
            bad.append(f"name:{node.id}:{node.lineno}")
        elif isinstance(node, ast.Attribute):
            if node.attr.startswith("__") and node.attr.endswith("__"):
                bad.append(f"dunder:.{node.attr}:{node.lineno}")
            if node.attr in _BAD_NAMES:
                bad.append(f"attr:{node.attr}:{node.lineno}")
            if isinstance(node.value, ast.Name) and node.value.id == "os" and _BAD_OS.match(node.attr):
                bad.append(f"os.{node.attr}:{node.lineno}")
            if node.attr == "spec_from_file_location":
                call = parent.get(id(node))
                if isinstance(call, ast.Call) and call.func is node:
                    loc = call.args[1] if len(call.args) > 1 else None
                    names = {n.id for n in ast.walk(loc) if isinstance(n, ast.Name)} \
                        if loc is not None else set()
                    if "__file__" not in names:
                        bad.append(f"spec_location-not-own-dir:{node.lineno}")
                    spec_calls.append(call)
                else:
                    bad.append(f"spec_from_file_location-not-called:{node.lineno}")

    def _sib_consts(node) -> list[str]:
        return [n.value for n in ast.walk(node)
                if isinstance(n, ast.Constant) and isinstance(n.value, str) and n.value in _SIB_ATTRS]

    # the pinned load: exactly one spec_from_file_location call site, located at the tool's own dir
    # (__file__ in the location argument).  The sibling loader is either named (a sibling constant in
    # its own body) or generic (the filename arrives as a constant argument at each loader call site);
    # each of the three siblings must be reachable one way or the other.
    if len(spec_calls) != 1:
        bad.append(f"spec_from_file_location-calls:{len(spec_calls)}")
    loader_fn = None
    if spec_calls:
        for f in ast.walk(tree):
            if isinstance(f, ast.FunctionDef) and any(n is spec_calls[0] for n in ast.walk(f)):
                loader_fn = f
                break
        if loader_fn is None:
            bad.append("spec_call-not-in-a-function")
    loader_file: str | None = None
    if loader_fn is not None:
        consts = _sib_consts(loader_fn)
        if consts:
            loader_file = consts[0]
    module_vars: dict[str, str | None] = {}     # name -> sibling filename (None = unresolved)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name) and isinstance(node.value, ast.Call) \
                and isinstance(node.value.func, ast.Attribute) \
                and node.value.func.attr == "module_from_spec":
            module_vars[node.targets[0].id] = loader_file
    # loader functions: return a module variable, or forward to another loader; a loader's own file is
    # a sibling constant in its body, else the file of the loader it forwards to
    fnodes = [f for f in ast.walk(tree) if isinstance(f, ast.FunctionDef)]
    loaders: dict[str, str | None] = {}
    changed = True
    while changed:
        changed = False
        for f in fnodes:
            if f.name in loaders:
                continue
            consts = _sib_consts(f)
            own = consts[0] if consts else None
            is_loader = False
            file = None
            for r in ast.walk(f):
                if isinstance(r, ast.Return) and r.value is not None:
                    if isinstance(r.value, ast.Name) and r.value.id in module_vars:
                        is_loader, file = True, own
                    elif isinstance(r.value, ast.Call) and isinstance(r.value.func, ast.Name) \
                            and r.value.func.id in loaders:
                        is_loader, file = True, (own or loaders[r.value.func.id])
            if is_loader:
                loaders[f.name] = file
                changed = True
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name) and isinstance(node.value, ast.Call) \
                and isinstance(node.value.func, ast.Name) and node.value.func.id in loaders:
            call_file = _sib_consts(node.value)
            module_vars[node.targets[0].id] = call_file[0] if call_file else loaders[node.value.func.id]
    if not module_vars:
        bad.append("no-module_from_spec-binding")
    else:
        resolved = {f for f in module_vars.values() if f is not None}
        if len(resolved) < len(_SIB_ATTRS):
            bad.append(f"sibling-files-unresolved:{','.join(sorted(resolved)) or 'none'}")
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Name) and node.id in module_vars and isinstance(node.ctx, ast.Load)):
            continue
        up = parent.get(id(node))
        if isinstance(up, ast.Attribute) and up.value is node:
            f = module_vars[node.id]
            allowed = _SIB_ATTRS.get(f) if f else None
            if allowed is not None and up.attr in allowed:
                continue
            upp = parent.get(id(up))
            if up.attr == "_libc" and isinstance(upp, ast.Attribute) and upp.attr == "setlocale":
                continue
            bad.append(f"module-attr:{node.id}.{up.attr}:{node.lineno}")
        elif isinstance(up, ast.Return):
            continue
        elif isinstance(up, (ast.Assign, ast.AnnAssign, ast.Call, ast.keyword)):
            continue          # the module object passed around is not an attribute access
        elif isinstance(up, ast.Call) and isinstance(up.func, ast.Attribute) and up.func.attr == "exec_module" \
                and node in up.args:
            continue
        else:
            bad.append(f"module-use:{node.id}:{node.lineno}")
    return bad


# ---------------------------------------------------------------- the audit launcher (every tool run)

LAUNCHER_SRC = r'''import os, socket, sys
_log = os.open(sys.argv[1], os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
_allow = [os.path.realpath(p) for p in sys.argv[2].split(os.pathsep) if p] + ["/dev/null"]
_tool = sys.argv[3]
sys.argv = [_tool] + sys.argv[4:]
_SPAWN_OK = {"ldconfig"}
_BUSY = [False]


def _deny(ev, arg):
    os.write(_log, ("AUDIT_DENY %s %r\n" % (ev, arg)).encode("utf-8", "backslashreplace"))
    os._exit(97)


def _hook(ev, args):
    if _BUSY[0]:
        return
    _BUSY[0] = True
    try:
        if ev == "open":
            p = args[0]
            if isinstance(p, int):
                return
            rp = os.path.realpath(os.fsdecode(p))
            if not any(rp == a or rp.startswith(a + os.sep) for a in _allow):
                _deny(ev, rp)
        elif ev in ("subprocess.Popen", "os.posix_spawn"):
            exe = os.fsdecode(args[0] or (args[1][0] if args[1] else ""))
            rx = os.path.realpath(exe) if os.sep in exe else exe
            if os.path.basename(exe) not in _SPAWN_OK or (os.sep in exe and not rx.startswith(("/usr/bin/", "/usr/sbin/"))):
                _deny(ev, exe)
        elif ev in ("os.system", "os.exec", "os.spawn", "os.fork", "os.forkpty", "pty.spawn",
                    "socket.connect", "socket.connect_ex", "urllib.Request", "http.client.connect"):
            _deny(ev, args[:1])
        elif ev == "socket.__new__":
            # AF_UNIX fixture files are part of the modelled surface; every network family is denied
            fam = args[1] if len(args) > 1 else None
            if fam is None or fam != socket.AF_UNIX:
                _deny(ev, args[:2])
        elif ev == "ctypes.dlopen":
            if args[0] is None:
                return
            if not os.path.basename(os.fsdecode(args[0])).startswith("libc.so"):
                _deny(ev, args[0])
    finally:
        _BUSY[0] = False


sys.addaudithook(_hook)
import runpy  # noqa: E402
runpy.run_path(_tool, run_name="__main__")
'''
_RUN = {"launcher": "", "allow": "", "logs": {}}


def audit_log(kind: str) -> str:
    return _RUN["logs"][kind]


# ---------------------------------------------------------------- tool runs and scoring

_LINE_RE = re.compile(r"^MADO_FILETYPE: (\S+) attr=(full|fast) mode=(follow|nofollow) path=(.*)$")
_ERRLINE_RE = re.compile(r"^MADO_FILETYPE: ERROR stat path=(.*)$")
_DIRS_RE = re.compile(r"^MADO_FILETYPE_DIRS: db=(cache|text|none)(?:\s|$)")


def parse_tool_output(stdout: str) -> tuple[list[dict], str | None]:
    """(per-path parsed lines in print order, dirs db value or None)."""
    lines: list[dict] = []
    dirs = None
    for ln in stdout.splitlines():
        m = _ERRLINE_RE.match(ln)
        if m:
            lines.append({"kind": "error", "path": m.group(1)})
            continue
        m = _LINE_RE.match(ln)
        if m:
            lines.append({"kind": "type", "type": m.group(1), "attr": m.group(2),
                          "mode": m.group(3), "path": m.group(4)})
            continue
        m = _DIRS_RE.match(ln)
        if m:
            dirs = m.group(1)
    return lines, dirs


def tool_flags(case: dict, root: str, attr_override: str | None = None) -> list[str]:
    env = case_env(case, root)
    argv = ["--nofollow"] if case.get("mode") == "nofollow" else ["--follow"]
    if (attr_override or case.get("attr", "full")) == "fast":
        argv.append("--fast")
    home = env.get("HOME")
    argv += ["--home", home] if home is not None else ["--home-unset"]
    dh = env.get("XDG_DATA_HOME")
    argv += ["--data-home", dh] if dh is not None else ["--data-home-unset"]
    dd = env.get("XDG_DATA_DIRS")
    argv += ["--data-dirs", dd] if dd is not None else ["--data-dirs-unset"]
    return argv


def run_tool(tool_path: str, flags: list[str], paths: list[str], cwd: str, timeout: float = TOOL_TIMEOUT,
             audit: str = "main") -> tuple[str, str, int]:
    """("ok", stdout, rc) | ("crash", "", rc).  Only rc 0 and the ERROR-stat rc 2 are parseable output;
    anything else (rc 3 UNSUPPORTED, 97 audit denial) is a crash."""
    argv = [sys.executable, "-I", _RUN["launcher"], audit_log(audit), _RUN["allow"], tool_path] \
        + flags + ["--"] + list(paths)
    try:
        r = subprocess.run(argv, capture_output=True, text=True, timeout=timeout, cwd=cwd,
                           env={"PATH": _RUN["emptypath"], "TMPDIR": cwd})
    except (OSError, subprocess.TimeoutExpired):
        return "crash", "", -1
    if r.returncode not in (0, 2):
        return "crash", "", r.returncode
    return "ok", r.stdout, r.returncode


_HEX_UNESC = re.compile(rb"\\x([0-9a-fA-F]{2})")


def _path_field_ok(raw: str, expect: str) -> bool:
    """The path= value is the tool's esc() spelling of the argv path: printable ASCII (minus
    backslash) literal, every other byte as \\xHH.  Exact equality, or equality after \\xHH
    reversal, passes; any other spelling is a scored wrong answer."""
    if raw == expect:
        return True
    try:
        un = _HEX_UNESC.sub(lambda m: bytes([int(m.group(1), 16)]), os.fsencode(raw))
        return os.fsdecode(un) == expect
    except Exception:
        return False


def score_case(tool_path: str, case: dict, root: str, attr_override: str | None = None,
               audit: str = "main") -> str:
    """'ok' | 'wrong' | 'crash' for one materialised case against its frozen labels.  The scored
    answer per path is the type token, the attr and mode tokens and the path= spelling (esc-
    reversible); the DIRS db value is scored per case; the exit code must be 0, or 2 exactly when an
    ERROR label is scored.  The tool prints ERROR lines during the stat loop and the remaining lines
    after it, so lines are matched per kind in path order - a missing or extra line is a scored
    wrong answer, never a crash."""
    try:
        paths = materialise_case(case, root)
    except (CaseError, OSError, ValueError, KeyError):
        return "crash"
    status, out, rc = run_tool(tool_path, tool_flags(case, root, attr_override), paths, root,
                               audit=audit)
    if status == "crash":
        return "crash"
    parsed, dirs = parse_tool_output(out)
    labels = [l[0] for l in case.get("labels", [])]
    expect_rc = 2 if any(l == "ERROR" for l in labels) else 0
    if dirs != case_db_mode(case, root) or rc != expect_rc:
        return "wrong"
    errs = [p for p in parsed if p["kind"] == "error"]
    typs = [p for p in parsed if p["kind"] == "type"]
    if len(errs) + len(typs) != len(labels):
        return "wrong"
    ei = ti = 0
    want_attr = attr_override or case.get("attr", "full")
    want_mode = case.get("mode", "follow")
    for lab, p in zip(labels, paths):
        if lab == "ERROR":
            if ei >= len(errs) or not _path_field_ok(errs[ei]["path"], p):
                return "wrong"
            ei += 1
        else:
            if ti >= len(typs):
                return "wrong"
            ln = typs[ti]
            ti += 1
            if ln["type"] != lab or ln["attr"] != want_attr or ln["mode"] != want_mode \
                    or not _path_field_ok(ln["path"], p):
                return "wrong"
    if ei != len(errs) or ti != len(typs):
        return "wrong"
    return "ok"


def run_cases(tool_path: str, cases: list[dict], work: str, jobs: int, attr_override: str | None = None,
              audit: str = "main", prefix: str = "case-") -> list[str]:
    def one(c: dict) -> str:
        root = tempfile.mkdtemp(prefix=prefix, dir=work)
        try:
            return score_case(tool_path, c, root, attr_override, audit)
        finally:
            shutil.rmtree(root, ignore_errors=True)
    with ThreadPoolExecutor(jobs) as ex:
        return list(ex.map(one, cases))


# ---------------------------------------------------------------- controls

_NAIVE_EXT = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif",
              ".txt": "text/plain", ".md": "text/markdown", ".html": "text/html", ".css": "text/css",
              ".js": "text/javascript", ".json": "application/json", ".xml": "application/xml",
              ".pdf": "application/pdf", ".zip": "application/zip", ".gz": "application/gzip",
              ".tar": "application/x-tar", ".svg": "image/svg+xml", ".mp3": "audio/mpeg",
              ".mp4": "video/mp4", ".wav": "audio/x-wav", ".csv": "text/csv", ".py": "text/x-python",
              ".sh": "application/x-shellscript", ".so": "application/x-sharedlib",
              ".yaml": "application/yaml", ".yml": "application/yaml", ".bmp": "image/bmp",
              ".webp": "image/webp", ".ico": "image/vnd.microsoft.icon", ".ogg": "audio/ogg",
              ".log": "text/plain", ".ini": "text/plain", ".conf": "text/plain"}
_NAIVE_NAME = {"dir": "inode/directory", "directory": "inode/directory", "subdir": "inode/directory",
               "h": "inode/directory", "dh": "inode/directory", "d1": "inode/directory",
               "d2": "inode/directory", "mime": "inode/directory", "fifo": "inode/fifo",
               "pipe": "inode/fifo", "pipe.fifo": "inode/fifo", "sock": "inode/socket",
               "socket": "inode/socket", "sock.unix": "inode/socket", "symlink": "inode/symlink",
               "link": "inode/symlink", "null": "inode/chardevice", "zero": "inode/chardevice",
               "random": "inode/chardevice", "loop0": "inode/blockdevice", "sda": "inode/blockdevice",
               "nvme0n1": "inode/blockdevice", "nvme0n1p1": "inode/blockdevice",
               "zerosize": "application/x-zerosize", "zero.bin": "application/x-zerosize",
               "empty.bin": "application/x-zerosize"}


def naive_answers(case: dict, root: str) -> list[str]:
    """The naive extension-table model: the six fixed inode/* names by fixture name, extensions from a
    small table, application/octet-stream otherwise; it never answers ERROR and never sees content."""
    out = []
    for ent in case.get("paths", []):
        rp = ent.get("path", "")
        if ent.get("type") == "dir" or rp.endswith("/"):
            out.append("inode/directory")
            continue
        base = rp.rstrip("/").rsplit("/", 1)[-1]
        ext = base.rsplit(".", 1)
        hit = _NAIVE_NAME.get(base)
        if hit is None and len(ext) == 2:
            hit = _NAIVE_EXT.get("." + ext[1].lower())
        out.append(hit or UNKNOWN)
    return out


def control_case_ok(answers: list[str], labels: list[str]) -> bool:
    if len(answers) != len(labels):
        return False
    return all(a == l for a, l in zip(answers, labels))


def score_naive(cases: list[dict], work: str, jobs: int) -> int:
    def one(c: dict) -> bool:
        root = tempfile.mkdtemp(prefix="naive-", dir=work)
        try:
            materialise_case(c, root)
            return control_case_ok(naive_answers(c, root), [l[0] for l in c.get("labels", [])])
        except (CaseError, OSError, ValueError, KeyError):
            return False
        finally:
            shutil.rmtree(root, ignore_errors=True)
    with ThreadPoolExecutor(jobs) as ex:
        return sum(1 for ok in ex.map(one, cases) if ok)


def case_fingerprint(case: dict) -> str:
    """The memoriser's case identity: mode + attr + env triple + files digests + the path entries.
    Labels are NOT in the key (the model maps identity to labels); a fresh case can never collide."""
    h = hashlib.sha256()
    h.update(case.get("mode", "?").encode("ascii") + b"\x00")
    h.update(case.get("attr", "?").encode("ascii") + b"\x01")
    env = case_env(case, "")
    for k in ("HOME", "XDG_DATA_HOME", "XDG_DATA_DIRS"):
        v = env.get(k)
        h.update(k.encode("ascii") + b"=" + (v.encode("utf-8", "surrogateescape")
                                             if v is not None else b"<unset>") + b"\x02")
    for rel in sorted(case.get("files", {})):
        h.update(rel.encode("utf-8", "surrogateescape") + b"\x03" + sha(unb64(case["files"][rel])).encode("ascii"))
    for ent in case.get("paths", []):
        h.update(json.dumps(ent, sort_keys=True).encode("utf-8") + b"\x04")
    return h.hexdigest()


def memoriser_model_path(cases: list[dict], secret: str) -> str:
    table = {case_fingerprint(c): [l[0] for l in c.get("labels", [])] for c in cases}
    p = os.path.join(secret, "memo-model.json")
    with open(p, "w", encoding="ascii") as fh:
        json.dump(table, fh, sort_keys=True)
    return p


def memoriser_answers(table: dict, case: dict) -> list[str]:
    labs = table.get(case_fingerprint(case))
    n = len(case.get("paths", []))
    if labs is None or len(labs) != n:
        return [MEMO_MISS] * n
    return list(labs)


def score_memoriser(table: dict, cases: list[dict], work: str, jobs: int) -> int:
    def one(c: dict) -> bool:
        root = tempfile.mkdtemp(prefix="memo-", dir=work)
        try:
            materialise_case(c, root)
            return control_case_ok(memoriser_answers(table, c), [l[0] for l in c.get("labels", [])])
        except (CaseError, OSError, ValueError, KeyError):
            return False
        finally:
            shutil.rmtree(root, ignore_errors=True)
    with ThreadPoolExecutor(jobs) as ex:
        return sum(1 for ok in ex.map(one, cases) if ok)


# the do-nothing control: a generated shim that answers the pinned r94 name-only guess for every
# path (no stat branches, no sniff), scored through the same parser as the candidate
SHIM_SRC = r'''import argparse, importlib.util, os, sys
spec = importlib.util.spec_from_file_location("mado_mimeglob_pin", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "mado-mimeglob.py"))
mg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mg)
TEXT_DB_FILES = ("magic", "globs", "globs2", "aliases", "subclasses", "icons", "generic-icons",
                 "XMLnamespaces")
ap = argparse.ArgumentParser(add_help=False)
ap.add_argument("--follow", action="store_true")
ap.add_argument("--nofollow", action="store_true")
ap.add_argument("--fast", action="store_true")
ap.add_argument("--home")
ap.add_argument("--home-unset", action="store_true")
ap.add_argument("--data-home")
ap.add_argument("--data-home-unset", action="store_true")
ap.add_argument("--data-dirs")
ap.add_argument("--data-dirs-unset", action="store_true")
ap.add_argument("paths", nargs="*")
a = ap.parse_args(sys.argv[1:])
dh = a.data_home if not a.data_home_unset else None
dd = a.data_dirs if not a.data_dirs_unset else None
home = a.home if not a.home_unset else None
roots = []
if dh:
    roots.append(dh)
elif home:
    roots.append(os.path.join(home, ".local/share"))
if dd:
    roots.extend(dd.split(":"))
db = "none"
for r in roots:
    try:
        data = open(os.path.join(r, "mime", "mime.cache"), "rb").read()
    except OSError:
        data = b""
    if len(data) >= 40 and data[0:2] == b"\x00\x01" and data[2:4] in (b"\x00\x01", b"\x00\x02"):
        db = "cache"
        break
    if any(os.path.exists(os.path.join(r, "mime", fn)) for fn in TEXT_DB_FILES):
        db = "text"
try:
    resolver = mg.Resolver(mg.xdgmime_dirs(dh, home, dd))
except Exception:
    resolver = None
attr = "fast" if a.fast else "full"
mode = "nofollow" if a.nofollow else "follow"
for p in a.paths:
    base = mg.g_path_get_basename(os.fsencode(p))
    t = "application/octet-stream"
    if resolver is not None:
        try:
            t = resolver.guess(base)["type"]
        except Exception:
            t = "application/octet-stream"
    sys.stdout.write("MADO_FILETYPE: %s attr=%s mode=%s path=%s\n" % (t, attr, mode, p))
sys.stdout.write("MADO_FILETYPE_DIRS: db=%s\n" % db)
'''


def build_shim(tdir: str) -> str:
    p = os.path.join(tdir, "mado-filetype-nameonly-shim.py")
    with open(p, "w", encoding="ascii") as fh:
        fh.write(SHIM_SRC)
    return p


# ---------------------------------------------------------------- fresh leg

def fresh_cases(gen_path: str, seed: str, secret: str, tag: int) -> list[dict]:
    """Run the frozen generator (`python3 -I <genseed> --seed HEX --dir D --out F --count 140`) inside
    the counter at measurement time; its PATH starts /usr/bin so its gio run resolves to the pinned
    oracle binary.  stdout is one JSON object per case whose labels[] were measured by that gio at
    generation time (refused paths dropped into dropped_paths, so no fresh label is ERROR).  Every
    case is validated (contract 2, fresh rules); the generator's scratch and output live under
    `secret`, OUTSIDE the audit allowlist, so the tool cannot read the labels."""
    gen_dir = os.path.join(secret, f"gendir-{tag}")
    gen_out = os.path.join(secret, f"fresh-{seed}-{tag}.jsonl")
    os.makedirs(gen_dir, exist_ok=True)
    r = subprocess.run([sys.executable, "-I", gen_path, "--seed", seed, "--dir", gen_dir,
                        "--out", gen_out, "--count", "140"], capture_output=True, text=True,
                       timeout=FRESH_RUN_TIMEOUT,
                       env={"PATH": "/usr/bin:/usr/sbin:/bin", "HOME": gen_dir,
                            "LC_ALL": "C", "TMPDIR": gen_dir})
    if r.returncode != 0:
        raise RuntimeError(f"generator rc={r.returncode}: {r.stderr[-400:]}")
    cases = []
    for ln in r.stdout.splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            cases.append(json.loads(ln))
        except json.JSONDecodeError as e:
            raise RuntimeError(f"generator stdout line is not JSON: {ln[:80]!r}: {e}")
    if len(cases) < MIN_FRESH_CASES:
        raise RuntimeError(f"generator produced {len(cases)} cases, contracted >= {MIN_FRESH_CASES}")
    for c in cases:
        e = validate_case_common(c, fresh=True)
        if e is not None:
            raise RuntimeError(f"fresh case violations: {e[0]} {e[1]}")
    return cases


# ---------------------------------------------------------------- host leg

def host_file_list(data: bytes) -> list[str]:
    """The frozen host list: '#' lines are the header; every other non-empty line is one path whose
    raw bytes may carry \\xHH escapes."""
    esc = re.compile(rb"\\x([0-9a-fA-F]{2})")
    paths = []
    for ln in data.split(b"\n"):
        if not ln or ln.startswith(b"#"):
            continue
        paths.append(os.fsdecode(esc.sub(lambda m: bytes([int(m.group(1), 16)]), ln)))
    return paths


def build_host_db(manifest_path: str, work: str) -> tuple[str, str, int]:
    """Returns (db_root, mode, files).  mode text: copy+verify the named files, no loadable cache in
    the copy.  mode cache: use the declared source dir read-only; its mime.cache must be loadable."""
    try:
        with open(manifest_path, encoding="utf-8") as fh:
            manifest = json.load(fh)
    except (OSError, json.JSONDecodeError) as e:
        raise RuntimeError(f"manifest unreadable: {e}")
    if manifest.get("version") != 1:
        raise RuntimeError(f"manifest version {manifest.get('version')!r} != 1")
    mode = manifest.get("mode")
    if mode not in ("text", "cache"):
        raise RuntimeError(f"manifest mode {mode!r} not text|cache")
    srcdir = manifest.get("source", {}).get("dir")
    if not isinstance(srcdir, str) or not srcdir or not os.path.isdir(srcdir):
        raise RuntimeError(f"manifest source.dir {srcdir!r} is not a directory")
    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        raise RuntimeError("manifest holds no files")
    if mode == "cache":
        cache_p = os.path.join(srcdir, "mime", "mime.cache")
        try:
            with open(cache_p, "rb") as fh:
                data = fh.read()
        except OSError as e:
            raise RuntimeError(f"cache mode: {cache_p} unreadable: {e}")
        if not loadable_cache(data):
            raise RuntimeError("cache mode: the declared source mime.cache is not loadable")
        return srcdir, mode, len(files)
    db = os.path.join(work, "hostdb")
    os.makedirs(os.path.join(db, "mime"))
    for ent in files:
        name = ent.get("name")
        want = ent.get("sha256")
        if not isinstance(name, str) or "/" in name or not isinstance(want, str):
            raise RuntimeError(f"manifest bad entry {ent!r}")
        src = os.path.join(srcdir, name)
        if not os.path.isfile(src):
            raise RuntimeError(f"host text file {src} missing")
        with open(src, "rb") as fh:
            data = fh.read()
        if sha(data) != want:
            raise RuntimeError(f"host text file {src} sha256 != manifest pin")
        with open(os.path.join(db, "mime", name), "wb") as fh:
            fh.write(data)
    if os.path.exists(os.path.join(db, "mime", "mime.cache")):
        raise RuntimeError("built host DB holds a mime.cache")
    return db, mode, len(files)


def host_leg(tool_path: str, gio: Gio, paths: list[str], work: str, jobs: int, dbroot: str,
             attr: str = "full", nofollow: bool = False) -> tuple[int, int]:
    """(correct, total).  Every host path: the live gio label vs the candidate's parsed line, both
    over the same db root (ERROR <-> ERROR stat agrees)."""
    hdir = os.path.join(work, "hosth")
    os.makedirs(hdir, exist_ok=True)
    env_extra = {"HOME": hdir, "XDG_DATA_HOME": None, "XDG_DATA_DIRS": dbroot}
    flags = ["--nofollow"] if nofollow else ["--follow"]
    flags += ["--home", hdir, "--data-home-unset", "--data-dirs", dbroot]
    total = len(paths)
    if total == 0:
        return 0, 0
    labels: list[str | None] = []

    def lab(p: str) -> str | None:
        return gio.label(p, env_extra, attr, nofollow)

    with ThreadPoolExecutor(ORACLE_WORKERS) as ex:
        labels = list(ex.map(lab, paths))
    tool_answers: list[dict] = [None] * total     # parsed line per path, in order
    for i in range(0, total, HOST_TOOL_CHUNK):
        chunk = paths[i:i + HOST_TOOL_CHUNK]
        status, out, _rc = run_tool(tool_path, flags, chunk, work, timeout=TOOL_TIMEOUT * 6, audit="main")
        if status == "crash":
            return 0, total
        parsed, _dirs = parse_tool_output(out)
        # the tool prints ERROR lines during the stat loop and the type lines after it: assign per
        # kind, in path order, keyed on the expected label kind
        errs = [p for p in parsed if p["kind"] == "error"]
        typs = [p for p in parsed if p["kind"] == "type"]
        ei = ti = 0
        for k in range(len(chunk)):
            idx = i + k
            if labels[idx] is None:
                if ei < len(errs):
                    tool_answers[idx] = errs[ei]
                    ei += 1
            else:
                if ti < len(typs):
                    tool_answers[idx] = typs[ti]
                    ti += 1
    correct = 0
    for lab, ans in zip(labels, tool_answers):
        if lab is None:
            if ans is not None and ans["kind"] == "error":
                correct += 1
        elif ans is not None and ans["kind"] == "type" and ans["type"] == lab:
            correct += 1
    return correct, total


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(
        description="Round-97 C1 counter: scores tools/mado-filetype.py (the PATH content-type "
                    "surface) against gio-labelled frozen cases, frozen mutants, a fresh seeded "
                    "generation, the frozen host list, controls, and the candidate's --selftest. "
                    "PRED-C1-r97-v1. rc 0 TARGET_MET / 1 TARGET_MISSED / 2 SETUP_ERROR.")
    ap.add_argument("--repo", required=True, help="the lane worktree (git -C target)")
    ap.add_argument("--rev", required=True, help="the measured revision holding the frozen candidate")
    ap.add_argument("--base-rev", required=True,
                    help="the round-start revision (tools/mado-filetype.py must be absent there)")
    ap.add_argument("--cases", required=True, help="frozen case file (contract 2 schema)")
    ap.add_argument("--expect-cases-sha256", required=True)
    ap.add_argument("--mutants", required=True, help="frozen mutant file (find/replace anchors)")
    ap.add_argument("--expect-mutants-sha256", required=True)
    ap.add_argument("--genseed", required=True, help="frozen fresh-case generator (--seed/--out/--scratch)")
    ap.add_argument("--expect-genseed-sha256", required=True)
    ap.add_argument("--host-list", required=True, help="frozen host path list (>=1500 paths)")
    ap.add_argument("--expect-host-list-sha256", required=True)
    ap.add_argument("--host-db", required=True, help="frozen host db manifest (mode text|cache)")
    ap.add_argument("--expect-host-db-sha256", required=True)
    ap.add_argument("--expect-tool-sha256", required=True,
                    help="sha256 of the frozen tools/mado-filetype.py bytes at --rev")
    ap.add_argument("--expect-mimeglob-sha256", required=True)
    ap.add_argument("--expect-mimesniff-sha256", required=True)
    ap.add_argument("--expect-mimetext-sha256", required=True)
    ap.add_argument("--expect-gio-sha256", required=True, help="sha256 of the installed /usr/bin/gio")
    ap.add_argument("--forgery", required=True, help="frozen library-asking forgery (must be rejected)")
    ap.add_argument("--expect-forgery-sha256", required=True)
    ap.add_argument("--scratch-root", required=True,
                    help="directory for the counter's own scratch (created, then removed on exit)")
    a = ap.parse_args()
    sys.stdout.reconfigure(line_buffering=True)

    def setup(detail: str) -> int:
        print(f"{PREFIX} SETUP_ERROR pred={PRED} {detail}")
        return 2

    # ---- 1: pin formats (M96-1: a malformed pin fails before anything runs)
    pins = [("cases", a.cases, a.expect_cases_sha256),
            ("mutants", a.mutants, a.expect_mutants_sha256),
            ("genseed", a.genseed, a.expect_genseed_sha256),
            ("host-list", a.host_list, a.expect_host_list_sha256),
            ("host-db", a.host_db, a.expect_host_db_sha256),
            ("forgery", a.forgery, a.expect_forgery_sha256)]
    for name, _path, want in pins:
        if not HEX64.match(want):
            return setup(f"id=setup-pin-format --expect-{name}-sha256 {want!r} is not 64 lowercase hex")
    for name, rev in (("rev", a.rev), ("base-rev", a.base_rev)):
        if not HEX40.match(rev.lstrip("g")) and not HEX40.match(rev):
            return setup(f"id=setup-rev-format {name} {rev!r} is not 40 hex")
    # ---- 2: input existence, in counting-command order
    for name, path, _want in pins:
        if not os.path.exists(path):
            return setup(f"id=setup-{name}-missing {path} missing")
    # ---- 3: scratch
    work = secret = None
    try:
        os.makedirs(a.scratch_root, exist_ok=True)
        work = tempfile.mkdtemp(prefix="c1r97-", dir=a.scratch_root)
        secret = tempfile.mkdtemp(prefix="c1r97-labels-", dir=a.scratch_root)
    except OSError as e:
        return setup(f"id=setup-scratch-root {a.scratch_root}: {e}")
    try:
        # ---- 4: input sha pins
        for name, path, want in pins:
            got = sha_file(path)
            if got != want:
                return setup(f"id=setup-{name}-sha256 {path} sha256 {got} != pinned {want}")
        # ---- 5: revisions; the tool must be absent at base (the declared before-state)
        for name, rev in (("rev", a.rev), ("base-rev", a.base_rev)):
            r = subprocess.run(["git", "-C", a.repo, "rev-parse", "--verify", "--quiet",
                                rev + "^{commit}"], capture_output=True)
            if r.returncode != 0:
                return setup(f"id=setup-{'rev' if name == 'rev' else 'base-rev'}-not-commit "
                             f"{rev} is not a commit in {a.repo}")
        base_tool_b = git_show(a.repo, a.base_rev, TOOL)
        if base_tool_b is not None:
            return setup(f"id=setup-base-has-tool {TOOL} already present at base-rev {a.base_rev} "
                         "(declared before: absent)")
        print(f"base: {TOOL} absent at base-rev {a.base_rev} (declared before 0/0)")
        # ---- 6: materialise the frozen candidate and its three pinned siblings (scratch, never the lane)
        tb = git_show(a.repo, a.rev, TOOL)
        if tb is None:
            return setup(f"id=setup-tool-missing-at-rev {TOOL} absent at {a.rev}")
        sib_bytes = {}
        for s in SIBS:
            b = git_show(a.repo, a.rev, s)
            if b is None:
                return setup(f"id=setup-{os.path.basename(s).replace('.py', '')}-missing-at-rev "
                             f"{s} absent at {a.rev}")
            sib_bytes[s] = b
        tool_pin = sha(tb) == a.expect_tool_sha256
        sib_pins = {"tools/mado-mimeglob.py": a.expect_mimeglob_sha256,
                    "tools/mado-mimesniff.py": a.expect_mimesniff_sha256,
                    "tools/mado-mimetext.py": a.expect_mimetext_sha256}
        for s, want in sib_pins.items():
            if sha(sib_bytes[s]) != want:
                return setup(f"id=setup-{os.path.basename(s).replace('.py', '')}-sha256 "
                             f"{s} at {a.rev} sha256 != its pin")
        if not tool_pin:
            return setup(f"id=setup-tool-sha256 {TOOL} at {a.rev} sha256 {sha(tb)} "
                         f"!= --expect-tool-sha256 {a.expect_tool_sha256}")
        print(f"tool_pin=ok sibling_pins=ok,ok,ok (mimeglob mimesniff mimetext)")
        src = tb.decode("utf-8", "surrogateescape")
        # ---- 7: the oracle is the installed gio
        if not (os.path.isfile(GIO) and os.access(GIO, os.X_OK)):
            return setup(f"id=setup-gio-missing {GIO} missing or not executable")
        gio_sha = sha_file(GIO)
        if gio_sha != a.expect_gio_sha256:
            return setup(f"id=setup-gio-sha256 {GIO} sha256 {gio_sha} != --expect-gio-sha256")
        gio = Gio(GIO)
        pq = subprocess.run(["pacman", "-Q", "glib2", "shared-mime-info", "xdg-utils", "file"],
                            capture_output=True, text=True)
        print("pacman -Q glib2 shared-mime-info xdg-utils file: " + (pq.stdout.strip() or pq.stderr.strip()))
        # ---- 8: frozen case envelope + census
        try:
            with open(a.cases, encoding="utf-8") as fh:
                cases_data = json.load(fh)
        except (OSError, json.JSONDecodeError) as e:
            return setup(f"id=setup-cases-parse {a.cases}: {e}")
        for eid, msg in validate_cases(cases_data, a.expect_gio_sha256):
            return setup(f"id={eid} {msg}")
        cases = cases_data["cases"]
        per_class = {k: sum(1 for c in cases if c.get("class") == k) for k in CLASSES}
        print("per_class " + " ".join(f"{k}={per_class[k]}" for k in CLASSES))
        print("case_db_modes " + " ".join(f"{m}={sum(1 for c in cases if case_db_mode(c) == m)}"
                                          for m in ("cache", "text", "none")))
        # ---- 9: mutant anchors against the frozen candidate bytes
        try:
            with open(a.mutants, encoding="utf-8") as fh:
                mutants_data = json.load(fh)
        except (OSError, json.JSONDecodeError) as e:
            return setup(f"id=setup-mutants-parse {a.mutants}: {e}")
        for eid, msg in validate_mutants(mutants_data, src):
            return setup(f"id={eid} {msg}")
        mutants = mutants_data["mutants"]
        # ---- 10: the frozen host list + the fail-closed credential guard (before any host byte)
        host_paths = host_file_list(open(a.host_list, "rb").read())
        print(f"host list paths={len(host_paths)}")
        cred = [p for p in host_paths if credential_hits(p)]
        if cred:
            return setup(f"credential-shaped host path: {cred[0]} credential_guard={len(cred)}")
        if len(host_paths) < MIN_HOST_PATHS:
            return setup(f"id=setup-host-list-short {len(host_paths)} paths < {MIN_HOST_PATHS}")
        # ---- 11: the host db manifest
        try:
            dbroot, db_mode, db_files = build_host_db(a.host_db, work)
        except RuntimeError as e:
            return setup(f"id=setup-host-db {e}")
        print(f"host_db={db_mode} files={db_files} root={dbroot}")

        # ---- the cases' declared host db roots: credential-guarded, then admitted read-only to the
        # audit allow (the tool and the shim must open exactly what gio labels against)
        host_roots_all = sorted({r for c in cases for r in case_host_roots(c)})
        cred_roots = sorted({r for c in cases for r in case_host_roots(c) if credential_hits(r)})
        if cred_roots:
            return setup(f"credential-shaped host path: {cred_roots[0]} credential_guard={len(cred_roots)}")
        if host_roots_all:
            print("case host db roots: " + ",".join(host_roots_all))

        # ---- place the tool tree, launcher, audit allow
        tdir = os.path.join(work, "tools")
        os.makedirs(tdir)
        tool_path = os.path.join(tdir, TOOL_NAME)
        with open(tool_path, "wb") as fh:
            fh.write(tb)
        for s in SIBS:
            with open(os.path.join(tdir, os.path.basename(s)), "wb") as fh:
                fh.write(sib_bytes[s])
        _RUN["launcher"] = os.path.join(work, "launcher.py")
        with open(_RUN["launcher"], "w", encoding="ascii") as fh:
            fh.write(LAUNCHER_SRC)
        pyroots = sorted({os.path.realpath(p) for k, p in sysconfig.get_paths().items()
                          if k in ("stdlib", "platstdlib", "purelib", "platlib")})
        _RUN["allow"] = os.pathsep.join([os.path.realpath(work), dbroot]
                                        + [os.path.realpath(r) for r in host_roots_all] + pyroots)
        _RUN["emptypath"] = tempfile.mkdtemp(prefix="emptypath-", dir=work)
        for k in ("main", "mutant", "selftest", "forgery", "control"):
            _RUN["logs"][k] = os.path.join(work, f"audit-{k}.log")
            open(_RUN["logs"][k], "w").close()
        print("audit_allow=" + _RUN["allow"])

        # ---- structural conjunct on the frozen candidate bytes
        static_bad = static_check(tb)
        print("static_findings=" + (",".join(static_bad) or "none"))

        # ---- selftest leg (vii)
        st = subprocess.run([sys.executable, "-I", _RUN["launcher"], audit_log("selftest"),
                             _RUN["allow"], tool_path, "--selftest"],
                            capture_output=True, text=True, timeout=TOOL_TIMEOUT,
                            cwd=work, env={"PATH": _RUN["emptypath"], "TMPDIR": work})
        st_fail = [ln for ln in st.stdout.splitlines() if ln.startswith("MADO_FILETYPE_SELFTEST_FAIL:")]
        st_res = re.search(r"^MADO_FILETYPE_SELFTEST: checks=(\d+) failed=(\d+)\s*$", st.stdout, re.M)
        st_checks = int(st_res.group(1)) if st_res else -1
        st_failed = int(st_res.group(2)) if st_res else -1
        selftest_ok = st.returncode == 0 and st_failed == 0 and not st_fail \
            and st_checks >= MIN_SELFTEST_CHECKS
        print(f"selftest rc={st.returncode} checks={st_checks} failed={st_failed} "
              f"fail_lines={len(st_fail)} ok={selftest_ok}")
        for ln in st_fail[:6]:
            print("selftest " + ln)

        # ---- frozen leg (i)
        oc = run_cases(tool_path, cases, work, jobs=8)
        for c, o in zip(cases, oc):
            if o != "ok":
                print(f"case {c['id']} {o.upper()}")
        correct = sum(1 for o in oc if o == "ok")
        n = len(cases)
        classes_ok = sum(1 for k in CLASSES
                         if all(o == "ok" for c, o in zip(cases, oc) if c.get("class") == k))
        audit_main = len(open(audit_log("main"), encoding="utf-8", errors="replace").read().splitlines())

        # ---- fresh leg (iii): one generation, a seed drawn at measurement (or the MADO_R97_FRESH_SEED
        # environment override for a reproducible run)
        seed = os.environ.get("MADO_R97_FRESH_SEED") or os.urandom(8).hex()
        try:
            fcases = fresh_cases(a.genseed, seed, secret, 0)
        except (RuntimeError, subprocess.TimeoutExpired, OSError) as e:
            return setup(f"id=setup-fresh-gen {e}")
        foc = run_cases(tool_path, fcases, work, jobs=8, prefix="fresh-")
        fresh_ok = sum(1 for o in foc if o == "ok")
        fresh_total = len(fcases)
        for c, o in zip(fcases, foc):
            if o != "ok":
                print(f"fresh case {c.get('id', '?')} {o.upper()}")
        print(f"fresh_seed={seed} fresh={fresh_ok}/{fresh_total}")
        memo_path = memoriser_model_path(cases, secret)
        memo_table = json.load(open(memo_path, encoding="ascii"))
        memo_fresh = score_memoriser(memo_table, fcases, work, jobs=8)
        memo_frozen = score_memoriser(memo_table, cases, work, jobs=8)
        print(f"control memoriser frozen={memo_frozen}/{n} fresh={memo_fresh}/{fresh_total}")

        # ---- host leg (iv)
        hcorrect, htot = host_leg(tool_path, gio, host_paths, work, jobs=8, dbroot=dbroot)
        print(f"host={hcorrect}/{htot} host_paths={htot}")
        audit_main += len(open(audit_log("main"), encoding="utf-8", errors="replace").read().splitlines())
        print(f"audit_denials={audit_main}")

        # ---- mutant leg (ii): kills are parsed wrong answers or missing lines; crashes are not kills
        mutdir = os.path.join(work, "mutants")
        os.makedirs(mutdir)
        for s in SIBS:
            os.symlink(os.path.join(tdir, os.path.basename(s)), os.path.join(mutdir, os.path.basename(s)))
        killed = crashed = survived = 0
        class_kills = {k: 0 for k in CLASSES}
        for m in mutants:
            mp = os.path.join(mutdir, TOOL_NAME)
            with open(mp, "w", encoding="utf-8") as fh:
                fh.write(src.replace(m["find"], m["replace"], 1))
            mors = run_cases(mp, cases, work, jobs=8, audit="mutant", prefix="mut-")
            wrong_ids = [c["id"] for c, o in zip(cases, mors) if o == "wrong"]
            base_o = oc
            new_crash = sum(1 for mo, co in zip(mors, base_o) if mo == "crash" and co != "crash")
            if wrong_ids:
                killed += 1
                for k in {c["class"] for c, o in zip(cases, mors) if o == "wrong"}:
                    class_kills[k] += 1
                status = f"killed by {wrong_ids[0]} (+{len(wrong_ids) - 1})"
            elif new_crash:
                crashed += 1
                status = f"crashed_not_killed ({new_crash} new crash cases)"
            else:
                survived += 1
                status = "survived"
            print(f"mutant {m['id']} {status}")
        class_kills_ok = sum(1 for k in CLASSES if class_kills[k] >= 1)
        print("class_kills " + " ".join(f"{k}={class_kills[k]}" for k in CLASSES))

        # ---- controls (vi)
        shim_path = build_shim(tdir)
        soc = run_cases(shim_path, cases, work, jobs=8, audit="control", prefix="shim-")
        nameonly_ok = sum(1 for o in soc if o == "ok")
        fprox = run_cases(tool_path, cases, work, jobs=8, attr_override="fast", audit="control",
                          prefix="fastpx-")
        fastproxy_ok = sum(1 for o in fprox if o == "ok")
        naive_ok = score_naive(cases, work, jobs=8)
        print(f"control_nameonly={nameonly_ok}/{n} control_fastproxy={fastproxy_ok}/{n} "
              f"control_naive={naive_ok}/{n}")
        fdir = os.path.join(work, "forgery")
        os.makedirs(fdir)
        forgery_b = open(a.forgery, "rb").read()
        with open(os.path.join(fdir, TOOL_NAME), "wb") as fh:
            fh.write(forgery_b)
        for s in SIBS:
            os.symlink(os.path.join(tdir, os.path.basename(s)), os.path.join(fdir, os.path.basename(s)))
        forgery_static = static_check(forgery_b)
        run_cases(os.path.join(fdir, TOOL_NAME), cases[:3], work, jobs=1, audit="forgery",
                  prefix="forg-")
        forgery_audit = len(open(audit_log("forgery"), encoding="utf-8",
                                 errors="replace").read().splitlines())
        forgery_rejected = forgery_audit > 0 or bool(forgery_static)
        print(f"control forgery static={','.join(forgery_static) or 'none'} "
              f"forgery_audit_denials={forgery_audit} rejected={forgery_rejected}")
        main_lines = open(audit_log("main"), encoding="utf-8", errors="replace").read().splitlines()
        for ln in main_lines[:20]:
            print("audit " + ln)
        audit_main = len(main_lines)
    finally:
        if work is not None:
            shutil.rmtree(work, ignore_errors=True)
        if secret is not None:
            shutil.rmtree(secret, ignore_errors=True)

    static_ok = not static_bad
    met = (tool_pin and static_ok and audit_main == 0
           and correct == n and classes_ok == len(CLASSES)
           and killed == len(mutants) and class_kills_ok == len(CLASSES)
           and fresh_ok == fresh_total and fresh_total >= MIN_FRESH_CASES and memo_fresh == 0
           and hcorrect == htot and htot >= MIN_HOST_PATHS
           and nameonly_ok < n and naive_ok < n and forgery_rejected
           and selftest_ok)
    word = "TARGET_MET" if met else "TARGET_MISSED"
    print(f"{PREFIX} {word} pred={PRED} rev={a.rev} base_rev={a.base_rev} "
          f"tool_sha256={sha(tb)} tool_pin={'ok' if tool_pin else 'FAIL'} "
          f"mimeglob_sha256={sha(sib_bytes[SIBS[0]])} mimesniff_sha256={sha(sib_bytes[SIBS[1]])} "
          f"mimetext_sha256={sha(sib_bytes[SIBS[2]])} gio_sha256={gio_sha} "
          f"cases={n} correct={correct} classes={classes_ok}/{len(CLASSES)} "
          + "per_class " + " ".join(f"{k}={per_class[k]}" for k in CLASSES) + " "
          + f"mutants={len(mutants)} killed={killed} crashed_not_killed={crashed} survived={survived} "
          f"class_kills={class_kills_ok}/{len(CLASSES)} "
          f"fresh={fresh_ok}/{fresh_total} fresh_seed={seed} "
          f"host={hcorrect}/{htot} host_paths={htot} "
          f"static_structural={'ok' if static_ok else 'FAIL'} audit_denials={audit_main} "
          f"forgery_audit_denials={forgery_audit} forgery={'rejected' if forgery_rejected else 'ACCEPTED'} "
          f"control_nameonly={nameonly_ok}/{n} control_fastproxy={fastproxy_ok}/{n} "
          f"control_naive={naive_ok}/{n} memoriser_frozen={memo_frozen}/{n} "
          f"memoriser_fresh={memo_fresh}/{fresh_total} "
          f"selftest={'ok' if selftest_ok else 'FAIL'} checks={st_checks} failed={st_failed} "
          f"host_db={db_mode} files={db_files} credential_guard=0")
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
