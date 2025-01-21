from django.urls import path

from skurut.views import LandingPageView, InfoView, sse_view

app_name = "skurut"

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing-page'),
    path('info/', InfoView.as_view(), name='info'),
    path('events/', sse_view, name='events'),
]
