# Final Stage Practice Problems and Evaluation Guide

*Update history:*

- *2024/9/12 - Exercise instances are available*

## 1. Additional practice problems

[stage3_problems.zip](instances/train/stage3_problems.zip)

Download and unzip the file above to obtain 3 JSON files. Each JSON file is a practice instance for algorithm development. The 3 instances have different characteristics (number of orders, fixed costs, etc.). The public instances are derived from real order data and processed for anonymization.

You can use these 3 instances together with the 27 practice problems from the preliminary and main stages, for a total of 30 practice problems.

> 💡 When you submit an algorithm, evaluation is performed on **separate hidden instances**, not only on the public ones. The hidden instances have similar characteristics to the public set, but their details (such as number of orders) are not disclosed.

## 2. Time limit

The final stage time limit varies by instance. **Each evaluation instance has its own time limit (the `timelimit` parameter of the `algorithm()` function), ranging from a minimum of 15 seconds to a maximum of 8 minutes (480 seconds).** If your algorithm exceeds the limit, it will be terminated and the instance receives the lowest score (-1). Scoring is the same as the preliminary stage.

> 💡 **Time limits for hidden evaluation instances are not disclosed (they are released after the final stage ends).** Likewise, the public practice instances do not have fixed limits. You should test and improve your algorithm under various time limits.

> 💡 Your algorithm should continuously monitor elapsed time internally. If a specific function is expensive and you do not check the time inside it, you may exceed the limit. Make sure each step leaves enough time margin.

> 💡 Be mindful of runtime differences between your local environment and the evaluation server. Even on the same server, execution time can vary slightly, so plan accordingly.

## 3. Randomized algorithms

If your algorithm uses randomness, the output can vary across runs. Each submission is evaluated only once, so resubmitting the same algorithm can yield different outcomes. The organizers do not guarantee any fixed random seed. Therefore, if your algorithm uses randomness, the evaluation result is not guaranteed to be identical across runs.
