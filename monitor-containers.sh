#!/bin/bash

# Script de monitoreo para verificar que los contenedores estén corriendo
# Ejecutar con: bash monitor-containers.sh

LOG_FILE="/home/informatica/panel-de-correos/logs/monitor.log"
mkdir -p "$(dirname "$LOG_FILE")"

check_containers() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Verificar MySQL
    if docker ps | grep -q panel-mysql; then
        mysql_status="✓ RUNNING"
    else
        mysql_status="✗ STOPPED"
    fi
    
    # Verificar Panel
    if docker ps | grep -q panel-correos; then
        panel_status="✓ RUNNING"
    else
        panel_status="✗ STOPPED"
    fi
    
    # Escribir en log
    echo "[$timestamp] MySQL: $mysql_status | Panel: $panel_status" >> "$LOG_FILE"
    
    # Si alguno está detenido, intentar reiniciar
    if [[ "$mysql_status" == "✗ STOPPED" ]] || [[ "$panel_status" == "✗ STOPPED" ]]; then
        echo "[$timestamp] ⚠ Contenedor detenido detectado, reiniciando..." >> "$LOG_FILE"
        cd /home/informatica/panel-de-correos
        docker-compose up -d
    fi
}

# Ejecutar verificación cada 5 minutos
while true; do
    check_containers
    sleep 300
done
