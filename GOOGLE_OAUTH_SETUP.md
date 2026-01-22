# 🔐 GUÍA: CREAR CREDENCIALES GOOGLE OAUTH 2.0

## Paso 1: Ir a Google Cloud Console
👉 https://console.cloud.google.com/

## Paso 2: Crear un Nuevo Proyecto

1. En la parte superior, haz clic en **"Seleccionar un proyecto"**
2. Haz clic en **"NUEVO PROYECTO"**
3. Nombre: `San Vicentino`
4. Haz clic en **"CREAR"**

Espera a que se cree (toma 1-2 minutos)

---

## Paso 3: Habilitar Google+ API

1. En el buscador superior, escribe: `Google+ API`
2. Haz clic en **"Google+ API"** en los resultados
3. Haz clic en **"HABILITAR"**

Espera a que se habilite (30 segundos)

---

## Paso 4: Crear Credenciales OAuth 2.0

1. En el menú izquierdo, ve a **"Credenciales"**
2. Haz clic en **"+ CREAR CREDENCIALES"**
3. Selecciona **"ID de cliente de OAuth"**

### Si aparece "Pantalla de consentimiento"

1. Haz clic en **"CONFIGURAR PANTALLA DE CONSENTIMIENTO"**
2. Selecciona **"Externo"** (recomendado)
3. Haz clic en **"CREAR"**

Rellena:
- **Nombre de la aplicación:** San Vicentino
- **Correo electrónico de soporte:** tu_email@gmail.com
- **Correo de contacto:** tu_email@gmail.com

4. Haz clic en **"GUARDAR Y CONTINUAR"**
5. En "Permisos", haz clic en **"GUARDAR Y CONTINUAR"**
6. En "Usuarios de prueba", haz clic en **"GUARDAR Y CONTINUAR"**
7. Revisa y haz clic en **"VOLVER AL PANEL"**

---

## Paso 5: Crear ID de Cliente OAuth

1. De nuevo en **"Credenciales"**, haz clic en **"+ CREAR CREDENCIALES"**
2. Selecciona **"ID de cliente de OAuth"**
3. Tipo de aplicación: **"Aplicación web"**

### Rellena los datos:

**Nombre:** San Vicentino Web App

**URIs de origen autorizados (Authorized redirect URIs):**
```
http://localhost:5000
https://sanvicentino-juana.herokuapp.com
```
(Reemplaza "juana" con tu nombre)

4. Haz clic en **"CREAR"**

---

## Paso 6: Copiar las Credenciales

Se abrirá una ventana emergente con:
- **ID de cliente:** ← COPIA ESTO
- **Contraseña de cliente:** ← COPIA ESTO TAMBIÉN

Cópialo en un lugar seguro (Notepad, OneNote, etc.)

---

## Paso 7: Agregar a tu Proyecto

En tu terminal o en Heroku:

```bash
# En local
heroku config:set \
  GOOGLE_CLIENT_ID="aqui_pega_el_id" \
  GOOGLE_CLIENT_SECRET="aqui_pega_el_secret"
```

O en el archivo `.env`:
```
GOOGLE_CLIENT_ID=aqui_pega_el_id
GOOGLE_CLIENT_SECRET=aqui_pega_el_secret
```

---

## ✅ CHECKLIST

- [ ] Proyecto "San Vicentino" creado
- [ ] Google+ API habilitado
- [ ] Pantalla de consentimiento configurada
- [ ] ID de cliente OAuth 2.0 creado
- [ ] URIs de redirección agregados
- [ ] Client ID copiado
- [ ] Client Secret copiado
- [ ] Variables configuradas en Heroku

---

## 🆘 PROBLEMAS COMUNES

### "No me permite crear proyecto"
- Verifica que tengas cuenta Google con tarjeta de crédito
- (No te cobrarán en nivel gratuito)

### "No aparece Google+ API"
- Busca "Google Identity" en lugar de "Google+ API"
- O usa: https://console.cloud.google.com/apis/library/plus.googleapis.com

### "Error: redirect_uri_mismatch"
- Asegúrate que los URIs en Google Cloud coincidan exactamente
- Incluye http:// o https://
- No dejes / al final

### "Credenciales no funcionan"
- Verifica que CLIENT_ID y SECRET sean correctos
- Ten cuidado con espacios en blanco
- Usa comillas correctamente

---

## 🔗 REFERENCIAS

- Google Cloud Console: https://console.cloud.google.com/
- Docs OAuth: https://developers.google.com/identity/protocols/oauth2
- Setup Flask-OAuth: https://authlib.org/integrations/flask-oauth2/

---

¡Listo! Una vez tengas las credenciales, puedes hacer el deploy a Heroku. 🚀
