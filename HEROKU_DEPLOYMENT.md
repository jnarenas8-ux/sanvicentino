# 🚀 PASOS PARA DESPLEGAR EN HEROKU

## Paso 1: Instalar Heroku CLI
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

## Paso 2: Crear cuenta en Heroku (GRATIS)
👉 https://www.heroku.com/

## Paso 3: Iniciar sesión en Heroku
```bash
heroku login
```
Se abrirá el navegador para confirmar. Haz login con tu cuenta.

## Paso 4: Crear aplicación en Heroku
```bash
cd /workspaces/sanvicentino
heroku create sanvicentino-juana
```
(Reemplaza "juana" con tu nombre o apellido para que sea único)

## Paso 5: Agregar base de datos MySQL
```bash
heroku addons:create jawsdb:kitefin --app sanvicentino-juana
```

Esto te dará una URL de conexión a MySQL.

## Paso 6: Establecer variables de entorno
```bash
heroku config:set \
  GOOGLE_CLIENT_ID="tu_client_id_aqui" \
  GOOGLE_CLIENT_SECRET="tu_client_secret_aqui" \
  SECRET_KEY="clave_super_secreta" \
  --app sanvicentino-juana
```

(Obtén el CLIENT_ID y SECRET desde: https://console.cloud.google.com/)

## Paso 7: Ver la URL de base de datos asignada
```bash
heroku config --app sanvicentino-juana
```

Busca la variable `JAWSDB_URL`. Tendrá un formato como:
```
mysql://usuario:password@servidor:3306/database
```

## Paso 8: Actualizar la variable de entorno de conexión
```bash
heroku config:set \
  SQLALCHEMY_DATABASE_URI="$(heroku config:get JAWSDB_URL --app sanvicentino-juana)" \
  --app sanvicentino-juana
```

## Paso 9: Hacer push a Heroku
```bash
git push heroku main
```

Esto iniciará el deploy. Verás los logs en la terminal.

## Paso 10: Ver los logs del deployment
```bash
heroku logs --tail --app sanvicentino-juana
```

## Paso 11: Abrir la aplicación
```bash
heroku open --app sanvicentino-juana
```

¡Tu app estará en vivo! 🎉

---

## 🆘 TROUBLESHOOTING

### Error: "No such app"
Reemplaza `sanvicentino-juana` con el nombre real de tu app.

### Error: "JAWSDB_URL no encontrada"
```bash
heroku config --app sanvicentino-juana
```

### Logs de error en el deploy
```bash
heroku logs --tail --app sanvicentino-juana
```

### Resetear la base de datos
```bash
heroku addons:destroy jawsdb --app sanvicentino-juana --confirm sanvicentino-juana
heroku addons:create jawsdb:kitefin --app sanvicentino-juana
```

### Ver URL de la aplicación
```bash
heroku apps:info --app sanvicentino-juana
```

---

## ✅ CHECKLIST FINAL
export HEROKU_API_KEY=HRKU-AA-DFUx-4WF1BNpcCM-zCk5BUOHlqDTK-QVizwyOCCfA_____wxlKdg6xBDa

- [ ] Heroku CLI instalado
- [ ] Cuenta de Heroku creada
- [ ] App creada en Heroku
- [ ] Base de datos MySQL agregada
- [ ] Variables de entorno configuradas
- [ ] Git push a Heroku completado
- [ ] App accesible en https://sanvicentino-juana.herokuapp.com
- [ ] Login funcionando
- [ ] Base de datos conectada

---

¡Cualquier problema avísame! 🚀
