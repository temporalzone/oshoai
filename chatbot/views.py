from django.shortcuts import render
from django.http import JsonResponse
import os
from groq import Groq


def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise ValueError("Missing GROQ_API_KEY. Set it in your .env file and restart Django.")
    return Groq(api_key=api_key)

def chat(request):
    return render(request, "chat.html")


def get_response(request):
    try:
        message = request.GET.get("message")
        lang = request.GET.get("lang", "auto")
        client = get_groq_client()

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
        error = str(e)
        if "invalid_api_key" in error or "Invalid API Key" in error:
            return JsonResponse({"response": "Your GROQ_API_KEY is invalid. Generate a new key at console.groq.com, update .env, then restart the server."})
        return JsonResponse({"response": error})


def daily_quote(request):
    try:
        prompt = "Give one short inspirational quote in the style of Osho."
        client = get_groq_client()

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )

        quote = chat_completion.choices[0].message.content

        return JsonResponse({"quote": quote})

    except Exception as e:
        error = str(e)
        if "invalid_api_key" in error or "Invalid API Key" in error:
            return JsonResponse({"quote": "Your GROQ_API_KEY is invalid. Generate a new key at console.groq.com, update .env, then restart the server."})
        return JsonResponse({"quote": error})