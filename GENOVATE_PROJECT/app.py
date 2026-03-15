import streamlit as st
from groq import Groq
from PIL import Image
import os
import base64
from dotenv import load_dotenv
from io import BytesIO
from datetime import datetime

# ── Load API Key ──────────────────────────────────────────────────────────────
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ProPushty",
    page_icon="🍳",
    layout="centered"
)

# ── Session State for History ─────────────────────────────────────────────────
if "food_history" not in st.session_state:
    st.session_state.food_history = []

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&family=Bebas+Neue&display=swap');

:root {
    --yellow: #F5F17A;
    --yellow-dark: #E8E84A;
    --yellow-light: #FAFAB0;
    --green-btn: #6DBE7A;
    --green-btn-hover: #4DA85C;
    --cream: #FFFFF0;
    --charcoal: #1E1E1E;
    --white: #FFFFFF;
    --gold: #C8A830;
    --green: #3A7D44;
    --red: #C0392B;
    --card-shadow: 0 8px 32px rgba(0,0,0,0.10);
}

html, body, [class*="stApp"], [class*="css"] {
    background-color: var(--yellow) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--charcoal);
}

[class*="stApp"]::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='600' height='600'%3E%3Cpath d='M0,300 Q150,200 300,300 T600,300' fill='none' stroke='rgba(0,0,0,0.04)' stroke-width='2'/%3E%3Cpath d='M0,250 Q150,150 300,250 T600,250' fill='none' stroke='rgba(0,0,0,0.04)' stroke-width='2'/%3E%3Cpath d='M0,350 Q150,250 300,350 T600,350' fill='none' stroke='rgba(0,0,0,0.04)' stroke-width='2'/%3E%3Cpath d='M0,200 Q150,100 300,200 T600,200' fill='none' stroke='rgba(0,0,0,0.03)' stroke-width='2'/%3E%3Cpath d='M0,400 Q150,300 300,400 T600,400' fill='none' stroke='rgba(0,0,0,0.03)' stroke-width='2'/%3E%3Cpath d='M0,150 Q150,50 300,150 T600,150' fill='none' stroke='rgba(0,0,0,0.02)' stroke-width='1.5'/%3E%3Cpath d='M0,450 Q150,350 300,450 T600,450' fill='none' stroke='rgba(0,0,0,0.02)' stroke-width='1.5'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
}

.block-container {
    background: transparent !important;
    padding-top: 2rem !important;
}

.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 5rem;
    color: var(--charcoal);
    text-align: center;
    line-height: 1.0;
    margin-bottom: 0.1rem;
    letter-spacing: 0.08em;
    text-shadow: 3px 3px 0px rgba(0,0,0,0.08);
}
.hero-title span {
    color: var(--green);
}
.hero-sub {
    text-align: center;
    font-size: 1.05rem;
    color: rgba(30,30,30,0.7);
    font-weight: 300;
    margin-bottom: 2rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.organic-badge {
    display: flex;
    justify-content: center;
    margin-bottom: 1.5rem;
}
.organic-badge-inner {
    background: var(--green);
    color: white;
    border-radius: 50px;
    padding: 6px 20px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

.spice-divider {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 1.5rem 0;
}
.spice-divider hr {
    flex: 1;
    border: none;
    border-top: 1.5px solid rgba(0,0,0,0.15);
}
.spice-divider span {
    color: var(--charcoal);
    font-size: 1.1rem;
}

.info-card {
    background: var(--white);
    border-radius: 20px;
    padding: 1.5rem 1.8rem;
    box-shadow: var(--card-shadow);
    margin-bottom: 1.2rem;
    border-left: 6px solid var(--green-btn);
    border-top: 1px solid rgba(255,255,255,0.9);
}
.info-card h3 {
    font-family: 'Playfair Display', serif;
    color: var(--green);
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
}
.info-card div {
    color: #2a2a2a;
    line-height: 1.7;
}

.digest-card {
    background: #f0faf2;
    border-radius: 20px;
    padding: 1.5rem 1.8rem;
    box-shadow: var(--card-shadow);
    margin-bottom: 1.2rem;
    border-left: 6px solid var(--green);
}
.digest-card h3 {
    font-family: 'Playfair Display', serif;
    color: var(--green);
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
}

.history-card {
    background: var(--white);
    border-radius: 14px;
    padding: 1rem 1.4rem;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    margin-bottom: 0.8rem;
    border-left: 5px solid var(--gold);
}

.health-good {
    background: #e8f5e9;
    border-radius: 14px;
    padding: 1rem 1.4rem;
    border-left: 5px solid var(--green);
    margin-bottom: 1rem;
    font-weight: 500;
    color: var(--green);
}
.health-bad {
    background: #fdecea;
    border-radius: 14px;
    padding: 1rem 1.4rem;
    border-left: 5px solid var(--red);
    margin-bottom: 1rem;
    font-weight: 500;
    color: var(--red);
}

.badge {
    display: inline-block;
    background: var(--green-btn);
    color: white;
    border-radius: 20px;
    padding: 4px 16px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

div.stButton > button {
    background: var(--green-btn) !important;
    color: white !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2.2rem !important;
    width: 100%;
    transition: all 0.2s ease;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
div.stButton > button:hover {
    background: var(--green-btn-hover) !important;
    transform: translateY(-1px);
}

section[data-testid="stFileUploadDropzone"] {
    background: rgba(255,255,255,0.85) !important;
    border: 2.5px dashed var(--green-btn) !important;
    border-radius: 20px !important;
}

div[data-testid="stTabs"] button {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    color: rgba(30,30,30,0.6) !important;
    background: transparent !important;
    border-bottom: 3px solid transparent !important;
    letter-spacing: 0.05em;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--charcoal) !important;
    border-bottom: 3px solid var(--green) !important;
}

div[data-testid="stInfo"] {
    background: rgba(255,255,255,0.85) !important;
    border: none !important;
    border-radius: 14px !important;
    color: var(--charcoal) !important;
}

.footer {
    text-align: center;
    color: rgba(30,30,30,0.5);
    font-size: 0.82rem;
    margin-top: 3rem;
    padding-bottom: 1.5rem;
    letter-spacing: 0.05em;
}

.arrows {
    color: rgba(30,30,30,0.3);
    font-size: 1.5rem;
    text-align: center;
    letter-spacing: 4px;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# ── Helper: convert image to base64 ──────────────────────────────────────────
def image_to_base64(img: Image.Image) -> str:
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

# ── Prompts ───────────────────────────────────────────────────────────────────
ANALYSIS_PROMPT = """
You are an expert nutritionist and culinary chef. Analyze the food image provided and give a detailed, structured response with these exact sections:

## 🥗 Identified Ingredients
List all visible food items and ingredients you can identify in the image.

## 📊 Nutritional Information
Provide estimated nutritional breakdown per serving:
- Calories
- Protein
- Carbohydrates
- Fats
- Fiber
- Key vitamins & minerals

## 👨‍🍳 Step-by-Step Recipe
Give a clear, easy-to-follow recipe using the identified ingredients. Include:
- Prep time & cook time
- Ingredients list with quantities
- Numbered cooking steps

## 💡 Health Tips
Share 2-3 quick health insights or tips about this meal.

## 🌿 Digestion Suggestions
Based on the food identified, give specific post-meal digestion tips. For example:
- How much water to drink and when
- Any specific drinks like jeera water, fennel tea, buttermilk etc.
- Light activities like walking
- Foods or drinks to avoid right after
- Any specific tips based on the heaviness of the meal

## 🏷️ Food Name
Just write the name of the main dish or food item identified. Just the name, nothing else.

## ✅ Healthy or Not
Just answer: HEALTHY or UNHEALTHY. Then in one line explain why.

Be specific, helpful, and encouraging. Format nicely with emojis.
"""

HISTORY_PROMPT = """
You are a nutrition expert. Based on the following food history of a person, analyze their overall eating habits and give a health report.

Food History:
{history}

Give a structured response with:

## 📈 Overall Health Score
Give a score out of 10 and a one-line summary.

## 🔍 Eating Pattern Analysis
Analyze if they are eating healthy, balanced, or unhealthy. Mention patterns you notice.

## ⚠️ Concerns
List any nutritional concerns or unhealthy patterns.

## ✅ What They Are Doing Well
List the positives in their diet.

## 🎯 Recommendations
Give 3-5 specific, actionable diet recommendations for this person based on their history.

Be encouraging, specific, and helpful.
"""

# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">PRO<span>PUSHTY</span></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">✦ AI-Powered Food & Nutrition Companion ✦</div>', unsafe_allow_html=True)
st.markdown('<div class="organic-badge"><div class="organic-badge-inner">🌿 100% Smart Nutrition Analysis</div></div>', unsafe_allow_html=True)
st.markdown('<div class="arrows">&rsaquo;&rsaquo;&rsaquo;</div>', unsafe_allow_html=True)
st.markdown('<div class="spice-divider"><hr><span>✦</span><hr></div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📸  Analyze Food", "📋  My Food History"])

# ════════════════════════════════════════════════════════════
# TAB 1 — Analyze Food
# ════════════════════════════════════════════════════════════
with tab1:
    uploaded_file = st.file_uploader(
        "📸 Drop your food photo here",
        type=["jpg", "jpeg", "png"],
        help="Supports JPG, JPEG, PNG"
    )

    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption="Let's analyze this dish...", use_column_width=True)
        st.markdown("")
        analyze = st.button("✨ Analyze My Food")

        if analyze:
            with st.spinner("ProPushty is working its magic..."):
                try:
                    img_base64 = image_to_base64(img)

                    response = client.chat.completions.create(
                        model="meta-llama/llama-4-scout-17b-16e-instruct",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "image_url",
                                        "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}
                                    },
                                    {"type": "text", "text": ANALYSIS_PROMPT}
                                ]
                            }
                        ],
                        max_tokens=2000
                    )

                    result = response.choices[0].message.content

                    food_name = "Unknown Food"
                    is_healthy = "Unknown"
                    for section in result.split("##"):
                        section = section.strip()
                        if section.startswith("🏷️ Food Name"):
                            lines = section.split("\n", 1)
                            if len(lines) > 1:
                                food_name = lines[1].strip()
                        if section.startswith("✅ Healthy or Not"):
                            lines = section.split("\n", 1)
                            if len(lines) > 1:
                                is_healthy = lines[1].strip()

                    st.session_state.food_history.append({
                        "food": food_name,
                        "healthy": is_healthy,
                        "time": datetime.now().strftime("%d %b %Y, %I:%M %p")
                    })

                    st.markdown('<div class="spice-divider"><hr><span>✦</span><hr></div>', unsafe_allow_html=True)
                    st.markdown('<div class="badge">✦ Analysis Complete</div>', unsafe_allow_html=True)

                    sections = result.split("##")
                    for section in sections:
                        section = section.strip()
                        if not section:
                            continue
                        lines = section.split("\n", 1)
                        title = lines[0].strip()
                        body = lines[1].strip() if len(lines) > 1 else ""

                        if "🏷️" in title:
                            continue
                        elif "🌿" in title:
                            st.markdown(f"""
                            <div class="digest-card">
                                <h3>{title}</h3>
                                <div>{body}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        elif "✅ Healthy" in title:
                            css_class = "health-good" if "UNHEALTHY" not in body.upper() else "health-bad"
                            st.markdown(f"""
                            <div class="{css_class}">
                                <strong>{title}</strong><br>{body}
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div class="info-card">
                                <h3>{title}</h3>
                                <div>{body}</div>
                            </div>
                            """, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Something went wrong: {e}")
    else:
        st.info("👆 Upload a food image above to get started!")

# ════════════════════════════════════════════════════════════
# TAB 2 — Food History
# ════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### 🗓️ Your Food Log")

    if len(st.session_state.food_history) == 0:
        st.info("No food analyzed yet! Go to the **Analyze Food** tab and upload a photo.")
    else:
        for entry in reversed(st.session_state.food_history):
            is_good = "UNHEALTHY" not in entry['healthy'].upper()
            emoji = "✅" if is_good else "❌"
            st.markdown(f"""
            <div class="history-card">
                <strong>{emoji} {entry['food']}</strong><br>
                <span style="color:#888; font-size:0.85rem;">🕐 {entry['time']}</span><br>
                <span style="font-size:0.9rem; margin-top:4px; display:block; color:#2a2a2a;">{entry['healthy']}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="spice-divider"><hr><span>✦</span><hr></div>', unsafe_allow_html=True)

        if st.button("🔍 Generate My Health Report"):
            with st.spinner("Analyzing your eating habits..."):
                try:
                    history_text = "\n".join([
                        f"- {e['food']} ({e['time']}): {e['healthy']}"
                        for e in st.session_state.food_history
                    ])
                    report_response = client.chat.completions.create(
                        model="meta-llama/llama-4-scout-17b-16e-instruct",
                        messages=[{"role": "user", "content": HISTORY_PROMPT.format(history=history_text)}],
                        max_tokens=1500
                    )
                    report = report_response.choices[0].message.content
                    st.markdown('<div class="badge">✦ Health Report</div>', unsafe_allow_html=True)
                    for section in report.split("##"):
                        section = section.strip()
                        if not section:
                            continue
                        lines = section.split("\n", 1)
                        title = lines[0].strip()
                        body = lines[1].strip() if len(lines) > 1 else ""
                        st.markdown(f"""
                        <div class="info-card">
                            <h3>{title}</h3>
                            <div>{body}</div>
                        </div>
                        """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

        if st.button("🗑️ Clear History"):
            st.session_state.food_history = []
            st.rerun()

st.markdown('<div class="footer">Built with ❤️ for Genovate &nbsp;·&nbsp; Powered by Groq + LLaMA 4</div>', unsafe_allow_html=True)