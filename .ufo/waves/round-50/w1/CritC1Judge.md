# CritC1Judge — frozen C1 judge attack

Status: blocked before counter execution by the mandated per-file limit: shallow-fetching commit `13631f24050f22db92bf5bd33e0f4d014192992e` under `/fast/scratch/hyaku/mado-r50/CritC1Judge/` failed `fatal: write error: File too large` / `fatal: fetch-pack: invalid index-pack output`. No judge verdict/digest outcomes are claimed. Counter object is available read-only from lane and hashes to `2597c204abf1e9e7c625d98cf83f0b340a0d82897da4986c550e35c5dff5db62`.

## Static attack surface (frozen counter source)

`quality/counters/c1-r49-keysym.py` at the requested frozen revision:
- compile subprocess env is a fresh allowlist (`PATH=/usr/bin`, work-local `HOME`, `XDG_CONFIG_HOME`, `LC_ALL=C`) and stdin is `DEVNULL` (`:414-423`); xkbcli how-to-type uses same env and stdin `DEVNULL` (`:462-468`). Thus caller XKB_CONFIG_ROOT, XKB_CONFIG_EXTRA_PATH, XKB_DEFAULT_*, LANG/LC_ALL and piped stdin are not inherited by those child processes.
- guarded compile passes `--include=/usr/share/xkeyboard-config-2`; reference compile uses default search with a fresh empty home (`:430-454`). It does not pass `--include` to the reference compile. It checks reference HOME emptiness and equality with guarded bytes.
- Work dir filesystem identity is not checked; only path exclusions/containment and TMPDIR exclusions (`:772-786`).
- This static evidence does not establish runtime verdict/digest invariance. A planted `$HOME/.config/xkb` test requires running with controlled HOME; the judge's HOME is always under its work directory, not caller HOME. Counter creates its own work subtree.

No tools installed/updated.
