# 경연 문제


이 문서는 [prob_gen_stage3.ipynb](rawdata/prob_gen_stage3.ipynb)를 기준으로,
아래 3개 raw 주문 데이터에서 Stage 3 문제 인스턴스를 생성한 과정을 설명합니다.

- [opt_challenge_data_order_density_high.csv](rawdata/opt_challenge_data_order_density_high.csv)
- [opt_challenge_data_order_density_medium.csv](rawdata/opt_challenge_data_order_density_medium.csv)
- [opt_challenge_data_order_density_low.csv](rawdata/opt_challenge_data_order_density_low.csv)

Stage1과 Stage2에서는 단일 raw 데이터에서 인스턴스를 생성했지만, Stage3에서는 위 세 raw 데이터를 활용해 다양한 밀도/패턴의 인스턴스를 만들었습니다. 특히, 세 raw 데이터에서 각각 부분 인스턴스를 만든 뒤 이를 공간적으로 섞는 방식으로 복합 분포 인스턴스도 생성했습니다.

Stage1/2의 문제 생성은 노트북 [prob_gen_stage1.ipynb](rawdata/prob_gen_stage1.ipynb)와 [prob_gen_stage2.ipynb](rawdata/prob_gen_stage2.ipynb)를 참고해주세요. 

---

## 1) 입력 데이터와 전처리

노트북의 `gen_problem_instance(...)` 함수는 raw CSV를 읽은 뒤 다음 컬럼을 생성합니다.

- `ord_time_sec`: 데이터 내 최소 주문시각(`earliest_date`) 기준 상대 초 단위 시간
- `cook_time_sec`: `cook_time(분)`를 초 단위로 변환
- `capacity_bike`: 원본 용량값에 100을 곱해 정수화

핵심 목적은 주문 시계열을 동일한 기준축(초 단위)으로 정규화하고,
생성되는 인스턴스 JSON이 바로 계산에 쓰일 수 있도록 수치형으로 고정하는 것입니다.

---

## 2) 시간 구간 샘플링

인스턴스는 raw 전체 기간에서 임의의 연속 구간을 먼저 뽑고, 그 안에서 주문을 선택합니다.

1. 길이 `sampling_time_span_seconds`(예: 2시간, 3시간, 8시간)인 시간창을 랜덤 시작점으로 선택
2. 해당 시간창에 포함된 주문 수가 `K * 1.2` 이상일 때까지 재시도
3. 조건을 만족한 시간창에서 `K`개 주문을 비복원 랜덤 샘플링
4. 샘플된 주문들의 시간축을 다시 0부터 시작하도록 재정렬

즉, **무작위 시작시각 + 최소 밀도 보장 + 최종 K개 추출** 구조입니다.

---

## 3) 거리 행렬과 주문(deadline) 계산

### 거리 행렬(`DIST`)

- 각 주문의 상점/배송 좌표를 모아 총 `2K`개 노드 구성
- 모든 노드 쌍의 거리를 haversine 기반으로 계산
- 지구 반경 기반 거리(km)를 m 단위로 변환 후 스케일러 `1.4`를 곱해 정수화

### 주문 정보(`ORDERS`)

각 주문은 아래 형식으로 기록됩니다.

`[ORD_ID, ORD_TIME, SHOP_LAT, SHOP_LON, DLV_LAT, DLV_LON, VOL, COOK_TIME, DLV_DEADLINE]`

deadline은 차량(CAR) 기준 도착 가능시간 + 버퍼로 설정됩니다.

DLV_DEADLINE = ORD_TIME + COOK_TIME + CAR_SERVICE_TIME + BUFFER_TIME + (shop→delivery 거리 / CAR 속도)

추가로 `INC_BUFFER_TIME_PROB` 확률로 `INC_BUFFER_TIME`(분)을 deadline에 더해,
주문별 마감시간 난이도에 랜덤 편차를 부여합니다.

---

## 4) 라이더 파라미터 설정

인스턴스에는 세 라이더 타입이 포함됩니다.

- `BIKE`, `WALK`, `CAR`

각 타입별로 다음 값이 들어갑니다.

- 속도(`speed`)
- 용량(`capa`)
- 변동비(`var_cost`)
- 고정비(`fixed_cost`)
- 서비스 시간(`service_time`)
- 가용 대수(`available number`)

기본적으로 `NUM_*_RATIO × K`로 가용 대수를 만들며,
노트북에서는 인스턴스별로 ratio/고정비/버퍼를 다르게 주어 난이도를 조정했습니다.

---

## 5) 3개 rawdata를 활용한 생성 방식

노트북에서는 high/medium/low 밀도 데이터를 다음 두 방식으로 사용합니다.

### A. 단일 소스 인스턴스

하나의 raw CSV에서 `gen_problem_instance(...)`를 직접 호출해 생성합니다.

- 예: `STAGE3_1`(high), `STAGE3_2`(medium), `STAGE3_3`(low)

### B. 혼합(Mixed) 인스턴스

세 raw CSV에서 각각 부분 인스턴스를 만든 뒤 `merge_problems(...)`로 합칩니다.

1. high/medium/low 각각에서 `K`와 seed를 다르게 설정해 부분 문제 생성
2. `merge_orders(...)`에서 각 부분 주문군의 좌표를 평행이동(`translations`) 및 회전(`rotations`)
3. 세 주문군을 시간 기준으로 합치고 `ORD_ID` 재할당
4. 합쳐진 전체 주문으로 거리행렬 재계산, 라이더 가용 대수는 부분 문제들의 합으로 구성

이 과정을 통해 단일 밀도 패턴이 아닌 **공간적으로 섞인 복합 분포 인스턴스**를 만듭니다.


![Stage3용 3개의 rawdata를 합쳐 만든 문제 예](instance_gen_example.png)

그림에서 각각의 색은 high/medium/low raw에서 생성된 주문군을 나타냅니다. 세 군이 공간적으로 섞여 있어, 라이더가 다양한 패턴의 주문을 동시에 처리해야 하는 상황이 됩니다.


