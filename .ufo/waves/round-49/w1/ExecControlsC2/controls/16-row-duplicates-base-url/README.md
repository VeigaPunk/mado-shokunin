# control 16-row-duplicates-base-url

A new, correctly pinned row for a file the registry already holds at the same commit (S303, S317 carry src/config/legacy/ConfigManager.cpp). c and f pass; g's base_urls loop must refuse it. This is the hazard the real entry hits if it opens a row for the bind parser instead of citing S303/S317.

Expected: MET (g (narrowed by design))
