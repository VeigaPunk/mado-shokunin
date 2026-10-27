#include <stdio.h>
#include <string.h>
#include <xkbcommon/xkbcommon.h>

int main(int argc, char **argv) {
    if (argc < 2) return 2;
    FILE *f = fopen(argv[1], "r");
    struct xkb_context *ctx = xkb_context_new(XKB_CONTEXT_NO_FLAGS);
    struct xkb_keymap *km = xkb_keymap_new_from_file(ctx, f, XKB_KEYMAP_FORMAT_TEXT_V2, XKB_KEYMAP_COMPILE_NO_FLAGS);
    fclose(f);
    if (!km) { fprintf(stderr, "keymap fail\n"); return 1; }
    struct xkb_state *st = xkb_state_new(km);
    char line[256];
    while (fgets(line, sizeof line, stdin)) {
        line[strcspn(line, "\r\n")] = 0;
        if (!*line) continue;
        xkb_keysym_t a = xkb_keysym_from_name(line, XKB_KEYSYM_NO_FLAGS);
        xkb_keysym_t b = xkb_keysym_from_name(line, XKB_KEYSYM_CASE_INSENSITIVE);
        printf("%s exact=0x%04x icase=0x%04x keys=", line, a, b);
        int n = 0;
        for (xkb_keycode_t kc = xkb_keymap_min_keycode(km); kc <= xkb_keymap_max_keycode(km); kc++) {
            xkb_keysym_t s = xkb_state_key_get_one_sym(st, kc);
            if (s == XKB_KEY_NoSymbol) continue;
            if ((a && s == a) || (b && s == b)) {
                const char *kn = xkb_keymap_key_get_name(km, kc);
                printf("%s%s(%u)", n ? "," : "", kn ? kn : "?", kc); n++;
            }
        }
        printf("%s\n", n ? "" : "NONE");
    }
    return 0;
}
