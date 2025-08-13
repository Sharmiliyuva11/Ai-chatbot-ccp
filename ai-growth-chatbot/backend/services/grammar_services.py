import speech_recognition as sr
import language_tool_python

def convert_voice_to_text(audio_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return {"success": True, "text": text}
    except sr.UnknownValueError:
        return {"success": False, "error": "Could not understand audio"}
    except sr.RequestError as e:
        return {"success": False, "error": f"Speech Recognition error: {e}"}

def analyze_grammar(text):
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(text)
    issues = len(matches)

    grammar_score = max(0, 100 - (issues * 5))  # simple scoring logic
    return {
        "text": text,
        "issues_found": issues,
        "grammar_score": grammar_score,
        "corrections": [match.message for match in matches]
    }

def evaluate_speech_grammar(audio_path):
    result = convert_voice_to_text(audio_path)
    if not result["success"]:
        return result
    return analyze_grammar(result["text"])
