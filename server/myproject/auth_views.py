import json

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET
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
def coursera_login_view(request):
    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"detail": "Request body must be valid JSON."}, status=400)

    if not isinstance(payload, dict):
        return JsonResponse(
            {"detail": "Request body must be a JSON object."},
            status=400,
        )

    username = payload.get("userName", "")
    password = payload.get("password", "")
    if not isinstance(username, str) or not isinstance(password, str):
        return JsonResponse(
            {"detail": "userName and password must be strings."},
            status=400,
        )

    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse(
            {"status": "Unauthenticated", "userName": ""},
            status=401,
        )

    login(request, user)
    get_token(request)
    return JsonResponse(
        {"status": "Authenticated", "userName": user.get_username()}
    )


@require_POST
def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "No authenticated user."}, status=401)

    logout(request)
    return JsonResponse({"detail": "Logout successful."})


@require_GET
def coursera_logout_view(request):
    logout(request)
    return JsonResponse({"userName": ""})
