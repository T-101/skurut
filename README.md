# Skurut
### Seuraa ratikoita kartalla
- - -
Käyttää [HSL:n avointa rajapintaa](https://www.hsl.fi/hsl/avoin-data)
sekä [OpenStreetMapin](https://www.openstreetmap.org) karttaa.
- - -
### Instructions for development
1. Clone the repo in your favorite way
2. Copy `.env-example` to  `.env` in project root and app-directory.
3. In `app/.env` change values for `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`
4. Build the container `docker compose build`
5. Edit `docker-compose.yml` and uncomment preferred command to run Django
6. Run the container `docker compose up -d`
7. Run migrations `docker compose exec app python manage.py migrate`
8. Create superuser `docker compose exec app python manage.py createsuperuser`
9. Collect static files `docker compose exec app python manage.py collectstatic --no-input`