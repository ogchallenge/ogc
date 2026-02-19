# Algorithm Development Environment and Baseline Algorithm Description

*Update history:*

- *2024/09/10 - `ogc2024_env.yml` updated - `scikit-learn-extra` package available*
- *2024/07/20 - `baseline_20240720.zip` updated*
- *2024/07/12 - Java (openjdk 17.0.11) available*
- *2024/07/01 - `baseline_20240701.zip` updated*
- *2024/06/29 - Added explanation for checking submission archive format*
- *2024/06/24 - Added algorithm execution result error code explanation*
- *2024/06/21 - `baseline_20240621.zip` updated*
- *2024/06/16 - `baseline_20240616.zip` updated*
- *2024/06/03 - Microsoft.NETCore.App 7.0.19 available*
- *2024/05/17 - Added information about commercial optimization solver license issuance*
- *2024/05/17 - `baseline_20240517.zip` updated*

This page explains how to write algorithm code to participate in the competition using the baseline algorithm provided as an example.

## 1. Environment Setup

Before submitting an algorithm, participating teams must first implement the algorithm on their personal PC and verify that the algorithm works. This section explains the process of creating a Python environment identical to the algorithm evaluation server on your personal PC.

The list of Python packages available to participating teams is as follows. Instead of installing these packages individually one by one, you can easily create the same environment as the evaluation server using conda environment creation below.

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

> 💡 If you need a package for algorithm implementation, request it on the Slack channel and it can be added!

### Creating Conda Environment

Conda is a program that creates virtual environments. It can be installed through Anaconda ([Anaconda](https://www.anaconda.com/download)) or [miniforge](https://github.com/conda-forge/miniforge).

> 💡 For what Conda is and why it's needed, see [here](https://wikidocs.net/135082)!

Conda environment creation procedure

[ogc2024_env.yml](baselines/ogc2024_env.yml)

1. Download the above file and save it to any folder.
2. Navigate to the saved folder.
3. Run the following in Terminal or cmd:
    
    `conda env create -f ogc2024_env.yml`
    
4. You will see the process of installing various packages. When all finished, run the following:
    
    `conda activate ogc2024`
    
5. Environment setup is complete when displayed as follows in Terminal or cmd window:

![Windows Anaconda Prompt](anaconda-prompt.png)

Windows Anaconda Prompt

## 2. Algorithm Submission Method

[baseline_20240720.zip](baselines/baseline_20240720.zip)

[alg_test_problems_20240429.zip](baselines/alg_test_problems_20240429.zip)

First, download the above two files and extract them to an appropriate folder. `baseline_2024XXXX.zip` is an archive of algorithm example code and `alg_test_problems_2024XXXX.zip` is problem examples for running the baseline code.

> 💡 `baseline_2024XXXX.zip` and `alg_test_problems_2024XXXX.zip` may be frequently updated for reasons such as code bug fixes! Need to periodically check the latest version!

> 💡 `alg_test_problems_2024XXXX.zip` is not the preliminary problem! Problems for each stage such as preliminary, main, etc. are released when each stage begins!

Extract the two archive files as follows:

![Baseline archive contents](baseline-folder-structure.png)

The `baseline` folder contains the following files:

- `myalgorithm.py`: **The file where the algorithm is actually implemented. Most important!**
- `util.py`: File containing functions helpful for algorithm implementation.
- `alg_test.ipynb`: Jupyter notebook for simply running the algorithm.

Let's first look at the `myalgorithm.py` file.

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

- `K`: Number of orders
- `all_orders`: List of orders
- `all_riders`: List of riders
- `dist_mat`: Distance matrix
- `timelimit`: Algorithm execution time (seconds). The algorithm must finish execution within this time.

`#------------- Custom algorithm code starts from here --------------#`

and

`#------------- End of custom algorithm code --------------#`

Write your algorithm between these lines. At this time, the algorithm must find a solution using the given `K`, `all_orders`, `all_riders`, `dist_mat`, `timelimit`.

> 💡 The `baseline` code includes a very simple example algorithm. Upon actual submission, this part must be replaced with the participating team's algorithm code!

> 💡 Using or modifying parts of the `baseline` code is allowed but submitting as is is not recommended! ⇒ Since you can submit once per day, avoid submitting meaningless algorithms!

> 💡 The name of the `myalgorithm.py` file and the function name `def algorithm(K, all_orders, all_riders, dist_mat, timelimit=60):` are **absolutely** unchangeable!

The solution must have the following structure:

- For the given problem, return a list of `[rider type, restaurant visit order, customer visit order]`
    - Visit order is defined by order of order IDs like `[1,3,2]`
    - E.g.) `["BIKE", [1,3,2], [2,3,1]]`
        - Meaning: Bundle orders 1, 2, 3 and assign to a bike rider, visit pickup locations in order 1,3,2 and visit delivery locations in order 2,3,1

Objective function and constraint satisfaction are performed by the scoring system. For details, see the problem description page.

### Algorithm Submission Method

Submit the written algorithm compressed into one file. At this time, the following conditions must be met:

- Compress into one `zip` file (archive file name can be arbitrary)
- Required files: `myalgorithm.py`, `util.py`
- `myalgorithm.py` file must not be in a subfolder when extracted.
    - `myalgorithm.py` must exist in the top-level folder when the archive is extracted!

> 💡 **`myalgorithm.py` in the submitted archive must not be in a subfolder inside the archive!!!!**
>
> **Renaming the file like `myalgorithm_best.py` is also not allowed!!!!**
>
> ![Correct submission archive](submission-correct-structure.png)
>
>
> ![Incorrectly compressed submission file](submission-incorrect-structure.png)
>
>
> On MacOS or Linux, you can view folders inside the archive as follows:
>
> ![Viewing archive internal folders](submission-terminal-check.png)
>
> As above, when running `unzip -vl archive.zip` in Terminal, **`myalgorithm.py` must NOT be located under a folder (in this case `test1`) as in the case below!!!**

- If there are additional files needed to run the algorithm (neural network checkpoint, etc.), compress them together. Creating a separate folder to store additional files is fine.
- `alg_test.ipynb` does not need to be submitted.
- `util.py` file is not modifiable! (Even if modified and submitted together, it will be replaced with the original file during evaluation)
- Additional Python files (modules) can be added. All must be compressed together.
- Archive file size must be 30MB or less (If capacity is insufficient, request capacity increase on Slack channel.)

In summary, the `algorithm()` function of `myalgorithm.py` included in the extracted archive must be executable in the `ogc2024` environment.

> 💡 The easiest way to check if your written algorithm will run well on the evaluation server is to confirm that the algorithm runs well with the Jupyter notebook explained later, then compress the files in the folder containing the algorithm as is!

> 💡 Since the evaluation server runs algorithms on **hidden** problems, problem files do not need to be submitted together!

### How to Use Languages Other Than Python

It is also possible to use languages or libraries other than Python. Create an archive including all necessary libraries and simply write `myalgorithm.py` to execute functions in other languages.

MIP solvers like Gurobi, Xpress, and ORTools can only be used in Python environments. This competition recommends using Python as the center and other languages only as subroutines to shorten computation time, not for running mathematical models. (For reference, mathematical model execution speed is independent of the language used.)

Also, to prevent changes in algorithm execution environment and maintain fairness between participating teams, installation of languages or libraries requiring system-wide installation will be decided as carefully as possible. Participating teams have an obligation to do their best to localize everything they want to use into one archive file so as not to affect other participating teams' algorithm execution.

> 💡 For languages other than Python, pay attention to the evaluation server's execution environment. For example, if you want to implement an algorithm in C/C++, you must first compile in a Linux/Ubuntu 22.04 environment and submit the generated `so` file or executable. The evaluation server does not perform compilation!

> 💡 It is recommended to create an environment identical to the evaluation server through virtual machines, etc. to verify algorithm operation!

> 💡 Even when using languages that don't require separate compilation (Julia, etc.), first confirm availability by requesting through Slack channel!

> 💡 Although compilation is not performed on the evaluation server, include sources of written libraries, etc. when compressing and submitting!

### Java, Dotnet Usage Method (2024-7-12 updated)

Java and dotnet framework have been installed upon participating team request. Installation methods are as follows:

- Java
    - `sudo apt-get update`
    - `sudo apt-get install openjdk-17-jdk`
    - `java --version`
        
        ![Java version check](java-version-check.png)
        
- Dotnet framework(C#)
    - `sudo apt install -y dotnet-runtime-7.0`
    - `dotnet --info`
        
        ![Dotnet info check](dotnet-info-check.png)
        

### Algorithm Submission Error Code Explanation

After submitting an algorithm to the evaluation server and algorithm execution finishes and the leaderboard is updated, participating teams can view the execution status of submitted algorithms.

![Submission results table](submission-results-table.png)

As shown above, algorithm execution results are displayed by submission date. If the algorithm solves evaluation problems well within the time limit, the objective function (average delivery cost) value is shown as on screen. If a problem occurs during algorithm execution, the reason can be simply known. `alg_error` means a `Python exception` occurred during algorithm execution.

`sys_error` may show detailed error codes as follows:

- `sys_error(03)`: Failed to extract submitted archive on evaluation server (incorrect archive format)
- `sys_error(05)`: Cannot find `myalgorithm.py` in the top-level folder of submitted archive

`test_error` occurs when the algorithm cannot be executed.

- `test_error(01)`: Attempted to `import` a Python package that does not exist in the `ogc2024` environment from the submitted archive

Detailed error codes may be added as the competition progresses.

## 3. How to Run Baseline Algorithm

To implement and submit an algorithm, you must run the algorithm on your participant PC while examining algorithm results. You can use `alg_test.ipynb` for this.

> 💡 The following is explained based on an environment where Jupyter notebook can be used. Jupyter notebook is available by installing JupyterLab or Visual Studio Code.

Opening the `alg_test.ipynb` file with VSCode or JupyterLab looks like this:

![VSCode screen](vscode-screen.png)

VSCode screen

![JupyterLab screen](jupyterlab-screen.png)

JupyterLab screen

> 💡 After opening the notebook, be sure to check that the Jupyter kernel is the `ogc2024` environment! For JupyterLab, first activate the `ogc2024` environment in cmd or Terminal, then run `jupyter-lab`.

Running the notebook's cell executes the algorithm in the `myalgorithm.py` file in the same folder as the notebook. Below is a brief explanation of the execution code.

```python
problem_file = '../alg_test_problems_20240429/TEST_K100_1.json'
timelimit = 10
```

Read the problem file the algorithm will solve. The `'../alg_test_problems_20240429/TEST_K100_1.json` part specifies the problem path. In this example, the path of the test problem extracted above is specified. When problems are released for each stage, save those problems and specify their file path!

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

This is the part that reads the problem file and prepares the algorithm to solve the problem. This part is also performed identically on the actual evaluation server. Classes like `Rider` or `Order` are for helping algorithm implementation and are defined in `util.py`.

> 💡 Functions or classes defined in `util.py` cannot be modified! If modification is needed, define new classes and functions in a new file and use them!

```python
try:
    # Run algorithm!
    **solution = algorithm(K, ALL_ORDERS, ALL_RIDERS, DIST, timelimit)**
except Exception as e:
    exception = f'{e}'
```

This is the part where the algorithm executes. The algorithm written in `myalgorithm.py` executes through the command `algorithm(K, ALL_ORDERS, ALL_RIDERS, DIST, timelimit)`.

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

This is the part that checks the solution after algorithm execution. In particular, the command `solution_check(K, ALL_ORDERS, ALL_RIDERS, DIST, solution)` verifies that the algorithm's solution satisfies all constraints and is valid, and if not valid, simply tells the reason. For the detailed process of verifying solution validity, check the function code in `util.py`!

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
 'prob_file': '../alg_test_problems_20240429/TEST_K100_1.json'}
```

Above is the content of `checked_solution`. Looking at important items:

- `avg_cost`: Average cost. That is, objective function
- `feasible`: Whether solution is valid
- `infeasibility`: Reason solution is not valid. `None` if solution is valid
- `timelimit_exception`: Time limit compliance
- `exception`: Exception occurrence during algorithm execution. `None` if no exception

> 💡 In `checked_solution`, only the `bundles` item is the solution returned by the algorithm (**`solution = algorithm(...)`**), and the rest are separately calculated and verified by `solution_check()` and added.

> 💡 Algorithm execution time means purely the time `algorithm(K, ALL_ORDERS, ALL_RIDERS, DIST, timelimit)` executes, excluding all time for reading problems or `check_solution()`, etc., and this time must not exceed the time limit! In the above example, `'time'` represents the actual algorithm execution time (wall clock based). If the time limit is exceeded, `'timelimit_exception'` becomes `True`, and in this case, regardless of the solution, a penalty score is obtained, so be careful!

![Solution route visualization](solution-route-visualization.png)

The command `draw_route_solution(ALL_ORDERS, checked_solution)` shows the algorithm solution's routes.

![Solution bundle details](solution-bundle-details.png)

The command `draw_bundle_solution(ALL_ORDERS, ALL_RIDERS, DIST, checked_solution)` shows detailed information for each bundle delivery. In particular, you can verify whether the time of each pickup and delivery is within time constraints.

> 💡 Even if you modify the notebook code, it does not affect execution on the algorithm evaluation server because the actual algorithm code is in `myalgorithm.py`. That is, the purpose of this notebook is to verify that the algorithm runs well in the given Python environment `ogc2024` during the algorithm development stage, and to examine algorithm results.

## 4. Commercial Optimization Solver License Issuance

Participating teams can basically use Google ORTools, an open-source optimization solver. If any participating teams in the optimization competition need commercial optimization solver licenses, you can request solver license issuance by sending an email to the contact below.

> Gurobi: [kangju.lee@gurobi.com](mailto:kangju.lee@gurobi.com) (Contact person: Lee Kang-ju, Sales Representative)
Xpress: [ricelove@optimasolution.co.kr](mailto:ricelove@optimasolution.co.kr) (Contact person: Yoon Ki-seop, Principal)
> 

When requesting a solver license, note the following:

> 💡 When sending email, write "**[OGC2024] Solver License Application - Team Name**" in the subject

> 💡 The solver company contact person will verify competition participation and proceed with solver license issuance work

> 💡 License validity period: From issuance ~ End of October 2024 (maximum)

> 💡 For technical issues that occur during solver installation and use, consult with the solver company contact person.
