from mlask import MLAsk
import ipadic


def analyze(text):
    emotion_analyzer = MLAsk(ipadic.MECAB_ARGS)
    return emotion_analyzer.analyze(text)
