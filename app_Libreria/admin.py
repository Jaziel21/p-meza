# app_Libreria/admin.py
from django.contrib import admin
from .models import Evento, Blog, Libro, Autor, Editorial, Venta, DetalleVenta, Carrito, Cliente
@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ['autorid', 'nombre', 'apellido', 'nacionalidad', 'fechanacimiento']
    list_filter = ['nacionalidad']
    search_fields = ['nombre', 'apellido']
    ordering = ['nombre', 'apellido']

@admin.register(Editorial)
class EditorialAdmin(admin.ModelAdmin):
    list_display = ['editorialid', 'nombre', 'telefono', 'email', 'pais']
    list_filter = ['pais']
    search_fields = ['nombre', 'direccion']
    ordering = ['nombre']

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['clienteid', 'user', 'telefono', 'fecharegistro']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    list_filter = ['fecharegistro']
    readonly_fields = ['fecharegistro']

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ['libroid', 'titulo', 'autorid', 'editorialid', 'precioventa', 'stock', 'aniopublicacion', 'disponible']
    list_filter = ['genero', 'aniopublicacion', 'editorialid']
    search_fields = ['titulo', 'autorid__nombre', 'autorid__apellido']
    ordering = ['titulo']
    readonly_fields = ['disponible']

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['ventaid', 'clienteid', 'fechaventa', 'montototal', 'metodopago', 'estadoventa']
    list_filter = ['estadoventa', 'metodopago', 'fechaventa']
    search_fields = ['clienteid__username', 'ventaid']
    readonly_fields = ['fechaventa', 'montototal', 'cambio']
    ordering = ['-fechaventa']

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ['detalleventaid', 'ventaid', 'libroid', 'cantidad', 'preciounitario', 'subtotal']
    list_filter = ['ventaid__fechaventa']
    search_fields = ['libroid__titulo', 'ventaid__ventaid']
    readonly_fields = ['subtotal']

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ['carritoid', 'usuario', 'libro', 'cantidad', 'fechaagregado']
    list_filter = ['fechaagregado']
    search_fields = ['usuario__username', 'libro__titulo']
    readonly_fields = ['fechaagregado']

# CORREGIR la clase EventoAdmin
class EventoAdmin(admin.ModelAdmin):
    list_display = ('eventoid', 'titulo', 'fecha', 'categoria', 'ubicacion')  # QUITAR 'activo'
    list_filter = ('categoria', 'fecha')  # QUITAR 'activo'
    search_fields = ('titulo', 'descripcion', 'ubicacion')
    ordering = ('-fecha',)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['blogid', 'titulo', 'autor', 'fechapublicacion', 'activo']
    list_filter = ['fechapublicacion', 'activo']
    search_fields = ['titulo', 'contenido']
