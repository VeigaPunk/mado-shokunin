# SrcPyShlex — CPython v3.14.8 documents `shlex.join` as a pure string formatter and `args` as the subprocess command parameter in both positional and `args=` keyword form; two S1xx-pending rows drafted

All paths relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`. Fetch bodies and receipts are in
`.ufo/waves/round-20/fetch/SrcPyShlex/`. Fixture code was never executed; no transcript was scanned;
no lane file was edited. Quotes are documentary; the only commands run against Python were two local
probes that create no process (`probe-kwargs.py` replaces `subprocess.Popen` with a stub).

## Findings

### F1. Tag → commit resolved (observed, high confidence)

```
$ git ls-remote https://github.com/python/cpython refs/tags/v3.14.8 'refs/tags/v3.14.8^{}'
992560c2cc62d47b308cec662feb485456847931	refs/tags/v3.14.8
8e6e75d9102e39bed2a2b279203a396741180f12	refs/tags/v3.14.8^{}
```

`v3.14.8` is an annotated tag: tag object `992560c2cc62d47b308cec662feb485456847931`, peeled commit
`8e6e75d9102e39bed2a2b279203a396741180f12`. Saved: `fetch/SrcPyShlex/git-ls-remote-v3.14.8.txt`
(121 B, sha256 `6549cb7c3492366c3440e8b774e38c2642d153ce3e3f660ac6d8e94b5447d0ac`).

### F2. `shlex.join` is a formatter that returns a `str` (observed, high confidence)

- `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/shlex.rst` → HTTP **200**,
  17,867 B, sha256 `819c6e6fab583c8d30e32950591ed1fda2b552cebcbfadc5d1619e3e35ea03b0` (`shlex.rst`;
  `receipts.jsonl` line 1). The path exists at this tag (200), unlike `Doc/library/functions.rst`,
  which a sibling seat found 404 after the 3.14 docs-tree move.
- Located quotes (markup tokens not counted): `:37` `.. function:: join(split_command)`;
  `:39-40` "Concatenate the tokens of the list *split_command* and return a string. This function is
  the inverse of :func:`split`." (20 words); `:46-47` "The returned value is shell-escaped to protect
  against injection vulnerabilities"; `:49` `.. versionadded:: 3.8`.
- Implementation `https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/shlex.py` → HTTP
  **200**, 13,756 B, sha256 `aeda1c54188363d907654a19d338e5961416ebec2e2f506afab19be61ada8120`
  (`shlex.py`; `receipts.jsonl` line 3): `:315-317`

  ```python
  def join(split_command):
      """Return a shell-escaped string from *split_command*."""
      return ' '.join(quote(arg) for arg in split_command)
  ```

  A formatter over the token list; no process call anywhere in the function.
- The running 3.14.8 stdlib is byte-identical to the pinned implementation:
  `sha256sum /usr/lib/python3.14/shlex.py` → `aeda1c54188363d907654a19d338e5961416ebec2e2f506afab19be61ada8120`
  (same digest). Probe `fetch/SrcPyShlex/probe-join.out` (sha256
  `41b0f30dc6af7bb5515dbe0f380978964f9f6c247ac5651a3f71f9d9e9376806`):

  ```
  str
  pacman -Q hyprland
  ```

  i.e. `shlex.join(['pacman','-Q','hyprland'])` returns a string; it executes nothing. (The string is
  data in this probe; no host command ran.)
- Establishes: a literal argv handed to `shlex.join` is formatted, never spawned, so a finding at the
  join site would attribute execution to a call whose documented result is a string. Does not
  establish how a caller later uses that string — the later spawn, if any, is a separate site.

### F3. `args` is the subprocess command parameter; the keyword `args=[...]` binds it (observed, high confidence)

- `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/subprocess.rst` → HTTP
  **200**, 61,603 B, sha256 `05cd782c5181481ad961788dd678b99c903eb3ff53e0ebab3095c38b48c74dfd`
  (`subprocess.rst`; `receipts.jsonl` line 2).
- Documented anchors:
  - `:38-41` `.. function:: run(args, *, stdin=None, input=None, stdout=None, stderr=None, ...)` —
    `args` stands before the `*` marker, i.e. not keyword-only in the documented signature.
  - `:43` "Run the command described by *args*." (6 words).
  - `:359-366` `.. class:: Popen(args, bufsize=-1, executable=None, ...)`; the `*` marker comes only
    at `*, group=None` on `:363`, so `args` is the first (positional-or-keyword) parameter.
  - `:898-900` `.. attribute:: Popen.args` / "The *args* argument as it was passed to
    :class:`Popen` -- a sequence of program arguments or else a single string." (19 words).
  - `:46-48` says the shown signature is abbreviated ("The arguments shown above are merely the most
    common ones ... hence the use of keyword-only notation in the abbreviated signature"). That is a
    disclaimer about the *other* parameters, not about `args`, which is the required command slot.
- Implementation `https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/subprocess.py` → HTTP
  **200**, 90,748 B, sha256 `7fa4af83422024a19e64a80937f6c8094244c3397372a495b348dfbe44a5dd72`
  (`subprocess.py`; `receipts.jsonl` line 4):
  - `:513-514` `def run(*popenargs, input=None, capture_output=False, timeout=None, check=False, **kwargs)`.
  - `:555` `with Popen(*popenargs, **kwargs) as process:` — a keyword in `kwargs` reaches `Popen`.
  - `:817-818` `def __init__(self, args, bufsize=-1, executable=None, ...)` — `Popen`'s first
    parameter is named `args`, so `Popen(args=[...])` binds the command slot.
  - `:388` / `:396` `def call(*popenargs, timeout=None, **kwargs)` → `with Popen(*popenargs, **kwargs) as p:`.
  - `:405` / `:415-417` `check_call` → `call(*popenargs, **kwargs)`, then on failure
    `cmd = kwargs.get("args")` — the implementation explicitly recovers a keyword-supplied command,
    which only makes sense because `args=` is a legal call form.
  - `:424` / `:473-474` `check_output` → `run(*popenargs, ..., **kwargs)`.
- The running 3.14.8 stdlib is byte-identical:
  `sha256sum /usr/lib/python3.14/subprocess.py` → `7fa4af83422024a19e64a80937f6c8094244c3397372a495b348dfbe44a5dd72`;
  `grep -n 'kwargs.get("args")' /usr/lib/python3.14/subprocess.py` → `417`.
- Probe `fetch/SrcPyShlex/probe-kwargs.py` (sha256
  `42ee139265b51ac18b13b6c9bd0741975d25252a3c45ccaaba6548bd5c4c72c4`; output sha256
  `ed64f77f7394176515489f5c6ac747d85fc3c0c81a98a904c98cb5b384d22f2b`), run under
  `python3 -I` with `subprocess.Popen` stubbed before any call:

  ```
  run(args=...)      -> {'pos': (), 'kw': {'args': ['example-prog', '--flag']}} returncode 0
  call(args=...)     -> {'pos': (), 'kw': {'args': ['example-prog', '--flag']}} returncode 0
  Popen(args=...)    -> {'pos': (), 'kw': {'args': ['example-prog', '--flag']}}
  run(positional)    -> {'pos': (['example-prog', '--flag'],), 'kw': {}} returncode 0
  check_output(args=) -> {'pos': (), 'kw': {'stdout': -1, 'args': ['example-prog', '--flag']}} bytes b''
  ```

  No process was created; `example-prog` is a non-host placeholder and the stub never execs.
- Establishes: the same command description is stated by a positional argv and by `args=[...]`; the
  keyword form is not a different interface. A scan that reads only the first positional slot and
  records "(a keyword `args=[...]` is a miss)" is blind to a literal spawn the transcript spells out.
  Does not establish that any transcript used the keyword form (none was scanned here).

### F4. Why two rows, not one (inference from the registry contract)

[INFERENCE] The 11-column row (S004 contract) carries one source, one anchor cell, and one located
quote/line range. These are two files at the same tag with distinct digests and disjoint line ranges
(`shlex` vs `subprocess`), so splitting keeps each row independently re-derivable, matching the
sibling split in `reports/SrcPyBuiltins.md` F6.

### F5. Context: the pinned tool currently declares the keyword form a miss (observed, read-only)

At lane HEAD `e629f731172b8238caffe50f152217ce56535fb4`, `tools/mado-tripwire.py` is
`367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`; its own docstring says at
`:49-50`: "only positional argv lists are read (a keyword `args=[...]` is a miss)". `PURE_ARG_CALLS`
(`:1252-1256`) enumerates builtins only (`print`, `list`, `tuple`, `set`, `dict`, ...) and does not
list `shlex.join`. The attribute form `shlex.join([...])` escapes the lead branch because that branch
requires a bare `ast.Name` callee; the from-import form is different: `from shlex import join;
join(['pacman','-Q','hyprland'])` is a bare, unbound name, is not a spawn, and is not in
`PURE_ARG_CALLS`, so by code reading `helper_argv_leads` (`:1379-1390`) classifies its literal argv
and would emit a `lead` row. That is a code-path inference, not a run of the tool: no `--scan` was
executed here. The E2 known-pure status of `shlex.join` is what keeps such a site clean, which is why
the shlex row is needed. This seat did not edit or evaluate the in-flight repair; F2/F3 are the
source ground such a repair can lean on, and the observed/lead classification remains the contract's
call.

## Draft rows (id `S1xx-pending`; L1 assigns S099–S110)

Both rows are opened but not yet mined: `status` `queued`, `used-by` `—`. If a round-20 knowledge
note (e.g. `corpus/knowledge/tripwire-precision-r20.md`) lands citing them, L1 flips `status` to
`mined` and sets `used-by` per the registry lifecycle. No `corpus/SOURCES.md` row for CPython,
`shlex` or `subprocess` exists today (`grep -in 'cpython\|shlex\|subprocess' corpus/SOURCES.md` → no
matches), so these scopes are new.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S1xx-pending | CPython v3.14.8 shlex reference and implementation — https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/shlex.rst (also https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/shlex.py at the same tag) | docs | A | `shlex.join` is a pure formatter: it concatenates and shell-escapes a token list and returns a `str`; it has no execution path and its input list is data | tag `v3.14.8` → annotated tag object `992560c2cc62d47b308cec662feb485456847931`, peeled commit `8e6e75d9102e39bed2a2b279203a396741180f12` (`git ls-remote … refs/tags/v3.14.8 'refs/tags/v3.14.8^{}'`); `shlex.rst` 17,867 B sha256 `819c6e6fab583c8d30e32950591ed1fda2b552cebcbfadc5d1619e3e35ea03b0`, `join` :37-49; `Lib/shlex.py` 13,756 B sha256 `aeda1c54188363d907654a19d338e5961416ebec2e2f506afab19be61ada8120`, `join` :315-317; host `/usr/lib/python3.14/shlex.py` has the same sha256 | Doc: "Concatenate the tokens of the list *split_command* and return a string. This function is the inverse of :func:`split`." (:39-40), "The returned value is shell-escaped to protect against injection vulnerabilities" (:46-47, versionadded 3.8 :49); source returns `' '.join(quote(arg) for arg in split_command)` (:317), a formatter over tokens with no process call. Establishes that a literal argv handed to `shlex.join` is formatted, never spawned; does not establish how the returned string is later used | queued | 2026-10-20 | on-release | — |
| S1xx-pending | CPython v3.14.8 subprocess reference and implementation — https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/subprocess.rst (also https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/subprocess.py at the same tag) | docs | A | the command parameter of `subprocess.run`/`Popen`/`call`/`check_call`/`check_output` is `args`, stated positionally or as the keyword `args=[...]`; both bind the same command description | tag `v3.14.8` → tag object `992560c2cc62d47b308cec662feb485456847931`, peeled commit `8e6e75d9102e39bed2a2b279203a396741180f12`; `subprocess.rst` 61,603 B sha256 `05cd782c5181481ad961788dd678b99c903eb3ff53e0ebab3095c38b48c74dfd`, `run` :38-43, `Popen` :359-366, `Popen.args` :898-900; `Lib/subprocess.py` 90,748 B sha256 `7fa4af83422024a19e64a80937f6c8094244c3397372a495b348dfbe44a5dd72`, `run` :513-514, forwarding :555, `call` :388/:396, `check_call` :405/:415-417, `check_output` :424/:473-474, `Popen.__init__` :817-818; host `/usr/lib/python3.14/subprocess.py` has the same sha256; probe `probe-kwargs.py` sha256 `42ee139265b51ac18b13b6c9bd0741975d25252a3c45ccaaba6548bd5c4c72c4` | Doc: "Run the command described by *args*." (:43), with `args` before the `*`; `Popen.args` is "The *args* argument as it was passed to :class:`Popen` -- a sequence of program arguments or else a single string." (:900-901). Source: `run(*popenargs, …, **kwargs)` forwards `Popen(*popenargs, **kwargs)` (:555) into `Popen.__init__(self, args, …)` (:817), and `check_call` recovers a keyword-supplied command via `kwargs.get("args")` (:417); stub-Popen probe on the byte-identical host 3.14.8 shows `args=[…]` binding in `run`/`call`/`Popen`/`check_output`. Does not establish that any transcript used the keyword form | queued | 2026-10-20 | on-release | — |

## Re-derivation commands

```
git ls-remote https://github.com/python/cpython refs/tags/v3.14.8 'refs/tags/v3.14.8^{}'
curl -sSL --max-time 60 https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/shlex.rst | sha256sum
curl -sSL --max-time 60 https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/subprocess.rst | sha256sum
curl -sSL --max-time 60 https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/shlex.py | sha256sum
curl -sSL --max-time 60 https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/subprocess.py | sha256sum
grep -n 'join' /tmp/shlex.rst            # :37 function, :39-40 quote, :46-47 escaping, :49 versionadded
grep -n 'def join' /tmp/shlex.py         # :315-317
grep -n 'run(args\|Popen(args\|Popen.args' /tmp/subprocess.rst   # :38, :359, :898
grep -n 'def run(\*popenargs\|def __init__(self, args\|kwargs.get("args")' /tmp/subprocess.py  # :513, :817, :417
python3 -I .ufo/waves/round-20/fetch/SrcPyShlex/probe-kwargs.py
sha256sum /usr/lib/python3.14/shlex.py /usr/lib/python3.14/subprocess.py
```

Expected digests: `819c6e6f…` (shlex.rst), `05cd782c…` (subprocess.rst), `aeda1c54…` (shlex.py and
host shlex), `7fa4af83…` (subprocess.py and host subprocess), plus the two ls-remote lines in F1.

## Fetch receipts inventory

`fetch/SrcPyShlex/receipts.jsonl` — 4 lines, 2,344 B, sha256
`e61f658b1414299f682128d71902a42f34443d8a89abbc9eba96d011ce1d1a03`; fetched at
`2026-10-20T19:43:43Z` (docs) and `2026-10-20T19:44:07Z` (implementations); tool line
`curl 8.23.0 (x86_64-pc-linux-gnu) libcurl/8.23.0 OpenSSL/3.6.5 zlib/1.3.2 brotli/1.2.0 zstd/1.5.7
libidn2/2.3.8 libpsl/0.21.5 libssh2/1.11.1 nghttp2/1.70.0 ngtcp2/1.25.0 nghttp3/1.18.0
mit-krb5/1.22.2`.

| body | http | bytes | sha256 |
|---|---|---|---|
| shlex.rst | 200 | 17,867 | 819c6e6fab583c8d30e32950591ed1fda2b552cebcbfadc5d1619e3e35ea03b0 |
| subprocess.rst | 200 | 61,603 | 05cd782c5181481ad961788dd678b99c903eb3ff53e0ebab3095c38b48c74dfd |
| shlex.py | 200 | 13,756 | aeda1c54188363d907654a19d338e5961416ebec2e2f506afab19be61ada8120 |
| subprocess.py | 200 | 90,748 | 7fa4af83422024a19e64a80937f6c8094244c3397372a495b348dfbe44a5dd72 |

Supporting (not curl bodies, so no receipt lines): `git-ls-remote-v3.14.8.txt` (121 B, sha256
`6549cb7c3492366c3440e8b774e38c2642d153ce3e3f660ac6d8e94b5447d0ac`), `probe-kwargs.py` (1,403 B,
sha256 `42ee139265b51ac18b13b6c9bd0741975d25252a3c45ccaaba6548bd5c4c72c4`), `probe-kwargs.out`
(447 B, sha256 `ed64f77f7394176515489f5c6ac747d85fc3c0c81a98a904c98cb5b384d22f2b`), `probe-join.out`
(23 B, sha256 `41b0f30dc6af7bb5515dbe0f380978964f9f6c247ac5651a3f71f9d9e9376806`).

## Limits

- Did not execute any fixture, the precision counter, `--scan`, or the tripwire; no transcript was
  read beyond the tool's own docstring quoted in F5. The two probes use a stubbed `subprocess.Popen`
  and a pure `shlex.join`, and create no process.
- The docs' `run` signature is explicitly abbreviated (`subprocess.rst:46-48`); `run` is implemented
  as `*popenargs, **kwargs`, so the keyword form works by forwarding to `Popen`, not because `run`
  declares `args`. The row states this; a reader who quotes only the RST signature would miss the
  forwarding path.
- Did not check docs.python.org HTML, other 3.14 patch tags (v3.14.0–v3.14.7), PyPy, or embedded
  interpreters: the relocation of `Doc/library/functions.rst` another seat observed shows the docs
  tree can move within a series, so the path pin is only measured at v3.14.8. Whether
  `Doc/library/shlex.rst`/`subprocess.rst` persist in later patches is [UNK].
- Did not verify release signatures or a source tarball against the tag; the anchor is tag→commit
  plus raw-body digest, and host-stdlib byte equality is an additional cross-check, not a signature
  check.
- [INFERENCE] The mapping from these documented facts to the tripwire's `observed`/`lead`/pure
  categories is a reading of the round-20 contract; the pages name no tripwire rule, and F5 does not
  judge the in-flight repair.
- Did not assign SOURCES ids, edit `corpus/SOURCES.md`, or set `status` beyond `queued`; L1
  integrates.

## Installs

none
