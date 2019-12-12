from django.shortcuts import(
    HttpResponse,
    get_object_or_404,
    redirect,
    render
)
from django.views.generic.base import TemplateView
from django.core.paginator import(
    Paginator,
    EmptyPage,
    PageNotAnInteger
)
from django.db.models import Q

from .models import(
    PackageAdd,
    Package,
    RemovedPackage
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
                    return redirect('strona:packagelist')
                except Exception as e:
                    return render(request, 'package_add.html', {'e':e, 'form':form})
        else:
            form = PackageAdd()
        return render(request, 'package_add.html', {'form':form})            
    return redirect('strona:packagelist')

def delete(request, pk):
    if request.user.is_superuser:
        try:
            package_id = pk
            get_object_or_404(Package, pk=package_id)
            name = Package.objects.values_list('name', flat=True).get(pk=package_id)
            data = []
            data.append(name)
            remove_package(data)
            return redirect('strona:packagelist')
        except Exception as exception:
            error = "Something went wrong. If error occurs often please send error message contained below to administator."
            error_message = str(exception)
            return render(request, 'error.html', {'em':error_message, 'e':error})

def package_list(request):
    try:
        package_list = Package.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(package_list, 9)
        try:
            packages = paginator.page(page)
        except PageNotAnInteger:
            packages = paginator.page(1)
        except EmptyPage:
            packages = paginator.page(paginator.num_pages)

        return render(request, 'package_list.html', { 'packages': packages })
    except Exception as exception:
        error = "Something went wrong. If error occurs often please send error message contained below to administator."
        error_message = str(exception)
        return render(request, 'error.html', {'em':error_message, 'e':error})

def removedpackages_list(request):
     if request.user.is_superuser:
        try: 
            package_list = RemovedPackage.objects.all()
            page = request.GET.get('page', 1)

            paginator = Paginator(package_list, 2)
            try:
                packages = paginator.page(page)
            except PageNotAnInteger:
                packages = paginator.page(1)
            except EmptyPage:
                packages = paginator.page(paginator.num_pages)

            return render(request, 'removed_packages.html', {'packages':packages})
        except Exception as exception:
            error = "Something went wrong. If error occurs often please send error message contained below to administator."
            error_message = str(exception)
            return render(request, 'error.html', {'em':error_message, 'e':error})

def searchresultview(request):
    query = request.GET.get('q')
    object_list = Package.objects.filter(
        Q(name__icontains=query) | Q(package_type__type_name__icontains=query)
    )
    
    page = request.GET.get('page', 1)
    paginator = Paginator(object_list, 9)

    try:
        packages = paginator.page(page)
        for package in packages:
            print(package, packages)
    except PageNotAnInteger:
        packages = paginator.page(1)
    except EmptyPage:
        packages = paginator.page(paginator.num_pages)

    return render(request, 'search_results.html', { 'searchresults': packages })

def removedpackages_searchlist(request):
    query = request.GET.get('q')
    object_list = RemovedPackage.objects.filter(
        Q(name__icontains=query) & Q(package_type__type_name__icontains=query)
    )
    
    page = request.GET.get('page', 1)
    paginator = Paginator(object_list, 9)

    try:
        packages = paginator.page(page)
        for package in packages:
            print(package, packages)
    except PageNotAnInteger:
        packages = paginator.page(1)
    except EmptyPage:
        packages = paginator.page(paginator.num_pages)
        
    return render(request, 'search_removedpackages.html', { 'searchresults': packages })
