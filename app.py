import os
import pandas as pd
import streamlit as st
from chatbot import build_chatbot, leaked
from attacks import ATTACKS

st.set_page_config(page_title="PromptShield", page_icon="🛡️")
st.title("🛡️ PromptShield")
st.caption(
    "Testing a bank helpdesk chatbot against prompt-injection attacks. "
    "All secrets are fake and used only for this experiment."
)

LEVELS = {
    "1. Naive (no rules)": dict(naive=True),
    "2. With rules": dict(),
    "3. Strict prompt": dict(strict=True),
    "4. Strict prompt + output filter": dict(strict=True, output_filter=True),
}

tab_demo, tab_results = st.tabs(["Live demo", "Results"])

with tab_demo:
    level = st.selectbox("Protection level", list(LEVELS))
    choice = st.selectbox(
        "Sample attack (or choose none and type your own)",
        ["(none)"] + [a["prompt"] for a in ATTACKS],
    )
    msg = st.text_area(
        "Message to the chatbot",
        value="" if choice == "(none)" else choice,
        key=f"msg_{choice}",
    )

    if st.button("Send") and msg.strip():
        with st.spinner("Thinking..."):
            ask = build_chatbot(**LEVELS[level])
            reply = ask(msg)
        st.markdown("**Chatbot reply:**")
        st.write(reply)
        if leaked(reply):
            st.error("Secret LEAKED: this attack succeeded.")
        else:
            st.success("No secret leaked.")

with tab_results:
    if os.path.exists("results_all.csv"):
        df = pd.read_csv("results_all.csv")
        overall = (df.groupby("level").success.mean() * 100).round(0)
        st.subheader("Attack success rate by protection level (%)")
        st.bar_chart(overall)

        st.subheader("By attack category (%)")
        table = df.pivot_table(index="level", columns="category",
                               values="success", aggfunc="mean") * 100
        st.dataframe(table.round(0))

        with st.expander("Raw results (every prompt and reply)"):
            st.dataframe(df[["level", "category", "prompt", "success", "reply"]])
    else:
        st.info("Run `python run_attacks.py` first to generate results_all.csv.")