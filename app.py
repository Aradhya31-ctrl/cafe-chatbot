import streamlit as st
from data import DOCUMENTS, MENU, HOURS , FAQS
from embedding import EmbeddingRetriever
from generation import RAGAnswerer
from utils import detect_intent, rupee

st.set_page_config(page_title="Cafe RAG Chatbot", page_icon="☕", layout="wide")

# -------------- Styles --------------


# Inject custom CSS
st.markdown("""
<style>
/* ===== App Background ===== */
.stApp {
    background: linear-gradient(135deg, #fbe9e7 0%, #fff3e0 100%);
    font-family: "Segoe UI", sans-serif;
    color: #333;
    padding: 0;
    margin: 0;
}

/* ===== Sidebar ===== */
.css-1d391kg, .stSidebar {
    background-color: #3e2723 !important; /* coffee dark brown */
    color: #f5f5f5 !important;
}
.stSidebar h3, .stSidebar label, .stSidebar span, .stSidebar p {
    color: #f5f5f5 !important;
}

/* ===== Headers ===== */
.title {
    font-size: 40px !important;
    font-weight: 800;
    color: #4e342e; /* strong coffee brown */
    margin-bottom: 8px;
}
.subtitle, .muted {
    font-size: 16px;
    color: #6d4c41;
    margin-bottom: 18px;
}

/* ===== Chat Container ===== */
.chat-container {
    background: #ffffffcc; /* semi-transparent white */
    border-radius: 16px;
    padding: 20px;
    margin-top: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

/* ===== Chat Bubbles ===== */
.bubble-user {
    background: #c8e6c9;
    padding: 12px 15px;
    border-radius: 15px;
    margin: 8px 0;
    font-size: 15px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
.bubble-bot {
    background: #ffe0b2;
    padding: 12px 15px;
    border-radius: 15px;
    margin: 8px 0;
    font-size: 15px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

/* ===== Input & Ask Button Inline ===== */
.stForm {
    display: flex;
    align-items: center;
    gap: 10px; /* space between input and button */
}
.stForm .stTextInput {
    flex: 1; /* input takes max width */
}
.stForm button {
    background-color: #212121 !important;   /* dark background */
    color: #FFFFFF !important;             /* white text */
    border-radius: 10px !important;
    padding: 8px 20px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    border: none !important;
    margin-top: 0 !important; /* align perfectly inline */
    transition: background 0.2s ease, color 0.2s ease;
}


/* ===== Menu Cards ===== */
.menu-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 15px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.08);
}
.pill {
    background: #d7ccc8;
    color: #3e2723;
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 13px;
    font-weight: 600;
}
.tag {
    background: #efebe9;
    border-radius: 8px;
    padding: 3px 7px;
    font-size: 12px;
    margin-right: 5px;
    color: #4e342e;
}

/* ===== Styled Tables (Hours/Menu Output) ===== */
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    font-size: 14px;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
table thead tr {
    background-color: #d7ccc8; /* coffee cream */
    color: #3e2723;
    font-weight: 600;
}
table td, table th {
    padding: 10px;
    text-align: left;
}
table, th, td {
    color: #3e2723 !important;   /* dark coffee brown text */
    font-weight: 600;
}
table tr:nth-child(even) {
    background-color: #fbe9e7;
}
</style>
""", unsafe_allow_html=True)

# -------------- Load models --------------
@st.cache_resource
def get_retriever():
    return EmbeddingRetriever(DOCUMENTS)

@st.cache_resource
def get_answerer():
    return RAGAnswerer()

retriever = get_retriever()
answerer = get_answerer()

# -------------- Sidebar: Preferences --------------
with st.sidebar:
    st.markdown("### Meal Preferences")
    veg_pref = st.selectbox("Vegetarian?", ["No preference","Vegetarian only","Non‑veg only"])
    spicy = st.checkbox("Spicy")
    sweet = st.checkbox("Sweet / Dessert")
    caffeine_free = st.checkbox("Caffeine‑free")
    cold = st.checkbox("Cold drink")
    high_protein = st.checkbox("High protein")
    min_budget = st.number_input("Budget min (INR)", 0, 2000, 0, step=10)
    max_budget = st.number_input("Budget max (INR)", 0, 2000, 1000, step=10)
    st.markdown("---")
    st.markdown("**Hours**")
    for d,t in HOURS.items():
        st.caption(f"{d.title()}: {t}")

# -------------- Header --------------
col1, col2 = st.columns([2,1])
with col1:
    st.markdown("<div class='title'>☕ Café RAG Chatbot</div>", unsafe_allow_html=True)
    st.markdown("<div class='muted'>Answers about hours, menu, prices, and gives meal suggestions.</div>", unsafe_allow_html=True)
with col2:
    st.markdown("")

st.write("")
# -------------- Chat Input --------------
st.markdown("### 💬 Ask me anything about our café")



with st.form("ask"):
    q = st.text_input(
        "", 
        placeholder= " ")
    submit = st.form_submit_button("Ask ➤", use_container_width=False)

    
if "history" not in st.session_state:
    st.session_state.history = []

def filter_menu():
    res = []
    for name, price, tags, desc in MENU:
        if veg_pref == "Vegetarian only" and "vegetarian" not in tags: 
            continue
        if veg_pref == "Non‑veg only" and "non-veg" not in tags:
            continue
        if spicy and "spicy" not in tags: 
            continue
        if sweet and "sweet" not in tags and "dessert" not in tags:
            continue
        if caffeine_free and "caffeine" in tags:
            continue
        if cold and "cold" not in tags:
            continue
        if high_protein and "high-protein" not in tags:
            continue
        if not (min_budget <= price <= max_budget): 
            continue
        res.append((name, price, tags, desc))
    return res

import re
import pandas as pd   # ⬅ add this at the top if not already

def answer_query(q):
    q_lower = q.lower()
    intent = detect_intent(q)

    # Use retrieval (kept as-is)
    retrieved = retriever.retrieve(q, top_k=5)
    contexts = [r["text"] for r in retrieved]
    base_answer = answerer.answer(q, contexts)

    # --- Hours intent ---
    if intent == "hours":
        # Specific day?
        for day in HOURS.keys():
            if day.lower() in q_lower:
                return f"{day.title()}: {HOURS[day]}"
        # Otherwise, whole week
        return "Hours: " + ", ".join(f"{d.title()} {t}" for d, t in HOURS.items())

    # --- Menu intent ---
    if intent == "menu":
        items = filter_menu()[:8]
        if not items:
            return "No items match your current filters. Try adjusting your preferences."
        return "Here are some menu items: " + "; ".join(f"{n} ({rupee(p)})" for n, p, _, _ in items) + "."

    # --- Price intent (fixed indentation/logic) ---
    if intent == "price":
        for name, price, tags, desc in MENU:
            if name.lower() in q_lower:
                return f"{name} — {rupee(price)}."
        return "I couldn’t find that item on the menu."

    # --- Suggest intent ---
    if intent == "suggest":
        items = filter_menu()
        if not items:
            items = [(n, p, t, d) for n, p, t, d in MENU]
        items = sorted(items, key=lambda x: x[1])
        top = items[:3]
        return "My picks for you: " + "; ".join(f"{n} ({rupee(p)})" for n, p, _, _ in top) + "."

    return base_answer



if submit and q.strip():
    q_clean = q.strip()
    ans = answer_query(q_clean)

    # Always show what the user asked
    st.markdown(f"<div class='bubble-user'><b>You:</b> {q_clean}</div>", unsafe_allow_html=True)

    # Decide whether to show a table (full week or single day)
    q_lower = q_clean.lower()
    show_hours_table = False
    df = None

    # Full-week case (answer starts with "Hours:")
    if isinstance(ans, str) and ans.startswith("Hours:"):
        df = pd.DataFrame(list(HOURS.items()), columns=["Day", "Hours"])
        show_hours_table = True
    else:
        # Single-day case: build a one-row table for the day mentioned in the question
        for day in HOURS.keys():
            if day.lower() in q_lower:
                df = pd.DataFrame([[day.title(), HOURS[day]]], columns=["Day", "Hours"])
                show_hours_table = True
                break

    if show_hours_table and df is not None:
        # Show table without numeric index
        st.table(df.set_index("Day"))
    else:
        # For non-hours answers, show the text bubble
        st.markdown(f"<div class='bubble-bot'><b>Bot:</b> {ans}</div>", unsafe_allow_html=True)


st.write("")
st.markdown("---")

# -------------- Menu Panel --------------
st.markdown("#### Menu")
menu = filter_menu()
if not menu:
    st.caption("No items match current filters.")
else:
    cols = st.columns(2)
    for i, (name, price, tags, desc) in enumerate(menu):
        with cols[i%2]:
            st.markdown(f"""
            <div class='menu-card'>
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <div style='font-weight:700;font-size:18px'>{name}</div>
                    <div class='pill'>{rupee(price)}</div>
                </div>
                <div class='muted' style='margin:6px 0 8px'>{desc}</div>
                <div>{' '.join(f"<span class='tag'>{t}</span>" for t in tags)}</div>
            </div>
            """, unsafe_allow_html=True)
           
st.markdown("#### ❓ Frequently Asked Questions")

for faq in FAQS:
    with st.expander(faq["question"]):
         st.write(faq["answer"])
