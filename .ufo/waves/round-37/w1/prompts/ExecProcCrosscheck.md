# ExecProcCrosscheck — executor seat, mado round 37 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: executor

Independent live cross-check of the event-socket subscriber census WITHOUT ss: write /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-37/w1/scratch/ExecProcCrosscheck/proc-census.py that reads /proc/net/unix (inode, path, state) and maps socket inodes to processes through /proc/<pid>/fd symlinks (`socket:[inode]`), then derives which processes hold the client end of a connection to `$XDG_RUNTIME_DIR/hypr/<instance>/.socket2.sock`. Unix-socket peer inodes are not in /proc/net/unix; find a sound way (e.g. `ss -xpa` only as a comparison, or the server inode set plus /proc/<compositor pid>/fd) and say exactly what /proc can and cannot prove. Run it read-only, compare with `ss -xpa` output, and report agreement or disagreement per subscriber (comm, pid, fd). Never connect to any socket.
