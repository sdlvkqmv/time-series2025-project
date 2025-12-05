# 📋 Vibe Coding Prompt: F1 2023 Suzuka EDA (Charts 7-10)

## **1. Context & Objective**
* **Goal:** `fastf1` 라이브러리를 사용하여 2023년 일본 그랑프리(Suzuka) 데이터를 분석하고, 오토인코더/LSTM 모델링을 위한 사전 EDA(Chart 7~10)를 수행한다.
* **Environment:** Python, `fastf1`, `pandas`, `matplotlib`, `seaborn`.
* **Cache:** `fastf1_cache` 폴더를 사용하여 데이터를 로드한다.

## **2. Phase 0: Data Preprocessing (Crucial)**
모든 차트는 데이터를 아래 세 가지 시나리오(**Data Subsets**)로 분리하여 분석해야 한다.

1.  **Session Load:**
    * Event: 2023 Japanese Grand Prix (Suzuka).
    * Sessions: Qualifying (`Q`), Race (`R`).
    * Load with `telemetry=True`.

2.  **Scenario Logic (Create 3 DataFrames):**
    * **Dataset A (Quali - Flying):**
        * Session: `Q`
        * Filter: `pick_wo_box()`, `pick_accurate()`, `is_flying_lap=True`.
    * **Dataset B (Race - Clean Air / Pure Pace):**
        * Session: `R`
        * Logic: 각 Lap마다 **앞차와의 간격(Gap to car ahead)**을 계산.
        * Filter: `Gap > 1.5s` (앞차의 방해를 받지 않는 상태).
    * **Dataset C (Race - Battle / Dirty Air):**
        * Session: `R`
        * Logic: 위와 동일.
        * Filter: `Gap <= 1.5s` (배틀 중이거나 Dirty Air 영향을 받는 상태).

> **Tip for Coding:** Race Session에서 앞차와의 간격을 계산할 때, 각 Driver의 `LapStartTime`과 `Position` 정보를 활용하여 바로 앞 순위 드라이버와의 시간 차를 근사치로 계산하는 로직을 구현할 것.

---

## **3. Phase 1: Chart Generation Plan**

### **🔵 Chart 7. Outlier Detection (Z-score Analysis)**
* **목적:** 배틀 상황(Scenario C)이 드라이버의 실수(Anomaly)에 미치는 영향 분석.
* **Data:** Dataset B (Clean) vs Dataset C (Battle).
* **Process:**
    1.  각 드라이버 및 시나리오별로 LapTime의 **Z-score** 계산 ($Z = \frac{x - \mu}{\sigma}$).
    2.  Threshold: $|Z| > 2.5$인 Lap을 'Outlier(실수)'로 정의.
    3.  드라이버별 Outlier 개수를 Count.
* **Visualization:**
    * **Grouped Bar Chart:**
        * X축: Driver (상위 10명 or 관심 대상).
        * Y축: Outlier Count.
        * Hue(색상): Scenario B(Clean) vs C(Battle).
    * *Insight:* 배틀 시 실수가 급증하는 드라이버 식별.

### **🔵 Chart 8. Driver Sector Stability (Best vs. Average Gap)**
* **목적:** 드라이버가 본인의 최고 퍼포먼스(Best Sector)를 얼마나 일관되게 재현하는가?
* **Data:** Dataset B (Race - Clean Air) *순수 실력을 보기 위함*.
* **Process:**
    1.  각 드라이버의 Sector 1, 2, 3별 `Best Time`과 `Average Time` 계산.
    2.  `Gap = Average Time - Best Time` 계산 (값이 작을수록 일관성 높음).
    3.  모든 Sector의 Gap을 합산하여 `Total Gap` 생성.
* **Visualization:**
    * **Stacked Bar Chart:**
        * X축: Driver (Total Gap 기준 정렬).
        * Y축: Delta Time (seconds).
        * Stack: Sector 1, Sector 2, Sector 3 Gap.
    * *Insight:* 특정 섹터에서 약한 드라이버 파악 (LSTM 입력 피처 중요도).

### **🔵 Chart 9. RPM-Speed Difference (Physical Feature: SLIP_DELTA)**
* **목적:** 휠락(Wheel Lock)이나 트랙션 손실(Slip)이 발생한 구간 탐지 (Feature Engineering 검증).
* **Data:** Dataset A (Quali)의 Fastest Lap에 대한 **Telemetry Data**.
* **Process:**
    1.  **Telemetry 로드:** 각 드라이버의 Fastest Lap 텔레메트리(Speed, RPM, nGear) 추출.
    2.  **Ratio Calculation:** 각 기어(nGear)별 `Speed / RPM` 평균 비율 계산 (정상 주행 기준).
    3.  **Feature Generation:**
        * `Estimated_Speed = RPM * Ratio`
        * `SLIP_DELTA = Estimated_Speed - Actual_Speed`
    4.  브레이킹 구간(Speed 감소 구간)에서의 `SLIP_DELTA`만 필터링.
* **Visualization:**
    * **KDE Plot (Kernel Density Estimate):**
        * X축: SLIP_DELTA.
        * Y축: Density.
        * Hue: Drivers (비교할 3~4명).
    * *Insight:* 분포의 꼬리(Tail)가 길수록 휠락이 잦거나 심하게 걸림.

### **🔵 Chart 10. Driver Performance Map (Clustering)**
* **목적:** 드라이버의 주행 성향(Style)을 2차원 공간에 매핑.
* **Data:** Dataset B (Race - Clean Air) 사용.
* **Process:**
    1.  **Axis X (Consistency):** LapTime의 표준편차(Std Dev).
    2.  **Axis Y (Tire Management):** LapNumber에 따른 LapTime의 기울기(Slope) - `Linregress` 사용.
    3.  **Bubble Size (Error Potential):** Chart 9에서 구한 `Avg SLIP_DELTA` 혹은 Chart 7의 `Outlier Count`.
* **Visualization:**
    * **Scatter Plot (Bubble Chart):**
        * 각 점은 드라이버를 나타냄.
        * 4분면으로 나누어 해석 (예: 일관성 높고 타이어 관리 잘함 = 우상단 등).
    * *Insight:* 드라이버별 클러스터링을 통해 모델의 `Label` 혹은 `Group` 정보로 활용.

---

## **4. Output Requirements**
1.  Python Code (Refactored & Modularized).
2.  각 Chart별 해석(Interpretation)을 주석으로 포함할 것.
3.  데이터프레임 전처리 과정에서 `SettingWithCopyWarning`이 발생하지 않도록 `.copy()`를 적절히 사용할 것.