# Project: F1 Driver Skill Quantification via Autoencoder

## 1. Project Overview
This project aims to quantify F1 driver skills by training an Autoencoder on telemetry data. The model learns the "ideal" driving patterns from the Top 10 performers and measures reconstruction errors or latent space distributions to analyze driving nuances.

## 2. Data Configuration
- **Event:** 2023 Japanese Grand Prix (Suzuka)
- **Session:** Race
- **Data Cache Path:** `fastf1_cache\2023\2023-09-24_Japanese_Grand_Prix`
- **Library:** `fastf1`, `pandas`, `numpy`, `scikit-learn`

## 3. Training Dataset (The "Gold Standard")
The model will be trained **ONLY** on the clean laps of the Top 10 finishers to establish a high-quality baseline.

**Target Drivers (Top 10):**
1. Max Verstappen (VER)
2. Lando Norris (NOR)
3. Oscar Piastri (PIA)
4. Charles Leclerc (LEC)
5. Lewis Hamilton (HAM)
6. Carlos Sainz (SAI)
7. George Russell (RUS)
8. Fernando Alonso (ALO)
9. Esteban Ocon (OCO)
10. Pierre Gasly (GAS)

## 4. Data Processing Pipeline

### Step 1: Data Loading & Filtering
Load race data for the target drivers and apply the following **strict filters** to ensure only "Pure Performance" laps are used:
1.  **Track Status:** Green flag only (`TrackStatus == '1'`).
2.  **Pit Stops:** Exclude In-laps and Out-laps.
3.  **Lap 1:** Exclude the standing start lap.
4.  **Clean Air Filter (Crucial):**
    * Calculate the time gap to the car ahead.
    * Calculate the time gap to the car behind.
    * **Condition:** Keep lap ONLY IF `Gap_Front > 1.5s` AND `Gap_Behind > 1.5s`.
    * *Reason:* To remove dirty air effects and defensive driving logic.

### Step 2: Feature Engineering
Construct the feature set including the physics-based engineered feature `SLIP_DELTA` and race context.

#### A. Core Telemetry Features
- `Speed` (km/h)
- `RPM`
- `Throttle` (0-100)
- `Brake` (Boolean or Pressure)
- `nGear`
- `DRS`

#### B. Engineered Feature: `SLIP_DELTA`
Goal: Detect wheel spin (traction loss) and wheel lock.
- **Logic:**
  1. Calculate `Baseline_Ratio_k` = Mean(`Speed` / `RPM`) for each gear $k$ (using clean laps).
  2. Calculate `Estimated_Speed` = `RPM` * `Baseline_Ratio_k`.
  3. **`SLIP_DELTA`** = `Estimated_Speed` - `Actual_Speed`.

#### C. Race Context Features
Since this is race data, context is required for the model to understand variable performance.
- `TyreLife`: Laps driven on current tires.
- `Compound`: One-Hot Encoded (SOFT, MEDIUM, HARD).
- `LapNumber`: To account for fuel load (weight) changes.

### Step 3: Preprocessing (Distance-Based)
**IMPORTANT:** Do NOT use Time as an index. Use Distance.
1.  **Resampling:** Interpolate all telemetry data to a fixed distance grid (e.g., every 1 meter or fixed N points per lap) to ensure fixed input dimensions for the Autoencoder.
2.  **Scaling:** Apply `MinMaxScaler` (0 to 1) to ALL features (including `SLIP_DELTA` and `Speed`).

## 5. Final Feature Set (Input Vector)
The resulting DataFrame for training should have the following columns (after encoding/scaling):

| Feature Type | Columns |
| :--- | :--- |
| **Physics** | `Speed`, `RPM` |
| **Control** | `Throttle`, `Brake`, `nGear`, `DRS` |
| **Engineered** | `SLIP_DELTA` |
| **Context** | `TyreLife`, `LapNumber`, `Compound_SOFT`, `Compound_MEDIUM`, `Compound_HARD` |

## 6. Model Objective
- Train an **LSTM-Autoencoder** or **CNN-Autoencoder**.
- **Input Shape:** `(Batch_Size, Sequence_Length, Num_Features)` where `Sequence_Length` corresponds to the fixed distance points per lap.