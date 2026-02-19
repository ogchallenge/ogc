# Preliminary Practice Problems and Evaluation Guide

*Update history:*

- *2024/6/17 - Training instances are available*

## 1. Algorithm Practice Problems

[stage1_problems.zip](https://github.com/ogchallenge/ogc/releases/download/ogc-2024-assets/2024__instances__train__stage1_problems_v1.0.0.zip)

Download and extract the above file to get a total of 18 JSON files. Each JSON file is a problem for participating teams to use to develop algorithms. The 18 problems all have different characteristics (number of orders, fixed cost, etc.). Public problems have been slightly processed for anonymization based on actual order data.

New problems will be released for each stage of preliminary, main, and final. The characteristics of the next stage problems will be determined by reviewing the competition's progress.

> 💡 When you submit an algorithm, evaluation is performed using **separate hidden problems** other than the above public problems. Hidden evaluation problems have similar characteristics to public problems ⇒ Characteristics of evaluation problems (number of orders, etc.) are not disclosed but do not differ greatly from practice problems

## 2. Algorithm Time Limit

The preliminary algorithm execution time limit is **1 minute (60 seconds)** per problem. If the algorithm exceeds the time limit, problem solving is forcibly terminated and the lowest score (-1 point) is received for that problem.

> 💡 Execution time must be continuously checked within the algorithm to not exceed the time limit. For example, if a specific function used within the algorithm may take a long time and does not check the time limit within that function, the algorithm's execution time may exceed the time limit. Participating teams should pay attention to this and verify that there is sufficient margin time at each execution stage of the algorithm so that the algorithm does not exceed the time limit

> 💡 Also note the execution time difference that may occur due to differences between the environment where participating teams develop algorithms and the evaluation server environment. In particular, even when running the same algorithm in the same server environment, slight differences in algorithm execution time may occur, which should be considered

## 3. Randomized Algorithms

When using randomness in an algorithm, results may differ each time the algorithm executes. Algorithm evaluation is performed only once immediately after algorithm submission. Therefore, if the same algorithm is resubmitted multiple times, different random numbers may be obtained with each submission, possibly yielding different results. The organizer does not guarantee that submitted algorithms have specific random number conditions (random seed). That is, algorithm evaluation results are not guaranteed to always be the same when algorithms use random numbers.
