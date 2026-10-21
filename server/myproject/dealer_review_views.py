from django.http import JsonResponse
from django.views.decorators.http import require_GET

from myproject.models import Dealer, DealerReview


def serialize_dealer(dealer):
    return {
        "id": dealer.id,
        "name": dealer.name,
        "city": dealer.city,
        "state": dealer.state,
        "address": dealer.address,
        "zip": dealer.zip,
        "latitude": dealer.latitude,
        "longitude": dealer.longitude,
        "short_name": dealer.short_name or dealer.name,
        "full_name": dealer.full_name or dealer.name,
    }


def serialize_submission_dealer(dealer):
    return {
        "id": dealer.id,
        "name": dealer.name,
        "city": dealer.city,
        "state": dealer.state,
        "address": dealer.address,
        "zip": dealer.zip,
        "lat": dealer.latitude,
        "lng": dealer.longitude,
        "short_name": dealer.short_name or dealer.name,
        "full_name": dealer.full_name or dealer.name,
    }


@require_GET
def all_dealers(request):
    dealers = Dealer.objects.all()
    return JsonResponse(
        {
            "count": dealers.count(),
            "dealers": [
                {
                    "id": dealer.id,
                    "name": dealer.name,
                    "city": dealer.city,
                    "address": dealer.address,
                }
                for dealer in dealers
            ],
        }
    )


@require_GET
def coursera_all_dealers(request):
    dealers = Dealer.objects.all()
    return JsonResponse(
        {
            "count": dealers.count(),
            "dealers": [
                serialize_submission_dealer(dealer)
                for dealer in dealers
            ],
        }
    )


@require_GET
def dealers_by_state(request, state_code):
    dealers = Dealer.objects.filter(state__iexact=state_code.upper())
    return JsonResponse(
        {
            "state": state_code.upper(),
            "count": dealers.count(),
            "dealers": [
                {
                    "id": dealer.id,
                    "name": dealer.name,
                    "city": dealer.city,
                    "state": dealer.state,
                    "address": dealer.address,
                }
                for dealer in dealers
            ],
        }
    )


@require_GET
def dealer_detail(request, dealer_id):
    try:
        dealer = Dealer.objects.get(id=dealer_id)
    except Dealer.DoesNotExist:
        return JsonResponse({"detail": "Dealer not found."}, status=404)

    return JsonResponse(
        {
            "id": dealer.id,
            "name": dealer.name,
            "city": dealer.city,
            "state": dealer.state,
            "address": dealer.address,
        }
    )


@require_GET
def coursera_dealer_detail(request, dealer_id):
    try:
        dealer = Dealer.objects.get(id=dealer_id)
    except Dealer.DoesNotExist:
        return JsonResponse({"detail": "Dealer not found."}, status=404)
    return JsonResponse(serialize_dealer(dealer))


@require_GET
def fetch_dealer_detail(request, dealer_id):
    try:
        dealer = Dealer.objects.get(id=dealer_id)
    except Dealer.DoesNotExist:
        return JsonResponse({"detail": "Dealer not found."}, status=404)
    return JsonResponse(serialize_submission_dealer(dealer))


@require_GET
def dealer_reviews(request, dealer_id):
    reviews = DealerReview.objects.filter(dealer_id=dealer_id)
    return JsonResponse(
        {
            "dealer_id": dealer_id,
            "count": reviews.count(),
            "reviews": [
                {
                    "id": review.id,
                    "reviewer_name": review.reviewer_name,
                    "rating": review.rating,
                    "comment": review.comment,
                    "created_at": review.created_at.isoformat(),
                }
                for review in reviews
            ],
        }
    )


@require_GET
def coursera_dealer_reviews(request, dealer_id):
    reviews = DealerReview.objects.filter(dealer_id=dealer_id)
    return JsonResponse(
        {
            "dealer_id": dealer_id,
            "count": reviews.count(),
            "reviews": [
                {
                    "id": review.id,
                    "name": review.reviewer_name,
                    "reviewer_name": review.reviewer_name,
                    "dealership": review.dealer_id,
                    "review": review.comment,
                    "rating": review.rating,
                    "comment": review.comment,
                    "purchase": review.purchase,
                    "purchase_date": (
                        review.purchase_date.isoformat()
                        if review.purchase_date
                        else None
                    ),
                    "car_make": review.car_make,
                    "car_model": review.car_model,
                    "car_year": review.car_year,
                    "sentiment": review.sentiment,
                    "created_at": review.created_at.isoformat(),
                }
                for review in reviews
            ],
        }
    )
