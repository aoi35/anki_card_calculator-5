import tkinter as tk
from tkinter import ttk, messagebox

# ======================
# 計算関数
# ======================
def calculate():
    try:
        # 入力時間を小数に変換
        h_input, m_input = map(int, input_time_var.get().split(":"))
        input_hours = h_input + m_input / 60

        h_anki, m_anki = map(int, anki_time_var.get().split(":"))
        anki_hours = h_anki + m_anki / 60
    except:
        messagebox.showerror("Error", "Invalid time format. Example: 1:30")
        return

    try:
        input_part, anki_part = map(float, ratio_var.get().split(":"))
        ideal_ratio = anki_part / (input_part + anki_part)
    except:
        messagebox.showerror("Error", "Invalid ratio format. Example: 4:1")
        return

    total_cards = total_cards_var.get()
    due_cards = due_cards_var.get()
    factor = factor_var.get()

    # 計算ロジック
    actual_ratio = anki_hours / (input_hours + anki_hours)
    if abs(actual_ratio - ideal_ratio) < 0.01:
        new_cards = total_cards - due_cards
    else:
        sec_per_card = (anki_hours*3600)/total_cards
        ideal_anki_seconds = input_hours*3600*ideal_ratio
        new_cards = int(ideal_anki_seconds / sec_per_card - due_cards)

    adjusted_cards = max(0, round(new_cards / factor))

    # 結果表示（縦並び）
    result_label.config(text=f"✅ Recommended number of new cards (factor {factor}): {adjusted_cards}\n"
                             f"✅ 推奨新規カード枚数 (係数 {factor} で調整後): {adjusted_cards}")

    # 補足メッセージ（st.info に相当）
    info_label.config(text="※ 推奨値は目安です。学習ペースに合わせて調整してください。")

# ======================
# GUI 設定
# ======================
root = tk.Tk()
root.title("New Card Limit Calculator / 新規カード上限計算")
root.geometry("450x450")

# 入力ラベルとエントリー
input_time_var = tk.StringVar(value="1:00")
anki_time_var = tk.StringVar(value="0:15")
ratio_var = tk.StringVar(value="4:1")
total_cards_var = tk.IntVar(value=20)
due_cards_var = tk.IntVar(value=8)
factor_var = tk.IntVar(value=4)

ttk.Label(root, text="昨日Inputに使った時間 / Yesterday's Input time (例: 1:00)").pack(pady=2)
ttk.Entry(root, textvariable=input_time_var).pack(pady=2)

ttk.Label(root, text="昨日暗記カードにかかった時間 / Yesterday's Anki time (例: 0:15)").pack(pady=2)
ttk.Entry(root, textvariable=anki_time_var).pack(pady=2)

ttk.Label(root, text="理想のInput:暗記カードの比率 / The ideal input:Anki ratio (例: 4:1)").pack(pady=2)
ttk.Entry(root, textvariable=ratio_var).pack(pady=2)

ttk.Label(root, text="昨日の総レビュー枚数 / Total cards reviewed yesterday").pack(pady=2)
ttk.Entry(root, textvariable=total_cards_var).pack(pady=2)

ttk.Label(root, text="今日が期限のカード枚数 / Cards due today").pack(pady=2)
ttk.Entry(root, textvariable=due_cards_var).pack(pady=2)

ttk.Label(root, text="⚠ 新規カード労力係数 / ⚠ Effort Multiplier for New Cards").pack(pady=2)
ttk.Entry(root, textvariable=factor_var).pack(pady=2)
ttk.Label(root, text="デフォルトは4。通常は触らないことを推奨。").pack(pady=2)

# 計算ボタン
ttk.Button(root, text="Calculate / 計算", command=calculate).pack(pady=10)

# 結果表示ラベル
result_label = ttk.Label(root, text="", justify="left")
result_label.pack(pady=10)

# 補足メッセージラベル
info_label = ttk.Label(root, text="", justify="left", foreground="blue")
info_label.pack(pady=5)

root.mainloop()
