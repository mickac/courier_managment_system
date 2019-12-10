import datetime
import time

from django.core.exceptions import ObjectDoesNotExist

from .models import (
    PackageAdd,
    PackageType,
    Package,
    RemovedPackage,
    PackageChange
)

def add_package(data):
    try:
        package_name = data[0].text
        package_type_name = data[1].text
        package_destination = data[2].text
        package_sizes = data[3].text
    except AttributeError:
        package_name = data[0]
        package_type_name = data[1]
        package_destination = data[2]
        package_sizes = data[3]

    new_package = Package(
        name=package_name,
        package_type=package_type_name,
        package_destination=package_destination,
        package_sizes=package_sizes,
    )

    new_package.save()

def remove_package(data):
    try:
        package_name = data[0].text
    except AttributeError:
        package_name = data[0]

    package = Package.objects.get(name=package_name)

    removed_package = RemovedPackage(
        name=package.name,
        package_type=package.package_type,
        package_sizes=package.package_sizes,
        package_destination=package.package_destination,
        create_date=package.create_date,
    )
    removed_package.save()
    changes = PackageChange.objects.all().filter(package=package)
    for change in changes:
        old_change = OldChange(
            user=change.user,
            package=removed_package,
            create_date=change.create_date,
        )
        old_change.save()
        change.delete()
    package.delete()