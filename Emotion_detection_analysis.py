import os
import re
from transformers import pipeline  # type: ignore

# Load multi-label emotion detection model
emotion_classifier = pipeline("text-classification",model="SamLowe/roberta-base-go_emotions",top_k=None)  # Multi-label classification

def clean_text(text):
    """Cleans input text by removing unnecessary characters."""
    text = text.lower().strip()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
    return text

def get_activation_level(score):
    """Categorizes activation level based on confidence score."""
    return "High" if score > 0.7 else "Medium" if score > 0.4 else "Low"

def detect_emotions(text):
    """Detects multiple emotions in customer feedback with confidence scores and activation levels."""
    
    text = clean_text(text)  # Preprocess input text

    # Get predictions from the model
    results = emotion_classifier(text)[0]

    # Sort emotions by confidence score
    results_sorted = sorted(results, key=lambda x: x['score'], reverse=True)

    # Keep multiple emotions if they are significant
    highest_score = results_sorted[0]['score']
    min_threshold = max(0.05, highest_score * 0.3)  # 30% of the highest score

    # Filter emotions based on dynamic threshold
    valid_emotions = [emo for emo in results_sorted if emo["score"] >= min_threshold]

    # If no valid emotions remain, return "neutral"
    if not valid_emotions:
        return [{"emotion": "neutral", "activation": "Low", "intensity": 1.0}]

    # Extract detected emotions
    detected_emotions = [
        {
            "emotion": emo["label"],
            "activation": get_activation_level(emo["score"]),
            "intensity": round(emo["score"], 2)
        }
        for emo in valid_emotions
    ]

    return detected_emotions

# Take a single feedback input and analyze emotions
'''text = input("\nEnter customer feedback: ")
result = detect_emotions(text)

# Display results
print("\n Emotion Analysis Result:")
for emo in result:
    print(f"{emo['emotion'].capitalize()} → Confidence: {emo['intensity']}, Activation: {emo['activation']}")

# Terminate program
os._exit(0)'''
