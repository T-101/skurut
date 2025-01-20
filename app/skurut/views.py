from django.views.generic import TemplateView


class LandingPageView(TemplateView):
    template_name = 'skurut/index.html'


class InfoView(TemplateView):
    template_name = 'skurut/info.html'