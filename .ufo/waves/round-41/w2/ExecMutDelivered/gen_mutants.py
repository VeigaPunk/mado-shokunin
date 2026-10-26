#!/usr/bin/env python3
"""Generate NEW single-edit mutants of the delivered v2 tool (round 41, w2).

Base text: tools/mado-globals.py at DATA commit 07f2641696b5ac73de1404ea737a9f27e9819aa1
(byte-identical to .ufo/waves/round-41/c1/ctl-ref-tool-v2.py.txt, sha256
286c051f648f24b23475a893d386f5366b91df00b7e87924bc212c8bf797f55e).

Every entry is one contiguous textual replacement. The set is written to be
novel against (a) ctl/run-c1-v2-controls.py (M01-M39, C1-C4, K01-K12),
(b) w1/ExecC1ExtraMutants/gen_mutants.py (N01-N43), and (c) w1/
MutSelftestFixtures/matrix.md (495-site sweep of the v1 reference) — the
latter two were made against the v1 reference text, so exact duplicates are
impossible for the v2-only regions; the pairwise (old,new) check against (a)
and (b) is mechanical.

Usage: python3 gen_mutants.py [--ref PATH] [--out DIR]
"""
import argparse
import os

MUTANTS = [
    # --- regex / grammar value domains (fixtures never exercise these)
    ("M100-ver-zero-rejected",
     r'\(ver ([0-9]{1,6})\)',
     r'\(ver ([1-9][0-9]{0,5})\)'),
    ("M101-ts-minus-only",
     r'T[0-9]{2}:[0-9]{2}:[0-9]{2}[+-][0-9]{2}:[0-9]{2})',
     r'T[0-9]{2}:[0-9]{2}:[0-9]{2}-[0-9]{2}:[0-9]{2})'),
    ("M102-year-locked-2026",
     r'([0-9]{4}-[0-9]{2}-[0-9]{2}T',
     r'(2026-[0-9]{2}-[0-9]{2}T'),
    ("M103-host-spaces-allowed",
     r'[0-9]{2}:[0-9]{2}) (\S+) ',
     r'[0-9]{2}:[0-9]{2}) (.+) '),
    ("M104-level-warning-accepted",
     r'\[LOG\]  \| "',
     r'\[(?:LOG|WARNING)\]  \| "'),
    ("M105-boot-33hex",
     r'-- Boot ([0-9a-f]{32}) --',
     r'-- Boot ([0-9a-f]{32,33}) --'),
    ("M116-ts-fractional-seconds",
     r':[0-9]{2}:[0-9]{2}[+-][0-9]{2}:[0-9]{2})',
     r':[0-9]{2}:[0-9]{2}(?:\.\d+)?[+-][0-9]{2}:[0-9]{2})'),
    ("M117-name-dot-allowed",
     r'Got interface: ([A-Za-z0-9_]{1,128}) \(ver ([0-9]{1,6})\)',
     r'Got interface: ([A-Za-z0-9_.]{1,128}) \(ver ([0-9]{1,6})\)'),
    ("M135-month-validator",
     r'[0-9]{2}-[0-9]{2}T',
     r'(?:0[1-9]|1[0-2])-[0-9]{2}T'),
    ("M145-host-length-cap128",
     r'(\S+) ',
     r'(\S{1,128}) '),
    ("M146-pid-length-cap7",
     r'\[([0-9]+)\]: \[LOG\]',
     r'\[([0-9]{1,7})\]: \[LOG\]'),
    # --- report / diff value domains
    ("M106-diff-added-empty-X",
     '",".join(added) or "-",',
     '",".join(added) or "X",'),
    ("M107-diff-removed-empty-X",
     '",".join(removed) or "-",',
     '",".join(removed) or "X",'),
    ("M120-diff-added-unsorted",
     'added = sorted(set(b) - set(a))',
     'added = list(set(b) - set(a))'),
    ("M121-diff-removed-unsorted",
     'removed = sorted(set(a) - set(b))',
     'removed = list(set(a) - set(b))'),
    ("M133-diff-none-line-text",
     '"MADO_GLOBALS_DIFF: sessions=%d none" % len(sessions))',
     '"MADO_GLOBALS_DIFF: sessions=%d nope" % len(sessions))'),
    # --- parse mechanics
    ("M108-ignored-counts-twice",
     'ignored += 1',
     'ignored += 2'),
    ("M109-ver-min-not-max",
     'ent[1] = max(ent[1], ver)',
     'ent[1] = min(ent[1], ver)'),
    ("M110-name-count-adds-two",
     'ent[0] += 1',
     'ent[0] += 2'),
    ("M122-unit-loosened-plus",
     r'xdg-desktop-portal-hyprland\[([0-9]+)\]:',
     r'[A-Za-z0-9_-]+\[([0-9]+)\]:'),
    ("M123-verdict-unrec-overrides",
     'if not sessions and ignored > 0:',
     'if ignored > 0:'),
    ("M126-session-init-adverts-one",
     '"adverts": 0,',
     '"adverts": 1,'),
    ("M127-guard-raw-compare",
     'if bool(args.journal_file) == bool(args.live):',
     'if args.journal_file == args.live:'),
    ("M129-global-line-column-swap",
     '"MADO_GLOBAL: name=%s ver=%d count=%d class=%s"',
     '"MADO_GLOBAL: name=%s count=%d ver=%d class=%s"'),
    ("M134-last-first-column-swap",
     's["first"], s["last"],',
     's["last"], s["first"],'),
    ("M136-summary-ignore-position",
     'expected_missing=%s ignored=%d verdict=%s"',
     'ignored=%d expected_missing=%s verdict=%s"'),
    ("M132-expect-dups-not-deduped",
     'sorted(set(args.expect))',
     'sorted(args.expect)'),
    # --- input reading / live plumbing
    ("M111-live-too-large-ge",
     'if total > MAX_BYTES:',
     'if total >= MAX_BYTES:'),
    ("M112-read-chunk-2MiB",
     'block = os.read(fd, 1 << 20)',
     'block = os.read(fd, 1 << 21)'),
    ("M118-open-nonblock-drop",
     'os.O_RDONLY | os.O_NONBLOCK',
     'os.O_RDONLY'),
    ("M119-loop-lt-maxbytes",
     'while len(data) <= MAX_BYTES:',
     'while len(data) < MAX_BYTES:'),
    ("M124-maxbytes-9MiB",
     'MAX_BYTES = 8 * 1024 * 1024',
     'MAX_BYTES = 9 * 1024 * 1024'),
    ("M128-unit-flag-longform",
     '["--user", "-u", "xdg-desktop-portal-hyprland", "--no-pager",',
     '["--user", "--unit", "xdg-desktop-portal-hyprland", "--no-pager",'),
    ("M130-ignoree-short-iso",
     '"-o", "short-iso"]',
     '"-o", "short-iso", "-e"]'),
    ("M131-stderr-pipe",
     'stderr=subprocess.DEVNULL,',
     'stderr=subprocess.PIPE,'),
    ("M144-live-timeout-zero",
     'MAX_BYTES = 8 * 1024 * 1024\nLIVE_TIMEOUT = 30\n',
     'MAX_BYTES = 8 * 1024 * 1024\nLIVE_TIMEOUT = 0\n'),
    ("M149-live-failed-reason-text",
     'reason = "journalctl_failed"',
     'reason = "journalctl_timeout"'),
    ("M150-live-too-large-reason",
     'reason = "journalctl_too_large"',
     'reason = "journalctl_huge"'),
    ("M160-argv-order-reversed",
     '["--user", "-u", "xdg-desktop-portal-hyprland", "--no-pager",',
     '["--user", "-u", "xdg-desktop-portal-hyprland", "-o", "short-iso",\n'
     '                   "--no-pager",'),
    # --- exit / setup codes
    ("M125-usage-exit-3",
     '        raise Setup("usage")\n    if bool(args.journal_file) == bool(args.live):',
     '        raise Setup("usage", 3)\n    if bool(args.journal_file) == bool(args.live):'),
    ("M148-toolarge-exit-3",
     'raise Setup("too_large")',
     'raise Setup("too_large", 3)'),
    ("M151-badexpect-exit-3",
     'raise Setup("bad_expect")',
     'raise Setup("bad_expect", 3)'),
    ("M152-unrec-verdict-exit-3",
     'verdict, code = "UNRECOGNIZED_FORMAT", 4',
     'verdict, code = "UNRECOGNIZED_FORMAT", 3'),
    ("M153-ok-verdict-exit-1",
     'verdict, code = "OK", 0',
     'verdict, code = "OK", 1'),
    ("M147-os-exit",
     'sys.exit(main())',
     'os._exit(main())'),
    # --- selftest machinery / integrity
    ("M113-selftest-ok-always",
     'ok += bool(cond)',
     'ok += 1'),
    ("M114-selftest-return-flat",
     'return 0 if ok == n else 1',
     'return 0'),
    ("M115-selftest-n-twice",
     'n += 1',
     'n += 2'),
    ("M137-selftest-timeout-reset-drop",
     '        LIVE_TIMEOUT = 30\n',
     ''),
    ("M143-selftest-ts-literal-change",
     'ts = "2026-10-25T13:36:24-03:00"',
     'ts = "2026-10-25T13:36:24+03:00"'),
    ("M154-selftest-check-cond-negate",
     'check(len(s) == 1 and s[0]["adverts"] == 3 and ig == 0)',
     'check(not (len(s) == 1 and s[0]["adverts"] == 3 and ig == 0))'),
    # --- selftest probe deletions (single-statement removals)
    ("M138-selftest-drop-ver10-probe",
     '    check(parse((fmt % ("11", "wl_seat", 9) + fmt % ("11", "wl_seat", 10)).encode())[0][0]["names"]["wl_seat"] == [2, 10])\n',
     ''),
    ("M139-selftest-drop-128-probe",
     '    check(parse(data.replace(b"wl_seat", b"a" * 129))[0] != parse(data.replace(b"wl_seat", b"a" * 128))[0])\n',
     ''),
    ("M140-selftest-drop-names-probe",
     '    check(s[0]["names"]["wl_seat"] == [2, 9])\n',
     ''),
    ("M141-selftest-drop-adverts-probe",
     '    check(len(s) == 1 and s[0]["adverts"] == 3 and ig == 0)\n',
     ''),
    ("M142-selftest-drop-bootsplit-probe",
     '    check(len(parse(b1 + (fmt % ("11", "wl_seat", 9)).encode() + b1\n                    + (fmt % ("11", "wl_seat", 9)).encode())[0]) == 2)\n',
     ''),
    ("M158-selftest-drop-usage-probes",
     '        check(code_of(run, ["--journal-file", jf, "--live"]) == "usage:2")\n',
     ''),
    ("M155-selftest-drop-upperclass-probe",
     '    check(classify("HYPRLAND_FOCUS_GRAB_MANAGER_V1") == "other")\n',
     ''),
    ("M156-selftest-drop-sandbox-probe",
     '    check(classify("wp_security_context_manager_v1") == "sandbox")\n',
     ''),
    ("M157-selftest-drop-classof-probe",
     '    check(len(CLASS_OF) == sum(len(v) for v in CLASSES.values()))\n',
     ''),
    ("M159-selftest-drop-gw-probe",
     '        check(code_of(resolve_program, stub("gw", "#!/bin/sh\\n", 0o775))\n'
     '              == "journalctl_unusable:5")\n',
     ''),
    ("M161-selftest-drop-ignored-probe",
     '    check(parse(data.replace(b"[LOG]  |", b"[LOG] |")) == ([], 3))\n',
     ''),
    ("M162-selftest-drop-verint-probe",
     '    check(parse(data.replace(b"(ver 5)", b"(ver 123456)"))[0][0]["adverts"] == 3)\n',
     ''),
    ("M163-selftest-drop-diffnone-probe",
     '    check("MADO_GLOBALS_DIFF: sessions=1 none" in lines)\n',
     ''),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default="/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-41/c1/ctl-ref-tool-v2.py.txt")
    ap.add_argument("--out", default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "mutants"))
    args = ap.parse_args()
    ref = open(args.ref, encoding="utf-8").read()
    os.makedirs(args.out, exist_ok=True)
    names = set()
    bad = 0
    for name, old, new in MUTANTS:
        if name in names:
            print("DUP name %s" % name)
            bad += 1
        names.add(name)
        if ref.count(old) != 1:
            print("ABSENT/AMBIGUOUS %s count=%d" % (name, ref.count(old)))
            bad += 1
            continue
        src = ref.replace(old, new, 1)
        if src == ref:
            print("NOOP %s" % name)
            bad += 1
            continue
        with open(os.path.join(args.out, name + ".py"), "w",
                  encoding="utf-8") as fh:
            fh.write(src)
        print("WROTE %s" % name)
    print("MUTANTS total=%d bad=%d" % (len(MUTANTS), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
