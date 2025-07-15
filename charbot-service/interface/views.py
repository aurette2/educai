from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI

# Assure-toi que la clé est définie ici ou via une variable d’environnement
client = OpenAI(api_key = "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" )# ← ou utilise 

@csrf_exempt
def chat_page(request):
    user_input = None
    bot_response = None

    if request.method == "POST":
        user_input = request.POST.get("message")

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Tu es un assistant pédagogique."},
                    {"role": "user", "content": user_input}
                ]
            )
            bot_response = response.choices[0].message.content.strip()

        except Exception as e:
            bot_response = f"Erreur : {e}"

    return render(request, "interface/chat.html", {
        "user_input": user_input,
        "bot_response": bot_response,
    })