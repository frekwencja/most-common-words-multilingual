import textwrap
from typing import List

from deep_translator import GoogleTranslator
import pandas as pd

import time

CONFIG = {
    # 'SHEET_DOWNLOAD_URL': 'https://www.wordfrequency.info/samples/wordFrequency.xlsx',
    'SHEET_DOWNLOAD_URL': 'http://localhost:2137/wordFrequency.xlsx',
    'SHEET_NAME_TO_READ': '1 lemmas',
    'SHEET_COLUMN_TO_READ': 'lemma',
    'WORDS_EXPORT_COUNT': 5050,
    'GOOGLE_TRANSLATE_CHARACTER_LIMIT': 4500,
    'SOURCE_LANGUAGE': 'en',
    'SUPPORTED_LANGUAGES': GoogleTranslator.get_supported_languages(as_dict=True),
    'SLEEP_AMOUNT': 5,
}


def read_words_from_sheet() -> List[str]:
    # Pandas can read directly from URL. We are interested in lemmas sheet, as it contains basic forms of words.
    df = pd.read_excel(CONFIG['SHEET_DOWNLOAD_URL'], CONFIG['SHEET_NAME_TO_READ'])

    # Limit how many words should be read.
    df = df.head(CONFIG['WORDS_EXPORT_COUNT'])

    # Some words are recognized as boolean, so we should correct them to string.
    return [str(row.lemma) for row in df.itertuples()]


def prepare_words_for_translation(words: List[str]) -> List[str]:
    # Translators have characters limit. This function splits lists, so it will be possible to translate them.
    split_word_lists = textwrap.wrap(' '.join(words), width=CONFIG['GOOGLE_TRANSLATE_CHARACTER_LIMIT'])

    # Put the words in separate lines, so translator will treat them individually.
    return ['\n'.join(words.split()) for words in split_word_lists]


def translate_words(lang: str, words: List) -> List[str]:
    translated_strings = GoogleTranslator(source='en', target=lang).translate_batch(words)

    # Converts to lists and then flatten as we only will need only one list
    return flatten([translation.split('\n') for translation in translated_strings])


def translate_to_every_language_and_export(words_prepared_to_translate):
    for lang in CONFIG['SUPPORTED_LANGUAGES']:
        lang_shortcode = CONFIG['SUPPORTED_LANGUAGES'][lang]

        if lang_shortcode == 'en':
            continue
        
        data = {
            lang_shortcode: translate_words(lang, words_prepared_to_translate)
        }

        df = pd.DataFrame(data)
        df.to_csv(f'data/wordfrequency.info/{lang_shortcode}.txt', index=False)

        time.sleep(CONFIG['SLEEP_AMOUNT'])


def flatten(list: List[List]) -> List:
    return [item for sublist in list for item in sublist]


def main():
    words = read_words_from_sheet()
    prepared_words = prepare_words_for_translation(words)
    translate_to_every_language_and_export(prepared_words)

    


main()
