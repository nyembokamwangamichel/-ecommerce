from django.db import models


# la table pour la categorie
class category(models.Model):
    name = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_added']
    def __str__(self):
        return self.name

# la table pour les produits        
class Product (models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    quantity = models.DecimalField(max_digits=100000,decimal_places=0)
    description = models.TextField()
    category = models.ForeignKey(category ,related_name = 'categorie',on_delete=models.CASCADE)  # la clé etrangère qui reilie la table produit à la table categorie
    image = models.ImageField(upload_to='images',blank=True)
    date_added = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_added']
    def __str__(self):
        return self.title
        