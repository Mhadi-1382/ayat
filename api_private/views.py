
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from authentication.models import CustomeUser
from panel.bale import send_bale_message
import json

@csrf_exempt
def bale_webhook(request):
    if request.method != "POST":
        return JsonResponse({"ok": False})

    try:
        data = json.loads(request.body)
        message = data.get("message", {})
        text = message.get("text", "").strip()
        chat = message.get("chat", {})
        chat_id = chat.get("id")

        if not text or not chat_id:
            return JsonResponse({"ok": True})
        
        user = CustomeUser.objects.filter(id=text).first()
        if user:
            user.bale_chat_id = chat_id
            user.save()

            send_bale_message(chat_id, "حساب شما با موفقیت به آیت متصل شد.")

        return JsonResponse({"ok": True})
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)})
