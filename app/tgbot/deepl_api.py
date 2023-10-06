import deepl
from decouple import config


async def translate(text: str, language: str) -> str:
    """
    Функция затычка, которая имитирует работу api deepl
    """
    token = config('DEEPL_API')
    try:
        translator = deepl.Translator(token)
        result = await translator.translate_text(text=f'{text}', target_lang=f'{language}')
        return result.text
    except:
        return 'This is mock translation'
