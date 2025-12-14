# reparar_definitivo.py
import os
import sys
import django
import sqlite3
from decimal import Decimal
import json

print("🛠️  REPARACIÓN DEFINITIVA DE BASE DE DATOS")
print("="*50)

# 1. PRIMERO: Backup de seguridad
db_path = 'db.sqlite3'
backup_path = 'db_backup_pre_reparacion.sqlite3'

if os.path.exists(db_path):
    import shutil
    shutil.copy2(db_path, backup_path)
    print(f"✅ Backup creado: {backup_path}")
else:
    print("❌ No se encontró la base de datos")
    sys.exit(1)

# 2. CONEXIÓN DIRECTA A SQLITE
print("\n🔍 Analizando base de datos...")
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# 3. DIAGNÓSTICO COMPLETO
print("\n📊 DIAGNÓSTICO:")

# Ver todas las tablas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tablas = [row[0] for row in cursor.fetchall()]
print(f"Tablas encontradas: {len(tablas)}")
for tabla in sorted(tablas):
    cursor.execute(f"SELECT COUNT(*) as count FROM {tabla}")
    count = cursor.fetchone()[0]
    print(f"  • {tabla}: {count} registros")

# 4. VERIFICAR TABLA EVENTOS ESPECÍFICAMENTE
print("\n🔍 ANALIZANDO TABLA 'app_libreria_evento':")
cursor.execute("PRAGMA table_info(app_libreria_evento)")
columnas = cursor.fetchall()

print("Columnas de la tabla eventos:")
for col in columnas:
    print(f"  {col[1]} ({col[2]})")

# 5. VER DATOS PROBLEMÁTICOS EN EVENTOS
print("\n🔎 Buscando datos problemáticos en eventos...")
cursor.execute("""
    SELECT eventoid, titulo, precio, typeof(precio) as tipo
    FROM app_libreria_evento 
    WHERE precio IS NULL 
       OR precio = '' 
       OR typeof(precio) != 'real'
       OR precio LIKE '%[a-zA-Z]%'
""")

problemas = cursor.fetchall()
if problemas:
    print(f"⚠️  Encontrados {len(problemas)} registros problemáticos:")
    for p in problemas:
        print(f"  ID {p['eventoid']}: '{p['titulo'][:30]}...' - Valor: '{p['precio']}' - Tipo: {p['tipo']}")
else:
    print("✅ No se encontraron datos problemáticos evidentes")

# 6. VER TODOS LOS EVENTOS
print("\n📋 TODOS LOS EVENTOS (primeros 10):")
cursor.execute("SELECT eventoid, titulo, precio FROM app_libreria_evento LIMIT 10")
todos = cursor.fetchall()
for e in todos:
    print(f"  ID {e['eventoid']}: Precio = {e['precio']} (tipo: {type(e['precio']).__name__})")

# 7. SOLUCIÓN: CREAR TABLA TEMPORAL CON DATOS CORRECTOS
print("\n🔄 CREANDO TABLA TEMPORAL...")

# Crear tabla temporal con estructura corregida
cursor.execute("""
    CREATE TABLE IF NOT EXISTS eventos_temp (
        eventoid INTEGER PRIMARY KEY,
        titulo TEXT,
        descripcion TEXT,
        fecha TEXT,
        ubicacion TEXT,
        imagen TEXT,
        categoria TEXT,
        capacidad INTEGER,
        precio REAL,
        activo BOOLEAN
    )
""")

# 8. COPIAR DATOS CONVIRTIENDO PRECIOS
print("📥 Copiando datos con conversión segura...")

cursor.execute("SELECT * FROM app_libreria_evento")
eventos_originales = cursor.fetchall()

insertados = 0
for evento in eventos_originales:
    try:
        # Convertir precio de forma segura
        precio_original = evento['precio']
        precio_nuevo = 0.0
        
        if precio_original is None:
            precio_nuevo = 0.0
        elif isinstance(precio_original, (int, float)):
            precio_nuevo = float(precio_original)
        elif isinstance(precio_original, str):
            # Limpiar string
            limpio = precio_original.strip()
            if limpio == '':
                precio_nuevo = 0.0
            else:
                # Remover caracteres no numéricos excepto punto
                limpio = ''.join(c for c in limpio if c.isdigit() or c == '.' or c == '-')
                if limpio and limpio.replace('.', '').replace('-', '').isdigit():
                    precio_nuevo = float(limpio) if limpio else 0.0
                else:
                    precio_nuevo = 0.0
        else:
            precio_nuevo = 0.0
        
        # Insertar en tabla temporal
        cursor.execute("""
            INSERT INTO eventos_temp 
            (eventoid, titulo, descripcion, fecha, ubicacion, imagen, categoria, capacidad, precio, activo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            evento['eventoid'],
            evento['titulo'],
            evento['descripcion'],
            evento['fecha'],
            evento['ubicacion'],
            evento['imagen'],
            evento['categoria'],
            evento['capacidad'],
            precio_nuevo,
            evento.get('activo', 1) if 'activo' in evento.keys() else 1
        ))
        insertados += 1
        
    except Exception as e:
        print(f"  ⚠️  Error en evento ID {evento['eventoid']}: {e}")

print(f"✅ {insertados} eventos copiados a tabla temporal")

# 9. REEMPLAZAR TABLA ORIGINAL
print("\n🔄 REEMPLAZANDO TABLA ORIGINAL...")

# Renombrar tabla original (backup)
cursor.execute("ALTER TABLE app_libreria_evento RENAME TO app_libreria_evento_backup")

# Renombrar temporal a original
cursor.execute("ALTER TABLE eventos_temp RENAME TO app_libreria_evento")

# 10. VERIFICAR
print("\n✅ VERIFICACIÓN FINAL:")
cursor.execute("SELECT COUNT(*) FROM app_libreria_evento")
total = cursor.fetchone()[0]
print(f"Total eventos en nueva tabla: {total}")

cursor.execute("SELECT eventoid, titulo, precio FROM app_libreria_evento LIMIT 5")
verificacion = cursor.fetchall()
print("\nPrimeros 5 eventos (precios corregidos):")
for e in verificacion:
    print(f"  ID {e['eventoid']}: '{e['titulo'][:30]}...' - Precio: {e['precio']}")

# Guardar cambios
conn.commit()
conn.close()

print("\n" + "="*50)
print("🎯 REPARACIÓN COMPLETADA")
print("="*50)
print("\n📋 RESUMEN:")
print(f"• Backup creado: {backup_path}")
print(f"• Tabla original respaldada: app_libreria_evento_backup")
print(f"• Tabla nueva creada: app_libreria_evento")
print(f"• Eventos transferidos: {insertados}")
print("\n🚀 AHORA PRUEBA TU SITIO:")
print("python manage.py runserver 1194")
print("http://127.0.0.1:1194/panel-admin/eventos/")