from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import EchoHistory
# Create your views here.
@login_required
def image_history(request):

    histories = (
        EchoHistory.objects
        .filter(user=request.user)
        .order_by("-created_at")[:5]
    )

    data = []

    for item in histories:
        data.append({
            "id": item.id,
            "result_image": item.image.url,
            "created_at": item.created_at,
        })

    return JsonResponse({
        "status": "success",
        "data": data
    })