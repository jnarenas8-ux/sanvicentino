#!/usr/bin/env python3
"""
Script para facilitar la configuración de Google OAuth en desarrollo

Opciones:
1. Ver instrucciones para obtener credenciales reales
2. Configurar credenciales en el .env
3. Verificar si OAuth está habilitado
"""

import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
OAUTH_ENABLED = (
    GOOGLE_CLIENT_ID and 
    GOOGLE_CLIENT_SECRET and 
    not GOOGLE_CLIENT_ID.startswith("placeholder") and 
    not GOOGLE_CLIENT_SECRET.startswith("placeholder")
)

def show_menu():
    print("\n" + "="*60)
    print("🔐 CONFIGURADOR DE GOOGLE OAUTH PARA SAN VICENTINO")
    print("="*60)
    print("\n1. ✅ Ver estado de Google OAuth")
    print("2. 📝 Ver instrucciones para obtener credenciales")
    print("3. 🔧 Configurar credenciales en .env")
    print("4. 🚪 Salir\n")

def show_status():
    print("\n" + "-"*60)
    if OAUTH_ENABLED:
        print("✅ GOOGLE OAUTH ESTÁ HABILITADO")
        print(f"   Client ID: {GOOGLE_CLIENT_ID[:20]}...")
        print("\n   Los botones de Google aparecerán en:")
        print("   - Página de Login")
        print("   - Página de Registro")
    else:
        print("❌ GOOGLE OAUTH NO ESTÁ HABILITADO")
        if GOOGLE_CLIENT_ID.startswith("placeholder"):
            print("\n   Razón: Usando valores de desarrollo (placeholder)")
            print("   Necesitas credenciales reales de Google")
        elif not GOOGLE_CLIENT_ID:
            print("\n   Razón: GOOGLE_CLIENT_ID no está configurado")
        else:
            print("\n   Razón: GOOGLE_CLIENT_SECRET no está configurado")
    print("-"*60 + "\n")

def show_instructions():
    print("\n" + "="*60)
    print("📖 INSTRUCCIONES PARA OBTENER CREDENCIALES REALES")
    print("="*60)
    print("""
1. ACCEDER A GOOGLE CLOUD CONSOLE
   👉 https://console.cloud.google.com/

2. CREAR UN NUEVO PROYECTO
   - Haz clic en "Seleccionar un proyecto"
   - Selecciona "NUEVO PROYECTO"
   - Nombre: "San Vicentino"
   - Haz clic en "CREAR"

3. HABILITAR GOOGLE+ API
   - Busca "Google+ API" en el buscador superior
   - Haz clic en ella y presiona "HABILITAR"

4. CREAR CREDENCIALES OAUTH
   - Ve a "Credenciales" en el menú izquierdo
   - Haz clic en "+ CREAR CREDENCIALES"
   - Selecciona "ID de cliente OAuth"
   
   Si aparece "Pantalla de consentimiento":
   - Haz clic en "CONFIGURAR PANTALLA DE CONSENTIMIENTO"
   - Selecciona "Externo"
   - Rellena los campos requeridos
   - Completa todos los pasos

5. CONFIGURAR URI DE REDIRECCIONAMIENTO
   En la sección "Aplicación web", agrega estas URLs:
   - http://localhost:5000/authorize/google
   - http://localhost:8000/authorize/google
   - http://localhost:3000/authorize/google

6. COPIAR CREDENCIALES
   - Copia el "Client ID"
   - Copia el "Client Secret"
   - Pégalos en el archivo .env (opción 3)

7. REINICIAR EL SERVIDOR
   docker compose restart

¡Luego los botones de Google aparecerán automáticamente!
""")
    print("="*60 + "\n")

def configure_env():
    print("\n" + "="*60)
    print("🔧 CONFIGURAR CREDENCIALES")
    print("="*60)
    
    client_id = input("\n📝 Ingresa tu GOOGLE_CLIENT_ID: ").strip()
    if not client_id:
        print("❌ Cliente ID no puede estar vacío")
        return
    
    client_secret = input("📝 Ingresa tu GOOGLE_CLIENT_SECRET: ").strip()
    if not client_secret:
        print("❌ Client Secret no puede estar vacío")
        return
    
    # Leer el archivo .env actual
    env_content = ""
    if env_path.exists():
        with open(env_path, 'r') as f:
            env_content = f.read()
    
    # Actualizar o crear las líneas de configuración
    lines = env_content.split('\n') if env_content else []
    new_lines = []
    oauth_updated = False
    
    for line in lines:
        if line.startswith('GOOGLE_CLIENT_ID='):
            new_lines.append(f'GOOGLE_CLIENT_ID={client_id}')
            oauth_updated = True
        elif line.startswith('GOOGLE_CLIENT_SECRET='):
            new_lines.append(f'GOOGLE_CLIENT_SECRET={client_secret}')
        else:
            new_lines.append(line)
    
    # Si no existían, agregarlos
    if not oauth_updated:
        if new_lines and new_lines[-1] != "":
            new_lines.append("")
        new_lines.extend([
            "# ========================",
            "# GOOGLE OAUTH",
            "# ========================",
            f"GOOGLE_CLIENT_ID={client_id}",
            f"GOOGLE_CLIENT_SECRET={client_secret}"
        ])
    
    # Escribir de vuelta
    with open(env_path, 'w') as f:
        f.write('\n'.join(new_lines))
    
    print("\n✅ Credenciales configuradas exitosamente en .env")
    print("🔄 Reinicia el servidor para que los cambios tomen efecto:")
    print("   docker compose restart")
    print("="*60 + "\n")

def main():
    while True:
        show_menu()
        choice = input("Selecciona una opción (1-4): ").strip()
        
        if choice == "1":
            show_status()
        elif choice == "2":
            show_instructions()
        elif choice == "3":
            configure_env()
        elif choice == "4":
            print("\n👋 ¡Hasta luego!\n")
            break
        else:
            print("\n❌ Opción no válida. Intenta de nuevo.\n")

if __name__ == "__main__":
    main()
