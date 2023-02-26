# URL Shortening Service

This is a URL shortening service that generates short and unique URLs for long URLs. The service is built with Django and supports custom aliases and expiration dates.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.x
- Django 3.x
- SQLite 3.x (or any other supported database)

### Installing

1. Clone the repository to your local machine:

```json
git clone https://github.com/<username>/url-shortener.git
```

2. Change directory to the project folder:

```json
cd url-shortener

```

3. Install the project dependencies:

```json
pip install -r requirements.txt

```

4. Make a `.env` file in this directory only and put the following

```bash
DJANGO_SECRET_KEY = django-insecure-3a65@ycam887r2c69p=3st-_#s8k26t(-*h8@4ic_f1qo1*ow6
DJANGO_DEBUG = True
```

5. Run the database migrations:

```json
python manage.py migrate

```

6. Start the development server:

```json
python manage.py runserver
```

7. Open your web browser and navigate to `http://localhost:8000` to access the URL shortening service.

8. To run the unittests

```json
python manage.py test
```

## API Reference

The URL shortening service exposes the following API:

### POST /shorten_url

This API generates a short URL for the specified original URL. The API supports custom aliases and expiration dates.

#### Request

- **URL**: `/shorten_url`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Request Body**:

| Parameter      | Type     | Required | Description                                                                      |
| -------------- | -------- | -------- | -------------------------------------------------------------------------------- |
| `original_url` | `string` | Yes      | The original URL to shorten.                                                     |
| `custom_alias` | `string` | No       | Optional custom alias for the short URL.                                         |
| `expires_at`   | `string` | No       | Optional expiration date/time for the short URL in `YYYY-MM-DD HH:MM:SS` format. |

#### Response

The API returns a JSON object containing the generated short URL:

```json
{
  "original_url": "https://www.google.com/search?q=url+shortener",
  "short_url": "http://localhost:8000/abc123",
  "expires_at": "2023-03-31 12:00:00"
}
```

If a custom alias is provided and it is already in use, the API will return a `400 Bad Request` response with the following error message:

```json
{
  "error": "The specified alias is already in use."
}
```

If an expiration date/time is provided and it is in the past, the API will return a `400 Bad Request` response.

### GET /<str:short_url>

This APIView is responsible for redirecting to the original URL corresponding to the specified short URL.

#### Request

- **URL**: `/<str:short_url>`
- **Method**: `GET`
- **Content-Type**: `application/json`
- **URL Parameters**: `short_url` (string, required): the short URL to redirect to the original URL.

#### Response

A redirect response to the original URL if the short URL exists, or a 404 error response.

## Expired URL Deletion

Shortened URLs with expiration datetime are set to be deleted after expiration. To automatically delete expired URLs, a `delete_expired_urls` function has been implemented in `backends` folder of `shortener` app. This function is run periodically on daily basis using APScheduler.

## Built With

- [Python](https://www.python.org/) - Programming language used
- [Django](https://www.djangoproject.com/) - Web framework used
- [Django REST Framework](https://www.django-rest-framework.org/) - Toolkit used for building APIs
