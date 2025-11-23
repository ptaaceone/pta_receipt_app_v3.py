import streamlit as st

st.set_page_config(page_title="PTA レシート仕分け v3.10", layout="centered")

st.title("PTA レシート自動仕分け（v3.10）")

# セッションステートで残りレシートとセットを保持
if "remaining" not in st.session_state:
    st.session_state["remaining"] = []

if "sets" not in st.session_state:
    st.session_state["sets"] = []

# レシート入力欄
st.subheader("レシート金額を入力")
input_text = st.text_area(
    "空白またはカンマで区切って入力してください",
    value=" ".join([str(x) for x in st.session_state["remaining"]]),
    height=100
)

# リセットボタン（入力欄の下に常に表示）
if st.button("リセット"):
    st.session_state["remaining"] = []
    st.session_state["sets"] = []

# 目標金額入力
target = st.number_input("1セットの目標金額を入力", min_value=1, value=54000)

# 計算ボタン
if st.button("計算する"):
    if not input_text.strip():
        st.warning("レシート金額を入力してください")
    else:
        try:
            cleaned = input_text.replace("、", " ").replace(",", " ")
            parts = [p for p in cleaned.split() if p.strip() != ""]
            receipts = [int(x) for x in parts]
        except:
            st.error("数字として読み取れないデータがあります")
            st.stop()

        st.session_state["remaining"] = receipts.copy()
        st.session_state["sets"] = []

        remaining = st.session_state["remaining"].copy()
        sets = []

        # 自動仕分け
        while remaining:
            remaining.sort(reverse=True)
            current = []
            total = 0
            for r in remaining[:]:
                if total + r <= target:
                    current.append(r)
                    total += r
                    remaining.remove(r)
            if not current:
                n = remaining.pop(0)
                current = [n]
                total = n
            sets.append((current, total))

        st.session_state["sets"] = sets

# セット表示
st.subheader("計算済セット")
for i, (comb, total) in enumerate(list(st.session_state["sets"])):  # コピー使用
    diff = total - target
    if diff == 0:
        comment = "たまるか！"
    elif abs(diff) <= 999:
        comment = "おしいにゃぁ"
    elif abs(diff) >= 33000:
        comment = "どいた？！"
    else:
        comment = "！？"

    st.markdown(f"**セット{i+1}（{len(comb)}枚）**")
    st.write("レシート：" + " ".join([str(x) for x in comb]))
    st.write(f"合計：{total}円 → 差額：{diff:+}円 → {comment}")

    # 仕分け完了ボタン
    btn_key = f"done_{i}"
    if st.button(f"セット{i+1}を仕分け完了", key=btn_key):
        for x in comb:
            if x in st.session_state["remaining"]:
                st.session_state["remaining"].remove(x)
        st.session_state["sets"].remove((comb, total))

# 全合計と残り枚数
st.subheader("残りレシート合計")
st.write(f"全レシート枚数: {len(st.session_state['remaining'])}枚, 合計金額: {sum(st.session_state['remaining'])}円")

