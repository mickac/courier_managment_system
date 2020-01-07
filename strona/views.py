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
    PackageEdit,
    Package,
    RemovedPackage,
    DeliveredPackage,
    PackageChange
)
from .api_operations import(
    add_package,
    remove_package,
    deliver_package
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
                except Exception as exception:
                    error = "Something went wrong. If error occurs often please send error message contained below to administator."
                    error_message = str(exception)
                    return render(request, 'error.html', {'em':error_message, 'e':error})
        else:
            form = PackageAdd()
        return render(request, 'package_add.html', {'form':form})            
    return redirect('strona:packagelist')

def edit(request, pk):
    try:
        if request.user.is_superuser:
            package = get_object_or_404(Package, pk=pk)
            if request.method == "POST":
                form = PackageEdit(request.POST, instance=package)
                if form.is_valid():
                    package_name = package.name
                    package_type = form.cleaned_data['package_type']
                    package_destination = form.cleaned_data['package_destination']
                    package_sizes = form.cleaned_data['package_sizes']
                    pack = form.save(commit=False)
                    pack.package_type = package_type
                    pack.package_destination = package_destination
                    pack.package_sizes = package_sizes
                    #pack.create_date = timezone.now()
                    pack.save()
                    packageedit = PackageChange(
                        user = request.user,
                        package_name = package_name,
                        package_id = pk,
                        package_type = package_type,
                        package_destination = package_destination,
                        package_sizes = package_sizes,
                    )
                    packageedit.save()
                    return redirect('strona:packagelist')
            else:
                form = PackageEdit(instance=package)
            return render(request, 'package_edit.html', {'form':form}) 
    except Exception as exception:
        error = "Something went wrong. If error occurs often please send error message contained below to administator."
        error_message = str(exception)
        return render(request, 'error.html', {'em':error_message, 'e':error})

def package_delivered(request, pk):
    if request.user.is_authenticated:
        try:
            package_id = pk
            get_object_or_404(Package, pk=package_id)
            name = Package.objects.values_list('name', flat=True).get(pk=package_id)
            data = []
            data.append(name)
            deliver_package(data)
            return redirect('strona:deliveredlist')
        except Exception as exception:
            error = "Something went wrong. If error occurs often please send error message contained below to administator."
            error_message = str(exception)
            return render(request, 'error.html', {'em':error_message, 'e':error})        
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

            paginator = Paginator(package_list, 5)
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

def deliveredpackages_list(request):
     if request.user.is_superuser:
        try: 
            package_list = DeliveredPackage.objects.all()
            page = request.GET.get('page', 1)

            paginator = Paginator(package_list, 5)
            try:
                packages = paginator.page(page)
            except PageNotAnInteger:
                packages = paginator.page(1)
            except EmptyPage:
                packages = paginator.page(paginator.num_pages)

            return render(request, 'delivered_packages.html', {'packages':packages})
        except Exception as exception:
            error = "Something went wrong. If error occurs often please send error message contained below to administator."
            error_message = str(exception)
            return render(request, 'error.html', {'em':error_message, 'e':error})

def changedpackages_list(request):
     if request.user.is_superuser:
        try: 
            package_list = PackageChange.objects.all()
            page = request.GET.get('page', 1)

            paginator = Paginator(package_list, 5)
            try:
                packages = paginator.page(page)
            except PageNotAnInteger:
                packages = paginator.page(1)
            except EmptyPage:
                packages = paginator.page(paginator.num_pages)

            return render(request, 'package_changes.html', {'packages':packages})
        except Exception as exception:
            error = "Something went wrong. If error occurs often please send error message contained below to administator."
            error_message = str(exception)
            return render(request, 'error.html', {'em':error_message, 'e':error})

def searchresultview(request):
    if request.user.is_authenticated:
        try:
            query = request.GET.get('q')
            package_list = Package.objects.filter(
                Q(name__icontains=query) | Q(package_type__type_name__icontains=query) | Q(package_destination__icontains=query) | Q(package_sizes__icontains=query)
            )
            
            page = request.GET.get('page', 1)
            paginator = Paginator(package_list, 9)

            try:
                packages = paginator.page(page)
                for package in packages:
                    print(package, packages)
            except PageNotAnInteger:
                packages = paginator.page(1)
            except EmptyPage:
                packages = paginator.page(paginator.num_pages)

            return render(request, 'search_results.html', { 'searchresults': packages })
        except Exception as exception:
            error = "Something went wrong. If error occurs often please send error message contained below to administator."
            error_message = str(exception)
            return render(request, 'error.html', {'em':error_message, 'e':error})

def removedpackages_searchlist(request):
    if request.user.is_superuser:
        try:
            query = request.GET.get('q')
            package_list = RemovedPackage.objects.filter(
                Q(name__icontains=query) | Q(package_type__type_name__icontains=query) | Q(package_destination__icontains=query) | Q(package_sizes__icontains=query)
            )
            
            page = request.GET.get('page', 1)
            paginator = Paginator(package_list, 5)

            try:
                packages = paginator.page(page)
                for package in packages:
                    print(package, packages)
            except PageNotAnInteger:
                packages = paginator.page(1)
            except EmptyPage:
                packages = paginator.page(paginator.num_pages)
                
            return render(request, 'search_removedpackages.html', { 'searchresults': packages })
        except Exception as exception:
            error = "Something went wrong. If error occurs often please send error message contained below to administator."
            error_message = str(exception)
            return render(request, 'error.html', {'em':error_message, 'e':error})

def deliveredpackages_searchlist(request):
    if request.user.is_authenticated:
        try:
            query = request.GET.get('q')
            package_list = DeliveredPackage.objects.filter(
                Q(name__icontains=query) | Q(package_type__type_name__icontains=query) | Q(package_destination__icontains=query) | Q(package_sizes__icontains=query)
            )
            
            page = request.GET.get('page', 1)
            paginator = Paginator(package_list, 5)

            try:
                packages = paginator.page(page)
                for package in packages:
                    print(package, packages)
            except PageNotAnInteger:
                packages = paginator.page(1)
            except EmptyPage:
                packages = paginator.page(paginator.num_pages)
                
            return render(request, 'search_deliveredpackages.html', { 'searchresults': packages })
        except Exception as exception:
            error = "Something went wrong. If error occurs often please send error message contained below to administator."
            error_message = str(exception)
            return render(request, 'error.html', {'em':error_message, 'e':error})            

def changedpackages_searchlist(request):
    if request.user.is_superuser:
        try:
            query = request.GET.get('q')
            package_list = PackageChange.objects.filter(
                Q(name__icontains=query) | Q(package_type__type_name__icontains=query) | Q(package_destination__icontains=query) | Q(package_sizes__icontains=query)
            )
            
            page = request.GET.get('page', 1)
            paginator = Paginator(package_list, 5)

            try:
                packages = paginator.page(page)
                for package in packages:
                    print(package, packages)
            except PageNotAnInteger:
                packages = paginator.page(1)
            except EmptyPage:
                packages = paginator.page(paginator.num_pages)
                
            return render(request, 'search_changedpackages.html', { 'searchresults': packages })
        except Exception as exception:
            error = "Something went wrong. If error occurs often please send error message contained below to administator."
            error_message = str(exception)
            return render(request, 'error.html', {'em':error_message, 'e':error})      