from django.http import JsonResponse
from django.views.decorators.http import require_GET

from myproject.models import Dealer, DealerReview


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
