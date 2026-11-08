---
source: S528 (GLib 2.90.1 gdesktopappinfo.c 8e9ce1a8327a2daf6bc16e8dcfb653c482afde7bebc2ca2621747626b5495b0d, 163369 B, 5356 L - the load gate that calls the lookup twice: the `TryExec` check at :1947-1959 (:1951 `g_find_program_for_path (try_exec, NULL, path)`) and the `Exec` argv[0] check at :1978-2004 (:1993 `g_find_program_for_path (argv[0], NULL, path)`), both with the `Path=` value as `working_dir` and NULL as the search path), S532 (GLib 2.90.1 gio-tool-launch.c 16b4c8683b00407670f600eda0e65e9d929a59daac499cbe8f3d1fd532f6595a, 3991 B, 134 L - the CLI that constructs the app info at :106 and prints the load refusal at :109), S533 (GLib 2.90.1 gutils.c 65086c293646bf83884f56f54bb5e2e872adb28ee77f1223d6d9f095a75e3771, 100534 B, 3245 L - the lookup itself: the PATH source at :371, the unset guard at :376, the `/bin:/usr/bin:.` literal at :388, the absolute-or-slash short-circuit at :331-357, and the entry walk at :462-500)
verified-at: 2026-11-08 - `glib2 2.90.1-1`; the oracle `/usr/bin/gio` sha256 `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462` (re-hashed by this seat, equal to the L1 pin and to the round-99 case-file pin). `gutils.c` was re-opened twice by this seat: the committed round-99 fetch bytes (`.ufo/waves/round-99/fetch/gutils.c`, sha256 `65086c29...e3771`) and a live re-fetch of `https://gitlab.gnome.org/GNOME/glib/-/raw/2.90.1/glib/gutils.c` (HTTP 200, byte-identical). The 21 measurement rows of section 7 are this seat's read-only runs of the installed `gio` through the committed round-99 oracle (`.ufo/waves/round-99/controls/launchenv-probe-r99.py`, sha256 `cbfff7a4...d129199`, two runs per case, all agreeing), over case roots built under `/fast/scratch/hyaku/mado-r100/R100MScribeEntry` (deleted before this draft was filed). Every `gio launch` call ran with `env`-style env `LC_ALL=C HOME=<root>/h PROBE_OUT=<root>/out` and, where the case sets one, the case's own PATH entries only - never a host PATH - so no host application and no terminal was ever started.
recheck: 180d - re-pull `gutils.c`, `gdesktopappinfo.c` and `gio-tool-launch.c` at the next GLib tag that changes any of them (2.90.1 is the pin) and re-hash them against the digests above; also when `glib2` leaves 2.90.1-1 or the `gio` CLI's `launch` spelling moves. A change to the `/bin:/usr/bin:.` literal, to the `if (path == NULL)` guard, to the empty-entry branch at :471-475, to the absolute-or-slash branch at :331-357, to the two load-gate calls at :1951 and :1993, or to the working-directory join at :480 flips this entry.
covers: the **PATH-unset default branch** of GLib 2.90.1's `g_find_program_for_path` as the launch load gate reaches it - what the branch decides when the environment carries no `PATH` at all, how that default differs from a set-but-empty `PATH` and from the ambient search, the exact `argv[0]` strings the branch's trailing `.` produces, the load-time consequence that the resolving process's cwd (not the desktop file's `Path=`) decides the `.` entry, and the one-line recheck that re-derives all of it.
---

# The PATH-unset default branch of GIO 2.90.1's program lookup

> **Landing status (2026-11-08, this seat's last write).** The L1 integrated an entry of this name
> at `corpus/knowledge/gio-launch-path-default-r100.md` **while this draft was being written**
> (the landed file's mtime is 02:31:20; this draft's is later). The landed entry is a shorter
> version of the same ground, sourced to **S533 alone**, and the landed registry already appends
> this entry's path to **S533's** `used-by` cell. The L1 therefore has two options, and this
> draft states which one it is written for:
>
> - **Option A (what this draft is written for):** land this draft and add the **two** further
>   `used-by` appends it needs (S528 and S532 - see `.ufo/waves/round-100/build/sources-append-r100.md`
>   section 2). This draft's front matter names S528, S532 and S533, so the read-back gate's R4
>   rule requires all three rows to name the entry. **Measured**: with the landed registry (S533
>   appended, S528/S532 not) and this draft installed, the read-back gate reports
>   `FINDING R4 S528 entry=corpus/knowledge/gio-launch-path-default-r100.md` and the same for S532
>   (2 findings, exit 1). With the S528 and S532 cells appended as well, it reports
>   `rows=469 entries=121 findings=0`, exit 0.
> - **Option B:** keep the landed entry, and take from this draft only what the landed one does not
>   carry - the **21 measured rows** of section 7 (the landed entry has seven fixture rows, all
>   re-derivable from the round's own receipts), the **load-time cwd consequence** with its three
>   extra shapes (section 4), the **separation-(3) analysis** (section 2 (3)), and the **one-line
>   recheck** with its wall time (section 6).
>
> What this draft adds over the landed entry, in one line each: the exact argv0 string table with
> its nine rows (section 3), the fact that the trailing `.`'s contribution is **lexical** and the
> declaration's separation (3) is therefore not reproducible as written (section 2 (3)), the
> locator correction that the default literal is at **`gutils.c:388`** and not inside the
> declaration's cited `:370-382` (section "Declaration" below), and the `Path=`-relative shape
> where the `./` survives the working-directory join (`{root}/work/./probe` against
> `{root}/work/probe`, rows P15/P16).
>
> Either way the L1's already-landed `corpus/lessons/round-100.md` `## Gate` block carries the admit
> and the reject this seat was asked to draft (S533 re-opened with the `:388` quote, and the staged
> `S205` reject with its flip condition), and the L1's landed SOURCES change is the S533 `used-by`
> append - which is the correct shape for Option B and half of Option A's shape.

This entry states what GLib 2.90.1 does when the environment has **no `PATH` variable at all** and a
desktop file's `Exec`/`TryExec` name is resolved at the load gate. It is the narrow branch that the
round-99 entry (`corpus/knowledge/gio-launch-env-r99.md`, sections 2 and 4) named but never
exercised: that entry states the default literal in prose and measures none of it. Every sentence
below carries a located line of one of the three fetched files or a measured row of section 7.
Quotation marks around paths are written as ASCII `'` here; the bytes on the wire are the
typographic ones (`gio-tool-launch.c:109`).

## Declaration

The frozen claim this entry answers is `.ufo/waves/round-100/claims-declaration-r100.md`, C1: at the
base revision `43309e6a` the PATH-unset default search path of the launch load gate is
`/bin:/usr/bin:.`, modelled by `tools/mado-launchenv.py` and exercised by zero frozen cases, because
both round-99 `path-unset` cases carry an **absolute** `Exec` and so return at `gutils.c:331-357`
before the PATH source is read at `gutils.c:371`. C1 requires the round-100 case file to carry a
`path-default` class of at least six cases, every label measured twice against the installed
`/usr/bin/gio`, and requires the class to separate the unset default from three neighbours: unset
vs empty, unset vs the ambient search, and the reality of the default's trailing `.`.

The declaration's cited range for the literal is `gutils.c:370-382`. **The literal is not inside
that range**: `gutils.c:371` reads the PATH source, `gutils.c:376` is the `if (path == NULL)` guard,
and the assignment `path = "/bin:/usr/bin:.";` sits at **`gutils.c:388`** (the block runs :376-389).
This entry uses the lines the quotes sit on (round-99 lesson M99-2's rule: every locator comes from
`grep -n` on the fetched bytes, never from a function's range).

## 1. The branch, in the source

The load gate resolves two names, and both call the same lookup with the **same** argument shape
(`gdesktopappinfo.c`):

| step | call | line |
|---|---|---|
| `TryExec` (only when the value is non-empty) | `g_find_program_for_path (try_exec, NULL, path)` | `:1951` |
| `Exec` argv[0] (after `g_shell_parse_argv`) | `g_find_program_for_path (argv[0], NULL, path)` | `:1993` |

The second argument is `NULL` in both, so inside the lookup the search path is the **process**
environment's, not the launch environment's:

```c
  if G_LIKELY (original_path == NULL)
    path = g_getenv ("PATH");
```

(`gutils.c:370-371`). `path` is the desktop file's `Path=` value in the third argument, so it is the
lookup's `working_dir`, not its search path.

When that `g_getenv` returns NULL, the Unix branch substitutes the default:

```c
  if (path == NULL)
    {
      ...
      /* In GLib we put . last, for security, and don't use the
       * unportable confstr(); UNIX98 does not actually specify
       * what to search if PATH is unset. POSIX may, dunno.
       */
      path = "/bin:/usr/bin:.";
    }
```

(`gutils.c:376-389`; the literal at `:388`, the security comment at `:383-386`). So the default is
three entries - `/bin`, `/usr/bin`, `.` - and the `.` is **last**, by an explicit security decision
recorded in the source.

Before the walk is ever reached, the lookup short-circuits on an absolute or slash-bearing program
(`gutils.c:331-357`):

```c
  if (g_path_is_absolute (program)
      || strchr (original_program, G_DIR_SEPARATOR) != NULL
```

(`:332-333`), then

```c
      if (g_file_test (program, G_FILE_TEST_IS_EXECUTABLE) &&
	  !g_file_test (program, G_FILE_TEST_IS_DIR))
```

(`:339-340`) and the hit is returned absolute, joined to the process cwd when the candidate was
relative (`:344-351`, returned at `:357`). **This is why the two round-99 `path-unset` cases cannot
witness the branch**: an absolute `Exec` returns here, before `:371` is read at all.

The walk itself (`:462-500`) distinguishes an **empty** entry from a **non-empty** one:

```c
      if (p == path)
        /* Two adjacent colons, or a colon at the beginning or the end
         * of 'PATH' means to search the current directory.
         */
        startp = name + 1;
      else
        startp = memcpy (name - (p - path), path, p - path);
```

(`:471-477`). The empty entry yields the **bare program name**; a non-empty entry yields
`<entry>/<program>` - so the default's `.` entry yields `./<program>`. Each relative candidate is
then joined to `working_dir` again (`:480-484`), tested executable-and-not-a-directory
(`:486-487`), and returned absolute against the process cwd (`:490-497`).

Two facts follow that a model of this branch must carry:

- **unset is not empty.** Unset means the three-entry literal above. Empty means *one* entry, the
  empty one, which is the current directory - and the candidate string differs (`./probe` vs
  `probe`), so the two produce different absolute answers (section 3).
- **the `.` of the default is a cwd entry, and the cwd is the resolving process's cwd.** The lookup
  joins the relative hit to `g_get_current_dir()` at `:494-495`, and the load gate runs at LOAD time,
  inside the `gio launch` process (section 4).

## 2. The three separations the declaration names, measured

The declaration asks the class to separate the unset default from three neighbours. Each is
measured here; the rows are section 7's.

### (1) unset != empty

A program that exists only in a system binary directory is reachable with `PATH` **unset** and not
reachable with `PATH` **set to the empty string**: the default's `/bin` and `/usr/bin` entries are
searched, the empty walk has only the cwd. Measured with `TryExec=true` (the host's `/usr/bin/true`,
which on this host `/bin` symlinks to) and `Exec={root}/probe`, so no host program is ever spawned:

- `PATH` unset -> the load gate resolves `true` and the launch happens (P13);
- `PATH=""` -> the load gate refuses: `Unable to load application information for '<desktop>'`
  (P14).

The same separation is visible without any host binary in the success region, but only lexically:
the argv0 strings differ (section 3), while the launch count, the cwd and the environment value are
identical (P1 vs P2).

### (2) unset != the ambient search

A program that exists only in a **case-private** directory is not found when `PATH` is unset -
the default does not know that directory - and is found when `PATH` is set to it:

- `PATH` unset, program only in `{root}/bin` -> load refusal (P3);
- `PATH={root}/bin` -> launch, `argv[0]={root}/bin/probe` (P4).

### (3) the default's trailing `.` is real - and what it is worth is lexical

The declaration's sentence for this separation reads: *"A bare program present only in the launch
working directory is found with `PATH` unset, and is not found by the same fixture under `PATH=""`
when the working directory differs from the process cwd."* **The found/not-found half of that
sentence is not reproducible in any fixture the round-99 oracle's schema can express**, and this
seat's measurements say so independently of the wave's other seats:

- `PATH` unset vs `PATH=""`, program at the case root, no `Path=`: **both launch** (P1, P2). The
  empty walk's single entry is the current directory too, so the program is found either way.
- `PATH` unset vs `PATH=""`, `Path={root}/work` (absolute), program in `work/`: **both launch** with
  the identical argv0 `{root}/work/probe` (P7, P8). With an absolute `Path=` the working-directory
  join at `:322-327` answers before the PATH source is read, so the PATH state cannot matter.
- `PATH` unset vs `PATH=""`, `Path={root}/work` (absolute), program at the case root: **both refuse**
  (P5, P6) - the working-directory join points at `work/`, the program is not there, and the walk
  re-joins each candidate to `working_dir` (`:480-484`), so no PATH entry can rescue it.

What the trailing `.` is worth, measured, is the **lexical** difference in the returned path: with
`PATH` unset the candidate is `./<program>` and the answer keeps the `./`; with `PATH=""` the
candidate is the bare `<program>` and the answer does not. That difference is observable whenever
the `.` entry is the one that hits, and it survives a relative `Path=`:

- `Path=` absent: `{root}/./probe` (P1) vs `{root}/probe` (P2);
- `Path=work` (relative), program in `work/`: `{root}/work/./probe` (P15) vs `{root}/work/probe`
  (P16).

A frozen case that compares only the launch status cannot see this; the frozen expectation must
carry the argv vector verbatim (section 6).

One further property of the trailing `.` is **source-located, not measured here**: the default's
entries are searched in the literal's order, so `/bin` and `/usr/bin` precede `.` (`gutils.c:388`,
walk at `:462-500`). A program present both in `/usr/bin` and in the cwd is therefore found in
`/usr/bin` first, and the child would be the host binary. This seat did not spawn a host binary to
demonstrate it; the ordering follows from the literal and the walk.

## 3. The exact argv0 strings the `.` entry produces

All rows: `Exec=probe` (a bare name) with a program file named `probe` at the case root, cwd = the
case root, the load gate's cwd.

| PATH state | `Path=` | measured `argv[0]` | row |
|---|---|---|---|
| unset (`/bin:/usr/bin:.`) | absent | `{root}/./probe` | P1 |
| set to `""` (one empty entry) | absent | `{root}/probe` | P2 |
| unset | present, empty value | `{root}/./probe` | P9 |
| set to `""` | present, empty value | `{root}/probe` | P10 |
| unset | `work` (relative), program in `work/` | `{root}/work/./probe` | P15 |
| set to `""` | `work` (relative), program in `work/` | `{root}/work/probe` | P16 |
| unset | `{root}/work` (absolute), program in `work/` | `{root}/work/probe` | P7 |
| set to `""` | `{root}/work` (absolute), program in `work/` | `{root}/work/probe` | P8 |
| unset, program in `{root}/bin` on PATH | absent | `{root}/bin/probe` | P4 |

The forms are exactly what the source predicts: the default's `.` entry makes the candidate
`./probe`, the empty entry makes it `probe`, the working-directory join at `:480-484` prefixes
`work/` to whichever of the two it is, and the final join to the process cwd at `:494-495` makes
the answer absolute.

Two traps a frozen expectation must know:

- **The `./` defeats the oracle's canonicalisation.** The oracle replaces the probe file's own path
  with `{probe}` before replacing the case root with `{root}`. The unset answer
  `{root}/./probe.sh` does not contain the probe path (the `./` sits in between), so it survives as
  `{root}/./probe.sh`; the empty answer `{root}/probe.sh` is replaced and prints as `{probe}`. The
  one-line recheck below shows both, and the difference between the two printed forms is the
  branch, not a naming accident.
- **The answer is the string, not the file.** `{root}/./probe` and `{root}/probe` name the same
  file. Any comparison that normalises (`normpath`, `realpath`) erases the only success-region
  difference between the two PATH states, and the class stops separating them.

## 4. The load-time consequence: the resolving process's cwd decides

The gate runs at LOAD time, inside the `gio launch` process: the CLI constructs the app info at
`gio-tool-launch.c:106` and the constructor's load gate is what calls the lookup. So the lookup's
cwd - the cwd of the `gio launch` process - is what the default's `.` and the empty walk's current
directory resolve against, and the same desktop file answers differently from different cwds:

- program at the case root, `PATH` unset, **cwd = the case root** -> launch, `argv[0]={root}/./probe`
  (P18);
- the same desktop file and program, **cwd = another directory** -> load refusal
  `Unable to load application information for '<desktop>'` (P17), because the `.` entry now means
  that other directory;
- the same, with `PATH=""` -> also a load refusal (P20): the empty entry is the current directory as
  well.

Two corollaries:

- **`Path=` is not the cwd for this purpose.** `Path=` is the lookup's `working_dir`; it changes what
  a relative candidate means *inside* the lookup (`:322-327`, `:480-484`), and it becomes the
  child's cwd at the spawn. The `.` entry's cwd is the process's **when `Path=` is absent or
  empty**; when `Path=` is set, the walk's `.` candidate is joined to `Path=` first (`:480-484`),
  so a program present only in the process cwd is then not found under either PATH state (P5,
  P6). A **relative** `Path=` is itself resolved against the process's cwd, because the candidate
  stays relative and `g_file_test` resolves it against the cwd (`:486`): `Path=work` with the
  program in `work/` launches from the case root (P15, `argv[0]={root}/work/./probe`) and refuses
  from another cwd (P19).
- **The refusal is the load refusal, not the launch refusal.** The message
  `Unable to load application information for '<desktop>'` is printed by the CLI at
  `gio-tool-launch.c:109` when the constructor returns NULL, and the process exits 1. The launch
  refusal (`gio-tool-launch.c:121`) is a different shape and never appears here.

The `/usr/bin` arm is the one arm that is cwd-independent: with `PATH` unset, `TryExec=true`
resolves from any cwd, because `/bin` and `/usr/bin` are absolute entries (P21, from a cwd other
than the case root).

## 5. Sources

| id | what this entry cites from it | located lines |
|---|---|---|
| S528 | the two load-gate calls and their argument shape (`NULL` search path, `Path=` working dir) | `gdesktopappinfo.c:1947-1959` (TryExec; `:1951` the call), `:1978-2004` (Exec; `:1993` the call), `:1950` and `:1992` the `working_dir` comments |
| S532 | the CLI's construction and the load refusal it prints | `gio-tool-launch.c:106` (constructor), `:109` (the refusal line), `:111` (exit 1) |
| S533 | the lookup: PATH source, unset guard, the default literal, the short-circuit, the empty-entry rule, the joins | `gutils.c:370-371` (PATH source), `:376` (guard), `:383-386` (the security comment), `:388` (the literal), `:331-357` (absolute-or-slash branch; `:332-333` the test, `:339-340` the executable-and-not-a-directory test), `:359-368` (an absolute miss returns NULL), `:462-500` (the walk; `:471-477` the empty-entry rule, `:480-484` the working-dir join, `:486-487` the test, `:490-497` the cwd join) |

The digests of all three files are in the front matter and were re-hashed by this seat; `gutils.c`
was additionally re-fetched live (HTTP 200, byte-identical to the committed round-99 bytes).

## 6. Recheck

One line, from the lane root, re-derives the branch's two answers against the installed `gio`
(`$S` is any writable scratch directory; the two commands together took **6.84 s** on this host at
load average 116-155 on 32 cores):

```sh
printf '%s' '{"id":"pd-unset","path":null,"files":{},"desktop":{"Type":"Application","Name":"n","Exec":"probe.sh"}}' | python3 .ufo/waves/round-99/controls/launchenv-probe-r99.py - --parent "$S"
printf '%s' '{"id":"pd-empty","path":[""],"files":{},"desktop":{"Type":"Application","Name":"n","Exec":"probe.sh"}}' | python3 .ufo/waves/round-99/controls/launchenv-probe-r99.py - --parent "$S"
```

`path:null` means the child environment has **no** `PATH` key; `path:[""]` means `PATH` is present
and empty. (`path:[]` is the same case - the oracle joins the entries with `:`, so an empty list and
a one-empty-entry list are the same string. **Measured**: both give
`argv=[["{root}/probe"]]`.) Measured on 2026-11-08:

```
{"launches": 1, "argv": [["{root}/./probe.sh"]], "cwd": "{root}", "env_gdf": "{root}/case.desktop"}
{"launches": 1, "argv": [["{probe}"]], "cwd": "{root}", "env_gdf": "{root}/case.desktop"}
```

(The second is `{probe}` and not `{root}/probe.sh` because the oracle replaces the probe file's own
path first, and the empty walk's answer contains that path unchanged while the unset answer's `./`
interrupts it.)

The model's own answers, for the same two states with `--path` omitted (the model process's own
PATH is unset) and with `--path ""`:

```sh
python3 -I tools/mado-launchenv.py "$CASE/case.desktop"            # ARGV[1][0]=<case>/./probe
python3 -I tools/mado-launchenv.py "$CASE/case.desktop" --path ""  # ARGV[1][0]=<case>/probe
```

`tools/mado-launchenv.py` needs `tools/mado-execargv.py` beside it and loads it by path. The
round-100 candidate copy under `.ufo/waves/round-100/build/` answers the same two strings when that
sibling is beside it, and answers `SETUP_ERROR execargv-missing` when it is not.

Flip conditions, in the order they would bite: a different default literal at `gutils.c:388`; a
`g_getenv ("PATH")` that is no longer the source at `:371`; a guard at `:376` that treats an empty
string as absent; an empty-entry rule at `:471-475` that stops meaning the current directory; a
change to the absolute-or-slash branch at `:331-357` that would let the round-99 `path-unset` cases
reach the PATH source; a change to the working-directory join at `:480-484` or to the cwd join at
`:494-495`; a change to either load-gate call at `gdesktopappinfo.c:1951` or `:1993` (in particular
a non-NULL search-path argument, which would make the branch depend on the launch environment
rather than on the process environment); a change to the load refusal at `gio-tool-launch.c:109`.

## 7. Measured rows

This seat's read-only runs, 2026-11-08, `/usr/bin/gio` sha256 `d2164260...c462`, through the
committed round-99 oracle (`launchenv-probe-r99.py`), two runs per case with agreeing labels,
`cwd = the case root` unless the row says otherwise, and the child environment carrying
`LC_ALL=C`, `HOME=<root>/h`, `PROBE_OUT=<root>/out` plus the case's own PATH entries only.
`<root>` is the case root. `files` are written 0755; `probe` is a one-line `printf` appender, so a
launch records exactly one line.

| row | fixture | PATH | measured | label |
|---|---|---|---|---|
| P1 | `Exec=probe`, program at the case root | unset | `launches=1 argv=[[{root}/./probe]] cwd={root}` | the default's `.` entry, with its `./` |
| P2 | same fixture | `""` | `launches=1 argv=[[{root}/probe]] cwd={root}` | the empty entry, bare name |
| P3 | program only in `{root}/bin` | unset | rc 1, `Unable to load application information for '<desktop>'` | the default does not know a private dir |
| P4 | same fixture | `{root}/bin` | `launches=1 argv=[[{root}/bin/probe]]` | the ambient search finds it |
| P5 | `Path={root}/work`, program at the case root | unset | rc 1, load refusal | the working-dir join points elsewhere |
| P6 | same fixture | `""` | rc 1, load refusal | same; no PATH entry rescues it |
| P7 | `Path={root}/work`, program in `work/` | unset | `launches=1 argv=[[{root}/work/probe]] cwd={root}/work` | the working-dir join answers before PATH |
| P8 | same fixture | `""` | `launches=1 argv=[[{root}/work/probe]] cwd={root}/work` | identical - the PATH state cannot matter here |
| P9 | `Path=` (present, empty), program at the case root | unset | `launches=1 argv=[[{root}/./probe]]` | an empty `Path=` does not change the answer |
| P10 | same fixture | `""` | `launches=1 argv=[[{root}/probe]]` | same |
| P11 | `Exec=./probe` (slash form), program at the case root | unset | `launches=1 argv=[[{root}/./probe]]` | the slash short-circuit answers, same string |
| P12 | `probe` is a **directory** at the case root | unset | rc 1, load refusal | the `!IS_DIR` half of the test |
| P13 | `TryExec=true` (host `/usr/bin/true`), `Exec={root}/probe` | unset | `launches=1 argv=[[{root}/probe]]` | the `/usr/bin` arm: reachable |
| P14 | same fixture | `""` | rc 1, load refusal | the `/usr/bin` arm: not reachable when empty |
| P15 | `Path=work` (relative), program in `work/` | unset | `launches=1 argv=[[{root}/work/./probe]] cwd={root}/work` | the relative `Path=` keeps the `./` |
| P16 | same fixture | `""` | `launches=1 argv=[[{root}/work/probe]] cwd={root}/work` | the empty entry's bare name |
| P17 | program at the case root | unset, **cwd = another directory** | rc 1, load refusal | the `.` is the process cwd |
| P18 | same fixture | unset, **cwd = the case root** | `launches=1 argv=[[{root}/./probe]]` | the same desktop file answers differently |
| P19 | `Path=work` (relative), program in `work/` | unset, cwd = another directory | rc 1, load refusal | a relative `Path=` resolves against the process cwd |
| P20 | program at the case root | `""`, cwd = another directory | rc 1, load refusal | the empty entry is the process cwd too |
| P21 | `TryExec=true`, `Exec={root}/probe` | unset, cwd = another directory | `launches=1 argv=[[{root}/probe]]` | the `/usr/bin` arm is cwd-independent |

Method notes for the reader who wants to reproduce a row: the oracle's `path` field is `null` for
"no `PATH` in the child environment" and a list for a set one (`[""]` is set-and-empty); the oracle
runs `gio launch` with `cwd = the case root` and builds the child environment itself, so a case with
`path:null` never carries a host PATH; the `TryExec` rows use `true`, whose resolution at the load
gate is a lookup and never a spawn - no host binary is executed by any row of this table.

## 8. Named limits

- **The `/usr/bin` arm is a lookup, never a spawn.** The rows that use `TryExec=true` measure the
  *search*, not the execution; a row that put `true` in `Exec` would spawn the host binary, which
  this seat did not do.
- **The default's entry order (`/bin`, `/usr/bin`, `.`) is source-located only** (section 2's last
  paragraph). Demonstrating it in the success region would require spawning a host binary.
- **`/bin` is a symlink to `usr/bin` on this host**, so "exists only in `/usr/bin`" and "exists only
  in `/bin`" are the same directory here; the row P13/P14 pair therefore witnesses the *presence of
  a system binary directory* in the default, not the two entries separately.
- **The argv0 strings are cwd-dependent by construction** (section 4). Any harness that runs the
  model or the oracle from a cwd other than the case root manufactures a false miss, and the
  model's own `find_program` joins the relative hit to `os.getcwd()`.
- **The `.`/`..` normalisation of the child's cwd is out of scope** here; this entry states the
  lookup's answers, not the spawn's cwd rules.
- **Multi-spawn ordering, `DBusActivatable`, the portal path and the `gio-launch-desktop`
  wrapper's environment scrubbing stay out of scope**, as in the round-99 entry.
- **The model's structural rule (no `gio` in the candidate) is unchanged**: `tools/mado-launchenv.py`
  models the walk from the source lines; every measurement in section 7 was produced by an
  instrument that runs the installed `gio`, never by the candidate.
