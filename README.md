# 🏎️ F1 Driver Skill Quantification via Autoencoder

이 프로젝트는 F1 텔레메트리 데이터를 활용하여 오토인코더(Autoencoder) 기반으로 드라이버의 주행 실력을 정량화하는 것을 목표로 합니다. 2023 일본 그랑프리 데이터를 바탕으로 상위권 드라이버의 "이상적인 주행 패턴"을 학습하고, 이를 기준으로 개별 드라이버의 주행 오차(복원 오차)를 측정하여 실력을 분석합니다.

## 📌 주요 목표

1.  **드라이버 실력 정량화**: 단순 랩 타임 비교가 아닌, 텔레메트리 데이터를 통한 정밀 분석
2.  **이상치 탐지 (Anomaly Detection)**: 오토인코더를 활용하여 정상 주행 범위를 벗어나는 실수(Error)나 특이 패턴 탐지
3.  **DEI (Driver Error Index)**: 복원 오차를 바탕으로 드라이버 에러 지수 개발

## 📂 프로젝트 구조

-   `EDA/`: 데이터 탐색적 분석 (Exploratory Data Analysis) 파일들이 위치합니다.
-   `modeling/`: 모델 학습 및 평가 관련 코드가 위치합니다. **핵심 모델링 코드는 이곳에 있습니다.**
    -   `modeling_AE.ipynb`: 오토인코더 모델링 메인 노트북
-   `src/`: 데이터 로드 및 전처리를 위한 소스 코드
-   `fastf1_cache/`: FastF1 라이브러리 데이터 캐시

## 🚀 모델링 확인 방법 (Modeling)

모델링과 관련된 상세 코드와 분석 과정은 `modeling` 디렉토리 내의 주피터 노트북에서 확인하실 수 있습니다.

-   **메인 모델링 파일**: `modeling/modeling_AE.ipynb`
    -   이 파일에서 데이터 전처리, 모델 구조(LSTM-Autoencoder), 학습 과정, 그리고 결과 분석(Reconstruction Error)을 단계별로 볼 수 있습니다.

## 📊 데이터 및 방법론

-   **데이터셋**: 2023 Japanese Grand Prix (Suzuka) - Race Session
-   **학습 데이터**: Top 10 드라이버의 Clean Lap (Clean Air, No Pit/SC)만을 사용하여 "Gold Standard" 구축
-   **사용 모델**: LSTM-Autoencoder / CNN-Autoencoder
-   **주요 피처**:
    -   Physics: Speed, RPM
    -   Control: Throttle, Brake, nGear, DRS
    -   Engineered: `SLIP_DELTA` (Wheel lock/spin 감지)
    -   Context: TyreLife, Compound, LapNumber

## 📈 주요 분석 내용

프로젝트는 다음과 같은 분석 과정을 포함합니다:
1.  **휠락(Wheel Lock) 추정**: RPM과 속도 차이를 이용한 `SLIP_DELTA` 피처 생성
2.  **주행 패턴 학습**: 상위권 드라이버의 주행을 학습하여 이상적인 주행 모델 생성
3.  **실력 평가**: 테스트 데이터의 복원 오차(Reconstruction Error)를 계산하여 드라이버별 일관성 및 실수 패턴 분석

---
*Developed by Time-Series Team Project*
