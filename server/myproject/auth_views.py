from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST


@require_GET
def health_check(request):
    return JsonResponse({"status": "ok"})


@ensure_csrf_cookie
@require_GET
def csrf_token(request):
    return JsonResponse(
        {
            "detail": "CSRF cookie set",
            "csrfToken": get_token(request),
        }
    )


@require_POST
def login_view(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    user = authenticate(request, username=username, password=password)

    if user is None:
        return JsonResponse({"detail": "Invalid username or password."}, status=401)

    login(request, user)
    response = JsonResponse(
        {
            "detail": "Login successful.",
            "username": user.get_username(),
        }
    )
    get_token(request)
    return response


@require_POST
def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "No authenticated user."}, status=401)

    logout(request)
    return JsonResponse({"detail": "Logout successful."})
