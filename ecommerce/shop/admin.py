from django.contrib import admin
from .models import Product,category

# permet d'afficher les infos de chq produit sous forme de la table au niveau de la page admin du site
class admin_product(admin.ModelAdmin):
    list_display = ('title','description','price','date_added','category','image')
    list_filter = ['category','date_added']
    search_fields = ['title','price','date_added','category']

# permet d'afficher les infos de chq cateogrie sous forme de la table au niveau de la page admin du site
class Admin_categorie(admin.ModelAdmin):
    list_display = ('name','date_added')
    list_filter = ['name','date_added']
    search_fields = ['name','date_added']
    


# enregistrement de tables au niveau de l'administration
admin.site.register(Product,admin_product)
admin.site.register(category,Admin_categorie)

# permet de changer le nom du titre de la page admin
admin.site.site_header = "Maïck_service Administration"