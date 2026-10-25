# ScoutD1Facts — scout seat, mado round 36 wave 1

Lane: /home/vgpnk/Projects/shokunin/mado-shokunin
Role: scout

Re-derive the round-35 report-ordering facts: the last round-35-labelled commit on `master` before the spot-check, the commit that added `.ufo/reports/round-35/mado.md` on the FLEET repo (`git -C /home/vgpnk/Projects/shokunin log -1 --format='%H %ad' --date=iso -- .ufo/reports/round-35/mado.md`), and every lane commit after the report's first commit. Report whether the report landed last, the round-35 lane tip hash, and the exact one-sentence erratum round 36 owes.
