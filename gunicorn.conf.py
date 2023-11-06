"""
gunicorn
 --bind 0.0.0.0:8005
 --pythonpath django-apps
 --env DJANGO_CONFIGURATION=Production
 --env DJANGO_SETTINGS_MODULE=project.settings
 project.wsgi

"""
from pathlib import Path

BASE_DIR = Path(__file__).parents[0].resolve()

proc_name = "sveetch-home_gunicorn"

bind = ["0.0.0.0:8005"]

pythonpath = str(BASE_DIR / "django-apps")

raw_env = [
    "DJANGO_CONFIGURATION=Production",
    "DJANGO_SETTINGS_MODULE=project.settings",
]
