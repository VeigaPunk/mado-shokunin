# MutPtrNoSetup — mutation-tester seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: mutation-tester

Mutate the C2 gate in /tmp: remove the `setup_ok` conjunct from the verdict. Show that a tree with no round-36 sections then exits 0 (the absence-is-a-pass defect the gate was built to prevent), with the exit code.
