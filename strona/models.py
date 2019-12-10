from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.forms import(
    ModelForm,
    Textarea
)

class PackageType(models.Model):
    type_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.type_name

class PackageAbstract(models.Model):
    name = models.CharField(max_length=50, unique=True)
    package_type = models.ForeignKey(PackageType, on_delete=models.PROTECT)
    
    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class Package(PackageAbstract):
    create_date = models.DateTimeField(auto_now_add=True)
    package_destination = models.CharField(max_length=50)
    package_sizes = models.CharField(max_length=50)

    class Meta(PackageAbstract.Meta):
        ordering = ['create_date']

class DeliveredPackage(PackageAbstract):
    name = models.CharField(max_length=50, unique=False)
    create_date = models.DateTimeField()
    delivered_date = models.DateTimeField(auto_now_add=True)

class PackageAdd(ModelForm):
    class Meta:
        model = Package
        fields = ['name', 'package_type', 'package_destination', 'package_sizes']