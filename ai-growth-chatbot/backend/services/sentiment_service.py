from textblob import TextBlob

def analyze_sentiment(user_input):
    """
    Analyzes the sentiment of the given user input and returns the sentiment score and a suggestion.
    """
    if not user_input or not user_input.strip():
        return {
            "success": False,
            "message": "No input text provided."
        }

    blob = TextBlob(user_input)
    polarity = blob.sentiment.polarity  # Range: -1 (negative) to 1 (positive)

    if polarity > 0.2:
        sentiment = "positive"
        suggestion = "That's great to hear! Keep up the good energy and positivity ✨"
    elif polarity < -0.2:
        sentiment = "negative"
        suggestion = "It seems you're feeling down. Remember, tough times pass. Talk to a friend or try a short walk. You're not alone. 💙"
    else:
        sentiment = "neutral"
        suggestion = "It's okay to feel neutral. Try doing something you enjoy or take a small break to recharge 😊"

    return {
        "success": True,
        "sentiment": sentiment,
        "polarity_score": round(polarity, 3),
        "suggestion": suggestion
    }
