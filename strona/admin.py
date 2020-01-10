from django.contrib import admin
from .models import (
    Package,
    PackageType,
    PackageChange,
    OldChange,
    RemovedPackage,
    DeliveredPackage,
    DeliveringStats,
    AddingStats,
    DeletingStats
)

# Register your models here.
admin.site.register(Package)
admin.site.register(PackageType)
admin.site.register(PackageChange)
admin.site.register(OldChange)
admin.site.register(RemovedPackage)
admin.site.register(DeliveredPackage)
admin.site.register(DeliveringStats)
admin.site.register(AddingStats)
admin.site.register(DeletingStats)

