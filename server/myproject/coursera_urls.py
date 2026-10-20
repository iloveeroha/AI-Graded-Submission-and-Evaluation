from django.urls import path

from myproject import auth_views, car_views, dealer_review_views, sentiment_views


urlpatterns = [
    path("login/", auth_views.coursera_login_view, name="coursera-login"),
    path("logout", auth_views.coursera_logout_view, name="coursera-logout"),
    path("logout/", auth_views.coursera_logout_view),
    path("get_cars", car_views.cars_for_course, name="course-get-cars"),
    path("get_cars/", car_views.cars_for_course),
    path(
        "get_dealer_details/<int:dealer_id>",
        dealer_review_views.coursera_dealer_detail,
        name="course-dealer-detail",
    ),
    path(
        "get_dealer_details/<int:dealer_id>/",
        dealer_review_views.coursera_dealer_detail,
    ),
    path(
        "get_dealer_reviews/<int:dealer_id>",
        dealer_review_views.coursera_dealer_reviews,
        name="course-dealer-reviews",
    ),
    path(
        "get_dealer_reviews/<int:dealer_id>/",
        dealer_review_views.coursera_dealer_reviews,
    ),
    path(
        "analyzer/<path:review_text>",
        sentiment_views.analyze_path_review,
        name="course-review-analyzer",
    ),
]
