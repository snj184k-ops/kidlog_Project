import csv
import random
from datetime import date, timedelta
import argparse


def generate_growth_data(child_id: int, sex: str, filename: str):
    """
    1年間 (1週間ごと) の身長・体重データを成長曲線に基づいて生成し、CSVに保存する
    """

    # WHO 標準成長曲線を参考にした 0ヶ月〜12ヶ月 の平均値
    if sex.lower() == "male":
        height_start, height_end = 50.0, 75.0  # cm
        weight_start, weight_end = 3.3, 9.6  # kg
    else:
        height_start, height_end = 49.0, 74.0
        weight_start, weight_end = 3.2, 8.9

    # start日を指定する
    start_date = date.today() - timedelta(weeks=52)
    # start_date = date(2024, 10, 1)

    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["child_id", "height", "weight", "date"])  # ヘッダー

        for week in range(53):  # 0〜52週 (1年分)
            ts = start_date + timedelta(weeks=week)

            # 線形補間 (0週→start, 52週→end)
            height = height_start + (height_end - height_start) * (week / 52)
            weight = weight_start + (weight_end - weight_start) * (week / 52)

            # ±2% のノイズを加えるとリアル感が出る
            height *= random.uniform(0.98, 1.02)
            weight *= random.uniform(0.98, 1.02)

            writer.writerow(
                [
                    child_id,
                    round(height, 1),
                    round(weight, 1),
                    ts.strftime("%Y-%m-%d"),
                ]
            )

    print(f"✅ CSVファイルを出力しました: {filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("child_id", type=int, help="子供のID")
    parser.add_argument(
        "sex", type=str, choices=["male", "female"], help="性別 (male/female)"
    )
    parser.add_argument(
        "--output", type=str, default="data/htmt_records.csv", help="出力ファイル名"
    )
    args = parser.parse_args()

    generate_growth_data(args.child_id, args.sex, args.output)
