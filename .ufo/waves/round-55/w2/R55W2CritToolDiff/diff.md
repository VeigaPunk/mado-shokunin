# R55W2CritToolDiff: differential test, tools/mado-kbdopts.py vs independent oracle

Seat: R55W2CritToolDiff (leaf, falsify wave w2). Contract: registration.md §C2 + registration-v2.md E7.

Generator: `gen_diff.py` (embedded in Appendix A). Oracle: `oracle.py` (embedded in Appendix B), written from the
contract text before the tool source was opened. Python 3.14.8 (`python3 -I`). Tool run as
`python3 -I tools/mado-kbdopts.py <argv>` with cwd = a private per-case directory holding only the input files.
Comparison: stdout bytes and exit code, exact.

## Volume

| run | inputs | setup-failures (oracle) | divergent | tool timeouts |
|---|---|---|---|---|
| `final-clean-adv` (clean profile, adversarial grammar soup, seed 55, n=3400) | 3443 | 563 | 29 | 0 |
| `final-clean-valid` (clean profile, mostly-valid device/global structure, seed 56, n=1200) | 1243 | 199 | 11 | 0 |
| `final-ambig-adv` (ambig profile (keeps control-char names and ws-only getoption lines), seed 57, n=1000) | 1043 | 270 | 145 | 0 |

Total inputs: 5729. Random generated configs: 3400 + 1200 + 1000 = 5600 (each run also includes 43 deterministic edge cases). Directed battery: 71 more (run separately).

## Coverage (oracle-side, per run; counts of inputs that reached the grammar)

- `final-clean-adv`: ok=2880 setup=563; device-scoped value reached output (from=D) 12; global (from=G) 232; unsupported>0 1400; numlock=1 13; live AGREE/DIFFER/UNKNOWN 66/456/1185.
- `final-clean-valid`: ok=1044 setup=199; device-scoped value reached output (from=D) 122; global (from=G) 329; unsupported>0 840; numlock=1 122; live AGREE/DIFFER/UNKNOWN 20/153/400.
- `final-ambig-adv`: ok=773 setup=270; device-scoped value reached output (from=D) 10; global (from=G) 59; unsupported>0 329; numlock=1 4; live AGREE/DIFFER/UNKNOWN 9/93/236.

## Divergences (minimised, deduplicated by minimal input)

Classes: `CTL-NAME` = tool rejects a `--keyboard` NAME containing an ASCII control character with `SETUP usage`; `GO-FF-STRIP` = a getoption line whose JSON is followed by a form feed or vertical tab (tool strips them, oracle rejects); `GO-WS-ONLY` = a getoption line that is whitespace only (tool skips it as empty, oracle rejects it as bad JSON). `OTHER` would need manual classification and there are none.

Occurrences: CTL-NAME=60, GO-FF-STRIP=45, GO-WS-ONLY=80.

### D01 [CTL-NAME] seen in 12 input(s), e.g. `final-ambig-adv:ambig-adv-R00011`

- argv: `["--keyboard", "tab\tname", "--config", "c0.conf"]`
- file `c0.conf` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=tab\tname repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: DONE keyboards=1 unsupported=0 live=NONE\n'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D02 [CTL-NAME] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00025`

- argv: `["--keyboard", "tab\tname", "--config", "c0.conf", "--config", "c1.conf"]`
- file `c0.conf` (0 bytes): `b''`
- file `c1.conf` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=tab\tname repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: DONE keyboards=1 unsupported=0 live=NONE\n'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D03 [CTL-NAME] seen in 14 input(s), e.g. `final-ambig-adv:ambig-adv-R00051`

- argv: `["--config", "c0.conf", "--keyboard", "tab\tname"]`
- file `c0.conf` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=tab\tname repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: DONE keyboards=1 unsupported=0 live=NONE\n'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D04 [CTL-NAME] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00070`

- argv: `["--keyboard", "tab\tname", "--keyboard", "##", "--config", "c0.conf"]`
- file `c0.conf` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=tab\tname repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: keyboard=## repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOP'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D05 [CTL-NAME] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00213`

- argv: `["--config", "c1.conf", "--keyboard", "tab\tname", "--keyboard", "\u00e9"]`
- file `c1.conf` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=tab\tname repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: keyboard=é repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D06 [CTL-NAME] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00269`

- argv: `["--keyboard", "=", "--config", "c0.conf", "--keyboard", "tab\tname"]`
- file `c0.conf` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard== repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: keyboard=tab\tname repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D07 [CTL-NAME] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00364`

- argv: `["--keyboard", "tab\tname", "--keyboard", "a=b", "--config", "c0.conf"]`
- file `c0.conf` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=tab\tname repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: keyboard=a=b repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDO'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D08 [CTL-NAME] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00384`

- argv: `["--keyboard", "tab\tname", "--keyboard", "My Keyboard", "--config", "c1.conf"]`
- file `c1.conf` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=tab\tname repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: keyboard=My Keyboard repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nM'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D09 [CTL-NAME] seen in 2 input(s), e.g. `final-ambig-adv:ambig-adv-R00421`

- argv: `["--keyboard", "tab\tname", "--config", "c2.conf"]`
- file `c2.conf` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=tab\tname repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: DONE keyboards=1 unsupported=0 live=NONE\n'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D10 [CTL-NAME] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00458`

- argv: `["--config", "c2.conf", "--config", "c0.conf", "--keyboard", "tab\tname"]`
- file `c0.conf` (0 bytes): `b''`
- file `c2.conf` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=tab\tname repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: DONE keyboards=1 unsupported=0 live=NONE\n'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D11 [CTL-NAME] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00489`

- argv: `["--keyboard", "k\"q\"", "--keyboard", "tab\tname", "--getoption", "go.json", "--keyboard", "k\"q\"", "--config", "c0.conf", "--config", "c1.conf"]`
- file `c0.conf` (0 bytes): `b''`
- file `c1.conf` (0 bytes): `b''`
- file `go.json` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=k"q" repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: keyboard=tab\tname repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBD'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D12 [CTL-NAME] seen in 2 input(s), e.g. `final-ambig-adv:ambig-adv-R00534`

- argv: `["--keyboard", "tab\tname", "--config", "c0.conf", "--getoption", "go.json"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=tab\tname repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=i'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D13 [CTL-NAME] seen in 2 input(s), e.g. `final-ambig-adv:ambig-adv-R00586`

- argv: `["--keyboard", "tab\tname", "--config", "c1.conf"]`
- file `c1.conf` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=tab\tname repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: DONE keyboards=1 unsupported=0 live=NONE\n'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D14 [CTL-NAME] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00602`

- argv: `["--keyboard", "tab\tname", "--keyboard", "kb#1", "--config", "c0.conf"]`
- file `c0.conf` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=tab\tname repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: keyboard=kb#1 repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBD'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D15 [CTL-NAME] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00651`

- argv: `["--keyboard", "Mouse 1", "--config", "c0.conf", "--keyboard", "tab\tname"]`
- file `c0.conf` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=Mouse 1 repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: keyboard=tab\tname repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D16 [CTL-NAME] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00657`

- argv: `["--config", "c0.conf", "--keyboard", "tab\tname", "--getoption", "go.json"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=tab\tname repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=i'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D17 [CTL-NAME] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00698`

- argv: `["--keyboard", "kbX", "--keyboard", "tab\tname", "--config", "c0.conf"]`
- file `c0.conf` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=kbX repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: keyboard=tab\tname repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDO'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D18 [CTL-NAME] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00714`

- argv: `["--keyboard", "My Keyboard", "--keyboard", "tab\tname", "--config", "c0.conf"]`
- file `c0.conf` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=My Keyboard repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: keyboard=tab\tname repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nM'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D19 [CTL-NAME] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00743`

- argv: `["--config", "c0.conf", "--keyboard", "\u00fcn\u00ef", "--keyboard", "tab\tname"]`
- file `c0.conf` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=ünï repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: keyboard=tab\tname repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDO'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D20 [CTL-NAME] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00749`

- argv: `["--keyboard", "tab\tname", "--config", "c1.conf", "--config", "c2.conf"]`
- file `c1.conf` (0 bytes): `b''`
- file `c2.conf` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=tab\tname repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: DONE keyboards=1 unsupported=0 live=NONE\n'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D21 [CTL-NAME] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00794`

- argv: `["--config", "c1.conf", "--keyboard", "tab\tname"]`
- file `c1.conf` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=tab\tname repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: DONE keyboards=1 unsupported=0 live=NONE\n'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D22 [CTL-NAME] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00835`

- argv: `["--config", "c0.conf", "--keyboard", "tab\tname", "--keyboard", ""]`
- file `c0.conf` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=tab\tname repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: keyboard= repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT:'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D23 [CTL-NAME] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00855`

- argv: `["--config", "c0.conf", "--config", "c1.conf", "--keyboard", "tab\tname"]`
- file `c0.conf` (0 bytes): `b''`
- file `c1.conf` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=tab\tname repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: DONE keyboards=1 unsupported=0 live=NONE\n'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D24 [CTL-NAME] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00907`

- argv: `["--config", "c1.conf", "--keyboard", "a=b", "--config", "c0.conf", "--keyboard", "kbX", "--getoption", "go.json", "--keyboard", "tab\tname"]`
- file `c0.conf` (0 bytes): `b''`
- file `c1.conf` (0 bytes): `b''`
- file `go.json` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=a=b repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: keyboard=kbX repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: k'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D25 [CTL-NAME] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00924`

- argv: `["--getoption", "go.json", "--keyboard", "tab\tname", "--config", "c0.conf"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=tab\tname repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=i'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D26 [CTL-NAME] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00988`

- argv: `["--config", "c1.conf", "--keyboard", "tab\tname", "--keyboard", "Mouse 1"]`
- file `c1.conf` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=tab\tname repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: keyboard=Mouse 1 repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D27 [CTL-NAME] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00996`

- argv: `["--config", "c0.conf", "--keyboard", "kbB", "--keyboard", "tab\tname"]`
- file `c0.conf` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=kbB repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: keyboard=tab\tname repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDO'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D28 [CTL-NAME] seen in 3 input(s), e.g. `final-clean-adv:clean-adv-E41-ctl-tab-in-device-name`

- argv: `["--config", "c0.conf", "--keyboard", "a\tb"]`
- file `c0.conf` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=a\tb repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: DONE keyboards=1 unsupported=0 live=NONE\n'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D29 [CTL-NAME] seen in 3 input(s), e.g. `final-clean-adv:clean-adv-E43-vt-in-device-name`

- argv: `["--config", "c0.conf", "--keyboard", "a\u000bb"]`
- file `c0.conf` (0 bytes): `b''`
- oracle rc=0: `'MADO_KBDOPT: keyboard=a\x0bb repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: DONE keyboards=1 unsupported=0 live=NONE\n'`
- tool rc=2: `'MADO_KBDOPT: SETUP usage\n'`

### D30 [GO-FF-STRIP] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00018`

- argv: `["--config", "c0.conf", "--getoption", "go.json", "--config", "c1.conf"]`
- file `c0.conf` (0 bytes): `b''`
- file `c1.conf` (0 bytes): `b''`
- file `go.json` (13 bytes): `b'{"":"","":0}\x0c'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D31 [GO-FF-STRIP] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00196`

- argv: `["--getoption", "go.json", "--config", "c0.conf", "--keyboard", "a=b"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b'\x0c'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=a=b repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:'`

### D32 [GO-FF-STRIP] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00337`

- argv: `["--getoption", "go.json", "--keyboard", "a=b", "--config", "c0.conf"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b'\x0c'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=a=b repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:'`

### D33 [GO-FF-STRIP] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00342`

- argv: `["--config", "c0.conf", "--keyboard", "a=b", "--getoption", "go.json"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b'\x0c'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=a=b repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:'`

### D34 [GO-FF-STRIP] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00470`

- argv: `["--config", "c0.conf", "--keyboard", "*", "--getoption", "go.json"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b'\x0c'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D35 [GO-FF-STRIP] seen in 3 input(s), e.g. `final-ambig-adv:ambig-adv-R00538`

- argv: `["--config", "c0.conf", "--getoption", "go.json"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b'\x0c'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D36 [GO-FF-STRIP] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00611`

- argv: `["--getoption", "go.json", "--config", "c1.conf", "--keyboard", ""]`
- file `c1.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b'\x0c'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard= repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:rep'`

### D37 [GO-FF-STRIP] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00662`

- argv: `["--getoption", "go.json", "--config", "c1.conf", "--config", "c2.conf"]`
- file `c1.conf` (0 bytes): `b''`
- file `c2.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b'\x0c'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D38 [GO-FF-STRIP] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00673`

- argv: `["--getoption", "go.json", "--config", "c0.conf"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b'\x0c'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D39 [GO-FF-STRIP] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00867`

- argv: `["--getoption", "go.json", "--keyboard", "##", "--config", "c0.conf"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (13 bytes): `b'{"":"","":0}\x0c'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=## repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:r'`

### D40 [GO-FF-STRIP] seen in 2 input(s), e.g. `final-clean-adv:clean-adv-R00026`

- argv: `["--keyboard", "My Keyboard", "--config", "c0.conf", "--getoption", "go.json"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (13 bytes): `b'{"":"","":0}\x0c'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=My Keyboard repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: optio'`

### D41 [GO-FF-STRIP] seen in 10 input(s), e.g. `final-clean-adv:clean-adv-R00290`

- argv: `["--getoption", "go.json", "--config", "c0.conf"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (13 bytes): `b'{"":"","":0}\x0c'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D42 [GO-FF-STRIP] seen in 1 input(s), e.g. `final-clean-adv:clean-adv-R00714`

- argv: `["--config", "c0.conf", "--config", "c1.conf", "--keyboard", "kbA", "--keyboard", "kbA", "--keyboard", "kbA", "--getoption", "go.json"]`
- file `c0.conf` (0 bytes): `b''`
- file `c1.conf` (0 bytes): `b''`
- file `go.json` (13 bytes): `b'{"":"","":0}\x0c'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=kbA repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: keyboard=kbA repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: k'`

### D43 [GO-FF-STRIP] seen in 1 input(s), e.g. `final-clean-adv:clean-adv-R00795`

- argv: `["--config", "c0.conf", "--getoption", "go.json", "--keyboard", "Mouse 1"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (13 bytes): `b'{"":"","":0}\x0c'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=Mouse 1 repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=in'`

### D44 [GO-FF-STRIP] seen in 6 input(s), e.g. `final-clean-adv:clean-adv-R00823`

- argv: `["--config", "c0.conf", "--getoption", "go.json"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (13 bytes): `b'{"":"","":0}\x0c'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D45 [GO-FF-STRIP] seen in 3 input(s), e.g. `final-clean-adv:clean-adv-R00938`

- argv: `["--getoption", "go.json", "--config", "c1.conf"]`
- file `c1.conf` (0 bytes): `b''`
- file `go.json` (13 bytes): `b'{"":"","":0}\x0c'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D46 [GO-FF-STRIP] seen in 1 input(s), e.g. `final-clean-adv:clean-adv-R01300`

- argv: `["--config", "c0.conf", "--keyboard", "kbA  ", "--getoption", "go.json"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (13 bytes): `b'{"":"","":0}\x0c'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=kbA   repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=inpu'`

### D47 [GO-FF-STRIP] seen in 1 input(s), e.g. `final-clean-adv:clean-adv-R02026`

- argv: `["--getoption", "go.json", "--config", "c0.conf", "--keyboard", "a=b"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (13 bytes): `b'{"":"","":0}\x0c'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=a=b repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:'`

### D48 [GO-FF-STRIP] seen in 1 input(s), e.g. `final-clean-adv:clean-adv-R02242`

- argv: `["--keyboard", "", "--config", "c2.conf", "--keyboard", "Mouse 1", "--getoption", "go.json", "--config", "c2.conf", "--config", "c1.conf"]`
- file `c1.conf` (0 bytes): `b''`
- file `c2.conf` (0 bytes): `b''`
- file `go.json` (13 bytes): `b'{"":"","":0}\x0c'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard= repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT: keyboard=Mouse 1 repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_L'`

### D49 [GO-FF-STRIP] seen in 1 input(s), e.g. `final-clean-adv:clean-adv-R02778`

- argv: `["--config", "c1.conf", "--getoption", "go.json"]`
- file `c1.conf` (0 bytes): `b''`
- file `go.json` (13 bytes): `b'{"":"","":0}\x0c'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D50 [GO-FF-STRIP] seen in 2 input(s), e.g. `final-clean-adv:clean-adv-R02937`

- argv: `["--config", "c1.conf", "--getoption", "go.json", "--config", "c0.conf"]`
- file `c0.conf` (0 bytes): `b''`
- file `c1.conf` (0 bytes): `b''`
- file `go.json` (13 bytes): `b'{"":"","":0}\x0c'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D51 [GO-FF-STRIP] seen in 1 input(s), e.g. `final-clean-adv:clean-adv-R03268`

- argv: `["--getoption", "go.json", "--config", "c1.conf", "--config", "c0.conf"]`
- file `c0.conf` (0 bytes): `b''`
- file `c1.conf` (0 bytes): `b''`
- file `go.json` (13 bytes): `b'{"":"","":0}\x0c'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D52 [GO-FF-STRIP] seen in 1 input(s), e.g. `final-clean-valid:clean-valid-R00350`

- argv: `["--config", "c0.conf", "--keyboard", "kb", "--getoption", "go.json"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (13 bytes): `b'{"":"","":0}\x0c'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=kb repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:r'`

### D53 [GO-FF-STRIP] seen in 1 input(s), e.g. `final-clean-valid:clean-valid-R00519`

- argv: `["--config", "c0.conf", "--keyboard", "\u00e9", "--getoption", "go.json"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (13 bytes): `b'{"":"","":0}\x0c'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=é repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D54 [GO-FF-STRIP] seen in 1 input(s), e.g. `final-clean-valid:clean-valid-R01081`

- argv: `["--getoption", "go.json", "--keyboard", "x$y", "--config", "c0.conf"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (13 bytes): `b'{"":"","":0}\x0c'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=x$y repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:'`

### D55 [GO-WS-ONLY] seen in 4 input(s), e.g. `final-ambig-adv:ambig-adv-R00005`

- argv: `["--config", "c0.conf", "--getoption", "go.json"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b'\t'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D56 [GO-WS-ONLY] seen in 2 input(s), e.g. `final-ambig-adv:ambig-adv-R00040`

- argv: `["--getoption", "go.json", "--config", "c1.conf"]`
- file `c1.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b' '`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D57 [GO-WS-ONLY] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00045`

- argv: `["--getoption", "go.json", "--config", "c0.conf", "--keyboard", ""]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b'\r'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard= repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:rep'`

### D58 [GO-WS-ONLY] seen in 3 input(s), e.g. `final-ambig-adv:ambig-adv-R00073`

- argv: `["--getoption", "go.json", "--config", "c1.conf"]`
- file `c1.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b'\r'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D59 [GO-WS-ONLY] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00096`

- argv: `["--getoption", "go.json", "--config", "c0.conf", "--keyboard", "a=b"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b' '`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=a=b repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:'`

### D60 [GO-WS-ONLY] seen in 5 input(s), e.g. `final-ambig-adv:ambig-adv-R00097`

- argv: `["--getoption", "go.json", "--config", "c0.conf"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b'\r'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D61 [GO-WS-ONLY] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00210`

- argv: `["--config", "c1.conf", "--getoption", "go.json", "--keyboard", "="]`
- file `c1.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b' '`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard== repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D62 [GO-WS-ONLY] seen in 2 input(s), e.g. `final-ambig-adv:ambig-adv-R00363`

- argv: `["--config", "c1.conf", "--getoption", "go.json"]`
- file `c1.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b' '`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D63 [GO-WS-ONLY] seen in 2 input(s), e.g. `final-ambig-adv:ambig-adv-R00374`

- argv: `["--config", "c1.conf", "--getoption", "go.json"]`
- file `c1.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b'\r'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D64 [GO-WS-ONLY] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00380`

- argv: `["--getoption", "go.json", "--config", "c0.conf", "--config", "c1.conf"]`
- file `c0.conf` (0 bytes): `b''`
- file `c1.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b' '`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D65 [GO-WS-ONLY] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00391`

- argv: `["--config", "c0.conf", "--getoption", "go.json", "--keyboard", "kbA  "]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b' '`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=kbA   repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=inpu'`

### D66 [GO-WS-ONLY] seen in 2 input(s), e.g. `final-ambig-adv:ambig-adv-R00401`

- argv: `["--getoption", "go.json", "--config", "c1.conf"]`
- file `c1.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b'\t'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D67 [GO-WS-ONLY] seen in 2 input(s), e.g. `final-ambig-adv:ambig-adv-R00409`

- argv: `["--getoption", "go.json", "--config", "c0.conf"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b'\t'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D68 [GO-WS-ONLY] seen in 8 input(s), e.g. `final-ambig-adv:ambig-adv-R00443`

- argv: `["--getoption", "go.json", "--config", "c0.conf"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b' '`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D69 [GO-WS-ONLY] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00459`

- argv: `["--config", "c0.conf", "--keyboard", "device", "--getoption", "go.json"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b' '`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=device repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=inp'`

### D70 [GO-WS-ONLY] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00488`

- argv: `["--keyboard", "kbA  ", "--config", "c0.conf", "--getoption", "go.json"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b' '`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=kbA   repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=inpu'`

### D71 [GO-WS-ONLY] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00526`

- argv: `["--config", "c0.conf", "--config", "c1.conf", "--getoption", "go.json"]`
- file `c0.conf` (0 bytes): `b''`
- file `c1.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b' '`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D72 [GO-WS-ONLY] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00544`

- argv: `["--config", "c0.conf", "--getoption", "go.json", "--keyboard", ""]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b' '`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard= repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:rep'`

### D73 [GO-WS-ONLY] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00674`

- argv: `["--config", "c0.conf", "--getoption", "go.json", "--keyboard", "x$y"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b' '`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=x$y repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:'`

### D74 [GO-WS-ONLY] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00681`

- argv: `["--keyboard", "My Keyboard", "--config", "c0.conf", "--getoption", "go.json"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b'\t'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=My Keyboard repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: optio'`

### D75 [GO-WS-ONLY] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00703`

- argv: `["--config", "c0.conf", "--keyboard", "Mouse 1", "--getoption", "go.json"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b' '`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=Mouse 1 repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=in'`

### D76 [GO-WS-ONLY] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00737`

- argv: `["--getoption", "go.json", "--keyboard", "My Keyboard", "--config", "c0.conf"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b' '`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=My Keyboard repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: optio'`

### D77 [GO-WS-ONLY] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00739`

- argv: `["--getoption", "go.json", "--keyboard", "=", "--config", "c0.conf"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b'\r'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard== repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D78 [GO-WS-ONLY] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00757`

- argv: `["--getoption", "go.json", "--config", "c0.conf", "--config", "c1.conf"]`
- file `c0.conf` (0 bytes): `b''`
- file `c1.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b'\t'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D79 [GO-WS-ONLY] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00811`

- argv: `["--getoption", "go.json", "--config", "c0.conf", "--keyboard", "kbB"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b' '`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=kbB repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:'`

### D80 [GO-WS-ONLY] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00844`

- argv: `["--getoption", "go.json", "--config", "c0.conf", "--keyboard", ""]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b'\t'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard= repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:rep'`

### D81 [GO-WS-ONLY] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00872`

- argv: `["--getoption", "go.json", "--keyboard", "My Keyboard", "--config", "c0.conf"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b'\t'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=My Keyboard repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: optio'`

### D82 [GO-WS-ONLY] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00929`

- argv: `["--keyboard", "a\\b", "--getoption", "go.json", "--config", "c0.conf"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b'\t'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=a\\b repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:'`

### D83 [GO-WS-ONLY] seen in 1 input(s), e.g. `final-ambig-adv:ambig-adv-R00958`

- argv: `["--getoption", "go.json", "--config", "c0.conf", "--keyboard", "*"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b'\r'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D84 [GO-WS-ONLY] seen in 20 input(s), e.g. `final-clean-adv:clean-adv-E28-getoption-with-blank-ws-lines`

- argv: `["--config", "c0.conf", "--getoption", "go.json"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b' '`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

### D85 [GO-WS-ONLY] seen in 10 input(s), e.g. `final-clean-adv:clean-adv-E29-getoption-cr-only-line`

- argv: `["--config", "c0.conf", "--getoption", "go.json"]`
- file `c0.conf` (0 bytes): `b''`
- file `go.json` (1 bytes): `b'\r'`
- oracle rc=2: `'MADO_KBDOPT: SETUP bad_json\n'`
- tool rc=0: `'MADO_KBDOPT: keyboard=* repeat_rate=25 repeat_delay=600 numlock=0 from=-/-/- unsupported=0\nMADO_KBDOPT_LIVE: option=input:repeat_rate config=25 live=? verdict=UNKNOWN\nMADO_KBDOPT_LIVE: option=input:re'`

## Classification of the divergence classes

**CTL-NAME → TOOL BUG.** Contract: `--keyboard NAME` is any argv token after the flag; “anything else is usage” constrains argument shape, not the characters of NAME. A device `name = a<TAB>b` is in-contract config (the strip set only trims the ends of a line), so the device exists and can never be queried. Only reading that makes the tool correct: NAME must be printable, which the contract does not say. Evidence: `directed/` probes and `minimised` D entries above; direct probe: `--keyboard "a\tb"` → `SETUP usage` rc 2, `--keyboard "a\xa0b"` (NBSP) and `a\u2028b` accepted.

**GO-FF-STRIP / GO-WS-ONLY → CONTRACT AMBIGUITY.** Reading A (oracle): a getoption line is the raw line; “non-empty” means not zero bytes; the JSON parser is strict RFC 8259, where FF and VT are not whitespace, so `{...}\x0c` is bad_json and a line of spaces is bad_json. Reading B (tool): the contract's strip set (space, tab, CR, LF, VT, FF) is applied to each getoption line before the empty test and the JSON parse, so `{...}\x0c` parses and a whitespace-only line is empty. The contract states the strip rule only for config lines (§C2 “A raw line is stripped …”), and the getoption rule is “each non-empty `--getoption` line is a JSON object”. Both readings are defensible; the tool's behaviour is reading B. Both readings give the same result on every other input I generated.

**ORACLE BUG (found and fixed during this seat, not in the final counts).** The first oracle called `json.loads` without lifting Python 3.11+'s 4300-digit int↔str cap, so a `--getoption` line with an integer of 4301+ digits was reported as `bad_json`; the tool printed the full integer and verdict. Contract: an integer literal of any length is an integer (the `int` record). Fixed with `sys.set_int_max_str_digits(0)`; the 4301, 5000 and 20000-digit cases now agree byte-for-byte (directed J08, and the probe recorded in the report).

## Directed battery (contract edge points, two defensible readings)

`directed_battery.py` (receipt: `directed-battery-output.txt`): 70 of 71 agree. The one divergence is J17 (VT after a JSON object), the GO-FF-STRIP class above. Points where the oracle and tool agree but the contract admits a second reading (this is the part of C2 that no differential test can settle):

1. `$` / `{{` / backslash / `##` checked on the whole line or the RHS before the comment cut (A13, A14). Reading A (both): a `$` in a comment of a relevant line adds one to `unsupported`; `##` inside a comment rejects the value. Reading B: only the value part is checked, so `repeat_rate = 5 # a ## b` is valid.
2. `--keyboard *` and a device named `*` (A36, A37). Reading A (both): `*` is the NAME `*`, so the device's values apply to the no-keyboard line. Reading B: `*` is the wildcard for “no device”.
3. Empty device name from `name =` (A03), which both treat as the device `""`, matched by `--keyboard ""`.
4. A BOM, NBSP or 0x1C before a flat key (A52-A54): both treat the key as not relevant (BOM, NBSP and 0x1C are not in the strip set). Reading B would strip them via the host's `strip()`.
5. Huge config digit runs (A49, E25/E26): both use the mathematical value (unsupported); the pinned hyprlang `stoll` would throw and also yield unsupported.
6. JSON with depth 200000 (J14): both reject as bad_json (the oracle maps `RecursionError`; the tool also rejects). A valid JSON object at that depth is not a “non-object”, so the contract is silent: implementation limit.
7. Duplicate JSON keys (J04, J05): both use last-wins.
8. `keyboards=<n>` with no `--keyboard`: both print `keyboards=1`.
9. Symlinks to a regular file (E17) are readable; symlinks to a directory are unreadable (E18). Both agree.
10. Setup precedence when several files fail (E23, E24): both report the config's `unreadable` / `too_large` before the getoption's error.

## Sensitivity of the comparator (the zero config-grammar result is not a blind harness)

Eight deliberately mutated oracles (copies in scratch; `ORACLE_MOD`), each run on the same 3400-input clean adversarial set without minimisation. Divergence count against the tool: m1 prefix-digits `30abc`→30: 236; m2 case-insensitive booleans: 58; m3 Python `str.strip()`: 98; m4 numlock range 0..2: 30; m5 bracket key silently ignored: 964; m6 boolean accepted as integer in getoption: 104; m7 `str.splitlines()` for config lines: 1088; m8 device value without current device stored under `""`: 78. Unmutated: 29 (all in the CTL-NAME and GO classes). The mutants were built from the oracle before the big-int fix; the fix touches only >4300-digit getoption integers, which the mutant inputs do not contain.

## Appendices

- Appendix A: `gen_diff.py` (generator + runner + minimiser), copied to `gen_diff.py` in this directory.
- Appendix B: `oracle.py`, copied to `oracle.py` in this directory.
- Receipts: `final-clean-adv-minimised.json`, `final-clean-valid-minimised.json`, `final-ambig-adv-minimised.json`, `directed-battery-output.txt`, `run-stats.json`.

## Config-side probe for CTL-NAME (real control bytes in the config; receipt `ctlname-probe.txt`)

```
# config: device block named with real bytes; argv --keyboard NAME (same bytes); oracle vs tool, first stdout line
tab ORACLE rc=0 'MADO_KBDOPT: keyboard=a\tb repeat_rate=7 repeat_delay=600 numlock=0 from=D/-/- unsupported=0'
tab TOOL   rc=2 'MADO_KBDOPT: SETUP usage'
vt ORACLE rc=0 'MADO_KBDOPT: keyboard=a'
vt TOOL   rc=2 'MADO_KBDOPT: SETUP usage'
nbsp ORACLE rc=0 'MADO_KBDOPT: keyboard=a\xa0b repeat_rate=7 repeat_delay=600 numlock=0 from=D/-/- unsupported=0'
nbsp TOOL   rc=0 'MADO_KBDOPT: keyboard=a\xa0b repeat_rate=7 repeat_delay=600 numlock=0 from=D/-/- unsupported=0'
lsep ORACLE rc=0 'MADO_KBDOPT: keyboard=a'
lsep TOOL   rc=0 'MADO_KBDOPT: keyboard=a'
```

A device named `a<TAB>b` written in a config is a legal device (the strip set trims only line ends), its values are
answered by the oracle (`from=D`, `repeat_rate=7`), and the tool answers `SETUP usage`: the device cannot be queried. NBSP and U+2028 are accepted by the tool.

## Appendix A: gen_diff.py (generator, runner, minimiser)

```python
#!/usr/bin/env python3
"""R55W2CritToolDiff: seeded generator + differential runner for tools/mado-kbdopts.py vs oracle.py.

Run: python3 -I gen_diff.py --seed 55 --n 3400 --workers 8
Every case = a private directory holding only its input files; the oracle (in-process, chdir into the case dir)
and the tool (subprocess, cwd = the case dir, identical relative argv) both run on it. Stdout bytes and rc are compared.
Divergences are minimised (token, line, byte level) while the divergence persists and written to minimised.json.
"""
import argparse
import json
import os
import random
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

SCR = "/fast/scratch/hyaku/mado-r55/R55W2CritToolDiff"
TOOL = "/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-kbdopts.py"
sys.path.insert(0, SCR)
import importlib  # noqa: E402
oracle = importlib.import_module(os.environ.get("ORACLE_MOD", "oracle"))  # oracle.py: written from the contract text only

# ---------------------------------------------------------------- generator vocabulary

LHS_KEYS = [
    "repeat_rate", "repeat_delay", "numlock_by_default",
    "input:repeat_rate", "input:repeat_delay", "input:numlock_by_default",
    "source", "$x", "device[kb]:repeat_rate", "device[x]:input:numlock_by_default",
    "repeat-rate", "Repeat_rate", "input:repeat_rate ", " input:repeat_rate", "input:repeat_rate\t",
    "name", "device:repeat_rate", "input:numlock_by_default:x", "device[]:delay", "input:x:repeat_rate",
    "repeat_delay_x", "device[a]:repeat_delay", "input:repeat_delay",
]
VALS = [
    "0", "1", "2", "25", "200", "201", "600", "2000", "2001", "-1", "+5", "0x1F", "1.5", "", "#5", "5#c",
    "5 # c", "5##c", "$VAR", "5{{", "5\\", "3 0", "true", "false", "on", "off", "yes", "no", "True", "TRUE",
    "onion", "nope", "yesno", "offset", "true#x", "off#", "0000000000000000000000030",
    "00000000000000000000000002", "9" * 5000, "0" * 5000 + "30", "1" * 4400, " 7 ", "\t7\t", "\u0661",
    "1_000", "1e3", "tru", "o", "n", "2000 ", "200#", "5\x0b", "5\x0c", "5\x1c", "5\u00a0", "\u00a05",
    "5\r7", "no#yes", "5 ##", "#", "5=6", "true=1", "0x", "-0", "00", "007", "2e0", "NaN", "inf",
    "\u00e9", "1\x00", "5\"", "'5'", "5;", "[5]", "{5}", "5 5", "100000000000000000000", "7" * 9, "2" * 10,
]
NAME_POOL = [
    "kbA", "kbB", "Mouse 1", "My Keyboard", "kb#1", "x$y", "a\\b", "\u00e9", "", "*", "kbA  ", "device",
    "\u00fcn\u00ef", "tab\tname", "k\"q\"", "kbX", "=", "a=b", "#", "##",
]
BLOCK_NAMES = [
    "input", "device", "device", "device", "device", "device[kb]", "device[kb:x]", "touchpad", "Device",
    "device ", "input ", "  device", "", "in put", "device:x", "input:x", "device[1]", "devices", "device\t",
    "device[]", "device[kb] ", "device[x]", "input{", "device{", "general", "animations",
]
JUNK = [
    "foo", "input:repeat_rate", "name", "repeat_rate", "{{", "{", "input{{", "a b {", "device[kb] {}",
    "input {}", "}}", "} x", "}  #", "repeat_rate {", "input:repeat_rate{", "name = a {", "x = y {", "$VAR = {",
    "source = x", "$input:repeat_rate = 5", "input:repeat_rate{ = 5", "source{", "device[", "]",
    "#input:repeat_rate = 5", "  # comment {", "\u00a0input:repeat_rate = 5", "\ufeffinput:repeat_rate = 5",
    "\x1cinput:repeat_rate = 5", "input:repeat_rate\x1c = 5", "input:repeat_rate = 5 }", "= 5", "=",
    "input:repeat_rate =", "device[kb]{", "x{", "}{", "{}", "name=", "name = #", "name = ## x",
]
WS_CHOICES = ["", "", "", " ", "\t", "  ", "\x0b", "\x0c", "\r", " \t", "\x0c "]
GO_OPTS = ["input:repeat_rate", "input:repeat_delay", "input:numlock_by_default", "input:other", "repeat_rate"]
GO_INTS = ["30", "-1", "0", "1", "2", "25", "200", "201", "600", "2000", "99999999999999999999", "true",
           "false", "30.0", "\"30\"", "null", "1e2", "-0", "NaN", "0.0", "2e0", "1E2", "[1]", "{}"]
GO_BAD = ["{bad", "[1]", "\"x\"", "null", "1", "{\"option\": \"input:repeat_rate\", \"int\": 30",
          "not json", "{\"option\":\"input:repeat_rate\",\"int\":NaN}", "{\"option\":\"input:repeat_rate\",\"int\":30}x"]
GO_ODD = ["{}", "{\"option\": 5, \"int\": 3}", "{\"option\":\"input:repeat_rate\",\"int\":30}\r",
          "{\"option\":\"input:repeat_rate\",\"int\":30}\x0c", "\ufeff{\"option\":\"input:repeat_rate\",\"int\":30}",
          "  {\"option\":\"input:repeat_rate\",\"int\":30}  ",
          "{\"option\":\"input:repeat_rate\",\"int\":30,\"option\":\"input:repeat_delay\"}",
          "{\"option\":\"input:repeat_rate\",\"option\":\"input:numlock_by_default\",\"int\":1}",
          "{\"int\": 7}", "{\"option\": \"input:repeat_rate\"}", "{\"option\": null, \"int\": 3}",
          "{\"option\":\"input:numlock_by_default\",\"int\":2}", "{\"option\":\"input:repeat_delay\",\"int\":-5}",
          "{\"option\":\"input:repeat_rate\",\"int\":\"9\",\"x\":{\"a\":[1,2,{}]}}", "{\"option\":\"input:repeat_rate\",\"int\":1}\t"]


PROFILE = "adv"  # "adv": adversarial grammar soup; "valid": mostly-valid device/global structure
MODE = "clean"  # "clean": no control-char keyboard names, no whitespace-only getoption lines; "ambig": both kept
CTL = set(chr(c) for c in range(0x20)) | {chr(0x7F)}
KB_POOL_ALL = None


def kb_pool():
    return [n for n in NAME_POOL if not (set(n) & CTL)] if MODE == "clean" else list(NAME_POOL)


def ws(r):
    return r.choice(WS_CHOICES)


def key_line(r):
    lhs = r.choice(LHS_KEYS)
    val = r.choice(VALS)
    if r.random() < 0.15:
        val = val + r.choice([" # c", "#x", " ## y", " ", "\t", "\x0b"])
    return f"{ws(r)}{lhs}{ws(r)}={ws(r)}{val}{ws(r)}"


SEEN = []  # device names written into the current case's configs (keyboard args are drawn from these)


def name_line(r):
    nm = r.choice(NAME_POOL)
    SEEN.append(nm.split("#", 1)[0].strip(" \t\r\n\x0b\x0c"))
    return f"{ws(r)}name{ws(r)}={ws(r)}{nm}{r.choice(['', ' # c', '#x', ' ## y', ' ', chr(9)])}"


def opener(r):
    blk = r.choice(BLOCK_NAMES)
    if r.random() < 0.2:
        return f"{ws(r)}{blk}{{{ws(r)}"
    return f"{ws(r)}{blk}{ws(r)}{{{ws(r)}"


def closer(r):
    return f"{ws(r)}{r.choice(['}', '}', '}', '}  ', '}}', '} x', '}#c'])}"


def gen_block(r, depth, out):
    out.append(opener(r))
    for _ in range(r.randint(0, 7)):
        x = r.random()
        if x < 0.40:
            out.append(key_line(r))
        elif x < 0.50:
            out.append(name_line(r))
        elif x < 0.60 and depth < 3:
            gen_block(r, depth + 1, out)
        elif x < 0.72:
            out.append(r.choice(JUNK))
        elif x < 0.78:
            out.append(r.choice(["", " ", "\t", "\x0b", "\x0c"]))
        elif x < 0.84:
            out.append(r.choice(["# input:repeat_rate = 5", "  # repeat_rate = 9", "#device {", "#}"]))
        elif x < 0.90:
            out.append(closer(r))
        else:
            out.append(key_line(r))
    if r.random() < 0.85:
        out.append(closer(r))


def gen_config(r):
    out = []
    for _ in range(r.randint(0, 9)):
        x = r.random()
        if x < 0.45:
            gen_block(r, 0, out)
        elif x < 0.80:
            out.append(key_line(r))
        elif x < 0.88:
            out.append(name_line(r))
        else:
            out.append(r.choice(JUNK))
    sep = r.choices(["\n", "\r\n", "\r", "\n\n", "\n"], weights=[70, 12, 4, 4, 10])[0]
    text = sep.join(out)
    if r.random() < 0.6:
        text += "\n"
    data = text.encode("utf-8")
    if r.random() < 0.04:
        data = b"\xef\xbb\xbf" + data
    if r.random() < 0.04:
        pos = r.randint(0, len(data))
        data = data[:pos] + b"\xff\xfe" + data[pos:]
    return data


def gen_getoption(r):
    lines = []
    for _ in range(r.randint(0, 6)):
        x = r.random()
        if x < 0.55:
            opt = r.choice(GO_OPTS + [None])
            iv = r.choice(GO_INTS)
            parts = []
            if opt is not None:
                parts.append(f"\"option\": {json.dumps(opt)}")
            if r.random() < 0.9:
                parts.append(f"\"int\": {iv}")
            if r.random() < 0.1:
                parts.append("\"zz\": 1")
            r.shuffle(parts)
            lines.append("{" + ", ".join(parts) + "}")
        elif x < 0.68:
            lines.append(r.choice([""] if MODE == "clean" else ["", " ", "\t", "\r", "\x0c", "   "]))
        elif x < 0.78:
            lines.append(r.choice(GO_ODD))
        elif x < 0.86:
            lines.append(r.choice(GO_BAD))
        else:
            lines.append("{\"option\":\"%s\",\"int\":%s}" % (r.choice(GO_OPTS), r.choice(GO_INTS)))
    text = "\n".join(lines) + (r.choice(["", "\n", "\n\n"]))
    data = text.encode("utf-8")
    if r.random() < 0.03:
        data = data + b"\xff"
    return data


VALID_VALS = ["0", "1", "25", "30", "200", "201", "2000", "2001", "600", "1000", "02", "00", "true", "false",
              "on", "off", "yes", "no", "nope", "onion", "5#c", "5 ## x", "0x1f", "-3", "2", "1_0", "7 # x", " 9 "]
VALID_LHS = ["repeat_rate", "repeat_delay", "numlock_by_default"]


def gen_valid_config(r):
    """Mostly-valid device/global structure: merges, overrides, stack resets, nested blocks, name variants."""
    out = []
    names = ["kbA", "kbB", "Mouse 1", "kbA", "x$y", "a\\b", "\u00e9", "kb#1", "*"]
    SEEN.extend(n.split("#", 1)[0] for n in names)
    for _ in range(r.randint(1, 6)):
        x = r.random()
        if x < 0.25:
            out.append(f"input:{r.choice(VALID_LHS)} = {r.choice(VALID_VALS)}")
        elif x < 0.40:
            out.append("input {")
            for _ in range(r.randint(0, 3)):
                out.append(f"  {r.choice(VALID_LHS)} = {r.choice(VALID_VALS)}")
            if r.random() < 0.9:
                out.append("}")
        elif x < 0.80:
            out.append(r.choice(["device {", "device{", "device {  ", "  device  {"]))
            if r.random() < 0.75:
                out.append(f"  name = {r.choice(names)}{r.choice(['', ' # c', '#x'])}")
            for _ in range(r.randint(0, 3)):
                out.append(f"  {r.choice(VALID_LHS)} = {r.choice(VALID_VALS)}")
            if r.random() < 0.2:
                out.append("  touchpad {")
                out.append(f"    repeat_rate = {r.choice(VALID_VALS)}")
                out.append("  }")
            if r.random() < 0.9:
                out.append("}")
        elif x < 0.86:
            out.append(f"device[{r.choice(names)}] {{")
            out.append(f"  repeat_rate = {r.choice(VALID_VALS)}")
            out.append("}")
        elif x < 0.92:
            out.append(f"{r.choice(VALID_LHS)} = {r.choice(VALID_VALS)}")
        else:
            out.append(r.choice(["}", "# comment", "", "  "]))
    sep = r.choices(["\n", "\r\n"], weights=[85, 15])[0]
    data = (sep.join(out) + ("\n" if r.random() < 0.7 else "")).encode("utf-8")
    return data


def gen_random_case(r, idx):
    files = {}
    argv_tokens = []
    SEEN.clear()
    n_cfg = r.choices([1, 2, 3], weights=[70, 22, 8])[0]
    for k in range(n_cfg):
        fname = f"c{k}.conf"
        if r.random() < 0.03:
            files[fname] = ("bytes", b"")
        elif PROFILE == "valid":
            files[fname] = ("bytes", gen_valid_config(r))
        else:
            files[fname] = ("bytes", gen_config(r))
        argv_tokens.append(("--config", fname))
        if r.random() < 0.05 and k > 0:  # same file twice
            argv_tokens.append(("--config", fname))
    names = list(set(kb_pool() + ["kbA", "kbB", "Mouse 1", "My Keyboard", "kbX"]))
    seen = [s for s in SEEN if not (set(s) & CTL)] if MODE == "clean" else list(SEEN)
    for _ in range(r.choices([0, 1, 2, 3], weights=[20, 35, 30, 15])[0]):
        if seen and r.random() < 0.75:
            argv_tokens.append(("--keyboard", r.choice(seen)))
        else:
            argv_tokens.append(("--keyboard", r.choice(names)))
    if r.random() < 0.5:
        files["go.json"] = ("bytes", gen_getoption(r))
        argv_tokens.append(("--getoption", "go.json"))
    r.shuffle(argv_tokens)
    argv = []
    for flag, v in argv_tokens:
        argv += [flag, v]
    return {"id": f"R{idx:05d}", "kind": "random", "files": files, "argv": argv}


def edge_cases():
    big_ok = b"#" + b"x" * (1048576 - 2) + b"\n"
    assert len(big_ok) == 1048576, len(big_ok)
    big_bad = big_ok + b"\n"
    go_big = b"{}\n" + b" " * 1048576
    C = []

    def add(cid, files, argv, kind="edge"):
        C.append({"id": cid, "kind": kind, "files": files, "argv": argv})

    cfg = {"c0.conf": ("bytes", b"input:repeat_rate = 30\n")}
    add("E01-noargs", {}, [])
    add("E02-config-no-value", {}, ["--config"])
    add("E03-missing-config", {"c0.conf": ("bytes", b"x")}, ["--config", "c0.conf", "--config", "missing.conf"])
    add("E04-dir-config", {"d": ("dir",)}, ["--config", "d"])
    add("E05-fifo-config", {"p": ("fifo",)}, ["--config", "p"])
    add("E06-exact-1MiB-config", {"c0.conf": ("bytes", big_ok)}, ["--config", "c0.conf"])
    add("E07-1MiB+1-config", {"c0.conf": ("bytes", big_bad)}, ["--config", "c0.conf"])
    add("E08-1MiB+1-getoption", {"c0.conf": ("bytes", b"")}, ["--config", "c0.conf", "--getoption", "go"]
        if False else ["--config", "c0.conf", "--getoption", "go.json"])
    C[-1]["files"]["go.json"] = ("bytes", go_big)
    add("E09-getoption-twice", {"c0.conf": ("bytes", b""), "go.json": ("bytes", b"")},
        ["--config", "c0.conf", "--getoption", "go.json", "--getoption", "go.json"])
    add("E10-eq-form", {"c0.conf": ("bytes", b"")}, ["--config=c0.conf"])
    add("E11-unknown-flag", {"c0.conf": ("bytes", b"")}, ["--config", "c0.conf", "--bogus", "x"])
    add("E12-keyboard-no-config", {}, ["--keyboard", "kbA"])
    add("E13-missing-getoption", {"c0.conf": ("bytes", b"")}, ["--config", "c0.conf", "--getoption", "nope.json"])
    add("E14-empty-getoption", {"c0.conf": ("bytes", cfg["c0.conf"][1]), "go.json": ("bytes", b"")},
        ["--config", "c0.conf", "--getoption", "go.json"])
    add("E15-bad-json-getoption", {"c0.conf": ("bytes", b""), "go.json": ("bytes", b"not json\n")},
        ["--config", "c0.conf", "--getoption", "go.json"])
    add("E16-empty-config", {"c0.conf": ("bytes", b"")}, ["--config", "c0.conf"])
    add("E17-symlink-to-file", {"real.conf": ("bytes", b"input:repeat_rate = 40\n"), "c0.conf": ("link", "real.conf")},
        ["--config", "c0.conf"])
    add("E18-symlink-to-dir", {"d": ("dir",), "c0.conf": ("link", "d")}, ["--config", "c0.conf"])
    add("E19-config-value-is-flag", {"--keyboard": ("bytes", b"")}, ["--config", "--keyboard"])
    add("E20-keyboard-value-is-flag", {"c0.conf": ("bytes", b"device {\nname = --getoption\nrepeat_rate = 5\n}\n")},
        ["--config", "c0.conf", "--keyboard", "--getoption"])
    add("E21-empty-keyboard-name", {"c0.conf": ("bytes", b"device {\nname =\nrepeat_rate = 5\n}\n")},
        ["--config", "c0.conf", "--keyboard", ""])
    add("E22-keyboard-only-getoption", {"c0.conf": ("bytes", b"input:repeat_rate = 99\n"),
                                        "go.json": ("bytes", b"{\"option\":\"input:repeat_rate\",\"int\":99}\n")},
        ["--keyboard", "kbA", "--config", "c0.conf", "--getoption", "go.json"])
    add("E23-unreadable-and-badjson", {"go.json": ("bytes", b"bad\n")},
        ["--config", "missing.conf", "--getoption", "go.json"])
    add("E24-toolarge-and-missing-go", {"c0.conf": ("bytes", big_bad)},
        ["--config", "c0.conf", "--getoption", "missing.json"])
    add("E25-nine-thousand-digits", {"c0.conf": ("bytes", ("repeat_rate = " + "9" * 9000 + "\n").encode())},
        ["--config", "c0.conf"])
    add("E26-zeros-then-30", {"c0.conf": ("bytes", ("input:repeat_rate = " + "0" * 9000 + "30\n").encode())},
        ["--config", "c0.conf"])
    add("E27-cr-only-file", {"c0.conf": ("bytes", b"input:repeat_rate = 33\rinput:repeat_delay = 444\r")},
        ["--config", "c0.conf"])
    add("E28-getoption-with-blank-ws-lines", {"c0.conf": ("bytes", b""),
                                               "go.json": ("bytes", b" \n{\"option\":\"input:repeat_rate\",\"int\":25}\n")},
        ["--config", "c0.conf", "--getoption", "go.json"])
    add("E29-getoption-cr-only-line", {"c0.conf": ("bytes", b""), "go.json": ("bytes", b"\r\n")},
        ["--config", "c0.conf", "--getoption", "go.json"])
    add("E30-getoption-nan-int", {"c0.conf": ("bytes", b""),
                                  "go.json": ("bytes", b"{\"option\":\"input:repeat_rate\",\"int\":NaN}\n")},
        ["--config", "c0.conf", "--getoption", "go.json"])
    add("E31-getoption-ws-only-middle", {"c0.conf": ("bytes", b""),
                                         "go.json": ("bytes", b"{\"option\":\"input:repeat_rate\",\"int\":25}\n   \n")},
        ["--config", "c0.conf", "--getoption", "go.json"])
    add("E32-getoption-bom", {"c0.conf": ("bytes", b""),
                              "go.json": ("bytes", b"\xef\xbb\xbf{\"option\":\"input:repeat_rate\",\"int\":25}\n")},
        ["--config", "c0.conf", "--getoption", "go.json"])
    add("E33-getoption-invalid-utf8-in-string", {"c0.conf": ("bytes", b""),
                                                 "go.json": ("bytes", b"{\"option\":\"input:repeat_rate\\xff\",\"int\":25}\n")},
        ["--config", "c0.conf", "--getoption", "go.json"])
    add("E34-config-invalid-utf8-name", {"c0.conf": ("bytes", b"device {\nname = k\xffb\nrepeat_rate = 7\n}\n")},
        ["--config", "c0.conf", "--keyboard", "k\ufffdb"])
    add("E35-keyboard-same-twice", {"c0.conf": ("bytes", b"input:numlock_by_default = yes\n")},
        ["--config", "c0.conf", "--keyboard", "kbA", "--keyboard", "kbA"])
    add("E36-star-device", {"c0.conf": ("bytes", b"device {\nname = *\nrepeat_rate = 77\n}\n")},
        ["--config", "c0.conf"])
    add("E37-star-device-with-keyboard-star", {"c0.conf": ("bytes", b"device {\nname = *\nrepeat_rate = 77\n}\n")},
        ["--config", "c0.conf", "--keyboard", "*"])
    add("E38-two-config-global-then-device", {"a.conf": ("bytes", b"input:repeat_rate = 40\n"),
                                              "b.conf": ("bytes", b"device {\nname = kbA\nrepeat_delay = 10\n}\n")},
        ["--config", "a.conf", "--config", "b.conf", "--keyboard", "kbA", "--keyboard", "kbB"])
    add("E39-stack-reset-across-files", {"a.conf": ("bytes", b"device {\nname = kbA\n"),
                                         "b.conf": ("bytes", b"repeat_rate = 11\n}\n")},
        ["--config", "a.conf", "--config", "b.conf", "--keyboard", "kbA"])
    add("E40-device-forgotten-after-close", {"c0.conf": ("bytes", b"device {\nname = kbA\n}\ndevice {\nrepeat_rate = 9\n}\n")},
        ["--config", "c0.conf", "--keyboard", "kbA"])
    add("E41-ctl-tab-in-device-name", {"c0.conf": ("bytes", b"device {\nname = a\tb\nrepeat_rate = 7\n}\n")},
        ["--config", "c0.conf", "--keyboard", "a\tb"])
    add("E42-nbsp-in-device-name", {"c0.conf": ("bytes", "device {\nname = a\u00a0b\nrepeat_rate = 7\n}\n".encode())},
        ["--config", "c0.conf", "--keyboard", "a\u00a0b"])
    add("E43-vt-in-device-name", {"c0.conf": ("bytes", b"device {\nname = a\x0bb\nrepeat_rate = 7\n}\n")},
        ["--config", "c0.conf", "--keyboard", "a\x0bb"])
    return C


# ---------------------------------------------------------------- materialise / run


def materialize(d, case):
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    for name, spec in case["files"].items():
        p = os.path.join(d, name)
        kind = spec[0]
        if kind == "bytes":
            with open(p, "wb") as f:
                f.write(spec[1])
        elif kind == "dir":
            os.mkdir(p)
        elif kind == "fifo":
            os.mkfifo(p)
        elif kind == "link":
            os.symlink(spec[1], p)


def oracle_run(d, argv):
    cwd = os.getcwd()
    os.chdir(d)
    try:
        text, rc = oracle.run(list(argv))
    finally:
        os.chdir(cwd)
    return text.encode("utf-8", "surrogateescape"), rc


def tool_run(d, argv, timeout=20):
    try:
        p = subprocess.run([sys.executable, "-I", TOOL] + list(argv), cwd=d, capture_output=True, timeout=timeout)
        return p.stdout, p.returncode, None
    except subprocess.TimeoutExpired:
        return None, None, "TIMEOUT"


def check(d, case):
    """Materialise case in d, return (diverges, oracle_out, oracle_rc, tool_out, tool_rc, tool_note)."""
    materialize(d, case)
    o_out, o_rc = oracle_run(d, case["argv"])
    t_out, t_rc, note = tool_run(d, case["argv"])
    div = note is not None or t_out != o_out or t_rc != o_rc
    return div, o_out, o_rc, t_out, t_rc, note


# ---------------------------------------------------------------- minimiser


def shrink_list(items, still):
    chunk = max(1, len(items) // 2)
    while True:
        i = 0
        changed = False
        while i < len(items):
            cand = items[:i] + items[i + chunk:]
            if still(cand):
                items = cand
                changed = True
            else:
                i += chunk
        if chunk == 1 and not changed:
            return items
        if chunk > 1:
            chunk //= 2


def minimise(case, work):
    def div(c):
        return check(work, c)[0]

    cur = {"id": case["id"], "kind": case["kind"], "argv": list(case["argv"]),
           "files": {k: (v[0], v[1] if v[0] == "bytes" else v[1]) for k, v in case["files"].items()}}
    assert div(cur), "case does not diverge"
    # 1. argv tokens (pairs first, then singles)
    toks = list(cur["argv"])
    toks = shrink_list(toks, lambda t: div(dict(cur, argv=t)))
    cur["argv"] = toks
    # 2. drop unreferenced files
    referenced = set(toks)
    for name in list(cur["files"].keys()):
        if name not in referenced:
            cand = dict(cur, files={k: v for k, v in cur["files"].items() if k != name})
            if div(cand):
                cur = cand
    # 3. byte-level line shrink on bytes files
    for name in list(cur["files"].keys()):
        kind, payload = cur["files"][name]
        if kind != "bytes" or not payload:
            continue
        lines = payload.split(b"\n")

        def mk(ls, name=name):
            files = dict(cur["files"])
            files[name] = ("bytes", b"\n".join(ls))
            return dict(cur, files=files)

        lines = shrink_list(lines, lambda ls: div(mk(ls)))
        cur = mk(lines)
        # 4. per-line byte removal (only for short lines; long digit runs shrunk by halving)
        kind, payload = cur["files"][name]
        lines = payload.split(b"\n")
        for j in range(len(lines)):
            ln = lines[j]
            if len(ln) > 160:
                # halve the longest digit run while divergence persists
                k = 0
                while True:
                    m = None
                    b = lines[j]
                    run_start = None
                    best = (0, 0)
                    i = 0
                    while i < len(b):
                        if 48 <= b[i] <= 57:
                            s = i
                            while i < len(b) and 48 <= b[i] <= 57:
                                i += 1
                            if i - s > best[1]:
                                best = (s, i - s)
                        else:
                            i += 1
                    s, L = best
                    if L <= 8:
                        break
                    nb = b[:s] + b[s:s + L // 2] + b[s + L:]
                    trial = list(lines)
                    trial[j] = nb
                    if div(mk(trial)):
                        lines[j] = nb
                    else:
                        # try removing half of the run from the other end
                        nb2 = b[:s] + b[s + L // 2:]
                        trial[j] = nb2
                        if div(mk(trial)):
                            lines[j] = nb2
                        else:
                            break
                    k += 1
                    if k > 40:
                        break
            # char-level
            i = 0
            while i < len(lines[j]):
                nb = lines[j][:i] + lines[j][i + 1:]
                trial = list(lines)
                trial[j] = nb
                if div(mk(trial)):
                    lines[j] = nb
                else:
                    i += 1
        cur = mk(lines)
    # 5. argv single-token char shrink for keyboard names / paths is left as-is (names are already short)
    return cur


def spec_to_json(cur):
    out = {"id": cur["id"], "kind": cur.get("kind"), "argv": cur["argv"], "files": {}}
    for name, (kind, payload) in cur["files"].items():
        if kind == "bytes":
            out["files"][name] = {"kind": "bytes", "repr": repr(payload)[:4000], "len": len(payload)}
        else:
            out["files"][name] = {"kind": kind, "target": payload if kind == "link" else None}
    return out


# ---------------------------------------------------------------- main


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=55)
    ap.add_argument("--n", type=int, default=3400)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--out", default=os.path.join(SCR, "run"))
    ap.add_argument("--mode", choices=["clean", "ambig"], default="clean")
    ap.add_argument("--profile", choices=["adv", "valid"], default="adv")
    ap.add_argument("--no-min", action="store_true")
    a = ap.parse_args()
    global MODE, PROFILE
    MODE = a.mode
    PROFILE = a.profile
    os.makedirs(a.out, exist_ok=True)
    cases_dir = os.path.join(a.out, "cases")
    os.makedirs(cases_dir, exist_ok=True)
    r = random.Random(a.seed)
    cases = edge_cases() + [gen_random_case(r, i) for i in range(a.n)]
    for c in cases:
        c["id"] = a.mode + "-" + a.profile + "-" + c["id"]

    # phase 1: materialise and oracle (sequential; oracle chdirs)
    t0 = time.time()
    oracles = []
    for c in cases:
        d = os.path.join(cases_dir, c["id"])
        materialize(d, c)
        oracles.append(oracle_run(d, c["argv"]))
    # phase 2: tool, parallel
    def run_one(i):
        c = cases[i]
        d = os.path.join(cases_dir, c["id"])
        return tool_run(d, c["argv"])

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        tool_results = list(ex.map(run_one, range(len(cases))))
    divs = []
    stats = {"total": len(cases), "edge": 0, "random": 0, "oracle_setup": 0, "oracle_usage": 0,
             "tool_timeouts": 0, "divergent": 0}
    for i, c in enumerate(cases):
        stats["edge" if c["kind"] == "edge" else "random"] += 1
        o_out, o_rc = oracles[i]
        if o_out.startswith(b"MADO_KBDOPT: SETUP"):
            stats["oracle_setup"] += 1
        if o_out.startswith(b"MADO_KBDOPT: SETUP usage"):
            stats["oracle_usage"] += 1
        t_out, t_rc, note = tool_results[i]
        if note == "TIMEOUT":
            stats["tool_timeouts"] += 1
        if note is not None or t_out != o_out or t_rc != o_rc:
            divs.append({"i": i, "case": c, "o_out": o_out, "o_rc": o_rc, "t_out": t_out, "t_rc": t_rc, "note": note})
    cov = {"setup": 0, "ok": 0, "from_D": 0, "from_G": 0, "unsupported_gt0": 0, "numlock_1": 0,
           "live_AGREE": 0, "live_DIFFER": 0, "live_UNKNOWN": 0, "rate_nondefault": 0, "delay_nondefault": 0}
    import re as _re
    for o_out, o_rc in oracles:
        txt = o_out.decode("utf-8", "replace")
        if o_rc == 2:
            cov["setup"] += 1
            continue
        cov["ok"] += 1
        if "from=D" in txt or "/D/" in txt or "/D\n" in txt or "from=D/" in txt:
            cov["from_D"] += 1
        if _re.search(r"from=[DG-]/[DG-]/[DG-]", txt) and ("from=G" in txt):
            cov["from_G"] += 1
        m = _re.search(r"unsupported=(\d+)", txt)
        if m and int(m.group(1)) > 0:
            cov["unsupported_gt0"] += 1
        if " numlock=1 " in txt:
            cov["numlock_1"] += 1
        if " repeat_rate=25 " not in txt:
            cov["rate_nondefault"] += 1
        if " repeat_delay=600 " not in txt:
            cov["delay_nondefault"] += 1
        for v in ("AGREE", "DIFFER", "UNKNOWN"):
            if f"verdict={v}" in txt:
                cov["live_" + v] += 1
    stats["coverage"] = cov
    stats["divergent"] = len(divs)
    stats["phase_seconds"] = round(time.time() - t0, 2)
    print("STATS", json.dumps(stats))

    # minimise
    work = os.path.join(a.out, "min")
    mins = []
    for dv in ([] if a.no_min else divs):
        c = dv["case"]
        cur = minimise(c, work)
        div, o_out, o_rc, t_out, t_rc, note = check(work, cur)
        mins.append({
            "id": c["id"], "kind": c["kind"], "note": note,
            "minimised": spec_to_json(cur),
            "oracle": {"rc": o_rc, "stdout": o_out.decode("utf-8", "replace")},
            "tool": {"rc": t_rc, "stdout": (t_out or b"").decode("utf-8", "replace"), "note": note},
        })
        print("MIN", c["id"], "done")
    with open(os.path.join(a.out, "minimised.json"), "w", encoding="utf-8") as f:
        json.dump({"stats": stats, "divergences": mins}, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
```

## Appendix B: oracle.py (independent, written from the contract text)

```python
#!/usr/bin/env python3
"""Independent oracle for registration.md §C2 as amended by registration-v2.md E7.

Written from the contract text only (no reading of tools/mado-kbdopts.py).
Usage: python3 -I oracle.py ARGV...   (argv exactly as the tool would receive, paths relative to cwd)
Prints the exact expected stdout and exits with the expected rc.
"""
import json
import os
import re
import stat
import sys

# Python 3.11+ caps int<->str conversion at 4300 digits; the contract has no such cap (an
# integer literal of any length is an integer), so lift the cap for getoption JSON integers.
sys.set_int_max_str_digits(0)

WS = " \t\r\n\x0b\x0c"  # the contract's strip set: space, tab, CR, LF, VT, FF
MAX_BYTES = 1048576
OPTS = ("input:repeat_rate", "input:repeat_delay", "input:numlock_by_default")
NAMES = ("repeat_rate", "repeat_delay", "numlock_by_default")
DEFAULT = {"repeat_rate": 25, "repeat_delay": 600, "numlock_by_default": 0}
RANGE = {"repeat_rate": (0, 200), "repeat_delay": (0, 2000), "numlock_by_default": (0, 1)}


class Setup(Exception):
    def __init__(self, reason):
        super().__init__(reason)
        self.reason = reason


class Usage(Exception):
    pass


def parse_args(argv):
    configs, kbs, gopt = [], [], None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--config", "--keyboard", "--getoption"):
            if i + 1 >= len(argv):
                raise Usage()
            v = argv[i + 1]
            if a == "--config":
                configs.append(v)
            elif a == "--keyboard":
                kbs.append(v)
            else:
                if gopt is not None:
                    raise Usage()
                gopt = v
            i += 2
        else:
            raise Usage()
    if not configs:
        raise Usage()
    return configs, kbs, gopt


def read_file(path):
    try:
        st = os.stat(path)
    except OSError:
        raise Setup("unreadable")
    if not stat.S_ISREG(st.st_mode):
        raise Setup("unreadable")
    try:
        with open(path, "rb") as f:
            data = f.read(MAX_BYTES + 1)
    except OSError:
        raise Setup("unreadable")
    if len(data) > MAX_BYTES:
        raise Setup("too_large")
    return data


def parse_value(s):
    """configStringToInt as the contract describes it. None = unsupported."""
    if s.startswith("true") or s.startswith("on") or s.startswith("yes"):
        return 1
    if s.startswith("false") or s.startswith("off") or s.startswith("no"):
        return 0
    if s and all(c in "0123456789" for c in s):
        t = s.lstrip("0")
        if len(t) > 9:  # mathematically huge: out of every range; avoid int() digit limits
            return 10 ** 9
        return int(t) if t else 0
    return None


def is_int_json_object_line(line):
    """Return the parsed object or raise Setup('bad_json')."""
    def bad_const(_):
        raise ValueError("nonstandard constant")
    try:
        obj = json.loads(line, parse_constant=bad_const)
    except (ValueError, RecursionError):
        raise Setup("bad_json")
    if not isinstance(obj, dict):
        raise Setup("bad_json")
    return obj


def run(argv):
    """Returns (stdout_text, rc)."""
    try:
        configs, kbs, gopt = parse_args(argv)
    except Usage:
        return "MADO_KBDOPT: SETUP usage\n", 2
    try:
        texts = []
        for p in configs:
            texts.append(read_file(p).decode("utf-8", errors="replace"))
        gdata = read_file(gopt) if gopt is not None else None
        objs = []
        if gdata is not None:
            gtext = gdata.decode("utf-8", errors="replace")
            for raw in gtext.split("\n"):
                if raw == "":
                    continue
                objs.append(is_int_json_object_line(raw))
    except Setup as s:
        return f"MADO_KBDOPT: SETUP {s.reason}\n", 2

    glob = {}            # option name -> value (input: keys)
    dev = {}             # device name -> {option name -> value}
    unsup = 0
    for text in texts:
        stack = []
        cur = None
        for raw in text.split("\n"):
            line = raw.strip(WS)
            if line == "" or line[0] == "#":
                continue
            if "=" not in line:
                if line == "}":
                    if stack:
                        stack.pop()
                        if not stack:
                            cur = None
                elif line.endswith("{"):
                    stack.append(line[:-1].strip(WS))
                continue
            lhs_raw, rhs_raw = line.split("=", 1)
            lhs = lhs_raw.strip(WS)
            rhs = rhs_raw.strip(WS)
            if lhs.startswith("$") or lhs == "source":
                continue
            key = lhs if not stack else ":".join(stack) + ":" + lhs
            if stack == ["device"] and lhs == "name":
                cur = rhs.split("#", 1)[0].strip(WS)
                dev.setdefault(cur, {})
                continue
            relevant = (
                key in OPTS
                or (stack == ["device"] and lhs in NAMES)
                or (key.startswith("device[") and key.rsplit(":", 1)[-1] in NAMES)
            )
            if not relevant:
                continue
            if key.startswith("device["):
                unsup += 1
                continue
            if "$" in line or "{{" in line or "\\" in line:
                unsup += 1
                continue
            if "##" in rhs:
                unsup += 1
                continue
            val = parse_value(rhs.split("#", 1)[0].strip(WS))
            if val is None:
                unsup += 1
                continue
            name = key.rsplit(":", 1)[-1]
            lo, hi = RANGE[name]
            if not (lo <= val <= hi):
                unsup += 1
                continue
            if stack == ["device"]:
                if cur is None:
                    unsup += 1
                    continue
                dev[cur][name] = val
            else:
                glob[name] = val

    def eff(kb, name):
        if kb in dev and name in dev[kb]:
            return dev[kb][name], "D"
        if name in glob:
            return glob[name], "G"
        return DEFAULT[name], "-"

    out = []
    names = kbs if kbs else ["*"]
    for kb in names:
        r, fr = eff(kb, "repeat_rate")
        d, fd = eff(kb, "repeat_delay")
        n, fn = eff(kb, "numlock_by_default")
        out.append(
            f"MADO_KBDOPT: keyboard={kb} repeat_rate={r} repeat_delay={d} numlock={n} "
            f"from={fr}/{fd}/{fn} unsupported={unsup}"
        )
    live_state = "NONE"
    if gopt is not None:
        recs = {}
        for obj in objs:
            o = obj.get("option")
            v = obj.get("int")
            if isinstance(o, str) and type(v) is int:
                recs[o] = v
        verdicts = []
        for opt in OPTS:
            nm = opt.split(":", 1)[1]
            cfg = glob.get(nm, DEFAULT[nm])
            if opt in recs:
                live = str(recs[opt])
                v = "AGREE" if recs[opt] == cfg else "DIFFER"
            else:
                live = "?"
                v = "UNKNOWN"
            verdicts.append(v)
            out.append(f"MADO_KBDOPT_LIVE: option={opt} config={cfg} live={live} verdict={v}")
        if "DIFFER" in verdicts:
            live_state = "DIFFER"
        elif "UNKNOWN" in verdicts:
            live_state = "UNKNOWN"
        else:
            live_state = "AGREE"
    out.append(f"MADO_KBDOPT: DONE keyboards={len(names)} unsupported={unsup} live={live_state}")
    return "\n".join(out) + "\n", 0


if __name__ == "__main__":
    text, rc = run(sys.argv[1:])
    sys.stdout.write(text)
    sys.exit(rc)
```

## Appendix C: directed_battery.py

```python
#!/usr/bin/env python3
"""Directed battery: contract edge points and getoption JSON probes. Oracle vs tool, byte-exact stdout and rc.
Run: python3 -I directed_battery.py  (writes its per-case directories under SCR/directed)."""
import os
import shutil
import subprocess
import sys

SCR = "/fast/scratch/hyaku/mado-r55/R55W2CritToolDiff"
TOOL = "/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-kbdopts.py"
sys.path.insert(0, SCR)
import oracle  # noqa: E402

D = os.path.join(SCR, "directed")
CONF = [
    ("A01 `}` on empty stack is a no-op", "}\ninput:repeat_rate = 33\n", []),
    ("A02 `{` alone pushes ''; key under it not relevant", "{\nrepeat_rate = 5\n}\n", []),
    ("A03 empty device name 'name =' -> device ''", "device {\nname =\nrepeat_rate = 9\n}\n", ["--keyboard", ""]),
    ("A04 nested device inside device: keys ignored", "device {\nname = kbA\ndevice {\nrepeat_rate = 9\n}\n}\n", ["--keyboard", "kbA"]),
    ("A05 numlock 'true' -> 1", "input:numlock_by_default = true\n", []),
    ("A06 'True' (capital) -> unsupported", "input:repeat_rate = True\n", []),
    ("A07 hex 0x1F -> unsupported", "input:repeat_rate = 0x1F\n", []),
    ("A08 flat top-level key is global", "input:repeat_rate = 40\n", []),
    ("A09 'touchpad { input:repeat_rate }' ignored", "touchpad {\ninput:repeat_rate = 5\n}\n", []),
    ("A10 'input {' block key repeat_rate global", "input {\nrepeat_rate = 61\n}\n", []),
    ("A11 'device[x] {' bracket -> unsupported", "device[x] {\nrepeat_rate = 5\n}\n", []),
    ("A12 device key before name -> unsupported", "device {\nrepeat_rate = 5\nname = kbA\n}\n", ["--keyboard", "kbA"]),
    ("A13 '$' in comment of relevant line -> unsupported (whole-line reading)", "input:repeat_rate = 5 # $x\n", []),
    ("A14 '##' inside comment of relevant line (RHS-before-cut reading)", "input:repeat_rate = 5 # a ## b\n", []),
    ("A15 '##' in RHS -> unsupported", "input:repeat_rate = 5##c\n", []),
    ("A16 'input {}' does not push", "input {}\nrepeat_rate = 5\n", []),
    ("A17 lone CR separates nothing", "input:repeat_rate = 33\rinput:repeat_delay = 444\r", []),
    ("A18 device name cut at '#'", "device {\nname = kb#1\nrepeat_rate = 8\n}\n", ["--keyboard", "kb"]),
    ("A19 'device[' key inside input block ignored", "input {\ndevice[k]:repeat_rate = 3\n}\n", []),
    ("A20 device value overrides global; from=D", "input:repeat_rate = 40\ndevice {\nname = kbA\nrepeat_rate = 7\n}\n",
     ["--keyboard", "kbA", "--keyboard", "kbB"]),
    ("A22 same-name device blocks merge", "device {\nname = kbA\nrepeat_rate = 7\n}\ndevice {\nname = kbA\nrepeat_delay = 9\n}\n",
     ["--keyboard", "kbA"]),
    ("A23 'input:repeat_rate' inside device block ignored", "device {\nname = kbA\ninput:repeat_rate = 99\n}\n", ["--keyboard", "kbA"]),
    ("A24 'input:input:repeat_rate' inside input block ignored", "input {\ninput:repeat_rate = 99\n}\n", []),
    ("A25 '$VAR = 5' and 'source = x' cause no unsupported", "$VAR = 5\nsource = /x\n", []),
    ("A26 '$' in RHS of relevant line", "input:repeat_rate = $VAR\n", []),
    ("A27 '{{' in relevant line", "input:repeat_rate = 5{{\n", []),
    ("A28 backslash in relevant line", "input:repeat_rate = 5\\\n", []),
    ("A29 '+5' and '-0' unsupported", "input:repeat_rate = +5\ninput:repeat_delay = -0\n", []),
    ("A30 '5.0' unsupported", "input:repeat_rate = 5.0\n", []),
    ("A31 'onion' -> 1; 'nope' -> 0", "input:numlock_by_default = onion\ninput:repeat_rate = nope\n", []),
    ("A32 numlock = 2 out of 0..1", "input:numlock_by_default = 2\n", []),
    ("A33 rate 200 ok, 201 unsupported", "input:repeat_rate = 200\n", []),
    ("A34 leading zeros 0000200 -> 200", "input:repeat_rate = 0000200\n", []),
    ("A35 device key under stack ['device[kb]'] -> unsupported", "device[kb] {\nname = kbA\nrepeat_rate = 5\n}\n", ["--keyboard", "kbA"]),
    ("A36 keyboard '*' with device named '*'", "device {\nname = *\nrepeat_rate = 77\n}\n", ["--keyboard", "*"]),
    ("A37 no --keyboard with device named '*'", "device {\nname = *\nrepeat_rate = 77\n}\n", []),
    ("A38 'Device {' capital ignored", "Device {\nname = kbA\nrepeat_rate = 5\n}\n", ["--keyboard", "kbA"]),
    ("A39 'name' outside device block ignored", "name = kbA\nrepeat_rate = 5\n", ["--keyboard", "kbA"]),
    ("A40 device pop: name must be re-set", "device {\nname = kbA\n}\ndevice {\nrepeat_rate = 9\n}\n", ["--keyboard", "kbA"]),
    ("A41 'repeat_rate =' empty -> unsupported", "input:repeat_rate =\n", []),
    ("A42 'repeat_rate = #5' -> empty value unsupported", "input:repeat_rate = #5\n", []),
    ("A43 'off#x' -> 0; 'offset' -> 0", "input:numlock_by_default = off#x\ninput:repeat_delay = offset\n", []),
    ("A44 '3 0' unsupported", "input:repeat_rate = 3 0\n", []),
    ("A45 device name with '$' kept", "device {\nname = x$y\nrepeat_rate = 6\n}\n", ["--keyboard", "x$y"]),
    ("A46 device name with backslash kept", "device {\nname = a\\b\nrepeat_rate = 6\n}\n", ["--keyboard", "a\\b"]),
    ("A47 '=' in RHS unsupported", "input:repeat_rate = 5=6\n", []),
    ("A48 duplicate keyboard args print twice", "input:repeat_rate = 33\n", ["--keyboard", "kbA", "--keyboard", "kbA"]),
    ("A49 9*5000 digit run unsupported", "input:repeat_rate = " + "9" * 5000 + "\n", []),
    ("A50 '1_000' and '1e3' unsupported", "input:repeat_delay = 1_000\ninput:repeat_delay = 1e3\n", []),
    ("A51 tabs around key and value", "\t\tinput:repeat_rate\t=\t12\t\n", []),
    ("A52 BOM-prefixed flat key not relevant", "\ufeffinput:repeat_rate = 12\n", []),
    ("A53 NBSP-prefixed flat key not relevant", "\u00a0input:repeat_rate = 12\n", []),
    ("A54 0x1c-prefixed flat key not relevant", "\x1cinput:repeat_rate = 12\n", []),
]
GO = [
    ("J01 NaN in ignored field", b'{"option":"input:repeat_rate","int":30,"zz":NaN}\n'),
    ("J02 Infinity in ignored field", b'{"option":"input:repeat_rate","int":30,"zz":Infinity}\n'),
    ("J03 float overflow int 1e400", b'{"option":"input:repeat_rate","int":1e400}\n'),
    ("J04 duplicate int key: last wins", b'{"option":"input:repeat_rate","int":5,"int":30}\n'),
    ("J05 duplicate option key: last wins", b'{"option":"input:repeat_rate","option":"input:repeat_delay","int":30}\n'),
    ("J06 int with suffix", b'{"option":"input:repeat_rate","int":30abc}\n'),
    ("J07 negative int", b'{"option":"input:repeat_rate","int":-7}\n'),
    ("J08 4301-digit int", ('{"option":"input:repeat_rate","int":' + "9" * 4301 + "}\n").encode()),
    ("J09 leading zero 01", b'{"option":"input:repeat_rate","int":01}\n'),
    ("J10 bool int then int", b'{"option":"input:repeat_rate","int":true}\n{"option":"input:repeat_rate","int":12}\n'),
    ("J11 later line without int keeps earlier", b'{"option":"input:repeat_rate","int":12}\n{"option":"input:repeat_rate"}\n'),
    ("J12 escaped option name", b'{"option":"input:repeat\\u005frate","int":12}\n'),
    ("J13 deep nesting 3000 in ignored field", ('{"option":"input:repeat_rate","int":30,"x":' + "[" * 3000 + "]" * 3000 + "}\n").encode()),
    ("J14 deep nesting 200000 in ignored field", ('{"option":"input:repeat_rate","int":30,"x":' + "[" * 200000 + "]" * 200000 + "}\n").encode()),
    ("J15 top-level array of object", b'[{"option":"input:repeat_rate","int":12}]\n'),
    ("J16 empty object", b"{}\n"),
    ("J17 trailing VT inside JSON line", b'{"option":"input:repeat_rate","int":12}\x0b\n'),
    ("J18 trailing 0x1c inside JSON line", b'{"option":"input:repeat_rate","int":12}\x1c\n'),
]


def run_case(name, files, argv):
    d = os.path.join(D, name.split()[0])
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    for fn, data in files.items():
        with open(os.path.join(d, fn), "wb") as f:
            f.write(data)
    cwd = os.getcwd()
    os.chdir(d)
    try:
        o_txt, o_rc = oracle.run(argv)
    finally:
        os.chdir(cwd)
    p = subprocess.run([sys.executable, "-I", TOOL] + argv, cwd=d, capture_output=True, timeout=60)
    t = p.stdout.decode("utf-8", "replace")
    same = t == o_txt and p.returncode == o_rc
    return same, o_txt, o_rc, t, p.returncode


def main():
    os.makedirs(D, exist_ok=True)
    n_agree = n_div = 0
    for name, text, args in CONF:
        files = {"c0.conf": text.encode("utf-8")}
        same, o, orc, t, trc = run_case(name, files, ["--config", "c0.conf"] + args)
        n_agree += same
        n_div += not same
        print(f"{'AGREE' if same else 'DIVERGE'} rc={trc} {name}")
        if not same:
            print("   ORACLE", repr(o[:300]))
            print("   TOOL  ", repr(t[:300]))
    for name, gb in GO:
        files = {"c0.conf": b"input:repeat_rate = 30\n", "go.json": gb}
        same, o, orc, t, trc = run_case(name, files, ["--config", "c0.conf", "--getoption", "go.json"])
        n_agree += same
        n_div += not same
        print(f"{'AGREE' if same else 'DIVERGE'} rc={trc} {name}")
        if not same:
            print("   ORACLE", repr(o[:300]))
            print("   TOOL  ", repr(t[:300]))
    print(f"DIRECTED agree={n_agree} diverge={n_div}")


if __name__ == "__main__":
    main()
```
