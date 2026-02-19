# Main Round Practice Problems and Evaluation Guide (1)

*Update history:*

- *2024/8/11 - Exercise instances are available*

## 1. Additional Practice Problems

[stage2_problems.zip](instances/train/stage2_problems.zip)

Download and extract the above file to get a total of 6 JSON files. Each JSON file is a practice problem that participating teams can use when developing algorithms. The 6 problems all have different characteristics (number of orders, fixed cost, etc.). Public problems have been processed for anonymization based on actual order data.

Use the 6 practice problems released this time, the 18 problems released in the preliminary stage, and the three problems used in preliminary evaluation, for a total of 27 practice problems.

> 💡 When you submit an algorithm, evaluation is performed using **separate hidden problems** other than the above public problems. Main round hidden evaluation problems have similar characteristics to public problems, and characteristics of evaluation problems (number of orders, etc.) are not disclosed

## 2. Algorithm Time Limit

Main round algorithm execution time limits are given differently for each problem. **Each evaluation problem is given a time limit (the `timelimit` parameter of the `algorithm()` function) with a range from minimum 1 minute (60 seconds, `timelimit=60`) to maximum 5 minutes (300 seconds, `timelimit=300`).** If the algorithm exceeds the execution time limit, problem solving is forcibly terminated and the lowest score (-1 point) is received for that problem. The scoring method for each team is the same as in the preliminary round.

> 💡 In the preliminary round, all problems had the same 1-minute execution time limit, but **in the main round, it's given differently for each problem.**

> 💡 **Execution time limits for evaluation problems are not disclosed.** Likewise, released practice problems do not have fixed execution time limits. That is, you must evaluate and improve algorithm performance by setting various execution time limits for released practice problems

> 💡 Execution time must be continuously checked within the algorithm to not exceed the time limit. For example, if a specific function used within the algorithm may take a long time and does not check the time limit within that function, the algorithm's execution time may exceed the time limit. Participating teams should pay attention to this and verify that there is sufficient margin time at each execution stage of the algorithm so that the algorithm does not exceed the time limit

> 💡 Also note the execution time difference that may occur due to differences between the environment where participating teams develop algorithms and the evaluation server environment. In particular, even when running the same algorithm in the same server environment, slight differences in algorithm execution time may occur, which should be considered

## 3. Randomized Algorithms

When using randomness in an algorithm, results may differ each time the algorithm executes. Algorithm evaluation is performed only once immediately after algorithm submission. Therefore, if the same algorithm is resubmitted multiple times, different random numbers may be obtained with each submission, possibly yielding different results. The organizer does not guarantee that submitted algorithms have specific random number conditions (random seed). That is, algorithm evaluation results are not guaranteed to always be the same when algorithms use random numbers.
