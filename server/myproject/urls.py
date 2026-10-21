from django.contrib import admin
from django.urls import include, path

from myproject import auth_views, dealer_review_views, sentiment_views


urlpatterns = [
    path("", auth_views.health_check, name="home"),
    path("admin/", admin.site.urls),
    path("api/", include("myproject.auth_urls")),
    path("djangoapp/", include("myproject.coursera_urls")),
    path(
        "fetchReviews/dealer/<int:dealer_id>",
        dealer_review_views.coursera_dealer_reviews,
        name="submission-fetch-dealer-reviews",
    ),
    path(
        "fetchReviews/dealer/<int:dealer_id>/",
        dealer_review_views.coursera_dealer_reviews,
    ),
    path(
        "fetchDealers",
        dealer_review_views.coursera_all_dealers,
        name="submission-fetch-dealers",
    ),
    path(
        "fetchDealers/",
        dealer_review_views.coursera_all_dealers,
    ),
    path(
        "fetchDealer/<int:dealer_id>",
        dealer_review_views.fetch_dealer_detail,
        name="submission-fetch-dealer",
    ),
    path(
        "fetchDealer/<int:dealer_id>/",
        dealer_review_views.fetch_dealer_detail,
    ),
    path(
        "analyze/<path:review_text>",
        sentiment_views.analyze_path_review,
        name="submission-analyze-review",
    ),
]
