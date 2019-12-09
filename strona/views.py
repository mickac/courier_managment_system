from django.shortcuts import(
    HttpResponse,
    get_object_or_404,
    redirect,
    render
)
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'

def logout(request):
    logout(request)
    return redirect('home')