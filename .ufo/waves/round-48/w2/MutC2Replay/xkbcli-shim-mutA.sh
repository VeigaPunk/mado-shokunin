#!/bin/sh
# MutC2Replay scratch shim (mutant A) - lives only in /fast/scratch, never installed.
# Fakes the PRED-C2-r48 clause_r replay: positive compile -> forged bytes (rc 0);
# the three negative probes -> rc 1/1/0 with the required stderr markers.
case "$1" in
compile-keymap)
  case "$*" in
  *--test*)
    case "$*" in
    *"--layout zz"*)
      echo "xkbcommon: ERROR: [XKB-338] Couldn't find file \"symbols/zz\" in include paths" >&2
      exit 1 ;;
    *"--variant nope"*)
      echo "xkbcommon: ERROR: [XKB-661] Couldn't process include statement for 'br(nope)'" >&2
      exit 1 ;;
    *"nope:nope"*)
      echo "xkbcommon: ERROR: [XKB-595] Unrecognized RMLVO option \"nope:nope\" was ignored" >&2
      exit 0 ;;
    esac
    exit 1 ;;
  *)
    cat "$FORGED_KEYMAP"
    exit 0 ;;
  esac ;;
esac
exec /usr/bin/xkbcli "$@"
