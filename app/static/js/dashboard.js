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

// Asignar pedido a usuario (Admin)
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

// Auto-asignar pedido (Logística/Usuario se asignan a sí mismos)
function asignarPedidoAuto(event, pedidoId, usuarioId) {
    event.preventDefault();
    
    // Mostrar confirmación
    const confirmModal = new bootstrap.Modal(document.getElementById('confirmAsignacionModal') || crearModalConfirmacion());
    
    // Guardar datos en el modal para usarlos después
    window.pendingAssignment = { pedidoId, usuarioId };
    
    // Mostrar el modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('confirmAsignacionModal')) || 
                  new bootstrap.Modal(document.getElementById('confirmAsignacionModal'));
    modal.show();
}

// Confirmar auto-asignación después del modal
function confirmarAsignacion() {
    const { pedidoId, usuarioId } = window.pendingAssignment;
    
    // Cerrar modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('confirmAsignacionModal'));
    modal.hide();
    
    // Deshabilitar botón
    const submitBtn = document.querySelector(`#asignarForm-${pedidoId} button[type="submit"]`);
    const originalText = submitBtn ? submitBtn.innerHTML : 'Asignándome...';
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Asignándome...';
    }
    
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
            showToast(data.error || 'Error al asignarte el pedido', 'danger');
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Error al asignarte el pedido', 'danger');
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    });
}

// Crear modal de confirmación si no existe
function crearModalConfirmacion() {
    const modalHTML = `
    <div class="modal fade" id="confirmAsignacionModal" tabindex="-1" data-bs-backdrop="static" data-bs-keyboard="false">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header bg-warning">
                    <h5 class="modal-title">
                        <i class="bi bi-exclamation-triangle"></i> Confirmar Auto-Asignación
                    </h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <p class="mb-3">
                        <strong>¿Estás seguro de que deseas asignarte este pedido?</strong>
                    </p>
                    <div class="alert alert-info">
                        <i class="bi bi-info-circle"></i>
                        Una vez asignado, serás responsable de gestionar este pedido hasta su completación.
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        <i class="bi bi-x-circle"></i> Cancelar
                    </button>
                    <button type="button" class="btn btn-warning" onclick="confirmarAsignacion()">
                        <i class="bi bi-check-circle"></i> Sí, asignarme
                    </button>
                </div>
            </div>
        </div>
    </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    return document.getElementById('confirmAsignacionModal');
}

// Crear modal de confirmación para completar pedido
function crearModalConfirmacionCompletar() {
    const modalHTML = `
    <div class="modal fade" id="confirmCompletarModal" tabindex="-1" data-bs-backdrop="static" data-bs-keyboard="false">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header bg-success">
                    <h5 class="modal-title">
                        <i class="bi bi-exclamation-triangle"></i> Confirmar Completación
                    </h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <p class="mb-3">
                        <strong>¿Estás seguro de que deseas marcar este pedido como completado?</strong>
                    </p>
                    <div class="alert alert-info">
                        <i class="bi bi-info-circle"></i>
                        Una vez completado, el pedido no podrá ser modificado. Asegúrate de que has resuelto correctamente la solicitud del cliente.
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        <i class="bi bi-x-circle"></i> Cancelar
                    </button>
                    <button type="button" class="btn btn-success" onclick="confirmarCompletacion()">
                        <i class="bi bi-check-circle"></i> Sí, completar
                    </button>
                </div>
            </div>
        </div>
    </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    return document.getElementById('confirmCompletarModal');
}

// Completar pedido - Mostrar confirmación
function completarPedido(event, pedidoId) {
    event.preventDefault();
    
    const respuesta = document.getElementById(`respuesta-${pedidoId}`).value.trim();
    
    // Mostrar confirmación
    const confirmModal = new bootstrap.Modal(document.getElementById('confirmCompletarModal') || crearModalConfirmacionCompletar());
    
    // Guardar datos en el modal para usarlos después
    window.pendingCompletion = { pedidoId, respuesta };
    
    // Mostrar el modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('confirmCompletarModal')) || 
                  new bootstrap.Modal(document.getElementById('confirmCompletarModal'));
    modal.show();
}

// Confirmar completación después del modal
function confirmarCompletacion() {
    const { pedidoId, respuesta } = window.pendingCompletion;
    
    // Cerrar modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('confirmCompletarModal'));
    modal.hide();
    
    // Deshabilitar botón
    const submitBtn = document.querySelector(`#completarForm-${pedidoId} button[type="submit"]`);
    const originalText = submitBtn ? submitBtn.innerHTML : 'Completando...';
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Completando...';
    }
    
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
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Error al completar pedido', 'danger');
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
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
