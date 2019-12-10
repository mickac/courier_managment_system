from django.contrib import admin
from .models import (
    Package,
    PackageType,
    PackageChange,
    OldChange,
    RemovedPackage
)

# Register your models here.
admin.site.register(Package)
admin.site.register(PackageType)
admin.site.register(PackageChange)
admin.site.register(OldChange)
admin.site.register(RemovedPackage)
