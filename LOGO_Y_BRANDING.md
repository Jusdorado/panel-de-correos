# 🎨 Logo y Branding - Mundosol

## Archivos de Logo

### 1. **Favicon** (`app/static/img/generated-image.png`)
- Tamaño: 256x256px
- Uso: Pestaña del navegador, bookmarks, favoritos
- Formato: SVG escalable
- Colores: Azul (#001689) y Verde (#7ED244)

**Cómo usarlo:**
```html
<!-- Ya está incluido en base.html -->
<link rel="icon" type="image/svg+xml" href="{{ url_for('static', filename='img/generated-image.png') }}">
```

### 2. **Fondo de Login** (`app/static/img/login-background.svg`)
- Tamaño: 1920x1080px (responsive)
- Uso: Fondo animado de la pantalla de login
- Formato: SVG con animaciones CSS
- Características:
  - Gradiente azul a turquesa
  - Formas flotantes animadas
  - Líneas decorativas
  - Efecto blur suave

**Cómo usarlo:**
```css
body {
    background-image: url("{{ url_for('static', filename='img/login-background.svg') }}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
```

### 3. **Imagen Original** (`generated-image.png`)
- Tamaño: 1024x1024px
- Uso: Referencia del logo original
- Formato: PNG con fondo transparente

---

## Dónde Usar el Logo

### ✅ Ya Implementado

| Ubicación | Archivo | Estado |
|-----------|---------|--------|
| Pestaña del navegador | generated-image.png | ✅ Activo |
| Pantalla de login | login-background.svg | ✅ Activo |
| Página base | base.html | ✅ Favicon incluido |

### 🔄 Lugares Donde Puedes Agregarlo

#### 1. **Navbar/Header**
```html
<img src="{{ url_for('static', filename='img/generated-image.png') }}" 
     alt="Mundosol" 
     style="width: 40px; height: 40px;">
```

#### 2. **Dashboard/Home**
```html
<div class="hero-section">
    <img src="{{ url_for('static', filename='img/generated-image.png') }}" 
         alt="Mundosol Logo" 
         class="hero-logo">
</div>
```

#### 3. **Tarjetas de Pedidos**
```html
<div class="card-header">
    <img src="{{ url_for('static', filename='img/generated-image.png') }}" 
         alt="Pedido" 
         style="width: 24px; height: 24px;">
    Pedido #12345
</div>
```

#### 4. **Emails/Notificaciones**
```html
<!-- Usar generated-image.png para emails -->
<img src="cid:mundosol-logo" alt="Mundosol" style="width: 100px;">
```

#### 5. **PDF Reports**
```python
# En reportlab o similar
from PIL import Image
img = Image.open('app/static/img/generated-image.png')
```

---

## Estilos CSS Recomendados

### Logo Pequeño (Navbar)
```css
.navbar-logo {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 22, 137, 0.2);
}
```

### Logo Mediano (Tarjetas)
```css
.card-logo {
    width: 60px;
    height: 60px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 22, 137, 0.15);
}
```

### Logo Grande (Hero)
```css
.hero-logo {
    width: 120px;
    height: 120px;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0, 22, 137, 0.2);
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}
```

---

## Colores del Branding

| Elemento | Color | Hex | RGB |
|----------|-------|-----|-----|
| Azul Principal | Azul Oscuro | #001689 | rgb(0, 22, 137) |
| Azul Secundario | Azul Claro | #0066cc | rgb(0, 102, 204) |
| Verde Acento | Verde Brillante | #7ED244 | rgb(126, 210, 68) |
| Turquesa | Turquesa | #00a8e8 | rgb(0, 168, 232) |

---

## Variantes del Logo

### Versión Completa (Con Texto)
```html
<div class="logo-with-text">
    <img src="{{ url_for('static', filename='img/generated-image.png') }}" alt="Mundosol">
    <span>Mundosol</span>
</div>
```

### Versión Solo Icono
```html
<img src="{{ url_for('static', filename='img/generated-image.png') }}" alt="Mundosol Logo">
```

### Versión Invertida (Fondo Oscuro)
```html
<div style="background: #001689; padding: 10px; border-radius: 8px;">
    <img src="{{ url_for('static', filename='img/generated-image.png') }}" alt="Mundosol">
</div>
```

---

## Responsive Design

El favicon SVG es **completamente escalable** y se adapta automáticamente a cualquier tamaño:

- **16x16px**: Navegador
- **32x32px**: Bookmarks
- **64x64px**: Navbar
- **128x128px**: Tarjetas
- **256x256px**: Pantalla completa

---

## Notas Importantes

⚠️ **Mantener Consistencia**
- Usa siempre el mismo logo en todos los lugares
- Respeta los colores del branding
- No modifiques el logo sin aprobación

✅ **Optimización**
- Los SVG son ligeros y escalables
- Se cargan rápidamente
- Funcionan en todos los navegadores modernos

🎨 **Personalización**
- Si necesitas variantes, crea archivos separados
- Mantén la carpeta `app/static/img/` organizada
- Documenta cualquier cambio

---

## Archivos Relacionados

- `app/static/img/generated-image.png` - Favicon del sitio
- `app/static/img/login-background.svg` - Fondo de login
- `app/static/img/generated-image.png` - Logo original
- `app/templates/base.html` - Template base con favicon
- `app/templates/login.html` - Página de login con branding
