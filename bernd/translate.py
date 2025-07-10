from googletrans import Translator


async def translate_from_german(text: str) -> list[str]:
    """
    Translate text that may contain german words to English.
    """

    words = text.split()
    print(f"Words to check: {words}")
    translated_words = []
    to_return = []
    async with Translator() as translator:
        for word in words:
            try:
                # if it's already in English, skip it
                lang = await translator.detect(word)
                if lang.lang == "en":
                    continue
                translation = await translator.translate(word, dest="en", src="de")
                translated_words.append(translation.text)
            except Exception as e:
                print(f"Error translating word '{word}': {e}")
                translated_words.append(word)  # Append original word in case of error
    print(f"Translated words: {translated_words}")

    # Remove duplicates while preserving order
    for word in translated_words:
        if word not in words:
            to_return.append(word)

    print(f"Final translated words: {to_return}")
    return translated_words
