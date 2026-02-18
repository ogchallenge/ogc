# Main Stage Practice Problems and Evaluation Guide (1)

*Update history:*

- *2024/8/11 - Exercise instances are available*

## 1. Additional practice problems

[stage2_problems.zip](https://github.com/ogchallenge/ogc/releases/download/ogc-2024-assets/2024__instances__train__stage2_problems_v1.0.0.zip)

Download and unzip the file above to obtain 6 JSON files. Each JSON file is a practice instance for algorithm development. The 6 instances have different characteristics (number of orders, fixed costs, etc.). The public instances are derived from real order data and processed for anonymization.

You can use these 6 instances together with the 18 preliminary practice instances and the 3 preliminary evaluation instances, for a total of 27 practice problems.

> 💡 When you submit an algorithm, evaluation is performed on **separate hidden instances**, not only on the public ones. The hidden instances have similar characteristics to the public set, but their details (such as number of orders) are not disclosed.

## 2. Time limit

The main stage time limit varies by instance. **Each evaluation instance has its own time limit (the `timelimit` parameter of the `algorithm()` function), ranging from a minimum of 1 minute (60 seconds) to a maximum of 5 minutes (300 seconds).** If your algorithm exceeds the limit, it will be terminated and the instance receives the lowest score (-1). Scoring is the same as the preliminary stage.

> 💡 The preliminary stage used a fixed 1 minute limit for all instances, but **the main stage uses a different limit per instance.**

> 💡 **Time limits for hidden evaluation instances are not disclosed.** Likewise, the public practice instances do not have fixed limits. You should test and improve your algorithm under various time limits.

> 💡 Your algorithm should continuously monitor elapsed time internally. If a specific function is expensive and you do not check the time inside it, you may exceed the limit. Make sure each step leaves enough time margin.

> 💡 Be mindful of runtime differences between your local environment and the evaluation server. Even on the same server, execution time can vary slightly, so plan accordingly.

## 3. Randomized algorithms

If your algorithm uses randomness, the output can vary across runs. Each submission is evaluated only once, so resubmitting the same algorithm can yield different outcomes. The organizers do not guarantee any fixed random seed. Therefore, if your algorithm uses randomness, the evaluation result is not guaranteed to be identical across runs.
