from http.server import BaseHTTPRequestHandler
from transformers import pipeline
import nltk
import spacy
import json
import random

nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)
from nltk.corpus import wordnet

nlp = spacy.load("en_core_web_sm")
paraphraser = pipeline("text2text-generation", model="tuner007/pegasus_paraphrase")

def get_synonyms(word, pos):
    synonyms = []
    for syn in wordnet.synsets(word):
        if syn.pos() == pos:
            for lemma in syn.lemmas():
                if lemma.name() != word and "_" not in lemma.name():
                    synonyms.append(lemma.name())
    return list(set(synonyms))

def paraphrase_sentence(sentence):
    paraphrased = paraphraser(sentence, max_length=60, num_return_sequences=3)
    return paraphrased[0]['generated_text']

def enhance_text(text, complexity, preserve_keywords):
    doc = nlp(text)
    enhanced_sentences = []

    for sent in doc.sents:
        if random.random() < 0.5:  # 50% chance to paraphrase the entire sentence
            enhanced_sentences.append(paraphrase_sentence(sent.text))
        else:
            enhanced_tokens = []
            for token in sent:
                if token.text.lower() in preserve_keywords or token.is_punct or token.is_space:
                    enhanced_tokens.append(token.text)
                elif len(token.text) > 3 and token.pos_ in ['NOUN', 'VERB', 'ADJ', 'ADV']:
                    synonyms = get_synonyms(token.text, token.pos_[0].lower())
                    if synonyms:
                        enhanced_tokens.append(random.choice(synonyms))
                    else:
                        enhanced_tokens.append(token.text)
                else:
                    enhanced_tokens.append(token.text)
            enhanced_sentences.append(" ".join(enhanced_tokens))

    enhanced_text = " ".join(enhanced_sentences)
    return enhanced_text

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        text = data['text']
        complexity = data['complexity']
        preserve_keywords = data['preserveKeywords']

        enhanced_text = enhance_text(text, complexity, preserve_keywords)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = json.dumps({'originalText': text, 'enhancedText': enhanced_text})
        self.wfile.write(response.encode('utf-8'))
        return
