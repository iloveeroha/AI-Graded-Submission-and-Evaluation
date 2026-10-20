from django.urls import path

from myproject import auth_views, car_views, dealer_review_views, sentiment_views


urlpatterns = [
    path("health/", auth_views.health_check, name="health-check"),
    path("carmakes/", car_views.all_car_makes, name="all-car-makes"),
    path("analyze-review/", sentiment_views.analyze_review, name="analyze-review"),
    path("dealers/", dealer_review_views.all_dealers, name="all-dealers"),
    path(
        "dealers/state/<str:state_code>/",
        dealer_review_views.dealers_by_state,
        name="dealers-by-state",
    ),
    path(
        "dealers/<int:dealer_id>/reviews/",
        dealer_review_views.dealer_reviews,
        name="dealer-reviews",
    ),
    path(
        "dealers/<int:dealer_id>/",
        dealer_review_views.dealer_detail,
        name="dealer-detail",
    ),
    path("csrf/", auth_views.csrf_token, name="csrf-token"),
    path("login/", auth_views.login_view, name="login"),
    path("logout/", auth_views.logout_view, name="logout"),
]
