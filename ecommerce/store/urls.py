from django.urls import path
from .views import  add_to_cart, cart, delete_cart,confirmation_commande, remove_from_cart, update_cart

app_name = "store"

urlpatterns = [
    path("product/add_to_cart/<int:id>", add_to_cart, name="add_to_cart"),
    path("cart/", cart, name="cart"),
    path("cart/delete/", delete_cart, name="delete_cart"),
    path('confirmationCommande/', confirmation_commande, name='confirmationCommande'),  # Ajoutez cette ligne pour la page de remerciement
    path('cart/remove/<int:order_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:order_id>/', update_cart, name='update_cart'),
    # ... autres URL patterns
    # Nouvelle route pour créer une commande, mais en fait on gère ça dans la vue 'cart'
    # path("order/create/", order_create, name="order_create"),
]
