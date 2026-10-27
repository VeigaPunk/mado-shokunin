Verdict: probes support the scoped libxkbcommon behavior claims; no contradiction found.
Probe built with gcc and pkg-config xkbcommon, host libxkbcommon 1.13.2.
CASE_INSENSITIVE outputs: Q -> 0x71 (q); SLASH -> 0x2f (slash); Delete and DELETE -> 0xffff (NoSymbol) on this installed keysyms table; XF86AudioMute -> 0x1008ff12.
Default host keymap (no explicit RMLVO): AD01 keycode 24 -> q; AB11 keycode 97 -> NoSymbol. This is not the entry’s Brazilian-layout condition.
Explicit layout=br, zero-mod state: AD01 -> q; AB11 -> slash. After xkb_state_update_mask(..., group=1), AD01 -> q; AB11 -> slash (the keymap exposes no different symbol in group 1 for these keys).
Therefore Q/SLASH preference and br AD01/AB11 zero-mod claims are supported. The group-selection mechanism itself remains demonstrated only if tested with a keymap whose group 1 differs; this probe did not establish a changing symbol. The entry correctly says multi-layout effect not observed on host.
Commands executed: gcc probe.c $(pkg-config --cflags --libs xkbcommon) && ./probe; pkg-config --modversion xkbcommon => 1.13.2. Scratch removed by trap.
