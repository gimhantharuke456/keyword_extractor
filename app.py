from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk import pos_tag
import warnings




warnings.filterwarnings('ignore')

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

app = Flask(__name__)
CORS(app)


def translator(t):
    from googletrans import Translator
    translator = Translator()
    return translator.translate(t).text

def sinhalTranslator(words):
    from googletrans import Translator
    translator = Translator()
    sinhala_words = []

    for word in words:
        # Translate each word from English to Sinhala
        translated_word = translator.translate(word, src='en', dest='si').text
        sinhala_words.append(translated_word)

    return sinhala_words


def keyworsExtractorEnglish(text):
    tokens = word_tokenize(text)

    tagged_tokens = pos_tag(tokens)

    # Extract nouns
    nouns = [word for word, pos in tagged_tokens if pos.startswith('NN')]

    # Calculate word frequencies for nouns
    freq_dist = FreqDist(nouns)

    # Extract the top N keywords (adjust N as needed)
    top_keywords = freq_dist.most_common(5)  # Change 5 to the desired number of keywords

    # Return the keywords
    return [keyword[0] for keyword in top_keywords]


def keywordExtractorFromSinhala(text):
    # Tokenize the text
    text = translator(text)
    tokens = word_tokenize(text)

    tagged_tokens = pos_tag(tokens)

    # Extract nouns
    nouns = [word for word, pos in tagged_tokens if pos.startswith('NN')]

    # Calculate word frequencies for nouns
    freq_dist = FreqDist(nouns)

    # Extract the top N keywords (adjust N as needed)
    top_keywords = freq_dist.most_common(5)  # Change 5 to the desired number of keywords
    wordds = [keyword[0] for keyword in top_keywords]
    # Return the keywords
    return sinhalTranslator(wordds)


@app.route('/extract_keywords-sinhala', methods=['POST'])
def extract_keywords():
    if request.method == 'POST':
        try:
            data = request.json
            text = data.get('text', '')

            if text:
                keywords = keyworsExtractorEnglish(text)
                return jsonify({'keywords': keywords})
            else:
                return jsonify({'error': 'Text not provided in the request body'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/extract_keywords', methods=['POST'])
def extract_keywords_english():
    if request.method == 'POST':
        try:
            data = request.json
            text = data.get('text', '')

            if text:
                keywords = keyworsExtractorEnglish(text)
                return jsonify({'keywords': keywords})
            else:
                return jsonify({'error': 'Text not provided in the request body'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
