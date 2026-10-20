# S087 non-author re-open — omarchy-restart-walker @ v3.8.4

Seat `MadoR18.ReopenS087`, wave 2 (falsify), 2026-10-20. Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`. Read-only: one `curl` fetch per
rules, `git ls-remote` to the public remote, byte reads of the host copy, and
the lane's own `fetch-verify.py`. No package manager, service, compositor,
input, screenshot or REA command. Nothing was executed from the fetched body.

## Row under test

`corpus/SOURCES.md:99`

```
| S087 | omarchy bin/omarchy-restart-walker @ v3.8.4 — https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-restart-walker | code | A | restart path for elephant and app-walker unit at tag v3.8.4 | file lines 5-24; sha256 9ac82d0c1370ec19f59c8347716036765d3335d348feaec4c9581e2ca3bf8174 (equal to host copy) | restart is systemctl --user restart of two units; prints RESTART MANUALLY when the unit is not enabled | mined | 2026-10-20 | on-change | corpus/knowledge/walker-route-r18.md |
```

The source and anchor cells name no further file. Per the item, nothing beyond
this one URL was re-fetched; the "equal to host copy" clause was checked against
the local host bytes instead.

## Commands and their output

1. Tag resolution (public remote; no lane write):

```
$ git ls-remote https://github.com/basecamp/omarchy refs/tags/v3.8.4 'refs/tags/v3.8.4^{}'
8fcc9d6048af4cb0e3af8512c78049857a3b53dd	refs/tags/v3.8.4
```

Only one line, no `^{}` peeled line → **lightweight tag**. The same command
against the redirect target's spelling (`https://github.com/omacom/omarchy`)
returns the identical `8fcc9d60…`.

2. Independent fetch (rules channel; body + receipt under
`.ufo/waves/round-18/fetch/ReopenS087/`):

```
$ curl -sSL --max-time 60 -o .ufo/waves/round-18/fetch/ReopenS087/omarchy-restart-walker \
    -w '%{http_code} %{url_effective}\n' \
    https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-restart-walker
200 https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-restart-walker
$ sha256sum …/ReopenS087/omarchy-restart-walker
9ac82d0c1370ec19f59c8347716036765d3335d348feaec4c9581e2ca3bf8174
$ stat -c '%s' …/ReopenS087/omarchy-restart-walker
709
```

Repeated at `2026-10-20T16:01:10Z`: same 200, same 709 bytes, same sha256.
Receipt appended at `.ufo/waves/round-18/fetch/ReopenS087/receipts.jsonl`
(`mado-fetch-receipt-v1`, curl 8.23.0).

3. Every wave-1 receipt for this file. Exhaustive scan of every
`receipts.jsonl` under `.ufo/waves/round-18/fetch/`; exactly two wave-1 lines
carry the artifact:

| seat | receipt `url` | `final_url` | HTTP | bytes | sha256 | fetched_at |
|---|---|---|---|---|---|---|
| NoteWalker | `raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-restart-walker` | same | 200 | 709 | `9ac82d0c1370ec19f59c8347716036765d3335d348feaec4c9581e2ca3bf8174` | 15:40:36Z |
| SrcOmarchyWalker | `github.com/basecamp/omarchy/raw/v3.8.4/bin/omarchy-restart-walker` | `raw.githubusercontent.com/omacom/omarchy/v3.8.4/bin/omarchy-restart-walker` | 200 | 709 | `9ac82d0c1370ec19f59c8347716036765d3335d348feaec4c9581e2ca3bf8174` | 15:40:52Z |

The `omacom` `final_url` looked like a typo, so it was measured:

```
$ curl -sSL --max-time 60 -o /dev/null -w '%{http_code} %{url_effective}\n' \
    https://github.com/basecamp/omarchy/raw/v3.8.4/bin/omarchy-restart-walker
200 https://raw.githubusercontent.com/omacom/omarchy/v3.8.4/bin/omarchy-restart-walker
```

The redirect is real (owner renamed upstream; the old spelling still serves);
that receipt is faithful, and its digest equals the row's. Three independent
fetches and the row all agree on `9ac82d0c…` / 709 bytes.

4. Host copy claim:

```
$ sha256sum ~/.local/share/omarchy/bin/omarchy-restart-walker
9ac82d0c1370ec19f59c8347716036765d3335d348feaec4c9581e2ca3bf8174
$ cmp -s ~/.local/share/omarchy/bin/omarchy-restart-walker \
         .ufo/waves/round-18/fetch/ReopenS087/omarchy-restart-walker && echo BYTE-EQUAL
BYTE-EQUAL
```

709 bytes. `(equal to host copy)` holds.

5. Lane join tool (read-only; re-hashes every body):

```
$ python3 .ufo/waves/round-18/fetch-verify.py --sources corpus/SOURCES.md \
    --rows S087 --quote 'S087=RESTART MANUALLY'
… FETCH ReopenS087/omarchy-restart-walker ok
ROW S087 receipted
QUOTE S087 ok
SUMMARY receipts=351 ok=351 bad=0 rows=1 unreceipted=0 quotes=1 quote_bad=0
exit=0
```

## Body read (24 lines, `cat -n` on my fetched copy)

Lines 5-24 are the whole executable body: `restart_services` (5-15) and the
`EUID == 0` re-exec branch (17-24). Line 3 is the `omarchy:summary` comment.
Full relevant region:

```bash
     5	restart_services() {
     6	  if systemctl --user is-enabled elephant.service &>/dev/null; then
     7	    systemctl --user restart elephant.service
     8	  fi
     9	
    10	  if systemctl --user is-enabled app-walker@autostart.service &>/dev/null; then
    11	    systemctl --user restart app-walker@autostart.service
    12	  else
    13	    echo -e "\e[31mUnable to restart Walker -- RESTART MANUALLY\e[0m"
    14	  fi
    15	}
    16	
    17	if (( EUID == 0 )); then
    18	  SCRIPT_OWNER=$(stat -c '%U' "$0")
    19	  USER_UID=$(id -u "$SCRIPT_OWNER")
    20	  systemd-run --uid="$SCRIPT_OWNER" --setenv=XDG_RUNTIME_DIR="/run/user/$USER_UID" \
    21	    bash -c "$(declare -f restart_services); restart_services"
    22	else
    23	  restart_services
    24	fi
```

## Judgments

**Tag-pinned?** Yes, by ref name: the URL path selects ref `v3.8.4`, not a
branch. But the tag is **lightweight**, so it is a mutable pointer — a re-point
would silently change the served bytes at an unchanged URL. It has resolved to
`8fcc9d6048af4cb0e3af8512c78049857a3b53dd` on 2026-10-20 by two spellings of the
owner. For strictness: content addressing here comes from the sha256 plus three
agreeing receipts, not from the URL alone. (Upstream `HEAD` has since moved to
`refs/heads/quattro` at `3ac43659…` and `refs/heads/master` no longer resolves
upstream; the tag path is unaffected.)

**kind = code.** Primary shell source, not documentation. Correct.

**tier A.** The artifact *is* the upstream implementation for the stated scope
(the restart path shipped at v3.8.4), fetched from its own repository at a tag.
Primary source for that scope — A holds.

**scope.** "restart path for elephant and app-walker unit at tag v3.8.4" names
the P3 surface keywords (`elephant`, `app-walker`/walker) and is exactly what
the file does: `elephant.service` restart (6-8) and
`app-walker@autostart.service` restart (10-11). Version matches the tag.

**anchor.** "file lines 5-24" is accurate for the 24-line file; the sha256 is
correct and reproducible three ways.

**teaches grounded?** Substantially yes, with one wording nuance:

- "restart is `systemctl --user restart` of two units" — lines 7 and 11. ✓
- "prints RESTART MANUALLY when the unit is not enabled" — line 13, the `else`
  of the *walker* unit's `is-enabled` test (10-14). ✓ for the walker unit. The
  elephant branch (6-8) silently skips when `elephant.service` is disabled — it
  prints nothing. The row's summary reads generically ("the unit"), so on a
  strict reading it over-generalises the print to both units; the cited note is
  precise (below). Not enough to uncredit the row; the substantive restart path
  and the manual-fallback behaviour are both present in the anchored region.
- Omitted from `teaches` but present in the file and the note: the root branch
  re-execs via `systemd-run --uid=…` with `XDG_RUNTIME_DIR` (17-21).

**Citing note truthful?** Yes.

- `corpus/knowledge/walker-route-r18.md:1` lists
  `S087 …/bin/omarchy-restart-walker (restart)` — the exact URL.
- Anchor table `:35` binds `OR` to that file; `:161-164` state: restarts
  `elephant.service` when enabled `[OR:6-8]`; restarts
  `app-walker@autostart.service` when enabled, else prints "Unable to restart
  Walker -- RESTART MANUALLY" `[OR:10-14]`; as root re-runs under
  `systemd-run --uid` with `XDG_RUNTIME_DIR` `[OR:17-21]`. Each range maps
  exactly onto the fetched lines; the note does not claim the elephant branch
  prints.
- Host declaration `:187` gives sha256 `9ac82d0c…`, 709 bytes, "equal to `OR`" —
  verified byte-equal.

**Other checks.** Row id unique (`grep -c '| S087 |'` = 1). Status `mined` and
`used-by` are consistent with the note's actual use. The note's tag prose
(v3.8.4 = `8fcc9d60…`, lightweight) matches my `ls-remote` and the host
checkout's `packed-refs` bytes (`:2` master and `:508` v3.8.4 both `8fcc9d60…`).

## Residual unknowns / caveats (do not change the verdict)

- Lightweight tag: "tag-pinned" is name-pinned only; closure should re-run
  `ls-remote` and compare the digest, as the note's `recheck` already instructs.
- Upstream owner rename: `github.com/basecamp/…` URLs redirect to `omacom`;
  receipts must record `final_url`, which both wave-1 seats did.
- The `teaches` print clause is scoped to the walker unit by the code; the row's
  compact wording is broader than the bytes.

GATE | S087 | https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/bin/omarchy-restart-walker | 2026-10-20 | .ufo/waves/round-18/fetch/ReopenS087/omarchy-restart-walker:10 "if systemctl --user is-enabled app-walker@autostart.service &>/dev/null; then" (7 words) | 9ac82d0c1370ec19f59c8347716036765d3335d348feaec4c9581e2ca3bf8174 | agree: independent fetch reproduces the row digest and both wave-1 receipts (709 B); URL is tag-ref-pinned at lightweight v3.8.4 (8fcc9d60); tier-A primary code for the stated P3 scope; note citations OR:6-8/10-14/17-21 and the host-copy claim are exact, with only a minor over-generalisation in the row's print clause (elephant branch skips silently)
