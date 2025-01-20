from django.urls import path

from skurut.views import LandingPageView, InfoView

app_name = "skurut"

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing-page'),
    path('info/', InfoView.as_view(), name='info')
]
