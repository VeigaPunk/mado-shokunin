# OracleImapStream

Axis: **C1 operability** — recall for a process-capable stdlib constructor and correct command binding. C2 calibration is outside this assignment.

The proposal at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/oracles/ImapStream.json` contains the minimal Python transcript (`import imaplib`; `imaplib.IMAP4_stream(["loginctl"])`). Expected finding: class `live_probe`, command `loginctl:list-sessions`, evidence `observed`.

Static reasoning: `IMAP4_stream.__init__` stores the passed list in `self.command` and invokes `IMAP4.__init__(self)`. The base initializer calls `self.open(...)`; that dispatches to the subclass override, which passes the bound `self.command` directly to `subprocess.Popen(..., shell=True)`. Python's POSIX `shell=True` sequence semantics make the first list element the shell command string, so the launched command is `loginctl`. systemd's `VERB_DEFAULT_NOARG` declaration selects `list-sessions` when no verb is supplied. That is a session-listing probe, hence `live_probe` and the canonical command `loginctl:list-sessions`. The call path and binding are explicit, not an opaque callback or recursive body, so `observed` is the appropriate evidence level. The evidence label is an oracle expectation, not a report of live execution.

Sources: CPython v3.14.8 saved source at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/sources/SourceImap/imaplib-v3.14.8.py:202-224,1795-1814`; its receipt at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-21/w1/sources/SourceImap/receipt.json` records the version and SHA-256. Public semantics: [Python subprocess Popen documentation](https://docs.python.org/3.14/library/subprocess.html#popen-constructor), [systemd loginctl default verb](https://github.com/systemd/systemd/blob/main/src/login/loginctl.c#L279), and [VERB_DEFAULT_NOARG definition](https://github.com/systemd/systemd/blob/main/src/shared/verbs.h#L107-L108).

Verification: static source reasoning only. The transcript was not executed; no scanner/tool was opened or run, and no build, test, measurement, installation, or live host probe was performed.
