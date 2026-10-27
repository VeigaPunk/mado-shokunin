#include <stdio.h>
#include <string.h>
#include <xkbcommon/xkbcommon.h>

static void name_flags(const char *n) {
    xkb_keysym_t a = xkb_keysym_from_name(n, XKB_KEYSYM_NO_FLAGS);
    xkb_keysym_t b = xkb_keysym_from_name(n, XKB_KEYSYM_CASE_INSENSITIVE);
    char na[64], nb[64];
    xkb_keysym_get_name(a, na, sizeof na); xkb_keysym_get_name(b, nb, sizeof nb);
    printf("from_name %-14s no_flags=0x%04x(%-12s) icase=0x%04x(%s)\n", n, a, na, b, nb);
}

int main(int argc, char **argv) {
    name_flags("q"); name_flags("Q"); name_flags("slash"); name_flags("Slash");
    name_flags("SLASH"); name_flags("Return"); name_flags("nosuchsym");
    if (argc < 2) return 0;
    FILE *f = fopen(argv[1], "r");
    struct xkb_context *ctx = xkb_context_new(XKB_CONTEXT_NO_FLAGS);
    struct xkb_keymap *km = xkb_keymap_new_from_file(ctx, f, XKB_KEYMAP_FORMAT_TEXT_V2, XKB_KEYMAP_COMPILE_NO_FLAGS);
    fclose(f);
    if (!km) { puts("KEYMAP FAIL"); return 1; }
    printf("layouts=%u\n", xkb_keymap_num_layouts(km));
    struct xkb_state *s0 = xkb_state_new(km);  /* zero mods, group 0: Hyprland bind states */
    struct xkb_state *sf = xkb_state_new(km);  /* full state, Mod5+LevelThree like AltGr */
    xkb_mod_mask_t m5 = 1u << xkb_keymap_mod_get_index(km, "Mod5");
    xkb_mod_mask_t l3 = 1u << xkb_keymap_mod_get_index(km, "LevelThree");
    xkb_state_update_mask(sf, m5|l3, 0, 0, 0, 0, 0);
    xkb_keycode_t keys[2] = {24, 97};
    const char *nm[2] = {"AD01", "AB11"};
    for (int i = 0; i < 2; i++) {
        xkb_keysym_t a = xkb_state_key_get_one_sym(s0, keys[i]);
        xkb_keysym_t b = xkb_state_key_get_one_sym(sf, keys[i]);
        char na[64], nb[64];
        xkb_keysym_get_name(a, na, sizeof na); xkb_keysym_get_name(b, nb, sizeof nb);
        printf("key %-4s xkb=%3u zero-mod=0x%04x(%-8s) mod5+levelthree=0x%04x(%s)\n", nm[i], keys[i], a, na, b, nb);
    }
    return 0;
}
