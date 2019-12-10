import datetime
import time

from django.core.exceptions import ObjectDoesNotExist

from .models import (
    PackageAdd,
    PackageType,
    Package,
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
        device_type=package.package_type,
        device_login=device.device_login,
        device_password=device.device_password,
        device_ipv4=device.device_ipv4,
        running_config=device.running_config,
        startup_config=device.startup_config,
        create_date=device.create_date
    )
    removed_package.save()
    changes = PackageChange.objects.all().filter(package=package)
    for change in changes:
        old_change = OldChange(
            user=change.user,
            device=removed_device,
            create_date=change.create_date,
            configuration_type=change.configuration_type,
            partial_configuration=change.partial_configuration,
        )
        old_change.save()
        change.delete()
    device.delete()

    return etree.Element("ok")