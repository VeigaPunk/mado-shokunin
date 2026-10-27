#!/usr/bin/env python3
"""mado-keysym reference B — independent reimplementation of libxkbcommon's
`xkbcli how-to-type --keymap=FILE --disable-compose --keysym ARG`.

Reads a keymap SERIALIZED by `xkbcli compile-keymap` (text_v1, pretty) plus a
keysym argument, and reproduces the judge byte for byte on stdout together with
its exit status.  Python 3 standard library only; starts no process, opens no
socket, writes nothing but stdout/stderr.

Semantics transcribed from libxkbcommon 1.13.2 (pins in the seat receipt):
  tools/how-to-type.c        argument handling, output format, iteration order
  src/keymap.c               xkb_keymap_key_get_mods_for_level and friends
  src/xkbcomp/keymap-dump.c  the text form this parser consumes
  src/xkbcomp/keymap.c       vmod -> real mod derivation, entry deactivation
  src/xkbcomp/symbols.c      trailing-NoSymbol drop, automatic type detection
  src/xkbcomp/types.c        type entries, num_levels
  src/xkbcomp/vmod.c         explicit virtual_modifiers mappings
  src/keysym.c               xkb_keysym_from_name / xkb_keysym_get_name
  src/keysym-case-mappings.c is_lower / is_upper_or_title (type detection)
  src/keysym-utf.c           utf32 -> keysym normalisation
  src/ks_tables.h            canonical and alias keysym name tables

Public API
    parse_keymap(text)          -> Keymap
    keysym_from_arg(arg)        -> int or None
    how_to_type(keymap, ks)     -> (stdout_text, return_code)
"""

import re
import sys

# --------------------------------------------------------------------------
# constants (xkbcommon-keysyms.h, src/keysym.h, src/keymap.h)
# --------------------------------------------------------------------------

REAL_MODS = ("Shift", "Lock", "Control", "Mod1", "Mod2", "Mod3", "Mod4", "Mod5")
MOD_REAL_MASK_ALL = 0xFF
NUM_REAL_MODS = 8
MAX_TYPE_MAP_ENTRIES = 100

XKB_KEYSYM_MAX = 0x1FFFFFFF
XKB_KEYSYM_UNICODE_OFFSET = 0x01000000
XKB_KEYSYM_UNICODE_MIN = 0x01000100
XKB_KEYSYM_UNICODE_MAX = 0x0110FFFF
XKB_KEY_NoSymbol = 0x0
XKB_KEY_Delete = 0xFFFF
KEYPAD_FIRST = 0xFF80   # XKB_KEY_KP_Space
KEYPAD_LAST = 0xFFBD    # XKB_KEY_KP_Equal

USAGE = (
    "Usage: %s [--help] [--verbose] [--keysym] [--disable-compose] "
    "[--rules <rules>] [--model <model>] "
    "[--layout <layout>] [--variant <variant>] "
    "[--options <options>] [--enable-environment-names] "
    "<character/codepoint/keysym>\n"
)

# --- BEGIN GENERATED TABLES (libxkbcommon 1.13.2, pinned) ---
# name_to_keysym: every explicit name, in libxkbcommon table order (alias order matters
# for case-insensitive lookup: the LAST case-insensitive match wins).
_NAME_TO_KEYSYM_ORDER = [
    ('0',0x30),('1',0x31),('2',0x32),('3',0x33),
    ('3270_AltCursor',0xfd10),('3270_Attn',0xfd0e),('3270_BackTab',0xfd05),('3270_ChangeScreen',0xfd19),
    ('3270_Copy',0xfd15),('3270_CursorBlink',0xfd0f),('3270_CursorSelect',0xfd1c),('3270_DeleteWord',0xfd1a),
    ('3270_Duplicate',0xfd01),('3270_Enter',0xfd1e),('3270_EraseEOF',0xfd06),('3270_EraseInput',0xfd07),
    ('3270_ExSelect',0xfd1b),('3270_FieldMark',0xfd02),('3270_Ident',0xfd13),('3270_Jump',0xfd12),
    ('3270_KeyClick',0xfd11),('3270_Left2',0xfd04),('3270_PA1',0xfd0a),('3270_PA2',0xfd0b),
    ('3270_PA3',0xfd0c),('3270_Play',0xfd16),('3270_PrintScreen',0xfd1d),('3270_Quit',0xfd09),
    ('3270_Record',0xfd18),('3270_Reset',0xfd08),('3270_Right2',0xfd03),('3270_Rule',0xfd14),
    ('3270_Setup',0xfd17),('3270_Test',0xfd0d),('4',0x34),('5',0x35),
    ('6',0x36),('7',0x37),('8',0x38),('9',0x39),
    ('A',0x41),('a',0x61),('Aacute',0xc1),('aacute',0xe1),
    ('Abelowdot',0x1001ea0),('abelowdot',0x1001ea1),('abovedot',0x1ff),('Abreve',0x1c3),
    ('abreve',0x1e3),('Abreveacute',0x1001eae),('abreveacute',0x1001eaf),('Abrevebelowdot',0x1001eb6),
    ('abrevebelowdot',0x1001eb7),('Abrevegrave',0x1001eb0),('abrevegrave',0x1001eb1),('Abrevehook',0x1001eb2),
    ('abrevehook',0x1001eb3),('Abrevetilde',0x1001eb4),('abrevetilde',0x1001eb5),('AccessX_Enable',0xfe70),
    ('AccessX_Feedback_Enable',0xfe71),('Acircumflex',0xc2),('acircumflex',0xe2),('Acircumflexacute',0x1001ea4),
    ('acircumflexacute',0x1001ea5),('Acircumflexbelowdot',0x1001eac),('acircumflexbelowdot',0x1001ead),('Acircumflexgrave',0x1001ea6),
    ('acircumflexgrave',0x1001ea7),('Acircumflexhook',0x1001ea8),('acircumflexhook',0x1001ea9),('Acircumflextilde',0x1001eaa),
    ('acircumflextilde',0x1001eab),('acute',0xb4),('Adiaeresis',0xc4),('adiaeresis',0xe4),
    ('AE',0xc6),('ae',0xe6),('Agrave',0xc0),('agrave',0xe0),
    ('Ahook',0x1001ea2),('ahook',0x1001ea3),('Alt_L',0xffe9),('Alt_R',0xffea),
    ('Amacron',0x3c0),('amacron',0x3e0),('ampersand',0x26),('Aogonek',0x1a1),
    ('aogonek',0x1b1),('apostrophe',0x27),('approxeq',0x1002248),('approximate',0x8c8),
    ('Arabic_0',0x1000660),('Arabic_1',0x1000661),('Arabic_2',0x1000662),('Arabic_3',0x1000663),
    ('Arabic_4',0x1000664),('Arabic_5',0x1000665),('Arabic_6',0x1000666),('Arabic_7',0x1000667),
    ('Arabic_8',0x1000668),('Arabic_9',0x1000669),('Arabic_ain',0x5d9),('Arabic_alef',0x5c7),
    ('Arabic_alefmaksura',0x5e9),('Arabic_beh',0x5c8),('Arabic_comma',0x5ac),('Arabic_dad',0x5d6),
    ('Arabic_dal',0x5cf),('Arabic_damma',0x5ef),('Arabic_dammatan',0x5ec),('Arabic_ddal',0x1000688),
    ('Arabic_farsi_yeh',0x10006cc),('Arabic_fatha',0x5ee),('Arabic_fathatan',0x5eb),('Arabic_feh',0x5e1),
    ('Arabic_fullstop',0x10006d4),('Arabic_gaf',0x10006af),('Arabic_ghain',0x5da),('Arabic_ha',0x5e7),
    ('Arabic_hah',0x5cd),('Arabic_hamza',0x5c1),('Arabic_hamza_above',0x1000654),('Arabic_hamza_below',0x1000655),
    ('Arabic_hamzaonalef',0x5c3),('Arabic_hamzaonwaw',0x5c4),('Arabic_hamzaonyeh',0x5c6),('Arabic_hamzaunderalef',0x5c5),
    ('Arabic_heh',0x5e7),('Arabic_heh_doachashmee',0x10006be),('Arabic_heh_goal',0x10006c1),('Arabic_jeem',0x5cc),
    ('Arabic_jeh',0x1000698),('Arabic_kaf',0x5e3),('Arabic_kasra',0x5f0),('Arabic_kasratan',0x5ed),
    ('Arabic_keheh',0x10006a9),('Arabic_khah',0x5ce),('Arabic_lam',0x5e4),('Arabic_madda_above',0x1000653),
    ('Arabic_maddaonalef',0x5c2),('Arabic_meem',0x5e5),('Arabic_noon',0x5e6),('Arabic_noon_ghunna',0x10006ba),
    ('Arabic_peh',0x100067e),('Arabic_percent',0x100066a),('Arabic_qaf',0x5e2),('Arabic_question_mark',0x5bf),
    ('Arabic_ra',0x5d1),('Arabic_rreh',0x1000691),('Arabic_sad',0x5d5),('Arabic_seen',0x5d3),
    ('Arabic_semicolon',0x5bb),('Arabic_shadda',0x5f1),('Arabic_sheen',0x5d4),('Arabic_sukun',0x5f2),
    ('Arabic_superscript_alef',0x1000670),('Arabic_switch',0xff7e),('Arabic_tah',0x5d7),('Arabic_tatweel',0x5e0),
    ('Arabic_tcheh',0x1000686),('Arabic_teh',0x5ca),('Arabic_tehmarbuta',0x5c9),('Arabic_thal',0x5d0),
    ('Arabic_theh',0x5cb),('Arabic_tteh',0x1000679),('Arabic_veh',0x10006a4),('Arabic_waw',0x5e8),
    ('Arabic_yeh',0x5ea),('Arabic_yeh_baree',0x10006d2),('Arabic_zah',0x5d8),('Arabic_zain',0x5d2),
    ('Aring',0xc5),('aring',0xe5),('Armenian_accent',0x100055b),('Armenian_amanak',0x100055c),
    ('Armenian_apostrophe',0x100055a),('Armenian_AT',0x1000538),('Armenian_at',0x1000568),('Armenian_AYB',0x1000531),
    ('Armenian_ayb',0x1000561),('Armenian_BEN',0x1000532),('Armenian_ben',0x1000562),('Armenian_but',0x100055d),
    ('Armenian_CHA',0x1000549),('Armenian_cha',0x1000579),('Armenian_DA',0x1000534),('Armenian_da',0x1000564),
    ('Armenian_DZA',0x1000541),('Armenian_dza',0x1000571),('Armenian_E',0x1000537),('Armenian_e',0x1000567),
    ('Armenian_exclam',0x100055c),('Armenian_FE',0x1000556),('Armenian_fe',0x1000586),('Armenian_full_stop',0x1000589),
    ('Armenian_GHAT',0x1000542),('Armenian_ghat',0x1000572),('Armenian_GIM',0x1000533),('Armenian_gim',0x1000563),
    ('Armenian_HI',0x1000545),('Armenian_hi',0x1000575),('Armenian_HO',0x1000540),('Armenian_ho',0x1000570),
    ('Armenian_hyphen',0x100058a),('Armenian_INI',0x100053b),('Armenian_ini',0x100056b),('Armenian_JE',0x100054b),
    ('Armenian_je',0x100057b),('Armenian_KE',0x1000554),('Armenian_ke',0x1000584),('Armenian_KEN',0x100053f),
    ('Armenian_ken',0x100056f),('Armenian_KHE',0x100053d),('Armenian_khe',0x100056d),('Armenian_ligature_ew',0x1000587),
    ('Armenian_LYUN',0x100053c),('Armenian_lyun',0x100056c),('Armenian_MEN',0x1000544),('Armenian_men',0x1000574),
    ('Armenian_NU',0x1000546),('Armenian_nu',0x1000576),('Armenian_O',0x1000555),('Armenian_o',0x1000585),
    ('Armenian_paruyk',0x100055e),('Armenian_PE',0x100054a),('Armenian_pe',0x100057a),('Armenian_PYUR',0x1000553),
    ('Armenian_pyur',0x1000583),('Armenian_question',0x100055e),('Armenian_RA',0x100054c),('Armenian_ra',0x100057c),
    ('Armenian_RE',0x1000550),('Armenian_re',0x1000580),('Armenian_SE',0x100054d),('Armenian_se',0x100057d),
    ('Armenian_separation_mark',0x100055d),('Armenian_SHA',0x1000547),('Armenian_sha',0x1000577),('Armenian_shesht',0x100055b),
    ('Armenian_TCHE',0x1000543),('Armenian_tche',0x1000573),('Armenian_TO',0x1000539),('Armenian_to',0x1000569),
    ('Armenian_TSA',0x100053e),('Armenian_tsa',0x100056e),('Armenian_TSO',0x1000551),('Armenian_tso',0x1000581),
    ('Armenian_TYUN',0x100054f),('Armenian_tyun',0x100057f),('Armenian_verjaket',0x1000589),('Armenian_VEV',0x100054e),
    ('Armenian_vev',0x100057e),('Armenian_VO',0x1000548),('Armenian_vo',0x1000578),('Armenian_VYUN',0x1000552),
    ('Armenian_vyun',0x1000582),('Armenian_YECH',0x1000535),('Armenian_yech',0x1000565),('Armenian_yentamna',0x100058a),
    ('Armenian_ZA',0x1000536),('Armenian_za',0x1000566),('Armenian_ZHE',0x100053a),('Armenian_zhe',0x100056a),
    ('asciicircum',0x5e),('asciitilde',0x7e),('asterisk',0x2a),('at',0x40),
    ('Atilde',0xc3),('atilde',0xe3),('AudibleBell_Enable',0xfe7a),('B',0x42),
    ('b',0x62),('Babovedot',0x1001e02),('babovedot',0x1001e03),('backslash',0x5c),
    ('BackSpace',0xff08),('BackTab',0x1000ff74),('ballotcross',0xaf4),('bar',0x7c),
    ('because',0x1002235),('Begin',0xff58),('blank',0x9df),('block',0x100000fc),
    ('botintegral',0x8a5),('botleftparens',0x8ac),('botleftsqbracket',0x8a8),('botleftsummation',0x8b2),
    ('botrightparens',0x8ae),('botrightsqbracket',0x8aa),('botrightsummation',0x8b6),('bott',0x9f6),
    ('botvertsummationconnector',0x8b4),('BounceKeys_Enable',0xfe74),('braceleft',0x7b),('braceright',0x7d),
    ('bracketleft',0x5b),('bracketright',0x5d),('braille_blank',0x1002800),('braille_dot_1',0xfff1),
    ('braille_dot_10',0xfffa),('braille_dot_2',0xfff2),('braille_dot_3',0xfff3),('braille_dot_4',0xfff4),
    ('braille_dot_5',0xfff5),('braille_dot_6',0xfff6),('braille_dot_7',0xfff7),('braille_dot_8',0xfff8),
    ('braille_dot_9',0xfff9),('braille_dots_1',0x1002801),('braille_dots_12',0x1002803),('braille_dots_123',0x1002807),
    ('braille_dots_1234',0x100280f),('braille_dots_12345',0x100281f),('braille_dots_123456',0x100283f),('braille_dots_1234567',0x100287f),
    ('braille_dots_12345678',0x10028ff),('braille_dots_1234568',0x10028bf),('braille_dots_123457',0x100285f),('braille_dots_1234578',0x10028df),
    ('braille_dots_123458',0x100289f),('braille_dots_12346',0x100282f),('braille_dots_123467',0x100286f),('braille_dots_1234678',0x10028ef),
    ('braille_dots_123468',0x10028af),('braille_dots_12347',0x100284f),('braille_dots_123478',0x10028cf),('braille_dots_12348',0x100288f),
    ('braille_dots_1235',0x1002817),('braille_dots_12356',0x1002837),('braille_dots_123567',0x1002877),('braille_dots_1235678',0x10028f7),
    ('braille_dots_123568',0x10028b7),('braille_dots_12357',0x1002857),('braille_dots_123578',0x10028d7),('braille_dots_12358',0x1002897),
    ('braille_dots_1236',0x1002827),('braille_dots_12367',0x1002867),('braille_dots_123678',0x10028e7),('braille_dots_12368',0x10028a7),
    ('braille_dots_1237',0x1002847),('braille_dots_12378',0x10028c7),('braille_dots_1238',0x1002887),('braille_dots_124',0x100280b),
    ('braille_dots_1245',0x100281b),('braille_dots_12456',0x100283b),('braille_dots_124567',0x100287b),('braille_dots_1245678',0x10028fb),
    ('braille_dots_124568',0x10028bb),('braille_dots_12457',0x100285b),('braille_dots_124578',0x10028db),('braille_dots_12458',0x100289b),
    ('braille_dots_1246',0x100282b),('braille_dots_12467',0x100286b),('braille_dots_124678',0x10028eb),('braille_dots_12468',0x10028ab),
    ('braille_dots_1247',0x100284b),('braille_dots_12478',0x10028cb),('braille_dots_1248',0x100288b),('braille_dots_125',0x1002813),
    ('braille_dots_1256',0x1002833),('braille_dots_12567',0x1002873),('braille_dots_125678',0x10028f3),('braille_dots_12568',0x10028b3),
    ('braille_dots_1257',0x1002853),('braille_dots_12578',0x10028d3),('braille_dots_1258',0x1002893),('braille_dots_126',0x1002823),
    ('braille_dots_1267',0x1002863),('braille_dots_12678',0x10028e3),('braille_dots_1268',0x10028a3),('braille_dots_127',0x1002843),
    ('braille_dots_1278',0x10028c3),('braille_dots_128',0x1002883),('braille_dots_13',0x1002805),('braille_dots_134',0x100280d),
    ('braille_dots_1345',0x100281d),('braille_dots_13456',0x100283d),('braille_dots_134567',0x100287d),('braille_dots_1345678',0x10028fd),
    ('braille_dots_134568',0x10028bd),('braille_dots_13457',0x100285d),('braille_dots_134578',0x10028dd),('braille_dots_13458',0x100289d),
    ('braille_dots_1346',0x100282d),('braille_dots_13467',0x100286d),('braille_dots_134678',0x10028ed),('braille_dots_13468',0x10028ad),
    ('braille_dots_1347',0x100284d),('braille_dots_13478',0x10028cd),('braille_dots_1348',0x100288d),('braille_dots_135',0x1002815),
    ('braille_dots_1356',0x1002835),('braille_dots_13567',0x1002875),('braille_dots_135678',0x10028f5),('braille_dots_13568',0x10028b5),
    ('braille_dots_1357',0x1002855),('braille_dots_13578',0x10028d5),('braille_dots_1358',0x1002895),('braille_dots_136',0x1002825),
    ('braille_dots_1367',0x1002865),('braille_dots_13678',0x10028e5),('braille_dots_1368',0x10028a5),('braille_dots_137',0x1002845),
    ('braille_dots_1378',0x10028c5),('braille_dots_138',0x1002885),('braille_dots_14',0x1002809),('braille_dots_145',0x1002819),
    ('braille_dots_1456',0x1002839),('braille_dots_14567',0x1002879),('braille_dots_145678',0x10028f9),('braille_dots_14568',0x10028b9),
    ('braille_dots_1457',0x1002859),('braille_dots_14578',0x10028d9),('braille_dots_1458',0x1002899),('braille_dots_146',0x1002829),
    ('braille_dots_1467',0x1002869),('braille_dots_14678',0x10028e9),('braille_dots_1468',0x10028a9),('braille_dots_147',0x1002849),
    ('braille_dots_1478',0x10028c9),('braille_dots_148',0x1002889),('braille_dots_15',0x1002811),('braille_dots_156',0x1002831),
    ('braille_dots_1567',0x1002871),('braille_dots_15678',0x10028f1),('braille_dots_1568',0x10028b1),('braille_dots_157',0x1002851),
    ('braille_dots_1578',0x10028d1),('braille_dots_158',0x1002891),('braille_dots_16',0x1002821),('braille_dots_167',0x1002861),
    ('braille_dots_1678',0x10028e1),('braille_dots_168',0x10028a1),('braille_dots_17',0x1002841),('braille_dots_178',0x10028c1),
    ('braille_dots_18',0x1002881),('braille_dots_2',0x1002802),('braille_dots_23',0x1002806),('braille_dots_234',0x100280e),
    ('braille_dots_2345',0x100281e),('braille_dots_23456',0x100283e),('braille_dots_234567',0x100287e),('braille_dots_2345678',0x10028fe),
    ('braille_dots_234568',0x10028be),('braille_dots_23457',0x100285e),('braille_dots_234578',0x10028de),('braille_dots_23458',0x100289e),
    ('braille_dots_2346',0x100282e),('braille_dots_23467',0x100286e),('braille_dots_234678',0x10028ee),('braille_dots_23468',0x10028ae),
    ('braille_dots_2347',0x100284e),('braille_dots_23478',0x10028ce),('braille_dots_2348',0x100288e),('braille_dots_235',0x1002816),
    ('braille_dots_2356',0x1002836),('braille_dots_23567',0x1002876),('braille_dots_235678',0x10028f6),('braille_dots_23568',0x10028b6),
    ('braille_dots_2357',0x1002856),('braille_dots_23578',0x10028d6),('braille_dots_2358',0x1002896),('braille_dots_236',0x1002826),
    ('braille_dots_2367',0x1002866),('braille_dots_23678',0x10028e6),('braille_dots_2368',0x10028a6),('braille_dots_237',0x1002846),
    ('braille_dots_2378',0x10028c6),('braille_dots_238',0x1002886),('braille_dots_24',0x100280a),('braille_dots_245',0x100281a),
    ('braille_dots_2456',0x100283a),('braille_dots_24567',0x100287a),('braille_dots_245678',0x10028fa),('braille_dots_24568',0x10028ba),
    ('braille_dots_2457',0x100285a),('braille_dots_24578',0x10028da),('braille_dots_2458',0x100289a),('braille_dots_246',0x100282a),
    ('braille_dots_2467',0x100286a),('braille_dots_24678',0x10028ea),('braille_dots_2468',0x10028aa),('braille_dots_247',0x100284a),
    ('braille_dots_2478',0x10028ca),('braille_dots_248',0x100288a),('braille_dots_25',0x1002812),('braille_dots_256',0x1002832),
    ('braille_dots_2567',0x1002872),('braille_dots_25678',0x10028f2),('braille_dots_2568',0x10028b2),('braille_dots_257',0x1002852),
    ('braille_dots_2578',0x10028d2),('braille_dots_258',0x1002892),('braille_dots_26',0x1002822),('braille_dots_267',0x1002862),
    ('braille_dots_2678',0x10028e2),('braille_dots_268',0x10028a2),('braille_dots_27',0x1002842),('braille_dots_278',0x10028c2),
    ('braille_dots_28',0x1002882),('braille_dots_3',0x1002804),('braille_dots_34',0x100280c),('braille_dots_345',0x100281c),
    ('braille_dots_3456',0x100283c),('braille_dots_34567',0x100287c),('braille_dots_345678',0x10028fc),('braille_dots_34568',0x10028bc),
    ('braille_dots_3457',0x100285c),('braille_dots_34578',0x10028dc),('braille_dots_3458',0x100289c),('braille_dots_346',0x100282c),
    ('braille_dots_3467',0x100286c),('braille_dots_34678',0x10028ec),('braille_dots_3468',0x10028ac),('braille_dots_347',0x100284c),
    ('braille_dots_3478',0x10028cc),('braille_dots_348',0x100288c),('braille_dots_35',0x1002814),('braille_dots_356',0x1002834),
    ('braille_dots_3567',0x1002874),('braille_dots_35678',0x10028f4),('braille_dots_3568',0x10028b4),('braille_dots_357',0x1002854),
    ('braille_dots_3578',0x10028d4),('braille_dots_358',0x1002894),('braille_dots_36',0x1002824),('braille_dots_367',0x1002864),
    ('braille_dots_3678',0x10028e4),('braille_dots_368',0x10028a4),('braille_dots_37',0x1002844),('braille_dots_378',0x10028c4),
    ('braille_dots_38',0x1002884),('braille_dots_4',0x1002808),('braille_dots_45',0x1002818),('braille_dots_456',0x1002838),
    ('braille_dots_4567',0x1002878),('braille_dots_45678',0x10028f8),('braille_dots_4568',0x10028b8),('braille_dots_457',0x1002858),
    ('braille_dots_4578',0x10028d8),('braille_dots_458',0x1002898),('braille_dots_46',0x1002828),('braille_dots_467',0x1002868),
    ('braille_dots_4678',0x10028e8),('braille_dots_468',0x10028a8),('braille_dots_47',0x1002848),('braille_dots_478',0x10028c8),
    ('braille_dots_48',0x1002888),('braille_dots_5',0x1002810),('braille_dots_56',0x1002830),('braille_dots_567',0x1002870),
    ('braille_dots_5678',0x10028f0),('braille_dots_568',0x10028b0),('braille_dots_57',0x1002850),('braille_dots_578',0x10028d0),
    ('braille_dots_58',0x1002890),('braille_dots_6',0x1002820),('braille_dots_67',0x1002860),('braille_dots_678',0x10028e0),
    ('braille_dots_68',0x10028a0),('braille_dots_7',0x1002840),('braille_dots_78',0x10028c0),('braille_dots_8',0x1002880),
    ('Break',0xff6b),('breve',0x1a2),('brokenbar',0xa6),('Byelorussian_SHORTU',0x6be),
    ('Byelorussian_shortu',0x6ae),('C',0x43),('c',0x63),('C_H',0xfea5),
    ('C_h',0xfea4),('c_h',0xfea3),('Cabovedot',0x2c5),('cabovedot',0x2e5),
    ('Cacute',0x1c6),('cacute',0x1e6),('Cancel',0xff69),('Caps_Lock',0xffe5),
    ('careof',0xab8),('caret',0xafc),('caron',0x1b7),('Ccaron',0x1c8),
    ('ccaron',0x1e8),('Ccedilla',0xc7),('ccedilla',0xe7),('Ccircumflex',0x2c6),
    ('ccircumflex',0x2e6),('cedilla',0xb8),('cent',0xa2),('CH',0xfea2),
    ('Ch',0xfea1),('ch',0xfea0),('checkerboard',0x9e1),('checkmark',0xaf3),
    ('circle',0xbcf),('Clear',0xff0b),('ClearLine',0x1000ff6f),('club',0xaec),
    ('Codeinput',0xff37),('colon',0x3a),('ColonSign',0x10020a1),('combining_acute',0x1000301),
    ('combining_belowdot',0x1000323),('combining_grave',0x1000300),('combining_hook',0x1000309),('combining_tilde',0x1000303),
    ('comma',0x2c),('containsas',0x100220b),('Control_L',0xffe3),('Control_R',0xffe4),
    ('copyright',0xa9),('cr',0x9e4),('crossinglines',0x9ee),('CruzeiroSign',0x10020a2),
    ('cuberoot',0x100221b),('currency',0xa4),('cursor',0xaff),('Cyrillic_A',0x6e1),
    ('Cyrillic_a',0x6c1),('Cyrillic_BE',0x6e2),('Cyrillic_be',0x6c2),('Cyrillic_CHE',0x6fe),
    ('Cyrillic_che',0x6de),('Cyrillic_CHE_descender',0x10004b6),('Cyrillic_che_descender',0x10004b7),('Cyrillic_CHE_vertstroke',0x10004b8),
    ('Cyrillic_che_vertstroke',0x10004b9),('Cyrillic_DE',0x6e4),('Cyrillic_de',0x6c4),('Cyrillic_DZHE',0x6bf),
    ('Cyrillic_dzhe',0x6af),('Cyrillic_E',0x6fc),('Cyrillic_e',0x6dc),('Cyrillic_EF',0x6e6),
    ('Cyrillic_ef',0x6c6),('Cyrillic_EL',0x6ec),('Cyrillic_el',0x6cc),('Cyrillic_EM',0x6ed),
    ('Cyrillic_em',0x6cd),('Cyrillic_EN',0x6ee),('Cyrillic_en',0x6ce),('Cyrillic_EN_descender',0x10004a2),
    ('Cyrillic_en_descender',0x10004a3),('Cyrillic_ER',0x6f2),('Cyrillic_er',0x6d2),('Cyrillic_ES',0x6f3),
    ('Cyrillic_es',0x6d3),('Cyrillic_GHE',0x6e7),('Cyrillic_ghe',0x6c7),('Cyrillic_GHE_bar',0x1000492),
    ('Cyrillic_ghe_bar',0x1000493),('Cyrillic_HA',0x6e8),('Cyrillic_ha',0x6c8),('Cyrillic_HA_descender',0x10004b2),
    ('Cyrillic_ha_descender',0x10004b3),('Cyrillic_HARDSIGN',0x6ff),('Cyrillic_hardsign',0x6df),('Cyrillic_I',0x6e9),
    ('Cyrillic_i',0x6c9),('Cyrillic_I_macron',0x10004e2),('Cyrillic_i_macron',0x10004e3),('Cyrillic_IE',0x6e5),
    ('Cyrillic_ie',0x6c5),('Cyrillic_IO',0x6b3),('Cyrillic_io',0x6a3),('Cyrillic_JE',0x6b8),
    ('Cyrillic_je',0x6a8),('Cyrillic_KA',0x6eb),('Cyrillic_ka',0x6cb),('Cyrillic_KA_descender',0x100049a),
    ('Cyrillic_ka_descender',0x100049b),('Cyrillic_KA_vertstroke',0x100049c),('Cyrillic_ka_vertstroke',0x100049d),('Cyrillic_LJE',0x6b9),
    ('Cyrillic_lje',0x6a9),('Cyrillic_NJE',0x6ba),('Cyrillic_nje',0x6aa),('Cyrillic_O',0x6ef),
    ('Cyrillic_o',0x6cf),('Cyrillic_O_bar',0x10004e8),('Cyrillic_o_bar',0x10004e9),('Cyrillic_PE',0x6f0),
    ('Cyrillic_pe',0x6d0),('Cyrillic_SCHWA',0x10004d8),('Cyrillic_schwa',0x10004d9),('Cyrillic_SHA',0x6fb),
    ('Cyrillic_sha',0x6db),('Cyrillic_SHCHA',0x6fd),('Cyrillic_shcha',0x6dd),('Cyrillic_SHHA',0x10004ba),
    ('Cyrillic_shha',0x10004bb),('Cyrillic_SHORTI',0x6ea),('Cyrillic_shorti',0x6ca),('Cyrillic_SOFTSIGN',0x6f8),
    ('Cyrillic_softsign',0x6d8),('Cyrillic_TE',0x6f4),('Cyrillic_te',0x6d4),('Cyrillic_TSE',0x6e3),
    ('Cyrillic_tse',0x6c3),('Cyrillic_U',0x6f5),('Cyrillic_u',0x6d5),('Cyrillic_U_macron',0x10004ee),
    ('Cyrillic_u_macron',0x10004ef),('Cyrillic_U_straight',0x10004ae),('Cyrillic_u_straight',0x10004af),('Cyrillic_U_straight_bar',0x10004b0),
    ('Cyrillic_u_straight_bar',0x10004b1),('Cyrillic_VE',0x6f7),('Cyrillic_ve',0x6d7),('Cyrillic_YA',0x6f1),
    ('Cyrillic_ya',0x6d1),('Cyrillic_YERU',0x6f9),('Cyrillic_yeru',0x6d9),('Cyrillic_YU',0x6e0),
    ('Cyrillic_yu',0x6c0),('Cyrillic_ZE',0x6fa),('Cyrillic_ze',0x6da),('Cyrillic_ZHE',0x6f6),
    ('Cyrillic_zhe',0x6d6),('Cyrillic_ZHE_descender',0x1000496),('Cyrillic_zhe_descender',0x1000497),('D',0x44),
    ('d',0x64),('Dabovedot',0x1001e0a),('dabovedot',0x1001e0b),('Dacute_accent',0x1000fe27),
    ('dagger',0xaf1),('Dcaron',0x1cf),('dcaron',0x1ef),('Dcedilla_accent',0x1000fe2c),
    ('Dcircumflex_accent',0x1000fe5e),('Ddiaeresis',0x1000fe22),('dead_A',0xfe81),('dead_a',0xfe80),
    ('dead_abovecomma',0xfe64),('dead_abovedot',0xfe56),('dead_abovereversedcomma',0xfe65),('dead_abovering',0xfe58),
    ('dead_aboveverticalline',0xfe91),('dead_acute',0xfe51),('dead_apostrophe',0xfe8e),('dead_belowbreve',0xfe6b),
    ('dead_belowcircumflex',0xfe69),('dead_belowcomma',0xfe6e),('dead_belowdiaeresis',0xfe6c),('dead_belowdot',0xfe60),
    ('dead_belowmacron',0xfe68),('dead_belowring',0xfe67),('dead_belowtilde',0xfe6a),('dead_belowverticalline',0xfe92),
    ('dead_breve',0xfe55),('dead_capital_schwa',0xfe8b),('dead_caron',0xfe5a),('dead_cedilla',0xfe5b),
    ('dead_circumflex',0xfe52),('dead_currency',0xfe6f),('dead_dasia',0xfe65),('dead_diaeresis',0xfe57),
    ('dead_doubleacute',0xfe59),('dead_doublegrave',0xfe66),('dead_E',0xfe83),('dead_e',0xfe82),
    ('dead_grave',0xfe50),('dead_greek',0xfe8c),('dead_hamza',0xfe8d),('dead_hook',0xfe61),
    ('dead_horn',0xfe62),('dead_I',0xfe85),('dead_i',0xfe84),('dead_invertedbreve',0xfe6d),
    ('dead_iota',0xfe5d),('dead_longsolidusoverlay',0xfe93),('dead_lowline',0xfe90),('dead_macron',0xfe54),
    ('dead_O',0xfe87),('dead_o',0xfe86),('dead_ogonek',0xfe5c),('dead_perispomeni',0xfe53),
    ('dead_psili',0xfe64),('dead_SCHWA',0xfe8b),('dead_schwa',0xfe8a),('dead_semivoiced_sound',0xfe5f),
    ('dead_small_schwa',0xfe8a),('dead_stroke',0xfe63),('dead_tilde',0xfe53),('dead_U',0xfe89),
    ('dead_u',0xfe88),('dead_voiced_sound',0xfe5e),('decimalpoint',0xabd),('degree',0xb0),
    ('Delete',0xffff),('DeleteChar',0x1000ff73),('DeleteLine',0x1000ff71),('Dgrave_accent',0x1000fe60),
    ('diaeresis',0xa8),('diamond',0xaed),('digitspace',0xaa5),('dintegral',0x100222c),
    ('division',0xf7),('dollar',0x24),('DongSign',0x10020ab),('doubbaselinedot',0xaaf),
    ('doubleacute',0x1bd),('doubledagger',0xaf2),('doublelowquotemark',0xafe),('Down',0xff54),
    ('downarrow',0x8fe),('downcaret',0xba8),('downshoe',0xbd6),('downstile',0xbc4),
    ('downtack',0xbc2),('DRemove',0x1000ff00),('Dring_accent',0x1000feb0),('Dstroke',0x1d0),
    ('dstroke',0x1f0),('Dtilde',0x1000fe7e),('E',0x45),('e',0x65),
    ('Eabovedot',0x3cc),('eabovedot',0x3ec),('Eacute',0xc9),('eacute',0xe9),
    ('Ebelowdot',0x1001eb8),('ebelowdot',0x1001eb9),('Ecaron',0x1cc),('ecaron',0x1ec),
    ('Ecircumflex',0xca),('ecircumflex',0xea),('Ecircumflexacute',0x1001ebe),('ecircumflexacute',0x1001ebf),
    ('Ecircumflexbelowdot',0x1001ec6),('ecircumflexbelowdot',0x1001ec7),('Ecircumflexgrave',0x1001ec0),('ecircumflexgrave',0x1001ec1),
    ('Ecircumflexhook',0x1001ec2),('ecircumflexhook',0x1001ec3),('Ecircumflextilde',0x1001ec4),('ecircumflextilde',0x1001ec5),
    ('EcuSign',0x10020a0),('Ediaeresis',0xcb),('ediaeresis',0xeb),('Egrave',0xc8),
    ('egrave',0xe8),('Ehook',0x1001eba),('ehook',0x1001ebb),('eightsubscript',0x1002088),
    ('eightsuperior',0x1002078),('Eisu_Shift',0xff2f),('Eisu_toggle',0xff30),('elementof',0x1002208),
    ('ellipsis',0xaae),('em3space',0xaa3),('em4space',0xaa4),('Emacron',0x3aa),
    ('emacron',0x3ba),('emdash',0xaa9),('emfilledcircle',0xade),('emfilledrect',0xadf),
    ('emopencircle',0xace),('emopenrectangle',0xacf),('emptyset',0x1002205),('emspace',0xaa1),
    ('End',0xff57),('endash',0xaaa),('enfilledcircbullet',0xae6),('enfilledsqbullet',0xae7),
    ('ENG',0x3bd),('eng',0x3bf),('enopencircbullet',0xae0),('enopensquarebullet',0xae1),
    ('enspace',0xaa2),('Eogonek',0x1ca),('eogonek',0x1ea),('equal',0x3d),
    ('Escape',0xff1b),('ETH',0xd0),('Eth',0xd0),('eth',0xf0),
    ('Etilde',0x1001ebc),('etilde',0x1001ebd),('EuroSign',0x20ac),('exclam',0x21),
    ('exclamdown',0xa1),('Execute',0xff62),('Ext16bit_L',0x1000ff76),('Ext16bit_R',0x1000ff77),
    ('EZH',0x10001b7),('ezh',0x1000292),('F',0x46),('f',0x66),
    ('F1',0xffbe),('F10',0xffc7),('F11',0xffc8),('F12',0xffc9),
    ('F13',0xffca),('F14',0xffcb),('F15',0xffcc),('F16',0xffcd),
    ('F17',0xffce),('F18',0xffcf),('F19',0xffd0),('F2',0xffbf),
    ('F20',0xffd1),('F21',0xffd2),('F22',0xffd3),('F23',0xffd4),
    ('F24',0xffd5),('F25',0xffd6),('F26',0xffd7),('F27',0xffd8),
    ('F28',0xffd9),('F29',0xffda),('F3',0xffc0),('F30',0xffdb),
    ('F31',0xffdc),('F32',0xffdd),('F33',0xffde),('F34',0xffdf),
    ('F35',0xffe0),('F4',0xffc1),('F5',0xffc2),('F6',0xffc3),
    ('F7',0xffc4),('F8',0xffc5),('F9',0xffc6),('Fabovedot',0x1001e1e),
    ('fabovedot',0x1001e1f),('Farsi_0',0x10006f0),('Farsi_1',0x10006f1),('Farsi_2',0x10006f2),
    ('Farsi_3',0x10006f3),('Farsi_4',0x10006f4),('Farsi_5',0x10006f5),('Farsi_6',0x10006f6),
    ('Farsi_7',0x10006f7),('Farsi_8',0x10006f8),('Farsi_9',0x10006f9),('Farsi_yeh',0x10006cc),
    ('femalesymbol',0xaf8),('ff',0x9e3),('FFrancSign',0x10020a3),('figdash',0xabb),
    ('filledlefttribullet',0xadc),('filledrectbullet',0xadb),('filledrighttribullet',0xadd),('filledtribulletdown',0xae9),
    ('filledtribulletup',0xae8),('Find',0xff68),('First_Virtual_Screen',0xfed0),('fiveeighths',0xac5),
    ('fivesixths',0xab7),('fivesubscript',0x1002085),('fivesuperior',0x1002075),('fourfifths',0xab5),
    ('foursubscript',0x1002084),('foursuperior',0x1002074),('fourthroot',0x100221c),('function',0x8f6),
    ('G',0x47),('g',0x67),('Gabovedot',0x2d5),('gabovedot',0x2f5),
    ('Gbreve',0x2ab),('gbreve',0x2bb),('Gcaron',0x10001e6),('gcaron',0x10001e7),
    ('Gcedilla',0x3ab),('gcedilla',0x3bb),('Gcircumflex',0x2d8),('gcircumflex',0x2f8),
    ('Georgian_an',0x10010d0),('Georgian_ban',0x10010d1),('Georgian_can',0x10010ea),('Georgian_char',0x10010ed),
    ('Georgian_chin',0x10010e9),('Georgian_cil',0x10010ec),('Georgian_don',0x10010d3),('Georgian_en',0x10010d4),
    ('Georgian_fi',0x10010f6),('Georgian_gan',0x10010d2),('Georgian_ghan',0x10010e6),('Georgian_hae',0x10010f0),
    ('Georgian_har',0x10010f4),('Georgian_he',0x10010f1),('Georgian_hie',0x10010f2),('Georgian_hoe',0x10010f5),
    ('Georgian_in',0x10010d8),('Georgian_jhan',0x10010ef),('Georgian_jil',0x10010eb),('Georgian_kan',0x10010d9),
    ('Georgian_khar',0x10010e5),('Georgian_las',0x10010da),('Georgian_man',0x10010db),('Georgian_nar',0x10010dc),
    ('Georgian_on',0x10010dd),('Georgian_par',0x10010de),('Georgian_phar',0x10010e4),('Georgian_qar',0x10010e7),
    ('Georgian_rae',0x10010e0),('Georgian_san',0x10010e1),('Georgian_shin',0x10010e8),('Georgian_tan',0x10010d7),
    ('Georgian_tar',0x10010e2),('Georgian_un',0x10010e3),('Georgian_vin',0x10010d5),('Georgian_we',0x10010f3),
    ('Georgian_xan',0x10010ee),('Georgian_zen',0x10010d6),('Georgian_zhar',0x10010df),('grave',0x60),
    ('greater',0x3e),('greaterthanequal',0x8be),('Greek_accentdieresis',0x7ae),('Greek_ALPHA',0x7c1),
    ('Greek_alpha',0x7e1),('Greek_ALPHAaccent',0x7a1),('Greek_alphaaccent',0x7b1),('Greek_BETA',0x7c2),
    ('Greek_beta',0x7e2),('Greek_CHI',0x7d7),('Greek_chi',0x7f7),('Greek_DELTA',0x7c4),
    ('Greek_delta',0x7e4),('Greek_EPSILON',0x7c5),('Greek_epsilon',0x7e5),('Greek_EPSILONaccent',0x7a2),
    ('Greek_epsilonaccent',0x7b2),('Greek_ETA',0x7c7),('Greek_eta',0x7e7),('Greek_ETAaccent',0x7a3),
    ('Greek_etaaccent',0x7b3),('Greek_finalsmallsigma',0x7f3),('Greek_GAMMA',0x7c3),('Greek_gamma',0x7e3),
    ('Greek_horizbar',0x7af),('Greek_IOTA',0x7c9),('Greek_iota',0x7e9),('Greek_IOTAaccent',0x7a4),
    ('Greek_iotaaccent',0x7b4),('Greek_iotaaccentdieresis',0x7b6),('Greek_IOTAdiaeresis',0x7a5),('Greek_IOTAdieresis',0x7a5),
    ('Greek_iotadieresis',0x7b5),('Greek_KAPPA',0x7ca),('Greek_kappa',0x7ea),('Greek_LAMBDA',0x7cb),
    ('Greek_lambda',0x7eb),('Greek_LAMDA',0x7cb),('Greek_lamda',0x7eb),('Greek_MU',0x7cc),
    ('Greek_mu',0x7ec),('Greek_NU',0x7cd),('Greek_nu',0x7ed),('Greek_OMEGA',0x7d9),
    ('Greek_omega',0x7f9),('Greek_OMEGAaccent',0x7ab),('Greek_omegaaccent',0x7bb),('Greek_OMICRON',0x7cf),
    ('Greek_omicron',0x7ef),('Greek_OMICRONaccent',0x7a7),('Greek_omicronaccent',0x7b7),('Greek_PHI',0x7d6),
    ('Greek_phi',0x7f6),('Greek_PI',0x7d0),('Greek_pi',0x7f0),('Greek_PSI',0x7d8),
    ('Greek_psi',0x7f8),('Greek_RHO',0x7d1),('Greek_rho',0x7f1),('Greek_SIGMA',0x7d2),
    ('Greek_sigma',0x7f2),('Greek_switch',0xff7e),('Greek_TAU',0x7d4),('Greek_tau',0x7f4),
    ('Greek_THETA',0x7c8),('Greek_theta',0x7e8),('Greek_UPSILON',0x7d5),('Greek_upsilon',0x7f5),
    ('Greek_UPSILONaccent',0x7a8),('Greek_upsilonaccent',0x7b8),('Greek_upsilonaccentdieresis',0x7ba),('Greek_UPSILONdieresis',0x7a9),
    ('Greek_upsilondieresis',0x7b9),('Greek_XI',0x7ce),('Greek_xi',0x7ee),('Greek_ZETA',0x7c6),
    ('Greek_zeta',0x7e6),('guilder',0x100000be),('guillemetleft',0xab),('guillemetright',0xbb),
    ('guillemotleft',0xab),('guillemotright',0xbb),('H',0x48),('h',0x68),
    ('hairspace',0xaa8),('Hangul',0xff31),('Hangul_A',0xebf),('Hangul_AE',0xec0),
    ('Hangul_AraeA',0xef6),('Hangul_AraeAE',0xef7),('Hangul_Banja',0xff39),('Hangul_Cieuc',0xeba),
    ('Hangul_Codeinput',0xff37),('Hangul_Dikeud',0xea7),('Hangul_E',0xec4),('Hangul_End',0xff33),
    ('Hangul_EO',0xec3),('Hangul_EU',0xed1),('Hangul_Hanja',0xff34),('Hangul_Hieuh',0xebe),
    ('Hangul_I',0xed3),('Hangul_Ieung',0xeb7),('Hangul_J_Cieuc',0xeea),('Hangul_J_Dikeud',0xeda),
    ('Hangul_J_Hieuh',0xeee),('Hangul_J_Ieung',0xee8),('Hangul_J_Jieuj',0xee9),('Hangul_J_Khieuq',0xeeb),
    ('Hangul_J_Kiyeog',0xed4),('Hangul_J_KiyeogSios',0xed6),('Hangul_J_KkogjiDalrinIeung',0xef9),('Hangul_J_Mieum',0xee3),
    ('Hangul_J_Nieun',0xed7),('Hangul_J_NieunHieuh',0xed9),('Hangul_J_NieunJieuj',0xed8),('Hangul_J_PanSios',0xef8),
    ('Hangul_J_Phieuf',0xeed),('Hangul_J_Pieub',0xee4),('Hangul_J_PieubSios',0xee5),('Hangul_J_Rieul',0xedb),
    ('Hangul_J_RieulHieuh',0xee2),('Hangul_J_RieulKiyeog',0xedc),('Hangul_J_RieulMieum',0xedd),('Hangul_J_RieulPhieuf',0xee1),
    ('Hangul_J_RieulPieub',0xede),('Hangul_J_RieulSios',0xedf),('Hangul_J_RieulTieut',0xee0),('Hangul_J_Sios',0xee6),
    ('Hangul_J_SsangKiyeog',0xed5),('Hangul_J_SsangSios',0xee7),('Hangul_J_Tieut',0xeec),('Hangul_J_YeorinHieuh',0xefa),
    ('Hangul_Jamo',0xff35),('Hangul_Jeonja',0xff38),('Hangul_Jieuj',0xeb8),('Hangul_Khieuq',0xebb),
    ('Hangul_Kiyeog',0xea1),('Hangul_KiyeogSios',0xea3),('Hangul_KkogjiDalrinIeung',0xef3),('Hangul_Mieum',0xeb1),
    ('Hangul_MultipleCandidate',0xff3d),('Hangul_Nieun',0xea4),('Hangul_NieunHieuh',0xea6),('Hangul_NieunJieuj',0xea5),
    ('Hangul_O',0xec7),('Hangul_OE',0xeca),('Hangul_PanSios',0xef2),('Hangul_Phieuf',0xebd),
    ('Hangul_Pieub',0xeb2),('Hangul_PieubSios',0xeb4),('Hangul_PostHanja',0xff3b),('Hangul_PreHanja',0xff3a),
    ('Hangul_PreviousCandidate',0xff3e),('Hangul_Rieul',0xea9),('Hangul_RieulHieuh',0xeb0),('Hangul_RieulKiyeog',0xeaa),
    ('Hangul_RieulMieum',0xeab),('Hangul_RieulPhieuf',0xeaf),('Hangul_RieulPieub',0xeac),('Hangul_RieulSios',0xead),
    ('Hangul_RieulTieut',0xeae),('Hangul_RieulYeorinHieuh',0xeef),('Hangul_Romaja',0xff36),('Hangul_SingleCandidate',0xff3c),
    ('Hangul_Sios',0xeb5),('Hangul_Special',0xff3f),('Hangul_SsangDikeud',0xea8),('Hangul_SsangJieuj',0xeb9),
    ('Hangul_SsangKiyeog',0xea2),('Hangul_SsangPieub',0xeb3),('Hangul_SsangSios',0xeb6),('Hangul_Start',0xff32),
    ('Hangul_SunkyeongeumMieum',0xef0),('Hangul_SunkyeongeumPhieuf',0xef4),('Hangul_SunkyeongeumPieub',0xef1),('Hangul_switch',0xff7e),
    ('Hangul_Tieut',0xebc),('Hangul_U',0xecc),('Hangul_WA',0xec8),('Hangul_WAE',0xec9),
    ('Hangul_WE',0xece),('Hangul_WEO',0xecd),('Hangul_WI',0xecf),('Hangul_YA',0xec1),
    ('Hangul_YAE',0xec2),('Hangul_YE',0xec6),('Hangul_YEO',0xec5),('Hangul_YeorinHieuh',0xef5),
    ('Hangul_YI',0xed2),('Hangul_YO',0xecb),('Hangul_YU',0xed0),('Hankaku',0xff29),
    ('Hcircumflex',0x2a6),('hcircumflex',0x2b6),('heart',0xaee),('hebrew_aleph',0xce0),
    ('hebrew_ayin',0xcf2),('hebrew_bet',0xce1),('hebrew_beth',0xce1),('hebrew_chet',0xce7),
    ('hebrew_dalet',0xce3),('hebrew_daleth',0xce3),('hebrew_doublelowline',0xcdf),('hebrew_finalkaph',0xcea),
    ('hebrew_finalmem',0xced),('hebrew_finalnun',0xcef),('hebrew_finalpe',0xcf3),('hebrew_finalzade',0xcf5),
    ('hebrew_finalzadi',0xcf5),('hebrew_gimel',0xce2),('hebrew_gimmel',0xce2),('hebrew_he',0xce4),
    ('hebrew_het',0xce7),('hebrew_kaph',0xceb),('hebrew_kuf',0xcf7),('hebrew_lamed',0xcec),
    ('hebrew_mem',0xcee),('hebrew_nun',0xcf0),('hebrew_pe',0xcf4),('hebrew_qoph',0xcf7),
    ('hebrew_resh',0xcf8),('hebrew_samech',0xcf1),('hebrew_samekh',0xcf1),('hebrew_shin',0xcf9),
    ('Hebrew_switch',0xff7e),('hebrew_taf',0xcfa),('hebrew_taw',0xcfa),('hebrew_tet',0xce8),
    ('hebrew_teth',0xce8),('hebrew_waw',0xce5),('hebrew_yod',0xce9),('hebrew_zade',0xcf6),
    ('hebrew_zadi',0xcf6),('hebrew_zain',0xce6),('hebrew_zayin',0xce6),('Help',0xff6a),
    ('Henkan',0xff23),('Henkan_Mode',0xff23),('hexagram',0xada),('Hiragana',0xff25),
    ('Hiragana_Katakana',0xff27),('Home',0xff50),('horizconnector',0x8a3),('horizlinescan1',0x9ef),
    ('horizlinescan3',0x9f0),('horizlinescan5',0x9f1),('horizlinescan7',0x9f2),('horizlinescan9',0x9f3),
    ('hpBackTab',0x1000ff74),('hpblock',0x100000fc),('hpClearLine',0x1000ff6f),('hpDeleteChar',0x1000ff73),
    ('hpDeleteLine',0x1000ff71),('hpguilder',0x100000be),('hpInsertChar',0x1000ff72),('hpInsertLine',0x1000ff70),
    ('hpIO',0x100000ee),('hpKP_BackTab',0x1000ff75),('hplira',0x100000af),('hplongminus',0x100000f6),
    ('hpModelock1',0x1000ff48),('hpModelock2',0x1000ff49),('hpmute_acute',0x100000a8),('hpmute_asciicircum',0x100000aa),
    ('hpmute_asciitilde',0x100000ac),('hpmute_diaeresis',0x100000ab),('hpmute_grave',0x100000a9),('hpReset',0x1000ff6c),
    ('hpSystem',0x1000ff6d),('hpUser',0x1000ff6e),('hpYdiaeresis',0x100000ee),('Hstroke',0x2a1),
    ('hstroke',0x2b1),('ht',0x9e2),('Hyper_L',0xffed),('Hyper_R',0xffee),
    ('hyphen',0xad),('I',0x49),('i',0x69),('Iabovedot',0x2a9),
    ('Iacute',0xcd),('iacute',0xed),('Ibelowdot',0x1001eca),('ibelowdot',0x1001ecb),
    ('Ibreve',0x100012c),('ibreve',0x100012d),('Icircumflex',0xce),('icircumflex',0xee),
    ('identical',0x8cf),('Idiaeresis',0xcf),('idiaeresis',0xef),('idotless',0x2b9),
    ('ifonlyif',0x8cd),('Igrave',0xcc),('igrave',0xec),('Ihook',0x1001ec8),
    ('ihook',0x1001ec9),('Imacron',0x3cf),('imacron',0x3ef),('implies',0x8ce),
    ('includedin',0x8da),('includes',0x8db),('infinity',0x8c2),('Insert',0xff63),
    ('InsertChar',0x1000ff72),('InsertLine',0x1000ff70),('integral',0x8bf),('intersection',0x8dc),
    ('IO',0x100000ee),('Iogonek',0x3c7),('iogonek',0x3e7),('ISO_Center_Object',0xfe33),
    ('ISO_Continuous_Underline',0xfe30),('ISO_Discontinuous_Underline',0xfe31),('ISO_Emphasize',0xfe32),('ISO_Enter',0xfe34),
    ('ISO_Fast_Cursor_Down',0xfe2f),('ISO_Fast_Cursor_Left',0xfe2c),('ISO_Fast_Cursor_Right',0xfe2d),('ISO_Fast_Cursor_Up',0xfe2e),
    ('ISO_First_Group',0xfe0c),('ISO_First_Group_Lock',0xfe0d),('ISO_Group_Latch',0xfe06),('ISO_Group_Lock',0xfe07),
    ('ISO_Group_Shift',0xff7e),('ISO_Last_Group',0xfe0e),('ISO_Last_Group_Lock',0xfe0f),('ISO_Left_Tab',0xfe20),
    ('ISO_Level2_Latch',0xfe02),('ISO_Level3_Latch',0xfe04),('ISO_Level3_Lock',0xfe05),('ISO_Level3_Shift',0xfe03),
    ('ISO_Level5_Latch',0xfe12),('ISO_Level5_Lock',0xfe13),('ISO_Level5_Shift',0xfe11),('ISO_Lock',0xfe01),
    ('ISO_Move_Line_Down',0xfe22),('ISO_Move_Line_Up',0xfe21),('ISO_Next_Group',0xfe08),('ISO_Next_Group_Lock',0xfe09),
    ('ISO_Partial_Line_Down',0xfe24),('ISO_Partial_Line_Up',0xfe23),('ISO_Partial_Space_Left',0xfe25),('ISO_Partial_Space_Right',0xfe26),
    ('ISO_Prev_Group',0xfe0a),('ISO_Prev_Group_Lock',0xfe0b),('ISO_Release_Both_Margins',0xfe2b),('ISO_Release_Margin_Left',0xfe29),
    ('ISO_Release_Margin_Right',0xfe2a),('ISO_Set_Margin_Left',0xfe27),('ISO_Set_Margin_Right',0xfe28),('Itilde',0x3a5),
    ('itilde',0x3b5),('J',0x4a),('j',0x6a),('Jcircumflex',0x2ac),
    ('jcircumflex',0x2bc),('jot',0xbca),('K',0x4b),('k',0x6b),
    ('kana_A',0x4b1),('kana_a',0x4a7),('kana_CHI',0x4c1),('kana_closingbracket',0x4a3),
    ('kana_comma',0x4a4),('kana_conjunctive',0x4a5),('kana_E',0x4b4),('kana_e',0x4aa),
    ('kana_FU',0x4cc),('kana_fullstop',0x4a1),('kana_HA',0x4ca),('kana_HE',0x4cd),
    ('kana_HI',0x4cb),('kana_HO',0x4ce),('kana_HU',0x4cc),('kana_I',0x4b2),
    ('kana_i',0x4a8),('kana_KA',0x4b6),('kana_KE',0x4b9),('kana_KI',0x4b7),
    ('kana_KO',0x4ba),('kana_KU',0x4b8),('Kana_Lock',0xff2d),('kana_MA',0x4cf),
    ('kana_ME',0x4d2),('kana_MI',0x4d0),('kana_middledot',0x4a5),('kana_MO',0x4d3),
    ('kana_MU',0x4d1),('kana_N',0x4dd),('kana_NA',0x4c5),('kana_NE',0x4c8),
    ('kana_NI',0x4c6),('kana_NO',0x4c9),('kana_NU',0x4c7),('kana_O',0x4b5),
    ('kana_o',0x4ab),('kana_openingbracket',0x4a2),('kana_RA',0x4d7),('kana_RE',0x4da),
    ('kana_RI',0x4d8),('kana_RO',0x4db),('kana_RU',0x4d9),('kana_SA',0x4bb),
    ('kana_SE',0x4be),('kana_SHI',0x4bc),('Kana_Shift',0xff2e),('kana_SO',0x4bf),
    ('kana_SU',0x4bd),('kana_switch',0xff7e),('kana_TA',0x4c0),('kana_TE',0x4c3),
    ('kana_TI',0x4c1),('kana_TO',0x4c4),('kana_TSU',0x4c2),('kana_tsu',0x4af),
    ('kana_TU',0x4c2),('kana_tu',0x4af),('kana_U',0x4b3),('kana_u',0x4a9),
    ('kana_WA',0x4dc),('kana_WO',0x4a6),('kana_YA',0x4d4),('kana_ya',0x4ac),
    ('kana_YO',0x4d6),('kana_yo',0x4ae),('kana_YU',0x4d5),('kana_yu',0x4ad),
    ('Kanji',0xff21),('Kanji_Bangou',0xff37),('kappa',0x3a2),('Katakana',0xff26),
    ('Kcedilla',0x3d3),('kcedilla',0x3f3),('Korean_Won',0xeff),('KP_0',0xffb0),
    ('KP_1',0xffb1),('KP_2',0xffb2),('KP_3',0xffb3),('KP_4',0xffb4),
    ('KP_5',0xffb5),('KP_6',0xffb6),('KP_7',0xffb7),('KP_8',0xffb8),
    ('KP_9',0xffb9),('KP_Add',0xffab),('KP_BackTab',0x1000ff75),('KP_Begin',0xff9d),
    ('KP_Decimal',0xffae),('KP_Delete',0xff9f),('KP_Divide',0xffaf),('KP_Down',0xff99),
    ('KP_End',0xff9c),('KP_Enter',0xff8d),('KP_Equal',0xffbd),('KP_F1',0xff91),
    ('KP_F2',0xff92),('KP_F3',0xff93),('KP_F4',0xff94),('KP_Home',0xff95),
    ('KP_Insert',0xff9e),('KP_Left',0xff96),('KP_Multiply',0xffaa),('KP_Next',0xff9b),
    ('KP_Page_Down',0xff9b),('KP_Page_Up',0xff9a),('KP_Prior',0xff9a),('KP_Right',0xff98),
    ('KP_Separator',0xffac),('KP_Space',0xff80),('KP_Subtract',0xffad),('KP_Tab',0xff89),
    ('KP_Up',0xff97),('kra',0x3a2),('L',0x4c),('l',0x6c),
    ('L1',0xffc8),('L10',0xffd1),('L2',0xffc9),('L3',0xffca),
    ('L4',0xffcb),('L5',0xffcc),('L6',0xffcd),('L7',0xffce),
    ('L8',0xffcf),('L9',0xffd0),('Lacute',0x1c5),('lacute',0x1e5),
    ('Last_Virtual_Screen',0xfed4),('latincross',0xad9),('Lbelowdot',0x1001e36),('lbelowdot',0x1001e37),
    ('Lcaron',0x1a5),('lcaron',0x1b5),('Lcedilla',0x3a6),('lcedilla',0x3b6),
    ('Left',0xff51),('leftanglebracket',0xabc),('leftarrow',0x8fb),('leftcaret',0xba3),
    ('leftdoublequotemark',0xad2),('leftmiddlecurlybrace',0x8af),('leftopentriangle',0xacc),('leftpointer',0xaea),
    ('leftradical',0x8a1),('leftshoe',0xbda),('leftsingleanglequotemark',0x1002039),('leftsinglequotemark',0xad0),
    ('leftt',0x9f4),('lefttack',0xbdc),('less',0x3c),('lessthanequal',0x8bc),
    ('lf',0x9e5),('Linefeed',0xff0a),('lira',0x100000af),('LiraSign',0x10020a4),
    ('logicaland',0x8de),('logicalor',0x8df),('longminus',0x100000f6),('lowleftcorner',0x9ed),
    ('lowrightcorner',0x9ea),('Lstroke',0x1a3),('lstroke',0x1b3),('M',0x4d),
    ('m',0x6d),('Mabovedot',0x1001e40),('mabovedot',0x1001e41),('Macedonia_DSE',0x6b5),
    ('Macedonia_dse',0x6a5),('Macedonia_GJE',0x6b2),('Macedonia_gje',0x6a2),('Macedonia_KJE',0x6bc),
    ('Macedonia_kje',0x6ac),('macron',0xaf),('Mae_Koho',0xff3e),('malesymbol',0xaf7),
    ('maltesecross',0xaf0),('marker',0xabf),('masculine',0xba),('Massyo',0xff2c),
    ('Menu',0xff67),('Meta_L',0xffe7),('Meta_R',0xffe8),('MillSign',0x10020a5),
    ('minus',0x2d),('minutes',0xad6),('Mode_switch',0xff7e),('MouseKeys_Accel_Enable',0xfe77),
    ('MouseKeys_Enable',0xfe76),('mu',0xb5),('Muhenkan',0xff22),('Multi_key',0xff20),
    ('MultipleCandidate',0xff3d),('multiply',0xd7),('musicalflat',0xaf6),('musicalsharp',0xaf5),
    ('mute_acute',0x100000a8),('mute_asciicircum',0x100000aa),('mute_asciitilde',0x100000ac),('mute_diaeresis',0x100000ab),
    ('mute_grave',0x100000a9),('N',0x4e),('n',0x6e),('nabla',0x8c5),
    ('Nacute',0x1d1),('nacute',0x1f1),('NairaSign',0x10020a6),('Ncaron',0x1d2),
    ('ncaron',0x1f2),('Ncedilla',0x3d1),('ncedilla',0x3f1),('NewSheqelSign',0x10020aa),
    ('Next',0xff56),('Next_Virtual_Screen',0xfed2),('ninesubscript',0x1002089),('ninesuperior',0x1002079),
    ('nl',0x9e8),('nobreakspace',0xa0),('NoSymbol',0x0),('notapproxeq',0x1002247),
    ('notelementof',0x1002209),('notequal',0x8bd),('notidentical',0x1002262),('notsign',0xac),
    ('Ntilde',0xd1),('ntilde',0xf1),('Num_Lock',0xff7f),('numbersign',0x23),
    ('numerosign',0x6b0),('O',0x4f),('o',0x6f),('Oacute',0xd3),
    ('oacute',0xf3),('Obarred',0x100019f),('obarred',0x1000275),('Obelowdot',0x1001ecc),
    ('obelowdot',0x1001ecd),('Ocaron',0x10001d1),('ocaron',0x10001d2),('Ocircumflex',0xd4),
    ('ocircumflex',0xf4),('Ocircumflexacute',0x1001ed0),('ocircumflexacute',0x1001ed1),('Ocircumflexbelowdot',0x1001ed8),
    ('ocircumflexbelowdot',0x1001ed9),('Ocircumflexgrave',0x1001ed2),('ocircumflexgrave',0x1001ed3),('Ocircumflexhook',0x1001ed4),
    ('ocircumflexhook',0x1001ed5),('Ocircumflextilde',0x1001ed6),('ocircumflextilde',0x1001ed7),('Odiaeresis',0xd6),
    ('odiaeresis',0xf6),('Odoubleacute',0x1d5),('odoubleacute',0x1f5),('OE',0x13bc),
    ('oe',0x13bd),('ogonek',0x1b2),('Ograve',0xd2),('ograve',0xf2),
    ('Ohook',0x1001ece),('ohook',0x1001ecf),('Ohorn',0x10001a0),('ohorn',0x10001a1),
    ('Ohornacute',0x1001eda),('ohornacute',0x1001edb),('Ohornbelowdot',0x1001ee2),('ohornbelowdot',0x1001ee3),
    ('Ohorngrave',0x1001edc),('ohorngrave',0x1001edd),('Ohornhook',0x1001ede),('ohornhook',0x1001edf),
    ('Ohorntilde',0x1001ee0),('ohorntilde',0x1001ee1),('Omacron',0x3d2),('omacron',0x3f2),
    ('oneeighth',0xac3),('onefifth',0xab2),('onehalf',0xbd),('onequarter',0xbc),
    ('onesixth',0xab6),('onesubscript',0x1002081),('onesuperior',0xb9),('onethird',0xab0),
    ('Ooblique',0xd8),('ooblique',0xf8),('openrectbullet',0xae2),('openstar',0xae5),
    ('opentribulletdown',0xae4),('opentribulletup',0xae3),('ordfeminine',0xaa),('ordmasculine',0xba),
    ('osfActivate',0x1004ff44),('osfAddMode',0x1004ff31),('osfBackSpace',0x1004ff08),('osfBackTab',0x1004ff07),
    ('osfBeginData',0x1004ff5a),('osfBeginLine',0x1004ff58),('osfCancel',0x1004ff69),('osfClear',0x1004ff0b),
    ('osfCopy',0x1004ff02),('osfCut',0x1004ff03),('osfDelete',0x1004ffff),('osfDeselectAll',0x1004ff72),
    ('osfDown',0x1004ff54),('osfEndData',0x1004ff59),('osfEndLine',0x1004ff57),('osfEscape',0x1004ff1b),
    ('osfExtend',0x1004ff74),('osfHelp',0x1004ff6a),('osfInsert',0x1004ff63),('osfLeft',0x1004ff51),
    ('osfMenu',0x1004ff67),('osfMenuBar',0x1004ff45),('osfNextField',0x1004ff5e),('osfNextMenu',0x1004ff5c),
    ('osfPageDown',0x1004ff42),('osfPageLeft',0x1004ff40),('osfPageRight',0x1004ff43),('osfPageUp',0x1004ff41),
    ('osfPaste',0x1004ff04),('osfPrevField',0x1004ff5d),('osfPrevMenu',0x1004ff5b),('osfPrimaryPaste',0x1004ff32),
    ('osfQuickPaste',0x1004ff33),('osfReselect',0x1004ff73),('osfRestore',0x1004ff78),('osfRight',0x1004ff53),
    ('osfSelect',0x1004ff60),('osfSelectAll',0x1004ff71),('osfUndo',0x1004ff65),('osfUp',0x1004ff52),
    ('Oslash',0xd8),('oslash',0xf8),('Otilde',0xd5),('otilde',0xf5),
    ('overbar',0xbc0),('Overlay1_Enable',0xfe78),('Overlay2_Enable',0xfe79),('overline',0x47e),
    ('P',0x50),('p',0x70),('Pabovedot',0x1001e56),('pabovedot',0x1001e57),
    ('Page_Down',0xff56),('Page_Up',0xff55),('paragraph',0xb6),('parenleft',0x28),
    ('parenright',0x29),('partdifferential',0x1002202),('partialderivative',0x8ef),('Pause',0xff13),
    ('percent',0x25),('period',0x2e),('periodcentered',0xb7),('permille',0xad5),
    ('PesetaSign',0x10020a7),('phonographcopyright',0xafb),('plus',0x2b),('plusminus',0xb1),
    ('Pointer_Accelerate',0xfefa),('Pointer_Button1',0xfee9),('Pointer_Button2',0xfeea),('Pointer_Button3',0xfeeb),
    ('Pointer_Button4',0xfeec),('Pointer_Button5',0xfeed),('Pointer_Button_Dflt',0xfee8),('Pointer_DblClick1',0xfeef),
    ('Pointer_DblClick2',0xfef0),('Pointer_DblClick3',0xfef1),('Pointer_DblClick4',0xfef2),('Pointer_DblClick5',0xfef3),
    ('Pointer_DblClick_Dflt',0xfeee),('Pointer_DfltBtnNext',0xfefb),('Pointer_DfltBtnPrev',0xfefc),('Pointer_Down',0xfee3),
    ('Pointer_DownLeft',0xfee6),('Pointer_DownRight',0xfee7),('Pointer_Drag1',0xfef5),('Pointer_Drag2',0xfef6),
    ('Pointer_Drag3',0xfef7),('Pointer_Drag4',0xfef8),('Pointer_Drag5',0xfefd),('Pointer_Drag_Dflt',0xfef4),
    ('Pointer_EnableKeys',0xfef9),('Pointer_Left',0xfee0),('Pointer_Right',0xfee1),('Pointer_Up',0xfee2),
    ('Pointer_UpLeft',0xfee4),('Pointer_UpRight',0xfee5),('prescription',0xad4),('Prev_Virtual_Screen',0xfed1),
    ('PreviousCandidate',0xff3e),('Print',0xff61),('Prior',0xff55),('prolongedsound',0x4b0),
    ('punctspace',0xaa6),('Q',0x51),('q',0x71),('quad',0xbcc),
    ('question',0x3f),('questiondown',0xbf),('quotedbl',0x22),('quoteleft',0x60),
    ('quoteright',0x27),('R',0x52),('r',0x72),('R1',0xffd2),
    ('R10',0xffdb),('R11',0xffdc),('R12',0xffdd),('R13',0xffde),
    ('R14',0xffdf),('R15',0xffe0),('R2',0xffd3),('R3',0xffd4),
    ('R4',0xffd5),('R5',0xffd6),('R6',0xffd7),('R7',0xffd8),
    ('R8',0xffd9),('R9',0xffda),('Racute',0x1c0),('racute',0x1e0),
    ('radical',0x8d6),('Rcaron',0x1d8),('rcaron',0x1f8),('Rcedilla',0x3a3),
    ('rcedilla',0x3b3),('Redo',0xff66),('registered',0xae),('RepeatKeys_Enable',0xfe72),
    ('Reset',0x1000ff6c),('Return',0xff0d),('Right',0xff53),('rightanglebracket',0xabe),
    ('rightarrow',0x8fd),('rightcaret',0xba6),('rightdoublequotemark',0xad3),('rightmiddlecurlybrace',0x8b0),
    ('rightmiddlesummation',0x8b7),('rightopentriangle',0xacd),('rightpointer',0xaeb),('rightshoe',0xbd8),
    ('rightsingleanglequotemark',0x100203a),('rightsinglequotemark',0xad1),('rightt',0x9f5),('righttack',0xbfc),
    ('Romaji',0xff24),('RupeeSign',0x10020a8),('S',0x53),('s',0x73),
    ('Sabovedot',0x1001e60),('sabovedot',0x1001e61),('Sacute',0x1a6),('sacute',0x1b6),
    ('Scaron',0x1a9),('scaron',0x1b9),('Scedilla',0x1aa),('scedilla',0x1ba),
    ('SCHWA',0x100018f),('schwa',0x1000259),('Scircumflex',0x2de),('scircumflex',0x2fe),
    ('script_switch',0xff7e),('Scroll_Lock',0xff14),('seconds',0xad7),('section',0xa7),
    ('Select',0xff60),('semicolon',0x3b),('semivoicedsound',0x4df),('Serbian_DJE',0x6b1),
    ('Serbian_dje',0x6a1),('Serbian_DZE',0x6bf),('Serbian_dze',0x6af),('Serbian_JE',0x6b8),
    ('Serbian_je',0x6a8),('Serbian_LJE',0x6b9),('Serbian_lje',0x6a9),('Serbian_NJE',0x6ba),
    ('Serbian_nje',0x6aa),('Serbian_TSHE',0x6bb),('Serbian_tshe',0x6ab),('seveneighths',0xac6),
    ('sevensubscript',0x1002087),('sevensuperior',0x1002077),('Shift_L',0xffe1),('Shift_Lock',0xffe6),
    ('Shift_R',0xffe2),('signaturemark',0xaca),('signifblank',0xaac),('similarequal',0x8c9),
    ('SingleCandidate',0xff3c),('singlelowquotemark',0xafd),('Sinh_a',0x1000d85),('Sinh_aa',0x1000d86),
    ('Sinh_aa2',0x1000dcf),('Sinh_ae',0x1000d87),('Sinh_ae2',0x1000dd0),('Sinh_aee',0x1000d88),
    ('Sinh_aee2',0x1000dd1),('Sinh_ai',0x1000d93),('Sinh_ai2',0x1000ddb),('Sinh_al',0x1000dca),
    ('Sinh_au',0x1000d96),('Sinh_au2',0x1000dde),('Sinh_ba',0x1000db6),('Sinh_bha',0x1000db7),
    ('Sinh_ca',0x1000da0),('Sinh_cha',0x1000da1),('Sinh_dda',0x1000da9),('Sinh_ddha',0x1000daa),
    ('Sinh_dha',0x1000daf),('Sinh_dhha',0x1000db0),('Sinh_e',0x1000d91),('Sinh_e2',0x1000dd9),
    ('Sinh_ee',0x1000d92),('Sinh_ee2',0x1000dda),('Sinh_fa',0x1000dc6),('Sinh_ga',0x1000d9c),
    ('Sinh_gha',0x1000d9d),('Sinh_h2',0x1000d83),('Sinh_ha',0x1000dc4),('Sinh_i',0x1000d89),
    ('Sinh_i2',0x1000dd2),('Sinh_ii',0x1000d8a),('Sinh_ii2',0x1000dd3),('Sinh_ja',0x1000da2),
    ('Sinh_jha',0x1000da3),('Sinh_jnya',0x1000da5),('Sinh_ka',0x1000d9a),('Sinh_kha',0x1000d9b),
    ('Sinh_kunddaliya',0x1000df4),('Sinh_la',0x1000dbd),('Sinh_lla',0x1000dc5),('Sinh_lu',0x1000d8f),
    ('Sinh_lu2',0x1000ddf),('Sinh_luu',0x1000d90),('Sinh_luu2',0x1000df3),('Sinh_ma',0x1000db8),
    ('Sinh_mba',0x1000db9),('Sinh_na',0x1000db1),('Sinh_ndda',0x1000dac),('Sinh_ndha',0x1000db3),
    ('Sinh_ng',0x1000d82),('Sinh_ng2',0x1000d9e),('Sinh_nga',0x1000d9f),('Sinh_nja',0x1000da6),
    ('Sinh_nna',0x1000dab),('Sinh_nya',0x1000da4),('Sinh_o',0x1000d94),('Sinh_o2',0x1000ddc),
    ('Sinh_oo',0x1000d95),('Sinh_oo2',0x1000ddd),('Sinh_pa',0x1000db4),('Sinh_pha',0x1000db5),
    ('Sinh_ra',0x1000dbb),('Sinh_ri',0x1000d8d),('Sinh_rii',0x1000d8e),('Sinh_ru2',0x1000dd8),
    ('Sinh_ruu2',0x1000df2),('Sinh_sa',0x1000dc3),('Sinh_sha',0x1000dc1),('Sinh_ssha',0x1000dc2),
    ('Sinh_tha',0x1000dad),('Sinh_thha',0x1000dae),('Sinh_tta',0x1000da7),('Sinh_ttha',0x1000da8),
    ('Sinh_u',0x1000d8b),('Sinh_u2',0x1000dd4),('Sinh_uu',0x1000d8c),('Sinh_uu2',0x1000dd6),
    ('Sinh_va',0x1000dc0),('Sinh_ya',0x1000dba),('sixsubscript',0x1002086),('sixsuperior',0x1002076),
    ('slash',0x2f),('SlowKeys_Enable',0xfe73),('soliddiamond',0x9e0),('space',0x20),
    ('squareroot',0x100221a),('SSHARP',0x1001e9e),('ssharp',0xdf),('sterling',0xa3),
    ('StickyKeys_Enable',0xfe75),('stricteq',0x1002263),('SunAgain',0xff66),('SunAltGraph',0xff7e),
    ('SunAudioLowerVolume',0x1005ff77),('SunAudioMute',0x1005ff78),('SunAudioRaiseVolume',0x1005ff79),('SunCompose',0xff20),
    ('SunCopy',0x1005ff72),('SunCut',0x1005ff75),('SunF36',0x1005ff10),('SunF37',0x1005ff11),
    ('SunFA_Acute',0x1005ff03),('SunFA_Cedilla',0x1005ff05),('SunFA_Circum',0x1005ff01),('SunFA_Diaeresis',0x1005ff04),
    ('SunFA_Grave',0x1005ff00),('SunFA_Tilde',0x1005ff02),('SunFind',0xff68),('SunFront',0x1005ff71),
    ('SunOpen',0x1005ff73),('SunPageDown',0xff56),('SunPageUp',0xff55),('SunPaste',0x1005ff74),
    ('SunPowerSwitch',0x1005ff76),('SunPowerSwitchShift',0x1005ff7d),('SunPrint_Screen',0xff61),('SunProps',0x1005ff70),
    ('SunStop',0xff69),('SunSys_Req',0x1005ff60),('SunUndo',0xff65),('SunVideoDegauss',0x1005ff7a),
    ('SunVideoLowerBrightness',0x1005ff7b),('SunVideoRaiseBrightness',0x1005ff7c),('Super_L',0xffeb),('Super_R',0xffec),
    ('Sys_Req',0xff15),('System',0x1000ff6d),('T',0x54),('t',0x74),
    ('Tab',0xff09),('Tabovedot',0x1001e6a),('tabovedot',0x1001e6b),('Tcaron',0x1ab),
    ('tcaron',0x1bb),('Tcedilla',0x1de),('tcedilla',0x1fe),('telephone',0xaf9),
    ('telephonerecorder',0xafa),('Terminate_Server',0xfed5),('Thai_baht',0xddf),('Thai_bobaimai',0xdba),
    ('Thai_chochan',0xda8),('Thai_chochang',0xdaa),('Thai_choching',0xda9),('Thai_chochoe',0xdac),
    ('Thai_dochada',0xdae),('Thai_dodek',0xdb4),('Thai_fofa',0xdbd),('Thai_fofan',0xdbf),
    ('Thai_hohip',0xdcb),('Thai_honokhuk',0xdce),('Thai_khokhai',0xda2),('Thai_khokhon',0xda5),
    ('Thai_khokhuat',0xda3),('Thai_khokhwai',0xda4),('Thai_khorakhang',0xda6),('Thai_kokai',0xda1),
    ('Thai_lakkhangyao',0xde5),('Thai_lekchet',0xdf7),('Thai_lekha',0xdf5),('Thai_lekhok',0xdf6),
    ('Thai_lekkao',0xdf9),('Thai_leknung',0xdf1),('Thai_lekpaet',0xdf8),('Thai_leksam',0xdf3),
    ('Thai_leksi',0xdf4),('Thai_leksong',0xdf2),('Thai_leksun',0xdf0),('Thai_lochula',0xdcc),
    ('Thai_loling',0xdc5),('Thai_lu',0xdc6),('Thai_maichattawa',0xdeb),('Thai_maiek',0xde8),
    ('Thai_maihanakat',0xdd1),('Thai_maihanakat_maitho',0xdde),('Thai_maitaikhu',0xde7),('Thai_maitho',0xde9),
    ('Thai_maitri',0xdea),('Thai_maiyamok',0xde6),('Thai_moma',0xdc1),('Thai_ngongu',0xda7),
    ('Thai_nikhahit',0xded),('Thai_nonen',0xdb3),('Thai_nonu',0xdb9),('Thai_oang',0xdcd),
    ('Thai_paiyannoi',0xdcf),('Thai_phinthu',0xdda),('Thai_phophan',0xdbe),('Thai_phophung',0xdbc),
    ('Thai_phosamphao',0xdc0),('Thai_popla',0xdbb),('Thai_rorua',0xdc3),('Thai_ru',0xdc4),
    ('Thai_saraa',0xdd0),('Thai_saraaa',0xdd2),('Thai_saraae',0xde1),('Thai_saraaimaimalai',0xde4),
    ('Thai_saraaimaimuan',0xde3),('Thai_saraam',0xdd3),('Thai_sarae',0xde0),('Thai_sarai',0xdd4),
    ('Thai_saraii',0xdd5),('Thai_sarao',0xde2),('Thai_sarau',0xdd8),('Thai_saraue',0xdd6),
    ('Thai_sarauee',0xdd7),('Thai_sarauu',0xdd9),('Thai_sorusi',0xdc9),('Thai_sosala',0xdc8),
    ('Thai_soso',0xdab),('Thai_sosua',0xdca),('Thai_thanthakhat',0xdec),('Thai_thonangmontho',0xdb1),
    ('Thai_thophuthao',0xdb2),('Thai_thothahan',0xdb7),('Thai_thothan',0xdb0),('Thai_thothong',0xdb8),
    ('Thai_thothung',0xdb6),('Thai_topatak',0xdaf),('Thai_totao',0xdb5),('Thai_wowaen',0xdc7),
    ('Thai_yoyak',0xdc2),('Thai_yoying',0xdad),('therefore',0x8c0),('thinspace',0xaa7),
    ('THORN',0xde),('Thorn',0xde),('thorn',0xfe),('threeeighths',0xac4),
    ('threefifths',0xab4),('threequarters',0xbe),('threesubscript',0x1002083),('threesuperior',0xb3),
    ('tintegral',0x100222d),('topintegral',0x8a4),('topleftparens',0x8ab),('topleftradical',0x8a2),
    ('topleftsqbracket',0x8a7),('topleftsummation',0x8b1),('toprightparens',0x8ad),('toprightsqbracket',0x8a9),
    ('toprightsummation',0x8b5),('topt',0x9f7),('topvertsummationconnector',0x8b3),('Touroku',0xff2b),
    ('trademark',0xac9),('trademarkincircle',0xacb),('Tslash',0x3ac),('tslash',0x3bc),
    ('twofifths',0xab3),('twosubscript',0x1002082),('twosuperior',0xb2),('twothirds',0xab1),
    ('U',0x55),('u',0x75),('Uacute',0xda),('uacute',0xfa),
    ('Ubelowdot',0x1001ee4),('ubelowdot',0x1001ee5),('Ubreve',0x2dd),('ubreve',0x2fd),
    ('Ucircumflex',0xdb),('ucircumflex',0xfb),('Udiaeresis',0xdc),('udiaeresis',0xfc),
    ('Udoubleacute',0x1db),('udoubleacute',0x1fb),('Ugrave',0xd9),('ugrave',0xf9),
    ('Uhook',0x1001ee6),('uhook',0x1001ee7),('Uhorn',0x10001af),('uhorn',0x10001b0),
    ('Uhornacute',0x1001ee8),('uhornacute',0x1001ee9),('Uhornbelowdot',0x1001ef0),('uhornbelowdot',0x1001ef1),
    ('Uhorngrave',0x1001eea),('uhorngrave',0x1001eeb),('Uhornhook',0x1001eec),('uhornhook',0x1001eed),
    ('Uhorntilde',0x1001eee),('uhorntilde',0x1001eef),('Ukrainian_GHE_WITH_UPTURN',0x6bd),('Ukrainian_ghe_with_upturn',0x6ad),
    ('Ukrainian_I',0x6b6),('Ukrainian_i',0x6a6),('Ukrainian_IE',0x6b4),('Ukrainian_ie',0x6a4),
    ('Ukrainian_YI',0x6b7),('Ukrainian_yi',0x6a7),('Ukranian_I',0x6b6),('Ukranian_i',0x6a6),
    ('Ukranian_JE',0x6b4),('Ukranian_je',0x6a4),('Ukranian_YI',0x6b7),('Ukranian_yi',0x6a7),
    ('Umacron',0x3de),('umacron',0x3fe),('underbar',0xbc6),('underscore',0x5f),
    ('Undo',0xff65),('union',0x8dd),('Uogonek',0x3d9),('uogonek',0x3f9),
    ('Up',0xff52),('uparrow',0x8fc),('upcaret',0xba9),('upleftcorner',0x9ec),
    ('uprightcorner',0x9eb),('upshoe',0xbc3),('upstile',0xbd3),('uptack',0xbce),
    ('Uring',0x1d9),('uring',0x1f9),('User',0x1000ff6e),('Utilde',0x3dd),
    ('utilde',0x3fd),('V',0x56),('v',0x76),('variation',0x8c1),
    ('vertbar',0x9f8),('vertconnector',0x8a6),('voicedsound',0x4de),('VoidSymbol',0xffffff),
    ('vt',0x9e9),('W',0x57),('w',0x77),('Wacute',0x1001e82),
    ('wacute',0x1001e83),('Wcircumflex',0x1000174),('wcircumflex',0x1000175),('Wdiaeresis',0x1001e84),
    ('wdiaeresis',0x1001e85),('Wgrave',0x1001e80),('wgrave',0x1001e81),('WonSign',0x10020a9),
    ('X',0x58),('x',0x78),('Xabovedot',0x1001e8a),('xabovedot',0x1001e8b),
    ('XF8610ChannelsDown',0x100811b9),('XF8610ChannelsUp',0x100811b8),('XF863DMode',0x1008126f),('XF86Accessibility',0x1008124e),
    ('XF86ActionOnSelection',0x10081254),('XF86AddFavorite',0x1008ff39),('XF86Addressbook',0x100811ad),('XF86ALSToggle',0x10081230),
    ('XF86ApplicationLeft',0x1008ff50),('XF86ApplicationRight',0x1008ff51),('XF86AppSelect',0x10081244),('XF86AspectRatio',0x10081177),
    ('XF86Assistant',0x10081247),('XF86AttendantOff',0x1008121c),('XF86AttendantOn',0x1008121b),('XF86AttendantToggle',0x1008121d),
    ('XF86Audio',0x10081188),('XF86AudioBassBoost',0x100810d1),('XF86AudioChannelMode',0x10081175),('XF86AudioCycleTrack',0x1008ff9b),
    ('XF86AudioDesc',0x1008126e),('XF86AudioForward',0x1008ff97),('XF86AudioLowerVolume',0x1008ff11),('XF86AudioMedia',0x1008ff32),
    ('XF86AudioMicMute',0x1008ffb2),('XF86AudioMute',0x1008ff12),('XF86AudioNext',0x1008ff17),('XF86AudioPause',0x1008ff31),
    ('XF86AudioPlay',0x1008ff14),('XF86AudioPreset',0x1008ffb6),('XF86AudioPrev',0x1008ff16),('XF86AudioRaiseVolume',0x1008ff13),
    ('XF86AudioRandomPlay',0x1008ff99),('XF86AudioRecord',0x1008ff1c),('XF86AudioRepeat',0x1008ff98),('XF86AudioRewind',0x1008ff3e),
    ('XF86AudioStop',0x1008ff15),('XF86AutopilotEngageToggle',0x1008127d),('XF86Away',0x1008ff8d),('XF86Back',0x1008ff26),
    ('XF86BackForward',0x1008ff3f),('XF86Battery',0x1008ff93),('XF86Blue',0x1008ffa6),('XF86Bluetooth',0x1008ff94),
    ('XF86Book',0x1008ff52),('XF86Break',0x1008119b),('XF86BrightnessAdjust',0x1008ff3b),('XF86BrightnessAuto',0x100810f4),
    ('XF86BrightnessMax',0x10081251),('XF86BrightnessMin',0x10081250),('XF86Buttonconfig',0x10081240),('XF86Calculater',0x1008ff54),
    ('XF86Calculator',0x1008ff1d),('XF86Calendar',0x1008ff20),('XF86CameraAccessDisable',0x1008124c),('XF86CameraAccessEnable',0x1008124b),
    ('XF86CameraAccessToggle',0x1008124d),('XF86CameraDown',0x10081218),('XF86CameraFocus',0x10081210),('XF86CameraLeft',0x10081219),
    ('XF86CameraRight',0x1008121a),('XF86CameraUp',0x10081217),('XF86CameraZoomIn',0x10081215),('XF86CameraZoomOut',0x10081216),
    ('XF86CD',0x1008ff53),('XF86ChannelDown',0x10081193),('XF86ChannelUp',0x10081192),('XF86Clear',0x1008ff55),
    ('XF86ClearGrab',0x1008fe21),('XF86ClearvuSonar',0x10081286),('XF86Close',0x1008ff56),('XF86Community',0x1008ff3d),
    ('XF86ContextMenu',0x100811b6),('XF86ContextualInsert',0x10081255),('XF86ContextualQuery',0x10081256),('XF86ContrastAdjust',0x1008ff22),
    ('XF86ControlPanel',0x10081243),('XF86Copy',0x1008ff57),('XF86Cut',0x1008ff58),('XF86CycleAngle',0x1008ff9c),
    ('XF86Data',0x10081277),('XF86Database',0x100811aa),('XF86Dictate',0x1008124a),('XF86Display',0x1008ff59),
    ('XF86DisplayOff',0x100810f5),('XF86DisplayToggle',0x100811af),('XF86Documents',0x1008ff5b),('XF86DoNotDisturb',0x1008124f),
    ('XF86DOS',0x1008ff5a),('XF86DualRangeRadar',0x10081283),('XF86DVD',0x10081185),('XF86Editor',0x100811a6),
    ('XF86Eject',0x1008ff2c),('XF86ElectronicPrivacyScreenOff',0x10081253),('XF86ElectronicPrivacyScreenOn',0x10081252),('XF86EmojiPicker',0x10081249),
    ('XF86Excel',0x1008ff5c),('XF86Exit',0x100810ae),('XF86Explorer',0x1008ff5d),('XF86FastReverse',0x10081275),
    ('XF86Favorites',0x1008ff30),('XF86Finance',0x1008ff3c),('XF86FishingChart',0x10081281),('XF86Fn',0x100811d0),
    ('XF86Fn_1',0x100811de),('XF86Fn_2',0x100811df),('XF86Fn_B',0x100811e4),('XF86Fn_D',0x100811e0),
    ('XF86Fn_E',0x100811e1),('XF86Fn_Esc',0x100811d1),('XF86Fn_F',0x100811e2),('XF86Fn_F1',0x100811d2),
    ('XF86Fn_F10',0x100811db),('XF86Fn_F11',0x100811dc),('XF86Fn_F12',0x100811dd),('XF86Fn_F2',0x100811d3),
    ('XF86Fn_F3',0x100811d4),('XF86Fn_F4',0x100811d5),('XF86Fn_F5',0x100811d6),('XF86Fn_F6',0x100811d7),
    ('XF86Fn_F7',0x100811d8),('XF86Fn_F8',0x100811d9),('XF86Fn_F9',0x100811da),('XF86Fn_S',0x100811e3),
    ('XF86FnRightShift',0x100811e5),('XF86Forward',0x1008ff27),('XF86FrameBack',0x1008ff9d),('XF86FrameForward',0x1008ff9e),
    ('XF86FullScreen',0x1008ffb8),('XF86Game',0x1008ff5e),('XF86Go',0x1008ff5f),('XF86GoTo',0x10081162),
    ('XF86GraphicsEditor',0x100811a8),('XF86Green',0x1008ffa4),('XF86HangupPhone',0x100811be),('XF86Hibernate',0x1008ffa8),
    ('XF86History',0x1008ff37),('XF86HomePage',0x1008ff18),('XF86HotLinks',0x1008ff3a),('XF86Images',0x100811ba),
    ('XF86Info',0x10081166),('XF86iTouch',0x1008ff60),('XF86Journal',0x10081242),('XF86KbdBrightnessDown',0x1008ff06),
    ('XF86KbdBrightnessUp',0x1008ff05),('XF86KbdInputAssistAccept',0x10081264),('XF86KbdInputAssistCancel',0x10081265),('XF86KbdInputAssistNext',0x10081261),
    ('XF86KbdInputAssistNextgroup',0x10081263),('XF86KbdInputAssistPrev',0x10081260),('XF86KbdInputAssistPrevgroup',0x10081262),('XF86KbdLcdMenu1',0x100812b8),
    ('XF86KbdLcdMenu2',0x100812b9),('XF86KbdLcdMenu3',0x100812ba),('XF86KbdLcdMenu4',0x100812bb),('XF86KbdLcdMenu5',0x100812bc),
    ('XF86KbdLightOnOff',0x1008ff04),('XF86Keyboard',0x1008ffb3),('XF86Launch0',0x1008ff40),('XF86Launch1',0x1008ff41),
    ('XF86Launch2',0x1008ff42),('XF86Launch3',0x1008ff43),('XF86Launch4',0x1008ff44),('XF86Launch5',0x1008ff45),
    ('XF86Launch6',0x1008ff46),('XF86Launch7',0x1008ff47),('XF86Launch8',0x1008ff48),('XF86Launch9',0x1008ff49),
    ('XF86LaunchA',0x1008ff4a),('XF86LaunchB',0x1008ff4b),('XF86LaunchC',0x1008ff4c),('XF86LaunchD',0x1008ff4d),
    ('XF86LaunchE',0x1008ff4e),('XF86LaunchF',0x1008ff4f),('XF86LeftDown',0x10081269),('XF86LeftUp',0x10081268),
    ('XF86LightBulb',0x1008ff35),('XF86LightsToggle',0x1008121e),('XF86LinkPhone',0x100811bf),('XF86LogGrabInfo',0x1008fe25),
    ('XF86LogOff',0x1008ff61),('XF86LogWindowTree',0x1008fe24),('XF86Macro1',0x10081290),('XF86Macro10',0x10081299),
    ('XF86Macro11',0x1008129a),('XF86Macro12',0x1008129b),('XF86Macro13',0x1008129c),('XF86Macro14',0x1008129d),
    ('XF86Macro15',0x1008129e),('XF86Macro16',0x1008129f),('XF86Macro17',0x100812a0),('XF86Macro18',0x100812a1),
    ('XF86Macro19',0x100812a2),('XF86Macro2',0x10081291),('XF86Macro20',0x100812a3),('XF86Macro21',0x100812a4),
    ('XF86Macro22',0x100812a5),('XF86Macro23',0x100812a6),('XF86Macro24',0x100812a7),('XF86Macro25',0x100812a8),
    ('XF86Macro26',0x100812a9),('XF86Macro27',0x100812aa),('XF86Macro28',0x100812ab),('XF86Macro29',0x100812ac),
    ('XF86Macro3',0x10081292),('XF86Macro30',0x100812ad),('XF86Macro4',0x10081293),('XF86Macro5',0x10081294),
    ('XF86Macro6',0x10081295),('XF86Macro7',0x10081296),('XF86Macro8',0x10081297),('XF86Macro9',0x10081298),
    ('XF86MacroPreset1',0x100812b3),('XF86MacroPreset2',0x100812b4),('XF86MacroPreset3',0x100812b5),('XF86MacroPresetCycle',0x100812b2),
    ('XF86MacroRecordStart',0x100812b0),('XF86MacroRecordStop',0x100812b1),('XF86Mail',0x1008ff19),('XF86MailForward',0x1008ff90),
    ('XF86Market',0x1008ff62),('XF86MarkWaypoint',0x1008127e),('XF86MediaLanguageMenu',0x10081170),('XF86MediaPlayer',0x10081183),
    ('XF86MediaPlayPause',0x100810a4),('XF86MediaPlaySlow',0x10081199),('XF86MediaRepeat',0x100811b7),('XF86MediaSelectAuxiliary',0x10081186),
    ('XF86MediaSelectCable',0x1008117a),('XF86MediaSelectCD',0x1008ff53),('XF86MediaSelectDVD',0x10081185),('XF86MediaSelectHome',0x1008116e),
    ('XF86MediaSelectPC',0x10081178),('XF86MediaSelectProgramGuide',0x1008116a),('XF86MediaSelectRadio',0x10081181),('XF86MediaSelectSatellite',0x1008117d),
    ('XF86MediaSelectTape',0x10081180),('XF86MediaSelectTeletext',0x10081184),('XF86MediaSelectTuner',0x10081182),('XF86MediaSelectTV',0x10081179),
    ('XF86MediaSelectVCR',0x1008117b),('XF86MediaSelectVCRPlus',0x1008117c),('XF86MediaTitleMenu',0x10081171),('XF86MediaTopMenu',0x1008126b),
    ('XF86Meeting',0x1008ff63),('XF86Memo',0x1008ff1e),('XF86MenuKB',0x1008ff65),('XF86MenuPB',0x1008ff66),
    ('XF86Messenger',0x1008ff8e),('XF86ModeLock',0x1008ff01),('XF86MonBrightnessAuto',0x100810f4),('XF86MonBrightnessCycle',0x1008ff07),
    ('XF86MonBrightnessDown',0x1008ff03),('XF86MonBrightnessUp',0x1008ff02),('XF86Music',0x1008ff92),('XF86MyComputer',0x1008ff33),
    ('XF86MySites',0x1008ff67),('XF86NavChart',0x10081280),('XF86NavInfo',0x10081288),('XF86New',0x1008ff68),
    ('XF86News',0x1008ff69),('XF86Next_VMode',0x1008fe22),('XF86NextElement',0x1008127b),('XF86NextFavorite',0x10081270),
    ('XF86NotificationCenter',0x100811bc),('XF86NumberEntryMode',0x1008119d),('XF86Numeric0',0x10081200),('XF86Numeric1',0x10081201),
    ('XF86Numeric11',0x1008126c),('XF86Numeric12',0x1008126d),('XF86Numeric2',0x10081202),('XF86Numeric3',0x10081203),
    ('XF86Numeric4',0x10081204),('XF86Numeric5',0x10081205),('XF86Numeric6',0x10081206),('XF86Numeric7',0x10081207),
    ('XF86Numeric8',0x10081208),('XF86Numeric9',0x10081209),('XF86NumericA',0x1008120c),('XF86NumericB',0x1008120d),
    ('XF86NumericC',0x1008120e),('XF86NumericD',0x1008120f),('XF86NumericPound',0x1008120b),('XF86NumericStar',0x1008120a),
    ('XF86OfficeHome',0x1008ff6a),('XF86OK',0x10081160),('XF86OnScreenKeyboard',0x10081278),('XF86Open',0x1008ff6b),
    ('XF86OpenURL',0x1008ff38),('XF86Option',0x1008ff6c),('XF86Paste',0x1008ff6d),('XF86PauseRecord',0x10081272),
    ('XF86PerformanceMode',0x100812bd),('XF86Phone',0x1008ff6e),('XF86PickupPhone',0x100811bd),('XF86Pictures',0x1008ff91),
    ('XF86PowerDown',0x1008ff21),('XF86PowerOff',0x1008ff2a),('XF86Presentation',0x100811a9),('XF86Prev_VMode',0x1008fe23),
    ('XF86PreviousElement',0x1008127c),('XF86PrivacyScreenToggle',0x10081279),('XF86Q',0x1008ff70),('XF86RadarOverlay',0x10081284),
    ('XF86Red',0x1008ffa3),('XF86Refresh',0x1008ff29),('XF86RefreshRateToggle',0x10081232),('XF86Reload',0x1008ff73),
    ('XF86Reply',0x1008ff72),('XF86RFKill',0x1008ffb5),('XF86RightDown',0x10081267),('XF86RightUp',0x10081266),
    ('XF86RockerDown',0x1008ff24),('XF86RockerEnter',0x1008ff25),('XF86RockerUp',0x1008ff23),('XF86RootMenu',0x1008126a),
    ('XF86RotateWindows',0x1008ff74),('XF86RotationKB',0x1008ff76),('XF86RotationLockToggle',0x1008ffb7),('XF86RotationPB',0x1008ff75),
    ('XF86Save',0x1008ff77),('XF86ScreenSaver',0x1008ff2d),('XF86Screensaver',0x10081245),('XF86ScrollClick',0x1008ff7a),
    ('XF86ScrollDown',0x1008ff79),('XF86ScrollUp',0x1008ff78),('XF86Search',0x1008ff1b),('XF86Select',0x1008ffa0),
    ('XF86SelectiveScreenshot',0x1008127a),('XF86Send',0x1008ff7b),('XF86Shop',0x1008ff36),('XF86SidevuSonar',0x10081287),
    ('XF86SingleRangeRadar',0x10081282),('XF86Sleep',0x1008ff2f),('XF86SlowReverse',0x10081276),('XF86Sos',0x1008127f),
    ('XF86Spell',0x1008ff7c),('XF86SpellCheck',0x100811b0),('XF86SplitScreen',0x1008ff7d),('XF86Sport',0x100810dc),
    ('XF86Standby',0x1008ff10),('XF86Start',0x1008ff1a),('XF86Stop',0x1008ff28),('XF86StopRecord',0x10081271),
    ('XF86Subtitle',0x1008ff9a),('XF86Support',0x1008ff7e),('XF86Suspend',0x1008ffa7),('XF86Switch_VT_1',0x1008fe01),
    ('XF86Switch_VT_10',0x1008fe0a),('XF86Switch_VT_11',0x1008fe0b),('XF86Switch_VT_12',0x1008fe0c),('XF86Switch_VT_2',0x1008fe02),
    ('XF86Switch_VT_3',0x1008fe03),('XF86Switch_VT_4',0x1008fe04),('XF86Switch_VT_5',0x1008fe05),('XF86Switch_VT_6',0x1008fe06),
    ('XF86Switch_VT_7',0x1008fe07),('XF86Switch_VT_8',0x1008fe08),('XF86Switch_VT_9',0x1008fe09),('XF86Taskmanager',0x10081241),
    ('XF86TaskPane',0x1008ff7f),('XF86Terminal',0x1008ff80),('XF86Time',0x1008ff9f),('XF86ToDoList',0x1008ff1f),
    ('XF86Tools',0x1008ff81),('XF86TopMenu',0x1008ffa2),('XF86TouchpadOff',0x1008ffb1),('XF86TouchpadOn',0x1008ffb0),
    ('XF86TouchpadToggle',0x1008ffa9),('XF86TraditionalSonar',0x10081285),('XF86Travel',0x1008ff82),('XF86Ungrab',0x1008fe20),
    ('XF86Unmute',0x10081274),('XF86User1KB',0x1008ff85),('XF86User2KB',0x1008ff86),('XF86UserPB',0x1008ff84),
    ('XF86UWB',0x1008ff96),('XF86VendorHome',0x1008ff34),('XF86VendorLogo',0x10081168),('XF86Video',0x1008ff87),
    ('XF86VideoPhone',0x100811a0),('XF86View',0x1008ffa1),('XF86VOD',0x10081273),('XF86VoiceCommand',0x10081246),
    ('XF86Voicemail',0x100811ac),('XF86WakeUp',0x1008ff2b),('XF86WebCam',0x1008ff8f),('XF86WheelButton',0x1008ff88),
    ('XF86WLAN',0x1008ff95),('XF86Word',0x1008ff89),('XF86WPSButton',0x10081211),('XF86WWAN',0x1008ffb4),
    ('XF86WWW',0x1008ff2e),('XF86Xfer',0x1008ff8a),('XF86Yellow',0x1008ffa5),('XF86ZoomIn',0x1008ff8b),
    ('XF86ZoomOut',0x1008ff8c),('XF86ZoomReset',0x100811a4),('Y',0x59),('y',0x79),
    ('Yacute',0xdd),('yacute',0xfd),('Ybelowdot',0x1001ef4),('ybelowdot',0x1001ef5),
    ('Ycircumflex',0x1000176),('ycircumflex',0x1000177),('Ydiaeresis',0x13be),('ydiaeresis',0xff),
    ('yen',0xa5),('Ygrave',0x1001ef2),('ygrave',0x1001ef3),('Yhook',0x1001ef6),
    ('yhook',0x1001ef7),('Ytilde',0x1001ef8),('ytilde',0x1001ef9),('Z',0x5a),
    ('z',0x7a),('Zabovedot',0x1af),('zabovedot',0x1bf),('Zacute',0x1ac),
    ('zacute',0x1bc),('Zcaron',0x1ae),('zcaron',0x1be),('Zen_Koho',0xff3d),
    ('Zenkaku',0xff28),('Zenkaku_Hankaku',0xff2a),('zerosubscript',0x1002080),('zerosuperior',0x1002070),
    ('Zstroke',0x10001b5),('zstroke',0x10001b6),
]
# keysym_to_name: canonical (get_name) table.
_KEYSYM_TO_NAME = {
    0x0:'NoSymbol',0x20:'space',0x21:'exclam',0x22:'quotedbl',0x23:'numbersign',
    0x24:'dollar',0x25:'percent',0x26:'ampersand',0x27:'apostrophe',0x28:'parenleft',
    0x29:'parenright',0x2a:'asterisk',0x2b:'plus',0x2c:'comma',0x2d:'minus',
    0x2e:'period',0x2f:'slash',0x30:'0',0x31:'1',0x32:'2',
    0x33:'3',0x34:'4',0x35:'5',0x36:'6',0x37:'7',
    0x38:'8',0x39:'9',0x3a:'colon',0x3b:'semicolon',0x3c:'less',
    0x3d:'equal',0x3e:'greater',0x3f:'question',0x40:'at',0x41:'A',
    0x42:'B',0x43:'C',0x44:'D',0x45:'E',0x46:'F',
    0x47:'G',0x48:'H',0x49:'I',0x4a:'J',0x4b:'K',
    0x4c:'L',0x4d:'M',0x4e:'N',0x4f:'O',0x50:'P',
    0x51:'Q',0x52:'R',0x53:'S',0x54:'T',0x55:'U',
    0x56:'V',0x57:'W',0x58:'X',0x59:'Y',0x5a:'Z',
    0x5b:'bracketleft',0x5c:'backslash',0x5d:'bracketright',0x5e:'asciicircum',0x5f:'underscore',
    0x60:'grave',0x61:'a',0x62:'b',0x63:'c',0x64:'d',
    0x65:'e',0x66:'f',0x67:'g',0x68:'h',0x69:'i',
    0x6a:'j',0x6b:'k',0x6c:'l',0x6d:'m',0x6e:'n',
    0x6f:'o',0x70:'p',0x71:'q',0x72:'r',0x73:'s',
    0x74:'t',0x75:'u',0x76:'v',0x77:'w',0x78:'x',
    0x79:'y',0x7a:'z',0x7b:'braceleft',0x7c:'bar',0x7d:'braceright',
    0x7e:'asciitilde',0xa0:'nobreakspace',0xa1:'exclamdown',0xa2:'cent',0xa3:'sterling',
    0xa4:'currency',0xa5:'yen',0xa6:'brokenbar',0xa7:'section',0xa8:'diaeresis',
    0xa9:'copyright',0xaa:'ordfeminine',0xab:'guillemotleft',0xac:'notsign',0xad:'hyphen',
    0xae:'registered',0xaf:'macron',0xb0:'degree',0xb1:'plusminus',0xb2:'twosuperior',
    0xb3:'threesuperior',0xb4:'acute',0xb5:'mu',0xb6:'paragraph',0xb7:'periodcentered',
    0xb8:'cedilla',0xb9:'onesuperior',0xba:'masculine',0xbb:'guillemotright',0xbc:'onequarter',
    0xbd:'onehalf',0xbe:'threequarters',0xbf:'questiondown',0xc0:'Agrave',0xc1:'Aacute',
    0xc2:'Acircumflex',0xc3:'Atilde',0xc4:'Adiaeresis',0xc5:'Aring',0xc6:'AE',
    0xc7:'Ccedilla',0xc8:'Egrave',0xc9:'Eacute',0xca:'Ecircumflex',0xcb:'Ediaeresis',
    0xcc:'Igrave',0xcd:'Iacute',0xce:'Icircumflex',0xcf:'Idiaeresis',0xd0:'ETH',
    0xd1:'Ntilde',0xd2:'Ograve',0xd3:'Oacute',0xd4:'Ocircumflex',0xd5:'Otilde',
    0xd6:'Odiaeresis',0xd7:'multiply',0xd8:'Oslash',0xd9:'Ugrave',0xda:'Uacute',
    0xdb:'Ucircumflex',0xdc:'Udiaeresis',0xdd:'Yacute',0xde:'THORN',0xdf:'ssharp',
    0xe0:'agrave',0xe1:'aacute',0xe2:'acircumflex',0xe3:'atilde',0xe4:'adiaeresis',
    0xe5:'aring',0xe6:'ae',0xe7:'ccedilla',0xe8:'egrave',0xe9:'eacute',
    0xea:'ecircumflex',0xeb:'ediaeresis',0xec:'igrave',0xed:'iacute',0xee:'icircumflex',
    0xef:'idiaeresis',0xf0:'eth',0xf1:'ntilde',0xf2:'ograve',0xf3:'oacute',
    0xf4:'ocircumflex',0xf5:'otilde',0xf6:'odiaeresis',0xf7:'division',0xf8:'oslash',
    0xf9:'ugrave',0xfa:'uacute',0xfb:'ucircumflex',0xfc:'udiaeresis',0xfd:'yacute',
    0xfe:'thorn',0xff:'ydiaeresis',0x1a1:'Aogonek',0x1a2:'breve',0x1a3:'Lstroke',
    0x1a5:'Lcaron',0x1a6:'Sacute',0x1a9:'Scaron',0x1aa:'Scedilla',0x1ab:'Tcaron',
    0x1ac:'Zacute',0x1ae:'Zcaron',0x1af:'Zabovedot',0x1b1:'aogonek',0x1b2:'ogonek',
    0x1b3:'lstroke',0x1b5:'lcaron',0x1b6:'sacute',0x1b7:'caron',0x1b9:'scaron',
    0x1ba:'scedilla',0x1bb:'tcaron',0x1bc:'zacute',0x1bd:'doubleacute',0x1be:'zcaron',
    0x1bf:'zabovedot',0x1c0:'Racute',0x1c3:'Abreve',0x1c5:'Lacute',0x1c6:'Cacute',
    0x1c8:'Ccaron',0x1ca:'Eogonek',0x1cc:'Ecaron',0x1cf:'Dcaron',0x1d0:'Dstroke',
    0x1d1:'Nacute',0x1d2:'Ncaron',0x1d5:'Odoubleacute',0x1d8:'Rcaron',0x1d9:'Uring',
    0x1db:'Udoubleacute',0x1de:'Tcedilla',0x1e0:'racute',0x1e3:'abreve',0x1e5:'lacute',
    0x1e6:'cacute',0x1e8:'ccaron',0x1ea:'eogonek',0x1ec:'ecaron',0x1ef:'dcaron',
    0x1f0:'dstroke',0x1f1:'nacute',0x1f2:'ncaron',0x1f5:'odoubleacute',0x1f8:'rcaron',
    0x1f9:'uring',0x1fb:'udoubleacute',0x1fe:'tcedilla',0x1ff:'abovedot',0x2a1:'Hstroke',
    0x2a6:'Hcircumflex',0x2a9:'Iabovedot',0x2ab:'Gbreve',0x2ac:'Jcircumflex',0x2b1:'hstroke',
    0x2b6:'hcircumflex',0x2b9:'idotless',0x2bb:'gbreve',0x2bc:'jcircumflex',0x2c5:'Cabovedot',
    0x2c6:'Ccircumflex',0x2d5:'Gabovedot',0x2d8:'Gcircumflex',0x2dd:'Ubreve',0x2de:'Scircumflex',
    0x2e5:'cabovedot',0x2e6:'ccircumflex',0x2f5:'gabovedot',0x2f8:'gcircumflex',0x2fd:'ubreve',
    0x2fe:'scircumflex',0x3a2:'kra',0x3a3:'Rcedilla',0x3a5:'Itilde',0x3a6:'Lcedilla',
    0x3aa:'Emacron',0x3ab:'Gcedilla',0x3ac:'Tslash',0x3b3:'rcedilla',0x3b5:'itilde',
    0x3b6:'lcedilla',0x3ba:'emacron',0x3bb:'gcedilla',0x3bc:'tslash',0x3bd:'ENG',
    0x3bf:'eng',0x3c0:'Amacron',0x3c7:'Iogonek',0x3cc:'Eabovedot',0x3cf:'Imacron',
    0x3d1:'Ncedilla',0x3d2:'Omacron',0x3d3:'Kcedilla',0x3d9:'Uogonek',0x3dd:'Utilde',
    0x3de:'Umacron',0x3e0:'amacron',0x3e7:'iogonek',0x3ec:'eabovedot',0x3ef:'imacron',
    0x3f1:'ncedilla',0x3f2:'omacron',0x3f3:'kcedilla',0x3f9:'uogonek',0x3fd:'utilde',
    0x3fe:'umacron',0x47e:'overline',0x4a1:'kana_fullstop',0x4a2:'kana_openingbracket',0x4a3:'kana_closingbracket',
    0x4a4:'kana_comma',0x4a5:'kana_conjunctive',0x4a6:'kana_WO',0x4a7:'kana_a',0x4a8:'kana_i',
    0x4a9:'kana_u',0x4aa:'kana_e',0x4ab:'kana_o',0x4ac:'kana_ya',0x4ad:'kana_yu',
    0x4ae:'kana_yo',0x4af:'kana_tsu',0x4b0:'prolongedsound',0x4b1:'kana_A',0x4b2:'kana_I',
    0x4b3:'kana_U',0x4b4:'kana_E',0x4b5:'kana_O',0x4b6:'kana_KA',0x4b7:'kana_KI',
    0x4b8:'kana_KU',0x4b9:'kana_KE',0x4ba:'kana_KO',0x4bb:'kana_SA',0x4bc:'kana_SHI',
    0x4bd:'kana_SU',0x4be:'kana_SE',0x4bf:'kana_SO',0x4c0:'kana_TA',0x4c1:'kana_CHI',
    0x4c2:'kana_TSU',0x4c3:'kana_TE',0x4c4:'kana_TO',0x4c5:'kana_NA',0x4c6:'kana_NI',
    0x4c7:'kana_NU',0x4c8:'kana_NE',0x4c9:'kana_NO',0x4ca:'kana_HA',0x4cb:'kana_HI',
    0x4cc:'kana_FU',0x4cd:'kana_HE',0x4ce:'kana_HO',0x4cf:'kana_MA',0x4d0:'kana_MI',
    0x4d1:'kana_MU',0x4d2:'kana_ME',0x4d3:'kana_MO',0x4d4:'kana_YA',0x4d5:'kana_YU',
    0x4d6:'kana_YO',0x4d7:'kana_RA',0x4d8:'kana_RI',0x4d9:'kana_RU',0x4da:'kana_RE',
    0x4db:'kana_RO',0x4dc:'kana_WA',0x4dd:'kana_N',0x4de:'voicedsound',0x4df:'semivoicedsound',
    0x5ac:'Arabic_comma',0x5bb:'Arabic_semicolon',0x5bf:'Arabic_question_mark',0x5c1:'Arabic_hamza',0x5c2:'Arabic_maddaonalef',
    0x5c3:'Arabic_hamzaonalef',0x5c4:'Arabic_hamzaonwaw',0x5c5:'Arabic_hamzaunderalef',0x5c6:'Arabic_hamzaonyeh',0x5c7:'Arabic_alef',
    0x5c8:'Arabic_beh',0x5c9:'Arabic_tehmarbuta',0x5ca:'Arabic_teh',0x5cb:'Arabic_theh',0x5cc:'Arabic_jeem',
    0x5cd:'Arabic_hah',0x5ce:'Arabic_khah',0x5cf:'Arabic_dal',0x5d0:'Arabic_thal',0x5d1:'Arabic_ra',
    0x5d2:'Arabic_zain',0x5d3:'Arabic_seen',0x5d4:'Arabic_sheen',0x5d5:'Arabic_sad',0x5d6:'Arabic_dad',
    0x5d7:'Arabic_tah',0x5d8:'Arabic_zah',0x5d9:'Arabic_ain',0x5da:'Arabic_ghain',0x5e0:'Arabic_tatweel',
    0x5e1:'Arabic_feh',0x5e2:'Arabic_qaf',0x5e3:'Arabic_kaf',0x5e4:'Arabic_lam',0x5e5:'Arabic_meem',
    0x5e6:'Arabic_noon',0x5e7:'Arabic_ha',0x5e8:'Arabic_waw',0x5e9:'Arabic_alefmaksura',0x5ea:'Arabic_yeh',
    0x5eb:'Arabic_fathatan',0x5ec:'Arabic_dammatan',0x5ed:'Arabic_kasratan',0x5ee:'Arabic_fatha',0x5ef:'Arabic_damma',
    0x5f0:'Arabic_kasra',0x5f1:'Arabic_shadda',0x5f2:'Arabic_sukun',0x6a1:'Serbian_dje',0x6a2:'Macedonia_gje',
    0x6a3:'Cyrillic_io',0x6a4:'Ukrainian_ie',0x6a5:'Macedonia_dse',0x6a6:'Ukrainian_i',0x6a7:'Ukrainian_yi',
    0x6a8:'Cyrillic_je',0x6a9:'Cyrillic_lje',0x6aa:'Cyrillic_nje',0x6ab:'Serbian_tshe',0x6ac:'Macedonia_kje',
    0x6ad:'Ukrainian_ghe_with_upturn',0x6ae:'Byelorussian_shortu',0x6af:'Cyrillic_dzhe',0x6b0:'numerosign',0x6b1:'Serbian_DJE',
    0x6b2:'Macedonia_GJE',0x6b3:'Cyrillic_IO',0x6b4:'Ukrainian_IE',0x6b5:'Macedonia_DSE',0x6b6:'Ukrainian_I',
    0x6b7:'Ukrainian_YI',0x6b8:'Cyrillic_JE',0x6b9:'Cyrillic_LJE',0x6ba:'Cyrillic_NJE',0x6bb:'Serbian_TSHE',
    0x6bc:'Macedonia_KJE',0x6bd:'Ukrainian_GHE_WITH_UPTURN',0x6be:'Byelorussian_SHORTU',0x6bf:'Cyrillic_DZHE',0x6c0:'Cyrillic_yu',
    0x6c1:'Cyrillic_a',0x6c2:'Cyrillic_be',0x6c3:'Cyrillic_tse',0x6c4:'Cyrillic_de',0x6c5:'Cyrillic_ie',
    0x6c6:'Cyrillic_ef',0x6c7:'Cyrillic_ghe',0x6c8:'Cyrillic_ha',0x6c9:'Cyrillic_i',0x6ca:'Cyrillic_shorti',
    0x6cb:'Cyrillic_ka',0x6cc:'Cyrillic_el',0x6cd:'Cyrillic_em',0x6ce:'Cyrillic_en',0x6cf:'Cyrillic_o',
    0x6d0:'Cyrillic_pe',0x6d1:'Cyrillic_ya',0x6d2:'Cyrillic_er',0x6d3:'Cyrillic_es',0x6d4:'Cyrillic_te',
    0x6d5:'Cyrillic_u',0x6d6:'Cyrillic_zhe',0x6d7:'Cyrillic_ve',0x6d8:'Cyrillic_softsign',0x6d9:'Cyrillic_yeru',
    0x6da:'Cyrillic_ze',0x6db:'Cyrillic_sha',0x6dc:'Cyrillic_e',0x6dd:'Cyrillic_shcha',0x6de:'Cyrillic_che',
    0x6df:'Cyrillic_hardsign',0x6e0:'Cyrillic_YU',0x6e1:'Cyrillic_A',0x6e2:'Cyrillic_BE',0x6e3:'Cyrillic_TSE',
    0x6e4:'Cyrillic_DE',0x6e5:'Cyrillic_IE',0x6e6:'Cyrillic_EF',0x6e7:'Cyrillic_GHE',0x6e8:'Cyrillic_HA',
    0x6e9:'Cyrillic_I',0x6ea:'Cyrillic_SHORTI',0x6eb:'Cyrillic_KA',0x6ec:'Cyrillic_EL',0x6ed:'Cyrillic_EM',
    0x6ee:'Cyrillic_EN',0x6ef:'Cyrillic_O',0x6f0:'Cyrillic_PE',0x6f1:'Cyrillic_YA',0x6f2:'Cyrillic_ER',
    0x6f3:'Cyrillic_ES',0x6f4:'Cyrillic_TE',0x6f5:'Cyrillic_U',0x6f6:'Cyrillic_ZHE',0x6f7:'Cyrillic_VE',
    0x6f8:'Cyrillic_SOFTSIGN',0x6f9:'Cyrillic_YERU',0x6fa:'Cyrillic_ZE',0x6fb:'Cyrillic_SHA',0x6fc:'Cyrillic_E',
    0x6fd:'Cyrillic_SHCHA',0x6fe:'Cyrillic_CHE',0x6ff:'Cyrillic_HARDSIGN',0x7a1:'Greek_ALPHAaccent',0x7a2:'Greek_EPSILONaccent',
    0x7a3:'Greek_ETAaccent',0x7a4:'Greek_IOTAaccent',0x7a5:'Greek_IOTAdieresis',0x7a7:'Greek_OMICRONaccent',0x7a8:'Greek_UPSILONaccent',
    0x7a9:'Greek_UPSILONdieresis',0x7ab:'Greek_OMEGAaccent',0x7ae:'Greek_accentdieresis',0x7af:'Greek_horizbar',0x7b1:'Greek_alphaaccent',
    0x7b2:'Greek_epsilonaccent',0x7b3:'Greek_etaaccent',0x7b4:'Greek_iotaaccent',0x7b5:'Greek_iotadieresis',0x7b6:'Greek_iotaaccentdieresis',
    0x7b7:'Greek_omicronaccent',0x7b8:'Greek_upsilonaccent',0x7b9:'Greek_upsilondieresis',0x7ba:'Greek_upsilonaccentdieresis',0x7bb:'Greek_omegaaccent',
    0x7c1:'Greek_ALPHA',0x7c2:'Greek_BETA',0x7c3:'Greek_GAMMA',0x7c4:'Greek_DELTA',0x7c5:'Greek_EPSILON',
    0x7c6:'Greek_ZETA',0x7c7:'Greek_ETA',0x7c8:'Greek_THETA',0x7c9:'Greek_IOTA',0x7ca:'Greek_KAPPA',
    0x7cb:'Greek_LAMDA',0x7cc:'Greek_MU',0x7cd:'Greek_NU',0x7ce:'Greek_XI',0x7cf:'Greek_OMICRON',
    0x7d0:'Greek_PI',0x7d1:'Greek_RHO',0x7d2:'Greek_SIGMA',0x7d4:'Greek_TAU',0x7d5:'Greek_UPSILON',
    0x7d6:'Greek_PHI',0x7d7:'Greek_CHI',0x7d8:'Greek_PSI',0x7d9:'Greek_OMEGA',0x7e1:'Greek_alpha',
    0x7e2:'Greek_beta',0x7e3:'Greek_gamma',0x7e4:'Greek_delta',0x7e5:'Greek_epsilon',0x7e6:'Greek_zeta',
    0x7e7:'Greek_eta',0x7e8:'Greek_theta',0x7e9:'Greek_iota',0x7ea:'Greek_kappa',0x7eb:'Greek_lamda',
    0x7ec:'Greek_mu',0x7ed:'Greek_nu',0x7ee:'Greek_xi',0x7ef:'Greek_omicron',0x7f0:'Greek_pi',
    0x7f1:'Greek_rho',0x7f2:'Greek_sigma',0x7f3:'Greek_finalsmallsigma',0x7f4:'Greek_tau',0x7f5:'Greek_upsilon',
    0x7f6:'Greek_phi',0x7f7:'Greek_chi',0x7f8:'Greek_psi',0x7f9:'Greek_omega',0x8a1:'leftradical',
    0x8a2:'topleftradical',0x8a3:'horizconnector',0x8a4:'topintegral',0x8a5:'botintegral',0x8a6:'vertconnector',
    0x8a7:'topleftsqbracket',0x8a8:'botleftsqbracket',0x8a9:'toprightsqbracket',0x8aa:'botrightsqbracket',0x8ab:'topleftparens',
    0x8ac:'botleftparens',0x8ad:'toprightparens',0x8ae:'botrightparens',0x8af:'leftmiddlecurlybrace',0x8b0:'rightmiddlecurlybrace',
    0x8b1:'topleftsummation',0x8b2:'botleftsummation',0x8b3:'topvertsummationconnector',0x8b4:'botvertsummationconnector',0x8b5:'toprightsummation',
    0x8b6:'botrightsummation',0x8b7:'rightmiddlesummation',0x8bc:'lessthanequal',0x8bd:'notequal',0x8be:'greaterthanequal',
    0x8bf:'integral',0x8c0:'therefore',0x8c1:'variation',0x8c2:'infinity',0x8c5:'nabla',
    0x8c8:'approximate',0x8c9:'similarequal',0x8cd:'ifonlyif',0x8ce:'implies',0x8cf:'identical',
    0x8d6:'radical',0x8da:'includedin',0x8db:'includes',0x8dc:'intersection',0x8dd:'union',
    0x8de:'logicaland',0x8df:'logicalor',0x8ef:'partialderivative',0x8f6:'function',0x8fb:'leftarrow',
    0x8fc:'uparrow',0x8fd:'rightarrow',0x8fe:'downarrow',0x9df:'blank',0x9e0:'soliddiamond',
    0x9e1:'checkerboard',0x9e2:'ht',0x9e3:'ff',0x9e4:'cr',0x9e5:'lf',
    0x9e8:'nl',0x9e9:'vt',0x9ea:'lowrightcorner',0x9eb:'uprightcorner',0x9ec:'upleftcorner',
    0x9ed:'lowleftcorner',0x9ee:'crossinglines',0x9ef:'horizlinescan1',0x9f0:'horizlinescan3',0x9f1:'horizlinescan5',
    0x9f2:'horizlinescan7',0x9f3:'horizlinescan9',0x9f4:'leftt',0x9f5:'rightt',0x9f6:'bott',
    0x9f7:'topt',0x9f8:'vertbar',0xaa1:'emspace',0xaa2:'enspace',0xaa3:'em3space',
    0xaa4:'em4space',0xaa5:'digitspace',0xaa6:'punctspace',0xaa7:'thinspace',0xaa8:'hairspace',
    0xaa9:'emdash',0xaaa:'endash',0xaac:'signifblank',0xaae:'ellipsis',0xaaf:'doubbaselinedot',
    0xab0:'onethird',0xab1:'twothirds',0xab2:'onefifth',0xab3:'twofifths',0xab4:'threefifths',
    0xab5:'fourfifths',0xab6:'onesixth',0xab7:'fivesixths',0xab8:'careof',0xabb:'figdash',
    0xabc:'leftanglebracket',0xabd:'decimalpoint',0xabe:'rightanglebracket',0xabf:'marker',0xac3:'oneeighth',
    0xac4:'threeeighths',0xac5:'fiveeighths',0xac6:'seveneighths',0xac9:'trademark',0xaca:'signaturemark',
    0xacb:'trademarkincircle',0xacc:'leftopentriangle',0xacd:'rightopentriangle',0xace:'emopencircle',0xacf:'emopenrectangle',
    0xad0:'leftsinglequotemark',0xad1:'rightsinglequotemark',0xad2:'leftdoublequotemark',0xad3:'rightdoublequotemark',0xad4:'prescription',
    0xad5:'permille',0xad6:'minutes',0xad7:'seconds',0xad9:'latincross',0xada:'hexagram',
    0xadb:'filledrectbullet',0xadc:'filledlefttribullet',0xadd:'filledrighttribullet',0xade:'emfilledcircle',0xadf:'emfilledrect',
    0xae0:'enopencircbullet',0xae1:'enopensquarebullet',0xae2:'openrectbullet',0xae3:'opentribulletup',0xae4:'opentribulletdown',
    0xae5:'openstar',0xae6:'enfilledcircbullet',0xae7:'enfilledsqbullet',0xae8:'filledtribulletup',0xae9:'filledtribulletdown',
    0xaea:'leftpointer',0xaeb:'rightpointer',0xaec:'club',0xaed:'diamond',0xaee:'heart',
    0xaf0:'maltesecross',0xaf1:'dagger',0xaf2:'doubledagger',0xaf3:'checkmark',0xaf4:'ballotcross',
    0xaf5:'musicalsharp',0xaf6:'musicalflat',0xaf7:'malesymbol',0xaf8:'femalesymbol',0xaf9:'telephone',
    0xafa:'telephonerecorder',0xafb:'phonographcopyright',0xafc:'caret',0xafd:'singlelowquotemark',0xafe:'doublelowquotemark',
    0xaff:'cursor',0xba3:'leftcaret',0xba6:'rightcaret',0xba8:'downcaret',0xba9:'upcaret',
    0xbc0:'overbar',0xbc2:'downtack',0xbc3:'upshoe',0xbc4:'downstile',0xbc6:'underbar',
    0xbca:'jot',0xbcc:'quad',0xbce:'uptack',0xbcf:'circle',0xbd3:'upstile',
    0xbd6:'downshoe',0xbd8:'rightshoe',0xbda:'leftshoe',0xbdc:'lefttack',0xbfc:'righttack',
    0xcdf:'hebrew_doublelowline',0xce0:'hebrew_aleph',0xce1:'hebrew_bet',0xce2:'hebrew_gimel',0xce3:'hebrew_dalet',
    0xce4:'hebrew_he',0xce5:'hebrew_waw',0xce6:'hebrew_zain',0xce7:'hebrew_chet',0xce8:'hebrew_tet',
    0xce9:'hebrew_yod',0xcea:'hebrew_finalkaph',0xceb:'hebrew_kaph',0xcec:'hebrew_lamed',0xced:'hebrew_finalmem',
    0xcee:'hebrew_mem',0xcef:'hebrew_finalnun',0xcf0:'hebrew_nun',0xcf1:'hebrew_samech',0xcf2:'hebrew_ayin',
    0xcf3:'hebrew_finalpe',0xcf4:'hebrew_pe',0xcf5:'hebrew_finalzade',0xcf6:'hebrew_zade',0xcf7:'hebrew_qoph',
    0xcf8:'hebrew_resh',0xcf9:'hebrew_shin',0xcfa:'hebrew_taw',0xda1:'Thai_kokai',0xda2:'Thai_khokhai',
    0xda3:'Thai_khokhuat',0xda4:'Thai_khokhwai',0xda5:'Thai_khokhon',0xda6:'Thai_khorakhang',0xda7:'Thai_ngongu',
    0xda8:'Thai_chochan',0xda9:'Thai_choching',0xdaa:'Thai_chochang',0xdab:'Thai_soso',0xdac:'Thai_chochoe',
    0xdad:'Thai_yoying',0xdae:'Thai_dochada',0xdaf:'Thai_topatak',0xdb0:'Thai_thothan',0xdb1:'Thai_thonangmontho',
    0xdb2:'Thai_thophuthao',0xdb3:'Thai_nonen',0xdb4:'Thai_dodek',0xdb5:'Thai_totao',0xdb6:'Thai_thothung',
    0xdb7:'Thai_thothahan',0xdb8:'Thai_thothong',0xdb9:'Thai_nonu',0xdba:'Thai_bobaimai',0xdbb:'Thai_popla',
    0xdbc:'Thai_phophung',0xdbd:'Thai_fofa',0xdbe:'Thai_phophan',0xdbf:'Thai_fofan',0xdc0:'Thai_phosamphao',
    0xdc1:'Thai_moma',0xdc2:'Thai_yoyak',0xdc3:'Thai_rorua',0xdc4:'Thai_ru',0xdc5:'Thai_loling',
    0xdc6:'Thai_lu',0xdc7:'Thai_wowaen',0xdc8:'Thai_sosala',0xdc9:'Thai_sorusi',0xdca:'Thai_sosua',
    0xdcb:'Thai_hohip',0xdcc:'Thai_lochula',0xdcd:'Thai_oang',0xdce:'Thai_honokhuk',0xdcf:'Thai_paiyannoi',
    0xdd0:'Thai_saraa',0xdd1:'Thai_maihanakat',0xdd2:'Thai_saraaa',0xdd3:'Thai_saraam',0xdd4:'Thai_sarai',
    0xdd5:'Thai_saraii',0xdd6:'Thai_saraue',0xdd7:'Thai_sarauee',0xdd8:'Thai_sarau',0xdd9:'Thai_sarauu',
    0xdda:'Thai_phinthu',0xdde:'Thai_maihanakat_maitho',0xddf:'Thai_baht',0xde0:'Thai_sarae',0xde1:'Thai_saraae',
    0xde2:'Thai_sarao',0xde3:'Thai_saraaimaimuan',0xde4:'Thai_saraaimaimalai',0xde5:'Thai_lakkhangyao',0xde6:'Thai_maiyamok',
    0xde7:'Thai_maitaikhu',0xde8:'Thai_maiek',0xde9:'Thai_maitho',0xdea:'Thai_maitri',0xdeb:'Thai_maichattawa',
    0xdec:'Thai_thanthakhat',0xded:'Thai_nikhahit',0xdf0:'Thai_leksun',0xdf1:'Thai_leknung',0xdf2:'Thai_leksong',
    0xdf3:'Thai_leksam',0xdf4:'Thai_leksi',0xdf5:'Thai_lekha',0xdf6:'Thai_lekhok',0xdf7:'Thai_lekchet',
    0xdf8:'Thai_lekpaet',0xdf9:'Thai_lekkao',0xea1:'Hangul_Kiyeog',0xea2:'Hangul_SsangKiyeog',0xea3:'Hangul_KiyeogSios',
    0xea4:'Hangul_Nieun',0xea5:'Hangul_NieunJieuj',0xea6:'Hangul_NieunHieuh',0xea7:'Hangul_Dikeud',0xea8:'Hangul_SsangDikeud',
    0xea9:'Hangul_Rieul',0xeaa:'Hangul_RieulKiyeog',0xeab:'Hangul_RieulMieum',0xeac:'Hangul_RieulPieub',0xead:'Hangul_RieulSios',
    0xeae:'Hangul_RieulTieut',0xeaf:'Hangul_RieulPhieuf',0xeb0:'Hangul_RieulHieuh',0xeb1:'Hangul_Mieum',0xeb2:'Hangul_Pieub',
    0xeb3:'Hangul_SsangPieub',0xeb4:'Hangul_PieubSios',0xeb5:'Hangul_Sios',0xeb6:'Hangul_SsangSios',0xeb7:'Hangul_Ieung',
    0xeb8:'Hangul_Jieuj',0xeb9:'Hangul_SsangJieuj',0xeba:'Hangul_Cieuc',0xebb:'Hangul_Khieuq',0xebc:'Hangul_Tieut',
    0xebd:'Hangul_Phieuf',0xebe:'Hangul_Hieuh',0xebf:'Hangul_A',0xec0:'Hangul_AE',0xec1:'Hangul_YA',
    0xec2:'Hangul_YAE',0xec3:'Hangul_EO',0xec4:'Hangul_E',0xec5:'Hangul_YEO',0xec6:'Hangul_YE',
    0xec7:'Hangul_O',0xec8:'Hangul_WA',0xec9:'Hangul_WAE',0xeca:'Hangul_OE',0xecb:'Hangul_YO',
    0xecc:'Hangul_U',0xecd:'Hangul_WEO',0xece:'Hangul_WE',0xecf:'Hangul_WI',0xed0:'Hangul_YU',
    0xed1:'Hangul_EU',0xed2:'Hangul_YI',0xed3:'Hangul_I',0xed4:'Hangul_J_Kiyeog',0xed5:'Hangul_J_SsangKiyeog',
    0xed6:'Hangul_J_KiyeogSios',0xed7:'Hangul_J_Nieun',0xed8:'Hangul_J_NieunJieuj',0xed9:'Hangul_J_NieunHieuh',0xeda:'Hangul_J_Dikeud',
    0xedb:'Hangul_J_Rieul',0xedc:'Hangul_J_RieulKiyeog',0xedd:'Hangul_J_RieulMieum',0xede:'Hangul_J_RieulPieub',0xedf:'Hangul_J_RieulSios',
    0xee0:'Hangul_J_RieulTieut',0xee1:'Hangul_J_RieulPhieuf',0xee2:'Hangul_J_RieulHieuh',0xee3:'Hangul_J_Mieum',0xee4:'Hangul_J_Pieub',
    0xee5:'Hangul_J_PieubSios',0xee6:'Hangul_J_Sios',0xee7:'Hangul_J_SsangSios',0xee8:'Hangul_J_Ieung',0xee9:'Hangul_J_Jieuj',
    0xeea:'Hangul_J_Cieuc',0xeeb:'Hangul_J_Khieuq',0xeec:'Hangul_J_Tieut',0xeed:'Hangul_J_Phieuf',0xeee:'Hangul_J_Hieuh',
    0xeef:'Hangul_RieulYeorinHieuh',0xef0:'Hangul_SunkyeongeumMieum',0xef1:'Hangul_SunkyeongeumPieub',0xef2:'Hangul_PanSios',0xef3:'Hangul_KkogjiDalrinIeung',
    0xef4:'Hangul_SunkyeongeumPhieuf',0xef5:'Hangul_YeorinHieuh',0xef6:'Hangul_AraeA',0xef7:'Hangul_AraeAE',0xef8:'Hangul_J_PanSios',
    0xef9:'Hangul_J_KkogjiDalrinIeung',0xefa:'Hangul_J_YeorinHieuh',0xeff:'Korean_Won',0x13bc:'OE',0x13bd:'oe',
    0x13be:'Ydiaeresis',0x20ac:'EuroSign',0xfd01:'3270_Duplicate',0xfd02:'3270_FieldMark',0xfd03:'3270_Right2',
    0xfd04:'3270_Left2',0xfd05:'3270_BackTab',0xfd06:'3270_EraseEOF',0xfd07:'3270_EraseInput',0xfd08:'3270_Reset',
    0xfd09:'3270_Quit',0xfd0a:'3270_PA1',0xfd0b:'3270_PA2',0xfd0c:'3270_PA3',0xfd0d:'3270_Test',
    0xfd0e:'3270_Attn',0xfd0f:'3270_CursorBlink',0xfd10:'3270_AltCursor',0xfd11:'3270_KeyClick',0xfd12:'3270_Jump',
    0xfd13:'3270_Ident',0xfd14:'3270_Rule',0xfd15:'3270_Copy',0xfd16:'3270_Play',0xfd17:'3270_Setup',
    0xfd18:'3270_Record',0xfd19:'3270_ChangeScreen',0xfd1a:'3270_DeleteWord',0xfd1b:'3270_ExSelect',0xfd1c:'3270_CursorSelect',
    0xfd1d:'3270_PrintScreen',0xfd1e:'3270_Enter',0xfe01:'ISO_Lock',0xfe02:'ISO_Level2_Latch',0xfe03:'ISO_Level3_Shift',
    0xfe04:'ISO_Level3_Latch',0xfe05:'ISO_Level3_Lock',0xfe06:'ISO_Group_Latch',0xfe07:'ISO_Group_Lock',0xfe08:'ISO_Next_Group',
    0xfe09:'ISO_Next_Group_Lock',0xfe0a:'ISO_Prev_Group',0xfe0b:'ISO_Prev_Group_Lock',0xfe0c:'ISO_First_Group',0xfe0d:'ISO_First_Group_Lock',
    0xfe0e:'ISO_Last_Group',0xfe0f:'ISO_Last_Group_Lock',0xfe11:'ISO_Level5_Shift',0xfe12:'ISO_Level5_Latch',0xfe13:'ISO_Level5_Lock',
    0xfe20:'ISO_Left_Tab',0xfe21:'ISO_Move_Line_Up',0xfe22:'ISO_Move_Line_Down',0xfe23:'ISO_Partial_Line_Up',0xfe24:'ISO_Partial_Line_Down',
    0xfe25:'ISO_Partial_Space_Left',0xfe26:'ISO_Partial_Space_Right',0xfe27:'ISO_Set_Margin_Left',0xfe28:'ISO_Set_Margin_Right',0xfe29:'ISO_Release_Margin_Left',
    0xfe2a:'ISO_Release_Margin_Right',0xfe2b:'ISO_Release_Both_Margins',0xfe2c:'ISO_Fast_Cursor_Left',0xfe2d:'ISO_Fast_Cursor_Right',0xfe2e:'ISO_Fast_Cursor_Up',
    0xfe2f:'ISO_Fast_Cursor_Down',0xfe30:'ISO_Continuous_Underline',0xfe31:'ISO_Discontinuous_Underline',0xfe32:'ISO_Emphasize',0xfe33:'ISO_Center_Object',
    0xfe34:'ISO_Enter',0xfe50:'dead_grave',0xfe51:'dead_acute',0xfe52:'dead_circumflex',0xfe53:'dead_tilde',
    0xfe54:'dead_macron',0xfe55:'dead_breve',0xfe56:'dead_abovedot',0xfe57:'dead_diaeresis',0xfe58:'dead_abovering',
    0xfe59:'dead_doubleacute',0xfe5a:'dead_caron',0xfe5b:'dead_cedilla',0xfe5c:'dead_ogonek',0xfe5d:'dead_iota',
    0xfe5e:'dead_voiced_sound',0xfe5f:'dead_semivoiced_sound',0xfe60:'dead_belowdot',0xfe61:'dead_hook',0xfe62:'dead_horn',
    0xfe63:'dead_stroke',0xfe64:'dead_abovecomma',0xfe65:'dead_abovereversedcomma',0xfe66:'dead_doublegrave',0xfe67:'dead_belowring',
    0xfe68:'dead_belowmacron',0xfe69:'dead_belowcircumflex',0xfe6a:'dead_belowtilde',0xfe6b:'dead_belowbreve',0xfe6c:'dead_belowdiaeresis',
    0xfe6d:'dead_invertedbreve',0xfe6e:'dead_belowcomma',0xfe6f:'dead_currency',0xfe70:'AccessX_Enable',0xfe71:'AccessX_Feedback_Enable',
    0xfe72:'RepeatKeys_Enable',0xfe73:'SlowKeys_Enable',0xfe74:'BounceKeys_Enable',0xfe75:'StickyKeys_Enable',0xfe76:'MouseKeys_Enable',
    0xfe77:'MouseKeys_Accel_Enable',0xfe78:'Overlay1_Enable',0xfe79:'Overlay2_Enable',0xfe7a:'AudibleBell_Enable',0xfe80:'dead_a',
    0xfe81:'dead_A',0xfe82:'dead_e',0xfe83:'dead_E',0xfe84:'dead_i',0xfe85:'dead_I',
    0xfe86:'dead_o',0xfe87:'dead_O',0xfe88:'dead_u',0xfe89:'dead_U',0xfe8a:'dead_small_schwa',
    0xfe8b:'dead_capital_schwa',0xfe8c:'dead_greek',0xfe8d:'dead_hamza',0xfe8e:'dead_apostrophe',0xfe90:'dead_lowline',
    0xfe91:'dead_aboveverticalline',0xfe92:'dead_belowverticalline',0xfe93:'dead_longsolidusoverlay',0xfea0:'ch',0xfea1:'Ch',
    0xfea2:'CH',0xfea3:'c_h',0xfea4:'C_h',0xfea5:'C_H',0xfed0:'First_Virtual_Screen',
    0xfed1:'Prev_Virtual_Screen',0xfed2:'Next_Virtual_Screen',0xfed4:'Last_Virtual_Screen',0xfed5:'Terminate_Server',0xfee0:'Pointer_Left',
    0xfee1:'Pointer_Right',0xfee2:'Pointer_Up',0xfee3:'Pointer_Down',0xfee4:'Pointer_UpLeft',0xfee5:'Pointer_UpRight',
    0xfee6:'Pointer_DownLeft',0xfee7:'Pointer_DownRight',0xfee8:'Pointer_Button_Dflt',0xfee9:'Pointer_Button1',0xfeea:'Pointer_Button2',
    0xfeeb:'Pointer_Button3',0xfeec:'Pointer_Button4',0xfeed:'Pointer_Button5',0xfeee:'Pointer_DblClick_Dflt',0xfeef:'Pointer_DblClick1',
    0xfef0:'Pointer_DblClick2',0xfef1:'Pointer_DblClick3',0xfef2:'Pointer_DblClick4',0xfef3:'Pointer_DblClick5',0xfef4:'Pointer_Drag_Dflt',
    0xfef5:'Pointer_Drag1',0xfef6:'Pointer_Drag2',0xfef7:'Pointer_Drag3',0xfef8:'Pointer_Drag4',0xfef9:'Pointer_EnableKeys',
    0xfefa:'Pointer_Accelerate',0xfefb:'Pointer_DfltBtnNext',0xfefc:'Pointer_DfltBtnPrev',0xfefd:'Pointer_Drag5',0xff08:'BackSpace',
    0xff09:'Tab',0xff0a:'Linefeed',0xff0b:'Clear',0xff0d:'Return',0xff13:'Pause',
    0xff14:'Scroll_Lock',0xff15:'Sys_Req',0xff1b:'Escape',0xff20:'Multi_key',0xff21:'Kanji',
    0xff22:'Muhenkan',0xff23:'Henkan_Mode',0xff24:'Romaji',0xff25:'Hiragana',0xff26:'Katakana',
    0xff27:'Hiragana_Katakana',0xff28:'Zenkaku',0xff29:'Hankaku',0xff2a:'Zenkaku_Hankaku',0xff2b:'Touroku',
    0xff2c:'Massyo',0xff2d:'Kana_Lock',0xff2e:'Kana_Shift',0xff2f:'Eisu_Shift',0xff30:'Eisu_toggle',
    0xff31:'Hangul',0xff32:'Hangul_Start',0xff33:'Hangul_End',0xff34:'Hangul_Hanja',0xff35:'Hangul_Jamo',
    0xff36:'Hangul_Romaja',0xff37:'Codeinput',0xff38:'Hangul_Jeonja',0xff39:'Hangul_Banja',0xff3a:'Hangul_PreHanja',
    0xff3b:'Hangul_PostHanja',0xff3c:'SingleCandidate',0xff3d:'MultipleCandidate',0xff3e:'PreviousCandidate',0xff3f:'Hangul_Special',
    0xff50:'Home',0xff51:'Left',0xff52:'Up',0xff53:'Right',0xff54:'Down',
    0xff55:'Prior',0xff56:'Next',0xff57:'End',0xff58:'Begin',0xff60:'Select',
    0xff61:'Print',0xff62:'Execute',0xff63:'Insert',0xff65:'Undo',0xff66:'Redo',
    0xff67:'Menu',0xff68:'Find',0xff69:'Cancel',0xff6a:'Help',0xff6b:'Break',
    0xff7e:'ISO_Group_Shift',0xff7f:'Num_Lock',0xff80:'KP_Space',0xff89:'KP_Tab',0xff8d:'KP_Enter',
    0xff91:'KP_F1',0xff92:'KP_F2',0xff93:'KP_F3',0xff94:'KP_F4',0xff95:'KP_Home',
    0xff96:'KP_Left',0xff97:'KP_Up',0xff98:'KP_Right',0xff99:'KP_Down',0xff9a:'KP_Prior',
    0xff9b:'KP_Next',0xff9c:'KP_End',0xff9d:'KP_Begin',0xff9e:'KP_Insert',0xff9f:'KP_Delete',
    0xffaa:'KP_Multiply',0xffab:'KP_Add',0xffac:'KP_Separator',0xffad:'KP_Subtract',0xffae:'KP_Decimal',
    0xffaf:'KP_Divide',0xffb0:'KP_0',0xffb1:'KP_1',0xffb2:'KP_2',0xffb3:'KP_3',
    0xffb4:'KP_4',0xffb5:'KP_5',0xffb6:'KP_6',0xffb7:'KP_7',0xffb8:'KP_8',
    0xffb9:'KP_9',0xffbd:'KP_Equal',0xffbe:'F1',0xffbf:'F2',0xffc0:'F3',
    0xffc1:'F4',0xffc2:'F5',0xffc3:'F6',0xffc4:'F7',0xffc5:'F8',
    0xffc6:'F9',0xffc7:'F10',0xffc8:'F11',0xffc9:'F12',0xffca:'F13',
    0xffcb:'F14',0xffcc:'F15',0xffcd:'F16',0xffce:'F17',0xffcf:'F18',
    0xffd0:'F19',0xffd1:'F20',0xffd2:'F21',0xffd3:'F22',0xffd4:'F23',
    0xffd5:'F24',0xffd6:'F25',0xffd7:'F26',0xffd8:'F27',0xffd9:'F28',
    0xffda:'F29',0xffdb:'F30',0xffdc:'F31',0xffdd:'F32',0xffde:'F33',
    0xffdf:'F34',0xffe0:'F35',0xffe1:'Shift_L',0xffe2:'Shift_R',0xffe3:'Control_L',
    0xffe4:'Control_R',0xffe5:'Caps_Lock',0xffe6:'Shift_Lock',0xffe7:'Meta_L',0xffe8:'Meta_R',
    0xffe9:'Alt_L',0xffea:'Alt_R',0xffeb:'Super_L',0xffec:'Super_R',0xffed:'Hyper_L',
    0xffee:'Hyper_R',0xfff1:'braille_dot_1',0xfff2:'braille_dot_2',0xfff3:'braille_dot_3',0xfff4:'braille_dot_4',
    0xfff5:'braille_dot_5',0xfff6:'braille_dot_6',0xfff7:'braille_dot_7',0xfff8:'braille_dot_8',0xfff9:'braille_dot_9',
    0xfffa:'braille_dot_10',0xffff:'Delete',0xffffff:'VoidSymbol',0x100012c:'Ibreve',0x100012d:'ibreve',
    0x1000174:'Wcircumflex',0x1000175:'wcircumflex',0x1000176:'Ycircumflex',0x1000177:'ycircumflex',0x100018f:'SCHWA',
    0x100019f:'Obarred',0x10001a0:'Ohorn',0x10001a1:'ohorn',0x10001af:'Uhorn',0x10001b0:'uhorn',
    0x10001b5:'Zstroke',0x10001b6:'zstroke',0x10001b7:'EZH',0x10001d1:'Ocaron',0x10001d2:'ocaron',
    0x10001e6:'Gcaron',0x10001e7:'gcaron',0x1000259:'schwa',0x1000275:'obarred',0x1000292:'ezh',
    0x1000300:'combining_grave',0x1000301:'combining_acute',0x1000303:'combining_tilde',0x1000309:'combining_hook',0x1000323:'combining_belowdot',
    0x1000492:'Cyrillic_GHE_bar',0x1000493:'Cyrillic_ghe_bar',0x1000496:'Cyrillic_ZHE_descender',0x1000497:'Cyrillic_zhe_descender',0x100049a:'Cyrillic_KA_descender',
    0x100049b:'Cyrillic_ka_descender',0x100049c:'Cyrillic_KA_vertstroke',0x100049d:'Cyrillic_ka_vertstroke',0x10004a2:'Cyrillic_EN_descender',0x10004a3:'Cyrillic_en_descender',
    0x10004ae:'Cyrillic_U_straight',0x10004af:'Cyrillic_u_straight',0x10004b0:'Cyrillic_U_straight_bar',0x10004b1:'Cyrillic_u_straight_bar',0x10004b2:'Cyrillic_HA_descender',
    0x10004b3:'Cyrillic_ha_descender',0x10004b6:'Cyrillic_CHE_descender',0x10004b7:'Cyrillic_che_descender',0x10004b8:'Cyrillic_CHE_vertstroke',0x10004b9:'Cyrillic_che_vertstroke',
    0x10004ba:'Cyrillic_SHHA',0x10004bb:'Cyrillic_shha',0x10004d8:'Cyrillic_SCHWA',0x10004d9:'Cyrillic_schwa',0x10004e2:'Cyrillic_I_macron',
    0x10004e3:'Cyrillic_i_macron',0x10004e8:'Cyrillic_O_bar',0x10004e9:'Cyrillic_o_bar',0x10004ee:'Cyrillic_U_macron',0x10004ef:'Cyrillic_u_macron',
    0x1000531:'Armenian_AYB',0x1000532:'Armenian_BEN',0x1000533:'Armenian_GIM',0x1000534:'Armenian_DA',0x1000535:'Armenian_YECH',
    0x1000536:'Armenian_ZA',0x1000537:'Armenian_E',0x1000538:'Armenian_AT',0x1000539:'Armenian_TO',0x100053a:'Armenian_ZHE',
    0x100053b:'Armenian_INI',0x100053c:'Armenian_LYUN',0x100053d:'Armenian_KHE',0x100053e:'Armenian_TSA',0x100053f:'Armenian_KEN',
    0x1000540:'Armenian_HO',0x1000541:'Armenian_DZA',0x1000542:'Armenian_GHAT',0x1000543:'Armenian_TCHE',0x1000544:'Armenian_MEN',
    0x1000545:'Armenian_HI',0x1000546:'Armenian_NU',0x1000547:'Armenian_SHA',0x1000548:'Armenian_VO',0x1000549:'Armenian_CHA',
    0x100054a:'Armenian_PE',0x100054b:'Armenian_JE',0x100054c:'Armenian_RA',0x100054d:'Armenian_SE',0x100054e:'Armenian_VEV',
    0x100054f:'Armenian_TYUN',0x1000550:'Armenian_RE',0x1000551:'Armenian_TSO',0x1000552:'Armenian_VYUN',0x1000553:'Armenian_PYUR',
    0x1000554:'Armenian_KE',0x1000555:'Armenian_O',0x1000556:'Armenian_FE',0x100055a:'Armenian_apostrophe',0x100055b:'Armenian_accent',
    0x100055c:'Armenian_exclam',0x100055d:'Armenian_separation_mark',0x100055e:'Armenian_question',0x1000561:'Armenian_ayb',0x1000562:'Armenian_ben',
    0x1000563:'Armenian_gim',0x1000564:'Armenian_da',0x1000565:'Armenian_yech',0x1000566:'Armenian_za',0x1000567:'Armenian_e',
    0x1000568:'Armenian_at',0x1000569:'Armenian_to',0x100056a:'Armenian_zhe',0x100056b:'Armenian_ini',0x100056c:'Armenian_lyun',
    0x100056d:'Armenian_khe',0x100056e:'Armenian_tsa',0x100056f:'Armenian_ken',0x1000570:'Armenian_ho',0x1000571:'Armenian_dza',
    0x1000572:'Armenian_ghat',0x1000573:'Armenian_tche',0x1000574:'Armenian_men',0x1000575:'Armenian_hi',0x1000576:'Armenian_nu',
    0x1000577:'Armenian_sha',0x1000578:'Armenian_vo',0x1000579:'Armenian_cha',0x100057a:'Armenian_pe',0x100057b:'Armenian_je',
    0x100057c:'Armenian_ra',0x100057d:'Armenian_se',0x100057e:'Armenian_vev',0x100057f:'Armenian_tyun',0x1000580:'Armenian_re',
    0x1000581:'Armenian_tso',0x1000582:'Armenian_vyun',0x1000583:'Armenian_pyur',0x1000584:'Armenian_ke',0x1000585:'Armenian_o',
    0x1000586:'Armenian_fe',0x1000587:'Armenian_ligature_ew',0x1000589:'Armenian_full_stop',0x100058a:'Armenian_hyphen',0x1000653:'Arabic_madda_above',
    0x1000654:'Arabic_hamza_above',0x1000655:'Arabic_hamza_below',0x1000660:'Arabic_0',0x1000661:'Arabic_1',0x1000662:'Arabic_2',
    0x1000663:'Arabic_3',0x1000664:'Arabic_4',0x1000665:'Arabic_5',0x1000666:'Arabic_6',0x1000667:'Arabic_7',
    0x1000668:'Arabic_8',0x1000669:'Arabic_9',0x100066a:'Arabic_percent',0x1000670:'Arabic_superscript_alef',0x1000679:'Arabic_tteh',
    0x100067e:'Arabic_peh',0x1000686:'Arabic_tcheh',0x1000688:'Arabic_ddal',0x1000691:'Arabic_rreh',0x1000698:'Arabic_jeh',
    0x10006a4:'Arabic_veh',0x10006a9:'Arabic_keheh',0x10006af:'Arabic_gaf',0x10006ba:'Arabic_noon_ghunna',0x10006be:'Arabic_heh_doachashmee',
    0x10006c1:'Arabic_heh_goal',0x10006cc:'Farsi_yeh',0x10006d2:'Arabic_yeh_baree',0x10006d4:'Arabic_fullstop',0x10006f0:'Farsi_0',
    0x10006f1:'Farsi_1',0x10006f2:'Farsi_2',0x10006f3:'Farsi_3',0x10006f4:'Farsi_4',0x10006f5:'Farsi_5',
    0x10006f6:'Farsi_6',0x10006f7:'Farsi_7',0x10006f8:'Farsi_8',0x10006f9:'Farsi_9',0x1000d82:'Sinh_ng',
    0x1000d83:'Sinh_h2',0x1000d85:'Sinh_a',0x1000d86:'Sinh_aa',0x1000d87:'Sinh_ae',0x1000d88:'Sinh_aee',
    0x1000d89:'Sinh_i',0x1000d8a:'Sinh_ii',0x1000d8b:'Sinh_u',0x1000d8c:'Sinh_uu',0x1000d8d:'Sinh_ri',
    0x1000d8e:'Sinh_rii',0x1000d8f:'Sinh_lu',0x1000d90:'Sinh_luu',0x1000d91:'Sinh_e',0x1000d92:'Sinh_ee',
    0x1000d93:'Sinh_ai',0x1000d94:'Sinh_o',0x1000d95:'Sinh_oo',0x1000d96:'Sinh_au',0x1000d9a:'Sinh_ka',
    0x1000d9b:'Sinh_kha',0x1000d9c:'Sinh_ga',0x1000d9d:'Sinh_gha',0x1000d9e:'Sinh_ng2',0x1000d9f:'Sinh_nga',
    0x1000da0:'Sinh_ca',0x1000da1:'Sinh_cha',0x1000da2:'Sinh_ja',0x1000da3:'Sinh_jha',0x1000da4:'Sinh_nya',
    0x1000da5:'Sinh_jnya',0x1000da6:'Sinh_nja',0x1000da7:'Sinh_tta',0x1000da8:'Sinh_ttha',0x1000da9:'Sinh_dda',
    0x1000daa:'Sinh_ddha',0x1000dab:'Sinh_nna',0x1000dac:'Sinh_ndda',0x1000dad:'Sinh_tha',0x1000dae:'Sinh_thha',
    0x1000daf:'Sinh_dha',0x1000db0:'Sinh_dhha',0x1000db1:'Sinh_na',0x1000db3:'Sinh_ndha',0x1000db4:'Sinh_pa',
    0x1000db5:'Sinh_pha',0x1000db6:'Sinh_ba',0x1000db7:'Sinh_bha',0x1000db8:'Sinh_ma',0x1000db9:'Sinh_mba',
    0x1000dba:'Sinh_ya',0x1000dbb:'Sinh_ra',0x1000dbd:'Sinh_la',0x1000dc0:'Sinh_va',0x1000dc1:'Sinh_sha',
    0x1000dc2:'Sinh_ssha',0x1000dc3:'Sinh_sa',0x1000dc4:'Sinh_ha',0x1000dc5:'Sinh_lla',0x1000dc6:'Sinh_fa',
    0x1000dca:'Sinh_al',0x1000dcf:'Sinh_aa2',0x1000dd0:'Sinh_ae2',0x1000dd1:'Sinh_aee2',0x1000dd2:'Sinh_i2',
    0x1000dd3:'Sinh_ii2',0x1000dd4:'Sinh_u2',0x1000dd6:'Sinh_uu2',0x1000dd8:'Sinh_ru2',0x1000dd9:'Sinh_e2',
    0x1000dda:'Sinh_ee2',0x1000ddb:'Sinh_ai2',0x1000ddc:'Sinh_o2',0x1000ddd:'Sinh_oo2',0x1000dde:'Sinh_au2',
    0x1000ddf:'Sinh_lu2',0x1000df2:'Sinh_ruu2',0x1000df3:'Sinh_luu2',0x1000df4:'Sinh_kunddaliya',0x10010d0:'Georgian_an',
    0x10010d1:'Georgian_ban',0x10010d2:'Georgian_gan',0x10010d3:'Georgian_don',0x10010d4:'Georgian_en',0x10010d5:'Georgian_vin',
    0x10010d6:'Georgian_zen',0x10010d7:'Georgian_tan',0x10010d8:'Georgian_in',0x10010d9:'Georgian_kan',0x10010da:'Georgian_las',
    0x10010db:'Georgian_man',0x10010dc:'Georgian_nar',0x10010dd:'Georgian_on',0x10010de:'Georgian_par',0x10010df:'Georgian_zhar',
    0x10010e0:'Georgian_rae',0x10010e1:'Georgian_san',0x10010e2:'Georgian_tar',0x10010e3:'Georgian_un',0x10010e4:'Georgian_phar',
    0x10010e5:'Georgian_khar',0x10010e6:'Georgian_ghan',0x10010e7:'Georgian_qar',0x10010e8:'Georgian_shin',0x10010e9:'Georgian_chin',
    0x10010ea:'Georgian_can',0x10010eb:'Georgian_jil',0x10010ec:'Georgian_cil',0x10010ed:'Georgian_char',0x10010ee:'Georgian_xan',
    0x10010ef:'Georgian_jhan',0x10010f0:'Georgian_hae',0x10010f1:'Georgian_he',0x10010f2:'Georgian_hie',0x10010f3:'Georgian_we',
    0x10010f4:'Georgian_har',0x10010f5:'Georgian_hoe',0x10010f6:'Georgian_fi',0x1001e02:'Babovedot',0x1001e03:'babovedot',
    0x1001e0a:'Dabovedot',0x1001e0b:'dabovedot',0x1001e1e:'Fabovedot',0x1001e1f:'fabovedot',0x1001e36:'Lbelowdot',
    0x1001e37:'lbelowdot',0x1001e40:'Mabovedot',0x1001e41:'mabovedot',0x1001e56:'Pabovedot',0x1001e57:'pabovedot',
    0x1001e60:'Sabovedot',0x1001e61:'sabovedot',0x1001e6a:'Tabovedot',0x1001e6b:'tabovedot',0x1001e80:'Wgrave',
    0x1001e81:'wgrave',0x1001e82:'Wacute',0x1001e83:'wacute',0x1001e84:'Wdiaeresis',0x1001e85:'wdiaeresis',
    0x1001e8a:'Xabovedot',0x1001e8b:'xabovedot',0x1001e9e:'SSHARP',0x1001ea0:'Abelowdot',0x1001ea1:'abelowdot',
    0x1001ea2:'Ahook',0x1001ea3:'ahook',0x1001ea4:'Acircumflexacute',0x1001ea5:'acircumflexacute',0x1001ea6:'Acircumflexgrave',
    0x1001ea7:'acircumflexgrave',0x1001ea8:'Acircumflexhook',0x1001ea9:'acircumflexhook',0x1001eaa:'Acircumflextilde',0x1001eab:'acircumflextilde',
    0x1001eac:'Acircumflexbelowdot',0x1001ead:'acircumflexbelowdot',0x1001eae:'Abreveacute',0x1001eaf:'abreveacute',0x1001eb0:'Abrevegrave',
    0x1001eb1:'abrevegrave',0x1001eb2:'Abrevehook',0x1001eb3:'abrevehook',0x1001eb4:'Abrevetilde',0x1001eb5:'abrevetilde',
    0x1001eb6:'Abrevebelowdot',0x1001eb7:'abrevebelowdot',0x1001eb8:'Ebelowdot',0x1001eb9:'ebelowdot',0x1001eba:'Ehook',
    0x1001ebb:'ehook',0x1001ebc:'Etilde',0x1001ebd:'etilde',0x1001ebe:'Ecircumflexacute',0x1001ebf:'ecircumflexacute',
    0x1001ec0:'Ecircumflexgrave',0x1001ec1:'ecircumflexgrave',0x1001ec2:'Ecircumflexhook',0x1001ec3:'ecircumflexhook',0x1001ec4:'Ecircumflextilde',
    0x1001ec5:'ecircumflextilde',0x1001ec6:'Ecircumflexbelowdot',0x1001ec7:'ecircumflexbelowdot',0x1001ec8:'Ihook',0x1001ec9:'ihook',
    0x1001eca:'Ibelowdot',0x1001ecb:'ibelowdot',0x1001ecc:'Obelowdot',0x1001ecd:'obelowdot',0x1001ece:'Ohook',
    0x1001ecf:'ohook',0x1001ed0:'Ocircumflexacute',0x1001ed1:'ocircumflexacute',0x1001ed2:'Ocircumflexgrave',0x1001ed3:'ocircumflexgrave',
    0x1001ed4:'Ocircumflexhook',0x1001ed5:'ocircumflexhook',0x1001ed6:'Ocircumflextilde',0x1001ed7:'ocircumflextilde',0x1001ed8:'Ocircumflexbelowdot',
    0x1001ed9:'ocircumflexbelowdot',0x1001eda:'Ohornacute',0x1001edb:'ohornacute',0x1001edc:'Ohorngrave',0x1001edd:'ohorngrave',
    0x1001ede:'Ohornhook',0x1001edf:'ohornhook',0x1001ee0:'Ohorntilde',0x1001ee1:'ohorntilde',0x1001ee2:'Ohornbelowdot',
    0x1001ee3:'ohornbelowdot',0x1001ee4:'Ubelowdot',0x1001ee5:'ubelowdot',0x1001ee6:'Uhook',0x1001ee7:'uhook',
    0x1001ee8:'Uhornacute',0x1001ee9:'uhornacute',0x1001eea:'Uhorngrave',0x1001eeb:'uhorngrave',0x1001eec:'Uhornhook',
    0x1001eed:'uhornhook',0x1001eee:'Uhorntilde',0x1001eef:'uhorntilde',0x1001ef0:'Uhornbelowdot',0x1001ef1:'uhornbelowdot',
    0x1001ef2:'Ygrave',0x1001ef3:'ygrave',0x1001ef4:'Ybelowdot',0x1001ef5:'ybelowdot',0x1001ef6:'Yhook',
    0x1001ef7:'yhook',0x1001ef8:'Ytilde',0x1001ef9:'ytilde',0x1002039:'leftsingleanglequotemark',0x100203a:'rightsingleanglequotemark',
    0x1002070:'zerosuperior',0x1002074:'foursuperior',0x1002075:'fivesuperior',0x1002076:'sixsuperior',0x1002077:'sevensuperior',
    0x1002078:'eightsuperior',0x1002079:'ninesuperior',0x1002080:'zerosubscript',0x1002081:'onesubscript',0x1002082:'twosubscript',
    0x1002083:'threesubscript',0x1002084:'foursubscript',0x1002085:'fivesubscript',0x1002086:'sixsubscript',0x1002087:'sevensubscript',
    0x1002088:'eightsubscript',0x1002089:'ninesubscript',0x10020a0:'EcuSign',0x10020a1:'ColonSign',0x10020a2:'CruzeiroSign',
    0x10020a3:'FFrancSign',0x10020a4:'LiraSign',0x10020a5:'MillSign',0x10020a6:'NairaSign',0x10020a7:'PesetaSign',
    0x10020a8:'RupeeSign',0x10020a9:'WonSign',0x10020aa:'NewSheqelSign',0x10020ab:'DongSign',0x1002202:'partdifferential',
    0x1002205:'emptyset',0x1002208:'elementof',0x1002209:'notelementof',0x100220b:'containsas',0x100221a:'squareroot',
    0x100221b:'cuberoot',0x100221c:'fourthroot',0x100222c:'dintegral',0x100222d:'tintegral',0x1002235:'because',
    0x1002247:'notapproxeq',0x1002248:'approxeq',0x1002262:'notidentical',0x1002263:'stricteq',0x1002800:'braille_blank',
    0x1002801:'braille_dots_1',0x1002802:'braille_dots_2',0x1002803:'braille_dots_12',0x1002804:'braille_dots_3',0x1002805:'braille_dots_13',
    0x1002806:'braille_dots_23',0x1002807:'braille_dots_123',0x1002808:'braille_dots_4',0x1002809:'braille_dots_14',0x100280a:'braille_dots_24',
    0x100280b:'braille_dots_124',0x100280c:'braille_dots_34',0x100280d:'braille_dots_134',0x100280e:'braille_dots_234',0x100280f:'braille_dots_1234',
    0x1002810:'braille_dots_5',0x1002811:'braille_dots_15',0x1002812:'braille_dots_25',0x1002813:'braille_dots_125',0x1002814:'braille_dots_35',
    0x1002815:'braille_dots_135',0x1002816:'braille_dots_235',0x1002817:'braille_dots_1235',0x1002818:'braille_dots_45',0x1002819:'braille_dots_145',
    0x100281a:'braille_dots_245',0x100281b:'braille_dots_1245',0x100281c:'braille_dots_345',0x100281d:'braille_dots_1345',0x100281e:'braille_dots_2345',
    0x100281f:'braille_dots_12345',0x1002820:'braille_dots_6',0x1002821:'braille_dots_16',0x1002822:'braille_dots_26',0x1002823:'braille_dots_126',
    0x1002824:'braille_dots_36',0x1002825:'braille_dots_136',0x1002826:'braille_dots_236',0x1002827:'braille_dots_1236',0x1002828:'braille_dots_46',
    0x1002829:'braille_dots_146',0x100282a:'braille_dots_246',0x100282b:'braille_dots_1246',0x100282c:'braille_dots_346',0x100282d:'braille_dots_1346',
    0x100282e:'braille_dots_2346',0x100282f:'braille_dots_12346',0x1002830:'braille_dots_56',0x1002831:'braille_dots_156',0x1002832:'braille_dots_256',
    0x1002833:'braille_dots_1256',0x1002834:'braille_dots_356',0x1002835:'braille_dots_1356',0x1002836:'braille_dots_2356',0x1002837:'braille_dots_12356',
    0x1002838:'braille_dots_456',0x1002839:'braille_dots_1456',0x100283a:'braille_dots_2456',0x100283b:'braille_dots_12456',0x100283c:'braille_dots_3456',
    0x100283d:'braille_dots_13456',0x100283e:'braille_dots_23456',0x100283f:'braille_dots_123456',0x1002840:'braille_dots_7',0x1002841:'braille_dots_17',
    0x1002842:'braille_dots_27',0x1002843:'braille_dots_127',0x1002844:'braille_dots_37',0x1002845:'braille_dots_137',0x1002846:'braille_dots_237',
    0x1002847:'braille_dots_1237',0x1002848:'braille_dots_47',0x1002849:'braille_dots_147',0x100284a:'braille_dots_247',0x100284b:'braille_dots_1247',
    0x100284c:'braille_dots_347',0x100284d:'braille_dots_1347',0x100284e:'braille_dots_2347',0x100284f:'braille_dots_12347',0x1002850:'braille_dots_57',
    0x1002851:'braille_dots_157',0x1002852:'braille_dots_257',0x1002853:'braille_dots_1257',0x1002854:'braille_dots_357',0x1002855:'braille_dots_1357',
    0x1002856:'braille_dots_2357',0x1002857:'braille_dots_12357',0x1002858:'braille_dots_457',0x1002859:'braille_dots_1457',0x100285a:'braille_dots_2457',
    0x100285b:'braille_dots_12457',0x100285c:'braille_dots_3457',0x100285d:'braille_dots_13457',0x100285e:'braille_dots_23457',0x100285f:'braille_dots_123457',
    0x1002860:'braille_dots_67',0x1002861:'braille_dots_167',0x1002862:'braille_dots_267',0x1002863:'braille_dots_1267',0x1002864:'braille_dots_367',
    0x1002865:'braille_dots_1367',0x1002866:'braille_dots_2367',0x1002867:'braille_dots_12367',0x1002868:'braille_dots_467',0x1002869:'braille_dots_1467',
    0x100286a:'braille_dots_2467',0x100286b:'braille_dots_12467',0x100286c:'braille_dots_3467',0x100286d:'braille_dots_13467',0x100286e:'braille_dots_23467',
    0x100286f:'braille_dots_123467',0x1002870:'braille_dots_567',0x1002871:'braille_dots_1567',0x1002872:'braille_dots_2567',0x1002873:'braille_dots_12567',
    0x1002874:'braille_dots_3567',0x1002875:'braille_dots_13567',0x1002876:'braille_dots_23567',0x1002877:'braille_dots_123567',0x1002878:'braille_dots_4567',
    0x1002879:'braille_dots_14567',0x100287a:'braille_dots_24567',0x100287b:'braille_dots_124567',0x100287c:'braille_dots_34567',0x100287d:'braille_dots_134567',
    0x100287e:'braille_dots_234567',0x100287f:'braille_dots_1234567',0x1002880:'braille_dots_8',0x1002881:'braille_dots_18',0x1002882:'braille_dots_28',
    0x1002883:'braille_dots_128',0x1002884:'braille_dots_38',0x1002885:'braille_dots_138',0x1002886:'braille_dots_238',0x1002887:'braille_dots_1238',
    0x1002888:'braille_dots_48',0x1002889:'braille_dots_148',0x100288a:'braille_dots_248',0x100288b:'braille_dots_1248',0x100288c:'braille_dots_348',
    0x100288d:'braille_dots_1348',0x100288e:'braille_dots_2348',0x100288f:'braille_dots_12348',0x1002890:'braille_dots_58',0x1002891:'braille_dots_158',
    0x1002892:'braille_dots_258',0x1002893:'braille_dots_1258',0x1002894:'braille_dots_358',0x1002895:'braille_dots_1358',0x1002896:'braille_dots_2358',
    0x1002897:'braille_dots_12358',0x1002898:'braille_dots_458',0x1002899:'braille_dots_1458',0x100289a:'braille_dots_2458',0x100289b:'braille_dots_12458',
    0x100289c:'braille_dots_3458',0x100289d:'braille_dots_13458',0x100289e:'braille_dots_23458',0x100289f:'braille_dots_123458',0x10028a0:'braille_dots_68',
    0x10028a1:'braille_dots_168',0x10028a2:'braille_dots_268',0x10028a3:'braille_dots_1268',0x10028a4:'braille_dots_368',0x10028a5:'braille_dots_1368',
    0x10028a6:'braille_dots_2368',0x10028a7:'braille_dots_12368',0x10028a8:'braille_dots_468',0x10028a9:'braille_dots_1468',0x10028aa:'braille_dots_2468',
    0x10028ab:'braille_dots_12468',0x10028ac:'braille_dots_3468',0x10028ad:'braille_dots_13468',0x10028ae:'braille_dots_23468',0x10028af:'braille_dots_123468',
    0x10028b0:'braille_dots_568',0x10028b1:'braille_dots_1568',0x10028b2:'braille_dots_2568',0x10028b3:'braille_dots_12568',0x10028b4:'braille_dots_3568',
    0x10028b5:'braille_dots_13568',0x10028b6:'braille_dots_23568',0x10028b7:'braille_dots_123568',0x10028b8:'braille_dots_4568',0x10028b9:'braille_dots_14568',
    0x10028ba:'braille_dots_24568',0x10028bb:'braille_dots_124568',0x10028bc:'braille_dots_34568',0x10028bd:'braille_dots_134568',0x10028be:'braille_dots_234568',
    0x10028bf:'braille_dots_1234568',0x10028c0:'braille_dots_78',0x10028c1:'braille_dots_178',0x10028c2:'braille_dots_278',0x10028c3:'braille_dots_1278',
    0x10028c4:'braille_dots_378',0x10028c5:'braille_dots_1378',0x10028c6:'braille_dots_2378',0x10028c7:'braille_dots_12378',0x10028c8:'braille_dots_478',
    0x10028c9:'braille_dots_1478',0x10028ca:'braille_dots_2478',0x10028cb:'braille_dots_12478',0x10028cc:'braille_dots_3478',0x10028cd:'braille_dots_13478',
    0x10028ce:'braille_dots_23478',0x10028cf:'braille_dots_123478',0x10028d0:'braille_dots_578',0x10028d1:'braille_dots_1578',0x10028d2:'braille_dots_2578',
    0x10028d3:'braille_dots_12578',0x10028d4:'braille_dots_3578',0x10028d5:'braille_dots_13578',0x10028d6:'braille_dots_23578',0x10028d7:'braille_dots_123578',
    0x10028d8:'braille_dots_4578',0x10028d9:'braille_dots_14578',0x10028da:'braille_dots_24578',0x10028db:'braille_dots_124578',0x10028dc:'braille_dots_34578',
    0x10028dd:'braille_dots_134578',0x10028de:'braille_dots_234578',0x10028df:'braille_dots_1234578',0x10028e0:'braille_dots_678',0x10028e1:'braille_dots_1678',
    0x10028e2:'braille_dots_2678',0x10028e3:'braille_dots_12678',0x10028e4:'braille_dots_3678',0x10028e5:'braille_dots_13678',0x10028e6:'braille_dots_23678',
    0x10028e7:'braille_dots_123678',0x10028e8:'braille_dots_4678',0x10028e9:'braille_dots_14678',0x10028ea:'braille_dots_24678',0x10028eb:'braille_dots_124678',
    0x10028ec:'braille_dots_34678',0x10028ed:'braille_dots_134678',0x10028ee:'braille_dots_234678',0x10028ef:'braille_dots_1234678',0x10028f0:'braille_dots_5678',
    0x10028f1:'braille_dots_15678',0x10028f2:'braille_dots_25678',0x10028f3:'braille_dots_125678',0x10028f4:'braille_dots_35678',0x10028f5:'braille_dots_135678',
    0x10028f6:'braille_dots_235678',0x10028f7:'braille_dots_1235678',0x10028f8:'braille_dots_45678',0x10028f9:'braille_dots_145678',0x10028fa:'braille_dots_245678',
    0x10028fb:'braille_dots_1245678',0x10028fc:'braille_dots_345678',0x10028fd:'braille_dots_1345678',0x10028fe:'braille_dots_2345678',0x10028ff:'braille_dots_12345678',
    0x100000a8:'hpmute_acute',0x100000a9:'hpmute_grave',0x100000aa:'hpmute_asciicircum',0x100000ab:'hpmute_diaeresis',0x100000ac:'hpmute_asciitilde',
    0x100000af:'hplira',0x100000be:'hpguilder',0x100000ee:'hpYdiaeresis',0x100000f6:'hplongminus',0x100000fc:'hpblock',
    0x1000fe22:'Ddiaeresis',0x1000fe27:'Dacute_accent',0x1000fe2c:'Dcedilla_accent',0x1000fe5e:'Dcircumflex_accent',0x1000fe60:'Dgrave_accent',
    0x1000fe7e:'Dtilde',0x1000feb0:'Dring_accent',0x1000ff00:'DRemove',0x1000ff48:'hpModelock1',0x1000ff49:'hpModelock2',
    0x1000ff6c:'hpReset',0x1000ff6d:'hpSystem',0x1000ff6e:'hpUser',0x1000ff6f:'hpClearLine',0x1000ff70:'hpInsertLine',
    0x1000ff71:'hpDeleteLine',0x1000ff72:'hpInsertChar',0x1000ff73:'hpDeleteChar',0x1000ff74:'hpBackTab',0x1000ff75:'hpKP_BackTab',
    0x1000ff76:'Ext16bit_L',0x1000ff77:'Ext16bit_R',0x1004ff02:'osfCopy',0x1004ff03:'osfCut',0x1004ff04:'osfPaste',
    0x1004ff07:'osfBackTab',0x1004ff08:'osfBackSpace',0x1004ff0b:'osfClear',0x1004ff1b:'osfEscape',0x1004ff31:'osfAddMode',
    0x1004ff32:'osfPrimaryPaste',0x1004ff33:'osfQuickPaste',0x1004ff40:'osfPageLeft',0x1004ff41:'osfPageUp',0x1004ff42:'osfPageDown',
    0x1004ff43:'osfPageRight',0x1004ff44:'osfActivate',0x1004ff45:'osfMenuBar',0x1004ff51:'osfLeft',0x1004ff52:'osfUp',
    0x1004ff53:'osfRight',0x1004ff54:'osfDown',0x1004ff57:'osfEndLine',0x1004ff58:'osfBeginLine',0x1004ff59:'osfEndData',
    0x1004ff5a:'osfBeginData',0x1004ff5b:'osfPrevMenu',0x1004ff5c:'osfNextMenu',0x1004ff5d:'osfPrevField',0x1004ff5e:'osfNextField',
    0x1004ff60:'osfSelect',0x1004ff63:'osfInsert',0x1004ff65:'osfUndo',0x1004ff67:'osfMenu',0x1004ff69:'osfCancel',
    0x1004ff6a:'osfHelp',0x1004ff71:'osfSelectAll',0x1004ff72:'osfDeselectAll',0x1004ff73:'osfReselect',0x1004ff74:'osfExtend',
    0x1004ff78:'osfRestore',0x1004ffff:'osfDelete',0x1005ff00:'SunFA_Grave',0x1005ff01:'SunFA_Circum',0x1005ff02:'SunFA_Tilde',
    0x1005ff03:'SunFA_Acute',0x1005ff04:'SunFA_Diaeresis',0x1005ff05:'SunFA_Cedilla',0x1005ff10:'SunF36',0x1005ff11:'SunF37',
    0x1005ff60:'SunSys_Req',0x1005ff70:'SunProps',0x1005ff71:'SunFront',0x1005ff72:'SunCopy',0x1005ff73:'SunOpen',
    0x1005ff74:'SunPaste',0x1005ff75:'SunCut',0x1005ff76:'SunPowerSwitch',0x1005ff77:'SunAudioLowerVolume',0x1005ff78:'SunAudioMute',
    0x1005ff79:'SunAudioRaiseVolume',0x1005ff7a:'SunVideoDegauss',0x1005ff7b:'SunVideoLowerBrightness',0x1005ff7c:'SunVideoRaiseBrightness',0x1005ff7d:'SunPowerSwitchShift',
    0x100810a4:'XF86MediaPlayPause',0x100810ae:'XF86Exit',0x100810d1:'XF86AudioBassBoost',0x100810dc:'XF86Sport',0x100810f4:'XF86BrightnessAuto',
    0x100810f5:'XF86DisplayOff',0x10081160:'XF86OK',0x10081162:'XF86GoTo',0x10081166:'XF86Info',0x10081168:'XF86VendorLogo',
    0x1008116a:'XF86MediaSelectProgramGuide',0x1008116e:'XF86MediaSelectHome',0x10081170:'XF86MediaLanguageMenu',0x10081171:'XF86MediaTitleMenu',0x10081175:'XF86AudioChannelMode',
    0x10081177:'XF86AspectRatio',0x10081178:'XF86MediaSelectPC',0x10081179:'XF86MediaSelectTV',0x1008117a:'XF86MediaSelectCable',0x1008117b:'XF86MediaSelectVCR',
    0x1008117c:'XF86MediaSelectVCRPlus',0x1008117d:'XF86MediaSelectSatellite',0x10081180:'XF86MediaSelectTape',0x10081181:'XF86MediaSelectRadio',0x10081182:'XF86MediaSelectTuner',
    0x10081183:'XF86MediaPlayer',0x10081184:'XF86MediaSelectTeletext',0x10081185:'XF86DVD',0x10081186:'XF86MediaSelectAuxiliary',0x10081188:'XF86Audio',
    0x10081192:'XF86ChannelUp',0x10081193:'XF86ChannelDown',0x10081199:'XF86MediaPlaySlow',0x1008119b:'XF86Break',0x1008119d:'XF86NumberEntryMode',
    0x100811a0:'XF86VideoPhone',0x100811a4:'XF86ZoomReset',0x100811a6:'XF86Editor',0x100811a8:'XF86GraphicsEditor',0x100811a9:'XF86Presentation',
    0x100811aa:'XF86Database',0x100811ac:'XF86Voicemail',0x100811ad:'XF86Addressbook',0x100811af:'XF86DisplayToggle',0x100811b0:'XF86SpellCheck',
    0x100811b6:'XF86ContextMenu',0x100811b7:'XF86MediaRepeat',0x100811b8:'XF8610ChannelsUp',0x100811b9:'XF8610ChannelsDown',0x100811ba:'XF86Images',
    0x100811bc:'XF86NotificationCenter',0x100811bd:'XF86PickupPhone',0x100811be:'XF86HangupPhone',0x100811bf:'XF86LinkPhone',0x100811d0:'XF86Fn',
    0x100811d1:'XF86Fn_Esc',0x100811d2:'XF86Fn_F1',0x100811d3:'XF86Fn_F2',0x100811d4:'XF86Fn_F3',0x100811d5:'XF86Fn_F4',
    0x100811d6:'XF86Fn_F5',0x100811d7:'XF86Fn_F6',0x100811d8:'XF86Fn_F7',0x100811d9:'XF86Fn_F8',0x100811da:'XF86Fn_F9',
    0x100811db:'XF86Fn_F10',0x100811dc:'XF86Fn_F11',0x100811dd:'XF86Fn_F12',0x100811de:'XF86Fn_1',0x100811df:'XF86Fn_2',
    0x100811e0:'XF86Fn_D',0x100811e1:'XF86Fn_E',0x100811e2:'XF86Fn_F',0x100811e3:'XF86Fn_S',0x100811e4:'XF86Fn_B',
    0x100811e5:'XF86FnRightShift',0x10081200:'XF86Numeric0',0x10081201:'XF86Numeric1',0x10081202:'XF86Numeric2',0x10081203:'XF86Numeric3',
    0x10081204:'XF86Numeric4',0x10081205:'XF86Numeric5',0x10081206:'XF86Numeric6',0x10081207:'XF86Numeric7',0x10081208:'XF86Numeric8',
    0x10081209:'XF86Numeric9',0x1008120a:'XF86NumericStar',0x1008120b:'XF86NumericPound',0x1008120c:'XF86NumericA',0x1008120d:'XF86NumericB',
    0x1008120e:'XF86NumericC',0x1008120f:'XF86NumericD',0x10081210:'XF86CameraFocus',0x10081211:'XF86WPSButton',0x10081215:'XF86CameraZoomIn',
    0x10081216:'XF86CameraZoomOut',0x10081217:'XF86CameraUp',0x10081218:'XF86CameraDown',0x10081219:'XF86CameraLeft',0x1008121a:'XF86CameraRight',
    0x1008121b:'XF86AttendantOn',0x1008121c:'XF86AttendantOff',0x1008121d:'XF86AttendantToggle',0x1008121e:'XF86LightsToggle',0x10081230:'XF86ALSToggle',
    0x10081232:'XF86RefreshRateToggle',0x10081240:'XF86Buttonconfig',0x10081241:'XF86Taskmanager',0x10081242:'XF86Journal',0x10081243:'XF86ControlPanel',
    0x10081244:'XF86AppSelect',0x10081245:'XF86Screensaver',0x10081246:'XF86VoiceCommand',0x10081247:'XF86Assistant',0x10081249:'XF86EmojiPicker',
    0x1008124a:'XF86Dictate',0x1008124b:'XF86CameraAccessEnable',0x1008124c:'XF86CameraAccessDisable',0x1008124d:'XF86CameraAccessToggle',0x1008124e:'XF86Accessibility',
    0x1008124f:'XF86DoNotDisturb',0x10081250:'XF86BrightnessMin',0x10081251:'XF86BrightnessMax',0x10081252:'XF86ElectronicPrivacyScreenOn',0x10081253:'XF86ElectronicPrivacyScreenOff',
    0x10081254:'XF86ActionOnSelection',0x10081255:'XF86ContextualInsert',0x10081256:'XF86ContextualQuery',0x10081260:'XF86KbdInputAssistPrev',0x10081261:'XF86KbdInputAssistNext',
    0x10081262:'XF86KbdInputAssistPrevgroup',0x10081263:'XF86KbdInputAssistNextgroup',0x10081264:'XF86KbdInputAssistAccept',0x10081265:'XF86KbdInputAssistCancel',0x10081266:'XF86RightUp',
    0x10081267:'XF86RightDown',0x10081268:'XF86LeftUp',0x10081269:'XF86LeftDown',0x1008126a:'XF86RootMenu',0x1008126b:'XF86MediaTopMenu',
    0x1008126c:'XF86Numeric11',0x1008126d:'XF86Numeric12',0x1008126e:'XF86AudioDesc',0x1008126f:'XF863DMode',0x10081270:'XF86NextFavorite',
    0x10081271:'XF86StopRecord',0x10081272:'XF86PauseRecord',0x10081273:'XF86VOD',0x10081274:'XF86Unmute',0x10081275:'XF86FastReverse',
    0x10081276:'XF86SlowReverse',0x10081277:'XF86Data',0x10081278:'XF86OnScreenKeyboard',0x10081279:'XF86PrivacyScreenToggle',0x1008127a:'XF86SelectiveScreenshot',
    0x1008127b:'XF86NextElement',0x1008127c:'XF86PreviousElement',0x1008127d:'XF86AutopilotEngageToggle',0x1008127e:'XF86MarkWaypoint',0x1008127f:'XF86Sos',
    0x10081280:'XF86NavChart',0x10081281:'XF86FishingChart',0x10081282:'XF86SingleRangeRadar',0x10081283:'XF86DualRangeRadar',0x10081284:'XF86RadarOverlay',
    0x10081285:'XF86TraditionalSonar',0x10081286:'XF86ClearvuSonar',0x10081287:'XF86SidevuSonar',0x10081288:'XF86NavInfo',0x10081290:'XF86Macro1',
    0x10081291:'XF86Macro2',0x10081292:'XF86Macro3',0x10081293:'XF86Macro4',0x10081294:'XF86Macro5',0x10081295:'XF86Macro6',
    0x10081296:'XF86Macro7',0x10081297:'XF86Macro8',0x10081298:'XF86Macro9',0x10081299:'XF86Macro10',0x1008129a:'XF86Macro11',
    0x1008129b:'XF86Macro12',0x1008129c:'XF86Macro13',0x1008129d:'XF86Macro14',0x1008129e:'XF86Macro15',0x1008129f:'XF86Macro16',
    0x100812a0:'XF86Macro17',0x100812a1:'XF86Macro18',0x100812a2:'XF86Macro19',0x100812a3:'XF86Macro20',0x100812a4:'XF86Macro21',
    0x100812a5:'XF86Macro22',0x100812a6:'XF86Macro23',0x100812a7:'XF86Macro24',0x100812a8:'XF86Macro25',0x100812a9:'XF86Macro26',
    0x100812aa:'XF86Macro27',0x100812ab:'XF86Macro28',0x100812ac:'XF86Macro29',0x100812ad:'XF86Macro30',0x100812b0:'XF86MacroRecordStart',
    0x100812b1:'XF86MacroRecordStop',0x100812b2:'XF86MacroPresetCycle',0x100812b3:'XF86MacroPreset1',0x100812b4:'XF86MacroPreset2',0x100812b5:'XF86MacroPreset3',
    0x100812b8:'XF86KbdLcdMenu1',0x100812b9:'XF86KbdLcdMenu2',0x100812ba:'XF86KbdLcdMenu3',0x100812bb:'XF86KbdLcdMenu4',0x100812bc:'XF86KbdLcdMenu5',
    0x100812bd:'XF86PerformanceMode',0x1008fe01:'XF86Switch_VT_1',0x1008fe02:'XF86Switch_VT_2',0x1008fe03:'XF86Switch_VT_3',0x1008fe04:'XF86Switch_VT_4',
    0x1008fe05:'XF86Switch_VT_5',0x1008fe06:'XF86Switch_VT_6',0x1008fe07:'XF86Switch_VT_7',0x1008fe08:'XF86Switch_VT_8',0x1008fe09:'XF86Switch_VT_9',
    0x1008fe0a:'XF86Switch_VT_10',0x1008fe0b:'XF86Switch_VT_11',0x1008fe0c:'XF86Switch_VT_12',0x1008fe20:'XF86Ungrab',0x1008fe21:'XF86ClearGrab',
    0x1008fe22:'XF86Next_VMode',0x1008fe23:'XF86Prev_VMode',0x1008fe24:'XF86LogWindowTree',0x1008fe25:'XF86LogGrabInfo',0x1008ff01:'XF86ModeLock',
    0x1008ff02:'XF86MonBrightnessUp',0x1008ff03:'XF86MonBrightnessDown',0x1008ff04:'XF86KbdLightOnOff',0x1008ff05:'XF86KbdBrightnessUp',0x1008ff06:'XF86KbdBrightnessDown',
    0x1008ff07:'XF86MonBrightnessCycle',0x1008ff10:'XF86Standby',0x1008ff11:'XF86AudioLowerVolume',0x1008ff12:'XF86AudioMute',0x1008ff13:'XF86AudioRaiseVolume',
    0x1008ff14:'XF86AudioPlay',0x1008ff15:'XF86AudioStop',0x1008ff16:'XF86AudioPrev',0x1008ff17:'XF86AudioNext',0x1008ff18:'XF86HomePage',
    0x1008ff19:'XF86Mail',0x1008ff1a:'XF86Start',0x1008ff1b:'XF86Search',0x1008ff1c:'XF86AudioRecord',0x1008ff1d:'XF86Calculator',
    0x1008ff1e:'XF86Memo',0x1008ff1f:'XF86ToDoList',0x1008ff20:'XF86Calendar',0x1008ff21:'XF86PowerDown',0x1008ff22:'XF86ContrastAdjust',
    0x1008ff23:'XF86RockerUp',0x1008ff24:'XF86RockerDown',0x1008ff25:'XF86RockerEnter',0x1008ff26:'XF86Back',0x1008ff27:'XF86Forward',
    0x1008ff28:'XF86Stop',0x1008ff29:'XF86Refresh',0x1008ff2a:'XF86PowerOff',0x1008ff2b:'XF86WakeUp',0x1008ff2c:'XF86Eject',
    0x1008ff2d:'XF86ScreenSaver',0x1008ff2e:'XF86WWW',0x1008ff2f:'XF86Sleep',0x1008ff30:'XF86Favorites',0x1008ff31:'XF86AudioPause',
    0x1008ff32:'XF86AudioMedia',0x1008ff33:'XF86MyComputer',0x1008ff34:'XF86VendorHome',0x1008ff35:'XF86LightBulb',0x1008ff36:'XF86Shop',
    0x1008ff37:'XF86History',0x1008ff38:'XF86OpenURL',0x1008ff39:'XF86AddFavorite',0x1008ff3a:'XF86HotLinks',0x1008ff3b:'XF86BrightnessAdjust',
    0x1008ff3c:'XF86Finance',0x1008ff3d:'XF86Community',0x1008ff3e:'XF86AudioRewind',0x1008ff3f:'XF86BackForward',0x1008ff40:'XF86Launch0',
    0x1008ff41:'XF86Launch1',0x1008ff42:'XF86Launch2',0x1008ff43:'XF86Launch3',0x1008ff44:'XF86Launch4',0x1008ff45:'XF86Launch5',
    0x1008ff46:'XF86Launch6',0x1008ff47:'XF86Launch7',0x1008ff48:'XF86Launch8',0x1008ff49:'XF86Launch9',0x1008ff4a:'XF86LaunchA',
    0x1008ff4b:'XF86LaunchB',0x1008ff4c:'XF86LaunchC',0x1008ff4d:'XF86LaunchD',0x1008ff4e:'XF86LaunchE',0x1008ff4f:'XF86LaunchF',
    0x1008ff50:'XF86ApplicationLeft',0x1008ff51:'XF86ApplicationRight',0x1008ff52:'XF86Book',0x1008ff53:'XF86CD',0x1008ff54:'XF86Calculater',
    0x1008ff55:'XF86Clear',0x1008ff56:'XF86Close',0x1008ff57:'XF86Copy',0x1008ff58:'XF86Cut',0x1008ff59:'XF86Display',
    0x1008ff5a:'XF86DOS',0x1008ff5b:'XF86Documents',0x1008ff5c:'XF86Excel',0x1008ff5d:'XF86Explorer',0x1008ff5e:'XF86Game',
    0x1008ff5f:'XF86Go',0x1008ff60:'XF86iTouch',0x1008ff61:'XF86LogOff',0x1008ff62:'XF86Market',0x1008ff63:'XF86Meeting',
    0x1008ff65:'XF86MenuKB',0x1008ff66:'XF86MenuPB',0x1008ff67:'XF86MySites',0x1008ff68:'XF86New',0x1008ff69:'XF86News',
    0x1008ff6a:'XF86OfficeHome',0x1008ff6b:'XF86Open',0x1008ff6c:'XF86Option',0x1008ff6d:'XF86Paste',0x1008ff6e:'XF86Phone',
    0x1008ff70:'XF86Q',0x1008ff72:'XF86Reply',0x1008ff73:'XF86Reload',0x1008ff74:'XF86RotateWindows',0x1008ff75:'XF86RotationPB',
    0x1008ff76:'XF86RotationKB',0x1008ff77:'XF86Save',0x1008ff78:'XF86ScrollUp',0x1008ff79:'XF86ScrollDown',0x1008ff7a:'XF86ScrollClick',
    0x1008ff7b:'XF86Send',0x1008ff7c:'XF86Spell',0x1008ff7d:'XF86SplitScreen',0x1008ff7e:'XF86Support',0x1008ff7f:'XF86TaskPane',
    0x1008ff80:'XF86Terminal',0x1008ff81:'XF86Tools',0x1008ff82:'XF86Travel',0x1008ff84:'XF86UserPB',0x1008ff85:'XF86User1KB',
    0x1008ff86:'XF86User2KB',0x1008ff87:'XF86Video',0x1008ff88:'XF86WheelButton',0x1008ff89:'XF86Word',0x1008ff8a:'XF86Xfer',
    0x1008ff8b:'XF86ZoomIn',0x1008ff8c:'XF86ZoomOut',0x1008ff8d:'XF86Away',0x1008ff8e:'XF86Messenger',0x1008ff8f:'XF86WebCam',
    0x1008ff90:'XF86MailForward',0x1008ff91:'XF86Pictures',0x1008ff92:'XF86Music',0x1008ff93:'XF86Battery',0x1008ff94:'XF86Bluetooth',
    0x1008ff95:'XF86WLAN',0x1008ff96:'XF86UWB',0x1008ff97:'XF86AudioForward',0x1008ff98:'XF86AudioRepeat',0x1008ff99:'XF86AudioRandomPlay',
    0x1008ff9a:'XF86Subtitle',0x1008ff9b:'XF86AudioCycleTrack',0x1008ff9c:'XF86CycleAngle',0x1008ff9d:'XF86FrameBack',0x1008ff9e:'XF86FrameForward',
    0x1008ff9f:'XF86Time',0x1008ffa0:'XF86Select',0x1008ffa1:'XF86View',0x1008ffa2:'XF86TopMenu',0x1008ffa3:'XF86Red',
    0x1008ffa4:'XF86Green',0x1008ffa5:'XF86Yellow',0x1008ffa6:'XF86Blue',0x1008ffa7:'XF86Suspend',0x1008ffa8:'XF86Hibernate',
    0x1008ffa9:'XF86TouchpadToggle',0x1008ffb0:'XF86TouchpadOn',0x1008ffb1:'XF86TouchpadOff',0x1008ffb2:'XF86AudioMicMute',0x1008ffb3:'XF86Keyboard',
    0x1008ffb4:'XF86WWAN',0x1008ffb5:'XF86RFKill',0x1008ffb6:'XF86AudioPreset',0x1008ffb7:'XF86RotationLockToggle',0x1008ffb8:'XF86FullScreen',
}
# case mappings (src/keysym-case-mappings.c), chunk-compressed exactly as upstream.
_LEGACY_DATA = [(0, 1, 0), (1, 0, 16), (0, 0, 0), (0, 0, 0), (1, 0, 32), (0, 1, -16784831), (1, 0, 32), (1, 0, 32), (0, 0, 0), (0, 1, -1815), (0, 1, 32), (0, 0, 0), (0, 1, 32), (0, 1, 32), (0, 1, -4799), (0, 1, 0), (0, 0, 0), (1, 0, 16), (1, 0, 16), (0, 1, -16775323), (0, 0, 0), (0, 1, 16), (0, 0, 0), (0, 1, -16), (0, 1, -16), (0, 1, 0), (0, 1, 16), (0, 1, 16), (1, 0, 2), (0, 0, 0), (1, 0, -16), (1, 0, -16), (1, 0, -4799), (1, 0, -32), (1, 0, -32), (0, 1, -32), (0, 1, -32), (0, 0, 0), (1, 0, -576), (0, 0, 0), (0, 1, 2), (0, 0, 0), (0, 1, 624), (0, 1, 32), (0, 1, 33), (1, 0, 1), (0, 1, 1)]
_LEGACY_O1 = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 2, 2, 11, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 10, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 16, 17, 17, 16, 17, 16, 2, 2, 20, 26, 26, 25, 26, 25, 2, 2, 3, 6, 6, 6, 6, 6, 6, 6, 6, 7, 6, 6, 6, 2, 2, 2, 11, 12, 12, 12, 12, 12, 12, 12, 12, 43, 12, 12, 12, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 19, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 45, 32, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 16, 1, 2, 17, 1, 2, 2, 20, 20, 21, 2, 26, 27, 39, 7, 2, 2, 3, 2, 2, 7, 3, 3, 6, 2, 2, 3, 2, 3, 7, 10, 2, 2, 11, 2, 2, 10, 11, 11, 12, 2, 2, 11, 2, 11, 10, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 15, 2, 2, 2, 2, 8, 2, 2, 15, 2, 2, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 6, 6, 6, 4, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 10, 12, 12, 12, 13, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 16, 2, 2, 1, 37, 16, 1, 2, 20, 2, 2, 21, 41, 20, 21, 2, 2, 2, 3, 7, 2, 2, 2, 2, 2, 2, 3, 2, 7, 2, 3, 7, 2, 2, 11, 10, 2, 2, 2, 2, 2, 2, 11, 2, 10, 2, 11, 10, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 16, 16, 16, 1, 16, 17, 1, 17, 20, 20, 20, 21, 20, 26, 21, 26, 7, 3, 3, 7, 7, 7, 7, 3, 6, 7, 3, 2, 6, 3, 2, 7, 10, 11, 11, 10, 10, 10, 10, 11, 12, 10, 11, 2, 12, 11, 2, 10, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 22, 23, 23, 23, 23, 23, 23, 23, 29, 30, 30, 30, 30, 30, 30, 30, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33]
_LEGACY_O2 = [0, 284, 123, 412, 123, 348, 123, 220, 123, 123, 123, 123, 123, 476, 123, 62, 123, 128, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 188]
_UNICODE_DATA = [(0, 1, -128), (0, 1, -128), (0, 1, -112), (0, 1, -112), (0, 1, -126), (0, 1, -126), (0, 0, 0), (0, 0, 0), (0, 1, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, -42261), (0, 1, -42258), (0, 1, 0), (1, 0, 2), (1, 1, 1), (0, 1, 2), (1, 0, 1), (0, 1, 1), (1, 0, -97), (1, 0, -56), (1, 0, 32), (1, 0, 32), (0, 0, 0), (1, 0, 32), (1, 0, 32), (1, 0, 32), (1, 0, 32), (1, 0, 32), (1, 0, 32), (1, 0, 32), (1, 0, 32), (0, 1, -7615), (1, 0, -8), (1, 0, -8), (1, 0, -100), (1, 0, -100), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (1, 0, -8), (0, 0, 0), (1, 0, -8), (0, 0, 0), (1, 0, -8), (0, 0, 0), (1, 0, -8), (1, 0, -8), (1, 0, -74), (1, 0, -74), (1, 0, -9), (0, 0, 0), (0, 1, 7205), (0, 0, 0), (0, 1, 32), (0, 1, 32), (0, 1, 32), (0, 1, 32), (0, 1, 32), (0, 1, 32), (0, 1, 32), (0, 1, 32), (0, 1, -121), (0, 1, -10783), (0, 1, -10780), (0, 1, -10782), (0, 1, 210), (0, 1, 206), (0, 1, 0), (0, 1, 205), (0, 1, 205), (0, 1, -42315), (0, 1, 0), (0, 1, 207), (0, 1, -42343), (0, 1, -42280), (0, 1, -42308), (0, 1, 0), (1, 0, 32), (1, 0, 32), (1, 0, 32), (1, 0, 32), (1, 0, 32), (1, 0, 32), (1, 0, 32), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 1, -743), (0, 0, 0), (0, 0, 0), (0, 1, 0), (0, 1, -9), (0, 1, 0), (0, 0, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (1, 0, 0), (1, 0, 0), (0, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 0), (1, 0, 0), (0, 0, 0), (0, 0, 0), (0, 1, -8), (0, 1, -8), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, -7), (0, 1, 0), (0, 1, 0), (1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 1, 1), (0, 1, 15), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (0, 0, 0), (1, 0, 0), (0, 0, 0), (1, 0, -8383), (1, 0, -8262), (1, 0, 0), (1, 0, 0), (0, 0, 0), (0, 1, 0), (0, 0, 0), (0, 0, 0), (0, 1, 0), (0, 1, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (0, 0, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (1, 0, 26), (1, 0, 26), (1, 0, 26), (1, 0, 26), (1, 0, 26), (1, 0, 26), (1, 0, 26), (1, 0, 26), (0, 1, -35266), (1, 0, 1), (0, 1, 1), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (1, 0, 38), (0, 0, 0), (1, 0, -128), (1, 0, -128), (1, 0, -126), (1, 0, -126), (1, 0, -9), (0, 0, 0), (0, 0, 0), (0, 0, 0), (1, 0, 48), (1, 0, 48), (1, 0, 48), (1, 0, 48), (1, 0, 48), (1, 0, 48), (1, 0, 48), (1, 0, 48), (0, 0, 0), (0, 1, 62), (0, 1, 57), (1, 0, 0), (1, 0, 0), (1, 0, 0), (0, 1, 47), (0, 1, 54), (0, 1, 8), (0, 1, 8), (0, 1, 8), (0, 1, 8), (0, 1, 8), (0, 1, 8), (0, 0, 0), (0, 0, 0), (1, 0, 0), (0, 0, 0), (0, 0, 0), (1, 0, 0), (1, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (1, 0, 1), (0, 1, 1), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (1, 0, 2), (1, 1, 1), (0, 1, 2), (1, 0, 2), (1, 1, 1), (0, 1, 2), (1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 1, 1), (1, 0, -48), (1, 0, -42307), (1, 0, -35384), (1, 0, 1), (0, 1, 1), (0, 1, -163), (0, 1, -42561), (1, 0, 211), (1, 0, 213), (0, 1, -130), (1, 0, 214), (1, 0, -199), (0, 1, 232), (1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 1, 1), (1, 0, 218), (1, 0, 1), (1, 0, 15), (1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 1, 1), (1, 0, -10780), (1, 0, -10749), (1, 0, -10783), (0, 1, 1), (0, 1, 0), (1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 1, 1), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (1, 0, 0), (0, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 28), (1, 0, 0), (0, 1, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 1, 1), (1, 0, -7), (1, 0, 1), (0, 1, 1), (0, 1, 0), (1, 0, -130), (1, 0, -130), (1, 0, -130), (0, 1, 0), (1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 1, 1), (0, 0, 0), (0, 0, 0), (1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 1, 1), (0, 1, 79), (1, 0, 1), (0, 1, 1), (1, 0, -42308), (1, 0, -42319), (1, 0, -42315), (1, 0, -42305), (1, 0, -42308), (0, 1, 0), (0, 1, 202), (0, 1, 0), (0, 1, 203), (0, 1, -42319), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 928), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 0, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (1, 0, -10815), (1, 0, -10815), (1, 0, 7264), (1, 0, 7264), (1, 0, 7264), (1, 0, 7264), (1, 0, 7264), (1, 0, 7264), (1, 0, 7264), (1, 0, 7264), (0, 0, 0), (1, 0, 7264), (0, 1, -8), (0, 1, -8), (0, 1, -8), (0, 1, -8), (0, 1, -8), (0, 1, -8), (0, 1, -8), (0, 1, -8), (0, 0, 0), (0, 0, 0), (1, 0, -8), (1, 0, -8), (1, 0, -8), (1, 0, -8), (1, 0, -8), (1, 0, -8), (1, 0, -8), (1, 0, -8), (0, 0, 0), (0, 0, 0), (0, 1, 7264), (0, 1, 7264), (0, 1, 7264), (0, 1, 7264), (0, 1, 7264), (0, 1, 7264), (0, 1, 7264), (0, 1, 7264), (0, 0, 0), (0, 1, 7264), (1, 0, 34), (1, 0, 34), (1, 0, 34), (1, 0, 34), (1, 0, 34), (1, 0, 34), (1, 0, 34), (1, 0, 34), (0, 1, 34), (0, 1, 34), (0, 1, 34), (0, 1, 34), (0, 1, 34), (0, 1, 34), (0, 1, 34), (0, 1, 34), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 1, 1), (0, 0, 0), (0, 1, -8), (0, 1, -8), (0, 1, 0), (0, 1, -9), (0, 1, 0), (0, 0, 0), (0, 1, 0), (0, 1, 0), (0, 1, 219), (0, 1, 0), (0, 0, 0), (0, 0, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 0, 0), (0, 1, 0), (0, 0, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (1, 0, 1), (0, 1, 1), (0, 0, 0), (0, 1, 26), (0, 1, 26), (0, 1, 26), (0, 1, 26), (0, 1, 26), (0, 1, 26), (0, 1, 26), (0, 1, 26), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 1, -84), (0, 0, 0), (0, 0, 0), (1, 0, 64), (1, 0, 64), (1, 0, 64), (1, 0, 64), (1, 0, 64), (1, 0, 64), (1, 0, 64), (1, 0, 64), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 0), (1, 0, 0), (0, 1, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 1, 64), (0, 1, 64), (0, 1, 64), (0, 1, 64), (0, 1, 64), (0, 1, 64), (0, 1, 64), (0, 1, 64), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 1, 7264), (0, 0, 0), (0, 0, 0), (1, 0, 27), (1, 0, 27), (1, 0, 27), (1, 0, 27), (1, 0, 27), (1, 0, 27), (1, 0, 27), (1, 0, 27), (0, 0, 0), (0, 0, 0), (0, 1, 27), (0, 1, 27), (0, 1, 27), (0, 1, 27), (0, 1, 27), (0, 1, 27), (0, 1, 27), (0, 1, 27), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (1, 0, 1), (0, 1, 1), (1, 0, -42280), (0, 1, 0), (0, 0, 0), (0, 1, 32), (0, 1, 32), (0, 1, 31), (0, 1, 32), (0, 1, 32), (0, 1, 32), (0, 1, 32), (0, 1, 32), (0, 1, 64), (0, 1, 63), (0, 1, 63), (1, 0, 8), (1, 0, 8), (1, 0, 8), (1, 0, 8), (1, 0, 8), (1, 0, 8), (0, 0, 0), (0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (0, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (0, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (0, 0, 0), (0, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 59), (0, 1, 0), (0, 1, 0), (1, 0, -7615), (0, 1, 0), (0, 1, 48), (0, 1, 48), (0, 1, 48), (0, 1, 48), (0, 1, 48), (0, 1, 48), (0, 1, 48), (0, 1, 48), (0, 1, 0), (0, 1, -8), (0, 1, 0), (0, 1, -8), (0, 1, 0), (0, 1, -8), (0, 1, 0), (0, 1, -8), (0, 1, -8), (0, 1, 0), (0, 1, 0), (0, 0, 0), (0, 0, 0), (0, 1, 0), (0, 1, 0), (0, 1, -35332), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, -3814), (0, 1, 0), (0, 1, 0), (0, 1, 32), (0, 1, 32), (0, 1, 32), (0, 1, 32), (0, 1, 32), (0, 1, 32), (0, 1, 32), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (1, 0, 7264), (0, 0, 0), (0, 0, 0), (0, 1, 0), (0, 1, -130), (0, 1, -130), (0, 1, -130), (0, 0, 0), (1, 0, 116), (0, 1, 1), (1, 0, 1), (0, 1, 1), (1, 0, -42343), (1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 1, 1), (0, 1, 0), (0, 1, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 1, 28), (0, 0, 0), (1, 0, -42258), (1, 0, -42282), (1, 0, -42261), (1, 0, 928), (1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 1, 1), (0, 1, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (1, 0, 40), (1, 0, 40), (1, 0, 40), (1, 0, 40), (1, 0, 40), (1, 0, 40), (1, 0, 40), (1, 0, 40), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 1, 40), (0, 1, 40), (0, 1, 40), (0, 1, 40), (0, 1, 40), (0, 1, 40), (0, 1, 40), (0, 1, 40), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (1, 0, 39), (1, 0, 39), (1, 0, 39), (0, 0, 0), (1, 0, 39), (1, 0, 39), (1, 0, 39), (1, 0, 39), (1, 0, 39), (1, 0, 39), (1, 0, 39), (1, 0, 39), (0, 0, 0), (1, 0, 39), (1, 0, 39), (0, 0, 0), (0, 1, 39), (0, 1, 39), (0, 0, 0), (0, 1, 39), (0, 1, 39), (0, 1, 39), (0, 1, 39), (0, 1, 39), (0, 1, 39), (0, 1, 39), (0, 1, 39), (0, 0, 0), (0, 1, 39), (0, 1, 39), (0, 0, 0), (0, 0, 0), (0, 0, 0), (1, 0, -10782), (0, 1, 0), (1, 0, 1), (0, 1, 1), (0, 1, 0), (1, 0, 1), (0, 1, 1), (0, 1, 0), (0, 0, 0), (1, 0, 1), (0, 1, 1), (0, 1, 0), (0, 1, -56), (0, 1, 218), (0, 1, 69), (0, 1, 217), (0, 1, 217), (0, 1, 71), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, -10727), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, -35384), (0, 1, 0), (0, 1, -10749), (0, 1, 213), (0, 1, 0), (0, 1, 0), (0, 1, 214), (0, 1, 0), (0, 1, 0), (1, 0, 10795), (1, 0, 1), (0, 1, 1), (1, 0, -163), (1, 0, 10792), (0, 1, -10815), (1, 0, 1), (0, 1, 1), (1, 0, -195), (1, 0, 69), (1, 0, 71), (1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 1, 1), (1, 0, -42561), (0, 0, 0), (0, 0, 0), (0, 0, 0), (1, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (1, 0, 0), (0, 0, 0), (1, 0, -7517), (0, 0, 0), (0, 1, -3008), (0, 1, -3008), (0, 1, -3008), (0, 1, -3008), (0, 1, -3008), (0, 1, -3008), (0, 1, -3008), (0, 1, -3008), (0, 0, 0), (0, 1, 0), (0, 1, -3008), (0, 1, -3008), (0, 1, -3008), (1, 0, -3008), (1, 0, -3008), (1, 0, -3008), (1, 0, -3008), (1, 0, -3008), (1, 0, -3008), (1, 0, -3008), (1, 0, -3008), (0, 0, 0), (0, 0, 0), (1, 0, -3008), (1, 0, -3008), (1, 0, -3008), (0, 1, 1), (1, 0, 218), (0, 1, 0), (0, 1, 0), (1, 0, 1), (0, 1, 1), (1, 0, 218), (1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 1, 1), (0, 1, -48), (0, 1, 0), (1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 1, 1), (1, 0, -35332), (1, 0, 1), (0, 1, 1), (1, 0, -10743), (1, 0, -3814), (1, 0, -10727), (0, 1, 10795), (0, 1, 10792), (1, 0, 1), (1, 0, -121), (1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 1, 1), (0, 1, 300), (1, 0, -86), (1, 0, -86), (1, 0, -86), (1, 0, -86), (1, 0, -9), (0, 0, 0), (0, 0, 0), (0, 0, 0), (1, 0, -8), (1, 0, -8), (1, 0, -112), (1, 0, -112), (1, 0, -7), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 1, -195), (1, 0, 210), (1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 1, 1), (1, 0, 206), (1, 0, 1), (0, 1, -74), (0, 1, -74), (0, 1, -86), (0, 1, -86), (0, 1, -86), (0, 1, -86), (0, 1, -100), (0, 1, -100), (0, 1, 1), (1, 0, 205), (1, 0, 205), (1, 0, 1), (0, 1, 1), (0, 1, 0), (1, 0, 79), (1, 0, 202), (0, 1, 1), (1, 0, 217), (1, 0, 217), (1, 0, 1), (0, 1, 1), (1, 0, 1), (0, 1, 1), (1, 0, 219), (0, 1, 16), (0, 1, 16), (0, 1, 16), (0, 1, 16), (0, 1, 16), (0, 1, 16), (0, 1, 16), (0, 1, 16), (0, 1, 80), (0, 1, 80), (0, 1, 80), (0, 1, 80), (0, 1, 80), (0, 1, 80), (0, 1, 80), (0, 1, 80), (0, 1, 86), (0, 1, 80), (0, 1, -7), (0, 1, 116), (1, 0, -60), (0, 1, 96), (0, 0, 0), (1, 0, 1), (0, 1, 209), (0, 1, 211), (0, 1, -42308), (0, 1, -10743), (0, 1, -42305), (0, 1, 0), (0, 1, 0), (0, 1, 211), (0, 1, 218), (0, 1, 0), (0, 1, -42307), (0, 1, 218), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, -42282), (0, 1, 6254), (0, 1, 6253), (0, 1, 6244), (0, 1, 6242), (0, 1, 6242), (0, 1, 6243), (0, 1, 6236), (0, 1, 6181), (0, 1, 38864), (0, 1, 38864), (0, 1, 38864), (0, 1, 38864), (0, 1, 38864), (0, 1, 38864), (0, 1, 38864), (0, 1, 38864), (1, 0, 16), (1, 0, 16), (1, 0, 16), (1, 0, 16), (1, 0, 16), (1, 0, 16), (1, 0, 16), (1, 0, 16), (1, 0, 32), (1, 0, 32), (1, 0, 32), (1, 0, 32), (0, 1, 38), (0, 1, 37), (0, 1, 37), (0, 1, 37), (1, 0, 37), (1, 0, 37), (1, 0, 37), (0, 0, 0), (1, 0, 64), (0, 0, 0), (1, 0, 63), (1, 0, 63), (1, 0, 80), (1, 0, 80), (1, 0, 80), (1, 0, 80), (1, 0, 80), (1, 0, 80), (1, 0, 80), (1, 0, 80), (1, 0, 203), (1, 0, 1), (0, 1, 1), (1, 0, 205), (1, 0, 207), (0, 1, -97), (1, 0, 211), (1, 0, 209), (1, 0, 38864), (1, 0, 38864), (1, 0, 38864), (1, 0, 38864), (1, 0, 38864), (1, 0, 38864), (1, 0, 38864), (1, 0, 38864)]
_UNICODE_O1 = [166, 9, 14, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 173, 179, 179, 179, 458, 458, 458, 464, 9, 9, 398, 398, 398, 398, 400, 505, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 368, 368, 368, 368, 370, 641, 807, 807, 807, 807, 807, 812, 165, 357, 165, 166, 12, 170, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 35, 35, 35, 35, 66, 66, 66, 66, 9, 9, 9, 9, 513, 513, 513, 520, 523, 523, 527, 9, 9, 9, 9, 9, 329, 132, 130, 132, 132, 132, 132, 132, 132, 132, 165, 845, 132, 532, 840, 132, 132, 338, 671, 132, 253, 655, 132, 790, 9, 9, 450, 170, 569, 569, 569, 561, 165, 165, 565, 569, 569, 590, 354, 165, 165, 569, 569, 569, 561, 165, 165, 300, 228, 577, 590, 446, 355, 165, 569, 569, 569, 561, 165, 165, 354, 565, 569, 569, 159, 165, 165, 166, 563, 569, 569, 570, 165, 165, 165, 358, 569, 569, 569, 163, 165, 165, 356, 489, 9, 9, 9, 9, 9, 9, 165, 165, 165, 165, 350, 356, 165, 171, 963, 963, 963, 963, 963, 963, 963, 963, 963, 963, 9, 9, 9, 9, 9, 9, 9, 9, 165, 165, 165, 165, 165, 165, 165, 167, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 955, 187, 820, 820, 820, 820, 820, 825, 9, 9, 9, 9, 9, 9, 9, 9, 467, 9, 9, 9, 9, 9, 325, 647, 190, 987, 89, 35, 32, 979, 633, 66, 540, 544, 215, 132, 132, 132, 931, 314, 408, 408, 408, 408, 414, 416, 416, 416, 420, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 442, 165, 165, 165, 165, 165, 358, 170, 9, 9, 9, 9, 9, 9, 9, 9, 34, 35, 35, 94, 65, 66, 66, 638, 9, 9, 9, 9, 9, 6, 97, 6, 35, 35, 90, 36, 66, 66, 634, 67, 796, 557, 116, 582, 799, 147, 306, 153, 483, 663, 9, 9, 971, 971, 915, 915, 238, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 475, 475, 475, 475, 475, 475, 480, 9, 497, 497, 497, 497, 497, 497, 502, 9, 995, 995, 35, 35, 35, 35, 66, 66, 66, 66, 923, 923, 132, 132, 132, 132, 188, 329, 132, 132, 132, 132, 132, 132, 278, 133, 132, 132, 132, 132, 132, 132, 205, 206, 206, 206, 207, 9, 603, 604, 604, 604, 605, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 7, 10, 9, 9, 165, 168, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 569, 569, 569, 233, 569, 569, 569, 233, 569, 569, 569, 113, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 165, 626, 165, 764, 165, 165, 165, 165, 165, 165, 9, 9, 9, 9, 9, 9, 9, 9, 132, 132, 132, 132, 132, 323, 9, 9, 132, 132, 132, 659, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 35, 35, 91, 9, 66, 66, 635, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 711, 707, 711, 707, 716, 726, 723, 726, 723, 732, 9, 9, 9, 9, 9, 9, 9, 9, 34, 35, 35, 94, 65, 66, 66, 638, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1011, 1011, 1011, 1011, 1011, 1011, 1011, 1011, 1011, 1011, 551, 222, 109, 585, 572, 159, 165, 165, 165, 575, 141, 588, 163, 165, 165, 565, 569, 569, 590, 165, 165, 165, 569, 569, 569, 561, 165, 165, 565, 569, 569, 590, 165, 165, 165, 569, 569, 569, 561, 165, 165, 167, 569, 569, 569, 163, 165, 165, 356, 567, 569, 569, 161, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 294, 596, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 268, 131, 280, 292, 132, 132, 132, 132, 132, 859, 883, 899, 1003, 260, 270, 833, 907, 745, 243, 248, 280, 332, 132, 132, 24, 132, 132, 132, 132, 321, 132, 296, 777, 784, 132, 75, 345, 82, 939, 771, 758, 947, 753, 439, 17, 165, 165, 165, 8, 171, 9, 9, 9, 168, 9, 9, 9, 206, 206, 206, 206, 206, 206, 604, 604, 604, 604, 604, 604, 851, 284, 740, 360, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 132, 675, 425, 239, 9, 378, 388, 380, 390, 378, 388, 378, 388, 380, 390, 612, 51, 378, 388, 891, 0, 378, 388, 378, 388, 378, 388, 433, 58, 103, 867, 619, 44, 124, 875, 103, 198, 683, 683, 683, 683, 683, 695, 695, 695, 695, 695, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 683, 683, 683, 683, 687, 695, 695, 695, 695, 699]
_UNICODE_O2 = [367, 749, 780, 295, 448, 474, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 57, 3, 3, 640, 3, 3, 3, 3, 3, 3, 3, 3, 271, 536, 723, 844, 492, 399, 3, 3, 13, 3, 3, 3, 3, 3, 3, 3, 812, 45, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 560, 141, 3, 3, 3, 229, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 628, 3, 3, 3, 3, 876, 600, 3, 343, 3, 3, 3, 3, 416, 582, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 101, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 113, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 173, 672, 691, 203, 3, 3, 3, 3, 3, 3, 3, 89, 255, 3, 3, 3, 3, 3, 3, 3, 3, 327, 3, 3, 3, 3, 3, 3, 3, 518]
# U+0000..U+00FF normalisation table (src/keysym-utf.c keysymtab, non-deprecated).
_LOW_UCS = []
# --- END GENERATED TABLES ---


_NAME_TO_KEYSYM = {}
for _n, _v in _NAME_TO_KEYSYM_ORDER:
    _NAME_TO_KEYSYM.setdefault(_n, _v)

_LOW_UCS_MAP = dict(_LOW_UCS)

# --------------------------------------------------------------------------
# keysym name <-> value (src/keysym.c)
# --------------------------------------------------------------------------


def keysym_get_name(ks):
    """xkb_keysym_get_name -> the name `how-to-type` prints on line 1."""
    if ks > XKB_KEYSYM_MAX:
        return "Invalid"
    name = _KEYSYM_TO_NAME.get(ks)
    if name is not None:
        return name
    if XKB_KEYSYM_UNICODE_MIN <= ks <= XKB_KEYSYM_UNICODE_MAX:
        return "U%04X" % (ks & 0xFFFFFF)
    return "0x%08x" % ks


_HEX8 = re.compile(r"[0-9a-fA-F]{1,8}\Z")


def _utf32_to_keysym(ucs):
    """xkb_utf32_to_keysym (src/keysym-utf.c)."""
    if (0x0020 <= ucs <= 0x007E) or (0x00A0 <= ucs <= 0x00FF):
        return ucs
    if (0x08 <= ucs <= 0x0B) or ucs == 0x0D or ucs == 0x1B:  # \b \t \n \v, CR, ESC
        return ucs | 0xFF00
    if ucs == 0x7F:  # DEL
        return XKB_KEY_Delete
    if ucs == 0 or 0xD800 <= ucs <= 0xDFFF or ucs > 0x10FFFF:
        return XKB_KEY_NoSymbol
    low = _LOW_UCS_MAP.get(ucs)
    if low is not None:  # empty in 1.13.2: every U+0000..U+00FF table entry is deprecated
        return low
    return ucs | XKB_KEYSYM_UNICODE_OFFSET


def keysym_from_name(name):
    """xkb_keysym_from_name(name, XKB_KEYSYM_NO_FLAGS); 0 means NoSymbol."""
    val = _NAME_TO_KEYSYM.get(name)
    if val is not None:
        return val
    if name[:1] == "U":
        rest = name[1:]
        if _HEX8.match(rest):
            num = int(rest, 16)
            if 0xFF < num <= 0x10FFFF:
                return XKB_KEYSYM_UNICODE_OFFSET + num
            return _utf32_to_keysym(num)
        return XKB_KEY_NoSymbol
    if name[:2] == "0x":
        rest = name[2:]
        if _HEX8.match(rest):
            num = int(rest, 16)
            if num <= XKB_KEYSYM_MAX:
                return num
        return XKB_KEY_NoSymbol
    if name[:5] == "XF86_":
        return keysym_from_name(name[:4] + name[5:])
    return XKB_KEY_NoSymbol


_DEC = re.compile(r"[ \t\n\v\f\r]*([+-]?)([0-9]+)\Z")


def keysym_from_arg(arg):
    """`how-to-type --keysym ARG` resolution: keysym name first, then decimal.

    Returns None where how-to-type fails ("ERROR: Failed to convert argument to
    keysym", rc 2): unresolvable, zero, negative, or above XKB_KEYSYM_MAX.
    """
    ks = keysym_from_name(arg)
    if ks != XKB_KEY_NoSymbol:
        return ks
    m = _DEC.match(arg)
    if not m or m.group(1) == "-":
        return None
    val = int(m.group(2))
    if val <= 0 or val > XKB_KEYSYM_MAX:
        return None
    return val


# --------------------------------------------------------------------------
# keysym case predicates (src/keysym-case-mappings.c), used by automatic type
# detection.  Entries are (has_lower_mapping, has_upper_mapping, offset).
# --------------------------------------------------------------------------


def _legacy_case_entry(ks):
    return _LEGACY_DATA[_LEGACY_O1[_LEGACY_O2[ks >> 7] + ((ks >> 1) & 0x3F)] + (ks & 0x1)]


def _unicode_case_entry(ucs):
    return _UNICODE_DATA[_UNICODE_O1[_UNICODE_O2[ucs >> 8] + ((ucs >> 3) & 0x1F)] + (ucs & 0x7)]


def keysym_is_lower(ks):
    """xkb_keysym_is_lower."""
    if ks <= 0x13BE:
        e = _legacy_case_entry(ks)
        return bool(e[1]) and not e[0]
    if XKB_KEYSYM_UNICODE_MIN <= ks <= 0x0101F189:
        e = _unicode_case_entry(ks - XKB_KEYSYM_UNICODE_OFFSET)
        return bool(e[1]) and not e[0]
    return False


def keysym_is_upper_or_title(ks):
    """xkb_keysym_is_upper_or_title."""
    if ks <= 0x13BE:
        return bool(_legacy_case_entry(ks)[0])
    if XKB_KEYSYM_UNICODE_MIN <= ks <= 0x0101F189:
        return bool(_unicode_case_entry(ks - XKB_KEYSYM_UNICODE_OFFSET)[0])
    return False


def keysym_is_keypad(ks):
    """xkb_keysym_is_keypad."""
    return KEYPAD_FIRST <= ks <= KEYPAD_LAST


# --------------------------------------------------------------------------
# keymap model
# --------------------------------------------------------------------------


class TypeEntry:
    __slots__ = ("mods_expr", "raw", "eff", "level", "active")

    def __init__(self, mods_expr, level):
        self.mods_expr = mods_expr   # (names, literal) resolved in _finish
        self.raw = 0
        self.eff = 0
        self.level = level
        self.active = False


class KeyType:
    __slots__ = ("name", "num_levels", "entries")

    def __init__(self, name):
        self.name = name
        self.num_levels = 1
        self.entries = []


class Group:
    __slots__ = ("type", "levels", "explicit_actions")

    def __init__(self):
        self.type = None
        self.levels = []          # list of lists of keysyms
        self.explicit_actions = False


class Key:
    __slots__ = ("keycode", "name", "modmap", "vmodmap", "vmodmap_explicit", "groups")

    def __init__(self, keycode, name):
        self.keycode = keycode
        self.name = name
        self.modmap = 0
        self.vmodmap = 0
        self.vmodmap_explicit = False
        self.groups = []


class Keymap:
    __slots__ = ("keys", "types", "types_order", "vmods", "vmod_masks",
                 "mod_names", "mod_masks", "group_names",
                 "min_keycode", "max_keycode")

    def __init__(self):
        self.keys = {}
        self.types = {}
        self.types_order = []
        self.vmods = []
        self.vmod_masks = []
        self.mod_names = list(REAL_MODS)
        self.mod_masks = [1 << i for i in range(NUM_REAL_MODS)]
        self.group_names = []
        self.min_keycode = 8
        self.max_keycode = 255

    def vmod_index(self):
        return {name: NUM_REAL_MODS + i for i, name in enumerate(self.vmods)}


class Interpret:
    __slots__ = ("sym", "match", "mods_expr", "mods", "vmod", "level_one_only")

    def __init__(self):
        self.sym = 0
        self.match = "AnyOfOrNone"
        self.mods_expr = ([], 0)
        self.mods = 0
        self.vmod = None
        self.level_one_only = False


# --------------------------------------------------------------------------
# tokenizer for the serialized text_v1 keymap
# --------------------------------------------------------------------------

_TOKEN_RE = re.compile(
    r"""
      (?P<ws>\s+)
    | (?P<comment>//[^\n]*|/\*.*?\*/)
    | (?P<str>"(?:[^"\\]|\\.)*")
    | (?P<punct>[{}\[\]()<>;,=+\-])
    | (?P<word>[A-Za-z0-9_.]+)
    | (?P<other>.)
    """,
    re.S | re.X,
)

_ESCAPE_RE = re.compile(r"\\(n|\\|0([0-7])([0-7]))")


def _unescape(lit):
    def repl(m):
        if m.group(1) == "n":
            return "\n"
        if m.group(1) == "\\":
            return "\\"
        return chr(((ord(m.group(2)) - 48) << 3) | (ord(m.group(3)) - 48))

    return _ESCAPE_RE.sub(repl, lit[1:-1])


def _tokenize(text):
    toks = []
    pos = 0
    n = len(text)
    while pos < n:
        m = _TOKEN_RE.match(text, pos)
        if not m:
            raise ValueError("cannot tokenize at offset %d: %r" % (pos, text[pos:pos + 24]))
        pos = m.end()
        kind = m.lastgroup
        if kind in ("ws", "comment"):
            continue
        if kind == "other":
            toks.append(("punct", val))
            continue
        val = m.group()
        toks.append(("str", _unescape(val)) if kind == "str" else (kind, val))
    return toks


class _Parser:
    __slots__ = ("toks", "i")

    def __init__(self, toks):
        self.toks = toks
        self.i = 0

    def peek(self, k=0):
        j = self.i + k
        return self.toks[j] if j < len(self.toks) else (None, None)

    def at(self, value, k=0):
        t = self.peek(k)
        return t[0] in ("punct", "word") and t[1] == value

    def take(self):
        t = self.peek()
        self.i += 1
        return t

    def expect(self, value):
        t = self.take()
        if t[1] != value:
            raise ValueError("expected %r, got %r at token %d" % (value, t, self.i - 1))
        return t

    def take_key_name(self):
        """A `<...>` key name, whose text may contain '+' or '-' (e.g. <VOL+>)."""
        self.expect("<")
        parts = []
        while not self.at(">"):
            kind, val = self.take()
            if kind is None:
                raise ValueError("unterminated key name")
            parts.append(val)
        self.expect(">")
        return "".join(parts)

    def skip_statement(self):
        """Consume to the ';' ending the current statement (nesting aware)."""
        depth = 0
        while True:
            kind, val = self.take()
            if kind is None:
                return
            if kind != "punct":
                continue
            if val in "{[(":
                depth += 1
            elif val in "}])":
                if depth == 0:
                    self.i -= 1
                    return
                depth -= 1
            elif val == ";" and depth == 0:
                return

    def skip_block(self, depth):
        """Consume tokens until the block opened before self.i closes."""
        while depth:
            kind, val = self.take()
            if kind is None:
                raise ValueError("unterminated block")
            if kind == "punct":
                if val == "{":
                    depth += 1
                elif val == "}":
                    depth -= 1


# --------------------------------------------------------------------------
# modifier expressions: names joined by '+', plus none / all / 0xNNNN / decimal
# --------------------------------------------------------------------------


def _parse_mod_expr(p):
    """Return (names, literal_bits)."""
    names = []
    literal = 0
    while True:
        kind, val = p.peek()
        if kind == "word":
            p.take()
            if val == "none":
                pass
            elif val == "all":
                literal |= MOD_REAL_MASK_ALL
            elif val[:2] == "0x":
                literal |= int(val, 16)
            elif val.isdigit():
                literal |= int(val)
            else:
                names.append(val)
        elif kind == "punct" and val == "+":
            p.take()
            continue
        else:
            break
        if p.at("+"):
            p.take()
            continue
        break
    return names, literal


def _resolve_mod_expr(expr, index):
    names, literal = expr
    mask = literal
    for name in names:
        if name in REAL_MODS:
            mask |= 1 << REAL_MODS.index(name)
        elif name in index:
            mask |= 1 << index[name]
        else:
            raise ValueError("unknown modifier name %r" % (name,))
    return mask


# --------------------------------------------------------------------------
# section parsers
# --------------------------------------------------------------------------


def _parse_virtual_modifiers(p, vmod_order, vmod_explicit):
    p.take()  # virtual_modifiers
    while True:
        kind, val = p.peek()
        if kind == "word":
            p.take()
            name = val
            value = None
            if p.at("="):
                p.take()
                names, literal = _parse_mod_expr(p)
                value = _resolve_mod_expr((names, literal),
                                          {n: NUM_REAL_MODS + i for i, n in enumerate(vmod_order)})
            if name not in vmod_order:
                vmod_order.append(name)
            if value is not None:
                vmod_explicit[name] = value
        if p.at(","):
            p.take()
            continue
        break
    p.expect(";")


def _parse_keycodes(p, km):
    keys = {}
    aliases = []
    while not p.at("}"):
        kind, val = p.peek()
        if kind is None:
            raise ValueError("unexpected end of keycodes section")
        if val in ("minimum", "maximum"):
            p.take()
            p.expect("=")
            num = int(p.take()[1], 0)
            p.expect(";")
            if val == "minimum":
                km.min_keycode = num
            else:
                km.max_keycode = num
        elif val == "alias":
            p.take()
            alias = p.take_key_name()
            p.expect("=")
            real = p.take_key_name()
            p.expect(";")
            aliases.append((alias, real))
        elif val == "<":
            name = p.take_key_name()
            p.expect("=")
            kc = int(p.take()[1], 0)
            p.expect(";")
            keys[name] = kc
        else:
            p.skip_statement()
    p.expect("}")
    for alias, real in aliases:
        if real in keys and alias not in keys:
            keys[alias] = keys[real]
    for name, kc in keys.items():
        if kc not in km.keys:
            km.keys[kc] = Key(kc, name)


def _parse_types(p, km, vmod_order, vmod_explicit):
    while not p.at("}"):
        kind, val = p.peek()
        if kind is None:
            raise ValueError("unexpected end of types section")
        if val == "virtual_modifiers":
            _parse_virtual_modifiers(p, vmod_order, vmod_explicit)
        elif val == "type":
            p.take()
            tkind, tname = p.take()
            if tkind != "str":
                raise ValueError("type name must be a string")
            p.expect("{")
            t = KeyType(tname)
            while not p.at("}"):
                fval = p.peek()[1]
                if fval == "modifiers":
                    p.take()
                    p.expect("=")
                    _parse_mod_expr(p)
                    p.expect(";")
                elif fval == "map":
                    p.take()
                    p.expect("[")
                    expr = _parse_mod_expr(p)
                    p.expect("]")
                    p.expect("=")
                    value = p.take()[1]
                    p.expect(";")
                    level = int(value, 0) - 1
                    if level < 0:
                        level = 0
                    t.entries.append(TypeEntry(expr, level))
                    if level + 1 > t.num_levels:
                        t.num_levels = level + 1
                elif fval == "preserve":
                    p.take()
                    p.expect("[")
                    _parse_mod_expr(p)
                    p.expect("]")
                    p.expect("=")
                    _parse_mod_expr(p)
                    p.expect(";")
                elif fval == "level_name":
                    p.skip_statement()
                else:
                    p.skip_statement()
            p.expect("}")
            p.expect(";")
            if tname not in km.types:
                km.types[tname] = t
                km.types_order.append(tname)
        else:
            p.skip_statement()
    p.expect("}")


def _parse_compat(p, vmod_order, vmod_explicit, interps):
    while not p.at("}"):
        kind, val = p.peek()
        if kind is None:
            raise ValueError("unexpected end of compat section")
        if val == "virtual_modifiers":
            _parse_virtual_modifiers(p, vmod_order, vmod_explicit)
        elif val == "interpret":
            p.take()
            it = Interpret()
            _skind, sval = p.take()
            it.sym = 0 if sval == "Any" else keysym_from_name(sval)
            p.expect("+")
            it.match = p.take()[1]
            p.expect("(")
            it.mods_expr = _parse_mod_expr(p)
            p.expect(")")
            p.expect("{")
            while not p.at("}"):
                fval = p.peek()[1]
                if fval == "virtualModifier":
                    p.take()
                    p.expect("=")
                    it.vmod = p.take()[1]
                    p.expect(";")
                elif fval == "useModMapMods":
                    p.take()
                    p.expect("=")
                    it.level_one_only = (p.take()[1] == "level1")
                    p.expect(";")
                elif fval == "repeat":
                    p.skip_statement()
                elif fval == "action":
                    p.take()
                    p.expect("=")
                    _skip_action(p)
                    p.expect(";")
                else:
                    p.skip_statement()
            p.expect("}")
            p.expect(";")
            interps.append(it)
        else:
            p.skip_statement()
    p.expect("}")


def _skip_action(p):
    """Skip one action value: Name(...) or { Name(...), ... }."""
    if p.at("{"):
        depth = 0
        while True:
            kind, val = p.take()
            if kind is None:
                raise ValueError("unterminated action block")
            if kind == "punct":
                if val == "{":
                    depth += 1
                elif val == "}":
                    depth -= 1
                    if depth == 0:
                        return
    p.take()  # action name
    if p.at("("):
        depth = 0
        while True:
            kind, val = p.take()
            if kind is None:
                raise ValueError("unterminated action arguments")
            if kind == "punct":
                if val == "(":
                    depth += 1
                elif val == ")":
                    depth -= 1
                    if depth == 0:
                        return


def _parse_keysym_levels(p):
    """Parse `[ level, level, ... ]`; a level is `sym` or `{ sym, ... }`."""
    p.expect("[")
    levels = []
    while not p.at("]"):
        if p.at("{"):
            p.take()
            syms = []
            while not p.at("}"):
                if p.at(","):
                    p.take()
                    continue
                kind, val = p.take()
                if kind != "word":
                    raise ValueError("unexpected token in keysym group: %r" % (val,))
                if val == "NoSymbol":
                    continue
                syms.append(keysym_from_name(val))
            p.expect("}")
            levels.append(syms)
        else:
            kind, val = p.take()
            if kind != "word":
                raise ValueError("unexpected token in keysym list: %r" % (val,))
            levels.append([] if val == "NoSymbol" else [keysym_from_name(val)])
        if p.at(","):
            p.take()
    p.expect("]")
    return levels


def _skip_actions_list(p):
    p.expect("[")
    depth = 0
    while True:
        kind, val = p.take()
        if kind is None:
            raise ValueError("unterminated actions list")
        if kind == "punct":
            if val in "([{":
                depth += 1
            elif val in ")]}":
                if val == "]" and depth == 0:
                    return
                depth -= 1


def _parse_symbols(p, km, vmod_order, vmod_explicit):
    pending_modmap = []
    while not p.at("}"):
        kind, val = p.peek()
        if kind is None:
            raise ValueError("unexpected end of symbols section")
        if val == "name":
            p.take()
            p.expect("[")
            idx = int(p.take()[1], 0) - 1
            p.expect("]")
            p.expect("=")
            _gkind, gname = p.take()
            p.expect(";")
            while len(km.group_names) <= idx:
                km.group_names.append(None)
            km.group_names[idx] = gname
        elif val == "key":
            p.take()
            kname = p.take_key_name()
            p.expect("{")
            kc = None
            for key in km.keys.values():
                if key.name == kname:
                    kc = key.keycode
                    break
            if kc is None:
                p.skip_block(1)
                if p.at(";"):
                    p.take()
                continue
            key = km.keys[kc]
            key_levels = {}
            key_types = {}
            default_type = None
            action_groups = set()
            vmods_expr = None
            while not p.at("}"):
                fval = p.peek()[1]
                if fval == "type":
                    p.take()
                    if p.at("["):
                        p.take()
                        gidx = int(p.take()[1], 0) - 1
                        p.expect("]")
                        p.expect("=")
                        key_types[gidx] = p.take()[1]
                    else:
                        p.expect("=")
                        default_type = p.take()[1]
                    p.expect(",")
                elif fval == "repeat":
                    p.take()
                    p.expect("=")
                    p.take()
                    p.expect(",")
                elif fval == "virtualMods":
                    p.take()
                    p.expect("=")
                    vmods_expr = _parse_mod_expr(p)
                    p.expect(",")
                elif fval in ("groupsClamp", "groupsRedirectionStub"):
                    p.skip_statement()
                    if p.at(","):
                        p.take()
                elif fval == "groupsRedirect":
                    p.skip_statement()
                    if p.at(","):
                        p.take()
                elif fval == "symbols":
                    p.take()
                    p.expect("[")
                    gidx = int(p.take()[1], 0) - 1
                    p.expect("]")
                    p.expect("=")
                    key_levels[gidx] = _parse_keysym_levels(p)
                    if p.at(","):
                        p.take()
                elif fval == "actions":
                    p.take()
                    p.expect("[")
                    gidx = int(p.take()[1], 0) - 1
                    p.expect("]")
                    p.expect("=")
                    _skip_actions_list(p)
                    action_groups.add(gidx)
                    if p.at(","):
                        p.take()
                elif fval == "[":
                    key_levels[0] = _parse_keysym_levels(p)
                else:
                    p.skip_statement()
                    if p.at(","):
                        p.take()
            p.expect("}")
            p.expect(";")
            ngroups = 0
            for gidx in set(key_levels) | set(key_types):
                if key_levels.get(gidx) or gidx in key_types:
                    ngroups = max(ngroups, gidx + 1)
            if default_type is not None:
                for gidx in key_levels:
                    if key_levels[gidx]:
                        ngroups = max(ngroups, gidx + 1)
            if ngroups <= 0:
                continue
            key.groups = []
            for gidx in range(ngroups):
                g = Group()
                g.levels = key_levels.get(gidx, [])
                g.explicit_actions = gidx in action_groups
                g.type = _resolve_type(km, g, key_types.get(gidx, default_type))
                _resize_levels(g)
                key.groups.append(g)
            if vmods_expr is not None:
                key.vmodmap = _resolve_mod_expr(
                    vmods_expr, {n: NUM_REAL_MODS + i for i, n in enumerate(vmod_order)})
                key.vmodmap_explicit = True
        elif val == "modifier_map":
            p.take()
            mod_name = p.take()[1]
            p.expect("{")
            names = []
            while not p.at("}"):
                if p.at("<"):
                    names.append(p.take_key_name())
                elif p.at(","):
                    p.take()
                else:
                    p.take()
            p.expect("}")
            p.expect(";")
            pending_modmap.append((mod_name, names))
        else:
            p.skip_statement()
    p.expect("}")
    by_name = {key.name: key for key in km.keys.values()}
    for mod_name, names in pending_modmap:
        if mod_name not in REAL_MODS:
            continue
        bit = 1 << REAL_MODS.index(mod_name)
        for name in names:
            key = by_name.get(name)
            if key is not None:
                key.modmap |= bit


# --------------------------------------------------------------------------
# type assignment (src/xkbcomp/symbols.c)
# --------------------------------------------------------------------------


def _find_automatic_type(levels):
    def get_sym(i):
        if i >= len(levels) or not levels[i]:
            return XKB_KEY_NoSymbol
        return levels[i][0]

    width = len(levels)
    if width <= 1:
        return "ONE_LEVEL"
    sym0, sym1 = get_sym(0), get_sym(1)
    if width == 2:
        if keysym_is_lower(sym0) and keysym_is_upper_or_title(sym1):
            return "ALPHABETIC"
        if keysym_is_keypad(sym0) or keysym_is_keypad(sym1):
            return "KEYPAD"
        return "TWO_LEVEL"
    if width <= 4:
        if keysym_is_lower(sym0) and keysym_is_upper_or_title(sym1):
            sym2 = get_sym(2)
            sym3 = get_sym(3) if width == 4 else XKB_KEY_NoSymbol
            if keysym_is_lower(sym2) and keysym_is_upper_or_title(sym3):
                return "FOUR_LEVEL_ALPHABETIC"
            return "FOUR_LEVEL_SEMIALPHABETIC"
        if keysym_is_keypad(sym0) or keysym_is_keypad(sym1):
            return "FOUR_LEVEL_KEYPAD"
        return "FOUR_LEVEL"
    return None


def _resolve_type(km, group, type_name):
    if type_name is None:
        type_name = _find_automatic_type(group.levels)
    if type_name is not None:
        t = km.types.get(type_name)
        if t is not None:
            return t
    if km.types_order:
        return km.types[km.types_order[0]]
    t = KeyType("ONE_LEVEL")
    km.types[t.name] = t
    km.types_order.append(t.name)
    return t


def _resize_levels(group):
    n = group.type.num_levels
    if len(group.levels) > n:
        del group.levels[n:]
    while len(group.levels) < n:
        group.levels.append([])


# --------------------------------------------------------------------------
# top-level parse
# --------------------------------------------------------------------------


def parse_keymap(text):
    p = _Parser(_tokenize(text))
    p.expect("xkb_keymap")
    p.expect("{")
    km = Keymap()
    vmod_order = []
    vmod_explicit = {}
    interps = []
    while not p.at("}"):
        val = p.peek()[1]
        if val == "xkb_keycodes":
            p.take()
            if p.peek()[0] == "str":
                p.take()
            p.expect("{")
            _parse_keycodes(p, km)
            p.expect(";")
        elif val == "xkb_types":
            p.take()
            if p.peek()[0] == "str":
                p.take()
            p.expect("{")
            _parse_types(p, km, vmod_order, vmod_explicit)
            p.expect(";")
        elif val == "xkb_compatibility":
            p.take()
            if p.peek()[0] == "str":
                p.take()
            p.expect("{")
            _parse_compat(p, vmod_order, vmod_explicit, interps)
            p.expect(";")
        elif val == "xkb_symbols":
            p.take()
            if p.peek()[0] == "str":
                p.take()
            p.expect("{")
            _parse_symbols(p, km, vmod_order, vmod_explicit)
            p.expect(";")
        else:
            p.skip_statement()
    p.expect("}")
    if p.at(";"):
        p.take()
    _finish(km, vmod_order, vmod_explicit, interps)
    return km


def _finish(km, vmod_order, vmod_explicit, interps):
    km.vmods = list(vmod_order)
    index = km.vmod_index()
    # Interpret mod masks need the final vmod index order.
    for it in interps:
        it.mods = _resolve_mod_expr(it.mods_expr, index)
    for tname in km.types_order:
        for e in km.types[tname].entries:
            e.raw = _resolve_mod_expr(e.mods_expr, index)
    # virtual modifier -> real modifier mapping (src/xkbcomp/keymap.c)
    mapping = dict((name, vmod_explicit.get(name, 0)) for name in km.vmods)
    for kc in sorted(km.keys):
        key = km.keys[kc]
        if not key.vmodmap_explicit:
            key.vmodmap = _apply_interps(key, interps, index)
    for kc in sorted(km.keys):
        key = km.keys[kc]
        if not key.vmodmap:
            continue
        for name in km.vmods:
            if key.vmodmap & (1 << index[name]):
                mapping[name] |= key.modmap
    # The judge always parses the file as keymap format 2 (how-to-type's
    # --format default), where a virtual modifier left without an explicit
    # mapping takes its canonical encoding, i.e. itself
    # (src/xkbcomp/keymap.c:459-481).  Only `virtual_modifiers M = <expr>`
    # suppresses that, so an explicit `= none` keeps the mapping at zero.
    for name in km.vmods:
        if mapping[name] == 0 and name not in vmod_explicit:
            mapping[name] = 1 << index[name]
    km.vmod_masks = [mapping[name] for name in km.vmods]
    km.mod_names = list(REAL_MODS) + list(km.vmods)
    km.mod_masks = [1 << i for i in range(NUM_REAL_MODS)] + list(km.vmod_masks)
    # type entries: effective masks, deactivated entries with unbound vmods
    nmods = len(km.mod_names)
    known = (1 << nmods) - 1
    for tname in km.types_order:
        for e in km.types[tname].entries:
            eff = e.raw & MOD_REAL_MASK_ALL
            unbound = False
            for i, mask in enumerate(km.vmod_masks):
                if e.raw & (1 << (NUM_REAL_MODS + i)):
                    if mask == 0:
                        unbound = True
                    eff |= mask
            eff |= e.raw & ~known
            e.eff = eff
            e.active = (e.raw == 0) or (not unbound)


def _apply_interps(key, interps, index):
    """ApplyInterpsToKey: the vmodmap contribution of the interpretations."""
    vmodmap = 0
    for group_index, group in enumerate(key.groups):
        if group.explicit_actions:
            continue
        for level, syms in enumerate(group.levels):
            if not syms:
                continue
            matched = []
            for sym in syms:
                chosen = None
                for i, it in enumerate(interps):
                    if it.sym != sym and it.sym != XKB_KEY_NoSymbol:
                        continue
                    mods = 0 if (it.level_one_only and level != 0) else key.modmap
                    found = _match_interp(it, mods)
                    if found and i > 0 and it.sym == XKB_KEY_NoSymbol:
                        # Repeated catch-all interpretation for a later keysym
                        # of the same level is ignored (keymap.c:143-165).
                        if any(prev is it for prev in matched):
                            found = False
                    if found:
                        chosen = it
                        break
                if chosen is None:
                    continue
                matched.append(chosen)
                if (group_index == 0 and level == 0) or not chosen.level_one_only:
                    if chosen.vmod is not None:
                        idx = index.get(chosen.vmod)
                        if idx is not None:
                            vmodmap |= 1 << idx
    return vmodmap


def _match_interp(it, mods):
    if it.match == "NoneOf":
        return not (it.mods & mods)
    if it.match == "AnyOfOrNone":
        return (not mods) or bool(it.mods & mods)
    if it.match == "AnyOf":
        return bool(it.mods & mods)
    if it.match == "AllOf":
        return (it.mods & mods) == it.mods
    if it.match == "Exactly":
        return it.mods == mods
    raise ValueError("unknown interpret match %r" % (it.match,))


# --------------------------------------------------------------------------
# rendering (tools/how-to-type.c)
# --------------------------------------------------------------------------


def _printf_x06(value):
    """C `printf("%#06" PRIx32, value)`; '#' adds no prefix for zero."""
    if value == 0:
        return "000000"
    return "0x%04x" % value


def mods_for_level(type_, level):
    """xkb_keymap_key_get_mods_for_level."""
    if level >= type_.num_levels:
        return []
    masks = []
    if level == 0:
        empty_mapped = any(e.active and e.eff == 0 for e in type_.entries)
        if not empty_mapped:
            masks.append(0)
    for e in type_.entries:
        if len(masks) >= MAX_TYPE_MAP_ENTRIES:
            break
        if e.active and e.level == level:
            masks.append(e.eff)
    return masks


def _mod_names_for_mask(km, mask):
    return [name for name, mmask in zip(km.mod_names, km.mod_masks)
            if (mask & mmask) == mmask]


def _pad(text, width):
    """C `printf("%-Ns", text)` pads by BYTES, not characters."""
    n = len(text.encode("utf-8", "surrogateescape"))
    if n >= width:
        return text
    return text + " " * (width - n)


def _combo_line(km, keycode, key_name, layout, layout_name, level, mask):
    return "".join((
        _pad(str(keycode), 8), " ",
        _pad(key_name, 9), " ",
        _pad(str(layout + 1), 8), " ",
        _pad(layout_name, 20), " ",
        _pad(str(level + 1), 7), " [ ",
        "".join(name + " " for name in _mod_names_for_mask(km, mask)),
        "]\n"))


def how_to_type(keymap, ks):
    """The judge's stdout for `--keymap ... --disable-compose --keysym ks`."""
    km = keymap
    out = ["keysym: %s (%s)\n\n" % (keysym_get_name(ks), _printf_x06(ks)),
           "=== Direct access ===\n\n",
           "".join((_pad("KEYCODE", 8), " ", _pad("KEY NAME", 9), " ",
                    _pad("LAYOUT", 8), " ", _pad("LAYOUT NAME", 20), " ",
                    _pad("LEVEL#", 7), " MODIFIERS\n"))]
    for kc in sorted(km.keys):
        key = km.keys[kc]
        if key.name is None:
            continue
        for layout, group in enumerate(key.groups):
            type_ = group.type
            if type_ is None:
                continue
            layout_name = (km.group_names[layout]
                           if layout < len(km.group_names) else None)
            if layout_name is None:
                layout_name = "?"
            for level in range(type_.num_levels):
                syms = group.levels[level] if level < len(group.levels) else ()
                if len(syms) != 1 or syms[0] != ks:
                    continue
                for mask in mods_for_level(type_, level):
                    out.append(_combo_line(km, kc, key.name, layout,
                                           layout_name, level, mask))
    return "".join(out), 0


# --------------------------------------------------------------------------
# CLI: only the contract's command line
# --------------------------------------------------------------------------


def _cli(argv):
    prog = argv[0] if argv else "mado-keysym.py"
    path = None
    disable_compose = False
    keysym_mode = False
    positional = []
    i = 1
    while i < len(argv):
        a = argv[i]
        if a == "--keymap":
            # how-to-type declares --keymap with an *optional* argument, so the
            # space-separated form never binds: getopt leaves it NULL and the
            # would-be FILE becomes a positional.  Reproduce that exactly.
            pass
        elif a.startswith("--keymap="):
            path = a.split("=", 1)[1]
        elif a == "--disable-compose":
            disable_compose = True
        elif a == "--keysym":
            keysym_mode = True
        elif a in ("--help", "-h"):
            # getopt_long's 'h': usage on stdout, exit success.
            sys.stdout.write(USAGE % prog)
            return 0
        elif a.startswith("--"):
            sys.stderr.write("ERROR: option out of contract: %s\n" % a)
            sys.stderr.write(USAGE % prog)
            return 2
        else:
            positional.append(a)
        i += 1
    if len(positional) != 1:
        sys.stderr.write("ERROR: missing positional parameter\n")
        sys.stderr.write(USAGE % prog)
        return 2
    if path is None or not disable_compose or not keysym_mode:
        sys.stderr.write("ERROR: --keymap=FILE, --disable-compose and --keysym ARG "
                         "are required (a stdin keymap, Compose sequences and "
                         "character/code-point interpretation are out of "
                         "contract)\n")
        sys.stderr.write(USAGE % prog)
        return 2
    ks = keysym_from_arg(positional[0])
    if ks is None:
        sys.stderr.write("ERROR: Failed to convert argument to keysym\n")
        sys.stderr.write(USAGE % prog)
        return 2
    with open(path, "r", encoding="utf-8", errors="surrogateescape") as f:
        text = f.read()
    out, rc = how_to_type(parse_keymap(text), ks)
    sys.stdout.buffer.write(out.encode("utf-8", "surrogateescape"))
    sys.stdout.buffer.flush()
    return rc


def main(argv=None):
    return _cli(list(sys.argv if argv is None else argv))


if __name__ == "__main__":
    sys.exit(main())
