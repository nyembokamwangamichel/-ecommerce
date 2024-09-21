#  LES IMPORTS POUR LE MAIL D'ACTIVATION DE COMPTE UTILISATEUR

from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_text  #
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site 
from .token import generatorToken


##### installation d'une bibliothèque en SIX
##### Creation du fichier tokken  dans l'app
###################################################

from django.shortcuts import redirect, render 
from django.contrib.auth.models import User   # l'impprtation du modele utilisateur 
from django.contrib import messages      # pour les messages d'erreurs et succès
from django.contrib.auth import authenticate, login, logout    # pour la connéxion et la déconnexion d'utilisateur
from django.core.mail import send_mail       # pour l'envoi de mail
from ecommerce.settings import EMAIL_HOST_USER   # importation de la variable qui est dans settings pour l'adresse mail du site
from store.models import historiqueAchats    #  pour l'historique des achats de l'utilisateur 
from django.contrib.auth.decorators import login_required   # le décorrateur  qui internit l'accès des views avant la connexion de l'utilisateur
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CustomUserChangeForm



# FNCT POUR L'ENREGISTREMENT DU COMPTE D'UN UTILISATEUR
def register_user(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

    # vérification de saisie
        
        if username == "" or email == "" or password == "":
            messages.error(request, "Attention ! rassurez-vous que les champs nom,email et mot de passe sont bien remplis")
            return redirect('accounts:register_user')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom a été déjà pris")
            return redirect('accounts:register_user')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet email a déjà un compte")
            return redirect('accounts:register_user')

        if not username.isalnum():
            messages.error(request, "Le nom doit être alphanumérique")
            return redirect('accounts:register_user')

        if password != password1:
            messages.error(request, "Les mots de passe ne sont pas identiques")
            return redirect('accounts:register_user')
        
    # création de compte d'utilisateur 
        mon_utilisateur = User.objects.create_user(username=username, email=email, password=password)
        mon_utilisateur.first_name = firstname
        mon_utilisateur.last_name = lastname
        mon_utilisateur.is_active = False     # Permet de desactiver l'utilisateur même si il est enregistrer 
                                              # il va activé son compte à partir de message mail qui lui séra envoyer lors de la création de compte
        mon_utilisateur.save()

        messages.success(request, 'Votre compte a été créé avec succès')
        
    # Envoi le mail de bienvenue
        subject = "Bienvenue sur Maïck de réseaux système login" # le sujet 
        message = f"Bienvenue {mon_utilisateur.username} {mon_utilisateur.first_name} \nNous sommes heureux de vous compter parmi nous \n\nMerci \n\nMaïck de réseaux" # le message envoyer
        from_email = EMAIL_HOST_USER    # adresse de l'expéditeur
        recipient_list = [mon_utilisateur.email]  # la liste des addresse de déstinateur

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)  # l'envoi de message
                                                                                      # fiel_silently : pour la vérification de l'envie
        
    # Email de confirmation 
        current_site = get_current_site(request)
        emal_subject = "Confirmation de l'address email sur maïck de réseau"   # sujet
        messageConfirm = render_to_string("emailconfirm.html",{ #  le fichier  emailconfirm.html est créer dans le dossier templates de cette app
            "name":mon_utilisateur.username,
            "domain":current_site,
            "uid":urlsafe_base64_encode(force_bytes(mon_utilisateur.pk)),   # l'id du compte a activé
            "token":generatorToken.make_token(mon_utilisateur)  
        })
        
        email = EmailMessage(
            emal_subject,
            messageConfirm,
            EMAIL_HOST_USER,
            [mon_utilisateur.email]
        )
        
        email.fail_silently = False
        email.send()  # envoie du message
        
        return redirect('accounts:login_user')

    return render(request, 'accounts/register_user.html')



# FNCT POUR LA CONNEXION D'UTILISATEUR
def login_user(request):
    
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        my_user = User.objects.get(username=username) # permet de recuperer l'utilisateur qui veut se connécter puis
                                                    
        if user is not None:
            login(request,user)
            username = user.username
            context = {'username':username}
            return redirect('shop:home')
        elif my_user.is_active == False:  # pour nous permettre de vérifiér si son compte est activé ou pas 
            messages.error(request, "vous avez pas encore activé / confirmer votre compte, fait le avant de se connecter merci")
        else:
            messages.error(request,'mauvaise authentification')
            return redirect('accounts:login_user')
    return render(request,'accounts/login_user.html')



# FNCT POUR LA DECONNEXION D'UTILISATEUR
def logout_user(request):
    
    logout(request)
    messages.success(request,'vous êtes bien déconnecté ')
    return redirect("shop:home")



# FNCT POUR LA VOIR LE PROFIL D'UTILISATEUR
def profil(request):
    return render(request,'accounts/profil_compte.html')


#FNCT POUR LA MODIFICATION DES PROFILS
@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:profil')  # Redirection après la sauvegarde
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'accounts/profile_edit.html', {'form': form})





# FNCT POUR LA MODIFICATION DU MOT DE PASSE D'UTILISATEUR
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # sa récupere l'utilisateur qui est connecter
            return redirect('password_change_done')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'accounts/modification_password.html', {'form': form})



# FNCT POUR L'HISTORIQUE D'ACHAT D'UN UTILISATEUR
def historique_achats(request):
    
    histor = historiqueAchats.objects.filter(user=request.user)
    context = {'historique':histor}
    
    return render(request,'accounts/historique_achats.html', context)


# FNC POUR ACTIVER LE COMPTE D'UTILISATEUR APRES AVOIR CLIQUER SUR LE LEIN QUI LUI SERA ENVOYER DANS LE MESSAGE DE CONFI
def activate(request,uidb64, token):
    
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid) # récuper l'utilisateur 
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None
    if user is not None and generatorToken.check_token(user,token):
        user.is_active  
        user.save()
        messages.success(request,"Votre compte a été bien activé felicitation vous pouvais maintement vous connecter")
        return redirect('accounts:login_user')
    else:
        messages.error(request,'activation a échoué !!')
        return redirect('accounts:home')
    

# FNCT POUR LA SUPPRESSION DE L'HISTORIQUE
@login_required
def deleteHistore(request):
    
    histor = historiqueAchats.objects.filter(user=request.user)
    histor.delete()
        
    return redirect('shop:home')