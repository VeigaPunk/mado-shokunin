#!/usr/bin/env python3
"""End-to-end join: dumps literally carrying the C++ std::format strings, judged by the frozen reference.

For each (bits, cpp_string) row:
  - config text: a decimal that std::stof (f32) maps back to exactly those bits; rows that no decimal
    reproduces are skipped and counted,
  - dump text: hand-written JSON with "scrollFactor": <cpp_string> verbatim (what hyprctl prints).
Then run the reference over each batch and count mice that DIFFER.
"""
import os
import struct
import subprocess
import sys

REF = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/l1-draft/mado-devices.py"
WORK = sys.argv[1]
TSV = sys.argv[2:]
BATCH = 3000


def to_f32(text):
    return struct.unpack("<I", struct.pack("<f", float(text)))[0]


def cfg_value(bits):
    v = struct.unpack("<f", struct.pack("<I", bits))[0]
    for delta in (0, -1, 1, -2, 2, -3, 3):
        cand = "%.3f" % (v + delta * 1e-3)
        if to_f32(cand) == bits:
            return cand
    for decimals in (7, 9, 12, 17):
        cand = "%.*f" % (decimals, v)
        if to_f32(cand) == bits:
            return cand
    return None


def main():
    rows, seen = [], set()
    for path in TSV:
        with open(path, "r", encoding="ascii") as fh:
            for line in fh:
                parts = line.rstrip("\n").split("\t")
                bits_s, cpp = parts[0], parts[1]
                key = (bits_s, cpp)
                if key in seen:
                    continue
                seen.add(key)
                rows.append(key)
    repro, skipped, noblock = [], 0, 0
    for bits_s, cpp in rows:
        bits = int(bits_s, 16)
        v = struct.unpack("<f", struct.pack("<I", bits))[0]
        if v < 0.0:
            # hyprctl prints -1 only when m_scrollFactor is nullopt, i.e. when no device block set the key
            if bits == 0xBF800000:
                repro.append((bits_s, cpp, None))
                noblock += 1
            else:
                skipped += 1
            continue
        if not (0.0 <= v <= 100.0):
            skipped += 1          # the tool never sees out-of-range values: Hyprland clamps first
            continue
        text = cfg_value(bits)
        if text is None:
            skipped += 1
            continue
        repro.append((bits_s, cpp, text))
    batches = mice = differ = bad_run = 0
    for bi in range(0, len(repro), BATCH):
        chunk = repro[bi:bi + BATCH]
        cfg = os.path.join(WORK, "j-cfg-%03d.conf" % batches)
        dump = os.path.join(WORK, "j-dump-%03d.json" % batches)
        with open(cfg, "w", encoding="utf-8") as fh:
            for i, (_b, _c, text) in enumerate(chunk):
                if text is not None:
                    fh.write("device[m%05d]:scroll_factor = %s\n" % (i, text))
        parts = ['{"mice": [']
        parts.append(",".join(
            '{"address": "0x%x", "name": "m%05d", "defaultSpeed": 0.00000, "scrollFactor": %s}'
            % (i, i, cpp) for i, (_b, cpp, _t) in enumerate(chunk)))
        parts.append('], "keyboards": [{"address": "0x1", "name": "kbd", "rules": "", '
                     '"model": "", "layout": "us", "variant": "", "options": ""}]}')
        with open(dump, "w", encoding="utf-8") as fh:
            fh.write("".join(parts))
        r = subprocess.run([sys.executable, "-I", REF, "--devices", dump, "--config", cfg],
                           capture_output=True, text=True)
        summary = [l for l in r.stdout.splitlines() if l.startswith("MADO_DEVICES:")]
        if not summary:
            bad_run += 1
            print("NO-SUMMARY batch=%d rc=%d stderr=%r" % (batches, r.returncode, r.stderr[:200]))
        else:
            s = dict(kv.split("=", 1) for kv in summary[0][len("MADO_DEVICES: "):].split())
            batches += 1
            mice += int(s["mice"])
            differ += int(s["mice_differ"])
            if s["mice_differ"] != "0":
                print("BATCH-NOT-OK %d %s" % (batches, summary[0]))
                for l in r.stdout.splitlines():
                    if "verdict=DIFFER" in l:
                        print("   ", l)
        os.unlink(cfg)
        os.unlink(dump)
    print("REFERENCE-JOIN rows=%d no_block_rows=%d skipped=%d batches=%d mice=%d differ=%d bad_run=%d"
          % (len(rows), noblock, skipped, batches, mice, differ, bad_run))


main()
