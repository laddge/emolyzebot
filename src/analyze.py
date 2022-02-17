import googletrans
import nltk
if nltk.download('vader_lexicon'):
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

tr = googletrans.Translator()
vader_analyzer = SentimentIntensityAnalyzer()


def analyze(text):
    en = tr.translate(text).text
    res = vader_analyzer.polarity_scores(en)
    return res
