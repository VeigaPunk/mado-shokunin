# ScoutS189 — scout seat, mado round 37 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: scout

Re-open the Hyprland v0.56.2 event manager yourself: `curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/EventManager.cpp -o /dev/shm/mado37-ScoutS189/EventManager.cpp`, `cmp` with /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-37/fetch/S189.bin, then map the delivery path with line numbers: postEvent (queueing, the shutdown suppression :165), the cap check (:169-175: is removal at `>= 64` queued, and what exactly is removed/closed), flushClient (:136-155: partial-write resume via writeOffset, EAGAIN/EWOULDBLOCK keep, EINTR retry, other errors), and when flush is attempted (event-loop writable callback?). Also locate the socket's listen/accept and whether accepted fds are non-blocking. Report a line-cited state machine and any sentence of /home/vgpnk/Projects/shokuknow/merge/mado/knowledge/corpus/knowledge/event-delivery-limits-r26.md the bytes contradict.
