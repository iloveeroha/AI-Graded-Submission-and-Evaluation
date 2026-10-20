from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from myproject.models import CarMake, CarModel, Dealer, DealerReview


class ApplicationHomeTests(TestCase):
    def test_home_page_reports_application_health(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})


class SessionAuthenticationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="StrongTestPassword123!",
        )
        self.client = Client(enforce_csrf_checks=True)
        csrf_response = self.client.get("/api/csrf/")
        self.csrf_token = csrf_response.json()["csrfToken"]

    def test_login_and_logout(self):
        login_response = self.client.post(
            "/api/login/",
            {"username": self.user.username, "password": "StrongTestPassword123!"},
            HTTP_X_CSRFTOKEN=self.csrf_token,
        )

        self.assertEqual(login_response.status_code, 200)
        self.assertEqual(login_response.json()["username"], self.user.username)
        self.assertIn("_auth_user_id", self.client.session)

        logout_response = self.client.post(
            "/api/logout/",
            HTTP_X_CSRFTOKEN=self.client.cookies["csrftoken"].value,
        )

        self.assertEqual(logout_response.status_code, 200)
        self.assertEqual(logout_response.json()["detail"], "Logout successful.")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_rejects_invalid_credentials(self):
        response = self.client.post(
            "/api/login/",
            {"username": self.user.username, "password": "incorrect"},
            HTTP_X_CSRFTOKEN=self.csrf_token,
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json()["detail"],
            "Invalid username or password.",
        )

    def test_login_requires_csrf_token(self):
        response = self.client.post(
            "/api/login/",
            {"username": self.user.username, "password": "StrongTestPassword123!"},
        )

        self.assertEqual(response.status_code, 403)

    def test_coursera_login_accepts_json_and_returns_expected_contract(self):
        response = self.client.post(
            "/djangoapp/login/",
            data=(
                '{"userName":"%s","password":"StrongTestPassword123!"}'
                % self.user.username
            ),
            content_type="application/json",
            HTTP_X_CSRFTOKEN=self.csrf_token,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"status": "Authenticated", "userName": self.user.username},
        )

    def test_coursera_login_rejects_invalid_json(self):
        response = self.client.post(
            "/djangoapp/login/",
            data="{",
            content_type="application/json",
            HTTP_X_CSRFTOKEN=self.csrf_token,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "Request body must be valid JSON."},
        )

    def test_coursera_logout_returns_empty_username(self):
        self.client.force_login(self.user)

        response = self.client.get("/djangoapp/logout")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"userName": ""})
        self.assertNotIn("_auth_user_id", self.client.session)


class DealerReviewApiTests(TestCase):
    def test_returns_reviews_for_requested_dealer(self):
        DealerReview.objects.create(
            dealer_id=42,
            reviewer_name="Jordan Lee",
            rating=5,
            comment="Helpful staff and a smooth buying experience.",
        )
        DealerReview.objects.create(
            dealer_id=7,
            reviewer_name="Taylor Smith",
            rating=3,
            comment="The service was fine.",
        )

        response = self.client.get("/api/dealers/42/reviews/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["dealer_id"], 42)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(
            response.json()["reviews"][0]["reviewer_name"],
            "Jordan Lee",
        )

    def test_unknown_dealer_returns_empty_reviews(self):
        response = self.client.get("/api/dealers/999/reviews/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"dealer_id": 999, "count": 0, "reviews": []},
        )

    def test_rejects_non_get_requests(self):
        response = self.client.post("/api/dealers/42/reviews/")

        self.assertEqual(response.status_code, 405)

    def test_coursera_reviews_include_expected_fields(self):
        DealerReview.objects.create(
            dealer_id=42,
            reviewer_name="Jordan Lee",
            rating=5,
            comment="Helpful staff and a smooth buying experience.",
            purchase=True,
            car_make="Toyota",
            car_model="Camry",
            sentiment="positive",
        )

        response = self.client.get("/djangoapp/get_dealer_reviews/42")

        self.assertEqual(response.status_code, 200)
        review = response.json()["reviews"][0]
        self.assertEqual(review["name"], "Jordan Lee")
        self.assertEqual(review["dealership"], 42)
        self.assertEqual(
            review["review"],
            "Helpful staff and a smooth buying experience.",
        )
        self.assertTrue(review["purchase"])
        self.assertEqual(review["car_make"], "Toyota")
        self.assertEqual(review["car_model"], "Camry")
        self.assertEqual(review["sentiment"], "positive")


class DealerListApiTests(TestCase):
    def setUp(self):
        Dealer.objects.all().delete()

    def test_returns_all_dealers(self):
        Dealer.objects.create(
            name="Demo Auto Center",
            city="Demo City",
            state="KS",
            address="123 Example Street",
        )
        Dealer.objects.create(name="Sample Motors", city="Sample Town")

        response = self.client.get("/api/dealers/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 2)
        self.assertEqual(
            [dealer["name"] for dealer in response.json()["dealers"]],
            ["Demo Auto Center", "Sample Motors"],
        )

    def test_returns_empty_list_when_there_are_no_dealers(self):
        response = self.client.get("/api/dealers/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"count": 0, "dealers": []})

    def test_rejects_non_get_requests(self):
        response = self.client.post("/api/dealers/")

        self.assertEqual(response.status_code, 405)


class DealerDetailApiTests(TestCase):
    def setUp(self):
        self.dealer = Dealer.objects.create(
            name="Demo Auto Center",
            city="Demo City",
            address="123 Example Street",
        )

    def test_returns_dealer_details(self):
        response = self.client.get(f"/api/dealers/{self.dealer.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "id": self.dealer.id,
                "name": "Demo Auto Center",
                "city": "Demo City",
                "state": "",
                "address": "123 Example Street",
            },
        )

    def test_coursera_dealer_details_include_all_submission_fields(self):
        self.dealer.zip = "67202"
        self.dealer.latitude = 37.6872
        self.dealer.longitude = -97.3301
        self.dealer.short_name = "Demo Auto"
        self.dealer.full_name = "Demo Auto Center of Wichita"
        self.dealer.save()

        response = self.client.get(
            f"/djangoapp/get_dealer_details/{self.dealer.id}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "id": self.dealer.id,
                "name": "Demo Auto Center",
                "city": "Demo City",
                "state": "",
                "address": "123 Example Street",
                "zip": "67202",
                "latitude": 37.6872,
                "longitude": -97.3301,
                "short_name": "Demo Auto",
                "full_name": "Demo Auto Center of Wichita",
            },
        )

    def test_unknown_dealer_returns_not_found(self):
        response = self.client.get("/api/dealers/999/")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Dealer not found."})

    def test_rejects_non_get_requests(self):
        response = self.client.post(f"/api/dealers/{self.dealer.id}/")

        self.assertEqual(response.status_code, 405)


class DealersByStateApiTests(TestCase):
    def setUp(self):
        Dealer.objects.all().delete()
        Dealer.objects.create(
            name="Demo Kansas Auto Center",
            city="Wichita",
            state="KS",
            address="123 Example Street",
        )
        Dealer.objects.create(
            name="Demo Missouri Motors",
            city="Kansas City",
            state="MO",
            address="456 Sample Avenue",
        )

    def test_returns_only_dealers_in_requested_state(self):
        response = self.client.get("/api/dealers/state/KS/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["state"], "KS")
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(
            response.json()["dealers"][0]["name"],
            "Demo Kansas Auto Center",
        )

    def test_state_filter_is_case_insensitive(self):
        response = self.client.get("/api/dealers/state/ks/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)

    def test_unknown_state_returns_empty_list(self):
        response = self.client.get("/api/dealers/state/NY/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"state": "NY", "count": 0, "dealers": []},
        )


class CarMakeListApiTests(TestCase):
    def setUp(self):
        CarMake.objects.all().delete()

    def test_returns_all_makes_with_their_models(self):
        toyota = CarMake.objects.create(name="Toyota")
        CarModel.objects.create(make=toyota, name="Camry")
        CarModel.objects.create(make=toyota, name="Corolla")
        honda = CarMake.objects.create(name="Honda")
        CarModel.objects.create(make=honda, name="Civic")

        response = self.client.get("/api/carmakes/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 2)
        self.assertEqual(
            response.json()["makes"],
            [
                {
                    "id": honda.id,
                    "name": "Honda",
                    "models": [{"id": honda.models.get().id, "name": "Civic"}],
                },
                {
                    "id": toyota.id,
                    "name": "Toyota",
                    "models": [
                        {"id": model.id, "name": model.name}
                        for model in toyota.models.all()
                    ],
                },
            ],
        )

    def test_returns_empty_list_when_no_makes_exist(self):
        response = self.client.get("/api/carmakes/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"count": 0, "makes": []})

    def test_rejects_non_get_requests(self):
        response = self.client.post("/api/carmakes/")

        self.assertEqual(response.status_code, 405)

    def test_coursera_cars_endpoint_returns_car_models(self):
        toyota = CarMake.objects.create(name="Toyota")
        CarModel.objects.create(make=toyota, name="Camry")

        response = self.client.get("/djangoapp/get_cars")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["CarMakes"], [{"id": toyota.id, "name": "Toyota"}])
        self.assertEqual(
            response.json()["CarModels"],
            [
                {
                    "id": toyota.models.get().id,
                    "name": "Camry",
                    "make": "Toyota",
                    "make_id": toyota.id,
                }
            ],
        )


class ReviewSentimentApiTests(TestCase):
    def test_analyzes_fantastic_services_as_positive(self):
        response = self.client.get(
            "/api/analyze-review/",
            {"text": "Fantastic services"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "text": "Fantastic services",
                "sentiment": "positive",
                "score": 1,
            },
        )

    def test_rejects_missing_review_text(self):
        response = self.client.get("/api/analyze-review/")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "Provide review text using the 'text' query parameter."},
        )

    def test_rejects_non_get_requests(self):
        response = self.client.post("/api/analyze-review/")

        self.assertEqual(response.status_code, 405)

    def test_coursera_analyzer_returns_sentiment_for_path_text(self):
        response = self.client.get(
            "/djangoapp/analyzer/Fantastic%20services"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"sentiment": "positive"})
