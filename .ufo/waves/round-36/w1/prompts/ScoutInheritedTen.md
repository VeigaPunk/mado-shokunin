# ScoutInheritedTen — scout seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: scout

Audit the ten round-35 paths still dirty in the lane work tree (`git -C /home/vgpnk/Projects/shokunin/mado-shokunin status --porcelain`): for each, diff the working-tree bytes against the committed blob, say what changed (seat report revisions, evidence txt, two untracked scratch dirs) and recommend commit-versus-revert with a reason. Do not run any mutating git command; `git diff --stat`/`git show` only.
