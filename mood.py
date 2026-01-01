# mood.py

POSITIVE_WORDS = [
    "thank you", "thanks", "great", "awesome", "nice", "good",
    "love", "happy", "cool", "amazing", "fantastic", "helpful",
    "excited", "understood", "clear now", "yay"
]

NEGATIVE_WORDS = [
    "sad", "upset", "angry", "bad", "terrible", "hate",
    "confused", "depressed", "tired", "anxious", "anxiety",
    "stress", "stressed", "frustrated", "didn't understand",
    "not understanding", "hard", "difficult"
]

def detect_mood(text: str) -> str:
    text = text.lower()

    if any(word in text for word in ["sad", "cry", "alone", "depressed"]):
        return "😔"
    if any(word in text for word in ["happy", "great", "awesome", "love"]):
        return "😊"
    if any(word in text for word in ["angry", "hate", "mad"]):
        return "😡"

    return "😐"
