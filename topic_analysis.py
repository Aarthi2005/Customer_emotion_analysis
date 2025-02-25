import spacy # type: ignore
from collections import defaultdict
import subprocess

# Ensure model is installed
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
    nlp = spacy.load("en_core_web_sm")

#nlp = spacy.load("en_core_web_sm")


stopwords = {"although", "since", "however", "but", "though", "yet", "nevertheless", "nonetheless", "also"}

def extract_topics_and_subtopics(feedback_text):
    doc = nlp(feedback_text)

    main_topics = set()
    subtopics = defaultdict(list)

    compound_nouns = {}  # Stores multi-word nouns (e.g., "customer support")
    noun_mapping = {}  # Maps individual nouns to their full form

    # Step 1: Identify compound nouns (e.g., "customer support")
    for token in doc:
        if token.dep_ == "compound" and token.head.pos_ in {"NOUN", "PROPN"}:
            compound_noun = f"{token.text} {token.head.text}"
            compound_nouns[token.head.text.lower()] = compound_noun  # Store lowercase key
            noun_mapping[token.text.lower()] = compound_noun
            noun_mapping[token.head.text.lower()] = compound_noun

    # Step 2: Identify all main topics (including stand-alone nouns and uppercase words)
    for token in doc:
        if token.pos_ in {"NOUN", "PROPN"} or token.text.isupper():  # Treat all uppercase words as nouns
            topic = compound_nouns.get(token.text.lower(), token.text)
            noun_mapping[token.text.lower()] = topic  # Store mapping in lowercase

            if topic.lower() not in {"customer"}:  # Avoid generic words
                main_topics.add(topic)

    # Step 3: Identify subtopics (Adjectives and Adverbs modifying Nouns)
    for token in doc:
        if token.pos_ in {"ADJ", "ADV"} and token.text.lower() not in stopwords:
            noun_head = token.head
            topic = noun_mapping.get(noun_head.text.lower(), noun_head.text)

            # If the adjective modifies a noun, add it
            if noun_head.pos_ in {"NOUN", "PROPN"} or noun_head.text.isupper():
                if topic.lower() not in {"customer"}:
                    subtopics[topic].append(f"{token.text.capitalize()} {topic}")

            # If the adjective/adverb modifies a verb like "was", find the noun subject
            elif noun_head.text.lower() in ["was", "is", "felt"]:
                for child in noun_head.children:
                    if child.dep_ in ["nsubj", "nsubjpass"] and (child.pos_ in {"NOUN", "PROPN"} or child.text.isupper()):
                        subject = noun_mapping.get(child.text.lower(), child.text)
                        if subject.lower() not in {"customer"}:
                            subtopics[subject].append(f"{token.text.capitalize()} {subject}")
                            main_topics.add(subject)

    # Step 4: Ensure all noun subjects are captured (Fix for short sentences)
    for sent in doc.sents:
        for token in sent:
            if token.dep_ in ["nsubj", "nsubjpass"] and (token.pos_ in {"NOUN", "PROPN"} or token.text.isupper()):
                subject = noun_mapping.get(token.text.lower(), token.text)
                if subject.lower() not in {"customer"}:
                    main_topics.add(subject)

    # Step 5: Detect "X of Y" relationships (e.g., "quality of clothes")
    for token in doc:
        if token.dep_ == "pobj" and token.head.dep_ == "prep" and token.head.text.lower() == "of":
            noun_before = token.head.head.text  # The noun before "of" (e.g., "quality")
            noun_after = token.text  # The noun after "of" (e.g., "clothes")

            mapped_before = noun_mapping.get(noun_before.lower(), noun_before)
            mapped_after = noun_mapping.get(noun_after.lower(), noun_after)

            if mapped_before in main_topics and mapped_after in main_topics:
                main_topics.remove(mapped_before)  # Remove as a main topic
                subtopics[mapped_after].append(mapped_before)  # Add as a subtopic

    return {
        "topics": {
            "main": sorted(list(main_topics)),  # Sort for consistency
            "subtopics": dict(subtopics)  # Convert defaultdict to normal dict
        }
    }

'''# Ask for a single feedback input
feedback_text = input("\nEnter your feedback: ")

# Process the feedback
result = extract_topics_and_subtopics(feedback_text)

# Display the result
print("\nExtracted Topics and Subtopics:", result)'''
