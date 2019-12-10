from django.shortcuts import(
    HttpResponse,
    get_object_or_404,
    redirect,
    render
)
from django.views.generic.base import TemplateView

from .models import(
    PackageAdd,
)
from .api_operations import(
    add_package,
    remove_package
)

class IndexView(TemplateView):
    template_name = 'index.html'

def logout(request):
    logout(request)
    return redirect('home')

def package_add(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = PackageAdd(request.POST)
            if form.is_valid():
                data = []
                data.append(form.cleaned_data['name'])
                data.append(form.cleaned_data['package_type'])
                data.append(form.cleaned_data['package_destination'])
                data.append(form.cleaned_data['package_sizes'])
                try:
                    add_package(data)
                    return redirect('stronka:packagelist')
                except Exception as e:
                    return render(request, 'package_add.html', {'e':e, 'form':form})
        else:
            form = PackageAdd()
        return render(request, 'package_add.html', {'form':form})            
    return redirect('stronka:packagelist')