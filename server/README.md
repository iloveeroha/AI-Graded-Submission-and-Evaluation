# Local Django login/logout demo

This Django project provides session-based `POST /api/login/` and
`POST /api/logout/` endpoints with CSRF protection, as well as a public
`GET /api/dealers/`, `GET /api/dealers/state/<state_code>/`,
`GET /api/dealers/<dealer_id>/`, `GET /api/dealers/<dealer_id>/reviews/`, and
`GET /api/carmakes/` endpoints, along with a lightweight review sentiment
endpoint at `GET /api/analyze-review/?text=...`.

Course-compatible endpoints are also available at `/djangoapp/login/`
(JSON POST with `userName` and `password`), `/djangoapp/logout` (GET),
`/djangoapp/get_dealer_reviews/<dealer_id>`,
`/djangoapp/get_dealer_details/<dealer_id>`, `/djangoapp/get_cars`, and
`/djangoapp/analyzer/<review_text>`. The existing `/api/...` routes remain
available with their original response contracts.

## Set up and run (PowerShell)

From the `server` directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:DJANGO_SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(50))"
$env:DJANGO_DEBUG = "true"
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Create the local user when prompted. Keep its password private; the login
helper prompts for it without echoing it or writing it to a file.

## Deploy on Render

The repository root contains `render.yaml`, which configures a free Render web
service using the `server` directory. Once the Django project is pushed to
GitHub, create a Blueprint in Render and select this repository. Render will
install the requirements, collect static files, apply migrations on startup,
and expose a public `onrender.com` URL. The service's `/api/health/` endpoint
is used for health checks.

The free instance uses its local SQLite database, which is ephemeral and can be
reset when the service restarts or redeploys. A migration adds clearly
synthetic dealer, review, and 15 car-model records so the coursework endpoints
have demonstration data; do not use this setup for persistent production data.

## Capture the login and logout examples

Open a second PowerShell terminal in this directory and run:

```powershell
.\loginuser.ps1
.\logoutuser.ps1
```

The first script writes the cURL command and real HTTP response to `loginuser`.
It requests a CSRF token, then sends a JSON body containing `userName` and
`password` to `/djangoapp/login/`. The second uses the session cookie from the
successful login and sends `GET /djangoapp/logout`, saving its response to
`logoutuser`. The cookie jar is ignored by Git because it contains local
session data; the captures contain only redacted credentials and response data.

The CSRF bootstrap endpoint is `GET /api/csrf/`; use its token and the cookie
jar for login POST requests. The Django test suite covers both authentication
contracts, invalid credentials, CSRF enforcement, and dealer-review queries:

```powershell
$env:DJANGO_SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(50))"
$env:DJANGO_DEBUG = "true"
python manage.py test
```

Use a fresh generated secret in each terminal session. The project refuses to
start when `DJANGO_SECRET_KEY` is missing and has debug mode disabled unless
`DJANGO_DEBUG=true` is explicitly set.

## Capture dealer reviews

Use a dealer ID returned by `GET /api/dealers/`, then run:

```powershell
.\getdealerreviews.ps1 -DealerId 1
```

The script writes the cURL command and actual JSON response to `getdealerreviews`.
The course endpoint returns review records for that dealer, including reviewer,
purchase, vehicle, and sentiment fields.

## Capture all dealers

```powershell
.\getalldealers.ps1
```

This saves the cURL command and actual JSON response to `getalldealers`. Dealer
records come from the local database; the project does not include real dealer
data, so add the appropriate records before capturing a submission.

## Capture a dealer's details

```powershell
.\getdealerbyid.ps1 -DealerId 1
```

The script writes the cURL command and actual JSON response to `getdealerbyid`.
Use an ID returned by `GET /api/dealers/`.

## Capture dealers by state

```powershell
.\getdealersbyState.ps1
```

This requests `GET /api/dealers/state/KS/` and saves the cURL command and
response to `getdealersbyState`. State values are US postal abbreviations, and
the database must contain actual dealer records for the results to be real.

## Capture all car makes and models

```powershell
.\getallcarmakes.ps1
```

This saves the cURL command and actual JSON response to `getallcarmakes`.
The course endpoint returns `CarMakes` and `CarModels`; the demo migration
seeds 15 models.

## Analyze a review

```powershell
.\analyzerreview.ps1
```

This captures the sentiment response for the review text `Fantastic services`
in `analyzerreview` using the course-compatible path endpoint. The demo uses a
small built-in positive/negative word list; it is a basic demonstration, not a
machine-learning sentiment service.
