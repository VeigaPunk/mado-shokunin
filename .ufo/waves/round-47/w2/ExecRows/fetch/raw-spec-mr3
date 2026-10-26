* Name: xdg-terminal-exec
* Start Date: 2019-01-29

# Summary

Proposal for XDG Default Terminal Execution Specification describing the way
implementations should handle selecting and launching terminal emulators, including
handling of emulators cli arguments.

The configuration spec is crafted in image of
[mime-apps-spec](https://specifications.freedesktop.org/mime-apps-spec/latest)
using different names in similar structure, governed by
[basedir-spec](https://specifications.freedesktop.org/basedir-spec/latest).

Working implementation of this proposal can be found here:
https://github.com/Vladimir-csp/xdg-terminal-exec/blob/master/xdg-terminal-exec
https://gitlab.freedesktop.org/Vladimir-csp/xdg-terminal-exec/-/blob/master/xdg-terminal-exec

# Motivation

Currently there is no overarching specification to handle selection of default
terminal emulator application compatible with most major DEs or setups without a
DE.

# Default Terminal Execution Specification

This spec consists of three parts:

1. Additional keys for the
   [desktop-entry-spec](https://specifications.freedesktop.org/desktop-entry-spec/latest/)
   that allow terminals to define how they are invoked.
2. The configuration spec for defining and customizing default terminals
   in context of Desktop Environments and user overrides. This is crafted in
   image of
   [mime-apps-spec](https://specifications.freedesktop.org/mime-apps-spec/latest)
   using different config files in similar structure, governed by
   [basedir-spec](https://specifications.freedesktop.org/basedir-spec/latest).
3. A CLI interface to launch the configured terminal from (2) with the cli
   options corresponding to keys from (1). Working reference implementation of
   this CLI interface can be found here:
     - [github.com/Vladimir-csp/xdg-terminal-exec](https://github.com/Vladimir-csp/xdg-terminal-exec/)
     - [gitlab.freedesktop.org/Vladimir-csp/xdg-terminal-exec](https://gitlab.freedesktop.org/Vladimir-csp/xdg-terminal-exec/)

Terminal emulators (with their exec arguments) are described by stock Desktop
Entries located in `applications` subdirs of XDG data hierarchy.

Preferred terminals are configured by listing their
[entry IDs](https://specifications.freedesktop.org/desktop-entry-spec/latest/file-naming.html#desktop-file-id)
in configuration files. Optionally an entry ID can be suffixed with
[action ID](https://specifications.freedesktop.org/desktop-entry-spec/latest/extra-actions.html),
delimited by `:` (`entry-id.desktop:action-id`).

## Desktop entry for a terminal

Stock Desktop Entries for terminal emulator applications are used. Entry
eligible for selection should have `TerminalEmulator` Category and
`X-TerminalArgExec=` key (`X-TerminalArgExec=` while the Specification is in
proposed status) which contains command execution argument: an argument to be
placed before command if it is requested. If the terminal accepts commands
without special argument, this key should be explicitly set to an empty value
(execution argument will be omitted). Although in this case it is recommended to
use `--` if the terminal handles it correctly.

### Additional argument keys

Implementations should expect these keys prefixed with `X-` while the
Specification is in proposed status.

If argument expects a value and is defined as ending with `=`, value should be
appended to the same argument without a white space.

- `X-TerminalArgAppId=` - argument to set `app-id` (Wayland) or `WM_CLASS`
  (X11). Terminal is expected to use same argument for either backend.
- `X-TerminalArgTitle=` - argument to set window title.
- `X-TerminalArgDir=` - argument to set working directory.
- `X-TerminalArgHold=` - argument to hold terminal open after requested command
  exits.

Since terminal emulators have varying set of features, any option support is
considred best effort.

Whether launched terminal process waits for command to finish or exits
immediately (i.e. after sending IPC request to a master process) is not defined
by the this Specification. Some IPC-using terminals provide separate entries or
[actions](https://specifications.freedesktop.org/desktop-entry-spec/latest/extra-actions.html)
for launching separate processes without IPC.

## Configuration

### Location

Configuration files are named `${desktop}-xdg-terminals.list` or
`xdg-terminals.list` and placed in XDG config hierarchy.

`${desktop}` here is a lowercased string that can be matched
(case-insensitively) against items of `$XDG_CURRENT_DESKTOP` (a colon-separated
list of names for the current DE) in order of decreasing priority.

Lower priority fallback config files (for upstream/distribution usage) are
paced in system part of XDG data hierarchy within `xdg-terminal-exec` subdirs.

Default paths for configuration and data are resolved into (in order of
decreasing priority):

- config files:
  - main config sequence (in `${XDG_CONFIG_HOME}:${XDG_CONFIG_DIRS}`):
    - `${HOME}/.config/${desktop}-xdg-terminals.list`
    - `${HOME}/.config/xdg-terminals.list`
    - `/etc/xdg/${desktop}-xdg-terminals.list`
    - `/etc/xdg/xdg-terminals.list`
  - upstream/distribution config fallbacks (subdirs in `${XDG_DATA_DIRS}`):
    - `/usr/local/share/xdg-terminal-exec/${desktop}-xdg-terminals.list`
    - `/usr/local/share/xdg-terminal-exec/xdg-terminals.list`
    - `/usr/share/xdg-terminal-exec/${desktop}-xdg-terminals.list`
    - `/usr/share/xdg-terminal-exec/xdg-terminals.list`
- desktop entries (in `${XDG_DATA_HOME}:${XDG_DATA_DIRS}`):
  - `${HOME}/.local/share/applications/`
  - `/usr/local/share/applications/`
  - `/usr/share/applications/`

### File format

The format is a simple newline-separated list with decreasing priority.

Empty lines and lines starting with `#` are ignored, dangling whitespaces are
trimmed.

Line format:

`terminal.desktop` or `terminal.desktop:action`: marks entry for explicit
selection.

`-terminal.desktop` excludes entry from fallback selection.

`+terminal.desktop` protects entry from fallback exclusion.

Special directives for modifying behavior of implementations may be present in
config files. Directives that are not listed by this Specification and are not
understood by a particular implementation should be discarded.

Directives should not contain `.desktop` substring in them. And it is
recommended to start directives with a symbol that is not valid for entry ID,
i.e. `/`.

## Priority of selecting an entry

- A list of explicitly preferred entry IDs and fallback exclusions is composed
  by taking previously unseen IDs:
  - from each dir of XDG config hierarchy in the order of decreasing priority:
    - from `${desktop}-xdg-terminals.list` files in the order of
      `$XDG_CURRENT_DESKTOP` items
    - from `xdg-terminals.list`
  - from each dir of system XDG data hierarchy in the order of decreasing
    priority:
    - from `xdg-terminal-exec/${desktop}-xdg-terminals.list` files in the order
      of `$XDG_CURRENT_DESKTOP` items
    - from `xdg-terminal-exec/xdg-terminals.list`
- Each entry from the explicit selection list is checked for applicability:
  - presense of `TerminalEmulator` category
  - validation by the same rules as in Desktop Entry Specification, except
    `*ShowIn` conditions
  - entry is discarded if it does not pass the checks
  - the first applicable entry is used
- If no applicable entry is found, fallback selection is performed from entries
  in XDG data hierarchy (except those discarded and excluded earlier). Each is
  checked for applicability:
  - presense of `TerminalEmulator` category
  - validation by the same rules as in Desktop Entry Specification, now
    including `*ShowIn` conditions
  - the first applicable entry is used
    - the order in which found entries under the same base directory are checked
      in is undefined
- If no applicable entry is found, an error is returned.

## Syntax

```
xdg-terminal-exec [-[-]options ...] [command [arguments ...]]
```

A set of arguments each starting with `-` and located at the beginning of the
input command line is considered to be options processed by the implementation
and should always be discarded from the resulting command line, inlcuding `-e`
or any matching execution argument. Option processing should end on `--`, `-e`,
or matching execution argument.

Each option should be monolithic: as a single argument, value (if applicable)
delimited by `=`.

### Options for modifying terminal's behavior

- `--app-id=`
- `--title=`
- `--dir=`
- `--hold`

Requested options then translated into arguments according to the keys existing
in the terminal's Desktop Entry (or discarded otherwise). If `--dir=` option is
given, but terminal's entry lacks `X-TerminalArgDir=` key, implementation should
instead change dir before executing terminal.

### Execution argument and Execution

If a command (with or witout its arguments) is given, and `TerminalArgExec=` key
is not explicitly empty, then the value `TerminalArgExec=` (defaulting to `-e`)
is appended as the next argument.

Next the command and arguments are passed as is.

The resulting command is executed without forking.

### Options for returning data instead of executing terminal

- `--print-id`: print selected Desktop Entry ID. Action is appended delimited
  by `:`.
- `--print-path`: print absolute path to selected Desktop Entry. Action is
  appended delimited by `:`.
- `--print-content`: print content of selected Desktop Entry.
- `--print-cmd[=printf_sequence]`: print resulting command line, delimited by
  given printf sequence, `\n` by default. If sequence is `\n`, command output
  is terminated with newline.
- `--print-delimiter=printf_sequence`: printf sequence to be used as the
  delimiter between multiple requested print statements, `\n` by default. If
  sequence is `\n`, overall output is terminated with a newline (without
  duplication in case command output already terminated on a newline).

Depending on selected data options, data is returned in the following order:

- id
- path
- content
- cmd

## Limitations and compliance of terminals

There is no mechanism for handling special quoting and arguments/strings that
may be required for some terminals.

The expected behavior is modelled after xterm and is arguably common for a
majority of terminals. This example:

```
xdg-terminal-exec nano "some file with spaces"\ and\ unquoted\ spaces second\ file
```

is expected to launch `nano` editing two files named
`some file with spaces and unquoted spaces` and `second file`.
