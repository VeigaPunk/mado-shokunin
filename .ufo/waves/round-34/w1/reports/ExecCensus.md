# ExecCensus — mado source census (round 34, wave 1)

Scoped run: census `validate` for lane `mado` plus registry row count. `corpus/SOURCES.md` unmodified.

## Command + receipt

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
```

- Exit code: `0` (pass; warnings only)
- Full receipt (stdout + stderr + code): `.ufo/waves/round-34/scratch/ExecCensus/census.txt`
- stderr: empty

## Census output

8 lines, all on stdout:

```
mado	W04	S030 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S042 duplicate url wayland.freedesktop.org/extras.html across scopes
mado	W04	S045 duplicate url wiki.hypr.land/Configuring/Basics/Window-Rules across scopes
mado	W04	S097 duplicate url raw.githubusercontent.com/basecamp/omarchy/v3.8.4/themes/matte-black/colors.toml across scopes
mado	W04	S119 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Lib/imaplib.py across scopes
mado	W04	S120 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	W04	S121 duplicate url raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/executionmodel.rst across scopes
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
```

7× W04 (duplicate URL reused across distinct scopes/rows) — advisory, not blocking; the validator still emitted `ok`.

## Registry row count

Literal command as dispatched:

```
grep -cE '^\|[[:space:]]*S[0-9](3,)[[:space:]]*\|' corpus/SOURCES.md
```

- Result: `0`, grep exit `1`

The dispatched pattern is ERE, so `(3,)` is a literal parenthesized string, not the `{3,}` quantifier — it cannot match `S001`. Re-run with the intended brace quantifier:

```
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
```

- Result: `192`, grep exit `0`

Sanity: registry IDs run S001–S202; 192 ID rows counted — residual 10-ID gap is skipped numbers / non-ID table rows, consistent with an append-only register.

## Findings

- Census green for mado (exit 0); only W04 duplicate-URL advisories, listed above for whoever adjudicates scope-dedup.
- Dispatch command's grep pattern has an ERE literal-vs-quantifier defect: `(3,)` should read `{3,}`. Verbatim count is 0 (rc=1); corrected count is 192 rows.
