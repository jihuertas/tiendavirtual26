from django.urls import path
from .views import *

urlpatterns = [
    #CRUD PRODUCTOS
        path('admin/productos/', ProductoListView.as_view(), name='producto_lista'),
        path('admin/productos/<int:pk>', ProductoDetailView.as_view(), name='producto_detalle'),
        path('admin/productos/<int:pk>/edit', ProductoUpdateView.as_view(), name='producto_edit'),
        
        
    #TIENDA PRODUCTOS  
        path('', CompraListView.as_view(), name='compra_lista'),
        path('checkout/<int:pk>', CheckoutView.as_view(), name='checkout'),

    # Perfil
        path('perfil', PerfilView.as_view(), name='perfil'),

    #Informe
        path('informes', informes, name='informes'),

]
