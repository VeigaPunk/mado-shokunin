# round-14 regular-file source-target predicate mutants
# Candidate anchors follow round-13 covering.spec's @defect/@old/@new format.
# @old/@new are exact anchors in the landed resolver; no mutant was run.
# Fixtures keep hyprland.conf source membership and ordering unchanged.

@defect RT1 | accept an existing directory as a direct source target
@old           if [ -f "$x" ]; then continue; fi
@new           if [ -e "$x" ]; then continue; fi

@defect RT2 | bypass regular-file filtering for every expanded glob match
@old               if [ -f "$m" ]; then continue; fi
@new               continue
# RT3 is a distinct mixed-glob false-positive defect; exercise it with N11.
@defect RT3 | invert the glob regular-file guard and misclassify both match kinds
@old               if [ -f "$m" ]; then continue; fi
@new               if [ ! -f "$m" ]; then continue; fi

# N4's exact owning-row assertion requires unresolved: for a missing target.
@defect RT4 | omit the unresolved: label from a missing-target row
@old       [ -n "$tmiss" ] && tdetail="unresolved:$tmiss"
@new       [ -n "$tmiss" ] && tdetail="$tmiss"
