/* round-95 C1 oracle: what the installed GLib answers for g_content_type_guess (name|NULL, data, len, &u).
 * argv: pairs "<0 | =NAME>" "<data file>"; "0" passes filename NULL, "=NAME" passes NAME (bytes after '=').
 * One line per pair: "<type>\t<uncertain>".  Build: cc -O0 oracle.c $(pkg-config --cflags --libs gio-2.0). */
#include <gio/gio.h>
#include <stdio.h>
int main (int argc, char **argv) {
  for (int i = 1; i + 1 < argc; i += 2) {
    gchar *data = NULL; gsize len = 0; gboolean u = FALSE;
    if (!g_file_get_contents (argv[i + 1], &data, &len, NULL)) { fprintf (stderr, "read %s\n", argv[i + 1]); return 2; }
    const char *name = argv[i][0] == '=' ? argv[i] + 1 : NULL;
    gchar *t = g_content_type_guess (name, (const guchar *) data, len, &u);
    printf ("%s\t%d\n", t, u ? 1 : 0);
    g_free (t); g_free (data);
  }
  return 0;
}
