import streamlit as st  # Streamlit for UI
import base64  # For encoding image
import os  # For file checks

from Emotion_detection_analysis import detect_emotions  # Import emotion analysis function
from topic_analysis import extract_topics_and_subtopics  # Import topic analysis function
from scoring import calculate_adorescore  # Import Adorescore calculation

# Function to set background image using Base64
def set_background(image_path):
    if not os.path.exists(image_path):
        st.warning("⚠️ Background image not found! Skipping background setup.")
        return
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        page_bg_img = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded_string}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading background image: {str(e)}")

# Call function with correct image path
set_background("C:\\Users\\aarth\\OneDrive\\Desktop\\Customer_emotion_analysis\\emoji-meaning.jpg")

# Streamlit App UI - Title in Black and Bold
st.markdown(
    "<h1 style='text-align: center; color: black; font-weight: bold;'>🎭 Customer Emotion Analysis System</h1>",
    unsafe_allow_html=True
)

# User selects the analysis type (Bold and Black)
st.markdown(
    "<h2 style='color: black; font-weight: bold;'>🛠 Choose an Analysis Type:</h2>",
    unsafe_allow_html=True
)
option = st.radio(
    "**Select an option:**",  # Bold text
    ["Emotion Detection Engine", "Topic Analysis System", "Adorescore Calculation"]
)

# Emotion Detection
if option == "Emotion Detection Engine":
    st.markdown("**Enter customer feedback for emotion detection:**", unsafe_allow_html=True)
    text = st.text_area("**Enter customer feedback**", "")

    if st.button("Analyze Emotions", key="emotion"):
        if text.strip():
            emotion_result = detect_emotions(text)
            st.markdown("<h3 style='color: black; font-weight: bold;'>🔍 Emotion Analysis Result:</h3>", unsafe_allow_html=True)
            for emo in emotion_result:
                st.markdown(f"**🔹{emo['emotion'].capitalize()}** → Confidence: {emo['intensity']}, Activation: {emo['activation']}", unsafe_allow_html=True)
        else:
            st.warning("⚠️ **Please enter some feedback to analyze.**")

# Topic Analysis
elif option == "Topic Analysis System":
    st.markdown("**Enter customer feedback for topic analysis:**", unsafe_allow_html=True)
    text = st.text_area("**Enter customer feedback**", "")

    if st.button("Analyze Topics", key="topic"):
        if text.strip():
            topic_result = extract_topics_and_subtopics(text)
            st.markdown("<h3 style='color: black; font-weight: bold;'>📌 Extracted Topics and Subtopics:</h3>", unsafe_allow_html=True)
            main_topics = topic_result["topics"]["main"]
            subtopics = topic_result["topics"]["subtopics"]
            st.markdown(f"**Main Topics:** {', '.join(main_topics) if main_topics else 'None'}", unsafe_allow_html=True)
            if subtopics:
                for topic, sub_list in subtopics.items():
                    st.markdown(f"**{topic}**: {', '.join(sub_list)}", unsafe_allow_html=True)
        else:
            st.warning("⚠️ **Please enter some feedback to analyze.**")

# Adorescore Calculation
elif option == "Adorescore Calculation":
    st.markdown("**Enter customer feedback for Adorescore calculation:**", unsafe_allow_html=True)
    text = st.text_area("**Enter customer feedback**", "")

    if st.button("Calculate Adorescore", key="adorescore"):
        if text.strip():
            adorescore_result = calculate_adorescore(text)
            st.markdown("<h3 style='color: black; font-weight: bold;'>📊 Adorescore Calculation Result:</h3>", unsafe_allow_html=True)
            st.markdown(f"**Overall Adorescore:** {adorescore_result['Adorescore']['overall']}", unsafe_allow_html=True)
            st.markdown("<h3 style='color: black; font-weight: bold;'>📌 Adorescore Breakdown by Topic:</h3>", unsafe_allow_html=True)
            for topic, score in adorescore_result["Adorescore"]["breakdown"].items():
                st.markdown(f"**🔹{topic}** → Adorescore: {score}", unsafe_allow_html=True)
        else:
            st.warning("⚠️ **Please enter some feedback to analyze.**")
