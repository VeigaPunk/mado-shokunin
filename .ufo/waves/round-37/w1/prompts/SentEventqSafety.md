# SentEventqSafety — sentinel seat, mado round 37 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: sentinel

Security and privacy review of the C2 contract (registration + the counter) before a line of the tool exists: (1) ss -xpa exposes process names/pids of every unix socket — what should a committed `--snapshot-out` contain at most (propose the minimal row set) and what must never be committed; (2) journalctl output privacy — confirm the contract prints counts only; (3) any path where the tool could block or stall the compositor (it must never connect; is `hyprctl getoption` itself a request-socket client that could freeze Hyprland per the IPC page's synchronous-evaluation rule — read /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md row S186 and say whether a one-shot getoption is safe); (4) subprocess hygiene (no shell=True, timeouts). Findings with severity and the contract line each one changes.
