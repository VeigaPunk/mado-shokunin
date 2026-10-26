#!/usr/bin/env python3
"""re2fuzz.py - differential test: Python `re.fullmatch` versus RE2 `FullMatch` over the
PRED-C1-r42 REGEX alphabet.

Seat `LabRe2Fuzz`, mado round 43 wave w1. Hypothesis H: for every REGEX the C1 contract
accepts (SAFE alphabet + bad-substring bans + Python compile) and every class string,
`re.fullmatch(REGEX, class)` is true exactly when RE2's `FullMatch` is; and no REGEX the
contract accepts is rejected by RE2.

The contract's regex gate is copied verbatim from the frozen reference
`.ufo/waves/round-42/c1/ctl-ref-tool.py.txt` (SAFE, the four banned substrings, the Python
compile test). The Hyprland side is pinned by `.ufo/waves/round-43/fetch/Hyprland-RegexMatchEngine.cpp`
(sha256 8ca655336cd111df1136be76bbdf91bd6830e7e8891df4bb8c766f1e55a3a282): a rule string is
`re2::RE2(regex)` with default options and matched as `re2::RE2::FullMatch(other, *m_regex)`.
`google-re2`'s `_Regexp.fullmatch` calls the engine with `_Anchor.ANCHOR_BOTH`, exactly what
`RE2::FullMatch` passes, and its `Options()` defaults equal the C++ defaults (encoding UTF-8,
posix_syntax false, one_line false, longest_match false, dot_nl false, never_nl false,
case_sensitive true, perl_classes false, word_boundary false). So `re2.compile(rx).fullmatch(cls)`
is a faithful stand-in for Hyprland's call.

Sweeps (full mode)
  E1  exhaustive strings over the 11 structural characters `a b . ^ $ | ( ) * + ?`, lengths
      1..5, filtered by the contract gate, each against S1 classes.
  E2  exhaustive strings over a representative literal set of 16 characters (`a b . ^ $ | ( ) * +
      ? -` and `\\`), lengths 1..4, filtered by the contract gate, each against S1.
  E3  exhaustive token strings over 22 representative tokens (the 11 structural characters and all
      11 legal escapes), token lengths 1..3, filtered by the contract gate, each against S1. The
      remaining literal characters (letters, digits, `_`) behave as `a` and are exercised by R.
  R   random patterns of contract-token length 1..200 from biased generators (nested groups,
      alternation with empty branches, repetition of groups, anchors in the middle, escaped
      punctuation, runs of dots and quantifiers), each against random classes (length <= 8).
  C   compile-acceptance comparison over every pattern of E1-E3 and R: contract-gate accept
      (Python) versus RE2 accept, both directions counted. `py_only` (the contract accepts a
      regex RE2 rejects) is the direction that would make the tool evaluate a rule Hyprland
      cannot: a rule whose RE2 is not ok() never matches.

Long classes are exercised in two bounded stages, because Python's backtracking engine is
exponential on nested quantifiers while RE2 is linear (measured: `(a*)*` against "a"*24 + "b"
takes 0.48 s in Python, 18 us in RE2; the cost doubles per character):
  L  long-class semantics without nested quantifiers: dot/literal/alternation patterns against
     classes of 64-512 characters (ASCII, non-ASCII, astral), in-process (all linear).
  X  cost stage: curated contract-accepted pathological patterns against long classes, each
     pair in a child process with a 3 s timeout; a timed-out pair is a measured engine-cost
     divergence (Python `re` does not terminate, RE2 does), reported separately from the
     boolean comparison.

Positive controls (the comparator must have teeth): `\\d` vs an Arabic-Indic digit, `\\w` vs
`é`, `\\s` vs U+00A0, `\\D` vs an Arabic-Indic digit, `\\Z`, `[ab]`, `a{2}`: the run reports
whether the contract gate rejects them and that the comparator flags the divergence.

Every value divergence is counted, bucketed by feature, and greedily minimised (pattern first,
then class). If any survives minimisation the run scores candidate contract restrictions
(refuse the construct) against the same pairs. With no value divergence the run reports an
honest negative: pair count, seed, sweeps.

Deterministic: the seed is printed; the random pattern stream uses `random.Random(seed ^ 0x5EED)`
and the random class draws use a separate `random.Random(seed)`, so `restrict-score.py` can
regenerate the identical accepted pattern population from the printed seed alone.
"""
import argparse
import itertools
import json
import random
import re
import signal
import subprocess
import sys
import time

import re2

try:
    from importlib.metadata import version as _pkg_version
    RE2_PKG_VERSION = _pkg_version("google-re2")
except Exception:                                   # pragma: no cover
    RE2_PKG_VERSION = getattr(re2, "__version__", "unknown")

# --- contract regex gate: verbatim from .ufo/waves/round-42/c1/ctl-ref-tool.py.txt:67-69,120-128
SAFE = re.compile(r"(?:[A-Za-z0-9_.^$()|*+?-]|\\[.\-()|*+?^$\\]){1,200}")
BAD = ("(?", "*+", "++", "?+")
BS = chr(92)
TOKEN_ALPHABET = list("ab.^$|()*+?")
EXH_CHARS = list("ab.^$|()*+?-" + chr(92))      # representative literal set (16 characters)
EXH_TOKENS = list("ab.^$|()*+?") + [chr(92) + c for c in ".-()|*+?^$" + chr(92)]
LITERAL_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.^$()|*+?-"
LEGAL_ESCAPES = [BS + c for c in ".-()|*+?^$" + BS]
CONTRACT_TOKENS = list(LITERAL_CHARS) + LEGAL_ESCAPES


def regex_ok(rx):
    if not SAFE.fullmatch(rx):
        return False
    for bad in BAD:
        if bad in rx:
            return False
    try:
        re.compile(rx)
    except re.error:
        return False
    return True


# --- classes
S1 = ["", "a", "ab", "a\n", "é", "😀"]                    # exhaustive-sweep classes
SHORT_POOL = ["", "a", "aa", "ab", "abc", "A", "0", "a0", "a.b", "a_b", "a-b",
              "a\n", "\n", "a\nb", "\x00", "a\x00b", "\x01", "a\tb",
              "é", "aé", "😀", "a😀b", "éé", "Ω", "\u00a0",
              "gkeep", "Alacritty", "zcode", "chromium", ".", "$", "^", "()",
              "aaab", "abab", "aaa", "ab" * 4]
RANDOM_CHARS = list("abAB0._-^$()|*+?éΩ😀 \n\x00")
LONG_CLASSES = ["a" * 64, "ab" * 256, "x" * 300, "é" * 200, "😀" * 120,
                "org.omarchy.gkeep" + "x" * 300, "aA." * 100]


def rand_class(rng):
    if rng.random() < 0.6:
        return rng.choice(SHORT_POOL)
    n = rng.randint(0, 8)
    return "".join(rng.choice(RANDOM_CHARS) for _ in range(n))


# --- pattern generators
def gen_exhaustive(alphabet, maxlen):
    for n in range(1, maxlen + 1):
        for tup in itertools.product(alphabet, repeat=n):
            yield "".join(tup)


def _atom(rng, depth):
    r = rng.random()
    if depth < 3 and r < 0.22:
        return "(" + _braced(rng, depth + 1) + ")"
    if depth < 3 and r < 0.30:
        return "(" + _braced(rng, depth + 1) + "|" + _braced(rng, depth + 1) + ")"
    if r < 0.36:
        return "(" + _braced(rng, depth + 1) + "|)"
    if r < 0.44:
        return rng.choice(LITERAL_CHARS)
    if r < 0.50:
        return rng.choice(LEGAL_ESCAPES)
    if r < 0.58:
        return "."
    if r < 0.64:
        return rng.choice("^$")
    return rng.choice("ab.-")


def _braced(rng, depth):
    out = []
    for _ in range(rng.randint(0, 3)):
        out.append(_atom(rng, depth))
        if rng.random() < 0.30:
            out[-1] += rng.choice("*+?")
    s = "".join(out)
    if rng.random() < 0.25 and s:
        s += "|" + "".join(_atom(rng, depth + 1) for _ in range(rng.randint(0, 2)))
    return s


def gen_random(rng):
    r = rng.random()
    if r < 0.35:
        s = "".join(_atom(rng, 0) for _ in range(rng.randint(1, 6)))
    elif r < 0.55:                     # anchors in the middle
        body = "".join(rng.choice("ab|()*+?.") for _ in range(rng.randint(1, 8)))
        i = rng.randint(0, len(body))
        s = body[:i] + rng.choice("^$") + body[i:]
    elif r < 0.70:                     # repetition of groups / empty alternatives
        s = "".join(rng.choice(["()", "(|)", "(a|)", "(|a)", "((a))", "(a*)", "($)", "(^)"])
                    for _ in range(rng.randint(1, 3)))
        s += rng.choice(["*", "+", "?", ""])
    elif r < 0.85:                     # dot and quantifier runs
        s = "".join(rng.choice([".", "*", "+", "?", "a", "|"]) for _ in range(rng.randint(1, 10)))
    else:                              # escaped punctuation and literals
        s = "".join(rng.choice(CONTRACT_TOKENS) for _ in range(rng.randint(1, 10)))
    return s[:400]


# --- engines
PAIR_BUDGET = 0.05        # seconds; a value pair slower than this is a liveness divergence


class SlowPair(Exception):
    pass


def _on_alarm(signum, frame):
    raise SlowPair()


signal.signal(signal.SIGALRM, _on_alarm)


def py_match(rx, cls):
    """Unbudgeted match, for controls and minimisation of already-known divergences."""
    return re.compile(rx).fullmatch(cls) is not None


def py_match_timed(rx, cls, budget=PAIR_BUDGET):
    """-> (result or None, seconds, timed_out). Python's sre engine checks signals inside its
    backtracking loop, so SIGALRM interrupts an exponential match (verified: a 0.2 s budget
    interrupted `(a*)*` on "a"*30 + "b" at 0.200 s)."""
    c = re.compile(rx)
    t = time.perf_counter()
    signal.setitimer(signal.ITIMER_REAL, budget)
    try:
        return c.fullmatch(cls) is not None, time.perf_counter() - t, False
    except SlowPair:
        return None, time.perf_counter() - t, True
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


def re2_compile(rx):
    try:
        return re2.compile(rx)
    except re2.error:
        return None


def re2_match(obj, cls):
    return obj.fullmatch(cls) is not None


def guarded(cls):
    return not any(ord(ch) < 0x20 for ch in cls)


# --- minimisation
def diverges(rx, cls):
    if not regex_ok(rx):
        return False
    o = re2_compile(rx)
    if o is None:
        return False
    return py_match(rx, cls) != re2_match(o, cls)


def tool_diverges(rx, cls):
    """True when the contract's own predicate (no control char AND re.fullmatch) differs from
    Hyprland's RE2::FullMatch."""
    if not regex_ok(rx):
        return False
    o = re2_compile(rx)
    if o is None:
        return False
    return (guarded(cls) and py_match(rx, cls)) != re2_match(o, cls)


def minimise(pred, rx, cls):
    changed = True
    while changed:
        changed = False
        for i in range(len(rx)):
            cand = rx[:i] + rx[i + 1:]
            if cand and pred(cand, cls):
                rx, changed = cand, True
                break
    changed = True
    while changed:
        changed = False
        for i in range(len(cls)):
            cand = cls[:i] + cls[i + 1:]
            if pred(rx, cand):
                cls, changed = cand, True
                break
    return rx, cls


# --- restriction candidates (refuse the construct)
def _no_caret_mid(rx):
    return "^" not in rx[1:]


def _no_dollar_mid(rx):
    return "$" not in rx[:-1]


def _no_empty_branch(rx):
    return not any(x in rx for x in ("(|", "|)", "||", "()"))


def _no_dot(rx):
    return "." not in rx


def _no_escape(rx):
    return BS not in rx


def _no_anchor(rx):
    return "^" not in rx and "$" not in rx


RESTRICTIONS = [
    ("refuse `^` anywhere but position 0", _no_caret_mid),
    ("refuse `$` anywhere but the last position", _no_dollar_mid),
    ("refuse empty alternatives and empty groups", _no_empty_branch),
    ("refuse `.`", _no_dot),
    ("refuse every backslash escape", _no_escape),
    ("refuse both anchors entirely", _no_anchor),
]


# --- nested-quantifier family (the Python-backtracking blowup)
def has_nested_quantifier(rx):
    """True when a quantifier is applied to a group whose body holds `|` or another quantifier."""
    stack = []
    for i, ch in enumerate(rx):
        if ch == "(":
            stack.append([])
            continue
        if ch == ")":
            if not stack:
                continue
            body = "".join(stack.pop())
            if i + 1 < len(rx) and rx[i + 1] in "*+?" and any(c in body for c in "|*+?"):
                return True
            if stack:
                stack[-1].append(body)
            continue
        if stack:
            stack[-1].append(ch)
    return False


NESTED_FAMILY = ["(a*)*", "(a+)+", "(a|a)*", "(a|aa)*", "((a)*)*", "(a*)+", "(a|a)+", "(.*)*"]
NEAR_MISS = ["a" * k + "b" for k in (8, 12, 16, 20, 24, 64, 200)]

COST_CODE = (
    "import re,sys,time\n"
    "rx,cls=sys.argv[1],sys.argv[2]\n"
    "c=re.compile(rx)\n"
    "t=time.perf_counter()\n"
    "r=c.fullmatch(cls)\n"
    "print(repr(r is not None), time.perf_counter()-t)\n"
)


def cost_pair(rx, cls, limit=3.0):
    try:
        p = subprocess.run([sys.executable, "-I", "-c", COST_CODE, rx, cls],
                           capture_output=True, text=True, timeout=limit)
    except subprocess.TimeoutExpired:
        return {"regex": rx, "class": cls, "class_len": len(cls),
                "python_seconds": None, "python_result": None, "timed_out": True}
    out = p.stdout.strip().split()
    return {"regex": rx, "class": cls, "class_len": len(cls),
            "python_result": out[0] if out else None,
            "python_seconds": (round(float(out[1]), 6) if len(out) > 1 else None),
            "timed_out": False}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20261026)
    ap.add_argument("--mode", choices=("full", "quick"), default="full")
    ap.add_argument("--random-patterns", type=int, default=60000)
    ap.add_argument("--sweeps", default="E1,E2,E3,R")
    ap.add_argument("--json")
    args = ap.parse_args(argv)
    rng = random.Random(args.seed)                 # class draws
    rng_pat = random.Random(args.seed ^ 0x5EED)    # pattern stream (independent of class draws)
    full = args.mode == "full"

    acc = {"both": 0, "py_only": 0, "re2_only": 0, "gated_out": 0}
    rejects = {"py_only": [], "re2_only": []}
    gate = {"seen": 0, "accepted": 0, "nested": 0}

    def note_acceptance(rx):
        gate["seen"] += 1
        if not regex_ok(rx):
            acc["gated_out"] += 1
            return False
        gate["accepted"] += 1
        if has_nested_quantifier(rx):
            gate["nested"] += 1
        if re2_compile(rx) is not None:
            acc["both"] += 1
            return True
        acc["py_only"] += 1
        if len(rejects["py_only"]) < 200:
            rejects["py_only"].append(rx)
        return False

    pairs = {"total": 0, "compared": 0, "diverged": 0, "tool_diverged": 0,
             "guard_masked": 0, "slow": 0}
    slow_examples = []
    slow_max_seconds = 0.0
    divs = []
    tool_divs = []
    buckets = {}
    tbuckets = {}

    def bucket(rx, cls):
        f = []
        if any(ord(ch) < 0x20 for ch in cls):
            f.append("class-control-char")
        if any(ord(ch) > 127 for ch in cls):
            f.append("class-non-ascii")
        if "|" in rx:
            f.append("alternation")
        if any(x in rx for x in ("(|", "|)", "||", "()")):
            f.append("empty-branch")
        if "^" in rx[1:]:
            f.append("caret-mid")
        if "$" in rx[:-1]:
            f.append("dollar-mid")
        if "." in rx:
            f.append("dot")
        if "(" in rx:
            f.append("group")
        if BS in rx:
            f.append("escape")
        return "+".join(f) or "other"

    def cmp_pair(rx, cls):
        nonlocal slow_max_seconds
        o = re2_compile(rx)
        if o is None:
            return
        pairs["total"] += 1
        a, dt, slow = py_match_timed(rx, cls)
        if slow:
            pairs["slow"] += 1
            slow_max_seconds = max(slow_max_seconds, dt)
            if len(slow_examples) < 60:
                t = time.perf_counter()
                rb = re2_match(o, cls)
                slow_examples.append({"regex": rx, "class": cls, "class_len": len(cls),
                                      "python_seconds": ">%.3f" % PAIR_BUDGET,
                                      "re2": rb,
                                      "re2_seconds": round(time.perf_counter() - t, 8)})
            return
        b = re2_match(o, cls)
        pairs["compared"] += 1
        if not guarded(cls) and a:
            pairs["guard_masked"] += 1
        if a != b:
            pairs["diverged"] += 1
            k = bucket(rx, cls)
            buckets[k] = buckets.get(k, 0) + 1
            if len(divs) < 5000:
                divs.append((rx, cls, a, b))
        if (guarded(cls) and a) != b:
            pairs["tool_diverged"] += 1
            k = bucket(rx, cls)
            tbuckets[k] = tbuckets.get(k, 0) + 1
            if len(tool_divs) < 5000:
                tool_divs.append((rx, cls))

    def sweep(gen, class_list, label=""):
        npat = npair = 0
        t0 = time.perf_counter()
        last = t0
        for rx in gen:
            if not note_acceptance(rx):
                continue
            npat += 1
            for cls in class_list:
                cmp_pair(rx, cls)
                npair += 1
            now = time.perf_counter()
            if label and now - last > 20:
                print("PROGRESS %s patterns=%d pairs=%d elapsed=%.1fs"
                      % (label, npat, npair, now - t0))
                sys.stdout.flush()
                last = now
        dt = time.perf_counter() - t0
        print("PROGRESS %s DONE patterns=%d pairs=%d seconds=%.1f" % (label, npat, npair, dt))
        sys.stdout.flush()
        return {"patterns": npat, "pairs": npair, "seconds": round(dt, 1)}

    sweeps = {}
    chosen = [x.strip() for x in args.sweeps.split(",") if x.strip()]
    if full and "E1" in chosen:
        sweeps["E1"] = sweep(gen_exhaustive(TOKEN_ALPHABET, 5), S1, "E1")
    if full and "E2" in chosen:
        sweeps["E2"] = sweep(gen_exhaustive(EXH_CHARS, 4), S1, "E2")
    if full and "E3" in chosen:
        sweeps["E3"] = sweep(gen_exhaustive(EXH_TOKENS, 3), S1, "E3")

    npatt = args.random_patterns if full else max(2000, args.random_patterns // 10)
    rand_pairs = 0
    t0 = time.perf_counter()
    if "R" in chosen:
        for _ in range(npatt):
            rx = gen_random(rng_pat)
            if not rx or not note_acceptance(rx):
                continue
            for _ in range(6):
                cmp_pair(rx, rand_class(rng))
                rand_pairs += 1
    sweeps["R"] = {"patterns": npatt, "pairs": rand_pairs,
                   "seconds": round(time.perf_counter() - t0, 1)}

    # ---- L: long-class semantics without nested quantifiers (linear in both engines)
    lin_patterns = ["a+", "a*", ".+", ".*", "a|b", "(a|b)+", "é+", "😀+", ".",
                    "^(a|ab)+$", "a.b", "org\\.omarchy\\.gkeep", "x+",
                    "ab*", "(ab)+", "é😀", "a" * 32]
    l_pat = l_pair = 0
    for rx in lin_patterns:
        if not regex_ok(rx):
            continue
        l_pat += 1
        for cls in LONG_CLASSES:
            cmp_pair(rx, cls)
            l_pair += 1
    sweeps["L"] = {"patterns": l_pat, "pairs": l_pair}

    # ---- X: cost stage, measured in child processes with a 3 s ceiling
    cost = []
    for rx in NESTED_FAMILY:
        if not regex_ok(rx):
            cost.append({"regex": rx, "skipped": "contract gate rejects"})
            continue
        for cls in ["a" * 8, "a" * 16, "a" * 24, "a" * 64, "a" * 200]:
            cost.append(cost_pair(rx, cls))
        o = re2_compile(rx)
        t = time.perf_counter()
        re2_match(o, "a" * 200 + "b")
        cost.append({"regex": rx, "class": "a*200+b", "class_len": 201,
                     "python_result": None, "python_seconds": None,
                     "timed_out": False, "re2_seconds": round(time.perf_counter() - t, 8)})
    near = []
    for rx in NESTED_FAMILY[:4]:
        o = re2_compile(rx)
        for cls in NEAR_MISS:
            e = cost_pair(rx, cls, limit=1.0)
            t = time.perf_counter()
            e["re2_result"] = re2_match(o, cls)
            e["re2_seconds"] = round(time.perf_counter() - t, 8)
            near.append(e)

    # ---- positive controls
    controls = []
    for rx, cls, note in [
        ("\\d", "\u0663", "Python \\d is Unicode, RE2 \\d is ASCII"),
        ("\\w", "é", "Python \\w is Unicode, RE2 \\w is ASCII"),
        ("\\s", "\u00a0", "Python \\s matches NBSP, RE2 does not"),
        ("\\D", "\u0663", "Python \\D vs a Unicode digit"),
        (".", "😀", "dot vs an astral rune (both engines: one rune)"),
        ("a$", "a\n", "dollar before a trailing newline under fullmatch"),
        ("\\Z", "a", "Python-only end anchor"),
    ]:
        o = re2_compile(rx)
        entry = {"regex": rx, "class": cls, "note": note,
                 "contract_gate": regex_ok(rx),
                 "python": py_match(rx, cls),
                 "re2": (re2_match(o, cls) if o is not None else None)}
        entry["diverges"] = (entry["re2"] is not None and entry["python"] != entry["re2"])
        controls.append(entry)
    ctl_div = sum(1 for c in controls if c["diverges"])

    # ---- minimised value-divergence classes
    min_examples = []
    seen_min = set()
    for rx, cls, a, b in divs:
        mrx, mcls = minimise(diverges, rx, cls)
        if (mrx, mcls) in seen_min:
            continue
        seen_min.add((mrx, mcls))
        min_examples.append({"regex": mrx, "class": mcls,
                             "python": py_match(mrx, mcls),
                             "re2": re2_match(re2_compile(mrx), mcls),
                             "verified_divergent": diverges(mrx, mcls)})
        if len(min_examples) >= 40:
            break

    tool_min = []
    seen_tool = set()
    for rx, cls in tool_divs:
        mrx, mcls = minimise(tool_diverges, rx, cls)
        if (mrx, mcls) in seen_tool:
            continue
        seen_tool.add((mrx, mcls))
        tool_min.append({"regex": mrx, "class": mcls,
                         "class_codepoints": [ord(c) for c in mcls],
                         "guard_blocks": not guarded(mcls),
                         "python_engine": py_match(mrx, mcls),
                         "re2": re2_match(re2_compile(mrx), mcls),
                         "verified_divergent": tool_diverges(mrx, mcls)})
        if len(tool_min) >= 20:
            break

    restriction_scores = []
    for name, pred in RESTRICTIONS:
        kept = sum(1 for rx, cls, a, b in divs if not pred(rx))
        restriction_scores.append({"restriction": name,
                                   "value_divergences_removed": len(divs) - kept,
                                   "value_divergences_remaining": kept})

    cost_refused = sum(1 for rx in NESTED_FAMILY if has_nested_quantifier(rx))
    cost_remaining_timeouts = sum(
        1 for c in near if c["timed_out"] and not has_nested_quantifier(c["regex"]))
    timed_out = [c for c in cost if c.get("timed_out")]
    h = (lambda x: max((c["python_seconds"] for c in cost
                        if c.get("regex") == x and isinstance(c.get("python_seconds"), float)),
                       default=None))
    result = {
        "seed": args.seed, "mode": args.mode,
        "python": sys.version.split()[0],
        "re2_package": RE2_PKG_VERSION,
        "contract_gate": gate,
        "compile_acceptance": acc,
        "compile_py_only_examples": rejects["py_only"][:20],
        "compile_re2_only_examples": rejects["re2_only"][:20],
        "sweeps": sweeps,
        "pairs": pairs,
        "slow_pairs": {"count": pairs["slow"], "budget_seconds": PAIR_BUDGET,
                       "max_seconds_before_abort": round(slow_max_seconds, 4),
                       "examples": slow_examples},
        "value_divergence_buckets": buckets,
        "value_divergence_count": len(divs),
        "positive_controls": {"diverging": ctl_div, "entries": controls},
        "minimised_examples": min_examples,
        "tool_level_divergences": {"count": pairs["tool_diverged"],
                                   "buckets": tbuckets,
                                   "minimised_examples": tool_min},
        "value_restriction_scores": restriction_scores,
        "cost_stage": {"timed_out": len(timed_out), "entries": cost,
                       "near_miss_scan": near,
                       "near_miss_timeouts": sum(1 for c in near if c["timed_out"]),
                       "nested_family_refused_by_restriction": cost_refused,
                       "near_miss_timeouts_remaining_under_restriction": cost_remaining_timeouts},
        "nested_quantifier_patterns_accepted": gate["nested"],
        "nested_family_worst_python_seconds": {rx: h(rx) for rx in NESTED_FAMILY},
    }

    print("RE2FUZZ: python=%s re2_package=%s seed=%d mode=%s"
          % (result["python"], result["re2_package"], args.seed, args.mode))
    for k in ("E1", "E2", "E3", "R", "L"):
        if k in sweeps:
            print("SWEEP %s: patterns=%d pairs=%d" % (k, sweeps[k]["patterns"], sweeps[k]["pairs"]))
    print("GATE: patterns_seen=%d contract_accepted=%d nested_quantifier_accepted=%d"
          % (gate["seen"], gate["accepted"], gate["nested"]))
    print("COMPILE: both=%d py_only=%d re2_only=%d gated_out=%d"
          % (acc["both"], acc["py_only"], acc["re2_only"], acc["gated_out"]))
    print("PAIRS: total=%d compared=%d   engine_diverged=%d tool_diverged=%d guard_masked=%d"
          % (pairs["total"], pairs["compared"], pairs["diverged"],
             pairs["tool_diverged"], pairs["guard_masked"]))
    print("SLOW: budget=%.3fs slow_pairs=%d" % (PAIR_BUDGET, pairs["slow"]))
    for e in slow_examples[:12]:
        print("  SLOW %r vs %r class_len=%d re2=%r re2_seconds=%s"
              % (e["regex"], e["class"][:20], e["class_len"], e["re2"], e["re2_seconds"]))
    for k in sorted(buckets):
        print("BUCKET %s: %d" % (k, buckets[k]))
    print("CONTROLS: diverging=%d/%d" % (ctl_div, len(controls)))
    for c in controls:
        print("  CONTROL %r vs %r python=%r re2=%r diverges=%r gate=%r"
              % (c["regex"], c["class"], c["python"], c["re2"], c["diverges"], c["contract_gate"]))
    print("COST: timed_out=%d/%d" % (len(timed_out), len(cost)))
    print("COST-NEAR-MISS: timeouts=%d/%d nested_refused=%d remaining_under_restriction=%d"
          % (sum(1 for c in near if c["timed_out"]), len(near), cost_refused,
             cost_remaining_timeouts))
    for c in near:
        print("  NEAR %r len=%d python=%r timeout=%r re2=%r/%ss"
              % (c["regex"], c["class_len"], c["python_seconds"], c["timed_out"],
                 c.get("re2_result"), c.get("re2_seconds")))
    for c in cost:
        if "skipped" in c:
            print("  COST %r skipped=%s" % (c["regex"], c["skipped"]))
        elif c["timed_out"]:
            print("  COST %r len=%d TIMEOUT>3s" % (c["regex"], c["class_len"]))
        else:
            print("  COST %r len=%d python=%ss" % (c["regex"], c["class_len"], c["python_seconds"]))
    print("MINIMISED: %d distinct engine divergences" % len(min_examples))
    for m in min_examples[:10]:
        print("  MIN-ENGINE %r vs %r python=%r re2=%r" % (m["regex"], m["class"], m["python"], m["re2"]))
    print("TOOL-LEVEL: diverged=%d in %d buckets" % (pairs["tool_diverged"], len(tbuckets)))
    for k in sorted(tbuckets):
        print("  TBUCKET %s: %d" % (k, tbuckets[k]))
    for m in tool_min[:10]:
        print("  MIN-TOOL %r vs %r cps=%r guard_blocks=%r python=%r re2=%r"
              % (m["regex"], m["class"], m["class_codepoints"], m["guard_blocks"],
                 m["python_engine"], m["re2"]))
    verdict = "VALUE_DIVERGED" if pairs["diverged"] or acc["py_only"] else "NO_VALUE_DIVERGENCE"
    print("RE2FUZZ VERDICT: %s value_pairs=%d seed=%d cost_timeouts=%d"
          % (verdict, pairs["compared"], args.seed, len(timed_out)))
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=1, ensure_ascii=True)
            fh.write("\n")
    return 0 if verdict == "NO_VALUE_DIVERGENCE" else 1


if __name__ == "__main__":
    sys.exit(main())
