from django.shortcuts import render
from django.http import JsonResponse
import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def chat(request):
    return render(request, "chat.html")


def get_response(request):
    try:
        message = request.GET.get("message")
        lang = request.GET.get("lang", "auto")

        prompt = f"""
You are Osho, the spiritual teacher.
Reply in a calm philosophical tone like Osho.
Respond in {lang} language if specified.

User message:
{message}
"""

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )

        reply = chat_completion.choices[0].message.content

        return JsonResponse({"response": reply})

    except Exception as e:
        return JsonResponse({"response": str(e)})


def daily_quote(request):
    try:
        prompt = "Give one short inspirational quote in the style of Osho."

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )

        quote = chat_completion.choices[0].message.content

        return JsonResponse({"quote": quote})

    except Exception as e:
        return JsonResponse({"quote": str(e)})