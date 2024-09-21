from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.core.mail import send_mail
from ecommerce.settings import EMAIL_HOST_USER
from django.contrib.auth.decorators import login_required


# POUR L'ENVOIE DU MESSAGE COMMENTAIRE
@login_required
def sendmail_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        website = request.POST.get('website')
        message = request.POST.get('message')
        context = {'name':name,'email':email}
        
        subject = f'Message de {name}' # Le sujet du message
        body = f"""   
        Nom : {name}
        Email : {email}
        Téléphone : {phone}
        Site web : {website}
        Message : {message}
        """    # le corps du message

        from_email = EMAIL_HOST_USER   # adresse du  derstinateur
        recipient_list = email  # adresse expediteur
        send_mail(subject, body,from_email,[recipient_list], fail_silently=False)  # envoie du message
        
        return render(request,'sendmail/confirmation.html',context)
    return render(request,'sendmail/sendmail.html')



# FNCT L'ENVOIE DU MESSAGE DE CONFIRMATION DE COMPTE
@login_required
def confirmation_view(request):
    name = request.GET.get('name')
    email = request.GET.get('email')
    context = {'name':name,'email':email}
    
    return render(request,'sendmail/confirmation.html',context)
