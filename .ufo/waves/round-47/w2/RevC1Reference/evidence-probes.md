# RevC1Reference — probe evidence (all commands run 2026-10-26, cwd /fast/scratch/hyaku/mado-r47/RevC1Reference)

Host: /bin/sh -> /usr/bin/bash, bash 5.3.20(1)-release, POSIX mode (confirmed `$BASH_VERSION $POSIXLY_CORRECT` = `5.3.20(1)-release y`).
No tools installed; no pacman; no packages.

## A. bash `IFS=<ch> read -r` remainder rule (draft read_split target)

```
bash -c 'IFS=: read -r a r <<<"x:y:";   echo "1 a=[$a] r=[$r]"'   -> 1 a=[x] r=[y]
bash -c 'IFS=: read -r a r <<<"x:y::";  echo "2 r=[$r]"'          -> 2 r=[y::]
bash -c 'IFS=: read -r a r <<<"x:y:z:"; echo "3 r=[$r]"'          -> 3 r=[y:z:]
bash -c 'IFS=: read -r a r <<<"x::";    echo "4 r=[$r]"'          -> 4 r=[]
bash -c 'IFS=: read -r a b r <<<"x:y:z:"; echo "5 a=[$a] b=[$b] r=[$r]"'  -> 5 a=[x] b=[y] r=[z]
bash -c 'IFS== read -r o v <<<"--title=a:b="; echo "6 o=[$o] v=[$v]"'     -> 6 o=[--title] v=[a:b]
sh    -c 'IFS=: read -r a r <<<"x::y:"; echo "7 a=[$a] r=[$r]"'   -> 7 a=[x] r=[:y:]   (POSIX mode)
sh    -c 'IFS== read -r o v <<<"--title=="; echo "8 o=[$o] v=[$v]"' -> 8 o=[--title] v=[]
bash -c 'IFS== read -r o v <<<"--title=a==b"; echo "9 v=[$v]"'    -> 9 v=[a==b]
```
Draft rule (drop exactly one trailing delimiter iff the rest before it holds no delimiter) reproduces all nine.
POSIX-mode spot check r=[y::] identical to bash mode.

## B. command -v edge names

```
bash -c 'command -v -;  echo rc=$?'  -> rc=1            (draft: False -> agree)
bash -c 'command -v -x 2>/dev/null; echo rc=$?' -> rc=2 (draft: False -> agree)
```

## C. PATH

```
(cd pb && PATH= bash -c 'command -v foo; echo rc=$?')   -> ./foo, rc=0   (empty PATH = cwd; draft agrees)
(cd pb && PATH=: bash -c 'command -v foo; echo rc=$?')  -> ./foo, rc=0   (empty entries = cwd; draft agrees)
bash -c 'unset PATH; command -v sh; echo rc=$?'         -> (no output), rc=1
```
NOTE: despite the bare-probe rc=1, the RESOLVER with PATH unset finds its externals via bash's built-in
default path and resolves bare Exec words against it — see E (e3/e3b). The draft instead refuses
(OOC "PATH unset", mado-terminal.py:374).

## D. printf %b

```
printf '%b' 'a\101b'  -> a A b        (octal \NNN accepted; draft agrees)
printf '%b' '\0101'   -> A
printf '%b' 'a\x41b'  -> a A b
printf '%b' '\u0041'  -> A            (ASCII \u accepted; draft agrees)
printf '%b' '\u00e9'  -> 303 251 (UTF-8 e-acute; draft refuses = OOC-DECLARED)
printf '%b' 'x\cy'    -> x            (\c stops that call; draft agrees)
printf '%b' 'A\zB'    -> A \ z B      (unknown escape literal; draft agrees)
```

## E. e2e real-vs-draft matrix (harness e2e.py, root-normalized stdout+rc; stderr not compared)

14 AGREE, 4 DIVERGE. Full transcript: `evidence-e2e.txt` (this dir). Summary:

```
e1a-digit-listed      AGREE (real rc0 2048qt.desktop / draft rc0 2048qt.desktop)
e1b-digit-fallback    AGREE
e1c-letter-control    AGREE
e2-home-unset         DIVERGE  REAL rc=0 out=foot.desktop   | DRAFT rc=2 MADO_TERM_OUT_OF_CONTRACT: HOME unset
e3-path-unset         DIVERGE  REAL rc=1 No valid terminal…  | DRAFT rc=2 MADO_TERM_OUT_OF_CONTRACT: PATH unset
e3b-path-unset-exec-sh DIVERGE REAL rc=0 out=foot.desktop   | DRAFT rc=2 MADO_TERM_OUT_OF_CONTRACT: PATH unset
e2b-home-unset-default-paths DIVERGE REAL rc=1 err="…line 148: HOME: unbound variable" | DRAFT rc=2 …HOME unset
e8-content-plus-cmd   AGREE    (content then delimiter then cmd words)
e9-actions-empty      AGREE    (both rc 1)
e12-content-no-final-nl AGREE  (both rc 1 here; shcat drops unterminated last line)
e14-action-id-path    AGREE    (id:action and path:action)
e15-execarg-consumes  AGREE    (execarg matches before --hold handling; command empty)
s1-test-beats-cmd     AGREE
s2-unknown-option-discard AGREE
s3-last-cmd-delim-wins AGREE    (foot<TAB>-e<TAB>a)
s6-upper-desktop      AGREE    (XDG_CURRENT_DESKTOP=HYPRLAND lowered)
e17-empty-delimiter   AGREE    (id+path concatenated, no trailing newline)
e18-unreadable-list   AGREE    (both rc 1, stdout empty; real stderr has shell "line 361:" prefix, draft bare path)
```

## F. builtin/keyword tables vs host bash 5.3.20

```
compgen -b diff vs draft BASH_BUILTINS: empty both ways (61/61)
compgen -k diff vs draft BASH_KEYWORDS: empty both ways (22/22)
draft SCRIPT_FUNCTIONS: 24 names, complete vs the script's function list.
```

## G. harness notes

- The resolver needs tr/find/awk/ls/md5sum/mkdir/rm on PATH (the counter's clause-i sandbox supplies
  exactly those seven as /oracle/bin). The harness mirrors that with <root>/ext.
- First harness revision mis-probed alias expansion in NON-POSIX bash (eval "2048-qt.desktop" rc 127);
  POSIX mode (as run via #!/bin/sh) expands digit-leading aliases rc 0 — draft agrees.
