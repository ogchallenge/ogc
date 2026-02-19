# Main Stage Practice Problems and Evaluation Guide

## 1. Additional Practice Problems

[stage2_exercise_problems.zip](instances/train/stage2_exercise_problems.zip)

If you download and unzip the file above, you will get 10 JSON files. Each JSON file is a practice problem set that teams can use while developing algorithms. The 10 problems all have different characteristics.

You can use a total of 25 practice problems: the 10 newly released practice problems, the 10 problems released in the preliminary stage, and the 5 preliminary evaluation problems.

> 💡 When you submit an algorithm, evaluation is performed using **separate hidden problems**, not the public problems listed above. Hidden problems for main-stage evaluation have characteristics similar to public ones, but details (such as problem size) are not disclosed.

## 2. Algorithm Time Limit

Main-stage algorithm time limits vary by problem. **Each evaluation problem provides a time limit (the `timelimit` parameter of `algorithm()`), ranging from a minimum of 1 minute (60 seconds, `timelimit=60`) to a maximum of 4 minutes (240 seconds, `timelimit=240`).** If your algorithm exceeds the time limit, execution is forcibly terminated and that problem receives the minimum score (-1 point). Team scoring method is the same as in the preliminary stage.

> 💡 **Evaluation problem time limits are disclosed after the main stage ends.** Public practice problems also do not have fixed time limits. Teams should test with varied time limits to evaluate and improve performance.

> 💡 Your algorithm must continuously check elapsed time and avoid exceeding the limit. If an internal function takes long and does not check time limits, total runtime may exceed limits. Ensure sufficient time margin at each stage.

> 💡 Be aware of runtime differences between your local environment and evaluation servers. Even in the same server environment, runtime may vary slightly.

## 3. Randomized Algorithms

If your algorithm uses randomness, results may differ per run. Evaluation is performed once immediately after submission. Therefore, resubmitting the same algorithm multiple times may produce different outcomes due to different random values. Organizers do not guarantee specific random seed conditions. In short, evaluation results are not guaranteed to be identical when randomness is used.
