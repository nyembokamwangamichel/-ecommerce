from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
from shop.models import Product  # Assurez-vous que 'Product' est importé correctement

from django.db import models
from django.contrib.auth.models import User
from shop.models import Product
from django.utils import timezone

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    prix_total = models.FloatField(default=0.0)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)
    delivery_address = models.CharField(max_length=255, blank=True, null=True)  # Champ pour l'adresse de livraison
    phone_number = models.CharField(default=False,max_length=15)

    def __str__(self):
        return f"{self.product.title} ({self.quantity})"



class historiqueAchats(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.CharField(max_length=120)
    quantity = models.IntegerField(default=1)
    prix_total = models.FloatField(default=0.0)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)
    delivery_address = models.CharField(max_length=255, blank=True, null=True)  # Champ pour l'adresse de livraison
    phone_number = models.CharField(default=False,max_length=15)
    
    
   
    
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order, related_name='carts')


    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()
        self.orders.clear()
        super().delete(*args, **kwargs)
