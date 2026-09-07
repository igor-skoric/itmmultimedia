# ITM Multimedia

Django sajt za organizaciju i reklamiranje događaja.

## Pokretanje (lokalno)

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

- Sajt: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

Kopiraj `.env.example` u `.env` samo ako hoćeš da menjaš lokalna podešavanja. Bez `.env` sajt radi u debug režimu.

## Jezici

SR / EN / FR — cookie `itm_lang`, prekidač u navigaciji.

## Sadržaj (admin)

- Galerija: kategorije, podkategorije, slike
- Aktuelnosti
- Video snimci (YouTube / Instagram / lokalno)
- Partneri

## Deploy

Kod je na GitHubu: https://github.com/igor-skoric/itmmultimedia

Najjednostavniji put je **VPS (Ubuntu) + Nginx + Gunicorn + HTTPS**. Ako hosting već ima cPanel sa Python/Passenger, koristi `passenger_wsgi.py`.

### 1. Sa ovog računara

```bash
git push origin main
```

### 2. Na VPS-u (prvi put)

1. Ubaci A record domena `itmmultimedia.rs` i `www` na IP servera.
2. Instaliraj Python 3.12, Nginx, Git i Certbot.
3. Kloniraj repo i podigni aplikaciju:

```bash
sudo mkdir -p /var/www
sudo git clone https://github.com/igor-skoric/itmmultimedia.git /var/www/itmmultimedia
cd /var/www/itmmultimedia
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

4. U `.env` obavezno promeni:

- `DJANGO_SECRET_KEY` — generiši sa:
  `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- `DJANGO_ALLOWED_HOSTS=itmmultimedia.rs,www.itmmultimedia.rs`
- `DJANGO_CSRF_TRUSTED_ORIGINS=https://itmmultimedia.rs,https://www.itmmultimedia.rs`

5. Baza, sadržaj i statika:

```bash
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

6. Systemd servis:

```bash
sudo cp deploy/itmmultimedia.service.example /etc/systemd/system/itmmultimedia.service
# uskladi User/WorkingDirectory ako nisu www-data / /var/www/itmmultimedia
sudo systemctl daemon-reload
sudo systemctl enable --now itmmultimedia
```

7. Nginx + HTTPS:

```bash
sudo cp deploy/nginx.conf.example /etc/nginx/sites-available/itmmultimedia
sudo ln -s /etc/nginx/sites-available/itmmultimedia /etc/nginx/sites-enabled/itmmultimedia
sudo nginx -t
sudo systemctl reload nginx
sudo certbot --nginx -d itmmultimedia.rs -d www.itmmultimedia.rs
```

Posle uspešnog HTTPS-a u `.env` stavi `SECURE_SSL_REDIRECT=true` i `SECURE_HSTS_SECONDS=31536000`, pa `sudo systemctl restart itmmultimedia`.

### 3. Svaki sledeći deploy

```bash
cd /var/www/itmmultimedia
git pull origin main
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart itmmultimedia
```

`seed_demo` pokreći samo kada namerno želiš da resetuješ demo sadržaj — briše postojeće vesti, video, partnere i galeriju.

### cPanel / Passenger

Ako je hosting cPanel:

1. Clone ili upload projekta.
2. Python aplikacija neka pokazuje na `passenger_wsgi.py`.
3. Napravi `.env` iz `.env.example`.
4. Pokreni `migrate`, `seed_demo`, `createsuperuser`, `collectstatic --noinput`.
