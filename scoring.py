import spacy # type: ignore
from textblob import TextBlob # type: ignore
from topic_analysis import extract_topics_and_subtopics
from Emotion_detection_analysis import detect_emotions
from collections import defaultdict

nlp = spacy.load("en_core_web_sm")

def get_sentiment_score(text):
    """Returns sentiment score (-100 to +100) using TextBlob."""
    sentiment = TextBlob(text).sentiment.polarity  # Range: -1 to +1
    return int(sentiment * 100)  # Convert to -100 to +100 scale

def map_emotions_to_topics(feedback_text):
    """
    Maps detected emotions to specific topics and subtopics.
    """
    topic_data = extract_topics_and_subtopics(feedback_text)
    main_topics = topic_data["topics"]["main"]
    subtopics = topic_data["topics"]["subtopics"]

    detected_emotions = detect_emotions(feedback_text)

    # Mapping emotions to topics
    topic_emotion_map = defaultdict(list)

    for sent in nlp(feedback_text).sents:
        sentence_text = sent.text
        emotions = detect_emotions(sentence_text)  # Get emotions per sentence
        for topic in main_topics:
            if topic in sentence_text:
                topic_emotion_map[topic].extend(emotions)

    return {
        "topics": topic_data,
        "emotions": detected_emotions,
        "theme_emotion_map": dict(topic_emotion_map)
    }

def calculate_adorescore(feedback_text):
    """
    Computes Adorescore with breakdown per topic.
    """
    integrated_data = map_emotions_to_topics(feedback_text)
    main_topics = integrated_data["topics"]["topics"]["main"]
    
    adorescore = get_sentiment_score(feedback_text)

    # Score breakdown for each topic
    topic_scores = {}
    for topic in main_topics:
        topic_sentences = [sent.text for sent in nlp(feedback_text).sents if topic in sent.text]
        topic_text = " ".join(topic_sentences) if topic_sentences else feedback_text  # Fallback to full text
        topic_scores[topic] = get_sentiment_score(topic_text)

    return {
        "Adorescore": {
            "overall": adorescore,
            "breakdown": topic_scores
        },
        "Integrated Analysis": integrated_data
    }
