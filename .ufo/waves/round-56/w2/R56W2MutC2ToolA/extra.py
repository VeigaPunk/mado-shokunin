"""Extra killing proposals for the two mutants whose snippets were fixed after the first batch (M86, M100)."""
EXTRA = [
    ("K86", "M86", "a symlink source is followed (stat), not rejected as nonregular (lstat)",
     {"real.conf": b"x = 1\n",
      "lnk.conf": ("symlink", "real.conf"),
      "hyprland.conf": b"source = lnk.conf\n"},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}"]),
    ("K100", "M100", "a `#`-first line in the --getoption dump is NOT skipped: it is bad_json",
     {"hyprland.conf": b"misc:disable_autoreload = 0\n",
      "go.json": b'# comment\n{"option": "misc:disable_autoreload", "int": 0}\n'},
     ["--config", "{FX}/tree/hyprland.conf", "--display-root", "{FX}", "--getoption", "{FX}/tree/go.json"]),
]
