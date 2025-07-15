import random
from googletrans import Translator, LANGCODES
from bernd.database.models import GuildSetting


def random_langcode() -> str:
    """
    Get a random language code from the LANGCODES dictionary.
    """
    lang_code = random.choice(list(LANGCODES.keys()))
    print(f"Random language code selected: {lang_code}")
    return lang_code


async def translate_from_german(text: str, guild_setting: GuildSetting) -> list[str]:
    """
    Translate text that may contain german words to English.
    """

    words = text.lower().split()
    print(f"Words to check: {words}")
    translated_words: list[str] = []
    to_return = []
    if guild_setting.chaos_level == 1:
        translated_words = await normal_translate(text)
    elif guild_setting.chaos_level == 2:
        translated_words = await no_context_translate(text)
    elif guild_setting.chaos_level == 3:
        translated_words = await chaos_translate(text)
    else:
        print(f"Unknown chaos level: {guild_setting.chaos_level}")
        return []

    if guild_setting.response_mode == "single":
        # Remove duplicates while preserving order
        for word in translated_words:
            if word.lower() not in words:
                to_return.append(word)
    elif guild_setting.response_mode == "full":
        to_return = translated_words
    else:
        print(f"Unknown response mode: {guild_setting.response_mode}")
        return []

    print(f"Final translated words: {to_return}")
    return to_return


async def has_non_english_words(text: str) -> bool:
    """
    Check if the text contains any German words.
    """
    words = text.lower().split()
    async with Translator() as translator:
        for word in words:
            try:
                lang = await translator.detect(word)
                if lang.lang != "en":
                    return True
            except Exception as e:
                print(f"Error detecting language for word '{word}': {e}")
    return False


async def normal_translate(text: str) -> list[str]:
    """
    Translate text from German to English.
    """
    if not await has_non_english_words(text):
        return []
    async with Translator() as translator:
        try:
            translation = await translator.translate(text, dest="en", src="de")
            return translation.text.split()
        except Exception as e:
            print(f"Error translating text '{text}': {e}")
            return []


async def no_context_translate(text: str) -> list[str]:
    """
    Translate text from German to English without context.
    """
    if not await has_non_english_words(text):
        return []
    words = text.lower().split()
    to_return = []

    async with Translator() as translator:
        for word in words:
            try:
                lang = await translator.detect(word)
                if lang.lang != "en":
                    translation = await translator.translate(word, dest="en", src="de")
                    to_return.append(translation.text)
                else:
                    to_return.append(word)
            except Exception as e:
                print(f"Error translating word '{word}': {e}")
                to_return.append(word)
    print(f"Translated words without context: {to_return}")
    return to_return


async def chaos_translate(text: str) -> list[str]:
    """
    Translate text from German to English with chaos mode. This mode translates the text to a random language,
    back to German, and then to English without context.
    """
    if not await has_non_english_words(text):
        return []

    words = text.lower().split()
    to_return = []
    random_lang = random_langcode()

    async with Translator() as translator:
        for word in words:
            try:
                lang = await translator.detect(word)
                if lang.lang != "en":
                    # Translate to a random language
                    translation = await translator.translate(
                        word, dest=random_lang, src="de"
                    )
                    # Translate back to German
                    back_to_german = await translator.translate(
                        translation.text, dest="de", src=random_lang
                    )
                    # Finally translate to English
                    final_translation = await translator.translate(
                        back_to_german.text, dest="en", src="de"
                    )
                    to_return.append(final_translation.text)
                else:
                    to_return.append(word)
            except Exception as e:
                print(f"Error translating word '{word}': {e}")
                to_return.append(word)
    print(f"Chaos translated words: {to_return}")
    return to_return
