import numpy as np
import pandas as pd


# --- 3. Telemetry Processing Functions (기존 로직 유지) ---

def calculate_slip_delta(telemetry_df):
    # (이전과 동일한 로직: Gear Ratio 기반 SLIP_DELTA 계산)
    baseline_data = telemetry_df[telemetry_df['nGear'] > 0]
    gear_ratios = {}
    for gear in baseline_data['nGear'].unique():
        gear_slice = baseline_data[baseline_data['nGear'] == gear]
        valid_rpm = gear_slice[gear_slice['RPM'] > 0]
        if len(valid_rpm) > 0:
            gear_ratios[gear] = (valid_rpm['Speed'] / valid_rpm['RPM']).mean()
            
    telemetry_df['Estimated_Speed'] = telemetry_df.apply(
        lambda row: row['RPM'] * gear_ratios.get(row['nGear'], 0), axis=1
    )
    telemetry_df['SLIP_DELTA'] = telemetry_df['Estimated_Speed'] - telemetry_df['Speed']
    return telemetry_df

def process_laps_to_tensor(laps_df, dist_points=200):
    """
    필터링된 Laps DataFrame을 받아 Telemetry를 추출하고 Resampling하여 통합 DataFrame 반환
    """
    processed_laps = []
    
    # 진행 상황 표시를 위해 enumerate 사용
    print(f"Processing {len(laps_df)} laps...")
    
    for i, (idx, lap) in enumerate(laps_df.iterrows()):
        try:
            # 1. Telemetry 로드
            telemetry = lap.get_telemetry()
            
            # 2. Distance Interpolation (Resampling)
            total_dist = telemetry['Distance'].max()
            new_dist = np.linspace(0, total_dist, dist_points)
            
            cols_to_interp = ['Speed', 'RPM', 'Throttle', 'nGear', 'DRS']
            new_data = {'Distance': new_dist}
            
            for col in cols_to_interp:
                new_data[col] = np.interp(new_dist, telemetry['Distance'], telemetry[col])
            
            new_data['Brake'] = np.interp(new_dist, telemetry['Distance'], telemetry['Brake'].astype(float))
            
            resampled_df = pd.DataFrame(new_data)
            
            # 3. Feature Engineering
            resampled_df = calculate_slip_delta(resampled_df)
            
            # 4. Context Features
            resampled_df['TyreLife'] = lap['TyreLife']
            resampled_df['LapNumber'] = lap['LapNumber']
            resampled_df['Compound_SOFT'] = 1 if lap['Compound'] == 'SOFT' else 0
            resampled_df['Compound_MEDIUM'] = 1 if lap['Compound'] == 'MEDIUM' else 0
            resampled_df['Compound_HARD'] = 1 if lap['Compound'] == 'HARD' else 0
            resampled_df['Driver'] = lap['Driver'] # 나중에 분석용으로 드라이버 태그 추가
            
            processed_laps.append(resampled_df)
            
        except Exception as e:
            continue
            
    if not processed_laps:
        return None
        
    return pd.concat(processed_laps, ignore_index=True)