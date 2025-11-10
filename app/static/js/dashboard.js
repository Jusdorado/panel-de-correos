/**
 * Dashboard JavaScript - Mundosol
 * Funciones para gestión de pedidos
 */

// Cargar detalle de pedido via AJAX
function loadPedido(pedidoId) {
    // Marcar item como activo
    document.querySelectorAll('.pedido-item').forEach(item => {
        item.classList.remove('active');
    });
    
    const activeItem = document.querySelector(`[data-pedido-id="${pedidoId}"]`);
    if (activeItem) {
        activeItem.classList.add('active');
    }
    
    // Mostrar spinner
    const detailContainer = document.getElementById('pedido-detail');
    detailContainer.innerHTML = `
        <div class="text-center py-5">
            <div class="spinner-border text-mundosol" role="status">
                <span class="visually-hidden">Cargando...</span>
            </div>
            <p class="mt-3 text-muted">Cargando detalle...</p>
        </div>
    `;
    
    // Cargar detalle
    fetch(`/pedidos/${pedidoId}/detalle`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al cargar el pedido');
            }
            return response.text();
        })
        .then(html => {
            detailContainer.innerHTML = html;
        })
        .catch(error => {
            console.error('Error:', error);
            detailContainer.innerHTML = `
                <div class="alert alert-danger m-3">
                    <i class="bi bi-exclamation-triangle"></i>
                    Error al cargar el detalle del pedido
                </div>
            `;
        });
}

// Asignar pedido a usuario
function asignarPedido(event, pedidoId) {
    event.preventDefault();
    
    const usuarioId = document.getElementById(`usuario-${pedidoId}`).value;
    
    if (!usuarioId) {
        showToast('Debes seleccionar un usuario', 'warning');
        return;
    }
    
    // Deshabilitar botón
    const submitBtn = event.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Asignando...';
    
    fetch(`/pedidos/${pedidoId}/asignar`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ usuario_id: parseInt(usuarioId) })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast(data.message, 'success');
            // Recargar página después de 1 segundo
            setTimeout(() => {
                location.reload();
            }, 1000);
        } else {
            showToast(data.error || 'Error al asignar pedido', 'danger');
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Error al asignar pedido', 'danger');
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    });
}

// Completar pedido
function completarPedido(event, pedidoId) {
    event.preventDefault();
    
    const respuesta = document.getElementById(`respuesta-${pedidoId}`).value.trim();
    
    // Deshabilitar botón
    const submitBtn = event.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Completando...';
    
    fetch(`/pedidos/${pedidoId}/completar`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ respuesta_email: respuesta })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast(data.message, 'success');
            // Recargar página después de 1 segundo
            setTimeout(() => {
                location.reload();
            }, 1000);
        } else {
            showToast(data.error || 'Error al completar pedido', 'danger');
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Error al completar pedido', 'danger');
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    });
}

// Archivar pedido
function archivarPedido(pedidoId) {
    if (!confirm('¿Estás seguro de archivar este pedido?')) {
        return;
    }
    
    fetch(`/pedidos/${pedidoId}/archivar`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast(data.message, 'success');
            // Recargar página después de 1 segundo
            setTimeout(() => {
                location.reload();
            }, 1000);
        } else {
            showToast(data.error || 'Error al archivar pedido', 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Error al archivar pedido', 'danger');
    });
}

// Mostrar toast de notificación
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toastContainer');
    
    // Mapear tipos de Bootstrap
    const bgClass = {
        'success': 'bg-success',
        'danger': 'bg-danger',
        'warning': 'bg-warning',
        'info': 'bg-info'
    }[type] || 'bg-info';
    
    const iconClass = {
        'success': 'bi-check-circle-fill',
        'danger': 'bi-exclamation-triangle-fill',
        'warning': 'bi-exclamation-circle-fill',
        'info': 'bi-info-circle-fill'
    }[type] || 'bi-info-circle-fill';
    
    const toastId = `toast-${Date.now()}`;
    
    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white ${bgClass} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi ${iconClass} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 5000
    });
    
    toast.show();
    
    // Eliminar del DOM después de ocultarse
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

// Auto-refresh cada 30 segundos (opcional, comentado por defecto)
// setInterval(() => {
//     location.reload();
// }, 30000);
