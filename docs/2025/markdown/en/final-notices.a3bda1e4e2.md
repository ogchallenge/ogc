# Final Stage Reference Notes

## 1. Additional Practice Problems

There are no additional practice problems for the final stage. The practice problems used in the main stage and the evaluation problems used in the final stage are similar in characteristics. For reference, final-stage evaluation problems are expected to have no more than about 400 nodes.

## 2. Algorithm Time Limit

Final-stage algorithm time limits vary by problem. **Each evaluation problem has its own time limit (the `timelimit` parameter of `algorithm()`), ranging from a minimum of 0.5 minute (30 seconds, `timelimit=30`) to a maximum of 10 minutes (600 seconds, `timelimit=600`).** If your algorithm exceeds the time limit, execution is forcibly terminated and that problem receives the minimum score (-1 point). Team scoring method is the same as in the preliminary stage.

> 💡 Your algorithm must continuously check elapsed time and avoid exceeding the time limit. If a specific function may run long, not checking within that function can cause a timeout.

> 💡 Also consider runtime differences between your local development environment and the evaluation server. Even in the same server environment, runtime can vary slightly.

## 3. Final Stage Procedure

The final stage proceeds **without additional submissions**, using each team’s **last algorithm submitted in the main stage**. Two problems are added per day for 7 days (14 total). Results are disclosed on the leaderboard by adding one problem at 12:00 and one at 24:00 each day. Rankings are based on cumulative scores for all problems released up to each update point.

## 4. Source Code Submission Guide

All teams participating in the final stage must submit **all source code and a `readme.md` file** together in one archive, following the guide below.

- **Submitted source must be fundamentally identical to the last code submitted in main stage.** “Fundamentally identical” means it should produce the same algorithm outputs when executed. Bug fixes or code improvements are not allowed.
- If precompiled libraries (e.g., Shared Object files) are used, you must submit source code before compilation and include build instructions in `readme.md`.
- If precompiled files are not used but external packages not included in OGC2025 are used, submit source code and package descriptions in `readme.md`. If source cannot be submitted for publicly accessible packages, provide package details and access methods.
- If all submitted files are source code and run directly in OGC2025, briefly state that in `readme.md`.
- `readme.md` may also include any additional notes your team wants to provide.
- **Important:** During the final stage, organizers will review submitted source and verify reproducibility (including compilation). If issues are found, teams may be disqualified. As announced, source code will be publicly disclosed after the competition.
- Compress source and documents with the required name format (**팀명_소스.zip**) and upload by **September 5**:
  - https://optlab.hufs.ac.kr:5001/sharing/ME1pDta0R

## 5. Final Presentation Preparation

All final-stage teams must prepare for the presentation evaluation on September 19.

Presentation format is **5 minutes presentation + 5 minutes Q&A** per team.

You must prepare a 5-minute presentation video in advance (**the pre-submitted video will be played onsite, followed by Q&A**).

Your 5-minute video should freely include the following:

- **Algorithm logic**: overall structure and details
- **Implementation**: language, packages, implementation techniques
- **Strengths**: key merits of your algorithm (logic + implementation), e.g., creativity, adaptability, scalability
- **Future directions**: possible improvements and methods not used due to constraints
- **Participation review**: retrospective, suggestions, future directions for the challenge
- **Video quality**: verify HD resolution and clear audio
- Upload your video (**팀명_발표동영상.mp4**) and slides (**팀명_발표자료.pdf**) by **September 17**:
  - https://optlab.hufs.ac.kr:5001/sharing/ME1pDta0R
