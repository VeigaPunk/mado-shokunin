#!/bin/sh
# ExecJournalFormat (mado round 41, w1) - read-only reproduction of the journal
# output-format census.  Writes only into $OUT (default: a fresh mktemp dir).
# Uses only read-only journalctl verbs: --user -u <unit> --no-pager -o FORMAT
# [-b N | --since D | --until D | --no-hostname].  No compositor/socket access.
set -u
LANE=/home/vgpnk/Projects/shokunin/mado-shokunin
REF="$LANE/.ufo/waves/round-41/c1/ctl-ref-tool.py.txt"
COUNTER="$LANE/quality/counters/c1-r41-globals.py"
UNIT=xdg-desktop-portal-hyprland
OUT=${1:-$(mktemp -d)}
mkdir -p "$OUT"
cp "$REF" "$OUT/ref.py"
chmod +x "$OUT/ref.py"

echo "journalctl --version: $(journalctl --version | head -1)"
echo "hyprctl version: $(hyprctl version | head -1)"

for f in short short-iso short-iso-precise short-full cat json; do
    journalctl --user -u "$UNIT" --no-pager -o "$f" > "$OUT/cap-$f.txt"
    journalctl --user -u "$UNIT" --no-pager -o "$f" --since 2030-01-01 > "$OUT/empty-$f.txt"
done
journalctl --user -u "$UNIT" --no-pager -o short-iso --no-hostname > "$OUT/cap-nohost.txt"
journalctl --user -u "$UNIT" --no-pager -o short-iso -b 0 > "$OUT/b0.txt"
journalctl --user -u "$UNIT" --no-pager -o short-iso -b -1 > "$OUT/bm1.txt"
journalctl --user -u "$UNIT" --no-pager -o short-iso --since 2020-01-01 > "$OUT/since2020.txt"
journalctl --user -u "$UNIT" --no-pager -o short-iso --until 2020-01-01 > "$OUT/until2020.txt"

for f in short short-iso short-iso-precise short-full cat json nohost; do
    n=$(grep -c 'Got interface:' "$OUT/cap-$f.txt")
    two=$(grep -c '\[LOG\]  | Got interface:' "$OUT/cap-$f.txt")
    one=$(grep -c '\[LOG\] | Got interface:' "$OUT/cap-$f.txt")
    tsp=$(grep -c ' $' "$OUT/cap-$f.txt")
    cr=$(grep -c "$(printf '\r')" "$OUT/cap-$f.txt")
    "$OUT/ref.py" --journal-file "$OUT/cap-$f.txt" > "$OUT/ref-$f.out" 2>&1
    rc=$?
    printf '%-18s adverts=%-3s two_space=%-3s one_space=%-2s trailing_sp=%-2s cr=%-2s ref_rc=%-2s ref_last=%s\n' \
        "$f" "$n" "$two" "$one" "$tsp" "$cr" "$rc" "$(tail -1 "$OUT/ref-$f.out" | cut -c1-150)"
done

for f in short short-iso short-iso-precise short-full cat json; do
    printf '%-18s empty_last=%s\n' "$f" "$(tr '\n' '|' < "$OUT/empty-$f.txt")"
done

for x in b0 bm1 since2020 until2020; do
    "$OUT/ref.py" --journal-file "$OUT/$x.txt" > "$OUT/ref-$x.out" 2>&1
    printf '%-10s rc=%s lines=%s bootlines=%s last=%s\n' "$x" "$?" \
        "$(wc -l < "$OUT/$x.txt")" "$(grep -c -- '^-- Boot' "$OUT/$x.txt")" \
        "$(tail -1 "$OUT/ref-$x.out" | cut -c1-120)"
done

for x in b0 bm1; do
    "$OUT/ref.py" --journal-file "$OUT/$x.txt" --diff > "$OUT/ref-$x-diff.out" 2>&1
    printf '%-10s --diff rc=%s %s\n' "$x" "$?" "$(grep DIFF "$OUT/ref-$x-diff.out")"
done

echo '-- probe: a journalctl-style header line injected into a short-iso copy'
{ echo '-- Journal begins at Sat 2026-10-24 20:57:12 -03, ends at Sun 2026-10-25 19:59:32 -03. --'; cat "$OUT/cap-short-iso.txt"; } > "$OUT/inject-iso.txt"
{ echo '-- Journal begins at Sat 2026-10-24 20:57:12 -03. --'; cat "$OUT/cap-short-iso.txt"; } > "$OUT/inject-iso2.txt"
for x in inject-iso inject-iso2; do
    "$OUT/ref.py" --journal-file "$OUT/$x.txt" > "$OUT/ref-$x.out" 2>&1
    printf '%-12s rc=%s last=%s\n' "$x" "$?" "$(tail -1 "$OUT/ref-$x.out" | cut -c1-90)"
done

echo '-- probe: short + short-iso concatenated (mixed shapes in one file)'
cat "$OUT/cap-short.txt" "$OUT/cap-short-iso.txt" > "$OUT/mixed.txt"
"$OUT/ref.py" --journal-file "$OUT/mixed.txt" > "$OUT/ref-mixed.out" 2>&1
printf 'mixed rc=%s adverts=%s last=%s\n' "$?" "$(grep -c 'Got interface:' "$OUT/mixed.txt")" \
    "$(tail -1 "$OUT/ref-mixed.out" | cut -c1-90)"
echo '-- mixed report vs short-iso-only report (expect: only the session-1 boot= field differs)'
diff "$OUT/ref-short-iso.out" "$OUT/ref-mixed.out" | cut -c1-170
echo '-- stderr sizes on the two rc-3 runs (a non-empty advert file vs a genuinely empty one)'
"$OUT/ref.py" --journal-file "$OUT/cap-short.txt" >/dev/null 2> "$OUT/e-short.err"; echo "cap-short rc=$? stderr_bytes=$(wc -c < "$OUT/e-short.err")"
"$OUT/ref.py" --journal-file "$OUT/empty-short-iso.txt" >/dev/null 2> "$OUT/e-empty.err"; echo "empty-short-iso rc=$? stderr_bytes=$(wc -c < "$OUT/e-empty.err")"

echo '-- probe: --live through a wrapper that reformats to -o short'
printf '#!/bin/sh\nexec cat %s/cap-short.txt\n' "$OUT" > "$OUT/wrap-short.sh"
chmod 755 "$OUT/wrap-short.sh"
"$OUT/ref.py" --live --journalctl "$OUT/wrap-short.sh" > "$OUT/ref-livewrap.out" 2>&1
printf 'livewrap rc=%s last=%s\n' "$?" "$(tail -1 "$OUT/ref-livewrap.out" | cut -c1-90)"

echo '-- the counter judge model on the same captures (model_out from c1-r41-globals.py)'
python3 - "$COUNTER" "$OUT" <<'PY'
import importlib.util, pathlib, sys
p, out = sys.argv[1], pathlib.Path(sys.argv[2])
spec = importlib.util.spec_from_file_location("c1", p)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
for f in ["short", "short-iso", "short-iso-precise", "short-full", "cat", "json", "nohost"]:
    t = (out / ("cap-%s.txt" % f)).read_text(errors="replace")
    o, rc = m.model_out(t, [], False)
    print("%-18s model_rc=%s sessions=%d last=%s" % (f, rc, len(m.model_sessions(t)), o.splitlines()[-1][:110]))
PY

echo '-- sha256 of the captures'
sha256sum "$OUT"/cap-*.txt "$OUT"/empty-*.txt "$OUT"/b0.txt "$OUT"/bm1.txt "$OUT"/since2020.txt "$OUT"/until2020.txt
echo "OUT=$OUT"
