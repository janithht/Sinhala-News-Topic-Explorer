from flask import Flask, request, jsonify
from gensim import corpora
from gensim.models import LdaModel
import json
from itertools import chain
from sinling import SinhalaTokenizer, SinhalaStemmer
import os

# 1. Show your current working directory
print("CWD:", os.getcwd())

dictionary = corpora.Dictionary.load("./Flask App/dictionary.dict")
lda = LdaModel.load("./Flask App/model.lda")
with open("./Flask App/labels.json", "r", encoding="utf-8") as f:
    HUMAN_LABELS = json.load(f)

tok = SinhalaTokenizer()
stem = SinhalaStemmer()

def preprocess(text):
    """
    Split, tokenize, stem, and filter out stopwords/short tokens.
    """
    SINHALA_STOPWORDS = {
        "අ","ආ","ඉ","ඊ","උ","ඌ","එ","ඔ","ඓ","ඖ",
        "ක","ග","ච","ට","ත","ප","බ","ම","ය","ර","ල","ව",
        "ශ","ෂ","ස","හ","ළ","ෆ"
    }
    tokens = []
    for sent in tok.split_sentences(str(text)):
        for w in tok.tokenize(sent):
            if len(w) > 1 and w not in SINHALA_STOPWORDS:
                tokens.append(stem.stem(w))
    return tokens

def flatten_and_extract(doc):
    flat = list(chain.from_iterable(doc)) if any(isinstance(el, list) for el in doc) else doc
    return [token if isinstance(token, str) else token[0] for token in flat]

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "<h2>Sinhala News Topic Explorer</h2>\n<p>POST JSON {'text': '<your Sinhala text>'} to /infer_topic</p>"

@app.route("/infer_topic", methods=["POST"])
def infer_topic():
    data = request.get_json()
    text = data.get("text", "")

    # Preprocess and vectorize
    raw_tokens = preprocess(text)
    tokens = flatten_and_extract(raw_tokens)
    bow = dictionary.doc2bow(tokens)

    # Get and sort topic probabilities
    doc_topics = sorted(lda.get_document_topics(bow), key=lambda x: -x[1])

    # Build response with top 3
    result = []
    for tid, score in doc_topics[:3]:
        keywords = [w for w, _ in lda.show_topic(int(tid), topn=5)]
        label = HUMAN_LABELS.get(str(tid), HUMAN_LABELS.get(int(tid), f"Topic {tid}"))
        result.append({
            "topic_id": tid,
            "label": label,
            "score": float(score),
            "keywords": keywords
        })
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
