from django.http import JsonResponse


def TestUserView(request):
    try:
        current_user = request.user
        print("Fro View", current_user.is_authenticated)
        return JsonResponse({"user": current_user})
    except Exception as e:
        print(str(e))
        return JsonResponse({"user": "Anonymous"})
