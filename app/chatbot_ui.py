"""IT Helpdesk Chatbot UI — Streamlit frontend for the FastAPI backend."""
from __future__ import annotations

import uuid

import httpx
import streamlit as st

API_URL = "http://localhost:8000"

st.set_page_config(page_title="IT Helpdesk", page_icon="🖥️", layout="centered")
st.title("🖥️ IT Helpdesk Assistant")
st.caption("Ask me anything about passwords, VPN, laptop, email, access, server, network, software, or backup.")

# ── Session state ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = f"s-{uuid.uuid4().hex[:8]}"
if "user_id" not in st.session_state:
    st.session_state.user_id = f"u-{uuid.uuid4().hex[:8]}"

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    feature = st.selectbox("Feature", ["qa", "summary"], index=0)
    user_id = st.text_input("User ID", value=st.session_state.user_id)
    st.caption(f"Session: `{st.session_state.session_id}`")

    st.divider()
    st.header("🚨 Inject Incident")
    col1, col2 = st.columns(2)
    for scenario in ["rag_slow", "tool_fail", "cost_spike"]:
        with col1:
            if st.button(f"▶ {scenario}", key=f"en_{scenario}", use_container_width=True):
                httpx.post(f"{API_URL}/incidents/{scenario}/enable", timeout=5)
                st.toast(f"{scenario} enabled", icon="🔴")
        with col2:
            if st.button(f"■ stop", key=f"dis_{scenario}", use_container_width=True):
                httpx.post(f"{API_URL}/incidents/{scenario}/disable", timeout=5)
                st.toast(f"{scenario} disabled", icon="🟢")

    st.divider()
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = f"s-{uuid.uuid4().hex[:8]}"
        st.rerun()

# ── Chat history ───────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "meta" in msg:
            m = msg["meta"]
            st.caption(
                f"⏱ {m['latency_ms']}ms · "
                f"🪙 {m['tokens_in']}↑ {m['tokens_out']}↓ tokens · "
                f"💰 ${m['cost_usd']:.6f} · "
                f"⭐ quality {m['quality_score']:.2f} · "
                f"🔗 `{m['correlation_id']}`"
            )

# ── Input ──────────────────────────────────────────────────────────────────────
if prompt := st.chat_input("e.g. How do I reset my password?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                resp = httpx.post(
                    f"{API_URL}/chat",
                    json={
                        "user_id": user_id,
                        "session_id": st.session_state.session_id,
                        "feature": feature,
                        "message": prompt,
                    },
                    timeout=30.0,
                )
                resp.raise_for_status()
                data = resp.json()
                answer = data["answer"]
                st.markdown(answer)
                st.caption(
                    f"⏱ {data['latency_ms']}ms · "
                    f"🪙 {data['tokens_in']}↑ {data['tokens_out']}↓ tokens · "
                    f"💰 ${data['cost_usd']:.6f} · "
                    f"⭐ quality {data['quality_score']:.2f} · "
                    f"🔗 `{data['correlation_id']}`"
                )
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "meta": data,
                })
            except httpx.ConnectError:
                err = "❌ Cannot connect to backend. Make sure `uvicorn app.main:app --reload` is running."
                st.error(err)
                st.session_state.messages.append({"role": "assistant", "content": err})
            except Exception as e:
                err = f"❌ Error: {e}"
                st.error(err)
                st.session_state.messages.append({"role": "assistant", "content": err})
