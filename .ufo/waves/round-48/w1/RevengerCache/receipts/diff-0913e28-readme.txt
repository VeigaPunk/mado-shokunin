commit 0913e283d2d396bc87718438969a70ff6528b0ae
Author: Vladimir-csp <4061903+Vladimir-csp@users.noreply.github.com>
Date:   Tue Jun 11 23:58:06 2024 +0300

    Enable cache by default, closes #36

diff --git a/README.md b/README.md
index 9e9faa0..1d613d7 100644
--- a/README.md
+++ b/README.md
@@ -158,9 +158,9 @@ feeding `md5sum` the value of `$XDG_CURRENT_DESKTOP` and output of `ls -LRl` for
 all possible config file and data dir paths in one go. Valid cache bypasses
 reading of any other file.
 
-Currentry this feature is disabled by default and can be controlled by first
-encountered `/enable_cache`|`/disable_cache` direcive in the configs or
-`XTE_CACHE_ENABLED` env var (truthy or falsy value, has priority).
+This feature is enabled by default and can be controlled by first encountered
+`/enable_cache`|`/disable_cache` direcive in the configs or `XTE_CACHE_ENABLED`
+env var (truthy or falsy value, has priority).
 
 Unless `XTE_CACHE_ENABLED` is false, an attempt at reading the cache file is
 always performed though. Its existence translates into initial assumption about
@@ -174,5 +174,3 @@ and the var was later removed, the script will not know that the cache is
 disabled until one of three things happens: cache file is removed, something
 invalidates it (like touching/editing a config/entry), or a run with falsy
 `XTE_CACHE_ENABLED` is performed.
-
-The plan is to eventually enable it by default for unattended fastness.
commit 0913e283d2d396bc87718438969a70ff6528b0ae
Author: Vladimir-csp <4061903+Vladimir-csp@users.noreply.github.com>
Date:   Tue Jun 11 23:58:06 2024 +0300

    Enable cache by default, closes #36

diff --git a/xdg-terminal-exec b/xdg-terminal-exec
index e4d730d..d2064fa 100755
--- a/xdg-terminal-exec
+++ b/xdg-terminal-exec
@@ -563,7 +563,7 @@ make_paths
 # so just try reading it as if default is true, otherwise do the usual thing.
 # Editing config to disable cache should invalidate the cache.
 # The true default is false though:
-CACHE_ENABLED=${XTE_CACHE_ENABLED-false}
+CACHE_ENABLED=${XTE_CACHE_ENABLED-true}
 
 # HASH can be reused
 HASH=''
