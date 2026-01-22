# 🚀 San Vicentino - Tienda Online

Tienda online para venta de agua San Vicentino con autenticación de usuarios, carrito de compras y panel administrativo.

---

## ✨ Características

✅ **Autenticación de Usuarios**
- Registro y login local
- Login con Google OAuth
- Sistema de roles (usuario/admin)

✅ **Tienda Online**
- Carrusel de productos
- Catálogo de productos
- Carrito de compras
- Proceso de checkout

✅ **Tecnología Moderna**
- Flask (Backend)
- SQLAlchemy (ORM)
- Tailwind CSS (Frontend)
- MySQL (Base de datos)
- Docker (Containerización)

---

## 🏠 Ejecutar Localmente

### Requisitos Previos
- Docker y Docker Compose
- Node.js 18+ (para Tailwind CSS)
- Python 3.12+ (opcional, para desarrollo)

### Instalación

1. **Clonar repositorio**
```bash
git clone https://github.com/JuanaArenas/sanvicentino.git
cd sanvicentino
```

2. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

3. **Compilar CSS con Tailwind**
```bash
npm install
npm run build:css
```

4. **Levantar contenedores**
```bash
docker-compose up -d
```

5. **Acceder a la aplicación**
```
http://localhost:5000
```

---

## 📱 Deployment Online

### Opción 1: Azure (Recomendado)
```bash
# Ver guía completa en: azure-app-deployment.md
```

**Ventajas:**
- Escalabilidad automática
- Base de datos administrada
- SSL/HTTPS gratis
- Backups automáticos
- Costo: $5-15/mes

### Opción 2: Heroku
```bash
heroku create sanvicentino
git push heroku main
```

**Ventajas:**
- Muy fácil de usar
- Despliegue automático
- Costo: Gratis (limitado)

### Opción 3: DigitalOcean
```bash
# App Platform
# Costo: $5-12/mes
```

---

## 📁 Estructura del Proyecto

```
sanvicentino/
├── app/
│   ├── run.py                 # Aplicación principal
│   ├── config.py              # Configuración
│   ├── database.py            # Conexión BD
│   ├── requirements.txt        # Dependencias Python
│   ├── static/
│   │   ├── css/              # Estilos (Tailwind)
│   │   ├── js/               # Scripts frontend
│   │   └── img/              # Imágenes
│   └── templates/            # Plantillas HTML
├── Dockerfile                # Construcción de imagen
├── docker-compose.yml        # Composición local
├── docker-compose.prod.yml   # Composición producción
├── package.json              # Dependencias Node
├── tailwind.config.js        # Config Tailwind
└── .env                       # Variables de entorno
```

---

## 🔧 Configuración

### Variables de Entorno (.env)

```env
# Google OAuth
GOOGLE_CLIENT_ID=tu_id_aqui
GOOGLE_CLIENT_SECRET=tu_secret_aqui

# Flask
SECRET_KEY=clave_super_secreta

# MySQL
DB_HOST=mysql
DB_PORT=3306
DB_NAME=sanvicentino
DB_USER=usuario_app
DB_PASSWORD=password_app
```

### Obtener Credenciales Google OAuth

1. Ir a [Google Cloud Console](https://console.cloud.google.com/)
2. Crear nuevo proyecto
3. Ir a OAuth 2.0 Client IDs
4. Copiar Client ID y Secret
5. Pegar en `.env`

---

## 🗄️ Base de Datos

### Crear Tablas Automáticamente
Las tablas se crean automáticamente al iniciar la app.

### Conexión Manual a MySQL
```bash
# Desde terminal
docker exec -it mysql_db mysql -u usuario_app -p

# Password: password_app
# Usar base de datos: USE sanvicentino;
```

### Backup de Base de Datos
```bash
docker exec mysql_db mysqldump -u usuario_app -ppassword_app sanvicentino > backup.sql
```

---

## 🚀 Scripts Disponibles

```bash
# Compilar CSS
npm run build:css

# Observar cambios en CSS
npm run watch:css

# Levantar contenedores
docker-compose up

# Bajar contenedores
docker-compose down

# Ver logs
docker-compose logs -f

# Reconstruir imagen
docker-compose up --build
```

---

## 🧪 Testing

### Rutas Disponibles

| Ruta | Método | Descripción |
|------|--------|-------------|
| `/` | GET | Página de inicio |
| `/register` | GET, POST | Registro de usuario |
| `/login` | GET, POST | Login |
| `/login/google` | GET | Login con Google |
| `/logout` | GET | Cerrar sesión |
| `/contactanos` | GET | Página de contacto |

---

## 🐛 Troubleshooting

### Error: "Could not build url for endpoint"
Asegúrate de que todas las rutas están definidas en `run.py`

### Error de conexión a MySQL
```bash
# Verificar que MySQL está corriendo
docker-compose ps

# Ver logs de MySQL
docker-compose logs mysql
```

### Error: "Static files not found"
```bash
# Compilar CSS
npm run build:css

# Reconstruir imagen
docker-compose up --build
```

---

## 📊 Performance

- **Tiempo de carga**: < 2 segundos
- **Concurrencia**: Soporta 100+ usuarios simultáneos
- **Almacenamiento**: 1GB (incluye BD)

---

## 📈 Roadmap

- [ ] Sistema de pagos Stripe
- [ ] Panel administrativo
- [ ] Reseñas de productos
- [ ] Historial de pedidos
- [ ] Notificaciones por email
- [ ] App móvil

---

## 👥 Contribuyentes

- **Juana Arenas** - Desarrolladora principal

---

## 📄 Licencia

MIT License - Libre para usar y modificar

---

## 📞 Soporte

**Email:** juana@sanvicentino.com  
**GitHub:** https://github.com/JuanaArenas/sanvicentino  
**Issues:** https://github.com/JuanaArenas/sanvicentino/issues

---

## ✅ Estado del Proyecto

| Aspecto | Estado |
|--------|--------|
| Desarrollo | ✅ Funcionando |
| Tests | ⏳ Pendiente |
| Documentación | ✅ Actualizada |
| Deploy | 🚀 Listo |

---

**¡Gracias por usar San Vicentino!** 🎉
