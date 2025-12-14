from django.urls import path
from . import views

urlpatterns = [
    # Páginas públicas
    path('', views.inicio, name='inicio'),
    path('libros/', views.libros, name='libros'),
    path('eventos/', views.eventos, name='eventos'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:blog_id>/', views.detalle_blog, name='detalle_blog'),  # <-- NUEVA URL
    path('contacto/', views.contacto, name='contacto'),

    
    # Autenticación
    path('login/', views.login_selector, name='login_selector'),
    path('login/cliente/', views.login_cliente, name='login_cliente'),
    path('login/admin/', views.login_admin, name='login_admin'),
    path('logout/', views.logout_view, name='logout'),    
    # Panel administrador
    path('panel-admin/', views.panel_admin, name='panel_admin'),
    
    # CRUD Autores (admin)
    path('panel-admin/autores/', views.admin_autores, name='admin_autores'),
    path('panel-admin/autores/agregar/', views.agregar_autor, name='agregar_autor'),
    path('panel-admin/autores/editar/<int:id>/', views.editar_autor, name='editar_autor'),
    path('panel-admin/autores/eliminar/<int:id>/', views.eliminar_autor, name='eliminar_autor'),
    
    # CRUD Editoriales (admin)
    path('panel-admin/editoriales/', views.admin_editoriales, name='admin_editoriales'),
    path('panel-admin/editoriales/agregar/', views.agregar_editorial, name='agregar_editorial'),
    path('panel-admin/editoriales/editar/<int:id>/', views.editar_editorial, name='editar_editorial'),
    path('panel-admin/editoriales/eliminar/<int:id>/', views.eliminar_editorial, name='eliminar_editorial'),
    
    # CRUD Libros (admin)
    path('panel-admin/libros/', views.admin_libros, name='admin_libros'),
    path('panel-admin/libros/agregar/', views.agregar_libro, name='agregar_libro'),
    path('panel-admin/libros/editar/<int:id>/', views.editar_libro, name='editar_libro'),
    path('panel-admin/libros/eliminar/<int:id>/', views.eliminar_libro, name='eliminar_libro'),
    
    # CRUD Ventas (admin)
    path('panel-admin/ventas/', views.admin_ventas, name='admin_ventas'),
    path('panel-admin/ventas/agregar/', views.agregar_venta, name='agregar_venta'),
    path('panel-admin/ventas/editar/<int:id>/', views.editar_venta, name='editar_venta'),
    path('panel-admin/ventas/eliminar/<int:id>/', views.eliminar_venta, name='eliminar_venta'),
    path('panel-admin/ventas/<int:venta_id>/', views.detalle_venta_admin, name='detalle_venta_admin'),
    path('panel-admin/ventas/cancelar/<int:venta_id>/', views.cancelar_venta, name='cancelar_venta'),
    
    # CRUD Detalles Venta (admin)
    path('panel-admin/detalles-venta/', views.admin_detalles_venta, name='admin_detalles_venta'),
    path('panel-admin/detalles-venta/agregar/', views.agregar_detalle_venta, name='agregar_detalle_venta'),
    path('panel-admin/detalles-venta/editar/<int:id>/', views.editar_detalle_venta, name='editar_detalle_venta'),
    path('panel-admin/detalles-venta/eliminar/<int:id>/', views.eliminar_detalle_venta, name='eliminar_detalle_venta'),
    
    # CRUD Eventos (admin)
    path('panel-admin/eventos/', views.admin_eventos, name='admin_eventos'),
    path('panel-admin/eventos/agregar/', views.agregar_evento, name='agregar_evento'),
    path('panel-admin/eventos/editar/<int:id>/', views.editar_evento, name='editar_evento'),
    path('panel-admin/eventos/eliminar/<int:id>/', views.eliminar_evento, name='eliminar_evento'),

    # CRUD Blog (admin)
    path('panel-admin/blog/', views.admin_blog, name='admin_blog'),
    path('panel-admin/blog/agregar/', views.agregar_entrada_blog, name='agregar_entrada_blog'),
    path('panel-admin/blog/editar/<int:id>/', views.editar_entrada_blog, name='editar_entrada_blog'),
    path('panel-admin/blog/eliminar/<int:id>/', views.eliminar_entrada_blog, name='eliminar_entrada_blog'),
    
    
    # Carrito y compras (cliente)
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:libro_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:carrito_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/procesar/', views.procesar_compra, name='procesar_compra'),
    path('carrito/detalle/<int:venta_id>/', views.detalle_venta, name='detalle_venta'),
    path('carrito/mis-compras/', views.mis_compras, name='mis_compras'),
    path('carrito/actualizar/<int:carrito_id>/', views.actualizar_carrito, name='actualizar_carrito'),
]