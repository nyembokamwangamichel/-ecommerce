from django.shortcuts import render,redirect
from .models import Product,category
from django.db.models import Q    # Ce models  permet de rechercher un contenu dans la base de donnée avec plusieur possibilité
from django.core.paginator import Paginator   # permet de limiter le nombre de elements qui séront afficher sur une page 
from django.db.models.signals import post_delete
from django.dispatch import receiver 
import os



# LA FNCT POUR AFFICHER LA PAGE D'ACCUEIL
def index(request):
    products = Product.objects.filter(quantity__gt = 0)  # recuperation de produits qui ont une quantité supérieure à 0
    categorie = category.objects.all()    
    
    
    paginator = Paginator(products,8)     # La limitation 8 produits par page
    page = request.GET.get('page')
    products = paginator.get_page(page)   
    
    context = {'product':products,'categorie':categorie}
    return render(request,'shop/index.html',context)


# FNCT POUR LA CHERCHE PAR CATEGORIE 
def search_categorie(request,id):
    
    cat = category.objects.get(id=id)
    produit = Product.objects.filter(category=cat).filter(quantity__gt = 0) # Recupere le produits qui ont une quantité supérieure à 0  et une catégorie précise
    categorie = category.objects.all()
    context = {'product':produit,'categorie':categorie}
    
    return render(request,'shop/seach_categ.html',context)


# FNCT POUR LA RECHERCHE DE PRODUITS
def recherche_produit(request):
    recherche = request.GET.get('search')
    categorie = category.objects.all()
    if recherche != '' and recherche is not None:
        resultat = Product.objects.filter(Q(title__icontains=recherche), # permet de chercher le produit selon le nom ou bien 
                                         Q(title__icontains=recherche)) #  recherche selon la description
                                          
        paginator = Paginator(resultat,4)  # limitation de page par 4 produits par page
        page = request.GET.get('page')
        products = paginator.get_page(page)
    
        context = {'product':resultat,'categorie':categorie}
        return render(request,'shop/search.html',context)
    
    return redirect('shop:home')

# FNCT POUR LA DETAIL D'UN PRODUIT 
def detail(request,id):
    produit = Product.objects.get(id=id) 
    context = {'product':produit}

    return render(request,'shop/detail.html',context)



# FNCT POUR LA SUPRESSION D'UN PRODUIT

@receiver(post_delete,sender=Product)
def supprimer_produit(sender,instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
    