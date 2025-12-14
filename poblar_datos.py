# poblar_datos.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tu_proyecto.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from tu_app.models import Editorial, Autor, Libro, Evento, Blog, Usuario, Pedido, DetallePedido

def poblar_datos():
    # Limpiar datos existentes (opcional)
    print("🧹 Limpiando datos existentes...")
    Editorial.objects.all().delete()
    Autor.objects.all().delete()
    Libro.objects.all().delete()
    Evento.objects.all().delete()
    Blog.objects.all().delete()
    Usuario.objects.all().delete()
    Pedido.objects.all().delete()
    
    # Crear editoriales
    print("📚 Creando editoriales...")
    editoriales_data = [
        {'nombre': 'Penguin Random House', 'pais': 'Estados Unidos', 'telefono': '+1-555-0101', 'email': 'contacto@penguin.com'},
        {'nombre': 'Editorial Planeta', 'pais': 'España', 'telefono': '+34-915-555-123', 'email': 'info@planeta.es'},
        {'nombre': 'Alfaguara', 'pais': 'México', 'telefono': '+52-55-1234-5678', 'email': 'contacto@alfaguara.mx'},
        {'nombre': 'Anaya', 'pais': 'España', 'telefono': '+34-913-555-789', 'email': 'ventas@anaya.es'},
        {'nombre': 'Fondo de Cultura Económica', 'pais': 'México', 'telefono': '+52-55-5678-9012', 'email': 'fce@fondodecultura.com'},
    ]
    
    for editorial_data in editoriales_data:
        Editorial.objects.create(**editorial_data)
    
    # Crear autores
    print("👨‍💻 Creando autores...")
    autores_data = [
        {'nombre': 'Gabriel García Márquez', 'nacionalidad': 'Colombiano', 'fecha_nacimiento': '1927-03-06', 'biografia': 'Premio Nobel de Literatura 1982'},
        {'nombre': 'Isabel Allende', 'nacionalidad': 'Chilena', 'fecha_nacimiento': '1942-08-02', 'biografia': 'Conocida por La casa de los espíritus'},
        {'nombre': 'Carlos Ruiz Zafón', 'nacionalidad': 'Español', 'fecha_nacimiento': '1964-09-25', 'biografia': 'Autor de La sombra del viento'},
        {'nombre': 'Laura Gallego', 'nacionalidad': 'Española', 'fecha_nacimiento': '1977-10-11', 'biografia': 'Autora de Memorias de Idhún'},
        {'nombre': 'Jorge Luis Borges', 'nacionalidad': 'Argentino', 'fecha_nacimiento': '1899-08-24', 'biografia': 'Uno de los autores más destacados'},
    ]
    
    for autor_data in autores_data:
        Autor.objects.create(**autor_data)
    
    # Crear libros
    print("📖 Creando libros...")
    editorial_penguin = Editorial.objects.get(nombre='Penguin Random House')
    editorial_planeta = Editorial.objects.get(nombre='Editorial Planeta')
    editorial_alfaguara = Editorial.objects.get(nombre='Alfaguara')
    editorial_anaya = Editorial.objects.get(nombre='Anaya')
    editorial_fce = Editorial.objects.get(nombre='Fondo de Cultura Económica')
    
    autor_marquez = Autor.objects.get(nombre='Gabriel García Márquez')
    autor_allende = Autor.objects.get(nombre='Isabel Allende')
    autor_ruiz_zafon = Autor.objects.get(nombre='Carlos Ruiz Zafón')
    autor_gallego = Autor.objects.get(nombre='Laura Gallego')
    autor_borges = Autor.objects.get(nombre='Jorge Luis Borges')
    
    libros_data = [
        {'titulo': 'Cien años de soledad', 'isbn': '978-8437604947', 'fecha_publicacion': '1967-05-30', 'precio': 450.00, 'stock': 25, 'descripcion': 'La obra maestra del realismo mágico', 'editorial': editorial_penguin, 'autor': autor_marquez, 'imagen': 'cien_anos_soledad.jpg'},
        {'titulo': 'La sombra del viento', 'isbn': '978-8408094352', 'fecha_publicacion': '2001-04-05', 'precio': 380.00, 'stock': 18, 'descripcion': 'Una novela de misterio en Barcelona', 'editorial': editorial_planeta, 'autor': autor_ruiz_zafon, 'imagen': 'sombra_viento.jpg'},
        {'titulo': 'La casa de los espíritus', 'isbn': '978-8466337102', 'fecha_publicacion': '1982-01-01', 'precio': 420.00, 'stock': 15, 'descripcion': 'Crónica de una familia latinoamericana', 'editorial': editorial_alfaguara, 'autor': autor_allende, 'imagen': 'casa_espiritus.jpg'},
        {'titulo': 'Memorias de Idhún: La Resistencia', 'isbn': '978-8467500123', 'fecha_publicacion': '2004-10-01', 'precio': 320.00, 'stock': 20, 'descripcion': 'Trilogía fantástica', 'editorial': editorial_anaya, 'autor': autor_gallego, 'imagen': 'memorias_idhun.jpg'},
    ]
    
    for libro_data in libros_data:
        Libro.objects.create(**libro_data)
    
    # Crear usuarios
    print("👥 Creando usuarios...")
    usuarios_data = [
        {'nombre': 'Admin Principal', 'email': 'admin@libreria.com', 'password': make_password('password123'), 'rol': 'admin', 'telefono': '555-1234', 'direccion': 'Av. Principal 123'},
        {'nombre': 'Carlos López', 'email': 'carlos@email.com', 'password': make_password('password123'), 'rol': 'usuario', 'telefono': '555-5678', 'direccion': 'Calle Secundaria 456'},
    ]
    
    for usuario_data in usuarios_data:
        Usuario.objects.create(**usuario_data)
    
    print("✅ ¡Datos creados exitosamente!")
    print("📧 Admin: admin@libreria.com")
    print("🔑 Contraseña: password123")

if __name__ == '__main__':
    poblar_datos()