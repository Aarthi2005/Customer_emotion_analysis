import sys
import os
import spacy  # type: ignore
from collections import defaultdict

# Ensure the correct module path is added
MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
if MODULE_PATH not in sys.path:
    sys.path.append(MODULE_PATH)

# Try loading the spaCy model, and handle the case where it is missing
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Error: spaCy model 'en_core_web_sm' not found. Please install it using:")
    print("   python -m spacy download en_core_web_sm")
    sys.exit(1)

stopwords = {"although", "since", "however", "but", "though", "yet", "nevertheless", "nonetheless", "also"}

def extract_topics_and_subtopics(feedback_text):
    """
    Extracts main topics and subtopics from feedback text using NLP.
    """
    doc = nlp(feedback_text)

    main_topics = set()
    subtopics = defaultdict(list)

    compound_nouns = {}  # Stores multi-word nouns (e.g., "customer support")
    noun_mapping = {}  # Maps individual nouns to their full form

    # Step 1: Identify compound nouns (e.g., "customer support")
    for token in doc:
        if token.dep_ == "compound" and token.head.pos_ in {"NOUN", "PROPN"}:
            compound_noun = f"{token.text} {token.head.text}"
            compound_nouns[token.head.text.lower()] = compound_noun
            noun_mapping[token.text.lower()] = compound_noun
            noun_mapping[token.head.text.lower()] = compound_noun

    # Step 2: Identify all main topics
    for token in doc:
        if token.pos_ in {"NOUN", "PROPN"} or token.text.isupper():
            topic = compound_nouns.get(token.text.lower(), token.text)
            noun_mapping[token.text.lower()] = topic

            if topic.lower() not in {"customer"}:
                main_topics.add(topic)

    # Step 3: Identify subtopics (Adjectives and Adverbs modifying Nouns)
    for token in doc:
        if token.pos_ in {"ADJ", "ADV"} and token.text.lower() not in stopwords:
            noun_head = token.head
            topic = noun_mapping.get(noun_head.text.lower(), noun_head.text)

            if noun_head.pos_ in {"NOUN", "PROPN"} or noun_head.text.isupper():
                if topic.lower() not in {"customer"}:
                    subtopics[topic].append(f"{token.text.capitalize()} {topic}")

            elif noun_head.text.lower() in ["was", "is", "felt"]:
                for child in noun_head.children:
                    if child.dep_ in ["nsubj", "nsubjpass"] and (child.pos_ in {"NOUN", "PROPN"} or child.text.isupper()):
                        subject = noun_mapping.get(child.text.lower(), child.text)
                        if subject.lower() not in {"customer"}:
                            subtopics[subject].append(f"{token.text.capitalize()} {subject}")
                            main_topics.add(subject)

    # Step 4: Ensure all noun subjects are captured
    for sent in doc.sents:
        for token in sent:
            if token.dep_ in ["nsubj", "nsubjpass"] and (token.pos_ in {"NOUN", "PROPN"} or token.text.isupper()):
                subject = noun_mapping.get(token.text.lower(), token.text)
                if subject.lower() not in {"customer"}:
                    main_topics.add(subject)

    # Step 5: Detect "X of Y" relationships (e.g., "quality of clothes")
    to_remove = set()
    for token in doc:
        if token.dep_ == "pobj" and token.head.dep_ == "prep" and token.head.text.lower() == "of":
            noun_before = token.head.head.text
            noun_after = token.text

            mapped_before = noun_mapping.get(noun_before.lower(), noun_before)
            mapped_after = noun_mapping.get(noun_after.lower(), noun_after)

            if mapped_before in main_topics and mapped_after in main_topics:
                to_remove.add(mapped_before)
                subtopics[mapped_after].append(mapped_before)

    main_topics -= to_remove

    return {
        "topics": {
            "main": sorted(list(main_topics)),
            "subtopics": dict(subtopics)
        }
    }

# Run only when executed directly
if __name__ == "__main__":
    feedback_text = input("\nEnter your feedback: ")
    result = extract_topics_and_subtopics(feedback_text)
    print("\nExtracted Topics and Subtopics:", result)
