import csv
import random
from datetime import datetime, timedelta

# -------------------------------
# 設定
# -------------------------------
child_id = 1  # サンプル用に固定
start_date = datetime(2024, 10, 1)
days = 400

# 出力先
OUTPUT_DIR = "data/"
files = {
    "milk": OUTPUT_DIR + "milk_records.csv",
    "sleep": OUTPUT_DIR + "sleep_records.csv",
    "poop": OUTPUT_DIR + "poop_records.csv",
    "pee": OUTPUT_DIR + "pee_records.csv",
    "temp": OUTPUT_DIR + "temperature_records.csv",
    "food": OUTPUT_DIR + "food_records.csv",
}

# -------------------------------
# 授乳データ
# -------------------------------
with open(files["milk"], "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["child_id", "time", "amount", "note"])
    for d in range(days):
        date = start_date + timedelta(days=d)
        for _ in range(random.randint(5, 8)):  # 1日5〜8回
            t = date + timedelta(
                hours=random.randint(0, 23), minutes=random.randint(0, 59)
            )
            amount = random.choice([80, 100, 120, 150])
            note = random.choice(["", "母乳", "哺乳瓶"])
            writer.writerow([child_id, t.strftime("%Y-%m-%d %H:%M"), amount, note])

# -------------------------------
# 睡眠データ
# -------------------------------
with open(files["sleep"], "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["child_id", "start_time", "end_time", "note"])
    for d in range(days):
        date = start_date + timedelta(days=d)
        # 夜間睡眠
        start = date + timedelta(hours=22)
        end = date + timedelta(days=1, hours=6)
        writer.writerow(
            [
                child_id,
                start.strftime("%Y-%m-%d %H:%M"),
                end.strftime("%Y-%m-%d %H:%M"),
                "夜間",
            ]
        )
        # 昼寝2回
        for h in [10, 15]:
            st = date + timedelta(hours=h)
            ed = st + timedelta(hours=random.choice([1, 2]))
            writer.writerow(
                [
                    child_id,
                    st.strftime("%Y-%m-%d %H:%M"),
                    ed.strftime("%Y-%m-%d %H:%M"),
                    "昼寝",
                ]
            )

# -------------------------------
# うんちデータ
# -------------------------------
with open(files["poop"], "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["child_id", "time", "note"])
    for d in range(days):
        date = start_date + timedelta(days=d)
        for _ in range(random.randint(1, 3)):  # 1日1〜3回
            t = date + timedelta(
                hours=random.randint(6, 20), minutes=random.randint(0, 59)
            )
            note = random.choice(["普通便", "少なめ", "やわらかめ"])
            writer.writerow([child_id, t.strftime("%Y-%m-%d %H:%M"), note])

# -------------------------------
# おしっこデータ
# -------------------------------
with open(files["pee"], "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["child_id", "time", "note"])
    for d in range(days):
        date = start_date + timedelta(days=d)
        for _ in range(random.randint(6, 10)):  # 1日6〜10回
            t = date + timedelta(
                hours=random.randint(0, 23), minutes=random.randint(0, 59)
            )
            writer.writerow([child_id, t.strftime("%Y-%m-%d %H:%M"), ""])

# -------------------------------
# 体温データ
# -------------------------------
with open(files["temp"], "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["child_id", "time", "temperature", "note"])
    for d in range(days):
        date = start_date + timedelta(days=d)
        t = date + timedelta(hours=8)  # 朝測定
        temp = round(random.uniform(36.5, 37.5), 1)
        note = "" if temp < 37.0 else "少し高め"
        writer.writerow([child_id, t.strftime("%Y-%m-%d %H:%M"), temp, note])

# -------------------------------
# 離乳食データ
# -------------------------------
menus = ["おかゆ", "にんじんペースト", "かぼちゃスープ", "りんごすりおろし"]
with open(files["food"], "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["child_id", "time", "menu", "amount", "note"])
    for d in range(days):
        date = start_date + timedelta(days=d)
        for h in [12, 18]:  # 1日2回
            t = date + timedelta(hours=h)
            menu = random.choice(menus)
            amount = random.choice(["小さじ1", "大さじ2"])
            note = random.choice(["", "よく食べた", "残した"])
            writer.writerow(
                [child_id, t.strftime("%Y-%m-%d %H:%M"), menu, amount, note]
            )

print("✅ ダミーデータをCSVに出力しました")
