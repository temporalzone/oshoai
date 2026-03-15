from django.shortcuts import render
from django.http import JsonResponse
from django.http import JsonResponse
from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_response(request):

    message = request.GET.get("message")
    lang = request.GET.get("lang", "auto")

    prompt = f"""
You are Osho, the spiritual teacher.

Reply in a calm and philosophical tone like Osho.
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

        from django.http import JsonResponse

def daily_quote(request):

    prompt = "Give one short inspirational quote in the style of Osho."

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )

    quote = chat_completion.choices[0].message.content

    return JsonResponse({"quote": quote})