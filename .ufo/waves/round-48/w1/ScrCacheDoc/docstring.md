# C1 docstring draft — the warm-cache contract (round 48 w1, seat ScrCacheDoc)

Target: the `Cache` paragraph of `tools/mado-terminal.py:82-85` and the out-of-contract list that shares those lines,
plus the collateral docstring lines that the new contract invalidates. Every `x:N` is a line of the pinned script

    .ufo/waves/round-47/fetch/xdg-terminal-exec
    sha256 89f2be9a65deb8df93633a9a09b4953a921c83d591ab987f7569280ecd3127ac  (= /usr/bin/xdg-terminal-exec)

Locators were computed with `grep -n` / numbered reads of that file and are re-checked by `verify-quotes.sh`, whose
output is `receipts/quotes.txt`. Behaviour claims are backed by runs of the real script against a fixture tree, with
`--print-cmd` only and `XDG_CACHE_HOME` inside this seat's scratch (`receipts/warm-cache.txt`,
`receipts/ls-listing.txt`). The draft is interface text for the L1 to freeze; it does not edit the tool.

---

## A. Drop-in replacement for `tools/mado-terminal.py:82-85`

```
Cache (in contract since round 48). The resolver reads $XDG_CACHE_HOME/xdg-terminal-exec (XDG_CACHE_HOME defaults to
$HOME/.cache; x:171-173) BEFORE any list or desktop entry: make_paths at x:1167, XTE_CACHE_ENABLED from the environment
with default true at x:1172, the read at x:1179, and only the else branch at x:1181-1200 reads lists and entries. When
the file is trusted the whole selection comes from it - entry path, id, action, the five argument names and the
tokenized command (x:276-285) - so no list is read, no entry is opened, no TryExec/Exec check and no command -v on the
entry runs, and no /execarg_default applies. `print` answers as the resolver does in the same tree, environment and
cache state: its stdout and exit status, not its stderr.

The file is used only when it is a regular file (x:221; a directory, FIFO or device is "no cache data", x:294-296), and
it is read with `IFS= read -r` (x:226): backslashes literal, nothing trimmed, NUL bytes dropped, a last line without a
newline not seen. Lines 1-10 are hash, command, entry path, entry id, entry action, exec argument, app-id argument,
title argument, dir argument, hold argument (x:229-238). Line 11 onward is the cached command, XTE__USEP-separated,
newlines reconstructed, ending at a line that ends with 0x1e "END_OF_EXEC_USEP", which is stripped (x:243-256). Line 50
ends the read as invalid (x:239-242); a terminator that is never seen - including one in a last line without a newline -
is invalid too (x:259-260, x:290-292). A saved cache is exactly these 11 lines plus one per newline inside any field
(x:321-332), written with umask 0077 (x:319-320).

Trust (x:272-289) needs both: the cached hash equals md5("4\n" + XDG_CURRENT_DESKTOP + "\n" + the stdout of
`LANG=C ls -LRl` over the colon-split operands "${XTE__CONFIGS}:${XTE__APPLICATIONS_DIRS}", stderr dropped, run under
LC_ALL=C - x:183-201), and `command -v` resolves the cached command (x:274). Nothing else is checked. So the cache stays
a hit when an entry's bytes change but its size and ls date do not, when its TryExec stub is gone while the cached
command still resolves, or when a list line changes within the same size and minute; it goes stale when a name, size,
mode, link count, owner, group or ls date under those operands changes, when XDG_CURRENT_DESKTOP changes, or when the
cached command stops resolving. On the warm path no entry-id aliases exist - find_entry_paths registers them (x:782)
and runs only cold (x:1200) - so `command -v` sees only bash's own vocabulary, a name containing '/', or a PATH file.

The hash's `ls` is GNU ls in the C locale on a pipe: one entry per line, names literal, file operands first and then
directory operands, a blank line and "<operand>:" before each directory, "total <st_blocks/2>" per directory, -L
dereferencing (a broken symlink or a loop is listed as an all-'?' line and reported on stderr), -R recursing in name
order, and the date as "Mon dd HH:MM" for 0 <= now - mtime <= 15778476 s and "Mon dd  YYYY" otherwise (any future mtime
takes the year form). The tool reproduces that listing byte-exactly from the same tree and clock, ownership as ls
renders it (the name when the passwd/group database visible to the tool has the id, the number otherwise). Any
difference changes the md5 and the cache verdict.

`explain` reports `cache=<absent|hit|stale|invalid|disabled>` in its MADO_TERM line: absent - no regular file (x:221,
x:294-296); invalid - present but not parsed (x:239-242, x:259-260, x:290-292); stale - parsed but the hash differs or
the cached command does not resolve (x:286-288); hit - trusted and used (x:274-285); disabled - XTE_CACHE_ENABLED set
to a value check_bool rejects, including the empty string (x:50-59), so the file is not even opened (x:1179). A cache
file that exists but cannot be read is a failed read, not a fatal error: read_cache is called in an if-condition
(x:1179), so errexit does not apply and the resolver continues cold.

The tool writes nothing: it never creates, rewrites or removes the cache the resolver would. A cold resolver run that
reaches x:1455-1458 - --print-cmd, --test or a launch; the other print modes exit at x:1368-1385 first - saves the cache
there, or removes it when the cache is disabled (x:336-337). The tool reports that consequence and never performs it.
```

## B. Drop-in replacement for the out-of-contract list (`tools/mado-terminal.py:85` and following)

```
Out of contract (round 48): -h/--help; a FIFO named like a desktop file in a later application dir (the script blocks
reading it); a symlink loop under an application dir (find -L errors and the entry set is not modelled); an empty-string
argument (the script loops forever); XDG dirs or HOME containing ':' inside a default; glob characters or a quote in
those defaults; \u/\U escapes beyond ASCII in a delimiter; file names with bytes the shell would see differently in
another locale; a relative XDG_CACHE_HOME or relative XDG config/data dirs (the resolver resolves them against its
working directory, which the tool does not model); a cache file larger than 1 MiB (refused, not read); a cache file
that changes while it is read; and an mtime within 24 h of the six-month date boundary (x:200), where the tool's
boundary constant is not pinned to the second. HOME unset is IN contract (step 0): the resolver exits 1 with empty
stdout only when it must expand a default (x:148, x:166, x:172; set -u at x:23), and runs normally when XDG_CONFIG_HOME,
XDG_DATA_HOME and XDG_CACHE_HOME are all set.
```

Note what moved: `HOME unset` leaves the out-of-contract list and becomes a contract case; the cache file itself is no
longer out of contract. A cache file that is not a regular file needs no out-of-contract entry - `-f` (x:221) makes it
"absent", which is modelled.

## C. Collateral docstring edits the new contract forces

1. `:12-16` (the `print` bullet): "for a cold cache (see "Cache" below)" becomes "in the cache state of the
   environment (see "Cache" below)".
2. `:19` (the MADO_TERM shape): `cache=<absent|present|disabled>` becomes `cache=<absent|hit|stale|invalid|disabled>`;
   on a hit, `selected=`, `path=` and `cmd=` are the cached values (`cmd=` is the first USEP field of the cached
   command, the same field the resolver's print-cmd prints first, x:1450, x:1470-1484).
3. `:20-23` (`--observed`): the capture must be cold (it is, with `XDG_CACHE_HOME=$(mktemp -d)`) and the tool must be
   run with the same environment, including `XDG_CACHE_HOME`, or a legitimate DIFFER is reported.
4. `:28-29` (environment read): add `TZ` (the hashed ls dates follow the resolver's local time zone; unset means
   /etc/localtime, absent in the counter's sandbox) and name the read surface the ls emulation needs: the config/data
   trees, the cache file, and the passwd/group databases for ownership.
5. New step 0 in "The selection (contract)", before step 1:

```
 0. Cache (x:1167-1200): with a true-y XTE_CACHE_ENABLED and a trusted cache file, the selection is the cached one
    (see "Cache") and steps 1-5 do not run; otherwise the cold path runs. HOME unset ends the resolver with exit 1
    and empty stdout when it must expand a default (x:148, x:166, x:172; set -u at x:23) - with all three XDG base
    variables set, HOME unset changes nothing.
```

6. Step 3 (`:41-43`): after "XTE_EXECARG_COMPAT / XTE_CACHE_ENABLED set in the environment win over any directive", add:
   "`/enable_cache` and `/disable_cache` are read only on the cold path (x:376-384, reached at x:1198) and decide only
   whether the run's save at x:1457 writes or removes the cache (x:302, x:336-337); they cannot prevent a cache hit,
   because a hit never reads a list."

## D. Drop-in PROVINCE.md round-48 refinement line

```
**Round-48 refinement (append-only; one tool, one derived-state file read, no new write surface):** `tools/mado-terminal.py`
now also reads the resolver's cache file `$XDG_CACHE_HOME/xdg-terminal-exec` (default `$HOME/.cache/xdg-terminal-exec`)
and models `xdg-terminal-exec` v0.14.3's warm-cache path (script x:171-173, x:179-298, x:1179, x:1455-1458), the file
SUPER+RETURN's resolver consults before any list. It is derived state of the resolver, not a config plane: the tool
reads it and the passwd/group databases (ownership in the hashed listing), never creates, rewrites or removes the cache,
starts no process and opens no socket; `--selftest` writes only inside a private temporary directory it removes. Naming
the read keeps the province complete; the terminal-selection chain it explains stays operator-applied.
```

## E. Implementation obligations this text imposes on the tool

1. Gate: `check_bool(XTE_CACHE_ENABLED or "true")` - the same accepted values and the same stderr note for an
   unrecognised value (x:50-59); a false-y gate skips the read entirely (x:1179).
2. Cache path: `XDG_CACHE_HOME or HOME + "/.cache"` + `/xdg-terminal-exec` (x:172-173); a missing HOME is only
   reached here when XDG_CACHE_HOME is unset, and that case is itself fatal at x:172.
3. Parse in the resolver's order and stop exactly where it stops: `-f` first (x:221), then lines 1-10, then the command
   lines with the terminator, with line 50 invalid before any assignment (x:239-242).
4. Hash: reproduce `LANG=C ls -LRl` byte-exactly (A, fourth paragraph), md5 the three-part input (x:189-203), accept
   only a 32-hex result (x:204-213), compare as a string.
5. Trust: `command -v` over the tool's existing model but with the alias table empty on this path (x:782 runs cold
   only).
6. Selection: on a hit, set path/id/action/argument names and the USEP command from the cache and skip
   read_config_paths/find_entry_paths (x:1181-1200); `--print-content` then reads the CACHED path (x:1362), and a path
   that cannot be read ends that mode with the shell's redirect failure (exit 1, output up to that point).
7. Split the cached command with the tool's `split_ifs(..., USEP)` semantics (unquoted expansion under `set -f`, x:23,
   x:1448-1451): interior empty fields kept, one trailing empty dropped.
8. Write nothing, in every mode, including `--selftest`.

## F. Findings for the freeze (each with its receipt)

**F1 - `/disable_cache` is a save-side switch, never a read switch.** The directives are parsed in
`read_config_paths` (x:376-384), which runs only in the cold else branch (x:1198); the read gate is x:1179 and a hit
never reads a list. Receipt `receipts/warm-cache.txt`: adding `/disable_cache` to the list changes the list's size and
mtime, so the hash changes ("cache is out-of-date"), the cold path runs, the directive is found, and the file is
removed. The brief's "disabled via XTE_CACHE_ENABLED or /disable_cache" therefore has to be read as: the READ is
disabled only by `XTE_CACHE_ENABLED`; `/disable_cache` only makes a cold run remove the file. `cache=disabled` must be
defined on `XTE_CACHE_ENABLED` alone, or `explain` will call a hit "disabled".

**F2 - `--test` also triggers the background save.** `save_cache "$1" &` (x:1455-1458) precedes the test-mode branch
(x:1460-1466), so a cold `--test` writes the cache, exactly like `--print-cmd` and a launch. The brief's "print-cmd or a
launch" is incomplete; counter priming must either use `--print-cmd` (as specified) or account for `--test`.

**F3 - an empty `XTE_CACHE_ENABLED` disables the read but freezes nothing.** `check_bool` rejects the empty string
(x:50-59) so the read is skipped, while `XTE__CACHE_CONFIGURED=${XTE_CACHE_ENABLED-}` (x:1174) reads the ENVIRONMENT
variable, so an empty value leaves the directive slot open and a later `/enable_cache` can turn the save back on. Any
non-empty environment value freezes both directives (x:376, x:382).

**F4 - the newline guard is dead code.** x:312-318 compares `"${XTE__HASH}${1}...${XTE__HOLDARG}"` against a single
newline, and the hash is 32 hex characters by then (x:204-213, x:310), so the pattern can never match: an argument
containing a newline is written to the cache and shifts every following field. A fixture may rely on such a file
existing; the tool must parse whatever file it is given.

**F5 - the priming run's print modes change the saved path.** `--print-path` rewrites `XTE__ENTRY_PATH` in place
(x:1341-1343) before the save at x:1455, so a prime with `--print-cmd --print-path` stores the folded path and a prime
with `--print-cmd` alone stores the `/./` form. Both print identically, but line 3 of the cache differs; compare cache
bytes only if the priming argv is fixed.

**F6 - an unreadable cache file is a failed read, not a fatal error.** `read_cache` is called in an `if` condition
(x:1179), so errexit is suspended for it; the redirection failure prints "Permission denied" and the resolver continues
cold. Receipt: `chmod 000` on a primed cache gave rc 0 and the cold answer, with one "Permission denied" line.

**F7 - HOME unset is conditional, not unconditional.** Round-47 D1 says "pin exit 1, empty stdout"; measured, that holds
only when a default must expand: `XDG_CONFIG_HOME` unset -> x:148, `XDG_DATA_HOME` unset -> x:166, `XDG_CACHE_HOME`
unset -> x:172, each "HOME: unbound variable", rc 1, empty stdout. With all three set, a HOME-less run selects normally
(rc 0, `foo`). Receipt `receipts/warm-cache.txt`, last block. The C1 contract and the D1 lesson line must both carry the
condition.

**F8 - no aliases on the warm path.** Entry ids are bash aliases registered by `find_entry_paths` (x:782), which runs
only cold (x:1200). A cached command that is an entry id therefore fails `command -v` (x:274) on the warm path even
though it would resolve cold: a stale class that a cold-path-only model cannot produce.

**F9 - the ls facts the md5 needs, measured.** On this host's GNU ls, a pipe and the C locale: names print literally
(no quoting; a name with a newline injects a line into the hash input); `total` is `st_blocks/2`; a broken symlink or a
loop under `-L` is listed as an all-`?` line whose field padding follows the block's other entries, with the error only
on stderr; a future mtime ALWAYS takes the year form (no one-hour grace: `now+1 s` -> `Mon dd  YYYY`); the six-month
boundary lies in (15771276 s, 15785676 s) - `now-15771276` prints `HH:MM`, `now-15785676` prints the year; without
/etc the owner/group are numeric (`1000 1000` under `bwrap --dev-bind / / --tmpfs /etc`). Receipts
`receipts/ls-listing.txt`; the md5 itself was reproduced byte-exactly from the tree (`receipts/warm-cache.txt`,
"gen_hash reproduced").

**F10 - what in the tool has to move.** `explain`'s vocabulary is `present|absent` today
(`tools/mado-terminal.py:852-861`), and `select()` computes the cache path only after `read_config_paths` and
`find_entry_paths` have already run (`tools/mado-terminal.py:721-726`). The contract puts the cache read first and the
verdict in the MADO_TERM line.

## G. Receipts

- `receipts/quotes.txt` - every literal quote and `x:N` locator used above, re-checked against the pin
  (`verify-quotes.sh`, exit 0).
- `receipts/warm-cache.txt` - pin hashes; cold prime and its 11-line cache bytes; the md5 reproduced byte-exactly; a
  same-size same-minute `Exec=` edit where the warm run prints `foo` and the cold run prints `bar`; `/disable_cache`
  reaching only the cold path and removing the file; `XTE_CACHE_ENABLED=false` ignoring a valid cache and removing it;
  an unreadable cache; the four HOME-unset variants.
- `receipts/ls-listing.txt` - the exact `ls -LRl` bytes that are hashed (broken symlink, symlink loop, recursion
  headers, `total`), the date forms around both boundaries, and numeric ownership without /etc.
- `probe.sh` - regenerates both from a fixture tree under `$WORK` (default
  `/fast/scratch/hyaku/mado-r48/ScrCacheDoc`); it never writes the host cache, never launches a terminal, and every
  resolver call uses `--print-cmd`.
