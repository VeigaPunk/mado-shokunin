/* Probe the installed GLib 2.90.1 for the exact GKeyFile / D-Bus-name rules
 * that xdg-desktop-portal 1.22.1 inherits. Read-only; prints T## PASS/FAIL. */
#include <glib.h>
#include <gio/gio.h>
#include <string.h>
#include <stdio.h>
#include <locale.h>

static int fails = 0;

static void
chk (int id, gboolean cond, const char *note)
{
  if (!cond)
    {
      fails++;
      printf ("T%02d FAIL %s\n", id, note);
    }
  else
    printf ("T%02d ok   %s\n", id, note);
}

static GKeyFile *
load (const char *text, gboolean *ok)
{
  GKeyFile *kf = g_key_file_new ();
  GError *err = NULL;
  g_key_file_load_from_data (kf, text, strlen (text), G_KEY_FILE_NONE, &err);
  *ok = (err == NULL);
  if (err) g_error_free (err);
  return kf;
}

int
main (void)
{
  gboolean ok;
  GKeyFile *kf;
  GError *err = NULL;
  gchar **keys, **list;
  gsize n;
  char big[300];

  g_setenv ("LC_ALL", "C", TRUE);
  setlocale (LC_ALL, "C");

  /* T01 key containing ']' voids the file */
  kf = load ("[preferred]\nbad]key=x\n", &ok);
  chk (1, !ok, "key 'bad]key' must void file");
  g_key_file_unref (kf);

  /* T02 Encoding=ISOLatin1 in start group voids the file */
  kf = load ("[portal]\nEncoding=ISOLatin1\nDBusName=org.a.b\n", &ok);
  chk (2, !ok, "Encoding=ISOLatin1 in first group must void file");
  g_key_file_unref (kf);

  /* T03/T04 Encoding=UTF-8 / utf-8 accepted */
  kf = load ("[portal]\nEncoding=UTF-8\nDBusName=org.a.b\n", &ok);
  chk (3, ok, "Encoding=UTF-8 accepted");
  g_key_file_unref (kf);
  kf = load ("[portal]\nEncoding=utf-8\nDBusName=org.a.b\n", &ok);
  chk (4, ok, "Encoding=utf-8 accepted");
  g_key_file_unref (kf);

  /* T05 Encoding in a NON-first group ignored */
  kf = load ("[other]\nEncoding=ISOLatin1\n[portal]\nDBusName=org.a.b\n", &ok);
  chk (5, ok, "Encoding in non-start group ignored");
  g_key_file_unref (kf);

  /* T06 group name keeps inner spaces */
  kf = load ("[ preferred ]\ndefault=kde\n", &ok);
  chk (6, ok, "'[ preferred ]' loads");
  if (ok)
    {
      keys = g_key_file_get_keys (kf, " preferred ", &n, NULL);
      chk (6, keys != NULL, "group name is ' preferred ' (untrimmed)");
      g_strfreev (keys);
      keys = g_key_file_get_keys (kf, "preferred", &n, NULL);
      chk (6, keys == NULL, "untrimmed group is not 'preferred'");
      g_strfreev (keys);
    }
  g_key_file_unref (kf);

  /* T07 key before group voids file */
  kf = load ("default=kde\n", &ok);
  chk (7, !ok, "key before group voids file");
  g_key_file_unref (kf);

  /* T08 value leading whitespace chomped, trailing kept */
  kf = load ("[preferred]\ndefault= \t kde \n", &ok);
  chk (8, ok, "'default= \\t kde ' loads");
  if (ok)
    {
      gchar *v = g_key_file_get_string (kf, "preferred", "default", NULL);
      chk (8, v && strcmp (v, "kde ") == 0, "value is 'kde ' (leading chomped, trailing kept)");
      g_free (v);
    }
  g_key_file_unref (kf);

  /* T09 trailing empty list element dropped, middles kept */
  kf = load ("[preferred]\ndefault=a;b;\nx=a;;b\ny=;\n", &ok);
  chk (9, ok, "list file loads");
  if (ok)
    {
      list = g_key_file_get_string_list (kf, "preferred", "default", &n, NULL);
      chk (9, list && n == 1 && !strcmp (list[0], "a"), "'a;b;' -> {a}");
      g_strfreev (list);
      list = g_key_file_get_string_list (kf, "preferred", "x", &n, NULL);
      chk (9, list && n == 3 && !list[1][0] && !strcmp (list[2], "b"), "'a;;b' -> {a,'',b}");
      g_strfreev (list);
      list = g_key_file_get_string_list (kf, "preferred", "y", &n, NULL);
      chk (9, list && n == 1 && !list[0][0], "';' -> {''}");
      g_strfreev (list);
    }
  g_key_file_unref (kf);

  /* T10 escaped separator valid in lists, invalid in scalar */
  kf = load ("[preferred]\ndefault=a\\;b\n", &ok);
  chk (10, ok, "escaped separator file loads");
  if (ok)
    {
      list = g_key_file_get_string_list (kf, "preferred", "default", &n, NULL);
      chk (10, list && n == 1 && !strcmp (list[0], "a;b"), "list {a;b}");
      g_strfreev (list);
      err = NULL;
      gchar *v = g_key_file_get_string (kf, "preferred", "default", &err);
      chk (10, v == NULL && err != NULL, "scalar get_string errors on \\;");
      g_free (v); g_clear_error (&err);
    }
  g_key_file_unref (kf);

  /* T11 invalid escape voids list and scalar */
  kf = load ("[preferred]\ndefault=a\\q\n", &ok);
  chk (11, ok, "raw line with \\q parses at load time");
  if (ok)
    {
      err = NULL;
      list = g_key_file_get_string_list (kf, "preferred", "default", &n, &err);
      chk (11, list == NULL && err != NULL, "get_string_list errors on \\q");
      g_clear_error (&err);
      err = NULL;
      gchar *v = g_key_file_get_string (kf, "preferred", "default", &err);
      chk (11, v == NULL && err != NULL, "get_string errors on \\q");
      g_clear_error (&err);
    }
  g_key_file_unref (kf);

  /* T12 bad UseIn does NOT void the file at load; scalar keys stay good */
  kf = load ("[portal]\nDBusName=org.a.b\nInterfaces=org.freedesktop.impl.portal.X\nUseIn=gnome;\\q\n", &ok);
  chk (12, ok, "bad escape in UseIn does not fail load_from_file");
  if (ok)
    {
      err = NULL;
      list = g_key_file_get_string_list (kf, "portal", "UseIn", &n, &err);
      chk (12, list == NULL, "UseIn getter returns NULL");
      g_clear_error (&err);
      gchar *v = g_key_file_get_string (kf, "portal", "DBusName", NULL);
      chk (12, v && !strcmp (v, "org.a.b"), "DBusName still readable");
      g_free (v);
    }
  g_key_file_unref (kf);

  /* T13 locale key [de] dropped in C locale, [C] kept under raw name */
  kf = load ("[preferred]\ndefault[de]=kde\nplain=1\n", &ok);
  chk (13, ok, "locale file loads");
  if (ok)
    {
      keys = g_key_file_get_keys (kf, "preferred", &n, NULL);
      chk (13, keys && n == 1 && !strcmp (keys[0], "plain"), "default[de] dropped in C locale");
      g_strfreev (keys);
    }
  g_key_file_unref (kf);
  kf = load ("[preferred]\ndefault[C]=kde\ndefault=gtk\n", &ok);
  chk (13, ok, "default[C] file loads");
  if (ok)
    {
      keys = g_key_file_get_keys (kf, "preferred", &n, NULL);
      chk (13, keys && n == 2, "default[C] and default both stored raw");
      g_strfreev (keys);
    }
  g_key_file_unref (kf);

  /* T14 inner spaces in keys accepted; tab inner accepted */
  kf = load ("[preferred]\nmy key=x\nmy\tkey=y\n", &ok);
  chk (14, ok, "inner space/tab keys accepted");
  g_key_file_unref (kf);

  /* T15 junk after ']' voids the file */
  kf = load ("[preferred] junk\ndefault=kde\n", &ok);
  chk (15, !ok, "'[preferred] junk' must void file");
  g_key_file_unref (kf);

  /* T16 spaces/tabs after ']' tolerated */
  kf = load ("[preferred] \t\ndefault=kde\n", &ok);
  chk (16, ok, "trailing blanks after group tolerated");
  g_key_file_unref (kf);

  /* T17 CRLF tolerated */
  kf = load ("[preferred]\r\ndefault=kde\r\n", &ok);
  chk (17, ok, "CRLF loads");
  if (ok)
    {
      gchar *v = g_key_file_get_string (kf, "preferred", "default", NULL);
      chk (17, v && !strcmp (v, "kde"), "CRLF value clean");
      g_free (v);
    }
  g_key_file_unref (kf);

  /* T18 empty key ('=v') voids file */
  kf = load ("[preferred]\n=kde\n", &ok);
  chk (18, !ok, "'=kde' voids file");
  g_key_file_unref (kf);

  /* T19 locale-only preferred group still yields an (empty) config object */
  kf = load ("[preferred]\na[de]=x\n", &ok);
  chk (19, ok, "locale-only preferred loads");
  if (ok)
    {
      keys = g_key_file_get_keys (kf, "preferred", &n, NULL);
      chk (19, keys != NULL && n == 0, "get_keys returns EMPTY non-NULL");
      g_strfreev (keys);
    }
  g_key_file_unref (kf);

  /* T20 duplicate key: last value wins in the map */
  kf = load ("[preferred]\ndefault=a\ndefault=b\n", &ok);
  chk (20, ok, "duplicate key loads");
  if (ok)
    {
      gchar *v = g_key_file_get_string (kf, "preferred", "default", NULL);
      chk (20, v && !strcmp (v, "b"), "duplicate key: last value wins");
      g_free (v);
    }
  g_key_file_unref (kf);

  /* T21 bus names */
  chk (21,  g_dbus_is_name (":1.2"), "':1.2' valid");
  chk (21, !g_dbus_is_name ("org.1a"), "'org.1a' invalid (digit after dot)");
  chk (21,  g_dbus_is_name ("org.-a.b-1"), "'org.-a.b-1' valid (hyphen ok)");
  chk (21, !g_dbus_is_name ("org.a..b"), "'org.a..b' invalid");
  chk (21, !g_dbus_is_name ("org.a.b;"), "'org.a.b;' invalid");
  memset (big, 'a', 253); big[253] = '.'; big[254] = 'b'; big[255] = 0;
  chk (21,  g_dbus_is_name (big), "255-byte name valid");
  memset (big, 'a', 254); big[254] = '.'; big[255] = 'b'; big[256] = 0;
  chk (21, !g_dbus_is_name (big), "256-byte name invalid");

  /* T22 interface names */
  chk (22,  g_dbus_is_interface_name ("org.a.B_c1"), "iface with digits/underscore valid");
  chk (22, !g_dbus_is_interface_name ("org.a.b-c"), "iface with hyphen invalid");
  chk (22, !g_dbus_is_interface_name ("org.1a"), "iface digit element invalid");

  /* T23 g_strsplit keeps empty elements */
  list = g_strsplit ("a::b", ":", 0);
  chk (23, g_strv_length (list) == 3 && !list[1][0], "g_strsplit keeps empty middle");
  g_strfreev (list);

  /* T24 tab-prefixed value chomped */
  kf = load ("[preferred]\ndefault=\tkde\n", &ok);
  chk (24, ok, "tab after = ok");
  if (ok)
    {
      gchar *v = g_key_file_get_string (kf, "preferred", "default", NULL);
      chk (24, v && !strcmp (v, "kde"), "value leading tab chomped");
      g_free (v);
    }
  g_key_file_unref (kf);

  printf ("PROBE done fails=%d\n", fails);
  return fails ? 1 : 0;
}
