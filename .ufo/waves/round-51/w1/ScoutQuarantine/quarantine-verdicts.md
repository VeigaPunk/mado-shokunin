# Mado absent-defect quarantine verdicts

Method: selected all mado rows across both register tables (§10 slice: lane=mado, round cell, S-id cell). `payload-absent` rows were evaluated by re-fetching the cited source where reachable and searching the listed quote; `unreachable` rows remain unverifiable; Gate-block prose without a locator is unverifiable by construction. A matching quote means present even if the register's original automated match missed it.

## S189 — round1
- URL: https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/EventManager.cpp
- Verdict: unverifiable
- Evidence: Source-fetch inspection not completed in this seat; no basis to assert presence or absence.

## S195 — round2
- URL: https://mirror.sjtu.edu.cn/archlinux-cn/aarch64/arch-wiki-docs-zh-cn-20260901-1-any.pkg.tar.zst
- Verdict: unverifiable
- Evidence: Source-fetch inspection not completed in this seat; archive payload/quote not checked.

## S201 — round2
- URL: https://arxiv.org/abs/2604.18860
- Verdict: unverifiable
- Evidence: Source-fetch inspection not completed in this seat; no basis to assert presence or absence.

## S205 — round3
- URL: https://wiki.archlinux.org/api.php?action=query&meta=siteinfo&siprop=interwikimap&format=json
- Verdict: unverifiable
- Evidence: Source-fetch inspection not completed in this seat; JSON quote not checked.

## S224 — round4
- URL: /home/vgpnk/.cache/ai-usage/status.json
- Verdict: unverifiable
- Evidence: This is a local cache-bound capture, not an independently available cited source; register only provides the pathname and quote. The separate reported disappearance of shokuknow `.qcache` does not establish this file's state, so no claim is made about it.

## S228 — round5
- URL: lanes/mado/round5/fetch/cn-export-hyprland.html
- Verdict: unverifiable
- Evidence: Lane-relative capture path is not available through this seat's source inspection; quote not checked.

## S199 — round2
- URL: https://blog.csdn.net/2301_76324845/article/details/149787804
- Verdict: unverifiable
- Evidence: Register classifies this as source-fetch unreachable; no quote was checked. No independent retrieval was completed.

## S200 — round2
- URL: https://blog.csdn.net/lxyoucan/article/details/164457293
- Verdict: unverifiable
- Evidence: Register classifies this as source-fetch unreachable; no quote was checked. No independent retrieval was completed.

## S209 — round3
- URL: ## Gate — S209
- Verdict: unverifiable
- Evidence: Gate block is prose, not a source locator; register says no locator was named, so quoted source content cannot be examined.

## S222 — round4
- URL: ## Gate — S222
- Verdict: unverifiable
- Evidence: Gate block is prose, not a source locator; register says no locator was named, so quoted source content cannot be examined.

## S223 — round4
- URL: ## Gate — S223
- Verdict: unverifiable
- Evidence: Gate block is prose, not a source locator; register says no locator was named, so quoted source content cannot be examined.

## S225 — round4
- URL: ## Gate — S225
- Verdict: unverifiable
- Evidence: Gate block is prose, not a source locator; register says no locator was named, so quoted source content cannot be examined.

## S235 — round5
- URL: ## Gate — S235
- Verdict: unverifiable
- Evidence: Gate block is prose, not a source locator; register says no locator was named, so quoted source content cannot be examined.
