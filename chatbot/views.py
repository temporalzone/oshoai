from django.shortcuts import render
from django.http import JsonResponse
from groq import Groq

client = Groq(api_key="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")


def chat(request):
    return render(request, "chat.html")


from .models import ChatHistory

def get_response(request):

    try:

        message = request.GET.get("message")

        # last 5 chats memory
        previous_chats = ChatHistory.objects.all().order_by('-id')[:5]

        memory = ""
        for chat in previous_chats:
            memory += f"User: {chat.user_message}\nOsho: {chat.bot_reply}\n"

        prompt = f"""
You are Osho, the Indian spiritual teacher.

Previous conversation:
{memory}

Now respond to the new problem in Osho's style.

User: {message}
Osho:
"""

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        reply = completion.choices[0].message.content

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