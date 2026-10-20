# WITHHELD bodies

`s061-archwiki-oldid-{1,2,3}.txt` were moved out of this directory on 2026-10-20 after
MadoR19.SentinelVcsFixtures flagged that these three HTTP-200 bodies are Anubis anti-bot
challenge HTML embedding the operator's public IPv6 in the `X-Real-Ip` field of the
challenge JSON. They are retained only outside the lane (mode 0600, `/tmp`), and the
receipts in `receipts.jsonl` (lines 13, 14, 19) remain the digest-only record of the fetches.

They are not evidence of `oldid=` content instability: the three digests differ because the
challenge nonce/timestamp differ per request, which is the same failure mode the report
documents for GitHub tree pages. Do not copy these bodies into any committed artifact.
