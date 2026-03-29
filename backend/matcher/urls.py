from django.urls import path
from .views import match_resume, match_text

urlpatterns = [
    path('match/', match_resume, name='match_resume'),
    # path("api/match-text/", match_text, name="match_text"),   model evaluation route
]