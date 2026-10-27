# ExecSkillRows r50 — the section's parity sentence, measured on the judge's own argument form (--keymap=FILE)
# judge: /usr/lib/xkbcommon/xkbcli-how-to-type --keymap=FILE --disable-compose --keysym ARG
# tool : python3 tools/mado-keysym.py how-to-type --keymap FILE --disable-compose --keysym ARG
# compare: stdout byte-equal and exit code equal. keymap sha256=efd487a399201523540f4e5bbf81818be3183f6d9957c2f2b12469a2cf6fce81 (73079 B)
slash            judge rc=0   505B | tool rc=0   505B | equal
SLASH            judge rc=2     0B | tool rc=2     0B | equal
0x2f             judge rc=0   505B | tool rc=0   505B | equal
U002F            judge rc=0   505B | tool rc=0   505B | equal
47               judge rc=0   505B | tool rc=0   505B | equal
XKB_KEY_a        judge rc=2     0B | tool rc=2     0B | equal
U+002F           judge rc=2     0B | tool rc=2     0B | equal
0X2F             judge rc=2     0B | tool rc=2     0B | equal
Return           judge rc=0   176B | tool rc=0   176B | equal
nosuchsym        judge rc=2     0B | tool rc=2     0B | equal
0x0100           judge rc=0   119B | tool rc=0   119B | equal
Caps_Lock        judge rc=0   118B | tool rc=0   118B | equal
Num_Lock         judge rc=0   178B | tool rc=0   178B | equal
Multi_key        judge rc=0   246B | tool rc=0   246B | equal
dead_acute       judge rc=0   339B | tool rc=0   339B | equal
a                judge rc=0   171B | tool rc=0   171B | equal
s                judge rc=0   171B | tool rc=0   171B | equal
0x41             judge rc=0   243B | tool rc=0   243B | equal
U20AC            judge rc=0   117B | tool rc=0   117B | equal
U00E9            judge rc=0   115B | tool rc=0   115B | equal
XF86AudioMute    judge rc=0   187B | tool rc=0   187B | equal
Shift_L          judge rc=0   177B | tool rc=0   177B | equal
Control_L        judge rc=0   179B | tool rc=0   179B | equal
Alt_L            judge rc=0   242B | tool rc=0   242B | equal
Super_L          judge rc=0   244B | tool rc=0   244B | equal
ISO_Level3_Shift judge rc=0   247B | tool rc=0   247B | equal
KP_Enter         judge rc=0   178B | tool rc=0   178B | equal
BackSpace        judge rc=0   246B | tool rc=0   246B | equal
Tab              judge rc=0   173B | tool rc=0   173B | equal
Escape           judge rc=0   176B | tool rc=0   176B | equal
space            judge rc=0   175B | tool rc=0   175B | equal
comma            judge rc=0   175B | tool rc=0   175B | equal
period           judge rc=0   176B | tool rc=0   176B | equal
bracketleft      judge rc=0   258B | tool rc=0   258B | equal
numbersign       judge rc=0   186B | tool rc=0   186B | equal
dead_grave       judge rc=0   186B | tool rc=0   186B | equal
greek_alpha      judge rc=2     0B | tool rc=2     0B | equal
yen              judge rc=0   283B | tool rc=0   283B | equal
ro               judge rc=2     0B | tool rc=2     0B | equal
total=39 equal=39 differs=0 
