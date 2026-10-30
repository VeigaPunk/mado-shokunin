# R56W3MutBwrapChannels receipts matrix (harness: FROZEN quality/check-r56-controls.py at tip bytes; only tools/mado-watchplan.py swapped per cheat)

| cheat | bwrap (host default) | no bwrap, harness default | no bwrap + --no-sandbox |
|---|---|---|---|
| baseline | fixtures=18/18 holdout=8/8 TARGET_MET sandbox=bwrap | SETUP-REFUSAL rc=2: bwrap is not installed: the staged layout alone does not hide the answ | fixtures=18/18 holdout=8/8 TARGET_MET sandbox=none |
| c1a-sibling-direct | fixtures=0/18 holdout=0/8 TARGET_MISSED sandbox=bwrap | SETUP-REFUSAL rc=2: bwrap is not installed: the staged layout alone does not hide the answ | fixtures=0/18 holdout=0/8 TARGET_MISSED sandbox=none |
| c1-sibling | fixtures=0/18 holdout=0/8 TARGET_MISSED sandbox=bwrap | SETUP-REFUSAL rc=2: bwrap is not installed: the staged layout alone does not hide the answ | fixtures=18/18 holdout=8/8 TARGET_MET sandbox=none |
| c2a-filename | fixtures=15/18 holdout=0/8 TARGET_MISSED sandbox=bwrap | SETUP-REFUSAL rc=2: bwrap is not installed: the staged layout alone does not hide the answ | fixtures=15/18 holdout=0/8 TARGET_MISSED sandbox=none |
| c2b-filename-all | fixtures=15/18 holdout=6/8 TARGET_MISSED sandbox=bwrap | SETUP-REFUSAL rc=2: bwrap is not installed: the staged layout alone does not hide the answ | fixtures=15/18 holdout=6/8 TARGET_MISSED sandbox=none |
| c2c-content-all | fixtures=18/18 holdout=8/8 TARGET_MET sandbox=bwrap | SETUP-REFUSAL rc=2: bwrap is not installed: the staged layout alone does not hide the answ | fixtures=18/18 holdout=8/8 TARGET_MET sandbox=none |
| c2d-fid-lookup-all | fixtures=18/18 holdout=8/8 TARGET_MET sandbox=bwrap | SETUP-REFUSAL rc=2: bwrap is not installed: the staged layout alone does not hide the answ | fixtures=18/18 holdout=8/8 TARGET_MET sandbox=none |
| c3-env | fixtures=0/18 holdout=0/8 TARGET_MISSED sandbox=bwrap | SETUP-REFUSAL rc=2: bwrap is not installed: the staged layout alone does not hide the answ | fixtures=18/18 holdout=8/8 TARGET_MET sandbox=none |
| c4-cwd | fixtures=0/18 holdout=0/8 TARGET_MISSED sandbox=bwrap | SETUP-REFUSAL rc=2: bwrap is not installed: the staged layout alone does not hide the answ | fixtures=18/18 holdout=8/8 TARGET_MET sandbox=none |
| c5-lane-abs | fixtures=0/18 holdout=0/8 TARGET_MISSED sandbox=bwrap | SETUP-REFUSAL rc=2: bwrap is not installed: the staged layout alone does not hide the answ | fixtures=18/18 holdout=8/8 TARGET_MET sandbox=none |
| c6-proc-crawl | fixtures=0/18 holdout=0/8 TARGET_MISSED sandbox=bwrap | SETUP-REFUSAL rc=2: bwrap is not installed: the staged layout alone does not hide the answ | fixtures=18/18 holdout=8/8 TARGET_MET sandbox=none |
| c7-git-objects | fixtures=0/18 holdout=0/8 TARGET_MISSED sandbox=bwrap | SETUP-REFUSAL rc=2: bwrap is not installed: the staged layout alone does not hide the answ | fixtures=18/18 holdout=8/8 TARGET_MET sandbox=none |

## bwrap stub experiments (stub replaces /usr/bin/bwrap in a private mount namespace; c1-sibling cheat installed)

| stub | result |
|---|---|
| bwrap-passthru | fixtures=18/18 holdout=8/8 TARGET_MET sandbox=bwrap |
| bwrap-fail | fixtures=0/18 holdout=0/8 TARGET_MISSED sandbox=bwrap |

## identity test (honest tool, same rev): stdout claim line

- bwrap: fixtures=18/18 holdout=8/8 TARGET_MET sandbox=bwrap
- nosb: SETUP-REFUSAL rc=2: bwrap is not installed: the staged layout alone does not hide the answ
- nosb-ns: fixtures=18/18 holdout=8/8 TARGET_MET sandbox=none

## lane tip 0f3a54361a9824484d0801679ceb1fd8ac7c32e1 (read-only harness run, --work scratch)

- bwrap: fixtures=18/18 holdout=8/8 TARGET_MET sandbox=bwrap
- no bwrap (mount-masked): SETUP-REFUSAL rc=2: bwrap is not installed: the staged layout alone does not hide the answ
