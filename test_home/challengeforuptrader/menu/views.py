from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'menu/home.html'


class BlogView(TemplateView):
    template_name = 'menu/blog.html'
