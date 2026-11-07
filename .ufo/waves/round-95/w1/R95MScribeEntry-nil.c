#include <gio/gio.h>
#include <stdio.h>
int main (void) {
  const char *names[3] = { (const char *) NULL, "zz", "x.txt" };
  for (int i = 0; i < 3; i++) {
    gboolean u = FALSE;
    gchar *t = g_content_type_guess (names[i], NULL, 0, &u);
    printf ("%s\t%d\n", t, u ? 1 : 0);
    g_free (t);
  }
  return 0;
}
