import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.extractor import extract_text_from_pdf, extract_text_from_txt
from utils.analyzer import analyze_document
from utils.ai_explainer import get_plain_summary, chat_with_document
from utils.nlp_extractor import extract_entities
from utils.risk_scorer import calculate_risk_score

st.set_page_config(
    page_title="RightsAI — Know Before You Sign",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stApp { background-color: #0A0A0A; color: #F0F0F0; }
    .main { background-color: #0A0A0A; max-width: 760px; }
    section[data-testid="stSidebar"] { background-color: #111111; }
    .hero-title { font-size: 2rem; font-weight: 700; color: #FFFFFF; line-height: 1.2; margin-bottom: 8px; }
    .hero-sub { font-size: 1rem; color: #AAAAAA; margin-bottom: 24px; line-height: 1.6; }
    .risk-badge-red { background: #3D1515; color: #FF6B6B; padding: 3px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; }
    .risk-badge-yellow { background: #3D2D0A; color: #FFD166; padding: 3px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; }
    .risk-badge-green { background: #0A2D15; color: #06D6A0; padding: 3px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; }
    .snippet-box { background: #1A1A1A; border-left: 3px solid #FF6B6B; padding: 8px 12px; border-radius: 4px; font-size: 13px; color: #AAAAAA; margin-top: 6px; font-style: italic; }
    div[data-testid="stExpander"] { border: 1px solid #2A2A2A; border-radius: 10px; margin-bottom: 8px; background-color: #111111; }
    div[data-testid="stMetricValue"] { color: #FFFFFF; }
    .score-box { border-radius: 16px; padding: 24px; text-align: center; margin-bottom: 20px; }
    .score-number { font-size: 4rem; font-weight: 800; line-height: 1; }
    .score-label { font-size: 1.1rem; font-weight: 600; margin-top: 8px; }
    .entity-box { background: #1A1A1A; border: 1px solid #2A2A2A; border-radius: 12px; padding: 16px; margin-bottom: 12px; }
    .entity-row { display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #2A2A2A; }
    p, label, span { color: #DDDDDD !important; }
    h1, h2, h3, h4 { color: #FFFFFF !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero-title">⚖️ RightsAI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">Upload any contract, offer letter, or rent agreement.<br>'
    'Know exactly what you\'re signing — in plain language.</div>',
    unsafe_allow_html=True
)
st.divider()

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...", help="Required for AI summary and chat features")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        st.success("API key set ✓")
    st.markdown("---")
    st.markdown("**Supported documents:**")
    st.markdown("- Job offer letters\n- Rent agreements\n- Freelance contracts\n- Loan documents\n- App terms of service")
    st.markdown("---")
    st.caption("🔒 Your document is never stored. Analyzed locally.")

uploaded_file = st.file_uploader("Upload your document", type=["pdf", "txt"], help="PDF or text file supported")

if uploaded_file is None:
    st.markdown("#### 📋 What can RightsAI detect?")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("🔴 **High Risk**")
        st.caption("Non-compete clauses, IP grabs, forced arbitration, auto-renewal traps")
    with col2:
        st.markdown("🟡 **Review Needed**")
        st.caption("Notice period gaps, confidentiality scope, variable pay terms")
    with col3:
        st.markdown("🟢 **Safe**")
        st.caption("Clear salary, defined leave policy, grievance mechanism present")
    st.info("👆 Upload a PDF or TXT file to get your free risk report")
    st.stop()

with st.spinner("Reading your document..."):
    if uploaded_file.type == "application/pdf":
        document_text = extract_text_from_pdf(uploaded_file)
    else:
        document_text = extract_text_from_txt(uploaded_file)

if not document_text or len(document_text) < 50:
    st.error("Could not read document. Please try a different file.")
    st.stop()

st.success(f"✓ Document read — {len(document_text.split())} words analyzed")

with st.spinner("Running AI analysis..."):
    results = analyze_document(document_text)
    risk_score = calculate_risk_score(results)
    entities = extract_entities(document_text)

summary = results["summary"]

# ── Risk Score ──────────────────────────────────────────────────────────────────
st.markdown("### 🎯 Risk Score")

score = risk_score["score"]
color = risk_score["color"]
label = risk_score["label"]
emoji = risk_score["emoji"]

st.markdown(f"""
<div class="score-box" style="background: {color}18; border: 2px solid {color};">
    <div class="score-number" style="color: {color};">{score}<span style="font-size:1.5rem;">/100</span></div>
    <div class="score-label" style="color: {color};">{emoji} {label}</div>
</div>
""", unsafe_allow_html=True)

# Progress bar
st.progress(score / 100)

# ── Stats Row ───────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🔴 High Risk", summary["total_red"])
with col2:
    st.metric("🟡 Review", summary["total_yellow"])
with col3:
    st.metric("🟢 Safe", summary["total_green"])

st.divider()

# ── NLP Entity Extraction ───────────────────────────────────────────────────────
st.markdown("### 🔍 Key Information Extracted")
st.caption("Automatically pulled from your document using NLP")

ecol1, ecol2 = st.columns(2)

with ecol1:
    st.markdown("**📌 Company**")
    st.info(entities["company_name"] if entities["company_name"] else "Not detected")

    st.markdown("**💰 Salary**")
    st.info(entities["salary"] if entities["salary"] else "Not detected")

    st.markdown("**⏰ Notice Period**")
    st.info(entities["notice_period"] if entities["notice_period"] else "Not detected")

with ecol2:
    st.markdown("**🕐 Probation Period**")
    st.info(entities["probation_period"] if entities["probation_period"] else "Not detected")

    st.markdown("**📅 Dates Mentioned**")
    st.info(", ".join(entities["dates"]) if entities["dates"] else "Not detected")

    st.markdown("**📍 Locations**")
    st.info(", ".join(entities["locations"]) if entities["locations"] else "Not detected")

st.divider()

# ── Detailed Flags ──────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["🔴 High Risk", "🟡 Review Needed", "🟢 Safe Clauses", "💬 Ask Anything"])

with tab1:
    if not results["red"]:
        st.success("No high-risk clauses found. 👍")
    for item in results["red"]:
        with st.expander(f"🔴 {item['clause']}"):
            st.markdown(f'<span class="risk-badge-red">High Risk</span>', unsafe_allow_html=True)
            st.markdown(f"**Keywords found:** `{'`, `'.join(item['keywords_found'])}`")
            if item["snippet"]:
                st.markdown(f'<div class="snippet-box">{item["snippet"]}</div>', unsafe_allow_html=True)

with tab2:
    if not results["yellow"]:
        st.success("No clauses needing review. 👍")
    for item in results["yellow"]:
        with st.expander(f"🟡 {item['clause']}"):
            st.markdown(f'<span class="risk-badge-yellow">Review Needed</span>', unsafe_allow_html=True)
            st.markdown(f"**Keywords found:** `{'`, `'.join(item['keywords_found'])}`")
            if item["snippet"]:
                st.markdown(f'<div class="snippet-box">{item["snippet"]}</div>', unsafe_allow_html=True)

with tab3:
    if not results["green"]:
        st.info("No explicitly safe/protective clauses detected.")
    for item in results["green"]:
        with st.expander(f"🟢 {item['clause']}"):
            st.markdown(f'<span class="risk-badge-green">Safe</span>', unsafe_allow_html=True)
            st.markdown(f"**Keywords found:** `{'`, `'.join(item['keywords_found'])}`")

with tab4:
    st.markdown("#### 💬 Ask anything about this document")
    st.caption("Powered by GPT — works best with an API key in the sidebar")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    st.markdown("**Quick questions:**")
    qcol1, qcol2 = st.columns(2)
    with qcol1:
        if st.button("Can they fire me without notice?"):
            st.session_state.pending_question = "Can they fire me without notice based on this document?"
    with qcol2:
        if st.button("Do I own my side projects?"):
            st.session_state.pending_question = "Based on this document, do I own my personal side projects?"
    qcol3, qcol4 = st.columns(2)
    with qcol3:
        if st.button("What happens if I break this?"):
            st.session_state.pending_question = "What are the consequences if I break this agreement?"
    with qcol4:
        if st.button("Is this rent agreement fair?"):
            st.session_state.pending_question = "Is this rent agreement fair to me as a tenant?"

    user_input = st.chat_input("Ask about your document...")
    question_to_ask = user_input or st.session_state.get("pending_question")
    if "pending_question" in st.session_state:
        del st.session_state.pending_question

    if question_to_ask:
        st.chat_message("user").write(question_to_ask)
        with st.spinner("Thinking..."):
            answer = chat_with_document(document_text, question_to_ask, st.session_state.chat_history)
        st.chat_message("assistant").write(answer)
        st.session_state.chat_history.append({"role": "user", "content": question_to_ask})
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

st.divider()
st.markdown("### 📝 Plain Language Summary")

if not os.getenv("OPENAI_API_KEY"):
    st.info("Add your OpenAI API key in the sidebar to get a plain language summary.")
else:
    if "ai_summary" not in st.session_state:
        with st.spinner("Generating plain language summary..."):
            st.session_state.ai_summary = get_plain_summary(document_text, results)
    st.markdown(st.session_state.ai_summary)

st.divider()
st.caption("⚖️ RightsAI — For informational purposes only. Not a substitute for professional legal advice.")
st.caption("🔒 Your documents are never stored or shared.")