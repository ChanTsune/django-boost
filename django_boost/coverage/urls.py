import os
from django.urls import path, include
from django.conf import settings
from django_boost.urls import include_static_files



urlpatterns = [
    path('', include_static_files(os.path.join(settings.BASE_DIR, 'htmlcov')))
]
