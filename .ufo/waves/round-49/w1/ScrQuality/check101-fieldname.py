#!/usr/bin/env python3
"""check101-fieldname.py - candidate criterion 101 (a receipt field's name).

Question answered: does a `<name>=<value>` field whose name asserts a state
carry, in the same receipt, the comparator that establishes that state?

A state-asserting name is one whose tail token is in STATE_TOKENS, e.g.
`host_cache_untouched_sha256` (asserts: untouched), `probe_clean`,
`explain_absent`. The comparator that would establish it is one of:

  * a sibling field for the same stem carrying `before` (`host_cache_before_sha256`),
  * a line `before=<path|sha256=...>`,
  * the field name itself carrying `_before_` or `_after_`,
  * a `compared_with=<...>` / `reference_sha256=<...>` line in the same file.

With no comparator the field is FIELD_NAME_UNBACKED: it claims a state it does
not measure. `--payload` additionally re-derives a digest value against a
payload the receipt's own round is known to have written and prints
FIELD_VALUE_IS_PAYLOAD - the N2 shape, where `host_cache_untouched_sha256`
equalled sha256 of the mutant's 7 bytes `r48-w2\\n`.

Reads only; writes nothing.

Usage:
  check101-fieldname.py [--payload TEXT] [--payload-hex HEX] RECEIPT...
Exit: 0 no unbacked state field, 1 at least one, 2 usage / unreadable.

Declared limit: the token list is the vocabulary this lane's receipts use
today; a new state word (`pristine_at_capture`, `has_not_moved`) is not
detected until it is added. The instrument also cannot tell whether the
comparator is honest - it proves a comparator field exists, so a paired
before/after receipt is read, not trusted.
"""
import argparse
import hashlib
import re
import sys

STATE_TOKENS = (
    "untouched", "unchanged", "unmodified", "pristine", "clean",
    "readonly", "read_only", "no_write", "absent", "no_probe",
)
FIELD = re.compile(r'^([A-Za-z_][A-Za-z0-9_.-]*)=(.*)$')
COMPARATOR = re.compile(r'^(before|compared_with|reference_sha256|.*_before(_sha256)?)=', re.I)


def token_of(name):
    """A token at an underscore boundary anywhere in the name."""
    for token in STATE_TOKENS:
        if name == token or re.search(r"(^|_)%s(_|$)" % re.escape(token), name):
            return token
    return None


def stem_of(name, token):
    """Everything before the token, so a sibling's 'before' field can be found."""
    match = re.search(r"(^|_)%s(_|$)" % re.escape(token), name)
    return name[: match.start()] if match else name


def check(path, payload_digests, state):
    try:
        text = open(path, "r", errors="replace").read()
    except OSError as exc:
        print("CHECK101: error=receipt-unreadable %s: %s" % (path, exc))
        return 2
    lines = text.splitlines()
    names = set()
    for line in lines:
        match = FIELD.match(line.strip())
        if match:
            names.add(match.group(1))
    has_before_line = any(COMPARATOR.match(line.strip()) for line in lines)
    state_fields = 0
    for idx, line in enumerate(lines, 1):
        match = FIELD.match(line.strip())
        if not match:
            continue
        name, value = match.group(1), match.group(2)
        token = token_of(name)
        if not token:
            continue
        state_fields += 1
        stem = stem_of(name, token)
        comparator = has_before_line
        if not comparator:
            comparator = any(
                other != name and (stem and stem in other) and ("before" in other or "reference" in other)
                for other in names)
        print("STATE_FIELD %s:%d name=%s token=%s comparator=%s"
              % (path, idx, name, token, "present" if comparator else "none"))
        if not comparator:
            state["unbacked"] += 1
            print("FIELD_NAME_UNBACKED %s:%d name=%s" % (path, idx, name))
        if re.fullmatch(r'[0-9a-f]{64}', value) and value in payload_digests:
            state["payload"] += 1
            print("FIELD_VALUE_IS_PAYLOAD %s:%d name=%s sha256=%s" % (path, idx, name, value))
    print("RECEIPT: file=%s state_fields=%d" % (path, state_fields))
    return 0


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--payload")
    parser.add_argument("--payload-hex")
    parser.add_argument("receipts", nargs="+")
    args = parser.parse_args()
    payload_digests = set()
    if args.payload is not None:
        payload_digests.add(hashlib.sha256(args.payload.encode()).hexdigest())
    if args.payload_hex is not None:
        payload_digests.add(hashlib.sha256(bytes.fromhex(args.payload_hex)).hexdigest())
    state = {"unbacked": 0, "payload": 0}
    for path in args.receipts:
        if check(path, payload_digests, state):
            return 2
    print("CHECK101: receipts=%d unbacked=%d payload_matches=%d verdict=%s"
          % (len(args.receipts), state["unbacked"], state["payload"],
             "FAIL" if state["unbacked"] else "OK"))
    return 1 if state["unbacked"] else 0


if __name__ == "__main__":
    sys.exit(main())
