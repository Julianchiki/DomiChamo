from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class MeasurementUnits(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(verbose_name='name', null=False)
    abbreviation = models.TextField(verbose_name='abbreviation', null=False)

    def __str__(self):
        return self.name

class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(verbose_name='name', null=False)

    def __str__(self):
        return self.name

class Elements(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(verbose_name='Nombre', null=False)
    measurement_unit = models.ForeignKey(MeasurementUnits, on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Descripción', null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', verbose_name='Imagen', null=True)

    def __str__(self):
        return self.name


class Inventories(models.Model):
    id = models.AutoField(primary_key=True)
    element = models.ForeignKey(Elements, on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='Precio', null=False, default=0)
    amount = models.IntegerField(verbose_name='Cantidad', null=False, default=0)
    stock = models.IntegerField(verbose_name='Stock', null=False, default=0)
    lot_number = models.IntegerField(verbose_name='Lote', null=True)
    expiration_date = models.DateField(verbose_name='Fecha de Expiración', null=True)
    user  = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.element.name

class Domicilies(models.Model):
    id = models.AutoField(primary_key=True)
    addres = models.TextField(null=False)
    date_time = models.DateTimeField(null=False)
    state = models.TextField(null=False)
    total = models.IntegerField(null=False, default=0)
    user  = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.addres

class AssignDomicilies(models.Model):
    id = models.AutoField(primary_key=True)
    domicilie  = models.ForeignKey(Domicilies, on_delete=models.CASCADE)    
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    
class DomicilieDetail(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.IntegerField(null=False)
    subtotal = models.IntegerField(null=False)
    inventory = models.ForeignKey(Inventories, on_delete=models.CASCADE)
    domicilie  = models.ForeignKey(Domicilies, on_delete=models.CASCADE)    
    user  = models.ForeignKey(User, on_delete=models.CASCADE)