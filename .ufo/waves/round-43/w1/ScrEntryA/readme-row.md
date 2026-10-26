# corpus/README.md row - SUPERSEDED, do not land this file

The coverage-map row for `knowledge/hyprland-gkeep-geometry-r43.md` is owned by seat
`ScrSkillProvince` (`.ufo/waves/round-43/w1/ScrSkillProvince/readme-row.md`), which ran
`quality/check-index-rows.py` against it (`errors=0`, plus five negative controls). **Exactly one**
row matching `^\| \`knowledge/hyprland-gkeep-geometry-r43.md\`` may sit in `corpus/README.md`:
PRED-C2-r43 clause f counts those rows and admits only a count of 1, so landing two rows fails the
counter.

This file is kept only as the record that the entry seat also drafted a row. It is not the row to
insert. The earlier draft (kept here for audit) began:

| `knowledge/hyprland-gkeep-geometry-r43.md` (MADO-R43-1, round 43; assimilation of the gkeep-geometry theme of the shokuknow package) | What decides the size of the host's gkeep window, end to end: three host rules for one class (float on, centre on, `size 420 500`, regex `^(org.omarchy.gkeep)$`), the anchored `RE2::FullMatch` matcher, a rule size stored as an expression and consumed only in the floating algorithm's first-map branch, the target and window boxes, the animation GOAL behind `hyprctl clients -j` `size`, the client's own `set_default_size(420, 500)`, and today's census (4 clients, 0 floating, 0 gkeep); the rendered size stays UNK. | S290-S299 |

One wording change since that draft: the entry's `ground:` line now opens with the
`ScrSkillProvince` Holds cell's own sequence ("what determines the size of the host's gkeep
window, end to end"), so `check-index-rows.py`'s `holds-no-overlap` WARN stays silent without
editing the row.
