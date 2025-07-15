from django.http import JsonResponse
from django.views import View
import json
import os
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = "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"
client = OpenAI()

class ChatAPIView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Tu es un assistant éducatif."},
                    {"role": "user", "content": user_message}
                ]
            )

            bot_reply = response.choices[0].message.content.strip()
            return JsonResponse({"response": bot_reply})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)