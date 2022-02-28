# study evaluation website of my master thesis

## How to install (development)

### Requirements :
You should have Python >= 3.9 and pip install on your computer
Having a dedicated python env for this project is strongly recommended 

### Installation

clone the project and then :
```bash
# enter the repository
cd master_thesis

# install dependencies 
pip install -r requirements.txt

# initialyse django
python manage.py makemigrations my_app
python manage.py migrate

# create a superuser
python manage.py createsuperuser

# start the server
python manage.py runserver

```
## How to install (production)

Follow the same intructions as in development except `python manage.py runserver`

For production, you'll need to obtain your hCaptcha site key and secret key and add them to your settings.
This project is setup so that you can overwrite settings in production by creating a `production.py` file in `/VRCUe_evaluation/settings`

example of what `production.py` can look like :

```python
DEBUG = False

SECRET_KEY = 'YOUR_KEY'
    
ALLOWED_HOSTS = ['my_ip','example.com']
CSRF_TRUSTED_ORIGINS = ['https://example.com']
SRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
    
HCAPTCHA_SITEKEY = '<your sitekey>'
HCAPTCHA_SECRET = '<your secret key>'
    
STATIC_ROOT = "/home/admin/static/"
    
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD=True
```

You will then need to [deploy a webserver](https://docs.djangoproject.com/en/4.0/howto/deployment/)
This was successfully tested with gunicorn and Nginx.
