#!/usr/bin/env bash
# mado round 51, w1, seat ExecFetchDispatch — commit-pinned fetch of the Hyprland
# 0.56.2 dispatcher-execution surface (C2: keybind dispatcher string -> m_dispatchers).
#
# Pins are byte-identical git blobs of the pinned commits, fetched over
# raw.githubusercontent.com with curl -fsSL and verified two ways:
#   1. git blob sha1 recomputed from the fetched bytes must equal the tree's blob id
#      at the pinned revision (commit binding, not just transport success);
#   2. sha256 recorded in SHA256SUMS / fetch-manifest.json for the pin manifest.
#
# SHA256SUMS never digests itself: there is no self row (M50-9 / D4 rule).
#
# Usage: fetch-all.sh --out <dir> [--scratch <dir>]
#   --out      where the pin files, SHA256SUMS and fetch-manifest.json land
#   --scratch  staging dir (default: mktemp -d under $TMPDIR, else /tmp); removed on exit
set -euo pipefail

OUT=""
SCRATCH=""
while [ $# -gt 0 ]; do
    case "$1" in
        --out)     OUT="${2:?--out needs a dir}"; shift 2 ;;
        --scratch) SCRATCH="${2:?--scratch needs a dir}"; shift 2 ;;
        -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
        *) echo "unknown arg: $1" >&2; exit 2 ;;
    esac
done
[ -n "$OUT" ] || { echo "fetch-all.sh: --out is required" >&2; exit 2; }

HYPR_REV=efb50993780079460b0cbed1363e2166a2de1d9f
WIKI_REV=d5f07c60e16fe03744aabb76e492117b7f7c4679
# hyprutils: Hyprland links it via pkg-config (>=0.14.0, CMakeLists.txt:150), so the
# commit is not derivable from the Hyprland pin. Pinned at tag v0.14.2 — the version
# installed on this host (hyprutils 0.14.2-1) — resolved to commit a21e87b8.
HU_REV=a21e87b878e72ee5dfd375899e8b2ad0d0c4c0e1
HU_TAG=v0.14.2
HYPR_URL="https://raw.githubusercontent.com/hyprwm/Hyprland/$HYPR_REV"
HU_URL="https://raw.githubusercontent.com/hyprwm/hyprutils/$HU_REV"
WIKI_URL="https://raw.githubusercontent.com/hyprwm/hyprland-wiki/$WIKI_REV"

# file | repo | url | blob sha1 at the pinned revision
PINS=$(cat <<'EOF'
Hyprland-KeybindManager.cpp	Hyprland	src/managers/KeybindManager.cpp	4ab407ecda7570f189ec22f7629f4358b25b399f
Hyprland-KeybindManager.hpp	Hyprland	src/managers/KeybindManager.hpp	7aa01121c245a0ca2f187bc0b4c0c4edba4cf5de
Hyprland-legacy-DispatcherTranslator.cpp	Hyprland	src/config/legacy/DispatcherTranslator.cpp	b534fec35801707063a902ef0eeebcd3826b26c9
Hyprland-legacy-DispatcherTranslator.hpp	Hyprland	src/config/legacy/DispatcherTranslator.hpp	18978f798b5f92940732e1ea0e2cadb826e2ea26
Hyprland-legacy-ConfigManager.cpp	Hyprland	src/config/legacy/ConfigManager.cpp	4f1b11f25f227cca2a3e5b16c8de760b76231bf5
Hyprland-ConfigManager.cpp	Hyprland	src/config/ConfigManager.cpp	74010df87ee169aeb756fffda17882e769a44783
Hyprland-ConfigManager.hpp	Hyprland	src/config/ConfigManager.hpp	c5a8390a9655d3708c45aa08fec07aa214115373
Hyprland-ConfigActions.cpp	Hyprland	src/config/shared/actions/ConfigActions.cpp	cf38816790e4151ea51b58d352291da248e079b4
Hyprland-ConfigActions.hpp	Hyprland	src/config/shared/actions/ConfigActions.hpp	9519245816ef3075f6087b854e2330c2e05e9b68
Hyprland-HyprCtl.cpp	Hyprland	src/debug/HyprCtl.cpp	060e25b096e682770e4be64a4e1570f355ce72b3
Hyprland-docs-hyprctl.1.rst	Hyprland	docs/hyprctl.1.rst	7b8868cc1467afee9356f2817ca637f030a9f37d
Hyprland-SharedDefs.hpp	Hyprland	src/SharedDefs.hpp	bb7c601e3b299623f433bf809759f57050eb4c9f
Hyprutils-VarList.hpp	Hyprutils	include/hyprutils/string/VarList.hpp	21c76f8020abe5e1b9036abd9466ff90f69cb5fb
Hyprutils-VarList.cpp	Hyprutils	src/string/VarList.cpp	48508ba80e20a79a5881555dcb2ca53755a85aac
Hyprutils-VarList2.hpp	Hyprutils	include/hyprutils/string/VarList2.hpp	db3c43753dae3c12721e86ff0b50894fad7ce63f
Hyprutils-VarList2.cpp	Hyprutils	src/string/VarList2.cpp	473469483cf44e9786b1b5d63b7866a385202c5e
wiki-Dispatchers.md	wiki	content/Configuring/Basics/Dispatchers.md	21e9dd0eb547556e6e24ee7eb4e25f73d19654b7
wiki-Binds.md	wiki	content/Configuring/Basics/Binds.md	0ebce492ee4808176e9d0872e188a1ac2c9b0b90
wiki-Using-hyprctl.md	wiki	content/Configuring/Advanced%20and%20Cool/Using-hyprctl.md	32e2983dc7535737d8388881dfd7b4b2f1fd5e27
EOF
)

mkdir -p "$OUT"
OUT=$(cd "$OUT" && pwd)

CLEAN_SCRATCH=0
if [ -z "$SCRATCH" ]; then
    SCRATCH=$(mktemp -d "${TMPDIR:-/tmp}/mado-r51-fetch.XXXXXX")
    CLEAN_SCRATCH=1
fi
mkdir -p "$SCRATCH"
SCRATCH=$(cd "$SCRATCH" && pwd)
cleanup() { [ "$CLEAN_SCRATCH" = 1 ] && rm -rf "$SCRATCH"; return 0; }
trap cleanup EXIT

TSV="$SCRATCH/pins.tsv"
: > "$TSV"

while IFS=$'\t' read -r file repo path blob; do
    [ -n "$file" ] || continue
    case "$repo" in
        Hyprland) base="$HYPR_URL"; rev="$HYPR_REV" ;;
        Hyprutils) base="$HU_URL"; rev="$HU_REV" ;;
        wiki)     base="$WIKI_URL"; rev="$WIKI_REV" ;;
        *) echo "unknown repo: $repo" >&2; exit 3 ;;
    esac
    url="$base/$path"
    stage="$SCRATCH/$file"
    code=$(curl -fsSL --max-time 90 --retry 2 --retry-delay 1 \
                -A 'mado-r51-fetch/1' -w '%{http_code}' -o "$stage" "$url") || {
        echo "FETCH FAILED: $url" >&2; exit 4; }
    [ "$code" = "200" ] || { echo "HTTP $code for $url" >&2; exit 4; }
    [ -s "$stage" ] || { echo "empty body for $url" >&2; exit 4; }

    got=$(python3 - "$stage" <<'PY'
import hashlib, sys
data = open(sys.argv[1], 'rb').read()
print(hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest())
PY
)
    if [ "$got" != "$blob" ]; then
        echo "BLOB MISMATCH $file: tree=$blob fetched=$got ($url)" >&2; exit 5
    fi
    cp "$stage" "$OUT/$file"
    bytes=$(wc -c < "$OUT/$file")
    sha=$(sha256sum "$OUT/$file" | cut -d' ' -f1)
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$file" "$repo" "$rev" "$url" "$bytes" "$sha" "$blob" >> "$TSV"
    printf 'OK  %-44s %8s B  sha256=%s  blob=%s\n' "$file" "$bytes" "$sha" "$blob"
done <<< "$PINS"

# SHA256SUMS over the pins only — never a self row.
awk -F'\t' '{print $6"  "$1}' "$TSV" | LC_ALL=C sort -k2 > "$OUT/SHA256SUMS"
if grep -q ' SHA256SUMS$' "$OUT/SHA256SUMS"; then
    echo "SHA256SUMS contains a self row (M50-9 violation)" >&2; exit 6
fi
( cd "$OUT" && sha256sum -c --quiet SHA256SUMS ) || { echo "SHA256SUMS check failed" >&2; exit 7; }

python3 - "$TSV" "$OUT/fetch-manifest.json" <<'PY'
import json, sys, datetime
tsv, out = sys.argv[1], sys.argv[2]
files = []
for line in open(tsv, encoding='utf-8'):
    line = line.rstrip('\n')
    if not line:
        continue
    f, repo, rev, url, b, sha, blob = line.split('\t')
    files.append({
        "file": f, "repo": repo, "revision": rev, "url": url,
        "bytes": int(b), "sha256": sha,
        "git_blob_sha1": blob, "blob_verified": True, "http_status": 200,
    })
man = {
    "round": 51, "wave": "w1", "seat": "ExecFetchDispatch",
    "claim": "C2 — Hyprland 0.56.2 dispatcher dispatch surface",
    "fetched": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    "transport": "curl -fsSL https://raw.githubusercontent.com only",
    "hyprland_revision": "efb50993780079460b0cbed1363e2166a2de1d9f",
    "wiki_revision": "d5f07c60e16fe03744aabb76e492117b7f7c4679",
    "hyprutils_revision": "a21e87b878e72ee5dfd375899e8b2ad0d0c4c0e1",
    "hyprutils_tag": "v0.14.2 (host-installed version; Hyprland links hyprutils via pkg-config >=0.14.0, not a submodule)",
    "integrity": "git blob sha1 recomputed from fetched bytes equals the pinned tree blob id; sha256 in this manifest and in SHA256SUMS",
    "sums_self_row": "none — SHA256SUMS digests pins only (M50-9/D4 rule)",
    "files": files,
}
json.dump(man, open(out, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
open(out, 'a', encoding='utf-8').write('\n')
print(f"manifest: {out} ({len(files)} files)")
PY

echo "pins written to $OUT"
