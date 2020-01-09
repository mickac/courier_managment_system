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
    package_destination = models.CharField(max_length=50, null=True)
    package_sizes = models.CharField(max_length=50, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class Package(PackageAbstract):
    STATUS_CHOICES = (
        ('NDY','Not Deposited Yet'),
        ('DP','Depository'),
        ('IT','In Transit'),
        ('DE','Delivering'),
    )
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='NDY')
    create_date = models.DateTimeField(auto_now_add=True)

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

class PackageEdit(ModelForm):
    class Meta:
        model = Package
        fields = ['package_type', 'package_destination', 'package_sizes','status']

class RemovedPackage(PackageAbstract):
    name = models.CharField(max_length=50, unique=False)
    create_date = models.DateTimeField()
    removal_date = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=500)

class PackageChangeAbstract(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    create_date = models.DateTimeField()
    package_name = models.CharField(max_length=50, null=True)
    package_type = models.ForeignKey(PackageType, on_delete=models.PROTECT)
    package_destination = models.CharField(max_length=50, null=True)
    package_sizes = models.CharField(max_length=50, null=True)

    class Meta:
        abstract = True
        ordering = ['-create_date']

    def __str__(self):
        return self.package.name

class PackageChange(PackageChangeAbstract):
    create_date = models.DateTimeField(auto_now_add=True)   

class OldChange(PackageChangeAbstract):
    package = models.ForeignKey(RemovedPackage, on_delete=models.CASCADE)