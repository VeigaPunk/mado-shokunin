# RevRowsUnchanged — reviewer seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: reviewer

Verify that no `corpus/SOURCES.md` row has been edited in place since the round-35 tip: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff --numstat 7a068cb master -- corpus/SOURCES.md` (expect empty) and `git -C /home/vgpnk/Projects/shokunin/mado-shokunin log --oneline 7a068cb..master -- corpus/SOURCES.md`. Report the row count at both revisions and the command output. If a row did change, name it.
