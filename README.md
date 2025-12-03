# Instalación Automática de Docker, Docker Compose, y Evolution API

Este repositorio proporciona un script Bash (`install.sh`) para instalar y configurar Docker, Docker Compose plugin y Evolution API en servidores basados en Ubuntu.

## Requisitos previos

- Sistema operativo: Ubuntu 18.04, 20.04, 22.04, 24.04 (u otra versión compatible con los repositorios oficiales de Docker)
- Acceso con usuario que tenga privilegios de sudo
- Conexión a Internet desde el servidor

## Contenido del repositorio

- `install.sh`: script que automatiza la instalación.

### 1. Descargar o clonar el repositorio

```bash
git clone https://github.com/devalexcode/shell-evolution-api.git
```

### 2. Ingresa a la carpeta del proyecto

```bash
cd shell-evolution-api
```

### 3. Crea el archivo `.env`

```bash
cp .env.example .env
```

**3.1 ⚙️ Configuración del archivo `.env`**

Antes de levantar los servicios, asegúrate de crear y configurar tu archivo `.env`:

```bash
nano .env
```

Edita el archivo `.env` con tus propios valores:

```dotenv
############################################
# Evolution API
############################################

# ------------------------------------------
AUTHENTICATION_API_KEY=api_key # Clave de autenticación para Evolution API (Contraseña de administrador)
# ------------------------------------------
EVOLUTION_API_PORT=8080 # Puerto de escucha para Evolution API
# ------------------------------------------
CONFIG_SESSION_PHONE_VERSION=2.3000.1023204200 # Whatsapp Web version for baileys channel: https://web.whatsapp.com/check-update?version=0&platform=web
# ------------------------------------------

############################################
# PostgreSQL
############################################

# ------------------------------------------
POSTGRESS_USER=user # Usuario de PostgreSQL (POR SEGURIDAD MODIFICA ESTE VALOR)
# ------------------------------------------
POSTGRESS_PASS=123456 # Contraseña de PostgreSQL (POR SEGURIDAD MODIFICA ESTE VALOR)
# ------------------------------------------
POSTGRESS_PORT=5432 # Puerto de PostgreSQL (Se sugiere no modificar)
# ------------------------------------------

############################################
# Redis
############################################

REDIS_PORT=6379 # Puerto de Redis (Se sugiere no modificar)
```

### 4. Dar permisos de ejecución al script

```bash
chmod +x install.sh
```

### 5 Ejecutar el script

```bash
./install.sh
```

- El script actualizará el sistema, instalará Docker y sus herramientas, añadirá el usuario al grupo `docker` desplegará n8n, Evolution API y Portainer.

![Shell instalacion](docs/shell.png)

## Ingresar a Evolution API

Al finalizar, verás un mensaje indicando la URL de acceso a Evolution API:

```bash
¡Instalación completada! Evolution API funcionando y accesible: http://<IP_DEL_SERVIDOR>:EVOLUTION_API_PORT/manager
```

![Login Evolution API](docs/Evolution-API-login.png)

¡Listo! Con estos pasos tu servidor quedará con Evolution API instalado.

## 👨‍💻 Autor

Desarrollado por [Alejandro Robles | Devalex ](http://devalexcode.com)  
¿Necesitas que lo haga por ti? ¡Estoy para apoyarte! 🤝 https://devalexcode.com/soluciones/evolution-api-whatsapp-en-servidor-vps

¿Dudas o sugerencias? ¡Contribuciones bienvenidas!
