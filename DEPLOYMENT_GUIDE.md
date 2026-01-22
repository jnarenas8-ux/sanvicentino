# 🚀 GUÍA RÁPIDA DE DEPLOYMENT

## ✅ Lo que se hizo

1. ✅ Configuró variables de entorno (.env)
2. ✅ Instaló todas las dependencias
3. ✅ Compiló CSS con Tailwind
4. ✅ Levantó docker-compose con MySQL + Flask
5. ✅ Corrigió ruta faltante (/contactanos)
6. ✅ Verificó que la aplicación funciona en localhost:5000

---

## 🌐 DEPLOYMENT ONLINE EN 10 MINUTOS

### Opción A: HEROKU (Más Fácil)

```bash
# 1. Instalar Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# 2. Crear cuenta Heroku (gratis)
# https://www.heroku.com

# 3. Crear archivo Procfile
echo "web: python app/run.py" > Procfile

# 4. Hacer git commit
git add .
git commit -m "Preparado para deploy"

# 5. Crear app en Heroku
heroku login
heroku create sanvicentino-tuapellido

# 6. Agregar base de datos
heroku addons:create jawsdb:kitefin

# 7. Deploy
git push heroku main

# 8. Ver logs
heroku logs --tail
```

**URL Final:** https://sanvicentino-tuapellido.herokuapp.com

---

### Opción B: AZURE (Más Potente)

```bash
# 1. Instalar Azure CLI
# https://docs.microsoft.com/cli/azure/install-azure-cli

# 2. Crear cuenta Azure (gratis por 1 año)
# https://azure.microsoft.com/es-es/free/

# 3. Login
az login

# 4. Crear grupo de recursos
az group create --name sanvicentino-rg --location eastus

# 5. Crear App Service Plan
az appservice plan create \
  --name sanvicentino-plan \
  --resource-group sanvicentino-rg \
  --sku B1 --is-linux

# 6. Crear Web App
az webapp create \
  --resource-group sanvicentino-rg \
  --plan sanvicentino-plan \
  --name sanvicentino-app \
  -i mcr.microsoft.com/azure-app-service/python:3.12

# 7. Configurar env
az webapp config appsettings set \
  --resource-group sanvicentino-rg \
  --name sanvicentino-app \
  --settings \
    WEBSITES_PORT=5000 \
    GOOGLE_CLIENT_ID="tu_id" \
    GOOGLE_CLIENT_SECRET="tu_secret"

# 8. Deploy
az webapp deployment source config --name sanvicentino-app \
  --resource-group sanvicentino-rg \
  --repo-url https://github.com/JuanaArenas/sanvicentino \
  --branch main --manual-integration
```

**URL Final:** https://sanvicentino-app.azurewebsites.net

---

### Opción C: DIGITALOCEAN (Recomendado Precio/Calidad)

```bash
# 1. Crear cuenta DigitalOcean
# https://www.digitalocean.com

# 2. Crear App
# - Conectar repo GitHub
# - Seleccionar Dockerfile
# - Seleccionar región

# 3. Agregar base de datos MySQL
# - Add Component → Database → MySQL

# 4. Deploy automático
# Cada push a main hace deploy automático
```

---

## 🎯 PRÓXIMOS PASOS

1. **Elegir plataforma** (Heroku es la más rápida)
2. **Crear cuenta** en la plataforma elegida
3. **Seguir los pasos** de la opción elegida
4. **Configurar credenciales de Google**
   - Ir a: https://console.cloud.google.com/
   - Crear OAuth credentials
   - Agregar URL de la app
5. **Actualizar .env** en la plataforma
6. **Testear la app** en producción

---

## 🆘 PROBLEMAS COMUNES

### "No funciona la base de datos en producción"
**Solución:** Agregar URL de conexión correcta en la plataforma

### "Error 500"
**Solución:** Ver logs con:
- Heroku: `heroku logs --tail`
- Azure: Portal Azure → Logs
- DigitalOcean: Dashboard → Logs

### "Imágenes no se ven"
**Solución:** Agregar archivos a carpeta `/app/static/img/`

### "Login de Google no funciona"
**Solución:** 
- Agregar URL de callback en Google Cloud Console
- Formato: `https://tuapp.com/authorize/google`

---

## 📊 COMPARATIVA FINAL

| Factor | Heroku | Azure | DigitalOcean |
|--------|--------|-------|--------------|
| Tiempo de setup | 5 min | 15 min | 10 min |
| Costo inicial | Gratis | $5/mes | $5/mes |
| Escalabilidad | Baja | Alta | Media |
| Facilidad | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## ✨ RECOMENDACIÓN FINAL

👉 **Comienza con HEROKU** por su simplicidad. Luego migra a Azure/DigitalOcean cuando necesites más usuarios.

---

**¡Tu app está lista para volar! 🚀**
