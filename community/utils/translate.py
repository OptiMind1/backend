from google.cloud import translate_v2 as translate
from asgiref.sync import sync_to_async

translate_client = translate.Client()

@sync_to_async
def translate_text(text, target_lang='en'):
    if isinstance(text, bytes):
        text = text.decode("utf-8")

    try:
        result = translate_client.translate(
            text,
            target_language=target_lang,
            format_='text'
        )
        return result['translatedText']
    except Exception as e:
        print("Translation error:", e)
        return text
