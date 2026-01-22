# 📋 Guía de Deployment - San Vicentino

## ✅ Estado Actual
- ✅ Proyecto funciona localmente
- ✅ Docker está configurado correctamente
- ✅ Base de datos MySQL integrada
- ✅ Todas las rutas funcionan

---

## 🚀 Opción 1: Deployment en AZURE (Recomendado)

### Requisitos:
- Cuenta de Azure (crea una gratis en https://azure.microsoft.com/es-es/free/)
- Azure CLI instalado (`az`)
- Docker Hub account (para hospedar la imagen)

### Pasos:

#### 1️⃣ Crear Image en Docker Hub
```bash
# Login en Docker Hub
docker login

# Tagear la imagen
docker tag sanvicentino-flask:latest tuusuario/sanvicentino:latest

# Subir la imagen
docker push tuusuario/sanvicentino:latest
```

#### 2️⃣ Crear Recursos en Azure
```bash
# Login en Azure
az login

# Crear grupo de recursos
az group create --name sanvicentino-rg --location eastus

# Crear App Service Plan
az appservice plan create \
  --name sanvicentino-plan \
  --resource-group sanvicentino-rg \
  --sku B1 --is-linux

# Crear Web App con contenedor
az webapp create \
  --resource-group sanvicentino-rg \
  --plan sanvicentino-plan \
  --name sanvicentino-app \
  --deployment-container-image-name tuusuario/sanvicentino:latest

# Configurar variables de entorno
az webapp config appsettings set \
  --resource-group sanvicentino-rg \
  --name sanvicentino-app \
  --settings \
    GOOGLE_CLIENT_ID="tu_id" \
    GOOGLE_CLIENT_SECRET="tu_secret" \
    SECRET_KEY="clave_segura" \
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://usuario:password@servidor:3306/sanvicentino"
```

#### 3️⃣ Crear Base de Datos MySQL en Azure
```bash
# Crear servidor MySQL
az mysql server create \
  --resource-group sanvicentino-rg \
  --name sanvicentino-db \
  --admin-user dbadmin \
  --admin-password "Password123!" \
  --sku-name B_Gen5_1 \
  --storage-size 51200

# Crear base de datos
az mysql db create \
  --resource-group sanvicentino-rg \
  --server-name sanvicentino-db \
  --name sanvicentino

# Permitir conexiones desde Azure
az mysql server firewall-rule create \
  --resource-group sanvicentino-rg \
  --server sanvicentino-db \
  --name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

---

## 🚀 Opción 2: Deployment en Heroku (Alternativa)

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Crear app
heroku create sanvicentino

# Setup Procfile
echo "web: python app/run.py" > Procfile

# Agregar MySQL add-on
heroku addons:create jawsdb:kitefin

# Deploy
git push heroku main
```

---

## 📊 Comparativa de Opciones

| Aspecto | Azure | Heroku | DigitalOcean |
|---------|-------|--------|--------------|
| Costo | $5-15/mes | Gratis* | $5+/mes |
| Facilidad | Media | Muy Fácil | Media |
| Escalabilidad | Alta | Limitada | Buena |
| Base de datos | ✅ | ✅ | ✅ |
| SSL/HTTPS | ✅ | ✅ | ✅ |

*Heroku puede ser gratis pero con limitaciones

---

## ⚙️ Variables de Entorno Necesarias

Configura estas variables en tu plataforma de hosting:

```
GOOGLE_CLIENT_ID=tu_id_aqui
GOOGLE_CLIENT_SECRET=tu_secret_aqui
SECRET_KEY=clave_muy_segura_aqui
DB_HOST=servidor_mysql
DB_USER=usuario_db
DB_PASSWORD=password_db
DB_NAME=sanvicentino
FLASK_ENV=production
```

---

## 📝 Notas Importantes

1. **Cambiar `debug=True` a `False`** en producción
2. **Usar variables de entorno** para credenciales
3. **Configurar HTTPS** obligatoriamente
4. **Hacer backup** de la base de datos regularmente
5. **Monitorear logs** en producción

---

## 🆘 Soporte

¿Preguntas? Consulta:
- Documentación Azure: https://docs.microsoft.com/azure/
- Docs de Flask: https://flask.palletsprojects.com/
