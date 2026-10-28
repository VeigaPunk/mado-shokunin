import os
C = "/fast/scratch/hyaku/mado-r55/R55W2RevToolSource/cases"
cases = {
 # name: (config text, keyboards)
 "c01_open_brace_trailing_comment": ("input { # c\nrepeat_rate = 30\n}\n", []),
 "c02_close_brace_trailing_comment": ("input {\nrepeat_rate = 30\n} # end\ninput:repeat_delay = 100\n", []),
 "c03_double_hash_in_value": ("input:repeat_rate = 4##0\n", []),
 "c04_negzero_after_30": ("input:repeat_rate = 30\ninput:repeat_rate = -0\n", []),
 "c05_plus_sign": ("input:repeat_rate = +5\n", []),
 "c06_leading_zero": ("input:repeat_rate = 007\n", []),
 "c07_float": ("input:repeat_rate = 3.5\n", []),
 "c08_hex": ("input:repeat_rate = 0x10\n", []),
 "c09_numlock_1_then_2": ("input:numlock_by_default = 1\ninput:numlock_by_default = 2\n", []),
 "c10_rate_300": ("input:repeat_rate = 300\n", []),
 "c11_var_in_device_name": ("$dev = mykbd\ndevice {\nname = $dev\nrepeat_rate = 50\n}\n", ["mykbd"]),
 "c12_hyprlang_if_false": ("#hyprlang if NOPE\ninput:repeat_rate = 30\n#hyprlang endif\n", []),
 "c13_backslash_comment_joins": ("# disabled \\\ninput:repeat_rate = 30\n", []),
 "c14_source_sub": ("source = " + C + "/c14_sub.conf\n", []),
 "c15_device_key_before_name": ("device {\nrepeat_rate = 50\nname = a\n}\n", ["a"]),
 "c16_plain_global": ("input {\nrepeat_rate = 30\n}\n", []),
 "c17_numlock_online": ("input:numlock_by_default = online\n", []),
 "c18_numlock_nope": ("input:numlock_by_default = nope\n", []),
 "c19_dollar_in_comment": ("input:repeat_rate = 30 # $x\n", []),
 "c20_empty_value": ("input:repeat_rate =\n", []),
 "c21_words_after_digits": ("input:repeat_rate = 30abc\n", []),
 "c22_device_comment_name": ("device {\nname = a # kbd\nrepeat_rate = 50\n}\n", ["a"]),
}
for n, (txt, kbs) in cases.items():
    open(os.path.join(C, n + ".conf"), "w").write(txt)
open(os.path.join(C, "c14_sub.conf"), "w").write("input:repeat_rate = 30\n")
import json
json.dump({k: v[1] for k, v in cases.items()}, open(os.path.join(C, "kbs.json"), "w"))
print(len(cases), "cases")
