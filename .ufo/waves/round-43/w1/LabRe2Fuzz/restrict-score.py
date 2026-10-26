#!/usr/bin/env python3
"""restrict-score.py - scores candidate contract restrictions for the two divergences the
`re2fuzz.py` sweep reports, on the same pattern population and the same seed.

Two divergence classes measured by `re2fuzz.py`:
  (1) tool-level, by contract design: the contract's client predicate is
      `no character below U+0020 AND re.fullmatch(...)`, while Hyprland runs
      `RE2::FullMatch` on the raw class; for classes holding a control character the tool
      declines a rule the compositor would apply.
  (2) engine cost: `re.fullmatch` is a backtracking engine. A contract-accepted regex such as
      `(a*)*` applied to a near-miss class ("a"*24 + "b") is exponential in Python and linear
      in RE2, so the tool does not terminate where Hyprland answers at once.

This script does not re-run the match sweeps. It regenerates the same accepted pattern
population (E1, E2, E3, and the R generator with the same seed) with `re2fuzz.py`'s own
generators and gate, then counts for each candidate restriction
  * how many accepted patterns it refuses (the price of the restriction),
  * which cost-family patterns it refuses,
  * how many near-miss timeouts remain when the cost stage is re-run with it applied.

Candidates
  R1  refuse a quantifier applied to a group whose body contains `*`, `+` or `?`
  R2  refuse a quantifier applied to any group containing `|`
  R3  R1, plus refuse a quantifier applied to a group with two identical `|`-branches
  R5  R1, plus refuse a quantifier applied to a group with two branches that share a first
      character (the ambiguous-alternation family: `(a|a)*`, `(a|aa)*`, `(a|ab)+`)
  R4  refuse every quantified group (over-broad baseline)
"""
import argparse
import random
import sys

import re2fuzz as F


def _groups(rx):
    """Yield (open_index, close_index, body) for every parenthesised group."""
    stack = []
    for i, ch in enumerate(rx):
        if ch == "(":
            stack.append(i)
        elif ch == ")" and stack:
            j = stack.pop()
            yield j, i, rx[j + 1:i]


def _quantified(rx, j, i):
    return i + 1 < len(rx) and rx[i + 1] in "*+?"


def r1(rx):
    for j, i, body in _groups(rx):
        if _quantified(rx, j, i) and any(c in body for c in "*+?"):
            return True
    return False


def r2(rx):
    for j, i, body in _groups(rx):
        if _quantified(rx, j, i) and "|" in body:
            return True
    return False


def _branches(body):
    depth, cur, out = 0, [], []
    for ch in body:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "|" and depth == 0:
            out.append("".join(cur))
            cur = []
            continue
        cur.append(ch)
    out.append("".join(cur))
    return out


def r3(rx):
    for j, i, body in _groups(rx):
        if not _quantified(rx, j, i):
            continue
        if any(c in body for c in "*+?"):
            return True
        br = _branches(body)
        if len(br) != len(set(br)):
            return True
    return False


def _first_char(branch):
    for ch in branch:
        if ch not in "^":
            return ch
    return ""


def r5(rx):
    for j, i, body in _groups(rx):
        if not _quantified(rx, j, i):
            continue
        if any(c in body for c in "*+?"):
            return True
        br = _branches(body)
        if len(br) != len(set(br)):
            return True
        heads = [_first_char(b) for b in br]
        if len(heads) != len(set(heads)):
            return True
    return False


def r4(rx):
    return any(_quantified(rx, j, i) for j, i, _ in _groups(rx))


RESTRICTIONS = [("R1 nested quantifier", r1),
                ("R2 quantified alternation", r2),
                ("R3 nested+duplicate-branch", r3),
                ("R5 nested+same-first-char branch", r5),
                ("R4 any quantified group", r4)]

REF_SELFTEST_REGEXES = ["^(a|b)+\\.c$", "^(org.omarchy.gkeep)$", "org\\.omarchy\\..*",
                        "Alacritty|kitty", "a", "a|ab", ".*", "a\\.b", "^(a|ab)$",
                        "(x y)?", "x.y", "firefox+", "org.a.b", "\\(a\\)", "a?b?", "k.*y", "^$"]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20261026)
    ap.add_argument("--random-patterns", type=int, default=60000)
    ap.add_argument("--mode", choices=("full", "quick"), default="full")
    ap.add_argument("--slow-json", help="result.json of a re2fuzz run; score the restrictions "
                                        "against the slow pairs it recorded")
    args = ap.parse_args(argv)
    full = args.mode == "full"

    accepted = 0
    hits = {name: 0 for name, _ in RESTRICTIONS}
    sources = []

    def consider(rx):
        nonlocal accepted
        if not rx or not F.regex_ok(rx):
            return
        accepted += 1
        for name, pred in RESTRICTIONS:
            if pred(rx):
                hits[name] += 1

    if full:
        for gen in (F.gen_exhaustive(F.TOKEN_ALPHABET, 5),
                    F.gen_exhaustive(F.EXH_CHARS, 4),
                    F.gen_exhaustive(F.EXH_TOKENS, 3)):
            n = 0
            for rx in gen:
                consider(rx)
                n += 1
            sources.append(n)
    rng = random.Random(args.seed ^ 0x5EED)
    n = 0
    for _ in range(args.random_patterns if full else max(2000, args.random_patterns // 10)):
        consider(F.gen_random(rng))
        n += 1
    sources.append(n)

    print("POPULATION: accepted=%d exhaustive_candidates=%s random_candidates=%d seed=%d"
          % (accepted, sources[:-1], sources[-1], args.seed))
    for name, _ in RESTRICTIONS:
        print("RESTRICT %-28s refuses=%d (%.2f%% of accepted)"
              % (name, hits[name], 100.0 * hits[name] / accepted if accepted else 0.0))

    print("COST-FAMILY: patterns=%d" % len(F.NESTED_FAMILY))
    for name, pred in RESTRICTIONS:
        refused = [rx for rx in F.NESTED_FAMILY if pred(rx)]
        left = [rx for rx in F.NESTED_FAMILY if not pred(rx)]
        print("  %-28s refuses=%d leaves=%r" % (name, len(refused), left))

    print("REFERENCE-SELFTEST: %d regexes" % len(REF_SELFTEST_REGEXES))
    for name, pred in RESTRICTIONS:
        bad = [rx for rx in REF_SELFTEST_REGEXES if F.regex_ok(rx) and pred(rx)]
        print("  %-28s refuses=%r" % (name, bad))

    if args.slow_json:
        import json
        with open(args.slow_json, encoding="utf-8") as fh:
            doc = json.load(fh)
        ex = doc.get("slow_pairs", {}).get("examples", [])
        print("SLOW-PAIRS from %s: recorded=%d of total=%d"
              % (args.slow_json, len(ex), doc.get("slow_pairs", {}).get("count")))
        for name, pred in RESTRICTIONS:
            kept = [e for e in ex if not pred(e["regex"])]
            print("  %-40s refuses=%d/%d leaves=%r"
                  % (name, len(ex) - len(kept), len(ex),
                     [e["regex"][:40] for e in kept[:3]]))

    print("NEAR-MISS re-run under each restriction (limit 1.0 s per pair):")
    for name, pred in RESTRICTIONS:
        allowed = [rx for rx in F.NESTED_FAMILY[:4] if not pred(rx)]
        to = 0
        ran = 0
        for rx in allowed:
            for cls in F.NEAR_MISS:
                e = F.cost_pair(rx, cls, limit=1.0)
                ran += 1
                to += 1 if e["timed_out"] else 0
        print("  %-28s patterns=%d pairs=%d timeouts=%d" % (name, len(allowed), ran, to))
    return 0


if __name__ == "__main__":
    sys.exit(main())
