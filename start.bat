@echo off
echo ========================================
echo Mundosol - Sistema de Gestion de Pedidos
echo ========================================
echo.

REM Verificar si existe el entorno virtual
if not exist "venv\" (
    echo [ERROR] No se encontro el entorno virtual.
    echo Por favor ejecuta primero: python -m venv venv
    echo.
    pause
    exit /b 1
)

REM Activar entorno virtual
echo [1/3] Activando entorno virtual...
call venv\Scripts\activate.bat

REM Verificar si existe .env
if not exist ".env" (
    echo.
    echo [ADVERTENCIA] No se encontro archivo .env
    echo Copiando .env.example a .env...
    copy .env.example .env
    echo.
    echo [IMPORTANTE] Edita el archivo .env con tus credenciales antes de continuar.
    echo Presiona cualquier tecla cuando hayas configurado .env...
    pause
)

REM Ejecutar aplicación
echo.
echo [2/3] Verificando dependencias...
pip install -q -r requirements.txt

echo.
echo [3/3] Iniciando servidor Mundosol...
echo.
python run.py

pause
