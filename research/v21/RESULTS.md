# Executed result v21

Corrected code b8d245541f9d031b0934e29218ab4963097b2337; official evidence f4a79052d0cf92c3a36693533c67bb2053506284; workflow42437618512.75 measurements, no failures/mismatches, fixed inputs/threads, three subprocess repetitions. The invalid first run906c627 is preserved and excluded.

AtN8,H10: CDKA5.632ms vs Storm sparse451.194ms, sparse+strong-bisim468.054ms, symbolic6493.131ms; informed subset-renewal13.006ms. Ratio to fastest measured Storm80.11 internally,4.87 for whole process. AtN4,H20 informed subset-renewal4.222ms beats histogram11.923ms. All setup timings and RSS are retained in evidence/official/results.json.

The method handles rank-one restarts that preserve achieved goals. It fails the v20 goal-relative commutation test but has an exact work-run histogram response. Complexity O(H sum d_i²+H²+N p(H+1)) arithmetic, with explicit bit/numeric and partition-growth limits. This is a source-recognized synthetic extension of Meeting, not a general SOTA assertion.

[Proof](docs/T4V-regenerative-exposure-histograms.md) · [Impact plan](docs/impact-plan.md) · [Research memory](registry/v21-decision.json) · [Raw official summary](evidence/official/summary.json).

The larger local package also contains the interactive dashboard, complete small traces, separate local benchmark samples, hash-verified copy of the official summary and Chromium QA. Main and Pages are unchanged; this remains a research branch.
