from deep_translator import GoogleTranslator

SUPPORTED_LANGUAGES = GoogleTranslator.get_supported_languages(as_dict=True)

for lang in SUPPORTED_LANGUAGES:
  lang_shortcode = SUPPORTED_LANGUAGES[lang]

  print(f'| {lang.capitalize()} ({lang_shortcode}) | [.txt](https://github.com/frekwencja/most-common-words-multilingual/blob/main/data/wordfrequency.info/{lang_shortcode}.txt) |')