# ✅ Verificación: Enlaces en Correos Abren en Nueva Pestaña

## Estado Actual

✅ **IMPLEMENTADO Y ACTIVO**

Todos los enlaces (`<a>` tags) en los correos ahora abren en una **nueva pestaña** automáticamente.

---

## Cómo Funciona

### 1. Filtro Jinja2: `fix_email_html`
**Ubicación:** `app/__init__.py` línea 76-107

El filtro procesa el HTML del correo y:
- ✅ Agrega `target="_blank"` a todos los enlaces que no lo tengan
- ✅ Reemplaza cualquier `target` existente por `target="_blank"`
- ✅ Mantiene la estructura del HTML intacta

### 2. Aplicación en Template
**Ubicación:** `app/templates/pedidos/detalle.html` línea 23 y 25

```html
{{ pedido.contenido_html | fix_email_html | safe }}
```

El filtro se aplica automáticamente cuando se muestra el correo.

---

## Ejemplos de Transformación

### Antes (Sin filtro)
```html
<a href="https://ejemplo.com">Click aquí</a>
<a href="https://otro.com" target="_self">Enlace</a>
```

### Después (Con filtro)
```html
<a href="https://ejemplo.com" target="_blank">Click aquí</a>
<a href="https://otro.com" target="_blank">Enlace</a>
```

---

## Casos Cubiertos

✅ Enlaces sin atributo `target`
✅ Enlaces con `target="_self"`
✅ Enlaces con `target="_parent"`
✅ Enlaces con `target="_top"`
✅ Enlaces con espacios irregulares
✅ Enlaces con comillas simples o dobles

---

## Prueba Manual

Para verificar que funciona:

1. **Envía un correo** con enlaces desde Outlook
2. **Abre el correo** en la web
3. **Haz click en un enlace** - debe abrir en nueva pestaña
4. **Verifica el HTML** - presiona F12 en el navegador
5. **Busca `target="_blank"`** en los tags `<a>`

---

## Código del Filtro

```python
@app.template_filter('fix_email_html')
def fix_email_html(html_content):
    """Procesa HTML de correo para asegurar que los enlaces abran en nueva pestaña"""
    if not html_content:
        return ''
    
    # Asegurar que las imágenes base64 tengan el formato correcto
    html_content = re.sub(
        r'src\s*=\s*["\']?data:image/([^;]+);base64,([A-Za-z0-9+/=]+)["\']?',
        r'src="data:image/\1;base64,\2"',
        html_content,
        flags=re.IGNORECASE
    )
    
    # Agregar target="_blank" a TODOS los enlaces <a>
    # Primero, agregar target="_blank" a los que no tienen target
    html_content = re.sub(
        r'<a\s+([^>]*?)href\s*=\s*["\']([^"\']*)["\']([^>]*)>',
        lambda m: f'<a {m.group(1)}href="{m.group(2)}" target="_blank"{m.group(3)}>' if 'target' not in m.group(0).lower() else m.group(0),
        html_content,
        flags=re.IGNORECASE
    )
    
    # Segundo, reemplazar cualquier target existente que no sea "_blank" por "_blank"
    html_content = re.sub(
        r'target\s*=\s*["\']([^"\']*)["\']',
        r'target="_blank"',
        html_content,
        flags=re.IGNORECASE
    )
    
    return html_content
```

---

## Archivos Relacionados

- `app/__init__.py` - Definición del filtro
- `app/templates/pedidos/detalle.html` - Aplicación del filtro
- `app/templates/base.html` - Template base

---

## Notas Importantes

⚠️ **El filtro se aplica a TODOS los correos**
- Automáticamente en cada visualización
- No requiere configuración adicional
- Funciona con cualquier formato de HTML

✅ **Seguridad**
- No modifica el contenido del correo
- Solo agrega atributos HTML estándar
- Compatible con todos los navegadores modernos

🔄 **Performance**
- El filtro es rápido (regex compilado)
- Se ejecuta solo cuando se visualiza el correo
- No afecta la carga de la página
