/* Round-94 C1 oracle: the installed GLib's filename-only content-type guess.
 * For each argv name (raw bytes) prints "<type>\t<uncertain 0|1>" on its own line.
 * Reads XDG_DATA_HOME / XDG_DATA_DIRS from the environment exactly as GLib does. */
#include <gio/gio.h>
#include <stdio.h>
int main(int argc, char **argv) {
  for (int i = 1; i < argc; i++) {
    gboolean unc = FALSE;
    gchar *t = g_content_type_guess(argv[i], NULL, 0, &unc);
    printf("%s\t%d\n", t, unc ? 1 : 0);
    g_free(t);
  }
  return 0;
}
