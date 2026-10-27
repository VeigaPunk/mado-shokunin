# Pinned sources — libxkbcommon xkbcommon-1.13.2

Tag URL base: `https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/`
(tag, never a branch). Files are stored byte-for-byte as fetched by `curl -sS --fail`
into this directory; `SHA256SUMS` is `sha256sum` output over them.

| file | path in the tag | sha256 | host counterpart | host match |
|---|---|---|---|---|
| `how-to-type.c` | `tools/how-to-type.c` | `f774882e88f012cb18225db4232c8a8074f7c7a7371c789fca8c27f41c8515bc` | `/usr/lib/xkbcommon/xkbcli-how-to-type` (binary, sha256 `f6c0b122ad90c9e30086653517c51f4b2203b6c7c07bcbc89c71e55ab2927e54`) | source of the installed judge |
| `keysym.c` | `src/keysym.c` | `123e3390d443b85c9cc9d1833c168ecda955d1c642fda03881052bb99c3369c5` | inside `libxkbcommon.so.0.13.2` | not directly comparable (compiled) |
| `keymap.c` | `src/keymap.c` | `bfb95187887e3881a30a4891e681627eaffa9b8403aaa1e1915185b2f279e5bd` | inside `libxkbcommon.so.0.13.2` | not directly comparable (compiled) |
| `keysym.h` | `src/keysym.h` | `1398b750580fed827f4888f9a05e8ad75f2a197dfca7f68506ca506678431949` | none installed (`src/` headers are not packaged) | n/a |
| `xkbcommon.h` | `include/xkbcommon/xkbcommon.h` | `17e58db5edc299d13b4365adce6c6d805e16642977ffaacf98d9be0c4c7071ff` | `/usr/include/xkbcommon/xkbcommon.h` | **byte-identical** (`cmp` exits 0) |
| `xkbcommon-keysyms.h` | `include/xkbcommon/xkbcommon-keysyms.h` | `13023369f65a17411606084e3e09557b4886aeb15f89affba4aaa86490a463f3` | `/usr/include/xkbcommon/xkbcommon-keysyms.h` | **byte-identical** (`cmp` exits 0) |

Host package facts used for the comparison: the installed header pair hashes to the same
digests as the tag files, and `xkbcommon-keysyms.h` matches the digest named in the round-49
C1 brief (`13023369…a463f3`), so the pinned source tree is the source of the host judge.

Full URLs:

```
https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/tools/how-to-type.c
https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/keysym.c
https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/keymap.c
https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/src/keysym.h
https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/include/xkbcommon/xkbcommon.h
https://raw.githubusercontent.com/xkbcommon/libxkbcommon/xkbcommon-1.13.2/include/xkbcommon/xkbcommon-keysyms.h
```

Version corroboration: `src/keymap.c` in this tag carries `xkb_keymap_new_from_rmlvo`,
`xkb_keymap_key_by_name` and a 676-line body (the 1.13 split), and `src/keysym.h` states
`XKB_KEYSYM_COUNT_EXPLICIT 2505`, which equals the number of distinct keysym values measured
in the header (see the report's sufficiency section).
