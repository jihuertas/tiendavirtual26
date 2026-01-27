from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Marca, Producto, Compra

class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('foto', 'vip', 'saldo', 'bio')}),
    )
# Register your models here.
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Marca)
admin.site.register(Producto)
admin.site.register(Compra)

