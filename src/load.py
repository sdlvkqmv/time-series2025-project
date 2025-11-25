import fastf1
import os

# 1. 캐시 폴더 설정 (데이터를 저장해두고 빠르게 불러오기 위함)
# 현재 경로에 'cache' 폴더가 없으면 생성
cache_dir = '../fastf1_cache'
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

fastf1.Cache.enable_cache(cache_dir) 

print("🔵 데이터 로드 시작... (첫 실행 시 시간이 걸릴 수 있습니다)")

# ==========================================
# A. Qualifying 세션 로드 (기준점 - Baseline)
# ==========================================
print("\n--- Loading Qualifying Session (Baseline) ---")
session_quali = fastf1.get_session(2023, 'Suzuka', 'Q')
session_quali.load() # 랩타임, 텔레메트리, 날씨 등 모든 데이터 로드

# 퀄리파잉 Flying Lap 필터링 (앞서 논의한 로직 적용)
quali_laps = session_quali.laps.pick_wo_box().pick_accurate()
pole_time = session_quali.laps.pick_fastest()['LapTime']
# 107% 룰 적용하여 Cool-down lap 제거
threshold = pole_time * 1.07
best_flying_laps = quali_laps[quali_laps['LapTime'] <= threshold]

print(f"✅ Quali 로드 완료: 총 {len(best_flying_laps)}개의 Flying Laps 확보")


# ==========================================
# B. Race 세션 로드 (분석 대상 - Main)
# ==========================================
print("\n--- Loading Race Session (Main Analysis) ---")
session_race = fastf1.get_session(2023, 'Suzuka', 'R')
session_race.load()

# 레이스 데이터는 별도 필터링 없이 전체를 가져오되, 정확도 필터만 적용
race_laps = session_race.laps.pick_accurate()

print(f"✅ Race 로드 완료: 총 {len(race_laps)}개의 Clean Laps 확보")

# ==========================================
# C. 데이터 확인
# ==========================================
print("\n[데이터 샘플 확인]")
print(f"Event: {session_race.event['EventName']}")
print(f"Track: {session_race.event['Location']}")
print("-" * 30)
print("Race Laps Columns:", race_laps.columns.tolist())