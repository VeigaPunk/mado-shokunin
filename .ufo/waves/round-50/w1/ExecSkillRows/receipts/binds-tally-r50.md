# ExecSkillRows r50 — the section's host figures, recomputed from a fresh read-only capture (2026-10-27)
# hyprctl binds -j -> 90401 bytes JSON; Python tally (no raw JSON committed: session material is shape-only)
binds_total: 192
form_tally: {"key_empty_keycode_bind":42,"key_field_keysym_name":142,"key_field_mouse_button":2,"key_field_mouse_dir":4,"key_field_switch":2}
empty_key_with_keycode_nonzero: 42 (all keycode>0: True)
keycode_zero_rows: 150
keycode_range_on_keycode_binds: 10..201
submaps: {"":192}
modmask_tally: {"64":42,"65":37,"68":26,"0":23,"73":22,"72":19,"8":7,"76":6,"69":3,"1":2,"12":2,"9":2,"13":1}
# modmask decoding from IKeyboard.hpp:13-22: SHIFT=1<<0, CTRL=1<<2, META(SUPER)=1<<6, MOD5=1<<7 -> 64=SUPER, 65=SUPER|SHIFT, 68=SUPER|CTRL
SLASH_rows: 1 (modmask [65], keycode [0])
mouse_button_keys_present: ['mouse:272', 'mouse:273']
mouse_dir_keys_present: ['mouse_down', 'mouse_up']
switch_rows: 2 (names withheld: device material)

# hyprctl devices -j -> keyboards=10, layout values={"br":10}
# device names withheld: session material is shape-only (no home paths, no serials, no account name)

# section claims checked against this tally:
  142 of 192 name a keysym          -> 142 of 192
  42 empty key with a keycode       -> 42
  2 mouse:N, 4 mouse_*, 2 switch:   -> 2, 4, 2
  all 192 bind submaps empty        -> True
