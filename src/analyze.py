from mlask import MLAsk


def analyze(text):
    emotion_analyzer = MLAsk()
    return emotion_analyzer.analyze(text)
