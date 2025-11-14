#!/bin/bash

# Script para configurar Docker y panel-de-correos para iniciar automáticamente
# Ejecutar con: sudo bash setup-docker-autostart.sh

set -e

echo "=== Configurando Docker para autostart ==="

# Habilitar servicio Docker
sudo systemctl enable docker
echo "✓ Docker habilitado para iniciar en el arranque"

# Iniciar Docker si no está corriendo
sudo systemctl start docker
echo "✓ Docker iniciado"

# Agregar usuario actual al grupo docker (opcional, para no usar sudo)
if ! groups $USER | grep -q docker; then
    sudo usermod -aG docker $USER
    echo "✓ Usuario agregado al grupo docker (requiere logout/login)"
fi

# Crear servicio systemd para panel-de-correos
echo "=== Creando servicio systemd para panel-de-correos ==="

sudo tee /etc/systemd/system/panel-de-correos.service > /dev/null <<EOF
[Unit]
Description=Panel de Correos Docker Compose
Requires=docker.service
After=docker.service

[Service]
Type=simple
WorkingDirectory=/home/informatica/panel-de-correos
ExecStart=/usr/bin/docker-compose up
ExecStop=/usr/bin/docker-compose down
Restart=always
RestartSec=10
User=informatica
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

echo "✓ Servicio creado en /etc/systemd/system/panel-de-correos.service"

# Recargar systemd
sudo systemctl daemon-reload
echo "✓ Systemd recargado"

# Habilitar servicio
sudo systemctl enable panel-de-correos.service
echo "✓ Servicio habilitado para iniciar en el arranque"

# Iniciar servicio
sudo systemctl start panel-de-correos.service
echo "✓ Servicio iniciado"

echo ""
echo "=== Configuración completada ==="
echo ""
echo "Comandos útiles:"
echo "  Ver estado:        sudo systemctl status panel-de-correos"
echo "  Ver logs:          sudo journalctl -u panel-de-correos -f"
echo "  Detener:           sudo systemctl stop panel-de-correos"
echo "  Reiniciar:         sudo systemctl restart panel-de-correos"
echo ""
