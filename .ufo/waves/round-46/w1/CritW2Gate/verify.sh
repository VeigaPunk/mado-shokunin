#!/bin/sh
# CritW2Gate locator check: every quoted fragment in the report must appear at the
# reported line of the frozen gate. Locators are computed here, never typed.
G=/home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-session-material.py
fail=0
c() {
  n=$(grep -n -F -- "$1" "$G" | head -1 | cut -d: -f1)
  if [ "$n" = "$2" ]; then
    echo "OK   :$2  $1"
  else
    echo "FAIL expect:$2 got:$n  $1"
    fail=1
  fi
}
c 'MAX_TEXT = 16 << 20' 68
c 'MAX_OBJECTS = 20000' 69
c 'PROC_RE = re.compile(r'"'"'users:\(\("[^"]{0,128}",pid=\d+'"'"')' 74
c 'HOME_PATH_RE = re.compile(r'"'"'^/home/[A-Za-z0-9._-]+(?:/[^\s]*)?/?$'"'"')' 75
c 'return _nonempty(obj.get("title")) or _nonempty(obj.get("initialTitle"))' 99
c 'for key in ("description", "make", "model"):' 106
c 'def scan_json_objects(text, all_sub, any_sub, pred, limit=MAX_OBJECTS):' 127
c 'return 0, 0, False' 136
c 'if examined >= limit:' 156
c 'examined += 1' 159
c 'hits += _count_objects(obj, pred)' 166
c 'if not entry or any(ch.isspace() for ch in entry):' 176
c 'if not data or b"\x00" in data[:8192]:' 186
c 'data = data[:MAX_TEXT]' 189
c 'hits, examined, truncated = scan_json_objects(' 208
c 'text, ('"'"'"class"'"'"',), ('"'"'"title"'"'"', '"'"'"initialTitle"'"'"'), _is_client' 209
c 'if hits:' 211
c 'text, ('"'"'"serial"'"'"',), ('"'"'"description"'"'"', '"'"'"make"'"'"', '"'"'"model"'"'"'),' 223
c 'raw = _git(repo, "ls-tree", "-r", "-z", sha, "--", ".ufo")' 256
[ "$fail" = 0 ] && echo "VERIFY: all locators match"
exit "$fail"
