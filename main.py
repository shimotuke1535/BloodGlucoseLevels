import csv
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

CSV_FILE = "glucose_log.csv"
GRAPH_FILE_ALL = "glucose_graph_all.png"
GRAPH_FILE_WEEK = "glucose_graph_week.png"

def ensure_csv_header():
    if not os.path.isfile(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Datetime", "Glucose(mg/dl)", "HbA1c(%)"])

def log_glucose(glucose_value):
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d %H:%M:%S')
    ensure_csv_header()
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([date_str, glucose_value, ""])

def log_HbA1c(glucose_value, HbA1c_value):
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d %H:%M:%S')
    ensure_csv_header()
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([date_str, glucose_value, HbA1c_value])

def read_logs():
    logs = []
    if os.path.isfile(CSV_FILE):
        with open(CSV_FILE, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for row in reader:
                if len(row) >= 2 and row[1]:
                    try:
                        dt = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                        glucose = int(row[1])
                        HbA1c = float(row[2]) if len(row) > 2 and row[2] else None
                        logs.append((dt, glucose, HbA1c))
                    except ValueError:
                        continue
    return logs

def plot_graph(logs, filename, title_suffix=""):
    if not logs:
        print("ログがありません")
        return

    dates = [row[0] for row in logs]
    glucose_values = [row[1] for row in logs]
    hba1c_values = [row[2] for row in logs]

    fig, ax1 = plt.subplots(figsize=(10, 5))

    # 血糖値プロット（左軸）
    ax1.plot(dates, glucose_values, marker='o', linestyle='-', color='blue', label='Glucose (mg/dl)')
    ax1.set_xlabel('Datetime')
    ax1.set_ylabel('Glucose (mg/dl)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.grid(True)

    # HbA1cプロット（右軸、Noneはプロットしない）
    if any(hba1c is not None for hba1c in hba1c_values):
        ax2 = ax1.twinx()
        hba1c_dates = [d for d, h in zip(dates, hba1c_values) if h is not None]
        hba1c_points = [h for h in hba1c_values if h is not None]
        ax2.plot(hba1c_dates, hba1c_points, marker='s', linestyle='-', color='red', label='HbA1c (%)')
        ax2.set_ylabel('HbA1c (%)', color='red')
        ax2.tick_params(axis='y', labelcolor='red')

    plt.title(f'Blood Glucose and HbA1c Over Time{title_suffix}')
    fig.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"グラフ画像を「{filename}」として保存しました。")

def plot_all_and_weekly_graphs(logs):
    # 全データ
    plot_graph(logs, GRAPH_FILE_ALL, "")
    # 直近1週間
    one_week_ago = datetime.now() - timedelta(days=7)
    week_logs = [row for row in logs if row[0] >= one_week_ago]
    plot_graph(week_logs, GRAPH_FILE_WEEK, " (Last 7 days)")

def main():
    print("モードを選んでください:")
    print("1: 血糖値を新規入力して記録＆グラフ更新")
    print("2: 血糖値&HbA1cを新規入力して記録&グラフ更新")
    print("3: グラフだけを更新（CSVの内容を再描画）")
    mode = input("番号を入力してください（1~3）: ")

    if mode == "1":
        try:
            glucose_value = int(input("血糖値を入力してください（mg/dl）: "))
            log_glucose(glucose_value)
            logs = read_logs()
            plot_all_and_weekly_graphs(logs)
            print("記録しました。")
        except ValueError:
            print("整数で入力してください。")
    elif mode == "2":
        try:
            glucose_value = int(input("血糖値を入力してください（mg/dl）: "))
            HbA1c_value = float(input("HbA1cを入力してください（%）: "))
            log_HbA1c(glucose_value, HbA1c_value)
            logs = read_logs()
            plot_all_and_weekly_graphs(logs)
            print("記録しました。")
        except ValueError:
            print("正しい値を入力してください。")
    elif mode == "3":
        logs = read_logs()
        plot_all_and_weekly_graphs(logs)
    else:
        print("無効な選択です。")

if __name__ == "__main__":
    main()
    input("終了するにはEnterキーを押してください。")