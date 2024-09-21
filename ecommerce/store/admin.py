from django.contrib import admin
from .models import Cart,  Order, historiqueAchats
# Register your models here.

class AdminOrder(admin.ModelAdmin):
    list_display = ('product','quantity','prix_total','user','phone_number','ordered_date')
    list_filter = ['product','user','ordered_date']
    search_fields = ['product','user','ordered_date']
    
class Adminhistor(admin.ModelAdmin):
    list_display = ('user','quantity','prix_total','ordered_date')
    list_filter = ['product','user','ordered_date']
    search_fields = ['product','user','ordered_date']
    
admin.site.register(Order, AdminOrder)
admin.site.register(Cart)
admin.site.register(historiqueAchats,Adminhistor)
