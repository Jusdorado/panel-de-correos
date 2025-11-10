@echo off
echo ========================================
echo Mundosol - Instalacion Automatica
echo ========================================
echo.

REM Verificar Python
echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en el PATH
    echo Descarga Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version

REM Crear entorno virtual
echo.
echo [2/5] Creando entorno virtual...
if exist "venv\" (
    echo Entorno virtual ya existe, omitiendo...
) else (
    python -m venv venv
    echo Entorno virtual creado correctamente
)

REM Activar entorno virtual
echo.
echo [3/5] Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo.
echo [4/5] Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt

REM Configurar .env
echo.
echo [5/5] Configurando archivo .env...
if exist ".env" (
    echo Archivo .env ya existe, omitiendo...
) else (
    copy .env.example .env
    echo.
    echo ========================================
    echo IMPORTANTE: Configuracion requerida
    echo ========================================
    echo.
    echo Se ha creado el archivo .env
    echo.
    echo Debes editar .env y configurar:
    echo   - SECRET_KEY: Clave secreta para Flask
    echo   - DATABASE_URL: Conexion a MySQL
    echo   - N8N_WEBHOOK_URL: URL de tu instancia n8n
    echo   - WEBHOOK_TOKEN: Token de seguridad
    echo.
    echo Ejemplo de DATABASE_URL:
    echo   mysql+pymysql://usuario:contraseña@localhost/mundosol_pedidos
    echo.
)

echo.
echo ========================================
echo Instalacion completada!
echo ========================================
echo.
echo Proximos pasos:
echo   1. Configura MySQL y crea la base de datos
echo   2. Edita el archivo .env con tus credenciales
echo   3. Ejecuta: start.bat
echo.
echo Para mas informacion, consulta INSTALL.md
echo.
pause
