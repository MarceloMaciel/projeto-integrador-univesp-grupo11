# create_superuser.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BibliotecaPI.settings')
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('userAdminGrupo11', 'userAdminGrupo11@userAdminGrupo11.com', 'grupo11@123')