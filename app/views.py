from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView,  TemplateView, View
from .models import Producto, Compra, Usuario
from django.urls import reverse_lazy
from .forms import CompraForm
from django.contrib import messages
from django.db.models import Sum,Count, Max, Avg, Min
from django.contrib.auth.decorators import login_required

# Create your views here.
class ProductoListView(ListView):
    model = Producto
    template_name = 'app/producto/producto_lista.html'
    context_object_name = 'productos'

class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'app/producto/producto_detalle.html'
    context_object_name = 'producto'

class ProductoUpdateView(UpdateView):
    model = Producto

    fields = ['nombre', 'marca', 'modelo', 'unidades', 'precio', 'vip', 'foto']
    template_name = 'app/producto/producto_edit.html'
    context_object_name = 'producto'
    success_url = reverse_lazy('producto_lista')

class CompraListView(ListView):
    model = Producto
    template_name = 'app/compra_lista.html'
    context_object_name = 'productos'


    def get_queryset(self):
        query = super().get_queryset()
        nombre = self.request.GET.get("input_nombre")
        if nombre:
            query = query.filter(nombre__icontains=nombre)
        return query

class CheckoutView(View):
    
    def get(self, request, pk):
        producto = Producto.objects.get(pk = pk)
        form = CompraForm()
        return render(request,"app/checkout.html", {"producto":producto, "form": form})
        


    def post(self, request, pk):
        producto = Producto.objects.get(pk = pk)
        
        form = CompraForm(request.POST)
        if form.is_valid():
            unidades = form.cleaned_data['unidades']

            if producto.unidades < unidades:
                messages.error(request, "No hay suficiente stock")
                
            else:
                # Agregamos la compra
                usuario = request.user
                importe = unidades * producto.precio
                # Comprobamos si el usuario dispone de saldo suficiente
                if usuario.saldo >= importe:
                    Compra.objects.create(usuario = request.user, 
                                        producto = producto, 
                                        unidades = unidades, 
                                        importe = importe,
                                        iva = 0.21)
                    # restamos las unidades del producto
                    producto.unidades -= unidades
                    producto.save()
                    
                    # restamos el importe al saldo del usuario
                    usuario.saldo -= importe
                    usuario.save()

                    messages.success(request, "Guardado correctamente")
                else:
                    messages.error(request,"El usuario no dispone de saldo suficiente")
        return redirect("compra_lista")
    
class PerfilView(TemplateView):
    template_name = "app/perfil.html"


    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        
        contexto['compras'] = Compra.objects.filter(usuario = self.request.user)

        return contexto
         
@login_required
def informes(request):

    topclientes = Usuario.objects.annotate(total_gastado = Sum("compras__importe")).order_by("-total_gastado")[:10]
    topcompras=Usuario.objects.annotate(total_compras=Count("compras")).order_by("-total_compras")[:10]

    estadistica = Compra.objects.aggregate(n_total = Count("id"), total_importe = Sum("importe"), max_importe = Max("importe"), min_importe = Min("importe"), avg_importe = Avg("importe"))

    estadistica_clientes = Usuario.objects.annotate(n_total = Count("compras__id"), 
                                                    total_importe = Sum("compras__importe"), 
                                                    max_importe = Max("compras__importe"), 
                                                    min_importe = Min("compras__importe"), 
                                                    avg_importe = Avg("compras__importe"))
    

    estadistica_usuario=Compra.objects.filter(usuario=request.user).aggregate(
                                                            n_total = Count("id"), 
                                                            total_importe = Sum("importe"), 
                                                            max_importe = Max("importe"), 
                                                            min_importe = Min("importe"), 
                                                            avg_importe = Avg("importe")            
    )
    context={"topclientes":topclientes,"topcompras":topcompras, "estadisticas":estadistica,"estadistica_usuario":estadistica_usuario, "estadistica_clientes": estadistica_clientes}

    


    return render(request, "app/informes.html" ,context)
