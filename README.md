# ITM Multimedia

Django demo sajt za organizaciju i reklamiranje događaja.

## Pokretanje

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

- Sajt: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Jezici

SR / EN / FR — cookie `itm_lang`, prekidač u navigaciji.

## Sadržaj (admin)

- Galerija: kategorije, podkategorije, slike
- Aktuelnosti
- Video snimci (YouTube / Instagram / lokalno)
- Partneri
