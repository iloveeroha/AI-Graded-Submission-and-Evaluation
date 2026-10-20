import re

from django.http import JsonResponse
from django.views.decorators.http import require_GET


POSITIVE_WORDS = {
    "amazing",
    "awesome",
    "excellent",
    "fantastic",
    "friendly",
    "good",
    "great",
    "helpful",
    "love",
    "smooth",
    "wonderful",
}
NEGATIVE_WORDS = {
    "awful",
    "bad",
    "disappointing",
    "hate",
    "horrible",
    "poor",
    "rude",
    "terrible",
    "worst",
}


@require_GET
def analyze_review(request):
    text = request.GET.get("text", "").strip()
    if not text:
        return JsonResponse(
            {"detail": "Provide review text using the 'text' query parameter."},
            status=400,
        )

    words = re.findall(r"[a-z]+", text.lower())
    score = sum(word in POSITIVE_WORDS for word in words) - sum(
        word in NEGATIVE_WORDS for word in words
    )
    sentiment = "positive" if score > 0 else "negative" if score < 0 else "neutral"

    return JsonResponse(
        {
            "text": text,
            "sentiment": sentiment,
            "score": score,
        }
    )
