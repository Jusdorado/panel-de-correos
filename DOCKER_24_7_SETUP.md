# Configuración Docker 24/7 - Panel de Correos

## Resumen de cambios

Tu Docker ahora está configurado para:
- ✅ Reiniciarse automáticamente si falla
- ✅ Iniciarse automáticamente al encender la máquina
- ✅ Funcionar 24/7 sin interrupciones

## Cambios realizados

### 1. docker-compose.yml
- Cambio de `restart: unless-stopped` a `restart: always`
- Agregada versión explícita `3.8`
- Agregados límites de recursos para estabilidad

### 2. Scripts creados

#### setup-docker-autostart.sh
Configura Docker y crea un servicio systemd para autostart.

**Ejecutar una sola vez:**
```bash
sudo bash /home/informatica/panel-de-correos/setup-docker-autostart.sh
```

#### monitor-containers.sh
Monitorea los contenedores cada 5 minutos y reinicia si es necesario.

**Ejecutar en background:**
```bash
bash /home/informatica/panel-de-correos/monitor-containers.sh &
```

## Pasos de instalación

### Paso 1: Ejecutar setup (requiere sudo)
```bash
cd /home/informatica/panel-de-correos
sudo bash setup-docker-autostart.sh
```

### Paso 2: Verificar estado
```bash
sudo systemctl status panel-de-correos
```

### Paso 3: Ver logs
```bash
sudo journalctl -u panel-de-correos -f
```

## Comandos útiles

### Ver estado del servicio
```bash
sudo systemctl status panel-de-correos
```

### Ver logs en tiempo real
```bash
sudo journalctl -u panel-de-correos -f
```

### Detener servicio
```bash
sudo systemctl stop panel-de-correos
```

### Reiniciar servicio
```bash
sudo systemctl restart panel-de-correos
```

### Ver logs históricos
```bash
sudo journalctl -u panel-de-correos --since "2 hours ago"
```

### Ver contenedores corriendo
```bash
docker ps
```

### Ver logs de un contenedor específico
```bash
docker logs -f panel-correos
docker logs -f panel-mysql
```

## Configuración de N8N (si aplica)

Si tienes N8N corriendo, asegúrate de que también tenga:
```yaml
restart: always
```

En su docker-compose.yml.

## Verificación

Después de ejecutar el setup, verifica:

1. **Docker inicia automáticamente:**
   ```bash
   sudo systemctl is-enabled docker
   # Debe mostrar: enabled
   ```

2. **Panel inicia automáticamente:**
   ```bash
   sudo systemctl is-enabled panel-de-correos
   # Debe mostrar: enabled
   ```

3. **Contenedores están corriendo:**
   ```bash
   docker ps
   # Debe mostrar panel-mysql y panel-correos
   ```

## Troubleshooting

### Los contenedores no inician
```bash
# Ver logs detallados
sudo journalctl -u panel-de-correos -n 50

# Reintentar manualmente
sudo systemctl restart panel-de-correos
```

### Docker no inicia al encender
```bash
# Verificar que Docker está habilitado
sudo systemctl is-enabled docker

# Si no está habilitado:
sudo systemctl enable docker
```

### Contenedor se detiene constantemente
```bash
# Ver logs del contenedor
docker logs panel-correos

# Verificar recursos disponibles
free -h
df -h
```

## Monitoreo adicional (opcional)

Para mayor seguridad, ejecuta el script de monitoreo:

```bash
# En background
bash /home/informatica/panel-de-correos/monitor-containers.sh &

# O crear un servicio systemd para él también
```

## Notas importantes

- El cambio de `unless-stopped` a `always` significa que los contenedores se reiniciarán incluso si los detuviste manualmente
- Si necesitas detener los contenedores permanentemente, usa `sudo systemctl stop panel-de-correos`
- Los logs se guardan en journalctl, accesibles con `journalctl -u panel-de-correos`
- Verifica que haya suficiente espacio en disco para MySQL
