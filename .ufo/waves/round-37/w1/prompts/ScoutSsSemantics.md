# ScoutSsSemantics — scout seat, mado round 37 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: scout

Find and OPEN a primary source for what `ss -x` reports for a connected unix stream socket: the meaning of Recv-Q and Send-Q for ESTAB unix stream rows, the peer inode column, and the users:(...) process column (iproute2 ss(8) man page — `man 8 ss` locally and/or https://man7.org/linux/man-pages/man8/ss.8.html — and the kernel's sock_diag/unix_diag documentation or source if the man page is silent). Quote ≤25 words per fact with its location and access date. Then check the live host: `ss -xpa | grep -F .socket2.sock` and the matching peer rows — confirm the column layout the C2 contract assumes (Netid State Recv-Q Send-Q LocalAddr LocalInode PeerAddr PeerInode users). Report any layout variant (e.g. missing users column for other-uid processes).
