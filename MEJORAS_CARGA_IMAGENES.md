# 📸 Mejoras en Carga de Imágenes - Sistema San Vicentino

## Descripción General
Se ha mejorado profesionalmente el sistema de carga de imágenes en los formularios de creación de productos, permitiendo ahora subir archivos desde el disco local además de la opción de URL externa.

## Cambios Realizados

### 1. **Frontend - Nuevos Templates**

#### `crear.html` (Actualizado)
- ✅ Campo de carga de archivo con validación en cliente
- ✅ Vista previa de imagen antes de guardar
- ✅ Opción alternativa de URL
- ✅ Divisor visual entre opciones
- ✅ Estilos mejorados con Tailwind CSS
- ✅ Validación de tipo de archivo (JPG, PNG, GIF, WebP)
- ✅ Validación de tamaño máximo (5MB)
- ✅ Botón para limpiar selección

#### `crear_producto.html` (Actualizado)
- ✅ Mismo sistema mejorado de carga
- ✅ Labels descriptivos con asteriscos para campos obligatorios
- ✅ Interfaz profesional y moderna
- ✅ Manejo de errores con alertas claras

### 2. **Backend - Actualizaciones en `run.py`**

#### Nuevas Importaciones
```python
from werkzeug.utils import secure_filename
from PIL import Image
```

#### Configuración de Uploads
```python
UPLOAD_FOLDER = Path(__file__).parent / "static" / "uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
```

#### Nuevas Funciones Auxiliares

**`allowed_file(filename)`**
- Valida que el archivo tenga una extensión permitida
- Extensiones soportadas: PNG, JPG, JPEG, GIF, WebP

**`save_upload_image(file)`**
- Procesa y guarda la imagen subida
- Funcionalidades:
  - Validación de tipo de archivo
  - Validación de tamaño (máx 5MB)
  - Generación de nombre único (UUID)
  - Optimización de imagen:
    - Conversión RGBA → RGB
    - Redimensionamiento (máx 1920x1080)
    - Compresión JPEG (calidad 85%)
  - Manejo de errores con mensajes al usuario
  - Retorna ruta relativa (`/static/uploads/filename.jpg`)

#### Ruta Actualizada: `crear_producto()`
```python
@app.route('/producto/crear', methods=['GET', 'POST'])
```
- Procesa tanto archivos subidos como URLs externas
- Prioridad: Archivo > URL
- Validación mejorada de datos
- Mensajes de error más descriptivos

### 3. **Dependencias**

#### Nuevo paquete: `Pillow`
- Libería para procesamiento de imágenes
- Optimiza y valida imágenes antes de guardar
- Redimensiona automáticamente si es necesario

Se agregó a `requirements.txt`:
```
Pillow
```

### 4. **Estructura de Archivos**

#### Carpeta de Uploads
```
app/static/uploads/
├── [imagen1].jpg
├── [imagen2].jpg
└── ...
```
- Creada automáticamente en `app/static/uploads/`
- Nombres únicos generados con UUID
- Accesible vía URL: `/static/uploads/[filename]`

## Flujo de Funcionamiento

### Creación de Producto con Archivo:

1. **Usuario selecciona archivo**
   - Validación en cliente (tipo y tamaño)
   - Vista previa mostrada inmediatamente

2. **Submit del formulario**
   - Flask recibe archivo en `request.files['imagen_archivo']`
   - Se llama `save_upload_image(file)`

3. **Procesamiento de imagen**
   - Validación de extensión
   - Validación de tamaño
   - Optimización y redimensionamiento
   - Generación de nombre único

4. **Guardado en BD**
   - Se almacena ruta relativa: `/static/uploads/[uuid].jpg`
   - Se crea producto con imagen

5. **Acceso a imagen**
   - URL de acceso: `/static/uploads/[filename].jpg`
   - Servida como archivo estático por Flask

### Alternativa con URL:

1. Si no se selecciona archivo, se usa la URL proporcionada
2. URL se almacena directamente en BD
3. Se sirve desde servidor externo

## Validaciones

### Cliente (JavaScript)
- ✅ Tipo de archivo (MIME)
- ✅ Tamaño máximo (5MB)
- ✅ Extensión válida

### Servidor (Python)
- ✅ Extensión permitida
- ✅ Tamaño máximo
- ✅ Validación de imagen
- ✅ Manejo de excepciones

## Seguridad

- ✅ Nombres de archivo sanitizados (UUID)
- ✅ Validación de extensión (whitelist)
- ✅ Límite de tamaño (5MB)
- ✅ Validación en servidor (no confiar en cliente)
- ✅ Conversión de RGBA a RGB (evita problemas)
- ✅ Almacenamiento en carpeta dedicada
- ✅ Sin acceso directo a sistema de archivos

## Características Destacadas

### Optimización de Imagen
- Redimensionamiento automático (máx 1920x1080)
- Compresión JPEG (calidad 85%)
- Conversión de formatos (RGBA → RGB)
- Genera imágenes ligeras pero de buena calidad

### Experiencia de Usuario
- Vista previa instantánea
- Validación con mensajes claros
- Opción para cambiar selección
- Interfaz moderna y profesional

### Escalabilidad
- Estructura preparada para múltiples usuarios
- Nombres únicos evitan conflictos
- Sistema de archivos limpio

## Requisitos

- Python 3.7+
- Flask (ya instalado)
- Pillow (nuevo)
- Navegador moderno (HTML5 File API)

## Instalación de Dependencias

```bash
cd app
pip install -r requirements.txt
```

## Testing

### Prueba Manual:
1. Navegar a `/producto/crear`
2. Seleccionar una imagen del disco
3. Ver preview
4. Completar otros campos
5. Hacer clic en "Crear Producto"
6. Verificar que la imagen se guardó en `/static/uploads/`

### Validaciones a probar:
- [ ] Subir archivo válido (JPG, PNG, GIF, WebP)
- [ ] Intentar subir archivo inválido (PDF, TXT)
- [ ] Intentar subir archivo > 5MB
- [ ] Subir con URL en lugar de archivo
- [ ] Usar ambos (debe priorizar archivo)
- [ ] Limpiar selección y volver a intentar

## Cambios Realizados en Archivos

### Archivos Modificados:
1. `/app/templates/crear.html` - Nuevo diseño con carga de archivos
2. `/app/templates/crear_producto.html` - Mismo sistema mejorado
3. `/app/run.py` - Backend para procesar uploads
4. `/app/requirements.txt` - Agregado Pillow

### Archivos Creados:
- `/app/static/uploads/` - Carpeta para imágenes subidas

## Notas Importantes

- Las imágenes se optimizan automáticamente al guardarse
- Se recomienda usar JPG para fotos y PNG para gráficos
- La carpeta `uploads` debe tener permisos de escritura
- En producción, considerar usar servicio de almacenamiento cloud (S3, Azure Blob)
- Los archivos antiguos no se limpian automáticamente (implementar limpieza si necesario)

## Próximos Pasos (Opcional)

- Implementar limpieza de imágenes huérfanas
- Agregar thumbnails para optimizar carga de listados
- Considerar CDN para servir imágenes
- Implementar validación más exhaustiva (exif, metadatos)
- Agregar gallery/carrusel de imágenes por producto
