---
source: S533 (GLib 2.90.1 gutils.c 65086c293646bf83884f56f54bb5e2e872adb28ee77f1223d6d9f095a75e3771, 100534 B, 3245 L - re-opened 2026-11-08 at its recorded URL, HTTP 200; the PATH source at :370-371, the unset default at :376-389 with the literal at :388, the absolute-or-slash short-circuit at :332-357 with the exec/IS_DIR test at :339-340, and the entry walk at :462-500 with the empty-entry rule at :471-475 and the exec test at :486-487). Measured against the installed `/usr/bin/gio` sha256 d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462 (glib2 2.90.1-1) through the round-99 oracle module.
verified-at: 2026-11-08 - the fetched bytes hash to the S533 pin (`sha256sum` -> `65086c29...3771`) at HTTP 200; every label below is an oracle measurement in `.ufo/waves/round-100/receipts/c1-cases-r100.txt` (two runs per case, `agreed: true`); the tool answer is the round-100 counter's run at revision `219e14f4` (`.ufo/waves/round-100/receipts/c1-measured-r100.txt`).
recheck: 180d - re-pull `gutils.c` at the next GLib tag and re-open the block at :370-389; a change to the literal `/bin:/usr/bin:.`, to the `if (p == path)` empty-entry rule, or to the `working_dir` join inside the walk flips this entry. Also flips when `glib2` leaves 2.90.1-1 or `/usr/bin/gio` changes its digest.
covers: what `g_find_program_for_path` decides when the launching process has **no PATH** - the literal `/bin:/usr/bin:.` default, why `.` is last, the three observable consequences (a program in the launch working directory resolves and keeps a `./` in its returned path; a program reachable only through a case-private directory is refused; a `TryExec` name that exists only in the system directories still passes the load gate), the empty-vs-absent distinction (`PATH=""` is one empty entry = the process cwd, so it finds the working-directory program as a bare name and not the system one), the load-time consequence (the gate runs when the desktop file is loaded, so `gio launch` resolves against its own cwd), and the named limits (entry order is unobservable on this surface; a spawned system binary writes no probe record).
---

# The unset-PATH default that decides a launch

Round 99 modelled the launch spawn environment but froze no case in which the launching process
has **no `PATH`**; the two `path-unset` cases it shipped give an absolute `Exec` and return at
`gutils.c:332-357` before the PATH source is read. Round 100 measured that branch against the
installed `gio` and cored it: ten frozen cases in four classes, six counted mutants, a seeded fresh
leg. This entry is the branch itself.

## 1. The rule

`g_find_program_for_path` takes `path` from three places (`gutils.c:370-373`): the argument when a
caller gives one, otherwise `g_getenv ("PATH")`. On UNIX, a NULL path — the variable **absent** from
the environment — is replaced by a literal:

```
      /* In GLib we put . last, for security, and don't use the
       * unportable confstr(); UNIX98 does not actually specify
       * what to search if PATH is unset. POSIX may, dunno.
       */
      
      path = "/bin:/usr/bin:.";
```

(`gutils.c:376-389`; the assignment is `:388`, the comment `:383-386`.) The three entries then walk
with the ordinary loop (`:462-500`): each entry gets `program` appended, the working directory is
joined onto a relative candidate when `working_dir` is given (`:479-484`), and a candidate is a hit
when it is executable and not a directory (`:486-487`). A hit that is still relative is returned
absolute against the **process cwd** (`:494-496`), which is why the `.` entry answers
`<cwd>/./probe` and not `<cwd>/probe`.

An **empty** path string is not the same thing: `if (p == path)` treats two adjacent separators — or
a separator at either end — as "search the current directory", and `startp` becomes the bare program
name (`:471-475`). `PATH=""` is therefore exactly one empty entry.

## 2. What that decides, measured

Each row is an oracle measurement of `gio launch` with `path: null` (no PATH in the child
environment) or `path: []` (`PATH=""`); the labels live in
`.ufo/waves/round-100/controls/launchenv-cases-r100.json` (77 cases) and their receipts in
`receipts/c1-cases-r100.txt`.

| Fixture | PATH | Outcome | argv[0] |
|---|---|---|---|
| `Exec=probe`, program at the case root | absent | launch | `{root}/./probe` (the `.` entry, `./` kept) |
| same fixture | `""` | launch | `{root}/probe` (the bare name) |
| `Exec=probe`, program only in `{root}/bin` | absent | refusal `load` | — (the default does not know that directory) |
| same fixture | `{root}/bin` | launch | `{root}/bin/probe` |
| `TryExec=sh`, `Exec={root}/probe.sh` | absent | launch | `{probe}` (`sh` resolves in `/bin` or `/usr/bin`) |
| same fixture | `""` | refusal `load` | — (`{root}/sh` does not exist) |
| `Path={root}/work`, `Exec=probe`, program in `work/` | absent | launch, child cwd `{root}/work` | `{root}/work/probe` |

Two consequences for anyone modelling this:

1. **The load gate runs at load time, not at spawn time.** `gio launch` resolves `Exec` (and
   `TryExec`) while constructing the app info, so the resolution uses the *launcher's* cwd. The same
   desktop file, same `Exec`, same absent PATH refuses from any other cwd — measured (a hand-built
   copy under a different directory printed `Unable to load application information`). A model that
   resolves the program at spawn time will accept files `gio` refuses.
2. **`TryExec` is the only oracle-observable way to read the system arm.** A desktop file whose
   `Exec` names a program that exists only in `/bin` or `/usr/bin` spawns that program, which writes
   no probe record, so the case's label cannot separate the models. `TryExec=<system program>` with
   an `Exec` that is the case's own probe keeps the whole surface inside the case root.

## 3. The model and its proof

`tools/mado-launchenv.py` answers the branch read-only: `--path` absent and no `PATH` in its own
environment means *unset* (the default); `--path ""` means one empty entry. Its selftest carries
five checks over the branch (`st-unset-default-dot-launch`, `st-empty-string-no-dot`,
`st-dot-entry-explicit`, `st-unset-tryexec-privbin-miss`, `st-unset-tryexec-dot-hit`), and six
anchored mutants of the program lookup are killed by the frozen case set:

| mutant | what it breaks | killed by |
|---|---|---|
| `m1` | default without its trailing `.` | `pd-dot-root` |
| `m2` | unset treated as empty | `pd-dot-root`, `pd-sysbin-unset` |
| `m3` | the working-directory join inside the walk | `tx-viawd`, `pd-wd-unset` |
| `m4` | the empty entry read as `/bin` | `pe-empty-str`, `pd-empty-root`, `pd-sysbin-empty` |
| `m5` | the not-a-directory half of the executable test | `pd-abs`, `pd-onpath` |
| `m6` | a relative hit normalised (no `./`) | `pe-dot`, `pd-dot-root` |

`m1` and `m2` **survive the round-99 case set alone** — that survival is the measured proof that
the new class is load-bearing rather than a relabelling
(`.ufo/waves/round-100/controls/launchenv-mutants-r100-probe.txt`).

## 4. Named limits

- **Entry order is not separable on this surface.** No fixture the schema can express distinguishes
  `.`-first from `/bin`-then-`/usr/bin`-then-`.`: a program that exists in two of the entries is
  found either way, and the only shape difference (the `./`) is produced by the `.` entry whichever
  position it holds. The class pins the entry *set* and the `.`-shape, not the order.
- **A spawned system binary is invisible** to the probe-record surface, so `Exec` on a `/bin` program
  cannot be labelled; `TryExec` carries that arm (section 2).
- **`Terminal=true` is out of reach here**: this host carries `/usr/bin/xdg-terminal-exec`, so a
  `Terminal=true` case with an absent PATH would start a real terminal. The class keeps
  `Terminal` absent.
- The branch is per-process: a launcher with PATH absent and a child that sets PATH are two different
  surfaces, and nothing here claims anything about the child's own lookups after spawn.

## 5. Provenance

- **Declaration:** `.ufo/waves/round-100/claims-declaration-r100.md` C1; frozen predicate
  `PRED-C1-r100-v1`; pre-file amendments A1-A5 in `plans/round-100.md`.
- **Sources:** S533 (this entry's only row), re-opened 2026-11-08.
- **Recheck:** 180 days, or on a GLib tag bump / `gio` digest change — re-open `gutils.c:370-389` and
  re-run `python3 -I tools/mado-launchenv.py --selftest` plus
  `python3 -I quality/counters/c1-r100-launchenv-path.py ... --rev worktree`.
