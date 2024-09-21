from django.urls import path
from .views import detail, index,recherche_produit, search_categorie


app_name = 'shop'

urlpatterns = [
    path('',index,name="home"),
    path('search/',recherche_produit,name='search'),
    path('search_categorie/<int:id>',search_categorie,name='search_categorie'),
    path('detail/<int:id>/',detail,name='detail'), # il faut que la variable id_pro soit la même au niveau du parametre du vieuw
]
