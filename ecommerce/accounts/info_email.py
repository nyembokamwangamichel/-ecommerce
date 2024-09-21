

# TOUTES INFORMATIONS QUI SONT RELIEES  ( envoi et reception du mail)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'      # le protocol pour l'envoie de mail sur (smtp) 
EMAIL_HOST = 'smtp.gmail.com'     #  serveur SMTP pour l'envoie de mail
EMAIL_PORT = 587     # numéro de port du protocol 
EMAIL_USE_TLS = True  # je mets  à true parce que j'utilise  EMAIL_USE_TLS 
EMAIL_HOST_USER = 'michelnyembo28@gmail.com'  # l'addresse mail qui sera utilisée par l'application
EMAIL_HOST_PASSWORD = 'yvevpbhlwoipqqis'   # le mot de passe  pour le compte gmail de l'adresse qui est utilisée par l'application


