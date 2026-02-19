# 문제 생성 방법

여기서는 `stage3_prob_gen.ipynb`의 코드를 기준으로 Stage 3 문제가 어떻게 생성되는지 설명합니다. Stage 1/2 문제도 유사한 방식으로 생성되었으며, 세부적인 파라미터 설정과 그래프 구조에서 차이가 있습니다. 다음의 노트북을 다운로드하여 직접 같은 문제들을 생성해 볼 수 있습니다.

- [stage1_prob_gen.ipynb](prob_gen/stage1_prob_gen.ipynb)
- [stage2_prob_gen.ipynb](prob_gen/stage2_prob_gen.ipynb)
- [stage3_prob_gen.ipynb](prob_gen/stage3_prob_gen.ipynb)

---

## 1. 전체 생성 파이프라인

노트북의 흐름은 크게 다음과 같습니다.

1. `Prob(...)` 객체 생성
2. 다층 격자 그래프(`N`, `E`) 생성
3. 포트 간 수요(`K`) 랜덤 생성
4. 사용되지 않는 포트 제거(`remove_unused_ports`)
5. 하한(`LB`) 계산
6. JSON 저장 (`save_to_file`)
7. 생성된 14개 문제를 평가용 10개/연습용 4개로 분할

---

## 2. 핵심 클래스와 입력 파라미터

문제 인스턴스는 `Prob` 클래스에서 생성됩니다.

주요 파라미터:

- `P`: 포트(기항지) 수
- `H, W, L`: 층별 격자 높이/너비/층 수
- `F`: 포트별 고정 처리비(또는 기본 이동 관련 계수로 사용)
- `obstacle_ratio`: 장애물 노드 비율
- `total_allocation_ratio`: 수요 할당 총량 비율
- `min_demands`: 수요 생성 최소 단위 관련 파라미터
- `rnd_seed`: 랜덤 시드
- `inc`: 층이 올라갈 때 격자 크기 증가량
- `min_demand_interval`: 출발 포트와 도착 포트 간 최소 간격
- `asym_demand_prob`: 수요 분포 비대칭 여부
- `tri`, `diag`: 삼각형 형태/대각선 arc 생성 여부
- `ramp_one`, `rnd_ramp_pos`: 층간 연결 ramp 수/위치 제어

---

## 3. 그래프 생성 로직 (`_create_multilayer_grid_graph`)

### 3-1. 다층 격자 생성

- 각 층 `l`에 대해 크기 `H+inc*l`, `W+inc*l`의 격자를 구성합니다.
- 노드 타입은 기본적으로 `hold`로 시작합니다.
- `tri`, `diag` 설정에 따라 수평/수직/대각선 간선이 생성됩니다.

### 3-2. 층간 ramp 연결

- 인접 층 사이를 `ramp` 간선으로 연결합니다.
- `ramp_one=True`면 보통 단일 ramp 축을 사용하고,
- `rnd_ramp_pos=True`면 ramp 위치를 랜덤으로 배치합니다.

### 3-3. gate/obstacle 처리

- `(0,0,0)` 노드는 `gate`로 지정됩니다.
- `obstacle_ratio`에 따라 일부 `hold` 노드를 `obstacle`로 바꾸고 인접 간선을 제거합니다.

### 3-4. 노드 ID와 도달 가능성 정리

- gate 기준 최단거리로 정렬해 노드 ID를 부여합니다.
- gate에서 도달 불가능한 노드는 제거합니다.

결과적으로 그래프 정보는 아래처럼 인스턴스에 반영됩니다.

- `N`: 최종 노드 수
- `E`: 간선 목록(노드 ID 쌍)

---

## 4. 수요 생성 로직 (`_generate_random_demands`)

수요 `K`는 포트 쌍 `(origin, destination)`에 대해 랜덤 생성됩니다.

- 출발 포트는 초기 포트 쪽에 더 높은 확률이 주어지도록 샘플링됩니다.
- 도착 포트는 `origin + min_demand_interval` 이상에서 선택됩니다.
- 현재 할당량의 최대치(`allocations`)가 용량(`max_capa`)을 넘지 않도록 확인합니다.
- `total_allocation_ratio * max_capa * P`에 도달할 때까지 반복합니다.

`K`는 최종적으로 포트 쌍별 수요량 리스트로 저장됩니다.

---

## 5. 사용되지 않는 포트 제거 (`remove_unused_ports`)

수요의 출발/도착으로 한 번도 등장하지 않는 포트는 제거합니다.

- 새 포트 수 `new_P` 계산
- 기존 포트 인덱스를 압축하여 `new_K` 생성

이 정리 과정을 거쳐 문제 크기를 줄이고 불필요한 포트를 제거합니다.

---

## 6. 하한 계산 (`_get_LB`)

`LB`는 gate(노드 0) 기준 최단거리 기반의 단순 하한으로 계산됩니다.

- 각 포트의 loading/unloading 총수요를 집계
- `F * 수요 + 근접 노드 거리 합` 형태로 누적

이 값은 알고리즘 성능 비교를 위한 참고 하한으로 활용됩니다.

---

## 7. 저장 포맷 (`save_to_file`)

문제 JSON에는 기본적으로 다음 필드가 저장됩니다.

- `N`: 노드 수
- `E`: 간선 목록
- `P`: 포트 수
- `K`: 수요 목록
- `F`: 비용 계수
- `LB`: 하한

옵션 `with_graph=True`일 때는 디버깅/시각화를 위한 원본 그래프 정보도 포함됩니다.

- `grid_graph.nodes`
- `grid_graph.edges`

---

## 8. Stage 3 문제 세트 구성 방식

노트북에서는 `prob1.json` ~ `prob14.json`을 생성한 뒤,
아래 방식으로 평가/연습 문제를 분리합니다.

- 랜덤 시드 `np.random.seed(2)` 고정
- 14개 중 10개를 무작위 선택 → `stage3_problems` (평가용)
- 나머지 4개 → `stage3_exercise_problems` (연습용)
- 파일명은 각각 `prob1.json`부터 다시 순번 부여

---

## 9. 요약

`stage3_prob_gen.ipynb`의 핵심은 다음입니다.

- 다층/장애물/ramp 구조를 갖는 그래프를 랜덤하게 생성하고,
- 포트 간 수요를 용량 제약 하에 확률적으로 할당한 뒤,
- 불필요 포트 제거 및 하한 계산을 수행하여,
- 평가용/연습용 세트를 재현 가능한 시드 기반으로 분리해 배포 가능한 JSON으로 저장합니다.

