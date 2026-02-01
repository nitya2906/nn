import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="Plant Disease Detection",
    page_icon="🌿",
    layout="centered"
)

# ------------------ API KEY ------------------
# Streamlit Cloud / Local environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini Vision Model
model = genai.GenerativeModel("gemini-1.5-flash")

# ------------------ UI ------------------
st.title("🌿 Plant Disease Detection System")
st.write(
    "Upload a **plant leaf image** to identify the disease and get "
    "symptoms, causes, and treatment recommendations using **Gemini AI**."
)

uploaded_file = st.file_uploader(
    "📷 Upload plant leaf image",
    type=["jpg", "jpeg", "png"]
)

# ------------------ PROCESS ------------------
if uploaded_file is not None:
    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Leaf Image",
        use_container_width=True
    )

    if st.button("🔍 Analyze Disease"):
        with st.spinner("Analyzing leaf image using AI... 🌱"):
            prompt = """
            You are an agriculture and plant pathology expert.
            Analyze the given plant leaf image and provide:

            1. Plant name (if possible)
            2. Disease name (or say 'Healthy' if no disease)
            3. Visible symptoms
            4. Possible causes
            5. Treatment recommendations
            6. Prevention methods

            Keep the explanation clear and student-friendly.
            """

            try:
                response = model.generate_content([prompt, image])

                st.success("✅ Analysis Completed")

                st.subheader("🧪 Disease Analysis Report")
                st.write(response.text)

            except Exception as e:
                st.error("❌ Error occurred while analyzing the image")
                st.write(e)

else:
    st.info("⬆️ Please upload a plant leaf image to start analysis")
