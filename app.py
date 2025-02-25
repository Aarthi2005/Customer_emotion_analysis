import streamlit as st  # Streamlit for UI
import base64  # For encoding image

from Emotion_detection_analysis import detect_emotions  # Import emotion analysis function
from topic_analysis import extract_topics_and_subtopics  # Import topic analysis function
from scoring import calculate_adorescore  # Import Adorescore calculation

# Function to set background image using Base64
def set_background(image_path):
    """
    Adds a background image to the Streamlit app using Base64 encoding.
    """
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

    /* Make all text black and bold */
    h1, h2, h3, h4, h5, h6, p, label, div, span {{
        color: #000000 !important;  /* Black */
        font-weight: bold !important;  /* Bold */
    }}

    /* Style for red Analyze button */
    .analyze-button {{
        background-color: red !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: bold !important;
        padding: 10px 24px !important;
        border: none !important;
        border-radius: 5px !important;
        cursor: pointer !important;
        display: inline-block !important;
        width: 100% !important;
        text-align: center !important;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Call the function with the correct image path
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

# Function to create a red button
def red_button(label):
    return st.markdown(f'<button class="analyze-button">{label}</button>', unsafe_allow_html=True)

# Emotion Detection
if option == "Emotion Detection Engine":
    st.markdown("**Enter customer feedback for emotion detection:**", unsafe_allow_html=True)
    text = st.text_area("**Enter customer feedback**", "")

    if st.markdown('<button class="analyze-button">Analyze Emotions</button>', unsafe_allow_html=True):
        if text.strip():
            emotion_result = detect_emotions(text)

            # Display Emotion Analysis Results in Black and Bold
            st.markdown(
                "<h3 style='color: black; font-weight: bold;'>🔍 Emotion Analysis Result:</h3>",
                unsafe_allow_html=True
            )
            for emo in emotion_result:
                st.markdown(f"**🔹{emo['emotion'].capitalize()}** → Confidence: {emo['intensity']}, Activation: {emo['activation']}", unsafe_allow_html=True)
        else:
            st.warning("⚠️ **Please enter some feedback to analyze.**")

# Topic Analysis
elif option == "Topic Analysis System":
    st.markdown("**Enter customer feedback for topic analysis:**", unsafe_allow_html=True)
    text = st.text_area("**Enter customer feedback**", "")

    if st.markdown('<button class="analyze-button">Analyze Topics</button>', unsafe_allow_html=True):
        if text.strip():
            topic_result = extract_topics_and_subtopics(text)

            # Display Topic Extraction Results in Black and Bold
            st.markdown(
                "<h3 style='color: black; font-weight: bold;'>📌 Extracted Topics and Subtopics:</h3>",
                unsafe_allow_html=True
            )
            main_topics = topic_result["topics"]["main"]
            subtopics = topic_result["topics"]["subtopics"]

            st.markdown("**🔹 Topics:**", unsafe_allow_html=True)
            st.markdown(f"**Main Topics:** {', '.join(main_topics) if main_topics else 'None'}", unsafe_allow_html=True)

            if subtopics:
                st.markdown("**🔹 Subtopics:**", unsafe_allow_html=True)
                for topic, sub_list in subtopics.items():
                    st.markdown(f"**{topic}**: {', '.join(sub_list)}", unsafe_allow_html=True)
        else:
            st.warning("⚠️ **Please enter some feedback to analyze.**")

# Adorescore Calculation
elif option == "Adorescore Calculation":
    st.markdown("**Enter customer feedback for Adorescore calculation:**", unsafe_allow_html=True)
    text = st.text_area("**Enter customer feedback**", "")

    if st.markdown('<button class="analyze-button">Calculate Adorescore</button>', unsafe_allow_html=True):
        if text.strip():
            # Call function from scoring.py
            adorescore_result = calculate_adorescore(text)

            # Display Adorescore in Black and Bold
            st.markdown(
                "<h3 style='color: black; font-weight: bold;'>📊 Adorescore Calculation Result:</h3>",
                unsafe_allow_html=True
            )
            st.markdown(f"**Overall Adorescore:** {adorescore_result['Adorescore']['overall']}", unsafe_allow_html=True)

            # Display Topic Breakdown in Black and Bold
            st.markdown(
                "<h3 style='color: black; font-weight: bold;'>📌 Adorescore Breakdown by Topic:</h3>",
                unsafe_allow_html=True
            )
            for topic, score in adorescore_result["Adorescore"]["breakdown"].items():
                st.markdown(f"**🔹{topic}** → Adorescore: {score}", unsafe_allow_html=True)

        else:
            st.warning("⚠️ **Please enter some feedback to analyze.**")
