from django.shortcuts import render
from django.http import JsonResponse
import os
from groq import Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def chat(request):
    return render(request, "chat.html")


from .models import ChatHistory

def get_response(request):

    try:

        message = request.GET.get("message")
        lang = request.GET.get("lang", "auto")
        # last 5 chats memory
        previous_chats = ChatHistory.objects.all().order_by('-id')[:5]

        memory = ""
        for chat in previous_chats:
            memory += f"User: {chat.user_message}\nOsho: {chat.bot_reply}\n"

        prompt = f"""
You are Osho, the spiritual teacher.

Reply in {lang} language if specified, otherwise respond naturally.

User message:
{message}
"""

        chat_completion = client.chat.completions.create(
        messages=[{"role":"user","content":prompt}],
        model="llama-3.3-70b-versatile",
        )

        reply = chat_completion.choices[0].message.content

        # save chat
        if request.user.is_authenticated:
            ChatHistory.objects.create(
                user=request.user,
                user_message=message,
                bot_reply=reply
            )

        return JsonResponse({"response": reply})

    except Exception as e:
        return JsonResponse({"response": str(e)})

        from django.http import JsonResponse

def daily_quote(request):

    prompt = "Give one short inspirational quote in the style of Osho."

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )

    quote = chat_completion.choices[0].message.content

    return JsonResponse({"quote": quote})