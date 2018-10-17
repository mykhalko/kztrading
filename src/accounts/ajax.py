from django.contrib.auth import get_user_model
from django.http import JsonResponse

User = get_user_model()


def check_email_existence(request):
    email = request.GET['email'].lower()
    return JsonResponse({
        'existence': User.objects.filter(email=email).exists()
    })
