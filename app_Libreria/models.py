#app_Libreria/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Autor(models.Model):
    autorid = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=100)
    fechanacimiento = models.DateField()
    bibliografia = models.TextField()
    paginaweb = models.URLField(blank=True)
    
    class Meta:
        verbose_name_plural = "Autores"
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Editorial(models.Model):
    editorialid = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, unique=True, verbose_name="Nombre Editorial")
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(verbose_name="Email de Contacto")
    sitioweb = models.URLField(blank=True, verbose_name="Sitio Web")
    pais = models.CharField(max_length=50, verbose_name="País de Origen")
    
    class Meta:
        verbose_name_plural = "Editoriales"
    
    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    clienteid = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, blank=True)
    apellido = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    fecharegistro = models.DateTimeField(default=timezone.now)
    preferencias_genero = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Clientes"
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Libro(models.Model):
    GENEROS = [
        ('FIC', 'Ficción'),
        ('ROM', 'Romance'),
        ('TER', 'Terror'),
        ('CIE', 'Ciencia Ficción'),
        ('FAN', 'Fantasía'),
        ('HIS', 'Histórico'),
        ('BIO', 'Biografía'),
        ('INF', 'Infantil'),
    ]
    
    libroid = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    autorid = models.ForeignKey(Autor, on_delete=models.CASCADE, db_column='autorid')
    editorialid = models.ForeignKey(Editorial, on_delete=models.CASCADE, db_column='editorialid')
    isbn = models.CharField(max_length=17, unique=True)
    aniopublicacion = models.IntegerField()
    genero = models.CharField(max_length=100, choices=GENEROS)
    precioventa = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    descripcion = models.TextField(blank=True)
    portada = models.ImageField(upload_to='portadas/', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Libros"
    
    def __str__(self):
        return self.titulo
    
    def disponible(self):
        return self.stock > 0
from decimal import Decimal

class Venta(models.Model):
    METODOS_PAGO = [
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta'),
        ('TRANSFERENCIA', 'Transferencia'),
    ]
    
    ESTADOS_VENTA = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADA', 'Completada'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    ventaid = models.AutoField(primary_key=True)
    clienteid = models.ForeignKey(User, on_delete=models.CASCADE, db_column='clienteid')
    fechaventa = models.DateTimeField(default=timezone.now)
    montototal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    metodopago = models.CharField(max_length=50, choices=METODOS_PAGO)
    estadoventa = models.CharField(max_length=50, choices=ESTADOS_VENTA, default='PENDIENTE')
    descuentoaplicado = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    pagorecibido = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cambio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        verbose_name_plural = "Ventas"
    
    def __str__(self):
        return f"Venta #{self.ventaid} - {self.clienteid.username}"
    
    def calcular_cambio(self):
        if self.pagorecibido and self.pagorecibido >= self.montototal:
            # Convertir ambos a Decimal para la operación
            pagorecibido_decimal = Decimal(str(self.pagorecibido))
            self.cambio = pagorecibido_decimal - self.montototal
        else:
            self.cambio = Decimal('0.00')
        return self.cambio

class DetalleVenta(models.Model):
    detalleventaid = models.AutoField(primary_key=True)
    ventaid = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles', db_column='ventaid')
    libroid = models.ForeignKey(Libro, on_delete=models.CASCADE, db_column='libroid')
    cantidad = models.IntegerField()
    preciounitario = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=5, decimal_places=2, default=0.16)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name_plural = "Detalles de Venta"
    
    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.preciounitario
        super().save(*args, **kwargs)

class Carrito(models.Model):
    carritoid = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    fechaagregado = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name_plural = "Carritos"
    
    def subtotal(self):
        return Decimal(str(self.libro.precioventa)) * self.cantidad

# Agregar modelos faltantes
class Evento(models.Model):
    CATEGORIAS = [
        ('PRESENTACION', 'Presentación de Libro'),
        ('CLUB_LECTURA', 'Club de Lectura'),
        ('TALLER', 'Taller Literario'),
        ('FIRMA', 'Firma de Autores'),
        ('CONFERENCIA', 'Conferencia'),
        ('LANZAMIENTO', 'Lanzamiento'),
        ('INFANTIL', 'Evento Infantil'),
    ]
    
    eventoid = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha = models.DateTimeField()
    ubicacion = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS, default='PRESENTACION')
    capacidad = models.IntegerField(default=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    activo = models.BooleanField(default=True, verbose_name="Evento activo")
    # NO DEBE TENER: activo = models.BooleanField(default=True) ← ELIMINADO
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['fecha']
class Blog(models.Model):
    CATEGORIAS = [
        ('GENERAL', 'General'),
        ('RESENA', 'Reseñas de Libros'),
        ('AUTOR', 'Autores y Escritores'),
        ('EVENTO', 'Eventos Literarios'),
        ('TALLER', 'Talleres y Cursos'),
        ('NOTICIA', 'Noticias Editoriales'),
        ('RECOMENDACION', 'Recomendaciones'),
        ('ENTREVISTA', 'Entrevistas'),
    ]
    
    blogid = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    fechapublicacion = models.DateTimeField(default=timezone.now)
    imagen = models.ImageField(upload_to='blog/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS, default='GENERAL')
    resumen = models.TextField(blank=True, help_text="Resumen breve para mostrar en listados")
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = "Entrada de Blog"
        verbose_name_plural = "Entradas de Blog"
        ordering = ['-fechapublicacion']