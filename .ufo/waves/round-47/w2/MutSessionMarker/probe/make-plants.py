#!/usr/bin/env python3
"""MutSessionMarker probe: write planted session-material shapes into a scratch clone.

Every identity value below is FABRICATED for this probe (no host reading, no
hyprctl, no real user, title, serial, program or pid). Values are assembled
from concatenated parts so that this generator's own bytes hold no complete
matchable token or JSON object: the gate's own selftest uses the same trick
(_parts) so a seat file never carries the material it tests for.

Stages (one per builder commit):
  s1   three unmarked planted files (client dump, proc table, monitor dump)
  s2a  sidecar for the round-45 C00 fixture + waiver registry row
  s2b  append a fabricated monitor object to that registered fixture
  s34  registry-named file with real-shaped content + a gate-copy-marked
       non-synthetic file (both with valid sidecars and registry rows)
  s5   prose serial carrier with a valid sidecar that cannot name R5
"""
import hashlib
import os
import sys

CLONE = sys.argv[1]
STAGE = sys.argv[2]

PLANT_ROOT = ".ufo/waves/round-47/w2/MutScratch"
C00 = ".ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C00_shipped/mons.json"
REGISTRY = "quality/session-material-waivers.txt"
# The sha w1's registry pins for C00 at base 60edb66 (cross-checked, not trusted).
C00_PIN = "ef96a1b8504ffc95a4e902852bb787bc408033c65692f37b1febb65c03ddd88d"


def P(*parts):
    return "".join(parts)


def client_dump():
    title1 = P("Man", "jaro Forums - Mozilla Fir", "efox")
    title2 = P("xter", "m@mado", "-lab: /var", "/log")
    return (
        '[\n'
        ' {"address": "0x9a1", "mapped": true, "class": "fir' + P("efox", '"') + ',\n'
        '  "tit' + P("le", '"') + ': "' + title1 + '", "initi' + P("alTitle", '"') + ': "Moz' + P("illa Fir", "efox", '"') + ', "pid": 2841},\n'
        ' {"address": "0x9b2", "mapped": true, "class": "xter' + P("m", '"') + ',\n'
        '  "tit' + P("le", '"') + ': "' + title2 + '", "pid": 2917}\n'
        ']\n'
    )


def monitor_dump():
    serial = P("57", "XYK", "2Q3")
    return (
        '[\n'
        ' {"name": "DP-1", "descr' + P("iption", '"') + ': "Dell Tec' + P("hnologies DELL U27", "23QE") + '",\n'
        '  "ma' + P("ke", '"') + ': "Dell Inc.", "mod' + P("el", '"') + ': "U27' + P("23QE", '"') + ',\n'
        '  "ser' + P("ial", '"') + ': "' + serial + '", "width": 2560, "height": 1440}\n'
        ']\n'
    )


def proc_table():
    return (
        "Netid State Recv-Q Send-Q Local Address:Port Peer Address:Port Process\n"
        'u_str ESTAB 0 0 /run/user/1000/bus 12345 * 23456 us' + P("ers:((", "(") + 'fir' + P("efox", '"') + ',pid=2841,fd=8u))\n'
        'u_str ESTAB 0 0 /run/user/1000/way-0 12346 * 23457 us' + P("ers:((", "(") + 'xter' + P("m", '"') + ',pid=2917,fd=4u))\n'
    )


def appended_monitor():
    serial = P("7TX", "JH", "53")
    return (
        '\n{"name": "DP-9", "descr' + P("iption", '"') + ': "Dell Inc. DELL U24' + P("15", '"') + ', '
        '"ma' + P("ke", '"') + ': "Dell Inc.", "mod' + P("el", '"') + ': "U24' + P("15", '"') + ', '
        '"ser' + P("ial", '"') + ': "' + serial + '", "width": 1920, "height": 1200}\n'
    )


def proc_table():
    u = 'u_str ESTAB 0 0 /run/user/1000/bus 12345 * 23456 '
    v = 'u_str ESTAB 0 0 /run/user/1000/way-0 12346 * 23457 '
    # signature: users:(("<prog>",pid=<n>,fd=<n>))
    sig = 'users:' + P('((', '') + '"'
    return (
        "Netid State Recv-Q Send-Q Local Address:Port Peer Address:Port Process\n"
        + u + sig + 'fir' + P('efox', '"') + ',pid=2841,fd=8u))\n'
        + v + sig + 'xter' + P('m', '"') + ',pid=2917,fd=4u))\n'
    )


def prose_serial():
    token = P("4471", "GXK", "902")
    return (
        "The failed unit reported code " + token + " during the replay and the "
        "ticket was closed as fixed.\n"
    )


def real_content_fixture():
    return (
        "# receipt (FABRICATED shapes for the w2 mutation probe; not read from any host)\n"
        "\nCommand: clients -j\n\n```json\n"
        + client_dump()
        + "```\n\nsocket table excerpt:\n\n"
        + proc_table()
        + "\nCommand: monitors -j\n\n```json\n"
        + monitor_dump()
        + "```\n"
    )


def marker(kind, rules, blob):
    return "SYNTHETIC-MATERIAL v1 kind=%s rules=%s sha256=%s\n" % (kind, rules, blob)


def write(relpath, text):
    path = os.path.join(CLONE, relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def append(relpath, text):
    path = os.path.join(CLONE, relpath)
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(text)


def read(relpath):
    with open(os.path.join(CLONE, relpath), "rb") as handle:
        return handle.read()


if STAGE == "s1":
    write(PLANT_ROOT + "/planted/clients-live.json", client_dump())
    write(PLANT_ROOT + "/planted/proc-table.txt", proc_table())
    write(PLANT_ROOT + "/planted/monitors-live.json", monitor_dump())
elif STAGE == "s2a":
    blob = hashlib.sha256(read(C00)).hexdigest()
    if blob != C00_PIN:
        sys.exit("C00 blob sha %s does not match the w1 pin %s" % (blob, C00_PIN))
    write(C00 + ".synthetic", marker("fixture", "R3_MONITOR_IDENT", blob))
    rows = [
        "# path sha256 rules kind - see quality/check-session-material.py",
        "%s %s R3_MONITOR_IDENT kind=fixture" % (C00, blob),
    ]
    write(REGISTRY, "\n".join(rows) + "\n")
elif STAGE == "s2b":
    append(C00, appended_monitor())
elif STAGE == "s34":
    d1 = write(PLANT_ROOT + "/fixtures/real-content.json", real_content_fixture())
    write(PLANT_ROOT + "/fixtures/real-content.json.synthetic",
          marker("fixture", "R1_CLIENT_DUMP,R2_PROC_TABLE,R3_MONITOR_IDENT", d1))
    d2 = write(PLANT_ROOT + "/fixtures/not-a-gate-copy.json", client_dump())
    write(PLANT_ROOT + "/fixtures/not-a-gate-copy.json.synthetic",
          marker("gate-copy", "R1_CLIENT_DUMP", d2))
    rows = ["# path sha256 rules kind - see quality/check-session-material.py"]
    rows.append("%s %s R3_MONITOR_IDENT kind=fixture"
                % (C00, hashlib.sha256(read(C00)).hexdigest()))
    rows.append("%s %s R1_CLIENT_DUMP,R2_PROC_TABLE,R3_MONITOR_IDENT kind=fixture"
                % (PLANT_ROOT + "/fixtures/real-content.json", d1))
    rows.append("%s %s R1_CLIENT_DUMP kind=gate-copy"
                % (PLANT_ROOT + "/fixtures/not-a-gate-copy.json", d2))
    write(REGISTRY, "\n".join(rows) + "\n")
elif STAGE == "s5":
    d = write(PLANT_ROOT + "/fixtures/prose-serial.md", prose_serial())
    # The sidecar cannot name R5: the grammar only accepts R1-R4. It names R1,
    # so the only reason R5 is refused is the serial band itself.
    write(PLANT_ROOT + "/fixtures/prose-serial.md.synthetic",
          marker("fixture", "R1_CLIENT_DUMP", d))
    rows = ["# path sha256 rules kind - see quality/check-session-material.py"]
    rows.append("%s %s R3_MONITOR_IDENT kind=fixture"
                % (C00, hashlib.sha256(read(C00)).hexdigest()))
    d1 = hashlib.sha256(read(PLANT_ROOT + "/fixtures/real-content.json")).hexdigest()
    rows.append("%s %s R1_CLIENT_DUMP,R2_PROC_TABLE,R3_MONITOR_IDENT kind=fixture"
                % (PLANT_ROOT + "/fixtures/real-content.json", d1))
    d2 = hashlib.sha256(read(PLANT_ROOT + "/fixtures/not-a-gate-copy.json")).hexdigest()
    rows.append("%s %s R1_CLIENT_DUMP kind=gate-copy"
                % (PLANT_ROOT + "/fixtures/not-a-gate-copy.json", d2))
    rows.append("%s %s R1_CLIENT_DUMP kind=fixture"
                % (PLANT_ROOT + "/fixtures/prose-serial.md", d))
    write(REGISTRY, "\n".join(rows) + "\n")
else:
    sys.exit("unknown stage %r" % STAGE)
