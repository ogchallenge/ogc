# 알고리즘 개발 환경 및 baseline 알고리즘 설명

*Update history:*

- *2024/09/10 - `ogc2024_env.yml` updated - `scikit-learn-extra` package 사용가능*
- *2024/07/20 - `baseline_20240720.zip` updated*
- *2024/07/12 - Java (openjdk 17.0.11) 사용 가능*
- *2024/07/01 - `baseline_20240701.zip` updated*
- *2024/06/29 - 알고리즘 제출 시 압축파일 형태 확인 설명 추가*
- *2024/06/24 - 알고리즘 실행 결과 error code 설명 추가*
- *2024/06/21 - `baseline_20240621.zip` updated*
- *2024/06/16 - `baseline_20240616.zip` updated*
- *2024/06/03 - Microsoft.NETCore.App 7.0.19 사용 가능*
- *2024/05/17 - 상용 최적화 솔버 라이센스 발급 관련 내용 추가*
- *2024/05/17 - `baseline_20240517.zip` updated*

본 페이지에서는 경연에 참가하기 위해 알고리즘 코드를 작성하는 방법을 예제로 제공되는 baseline 알고리즘을 통해 설명합니다. 

## 1. 환경설정

알고리즘을 제출하기 전에 먼저 참가팀은 개인의 PC에서 알고리즘을 구현하고 알고리즘이 작동하는지 확인해야 합니다. 이를 위해 개인 PC에 알고리즘 평가용 서버와 같은 Python 환경을 만드는 과정을 설명합니다. 

참가팀이 사용 가능한 Python 패키지의 목록은 다음과 같습니다. 이들 패키지를 개별로 하나씩 설치할 필요 없이 아래의 conda 환경 생성을 이용하면 간단하게 평가 서버와 같은 환경을 만들 수 있습니다.

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

> 💡 알고리즘 구현에 필요한 패키지가 있으면 Slack 채널에서 요청하시면 추가할 수 있습니다!

### Conda 환경 만들기

Conda는 가상환경을 만들어 주는 프로그램입니다. 아나콘다([Anaconda](https://www.anaconda.com/download)) 또는 [miniforge](https://github.com/conda-forge/miniforge)등을 통해 설치할 수 있습니다. 

> 💡 Conda가 무엇이고 왜 필요한지는 [여기](https://wikidocs.net/135082)를 참조하세요!

Conda 환경 생성 절차

[ogc2024_env.yml](baselines/ogc2024_env.yml)

1. 위 파일을 다운로드 해서 임의의 폴더에 저장합니다. 
2. 저장한 폴더로 이동합니다.
3. Terminal 또는 cmd로 다음을 실행합니다.
    
    `conda env create -f ogc2024_env.yml`
    
4. 여러 패키지를 설치하는 과정이 보입니다. 모두 끝나면 다음을 실행합니다.
    
    `conda activate ogc2024`
    
5. Terminal 또는 cmd 창에 다음과 같이 표시되면 환경 설정 완료입니다.

![Windows Anaconda Prompt](anaconda-prompt.png)

Windows Anaconda Prompt

## 2. 알고리즘 제출 방법

[baseline_20240720.zip](baselines/baseline_20240720.zip)

[alg_test_problems_20240429.zip](baselines/alg_test_problems_20240429.zip)

먼저 위 두 파일을 받아서 적당한 폴더에서 압축을 해제합니다. `baseline_2024XXXX.zip` 은 알고리즘 예제 코드를 압축한 파일이고 `alg_test_problems_2024XXXX.zip`은 baseline 코드를 실행하기 위한 문제 예제입니다.

> 💡 `baseline_2024XXXX.zip` 과 `alg_test_problems_2024XXXX.zip` 는 코드의 버그 수정등의 이유로 종종 업데이트 될 수 있음! 주기적으로 최신 버전을 확인 필요!

> 💡 `alg_test_problems_2024XXXX.zip` 은 예선 문제가 아님! 예선, 본선 등 각 단계의 문제는 각 단계가 시작될때 공개함!

두 압축 파일을 다음과 같이 압축 해제합니다. 

![baseline 압축 파일 내용](baseline-folder-structure.png)

`baseline` 폴더에는 다음의 파일들이 있습니다.

- `myalgorithm.py` : **실제로 알고리즘을 구현하는 파일. 가장 중요함!**
- `util.py`: 알고리즘 구현에 도움이 되는 함수들이 포함된 파일.
- `alg_test.ipynb` : 알고리즘을 간단히 실행 해 볼 수 있는 Jupyter notebook.

먼저 `myalgorithm.py` 파일을 살펴 봅시다. 

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

`algorithm()`함수는 다음의 파라메터로 호출됩니다.

- `K`: 주문의 개수
- `all_orders`: 주문의 list
- `all_riders`: 배달원의 list
- `dist_mat`: 거리 행렬(distance matrix)
- `timelimit` : 알고리즘 실행시간(초). 이 시간 이내에 알고리즘은 실행을 종료해야 합니다.

`#------------- Custom algorithm code starts from here --------------#`

와

`#------------- End of custom algorithm code --------------#`

사이에 알고리즘을 작성하면 됩니다. 이 때 주어진 `K`,`all_orders`, `all_riders`, `dist_mat`, `timelimit` 를 이용해서 알고리즘은 해(solution)을 찾아야 합니다. 

> 💡 `baseline` 코드는 아주 간단한 예제 알고리즘을 포함하고 있음. 실제 제출시에는 이 부분을 참가팀의 알고리즘 코드로 바꿔서 제출해야 함!

> 💡 `baseline` 코드를 일부 사용하거나 수정하는것은 허용되나 그대로 제출은 권장하지 않음! ⇒ 하루에 한번 제출 가능하니 의미없는 알고리즘 제출은 지양!

> 💡 `myalgorithm.py` 파일의 이름과 함수 `def algorithm(K, all_orders, all_riders, dist_mat, timelimit=60):` 이름은 **절대로** 변경 불가!

해는 다음의 구조를 가져야 합니다. 

- 주어진 문제에 대해 `[배달원 종류, 음식점 방문 순서, 고객 방문 순서]` 의 리스트를 반환
    - 방문 순서는 주문  `[1,3,2]` 와 같이 주문 id의 순서로 정의됨
    - 예) `["BIKE", [1,3,2], [2,3,1]]`
        - 의미: 주문 1, 2, 3을 묶어 오토바이 배달원에 할당하고 1,3,2 순서로 픽업 장소를 방문하고 2,3,1 순서로 배달 장소 방문

목적함수 및 제약사항 만족 여부는 체점 시스템에서 수행합니다. 자세한 사항은 문제 설명 페이지를 참조하세요.

### 알고리즘 제출 방법

작성한 알고리즘은 하나의 파일로 압축해서 제출합니다. 이 때 다음의 조건들을 만족해야 합니다.

- 하나의 `zip`파일로 압축 (압축 파일 이름은 임의로 지정)
- 필수 파일: `myalgorithm.py`, `util.py`
- `myalgorithm.py` 파일은 압축을 풀었을 때 하위 폴더에 있으면 안됨.
    - 압축 파일을 풀었을 때 최상위 폴더에 `myalgorithm.py`이 존재해야 함!

> 💡 **제출하는 압축파일의 `myalgorithm.py` 는 압축파일 내부의 하위폴더에 있으면 안됨!!!!**
>
> **`myalgorithm_best.py`와 같이 파일 이름을 바꿔도 안됨!!!!**
>
> ![올바른 제출용 압축 파일](submission-correct-structure.png)
>
>
> ![잘못 압축된 제출용 파일](submission-incorrect-structure.png)
>
>
> MacOS 또는 Linux에서는 다음과 같이 압축파일 내부의 폴더를 조회할 수 있음
>
> ![압축파일 내부 폴더 조회](submission-terminal-check.png)
>
> 위와 같이 Terminal에서 `unzip -vl 압축파일.zip` 을 실행했을 때 **아래 경우와 같이 `myalgorithm.py`이 폴더(이 경우에는 `test1`) 아래에 위치하면 안됨!!!**

- 알고리즘 실행을 위해 필요한 추가적인 파일(neural network checkpoint 등)이 있으면 같이 압축함. 이 때 별도의 폴더를 만들어서 추가적인 파일들을 저장해도 문제 없음.
- `alg_test.ipynb` 는 제출하지 않아도 상관 없음.
- `util.py` 파일은 수정 불가! (수정해서 같이 제출해도 평가시에 원래 파일로 replace한 후 평가함)
- 별도의 Python 파일(모듈)을 추가 가능. 모두 같이 압축되어야 함.
- 압축 파일의 크기는 30MB이하 (용량이 부족하면 Slack 채널에서 용량 증가를 요청하세요.)

정리하면 압축을 풀어서 안에 포함된 `myalgorithm.py` 함수의 `algorithm()` 함수를 `ogc2024` 환경에서 실행이 가능해야 합니다. 

> 💡 작성한 알고리즘이 평가 서버에서 잘 살행될지 확인하는 가장 쉬운 방법은 뒤에 설명할 Jupyter notebook으로 알고리즘이 잘 실행되는것을 확인한 후 알고리즘이 포함된 폴더에 있는 파일들을 그대로 압축하는것!

> 💡 평가 서버에서는 **숨겨진** 문제로 알고리즘을 실행하기 때문에 문제 파일은 같이 제출할 필요 없음!

### Python이 아닌 다른 언어를 사용하는 방법

Python이 아닌 다른 언어 또는 라이브러리를 사용하는것도 가능합니다. 필요한 라이브러리를 모두 포함해서 압축 파일을 만들고 단지 `myalgorithm.py` 에서 다른 언어의 함수를 실행하도록 작성하면 됩니다. 

Guroby, Xpress, ORTools 와 같은 MIP solver는 Python 환경에서만 사용 가능합니다. 본 대회는 Python을 중심으로 다른 언어는 수리모형의 실행이 아닌 계산 시간을 단축하기 위한 subroutine으로만 사용하는것을 권장합니다. (참고로 수리모형의 실행 속도는 사용 언어와 관계없습니다.)

또한 참가팀들간의 형평성과 알고리즘 실행 환경의 변화를 방지하기 위해 전체 시스템에 설치가 필요한 언어 또는 라이브러리의 설치는 최대한 신중하게 결정할 예정입니다. 참가팀은 최선을 다해 사용 하고 싶은 모든것을 하나의 압축파일으로 localize 해서 다른 참가팀의 알고리즘 실행에 영향이 없도록 할 의무가 있습니다.

> 💡 Python이 아닌 다른 언어의 경우 평가 서버의 실행환경을 유의 할것. 예를 들어 C/C++로 알고리즘을 구현하고자 하면 먼저 Linux/Ubuntu 22.04 환경에서 컴파일 후 생성된 `so` 파일 또는 실행파일을 제출하여야 함. 평가 서버에서 컴파일 과정을 수행하지 않음!

> 💡 평가 서버와 같은 환경을 가상머신등을 통해 만들어서 알고리즘의 작동을 확인할것을 추천!

> 💡 별도의 컴파일 과정이 필요 없은 언어(Julia 등)를 사용하고자 할때도 Slack 채널을 통해 요청 후 사용 가능함을 먼저 확인할것!

> 💡 평가 서버에서 컴파일을 수행하지 않지만 작성한 라이브러리등의 소스를 포함해서 압축 후 제출할것!

### Java, Dotnet 사용 방법 (2024-7-12 updated)

참여팀의 요구로 Java와 dotnet framework를 설치했습니다. 설치 방법은 다음과 같습니다.

- Java
    - `sudo apt-get update`
    - `sudo apt-get install openjdk-17-jdk`
    - `java --version`
        
        ![Java 버전 확인](java-version-check.png)
        
- Dotnet framework(C#)
    - `sudo apt install -y dotnet-runtime-7.0`
    - `dotnet --info`
        
        ![Dotnet 정보 확인](dotnet-info-check.png)
        

### 알고리즘 제출 시 에러 코드 설명

알고리즘을 평가 서버로 제출하고 알고리즘의 실행이 끝나고 리더 보드가 업데이트 되면 참가팀은 제출한 알고리즘들의 실행 상태를 조회할 수 있습니다.

![제출 결과 테이블](submission-results-table.png)

위 그림과 같이 제출한 일자 별로 알고리즘의 실행결과를 보여줍니다. 알고리즘이 평가문제를 시간제한 내에 잘 풀면 화면과 같이 목적함수(평균 배달 비용)값을 보여줍니다. 만약에 알고리즘 실행도중에 문제가 발행하면 간단하게 그 이유를 알 수 있습니다. `alg_error` 는 알고리즘 실행 도중 `Python exception`이 발생했음을 의미합니다.  

`sys_error` 는 다음과 같이 세부 에러코드를 보여줄 수도 있습니다.

- `sys_error(03)`: 제출한 압축파일을 평가서버에서 압축해제 실패(잘못된 압축파일 형식)
- `sys_error(05)`: 제출한 압축파일의 최상의 폴더에서 `myalgorithm.py`를 찾을 수 없음

`test_error`는 알고리즘을 실행이 불가능한 경우에 발생합니다. 

- `test_error(01)`: 제출한 압축파일에서 `ogc2024` 환경에 존재하지 않는 Python package를 `import` 를 시도함

세부 에러코드는 대회가 진행됨에 따라 추가될 수 있습니다.

## 3. Baseline 알고리즘 실행 방법

알고리즘을 구현하고 제출하기 위해서는 참가자 PC에서 알고리즘을 실행하면서 알고리즘의 결과를 살펴봐야 합니다. 이를 위해 `alg_test.ipynb` 를 사용할 수 있습니다.

> 💡 이하의 내용은 Jupyter notebook을 사용할 수 있는 환경은 기준으로 설명함. Jupyter notebook은 JupyterLab 또는 Visual Studio Code 등을 설치하면 사용 가능.

VSCode 또는 JupyterLab으로 `alg_test.ipynb` 파일을 열면 다음과 같이 됩니다.

![VSCode 화면](vscode-screen.png)

VSCode 화면

![JupyterLab 화면](jupyterlab-screen.png)

JupyterLab 화면

> 💡 Notebook을 연 후 Jupyter kernel이 `ogc2024` 환경인지 꼭! 확인필요!  JupyterLab의 경우에는 먼저 cmd 또는 Terminal에서 `ogc2024` 환경을 activate 한 후 `jupyter-lab` 을 실행하면 됨.

노트북의 cell을 실행하면 노트북과 같은 폴더에 있는 `myalgorithm.py` 파일의 알고리즘이 실행됩니다. 아래에 실행 코드를 간단히 설명합니다.

```python
problem_file = '../alg_test_problems_20240429/TEST_K100_1.json'
timelimit = 10
```

알고리즘이 풀 문제 파일을 읽어옵니다. `'../alg_test_problems_20240429/TEST_K100_1.json` 부분은 문제의 경로(path)를 지정합니다. 이 예제에서는 위에서 같이 압축푼 테스트 문제의 경로가 지정되어 있습니다. 각 단계별로 문제가 공개되면 이들 문제를 저장하고 그 파일경로를 지정하세요!

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

문제 파일을 읽어와서 알고리즘이 문제를 풀 준비를 하는 부분입니다. 이 부분은 실제로 평가 서버에서도 동일하게 수행됩니다. `Rider` 또는 `Order`등의 class는 알고리즘 구현을 돕기위한 것들이고 `util.py`에 정의되어 있습니다.

> 💡 `util.py` 에 정의된 함수 또는 class는 수정할 수 없음! 수정이 필요하면 새로운 파일에 새로운 class와 함수들을 정의해서 그것을 사용할것!

```python
try:
    # Run algorithm!
    **solution = algorithm(K, ALL_ORDERS, ALL_RIDERS, DIST, timelimit)**
except Exception as e:
    exception = f'{e}'
```

알고리즘이 실행되는 부분입니다. `algorithm(K, ALL_ORDERS, ALL_RIDERS, DIST, timelimit)` 명령어를 통해 `myalgorithm.py` 에 작성한 알고리즘이 실행됩니다. 

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

알고리즘 실행 후 해를 검사하는 부분입니다. 특히 `solution_check(K, ALL_ORDERS, ALL_RIDERS, DIST, solution)` 명령어는 알고리즘의 해가 제약을 모두 만족하여 유효한지 확인하고 만약에 유효하지 않으면 간단하게 이유를 알려줍니다. 해의 유효성을 확인하는 자세한 과정은 `util.py` 의 함수 코드를 확인하세요!

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

위는 `checked_solution` 의 내용입니다. 중요한 항목을 살펴보면

- `avg_cost`: 평균 비용. 즉 목적 함수
- `feasible`: 해가 유효한지 여부
- `infeasibility`: 해가 유효하지 않은 이유. 해가 유효하면 `None`
- `timelimit_exception`: 시간제한 준수 여부
- `exception`: 알고리즘 실행 중에 예외 발생 상황. 예외 없으면 `None`

> 💡 `checked_solution` 에서 `bundles` 항목만이 알고리즘이 반환한 해(**`solution = algorithm(...)`**)이고 나머지는 `solution_check()` 에서 별도로 계산하고 확인해서 추가함.

> 💡 알고리즘의 실행 시간은 문제를 읽어오거나 `check_solution()` 등의 시간은 모두 제외하고 순수하게 `algorithm(K, ALL_ORDERS, ALL_RIDERS, DIST, timelimit)` 이 실행되는 시간을 의미하고 이 시간이 제한시간을 넘으면 안됨! 위 예제에서 `'time'` 은 실제로 알고리즘이 실행된 시간(wall clock기준)을 나타냄. 제한시간을 넘으면 `'timelimit_exception'` 이 `True` 가 되며 이 경우에는 solution과 상관없이 penalty 점수를 얻게 되니 주의!

![배달 경로 시각화](solution-route-visualization.png)

`draw_route_solution(ALL_ORDERS, checked_solution)` 명령은 알고리즘 해의 경로를 보여줍니다. 

![묶음 배송 상세 정보](solution-bundle-details.png)

`draw_bundle_solution(ALL_ORDERS, ALL_RIDERS, DIST, checked_solution)` 명령은 묶음 배송마다 자세한 정보를 보여줍니다. 특히, 각각의 픽업과 배달의 시간이 시간 제약안에 있는지 여부를 확인할 수 있습니다.

> 💡 노트북의 코드를 수정해도 실제 알고리즘의 코드는 `myalgorithm.py` 안에 있기 때문에 알고리즘 평가 서버에서의 실행에 영향을 미치지 않음. 즉, 이 노트북은 알고리즘 개발 단계에서 알고리즘이 주어진 Python 환경 `ogc2024`에서 잘 실행되는지 확인하고, 알고리즘의 결과를 살펴 보는것이 목적임.

## 4. 상용 최적화 Solver 라이센스 발급 관련

참가팀은 기본적으로 공개 SW 최적화 솔버인 Google ORTools를 이용할 수 있습니다. 만약에 최적화 경연 참가팀 중에서 상용 최적화 솔버 라이선스가 필요하신 팀은 아래 연락처로 메일을 보내셔서 솔버 라이선스 발급을 요청할 수 있습니다.

> Gurobi : [kangju.lee@gurobi.com](mailto:kangju.lee@gurobi.com) (담당자 이강주 영업대표)
Xpress : [ricelove@optimasolution.co.kr](mailto:ricelove@optimasolution.co.kr) (담당자 윤기섭 수석)
> 

솔버 라이센스를 요청할 때는 다음의 사항들을 유의 하세요.

> 💡 메일 보내실 때, 제목에 "**[OGC2024] 솔버 라이센스 신청 - 참가팀명**" 표기

> 💡 솔버사 담당자가 경연 참가 여부를 확인하고, 솔버 라이선스 발급 작업 진행

> 💡 라이선스 유효기간 : 발급 시점 ~ 2024년 10월말 (최대)

> 💡 솔버 설치 및 사용 시 발생하는 기술적인 문제는 솔버사 담당자와 협의 요망.