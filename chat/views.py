from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import os
from google.cloud import translate_v2 as translate
from dotenv import load_dotenv

load_dotenv()

class TranslateAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        text = request.data.get("text")
        target_lang = request.data.get("target_lang")

        if not text or not target_lang:
            return Response({"error": "text와 target_lang이 필요합니다."}, status=400)

        try:
            credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            translate_client = translate.Client.from_service_account_json(credentials_path)

            result = translate_client.translate(text, target_language=target_lang)
            return Response({"translated_text": result["translatedText"]})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
