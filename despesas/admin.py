from django.contrib import admin
from .models import Category, Bank, Payer, Owner

admin.site.register(Category)
admin.site.register(Bank)
admin.site.register(Payer)
admin.site.register(Owner)