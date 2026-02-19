# Algorithm Development Guide and Baseline Algorithm Description

*Update history:*

- *2025/07/19 - baseline_20250719 updated (bugs in heuristics fixed)*
- *2025/07/05 - baseline_20250705 updated (bugs in util.py fixed)*
- *2025/06/01 - baseline_20250601 updated (bugs in heuristics fixed)*
- *2025/05/31 - baseline_20250531 updated (minor bugs fixed)*
- *2025/05/19 - baseline_20250519 updated (minor bugs fixed)*
- *2025/05/07 - initial page created*

This page explains how to write algorithm code for the competition using the provided baseline algorithm as an example.

## 1. Environment Setup

Before submission, each team should implement and test the algorithm on their own PC. This section explains how to build a Python environment similar to the evaluation server.

Available Python packages on the evaluation server are:

```
- python 3.11
- jupyterlab 4.4.1
- notebook 7.4.1
- ipympl 0.9.7
- matplotlib 3.8.4
- pandas 2.2.3
- networkx 3.4.2
- scipy 1.15.2
- scikit-learn 1.6.1
- numba 0.61.0
- cython 3.0.10
- jsbeautifier
- ortools 9.11.4210
- gurobipy 12.0.1
- xpress 9.5.4
- gymnasium 1.1.1
- torch 2.6.0
- torchvision 0.21.0
- tensorflow 2.18.0
- keras 3.9.0
```

> 💡 If you need additional packages for development, request them in Slack.

### Create a Conda Environment

Conda is a tool for managing virtual environments. You can install it via Anaconda or miniforge. **For this competition, miniforge is recommended.**

> 💡 If you are new to Conda, see [this guide](https://wikidocs.net/135082).

Conda setup steps:

[ogc2025_env_20250506.yml.zip](baselines/ogc2025_env_20250506.yml.zip)

1. Download the file above and save it to any folder.
2. Move to that folder.
3. Run the following in Terminal/cmd (*replace `ogc2025_env_2025XXXX.yml` with the actual filename*):

   `conda env create -f ogc2025_env_2025XXXX.yml`

4. After package installation finishes, run:

   `conda activate ogc2025`

5. If your prompt looks like below, setup is complete:

![MacOS Terminal example](conda_terminal.png)

> 💡 Depending on hardware/OS, environment creation may fail (especially with `pytorch`, `tensorflow`, etc.). If you do not use a problematic package, remove it from the provided YAML and retry. If issues continue, contact Slack.

> 💡 This conda environment is provided to increase compatibility with the evaluation server. It is not mandatory, and exact behavior may still differ by OS. General Conda/Python issues should be handled by teams. Please keep Slack questions focused on competition-related topics.

### Additional Installed Python Packages

The following packages were additionally installed on the evaluation server upon team requests after competition launch. Teams may use them.

```python
torch_cluster                1.6.3+pt26cu124
torch-geometric              2.6.1
torch_scatter                2.1.2+pt26cu124
torch_sparse                 0.6.18+pt26cu124
torch_spline_conv            1.2.2+pt26cu124
cdlib                        0.4.0
leidenalg                    0.10.2
stable_baselines3            2.6.0
```

## 2. How to Submit an Algorithm

[baseline_20250719.zip](baselines/baseline_20250719.zip)

[exercise_problems_20250512.zip](baselines/exercise_problems_20250512.zip)

Download both files above and unzip them in an appropriate folder.

- `baseline_2025XXXX.zip`: sample algorithm code
- `exercise_problems_2025XXXX.zip`: sample practice problems

> 💡 `baseline_2025XXXX.zip` and `exercise_problems_2025XXXX.zip` may be updated to fix bugs. Check for the latest version regularly.

> 💡 `exercise_problems_2025XXXX.zip` contains **practice** problems, not stage **evaluation** problems. Evaluation problems for each stage are disclosed only after that stage ends.

After downloading, copy both zip files to a folder.

![Baseline Files](baseline_files.png)

Then unzip as follows.

![Unzipped Baseline Files](baseline_files_decompressed.png)

The `baseline` folder contains:

- `myalgorithm.py`: **the main file where you implement your algorithm**
- `util.py`: helper functions for development

Now check `myalgorithm.py` first.

```python
import time
import util
import networkx as nx
from itertools import islice
import numpy as np

def algorithm(prob_info, timelimit=60):
    """
    This is a template for the custom algorithm.
    The algorithm should return a solution that is a list of (route, k) pairs.
    Each route is a list of node indices, and k is the index of the demand that is moved by the route.
    You CANNOT change or remove this function signature.
    But it is fine to define extra functions or mudules that are used in this function.
    """

    #------------- begin of custom algorithm code --------------#
    ...
    ...
    ...
    #------------- end of custom algorithm code --------------#

    return solution
```

`algorithm()` is called with:

- `prob_info`: problem data
- `timelimit`: execution time limit (seconds). Your algorithm must finish within this limit.

Meaning of key markers:

`#------------- begin of custom algorithm code --------------#`
- Start of your implementation.

`#------------- end of custom algorithm code --------------#`
- End of your implementation.

Write your algorithm code between these two lines using the provided `prob_info` and `timelimit`.

> 💡 The baseline is a simple educational example. Replace this part with your own algorithm before submission.

> 💡 You may modify/reuse baseline code, but submitting it as-is is not recommended. Since submission count is limited, avoid meaningless submissions.

> 💡 The filename `myalgorithm.py` and function signature `def algorithm(prob_info, timelimit=60):` must **never** be changed.

> The baseline `myalgorithm.py` includes simple test code for your algorithm. See the section starting with `if __name__ == "__main__":`.

You can read problem data from `prob_info` as follows:

```python
# Get parameters from the prob_info dictionary
N = prob_info['N']
E = prob_info['E']
K = prob_info['K']
P = prob_info['P']
F = prob_info['F']
```

- `N`: number of nodes. `0` is gate; `1 ~ N-1` are placeable nodes.
- `E`: edge list (undirected).
- `K`: demand list, `[ [[o,d)],quantity], ... ]`.
- `P`: number of ports, visited in order `0 ~ P-1`.
- `F`: route fixed cost.

The returned solution must have this structure:

- Dict format: `port_index: [(route, demand_index), ...]`
  - `port_index`: integer in `0 ~ P-1`
  - `route`: list of nodes like `[0,3,2]`
  - `demand_index`: index in `K`, i.e., `0 ~ len(K)-1`

Example:

```python
solution = {
  0: [
    [[0, 1, 3, 5, 6, 9, 15, 20, 22], 2],
    [[0, 1, 2, 4, 7, 10, 14, 19, 21], 2],
    [[0, 1, 3, 5, 6, 9, 15, 20], 1],
    [[0, 1, 2, 4, 7, 10, 14, 19], 1],
    [[0, 1, 3, 5, 6, 9, 16], 1],
    [[0, 1, 3, 5, 6, 11, 17], 1],
    [[0, 1, 2, 4, 7, 12, 18], 1],
    [[0, 1, 3, 5, 6, 9, 15], 0],
    [[0, 1, 2, 4, 7, 10, 14], 0],
    [[0, 1, 3, 5, 8, 13], 0],
    [[0, 1, 3, 5, 6, 9], 0]
  ],
  1: [
    [[9, 6, 5, 3, 1, 0], 0],
    [[13, 8, 5, 3, 1, 0], 0],
    [[14, 10, 7, 4, 3, 1, 0], 0],
    [[15, 10, 7, 4, 3, 1, 0], 0],
    ...
  ]
}
```

Objective and feasibility are checked separately. See the problem description page for details.

> Use `check_feasibility(prob_info, solution)` in `util.py` to validate your solution and compute objective.

`check_feasibility(prob_info, solution)` returns:

```python
{
  'obj': 588.0,
  'feasible': True,
  'infeasibility': None,
  'solution': ...
}
```

Key fields:

- `obj`: objective value (sum of route costs - LB)
- `feasible`: whether solution is feasible (`True`/`False`)
- `infeasibility`: reason when infeasible (`None` if feasible)

> 💡 Time limit only counts pure `algorithm()` wall-clock runtime. Problem loading and validation (`check_solution()` etc.) are excluded. If limit is exceeded, penalty is applied regardless of solution quality.

The baseline is intentionally simple and includes two core functions:

- `loading_heuristic(p, node_allocations, rehandling_demands)`: loading heuristic at port `p` (`rehandling_demands` are demands reloaded after temporary unloading)
- `unloading_heuristic(p, node_allocations)`: unloading heuristic at port `p`

Baseline core loop:

```python
# Loop over all ports and apply the loading and unloading heuristics to generate the routes
for p in range(P):

    print(f"Port {p} ==============================")

    if p > 0:
        # Unloading heuristic
        route_list_unload, rehandling_demands = unloading_heuristic(p, node_allocations)

        solution[p].extend(route_list_unload)
    else:
        rehandling_demands = []

    if p < P-1:
        # Loading heuristic
        route_list_load, node_allocations = loading_heuristic(p, node_allocations, rehandling_demands)

        solution[p].extend(route_list_load)

    print()
```

As shown, the algorithm iterates ports in route order and repeats unload → load heuristics. See baseline source for details.

> Baseline is provided to help understanding and reduce development time. You may reuse parts of it in your own algorithm.

### Submission Packaging Rules

Submit your algorithm as a single zip file with all required files.

Requirements:

- One `zip` file (filename is arbitrary)
- Required files: `myalgorithm.py`, `util.py`
- `myalgorithm.py` must be at the root when unzipped (not inside a subfolder)

> 💡 **`myalgorithm.py` must not be inside any folder in the submission zip.**
>
> **Renaming (e.g., `myalgorithm_best.py`) is not allowed.**
>
> ![Correct submission zip (Windows)](zip_file_contents_win.png)
>
> ![Incorrect submission zip (Windows)](zip_file_contents_win_err.png)
>
> On MacOS/Linux, inspect zip contents with:
>
> `unzip -vl your_submission.zip`
>
> If `myalgorithm.py` appears under a folder (e.g., `test1/myalgorithm.py`), it is invalid.

Other rules:

- Additional required files (e.g., neural-network checkpoints) may be included; extra folders are allowed.
- `util.py` is not editable for evaluation purposes (even if modified and submitted, it is replaced with the official one during evaluation).
- Additional Python modules/files are allowed, but must be included in the zip.
- Zip size must be **30MB or less** (request increase via Slack if necessary).

In short, after unzipping, `algorithm()` in `myalgorithm.py` must run in the `ogc2025` environment.

> Hidden evaluation problems are used on the server, so you do not need to submit problem files.

### Using Languages Other Than Python

Using non-Python languages/libraries is allowed. Include all required binaries/libraries in the zip, and call them from `myalgorithm.py`.

To maintain fairness and avoid changing global execution environment, installation of system-wide languages/libraries is decided very carefully. Teams are responsible for localizing everything into their submission so it does not affect other teams.

> 💡 For non-Python implementations, ensure compatibility with the server environment. Example: if using C/C++, compile on Linux/Ubuntu 24.04 first, then submit the generated `.so` or executable in the zip. Server-side compilation is not performed.

> 💡 Strongly recommended: reproduce the evaluation environment (e.g., VM) and test there.

> 💡 Even for interpreted languages with no compile step (e.g., Julia), request and confirm availability via Slack first.

> 💡 Although server-side compilation is not performed, include source code for your own libraries in the zip.

- Java
  - `sudo apt-get update`
  - `sudo apt-get install openjdk-17-jdk`
  - `java --version`

  ![Check Java version](java_version.png)

- Dotnet framework (C#)
  - `sudo apt install -y dotnet-runtime-8.0`
  - `dotnet --info`

  ![Check Dotnet version](dotnet_version.png)

### Error Codes on Submission

After submission and leaderboard update, teams can view execution status of submitted algorithms by date. If execution succeeds within time limits, objective values are shown. If errors occur, reasons are displayed.

`alg_error` indicates a Python exception occurred during algorithm execution.

![Check algorithm error codes](error_code1.png)

![Algorithm error code details](error_code2.png)

- `infeasible`: returned solution is infeasible
- `time_limit`: runtime exceeded allowed limit
- `crash`: abnormal termination (e.g., segmentation fault)
- `algo_error`: internal algorithm error
- `test_error`: evaluator could not run submission
  - `test_error(01)`: unzip failed on evaluation server (invalid zip format)
  - `test_error(02)`: `myalgorithm.py` not found at zip root
  - `test_error(03)`: attempted to `import` package not available in `ogc2025`

`sys_error` indicates an error on the evaluation system side.

Detailed error codes may be expanded during the competition.

## 3. How to Use `alg_tester`

This section introduces a simple way to test your algorithm and verify submission format before submission.

[alg_tester_20250513.zip](baselines/alg_tester_20250513.zip)

Download and unzip this file in an appropriate folder. Open `alg_tester.ipynb` from the unzipped folder.

![Algorithm Tester Files](alg_tester_files.png)

You will see a notebook like below. Run the first cell (`ctrl+enter`).

![Algorithm Tester Notebook](alg_tester_notebook.png)

`alg_tester` provides:

- Reads submission zip and checks zip format and existence of `algorithm()`
- Runs submitted algorithm on multiple problem files to verify successful return
- Computes objective and visualizes solution when feasible
- Supports comparing results across multiple algorithm/problem combinations

> Even if your algorithm runs in `alg_tester`, server-side errors may still occur due to environment differences. Refer to the problem description page for evaluation server details.