from django.views.generic import TemplateView


class EmptyView(TemplateView):
    template_name = 'boost/test/index.html'
