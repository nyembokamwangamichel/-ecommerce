from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Cart, Order, historiqueAchats
from .forms import OrderForm
from shop.models import Product



# FNCT POUR L'AJOUT DE CART
@login_required
def add_to_cart(request, id):
    user = request.user
    product = get_object_or_404(Product, id=id)
    
    # Récupère ou crée un panier pour l'utilisateur
    cart, created = Cart.objects.get_or_create(user=user)
    
    # Récupère ou crée une commande pour ce produit dans le panier
    order, created = Order.objects.get_or_create(user=user, ordered=False, product=product)
    
    if created:
        # Si la commande est nouvellement créée, initialisez le prix total
        order.quantity = 1
        order.prix_total = product.price
        order.save()
        cart.orders.add(order)
    else:
        # Si la commande existe déjà, mettez à jour la quantité et le prix total
        order.quantity += 1
        order.prix_total = product.price * order.quantity
        order.save()
    
    cart.save()
    
    # Redirige vers la page du panier après l'ajout
    return redirect('shop:home')



# AJOUT DE CART
@login_required
def cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    if request.method == 'POST':
        form = OrderForm(request.POST, user=request.user)
        if form.is_valid():
            order_data = form.cleaned_data
            delivery_address = order_data['delivery_address']
            phone_number = order_data['phone_number'] if 'phone_number' in order_data else 'N/A'
            
            # Vérifie la disponibilité des produits dans le panier
            insufficient_stock = []
            for order in cart.orders.all():
                if order.quantity > order.product.quantity or order.quantity < 1:
                    insufficient_stock.append(order.product.title)
            
            if insufficient_stock:
                return render(request, 'store/erreur_cmmd.html', {'produits': insufficient_stock})
            
            # Crée une commande pour chaque article dans le panier
            for order in cart.orders.all():
                Order.objects.create(
                    user=request.user,
                    product=order.product,
                    quantity=order.quantity,
                    prix_total=order.prix_total,
                    ordered=True,
                    ordered_date=timezone.now(),
                    delivery_address=delivery_address,
                    phone_number=phone_number
                )
                
                # permet de creer une historique de l'achat pour l'utilisateur
                historiqueAchats.objects.create(
                    user=request.user,
                    product=order.product.title,
                    quantity=order.quantity,
                    prix_total=order.prix_total,
                    ordered=True,
                    ordered_date=timezone.now(),
                    delivery_address=delivery_address,
                    phone_number=phone_number
                    
                )

            # Supprimer le panier après avoir passé la commande
            request.session['user_info'] = {
                'name': request.user.get_full_name() or request.user.username,
                'email': request.user.email,
                'address': delivery_address,
                'phone': phone_number
            }
            
        
                
            
            
            cart.delete()
            
            return redirect('store:confirmationCommande')
        
    else:
        form = OrderForm(user=request.user)

    total = sum(order.prix_total for order in cart.orders.all())

    return render(request, 'store/cart.html', {
        'orders': cart.orders.all(),
        'form': form,
        'total': total,
        'error_message': None
    })

# FNCT POUR LA SUPPRESSION DE CART
@login_required
def delete_cart(request):
    cart = get_object_or_404(Cart, user=request.user)

    if cart:
        cart.orders.all().delete()
        
        
    return redirect('shop:home')

# POUR LA CONFIRMATION DE LA COMMANDE FAITE PART L'UTILISATEUR 
@login_required
def confirmation_commande(request):
    user_info = request.session.pop('user_info', None)  # Retire les informations de la session
    return render(request, 'store/confirmation_commande.html', {'user_info': user_info})



# POUR RETIRER UN PRODUIT DANS LE PANIER
@login_required
def remove_from_cart(request, order_id):
    user = request.user
    order = get_object_or_404(Order, id=order_id, user=user, ordered=False)
    
    cart = get_object_or_404(Cart, user=user)
    cart.orders.remove(order)
    order.delete()  # Supprimer l'ordre si souhaité ou juste le retirer du panier
    
    return redirect('store:cart')  # Redirige vers la page du panier



# POUR LA MODIFICATION D'UN PRODUIT DANS LE PANIER 
@login_required
def update_cart(request, order_id):
    user = request.user
    order = get_object_or_404(Order, id=order_id, user=user, ordered=False)
    form = OrderForm(request.POST, user=request.user)
    
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 1))
        if new_quantity > 0:
            order.quantity = new_quantity
            order.prix_total = order.product.price * new_quantity
            order.save()
        
        else:
            # Supprimer l'article si la quantité est 0 ou moins
            order.delete()
    
    return redirect('store:cart')  # Redirige vers la page du panier
















