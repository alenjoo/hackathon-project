from django.http import JsonResponse
import os

def payment_health(request):
    keys = {
        "RAZORPAY_KEY_ID": os.getenv("RAZORPAY_KEY_ID"),
        "RAZORPAY_KEY_SECRET": os.getenv("RAZORPAY_KEY_SECRET"),
        "RAZORPAY_SECRET_KEY": os.getenv("RAZORPAY_SECRET_KEY"),
    }

    missing = [k for k, v in keys.items() if not v]
    if missing:
        return JsonResponse({"status": "Missing keys", "missing": missing}, status=500)

    return JsonResponse({"status": "OK", "gateway": "Razorpay Sandbox"})
