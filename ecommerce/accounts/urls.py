from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from .views import activate, change_password, deleteHistore, historique_achats,login_user, logout_user, profil, register_user
from .views import profile_edit
from django.contrib.auth import views

app_name ='accounts'

urlpatterns = [
    path('register/',register_user,name='register_user'),
    path('login_user/',login_user,name='login_user'),
    path('logout_user/',logout_user,name='logout_user'),
    
    path('reset_password/',views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),name="reset_password"), # pour la reinitialisation de mot de passe
    path('reset_password_send/',views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_send.html'),name="password_reset_done"), # charger d'envoyer le mail pour la confirmation
    path('reset/<uid64>/<token>', views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),name="password_reset_confirm"),
    path('reset_password_complete',views.PasswordResetCompleteView.as_view(template_name= 'accounts/password_reset_done.html'),name="password_reset_complete"),
    
    path('activate/<uidb64>/<token>',activate,name='activate'),
    path('change-password/', change_password, name='change_password'),
    
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('profil/',profil,name="profil"),
    path('historique/',historique_achats,name="historique_achats"),
    path('deletehistore/>',deleteHistore,name="deletehistore"),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


