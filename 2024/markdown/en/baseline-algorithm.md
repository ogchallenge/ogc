# Algorithm Development Environment and Baseline Algorithm Guide

*Update history:*

- *2024/09/10 - `ogc2024_env.yml` updated - `scikit-learn-extra` package available*
- *2024/07/20 - `baseline_20240720.zip` updated*
- *2024/07/12 - Java (openjdk 17.0.11) available*
- *2024/07/01 - `baseline_20240701.zip` updated*
- *2024/06/29 - added clarification on required zip structure for submission*
- *2024/06/24 - added explanation of algorithm error codes*
- *2024/06/21 - `baseline_20240621.zip` updated*
- *2024/06/16 - `baseline_20240616.zip` updated*
- *2024/06/03 - Microsoft.NETCore.App 7.0.19 available*
- *2024/05/17 - added information on commercial solver licenses*
- *2024/05/17 - `baseline_20240517.zip` updated*

This page explains how to build your algorithm using the provided baseline implementation as an example.

## 1. Environment setup

Before submitting, each team should implement and test the algorithm on a local machine. This section explains how to create a Python environment that matches the evaluation server.

Available Python packages on the evaluation server:

```
- python 3.10
- jupyterlab 4.0.11
- matplotlib 3.8.4
- pandas 2.2.1
- networkx 3.1
- scipy 1.12.0
- tensorflow 2.10.0
- keras 2.10.0
- pytorch 2.2.0
- scikit-learn 1.3.0
- scikit-learn-extra 0.3.0
- numba 0.59.1
- cython 3.0.10
- ortools 9.9.3963
- gurobipy 11.0.1
- xpress 9.3
```

> 💡 If you need additional packages, request them via the Slack channel.

### Creating a conda environment

Conda is a virtual environment manager. Install it via [Anaconda](https://www.anaconda.com/download) or [miniforge](https://github.com/conda-forge/miniforge).

> 💡 For a primer on conda and why it is useful, see [this page](https://wikidocs.net/135082).

Conda environment setup steps:

[ogc2024_env.yml](baselines/ogc2024_env.yml)

1. Download the file above and save it in a folder of your choice.
2. Navigate to that folder.
3. Run the following in Terminal or cmd:
    
    `conda env create -f ogc2024_env.yml`
    
4. After installation finishes, run:
    
    `conda activate ogc2024`
    
5. If your terminal shows the activated environment, the setup is complete.

![Windows Anaconda Prompt](anaconda-prompt.png)

Windows Anaconda Prompt

## 2. How to submit an algorithm

    [baseline_20240720.zip](baselines/baseline_20240720.zip)

    [alg_test_problems_20240429.zip](baselines/alg_test_problems_20240429.zip)

Download and unzip the two files above. `baseline_2024XXXX.zip` contains example algorithm code. `alg_test_problems_2024XXXX.zip` contains sample problem instances used to run the baseline.

> 💡 `baseline_2024XXXX.zip` and `alg_test_problems_2024XXXX.zip` may be updated periodically (e.g., for bug fixes). Check for the latest version regularly.

> 💡 `alg_test_problems_2024XXXX.zip` are not the official contest instances. Preliminary/main/final problems will be released at the start of each stage.

Unzip both archives as shown below.

![Baseline folder structure](baseline-folder-structure.png)

The `baseline` folder contains:

- `myalgorithm.py`: **the main algorithm implementation file**
- `util.py`: helper functions for algorithm development
- `alg_test.ipynb`: Jupyter notebook for quick testing

Open `myalgorithm.py` first.

```python
from util import *

def algorithm(K, all_orders, all_riders, dist_mat, timelimit=60):

    start_time = time.time()

    for r in all_riders:
        r.T = np.round(dist_mat/r.speed + r.service_time)

    # A solution is a list of bundles
    solution = []

    #------------- Custom algorithm code starts from here --------------#
		...
    #------------- End of custom algorithm code --------------#

    return solution
```

The `algorithm()` function is called with the following parameters:

- `K`: number of orders
- `all_orders`: list of orders
- `all_riders`: list of riders
- `dist_mat`: distance matrix
- `timelimit`: time limit (seconds). The algorithm must finish within this time.

Write your algorithm between the two markers:

- `#------------- Custom algorithm code starts from here --------------#`
- `#------------- End of custom algorithm code --------------#`

Use `K`, `all_orders`, `all_riders`, `dist_mat`, and `timelimit` to compute a valid solution.

> 💡 The baseline code includes only a simple example. Replace it with your own algorithm for submission.

> 💡 You may reuse or modify the baseline code, but do not submit it as-is. You can submit only once per day, so avoid meaningless submissions.

> 💡 The file name `myalgorithm.py` and the function signature `def algorithm(K, all_orders, all_riders, dist_mat, timelimit=60):` **must not be changed**.

The solution must have the following structure:

- Return a list of `[rider_type, pickup_order_sequence, delivery_order_sequence]`
    - Example order sequence: `[1, 3, 2]` (order IDs)
    - Example: `['BIKE', [1,3,2], [2,3,1]]`
        - Meaning: Assign orders 1, 2, 3 to a bike rider, visit pickup locations in 1,3,2 order, then delivery locations in 2,3,1 order.

Validity and objective evaluation are performed by the scoring system. See the problem description page for full details.

### Submission format

Submit your algorithm as a single zip file that satisfies the following:

- One `zip` file (file name can be arbitrary)
- Required files: `myalgorithm.py`, `util.py`
- `myalgorithm.py` must be in the **root** of the archive (not inside a subfolder)

> 💡 **`myalgorithm.py` must NOT be inside a subfolder of the zip file.**
>
> **Renaming it to `myalgorithm_best.py` or similar is NOT allowed.**
>
> ![Correct submission archive structure**](submission-correct-structure.png)
>
>
> ![Incorrect submission archive](submission-incorrect-structure.png)
>
>
> On macOS or Linux, you can inspect the archive with:
>
> ![Check archive structure](submission-terminal-check.png)
>
> If `unzip -vl your.zip` shows `myalgorithm.py` under a folder (e.g., `test1`), it is invalid.

- You may include additional files (e.g., checkpoints) in the archive. Additional subfolders are allowed for extra files.
- `alg_test.ipynb` is optional and does not need to be included.
- `util.py` must not be modified (any changes will be replaced during evaluation).
- Additional Python modules are allowed, but must be included in the archive.
- The archive size must be <= 30MB (request a larger limit via Slack if needed).

In summary, after unzipping, the `algorithm()` function in `myalgorithm.py` must be executable in the `ogc2024` environment.

> 💡 The easiest way to verify compatibility is to run your algorithm in the provided Jupyter notebook, then zip the working files.

> 💡 You do not need to include any problem instance files in the submission; hidden instances are used for evaluation.

### Using non-Python languages

You may use languages or libraries other than Python by packaging all required files and invoking them from `myalgorithm.py`.

MIP solvers such as Gurobi, Xpress, and OR-Tools are only available in the Python environment. We recommend using other languages only as subroutines for speed, not for the full optimization model (model execution speed does not depend on the language).

To preserve fairness and stability, installing system-wide languages or libraries is done cautiously. Teams must package everything needed in their archive so that their submission does not impact others.

> 💡 For non-Python languages, be mindful of the evaluation environment. For example, if you implement in C/C++, compile on Ubuntu 22.04 and submit the resulting `so` or executable. The evaluation server will not compile for you.

> 💡 Consider setting up a VM that mirrors the evaluation server to verify compatibility.

> 💡 For languages without compilation steps (e.g., Julia), request approval via Slack before use.

> 💡 Include source code for any libraries you build, because compilation is not performed on the evaluation server.

### Java and .NET (updated 2024-07-12)

Java and .NET were installed per team requests. Usage notes:

- Java
    - `sudo apt-get update`
    - `sudo apt-get install openjdk-17-jdk`
    - `java --version`
        
        ![Java version check](java-version-check.png)
        
- .NET (C#)
    - `sudo apt install -y dotnet-runtime-7.0`
    - `dotnet --info`
        
        ![Dotnet info check](dotnet-info-check.png)

### Algorithm submission error codes

After submission and evaluation, you can view the execution status for each submission date.

![Submission results table](submission-results-table.png)

If the algorithm completes successfully within the time limit, the objective value (average delivery cost) is shown. If execution fails, you will see an error code. `alg_error` indicates a Python exception occurred during execution.

`sys_error` can include specific codes:

- `sys_error(03)`: the submitted archive failed to unzip (invalid format)
- `sys_error(05)`: `myalgorithm.py` not found at the root of the archive

`test_error` indicates the algorithm could not run:

- `test_error(01)`: the submission imports a Python package not available in the `ogc2024` environment

Additional codes may be introduced later.

## 3. Running the baseline algorithm

Use `alg_test.ipynb` to run your algorithm locally.

> 💡 The instructions below assume you can run Jupyter notebooks. You can use JupyterLab or Visual Studio Code.

Open `alg_test.ipynb` in VS Code or JupyterLab.

![VSCode screen](vscode-screen.png)

VS Code screen

![JupyterLab screen](jupyterlab-screen.png)

JupyterLab screen

> 💡 After opening the notebook, ensure the kernel is set to the `ogc2024` environment. In JupyterLab, activate the environment first and then run `jupyter-lab`.

When you run the notebook cells, the algorithm in `myalgorithm.py` (in the same folder) will execute. Below is a brief explanation of the code:

```python
problem_file = '../alg_test_problems_20240429/TEST_K100_1.json'
timelimit = 10
```

The `'../alg_test_problems_20240429/TEST_K100_1.json'` part specifies the problem file path. In this example, it points to the test instances you extracted earlier. As new problems are released in each stage, save them and update the file path accordingly.

```python
with open(problem_file, 'r') as f:
    prob = json.load(f)

K = prob['K']

ALL_ORDERS = [Order(order_info) for order_info in prob['ORDERS']]
ALL_RIDERS = [Rider(rider_info) for rider_info in prob['RIDERS']]

DIST = np.array(prob['DIST'])
for r in ALL_RIDERS:
    r.T = np.round(DIST/r.speed + r.service_time)

alg_start_time = time.time()

exception = None

solution = None
```

This prepares the problem data. `Rider` and `Order` classes are defined in `util.py`.

> 💡 Functions or classes in `util.py` must not be modified. If you need changes, create new files with your own classes and functions.

```python
try:
    # Run algorithm!
    solution = algorithm(K, ALL_ORDERS, ALL_RIDERS, DIST, timelimit)
except Exception as e:
    exception = f'{e}'
```

This runs your algorithm.

```python
lg_end_time = time.time()

with open(problem_file, 'r') as f:
    prob = json.load(f)

K = prob['K']

ALL_ORDERS = [Order(order_info) for order_info in prob['ORDERS']]
ALL_RIDERS = [Rider(rider_info) for rider_info in prob['RIDERS']]

DIST = np.array(prob['DIST'])
for r in ALL_RIDERS:
    r.T = np.round(DIST/r.speed + r.service_time)

checked_solution = solution_check(K, ALL_ORDERS, ALL_RIDERS, DIST, solution)

checked_solution['time'] = alg_end_time - alg_start_time
checked_solution['timelimit_exception'] = (alg_end_time - alg_start_time) > timelimit + 1 # allowing additional 1 second!
checked_solution['exception'] = exception

checked_solution['prob_name'] = prob['name']
checked_solution['prob_file'] = problem_file
```

This validates the solution. `solution_check` verifies feasibility and reports any violations.

```python
{'total_cost': 573047.2,
 'avg_cost': 5730.472,
 'num_drivers': 50,
 'total_dist': 354962,
 'feasible': True,
 'infeasibility': None,
 'bundles': [['BIKE', [14], [14]],
  ['BIKE', [28], [28]],
  ['BIKE', [29], [29]],
  ['BIKE', [85], [85]],
  ['BIKE', [93], [93]],
  
  ...
  
  ['BIKE', [67, 61], [61, 67]],
  ['BIKE', [71, 73], [73, 71]],
  ['BIKE', [5, 0], [0, 5]],
  ['BIKE', [22, 75, 98], [22, 75, 98]]],
 'time': 9.459444999694824,
 'timelimit_exception': False,
 'exception': None,
 'prob_name': 'TEST_K100_1',
```
