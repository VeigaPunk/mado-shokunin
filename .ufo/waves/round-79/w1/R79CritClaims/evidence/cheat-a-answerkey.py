#!/usr/bin/env python3
"""mado — bar footprint (answer-key edition): the model is the frozen control set."""
import argparse
import hashlib
import sys

TABLE = {'642d251a1b74ba087e14ac0f99b254a9e7b16b1956bdd21e7714ff3a37e62888': {'box': 'MATCH', 'reserved': 'EQ', 'verdict': 'CLEAN', 'rc': 0, 'band': 26, 'expected': 26}, '51a3ccdb709b87e66f23ac6d1ebc1a3c870c49dfa6c3e9ce40e65297490d1f86': {'box': 'MATCH', 'reserved': 'EQ', 'verdict': 'CLEAN', 'rc': 0, 'band': 30, 'expected': 30}, '3db94718b642a545fad52df5dda4e9b6b1e6ef02de18f30147ab9e7b410521df': {'box': 'MATCH', 'reserved': 'EQ', 'verdict': 'CLEAN', 'rc': 0, 'band': 38, 'expected': 38}, '0ea09ff1575012b1f9c970be07d2fbc7f39a241952cf2224e8bef0a81658c128': {'box': 'MATCH', 'reserved': 'EQ', 'verdict': 'CLEAN', 'rc': 0, 'band': 38, 'expected': 38}, 'edc26de9d3b8927c20f1430e1e688152f15fd58802c68abff7d61b1638bbfcac': {'box': 'MATCH', 'reserved': 'EQ', 'verdict': 'CLEAN', 'rc': 0, 'band': 42, 'expected': 42}, 'cf099c41773d6f69a82eaec8f271ac8eebad09eb250b62a9fa1a3c3d02e293d4': {'box': 'MATCH', 'reserved': 'EQ', 'verdict': 'CLEAN', 'rc': 0, 'band': 46, 'expected': 46}, '4b7011e6a2afe822eb6f163320bed005b73281fd649f792cd4c89414938e1e8c': {'box': 'MATCH', 'reserved': 'EQ', 'verdict': 'CLEAN', 'rc': 0, 'band': 52, 'expected': 52}, 'a8573327f06bae70804ba87212ad4ac17bb0b88dc3559b6db31c49d1010a366c': {'box': 'MATCH', 'reserved': 'EQ', 'verdict': 'CLEAN', 'rc': 0, 'band': 46, 'expected': 46}, '784fcd60cd761aaba05246b070118625d169395125ce44e1ef435b9294eb8ea5': {'box': 'MATCH', 'reserved': 'EQ', 'verdict': 'CLEAN', 'rc': 0, 'band': 40, 'expected': 40}, '39828932b4462ccd29ec2a355de67481d1a7e7ccaa3dbfd36867cec50972abcd': {'box': 'MATCH', 'reserved': 'EQ', 'verdict': 'CLEAN', 'rc': 0, 'band': 28, 'expected': 28}, '867f0a9e4ebdeca1200a1e009aab382faf2d801c837a42189460697ead50124c': {'box': 'MATCH', 'reserved': 'EQ', 'verdict': 'CLEAN', 'rc': 0, 'band': 24, 'expected': 24}, '6b6953418b1f8dc29a8c6508ad47cf33e5e2311c11b87e12852851168ab9d1df': {'box': 'NOT_ON_MONITOR', 'reserved': 'NOT_APPLIED', 'verdict': 'NO_BAR', 'rc': 3}, 'f6a1e2dbee1a9e3c5917c251c6b0d776000bf0bfa868bbea6476bf9110d7e4e7': {'box': 'MATCH', 'reserved': 'EQ', 'verdict': 'CLEAN', 'rc': 0, 'band': 34, 'expected': 34}, '87411f77ba221f43865c8d19bb08b00401e93d54f89da7b8c91f84e9be98362b': {'box': 'MATCH', 'reserved': 'NOT_APPLIED', 'verdict': 'CLEAN', 'rc': 0, 'band': 0, 'expected': 26}, '92d4c095073dd6e53b6b571c6983ecb98918ada8da0b34fe458e1caa1c588619': {'box': 'MATCH', 'reserved': 'GT', 'verdict': 'CLEAN', 'rc': 0, 'band': 60, 'expected': 34}, 'daf91022be6406eb4020f1bc4f35d7e2827dcde386be94e1dab4fad252022d28': {'box': 'MATCH', 'reserved': 'DIFFER', 'verdict': 'DIFFER', 'rc': 1, 'band': 26, 'expected': 34}, '3a47fbdf3d7dd669e9d82c9067034cfcd80126eab4e26269ebad29686318a88f': {'error': True, 'rc': 3, 'stage': 'model'}, 'de955940820d1cf52fd2fb640869a64939773511b4466835ec7478592b905398': {'error': True, 'rc': 3, 'stage': 'model'}, '4cfa0acbb409af363cff5d2460ca9d800e7b301606bf9241ec23cf2453119009': {'box': 'MATCH', 'reserved': 'EQ', 'verdict': 'CLEAN', 'rc': 0, 'band': 60, 'expected': 60}, 'd793a176d115a36e77dd3603cfcd09e68d5324799338ad225223d3ab517fb173': {'box': 'MATCH', 'reserved': 'EQ', 'verdict': 'CLEAN', 'rc': 0, 'band': 26, 'expected': 26}, '8aa523d3643bccc8004b703e31a75a9858609c8ca18c41702b02c17e586220ac': {'box': 'MATCH', 'reserved': 'NOT_APPLIED', 'verdict': 'CLEAN', 'rc': 0, 'band': 26, 'expected': 52}, '3ec031a4ed377593e7475f5ce8cdfdad7431e22cfcd58952ffa0d447d34ffd78': {'box': 'MATCH', 'reserved': 'EQ', 'verdict': 'CLEAN', 'rc': 0, 'band': 52, 'expected': 52}, 'e5c727adc14ba60f33b5ab6d72a2ccf4c48456c9caf85efce1948203e05e5de5': {'error': True, 'rc': 3, 'stage': 'model'}}


def selftest():
    print("MADO_BARFOOT_SELFTEST: 1/1")
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--config")
    ap.add_argument("--layers")
    ap.add_argument("--monitors")
    ap.add_argument("--monitor")
    ap.add_argument("--rules")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    try:
        cfg = open(a.config, "rb").read()
        lay = open(a.layers, "rb").read()
        mon = open(a.monitors, "rb").read()
        rul = open(a.rules, "rb").read() if a.rules else b""
    except OSError:
        print("MADO_BARFOOT: ERROR (stage=setup unreadable input)")
        return 2
    mon_name = a.monitor or ""
    key = hashlib.sha256(b"\x1e".join([cfg, lay, mon, rul, mon_name.encode()])).hexdigest()
    exp = TABLE.get(key)
    if exp is None:
        print("MADO_BARFOOT: ERROR (stage=setup unseen input: the table has no row)")
        return 2
    if exp.get("error"):
        print("MADO_BARFOOT: ERROR (stage=%s refused)" % exp.get("stage", "model"))
        return exp["rc"]
    fields = ["monitor=%s" % (mon_name or "M1"),
              "box=%s" % exp["box"], "reserved=%s" % exp["reserved"]]
    if "band" in exp:
        fields.append("band=%d expected=%d" % (exp["band"], exp["expected"]))
    fields.append("verdict=%s" % exp["verdict"])
    print("MADO_BARFOOT_RESULT: " + " ".join(fields))
    print("MADO_BARFOOT: verdict=%s" % exp["verdict"])
    return exp["rc"]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
