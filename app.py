import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Plant Disease Detection & Chatbot",
    page_icon="🌿",
    layout="centered"
)

# ---------------- API KEY ----------------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Models
vision_model = genai.GenerativeModel("gemini-1.5-flash")
chat_model = genai.GenerativeModel("gemini-pro")

# ---------------- UI ----------------
st.title("🌿 Plant Disease Detection & Agri Chatbot")

tab1, tab2 = st.tabs(["🌱 Plant Disease Detection", "💬 Chat with AgriBot"])

# =====================================================
# 🌱 TAB 1 : PLANT DISEASE DETECTION
# =====================================================
with tab1:
    st.subheader("Upload Plant Leaf Image")

    uploaded_file = st.file_uploader(
        "📷 Upload plant leaf image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Leaf Image", use_container_width=True)

        if st.button("🔍 Analyze Disease"):
            with st.spinner("Analyzing plant leaf... 🌱"):
                prompt = """
                You are an agriculture expert.
                Analyze the given plant leaf image and provide:
                1. Plant name (if possible)
                2. Disease name or Healthy
                3. Symptoms
                4. Causes
                5. Treatment
                6. Prevention methods
                """

                try:
                    response = vision_model.generate_content([prompt, image])
                    st.success("✅ Analysis Completed")
                    st.write("### 🧪 Disease Report")
                    st.write(response.text)
                except Exception as e:
                    st.error("Error while analyzing image")
                    st.write(e)

    else:
        st.info("⬆️ Upload a plant leaf image to analyze")

# =====================================================
# 💬 TAB 2 : AGRICULTURE CHATBOT
# =====================================================
with tab2:
    st.subheader("💬 Chat with AgriBot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Ask about plant diseases, crops, fertilizers...")

    if user_input:
        # Show user message
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )
        with st.chat_message("user"):
            st.write(user_input)

        # Gemini response
        with st.chat_message("assistant"):
            with st.spinner("AgriBot thinking... 🤖🌱"):
                response = chat_model.generate_content(
                    "You are an agriculture expert. Answer clearly.\n" + user_input
                )
                st.write(response.text)

        st.session_state.messages.append(
            {"role": "assistant", "content": response.text}
        )
