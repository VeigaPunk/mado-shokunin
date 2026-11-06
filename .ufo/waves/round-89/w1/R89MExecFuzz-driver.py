#!/usr/bin/env python3
"""R89MExecFuzz driver — differential test of the round-89 C1 candidate's POSIX ERE matcher
against the independent C oracle.

DRAFT tooling for mado round 89 (hyaku run 15, attempt 1). This is a case-set/implementation
check, NOT a measurement: it writes no receipts, and nothing here may be cited as a counter run.

What it does
------------
1. Imports the candidate (``build/mado-mako.c1.py``) by path with importlib (the file is read,
   never modified) and uses its three matcher entry points:

       posix_ere_compile(pattern) -> 256-byte ctypes buffer, or None when regcomp refuses
       posix_ere_search(compiled, text) -> bool (regexec(...,0,NULL,0) == 0)
       posix_ere_free(compiled)

   The candidate's verdict is therefore {match, nomatch, invalid}, exactly mako 1.11.0
   criteria.c's ``match_regex_criteria`` decision shape.
2. Generates a deterministic list of (pattern, text) pairs from a fixed seed. Patterns are built
   only from the seat-specified vocabulary ``a b é . * + ? | ( ) [ ] ^ $ { } \\ - :`` plus the
   three classes ``[[:alpha:]] [[:digit:]] [[:space:]]`` and a small set of templates that use the
   same vocabulary (anchors, alternation, bracket expressions, escapes). Texts are built from
   ``a b é``, the space and the digits.
3. Runs the oracle binary (``controls/posix-ere-oracle.c``: regcomp(REG_EXTENDED|REG_NOSUB) then
   regexec, never setlocale -> always the C locale) over every pair, passing pattern and text as
   explicit UTF-8 byte argv so no locale-dependent re-encoding stands between the two sides.
4. Compares candidate vs oracle and counts python ``re`` disagreements on the same pairs (the
   motivation figure: Python re is not POSIX ERE).
5. Minimises any candidate/oracle disagreement to a reproducing pair.

Exit status: 0 when the candidate agrees with the oracle on every pair; 1 when at least one
disagreement exists; 2 on a setup error.

Reproduce (S is this seat's scratch root; see the seat report):
    cc -O0 -o "$S/ore" .../controls/posix-ere-oracle.c
    LC_ALL=C          python3 R89MExecFuzz-driver.py --oracle "$S/ore" --candidate ... --out "$S/run-C.json"
    LC_ALL=C.UTF-8    python3 R89MExecFuzz-driver.py --oracle "$S/ore" --candidate ... --out "$S/run-C.UTF-8.json"
    LC_ALL=en_US.UTF-8 python3 R89MExecFuzz-driver.py --oracle "$S/ore" --candidate ... --out "$S/run-en_US.UTF-8.json"
"""

import argparse
import hashlib
import importlib.util
import json
import os
import random
import re
import subprocess
import sys
import warnings

# The candidate is imported from build/ (outside this seat's write scope): never let CPython drop
# a __pycache__ next to it or next to this driver.
sys.dont_write_bytecode = True

# --- vocabulary -----------------------------------------------------------------------------

ALPHABET = ["a", "b", "é", ".", "*", "+", "?", "|", "(", ")", "[", "]", "^", "$",
            "{", "}", "\\", "-", ":"]
CLASSES = ["[[:alpha:]]", "[[:digit:]]", "[[:space:]]"]
PATTERN_TOKENS = ALPHABET + CLASSES
TEXT_CHARS = ["a", "b", "é", " ", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

# Templates use only the same vocabulary; they raise the share of well-formed patterns so the
# comparison exercises match/nomatch as well as the invalid branch.
TEMPLATES = [
    "(a|b)*", "^(a|b)*$", "a|b", "(a|b)?", "a.*b", ".*é", "é|a", "^é$",
    "[ab]+", "[^ab]*", "[[:alpha:]]+", "[[:digit:]]*", "[[:space:]]?",
    "[[:alpha:]][[:digit:]]", "^$", "a$", "^a", "([[:alpha:]]|[[:space:]])+",
    "a\\*b", "\\.", "\\-", "\\", "a\\", "[]a]", "[^]a]", "a{", "}", "{",
    "[[:alpha:]]*[[:space:]]*$", "^[[:digit:]]+$", "(a|b|é)+", "a**b", "*a", "?a",
    "a|", "|a", "()", "[]", "[^]",
]


def make_pairs(seed, count):
    """Deterministic list of (pattern, text) pairs; the same seed yields the same list."""
    rng = random.Random(seed)
    pairs = []
    fixed_texts = ["", "a", "b", "ab", "é", " ", "0", "abc123", "a b", "éé", "aaaaaaaa", "0123456789"]
    while len(pairs) < count:
        roll = rng.randrange(100)
        if roll < 50:
            length = rng.randrange(0, 8)
            pattern = "".join(rng.choice(PATTERN_TOKENS) for _ in range(length))
        elif roll < 75:
            pattern = rng.choice(TEMPLATES)
        elif roll < 90:
            # bracket expression with a random inside, optionally quantified
            inner = "".join(rng.choice(["a", "b", "é", ".", "^", "-", ":", "*", "+", "?"])
                            for _ in range(rng.randrange(0, 4)))
            pattern = "[" + inner + "]" + rng.choice(["", "", "*", "+", "?"])
        else:
            # a literal run, optionally anchored/quantified
            run = "".join(rng.choice(["a", "b", "é"]) for _ in range(rng.randrange(0, 5)))
            pattern = rng.choice(["", "^"]) + run + rng.choice(["", "*", "+", "?", "$"])
        if rng.randrange(100) < 15:
            text = rng.choice(fixed_texts)
        else:
            text = "".join(rng.choice(TEXT_CHARS) for _ in range(rng.randrange(0, 9)))
        pairs.append((pattern, text))
    return pairs


# --- candidate -------------------------------------------------------------------------------

def import_candidate(path):
    spec = importlib.util.spec_from_file_location("mado_mako_candidate_r89", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot build an import spec for " + path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for name in ("posix_ere_compile", "posix_ere_search", "posix_ere_free"):
        if not callable(getattr(module, name, None)):
            raise RuntimeError("candidate lacks callable " + name)
    return module


def candidate_verdict(module, pattern, text):
    compiled = module.posix_ere_compile(pattern)
    if compiled is None:
        return "invalid"
    try:
        return "match" if module.posix_ere_search(compiled, text) else "nomatch"
    finally:
        module.posix_ere_free(compiled)


# --- oracle ----------------------------------------------------------------------------------

def oracle_verdict(oracle, pattern, text):
    proc = subprocess.run([oracle, pattern.encode("utf-8"), text.encode("utf-8")],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    if proc.returncode != 0:
        raise RuntimeError("oracle exit " + str(proc.returncode) + " for "
                           + repr(pattern) + " " + repr(text) + ": "
                           + proc.stderr.decode("utf-8", "replace"))
    return proc.stdout.decode("ascii").strip()


# --- python re control -----------------------------------------------------------------------

def python_re_verdict(pattern, text):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            compiled = re.compile(pattern)
        except (re.error, OverflowError) as exc:
            return "invalid", type(exc).__name__ + ": " + str(exc)
        return ("match" if compiled.search(text) else "nomatch"), None


# --- minimisation ----------------------------------------------------------------------------

def minimise(pattern, text, disagrees):
    """Greedily delete characters while the two sides still disagree."""
    changed = True
    while changed:
        changed = False
        for i in range(len(pattern)):
            cand = pattern[:i] + pattern[i + 1:]
            if disagrees(cand, text):
                pattern = cand
                changed = True
                break
        if changed:
            continue
        for i in range(len(text)):
            cand = text[:i] + text[i + 1:]
            if disagrees(pattern, cand):
                text = cand
                changed = True
                break
    return pattern, text


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main(argv):
    parser = argparse.ArgumentParser(prog="R89MExecFuzz-driver.py")
    parser.add_argument("--oracle", required=True, help="compiled posix-ere-oracle binary")
    parser.add_argument("--candidate", required=True, help="mado-mako c1 candidate .py")
    parser.add_argument("--pairs", type=int, default=3200)
    parser.add_argument("--seed", type=int, default=89151006)
    parser.add_argument("--out", required=True, help="JSON result path (scratch only)")
    parser.add_argument("--label", default="")
    args = parser.parse_args(argv)

    if args.pairs < 3000:
        print("setup error: --pairs must be >= 3000 (seat requirement)", file=sys.stderr)
        return 2
    for path in (args.oracle, args.candidate):
        if not os.path.isfile(path):
            print("setup error: missing " + path, file=sys.stderr)
            return 2
    if not os.access(args.oracle, os.X_OK):
        print("setup error: not executable: " + args.oracle, file=sys.stderr)
        return 2

    pairs = make_pairs(args.seed, args.pairs)
    module = import_candidate(args.candidate)

    oracle_counts = {"match": 0, "nomatch": 0, "invalid": 0}
    candidate_disagreements = []
    python_re_disagreements = []
    python_re_errors = 0

    cache = {}
    for pattern, text in pairs:
        key = (pattern, text)
        oracle = cache.get(key)
        if oracle is None:
            oracle = oracle_verdict(args.oracle, pattern, text)
            cache[key] = oracle
        oracle_counts[oracle] += 1

        have = candidate_verdict(module, pattern, text)
        if have != oracle:
            candidate_disagreements.append({"pattern": pattern, "text": text,
                                            "oracle": oracle, "candidate": have})

        py, py_error = python_re_verdict(pattern, text)
        if py_error is not None:
            python_re_errors += 1
        if py != oracle:
            python_re_disagreements.append({"pattern": pattern, "text": text,
                                            "oracle": oracle, "python_re": py,
                                            "python_re_error": py_error})

    minimised = []
    for item in candidate_disagreements[:10]:
        pattern, text = minimise(
            item["pattern"], item["text"],
            lambda p, t: candidate_verdict(module, p, t) != oracle_verdict(args.oracle, p, t))
        minimised.append({"pattern": pattern, "text": text,
                          "oracle": oracle_verdict(args.oracle, pattern, text),
                          "candidate": candidate_verdict(module, pattern, text)})

    result = {
        "label": args.label,
        "driver": os.path.realpath(__file__),
        "seed": args.seed,
        "pairs": len(pairs),
        "oracle": os.path.realpath(args.oracle),
        "oracle_sha256": sha256_file(args.oracle),
        "candidate": os.path.realpath(args.candidate),
        "candidate_sha256": sha256_file(args.candidate),
        "environment": {name: os.environ.get(name) for name in ("LC_ALL", "LANG", "LC_CTYPE")},
        "python": sys.version.split()[0],
        "oracle_counts": oracle_counts,
        "candidate_disagreement_count": len(candidate_disagreements),
        "candidate_first_disagreements": candidate_disagreements[:10],
        "candidate_minimised": minimised,
        "python_re_disagreement_count": len(python_re_disagreements),
        "python_re_compile_errors": python_re_errors,
        "python_re_first_disagreements": python_re_disagreements[:10],
    }
    with open(args.out, "w", encoding="utf-8") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=1, sort_keys=True)
        handle.write("\n")

    print(json.dumps({
        "label": args.label, "seed": args.seed, "pairs": len(pairs),
        "env": result["environment"],
        "oracle_counts": oracle_counts,
        "candidate_disagreements": len(candidate_disagreements),
        "python_re_disagreements": len(python_re_disagreements),
    }, ensure_ascii=False, sort_keys=True))
    return 0 if not candidate_disagreements else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
