# Preliminary Practice Problems and Evaluation Guide

*Update history:*

- *2024/6/17 - Training instances are available*

## 1. Practice problem set

[stage1_problems.zip](https://github.com/ogchallenge/ogc/releases/download/ogc-2024-assets/2024__instances__train__stage1_problems_v0.0.1.zip)

Download and unzip the file above to obtain 18 JSON files. Each JSON file is a practice instance for algorithm development. The 18 instances have different characteristics (number of orders, fixed costs, etc.). The public instances are derived from real order data and slightly processed for anonymization.

New problem sets will be released for each stage (preliminary, main, final). The characteristics of the next stage instances will be determined based on progress of the competition.

> 💡 When you submit an algorithm, evaluation is performed on **separate hidden instances**, not only on the public ones. The hidden instances have similar characteristics to the public set, but their details (such as number of orders) are not disclosed.

## 2. Time limit

The preliminary time limit is **1 minute (60 seconds) per instance**. If your algorithm exceeds the limit, it will be terminated and the instance receives the lowest score (-1).

> 💡 Your algorithm should continuously monitor elapsed time internally. If a specific function is expensive and you do not check the time inside it, you may exceed the limit. Make sure each step leaves enough time margin.

> 💡 Be mindful of runtime differences between your local environment and the evaluation server. Even on the same server, execution time can vary slightly, so plan accordingly.

## 3. Randomized algorithms

If your algorithm uses randomness, the output can vary across runs. Each submission is evaluated only once, so resubmitting the same algorithm can yield different outcomes. The organizers do not guarantee any fixed random seed. Therefore, if your algorithm uses randomness, the evaluation result is not guaranteed to be identical across runs.
