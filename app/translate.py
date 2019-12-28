import json

import nltk
import requests
from flask import current_app
from flask_babel import _


STOPWORDS_DICT = {lang: set(nltk.corpus.stopwords.words(lang))
                  for lang in nltk.corpus.stopwords.fileids()}

def translate(text, source_language, dest_language):
    if 'MS_TRANSLATOR_KEY' not in current_app.config or \
            not current_app.config['MS_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')
    auth = {
        'Ocp-Apim-Subscription-Key': current_app.config['MS_TRANSLATOR_KEY']}
    r = requests.get('https://api.microsofttranslator.com/v2/Ajax.svc'
                     '/Translate?text={}&from={}&to={}'.format(
                         text, source_language, dest_language),
                     headers=auth)
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    return json.loads(r.content.decode('utf-8-sig'))

def guess_language(text):
    words = set(nltk.wordpunct_tokenize(text.lower()))
    lang = max(((lang, len(words & stopwords))
                for lang, stopwords in STOPWORDS_DICT.items()),
               key=lambda x: x[1])[0]
    return lang[:2]